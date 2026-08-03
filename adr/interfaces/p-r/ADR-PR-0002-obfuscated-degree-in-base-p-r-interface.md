---
adr: ADR-PR-0002
title: Include Obfuscated degree in the base P-R Interface
scope: p-r-interface
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/p-r/0.2.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-PR-0002: Include Obfuscated degree in the base P-R Interface

## Context

The R-Stratum topology-discovery design needs a privacy-preserving cardinality telling a Node how many neighbor-expansion slots to prepare through a Close. The P-Stratum paper describes an obfuscated degree derived by excluding common Peers and adding positive noise. Omitting it from P-R would leave a required cross-stratum input undefined.

## Decision

Every Edge snapshot in `NOVA-IF-P-R 0.2.0` includes `ObfuscatedDegree`. Its observable meaning is strictly the number of neighbor-expansion slots R-Stratum prepares. It is not an exact Peer degree, Path count, physical topology claim, or verified remote fact.

The value includes a profile identifier, age at snapshot emission, and validity duration. Interface opening declares every profile that may appear and its maximum value. The base Interface freezes presence, bounds, expansion-cardinality meaning, zero semantics, freshness, and update behavior. Noise distribution, common-Peer detection, dummy-slot realization, and profile algorithms remain separately versioned below the boundary.

## Architectural boundaries

- Owned by: the P–R Interface.
- Consumed through: `NOVA-IF-P-R`, as a field of every Edge snapshot.
- Must not depend on: the noise distribution, common-Peer detection, or dummy-slot realization of any profile.
- Information allowed to cross the boundary: the profile identifier, the bounded value, its age at emission, and its validity duration.
- Information prohibited from crossing the boundary: exact Peer degree, Provider Path count, and any verified claim about remote topology.

## Interface and contract impact

`NOVA-IF-P-R 0.2.0` carries `ObfuscatedDegree` on every Edge snapshot and freezes presence, bounds, expansion-cardinality meaning, zero semantics, freshness, and update behavior. Interface opening declares every profile that may appear and its maximum value. Profile algorithms are versioned separately below the boundary.

## Security and privacy impact

Incorrect treatment as an exact degree would leak or distort topology. Profile algorithms require independent privacy analysis before stabilization.

## Alternatives considered

- Omit the field from 1.0 and add a later extension.
- Expose an exact degree.
- Expose Provider Path count.

## Consequences

- R-Stratum can begin topology-discovery work without depending on P-Stratum internals.
- Consumers must tolerate noise and dummy slots.
- Providers must update the Edge revision when the valid expansion cardinality changes.
- P-0AP must configure and reproduce the hint deterministically.

## Validation and conformance

- every newly added Edge carries a bounded, fresh value;
- R-Stratum uses it only as expansion cardinality;
- profile and freshness changes increment Edge revision;
- P-0AP replay reproduces the same value and updates.

## Migration and rollback

The field is present from `0.2.0` onward, so no consumer migrates from an earlier shape. Removing it later would be a breaking change requiring a new major version.

## Unresolved questions

Profile `1` is a proposed production shape whose algorithm and privacy analysis are unresolved. Only profile `0`, which is deterministic and test-only, is settled.
