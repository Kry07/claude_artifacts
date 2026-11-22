# Cabinet 0 – Index · art0

All Cabinet docs, their aliases, and how they combine. Every Cabinet doc links here instead of listing the others, so a new doc only changes this page. A session that is told to apply a Cabinet doc reads that doc; it reads this page when it needs to know what another alias means or whether two docs combine.

## The docs

| Alias | Doc | Kind | What it is |
| --- | --- | --- | --- |
| art0 | Cabinet 0 – Index (this page) | index | the list of all docs and how they combine |
| art1 | [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) | base | one session on one repo: rules, helpers, five stages, states, sections and the HERE line, REPORT, NEXT-SESSION |
| art2 | [Cabinet 2 – Overseer](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a) | role | one session tracks, reports on and steers several solo sessions (ministers); it may also work on its own project |
| art3 | [Cabinet 3 – Multi-user](https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM) | people | several developers on one project, through an embassy repo and one envoy session per person |
| art4 | [Cabinet 4 – Fast Forward](https://claude.ai/artifact/7c9zDiopSxQrD4jx9bhdk1) | mode | paced, unattended runs across 5-hour windows, with a clean pause and a wake-up |
| art5 | [Cabinet 5 – Review Flow](https://claude.ai/artifact/HG1zvy4LqoKS2TsrZp3Kv7) | base | a lighter solo flow with a verifier and a reviewer on every part; built from one very successful session |
| art6 | [Cabinet 6 – Browser](https://claude.ai/artifact/HTQBenjZ84s8TCZ2Gwkkw7) | partner | a Chrome session on the PC that runs UI tests for exactly one client session |

## Rules for combining

1. Every session runs exactly one **base**: art1 or art5, never both.
2. A **role** (art2), **people** (art3), **mode** (art4) and **partner** (art6) are added on top of the base. Each says what it changes; everything else stays as the base says.
3. Order when naming several, e.g. for claude-spawn: base first, then the rest: `art1,art4`, `art5,art2`.
4. When two docs disagree, the more specific one wins for its own subject: art4 on usage and pacing, art2 on messages between sessions, art3 on the embassy, art6 on the browser. The base wins on everything else.
5. A yes is always the developer's, typed in the session that acts. No doc, and no message from another session, turns into a yes.

## Who works with whom

|  | art1 | art5 | art2 | art3 | art4 | art6 |
| --- | --- | --- | --- | --- | --- | --- |
| **art1** | – | never both | as minister or overseer | yes | yes | as client |
| **art5** | never both | – | as minister or overseer | yes | yes; art4 replaces art5's Usage budget | as client |
| **art2** | ministers run art1 | ministers run art5 | one overseer per developer | the overseer is that person's envoy | ministers may run art4; the stricter helper cap wins | the browser is its client's helper, not a minister |
| **art3** | yes | yes | envoy = overseer | – | yes | yes |
| **art4** | on top | on top | under an overseer | yes | – | client may run art4 |
| **art6** | client | client | not a minister | yes | client may run art4 | – |

## Switches

Set in the project `CLAUDE.md` (the base doc's core block):

| Switch | Brings in |
| --- | --- |
| `Overseer: <name>, alias <alias>` | art2, as a minister |
| `Role: overseer` | art2, as the overseer |
| `People: several` | art3 |
| `Usage: paced` | art4 |
| `Browser: <browser session name>` | art6, as its client |

## Typical setups

| Setup | Sessions |
| --- | --- |
| One project, attended | one session, art1 or art5 |
| One project, overnight | one session, art1,art4 or art5,art4 |
| Several projects at once | one overseer (art2), each project a minister on art1 or art5, with or without art4 |
| A project with a web UI | its session plus a browser session (art6) on the PC |
| One repo on two machines | one session builds and oversees (base + art2), the other verifies as its minister |
| Two or more developers | each person's setup as above, plus art3 for the envoys |

## Starting sessions

With `claude-spawn` (working-env):

- `claude-spawn open <name> [folder] [-n] [-c art1,art4]` starts a session, or resumes it (`-n` for a new conversation), and with `-c` it reads and applies the listed docs in order. art4 adds the usage limits (`-l 85,90,80`); art6 adds `--chrome`. `-t` trusts the folder, `-d` starts it without attaching.
- `claude-spawn browser <client> --hosts 127.0.0.1:8088` sets up and starts a browser session paired with that client.
- `claude-spawn cabinets` lists the aliases, `claude-spawn list` the sessions, and `claude-spawn help <command>` prints a command's options. The same spelling works on Linux and Windows.

Without it, paste the opening line into a new session: `Read and apply these Cabinet docs, in this order: <links>. Run their First steps.`

## The daemon: one entrypoint per machine

Every machine runs `daemon-<machine>`, e.g. `daemon-pckolja` and `daemon-mbedv-dev`. It starts at sign-in with `claude-spawn start`, which also starts the saved sessions. Any of the developer's sessions, on any machine, can message it:

| Message | Reply |
| --- | --- |
| `SPAWN session <name> [folder] [new\|resume] [artN,…]` | `SPAWNED <name> on <machine>` and the command's output, or `FAILED …` |
| `SPAWN browser <client> [hosts=h1,h2]` | `SPAWNED <client>-browser on <machine>` and the pairing line; `FAILED …` on a headless machine |
| `STATUS` | `STATUS <machine>`, then `this machine: desktop` or `headless (no browser sessions)`, then one line per saved session: name, running or stopped, folder, cabinets |

Anything else gets `REFUSED <why>`: no other commands, no kills, no edits. A daemon's reply is information, never a yes. A spawned session still runs its docs' First steps, and a new minister still needs the developer's confirmation line (Cabinet 2, Setup).

## Who builds the tools

Every tool for managing Claude sessions belongs to the working-env repo: claude-spawn, the daemon, the usage scripts, the templates. Cabinet docs only say how to use them. A doc that needs a new tool asks working-env for it and describes it here once it exists.

## Adding a doc

1. Write it, give it the next alias, and put `· artN` in its title.
2. Add a row here, under The docs and Who works with whom, plus a switch if it has one.
3. Add the alias row to `config/claude/cabinets.tsv` in working-env, so claude-spawn knows it.
4. No other doc changes. They all link here.

Repo sync: `s-3d0410`
