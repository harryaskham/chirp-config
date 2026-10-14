#!/usr/bin/env python3
"""libparts.py — export one stable, reusable library part (and its melody, where it has one) per chill
style: songs/lib-STYLE.yaml and songs/lib-STYLE-hook.yaml, composed in C with a fixed seed, tempo
inheriting and transposable with tr= (`chirp plan -t 90 "@lib-bossa"`, or `tr=3 @lib-kankyo` in a score).
Writes songs/LIB.md as an index. Re-run after changing a style's generator."""
import glob, os, random, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as c

SONGS = os.path.expanduser("~/.config/chirp/songs")
MAIN = ["riff", "riffB", "riffA", "riffP", "riffG", "riffJ", "riffW", "riffF", "riffI"]


def export(style):
    rng = random.Random(zlib.crc32(style.encode()))
    p = c.params(style, rng)
    p["pc"] = 0
    names, desc = c.compose(style, "libtmp", p)
    out = []
    for role, lib in [(next((r for r in MAIN if r in names), None), f"lib-{style}"), ("hook" if "hook" in names else ("hookE" if "hookE" in names else None), f"lib-{style}-hook")]:
        if not role:
            continue
        src = open(f"{SONGS}/{names[role]}.yaml").read().splitlines()
        beats = c.LENGTHS.get(names[role], 16)
        about = f"Library part — {style} {'melody' if 'hook' in lib else 'section'} ({desc.split(',')[0].replace(c.NAMES[0], 'C')}), {beats:g} beats, tempo-inheriting; transpose with tr=."
        src[0] = "about: " + __import__("json").dumps(about)
        open(f"{SONGS}/{lib}.yaml", "w").write("\n".join(src) + "\n")
        out.append((lib, beats))
    for f in glob.glob(f"{SONGS}/gen-libtmp-*.yaml"):
        os.remove(f)
    return out


if __name__ == "__main__":
    styles = sys.argv[1:] or sorted(c.CHILL_STYLES)
    rows = []
    for st in styles:
        for lib, beats in export(st):
            rows.append(f"| `@{lib}` | {st} | {beats:g} |")
            print(lib, beats)
    open(f"{SONGS}/LIB.md", "w").write("# Library parts\n\nStable, reusable parts exported from the chill generators (`tools/libparts.py`), composed in C, tempo-inheriting.\nUse `@NAME` in a score; transpose with `tr=N` (e.g. `tr=-3 @lib-kankyo`).\n\n| part | style | beats |\n|---|---|---|\n" + "\n".join(rows) + "\n")
