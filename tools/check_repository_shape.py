from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
empty = []
for directory in sorted(path for path in root.rglob("*") if path.is_dir() and ".git" not in path.parts):
    if not any(directory.iterdir()):
        empty.append(directory.relative_to(root))
if empty:
    print("empty directories must contain a README.md or placeholder:", file=sys.stderr)
    for directory in empty:
        print(directory, file=sys.stderr)
    raise SystemExit(1)
print("repository shape OK")
