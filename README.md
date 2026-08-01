<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Nova

Nova is a research and engineering project for a new Internet protocol stack.

The long-term aim is an Internet that is simpler to operate, private by default, economically open to new participants, and deployable progressively alongside today’s TCP/IP infrastructure. Nova is not intended to be another VPN, overlay network, transport library, or isolated routing protocol. It is an attempt to redesign the stack as a coherent whole.

The original paper describes a network in which encrypted application data can travel over selectable routes, communication services can expose meaningful characteristics and prices, forwarding providers can be compensated in real time, and Nodes that add useful capacity can share in the resulting economic activity. The adoption model is deliberately incremental: the new network should grow inside the existing one rather than depend on a coordinated global replacement.

The paper is the source of the project’s direction, not its current specification. Its routing, privacy, settlement, monetary, and incentive mechanisms remain research goals until they are expressed as versioned contracts, reviewed protocol specifications, conformance tests, and interoperable implementations.

## Why Nova

The project starts from several observations about the present Internet:

- applications communicate, but IP addressing is tied to network interfaces and location;
- route choice and service characteristics are mostly hidden from end users and applications;
- privacy is commonly added through overlays instead of being built into the network architecture;
- inter-provider charging and settlement remain indirect, aggregated, and operationally expensive;
- operators that add forwarding capacity do not receive a direct protocol-level reward for carrying useful traffic; and
- replacing a globally deployed stack is impossible without a credible path for gradual adoption.

Nova explores whether these problems can be addressed together without abandoning the end-to-end principle. Intelligence and application policy remain at the endpoints, while the stack provides protected communication, explicit service characteristics, route choice, and—eventually—native economic settlement.

## Long-term vision

A complete Nova network is intended to provide:

- **privacy by design**: payload confidentiality, protected routing information, replay resistance, and relationship confidentiality as properties of the stack;
- **selectable communication services**: applications and users can express the characteristics they need and choose among suitable routes;
- **market-based routing and transport**: providers can advertise service characteristics and prices without inspecting or discriminating by application content;
- **real-time settlement**: the value of communication can be settled while traffic is carried and distributed among participating Nodes;
- **incentives for a distributed topology**: operators, individuals, and new hardware providers can be rewarded for adding useful forwarding capacity;
- **lower operational friction**: less manual router configuration, fewer bilateral settlement processes, and fewer centralized coordination points;
- **identity independent of attachment point**: mobility and multi-homing do not redefine the communicating entity; and
- **incremental adoption**: Nova can cross existing routed networks and support compatibility services for software that still expects IP.

These are objectives, not current capabilities. Production anonymous routing, service negotiation, traffic settlement, monetary issuance, proof of bandwidth, and economic consensus have not yet been implemented or validated.

## Stack architecture

Nova is divided into three strict strata. Each stratum owns its terminology, protocols, and internal state. Adjacent strata interact only through versioned Interfaces.

### Proximitate Stratum — P-Stratum

P-Stratum provides protected, message-preserving communication with authenticated Peers through one or more Paths. It hides the differences between local adjacency, remote association, simulation, and the technologies beneath them.

Its complete objectives are documented in [`protocols/p-stratum/objectives.md`](protocols/p-stratum/objectives.md).

P-Stratum uses three Path Provider protocols:

- **P-0AP** for deterministic zero-underlay association and simulation;
- **P-LAP** for association with Peers adjacent through a Nexus Fundamenta, using replaceable Adapters; and
- **P-RAP** for association with remote Peers across an existing routed underlay, using replaceable Bindings.

P-0AP, P-LAP, and P-RAP are protocols. Implementations of those protocols create running Path Provider instances, which maintain Provider Paths for P-Stratum common.

### Remotis Stratum — R-Stratum

R-Stratum is responsible for network-wide reachability and forwarding. It discovers and selects Routes, defines directional Links, establishes Trails and Flows, and carries Grams.

Its topology, privacy, route-selection, and forwarding mechanisms are still at an early design stage.

### Onerarii Stratum — O-Stratum

O-Stratum provides application-facing transport services. Its purpose is to carry application data while preserving the confidentiality and traffic-analysis-resistance properties required by the architecture.

O-Stratum remains largely a research and specification workstream.

### Interfaces between strata

The Interfaces are where concepts from adjacent strata are related. For example, the P–R Interface defines how P-Stratum service is presented to R-Stratum without exposing Path Provider, Adapter, Binding, locator, or simulation details.

The authoritative P–R terminology mapping is in [`contracts/interfaces/p-r/glossary.md`](contracts/interfaces/p-r/glossary.md).

