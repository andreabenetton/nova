// SPDX-License-Identifier: AGPL-3.0-or-later
#![forbid(unsafe_code)]

use nova_interface_p_0ap_control::P0apControl;

pub struct P0apController<C: P0apControl> {
    controlled: C,
}

impl<C: P0apControl> P0apController<C> {
    pub const fn new(controlled: C) -> Self {
        Self { controlled }
    }

    pub fn controlled_mut(&mut self) -> &mut C {
        &mut self.controlled
    }
}
