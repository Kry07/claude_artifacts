# Cabinet 7 – Skeleton

Nov 21, 2026 · @Kolja Kauer · draft, waiting for the developer's OK

## Start here

With `Skeleton: on` a Cabinet session runs Fabian's `claude-skeleton` exactly as its author runs it: the same rules, commands, hooks, skills, agents and status board. The only thing that is the session's own is the place. Everything sits in the person's own folder (Cabinet 3, Personal folders) instead of `.claude/` and the repo root, so it loads only in that person's sessions.

Source: the skeleton at commit `f41d005`, as adopted in the Kalendo repo. Rewritten 2026-11-22 so that a comparison of a folder set up from this doc with the skeleton finds no difference in rules or behaviour. Proposed alias: art7; Cabinet 0 – Index and `cabinets.tsv` do not list it yet.

Who wins:

- **The skeleton's files are the rule text.** This doc lists them, says where they go and sums them up. Where this doc and a skeleton file disagree, the file wins and this doc is corrected.
- On the skeleton's subjects Cabinet 7 wins over the base (Cabinet 1 or 5): branches, the guard, shipping, the status board, `done`, review, helpers, tests, CI, changelog, Docker and design.
- The base keeps everything the skeleton says nothing about: the stages and sub-specs, section addresses, `go`, the REPORT format, the overseer's messages (Cabinet 2) and the safety rules.

Order on a conflict inside the skeleton's own rules, as its rules file states it: the machine's rules (the VM rules file) first, then the skeleton's rules, then the project `CLAUDE.md`.

## What changes in the base

| Subject | Base alone | With `Skeleton: on` (as the skeleton has it) |
| --- | --- | --- |
| Push, pull request, merge | each needs its own yes | calling `/ship` is the developer's yes to push the current branch, open its pull request and merge it |
| `done` | only after the developer's yes to "Is this fully solved and checked?" | a row is `done` when it is merged through `/ship`; calling `/ship` is the yes |
| Who moves a state | the session, `done` after the yes | only the row's owner moves it forward; the developer may overrule |
| Status file | a snapshot with one line per section | the skeleton's board, in the shape below |
| Next session | `~/.claude/<session>/NEXT-SESSION.md` | the board's "Next session" section, written so a new session can continue from the board alone; the NEXT-SESSION file only points to it |
| Review before a merge | verifier and reviewer helpers | the built-in `/code-review` on the diff, then the security gate |
| Helpers | scout, keeper, builder, architect, reviewer, verifier | the skeleton's agents (below) |
| Merge | not fixed | squash merge, branch deleted |
| Status reminder | status written at state changes and `adjourn` | a stop hook demands a board update once, when uncommitted changes exist and the board is not among them |
| Formatting | not fixed | Prettier runs after Edit, Write and MultiEdit on the file types it lists (not Rust); it does nothing when Prettier is not installed |

A section address (`B.2`) is used as the row ID on the board, so the base's addresses and the skeleton's rows are the same items.

## Files: what goes where

The personal folder holds a copy of every skeleton file. "Same" means the same content; the only edits allowed are the folder's own path in place of `.claude/` and the person's name.

| Skeleton file | In `claude-<person>/` | Content |
| --- | --- | --- |
| `AGENTS.md` | `RULES.md` | the skeleton's rules, whole; the Cabinet core block and project facts stand above them |
| `STATUS.md` | `STATUS.md` | the board, template shape |
| `.claude/settings.json`, hooks block | `hooks/hooks.json` | same hooks, same events and matchers |
| `.claude/settings.json`, the rest | `settings.json` | same deny rules, same plugin list; loaded with `--settings` or merged into the own user settings |
| `.mcp.json` | `.mcp.json` | same servers and pinned versions (`chrome-devtools-mcp@1.13.0`, `shadcn@4.23.0`) |
| `.claude/commands/ship.md`, `devup.md` | `commands/` | same |
| `.claude/agents/` (designer, explorer, implementer, orchestrator, scribe, tester) | `agents/` | same, with the same models |
| `.claude/skills/` (architecture, changelog-semver, ci-pipeline, design-standards, docker-dev, stack-advisor, status-tracking, tdd-testing, web-design-guidelines) | `skills/` | same, templates included |
| `.claude/hooks/` (guard and its tests, format and its test, check-env, status-reminder, ci-quota) | `hooks/` | same |
| `.claude/bootstrap/` (bootstrap.mjs, manifest.json, adopt-skeleton.md, user-CLAUDE.md) and `.skeleton-version` | `bootstrap/`, `.skeleton-version` | same |

