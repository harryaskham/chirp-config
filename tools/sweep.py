#!/usr/bin/env python3
"""Render one section of a song under candidate overrides and score each against the matching span
of the reference (tools/likeness.py), best first.

  sweep.py SONG SECTION BEATS REF_START REF_END 'label=--set PATH=V --def N=P …' …

Each candidate is `label=ARGS` (ARGS: chirp render flags, shell-split). `base=` is the unmodified
section. Renders run at low priority, two at a time."""
import json, os, shlex, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
import likeness

C = os.environ.get("CHIRP", "/home/harry/.herdr/worktrees/tools/chirp/cli/chirp/target/release/chirp")
REF = os.path.expanduser("~/.config/chirp/ref/shadows.wav")


def run(song, section, beats, rs, re_, label, args):
    out = f"/tmp/lt/sweep-{section}-{label}.wav"
    cmd = ["nice", "-n", "15", C, "render", "-s", song, "--set", f"tracks.0.score=@{section}/{beats}b", *shlex.split(args), "-o", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        return label, {"error": r.stderr.strip()[-200:]}
    return label, likeness.compare(REF, out, ref_start=rs, ref_end=re_)


if __name__ == "__main__":
    song, section, beats, rs, re_ = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
    cands = [c.split("=", 1) for c in sys.argv[6:]]
    with ThreadPoolExecutor(2) as ex:
        res = list(ex.map(lambda c: run(song, section, beats, rs, re_, c[0], c[1]), cands))
    res.sort(key=lambda t: -t[1].get("total", -1))
    for label, d in res:
        if "error" in d:
            print(f"{label:24s} ERROR {d['error']}"); continue
        print(f"{label:24s} total {d['total']:5.1f}  loud {d['loudness']:5.1f} spec {d['spectral']:5.1f} chroma {d['chroma']:5.1f} rhythm {d['rhythm']:5.1f} ltas {d['ltas']:5.1f}")
