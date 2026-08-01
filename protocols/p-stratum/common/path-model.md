# P-Stratum Path model

A Path has:

- PathId, unique within one P-Stratum Interface instance;
- PeerId;
- PathKind: `LINK_ADJACENT` or `REMOTE_ASSOCIATION`;
- lifecycle generation;
- maximum SDU size;
- supported delivery classes;
- abstract latency, jitter, rate, and availability characteristics when known;
- provider-local opaque identifier.

R-Stratum must not receive a Path Provider identifier, Adapter identifier, Binding identifier, MAC address, IP address, port, QUIC connection identifier, Virtual Fabric endpoint, simulation seed, or other integration detail.

P-0AP does not introduce a third PathKind. Each P-0AP Path declares which existing PathKind it models. This permits R-Stratum to test behavior for link-adjacent and remote-association Edges without learning that the Path is simulated.

A literal P-0AP self-loop is a diagnostic transport path. It must not normally be mapped to an R-Stratum Edge because a Node is not a Close of itself.