Three files exist only because of the folder layout: `.claude-plugin/plugin.json` (makes the folder loadable), `hooks/hooks.json` (the hooks block as its own file) and `hooks/print-rules.mjs` (a second session-start hook that prints `RULES.md`, because a plugin cannot carry a `CLAUDE.md`).

Machine baseline, from the skeleton's manifest: the plugins `superpowers`, `context7`, `typescript-lsp`, `claude-security` and `impeccable`, the pinned `security-audit` skill, and the npm tools `typescript` and `typescript-language-server`. Install them with `node claude-<person>/bootstrap/bootstrap.mjs --keep-user-settings`; the session-start check reports missing plugins and the missing skill; the npm tools are reported only by the bootstrap's check run.

The manifest holds more, and all of it belongs to running as the author does:

- The marketplace `impeccable` (`pbakaus/impeccable`), and the `security-audit` skill pinned to one commit.
- User files: the `adopt-skeleton` skill (to `~/.claude/skills/adopt-skeleton/`) and the skeleton's global file (to `~/.claude/CLAUDE.md`). Each is written when it is missing or already managed by the skeleton. Beside a hand-written one the bootstrap writes a `.skeleton.md` copy instead and leaves the original alone; `--force` replaces it and keeps a backup; `--check` writes nothing. The bootstrap has no switch to leave the global file out. That file carries the author's preferences, among them replies in German and shipping after every larger task without asking.
- User settings in `~/.claude/settings.json`: the five baseline plugins switched on, the model set to `opus`, and eight plugins switched off where the settings already list them (`feature-dev`, `code-review`, `commit-commands`, `code-simplifier`, `claude-md-management`, `playwright`, `frontend-design`, `ui-ux-pro-max`). The flag `--keep-user-settings` skips this whole step; the skeleton's own start check recommends that flag. To match the author's machine fully, run the bootstrap without it.

Project files stay shared and outside the folder: the CI workflow, the test scripts, `CHANGELOG.md`, `VERSION`, the formatter config.

Check that nothing drifted: `diff -r` between the skeleton's files and the folder shows the folder path, the person's name, the core block in `RULES.md` and the rows of `STATUS.md`.

The `diff` also shows the three layout files above, any project exceptions written into the guard, and notes a project added to `RULES.md`. Verify the folder with `node --test claude-<person>/hooks/` and `claude plugin validate claude-<person>`.

## The rules in short

A summary for reading. The files in the folder are the rules.

### Several people

- Several people and agents always work on the repo at the same time. Never assume you are alone.
- Before starting: `git fetch`, read the board, look at open work (`gh pr list --state open`, `git branch -r`; a draft pull request is a claim too), and compare your paths with every open claim. An overlap is not started: it goes under Blocked and the developer is told.
- Then add your own row under Now (ID, owner, branch, state in-progress, paths, date) and commit it with your first commit. Work others must see at once is pushed early as a draft pull request.
- Parallel work runs on separate branches, and in separate git worktrees if it could touch the same files. Two claims never share a path.
- Never overwrite or discard somebody else's uncommitted changes. No `--force` and no `reset --hard` without asking.

### Working method

- Ask when something is unclear; no far-reaching assumptions. Report honestly. Never claim something is checked without a shown run.
- Test first: a failing test, then green, then refactor. A bugfix starts with a test that reproduces the bug. Test behaviour and contracts, prefer real collaborators, fake only boundaries the project does not own. Never weaken or skip a test to get green; a flaky test is fixed or deleted, never retried into green.
- Work that can run in parallel goes to subagents. A subagent gets a self-contained brief (goal, files, constraints, expected output) and never writes the board.
- Code comments in English and only for the why. Docs in the repo in English.
- A look the project chose on purpose wins over the "no generic look" rule only. Accessibility (WCAG) and the anti-slop checklist still apply to new components.

