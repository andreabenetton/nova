<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-0AP state machine

Provider states:

```text
INACTIVE -> ACTIVE -> DRAINING -> INACTIVE
                 \-> RESET
```

Provider Path states:

```text
ABSENT -> AVAILABLE -> DEGRADED -> DRAINING -> ABSENT
```

P-0AP does not simulate an unauthenticated Path: a Provider Path is announced only after the control model supplies a valid authenticated Node identity.

Rules:

- activation returns an atomic initial Path snapshot and continuation sequence;
- `provider-path-added` follows identity validation;
- address rotation, identity replacement, characteristic change, and Obfuscated-degree change increment Provider Path revision;
- restoration after removal uses a non-reused Path identifier within the generation;
- every accepted Provider Submission has exactly one terminal result;
- no conforming SDU reception occurs after final Path removal;
- reset emits `PROVIDER_RESET` completions before the final reset event;
- orderly deactivation drains or terminally resolves accepted work;
- self-Paths are rejected and never announced.
