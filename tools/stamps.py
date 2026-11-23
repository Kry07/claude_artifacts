"""Stamps of the Cabinet docs: check exports, make new stamps, keep cabinets.tsv current.

A doc's stamp is its last line, "Version: a2-3f9c21aa": the short alias (a2 = art2) and the
first 8 hex digits of the md5 of the doc's Markdown export without that last line (the body).
So every export proves its own version: if the body no longer hashes to the stamp, the text
was changed after the stamp was made.

docs/stamps.tsv is the log, one row per stamp, never edited afterwards:
  stamp  date  parent (the stamp before, or -)  kind (initial|rules|wording)  md5 (of the whole export)  note
cabinets.tsv lists the docs (alias, title, url, file) and, written by this script, the current
stamp and the newest stamp whose kind is rules or initial. working-env reads it.

  uv run tools/stamps.py check <export.md>...         current | EDITED | OLD | UNKNOWN | NO STAMP
  uv run tools/stamps.py new <kind> "<note>" <export.md>...
        for each export whose text changed: prints the new stamp line, writes docs/<file> as the
        doc will be after you put that line at its end, and logs the stamp
  uv run tools/stamps.py verify                         every docs/ file: stamp proves its body, is
                                                        logged, is current, md5 matches the log
  uv run tools/stamps.py list                           the current stamp of each doc
  uv run tools/stamps.py log <alias> [--since <stamp>]  a doc's stamps, newest first
An export is matched to its doc by the stamp's alias, or by the first number in its file name.
"""

import datetime
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOG = REPO / "docs" / "stamps.tsv"
CABINETS = REPO / "cabinets.tsv"
STAMP_LINE = re.compile(rb"Version: (a(\d+)-[0-9a-f]{8})\n?")
OLD_LINE = re.compile(rb"Version: .*\n?")
KINDS = ("initial", "rules", "wording")


def split(data: bytes):
    """(body, last line) of an export: the body keeps the newline before the last line"""
    end = data.rstrip(b"\n")
    cut = end.rfind(b"\n") + 1
    return data[:cut], data[cut:]


def key(body: bytes) -> str:
    return hashlib.md5(body).hexdigest()[:8]


def stamp_of(data: bytes):
    """(stamp, alias number) from the last line, or (None, None)"""
    m = STAMP_LINE.fullmatch(split(data)[1])
    return (m.group(1).decode(), m.group(2).decode()) if m else (None, None)


def read_tsv(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, line.split("\t"))) for line in lines[1:] if line]


def write_tsv(path: Path, rows: list[dict], head: list[str]) -> None:
    text = "\t".join(head) + "\n" + "".join("\t".join(r[h] for h in head) + "\n" for r in rows)
    path.write_text(text, encoding="utf-8", newline="\n")


def log() -> list[dict]:
    return read_tsv(LOG)


def current() -> dict[str, dict]:
    """alias number -> its newest log row (the last one in the file)"""
    out = {}
    for row in log():
        out[row["stamp"].split("-")[0][1:]] = row
    return out


def doc_row(n: str) -> dict:
    for row in read_tsv(CABINETS):
        if row["alias"] == f"art{n}":
            return row
    sys.exit(f"art{n} is not in cabinets.tsv")


def number_of(export: Path, data: bytes) -> str:
    n = stamp_of(data)[1]
    if n is None:
        m = re.search(r"(\d+)", export.stem)
        if not m:
            sys.exit(f"{export}: no stamp and no doc number in the file name")
        n = m.group(1)
    return n


def status(data: bytes, logged: dict, top: dict):
    stamp, n = stamp_of(data)
    if stamp is None:
        return "NO STAMP", None
    body = split(data)[0]
    if key(body) != stamp.split("-")[1]:
        return "EDITED", stamp
    if stamp not in logged:
        return "UNKNOWN", stamp
    if top[n]["stamp"] != stamp:
        return f"OLD (current {top[n]['stamp']})", stamp
    return "current", stamp


