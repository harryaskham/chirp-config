#!/usr/bin/env python3
"""eqcuts: a song's EQ cuts, the version each dates from, and what has stopped playing with it since.

chirper-zero, 16 Nov (False Summit v13): "AN EQ SET AGAINST A PILE OUTLIVES THE PILE. When a part leaves a band,
re-read every cut that was made while it was there. (If a tool could list a song's eq cuts with the version that added
them and what has left the band since, I would have found this at v11.)" At v3 he cut 700 Hz on eight guitars because a
plain tone played under them; at v11 the tone left, and the cut stayed for two versions, 2.4 dB short in that band.

  eqcuts.py ID [--min 1.5] [--from HZ] [--to HZ] [--song CANDIDATE.yaml] [--pin CHIRP] [--json]
  eqcuts.py ID --versions v12=OLD.yaml cand=NEW.yaml      your own files, oldest first, in place of the song's history

It plans every committed version of songs/ID.yaml (the commits that touched it, oldest first; a commit's label is the
"vN" in its subject) and the file as it stands when that differs (--song: a candidate in its place), and lists the
newest one's EQ bands that cut by --min dB or more: on a track, a bus, a patch or the master. For each:
  since     the first version of the unbroken run in which that place has had a cut of that kind within a third of an
            octave of it (so a cut retuned or deepened keeps its date; "was" gives what it was then when it differs)
  LEFT      the parts that sounded on a quarter or more of its beats in that version and on half as many or fewer now,
            with the version from which that is so. "Its beats" are the beats on which the cut's own tracks sound (a
            bus: the tracks routed to it; a patch: the tracks that play it; the master: every track). A part SOUNDS
            on a beat when it has a note there and its own gain there (its `gain` and the lanes that move it) is
            within 30 dB of its loudest: a part turned down to nothing by a lane has left, though its notes are
            still written (False Summit's tone left that way: a lane to -60 dB, the same 299 notes).
  joined    the reverse: company the cut was not made against
A part that left is one of three kinds, and only the first is marked: its lowest note is at or under the cut, so its
harmonics reached that band (LEFT SINCE); it is pitched above the cut (not in the band by its notes); or its notes
cannot say (a kit piece has no pitch, and how far a part's harmonics reach up under a high shelf is its sound). Parts
that left the same cuts from the same version are one entry (a left and a right, a rig's four guitars). This reads
NOTES and gain lanes, not sound: it says a cut's reason may have gone, never that the cut is wrong. The like-for-like
check is the band itself, with and without the cut, against the records or the song's own stretches
(tools/stembal.py, `seams.py --bands`). The exit status is 0 whatever it finds.
A version that does not plan on this engine is skipped and said. Plans are cached by the file's content
(~/.cache/chirp/eqcuts), so a second run reads only what is new.
(chirp-eco, 16 Nov; tests: tools/tests/test_eqcuts.py.)"""
import argparse
import bisect
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import keyshape  # noqa: E402

DIGEST = 2                # bump when a digest's shape or meaning changes: older cache files are then not read
QUIET = 30.0              # dB under a track's own loudest gain: there it does not sound
NEAR = 1 / 3              # octaves: a cut within this of an older one at the same place is the same cut
THEN, HALF = 0.25, 0.5    # company: a quarter of the cut's beats then; half of that or less now
CUT_KINDS = {"peak", "bell", "lowshelf", "highshelf", "notch", "bp"}


def cache_dir():
    return os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "chirp", "eqcuts")


def db(v):
    """(dB, the lanes that move it): "-2.5dB", -2.5 or {"value": …, "mod": [{"src": "auto.x"}]}."""
    lanes = []
    if isinstance(v, dict):
        lanes = [str(m.get("src")) for m in v.get("mod") or [] if isinstance(m, dict) and m.get("src")]
        v = v.get("value")
    if isinstance(v, str):
        m = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*(?:dB)?\s*", v, re.I)
        v = float(m.group(1)) if m else None
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        v = None
    return (float(v) if v is not None else None), lanes


def band(b):
    """An EQ band as a mapping: its own, or the string form `peak cutoff=700 q=1 gain=-2.5dB`."""
    if isinstance(b, dict):
        return b
    if isinstance(b, str):
        words = b.split()
        out = {"kind": words[0]} if words and "=" not in words[0] else {}
        for w in words:
            if "=" in w:
                k, v = w.split("=", 1)
                out[k] = v
        return out
    return {}


