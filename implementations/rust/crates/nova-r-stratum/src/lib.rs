// SPDX-License-Identifier: AGPL-3.0-or-later
#![forbid(unsafe_code)]

use nova_interface_p_r::{PStratumService, VERSION};
use nova_types::InterfaceVersion;

pub struct RStratum<P: PStratumService> {
    p_stratum: P,
}

impl<P: PStratumService> RStratum<P> {
    pub const fn new(p_stratum: P) -> Self {
        Self { p_stratum }
    }

    pub const fn required_p_interface() -> InterfaceVersion {
        VERSION
    }

    pub fn p_stratum_mut(&mut self) -> &mut P {
        &mut self.p_stratum
    }
}
