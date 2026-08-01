# P-Stratum review

Status: non-normative research assessment.

## Valid architectural role

P-Stratum should transform heterogeneous lower connectivity into protected, message-preserving Paths presented through one service contract to R-Stratum.

## Correct decomposition

- P-Stratum common exposes `NOVA-IF-P-R`.
- P-LAP manages link adjacency and consumes Adapters.
- P-RAP manages remote Association and consumes Bindings.
- P-LAP and P-RAP both implement the Path Provider contract.

A routed underlay is not merely another P-LAP Adapter. IPv4-QUIC and IPv6-QUIC are P-RAP Bindings because discovery, timing, congestion, locator, migration, and topology semantics differ from Nexus Fundamenta adjacency.

## Findings retained for later protocol work

- Define peer, Path, Edge, Association, Adapter, Binding, and locator precisely.
- Separate association lifecycle from data-transfer lifecycle.
- Separate packet number, message identifier, and fragment index.
- Specify exact AEAD nonce and key-epoch construction before any protected wire format is frozen.
- Do not expose stable Nova Node addresses or post-association message types unnecessarily in cleartext.
- Treat CRC32C as accidental-corruption machinery, not cryptographic integrity, and do not duplicate AEAD without a measured reason.
- Define Noise pattern, suite, transcript, identity binding, retransmission, downgrade, and simultaneous-open behavior exactly.
- Do not couple proof-of-work puzzles to ephemeral key generation without a complete challenge and resource policy.
- Distinguish Adapter-reported native limits from P-Stratum SDU fragmentation.
- Treat Delta-t bounds as explicit protocol assumptions; routed underlays do not provide strict physical MPL bounds.
- Make reliable and unreliable SDU classes explicit rather than duplicating end-to-end reliability everywhere.
- Define ACK, NACK, replay, retransmission, reassembly, abandonment, and backpressure behavior before claiming reliable transport.
- Make constant-rate shaping and chaff optional profiles until cost and congestion interactions are solved.
- Report packet-format efficiency separately from total efficiency including chaff, retransmission, control traffic, and padding.
- Bound control-plane priority to prevent starvation.
- Keep common-peer detection and obfuscated degree out of the mandatory first profile until a complete private protocol exists.

## First implementation recommendation

- P-LAP with Ethernet Adapter.
- P-RAP with IPv6-QUIC and IPv4-QUIC Bindings.
- Reliable QUIC control stream.
- QUIC DATAGRAM for message-oriented data when negotiated.
- TCP Bindings later as compatibility fallbacks.
