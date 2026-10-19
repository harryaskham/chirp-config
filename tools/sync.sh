#!/usr/bin/env bash
# sync.sh — keep the live groove on the latest shared config, evolver and chirp build.
#  1. fast-forward chirp-config (never stashes; bd-d30a90); restart the evolver (keeping the playing song) if
#     evolve.py/compose.py changed upstream
#  2. if tools origin/main has new chirp commits, rebuild in a detached worktree and restart the
#     groove on a fresh pinned copy (resuming the queued song)
#   CHIRP_REPO  tools checkout (default ~/tools)   CHIRP_MAIN  build worktree (default /tmp/lt/chirp-main)
set -u
here=$(cd "$(dirname "$0")" && pwd); cfg=$(dirname "$here")
repo=${CHIRP_REPO:-$HOME/tools}; main=${CHIRP_MAIN:-/tmp/lt/chirp-main}
pinned=${XDG_RUNTIME_DIR:-/tmp}/chirp-groove; log=${TMPDIR:-/tmp}/chirp-evolve.log
py=$(command -v python3)

before=$(git -C "$cfg" rev-parse HEAD)
# Fast-forward only, under climb.py's git lock: the tree is shared, so never stash or rebase another agent's
# uncommitted work (bd-d30a90); local commits are climb.py's to publish (`climb.py publish`).
flock "$cfg/.git/climb-git.lock" -c "git -C '$cfg' fetch -q origin main && git -C '$cfg' merge -q --ff-only origin/main" \
  || echo "sync: config not fast-forwarded (local commits to publish, or an edit in the way; nothing stashed)"
after=$(git -C "$cfg" rev-parse HEAD)
tools_changed=$(git -C "$cfg" diff --name-only "$before" "$after" -- tools/evolve.py tools/compose.py | wc -l)
[ "$before" != "$after" ] && echo "sync: config $before → $after ($(git -C "$cfg" log --oneline "$before..$after" | wc -l) commits)"

rebuilt=0
git -C "$repo" fetch -q origin
[ -d "$main" ] || git -C "$repo" worktree add -f --detach "$main" origin/main >/dev/null 2>&1
cur=$(git -C "$main" rev-parse HEAD); head=$(git -C "$repo" rev-parse origin/main)
# Rebuild only for engine/library changes (not docs).
src_changes=$(git -C "$repo" log --format=%H "$cur..$head" -- cli/chirp/crates cli/chirp/Cargo.toml cli/chirp/Cargo.lock 2>/dev/null)
if [ "$cur" != "$head" ] && [ -n "$src_changes" ] || [ ! -x "$main/cli/chirp/target/release/chirp" ]; then
  git -C "$main" checkout -q --detach "$head"
  echo "sync: building chirp $(git -C "$main" log --oneline -1 | cut -c1-80)"
  if (cd "$main/cli/chirp" && nix develop -c cargo build --release -p chirp-cli >/tmp/chirp-sync-build.log 2>&1); then rebuilt=1; else echo "sync: build failed (see /tmp/chirp-sync-build.log)"; fi
else
  git -C "$main" checkout -q --detach "$head" 2>/dev/null
fi

new="$main/cli/chirp/target/release/chirp"
if [ "$rebuilt" = 1 ] && ! cmp -s "$new" "$pinned"; then
  nxt=$("$py" -c "import json;print(json.load(open('$here/state.json')).get('next') or 'form-1')" 2>/dev/null || echo form-1)
  # Restart at a pass boundary (≤ 2.5 s left in the playing chapter) so it lands where the music changes.
  for _ in $(seq 1 240); do
    left=$("$pinned" --json live status --id groove 2>/dev/null | "$py" -c "import json,sys; d=json.load(sys.stdin)['data']; print(d['loop_seconds'] - d['position'])" 2>/dev/null || echo 0)
    "$py" -c "import sys; sys.exit(0 if float('$left') <= 2.5 else 1)" && break
    sleep 0.5
  done
  nxt=$("$py" -c "import json;print(json.load(open('$here/state.json')).get('next') or 'form-1')" 2>/dev/null || echo form-1)
  echo "sync: restarting groove on the new build at a pass boundary (resuming @$nxt)"
  song=$(cat "$here/groove-song" 2>/dev/null || echo live-suite)  # what the groove should play (runtime state)
  if [ "$song" = live-suite ]; then CHIRP_SRC="$new" bash "$here/restart-groove.sh" live-suite "@$nxt"
  else CHIRP_SRC="$new" bash "$here/restart-groove.sh" "$song"; fi
elif [ "$tools_changed" -gt 0 ]; then
  echo "sync: evolver/composer changed upstream — restarting the evolver (keeping the playing song)"
  pgrep -f "^[^ ]*python3 $here/evolve.py" | xargs -r kill; sleep 0.5
  CHIRP_BIN="$pinned" EVOLVE_RESUME=keep setsid nohup "$py" "$here/evolve.py" >> "$log" 2>&1 < /dev/null &
fi
echo "sync: config $(git -C "$cfg" log --oneline -1 | cut -c1-60) · chirp $(git -C "$main" log --oneline -1 | cut -c1-60)"
