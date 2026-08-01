#![forbid(unsafe_code)]

use nova_interface_p_r::{PError, PEvent, PRequest, PResponse, PStratumService, VERSION};
use nova_types::InterfaceVersion;

#[derive(Default)]
pub struct PStratumCore;

impl PStratumService for PStratumCore {
    fn version(&self) -> InterfaceVersion {
        VERSION
    }

    fn request(&mut self, request: PRequest) -> Result<PResponse, PError> {
        match request {
            PRequest::OpenInterface => Ok(PResponse::InterfaceOpened),
            _ => Err(PError::PathUnavailable),
        }
    }

    fn poll_event(&mut self) -> Option<PEvent> {
        None
    }
}
