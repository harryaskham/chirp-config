#!/usr/bin/env python3
"""Master ride / master chain for a hand-written YAML song (levelride.py edits tab maps; this edits songs directly).
Appends one `master:` line in JSON flow style (valid YAML) to a song that has no top-level `master` yet:
an optional fader ride (levelride.ride: short-term loudness of the reference minus the render, median removed, as a
gain lane `auto.ride`) followed by any extra master effects (e.g. a clipper for a brick-walled record).

  songride.py SONG.yaml REF.wav RENDER.wav -o OUT.yaml [--win 4] [--step 2] [--max 9] [--amount 1]
              [--contour --sections F] [--slew 8] [--no-ride] [--fx "clip drive=3dB ceiling=-0.5dB" …]

--no-ride writes only the --fx chain (e.g. --no-ride --fx rack:master-loud). Refuses a song that already has a
top-level master (edit that by hand)."""
import json
import os
import sys
import importlib.util

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("lr", os.path.join(HERE, "levelride.py"))
LR = importlib.util.module_from_spec(spec); spec.loader.exec_module(LR)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    song, ref, render, out = a[0], a[1], a[2], opt("-o", "")
    text = open(song).read()
    if any(line.startswith("master:") for line in text.splitlines()):
        sys.exit(f"{song} already has a top-level master; edit it by hand")
    fx_extra = [a[i + 1] for i, k in enumerate(a) if k == "--fx"]
    master = {"fx": []}
    if "--no-ride" not in a:
        t, d = LR.ride(ref, render, opt("--win", 4.0), opt("--step", 2.0), opt("--max", 9.0), opt("--amount", 1.0))
        if "--contour" in a:
            secs = [float(v) for v in open(opt("--sections", "")).read().strip().split(",")]
            d = LR.contour_only(t, d, secs)
        if "--slew" in a:
            lim = opt("--slew", 8.0); d = d.copy()
            for i in range(1, len(d)):
                d[i] = np.clip(d[i], d[i - 1] - lim * (t[i] - t[i - 1]), d[i - 1] + lim * (t[i] - t[i - 1]))
            for i in range(len(d) - 2, -1, -1):
                d[i] = np.clip(d[i], d[i + 1] - lim * (t[i + 1] - t[i]), d[i + 1] + lim * (t[i + 1] - t[i]))
        master["fx"].append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}})
        master["auto"] = {"ride": {"points": [["0s", round(float(d[0]), 2)]] + [[f"{x:.2f}s", round(float(v), 2)] for x, v in zip(t, d)]}}
        print(f"ride: {len(t)} points, range {d.min():+.1f}..{d.max():+.1f} dB, mean |d| {np.abs(d).mean():.1f} dB", file=sys.stderr)
    master["fx"] += fx_extra
    if not master["fx"]:
        sys.exit("nothing to write: no ride and no --fx")
    open(out, "w").write(text.rstrip("\n") + "\nmaster: " + json.dumps(master, separators=(", ", ": ")) + "\n")
    print(f"wrote {out}: master fx {[f if isinstance(f, str) else f['type'] for f in master['fx']]}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
