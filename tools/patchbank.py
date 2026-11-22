#!/usr/bin/env python3
"""patchbank: BANK AN ALBUM'S INSTRUMENTS IN THE LIBRARY, so what a record learned is there for the next one.
(chirp-eco, 22 Nov 2026. Harry: "banking patches, why were these not committed? we should ensure we persist changes".
In four days of instrument rounds on Common Time every mend was made by hand in a song: an override string on a library
patch, a patch of the song's own, an effect on a track. All of it is committed with the song, and none of it reached
patches/: a new song that asked for `ct-twin` or `ct-kit` got the sound of 12 November.)

  patchbank.py promote ALBUM [--dry]     into patches/, under names nothing else has, each resolved and self-contained:
                                         EACH SONG'S KIT AS PLAYED (its kit tracks merged into one kit, each piece as
                                         the track that plays it has it: `ct-kit-so-far`) and every other instrument of
                                         the song's own (its `patches:` and a track's inline patch: `owing-bow`).
  patchbank.py succeed ALBUM [--dry]     A SUCCESSOR for each shared patch the songs agree about: `NAME-2` is NAME with
                                         every setting that more than half of its tracks carry, in three songs or more
                                         (and an effect those tracks all added after it, moved into the patch).
  patchbank.py census ALBUM [--md FILE]  what the songs did to each patch they share, field by field: which songs set it
                                         and to what. Where they agree is the successor; the rest each song chose.
  patchbank.py take ID TRACK NAME [--fx] [--about TEXT]
                                         ONE track's instrument as played, into patches/NAME.yaml: its patch with every
                                         override resolved; --fx appends the track's own effects after the patch's.
  patchbank.py archive ALBUM             compose/ALBUM/bank/ID.json: each song's whole instrument and mix state as the
                                         engine resolves it (every patch, bus and effect; no notes).
  common: [--pin CHIRP] [--json]

HOW. `chirp plan` prints a song's canonical form, in which every patch a track names is resolved in full (extends,
overrides and sugar applied). A banked patch IS that resolved form, so it cannot differ from what the song plays; each
one written is then planned again by its new name and compared, and a file that does not come back the same is removed
and reported. NOTHING HERE EDITS A SONG OR ANOTHER LIBRARY FILE: a banked name is new, or is a file this tool wrote
before; one of those is written again only while no registered song would change (tools/libguard.py's own check).
NOT BANKED: a patch that plays another song inside the song (a layer with `song:`), which means nothing outside it.
A SUCCESSOR IS A RULE'S, NOT AN EAR'S: it holds what the songs agree about and nothing else; fit it before trusting it.
Tests: tools/tests/test_patchbank.py.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)

MARK = "BANKED by tools/patchbank.py"


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", str(title).lower()).strip("-")


def walk(tracks, out=None):
    """Every track at any depth that names a patch."""
    out = [] if out is None else out
    for t in tracks or []:
        if isinstance(t, dict):
            if isinstance(t.get("patch"), str) and t.get("name"):
                out.append(t)
            walk(t.get("tracks"), out)
    return out


def base_of(ref):
    return ref.split(" ", 1)[0]


def fields(ref):
    """{field: value} for the overrides of a reference string (`ct-twin fx.1.tight=150 synth.layers.0.soft=expr.pm*0.5`)."""
    try:
        toks = shlex.split(ref)
    except ValueError:
        toks = ref.split(" ")
    return dict(tok.split("=", 1) for tok in toks[1:] if "=" in tok)


def plays_a_song(patch):
    """True when a resolved patch has a layer that plays another song (it means nothing outside its own song)."""
    if isinstance(patch, dict):
        return any((k == "song" and v) or plays_a_song(v) for k, v in patch.items())
    if isinstance(patch, list):
        return any(plays_a_song(v) for v in patch)
    return False


def inline_kit(patch, pats):
    """A resolved kit with each piece's patch written in it. The canonical plan keeps a piece's patch as its own entry
    (`KIT.PIECE`) and names it in the kit; a banked kit must hold it. A name that is not an entry is the library's own."""
    if not (isinstance(patch, dict) and isinstance(patch.get("kit"), dict)):
        return patch
    kit = {}
    for piece, d in patch["kit"].items():
        if isinstance(d, dict) and isinstance(d.get("patch"), str) and isinstance(pats.get(d["patch"]), dict):
            d = dict(d, patch=inline_kit(pats[d["patch"]], pats))
        kit[piece] = d
    return dict(patch, kit=kit)


