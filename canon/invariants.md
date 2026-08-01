---
document_id: NOVA-CANON-INVARIANTS
status: draft
normative: true
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->


# Architectural invariants

1. A stratum implementation depends only on declared adjacent Interface contracts.
2. R-Stratum must not depend on P-0AP, P-LAP, P-RAP, any Path Provider, Adapter, Binding, or the Virtual Fabric.
3. P-LAP must not depend on a concrete Adapter implementation.
4. P-RAP must not depend on a concrete Binding implementation.
5. P-Stratum common consumes P-0AP, P-LAP, and P-RAP only through the Path Provider Interface.
6. An Adapter binds P-LAP to a Nexus Fundamenta. A Binding binds P-RAP to an integrated routed underlay. P-0AP uses neither.
7. A P-RAP Association remains distinct from a Binding instance.
8. A Node address identifies a Node cryptographically; a locator identifies a current means of reachability.
9. A Path is private to P-Stratum. The P-R Interface exposes Edges, not Paths.
10. P-Stratum common exposes at most one active Edge per profile-qualified authenticated Node identity identifier in one Interface instance.
11. Path addition or removal does not add or remove an Edge while another usable Path to the same Peer remains.
12. R-Stratum selects an Edge service profile; P-Stratum selects the underlying Path or Paths.
13. P-0AP must not expose provider, simulation, Path-kind, or Virtual Fabric identity through P-R.
14. A self-Path is not a conforming Provider Path; any diagnostic loopback remains private and never creates an Edge.
15. Every Edge snapshot contains an Obfuscated degree, treated only as a privacy-preserving expansion cardinality.
16. An active Edge authenticates the Peer and provides confidentiality, integrity, replay protection, and complete-SDU boundary preservation between P-Stratum Peers.
17. The P-R baseline provides reliable atomic SDU delivery while an Edge remains usable, with no inter-SDU ordering guarantee.
18. Every accepted Submission receives exactly one terminal result, including an `INTERFACE_RESET` result before Interface reset.
19. Providers use finite Submission and event queues, observable backpressure, and reserved capacity for terminal reset notification.
20. Edge IDs, Peer handles, Submission IDs, and event sequences are local to one Interface instance and invalid after reset; a Peer handle is never reassigned to a different identity.
21. An Edge ID is never reused within one Interface instance.
22. The initial Edge snapshot and subsequent event stream form one atomic, gap-detectable sequence.
23. The Virtual Fabric is deterministic for fixed schema, scenario, seed, implementation, and tie-breaking policy.
24. P-0AP and Virtual Fabric cannot override normative contracts.
25. Simulated Adapters and Bindings implement the same Interfaces as real ones.
26. Adversarial behavior is explicitly enabled and is not conformance evidence.
27. IP-over-Nova uses the application-facing O-Stratum Interface and does not bypass the stack.
28. Platform Attachments do not implement Nova routing or P-Stratum behavior.
29. Published identifiers are never reused within the same major version.
30. NIDL YAML plus its validated semantic model are authoritative; generated outputs are derived.
31. Research documents are non-normative when a corresponding contract exists.
32. A component's `CONTEXT.yaml` is part of its enforceable design boundary.
33. Mandatory version semantics are not negotiated as optional capabilities.
34. Metric units are closed and versioned; freshness is expressed without assuming a shared process clock.
35. Every Obfuscated degree uses a declared profile and remains within its declared maximum.
36. A service profile is removed only after accepted Submissions using it reach terminal results.
