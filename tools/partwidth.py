#!/usr/bin/env python3
"""Per-part stereo width vs the record: which part is too wide (or narrow) for the master's band lanes to fix?
  partwidth.py SONG.yaml REF.wav --parts vox,pad [--stem ref/stems/.../vocals.wav] [--from 30] [--to 230] [--jobs 3]
Renders each part solo (chirp --solo; CHIRP env = the binary, default chirp), then prints side/mid dB per band
(60-150 / 150-400 / 400-1.2k / 1.2-3.5k / 3.5-8k) for the record, the optional stem and every part, with each
part's level. Flags parts >= 5 dB wider than the stem (or the record) in 400 Hz-8 kHz.
A LEAD that is much wider than its stem is a part-level fault no master width lane can separate: a track width
stage in the part ({"type": "width", "width": 0} in extra.fx; track fx run before pan) paid on four climbs - HBFS
vocoder +0.23 (with the synths at 0.6), TNA vox +0.22, Dreams vox (0.4) +0.33, Wuthering Heights vox +0.18 held-out.
Beds (keys, drums, pads) on a mature master usually LOSE when narrowed - the wb lanes are fitted around them (Flim)."""
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000
BANDS = [(60, 150), (150, 400), (400, 1200), (1200, 3500), (3500, 8000)]


def side_mid(x, a, b):
    x = x[int(a * SR):int(b * SR)]
    m, s = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2
    out = []
    for lo, hi in BANDS:
        sos = butter(4, [lo, hi], btype="band", fs=SR, output="sos")
        out.append(10 * np.log10((sosfilt(sos, s) ** 2).mean() + 1e-12) - 10 * np.log10((sosfilt(sos, m) ** 2).mean() + 1e-12))
    return np.array(out), 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)


def main():
    a = sys.argv[1:]
    if len(a) < 2 or "--parts" not in a:
        sys.exit(__doc__)
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    song, ref = a[0], a[1]
    parts = [p for p in opt("--parts", "").split(",") if p]
    t0, t1, jobs = opt("--from", 30.0), opt("--to", 230.0), opt("--jobs", 3)
    chirp = os.environ.get("CHIRP", "chirp")
    tmp = tempfile.mkdtemp(prefix="partwidth-")

    def render(p):
        out = os.path.join(tmp, f"{p}.wav")
        r = subprocess.run(["nice", "-n", "15", chirp, "render", "-f", song, "--solo", p, "-o", out], capture_output=True, text=True)
        return p, out if r.returncode == 0 else None

    with ThreadPoolExecutor(jobs) as ex:
        rendered = dict(ex.map(render, parts))
    hdr = " ".join(f"{lo}-{hi}".rjust(10) for lo, hi in BANDS)
    print(f"side/mid dB, {t0:.0f}-{t1:.0f} s   {hdr}   level")
    rec, lv = side_mid(L.load(ref), t0, t1)
    print(f"{'record':14s} " + " ".join(f"{v:10.1f}" for v in rec) + f"   {lv:6.1f}")
    base = rec
    if "--stem" in a:
        st, lv = side_mid(L.load(opt("--stem", "")), t0, t1)
        print(f"{'stem':14s} " + " ".join(f"{v:10.1f}" for v in st) + f"   {lv:6.1f}")
        base = st
    for p in parts:
        if not rendered.get(p):
            print(f"{p:14s} (render failed: unknown part?)")
            continue
        v, lv = side_mid(L.load(rendered[p]), t0, t1)
        if lv < -80:
            print(f"{p:14s} (silent in {t0:.0f}-{t1:.0f} s: pick a window where it plays)")
            os.remove(rendered[p])
            continue
        wide = float(np.mean(v[2:] - base[2:]))
        flag = f"  <- {wide:+.1f} dB wider than the {'stem' if '--stem' in a else 'record'} above 400 Hz" if wide >= 5 else (
            f"  <- {-wide:.1f} dB NARROWER (a mono lead vs a doubled/stacked record: try extra.double)" if wide <= -8 else "")
        print(f"{p:14s} " + " ".join(f"{x:10.1f}" for x in v) + f"   {lv:6.1f}{flag}")
        os.remove(rendered[p])
    os.rmdir(tmp)


if __name__ == "__main__":
    main()
