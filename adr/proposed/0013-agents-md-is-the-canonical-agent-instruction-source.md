# ADR-0013: AGENTS.md is the canonical agent instruction source

- Status: proposed
- Date: 2026-08-01
- Decision owners: TBD

## Context

Nova is intended for work by multiple coding agents. Duplicating shared instructions in vendor-specific files would create inconsistent scopes, stale copies, and unnecessary context.

## Decision

`AGENTS.md` shall remain the canonical, vendor-neutral instruction format. Nested `AGENTS.md` files shall scope instructions to directory trees. Claude Code shall use sibling `CLAUDE.md` adapter files that import `@AGENTS.md`, and Gemini CLI shall be configured to load `AGENTS.md`. Other vendor files shall be introduced only for requirements that cannot be expressed portably.

A deterministic repository check shall validate the adapter hierarchy and report suspicious duplicated instruction files.

## Consequences

- Shared instructions have one authoritative source.
- Claude and Gemini receive small compatibility adapters.
- New scoped `AGENTS.md` files require matching Claude adapters.
- CI detects drift but does not automatically remove vendor-specific files.

## Alternatives considered

- Copying instructions into one file per coding agent.
- Making `CLAUDE.md` or another vendor format authoritative.
- Relying only on human review to detect drift.

## Contract and migration impact

No Nova protocol or NIDL Interface changes are required. Repository contributors must follow the new instruction-file validation rule.

## Security impact

Reducing duplicated instructions lowers the chance that an agent bypasses current repository constraints because it loaded a stale vendor-specific copy.

## Validation plan

Require `tools/check_agent_instructions.py` to pass locally through `make agent-instructions` and in the existing contracts workflow.
