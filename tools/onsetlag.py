#!/usr/bin/env python3
"""Global onset lag of a render against the record, and a uniform shift for songs without a map.
  onsetlag.py OURS.wav REF.wav [--win 4] [--step 8] [--max 250]       windowed lags (ms) + their median
  onsetlag.py OURS.wav REF.wav --shift SONG.yaml -o OUT.yaml [--ms M]  prepend a rest of M ms (default: -median)
                                                                      to every track's score
Each window cross-correlates likeness-style onset envelopes (10 ms hop) over ±--max ms; a negative lag means
ours is EARLY. A consistent lag across windows (with near-zero correlation at lag 0) is a setup error: stemsong
/drumtrans setups take the beat phase from an onset-envelope comb, which can sit a few tens of ms early of the
perceived onsets. Playing God v3 -> v4: ours 25 ms early everywhere; +25 ms on all tracks 49.81 -> 52.01 (rhythm
up in every section, the intro 29 -> 82). Lags near ±half a beat in single windows are aliases — trust the median.
Map-built songs shift with the map's `offset` instead (then regenerate with tab2song.py); try ±10 ms around the
median, the rhythm term is sharp. On live/room recordings with smeared onsets the SIGN can mislead: Daydreaming
measured +10 ms (ours late), yet shifting earlier lost steadily (-5/-10/-15 ms: 71.68/71.26/70.85) and later won
(+10 ms 71.89 -> 72.03, +0.14 held-out). Always scan both directions in 5 ms steps.
  onsetlag.py OURS.wav REF.wav --chroma --sections F [--max 1.0]   per-section CHROMA lag (chirper-zero's scan)
Chroma mode compares 0.5 s chroma windows of ours, shifted up to ±--max s, with the record's, per section. A section
that peaks cleanly off zero while the others peak at 0 has PARTS a beat off (Raining Blood v29: the rhythm guitar
and bass one beat early in one section after a DTW/grid fit, the retimed drums right; +0.31..+0.38 on all seeds).
Then solo-scan the parts against their stems and delay only that section's beats in those parts."""
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402


def env(x):
    m = x.mean(1); hop = 480; n = len(m) // hop
    fr = m[:n * hop].reshape(n, hop); e = np.log(np.sqrt((fr ** 2).mean(1)) + 1e-6)
    return np.maximum(np.diff(e, prepend=e[0]), 0)


def chroma_scan(ours, ref, sections, mx):
    F = {k: L.Feat(L.load(p)) for k, p in (("o", ours), ("r", ref))}
    fps, w = L.FPS, max(1, int(round(L.FPS / 2)))
    co, cr = F["o"].chroma, F["r"].chroma
    n = min(co.shape[1], cr.shape[1])
    cuts = [float(v) for v in open(sections).read().replace("\n", ",").split(",") if v.strip()]
    M = int(round(mx * fps))
    print(f"section   start    end   best lag (ms)   sim@0  sim@best   (negative = ours early)")
    for i in range(len(cuts) - 1):
        a, b = int(cuts[i] * fps), min(int(cuts[i + 1] * fps), n)
        starts = list(range(a + M, b - M - w, w))
        if len(starts) < 2:
            continue
        def sim(g):
            s = []
            for k in starts:
                x, y = cr[:, k:k + w].mean(1), co[:, k + g:k + g + w].mean(1)
                s.append(float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-9)))
            return float(np.mean(s))
        res = [(sim(g), g) for g in range(-M, M + 1)]
        best = max(res); zero = [r for r in res if r[1] == 0][0]
        flag = "  <- off zero" if best[1] != 0 and best[0] - zero[0] > 0.01 else ""
        print(f"{i + 1:7d} {cuts[i]:7.1f} {cuts[i + 1]:6.1f} {best[1] / fps * 1000:+12.0f}   {zero[0]:.3f}    {best[0]:.3f}{flag}")


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    if "--chroma" in a:
        return chroma_scan(a[0], a[1], opt("--sections", ""), opt("--max", 1.0))
    win, step, mx = opt("--win", 4.0), opt("--step", 8.0), opt("--max", 250)
    r, o = env(L.load(a[1])), env(L.load(a[0]))
    n = min(len(r), len(o)); M = mx // 10; lags = []
    t = 0.0
    while (t + win) * 100 + M < n:
        i0, i1 = int(t * 100), int((t + win) * 100); rr = r[i0:i1] - r[i0:i1].mean(); best = (-1.0, 0)
        if np.linalg.norm(rr) > 0:
            for g in range(-M, M + 1):
                if i0 + g < 0:
                    continue
                oo = o[i0 + g:i1 + g]; oo = oo - oo.mean()
                c = float(np.dot(rr, oo) / (np.linalg.norm(rr) * np.linalg.norm(oo) + 1e-9))
                if c > best[0]:
                    best = (c, g)
            if best[0] > 0.1:
                lags.append(best[1] * 10)
            print(f"{t:6.1f}-{t + win:.1f}s lag {best[1] * 10:+5d} ms corr {best[0]:.2f}")
        t += step
    med = float(np.median(lags)) if lags else 0.0
    print(f"median lag {med:+.0f} ms over {len(lags)} windows (corr > 0.1); negative = ours early")
    if "--shift" in a:
        ms = opt("--ms", -med)
        src = open(a[a.index("--shift") + 1]).read()
        bpm = float(re.search(r"^tempo:\s*([0-9.]+)", src, re.M).group(1))
        if re.search(r"^tempo:\s*\[", src, re.M) or "tempo_map" in src:
            sys.exit("tempo map: shift by hand (the first tempo segment's bpm applies to the prepended rest)")
        d = round(ms / 1000 * bpm / 60, 4)
        if d <= 0:
            sys.exit(f"shift {ms:+.0f} ms is not a delay; trim the leading rests by hand")
        out, k = re.subn(r'(\{name: "[^"]+", patch: [^\n]*?score: ")', lambda m: m.group(1) + f"R/{d}b ", src)
        open(opt("-o", ""), "w").write(out)
        print(f"shifted {k} tracks by {ms:+.0f} ms ({d} beats at {bpm} BPM) -> {opt('-o', '')}")


if __name__ == "__main__":
    main()
