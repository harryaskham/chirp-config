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
(+10 ms 71.89 -> 72.03, +0.14 held-out). Always scan both directions in 5 ms steps."""
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


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
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
