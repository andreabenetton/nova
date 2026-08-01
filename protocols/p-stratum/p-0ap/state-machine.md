
# P-0AP state machine

Minimum provider states:

```text
INACTIVE -> ACTIVE -> DRAINING -> INACTIVE
                 \
                  -> FAILED
```

Minimum modeled Path states:

```text
ABSENT -> AVAILABLE -> DEGRADED -> UNAVAILABLE -> ABSENT
```

Rules:

- Provider activation precedes any provider Path event.
- A Path is assigned a new generation when restored after removal.
- `provider-sdu-received` is not emitted after final Path removal for the same generation.
- In-flight SDUs at partition or removal follow the scenario's declared disposition: deliver-before-cutoff, drop, or explicit adversarial violation.
- Deactivation drains or drops queued work according to the selected profile and emits no later conforming events.