### Branches and ship

- The stable branch (main and master), the integration branch and the live branch are protected: no direct commit, no direct push, no force push. Work happens on `<type>/<short-name>` (`feat/`, `fix/`, `chore/`) from the integration branch and returns to it by pull request. The live branch takes `hotfix/<name>` branches only, started from it; the integration branch is never merged into the live branch or into a hotfix branch. A fix needed in both goes into the live branch first and then reaches the integration branch through a feature branch from it that merges the live branch. A hotfix is only a fix for the live instance: no features, no refactoring.
- A reserved branch type that is not defined yet (an urgent-fix branch for the stable branch) is never invented: ask.
- Conventional Commits; the body says why.

`/ship`, in this order, stopping at the first failing gate:

1. Preconditions: not on a protected branch; `gh` signed in and a GitHub remote; `git fetch`, and if the target moved, merge it into the branch (no rebase, no force) and start the checks again; never stage a secret file.
2. Verify, in parallel: the `tester` agent runs the suites that apply (end-to-end when UI flows changed); the built-in `/code-review` runs on the diff against the target. Fix and repeat until clean.
3. Security gate: a `/claude-security` scan of the diff. More than 400 changed lines, a path matching `auth|login|session|token|password|payment|billing|crypto|upload|middleware|permission`, or a new public endpoint: also the `security-audit` skill in full audit mode, output to `.security-audit/` (ignored by git). A confirmed finding of medium severity or higher blocks the ship.
4. Documentation: the `scribe` agent drafts the changelog lines for `## [Unreleased]`; no version bump. The own row on the board goes to `done` and moves to Done.
5. Commit (Conventional Commit, drafted by `scribe`) and `git push -u origin <branch>`.
6. `gh pr create --fill --base <target>`, naming the changelog entry.
7. CI: `ci-quota.mjs` says `ok`, `exhausted` or `unknown`. `ok` or `unknown`: `gh pr checks --watch`. `exhausted`, a billing message or `no checks reported`: run every suite locally, end-to-end included. Never merge untested.
8. `gh pr merge --squash --delete-branch`, then switch to the target branch and pull.
9. Report: pull request link, security gate result, where CI ran.

Stops and details of `/ship`:

- No `gh` sign-in or no GitHub remote: commit locally, say what is missing, stop.
- Docker cannot be used: stop and report; nothing is merged without a run.
- CI fails: fix on the branch and push again.
- The diff scan runs at effort `low`. When the full audit runs, tell the developer that it runs because the change is large or sensitive.
- Guardrails: never `--force`, never push to a protected branch, never skip a failing gate, never merge with unresolved review findings.
- Hotfix variant (a `hotfix/<name>` branch started from the live branch): the same steps with the live branch in place of the integration branch everywhere, in the diff, the pull request base and the merge.

`/devup` first checks that the env file exists (if not, the developer is asked to create it from the example; the session never reads, creates or edits it), then starts the dev stack, rebuilding only when dependencies, a Dockerfile or build-time settings changed, and reports the web and API addresses.

### Status board

One file, `STATUS.md` in the folder, in the template's shape: a line with version, integration branch and last full test run, then the sections Now, Blocked, Needs the developer, Next session, Done and Decisions.

```markdown
## Now

| ID | Owner | Branch | State | Paths | Since | Note |
| -- | ----- | ------ | ----- | ----- | ----- | ---- |

## Done

| ID | Owner | PR / version | Date | Note |
| -- | ----- | ------------ | ---- | ---- |
```

- One line per item, no multi-line cells, rows short. Long detail goes to `docs/topics/<topic>/` and the row links it.
- One writer per row: only the owner edits a row. Subagents never write the board.
- States: `open`, `in-progress`, `review` (pull request open, `/ship` pending), `done` (merged through `/ship`).
- Update when work starts, changes state, is blocked and finishes. No secrets, tokens or personal data.
- End of a session: rewrite Next session (ordered, each item with its first step, the branch and open questions), move `done` rows to Done, newest first, and put decisions for the developer under Needs the developer, each with a recommendation. More than 20 rows in Done: the older ones go to the changelog or `docs/archive/`.

