# ADR-0016: Include Obfuscated degree in the base P-R Interface

- Status: proposed
- Date: 2026-08-01
- Decision owners: TBD

## Context

The R-Stratum topology-discovery design needs a privacy-preserving cardinality telling a Node how many neighbor-expansion slots to prepare through a Close. The P-Stratum paper describes an obfuscated degree derived by excluding common Peers and adding positive noise. Omitting it from P-R would leave a required cross-stratum input undefined.

## Decision

Every Edge snapshot in `NOVA-IF-P-R 0.2.0` includes `ObfuscatedDegree`. Its observable meaning is strictly the number of neighbor-expansion slots R-Stratum prepares. It is not an exact Peer degree, Path count, physical topology claim, or verified remote fact.

The value includes a profile identifier, age at snapshot emission, and validity duration. Interface opening declares every profile that may appear and its maximum value. The base Interface freezes presence, bounds, expansion-cardinality meaning, zero semantics, freshness, and update behavior. Noise distribution, common-Peer detection, dummy-slot realization, and profile algorithms remain separately versioned below the boundary.

## Consequences

- R-Stratum can begin topology-discovery work without depending on P-Stratum internals.
- Consumers must tolerate noise and dummy slots.
- Providers must update the Edge revision when the valid expansion cardinality changes.
- P-0AP must configure and reproduce the hint deterministically.

## Alternatives considered

- Omit the field from 1.0 and add a later extension.
- Expose an exact degree.
- Expose Provider Path count.

## Security and privacy impact

Incorrect treatment as an exact degree would leak or distort topology. Profile algorithms require independent privacy analysis before stabilization.

## Validation plan

- every newly added Edge carries a bounded, fresh value;
- R-Stratum uses it only as expansion cardinality;
- profile and freshness changes increment Edge revision;
- P-0AP replay reproduces the same value and updates.
