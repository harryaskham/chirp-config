#!/usr/bin/env python3
"""Emit the native, sample-free I harmonic-field guide byte-exactly.

  python3 tools/i-build.py > songs/i.yaml
  python3 tools/i-build.py --check

Native Song JSON, not a tab2song map. All note velocities are normalized0..1;
52sustained inputevents and measured native colour-controller response are
symbolic parameters, not recorded audio. Evidence: ref/evidence/chirper-one/i-r2.
"""
from pathlib import Path
import json
import math
import sys

HERE = Path(__file__).resolve().parent
raw = (HERE / "i-source.json").read_bytes()
song = json.loads(raw)
assert song["meta"] == {
    "artist": "Aphex Twin",
    "album": "Selected Ambient Works 85-92",
    "title": "I",
    "track": 5,
    "year": 1992,
}
notes = [n for t in song["tracks"] for n in t.get("notes", [])]
assert len(notes) == 52
for n in notes:
    velocity = float(n.get("vel", 0.8))
    assert math.isfinite(velocity) and 0 <= velocity <= 1
text = json.dumps(song, indent=2, ensure_ascii=True) + "\n"
assert text.encode() == raw, "review source format instead of silently rewriting it"
if "--check" in sys.argv[1:]:
    assert (HERE.parent / "songs" / "i.yaml").read_bytes() == raw
    print("i: native source, song, metadata and normalized52-note bytes match")
else:
    sys.stdout.write(text)
