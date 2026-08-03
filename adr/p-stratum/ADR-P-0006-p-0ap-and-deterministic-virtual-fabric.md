<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0006: Add P-0AP and a deterministic Virtual Fabric

- Status: proposed
- Date: 2026-08-01
- Decision owners: TBD

## Context

R-Stratum and P-Stratum common need an executable, deterministic Path Provider instance before real Ethernet and QUIC integrations are complete. A simple self-loop is insufficient because topology, failure, forwarding, and multi-node behavior require distinct Node instances and programmable characteristics.

## Decision

Introduce P-0AP, the P-Stratum Zero-Underlay Association Protocol, as a development and conformance Path Provider protocol. A P-0AP Path Provider implementation implements `NOVA-IF-P-PATH-PROVIDER`; a running Path Provider instance provides the service, exposes the test-only `NOVA-IF-P-0AP-CONTROL`, and may consume a reusable deterministic Virtual Fabric through `NOVA-IF-VIRTUAL-FABRIC`.

The Virtual Fabric shall also support a Simulated P-LAP Adapter and Simulated P-RAP Binding so the real P-LAP and P-RAP protocols can be exercised deterministically at their proper boundaries.

P-0AP shall support paired-node mode as the minimum useful profile. A self-Path is rejected as a Provider Path; any future diagnostic loopback remains private to the control surface and never exposes an R-Stratum Edge. P-0AP creates Provider Paths without a Path-kind selector. P-Stratum common aggregates them into Edges; P-0AP never creates or classifies R-Stratum Edges directly.

## Consequences

- R-Stratum can be implemented and tested before external integrations exist.
- Multi-node forwarding, failure, partition, and replay tests become CI-friendly.
- P-LAP and P-RAP retain independent conformance paths through simulated integrations.
- Additional contracts, schemas, deterministic algorithms, resource limits, and trace governance are required.

## Alternatives considered

- Use only an in-process mock P-Stratum.
- Implement P-RAP/QUIC before any deterministic Path Provider instance.
- Treat the internal virtual Adapter as the simulator.
- Build separate unrelated simulators for P-0AP, P-LAP, and P-RAP.

## Contract and migration impact

Use `NOVA-IF-P-0AP-CONTROL 0.3.0`, `NOVA-IF-P-PATH-PROVIDER 0.4.0`, and `NOVA-IF-VIRTUAL-FABRIC 0.1.0`. P-0AP supplies authenticated identity, finite Path properties, and Obfuscated degree to P-Stratum common. Add implementation declarations for P-0AP, the Virtual Fabric, Simulated Adapter, and Simulated Binding.

## Security impact

P-0AP can test lifecycle, limits, and failure handling but does not establish cryptographic or real-underlay security. Conforming and intentionally violating provider modes must be separated. Scenario and trace loaders require strict resource limits.

## Validation plan

- Validate scenarios and traces against versioned schemas.
- Require deterministic traces for fixed inputs.
- Run Path Provider conformance against P-0AP.
- Run P-LAP Adapter and P-RAP Binding conformance against simulated integrations.
- Run R-Stratum consumer tests without importing P-0AP internals.
