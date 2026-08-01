# Obfuscated degree

Each Provider Path supplies a current Obfuscated-degree hint for its Peer. P-Stratum common exposes one coherent value in every Edge snapshot.

The visible value is the number of neighbor-expansion slots R-Stratum should prepare. It is not an exact degree, Path count, Edge count, or physical-topology assertion. Zero means no additional expansion slot is required under the selected profile.

Every profile identifier and maximum is declared when the P-R Interface opens and comes from the canonical profile registry. Profile algorithms remain below P-R.

## Deterministic reconciliation

For multiple Provider Paths to the same Peer, P-Stratum common:

1. rejects values using undeclared profiles or exceeding the declared maximum;
2. applies configured profile preference, if any;
3. within one profile, selects the fresh value with the lowest age;
4. if equally fresh values conflict, selects the larger cardinality to avoid under-allocation and records a diagnostic;
5. if no fresh value exists, exposes the least-stale validly encoded value so the Edge remains describable, while R-Stratum refrains from new expansion until an update.

A selected profile, value, age class, or validity change increments `EdgeRevision`. Noise distribution, common-Peer detection, dummy-slot realization, and profile algorithms are separate work and must not be inferred from P-0AP behavior.
