<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-0AP

P-0AP is the **P-Stratum Zero-Underlay Association Protocol**. It is the first deterministic Path Provider protocol used to make P-Stratum common and its upper Interface executable without an external Nexus Fundamenta or routed underlay.

P-0AP:

- implements `NOVA-IF-P-PATH-PROVIDER 0.4.0`;
- provides test control through `NOVA-IF-P-0AP-CONTROL 0.3.0`;
- consumes `NOVA-IF-VIRTUAL-FABRIC 0.1.0` when using the Virtual Fabric;
- defines how a P-0AP Path Provider instance creates authenticated Provider Paths;
- has no Path-kind selector;
- provides deterministic expansion-cardinality hints and finite resource behavior;
- is not an Adapter, Binding, or substitute for P-LAP/P-RAP protocol conformance.

The digit `0` means zero external underlay. It does not denote any graph distance.
