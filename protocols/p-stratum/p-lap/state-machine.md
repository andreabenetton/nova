# P-LAP state-machine stub

Proposed conceptual states:

```text
INACTIVE -> DISCOVERING -> HANDSHAKING -> ASSOCIATED -> STALE -> CLOSED
```

The final state machine must define simultaneous discovery, duplicate handshakes, retransmission, timeouts, Adapter failure, rekey, and crash recovery. State names are not yet wire identifiers.
