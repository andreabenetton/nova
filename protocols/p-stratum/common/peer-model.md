# P-Stratum Peer model

A Peer is a Nova Node reachable through one or more P-Stratum Paths. Multiple Paths may reach the same Peer. P-Stratum common may expose them separately so R-Stratum can select according to abstract policy.

A P-LAP Path implies link adjacency through a Nexus Fundamenta. A P-RAP Path implies a remote P-RAP Association. A P-0AP Path models one of those two semantics for deterministic development and testing. All are one P-Stratum hop, but only a real P-LAP Path proves Nexus Fundamenta adjacency.

Paired-node and Virtual Fabric P-0AP modes must use distinct Node identities and independent state even when all Nodes execute in one process.
