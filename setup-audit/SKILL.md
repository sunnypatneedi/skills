---
name: setup-audit
description: Measure then prune a Claude Code harness — MCP servers, hooks, plugins, skill descriptions, instruction files, auto-loaded memory. Evidence before cuts. Use on "session starts slow", "prune my MCP servers", "too much context loads before I type", or harness/config cleanup — not CLAUDE.md wording alone (see claudemd-improve).
---

# Setup Audit

Measure first. The measurement can **veto any cut proposed below** — if evidence contradicts a
prescription here, follow the evidence and say so explicitly in the report.

Do not assume MCP servers, hooks, or skills are the problem. They are candidates, not defendants.
It is common for the suspected cause to measure ~0 while something unmeasured dominates — that is
why the order below is measure-then-prescribe, not the reverse.

## The four cost axes

Measuring only the first is the standard mistake. On the machine this skill was built from,
startup was the *smallest* axis — but that is one observation, not a law. A setup with
stdio/npx-spawned or cold network MCP servers can spend 20-60s in startup alone. Rank only
after measuring, and never assume the axis the user complained about is the wrong one.

| axis | paid | how |
|---|---|---|
| startup | once per session | `scripts/measure-startup.sh` |
| per-tool-call | every tool use | time the hook path directly |
| per-session | per-call × real call counts | `scripts/usage-evidence.py` |
| context | every turn, forever | `scripts/context-inventory.py` |

Rank findings by **total session impact**, never by startup. If the axis named in the user's
request is not the dominant one, say that in the first line of the report.

## Scripts

| script | use |
|---|---|
| `scripts/measure-startup.sh [REPS] [MODEL]` | Interleaved startup measurement against the isolation floor. Run with `bash`. Quote the model (`'opus[1m]'`). |
| `scripts/context-inventory.py [--project DIR]` | Always-loaded tokens by surface; flags a truncated memory index (exit 1). |
| `scripts/usage-evidence.py [--pattern REGEX]` | Real MCP/tool call counts from transcripts; `--pattern` sizes a hook's trigger rate. |

## Workflow

### Phase 0 — Discover and make reversible

Locate every surface that loads; report which exist and which don't (absent is a finding):
config files at project/user/managed scope · MCP from all sources (project file, user scope,
plugin-provided, account connectors, IDE/browser extensions — different places, different off
switches, some with none) · hooks at every event · plugins, skills, commands, subagents, output
styles, statusline, workflows, LSP · instruction files at every scope plus `@`-imports followed
transitively · auto-loaded memory · env vars affecting startup.

Useful commands: `claude mcp list` and the debug trace for connected servers (account-level
connectors and IDE/extension servers do NOT appear on disk — the trace is the only inventory);
`git check-ignore -v <path>`; `claude --help | grep safe-mode` to confirm a floor flag exists.

For each, answer three questions — they determine what you're allowed to do:
1. **Version-controlled?** `git check-ignore -v` + `git rev-parse --show-toplevel`. Gitignored or
   non-repo config cannot go in a PR; plan to ship in place and say so.
2. **Upstream copy?** Hash the trees and confirm it's actually pushed before calling anything
   reversible.
3. **Symlink with a resolving target?**

Then **snapshot** everything you might touch, verify the archive contains the key paths by listing
them, and report its location. Check sizes first — exclude worktrees/caches.

### Phase 1 — Measure

Run all four axes. For startup use `measure-startup.sh` (≥5 reps, median, interleaved).

Then capture one debug trace: `claude --debug-file /tmp/dbg.log -p 'Reply with exactly: ok'`
(sort inter-event deltas to find the gaps). For the **per-tool-call axis**, hooks are commands in
the `hooks` object of settings.json — time one directly by piping it the payload it expects:
`printf '{"tool_name":"Bash","tool_input":{"command":"ls"},"cwd":"'$PWD'"}' | <hook cmd>`.
An empty stdin makes most hooks error out instantly and record a fake ~0.

From the trace, extract: per-server connect times and transport, any
timeout/retry/auth failure/ENOENT, components explicitly marked non-blocking (these cost ~0 *on
the startup axis* regardless of count — they can still dominate the context axis via tool schemas,
and pay latency at first call), and the **largest unlogged gaps** — the expensive thing is often
the silence between two log lines.

Report a table: component → cost per axis → total session impact.

### Phase 2 — Inventory

