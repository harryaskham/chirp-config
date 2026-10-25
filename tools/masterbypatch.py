#!/usr/bin/env python3
"""masterbypatch: which library patches do album masters keep correcting? (chirper-three, 25 Oct: the micro benchmark
found library patches voiced brighter/thinner than the records, with every song's master compensating.)

  masterbypatch.py MASTERAUDIT.json [--min-notes 5] [--min-songs 3] [--threshold 2] [--json OUT]

Reads `masteraudit.py --json` (per-song master correction curves, dB per 1/3-octave, over its render window). For every
song it plans the song (`chirp plan --json`, the groove pin), resolves each track's patch to its LIBRARY patch (a
variant string's first token; a song-local patch through its `extends` chain) and keeps the patches that actually play
in the audit window (>= --min-notes notes). Then per library patch: the songs that use it, and the median of their
curves MINUS the album-wide median (the patch-specific excess, not every master's common tilt). Bands where that excess
is at least --threshold dB and at least 2/3 of the patch's songs agree in sign are listed. A song's master corrects the
whole mix, so this is attribution by co-occurrence, not a measured patch response: confirm a lead with a micro clip.
Read-only (plans only, no renders). Songs built from embedded `songs:` sections (Shadows) are not unpacked yet: they
contribute no patches."""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402


def tpoints(tempo):
    if tempo is None:
        return [(0.0, 120.0)]
    if isinstance(tempo, (int, float)):
        return [(0.0, float(tempo))]
    pts = []
    for t in tempo:
        at = t.get("at", 0)
        b = float(at[:-1]) if isinstance(at, str) and at.endswith("b") else float(at)
        pts.append((b, float(t.get("bpm", 120))))
    pts.sort()
    if pts[0][0] > 0:
        pts.insert(0, (0.0, 120.0))
    return pts


def beat_to_sec(beat, pts):
    s = 0.0
    for i, (b, bpm) in enumerate(pts):
        nb = pts[i + 1][0] if i + 1 < len(pts) else float("inf")
        if beat <= nb:
            return s + (beat - b) * 60 / bpm
        s += (nb - b) * 60 / bpm
    return s


def sec_to_beat(sec, pts):
    s = 0.0
    for i, (b, bpm) in enumerate(pts):
        nb = pts[i + 1][0] if i + 1 < len(pts) else float("inf")
        seg = (nb - b) * 60 / bpm
        if sec <= s + seg:
            return b + (sec - s) * bpm / 60
        s += seg
    return pts[-1][0]


def at_seconds(p, pts, track_at):
    """Seconds of a note position (beats unless s/ms; ramps approximated as steps)."""
    if isinstance(p, (int, float)):
        return beat_to_sec(sec_to_beat(track_at, pts) + float(p), pts)
    m = re.fullmatch(r"(-?[0-9.]+)(ms|s|b)?", str(p).strip())
    if not m:
        return None
    v, u = float(m.group(1)), m.group(2)
    if u == "s":
        return track_at + v
    if u == "ms":
        return track_at + v / 1000
    return beat_to_sec(sec_to_beat(track_at, pts) + v, pts)


LIBRARY = None


def library_names():
    """Patch names in the library (`chirp patch list`): built-in plus the config dir's patches/."""
    global LIBRARY
    if LIBRARY is None:
        p = subprocess.run([chirpbin.resolve("chirp"), "patch", "list"], capture_output=True, text=True)
        LIBRARY = {ln.split()[0] for ln in p.stdout.splitlines() if ln.strip()}
    return LIBRARY


def library_name(patch, local):
    """The library patch a track's patch resolves to: a variant string's first token, a song-local patch through its
    `extends` chain (the canonical plan embeds library patches too, so names are checked against the library list);
    None for inline or unresolvable patches."""
    lib, seen = library_names(), set()
    while isinstance(patch, str):
        name = patch.split()[0]
        if name in lib:
            return name
        if name not in local or name in seen:
            return None
        seen.add(name)
        patch = local[name].get("extends")
    return None


def song_patches(song, frm, to, min_notes):
    p = subprocess.run([chirpbin.resolve("chirp"), "plan", "-f", f"{song}.yaml", "--json"], capture_output=True, text=True,
                       cwd=os.path.join(ROOT, "songs"))
    try:
        c = json.loads(p.stdout[p.stdout.find("{"):])["data"]["canonical"]
    except (ValueError, KeyError):
        return None
    pts, local, used = tpoints(c.get("tempo")), dict(c.get("patches") or {}), {}
    # the canonical plan flattens song-local patches (no `extends`): take the chains from the song source's
    # `patches:` line (flow YAML: one JSON value per top-level key) where it parses
    try:
        for ln in open(os.path.join(ROOT, "songs", f"{song}.yaml")):
            if ln.startswith("patches: "):
                local.update(json.loads(ln[len("patches: "):]))
                break
    except (OSError, ValueError):
        pass
    for t in c.get("tracks") or []:
        lib = library_name(t.get("patch"), local)
        if not lib:
            continue
        ta = t.get("at")
        ta = float(ta[:-1]) if isinstance(ta, str) and ta.endswith("s") and not ta.endswith("ms") else 0.0
        n = 0
        for x in t.get("notes") or []:
            if x.get("pitch") is None:
                continue
            s = at_seconds(x.get("at", 0), pts, ta)
            if s is not None and frm <= s < to:
                n += 1
        if n >= min_notes:
            used[lib] = used.get(lib, 0) + n
    return used


def secs(v):
    v = str(v)
    return float(v[:-1]) if v.endswith("s") else float(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("audit")
    ap.add_argument("--min-notes", type=int, default=5)
    ap.add_argument("--min-songs", type=int, default=3)
    ap.add_argument("--threshold", type=float, default=2.0)
    ap.add_argument("--json")
    a = ap.parse_args()
    d = json.load(open(a.audit))
    centres, frm, to = d["centres"], secs(d["window"][0]), secs(d["window"][1])
    curves = {k: np.array(v) for k, v in d["songs"].items()}
    glob = np.median(np.array(list(curves.values())), 0)
    by = {}
    for song in curves:
        used = song_patches(song, frm, to, a.min_notes)
        if used is None:
            print(f"masterbypatch: {song}: plan failed, skipped", file=sys.stderr)
            continue
        for lib in used:
            by.setdefault(lib, []).append(song)
    out = {}
    for lib, songs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        if len(songs) < a.min_songs:
            continue
        ex = np.array([curves[s] - glob for s in songs])
        med = np.median(ex, 0)
        agree = (np.sign(ex) == np.sign(med)).mean(0)
        hits = [(c, m) for c, m, g in zip(centres, med, agree) if abs(m) >= a.threshold and g >= 2 / 3]
        out[lib] = {"songs": songs, "excess_median": [round(float(v), 2) for v in med],
                    "bands": [[c, round(float(m), 1)] for c, m in hits]}
        print(f"{lib:22s} {len(songs):2d} songs  " + (", ".join(f"{c:g} Hz {m:+.1f}" for c, m in hits) or "no consistent excess"))
    if a.json:
        json.dump({"centres": centres, "window": d["window"], "global_median": [round(float(v), 2) for v in glob],
                   "patches": out}, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
