#![forbid(unsafe_code)]

use nova_interface_p_r::{
    InterfaceOpened, PError, PEvent, PRequest, PResponse, PStratumService, VERSION,
};
use nova_types::{
    CapabilityId, EventSequence, InterfaceInstanceId, InterfaceLimits, InterfaceVersion,
    ObfuscationProfileDescriptor, ObfuscationProfileId,
};

#[derive(Default)]
pub struct PStratumCore {
    next_interface: u64,
}

impl PStratumService for PStratumCore {
    fn version(&self) -> InterfaceVersion {
        VERSION
    }

    fn request(&mut self, request: PRequest) -> Result<PResponse, PError> {
        match request {
            PRequest::OpenInterface(request) => {
                if !request.supported_versions.contains(&VERSION) {
                    return Err(PError::UnsupportedVersion);
                }
                self.next_interface = self
                    .next_interface
                    .checked_add(1)
                    .ok_or(PError::ProviderUnavailable)?;

                let supported_capabilities = [CapabilityId(1), CapabilityId(2)];
                let capabilities = request
                    .requested_capabilities
                    .into_iter()
                    .filter(|requested| supported_capabilities.contains(requested))
                    .collect();

                Ok(PResponse::InterfaceOpened(InterfaceOpened {
                    interface_instance: InterfaceInstanceId(self.next_interface),
                    selected_version: VERSION,
                    capabilities,
                    limits: InterfaceLimits {
                        maximum_edge_count: 1024,
                        maximum_sdu_size: 65_535,
                        maximum_queued_sdus_per_profile: 1024,
                        maximum_queued_bytes_per_profile: 16 * 1024 * 1024,
                        maximum_event_backlog: 4096,
                    },
                    obfuscation_profiles: vec![ObfuscationProfileDescriptor {
                        id: ObfuscationProfileId(0),
                        maximum_value: 65_535,
                        description: "deterministic baseline expansion-cardinality profile"
                            .to_owned(),
                    }],
                    initial_edges: Vec::new(),
                    next_event_sequence: EventSequence(1),
                }))
            }
            PRequest::CloseInterface { .. } => Ok(PResponse::InterfaceClosed),
            PRequest::SubmitSdu { .. } => Err(PError::EdgeUnavailable),
            PRequest::QueryEdge { .. } => Err(PError::UnknownEdge),
        }
    }

    fn poll_event(&mut self) -> Option<PEvent> {
        None
    }
}
