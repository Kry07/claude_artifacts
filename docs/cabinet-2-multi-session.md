# Cabinet 2 – Multi-Session

## Start here

One developer, several `claude` sessions: a lead plus deputies, talking only through files. Applies whenever `<repo>/CLAUDE.md` says `Sessions: many`, even with no deputy yet: the lead runs JOIN and keeps BOARD. All of [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) applies to every session here and is not repeated. Two or more people on one project: [Cabinet 3 – Multi-User](https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM).

## Sessions

Session files: `~/.claude/<name>/`. Role, area and lead = your launch prompt, else your `NEXT-SESSION.md` header, else ask the developer once. `<lead>` in every path here = the name after `Lead is` in your launch prompt (`me`: your own name).

| Role | Count | Does | Talks to |
| --- | --- | --- | --- |
| lead | one per developer | talks to the developer about everything; issues every order; keeps BOARD; no item work once it has a deputy | developer; deputies via ORDERS and REPORTS |
| deputy | one per area | works its area with its own helpers; orders from the lead, direct instructions from the developer | developer; lead via REPORTS |

Hub and spoke: deputies never talk to each other; lead → ORDER → deputy, deputy → REPORT → lead, nothing else. A shared piece (used by two or more areas) is ordered to one deputy, whose architect lands it before any builder starts. Work in the lead's own repo goes to a deputy in a worktree, never to the lead. Helpers: the helper table in [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw), section Helpers.

## Starting a session

The developer starts every session. Lead: by hand in the project repo, the command below with `<role>` = lead, `<area>` = `<repo>`, `Lead is me` (after a handover: Lead handover, step 2). Deputy: by summon.

Summon, on `summon <name> <dir>` in the lead session. `<repo>` = folder name of the git root at `<dir>`; `<area>` = `<repo>` unless a third word, `summon <name> <dir> <area>`, names one; `<role>` = deputy.

1. Check: `<dir>/CLAUDE.md` exists and says `Sessions: many`; `<name>` is not `active` in BOARD Sessions (`stale`: re-summon in its existing directory, same command; `retired`: never reused, ask for another name). Anything missing or failing: say which, ask, change nothing.
2. `<repo>` already the Area of an `active` or `stale` row and `<name>` new: after the `go` of step 4, first run `git worktree add ../<repo>-<name>` in `<dir>`; `<dir>` = that new path from here on.
3. Show the exact command; the quoted prompt holds no quotes, `$`, backticks or secrets:

```
cd <dir> && claude -n <name> "You are <name>, <role> for <area>. Lead is <lead>. Run the First steps in CLAUDE.md."
```

4. After `go` (one per summon): tell the developer to run it in a new terminal window or pane named `<name>`; a `spawn` or `tmux` skill (Skills) may run it instead, never required.
5. The new window may ask whether to trust the project; the developer answers there. Never answer it yourself, pass flags that skip prompts, type into another session's window or stop a session you did not start.
6. Done when the new session's JOIN line shows in its window; your first line to the developer after that reports it. No order to `<name>` before it.

JOIN, run by every new session after the First steps of [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) (section CLAUDE.md core) and the developer's `go`:

1. Take role, area and lead from your launch prompt, else from `NEXT-SESSION.md`; missing: ask the developer, do nothing else.
2. Read `~/.claude/<lead>/BOARD.md`. Lead and no BOARD: create it from the BOARD template below with your own REGISTER row, `active`. Lead and BOARD exists: Lead handover, step 3.
3. Deputy: append your REGISTER line (template in Orders and reports) to `~/.claude/<name>/REPORTS.md`; never write BOARD.
4. Deputy: read `~/.claude/<lead>/ORDERS.md`; note the orders `to <name>` without a `done` line.
5. Reply in one line: `JOIN <name>, <role>, area <area>, lead <lead>, orders <numbers|none>.`
6. Then act only on the developer's next message or, as deputy, on an order.

## Orders and reports

Order = numbered brief, lead to one deputy, appended to `~/.claude/<lead>/ORDERS.md`; `<#>` counts 1, 2, 3 … across all deputies, never reused. Report = REPORT of [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) (section Talking to the developer), `<item/order #>` = the order number, appended to `~/.claude/<deputy>/REPORTS.md`; in STATUS the item is `O<order #>`. `<stamp>` = `<YYYY-MM-DD HH:MM>` from `date` run this turn.

1. `order <deputy>` (lead): read every REPORTS.md; write the ORDER; show it; after `go` append it to ORDERS.md, BOARD row `open`. Empty Scope = not ready: ask the developer for paths.
2. Deputy, on reading a new order to it: STATUS `O<#> in-progress`, then REPORT `<#>` with `STATUS: in-progress`, `Changed: order <#> accepted`.
3. Deputy works; at each state change STATUS first, then REPORT (`in-progress | blocked | review`). The lead, on reading a REPORT, mirrors its state in BOARD and copies each `Open:` line to Needs you.
4. On `review` the lead runs `verify N` (Cabinet 1) against the basis, the order's `Input` line: `yes | no | contradicted`; result into BOARD Verified. Not `yes`, or the developer says no: the lead appends `note <stamp>: <one line>` under the order, BOARD `in-progress`; the deputy sets STATUS `in-progress` when it reads the note.
5. `yes`: the lead asks the developer "Is this fully solved and checked?" with the evidence. Yes: the lead appends `done <stamp>` under the order, BOARD `done`; the deputy sets STATUS `done` when it reads that line.

ORDER = exactly these 7 lines; under it only the lead appends `note <stamp>: <one line>` and `done <stamp>`:

