# ADR index

Generated from the ADR front matter. Do not edit manually.

Identifiers are allocated per scope and are never reused. A record's
status lives in its front matter rather than in its path.

## architecture (`ADR-ARCH-`, `adr/architecture/`)

| Identifier | Title | Status | Date | Source |
|---|---|---|---|---|
| ADR-ARCH-0001 | Strict strata and versioned boundaries | proposed | 2026-08-01 | [adr/architecture/ADR-ARCH-0001-strict-strata-and-versioned-boundaries.md](../../adr/architecture/ADR-ARCH-0001-strict-strata-and-versioned-boundaries.md) |
| ADR-ARCH-0002 | Version all replaceable boundaries | proposed | 2026-08-01 | [adr/architecture/ADR-ARCH-0002-version-all-replaceable-boundaries.md](../../adr/architecture/ADR-ARCH-0002-version-all-replaceable-boundaries.md) |
| ADR-ARCH-0003 | Scope terminology by stratum | proposed | 2026-08-01 | [adr/architecture/ADR-ARCH-0003-stratum-scoped-glossaries.md](../../adr/architecture/ADR-ARCH-0003-stratum-scoped-glossaries.md) |

## p-r-interface (`ADR-PR-`, `adr/interfaces/p-r/`)

| Identifier | Title | Status | Date | Source |
|---|---|---|---|---|
| ADR-PR-0001 | Expose aggregated Edges rather than Paths through P-R | proposed | 2026-08-01 | [adr/interfaces/p-r/ADR-PR-0001-p-r-exposes-aggregated-edges.md](../../adr/interfaces/p-r/ADR-PR-0001-p-r-exposes-aggregated-edges.md) |
| ADR-PR-0002 | Include Obfuscated degree in the base P-R Interface | proposed | 2026-08-01 | [adr/interfaces/p-r/ADR-PR-0002-obfuscated-degree-in-base-p-r-interface.md](../../adr/interfaces/p-r/ADR-PR-0002-obfuscated-degree-in-base-p-r-interface.md) |
| ADR-PR-0003 | Use an atomic reliable SDU baseline with explicit lifecycle | proposed | 2026-08-01 | [adr/interfaces/p-r/ADR-PR-0003-p-r-atomic-reliable-sdu-lifecycle.md](../../adr/interfaces/p-r/ADR-PR-0003-p-r-atomic-reliable-sdu-lifecycle.md) |

## r-o-interface (`ADR-RO-`, `adr/interfaces/r-o/`)

No records.

## p-stratum (`ADR-P-`, `adr/p-stratum/`)

| Identifier | Title | Status | Date | Source |
|---|---|---|---|---|
| ADR-P-0001 | Split P-Stratum into P-LAP and P-RAP | proposed | 2026-08-01 | [adr/p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md](../../adr/p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md) |
| ADR-P-0002 | Adapters and Bindings are distinct extension points | proposed | 2026-08-01 | [adr/p-stratum/ADR-P-0002-adapters-and-bindings-are-distinct.md](../../adr/p-stratum/ADR-P-0002-adapters-and-bindings-are-distinct.md) |
| ADR-P-0003 | Sequence QUIC before Ethernet while developing R-Stratum in parallel | proposed | 2026-08-01 | [adr/p-stratum/ADR-P-0003-sequence-quic-before-ethernet.md](../../adr/p-stratum/ADR-P-0003-sequence-quic-before-ethernet.md) |
| ADR-P-0004 | Classify P-0AP, P-LAP, and P-RAP as Path Provider protocols | proposed | 2026-08-01 | [adr/p-stratum/ADR-P-0004-path-provider-protocols-and-p-stratum-objectives.md](../../adr/p-stratum/ADR-P-0004-path-provider-protocols-and-p-stratum-objectives.md) |

## p-0ap (`ADR-P0AP-`, `adr/p-stratum/p-0ap/`)

