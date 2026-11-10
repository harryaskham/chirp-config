#!/usr/bin/env python3
"""visdrift: has a song moved under its picture? (chirp-eco, 10 Nov)

A directed programme (vis/<id>.yaml) cuts its scenes at absolute seconds chosen against the song as it was ("act II at
2:05: the jet"). When the song's structure changes later - bars added or removed, a tempo change, a landmark moved - the
cuts keep their seconds and the picture is out of step, silently; the album film is rendered once from these files.

  visdrift.py [ALBUM_ID] [--json] [--ids 4,8]        (default: the focus album)

Per track, the song as it was when the programme was last committed (git) against the song as committed now:
  * length, bar count and where each scene cut's BAR now falls in time (the engine's own beat clock, `chirp plan`):
    DRIFT when the length moved 1 s or more, the bar count changed, or a cut's bar moved 0.5 s or more;
  * for landmarks that move inside an unchanged grid, the CONTRAST at each cut (flatness.py's distance between the 8 s
    before and after it) in the review-app snapshot nearest the programme's date against the latest snapshot: CHECK
    when a cut that sat on a clear change (1.0 or more) now sits on less than 60% of it.
A report for the picture's author, not a verdict: a cut placed on purpose mid-phrase reads low both times, and bars
inserted before a cut need re-timing by ear. Read-only; exits 1 when any track drifts or wants a check.
"""
import argparse
import calendar
import json
import os
import re
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)

LENGTH_S, CUT_S = 1.0, 0.5            # drift thresholds: seconds of length, seconds a cut's bar moved
CLEAR, FADED = 1.0, 0.6               # a clear change at a cut then; the share of it that must remain now
WIN = 8                               # seconds each side of a cut for the contrast


def git(*args):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def programme(cid):
    for ext in (".yaml", ".yml", ".json"):
        p = os.path.join(ROOT, "vis", cid + ext)
        if os.path.exists(p):
            return p
    return None


def cuts(text):
    """Scene cut times (seconds, after 0) of a programme: its top-level scene items' `at:`."""
    out = []
    for m in re.finditer(r"^  - at:\s*([0-9]+(?:\.[0-9]+)?)\s*(?:#.*)?$", text, re.M):
        t = float(m.group(1))
        if t > 0:
            out.append(t)
    return sorted(set(out))


def clock(pin, text, tag):
    """{secs, times (seconds of each whole beat), per (beats a bar), bars} of a song text, or None when it doesn't plan."""
    import chirpers as CH
    import sectionmap as SM
    tmp = os.path.join(ROOT, "songs", f".visdrift-{os.getpid()}-{tag}.yaml")      # beside its includes
    try:
        with open(tmp, "w") as f:
            f.write(text)
        tl = CH.song_timeline(pin, tmp)
        per = SM.meter_beats(tmp)
    finally:
        os.path.exists(tmp) and os.unlink(tmp)
    if not tl:
        return None
    times = np.asarray(tl["times"], float)
    end = float(np.interp(tl["secs"], times, np.arange(len(times))))
    return {"secs": float(tl["secs"]), "times": times, "per": per, "bars": end / per}


def compare(then, now, cut_times):
    """{length, bars, cuts: [{at, bar, now, shift}], drift} for two clocks."""
    out = {"length": [round(then["secs"], 1), round(now["secs"], 1)], "bars": [round(then["bars"], 1), round(now["bars"], 1)],
           "cuts": []}
    for t in cut_times:
        beat = float(np.interp(t, then["times"], np.arange(len(then["times"]))))
        bar = 1 + beat / then["per"]
        now_beat = (bar - 1) * now["per"]
        t_now = float(np.interp(now_beat, np.arange(len(now["times"])), now["times"]))
        out["cuts"].append({"at": t, "bar": round(bar, 1), "now": round(t_now, 1), "shift": round(t_now - t, 1)})
    out["drift"] = (abs(now["secs"] - then["secs"]) >= LENGTH_S or abs(now["bars"] - then["bars"]) >= 0.5
                    or any(abs(c["shift"]) >= CUT_S for c in out["cuts"]))
    return out


