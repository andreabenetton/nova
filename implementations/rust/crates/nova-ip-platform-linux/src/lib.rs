#![forbid(unsafe_code)]

use nova_interface_ip_platform_attachment::{IpDatagram, IpPlatformAttachment, PlatformError, PlatformEvent, PlatformInterfaceId};

#[derive(Default)]
pub struct LinuxTunPlatformAttachment {
    next_interface: u64,
}

impl IpPlatformAttachment for LinuxTunPlatformAttachment {
    fn create_interface(&mut self, _name: &str) -> Result<PlatformInterfaceId, PlatformError> {
        self.next_interface = self.next_interface.saturating_add(1);
        Ok(PlatformInterfaceId(self.next_interface))
    }

    fn set_mtu(&mut self, _interface: PlatformInterfaceId, mtu: u32) -> Result<(), PlatformError> {
        if mtu < 576 {
            return Err(PlatformError::InvalidMtu);
        }
        Ok(())
    }

    fn inject_datagram(&mut self, _interface: PlatformInterfaceId, _datagram: IpDatagram) -> Result<(), PlatformError> {
        Ok(())
    }

    fn poll_event(&mut self) -> Option<PlatformEvent> {
        None
    }
}
