#!/usr/bin/env python3
"""snarespec: a snare alone beside the snares of six records, by thirds of an octave, as a shape; with drumpunch's
two ratios and the stroke's fall. chirper-zero's bench of 19 Nov (Extreme and Mean v26), moved into tools/ at his
offer; its twins are tools/bassspec.py and tools/cymspec.py.

  snarespec.py NAME=SOLO.wav[:FROM:TO] ... [--each]

FILE is a raw solo render of the snare (`chirp render --solo TRACK --set loudness=null`); the strokes are found in
the file itself. Rows are SHAPES, each level on its own mean over 160 Hz-5 kHz: the records' median, half their
range, then each NAME less the median and its mean distance over that range; then body against crack (150-300 Hz
less 1.5-5 kHz), wires against crack (5-12 kHz less 1.5-5 kHz), and how long a stroke takes to fall 20 dB.
--each also prints every record less the median.

THE RECORDS' SIDE: each record's separated drum stem (ref/stems/bs_roformer_sw/ID/drums.wav), 30-90 s, at the snare
strokes of OUR transcription of that record (songs/ID.yaml) that no kick or tom falls within 30 ms of; the stem is
lined up with the transcription by its onsets and each stroke's peak found within 25 ms. Each stroke: the 120 ms
from 5 ms before its peak. Cymbals and hats fall with those strokes: trust 160 Hz-5 kHz, not the row above it, and
a stem's level is not the record's (tools/cymspec.py says how much of the top a stem loses). Five of the six agree
within 1.6 dB; The Faultless stands 5.2 off. The cache is ref/snarespec/records-snare.json (local; about 11 s to
build; it needs the six reproductions' song files and stems).

WHAT IT SHOWED THAT THE TWO RATIOS DID NOT (the album kit's snare, `ct-kit` s, on A3): its NOTE is in the 250 Hz
band where the records have theirs at 200 (ours -17 dB at 200, +6 at 250), with humps of +7.5 at 1-1.25 kHz and +6
to +8 at 2-2.5 kHz where theirs dip. `kit.s.pitch=G3` moves the note; `shell`, `shell_hz` and `reso_level` move
nothing (under 0.8 dB); `damp` 0.9 takes 2.5 dB off 1 kHz. THE HUMPS COME OUT WHERE THEY ARE MADE (In the Time Of
v26, the same night): the head's `mode_count` 24 -> 10 takes 1 kHz from +8.1 to +4.1 and 1.25 kHz from +6.9 to
+0.8; `slap` 1.2 -> 0.5 takes 2.5 kHz from +6.9 to +3.3 (the slap IS the crack at 2.5 to 3 kHz). Bench
`kit.s.patch.synth.layers.0.mode_count` and `.slap` against this before reaching for eq. And two
cautions: the drums' bus glue and clip make a snare's measures depend on its FADER; and a snare's box can be
standing in for guitars that are short at 250 Hz-4 kHz, so let the MIX say how much of the cure to keep. A read,
not a score.
"""
import json
import os
import sys
import wave

import numpy as np

ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = ["bleed", "combustion", "electric-red", "obzen", "pravus", "the-faultless"]
C = [100 * 2 ** (i / 3) for i in range(22)]                    # 100 Hz ... 12.5 kHz
LAB = "100 125 160 200 250 315 400 500 630 800 1k 1.25k 1.6k 2k 2.5k 3.15k 4k 5k 6.3k 8k 10k 12.5k".split()
NORM = [i for i, c in enumerate(C) if 155 <= c <= 5100]
SR = 48000


def load(f, a=None, b=None):
    """The mono sum of a 16-bit WAV from second a to second b, at 48 kHz."""
    with wave.open(f) as w:
        sr = w.getframerate()
        if a is not None:
            w.setpos(int(a * sr))
        n = w.getnframes() - w.tell() if b is None else int((b - (a or 0)) * sr)
        y = np.frombuffer(w.readframes(n), dtype="<i2").reshape(-1, w.getnchannels()).astype(np.float64).mean(1) / 32768
    if sr != SR:
        from math import gcd

        from scipy.signal import resample_poly
        g = gcd(SR, sr)
        y = resample_poly(y, SR // g, sr // g)
    return y


def env(y, ms=2):
    """(the RMS envelope in steps of ms, the step in samples)."""
    h = int(SR * ms / 1000)
    n = len(y) // h
    return np.sqrt((y[:n * h].reshape(n, h) ** 2).mean(1) + 1e-20), h


def bp(y, lo, hi):
    Y = np.fft.rfft(y)
    f = np.fft.rfftfreq(len(y), 1 / SR)
    Y[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(Y, len(y))


def strokes_in(y):
    """The strokes of a solo snare file (s): rises of the 150 Hz-12 kHz envelope over a tenth of its top, 80 ms apart."""
    e, h = env(bp(y, 150, 12000))
    top = np.percentile(e, 99.5)
    out, i = [], 1
    while i < len(e):
        if e[i] > 0.1 * top and e[i] > 3 * e[max(0, i - 5)]:
            j = i + int(np.argmax(e[i:i + 15]))
            out.append(j * h / SR)
            i = j + int(0.08 * SR / h)
        else:
            i += 1
    return out


def read(y, peaks):
    """(shape, body-crack, wires-crack, the fall to -20 dB in ms, strokes read) over the strokes at `peaks` (s)."""
    acc = np.zeros(len(C))
    n = 4096 * 2
    f = np.fft.rfftfreq(n, 1 / SR)
    body, wires, dec = [], [], []
    e, h = env(bp(y, 150, 12000), 1)
    for t in peaks:
        a = int((t - 0.005) * SR)
        seg = y[a:a + int(0.12 * SR)]
        if a < 0 or len(seg) < int(0.12 * SR):
            continue
        P = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n)) ** 2
        acc += np.array([P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() for c in C])
        band = lambda lo, hi: 10 * np.log10(P[(f >= lo) & (f < hi)].sum() + 1e-20)  # noqa: E731
        body.append(band(150, 300) - band(1500, 5000))
        wires.append(band(5000, 12000) - band(1500, 5000))
        k = int(t * SR / h)
        tail = e[k:k + 400]
        below = np.nonzero(tail < e[k:k + 20].max() / 10)[0]
        dec.append(float(below[0]) if len(below) else 400.0)
    if not body:
        raise SystemExit("snarespec: no stroke found (a stroke needs 120 ms of the file after it)")
    s = 10 * np.log10(acc + 1e-20)
    return s - s[NORM].mean(), float(np.median(body)), float(np.median(wires)), float(np.median(dec)), len(body)


