# Nova

Nova is an experimental replacement Internet protocol stack organized into three strict strata:

- **Proximitate Stratum (P-Stratum)**: creates protected Paths to Peers, aggregates them into Edges, and supplies a versioned Edge service to R-Stratum.
- **Remotis Stratum (R-Stratum)**: discovers Routes, establishes Flows, routes Grams, and coordinates routing-related services.
- **Onerarii Stratum (O-Stratum)**: provides application-facing transport semantics.

This repository is deliberately organized for independent human and LLM-assisted implementation. A component receives only the contracts and design material required for its boundary. Higher strata depend on the **service interface** of lower strata, never on their private protocols or technology integrations.

## Current status

This is a **design scaffold**, not an interoperable implementation. All ADRs are proposed, all Interface versions are experimental, and the Rust crates are compilable-intent skeletons intended to make architectural boundaries visible.

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
   Edge aggregation, profiles, queues
                 |
       NOVA-IF-P-PATH-PROVIDER
          /          |          \
       P-0AP       P-LAP       P-RAP
         |            |           |
 Virtual Fabric    Adapters     Bindings
                      |           |
             Nexus Fundamenta  Integrated routed underlays
             (Ethernet, Wi-Fi) (IPv4-QUIC, IPv6-QUIC, ...)
```

- **P-0AP** is the deterministic zero-underlay Path Provider used for local, simulated, and replayable development. It creates authenticated Provider Paths, not Edges, has no Path-kind selector, and does not replace P-LAP or P-RAP conformance testing.
- **P-LAP** establishes Paths with link-adjacent Peers through **Adapters**.
- **P-RAP** establishes Paths with remote Peers through **Bindings**.
- A P-RAP Binding identifies the integrated network/transport combination, such as **IPv4-QUIC** or **IPv6-QUIC**, because contemporary routing and transport implementations are tightly integrated.
- **IP-over-Nova** is a Compatibility Service above O-Stratum. Its operating-system integration is provided by **Platform Attachments**, such as Windows NDIS or Linux TUN.

P-0AP, P-LAP, and P-RAP provide private Paths to P-Stratum common through `NOVA-IF-P-PATH-PROVIDER 0.3.0`. P-Stratum common groups Paths by authenticated Node identity and exposes one Edge per Peer through `NOVA-IF-P-R 0.2.0`. Every Edge includes service profiles and a mandatory, profile-bounded Obfuscated degree. Peer identity continuity, finite Submission and event queues, exactly-one terminal completion, and reset ordering are explicit contract semantics. R-Stratum never learns which Path Provider, Adapter, Binding, locator, or simulation component produced it.

## Authority order

1. `canon/`
2. `contracts/`
3. `protocols/`
4. `integrations/`, `simulation/`, and `compatibility/`
5. accepted ADRs
6. implementation documentation
7. `research/`, including the original papers

The original papers are preserved as non-normative research inputs. Where a normative document conflicts with a research paper, the normative document wins.

## First implementation target

The proposed first executable slice is:

- the Edge-oriented P-R 0.2.0 contract and its conformance suite;
- a deterministic Virtual Fabric;
- P-0AP paired-node and virtual-fabric modes;
- R-Stratum developed in parallel against `NOVA-IF-P-R`, first with mocks and P-0AP;
- P-RAP tested first against a Simulated Binding, then with IPv6-QUIC and IPv4-QUIC Bindings;
- a reliable QUIC control stream and reliable baseline data mapping first; QUIC DATAGRAM remains an optional later profile;
- P-LAP tested against a Simulated Adapter before the Ethernet Adapter;
- mixed P-LAP/P-RAP topology tests after both real integrations exist.

See `docs/p-r-interface-design.md`, `ROADMAP.md`, `adr/proposed/`, and `STATUS.md`.

## Local checks

```sh
make setup
make check
```

The contract tool validates NIDL YAML against JSON Schema, normalizes contracts, performs Nova-specific linting, checks context manifests and dependency boundaries, and supports compatibility checks. Simulation profiles and scenarios are validated independently against their schemas.
