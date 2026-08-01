# Nova

Nova is an experimental replacement Internet protocol stack organized into three strict strata:

- **Proximitate Stratum (P-Stratum)**: creates protected paths to peers.
- **Remotis Stratum (R-Stratum)**: discovers routes, establishes flows, routes grams, and coordinates routing-related services.
- **Onerarii Stratum (O-Stratum)**: provides application-facing transport semantics.

This repository is deliberately organized for independent human and LLM-assisted implementation. A component receives only the contracts and design material required for its boundary. Higher strata depend on the **service interface** of lower strata, never on their private protocols or technology integrations.

## Current status

This is a **design scaffold**, not an interoperable implementation. All ADRs are proposed, all interface versions are experimental, and the Rust crates are compileable skeletons intended to make architectural boundaries visible.

## Architectural decomposition

```text
Applications and compatibility services
                 |
            O-Stratum
                 |
       NOVA-IF-R-O / NOVA-IF-O-A
                 |
            R-Stratum
                 |
             NOVA-IF-P-R
                 |
            P-Stratum common
            /             \
         P-LAP           P-RAP
           |               |
       Adapters          Bindings
           |               |
  Nexus Fundamenta   Integrated routed underlays
  (Ethernet, Wi-Fi)  (IPv4-QUIC, IPv6-QUIC, ...)
```

- **P-LAP** establishes paths with link-adjacent peers through **Adapters**.
- **P-RAP** establishes paths with remote peers through **Bindings**.
- A P-RAP Binding identifies the integrated network/transport combination, such as **IPv4-QUIC** or **IPv6-QUIC**, because contemporary routing and transport implementations are tightly integrated.
- **IP-over-Nova** is a compatibility service above O-Stratum. Its operating-system integration is provided by **Platform Attachments**, such as Windows NDIS or Linux TUN.

## Authority order

1. `canon/`
2. `contracts/`
3. `protocols/`
4. `integrations/` and `compatibility/`
5. accepted ADRs
6. implementation documentation
7. `research/`, including the original papers

The original papers are preserved as non-normative research inputs. Where a normative document conflicts with a research paper, the normative document wins.

## First implementation target

The proposed first slice is:

- P-LAP with an Ethernet Adapter;
- P-RAP with IPv4-QUIC and IPv6-QUIC Bindings;
- a reliable QUIC control stream;
- QUIC DATAGRAM for message-oriented P-RAP data when supported;
- R-Stratum developed against a mock implementation of `NOVA-IF-P-R`;
- IP-over-Nova point-to-point profile with Linux TUN and Windows Platform Attachment stubs.

See `ROADMAP.md`, `adr/proposed/`, and `STATUS.md`.

## Local checks

```sh
make setup
make check
```

The contract tool validates NIDL YAML against JSON Schema, normalizes contracts, performs Nova-specific linting, checks context manifests and dependency boundaries, and supports compatibility checks.
