---
adr: ADR-PR-0001
title: Expose aggregated Edges rather than Paths through P-R
scope: p-r-interface
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-PR-0001: Expose aggregated Edges rather than Paths through P-R

## Context

The original architecture distinguishes P-Stratum Paths from R-Stratum Edges. Multiple Paths may connect the local Node to the same Peer, while P-Stratum is expected to hide lower-layer multiplicity and technology from R-Stratum. The experimental P-R `0.1.0` contract incorrectly exposed `PathId` and `PathKind`.

## Decision

`NOVA-IF-P-R 0.2.0` exposes one Edge per authenticated Peer identity. P-Stratum common consumes Provider Paths, groups them by Node identity, constructs Edge service profiles, selects underlying Paths, and owns multipath policy.

Path Provider instances conforming to P-0AP, P-LAP, or P-RAP implement the internal Path Provider Interface. Provider Paths, provider type, Adapter, Binding, locator, Ethernet, QUIC, and simulation metadata do not cross P-R.

## Consequences

- R-Stratum depends on stable semantic service profiles rather than provider provenance.
- Adding or removing a Path may only update an Edge.
- The last usable Path removes the Edge; later reachability creates a new Edge incarnation.
- P-Stratum common requires an explicit aggregation and queue engine.

## Alternatives considered

- Expose every Path as an R-Stratum Edge.
- Expose a `PathKind` and let R-Stratum choose technologies.
- Aggregate only multiple Adapters but not P-RAP Paths.

## Contract and migration impact

Introduce `NOVA-IF-P-R 0.2.0` and `NOVA-IF-P-PATH-PROVIDER 0.4.0`. Preserve earlier `0.x` versions without claiming compatibility.

## Validation plan

- two Provider Paths with one Node identity produce one Edge;
- removal of one Path updates rather than removes the Edge;
- no provider or technology identifier appears in P-R traces;
- R-Stratum runs unchanged over P-0AP, P-LAP, and P-RAP-derived Edges.
