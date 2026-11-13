#!/usr/bin/env python3
"""stops: do the guitars stop? How far a part's level falls between its notes, beside the same part on reference records.

  stops.py [--refs ID,ID,...] [--stem guitar] [--model bs_roformer_sw] [--from 30 --dur 120] --ours WAV [WAV ...]

For each reference: its stem (ref/stems/MODEL/ID/STEM.*) over the window. For ours: the part rendered alone and raw
(`chirp render --solo gl --solo gr ... --set loudness=null`). The level is taken in 10 ms frames, 150 Hz-8 kHz; only the
seconds where the part is playing count (their loud level within 6 dB of the whole window's), so a section where it rests
is not read as a stop. Against the loud level (the 95th percentile of the frames), in dB:
  p50, p25, p5   how far the middling, the quieter and the quietest frames sit below it
  <-12, <-20     the share of frames more than 12 and 20 dB below it: the time spent in gaps
A high-gain guitar that never stops reads p5 about -3 dB and no time in gaps: a wall. A rig with a working gate reads tens of dB.

What it found (Common Time, 13 Nov): see the numbers in compose/chirpers10/sounds.md, "the stops that did not stop".
Caveat: a reference is the separator's stem. Drums bleeding into a guitar stem's gaps make the record look LESS gapped than
it is, so the records' figures are a floor for how far real guitars fall. (chirper-zero, for Common Time.)"""
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
SR = 24000
DEFAULT = ("bleed,combustion,dancers-to-a-discordant-system,electric-red,lethargica,obzen,pineal-gland-optics,pravus,"
           "the-abysmal-eye,the-faultless,this-spiteful-snake")
ENV = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
SOS = sg.butter(4, [150, 8000], "bandpass", fs=SR, output="sos")


def load(path, ss=None, t=None):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        cut = ["-ss", str(ss), "-t", str(t)] if ss is not None else []
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *cut, "-i", path, "-ar", str(SR), "-ac", "1", f.name], env=ENV, check=True)
        w = wave.open(f.name)
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768


def measure(x):
    x = sg.sosfilt(SOS, x)
    n = SR // 100
    e = 10 * np.log10((x[:len(x) // n * n].reshape(-1, n) ** 2).mean(1) + 1e-12)
    sec = e[:len(e) // 100 * 100].reshape(-1, 100)
    loud = np.percentile(sec, 95, axis=1)
    top = np.percentile(e, 95)
    on = sec[loud > top - 6].ravel()
    if not len(on):
        return None
    p95 = np.percentile(on, 95)
    return [np.percentile(on, q) - p95 for q in (50, 25, 5)] + [100 * (on < p95 - 12).mean(), 100 * (on < p95 - 20).mean(), len(on) / 100]


def stem_path(model, rid, stem):
    d = os.path.join(ROOT, "ref", "stems", model, rid)
    for ext in ("wav", "opus", "flac"):
        p = os.path.join(d, f"{stem}.{ext}")
        if os.path.exists(p):
            return p
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--refs", default=DEFAULT)
    ap.add_argument("--stem", default="guitar")
    ap.add_argument("--model", default="bs_roformer_sw")
    ap.add_argument("--from", dest="start", type=float, default=30)
    ap.add_argument("--dur", type=float, default=120)
    ap.add_argument("--ours", nargs="*", default=[])
    a = ap.parse_args()
    head = "%-36s %7s %7s %7s %8s %8s %8s" % ("", "p50", "p25", "p5", "<-12 dB", "<-20 dB", "seconds")
    print(head)
    rows = []
    for rid in [r for r in a.refs.split(",") if r]:
        p = stem_path(a.model, rid, a.stem)
        if not p:
            print(f"  (skipped {rid}: no {a.stem} stem)", file=sys.stderr)
            continue
        m = measure(load(p, a.start, a.dur))
        if m:
            rows.append(m)
            print("%-36s %7.1f %7.1f %7.1f %7.0f%% %7.0f%% %8.0f" % (rid, *m))
    if rows:
        r = np.array(rows)
        print("%-36s %7.1f %7.1f %7.1f %7.0f%% %7.0f%%" % (f"records' {a.stem}, median", *np.median(r[:, :5], 0)))
    for p in a.ours:
        m = measure(load(p))
        print("%-36s %7.1f %7.1f %7.1f %7.0f%% %7.0f%% %8.0f" % ("OURS " + os.path.basename(p)[:30], *m) if m else f"OURS {p}: silent")


if __name__ == "__main__":
    main()
