---
document_id: NOVA-CANON-INVARIANTS
status: draft
normative: true
---

# Architectural invariants

1. A stratum implementation depends only on the declared versions of adjacent interface contracts.
2. R-Stratum must not depend on P-LAP, P-RAP, any Adapter, or any Binding.
3. P-LAP must not depend on a concrete Adapter implementation.
4. P-RAP must not depend on a concrete Binding implementation.
5. P-Stratum common must consume P-LAP and P-RAP through the Path Provider interface.
6. An Adapter binds P-LAP to a Nexus Fundamenta. A Binding binds P-RAP to an integrated routed underlay.
7. A P-RAP Association must remain conceptually distinct from a Binding instance.
8. A Node address identifies a Nova Node cryptographically; a locator identifies a current means of reachability.
9. IP-over-Nova must use the application-facing O-Stratum interface and must not bypass R-Stratum or P-Stratum.
10. Platform Attachments must not implement Nova routing or P-Stratum behavior.
11. Published contract identifiers and numeric identifiers must never be reused within the same major version.
12. Generated code and canonical JSON are derived artifacts; NIDL YAML plus its validated semantic model are authoritative.
13. Research documents are not normative implementation inputs when a corresponding contract or protocol specification exists.
14. A component's `CONTEXT.yaml` is part of its enforceable design boundary.