def lanes_of(patch):
    """The track automation lanes a patch reads (`auto.wah`): the track that plays it must define them."""
    found = set()

    def look(o):
        if isinstance(o, dict):
            for v in o.values():
                look(v)
        elif isinstance(o, list):
            for v in o:
                look(v)
        elif isinstance(o, str):
            found.update(re.findall(r"\bauto\.([A-Za-z0-9_-]+)", o))
    look({k: v for k, v in patch.items() if k != "about"} if isinstance(patch, dict) else patch)
    return sorted(found)


def kind_of(ref, own, library):
    """'local' (the song defines it), 'inline' (a track's own: NAME.patch), 'library' (a file in patches/) or 'builtin'."""
    b = base_of(ref)
    if b in own:
        return "local"
    if b.endswith(".patch"):
        return "inline"
    return "library" if b in library else "builtin"


def same_patch(a, b):
    """Two resolved patches are the same instrument: equal but for their `about`."""
    strip = lambda p: {k: v for k, v in p.items() if k != "about"} if isinstance(p, dict) else p  # noqa: E731
    return strip(a) == strip(b)


# ---- census -----------------------------------------------------------------------------------------------------------

def track_fx_fields(track):
    """{'+TYPE.PARAM': value} for the first effect of each type among a track's OWN effects (after its patch's)."""
    out, seen = {}, set()
    for e in track.get("fx") or []:
        if not isinstance(e, dict) or not e.get("type") or e["type"] in seen:
            continue
        seen.add(e["type"])
        for k, v in e.items():
            if k != "type" and not isinstance(v, (dict, list)):
                out[f"+{e['type']}.{k}"] = str(v)
    return out


def census(songs):
    """{parent: {"songs": [n], "tracks": N, "plain": [n], "fields": {field: {value: {"songs": [n], "tracks": N}}},
                 "rows": [(n, track, {field: value})]}} over songs: [(n, canonical, own names, {own name: extends})].
    A parent is the library or built-in patch a reference starts from; a song's own patch counts under what it
    extends, with its `extends` string's overrides. A field is an override (`fx.1.tight`), or `+TYPE.PARAM` for an
    effect the track adds after the patch."""
    out = {}
    for n, canon, own, ext in songs:
        for t in walk(canon.get("tracks")):
            ref = t["patch"]
            b = base_of(ref)
            f = fields(ref)
            hops = 0
            while (b in own or b.endswith(".patch")) and hops < 8:      # the song's own: count it under what it extends
                e = ext.get(b)
                if not e:
                    b = None
                    break
                f = dict(fields(e), **f)
                b = base_of(e)
                hops += 1
            if not b:
                continue
            row = out.setdefault(b, {"songs": set(), "tracks": 0, "plain": set(), "fields": {}, "rows": []})
            row["songs"].add(n)
            row["tracks"] += 1
            if not f:
                row["plain"].add(n)
            f = dict(f, **track_fx_fields(t))
            row["rows"].append((n, t["name"], f))
            for k, v in f.items():
                cell = row["fields"].setdefault(k, {}).setdefault(v, {"songs": set(), "tracks": 0})
                cell["songs"].add(n)
                cell["tracks"] += 1
    return {b: {"songs": sorted(r["songs"]), "tracks": r["tracks"], "plain": sorted(r["plain"]), "rows": r["rows"],
                "fields": {k: {v: {"songs": sorted(c["songs"]), "tracks": c["tracks"]} for v, c in vs.items()}
                           for k, vs in r["fields"].items()}}
            for b, r in out.items()}


def group_of(field):
    """Settings decided together: an eq band's cutoff, q and gain are one decision."""
    m = re.match(r"(.*\.bands\.\d+)\.", field)
    return m.group(1) if m else field


def agreed(row, least=3):
    """[(field, value, tracks, songs)] where a parent's songs agree: one value on MORE THAN HALF of the parent's tracks
    and in `least` songs or more; a band is taken only when every setting any track gives it is agreed."""
    n = row["tracks"]
    ok = {}
    for k, vs in row["fields"].items():
        v, c = max(vs.items(), key=lambda kv: kv[1]["tracks"])
        if 2 * c["tracks"] > n and len(c["songs"]) >= least:
            ok[k] = (v, c["tracks"], c["songs"])
    whole = {}
    for k in row["fields"]:
        whole.setdefault(group_of(k), []).append(k in ok)
    return sorted(((k, v, t, s) for k, (v, t, s) in ok.items() if all(whole[group_of(k)])), key=lambda q: (-q[2], q[0]))


