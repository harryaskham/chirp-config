#!/usr/bin/env python3
"""Consonant transcription from a vocal stem: for every sung note of a song track, classify the onset just before
the vowel and the coda at the note's end from the reference vocal, and write chirp's voice-layer consonant codes
as per-note articulations (`^on=N`, `^off=N`; bind them in the patch: `onset: expr.on`, `coda: expr.off`).
Measured from audio — no lyric text — so a synthesised singer starts and ends syllables the way the singer did.

  stemconsonants.py VOCALS.wav SONG.yaml TRACK OUT.json [--key vox] [--codas]

Onset window: the 90 ms before the note to 20 ms after; reference: the vowel 60-160 ms in. Classes (codes from the
voice layer): unvoiced hiss with a high centroid → s 11 (sh 13 when the hiss centres at 2.5-4.5 kHz), weaker
broadband hiss → f 7, breathy noise in the formant range → h 15, a short broadband burst after near-silence →
t 3 (k 5 when the burst centres at 1.2-3 kHz, p 1 below), a voiced low murmur well below the vowel's brightness →
m 16; otherwise a vowel onset (0). Codas use the same tests on the 120 ms after the note's vowel (n 17 for the
murmur). Existing articulations (e.g. ^vow from stemvowels.py) are kept."""
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stemvowels as V  # noqa: E402
import drumtrans as D  # noqa: E402
import likeness as L  # noqa: E402

SR = 48000


def feats(x):
    """level (dB), share of energy above 3.5 kHz, spectral centroid (Hz), voicing (0..1)"""
    if len(x) < 256:
        return -120.0, 0.0, 0.0, 0.0
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / SR)
    tot = sp.sum() + 1e-12
    lvl = 10 * np.log10(np.mean(x ** 2) + 1e-12)
    hf = sp[f > 3500].sum() / tot
    cen = float((f * sp).sum() / tot)
    y = x - x.mean()
    ac = np.correlate(y, y, "full")[len(y) - 1:]
    lo, hi = int(SR / 420), int(SR / 70)
    voi = float(ac[lo:hi].max() / (ac[0] + 1e-12)) if hi < len(ac) else 0.0
    return lvl, hf, cen, voi


def classify(pre, vowel, before, coda=False):
    lp, hf, cen, voi = feats(pre)
    lv, hfv, cenv, _ = feats(vowel)
    lb = feats(before)[0]
    rel = lp - lv
    if rel < -30:
        return 0
    if voi < 0.45 and hf > 0.45 and rel > -22:
        return 13 if 2500 <= cen <= 4500 else 11          # sh / s
    if voi < 0.45 and hf > 0.25 and rel > -26:
        return 7                                           # f
    if voi < 0.4 and 0.08 < hf <= 0.25 and 900 < cen < 3500 and rel > -20:
        return 15                                          # h
    if not coda and lb - lv < -32 and rel > -18 and voi < 0.5:
        return 5 if 1200 <= cen <= 3000 else (1 if cen < 1200 else 3)    # k / p / t
    if voi > 0.6 and cen < 0.6 * max(cenv, 1.0) and -16 < rel < -2:
        return 17 if coda else 16                          # n / m
    return 0


def run(stem, song, track, key="vox", codas=False):
    x = L.load(stem).mean(1)
    pts = D.tempo_points(song)
    beats = np.array([b for b, _ in pts]); bpm = np.array([v for _, v in pts])
    secs = np.concatenate([[0.0], np.cumsum(np.diff(beats) * 60 / bpm[:-1])])

    def b2t(b):
        i = max(0, np.searchsorted(beats, b, side="right") - 1)
        return secs[i] + (b - beats[i]) * 60 / bpm[i]

    seg = lambda a, b: x[max(0, int(a * SR)):max(0, int(b * SR))]
    toks, out, pos, counts = V.track_tokens(song, track), [], 0.0, {}
    for t in toks:
        m = re.match(r"^([^/]+)/([0-9.]+)b(.*)$", t)
        if not m:
            out.append(t); continue
        body, ln, rest = m.group(1), float(m.group(2)), m.group(3)
        if body in ("R", "r", "_"):
            out.append(t); pos += ln; continue
        a, e = b2t(pos), b2t(pos + ln)
        on = classify(seg(a - 0.09, a + 0.02), seg(a + 0.06, a + 0.16), seg(a - 0.16, a - 0.09))
        rest = re.sub(r"\^on=\d+|\^off=\d+", "", rest)
        if on:
            rest += f"^on={on}"
        counts[on] = counts.get(on, 0) + 1
        if codas and e - a > 0.2:
            off = classify(seg(e - 0.02, e + 0.10), seg(e - 0.16, e - 0.06), seg(e - 0.3, e - 0.2), coda=True)
            if off:
                rest += f"^off={off}"
        out.append(f"{body}/{m.group(2)}b{rest}")
        pos += ln
    return {key: {"score": " ".join(out)}}, counts


if __name__ == "__main__":
    a = sys.argv[1:]
    key = a[a.index("--key") + 1] if "--key" in a else "vox"
    res, counts = run(a[0], a[1], a[2], key, "--codas" in a)
    json.dump(res, open(a[3], "w"))
    names = {0: "-", 1: "p", 3: "t", 5: "k", 7: "f", 11: "s", 13: "sh", 15: "h", 16: "m"}
    print("onsets: " + ", ".join(f"{names.get(k, k)} {v}" for k, v in sorted(counts.items())))
