---
document_id: NOVA-CANON-SECURITY-MODEL
status: draft
normative: true
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->


# Security model

Every security claim must identify the attacker class it addresses.

## Attacker classes

- Passive local observer: observes one Nexus Fundamenta or routed underlay segment.
- Active local attacker: injects, drops, delays, duplicates, or reorders units.
- Malicious authenticated Peer: completes authentication and violates protocol behavior.
- Sybil attacker: creates multiple Nova identities.
- Compromised Endpoint: controls keys and plaintext at one Endpoint.
- Multi-link observer: correlates observations across multiple locations.
- Resource-exhaustion attacker: consumes state, CPU, bandwidth, or queue capacity.
- Faulty Path Provider: violates the internal Path Provider Interface through defects or deliberate adversarial testing.
- Faulty simulation controller: supplies malformed, contradictory, or resource-exhausting scenarios.

## Required analyses

Each peer protocol and integration must specify:

- identity binding;
- replay protection;
- nonce and key-epoch rules;
- downgrade resistance;
- malformed-unit behavior;
- state and queue limits;
- timeout assumptions;
- logging and privacy impact;
- which metadata remains visible to the underlay.

Simulation components must additionally specify:

- deterministic seed and virtual-clock behavior;
- resource limits for Nodes, Paths, events, queues, traces, and scenario duration;
- whether a fault is modeled below an Interface or as an intentional Interface violation;
- trace integrity and provenance;
- behavior when a scenario cannot be represented without violating the selected conformance mode.

P-Stratum link protection alone does not establish end-to-end relationship anonymity. The P-R Interface defines the observable Obfuscated-degree hint, but its noise distribution, private common-Peer detection, dummy-slot protocol, and privacy guarantees remain research and specification work. Constant-rate shaping, chaff, proof of bandwidth, and monetary security also remain research topics until separately specified and reviewed.

P-0AP and Virtual Fabric can test specified security invariants and failure handling but cannot prove properties that depend on real Ethernet, IP, QUIC, operating-system, timing, or cryptographic implementations.
