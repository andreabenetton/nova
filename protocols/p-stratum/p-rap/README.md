<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-RAP

The P-Stratum Remote Association Protocol establishes protected Provider Paths with remote Nova Nodes through an already routed underlay. It uses Bindings through `NOVA-IF-P-RAP-BINDING` and supplies authenticated Paths through `NOVA-IF-P-PATH-PROVIDER 0.3.0`.

P-RAP behavior is transport-independent at its common boundary. Binding-specific behavior belongs under `integrations/p-rap-bindings/`. A Provider Path is private to P-Stratum and is later aggregated into an Edge by P-Stratum common.
