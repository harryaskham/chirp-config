#!/usr/bin/env python3
"""bounds: compscore's section-boundary novelty peaks for a render, so a boundary sitting on a threshold shows.

  bounds.py WAV... [--floor 0.10] [--album chirpers9]

compscore cuts a song into sections where its checkerboard novelty (frame self-similarity, +-8 s) peaks above a
threshold; an album can score an ensemble of thresholds (album.json params.sections.novelty, Accretion: 0.12-0.18).
A peak that sits near one of them flips a section in or out and moves `recurrence`/`structure` by tenths while the
music barely changes (10 Nov: t6 0.119 -> 0.121 against 0.12; t8's plucks took the 2:08 peak 0.181 -> 0.151 and lost
a section at 0.17 and 0.18; t4 seed 5). This prints every peak (time = height), marks the ones within 0.01 of a
threshold with `*`, and the section count per threshold - compare HEAD's render with the candidate's to see which
boundary moved. What lowers a peak (chirper-three, t8 v100): making a melodic part audible INSIDE the 8 s after a
boundary (frame-wise chroma gets less uniform there); a change that starts exactly on the boundary and HOLDS keeps it.
Read-only; a flashlight, not a score.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compscore as C  # noqa: E402
import likeness as L  # noqa: E402


def main(argv=None):
    from scipy import signal
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("wav", nargs="+")
    ap.add_argument("--floor", type=float, default=0.10, help="list peaks above this height (default 0.10)")
    ap.add_argument("--album", default="chirpers9", help="album whose novelty thresholds to mark (default chirpers9)")
    a = ap.parse_args(argv)
    ths = None
    try:
        album = json.load(open(os.path.join(os.path.dirname(HERE), "compose", a.album, "album.json")))
        ths = C.novelty_thresholds(album)
    except (OSError, ValueError):
        pass
    ths = ths or [C.NOVELTY]
    for p in a.wav:
        x = L.load(p)
        nov = C.novelty(C.frames(L.Feat(x)))
        pk, _ = signal.find_peaks(nov, height=a.floor, distance=16)
        cells = []
        for q in pk:
            edge = "*" if any(abs(nov[q] - t) < 0.01 for t in ths) else ""
            cells.append(f"{int(q / 2) // 60}:{int(q / 2) % 60:02d}={nov[q]:.3f}{edge}")
        print(os.path.basename(p))
        print("   " + "  ".join(cells))
        print("   sections per threshold: " + "  ".join(f"{t:g}:{1 + sum(nov[q] >= t for q in pk)}" for t in ths))


if __name__ == "__main__":
    main()
