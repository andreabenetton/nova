# Obfuscated degree and neighbor expansion

The P-R Interface includes Obfuscated degree in the base contract.

For an Edge to Peer `n`, the value means:

> the number of neighbor-expansion slots R-Stratum should prepare when beginning local topology discovery through `n`.

It does not mean:

- the exact number of P-Stratum Paths;
- the exact number of Edges visible to the Peer;
- the exact physical or routed degree of the Peer;
- a verified claim about the whole topology.

P-Stratum derives the value from the remote Peer notification, its knowledge of common Peers, and the selected obfuscation profile. In the model inherited from the P-Stratum design, zero means that no additional expansion slot is required; otherwise the value may include positive noise after excluding known common Peers.

Dummy expansion slots must be handled without becoming an error oracle. R-Stratum allocates and processes the advertised number of slots but must not infer that every slot corresponds to a real Edge.

`InterfaceOpened` declares every profile identifier that can appear and its maximum value. All profiles preserve the same expansion-cardinality meaning; the consumer need not know the profile algorithm. A profile change or value change produces `edge-updated` and increments `EdgeRevision`.

A fresh value is mandatory at `edge-added`. P-Stratum should refresh it before expiry. When it becomes stale, the Edge remains usable for SDU transport, but R-Stratum must not begin new topology expansion through that hint.

The base Interface freezes:

- field presence;
- integer range and profile-specific maximum;
- expansion-cardinality meaning;
- zero-value meaning;
- profile identification;
- freshness and update behavior.

It deliberately does not freeze the noise distribution, private common-Peer detection protocol, or profile algorithm. Those are versioned below the boundary.
