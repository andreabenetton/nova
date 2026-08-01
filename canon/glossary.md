---
document_id: NOVA-CANON-GLOSSARY
status: draft
normative: true
---

# Nova glossary

## Stack and data terms

**Nexus Fundamenta**
The heterogeneous technologies commonly associated with the ISO-OSI Data Link Layer and exposed through device drivers or equivalent lower-layer facilities.

**Proximitate Stratum (P-Stratum)**
The lower Nova stratum. It establishes protected Paths to Peers, aggregates those Paths into Edges, and presents Edges to R-Stratum.

**Remotis Stratum (R-Stratum)**
The middle Nova stratum. It establishes communication across Routes, performs routing functions, and coordinates routing-related Facilities.

**Onerarii Stratum (O-Stratum)**
The upper Nova stratum. It provides application-facing transport services.

**Stratum Data Unit (SDU)**
Information transmitted as one logical unit between peer entities at a stratum boundary.

**Process Logical Unit (PLU)**
Information yielded by a process inside a stratum before aggregation into or splitting across SDUs.

**Submitted**
Data passed from an overlying stratum to the current stratum.

**Sent**
Data passed from the current stratum to an underlying stratum or integration.

**Received**
Data obtained by the current stratum from an underlying stratum or integration.

**Delivered**
Data returned by the current stratum to the overlying stratum after processing.

## Node, identity, and topology terms

**Node**
A Nova distribution point capable of acting as an Endpoint, Router node, or provider of a Facility.

**Node identity**
The cryptographically authenticated identity of a Nova Node. It contains a stable identity identifier under an identity profile and one or more canonically ordered Node addresses proven to belong to that identity.

**Node identity identifier**
A profile-qualified cryptographic digest used by P-Stratum to decide whether independently established Paths reach the same Peer. Identity-profile rules define key binding, continuity, rotation, and canonicalization.

**Node address**
An address derived from a Node's long-term public key under one cryptographic suite. It is distinct from any underlay locator. Multiple addresses are merged only when their binding to one Node identity identifier has been cryptographically established.

**Peer handle**
A local, opaque identifier assigned by one P-R Interface instance to a `Node identity identifier`. It remains stable for that identity during the Interface instance, is never assigned to a different identity, and has no wire meaning.

**Endpoint**
A Node that originates or receives traffic intended for itself.

**Sender**
The Endpoint originating a transmission.

**Receiver**
The Endpoint receiving a transmission.

**Router node**
A Node forwarding data not intended for itself.

**Peer**
An authenticated Nova Node reachable through one or more established P-Stratum Paths.

**Path**
An internal P-Stratum association between the local Node and one Peer through which P-Stratum SDUs can be exchanged. A Path is supplied by P-0AP, P-LAP, or P-RAP and is not directly visible to R-Stratum.

**Edge**
The R-Stratum-visible relationship between the local Node and one authenticated Peer. One Edge is backed by one or more usable P-Stratum Paths. P-Stratum common owns Path aggregation and selection.

**Edge incarnation**
The lifetime of one Edge identifier within one P-R Interface instance, beginning with `edge-added` and ending with `edge-removed` or `interface-reset`.

**Edge service profile**
A P-Stratum promise describing one selectable set of SDU-delivery properties and limits available over an Edge. R-Stratum selects a profile; P-Stratum selects the underlying Path or Paths.

**Obfuscated degree**
A profile-bounded privacy-preserving expansion cardinality supplied by P-Stratum for a Peer. It is the number of R-Stratum neighbor-expansion slots to prepare, not the exact degree. Zero means no additional expansion slot is required under the profile; nonzero values may include positive noise after excluding known common Peers.

**Route**
An unweighted sequence of Nodes connecting a Sender and Receiver, as used by R-Stratum topology discovery.

**Trail**
A directed and weighted sequence of Nodes and Links on which a Flow can be established.

**Flow**
A Trail effectively established for data transmission.

**Close**
A Node at R-Stratum distance one. R-Stratum derives a Close from an Edge; a Path is not itself a Close.

## P-Stratum protocol and integration terms

