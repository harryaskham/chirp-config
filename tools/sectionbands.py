#!/usr/bin/env python3
"""Per-section octave-band balance vs the reference — where a section's TONE is off by more than a master EQ can fix.
  sectionbands.py REF.wav RENDER.wav SECTIONS.txt [--flag 6] [--solo SOLO.wav]

Prints, per section, ours minus the record in octave bands 31 Hz-8 kHz (level-normalised by the median band, dB),
marking |d| >= --flag. sectioneq.py clamps at +-9 dB and couples to the whole mix; a section several bands off by
6-13 dB usually means a PART is wrong there (too bright, missing a register, an extra layer) — fix it at the source
with a part filter or level driven by a track lane over that section (Saturnine v17: the intro's muted piano was
+5..+13 dB too bright at 500 Hz-4 kHz; a lowpass at 400 Hz only before 22 s gave the intro 61.7 -> 67.0).
Only deviations of ~6 dB or more have paid (TNA v18/v22, Saturnine v17); +-3..5 dB lanes lost or tied (TNA r35,
Flim r34) — the 40-band spectral/ltas terms already tolerate them. And not every >= 6 dB gap is EQ-able: Shadows' intro
(+6 dB at 125 Hz, -6..-8 above 2 kHz) lost to every master lane (its tone is the parts' balance, not an EQ).
--solo SOLO.wav adds a line per section with a solo render's bands (relative to the full render) to see which part
carries the excess."""
import sys
import wave

import numpy as np

EDGES = [31, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]


def rd(p):
    with wave.open(p, "rb") as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    x = np.frombuffer(raw, dtype="<i2" if sw == 2 else "<i4").astype(np.float32) / (32768 if sw == 2 else 2147483648)
    return x.reshape(-1, ch).mean(1), sr


def octaves(x, sr, a, b, n=8192):
    s = x[int(a * sr):int(b * sr)]
    if len(s) < n:
        s = np.pad(s, (0, n - len(s)))
    f = np.fft.rfftfreq(n, 1 / sr)
    masks = [(f >= EDGES[k]) & (f < EDGES[k + 1]) for k in range(len(EDGES) - 1)]
    frames = np.lib.stride_tricks.sliding_window_view(s, n)[::n // 2] * np.hanning(n)
    P = (np.abs(np.fft.rfft(frames, axis=1)) ** 2).sum(0)
    return 10 * np.log10(np.array([P[m].sum() for m in masks]) + 1e-12)


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    R, sr = rd(a[0]); O, _ = rd(a[1]); S = rd(opt("--solo", ""))[0] if "--solo" in a else None
    cuts = [float(v) for v in open(a[2]).read().replace("\n", ",").split(",") if v.strip()]
    fl = opt("--flag", 6.0)
    print("sec  start  " + " ".join(f"{e:>6d}" for e in EDGES[:-1]) + f"   ours - record (dB, level-normalised; * |d| >= {fl:g})")
    for i in range(len(cuts) - 1):
        r, o = octaves(R, sr, cuts[i], cuts[i + 1]), octaves(O, sr, cuts[i], cuts[i + 1])
        d = (o - r) - np.median(o - r)
        print(f"{i + 1:3d} {cuts[i]:6.1f}  " + " ".join(f"{v:+5.1f}{'*' if abs(v) >= fl else ' '}" for v in d))
        if S is not None:
            s = octaves(S, sr, cuts[i], cuts[i + 1]) - o
            print("     solo  " + " ".join(f"{v:+6.1f}" for v in s) + "   (solo - full render)")


if __name__ == "__main__":
    main()
