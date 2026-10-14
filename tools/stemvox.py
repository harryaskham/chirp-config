#!/usr/bin/env python3
"""Vocal stem → rhythmic syllable notation (for harsh/shouted vocals, where the rhythm and dynamics matter and
the pitch is noise): syllables are runs of vocal-band energy above a floor, split at internal dips, quantised to
a grid on the tab's own measure timeline (so odd-length bars stay exact), with velocity from loudness.

  stemvox.py STEM --tab DIR --d0 SECONDS --bars B0-B1 [--note Eb3|auto] [--grid 0.125] [--range 30] [--dip 6] [--min 0.25]

  --note   one pitch for every syllable, or `auto`: each syllable's pitch from the stem (harmonic summation,
           G3..F5; a shout's pitch moves from phrase to phrase)
  --range  dB below the passage's loudest frame that still counts as voice (default 30)
  --dip    a fall of this many dB inside a run, then a rise, starts a new syllable (default 6)
  --min    shortest syllable in beats after quantising (default 0.25)
Prints one line per bar: `bar N  tokens` (R for rests), like stemnotes.py."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402
import tabtime as T  # noqa: E402

SR = 48000


def band_env(x, hop=0.005, win=0.02, lo=250, hi=5000):
    n, h = int(win * SR), int(hop * SR)
    f = np.fft.rfftfreq(n, 1 / SR); sel = (f >= lo) & (f < hi); w = np.hanning(n)
    out = [10 * np.log10((np.abs(np.fft.rfft(x[i:i + n] * w))[sel] ** 2).sum() + 1e-12) for i in range(0, len(x) - n, h)]
    e = np.array(out)
    k = 3
    return np.convolve(e, np.ones(k) / k, "same"), hop


def syllables(env, hop, rng, dip):
    top = np.percentile(env, 99.5); on = env > top - rng
    segs, i = [], 0
    while i < len(env):
        if not on[i]:
            i += 1; continue
        j = i
        while j < len(env) and on[j]:
            j += 1
        # split [i, j) at dips: local minimum ≥ dip below the running peak, followed by a rise of ≥ dip
        start, peak = i, env[i]
        k = i + 1
        while k < j - 1:
            peak = max(peak, env[k])
            if env[k] < peak - dip and env[k] <= env[k - 1] and env[k] <= env[k + 1]:
                nxt = env[k:j].max() if k < j else env[k]
                if nxt > env[k] + dip:
                    segs.append((start, k, peak)); start, peak = k, env[k]
            k += 1
        segs.append((start, j, max(peak, env[start:j].max())))
        i = j
    return [(a * hop, b * hop, p - top) for a, b, p in segs]


def syllable_pitch(x, a, b, lo=55, hi=77, default="A4"):
    """Pitch of one syllable (MIDI lo..hi): harmonic summation over 5 harmonics of the segment's spectrum.
    Shouted vocals are noisy but strongly pitched; the estimate is the most salient harmonic series."""
    seg = x[int(a * SR):int(b * SR)]
    if len(seg) < int(0.04 * SR):
        return default
    n = 1 << int(np.ceil(np.log2(max(len(seg), 8192))))
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    f = np.fft.rfftfreq(n, 1 / SR)
    mag = np.log1p(spec / (spec.max() + 1e-12) * 1000)
    best, bm = -1.0, None
    for m in range(lo, hi + 1):
        f0 = 440 * 2 ** ((m - 69) / 12)
        s = sum(mag[min(len(mag) - 1, int(round(h * f0 * n / SR)))] / h for h in range(1, 6))
        if s > best:
            best, bm = s, m
    names = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    return f"{names[bm % 12]}{bm // 12 - 1}"


def main():
    a = sys.argv[1:]
    stem = a[0]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    tab, d0 = opt("--tab", None), float(opt("--d0", "0"))
    b0, b1 = (int(v) for v in opt("--bars", "1-1").split("-"))
    note, grid = opt("--note", "Eb3"), float(opt("--grid", "0.125"))
    rng, dip, mn = float(opt("--range", "30")), float(opt("--dip", "6")), float(opt("--min", "0.25"))
    tl = T.timeline(tab)
    t_start = d0 + tl[b0 - 1]["start"]
    last = tl[b1 - 1]; t_end = d0 + last["start"] + last["beats"] * 60 / last["bpm"]
    x = L.load(stem).mean(1)[int(t_start * SR):int(t_end * SR)]
    env, hop = band_env(x)
    segs = syllables(env, hop, rng, dip)
    # time → (bar, beat-in-bar) on the tab timeline, quantised
    bars = {m: [] for m in range(b0, b1 + 1)}
    for s, e, lvl in segs:
        ts, te = t_start + s, t_start + e
        for m in range(b0, b1 + 1):
            ms = d0 + tl[m - 1]["start"]; spb = 60 / tl[m - 1]["bpm"]; me = ms + tl[m - 1]["beats"] * spb
            if ms <= ts < me:
                qs = round((ts - ms) / spb / grid) * grid
                ql = max(mn, round((te - ts) / spb / grid) * grid)
                vel = int(np.clip(120 + 3 * lvl, 50, 124))
                pitch = syllable_pitch(x, s, e) if note == "auto" else note
                bars[m].append([qs, ql, vel, pitch])
                break
    for m in range(b0, b1 + 1):
        nb = tl[m - 1]["beats"]; ev = sorted(bars[m]); toks, pos = [], 0.0
        for qs, ql, vel, pitch in ev:
            if qs < pos - 1e-9 or qs >= nb:
                continue
            if qs > pos + 1e-9:
                toks.append(f"R/{qs - pos:g}b")
            ql = min(ql, nb - qs)
            toks.append(f"{pitch}/{ql:g}b@{vel}"); pos = qs + ql
        if pos < nb - 1e-9:
            toks.append(f"R/{nb - pos:g}b")
        print(f"bar {m:3d}  {' '.join(toks)}")


if __name__ == "__main__":
    main()
