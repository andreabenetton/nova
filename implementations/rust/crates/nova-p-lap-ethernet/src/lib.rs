#![forbid(unsafe_code)]

use nova_interface_p_lap_adapter::{AdapterError, AdapterEvent, AdapterFrame, AdapterProperties, NexusLocator, PLapAdapter};

#[derive(Default)]
pub struct EthernetAdapter {
    active: bool,
}

impl PLapAdapter for EthernetAdapter {
    fn activate(&mut self) -> Result<AdapterProperties, AdapterError> {
        self.active = true;
        Ok(AdapterProperties {
            effective_maximum_frame_size: 1500,
            supports_broadcast: true,
            supports_multicast: true,
            point_to_point: false,
        })
    }

    fn send_frame(&mut self, _destination: &NexusLocator, frame: AdapterFrame) -> Result<(), AdapterError> {
        if !self.active {
            return Err(AdapterError::Inactive);
        }
        if frame.0.len() > 1500 {
            return Err(AdapterError::FrameTooLarge);
        }
        Ok(())
    }

    fn deactivate(&mut self) {
        self.active = false;
    }

    fn poll_event(&mut self) -> Option<AdapterEvent> {
        None
    }
}
