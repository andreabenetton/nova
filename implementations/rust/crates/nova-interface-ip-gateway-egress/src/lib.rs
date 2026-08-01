// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

use nova_types::Sdu;

pub trait IpGatewayEgress {
    fn forward(&mut self, datagram: Sdu) -> Result<(), GatewayError>;
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum GatewayError {
    EgressUnavailable,
    PolicyDenied,
}
