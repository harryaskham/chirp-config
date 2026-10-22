#!/usr/bin/env bash
# watchdog.sh — keep the groove alive: every 15 s, if the `groove` session is missing OR frozen
# (its position has not moved since the last check — e.g. its audio output stalled when the Pulse
# server went away) and the Pulse server for the music profile answers, restart it on the latest
# build (resuming the queued song).
#   CHIRP_MAIN (default /tmp/lt/chirp-main), PULSE (default tcp:sgu24:4713)
here=$(cd "$(dirname "$0")" && pwd)
. "$here/proc.sh"   # safe_pgrep: a definite answer or "unknown" (exit 2), never a hang; launch: its own systemd unit
main=${CHIRP_MAIN:-/tmp/lt/chirp-main}; pulse=${PULSE:-tcp:sgu24:4713}
last=""
while true; do
  bin="$main/cli/chirp/target/release/chirp"
  reason=""
  if [ -x "$bin" ] && flock -n "${TMPDIR:-/tmp}/chirp-restart-v2.lock" true; then
    if ! "$bin" live list 2>/dev/null | grep -q '^groove '; then
      reason="missing"; last=""
    else
      pos=$("$bin" --json live status --id groove 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(d.get('generation'), d.get('loop_index'), round(d.get('position', 0), 2))" 2>/dev/null)
      if [ -n "$pos" ] && [ "$pos" = "$last" ]; then reason="frozen at $pos"; fi
      last="$pos"
    fi
    out=$(cat "$here/groove-out" 2>/dev/null || echo music)
    if [ "$out" = chirp ]; then pulse="unix:/run/user/$(id -u)/pulse/native"; else pulse=${PULSE:-tcp:sgu24:4713}; fi
    # playlist mode: the groove alone keeps looping its current song, so a dead driver silently stops the rotation
    if [ -z "$reason" ] && [ "$(cat "$here/groove-song" 2>/dev/null)" = playlist ]; then
      if unit_active 'chirp-playlist-*'; then rc=0; else safe_pgrep -f "^[^ ]*python3 $here/playlist.py" >/dev/null; rc=$?; fi
      if [ "$rc" = 1 ]; then   # definitely none (2 = the process table did not answer: do nothing this round)
        echo "$(date +%T) watchdog: playlist driver missing — restarting it"
        launch chirp-playlist "CHIRP_BIN=$(printf '%q' "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/chirp-groove") XDG_RUNTIME_DIR=$(printf '%q' "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}") exec python3 $(printf '%q' "$here/playlist.py") >> $(printf '%q' "${TMPDIR:-/tmp}/chirp-playlist.log") 2>&1 < /dev/null"
      fi
    fi
    # the temp audio janitor (agents' renders fill the disk otherwise): one detached loop, every 10 min
    if unit_active 'chirp-tmpclean-*'; then rc=0; else safe_pgrep -f "tmpclean.py --loop" >/dev/null; rc=$?; fi
    if [ "$rc" = 1 ]; then
      launch chirp-tmpclean "exec python3 $(printf '%q' "$here/tmpclean.py") --loop 600 --quiet > /dev/null 2>&1 < /dev/null"
    fi
    if [ -n "$reason" ] && env -u PULSE_SERVER pactl -s "$pulse" info >/dev/null 2>&1; then
      nxt=$(python3 -c "import json;print(json.load(open('$here/state.json')).get('next') or 'form-1')" 2>/dev/null || echo form-1)
      echo "$(date +%T) watchdog: groove $reason — restarting (@$nxt)"
      song=$(cat "$here/groove-song" 2>/dev/null || echo live-suite)  # what the groove should play (runtime state)
      if [ "$song" = live-suite ]; then CHIRP_SRC="$bin" bash "$here/restart-groove.sh" live-suite "@$nxt" 2>&1 | tail -2
      else CHIRP_SRC="$bin" bash "$here/restart-groove.sh" "$song" 2>&1 | tail -2; fi
      last=""
      sleep 30
    fi
  fi
  sleep 15
done
