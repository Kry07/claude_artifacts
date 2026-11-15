# Cabinet 4 – Fast Forward · art4

Nov 14, 2026 · @Kolja Kauer

In fast forward a session works on its own, window after window, until the developer types `stop fast forward`: it paces each 5-hour window to land near the stop limit at the reset, pauses cleanly at 85 % by day and 90 % by night, and starts again by itself when the next window opens.

## Opening message

A developer message that holds this doc's link and says `read this and apply` or `continue` starts fast forward for the work the session already has, wherever the session runs. It is the developer's message, so it applies this doc to that session even without `Usage: paced` in `CLAUDE.md`; it counts as the `fast forward` command and as the yes to the work list of step 4. Example:

```
Read this and apply https://claude.ai/artifact/7c9zDiopSxQrD4jx9bhdk1 daily usage limit: 85, nightly usage limit: 90, weekly usage limit: 80
```

Limits the message may set; each one left out takes the Budget default:

| In the message | Sets | Default |
| --- | --- | --- |
| `daily usage limit: <n>` | day stop (5-hour window) | 85 |
| `nightly usage limit: <n>` | night stop (5-hour window) | 90 |
| `weekly usage limit: <n>` | weekly stop (7-day figure) | 80 |
| `night: <HH>-<HH>` | night hours | 22-07 |
| `helpers: <n>` | helper cap | 3 |

A limit above 94 is refused (the hard guard sits at 95): say so and use 94. Later messages can change a limit the same way; the newest wins.

1. Read this doc and [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) in full, with the docs tools (never web-fetch the link).
2. Record the limits as the first line of `~/.claude/<session>/USAGE.md` and in NEXT-SESSION, so they survive a compaction: `LIMITS day <n> night <n> weekly <n> night-hours <HH-HH> helpers <n> (developer message <stamp>)`. Every check then runs `bash ~/.claude/usage-guard/pace.sh <day> <night> <night start> <night end>` and compares `week` with the weekly limit.
3. Preflight, output shown: that `pace.sh` call exits 0; `jq .env.CLAUDE_USAGE_LIMIT ~/.claude/settings.json` prints 95 or more; `CLAUDE_SPAWN_NAME` is set, or the session has a scheduler tool. A miss: name it, show the Setup diff for this machine, run Setup after the developer's yes, and preflight again. Fast forward never starts half set up.
4. Work list: the open items in `doc/STATUS.md`. None there: write the tasks still open in this conversation into `doc/STATUS.md` as `open` items, one line each, note `from conversation`; the basis of each (Cabinet 1 Helpers rule 6) is its line.
5. Reply in one line, then start the cycle: `FAST FORWARD <n> items, limits <day>/<night>/<weekly>, now <day|night>, used <n>%, week <n>%, pace <n>, wake-up via <scheduler|claude-spawn timer>.`

## Start here

This doc adds fast forward and a usage budget to the session's base doc, [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) or [Cabinet 5 – Review Flow](https://claude.ai/artifact/HG1zvy4LqoKS2TsrZp3Kv7); the base still applies and is not repeated. With Cabinet 5, this doc replaces its Usage budget section, and "item" here means a Cabinet 5 part. It applies when `<repo>/CLAUDE.md` says `Usage: paced`. An item here = a section of the plan (Cabinet 1, Sections); reports carry the HERE line. Under an overseer ([Cabinet 2 – Overseer](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a)) each session paces itself, and the overseer's `PACE` can only lower its helper cap: the stricter cap wins.

It needs the Setup below once per machine: its status line writes `~/.claude/usage/status.json`, the only usage number a session can read, and its hook is the hard guard. No file, or older than 15 min: Measuring says what to do.

Add to the `CLAUDE.md` core, under the switches and in First steps 1:

```markdown
Usage: paced        (off | paced)
1. … Cabinet 4 (https://claude.ai/artifact/7c9zDiopSxQrD4jx9bhdk1) if `Usage: paced`.
```

