#![forbid(unsafe_code)]

use nova_interface_r_o::RStratumService;

pub struct OStratum<R: RStratumService> {
    r_stratum: R,
}

impl<R: RStratumService> OStratum<R> {
    pub const fn new(r_stratum: R) -> Self {
        Self { r_stratum }
    }

    pub fn r_stratum_mut(&mut self) -> &mut R {
        &mut self.r_stratum
    }
}
