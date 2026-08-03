---
adr: ADR-REPO-0002
title: Original papers are non-normative research inputs
scope: repository
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-REPO-0002: Original papers are non-normative research inputs

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

The Nova and P-Stratum papers remain preserved under research/original-papers. New canon, contracts, protocols, and accepted ADRs define conformance.

## Architectural boundaries

- Owned by: `canon/authority.md`, which places research below every normative artifact.
- Consumed through: citation only. Research is read for design lineage, never implemented from.
- Must not depend on: nothing; research is a leaf input.
- Information allowed to cross the boundary: motivation, lineage, and open questions.
- Information prohibited from crossing the boundary: conformance requirements taken directly from a paper.

## Interface and contract impact

none. Papers define no conformance. Where a paper and a contract disagree, the contract governs.

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

Third-party rights in the preserved papers are unreviewed, which is why they carry a restricted license reference rather than a project license.
