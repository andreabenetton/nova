<!-- SPDX-License-Identifier: Apache-2.0 -->

# R-Stratum implementer

Consume only `NOVA-IF-P-R 0.2.0` and `NOVA-IF-R-O`. Develop first against a reference mock, then run the same tests against P-0AP and later P-LAP/P-RAP-derived Edges.

R-Stratum observes Edges, never Paths. It selects Edge service profiles, respects finite backpressure and service-profile removal, validates event and Edge revisions, handles close/reset terminal ordering, and treats fresh Obfuscated degree only as a privacy-preserving neighbor-expansion cardinality. It must not branch on P-0AP, P-LAP, P-RAP, Adapter, Binding, QUIC, Ethernet, locator, or Virtual Fabric details.

## Required output

- changed authoritative files;
- version and compatibility assessment;
- consumer conformance tests using only adjacent Interfaces;
- evidence that provider-specific branches and exact-degree assumptions were not added;
- unresolved risks stated explicitly.
