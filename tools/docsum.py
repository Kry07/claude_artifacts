"""Versions of the Cabinet docs: compare published exports with the repo, and record new versions.

The repo copies in docs/ are byte-for-byte copies of the published docs (Markdown export).
Each doc ends with its version stamp, "Version: `art2.v3`": the alias never changes, the
number goes up by one for every new text. docs/versions.tsv has one row per version:
stamp, date, md5 of the whole export (stamp included), kind (rules or wording), note.

  uv run tools/docsum.py check <artN.md>...          compare exports with the registry
  uv run tools/docsum.py next <artN>                 print the next stamp for a doc
  uv run tools/docsum.py add <kind> <note> <artN.md>... record exports that carry their new stamp
  uv run tools/docsum.py list                        latest version of each doc

check prints per export:
  current   the stamp is the doc's latest version and the text is that version's
  EDITED    the text differs from what its stamp was recorded with: edited on claude.ai
            without a new version. Make one (next, stamp the doc, export, add).
  OLD       the export carries an older version than the registry's latest
  UNKNOWN   no stamp, or a stamp the registry does not have
Exports are matched to docs/cabinet-N-*.md by the first number in their file name.
"""

import datetime
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
REG = DOCS / "versions.tsv"
STAMP = re.compile(rb"Version: `(art(\d+)\.v(\d+))`\n?\Z")
KINDS = ("rules", "wording", "initial")


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def registry() -> list[dict]:
    lines = REG.read_text(encoding="utf-8").splitlines()
    keys = lines[0].split("\t")
    return [dict(zip(keys, line.split("\t"))) for line in lines[1:] if line]


def latest() -> dict[str, dict]:
    """alias -> its row with the highest version"""
    out = {}
    for row in registry():
        alias, v = row["stamp"].split(".v")
        if alias not in out or int(v) > int(out[alias]["stamp"].split(".v")[1]):
            out[alias] = row
    return out


def repo_file(alias_number: str) -> Path:
    hits = list(DOCS.glob(f"cabinet-{alias_number}-*.md"))
    if len(hits) != 1:
        sys.exit(f"no single docs/cabinet-{alias_number}-*.md (found {len(hits)})")
    return hits[0]


def stamp_of(data: bytes):
    m = STAMP.search(data)
    return (m.group(1).decode(), m.group(2).decode()) if m else (None, None)


def check(exports: list[Path]) -> int:
    rows = {r["stamp"]: r for r in registry()}
    top = latest()
    bad = 0
    for export in exports:
        data = export.read_bytes()
        stamp, n = stamp_of(data)
        if stamp not in rows:
            status = "UNKNOWN"
        elif rows[stamp]["md5"] != md5(data):
            status = "EDITED"
        elif top[f"art{n}"]["stamp"] != stamp:
            status = f"OLD (latest {top[f'art{n}']['stamp']})"
        else:
            status = "current"
        bad += status != "current"
        print(f"{export.name:12} {stamp or '-':10} {status}")
    return 1 if bad else 0


def add(kind: str, note: str, exports: list[Path]) -> None:
    if kind not in KINDS:
        sys.exit(f"kind must be one of {', '.join(KINDS)}")
    top = latest()
    rows = []
    for export in exports:
        data = export.read_bytes()
        stamp, n = stamp_of(data)
        if not stamp:
            sys.exit(f"{export}: no Version stamp at the end")
        want = next_stamp(f"art{n}", top)
        if stamp != want:
            sys.exit(f"{export}: carries {stamp}, the next version is {want}")
        repo_file(n).write_bytes(data)
        rows.append(f"{stamp}\t{datetime.date.today()}\t{md5(data)}\t{kind}\t{note}\n")
    with REG.open("a", encoding="utf-8", newline="\n") as f:
        f.writelines(rows)
    print("".join(rows), end="")


def next_stamp(alias: str, top=None) -> str:
    top = latest() if top is None else top
    return f"{alias}.v{int(top[alias]['stamp'].split('.v')[1]) + 1}" if alias in top else f"{alias}.v1"


def main() -> None:
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "check" and args:
        sys.exit(check([Path(a) for a in args]))
    if cmd == "next" and len(args) == 1:
        print(next_stamp(args[0]))
    elif cmd == "add" and len(args) >= 3:
        add(args[0], args[1], [Path(a) for a in args[2:]])
    elif cmd == "list":
        for alias, row in sorted(latest().items(), key=lambda kv: int(kv[0][3:])):
            print(f"{row['stamp']:10} {row['date']}  {row['kind']:8} {row['note']}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
