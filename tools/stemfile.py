#!/usr/bin/env python3
"""stemfile: a record's separated stem, whatever format it is stored in.

The stems under ref/stems/MODEL/ID/ were written as WAV, and the tools that read them ask for PART.wav. On 5 Nov the
htdemucs_6s stems were packed to Opus to give the disk back (134 records; the eleven Meshuggah records under
bs_roformer_sw are still WAV), and since then those tools have said "no stem" for a record whose stems are all there
(chirper-zero, 12 Nov: riffpunch on Pneuma for Common Time's mid-gain bench).

  import stemfile
  p = stemfile.find(ROOT, "pneuma", "guitar", ("bs_roformer_sw", "htdemucs_6s"))   # a path, or None
  x = stemfile.load(p)                                                              # as likeness.load: stereo float32, 48 kHz

find looks for a WAV in every model first, in the order given, and only then for another format, so a record that has a
WAV anywhere reads exactly the file it read before. load hands WAV to likeness.load untouched and decodes anything else
with ffmpeg. A packed stem is lossy (Opus at ~160 kb/s here: full band, the level within a few hundredths of a dB), and
the tool says so once on stderr, so a number taken against one is known for what it is.
(chirp-eco, 12 Nov; tests: tools/tests/test_stemfile.py.)"""
import os
import subprocess
import sys

import numpy as np

EXTS = (".wav", ".flac", ".opus", ".ogg", ".m4a", ".mp3")
LOSSY = (".opus", ".ogg", ".m4a", ".mp3")
_said = set()


def find(root, song, part, models=("bs_roformer_sw", "htdemucs_6s")):
    """The stem's file: a WAV under any of the models first (in their order), else another format; None without one."""
    for exts in ((".wav",), EXTS[1:]):
        for model in models:
            for ext in exts:
                p = os.path.join(root, "ref", "stems", model, song, part + ext)
                if os.path.isfile(p):
                    return p
    return None


def has(root, song, part, models=("bs_roformer_sw", "htdemucs_6s")):
    return find(root, song, part, models) is not None


def lossy(path):
    return os.path.splitext(path)[1].lower() in LOSSY


def load(path, quiet=False):
    """Stereo float32 at 48 kHz, as likeness.load gives: a WAV through likeness.load itself, anything else by ffmpeg."""
    import likeness
    if os.path.splitext(path)[1].lower() == ".wav":
        return likeness.load(path)
    if lossy(path) and not quiet and path not in _said:
        _said.add(path)
        print(f"stemfile: {os.path.relpath(path)} is a packed (lossy) stem; decoded with ffmpeg", file=sys.stderr)
    r = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(likeness.SR), "-"],
                       capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"stemfile: ffmpeg could not decode {path}: {r.stderr.decode(errors='replace').strip()[-200:]}")
    return np.frombuffer(r.stdout, dtype="<f4").reshape(-1, 2).copy()
