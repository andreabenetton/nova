<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Nova

Nova is a research and engineering project for a replacement Internet protocol stack.

Its long-term objective is not merely to add another overlay, tunnel, cryptocurrency payment layer, or privacy protocol to TCP/IP. Nova aims to define a coherent network architecture in which:

- routers and clients require substantially less manual configuration and operational management;
- connectivity can be paid for through real-time, very small payments;
- Nodes that contribute routing and transport resources can receive a share of that value;
- economic incentives favour a more distributed network topology and new classes of network hardware;
- confidentiality and unlinkability are architectural properties rather than optional additions;
- network neutrality can emerge from transparent market mechanisms instead of depending entirely on administrative enforcement;
- deployment and maintenance costs can be reduced through automation, decentralisation, and replaceable components; and
- adoption can proceed progressively over existing infrastructure, creating “the new Internet in the shell of the old.”

This is the destination described by the original Nova paper. The repository is the engineering path toward that destination.

## Project vision

The original Nova proposal starts from a simple question: what would the Internet look like if routing, transport, privacy, settlement, and incentives were designed together rather than accumulated as separate layers of historical compatibility?

Nova explores an answer built around five connected ideas:

1. **A replacement stack**
   Nova defines its own strata, Interfaces, identities, routing model, transport semantics, and compatibility mechanisms. It is not specified as an extension of the TCP/IP stack.

2. **Privacy by design**
   Confidentiality and resistance to unnecessary disclosure are intended to be structural properties of the protocols. The design must avoid exposing lower-level topology, locators, provider choices, or internal Path multiplicity across architectural boundaries unless the relevant Interface explicitly requires it.

3. **Economic participation**
   The long-term architecture is intended to support real-time settlement in which users pay for connectivity and participating Nodes receive compensation for resources they actually provide. The monetary and proof mechanisms required for this remain research work and are not implemented by the current scaffold.

4. **Distributed, low-administration networking**
   Nova seeks to reduce central coordination, manual configuration, and operational friction while allowing independently operated Nodes and heterogeneous network technologies to cooperate.

5. **Incremental adoption**
   Nova must be deployable before it replaces the existing Internet. Early implementations therefore use compatibility services and existing routed underlays while preserving a migration path toward native Nova networking.

These goals are coupled. Payments without privacy would create surveillance infrastructure; privacy without incentives would not by itself fund routing capacity; a clean architecture without an adoption path would remain academic; and incremental deployment without strict boundaries would simply reproduce the limitations of the existing stack.

## Current status

Nova is currently a **design and implementation scaffold**, not a production network and not an interoperable release.

The repository presently contains:

- draft normative architecture and stratum-scoped glossaries;
- versioned experimental Interface contracts;
- conformance scenarios and deterministic simulation models;
- Rust crate skeletons that make implementation boundaries explicit;
- proposed ADRs and unresolved research questions;
- licensing, contribution, and repository-validation policy.

The following are **not yet established**:

- a stable wire protocol;
- production-ready P-Stratum, R-Stratum, or O-Stratum implementations;
- independent interoperability evidence;
- a production privacy analysis;
- a complete economic, payment, or proof-of-resource design;
- a security review suitable for deployment;
- a stable `1.0` Interface or protocol specification.

See [`STATUS.md`](STATUS.md) for the detailed and current engineering status, and [`ROADMAP.md`](ROADMAP.md) for the implementation sequence.

## Architecture at a glance

Nova is divided into three strict strata. Each stratum owns its terminology and private protocols. Communication between strata occurs only through versioned Interfaces.

```text
Applications and compatibility services
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
       underlying technologies
```

### P-Stratum

P-Stratum establishes protected communication with Peers through Paths and presents a uniform service through the P–R Interface.

It contains a common service and three Path Provider protocols:

- **P-0AP**, for deterministic zero-underlay development, simulation, and replay;
- **P-LAP**, for communication with link-adjacent Peers through Adapters;
- **P-RAP**, for communication with remote Peers through Bindings over an already routed underlay.

P-0AP, P-LAP, and P-RAP are Path Provider protocols. A running realization is a Path Provider instance. Their private state and technology-specific details remain inside P-Stratum.

See [`protocols/p-stratum/objectives.md`](protocols/p-stratum/objectives.md) and [`protocols/p-stratum/glossary.md`](protocols/p-stratum/glossary.md).

