#!/usr/bin/env bash
# restart-groove.sh SONG [ARRANGEMENT] — restart the live `groove` on a pinned copy of the current
# chirp binary (so rebuilds don't change the engine under it) and resume the evolver.
#   CHIRP_SRC  binary to pin (default: $CHIRP_BIN or `command -v chirp`)
#   CHIRP_OUT  output profile (default: tools/groove-out, else music)
set -u
# One restart at a time (sync.sh and watchdog.sh can both trigger one): wait up to 60 s for the lock.
exec 9>"${TMPDIR:-/tmp}/chirp-restart-v2.lock"
flock -w 60 9 || { echo "restart-groove: another restart holds the lock"; exit 0; }
here=$(cd "$(dirname "$0")" && pwd)
# Never fall back to an installed (Nix) chirp: it can be far older than the library needs.
src=${CHIRP_SRC:-}
for c in "${CHIRP_MAIN:-/tmp/lt/chirp-main}/cli/chirp/target/release/chirp" "$HOME/.herdr/worktrees/tools/chirp/cli/chirp/target/release/chirp"; do
  [ -z "$src" ] && [ -x "$c" ] && src=$c
done
[ -n "$src" ] || { echo "restart-groove: set CHIRP_SRC to a chirp build from tools origin/main"; exit 1; }
C=${XDG_RUNTIME_DIR:-/tmp}/chirp-groove
log=${TMPDIR:-/tmp}/chirp-evolve.log
pgrep -f "^[^ ]*python3 $here/evolve.py" | xargs -r kill
pgrep -f "^[^ ]*python3 $here/playlist.py" | xargs -r kill
# Stop with the new binary first (the pinned copy may be missing or older); any build speaks the socket protocol.
# Musical stop (fade out on a bar line) where the build supports it; otherwise a plain stop.
"$src" stop groove --at bar --fade 800ms >/dev/null 2>&1 || "$src" stop groove >/dev/null 2>&1 || { [ -x "$C" ] && "$C" stop groove >/dev/null 2>&1; }
for _ in 1 2 3 4 5 6 7 8 9 10; do "$src" live list 2>/dev/null | grep -q '^groove ' || break; sleep 0.5; done
cp -f "$src" "$C"
sleep 0.3
# A generous output buffer: the music sink is a phone over Wi-Fi, and network jitter otherwise
# starves the stream (underruns) even when rendering is far ahead of real time.
# output profile: CHIRP_OUT, else tools/groove-out (runtime state), else music. The environment's PULSE_SERVER may
# point at a remote box, so it is unset: every profile names its own server. `chirp` is a pocket4-local null sink,
# (re)created here if missing so the groove never depends on the network during benchmark runs.
out=${CHIRP_OUT:-$(cat "$here/groove-out" 2>/dev/null || echo music)}
if [ "$out" = chirp ]; then
  local_pulse="unix:/run/user/$(id -u)/pulse/native"
  env -u PULSE_SERVER pactl -s "$local_pulse" list short sinks 2>/dev/null | grep -qw chirp \
    || env -u PULSE_SERVER pactl -s "$local_pulse" load-module module-null-sink sink_name=chirp rate=48000 channels=2 sink_properties=device.description=chirp >/dev/null
fi
# `playlist`: the hill-climb playlist (climbs.json) — start its first enabled climb from its file, then hand the
# groove to tools/playlist.py, which rotates the climbs and hot-swaps each owner's new best versions.
if [ "${1:-}" = playlist ]; then
  first=$(cd "$here/.." && python3 -c 'import json; c=[x for x in json.load(open("climbs.json"))["climbs"] if x.get("enabled", True)]; print(c[0]["song"])')
  src_args=(-f "$here/../$first")
else
  src_args=(-s "${1:-live-suite}")
fi
# Claim the sink: any other chirp stream on it refuses (naming the groove) unless --takeover, so stray playback
# can't double Harry's audio. Guarded: older binaries reject the flag.
excl=(); "$C" --help 2>/dev/null | grep -q -- --exclusive && excl=(--exclusive)
PULSE_LATENCY_MSEC=${CHIRP_PULSE_LATENCY_MSEC:-2000} setsid nohup env -u PULSE_SERVER "$C" --loop "${excl[@]}" --id groove -o "$out" "${src_args[@]}" > "${TMPDIR:-/tmp}/chirp-groove.log" 2>&1 < /dev/null 9>&- &
sleep 1.2
if [ -n "${2:-}" ]; then "$C" live set --id groove --when bar --xfade 150ms "tracks.arrangement.score=$2" | tail -1; fi
# the evolver only drives live-suite; any other song (a benchmark reproduction) plays as written
if [ "${1:-live-suite}" = live-suite ]; then CHIRP_BIN=$C EVOLVE_RESUME=1 setsid nohup python3 "$here/evolve.py" >> "$log" 2>&1 < /dev/null 9>&- & fi
if [ "${1:-}" = playlist ]; then CHIRP_BIN=$C setsid nohup python3 "$here/playlist.py" >> "${TMPDIR:-/tmp}/chirp-playlist.log" 2>&1 < /dev/null 9>&- & fi
sleep 0.5
"$C" live list
if pgrep -f "^[^ ]*python3 $here/playlist.py" >/dev/null; then echo "playlist driver running (log: ${TMPDIR:-/tmp}/chirp-playlist.log)"
else pgrep -f "^[^ ]*python3 $here/evolve.py" >/dev/null && echo "evolver running (log: $log)"; pgrep -f "^[^ ]*python3 $here/evolve.py" >/dev/null || echo "groove playing ${1:-live-suite} (no evolver)"; fi
