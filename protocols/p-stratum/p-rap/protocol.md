<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-RAP protocol stub

P-RAP common behavior shall define:

- remote Association establishment;
- Nova Node identity authentication;
- Association identifiers and generations;
- capability and version negotiation;
- Binding attachment and replacement;
- protected P-RAP unit semantics where required independently of the Binding;
- liveness and Association failure;
- complete SDU submission and terminal results;
- finite queues and capacity recovery;
- creation and removal of Provider Paths;
- production and update of the Path Provider Obfuscated-degree hint.

P-RAP must not assume UDP, TCP, QUIC, IPv4, or IPv6 behavior. It consumes declared Binding properties. The first QUIC implementation must not leak QUIC ordering, connection identity, or locator semantics into P-R or the common Path model.
