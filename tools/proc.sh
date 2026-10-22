# proc.sh — process helpers for the groove scripts (sourced by restart-groove.sh and watchdog.sh).

# safe_pgrep ARGS…: pgrep that cannot hang its caller. Exit 0 found (pids on stdout), 1 none, 2 unknown: pgrep did not
# finish in 10 s. A process stuck in the kernel blocks every read of its /proc/PID/cmdline (2026-10-21/22: kworkers
# stuck on the GPU's ttm), and a plain pgrep then hangs the watchdog forever. Act only on a definite 0 or 1.
# A pgrep that does not finish stays stuck in the kernel (unkillable) until the stuck process wakes: after one hangs,
# answer "unknown" without spawning another for 30 min (the first watchdog with this helper leaked one every ~15 s:
# 142 stuck pgreps inflated the load average to ~170 and stalled the climbers' load-gated renders).
PGREP_HUNG=${TMPDIR:-/tmp}/chirp-pgrep-hung
safe_pgrep() {
  local out rc p
  if [ -e "$PGREP_HUNG" ] && [ $(( $(date +%s) - $(stat -c %Y "$PGREP_HUNG" 2>/dev/null || echo 0) )) -lt 1800 ]; then
    return 2
  fi
  out=$(mktemp)
  # 9>&-: never hand the caller's lock fd (restart-groove.sh holds its flock on fd 9) to a pgrep that may hang:
  # a stuck pgrep from a restart held chirp-restart-v2.lock for two hours, refusing every later restart
  pgrep "$@" > "$out" 2>/dev/null 9>&- &
  p=$!
  for _ in $(seq 1 40); do kill -0 "$p" 2>/dev/null || break; sleep 0.25; done
  if kill -0 "$p" 2>/dev/null; then rm -f "$out"; touch "$PGREP_HUNG"; return 2; fi
  wait "$p"; rc=$?
  cat "$out"; rm -f "$out"
  return "$rc"
}

# launch NAME COMMAND: run the shell COMMAND detached, as its own transient systemd user unit (NAME-<ns>.service) when a
# user manager is available, else with setsid nohup. A unit outlives its caller's service: an agent's shell runs inside
# pi-daemon.service, and a system switch restarting that service killed a groove started from it (01:45 and 04:10 on
# 2026-10-22). A unit does not inherit the caller's environment: put what COMMAND needs inside it (VAR=… exec …).
launch() {
  local name=$1; shift
  if command -v systemd-run >/dev/null 2>&1 && systemctl --user show-environment >/dev/null 2>&1; then
    systemd-run --user --collect --quiet --unit="$name-$(date +%s%N)" -- /bin/sh -c "$*" && return 0
  fi
  setsid nohup /bin/sh -c "$*" > /dev/null 2>&1 < /dev/null &
}

# unit_active PATTERN: a running transient unit (e.g. 'chirp-playlist-*') — checks systemd, never /proc command lines.
unit_active() {
  systemctl --user list-units "$1" --state=active --no-legend 2>/dev/null | grep -q .
}
