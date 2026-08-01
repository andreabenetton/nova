# ADR-0011: P-RAP Association is independent from Binding instance

- Status: proposed
- Date: 2026-08-01
- Decision owners: TBD

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

A P-RAP Association is identified by Nova identities and Association state, not by an IP five-tuple, socket, QUIC connection, or current Binding instance.

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
