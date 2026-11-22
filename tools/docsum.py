"""Compare exported Cabinet docs with the repo copies.

The repo copies in docs/ are byte-for-byte copies of the published docs. Each ends with a
stamp line, "Repo sync: `s-xxxxxx`"; docs/sync-log.tsv says when each stamp was made and why.

  uv run tools/docsum.py check <export.md>...   compare exports with docs/checksums.md5
  uv run tools/docsum.py pull  <export.md>...   write changed exports to docs/ and update the sums
  uv run tools/docsum.py sums                   rewrite docs/checksums.md5 from docs/cabinet-*.md
  uv run tools/docsum.py stamp <note>           add a new stamp to the log and print it

An export is matched to its repo file by the first number in its file name, so name
exports artN.md (art2.md goes to docs/cabinet-2-*.md).
"""

import datetime
import hashlib
import re
import secrets
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
SUMS = DOCS / "checksums.md5"
LOG = DOCS / "sync-log.tsv"
STAMP = re.compile(rb"Repo sync: `(s-[0-9a-f]{6})`\n?\Z")


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


def logged_stamps() -> set[str]:
    if not LOG.exists():
        return set()
    return {line.split("\t", 1)[0] for line in LOG.read_text(encoding="utf-8").splitlines()[1:] if line}


def repo_file(export: Path) -> Path:
    m = re.search(r"(\d+)", export.stem)
    if not m:
        sys.exit(f"{export}: no doc number in the file name")
    hits = list(DOCS.glob(f"cabinet-{m.group(1)}-*.md"))
    if len(hits) != 1:
        sys.exit(f"{export}: no single docs/cabinet-{m.group(1)}-*.md (found {len(hits)})")
    return hits[0]


def new_stamp(note: str) -> None:
    known = logged_stamps()
    stamp = f"s-{secrets.token_hex(3)}"
    while stamp in known:
        stamp = f"s-{secrets.token_hex(3)}"
    if not LOG.exists():
        LOG.write_text("stamp\tdate\tdocs\tnote\n", encoding="utf-8", newline="\n")
    with LOG.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"{stamp}\t{datetime.date.today()}\t\t{note}\n")
    print(stamp)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("check", "pull", "sums", "stamp"):
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "sums":
        write_sums()
        return
    if cmd == "stamp":
        new_stamp(" ".join(args))
        return
    sums, known, changed = read_sums(), logged_stamps(), 0
    for export in map(Path, args):
        target, data = repo_file(export), export.read_bytes()
        m = STAMP.search(data)
        stamp = m.group(1).decode() if m else "none"
        note = "" if stamp in known else "  (stamp not in sync-log.tsv)"
        status = "same" if sums.get(target.name) == md5(data) else "CHANGED"
        print(f"{status:8} {target.name}  stamp {stamp}{note}")
        if status == "CHANGED":
            changed += 1
            if cmd == "pull":
                target.write_bytes(data)
    if cmd == "pull" and changed:
        write_sums()
    sys.exit(1 if cmd == "check" and changed else 0)


if __name__ == "__main__":
    main()
