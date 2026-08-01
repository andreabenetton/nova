# Data model

Provider Path identifiers, revisions, Submission identifiers, and event sequences are scoped to one provider generation and have no wire meaning.

Provider metrics use only `MICROSECONDS` and `BITS_PER_SECOND`. Their age is measured when the containing Path snapshot is emitted or returned. Unknown metrics are absent.

A Provider Path declares finite queue limits and whether it supports priority-prefix scheduling. These are inputs to P-Stratum common when constructing Edge service profiles; they are not exposed directly to R-Stratum.

The Provider Path may be reliable or unreliable and ordered or unordered. P-Stratum common may add mechanisms or combine Paths, but it may expose only service profiles whose guarantees it can actually satisfy.
