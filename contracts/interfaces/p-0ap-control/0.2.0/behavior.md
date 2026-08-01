# Behavior

Distinct simulated Nodes have distinct authenticated Node identities. Paired-node mode is the normal minimum topology. Self-loop mode is diagnostic and cannot request an R-Stratum Edge.

`create-path` creates a simulated Provider Path between two distinct Nodes and supplies private Provider Path properties. `set-obfuscated-degree` controls the expansion-cardinality hint that P-0AP supplies through the Path Provider Interface. It does not set an exact topology fact.

All limits are finite. Scenario, seed, virtual clock, scheduler algorithm, tie-breaking policy, and implementation version are recorded for reproducibility. Conforming mode may model loss, failure, backpressure, and reset, but may not deliver corrupted or contract-invalid P-R behavior.
