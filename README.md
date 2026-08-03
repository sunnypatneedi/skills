# AI Lingo + Session Skills

**Six powerful skills for AI-assisted thinking, session orchestration, and project hygiene.**

## Installation

```bash
npx skills add sunnypatneedi/skills
```

---

## 🧠 AI Lingo

**Transform how Claude thinks by using mode-switch words.**

Instead of saying "think about this," use specific cognitive trigger words that activate different thinking patterns:

### Quick Start

Just use these words naturally in your prompts:

```bash
# Depth & Rigor
"Let's think about this rigorously"
"Approach this from first-principles"
"What's the load-bearing assumption?"

# Creative Reframing
"Let's reimagine this problem"
"What's the contrarian take?"
"How could we invert this?"

# Precision & Math
"What are the probabilities here?"
"Give me order of magnitude estimates"
"What's the sensitivity analysis?"

# Tradeoffs
"What must we sacrifice?"
"What's the binding constraint?"
"Name the opportunity cost"

# Quality
"Make this elegant and idiomatic"
"Show me the canonical approach"
"What's production-grade here?"
```

### How It Works

When you use these words, Claude automatically:
1. **Recognizes the cognitive mode** you're requesting
2. **Activates specialized thinking skills** (rigorous-thinking, ideacritic, etc.)
3. **Adapts its reasoning style** to match your intent

### Full Trigger Word Reference

| Mode | Trigger Words | What You Get |
|------|---------------|--------------|
| **Depth & Rigor** | rigorous, first-principles, mechanistic, axiomatic, steelman, ultra think hard | Proof-like thinking, causal chains, no hand-waving |
| **Creative Reframing** | reimagine, orthogonal, contrarian, subversive, invert, zero-based | Break mental models, perpendicular thinking |
| **Precision & Math** | probabilities, bounded, monotonic, order of magnitude, sensitivity analysis | Statistical reasoning, calibrated estimates |
| **Tradeoff & Decision** | sacrifice, irreversible, binding constraint, pareto, opportunity cost | Explicit tradeoffs, identify bottlenecks |
| **Quality** | elegant, idiomatic, canonical, production-grade, battle-tested, composable | Clean, tasteful, maintainable solutions |
| **Systems** | emergent, cascading, equilibrium, feedback loop, entropy | Systems-level thinking |
| **Epistemic** | Bayesian, calibrated, crux, pre-mortem, adversarial, steel-thread | Reasoning about uncertainty |

### Examples in Practice

**Before (generic):**
> "Help me validate this startup idea"

**After (cognitive mode):**
> "Let's think about this **rigorously** — what's the **load-bearing** assumption? Give me **probabilities** not certainties, and what's the **contrarian** take?"

This triggers:
- ✅ rigorous-thinking skill (proof-like analysis)
- ✅ Focused on critical assumptions
- ✅ Statistical reasoning mode
- ✅ ideacritic skill (contrarian perspectives)

---

## 📊 Session Orchestration Skills

**Make your AI agent orchestration visible for demos, YC applications, and investor meetings.**

### showcase-export

Capture **what skills triggered, what decisions were made, and why** — at 95% accuracy.

**Usage:**
```bash
# Start session with showcase mode
"Build my-project --showcase"

# Work normally... Claude narrates orchestration

# Export when done
/export session.md
```

**Captures:**
- Skill logic (exact instructions each skill gave Claude)
- Subagent reasoning (reconstructed internal process)
- Decision rationale (tradeoffs considered)
- Compound learning (semantic patterns discovered)

### session-reconstruct

**Retroactively** analyze old sessions you didn't showcase — at ~70% accuracy.

**Usage:**
```bash
# Reconstruct from existing export
"Reconstruct orchestration from old-session.md --reconstruct"

# Or analyze current session
"Export and reconstruct this session --reconstruct"
```

**Infers:**
- Skill invocations (from output patterns)
- Agent reasoning (from results)
- Decision points (from choices made)
- Compound learning (from behavior changes)

---

## 🗺️ Project Hygiene Skills

### 4n1d — Roadmap Triage

**Keep your roadmap honest with a 5-file framework: NOW / NEXT / NOT-YET / NEVER / DONE.**

Run at session end, after shipping, or whenever the roadmap feels stale. Scans the conversation, checks anti-patterns (NOW >4 items, stale triggers, zombie ideas), and proposes promotions, demotions, and archives across all five files.

**Usage:**
```bash
/4n1d
"update roadmap"
"what should go in NOW?"
"session wrap-up"
```

**What it checks:**
- Items completed but not in DONE.md
- NEXT triggers that have actually fired
- NOT-YET ideas that have gone stale (>90 days)
- NOW items older than 14/30 days
- Missing `[learn]` items in NOW (executing without validating)

If your project has no `docs/roadmap/` yet, the skill offers to bootstrap one.

### claudemd-improve — CLAUDE.md Audit & Maintenance

**Audit, clean, and enrich the highest-leverage file in your repo.**

`CLAUDE.md` shapes every AI agent session. This skill detects stale rules, contradictions, missing pitfalls, dead file references, and bloat — then fixes them.

