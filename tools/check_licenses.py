# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import fnmatch
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "legal" / "license-policy.yaml"
HEADER_TOKEN = "SPDX-License-Identifier:"
COMMENTABLE_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".toml", ".rs"}
COMMENTABLE_NAMES = {"Makefile", ".editorconfig", ".gitattributes", ".gitignore"}
NONCOMMENTABLE_SUFFIXES = {".json", ".pdf"}
IGNORED_PARTS = {".git", "__pycache__", "target", ".cache", ".pytest_cache", ".mypy_cache"}


def load_policy() -> dict[str, Any]:
    return yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))


def posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def matches(pattern: str, path: str) -> bool:
    return fnmatch.fnmatchcase(path, pattern)


def rule_for(policy: dict[str, Any], rel: str) -> dict[str, Any] | None:
    for rule in policy["rules"]:
        if matches(rule["pattern"], rel):
            return rule
    return None


def is_exempt(policy: dict[str, Any], rel: str) -> bool:
    return any(matches(pattern, rel) for pattern in policy.get("exempt_files", []))


def tracked_files() -> list[Path]:
    # -z keeps paths verbatim; without it Git C-quotes non-ASCII names and any
    # name containing a newline. --cached also still reports a file deleted in
    # the worktree but not staged, so those are dropped as well.
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    )
    return [
        ROOT / line for line in output.split("\0") if line and (ROOT / line).exists()
    ]


def repository_directories() -> list[Path]:
    # Derived from the Git file listing rather than a filesystem walk, so that a
    # directory holding only ignored files is not required to carry a marker.
    # Agent tooling writes such files, and requiring a marker for them would fail
    # on some clones and not others.
    result: set[Path] = set()
    for path in tracked_files():
        for parent in path.parents:
            if parent == ROOT:
                break
            if any(part in IGNORED_PARTS for part in parent.relative_to(ROOT).parts):
                break
            result.add(parent)
    return [ROOT, *sorted(result)]


def expected_header(rule: dict[str, Any]) -> str:
    return f"{HEADER_TOKEN} {rule['license']}"


def header_required(rule: dict[str, Any], path: Path) -> bool:
    if rule.get("spdx_header") is False:
        return False
    if path.suffix in NONCOMMENTABLE_SUFFIXES:
        return False
    return path.suffix in COMMENTABLE_SUFFIXES or path.name in COMMENTABLE_NAMES


def read_head(path: Path, lines: int = 40) -> str:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return "".join(handle.readline() for _ in range(lines))
    except (UnicodeDecodeError, OSError):
        return ""


def check_crate_licenses(policy: dict[str, Any], errors: list[str]) -> None:
    expected: dict[str, str] = {}
    for name in policy["agpl_core_crates"]:
        expected[name] = "AGPL-3.0-or-later"
    for name in policy["apache_integration_and_sdk_crates"]:
        if name in expected:
            errors.append(f"crate listed in both AGPL and Apache groups: {name}")
        expected[name] = "Apache-2.0"

    crates = ROOT / "implementations" / "rust" / "crates"
    seen: set[str] = set()
    for manifest in sorted(crates.glob("*/Cargo.toml")):
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
        package = data.get("package", {})
        name = package.get("name")
        license_value = package.get("license")
        if not isinstance(name, str):
            errors.append(f"missing package.name: {posix(manifest)}")
            continue
        seen.add(name)
        want = expected.get(name)
        if want is None:
            errors.append(f"crate missing from license policy groups: {name}")
        elif license_value != want:
            errors.append(
                f"crate {name} has license {license_value!r}, expected {want!r}"
            )
    for missing in sorted(set(expected) - seen):
        errors.append(f"license policy names absent crate: {missing}")


def main() -> int:
    policy = load_policy()
    errors: list[str] = []

    for license_id, metadata in policy["licenses"].items():
        paths = [metadata["text"]] if "text" in metadata else metadata.get("texts", [])
        for rel in paths:
            if not (ROOT / rel).is_file():
                errors.append(f"missing license text for {license_id}: {rel}")

    files = tracked_files()
    for path in files:
        rel = posix(path)
        if any(part in IGNORED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if is_exempt(policy, rel):
            continue
        rule = rule_for(policy, rel)
        if rule is None:
            errors.append(f"unclassified file: {rel}")
            continue
        head = read_head(path)
        found = [line.strip(" #/<!->\t\r\n") for line in head.splitlines() if HEADER_TOKEN in line]
        expected = expected_header(rule)
        if header_required(rule, path):
            if expected not in found:
                errors.append(f"missing or incorrect SPDX header in {rel}; expected {expected}")
        elif found and expected not in found:
            errors.append(f"conflicting SPDX header in {rel}; expected {expected}")

    classified: list[tuple[Path, str]] = []
    for path in files:
        rel = posix(path)
        if is_exempt(policy, rel):
            continue
        rule = rule_for(policy, rel)
        if rule is not None:
            classified.append((path, rule["license"]))

    for directory in repository_directories():
        marker = directory / "LICENSE.md"
        display = posix(directory) if directory != ROOT else "."
        if not marker.is_file():
            errors.append(f"directory lacks LICENSE.md marker: {display}")
            continue
        if directory.name == "LICENSES":
            continue
        text = marker.read_text(encoding="utf-8")
        direct = sorted({license_id for path, license_id in classified if path.parent == directory})
        descendants = sorted({license_id for path, license_id in classified if directory in path.parents})
        expected_ids = direct or descendants
        for license_id in expected_ids:
            if f"`{license_id}`" not in text:
                errors.append(
                    f"directory marker {display}/LICENSE.md does not mention {license_id}"
                )

    check_crate_licenses(policy, errors)

    if errors:
        print("license policy check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"license policy check passed: {len(files)} files classified, "
        f"{len(repository_directories())} directory markers present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
