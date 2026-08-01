<!-- SPDX-License-Identifier: Apache-2.0 OR CC-BY-4.0 -->

# Simulation schemas

`scenario.schema.json` is the current `0.2` scenario schema. It requires distinct Node identities, mandatory Expansion-cardinality hints, and Provider Paths without a Path-kind field. `scenario-0.1.schema.json` preserves the earlier experimental schema.

`profile.schema.json` validates reusable characteristic presets. `trace.schema.json` validates portable externally observable traces. These schemas are independent from NIDL because they describe test data, not architectural Interfaces.