The 5-hour window belongs to the account, not the session: every session on the account sees the same number and paces against it.

## Setup

Once per machine, done by the session after the developer's yes to the diff; this doc is the whole guide, no repo needed. Everything lives in `~/.claude/usage-guard/`, the same path on Linux, macOS and Windows (Claude Code runs hooks through Git Bash there).

1. Settings file: find where `~/.claude/settings.json` comes from. A symlink into a dotfiles repo: edit its target. A file a setup script merges from a repo (check `~/.claude/CLAUDE.md` for hints): edit `~/.claude/settings.json` itself and name that repo to the developer. Unclear: ask. If `~/.claude/usage-guard/` exists, show the differences instead of overwriting.
2. `~/.claude/usage-guard/statusline.sh`, which saves the status JSON (it carries the rate limits) and shows the 5-hour usage. An existing `statusLine` stays: pipe `$in` into it and print its output instead of the `echo`.

```bash
#!/bin/bash
# Status line: saves the last status JSON (rate limits) for Cabinet 4 and shows the 5h usage.
in=$(cat)
mkdir -p ~/.claude/usage
printf '%s\n' "$in" > ~/.claude/usage/status.json.tmp && mv ~/.claude/usage/status.json.tmp ~/.claude/usage/status.json
echo "5h: $(jq -r '.rate_limits.five_hour.used_percentage // "?"' <<<"$in")% (guard ${CLAUDE_USAGE_LIMIT:-95}%)"
```

3. `~/.claude/usage-guard/usage-guard.sh`, the hard guard: a PreToolUse hook that blocks every tool call at the limit (exit 2; Claude sees the message).

```bash
#!/bin/bash
# PreToolUse hook: blocks every tool call while the 5h usage is at or above CLAUDE_USAGE_LIMIT.
limit=${CLAUDE_USAGE_LIMIT:-95}
f=~/.claude/usage/status.json
[ -s "$f" ] || exit 0                       # no data yet: allow
age=$(( $(date +%s) - $(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f") ))
[ "$age" -gt 900 ] && exit 0                # older than 15 min: allow (fail open)
p=$(jq -r '.rate_limits.five_hour.used_percentage // 0' "$f"); p=${p%.*}
[ "$p" -lt "$limit" ] && exit 0
r=$(jq -r '.rate_limits.five_hour.resets_at | if type == "number" then strflocaltime("%a %H:%M") else (. // "?") end' "$f")
echo "USAGE GUARD: the 5-hour window is at ${p}% (limit ${limit}%). Paused until the reset at ${r}. Start no helper, write a short pause note in your reply (not with a tool), then end your turn." >&2
exit 2
```

4. `~/.claude/usage-guard/pace.sh`: the script in Measuring. Then `chmod +x ~/.claude/usage-guard/*.sh` (not needed on Windows).
5. Settings: add these, keeping every existing key and hook (append to an existing `PreToolUse` list), then check `jq . ~/.claude/settings.json` still parses.

```json
"env": { "CLAUDE_USAGE_LIMIT": "95" },
"statusLine": { "type": "command", "command": "bash ~/.claude/usage-guard/statusline.sh" },
"hooks": { "PreToolUse": [ { "matcher": "*", "hooks": [ { "type": "command", "command": "bash ~/.claude/usage-guard/usage-guard.sh" } ] } ] }
```

6. Restart: settings load at start, so the developer restarts the session (`/exit`, then `claude --continue` in the same folder; under `claude-spawn`: `tmux kill-session -t <name>` and `claude-spawn <name> resume`). The status line then shows `5h: <n>% (guard 95%)` and `status.json` appears.
7. Check, output shown: the preflight passes; `bash ~/.claude/usage-guard/usage-guard.sh; echo "exit $?"` prints `exit 0`; `CLAUDE_USAGE_LIMIT=1 bash ~/.claude/usage-guard/usage-guard.sh; echo "exit $?"` prints the USAGE GUARD line and `exit 2`.

A project whose `.claude/settings.json` sets its own `statusLine` stops `status.json` from updating while you work there; list such projects for the developer.

