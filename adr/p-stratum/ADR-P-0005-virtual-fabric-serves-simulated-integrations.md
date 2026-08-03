---
adr: ADR-P-0005
title: Serve the simulated Adapter and Binding from one Virtual Fabric
scope: p-stratum
status: proposed
date: 2026-08-03
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/virtual-fabric/0.1.0
  - contracts/interfaces/p-lap-adapter/0.1.0
  - contracts/interfaces/p-rap-binding/0.1.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0005: Serve the simulated Adapter and Binding from one Virtual Fabric

## Context

The deterministic Virtual Fabric was introduced as the simulation model a P-0AP Path Provider instance may consume, and ADR-P0AP-0001 owns that consumption. P-LAP and P-RAP need the same determinism to be exercised at their own boundaries before Ethernet and QUIC integrations exist, and each could plausibly acquire its own simulator.

Whether one model serves all three is not a P-0AP decision. It constrains the Simulated P-LAP Adapter and the Simulated P-RAP Binding, so an implementer scoped to either protocol has to be able to find it.

## Decision

One reusable deterministic Virtual Fabric serves every simulated integration. It SHALL support a Simulated P-LAP Adapter and a Simulated P-RAP Binding, so the real P-LAP and P-RAP protocols are exercised deterministically at their proper boundaries rather than through a Path Provider instance that stands in for them.

Each simulated integration is consumed through its own contract. The Virtual Fabric supplies determinism; it does not become a shared implementation that the two protocols reach through.

## Architectural boundaries

- Owned by: P-Stratum, because the requirement binds P-LAP and P-RAP as well as P-0AP.
- Consumed through: `NOVA-IF-VIRTUAL-FABRIC` for the model, with each simulated integration consumed through `NOVA-IF-P-LAP-ADAPTER` or `NOVA-IF-P-RAP-BINDING`.
- Must not depend on: P-0AP behavior, and no simulated integration may depend on another.
- Information allowed to cross the boundary: deterministic scheduling, topology, and failure behavior declared by the Virtual Fabric contract.
- Information prohibited from crossing the boundary: P-0AP control state, and any assumption that one simulated integration observes another.

## Interface and contract impact

Uses `NOVA-IF-VIRTUAL-FABRIC 0.1.0`, and adds implementation declarations for the Simulated Adapter and the Simulated Binding against `NOVA-IF-P-LAP-ADAPTER 0.1.0` and `NOVA-IF-P-RAP-BINDING 0.1.0`. No Path Provider contract changes: a simulated integration is exercised at its own boundary, not through `NOVA-IF-P-PATH-PROVIDER`.

## Security and privacy impact

Sharing one simulation model concentrates the resource limits that scenario and trace loading require, so those limits are established once rather than per simulator. The model establishes no cryptographic or real-underlay property for any protocol that consumes it, and a conformance result obtained against it says nothing about a real Adapter or Binding.

## Alternatives considered

- Build separate unrelated simulators for P-0AP, P-LAP, and P-RAP. Rejected: three determinism models diverge, and a defect reproduced in one is not reproducible in the others.
- Treat the internal virtual Adapter as the simulator. Rejected: it exercises P-LAP through an Adapter that P-Stratum common already owns, so the protocol boundary is never actually tested.
- Exercise P-LAP and P-RAP through a P-0AP instance. Rejected: that tests P-0AP, and leaves both real protocols unexercised.

## Consequences

- P-LAP and P-RAP retain independent conformance paths through simulated integrations.
- Deterministic scheduling, topology, and failure semantics are specified once and reused.
- The Virtual Fabric acquires consumers beyond P-0AP, so its contract must not encode P-0AP assumptions.
- A change to the shared model affects three consumers, which raises the bar for revising it.

## Validation and conformance

- Run P-LAP Adapter conformance against the Simulated Adapter.
- Run P-RAP Binding conformance against the Simulated Binding.
- Require deterministic traces for fixed inputs across every simulated integration.
- Show that no simulated integration observes another's state within one scenario.

## Migration and rollback

none. No protocol-specific simulator exists to migrate from.

## Unresolved questions

The Simulated Adapter and Simulated Binding are declared but not conformance-complete. Whether one Virtual Fabric revision can serve three consumers without accumulating protocol-specific options is unproven.
