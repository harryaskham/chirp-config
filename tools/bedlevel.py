#!/usr/bin/env python3
"""bedlevel: how loud a song's noise bed sits under its music (Harry, 25 Oct: the S&M crowd bed was "overpowering ...
white noise dominating our sound"; measured 2-9 dB under the music, and above it in quiet passages).

  bedlevel.py [ID …] [--tracks crowd-l,crowd-r] [--body 15] [--win 10] [-j 3] [--json]   (default: the focus's climbs)

Renders the bed tracks solo and the song with them muted (the groove pin, 2 render threads), and compares their RMS
over the body (the first and last --body s left out: the applause edges) and in --win s windows. The S&M rule: the
bed sits at least 20 dB under the music over the body and never above -12 dB in any window; then refit the master.
The real audience sat ~40-50 dB under the music during songs (livestems' RoFormer crowd stem). Read-only.
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
BODY_MIN, WIN_MAX = -20.0, -12.0


def rms_db(x, a, b):
    seg = x[int(a * L.SR):int(b * L.SR)]
    return 10 * np.log10(np.mean(seg ** 2) + 1e-14) if len(seg) else -140.0


def levels(bed, music, body=15.0, win=10.0):
    """(body dB, median window dB, worst window dB) of the bed relative to the music (mono arrays)."""
    n = min(len(bed), len(music)) / L.SR
    a, e = body, max(body + win, n - body)
    rel = [rms_db(bed, t, t + win) - rms_db(music, t, t + win) for t in np.arange(a, e - win + 1e-9, win)]
    return rms_db(bed, a, e) - rms_db(music, a, e), (float(np.median(rel)) if rel else None), (float(np.max(rel)) if rel else None)


def verdict(body_db, worst_db):
    ok = body_db <= BODY_MIN and (worst_db is None or worst_db <= WIN_MAX)
    return "ok" if ok else "TOO LOUD"


def one(cid, tracks, body, win):
    song = os.path.join(ROOT, "songs", f"{cid}.yaml")
    if not os.path.exists(song):
        return cid, {"error": "no song"}
    with tempfile.TemporaryDirectory(dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None) as d:
        outs = {}
        for name, flag in (("bed", "--solo"), ("music", "--mute")):
            out = os.path.join(d, f"{name}.wav")
            args = [x for t in tracks for x in (flag, t)]
            r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song, *args, "-o", out],
                               capture_output=True, text=True, stdin=subprocess.DEVNULL, env={**os.environ, "RAYON_NUM_THREADS": "2"})
            if r.returncode:
                return cid, {"error": f"render failed: {r.stderr.strip()[-160:]}"}
            outs[name] = L.load(out).mean(1)
    b, m, w = levels(outs["bed"], outs["music"], body, win)
    return cid, {"body_db": round(b, 1), "median_db": None if m is None else round(m, 1),
                 "worst_db": None if w is None else round(w, 1), "verdict": verdict(b, w)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--tracks", default="crowd-l,crowd-r")
    ap.add_argument("--body", type=float, default=15.0)
    ap.add_argument("--win", type=float, default=10.0)
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    reg = json.load(open(os.path.join(ROOT, "climbs.json")))
    ids = a.ids or driftscan.focus_ids(reg)
    tracks = [t for t in a.tracks.split(",") if t]
    with ThreadPoolExecutor(max(1, a.j)) as ex:
        res = dict(ex.map(lambda c: one(c, tracks, a.body, a.win), ids))
    if a.json:
        print(json.dumps(res, indent=1))
        return
    for cid in ids:
        r = res[cid]
        if "error" in r:
            print(f"{cid:32s} {r['error']}")
            continue
        print(f"{cid:32s} bed {r['body_db']:+6.1f} dB under the music (median window {r['median_db']:+6.1f}, "
              f"worst {r['worst_db']:+6.1f})  {r['verdict']}")


if __name__ == "__main__":
    main()
