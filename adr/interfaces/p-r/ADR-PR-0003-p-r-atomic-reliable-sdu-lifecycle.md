---
adr: ADR-PR-0003
title: Use an atomic reliable SDU baseline with explicit lifecycle
scope: p-r-interface
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
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

## Consequences

- P-0AP must model finite resources rather than unlimited in-memory queues.
- QUIC stream use cannot leak an ordering promise upward.
- Optional unreliable profiles can be proposed later without weakening the stable baseline.
- deterministic race scenarios become part of conformance.

## Alternatives considered

- Global reliable/unreliable capabilities without per-profile semantics.
- Mandatory ordered delivery.
- Cancellation in the initial baseline.
- Unbounded provider queues.

## Validation plan

Test atomic delivery, ownership, exactly-one completion, both submit/remove linearizations, finite backpressure, capacity notification, profile removal, expiry, orderly close, reset ordering, event-backlog exhaustion, sequence gaps, stale Edge revisions, and no post-removal delivery.
