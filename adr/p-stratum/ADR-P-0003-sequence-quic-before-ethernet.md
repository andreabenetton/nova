---
adr: ADR-P-0003
title: Sequence QUIC before Ethernet while developing R-Stratum in parallel
scope: p-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0003: Sequence QUIC before Ethernet while developing R-Stratum in parallel

## Context

Ethernet is the correct first real P-LAP Adapter, but it requires discovery, privileges, framing, and link-specific behavior that should not block R-Stratum or P-RAP development. P-RAP over QUIC is user-space, CI-friendly, and already supplies encryption, congestion control, reliable streams, and optional datagrams.

## Decision

After the contract and P-0AP milestone:

- R-Stratum development begins in parallel against `NOVA-IF-P-R`, mocks, and P-0AP;
- P-RAP is first tested against the Simulated Binding and then implemented with IPv6-QUIC and IPv4-QUIC Bindings sharing QUIC-common behavior;
- P-LAP is first tested against the Simulated Adapter and then implemented with Ethernet as its first real Adapter;
- TCP remains a later compatibility Binding.

QUIC is the first real external-underlay integration. Ethernet is the first real Nexus Fundamenta integration, but not the first external implementation milestone.

## Architectural boundaries

- Owned by: the project's implementation sequence rather than any protocol.
- Consumed through: the existing P-LAP Adapter, P-RAP Binding, and Path Provider contracts, which sequencing does not alter.
- Must not depend on: QUIC semantics reaching P-RAP or the P–R Interface.
- Information allowed to cross the boundary: nothing beyond what the affected contracts already declare.
- Information prohibited from crossing the boundary: transport-specific behavior introduced because it was convenient for the first integration.

## Interface and contract impact

No Interface version changes as a result of sequencing. The Binding and Adapter contracts must be complete enough for their simulated and real providers before the corresponding implementation milestone is accepted.

## Security and privacy impact

QUIC reduces the amount of new remote-transport security code in the first integration, but it does not prove P-RAP Association security or binding independence. Ethernet and P-LAP security remain separate work.

## Alternatives considered

- Complete P-LAP Ethernet before beginning P-RAP or R-Stratum.
- Use TCP as the first P-RAP Binding.
- Implement R-Stratum only after both P-LAP and P-RAP are complete.

## Consequences

- A multi-node R-Stratum prototype can run earlier in ordinary CI.
- P-RAP and R-Stratum can produce feedback while P-LAP remains under design.
- P-0AP and simulated integrations provide deterministic reproduction.
- The project must prevent QUIC semantics from leaking into P-RAP or the P-R Interface.

## Validation and conformance

- Demonstrate R-Stratum over P-0AP.
- Demonstrate P-RAP over the Simulated Binding.
- Demonstrate multi-node forwarding over IPv4-QUIC and IPv6-QUIC.
- Demonstrate P-LAP over the Simulated Adapter and then Ethernet.
- Demonstrate a mixed P-LAP/P-RAP topology without R-Stratum source changes.

## Migration and rollback

Sequencing may be revised without a contract change. Reordering the milestones does not invalidate work already completed against a contract.

## Unresolved questions

Whether TCP Bindings are needed at all, beyond compatibility, is deferred until QUIC integration is complete.
