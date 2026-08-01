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
The lower Nova stratum. It establishes protected paths to peers and presents those paths to R-Stratum.

**Remotis Stratum (R-Stratum)**  
The middle Nova stratum. It establishes communication across routes, performs routing functions, and coordinates routing-related facilities.

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
A Nova distribution point capable of acting as an endpoint, router, or provider of a facility.

**Endpoint**  
A node that originates or receives traffic intended for itself.

**Sender**  
The endpoint originating a transmission.

**Receiver**  
The endpoint receiving a transmission.

**Router node**  
A node forwarding data not intended for itself.

**Peer**  
A node directly reachable through one established P-Stratum Path. A peer can be link-adjacent through P-LAP or remotely associated through P-RAP. The term does not imply physical adjacency unless the Path kind is `LINK_ADJACENT`.

**Path**  
An established P-Stratum association between two peers through which P-Stratum SDUs can be exchanged.

**Edge**  
The relationship exposed by P-Stratum to R-Stratum for a Path. An Edge is typed so R-Stratum can distinguish a link-adjacent relationship from a remote-association relationship without learning the underlying technology.

**Route**  
An unweighted sequence of nodes connecting a sender and receiver, as used by R-Stratum topology discovery.

**Trail**  
A directed and weighted sequence of nodes and links on which a flow can be established.

**Flow**  
A Trail effectively established for data transmission.

**Close**  
A node at R-Stratum distance one from another node.

## P-Stratum protocol and integration terms

**P-Stratum common service**  
The implementation-independent service presented to R-Stratum and supplied internally by Path Providers.

**P-Stratum Link Adjacency Protocol (P-LAP)**  
The P-Stratum peer protocol used to discover and establish Paths with nodes adjacent through a Nexus Fundamenta.

**Adapter**  
A P-LAP component that binds P-LAP to one Nexus Fundamenta technology or instance. Examples include Ethernet and Wi-Fi Adapters.

**P-Stratum Remote Association Protocol (P-RAP)**  
The P-Stratum peer protocol used to establish Paths with remote nodes through an already routed underlay.

**Binding**  
A P-RAP component that binds P-RAP to a specific integrated routed network and transport combination. Examples include IPv4-QUIC and IPv6-QUIC Bindings.

**Binding instance**  
An active realization of a Binding between local and remote locators used to convey P-RAP units.

**Remote locator**  
Binding-specific information required to reach a remote node. A Remote locator is not a Nova node address and may change without changing node identity.

**P-RAP association**  
An authenticated P-RAP relationship between Nova nodes. An Association may survive replacement of its Binding instance.

**Path Provider**  
A component implementing the internal P-Stratum Path Provider interface. P-LAP and P-RAP are Path Providers.

## Compatibility terms

**Compatibility Service**  
A system application using an application-facing Nova interface to provide compatibility with a legacy protocol or host facility.

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
