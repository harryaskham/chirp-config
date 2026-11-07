#!/usr/bin/env python3
"""flatness: how much of a render is "flat" - long stretches where nothing changes (chirp-eco, 6 Nov).

Harry, 6 Nov 23:55: "lots of contiguous music with very little change or dynamism ... we shouldnt be schizo about it
but we should add subtle variation so it doesnt get boring".

  flatness.py FILE... [--block 8] [--threshold 0.691] [--json]     FILE: any audio ffmpeg reads (wav, mp3, opus)

The song is cut into BLOCK-second blocks; each block is summarised by its 16-band log spectrum (shape, level removed),
its chroma and its level; "change" is the distance from one block to the next. A change below THRESHOLD is flat.
THRESHOLD is ABSOLUTE, not relative to the song: 0.691 is the 25th percentile of Standby Amber's own changes (the
released chirpers8 album, the one section climbs loosened up), so "flat" means "as still as Standby Amber's quietest
quarter". Standby Amber: 25% flat on average, longest flat run 29 s on average (8 to 72 s).
Reported: flat %, longest flat run, and every run of 32 s or more (the places to aim a section round). A flashlight,
not a score: a held breath before a drop is meant to be still; a minute and a half of the same loop is not.

WHAT IT SEES AND DOESN'T (7 Nov, after chirper-one found surface moves barely moved it): it compares 8 s blocks, so a
move counts when it HOLDS for a block or more - hats thinning for a phrase, an octave lift, a re-voicing, a drop-out
of a phrase, a new counter-line. A one-bar drop-out or a fill inside a block barely registers (tested on a synthetic
loop: per-phrase hat thinning and octave shifts register, a one-bar kick drop-out does not; onset-band and
within-block-spread features and 4 s blocks did not fix that without destabilising the album comparison). So don't
chase the number with chord changes (tone is home): brief fills and drop-outs are real variation the ear hears even
when this misses them. Use it to find the long ruts and to see a phrase-level move landed; let the ear judge the rest.
Composers' findings, 7 Nov: the measure is dominated by the LOUDEST, LOWEST layer (chroma is power-weighted and the
bass carries the level). Moves above a steady bass - hats to eighths, arps up an octave, all drums out, a clarinet
counter-line at -7 to -12 dB - barely register (chirper-two t3, chirper-three t4); re-orchestrating the loudest element
or moving the floor does. So a quiet counter-line can be exactly the subtle variation Harry asked for and still read flat
here. And a floor drop-out that never returns reads as a new section to compscore's recurrence (t3: 91.8 -> ~50).
"""
import argparse
import json
import subprocess
import sys

import numpy as np

SR = 22050
THRESHOLD = 0.691            # Standby Amber's 25th percentile of 8 s block-to-block change
SA_FLAT, SA_RUN = 25, 29     # Standby Amber means: % flat, longest flat run (s)


def load(path):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True).stdout
    return np.frombuffer(b, dtype=np.float32)


def features(x, hop_s=1.0):
    """One vector per second: band-spectrum shape, chroma (x4) and level/10."""
    n = int(SR * hop_s)
    win = np.hanning(4096)
    freqs = np.fft.rfftfreq(4096, 1 / SR)
    edges = np.geomspace(40, 10000, 17)
    pc = (np.round(12 * np.log2(np.maximum(freqs, 1) / 440.0)) % 12).astype(int)
    mid = (freqs > 60) & (freqs < 4000)
    out = []
    for i in range(len(x) // n):
        seg = x[i * n:(i + 1) * n]
        specs = [np.abs(np.fft.rfft(seg[j:j + 4096] * win)) for j in range(0, len(seg) - 4096, 2048)]
        S = np.mean(specs, axis=0) if specs else np.zeros(len(freqs))
        lb = np.log10(np.array([S[(freqs >= a) & (freqs < b)].sum() for a, b in zip(edges[:-1], edges[1:])]) + 1e-9)
        ch = np.bincount(pc[mid], weights=S[mid] ** 2, minlength=12)
        ch = ch / (ch.sum() + 1e-12)
        rms = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
        out.append(np.concatenate([lb - lb.mean(), ch * 4, [rms / 10]]))
    return np.array(out)


def changes(F, block=8):
    nb = len(F) // block
    if nb < 2:
        return np.zeros(0)
    B = np.array([F[i * block:(i + 1) * block].mean(0) for i in range(nb)])
    return np.linalg.norm(np.diff(B, axis=0), axis=1)


def runs(ch, block=8, threshold=THRESHOLD, min_s=32):
    """(flat %, longest flat run in s, [(start_s, end_s)] runs of min_s or more). A flat change between blocks i and
    i+1 makes both blocks part of the run."""
    flat = ch < threshold
    found, best, start = [], 0, None
    for i, f in enumerate(list(flat) + [False]):
        if f and start is None:
            start = i
        if not f and start is not None:
            a, b = start * block, (i + 1) * block
            best = max(best, b - a)
            if b - a >= min_s:
                found.append((a, b))
            start = None
    pct = 100.0 * float(flat.mean()) if len(flat) else 0.0
    return pct, best, found


def mmss(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("files", nargs="+")
    p.add_argument("--block", type=int, default=8)
    p.add_argument("--threshold", type=float, default=THRESHOLD)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    res = []
    for f in a.files:
        ch = changes(features(load(f)), a.block)
        pct, best, found = runs(ch, a.block, a.threshold)
        res.append({"file": f, "flat_pct": round(pct, 1), "longest_s": best, "runs": found,
                    "median_change": round(float(np.median(ch)), 3) if len(ch) else None})
    if a.json:
        json.dump(res, sys.stdout, indent=1)
        print()
        return
    for r in res:
        print(f"{r['file']}: {r['flat_pct']:.0f}% flat (Standby Amber {SA_FLAT}%), longest flat run {r['longest_s']} s "
              f"(SA {SA_RUN} s)")
        for x, y in r["runs"]:
            print(f"    flat {mmss(x)}-{mmss(y)} ({y - x} s)")


if __name__ == "__main__":
    main()
