# ADR-0001: Strict strata and versioned boundaries

- Status: proposed
- Date: 2026-08-01
- Decision owners: TBD

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

Nova components shall interact across explicit, independently versioned Interface contracts. A higher stratum shall not depend on the private protocol or implementation of a lower stratum.

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
