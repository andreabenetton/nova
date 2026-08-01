---
document_id: NOVA-CANON-ARCHITECTURE
status: draft
normative: true
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->


# Nova architecture

## Strict strata

Nova is organized into P-Stratum, R-Stratum, and O-Stratum. Communication across a stratum boundary is defined only by a versioned Interface contract.

## P-Stratum decomposition

P-Stratum contains a common service and three Path Provider protocols: P-0AP, P-LAP, and P-RAP. Running Path Provider instances conforming to those protocols provide internal Paths through the same Path Provider Interface and remain invisible across the P–R Interface.

```text
P-0AP          P-LAP          P-RAP
  \              |              /
    NOVA-IF-P-PATH-PROVIDER
                 |
          P-Stratum common
       identity and Path aggregation
       service-profile construction
       multipath and queue policy
                 |
            NOVA-IF-P-R
                 |
             R-Stratum
```

## Path-to-Edge aggregation

A Path is private to P-Stratum. P-Stratum common groups all usable Provider Paths that authenticate the same Peer Node identity into one R-Stratum-visible Edge.

- The first usable Path creates an Edge.
- Additional Paths to the same Peer update the Edge.
- Loss of one Path updates the Edge while another remains usable.
- Loss of the last usable Path removes the Edge.
- Reappearance creates a new Edge identifier. The same authenticated identity may retain its Peer handle within the Interface instance.

R-Stratum selects an Edge service profile. P-Stratum common selects the concrete Path or Paths. No Path Provider, Adapter, Binding, locator, QUIC, Ethernet, or simulation identifier crosses the P-R boundary.

## P-0AP and Virtual Fabric

P-0AP establishes deterministic local or simulated Provider Paths. Its default useful mode connects distinct Nova Node instances. A self-Path is not announced by a conforming Path Provider instance. Any future loopback diagnostic remains private to its test-control surface and never creates an Edge.

The Virtual Fabric can support P-0AP, a Simulated Adapter exercising real P-LAP, and a Simulated Binding exercising real P-RAP. These front ends are not interchangeable.

## P-LAP and Adapters

P-LAP manages link-adjacent behavior. Adapters isolate Nexus Fundamenta-specific locator, frame, discovery, MTU, and lower-layer behavior.

## P-RAP and Bindings

P-RAP manages remote Association behavior. Bindings isolate integrated routed underlays such as IPv4-QUIC and IPv6-QUIC. A P-RAP Association is not identified solely by an IP address, port, socket, or QUIC connection.

## R-Stratum visibility

R-Stratum sees only `NOVA-IF-P-R`. It observes authenticated Peer identity, one Edge per reachable Peer, Edge service profiles, Obfuscated degree, and SDU lifecycle events. It does not observe Paths or their provenance.

## Obfuscated degree

Every Edge includes an Obfuscated degree: the number of neighbor-expansion slots R-Stratum should prepare, not the exact Peer degree. The Interface freezes observable meaning, profile identifiers and maxima, freshness, and update rules. Noise distribution, common-Peer detection, dummy-slot realization, and profile algorithms remain versioned below the boundary.

## Simulation authority

Normative Interface and protocol specifications define behavior. Conformance scenarios derive from them. Simulator behavior never becomes authoritative merely because it is executable.

## Compatibility services

Legacy compatibility is implemented above O-Stratum as a system application. Windows NDIS, Linux TUN, and equivalents are Platform Attachments, not P-LAP Adapters or P-RAP Bindings.

## Documentation classes

- Canon: global normative concepts.
- Contracts: versioned architectural boundaries.
- Protocols: peer behavior at one stratum.
- Integrations: technology-specific Adapters and Bindings.
- Simulation: deterministic test models, scenarios, and traces.
- Compatibility: legacy compatibility profiles.
- Implementations: language- and platform-specific code.
- Research: non-normative source material and unresolved questions.
