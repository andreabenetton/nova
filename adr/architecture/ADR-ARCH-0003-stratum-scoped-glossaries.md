---
adr: ADR-ARCH-0003
title: Scope terminology by stratum
scope: architecture
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents:
  - canon/glossary.md
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-ARCH-0003: Scope terminology by stratum

## Context

The original unified glossary mixed P-Stratum and R-Stratum concepts. That encouraged definitions such as a P-Stratum Path being described directly as an R-Stratum Edge outside the P–R Interface specification.

## Decision

Each stratum owns a separate glossary. The common glossary contains only stratum-independent terms. Cross-stratum semantic mappings are defined exclusively by the corresponding versioned Interface documentation.

CI checks stratum documentation for obvious use of foreign canonical terminology. Scoped agent instructions identify the permitted glossary set.

## Architectural boundaries

- Owned by: `canon/glossary.md` as the index, with each stratum owning its own glossary.
- Consumed through: the Interface glossaries under `contracts/interfaces/`, which are the only place a cross-stratum mapping may appear.
- Must not depend on: a unified glossary or any definition that spans strata outside an Interface document.
- Information allowed to cross the boundary: term mappings stated by a versioned Interface.
- Information prohibited from crossing the boundary: a stratum-owned term used to define a term owned by another stratum.

## Interface and contract impact

No contract version changes. Interface documentation becomes the only authoritative location for cross-stratum term mappings.

## Security and privacy impact

none directly. Consistent terminology reduces the chance that a privacy-relevant term such as Obfuscated degree is redefined outside the Interface that owns its meaning.

## Alternatives considered

- Keep one unified glossary and rely on review to catch cross-stratum definitions. Rejected: the unified glossary is what produced the drift.
- Scope glossaries by document rather than by stratum. Rejected: ownership would follow file layout rather than architecture.

## Consequences

- Strict layering is reflected in documentation and LLM context boundaries.
- Interface documents become the only authoritative place for cross-stratum mappings.
- Some existing documents and filenames must be renamed or rewritten.
- Lexical CI checks supplement but do not replace architectural review.

## Validation and conformance

`tools/check_terminology.py`, run through `make terminology`, checks stratum documentation for foreign canonical terminology. Scoped agent instructions declare the permitted glossary set for each tree.

## Migration and rollback

Existing documents and filenames that mixed strata were renamed or rewritten as the scoped glossaries were introduced. Rollback would require restoring a unified glossary and is not planned.

## Unresolved questions

The lexical check matches obvious term usage only. Whether a stronger structural check is warranted remains open.
