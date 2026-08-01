# Changelog

## Unreleased

- Created the Nova architecture scaffold.
- Added strict strata, P-LAP/P-RAP decomposition, Adapters, Bindings, Platform Attachments, and IP-over-Nova separation.
- Added experimental NIDL contracts, generated canonical artifacts, and CI tooling.
- Added Rust boundary crates and proposed ADRs.
- Added P-0AP as a deterministic zero-underlay Path Provider and introduced the reusable Virtual Fabric design.
- Added simulation profiles, scenarios, schemas, implementation stubs, and CI validation.
- Reordered the roadmap so R-Stratum and P-RAP development proceed in parallel, with QUIC before the Ethernet vertical slice.
- Redesigned the P-Stratum/R-Stratum boundary around aggregated Edges in `NOVA-IF-P-R 0.2.0`.
- Added mandatory Obfuscated degree as a privacy-preserving neighbor-expansion cardinality.
- Specified service profiles, authenticated identity, directional metric provenance, atomic reliable SDUs, finite backpressure, lifecycle, reset, sequencing, and race semantics.
- Added `NOVA-IF-P-PATH-PROVIDER 0.3.0` and `NOVA-IF-P-0AP-CONTROL 0.2.0`.
- Added proposed ADRs 0015–0017 and revised the implementation roadmap.
- Refined P-R `0.2.0` with stable Peer handles, address rotation, typed limits, closed metric units, age-based freshness, declared Obfuscated-degree profiles, service-profile removal, orderly close, finite event backlog, and terminal reset ordering.
- Refined Path Provider `0.3.0` with event context, scheduling and expiry options, declared degree profiles, typed metrics, finite event limits, and reset completion semantics.
- Added P-0AP Node-identity update and Path-update control behavior and propagated identity or degree changes as Provider Path updates.
- Added strict NIDL type-reference lint for current development contracts and expanded provider/consumer conformance scenarios.
- Added the experimental Obfuscated-degree profile registry with a deterministic test profile and a proposed positive-noise production profile.
