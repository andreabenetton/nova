---
document_id: NOVA-CANON-ARCHITECTURE
status: draft
normative: true
---

# Nova architecture

## Strict strata

Nova is organized into P-Stratum, R-Stratum, and O-Stratum. An underlying stratum does not call features of an overlying stratum. Communication across a stratum boundary is defined only by a versioned Interface contract.

## P-Stratum decomposition

P-Stratum contains a common service and three Path Providers:

- P-0AP for deterministic local and simulated associations without an external underlay;
- P-LAP for link adjacency through Adapters;
- P-RAP for remote association through Bindings.

P-0AP is a development and conformance aid. P-LAP and P-RAP are the production peer protocols. All three provide Paths through the same internal Path Provider Interface and remain invisible to R-Stratum.

```text
P-Stratum common
       |
NOVA-IF-P-PATH-PROVIDER
   /          |          \
P-0AP       P-LAP       P-RAP
  |            |           |
Virtual      Adapter     Binding
Fabric       Interface   Interface
               |           |
       Ethernet, Wi-Fi  IPv4-QUIC, IPv6-QUIC
```

## P-0AP and Virtual Fabric

P-0AP establishes deterministic local or simulated Paths. Its default useful mode connects distinct Nova Node instances, even when they execute in one process. A literal self-loop is a diagnostic mode and must not normally expose an Edge to R-Stratum.

P-0AP may model either `LINK_ADJACENT` or `REMOTE_ASSOCIATION` Path behavior. It must not introduce a P-0AP-specific Path kind visible through `NOVA-IF-P-R`.

The Virtual Fabric is a reusable deterministic engine. It can support:

- P-0AP directly at the Path Provider boundary;
- a Simulated Adapter that exercises the real P-LAP protocol;
- a Simulated Binding that exercises the real P-RAP protocol.

These front ends are not interchangeable. A P-0AP test validates Path-level and inter-stratum behavior, while Simulated Adapter and Binding tests validate P-LAP and P-RAP behavior respectively.

## P-LAP and Adapters

P-LAP manages link-adjacent behavior. Adapters isolate Nexus Fundamenta-specific behavior, including locator representation, frame transmission, discovery primitives, MTU, and lower-layer signals.

## P-RAP and Bindings

P-RAP manages remote Association behavior. Bindings isolate the integrated routed underlay. Binding names include the network and transport combination because current implementations integrate routing and transport behavior. Initial examples are IPv4-QUIC and IPv6-QUIC.

A P-RAP Association is a Nova relationship. A Binding instance is only the current carrier. The Association must not be identified solely by an IP address, port, socket, or QUIC connection.

## R-Stratum visibility

R-Stratum sees only `NOVA-IF-P-R`. It may observe abstract Path properties, including Path kind and measurable characteristics, but it must not know whether a Path was provided by P-0AP, P-LAP, or P-RAP, nor whether Ethernet, QUIC, a simulated integration, or another technology is involved.

R-Stratum development may begin against a mock P-Stratum and P-0AP before real P-LAP or P-RAP integrations exist. This is a required demonstration of strict strata, not a temporary architectural shortcut.

## Simulation authority

Normative Interface and protocol specifications define behavior. Conformance scenarios derive from those specifications. P-0AP and Virtual Fabric implementations must conform to them. Observed simulator behavior must never become authoritative merely because it is executable.

## Compatibility services

Legacy compatibility is implemented above O-Stratum as a system application. IP-over-Nova carries IP datagrams as application payload. Windows NDIS, Linux TUN, and equivalent mechanisms are Platform Attachments, not P-LAP Adapters or P-RAP Bindings.

## Documentation classes

- Canon: global normative concepts.
- Contracts: versioned architectural boundaries.
- Protocols: peer behavior at one stratum.
- Integrations: technology-specific Adapters and Bindings.
- Simulation: deterministic test-model semantics, scenarios, and traces.
- Compatibility: legacy compatibility profiles and platform-independent behavior.
- Implementations: language- and platform-specific code decisions.
- Research: non-normative source material and unresolved questions.