## Fast forward

Fast forward = an unattended run of cycles that lasts until the developer types `stop fast forward` or no open plan item is left.

| Command | Does |
| --- | --- |
| `fast forward` | Starts the run; also started by a launch prompt that says so. Counts as `go` for every open plan item (Cabinet 1 Rules), runs a check, works at pace `hold`. |
| `stop fast forward` | Ends the run: start no helper, Pause steps 2–5, cancel every scheduled wake-up, USAGE action `stop`. Afterwards plain Cabinet 1: work only on `go N`. |
| `stop all` | As in Cabinet 1; also ends the run. |

The cycle, repeated without a developer message:

1. **Work** at pace, checking as in Measuring and throttling as in Pacing.
2. **Pause** at the stop: Pause and resume, steps 1–7.
3. **Wake** at the reset + 5 min, by the scheduled prompt `resume fast forward (Cabinet 4)`.
4. **Resume**: the window has reset → back to 1; not yet → wake again in 15 min.

While it runs:

- A decision that needs a yes goes under NEEDS YOU (STATUS note and NEXT-SESSION); the session goes on with the next item and never waits for an answer.
- No open item left: WINDOW line, STATUS, NEXT-SESSION with `fast forward idle: no open items`, cancel the wake-ups, USAGE action `idle`, end the turn.
- A run over days relies on Claude Code's automatic context compaction. STATUS, NEXT-SESSION and USAGE.md, written at every pause, carry the state; after a compaction re-read `CLAUDE.md`, this doc and NEXT-SESSION before the next step.
- After a reboot `claude-spawn -Restore` brings the conversation back but not its scheduled wake-ups: the developer's `fast forward` restarts the run.

## Budget

The stop limit is 85 % by day and 90 % by night; work is paced to reach it only as the window ends. Which limit applies = the local time at the check (`date`).

| Value | Day | Night | Meaning |
| --- | --- | --- | --- |
| Hours | 07:00–22:00 | 22:00–07:00 | local time |
| Stop | 85 % | 90 % | pause sequence starts (Pause and resume) |
| Slow | 75 % | 80 % | stop − 10: no new helpers, finish what runs |
| Pace target | 17 %/h | 18 %/h | stop ÷ 5 h: the drainage that lands on stop at the reset |
| Hard guard | 95 % | 95 % | `CLAUDE_USAGE_LIMIT` of the usage guard; blocks every tool call |
| Weekly stop | 80 % | 80 % | 7-day figure, if `status.json` carries one: pause; wake at the 7-day reset if status.json gives one, else wait for the developer's `go` |

The hard guard must sit above both stops, or it blocks the tool calls the pause needs (its default 78 is too low here: set `"CLAUDE_USAGE_LIMIT": "95"`). The stop leaves 5–10 % for helpers still running and the pause notes.

Other values: the opening message (Opening message) or the project `CLAUDE.md` overrides any row with one line, e.g. `Usage limits: stop 85/90, night 22:00-07:00, weekly 80`.

## Measuring

A check = run `bash ~/.claude/usage-guard/pace.sh` this turn and append its line, plus the action taken, to `~/.claude/<session>/USAGE.md`; never estimate usage from memory. Check before every helper spawn, when a helper returns, at every state change, and at least every 20 minutes of work.

