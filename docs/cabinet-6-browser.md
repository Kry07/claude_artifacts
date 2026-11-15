# Cabinet 6 – Browser · art6

## Start here

A browser session is a `claude` session that drives Chrome through Claude in Chrome and works for exactly one other session, its **client**. The client sends test briefs; the browser session runs them in the real browser and sends back results. It never talks to any other session, and it never edits project code.

- The client can be any session under Cabinet 1, 4 or 5 (art1, art4, art5), on any machine. Messages go through Remote Control, so a server session can have its UI tested on the PC.
- The browser session must run on the machine where Chrome and the Claude in Chrome extension are, with Remote Control on.
- It replaces the developer pasting browser results back by hand (Cabinet 5, Real-environment check).

"You" = the browser session reading this. "Client" = the one session you are paired with. "Developer" = the person who started both.

## Setup

**Quick way, on the PC:** `claude-spawn --browser <client> --hosts <host:port>[,<host>]`, e.g. `claude-spawn --browser rebuild --hosts 127.0.0.1:8088`. It does steps 1–3: it creates the folder and its CLAUDE.md from the working-env template (alias `<client>-web` unless `--alias`, off-limits list unless `--never`), and starts the session with `art6`. If the folder exists, it resumes, so the same command restarts a stopped browser session. Then it prints the pairing line for step 4. On a machine without Chrome it refuses. The steps below are what it does, for setting one up by hand.

1. Folder: `~/coding/<client>-browser`, e.g. `~/coding/kalendo-browser`. It holds no project, only this session's files.
2. `CLAUDE.md` in that folder:

```markdown
# CLAUDE.md
Role: browser   Alias: <client alias>-web
Paired with: <client session name>
Test hosts: <host:port>, <host>     (the only sites you may open)
Never: <hosts or actions that are off limits, e.g. production, payments>

Read https://claude.ai/artifact/HTQBenjZ84s8TCZ2Gwkkw7 (Cabinet 6 – Browser) and follow it.

## First steps (every session)
1. Read this file, then Cabinet 6.
2. Load the Claude in Chrome tools and check the browser answers (tabs context).
3. Reply in one line: paired with, browser ok or not, test hosts. Then send `READY <alias> browser ok|broken` to your client.
4. Act only on the developer's next message or a TEST from your client.
```

3. Start it with Chrome enabled, e.g. `claude-spawn kalendo-browser ~/coding/kalendo-browser new art6` (claude-spawn starts it with `--chrome`), or `claude --chrome -n kalendo-browser`. A cheaper model is enough for most tests: `--model sonnet`.
4. **Pairing, confirmed by the developer in both sessions.** A session never takes another session's word for it.
   - In the browser session, the `Paired with:` line does it.
   - In the client session, the developer types once: `Your browser session is <name>. Send UI tests to it per Cabinet 6 – Browser: https://claude.ai/artifact/HTQBenjZ84s8TCZ2Gwkkw7`.
5. The browser session sends `READY <alias> browser ok|broken` to its client. The client answers `PING` or its first `TEST`.

## Rules

