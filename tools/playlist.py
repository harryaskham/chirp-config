#!/usr/bin/env python3
"""Hill-climb playlist driver: plays every enabled climb in climbs.json on the live `groove`, each in its
current best version (see the registry's _protocol), using chirp's shared queue (`chirp live queue`).

- The groove always has exactly one climb waiting: whenever its queue is empty (the waiting climb has just
  started playing), the next climb in rotation is queued from its song file. So each turn plays the version
  committed up to about one pass before it, and the session never falls back to its start-up song.
- A climb with `passes: N` is queued N times in a row; `enabled: false` leaves the rotation.
- Every file is validated by the groove (and checked with its binary's `plan` first). A climb that fails,
  for example because it needs a newer engine than the groove runs, is skipped and logged.
- tools/playlist-solo (runtime, ignored) holding one climb id plays that climb exclusively.
- To show Harry something, take over for one pass: `chirp live queue FILE --id groove --now --label NAME`.
  The rotation carries on afterwards.
- Underrun increases are logged with the host load (they track CPU storms on the host).

Started by tools/restart-groove.sh playlist. Log: /tmp/chirp-playlist.log."""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
C = os.environ.get("CHIRP_BIN", os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "chirp-groove"))
ID = os.environ.get("PLAYLIST_GROOVE", "groove")


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


def enqueue(c):
    r = subprocess.run([C, "live", "queue", "--id", ID, "--label", c["id"], path(c)], capture_output=True, text=True, cwd=ROOT)
    ok = r.returncode == 0
    log(f"queued {c['id']}: {'ok' if ok else (r.stderr or r.stdout).strip()[-200:]}")
    return ok


def label_of(c):
    return os.path.splitext(os.path.basename(c["song"]))[0]


def main():
    log(f"playlist driver up (binary {C}, groove {ID}; chirp live queue)")
    last, run = None, 0          # last queued climb id and how many times in a row
    last_under = None
    while True:
        time.sleep(2)
        st = status()
        if not st:
            continue                                         # groove down: the watchdog restarts it
        u = st.get("underruns", 0)
        if last_under is not None and u > last_under:
            log(f"underruns +{u - last_under} (total {u}); host load {open('/proc/loadavg').read().split()[:3]}, groove load {st.get('load') or 0:.2f}")
        last_under = u
        if st.get("queue"):
            continue                                         # a climb is already waiting
        cl = climbs()
        if not cl:
            continue
        if last is None:                                     # adopt the start-up song (restart-groove plays the first climb)
            cur = next((c for c in cl if label_of(c) == st.get("label", "").lstrip("▶ ")), cl[0])
            last, run = cur["id"], 1
        cur = next((c for c in cl if c["id"] == last), None)
        if cur is not None and run < cur.get("passes", 1):
            order = [cur]
        else:
            i = next((k for k, c in enumerate(cl) if c["id"] == last), -1)
            order = cl[i + 1:] + cl[:i + 1]
        for c in order:
            if playable(c) and enqueue(c):
                run = run + 1 if c["id"] == last else 1
                last = c["id"]
                break
        else:
            time.sleep(30)                                   # nothing playable: retry later


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
