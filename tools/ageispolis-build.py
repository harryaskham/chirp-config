#!/usr/bin/env python3
"""Emit the checked-in native Ageispolis transcription, byte-exactly.

    python3 tools/ageispolis-build.py > songs/ageispolis.yaml
    python3 tools/ageispolis-build.py --check

Source is native Song JSON, NOT a tab2song map. Original signal analysis and
calibration receipts live in ref/evidence/chirper-one/ageispolis-r1/. No recorded
samples are embedded or loaded by the song. Native note velocities are 0..1.
"""
from pathlib import Path
import json
import math
import sys

HERE = Path(__file__).resolve().parent
source = HERE / "ageispolis-source.json"
raw = source.read_bytes()
song = json.loads(raw)
assert song["meta"] == {
    "artist": "Aphex Twin",
    "album": "Selected Ambient Works 85-92",
    "title": "Ageispolis",
    "track": 4,
    "year": 1992,
}
for track in song["tracks"]:
    for note in track.get("notes", []):
        velocity = float(note.get("vel", 0.8))
        assert math.isfinite(velocity) and 0.0 <= velocity <= 1.0, (track["name"], velocity)
text = json.dumps(song, indent=2, ensure_ascii=True) + "\n"
assert text.encode() == raw, "source formatting changed; review rather than silently rewriting it"
if "--check" in sys.argv[1:]:
    target = HERE.parent / "songs" / "ageispolis.yaml"
    assert target.read_bytes() == raw, "song must equal the authoritative native source"
    print("ageispolis: native source, metadata, velocity ranges and song bytes match")
else:
    sys.stdout.write(text)