def census_md(cen, album, least_songs=2):
    lines = [f"# {album}: what the songs did to the patches they share", "",
             "Written by `tools/patchbank.py census` from each song's plan as committed; do not edit by hand.",
             "A field is what a song set on top of the patch: an override (or its own patch's `extends`), or `+TYPE.PARAM`",
             "for an effect a track adds after the patch. AGREED: one value on more than half of the patch's tracks, in three",
             "songs or more: that is what `patchbank.py succeed` puts in the successor `NAME-2`. The rest each song chose.", ""]
    for b, row in sorted(cen.items(), key=lambda kv: (-len(kv[1]["songs"]), kv[0])):
        if len(row["songs"]) < least_songs or not row["fields"]:
            continue
        lines += [f"## `{b}`: {len(row['songs'])} songs, {row['tracks']} tracks"
                  + (f"; as it comes in tracks {', '.join(map(str, row['plain']))}" if row["plain"] else "; never as it comes"), ""]
        ok = {k for k, _, _, _ in agreed(row)}
        lines += ["| field | tracks | songs | values (the songs) | |", "|---|---|---|---|---|"]
        for k, vs in sorted(row["fields"].items(), key=lambda kv: -sum(c["tracks"] for c in kv[1].values())):
            songs = sorted({s for c in vs.values() for s in c["songs"]})
            vals = "; ".join(f"`{v}` in {', '.join(map(str, c['songs']))}"
                             for v, c in sorted(vs.items(), key=lambda kv: -kv[1]["tracks"])[:8])
            more = f"; and {len(vs) - 8} more values" if len(vs) > 8 else ""
            n_tracks = sum(c["tracks"] for c in vs.values())
            lines.append(f"| `{k}` | {n_tracks} | {len(songs)} | {vals}{more} | {'AGREED' if k in ok else ''} |")
        lines.append("")
    return "\n".join(lines) + "\n"


# ---- the engine ---------------------------------------------------------------------------------------------------------

def engine_planner(pin, cwd=None):
    def plan(song_path):
        env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
        r = subprocess.run([pin, "plan", "-f", os.path.abspath(song_path), "--json"], capture_output=True, text=True, env=env,
                           cwd=cwd or os.path.join(ROOT, "songs"))
        try:
            return json.loads(r.stdout)["data"]["canonical"]
        except (ValueError, KeyError, TypeError):
            raise SystemExit(f"patchbank: {os.path.basename(song_path)} does not plan: {r.stderr.strip()[-200:]}") from None
    return plan


def taken_names(pin):
    """Every patch name the engine knows (built-in and library)."""
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    r = subprocess.run([pin, "patch", "list"], capture_output=True, text=True, env=env, cwd=ROOT)
    return {ln.split()[0] for ln in r.stdout.splitlines() if ln.strip()}


