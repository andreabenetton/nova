<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Changelog

## Unreleased

- Classified P-0AP, P-LAP, and P-RAP as Path Provider protocols; distinguished protocol, implementation, and runtime instance.
- Corrected remaining mutable documentation so P-0AP, P-LAP, and P-RAP are never described as runtime Path Providers; implementations and instances are named explicitly.
- Added the normative P-Stratum objectives document and wired it into scoped agent and context manifests.
- Published `NOVA-IF-P-PATH-PROVIDER 0.4.0` with the provider role expressed as a Path Provider instance.
- Split the unified glossary into common, P-Stratum, R-Stratum, O-Stratum, and Interface-owned glossaries.
- Added term-ownership metadata, scoped agent instructions, context boundaries, and CI terminology enforcement.
- Moved Path-to-Edge and Obfuscated-Degree mappings exclusively into the P–R Interface documentation.
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
- Added `NOVA-IF-P-PATH-PROVIDER 0.4.0` and `NOVA-IF-P-0AP-CONTROL 0.3.0`.
- Added proposed ADRs 0015–0017 and revised the implementation roadmap.
- Refined P-R `0.2.0` with stable Peer handles, address rotation, typed limits, closed metric units, age-based freshness, declared Obfuscated-degree profiles, service-profile removal, orderly close, finite event backlog, and terminal reset ordering.
- Refined Path Provider `0.3.0` with event context, scheduling and expiry options, declared degree profiles, typed metrics, finite event limits, and reset completion semantics.
- Added P-0AP Node-identity update and Path-update control behavior and propagated identity or degree changes as Provider Path updates.
- Added strict NIDL type-reference lint for current development contracts and expanded provider/consumer conformance scenarios.
- Added the experimental Obfuscated-degree profile registry with a deterministic test profile and a proposed positive-noise production profile.

## Unreleased — licensing architecture

- adopted AGPL-3.0-or-later for the Nova core implementation;
- adopted Apache-2.0 for Interfaces, Adapters, Bindings, Platform Attachments,
  shared SDK types, conformance code, tooling, tests, and examples;
- adopted CC-BY-4.0 for project-authored documentation and specification prose;
- dual-licensed contracts, schemas, registries, and simulation fixtures under
  Apache-2.0 OR CC-BY-4.0;
- restricted historical research PDFs pending third-party rights review;
- added SPDX metadata, per-directory license markers, DCO, patent, copyright,
  trademark, and third-party notice files; and
- added deterministic license-policy CI enforcement.
