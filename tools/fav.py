#!/usr/bin/env python3
"""Save what was playing as a favourite: `fav.py 23:40 [ROLE]` finds the chapter that was playing
at that time (from ~/.cache/chirp/played, archived by evolve.py), copies its parts for ROLE (default:
all riff parts in the chapter's sections — e.g. riffBrk for a breakdown) to songs/fav-*.yaml and
registers them in favorites.json (forms recall them, transposed into each song's key); the
song identity is saved too so the whole song can return. `fav.py now` = the chapter playing now."""
import glob, json, os, re, shutil, sys, time

ARCHIVE = os.path.expanduser("~/.cache/chirp/played")
TOOLS = os.path.dirname(os.path.abspath(__file__))
SONGS = os.path.join(os.path.dirname(TOOLS), "songs")
NAMES = ["c", "c#", "d", "eb", "e", "f", "f#", "g", "ab", "a", "bb", "b"]

def chapter_at(hhmm):
    dirs = sorted(glob.glob(os.path.join(ARCHIVE, "*")))
    if hhmm == "now":
        return dirs[-1] if dirs else None
    day = time.strftime("%Y%m%d")
    t = day + "-" + hhmm.replace(":", "") + ("00" if hhmm.count(":") == 1 else "")
    best = None
    for d in dirs:
        if os.path.basename(d)[:15] <= t:
            best = d
    return best

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = chapter_at(sys.argv[1])
    if not d:
        sys.exit("nothing archived for that time")
    role = sys.argv[2] if len(sys.argv) > 2 else None
    ident = json.load(open(os.path.join(d, "ident.json")))
    g = ident.get("gen", {})
    key = f"{NAMES[g.get('pc', 0)]}-{g.get('mode', 'x')}".replace("#", "s")
    form = [f for f in glob.glob(os.path.join(d, "form-*.yaml"))][0]
    used = set(re.findall(r"@gen-form-\d-(riff\w*)", open(form).read()))
    roles = [role] if role else sorted(used)
    favs = json.load(open(os.path.join(TOOLS, "favorites.json")))
    stamp = os.path.basename(d)[9:13]
    for ro in roles:
        src = glob.glob(os.path.join(d, f"gen-form-*-{ro}.yaml"))
        if not src:
            print(f"no {ro} in {d}"); continue
        name = f"fav-{ro.lower()}-{key}-{stamp}"
        lines = open(src[0]).read().splitlines()
        lines[0] = f'about: "Favourite {ro} saved from the live set ({os.path.basename(d)}): {ident.get("style")} in {key.replace("-", " ")} at {ident.get("tempo")} BPM; tempo-inheriting part, 16 beats."'
        open(os.path.join(SONGS, name + ".yaml"), "w").write("\n".join(lines) + "\n")
        favs.append({"part": name, "role": ro, "pc": g.get("pc", 0), "mode": g.get("mode"), "bpm": ident.get("tempo"), "note": f"saved from {os.path.basename(d)}"})
        print("saved", name)
    if not any(f.get("song", {}).get("gen") == g for f in favs if "song" in f):
        favs.append({"song": dict(ident, chapter=0), "note": f"saved from {os.path.basename(d)}"})
    open(os.path.join(TOOLS, "favorites.json"), "w").write(json.dumps(favs, indent=1) + "\n")

if __name__ == "__main__":
    main()
