---
adr: ADR-PRAP-0001
title: QUIC carriage profile
scope: p-rap
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/p-rap-binding/0.1.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-PRAP-0001: QUIC carriage profile

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

P-RAP over QUIC should use a reliable bidirectional control stream and QUIC DATAGRAM for message-oriented data when available. Reliable data may use streams. Exact mapping remains subject to protocol specification and conformance tests.

## Architectural boundaries

- Owned by: P-RAP, for the mapping of its messages onto a QUIC Binding.
- Consumed through: `NOVA-IF-P-RAP-BINDING`.
- Must not depend on: QUIC behavior becoming visible in P-RAP Association semantics or at the P–R Interface.
- Information allowed to cross the boundary: the carriage properties the Binding contract declares.
- Information prohibited from crossing the boundary: stream identity, connection identity, and any ordering guarantee implied by QUIC streams.

## Interface and contract impact

The mapping is expressed by the QUIC Bindings under `NOVA-IF-P-RAP-BINDING`. Exact message-to-stream and message-to-datagram mapping remains subject to the P-RAP specification and its conformance tests.

## Wire compatibility impact

A reliable bidirectional control stream and QUIC DATAGRAM for message-oriented data are the intended carriage. Reliable data may use streams. The choice is Binding-local and must not become an assumption of the P-RAP wire format.

## Security and privacy impact

The decision reduces accidental cross-layer coupling but does not itself prove protocol security.

## Alternatives considered

- Informal prose-only boundaries.
- One monolithic P-Stratum protocol.
- Implementation-specific interfaces without shared conformance.

## Consequences

- Contracts and tests become first-class design artifacts.
- Implementation modules receive narrower context.
- Additional schema and CI tooling is required.

## Validation and conformance

Require schema validation, dependency checks, generated mocks, and conformance scenarios before acceptance.

## Migration and rollback

none. No QUIC Binding has been implemented against an earlier carriage profile.

## Unresolved questions

The exact mapping is not settled, and DATAGRAM availability is not guaranteed by every QUIC implementation. Fallback behavior when DATAGRAM is unavailable is undefined.
