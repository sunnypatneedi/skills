---
name: claudemd-improve
description: >
  Audit, improve, and maintain CLAUDE.md (project instructions for AI agents). Detects stale rules, contradictions, missing pitfalls, outdated workspace facts, bloat, and broken file references. Use whenever the user mentions CLAUDE.md, agent instructions, project context, or workspace rules — including "audit my CLAUDE.md", "clean up agent instructions", "add a pitfall", "update project context", "my CLAUDE.md is outdated", "trim CLAUDE.md", or after major codebase changes. Even if the user doesn't name CLAUDE.md explicitly — requests like "why do agents keep getting confused" or "something is wrong with my project setup" may indicate CLAUDE.md needs attention.
---

# CLAUDE.md Improver

Audit, refactor, and enhance `CLAUDE.md` — the project instruction file that shapes every AI agent session. A well-maintained CLAUDE.md is the highest-leverage artifact in a codebase: it compounds across every future session.

> **Scope:** This skill operates on `CLAUDE.md` only. If your project also keeps an `AGENTS.md` (or any other agent-instruction file), this skill does not touch it. Run a separate audit for that file.

## The Audit (Phase 1)

Read the entire `CLAUDE.md`. For each section, check:

### Staleness Check
- Do file paths referenced still exist? (`ls` each one)
- Do commands referenced still work? Verify they exist in `package.json`, `Makefile`, `justfile`, etc.
- Are schema names, table names, and constraints still accurate? (Check against migrations / schema files.)
- Are "Learned Workspace Facts" still true? (Spot-check 3–5 against the codebase.)
- Is the product description current? (Check against the landing page or top-level README.)

### Contradiction Check
- Does any rule in one section conflict with another? (e.g., "Never X" in one place, example showing X in another.)
- Do "Pitfalls" and "Production Lessons" overlap or contradict?
- Does the TL;DR still match the rest of the file?
- Are any audience/user details consistent across sections?

### Completeness Check
- Are there known patterns the team uses that aren't documented? Check recent git log for recurring patterns.
- Are there files/directories that agents frequently need but aren't in "Structure" or "Where to Add Code"?
- Are there recent production incidents whose lessons aren't captured?
- Is the testing strategy section current with the actual test infrastructure?

### Bloat Check
- Are any rules duplicated across sections?
- Are any rules so obvious they don't need stating? (e.g., "use TypeScript" in a TypeScript-only project.)
- Are any "Learned Workspace Facts" now documented elsewhere (in proper docs/) and redundant here?
- Is the file over 200 lines? If so, identify what can be moved to reference docs.

### Reference Integrity
- For every `docs/...` or `.claude/...` path mentioned, verify it exists with `ls`.
- For every "See X for details" pointer, verify X has the claimed content.
- Flag any dead references.
- For each dead reference, classify it: **(a)** file was moved — find the new path, **(b)** file was deleted — remove the reference, **(c)** file should exist but doesn't — flag for creation.
- Check that directory references actually exist. Claims like "X was removed" should be verified against the filesystem.

## The Report (Phase 2)

After auditing, produce a structured report:

```
CLAUDE.MD AUDIT REPORT
══════════════════════════════════════
File: CLAUDE.md
Lines: <N> | Sections: <N> | Last modified: <date>

STALE (needs update):
  🔴 Line <N>: <claim> — <what's actually true now>
  🟡 Line <N>: <claim> — <uncertain, needs verification>

CONTRADICTIONS:
  ⚠️ Line <N> says <X> but line <M> says <Y>

MISSING:
  ➕ <pattern/fact discovered in repo but not documented>

BLOAT:
  📎 <fact> appears in both <section A> and <section B>
  📎 <section> has <N> items — consider archiving resolved ones

DEAD REFERENCES:
  ❌ Line <N>: <path> — <classification: moved/deleted/missing>

SCORE: <N>/100 (<grade>)
══════════════════════════════════════
```

## The Fix (Phase 3)

After the user reviews the report and approves changes:

1. Create a backup: `cp CLAUDE.md CLAUDE.md.bak`
2. Apply fixes directly to `CLAUDE.md`
3. Show a diff of changes
4. Remove the backup if the user approves

### Edit Principles

When editing CLAUDE.md, follow these principles to avoid degrading it:

- **Preserve voice.** CLAUDE.md typically has a specific tone — terse, imperative, opinionated. Don't soften it or add filler words. Match the existing style.
- **Facts over opinions.** Every line should be verifiable against the codebase. *"Always use Tailwind"* is verifiable. *"Tailwind is the best CSS approach"* is opinion.
- **One place per fact.** If something is in Pitfalls, don't also put it in Production Lessons. Choose the better home and add a cross-reference if needed.
- **Learned Workspace Facts are temporary.** They capture things discovered during sessions. Once a fact is formalized into docs/ or into a proper section of CLAUDE.md, remove it from Learned Workspace Facts. **Graduation criteria:** if a fact has been stable for 2+ weeks and belongs in a proper section, move it there and delete the workspace fact.
- **Keep it under 200 lines.** CLAUDE.md is loaded into every agent session. Bloat costs real tokens. If a section grows beyond what's needed for quick reference, move the details to a reference doc and leave a pointer.
- **Dead references are urgent.** A broken path sends agents on wild goose chases. When you find dead references, fix them immediately — don't just report them. Either update the path, remove the reference, or create a stub doc.

### Section-Specific Guidance

| Section | What belongs here | What doesn't |
|---------|------------------|--------------|
| Behavioral Rules | Universal agent behavior rules | Project-specific technical rules |
| TL;DR | Short product summary + stack | Detailed architecture |
| Product Philosophy | Non-negotiable design principles | Implementation details |
| Critical Rules | Rules that prevent real damage if broken | Nice-to-have conventions |
| Pitfalls | Things that WILL break if you don't know them | General best practices |
| Production Lessons | Hard-won operational knowledge | Theoretical concerns |
| Learned Workspace Facts | Recent discoveries not yet formalized | Facts already in docs/ |
| Where to Add Code | Directory conventions | Detailed architecture |
| Reference Docs | Pointers to deeper docs | The docs themselves |

## Quick Audit Mode

When the user says "quick audit" or just wants a health check:

1. Count dead references (`ls` each path, report count).
2. Check the 3 most likely stale facts (product description, key commands, top-level structure).
3. Report line count and whether file is over 200 lines.
4. Skip full contradiction/completeness analysis.
5. Output: one-paragraph summary + score + top 3 actions.

This takes ~1 minute vs. the full audit's ~5 minutes.

## Enrichment Mode

When the user says "enrich" or "update CLAUDE.md with what we learned":

1. Read recent git log (`git log --oneline -20`).
2. Check for new files/directories not reflected in Structure or Where to Add Code.
3. Check for new patterns in recent commits not captured in any section.
4. Propose additions with exact placement.

## Trim Mode

When the user says "trim" or "CLAUDE.md is too long":

1. Count lines per section.
2. Identify the largest sections.
3. For each large section, identify what can move to reference docs.
4. Identify Learned Workspace Facts that are now redundant.
5. Propose removals with rationale.
