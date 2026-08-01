# R-Stratum implementer

Consume only `NOVA-IF-P-R` and `NOVA-IF-R-O`. Develop first against a mock P-Stratum, then run the same tests against P-0AP and later real P-LAP/P-RAP Paths. Do not inspect P-0AP, P-LAP, P-RAP, Adapter, Binding, or Virtual Fabric internals.

## Required output

- changed authoritative files;
- version and compatibility assessment;
- tests or conformance scenarios using only adjacent Interfaces;
- evidence that provider-specific branches were not added;
- unresolved risks stated explicitly.
