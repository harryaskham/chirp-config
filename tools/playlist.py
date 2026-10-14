#!/usr/bin/env python3
"""Hill-climb playlist driver: plays every enabled climb in climbs.json on the live `groove`, each in its
current best version (see the registry's _protocol).

- A few seconds before each pass ends, it queues the next climb with `live replace --when loop`, reading the
  song file fresh, so a turn always starts with the newest committed best. After `passes` passes it moves on.
- When the playing climb's song file changes on disk (its owner committed a new best), it hot-swaps it at the
  next bar, but never in the last seconds of a pass, where the queued handover wins.
- Every file is checked with the groove's own binary (`chirp plan`) first. A climb that fails, for example
  because it needs a newer engine than the groove is pinned to, is skipped and logged.
- tools/playlist-solo (runtime, ignored) holding one climb id plays that climb exclusively.

Started by tools/restart-groove.sh playlist. Log: /tmp/chirp-playlist.log."""
import hashlib, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
C = os.environ.get("CHIRP_BIN", os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "chirp-groove"))
ID = os.environ.get("PLAYLIST_GROOVE", "groove")
LEAD = float(os.environ.get("PLAYLIST_LEAD_S", "8"))       # queue the handover this long before the pass ends
SWAP_GUARD = LEAD + 6                                        # no hot-swaps this close to the end


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def climbs():
    try:
        reg = json.load(open(os.path.join(ROOT, "climbs.json")))
    except (OSError, ValueError) as e:
        log("registry unreadable:", e)
        return []
    on = [c for c in reg.get("climbs", []) if c.get("enabled", True)]
    try:
        solo = open(os.path.join(HERE, "playlist-solo")).read().strip()
    except OSError:
        solo = ""
    if solo:
        on = [c for c in on if c["id"] == solo] or on
    return on


def path(c):
    return os.path.join(ROOT, c["song"])


def digest(c):
    try:
        return hashlib.sha1(open(path(c), "rb").read()).hexdigest()
    except OSError:
        return None


def playable(c):
    r = subprocess.run([C, "plan", "-f", path(c)], capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        log(f"skip {c['id']}: does not plan with the groove binary: {(r.stderr or r.stdout).strip()[-200:]}")
    return r.returncode == 0


def status():
    r = subprocess.run([C, "--json", "live", "status", "--id", ID], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)["data"]
    except (ValueError, KeyError, TypeError):
        return None


def replace(c, when):
    r = subprocess.run([C, "live", "replace", "--id", ID, "--when", when, path(c)], capture_output=True, text=True)
    ok = r.returncode == 0
    log(f"replace {c['id']} --when {when}: {'ok' if ok else (r.stderr or r.stdout).strip()[-200:]}")
    return ok


def label_of(c):
    return os.path.splitext(os.path.basename(c["song"]))[0]


def main():
    log(f"playlist driver up (binary {C}, groove {ID})")
    playing, play_hash, passes_left = None, None, 1
    queued, queued_gen = None, None
    last_loop = None
    while True:
        time.sleep(1)
        st = status()
        if not st:
            continue                                         # groove down: the watchdog restarts it
        cl = climbs()
        if not cl:
            continue
        if playing is None:                                  # adopt whatever is playing (restart-groove started it)
            playing = next((c for c in cl if label_of(c) == st.get("label")), cl[0])
            play_hash, passes_left, last_loop = digest(playing), playing.get("passes", 1), st["loop_index"]
            log(f"now playing {playing['id']} ({st.get('label')})")
        gen, pos, length, loop = st["generation"], st["position"], st["loop_seconds"], st["loop_index"]
        if queued is not None and gen != queued_gen and not st.get("pending"):
            playing, play_hash, passes_left, last_loop = queued, digest(queued), queued.get("passes", 1), loop
            log(f"now playing {playing['id']}")
            queued = None
            continue
        if loop != last_loop:                                # a pass of the same song completed
            passes_left -= 1
            last_loop = loop
        playing = next((c for c in cl if c["id"] == playing["id"]), playing)   # registry edits (passes, song path)
        remaining = length - pos
        if queued is None and remaining < LEAD and not st.get("pending"):
            if passes_left > 1 or len(cl) == 1:
                nxt = playing                                # stay; re-queue only if the file changed
                if digest(nxt) == play_hash:
                    continue
            else:
                i = next((k for k, c in enumerate(cl) if c["id"] == playing["id"]), -1)
                order = cl[i + 1:] + cl[:i + 1]
                nxt = next((c for c in order if playable(c)), None)
                if nxt is None:
                    continue
            if nxt is playing or nxt["id"] == playing["id"]:
                if not playable(nxt):
                    continue
            if replace(nxt, "loop"):
                queued, queued_gen = nxt, gen
        elif queued is None and remaining > SWAP_GUARD and not st.get("pending"):
            h = digest(playing)
            if h and h != play_hash:
                log(f"{playing['id']}: song file changed on disk")
                if playable(playing) and replace(playing, "bar"):
                    pass
                play_hash = h                                # a failing file is not retried until it changes again


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
