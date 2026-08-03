---
adr: ADR-P0AP-0001
title: Add P-0AP and a deterministic Virtual Fabric
scope: p-0ap
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/p-0ap-control/0.3.0
  - contracts/interfaces/p-path-provider/0.4.0
  - contracts/interfaces/virtual-fabric/0.1.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P0AP-0001: Add P-0AP and a deterministic Virtual Fabric

## Context

R-Stratum and P-Stratum common need an executable, deterministic Path Provider instance before real Ethernet and QUIC integrations are complete. A simple self-loop is insufficient because topology, failure, forwarding, and multi-node behavior require distinct Node instances and programmable characteristics.

## Decision

Introduce P-0AP, the P-Stratum Zero-Underlay Association Protocol, as a development and conformance Path Provider protocol. A P-0AP Path Provider implementation implements `NOVA-IF-P-PATH-PROVIDER`; a running Path Provider instance provides the service, exposes the test-only `NOVA-IF-P-0AP-CONTROL`, and may consume a reusable deterministic Virtual Fabric through `NOVA-IF-VIRTUAL-FABRIC`.

Whether that Virtual Fabric also serves the simulated P-LAP and P-RAP integrations is not a P-0AP decision; ADR-P-0005 owns it.

P-0AP shall support paired-node mode as the minimum useful profile. A self-Path is rejected as a Provider Path; any future diagnostic loopback remains private to the control surface and never exposes an R-Stratum Edge. P-0AP creates Provider Paths without a Path-kind selector. P-Stratum common aggregates them into Edges; P-0AP never creates or classifies R-Stratum Edges directly.

## Architectural boundaries

- Owned by: P-0AP, with the Virtual Fabric owned separately as a reusable simulation model.
- Consumed through: `NOVA-IF-P-PATH-PROVIDER` for the service, `NOVA-IF-P-0AP-CONTROL` for test-only control, and `NOVA-IF-VIRTUAL-FABRIC` for the simulation model.
- Must not depend on: R-Stratum internals, and never creating or classifying R-Stratum Edges.
- Information allowed to cross the boundary: authenticated identity, finite Path properties, and Obfuscated degree.
- Information prohibited from crossing the boundary: control-surface state, scenario or trace detail, and any diagnostic loopback.

## Interface and contract impact

Uses `NOVA-IF-P-0AP-CONTROL 0.3.0`, `NOVA-IF-P-PATH-PROVIDER 0.4.0`, and `NOVA-IF-VIRTUAL-FABRIC 0.1.0`. Adds implementation declarations for P-0AP and the Virtual Fabric.

## Security and privacy impact

P-0AP can test lifecycle, limits, and failure handling but does not establish cryptographic or real-underlay security. Conforming and intentionally violating provider modes must be separated. Scenario and trace loaders require strict resource limits.

## Alternatives considered

- Use only an in-process mock P-Stratum.
- Implement P-RAP/QUIC before any deterministic Path Provider instance.

## Consequences

- R-Stratum can be implemented and tested before external integrations exist.
- Multi-node forwarding, failure, partition, and replay tests become CI-friendly.
- Additional contracts, schemas, deterministic algorithms, resource limits, and trace governance are required.

## Validation and conformance

- Validate scenarios and traces against versioned schemas.
- Require deterministic traces for fixed inputs.
- Run Path Provider conformance against P-0AP.
- Run R-Stratum consumer tests without importing P-0AP internals.

## Migration and rollback

P-0AP is a development and conformance provider, so removing it would not affect a deployed system. Tests that depend on deterministic reproduction would need an equivalent replacement first.

## Unresolved questions

P-0AP and the Virtual Fabric are not conformance-complete. Resource limits for scenario and trace loaders require review before the deterministic model is relied on outside CI.
