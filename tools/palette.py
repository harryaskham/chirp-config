#!/usr/bin/env python3
"""palette: a PALETTE round's brief for a composed song (Harry, 2 Nov: "specific climb types like considering used
instruments / adding new ones").

  palette.py ID [--all] [--grep WORD] [--roles] [--pin BIN]
  palette.py ID --bench TRACK FROM-TO PATCH[@DB] ... [--layer]     (swap or layer? tools/swapbench.py: the same notes
                                                                    on another patch, alone through the track's routing)

Prints the song's instruments (track -> patch, and what each patch is made of), the album's staples (library patches
three or more of its songs share), library patches no song on the album uses yet (with their `about` lines), the
song's own inline patches (candidates for the library), and the engine features the album has not used
(compose/<album>/features.md). A palette round changes one or two instruments: swap a staple for something no other
track uses, design a new patch, or add the part the song lacks, measured on full-length renders.

WHAT A STAPLE DOES HERE (14 Nov, chirper-zero's ask after Plain Hunt v2: a bowed bass swapped for a voice with no
fundamental took the low end out of three passages, and only the scorer said so). Under each staple, a "here:" line
for each of this song's tracks that plays it, read from the plan's notes with no render: its register as written,
how many bars it sounds in, in how many it is the lowest written part, and in which bars it is THE FLOOR: an
octave or more under every other pitched part, or the only pitched part there is. Those bars are what a swap must
go on holding. --roles prints the line for every track, not only the staples'. "As written": a patch's own octave,
its filters and how loud it is are not read (a part written low that has no fundamental still counts as low), and
drums count only as hits; for what a part really holds in a band, tools/stembal.py --parts.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compscore as CS  # noqa: E402
import notechk  # noqa: E402
import pitchbench  # noqa: E402

ROOT = CS.ROOT


def library(pin=None):
    """{name: about} of every patch chirp knows (the user library and the engine's built-ins: `chirp patch list`); the
    patches/ directory when the binary can't be asked."""
    if pin:
        r = subprocess.run([pin, "--json", "patch", "list"], cwd=ROOT, capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            items = d.get("data", d)
            items = items if isinstance(items, list) else items.get("patches", [])
            return {p["name"]: (p.get("about") or "").strip() for p in items if p.get("name")}
        except (ValueError, KeyError, TypeError, AttributeError):
            pass
    out = {}
    d = os.path.join(ROOT, "patches")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not fn.endswith(".yaml"):
            continue
        about = ""
        try:
            with open(os.path.join(d, fn)) as f:
                m = re.search(r'^about:\s*"?(.*?)"?\s*$', f.read(), re.M)
                about = m.group(1) if m else ""
        except OSError:
            pass
        out[fn[:-5]] = about
    return out


def base(key, lib):
    """The library patch a canonical patch key comes from: 'machine-kit.cb' -> machine-kit, 'blip amp.d=30ms' -> blip;
    None for a song's own patch."""
    k = key.split()[0]
    for cand in (k, k.split(".")[0]):
        if cand in lib:
            return cand
    return None


def kit_voices(cn, lib):
    """{(library kit, voice)} a song's tracks actually PLAY. A kit counts as one library patch in the staples, but what two
    songs share is a voice: machine-kit's kick in six songs is much of what makes neighbours read alike in 'distinct'
    (chirper-three, t11 v47, 4 Nov). The plan lists every voice of a kit, so the voices come from the notes."""
    pats = (cn or {}).get("patches") or {}
    got, stack = set(), list((cn or {}).get("tracks") or [])
    while stack:
        t = stack.pop()
        stack.extend(t.get("tracks") or [])
        pk = t.get("patch")
        b = base(pk, lib) if isinstance(pk, str) else None
        kit = (pats.get(pk) or {}).get("kit") if b else None
        if not isinstance(kit, dict):
            continue
        for n in t.get("notes") or []:
            v = n.get("pitch") if isinstance(n, dict) else None
            if isinstance(v, str) and v in kit:
                got.add((b, v))
    return got


def summary(p):
    """What a canonical patch is made of, in a few words: layer types (with wind exciters and modal mode sets), fx."""
    if not isinstance(p, dict):
        return ""
    syn = p.get("synth") or {}
    parts = []
    for ly in syn.get("layers") or []:
        if isinstance(ly, dict):
            t = ly.get("type", "osc")
            if t == "wind":
                t = f"wind:{ly.get('exciter', 'reed')}"
            elif t == "modal" and isinstance(ly.get("modes", "membrane"), str):
                t = f"modal:{ly.get('modes', 'membrane')}"
            elif t == "osc":
                t = f"osc:{ly.get('wave') or 'sine'}"
            parts.append(t)
    if p.get("kit") or p.get("voices"):
        parts.append("kit")
    fx = [f.get("type") for f in p.get("fx") or [] if isinstance(f, dict) and f.get("type")]
    s = "+".join(dict.fromkeys(parts)) or "?"
    return s + (f" | fx {','.join(dict.fromkeys(fx))}" if fx else "")


FLATS = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def note_name(m):
    """A MIDI number as the album writes pitches: 29 -> "F1" (C4 = 60)."""
    m = int(round(m))
    return f"{FLATS[m % 12]}{m // 12 - 1}"


def spans(bars):
    """Bars (0-indexed) as ranges the way `chirp render` counts them: [0, 1, 2, 7] -> "1-3, 8"."""
    out, run = [], []
    for b in sorted(set(bars)):
        if run and b == run[-1] + 1:
            run.append(b)
        else:
            if run:
                out.append(run)
            run = [b]
    if run:
        out.append(run)
    return ", ".join(f"{r[0] + 1}" if len(r) == 1 else f"{r[0] + 1}-{r[-1] + 1}" for r in out)


def roles(canon):
    """{track: role} for the song's top-level tracks that have notes, from the plan alone (as written; a warped
    track where it sounds). A pitched track: {"lo", "hi" (pitch names), "lo_hz", "hi_hz", "bars" (it sounds in),
    "lowest" (bars where it is the lowest written part), "floor" (bars, 0-indexed, where it is an octave or more
    under every other pitched part, or the only one), "of" (the song's bars)}. A kit's track: {"kit": True, "hits",
    "bars", "of"}. Bars are read in 4/4; a song whose tempo changes or whose meter is
    another gets registers and hits only ("of" is None)."""
    pats = canon.get("patches") or {}
    tempo = canon.get("tempo", 120.0)
    barred = (isinstance(tempo, (int, float)) and not isinstance(tempo, bool)
              and str(canon.get("meter") or "4/4").replace(" ", "") == "4/4")
    got, sounding, total = {}, {}, 0
    for t in canon.get("tracks") or []:
        name, pk = t.get("name"), t.get("patch")
        try:
            notes = notechk.track_notes(canon, name) or []
        except SystemExit:
            notes = [n for n in t.get("notes") or [] if isinstance(n, dict)]
        if not name or not notes:
            continue
        p = pats.get(pk) if isinstance(pk, str) else pk
        is_kit = isinstance(p, dict) and bool(p.get("kit") or p.get("voices"))
        rows = []
        for n in notes:
            at, ln = float(n.get("at") or 0), float(n.get("len") or 0)
            try:
                m = None if is_kit else pitchbench.midi(n.get("pitch"))
            except ValueError:
                m = None
            b0, b1 = int(at // 4), int(max(at, at + ln - 1e-6) // 4)
            rows.append((m, range(b0, b1 + 1)))
            total = max(total, b1 + 1)
        bars = sorted({b for _, r in rows for b in r})
        pitched = [m for m, _ in rows if m is not None]
        if not pitched:
            got[name] = {"kit": True, "hits": len(rows), "bars": len(bars)}
            continue
        low = {}
        for m, r in rows:
            if m is not None:
                for b in r:
                    low[b] = min(low.get(b, m), m)
        sounding[name] = low
        lo, hi = min(pitched), max(pitched)
        got[name] = {"lo": note_name(lo), "hi": note_name(hi), "lo_hz": round(pitchbench.hz(lo), 1),
                     "hi_hz": round(pitchbench.hz(hi), 1), "bars": len(low)}
    for name, r in got.items():
        r["of"] = total if barred else None
        if r.get("kit") or not barred:
            continue
        mine = sounding[name]
        others = [v for k, v in sounding.items() if k != name]
        r["lowest"] = sum(1 for b, m in mine.items() if all(o.get(b, 999) >= m for o in others))
        r["floor"] = sorted(b for b, m in mine.items() if all(o.get(b, 999) >= m + 12 for o in others))
    return got


def role_line(name, r):
    """One track's role as a line of the brief."""
    if r.get("kit"):
        return f"{name}: a kit's part, {r['hits']} hits" + (f" in {r['bars']} of {r['of']} bars" if r.get("of") else "")
    reg = r["lo"] if r["lo"] == r["hi"] else f"{r['lo']}-{r['hi']}"
    hz = f"{r['lo_hz']:g} Hz" if r["lo"] == r["hi"] else f"{r['lo_hz']:g}-{r['hi_hz']:g} Hz"
    s = f"{name}: {reg} ({hz}) as written"
    if r.get("of"):
        s += f"; sounds in {r['bars']} of {r['of']} bars; the lowest written part in {r['lowest']}"
        if r["floor"]:
            s += f"; THE FLOOR (an octave or more under every other pitched part) in {len(r['floor'])}: bars {spans(r['floor'])}"
    return s


def plan(song, pin):
    r = subprocess.run([pin, "--json", "plan", "-f", song], cwd=ROOT, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        return None


def album_songs(album_id):
    reg = CS.load_climbs() if hasattr(CS, "load_climbs") else None
    if reg is None:
        with open(os.path.join(ROOT, "climbs.json")) as f:
            reg = json.load(f)
    items = reg.get("climbs", reg) if isinstance(reg, dict) else reg
    items = items.values() if isinstance(items, dict) else items
    out = []
    for c in items:
        if (c.get("album") or (c.get("compose") or {}).get("album")) == album_id:
            out.append((c["id"], os.path.join(ROOT, c.get("song") or f"songs/{c['id']}.yaml")))
    return sorted(out)


def unused_features(album_id):
    try:
        with open(os.path.join(ROOT, "compose", album_id, "features.md")) as f:
            m = re.search(r"\*\*Not used by any track yet:\*\*\s*(.*)", f.read())
            return m.group(1).strip() if m else None
    except OSError:
        return None


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--bench" in argv:                               # swap or layer: the bench, not the brief
        import swapbench
        i = argv.index("--bench")
        return swapbench.main(argv[:i] + argv[i + 1:])
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("--all", action="store_true", help="list every unused library patch (default: 40)")
    ap.add_argument("--grep", help="only unused library patches whose name or about matches")
    ap.add_argument("--roles", action="store_true", help="what EVERY track does in the song (from the plan), not only the staples'")
    ap.add_argument("--pin", help="chirp binary (default: tools/groove-pin)")
    ap.add_argument("--as", dest="as_", help=argparse.SUPPRESS)
    ap.add_argument("--no-git", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    c = CS.climb_of(a.id)
    album_id = c.get("album") or (c.get("compose") or {}).get("album")
    lib = library(pin)
    song = os.path.join(ROOT, c.get("song") or f"songs/{a.id}.yaml")
    canon = plan(song, pin)
    if canon is None:
        raise SystemExit(f"palette: {song} does not plan with {pin}")
    pats = canon.get("patches") or {}
    print(f"{a.id}: PALETTE — the song's instruments, the album's staples, what the library and the engine still offer")
    print("this song's tracks:")
    for t in canon.get("tracks") or []:
        pk = t.get("patch")
        name = pk if isinstance(pk, str) else "(inline)"
        p = pats.get(pk) if isinstance(pk, str) else pk
        src = f"library {base(pk, lib)}" if isinstance(pk, str) and base(pk, lib) else "song's own"
        print(f"  {t.get('name', '?'):<14} {name[:28]:<28} {src:<22} {summary(p)}")
    role = roles(canon)
    if a.roles:
        print("what each track does here (from the plan's notes, as written; no render):")
        for t in canon.get("tracks") or []:
            if t.get("name") in role:
                print("  " + role_line(t["name"], role[t["name"]]))
    own = [k for k in pats if not base(k, lib) and "." not in k.split()[0]]
    if own:
        print(f"this song's own patches (library candidates if they are good): {', '.join(own)}")
    used, voices = {}, {}
    for cid, sp in album_songs(album_id):
        cn = canon if cid == a.id else plan(sp, pin)
        for k in (cn or {}).get("patches") or {}:
            b = base(k, lib)
            if b:
                used.setdefault(b, set()).add(cid.rsplit("-", 1)[-1])
        for b, v in kit_voices(cn, lib):
            voices.setdefault(f"{b}.{v}", set()).add(cid.rsplit("-", 1)[-1])
    staples = sorted(((b, s) for b, s in used.items() if len(s) >= 3), key=lambda t: -len(t[1]))
    if staples:
        print("album staples (library patches 3+ songs share; a swap here adds variety):")
        for b, s in staples:
            print(f"  {b:<16} {len(s)} songs ({', '.join(sorted(s, key=lambda x: int(x[1:]) if x[1:].isdigit() else 0))})")
            for t in canon.get("tracks") or []:                 # what the staple does in THIS song, before it is swapped
                if isinstance(t.get("patch"), str) and base(t["patch"], lib) == b and t.get("name") in role:
                    print("      here: " + role_line(t["name"], role[t["name"]]))
    shared = sorted(((k, s) for k, s in voices.items() if len(s) >= 3), key=lambda t: (-len(t[1]), t[0]))
    if shared:
        print("kit voices 3+ songs play (the staple inside a kit: another kit's voice or a drum of the song's own steps away):")
        for k, s in shared:
            print(f"  {k:<16} {len(s)} songs ({', '.join(sorted(s, key=lambda x: int(x[1:]) if x[1:].isdigit() else 0))})")
    unused = [(n, ab) for n, ab in lib.items() if n not in used]
    if a.grep:
        g = a.grep.lower()
        unused = [(n, ab) for n, ab in unused if g in n.lower() or g in ab.lower()]
    print(f"library patches no song on {album_id} uses ({len(unused)} of {len(lib)}"
          + (f", matching '{a.grep}'" if a.grep else "") + "; families of 5+ on one line):")
    fam = {}
    for n, ab in unused:
        if "-" in n:
            fam.setdefault(n.split("-")[0], []).append((n, ab))
    lines = []
    for n, ab in unused:
        f = fam.get(n.split("-")[0]) if "-" in n else None
        if f and len(f) >= 5:
            if f[0][0] == n:
                lines.append(f"  {n.split('-')[0] + '-*':<20} ({len(f)}: {', '.join(x[0].split('-', 1)[1] for x in f)[:80]}) "
                             f"{f[0][1][:40]}")
            continue
        lines.append(f"  {n:<20} {ab[:96]}")
    for ln in (lines if a.all or a.grep else lines[:40]):
        print(ln)
    if not (a.all or a.grep) and len(lines) > 40:
        print(f"  … {len(lines) - 40} more (--all, or --grep WORD)")
    uf = unused_features(album_id)
    if uf:
        print(f"engine features the album has not used yet (compose/{album_id}/features.md): {uf}")
    print("a palette round: change one or two instruments (swap a staple for something no other track uses, design a new "
          "patch, or add the part the song lacks), measured on full-length renders; note the swap in the round note.")
    print(f"swap or layer? before the full render: `chirpers.py palette {a.id} --bench TRACK FROM-TO PATCH[@DB] [--layer]` "
          "(the same notes on the new patch, alone through the track's own routing: the bands a swap LOSES, whether a "
          "layer is THERE).")


if __name__ == "__main__":
    main()
