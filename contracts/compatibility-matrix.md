# Compatibility matrix

Current contracts are experimental and require exact-version matching. Published version directories remain immutable.

## Current development baselines

- `NOVA-IF-P-R 0.2.0` is the Edge-oriented redesign for P-Stratum/R-Stratum work. It replaces the Path-oriented `0.1.0` model for new implementations.
- `NOVA-IF-P-PATH-PROVIDER 0.4.0` supplies authenticated Provider Paths, declared Obfuscated-degree profiles, scheduling and expiry options, finite Submission/event queues, and terminal reset ordering to P-Stratum common.
- `NOVA-IF-P-0AP-CONTROL 0.3.0` removes Path-kind selection and adds explicit identity creation/update, Path update, Obfuscated-degree, and finite-resource controls.
- `NOVA-IF-VIRTUAL-FABRIC 0.1.0` remains the deterministic simulation-engine boundary.

## Preserved historical versions

- `NOVA-IF-P-R 0.1.0` exposed Paths and is retained only as an experimental historical contract.
- `NOVA-IF-P-PATH-PROVIDER 0.1.0` and `0.2.0` are preserved.
- `NOVA-IF-P-0AP-CONTROL 0.1.0` is preserved.

No compatibility is implied between these `0.x` versions. Stable same-major negotiation is planned only after `1.0.0`.