A merge conflict on the board: keep both sides' rows; for the same row the owner's version wins; never resolve by dropping somebody else's row. Instead of changing another owner's row, add a note under Blocked.

### Tests, CI and Docker

- Builds and tests run only in containers; nothing is installed on the host for them. The test command and its suites are project facts.
- A CI pipeline always exists and runs the same suites on every pull request and every push to a protected branch. CI passes before a merge. It stays fast and pins third-party actions to a major version.
- End-to-end tests (Playwright) run on their own stack with anonymised data, never against real data. A live look at the UI with the `chrome-devtools` MCP is required for every UI change, as are the end-to-end tests.
- Nobody is added to the `docker` group. On Linux every `docker` call is prefixed with `sudo`; after a run with `sudo`, check that no root-owned files were left in the repo. Ports and the VM's compose stack belong to the stack repo; no database port is published.
- A project with several instances never mixes them: not their databases, volumes or tokens.

Every `sudo` call asks the developer. Anything that starts or builds containers (`up`, `build`, `run`, `exec`) needs approval, because a compose file can mount the host as root.

### Changelog and version

- `CHANGELOG.md` follows Keep a Changelog (Added, Changed, Fixed, Removed, Security, Deprecated), written by hand from the diff, one short line per change a user can see, under `## [Unreleased]`. Add lines, never rewrite other lines.
- One product version in `VERSION`, SemVer; every other place that carries it changes in the same commit. A feature or hotfix pull request never bumps it. A release is its own pull request from the integration branch into the stable branch, with the tag `vX.Y.Z` after the merge.

### Secrets

- Secret files (`.env` and its variants) are never read, committed or printed; only the `.example` templates are. No secrets in the repo, logs, the board or a pull request.

### Design, architecture and stack

- UI work follows the `design-standards` skill. Its sources, in this order: accessibility to WCAG 2.2 AA; the Web Interface Guidelines, run as an audit with the `web-design-guidelines` skill on finished UI; the Apple Human Interface Guidelines for interaction principles (touch targets of 44pt among them); the `impeccable` plugin for direction and critique; framework docs through context7.
- Also from that skill: the anti-slop checklist; design tokens defined first and reused; one clear hierarchy per screen with real content; states for loading, empty, error, disabled and focus; responsive from 360px; a check in a real browser with the `chrome-devtools` MCP.
- Structure follows the `architecture` skill: transport, application logic and data access kept apart, input validated at the boundary, versioned migrations, authorization checked on the server for every request.
- A new project or a new technology goes through the `stack-advisor` skill before any code: recommend, give the reason, wait for the confirmation.

### Hooks

| Hook | When | Does |
| --- | --- | --- |
| `check-env.mjs` | session start | checks Node (22 or newer), `gh` (signed in, with the `user` scope), Docker with the Compose plugin and a reachable daemon, Chrome or Chromium for the browser MCP, and the plugins and the pinned skill of the machine baseline. gh is a hard gate (installed and signed in; its message names 2.20 as the minimum, but the hook does not compare versions): without it no work starts until the developer has installed it and signed in. For everything else it prints what is missing and what to offer. It does not look at the npm tools |
| `guard.mjs` | before Bash, PowerShell, Read, Grep, Glob, Edit, Write, MultiEdit and NotebookEdit calls | blocks edits, commits, merges and pushes on a protected branch, force pushes, reading, copying, writing or staging a secret file (a command that only names one with ls, stat, test, echo, printf, git or gh passes), a pull request into the live branch from a branch that is not `hotfix/<name>`, and the integration branch flowing into a hotfix branch. It looks through `sudo`, `env` and nested shells. It is a guard rail, not a sandbox |
| `format.mjs` | after Edit, Write and MultiEdit | Prettier on the edited file if its type is listed (web and config types, not Rust), without a shell; does nothing when Prettier is not installed |
| `status-reminder.mjs` | when the session stops | uncommitted changes exist (more than the changelog) and the board is not among them: demands a board update once. Silent on a protected branch and when there is no board file |
| `ci-quota.mjs` | called by `/ship` | says ok, exhausted or unknown, keeping a reserve of 50 minutes; unknown when the repo owner is not the signed-in gh user, which is every organisation repo |

