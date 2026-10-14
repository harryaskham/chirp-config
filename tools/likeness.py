#!/usr/bin/env python3
"""Numeric likeness between a reference recording and a chirp render (no images, no librosa).

  likeness.py describe REF.wav            tempo, key, sections, loudness contour, band balance
  likeness.py compare REF.wav CAND.wav    0-100 scores (loudness contour, spectral balance, chroma,
                                          rhythm, long-term spectrum, tempo) + per-section gaps
  likeness.py bands REF.wav CAND.wav      per-section band-by-band dB differences (what to fix)

Features: 48 kHz mono, STFT 4096 / hop 1024 (~21 ms), 40 log-spaced bands 30 Hz-16 kHz, 12-bin
chroma from 55-2000 Hz, spectral-flux onsets, Krumhansl key, checkerboard novelty sections."""
import json
import sys
import wave

import numpy as np
from scipy import signal

SR = 48000
NFFT, HOP = 4096, 1024
FPS = SR / HOP
BANDS7 = [("sub", 20, 60), ("low", 60, 150), ("lowmid", 150, 400), ("mid", 400, 1200),
          ("himid", 1200, 3500), ("pres", 3500, 8000), ("air", 8000, 16000)]
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def load(path):
    with wave.open(path, "rb") as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if sw == 2:
        x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768
    elif sw == 4:
        x = np.frombuffer(raw, dtype="<i4").astype(np.float32) / 2147483648
    else:
        raise SystemExit(f"unsupported sample width {sw}")
    x = x.reshape(-1, ch)
    stereo = x if ch == 2 else np.repeat(x, 2, axis=1)
    if sr != SR:
        g = np.gcd(sr, SR)
        stereo = signal.resample_poly(stereo, SR // g, sr // g, axis=0).astype(np.float32)
    return stereo


class Feat:
    def __init__(self, stereo):
        self.st = stereo
        x = stereo.mean(axis=1)
        self.x = x
        f, t, Z = signal.stft(x, SR, nperseg=NFFT, noverlap=NFFT - HOP, boundary=None, padded=False)
        self.f, self.mag = f, np.abs(Z).astype(np.float32)
        self.n = self.mag.shape[1]
        edges = np.geomspace(30, 16000, 41)
        self.bands = np.stack([(self.mag[(f >= a) & (f < b)] ** 2).sum(0) for a, b in zip(edges[:-1], edges[1:])]) + 1e-10
        self.logb = 10 * np.log10(self.bands)
        self.b7 = np.stack([(self.mag[(f >= a) & (f < b)] ** 2).sum(0) + 1e-10 for _, a, b in BANDS7])
        flux = np.maximum(np.diff(self.logb, axis=1), 0).sum(0)
        self.onset = np.concatenate([[0], flux])
        # chroma from a long (16384) FFT so semitones separate; 100 Hz-4 kHz, resampled to the hop grid
        f2, t2, Z2 = signal.stft(x, SR, nperseg=16384, noverlap=16384 - 4 * HOP, boundary=None, padded=False)
        sel = (f2 >= 100) & (f2 <= 4000)
        pcs = np.round(12 * np.log2(f2[sel] / 440.0) + 9).astype(int) % 12
        m2 = np.abs(Z2[sel]) ** 2
        ch = np.stack([m2[pcs == pc].sum(0) for pc in range(12)])
        ch = np.repeat(ch, 4, axis=1)
        pad = self.n - ch.shape[1]
        ch = np.pad(ch, ((0, 0), (max(0, pad // 2), max(0, pad - pad // 2))), mode="edge")[:, :self.n] if pad > 0 else ch[:, :self.n]
        self.chroma = (ch / (ch.sum(0, keepdims=True) + 1e-9)).astype(np.float32)
        cs = np.concatenate([[0.0], np.cumsum(x.astype(np.float64) ** 2)])
        mean_sq = (cs[SR:] - cs[:-SR]) / SR  # 1 s sliding mean (linear time)
        rms = np.sqrt(mean_sq[::SR // 2] + 1e-12)
        self.loud = 20 * np.log10(rms)  # per 0.5 s, 1 s window


def tempo(onset, lo=60, hi=200):
    o = onset - onset.mean()
    ac = np.correlate(o, o, mode="full")[len(o) - 1:]
    lags = np.arange(len(ac))
    bpm = np.where(lags > 0, 60 * FPS / np.maximum(lags, 1), 0)
    ok = (bpm >= lo) & (bpm <= hi)
    best = lags[ok][np.argmax(ac[ok])]
    return 60 * FPS / best


def key_of(chroma):
    c = chroma.mean(1)
    best = None
    for i in range(12):
        for prof, mode in ((MAJ, "major"), (MIN, "minor")):
            r = np.corrcoef(np.roll(prof, i), c)[0, 1]
            if best is None or r > best[0]:
                best = (r, f"{NAMES[i]} {mode}")
    return best[1], round(float(best[0]), 2)


def sections(F, min_len=6.0):
    """Checkerboard novelty on 0.5 s band frames; peaks ≥ min_len apart."""
    hop = int(FPS / 2)
    frames = np.stack([F.logb[:, i:i + hop].mean(1) for i in range(0, F.n - hop, hop)])
    frames = frames - frames.mean(1, keepdims=True)
    frames /= np.linalg.norm(frames, axis=1, keepdims=True) + 1e-9
    S = frames @ frames.T
    L = 8
    k = np.ones((2 * L, 2 * L)); k[:L, L:] = -1; k[L:, :L] = -1
    k *= np.outer(signal.windows.hann(2 * L), signal.windows.hann(2 * L))
    nov = np.zeros(len(S))
    for i in range(L, len(S) - L):
        nov[i] = (S[i - L:i + L, i - L:i + L] * k).sum()
    peaks, _ = signal.find_peaks(nov, distance=int(min_len * 2), prominence=np.std(nov) * 0.5)
    return [round(p / 2, 1) for p in peaks]


def band_db(F, a=0, b=None):
    i0, i1 = int(a * FPS), int((b or F.n / FPS) * FPS)
    e = F.b7[:, i0:i1].mean(1)
    return 10 * np.log10(e / e.sum())


def describe(path):
    F = Feat(load(path))
    dur = len(F.x) / SR
    secs = sections(F)
    bounds = [0.0] + secs + [round(dur, 1)]
    out = {"duration": round(dur, 2), "tempo": round(tempo(F.onset), 1), "key": key_of(F.chroma),
           "lufs_ish_rms": round(float(20 * np.log10(np.sqrt((F.x ** 2).mean()))), 1),
           "sections": []}
    for a, b in zip(bounds[:-1], bounds[1:]):
        i0, i1 = int(a * FPS), int(b * FPS)
        seg_on = F.onset[i0:i1]
        out["sections"].append({
            "start": a, "end": b,
            "rms": round(float(np.median(F.loud[int(a * 2):max(int(a * 2) + 1, int(b * 2))])), 1),
            "tempo": round(tempo(seg_on), 1) if len(seg_on) > FPS * 4 else None,
            "key": key_of(F.chroma[:, i0:i1])[0],
            "top_pcs": [NAMES[i] for i in np.argsort(-F.chroma[:, i0:i1].mean(1))[:4]],
            "bands": [round(float(v), 1) for v in band_db(F, a, b)],
            "width": round(float(np.std(F.st[int(a * SR):int(b * SR), 0] - F.st[int(a * SR):int(b * SR), 1]) /
                                 (np.std(F.st[int(a * SR):int(b * SR)].mean(1)) + 1e-9)), 2),
        })
    return out


def _cos(a, b):
    return float((a * b).sum() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def compare(ref, cand, verbose=True):
    R, C = Feat(load(ref)), Feat(load(cand))
    n = min(R.n, C.n)
    dur = n / FPS
    # loudness contour (shape: correlation; level: mean abs diff after matching overall level)
    m = min(len(R.loud), len(C.loud))
    lr, lc = R.loud[:m], C.loud[:m]
    corr = np.corrcoef(lr, lc)[0, 1] if m > 3 else 0
    lmad = np.abs((lr - lr.mean()) - (lc - lc.mean())).mean()
    s_loud = 100 * max(0, (corr + 1) / 2) * np.exp(-lmad / 6)
    # spectral balance per 2 s window: 40-band shape, level-normalised
    w = int(2 * FPS)
    dists = []
    for i in range(0, n - w, w):
        a = R.logb[:, i:i + w].mean(1); b = C.logb[:, i:i + w].mean(1)
        dists.append(np.abs((a - a.mean()) - (b - b.mean())).mean())
    s_spec = 100 * np.exp(-np.mean(dists) / 8)
    # chroma per 0.5 s window
    w2 = int(FPS / 2)
    cs = [_cos(R.chroma[:, i:i + w2].mean(1) - 1 / 12, C.chroma[:, i:i + w2].mean(1) - 1 / 12) for i in range(0, n - w2, w2)]
    s_chroma = 100 * max(0, np.mean(cs))
    # rhythm: onset envelopes smoothed ±50 ms, correlated per 4 s window (allowing ±1 frame shift)
    sm = np.ones(5) / 5
    ro, co = np.convolve(R.onset[:n], sm, "same"), np.convolve(C.onset[:n], sm, "same")
    w4 = int(4 * FPS); rs = []
    for i in range(0, n - w4, w4):
        a, b = ro[i:i + w4], co[i:i + w4]
        if a.std() > 0 and b.std() > 0:
            rs.append(np.corrcoef(a, b)[0, 1])
    s_rhythm = 100 * max(0, np.mean(rs)) if rs else 0
    # long-term average spectrum
    a, b = R.logb[:, :n].mean(1), C.logb[:, :n].mean(1)
    s_ltas = 100 * np.exp(-np.abs((a - a.mean()) - (b - b.mean())).mean() / 6)
    tr, tc = tempo(R.onset), tempo(C.onset)
    s_tempo = 100 * np.exp(-abs(np.log2(tc / tr)) * 12)
    total = 0.15 * s_loud + 0.25 * s_spec + 0.25 * s_chroma + 0.2 * s_rhythm + 0.1 * s_ltas + 0.05 * s_tempo
    res = {k: round(float(v), 1) for k, v in {"total": total, "loudness": s_loud, "spectral": s_spec, "chroma": s_chroma,
           "rhythm": s_rhythm, "ltas": s_ltas, "tempo": s_tempo, "tempo_ref": tr, "tempo_cand": tc,
           "dur_ref": R.n / FPS, "dur_cand": C.n / FPS}.items()}
    # per-section gaps on the reference's sections
    bounds = [0.0] + sections(R) + [round(dur, 1)]
    secs = []
    for s0, s1 in zip(bounds[:-1], bounds[1:]):
        i0, i1 = int(s0 * FPS), min(n, int(s1 * FPS))
        if i1 - i0 < FPS:
            continue
        a, b = R.logb[:, i0:i1].mean(1), C.logb[:, i0:i1].mean(1)
        ch = _cos(R.chroma[:, i0:i1].mean(1) - 1 / 12, C.chroma[:, i0:i1].mean(1) - 1 / 12)
        rl = float(np.median(R.loud[int(s0 * 2):int(s1 * 2)])); cl = float(np.median(C.loud[int(s0 * 2):int(s1 * 2)]))
        secs.append({"start": s0, "end": s1, "spec_mad": round(float(np.abs((a - a.mean()) - (b - b.mean())).mean()), 1),
                     "chroma": round(ch, 2), "level_ref": round(rl, 1), "level_cand": round(cl, 1)})
    res["sections"] = secs
    return res


def bands(ref, cand):
    R, C = Feat(load(ref)), Feat(load(cand))
    dur = min(R.n, C.n) / FPS
    bounds = [0.0] + sections(R) + [round(dur, 1)]
    rows = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        rd, cd = band_db(R, a, b), band_db(C, a, b)
        rows.append({"start": a, "end": b, "diff_db": {name: round(float(c - r), 1) for (name, _, _), r, c in zip(BANDS7, rd, cd)}})
    return rows


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "describe":
        print(json.dumps(describe(sys.argv[2]), indent=1))
    elif cmd == "compare":
        print(json.dumps(compare(sys.argv[2], sys.argv[3]), indent=1))
    elif cmd == "bands":
        print(json.dumps(bands(sys.argv[2], sys.argv[3]), indent=1))
