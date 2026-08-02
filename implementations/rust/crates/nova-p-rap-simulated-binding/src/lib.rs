// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_interface_p_rap_binding::{
    BindingError, BindingEvent, BindingInstanceId, BindingProperties, PRapBinding, PrapUnit,
    RemoteLocator,
};
use nova_interface_virtual_fabric::VirtualFabric;

pub struct SimulatedBinding<F: VirtualFabric> {
    fabric: F,
    next_instance: u64,
}

impl<F: VirtualFabric> SimulatedBinding<F> {
    pub const fn new(fabric: F) -> Self {
        Self {
            fabric,
            next_instance: 0,
        }
    }

    pub fn fabric_mut(&mut self) -> &mut F {
        &mut self.fabric
    }
}

impl<F: VirtualFabric> PRapBinding for SimulatedBinding<F> {
    fn open(
        &mut self,
        _remote: RemoteLocator,
    ) -> Result<(BindingInstanceId, BindingProperties), BindingError> {
        self.next_instance = self
            .next_instance
            .checked_add(1)
            .ok_or(BindingError::Unreachable)?;
        Ok((
            BindingInstanceId(self.next_instance),
            BindingProperties {
                message_boundaries_preserved: true,
                reliable: false,
                ordered: false,
                congestion_controlled: false,
                effective_maximum_unit_size: 65_535,
                locator_migration: true,
                unreliable_datagram: true,
            },
        ))
    }

    fn send_unit(
        &mut self,
        _instance: BindingInstanceId,
        _unit: PrapUnit,
    ) -> Result<(), BindingError> {
        Ok(())
    }

    fn close(&mut self, _instance: BindingInstanceId) -> Result<(), BindingError> {
        Ok(())
    }

    fn poll_event(&mut self) -> Option<BindingEvent> {
        None
    }
}
