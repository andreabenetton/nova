// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_interface_p_rap_binding::{
    BindingError, BindingEvent, BindingInstanceId, BindingProperties, PRapBinding, PrapUnit,
    RemoteLocator,
};
use nova_p_rap_quic_common::proposed_quic_properties;

#[derive(Default)]
pub struct Ipv6QuicBinding {
    next_instance: u64,
}

impl PRapBinding for Ipv6QuicBinding {
    fn open(
        &mut self,
        remote: RemoteLocator,
    ) -> Result<(BindingInstanceId, BindingProperties), BindingError> {
        if remote.binding.0 != 2 {
            return Err(BindingError::UnsupportedLocator);
        }
        self.next_instance = self.next_instance.saturating_add(1);
        Ok((
            BindingInstanceId(self.next_instance),
            proposed_quic_properties(1200),
        ))
    }

    fn send_unit(
        &mut self,
        _instance: BindingInstanceId,
        unit: PrapUnit,
    ) -> Result<(), BindingError> {
        if unit.0.len() > 1200 {
            return Err(BindingError::UnitTooLarge);
        }
        Ok(())
    }

    fn close(&mut self, _instance: BindingInstanceId) -> Result<(), BindingError> {
        Ok(())
    }

    fn poll_event(&mut self) -> Option<BindingEvent> {
        None
    }
}
