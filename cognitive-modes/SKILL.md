---
name: cognitive-modes
description: >
  Meta-skill that maps cognitive mode-switch words to appropriate thinking behaviors and skills.

  **AUTO-INVOKE when user uses these trigger patterns:**
  - Depth: "rigorous", "first-principles", "mechanistic", "axiomatic", "falsifiable", "steelman", "non-trivial", "exhaustive", "load-bearing", "dispositive", "ultra think hard"
  - Reframe: "reimagine", "orthogonal", "contrarian", "subversive", "invert", "counterfactual", "zero-based", "provocative", "transmute", "reframe"
  - Precision: "probabilities", "bounded", "monotonic", "asymptotic", "invariant", "order of magnitude", "sensitivity analysis", "convex", "distribution", "marginal", "dimensionality"
  - Tradeoff: "sacrifice", "irreversible", "binding constraint", "pareto", "second-order", "opportunity cost", "regret minimization", "non-negotiable", "asymmetric"
  - Quality: "elegant", "idiomatic", "canonical", "production-grade", "battle-tested", "minimalist", "composable", "tasteful", "crisp"
  - Systems: "emergent", "cascading", "equilibrium", "phase transition", "feedback loop", "attractor", "entropy"
  - Epistemic: "Bayesian", "calibrated", "crux", "pre-mortem", "adversarial", "sparse", "steel-thread", "epistemic humility", "signal-to-noise"
---

# Cognitive Mode-Switch Words

Words that don't describe what you want — they rewire **how** you approach the problem.

## Quick Reference: Word → Behavior

When the user uses these words, activate the corresponding thinking mode:

### Depth & Rigor

| Word | Thinking Mode | Invoke Skill |
|------|---------------|--------------|
| **Rigorous** | Proof-like thinking — every step must earn its place | `rigorous-thinking` |
| **First-principles** | Derive from ground truth, strip borrowed reasoning | `rigorous-thinking` |
| **Mechanistic** | Demand causal chains: "A causes B because..." | `rigorous-thinking` |
| **Axiomatic** | Each claim follows logically from stated premises | `rigorous-thinking` |
| **Falsifiable** | Flip to "what would prove this wrong?" | `rigorous-thinking` |
| **Steelman** | Construct strongest possible version of opposing view | `rigorous-thinking`, `rigorous-exchange` |
| **Non-trivial** | Skip basics, assume expertise, go deeper | — |
| **Exhaustive** | Complete coverage, no blind spots, breadth before depth | — |
| **Necessary and sufficient** | Exact boundaries — no more, no less | `claim-validator` |
| **Load-bearing** | Identify the single assumption everything depends on | `rigorous-thinking` |
| **Dispositive** | Find the one fact that settles the debate | `rigorous-thinking` |
| **Ultra think hard** | Maximum cognitive effort, no shortcuts anywhere | `rigorous-thinking` |

### Creative Reframing

| Word | Thinking Mode | Invoke Skill |
|------|---------------|--------------|
| **Reimagine** | Break fixed mental models — clean-slate vision | `ideacritic` |
| **Orthogonal** | Think perpendicular to the current frame | `ideacritic` |
| **Contrarian** | Deliberate inversion of the popular view | `ideacritic` |
| **Subversive** | Question the premise itself, not just disagree | `ideacritic` |
| **Invert** | Instead of "how to succeed," ask "how to guarantee failure" | `inversion-analysis` |
| **Counterfactual** | "What would have happened if X didn't occur?" | `inversion-analysis` |
| **Zero-based** | Start from scratch — if you had none of this, what would you build? | `ideacritic` |
| **Provocative** | Bold, non-consensus ideas you'd never say in a meeting | `ideacritic` |
| **Transmute** | Convert a weakness into a strength | `ideacritic` |
| **Reframe** | Re-examine whether you're solving the right problem | `ideacritic` |
| **Degenerate case** | Push variables to 0, 1, or infinity to reveal hidden structure | — |
| **Adjacent possible** | Constrain creativity to what's buildable from current position | — |

### Precision & Mathematical

| Word | Thinking Mode | Invoke Skill |
|------|---------------|--------------|
| **Probabilities/Distribution** | Full statistical reasoning — likelihoods, not certainties | `claim-validator` |
| **Bounded** | Force upper and lower limits on any assertion | `claim-validator`, `unit-economics-validator` |
| **Monotonic** | Does this always increase/decrease, or are there reversals? | — |
| **Asymptotic** | What happens as scale approaches infinity? | — |
| **Invariant** | Identify the constant in a sea of variables | — |
| **Order of magnitude** | Calibration without false precision | `unit-economics-validator` |
| **Sensitivity analysis** | Which variable, if wrong by 2x, breaks the conclusion? | `unit-economics-validator` |
| **Convex** | Is the payoff shape concave (diminishing) or convex (accelerating)? | — |
| **Marginal** | What does one more unit buy you? Not average, incremental. | `pricing-strategy` |
| **Dimensionality** | How many independent axes actually matter? | — |
| **Closed-form** | Demand a computable formula, not hand-waving | — |

### Tradeoff & Decision

