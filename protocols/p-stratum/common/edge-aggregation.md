# Edge aggregation

P-Stratum common maintains a map from authenticated Node identity to one Peer aggregate. Each aggregate contains all usable Provider Paths and produces one Edge snapshot.

The aggregation algorithm must be deterministic for a fixed ordered Provider event stream. It must define:

- identity equivalence using the profile-qualified Node identity identifier;
- profile construction and metric aggregation;
- Path eligibility and failover;
- Obfuscated-degree selection or combination;
- queue allocation and fairness;
- revision increments;
- the exact linearization point for Edge addition, update, and removal.

The initial implementation may expose one default service profile per Edge. The data model must remain capable of multiple profiles without leaking the underlying Paths.
