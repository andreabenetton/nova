# P-Stratum Path model

A Path has:

- PathId, unique within one P-Stratum interface instance;
- PeerId;
- PathKind: `LINK_ADJACENT` or `REMOTE_ASSOCIATION`;
- lifecycle generation;
- maximum SDU size;
- supported delivery classes;
- abstract latency, jitter, rate, and availability characteristics when known;
- provider-local opaque identifier.

R-Stratum must not receive an Adapter identifier, Binding identifier, MAC address, IP address, port, QUIC connection identifier, or other integration detail.
