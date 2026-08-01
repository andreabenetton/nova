
# P-0AP semantics

## Path-level emulation

P-0AP models behavior observable at the Path Provider and P-R Interfaces:

- Peer and Path availability;
- Path addition, update, and removal;
- SDU submission and delivery;
- maximum SDU size;
- delivery class;
- latency, jitter, rate, availability, queueing, and backpressure;
- loss, duplication, reordering, interruption, partition, recovery, and restart.

P-0AP does not claim to emulate or validate:

- Ethernet framing or discovery;
- P-LAP association or cryptographic protection;
- QUIC connections, congestion control, or migration;
- IPv4 or IPv6 locator handling;
- P-RAP Association establishment;
- operating-system timing or packet scheduling.

Profiles named `adjacent-lan-like` or `remote-wan-like` are characteristic presets, not claims that P-LAP, Ethernet, P-RAP, or QUIC have been tested.

## Path kind

Every exposed P-0AP Path is configured to model either `LINK_ADJACENT` or `REMOTE_ASSOCIATION`. P-0AP-specific metadata remains below P-Stratum common.

## Self-loop

A self-loop may return an SDU to the same P-Stratum instance for smoke testing. Unless an explicitly adversarial scenario says otherwise, it must not emit a Path that P-Stratum common would expose as an R-Stratum Edge.
