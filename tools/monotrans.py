#!/usr/bin/env python3
"""monotrans: transcribe a monophonic line (a vocal, a lead, a bass) from a stem (chirper-zero's Green Calx r12
prototype, made a tool: vocals pitch accuracy 18 -> 45, +0.8).

  monotrans.py STEM.wav --from A --to B [--gate -40] [--a4 440] [--range 40-84] [--hop 0.05] [--harmonics 5]
               [--min-len 0.08] [--json]                              print the notes
  monotrans.py STEM.wav --from A --to B … --into SONG --track NAME [--patch P] -o OUT
               write them into SONG (TRACK's notes starting in [A, B) replaced, or a new track on --patch;
               score tracks: convert with songfmt.py notes first), planned by chirp

Every --hop seconds a 4096-sample window quieter than --gate dBFS is silence; otherwise each candidate pitch (MIDI
--range in 10-cent steps, at --a4) scores the sum of its first --harmonics harmonics' magnitudes weighted 0.8^(h-1)
in a zero-padded FFT, and the best one, rounded to a semitone, is the frame's note. Runs of the same note at least
--min-len long become notes, their velocity from the run's level. A harmonic sum can pick an octave error on a
breathy or bled stem: audition (audition.py) and check with noteacc before keeping.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from likeness import SR, load  # noqa: E402
from padtrans import write_into  # noqa: E402

N, NF = 4096, 1 << 15


def frames(x, t0, t1, gate=-40.0, a4=440.0, lo=40, hi=84, hop=0.05, harmonics=5):
    """[(time s, MIDI note or None, level dB)] per hop."""
    h_ = int(round(hop * SR))
    f = np.fft.rfftfreq(NF, 1 / SR)
    df = f[1]
    cands = a4 * 2 ** ((np.arange(lo * 10, hi * 10) / 10 - 69) / 12)
    idx = [np.clip(np.round(cands * h / df).astype(int), 0, len(f) - 1) for h in range(1, harmonics + 1)]
    win = np.hanning(N)
    out = []
    for i in range(int(t0 * SR), int(t1 * SR) - N, h_):
        z = x[i:i + N]
        lv = 10 * np.log10(np.mean(z ** 2) + 1e-20)
        if lv < gate:
            out.append((i / SR, None, lv))
            continue
        X = np.abs(np.fft.rfft(z * win, NF))
        sal = np.zeros(len(cands))
        for h, ix in enumerate(idx, 1):
            sal += 0.8 ** (h - 1) * X[ix]
        m = 69 + 12 * np.log2(cands[np.argmax(sal)] / a4)
        out.append((i / SR, int(round(m)), lv))
    return out


def notes_of(fr, t1, hop=0.05, min_len=0.08):
    notes, cur = [], None
    for t, m, lv in fr + [(t1, None, -200)]:
        if cur and m == cur[1]:
            cur[2] = t + hop
            cur[3].append(lv)
            continue
        if cur and cur[2] - cur[0] >= min_len:
            notes.append({"at": f"{cur[0]:.3f}s", "len": f"{cur[2] - cur[0]:.3f}s", "pitch": cur[1],
                          "vel": round(float(np.clip(0.4 + (np.mean(cur[3]) + 30) / 25, 0.15, 1.0)), 3)})
        cur = [t, m, t + hop, [lv]] if m is not None else None
    return notes


def main(argv):
    a = list(argv)

    def opt(k, d=None):
        if k in a:
            i = a.index(k)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return d

    t0, t1 = opt("--from"), opt("--to")
    if t0 is None or t1 is None:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    t0, t1 = float(t0.rstrip("s")), float(t1.rstrip("s"))
    lo, hi = (int(v) for v in opt("--range", "40-84").split("-"))
    hop = float(opt("--hop", 0.05))
    kw = dict(gate=float(opt("--gate", -40)), a4=float(opt("--a4", 440)), lo=lo, hi=hi, hop=hop,
              harmonics=int(opt("--harmonics", 5)))
    min_len = float(opt("--min-len", 0.08))
    into, track, patch, out = opt("--into"), opt("--track"), opt("--patch"), opt("-o")
    as_json = "--json" in a
    a = [v for v in a if v != "--json"]
    if len(a) != 1:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    notes = notes_of(frames(load(a[0]).astype(np.float64).mean(1), t0, t1, **kw), t1, hop, min_len)
    if not into:
        print(json.dumps(notes) if as_json else "\n".join(f"{n['at']:>10} {n['len']:>8}  {n['pitch']:3d}  vel {n['vel']}" for n in notes))
        return
    if not track or not out:
        raise SystemExit("monotrans: --into SONG needs --track NAME and -o OUT")
    write_into(notes, into, track, patch, t0, t1, out, "monotrans")
    print(f"wrote {out}: {len(notes)} notes in {t0:g}-{t1:g} s on {track}")


if __name__ == "__main__":
    main(sys.argv[1:])
