---
adr: ADR-PR-0001
title: Expose aggregated Edges rather than Paths through P-R
scope: p-r-interface
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/p-r/0.2.0
  - contracts/interfaces/p-path-provider/0.4.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-PR-0001: Expose aggregated Edges rather than Paths through P-R

## Context

The original architecture distinguishes P-Stratum Paths from R-Stratum Edges. Multiple Paths may connect the local Node to the same Peer, while P-Stratum is expected to hide lower-layer multiplicity and technology from R-Stratum. The experimental P-R `0.1.0` contract incorrectly exposed `PathId` and `PathKind`.

## Decision

`NOVA-IF-P-R 0.2.0` exposes one Edge per authenticated Peer identity. P-Stratum common consumes Provider Paths, groups them by Node identity, constructs Edge service profiles, selects underlying Paths, and owns multipath policy.

Path Provider instances conforming to P-0AP, P-LAP, or P-RAP implement the internal Path Provider Interface. Provider Paths, provider type, Adapter, Binding, locator, Ethernet, QUIC, and simulation metadata do not cross P-R.

## Architectural boundaries

- Owned by: the P–R Interface, jointly between P-Stratum and R-Stratum.
- Consumed through: `NOVA-IF-P-R`, with P-Stratum common consuming `NOVA-IF-P-PATH-PROVIDER` below it.
- Must not depend on: Path Provider protocol identity, Adapter, Binding, locator, Ethernet, QUIC, or simulation detail.
- Information allowed to cross the boundary: one Edge per authenticated Peer identity, its service profile, and its revision.
- Information prohibited from crossing the boundary: `PathId`, `PathKind`, provider type, and any technology or provenance metadata.

## Interface and contract impact

Introduces `NOVA-IF-P-R 0.2.0` and `NOVA-IF-P-PATH-PROVIDER 0.4.0`. P-Stratum common owns aggregation, Edge service profiles, Path selection, and multipath policy.

## Security and privacy impact

Removing provider provenance from P-R denies R-Stratum and anything above it a view of the local Node's underlay composition. It does not by itself authenticate Peers; Edge identity depends on the authenticated Node identity supplied by the Path Provider instance.

## Alternatives considered

- Expose every Path as an R-Stratum Edge.
- Expose a `PathKind` and let R-Stratum choose technologies.
- Aggregate only multiple Adapters but not P-RAP Paths.

## Consequences

- R-Stratum depends on stable semantic service profiles rather than provider provenance.
- Adding or removing a Path may only update an Edge.
- The last usable Path removes the Edge; later reachability creates a new Edge incarnation.
- P-Stratum common requires an explicit aggregation and queue engine.

## Validation and conformance

- two Provider Paths with one Node identity produce one Edge;
- removal of one Path updates rather than removes the Edge;
- no provider or technology identifier appears in P-R traces;
- R-Stratum runs unchanged over P-0AP, P-LAP, and P-RAP-derived Edges.

## Migration and rollback

Earlier `0.x` versions are preserved as experimental history without any claim of compatibility. A consumer written against `0.1.0` must be updated rather than adapted, because `PathId` and `PathKind` no longer exist at the boundary.

## Unresolved questions

none.
