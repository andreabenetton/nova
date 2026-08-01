# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

RULES = {
    ROOT / "protocols/p-stratum": [
        r"\bEdge(?:s|Id|Revision)?\b", r"\bClose(?:s)?\b", r"\bTrail(?:s)?\b",
        r"\bFlow(?:s)?\b", r"\bGram(?:s)?\b", r"\bGateway(?:s)?\b",
        r"\bBeacon(?:s)?\b", r"\bAuthority(?:ies)?\b", r"\bFacilit(?:y|ies)\b",
        r"\bObfuscated Degree\b", r"\bObfuscated-degree\b",
    ],
    ROOT / "protocols/r-stratum": [
        r"\bPeer(?:s|Handle)?\b", r"\bProvider Path(?:s)?\b", r"\bPath(?:s|Id|Revision)?\b",
        r"\bAdapter(?:s)?\b", r"\bBinding(?:s| instance)?\b", r"\bNexus Fundamenta\b",
        r"\bP-LAP\b", r"\bP-RAP\b", r"\bP-0AP\b", r"\bPacket(?:s)?\b",
    ],
    ROOT / "protocols/o-stratum": [
        r"\bPeer(?:s)?\b", r"\bPath(?:s)?\b", r"\bEdge(?:s)?\b", r"\bClose(?:s)?\b",
        r"\bLink(?:s)?\b", r"\bTrail(?:s)?\b", r"\bGram(?:s)?\b",
    ],
}

IGNORE_NAMES = {"LICENSE.md", "AGENTS.md", "CLAUDE.md"}

def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    return text

errors=[]
for base, patterns in RULES.items():
    compiled=[re.compile(x) for x in patterns]
    for path in sorted(base.rglob("*.md")):
        if path.name in IGNORE_NAMES or path.name == "glossary.md":
            continue
        text=strip_code(path.read_text(encoding="utf-8"))
        for lineno,line in enumerate(text.splitlines(),1):
            for pat in compiled:
                m=pat.search(line)
                if m:
                    errors.append(f"{path.relative_to(ROOT)}:{lineno}: foreign stratum term {m.group(0)!r}; move the mapping to an Interface document or rewrite in the owning vocabulary")

if errors:
    print("terminology boundary violations:", file=sys.stderr)
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("stratum terminology boundaries OK")
