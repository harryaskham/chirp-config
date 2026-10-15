#!/usr/bin/env python3
"""Songsterr tab → an explicit chirp song: one track per *part*, each part a tab track over chosen bar ranges
with its own patch (so one tab track can be a rhythm rig in the riffs, a clean rig in a bridge and a lead rig in
a solo). The output is plain notation — every bar written out, repeated bars collapsed to `[…]xN`, bar lines as
` | ` — a transcription aid to hand-edit, never a runtime dependency.

  tab2song.py MAP.json [-o OUT.yaml]

MAP.json:
  {"cache": "ref/songsterr-23825",          # a songsterr.py cache
   "offset": 0.396,                          # seconds of silence before bar 1 (align with the recording)
   "name": "bleed", "about": "…",
   "head": {…},                              # extra top-level song keys (master, buses, ceiling, …) copied verbatim
   "parts": [
     {"name": "gtr-l", "track": 2, "patch": "m8-chug-l", "bars": [[1, 212]], "pan": -0.8, "gain": "-3dB",
      "remap": {"t3": "ft"}, "drop": ["m98"], "extra": {…}}    # extra: more track keys, verbatim
   ]}

A part with "raw": "FILE.json#key" (or a text file) takes its score verbatim — e.g. tools/drumtrans.py output on
the same tempo map. A part's "chord": "low" keeps only the lowest note of every chord (a root/pedal layer), "upper" keeps the rest
(double-stops split into two parts with their own level and tone); single notes stay with "low".
Corrections measured against the recording (tools/scorealign.py): "bpm": {"37": 113.5, …} sets the tempo from
measure M on (until the next entry; earlier measures keep the tab's tempo), and "skip": [[285, 288], …] removes
measures the recording does not play (from the timeline and every part).
A tab with tempo changes becomes a song with a tempo map (a point at every tempo or meter change); "meters": true
emits the map for a constant-tempo tab too. A part may take `"score_file": "PATH"` instead of `track`: `bar N  tokens` lines (stemvox.py/stemnotes.py
output) on the tab's measure numbers, with optional `"rest": [[a, b], …]` ranges kept silent.

Bars are 1-based inclusive ranges. Outside its ranges a part rests. Drum pieces can be renamed (`remap`) or
dropped (`drop`) per part, for kits that name pieces differently from the tab's General-MIDI mapping.
"strip": ["ph", "bend", …] (map-wide or per part) removes those `^articulation` marks ("bend": the bend= tokens) from tab-derived parts (e.g. pinch
harmonics whose rung partial does not match the record's)."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import songsterr as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import tabtime as T  # noqa: E402


def fmt_beats(b):
    s = f"{b:.4f}".rstrip("0").rstrip(".")
    return f"R/{s}b"


def remap_drums(line, remap, drop):
    out = []
    for tok in line.split():
        body, _, rest = tok.partition("/")
        if body == "R":
            out.append(tok); continue
        pcs = [remap.get(p, p) for p in body.split(",") if p not in drop]
        out.append(f"{','.join(dict.fromkeys(pcs))}/{rest}" if pcs else f"R/{rest.split('@')[0]}")
    return " ".join(out)


DUR = re.compile(r"/([0-9]*\.?[0-9]+)b")


def fit_bar(line, want):
    """Scale a bar's durations so they sum to its signature length. Tabs often carry incomplete or overfull
    measures (loose tuplets, grace notes); concatenated as written they drift every later bar against the
    recording. Returns (line, actual_beats)."""
    durs = [float(m.group(1)) for m in DUR.finditer(line)]
    have = sum(durs)
    if not durs or abs(have - want) < 1e-4:
        return line, have
    k = want / have
    new = [round(d * k, 4) for d in durs]
    new[-1] = round(new[-1] + (want - sum(new)), 4)
    it = iter(new)
    return DUR.sub(lambda m: "/" + f"{next(it):.4f}".rstrip("0").rstrip(".") + "b", line), have


FITTED = []


NOTE_RE = re.compile(r"^([A-Ga-g][#sb]?-?\d)$")


def split_chords(line, mode):
    """Keep the lowest note of each chord ("low") or the notes above it ("upper"); chordless notes stay in
    "low" and rest in "upper"."""
    def key(n):
        m = re.match(r"([A-Ga-g])([#sb]?)(-?\d+)", n)
        base = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}[m.group(1).lower()]
        acc = {"#": 1, "s": 1, "b": -1}.get(m.group(2), 0)
        return int(m.group(3)) * 12 + base + acc
    out = []
    for tok in line.split():
        m = re.match(r"^([^/]+)(/.*)$", tok)
        if not m or m.group(1) in ("R", "r", "_", "-", ".") or "=" in tok:
            out.append(tok); continue
        notes = m.group(1).split(",")
        if not all(NOTE_RE.match(n) for n in notes):
            out.append(tok); continue
        notes.sort(key=key)
        keep = notes[:1] if mode == "low" else notes[1:]
        if keep:
            out.append(",".join(keep) + m.group(2))
        else:   # nothing above the root: a rest of the same length (articulations dropped)
            out.append("R" + re.sub(r"^(/[^@^]*).*$", r"\1", m.group(2)))
    return " ".join(out)


RING_TOK = re.compile(r"^([^/]+)/([0-9.]+)b(.*)$")


def ring_bar(line, max_beats):
    """Let notes ring through the rests that follow them (up to max_beats), as a guitarist or bassist lets a
    chord sustain where a tab writes short notes and rests. Muted/dead/staccato notes stay short; the bar's
    timing is unchanged (each rest shrinks by what the note before it takes)."""
    toks = line.split()
    out, i = [], 0
    while i < len(toks):
        m = RING_TOK.match(toks[i])
        if not m or m.group(1) == "R" or any(a in m.group(3) for a in ("^pm", "^dead", "^stac")):
            out.append(toks[i]); i += 1; continue
        head, dur, tail = m.group(1), float(m.group(2)), m.group(3)
        take, j, left = 0.0, i + 1, max_beats
        rests = []
        while j < len(toks) and left > 1e-9:
            r = RING_TOK.match(toks[j])
            if not r or r.group(1) != "R" or r.group(3):
                break
            rb = float(r.group(2)); t = min(rb, left)
            take += t; left -= t
            if rb - t > 1e-6:
                rests.append(fmt_beats(rb - t))
                j += 1
                break
            j += 1
        out.append(f"{head}/{fmt_num(dur + take)}b{tail}")
        out.extend(rests)
        i = j
    return " ".join(out)


def part_score(lines, beats, ranges, offset_beats, remap=None, drop=(), label="", chord=None, ring=None):
    """Bars inside `ranges` keep their tab line (fitted to the bar length); everything else rests. Consecutive
    identical bars collapse to [bar]xN; consecutive rests merge."""
    on = set()
    for a, b in ranges:
        on.update(range(a, b + 1))
    items = []  # ("rest", beats) | ("bar", text)
    if offset_beats > 0:
        items.append(["rest", offset_beats])
    for i, (line, nb) in enumerate(zip(lines, beats), start=1):
        if i in on and line.strip() and any(not t.startswith("R") for t in line.split()):
            if remap or drop:
                line = remap_drums(line, remap or {}, set(drop))
            if chord:
                line = split_chords(line, chord)
            line, have = fit_bar(line, nb)
            if ring:
                line = ring_bar(line, float(ring))
            if abs(have - nb) >= 1e-4:
                FITTED.append((label, i, round(have, 4), nb))
            items.append(["bar", line])
        elif items and items[-1][0] == "rest":
            items[-1][1] += nb
        else:
            items.append(["rest", nb])
    while items and items[-1][0] == "rest":
        items.pop()
    out, i = [], 0
    while i < len(items):
        kind, v = items[i]
        if kind == "rest":
            out.append(fmt_beats(v)); i += 1; continue
        j = i
        while j + 1 < len(items) and items[j + 1] == items[i]:
            j += 1
        n = j - i + 1
        out.append(f"[{v}]x{n}" if n > 1 else v)
        i = j + 1
    return " | ".join(out)


def tempo_map(tl, off_beats):
    """A tempo map with a point wherever the tab's tempo or meter changes (beats count from the song start,
    after the offset)."""
    pts, beat, last = [], off_beats, None
    if off_beats > 0:
        pts.append({"at": "0b", "bpm": tl[0]["bpm"]})
    for m in tl:
        key = (m["bpm"], m["sig"])
        if key != last:
            pts.append({"at": f"{fmt_num(beat)}b", "bpm": m["bpm"], "meter": m["sig"]})
            last = key
        beat += m["beats"]
    return pts


def fmt_num(x):
    return f"{round(x, 4):.4f}".rstrip("0").rstrip(".")


def corrected_timeline(cache, mp):
    """The tab's timeline with the map's tempo overrides applied and skipped measures marked."""
    tl = [dict(m) for m in T.timeline(cache)]
    over = sorted((int(k), float(v)) for k, v in mp.get("bpm", {}).items())
    for i, (m0, v) in enumerate(over):
        m1 = over[i + 1][0] if i + 1 < len(over) else len(tl) + 1
        for m in tl[m0 - 1:m1 - 1]:
            m["bpm"] = v
    skip = set()
    for a, b in mp.get("skip", []):
        skip.update(range(a, b + 1))
    for m in tl:
        m["skip"] = m["m"] in skip
    return tl


def build(mp):
    cache = mp["cache"]
    full = corrected_timeline(cache, mp)
    keep = [i for i, m in enumerate(full) if not m["skip"]]
    tl = [full[i] for i in keep]
    beats = [m["beats"] for m in tl]
    bpm = tl[0]["bpm"]
    # The offset is converted at the opening tempo; with tempo changes the song gets a tempo map
    # (also with "meters": true, to carry the tab's time signatures for bar-aligned editing).
    off_beats = round(mp.get("offset", 0) * bpm / 60, 4)
    varying = any(m["bpm"] != bpm for m in tl)
    tempo = tempo_map(tl, off_beats) if varying or mp.get("meters") else bpm
    lines_cache = {}
    tracks = []
    for p in mp["parts"]:
        if "score_file" in p:
            # a part that is not in the tab (e.g. a vocal line from stemvox.py): `bar N  tokens` lines on the
            # tab's measure numbers; unlisted bars and `rest` ranges are silent
            sf = os.path.join(ROOT, p["score_file"]) if not os.path.isabs(p["score_file"]) else p["score_file"]
            by_bar = {}
            for ln in open(sf):
                bits = ln.split(None, 2)
                if len(bits) == 3 and bits[0] == "bar":
                    by_bar[int(bits[1])] = bits[2].strip()
            silent = {m for a, b in p.get("rest", []) for m in range(a, b + 1)}
            key = ("file", p["score_file"], tuple(sorted(silent)))
            lines_cache[key] = ["" if full[i]["m"] in silent else by_bar.get(full[i]["m"], "") for i in keep]
            p = {**p, "track": key, "bars": p.get("bars", [[1, full[-1]["m"]]])}
        if "raw" in p:   # a score from elsewhere (e.g. tools/drumtrans.py output): "FILE.json#key" or a plain text file
            path, _, key = p["raw"].partition("#")
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = path if os.path.isabs(path) else os.path.join(root, path)
            sc = json.load(open(path))[key]["score"] if key else open(path).read().strip()
            tr = {"name": p["name"], "patch": p["patch"]}
            for k in ("gain", "pan"):
                if k in p:
                    tr[k] = p[k]
            tr.update(p.get("extra", {}))
            tr["score"] = sc
            tracks.append(tr)
            continue
        if p["track"] not in lines_cache:
            lines_all = S.score(cache, p["track"])[2]
            lines_cache[p["track"]] = [lines_all[i] for i in keep]
        pos = {full[i]["m"]: k + 1 for k, i in enumerate(keep)}   # tab measure → kept index (1-based)
        lines = lines_cache[p["track"]]
        if p.get("replace"):
            # per-bar corrections (e.g. from per-bar chroma against the stems): {"221": "D3,A3,E4/4b", ...} on the
            # tab's measure numbers, applied before chord splitting and bar fitting
            lines = list(lines)
            for m, txt in p["replace"].items():
                if int(m) in pos:
                    lines[pos[int(m)] - 1] = txt
        for a, b, fr, to in p.get("subst", []):
            # note corrections over a bar range: [[81, 97, "D3", "Eb3"]] swaps that note (alone or in a chord),
            # keeping the bar's rhythm and articulations (a tab's wrong fret across a passage)
            lines = list(lines)
            pat = re.compile(r"(^|[\s,])" + re.escape(fr) + r"(?=[/,])")
            for m in range(int(a), int(b) + 1):
                if m in pos:
                    lines[pos[m] - 1] = pat.sub(lambda g: g.group(1) + to, lines[pos[m] - 1])
        ranges = []
        for a, b in p["bars"]:
            kept = [pos[m] for m in range(a, b + 1) if m in pos]
            if kept:
                ranges.append((min(kept), max(kept)))
        sc = part_score(lines, beats, ranges, off_beats, p.get("remap"), p.get("drop", ()), p["name"], p.get("chord"), p.get("ring"))
        for art in list(mp.get("strip", [])) + list(p.get("strip", [])):   # e.g. "ph": drop ^ph articulations
            if art == "bend":   # drop bend= tokens (slides/bends); held notes stay
                sc = re.sub(r"\s*bend=\S+", "", sc)
            else:
                sc = re.sub(r"\^" + re.escape(art) + r"(?![A-Za-z0-9_])", "", sc)
        tr = {"name": p["name"], "patch": p["patch"]}
        for k in ("gain", "pan"):
            if k in p:
                tr[k] = p[k]
        tr.update(p.get("extra", {}))
        tr["score"] = sc
        tracks.append(tr)
    song = {"about": mp.get("about"), "tempo": tempo}   # a song is named by its file
    song.update(mp.get("head", {}))
    song["tracks"] = tracks
    return {k: v for k, v in song.items() if v is not None}


def dump(song):
    """YAML with one flow-mapping line per track (scores are long single-line strings)."""
    out = []
    for k, v in song.items():
        if k == "tracks":
            continue
        out.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    out.append("tracks:")
    for t in song["tracks"]:
        body = ", ".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in t.items())
        out.append(f"  - {{{body}}}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    a = sys.argv[1:]
    mp = json.load(open(a[0]))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mp["cache"] = os.path.join(root, mp["cache"]) if not os.path.isabs(mp["cache"]) else mp["cache"]
    text = dump(build(mp))
    for label, bar, have, want in FITTED:
        print(f"fitted {label} bar {bar}: {have} → {want} beats", file=sys.stderr)
    if "-o" in a:
        open(a[a.index("-o") + 1], "w").write(text)
    else:
        sys.stdout.write(text)
