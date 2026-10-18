#!/usr/bin/env python3
"""Does a vocal read as a voice? Render one track solo, separate it with Demucs htdemucs_6s and report each stem's
share of the energy (bd-f227d8). A real voice — the record's own vocal stem, re-separated — lands ~100% in
"vocals"; a harsh synthetic voice that leaks into "drums" (broadband, percussive bursts) or "other" (buzzy,
synth-like steady state) does not read as a voice to a listener either.

  vocaltest.py SONG TRACK [--from 168s --to 208s] [--set PATH=VALUE …] [--seed N] [--jobs 1] [--shifts N] [--keep DIR] [--json]
  vocaltest.py --wav FILE.wav [--jobs 1] [--shifts N] [--keep DIR] [--json]   # analysis only

--set is passed to `chirp render` (e.g. --set 'tracks.11.patch=kidman synth.layers.0.scream=0'), so voice-layer
ablations need no patch edits. CHIRP picks the binary. Separation runs on CPU at nice 15 (about a minute per 40 s).
--seed picks the synth render's seed (not the separator's); omitted keeps chirp's default.
--jobs defaults to 1; --shifts 0 disables Demucs random-shift averaging for repeatable paired diagnostics
(omit it to retain the model's normal default). Temporary renders/stems are deleted even on failure unless
--keep DIR is explicit; use ref/evidence/... for durable evidence. A supplied --wav input is never deleted.
"""
import json
import os
import shutil
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
          "--with", "demucs", "--with", "soundfile", "python", "-m", "demucs", "-n", "htdemucs_6s", "-d", "cpu", "-j", "1"]


def shares(wav, work, jobs=1, shifts=None):
    if jobs < 1 or (shifts is not None and shifts < 0):
        raise ValueError("jobs must be positive and shifts non-negative")
    cmd = list(DEMUCS)
    for flag, value in (("-j", jobs), ("--shifts", shifts)):
        if value is None:
            continue
        if flag in cmd:
            cmd[cmd.index(flag) + 1] = str(value)
        else:
            cmd += [flag, str(value)]
    base = os.path.join(work, "htdemucs_6s", os.path.splitext(os.path.basename(wav))[0])
    if any(os.path.realpath(wav) == os.path.realpath(os.path.join(base, s + ".wav")) for s in STEMS):
        raise SystemExit("separation output would overwrite --wav input; choose a different --keep directory")
    env = dict(os.environ, SSL_CERT_FILE=os.environ.get("SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt"))
    r = subprocess.run(["nice", "-n", "15"] + cmd + ["--out", work, wav], capture_output=True, text=True, env=env)
    if r.returncode:
        raise SystemExit(f"demucs failed: {r.stderr[-600:]}")
    e = {s: float((L.load(os.path.join(base, f"{s}.wav")) ** 2).sum()) for s in STEMS}
    tot = sum(e.values()) or 1.0
    return {s: round(100 * v / tot, 1) for s, v in e.items()}


def main(a):
    js = "--json" in a

    def opt(k, default=None):
        if k not in a:
            return default
        i = a.index(k) + 1
        if i >= len(a) or a[i].startswith("--"):
            raise SystemExit(f"{k} needs a value")
        return a[i]

    try:
        jobs = int(opt("--jobs", "1"))
        shifts = int(opt("--shifts")) if "--shifts" in a else None
        seed = int(opt("--seed")) if "--seed" in a else None
    except (ValueError, TypeError):
        raise SystemExit("--jobs, --shifts and --seed need integer values") from None
    if jobs < 1 or (shifts is not None and shifts < 0):
        raise SystemExit("--jobs must be positive and --shifts non-negative")
    if seed is not None and not 0 <= seed < 2**64:
        raise SystemExit("--seed must be an unsigned 64-bit integer")
    keep = opt("--keep")
    work = keep or tempfile.mkdtemp(prefix="vocaltest-")
    os.makedirs(work, exist_ok=True)
    try:
        if "--wav" in a:
            wav = opt("--wav")
        else:
            value_flags = ("--from", "--to", "--set", "--keep", "--jobs", "--shifts", "--seed")
            pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in value_flags)]
            if len(pos) < 2:
                raise SystemExit(__doc__)
            song, track = pos[:2]
            wav = os.path.join(work, f"vox-{os.getpid()}.wav")
            cmd = ["nice", "-n", "15", C, "render", "-f", song, "--solo", track, "-o", wav]
            for k in ("--from", "--to"):
                if k in a:
                    cmd += [k, opt(k)]
            if seed is not None:
                cmd += ["--seed", str(seed)]
            for i, x in enumerate(a):
                if x == "--set":
                    if i + 1 >= len(a) or a[i + 1].startswith("--"):
                        raise SystemExit("--set needs a value")
                    cmd += ["--set", a[i + 1]]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"render failed: {r.stderr[-600:]}")
        sh = shares(wav, work, jobs=jobs, shifts=shifts)
        if js:
            print(json.dumps(sh))
        else:
            print("  ".join(f"{s} {v:5.1f}%" for s, v in sh.items()))
    finally:
        if not keep:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv[1:])
