<!-- SPDX-License-Identifier: Apache-2.0 OR CC-BY-4.0 -->

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

Executable simulation behavior does not define Nova semantics. The same Virtual Fabric may support P-0AP, a Simulated P-LAP Adapter, and a Simulated P-RAP Binding through distinct front ends.

Scenario `0.2` assigns each simulated Node a distinct Nova identity and an Obfuscated-degree hint. Provider Paths have characteristics but no P-LAP/P-RAP Path-kind label.
