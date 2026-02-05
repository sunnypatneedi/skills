---
name: session-reconstruct
description: Retroactively analyze exported sessions to reveal orchestration that wasn't captured. Use --reconstruct for old sessions where you forgot --showcase. Infers skill logic, agent internals, and decision rationale from transcript patterns with 60-80% accuracy.
triggers:
  - "--reconstruct"
  - "--audit"
  - "--replay"
  - "--diff"
  - "reconstruct session"
  - "reconstruct orchestration"
  - "analyze export"
  - "analyze session"
  - "what happened in this session"
  - "fill in gaps"
---

# Session Reconstruct

Retroactively analyze and annotate exported sessions to reveal orchestration that wasn't captured.

> **Note:** This skill analyzes sessions exported via the built-in `/export` command or raw JSONL logs from `~/.claude/projects/`. It INFERS orchestration details that weren't narrated—accuracy is ~60-80% vs ~95% for `--showcase` mode.

## Quick Start

```bash
# For current session (export + reconstruct in one step)
"Export and reconstruct this session --reconstruct"

# For already-exported file
"Reconstruct orchestration from session.md --reconstruct"

# Other options
"Analyze this session --audit"
"Walk through what happened --replay"
```

> **Important:** `/export --reconstruct` won't work because `/export` is a built-in command that doesn't accept flags. Use the natural language commands above instead.

**For NEW sessions, use `showcase-export` with `--showcase` instead.**

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│ Input Sources                                           │
├─────────────────────────────────────────────────────────┤
│ 1. /export output (.md or .txt)                         │
│ 2. Raw JSONL logs (~/.claude/projects/*.jsonl)          │
│ 3. Community tool exports (claude-code-log, etc.)       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Reconstruction Engine                                   │
├─────────────────────────────────────────────────────────┤
│ • Identifies skill invocations from output patterns     │
│ • Infers agent reasoning from results                   │
│ • Reconstructs decision points from choices made        │
│ • Estimates compound learning from behavior changes     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Output: Annotated Session                               │
├─────────────────────────────────────────────────────────┤
│ Original transcript + [RECONSTRUCTED] markers           │
│ with confidence scores for each inference               │
└─────────────────────────────────────────────────────────┘
```

---

## When to Use This

| Scenario | Use This? | Why |
|----------|-----------|-----|
| Exported session without showcase mode | ✅ Yes | Reconstruct what happened |
| Old session you want to showcase | ✅ Yes | Add orchestration visibility |
| Session with partial showcase | ✅ Yes | Fill in gaps |
| New session starting now | ❌ No | Use `--showcase` at start |

---

## What Gets Reconstructed

### 1. Skill Logic (from outputs)
```markdown
[RECONSTRUCTED SKILL LOGIC]
Skill: idea-validator
Based on the output pattern, this skill likely instructed:
1. Problem clarity analysis (evidence: "clear problem" in output)
2. Market need validation (evidence: reference to "demand signals")
3. Competitive moat assessment (evidence: "defensibility" section)
Confidence: 85%
```

### 2. Subagent Internals (from results)
```markdown
[RECONSTRUCTED AGENT PROCESS]
Agent: rigorous-thinking
Final result mentioned: "4/5 counterarguments addressed"
Inferred process:
- Generated ~5 counterarguments (evidence: "4/5" ratio)
- Tested each against evidence (evidence: "addressed" language)
- Tool calls: ~4-6 (typical for this agent type)
Confidence: 70%
```

### 3. Decision Points (from choices made)
```markdown
[RECONSTRUCTED DECISION]
At this point, the session chose X over Y.
Likely tradeoffs considered:
- X advantage: [inferred from context]
- Y advantage: [what was given up]
- Why X won: [reasoning based on subsequent actions]
Confidence: 60%
```

### 4. Compound Learning (from patterns)
```markdown
[RECONSTRUCTED COMPOUND UPDATE]
A pattern was likely extracted here:
- Pattern: "[inferred from repeated behavior]"
- Evidence in session: [what suggested this]
- Likely confidence update: [estimate]
Confidence: 50%
```

---

## Reconstruction Protocol

### Step 1: Identify Orchestration Points

Scan for:
- Skill invocations (`Skill:`, `🔧`, skill names mentioned)
- Agent spawns (`Task`, `🤖`, "spawning", "agent")
- Phase transitions (numbered sections, "Phase", "Step")
- Decision indicators ("chose", "decided", "instead of", "rather than")
- Compound signals (database mentions, "pattern", "learned", "updated")

### Step 2: Mark Confidence Levels

| Confidence | Meaning | Evidence Required |
|------------|---------|-------------------|
| 90%+ | Almost certain | Explicit mention + output matches |
| 70-89% | High confidence | Output strongly implies process |
| 50-69% | Moderate | Reasonable inference from context |
| 30-49% | Speculative | Possible but uncertain |
| <30% | Guess | Flag as "[UNCERTAIN]" |

### Step 3: Generate Annotated Version

```markdown
# Session Reconstruction: [Project Name]

## Reconstruction Metadata
- Original session: [filename]
- Reconstruction date: [date]
- Overall confidence: [average %]
- Gaps identified: [count]

---

[ORIGINAL CONTENT]
User: Build sessionizer

[RECONSTRUCTION]
This request triggered the following orchestration:
- Skills likely loaded: idea-validator, software-architecture
- Why: "Build" keyword + project name suggests full build pipeline
- Confidence: 75%
```

---

## Reconstruction Markers

| Marker | Meaning |
|--------|---------|
| `[RECONSTRUCTED]` | Inferred, not captured |
| `[VERIFIED]` | Explicitly in transcript |
| `[UNCERTAIN]` | Low confidence inference |
| `[GAP]` | Cannot reconstruct |

---

## Complete Workflow

```bash
# If you FORGOT --showcase:

# 1. Export the session using built-in command
/export my-session.md

# 2. Reconstruct orchestration using this skill
"Reconstruct orchestration from my-session.md --audit"

# 3. Output: Annotated version with [RECONSTRUCTED] markers
```

---

## Comparison with showcase-export

| Timing | Skill | Flag | Accuracy |
|--------|-------|------|----------|
| Before session | showcase-export | `--showcase` | 95% |
| After session | session-reconstruct | `--audit` | 60-80% |

**Best practice:** Always start with `--showcase`. Use `--reconstruct` only for old sessions or gaps.

---

## Limitations

Reconstruction CANNOT provide:
1. **Exact subagent reasoning** - Can only infer from results
2. **Precise tool call counts** - Estimates only
3. **Actual confidence scores** - Must approximate
4. **Internal decision debates** - Only see final choice
5. **Timing information** - Unless explicitly logged

Always flag these limitations in the reconstructed output.

---

## Installation

```bash
npx skills add sunnypatneedi/skills
```
