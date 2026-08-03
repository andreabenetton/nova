#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate ADR records and generate the ADR index.

Scope directories alone cannot answer "which record governs this topic",
and they cannot detect two sessions allocating the same identifier in
separate clones. This tool turns the rules stated in `adr/README.md` into
a check and emits the index that retrieval depends on.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_ROOT = Path(__file__).resolve().parents[1]

# Scope name -> (identifier prefix, directory relative to adr/).
SCOPES = {
    "architecture": ("ARCH", "architecture"),
    "p-r-interface": ("PR", "interfaces/p-r"),
    "r-o-interface": ("RO", "interfaces/r-o"),
    "p-stratum": ("P", "p-stratum"),
    "p-0ap": ("P0AP", "p-stratum/p-0ap"),
    "p-lap": ("PLAP", "p-stratum/p-lap"),
    "p-rap": ("PRAP", "p-stratum/p-rap"),
    "r-stratum": ("R", "r-stratum"),
    "o-stratum": ("O", "o-stratum"),
    "security": ("SEC", "security"),
    "implementation": ("IMPL", "implementation"),
    "repository": ("REPO", "repository"),
}
SCOPE_BY_PREFIX = {prefix: scope for scope, (prefix, _) in SCOPES.items()}

STATUSES = ("proposed", "accepted", "rejected", "superseded", "deprecated")
REQUIRED_KEYS = (
    "adr",
    "title",
    "scope",
    "status",
    "date",
    "supersedes",
    "superseded_by",
    "affected_contracts",
    "affected_documents",
)
LIST_KEYS = ("supersedes", "superseded_by", "affected_contracts", "affected_documents")
PATH_KEYS = ("affected_contracts", "affected_documents")

# The canonical section set, in the order records must use. A required section
# with nothing to report says `none` rather than being dropped, so an absent
# concern reads as considered rather than forgotten.
SECTIONS = (
    ("Context", True),
    ("Decision drivers", False),
    ("Decision", True),
    ("Architectural boundaries", True),
    ("Interface and contract impact", True),
    ("Wire compatibility impact", False),
    ("Implementation impact", False),
    ("Security and privacy impact", True),
    ("Alternatives considered", True),
    ("Consequences", True),
    ("Validation and conformance", True),
    ("Migration and rollback", True),
    ("Unresolved questions", True),
)
SECTION_ORDER = [name for name, _ in SECTIONS]
REQUIRED_SECTIONS = [name for name, required in SECTIONS if required]
SECTION_HEADING = re.compile(r"^## (.+)$", re.M)

