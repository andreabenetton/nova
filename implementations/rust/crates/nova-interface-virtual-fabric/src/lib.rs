#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct FabricEndpointId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct FabricLinkId(pub u64);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct FabricUnit(pub Vec<u8>);

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct FabricLinkProperties {
    pub maximum_unit_size: u32,
    pub base_latency_micros: u64,
    pub jitter_micros: u64,
    pub rate_bits_per_second: Option<u64>,
    pub queue_units: u32,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum FabricEvent {
    UnitDelivered {
        destination: FabricEndpointId,
        link: FabricLinkId,
        unit: FabricUnit,
        virtual_time_micros: u64,
    },
    LinkStateChanged {
        link: FabricLinkId,
        available: bool,
    },
    Failed,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum FabricError {
    InvalidConfiguration,
    UnsupportedVersion,
    ResourceLimit,
    DuplicateEndpoint,
    UnknownEndpoint,
    UnknownLink,
    UnitTooLarge,
    Backpressure,
    InvalidTime,
    EventLimit,
    InvalidState,
}

pub trait VirtualFabric {
    fn initialize(&mut self, seed: u64) -> Result<(), FabricError>;
    fn register_endpoint(&mut self) -> Result<FabricEndpointId, FabricError>;
    fn configure_link(
        &mut self,
        source: FabricEndpointId,
        destination: FabricEndpointId,
        properties: FabricLinkProperties,
    ) -> Result<FabricLinkId, FabricError>;
    fn submit_unit(&mut self, link: FabricLinkId, unit: FabricUnit) -> Result<(), FabricError>;
    fn advance_time(&mut self, delta_micros: u64) -> Result<(), FabricError>;
    fn run_until_idle(&mut self) -> Result<(), FabricError>;
    fn poll_event(&mut self) -> Option<FabricEvent>;
}
