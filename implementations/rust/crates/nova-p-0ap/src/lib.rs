// SPDX-License-Identifier: AGPL-3.0-or-later
#![forbid(unsafe_code)]

use std::collections::{BTreeMap, VecDeque};

use nova_interface_p_0ap_control::{
    P0apControl, P0apControlError, ProviderComplianceMode, SimulationNodeId,
    SimulationPathCharacteristics, SimulationPathId,
};
use nova_interface_p_path_provider::{
    PathProvider, ProviderActivated, ProviderError, ProviderEvent, ProviderEventContext,
    ProviderEventSequence, ProviderGeneration, ProviderInstanceId, ProviderLimits,
    ProviderObfuscationProfileDescriptor, ProviderPathId, ProviderPathProperties,
    ProviderPathRevision, ProviderPathSnapshot, ProviderSubmissionId, ProviderSubmissionOptions,
    ProviderSubmissionStatus,
};
use nova_interface_virtual_fabric::VirtualFabric;
use nova_types::{
    DeliveryProperties, DirectionalMetrics, InterSduOrdering, Metric, MetricSource, MetricUnit,
    NodeIdentity, ObfuscatedDegree, ObfuscationProfileId, QueueLimits, Sdu,
};

#[derive(Clone, Debug)]
struct PathRecord {
    from: SimulationNodeId,
    to: SimulationNodeId,
    snapshot: ProviderPathSnapshot,
}

pub struct P0ap<F: VirtualFabric> {
    fabric: F,
    active_instance: Option<ProviderInstanceId>,
    generation: ProviderGeneration,
    next_node: u64,
    next_path: u64,
    next_event: u64,
    mode: ProviderComplianceMode,
    nodes: BTreeMap<SimulationNodeId, NodeIdentity>,
    degrees: BTreeMap<SimulationNodeId, ObfuscatedDegree>,
    paths: BTreeMap<SimulationPathId, PathRecord>,
    events: VecDeque<ProviderEvent>,
}

impl<F: VirtualFabric> P0ap<F> {
    pub fn new(fabric: F) -> Self {
        Self {
            fabric,
            active_instance: None,
            generation: ProviderGeneration(0),
            next_node: 0,
            next_path: 0,
            next_event: 1,
            mode: ProviderComplianceMode::Conforming,
            nodes: BTreeMap::new(),
            degrees: BTreeMap::new(),
            paths: BTreeMap::new(),
            events: VecDeque::new(),
        }
    }

    pub fn fabric_mut(&mut self) -> &mut F {
        &mut self.fabric
    }

    fn next_sequence(&mut self) -> ProviderEventSequence {
        let current = self.next_event;
        self.next_event = self.next_event.saturating_add(1);
        ProviderEventSequence(current)
    }

    fn event_context(&mut self) -> Result<ProviderEventContext, P0apControlError> {
        let instance = self.active_instance.ok_or(P0apControlError::InvalidState)?;
        Ok(ProviderEventContext {
            instance,
            generation: self.generation,
            sequence: self.next_sequence(),
        })
    }

    fn configured_metric(value: u64, unit: MetricUnit) -> Metric {
        Metric {
            value,
            unit,
            source: MetricSource::Configured,
            age_micros: 0,
            sample_window_micros: 0,
            valid_for_micros: u64::MAX,
            confidence_ppm: Some(1_000_000),
        }
    }

    fn properties(characteristics: SimulationPathCharacteristics) -> ProviderPathProperties {
        let latency = Self::configured_metric(
            characteristics.latency_micros,
            MetricUnit::Microseconds,
        );
        let jitter = Self::configured_metric(
            characteristics.jitter_micros,
            MetricUnit::Microseconds,
        );
        let capacity = Self::configured_metric(
            characteristics.bandwidth_bits_per_second,
            MetricUnit::BitsPerSecond,
        );

        ProviderPathProperties {
            maximum_sdu_size: characteristics.maximum_sdu_size,
            delivery: DeliveryProperties {
                reliable: characteristics.reliable,
                atomic_sdu: true,
                boundary_preserving: true,
                inter_sdu_ordering: if characteristics.ordered {
                    InterSduOrdering::Ordered
                } else {
                    InterSduOrdering::None
                },
                duplicate_suppression: true,
            },
            priority_prefix_supported: true,
            queue_limits: QueueLimits {
                maximum_queued_sdus: characteristics.queue_limit_sdus,
                maximum_queued_bytes: characteristics.queue_limit_bytes,
            },
            round_trip_latency: Some(Self::configured_metric(
                characteristics.latency_micros.saturating_mul(2),
                MetricUnit::Microseconds,
            )),
            outbound: DirectionalMetrics {
                estimated_one_way_latency: Some(latency.clone()),
                jitter: Some(jitter.clone()),
                nominal_capacity: Some(capacity.clone()),
                available_capacity: Some(capacity.clone()),
            },
            inbound: DirectionalMetrics {
                estimated_one_way_latency: Some(latency),
                jitter: Some(jitter),
                nominal_capacity: Some(capacity.clone()),
                available_capacity: Some(capacity),
            },
        }
    }

