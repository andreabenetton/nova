# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import re
import subprocess
import sys

SIGNOFF = re.compile(r"^Signed-off-by:\s+.+\s+<[^<>\s]+@[^<>\s]+>\s*$", re.MULTILINE)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("usage: check_dco.py <base-ref> [head-ref]", file=sys.stderr)
        return 2
    base = sys.argv[1]
    head = sys.argv[2] if len(sys.argv) == 3 else "HEAD"
    # Merge commits are exempt. Integration policy requires merge commits, and
    # both GitHub's merge button and `git merge` generate them without a
    # trailer, so checking them would fail every pull request regardless of how
    # the authored commits were signed off.
    records = git(
        "log", "--no-merges", "--format=%H%x00%B%x00", f"{base}..{head}"
    ).split("\x00")
    failures: list[str] = []
    for index in range(0, len(records) - 1, 2):
        commit = records[index].strip()
        body = records[index + 1]
        if commit and not SIGNOFF.search(body):
            subject = git("show", "-s", "--format=%s", commit).strip()
            failures.append(f"{commit[:12]} {subject}")
    if failures:
        print("DCO sign-off missing from commit(s):", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        print("Amend each commit with: git commit --amend -s", file=sys.stderr)
        return 1
    print("DCO check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
