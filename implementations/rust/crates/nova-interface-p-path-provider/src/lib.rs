// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_types::{
    DeliveryProperties, DirectionalMetrics, ExpansionCardinality, InterfaceVersion, Metric,
    NodeIdentity, QueueLimits, Sdu, Urgency,
};

pub const VERSION: InterfaceVersion = InterfaceVersion {
    major: 0,
    minor: 4,
    patch: 0,
};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ProviderInstanceId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ProviderGeneration(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ProviderPathId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ProviderSubmissionId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ProviderEventSequence(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, Ord, PartialOrd)]
pub struct ProviderPathRevision(pub u64);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ProviderEventContext {
    pub instance: ProviderInstanceId,
    pub generation: ProviderGeneration,
    pub sequence: ProviderEventSequence,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ProviderPathProperties {
    pub maximum_sdu_size: u32,
    pub delivery: DeliveryProperties,
    pub priority_prefix_supported: bool,
    pub queue_limits: QueueLimits,
    pub round_trip_latency: Option<Metric>,
    pub outbound: DirectionalMetrics,
    pub inbound: DirectionalMetrics,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ProviderPathSnapshot {
    pub instance: ProviderInstanceId,
    pub generation: ProviderGeneration,
    pub path: ProviderPathId,
    pub revision: ProviderPathRevision,
    pub peer_identity: NodeIdentity,
    pub properties: ProviderPathProperties,
    pub expansion_cardinality: ExpansionCardinality,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ProviderExpansionProfileDescriptor {
    pub profile_id: u32,
    pub maximum_value: u32,
    pub description: String,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ProviderLimits {
    pub maximum_active_paths: u32,
    pub maximum_event_backlog: u32,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ProviderActivated {
    pub instance: ProviderInstanceId,
    pub generation: ProviderGeneration,
    pub limits: ProviderLimits,
    pub expansion_profiles: Vec<ProviderExpansionProfileDescriptor>,
    pub initial_paths: Vec<ProviderPathSnapshot>,
    pub next_event_sequence: ProviderEventSequence,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ProviderSubmissionOptions {
    pub urgency: Urgency,
    pub priority_prefix_length: Option<u32>,
    pub expires_after_micros: Option<u64>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProviderSubmissionStatus {
    DeliveredToPeerProvider,
    PathRemoved,
    Expired,
    ProviderFailure,
    ProviderReset,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ProviderEvent {
    PathAdded {
        context: ProviderEventContext,
        path: ProviderPathSnapshot,
    },
    PathUpdated {
        context: ProviderEventContext,
        path: ProviderPathSnapshot,
    },
    PathRemoved {
        context: ProviderEventContext,
        path: ProviderPathId,
        last_revision: ProviderPathRevision,
    },
    SduReceived {
        context: ProviderEventContext,
        path: ProviderPathId,
        sdu: Sdu,
    },
    SubmissionCompleted {
        context: ProviderEventContext,
        submission: ProviderSubmissionId,
        status: ProviderSubmissionStatus,
    },
    CapacityAvailable {
        context: ProviderEventContext,
        path: ProviderPathId,
    },
    Reset {
        context: ProviderEventContext,
        reason: String,
    },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProviderError {
    UnsupportedConfiguration,
    ProviderUnavailable,
    UnknownProviderInstance,
    UnknownPath,
    PathUnavailable,
    SduTooLarge,
    WouldBlock,
    DuplicateSubmission,
    InvalidOptions,
}

pub trait PathProvider {
    fn activate(&mut self) -> Result<ProviderActivated, ProviderError>;

    fn send_sdu(
        &mut self,
        instance: ProviderInstanceId,
        path: ProviderPathId,
        submission: ProviderSubmissionId,
        options: ProviderSubmissionOptions,
        sdu: Sdu,
    ) -> Result<(), ProviderError>;

    fn deactivate(&mut self, instance: ProviderInstanceId) -> Result<(), ProviderError>;
    fn poll_event(&mut self) -> Option<ProviderEvent>;
}
