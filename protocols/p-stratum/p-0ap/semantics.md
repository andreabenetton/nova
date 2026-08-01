<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-0AP semantics

P-0AP models behavior observable at the Path Provider boundary:

- authenticated Peer identity and valid address rotation;
- Provider Path addition, update, removal, generation, and reset;
- complete SDU submission and delivery;
- finite queueing and backpressure;
- latency, jitter, bandwidth, loss, duplication, reordering, partition, recovery, and restart;
- Obfuscated-degree value, profile, freshness, and update propagation.

It does not emulate or validate Ethernet framing, P-LAP discovery and cryptography, IP locator behavior, QUIC, P-RAP Association establishment, or operating-system scheduling. Preset names such as `adjacent-lan-like` and `remote-wan-like` are characteristic profiles only.

A self-Path is not a valid Path Provider artifact because it would create an invalid R-Stratum self-Edge. A future diagnostic loopback may exercise local serialization and queue behavior only if it remains private to the P-0AP control surface.
