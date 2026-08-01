#![forbid(unsafe_code)]

use nova_types::{PathKind, PathProperties, PeerId, Sdu};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ProviderPathId(pub u64);

#[derive(Clone, Debug, PartialEq)]
pub enum ProviderEvent {
    PathAdded { provider_path: ProviderPathId, peer: PeerId, kind: PathKind, properties: PathProperties },
    PathUpdated { provider_path: ProviderPathId, properties: PathProperties },
    PathRemoved { provider_path: ProviderPathId },
    SduReceived { provider_path: ProviderPathId, sdu: Sdu },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProviderError {
    UnsupportedConfiguration,
    UnknownPath,
    Backpressure,
}

pub trait PathProvider {
    fn activate(&mut self) -> Result<(), ProviderError>;
    fn send_sdu(&mut self, path: ProviderPathId, sdu: Sdu) -> Result<(), ProviderError>;
    fn deactivate(&mut self);
    fn poll_event(&mut self) -> Option<ProviderEvent>;
}
