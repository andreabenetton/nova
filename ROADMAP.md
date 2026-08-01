# Roadmap

The roadmap is organized around executable boundaries rather than a serial implementation of the full stack. Once `NOVA-IF-P-R` and `NOVA-IF-P-PATH-PROVIDER` are usable, R-Stratum, P-0AP, P-RAP, and later P-LAP can advance in parallel without crossing knowledge boundaries.

## M0 — Repository and contract foundation

- Freeze glossary terms used by the repository.
- Validate NIDL source files in CI.
- Generate canonical contract representations.
- Enforce dependency and context boundaries.
- Keep all architecture decisions in proposed ADRs until reviewed.

## M1 — Executable P-Stratum boundaries

- Complete `NOVA-IF-P-R 0.1.0`.
- Complete `NOVA-IF-P-PATH-PROVIDER 0.2.0` for P-0AP, P-LAP, and P-RAP.
- Complete `NOVA-IF-P-0AP-CONTROL 0.1.0` and `NOVA-IF-VIRTUAL-FABRIC 0.1.0`.
- Produce provider and consumer conformance suites.
- Generate or implement deterministic mocks for R-Stratum and Path Provider testing.
- Freeze Path lifecycle, SDU submission and delivery, backpressure, Path characteristics, and failure semantics before depending on them.

M1 is the synchronization point after which the following workstreams proceed in parallel.

## M2A — Deterministic Virtual Fabric and P-0AP

- Implement the Virtual Fabric with a virtual clock, seeded pseudo-random generator, deterministic event queue, stable tie-breaking rules, and record/replay traces.
- Implement P-0AP as the first executable Path Provider.
- Support loopback, paired-node, virtual-fabric, and replay modes.
- Make paired-node mode the default useful topology; self-loop mode must not normally expose an Edge to R-Stratum.
- Support deterministic latency, jitter, bandwidth, queue limits, backpressure, loss, duplication, reordering, partition, recovery, and restart events.
- Separate contract-conforming fault simulation from explicitly adversarial provider behavior.

## M2B — R-Stratum executable core

This work proceeds in parallel with M2A.

- Implement the R-Stratum Gram model and control-plane registry against `NOVA-IF-P-R` only.
- React to Edge addition, update, and removal without inspecting P-0AP, P-LAP, or P-RAP internals.
- Implement basic processing and forwarding over manually supplied or deterministic Routes.
- Run deterministic tests first against a mock P-Stratum and then against P-0AP.
- Defer Beacons, Authorities, monetary issuance, proof of bandwidth, and traffic payments.

The first acceptance target is a three-node R-Stratum forwarding test over P-0AP:

```text
Node A -- P-0AP -- Node B -- P-0AP -- Node C
```

## M3 — P-RAP protocol and QUIC vertical slice

- Complete the minimum P-RAP peer protocol draft.
- Complete `NOVA-IF-P-RAP-BINDING 0.1.0`.
- Test P-RAP first against the Simulated Binding over the Virtual Fabric.
- Implement the QUIC-common layer and IPv6-QUIC and IPv4-QUIC Bindings.
- Use a reliable QUIC control stream and QUIC DATAGRAM where available.
- Prove that a P-RAP Association is independent from a Binding instance, IP locator, socket, or QUIC connection.
- Expose remote Paths through the same P-Stratum interfaces already used by P-0AP.

## M4 — First multi-node interoperable prototype

- Run R-Stratum unchanged over P-RAP Paths between at least three nodes.
- Prove Path creation, Gram delivery, intermediate forwarding, Path failure, Binding reconnection, and node restart.
- Test IPv4-QUIC and IPv6-QUIC interoperability and explicit Association survival rules.
- Preserve the ability to run the same R-Stratum tests over P-0AP for deterministic reproduction.

## M5 — P-LAP Ethernet vertical slice

- Complete the P-LAP peer protocol draft.
- Complete `NOVA-IF-P-LAP-ADAPTER 0.1.0`.
- Test P-LAP first against the Simulated Adapter over the Virtual Fabric.
- Implement the Ethernet Adapter.
- Prove peer discovery, association, protected SDU transfer, fragmentation, and Path lifecycle.
- Require R-Stratum to operate over P-LAP Paths without source changes or knowledge of Ethernet.

## M6 — Mixed topology

Validate a mixed topology such as:

```text
Node A -- P-LAP/Ethernet -- Node B -- P-RAP/QUIC -- Node C
```

Acceptance requires:

- P-LAP and P-RAP remain different peer protocols;
- both provide Paths through `NOVA-IF-P-PATH-PROVIDER`;
- P-Stratum exposes uniform behavior through `NOVA-IF-P-R`;
- R-Stratum sees only Edges and abstract Path characteristics;
- failures recorded from real integrations can be reproduced through Virtual Fabric traces when representable at the Path level.

## M7 — R-Stratum topology-discovery subset

- Implement bounded neighborhood discovery and Route-label lifecycle.
- Add deterministic topology fixtures, cycle handling, failure, and stale-state tests.
- Keep common-Peer detection and obfuscated degree feature-gated until their protocols and privacy properties are specified.
- Continue excluding monetary and proof-of-bandwidth mechanisms from the mandatory subset.

## M8 — IP-over-Nova compatibility

- Complete the point-to-point profile.
- Implement Linux TUN Platform Attachment.
- Implement Windows Platform Attachment prototype.
- Add a routed-gateway profile only after the point-to-point profile is interoperable.

## Sequencing principle

P-0AP is the first executable Path Provider. P-RAP over QUIC is the first real external-underlay integration because it is user-space and CI-friendly. Ethernet remains the first P-LAP Adapter but must not block R-Stratum or P-RAP development. The simulator is evidence and test infrastructure; it never becomes the normative definition of protocol behavior.
