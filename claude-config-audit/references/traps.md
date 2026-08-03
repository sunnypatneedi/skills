# Silent-failure catalog

Every entry here failed silently in a real audit — no error, no test failure, no symptom until
much later. Each has a check that takes seconds. Run the checks; do not rely on noticing.

## Contents
1. Measurement traps
2. Ordering traps (breaking the machine mid-audit)
3. Reversibility traps (deleting something that had no other copy)
4. Reference traps (removing something still pointed at)
5. Scope traps (evidence that doesn't mean what it looks like)
6. Content traps (cutting the wrong thing from instruction files)

---

## 1. Measurement traps

**Cross-batch wall time is not comparable.** API/machine latency drifts by seconds. One audit saw
the isolation floor — which by definition ignores all config — move 2.04s → 5.11s in an hour. A
naive before/after read as a 52% regression while config overhead had actually fallen 73%.
→ Always interleave against the floor in one batch; report `current − floor`.

**Three runs is not enough.** One outlier dominates a 3-run mean. Use ≥5 and report the median.

**zsh does not word-split unquoted variables.** A command assembled in a var and run as
`$CMD claude …` becomes one argv[0], fails in ~19ms, and produces a full table of plausible
near-zero timings that look like a spectacular win. → Run measurement scripts with `bash`.

**Shell globbing eats model identifiers.** `--model opus[1m]` is a glob in zsh: `no matches found`.
→ Quote it.

**`duration_api_ms` can exceed wall time** (concurrent requests), so `wall − api` is not startup
overhead. → Use the floor-delta method instead.

**Startup is usually the smallest axis.** Measure four: startup (once), per-tool-call (every call),
per-session (per-call × real call counts), context (every turn). One audit found 2s of startup
against 46s/session of hook overhead and 51k tokens of context.

**Non-blocking components cost ~0 regardless of count.** Check the debug log for explicit
async/nonblocking markers before assuming N servers cost N × something.

**The expensive thing is often the silence between two log lines.** Sort inter-event deltas in the
debug trace, not just the lines that mention timing.

---

## 2. Ordering traps

**Wire-before-install hard-fails everything.** Pointing config at a hook script that isn't at its
final path yet means the interpreter exits non-zero — and a non-zero PreToolUse hook can block
*every* tool call in *every* project. A path in a temp/scratch dir is a time bomb: it works today
and breaks when the dir is cleaned.
→ Install at the final path → run it from that path → only then wire config to it.

**Removing a worktree/dir you are standing in** breaks every later command in the same shell
(`Unable to read current working directory`), which can silently blank a variable you then write
to a log. → `cd` out first; do cleanup last.

**Backups that sweep in incidental subdirectories** can be gigabytes and time out. Check sizes
first (`du -sh`), exclude worktrees/caches/logs, then verify the archive actually contains the key
paths by listing them.

---

## 3. Reversibility traps

**"It's a move, not a delete" is a weaker claim than it sounds.** Verify an independent copy
exists before calling anything reversible: hash the trees and confirm byte-identity, and confirm
the other copy is actually pushed (`HEAD == origin/main`, 0 unpushed) rather than merely present.

**Live copy vs tracked mirror.** When a config dir is mirrored to a repo, the live path is usually
the one that takes effect and the repo is the one that's backed up. Editing live silently diverges
them; editing the repo silently does nothing. → Check both, and sync after editing.
This is its own recurring bug — it happened *again* during the audit that documented it.

**A symlink's entire content is its target string.** A dangling symlink holds zero bytes. Deleting
it destroys nothing — but say so with the target listed, rather than treating it as a file.

**Config dirs are often gitignored.** Changes there cannot go in a PR and will not survive a fresh
clone. → `git check-ignore -v <path>` and `git rev-parse --show-toplevel` before planning a PR.

**A working dir can be a non-repo *inside* another repo.** `git rev-parse --show-toplevel` then
returns the enclosing repo, and a naive commit pushes your work to an unrelated remote. → Compare
`--show-toplevel` to `$PWD` and check whether your files show as untracked there.

---

## 4. Reference traps

**Documented remedies fail silently when removed.** A skill named in a pitfalls doc, another
repo's instruction file, a subagent definition, or a memory entry will simply not exist next time
someone follows that instruction — no error, just an agent that can't do the thing.
→ Before removing anything by name, grep it across ALL instruction surfaces: project + user
instruction files, docs, other repos' instruction files, agents, commands, memory index.
In one audit this held back 33 of 126 archive candidates.

**Never renumber referenced identifiers.** Rule numbers, error codes, and IDs get cited as literal
strings in hooks' user-facing messages, tests, docs, and memory. Renumbering repoints all of them
with nothing failing. → Grep the identifier, then APPEND new entries instead of renumbering.

**Usage counters may not record what you assume.** Confirm whether a counter logs only explicit
invocations or also model-triggered loads before trusting a zero.

**Do not grep raw transcripts for a name to prove usage.** Every system prompt enumerates every
available skill and tool, so substring search matches the catalogue, not the call. Parse structured
tool-use blocks.

---

## 5. Scope traps

**Per-project evidence does not bound shared resources.** Account-level connectors are shared with
other projects and other clients of the same account. "Zero calls in this repo" is necessary, not
sufficient. → State the scope limit whenever citing per-project counts.

**Some things have no file-based off switch.** Account-level connectors may only be toggled in a
vendor UI. Report that honestly instead of implying a config change will disable them.

**User-global config changes affect every project.** Flag the blast radius explicitly and confirm
that scope, even when a general "apply everything" approval exists.

**A pending dependency outranks a zero.** Something unused today but required by a scheduled
activation is a keep. Check open work before removing on usage grounds alone.

---

## 6. Content traps

**Auto-loaded memory over its read limit is silently truncated.** Part of it never reaches
context — including whichever entries sit past the cutoff. Compressing it is a *correctness* fix,
not a token saving: label it accurately.

**Compression arithmetic must clear the limit.** N entries × target length can still exceed the
limit. Cut entry count too, or the fix doesn't fix anything.

**Line targets are not licences to drop safety rules.** An aggressive target will happily delete
data-minimisation, fail-closed constraints, error-leakage rules, and test-route production gates —
all of which an agent must know BEFORE acting, without being prompted to go look. Anything in that
class stays inline regardless of the target.

**Stale volatile content is worse than absent.** Dated strategy/pricing/positioning in an
always-loaded file gets paraphrased as current. Move it out; leave a pointer to the live source.

**Descriptions vs bodies.** Only descriptions are always in context; bodies load on invoke.
Archiving unused items does not fix fat descriptions on the items you KEEP — that is a separate
lever, and usually the bigger one.

**Multi-link index lines are more token-efficient than one line per item** when filenames are long:
one line carrying six links costs a fraction of six lines' markup overhead.