```
ORDER <#>  to <deputy>  <YYYY-MM-DD HH:MM>
Goal: <one sentence>
Scope: <paths>
Out of scope: <paths or topics>
Context: <decisions made>
Input: <spec, report, diff>
Report: REPORT in your REPORTS.md
```

REGISTER, one line: a deputy's into its REPORTS.md, the lead's into BOARD Sessions:

```
REGISTER <session> | lead|deputy | <area> | <YYYY-MM-DD HH:MM>
```

One writer per file: ORDERS.md the lead only; BOARD.md the lead; REPORTS.md that deputy only; `<repo>/doc/` the owning deputy, never the lead. Only the owner sets a state: the deputy in STATUS, the lead in ORDERS and BOARD.

Direct instructions: a developer message typed into a deputy session is an instruction for its area (sources: [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw), section Rules). Before acting the deputy appends `direct from developer <stamp>: <one line>` to its REPORTS.md. An order that clashes with it: REPORT the clash under `Open:` and wait; the lead never overrides it.

Polling: nothing polls by itself. A deputy reads ORDERS.md at JOIN, at every developer message and on `check`; the lead reads every REPORTS.md on `status`, `check` and before every ORDER. `check` = developer command in any session: read the other side's files now, then update your own.

## BOARD

`~/.claude/<lead>/BOARD.md` = the lead's dashboard, about 40 lines. Summary, not source: ORDERS, REPORTS and STATUS win. `status` in the lead session renders it.

```
# BOARD  Updated: <YYYY-MM-DD HH:MM> by <lead>
## Needs you: <decision + recommendation> | nothing
## Sessions: | Session | Role | Area | active|stale|retired | Last line |
## Orders: | # | Deputy | Goal | State | Verified yes|no|contradicted |
## Requests (People: several): | Id | Direction sent|received | With | open|closed |
## Later: parked steps
```

Needs you = one line per open developer decision with a recommendation, else `nothing`. Last line = first line of that session's newest REPORT or REGISTER. Verified = last `verify` result, empty before one. Requests: only when `People: several`, per [Cabinet 3 – Multi-User](https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM), section Envoy.

Update from files read now, never from memory, after: new ORDER, REGISTER read, REPORT read, `verify` result, developer yes or no, `check`, `status`.

Sessions: `active` → `stale` → `retired`. At each update mark `stale` a deputy whose REPORTS.md has no line newer than 24 h; its orders keep their state; list it under Needs you (wait, re-summon or retire). `retired` only after the developer's yes, or set by a new lead on the old lead's row (Lead handover).

Tidy up: propose `tidy up` when BOARD exceeds 40 lines or ten orders are `done`. List the moves: `done` orders from ORDERS.md to `~/.claude/<lead>/archive/`, `retired` rows out of Sessions, Later trimmed; move after `go`, delete nothing. A deputy moves old REPORTS.md lines to `~/.claude/<deputy>/archive/` on its own `tidy up`.

## Where files live

Rows this doc adds; NEXT-SESSION, scratch and repo `doc/` rows: [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw), section Where files live.

| Kind | Location | Writer | Reader | Rotates |
| --- | --- | --- | --- | --- |
| ORDERS | `~/.claude/<lead>/ORDERS.md` | lead only | deputies | append; `done` → `~/.claude/<lead>/archive/` |
| BOARD | `~/.claude/<lead>/BOARD.md` | lead (via keeper if any) | developer, new lead | overwritten |
| REPORTS | `~/.claude/<deputy>/REPORTS.md` | that deputy only | lead | append; old → `~/.claude/<deputy>/archive/` |
| STATUS | `<repo>/doc/STATUS.md` | owning deputy; never the lead | all | overwritten snapshot |

Read: own repo, own `~/.claude/<session>/`, the lead's and deputies' files in this table; the lead reads a deputy's repo for `verify N` only. Write only what a Writer column (here or in Cabinet 1) assigns to you.

## Lead handover

A lead closes on `adjourn` (Cabinet 1) with one difference: it writes BOARD and NEXT-SESSION only, no `doc/STATUS.md`.

1. On `adjourn`: update BOARD from files read now; write your NEXT-SESSION (Cabinet 1 path) with `Role: lead`, `Lead: me`, Proposed next action `JOIN`, and the last line below. Nothing else; leave your own Sessions row as it is.
2. The developer starts the new lead by hand with a new name, the same directory and `Lead is <lead>` (the name in the BOARD path, kept across handovers; Starting a session); it runs JOIN and, like every lead, writes `Lead: me` in its own NEXT-SESSION.
3. JOIN step 2, BOARD exists: the new lead reads the NEXT-SESSION of the Sessions row `lead`, `active` (`~/.claude/<that name>/`, data), sets that row `retired`, appends its own REGISTER row `active`, then goes on with JOIN step 5.
4. Between `adjourn` and that JOIN, deputies work only on orders already in ORDERS.md and on direct instructions.
5. The new lead runs `verify N` on every `review` order, updates BOARD, then issues orders.

Last line of NEXT-SESSION, lead only, one row per order not `done`, from BOARD:

```markdown
## Lead only: | # | Deputy | Order | State |  ;  Promised but not done:
```

Promised but not done = said to the developer, not yet true in a file.

## Skills

Optional, at `<dir>/.claude/skills/<skill>/SKILL.md` of the session using them, written by the developer; no step above needs one; a skill acts only after that step's `go`.

| Skill | Does |
| --- | --- |
| `spawn` | summon step 4: opens the window or pane and runs the shown command |
| `tmux` | same via tmux; lists panes, reads a screen, stops one |
