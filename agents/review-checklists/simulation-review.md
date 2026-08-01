<!-- SPDX-License-Identifier: Apache-2.0 -->

# Simulation review checklist

- The simulator implements a versioned boundary rather than a private shortcut.
- Virtual time, seed, PRNG, event ordering, and identifier allocation are explicit.
- Resource limits are finite and tested.
- Profiles are labeled as characteristic presets, not real-protocol conformance.
- Conforming faults remain within the Interface contract.
- Intentional violations require explicit adversarial mode.
- Portable traces include schema, implementation, scheduler, PRNG, seed, and scenario digest.
- R-Stratum tests do not depend on P-0AP or Virtual Fabric internals.
