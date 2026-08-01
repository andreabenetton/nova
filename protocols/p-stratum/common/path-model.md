<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Private Path model

A Provider Path is private to P-Stratum and contains:

- provider instance and generation;
- provider-local Path identifier and revision;
- authenticated Peer Node identity;
- complete-SDU delivery properties and finite queue limits;
- abstract directional metrics;
- expansion-cardinality contribution with profile and freshness;
- provider transfer lifecycle.

P-Stratum common may maintain multiple Paths to one Peer. It must not export Path identifiers, provider type, Adapter, Binding, locator, Ethernet, QUIC, simulation profile, or seed.

Path selection is P-Stratum policy. The outward service contract is defined only by `NOVA-IF-P-R`.
