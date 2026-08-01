// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_interface_p_rap_binding::BindingProperties;

pub const fn proposed_quic_properties(maximum_unit_size: u32) -> BindingProperties {
    BindingProperties {
        message_boundaries_preserved: true,
        reliable: true,
        ordered: false,
        congestion_controlled: true,
        effective_maximum_unit_size: maximum_unit_size,
        locator_migration: true,
        unreliable_datagram: true,
    }
}
