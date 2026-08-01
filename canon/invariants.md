---
document_id: NOVA-CANON-INVARIANTS
status: draft
normative: true
---

# Architectural invariants

1. A stratum implementation depends only on the declared versions of adjacent Interface contracts.
2. R-Stratum must not depend on P-0AP, P-LAP, P-RAP, any Adapter, any Binding, or the Virtual Fabric.
3. P-LAP must not depend on a concrete Adapter implementation.
4. P-RAP must not depend on a concrete Binding implementation.
5. P-Stratum common must consume P-0AP, P-LAP, and P-RAP through the Path Provider Interface.
6. An Adapter binds P-LAP to a Nexus Fundamenta. A Binding binds P-RAP to an integrated routed underlay. P-0AP uses neither.
7. A P-RAP Association must remain conceptually distinct from a Binding instance.
8. A Node address identifies a Nova Node cryptographically; a locator identifies a current means of reachability.
9. P-0AP must not expose a provider-specific Path kind or identity through the P-R Interface.
10. A P-0AP self-loop must not normally create an R-Stratum Edge.
11. The Virtual Fabric must be deterministic for a fixed schema version, scenario, seed, implementation version, and tie-breaking policy.
12. The Virtual Fabric and P-0AP are conformance infrastructure; their observed behavior cannot override normative contracts or protocol specifications.
13. Simulated Adapters and Bindings must implement the same versioned Interfaces as real Adapters and Bindings.
14. Adversarial provider behavior must be explicitly enabled and must not be reported as provider conformance.
15. IP-over-Nova must use the application-facing O-Stratum Interface and must not bypass R-Stratum or P-Stratum.
16. Platform Attachments must not implement Nova routing or P-Stratum behavior.
17. Published contract identifiers and numeric identifiers must never be reused within the same major version.
18. Generated code and canonical JSON are derived artifacts; NIDL YAML plus its validated semantic model are authoritative.
19. Research documents are not normative implementation inputs when a corresponding contract or protocol specification exists.
20. A component's `CONTEXT.yaml` is part of its enforceable design boundary.
