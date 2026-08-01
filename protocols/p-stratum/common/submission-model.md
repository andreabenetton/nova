<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-Stratum transfer model

A transfer begins when the P–R Interface accepts one submitted SDU. P-Stratum owns an immutable logical copy until exactly one terminal result.

The first baseline is atomic, reliable, boundary preserving, replay protected, and unordered between independent SDUs. Fragmentation, retransmission, Binding-specific carriage, Provider Path changes, and multipath policy remain private.

Queues are finite. A refusal caused by capacity means no acceptance and no ownership transfer. Capacity recovery is announced according to the P–R Interface. Expiry prevents peer acceptance after the deadline. Cancellation is intentionally absent from the baseline.

Detailed operation names, event ordering, and upper-stratum semantics are defined only in `contracts/interfaces/p-r/`.
