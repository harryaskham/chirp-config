#!/usr/bin/env python3
"""gapscan (wM, obZen rhythm; promoted 28 Oct): spans where the record's part plays but ours is silent.

  gapscan.py ID [ID …] [--out FILE.json]

Per family, drums (drum tracks soloed vs the drums stem) and guitar+bass (gtr*/bass* tracks vs the guitar+bass
stems): 0.5 s frames where the stem is at least -32 dBFS while our solo render is under -50 dB, kept when they run
for at least 1 s. Renders with the groove pin, seed 0, against ref/stems/bs_roformer_sw/ID/. This Spiteful Snake:
our drums silent at 150-151.5 and 279.5-285.5 s and our guitars at 286-291 s while the record plays; filling them
won +0.86..+0.91 on every seed (adopted, v18). Prints each family's gaps; --out writes them all as JSON.
Tracks are read with the song loader, so key order doesn't matter (the original regex wanted `name:` first and missed
rngsafe/drumtrans tracks written `{patch: …, name: …}`, e.g. Snake's `drumsr` fill, reporting a filled gap as open).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import likeness as L  # noqa: E402

HOP = 24000                                    # 0.5 s at 48 kHz


def frame_db(x):
    """Level in dB per 0.5 s frame (mean square over the frame and channels)."""
    n = len(x) // HOP
    return 10 * np.log10((x[:n * HOP].reshape(n, HOP, -1) ** 2).mean((1, 2)) + 1e-12)


def gaps(ref, ours, ref_on=-32.0, ours_off=-50.0, min_frames=2):
    """[(start s, end s, the stem's median dB)] where REF >= REF_ON while OURS < OURS_OFF for >= MIN_FRAMES frames."""
    n, out, i = min(len(ours), len(ref)), [], 0
    while i < n:
        if ref[i] >= ref_on and ours[i] < ours_off:
            j = i
            while j < n and ref[j] >= ref_on and ours[j] < ours_off:
                j += 1
            if j - i >= min_frames:
                out.append((round(i * 0.5, 1), round(j * 0.5, 1), round(float(np.median(ref[i:j])), 1)))
            i = j
        else:
            i += 1
    return out


def families(tracks):
    """{family: [track names]} from a song's tracks: drums (a kit patch or a drum* name), guitar+bass (gtr*/bass*)."""
    names = [(t.get("name", ""), t["patch"] if isinstance(t.get("patch"), str) else json.dumps(t.get("patch", "")))
             for t in tracks if t.get("name")]
    return {"drums": [n for n, p in names if "kit" in p or n.startswith("drum")],
            "guitar+bass": [n for n, p in names if n.startswith("gtr") or n.startswith("bass")]}


def render_solo(cid, tracks, out):
    b = open(os.path.join(ROOT, "tools", "groove-pin")).read().strip()
    env = dict(os.environ, RAYON_NUM_THREADS="2")
    env.pop("LD_LIBRARY_PATH", None)
    cmd = ["nice", "-n", "15", b, "render", "-f", f"songs/{cid}.yaml", "--seed", "0", "-o", out]
    for t in tracks:
        cmd += ["--solo", t]
    subprocess.run(cmd, env=env, cwd=ROOT, check=True, capture_output=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--out", default="/tmp/lt/gapscan.json")
    a = ap.parse_args(argv)
    out = {}
    for cid in a.ids:
        import songfmt
        fam = families(songfmt.load(os.path.join(ROOT, "songs", f"{cid}.yaml"))["tracks"])
        st = os.path.join(ROOT, "ref", "stems", "bs_roformer_sw", cid)
        out[cid] = {}
        for f, tracks in fam.items():
            with tempfile.TemporaryDirectory() as td:
                o = os.path.join(td, "o.wav")
                render_solo(cid, tracks, o)
                ours = frame_db(L.load(o))
            ref = 10 * np.log10(sum(10 ** (frame_db(L.load(os.path.join(st, f"{s}.wav"))) / 10) for s in f.split("+")) + 1e-12)
            g = gaps(ref, ours)
            out[cid][f] = {"tracks": tracks, "gaps": g}
            print(cid, f, tracks, "gaps (s, s, stem dB):", g, flush=True)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
