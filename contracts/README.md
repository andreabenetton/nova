# Contracts

Nova Interface Definition Language (NIDL) describes every replaceable architectural boundary. Source contracts are restricted YAML validated by JSON Schema and Nova-specific semantic rules. Canonical JSON, generated code, mocks, and reference documentation are derived artifacts.

## Contract classes

- stratum-interface
- provider-interface
- adapter-interface
- binding-interface
- facility-interface
- platform-attachment-interface
- gateway-egress-interface

Provider Interfaces also describe test-only replaceable boundaries such as P-0AP control and the Virtual Fabric. The Interface name and roles define the domain; NIDL `kind` remains structural rather than a complete taxonomy.

A contract describes provider and consumer roles, operations, events, types, errors, capabilities, limits, lifecycle, invariants, and conformance scenarios. It does not define peer-protocol wire formats or simulation scenario encodings.