    fn default_degree() -> ObfuscatedDegree {
        ObfuscatedDegree {
            value: 0,
            profile_id: ObfuscationProfileId(0),
            age_micros: 0,
            valid_for_micros: u64::MAX,
        }
    }

    fn update_paths_for_node(
        &mut self,
        node: SimulationNodeId,
    ) -> Result<(), P0apControlError> {
        let identity = self
            .nodes
            .get(&node)
            .cloned()
            .ok_or(P0apControlError::UnknownNode)?;
        let degree = self
            .degrees
            .get(&node)
            .copied()
            .unwrap_or_else(Self::default_degree);

        let affected: Vec<SimulationPathId> = self
            .paths
            .iter()
            .filter_map(|(id, record)| (record.to == node).then_some(*id))
            .collect();

        for id in affected {
            let updated = {
                let record = self.paths.get_mut(&id).ok_or(P0apControlError::UnknownPath)?;
                record.snapshot.revision = ProviderPathRevision(
                    record.snapshot.revision.0.saturating_add(1),
                );
                record.snapshot.peer_identity = identity.clone();
                record.snapshot.obfuscated_degree = degree;
                record.snapshot.clone()
            };
            let context = self.event_context()?;
            self.events
                .push_back(ProviderEvent::PathUpdated { context, path: updated });
        }
        Ok(())
    }
}

impl<F: VirtualFabric> PathProvider for P0ap<F> {
    fn activate(&mut self) -> Result<ProviderActivated, ProviderError> {
        if self.active_instance.is_some() {
            return Err(ProviderError::UnsupportedConfiguration);
        }
        self.fabric
            .initialize(self.generation.0.saturating_add(1))
            .map_err(|_| ProviderError::ProviderUnavailable)?;
        self.generation.0 = self.generation.0.saturating_add(1);
        let instance = ProviderInstanceId(self.generation.0);
        self.active_instance = Some(instance);
        self.next_event = 1;
        for record in self.paths.values_mut() {
            record.snapshot.instance = instance;
            record.snapshot.generation = self.generation;
            record.snapshot.revision = ProviderPathRevision(1);
        }
        Ok(ProviderActivated {
            instance,
            generation: self.generation,
            limits: ProviderLimits {
                maximum_active_paths: 65_535,
                maximum_event_backlog: 4_096,
            },
            obfuscation_profiles: vec![ProviderObfuscationProfileDescriptor {
                profile_id: 0,
                maximum_value: 65_535,
                description: "deterministic test profile".to_owned(),
            }],
            initial_paths: self
                .paths
                .values()
                .map(|record| record.snapshot.clone())
                .collect(),
            next_event_sequence: ProviderEventSequence(self.next_event),
        })
    }

    fn send_sdu(
        &mut self,
        instance: ProviderInstanceId,
        path: ProviderPathId,
        submission: ProviderSubmissionId,
        options: ProviderSubmissionOptions,
        sdu: Sdu,
    ) -> Result<(), ProviderError> {
        if self.active_instance != Some(instance) {
            return Err(ProviderError::UnknownProviderInstance);
        }
        let record = self
            .paths
            .get(&SimulationPathId(path.0))
            .ok_or(ProviderError::UnknownPath)?;
        if sdu.0.len() > record.snapshot.properties.maximum_sdu_size as usize {
            return Err(ProviderError::SduTooLarge);
        }
        if options
            .priority_prefix_length
            .is_some_and(|length| length as usize > sdu.0.len())
        {
            return Err(ProviderError::InvalidOptions);
        }

        if options.expires_after_micros == Some(0) {
            let context = ProviderEventContext {
                instance,
                generation: self.generation,
                sequence: self.next_sequence(),
            };
            self.events.push_back(ProviderEvent::SubmissionCompleted {
                context,
                submission,
                status: ProviderSubmissionStatus::Expired,
            });
            return Ok(());
        }

        let received_context = ProviderEventContext {
            instance,
            generation: self.generation,
            sequence: self.next_sequence(),
        };
        self.events.push_back(ProviderEvent::SduReceived {
            context: received_context,
            path,
            sdu,
        });

        let completed_context = ProviderEventContext {
            instance,
            generation: self.generation,
            sequence: self.next_sequence(),
        };
        self.events.push_back(ProviderEvent::SubmissionCompleted {
            context: completed_context,
            submission,
            status: ProviderSubmissionStatus::DeliveredToPeerProvider,
        });
        Ok(())
    }

    fn deactivate(&mut self, instance: ProviderInstanceId) -> Result<(), ProviderError> {
        if self.active_instance != Some(instance) {
            return Err(ProviderError::UnknownProviderInstance);
        }
        self.active_instance = None;
        self.events.clear();
        Ok(())
    }

    fn poll_event(&mut self) -> Option<ProviderEvent> {
        self.events.pop_front()
    }
}

impl<F: VirtualFabric> P0apControl for P0ap<F> {
    fn create_node(&mut self, identity: NodeIdentity) -> Result<SimulationNodeId, P0apControlError> {
        if !identity.is_valid() {
            return Err(P0apControlError::InvalidScenario);
        }
        if self.nodes.values().any(|known| known.id == identity.id) {
            return Err(P0apControlError::DuplicateIdentity);
        }
        self.next_node = self
            .next_node
            .checked_add(1)
            .ok_or(P0apControlError::ResourceLimit)?;
        let node = SimulationNodeId(self.next_node);
        self.nodes.insert(node, identity);
        Ok(node)
    }

