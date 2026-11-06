#!/usr/bin/env python3
"""modlint: modulation amounts in the wrong unit (chirp-eco, 6 Nov). A frequency parameter's mod amount is in OCTAVES
(cutoff=800+lfo.a*2 sweeps two octaves), a gain's in dB; an amount written in Hz (-2600 on a cutoff) slams the
filter shut or open the moment the source moves. chirper-three's t8 horizon light sat at -42.6 dB from v1 to v3 that
way; chirpers4 and chirpers5 carry the same slip (300-19000 "octaves").

  modlint.py [ID|FILE …] [--album NAME] [--octaves 15] [--json]   (default: the focus album's songs)

Reads each song through `chirp plan --json` (the canonical, patches resolved; groove pin) and flags a mod on
cutoff/freq/formant/center/rate whose |amount| > --octaves. The default 15 is the engine's whole range (frequencies
clamp to 1..30000 Hz, 14.9 octaves), so a flag is never musical; deliberate full sweeps (10-11 octaves on a library
filter envelope) pass. Gains are not judged: 60-120 dB envelope fades on layer levels are a library idiom.
Read-only; exits 1 when anything is flagged.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
FREQ = {"cutoff", "freq", "formant", "center", "rate"}


def lint(node, octaves=15.0, path=()):
    """[(path, kind, src, amount)] for frequency mod amounts beyond the engine's whole range (Hz written as octaves)."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            p = path + (str(k),)
            if isinstance(v, dict) and isinstance(v.get("mod"), list) and k in FREQ:
                for m in v["mod"]:
                    a = m.get("amount") if isinstance(m, dict) else None
                    if isinstance(a, (int, float)) and abs(a) > octaves:
                        out.append((".".join(p), "freq", m.get("src"), a))
            out += lint(v, octaves, p)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += lint(v, octaves, path + (str(i),))
    return out


def canonical(pin, song):
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        return None
    return (d.get("data") or d).get("canonical")


def focus_songs(album=None):
    reg = json.load(open(os.path.join(ROOT, "climbs.json")))
    album = album or reg.get("focus")
    out = []
    for c in reg.get("climbs", []):
        if str((c.get("meta") or {}).get("album", "")).casefold() == str(album).casefold():
            p = os.path.join(ROOT, c.get("song") or f"songs/{c['id']}.yaml")
            if os.path.exists(p):
                out.append(p)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("songs", nargs="*", help="climb ids or song files (default: the focus album)")
    ap.add_argument("--album")
    ap.add_argument("--octaves", type=float, default=15.0)
    ap.add_argument("--pin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    songs = [s if os.path.exists(s) else os.path.join(ROOT, "songs", f"{s}.yaml") for s in a.songs] or focus_songs(a.album)
    found, failed = {}, []
    for s in songs:
        c = canonical(pin, s)
        if c is None:
            failed.append(s)
            continue
        hits = lint(c, a.octaves)
        if hits:
            found[os.path.relpath(s, ROOT)] = hits
    if a.json:
        print(json.dumps({"flagged": found, "unplannable": failed, "checked": len(songs)}))
    else:
        for s, hits in found.items():
            for p, _kind, src, amt in hits:
                print(f"{s}: {p}  src {src}  amount {amt:g} octaves (beyond the 14.9-octave range: written in Hz?)")
        print(f"modlint: {len(songs)} song(s), {sum(len(h) for h in found.values())} flag(s)"
              + (f", {len(failed)} did not plan: {', '.join(failed)}" if failed else ""))
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