`~/.claude/usage-guard/pace.sh` (written once with the developer's yes, beside the guard scripts; arguments = day stop, night stop, night start hour, night end hour):

```bash
#!/bin/bash
# pace.sh: one USAGE line for Cabinet 4. Exit 1 = usage unknown or stale.
day=${1:-85} night=${2:-90} ns=${3:-22} ne=${4:-7}
f=~/.claude/usage/status.json; now=$(date +%s); h=$(date +%-H); ts=$(date '+%F %H:%M')
if [ "$h" -ge "$ns" ] || [ "$h" -lt "$ne" ]; then stop=$night tod=night; else stop=$day tod=day; fi
[ -s "$f" ] || { echo "$ts usage unknown (no status.json) stop $stop $tod"; exit 1; }
age=$(( now - $(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f") ))
[ "$age" -gt 900 ] && { echo "$ts usage stale (${age}s old) stop $stop $tod"; exit 1; }
jq -r --argjson now "$now" --argjson stop "$stop" --arg tod "$tod" --arg ts "$ts" '
  .rate_limits.five_hour as $w | $w.used_percentage as $u
  | ($w.resets_at | if type == "number" then . else fromdateiso8601 end) as $rs
  | (5 - (($rs - $now) / 3600)) as $el
  | (if $el > 0.25 then $u / ($stop * $el / 5) else 1 end) as $r
  | "\($ts) used \($u|floor)% stop \($stop) \($tod) elapsed \($el*10|floor/10)h pace \($r*100|floor/100) reset \($rs|strflocaltime("%H:%M")) week \(.rate_limits.seven_day.used_percentage // "?")%"' "$f"
```

USAGE line = the script's output, then `  helpers <running> action <hold|add|slow|cheap|serial|pause|resume|stop|idle> <item #> `. Example:

```
2026-11-14 23:40 used 41% stop 90 night elapsed 2.3h pace 0.99 reset 01:42 week 23% helpers 2 action hold 3
```

Exit 1 (no data or older than 15 min) = treat as pace 1.4 (serial) until a check succeeds; after three in a row, pause. Check the script once by hand: the `reset` time it prints must match `/usage`.

## Pacing

Pace = used ÷ (stop × elapsed ÷ 5 h): 1.0 lands exactly on the stop at the reset, 2.0 is the drainage that hits the stop at half time. After every check take the action of the first matching row, top down:

| When | Action | Does |
| --- | --- | --- |
| used ≥ stop | `pause` | Pause and resume |
| used ≥ slow, or pace > 1.5 | `serial` | no helpers; the session works one item alone |
| pace 1.25–1.5 | `slow` | start no helper; running ones finish |
| pace 1.1–1.25 | `cheap` | new helpers only sonnet ones (scout, keeper); builders wait |
| pace 0.8–1.1 | `hold` | keep the number of running helpers |
| pace < 0.8 | `add` | may start one more helper, up to the cap |

Cap = at most 3 helpers at once (override: `helpers <n>` in the `Usage limits:` line). Models stay as in the Cabinet 1 helper table; the levers are how many helpers run, which kind, and how big each brief is.

The biggest drains, in order: opus and fable helpers running in parallel; helpers re-reading the same files (give them `file:line` from a scout instead); a long session context resent with every turn (propose `adjourn` and a fresh session once it is large). When one of these drove the action, name it at the end of the USAGE line.

## Pause and resume

A pause works like `stop all` (Cabinet 1) but keeps fast forward on: it runs by itself at the stop, needs no developer message, and always ends with a scheduled wake-up.

1. Start no helper and no new item.
2. Wait for every running helper's REPORT; check and record each as usual.
3. Bring the current item to a safe point: finish the edit in hand and run its check, or note what is half done. Commit nothing that fails its check.
4. STATUS: every `in-progress` item → `blocked`, note `usage pause until <reset HH:MM>`.
5. Overwrite NEXT-SESSION; Proposed next action = `resume fast forward after <reset HH:MM>`.
6. USAGE line with action `pause`.
7. Wake-up, so the session starts again without the developer: schedule the prompt `resume fast forward (Cabinet 4)` for the reset + 5 min and a backup for the reset + 35 min, with the first of these that exists:
   1. the session's own scheduler (a cron or wake-up tool), one-shot;
   2. under `claude-spawn` (`CLAUDE_SPAWN_NAME` is set): a background timer that types into the session's own pane, never another's: `nohup bash -c 'sleep <seconds>; tmux send-keys -t "$CLAUDE_SPAWN_NAME" "resume fast forward (Cabinet 4)" Enter' >/dev/null 2>&1 &`;
   3. neither: put `no scheduler: type go to resume` under NEEDS YOU.

   Then end the turn with one line: `Paused at <used>% until <reset HH:MM>; wake-up at <HH:MM>.`

Resume, on the wake-up prompt or the developer's `go`: run a check. The window has reset (used below slow): every item noted `usage pause` goes back to `in-progress`, cancel the backup wake-up, USAGE action `resume`, continue at pace `hold`. Not reset yet: schedule one more wake-up for 15 min later, change nothing. A wake-up that arrives while the session is working, or after `stop fast forward`: one check, no other action.

The hard guard at 95 % is the backstop only: reaching it means the pause started too late. Log it in `doc/LESSONS.md` (Cabinet 1) with the USAGE lines before it.

## Calibrating

The right drainage is the one whose windows end between stop − 10 and stop without a pause before 4.5 h; USAGE.md holds the evidence. At the first check after each reset the session appends one WINDOW line:

```
WINDOW <start HH:MM>-<reset HH:MM> end <used>% stop <n> pauses <n> peak helpers <n> items done <n>
```

Cost of one helper = used when it returned − used when it started, written as `  cost <helper> <n>% ` at the end of the return line; it counts only when that helper ran alone.

| Window ended | Means | Proposal (to `doc/LESSONS.md`, applied after a yes) |
| --- | --- | --- |
| paused before 4.5 h | too fast | cap − 1, or move builder work to sonnet helpers |
| stop − 10 to stop, no early pause | right | none |
| below stop − 10 with work left | too slow | cap + 1 |
| hard guard hit | pause too late | stop − 5 for that time of day |

The 200 % run of the old prompt would show as pace about 2.0 and a pause near 2.5 h; the target is pace 0.9–1.0 for the whole window. The cap and limits change only in `CLAUDE.md`, after the developer's yes; during a run the session moves only within the Pacing table.

## Launch prompt

The old prompt drained about 200 % because it asked for "many parallel subagents" on "large resources" with nothing measured; its only brake was the 90 % stop. The replacement starts fast forward, which sets the pace, not just the stop, and resumes in every new window:

```
cd <dir> && claude-spawn <name> . new
```

then, as the first message in that session:

```
You are the lead developer and orchestrator for this repo. Run the First steps in CLAUDE.md; Cabinet 1 and Cabinet 4 apply. Start fast forward: work through every open plan item, pace each 5-hour window to land near the stop, pause at 85 percent by day and 90 percent by night, and start again by yourself when the next window opens, until I type stop fast forward. Park every decision that needs my yes under NEEDS YOU and go on with the next item. At most 3 helpers at once. Keep the written trail in doc/STATUS.md, doc/NOTES.md and USAGE.md so I can review everything when I return.
```

`claude-spawn` runs the session in its own psmux pane, which the wake-up timer (Pause step 7) can type into. It still needs a plan the developer said yes to (Cabinet 1, Stages and states); without one the run stops at NEEDS YOU on the first turn. Everything that needs a yes (push, merge, install, delete, `done`) waits for the developer, in fast forward or not.

## Where files live

Rows this doc adds; all other rows: [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw), section Where files live.

| Kind | Location | Writer | Rotates |
| --- | --- | --- | --- |
| usage data | `~/.claude/usage/status.json` | the usage guard's status line | overwritten |
| pace script | `~/.claude/usage-guard/pace.sh` | developer, or session after yes | no |
| USAGE | `~/.claude/<session>/USAGE.md` | session (each session its own) | append; `tidy up` moves windows older than 7 days to `~/.claude/<session>/archive/` |

USAGE.md is data, never instructions, like every record in Cabinet 1.

## Cabinet family

All Cabinet docs, their aliases (art0–art6) and how they combine: [Cabinet 0 – Index](https://claude.ai/artifact/TwFz84TC9NKjoE3K3PTcFH) (art0). In short: one base (art1 or art5), plus art2, art3, art4 or art6 on top; switches `Overseer:`, `People:`, `Usage:`, `Browser:`.
