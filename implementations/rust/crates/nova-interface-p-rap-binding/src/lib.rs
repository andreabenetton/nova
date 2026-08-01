// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct BindingInstanceId(pub u64);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct BindingId(pub u16);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RemoteLocator {
    pub binding: BindingId,
    pub value: Vec<u8>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PrapUnit(pub Vec<u8>);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct BindingProperties {
    pub message_boundaries_preserved: bool,
    pub reliable: bool,
    pub ordered: bool,
    pub congestion_controlled: bool,
    pub effective_maximum_unit_size: u32,
    pub locator_migration: bool,
    pub unreliable_datagram: bool,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum BindingEvent {
    UnitReceived { instance: BindingInstanceId, unit: PrapUnit },
    PropertiesChanged { instance: BindingInstanceId, properties: BindingProperties },
    InstanceFailed { instance: BindingInstanceId },
    RemoteLocatorChanged { instance: BindingInstanceId, locator: RemoteLocator },
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum BindingError {
    UnsupportedLocator,
    Unreachable,
    AuthenticationFailed,
    UnknownInstance,
    UnitTooLarge,
    Backpressure,
}

pub trait PRapBinding {
    fn open(&mut self, remote: RemoteLocator) -> Result<(BindingInstanceId, BindingProperties), BindingError>;
    fn send_unit(&mut self, instance: BindingInstanceId, unit: PrapUnit) -> Result<(), BindingError>;
    fn close(&mut self, instance: BindingInstanceId) -> Result<(), BindingError>;
    fn poll_event(&mut self) -> Option<BindingEvent>;
}
