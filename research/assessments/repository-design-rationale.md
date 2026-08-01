# Repository design rationale

Status: non-normative explanation of the scaffold.

The repository separates five knowledge classes:

1. canon shared by all contributors;
2. Interface contracts visible across replaceable boundaries;
3. peer-protocol specifications visible only to implementers of that stratum;
4. technology integrations visible only to Adapter, Binding, or Platform Attachment implementers;
5. implementation decisions visible only inside a language or platform implementation.

This structure is intended to prevent an R-Stratum implementation from learning P-LAP or P-RAP details, prevent P-RAP from depending on one QUIC library, and prevent an operating-system Compatibility Service from bypassing O-Stratum.

NIDL, contract locks, context manifests, generated mocks, dependency policy, conformance scenarios, and CI checks form a knowledge firewall for LLM-assisted work. The purpose is not to hide documentation from maintainers, but to make the minimum sufficient context explicit and testable.
