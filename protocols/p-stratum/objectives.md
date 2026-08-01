---
document_id: NOVA-P-OBJECTIVES
status: draft
normative: true
terminology:
  primary_glossary: NOVA-GLOSSARY-P
  additional_glossaries:
    - NOVA-GLOSSARY-COMMON
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-Stratum objectives

P-Stratum provides a uniform, protected, message-preserving communication service between authenticated Peers while hiding differences among local adjacency, remote association, deterministic simulation, and the technologies used below its protocol boundaries.

## Functional objectives

1. **Establish communication with authenticated Peers.**
   - P-0AP defines deterministic zero-underlay association behavior.
   - P-LAP defines link-adjacency discovery and association behavior.
   - P-RAP defines remote-association behavior over a routed underlay.
   - Running Path Provider instances conforming to those protocols create and maintain Paths.

2. **Separate identity from mutable reachability information.**
   - A Peer is identified by authenticated Node identity.
   - Adapter locators, Binding locators, sockets, ports, and Binding instances are not Peer identity.
   - Locator or lower-component replacement does not by itself create a different Peer.

3. **Maintain one or more Paths to a Peer.**
   - Create, update, and remove Paths.
   - Permit concurrent Provider Paths to the same authenticated Peer.
   - Keep provider protocol, Adapter, Binding, locator, and simulation details private to P-Stratum.

4. **Aggregate Provider Paths.**
   - Consume Provider Paths only through the Path Provider Interface.
   - Group usable Provider Paths by authenticated Peer identity.
   - Apply Path selection, failover, and multipath policy inside P-Stratum common.
   - Present provider-independent service behavior through the upper Interface.

5. **Provide protected Peer-to-Peer transfer.**
   - Authenticate the Peer before a Path becomes usable.
   - Preserve confidentiality, integrity, and replay protection.
   - Preserve complete submitted-unit boundaries.
   - Never deliver unauthenticated or partially reconstructed submitted units.

6. **Manage fragmentation and reassembly.**
   - Accept complete submitted units from the upper Interface.
   - Fragment according to effective Path constraints.
   - Reassemble before delivery.
   - Keep lower MTU and fragmentation mechanics private.

7. **Define explicit transfer lifecycle semantics.**
   - Accept or reject a transfer deterministically.
   - Define ownership of accepted data.
   - Produce exactly one terminal result for every accepted transfer.
   - Define expiry, provider failure, Path removal, orderly shutdown, and reset behavior.

8. **Enforce finite resource use and observable backpressure.**
   - Use bounded queues and bounded event backlogs.
   - Reject or defer work when capacity is unavailable.
   - Signal capacity recovery without requiring aggressive polling.
   - Reserve capacity for terminal lifecycle notification.

9. **Expose provider-independent characteristics.**
   - Maximum submitted-unit size.
   - Reliability, atomicity, boundary preservation, and ordering properties.
   - Capacity, latency, and jitter estimates with units, source, age, validity, and optional confidence.
   - Characteristics describe the service P-Stratum can provide, not the technology used to provide it.

10. **Supply privacy-preserving expansion-cardinality contributions.**
    - Obtain profile-qualified values from Path Provider instances.
    - Reconcile values for multiple Provider Paths to the same Peer.
    - Avoid exposing exact Path counts, provider provenance, or lower topology.
    - Keep cross-stratum interpretation in the P–R Interface specification.

11. **Normalize heterogeneous lower services.**
    - P-LAP uses Adapters for Nexus Fundamenta technologies.
    - P-RAP uses Bindings for integrated routed network and transport combinations.
    - P-0AP uses no Adapter or Binding and may use the Virtual Fabric for deterministic execution.
    - P-Stratum common remains independent of every concrete Adapter, Binding, and simulation implementation.

12. **Support deterministic and adversarial testing.**
    - P-0AP supports controlled local and simulated associations.
    - Simulated Adapters exercise P-LAP through the Adapter Interface.
    - Simulated Bindings exercise P-RAP through the Binding Interface.
    - Contract-conforming simulation and deliberately violating adversarial simulation remain explicitly distinct.

13. **Remain implementable in user space.**
    - P-Stratum common and all Path Provider protocol state machines must be implementable without kernel-mode execution.
    - Concrete Adapters and Bindings should run in user space.
    - Any required privileged shim remains minimal and outside P-Stratum protocol semantics.

14. **Preserve strict architectural boundaries.**
    - P-Stratum common depends on the Path Provider Interface, not on a specific Path Provider protocol.
    - P-LAP depends on the Adapter Interface, not on a concrete Adapter.
    - P-RAP depends on the Binding Interface, not on a concrete Binding.
    - The upper consumer depends only on the versioned upper Interface.

## Non-objectives

P-Stratum does not define application semantics, end-to-end transport semantics, global topology discovery, global routing policy, economic settlement, or technology-specific behavior that belongs to an Adapter or Binding.

Terms owned by another stratum are intentionally absent from this document. Their relationship to P-Stratum concepts is defined only in the corresponding Interface glossary and specification.
