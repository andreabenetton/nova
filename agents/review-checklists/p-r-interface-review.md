# P-R Interface review checklist

- The contract exposes Edges, never Paths or provider provenance.
- One authenticated `NodeIdentityId` produces at most one active Edge per Interface instance.
- `PeerHandle` stability, address rotation, identity replacement, Edge revisions, removal, and reappearance are precise.
- Every Edge has at least one service profile and mandatory Obfuscated degree.
- Obfuscated degree is only an expansion cardinality; profile declaration, maximum, zero meaning, freshness, and stale behavior are defined.
- Mandatory version semantics are not represented as optional capabilities.
- SDU ownership, atomicity, reliability, lack of inter-SDU ordering, expiry, and exactly-one completion are explicit.
- Service-profile removal, orderly close, Edge removal, and Interface reset define terminal Submission behavior.
- Queues and event backlogs are finite; backpressure recovery and terminal reset delivery are event-driven.
- Opening supplies an atomic snapshot and continuation sequence.
- Reset is the final event after `INTERFACE_RESET` completion events and invalidates runtime identifiers.
- Submit/remove, profile-removal, close, and reset races have linearization rules.
- Metrics define a closed unit set, source, age, validity, confidence, and absent-value behavior.
- Provider and consumer conformance cover normal, resource-limit, failure, and race cases.
- No Adapter, Binding, QUIC, Ethernet, locator, simulation, or language-specific type leaks into the contract.
