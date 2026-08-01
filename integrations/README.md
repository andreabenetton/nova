<!-- SPDX-License-Identifier: Apache-2.0 -->

# Integrations

Technology-specific integrations implement versioned Interfaces. They must not redefine the common protocol.

- P-LAP Adapters bind P-LAP to Nexus Fundamenta.
- P-RAP Bindings bind P-RAP to integrated routed network and transport combinations.
- Simulated Adapter and Binding implementations use the Virtual Fabric to exercise the real P-LAP and P-RAP protocols deterministically.
- P-0AP is not an integration; it is a separate zero-underlay Path Provider under `protocols/p-stratum/p-0ap/`.
