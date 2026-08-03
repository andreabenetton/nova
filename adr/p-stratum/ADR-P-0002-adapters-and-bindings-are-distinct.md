---
adr: ADR-P-0002
title: Adapters and Bindings are distinct extension points
scope: p-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0002: Adapters and Bindings are distinct extension points

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

P-LAP uses Adapters for Nexus Fundamenta. P-RAP uses Bindings for integrated routed network and transport combinations. Adapter and Binding are not interchangeable glossary terms.

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