def contrast(mp3, t, win=WIN):
    """flatness.py's distance between the WIN seconds before and after T in an audio file; None near the ends."""
    import flatness as FL
    if t < win or not os.path.exists(mp3):
        return None
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t - win), "-t", str(2 * win), "-i", mp3, "-ac", "1", "-ar",
                        str(FL.SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(b, dtype=np.float32)
    if len(x) < int(FL.SR * (2 * win - 0.5)):
        return None
    F = FL.features(x)
    if len(F) < 2 * win - 1:
        return None
    return float(np.linalg.norm(F[:win].mean(0) - F[win:2 * win].mean(0)))


def snapshot_pair(album_id, when):
    """(the latest snapshot cut at or before WHEN (epoch), else the earliest; the latest snapshot) as directories."""
    import listen as L
    snaps = L.snapshots(album_id)
    if not snaps:
        return None, None
    d = os.path.join(L.album_dir(album_id), "snapshots")

    def at(s):
        try:
            return float(calendar.timegm(time.strptime(s.get("at", ""), "%Y-%m-%dT%H:%M:%SZ")))
        except ValueError:
            return 0.0
    before = [s for s in snaps if at(s) <= when]
    return os.path.join(d, (before[-1] if before else snaps[0])["id"]), os.path.join(d, snaps[-1]["id"])


def track(cid, n, song, album_id, pin):
    """One track's report, or None when it has no programme."""
    prog = programme(cid)
    if not prog:
        return None
    relp = os.path.relpath(prog, ROOT)
    dirty = bool((git("status", "--porcelain", "--", relp) or "").strip())
    ct = git("log", "-1", "--format=%ct", "--", relp)
    when = os.path.getmtime(prog) if dirty or not (ct or "").strip() else float(ct.strip())
    rev = (git("rev-list", "-1", f"--before=@{int(when)}", "HEAD", "--", song) or "").strip() \
        or (git("rev-list", "--reverse", "HEAD", "--", song) or "").split("\n")[0].strip()
    then_text, now_text = git("show", f"{rev}:{song}") if rev else None, git("show", f"HEAD:{song}")
    res = {"id": cid, "n": n, "programme": time.strftime("%d %b %H:%M", time.gmtime(when)), "song_then": rev[:8]}
    if not then_text or not now_text:
        return {**res, "state": "unknown", "why": "the song is not in git at one of the two dates"}
    with open(prog) as f:
        cut_times = cuts(f.read())
    if then_text == now_text:
        return {**res, "state": "in step", "cuts": [{"at": t} for t in cut_times], "same_text": True}
    then, now = clock(pin, then_text, f"{cid}-then"), clock(pin, now_text, f"{cid}-now")
    if not then or not now:
        return {**res, "state": "unknown", "why": "the song does not plan on this pin at one of the two dates"}
    res.update(compare(then, now, cut_times))
    a, b = snapshot_pair(album_id, when)
    checks = []
    if a and b and a != b:
        for c in res["cuts"]:
            ca, cb = contrast(os.path.join(a, f"t{n:02d}.mp3"), c["at"]), contrast(os.path.join(b, f"t{n:02d}.mp3"), c["now"])
            if ca is not None and cb is not None:
                c["contrast"] = [round(ca, 2), round(cb, 2)]
                if ca >= CLEAR and cb < FADED * ca:
                    checks.append(c["at"])
        res["snapshots"] = [os.path.basename(a), os.path.basename(b)]
    res["check"] = checks
    res["state"] = "DRIFT" if res.pop("drift") else ("CHECK" if checks else "in step")
    return res


def mmss(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def lines(r):
    head = f"  t{r['n']} programme {r['programme']} (song then {r.get('song_then') or '?'}): "
    if r["state"] == "unknown":
        return [head + f"unknown - {r['why']}"]
    if r.get("same_text"):
        return [head + "in step (the song has not changed since)"]
    le, ba = r["length"], r["bars"]
    out = [head + (f"{r['state']} length {mmss(le[0])} -> {mmss(le[1])} ({le[1] - le[0]:+.1f} s), bars {ba[0]:g} -> {ba[1]:g}"
                   if r["state"] == "DRIFT" else f"{r['state']} ({mmss(le[1])}, {ba[1]:g} bars)")]
    for c in r["cuts"]:
        moved = abs(c["shift"]) >= CUT_S
        faded = c["at"] in r.get("check", [])
        if not (moved or faded):
            continue
        s = f"      cut {mmss(c['at'])} (bar {c['bar']:g} then)"
        if moved:
            s += f": that bar is now at {mmss(c['now'])} ({c['shift']:+.1f} s)"
        if faded:
            s += f"; the change it sat on is weaker ({c['contrast'][0]} -> {c['contrast'][1]}): has the landmark moved?"
        out.append(s)
    if r["state"] == "DRIFT" and abs(ba[1] - ba[0]) >= 0.5:
        out.append("      bars were added or removed: cuts after that point need re-timing by ear")
    return out


def main(argv=None):
    import chirpbin
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("album", nargs="?")
    ap.add_argument("--ids", help="track numbers, e.g. 4,8")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(os.path.join(ROOT, "climbs.json")) as f:
        reg = json.load(f)
    album_id = a.album
    rows = []
    for c in reg.get("climbs", []):
        meta = c.get("meta") or {}
        if album_id:
            if not c["id"].startswith(album_id + "-"):
                continue
        elif str(meta.get("album", "")).casefold() != str(reg.get("focus", "")).casefold():
            continue
        m = re.search(r"-t(\d+)$", c["id"])
        if m:
            rows.append((int(m.group(1)), c["id"], c.get("song") or f"songs/{c['id']}.yaml"))
    if not rows:
        ap.error("no tracks (give an ALBUM_ID such as chirpers9)")
    album_id = album_id or rows[0][1].rsplit("-", 1)[0]
    want = {int(x) for x in a.ids.split(",")} if a.ids else None
    pin = chirpbin.resolve("chirp")
    res = [r for n, cid, song in sorted(rows) if not want or n in want
           for r in [track(cid, n, song, album_id, pin)] if r]
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        print(f"visdrift: {album_id} - each programme against its song as committed now")
        for r in res:
            print("\n".join(lines(r)))
        bad = [f"t{r['n']}" for r in res if r["state"] in ("DRIFT", "CHECK")]
        print(f"visdrift: {len(res)} programmes, " + (f"look at {', '.join(bad)}" if bad else "all in step"))
    return 1 if any(r["state"] in ("DRIFT", "CHECK") for r in res) else 0


if __name__ == "__main__":
    sys.exit(main())
