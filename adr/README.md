<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Architecture Decision Records

Nova ADRs record durable architectural and engineering decisions that are not fully expressed by normative specifications, contracts, or source code.

## Scope-based organization

New ADRs are organized by decision ownership rather than only by lifecycle state:

| Directory | Prefix | Scope |
|---|---|---|
| `architecture/` | `ADR-ARCH-` | Cross-stratum architecture, dependency direction, authority, and global invariants |
| `interfaces/p-r/` | `ADR-PR-` | Decisions jointly owned by the P-Stratum and R-Stratum boundary |
| `interfaces/r-o/` | `ADR-RO-` | Decisions jointly owned by the R-Stratum and O-Stratum boundary |
| `p-stratum/` | `ADR-P-` | Decisions private to P-Stratum behavior and design |
| `r-stratum/` | `ADR-R-` | Decisions private to R-Stratum behavior and design |
| `o-stratum/` | `ADR-O-` | Decisions private to O-Stratum behavior and design |
| `security/` | `ADR-SEC-` | Cross-cutting security, privacy, cryptographic, and threat-model decisions |
| `implementation/` | `ADR-IMPL-` | Non-normative implementation architecture and technology choices |
| `repository/` | `ADR-REPO-` | Repository structure, authority, generation, licensing, and engineering policy |

Interface decisions must not be placed under either adjacent stratum. An Interface is a jointly owned architectural boundary, not an implementation detail of its provider or consumer.

## Choosing a scope

Use the narrowest scope that owns the decision completely.

A decision belongs to a stratum directory only when an independent implementation can apply it using that stratum's private specification and its published Interfaces, without changing another stratum's private model.

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

The identifier in the heading, the filename, and the front matter must match. Identifiers are never reused, including after rejection or supersession. The retired global identifiers `ADR-0001` through `ADR-0020` MUST NOT appear in a record; cite the current scoped identifier instead.

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

All nine keys are required and no others are permitted. `supersedes` and `superseded_by` MUST be symmetric between the two records, and a record with a `superseded_by` entry MUST carry the `superseded` or `deprecated` status.

## Index

`generated/documentation/adr-index.md` lists every record by scope, with title, status, and date. It is generated, never hand-edited, and is the cheapest entry point when looking for the record that governs a topic.

`tools/generate_adr_index.py` regenerates it and enforces every rule on this page: scope-to-directory placement, prefix agreement, identifier uniqueness, allowed statuses, ISO dates, heading agreement, supersession symmetry, and the ban on retired identifiers. Run `make adr-index` after touching any record; it is a required CI check.

## Status

Allowed status values are:

- `proposed`
- `accepted`
- `rejected`
- `superseded`
- `deprecated`

Status is metadata, not a directory. Moving an ADR because its status changes creates unnecessary link churn. The former `accepted/`, `proposed/`, `rejected/`, and `superseded/` directories were removed once every record carried a scope; a record declares its own status.

## Existing ADRs

Every record now uses a scope directory and a scoped identifier. The original global sequence `0001`–`0020` was migrated in one pass, preserving each record's relative order within its new scope. The legacy numbers are retired and MUST NOT be reused or cited.

Migrated identifiers:

| Legacy | Current |
|---|---|
| ADR-0001, ADR-0007, ADR-0019 | ADR-ARCH-0001, ADR-ARCH-0002, ADR-ARCH-0003 |
| ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0011, ADR-0014, ADR-0020 | ADR-P-0001 through ADR-P-0007 |
| ADR-0015, ADR-0016, ADR-0017 | ADR-PR-0001, ADR-PR-0002, ADR-PR-0003 |
| ADR-0010 | ADR-O-0001 |
| ADR-0006, ADR-0008, ADR-0009, ADR-0012, ADR-0013, ADR-0018 | ADR-REPO-0001 through ADR-REPO-0006 |

## Workflow

1. Copy [`template.md`](template.md) into the correct scope directory.
2. Allocate the next unused identifier within that scope.
3. Declare affected contracts and normative documents.
4. State architectural ownership and prohibited dependencies explicitly.
5. Add validation and migration evidence appropriate to the decision.
6. Submit the ADR for review before treating it as accepted authority.

Accepted ADRs are subordinate to `canon/`, versioned `contracts/`, and stratum-owned normative protocol specifications. When an accepted ADR requires a normative change, update the authoritative artifact rather than relying on the ADR alone.
