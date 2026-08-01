
# Virtual Fabric model

The minimum model contains:

- endpoint identifiers;
- link identifiers and direction;
- effective maximum unit size;
- base latency and jitter distribution;
- bandwidth and serialization delay;
- queue capacity and discipline;
- loss, duplication, and reordering policy;
- availability state;
- scheduled actions;
- virtual clock and event queue;
- deterministic random source;
- trace sink.

Each model element has explicit finite limits. Unsupported combinations fail scenario validation or activation rather than degrading silently.
