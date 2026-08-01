<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# O-Stratum

O-Stratum consumes `NOVA-IF-R-O` and provides `NOVA-IF-O-A`. It should eventually provide at least:

- a connectionless message-oriented protocol;
- a reliable connection-oriented protocol.

IP-over-Nova should initially use the connectionless message-oriented service to avoid stacking reliable inner TCP over another mandatory reliable transport.
