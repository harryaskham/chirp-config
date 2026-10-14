#!/usr/bin/env python3
"""Instrument-tone comparison on repeated isolated events: a reference stem vs our soloed render.

Averages over every occurrence of one articulation (e.g. the held B0 that opens a riff bar), each event
normalised to its own level, so it compares tone shape rather than loudness:
  env       spectral envelope in 1/6-octave bands, 60 Hz-16 kHz (dB re the event's mean)  -> amp/cab/EQ gaps
  contrast  peak-to-valley spread of the fine spectrum per octave (90th vs 10th percentile bins, dB)
            -> 'clean synthetic harmonics' (deep valleys) vs real rigs (noise, IMD, doubles and room fill them)
  irreg     partial irregularity: dB std of the f0-harmonic peaks around their smoothed envelope, 100 Hz-4 kHz
            -> pick-position combs, cab notches (a saw follows a smooth 1/n curve)
  attack    10 ms RMS frames: time to peak (ms) and decay slope over the window (dB/s)
  flux      std over 20 ms frames of the 0.5-4 kHz band level during the sustain (dB) -> does the tone breathe
  corr      L/R correlation over the events

  tonecmp.py REF.wav REF_T0 OURS.wav OURS_T0 --events 0,3.75,... --win 0.04,0.66 [--f0 30.87] [--json]
Event times are seconds relative to each file's T0."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import likeness as L

SR = 48000


def events(x, t0, evs, w0, w1):
    return [x[int((t0 + e + w0) * SR):int((t0 + e + w1) * SR)] for e in evs]


def spectrum(segs, n=65536):
    f = np.fft.rfftfreq(n, 1 / SR); P = np.zeros(n // 2 + 1)
    for s in segs:
        m = s.mean(1) if s.ndim == 2 else s
        p = np.abs(np.fft.rfft(m * np.hanning(len(m)), n)) ** 2
        P += p / (p[(f > 60) & (f < 16000)].mean() + 1e-20)        # each event normalised to its own level
    return f, P / len(segs)


def sixth_octave(f, P):
    edges = 60 * 2 ** (np.arange(0, 8.1, 1 / 6)); edges = edges[edges <= 16000]
    b = np.array([P[(f >= a) & (f < c)].mean() for a, c in zip(edges[:-1], edges[1:])])
    db = 10 * np.log10(b + 1e-20); return np.sqrt(edges[:-1] * edges[1:]), db - db.mean()


def contrast(f, P):
    out = {}
    for lo in (100, 200, 400, 800, 1600, 3200, 6400):
        sel = P[(f >= lo) & (f < 2 * lo)]
        out[lo] = float(10 * np.log10(np.percentile(sel, 90) / (np.percentile(sel, 10) + 1e-20)))
    return out


def irregularity(f, P, f0):
    ks = np.arange(1, int(4000 / f0)); amps = []
    for k in ks:
        sel = (f > k * f0 * 0.985) & (f < k * f0 * 1.015)
        amps.append(10 * np.log10(P[sel].max() + 1e-20) if sel.any() else np.nan)
    a = np.array(amps); hz = ks * f0; ok = (hz > 100) & np.isfinite(a)
    sm = np.convolve(a[ok], np.ones(7) / 7, "same")                  # smoothed envelope over neighbouring partials
    return float(np.std((a[ok] - sm)[3:-3]))


def temporal(segs):
    att, dec, flux = [], [], []
    for s in segs:
        m = s.mean(1) if s.ndim == 2 else s
        fr = m[: len(m) // 480 * 480].reshape(-1, 480); r = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
        k = int(np.argmax(r)); att.append(k * 10.0)
        tail = r[k:]; t = np.arange(len(tail)) * 0.01
        if len(tail) > 5:   # least-squares slope by hand (numpy's lstsq is broken on some hosts)
            tc = t - t.mean(); dec.append(float((tc * (tail - tail.mean())).sum() / ((tc ** 2).sum() + 1e-12)))
        n = 960; frames = m[: len(m) // n * n].reshape(-1, n)
        spec = np.abs(np.fft.rfft(frames * np.hanning(n), axis=1)) ** 2; ff = np.fft.rfftfreq(n, 1 / SR)
        band = 10 * np.log10(spec[:, (ff > 500) & (ff < 4000)].sum(1) + 1e-20)
        flux.append(float(np.std(np.diff(band[2:]))))
    return float(np.median(att)), float(np.median(dec)), float(np.median(flux))


def corr(segs):
    x = np.concatenate([s for s in segs if s.ndim == 2]); return float(np.corrcoef(x[:, 0], x[:, 1])[0, 1])


def profile(path, t0, evs, w0, w1, f0):
    segs = events(L.load(path), t0, evs, w0, w1)
    f, P = spectrum(segs); cen, env = sixth_octave(f, P)
    per = [contrast(*spectrum([s])) for s in segs]                    # per event: averaging smears drifting partials
    con = {lo: float(np.median([c[lo] for c in per])) for lo in per[0]}
    a, d, fl = temporal(segs)
    return {"centres": cen.tolist(), "env": env.tolist(), "contrast": con, "irreg": irregularity(f, P, f0),
            "attack_ms": a, "decay_db_s": d, "flux_db": fl, "corr": corr(segs)}


def main():
    a = sys.argv[1:]
    ref, rt0, ours, ot0 = a[0], float(a[1]), a[2], float(a[3])
    evs = [float(v) for v in a[a.index("--events") + 1].split(",")]
    w0, w1 = ([float(v) for v in a[a.index("--win") + 1].split(",")] if "--win" in a else (0.04, 0.66))
    f0 = float(a[a.index("--f0") + 1]) if "--f0" in a else 30.87
    R, O = profile(ref, rt0, evs, w0, w1, f0), profile(ours, ot0, evs, w0, w1, f0)
    if "--json" in a:
        print(json.dumps({"ref": R, "ours": O})); return
    print("1/6-octave envelope, ours − ref (dB):")
    row = [f"{int(c) if c < 1000 else f'{c / 1000:.1f}k':>5}" for c in R["centres"]]
    d = np.array(O["env"]) - np.array(R["env"])
    for i in range(0, len(row), 12):
        print("  " + " ".join(row[i:i + 12])); print("  " + " ".join(f"{v:+5.1f}" for v in d[i:i + 12]))
    print("harmonic-line contrast per octave (dB, 90th/10th pct)   ref → ours:")
    print("  " + "  ".join(f"{lo}: {R['contrast'][lo]:4.1f} → {O['contrast'][lo]:4.1f}" for lo in R["contrast"]))
    for k, lab in (("irreg", "partial irregularity (dB)"), ("attack_ms", "attack to peak (ms)"), ("decay_db_s", "decay slope (dB/s)"),
                   ("flux_db", "0.5-4 kHz fluctuation (dB)"), ("corr", "L/R correlation")):
        print(f"{lab:30s} ref {R[k]:7.2f}   ours {O[k]:7.2f}")


if __name__ == "__main__":
    main()
