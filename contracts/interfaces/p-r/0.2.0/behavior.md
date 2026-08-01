# Behavioral contract

## Interface opening

`open-interface` atomically negotiates the exact experimental version and returns:

- a new `InterfaceInstanceId`;
- optional capabilities and typed finite limits;
- every Obfuscated degree profile that may appear during the Interface instance;
- a coherent initial Edge snapshot;
- `next_event_sequence`, the first sequence number after the snapshot.

No Edge event may be lost between the snapshot and the event stream. Mandatory version semantics, including Edge service profiles and Obfuscated degree, are not optional capabilities and are not negotiated away.

## Peer identity and Edge aggregation

P-Stratum common groups all usable Provider Paths authenticating the same `NodeIdentityId` into one Edge.

- first usable Path: `edge-added`;
- additional Path or visible property change: `edge-updated`;
- loss of one of multiple Paths: `edge-updated`;
- loss of the last usable Path: `edge-removed`;
- later reachability: a new `EdgeId` and `edge-added`.

A `PeerHandle` remains associated with the same `NodeIdentityId` for the Interface lifetime and is never assigned to a different identity. A valid address-set rotation updates the existing Edge. A changed identity identifier represents a different Peer.

R-Stratum selects an Edge service profile. P-Stratum chooses the underlying Path or Paths.

## Submission acceptance and completion

`submit-sdu` has one linearization point.

- If acceptance linearizes before removal, the operation returns `SubmissionAccepted`; exactly one terminal `submission-completed` follows.
- If Edge removal linearizes first, the operation fails with `EDGE_UNAVAILABLE` or `UNKNOWN_EDGE`.

A successful completion means that the Peer P-Stratum accepted and reconstructed the complete SDU. It does not mean that the Peer R-Stratum processed the Gram or that a final Receiver was reached.

Before `interface-reset`, every accepted unresolved Submission completes with `INTERFACE_RESET`. The reset event is the final event of the old Interface instance. An orderly `close-interface` waits until every accepted Submission has a terminal result, returns `InterfaceClosed`, and produces no later event for that Interface instance.

## Ownership

After `SubmissionAccepted`, the consumer may release or reuse the original source buffer. P-Stratum owns an immutable logical copy until terminal completion. Zero-copy implementation techniques must preserve this semantic rule.

## Ordering

Each SDU is delivered atomically. Independent SDUs have no inter-SDU ordering guarantee. A consumer that requires ordering must encode it at R-Stratum.

## Scheduling hints

`service_profile_id` selects a required profile. `urgency` defines a relative scheduling class within an Edge service profile. Implementations must prevent indefinite starvation of lower urgency classes.

`priority_prefix_length` is a best-effort hint available only when the capability is advertised and must not exceed the SDU length. `expires_after_micros` is measured from Submission acceptance. If the Peer P-Stratum has not accepted the complete SDU before the deadline, the Submission completes with `EXPIRED`.

## Backpressure

Queues are finite. `WOULD_BLOCK` means that the Submission was not accepted. Backpressure is scoped to an Edge service profile. The provider emits `submission-capacity-available` after capacity may be available again. The notification may be coalesced or become stale because of concurrent consumers, so retry may still return `WOULD_BLOCK`; consumers must not use aggressive polling loops.

If an Edge service profile is removed, it accepts no new Submissions. Existing accepted Submissions either complete normally or terminate with `SERVICE_PROFILE_REMOVED` before the profile disappears from the Edge snapshot.

## Removal and delivery

After `edge-removed` for an Edge incarnation:

- no new Submission is accepted;
- no later `sdu-delivered` references that `EdgeId`;
- every accepted unresolved Submission has already received a terminal result;
- the `EdgeId` is never reused.

## Event stream and reset

Every event contains an `EventContext` with the Interface instance and a monotonically increasing sequence number. A sequence gap cannot be repaired by querying a known Edge because additions and removals may also be missing. The consumer must reopen the Interface and use a new atomic snapshot.

If the consumer does not drain events and the finite event backlog is exhausted, the provider resets the Interface rather than silently dropping events.
