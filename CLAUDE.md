# claude_artifacts

The published Cabinet docs (Claude Docs on claude.ai) are the source. `docs/cabinet-N-*.md` are byte-for-byte copies of their Markdown export. Links and aliases: README.md.

## Versions: the rule for every change

Every doc ends with its stamp, ``Version: `art2.v3` ``. The alias never changes; the number goes up by one with every new text. `docs/versions.tsv` records each version: stamp, date, md5 of the whole export, kind, note. Sessions report the stamps they carry, so the stamp must always name the text the doc really has.

- **No doc text changes without a new version.** That holds for edits on claude.ai and in the repo alike.
- **At the start of work here**, export every doc to `artN.md` in the scratchpad and run `uv run tools/docsum.py check art*.md`. Report anything that is not `current` before other work.
- **Making a version** (a doc shows `EDITED`, or you change one):
  1. `uv run tools/docsum.py next art2` prints the stamp, e.g. `art2.v4`.
  2. Make the text change in the published doc, and replace its last line with the new stamp.
  3. Export it again to `art2.md`.
  4. `uv run tools/docsum.py add <rules|wording> "<what changed, one line>" art2.md` writes the copy to `docs/` and adds the row.
  5. Commit the copy and `versions.tsv` together.
- **Kind:** `rules` when a session would act differently, `wording` when it only reads better. A session on an old `wording` version needs no refresh.
- **Never** write a stamp by hand that `next` did not print, reuse a number, or edit a row of `versions.tsv` after it is committed.
- A new doc starts at `artN.v1` (kind `initial`), and also gets its rows in README.md, Cabinet 0 and `cabinets.tsv` in working-env.
