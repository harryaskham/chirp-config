#!/usr/bin/env python3
"""polymeter: beat-synchronous polymeter salience (chirper-two; compscore plugin, compose/measures/).

compscore's built-in `rhythm` term looks for periodicities OFF the eighth grid, but a djent polymeter lives ON the
sixteenth grid: a 9-, 11- or 13-sixteenth cell over a steady 4/4 pulse. This looks for it directly.

1. Onset strength: spectral flux of the long-term bands below 1 kHz (kick, chugs, stabs carry the cell; hats and
   ride keep the 4/4 and sit mostly above).
2. Quantise to sixteenths at the declared tempo (max flux within half a sixteenth of each grid point). The phase is
   the one of 8 within a sixteenth that best articulates the bar (largest variance of the 16-slot bar template).
3. Remove the LOCAL metre: each grid point minus the mean of the same bar slot in the 2 bars either side
   (leave-one-out). A song-wide template leaves each section's own beat pattern behind (straight 4/4 then reads as
   a lag-4 "cycle"); a local one removes it, while a cell that does not divide the bar still varies bar to bar at
   every slot and survives.
4. Autocorrelate the residual and score each candidate cycle L (5-47 sixteenths, not a whole number of beats, and
   more than 2 sixteenths from a bar multiple, where tempo drift between a recording and its grid fakes cycles) by
   its comb, mean(ac[L], ac[2L], ac[3L]): a repeating cell recurs at its multiples, noise does not. z = the best comb
   over a robust noise floor (1.4826 * MAD of ac over lags 3-100).
5. Global z (whole song) and the 75th-percentile z of 32-bar windows (hop 16), so a polymetric passage counts even
   when the rest of the song is straight; eff = their mean. score = 100 * clip((eff - LO) / (HI - LO)).

Calibration (28 Oct, chirper-two; tab maps' exact grids for the records, declared tempo for our renders):

| set | eff z |
|---|---|
| Meshuggah: Bleed 2.4, Lethargica 2.7, obZen 2.05, Broken Cog 2.0, The Faultless 1.9, Electric Red 1.65, Combustion 1.6, Pravus 1.5 | 1.5-2.7 |
| straight 4/4: Blue Monday 1.1, Enter Sandman 1.05, Sad But True 0.9, You Can't Hurry Love 1.15, Harder Better Faster Stronger 1.25, One 1.15, Raining Blood 1.1, Money (7/4) 1.25 | 0.9-1.25 |
| odd metre: Take Five (5/4) | 1.7 |
| ours: Moult (9-cell, found at 9/27/45) 2.9; Splinterwork (11-cell, found at 11/22, NINEFOLD at 9) 2.2 | |

LO 1.3, HI 2.3: straight 4/4 scores 0, Meshuggah 20-100, Take Five 40. The cycle it names is reliable on exact
grids (our renders); on recordings the windows' cycles are noisier (map drift). Known limits: a cell made only of
sustained notes has no onsets to find; a cycle that is a whole number of beats (3/4 over 4/4) is excluded by
design; blasts and tremolo raise the noise floor (Splinterwork's global z is 1.7, its windows 2.7).

Detail-only until the album sets a weight: with no `polymeter` key in album.json weights the result carries
weight_scale 0 (shown in --text, not counted in the total).

  python3 compose/measures/polymeter.py WAV BPM        analyse one render
  python3 compose/measures/polymeter.py --ref ID ...   analyse reference recordings on their tab maps' grids
"""
import numpy as np

FLUX_HZ = 1000.0
LO, HI = 1.3, 2.3
NEIGH = 2
WINDOW_BARS, HOP_BARS = 32, 16
MAXLAG = 100
CANDIDATES = [n for n in range(5, 48) if n % 4 and min(abs(n - 16 * m) for m in (1, 2, 3)) > 2]


def _flux(F, hi_hz=FLUX_HZ):
    edges = np.geomspace(30, 16000, 41)
    k = int(np.searchsorted(edges[1:], hi_hz, side="right"))
    d = np.maximum(0.0, np.diff(F.logb[:max(1, k)], axis=1)).sum(0)
    return np.concatenate([[0.0], d])


def _fps(F):
    return F.n / (len(F.x) / 48000.0)


def _quantise(o, times, fps, half):
    out = np.zeros(len(times))
    for i, t in enumerate(times):
        a, b = max(0, int(np.floor((t - half) * fps))), min(len(o), int(np.ceil((t + half) * fps)))
        out[i] = o[a:b].max() if b > a else 0.0
    return out


