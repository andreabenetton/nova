
# P-0AP control Interface

`NOVA-IF-P-0AP-CONTROL` is a test-only, versioned Interface between a Simulation controller and P-0AP.

It is used to:

- create and remove simulated Nodes;
- create, update, remove, partition, and restore modeled Paths;
- load profiles and scenarios;
- advance virtual time and run until idle;
- start recording and replay traces;
- select conforming or explicitly adversarial provider behavior.

The control Interface must never be forwarded through `NOVA-IF-P-R` or treated as a Nova peer protocol.
