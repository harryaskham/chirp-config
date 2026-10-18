#!/usr/bin/env python3
"""Grounding check for the climb metric (likeness.sectioned): score a real reference against perturbed copies of
itself and look at what each change costs. A metric worth climbing on scores the reference 100 against itself,
barely moves for nuisances a listener would not call a different performance (a little noise, MP3, a few ms of
offset), drops in proportion for real degradation, and drops clearly for semantic changes (wrong pitch or tempo,
missing or wrong material) — and an impostor that matches the record's spectrum, loudness and stereo but plays
no notes must not score like a good reproduction.

  env -u LD_LIBRARY_PATH python3 tools/metricground.py ID [ID…] [--out DIR] [-j N]

ID is a climb (ref/ID.wav, tools/ID-sections.txt). Writes DIR/ID.json (default ref/evidence/metric-grounding) and
prints a table: the sectioned total and the duration-weighted term means for each perturbation. A one-off sanity
check, not part of a climb round (each song takes a few minutes).
"""
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS = ["loudness", "spectral", "chroma", "rhythm", "ltas", "stereo", "master"]


def fit(y, n):
    """Crop or zero-pad to n frames."""
    return y[:n] if len(y) >= n else np.concatenate([y, np.zeros((n - len(y), 2), y.dtype)])


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


def noise(x, snr_db, pink=False, seed=0):
    rng = np.random.default_rng(seed)
    w = rng.normal(0, 1, x.shape)
    if pink:   # 1/f power: shape white noise in the frequency domain
        W = np.fft.rfft(w, axis=0)
        f = np.fft.rfftfreq(len(w), 1 / SR)
        W /= np.sqrt(np.maximum(f, 20))[:, None]
        w = np.fft.irfft(W, len(w), axis=0)
    return x + w * rms(x) / rms(w) * 10 ** (-snr_db / 20)


def filt(x, kind, fc):
    sos = signal.butter(8, fc, btype=kind, fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=0)


def resample(x, ratio):
    """Play faster by `ratio` (pitch and tempo together)."""
    fr = Fraction(ratio).limit_denominator(2000)
    return signal.resample_poly(x, fr.denominator, fr.numerator, axis=0)


def stretch(x, rate, n=2048, hop=512):
    """Phase-vocoder time stretch (rate > 1: shorter), pitch kept."""
    out = []
    for ch in range(x.shape[1]):
        _, _, Z = signal.stft(x[:, ch], SR, nperseg=n, noverlap=n - hop)
        omega = 2 * np.pi * hop * np.arange(Z.shape[0]) / n
        steps = np.arange(0, Z.shape[1] - 1, rate)
        phase = np.angle(Z[:, 0])
        Y = np.empty((Z.shape[0], len(steps)), complex)
        for j, s in enumerate(steps):
            i, frac = int(s), s - int(s)
            mag = (1 - frac) * np.abs(Z[:, i]) + frac * np.abs(Z[:, i + 1])
            Y[:, j] = mag * np.exp(1j * phase)
            d = np.angle(Z[:, i + 1]) - np.angle(Z[:, i]) - omega
            phase = phase + omega + (d + np.pi) % (2 * np.pi) - np.pi
        _, y = signal.istft(Y, SR, nperseg=n, noverlap=n - hop)
        out.append(y)
    m = min(len(o) for o in out)
    return np.stack([o[:m] for o in out], 1)


def level(y, x):
    """y at x's RMS (the vocoder loses a few dB: a pitch or tempo case should not also be a level case)."""
    return y * rms(x) / rms(y)


def pitch(x, semis):
    r = 2 ** (semis / 12)
    return level(fit(resample(stretch(x, 1 / r), r), len(x)), x)


def drift(x, depth=0.005, period=60.0):
    """Wow: the playback speed wanders by ±depth over `period` seconds (tempo and pitch together)."""
    t = np.arange(len(x)) / SR
    src = t + depth * period / (2 * np.pi) * (1 - np.cos(2 * np.pi * t / period))
    src = np.clip(src * SR, 0, len(x) - 1)
    return np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in range(2)], 1)


def mp3(x, kbps, d):
    a, b = os.path.join(d, "in.wav"), os.path.join(d, "c.mp3")
    write(a, x)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-b:a", f"{kbps}k", b], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", b, "-ar", str(SR), a], check=True)
    return fit(L.load(a), len(x))


def impostor(x, seconds=0.0, seed=0):
    """Noise carrying the record's spectral envelope (third-octave smoothed: no pitches), loudness contour and stereo
    — every frame (seconds=0: the rhythm's envelope survives) or averaged over `seconds` (no rhythm either)."""
    rng = np.random.default_rng(seed)
    n, hop = 4096, 1024
    f = np.fft.rfftfreq(n, 1 / SR)
    edges = np.geomspace(20, SR / 2, 31)
    band = np.clip(np.searchsorted(edges, f) - 1, 0, 29)
    out = []
    for ch in range(2):
        _, _, Z = signal.stft(x[:, ch], SR, nperseg=n, noverlap=n - hop)
        P = np.abs(Z) ** 2
        E = np.stack([P[band == b].mean(0) if (band == b).any() else np.zeros(P.shape[1]) for b in range(30)])
        if seconds:
            k = max(1, int(seconds * SR / hop))
            E = signal.convolve(E, np.ones((1, k)) / k, mode="same")
        mag = np.sqrt(E[band])
        ph = np.exp(2j * np.pi * rng.random(Z.shape))
        _, y = signal.istft(mag * ph, SR, nperseg=n, noverlap=n - hop)
        out.append(y)
    m = min(len(o) for o in out)
    y = fit(np.stack([o[:m] for o in out], 1), len(x))
    return y * rms(x) / rms(y)


