// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct AdapterId(pub u64);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NexusLocator(pub Vec<u8>);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AdapterFrame(pub Vec<u8>);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct AdapterProperties {
    pub effective_maximum_frame_size: u32,
    pub supports_broadcast: bool,
    pub supports_multicast: bool,
    pub point_to_point: bool,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AdapterEvent {
    FrameReceived { source: NexusLocator, frame: AdapterFrame },
    PropertiesChanged(AdapterProperties),
    Failed,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AdapterError {
    UnsupportedNexus,
    PermissionDenied,
    Inactive,
    FrameTooLarge,
    Backpressure,
}

pub trait PLapAdapter {
    fn activate(&mut self) -> Result<AdapterProperties, AdapterError>;
    fn send_frame(&mut self, destination: &NexusLocator, frame: AdapterFrame) -> Result<(), AdapterError>;
    fn deactivate(&mut self);
    fn poll_event(&mut self) -> Option<AdapterEvent>;
}
