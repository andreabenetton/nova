# P-LAP protocol stub

## Required responsibilities

- discover Adapter-local candidate peers;
- bind a Nova Node identity to a Nexus locator through an authenticated transcript;
- establish protected peer state;
- create and remove link-adjacent Paths;
- preserve submitted SDU boundaries;
- fragment and reassemble according to Adapter-reported limits;
- provide replay protection and bounded resource use;
- report abstract Path characteristics;
- optionally support negotiated delivery and privacy profiles.

## Explicitly deferred from the first profile

- mandatory constant-rate transmission;
- chaff;
- private common-peer detection;
- obfuscated degree notification;
- proof-of-work admission;
- multipath aggregation.

These features require separate specifications and threat models.
