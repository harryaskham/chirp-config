#!/usr/bin/env python3
"""Guitar-tone benchmark for amp/cab/string work (bd-6ccdf9): render a song's rhythm guitars soloed, profile the
palm-muted events with tonecmp, and compare with a stored separation-corrected target.

  guitarbench.py [--song songs/bleed.yaml] [--set 'tracks.N.patch=…' …] [--wav OUT.wav] [--json]

Defaults reproduce the Bleed numbers in bd-6ccdf9:
  events   tools/maps/bleed-gtr-events.txt — the 170 palm-muted Eb2 sixteenths of Songsterr 23825 track 2, bars 1-16
           (times in seconds from the recording's start: bar 1 at 0.396 s; only events < 39 s are used)
  window   5-110 ms after each pick; f0 77.78 Hz (Eb2)
  render   chirp render -f SONG --solo gtr-l --solo gtr-r --solo gtr-l2 --solo gtr-r2 --to 40s (T0 = 0)
  target   tools/maps/bleed-gtr-target.json = R − (S − O): R = the reference guitar stem
           (ref/stems/htdemucs_6s/bleed/guitar.wav, htdemucs_6s), S = the same model's guitar stem of our own mix
           (first 40 s), O = our soloed guitar render — the separation's own bias removed.
Prints the 1/6-octave envelope error grouped by region, the harmonic-line contrast per octave (ours, target) and
partial irregularity. Contrast = 90th − 10th percentile of the fine spectrum per octave, median over events: a
clean synthetic harmonic series reads high (deep valleys), a real rig fills the valleys."""
import json
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tonecmp as T  # noqa: E402

C = chirpbin.resolve("chirp")


def main():
    a = sys.argv[1:]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    song = opt("--song", os.path.join(ROOT, "songs/bleed.yaml"))
    wav = opt("--wav", "/tmp/guitarbench.wav")
    sets = [a[i + 1] for i, x in enumerate(a) if x == "--set"]
    evs = [float(v) for v in open(os.path.join(ROOT, "tools/maps/bleed-gtr-events.txt")).read().split(",") if float(v) < 39]
    tgt = json.load(open(os.path.join(ROOT, "tools/maps/bleed-gtr-target.json")))
    if "--no-render" not in a:
        cmd = ["nice", "-n", "15", C, "render", "-f", song, "--to", "40s", "-o", wav]
        for s in ("gtr-l", "gtr-r", "gtr-l2", "gtr-r2"):
            cmd += ["--solo", s]
        for s in sets:
            cmd += ["--set", s]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        if r.returncode:
            raise SystemExit(r.stderr[-400:])
    p = T.profile(wav, 0, evs, 0.005, 0.11, 77.78)
    c = np.array(tgt["centres"]); e = np.array(p["env"]) - np.array(tgt["env"])
    g = lambda lo, hi: float(np.mean(e[(c >= lo) & (c < hi)]))
    regions = {"lows 63-230": g(63, 230), "lowmid 230-1150": g(230, 1150), "mid 1150-2300": g(1150, 2300),
               "bite 2300-4200": g(2300, 4200), "fizz 4200-8500": g(4200, 8500)}
    con = {lo: (round(p["contrast"][lo], 1), round(tgt["contrast"][str(lo)], 1)) for lo in p["contrast"]}
    out = {"envelope_error_db": {k: round(v, 1) for k, v in regions.items()},
           "contrast_ours_target_db": con, "irregularity_ours_target_db": (round(p["irreg"], 2), round(tgt["irreg"], 2))}
    if "--json" in a:
        print(json.dumps(out)); return
    print("envelope error (ours − target, dB): " + "  ".join(f"{k} {v:+.1f}" for k, v in out["envelope_error_db"].items()))
    print("contrast per octave (ours / target, dB): " + "  ".join(f"{lo}: {o}/{t}" for lo, (o, t) in con.items()))
    print(f"partial irregularity (ours / target, dB): {out['irregularity_ours_target_db'][0]} / {out['irregularity_ours_target_db'][1]}")


if __name__ == "__main__":
    main()
