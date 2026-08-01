<!-- SPDX-License-Identifier: Apache-2.0 -->

# Virtual Fabric implementer

Implement the deterministic simulation engine against `NOVA-IF-VIRTUAL-FABRIC`. Preserve virtual-clock, seeded-random, scheduler, resource-limit, and record/replay guarantees. Do not introduce knowledge of R-Stratum or concrete P-LAP/P-RAP protocols into the engine.

## Required output

- changed authoritative files;
- deterministic algorithm and version declarations;
- scenario and trace validation;
- reproducibility evidence;
- unresolved risks stated explicitly.
