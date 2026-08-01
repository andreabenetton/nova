
# P-0AP security and non-goals

P-0AP is useful for deterministic validation of:

- Interface lifecycle;
- backpressure and limits;
- failure ordering;
- Path generation handling;
- R-Stratum behavior under loss, delay, reordering, and partition;
- defensive behavior against an explicitly faulty Path Provider.

P-0AP does not provide evidence for:

- real cryptographic confidentiality or integrity;
- resistance to a local or multi-link observer;
- real packet-timing behavior;
- Ethernet, IP, UDP, TCP, QUIC, or operating-system correctness;
- P-LAP or P-RAP wire interoperability;
- traffic-analysis resistance.

Scenario and trace loaders must enforce resource limits and reject malformed or unsupported inputs deterministically.
