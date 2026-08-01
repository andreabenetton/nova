<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-RAP unit-format stub

The P-RAP unit format must remain independent of one Binding. A possible protected structure contains:

- P-RAP version;
- Association identifier;
- key epoch;
- packet number;
- encrypted message type;
- message identifier;
- fragment or stream semantics;
- acknowledgements only when P-RAP supplies them;
- payload;
- authentication tag when P-RAP protection is active.

The first QUIC profile may rely on QUIC confidentiality while binding Nova identity to the channel. The long-term portability requirement must be documented before freezing the format.