def fx_cuts(fx):
    """[(fx index, band index, kind, hz, q, dB, lanes)] for every band of an effect chain that turns something down."""
    out = []
    for i, e in enumerate(fx or []):
        if isinstance(e, str):
            e = band(e)
            e = {"type": "eq", "bands": [e]} if e.get("kind") in CUT_KINDS else {}
        if not isinstance(e, dict):
            continue
        bands = e.get("bands") if e.get("type") == "eq" else [e] if e.get("type") == "filter" else []
        for j, b in enumerate(bands or []):
            b = band(b)
            kind = str(b.get("kind") or "peak")
            gain, lanes = db(b.get("gain"))
            hz, more = db(b.get("cutoff"))
            if gain is None or gain >= 0 or hz is None or hz <= 0 or kind not in CUT_KINDS:
                continue
            q, _ = db(b.get("q"))
            out.append((i, j, kind, hz, q, gain, sorted(set(lanes + more))))
    return out


def ranges(beats):
    """A set of beat numbers as [[first, past the last], …]."""
    out = []
    for b in sorted(beats):
        if out and out[-1][1] == b:
            out[-1][1] = b + 1
        else:
            out.append([b, b + 1])
    return out


def beat_set(rs):
    return {b for a, z in rs or [] for b in range(a, z)}


def gain_at(t, tempo):
    """beat -> the track's own gain there in dB (its `gain` and the lanes that move it), or None when it has no lane on
    its gain or one of them cannot be placed."""
    import warp
    static, srcs = db(t.get("gain"))
    mods = [m for m in (t.get("gain") or {}).get("mod") or [] if isinstance(m, dict)] if isinstance(t.get("gain"), dict) else []
    lanes = []
    for m in mods:
        src = str(m.get("src") or "")
        points = ((t.get("auto") or {}).get(src[5:]) or {}).get("points") if src.startswith("auto.") else None
        if not points:
            return None
        try:
            pts = sorted((float(warp.beats(p[0], tempo)), float(p[1])) for p in points)
            lanes.append((float(m.get("amount", 1.0)), [p[0] for p in pts], [p[1] for p in pts]))
        except (TypeError, ValueError, IndexError):
            return None
    if not lanes:
        return None

    def value(xs, ys, b):
        if b <= xs[0]:
            return ys[0]
        if b >= xs[-1]:
            return ys[-1]
        i = bisect.bisect_right(xs, b) - 1
        span = xs[i + 1] - xs[i]
        return ys[i] if span <= 0 else ys[i] + (ys[i + 1] - ys[i]) * (b - xs[i]) / span

    return lambda b: (static or 0.0) + sum(amount * value(xs, ys, b) for amount, xs, ys in lanes)


def digest(canon):
    """What a version's plan says that this needs: each track's bus, patch, lowest note and the beats it sounds on;
    each bus's own bus; every cut and where it sits."""
    tracks, cuts = {}, []
    tempo = canon.get("tempo")
    tempo = float(tempo) if isinstance(tempo, (int, float)) and not isinstance(tempo, bool) and tempo > 0 else 120.0

    def walk(ts):
        for t in ts if isinstance(ts, list) else []:
            if not isinstance(t, dict):
                continue
            name = t.get("name")
            notes = [n for n in t.get("notes") or [] if isinstance(n, dict)]
            if name and notes:
                start = t.get("at")
                m = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)b\s*", start) if isinstance(start, str) else None
                off = float(m.group(1)) if m else 0.0
                beats, low = set(), None
                for n in notes:
                    try:
                        a = float(n.get("at") or 0) + off
                        z = a + max(float(n.get("len") or 0), 1e-6)
                    except (TypeError, ValueError):
                        continue
                    beats.update(range(int(math.floor(a)), int(math.ceil(z - 1e-9))))
                    p = keyshape.lowest(n.get("pitch"))
                    if p is not None and (low is None or p < low):
                        low = p
                gain = None if t.get("mute") is True else gain_at(t, tempo)
                if t.get("mute") is True:
                    beats = set()
                elif gain is not None and beats:
                    level = {b: gain(b + 0.5) for b in beats}
                    top = max(level.values())
                    beats = {b for b, g in level.items() if g > top - QUIET}
                patch = t.get("patch")
                tracks[name] = {"out": t.get("out") if isinstance(t.get("out"), str) else None,
                                "patch": patch.split()[0] if isinstance(patch, str) and patch.split() else None,
                                "low": low, "beats": ranges(beats)}
                for c in fx_cuts(t.get("fx")):
                    cuts.append(("track", name, *c))
            walk(t.get("tracks"))

    walk(canon.get("tracks"))
    buses = {}
    for name, b in (canon.get("buses") or {}).items():
        if isinstance(b, dict):
            buses[name] = b.get("out") if isinstance(b.get("out"), str) else None
            for c in fx_cuts(b.get("fx")):
                cuts.append(("bus", name, *c))
    for name, p in (canon.get("patches") or {}).items():
        if isinstance(p, dict) and "." not in name:
            for c in fx_cuts(p.get("fx")):
                cuts.append(("patch", name, *c))
    for c in fx_cuts((canon.get("master") or {}).get("fx") if isinstance(canon.get("master"), dict) else None):
        cuts.append(("master", "master", *c))
    return {"digest": DIGEST, "tracks": tracks, "buses": buses,
            "cuts": [{"on": on, "name": name, "fx": i, "band": j, "kind": kind, "hz": hz, "q": q, "gain": gain, "lanes": lanes}
                     for on, name, i, j, kind, hz, q, gain, lanes in cuts]}


