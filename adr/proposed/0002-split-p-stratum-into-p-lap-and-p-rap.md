<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-0002: Split P-Stratum into P-LAP and P-RAP

- Status: proposed
- Date: 2026-08-01
- Decision owners: TBD

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

P-Stratum shall use two distinct peer protocols: P-LAP for link-adjacent Paths and P-RAP for remote Paths over routed underlays. The distinction is protocol-level, not merely an Adapter choice.

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
