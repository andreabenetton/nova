
# Virtual Fabric architecture

```text
                         Virtual Fabric engine
                    deterministic scheduler and model
                    /              |              \
                  P-0AP      Simulated Adapter  Simulated Binding
                    |              |              |
          Path Provider IF   P-LAP Adapter IF  P-RAP Binding IF
```

The engine provides endpoint registration, directed or bidirectional modeled links, unit submission, virtual-time advancement, link updates, fault injection, and trace emission.

A front end owns the translation between its Interface and Virtual Fabric units. The engine must not infer P-LAP, P-RAP, P-Stratum, or R-Stratum semantics.
