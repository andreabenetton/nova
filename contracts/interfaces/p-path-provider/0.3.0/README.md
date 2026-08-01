# P-Stratum Path Provider Interface 0.3.0

This experimental Interface is implemented by P-0AP, P-LAP, and P-RAP and consumed only by P-Stratum common. It supplies authenticated Provider Paths, their private properties, a privacy-preserving Obfuscated degree hint, finite-queue behavior, and complete SDU lifecycle.

Provider Paths are not Edges. P-Stratum common groups Paths by authenticated Node identity and creates the Edge model exposed by `NOVA-IF-P-R 0.2.0`.