def plan(pin, path):
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    try:
        r = subprocess.run([pin, "--json", "plan", "-f", path], capture_output=True, text=True, env=env, timeout=600)
        return json.loads(r.stdout)["data"]["canonical"]
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        return None


def read_version(pin, text, cache=True):
    """The digest of one version's text (cached by its content and the engine), or None when it does not plan."""
    key = hashlib.sha256((os.path.basename(pin) + "\0" + str(DIGEST) + "\0" + text).encode()).hexdigest()[:32]
    path = os.path.join(cache_dir(), key + ".json")
    if cache:
        try:
            with open(path) as f:
                d = json.load(f)
            if d.get("digest") == DIGEST:
                return d
        except (OSError, ValueError):
            pass
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", prefix="eqcuts-", delete=False) as f:
        f.write(text)
        tmp = f.name
    try:
        canon = plan(pin, tmp)
    finally:
        os.unlink(tmp)
    if not isinstance(canon, dict):
        return None
    d = digest(canon)
    if cache:
        try:
            os.makedirs(cache_dir(), exist_ok=True)
            with open(f"{path}.{os.getpid()}", "w") as f:
                json.dump(d, f)
            os.replace(f"{path}.{os.getpid()}", path)
        except OSError:
            pass
    return d


def git(*args):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def history(cid):
    """[(label, text)] for every commit that touched songs/ID.yaml, oldest first, then the file as it stands when it
    differs from the newest commit. A label is the "vN" of the commit's subject, else its short hash."""
    rel = f"songs/{cid}.yaml"
    out, seen = [], {}
    for line in reversed((git("log", "--format=%h%x09%s", "--", rel) or "").splitlines()):
        sha, _, subject = line.partition("\t")
        text = git("show", f"{sha}:{rel}")
        if text is None:
            continue
        m = re.search(r"\b(v\d+)\b", subject)
        label = m.group(1) if m else sha
        seen[label] = seen.get(label, 0) + 1
        out.append((label if seen[label] == 1 else f"{label}.{seen[label]}", text))
    try:
        with open(os.path.join(ROOT, rel)) as f:
            now = f.read()
    except OSError:
        now = None
    if now is not None and (not out or out[-1][1] != now):
        out.append(("the file now", now))
    return out


def members(d, cut):
    """The tracks a cut sits over in a version's digest."""
    tracks = d["tracks"]
    if cut["on"] == "track":
        return [cut["name"]] if cut["name"] in tracks else []
    if cut["on"] == "patch":
        return [n for n, t in tracks.items() if t.get("patch") == cut["name"]]
    if cut["on"] == "bus":
        inside, grew = {cut["name"]}, True
        while grew:                                   # a bus routed into this bus brings its tracks
            more = {b for b, out in d.get("buses", {}).items() if out in inside} - inside
            inside |= more
            grew = bool(more)
        return [n for n, t in tracks.items() if t.get("out") in inside]
    return list(tracks)