| Word | Thinking Mode | Invoke Skill |
|------|---------------|--------------|
| **Sacrifice** | Name what you're willing to lose — make tradeoffs explicit | `operator-playbook` |
| **Irreversible** | Can we undo this or not? One-way vs two-way doors | `operator-playbook` |
| **Binding constraint** | Identify the single bottleneck | `systems-decompose` |
| **Pareto** | What 20% of effort gets 80% of the result? | `operator-playbook` |
| **Second-order effects** | What happens *after* the thing happens? Ripple effects. | `systems-review` |
| **Opportunity cost** | Is this better than the next best alternative? | `operator-playbook` |
| **Regret minimization** | Which choice do you regret least looking back from 10 years out? | `operator-playbook` |
| **Non-negotiable** | What will you absolutely not bend on? | — |
| **Asymmetric** | Where upside and downside are mismatched | — |
| **Reversibility gradient** | Not binary — place decision on the spectrum | — |

### Quality & Craft

| Word | Thinking Mode | Invoke Skill |
|------|---------------|--------------|
| **Elegant** | Simplicity, completeness, and surprise in one solution | `code-review`, `software-architecture` |
| **Idiomatic** | Domain-native solutions, not generic ones | `code-review` |
| **Canonical** | The accepted best practice, not improvisation | `code-review` |
| **Production-grade** | Error handling, edge cases, monitoring, logging | `code-review`, `security-review` |
| **Battle-tested** | Proven approaches over clever theory | `software-architecture` |
| **Minimalist** | Remove everything that isn't essential | `simplify` |
| **Composable** | Modular design where pieces can be mixed and matched | `software-architecture` |
| **Tasteful** | Aesthetic reasoning — what *feels* right to an expert? | — |
| **Crisp** | Precision in language — every word must earn its place | `deslop` |

### Systems Thinking

| Word | Thinking Mode | Invoke Skill |
|------|---------------|--------------|
| **Emergent** | What arises from interactions that no individual part possesses? | `systems-decompose` |
| **Cascading** | Maps domino effects through a system | `systems-review` |
| **Equilibrium** | Is this equilibrium stable or unstable? What disrupts it? | — |
| **Phase transition** | At what threshold does the system fundamentally shift? | — |
| **Feedback loop** | Is this positive (amplifying) or negative (stabilizing)? | `systems-decompose` |
| **Attractor** | Where does this naturally converge? | — |
| **Entropy** | What's degrading over time? What maintenance prevents collapse? | `techdebt` |

### Epistemic Calibration

| Word | Thinking Mode | Invoke Skill |
|------|---------------|--------------|
| **Bayesian** | Explicit priors, evidence weighting, posterior updates | `rigorous-thinking` |
| **Calibrated** | Honest probability assignment to claims | `rigorous-thinking` |
| **Crux** | Single disagreement that, if settled, resolves everything | `rigorous-exchange` |
| **Pre-mortem** | Assume this failed. Now explain why. | `inversion-analysis` |
| **Evidence-weighted** | Which signals carry the most weight and why? | `rigorous-thinking` |
| **Adversarial** | Assume someone is actively trying to break this | `security-review` |
| **Sparse** | Strip away everything except what carries information | `rigorous-thinking` |
| **Steel-thread** | Thinnest possible end-to-end proof of concept | — |
| **Epistemic humility** | Honest "here's what I don't know" disclosure | `rigorous-thinking` |
| **Signal-to-noise** | What fraction of this information changes decisions? | `rigorous-thinking` |

---

## Power Combos

The highest-leverage technique: **pair a depth word with a constraint word.**

| Combo | Effect | Invoke |
|-------|--------|--------|
| **Rigorous + Elegant** | Airtight reasoning that's also beautiful and simple | `rigorous-thinking` + `code-review` |
| **Reimagine + First-principles** | Clean-slate vision built from ground truth | `ideacritic` + `rigorous-thinking` |
| **Ultra think hard + Sacrifice** | Maximum depth applied to what must be cut | `rigorous-thinking` + `operator-playbook` |
| **Falsifiable + Bounded** | Testable claims with defined ranges | `rigorous-thinking` + `claim-validator` |
| **Adversarial + Exhaustive** | Complete threat surface mapping | `security-review` |
| **Contrarian + Evidence-weighted** | Bold takes backed by real data | `ideacritic` + `rigorous-thinking` |
| **Invert + Pre-mortem** | Failure-first scenario planning | `inversion-analysis` |
| **Sparse + Dispositive** | Cut to the one thing that decides everything | `rigorous-thinking` |
| **Distribution + Sensitivity analysis** | Full outcome range with fragility mapping | `unit-economics-validator` |

---

## Usage

This skill auto-invokes when the user uses trigger words. It then:

1. **Activates the thinking mode** corresponding to the word(s)
2. **Invokes relevant skills** if deeper analysis is needed
3. **Applies the cognitive constraint** to all reasoning in the response

### Examples

**User:** "Be rigorous: why won't this architecture scale?"
→ Invoke `rigorous-thinking`, apply proof-like reasoning

**User:** "Give me the contrarian take on our pricing."
→ Invoke `ideacritic`, deliberately invert the popular view

**User:** "Ultra think hard + sacrifice: what do we cut?"
→ Maximum cognitive effort applied to naming tradeoffs

**User:** "Sensitivity analysis on our unit economics."
→ Invoke `unit-economics-validator`, identify fragile assumptions

---

## The Meta-Pattern

Words that constrain the **solution space** in a non-obvious way always outperform words that merely describe desired **quality**.

- ❌ "Good" is useless
- ✅ "Elegant" rewires the entire approach
- ✅ "Falsifiable" flips from prove-right to prove-wrong
- ✅ "Sparse" strips away noise before answering

**When you hear a trigger word, change HOW you think, not just WHAT you output.**
