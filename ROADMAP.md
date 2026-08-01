<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Roadmap

The roadmap is organized around executable, versioned boundaries. P-0AP is the first deterministic Path Provider, P-RAP/QUIC is the first real external-underlay integration, and R-Stratum development proceeds in parallel against the P-R Interface.

## M0 — Repository and contract foundation

- Maintain the canonical glossary, architecture, and invariants.
- Validate and normalize NIDL in CI.
- Enforce dependency and LLM-context boundaries.
- Preserve published experimental version directories.

## M1 — P-R semantic redesign before implementation

- Use `NOVA-IF-P-R 0.2.0` as the development baseline.
- Use `NOVA-IF-P-PATH-PROVIDER 0.3.0`.
- Use `NOVA-IF-P-0AP-CONTROL 0.2.0` and `NOVA-IF-VIRTUAL-FABRIC 0.1.0`.
- Freeze the distinction between private Paths and R-Stratum-visible Edges.
- Define Node identity and address rotation, Edge aggregation, service-profile lifecycle, profile-bounded Obfuscated degree, atomic reliable SDUs, ownership, finite Submission and event queues, orderly close, reset ordering, sequencing, and race linearization.
- Complete provider and consumer conformance scenarios before implementing P-0AP behavior.

M1 is the synchronization point for the parallel workstreams below.

## M2A — Deterministic Virtual Fabric and P-0AP

- Implement virtual time, seeded pseudo-random behavior, deterministic scheduling, stable tie-breaking, finite resources, and record/replay.
- Implement P-0AP as a `NOVA-IF-P-PATH-PROVIDER 0.3.0` provider.
- Support paired-node mode as the first useful topology. Reject self-Paths as Provider Paths; any future loopback diagnostic remains private and invisible to R-Stratum.
- Configure distinct authenticated Node identities, address rotation or replacement, and registered Obfuscated-degree profiles and values.
- Model latency, jitter, bandwidth, finite queues, backpressure, loss, duplication, reordering, partition, recovery, and reset.
- Separate contract-conforming simulation from explicitly adversarial provider behavior.

## M2B — P-Stratum common Edge engine

- Group Provider Paths by authenticated Node identity.
- Create at most one Edge per Peer in an Interface instance.
- Construct initial default Edge service profiles.
- Aggregate Path changes without leaking provenance.
- Implement stable Peer handles, Edge revisions, event sequences, Submission ownership, finite queues, service-profile removal, terminal completion, and reserved reset-event capacity.
- Pass the P-R provider conformance suite using P-0AP as the first Provider.

## M2C — R-Stratum executable core

This work proceeds in parallel with M2A and M2B.

- Consume only `NOVA-IF-P-R 0.2.0`.
- Implement the Gram model and control-plane registry.
- React to Edge addition, update, removal, reset, and capacity changes.
- Use Obfuscated degree only as a neighbor-expansion cardinality.
- Implement basic forwarding over deterministic or manually supplied Routes.
- Run consumer conformance first against a reference mock, then P-0AP.
- Defer Beacons, Authorities, payments, monetary issuance, and proof of bandwidth.

First acceptance topology:

```text
Node A -- P-0AP -- Node B -- P-0AP -- Node C
```

## M3 — P-RAP and QUIC vertical slice

- Test P-RAP first against the Simulated Binding.
- Implement QUIC-common plus IPv6-QUIC and IPv4-QUIC Bindings.
- Use a reliable control stream and a reliable P-R baseline mapping; DATAGRAM remains optional experimental work.
- Prove P-RAP Association independence from Binding instance, locator, socket, and QUIC connection.
- Supply the same authenticated Provider Path semantics used by P-0AP.
- Run the P-R provider-visible conformance suite over real asynchronous behavior.

## M4 — P-R 0.3 correction cycle

- Incorporate ambiguities discovered by P-0AP, P-Stratum common, R-Stratum, and P-RAP/QUIC implementations.
- Publish a new immutable `0.3.0` contract rather than modifying `0.2.0`.
- Expand race, failure, restart, metric, and Obfuscated-degree profile tests.

## M5 — P-LAP Ethernet vertical slice

- Test real P-LAP against the Simulated Adapter.
- Implement Ethernet as the first real Adapter.
- Prove discovery, association, protected SDU transfer, fragmentation, finite queue behavior, authenticated identity, and Provider Path lifecycle.
- Require unchanged R-Stratum behavior over resulting Edges.

## M6 — Mixed topology

```text
Node A -- P-LAP/Ethernet -- Node B -- P-RAP/QUIC -- Node C
```

Acceptance requires P-LAP and P-RAP to remain different peer protocols while P-Stratum common exposes only Edges, service profiles, metrics, and Obfuscated degree.

## M7 — R-Stratum topology-discovery subset

- Implement bounded neighbor expansion using Obfuscated degree.
- Specify dummy-slot behavior, common-Peer detection, profile algorithms, and privacy analysis.
- Implement Route-label lifecycle, cycle handling, stale-state handling, and deterministic topology fixtures.

## M8 — P-R 1.0 stability gate

Freeze `1.0` only after:

- P-0AP passes provider conformance;
- R-Stratum passes consumer conformance against mock and P-0AP;
- P-RAP/QUIC provides independent implementation evidence;
- Edge aggregation, identity continuity, lifecycle, close/reset behavior, metrics, event backlog, and Obfuscated degree profiles are complete;
- no placeholder structures or implementation leakage remain;
- the relevant ADRs are accepted.

## M9 — IP-over-Nova compatibility

- Complete point-to-point IP-over-Nova.
- Implement Linux TUN and a Windows Platform Attachment prototype.
- Add routed-gateway behavior only after point-to-point interoperability.

## Sequencing principle

P-0AP validates contracts and deterministic behavior; it does not define them. QUIC precedes Ethernet as the first real external integration because it is user-space and CI-friendly. R-Stratum starts in parallel because it depends only on P-R.

## Public-release licensing gate

Before the first public release:

- confirm the rights holder authorized to license pre-existing Nova material;
- complete the third-party content review for historical papers;
- validate all files with `make licenses`;
- require DCO sign-off in contribution automation;
- decide whether historical papers will be replaced by clean-room project diagrams;
- perform trademark clearance; and
- establish the OWFa contributor and designation process before any normative
  specification is called `1.0` or Final.
