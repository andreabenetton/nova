---
adr: ADR-O-0001
title: IP-over-Nova is an O-Stratum Compatibility Service
scope: o-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/ip-platform-attachment/0.1.0
  - contracts/interfaces/ip-gateway-egress/0.1.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-O-0001: IP-over-Nova is an O-Stratum Compatibility Service

## Context

The Nova design requires independently implementable components and bounded context for human and LLM contributors.

## Decision

IP-over-Nova shall operate above O-Stratum. Operating-system integration shall use Platform Attachments such as Windows NDIS and Linux TUN. These are not P-LAP Adapters or P-RAP Bindings.

## Architectural boundaries

- Owned by: O-Stratum.
- Consumed through: the O–Application Interface, with operating-system integration provided by Platform Attachments.
- Must not depend on: P-LAP Adapters or P-RAP Bindings.
- Information allowed to cross the boundary: IP datagrams carried as application payload.
- Information prohibited from crossing the boundary: any assumption that a Platform Attachment is a Path Provider integration point.

## Interface and contract impact

IP-over-Nova consumes the O-Stratum service and the IP Platform Attachment and gateway-egress contracts. It introduces no P-Stratum contract.

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

none. No earlier placement of IP-over-Nova was implemented.

## Unresolved questions

The record was written as a scaffold entry and states the decision without the evidence required for acceptance. The validation work listed above is outstanding.
