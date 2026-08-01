# Coding-agent instruction architecture

Nova uses `AGENTS.md` as the canonical, vendor-neutral source of coding-agent instructions. Shared repository rules belong there once; vendor-specific files may only adapt or extend those rules when a tool requires it.

## Scope

The root `AGENTS.md` applies repository-wide. A nested `AGENTS.md` adds or narrows instructions for its directory tree. An agent working in a component reads the root instructions and the nearest applicable nested instructions.

A newly added nested `AGENTS.md` normally requires a sibling `CLAUDE.md` containing only:

```markdown
@AGENTS.md
```

This import lets Claude Code consume the same scoped source without duplicating it.

```text
repository/
├── AGENTS.md
├── CLAUDE.md
├── .gemini/
│   └── settings.json
├── docs/
│   └── agent-instructions.md
└── component/
    ├── AGENTS.md
    └── CLAUDE.md
```

## Agent compatibility

- **OpenAI Codex** reads the applicable `AGENTS.md` hierarchy directly.
- **Anthropic Claude Code** reads each sibling `CLAUDE.md`, which imports `@AGENTS.md`.
- **Google Gemini CLI** is configured by `.gemini/settings.json` to load `AGENTS.md` as an instruction context filename.
- **GitHub Copilot, Cursor, Windsurf, Devin, and Cline** use `AGENTS.md` as the portable repository baseline. Add a vendor file only when a real tool-specific requirement cannot be represented in `AGENTS.md`.

Tool-specific exceptions may contain path activation metadata, IDE-only behavior, agent-specific commands, or model-specific restrictions. They must state that shared repository rules remain in `AGENTS.md` and must not copy those rules.

## Guidance and enforcement

Instruction files guide an agent. Deterministic requirements—formatting, dependency boundaries, generated-file freshness, contract compatibility, and similar invariants—must be enforced by scripts, tests, and CI.

Run the instruction consistency check with:

```sh
make agent-instructions
```

The check verifies Claude adapters, Gemini configuration, and suspicious duplicate vendor instructions. It does not delete or rewrite files.
