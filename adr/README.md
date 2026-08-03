<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Architecture Decision Records

Nova ADRs record durable architectural and engineering decisions that are not fully expressed by normative specifications, contracts, or source code.

## Scope-based organization

ADRs are organized by decision ownership rather than by lifecycle state:

| Directory | Prefix | Scope |
|---|---|---|
| `architecture/` | `ADR-ARCH-` | Cross-stratum architecture, dependency direction, authority, and global invariants |
| `interfaces/p-r/` | `ADR-PR-` | Decisions jointly owned by the P-Stratum and R-Stratum boundary |
| `interfaces/r-o/` | `ADR-RO-` | Decisions jointly owned by the R-Stratum and O-Stratum boundary |
| `p-stratum/` | `ADR-P-` | Decisions spanning more than one P-Stratum Path Provider protocol, or owned by P-Stratum common |
| `p-stratum/p-0ap/` | `ADR-P0AP-` | Decisions private to P-0AP |
| `p-stratum/p-lap/` | `ADR-PLAP-` | Decisions private to P-LAP and its Adapter extension point |
| `p-stratum/p-rap/` | `ADR-PRAP-` | Decisions private to P-RAP, its Association semantics, and Binding carriage |
| `r-stratum/` | `ADR-R-` | Decisions private to R-Stratum behavior and design |
| `o-stratum/` | `ADR-O-` | Decisions private to O-Stratum behavior and design |
| `security/` | `ADR-SEC-` | Cross-cutting security, privacy, cryptographic, and threat-model decisions |
| `implementation/` | `ADR-IMPL-` | Non-normative implementation architecture and technology choices |
| `repository/` | `ADR-REPO-` | Repository structure, authority, generation, licensing, and engineering policy |

Interface decisions must not be placed under either adjacent stratum. An Interface is a jointly owned architectural boundary, not an implementation detail of its provider or consumer.

## Choosing a scope

Use the narrowest scope that owns the decision completely.

A decision belongs to a stratum directory only when an independent implementation can apply it using that stratum's private specification and its published Interfaces, without changing another stratum's private model.

The same test applies one level down. A decision belongs to a protocol directory only when an implementation of that Path Provider protocol alone can apply it. A decision that constrains two of P-0AP, P-LAP, and P-RAP, or that constrains P-Stratum common, stays in `p-stratum/`. The protocol directories mirror `protocols/p-stratum/`, so a contributor or agent scoped to one protocol loads only the decisions that bind it.

Use:

- `architecture/` when the decision constrains multiple strata or the whole system;
- an `interfaces/` directory when the decision changes information, behavior, errors, compatibility, or lifecycle semantics across a boundary;
- `security/` when a policy or invariant applies across multiple architectural scopes;
- `implementation/` when the choice must not become a protocol requirement;
- `repository/` when the decision governs project artifacts or engineering process.

## Identifiers and filenames

Each scope has an independent four-digit sequence:

```text
ADR-ARCH-0001-strict-stratum-dependency-direction.md
ADR-PR-0001-interface-version-negotiation.md
ADR-P-0001-path-provider-lifecycle.md
ADR-IMPL-0001-rust-workspace-boundaries.md
```

The identifier in the heading, the filename, and the front matter must match. Identifiers are never reused, including after rejection or supersession. Every citation names the full identifier, scope segment included.

## Front matter

Every record opens with YAML front matter, which is the only machine-readable declaration of its metadata:

```yaml
---
adr: ADR-P-0001
title: Split P-Stratum into P-LAP and P-RAP
scope: p-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---
```

All nine keys are required and no others are permitted. `affected_contracts` and `affected_documents` hold repository-relative paths that must exist. `supersedes` and `superseded_by` MUST be symmetric between the two records, and a record with a `superseded_by` entry MUST carry the `superseded` or `deprecated` status.

## Sections

Records use one canonical section set so that two records can be compared, and so that a reader knows an absent concern was considered rather than forgotten. Sections appear in this order:

| Section | Required |
|---|---|
| `## Context` | yes |
| `## Decision drivers` | optional |
| `## Decision` | yes |
| `## Architectural boundaries` | yes |
| `## Interface and contract impact` | yes |
| `## Wire compatibility impact` | optional |
| `## Implementation impact` | optional |
| `## Security and privacy impact` | yes |
| `## Alternatives considered` | yes |
| `## Consequences` | yes |
| `## Validation and conformance` | yes |
| `## Migration and rollback` | yes |
| `## Unresolved questions` | yes |

A required section with nothing to report says `none`; it is not dropped. No other second-level heading is permitted, no section repeats, and the order above is enforced, so a new concern becomes a template change rather than a per-record invention. Third-level headings are unconstrained.

## Index

`generated/documentation/adr-index.md` lists every record by scope, with title, status, and date. It is generated, never hand-edited, and is the cheapest entry point when looking for the record that governs a topic.

`tools/generate_adr_index.py` regenerates it and enforces every rule on this page: scope-to-directory placement, prefix agreement, identifier uniqueness, allowed statuses, ISO dates, heading agreement, supersession symmetry, the section set and its order, the existence of every affected path and that it stays inside the repository, and the requirement that a citation names the full identifier. Run `make adr-index` after touching any record; it is a required CI check.

## Status

Allowed status values are:

- `proposed`
- `accepted`
- `rejected`
- `superseded`
- `deprecated`

Status is metadata, not a directory. A record declares its own status, and moving a record because its status changed would create link churn for no gain.

## Workflow

1. Copy [`template.md`](template.md) into the correct scope directory.
2. Allocate the next unused identifier within that scope, and check the index for the highest one already taken.
3. Fill in the front matter, including affected contracts and normative documents.
4. State architectural ownership and prohibited dependencies explicitly.
5. Add validation and migration evidence appropriate to the decision.
6. Run `make adr-index` to regenerate the index and validate the record.
7. Submit the ADR for review before treating it as accepted authority.

Accepted ADRs are subordinate to `canon/`, versioned `contracts/`, and stratum-owned normative protocol specifications. When an accepted ADR requires a normative change, update the authoritative artifact rather than relying on the ADR alone.
