<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# R-Stratum

R-Stratum consumes only `NOVA-IF-P-R 0.2.0`. It observes authenticated Peers, aggregated Edges, service profiles, Obfuscated degree, and complete SDU lifecycle. It does not observe P-Stratum Paths or their provenance.

R-Stratum must be implementable against a reference mock and P-0AP without reading P-0AP, P-LAP, P-RAP, Adapter, Binding, QUIC, Ethernet, or Virtual Fabric internals.

The original Nova paper remains research lineage for Routes, Trails, Flows, Grams, topology discovery, link identification, flow setup, data transmission, Beacon Facility, and Validating Facility. Incomplete paper mechanisms are not silently promoted into normative behavior.
