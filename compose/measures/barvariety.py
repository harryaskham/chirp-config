#!/usr/bin/env python3
"""barvariety: bar-by-bar variety (chirper-two; compscore plugin, compose/measures/). Harry's brief for Odd Hours:
"really vary bar-by-bar ... no two consecutive bars alike unless the repetition is the point". This measures it.

1. Bar-scale windows at the declared tempo: 4 beats and 3 beats (meters change bar by bar, so one window length
   would line up with nothing; two scales average it out), each from the song's start.
2. Per window: HARMONY (mean chroma), ORCHESTRATION (level-normalised 40-band log spectrum), DENSITY (onset
   peaks per second), LEVEL (dB) and RHYTHM (the onset envelope on 12 slots).
3. Per consecutive pair, a change c in 0..1: the mean of each dimension's distance over its scale, capped at 1
   (chroma 1-cos / .2, spectrum mean |dB| / 3, density |log2 ratio| / .6, level |dB| / 4, rhythm 1-r / .6).
4. VARIETY v: the mean of the median harmony, orchestration and rhythm changes (each over its scale, capped at
   1.5): how far a bar typically moves from the one before. Calibrated (map tempos, both window lengths):
   a looped bar .24, Blue Monday .38, I Feel Love .46, HBFS .62 | The National Anthem .61, The Woven Web .80,
   Money .98, Take Five 1.03, Saturnine 1.06, Playing God 1.15, So What 1.18, Pyramid Song 1.21.
5. NOISE GUARD: change without structure is not variety. ANCHOR = the median, over windows, of the best
   similarity to any window at least two away; bars shuffled from six unrelated songs anchor .39 (records >= .50).
   Random filtered noise moves its orchestration 2.5 (records <= 1.35).
6. score = 100 * clip((v - .4) / .55) * clip((anchor - .38) / .12) * clip((2.4 - orchestration) / .4).
   Scores (28-29 Oct): records So What, Take Five, Money, Pyramid Song, Thin Thing, Saturnine, Playing God 100,
   The Woven Web 73, The National Anthem 38; loops Blue Monday 0, I Feel Love 12, HBFS 40; controls: a looped bar
   0, bars shuffled from six songs 11, random filtered noise 0; Ferrous Bloom's Splinterwork 17, Moult 35;
   Odd Hours t2 55, t4 ~100.
   change_share (pairs with c >= .22) is reported, not scored: at bar scale nearly every real bar differs a little.

Detail-only until the album sets a weight (weight_scale 0 without a `barvariety` key in album.json weights).

  python3 compose/measures/barvariety.py WAV BPM
"""
import numpy as np

SAME = 0.22
SCALES = {"harmony": 0.2, "orchestration": 3.0, "density": 0.6, "level": 4.0, "rhythm": 0.6}


def _fps(F):
    return F.n / (len(F.x) / 48000.0)


def _peaks(o, fps):
    """Onset peaks: local maxima above the median + 1.5 MAD of the onset curve."""
    thr = np.median(o) + 1.5 * np.median(np.abs(o - np.median(o)))
    k = np.where((o[1:-1] > o[:-2]) & (o[1:-1] >= o[2:]) & (o[1:-1] > thr))[0] + 1
    return k


def _windows(F, bpm, beats):
    fps = _fps(F)
    w = int(round(beats * 60.0 / bpm * fps))
    n = F.n // w
    if n < 6:
        return None
    o = F.onset
    pk = np.zeros(F.n)
    pk[_peaks(o, fps)] = 1
    lv = 10 * np.log10(F.bands.sum(0) + 1e-12)
    out = []
    for i in range(n):
        a, b = i * w, (i + 1) * w
        ch = F.chroma[:, a:b].mean(1)
        ch = ch / (np.linalg.norm(ch) + 1e-12)
        sp = F.logb[:, a:b].mean(1)
        sp = sp - sp.mean()
        dens = pk[a:b].sum() / (w / fps)
        level = float(np.mean(lv[a:b]))
        env = o[a:b]
        pat = np.array([env[int(j * len(env) / 12):int((j + 1) * len(env) / 12)].mean() for j in range(12)])
        out.append((ch, sp, dens, level, pat))
    return out


