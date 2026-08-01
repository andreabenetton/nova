# P-RAP state-machine stub

Proposed conceptual states:

```text
UNBOUND -> BINDING_OPEN -> ASSOCIATING -> ASSOCIATED -> REBINDING -> CLOSED
```

The final state machine must define duplicate Binding instances, simultaneous open, Binding failure, locator migration, reauthentication, capability downgrade, and Association expiry.
