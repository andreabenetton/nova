
# P-0AP determinism

For a fixed:

- P-0AP protocol version;
- Virtual Fabric Interface version;
- scenario schema version and scenario content;
- deterministic seed;
- implementation version;
- event tie-breaking policy;

a conforming run must produce the same externally observable trace.

Determinism requires:

- a virtual monotonic clock;
- a seeded pseudo-random generator with a named algorithm and version;
- a stable priority order for simultaneous events;
- stable identifiers or deterministic identifier allocation;
- no dependence on wall-clock scheduling, thread race order, hash-map iteration order, or platform entropy;
- explicit recording of implementation and schema versions in traces.

Real-time execution may be provided for demonstrations, but it is not the reference conformance mode.
