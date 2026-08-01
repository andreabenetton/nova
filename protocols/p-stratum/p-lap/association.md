<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-LAP association stub

The first profile should use an exact Noise pattern and suite after a separate cryptographic ADR. The authenticated transcript must bind:

- P-LAP version;
- local and remote Nova identities;
- Adapter type and relevant locator claims;
- negotiated capabilities;
- anti-downgrade values;
- session and key-epoch identifiers.

An unauthenticated discovery message may be used as a hint, but a Path must not be exposed until identity and locator binding are authenticated.
