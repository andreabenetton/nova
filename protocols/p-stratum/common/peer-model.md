# Peer and Edge model

A Peer is an authenticated Nova Node reachable through one or more usable P-Stratum Paths. P-Stratum common groups Paths exclusively by `NodeIdentityId`, never by locator, address-set equality, or provider-local identifier.

`PeerHandle` is assigned to that identity and remains stable for the P-R Interface instance. Valid Node-address growth or rotation updates the same Peer. A different identity identifier creates a different Peer and handle.

An Edge is the one R-Stratum-visible relationship to that Peer.

- the first usable Path capable of at least one compliant service profile creates the Edge;
- later Paths or identity-address updates change its snapshot and revision;
- removing one Path does not remove the Edge while another compliant Path or profile remains;
- removing the last usable Path removes the Edge after accepted Submissions reach terminal results;
- later reachability creates a new Edge incarnation and `EdgeId`, while the same Peer may retain its `PeerHandle`.

Runtime handles are local to one P-R Interface instance. Distinct simulated Nodes in P-0AP must have distinct identity identifiers even if hosted by one process.
