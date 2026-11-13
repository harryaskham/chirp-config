#!/usr/bin/env python3
"""voxref: a voice against the voices on reference records - its tone, and how loud it sits while it sings.

  voxref.py [--refs ID,ID,...] [--model bs_roformer_sw] [--secs 53] --ours SOLO.wav MIX.wav [--ours SOLO.wav MIX.wav ...]

For each reference: its vocal stem (ref/stems/MODEL/ID/vocals.*) and the record (ref/ID.wav), over the --secs seconds where
the stem is busiest. For ours: the voice rendered alone (`chirp render --solo vox --set loudness=null`) and the raw mix over the
same bars. Only the frames where the voice is within 15 dB of its own loud level count, so a sparse line and a dense one
compare. Two tables:
  TONE   the voice's own energy by band (120-250-500-1k-2k-4k-8k-16k Hz), in dB relative to the whole voice: the records'
         median and middle half, then ours and ours minus the median. An equaliser on the voice's track moves this.
  LEVEL  the voice's level minus the mix's, whole band and at 1-4 kHz (where words are told apart). The track's gain moves this.

What it found (Common Time v18, eleven Meshuggah records): their voices agree within about 1 dB per band from 500 Hz to 4 kHz,
and sit 9.2 dB under the record (7.1 at 1-4 kHz) with a middle half 0.8 dB wide. The library's `kidman` behind a 300 Hz
high-pass was 3-5 dB heavy at 250-500 Hz, 3.5 dB short at 1-2 kHz and 4 dB over at 4-8 kHz.

Caveat: a reference's voice is the separator's stem, so both tables lean on it (it may thin the low mids that the guitars
share and leak cymbals above 8 kHz). The records agreeing with each other says the estimate is steady, not that it is unbiased.
(chirper-zero, 13 Nov, for Common Time.)"""
import argparse
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from scipy import signal as sg

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(ROOT, "ref")) and ROOT != "/":
    ROOT = os.path.dirname(ROOT)
SR = 32000
EDGES = [120, 250, 500, 1000, 2000, 4000, 8000, 16000]
NAMES = ["-250", "-500", "-1k", "-2k", "-4k", "-8k", "-16k"]
DEFAULT = ("bleed,combustion,dancers-to-a-discordant-system,electric-red,lethargica,obzen,pineal-gland-optics,pravus,"
           "the-abysmal-eye,the-faultless,this-spiteful-snake")
ENV = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}


def load(path, ss=None, t=None):
    """Mono at SR through ffmpeg (so .wav, .opus and .flac all read)."""
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        cut = ["-ss", str(ss), "-t", str(t)] if ss is not None else []
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *cut, "-i", path, "-ar", str(SR), "-ac", "1", f.name], env=ENV, check=True)
        w = wave.open(f.name)
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768


def frames(v, n):
    return (v[:len(v) // n * n].reshape(-1, n) ** 2).mean(1) + 1e-12


def active(e):
    return e > np.percentile(e, 90) * 10 ** -1.5


def tone(v, n=4096):
    f = v[:len(v) // n * n].reshape(-1, n)
    on = active((f ** 2).mean(1) + 1e-12)
    spec = (np.abs(np.fft.rfft(f[on] * np.hanning(n), axis=1)) ** 2).mean(0)
    fr = np.fft.rfftfreq(n, 1 / SR)
    b = np.array([spec[(fr >= lo) & (fr < hi)].sum() for lo, hi in zip(EDGES[:-1], EDGES[1:])])
    return 10 * np.log10(b / b.sum() + 1e-12)


SOS = sg.butter(4, [1000, 4000], "bandpass", fs=SR, output="sos")


def level(v, m, n=SR // 10):
    k = min(len(v), len(m))
    v, m = v[:k], m[:k]
    fv, fm = frames(v, n), frames(m, n)
    on = active(fv)
    vb, mb = frames(sg.sosfilt(SOS, v), n), frames(sg.sosfilt(SOS, m), n)
    return 10 * np.log10(fv[on].mean() / fm[on].mean()), 10 * np.log10(vb[on].mean() / mb[on].mean()), float(on.mean())


def stem_path(model, rid):
    d = os.path.join(ROOT, "ref", "stems", model, rid)
    for ext in ("wav", "opus", "flac"):
        p = os.path.join(d, "vocals." + ext)
        if os.path.exists(p):
            return p
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--refs", default=DEFAULT)
    ap.add_argument("--model", default="bs_roformer_sw")
    ap.add_argument("--secs", type=int, default=53)
    ap.add_argument("--ours", nargs=2, action="append", default=[], metavar=("SOLO", "MIX"))
    a = ap.parse_args()
    tones, levels, names = [], [], []
    for rid in a.refs.split(","):
        stem, mix = stem_path(a.model, rid), os.path.join(ROOT, "ref", rid + ".wav")
        if not stem or not os.path.exists(mix):
            print(f"  (skipped {rid}: no vocal stem or no record)", file=sys.stderr)
            continue
        v = load(stem)
        ss = int(np.argmax(np.convolve(frames(v, SR), np.ones(a.secs), "valid")))
        v = v[ss * SR:(ss + a.secs) * SR]
        tones.append(tone(v))
        levels.append(level(v, load(mix, ss, a.secs)))
        names.append(rid)
    t, lv = np.array(tones), np.array(levels)
    print("TONE: the voice's own energy by band, dB relative to the whole voice (while it sings)")
    print("%-34s" % "" + "".join("%8s" % s for s in NAMES))
    print("%-34s" % f"records' voices, median of {len(names)}" + "".join("%8.1f" % x for x in np.median(t, 0)))
    print("%-34s" % "  25th" + "".join("%8.1f" % x for x in np.percentile(t, 25, 0)))
    print("%-34s" % "  75th" + "".join("%8.1f" % x for x in np.percentile(t, 75, 0)))
    ours = [(os.path.basename(s), load(s), load(m)) for s, m in a.ours]
    for name, v, _ in ours:
        s = tone(v)
        print("%-34s" % name[:32] + "".join("%8.1f" % x for x in s))
        print("%-34s" % "  minus the records" + "".join("%8.1f" % x for x in s - np.median(t, 0)))
    print("\nLEVEL: the voice minus the whole mix, dB (while it sings)")
    print("%-34s %8s %8s %9s" % ("", "whole", "1-4 kHz", "singing"))
    for n, r in zip(names, lv):
        print("%-34s %8.1f %8.1f %8.0f%%" % (n, r[0], r[1], r[2] * 100))
    print("%-34s %8.1f %8.1f" % ("records, median", *np.median(lv[:, :2], 0)))
    q = np.percentile(lv[:, :2], [25, 75], 0)
    print("%-34s %8s %8s" % ("records, middle half", "%.1f..%.1f" % (q[0, 0], q[1, 0]), "%.1f..%.1f" % (q[0, 1], q[1, 1])))
    for name, v, m in ours:
        r = level(v, m)
        print("%-34s %8.1f %8.1f %8.0f%%" % ("OURS " + name[:28], r[0], r[1], r[2] * 100))


if __name__ == "__main__":
    main()
