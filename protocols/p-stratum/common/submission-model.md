<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Submission model

A Submission begins when `submit-sdu` is accepted. P-Stratum owns an immutable logical copy until exactly one terminal completion event.

The first baseline is atomic, reliable, boundary preserving, replay protected, and unordered between independent SDUs. Fragmentation, retransmission, QUIC stream selection, Provider Path changes, and multipath policy are private.

Queues are finite per Edge service profile. `WOULD_BLOCK` means no acceptance and no ownership transfer. Capacity recovery is announced by event and may be coalesced. Expiry prevents peer acceptance after the deadline and completes with `EXPIRED`. Cancellation is intentionally absent from the baseline.

If a service profile disappears, accepted Submissions either complete under its promise or terminate with `SERVICE_PROFILE_REMOVED` before the profile is removed from the visible Edge snapshot. Edge removal terminally resolves every accepted Submission before `edge-removed`. Interface reset emits `INTERFACE_RESET` completions before the final reset event. Orderly close waits for terminal results before returning.
