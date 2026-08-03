#!/usr/bin/env python3
"""Usage evidence from stored session transcripts — what this project ACTUALLY calls.

Answers three questions that intuition gets wrong:
  1. which MCP servers have ever been invoked here (and how often)
  2. how many tool calls a typical session makes  -> turns per-call hook cost into
     per-session cost, which is where hooks actually hurt
  3. how often a given command pattern occurs     -> sizes a hook's trigger rate before
     you rewrite it

SCOPE LIMIT, STATE IT WHEN REPORTING: this reads THIS project's transcripts only.
"Zero calls here" does not mean unused elsewhere — account-level connectors are shared
with other projects and other clients of the same account. Never justify removing a
shared resource with a per-project zero alone.

CAUTION: do not grep raw transcript text for a name to prove usage. Every system prompt
lists every available skill and tool, so a substring search matches the catalogue, not the
call. This parses structured tool-use blocks instead.

Usage:
  python3 usage-evidence.py [--project DIR] [--pattern REGEX] [--since ISO8601]
"""
import argparse, collections, datetime, glob, json, os, re, sys


def transcript_dir(project):
    enc = re.sub(r"[/.]", "-", os.path.abspath(project))
    d = os.path.expanduser(f"~/.claude/projects/{enc}")
    return d if os.path.isdir(d) else None


def iter_tool_calls(files, since=None):
    """Yield (name, input_dict, timestamp) for every structured tool-use block."""
    for f in files:
        try:
            fh = open(f, encoding="utf-8", errors="ignore")
        except OSError:
            continue
        with fh:
            for line in fh:
                if '"name"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except (ValueError, TypeError):
                    continue
                ts = d.get("timestamp")
                if since and ts and ts < since:
                    continue
                content = (d.get("message") or {}).get("content")
                if not isinstance(content, list):
                    continue
                for blk in content:
                    if isinstance(blk, dict) and blk.get("type") == "tool_use" and blk.get("name"):
                        yield blk["name"], (blk.get("input") or {}), ts, f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=os.getcwd())
    ap.add_argument("--pattern", help="regex to count against Bash command text")
    ap.add_argument("--since", help="ISO8601; ignore entries before this")
    a = ap.parse_args()

    d = transcript_dir(a.project)
    if not d:
        sys.exit(f"no transcripts found for {a.project} — cannot produce usage evidence")
    files = sorted(glob.glob(f"{d}/*.jsonl") + glob.glob(f"{d}/*/*.jsonl")
                   + glob.glob(f"{d}/*/subagents/*.jsonl"))

    servers, tools = collections.Counter(), collections.Counter()
    per_session_tools = collections.Counter()
    bash_cmds, pattern_hits = [], 0
    rx = re.compile(a.pattern) if a.pattern else None

    for name, inp, ts, f in iter_tool_calls(files, a.since):
        per_session_tools[f] += 1
        if name.startswith("mcp__"):
            tools[name] += 1
            parts = name.split("__")
            servers[parts[1] if len(parts) > 1 else name] += 1
        elif name == "Bash":
            cmd = inp.get("command", "") or ""
            bash_cmds.append(cmd)
            if rx and rx.search(cmd):
                pattern_hits += 1

    sessions = len([f for f, n in per_session_tools.items() if n])
    print(f"transcripts: {len(files)} files, {sessions} with tool calls\n")

    print("=" * 62)
    print("MCP SERVERS INVOKED IN THIS PROJECT")
    print("=" * 62)
    if servers:
        for k, v in servers.most_common():
            print(f"  {v:>7}  {k}")
    else:
        print("  (none)")
    print("\n  Servers configured but absent from this list have ZERO calls HERE.")
    print("  That is necessary but not sufficient evidence for removal — see scope note.")

    print("\n" + "=" * 62)
    print("TOOL-CALL VOLUME  (turns per-call cost into per-session cost)")
    print("=" * 62)
    total = sum(per_session_tools.values())
    bash = len(bash_cmds)
    print(f"  total tool calls      {total:>7}")
    print(f"  Bash calls            {bash:>7}   ({bash/max(sessions,1):.0f} per session)")
    print(f"\n  A hook on Bash costing X ms therefore costs "
          f"{bash/max(sessions,1):.0f} * X ms per session.")
    print(f"  At 40ms that is {bash/max(sessions,1)*0.040:.1f}s/session — compare against startup.")

    if rx:
        print("\n" + "=" * 62)
        print(f"PATTERN  /{a.pattern}/  vs Bash command text")
        print("=" * 62)
        print(f"  matches {pattern_hits} of {bash} commands "
              f"({pattern_hits/max(sessions,1):.1f} per session)")
        print("  Use this to size a hook's real trigger rate before rewriting it,")
        print("  and to compare a loose matcher against a stricter one on the same corpus.")

    print("\n" + "=" * 62)
    print("TOP INDIVIDUAL MCP TOOLS")
    print("=" * 62)
    for k, v in tools.most_common(15):
        print(f"  {v:>7}  {k}")


if __name__ == "__main__":
    main()
