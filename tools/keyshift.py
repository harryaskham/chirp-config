#!/usr/bin/env python3
"""keyshift: is our render (or one part) in the record's key? The best circular pitch-class shift of our chroma
against the record's (chirper-one's S&M check: Metallica's S&M set is tuned a half step down, and Master of
Puppets' E-standard tab read chroma 5.5 until transposed -1, then 26; the best shift was -1 in every window).

  keyshift.py [ID …] [--all] [--per-track] [-j 3] [--json]     # default: the focus's climbs with a song
  keyshift.py --wav OURS.wav --ref REF.wav

likeness's chroma (12 pitch classes per frame, normalised) of ours, rolled by k = -6..+5 semitones, against the
record's: the mean frame cosine per k. Reported: the best k (the transpose to APPLY to ours: -1 = ours sounds a
semitone sharp), its gain over k = 0, and how many 10 s windows agree. --per-track renders each track solo against
the record's mix (one mistuned part shows even when the song's best k is 0). Per-track flags to ignore: percussion
reads noise, and harmony/backing lines read their interval to the lead (S&M: Master of Puppets' bvox -5, Sad but
True's added guitars -3, all five songs' mixes 0 after chirper-one's fix). Fix with the
tab map's "transpose" key (tab2song, map-wide or per part) after checking the tab's tuning field. Read-only.
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
import chirpbin  # noqa: E402
import driftscan  # noqa: E402  (focus_ids, track_names)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIFTS = list(range(-6, 6))


def chroma(path):
    import likeness as L
    return L.Feat(L.load(path)).chroma            # [12, frames], each frame normalised to sum 1


def shift_scores(ours, ref):
    """{k: mean frame cosine of roll(ours, k) against ref}."""
    n = min(ours.shape[1], ref.shape[1])
    o, r = ours[:, :n], ref[:, :n]
    rn = r / (np.linalg.norm(r, axis=0, keepdims=True) + 1e-9)
    out = {}
    for k in SHIFTS:
        ok = np.roll(o, k, axis=0)
        ok = ok / (np.linalg.norm(ok, axis=0, keepdims=True) + 1e-9)
        out[k] = float((ok * rn).sum(0).mean())
    return out


def measure(ours, ref, win_s=10.0):
    """Best shift, its gain over 0, and the share of windows whose own best shift agrees."""
    import likeness as L
    sc = shift_scores(ours, ref)
    best = max(sc, key=sc.get)
    w = max(1, int(win_s * L.FPS))
    n = min(ours.shape[1], ref.shape[1])
    wins = [max((s := shift_scores(ours[:, i:i + w], ref[:, i:i + w])), key=s.get) for i in range(0, n - w + 1, w)]
    agree = sum(1 for b in wins if b == best)
    return {"best": best, "score": round(sc[best], 4), "score0": round(sc[0], 4), "gain": round(sc[best] - sc[0], 4),
            "windows": len(wins), "agree": agree}


def scan(cid, work, a):
    song = os.path.join(ROOT, "songs", f"{cid}.yaml")
    ref = os.path.join(ROOT, "ref", f"{cid}.wav")
    if not (os.path.exists(song) and os.path.exists(ref)):
        return cid, {"_mix": {"error": "no song or reference"}}
    rc = chroma(ref)
    renders = [("", [])] + ([(n, ["--solo", n]) for n in driftscan.track_names(song)] if a.per_track else [])
    res = {}
    for name, extra in renders:
        out = os.path.join(work, f"{cid}{'-' + name if name else ''}.wav")
        r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song, *extra, "-o", out],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode:
            res[name or "_mix"] = {"error": f"render failed: {r.stderr.strip()[-160:]}"}
            continue
        res[name or "_mix"] = measure(chroma(out), rc)
        os.unlink(out)
    return cid, res


def row(cid, res):
    m = res.get("_mix", {})
    if "error" in m:
        return f"{cid:34s} {m['error']}"
    flag = f"  <- transpose {m['best']:+d}?" if m["best"] != 0 and m["gain"] > 0.01 else ""
    line = (f"{cid:34s} best shift {m['best']:+d} (chroma cos {m['score']:.3f} vs {m['score0']:.3f} at 0; "
            f"{m['agree']}/{m['windows']} windows agree){flag}")
    tr = [(k, v) for k, v in res.items() if k != "_mix" and "best" in v]
    if tr:
        line += "\n    per track: " + ", ".join(f"{k} {v['best']:+d}" + ("*" if v["best"] != 0 and v["gain"] > 0.01 else "")
                                             for k, v in tr)
    return line


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--per-track", action="store_true")
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--wav")
    ap.add_argument("--ref")
    a = ap.parse_args(argv)
    if a.wav:
        if not a.ref:
            ap.error("--wav needs --ref")
        m = measure(chroma(a.wav), chroma(a.ref))
        print(json.dumps(m) if a.json else row(os.path.basename(a.wav), {"_mix": m}))
        return
    with open(os.path.join(ROOT, "climbs.json")) as f:
        reg = json.load(f)
    ids = a.ids or ([c["id"] for c in reg["climbs"] if c.get("enabled") and c.get("song")] if a.all
                    else driftscan.focus_ids(reg))
    work = tempfile.mkdtemp(prefix="keyshift-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    try:
        with ThreadPoolExecutor(max_workers=max(1, a.j)) as ex:
            res = dict(ex.map(lambda c: scan(c, work, a), ids))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if a.json:
        print(json.dumps(res, indent=1))
        return
    for cid in ids:
        print(row(cid, res[cid]))


if __name__ == "__main__":
    main()
