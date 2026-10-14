#!/usr/bin/env python3
"""Full-mix "feel" comparison between a reference and a render, per section and band.

  mixfeel.py REF.wav OURS.wav T0,T1,...,Tn [--grid DOWNBEAT_S,BAR_S] [--json]

Everything is measured on the full mixes (no source separation), so it is grounded in what a listener hears.
Per band (sub 30-80, low 80-250, lowmid 250-800, mid 800-2.5k, presence 2.5-6k, air 6-16k), on 5 ms envelopes:

  punch    median attack rise at onsets: peak level in the 30 ms after an onset minus the minimum in the 60 ms
           before it (dB). Low punch = soft, smeared attacks; high = slaps, picks, sticks.
  rate     onsets per second in the band (distinct attacks, >= 3 dB rises 60 ms apart).
  vary     std of onset peak levels (dB): how different consecutive notes/hits are. Low = every note the same.
  micro    std of the 5 ms level around its 400 ms moving average (dB): fast movement inside the sound.
  crest    99th minus 50th percentile of the 5 ms level (dB).
  lock     (with --grid) share of the band's onsets within +-15 ms of a 16th of the bar grid. Hits played to a
           tight grid score high; amplitude ripple (beating between low partials), separation leakage and
           smeared sustains score ~26% (chance). ALWAYS check lock before reading punch/rate as "hits": on
           shadows the reference's sub band showed 10.5 'onsets'/s at 16 dB punch that were ripple (uniform
           offsets, no beater click), not a double kick.

Plus, per section:

  indep    1 - mean pairwise correlation between the six bands' onset functions: how independently the
           frequency ranges move. A homogeneous "wall" mix (everything accenting together, or nothing accenting)
           scores low; separate instruments playing their own rhythms score high.
  macro    std of the 400 ms level (dB): section-level dynamics.
"""
import json
import sys

import numpy as np
from scipy import signal as sg

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import likeness as L  # noqa: E402

SR = 48000
HOP = 240  # 5 ms
BANDS = [("sub", 30, 80), ("low", 80, 250), ("lowmid", 250, 800), ("mid", 800, 2500), ("pres", 2500, 6000), ("air", 6000, 16000)]


def envelopes(x):
    m = x.mean(1) if x.ndim == 2 else x
    out = []
    for _, lo, hi in BANDS:
        sos = sg.butter(4, [lo, hi], "bandpass", fs=SR, output="sos")
        y = sg.sosfilt(sos, m) ** 2
        n = len(y) // HOP
        out.append(10 * np.log10(y[: n * HOP].reshape(n, HOP).mean(1) + 1e-12))
    return np.array(out)  # bands x frames (dB)


def onsets(e):
    """Onset frames of one band envelope: rises >= 3 dB over 30 ms, at least 60 ms apart."""
    rise = np.zeros_like(e)
    rise[6:] = e[6:] - e[:-6]
    pk, _ = sg.find_peaks(rise, height=3.0, distance=12)
    return pk


GRID = None  # (downbeat_s, bar_s) when --grid is given


def band_feats(e, a, b):
    seg = e[a:b]
    floor = np.percentile(seg, 99) - 45  # ignore the noise floor: onsets must reach within 45 dB of the peak level
    pk = [p for p in onsets(seg) if seg[min(len(seg) - 1, p + 6)] > floor]
    rises, peaks = [], []
    for p in pk:
        pre = seg[max(0, p - 18):p + 1].min()
        post = seg[p:p + 7].max()
        rises.append(post - pre)
        peaks.append(post)
    dur = (b - a) * HOP / SR
    smooth = np.convolve(seg, np.ones(80) / 80, "same")
    lock = 0.0
    if GRID and pk:
        six = GRID[1] / 16
        offs = [((a + p) * HOP / SR - GRID[0]) / six for p in pk]
        lock = float(np.mean([abs(q - round(q)) * six <= 0.015 for q in offs]))
    return {
        "lock": lock,
        "punch": float(np.median(rises)) if rises else 0.0,
        "rate": len(pk) / dur,
        "vary": float(np.std(peaks)) if len(peaks) > 2 else 0.0,
        "micro": float(np.std((seg - smooth)[40:-40])),
        "crest": float(np.percentile(seg, 99) - np.percentile(seg, 50)),
    }


def section_feats(E, a, b):
    out = {name: band_feats(E[i], a, b) for i, (name, _, _) in enumerate(BANDS)}
    of = np.maximum(np.diff(E[:, a:b], axis=1), 0)
    of = of - of.mean(1, keepdims=True)
    c = np.corrcoef(of)
    iu = np.triu_indices(len(BANDS), 1)
    lin = 10 * np.log10(np.sum(10 ** (E[:, a:b] / 10), axis=0))
    lvl = np.convolve(lin, np.ones(80) / 80, "valid")[::80]
    out["_"] = {"indep": float(1 - np.nanmean(c[iu])), "macro": float(np.std(lvl))}
    return out


def main():
    global GRID
    argv = sys.argv[1:]
    if "--grid" in argv:
        i = argv.index("--grid")
        GRID = tuple(float(v) for v in argv[i + 1].split(","))
        del argv[i:i + 2]
    args = [x for x in argv if not x.startswith("--")]
    ref, ours, cuts = args[0], args[1], [float(t) for t in args[2].split(",")]
    Er, Eo = envelopes(L.load(ref)), envelopes(L.load(ours))
    n = min(Er.shape[1], Eo.shape[1])
    res = []
    for s0, s1 in zip(cuts[:-1], cuts[1:]):
        a, b = int(s0 * SR / HOP), min(n, int(s1 * SR / HOP))
        res.append({"start": s0, "end": s1, "ref": section_feats(Er, a, b), "ours": section_feats(Eo, a, b)})
    if "--json" in sys.argv:
        print(json.dumps(res, indent=1))
        return
    for i, r in enumerate(res):
        R, O = r["ref"], r["ours"]
        print(f"\n== section {i + 1} ({r['start']:.1f}-{r['end']:.1f} s)  indep ref {R['_']['indep']:.2f} ours {O['_']['indep']:.2f}"
              f"   macro ref {R['_']['macro']:.1f} ours {O['_']['macro']:.1f} dB")
        keys = ("punch", "rate", "vary", "micro", "crest") + (("lock",) if GRID else ())
        heads = {"punch": "punch dB", "rate": "rate /s", "vary": "vary dB", "micro": "micro dB", "crest": "crest dB", "lock": "lock %"}
        print("band     " + "".join(f"{heads[k]:>16s}" for k in keys))
        for name, _, _ in BANDS:
            print(f"{name:8s} " + "".join(
                f"{R[name][k] * (100 if k == 'lock' else 1):8.1f}{O[name][k] * (100 if k == 'lock' else 1):8.1f}" for k in keys))
    print("\n(columns: ref then ours)")


if __name__ == "__main__":
    main()
