# P-R 0.2 invariant rationale

The machine-readable invariants in `interface.yaml` are normative. The most important consequences are:

1. Provider Paths never cross this Interface.
2. One authenticated `NodeIdentityId` produces at most one active Edge in an Interface instance.
3. `PeerHandle` is stable for that identity and never reassigned.
4. Every Edge exposes at least one service profile and one profile-bounded Obfuscated degree.
5. The first delivery profile is reliable, atomic, boundary preserving, and unordered between SDUs.
6. Finite queues, event backlogs, and capacity notification are mandatory.
7. Every accepted Submission has exactly one terminal completion, including before reset.
8. Local identifiers are scoped to one Interface instance.
9. P-0AP, P-LAP, P-RAP, Adapter, and Binding provenance remains invisible.
10. Mandatory version semantics are not optional capabilities.
