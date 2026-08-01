# Data model

## Runtime identifiers

`InterfaceInstanceId`, `PeerHandle`, `EdgeId`, `SubmissionId`, and `EventSequence` are local runtime identifiers. They have no wire meaning and are invalid after Interface reset or close.

An `EdgeId` is never reused within one Interface instance. A Peer becoming reachable again after `edge-removed` receives a new `EdgeId`.

A `PeerHandle` is stable for one `NodeIdentityId` during one Interface instance, may appear again when the same Peer obtains a new Edge, and is never assigned to another identity.

## Node identity

`NodeIdentity` contains a profile-qualified `NodeIdentityId` plus one or more `NodeAddress` values. The identifier is the sole equality key used for Peer aggregation. Each address associates a cryptographic-suite identifier with a digest derived from the corresponding long-term public key, and providers must prove its binding to the identity identifier.

Addresses are canonically sorted by cryptographic-suite identifier and duplicate suite/address entries are invalid. Address-set growth or rotation with valid continuity proof updates the existing Edge. A changed identity identifier creates a different Peer and Edge.

A change of underlay locator, Adapter, Binding instance, or Provider Path does not change Node identity.

## Edge

An `EdgeSnapshot` contains:

- `EdgeId` and `EdgeRevision`;
- the local `PeerHandle`;
- the authenticated `NodeIdentity`;
- one or more `EdgeServiceProfile` values;
- the mandatory `ObfuscatedDegree`.

`EdgeRevision` increases monotonically for every visible update to an Edge. Consumers ignore stale updates.

## Service profiles

An Edge service profile is an abstract delivery promise. It does not reveal P-0AP, P-LAP, P-RAP, Adapter, Binding, locator, Ethernet, QUIC, or simulation provenance.

The 0.2 baseline profile provides:

- complete-SDU boundary preservation;
- Peer authentication;
- confidentiality, integrity, and replay protection between P-Stratum Peers;
- reliable completion or an explicit terminal failure;
- duplicate suppression within an Edge incarnation;
- no inter-SDU ordering guarantee.

A service profile identifier is scoped to one Edge incarnation. It remains stable while the profile exists and is not reused after removal.

## Metrics

Metrics are separated into inbound and outbound groups where applicable. Only two units exist in this version:

- `MICROSECONDS` for latency and jitter;
- `BITS_PER_SECOND` for capacity.

Every metric states its source, age when the containing snapshot is emitted or returned, sample window, total validity duration, and optional confidence in parts per million from 0 through 1,000,000. A metric is fresh when `age_micros < valid_for_micros`; consumers add local elapsed time after reception when checking later freshness. Unknown data is absent, never a fabricated zero.

## Obfuscated degree

`ObfuscatedDegree.value` is the number of neighbor-expansion slots R-Stratum prepares for the Peer. It is not an exact degree claim. It may include positive noise and excludes known common Peers under the named obfuscation profile.

Every profile used by an Edge is declared in `InterfaceOpened`, including its maximum value. The profile identifier does not alter the base consumer semantics: R-Stratum treats the value only as an expansion cardinality. Profile algorithms and privacy parameters remain below the Interface.

The degree age is measured when the containing snapshot is emitted or returned. A stale degree does not remove the Edge or prevent data transfer, but R-Stratum must not start new topology expansion from it until a fresh update arrives.

## Interface limits

`InterfaceOpened` supplies typed finite bounds for Edge count, SDU size, queued SDUs and bytes per service profile, and the event backlog. An implementation may advertise smaller bounds than another implementation but may not silently exceed or replace them with an unbounded queue.

## Submissions

A Submission is an immutable logical copy of one R-Stratum SDU. `SubmissionAccepted` transfers logical ownership to P-Stratum. A successful `SubmissionCompleted` means the Peer P-Stratum accepted and reconstructed the complete SDU. It does not mean the Peer R-Stratum processed it or that the final Receiver was reached.
