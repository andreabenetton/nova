<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Repository status

- Architecture: draft, with private Provider Paths aggregated into R-Stratum-visible Edges
- Normative canon: draft
- NIDL language: experimental `0.1`; strict type-reference lint is opt-in and enabled on current P-Stratum development contracts
- P-R development baseline: experimental `0.2.0`, with identity continuity, Edge profiles, profile-bounded Obfuscated degree, finite queues, close/reset ordering, and exactly-one Submission completion
- Path Provider development baseline: experimental `0.3.0`, with authenticated Paths, declared Obfuscated-degree profiles, scheduling options, finite events, and reset ordering
- P-0AP Control development baseline: experimental `0.2.0`, including Node identity update, Path update, and degree update controls
- Obfuscation profile registry: profile `0` is deterministic test-only; profile `1` is a proposed production shape whose algorithm and privacy analysis remain unresolved
- P-0AP and Virtual Fabric: design, contracts, scenarios, and implementation skeletons; not conformance-complete
- P-Stratum common Edge engine: specified but not implemented
- R-Stratum: design stubs; parallel implementation not started
- P-RAP/QUIC and P-LAP/Ethernet: integration stubs only
- Rust implementation: compilable-intent boundary skeletons; local compilation not verified because the construction environment lacks Rust
- Interoperability: not established
- Security review: not performed

No Interface, peer protocol, wire format, Obfuscated-degree production profile, simulation behavior, or cryptographic choice is stable. P-R `1.0` remains gated on P-0AP, R-Stratum, and an independent P-RAP/QUIC provider passing the same conformance semantics.

## Licensing status

- Split licensing policy: implemented and enforced by `legal/license-policy.yaml`.
- Core crates: AGPL-3.0-or-later.
- Interface and integration crates: Apache-2.0.
- Specifications and documentation: CC-BY-4.0.
- Contracts and schemas: Apache-2.0 OR CC-BY-4.0.
- Historical papers: restricted pending third-party rights review.
- OWFa final-specification registry: empty; no patent commitment is currently attached to a draft.
- Public-release blockers: confirmation of pre-existing rights ownership, review of third-party paper content, trademark clearance, and patent-process review.
