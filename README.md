# Showcase Skill

**Make your AI agent orchestration visible for YC, investors, and demos.**

When you build with AI agents (Claude Code, Cursor, etc.), most of the orchestration happens invisibly—skills inject silently, subagents work in the background, decisions are made without explanation. This skill makes all of that **visible** in your session transcript.

## Installation

```bash
npx skills add sunnypatneedi/skills
```

## Quick Reference

| When | Flag | Accuracy | Command |
|------|------|----------|---------|
| **Before** session | `--showcase` | 95% | `"Build my-project --showcase"` |
| **After** session | `--reconstruct` | 60-80% | `"Reconstruct from session.md --reconstruct"` |

---

## Usage

### `--showcase` — For New Sessions (Recommended)

Use at the **start** of a session to capture full orchestration details as they happen.

```bash
# Start your session with --showcase
"Build my-startup-idea --showcase"

# Work normally... Claude narrates all orchestration

# When done, export using built-in command
/export session.md
```

**What gets captured:**
- Skill logic (what each skill instructed Claude to do)
- Subagent reasoning (reconstructed internal process)
- Decision rationale (tradeoffs considered)
- Compound learning (semantic meaning of patterns)

**Example output with `--showcase`:**

```markdown
## 🔧 Skill Activated: idea-validator

**This skill instructs me to:**
1. Analyze problem clarity using the "would I pay for this" test
2. Check market need via revealed demand signals
3. Assess competitive moat using idea maze framework

**I will now execute these instructions...**

### 📋 Decision Point: Architecture Approach

| Option | Pros | Cons |
|--------|------|------|
| Monolith | Simple, fast to ship | Scaling limits |
| Microservices | Scalable | Complexity overhead |

**Decision:** Monolith first
**Rationale:** Ship fast, validate, refactor later if needed
```

---

### `--reconstruct` — For Old Sessions (Fallback)

Use **after** a session to retroactively infer orchestration from an existing export.

```bash
# Option 1: Current session (export + reconstruct in one step)
"Export and reconstruct this session --reconstruct"

# Option 2: Already-exported file
"Reconstruct orchestration from old-session.md --reconstruct"
```

> **Note:** `/export --reconstruct` won't work because `/export` is a built-in command that doesn't accept flags. Use the natural language commands above instead.

**Also available:**
```bash
# Full reconstruction with confidence scores
"Analyze this session --audit"

# Step-by-step walkthrough
"Walk me through what happened --replay"

# Compare original vs annotated
"Show reconstruction diff --diff"
```

**What gets reconstructed:**
- Skill invocations (inferred from output patterns)
- Agent reasoning (inferred from results)
- Decision points (inferred from choices made)
- Compound learning (inferred from behavior changes)

**Example output with `--reconstruct`:**

```markdown
[RECONSTRUCTED SKILL LOGIC]
Skill: idea-validator
Based on the output pattern, this skill likely instructed:
1. Problem clarity analysis (evidence: "clear problem" in output)
2. Market need validation (evidence: reference to "demand signals")
Confidence: 85%

[RECONSTRUCTED DECISION]
At this point, the session chose monolith over microservices.
Likely tradeoffs considered:
- Monolith advantage: Faster to ship, simpler debugging
- Microservices advantage: Better scaling
- Why monolith won: Early stage, need to validate first
Confidence: 70%
```

---

## When to Use What

| Scenario | Use | Why |
|----------|-----|-----|
| Starting a new project for YC demo | `--showcase` | Captures everything at 95% accuracy |
| Building something you might want to share later | `--showcase` | Better to capture than reconstruct |
| Old session you forgot to showcase | `--reconstruct` | Infers what happened (~70% accuracy) |
| Session with partial showcase coverage | `--reconstruct` | Fills in gaps |
| Quick prototype, no demo needed | Neither | Just work normally |

---

## Complete Workflow Examples

### Example 1: YC Application Session

```bash
# 1. Start with showcase mode
"Build my-saas-idea --showcase"

# 2. Work through your project
# Claude narrates: skills activated, decisions made, agents spawned

# 3. Before finishing, ask for summary
"Prepare for export"

# 4. Export using built-in command
/export yc-showcase-session.md

# 5. Submit to YC
# Your export now shows full orchestration mastery
```

### Example 2: Retroactive Analysis

```bash
# 1. You have an old session export
# (exported earlier without --showcase)

# 2. Reconstruct what happened
"Reconstruct orchestration from old-session.md --reconstruct"

# 3. Review the annotated version
# Look for [RECONSTRUCTED] and [GAP] markers

# 4. Fill specific gaps if needed
"What decisions were made in the architecture phase? --audit"
```

### Example 3: Partial Coverage

```bash
# 1. Started without --showcase, realized mid-session
"Enable showcase mode now"

# 2. Finish the session (new parts are captured)
/export partial-session.md

# 3. Reconstruct the early parts
"Reconstruct orchestration for the parts before showcase was enabled --reconstruct"
```

---

## What Gets Captured vs Reconstructed

| Element | With `--showcase` | With `--reconstruct` |
|---------|-------------------|----------------------|
| Skill logic | ✅ Exact instructions | 🔶 Inferred from outputs |
| Agent reasoning | ✅ Narrated process | 🔶 Inferred from results |
| Decision tradeoffs | ✅ Explicit options | 🔶 Inferred from choices |
| Compound learning | ✅ Semantic meaning | 🔶 Inferred from patterns |
| Timing | ✅ Can be included | ❌ Cannot reconstruct |
| Tool call counts | ✅ Can be included | 🔶 Estimates only |

Legend: ✅ Full capture | 🔶 Partial inference | ❌ Cannot recover

---

## Reconstruction Confidence Markers

When using `--reconstruct`, outputs include confidence markers:

| Marker | Meaning |
|--------|---------|
| `[RECONSTRUCTED]` | Inferred, not captured (60-90% confidence) |
| `[VERIFIED]` | Explicitly present in transcript |
| `[UNCERTAIN]` | Low confidence inference (<50%) |
| `[GAP]` | Cannot reconstruct this element |

---

## Skills Included

| Skill | Purpose | Flags |
|-------|---------|-------|
| `showcase-export` | Capture orchestration in new sessions | `--showcase` |
| `session-reconstruct` | Analyze old sessions retroactively | `--reconstruct`, `--audit`, `--replay`, `--diff` |

---

## Use Cases

- **YC Applications**: Show "cracked agent wrangler" skills
- **Investor Demos**: Demonstrate technical depth and decision-making
- **Team Knowledge Sharing**: Show how complex sessions were orchestrated
- **Learning**: Understand how AI agents coordinate skills and subagents
- **Documentation**: Create detailed records of AI-assisted work

---

## Works With

- Claude Code
- Cursor
- Any agent that supports the Vercel Skills format

## Related

- [Vercel Skills](https://github.com/vercel-labs/skills) - Skills framework
- [Claude Code](https://claude.ai/code) - AI coding agent

## License

MIT
