# claude_artifacts

The published Cabinet docs (Claude Docs on claude.ai) are the source. `docs/cabinet-N-*.md` are byte-for-byte copies of their Markdown export. `cabinets.tsv` lists the docs with their links and current stamps; working-env reads it (this repo is its submodule). `MANUAL.md` is the developer's manual for this repo, published as an artifact.

## Stamps: the rule for every change

Every doc ends with its stamp, `Version: a2-3f9c21aa`: the short alias and the first 8 hex digits of the md5 of the export without that last line. So an export proves its own version. `docs/stamps.tsv` logs every stamp (date, parent, kind, md5, note). Sessions report the stamps they read (DOCS line, Cabinet 0 – Index, Versions), so a stamp must always match the text.

- **No doc text changes without a new stamp,** on claude.ai and in the repo alike.
- **At the start of work here:** export every doc and run `uv run tools/stamps.py check <exports>`. Report anything that is not `current` before other work.
- **Getting an export onto disk** without retyping it: the docs connector's `create` with `object: "blob"`, `payload: {"from": {"object": "file", "id": "<tab id>"}, "format": "markdown"}` returns an asset id and a sha256; the Artifact tool's `read` with that asset id as `path` saves the file to the scratchpad. The sha256 alone checks a local file without downloading.
- **Making a new stamp** (a doc shows `EDITED`, or you change one):
  1. Change the text in the published doc.
  2. Export it and run `uv run tools/stamps.py new <rules|wording> "<what changed, one line>" <export>`. It prints the stamp line, writes the copy in `docs/` and logs the stamp in `docs/stamps.tsv` and `cabinets.tsv`.
  3. Replace the doc's last line with that stamp line.
  4. Check: the published doc's export sha256 equals `sha256sum docs/<file>`, and `uv run tools/stamps.py verify` says `current` for every doc.
  5. Commit the copy, `docs/stamps.tsv` and `cabinets.tsv` together. The pre-commit hook (`.githooks/`, enabled by `git config core.hooksPath .githooks`) runs `verify`.
- **Kind:** `rules` when a session would act differently, `wording` when it only reads better. Sessions on an old `wording` stamp need no refresh.
- **Never** write a stamp by hand, edit a committed row of `docs/stamps.tsv`, or change a doc's text after its stamp without making a new one.
- **A new doc:** next alias, `· artN` in its title, its row in `cabinets.tsv` (alias, title, url, file; stamp columns `-`), then `new initial`. Also add it to Cabinet 0 – Index and README.md.
- **Names:** Cabinet 0 – Index, 1 – Base Ant, 2 – Overseer, 3 – Embassy, 4 – Fast Forward, 5 – Base Owl, 6 – Browser, 7 – Fabian's Ruleset. Base Ant and Base Owl are equal bases; neither is the successor.
- **Every change to the repo's tools or routine** also updates `MANUAL.md` and republishes it.
