---
adr: ADR-P-0002
title: Adapters and Bindings are distinct extension points
scope: p-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/p-lap-adapter/0.1.0
  - contracts/interfaces/p-rap-binding/0.1.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0002: Adapters and Bindings are distinct extension points

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

P-LAP uses Adapters for Nexus Fundamenta. P-RAP uses Bindings for integrated routed network and transport combinations. Adapter and Binding are not interchangeable glossary terms.

## Architectural boundaries

- Owned by: P-Stratum, with each extension point owned by its protocol.
- Consumed through: the P-LAP Adapter contract and the P-RAP Binding contract.
- Must not depend on: a shared abstraction that treats a Nexus Fundamentum and a routed underlay as one extension point.
- Information allowed to cross the boundary: the properties each contract declares for its integration.
- Information prohibited from crossing the boundary: an Adapter concept used to describe a Binding, or the reverse.

## Interface and contract impact

`NOVA-IF-P-LAP-ADAPTER` and `NOVA-IF-P-RAP-BINDING` remain separate contracts. The two terms are glossary-distinct and are checked by the terminology rules.

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

none. The two extension points were never unified in an implemented contract.

## Unresolved questions

The record was written as a scaffold entry and states the decision without the evidence required for acceptance. The validation work listed above is outstanding.
