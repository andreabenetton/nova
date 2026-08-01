// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_types::{
    CapabilityId, EdgeId, EdgeRevision, EdgeSnapshot, EventSequence, InterfaceInstanceId,
    InterfaceLimits, InterfaceVersion, ObfuscationProfileDescriptor, Sdu, ServiceProfileId,
    SubmissionId, SubmissionOptions,
};

pub const VERSION: InterfaceVersion = InterfaceVersion {
    major: 0,
    minor: 2,
    patch: 0,
};

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct OpenInterfaceRequest {
    pub supported_versions: Vec<InterfaceVersion>,
    pub requested_capabilities: Vec<CapabilityId>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct InterfaceOpened {
    pub interface_instance: InterfaceInstanceId,
    pub selected_version: InterfaceVersion,
    pub capabilities: Vec<CapabilityId>,
    pub limits: InterfaceLimits,
    pub obfuscation_profiles: Vec<ObfuscationProfileDescriptor>,
    pub initial_edges: Vec<EdgeSnapshot>,
    pub next_event_sequence: EventSequence,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct EventContext {
    pub interface_instance: InterfaceInstanceId,
    pub sequence: EventSequence,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PRequest {
    OpenInterface(OpenInterfaceRequest),
    SubmitSdu {
        interface_instance: InterfaceInstanceId,
        edge: EdgeId,
        submission: SubmissionId,
        options: SubmissionOptions,
        sdu: Sdu,
    },
    QueryEdge {
        interface_instance: InterfaceInstanceId,
        edge: EdgeId,
    },
    CloseInterface {
        interface_instance: InterfaceInstanceId,
    },
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PResponse {
    InterfaceOpened(InterfaceOpened),
    SubmissionAccepted { submission: SubmissionId },
    EdgeSnapshot(EdgeSnapshot),
    InterfaceClosed,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SubmissionTerminalStatus {
    DeliveredToPeerPStratum,
    ServiceProfileRemoved,
    EdgeRemoved,
    Expired,
    ProviderFailure,
    InterfaceReset,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PEvent {
    EdgeAdded {
        context: EventContext,
        edge: EdgeSnapshot,
    },
    EdgeUpdated {
        context: EventContext,
        edge: EdgeSnapshot,
    },
    EdgeRemoved {
        context: EventContext,
        edge: EdgeId,
        last_revision: EdgeRevision,
    },
    SduDelivered {
        context: EventContext,
        edge: EdgeId,
        service_profile: ServiceProfileId,
        sdu: Sdu,
    },
    SubmissionCompleted {
        context: EventContext,
        submission: SubmissionId,
        status: SubmissionTerminalStatus,
    },
    SubmissionCapacityAvailable {
        context: EventContext,
        edge: EdgeId,
        service_profile: ServiceProfileId,
    },
    InterfaceReset {
        context: EventContext,
        reason: String,
    },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PError {
    UnsupportedVersion,
    ProviderUnavailable,
    UnknownInterface,
    UnknownEdge,
    EdgeUnavailable,
    UnknownServiceProfile,
    SduTooLarge,
    WouldBlock,
    DuplicateSubmission,
    InvalidOptions,
}

pub trait PStratumService {
    fn version(&self) -> InterfaceVersion;
    fn request(&mut self, request: PRequest) -> Result<PResponse, PError>;
    fn poll_event(&mut self) -> Option<PEvent>;
}