def write(path, x):
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def cases(x, other, d):
    n, h = len(x), len(x) // 2
    o = fit(other, n) * rms(x) / rms(fit(other, n))
    white_half = x.copy()
    white_half[h:] = np.random.default_rng(1).normal(0, rms(x[h:]), x[h:].shape)
    silent_half, other_half = x.copy(), x.copy()
    silent_half[h:] = 0
    other_half[h:] = o[h:]
    return [
        ("identity", "identity", lambda: x),
        ("nuisance", "gain -1 dB", lambda: x * 10 ** (-1 / 20)),
        ("nuisance", "white noise 40 dB SNR", lambda: noise(x, 40)),
        ("nuisance", "pink noise 30 dB SNR", lambda: noise(x, 30, pink=True)),
        ("nuisance", "MP3 192k", lambda: mp3(x, 192, d)),
        ("nuisance", "MP3 64k", lambda: mp3(x, 64, d)),
        ("nuisance", "low-pass 16 kHz", lambda: filt(x, "lowpass", 16000)),
        ("nuisance", "offset 10 ms", lambda: fit(np.concatenate([np.zeros((480, 2)), x]), n)),
        ("nuisance", "wow ±0.3%", lambda: drift(x, 0.003)),
        ("degraded", "white noise 20 dB SNR", lambda: noise(x, 20)),
        ("degraded", "white noise 10 dB SNR", lambda: noise(x, 10)),
        ("degraded", "low-pass 4 kHz", lambda: filt(x, "lowpass", 4000)),
        ("degraded", "low-pass 2 kHz", lambda: filt(x, "lowpass", 2000)),
        ("degraded", "high-pass 300 Hz", lambda: filt(x, "highpass", 300)),
        ("degraded", "8-bit", lambda: np.round(x * 127) / 127),
        ("degraded", "mono", lambda: np.repeat(x.mean(1, keepdims=True), 2, 1)),
        ("degraded", "gain -6 dB", lambda: x * 0.5),
        ("degraded", "offset 100 ms", lambda: fit(np.concatenate([np.zeros((4800, 2)), x]), n)),
        ("semantic", "pitch +1 semitone", lambda: pitch(x, 1)),
        ("semantic", "pitch -2 semitones", lambda: pitch(x, -2)),
        ("semantic", "tempo +3% (pitch kept)", lambda: level(fit(stretch(x, 1.03), n), x)),
        ("semantic", "speed +3% (pitch and tempo)", lambda: fit(resample(x, 1.03), n)),
        ("semantic", "second half silent", lambda: silent_half),
        ("semantic", "second half white noise", lambda: white_half),
        ("semantic", "second half another song", lambda: other_half),
        ("semantic", "reversed", lambda: x[::-1].copy()),
        ("control", "impostor: envelope noise, per frame", lambda: impostor(x)),
        ("control", "impostor: envelope noise, 1 s average", lambda: impostor(x, 1.0)),
        ("control", "another song", lambda: o),
    ]


def run_song(sid, other_id, out_dir):
    ref = os.path.join(ROOT, "ref", f"{sid}.wav")
    bounds = [float(v) for v in open(os.path.join(ROOT, "tools", f"{sid}-sections.txt")).read().split()[0].split(",")]
    x, other = L.load(ref), L.load(os.path.join(ROOT, "ref", f"{other_id}.wav"))
    rows = []
    with tempfile.TemporaryDirectory(prefix="metricground-") as d:
        for group, name, make in cases(x, other, d):
            y = make()
            path = os.path.join(d, "cand.wav")
            write(path, y)
            r = L.sectioned(ref, path, bounds)
            secs = r["sections"]
            w = np.array([s["end"] - s["start"] for s in secs])
            terms = {t: round(float(np.sum([s[t] for s in secs] * w) / w.sum()), 2) for t in TERMS}
            rows.append({"group": group, "case": name, "total": r["total"], **terms})
            print(f"{sid:22} {name:40} {r['total']:7.2f}", flush=True)
    json.dump(rows, open(os.path.join(out_dir, f"{sid}.json"), "w"), indent=1)
    return sid, rows


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(ROOT, "ref", "evidence", "metric-grounding")
    jobs = int(a[a.index("-j") + 1]) if "-j" in a else 2
    ids = [v for i, v in enumerate(a) if not v.startswith("-") and (i == 0 or a[i - 1] not in ("--out", "-j"))]
    os.makedirs(out, exist_ok=True)
    others = ids[1:] + ids[:1] if len(ids) > 1 else ["money" if ids[0] != "money" else "bleed"]
    with ProcessPoolExecutor(jobs) as ex:
        results = dict(ex.map(run_song, ids, others, [out] * len(ids)))
    # the table: each case's total per song and its mean, then the mean terms
    names = [(r["group"], r["case"]) for r in next(iter(results.values()))]
    print(f"\n{'':10}{'case':40}" + "".join(f"{s[:10]:>11}" for s in ids) + f"{'mean':>8}" + "".join(f"{t[:6]:>7}" for t in TERMS))
    for k, (g, c) in enumerate(names):
        tot = [results[s][k]["total"] for s in ids]
        terms = [np.mean([results[s][k][t] for s in ids]) for t in TERMS]
        print(f"{g:10}{c:40}" + "".join(f"{v:11.2f}" for v in tot) + f"{np.mean(tot):8.2f}" + "".join(f"{v:7.1f}" for v in terms))


if __name__ == "__main__":
    main(sys.argv[1:])