**Usage:**
```bash
"audit my CLAUDE.md"
"my CLAUDE.md is outdated"
"trim CLAUDE.md"
"enrich CLAUDE.md with what we learned"
"quick audit"
```

**Modes:**
- **Full audit** — staleness, contradictions, completeness, bloat, reference integrity (~5 min)
- **Quick audit** — top 3 problems + score (~1 min)
- **Enrich** — pull recent git log into CLAUDE.md additions
- **Trim** — find what to move into reference docs

> Operates on `CLAUDE.md` only. If you also keep an `AGENTS.md`, run a separate audit for it.

---

## Skills Included

| Skill | Purpose | How to Use |
|-------|---------|------------|
| **ai-lingo** | Activate specialized thinking modes | Use trigger words: "rigorous", "reimagine", "probabilities", etc. |
| **showcase-export** | Capture orchestration in new sessions | Add `--showcase` flag when starting |
| **session-reconstruct** | Analyze old sessions retroactively | Add `--reconstruct` flag to exports |
| **4n1d** | Roadmap triage across NOW/NEXT/NOT-YET/NEVER/DONE | `/4n1d` or "update roadmap" |
| **claudemd-improve** | Audit and improve CLAUDE.md | "audit my CLAUDE.md" |
| **setup-audit** | Measure and prune a slow/bloated harness | "why is my session slow", "prune my MCP servers" |

---

## Use Cases

**AI Lingo:**
- Strategic thinking for startup decisions
- Technical architecture discussions
- Code review requiring taste and rigor
- Problem-solving that needs reframing
- Design decisions with tradeoffs

**Session Skills:**
- YC applications (show agent orchestration mastery)
- Investor demos (technical depth + decision-making)
- Team knowledge sharing (how complex sessions work)
- Learning (understand AI agent coordination)

**Project Hygiene:**
- End-of-session roadmap triage (4n1d)
- Onboarding new contributors via a clean CLAUDE.md
- Catching dead doc references before they confuse agents
- Keeping the highest-leverage instruction file accurate

---

## Detailed Documentation

### Showcase Mode

<details>
<summary>Click to expand full showcase documentation</summary>

**When to use:** Starting a new project you might demo later

```bash
# 1. Start with showcase
"Build my-saas-idea --showcase"

# 2. Work through project
# Claude narrates: skills activated, decisions made, agents spawned

# 3. Export
/export yc-showcase-session.md
```

**Example output:**

```markdown
## 🔧 Skill Activated: idea-validator

**This skill instructs me to:**
1. Analyze problem clarity using the "would I pay for this" test
2. Check market need via revealed demand signals
3. Assess competitive moat using idea maze framework

### 📋 Decision Point: Architecture Approach

| Option | Pros | Cons |
|--------|------|------|
| Monolith | Simple, fast to ship | Scaling limits |
| Microservices | Scalable | Complexity overhead |

**Decision:** Monolith first
**Rationale:** Ship fast, validate, refactor later if needed
```

</details>

### Reconstruct Mode

<details>
<summary>Click to expand full reconstruct documentation</summary>

**When to use:** Old session you forgot to showcase

```bash
# Reconstruct from file
"Reconstruct orchestration from old-session.md --reconstruct"

# Also available:
"Analyze this session --audit"  # With confidence scores
"Walk me through what happened --replay"  # Step-by-step
"Show reconstruction diff --diff"  # Original vs annotated
```

**Example output:**

```markdown
[RECONSTRUCTED SKILL LOGIC]
Skill: idea-validator
Based on output pattern, likely instructed:
1. Problem clarity analysis (evidence: "clear problem" in output)
2. Market need validation (evidence: reference to "demand signals")
Confidence: 85%

[RECONSTRUCTED DECISION]
Session chose monolith over microservices.
Likely tradeoffs:
- Monolith advantage: Faster to ship
- Microservices advantage: Better scaling
- Why monolith won: Early stage
Confidence: 70%
```

</details>

### AI Lingo Deep Dive

<details>
<summary>Click to expand full cognitive modes reference</summary>

#### Depth & Rigor Triggers

| Word | Thinking Mode | Auto-Invokes |
|------|---------------|--------------|
| **Rigorous** | Proof-like thinking — every step must earn its place | `rigorous-thinking` |
| **First-principles** | Derive from ground truth, strip borrowed reasoning | `rigorous-thinking` |
| **Mechanistic** | Demand causal chains: "A causes B because..." | `rigorous-thinking` |
| **Steelman** | Construct strongest possible version of opposing view | `rigorous-exchange` |
| **Load-bearing** | Identify the single assumption everything depends on | `rigorous-thinking` |
| **Ultra think hard** | Maximum cognitive effort, no shortcuts anywhere | `rigorous-thinking` |

#### Creative Reframing Triggers

| Word | Thinking Mode | Auto-Invokes |
|------|---------------|--------------|
| **Reimagine** | Break fixed mental models — clean-slate vision | `ideacritic` |
| **Orthogonal** | Think perpendicular to the current frame | `ideacritic` |
| **Contrarian** | Deliberate inversion of the popular view | `ideacritic` |
| **Invert** | "How to guarantee failure" instead of "how to succeed" | `inversion-analysis` |
| **Zero-based** | If you had none of this, what would you build? | `ideacritic` |

