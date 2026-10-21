#!/usr/bin/env python3
"""noteacc: are the notes and the timing right, moment by moment? (opt-in, beside likeness; Harry 2026-10-20)

likeness scores each section through distributions (a section's chroma histogram, 4 s rhythm statistics). It
punishes a whole song in the wrong key or late (Xtal v3: a semitone -16.5, 100 ms late -9.7) but barely notices
local errors a listener hears at once (20% of notes a semitone off -3.2, 20% of onsets +-60 ms -2.1). noteacc
compares the two recordings frame by frame on the shared timeline, with no lag search (timing counts):

  pitch   chroma of the harmonic part (median-filter HPSS, 100 Hz-5 kHz, 50 ms hop, 200 ms smoothing, semitones
          soft-assigned so detuning counts), cosine per frame where both recordings are tonal, rescaled against
          chance (the candidate slid along itself): a song that is merely in the right key scores about 0, the
          same notes at the same times 100.
  timing  onsets (log spectral flux in low, mid and high bands, 10 ms hop) matched one-to-one within +-50 ms;
          F-measure per band weighted by the reference's onsets, rescaled against chance the same way.

It also reports the median signed onset offset (systematic lateness), the worst windows (where to listen and
fix) and, given section bounds, per-section values. Nothing here changes the default metric or any ledger.

usage: noteacc.py REF CAND [b0,b1,...] [--window S] [--worst N] [--json]
"""
import json
import os
import sys

import numpy as np
from scipy import ndimage, signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from likeness import SR, load  # noqa: E402  (same decoding and resampling as the metric)

C_N, C_HOP = 16384, 2400        # chroma: 2.9 Hz bins (semitones separate from ~100 Hz), 50 ms hop
C_LO, C_HI = 100.0, 5000.0
SMOOTH = 4                      # chroma frames averaged (200 ms)
TONAL_DB = 35.0                 # a frame is tonal within this many dB of its recording's 95th percentile
O_N, O_HOP = 1024, 480          # onsets: 21 ms window, 10 ms hop
O_BANDS = ((30, 200), (200, 2000), (2000, 12000))
O_DELTA = 0.4                   # peak threshold above the 1 s moving median of the normalised flux
O_GAP = 0.06                    # at most one onset per band per 60 ms
TOL = 0.05                      # onset match tolerance (s), the MIR convention
SHIFTS = (0.137, 0.213, 0.291, 0.377, 0.459, 0.541, 0.619, 0.703, 0.787, 0.863)   # chance: fractions of length


def chroma(x):
    """(12 x frames unit chroma of the harmonic part, frames tonal energy in dB)."""
    f, _, Z = signal.stft(x, SR, nperseg=C_N, noverlap=C_N - C_HOP, boundary=None, padded=False)
    sel = (f >= C_LO) & (f <= C_HI)
    f, m = f[sel], np.abs(Z[sel]).astype(np.float32)
    h = ndimage.median_filter(m, size=(1, 17))    # sustained along time: harmonic
    p = ndimage.median_filter(m, size=(17, 1))    # broadband along frequency: percussive
    mh = m * (h ** 2 / (h ** 2 + p ** 2 + 1e-12))
    midi = 12 * np.log2(f / 440.0) + 69
    lo = np.floor(midi).astype(int)
    frac = (midi - lo).astype(np.float32)
    W = np.zeros((12, len(f)), np.float32)
    np.add.at(W, (lo % 12, np.arange(len(f))), 1 - frac)
    np.add.at(W, ((lo + 1) % 12, np.arange(len(f))), frac)
    ch = ndimage.uniform_filter1d(W @ mh, SMOOTH, axis=1)
    e = ndimage.uniform_filter1d(10 * np.log10((mh.astype(np.float64) ** 2).sum(0) + 1e-12), SMOOTH)
    return ch / (np.linalg.norm(ch, axis=0) + 1e-12), e


def flux(x):
    """bands x frames positive log-magnitude flux (chunked: long songs stay small in memory)."""
    n = 1 + (len(x) - O_N) // O_HOP if len(x) >= O_N else 0
    out = np.zeros((len(O_BANDS), n), np.float32)
    if n == 0:
        return out
    f = np.fft.rfftfreq(O_N, 1 / SR)
    masks = [(f >= a) & (f < b) for a, b in O_BANDS]
    win = signal.get_window("hann", O_N).astype(np.float32)
    view = np.lib.stride_tricks.sliding_window_view(x, O_N)
    prev = None
    for s in range(0, n, 4096):
        idx = np.arange(s, min(n, s + 4096))
        L = np.log1p(1000 * np.abs(np.fft.rfft(view[idx * O_HOP] * win, axis=1)))
        first = L[:1] if prev is None else prev
        d = np.maximum(np.diff(np.concatenate([first, L]), axis=0), 0)
        for i, m in enumerate(masks):
            out[i, idx] = d[:, m].sum(1)
        prev = L[-1:]
    return out


