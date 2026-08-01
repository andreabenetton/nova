// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_types::{NodeIdentity, ObfuscatedDegree};

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct SimulationNodeId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct SimulationPathId(pub u64);

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SimulationPathCharacteristics {
    pub maximum_sdu_size: u32,
    pub reliable: bool,
    pub ordered: bool,
    pub queue_limit_sdus: u32,
    pub queue_limit_bytes: u64,
    pub latency_micros: u64,
    pub jitter_micros: u64,
    pub bandwidth_bits_per_second: u64,
    pub loss_probability_ppm: u32,
    pub duplication_probability_ppm: u32,
    pub reordering_probability_ppm: u32,
}

impl SimulationPathCharacteristics {
    #[must_use]
    pub fn is_valid(&self) -> bool {
        self.maximum_sdu_size > 0
            && self.queue_limit_sdus > 0
            && self.queue_limit_bytes > 0
            && self.loss_probability_ppm <= 1_000_000
            && self.duplication_probability_ppm <= 1_000_000
            && self.reordering_probability_ppm <= 1_000_000
    }
}

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
    DuplicateIdentity,
    UnknownNode,
    DuplicatePath,
    UnknownPath,
    SelfLoopNotAllowed,
    InvalidCharacteristics,
    InvalidObfuscatedDegree,
    InvalidTime,
    EventLimit,
    NoRecording,
    InvalidTrace,
    UnsupportedTraceVersion,
    ReplayIncompatible,
    InvalidMode,
    InvalidState,
}

pub trait P0apControl {
    fn create_node(&mut self, identity: NodeIdentity) -> Result<SimulationNodeId, P0apControlError>;

    fn update_node_identity(
        &mut self,
        node: SimulationNodeId,
        identity: NodeIdentity,
    ) -> Result<(), P0apControlError>;

    fn create_path(
        &mut self,
        from: SimulationNodeId,
        to: SimulationNodeId,
        characteristics: SimulationPathCharacteristics,
    ) -> Result<SimulationPathId, P0apControlError>;

    fn update_path(
        &mut self,
        path: SimulationPathId,
        characteristics: SimulationPathCharacteristics,
    ) -> Result<(), P0apControlError>;

    fn set_obfuscated_degree(
        &mut self,
        node: SimulationNodeId,
        degree: ObfuscatedDegree,
    ) -> Result<(), P0apControlError>;

    fn remove_path(&mut self, path: SimulationPathId) -> Result<(), P0apControlError>;
    fn advance_time(&mut self, delta_micros: u64) -> Result<(), P0apControlError>;
    fn run_until_idle(&mut self) -> Result<(), P0apControlError>;

    fn set_provider_compliance_mode(
        &mut self,
        mode: ProviderComplianceMode,
    ) -> Result<(), P0apControlError>;
}
