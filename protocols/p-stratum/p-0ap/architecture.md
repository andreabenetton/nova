
# P-0AP architecture

```text
Simulation controller
        |
NOVA-IF-P-0AP-CONTROL
        |
      P-0AP
       / \
      /   \ NOVA-IF-VIRTUAL-FABRIC
     /     \
NOVA-IF-P-PATH-PROVIDER
     |
P-Stratum common
     |
NOVA-IF-P-R
     |
R-Stratum
```

The control Interface configures Nodes, modeled Paths, characteristics, virtual time, faults, and replay. It is not visible through P-Stratum common.

The Path Provider Interface is the only P-0AP surface consumed by P-Stratum common. R-Stratum remains unaware that P-0AP is involved.

The Virtual Fabric is reusable. Simulated P-LAP Adapters and P-RAP Bindings may use the same engine, but they expose different Interfaces and exercise different protocol code.
