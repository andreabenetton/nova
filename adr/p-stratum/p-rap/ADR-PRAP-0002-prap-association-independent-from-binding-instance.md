---
adr: ADR-PRAP-0002
title: P-RAP Association is independent from Binding instance
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

# ADR-PRAP-0002: P-RAP Association is independent from Binding instance

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

A P-RAP Association is identified by Nova identities and Association state, not by an IP five-tuple, socket, QUIC connection, or current Binding instance.

## Architectural boundaries

- Owned by: P-RAP.
- Consumed through: `NOVA-IF-P-RAP-BINDING`, which carries an Association without defining its identity.
- Must not depend on: an IP five-tuple, socket, QUIC connection, or current Binding instance.
- Information allowed to cross the boundary: Nova identities and Association state.
- Information prohibited from crossing the boundary: transport-level identity of any kind.

## Interface and contract impact

The Binding contract carries Association traffic without owning Association identity. A Binding instance may be replaced while an Association continues.

## Security and privacy impact

Decoupling Association identity from transport identity means authentication cannot rely on the address or connection a peer arrives on, which is a property the P-RAP specification must establish explicitly rather than inherit.

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

none. No Association model bound to transport identity was implemented.

## Unresolved questions

The record was written as a scaffold entry and states the decision without the evidence required for acceptance. The validation work listed above is outstanding.