**P-Stratum common service**
The implementation-independent service presented to R-Stratum. It consumes Provider Paths, groups them by authenticated Peer identity, constructs Edge service profiles, applies multipath policy, and exposes Edges through the P-R Interface.

**P-Stratum Zero-Underlay Association Protocol (P-0AP)**
A deterministic P-Stratum Path Provider used to establish local or simulated Peer associations without an external Nexus Fundamenta Adapter or routed-underlay Binding. The digit `0` denotes zero external underlay; it does not denote R-Stratum distance zero.

**P-Stratum Link Adjacency Protocol (P-LAP)**
The P-Stratum peer protocol used to discover and establish Paths with Nodes adjacent through a Nexus Fundamenta.

**Adapter**
A P-LAP component that binds P-LAP to one Nexus Fundamenta technology or instance.

**Internal virtual Adapter**
A P-LAP Adapter representing an internal Nexus Fundamenta-like attachment inside one device. It is distinct from P-0AP.

**P-Stratum Remote Association Protocol (P-RAP)**
The P-Stratum peer protocol used to establish Paths with remote Nodes through an already routed underlay.

**Binding**
A P-RAP component that binds P-RAP to a specific integrated routed network and transport combination, such as IPv4-QUIC or IPv6-QUIC.

**Binding instance**
An active realization of a Binding between local and remote locators.

**Remote locator**
Binding-specific information required to reach a remote Node. It is not a Nova Node address and may change without changing Node identity.

**P-RAP Association**
An authenticated P-RAP relationship between Nova Nodes. It may survive replacement of its Binding instance.

**Path Provider**
A component implementing the internal P-Stratum Path Provider Interface. P-0AP, P-LAP, and P-RAP are Path Providers.

## Interface lifecycle terms

**Interface instance**
One negotiated activation of a versioned Interface contract. Its local identifiers are valid only until close or reset.

**Event sequence**
A monotonically increasing number assigned to provider events in one Interface instance, permitting deterministic ordering and gap detection.

**Submission**
One immutable R-Stratum SDU accepted by P-Stratum for delivery through an Edge service profile.

**Submission accepted**
The point at which P-Stratum accepts ownership of an immutable logical copy of an SDU. It does not mean delivery.

**Submission completed**
The terminal result for an accepted Submission. Successful completion means the Peer P-Stratum accepted and reconstructed the complete SDU, not that Peer R-Stratum processed it or a final Receiver was reached.

## Simulation terms

**Virtual Fabric**
A deterministic, reusable simulation engine that models endpoint delivery, link characteristics, virtual time, faults, and record/replay. It is test infrastructure, not the normative source of protocol semantics.

**Simulation front end**
A component translating one Nova architectural boundary into Virtual Fabric operations. P-0AP, a Simulated Adapter, and a Simulated Binding are different front ends.

**Simulation scenario**
A versioned description of Nodes, modeled Paths or links, characteristics, scheduled actions, seed, and clock policy.

**Simulation trace**
A deterministic record of control actions, virtual-time advancement, deliveries, failures, and observable events.

**Conforming simulation mode**
A mode in which simulated faults are translated into behavior permitted by the implemented Interface contract.

**Adversarial provider mode**
An explicitly enabled mode in which a simulated provider intentionally violates an Interface contract. It is not conformance evidence.

## Compatibility terms

**Compatibility Service**
A system application using an application-facing Nova Interface to provide compatibility with a legacy protocol or host facility.

**IP-over-Nova Compatibility Service**
A Compatibility Service that carries IPv4 or IPv6 datagrams through Nova using O-Stratum.

**Platform Attachment**
A platform-specific component connecting a Compatibility Service to an operating-system service or device abstraction.

## Contract terms

**NIDL**
Nova Interface Definition Language, the schema-driven language used to describe versioned architectural boundaries.

**Interface contract**
A versioned description of operations, events, data types, capabilities, errors, lifecycle, invariants, and conformance behavior.

**Peer protocol**
A protocol between peer entities at the same stratum, distinct from an intra-node Interface contract.
