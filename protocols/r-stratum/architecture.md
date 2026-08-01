<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# R-Stratum architecture

The first executable R-Stratum subset separates:

- Edge consumption and Close lifecycle;
- topology discovery and Neighbor expansion;
- Route-label lifecycle;
- Link identification and service-characteristic collection;
- Flow setup;
- Gram processing and forwarding;
- optional Facilities.

Through the P–R Interface, each exposed Edge establishes one Close in the local R-Stratum view. R-Stratum consumes only the Interface's delivery capabilities and metrics; it does not depend on how the lower stratum realizes them.

Traffic payments, monetary issuance, proof of bandwidth, and validating consensus remain outside the mandatory first subset.
