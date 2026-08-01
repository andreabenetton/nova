// SPDX-License-Identifier: AGPL-3.0-or-later
#![forbid(unsafe_code)]

use nova_interface_p_lap_adapter::PLapAdapter;

pub struct PLap<A: PLapAdapter> {
    adapter: A,
}

impl<A: PLapAdapter> PLap<A> {
    pub const fn new(adapter: A) -> Self {
        Self { adapter }
    }

    pub fn adapter_mut(&mut self) -> &mut A {
        &mut self.adapter
    }
}