def own_of(song_path):
    """({name}, {name: extends string}) for the patches a song file defines itself, inline ones as TRACK.patch."""
    import songfmt
    doc = songfmt.load(song_path)
    own, ext = set(), {}
    for name, p in (doc.get("patches") or {}).items():
        own.add(name)
        if isinstance(p, dict) and isinstance(p.get("extends"), str):
            ext[name] = p["extends"]

    def tracks(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if isinstance(t.get("patch"), dict) and t.get("name"):
                    if isinstance(t["patch"].get("extends"), str):
                        ext[f"{t['name']}.patch"] = t["patch"]["extends"]
                tracks(t.get("tracks"))
    tracks(doc.get("tracks"))
    return own, ext


def album_songs(album):
    """[(n, id, title, version, song path)] for an album's registered songs, in order."""
    import climb
    with open(os.path.join(ROOT, "compose", album, "album.json")) as f:
        titles = [t.get("title") if isinstance(t, dict) else str(t) for t in json.load(f).get("tracks") or []]
    out = []
    for n, title in enumerate(titles, 1):
        cid = f"{album}-t{n}"
        path = os.path.join(ROOT, "songs", f"{cid}.yaml")
        if not os.path.exists(path):
            continue
        vs = [e.get("version") for e in climb.history(cid) if e.get("version")]
        out.append((n, cid, title, vs[-1] if vs else "?", path))
    return out


# ---- writing a patch ------------------------------------------------------------------------------------------------------

def banked_about(patch, where, today):
    """The `about` of a banked patch: its own, then where it came from."""
    own = str(patch.get("about") or "").strip()
    own = own.split(f" {MARK}")[0].strip()
    lanes = lanes_of(patch)
    needs = (f" IT READS THE TRACK'S AUTOMATION ({', '.join('`' + x + '`' for x in lanes)}): give the track that plays it "
             f"`auto: {{{lanes[0]}: …}}`, as the song does." if lanes else "")
    return ((own + " " if own else "")
            + f"{MARK} ({today}) from {where}: every extends and override resolved, so it stands by itself.{needs}")


def with_track_fx(patch, track):
    """The patch with the track's own effects appended after its own (the instrument as the song plays it, before its bus)."""
    out = dict(patch)
    out["fx"] = list(patch.get("fx") or []) + list(track.get("fx") or [])
    return out


def write_patch(name, patch, dirpath=None):
    path = os.path.join(dirpath or os.path.join(ROOT, "patches"), f"{name}.yaml")
    with open(path + ".new", "w") as f:
        json.dump(patch, f, indent=1)
        f.write("\n")
    os.replace(path + ".new", path)
    return path


def may_write(name, taken, dirpath=None):
    """A banked name is new, or a file this tool wrote before (then it is written again)."""
    path = os.path.join(dirpath or os.path.join(ROOT, "patches"), f"{name}.yaml")
    if os.path.exists(path):
        try:
            with open(path) as f:
                return MARK in str(json.load(f).get("about") or "")
        except (OSError, ValueError, AttributeError):
            return False
    return name not in taken


def first_piece(patch):
    kit = patch.get("kit") if isinstance(patch, dict) else None
    return next(iter(kit)) if isinstance(kit, dict) and kit else None


def verify(names, plan):
    """{name: resolved patch} for banked names, planned again by name in one probe song (each on a track that defines
    the automation lanes it reads); if that song does not plan, one name at a time, so one bad file does not hide the
    others (a name that does not plan is not in the answer)."""
    def probe(some):
        tracks = []
        for i, name in enumerate(some):
            t = {"name": f"p{i}", "patch": name, "notes": [{"at": 0, "len": 1, "pitch": first_piece(names[name]) or "C3"}]}
            lanes = lanes_of(names[name])
            if lanes:
                t["auto"] = {lane: {"points": [["0b", 0.0]]} for lane in lanes}
            tracks.append(t)
        return {"tempo": 120, "tracks": tracks}

    def back(some):
        pats = plan_doc(plan, probe(some)).get("patches") or {}
        return {name: inline_kit(pats[name], pats) for name in some if name in pats}
    try:
        return back(list(names))
    except SystemExit:
        out = {}
        for name in names:
            try:
                out.update(back([name]))
            except SystemExit:
                pass
        return out


def on_disk(name, dirpath=None):
    path = os.path.join(dirpath or os.path.join(ROOT, "patches"), f"{name}.yaml")
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def bank(items, plan, taken, today, dirpath=None, dry=False, guard=None):
    """Write [(name, patch, where)]; -> {"new": [...], "changed": [...], "same": [...], "refused": [...], "wrong": [...],
    "held": [...]}. A name is refused when something else has it. A banked file whose instrument is unchanged is left
    as it is (its date and its song's version stay). CHANGED files are written only if guard({relpath: text}) is true
    (no registered song would change); else they are `held`. Each file written is planned again by name; one that
    does not come back the same is removed (`wrong`)."""
    res = {"new": [], "changed": [], "same": [], "refused": [], "wrong": [], "held": []}
    todo = {}
    for name, patch, where in items:
        if not may_write(name, taken, dirpath):
            res["refused"].append(name)
            continue
        old = on_disk(name, dirpath)
        if old is not None and same_patch(old, patch):
            res["same"].append(name)
            continue
        todo[name] = dict(patch, about=banked_about(patch, where, today))
        res["changed" if old is not None else "new"].append(name)
    if res["changed"] and not dry:
        texts = {os.path.join("patches", f"{n}.yaml"): json.dumps(todo[n], indent=1) + "\n" for n in res["changed"]}
        if guard is not None and not guard(texts):
            res["held"], res["changed"] = res["changed"], []
            for n in res["held"]:
                todo.pop(n)
    if dry or not todo:
        return res
    before = {n: on_disk(n, dirpath) for n in todo}
    for name, patch in todo.items():
        write_patch(name, patch, dirpath)
    back = verify(todo, plan)
    for name, patch in todo.items():
        if name in back and same_patch(back[name], patch):
            continue
        if before[name] is None:
            os.remove(os.path.join(dirpath or os.path.join(ROOT, "patches"), f"{name}.yaml"))
        else:
            write_patch(name, before[name], dirpath)
        res["wrong"].append(name)
        for k in ("new", "changed"):
            if name in res[k]:
                res[k].remove(name)
    return res


def index_md(items, album, cmd, dirpath=None):
    """The index of what was banked: name, where it came from, what it is."""
    lines = [f"# {album}: " + ("the instruments banked in the library" if cmd == "promote" else "successors"), "",
             f"Written by `tools/patchbank.py {cmd} {album} --md`; do not edit by hand. Each name is a file in `patches/`,",
             "resolved and self-contained: `patch: NAME` on a track gives the instrument as the song plays it.", "",
             "| name | from | what |", "|---|---|---|"]
    for name, patch, where in sorted(items):
        disk = str((on_disk(name, dirpath) or {}).get("about") or "")
        m = re.search(re.escape(MARK) + r" \([^)]*\) from (.*?): every extends and override resolved", disk, re.S)
        where = m.group(1) if m else where                       # as the FILE says: the version it was last banked from
        what = str(patch.get("about") or "").split(f" {MARK}")[0].replace("|", "/").replace("\n", " ").strip()
        kit = f"a kit of {len(patch['kit'])} pieces. " if isinstance(patch.get("kit"), dict) else ""
        lines.append(f"| `{name}` | {where.replace('|', '/')} | {kit}{what[:220]}{'…' if len(what) > 220 else ''} |")
    return "\n".join(lines) + "\n"


def libguard_ok(pin):
    """A guard for bank(): true when no registered song's plan changes under these library texts."""
    def guard(texts):
        import libguard
        code, lines = libguard.verdict(libguard.check(overlay=texts, root=ROOT, pin=pin))
        if code:
            print("\n".join(lines), file=sys.stderr)
        return code == 0
    return guard


def say(res, what, dry):
    lines = [f"patchbank: {what}: {len(res['new'])} new, {len(res['changed'])} changed, {len(res['same'])} as banked"
             + (" (nothing written: --dry)" if dry else "")]
    for key, text in (("new", "new"), ("changed", "changed"),
                      ("held", "HELD: a song uses the banked name and would change; bank it under a new name with `take`"),
                      ("refused", "REFUSED: the name is taken by a file this tool did not write"),
                      ("wrong", "DID NOT COME BACK THE SAME when planned by name; not written")):
        if res[key]:
            lines.append(f"  {text}: {' '.join(sorted(res[key]))}")
    return lines


# ---- promote: each song's kit as played, and its own instruments ----------------------------------------------------

def plan_doc(plan, doc):
    """The canonical plan of a song given as a document."""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="patchbank-probe-")
    with os.fdopen(fd, "w") as f:
        json.dump(doc, f)
    try:
        return plan(path)
    finally:
        os.remove(path)