def same(a, b):
    return a["on"] == b["on"] and a["name"] == b["name"] and a["kind"] == b["kind"] and abs(math.log2(a["hz"] / b["hz"])) <= NEAR


def since(versions, cut):
    """(index of the first version of the unbroken run that has this cut, that version's cut)."""
    at, then = len(versions) - 1, cut
    for i in range(len(versions) - 2, -1, -1):
        older = [c for c in versions[i][1]["cuts"] if same(c, cut)]
        if not older:
            break
        at, then = i, min(older, key=lambda c: abs(math.log2(c["hz"] / cut["hz"])))
    return at, then


def company(d, tracks):
    """{other track: the share of these tracks' beats on which it also sounds} in one version."""
    mine = set()
    for n in tracks:
        mine |= beat_set((d["tracks"].get(n) or {}).get("beats"))
    if not mine:
        return {}
    return {n: len(beat_set(t.get("beats")) & mine) / len(mine) for n, t in d["tracks"].items() if n not in tracks}


def reaches(low, cut):
    """Does a part whose lowest note is this MIDI number have harmonics in the cut's band? None: its notes cannot say
    (it has no pitch, or the cut is a high shelf: how far up a part's harmonics go is its sound, not its notes)."""
    if low is None or cut["kind"] == "highshelf":
        return None
    return 440.0 * 2 ** ((low - 69) / 12) <= cut["hz"] * 1.2


def moved(versions, at, cut):
    """The company that left and joined between version `at` and the newest: two lists of
    {track, then, now, from (label), low, reaches}."""
    old, new = versions[at][1], versions[-1][1]
    then_cut = dict(cut)
    was, now = company(old, members(old, then_cut)), company(new, members(new, cut))
    left, joined = [], []
    for n in sorted(set(was) | set(now)):
        a, b = was.get(n, 0.0), now.get(n, 0.0)
        if a >= THEN and b <= a * HALF:
            first = len(versions) - 1
            for i in range(len(versions) - 2, at, -1):
                share = company(versions[i][1], members(versions[i][1], cut)).get(n, 0.0)
                if share > a * HALF:
                    break
                first = i
            low = (old["tracks"].get(n) or {}).get("low")
            left.append({"track": n, "then": a, "now": b, "from": versions[first][0], "low": low, "reaches": reaches(low, cut)})
        elif b >= THEN and a <= b * HALF:
            joined.append({"track": n, "then": a, "now": b})
    return left, joined


def read(versions, least=1.5, lo=None, hi=None):
    """The newest version's cuts of `least` dB or more (between lo and hi Hz), alike ones on several tracks as one row:
    [{on, names, kind, hz, q, gain, lanes, since, first, was, left, joined}]."""
    rows = {}
    for cut in versions[-1][1]["cuts"]:
        if -cut["gain"] < least or (lo and cut["hz"] < lo) or (hi and cut["hz"] > hi):
            continue
        at, then = since(versions, cut)
        key = (cut["on"] if cut["on"] == "track" else (cut["on"], cut["name"], cut["fx"], cut["band"]),
               cut["kind"], cut["hz"], cut["q"], cut["gain"], tuple(cut["lanes"]), at, then["hz"], then["gain"])
        rows.setdefault(key, {"cut": cut, "names": [], "at": at, "then": then})["names"].append(cut["name"])
    out = []
    for r in rows.values():
        cut, at = r["cut"], r["at"]
        if cut["on"] == "track":                      # one row for the same band on several tracks: their beats together
            whole = dict(cut)
            left, joined = group_moved(versions, at, r["names"], whole)
        else:
            left, joined = moved(versions, at, cut)
        was = None
        if abs(r["then"]["hz"] - cut["hz"]) > 0.5 or abs(r["then"]["gain"] - cut["gain"]) > 0.05:
            was = {"hz": r["then"]["hz"], "gain": r["then"]["gain"]}
        out.append({"on": cut["on"], "names": r["names"], "kind": cut["kind"], "hz": cut["hz"], "q": cut["q"],
                    "gain": cut["gain"], "lanes": cut["lanes"], "since": versions[at][0], "first": at == 0,
                    "new": at == len(versions) - 1 and len(versions) > 1, "was": was, "left": left, "joined": joined})
    out.sort(key=lambda r: (r["hz"], r["names"]))
    return out


