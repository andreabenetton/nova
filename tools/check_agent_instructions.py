#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the repository's portable coding-agent instruction hierarchy."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "generated",
    "node_modules",
    "out",
    "target",
    "vendor",
    "venv",
}
CLAUDE_IMPORT = "@AGENTS.md"
CANONICAL_NOTICE = "AGENTS.md"


@dataclass(frozen=True)
class Finding:
    level: str
    path: Path
    message: str


def is_ignored(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return True
    return any(part in IGNORED_DIRECTORIES for part in relative.parts)


def repository_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and not is_ignored(path))


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def meaningful_lines(text: str, *, drop_claude_import: bool = False) -> set[str]:
    lines: set[str] = set()
    in_fence = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith("<!--"):
            continue
        if drop_claude_import and stripped == CLAUDE_IMPORT:
            continue
        if stripped.startswith("#"):
            continue
        normalized = re.sub(r"^[-*+]|^\d+[.)]", "", stripped).strip()
        normalized = re.sub(r"\s+", " ", normalized).casefold()
        if len(normalized) >= 20:
            lines.add(normalized)
    return lines


def nearest_agents(path: Path, agents_files: set[Path]) -> Path | None:
    directory = path.parent
    while directory == ROOT or ROOT in directory.parents:
        candidate = directory / "AGENTS.md"
        if candidate in agents_files:
            return candidate
        if directory == ROOT:
            break
        directory = directory.parent
    return None


def is_vendor_instruction_file(path: Path) -> bool:
    rel = relative(path)
    posix = rel.as_posix()
    if path.name == "GEMINI.md":
        return True
    if posix == ".github/copilot-instructions.md":
        return True
    if ".cursor/rules" in posix:
        return True
    if path.name == ".clinerules" or ".clinerules/" in posix:
        return True
    if ".windsurf/rules" in posix:
        return True
    if ".devin/rules" in posix:
        return True
    return False


def duplicate_lines(source: Path, candidate: Path) -> set[str]:
    source_lines = meaningful_lines(read_text(source))
    candidate_lines = meaningful_lines(read_text(candidate), drop_claude_import=True)
    return source_lines & candidate_lines


def check_claude_adapters(agents: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for agents_path in agents:
        claude_path = agents_path.with_name("CLAUDE.md")
        if not claude_path.exists():
            findings.append(Finding("error", claude_path, f"missing sibling adapter for {relative(agents_path)}"))
            continue

        text = read_text(claude_path)
        nonempty = [line.strip() for line in text.splitlines() if line.strip()]
        if CLAUDE_IMPORT not in nonempty:
            findings.append(Finding("error", claude_path, "must contain a standalone @AGENTS.md import"))
            continue

        extra = [line for line in nonempty if line != CLAUDE_IMPORT]
        if not extra:
            findings.append(Finding("managed", claude_path, "minimal Claude adapter"))
            continue

        overlaps = duplicate_lines(agents_path, claude_path)
        if overlaps:
            sample = sorted(overlaps)[0]
            findings.append(
                Finding(
                    "error",
                    claude_path,
                    f"appears to copy shared instructions from {relative(agents_path)}: {sample!r}",
                )
            )
        else:
            findings.append(Finding("specific", claude_path, "contains Claude-specific extensions after @AGENTS.md"))
    return findings


def check_gemini() -> list[Finding]:
    path = ROOT / ".gemini" / "settings.json"
    if not path.exists():
        return [Finding("error", path, "missing Gemini CLI configuration")]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [Finding("error", path, f"invalid JSON: {exc}")]

    file_names = data.get("context", {}).get("fileName")
    if not isinstance(file_names, list) or not all(isinstance(item, str) for item in file_names):
        return [Finding("error", path, "context.fileName must be an array of strings")]
    if "AGENTS.md" not in file_names:
        return [Finding("error", path, "context.fileName must include AGENTS.md")]
    if file_names[0] != "AGENTS.md":
        return [Finding("error", path, "AGENTS.md must be the first context filename")]
    return [Finding("managed", path, "Gemini CLI loads AGENTS.md first")]


def check_vendor_files(files: list[Path], agents: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    agents_set = set(agents)
    for path in files:
        if path.name == "CLAUDE.md" or not is_vendor_instruction_file(path):
            continue
        text = read_text(path)
        source = nearest_agents(path, agents_set)
        overlaps = duplicate_lines(source, path) if source is not None else set()
        if overlaps:
            findings.append(
                Finding(
                    "error",
                    path,
                    f"duplicates shared instructions from {relative(source)}; keep shared rules in AGENTS.md",
                )
            )
            continue
        if CANONICAL_NOTICE not in text:
            findings.append(
                Finding(
                    "warning",
                    path,
                    "vendor-specific instruction file does not state that shared rules remain in AGENTS.md",
                )
            )
        else:
            findings.append(Finding("specific", path, "vendor-specific instruction file preserved without copied rules"))
    return findings


def main() -> int:
    files = repository_files()
    agents = [path for path in files if path.name == "AGENTS.md"]
    findings: list[Finding] = []

    if not agents:
        findings.append(Finding("error", ROOT / "AGENTS.md", "no AGENTS.md files found"))
    else:
        findings.extend(check_claude_adapters(agents))
    findings.extend(check_gemini())
    findings.extend(check_vendor_files(files, agents))

    order = {"error": 0, "warning": 1, "specific": 2, "managed": 3}
    for finding in sorted(findings, key=lambda item: (order[item.level], str(item.path))):
        print(f"[{finding.level}] {relative(finding.path)}: {finding.message}")

    errors = [finding for finding in findings if finding.level == "error"]
    warnings = [finding for finding in findings if finding.level == "warning"]
    if errors:
        print(f"agent instruction check failed: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1

    print(
        f"agent instruction check passed: {len(agents)} AGENTS.md file(s), "
        f"{len(warnings)} warning(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
