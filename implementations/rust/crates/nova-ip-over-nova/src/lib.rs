// SPDX-License-Identifier: AGPL-3.0-or-later
#![forbid(unsafe_code)]

use nova_interface_ip_platform_attachment::IpPlatformAttachment;
use nova_interface_o_a::OStratumService;

pub struct IpOverNova<O: OStratumService, P: IpPlatformAttachment> {
    o_stratum: O,
    platform: P,
}

impl<O: OStratumService, P: IpPlatformAttachment> IpOverNova<O, P> {
    pub const fn new(o_stratum: O, platform: P) -> Self {
        Self { o_stratum, platform }
    }

    pub fn parts_mut(&mut self) -> (&mut O, &mut P) {
        (&mut self.o_stratum, &mut self.platform)
    }
}
