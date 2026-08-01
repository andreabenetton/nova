---
document_id: NOVA-CANON-ARCHITECTURE
status: draft
normative: true
---

# Nova architecture

## Strict strata

Nova is organized into P-Stratum, R-Stratum, and O-Stratum. An underlying stratum does not call features of an overlying stratum. Communication across a stratum boundary is defined only by a versioned interface contract.

## P-Stratum decomposition

P-Stratum contains a common service and two different peer protocols:

- P-LAP for link adjacency through Adapters;
- P-RAP for remote association through Bindings.

P-LAP and P-RAP may share common P-Stratum types and security invariants, but they do not share discovery, timing, topology, or underlay assumptions.

```text
P-Stratum common
       |
NOVA-IF-P-PATH-PROVIDER
    /               \
 P-LAP              P-RAP
   |                  |
Adapter interface   Binding interface
   |                  |
Ethernet, Wi-Fi     IPv4-QUIC, IPv6-QUIC
```

## P-LAP and Adapters

P-LAP manages link-adjacent behavior. Adapters isolate Nexus Fundamenta-specific behavior, including locator representation, frame transmission, discovery primitives, MTU, and lower-layer signals.

## P-RAP and Bindings

P-RAP manages remote association behavior. Bindings isolate the integrated routed underlay. Binding names include the network and transport combination because current implementations integrate routing and transport behavior. Initial examples are IPv4-QUIC and IPv6-QUIC.

A P-RAP Association is a Nova relationship. A Binding instance is only the current carrier. The Association must not be identified solely by an IP address, port, socket, or QUIC connection.

## R-Stratum visibility

R-Stratum sees only `NOVA-IF-P-R`. It may observe abstract Path properties, including Path kind and measurable characteristics, but it must not know whether a Path uses Ethernet, QUIC, P-LAP packet formats, P-RAP control streams, or any Adapter or Binding implementation.

## Compatibility services

Legacy compatibility is implemented above O-Stratum as a system application. IP-over-Nova carries IP datagrams as application payload. Windows NDIS, Linux TUN, and equivalent mechanisms are Platform Attachments, not P-LAP Adapters or P-RAP Bindings.

## Documentation classes

- Canon: global normative concepts.
- Contracts: versioned architectural boundaries.
- Protocols: peer behavior at one stratum.
- Integrations: technology-specific Adapters and Bindings.
- Compatibility: legacy compatibility profiles and platform-independent behavior.
- Implementations: language- and platform-specific code decisions.
- Research: non-normative source material and unresolved questions.
