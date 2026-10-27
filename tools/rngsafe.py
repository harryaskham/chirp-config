#!/usr/bin/env python3
"""rngsafe: an RNG-safe passage replacement (chirper-zero's method, chirper-one's script, promoted).

  rngsafe.py ID PREFIX TAG A B PARTS SUBST_JSON [--dir DIR]

Changing notes inside a track rerolls that track's later random draws (humanize and the track-local voice ordinal in
DSP seeds), which confounds an A/B. So instead of editing the map's PARTS in place, this renders those parts restricted
to bars A..B, with extra substitutions SUBST_JSON (a JSON list of [from, to] note pairs, applied as map `subst` over
A..B), through tab2song as NEW tracks named `<part>r` (copying the original's patch, pan, gain, sends and fx),
appends them LAST to the current song (so no existing draw moves), and mutes the originals over that span with a
-60 dB gain lane (auto.mx). Writes DIR/PREFIX-TAG.json (the candidate song, JSON) plus its intermediates; compare it
with an RNG-safe control (the same with SUBST_JSON [] ) on paired seeds. DIR defaults to /tmp/lt/rngsafe.
The engine's opt-in alternative is play.event_stable on BOTH arms (skill: bd-de8443), which rerolls the baseline once.
"""
import argparse
import copy
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))


def span(m, a, b):
    """(t0, t1) seconds of bars A..B on the map's performed clock (plus the map offset)."""
    import tab2song as T
    cache = m["cache"] if m["cache"].startswith("/") else os.path.join(ROOT, m["cache"])
    tl = T.performed_timeline(cache, m)
    st = [x["start"] for x in tl if a <= x["m"] <= b]
    en = [x["start"] + 60 * x["beats"] / x["bpm"] for x in tl if a <= x["m"] <= b]
    return min(st) + m.get("offset", 0), max(en) + m.get("offset", 0)


def replacement_map(m, parts, a, b, subs):
    """The map with only PARTS, renamed `<part>r`, restricted to bars A..B with SUBS added to their subst."""
    mm = copy.deepcopy(m)
    new = []
    for p in m["parts"]:
        if p["name"] in parts:
            q = copy.deepcopy(p)
            q["name"] = p["name"] + "r"
            q["bars"] = [[a, b]]
            q["subst"] = q.get("subst", []) + [[a, b, f, t] for f, t in subs]
            new.append(q)
    mm["parts"] = new
    return mm


def splice(cur, rep, parts, t0, t1):
    """CUR (the song, JSON) with PARTS muted over t0..t1 by an auto.mx gain lane and REP's tracks appended last, each
    taking its original's patch/pan/gain/sends and fx (minus the mute)."""
    d = copy.deepcopy(cur)
    for t in d["tracks"]:
        if t["name"] in parts:
            t.setdefault("auto", {})["mx"] = {"points": [["0s", 0], [f"{t0 - 0.05:.3f}s", 0], [f"{t0:.3f}s", -60],
                                                         [f"{t1:.3f}s", -60], [f"{t1 + 0.05:.3f}s", 0]]}
            t.setdefault("fx", []).append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.mx", "amount": 1}]}})
    for t in rep["tracks"]:
        src = next(x for x in d["tracks"] if x["name"] == t["name"][:-1])
        n = copy.deepcopy(t)
        for k in ("patch", "pan", "gain", "sends"):
            if k in src:
                n[k] = copy.deepcopy(src[k])
        n["fx"] = [f for f in copy.deepcopy(src.get("fx", [])) if not (isinstance(f, dict) and "auto.mx" in json.dumps(f))]
        if isinstance(n.get("gain"), dict):
            n["gain"] = n["gain"].get("value", "0dB")
        d["tracks"].append(n)
    return d


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for k in ("id", "prefix", "tag"):
        ap.add_argument(k)
    ap.add_argument("a", type=int)
    ap.add_argument("b", type=int)
    ap.add_argument("parts")
    ap.add_argument("subst")
    ap.add_argument("--dir", default="/tmp/lt/rngsafe")
    a = ap.parse_args(argv)
    os.makedirs(a.dir, exist_ok=True)
    parts, subs = a.parts.split(","), json.loads(a.subst)
    m = json.load(open(os.path.join(ROOT, "tools", "maps", f"{a.id}.json")))
    t0, t1 = span(m, a.a, a.b)
    mapf = os.path.join(a.dir, f"{a.id}-rs-{a.tag}.json")
    json.dump(replacement_map(m, parts, a.a, a.b, subs), open(mapf, "w"), indent=1)
    yml, repj, curj = (os.path.join(a.dir, f"{a.prefix}-rs-{a.tag}.yaml"), os.path.join(a.dir, f"{a.prefix}-rs-{a.tag}.json"),
                       os.path.join(a.dir, f"{a.prefix}-rscur.json"))
    for cmd in (["python3", "tools/tab2song.py", mapf, "-o", yml], ["python3", "tools/songfmt.py", "json", yml, "-o", repj],
                ["python3", "tools/songfmt.py", "json", f"songs/{a.id}.yaml", "-o", curj]):
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"rngsafe: {' '.join(cmd[:2])} failed: {r.stderr.strip()[-300:]}")
    d = splice(json.load(open(curj)), json.load(open(repj)), parts, t0, t1)
    json.dump(d, open(os.path.join(a.dir, f"{a.prefix}-{a.tag}.json"), "w"), indent=1)
    rep = json.load(open(repj))
    print(a.id, a.tag, "span %.2f-%.2f" % (t0, t1), [t["name"] for t in rep["tracks"]])


if __name__ == "__main__":
    main()
