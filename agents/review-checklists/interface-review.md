# Interface review checklist

- Provider and consumer roles are unambiguous.
- Operations and events have stable unique identifiers.
- Types, limits, errors, and capabilities are explicit.
- Lifecycle, ordering, concurrency, cancellation, and backpressure are defined.
- Optional behavior is represented by capabilities, not accidental version forks.
- Unknown-field, unknown-error, and unknown-capability behavior is defined.
- Provider and consumer conformance scenarios exist.
- No unrelated implementation details cross the boundary.
