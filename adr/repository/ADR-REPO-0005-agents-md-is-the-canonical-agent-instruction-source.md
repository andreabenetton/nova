---
adr: ADR-REPO-0005
title: AGENTS.md is the canonical agent instruction source
scope: repository
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents:
  - AGENTS.md
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-REPO-0005: AGENTS.md is the canonical agent instruction source

## Context

Nova is intended for work by multiple coding agents. Duplicating shared instructions in vendor-specific files would create inconsistent scopes, stale copies, and unnecessary context.

## Decision

`AGENTS.md` shall remain the canonical, vendor-neutral instruction format. Nested `AGENTS.md` files shall scope instructions to directory trees. Claude Code shall use sibling `CLAUDE.md` adapter files that import `@AGENTS.md`, and Gemini CLI shall be configured to load `AGENTS.md`. Other vendor files shall be introduced only for requirements that cannot be expressed portably.

A deterministic repository check shall validate the adapter hierarchy and report suspicious duplicated instruction files.

## Architectural boundaries

- Owned by: the root `AGENTS.md`, with nested files owning their directory trees.
- Consumed through: sibling vendor adapters, which import rather than copy.
- Must not depend on: a vendor-specific file carrying a rule that is not in `AGENTS.md`.
- Information allowed to cross the boundary: an import of the canonical file, plus genuinely vendor-specific extensions.
- Information prohibited from crossing the boundary: a duplicated copy of a shared rule, which becomes stale silently.

## Interface and contract impact

none. No Nova protocol or NIDL Interface changes. Repository contributors follow the instruction-file validation rule.

## Security and privacy impact

Reducing duplicated instructions lowers the chance that an agent bypasses current repository constraints because it loaded a stale vendor-specific copy.

## Alternatives considered

- Copying instructions into one file per coding agent.
- Making `CLAUDE.md` or another vendor format authoritative.
- Relying only on human review to detect drift.

## Consequences

- Shared instructions have one authoritative source.
- Claude and Gemini receive small compatibility adapters.
- New scoped `AGENTS.md` files require matching Claude adapters.
- CI detects drift but does not automatically remove vendor-specific files.

## Validation and conformance

Require `tools/check_agent_instructions.py` to pass locally through `make agent-instructions` and in the existing contracts workflow.

## Migration and rollback

Existing vendor files were reduced to adapters when the rule was introduced. Rollback would mean reintroducing duplicated instructions and is not planned.

## Unresolved questions

The check detects duplicated instructions but cannot detect a vendor file that contradicts `AGENTS.md` in substance while sharing no wording.
