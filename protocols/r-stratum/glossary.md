---
document_id: NOVA-GLOSSARY-R
status: draft
normative: true
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# R-Stratum glossary

This file owns R-Stratum terminology. It may be used together with the common glossary. P-Stratum and O-Stratum terminology is excluded except in an explicit Interface document.

**Close**  
A Node at R-Stratum distance one from the local Node.

**Edge**  
An adjacency between two R-Stratum Nodes through which Grams may be exchanged. From either endpoint's perspective, the other Node is a Close.

**Distance**  
The number of R-Stratum hops between two Nodes on a Route.

**Neighbor**  
A Node within a defined maximum R-Stratum Distance.

**Degree**  
The number of Edges incident to one R-Stratum Node.

**Obfuscated Degree**  
A profile-bounded privacy-preserving expansion cardinality used by topology discovery. It is not asserted to be the exact Degree.

**Route**  
An unweighted sequence of Nodes connecting a Sender and a Receiver.

**Link**  
A directional weighted service defined by R-Stratum upon an Edge. Multiple Links may exist on one Edge and may advertise different band characteristics and prices.

**Trail**  
A directed and weighted sequence of Nodes and Links on which a Flow can be established.

**Flow**  
A Trail effectively established for data transmission.

**Gram**  
The R-Stratum SDU.

**Message**  
The R-Stratum control-plane PLU.

**Sender**  
The endpoint Node originating an R-Stratum transmission.

**Receiver**  
The endpoint Node receiving an R-Stratum transmission.

**Router Node**  
A Node forwarding Grams not intended for itself.

**Gateway**  
An R-Stratum Node able to forward topology-discovery traffic through an anonymized Route toward a registered Node.

**Beacon**  
A Node running the Beacon Facility.

**Authority**  
An R-Stratum role authoritative for a defined part of the Node-address namespace in the topology-discovery design.

**Facility**  
A distributed R-Stratum service supporting operation of the R-Stratum core.
