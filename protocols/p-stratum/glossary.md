---
document_id: NOVA-GLOSSARY-P
status: draft
normative: true
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-Stratum glossary

This file owns P-Stratum terminology. It may be used together with the common glossary. R-Stratum and O-Stratum terminology is excluded except in an explicit Interface document.

**Nexus Fundamenta**  
The heterogeneous lower technologies commonly associated with the ISO-OSI Data Link Layer and exposed through device drivers or equivalent facilities.

**Peer**  
An authenticated Node reachable by P-Stratum through one or more established Paths.

**Peer handle**  
A local opaque identifier used by one P-Stratum implementation for a Peer during an Interface instance.

**Path**  
An established P-Stratum association through which P-Stratum Packets may be exchanged with a Peer.

**Provider Path**  
A Path supplied to P-Stratum common through the internal Path Provider Interface.

**Path Provider protocol**

A P-Stratum peer protocol that specifies how a class of Path Provider instances establishes, maintains, and removes Paths. P-0AP, P-LAP, and P-RAP are Path Provider protocols.

**Path Provider implementation**

Software implementing one Path Provider protocol and the internal P-Stratum Path Provider Interface.

**Path Provider instance**

A running realization of a Path Provider implementation within a Node. It creates and maintains Provider Paths and reports them to P-Stratum common through the Path Provider Interface.

The unqualified expression **Path Provider** is not a separate architectural kind. Normative text must use **Path Provider protocol**, **Path Provider implementation**, or **Path Provider instance**, according to the concept intended.

**Packet**  
The P-Stratum SDU exchanged between P-Stratum peer entities.

**Sequence**  
A P-Stratum grouping used to preserve the boundary of one submitted unit when it is carried by multiple Packets.

**P-Stratum common**  
The provider-independent P-Stratum component that groups Paths by authenticated Peer identity, applies selection policy, and implements the P–R Interface.

**P-Stratum Zero-Underlay Association Protocol (P-0AP)**  
A deterministic P-Stratum Path Provider protocol that specifies local or simulated association behavior without an external Nexus Fundamenta Adapter or routed-underlay Binding.

**P-Stratum Link Adjacency Protocol (P-LAP)**  
The P-Stratum Path Provider protocol used to discover and establish Paths with Nodes adjacent through a Nexus Fundamenta.

**Adapter**  
A P-LAP component that binds P-LAP to one Nexus Fundamenta technology or instance.

**Internal virtual Adapter**  
A P-LAP Adapter representing an internal Nexus Fundamenta-like attachment inside one device. It is distinct from P-0AP.

**P-Stratum Remote Association Protocol (P-RAP)**  
The P-Stratum Path Provider protocol used to establish Paths with remote Nodes through an already routed underlay.

**Binding**  
A P-RAP component that binds P-RAP to a specific integrated routed network and transport combination, such as IPv4-QUIC or IPv6-QUIC.

**Binding instance**  
An active realization of a Binding between local and remote locators.

**Remote locator**  
Binding-specific information required to reach a remote Node. It is not a Node address.

**P-RAP Association**  
An authenticated P-RAP relationship between Nodes. It may survive replacement of its Binding instance.

**Expansion cardinality contribution**  
A profile-qualified, freshness-bounded value supplied with a Provider Path for use by P-Stratum common when fulfilling the P–R Interface. Its cross-stratum meaning is defined only by that Interface.
