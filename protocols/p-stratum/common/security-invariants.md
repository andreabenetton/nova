# P-Stratum common security invariants

- An Edge is not exposed before Peer identity authentication and availability of a compliant service profile.
- Node identity is stable across locator, Adapter, Binding, Path, and QUIC connection changes.
- Address rotation preserves a Peer only when continuity to the same identity identifier is authenticated.
- Complete unauthenticated or corrupted SDUs are never delivered upward.
- Provider Paths cannot assume another provider's identity, instance, or generation.
- An `EdgeId` is never reused; a `PeerHandle` is never reassigned to a different identity.
- Obfuscated degree is a profile-bounded privacy hint with freshness semantics, not an exact topology claim.
- Event and Submission queues are finite; overload causes explicit backpressure or reset, never silent loss.
- P-0AP conforming results do not establish cryptographic, Ethernet, IP, QUIC, P-LAP, or P-RAP security.