```text
Applications and compatibility services
                 |
      O–Application Interface
                 |
            O-Stratum
                 |
          R–O Interface
                 |
            R-Stratum
                 |
          P–R Interface
                 |
            P-Stratum
                 |
      Path Provider Interface
          /          |          \
       P-0AP       P-LAP       P-RAP
                      |           |
                   Adapters     Bindings
                      |           |
             Nexus Fundamenta  Routed underlays
```

Nova protocol logic is intended to run in user space. A platform may require a small privileged driver or attachment shim, but routing, identity, cryptographic association, policy, and settlement semantics do not belong in kernel mode.

## What this repository contains

The repository currently focuses on the foundations required to turn the architecture into independently implementable software:

- versioned Interface contracts written in NIDL;
- conformance scenarios for providers and consumers;
- stratum-specific glossaries and architectural boundaries;
- deterministic simulation through P-0AP and the Virtual Fabric;
- early Rust crates that make the intended component boundaries concrete;
- planned P-RAP integration over user-space QUIC;
- planned P-LAP integration through simulated and Ethernet Adapters; and
- compatibility work, including IP-over-Nova, for gradual migration.

The main directories are:

- [`canon/`](canon/) — project-wide architecture, invariants, registries, and normative language;
- [`contracts/`](contracts/) — versioned Interfaces, schemas, and conformance scenarios;
- [`protocols/`](protocols/) — specifications and objectives owned by each stratum;
- [`implementations/`](implementations/) — implementation crates and executable prototypes;
- [`integrations/`](integrations/) — Adapters, Bindings, Platform Attachments, and SDK surfaces;
- [`simulation/`](simulation/) — deterministic profiles, scenarios, traces, and Virtual Fabric material;
- [`compatibility/`](compatibility/) — migration services such as IP-over-Nova;
- [`adr/`](adr/) — architectural decisions under discussion or accepted; and
- [`research/`](research/) — the original papers and other non-normative research inputs.

See [`REPOSITORY-MAP.md`](REPOSITORY-MAP.md) for a detailed inventory.

## Current status

Nova is in the design and early implementation phase.

The current repository establishes architectural boundaries and experimental contracts, but it does not yet provide an interoperable network stack. The Rust code is incomplete, the cryptographic and wire profiles are not stable, and the privacy and economic mechanisms have not undergone the analysis required for production use.

Do not use Nova today for production networking, financial settlement, or privacy-critical communication.

The immediate engineering sequence is:

1. make P-0AP and the Virtual Fabric deterministic and conformance-complete;
2. implement P-Stratum common against the Path Provider Interface;
3. develop the first R-Stratum executable subset against the P–R Interface;
4. implement P-RAP over IPv6-QUIC and IPv4-QUIC Bindings;
5. implement P-LAP first with a simulated Adapter and then Ethernet; and
6. validate mixed topologies before expanding into topology discovery, anonymous routing, settlement, and compatibility services.

See [`STATUS.md`](STATUS.md) for the present implementation state and [`ROADMAP.md`](ROADMAP.md) for the staged plan.

## Reading order

For a first technical reading:

1. this README;
2. [`canon/architecture.md`](canon/architecture.md);
3. the glossary index at [`canon/glossary.md`](canon/glossary.md);
4. the objectives or specification of the stratum of interest;
5. the relevant versioned Interface under [`contracts/interfaces/`](contracts/interfaces/); and
6. the corresponding ADRs and conformance scenarios.

The original papers explain the motivation and intended destination, but current implementation work follows the normative repository documents when they differ.

## Building and validation

```sh
make setup
make licenses
make check
```

The checks validate contracts and schemas, normalized generated material, conformance scenarios, context and dependency boundaries, terminology ownership, simulation fixtures, repository shape, licensing, and implementation tests where the required toolchains are installed.

Passing these checks establishes repository consistency only. It does not prove security, anonymity, economic soundness, or interoperability.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting changes. Contributions should preserve stratum boundaries, add tests or conformance material with new behavior, and keep published contract versions immutable.

Normative requirement words are interpreted according to [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt), as documented in [`canon/normative-language.md`](canon/normative-language.md).

## Licensing

Nova uses licences according to architectural role:

- **AGPL-3.0-or-later** for the core implementation;
- **Apache-2.0** for public Interfaces, Adapters, Bindings, Platform Attachments, conformance tooling, tests, and integration SDKs;
- **CC-BY-4.0** for architecture and specification prose; and
- **Apache-2.0 OR CC-BY-4.0** for machine-readable contracts and schemas.

Historical papers are excluded from those grants pending review of third-party material. Read [`LICENSE`](LICENSE), [`LICENSE-NOTICE.md`](LICENSE-NOTICE.md), [`docs/licensing.md`](docs/licensing.md), [`PATENTS.md`](PATENTS.md), and the nearest directory `LICENSE.md` before reuse.
