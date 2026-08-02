// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct InterfaceVersion {
    pub major: u16,
    pub minor: u16,
    pub patch: u16,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct InterfaceInstanceId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, Ord, PartialOrd)]
pub struct EventSequence(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct PeerHandle(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct EdgeId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, Ord, PartialOrd)]
pub struct EdgeRevision(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ServiceProfileId(pub u32);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct SubmissionId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct CapabilityId(pub u32);

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct CryptographicSuiteId(pub u32);

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct NodeAddress {
    pub cryptographic_suite: CryptographicSuiteId,
    pub address_digest: Vec<u8>,
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct NodeIdentityId {
    pub profile_id: u32,
    pub digest: Vec<u8>,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct NodeIdentity {
    pub id: NodeIdentityId,
    pub addresses: Vec<NodeAddress>,
}

impl NodeIdentity {
    #[must_use]
    pub fn is_valid(&self) -> bool {
        if self.id.digest.is_empty() || self.addresses.is_empty() {
            return false;
        }

        let mut previous: Option<(&CryptographicSuiteId, &[u8])> = None;
        for address in &self.addresses {
            if address.address_digest.is_empty() {
                return false;
            }
            let current = (
                &address.cryptographic_suite,
                address.address_digest.as_slice(),
            );
            if let Some(previous) = previous {
                if previous >= current {
                    return false;
                }
            }
            previous = Some(current);
        }
        true
    }

    #[must_use]
    pub fn same_identity(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum MetricSource {
    Measured,
    Configured,
    Declared,
    Derived,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum MetricUnit {
    Microseconds,
    BitsPerSecond,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Metric {
    pub value: u64,
    pub unit: MetricUnit,
    pub source: MetricSource,
    pub age_micros: u64,
    pub sample_window_micros: u64,
    pub valid_for_micros: u64,
    pub confidence_ppm: Option<u32>,
}

impl Metric {
    #[must_use]
    pub fn is_valid(&self) -> bool {
        self.confidence_ppm.is_none_or(|value| value <= 1_000_000)
    }

    #[must_use]
    pub fn is_fresh_after(&self, elapsed_since_snapshot_micros: u64) -> bool {
        self.age_micros
            .saturating_add(elapsed_since_snapshot_micros)
            < self.valid_for_micros
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum InterSduOrdering {
    None,
    Ordered,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct DeliveryProperties {
    pub reliable: bool,
    pub atomic_sdu: bool,
    pub boundary_preserving: bool,
    pub inter_sdu_ordering: InterSduOrdering,
    pub duplicate_suppression: bool,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct QueueLimits {
    pub maximum_queued_sdus: u32,
    pub maximum_queued_bytes: u64,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DirectionalMetrics {
    pub estimated_one_way_latency: Option<Metric>,
    pub jitter: Option<Metric>,
    pub nominal_capacity: Option<Metric>,
    pub available_capacity: Option<Metric>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EdgeServiceProfile {
    pub id: ServiceProfileId,
    pub maximum_sdu_size: u32,
    pub delivery: DeliveryProperties,
    pub queue_limits: QueueLimits,
    pub round_trip_latency: Option<Metric>,
    pub outbound: DirectionalMetrics,
    pub inbound: DirectionalMetrics,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ObfuscationProfileId(pub u32);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ObfuscationProfileDescriptor {
    pub id: ObfuscationProfileId,
    pub maximum_value: u32,
    pub description: String,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ObfuscatedDegree {
    pub value: u32,
    pub profile_id: ObfuscationProfileId,
    pub age_micros: u64,
    pub valid_for_micros: u64,
}

impl ObfuscatedDegree {
    #[must_use]
    pub fn is_fresh_after(&self, elapsed_since_snapshot_micros: u64) -> bool {
        self.age_micros
            .saturating_add(elapsed_since_snapshot_micros)
            < self.valid_for_micros
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ExpansionProfileId(pub u32);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExpansionProfileDescriptor {
    pub id: ExpansionProfileId,
    pub maximum_value: u32,
    pub description: String,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ExpansionCardinality {
    pub value: u32,
    pub profile_id: ExpansionProfileId,
    pub age_micros: u64,
    pub valid_for_micros: u64,
}

impl ExpansionCardinality {
    #[must_use]
    pub fn is_fresh_after(&self, elapsed_since_snapshot_micros: u64) -> bool {
        self.age_micros
            .saturating_add(elapsed_since_snapshot_micros)
            < self.valid_for_micros
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct InterfaceLimits {
    pub maximum_edge_count: u32,
    pub maximum_sdu_size: u32,
    pub maximum_queued_sdus_per_profile: u32,
    pub maximum_queued_bytes_per_profile: u64,
    pub maximum_event_backlog: u32,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EdgeSnapshot {
    pub interface_instance: InterfaceInstanceId,
    pub edge: EdgeId,
    pub revision: EdgeRevision,
    pub peer: PeerHandle,
    pub node_identity: NodeIdentity,
    pub service_profiles: Vec<EdgeServiceProfile>,
    pub obfuscated_degree: ObfuscatedDegree,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Urgency {
    Background,
    Normal,
    Urgent,
    Critical,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct SubmissionOptions {
    pub service_profile: ServiceProfileId,
    pub urgency: Urgency,
    pub priority_prefix_length: Option<u32>,
    pub expires_after_micros: Option<u64>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Sdu(pub Vec<u8>);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct AssociationId(pub [u8; 16]);
