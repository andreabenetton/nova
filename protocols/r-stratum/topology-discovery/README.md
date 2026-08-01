<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Topology discovery

Topology discovery begins from R-Stratum Edges. For each Edge, R-Stratum creates one Close and uses the mandatory Obfuscated Degree as the number of Neighbor-expansion slots to prepare.

The value is a bounded privacy hint, not an exact topology assertion. R-Stratum must tolerate positive noise and dummy slots and must not infer hidden lower-stratum multiplicity, physical adjacency, or underlay technology.

Before this subsystem stabilizes, it must specify:

- supported Obfuscated-Degree profiles;
- dummy-slot encoding and termination;
- common-Close detection interaction;
- bounded flooding and resource limits;
- Route-label lifecycle;
- stale hint and Edge-revision behavior;
- privacy and denial-of-service analysis.
