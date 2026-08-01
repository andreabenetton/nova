# P-0AP

P-0AP is the **P-Stratum Zero-Underlay Association Protocol**. It is the first deterministic Path Provider used to make P-Stratum common and R-Stratum executable without an external Nexus Fundamenta or routed underlay.

P-0AP:

- implements `NOVA-IF-P-PATH-PROVIDER 0.3.0`;
- provides test control through `NOVA-IF-P-0AP-CONTROL 0.2.0`;
- consumes `NOVA-IF-VIRTUAL-FABRIC 0.1.0` when using the Virtual Fabric;
- creates authenticated Provider Paths, not Edges;
- has no Path-kind selector;
- provides deterministic Obfuscated-degree hints and finite resource behavior;
- is not an Adapter, Binding, or substitute for P-LAP/P-RAP protocol conformance.

The digit `0` means zero external underlay. It does not mean R-Stratum distance zero.
