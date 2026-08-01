<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Expansion-cardinality reconciliation

Each Provider Path may supply a profile-qualified expansion-cardinality contribution for its Peer. P-Stratum common reconciles those contributions when implementing the P–R Interface.

For multiple Provider Paths to the same Peer, P-Stratum common:

1. rejects values using undeclared profiles or exceeding declared maxima;
2. applies configured profile preference;
3. within one profile, selects the fresh value with the lowest age;
4. if equally fresh values conflict, selects the larger cardinality and records a diagnostic;
5. if no fresh value exists, preserves only behavior explicitly allowed by the P–R Interface.

The contribution is not defined as a P-Stratum topology measurement. Its cross-stratum interpretation is specified only in the P–R Interface glossary.
