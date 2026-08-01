#![forbid(unsafe_code)]

use nova_interface_p_rap_binding::PRapBinding;

pub struct PRap<B: PRapBinding> {
    binding: B,
}

impl<B: PRapBinding> PRap<B> {
    pub const fn new(binding: B) -> Self {
        Self { binding }
    }

    pub fn binding_mut(&mut self) -> &mut B {
        &mut self.binding
    }
}
