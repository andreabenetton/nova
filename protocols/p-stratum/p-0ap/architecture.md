<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-0AP architecture

```text
Simulation controller
        |
NOVA-IF-P-0AP-CONTROL 0.2.0
        |
      P-0AP ----- NOVA-IF-VIRTUAL-FABRIC 0.1.0
        |
NOVA-IF-P-PATH-PROVIDER 0.3.0
        |
P-Stratum common
        |
NOVA-IF-P-R 0.2.0
        |
R-Stratum
```

Control configures simulated Nodes, identities, Provider Paths, expansion cardinality, finite resources, virtual time, faults, and replay. None of that metadata appears through the Path Provider Interface or P-R.

P-Stratum common, not P-0AP, aggregates Paths and implements the outward P–R Interface representation.
