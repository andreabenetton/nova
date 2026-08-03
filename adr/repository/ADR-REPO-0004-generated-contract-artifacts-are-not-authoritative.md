---
adr: ADR-REPO-0004
title: Generated artifacts are not authoritative
scope: repository
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-REPO-0004: Generated artifacts are not authoritative

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

NIDL source and its validated semantic model are authoritative. Generated Rust code, canonical JSON, mocks, and documentation are derived and must be reproducible in CI.

## Architectural boundaries

- Owned by: the NIDL source under `contracts/` and its validated semantic model.
- Consumed through: generated artifacts under `generated/`, which are derived and reproducible.
- Must not depend on: a hand edit to any generated file.
- Information allowed to cross the boundary: anything derivable from the source model by a tool.
- Information prohibited from crossing the boundary: a change introduced in a generated artifact and not present in its source.

## Interface and contract impact

Generated Rust code, canonical JSON, mocks, and documentation carry no authority. A contract question is answered from NIDL source and its semantic model.

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

none.

## Unresolved questions

none.
