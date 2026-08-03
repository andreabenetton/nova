---
adr: ADR-ARCH-0001
title: Strict strata and versioned boundaries
scope: architecture
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-ARCH-0001: Strict strata and versioned boundaries

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

Nova components shall interact across explicit, independently versioned Interface contracts. A higher stratum shall not depend on the private protocol or implementation of a lower stratum.

## Architectural boundaries

- Owned by: `canon/architecture.md` and `canon/authority.md`.
- Consumed through: every versioned NIDL contract under `contracts/interfaces/`.
- Must not depend on: the private protocol or implementation of any stratum.
- Information allowed to cross the boundary: the operations, events, types, errors, capabilities, and limits a contract declares.
- Information prohibited from crossing the boundary: implementation internals, provider provenance, and underlying technology identity.

## Interface and contract impact

This record constrains every boundary rather than one contract version. Each replaceable boundary requires its own versioned NIDL contract, and no existing contract version changes as a direct result.

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

none. The decision establishes the baseline architecture rather than replacing an earlier one.

## Unresolved questions

none.
