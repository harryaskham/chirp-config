#!/usr/bin/env python3
"""floorscan: where does our render fall to digital silence while the record keeps a floor? (chirper-zero's
fleet-wide lead #2; tools/floorfit.py then fills a gap with the record's own calibrated floor.)

  floorscan.py [ID …] [--all] [-j 3] [--under 20] [--win 2] [--quiet -90] [--keep DIR] [--json]
  floorscan.py --wav OURS.wav --ref REF.wav [--under 20] [--win 2]               # analysis only

Default IDs: the focus's climbs (climbs.json `focus`), else every enabled climb; each is rendered with the adopted
groove pin (nice 15). Per --win s window and per band (9 log bands, 30 Hz-16 kHz), our mean band power is compared
with the record's; a band more than --under dB under the record's is a gap (the record's room/tape floor, or a
sound we lack), unless the record's band is itself below --quiet dBFS (both silent). Gaps are reported as runs of
windows with their bands and worst deficit, each with the floorfit command to try. Pulk/Pull v6: a calibrated low
noise bed under its 172-200 s break and broadband floors in the intro gaps were +1.6 on every seed (break sections
+9/+11). What paid so far is a whole SECTION gone silent; scattered gaps did not: You and Whose Army's 8 kHz+ air at
168-178 s +0.04, its 60 Hz-2.2 kHz floor at 186-190 s -0.17 (stereo and loudness terms), Hunting Bears' floors no
change. A gap can also be a missing PART: listen before filling it with noise. Read-only.
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
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import driftscan  # noqa: E402  (focus_ids)
import likeness as L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGES = np.geomspace(30, 16000, 10)          # 9 bands


def band_levels(path, win):
    """[windows, 9] mean band power in dBFS per --win s window."""
    x = L.load(path)
    x = x.mean(1) if x.ndim > 1 else x
    f, _, Z = signal.stft(x, L.SR, nperseg=4096, noverlap=4096 - 1024, boundary=None, padded=False)
    P = np.abs(Z) ** 2                     # scipy's stft already scales by the window sum (full-scale sine ~ -6 dB)
    bands = np.stack([P[(f >= a) & (f < b)].sum(0) for a, b in zip(EDGES[:-1], EDGES[1:])])
    fps = L.SR / 1024
    w = max(1, int(round(win * fps)))
    n = bands.shape[1] // w
    if n == 0:
        return np.zeros((0, 9))
    m = bands[:, : n * w].reshape(9, n, w).mean(2)
    return 10 * np.log10(m.T + 1e-14)


def gaps(ours, ref, under=20.0, quiet=-90.0):
    """[(window, [(band, deficit_db), …])] where ours is more than `under` dB under a non-silent record band."""
    n = min(len(ours), len(ref))
    out = []
    for i in range(n):
        bad = [(b, float(ref[i, b] - ours[i, b])) for b in range(9)
               if ref[i, b] > quiet and ref[i, b] - ours[i, b] > under]
        if bad:
            out.append((i, bad))
    return out


def runs(g, win):
    """Contiguous windows merged: [(t0, t1, bands, worst_deficit)]."""
    out = []
    for i, bad in g:
        t0, t1 = i * win, (i + 1) * win
        bands = {b for b, _ in bad}
        worst = max(d for _, d in bad)
        if out and abs(out[-1][1] - t0) < 1e-9:
            a, _, bs, w = out[-1]
            out[-1] = (a, t1, bs | bands, max(w, worst))
        else:
            out.append((t0, t1, bands, worst))
    return out


def band_name(b):
    lo, hi = EDGES[b], EDGES[b + 1]
    fmt = lambda v: f"{v / 1000:.1f}k" if v >= 1000 else f"{v:.0f}"  # noqa: E731
    return f"{fmt(lo)}-{fmt(hi)}"


def measure(ours_path, ref_path, a):
    g = gaps(band_levels(ours_path, a.win), band_levels(ref_path, a.win), a.under, a.quiet)
    return {"windows": len(g), "runs": [{"from": t0, "to": t1, "bands": [band_name(b) for b in sorted(bs)],
                                         "worst_db": round(w, 1)} for t0, t1, bs, w in runs(g, a.win)]}


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
    return cid, measure(out, ref, a)


def report(cid, m, under):
    if "error" in m:
        return f"{cid:40s} {m['error']}"
    if not m["windows"]:
        return f"{cid:40s} no gaps (every band within {under:g} dB of a non-silent record)"
    lines = [f"{cid:40s} {m['windows']} gap windows in {len(m['runs'])} runs"]
    for r in m["runs"][:8]:
        lines.append(f"    {r['from']:6.0f}-{r['to']:<6.0f}s  worst {r['worst_db']:4.0f} dB under  bands "
                     f"{', '.join(r['bands'])}")
    lines.append(f"    fill one: python3 tools/floorfit.py measure ref/{cid}.wav --from A --to B, then "
                 f"floorfit.py fit songs/{cid}.yaml ref/{cid}.wav --from A --to B -o OUT (listen first)")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--under", type=float, default=20.0)
    ap.add_argument("--win", type=float, default=2.0)
    ap.add_argument("--quiet", type=float, default=-90.0, help="a record band under this (dBFS) is silent too")
    ap.add_argument("--keep")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--wav")
    ap.add_argument("--ref")
    a = ap.parse_args(argv)
    if a.wav:
        if not a.ref:
            ap.error("--wav needs --ref")
        m = measure(a.wav, a.ref, a)
        print(json.dumps(m, indent=1) if a.json else report(os.path.basename(a.wav), m, a.under))
        return
    with open(os.path.join(ROOT, "climbs.json")) as f:
        reg = json.load(f)
    ids = a.ids or ([c["id"] for c in reg["climbs"] if c.get("enabled") and c.get("song")] if a.all
                    else driftscan.focus_ids(reg))
    work = a.keep or tempfile.mkdtemp(prefix="floorscan-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
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
        print(report(cid, res[cid], a.under))


if __name__ == "__main__":
    main()