def _change(u, v):
    ch1, sp1, d1, l1, p1 = u
    ch2, sp2, d2, l2, p2 = v
    dh = 1 - float(ch1 @ ch2)
    dt = float(np.mean(np.abs(sp1 - sp2)))
    dd = abs(np.log2((d1 + 0.5) / (d2 + 0.5)))
    dl = abs(l1 - l2)
    r = np.corrcoef(p1, p2)[0, 1] if p1.std() > 1e-9 and p2.std() > 1e-9 else 1.0
    dr = 1 - float(r)
    parts = {"harmony": dh, "orchestration": dt, "density": dd, "level": dl, "rhythm": dr}
    return float(np.mean([min(1.0, parts[k] / SCALES[k]) for k in parts])), parts


def analyse(F, bpm):
    rows = []
    for beats in (4, 3):
        W = _windows(F, bpm, beats)
        if not W:
            continue
        cons = [_change(W[i], W[i + 1]) for i in range(len(W) - 1)]
        cs = np.array([c for c, _ in cons])
        change = float(np.mean(cs >= SAME))
        best = []
        for i in range(len(W)):
            sims = [1 - _change(W[i], W[j])[0] for j in range(len(W)) if abs(i - j) >= 2]
            if sims:
                best.append(max(sims))
        anchor = float(np.median(best)) if best else 0.0
        dims = {k: float(np.median([p[k] / SCALES[k] for _, p in cons])) for k in SCALES}
        rows.append((beats, change, anchor, float(np.median(cs)), dims))
    if not rows:
        return {"score": None}
    change = float(np.mean([r[1] for r in rows]))
    anchor = float(np.mean([r[2] for r in rows]))
    dims = {k: float(np.mean([r[4][k] for r in rows])) for k in SCALES}
    # VARIETY: how far a bar moves from the one before in harmony, orchestration and rhythm (medians over the
    # piece, each over its scale and capped at 1.5). Calibration: loops 0.24-0.46 (a looped bar, Blue Monday,
    # I Feel Love), jazz and prog 0.8-1.2 (So What, Take Five, Pyramid Song, Playing God, Saturnine).
    v = float(np.mean([min(1.5, dims[k]) for k in ("harmony", "orchestration", "rhythm")]))
    var = float(np.clip((v - 0.4) / 0.55, 0, 1))
    # NOISE GUARD: change that anchors nothing (bars shuffled from unrelated songs: anchor 0.39) or that is
    # noise-like timbre jumps (random filtered noise: orchestration 2.5) is not variety. Real records anchor >= 0.5
    # and move their orchestration <= 1.35; a klangfarbenmelodie passing the line between instruments every bar
    # (Odd Hours t4) moves it ~1.6, which is the point: the timbre guard only starts at 2.0.
    guard = float(np.clip((anchor - 0.38) / 0.12, 0, 1)) * float(np.clip((2.4 - dims["orchestration"]) / 0.4, 0, 1))
    score = 100.0 * var * guard
    return {"score": round(score, 1), "variety": round(v, 3), "guard": round(guard, 2),
            "change_share": round(change, 3), "anchor": round(anchor, 3),
            "median_change": round(float(np.mean([r[3] for r in rows])), 3),
            "dims_median": {k: round(x, 2) for k, x in dims.items()}}


def measure(ctx):
    bpm = ctx.get("bpm")
    if not bpm:
        return None, {"note": "no declared tempo"}
    d = analyse(ctx["F"], float(bpm))
    if d.get("score") is None:
        return None, d
    if "barvariety" not in ((ctx.get("album") or {}).get("weights") or {}):
        d["weight_scale"] = 0.0  # detail-only until the album gives it a weight
    return d["score"], d


if __name__ == "__main__":
    import json
    import os
    import sys
    sys.path.insert(0, os.path.expanduser("~/.config/chirp/tools"))
    import likeness as L
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    x = L.load(sys.argv[1])
    print(os.path.basename(sys.argv[1]), json.dumps(analyse(L.Feat(x), float(sys.argv[2]))))
