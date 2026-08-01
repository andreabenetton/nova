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
The lower Nova stratum. It establishes protected Paths to Peers and presents those Paths to R-Stratum.

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

## Node and topology terms

**Node**
A Nova distribution point capable of acting as an Endpoint, Router node, or provider of a Facility.

**Endpoint**
A Node that originates or receives traffic intended for itself.

**Sender**
The Endpoint originating a transmission.

**Receiver**
The Endpoint receiving a transmission.

**Router node**
A Node forwarding data not intended for itself.

**Peer**
A Node directly reachable through one established P-Stratum Path. A Peer can be link-adjacent through P-LAP, remotely associated through P-RAP, or represented by P-0AP in a local or simulated environment. P-0AP exposes a modeled Path kind and does not add a new R-Stratum topology category.

**Path**
An established P-Stratum association between two Peers through which P-Stratum SDUs can be exchanged.

**Edge**
The relationship exposed by P-Stratum to R-Stratum for a Path. An Edge is typed so R-Stratum can distinguish a link-adjacent relationship from a remote-association relationship without learning the underlying technology or Path Provider.

**Route**
An unweighted sequence of Nodes connecting a Sender and Receiver, as used by R-Stratum topology discovery.

**Trail**
A directed and weighted sequence of Nodes and Links on which a Flow can be established.

**Flow**
A Trail effectively established for data transmission.

**Close**
A Node at R-Stratum distance one from another Node.

## P-Stratum protocol and integration terms

**P-Stratum common service**
The implementation-independent service presented to R-Stratum and supplied internally by Path Providers.

**P-Stratum Zero-Underlay Association Protocol (P-0AP)**
A deterministic P-Stratum Path Provider used to establish local or simulated Peer associations without an external Nexus Fundamenta Adapter or routed-underlay Binding. The digit `0` denotes zero external underlay; it does not denote R-Stratum distance zero.

**P-Stratum Link Adjacency Protocol (P-LAP)**
The P-Stratum peer protocol used to discover and establish Paths with Nodes adjacent through a Nexus Fundamenta.

**Adapter**
A P-LAP component that binds P-LAP to one Nexus Fundamenta technology or instance. Examples include Ethernet and Wi-Fi Adapters.

**Internal virtual Adapter**
A P-LAP Adapter representing an internal Nexus Fundamenta-like attachment inside one device. It remains a P-LAP integration and is distinct from P-0AP, which directly provides deterministic local or simulated Paths.

**P-Stratum Remote Association Protocol (P-RAP)**
The P-Stratum peer protocol used to establish Paths with remote Nodes through an already routed underlay.

**Binding**
A P-RAP component that binds P-RAP to a specific integrated routed network and transport combination. Examples include IPv4-QUIC and IPv6-QUIC Bindings.

**Binding instance**
An active realization of a Binding between local and remote locators used to convey P-RAP units.

**Remote locator**
Binding-specific information required to reach a remote Node. A Remote locator is not a Nova Node address and may change without changing Node identity.

**P-RAP Association**
An authenticated P-RAP relationship between Nova Nodes. An Association may survive replacement of its Binding instance.

**Path Provider**
A component implementing the internal P-Stratum Path Provider Interface. P-0AP, P-LAP, and P-RAP are Path Providers.

## Simulation terms

**Virtual Fabric**
A deterministic, reusable simulation engine that models endpoint delivery, link characteristics, virtual time, faults, and record/replay for P-0AP and simulated Adapter or Binding implementations. It is test infrastructure and is not the normative source of protocol semantics.

**Simulation front end**
A component translating one Nova architectural boundary into Virtual Fabric operations. P-0AP, a Simulated Adapter, and a Simulated Binding are different Simulation front ends.

**Simulation scenario**
A versioned description of Nodes, modeled Paths or links, characteristics, scheduled actions, deterministic seed, and clock policy used to drive the Virtual Fabric.

**Simulation trace**
A deterministic record of control actions, virtual-time advancement, deliveries, failures, and externally observable events suitable for replay.

**Conforming simulation mode**
A mode in which simulated faults are translated into behavior permitted by the implemented Interface contract.

**Adversarial provider mode**
An explicitly enabled test mode in which a simulated provider intentionally violates an Interface contract to test defensive behavior. It must never be confused with normal conformance evidence.

## Compatibility terms

**Compatibility Service**
A system application using an application-facing Nova Interface to provide compatibility with a legacy protocol or host facility.

**IP-over-Nova Compatibility Service**
A Compatibility Service that carries IPv4 or IPv6 datagrams through Nova using O-Stratum.

**Platform Attachment**
A platform-specific component connecting a Compatibility Service to an operating-system service or device abstraction. Examples include Windows NDIS and Linux TUN Platform Attachments.

## Contract terms

**NIDL**
Nova Interface Definition Language, the schema-driven language used to describe versioned architectural boundaries.

**Interface contract**
A versioned description of operations, events, data types, capabilities, errors, lifecycle, invariants, and conformance behavior between provider and consumer roles.

**Peer protocol**
A protocol between peer entities at the same stratum. It is distinct from an Interface contract, which describes an intra-node architectural boundary.
