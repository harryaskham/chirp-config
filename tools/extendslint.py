#!/usr/bin/env python3
"""extendslint: a patch override that silently drops its base's modulation (chirp-eco, 9 Nov). A song's patch can
`extends` a library patch and override fields; a LIST it sets (pitch.mod, an LFO's routes) REPLACES the base's list
rather than merging, so an override that adds one route to `synth.pitch.mod` loses the base's vibrato route unless it
copies the whole list (chirper-three's t8 v82: "extends REPLACES a patch pitch.mod list - copy the whole list when
overriding").

  extendslint.py [ID|FILE …] [--album NAME] [--json]     (default: the focus album's songs)

For every dict in a song with `extends: NAME`, each list it sets under a key named `mod` is compared with the base
patch's list at the same path (the base resolved by `chirp patch show NAME --resolved`, or the song's own `patches`
map); every base route (by `src`) the override no longer has is reported. Deliberate drops are fine: this only says
what was lost. Read-only; exits 1 when anything is flagged.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)


def load_song(path):
    with open(path) as f:
        text = f.read()
    try:
        return json.loads(text)
    except ValueError:
        import songfmt                      # the tools' own YAML reader (onsetsnap uses it too)
        return songfmt.load(path)


def route_key(r):
    return r.get("src") if isinstance(r, dict) and "src" in r else json.dumps(r, sort_keys=True)


def dropped(override, base, path=()):
    """[(path, [base routes missing from the override's list])] for every `mod` list the override sets."""
    out = []
    if not isinstance(override, dict) or not isinstance(base, dict):
        return out
    for k, v in override.items():
        b = base.get(k)
        if k == "mod" and isinstance(v, list) and isinstance(b, list):
            have = {route_key(r) for r in v}
            lost = [r for r in b if route_key(r) not in have]
            if lost:
                out.append((".".join(path + (k,)), lost))
        elif isinstance(v, dict) and isinstance(b, dict):
            out.extend(dropped(v, b, path + (k,)))
    return out


_BASES = {}


def library_base(name, pin):
    """The library patch NAME with its own extends merged, or None."""
    if name not in _BASES:
        r = subprocess.run([pin, "patch", "show", name, "--resolved", "--json"], capture_output=True, text=True)
        try:
            _BASES[name] = json.loads(r.stdout)["data"]["patch"]
        except (ValueError, KeyError, TypeError):
            _BASES[name] = None
    return _BASES[name]


def overrides(node, where="song"):
    """[(label, override dict)] for every dict with a string `extends` (track patches, buses, local patches); the label
    is the nearest enclosing `name`, else the path."""
    out = []
    if isinstance(node, dict):
        here = node.get("name") if isinstance(node.get("name"), str) else where
        if isinstance(node.get("extends"), str):
            out.append((here, node))
        for k, v in node.items():
            if k != "extends":
                out.extend(overrides(v, here if here != "song" else f"song.{k}"))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.extend(overrides(v, f"{where}[{i}]"))
    return out


def lint_song(song, base_of):
    """[{where, extends, path, lost}] for one parsed song; base_of(name) -> base patch dict or None."""
    local = song.get("patches") if isinstance(song.get("patches"), dict) else {}
    found = []
    for where, ov in overrides(song):
        name = ov["extends"]
        base = local.get(name) if isinstance(local.get(name), dict) else base_of(name)
        if not isinstance(base, dict):
            continue
        for path, lost in dropped(ov, base):
            found.append({"where": where, "extends": name, "path": path, "lost": lost})
    return found


def main(argv=None):
    import modlint as ML
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("songs", nargs="*")
    ap.add_argument("--album")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    pin = os.path.realpath(open(os.path.join(HERE, "groove-pin")).read().strip()) \
        if os.path.exists(os.path.join(HERE, "groove-pin")) else "chirp"
    songs = [s if os.path.exists(s) else os.path.join(ROOT, "songs", f"{s}.yaml") for s in a.songs] \
        or ML.focus_songs(a.album)
    res = {}
    for s in songs:
        try:
            song = load_song(s)
        except Exception as e:              # songfmt.Unsupported or a parse error: say so, keep going
            print(f"extendslint: cannot read {s} ({e})", file=sys.stderr)
            continue
        res[os.path.basename(s)] = lint_song(song, lambda n: library_base(n, pin))
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        for s, found in res.items():
            for f in found:
                lost = ", ".join(f"{r.get('src', '?')} ({r.get('amount', '')})" if isinstance(r, dict) else str(r) for r in f["lost"])
                print(f"{s}: {f['where']} extends {f['extends']}: its {f['path']} replaces the base's and drops {lost}")
        n = sum(len(v) for v in res.values())
        print(f"extendslint: {n} dropped route set(s) in {len(songs)} song(s)")
    return 1 if any(res.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
