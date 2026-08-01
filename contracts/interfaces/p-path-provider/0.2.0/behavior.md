
# Behavior notes

P-0AP, P-LAP, and P-RAP provide the same lifecycle surface to P-Stratum common.

Required behavior before stabilization:

- activation and deactivation ordering;
- Path generation and identifier reuse;
- SDU acceptance, backpressure, cancellation, and drain behavior;
- event ordering during failure and removal;
- concurrency and queue limits;
- unknown and stale provider Path handling;
- Path characteristic update semantics.

P-0AP control operations, Virtual Fabric endpoint identifiers, Adapter details, Binding details, and peer-protocol state are outside this Interface.
