# Claude artifacts

Copies of the Cabinet docs, the rules Claude Code sessions follow. The published versions live as Claude Docs, and sessions read those links; the files here are byte-for-byte copies of their Markdown export. How to use all of it: [MANUAL.md](MANUAL.md), published as [Cabinet docs – Manual](https://claude.ai/artifact/8177hnvixmmPsmEofuYwEL). The rule for changing a doc: [CLAUDE.md](CLAUDE.md).

## The docs

| Alias | File | Published doc | Field rating (0–10) |
| --- | --- | --- | --- |
| art0 | [docs/cabinet-0-index.md](docs/cabinet-0-index.md) | [Cabinet 0 – Index](https://claude.ai/artifact/TwFz84TC9NKjoE3K3PTcFH) | index, no rating |
| art1 | [docs/cabinet-1-base-ant.md](docs/cabinet-1-base-ant.md) | [Cabinet 1 – Base Ant](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) | 7 – worked well in use |
| art2 | [docs/cabinet-2-overseer.md](docs/cabinet-2-overseer.md) | [Cabinet 2 – Overseer](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a) | rewritten 2026-11-15 (old Multi-Session design: 4 – worked badly); first test run 2026-11-15 |
| art3 | [docs/cabinet-3-embassy.md](docs/cabinet-3-embassy.md) | [Cabinet 3 – Embassy](https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM) | not used yet |
| art4 | [docs/cabinet-4-fast-forward.md](docs/cabinet-4-fast-forward.md) | [Cabinet 4 – Fast Forward](https://claude.ai/artifact/7c9zDiopSxQrD4jx9bhdk1) | in use (rebuild, robinliste-rb), not rated |
| art5 | [docs/cabinet-5-base-owl.md](docs/cabinet-5-base-owl.md) | [Cabinet 5 – Base Owl](https://claude.ai/artifact/HG1zvy4LqoKS2TsrZp3Kv7) | not used yet; built from the Kalendo session |
| art6 | [docs/cabinet-6-browser.md](docs/cabinet-6-browser.md) | [Cabinet 6 – Browser](https://claude.ai/artifact/HTQBenjZ84s8TCZ2Gwkkw7) | first run 2026-11-15 (rebuild-browser) |
| art7 | [docs/cabinet-7-fabians-ruleset.md](docs/cabinet-7-fabians-ruleset.md) | [Cabinet 7 – Fabian's Ruleset](https://claude.ai/artifact/NaZnikby9hTFXvUxdRdrx7) | not used yet |

The current stamp of each doc is in [cabinets.tsv](cabinets.tsv), the history in [docs/stamps.tsv](docs/stamps.tsv).

## What each one is

- **art0 Cabinet 0 – Index.** The list of all docs, how they combine, and the Versions rules (stamps, DOCS line); every doc links to it.
- **art1 Cabinet 1 – Base Ant (base).** One session on one repo. CLAUDE.md core with switches, rules for what counts as an instruction and a yes, helper roles (scout, keeper, builder, architect, reviewer, verifier), five stages (brain dump → meeting → plan → sub-specs → master spec), states `open → in-progress → review → done`, sections `A`, `A.1`, `A.1.3` with the HERE line, commands, REPORT, NEXT-SESSION.
- **art2 Cabinet 2 – Overseer (role).** One session keeps track of several solo sessions, the ministers: what they do, where they are, what they spend, which doc stamps they carry. It reports (`report all`), splits the budget (`share br 50 kal 20`), and passes on `stop`, `resume`, pace and tasks by session messages. Ministers never wait for it, and nothing it sends is a yes. It may also work on its own project.
- **art3 Cabinet 3 – Embassy (people).** Two or more developers on one project: areas with owners, branches per person, personal folders, and one envoy session per person that exchanges requests, replies and proposals through a small embassy repo.
- **art4 Cabinet 4 – Fast Forward (mode).** Unattended work across 5-hour windows. Usage is measured by a status line, paced to about 85% by day and 90% by night (weekly limit set by the developer), paused cleanly before the limit and woken up in the next window, until `stop fast forward`.
- **art5 Cabinet 5 – Base Owl (base).** The newer of the two equal bases, built from one very successful session: numbered questions with recommendations, a verifier and a fresh reviewer with a risk list on every part, an autonomous-run section, NEEDS YOU, the `ASSUMED:` marker. Not the successor of Base Ant.
- **art6 Cabinet 6 – Browser (partner).** A session on the PC that drives Chrome and runs UI tests for exactly one paired client session, which can be on any machine: TEST briefs in, RESULTs out, only on listed test hosts, no passwords, no real purchases.
- **art7 Cabinet 7 – Fabian's Ruleset (ruleset).** With `Skeleton: on`, a session runs Fabian's `claude-skeleton` rules, commands, hooks, skills, agents and status board exactly as he does, from the person's own folder (Cabinet 3, Personal folders).

## How they combine

See [Cabinet 0 – Index](https://claude.ai/artifact/TwFz84TC9NKjoE3K3PTcFH): one base (Base Ant or Base Owl), plus art2, art3, art4, art6 or art7 on top; the switches; who works with whom; typical setups; starting sessions with `claude-spawn`.

## History

Imported 2026-11-10 from the Markdown export of each doc. Synced 2026-11-22 (art2 and art3 had newer text, art7 added). 2026-11-23: renamed (Base Ant, Embassy, Base Owl, Fabian's Ruleset), art7 released, stamps and the DOCS line introduced.
