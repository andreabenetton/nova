#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct PlatformInterfaceId(pub u64);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum IpVersion {
    V4,
    V6,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct IpDatagram {
    pub version: IpVersion,
    pub bytes: Vec<u8>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PlatformEvent {
    DatagramReceived { interface: PlatformInterfaceId, datagram: IpDatagram },
    InterfaceFailed { interface: PlatformInterfaceId },
    MtuChanged { interface: PlatformInterfaceId, mtu: u32 },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PlatformError {
    PermissionDenied,
    UnsupportedPlatform,
    UnknownInterface,
    InvalidMtu,
    Backpressure,
    InvalidRoute,
}

pub trait IpPlatformAttachment {
    fn create_interface(&mut self, name: &str) -> Result<PlatformInterfaceId, PlatformError>;
    fn set_mtu(&mut self, interface: PlatformInterfaceId, mtu: u32) -> Result<(), PlatformError>;
    fn inject_datagram(&mut self, interface: PlatformInterfaceId, datagram: IpDatagram) -> Result<(), PlatformError>;
    fn poll_event(&mut self) -> Option<PlatformEvent>;
}
