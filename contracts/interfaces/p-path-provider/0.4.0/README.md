# P-Stratum Path Provider Interface 0.4.0

This experimental Interface is implemented by Path Provider instances conforming to P-0AP, P-LAP, or P-RAP and consumed only by P-Stratum common. It supplies authenticated Provider Paths, their private properties, a privacy-preserving Expansion cardinality hint, finite-queue behavior, and complete SDU lifecycle.

Provider Paths remain private to P-Stratum. P-Stratum common groups Paths by authenticated Node identity and implements the upper Interface without exporting Path provenance.
