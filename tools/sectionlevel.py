#!/usr/bin/env python3
"""Per-section ABSOLUTE level vs the reference — the gap the contour ride cannot close (levelride --contour removes
each section's mean) and the one likeness's mastering term punishes: a section 10 dB too loud scores ~13 there
(Flim's ending: the record drops 10-11 dB at 136 s and stays; a master gain lane gave +1.2 overall).
Results: Flim +1.2 (ending) then +2.95 (sections 1-7, 4-5 dB too loud), Daydreaming +1.65 (6 sections 2.5-5 dB quiet),
Hajnal +1.8, Saturnine +0.3, Shadows +0.2 (already within 1.4 dB). Full strength (--amount 1) beat half every time.

  sectionlevel.py SONG.yaml RENDER.wav REF.wav SECTIONS.txt [-o OUT.yaml] [--min 1.0] [--amount 1.0] [--only 2,7]
                  [--lane slev] [--ramp 0.5]

Prints each section's RMS, 99.9th-percentile peak and crest, ours vs the record. With -o, appends ONE gain stage at
the end of the song's master chain driven by a lane (default auto.slev) that steps at the section cuts to
-(ours - record) * amount dB for sections off by more than --min dB (others 0; default 1.0 — chirper-two: on
Saturnine 8 sections at --min 1 beat 2 sections at --min 2, 64.75 vs 64.5 held-out), ramping over --ramp seconds.
--only N,M (1-based) limits the correction to those sections. Song YAMLs with a one-line JSON `master:` (as
widthfit/songride/sectioneq write) or none. Keep only what the metric confirms (seeds 7/13 for small changes)."""
import json
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import likeness as L  # noqa: E402


def stats(x, a, b):
    s = x[int(a * 48000):int(b * 48000)]
    if len(s) < 4800:
        return None
    rms = 20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-9)
    pk = 20 * np.log10(np.percentile(np.abs(s), 99.9) + 1e-9)
    return rms, pk, pk - rms


def main():
    a = sys.argv[1:]
    if len(a) < 4:
        sys.exit(__doc__)
    song, render, ref, secf = a[:4]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    cuts = [float(x) for x in open(secf).read().replace("\n", ",").split(",") if x.strip()]
    R, O = L.load(ref), L.load(render)
    only = {int(v) for v in opt("--only", "").split(",") if v.strip()} if "--only" in a else None
    mn, amount = opt("--min", 1.0), opt("--amount", 1.0)
    gains = []
    print("section     start   ref rms  peak crest |  our rms  peak crest |  diff")
    for i in range(len(cuts) - 1):
        r, o = stats(R, cuts[i], cuts[i + 1]), stats(O, cuts[i], cuts[i + 1])
        if r is None or o is None:
            gains.append(0.0); continue
        d = o[0] - r[0]
        g = float(-d * amount) if abs(d) > mn and (only is None or i + 1 in only) else 0.0
        gains.append(round(g, 2))
        print(f"{i + 1:7d} {cuts[i]:9.1f}  {r[0]:7.1f} {r[1]:5.1f} {r[2]:5.1f} | {o[0]:7.1f} {o[1]:5.1f} {o[2]:5.1f} | {d:+5.1f}" + (f"  -> {g:+.1f} dB" if g else ""))
    if "-o" not in a:
        return
    lane = opt("--lane", "slev"); ramp = opt("--ramp", 0.5)
    lines = open(song).read().splitlines()
    mi = next((k for k, l in enumerate(lines) if l.startswith("master:")), None)
    master = json.loads(lines[mi][len("master:"):].strip()) if mi is not None else {"fx": []}
    if isinstance(master, list):
        master = {"fx": master}
    auto = master.setdefault("auto", {})
    if lane in auto:
        sys.exit(f"lane {lane} exists: pass --lane NAME")
    pts = [["0s", gains[0]]]
    for i in range(1, len(gains)):
        pts += [[f"{cuts[i] - ramp / 2:.3f}s", gains[i - 1]], [f"{cuts[i] + ramp / 2:.3f}s", gains[i]]]
    auto[lane] = {"points": pts}
    master.setdefault("fx", []).append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": f"auto.{lane}", "amount": 1}]}})
    line = "master: " + json.dumps(master)
    if mi is None:
        ci = next((k for k, l in enumerate(lines) if l.startswith(("ceiling:", "tempo:"))), 0)
        lines.insert(ci + 1, line)
    else:
        lines[mi] = line
    open(opt("-o", ""), "w").write("\n".join(lines) + "\n")
    print(f"lane {lane}: {sum(1 for g in gains if g)} sections corrected -> {opt('-o', '')}")


if __name__ == "__main__":
    main()
