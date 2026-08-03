---
adr: ADR-REPO-0003
title: LLM context manifests and knowledge firewalls
scope: repository
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents:
  - canon/dependency-policy.yaml
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-REPO-0003: LLM context manifests and knowledge firewalls

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

Every implementation unit shall declare required, optional, and forbidden context. CI shall validate manifests and code dependency rules.

## Architectural boundaries

- Owned by: each implementation unit, through its own `CONTEXT.yaml`.
- Consumed through: `nova-contract context`, which validates every manifest, and the dependency policy in `canon/dependency-policy.yaml`.
- Must not depend on: a contributor or agent reading beyond its declared context.
- Information allowed to cross the boundary: the required and optional context a manifest declares.
- Information prohibited from crossing the boundary: anything a manifest declares forbidden, including a peer stratum's private model.

## Interface and contract impact

No Interface changes. Manifests reference the contracts a unit is permitted to consume, so a boundary violation becomes a manifest violation.

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

none. Manifests were introduced with the scaffold.

## Unresolved questions

Manifests bound the context a contributor is told to load. They cannot bound what a model already knows, so they reduce rather than eliminate cross-boundary leakage.