Everything from Phase 0 with file paths. Mark MCP servers connected / erroring / timing out /
unauthenticated / never-called. Give hooks their event, matcher, what they execute, whether they
make a **network call**, and whether they can block the tool they intercept — flag any matching on
loose string containment rather than parsed structure. For skills/agents report description tokens
separately from body tokens.

### Phase 3 — Propose: keep / kill / **rewrite** / defer

Four verdicts, not two. Each gets one line of reasoning and its measured cost.

**REWRITE is the default for anything protective.** A guard that is expensive is a guard with a
bug, not a guard to delete. If prose rules already existed and the failure happened anyway, prose
has failed its trial — the answer is a cheaper mechanism, not removal. Fix the cost: match on
parsed structure instead of substring, merge N interceptors into one process, or cache the network
call — **but only where a stale answer is still a safe answer.** Caching a freshness, auth, or
revocation check defeats the guard at precisely the moment it matters. State the staleness window
against the threat before caching anything.

**KILL** only with: measured cost, no usage evidence, no pending dependency, and a name-grep across
every instruction surface showing nothing still points at it.

**KEEP** anything measured at ~0 on all *measured* axes — but note what the measurements do not
cover. `context-inventory.py` does **not** count MCP tool schemas, and an idle server has a risk
surface (write scopes, injection reach) that no timer registers. Zero measured time is not zero
cost: estimate schema tokens and scope risk before a KEEP on an unused server, or this rule makes
MCP structurally unprunable. List items you proposed cutting and then reversed, with the evidence.

**DEFER** where removal needs a decision or dependency first.

Specific rules: only descriptions are always in context, so rewrite them to concrete triggers under
25 words and move reference material into files pointed at by path — and note that fat descriptions
concentrate in the items you KEEP, so archiving does not fix them. The 25-word target is an
*aggregate* budget (100+ descriptions × 120 tokens is where the cost lives), not a per-skill law:
do not strip a trigger phrase or a disambiguator that prevents mis-routing in order to hit it. For instruction files, keep only
what is project-specific, non-inferable from the repo, and needed on most tasks; propose a line
target, but anything an agent must know BEFORE acting stays inline regardless. Never renumber
referenced identifiers — append.

Read `references/traps.md` before finalising. Every entry there failed silently in a real audit.

### Phase 4 — Adversarial gate

Before applying, have an independent reviewer (separate instance, ideally a different model) attack
the proposal with the measured numbers in hand:

- Which cut has a failure mode the numbers don't show?
- What breaks **silently** — where is the failure a missing capability nobody gets told about?
- Is any evidence over-read beyond its actual scope?
- Which cut is a false economy: real risk, negligible gain?
- Is anything in the measured data misinterpreted?
- **Ordering hazards** — does any step leave the system broken in between? Anything referenced by
  path must be installed and verified at its final path *before* config points at it.

Report the findings and what changed in response. If you disagree, say why. A gate whose findings
were all accepted uncritically was not adversarial enough.

### Phase 5 — Apply and re-measure

Order: snapshot → install new files at final paths and verify they run there → wire config → remove
old entries → verify. Never wire before install.

**Verify behavioural equivalence by replay, not by example.** If logic that gates other operations
was merged or rewritten, replay the real historical corpus through old and new and report the match
rate. Hand-picked cases confirm what you already believed; the corpus finds what you didn't.

Re-measure with the interleaved method. Report before/after on all four axes, following the
honesty rules in `references/ledger-template.md`.

### Phase 6 — Record

Write the ledger per `references/ledger-template.md`. **Scope the location to the audit:** a
project-scope audit belongs in the project repo; a *user-scope* audit inventories private skill
names, memory contents, machine paths and account connectors and must NOT be committed to a
project repo — write it under the user's own config dir instead. The two sections most often skipped are the
two that earn it: **re-add criteria** per item, and **kept-against-proposal** with the reversing
evidence — that section is what stops the next audit re-proposing the same cut.

## Constraints

- Show diffs before writing; get approval before applying.
- Never delete a file without listing what was in it and confirming a copy exists elsewhere.
- Prefer move-to-archive over delete; prefer rewrite over removal for anything protective.
- Do not add new tooling unless asked — record mechanizable follow-ups as queued candidates instead.
- Flag any change whose blast radius extends beyond this project and confirm that scope explicitly,
  even under a general approval.
- State the load-bearing assumption at each phase; if falsifiable in under two minutes, test it
  before building on it.
