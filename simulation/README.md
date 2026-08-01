
# Simulation

This directory defines the deterministic Virtual Fabric, scenario and trace schemas, reusable characteristic profiles, and reproducible fixtures.

The authority order is:

```text
Normative Interfaces and protocol specifications
                  |
        Conformance scenarios
                  |
       Virtual Fabric and P-0AP
```

Executable simulation behavior does not define Nova semantics. The same Virtual Fabric engine may be used through three distinct front ends:

- P-0AP at the Path Provider boundary;
- a Simulated P-LAP Adapter at the Adapter boundary;
- a Simulated P-RAP Binding at the Binding boundary.
