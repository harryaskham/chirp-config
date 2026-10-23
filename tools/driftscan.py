#!/usr/bin/env python3
"""driftscan: does a song drift against its record? The windowed onset lag (tools/onsetlag.py) fitted against time.

  driftscan.py [ID …] [--all] [-j 3] [--flag 60] [--win 4] [--step 8] [--max 250] [--keep DIR] [--json]
  driftscan.py --wav OURS.wav --ref REF.wav [--flag 60]                          # analysis only

Default IDs: the focus's climbs (climbs.json `focus`), else every enabled climb. Each song is rendered with the
adopted groove pin (nice 15) and compared with ref/ID.wav. Windows correlating above 0.1 give (time, lag) points;
their Theil-Sen slope (the median of pairwise slopes, robust to the +-half-beat aliases single windows show) times
the record's length is the drift. A tempo a fraction off shows as a steady slope: Pulk/Pull's tab said 97.000 BPM
against the record's 97.089, 0.17 s over the song, and fixing its tempo map was +11.4 on every seed (chirper-zero,
23 Oct). A constant offset shows as a median lag with no slope (onsetlag.py --shift, or the map's `offset`).
Flags |drift| >= --flag ms. Negative = ours early. Read-only: it never edits a song.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
import onsetlag  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def theil_sen(ts, ys):
    """Median of pairwise slopes (closed form; no least squares)."""
    s = [(ys[j] - ys[i]) / (ts[j] - ts[i]) for i in range(len(ts)) for j in range(i + 1, len(ts)) if ts[j] > ts[i]]
    return float(np.median(s)) if s else 0.0


def measure(ours, ref, win=4.0, step=8.0, mx=250):
    pts = [(t + win / 2, lag) for t, lag, corr in onsetlag.windowed_lags(ours, ref, win, step, mx) if corr > 0.1]
    if len(pts) < 4:
        return None
    ts = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    length = ts[-1] - ts[0]
    q = max(1, len(ys) // 4)
    slope = theil_sen(ts, ys)
    return {"windows": len(pts), "median_ms": float(np.median(ys)), "drift_ms": slope * length,
            "first_q_ms": float(np.median(ys[:q])), "last_q_ms": float(np.median(ys[-q:])),
            "span_s": length}


def focus_ids(reg):
    f = reg.get("focus")
    enabled = [c for c in reg["climbs"] if c.get("enabled") and c.get("song")]
    if isinstance(f, str) and f.startswith("climbs:"):
        want = [x.strip() for x in f.split(":", 1)[1].split(",")]
        return [c["id"] for c in enabled if c["id"] in want]
    if isinstance(f, str) and f:
        alb = [c for c in enabled if (c.get("meta") or {}).get("album", "").lower() == f.lower()]
        return [c["id"] for c in sorted(alb, key=lambda c: (c.get("meta") or {}).get("track") or 99)]
    return [c["id"] for c in enabled]


def scan(cid, work, a):
    song = os.path.join(ROOT, "songs", f"{cid}.yaml")
    ref = os.path.join(ROOT, "ref", f"{cid}.wav")
    if not (os.path.exists(song) and os.path.exists(ref)):
        return cid, {"error": "no song or reference"}
    out = os.path.join(work, f"{cid}.wav")
    r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song, "-o", out],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode:
        return cid, {"error": f"render failed: {r.stderr.strip()[-200:]}"}
    m = measure(out, ref, a.win, a.step, a.max)
    return cid, m or {"error": "too few correlated windows"}


def row(cid, m, flag):
    if "error" in m:
        return f"{cid:40s} {m['error']}"
    mark = "  DRIFT" if abs(m["drift_ms"]) >= flag else ""
    return (f"{cid:40s} {m['windows']:4d}  median {m['median_ms']:+5.0f} ms  drift {m['drift_ms']:+6.0f} ms over "
            f"{m['span_s']:.0f} s  (first quarter {m['first_q_ms']:+.0f}, last {m['last_q_ms']:+.0f}){mark}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true", help="every enabled climb, not just the focus")
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--flag", type=float, default=60.0)
    ap.add_argument("--win", type=float, default=4.0)
    ap.add_argument("--step", type=float, default=8.0)
    ap.add_argument("--max", type=int, default=250)
    ap.add_argument("--keep")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--wav")
    ap.add_argument("--ref")
    a = ap.parse_args(argv)
    if a.wav:
        if not a.ref:
            ap.error("--wav needs --ref")
        m = measure(a.wav, a.ref, a.win, a.step, a.max) or {"error": "too few correlated windows"}
        print(json.dumps(m) if a.json else row(os.path.basename(a.wav), m, a.flag))
        return
    with open(os.path.join(ROOT, "climbs.json")) as f:
        reg = json.load(f)
    ids = a.ids or ([c["id"] for c in reg["climbs"] if c.get("enabled") and c.get("song")] if a.all else focus_ids(reg))
    work = a.keep or tempfile.mkdtemp(prefix="driftscan-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    os.makedirs(work, exist_ok=True)
    try:
        with ThreadPoolExecutor(max_workers=max(1, a.j)) as ex:
            res = dict(ex.map(lambda c: scan(c, work, a), ids))
    finally:
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)
    if a.json:
        print(json.dumps(res, indent=1))
        return
    for cid in ids:
        print(row(cid, res[cid], a.flag))
    bad = [c for c in ids if "drift_ms" in res[c] and abs(res[c]["drift_ms"]) >= a.flag]
    print(f"\n{len(bad)} of {len(ids)} drift by {a.flag:g} ms or more" + (f": {', '.join(bad)}" if bad else ""))


if __name__ == "__main__":
    main()