def check(paths: list[Path]) -> int:
    logged = {r["stamp"]: r for r in log()}
    top = current()
    bad = 0
    for p in paths:
        s, stamp = status(p.read_bytes(), logged, top)
        bad += s != "current"
        print(f"{p.name:34} {stamp or '-':12} {s}")
    return 1 if bad else 0


def new(kind: str, note: str, paths: list[Path]) -> None:
    if kind not in KINDS:
        sys.exit(f"kind must be one of: {', '.join(KINDS)}")
    if "\t" in note or "\n" in note:
        sys.exit("the note must be one line without tabs")
    top = current()
    rows = []
    for p in paths:
        data = p.read_bytes()
        n = number_of(p, data)
        last = split(data)[1]
        body = split(data)[0] if (STAMP_LINE.fullmatch(last) or OLD_LINE.fullmatch(last)) else data
        if not body.endswith(b"\n\n"):
            body = body.rstrip(b"\n") + b"\n\n"
        stamp = f"a{n}-{key(body)}"
        if n in top and top[n]["stamp"] == stamp:
            print(f"{p.name}: unchanged, still {stamp}")
            continue
        final = body + f"Version: {stamp}\n".encode()
        (REPO / doc_row(n)["file"]).write_bytes(final)
        parent = top[n]["stamp"] if n in top else "-"
        rows.append({"stamp": stamp, "date": str(datetime.date.today()), "parent": parent,
                     "kind": kind, "md5": hashlib.md5(final).hexdigest(), "note": note})
        print(f"art{n}: put this as the doc's last line:  Version: {stamp}")
    if rows:
        write_tsv(LOG, log() + rows, ["stamp", "date", "parent", "kind", "md5", "note"])
        write_cabinets()


def write_cabinets() -> None:
    rows = read_tsv(CABINETS)
    by_alias: dict[str, list[dict]] = {}
    for r in log():
        by_alias.setdefault("art" + r["stamp"].split("-")[0][1:], []).append(r)
    for row in rows:
        hist = by_alias.get(row["alias"], [])
        row["stamp"] = hist[-1]["stamp"] if hist else "-"
        rules = [r for r in hist if r["kind"] in ("initial", "rules")]
        row["rules"] = rules[-1]["stamp"] if rules else "-"
    write_tsv(CABINETS, rows, ["alias", "title", "url", "file", "stamp", "rules"])


def verify() -> int:
    logged = {r["stamp"]: r for r in log()}
    top = current()
    bad = 0
    for row in read_tsv(CABINETS):
        p = REPO / row["file"]
        data = p.read_bytes()
        s, stamp = status(data, logged, top)
        if s == "current" and logged[stamp]["md5"] != hashlib.md5(data).hexdigest():
            s = "MD5 differs from the log"
        if s == "current" and row["stamp"] != stamp:
            s = "cabinets.tsv is behind (run: stamps.py new, or rewrite with write_cabinets)"
        bad += s != "current"
        print(f"{row['alias']:5} {stamp or '-':12} {s}")
    return 1 if bad else 0


def show_log(alias: str, since: str | None) -> None:
    n = alias.removeprefix("art").removeprefix("a")
    rows = [r for r in log() if r["stamp"].startswith(f"a{n}-")]
    if not rows:
        sys.exit(f"art{n} has no stamps")
    if since:
        stamps = [r["stamp"] for r in rows]
        if since not in stamps:
            sys.exit(f"{since} is not a stamp of art{n}")
        rows = rows[stamps.index(since) + 1:]
    for r in reversed(rows):
        print(f"{r['stamp']}  {r['date']}  {r['kind']:8} {r['note']}")


def main() -> None:
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "check" and args:
        sys.exit(check([Path(a) for a in args]))
    elif cmd == "new" and len(args) >= 3:
        new(args[0], args[1], [Path(a) for a in args[2:]])
    elif cmd == "verify":
        sys.exit(verify())
    elif cmd == "list":
        for n, r in sorted(current().items(), key=lambda kv: int(kv[0])):
            print(f"art{n:3} {r['stamp']}  {r['date']}  {r['kind']:8} {r['note']}")
    elif cmd == "log" and args:
        since = args[args.index("--since") + 1] if "--since" in args else None
        show_log(args[0], since)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