def pieces_of(track):
    return {str(n.get("pitch")) for n in track.get("notes") or [] if isinstance(n, dict)}


def body_of(patch):
    return {k: v for k, v in patch.items() if k not in ("kit", "about")}


def merge_kit(tracks):
    """(kit patch, [merged track names], [indexes left out]) for one song's tracks on one kit family, in the song's order.
    tracks: [(name, resolved kit patch, {pieces it plays})]. The kit starts as the first track's; each PIECE is then
    taken from the track that plays it. A track is left out (to be banked by itself) when a piece it plays is already
    another track's with a different sound, or when it differs outside the pieces (its own effects, level or `play`)."""
    first = tracks[0][1]
    out = dict(first, kit=dict(first["kit"]))
    claimed, merged, left = {}, [], []
    for i, (name, patch, pieces) in enumerate(tracks):
        mine = {p: patch["kit"][p] for p in pieces if p in patch["kit"]}
        if body_of(patch) != body_of(first) or any(p in claimed and claimed[p] != d for p, d in mine.items()):
            left.append(i)
            continue
        claimed.update(mine)
        out["kit"].update(mine)
        merged.append(name)
    return out, merged, left


def root_of(base, own, ext):
    """The library or built-in patch a song's own patch comes from (itself when it extends nothing)."""
    seen = set()
    while (base in own or base.endswith(".patch")) and base in ext and base not in seen:
        seen.add(base)
        base = base_of(ext[base])
    return base


