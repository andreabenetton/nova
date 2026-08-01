---
document_id: NOVA-GLOSSARY-COMMON
status: draft
normative: true
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Common Nova terminology

These terms are independent of a particular stratum.

**Node**  
A Nova distribution point capable of participating in one or more Nova strata.

**Node identity**  
The cryptographically authenticated identity of a Node under a defined identity profile.

**Node address**  
An address derived from a Node's long-term public key under one cryptographic suite. It is distinct from an underlay locator.

**Stratum**  
One strict architectural layer of the Nova stack. A stratum consumes only the versioned Interface of the stratum below it.

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

**Interface**  
A versioned behavioral contract between architectural components.

**Interface instance**  
One negotiated activation of a versioned Interface. Local identifiers are valid only for that instance.

**Operation**  
A request defined by an Interface and issued by its declared caller.

**Event**  
A notification defined by an Interface and emitted by its declared provider.

**Implementation**  
A concrete realization of a protocol, Interface provider, Interface consumer, or integration component.

**Conformance**  
Demonstrated compliance with a versioned normative contract and its executable scenarios.

**NIDL**  
Nova Interface Definition Language, used to describe versioned architectural boundaries.

**Peer protocol**  
A protocol between peer entities at the same stratum, distinct from an intra-node Interface.
