# Stability gates for P-R 1.0

Do not promote `NOVA-IF-P-R` to 1.0 until all of the following hold:

- no placeholder data structures remain;
- lifecycle, close, reset, ownership, concurrency, and linearization rules are complete;
- metric units, provenance, age, validity, confidence, and unknown-value behavior are fixed;
- Obfuscated degree profile registry, bounds, zero semantics, freshness, and dummy-slot behavior are specified;
- Node identity continuity and address rotation are exercised;
- provider and consumer conformance suites cover normal, resource-limit, and race behavior;
- P-0AP passes the provider suite;
- R-Stratum passes the consumer suite against both a reference mock and P-0AP;
- P-RAP over at least one QUIC Binding passes the same provider-visible semantics;
- Edge aggregation with multiple Provider Paths is implemented and tested;
- finite event-backlog exhaustion is tested;
- no implementation-specific type appears in the public contract;
- an accepted ADR records the final 1.0 semantics.

Expected progression:

```text
0.2 semantic redesign
P-0AP implementation and deterministic race tests
0.3 corrections from implementation
R-Stratum consumer implementation
P-RAP/QUIC independent provider validation
1.0 freeze
```
