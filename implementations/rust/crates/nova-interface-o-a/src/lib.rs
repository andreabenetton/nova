// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct ApplicationEndpointId(pub u64);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Message(pub Vec<u8>);

pub trait OStratumService {
    fn open_endpoint(&mut self, profile: &str) -> Result<ApplicationEndpointId, OError>;
    fn send_message(&mut self, endpoint: ApplicationEndpointId, message: Message) -> Result<(), OError>;
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum OError {
    UnsupportedProfile,
    UnknownEndpoint,
    Backpressure,
}
