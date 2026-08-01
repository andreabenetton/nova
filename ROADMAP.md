# Roadmap

## M0 — Repository and contract foundation

- Freeze glossary terms used by the repository.
- Validate NIDL source files in CI.
- Generate canonical contract representations.
- Enforce dependency and context boundaries.
- Keep all architecture decisions in proposed ADRs until reviewed.

## M1 — P-Stratum interface and mocks

- Complete `NOVA-IF-P-R 0.1.0`.
- Complete the P-Stratum Path Provider interface.
- Produce provider and consumer conformance suites.
- Implement deterministic mock P-Stratum for R-Stratum work.

## M2 — P-LAP Ethernet prototype

- Complete P-LAP peer protocol draft.
- Complete P-LAP Adapter interface.
- Implement Ethernet Adapter.
- Prove peer discovery, association, protected SDU transfer, fragmentation, and path lifecycle.

## M3 — P-RAP QUIC prototype

- Complete P-RAP peer protocol draft.
- Complete P-RAP Binding interface.
- Implement IPv6-QUIC and IPv4-QUIC Bindings sharing a QUIC-common layer.
- Use a reliable QUIC control stream and QUIC DATAGRAM where available.
- Prove that a P-RAP association is independent from a Binding instance.

## M4 — R-Stratum first interoperable subset

- Implement topology-discovery subset against `NOVA-IF-P-R` only.
- Keep facilities, monetary issuance, proof of bandwidth, and traffic-payment mechanisms out of the mandatory first subset.

## M5 — IP-over-Nova compatibility

- Complete point-to-point profile.
- Implement Linux TUN Platform Attachment.
- Implement Windows Platform Attachment prototype.
- Add a routed-gateway profile only after the point-to-point profile is interoperable.
