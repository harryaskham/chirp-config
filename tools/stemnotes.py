#!/usr/bin/env python3
"""Transcribe a monophonic low part (bass / riff) from a stem into explicit chirp notation.

  stemnotes.py STEM.wav DOWNBEAT_S BAR_S FIRST_BAR LAST_BAR [--lo MIDI] [--hi MIDI]
  stemnotes.py STEM.wav --map MAP.json FIRST_BAR LAST_BAR [...]   bar starts, lengths and beats from a tab2song
  map's corrected timeline (odd meters, tempo maps, skipped measures) instead of constant 4-beat bars.

Onsets: spectral flux on the stem, peak-picked and quantised to the 16th grid of the given bar grid.
Each note runs to the next onset (or a gap when the stem falls silent); its pitch is the candidate with
the most harmonic energy over the note (harmonic summation), and its octave is chosen by whether the
fundamental itself carries energy (so a B0 with a strong 62 Hz second harmonic isn't read as B1).
Prints one line per bar: `NOTE/<beats>b@vel …` (rests as R), ready to paste into a score."""
import sys, os
import numpy as np
from scipy import signal
sys.path.insert(0, os.path.dirname(__file__))
import likeness as L

NAMES = L.NAMES
ODD = 0.5  # odd/even harmonic energy below this → the note is really an octave up (calibrated on a tab)


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def transcribe(path, d0, bar, b0, b1, lo=23, hi=52, th=0.25, merge=0.6, floor_db=None, spans=None):
    """spans: optional {bar: (start_s, length_s, beats)} (a tab2song map's corrected timeline); otherwise every
    bar is `bar` seconds of 4 beats from d0."""
    x = L.load(path).mean(1)
    F = L.Feat(L.load(path))
    if spans is None:
        spans = {j: (d0 + j * bar, bar, 4.0) for j in range(b0, b1 + 1)}
    on = F.onset / (np.percentile(F.onset, 99) + 1e-9)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(1024) / 1024, "same"))
    loud = 20 * np.log10(rms + 1e-9)
    region = loud[int(spans[b0][0] * 48000):int((spans[b1][0] + spans[b1][1]) * 48000)]
    # 'sounding' floor: default 20th percentile + 6 dB of the region; --floor D uses the 10th percentile + D dB
    # (fades and quiet passages need a low floor or their notes read as rests)
    floor = np.percentile(region, 20) + 6 if floor_db is None else np.percentile(region, 10) + floor_db
    NFFT = 65536
    cands = np.arange(lo, hi + 1)
    hz = 440 * 2 ** ((cands - 69) / 12)
    out = []
    for j in range(b0, b1 + 1):
        t_bar, dur, beats = spans[j]
        NS = int(round(beats * 4))
        s16 = dur / NS
        steps = []
        for k in range(NS):
            t = t_bar + k * s16
            i = int(t * L.FPS)
            o = on[max(0, i - 1):i + 2].max()
            sounding = loud[int((t + s16 / 2) * 48000)] > floor
            steps.append((t, o, sounding))
        # note starts: onset peaks above threshold, plus the bar's first sounding step
        starts = [k for k, (t, o, snd) in enumerate(steps) if snd and (o > th or k == 0)]
        toks = []
        k = 0
        if not starts or starts[0] > 0:
            first = starts[0] if starts else NS
            toks.append(f"R/{first / 4:g}b"); k = first
        for si, st in enumerate(starts):
            end = starts[si + 1] if si + 1 < len(starts) else NS
            # stop at silence
            e = st + 1
            while e < end and steps[e][2]:
                e += 1
            t0, t1 = steps[st][0], steps[min(e, NS - 1)][0] + (s16 if e >= NS else 0)
            seg = x[int((t0 + 0.01) * 48000):int(max(t0 + 0.06, t1 - 0.01) * 48000)]
            P = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), NFFT))
            df = 48000 / NFFT
            def energy(h0, k_):
                b = int(round(h0 * k_ / df)); return P[max(0, b - 2):b + 3].max() if b < len(P) else 0
            scores = [sum(energy(h0, h) / (1 if h > 1 else 1.5) for h in range(1, 9)) for h0 in hz]
            m = cands[int(np.argmax(scores))]
            # octave check (subharmonic error): harmonic summation favours the octave below, which owns all of
            # the true note's harmonics as its even ones; a real low note also has odd harmonics (1, 3, 5)
            h0 = hz[m - lo]
            odd = energy(h0, 1) + energy(h0, 3) + energy(h0, 5)
            even = energy(h0, 2) + energy(h0, 4) + energy(h0, 6)
            if odd < ODD * even and m + 12 <= hi:
                m += 12
            v = int(np.clip(70 + 40 * min(1.0, steps[st][1]), 60, 120))
            # merge a weak re-attack of the same pitch into the previous note (picking noise, not a new note)
            if toks and toks[-1].startswith(nm(m) + "/") and steps[st][1] < merge:
                prev = toks[-1]; pl = float(prev.split("/")[1].split("b")[0])
                toks[-1] = f"{nm(m)}/{pl + (e - st) / 4:g}b@" + prev.split("@")[1]
            else:
                toks.append(f"{nm(m)}/{(e - st) / 4:g}b@{v}")
            if e < end:
                toks.append(f"R/{(end - e) / 4:g}b")
        out.append((j, " ".join(toks)))
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    spans = None
    if "--map" in a:   # stemnotes.py STEM --map MAP.json B0 B1 [...]: bar times/lengths from a tab2song map
        import importlib.util, json
        here = os.path.dirname(os.path.abspath(__file__))
        spec = importlib.util.spec_from_file_location("t2s", os.path.join(here, "tab2song.py"))
        t2s = importlib.util.module_from_spec(spec); spec.loader.exec_module(t2s)
        i = a.index("--map"); mp = json.load(open(a[i + 1])); del a[i:i + 2]
        cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(os.path.dirname(here), mp["cache"])
        spans, t = {}, mp.get("offset", 0.0)
        for m in t2s.corrected_timeline(cache, mp):
            if m["skip"]:
                continue
            d = m["beats"] * 60 / m["bpm"]; spans[m["m"]] = (t, d, m["beats"]); t += d
        path, b0, b1 = a[0], int(a[1]), int(a[2]); d0 = bar = 0.0
    else:
        path, d0, bar, b0, b1 = a[0], float(a[1]), float(a[2]), int(a[3]), int(a[4])
    lo = int(a[a.index("--lo") + 1]) if "--lo" in a else 23
    hi = int(a[a.index("--hi") + 1]) if "--hi" in a else 52
    th = float(a[a.index("--th") + 1]) if "--th" in a else 0.25
    mg = float(a[a.index("--merge") + 1]) if "--merge" in a else 0.6
    fl = float(a[a.index("--floor") + 1]) if "--floor" in a else None
    for j, line in transcribe(path, d0, bar, b0, b1, lo, hi, th, mg, fl, spans):
        print(f"bar {j:3d}  {line}")
