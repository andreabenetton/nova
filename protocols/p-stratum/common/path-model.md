<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Private Path model

A Provider Path is private to P-Stratum and contains:

- provider instance and generation;
- provider-local Path identifier and revision;
- authenticated Peer Node identity;
- complete-SDU delivery properties and finite queue limits;
- abstract directional metrics;
- Obfuscated degree with profile and freshness;
- provider Submission lifecycle.

P-Stratum common may maintain multiple Paths to one Peer. It must not export Path identifiers, Path kinds, provider type, Adapter, Binding, locator, Ethernet, QUIC, simulation profile, or seed.

Path selection is P-Stratum policy. R-Stratum selects an Edge service profile, not a concrete Path.
