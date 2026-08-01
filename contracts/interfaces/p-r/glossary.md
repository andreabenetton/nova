---
document_id: NOVA-GLOSSARY-IF-P-R
status: draft
normative: true
---

<!-- SPDX-License-Identifier: Apache-2.0 OR CC-BY-4.0 -->

# P–R Interface glossary and semantic mapping

This is the authoritative location for sentences that relate P-Stratum terminology to R-Stratum terminology.

**Path-to-Edge mapping**  
P-Stratum may maintain one or more usable Paths to the same authenticated Peer. Through the P–R Interface, that reachability is represented to R-Stratum as one Edge and the remote Node is represented as one Close. Path multiplicity, Path identifiers, Adapter details, Binding details, and provider provenance are not exposed.

**P–R submission**  
R-Stratum submits one complete Gram as an SDU through the P–R Interface. P-Stratum accepts, transports, and delivers that SDU according to the selected Interface capabilities without exposing Packet, Sequence, Path, Adapter, or Binding mechanics.

**Obfuscated-Degree mapping**  
P-Stratum supplies a profile-qualified expansion cardinality through the P–R Interface. R-Stratum consumes the exposed value as Obfuscated Degree for topology discovery. The derivation mechanism remains private to P-Stratum; the topology meaning remains owned by R-Stratum.

**Interface Edge identifier**  
A local identifier assigned by the P–R Interface to one exposed Edge incarnation. It is not a P-Stratum Path identifier and has no wire meaning.

**Submission**  
One immutable R-Stratum SDU accepted by P-Stratum through the P–R Interface.

**Submission accepted**  
The point at which P-Stratum accepts ownership of an immutable logical copy of the submitted SDU.

**Submission completed**  
The terminal P–R Interface result for an accepted Submission. Success means that the Peer-side P-Stratum accepted and reconstructed the complete SDU; it does not assert later R-Stratum processing.
