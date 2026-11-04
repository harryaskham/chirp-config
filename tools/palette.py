#!/usr/bin/env python3
"""palette: a PALETTE round's brief for a composed song (Harry, 2 Nov: "specific climb types like considering used
instruments / adding new ones").

  palette.py ID [--all] [--grep WORD] [--pin BIN]

Prints the song's instruments (track -> patch, and what each patch is made of), the album's staples (library patches
three or more of its songs share), library patches no song on the album uses yet (with their `about` lines), the
song's own inline patches (candidates for the library), and the engine features the album has not used
(compose/<album>/features.md). A palette round changes one or two instruments: swap a staple for something no other
track uses, design a new patch, or add the part the song lacks, measured on full-length renders.
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
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("--all", action="store_true", help="list every unused library patch (default: 40)")
    ap.add_argument("--grep", help="only unused library patches whose name or about matches")
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


if __name__ == "__main__":
    main()
