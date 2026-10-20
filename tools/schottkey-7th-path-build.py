#!/usr/bin/env python3
"""Emit the native, sample-free Schottkey 7th Path transcription byte-exactly.

  python3 tools/schottkey-7th-path-build.py > songs/schottkey-7th-path.yaml
  python3 tools/schottkey-7th-path-build.py --check

The source is native Song JSON, not a tab2song map. Analysis and calibration
receipts are in ref/evidence/chirper-one/schottkey-r1/. Velocities are 0..1.
"""
from pathlib import Path
import json
import math
import sys

HERE = Path(__file__).resolve().parent
ID = "schottkey-7th-path"
raw = (HERE / f"{ID}-source.json").read_bytes()
song = json.loads(raw)
assert song["meta"] == {
    "artist": "Aphex Twin",
    "album": "Selected Ambient Works 85-92",
    "title": "Schottkey 7th Path",
    "track": 9,
    "year": 1992,
}
for track in song["tracks"]:
    for note in track.get("notes", []):
        velocity = float(note.get("vel", 0.8))
        assert math.isfinite(velocity) and 0 <= velocity <= 1, (track["name"], velocity)
text = json.dumps(song, indent=2, ensure_ascii=True) + "\n"
assert text.encode() == raw, "review source format changes instead of silently rewriting"
if "--check" in sys.argv[1:]:
    assert (HERE.parent / "songs" / f"{ID}.yaml").read_bytes() == raw
    print(f"{ID}: source, song, metadata and normalized velocity bytes match")
else:
    sys.stdout.write(text)
