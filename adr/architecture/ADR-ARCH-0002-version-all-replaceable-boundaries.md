---
adr: ADR-ARCH-0002
title: Version all replaceable boundaries
scope: architecture
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents:
  - canon/versioning.md
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-ARCH-0002: Version all replaceable boundaries

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

Inter-stratum, Path Provider, Adapter, Binding, facility, Platform Attachment, and analogous replaceable boundaries shall each have an independent versioned NIDL contract.

## Architectural boundaries

- Owned by: `canon/versioning.md`.
- Consumed through: the contract registry `contracts/registry.yaml` and the versioned directories under `contracts/interfaces/`.
- Must not depend on: any single implementation's release cadence.
- Information allowed to cross the boundary: contract identity, version, kind, and declared roles.
- Information prohibited from crossing the boundary: an implementation's internal version or build identity.

## Interface and contract impact

Every inter-stratum, Path Provider, Adapter, Binding, facility, and Platform Attachment boundary carries an independently versioned contract. Adding a replaceable boundary without a contract is prohibited by this record.

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

none. Boundaries that predate the rule are already versioned.

## Unresolved questions

none.
