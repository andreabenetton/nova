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

## Current P-Stratum development baselines

- `NOVA-IF-P-R 0.2.0`: aggregated Edges, stable Peer identity handles, service profiles, declared Obfuscated-degree profiles, typed metrics, finite Submission/event queues, and explicit close/reset SDU lifecycle.
- `NOVA-IF-P-PATH-PROVIDER 0.4.0`: authenticated private Provider Paths, declared degree profiles, scheduling/expiry options, finite event behavior, and reset ordering consumed by P-Stratum common.
- `NOVA-IF-P-0AP-CONTROL 0.3.0`: deterministic P-0AP identity, Path, degree, time, fault, and replay control without a Path-kind selector.

Earlier `0.x` directories are preserved as immutable experimental history and are not compatible by implication.
