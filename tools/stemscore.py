#!/usr/bin/env python3
"""Per-stem likeness: render each instrument group of a song soloed and score it (sectioned, duration-weighted)
against the matching stem of the reference (Demucs htdemucs_6s: drums, bass, guitar, vocals, piano, other).
The weakest group/component is the biggest instrument gap — a much sharper signal than the full-mix score.

  stemscore.py SONG.yaml STEMS_DIR SECTIONS.txt GROUP=STEM:TRACK[,TRACK…] [GROUP=…] [--keep DIR]

e.g. stemscore.py songs/pneuma.yaml ref/stems/htdemucs_6s/pneuma tools/pneuma-sections.txt \\
       drums=drums:kit bass=bass:bass,bassfx guitar=guitar:gtr,xgtr vocals=vocals:vox keys=piano:synth,pads"""
import json
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

C = chirpbin.resolve("/tmp/lt/chirp-main/cli/chirp/target/release/chirp")
KEYS = ("loudness", "spectral", "chroma", "rhythm", "ltas", "stereo")


def run(song, stems, sections, groups, keep=None):
    bounds = [float(v) for v in open(sections).read().split(",")]
    tag = os.path.splitext(os.path.basename(song))[0]

    def one(g):
        name, (stem, tracks) = g
        out = os.path.join(keep or "/tmp", f"stemscore-{tag}-{name}.wav")
        cmd = ["nice", "-n", "15", C, "render", "-f", song, "-o", out]
        for t in tracks:
            cmd += ["--solo", t]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            return name, {"error": r.stderr[-300:]}
        d = L.sectioned(os.path.join(stems, f"{stem}.wav"), out, bounds)
        if not keep:
            os.unlink(out)
        secs = d["sections"]
        w = [s["end"] - s["start"] if "end" in s else 1.0 for s in secs]
        comp = {k: round(sum(s[k] * wi for s, wi in zip(secs, w)) / sum(w), 1) for k in KEYS}
        return name, {"total": d["total"], "sections": [round(s["total"], 1) for s in secs], **comp}

    with ThreadPoolExecutor(2) as ex:
        return dict(ex.map(one, groups.items()))


if __name__ == "__main__":
    a = sys.argv[1:]
    keep = a[a.index("--keep") + 1] if "--keep" in a else None
    groups = {}
    for g in a[3:]:
        if g.startswith("--") or (keep and g == keep):
            continue
        name, rest = g.split("=", 1)
        stem, tracks = rest.split(":", 1)
        groups[name] = (stem, tracks.split(","))
    res = run(a[0], a[1], a[2], groups, keep)
    for name, r in sorted(res.items(), key=lambda kv: kv[1].get("total", 0)):
        if "error" in r:
            print(f"{name:8s} ERROR {r['error']}")
            continue
        print(f"{name:8s} {r['total']:5.1f} | " + " ".join(f"{k} {r[k]:5.1f}" for k in KEYS) + f" | sections {r['sections']}")
    print(json.dumps(res))
