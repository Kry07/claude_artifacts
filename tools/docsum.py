"""Compare exported Cabinet docs with the repo copies.

Each published doc ends with a stamp line, "Repo sync: claude_artifacts commit <id>, <date>".
The stamp only lives in the published doc. This script strips it, so the md5 of an
export matches docs/checksums.md5 as long as the doc text itself is unchanged.

  uv run tools/docsum.py check <export.md>...   compare exports with docs/checksums.md5
  uv run tools/docsum.py pull  <export.md>...   write changed exports to docs/ and update the sums
  uv run tools/docsum.py sums                   rewrite docs/checksums.md5 from docs/*.md

An export is matched to its repo file by the first number in its file name, so name
exports artN.md (art2.md goes to docs/cabinet-2-*.md).
"""

import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
SUMS = DOCS / "checksums.md5"
STAMP = re.compile(rb"\n*Repo sync: [^\n]*\n*\Z")


def strip(data: bytes) -> bytes:
    """Remove the trailing stamp paragraph; the repo copies end with one newline."""
    out = STAMP.sub(b"\n", data)
    return out if out.endswith(b"\n") else out + b"\n"


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def read_sums() -> dict[str, str]:
    sums = {}
    if SUMS.exists():
        for line in SUMS.read_text().splitlines():
            digest, name = line.split(maxsplit=1)
            sums[name.lstrip("*")] = digest
    return sums


def write_sums() -> None:
    lines = [f"{md5(p.read_bytes())}  {p.name}" for p in sorted(DOCS.glob("cabinet-*.md"))]
    SUMS.write_text("\n".join(lines) + "\n", newline="\n")


def repo_file(export: Path) -> Path:
    m = re.search(r"(\d+)", export.stem)
    if not m:
        sys.exit(f"{export}: no doc number in the file name")
    hits = list(DOCS.glob(f"cabinet-{m.group(1)}-*.md"))
    if len(hits) != 1:
        sys.exit(f"{export}: no single docs/cabinet-{m.group(1)}-*.md (found {len(hits)})")
    return hits[0]


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("check", "pull", "sums"):
        sys.exit(__doc__)
    cmd, exports = sys.argv[1], [Path(a) for a in sys.argv[2:]]
    if cmd == "sums":
        write_sums()
        return
    sums, changed = read_sums(), 0
    for export in exports:
        target = repo_file(export)
        data = strip(export.read_bytes())
        stamp = STAMP.search(export.read_bytes())
        status = "same" if sums.get(target.name) == md5(data) else "CHANGED"
        print(f"{status:8} {target.name}  {'stamp: ' + stamp.group().strip().decode() if stamp else 'no stamp'}")
        if status == "CHANGED":
            changed += 1
            if cmd == "pull":
                target.write_bytes(data)
    if cmd == "pull" and changed:
        write_sums()
    sys.exit(1 if cmd == "check" and changed else 0)


if __name__ == "__main__":
    main()
