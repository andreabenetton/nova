// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_interface_p_lap_adapter::{
    AdapterError, AdapterEvent, AdapterFrame, AdapterProperties, NexusLocator, PLapAdapter,
};
use nova_interface_virtual_fabric::VirtualFabric;

pub struct SimulatedAdapter<F: VirtualFabric> {
    fabric: F,
    active: bool,
}

impl<F: VirtualFabric> SimulatedAdapter<F> {
    pub const fn new(fabric: F) -> Self {
        Self {
            fabric,
            active: false,
        }
    }

    pub fn fabric_mut(&mut self) -> &mut F {
        &mut self.fabric
    }
}

impl<F: VirtualFabric> PLapAdapter for SimulatedAdapter<F> {
    fn activate(&mut self) -> Result<AdapterProperties, AdapterError> {
        self.active = true;
        Ok(AdapterProperties {
            effective_maximum_frame_size: 65_535,
            supports_broadcast: true,
            supports_multicast: true,
            point_to_point: false,
        })
    }

    fn send_frame(
        &mut self,
        _destination: &NexusLocator,
        _frame: AdapterFrame,
    ) -> Result<(), AdapterError> {
        if self.active {
            Ok(())
        } else {
            Err(AdapterError::Inactive)
        }
    }

    fn deactivate(&mut self) {
        self.active = false;
    }

    fn poll_event(&mut self) -> Option<AdapterEvent> {
        None
    }
}