def onsets(env):
    """Onset times (s) of one band's flux; level-free (normalised by its own 99.5th percentile)."""
    top = np.percentile(env, 99.5) if env.size else 0.0
    if top <= 0:
        return np.zeros(0)
    e = env / top
    thr = ndimage.median_filter(e, size=int(SR / O_HOP)) + O_DELTA
    pk, _ = signal.find_peaks(e, height=thr, distance=max(1, int(O_GAP * SR / O_HOP)))
    return pk * O_HOP / SR + O_N / (2 * SR)


def match(r, c):
    """One-to-one matches within TOL, nearest first → (n_matched, signed offsets c - r)."""
    if not len(r) or not len(c):
        return 0, np.zeros(0)
    pairs = []
    for i, t in enumerate(r):
        a, b = np.searchsorted(c, t - TOL), np.searchsorted(c, t + TOL, side="right")
        pairs += [(abs(c[j] - t), i, j) for j in range(a, b)]
    pairs.sort()
    ur, uc, offs = set(), set(), []
    for d, i, j in pairs:
        if i not in ur and j not in uc:
            ur.add(i), uc.add(j), offs.append(c[j] - r[i])
    return len(offs), np.array(offs)


def _f(nm, nr, nc):
    return 2 * nm / (nr + nc) if nr + nc else np.nan


class Pair:
    """Both recordings' features on the reference's timeline [t0, t1) (a short candidate is padded with silence:
    what the listener hears)."""

    def __init__(self, rs, cs, t0=0.0, t1=None):
        t1 = len(rs) / SR if t1 is None else t1
        a, b = int(t0 * SR), int(t1 * SR)
        rs, cs = rs[a:b], cs[a:b]
        if len(cs) < len(rs):
            cs = np.concatenate([cs, np.zeros((len(rs) - len(cs), 2), cs.dtype)])
        self.t0, self.dur = t0, len(rs) / SR
        xr, xc = rs.mean(1).astype(np.float32), cs.mean(1).astype(np.float32)
        self.cr, self.er = chroma(xr)
        self.cc, self.ec = chroma(xc)
        n = min(self.cr.shape[1], self.cc.shape[1])
        self.cr, self.er, self.cc, self.ec = self.cr[:, :n], self.er[:n], self.cc[:, :n], self.ec[:n]
        self.tr = self.er > np.percentile(self.er, 95) - TONAL_DB
        top_c = np.percentile(self.ec, 95)
        self.tc = (self.ec > top_c - TONAL_DB) & (self.ec > -100)
        self.ctime = (np.arange(n) * C_HOP + C_N / 2) / SR
        self.cos = (self.cr * self.cc).sum(0)
        fr, fc = flux(xr), flux(xc)
        self.or_ = [onsets(e) for e in fr]
        self.oc = [onsets(e) for e in fc]
        self.pchance = self._pitch_chance()
        self.tchance = self._timing_chance()

    def _pitch_chance(self):
        n, vals = len(self.cos), []
        for s in SHIFTS:
            k = int(s * n)
            cc, tc = np.roll(self.cc, k, axis=1), np.roll(self.tc, k)
            both = self.tr & tc
            if both.sum() >= 10:
                vals.append(float((self.cr[:, both] * cc[:, both]).sum(0).mean()))
        return float(np.mean(vals)) if vals else np.nan

    def _timing_chance(self):
        vals = []
        for s in SHIFTS:
            nm = nr = nc = 0
            for r, c in zip(self.or_, self.oc):
                cs = np.sort((c + s * self.dur) % self.dur)
                m, _ = match(r, cs)
                nm, nr, nc = nm + m, nr + len(r), nc + len(c)
            vals.append(_f(nm, nr, nc))
        return float(np.nanmean(vals)) if vals else np.nan

    def pitch(self, a=None, b=None):
        sel = self.tr & self.tc
        if a is not None:
            sel = sel & (self.ctime >= a - self.t0) & (self.ctime < b - self.t0)
        span = np.ones_like(sel) if a is None else (self.ctime >= a - self.t0) & (self.ctime < b - self.t0)
        ref_tonal = (self.tr & span).sum()
        if sel.sum() < 10:
            return {"score": None, "frames": int(sel.sum()), "ref_tonal_frames": int(ref_tonal)}
        cos = float(self.cos[sel].mean())
        ch = self.pchance
        return {"score": round(100 * (cos - ch) / (1 - ch), 2), "cos": round(cos, 4), "chance": round(ch, 4),
                "frames": int(sel.sum()), "ref_tonal_frames": int(ref_tonal),
                "ref_only": round(float((self.tr & ~self.tc & span).sum() / max(1, ref_tonal)), 3),
                "cand_only": round(float((self.tc & ~self.tr & span).sum() / max(1, (self.tc & span).sum())), 3)}

    def timing(self, a=None, b=None):
        nm = nr = nc = 0
        offs, bands = [], []
        for (lo, hi), r, c in zip(O_BANDS, self.or_, self.oc):
            if a is not None:
                r = r[(r >= a - self.t0) & (r < b - self.t0)]
                c = c[(c >= a - self.t0 - TOL) & (c < b - self.t0 + TOL)]
            m, o = match(r, c)
            nm, nr, nc = nm + m, nr + len(r), nc + len(c)
            offs.append(o)
            bands.append({"band": f"{lo}-{hi} Hz", "ref_onsets": len(r), "cand_onsets": len(c),
                          "f": None if np.isnan(_f(m, len(r), len(c))) else round(_f(m, len(r), len(c)), 4)})
        if nr < 4:
            return {"score": None, "ref_onsets": nr, "bands": bands}
        f, ch = _f(nm, nr, nc), self.tchance
        o = np.concatenate(offs)
        return {"score": round(100 * (f - ch) / (1 - ch), 2), "f": round(f, 4), "chance": round(ch, 4),
                "ref_onsets": nr, "cand_onsets": nc, "matched": nm,
                "offset_ms_median": round(1000 * float(np.median(o)), 1) if len(o) else None,
                "offset_ms_mad": round(1000 * float(np.median(np.abs(o - np.median(o)))), 1) if len(o) else None,
                "bands": bands}


