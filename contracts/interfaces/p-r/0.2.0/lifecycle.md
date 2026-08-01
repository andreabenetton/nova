# Lifecycle and concurrency

## Interface states

```text
CLOSED -> OPEN -> RESET
   ^        |
   +--------+
```

`close-interface` performs an orderly close after accepted Submissions reach terminal results. `interface-reset` is provider-initiated and terminal for the current Interface instance.

## Edge states

```text
ACTIVE -> DRAINING -> REMOVED
```

An Edge is announced only after Peer authentication and availability of at least one service profile. `DRAINING` is an internal P-Stratum state: no new Submission is accepted for the disappearing Edge or service profile, while already accepted Submissions finish or fail before visible removal.

## Event order

Every provider event carries an `EventContext` containing the current `InterfaceInstanceId` and a monotonically increasing `EventSequence`. The sequence is total for the Interface instance. Gaps require reopening the Interface and consuming a fresh snapshot.

Each Edge update carries an increasing `EdgeRevision`. A revision is compared only within one Edge incarnation. Service profile identifiers are stable within an Edge incarnation and are not reused after removal.

## Linearization rules

- `edge-added` linearizes before any accepted Submission or delivered SDU on that Edge.
- removal of a service profile linearizes after terminal results for Submissions that cannot survive it.
- `edge-removed` linearizes after the terminal result for every unresolved Submission on the Edge and before any later operation can refer successfully to it.
- `interface-reset` linearizes after `INTERFACE_RESET` completion events for all unresolved accepted Submissions and is the final event of the old Interface instance.
- each accepted Submission has exactly one terminal completion event.
