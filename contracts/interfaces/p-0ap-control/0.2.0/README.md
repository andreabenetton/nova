# P-0AP Control Interface 0.2.0

This test-only Interface configures deterministic P-0AP Nodes and Provider Paths. P-0AP models Path Provider behavior, while P-Stratum common alone constructs R-Stratum Edges.

The control surface configures:

- authenticated Nova Node identities and identity/address updates;
- finite Provider Path resources and characteristics;
- Obfuscated degree values and profiles;
- virtual time, partitions, recording, and replay;
- conforming or intentionally adversarial provider behavior.

It contains no P-LAP, P-RAP, Adapter, Binding, or public Path-kind selector. Self-Paths are rejected as Provider Paths; a future diagnostic loopback, if implemented, remains entirely inside this control surface and is not announced upward.
