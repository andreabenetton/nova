# P-RAP protocol stub

P-RAP common behavior shall define:

- remote Association establishment;
- Nova identity authentication;
- Association identifiers and generations;
- capability and version negotiation;
- Binding attachment and replacement;
- protected P-RAP unit semantics where required independently of the Binding;
- liveness and Association failure;
- delivery of submitted SDUs;
- creation and removal of remote-association Paths.

P-RAP must not assume UDP, TCP, QUIC, IPv4, or IPv6 behavior. It consumes declared Binding properties.
