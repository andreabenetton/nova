#![forbid(unsafe_code)]

use std::collections::VecDeque;

use nova_interface_p_0ap_control::{
    P0apControl, P0apControlError, ProviderComplianceMode, SimulationNodeId, SimulationPathId,
};
use nova_interface_p_path_provider::{
    PathProvider, ProviderError, ProviderEvent, ProviderPathId,
};
use nova_interface_virtual_fabric::VirtualFabric;
use nova_types::{PathKind, PathProperties, Sdu};

pub struct P0ap<F: VirtualFabric> {
    fabric: F,
    active: bool,
    next_node: u64,
    next_path: u64,
    mode: ProviderComplianceMode,
    events: VecDeque<ProviderEvent>,
}

impl<F: VirtualFabric> P0ap<F> {
    pub fn new(fabric: F) -> Self {
        Self {
            fabric,
            active: false,
            next_node: 0,
            next_path: 0,
            mode: ProviderComplianceMode::Conforming,
            events: VecDeque::new(),
        }
    }

    pub fn fabric_mut(&mut self) -> &mut F {
        &mut self.fabric
    }
}

impl<F: VirtualFabric> PathProvider for P0ap<F> {
    fn activate(&mut self) -> Result<(), ProviderError> {
        self.active = true;
        Ok(())
    }

    fn send_sdu(&mut self, path: ProviderPathId, sdu: Sdu) -> Result<(), ProviderError> {
        if !self.active {
            return Err(ProviderError::UnsupportedConfiguration);
        }
        self.events.push_back(ProviderEvent::SduReceived { provider_path: path, sdu });
        Ok(())
    }

    fn deactivate(&mut self) {
        self.active = false;
        self.events.clear();
    }

    fn poll_event(&mut self) -> Option<ProviderEvent> {
        self.events.pop_front()
    }
}

impl<F: VirtualFabric> P0apControl for P0ap<F> {
    fn create_node(&mut self) -> Result<SimulationNodeId, P0apControlError> {
        self.next_node = self.next_node.checked_add(1).ok_or(P0apControlError::ResourceLimit)?;
        Ok(SimulationNodeId(self.next_node))
    }

    fn create_path(
        &mut self,
        _from: SimulationNodeId,
        _to: SimulationNodeId,
        kind: PathKind,
        mut properties: PathProperties,
    ) -> Result<SimulationPathId, P0apControlError> {
        self.next_path = self.next_path.checked_add(1).ok_or(P0apControlError::ResourceLimit)?;
        properties.kind = kind;
        let simulated = SimulationPathId(self.next_path);
        self.events.push_back(ProviderEvent::PathAdded {
            provider_path: ProviderPathId(simulated.0),
            peer: nova_types::PeerId([0; 32]),
            kind,
            properties,
        });
        Ok(simulated)
    }

    fn remove_path(&mut self, path: SimulationPathId) -> Result<(), P0apControlError> {
        self.events.push_back(ProviderEvent::PathRemoved { provider_path: ProviderPathId(path.0) });
        Ok(())
    }

    fn advance_time(&mut self, delta_micros: u64) -> Result<(), P0apControlError> {
        self.fabric.advance_time(delta_micros).map_err(|_| P0apControlError::InvalidTime)
    }

    fn run_until_idle(&mut self) -> Result<(), P0apControlError> {
        self.fabric.run_until_idle().map_err(|_| P0apControlError::EventLimit)
    }

    fn set_provider_compliance_mode(
        &mut self,
        mode: ProviderComplianceMode,
    ) -> Result<(), P0apControlError> {
        self.mode = mode;
        Ok(())
    }
}
