# Ledger template — the Phase 6 record

Write to `docs/engineering/claude-config.md` (or the repo's equivalent). **Append a new dated
section if the file exists; never overwrite** — the value is the series, not the snapshot.

The ledger exists so the next audit doesn't re-litigate settled questions. Two sections do that
work and are the ones most often skipped: **"Kept against the initial proposal"** (stops a cut
being re-proposed every cycle) and **re-add criteria** (turns "we deleted it" into a decision that
can be reversed on evidence).

---

```markdown
## <YYYY-MM-DD> — <audit scope>

**Snapshot:** `<path to archive>` (<size>, <n> entries — <what it covers>).
Restore: `<exact command>`

### Headline

<If the thing the audit was commissioned to fix turned out not to be the cost, say that in the
first line. State which axis actually dominates.>

| config | median (n runs) | vs baseline |
|---|---|---|
| current | | |
| <isolation variant> | | |
| floor (safe-mode) | | |

<One line on measurement method: interleaved against the floor, medians, n.>

| component | measured cost | how measured |
|---|---|---|

### Killed / changed

| # | item | path | cost | why removed | re-add criteria |
|---|---|---|---|---|---|
| 1 | | | | | <what must be true + the exact restore command> |

### Kept, against the initial proposal

<Items proposed for removal and then reversed, each with the evidence that reversed it.
This section is what stops the next audit re-proposing them.>

### Rewritten (kept the defence, dropped the cost)

<For anything protective: what the old cost was, what the mechanism is now, and how equivalence
was verified — replay match rate over the real corpus, not example counts.>

### Before / after — <date>

<Four axes. Report the controlled comparison, not raw wall time, and say which is meaningful.>

| | before | after |
|---|---|---|
| startup config overhead (current − floor) | | |
| absolute median startup | | <note if environmental> |
| per-session hook overhead | | |
| always-loaded context | | |

### Notes / open items

<Numbered. Include: what was NOT completed and its cost; blast-radius flags for anything global;
correctness fixes labelled as such rather than as savings.>

### Appendices

<Full lists for anything removed in bulk — the record must survive without the session transcript
or any temp directory. One appendix per bulk operation.>
```

---

## Reporting honesty rules

These are not stylistic. An audit that overstates its result gets its next recommendation ignored.

- **Under 20% is not a win.** Say so plainly.
- **If absolute numbers moved the wrong way**, report the raw AND controlled figures and state
  which is meaningful and why.
- **Correct your own earlier claims explicitly**, with the number that overturned them. An audit
  that measured something and changed its mind is more trustworthy, not less.
- **Distinguish savings from correctness fixes.** Making a truncated file load fully is not a
  token reduction.
- **List what you did not complete**, and what it would cost to finish.
- **Never report a cut's benefit as the sum of an axis it didn't affect.**
