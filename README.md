# Claude artifacts

Working copies of the Cabinet docs, the rules Claude Code sessions follow. They are developed here; the published versions live as Claude Docs, and sessions read those links.

## The docs

| Alias | File | Published doc | Field rating (0–10) |
| --- | --- | --- | --- |
| art0 | [docs/cabinet-0-index.md](docs/cabinet-0-index.md) | [Cabinet 0 – Index](https://claude.ai/artifact/TwFz84TC9NKjoE3K3PTcFH) | index, no rating |
| art1 | [docs/cabinet-1-solo-session.md](docs/cabinet-1-solo-session.md) | [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) | 7 – worked well in use |
| art2 | [docs/cabinet-2-overseer.md](docs/cabinet-2-overseer.md) | [Cabinet 2 – Overseer](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a) | rewritten 2026-11-15 (old Multi-Session design: 4 – worked badly); first test run 2026-11-15 |
| art3 | [docs/cabinet-3-multi-user.md](docs/cabinet-3-multi-user.md) | [Cabinet 3 – Multi-user](https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM) | not used yet |
| art4 | [docs/cabinet-4-fast-forward.md](docs/cabinet-4-fast-forward.md) | [Cabinet 4 – Fast Forward](https://claude.ai/artifact/7c9zDiopSxQrD4jx9bhdk1) | in use (rebuild, robinliste-rb), not rated |
| art5 | [docs/cabinet-5-review-flow.md](docs/cabinet-5-review-flow.md) | [Cabinet 5 – Review Flow (v1)](https://claude.ai/artifact/HG1zvy4LqoKS2TsrZp3Kv7) | not used yet; built from the Kalendo session, to compare with art1 |
| art6 | [docs/cabinet-6-browser.md](docs/cabinet-6-browser.md) | [Cabinet 6 – Browser](https://claude.ai/artifact/HTQBenjZ84s8TCZ2Gwkkw7) | first run 2026-11-15 (rebuild-browser) |

## What each one is

- **art0 Cabinet 0 – Index.** The list of all docs and how they combine; every doc links to it.
- **art1 Cabinet 1 – Solo-Session (base).** One session on one repo. CLAUDE.md core with switches, rules for what counts as an instruction and a yes, helper roles (scout, keeper, builder, architect, reviewer, verifier), five stages (brain dump → meeting → plan → sub-specs → master spec), states `open → in-progress → review → done`, sections `A`, `A.1`, `A.1.3` with the HERE line, commands, REPORT, NEXT-SESSION.
- **art2 Cabinet 2 – Overseer (role).** One session keeps track of several solo sessions, the ministers: what they do, where they are, what they spend. It reports (`report all`), splits the budget (`share br 50 kal 20`), and passes on `stop`, `resume`, pace and tasks by session messages. Ministers never wait for it, and nothing it sends is a yes. It may also work on its own project.
- **art3 Cabinet 3 – Multi-user (people).** Two or more developers on one project: areas with owners, branches per person, and one envoy session per person that exchanges requests, replies and proposals through a small embassy repo.
- **art4 Cabinet 4 – Fast Forward (mode).** Unattended work across 5-hour windows. Usage is measured by a status line, paced to about 85% by day and 90% by night (weekly limit set by the developer), paused cleanly before the limit and woken up in the next window, until `stop fast forward`.
- **art5 Cabinet 5 – Review Flow (base).** A lighter alternative to art1, built from one very successful session: numbered questions with recommendations, a verifier and a fresh reviewer with a risk list on every part, an autonomous-run section, NEEDS YOU, the `ASSUMED:` marker.
- **art6 Cabinet 6 – Browser (partner).** A session on the PC that drives Chrome and runs UI tests for exactly one paired client session, which can be on any machine: TEST briefs in, RESULTs out, only on listed test hosts, no passwords, no real purchases.

## How they combine

See [Cabinet 0 – Index](https://claude.ai/artifact/TwFz84TC9NKjoE3K3PTcFH) (art0, [docs/cabinet-0-index.md](docs/cabinet-0-index.md)): the rules for combining, who works with whom, the switches, typical setups and how to start sessions with `claude-spawn`. Every other doc links to it, so a new doc changes only the index, this README and `cabinets.tsv` in working-env.

Imported 2026-11-10 from the Markdown export of each doc (revisions 50, 50 and 39).
