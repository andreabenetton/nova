<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Design note: P-Stratum and repository decomposition

This note records the working design developed before the repository scaffold:

- P-LAP and P-RAP are separate peer protocols.
- P-LAP uses Adapters for Nexus Fundamenta.
- P-RAP uses Bindings named for integrated network/transport combinations, initially IPv4-QUIC and IPv6-QUIC.
- P-RAP common behavior is separated from Binding-specific behavior.
- R-Stratum knows only the P-R Interface.
- Every replaceable boundary is represented by a versioned schema-driven contract.
- NIDL uses restricted YAML for authoring, JSON Schema for structural validation, and deterministic JSON for derived fingerprints.
- CI enforces structural, semantic, provider, consumer, interoperability, context, and dependency compliance.
- IP-over-Nova is a Compatibility Service above O-Stratum; NDIS, TUN, and similar mechanisms are Platform Attachments.