def named(found, taken, dirpath=None):
    """[(name, patch, where)] under names nothing else has. found: [(n, title, version, wanted name, patch, tracks)].
    `-here` in a song's own name becomes the song's title; a name the engine, the library or another song has gains
    the title; the same instrument in two songs is one file."""
    count = {}
    for n, _, _, want, patch, _ in found:
        count.setdefault(want, []).append((n, patch))
    out = []
    for n, title, version, want, patch, tracks in found:
        others = [p for m, p in count[want] if m != n]
        name = want
        if re.search(r"-here(?=-|$)", want):
            name = re.sub(r"-here(?=-|$)", f"-{slug(title)}", want)
        elif not may_write(want, taken, dirpath) or (others and not all(same_patch(p, patch) for p in others)):
            name = f"{want}-{slug(title)}"                       # (a file this tool wrote keeps its name)
        where = f"{title} {version} (track{'s' if len(tracks) > 1 else ''} {', '.join(tracks[:10])})"
        twin = next((o for o in out if o[0] == name), None)
        if twin is not None:
            if same_patch(twin[1], patch):
                continue
            name = f"{name}-t{n}"
        out.append((name, patch, where))
    return out


def instruments(rows, taken, dirpath=None):
    """([(name, patch, where)], [(song n, ref, why)]): what `promote` banks, and what it leaves out.
    rows: [{n, title, version, canon, own, ext}].
    1. EACH SONG'S KIT AS PLAYED. Its kit tracks are grouped by the kit they come from (the library's, or a song's own
       that extends it) and merged (merge_kit); a kit every track plays as it comes from the library is not banked.
       The name is ROOT-TITLE where two songs or more play that root (`ct-kit-so-far`), else the song's own name.
       Tracks that cannot join it (the same pieces with another sound: a second tuning) make a kit of their own,
       together where they are on the same patch of the song's.
    2. EVERY OTHER PATCH OF THE SONG'S OWN that a track plays; one played only with overrides is banked as played."""
    shared = {}
    for r in rows:
        pats = r["canon"].get("patches") or {}
        for t in walk(r["canon"].get("tracks")):
            p = pats.get(t["patch"])
            if isinstance(p, dict) and isinstance(p.get("kit"), dict):
                shared.setdefault(root_of(base_of(t["patch"]), r["own"], r["ext"]), set()).add(r["n"])
    found, skipped = [], []
    for r in rows:
        n, title, version, own, ext = r["n"], r["title"], r["version"], r["own"], r["ext"]
        pats = r["canon"].get("patches") or {}
        fams, plain = {}, {}
        for t in walk(r["canon"].get("tracks")):
            ref = t["patch"]
            b = base_of(ref)
            patch = pats.get(ref)
            if isinstance(patch, dict) and isinstance(patch.get("kit"), dict):
                fams.setdefault(root_of(b, own, ext), []).append((t["name"], inline_kit(patch, pats), pieces_of(t), ref))
            elif b in own or b.endswith(".patch"):
                plain.setdefault(ref, []).append(t["name"])
        for root, ts in fams.items():
            mine = lambda b: b in own or b.endswith(".patch")     # noqa: E731
            if not mine(root) and all(ref == root for _, _, _, ref in ts):
                continue                                         # the library's kit as it comes: nothing to bank
            used = set()

            def add(group, want):
                """Merge a group into kits: the first under `want`, what cannot join it under want-TRACK."""
                while group:
                    kit, merged, left = merge_kit([(name, patch, pieces) for name, patch, pieces, _ in group])
                    name = want if want not in used else f"{want}-{slug(merged[0])}"
                    used.add(name)
                    found.append((n, title, version, name, kit, merged))
                    group = [group[i] for i in left]

            def own_name(b):
                return f"{slug(title)}-{b[:-6]}" if b.endswith(".patch") else b

            bases = {base_of(ref) for _, _, _, ref in ts}
            b0 = next(iter(bases))
            if len(bases) == 1 and mine(b0) and len(shared.get(root, ())) < 2:
                add(list(ts), own_name(b0))                      # one kit of the song's own, of a root no other song plays
                continue
            kit, merged, left = merge_kit([(name, patch, pieces) for name, patch, pieces, _ in ts])
            used.add(f"{root}-here")
            found.append((n, title, version, f"{root}-here", kit, merged))
            groups = {}
            for i in left:                                       # what cannot join it: by the patch each is on
                groups.setdefault(base_of(ts[i][3]), []).append(ts[i])
            for b, group in groups.items():
                add(group, own_name(b) if mine(b) else f"{root}-here-{slug(group[0][0])}")
        by_base = {}
        for ref in plain:
            by_base.setdefault(base_of(ref), []).append(ref)
        for ref, names in plain.items():
            patch = pats.get(ref)
            if not isinstance(patch, dict):
                skipped.append((n, ref, "not in the plan"))
                continue
            if plays_a_song(patch):
                skipped.append((n, ref, "plays a song inside the song"))
                continue
            b = base_of(ref)
            stem = f"{slug(title)}-{b[:-6]}" if b.endswith(".patch") else b
            want = stem if len(by_base[b]) == 1 or ref == b else f"{stem}-{slug(names[0])}"
            found.append((n, title, version, want, patch, names))
    return named(found, taken, dirpath), skipped


