---
adr: ADR-PR-0003
title: Use an atomic reliable SDU baseline with explicit lifecycle
scope: p-r-interface
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts:
  - contracts/interfaces/p-r/0.2.0
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-PR-0003: Use an atomic reliable SDU baseline with explicit lifecycle

## Context

P-R `0.1.0` left reliability, ordering, ownership, backpressure, cancellation, races, and reset semantics undefined. Allowing the first QUIC or in-memory implementation to define these implicitly would make the contract non-portable.

## Decision

The initial P-R baseline provides complete, authenticated, replay-protected, boundary-preserving, reliable SDU delivery between P-Stratum Peers while an Edge remains usable. Independent SDUs are not ordered.

Submission acceptance transfers ownership of an immutable logical copy. Every accepted Submission has exactly one terminal completion result. Before an Interface reset, unresolved accepted Submissions complete with `INTERFACE_RESET`, and the reset event is terminal for the instance. Queues and event backlogs are finite; `WOULD_BLOCK` rejects without ownership transfer and capacity recovery is event-driven. Service-profile removal and orderly close have explicit terminal behavior. Cancellation is excluded from the baseline.

Interface opening returns an atomic Edge snapshot plus continuation event sequence. Edge revisions and Interface event sequences are monotonic. Reset invalidates all runtime identifiers.

## Architectural boundaries

- Owned by: the P–R Interface.
- Consumed through: `NOVA-IF-P-R` Submission, completion, and Interface event operations.
- Must not depend on: QUIC stream behavior, in-memory queue behavior, or any provider's resource model.
- Information allowed to cross the boundary: Submission acceptance, exactly one terminal completion per accepted Submission, Edge revisions, and a monotonic Interface event sequence.
- Information prohibited from crossing the boundary: an ordering promise derived from a provider's transport, and any runtime identifier that survives a reset.

## Interface and contract impact

`NOVA-IF-P-R 0.2.0` defines the atomic reliable SDU baseline, ownership transfer on acceptance, exactly-one completion, `INTERFACE_RESET` for unresolved Submissions, finite queues with `WOULD_BLOCK` and event-driven capacity recovery, terminal behavior for service-profile removal and orderly close, and monotonic revisions and event sequences. Cancellation is excluded.

## Security and privacy impact

Delivery is authenticated and replay-protected while an Edge remains usable, which the baseline requires of every provider. Finite queues and explicit reset semantics bound the resources an adversary can consume through the Interface. The baseline does not itself establish the cryptographic strength of any underlying carriage.

## Alternatives considered

- Global reliable/unreliable capabilities without per-profile semantics.
- Mandatory ordered delivery.
- Cancellation in the initial baseline.
- Unbounded provider queues.

## Consequences

- P-0AP must model finite resources rather than unlimited in-memory queues.
- QUIC stream use cannot leak an ordering promise upward.
- Optional unreliable profiles can be proposed later without weakening the stable baseline.
- deterministic race scenarios become part of conformance.

## Validation and conformance

Test atomic delivery, ownership, exactly-one completion, both submit/remove linearizations, finite backpressure, capacity notification, profile removal, expiry, orderly close, reset ordering, event-backlog exhaustion, sequence gaps, stale Edge revisions, and no post-removal delivery.

## Migration and rollback

`0.1.0` left these semantics undefined, so no compatible migration exists; consumers move to `0.2.0` directly. Optional unreliable profiles may be added later without weakening the baseline.

## Unresolved questions

Whether cancellation is added as a later capability, and which unreliable profiles are worth defining, remain open.
