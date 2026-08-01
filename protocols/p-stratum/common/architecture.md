# P-Stratum common architecture

P-Stratum common:

- consumes Path Provider events from P-0AP, P-LAP, and P-RAP;
- maps provider-local Path identifiers to P-Stratum Path identifiers;
- exposes abstract Path properties through `NOVA-IF-P-R`;
- routes submitted R-Stratum SDUs to the selected Path Provider;
- delivers received SDUs to R-Stratum;
- enforces lifecycle and generation rules common to all Paths.

It does not implement P-0AP simulation control, P-LAP discovery, P-RAP Association establishment, Ethernet behavior, QUIC behavior, or Virtual Fabric scheduling.

P-Stratum common must not expose the identity of the Path Provider through `NOVA-IF-P-R`. P-0AP Paths must use the same abstract Path model and lifecycle as Paths supplied by P-LAP or P-RAP.
