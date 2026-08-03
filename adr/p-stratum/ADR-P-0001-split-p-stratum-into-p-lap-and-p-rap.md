---
adr: ADR-P-0001
title: Split P-Stratum into P-LAP and P-RAP
scope: p-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0001: Split P-Stratum into P-LAP and P-RAP

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

P-Stratum shall use two distinct peer protocols: P-LAP for link-adjacent Paths and P-RAP for remote Paths over routed underlays. The distinction is protocol-level, not merely an Adapter choice.

## Architectural boundaries

- Owned by: P-Stratum.
- Consumed through: `NOVA-IF-P-PATH-PROVIDER`, which both protocols implement.
- Must not depend on: R-Stratum behavior, or on either protocol knowing the other's internals.
- Information allowed to cross the boundary: Provider Paths and their declared properties.
- Information prohibited from crossing the boundary: the identity of the protocol that produced a Provider Path.

## Interface and contract impact

Both protocols implement the Path Provider Interface. P-LAP carries an Adapter contract and P-RAP a Binding contract; neither may be expressed as a variation of the other.

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

none. No single-protocol P-Stratum was implemented.

## Unresolved questions

The record was written as a scaffold entry and states the decision without the evidence required for acceptance. The validation work listed above is outstanding.
