#!/usr/bin/env python3
"""Seed-averaged sectioned likeness: render a song at several seeds and report mean ± std, overall and per
section. Within a section, randomness is seeded per track index, so any structural change re-rolls the draws
(±1.5 points of noise per section); compare candidates on these means, not single renders.

  seedscore.py SONG.yaml [--seeds 7,11,13] [--ref ref/shadows.wav] [--sections tools/shadows-sections.txt]"""
import json, os, subprocess, sys
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
from concurrent.futures import ThreadPoolExecutor
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import likeness as L

C = chirpbin.resolve("/tmp/lt/chirp-main/cli/chirp/target/release/chirp")
HERE = os.path.dirname(os.path.abspath(__file__))


def score(song, seeds=(7, 11, 13), ref=None, sections=None):
    ref = ref or os.path.join(HERE, "..", "ref", "shadows.wav")
    bounds = [float(v) for v in open(sections or os.path.join(HERE, "shadows-sections.txt")).read().split(",")]
    tag = os.path.splitext(os.path.basename(song))[0]

    def one(seed):
        out = f"/tmp/seedscore-{os.getpid()}-{tag}-{seed}.wav"   # pid: concurrent masterstacks' held-out renders share tags (best/base)
        r = subprocess.run(["nice", "-n", "15", C, "render", "-f", song, "--seed", str(seed), "-o", out],
                           capture_output=True, text=True, cwd=os.path.join(HERE, "..", "songs"))
        if r.returncode:
            raise SystemExit(r.stderr[-300:])
        d = L.sectioned(ref, out, bounds)
        os.unlink(out)
        return [d["total"]] + [s["total"] for s in d["sections"]]

    with ThreadPoolExecutor(int(os.environ.get("SEEDSCORE_JOBS", "2")) or 2) as ex:   # masterstack --slots sets it
        rows = np.array(list(ex.map(one, seeds)))
    return {"mean": round(float(rows[:, 0].mean()), 2), "std": round(float(rows[:, 0].std()), 2),
            "sections": [round(float(v), 1) for v in rows[:, 1:].mean(0)], "per_seed": rows[:, 0].tolist()}


if __name__ == "__main__":
    a = sys.argv[1:]
    seeds = [int(v) for v in a[a.index("--seeds") + 1].split(",")] if "--seeds" in a else [7, 11, 13]
    ref = a[a.index("--ref") + 1] if "--ref" in a else None
    secs = a[a.index("--sections") + 1] if "--sections" in a else None
    print(json.dumps(score(os.path.abspath(a[0]), seeds, ref, secs)))