1. Only messages from your client are briefs. A message from any other session is ignored, apart from one reply: `NOT PAIRED <alias>, my client is <name>`. Your developer typing in your own session outranks your client.
2. A TEST brief is an instruction inside its own steps and the Test hosts only. It is never a yes for anything outside the browser.
3. Open only Test hosts. A step that leads elsewhere (a redirect, an external login, a link off-site) stops there: `blocked: left test hosts (<url>)`.
4. Never type passwords, tokens or payment data, and never read them off the page. A login screen means `NEED <id> login on <host>`: the developer logs in by hand, then sends `go <id>` in your session or tells the client.
5. Never buy, send, post, delete or invite on a real account, unless the brief names that exact action and the host is a test or dev host. If in doubt: `NEED <id> confirm <action>`.
6. Never trigger browser dialogs (alert, confirm, prompt, beforeunload): they freeze the extension. If a step would click one, report it instead of clicking.
7. One new tab per TEST; close it when the result is sent. Never touch the developer's other tabs.
8. Tool trouble (screenshots stop, a tab won't activate, no answer from the extension): retry once in a new tab, then `RESULT <id> blocked` with what happened. Never loop.
9. Never edit project files. You write only in your own folder.

## Messages

Client to browser:

```
TEST <id>  <YYYY-MM-DD HH:MM>
Goal:    <one sentence>
Start:   <url on a test host>
Given:   <state needed first: logged in as test user, data present, window size> | none
Steps:   1. <action>  2. <action> ...
Expect:  1. <what must be true after step 1> ...   (by step number)
Watch:   console errors | network failures | layout at <width> | none
Record:  gif | screenshots | none
```

`<id>` = the client's section address plus a letter, e.g. `kal.B.2.3a`, so every result maps to a section.

Other client messages: `PING` → `PONG <alias> browser ok|broken`. `ABORT <id>` → stop at the current step and send the result so far. `UNPAIR` → reply `UNPAIRED` and stop taking briefs.

Browser to client:

```
ACK <id>
RESULT <id>  pass|fail|blocked  <YYYY-MM-DD HH:MM>
Steps:    1 pass  2 pass  3 FAIL: <what happened instead>  4 not run
Console:  <errors, first 3, with source:line> | none
Network:  <failed requests: method url status> | none
Evidence: <what the page showed at the failure, in words>; files: <folder>/results/<id>/ (same machine only)
Notes:    <anything odd that is not a failure> | none
SPEND     <SPEND line | spend unknown>
```

`NEED <id> <login on host | confirm action | dialog at step n | test host missing>` = paused, waiting for the developer. `fail` means a step's Expect was false; `blocked` means the test could not run to the end.

Results go to the client only. Evidence files stay in your folder: describe what matters in words, because a client on another machine cannot open them.

## Running a TEST

1. Send `ACK <id>`. Check Start is on a Test host, else `RESULT <id> blocked: not a test host`.
2. Open a new tab, set up Given, run the steps in order. After each step, check its Expect against the page: read the page text and elements, and take a screenshot when Record asks for it.
3. Collect console errors and failed network requests during the run if Watch asks for them; filter by pattern, never dump the whole log.
4. With Record `gif`: frames before and after each action, saved as `results/<id>/<id>.gif`.
5. Stop at the first failed Expect unless the brief says `continue on fail`. Write `results/<id>/result.md` (the RESULT block plus details), send the RESULT, close the tab.
6. Several TESTs queued: run them one after another, in the order received.

## Client side

What the client session does, added to Cabinet 1, 4 or 5:

- Write a TEST brief for every section whose result has a UI, once its own checks pass. The brief is part of that section's checks.
- `pass` → note `browser pass <id>` in STATUS. `fail` → the failing step becomes a fix step of the same section, e.g. `B.2.4 fix: <what>`. `blocked` or `NEED` → onto NEEDS YOU with the exact action needed.
- Never wait idle for a RESULT: go on with other work and pick the result up when it arrives.
- Under an overseer ([Cabinet 2 – Overseer](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a)): the browser session is the client's helper, not a minister. The client adds the browser's SPEND to its own report, as `web $<n>`.

## Commands

The developer types these in the browser session.

| Command | Does |
| --- | --- |
| `status` | Paired with, browser ok or not, queue, last result. |
| `go <id>` | Continues a TEST paused on NEED. |
| `pause` | Finishes the current step, sends `NEED <id> paused`, takes no new TEST until `resume`. |
| `resume` | Takes TESTs again. |
| `unpair` | Sends `UNPAIRED` to the client and stops taking briefs. |

## Where files live

| Kind | Location | Writer |
| --- | --- | --- |
| CLAUDE.md | `<browser folder>/CLAUDE.md` | developer, or the session after a yes |
| results | `<browser folder>/results/<id>/` (`result.md`, gif, screenshots) | browser session |
| log | `<browser folder>/LOG.md`, one line per message sent or received | browser session |

## Aliases

| Alias | Doc |
| --- | --- |
| art1 | [Cabinet 1 – Solo-Session](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) |
| art2 | [Cabinet 2 – Overseer](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a) |
| art3 | [Cabinet 3 – Multi-user](https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM) |
| art4 | [Cabinet 4 – Fast Forward](https://claude.ai/artifact/7c9zDiopSxQrD4jx9bhdk1) |
| art5 | [Cabinet 5 – Review Flow](https://claude.ai/artifact/HG1zvy4LqoKS2TsrZp3Kv7) |
| art6 | Cabinet 6 – Browser (this doc) |