### R-Stratum

R-Stratum is responsible for Nova routing concepts and behavior. Its vocabulary includes concepts such as Close, Edge, Link, Route, Trail, Flow, and Gram.

R-Stratum consumes only the P–R Interface. It must not depend on P-Stratum internals such as Paths, Adapters, Bindings, underlay locators, or provider-specific state.

### O-Stratum

O-Stratum provides application-facing transport semantics above R-Stratum. Compatibility services, including IP-over-Nova, belong above O-Stratum rather than inside P-Stratum or R-Stratum.

Where an operating system requires special integration, a minimal Platform Attachment may connect the compatibility service to facilities such as Linux TUN or Windows networking interfaces. Nova protocol logic remains in user space.

## Why the boundaries matter

Nova is intended to evolve through independently implementable components. The repository therefore treats Interfaces as first-class artifacts:

- higher strata depend only on versioned lower-stratum Interfaces;
- a stratum does not define itself using another stratum’s glossary;
- cross-stratum terminology appears together only in the corresponding Interface documentation;
- Adapters and Bindings isolate technology-specific integration;
- simulation validates contracts but does not become normative merely because it is executable;
- replaceable boundaries require contracts, conformance scenarios, and explicit compatibility rules.

This separation is essential to support independent implementations, multiple operating systems, different underlying technologies, and gradual migration from existing networks.

## Adoption path

The intended migration is progressive:

1. deterministic local development through P-0AP and the Virtual Fabric;
2. remote Nova communication over existing IP infrastructure through P-RAP Bindings such as QUIC-based Bindings;
3. native local adjacency through P-LAP Adapters such as Ethernet;
4. mixed topologies combining native and underlay-carried communication;
5. compatibility services that allow existing applications and IP traffic to use Nova;
6. later introduction of the broader routing, privacy, settlement, and incentive mechanisms described by the research vision.

Using existing IP networks during early deployment is a bootstrap mechanism, not the final architecture.

## Repository guide

For a human reader, a useful order is:

1. this README for the project purpose and current scope;
2. [`research/`](research/) for the original papers and historical rationale;
3. [`canon/`](canon/) for normative architecture, invariants, security principles, and glossary index;
4. [`protocols/`](protocols/) for stratum-owned protocol specifications and objectives;
5. [`contracts/`](contracts/) for versioned Interfaces and conformance semantics;
6. [`adr/`](adr/) for architectural decisions and unresolved proposals;
7. [`ROADMAP.md`](ROADMAP.md) and [`STATUS.md`](STATUS.md) for implementation progress;
8. [`implementations/`](implementations/) for code skeletons and later executable components.

`README.md` is written for people. Repository instructions for coding agents are in [`AGENTS.md`](AGENTS.md).

## Normative authority

The original papers explain the motivation and long-term direction, but they are non-normative research inputs. Engineering work follows the repository authority order:

1. `canon/`;
2. versioned `contracts/`;
3. stratum-owned `protocols/`;
4. integrations, simulation, and compatibility specifications;
5. accepted ADRs;
6. implementation documentation;
7. historical research material.

When a draft normative specification differs from a historical paper, the difference must be explicit and reviewable rather than silently inferred.

## Development and validation

The repository validates contracts, context boundaries, terminology ownership, licensing, generated documents, simulation fixtures, and repository structure.

```sh
make setup
make licenses
make check
```

The exact available checks and any environment limitations are recorded in [`VALIDATION.md`](VALIDATION.md).

## Licensing

Nova uses different licences for different architectural roles:

- **AGPL-3.0-or-later** for the core implementation;
- **Apache-2.0** for public Interfaces, Adapters, Bindings, Platform Attachments, conformance tooling, tests, and integration SDKs;
- **CC-BY-4.0** for architecture and specification prose;
- **Apache-2.0 OR CC-BY-4.0** for machine-readable contracts and schemas.

Historical papers remain excluded from the general documentation licence pending review of third-party material. Before reuse, consult [`LICENSE`](LICENSE), [`LICENSE-NOTICE.md`](LICENSE-NOTICE.md), [`docs/licensing.md`](docs/licensing.md), [`PATENTS.md`](PATENTS.md), and the nearest directory `LICENSE.md`.
