#!/usr/bin/env python3
"""Per-hit pitch of a drum piece from the drum stem — tune a kit to the record and split a piece that stands in for two.

  drumpeaks.py SONG.yaml TRACK STEM.wav [--piece ft] [--lo 40] [--hi 400] [--win 0.1]
               [--split B3-C#4 --to t1 -o OUT.yaml]

For every hit of PIECE in TRACK (a drumtrans-style score: `piece/<dur>b@vel` tokens, chords `a,b/…`), takes the stem's
strongest spectral peak between --lo and --hi Hz in the --win seconds after the hit and prints the histogram of those
peaks as notes (tune the piece with `kit.<piece>.pitch=NOTE`). With --split LO-HI --to OTHER, hits whose peak falls in
that note range are renamed to OTHER (another kit piece, e.g. a tom tuned to that pitch) and the song is written to -o.
Constant-tempo songs (`tempo:` at the top; no tempo automation). chirper-zero's Saturnine r20 method (kick G1, toms
C4/D3: +0.15 held-out); their floor tom stood in for both a low drum (C#2/B1) and a higher body (B3..C#4)."""
import re
import sys
import wave

import numpy as np

NM = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_of(name):
    m = re.match(r"^([A-G])(#|b)?(-?\d)$", name)
    n = NM.index(m.group(1)) + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0)
    return (int(m.group(3)) + 1) * 12 + n


def name_of(mi):
    return f"{NM[mi % 12]}{mi // 12 - 1}"


def load(p):
    with wave.open(p, "rb") as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes(); raw = w.readframes(n)
    x = np.frombuffer(raw, dtype="<i2" if sw == 2 else "<i4").astype(np.float32) / (32768 if sw == 2 else 2147483648)
    return x.reshape(-1, ch).mean(1), sr


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    song, track, stem = a[:3]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    piece, lo, hi, win = opt("--piece", "ft"), opt("--lo", 40.0), opt("--hi", 400.0), opt("--win", 0.1)
    y = open(song).read()
    tempo = float(re.search(r"^tempo:\s*([\d.]+)", y, re.M).group(1))
    m = re.search(r'(name: "?' + re.escape(track) + r'"?,.*?score: ")([^"]*)(")', y)
    if not m:
        sys.exit(f"track {track} not found")
    toks = m.group(2).split()
    x, sr = load(stem)
    n = int(win * sr); nfft = 1 << 16   # heavy zero-padding + parabolic interpolation: G1/G#1 are 2.9 Hz apart
    f = np.fft.rfftfreq(nfft, 1 / sr); band = (f >= lo) & (f <= hi)
    beat, peaks = 0.0, {}
    for i, t in enumerate(toks):
        head, _, rest = t.partition("/")
        dur = float(re.match(r"([\d.]+)b", rest).group(1))
        if piece in head.split(","):
            s0 = int(beat * 60 / tempo * sr); seg = x[s0:s0 + n]
            if len(seg) == n:
                F = np.log(np.abs(np.fft.rfft(seg * np.hanning(n), nfft)) + 1e-12)
                k = np.flatnonzero(band)[np.argmax(F[band])]
                d = 0.5 * (F[k - 1] - F[k + 1]) / (F[k - 1] - 2 * F[k] + F[k + 1] + 1e-12)
                fr = (k + float(np.clip(d, -1, 1))) * sr / nfft
                peaks[i] = int(round(69 + 12 * np.log2(fr / 440)))
        beat += dur
    hist = {}
    for v in peaks.values():
        hist[v] = hist.get(v, 0) + 1
    print(f"{piece} in {track}: {len(peaks)} hits; stem peak {lo:.0f}-{hi:.0f} Hz within {win * 1000:.0f} ms:")
    for k, v in sorted(hist.items(), key=lambda kv: -kv[1])[:14]:
        print(f"  {name_of(k):4s} {440 * 2 ** ((k - 69) / 12):7.1f} Hz  {v:4d}  {'#' * min(60, v // 3)}")
    if "--split" in a:
        r0, r1 = (midi_of(v) for v in opt("--split", "").split("-"))
        to = opt("--to", "")
        moved = 0
        for i, mi in peaks.items():
            if r0 <= mi <= r1:
                head, _, rest = toks[i].partition("/")
                toks[i] = ",".join(to if p == piece else p for p in head.split(",")) + "/" + rest; moved += 1
        out = y[:m.start(2)] + " ".join(toks) + y[m.end(2):]
        open(opt("-o", ""), "w").write(out)
        print(f"moved {moved} of {len(peaks)} {piece} hits ({opt('--split', '')}) to {to} -> {opt('-o', '')}")


if __name__ == "__main__":
    main()
