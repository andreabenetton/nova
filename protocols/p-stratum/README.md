<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-Stratum protocols

P-Stratum consists of a common service plus three Path Providers:

- P-0AP for deterministic local and simulated Paths without an external underlay;
- P-LAP for link adjacency;
- P-RAP for remote Association.

All three supply Paths to P-Stratum common through `NOVA-IF-P-PATH-PROVIDER`. None is visible directly to R-Stratum.

P-0AP is not a replacement for protocol conformance. The real P-LAP protocol must be tested through an implementation of `NOVA-IF-P-LAP-ADAPTER`, and the real P-RAP protocol through an implementation of `NOVA-IF-P-RAP-BINDING`.
