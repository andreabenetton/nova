<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Repository map

| Area | Authority | Purpose |
|---|---|---|
| `canon/` | normative | Shared glossary, architecture, invariants, security model, versioning, registries, dependency policy. |
| `contracts/` | normative | Versioned NIDL contracts, including P-R Edge semantics, Path Provider behavior, Obfuscated degree, schemas, implementation declarations, locks, canonical generated JSON, and conformance scenarios. |
| `protocols/` | normative drafts | Peer behavior inside P-Stratum, R-Stratum, and O-Stratum, including P-0AP, P-LAP, and P-RAP. |
| `integrations/` | normative drafts | P-LAP Adapters and P-RAP Bindings, including deterministic simulated integrations. |
| `simulation/` | normative test-model drafts | Virtual Fabric semantics, deterministic scheduler, scenario and trace schemas, profiles, and reproducible fixtures. |
| `compatibility/` | normative drafts | IP-over-Nova profiles and Platform Attachment design. |
| `implementations/` | non-normative code | Language- and platform-specific implementation skeletons. |
| `tests/` | conformance evidence | Provider, consumer, protocol, simulation, deterministic-trace, interoperability, adversarial, and performance test organization. |
| `schemas/` | normative drafts | Peer-protocol wire and vector schema locations. |
| `generated/` | derived | Reproducible generated code, documentation, mocks, harnesses, and dissector material. |
| `adr/` | decision process | Proposed, accepted, rejected, and superseded architecture decisions. |
| `agents/` | process | LLM roles, bounded context, task templates, and review checklists. |
| `docs/` | process and design navigation | Repository-wide contributor instructions plus non-normative guides linking authoritative Nova design sources. |
| `research/` | non-normative | Original papers, assessments, design notes, experiments, references, and unresolved questions. |
| `tools/` | enforcement | NIDL validation, semantic lint, compatibility guard, context, dependency, agent-instruction, and simulation-fixture checks. |
| `examples/` | non-normative | Version-pinned examples and mock topologies. |
| `fuzz/`, `benchmarks/` | evidence stubs | Security and performance work once wire formats and simulation models exist. |
