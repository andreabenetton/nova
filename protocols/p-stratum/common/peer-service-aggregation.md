<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Peer service aggregation

P-Stratum common maintains one aggregate for each authenticated Node identity. Each aggregate contains all usable Provider Paths for the corresponding Peer.

The aggregation algorithm must be deterministic for a fixed ordered Provider event stream and must define:

- identity equivalence under the selected identity profile;
- delivery-capability construction and metric aggregation;
- Path eligibility, selection, failover, and multipath policy;
- expansion-cardinality reconciliation;
- finite queue allocation and fairness;
- revision increments and provider-reset behavior.

The outward representation of an aggregate is specified only by the P–R Interface contract.
