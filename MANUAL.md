# Cabinet docs – Manual

Nov 23, 2026 · @Kolja Kauer

How to use the Cabinet docs and the claude\_artifacts repo: which doc to give a session, how to start it, and how to see which version of each doc every session runs.

## The docs

Every session runs exactly one base, Base Ant or Base Owl, and may add any of the others on top. The rules for combining are in [Cabinet 0 – Index](https://claude.ai/artifact/TwFz84TC9NKjoE3K3PTcFH).

| Alias | Doc | Kind | Pick it when |
| --- | --- | --- | --- |
| art0 | [Cabinet 0 – Index](https://claude.ai/artifact/TwFz84TC9NKjoE3K3PTcFH) | index | never given to a session on its own; every doc links to it |
| art1 | [Cabinet 1 – Base Ant](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) | base | one repo, worked in stages with many helper roles and full specs |
| art5 | [Cabinet 5 – Base Owl](https://claude.ai/artifact/HG1zvy4LqoKS2TsrZp3Kv7) | base | one repo, leaner: every part checked by a verifier and a fresh reviewer |
| art2 | [Cabinet 2 – Overseer](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a) | role | one session should track and report on several others |
| art3 | [Cabinet 3 – Embassy](https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM) | people | several developers work on one project |
| art4 | [Cabinet 4 – Fast Forward](https://claude.ai/artifact/7c9zDiopSxQrD4jx9bhdk1) | mode | the session should run unattended, paced to the usage limits |
| art6 | [Cabinet 6 – Browser](https://claude.ai/artifact/HTQBenjZ84s8TCZ2Gwkkw7) | partner | a project has a web UI to test in Chrome on the PC |
| art7 | [Cabinet 7 – Fabian's Ruleset](https://claude.ai/artifact/NaZnikby9hTFXvUxdRdrx7) | ruleset | the session should follow Fabian's claude-skeleton exactly |

Base Ant and Base Owl are equal; Base Owl is the newer model, not the successor.

## Starting a session with docs

Use `claude-spawn open` from working-env, with the docs after `-c`, base first:

```
claude-spawn open kalendo ~/coding/kalendo -n -c art1,art4
```

The session reads the docs on claude.ai, replies with its DOCS line (the stamps it read), then one line on where it stands, and waits for your next message or `go`. `-n` starts a fresh conversation; without it the saved one resumes. `-l 85,90,80` sets the Fast Forward limits, `-t` trusts the folder, `-d` starts it without attaching. Instead of `-c`, `-i <image>` takes a named recipe, e.g. `-i minister-ff` (art1, art4 with limits); `claude-spawn images` lists them.

| Setup | Docs |
| --- | --- |
| One project, you watching | `art1` or `art5` |
| One project, overnight | `art1,art4` or `art5,art4` |
| Several projects at once | one overseer with `art2`; each project `art1` or `art5` and its `CLAUDE.md` names the overseer |
| A web UI to test | the project session, plus `claude-spawn browser <client>` (art6) |
| Fabian's rules | `art1,art7` or `art5,art7`, with `Skeleton: on` in the project `CLAUDE.md` |

Without claude-spawn, paste into a new session: `Read and apply these Cabinet docs, in this order: <links>. Run their First steps.`

## Stamps and the DOCS line

A stamp names one exact text of one doc. It is the last line of every doc, for example `Version: a2-398d1d7d`: `a2` is art2, and `398d1d7d` is the start of the md5 of the doc's text without that line. Change one letter and the text no longer matches its stamp, so anyone with an export can see it was edited after stamping.

| Where | What you see |
| --- | --- |
| end of each doc on claude.ai | its stamp |
| `cabinets.tsv` in claude\_artifacts | each doc's current stamp, and its newest stamp that changed rules |
| `docs/stamps.tsv` | every stamp ever made: date, parent, kind (`rules` or `wording`), note |
| a session's DOCS line | the stamps that session actually read |

The DOCS line is the first thing a session says after reading its docs, e.g. `DOCS a1-6d8d693b a4-27d3b1f1`. Ministers repeat it in HELLO and REPORT to their overseer, and a browser session in its READY. `rules` means a session on the older text would act differently; `wording` means it only reads better, and an older session needs no refresh.

## Is every session up to date

Ask working-env; it reads `cabinets.tsv` from this repo through its submodule:

| Command | What it does |
| --- | --- |
| `claude-spawn list` | every session with its doc state: `current`, `old` (behind on wording only), `OLD` (rules changed), `unread`, `differs`, `unknown`, `unrecorded` |
| `claude-spawn list --stale` | only the sessions that are behind |
| `claude-cli docs [--stale]` | the details: each session's docs and stamps |
| `claude-cli docs log art2 --since <stamp>` | what changed in a doc since the stamp a session carries |
| daemon `STATUS` | the same states and stamps on every machine, so the overseer sees them all |
| `claude-spawn refresh <name>` | a running session re-reads the docs that changed; only when you say so |
| `claude-spawn respawn <name>` | closes a session with its handover and starts it fresh on the current docs; only when you say so |

By hand: compare a session's DOCS line, or a minister's DOCS row in its REPORT, with `cabinets.tsv`. The overseer puts a stale minister under NEEDS YOU; it never stops a session for it. [working-env's own manual](https://claude.ai/artifact/HGzSWAwvy8F1q3CRyc5WJi) has every option.

## Changing a doc

The easy way: open a Claude session in `~/coding/claude_artifacts` and say what to change, e.g. "art2: the overseer also reports helper sessions". Its `CLAUDE.md` makes it follow the steps below.

The steps:

1. Change the text in the published doc on claude.ai.
2. Export it as Markdown and run `uv run tools/stamps.py new rules "<what changed>" art2.md` (or `wording`). It prints the new stamp line and updates `docs/`, `docs/stamps.tsv` and `cabinets.tsv`.
3. Replace the doc's last line with that stamp line.
4. Check: `uv run tools/stamps.py verify` says `current`, and the doc's export matches the file in `docs/`.
5. Commit and push. working-env picks up `cabinets.tsv` through its submodule.

Edited on claude.ai and forgot the rest? `uv run tools/stamps.py check art2.md` says `EDITED`; continue at step 2.

Adding a doc: next alias, `· artN` in its title, a row in `cabinets.tsv`, Cabinet 0 – Index and README.md, then step 2 with kind `initial`.

## Reference

`tools/stamps.py`, run with `uv run tools/stamps.py <command>` in the repo:

| Command | Does |
| --- | --- |
| `check <export.md>…` | per export: `current`, `EDITED` (text changed after its stamp), `OLD` (an older stamp), `UNKNOWN` (not in the log), `NO STAMP` |
| `new <kind> "<note>" <export.md>…` | makes the stamp for each changed export, writes `docs/`, logs it |
| `verify` | checks every file in `docs/` against its stamp, the log and `cabinets.tsv`; the pre-commit hook runs it |
| `list` | the current stamp of each doc |
| `log <alias> [--since <stamp>]` | a doc's stamps, newest first; exits 1 for an alias without stamps |

| File | Holds |
| --- | --- |
| `docs/cabinet-N-*.md` | exact copies of the published docs |
| `docs/stamps.tsv` | every stamp: date, parent, kind, md5, note |
| `cabinets.tsv` | alias, title, link, file, current stamp, newest rules stamp; read by working-env |
| `CLAUDE.md` | the rule a Claude session follows in this repo |
| `MANUAL.md` | this manual, as exported |
| `.githooks/pre-commit` | runs `verify`; enable once with `git config core.hooksPath .githooks` |
