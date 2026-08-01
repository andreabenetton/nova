# P-Stratum common architecture

P-Stratum common:

- consumes Path Provider events from P-LAP and P-RAP;
- maps provider-local Path identifiers to P-Stratum Path identifiers;
- exposes abstract Path properties through `NOVA-IF-P-R`;
- routes submitted R-Stratum SDUs to the selected Path Provider;
- delivers received SDUs to R-Stratum;
- enforces lifecycle and generation rules common to all Paths.

It does not implement P-LAP discovery, P-RAP Association establishment, Ethernet behavior, or QUIC behavior.
