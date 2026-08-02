#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated" / "documentation"


def contract_index() -> str:
    rows: list[tuple[str, str, str, str, str, str]] = []
    for path in sorted((ROOT / "contracts" / "interfaces").glob("*/*/interface.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        interface = data["interface"]
        roles = data["roles"]
        rows.append(
            (
                interface["id"],
                interface["version"],
                interface["kind"],
                roles["provider"],
                roles["consumer"],
                path.relative_to(ROOT).as_posix(),
            )
        )
    lines = [
        "# Contract index",
        "",
        "Generated from NIDL sources. Do not edit manually.",
        "",
        "| Interface | Version | Kind | Provider | Consumer | Source |",
        "|---|---:|---|---|---|---|",
    ]
    lines.extend(f"| {' | '.join(row)} |" for row in rows)
    return "\n".join(lines) + "\n"


def repository_tree() -> str:
    # Derived from the Git file listing rather than a filesystem walk. Ignored
    # files such as build output and agent settings exist on some clones and
    # not others, so a walk produced a tree that depended on the clone.
    excluded_names = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "target"}
    listing = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    )
    entries: set[str] = set()
    for line in listing.splitlines():
        if not line:
            continue
        relative = Path(line)
        if any(part in excluded_names for part in relative.parts):
            continue
        entries.add(relative.as_posix())
        for parent in relative.parents:
            if parent != Path("."):
                entries.add(parent.as_posix())
    paths = ["."] + ["./" + entry for entry in sorted(entries)]
    return "\n".join(paths) + "\n"


def emit(path: Path, content: str, check: bool) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return True
    if check:
        print(f"stale generated documentation: {path.relative_to(ROOT)}", file=sys.stderr)
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"generated {path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    ok = True
    ok &= emit(GENERATED / "contracts-index.md", contract_index(), args.check)
    ok &= emit(GENERATED / "repository-tree.txt", repository_tree(), args.check)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
