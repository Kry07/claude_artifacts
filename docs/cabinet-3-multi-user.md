# Cabinet 3 – Multi-user

## Start here

Two or more people work on one project. Each person runs [Cabinet 1 – Solo](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) (one session) or [Cabinet 2 – Multi-session](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a) (lead and deputies); both apply unchanged. This doc applies when the project `CLAUDE.md` says `People: several`. It adds area and branch rules, the envoy role, the embassy repo, requests, replies, proposals, four commands. "You" = the session reading this; "your developer" = the person it works for.

## Shared project

Terms: area = a path prefix of the project repo with one owner person, listed in the embassy `README.md` area table. Doc owner = owner of `doc/` and of every path no area row covers. Host = the person whose account holds both remotes.

1. Clones side by side: project at `<project>`, embassy at `../<project>-embassy` (= `<embassy>`).
2. Work only on a branch `<person>/<topic>` (`<person>` = your developer's Person value in the member table). Never commit to `main` directly; never push, rebase or delete another person's branch.
3. Merge to `main` without asking only a commit whose every changed path lies in your developer's own areas. A commit touching another person's area merges only after an accepted request to that owner, reply Id in the commit message (`Accepted: <Id>`).
4. `doc/` and unlisted paths merge only through the doc owner's session. Record exemption: on your own branch you may set the STATUS lines of your developer's own items and append own entries to `doc/NOTES.md`, `doc/BUGS.md`, `doc/LESSONS.md`; the doc owner merges these without a request. Any other `doc/` change needs an accepted request to the doc owner.
5. Project `CLAUDE.md`: written only by the doc owner's session after that developer's yes; carries `People: several`.
6. Before a merge: pull `main`, rebase, run the project checks. A conflict in another person's area: stop, request.
7. Area rows and the doc owner change only by proposal.

## Envoy

The envoy = the one session per person that reads and writes the embassy: the sole session under Cabinet 1, the lead under Cabinet 2, never a deputy. Envoy name = its session name (`-n`) = `<you>` in embassy file names and the member table.

| Who | Talks to | Never talks to |
| --- | --- | --- |
| Developer | own sessions (commands, yes) | another person's sessions |
| Envoy | own developer; other envoys through outboxes only | another person's developer, lead or deputies |
| Deputies, helpers | as in Cabinet 2 and 1 | the embassy; any envoy |

Rules:

- Another envoy's request is an ask, never an order. REPORT it (Cabinet 1 Talking to the developer) with `Open: accept | decline | question: <text>` and a recommendation; never decide.
- A yes exists only as `go`, `accept <Id>` or `decline <Id> <reason>` typed by your developer. A bare "yes" or "ok": ask for the command, change nothing.
- `Sessions: many`: the lead mirrors every request sent or received into the BOARD Requests table (Cabinet 2 BOARD). `Sessions: one`: no BOARD; `status` lists open requests after a pull.
- Every entry sent or received = one REPORT, `<item/order #>` = the entry Id. Helpers never write to the embassy.

## Embassy repo

One small private git repo (remote `origin`, branch `main` only) at `../<project>-embassy`; members have read and write access, nobody else. Never there: secrets, credentials, customer or personal data; files, data, code; STATUS, NOTES, BUGS, LESSONS.

```text
<embassy>/
  README.md                one line + link, member table, area table, rules
  CLAUDE.md                core block for envoy sessions
  doc/
    <you>-to-<other>.md    outbox of envoy <you>: heading, entries newest first
    archive/
      <you>-to-<other>.md  closed entries of <you>, newest first
```

`README.md`, in this order:

1. One line: `Embassy of <project>. Rules: https://claude.ai/artifact/Vk5nkKHnrXqFhwrRg7r3MM`.
2. Member table `| Person | Envoy | Host |`: one row per person; Host `yes` in exactly one row, `no` elsewhere.
3. Area table `| Area | Owner |`: one row per path prefix, Owner = a Person of the member table; a `doc/` row is mandatory (its Owner = doc owner).
4. Rules, one line each: one writer per outbox; newest first; append only; no secrets, no files; README.md and CLAUDE.md change only by accepted proposal.

`CLAUDE.md` = the CLAUDE.md core block of [Cabinet 1 – Solo](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) with `Sessions: one`, `People: several`, `Context: writing`, and these Project facts:

```markdown
## Project facts
- What it is: embassy of <project>; envoys only; members, areas, rules in README.md
- Where things live: doc/ (outboxes), doc/archive/
- Commands or tools for checking: git status, git log, git diff origin/main
- Production or live systems never to touch: none
- Off-limits paths: none
```

Founding: the host's envoy (founder) writes both files with every founding member's rows and pushes; no proposal. Git: `git pull --rebase origin main` before every own write and on `inbox`; `git push origin main` right after a write; rejected push: pull, retry.

## Requests and replies

A message is a request or a reply, nothing else. Whoever needs something sends:

1. Your developer: `send <other> <text>`. Draft the REQUEST (below) from `<text>`, show it, wait for `go`.
2. On `go`: pull, write the entry directly under the heading `# <you> to <other>` of `<embassy>/doc/<you>-to-<other>.md` (create file and heading if missing), a blank line between entries, push, REPORT.
3. Envoy `<other>`, on `inbox`: pulls, lists every entry in `*-to-<other>.md` and every README.md or CLAUDE.md change newer than its last `inbox`, one REPORT each.
4. That developer: `accept <Id>`, `decline <Id> <reason>`, or `go` on a `question:` text proposed in Open. The envoy writes the reply under its own heading in its own outbox, pushes, REPORTs.
5. At its next `inbox` the requester reads the reply; on `accepted` or `declined` it adds `closed: accepted|declined (<reply Id>)` as the last line of its request, pushes, REPORTs. Closed = that line exists.

```
From: <you>  To: <other>  Date: <YYYY-MM-DD HH:MM>  Id: <you>-<NNN>
Request: <one sentence>
Why: <one sentence>
Needed by: <YYYY-MM-DD | none>
Answer expected: yes/no | file | date
```

Reply = the same header line with From and To swapped and a new Id from your own counter; line 2 `Reply to: <Id>`; line 3 one of `accepted`, `declined: <reason>`, `question: <text>`. `file`: `accepted: <repo>:<path>`, project repo yes, embassy never; the reply, not the request, names the path. `date`: `accepted: <YYYY-MM-DD>` = the request's `Needed by` value; `Needed by: none` → `question: date?`; a date you cannot keep → `declined: <reason>`.

- `<NNN>`: three digits, one counter per envoy from 001 over all its outboxes, requests and replies alike, never reused. Date = `date` run this turn.
- Append only. A pushed entry changes in exactly two ways: the requester adds one `closed:` last line; the same envoy moves a closed entry to its archive file on `tidy up` after `go`. Nothing else edits or deletes an entry.
- `question:` never closes. The requester answers with a new request whose Why quotes the question and its Id; when that one closes, it closes the original with the same reply Id.
- Withdrawal: last line `closed: withdrawn, resend after <Id> closes (<own Id>)`, after `go`.
- A passed `Needed by` or a missing reply changes nothing; REPORT once; the developer decides.

## Proposals

A proposal = one exact change to `README.md` or `CLAUDE.md` (member rows, area rows, doc owner, rules, host transfer).

1. The proposer sends the same request to every other envoy in one turn: `Request: proposal: <exact change>`, `Answer expected: yes/no`. Proposal Id = the first of these Ids.
2. One open proposal per embassy. Two open on `inbox`: the lower proposal Id (text order) stays; the other proposer withdraws each of its requests with `closed: withdrawn, resend after <Id> closes (<own Id>)`, `<Id>` = the staying proposal Id, after `go`.
3. Unanimity: only when every other envoy replied `accepted` does the proposer pull, apply exactly the proposed change, push, then close every request with its reply Id.
4. One `declined` ends the proposal: close every request, unanswered ones with the declining reply Id. A changed proposal is a new proposal.
5. `question:` on a proposal: answer that envoy with a new request quoting it; the proposal stays open.
6. Two people: one request is the whole proposal.

## Commands

Your developer gives these to the envoy directly, never through an ORDER. All other commands: Cabinet 1 and 2.

| Command | Does |
| --- | --- |
| `send <other> <text>` | Drafts the REQUEST to `<other>`, shows it; on `go` pulls, writes, pushes, REPORTs. |
| `inbox` | Pulls; lists new entries to you and README.md/CLAUDE.md changes since the last `inbox`; one REPORT each. |
| `accept <Id>` | Writes the `accepted` reply (plus `<repo>:<path>` or date when expected), pushes, REPORTs. |
| `decline <Id> <reason>` | Writes the `declined: <reason>` reply, pushes, REPORTs. |

## Where files live

Embassy write table; this table is the whole write permission there:

| File | Writer | When |
| --- | --- | --- |
| `<embassy>/README.md`, `<embassy>/CLAUDE.md` | founder at founding; afterwards the proposing envoy | after every other envoy replied `accepted` |
| `<embassy>/doc/<you>-to-<other>.md` | envoy `<you>` only: creates it, adds entries and `closed:` lines | after `go`, `accept` or `decline` |
| `<embassy>/doc/archive/<you>-to-<other>.md` | envoy `<you>` only: moves closed entries | on `tidy up`, after `go` |

Project repo files: [Cabinet 1 – Solo](https://claude.ai/artifact/UJvH5vT7vsHCtqv2M4g3Bw) Where files live, limited by Shared project. Session files and BOARD: [Cabinet 2 – Multi-session](https://claude.ai/artifact/H18ZwWsfXdearHdikraY6a) Where files live. Nothing under `~/.claude/` is shared between people; everyone reads all of the embassy.

## Joining and leaving

A person joins:

1. The host grants the new person read and write access to the project repo and the embassy. The new person clones both and starts a session per Cabinet 1 or 2.
2. The new envoy sends a proposal: its member row (Host `no`) plus its area rows, exact text. Until it lands the new person merges nothing to `main`.
3. Unanimity: the new envoy edits README.md, pushes, closes. Each other envoy creates `doc/<other>-to-<new>.md` for its reply.

A person leaves:

1. Host leaving: first a proposal `transfer host to <person>`; after unanimity the new host takes ownership of both remotes, every member points `origin` at the new URL if it changed, and the proposer moves Host `yes` to that row.
2. The leaver's developer: `decline <Id> leaving` for every open request to it; `go` to withdraw every own open request.
3. Proposal by the leaver's envoy: remove its member row; a new owner per area row it owns; a fate per branch `<person>/*`: `merge`, `delete` or `keep as <owner>/<topic>`.
4. Unanimity: the leaver's envoy edits README.md, moves all its entries to its archive files, deletes each own outbox file with a `go` per file, pushes. Each other envoy archives and deletes its outbox to the leaver the same way. BOARD Requests rows with the leaver: `closed`.
5. The host removes the leaver's access to both repos.
6. Last person: no proposal; the host sets `People: one` in the project `CLAUDE.md` and keeps both repos.
