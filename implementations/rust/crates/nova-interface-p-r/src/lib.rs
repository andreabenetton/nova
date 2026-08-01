#![forbid(unsafe_code)]

use nova_types::{DeliveryClass, InterfaceVersion, PathId, PathProperties, PeerId, Sdu, SubmissionId};

pub const VERSION: InterfaceVersion = InterfaceVersion { major: 0, minor: 1, patch: 0 };

#[derive(Clone, Debug, PartialEq)]
pub enum PRequest {
    OpenInterface,
    SubmitSdu { path: PathId, submission: SubmissionId, class: DeliveryClass, sdu: Sdu },
    CancelSubmission { submission: SubmissionId },
    QueryPath { path: PathId },
}

#[derive(Clone, Debug, PartialEq)]
pub enum PResponse {
    InterfaceOpened,
    SubmissionAccepted,
    SubmissionCancelled,
    PathSnapshot { peer: PeerId, properties: PathProperties },
}

#[derive(Clone, Debug, PartialEq)]
pub enum PEvent {
    PathAdded { path: PathId, peer: PeerId, properties: PathProperties },
    PathUpdated { path: PathId, properties: PathProperties },
    PathRemoved { path: PathId },
    SduDelivered { path: PathId, peer: PeerId, sdu: Sdu },
    SubmissionResult { submission: SubmissionId, delivered: bool },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PError {
    UnsupportedVersion,
    UnknownPath,
    PathUnavailable,
    SduTooLarge,
    Backpressure,
    UnknownSubmission,
    TooLate,
}

pub trait PStratumService {
    fn version(&self) -> InterfaceVersion;
    fn request(&mut self, request: PRequest) -> Result<PResponse, PError>;
    fn poll_event(&mut self) -> Option<PEvent>;
}
