<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-LAP protocol stub

## Required responsibilities

- discover Adapter-local candidate Peers;
- bind a Nova Node identity to a Nexus locator through an authenticated transcript;
- establish protected Peer state;
- create and remove Provider Paths;
- preserve complete SDU boundaries;
- fragment and reassemble according to Adapter-reported limits;
- provide replay protection and bounded resource use;
- report abstract Path characteristics and finite queue limits;
- obtain and update the expansion-cardinality hint required by the Path Provider Interface;
- emit terminal Provider Submission results.

## Explicitly deferred from the first profile

- mandatory constant-rate transmission;
- chaff;
- a final private common-Peer detection protocol;
- proof-of-work admission;
- provider-internal multipath aggregation.

expansion cardinality is not deferred at the Interface boundary: a first implementation may use a configured or deterministic experimental profile, clearly identified as such, until the private derivation protocol is specified.
