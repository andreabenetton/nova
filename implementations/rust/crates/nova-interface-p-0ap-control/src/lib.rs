#![forbid(unsafe_code)]

use nova_types::{PathKind, PathProperties};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct SimulationNodeId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct SimulationPathId(pub u64);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProviderComplianceMode {
    Conforming,
    IntentionallyViolating,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum P0apControlError {
    InvalidScenario,
    UnsupportedScenarioVersion,
    ResourceLimit,
    DuplicateNode,
    UnknownNode,
    DuplicatePath,
    UnknownPath,
    InvalidPathKind,
    InvalidCharacteristics,
    InvalidTime,
    EventLimit,
    InvalidTrace,
    ReplayIncompatible,
    InvalidMode,
    InvalidState,
}

pub trait P0apControl {
    fn create_node(&mut self) -> Result<SimulationNodeId, P0apControlError>;
    fn create_path(
        &mut self,
        from: SimulationNodeId,
        to: SimulationNodeId,
        kind: PathKind,
        properties: PathProperties,
    ) -> Result<SimulationPathId, P0apControlError>;
    fn remove_path(&mut self, path: SimulationPathId) -> Result<(), P0apControlError>;
    fn advance_time(&mut self, delta_micros: u64) -> Result<(), P0apControlError>;
    fn run_until_idle(&mut self) -> Result<(), P0apControlError>;
    fn set_provider_compliance_mode(
        &mut self,
        mode: ProviderComplianceMode,
    ) -> Result<(), P0apControlError>;
}