def group_moved(versions, at, names, cut):
    """moved() for one band on several tracks: the company of all of them together."""
    old, new = versions[at][1], versions[-1][1]

    def of(d):
        return company(d, [n for n in names if n in d["tracks"]])

    was, now = of(old), of(new)
    left, joined = [], []
    for n in sorted(set(was) | set(now)):
        a, b = was.get(n, 0.0), now.get(n, 0.0)
        if a >= THEN and b <= a * HALF:
            first = len(versions) - 1
            for i in range(len(versions) - 2, at, -1):
                if of(versions[i][1]).get(n, 0.0) > a * HALF:
                    break
                first = i
            low = (old["tracks"].get(n) or {}).get("low")
            left.append({"track": n, "then": a, "now": b, "from": versions[first][0], "low": low, "reaches": reaches(low, cut)})
        elif b >= THEN and a <= b * HALF:
            joined.append({"track": n, "then": a, "now": b})
    return left, joined


def hz_text(hz):
    return f"{hz / 1000:.3g} kHz" if hz >= 1000 else f"{hz:.4g} Hz"


def note_hz(low):
    return f"{keyshape.note_name(low)}, {440.0 * 2 ** ((low - 69) / 12):.0f} Hz"


def cut_text(r):
    what = f"{r['kind']} {hz_text(r['hz'])} {r['gain']:+g} dB" + (f" q {r['q']:g}" if r["q"] else "")
    return what + (" (moved by " + ", ".join(r["lanes"]) + ")" if r["lanes"] else "")


def on_text(r):
    names = r["names"]
    if r["on"] == "master":
        return "the master"
    where = "tracks" if r["on"] == "track" and len(names) > 1 else r["on"]
    return f"{where} " + ", ".join(names[:8]) + (f" (+{len(names) - 8})" if len(names) > 8 else "")


def spread(shares):
    return f"{min(shares):.0%}" if max(shares) - min(shares) < 0.005 else f"{min(shares):.0%} to {max(shares):.0%}"


