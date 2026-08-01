
# Record and replay

Recording captures control actions, virtual-time changes, accepted submissions, scheduled disposition, deliveries, characteristic updates, failures, and emitted Interface events.

Replay must declare whether it reproduces:

- only externally observable Interface events; or
- the complete internal scheduler trace.

Externally observable replay is the portable conformance format. Internal traces may be implementation-specific but must be labeled accordingly.
