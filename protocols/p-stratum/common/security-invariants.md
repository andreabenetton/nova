<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-Stratum common security invariants

- A Peer is not reported through the P–R Interface before identity authentication and availability of a compliant delivery capability.
- Node identity remains stable across locator, Adapter, Binding, Path, and QUIC-connection changes.
- Address rotation preserves a Peer only when continuity to the same identity is authenticated.
- Complete unauthenticated or corrupted SDUs are never delivered upward.
- Provider Paths cannot assume another provider's identity, instance, or generation.
- A local Peer handle is never reassigned to a different identity within one Interface instance.
- Expansion-cardinality contributions are profile-bounded and freshness-bounded.
- Event and transfer queues are finite; overload causes explicit backpressure or reset, never silent loss.
- P-0AP conforming results do not establish cryptographic, Ethernet, IP, QUIC, P-LAP, or P-RAP security.
