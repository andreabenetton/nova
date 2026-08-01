# P-RAP Association

A P-RAP Association is identified by Nova identities and P-RAP state. It is not the same as:

- an IP five-tuple;
- a socket;
- a TCP connection;
- a QUIC connection;
- a Binding instance.

The first prototype may bind Nova identities to a QUIC channel using an exporter or equivalent channel-binding value. Binding-independent session keys and cross-Binding migration may be deferred, but the API must not make them impossible.
