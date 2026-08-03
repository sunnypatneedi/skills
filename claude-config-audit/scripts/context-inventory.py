#!/usr/bin/env python3
"""Measure what is auto-loaded into context BEFORE the first user message.

This is usually the dominant cost and the one nobody measures. Reports the four
always-loaded surfaces separately, because they have different fixes:

  skill/agent DESCRIPTIONS  - always loaded; bodies are not. Fix = rewrite descriptions.
  instruction files         - always loaded in full. Fix = move content out, leave pointers.
  memory index              - always loaded, and SILENTLY TRUNCATED past its limit.
  bodies / reference files  - loaded on demand. Reported for contrast, not as a cost.

Usage:
  python3 context-inventory.py [--project DIR] [--json]

Exit code 1 if the memory index exceeds its read limit (a correctness bug, not a size issue).
"""
import argparse, glob, json, os, re, sys

TOK = lambda s: round(len(s) / 3.6)          # chars->tokens, conservative for prose
MEMORY_LIMIT_KB = 24.4                       # harness read limit; past this it truncates


def frontmatter(path):
    """Return (description, body) for a SKILL.md / agent .md file."""
    try:
        t = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return "", ""
    if not t.startswith("---"):
        return "", t
    end = t.find("\n---", 3)
    if end < 0:
        return "", t
    head, body = t[3:end], t[end + 4:]
    m = re.search(r"^description:\s*\|?\s*(.*?)(?=\n[a-zA-Z_-]+:\s|\Z)", head, re.M | re.S)
    return (" ".join(m.group(1).split()) if m else ""), body


