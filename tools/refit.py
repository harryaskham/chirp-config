#!/usr/bin/env python3
"""Re-fit a map's mastering after an instrument or arrangement change: the per-section master EQ (sectioneq.py lanes
auto.eq0..6) and the fader ride (levelride.py lane auto.ride) were fitted to an older mix, so they partly compensate
for instruments that have since changed. Given a render of the map as it stands, add the residual section-EQ fit to
the existing lanes (clamped) and accumulate the ride. Compare candidates only after the same re-fit of the baseline.

  refit.py MAP.json REF.wav RENDER.wav SECTIONS.txt [--only 0,1,2,3,6,7] [--max 9] [--no-ride] [--ride-range A-B]
           [-o OUT.json]

Re-fit only what moved: --only for the section EQ, --ride-range (seconds) for the ride."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mp_path, ref, render, sections = a[:4]
    out = opt("-o", mp_path)
    mx = opt("--max", 9.0)
    mp = json.load(open(mp_path))
    lanes = mp["head"]["master"]["auto"]
    cmd = ["python3", os.path.join(HERE, "sectioneq.py"), ref, render, sections]
    if "--only" in a:
        cmd += ["--only", opt("--only", "")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    resid = json.loads(r.stdout.strip().splitlines()[-1])["auto"]
    moved = []
    for k, lane in resid.items():
        if k not in lanes:
            continue
        old = lanes[k]["points"]
        assert [p[0] for p in old] == [p[0] for p in lane["points"]], f"{k}: lane grids differ"
        lanes[k]["points"] = [[t, round(max(-mx, min(mx, v0 + dv)), 2)] for (t, v0), (_, dv) in zip(old, lane["points"])]
        moved.append(max(abs(dv) for _, dv in lane["points"]))
    print(f"section EQ: residual up to {max(moved):.1f} dB across {len(moved)} bands", file=sys.stderr)
    json.dump(mp, open(out, "w"), indent=1)
    if "--no-ride" not in a:
        before = json.load(open(out))["head"]["master"]["auto"].get("ride")
        r = subprocess.run(["python3", os.path.join(HERE, "levelride.py"), out, ref, render, "--accumulate", "-o", out],
                           capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-400:], file=sys.stderr)
        if "--ride-range" in a and before:
            # keep the accumulated ride only inside A-B seconds; elsewhere the previous lane stands (sections that
            # were already right do not move — Pneuma: a global re-ride cost the intro/interlude what it gave the outro)
            lo, hi = (float(v) for v in opt("--ride-range", "0-1e9").split("-"))
            mp2 = json.load(open(out)); lane = mp2["head"]["master"]["auto"]["ride"]
            old = {p_[0]: p_[1] for p_ in before["points"]}
            lane["points"] = [[t, v if lo <= float(t.rstrip("s")) <= hi else old.get(t, v)] for t, v in lane["points"]]
            json.dump(mp2, open(out, "w"), indent=1)
            print(f"ride kept inside {lo:.0f}-{hi:.0f} s only", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
