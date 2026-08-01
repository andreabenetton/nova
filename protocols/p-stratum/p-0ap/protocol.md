
# P-0AP protocol model

P-0AP has no interoperable network wire format. Its normative behavior is the combination of:

- `NOVA-IF-P-PATH-PROVIDER`;
- `NOVA-IF-P-0AP-CONTROL`;
- `NOVA-IF-VIRTUAL-FABRIC` when the Virtual Fabric is used;
- the semantics and deterministic rules in this directory.

A conforming P-0AP implementation must support at least paired-node mode and deterministic Path lifecycle. Loopback, virtual-fabric, replay, and adversarial provider modes are separately declared capabilities.

P-0AP must preserve the distinction between:

- the Node identity used by Nova;
- the provider-local endpoint used by the Virtual Fabric;
- the provider-local Path identifier;
- the P-Stratum Path identifier assigned by P-Stratum common.
