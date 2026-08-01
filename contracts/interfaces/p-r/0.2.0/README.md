# P-R Interface 0.2.0

`NOVA-IF-P-R 0.2.0` is the experimental semantic redesign of the service supplied by P-Stratum to R-Stratum.

The authoritative machine-readable contract is `interface.yaml`. Companion documents define lifecycle, data, security, neighbor-expansion, and stability semantics. Machine-readable provider and consumer scenarios make those rules executable.

This version deliberately replaces the Path-oriented `0.1.0` model:

- Provider Paths are private to P-Stratum;
- R-Stratum observes one Edge per authenticated `NodeIdentityId`;
- `PeerHandle` remains stable for that identity within the Interface instance;
- P-Stratum aggregates one or more Paths into each Edge;
- every Edge supplies at least one Edge service profile;
- every Edge carries a profile-bounded Obfuscated degree used only as neighbor-expansion cardinality;
- SDUs are accepted, completed, and delivered with explicit ownership, finite-queue, profile-removal, close, and reset semantics;
- every accepted Submission has exactly one terminal completion;
- the finite event stream is ordered and gap-detectable within one Interface instance;
- metric units and freshness semantics are closed and versioned;
- mandatory version behavior is not negotiated as an optional capability.

`0.1.0` remains immutable as an obsolete experimental record. No new implementation should consume it.
