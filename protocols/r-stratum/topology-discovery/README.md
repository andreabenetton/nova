# Topology discovery

Topology discovery begins from R-Stratum Edges. For each Edge, R-Stratum creates one Close and uses the mandatory Obfuscated degree as the number of neighbor-expansion slots to prepare.

The value is a bounded privacy hint, not an exact topology assertion. R-Stratum must tolerate positive noise and dummy slots and must not infer Provider Path count, physical adjacency, or underlay technology.

Before this subsystem stabilizes, it must specify:

- supported Obfuscated-degree profiles;
- dummy-slot encoding and termination;
- common-Peer detection interaction;
- bounded flooding and resource limits;
- Route-label lifecycle;
- stale hint and Edge-revision behavior;
- privacy and denial-of-service analysis.
