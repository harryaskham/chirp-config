#!/usr/bin/env python3
"""share: a track's level against the mix and its share of the mix's power per octave, from fresh window renders.

  share.py songs/ID.yaml '33-36,81-84,92.25-96' voice,duet [--seed 0] [--threads 3]

For each bar window it renders the mix and each named track solo (`--set loudness=null`, so levels are the song's
own; any song format the groove reads) and prints, over the frames the track sounds in:

  on%    the share of the window's 0.4 s frames it sounds in
  lvl    its level against the mix in those frames, dB
  best   its best octave and its share there
  20 .. 5k6   its share of the mix's power in each octave band from 20 Hz to 11 kHz, dB
              (0 = it is the mix there; -6 = a quarter of the band; `.` = under -40 dB or an empty band)

It answers "what of this part reaches the listener, and where": tools/amap.py says whether a track is heard, this
says in which octaves. What it found first (chirper-three, t4 v100): a sung open vowel was the whole mix at
355-1400 Hz and 22 dB under the band from 1.4 to 5.6 kHz - nothing there for an eq to turn up; a `drive` on the
voice's track added the note's own harmonics and took it to -9 dB (compose/chirpers9/mixplan.md).

A solo carries its own reverb and delay returns. Read-only on the song; windows render in a few seconds each.
"""
import argparse
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EDGES = [20, 45, 90, 180, 355, 710, 1400, 2800, 5600, 11025]
NAMES = ["20", "45", "90", "180", "355", "710", "1k4", "2k8", "5k6"]
SR = 32000
FRAME = 0.4


def render(pin, song, a, z, out, seed, threads, solo=None):
    cmd = ["nice", "-n", "6", pin, "render", "-f", os.path.basename(song), "-o", out, "--from", f"{a:g}", "--to",
           f"{z:g}", "--preroll", "8", "--seed", str(seed), "--threads", str(threads), "--set", "loudness=null"]
    if solo:
        cmd += ["--solo", solo]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(song)))
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[-300:])
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", out, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def frames(m):
    n = int(FRAME * SR)
    k = len(m) // n
    fr = m[:k * n].reshape(k, n) * np.hanning(n)
    s = np.abs(np.fft.rfft(fr, axis=1)) ** 2
    f = np.fft.rfftfreq(n, 1 / SR)
    bands = np.stack([s[:, (f >= lo) & (f < hi)].sum(1) for lo, hi in zip(EDGES[:-1], EDGES[1:])], 1)
    return 10 * np.log10((fr ** 2).mean(1) + 1e-20), bands


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("song")
    ap.add_argument("windows", help="bar windows: '33-36,81-84'")
    ap.add_argument("tracks", help="track names: voice,duet")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--threads", type=int, default=3)
    a = ap.parse_args()
    pin = open(os.path.join(HERE, "groove-pin")).read().strip()
    tmp = tempfile.mkdtemp(prefix="share-")
    out = os.path.join(tmp, "x.wav")

    def power(v):
        return 10 * np.log10(np.mean(10 ** (v / 10)) + 1e-12)

    for w in a.windows.split(","):
        lo, hi = (float(x) for x in w.split("-"))
        mdb, mbp = frames(render(pin, a.song, lo, hi, out, a.seed, a.threads))
        if not len(mdb):
            print(f"== bars {lo:g}-{hi:g}: shorter than one {FRAME:g} s frame")
            continue
        print(f"== bars {lo:g}-{hi:g}   {'track':<9}{'on%':>5}{'lvl':>7}{'best':>10}   " + " ".join(f"{n:>5}" for n in NAMES))
        for name in a.tracks.split(","):
            try:
                db, bp = frames(render(pin, a.song, lo, hi, out, a.seed, a.threads, solo=name))
            except RuntimeError as e:
                print(f"   {name:<9} {e}")
                continue
            k = min(len(db), len(mdb))
            db, bp = db[:k], bp[:k]
            if db.max() < -100:
                print(f"   {'':<10}{name:<9} silent")
                continue
            on = db > max(db.max() - 25, -100)
            lvl = power(db[on]) - power(mdb[:k][on])
            mix = mbp[:k][on].mean(0)
            sh = 10 * np.log10(bp[on].mean(0) / (mix + 1e-20) + 1e-12)
            sig = mix > mix.max() * 1e-4
            best = int(np.argmax(np.where(sig, sh, -99)))
            print(f"   {'':<10}{name:<9}{on.mean() * 100:>5.0f}{lvl:>7.1f}{NAMES[best]:>5}{sh[best]:>5.1f}   "
                  + " ".join((f"{x:5.0f}" if s and x > -40 else "    .") for x, s in zip(sh, sig)))
    try:
        os.remove(out)
        os.rmdir(tmp)
    except OSError:
        pass


if __name__ == "__main__":
    main()
