#!/usr/bin/env bash
# watchdog.sh — keep the groove alive: every 15 s, if no `groove` session exists and the Pulse
# server for the music profile answers, restart it on the latest build (resuming the queued song).
#   CHIRP_MAIN (default /tmp/lt/chirp-main), PULSE (default tcp:sgu24:4713)
here=$(cd "$(dirname "$0")" && pwd)
main=${CHIRP_MAIN:-/tmp/lt/chirp-main}; pulse=${PULSE:-tcp:sgu24:4713}
while true; do
  bin="$main/cli/chirp/target/release/chirp"
  # Skip while another restart (sync.sh) holds the lock; re-check after it finishes.
  if [ -x "$bin" ] && flock -n "${TMPDIR:-/tmp}/chirp-restart.lock" true && ! "$bin" live list 2>/dev/null | grep -q '^groove '; then
    if pactl -s "$pulse" info >/dev/null 2>&1; then
      nxt=$(python3 -c "import json;print(json.load(open('$here/state.json')).get('next') or 'form-1')" 2>/dev/null || echo form-1)
      echo "$(date +%T) watchdog: groove missing — restarting (@$nxt)"
      CHIRP_SRC="$bin" bash "$here/restart-groove.sh" live-suite "@$nxt" 2>&1 | tail -2
      sleep 30
    fi
  fi
  sleep 15
done
