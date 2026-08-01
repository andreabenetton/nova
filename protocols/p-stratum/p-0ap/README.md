
# P-0AP

P-0AP is the **P-Stratum Zero-Underlay Association Protocol**. It is the deterministic local and simulation Path Provider used to make the P-Stratum boundary executable before external Nexus Fundamenta or routed underlays are available.

P-0AP:

- implements `NOVA-IF-P-PATH-PROVIDER`;
- provides a test-only control surface through `NOVA-IF-P-0AP-CONTROL`;
- consumes `NOVA-IF-VIRTUAL-FABRIC` when operating over the reusable Virtual Fabric;
- exposes existing Path kinds rather than a P-0AP-specific kind;
- is not an Adapter, Binding, or substitute for P-LAP/P-RAP protocol conformance.

The digit `0` means zero external underlay. Two distinct Nodes joined by P-0AP remain one P-Stratum hop apart and become Closes when the modeled Path is exposed to R-Stratum.
