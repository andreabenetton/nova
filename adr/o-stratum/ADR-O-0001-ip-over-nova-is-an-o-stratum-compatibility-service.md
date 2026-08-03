---
adr: ADR-O-0001
title: IP-over-Nova is an O-Stratum Compatibility Service
scope: o-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-O-0001: IP-over-Nova is an O-Stratum Compatibility Service

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

IP-over-Nova shall operate above O-Stratum. Operating-system integration shall use Platform Attachments such as Windows NDIS and Linux TUN. These are not P-LAP Adapters or P-RAP Bindings.

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
