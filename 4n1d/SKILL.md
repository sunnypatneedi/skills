---
name: 4n1d
description: Roadmap triage across the 4N1D framework (NOW/NEXT/NOT-YET/NEVER/DONE in docs/roadmap/). Scans session for completed work, killed ideas, new discoveries, fired triggers, and stale items. Recommends additions, promotions, demotions, and archiving across all five files. Checks anti-patterns (NOW >4, no [learn], stale triggers, zombie NOT-YET). Use at session end, after shipping, or on-demand. Triggers on "/4n1d", "update roadmap", "roadmap triage", "what goes in NOW", "promote to NEXT", "session wrap-up", "what did we ship", or any request to review docs/roadmap/ files.
---

# 4N1D Roadmap Triage

End-of-session review that keeps the 4N1D roadmap honest. Read all five files, scan the conversation, recommend changes.

## What is 4N1D?

A lightweight roadmap framework built around five files that each answer one question:

| File | Question it answers |
|------|--------------------|
| `NOW.md` | What are we actively working on? (≤4 items) |
| `NEXT.md` | What's queued with a written trigger for promotion? |
| `NOT-YET.md` | What ideas are parked until conditions change? |
| `NEVER.md` | What have we structurally killed and why? |
| `DONE.md` | What did we ship, and what did we learn? |

The framework forces every idea to live in exactly one file and forces every promotion to be justified by a written trigger — not vibes.

## Process

### 1. Read current state

Read all files in `docs/roadmap/` in parallel:
- `NOW.md` — current priorities
- `NEXT.md` — triggered queue
- `NOT-YET.md` — parked ideas
- `NEVER.md` — structural kills
- `DONE.md` — shipped archive
- `README.md` — framework rules (only if unfamiliar with 4N1D)

### 2. Scan conversation for signals

Review the current session for:

| Signal | Maps to |
|--------|---------|
| Completed work (merged PRs, shipped features, closed bugs) | → DONE.md entries |
| Killed ideas (adversarial review, infeasible, philosophy violation) | → NEVER.md (if structural) or NOT-YET.md (if timing) |
| New ideas discussed but not built | → NOT-YET.md (default) or NOW.md (if metric-justified) |
| Evidence that a NEXT trigger fired | → Promote NEXT → NOW |
| Evidence that a NOT-YET trigger emerged | → Promote NOT-YET → NEXT |
| NOW items worked on but not finished | → Keep in NOW, note progress |
| NOW items not touched this session | → Flag for staleness check |

### 3. Run anti-pattern checks

Flag violations before recommending changes:

- [ ] **NOW >4 items** — recommend cuts
- [ ] **NOW has no `[learn]` items** — flag "executing without validating"
- [ ] **NOW item >14 days old** — flag for re-justification
- [ ] **NOW item >30 days old** — recommend break-up or demotion
- [ ] **NEXT triggers >30 days old** — flag for refresh
- [ ] **NOT-YET items >90 days without activity** — recommend NEVER or delete
- [ ] **NEVER >10 items** — check for timing-kills that belong in NOT-YET
- [ ] **DONE.md missing entries for completed work** — add them

### 4. Generate recommendations

Output a structured triage report:

```
## 4N1D Triage — [date]

### DONE.md (add)
- [type] Description (duration) → outcome

### NOW.md (no changes / add / remove)
- Swap: remove [X], add [Y] because [reason]
- Flag: [item] has been in NOW for [N] days

### NEXT.md (no changes / promote / add / refresh triggers)
- Promote: [item] → NOW (trigger fired: [evidence])
- Refresh: [item] trigger is 45 days old

### NOT-YET.md (no changes / add / promote / delete)
- Add: [new idea from session] with thesis + trigger + kill condition
- Promote: [item] → NEXT (trigger checklist can now be written)

### NEVER.md (no changes / add)
- Add: [idea] — structural kill because [reason]

### Anti-pattern flags
- [list any violations found]
```

### 5. Apply changes

After presenting the triage report, ask: "Apply these changes?" If confirmed:

- Edit each file directly (use Edit tool, not full rewrites)
- Add `<!-- reviewed: YYYY-MM-DD -->` datestamp to each modified file
- For DONE.md: append to the current week's section
- For NEXT.md: include `**Trigger written:** YYYY-MM-DD` on new items
- For NOW.md: include `**Added:** YYYY-MM-DD` on new items

## Work-type tags

Every item must have one: `[build]`, `[learn]`, `[maintain]`, `[decide]`, `[hotfix]`.

## Typed triggers (NEXT items)

Pick the type that matches the decision structure:

| Type | Format |
|------|--------|
| Metric-gated | `>N [metric]` |
| Qualitative-gated | `[signal] from [named verifiable source]` |
| Time-gated | `by YYYY-MM-DD because [external constraint]` |
| Dependency-gated | `when [item X] reaches DONE` |
| Compound | metric AND qualitative (most common) |

## NEVER rules

Only structural kills: legal, philosophical, architectural. If the reason is "wrong timing" or "not a priority," it goes in NOT-YET. Keep NEVER under 10 items.

## DONE format

One-line entries grouped by ISO week. Include outcome for `[learn]` and `[decide]`:

```
- [build] Feature name (duration)
- [learn] Research topic → key finding
- [decide] Decision made → chosen option + rationale
- [hotfix] What broke — root cause
```

## Bootstrap: if docs/roadmap/ doesn't exist

If the project has no `docs/roadmap/` directory yet, offer to bootstrap one. Create five empty files with the section headers below and a short `README.md` explaining the framework.

```
docs/roadmap/
├── README.md      # "4N1D — one file per question. See each file's header."
├── NOW.md         # "# NOW\n\nActive work (≤4 items).\n"
├── NEXT.md        # "# NEXT\n\nTriggered queue.\n"
├── NOT-YET.md     # "# NOT-YET\n\nParked ideas.\n"
├── NEVER.md       # "# NEVER\n\nStructural kills.\n"
└── DONE.md        # "# DONE\n\n## Week of YYYY-MM-DD\n"
```