# A prefix may contain digits (P0AP) but always starts with a letter, which
# keeps it distinguishable from the four-digit sequence that follows.
FILENAME = re.compile(r"^ADR-([A-Z][A-Z0-9]*)-(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
HEADING = re.compile(r"^# (ADR-[A-Z][A-Z0-9]*-\d{4}): (.+)$", re.M)
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# An unscoped citation. `ADR-ARCH-0001` does not match: the scope segment
# separates `ADR-` from the digits.
UNSCOPED_CITATION = re.compile(r"\bADR-\d{4}\b")


@dataclass(frozen=True)
class Record:
    identifier: str
    title: str
    scope: str
    status: str
    date: str
    supersedes: tuple[str, ...]
    superseded_by: tuple[str, ...]
    path: Path


def adr_paths(root: Path) -> list[Path]:
    return sorted(path for path in (root / "adr").rglob("*.md") if path.name.startswith("ADR-"))


def sort_key(record: Record) -> tuple[str, str]:
    return (record.scope, record.identifier)


def load(path: Path, root: Path, errors: list[str]) -> Record | None:
    relative = path.relative_to(root).as_posix()
    filename_match = FILENAME.match(path.name)
    if filename_match is None:
        errors.append(f"{relative}: filename must match ADR-<SCOPE>-NNNN-<slug>.md")
        return None
    prefix, number = filename_match.groups()
    if prefix not in SCOPE_BY_PREFIX:
        errors.append(f"{relative}: unknown identifier prefix {prefix!r}")
        return None
    identifier = f"ADR-{prefix}-{number}"

    text = path.read_text(encoding="utf-8")
    front_matter = FRONT_MATTER.match(text)
    if front_matter is None:
        errors.append(f"{relative}: missing YAML front matter")
        return None
    try:
        data = yaml.safe_load(front_matter.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{relative}: invalid front matter: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{relative}: front matter must be a mapping")
        return None

    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        errors.append(f"{relative}: front matter missing {', '.join(missing)}")
        return None
    unknown = sorted(set(data) - set(REQUIRED_KEYS))
    if unknown:
        errors.append(f"{relative}: unknown front matter keys {', '.join(unknown)}")
        return None

    ok = True
    if data["adr"] != identifier:
        errors.append(f"{relative}: front matter adr {data['adr']!r} does not match the filename")
        ok = False
    expected_scope = SCOPE_BY_PREFIX[prefix]
    if data["scope"] != expected_scope:
        errors.append(f"{relative}: scope {data['scope']!r} does not match prefix {prefix} ({expected_scope})")
        ok = False
    else:
        expected_directory = root / "adr" / SCOPES[expected_scope][1]
        if path.parent != expected_directory:
            errors.append(f"{relative}: scope {expected_scope!r} belongs in {expected_directory.relative_to(root).as_posix()}/")
            ok = False
    if data["status"] not in STATUSES:
        errors.append(f"{relative}: status {data['status']!r} is not one of {', '.join(STATUSES)}")
        ok = False
    # An unquoted YAML date scalar loads as datetime.date; a quoted one loads
    # as str. Accept both spellings and normalize, but reject a timestamp,
    # which datetime.datetime would otherwise smuggle in as a date subclass.
    raw_date = data["date"]
    date = ""
    if isinstance(raw_date, datetime.datetime) or not isinstance(raw_date, (datetime.date, str)):
        errors.append(f"{relative}: date must be an ISO YYYY-MM-DD value")
        ok = False
    elif isinstance(raw_date, datetime.date):
        date = raw_date.isoformat()
    elif DATE.match(raw_date):
        date = raw_date
    else:
        errors.append(f"{relative}: date must be an ISO YYYY-MM-DD value")
        ok = False
    for key in LIST_KEYS:
        value = data[key]
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{relative}: {key} must be a list of strings")
            ok = False
            continue
        if key in PATH_KEYS:
            for item in value:
                if not (root / item).exists():
                    errors.append(f"{relative}: {key} names {item}, which does not exist")
                    ok = False

    heading = HEADING.search(text)
    if heading is None:
        errors.append(f"{relative}: missing an '# ADR-<SCOPE>-NNNN: Title' heading")
        ok = False
    else:
        if heading.group(1) != identifier:
            errors.append(f"{relative}: heading identifier {heading.group(1)!r} does not match the filename")
            ok = False
        if heading.group(2) != str(data["title"]):
            errors.append(f"{relative}: heading title does not match the front matter title")
            ok = False

    body = text[front_matter.end() :]
    for citation in sorted(set(UNSCOPED_CITATION.findall(body))):
        errors.append(f"{relative}: cites {citation} without a scope; use the scoped identifier")
        ok = False

    found = SECTION_HEADING.findall(body)
    unknown_sections = [name for name in found if name not in SECTION_ORDER]
    if unknown_sections:
        errors.append(f"{relative}: unknown section(s) {', '.join(unknown_sections)}")
        ok = False
    duplicates = sorted({name for name in found if found.count(name) > 1})
    if duplicates:
        errors.append(f"{relative}: repeated section(s) {', '.join(duplicates)}")
        ok = False
    missing_sections = [name for name in REQUIRED_SECTIONS if name not in found]
    if missing_sections:
        errors.append(f"{relative}: missing required section(s) {', '.join(missing_sections)}")
        ok = False
    known = [name for name in found if name in SECTION_ORDER]
    if known != sorted(known, key=SECTION_ORDER.index):
        errors.append(f"{relative}: sections are out of canonical order")
        ok = False

    if not ok:
        return None
    return Record(
        identifier=identifier,
        title=str(data["title"]),
        scope=data["scope"],
        status=data["status"],
        date=date,
        supersedes=tuple(data["supersedes"]),
        superseded_by=tuple(data["superseded_by"]),
        path=path,
    )


def check_cross_references(records: list[Record], root: Path, errors: list[str]) -> None:
    by_identifier: dict[str, Record] = {}
    for record in records:
        existing = by_identifier.get(record.identifier)
        if existing is not None:
            errors.append(
                f"duplicate identifier {record.identifier}: "
                f"{existing.path.relative_to(root).as_posix()} and {record.path.relative_to(root).as_posix()}"
            )
            continue
        by_identifier[record.identifier] = record

    for record in records:
        relative = record.path.relative_to(root).as_posix()
        for target in record.supersedes:
            other = by_identifier.get(target)
            if other is None:
                errors.append(f"{relative}: supersedes unknown record {target}")
            elif record.identifier not in other.superseded_by:
                errors.append(f"{relative}: supersedes {target}, which does not list it in superseded_by")
        for target in record.superseded_by:
            other = by_identifier.get(target)
            if other is None:
                errors.append(f"{relative}: superseded_by unknown record {target}")
            elif record.identifier not in other.supersedes:
                errors.append(f"{relative}: superseded_by {target}, which does not list it in supersedes")
        if record.superseded_by and record.status not in ("superseded", "deprecated"):
            errors.append(f"{relative}: has superseded_by but status is {record.status!r}")


def render(records: list[Record], root: Path) -> str:
    lines = [
        "# ADR index",
        "",
        "Generated from the ADR front matter. Do not edit manually.",
        "",
        "Identifiers are allocated per scope and are never reused. A record's",
        "status lives in its front matter rather than in its path.",
        "",
    ]
    for scope, (prefix, directory) in SCOPES.items():
        scoped = [record for record in records if record.scope == scope]
        lines.append(f"## {scope} (`ADR-{prefix}-`, `adr/{directory}/`)")
        lines.append("")
        if not scoped:
            lines.append("No records.")
            lines.append("")
            continue
        lines.append("| Identifier | Title | Status | Date | Source |")
        lines.append("|---|---|---|---|---|")
        for record in sorted(scoped, key=sort_key):
            source = record.path.relative_to(root).as_posix()
            lines.append(
                f"| {record.identifier} | {record.title} | {record.status} | {record.date} | [{source}]({'../../' + source}) |"
            )
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def emit(path: Path, content: str, root: Path, check: bool) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return True
    if check:
        print(f"stale generated documentation: {path.relative_to(root)}", file=sys.stderr)
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"generated {path.relative_to(root)}")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()

    errors: list[str] = []
    records = [record for record in (load(path, root, errors) for path in adr_paths(root)) if record is not None]
    check_cross_references(records, root, errors)
    if errors:
        print("ADR index check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    generated = root / "generated" / "documentation" / "adr-index.md"
    if not emit(generated, render(records, root), root, args.check):
        return 1
    print(f"ADR index check passed: {len(records)} record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
