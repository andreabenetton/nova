
# Behavior notes

The control Interface is test infrastructure. It configures P-0AP but never acts as a peer protocol or an R-Stratum service.

Deterministic behavior requires explicit scenario, seed, virtual-clock, scheduler, pseudo-random algorithm, implementation version, and tie-breaking policy. Wall-clock execution is not the conformance reference.

A self-loop is permitted only as a diagnostic mode and does not normally request an exposed Path. Paired-node mode is the minimum useful topology.
