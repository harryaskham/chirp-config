#!/usr/bin/env python3
"""voxtrans: a monophonic VOCAL stem -> notes [{at, len, pitch, vel}] JSON (chirper-zero's Human r4, promoted from
/tmp/lt/voxtrans.py; evidence ref/evidence/chirper-zero/hu-r4).

  voxtrans.py STEM.wav OUT.json [--from S] [--to S] [--lo 80] [--hi 420] [--floor 24] [--prom 2.0] [--method shs|yin]
                                [--conf 0.2] [--split 0.75] [--minlen 0.09]

Why: YIN on Hetfield's S&M vocal reads his 2nd/3rd harmonics (a strong ~930 Hz formant), and the old stem
transcriptions predated tools/livestems.py (the crowd sat in the vocal stem) and were sparse (Human: 128 notes,
36 s voiced, ~4 notes in verse 1). Subharmonic summation gives a sane line: Human's new line won +0.28 on top of a
refit from 97 s on (chroma +4..+12 per section) but lost in verse 1, so A/B per section.
How: the stem band-passed 70-1500 Hz and downsampled 4x; 40 ms frames every 10 ms; a frame is voiced when its level
is within --floor dB of the passage's loud level (95th percentile) and (shs) its best f0 candidate (--lo..--hi in
1/8 semitones; 8 harmonics weighted 0.84^h on a 60 ms zero-padded FFT magnitude^0.5) beats the median candidate by
--prom, or (yin) its YIN dip is under --conf. Pitch is median-smoothed over 5 frames; a note is a voiced run, split
where the smoothed pitch leaves the run's median by > --split semitones for 60 ms; notes under --minlen are dropped;
pitch = the run's median (rounded MIDI), vel from its level (0.35..1). Frames under -100 dBFS are never voiced
(the /tmp original turned digital silence into one long note at --lo).
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000


def f0_track(x, t0=0.0, t1=1e9, lo=80.0, hi=420.0, floor=24.0, prom=2.0, method="shs", conf=0.2):
    """(f0 Hz per 10 ms frame (nan unvoiced), level dB per frame, the loud level) for mono X at SR."""
    from scipy.signal import butter, resample_poly, sosfilt
    x = sosfilt(butter(4, [70, 1500], btype="band", fs=SR, output="sos"), x)
    ds = 4
    y = resample_poly(x, 1, ds)
    sr = SR // ds
    hop, win = int(0.01 * sr), int(0.04 * sr)
    tmax, tmin = int(sr / lo) + 1, int(sr / hi)
    i0, i1 = int(t0 * sr), min(len(y) - win - tmax, int(t1 * sr))
    fr = range(i0, i1, hop)
    lev = np.array([10 * np.log10(np.mean(y[i:i + win] ** 2) + 1e-20) for i in fr])
    if not len(lev):
        return np.zeros(0), lev, 0.0
    loud = float(np.percentile(lev, 95))
    f0 = np.full(len(lev), np.nan)
    if method == "yin":
        for k, i in enumerate(fr):
            if lev[k] < loud - floor or lev[k] < -100:
                continue
            seg = y[i:i + win + tmax]
            d = np.array([np.sum((seg[:win] - seg[tau:tau + win]) ** 2) for tau in range(1, tmax + 1)])
            cm = d * np.arange(1, tmax + 1) / (np.cumsum(d) + 1e-20)
            j = None
            for tau in range(tmin - 1, tmax - 1):
                if cm[tau] < conf and cm[tau] <= cm[tau + 1]:
                    j = tau
                    break
            if j is None:
                j = tmin - 1 + int(np.argmin(cm[tmin - 1:]))
                if cm[j] >= conf * 1.5:
                    continue
            f0[k] = sr / (j + 1)
    else:
        nw, nf = int(0.06 * sr), 8192
        hw = np.hanning(nw)
        fq = np.fft.rfftfreq(nf, 1 / sr)
        cands = lo * 2 ** (np.arange(0, int(96 * np.log2(hi / lo)) + 1) / 96)
        wts = 0.84 ** np.arange(8)
        for k, i in enumerate(fr):
            if lev[k] < loud - floor or lev[k] < -100:      # digital silence is never voiced
                continue
            c = i + win // 2 - nw // 2
            if c < 0 or c + nw > len(y):
                continue
            sp = np.sqrt(np.abs(np.fft.rfft(y[c:c + nw] * hw, nf)))
            sc = np.zeros(len(cands))
            for h in range(8):
                sc += wts[h] * np.interp(cands * (h + 1), fq, sp)
            j = int(np.argmax(sc))
            if sc[j] <= 0 or sc[j] < prom * np.median(sc):
                continue
            f0[k] = cands[j]
    return f0, lev, loud


def notes_of(f0, lev, loud, t0=0.0, split=0.75, minlen=0.09):
    with np.errstate(invalid="ignore", divide="ignore"):
        midi = 69 + 12 * np.log2(f0 / 440)
    sm = midi.copy()
    for k in range(len(midi)):
        w = midi[max(0, k - 2):k + 3]
        w = w[~np.isnan(w)]
        sm[k] = np.median(w) if len(w) >= 3 and not np.isnan(midi[k]) else np.nan
    notes, k, n = [], 0, len(sm)
    while k < n:
        if np.isnan(sm[k]):
            k += 1
            continue
        s, vals, out = k, [sm[k]], 0
        k += 1
        while k < n and not np.isnan(sm[k]):
            if abs(sm[k] - np.median(vals)) > split:
                out += 1
                if out >= 6:
                    k -= 5
                    break
            else:
                out = 0
            vals.append(sm[k])
            k += 1
        dur = (k - s) * 0.01
        if dur >= minlen:
            seg = sm[s:k]
            notes.append({"at": round(t0 + s * 0.01, 3), "len": round(dur, 3), "pitch": int(round(np.median(seg[~np.isnan(seg)]))),
                          "vel": round(float(np.clip(1 + (float(np.mean(lev[s:k])) - loud) / 30, 0.35, 1.0)), 3)})
    return notes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stem")
    ap.add_argument("out")
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=1e9)
    ap.add_argument("--lo", type=float, default=80.0)
    ap.add_argument("--hi", type=float, default=420.0)
    ap.add_argument("--floor", type=float, default=24.0)
    ap.add_argument("--prom", type=float, default=2.0)
    ap.add_argument("--method", choices=("shs", "yin"), default="shs")
    ap.add_argument("--conf", type=float, default=0.2)
    ap.add_argument("--split", type=float, default=0.75)
    ap.add_argument("--minlen", type=float, default=0.09)
    a = ap.parse_args(argv)
    x = L.load(a.stem).astype(float)
    x = x.mean(1) if x.ndim > 1 else x
    f0, lev, loud = f0_track(x, a.t0, a.t1, a.lo, a.hi, a.floor, a.prom, a.method, a.conf)
    notes = notes_of(f0, lev, loud, a.t0, a.split, a.minlen)
    with open(a.out, "w") as f:
        json.dump(notes, f)
    ps = [n["pitch"] for n in notes]
    print(len(notes), "notes", "pitch", min(ps) if ps else None, max(ps) if ps else None,
          "median", float(np.median(ps)) if ps else None)


if __name__ == "__main__":
    main()
