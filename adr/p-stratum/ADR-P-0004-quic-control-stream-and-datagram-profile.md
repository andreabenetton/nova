<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0004: QUIC carriage profile

- Status: proposed
- Date: 2026-08-01
- Decision owners: TBD

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

P-RAP over QUIC should use a reliable bidirectional control stream and QUIC DATAGRAM for message-oriented data when available. Reliable data may use streams. Exact mapping remains subject to protocol specification and conformance tests.

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
