#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct InterfaceVersion {
    pub major: u16,
    pub minor: u16,
    pub patch: u16,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct PeerId(pub [u8; 32]);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct PathId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct SubmissionId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct AssociationId(pub [u8; 16]);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PathKind {
    LinkAdjacent,
    RemoteAssociation,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum DeliveryClass {
    Reliable,
    Unreliable,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Sdu(pub Vec<u8>);

#[derive(Clone, Debug, PartialEq)]
pub struct PathProperties {
    pub kind: PathKind,
    pub maximum_sdu_size: u32,
    pub estimated_latency_micros: Option<u64>,
    pub estimated_jitter_micros: Option<u64>,
    pub estimated_rate_bits_per_second: Option<u64>,
}
