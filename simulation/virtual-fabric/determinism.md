
# Determinism requirements

Reference execution uses a virtual monotonic clock and explicit advancement. No wall-clock sleep is required.

A trace header records:

- scenario schema version;
- trace schema version;
- Virtual Fabric Interface version;
- engine implementation identifier and version;
- deterministic seed;
- pseudo-random algorithm identifier;
- scheduler policy identifier;
- scenario digest.

The same header and scenario must either reproduce the same observable trace or fail with an explicit incompatibility error.
