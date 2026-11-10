#!/usr/bin/env python3
"""look.py - SEE a render when you cannot hear it (chirper-three, 10 Nov 2026).

One PNG per WAV, four panels on a shared time axis:
  1. log-frequency spectrogram (mid channel, dB re the file's loudest bin)
  2. level: short-term RMS and its low (<120 Hz) / mid (120 Hz-2 kHz) / high (>2 kHz) bands, 1 s windows
  3. stereo: side/mid ratio in dB (0 = as much side as mid; -inf = mono), 1 s windows, per band
  4. motion: onsets per second (spectral-flux peaks, 4 s windows) and spectral centroid

  look.py WAV [--out PNG] [--title T] [--song songs/ID.yaml --bars "lens:1,A:17,..."] [--marks "0:33=A,..."]
          [--from S --to S]   (zoom: seconds)

Marks are drawn as vertical lines. With --song, bar numbers are mapped through the song's tempo map (ramps too).
Prints a small table of per-section numbers (level, bands, width, onsets, centroid) so the picture can be quoted.
Compare against a reference by running it on both: the scales are absolute (dBFS), not per-file.
"""
import argparse
import json
import math
import subprocess
import sys

import numpy as np


def decode(path, sr=32000, t0=None, t1=None):
    cmd = ["ffmpeg", "-loglevel", "error"]
    if t0 is not None:
        cmd += ["-ss", str(t0)]
    if t1 is not None:
        cmd += ["-t", str(t1 - (t0 or 0))]
    cmd += ["-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64), sr


def tempo_fn(song):
    d = json.load(open(song))
    pts = [(float(p["at"][:-1]), p["bpm"], p.get("ramp", False)) for p in d.get("tempo", [])] if isinstance(
        d.get("tempo"), list) else [(0.0, float(d.get("tempo", 120)), False)]

    def t_of(b):
        t = 0.0
        for i, (b0, bpm0, _) in enumerate(pts):
            b1 = pts[i + 1][0] if i + 1 < len(pts) else 1e12
            bpm1 = pts[i + 1][1] if i + 1 < len(pts) and pts[i + 1][2] else bpm0
            if b <= b0:
                break
            bb = min(b, b1)
            if bpm1 != bpm0 and b1 < 1e11:
                k = (bpm1 - bpm0) / (b1 - b0)
                t += 60 / k * math.log((bpm0 + k * (bb - b0)) / bpm0)
            else:
                t += (bb - b0) * 60 / bpm0
            if b <= b1:
                break
        return t
    bpb = 4
    return lambda bar: t_of((bar - 1) * bpb)


def stft(x, n=4096, hop=1024):
    w = np.hanning(n)
    frames = 1 + max(0, (len(x) - n) // hop)
    idx = np.arange(n)[None, :] + hop * np.arange(frames)[:, None]
    return np.abs(np.fft.rfft(x[idx] * w, axis=1)) ** 2          # frames x bins (power)


def db(x, floor=1e-12):
    return 10 * np.log10(np.maximum(x, floor))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--out")
    ap.add_argument("--title")
    ap.add_argument("--song")
    ap.add_argument("--bars", help='"name:bar,name:bar" (needs --song)')
    ap.add_argument("--marks", help='"M:SS=name,..."')
    ap.add_argument("--from", dest="t0", type=float)
    ap.add_argument("--to", dest="t1", type=float)
    ap.add_argument("--no-png", action="store_true")
    a = ap.parse_args()

    x, sr = decode(a.wav, t0=a.t0, t1=a.t1)
    off = a.t0 or 0.0
    mid, side = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2
    n, hop = 4096, 1024
    Pm, Ps = stft(mid, n, hop), stft(side, n, hop)
    freqs = np.fft.rfftfreq(n, 1 / sr)
    tt = off + (np.arange(Pm.shape[0]) * hop + n / 2) / sr
    norm = (np.hanning(n).sum() ** 2) / 4                          # power of a full-scale sine -> 0 dB

    marks = []
    if a.bars and a.song:
        bt = tempo_fn(a.song)
        for item in a.bars.split(","):
            name, bar = item.split(":")
            marks.append((bt(float(bar)), name))
    if a.marks:
        for item in a.marks.split(","):
            ts, name = item.split("=")
            m, s = ts.split(":")
            marks.append((int(m) * 60 + float(s), name))
    marks.sort()

    bands = {"low": (20, 120), "mid": (120, 2000), "high": (2000, 16000)}
    fps = sr / hop

    def smooth(v, secs):
        k = max(1, int(round(secs * fps)))
        return np.convolve(v, np.ones(k) / k, mode="same")

    tot = Pm.sum(1) + Ps.sum(1)
    lev = {"all": db(smooth(tot, 1.0) / norm)}
    wid = {"all": db(smooth(Ps.sum(1), 1.0) / np.maximum(smooth(Pm.sum(1), 1.0), 1e-15))}
    for k, (lo, hi) in bands.items():
        sel = (freqs >= lo) & (freqs < hi)
        lev[k] = db(smooth(Pm[:, sel].sum(1) + Ps[:, sel].sum(1), 1.0) / norm)
        wid[k] = db(smooth(Ps[:, sel].sum(1), 1.0) / np.maximum(smooth(Pm[:, sel].sum(1), 1.0), 1e-15))
    # spectral flux onsets (log-compressed magnitude, half-wave rectified), peak-picked
    mag = np.log1p(1000 * np.sqrt(Pm / norm))
    flux = np.maximum(mag[1:] - mag[:-1], 0).sum(1)
    flux = np.concatenate([[0], flux])
    med = np.array([np.median(flux[max(0, i - 8):i + 9]) for i in range(len(flux))])
    thr = med * 1.5 + 0.02 * flux.max()
    pk = (flux > thr) & (flux >= np.roll(flux, 1)) & (flux > np.roll(flux, -1))
    onset_rate = smooth(pk.astype(float), 4.0) * fps
    cen = smooth((Pm * freqs).sum(1), 1.0) / np.maximum(smooth(Pm.sum(1), 1.0), 1e-15)

    # table
    edges = [(off, "start")] + [(t, nm) for t, nm in marks if off < t < tt[-1]] + [(tt[-1], "end")]
    print(f"{a.title or a.wav}")
    print(f"  {'section':<12}{'from':>6}{'to':>7}{'level':>7}{'low':>7}{'mid':>7}{'high':>7}{'width':>7}{'w.hi':>7}{'ons/s':>7}{'cent':>7}")
    for (t0, nm), (t1, _) in zip(edges, edges[1:]):
        s = (tt >= t0) & (tt < t1)
        if s.sum() < 2:
            continue

        def avg_db(P, sel=None):
            v = P[s] if sel is None else P[s][:, sel]
            return db(v.sum(1).mean() / norm)
        lo_s, mi_s, hi_s = [((freqs >= lo) & (freqs < hi)) for lo, hi in bands.values()]
        allp = (Pm[s].sum(1) + Ps[s].sum(1)).mean()
        w_all = db(Ps[s].sum() / max(Pm[s].sum(), 1e-15))
        w_hi = db(Ps[s][:, hi_s].sum() / max(Pm[s][:, hi_s].sum(), 1e-15))
        print(f"  {nm:<12}{int(t0 // 60):>3}:{int(t0 % 60):02d}{int(t1 // 60):>4}:{int(t1 % 60):02d}{db(allp / norm):>7.1f}"
              f"{avg_db(Pm + Ps, lo_s):>7.1f}{avg_db(Pm + Ps, mi_s):>7.1f}{avg_db(Pm + Ps, hi_s):>7.1f}{w_all:>7.1f}{w_hi:>7.1f}"
              f"{pk[s].sum() / max(1e-9, (t1 - t0)):>7.1f}{cen[s].mean():>7.0f}")
    if a.no_png:
        return

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # log-frequency bins
    nb = 180
    fe = np.geomspace(30, 16000, nb + 1)
    S = np.zeros((nb, Pm.shape[0]))
    for i in range(nb):
        sel = (freqs >= fe[i]) & (freqs < fe[i + 1])
        if not sel.any():
            sel = np.zeros_like(freqs, bool)
            sel[np.argmin(np.abs(freqs - (fe[i] + fe[i + 1]) / 2))] = True
        S[i] = Pm[:, sel].mean(1)
    Sdb = db(S / norm)
    fig, ax = plt.subplots(4, 1, figsize=(15, 9.2), sharex=True, gridspec_kw={"height_ratios": [3.4, 1.5, 1.2, 1.2]})
    ax[0].imshow(Sdb, origin="lower", aspect="auto", cmap="magma", vmin=-95, vmax=-25,
                 extent=[tt[0], tt[-1], 0, nb])
    ticks = [50, 100, 200, 500, 1000, 2000, 5000, 10000]
    ax[0].set_yticks([np.log(f / 30) / np.log(16000 / 30) * nb for f in ticks])
    ax[0].set_yticklabels([str(f) for f in ticks])
    ax[0].set_ylabel("Hz")
    ax[0].set_title(a.title or a.wav, loc="left", fontsize=10)
    for k, c in (("all", "k"), ("low", "tab:red"), ("mid", "tab:green"), ("high", "tab:blue")):
        ax[1].plot(tt, lev[k], c, lw=1.1 if k == "all" else 0.8, label=k)
    ax[1].set_ylim(-60, -5)
    ax[1].set_ylabel("level dBFS")
    ax[1].legend(loc="lower right", ncol=4, fontsize=7)
    ax[1].grid(alpha=0.25)
    for k, c in (("all", "k"), ("low", "tab:red"), ("mid", "tab:green"), ("high", "tab:blue")):
        ax[2].plot(tt, wid[k], c, lw=1.1 if k == "all" else 0.8, label=k)
    ax[2].set_ylim(-40, 3)
    ax[2].set_ylabel("side/mid dB")
    ax[2].grid(alpha=0.25)
    ax[3].plot(tt, onset_rate, "k", lw=1.0)
    ax[3].set_ylabel("onsets/s")
    ax[3].set_ylim(0, 14)
    ax[3].grid(alpha=0.25)
    a2 = ax[3].twinx()
    a2.plot(tt, cen, "tab:orange", lw=0.8)
    a2.set_yscale("log")
    a2.set_ylim(150, 8000)
    a2.set_ylabel("centroid Hz", color="tab:orange")
    ax[3].set_xlabel("seconds")
    for t, nm in marks:
        for i in range(4):
            ax[i].axvline(t, color="w" if i == 0 else "0.4", lw=0.7, ls="--")
        ax[0].text(t, nb * 1.005, nm, color="k", fontsize=7, ha="left", va="bottom", clip_on=False, rotation=0)
    ax[0].set_xlim(tt[0], tt[-1])
    fig.tight_layout()
    out = a.out or (a.wav.rsplit(".", 1)[0] + "-look.png")
    fig.savefig(out, dpi=100)
    print("  ->", out)


if __name__ == "__main__":
    sys.exit(main())