# ---- succeed: a successor for each shared patch the songs agree about ----------------------------------------------

def exemplar(row, ok):
    """The track that is nearest the agreed settings: it has them all (or most) and the fewest others."""
    want = {k: v for k, v, _, _ in ok}
    return min(row["rows"], key=lambda r: (sum(1 for k, v in want.items() if r[2].get(k) != v),
                                          sum(1 for k in r[2] if k not in want), r[0]))


def successors(cen, rows, plan, taken, kits=()):
    """[(name, patch, where)] and [(parent, why)] left out. For each parent with agreed settings: PARENT-2 is the
    parent with the agreed overrides resolved by the engine, and each effect type the tracks agree about appended
    after the patch's own (the effect as the nearest track has it, the agreed values in it)."""
    by_n = {r["n"]: r for r in rows}
    out, left = [], []
    for parent, row in sorted(cen.items()):
        ok = agreed(row)
        if not ok:
            continue
        if parent in kits:
            left.append((parent, "a kit: each song's is banked as played (promote)"))
            continue
        plain = [(k, v) for k, v, _, _ in ok if not k.startswith("+")]
        added = {}
        for k, v, _, _ in ok:
            if k.startswith("+"):
                added.setdefault(k[1:].split(".", 1)[0], {})[k[1:].split(".", 1)[1]] = v
        ref = " ".join([parent] + [shlex.quote(f"{k}={v}") if " " in v else f"{k}={v}" for k, v in plain])
        probe = {"tempo": 120, "tracks": [{"name": "p", "patch": ref, "notes": [{"at": 0, "len": 1, "pitch": "C3"}]}]}
        patch = (plan_doc(plan, probe).get("patches") or {}).get(ref)
        if not isinstance(patch, dict):
            left.append((parent, "does not resolve by itself"))
            continue
        ex_n, ex_track, _ = exemplar(row, ok)
        note = []
        if added:
            src = next((t for t in walk(by_n[ex_n]["canon"].get("tracks")) if t["name"] == ex_track), {})
            patch = dict(patch, fx=list(patch.get("fx") or []))
            for e in src.get("fx") or []:
                if isinstance(e, dict) and e.get("type") in added:
                    patch["fx"].append(e)
                    note.append(f"a `{e['type']}` after the patch's own effects, as {by_n[ex_n]['title']}'s `{ex_track}` has it "
                                f"({json.dumps({k: v for k, v in e.items() if k != 'type'}, sort_keys=True)})")
                    added.pop(e["type"])
        where = (f"`{parent}` as the songs left it: "
                 + "; ".join(f"`{k}={v}` ({t} of {row['tracks']} tracks, {len(s)} songs)" for k, v, t, s in ok if not k.startswith("+"))
                 + ("; " if plain and note else "") + "; ".join(note)
                 + f". The songs that use `{parent}`: tracks {', '.join(map(str, row['songs']))}. A RULE'S SUCCESSOR, NOT HEARD")
        out.append((f"{parent}-2", patch, where))
    return out, left


# ---- commands -----------------------------------------------------------------------------------------------------------

def load_album(album, plan):
    rows = []
    for n, cid, title, version, path in album_songs(album):
        own, ext = own_of(path)
        rows.append({"n": n, "id": cid, "title": title, "version": version, "path": path, "canon": plan(path),
                     "own": own, "ext": ext})
    return rows


