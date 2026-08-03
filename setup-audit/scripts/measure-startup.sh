#!/bin/bash
# Interleaved startup measurement with a config-independent control.
#
# WHY INTERLEAVED: absolute wall times are NOT comparable across batches. API and
# machine latency drift by seconds — a real audit saw the isolation floor itself move
# 2.04s -> 5.11s between two batches an hour apart, which made a naive before/after
# read as a 52% regression when the config had actually improved. The only meaningful
# number is (current - floor) measured in the SAME batch, alternating run by run.
#
# WHY BASH: zsh does not word-split unquoted variables, so a command built in a
# variable silently becomes one argv[0] and exits in ~19ms — producing a full table of
# plausible near-zero timings. Run with bash.
#
# OUTPUT: TSV of samples on stdout; the summary table on stderr. Redirecting stdout
# captures the samples and leaves the table on screen.
#
# CAVEAT ON THE FLOOR: --safe-mode still applies admin-managed policy settings. On a
# managed machine the floor contains config, so (current - floor) UNDERSTATES overhead.
#
# Usage:
#   bash measure-startup.sh [REPS] [MODEL]
#   bash measure-startup.sh 6 'opus[1m]'        # quote model: [1m] is a zsh glob
set -u

REPS="${1:-5}"
MODEL="${2:-}"
PROMPT='Reply with exactly: ok'

case "$REPS" in ''|*[!0-9]*) echo "REPS must be an integer, got '$REPS'" >&2; exit 2;; esac
[ "$REPS" -lt 1 ] && { echo "REPS must be >= 1" >&2; exit 2; }

command -v claude >/dev/null 2>&1 || {
  echo "FATAL: 'claude' not on PATH. Without this check the script would have timed" >&2
  echo "both arms at ~5ms and reported CONFIG OVERHEAD +0.00s — plausible and wrong." >&2
  exit 2; }

# bash 3.2 (stock macOS) aborts on an empty array under `set -u`; guard the expansion.
MODEL_ARG=()
[ -n "$MODEL" ] && MODEL_ARG=(--model "$MODEL")
margs() { printf '%s\n' ${MODEL_ARG[@]+"${MODEL_ARG[@]}"}; }

CLEAN=(env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT -u CLAUDE_CODE_CHILD_SESSION
       -u CLAUDE_CODE_SESSION_ID -u CLAUDE_PID -u CLAUDE_EFFORT)

# Validate the floor flag BEFORE measuring. A CLI without --safe-mode fast-fails on the
# unknown option (~100ms) while the current arm runs for real, so the reported overhead
# becomes ~the entire startup time — a phantom that survives every later re-measure.
FLOOR_FLAG="--safe-mode"
if ! claude --help 2>&1 | grep -q -- '--safe-mode'; then
  echo "NOTE: --safe-mode not supported by this CLI; falling back to a synthetic floor." >&2
  FLOOR_FLAG=""
fi

now() { python3 -c 'import time;print(time.time())'; }

run_one() {  # $1 = label; remaining args = extra flags
  local label="$1"; shift
  local t0 t1 rc
  t0=$(now)
  if [ -n "$*" ]; then
    "${CLEAN[@]}" claude $(margs) "$@" -p "$PROMPT" >/dev/null 2>&1; rc=$?
  else
    "${CLEAN[@]}" claude $(margs) -p "$PROMPT" >/dev/null 2>&1; rc=$?
  fi
  t1=$(now)
  # A non-zero exit is NOT a fast sample — it is a discarded run. Recording it as a
  # timing is how a broken measurement produces a confident number.
  if [ "$rc" -ne 0 ]; then
    printf '%s\tFAILED\trc=%s\n' "$label" "$rc"
  else
    printf '%s\t%s\n' "$label" "$(python3 -c "print(f'{$t1-$t0:.3f}')")"
  fi
}

FLOOR_ARGS=()
[ -n "$FLOOR_FLAG" ] && FLOOR_ARGS=("$FLOOR_FLAG")
[ -z "$FLOOR_FLAG" ] && FLOOR_ARGS=(--strict-mcp-config --mcp-config '{"mcpServers":{}}' --setting-sources '')

echo "# interleaved: current vs floor (${FLOOR_FLAG:-synthetic}), ${REPS} reps each" >&2
{
for ((i=1; i<=REPS; i++)); do
  # alternate the order each pair so warmup can't systematically favour one arm
  if [ $((i % 2)) -eq 1 ]; then
    run_one current
    run_one floor "${FLOOR_ARGS[@]}"
  else
    run_one floor "${FLOOR_ARGS[@]}"
    run_one current
  fi
done
} | tee /dev/stderr | REPS="$REPS" python3 -c '
import sys, os, statistics, collections
d = collections.defaultdict(list); failed = collections.Counter()
for line in sys.stdin:
    p = line.split()
    if len(p) >= 2 and p[1] == "FAILED": failed[p[0]] += 1; continue
    if len(p) == 2:
        try: d[p[0]].append(float(p[1]))
        except ValueError: pass
reps = int(os.environ.get("REPS", "0"))
out = ["", "config          n   median      min      max", "-"*46]
for k in ("current", "floor"):
    if k in d:
        v = d[k]
        out.append(f"{k:<12}{len(v):>4}{statistics.median(v):>9.2f}s{min(v):>8.2f}s{max(v):>8.2f}s")
bad = [f"{k}: {n} run(s) failed" for k, n in failed.items()]
short = [k for k in ("current","floor") if len(d.get(k, [])) < reps]
if bad or short:
    out += ["-"*46, "!! MEASUREMENT INCOMPLETE — do not report a delta:"]
    out += ["   " + b for b in bad]
    out += [f"   {k}: {len(d.get(k,[]))}/{reps} samples" for k in short]
elif "current" in d and "floor" in d:
    delta = statistics.median(d["current"]) - statistics.median(d["floor"])
    out += ["-"*46,
            f"CONFIG OVERHEAD  {delta:+.2f}s   <- the only cross-batch comparable number",
            "",
            "Report this delta, not raw wall time. If the floor moved a lot since the",
            "last batch, the environment changed and raw before/after is meaningless."]
print("\n".join(out), file=sys.stderr)
' >/dev/null
