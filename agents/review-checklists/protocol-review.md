<!-- SPDX-License-Identifier: Apache-2.0 -->

# Peer-protocol review checklist

- Version negotiation and downgrade behavior are specified.
- State machine and timeouts are complete.
- Wire fields, widths, byte order, limits, and cryptographic coverage are exact.
- Nonce, key epoch, replay, crash recovery, and rekey rules are exact.
- Positive and negative vectors exist.
- Resource limits and malformed-input behavior exist.
- The protocol consumes only declared lower interfaces.