def strip_notes(o):
    if isinstance(o, dict):
        return {k: strip_notes(v) for k, v in o.items() if k != "notes"}
    if isinstance(o, list):
        return [strip_notes(v) for v in o]
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["census", "promote", "succeed", "take", "archive"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--md")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--fx", action="store_true")
    ap.add_argument("--about")
    ap.add_argument("--pin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    plan = engine_planner(pin)
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%d %b %Y")
    if a.cmd == "take":
        if len(a.args) != 3:
            raise SystemExit("patchbank: take ID TRACK NAME")
        cid, track, name = a.args
        canon = plan(os.path.join(ROOT, "songs", f"{cid}.yaml"))
        t = next((t for t in walk(canon.get("tracks")) if t["name"] == track), None)
        if t is None:
            raise SystemExit(f"patchbank: {cid} has no track {track} with a patch")
        patch = (canon.get("patches") or {}).get(t["patch"])
        if not isinstance(patch, dict) or plays_a_song(patch):
            raise SystemExit(f"patchbank: {cid} {track}: nothing to bank (its patch plays a song, or is not in the plan)")
        patch = inline_kit(patch, canon.get("patches") or {})
        if a.fx:
            patch = with_track_fx(patch, t)
        import climb
        vs = [e.get("version") for e in climb.history(cid) if e.get("version")]
        fx_note = (f"; with the track's own {len(t.get('fx') or [])} effects after the patch's" if a.fx
                   else "; the track's own effects are not in it")
        where = (f"{cid} {vs[-1] if vs else '?'}, track {track}, as played (`{t['patch'][:200]}`{fx_note})"
                 + (f". {a.about}" if a.about else ""))
        res = bank([(name, patch, where)], plan, taken_names(pin), today, dry=a.dry, guard=libguard_ok(pin))
        print(json.dumps(res) if a.json else "\n".join(say(res, f"{cid} {track} as {name}", a.dry)))
        return 1 if res["refused"] or res["wrong"] or res["held"] else 0
    if len(a.args) != 1:
        raise SystemExit(f"patchbank: {a.cmd} ALBUM")
    album = a.args[0]
    rows = load_album(album, plan)
    cen = census([(r["n"], r["canon"], r["own"], r["ext"]) for r in rows])
    if a.cmd == "census":
        if a.json:
            print(json.dumps(cen))
            return 0
        if a.md:
            with open(a.md, "w") as f:
                f.write(census_md(cen, album))
        for b, row in sorted(cen.items(), key=lambda kv: -len(kv[1]["songs"])):
            ok = agreed(row)
            if ok:
                print(f"{b}: {len(row['songs'])} songs, {row['tracks']} tracks; agreed: "
                      + "; ".join(f"{k}={v} ({t} tracks, {len(s)} songs)" for k, v, t, s in ok))
        return 0
    if a.cmd in ("promote", "succeed"):
        taken = taken_names(pin)
        if a.cmd == "promote":
            items, skipped = instruments(rows, taken)
        else:
            kits = {b for r in rows for b, p in ((base_of(k), v) for k, v in (r["canon"].get("patches") or {}).items())
                    if isinstance(p, dict) and isinstance(p.get("kit"), dict)}
            items, skipped = successors(cen, rows, plan, taken, kits)
        res = bank(items, plan, taken, today, dry=a.dry, guard=libguard_ok(pin))
        if a.md and not a.dry:
            with open(a.md, "w") as f:
                f.write(index_md(items, album, a.cmd))
        if a.json:
            print(json.dumps(dict(res, skipped=skipped)))
        else:
            what = "the songs' kits as played and their own instruments" if a.cmd == "promote" else "successors"
            print("\n".join(say(res, f"{album}: {len(items)} {what}", a.dry)))
            for q in skipped:
                print("  left out: " + (f"track {q[0]} `{q[1][:60]}`: {q[2]}" if len(q) == 3 else f"`{q[0]}`: {q[1]}"))
        return 1 if res["refused"] or res["wrong"] or res["held"] else 0
    # archive
    out_dir = os.path.join(ROOT, "compose", album, "bank")
    os.makedirs(out_dir, exist_ok=True)
    for r in rows:
        with open(r["path"], "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()[:16]
        doc = {"id": r["id"], "title": r["title"], "version": r["version"], "pin": os.path.basename(pin), "song_sha256": sha,
               "what": "the song's canonical plan without its notes: every patch, bus and effect as the engine resolved them",
               "plan": strip_notes(r["canon"])}
        with open(os.path.join(out_dir, f"{r['id']}.json"), "w") as f:
            json.dump(doc, f, sort_keys=True, separators=(",", ":"))
            f.write("\n")
        print(f"  {r['id']} {r['version']}: {len((r['canon'].get('patches') or {}))} patches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
