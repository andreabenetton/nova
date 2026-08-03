<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-Stratum to R-Stratum design guide

This guide indexes the current P-R design. It is explanatory; the authoritative sources are `canon/`, the versioned NIDL contracts, and accepted ADRs.

## Boundary model

```text
P-0AP / P-LAP / P-RAP
          |
NOVA-IF-P-PATH-PROVIDER 0.4.0
          |
P-Stratum common
  identity grouping
  Path aggregation and selection
  Edge service profiles
  finite queues and lifecycle
          |
NOVA-IF-P-R 0.2.0
          |
R-Stratum
```

Provider Paths never cross P-R. P-Stratum common exposes at most one active Edge per authenticated `NodeIdentityId`. R-Stratum cannot branch on P-0AP, P-LAP, P-RAP, Adapter, Binding, locator, Ethernet, QUIC, or simulation provenance.

## Identity and lifecycle

- `NodeIdentityId` is the Peer equality key.
- Canonically ordered Node addresses are authenticated as belonging to that identity.
- Valid address rotation updates the existing Peer and Edge.
- Identity replacement creates a different Peer and Edge.
- `PeerHandle` remains stable for one identity during an Interface instance and is never reassigned.
- `EdgeId` identifies one Edge incarnation and is never reused.
- Interface opening returns an atomic Edge snapshot and event continuation sequence.
- Every event has one Interface-scoped sequence number.
- Every accepted Submission has exactly one terminal result.
- Service-profile removal, Edge removal, orderly close, and reset terminally resolve affected Submissions before visible removal or termination.
- Interface reset is the final event after `INTERFACE_RESET` completion events and invalidates all runtime identifiers.

## Service profiles and metrics

R-Stratum selects an Edge service profile; P-Stratum selects the Provider Path or Paths. The `0.2.0` baseline is reliable, atomic, boundary preserving, duplicate suppressing, and unordered between independent SDUs.

Queues and event backlogs are finite. `WOULD_BLOCK` does not transfer ownership. Capacity notification is event-driven and may be coalesced.

Metric units are closed in this version:

- `MICROSECONDS`;
- `BITS_PER_SECOND`.

Metrics carry source, age at snapshot creation, sample window, total validity, and optional confidence. Age-based freshness avoids requiring a shared process clock.

## Obfuscated degree

Obfuscated degree is included in the base P-R contract. It is only the number of neighbor-expansion slots R-Stratum should prepare. It is not an exact degree or Path count.

- zero means no additional expansion slot under the selected profile;
- nonzero values may include positive noise after excluding known common Peers;
- Interface opening declares every usable profile and its maximum;
- stale degree blocks new topology expansion but does not remove the Edge or block SDU transfer;
- profile algorithms, common-Peer detection, noise parameters, and dummy-slot realization remain below P-R.

The experimental profile registry is `canon/registries/obfuscation-profile-identifiers.yaml`.

## P-0AP role

P-0AP is the first deterministic Path Provider protocol. A running P-0AP Path Provider instance creates Provider Paths, not Edges, and uses neither an Adapter nor a Binding. Its control Interface can model identity/address updates, Path changes, degree changes, finite resources, faults, virtual time, and replay.

Self-Paths are rejected as Provider Paths. A future loopback diagnostic may exist only inside the P-0AP control surface and must never create an Edge.

The implementation sequence is:

1. freeze the experimental contracts and conformance scenarios;
2. implement the Virtual Fabric and P-0AP;
3. implement P-Stratum common Edge aggregation;
4. develop R-Stratum in parallel against a mock and P-0AP;
5. validate the same P-R semantics independently through P-RAP/QUIC;
6. correct the experimental contract before freezing `1.0`.

## Authoritative locations

- glossary and global rules: `canon/`;
- P-R contract: `contracts/interfaces/p-r/0.2.0/`;
- Path Provider contract: `contracts/interfaces/p-path-provider/0.4.0/`;
- P-0AP Control contract: `contracts/interfaces/p-0ap-control/0.3.0/`;
- P-Stratum common design: `protocols/p-stratum/common/`;
- P-0AP design: `protocols/p-stratum/p-0ap/`;
- proposed decisions: ADR-PR-0001, ADR-PR-0002, ADR-PR-0003;
- implementation sequence and freeze gates: `ROADMAP.md` and `contracts/interfaces/p-r/0.2.0/stability-gates.md`.