def lines(cid, versions, rows, least, skipped=()):
    newest = versions[-1][0]
    out = [f"{cid} at {newest} ({len(versions)} version{'s' if len(versions) != 1 else ''} read"
           + (f"; {len(skipped)} did not plan and are skipped: {', '.join(skipped[:6])}" if skipped else "")
           + f"): {len(rows)} EQ cut{'s' if len(rows) != 1 else ''} of {least:g} dB or more"]
    if not rows:
        return out
    wide = max(len(cut_text(r)) for r in rows)
    span = max(len(on_text(r)) for r in rows)
    for r in rows:
        when = "new in this version" if r["new"] else f"since {r['since']}" + (" (the first read)" if r["first"] else "")
        if r["was"]:
            when += f"; was {hz_text(r['was']['hz'])} {r['was']['gain']:+g} dB then"
        out.append(f"  {cut_text(r):<{wide}s}  on {on_text(r):<{span}s}  {when}")
    order = {v[0]: i for i, v in enumerate(versions)}
    who, kit, away = {}, {}, {}
    for k, r in enumerate(rows):
        for x in r["left"]:
            table = who if x["reaches"] else kit if x["reaches"] is None else away
            table.setdefault((x["track"], x["from"]), []).append((k, x))
    groups = {}                                       # parts that left the same cuts from the same version: one entry
    for (track, frm), hits in who.items():
        groups.setdefault((frm, tuple(k for k, _ in hits)), []).append((track, hits))
    if groups:
        out.append("WHO HAS LEFT SINCE A CUT WAS MADE (it sounded on a quarter or more of the cut's beats then, half that or less now; "
                   "by its lowest note it reached that band):")
        for (frm, ks), parts in sorted(groups.items(), key=lambda kv: (-order.get(kv[0][0], 0), kv[1][0][0])):
            names = ", ".join(f"{track} ({note_hz(hits[0][1]['low'])})" for track, hits in parts[:6])
            names += f" (+{len(parts) - 6})" if len(parts) > 6 else ""
            out.append(f"  LEFT SINCE: {names}, from {frm}: {len(ks)} cut{'s' if len(ks) != 1 else ''} made while "
                       f"{'they were' if len(parts) > 1 else 'it was'} there, the newest first:")
            for i, k in sorted(enumerate(ks), key=lambda ik: (-order.get(rows[ik[1]]["since"], 0), rows[ik[1]]["hz"])):
                r = rows[k]
                then = [hits[i][1]["then"] for _, hits in parts]
                now = [hits[i][1]["now"] for _, hits in parts]
                share = f"{spread(then)} of its beats then, {spread(now)} now"
                out.append(f"      {cut_text(r)} on {on_text(r)} (since {r['since']}{', the first read' if r['first'] else ''}): {share}")
    for table, label in ((kit, "left; its notes cannot say what it had in the band (a kit piece, or a high shelf): a render does"),
                         (away, "left, pitched above the cut (not in that band by its notes)")):
        if table:
            def bands(hits):
                return ", ".join(hz_text(h) for h in sorted({rows[k]["hz"] for k, _ in hits}))
            out.append(f"  {label}: " + "; ".join(f"{track} from {frm} ({bands(hits)})" for (track, frm), hits in sorted(table.items())))
    joined = [(r, r["joined"]) for r in rows if r["joined"]]
    if joined:
        out.append("JOINED SINCE (the cut was not made against them):")
        seen = {}
        for r, js in joined:
            seen.setdefault(", ".join(x["track"] for x in js[:10]) + (f" (+{len(js) - 10})" if len(js) > 10 else ""), []).append(r)
        for names, rs in seen.items():
            out.append(f"  {names}: under " + "; ".join(f"{r['kind']} {hz_text(r['hz'])} on {on_text(r)}" for r in rs[:6])
                       + (f" (+{len(rs) - 6})" if len(rs) > 6 else ""))
    marked = len(groups)
    out.append(f"{marked} LEFT SINCE mark{'s' if marked != 1 else ''}: a question, not a fault. A part that played under a cut when it "
               "was made and has gone may have been the cut's reason; a cut the song began with may be the family's own. Read the "
               "band with and without the cut (tools/stembal.py; seams.py --bands). Notes and gain lanes are read here, not sound.")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("--min", type=float, default=1.5, dest="least", help="list cuts of this many dB or more (default 1.5)")
    ap.add_argument("--from", type=float, dest="lo", help="only cuts at or above this frequency (Hz)")
    ap.add_argument("--to", type=float, dest="hi", help="only cuts at or below this frequency (Hz)")
    ap.add_argument("--song", help="a candidate file: read as the newest version, in place of the file as it stands")
    ap.add_argument("--versions", nargs="+", metavar="LABEL=FILE", help="your own files, oldest first, in place of the history")
    ap.add_argument("--pin")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    pin = a.pin or chirpbin.resolve("chirp")
    if a.versions:
        texts = []
        for v in a.versions:
            label, eq, path = v.partition("=")
            if not eq:
                ap.error(f"--versions takes LABEL=FILE, not {v!r}")
            try:
                with open(path) as f:
                    texts.append((label, f.read()))
            except OSError as e:
                sys.exit(f"eqcuts: {e}")
    else:
        texts = history(a.id)
        if a.song:
            try:
                with open(a.song) as f:
                    cand = f.read()
            except OSError as e:
                sys.exit(f"eqcuts: {e}")
            if texts and texts[-1][0] == "the file now":
                texts.pop()
            if not texts or texts[-1][1] != cand:
                texts.append((os.path.basename(a.song), cand))
    if not texts:
        sys.exit(f"eqcuts: no version of songs/{a.id}.yaml to read (no commit touched it and there is no file)")
    versions, skipped = [], []
    for label, text in texts:
        d = read_version(pin, text, not a.no_cache)
        if d is None:
            skipped.append(label)
        else:
            versions.append((label, d))
    if not versions or (skipped and skipped[-1] == texts[-1][0]):
        sys.exit(f"eqcuts: the newest version ({texts[-1][0]}) does not plan on {os.path.basename(pin)}")
    rows = read(versions, a.least, a.lo, a.hi)
    if a.json:
        print(json.dumps({"id": a.id, "at": versions[-1][0], "versions": [v[0] for v in versions], "skipped": skipped,
                          "cuts": rows}, ensure_ascii=False))
        return 0
    print("\n".join(lines(a.id, versions, rows, a.least, skipped)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