The guard has its own tests (`node --test`). The skeleton states no general rule for exceptions. The Kalendo copy carries two dated ones in the guard's code: a fixed compose call that may take the stack's env file, for a short list of test services.

### Agents

| Agent | Model | Job |
| --- | --- | --- |
| `explorer` | haiku | search, read, locate, summarise; never edits |
| `scribe` | haiku | changelog entry, commit message and status text from the diff; returns text, edits nothing |
| `implementer` | sonnet | production code for one scoped task, so the given failing tests pass |
| `tester` | sonnet | writes the failing test first, runs suites, finds the cause of a failure |
| `designer` | sonnet | builds or reviews UI with `design-standards` and `impeccable` |
| `orchestrator` | opus | optional main-thread agent, a personal choice per user |

Pick the cheapest model that can do the job. A subagent that returns incomplete work, hits its turn limit or fails the same way twice is sent again with the next model up (haiku, sonnet, opus), never a third time on the same model. Binding for every orchestrator, whatever its style: read the board and claim, one branch per feature, ship only through `/ship`, write only the own rows.

Limits in the agent files: `explorer` and `scribe` have only the tools Read, Glob, Grep and Bash. Turn limits are 20 for `explorer`, 12 for `scribe` and 40 for `implementer`, `tester` and `designer`. The `implementer` never touches a secret file, the board or the changelog and stays inside the paths it was given. The `orchestrator` file and the `adopt-skeleton` skill say to reply in German.

## Own way

What a Cabinet session adds on top. None of it removes or weakens a skeleton rule.

- **Place:** the personal folder, loaded as a plugin, with a two-line pointer in the root `CLAUDE.md` (Cabinet 3). The developer, or the session after the developer's yes, writes that pointer; the `adopt-skeleton` skill never touches the root `CLAUDE.md`. Hence the three layout files listed under Files.
- **Other people's boards:** `updatestatus` reads the other `claude-*/STATUS.md` files and lists what touches the own paths.
- **Cabinet layer:** stages, sub-specs, section addresses as row IDs, `go`, REPORTs, the overseer. The Cabinet helpers (scout, keeper, builder, architect, reviewer, verifier) may exist beside the skeleton's agents; they never replace `/code-review`, the security gate or any other `/ship` step.
- **The developer's own choices, as the skeleton leaves them:** whether the bootstrap runs with `--keep-user-settings`, and which main-thread agent to use (the orchestrator is a personal choice per user). The skeleton's global file is not a choice of the bootstrap: a developer who keeps an own hand-written `~/.claude/CLAUDE.md` keeps it, and gets the skeleton's as a `.skeleton.md` copy beside it.

## Open points

1. Decided 2026-11-22: `updatestatus` never switches branches, but it fetches and may read the other people's boards from the remote integration branch, read-only. With this the step before starting is the skeleton's.
2. Decided 2026-11-22: the three guard fixes of the Kalendo copy in `claude-kolja/` (`git diff --no-index`, `git grep`, `gh` with a secret file; branch names from a config file) are offered to the skeleton's author. Until he takes them, that copy is stricter than the skeleton's guard and allows the same normal work.
3. Decided 2026-11-22: the bootstrap runs with `--keep-user-settings`, as the skeleton's own start check recommends.
4. Decisions of 2026-11-21 replaced by this rewrite: merge commit (now squash, as the skeleton), `done` only after a separate yes (now `done` on merge through `/ship`), formatter off (now on).
5. Open: alias art7 and the switch name `Skeleton:`. Recommended: keep both, then add the row to Cabinet 0 – Index and `cabinets.tsv`.

Version: `art7.v1`
