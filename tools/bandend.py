#!/usr/bin/env python3
"""bandend: where does our band stop, against where the record's band stops? (chirper-one's S&M finding 2: compare
the tab's end with the stems' band end. Where the live band plays on (Wherever I May Roam, Sad but True: +21 s) a held
root chord restruck each bar won +0.3..+0.5; where it stops early (Hero of the Day, Fuel, Master of Puppets, Of Wolf
and Man, Human) muting the band by a lane plus crowd-applause plus a refit won +0.6..+1.4.)

  bandend.py [ID …] [--mute TRACKS] [--floor 40] [-j 3] [--json]      (default: the focus's climbs)

Ours: the song rendered with its crowd tracks muted (any track named crowd/applause/audience, plus --mute).
Record: the htdemucs_6s stems except vocals (crowd cheering lands
there) summed. Each band end is the last 0.25 s frame within --floor dB of the signal's loud level (95th percentile).
Reports both ends and the difference; |difference| >= 3 s is flagged (PLAYS ON: the record's band continues after ours;
STOPS EARLY: ours continues after the record's). Read-only.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import driftscan  # noqa: E402  (focus_ids)
import likeness as L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAND_STEMS = ("drums", "bass", "guitar", "piano", "other")
HOP = 0.25


def band_end(x, floor=40.0):
    """The end (s) of the last frame within FLOOR dB of the loud level (mono X at L.SR), or None if silent."""
    h = int(HOP * L.SR)
    n = len(x) // h
    if n == 0:
        return None
    lev = 10 * np.log10((x[:n * h].reshape(n, h) ** 2).mean(1) + 1e-14)
    loud = np.percentile(lev, 95)
    on = np.nonzero(lev >= loud - floor)[0]
    return float((on[-1] + 1) * HOP) if len(on) else None


def record_band(cid):
    d = os.path.join(ROOT, "ref", "stems", "htdemucs_6s", cid)
    xs = [L.load(os.path.join(d, f"{s}.wav")).mean(1) for s in BAND_STEMS if os.path.exists(os.path.join(d, f"{s}.wav"))]
    if not xs:
        return None
    n = min(len(x) for x in xs)
    return sum(x[:n] for x in xs)


def one(cid, mute, floor):
    song = os.path.join(ROOT, "songs", f"{cid}.yaml")
    rec = record_band(cid)
    if not os.path.exists(song) or rec is None:
        return cid, {"error": "no song or no stems"}
    names = driftscan.track_names(song)                  # mute only tracks the song has (chirp refuses unknown names)
    crowd = [n for n in names if n in mute or any(k in n.lower() for k in ("crowd", "applause", "audience"))]
    with tempfile.TemporaryDirectory(dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None) as d:
        out = os.path.join(d, "band.wav")
        args = [x for t in crowd for x in ("--mute", t)]
        r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song, *args, "-o", out],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL, env={**os.environ, "RAYON_NUM_THREADS": "2"})
        if r.returncode:
            return cid, {"error": f"render failed: {r.stderr.strip()[-160:]}"}
        ours = band_end(L.load(out).mean(1), floor)
    theirs = band_end(rec, floor)
    if ours is None or theirs is None:
        return cid, {"error": "silent"}
    return cid, {"ours": ours, "record": theirs, "diff": round(theirs - ours, 2)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--mute", default="", help="more tracks to mute (crowd/applause/audience ones always are)")
    ap.add_argument("--floor", type=float, default=40.0)
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    reg = json.load(open(os.path.join(ROOT, "climbs.json")))
    ids = a.ids or driftscan.focus_ids(reg)
    mute = [t for t in a.mute.split(",") if t]
    with ThreadPoolExecutor(max(1, a.j)) as ex:
        res = dict(ex.map(lambda c: one(c, mute, a.floor), ids))
    if a.json:
        print(json.dumps(res, indent=1))
        return
    for cid in ids:
        r = res[cid]
        if "error" in r:
            print(f"{cid:30s} {r['error']}")
            continue
        flag = "  PLAYS ON" if r["diff"] >= 3 else ("  STOPS EARLY" if r["diff"] <= -3 else "")
        print(f"{cid:30s} our band ends {r['ours']:7.1f} s, the record's {r['record']:7.1f} s ({r['diff']:+6.1f}){flag}")


if __name__ == "__main__":
    main()