#### Precision & Mathematical Triggers

| Word | Thinking Mode | Auto-Invokes |
|------|---------------|--------------|
| **Probabilities** | Full statistical reasoning — likelihoods not certainties | `claim-validator` |
| **Bounded** | Force upper and lower limits on assertions | `claim-validator` |
| **Order of magnitude** | Calibration without false precision | `unit-economics-validator` |
| **Sensitivity analysis** | Which variable, if wrong by 2x, breaks conclusion? | `unit-economics-validator` |

#### Tradeoff & Decision Triggers

| Word | Thinking Mode | Auto-Invokes |
|------|---------------|--------------|
| **Sacrifice** | Make tradeoffs explicit — name what you're willing to lose | `operator-playbook` |
| **Irreversible** | One-way vs two-way doors | `operator-playbook` |
| **Binding constraint** | Identify the single bottleneck | `systems-decompose` |
| **Pareto** | Find 80/20 leverage points | `operator-playbook` |

#### Quality Triggers

| Word | Thinking Mode | Auto-Invokes |
|------|---------------|--------------|
| **Elegant** | Minimize complexity while maximizing power | `deslop` |
| **Idiomatic** | Follow language/framework conventions | `code-review` |
| **Production-grade** | Battle-tested, handles edge cases | `security-review` |
| **Composable** | Small pieces that combine well | `refactor` |

</details>

---

## Comparison Table

| Scenario | Use ai-lingo | Use showcase | Use reconstruct |
|----------|---------------------|--------------|-----------------|
| Strategic startup decision | ✅ "Let's think **rigorously**" | ❌ | ❌ |
| Building demo for YC | ✅ "Make this **elegant**" | ✅ `--showcase` | ❌ |
| Review old work session | ❌ | ❌ | ✅ `--reconstruct` |
| Architecture tradeoffs | ✅ "What's the **binding constraint**?" | ✅ `--showcase` | ❌ |
| Quick prototype | ❌ (unless you want quality) | ❌ | ❌ |

---

## ⏱️ Setup Audit

**Your session is slow. Find out which file is responsible — by measuring, not guessing.**

Six surfaces load before you type a word, and they charge on four different meters. The one people
usually blame — MCP servers at startup — is often the cheapest. A 40 ms hook firing on every tool
call outweighs two seconds of startup by an order of magnitude.

### Quick Start

```bash
"why is my session slow"
"prune my MCP servers"
"too much context loads before I type"
```

### What it measures

| Meter | Paid | Where it usually hides |
|-------|------|------------------------|
| Startup | Once per session | `stdio` MCP servers spawned via `npx`/`uvx` |
| Per tool call | Every Bash/Edit/Read | Hooks in `settings.json` — ×100–200 per session |
| Per session | Every hook trigger | A `git fetch` or `curl` inside a per-call hook |
| Context | Every single turn | Skill descriptions, the CLAUDE.md chain, MCP tool schemas |

### The workflow

Seven phases, in an order where each one exists to stop a specific way the previous one goes wrong:
discover and snapshot → measure all four meters → inventory with real usage evidence → propose
**keep / kill / rewrite / defer** → adversarial gate → apply and verify by replaying your real
command history → record a ledger with re-add criteria for every cut.

### Three rules it enforces

- **Measure before you prescribe** — and let the measurement overrule the plan. The suspected cause
  frequently measures zero.
- **Rewrite, don't delete, anything protective.** A guard that costs too much is a guard with a bug.
  Fix the cost and keep the defence.
- **Grep the name before you remove the thing.** Anything documented as a remedy fails *silently*
  when deleted — no error, just an instruction nobody can follow.

### Included scripts

| Script | Does |
|--------|------|
| `measure-startup.sh` | Interleaved startup timing against an isolation floor — the only cross-batch-comparable number |
| `context-inventory.py` | Tokens auto-loaded before your first message, by surface; flags a silently-truncated memory index |
| `usage-evidence.py` | Real MCP/tool call counts from your transcripts — turns per-call cost into per-session cost |

> **Note on the numbers.** The worked examples come from one real audit of one machine. They are
> labelled as observations, not laws — a setup with three `npx` MCP servers and no hooks inverts the
> ranking entirely. The skill tells you to measure before cutting for exactly this reason.

---

## Guides

- [Setting Up GitHub Sponsors](guides/github-sponsors-setup.md) — How to add the "Sponsor this project" button and structure your sponsors profile

---

## Works With

- **Claude Code** (Anthropic)
- **Cursor** (Anysphere)
- Any agent supporting Vercel Skills format

## Related

- [Vercel Skills](https://github.com/vercel-labs/skills) - Skills framework
- [Claude Code](https://claude.ai/code) - AI coding agent

## License

MIT

---

## Maintenance Note

⚠️ **This is a curated collection** — not all global skills are synced here. For the full library, see the main skills repository.
