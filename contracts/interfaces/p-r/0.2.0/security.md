# Security contract

At `edge-added`, P-Stratum promises:

- the Peer Node identity has been cryptographically authenticated;
- every advertised Node address is cryptographically bound to that identity;
- P-Stratum traffic between the local Node and Peer is confidential and integrity protected;
- replay protection is active for the Edge incarnation;
- only complete authenticated SDUs are delivered upward;
- duplicate delivery is suppressed according to the selected service profile.

The Interface does not promise that:

- the authenticated Peer behaves honestly;
- Peer R-Stratum accepts or processes an SDU;
- a final Receiver is reached;
- traffic analysis is impossible;
- a remotely supplied metric or Obfuscated degree is truthful beyond its declared provenance and profile semantics.

P-0AP conforming mode models corruption below P-Stratum as loss, failure, or a terminal Submission result. It must not deliver silently corrupted bytes as a conforming P-R event.
