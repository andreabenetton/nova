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

## Architectural boundaries

- Owned by: the NIDL tooling under `tools/nova-contract`.
- Consumed through: the JSON Schemas under `contracts/schemas` and the canonical JSON under `contracts/canonical`.
- Must not depend on: any authoring convenience that cannot be expressed in the restricted YAML subset.
- Information allowed to cross the boundary: the validated semantic model.
- Information prohibited from crossing the boundary: YAML formatting, comments, and key order, none of which carry meaning.

## Interface and contract impact

Every contract is authored in restricted YAML, validated against JSON Schema, and normalized to deterministic JSON. Fingerprints and generated artifacts derive from the normalized form.

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

none. No contract was authored in another representation.

## Unresolved questions

The record was written as a scaffold entry and states the decision without the evidence required for acceptance. The validation work listed above is outstanding.
