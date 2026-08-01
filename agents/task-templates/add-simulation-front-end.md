# Task template: add a simulation front end

- Name the architectural boundary being simulated.
- Implement the same versioned Interface as the real provider.
- Consume `NOVA-IF-VIRTUAL-FABRIC` rather than bypassing the boundary.
- Define how Virtual Fabric faults map to contract-conforming behavior.
- Keep intentional Interface violations behind an explicit adversarial mode.
- Add deterministic scenarios, provider conformance tests, and replay fixtures.
- Do not claim conformance for the real technology represented by a profile.
