#!/usr/bin/env python3
"""Fine beat grid for a tab2song map: follow a band that does not play to a click. The tab's eighth-note grid is
compared with a drum stem's onsets in blocks of N measures (pulse phase: the shift that puts the most onset energy
on the grid), the offsets are unwrapped against their neighbours, weak blocks interpolated, and every measure's
tempo rescaled so each block starts where the band really played it — the shape inside a block (a fermata, a
ritardando) is kept because all its measures scale together. Writes per-measure "bpm" overrides into the map.

  beatgrid.py MAP.json DRUMS.wav [--block 8] [--minconf 1.5] [--unwrap] [-o OUT.json] [--report]

Run, regenerate the song, (re-transcribe stem-timed parts on the new tempo map), and re-run to check the residual."""
import json
import os
import sys
import importlib.util

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t2s", os.path.join(HERE, "tab2song.py"))
T2S = importlib.util.module_from_spec(spec); spec.loader.exec_module(T2S)


def onset_curve(stem):
    F = L.Feat(L.load(stem))
    o = np.maximum(F.onset - np.convolve(F.onset, np.ones(int(L.FPS)) / int(L.FPS), "same"), 0)
    return np.convolve(o, np.hanning(3) / 2, "same")


def phases(mp, o, block=8):
    root = os.path.dirname(HERE)
    cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(root, mp["cache"])
    keep = [m for m in T2S.corrected_timeline(cache, mp) if not m["skip"]]
    t, starts, grid = mp.get("offset", 0.0), [], []
    for i, m in enumerate(keep):
        starts.append(t); P = 30 / m["bpm"]
        for k in range(int(round(m["beats"] * 2))):
            grid.append((t + k * P, P, i))
        t += m["beats"] * 60 / m["bpm"]
    G = np.array([g[0] for g in grid]); Pg = np.array([g[1] for g in grid]); Ig = np.array([g[2] for g in grid])
    at = lambda ts: o[np.clip(np.round(np.asarray(ts) * L.FPS).astype(int), 0, len(o) - 1)]
    blocks = []
    for b0 in range(0, len(keep), block):
        sel = (Ig >= b0) & (Ig < b0 + block)
        if sel.sum() < 6:
            continue
        P = float(np.median(Pg[sel])); ds = np.arange(-P / 2, P / 2, 0.002)
        sc = np.array([at(G[sel] + d).mean() for d in ds]); k = int(np.argmax(sc))
        blocks.append({"i": b0, "m": keep[b0]["m"], "t": starts[b0], "d": float(ds[k]), "q": float(sc[k] / (sc.mean() + 1e-9)), "P": P})
    return keep, starts, blocks


def fit(mp, stem, block=8, minconf=1.5, unwrap=False):
    o = onset_curve(stem)
    keep, starts, blocks = phases(mp, o, block)
    # Offsets stay the minimal phase correction (|d| <= half an eighth): the coarse alignment (scorealign.py)
    # already holds sections within ~0.2 s, and unwrapping block to block can accumulate whole-eighth slips
    # that shift a section's parts off the real downbeat. --unwrap allows it for grids known to be close.
    prev = 0.0
    for b in blocks:
        if b["q"] < minconf:
            b["d"] = None
            continue
        if unwrap:
            b["d"] = min((b["d"] + s * b["P"] for s in (-1, 0, 1)), key=lambda v: abs(v - prev))
        prev = b["d"]
    known = [(b["t"], b["d"]) for b in blocks if b["d"] is not None]
    for b in blocks:
        if b["d"] is None:
            b["d"] = float(np.interp(b["t"], [k[0] for k in known], [k[1] for k in known]))
    # real block starts, then per-measure tempo factors so each block spans real[j] → real[j+1]
    bpm = {}
    n = len(keep)
    for j, b in enumerate(blocks):
        i0 = b["i"]; i1 = blocks[j + 1]["i"] if j + 1 < len(blocks) else n
        old = sum(keep[i]["beats"] * 60 / keep[i]["bpm"] for i in range(i0, i1))
        d_next = blocks[j + 1]["d"] if j + 1 < len(blocks) else b["d"]
        new = old + (d_next - b["d"])
        k = old / max(new, 1e-3)
        for i in range(i0, i1):
            bpm[str(keep[i]["m"])] = round(keep[i]["bpm"] * k, 4)
    if blocks:
        mp = dict(mp); mp["offset"] = round(mp.get("offset", 0.0) + blocks[0]["d"], 4)
    mp["bpm"] = bpm
    return mp, blocks


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp = json.load(open(a[0]))
    if "--report" in a:
        _, _, blocks = phases(mp, onset_curve(a[1]), opt("--block", 8))
        res = [abs(b["d"]) * 1000 for b in blocks if b["q"] >= opt("--minconf", 1.5)]
        print(f"{len(blocks)} blocks; residual |offset| median {np.median(res):.0f} ms, p90 {np.percentile(res, 90):.0f} ms (confident blocks)")
        sys.exit()
    new, blocks = fit(mp, a[1], opt("--block", 8), opt("--minconf", 1.5), "--unwrap" in a)
    json.dump(new, open(opt("-o", a[0]), "w"), indent=1)
    print(f"{len(blocks)} blocks; offsets (ms): " + " ".join(f"{b['d'] * 1000:+.0f}" for b in blocks))