def _residual(q, pos):
    keys = {}
    for i, p in enumerate(pos):
        keys.setdefault(p, []).append(i)
    r = np.zeros(len(q))
    for idx in keys.values():
        v = q[idx].astype(float)
        for j in range(len(idx)):
            nb = [v[k] for k in range(max(0, j - NEIGH), min(len(v), j + NEIGH + 1)) if k != j]
            r[idx[j]] = v[j] - (np.mean(nb) if nb else v[j])
    return r - r.mean()


def _combz(r):
    n = len(r)
    if n < 2 * MAXLAG or not np.any(r):
        return 0.0, None
    ac = np.array([np.dot(r[:n - k], r[k:]) / (n - k) for k in range(MAXLAG + 1)])
    ac = ac / (ac[0] + 1e-12)
    comb = {c: float(np.mean([ac[k * c] for k in (1, 2, 3) if k * c <= MAXLAG])) for c in CANDIDATES}
    tail = ac[3:MAXLAG + 1]
    noise = 1.4826 * float(np.median(np.abs(tail - np.median(tail)))) + 1e-9
    c = max(comb, key=comb.get)
    return comb[c] / noise, c


def analyse(F, bpm=None, dur=None, times=None, pos=None):
    """F: likeness.Feat. Either an explicit sixteenth grid (times, and pos = one bar-slot key per point) or a
    declared tempo (a constant 4/4 grid whose phase is searched)."""
    fps = _fps(F)
    o = _flux(F)
    if times is None:
        s16 = 60.0 / float(bpm) / 4
        n = int((dur or len(o) / fps) / s16)
        best = None
        for k in range(8):
            q = _quantise(o, k * s16 / 8 + s16 * np.arange(n), fps, s16 / 2)
            v = float(np.array([q[j::16].mean() for j in range(16)]).var())
            if best is None or v > best[0]:
                best = (v, q)
        q = best[1]
        pos = [i % 16 for i in range(len(q))]
    else:
        q = _quantise(o, np.asarray(times), fps, float(np.median(np.diff(times))) / 2)
    zg, cg = _combz(_residual(q, pos))
    W, H = WINDOW_BARS * 16, HOP_BARS * 16
    wins = [_combz(_residual(q[a:a + W], pos[a:a + W])) for a in range(0, len(q) - W + 1, H)]
    zs = sorted(z for z, _ in wins)
    p75 = zs[int(0.75 * (len(zs) - 1))] if zs else zg
    eff = 0.5 * zg + 0.5 * p75
    cycles = {}
    for z, c in wins:
        if c and z >= 2.0:
            cycles[c] = cycles.get(c, 0) + 1
    return {"eff_z": round(eff, 2), "global_z": round(zg, 2), "cycle": cg, "window_p75_z": round(p75, 2),
            "windows": len(wins), "window_cycles": dict(sorted(cycles.items(), key=lambda kv: -kv[1])[:5]),
            "score": round(100.0 * float(np.clip((eff - LO) / (HI - LO), 0.0, 1.0)), 1)}


def measure(ctx):
    bpm = ctx.get("bpm")
    if not bpm:
        return None, {"note": "no declared tempo"}
    d = analyse(ctx["F"], bpm=bpm, dur=ctx.get("dur"))
    if "polymeter" not in ((ctx.get("album") or {}).get("weights") or {}):
        d["weight_scale"] = 0.0  # detail-only until the album gives it a weight
    return d["score"], d


def _ref_grid(sid):
    import json
    import os
    import sys
    cfg = os.path.expanduser("~/.config/chirp")
    sys.path.insert(0, os.path.join(cfg, "tools"))
    import tab2song as T
    m = json.load(open(os.path.join(cfg, "tools", "maps", f"{sid}.json")))
    times, pos = [], []
    for b in T.performed_timeline(m["cache"], m):
        s16, n = 60.0 / b["bpm"] / 4, int(round(b["beats"] * 4))
        for j in range(n):
            times.append(b["start"] + m.get("offset", 0) + j * s16)
            pos.append((n, j))
    return os.path.join(cfg, "ref", f"{sid}.wav"), np.array(times), pos


if __name__ == "__main__":
    import json
    import os
    import sys
    sys.path.insert(0, os.path.expanduser("~/.config/chirp/tools"))
    import likeness as L
    a = sys.argv[1:]
    if a and a[0] == "--ref":
        for sid in a[1:]:
            wav, times, pos = _ref_grid(sid)
            x = L.load(wav)
            print(sid, json.dumps(analyse(L.Feat(x), times=times, pos=pos)))
    elif len(a) == 2:
        x = L.load(a[0])
        print(os.path.basename(a[0]), json.dumps(analyse(L.Feat(x), bpm=float(a[1]), dur=len(x) / L.SR)))
    else:
        sys.exit(__doc__)
