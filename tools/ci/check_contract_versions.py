# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

import yaml


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def load_from_git(ref: str, path: str):
    try:
        text = git("show", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return None
    return yaml.safe_load(text)


def version_tuple(value: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in value.split("."))  # type: ignore[return-value]


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_contract_versions.py <base-ref>", file=sys.stderr)
        return 2
    base = sys.argv[1]
    changed = git("diff", "--name-status", f"{base}...HEAD", "--", "contracts/interfaces").splitlines()
    errors: list[str] = []
    for line in changed:
        status, path = line.split("\t", 1)
        if not path.endswith("/interface.yaml"):
            continue
        current_path = Path(path)
        current = yaml.safe_load(current_path.read_text(encoding="utf-8")) if current_path.exists() else None
        previous = load_from_git(base, path)
        if previous is not None and current is not None and canonical(previous) != canonical(current):
            errors.append(f"published Interface version modified in place: {path}")
            continue
        if status.startswith("A") and current is not None:
            iid = current["interface"]["id"]
            new_version = version_tuple(current["interface"]["version"])
            candidates = []
            for old_path in git("ls-tree", "-r", "--name-only", base, "contracts/interfaces").splitlines():
                if not old_path.endswith("/interface.yaml"):
                    continue
                old = load_from_git(base, old_path)
                if old and old.get("interface", {}).get("id") == iid:
                    candidates.append(version_tuple(old["interface"]["version"]))
            if candidates and new_version <= max(candidates):
                errors.append(f"new version {new_version} is not greater than baseline {max(candidates)} for {iid}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("contract version immutability check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
