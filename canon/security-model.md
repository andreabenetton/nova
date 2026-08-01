---
document_id: NOVA-CANON-SECURITY-MODEL
status: draft
normative: true
---

# Security model

Every security claim must identify the attacker class it addresses.

## Attacker classes

- Passive local observer: observes one Nexus Fundamenta or routed underlay segment.
- Active local attacker: injects, drops, delays, duplicates, or reorders units.
- Malicious authenticated peer: completes authentication and violates protocol behavior.
- Sybil attacker: creates multiple Nova identities.
- Compromised endpoint: controls keys and plaintext at one endpoint.
- Multi-link observer: correlates observations across multiple locations.
- Resource-exhaustion attacker: consumes state, CPU, bandwidth, or queue capacity.

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

P-Stratum link protection alone does not establish end-to-end relationship anonymity. Constant-rate shaping, chaff, degree obfuscation, proof of bandwidth, and monetary security remain research topics until separately specified and reviewed.