| Identifier | Title | Status | Date | Source |
|---|---|---|---|---|
| ADR-P0AP-0001 | Add P-0AP and a deterministic Virtual Fabric | proposed | 2026-08-01 | [adr/p-stratum/p-0ap/ADR-P0AP-0001-p-0ap-and-deterministic-virtual-fabric.md](../../adr/p-stratum/p-0ap/ADR-P0AP-0001-p-0ap-and-deterministic-virtual-fabric.md) |

## p-lap (`ADR-PLAP-`, `adr/p-stratum/p-lap/`)

No records.

## p-rap (`ADR-PRAP-`, `adr/p-stratum/p-rap/`)

| Identifier | Title | Status | Date | Source |
|---|---|---|---|---|
| ADR-PRAP-0001 | QUIC carriage profile | proposed | 2026-08-01 | [adr/p-stratum/p-rap/ADR-PRAP-0001-quic-control-stream-and-datagram-profile.md](../../adr/p-stratum/p-rap/ADR-PRAP-0001-quic-control-stream-and-datagram-profile.md) |
| ADR-PRAP-0002 | P-RAP Association is independent from Binding instance | proposed | 2026-08-01 | [adr/p-stratum/p-rap/ADR-PRAP-0002-prap-association-independent-from-binding-instance.md](../../adr/p-stratum/p-rap/ADR-PRAP-0002-prap-association-independent-from-binding-instance.md) |

## r-stratum (`ADR-R-`, `adr/r-stratum/`)

No records.

## o-stratum (`ADR-O-`, `adr/o-stratum/`)

| Identifier | Title | Status | Date | Source |
|---|---|---|---|---|
| ADR-O-0001 | IP-over-Nova is an O-Stratum Compatibility Service | proposed | 2026-08-01 | [adr/o-stratum/ADR-O-0001-ip-over-nova-is-an-o-stratum-compatibility-service.md](../../adr/o-stratum/ADR-O-0001-ip-over-nova-is-an-o-stratum-compatibility-service.md) |

## security (`ADR-SEC-`, `adr/security/`)

No records.

## implementation (`ADR-IMPL-`, `adr/implementation/`)

No records.

## repository (`ADR-REPO-`, `adr/repository/`)

| Identifier | Title | Status | Date | Source |
|---|---|---|---|---|
| ADR-REPO-0001 | NIDL representation | proposed | 2026-08-01 | [adr/repository/ADR-REPO-0001-nidl-yaml-json-schema-canonical-json.md](../../adr/repository/ADR-REPO-0001-nidl-yaml-json-schema-canonical-json.md) |
| ADR-REPO-0002 | Original papers are non-normative research inputs | proposed | 2026-08-01 | [adr/repository/ADR-REPO-0002-original-papers-are-non-normative.md](../../adr/repository/ADR-REPO-0002-original-papers-are-non-normative.md) |
| ADR-REPO-0003 | LLM context manifests and knowledge firewalls | proposed | 2026-08-01 | [adr/repository/ADR-REPO-0003-llm-context-manifests-and-knowledge-firewalls.md](../../adr/repository/ADR-REPO-0003-llm-context-manifests-and-knowledge-firewalls.md) |
| ADR-REPO-0004 | Generated artifacts are not authoritative | proposed | 2026-08-01 | [adr/repository/ADR-REPO-0004-generated-contract-artifacts-are-not-authoritative.md](../../adr/repository/ADR-REPO-0004-generated-contract-artifacts-are-not-authoritative.md) |
| ADR-REPO-0005 | AGENTS.md is the canonical agent instruction source | proposed | 2026-08-01 | [adr/repository/ADR-REPO-0005-agents-md-is-the-canonical-agent-instruction-source.md](../../adr/repository/ADR-REPO-0005-agents-md-is-the-canonical-agent-instruction-source.md) |
| ADR-REPO-0006 | Split core and integration licensing | proposed | 2026-08-01 | [adr/repository/ADR-REPO-0006-split-core-and-integration-licensing.md](../../adr/repository/ADR-REPO-0006-split-core-and-integration-licensing.md) |