def scan_dir(root, label):
    rows = []
    for p in sorted(glob.glob(os.path.join(root, "*", "SKILL.md"))) + \
             sorted(glob.glob(os.path.join(root, "*.md"))):
        if os.path.basename(p) == "SKILL.md":
            slug = os.path.basename(os.path.dirname(p))
        else:
            slug = os.path.splitext(os.path.basename(p))[0]
        desc, body = frontmatter(p)
        rows.append(dict(scope=label, slug=slug, path=p, desc=desc,
                         words=len(desc.split()),
                         desc_tok=TOK(slug + ": " + desc), body_tok=TOK(body)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=os.getcwd())
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    proj, home = os.path.abspath(a.project), os.path.expanduser("~")

    items = []
    for root, label in [(f"{home}/.claude/skills", "skill:user"),
                        (f"{proj}/.claude/skills", "skill:project"),
                        (f"{home}/.claude/agents", "agent:user"),
                        (f"{proj}/.claude/agents", "agent:project")]:
        if os.path.isdir(root):
            items += scan_dir(root, label)
    for mk in glob.glob(f"{home}/.claude/plugins/cache/*/*/skills") + \
              glob.glob(f"{home}/.claude/plugins/cache/*/skills"):
        items += scan_dir(mk, "skill:plugin")

    # instruction-file chain, following @-imports one level
    instr, seen = [], set()
    cands = [f"{proj}/CLAUDE.md", f"{proj}/AGENTS.md", f"{home}/.claude/CLAUDE.md"]
    p = os.path.dirname(proj)
    while p and p != os.path.dirname(p) and p.startswith(home):
        cands.append(f"{p}/CLAUDE.md"); p = os.path.dirname(p)
    for f in cands:
        real = os.path.realpath(f)
        if not os.path.exists(f) or real in seen:
            continue
        seen.add(real)
        t = open(f, encoding="utf-8", errors="ignore").read()
        instr.append((f, len(t.splitlines()), TOK(t)))
        for imp in re.findall(r"^@(\S+)", t, re.M):
            ip = imp if os.path.isabs(imp) else os.path.join(os.path.dirname(f), imp)
            if os.path.exists(ip) and os.path.realpath(ip) not in seen:
                seen.add(os.path.realpath(ip))
                it = open(ip, encoding="utf-8", errors="ignore").read()
                instr.append((f"  @import {imp}", len(it.splitlines()), TOK(it)))

    # memory index (per-project auto-memory), if present
    enc = re.sub(r"[/.]", "-", proj)   # harness maps BOTH / and . to -
    mem_path, mem_tok, mem_kb, truncated = None, 0, 0.0, False
    for c in [f"{home}/.claude/projects/{enc}/memory/MEMORY.md",
              f"{proj}/.claude/memory/MEMORY.md"]:
        if os.path.exists(c):
            t = open(c, encoding="utf-8", errors="ignore").read()
            mem_path, mem_kb, mem_tok = c, len(t.encode()) / 1024, TOK(t)
            truncated = mem_kb > MEMORY_LIMIT_KB
            break

    desc_tok = sum(i["desc_tok"] for i in items)
    body_tok = sum(i["body_tok"] for i in items)
    instr_tok = sum(t for _, _, t in instr)
    # cap in BYTES (the limit is a byte limit) then convert; multibyte-dense
    # memory truncates at fewer characters than a naive char cap implies.
    cap_tok = round(MEMORY_LIMIT_KB * 1024 / (len(open(mem_path,"rb").read())
                    / max(len(open(mem_path,encoding="utf-8",errors="ignore").read()),1))
                    / 3.6) if mem_path else 0
    loaded_mem = min(mem_tok, cap_tok) if mem_path else 0
    total = desc_tok + instr_tok + loaded_mem

    if a.json:
        print(json.dumps(dict(always=total, descriptions=desc_tok, instructions=instr_tok,
                              memory=loaded_mem, memoryTruncated=truncated,
                              onDemandBodies=body_tok, items=len(items)), indent=1))
        return 1 if truncated else 0

    print("=" * 68)
    print("ALWAYS IN CONTEXT (before you type anything)")
    print("=" * 68)
    print(f"  skill/agent descriptions {desc_tok:>9,} tok   ({len(items)} items)")
    print(f"  instruction files        {instr_tok:>9,} tok")
    print(f"  memory index             {loaded_mem:>9,} tok" +
          ("   <-- TRUNCATED" if truncated else ""))
    print(f"  {'TOTAL':<24}{total:>9,} tok")
    print("\n  NOT COUNTED — measure separately before concluding anything about MCP:")
    print("    MCP tool schemas/instructions, harness-bundled skills, commands/,")
    print("    output styles. On MCP-heavy setups the schema surface can exceed")
    print("    everything above. A ~0 reading here is NOT evidence a server is free.")
    print(f"\n  (on-demand bodies, NOT always loaded: ~{body_tok:,} tok)")

    print("\n" + "-" * 68)
    print("INSTRUCTION CHAIN")
    for f, lines, tk in instr:
        print(f"  {f.replace(home,'~'):<48}{lines:>5}L {tk:>8,} tok")

    if mem_path:
        print("\n" + "-" * 68)
        print(f"MEMORY INDEX  {mem_kb:.1f}KB / {MEMORY_LIMIT_KB}KB limit")
        if truncated:
            print("  *** EXCEEDS THE READ LIMIT — it is silently truncated at load. ***")
            print("  Part of the memory never reaches context. This is a CORRECTNESS bug,")
            print("  not a size issue: fixing it does not reduce tokens, it restores content.")

    over = [i for i in items if i["words"] > 25]
    print("\n" + "-" * 68)
    print(f"DESCRIPTIONS OVER 25 WORDS: {len(over)}/{len(items)}  "
          f"holding ~{sum(i['desc_tok'] for i in over):,} tok")
    print(f"  reclaimable by rewriting to <=25 words: "
          f"~{max(0, sum(i['desc_tok'] for i in over) - 55*len(over)):,} tok\n")
    for i in sorted(over, key=lambda x: -x["desc_tok"])[:20]:
        print(f"  {i['desc_tok']:>5} tok {i['words']:>4}w  {i['scope']:<15}{i['slug']}")
    print("\n  NOTE: fat descriptions concentrate in the skills you KEEP. Archiving")
    print("  unused skills does not fix them — rewriting is a separate lever.")
    return 1 if truncated else 0


if __name__ == "__main__":
    sys.exit(main())
