<!-- SPDX-License-Identifier: Apache-2.0 -->

# P-0AP implementer

Implement P-0AP against `NOVA-IF-P-PATH-PROVIDER 0.3.0`, `NOVA-IF-P-0AP-CONTROL 0.2.0`, and the Virtual Fabric Interface. P-0AP creates authenticated Provider Paths, not R-Stratum Edges. It has no Path-kind selector.

Model finite Submission and event queues, exactly-one terminal Provider Submission results, deterministic identity and address updates, profile-bounded Obfuscated degree, reset ordering, and record/replay. Do not import R-Stratum internals or imitate Ethernet, QUIC, P-LAP, or P-RAP private behavior.

## Required output

- changed authoritative files;
- version and compatibility assessment;
- deterministic scenarios and Path Provider conformance tests;
- clear distinction between conforming and adversarial modes;
- evidence that no control or simulation metadata crosses provider boundaries;
- unresolved risks stated explicitly.
