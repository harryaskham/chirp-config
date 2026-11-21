#!/usr/bin/env python3
"""try.py STUDY OUT.yaml [key=value ...] TRACK...: one study as a one-scene programme, to look at."""
import sys, json
import studies as S
study, out = sys.argv[1], sys.argv[2]
kw = dict(a.split("=", 1) for a in sys.argv[3:] if "=" in a)
tracks = [a for a in sys.argv[3:] if "=" not in a]
spot = kw.pop("spot", "#ff5a2a")
look = getattr(S, study)(tracks, spot, kw.pop("spot_track", tracks[-1]), **kw)
open(out, "w").write(json.dumps({"scenes": [{"at": 0, "look": look}]}, indent=1))
