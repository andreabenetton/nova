# P-Stratum common architecture

P-Stratum common is the only component that provides `NOVA-IF-P-R`. It consumes Provider Paths through `NOVA-IF-P-PATH-PROVIDER 0.3.0` and never depends on P-0AP, P-LAP, P-RAP, Adapter, Binding, locator, or Virtual Fabric implementation details.

Its responsibilities are:

- authenticate the provenance-neutral Node identity supplied with each Provider Path;
- group all usable Paths with the same Node identity into one Peer;
- create at most one active Edge per Peer in one Interface instance;
- construct one or more abstract Edge service profiles;
- select the Provider Path or Paths used for each Submission;
- combine or select a coherent Obfuscated degree;
- own Edge revision, event sequencing, finite queues, backpressure, and Submission lifecycle;
- expose only Edge semantics through `NOVA-IF-P-R 0.2.0`.

```text
P-0AP       P-LAP       P-RAP
   \          |          /
    NOVA-IF-P-PATH-PROVIDER
                |
       P-Stratum common
   identity grouping and Path selection
   Edge profiles, queues, event sequence
                |
           NOVA-IF-P-R
                |
            R-Stratum
```