def _combined(p, t):
    v = [x for x in (p.get("score"), t.get("score")) if x is not None]
    return round(sum(v) / len(v), 2) if v else None


def measure(ref, cand, bounds=None, window=8.0, worst=8):
    """→ {"accuracy", "pitch", "timing", "worst": [...], "sections": [...]} (scores ~0 = chance, 100 = identical)."""
    t0, t1 = (bounds[0], bounds[-1]) if bounds else (0.0, None)
    cs = load(cand)
    cand_s = len(cs) / SR
    P = Pair(load(ref), cs, t0, t1)
    p, t = P.pitch(), P.timing()
    out = {"accuracy": _combined(p, t), "pitch": p, "timing": t,
           "span": [round(t0, 3), round(t0 + P.dur, 3)], "candidate_seconds": round(cand_s, 3),
           "convention": "noteacc v1: chance-rescaled frame chroma cosine (harmonic, 50 ms) and onset F (+-50 ms); "
                         "shared timeline, no lag search; a short candidate is padded with silence"}
    wins = []
    s = t0
    while s + window / 2 < t0 + P.dur:
        e = min(s + window, t0 + P.dur)
        wp, wt = P.pitch(s, e), P.timing(s, e)
        c = _combined(wp, wt)
        if c is not None:
            wins.append({"start": round(s, 2), "end": round(e, 2), "accuracy": c, "pitch": wp.get("score"),
                         "timing": wt.get("score"), "offset_ms": wt.get("offset_ms_median")})
        s += window / 2
    out["worst"] = sorted(wins, key=lambda w: w["accuracy"])[:worst]
    if bounds:
        secs = []
        for a, b in zip(bounds[:-1], bounds[1:]):
            sp, st = P.pitch(a, b), P.timing(a, b)
            secs.append({"start": a, "end": b, "accuracy": _combined(sp, st), "pitch": sp.get("score"),
                         "timing": st.get("score"), "offset_ms": st.get("offset_ms_median")})
        out["sections"] = secs
    return out


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    opts = dict(zip(argv, argv[1:]))
    if len(args) < 2:
        raise SystemExit(__doc__.strip().splitlines()[-1])
    bounds = [float(v) for v in args[2].split(",")] if len(args) > 2 else None
    res = measure(args[0], args[1], bounds, float(opts.get("--window", 8.0)), int(opts.get("--worst", 8)))
    if "--json" in argv:
        print(json.dumps(res))
        return
    p, t = res["pitch"], res["timing"]
    print(f"accuracy {res['accuracy']}   pitch {p.get('score')} (cos {p.get('cos')} vs chance {p.get('chance')}; "
          f"ref-only tonal {p.get('ref_only')}, cand-only {p.get('cand_only')})   timing {t.get('score')} "
          f"(F {t.get('f')} vs chance {t.get('chance')}; median offset {t.get('offset_ms_median')} ms)")
    for b in t.get("bands", []):
        print(f"  onsets {b['band']:>14}: ref {b['ref_onsets']:5d} cand {b['cand_onsets']:5d} F {b['f']}")
    if res.get("sections"):
        print("sections:")
        for s in res["sections"]:
            print(f"  {s['start']:8.2f}-{s['end']:8.2f} s  accuracy {s['accuracy']}  pitch {s['pitch']}  "
                  f"timing {s['timing']}  offset {s['offset_ms']} ms")
    print("worst windows (listen here first):")
    for w in res["worst"]:
        print(f"  {w['start']:8.2f}-{w['end']:8.2f} s  accuracy {w['accuracy']}  pitch {w['pitch']}  "
              f"timing {w['timing']}  offset {w['offset_ms']} ms")


if __name__ == "__main__":
    main(sys.argv[1:])
