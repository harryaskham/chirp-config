# proc.sh — process helpers for the groove scripts (sourced by restart-groove.sh and watchdog.sh).

# safe_pgrep ARGS…: pgrep that cannot hang its caller. Exit 0 found (pids on stdout), 1 none, 2 unknown: pgrep did not
# finish in 10 s. A process stuck in the kernel blocks every read of its /proc/PID/cmdline (2026-10-21/22: kworkers
# stuck on the GPU's ttm), and a plain pgrep then hangs the watchdog forever. Act only on a definite 0 or 1.
safe_pgrep() {
  local out rc p
  out=$(mktemp)
  pgrep "$@" > "$out" 2>/dev/null &
  p=$!
  for _ in $(seq 1 40); do kill -0 "$p" 2>/dev/null || break; sleep 0.25; done
  if kill -0 "$p" 2>/dev/null; then rm -f "$out"; return 2; fi
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