def records(root=None):
    """{record id: {shape, body, wires, decay, n, lag_ms}}, cached in ref/snarespec/records-snare.json."""
    root = root or ROOT
    cache = os.path.join(root, "ref", "snarespec", "records-snare.json")
    if os.path.exists(cache):
        with open(cache) as fh:
            return json.load(fh)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import drumpunch as D
    out = {}
    for r in REFS:
        song, stem = os.path.join(root, "songs", r + ".yaml"), os.path.join(root, "ref", "stems", "bs_roformer_sw", r, "drums.wav")
        if not (os.path.exists(song) and os.path.exists(stem)):
            continue
        evs, _ = D.events(song)
        y = load(stem, 29.8, 90.2)
        e, h = env(bp(y, 150, 12000))
        train = np.zeros(len(e))
        for t, _, _ in evs:
            if 30 <= t < 90:
                train[min(len(e) - 1, int((t - 29.8) * SR / h))] = 1
        d = np.diff(e, prepend=e[0]).clip(0)
        L = int(0.1 * SR / h)
        lag = max(range(-L, L + 1), key=lambda s: float((np.roll(train, s) * d).sum())) * h / SR
        peaks = []
        for t in D.clean(evs, "snare"):
            if 30.3 <= t < 89.7:
                k, w = int((t - 29.8 + lag) * SR / h), int(0.025 * SR / h)
                peaks.append((k - w + int(np.argmax(e[k - w:k + w + 1]))) * h / SR)
        s, body, wires, dec, n = read(y, peaks)
        out[r] = {"shape": [float(v) for v in s], "body": body, "wires": wires, "decay": dec, "n": n, "lag_ms": 1000 * lag}
    if not out:
        raise SystemExit("snarespec: no record to read (songs/ID.yaml and ref/stems/bs_roformer_sw/ID/drums.wav)")
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache + ".new", "w") as fh:
        json.dump(out, fh)
    os.replace(cache + ".new", cache)
    return out


def tail(body, wires, dec, n=None):
    return f"| {body:+9.1f} {wires:+10.1f} {dec:8.0f}" + (f"   ({n})" if n is not None else "")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return
    R = records()
    M = np.array([v["shape"] for v in R.values()])
    med = np.median(M, 0)
    srt = np.sort(M, 0)
    half = (srt[-1] - srt[0]) / 2
    print(f"{'Hz':16s}" + "".join(f"{x:>6s}" for x in LAB) + "   mean|d| 160-5k | body-crack wires-crack fall-20dB ms  (strokes)")
    print(f"{'RECORDS (median)':16s}" + "".join(f"{v:6.1f}" for v in med) + " " * 18
          + tail(*(float(np.median([v[k] for v in R.values()])) for k in ("body", "wires", "decay"))) + f"   ({len(R)} records)")
    print(f"{'half their range':16s}" + "".join(f"{v:6.1f}" for v in half))
    if "--each" in argv:
        for r, v in R.items():
            d = np.array(v["shape"]) - med
            print(f"{r[:15]:16s}" + "".join(f"{x:+6.1f}" for x in d) + f"   {np.abs(d)[NORM].mean():.2f}            "
                  + tail(v["body"], v["wires"], v["decay"], v["n"]))
    for a in argv:
        if a.startswith("--"):
            continue
        if "=" not in a:
            raise SystemExit("snarespec: NAME=FILE[:FROM:TO]")
        name, rest = a.split("=", 1)
        parts = rest.split(":")
        y = load(parts[0], *(float(x) for x in parts[1:3])) if len(parts) == 3 else load(parts[0])
        s, body, wires, dec, n = read(y, strokes_in(y))
        d = s - med
        print(f"{name[:15]:16s}" + "".join(f"{v:+6.1f}" for v in d) + f"   {np.abs(d[NORM]).mean():.2f}            "
              + tail(body, wires, dec, n))
    print("(shapes, not levels. The records' strokes are in separated stems with their cymbals: trust 160 Hz-5 kHz; "
          "a stem's level is not the record's.)")


if __name__ == "__main__":
    main()
