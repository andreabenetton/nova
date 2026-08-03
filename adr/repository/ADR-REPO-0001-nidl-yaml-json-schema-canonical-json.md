---
adr: ADR-REPO-0001
title: NIDL representation
scope: repository
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-REPO-0001: NIDL representation

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

Humans and LLMs author restricted YAML. JSON Schema validates structure. Tooling normalizes the semantic model to deterministic JSON for fingerprints and generated artifacts.

## Consequences

- Contracts and tests become first-class design artifacts.
- Implementation modules receive narrower context.
- Additional schema and CI tooling is required.

## Alternatives considered

- Informal prose-only boundaries.
- One monolithic P-Stratum protocol.
- Implementation-specific interfaces without shared conformance.

## Contract and migration impact

To be specified before acceptance.

## Security impact

The decision reduces accidental cross-layer coupling but does not itself prove protocol security.

## Validation plan

Require schema validation, dependency checks, generated mocks, and conformance scenarios before acceptance.