    fn update_node_identity(
        &mut self,
        node: SimulationNodeId,
        identity: NodeIdentity,
    ) -> Result<(), P0apControlError> {
        if !identity.is_valid() {
            return Err(P0apControlError::InvalidScenario);
        }
        if self
            .nodes
            .iter()
            .any(|(known_node, known)| *known_node != node && known.id == identity.id)
        {
            return Err(P0apControlError::DuplicateIdentity);
        }
        let current = self.nodes.get_mut(&node).ok_or(P0apControlError::UnknownNode)?;
        *current = identity;
        self.update_paths_for_node(node)
    }

    fn create_path(
        &mut self,
        from: SimulationNodeId,
        to: SimulationNodeId,
        characteristics: SimulationPathCharacteristics,
    ) -> Result<SimulationPathId, P0apControlError> {
        if from == to {
            return Err(P0apControlError::SelfLoopNotAllowed);
        }
        if !characteristics.is_valid() {
            return Err(P0apControlError::InvalidCharacteristics);
        }
        if !self.nodes.contains_key(&from) || !self.nodes.contains_key(&to) {
            return Err(P0apControlError::UnknownNode);
        }
        if self.active_instance.is_none() {
            return Err(P0apControlError::InvalidState);
        }
        if self
            .paths
            .values()
            .any(|record| record.from == from && record.to == to)
        {
            return Err(P0apControlError::DuplicatePath);
        }

        self.next_path = self
            .next_path
            .checked_add(1)
            .ok_or(P0apControlError::ResourceLimit)?;
        let simulated = SimulationPathId(self.next_path);
        let peer_identity = self
            .nodes
            .get(&to)
            .cloned()
            .ok_or(P0apControlError::UnknownNode)?;
        let degree = self
            .degrees
            .get(&to)
            .copied()
            .unwrap_or_else(Self::default_degree);
        let snapshot = ProviderPathSnapshot {
            instance: self.active_instance.ok_or(P0apControlError::InvalidState)?,
            generation: self.generation,
            path: ProviderPathId(simulated.0),
            revision: ProviderPathRevision(1),
            peer_identity,
            properties: Self::properties(characteristics),
            obfuscated_degree: degree,
        };
        self.paths.insert(
            simulated,
            PathRecord {
                from,
                to,
                snapshot: snapshot.clone(),
            },
        );
        let context = self.event_context()?;
        self.events
            .push_back(ProviderEvent::PathAdded { context, path: snapshot });
        Ok(simulated)
    }

    fn update_path(
        &mut self,
        path: SimulationPathId,
        characteristics: SimulationPathCharacteristics,
    ) -> Result<(), P0apControlError> {
        if !characteristics.is_valid() {
            return Err(P0apControlError::InvalidCharacteristics);
        }
        let updated = {
            let record = self.paths.get_mut(&path).ok_or(P0apControlError::UnknownPath)?;
            record.snapshot.revision = ProviderPathRevision(
                record.snapshot.revision.0.saturating_add(1),
            );
            record.snapshot.properties = Self::properties(characteristics);
            record.snapshot.clone()
        };
        let context = self.event_context()?;
        self.events
            .push_back(ProviderEvent::PathUpdated { context, path: updated });
        Ok(())
    }

    fn set_obfuscated_degree(
        &mut self,
        node: SimulationNodeId,
        degree: ObfuscatedDegree,
    ) -> Result<(), P0apControlError> {
        if !self.nodes.contains_key(&node) {
            return Err(P0apControlError::UnknownNode);
        }
        if degree.valid_for_micros == 0
            || degree.profile_id != ObfuscationProfileId(0)
            || degree.value > 65_535
        {
            return Err(P0apControlError::InvalidObfuscatedDegree);
        }
        self.degrees.insert(node, degree);
        self.update_paths_for_node(node)
    }

    fn remove_path(&mut self, path: SimulationPathId) -> Result<(), P0apControlError> {
        let removed = self
            .paths
            .remove(&path)
            .ok_or(P0apControlError::UnknownPath)?;
        let context = self.event_context()?;
        self.events.push_back(ProviderEvent::PathRemoved {
            context,
            path: ProviderPathId(path.0),
            last_revision: removed.snapshot.revision,
        });
        Ok(())
    }

    fn advance_time(&mut self, delta_micros: u64) -> Result<(), P0apControlError> {
        self.fabric
            .advance_time(delta_micros)
            .map_err(|_| P0apControlError::InvalidTime)
    }

    fn run_until_idle(&mut self) -> Result<(), P0apControlError> {
        self.fabric
            .run_until_idle()
            .map_err(|_| P0apControlError::EventLimit)
    }

    fn set_provider_compliance_mode(
        &mut self,
        mode: ProviderComplianceMode,
    ) -> Result<(), P0apControlError> {
        self.mode = mode;
        Ok(())
    }
}
