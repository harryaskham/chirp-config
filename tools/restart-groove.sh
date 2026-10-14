#!/usr/bin/env bash
# restart-groove.sh SONG [ARRANGEMENT] — restart the live `groove` on a pinned copy of the current
# chirp binary (so rebuilds don't change the engine under it) and resume the evolver.
#   CHIRP_SRC  binary to pin (default: $CHIRP_BIN or `command -v chirp`)
#   CHIRP_OUT  output device (default: music)
set -u
# One restart at a time (sync.sh and watchdog.sh can both trigger one): wait up to 60 s for the lock.
exec 9>"${TMPDIR:-/tmp}/chirp-restart.lock"
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
# Stop with the new binary first (the pinned copy may be missing or older); any build speaks the socket protocol.
"$src" stop groove >/dev/null 2>&1 || { [ -x "$C" ] && "$C" stop groove >/dev/null 2>&1; }
for _ in 1 2 3 4 5 6 7 8 9 10; do "$src" live list 2>/dev/null | grep -q '^groove ' || break; sleep 0.5; done
cp -f "$src" "$C"
sleep 0.3
setsid nohup "$C" --loop --id groove -o "${CHIRP_OUT:-music}" -s "${1:-live-suite}" > "${TMPDIR:-/tmp}/chirp-groove.log" 2>&1 < /dev/null &
sleep 1.2
if [ -n "${2:-}" ]; then "$C" live set --id groove --when bar --xfade 150ms "tracks.arrangement.score=$2" | tail -1; fi
CHIRP_BIN=$C EVOLVE_RESUME=1 setsid nohup python3 "$here/evolve.py" >> "$log" 2>&1 < /dev/null &
sleep 0.5
"$C" live list
pgrep -f "^[^ ]*python3 $here/evolve.py" >/dev/null && echo "evolver running (log: $log)"
