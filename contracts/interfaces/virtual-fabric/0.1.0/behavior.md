
# Behavior notes

The reference execution model uses virtual time. Event ordering is deterministic and versioned. The engine accepts opaque units and reports endpoint/link events; front ends translate those events into Path Provider, Adapter, or Binding behavior.

Exact queue disciplines, PRNG, scheduler ordering, trace structure, cancellation, and resource limits remain to be completed before stabilization.
