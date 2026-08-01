# P-Stratum common security invariants

- A Path is not exposed before the relevant Peer identity and Path state meet the Path Provider contract.
- Path identifiers are not reused without a new generation after removal.
- Received SDUs are attributed to exactly one Peer and Path.
- Provider-specific locators and simulation identifiers are not exposed through the P-R Interface.
- Failure of one Path Provider does not authorize another provider to assume its Path identity.
- P-0AP must identify whether it is operating in conforming or explicitly adversarial provider mode.
- P-0AP test results do not establish P-LAP cryptographic, Ethernet, P-RAP, IP, or QUIC security properties.
