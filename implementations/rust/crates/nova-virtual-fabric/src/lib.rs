// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use std::collections::{HashMap, VecDeque};

use nova_interface_virtual_fabric::{
    FabricEndpointId, FabricError, FabricEvent, FabricLinkId, FabricLinkProperties, FabricUnit,
    VirtualFabric,
};

#[derive(Clone, Copy, Debug)]
struct Link {
    destination: FabricEndpointId,
    properties: FabricLinkProperties,
}

#[derive(Default)]
pub struct ReferenceVirtualFabric {
    initialized: bool,
    virtual_time_micros: u64,
    next_endpoint: u64,
    next_link: u64,
    links: HashMap<FabricLinkId, Link>,
    events: VecDeque<FabricEvent>,
}

impl VirtualFabric for ReferenceVirtualFabric {
    fn initialize(&mut self, _seed: u64) -> Result<(), FabricError> {
        self.initialized = true;
        Ok(())
    }

    fn register_endpoint(&mut self) -> Result<FabricEndpointId, FabricError> {
        if !self.initialized {
            return Err(FabricError::InvalidState);
        }
        self.next_endpoint = self.next_endpoint.checked_add(1).ok_or(FabricError::ResourceLimit)?;
        Ok(FabricEndpointId(self.next_endpoint))
    }

    fn configure_link(
        &mut self,
        _source: FabricEndpointId,
        destination: FabricEndpointId,
        properties: FabricLinkProperties,
    ) -> Result<FabricLinkId, FabricError> {
        if !self.initialized {
            return Err(FabricError::InvalidState);
        }
        self.next_link = self.next_link.checked_add(1).ok_or(FabricError::ResourceLimit)?;
        let id = FabricLinkId(self.next_link);
        self.links.insert(id, Link { destination, properties });
        Ok(id)
    }

    fn submit_unit(&mut self, link: FabricLinkId, unit: FabricUnit) -> Result<(), FabricError> {
        let configured = self.links.get(&link).copied().ok_or(FabricError::UnknownLink)?;
        if unit.0.len() > configured.properties.maximum_unit_size as usize {
            return Err(FabricError::UnitTooLarge);
        }
        let delivery_time = self
            .virtual_time_micros
            .saturating_add(configured.properties.base_latency_micros);
        self.events.push_back(FabricEvent::UnitDelivered {
            destination: configured.destination,
            link,
            unit,
            virtual_time_micros: delivery_time,
        });
        Ok(())
    }

    fn advance_time(&mut self, delta_micros: u64) -> Result<(), FabricError> {
        self.virtual_time_micros = self.virtual_time_micros.saturating_add(delta_micros);
        Ok(())
    }

    fn run_until_idle(&mut self) -> Result<(), FabricError> {
        Ok(())
    }

    fn poll_event(&mut self) -> Option<FabricEvent> {
        self.events.pop_front()
    }
}
