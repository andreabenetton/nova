# P-Stratum common security invariants

- A Path is not exposed before the relevant peer identity and Path state meet the provider contract.
- Path identifiers are not reused without a new generation after removal.
- Received SDUs are attributed to exactly one Peer and Path.
- Provider-specific locators are not exposed through the P-R Interface.
- Failure of one Path Provider does not authorize another provider to assume its Path identity.
