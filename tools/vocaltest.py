#!/usr/bin/env python3
"""Does a vocal read as a voice? Render one track solo, separate it with Demucs htdemucs_6s and report each stem's
share of the energy (bd-f227d8). A real voice — the record's own vocal stem, re-separated — lands ~100% in
"vocals"; a harsh synthetic voice that leaks into "drums" (broadband, percussive bursts) or "other" (buzzy,
synth-like steady state) does not read as a voice to a listener either.

  vocaltest.py SONG TRACK [--from 168s --to 208s] [--set PATH=VALUE …] [--keep DIR] [--json]
  vocaltest.py --wav FILE.wav [--json]                   # a given recording (e.g. a reference vocal stem)

--set is passed to `chirp render` (e.g. --set 'tracks.11.patch=kidman synth.layers.0.scream=0'), so voice-layer
ablations need no patch edits. CHIRP picks the binary. Separation runs on CPU at nice 15 (about a minute per 40 s).
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

C = os.environ.get("CHIRP", "chirp")
STEMS = ("vocals", "drums", "bass", "guitar", "piano", "other")
DEMUCS = ["uv", "run", "-q", "--python", "3.11", "--index", "https://download.pytorch.org/whl/cpu",
          "--index-strategy", "unsafe-best-match", "--with", "torch==2.5.1", "--with", "torchaudio==2.5.1",
          "--with", "demucs", "--with", "soundfile", "python", "-m", "demucs", "-n", "htdemucs_6s", "-d", "cpu", "-j", "2"]


def shares(wav, work):
    env = dict(os.environ, SSL_CERT_FILE=os.environ.get("SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt"))
    r = subprocess.run(["nice", "-n", "15"] + DEMUCS + ["--out", work, wav], capture_output=True, text=True, env=env)
    if r.returncode:
        raise SystemExit(f"demucs failed: {r.stderr[-600:]}")
    base = os.path.join(work, "htdemucs_6s", os.path.splitext(os.path.basename(wav))[0])
    e = {s: float((L.load(os.path.join(base, f"{s}.wav")) ** 2).sum()) for s in STEMS}
    tot = sum(e.values()) or 1.0
    return {s: round(100 * v / tot, 1) for s, v in e.items()}


def main(a):
    js = "--json" in a
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d  # noqa: E731
    keep = opt("--keep")
    work = keep or tempfile.mkdtemp(prefix="vocaltest-")
    os.makedirs(work, exist_ok=True)
    if "--wav" in a:
        wav = opt("--wav")
    else:
        pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--from", "--to", "--set", "--keep"))]
        if len(pos) < 2:
            raise SystemExit(__doc__)
        song, track = pos[:2]
        wav = os.path.join(work, f"vox-{os.getpid()}.wav")
        cmd = ["nice", "-n", "15", C, "render", "-f", song, "--solo", track, "-o", wav]
        for k in ("--from", "--to"):
            if k in a:
                cmd += [k, opt(k)]
        for i, x in enumerate(a):
            if x == "--set":
                cmd += ["--set", a[i + 1]]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"render failed: {r.stderr[-600:]}")
    sh = shares(wav, work)
    if js:
        print(json.dumps(sh))
    else:
        print("  ".join(f"{s} {v:5.1f}%" for s, v in sh.items()))


if __name__ == "__main__":
    main(sys.argv[1:])
