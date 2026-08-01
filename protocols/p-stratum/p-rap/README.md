# P-RAP

The P-Stratum Remote Association Protocol establishes protected Paths with remote Nova Nodes through an already routed underlay. It uses Bindings through `NOVA-IF-P-RAP-BINDING` and supplies Paths through `NOVA-IF-P-PATH-PROVIDER`.

P-RAP behavior is transport-independent at its common boundary. Binding-specific behavior belongs under `integrations/p-rap-bindings/`.
