<!-- SPDX-License-Identifier: Apache-2.0 -->

# Security review checklist

- Attacker classes are stated.
- Every claim has a scope and failure condition.
- Identity, locator, and channel binding are distinguished.
- Downgrade, replay, amplification, and state exhaustion are covered.
- Metadata visible to the underlay is documented.
- Cryptographic agility does not create silent downgrade.
- Negative and adversarial tests map to invariants.
