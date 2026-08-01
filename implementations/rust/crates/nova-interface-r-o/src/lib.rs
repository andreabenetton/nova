#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct FlowId(pub u64);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct FlowPayload(pub Vec<u8>);

pub trait RStratumService {
    fn open_flow(&mut self, destination: &[u8]) -> Result<FlowId, RError>;
    fn submit(&mut self, flow: FlowId, payload: FlowPayload) -> Result<(), RError>;
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum RError {
    DestinationUnreachable,
    UnknownFlow,
    Backpressure,
}
