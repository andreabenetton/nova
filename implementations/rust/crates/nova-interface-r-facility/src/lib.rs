// SPDX-License-Identifier: Apache-2.0
#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub struct FacilityId(pub u64);

pub trait RFacility {
    fn activate(&mut self) -> Result<FacilityId, FacilityError>;
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum FacilityError {
    UnsupportedFacility,
}
