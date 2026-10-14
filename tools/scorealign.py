#!/usr/bin/env python3
"""Score-to-audio alignment by dynamic time warping: map a render of a transcription (whose timeline is known)
onto the recording it transcribes, then read off where each measure really starts and the real tempo of each
tempo segment.

  scorealign.py REF.wav CAND.wav [--band 15] [--frame 0.2] [--tab DIR] [--offset S] [-o OUT.json]

Features per frame: chroma (12, unit-normalised), 8 coarse log-band energies and onset strength (z-scored per
signal), weighted 1 : 0.5 : 0.25; cost = 1 − cosine. Sakoe–Chiba band of ±band seconds around the diagonal;
off-diagonal steps cost a little extra so the path prefers steady tempo. With --tab (a songsterr.py cache whose
timeline the render follows, shifted by --offset seconds) the output also lists each measure's real start and
a fitted BPM per tempo segment."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402


def feats(path, frame):
    F = L.Feat(L.load(path))
    k = max(1, int(round(frame * L.FPS)))
    n = F.n // k

    def pool(a):
        return a[:, :n * k].reshape(a.shape[0], n, k).mean(2)

    ch = pool(F.chroma)
    ch = ch / (np.linalg.norm(ch, axis=0, keepdims=True) + 1e-9)
    edges = np.linspace(0, 40, 9).astype(int)
    lb = np.stack([F.logb[a:b].mean(0) for a, b in zip(edges[:-1], edges[1:])])
    lb = pool(lb)
    lb = (lb - lb.mean(1, keepdims=True)) / (lb.std(1, keepdims=True) + 1e-9)
    on = pool(F.onset[None, :])
    on = (on - on.mean()) / (on.std() + 1e-9)
    v = np.vstack([ch * 1.0, lb * 0.5 / np.sqrt(8), on * 0.25])
    return v / (np.linalg.norm(v, axis=0, keepdims=True) + 1e-9), n * k / L.FPS / n


def dtw(A, B, band):
    """A: cand (d×n), B: ref (d×m). Returns the path as (i, j) arrays."""
    n, m = A.shape[1], B.shape[1]
    INF = np.inf
    D = np.full((n + 1, m + 1), INF, dtype=np.float32)
    D[0, 0] = 0.0
    step = np.zeros((n + 1, m + 1), dtype=np.int8)
    slope = m / n
    for i in range(1, n + 1):
        c = int(round(i * slope))
        lo, hi = max(1, c - band), min(m, c + band)
        cost = 1.0 - A[:, i - 1] @ B[:, lo - 1:hi]
        diag = D[i - 1, lo - 1:hi]
        up = D[i - 1, lo:hi + 1] + 0.1           # cand advances, ref waits
        row = np.empty(hi - lo + 1, dtype=np.float32)
        st = np.empty(hi - lo + 1, dtype=np.int8)
        best = np.minimum(diag, up)
        st[:] = np.where(diag <= up, 0, 1)
        # left (ref advances, cand waits) needs a running pass along the row
        prev = D[i, lo - 1]
        for t in range(hi - lo + 1):
            left = prev + 0.1
            if left < best[t]:
                row[t] = cost[t] + left; st[t] = 2
            else:
                row[t] = cost[t] + best[t]
            prev = row[t]
        D[i, lo:hi + 1] = row
        step[i, lo:hi + 1] = st
    i, j, path = n, m, []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        s = step[i, j]
        if s == 0:
            i, j = i - 1, j - 1
        elif s == 1:
            i -= 1
        else:
            j -= 1
    path.reverse()
    p = np.array(path)
    return p[:, 0], p[:, 1], float(D[n, m] / len(path))


def mapping(ci, rj, dt):
    """Monotone cand-time → ref-time function from a DTW path (median ref frame per cand frame)."""
    n = ci.max() + 1
    ref = np.zeros(n)
    for i in range(n):
        ref[i] = np.median(rj[ci == i])
    ref = np.maximum.accumulate(ref)
    return lambda t: np.interp(np.asarray(t) / dt, np.arange(n), ref) * dt


if __name__ == "__main__":
    a = sys.argv[1:]
    ref, cand = a[0], a[1]
    band = float(a[a.index("--band") + 1]) if "--band" in a else 15.0
    frame = float(a[a.index("--frame") + 1]) if "--frame" in a else 0.2
    A, dt = feats(cand, frame)
    B, _ = feats(ref, frame)
    ci, rj, avg = dtw(A, B, int(band / dt))
    f = mapping(ci, rj, dt)
    out = {"frame": dt, "mean_cost": round(avg, 4), "path_cost_note": "1 − cosine per step; lower is better"}
    if "--tab" in a:
        import tabtime as T
        off = float(a[a.index("--offset") + 1]) if "--offset" in a else 0.0
        tl = T.timeline(a[a.index("--tab") + 1])
        starts = [m["start"] + off for m in tl]
        real = f(starts)
        out["measures"] = [{"m": m["m"], "tab": round(s, 3), "real": round(float(r), 3), "bpm": m["bpm"], "sig": m["sig"]}
                           for m, s, r in zip(tl, starts, real)]
        segs, cur = [], None
        for k, m in enumerate(tl):
            if cur is None or m["bpm"] != cur["bpm"]:
                cur = {"from": m["m"], "bpm": m["bpm"], "idx": []}; segs.append(cur)
            cur["idx"].append(k)
        fits = []
        for s in segs:
            idx = s["idx"]
            if len(idx) < 3:
                continue
            beats = np.concatenate([[0], np.cumsum([tl[k]["beats"] for k in idx[:-1]])])
            r = np.array([real[k] for k in idx])
            xb = beats - beats.mean()
            slope = float((xb * (r - r.mean())).sum() / ((xb ** 2).sum() + 1e-12))   # closed-form least squares
            fits.append({"from": s["from"], "to": tl[idx[-1]]["m"], "tab_bpm": s["bpm"], "real_bpm": round(60 / slope, 2) if slope > 0 else None,
                         "start_shift": round(float(r[0] - starts[idx[0]]), 3)})
        out["segments"] = fits
    text = json.dumps(out, indent=1)
    if "-o" in a:
        open(a[a.index("-o") + 1], "w").write(text)
    print(json.dumps({k: v for k, v in out.items() if k != "measures"}, indent=1))
