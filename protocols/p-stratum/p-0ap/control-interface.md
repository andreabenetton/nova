# P-0AP control Interface

`NOVA-IF-P-0AP-CONTROL 0.2.0` is a test-only Interface used to:

- create distinct simulated Nodes with distinct Nova Node identities;
- update a simulated Node identity to model address rotation or identity replacement;
- create, update, and remove Provider Paths without selecting a Path kind;
- configure complete-SDU behavior, finite queues, latency, jitter, bandwidth, loss, duplication, and reordering;
- configure Obfuscated degree and its profile, causing affected Provider Paths to update;
- partition and restore Nodes;
- advance virtual time and run until idle;
- record and replay traces;
- select conforming or explicitly adversarial provider behavior.

It is never a peer protocol and is invisible to R-Stratum.
