#!/usr/bin/env python3
"""chirpers: composition mode's album manager (compose/README.md). An album of ORIGINAL songs by "Chirpers": its
tracks start empty, climbers claim them like any climb (climb.py next / --take), compose each from scratch, then keep
climbing them on tools/compscore.py (no record to match) and Harry's ratings (tools/rate.py).

  chirpers.py new ALBUM_ID --spec SPEC.json          create compose/ALBUM_ID/ and its empty track climbs
  chirpers.py name ALBUM_ID "Album Name" [--force]   the first agent to get there names the album (once)
  chirpers.py title ID "Song Title" [--force]        the song's composer names it
  chirpers.py art ALBUM_ID [--prompt TEXT]           cover art with the tti CLI, pixelated for the player
  chirpers.py status [ALBUM_ID]                      tracks, composers, lengths, best scores, latest ratings
  chirpers.py refresh ALBUM_ID [--ids a,b]           render each composed song (seed 0, groove pin) and save its
                                                     features for the album terms (cohesion, distinct, flow)
  chirpers.py rebaseline ALBUM_ID [--ids a,b] [--seeds 0,11] [--apply]
                                                     after a compscore change: render each composed song's current
                                                     file on the seeds, re-score, and (with --apply) record the new
                                                     seed-0 score as its best (the old one kept under best.rescored,
                                                     a note in its history) and save its features, so `done` compares
                                                     like with like (Moult v3 was refused against an old-scale v2)
  chirpers.py release ALBUM_ID [--lufs L] [--out DIR] [--legacy-limiter] [--mix [--overlap-bars N]]
                                                     finish an album: render each composed track (seed 0, groove pin,
                                                     true-peak limiter; --mix: a continuous DJ mixtape too), match
                                                     loudness to the median (or L) without
                                                     passing -1 dBTP, export tagged MP3s with the cover to
                                                     ~/Music/Chirpers/ALBUM/ and a release.json levels report

SPEC.json: {"artist", "album" (a placeholder until named), "year", "genre", "brief", "palette", "bleed",
"genre_refs": [climb ids whose records give the genre's spectrum envelope], "master": {...}, "weights": {...},
"tracks": [{"n", "role": intro|song|outro, "length": [lo_s, hi_s], "brief"}, ...]}. Track climbs are ALBUM_ID-tN
(e.g. chirpers1-t3), songs/ALBUM_ID-tN.yaml, mode "compose", metric "python3 tools/compscore.py ID OUT.wav".
"""
import argparse
import glob
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)


def _climb():
    spec = importlib.util.spec_from_file_location("climb", os.path.join(HERE, "climb.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _climb()


def album_path(album_id):
    return os.path.join(ROOT, "compose", album_id, "album.json")


def load_album(album_id):
    p = album_path(album_id)
    if not os.path.exists(p):
        raise SystemExit(f"chirpers: no album {album_id} ({p})")
    with open(p) as f:
        return json.load(f)


def save_album(album):
    p = album_path(album["id"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(json.dumps(album, indent=2, ensure_ascii=False) + "\n")


def track_id(album_id, n):
    return f"{album_id}-t{n}"


def new_track_climb(album, t, by):
    cid = t["id"]
    title = t.get("title") or f"Track {t['n']} (untitled)"
    return {
        "id": cid, "song": f"songs/{cid}.yaml", "reference": f"{album['artist']} — {title}", "source": None,
        "owner": None, "metric": f"python3 tools/compscore.py {cid} OUT.wav", "best": None, "passes": 1,
        "enabled": False, "status": "requested", "rounds": 0, "priority": 1.0, "genre": album.get("genre"),
        "mode": "compose", "album": album["id"],
        "meta": {"artist": album["artist"], "album": album["album"], "title": title, "track": t["n"],
                 "year": album.get("year")},
        "requested": {"by": by, "at": C.now_iso(), "note": f"COMPOSE ({t['role']}, {t['length'][0]}-{t['length'][1]} s): "
                      f"{t.get('brief', '')}"},
    }


def cmd_new(a, args):
    with open(a.spec) as f:
        spec = json.load(f)
    album = {"id": a.album_id, "artist": spec.get("artist", "Chirpers"), "album": spec["album"], "named": False,
             **{k: v for k, v in spec.items() if k not in ("artist", "album", "tracks")}}
    album["tracks"] = [{**t, "id": track_id(a.album_id, t["n"])} for t in spec["tracks"]]
    if os.path.exists(album_path(a.album_id)):
        raise SystemExit(f"chirpers: album {a.album_id} exists")
    by = C.whoami(args)
    with C.registry() as reg:
        have = {c["id"] for c in reg["climbs"]}
        clash = [t["id"] for t in album["tracks"] if t["id"] in have]
        if clash:
            raise SystemExit(f"chirpers: climbs exist: {', '.join(clash)}")
        for t in album["tracks"]:
            reg["climbs"].append(new_track_climb(album, t, by))
    save_album(album)
    motifs = os.path.join(ROOT, "compose", a.album_id, "motifs.md")
    if not os.path.exists(motifs):
        with open(motifs, "w") as f:
            f.write(f"# {album['album']}: the album's motif bank\n\nShared themes, riffs, rhythmic cells and harmonic "
                    "ideas that tie the album together. Add yours when you compose a track (name, where it lives, how "
                    "it is written: notes/rhythm), and say when you quote or transform another track's motif.\n")
    C.commit_or_die(["climbs.json", os.path.relpath(album_path(a.album_id), ROOT), os.path.relpath(motifs, ROOT)],
                    f"compose: new album {a.album_id} ({len(album['tracks'])} empty tracks, {album['genre']})", args)
    print(f"{a.album_id}: {len(album['tracks'])} tracks requested ({', '.join(t['id'] for t in album['tracks'])})")


def rename_album(reg, old, new):
    for c in reg["climbs"]:
        m = c.get("meta") or {}
        if m.get("album") == old:
            m["album"] = new
    if reg.get("focus") == old:
        reg["focus"] = new


def cmd_name(a, args):
    album = load_album(a.album_id)
    if album.get("named") and not a.force:
        raise SystemExit(f"chirpers: {a.album_id} is already named '{album['album']}' by {album.get('named_by')}")
    old = album["album"]
    who = C.whoami(args)
    with C.registry() as reg:
        rename_album(reg, old, a.name)
    album.update(album=a.name, named=True, named_by=who, named_at=C.now_iso())
    save_album(album)
    paths = ["climbs.json", os.path.relpath(album_path(a.album_id), ROOT)]
    pa = os.path.join(ROOT, "tools", "playlist-album")
    if os.path.exists(pa) and open(pa).read().strip() == old:
        with open(pa, "w") as f:
            f.write(a.name + "\n")
    C.commit_or_die(paths, f"compose: {a.album_id} is named '{a.name}' (by {who})", args)
    print(f"{a.album_id}: '{old}' -> '{a.name}'. Make its cover: chirpers.py art {a.album_id}")


def cmd_title(a, args):
    with C.registry() as reg:
        c = C.find(reg, a.id)
        if c.get("mode") != "compose":
            raise SystemExit(f"chirpers: {a.id} is not a composition")
        m = c.setdefault("meta", {})
        if m.get("title") and "(untitled)" not in m["title"] and not a.force:
            raise SystemExit(f"chirpers: {a.id} is already titled '{m['title']}' (--force to rename)")
        m["title"] = a.title
        c["reference"] = f"{m.get('artist', 'Chirpers')} — {a.title}"
        album = load_album(c["album"])
    for t in album["tracks"]:
        if t["id"] == a.id:
            t["title"] = a.title
    save_album(album)
    C.commit_or_die(["climbs.json", os.path.relpath(album_path(album["id"]), ROOT)],
                    f"compose: {a.id} is titled '{a.title}'", args)
    print(f"{a.id}: '{a.title}'")


def art_prompt(album, extra=None):
    return (f"Album cover art for '{album['album']}' by {album['artist']}, an original {album.get('genre', '')} album. "
            f"{album.get('art_brief') or album.get('brief', '')} {extra or ''} Striking, abstract, no text, no letters, "
            f"no band logo, square composition.").strip()


def cmd_art(a, args):
    album = load_album(a.album_id)
    keep = os.path.join(ROOT, "ref", "albums", C.slug(album["album"]))
    os.makedirs(keep, exist_ok=True)
    out = os.path.join(keep, "cover-tti.png")
    prompt = art_prompt(album, a.prompt)
    r = subprocess.run(["tti", prompt, "-o", out, "-s", "1024x1024"], capture_output=True, text=True)
    if r.returncode or not os.path.exists(out):
        raise SystemExit(f"chirpers: tti failed: {(r.stderr or r.stdout).strip()[-300:]}")
    album["art"] = {"file": os.path.relpath(out, ROOT), "prompt": prompt, "at": C.now_iso()}
    save_album(album)
    rc = subprocess.run([sys.executable, os.path.join(HERE, "climb.py"), "art", album["album"], "--file", out,
                         "--artist", album["artist"], *(["--no-git"] if "--no-git" in args else [])], cwd=ROOT)
    C.commit_or_die([os.path.relpath(album_path(album["id"]), ROOT)], f"compose: {album['id']} cover (tti)", args)
    print(f"{album['id']}: cover {os.path.relpath(out, ROOT)}" + ("" if rc.returncode == 0 else " (pixel art failed)"))


def latest_ratings(album_id):
    """{id: {who: entry}}: each rater's latest SCORED entry, carrying their latest note (a note-only entry after a
    score, as the player's :note writes, must not hide the score: Harry's notes on Phantom Downbeat, 30 Oct)."""
    p = os.path.join(ROOT, "compose", album_id, "ratings.jsonl")
    out = {}
    if os.path.exists(p):
        with open(p) as f:
            for ln in f:
                if ln.strip():
                    r = json.loads(ln)
                    mine = out.setdefault(r["id"], {})
                    prev = mine.get(r.get("who")) or {}
                    if "score" in r:
                        mine[r.get("who")] = dict(r) if r.get("note") or not prev.get("note") else {**r, "note": prev["note"]}
                    elif r.get("note"):
                        mine[r.get("who")] = {**prev, "id": r["id"], "who": r.get("who"), "note": r["note"]}
    return out


def cmd_status(a, args):
    reg = C.load()
    albums = [a.album_id] if a.album_id else sorted(os.path.basename(os.path.dirname(p))
                                                    for p in glob.glob(os.path.join(ROOT, "compose", "*", "album.json")))
    for aid in albums:
        album = load_album(aid)
        rt = latest_ratings(aid)
        print(f"{album['album']} — {album['artist']} ({album.get('genre', '')}){'' if album.get('named') else '  [unnamed]'}")
        for t in album["tracks"]:
            c = next((c for c in reg["climbs"] if c["id"] == t["id"]), {})
            best = c.get("best") or {}
            song = os.path.exists(os.path.join(ROOT, c.get("song", "") or "-"))
            h = (rt.get(t["id"]) or {}).get("harry")
            print(f"  {t['n']:2d} {t['id']:14s} {(c.get('meta') or {}).get('title', '?')[:28]:28s} {t['role']:6s} "
                  f"{t['length'][0]}-{t['length'][1]}s  {c.get('status', '?'):9s} owner {c.get('owner') or '-':14s} "
                  f"{'composed' if song else 'empty   '} best {best.get('score', '—')} {best.get('version', '')}"
                  + (f"  harry {h['score']}/10" if h and "score" in h else "")
                  + (f" ({h['note'][:40]})" if h and h.get("note") else ""))


def cmd_refresh(a, args):
    album = load_album(a.album_id)
    reg = C.load()
    pin = open(os.path.join(ROOT, "tools", "groove-pin")).read().strip()
    ids = a.ids.split(",") if a.ids else [t["id"] for t in album["tracks"]]
    env = dict(os.environ, RAYON_NUM_THREADS="2")
    env.pop("LD_LIBRARY_PATH", None)
    for cid in ids:
        c = next((c for c in reg["climbs"] if c["id"] == cid), None)
        if not c or not os.path.exists(os.path.join(ROOT, c["song"])):
            continue
        with tempfile.TemporaryDirectory(dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None) as d:
            snap = os.path.join(ROOT, "songs", f".chirpers-{os.getpid()}-{cid}.yaml")
            shutil.copy(os.path.join(ROOT, c["song"]), snap)
            try:
                wav = os.path.join(d, "r.wav")
                r = subprocess.run(["nice", "-n", "15", pin, "render", "-f", os.path.basename(snap), "--seed", "0", "-o", wav],
                                   cwd=os.path.join(ROOT, "songs"), env=env, capture_output=True, text=True)
            finally:
                os.unlink(snap)
            if r.returncode:
                print(f"{cid}: render failed: {r.stderr.strip()[-200:]}")
                continue
            r = subprocess.run([sys.executable, os.path.join(HERE, "compscore.py"), cid, wav, "--save"],
                               capture_output=True, text=True, env=env)
            tot = json.loads(r.stdout).get("total") if r.returncode == 0 else None
            print(f"{cid}: features saved, compscore {tot}")


def render(pin, song, seed, out, env):
    """Render SONG (copied into songs/ so its relative includes resolve) at SEED to OUT; the error text or None."""
    snap = os.path.join(ROOT, "songs", f".chirpers-{os.getpid()}-{os.path.basename(song)}")
    shutil.copy(song, snap)
    try:
        r = subprocess.run(["nice", "-n", "15", pin, "render", "-f", os.path.basename(snap), "--seed", str(seed), "-o", out],
                           cwd=os.path.join(ROOT, "songs"), env=env, capture_output=True, text=True)
    finally:
        os.unlink(snap)
    return r.stderr.strip()[-200:] if r.returncode else None


def snapshot(c):
    """What a rebaseline must find unchanged before it writes: the climb's rounds and best version."""
    return (c.get("rounds"), (c.get("best") or {}).get("version"))


def apply_rescore(c, scores, rev, who, at):
    """Record SCORES ({seed: total}) as C's best (seed 0, else the first seed); the history note to append."""
    best = c.setdefault("best", {})
    best.pop("stale", None)                              # re-measured under today's ratings
    old = best.get("score")
    first = scores.get(0, next(iter(scores.values())))
    best["score"] = round(float(first), 3)
    best["rescored"] = {"compscore": rev, "seeds": {str(k): round(float(v), 3) for k, v in scores.items()}, "at": at,
                        "was": old}
    seeds = "/".join(str(k) for k in scores)
    vals = "/".join(f"{v:.3f}" for v in scores.values())
    return {"round": c.get("rounds", 0), "at": at, "who": who, "steer": True,
            "note": f"rebaselined on compscore {rev}: {best.get('version')} (the song file) scores {vals} on seeds {seeds}; "
                    f"best was {old} on an older compscore. Compare candidates against this."}


def cmd_rebaseline(a, args):
    sys.path.insert(0, HERE)
    import compscore as CS
    album = CS.load_album(a.album_id)
    reg = C.load()
    pin = open(os.path.join(ROOT, "tools", "groove-pin")).read().strip()
    seeds = [int(x) for x in a.seeds.split(",")]
    ids = a.ids.split(",") if a.ids else [t["id"] for t in album["tracks"]]
    env = dict(os.environ, RAYON_NUM_THREADS="4")
    env.pop("LD_LIBRARY_PATH", None)
    rev = subprocess.run(["git", "log", "-1", "--format=%h", "--", "tools/compscore.py"], cwd=ROOT, capture_output=True,
                         text=True).stdout.strip() or "?"
    work = tempfile.mkdtemp(prefix="rebaseline-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    todo = []
    try:
        for cid in ids:                                   # pass 1: render, and save features so pass 2's album terms
            c = next((c for c in reg["climbs"] if c["id"] == cid), None)        # see every song's current version
            if not c or not os.path.exists(os.path.join(ROOT, c["song"])) or not (c.get("best") or {}).get("version"):
                continue
            song = os.path.join(work, f"{cid}.yaml")
            shutil.copy(os.path.join(ROOT, c["song"]), song)
            wavs = {}
            for sd in seeds:
                wavs[sd] = os.path.join(work, f"{cid}-s{sd}.wav")
                err = render(pin, song, sd, wavs[sd], env)
                if err:
                    print(f"{cid}: seed {sd} render failed: {err}")
                    break
            else:
                todo.append((c, song, wavs, snapshot(c)))
                if a.apply:
                    me = CS.build_ctx(cid, wavs[seeds[0]], c, album, song)["me"]
                    d = os.path.join(CS.cache_dir(a.album_id), "features")
                    os.makedirs(d, exist_ok=True)
                    with open(os.path.join(d, f"{cid}.json"), "w") as f:
                        json.dump(me, f)
        results = []
        for c, song, wavs, _seen in todo:                # pass 2: score
            scores = {sd: CS.score(CS.build_ctx(c["id"], w, c, album, song), CS.plugins())["total"] for sd, w in wavs.items()}
            last = subprocess.run(["git", "log", "-1", "--format=%s", "--", c["song"]], cwd=ROOT, capture_output=True,
                                  text=True).stdout.strip()
            results.append((c["id"], scores, _seen))
            hist = [h for h in C.history(c["id"]) if h.get("version") and not h.get("steer")]
            if hist and hist[-1]["version"] != c["best"].get("version"):
                print(f"{c['id']}: WARNING the latest round recorded {hist[-1]['version']} (round {hist[-1].get('round')}, "
                      f"not kept) while best is {c['best'].get('version')}: if the song file is {hist[-1]['version']} "
                      f"(a judgment keep), re-point best (climb.py set … best=…, judged) — the scores below are its file's")
            print(f"{c['id']:14s} best {c['best'].get('version'):4s} {c['best'].get('score')!s:>8} -> "
                  + " ".join(f"s{k} {v:.3f}" for k, v in scores.items()) + f"   (song file: {last[:60]})")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if not a.apply or not results:
        return
    who, at = C.whoami(args), C.now_iso()
    paths = ["climbs.json"]
    skipped = []
    with C.registry() as reg:
        for cid, scores, seen in results:
            c = C.find(reg, cid)
            if snapshot(c) != seen:
                # a round landed while we rendered (chirper-zero's Thirteen Teeth v9, 28 Oct): our scores are the old
                # file's, so leave the newly recorded best alone
                skipped.append(cid)
                continue
            h = apply_rescore(c, scores, rev, who, at)
            with open(os.path.join(ROOT, "climbs", f"{cid}.jsonl"), "a") as f:
                f.write(json.dumps(h, ensure_ascii=False) + "\n")
            paths.append(f"climbs/{cid}.jsonl")
    for cid in skipped:
        print(f"{cid}: a round landed during the rebaseline; its new best is left as recorded (re-run to rescore it)")
    done = [(cid, s) for cid, s, _ in results if cid not in skipped]
    if not done:
        return
    C.commit_or_die(paths, f"compose: {a.album_id} rebaselined on compscore {rev} ({len(done)} songs, seeds "
                    f"{a.seeds}): " + ", ".join(f"{cid.split('-')[-1]} {s[seeds[0]]:.2f}" for cid, s in done), args)


def mix_stream(parts, emit):
    """Assemble a DJ mix: PARTS yields (x, overlap) per track in order, x float stereo samples cut at the track's
    musical end (the last keeps its tail), overlap = samples it shares with the PREVIOUS track. Each overlap is a linear
    crossfade (out*(1-t) + in*t), which never exceeds the louder input's sample peak, so the mix cannot clip.
    EMIT receives finished blocks in order; at most one track is held in memory."""
    held = None
    for x, ov in parts:
        if held is None:
            held = x
            continue
        ov = int(max(0, min(ov, len(held), len(x))))
        if ov:
            emit(held[:-ov])
            t = np.linspace(0.0, 1.0, ov, endpoint=False, dtype=np.float32)[:, None]
            held = np.concatenate([held[-ov:] * (1 - t) + x[:ov] * t, x[ov:]])
        else:
            emit(held)
            held = x
    if held is not None:
        emit(held)


def seam_overlaps(album_id, default_bars=16, root=None):
    """{(out_n, in_n): bars} from compose/ALBUM/mixplan.md's seam table ('| tN -> tM | ... | overlap (bars) | ...');
    unknown seams use DEFAULT_BARS."""
    import re
    p = os.path.join(root or ROOT, "compose", album_id, "mixplan.md")
    out = {}
    if os.path.exists(p):
        head = None
        for ln in open(p):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) > 2 and cells[0].lower() == "seam":
                head = [c.lower() for c in cells]
                continue
            m = re.match(r"t(\d+)\s*->\s*t(\d+)", cells[0]) if cells else None
            if m and head:
                col = next((i for i, h in enumerate(head) if h.startswith("overlap")), None)
                v = re.search(r"\d+(\.\d+)?", cells[col]) if col is not None and col < len(cells) else None
                if v:
                    out[(int(m.group(1)), int(m.group(2)))] = float(v.group(0))
    return out, default_bars


def release_plan(rows, target=None, tp_ceiling=-1.0):
    """Per-track gain (dB) to bring each track to the album's TARGET integrated loudness (default: the median), never
    past TP_CEILING dBTP. rows: [{lufs, true_peak_dbtp}]. Returns [{gain_db, lufs_out, tp_out, capped}]."""
    t = float(sorted(r["lufs"] for r in rows)[len(rows) // 2]) if target is None else float(target)
    out = []
    for r in rows:
        want = t - r["lufs"]
        room = tp_ceiling - r["true_peak_dbtp"]
        g = min(want, room)
        g, want = float(g), float(want)          # levels' numbers are numpy: release.json needs plain floats and bools
        out.append({"gain_db": round(g, 2), "lufs_out": round(float(r["lufs"]) + g, 1),
                    "tp_out": round(float(r["true_peak_dbtp"]) + g, 2), "capped": bool(g < want - 0.05)})
    return t, out


def cmd_release(a, args):
    """Render, loudness-match and export an album as tagged MP3s with its cover (Harry's process review, 30 Oct: albums
    are started but never finished)."""
    import concurrent.futures as cf
    sys.path.insert(0, HERE)
    import levels as LV
    album = load_album(a.album_id)
    reg = C.load()
    pin = open(os.path.join(ROOT, "tools", "groove-pin")).read().strip()
    tracks = []
    for t in album["tracks"]:
        c = next((c for c in reg["climbs"] if c["id"] == t["id"]), {})
        if c.get("song") and os.path.exists(os.path.join(ROOT, c["song"])):
            tracks.append((t["n"], t["id"], (c.get("meta") or {}).get("title") or t["id"], os.path.join(ROOT, c["song"])))
    if not tracks:
        sys.exit(f"release: {a.album_id} has no composed tracks")
    name = album["album"]
    out_dir = os.path.expanduser(os.path.join(a.out, "".join(ch for ch in name if ch not in '/\\:*?"<>|')))
    os.makedirs(out_dir, exist_ok=True)
    work = tempfile.mkdtemp(prefix="release-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    env = dict(os.environ, RAYON_NUM_THREADS="3")
    env.pop("LD_LIBRARY_PATH", None)

    def render(tr):
        n, cid, title, song = tr
        snap, wav = os.path.join(work, f"{cid}.yaml"), os.path.join(work, f"{cid}.wav")
        shutil.copy(song, snap)
        cmd = [pin, "render", "-f", snap, "--seed", str(a.seed), "-o", wav] + (["--set", "true_peak=false"] if a.legacy_limiter else [])
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return tr, wav if r.returncode == 0 else None, r.stderr[-300:]

    rows = []
    try:
        with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
            for (n, cid, title, song), wav, err in ex.map(render, tracks):
                if not wav:
                    print(f"{cid}: render failed: {err}", file=sys.stderr)
                    continue
                m = LV.measure(wav)
                rows.append({"n": n, "id": cid, "title": title, "wav": wav, "lufs": float(m["lufs"]),
                             "true_peak_dbtp": float(m["true_peak_dbtp"]), "longest_pinned_run": int(m["longest_pinned_run"]),
                             "dur": float(m["dur"])})
        rows.sort(key=lambda r: r["n"])
        target, plan = release_plan(rows, a.lufs)
        art = (album.get("art") or {}).get("file")
        art = os.path.join(ROOT, art) if art and os.path.exists(os.path.join(ROOT, art)) else None
        report = {"album": name, "artist": album["artist"], "target_lufs": round(target, 1), "pin": os.path.basename(pin),
                  "seed": a.seed, "true_peak_limiter": not a.legacy_limiter, "tracks": []}
        for r, p in zip(rows, plan):
            safe = "".join(ch for ch in r["title"] if ch not in '/\\:*?"<>|')
            mp3 = os.path.join(out_dir, f"{r['n']:02d} - {safe}.mp3")
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", r["wav"]] + (["-i", art] if art else []) + [
                "-map", "0:a"] + (["-map", "1:v", "-c:v", "png", "-disposition:v", "attached_pic"] if art else []) + [
                "-af", f"volume={p['gain_db']}dB", "-c:a", "libmp3lame", "-q:a", "0", "-id3v2_version", "3",
                "-metadata", f"title={r['title']}", "-metadata", f"artist={album['artist']}", "-metadata", f"album={name}",
                "-metadata", f"track={r['n']}/{len(album['tracks'])}", "-metadata", f"date={album.get('year', '')}", mp3]
            ok = subprocess.run(cmd, capture_output=True, text=True).returncode == 0
            report["tracks"].append({**{k: r[k] for k in ("n", "id", "title", "dur", "lufs", "true_peak_dbtp",
                                                           "longest_pinned_run")}, **p, "file": os.path.basename(mp3) if ok else None})
            print(f"{r['n']:2d} {r['title'][:28]:28s} {r['lufs']:6.1f} LUFS  TP {r['true_peak_dbtp']:6.2f}  gain {p['gain_db']:+5.1f}"
                  f" -> {p['lufs_out']:6.1f} LUFS TP {p['tp_out']:6.2f}{'  (capped by true peak)' if p['capped'] else ''}"
                  f"{'  FLAT ' + str(r['longest_pinned_run']) if r['longest_pinned_run'] >= 4 else ''}{'' if ok else '  ENCODE FAILED'}")
        if a.mix and len(rows) > 1:
            report["mix"] = mix_release(a, album, rows, plan, pin, work, out_dir, art, env)
        with open(os.path.join(out_dir, "release.json"), "w") as f:
            json.dump(report, f, indent=1)
        print(f"{name}: {len(rows)} tracks at {target:.1f} LUFS -> {out_dir}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def mix_release(a, album, rows, plan, pin, work, out_dir, art, env):
    """The continuous mixtape: each track starts OVERLAP bars (mixplan.md, else --overlap-bars) before the previous
    one's musical end (chirp plan's `seconds`, at the outgoing song's declared tempo), crossfaded linearly; one MP3 and
    a tracklist/CUE. Returns the tracklist."""
    sys.path.insert(0, HERE)
    import likeness as L
    import compscore as CS
    seams, default = seam_overlaps(a.album_id, a.overlap_bars)
    info = []
    for r in rows:
        snap = os.path.join(work, f"{r['id']}.yaml")
        pl = subprocess.run([pin, "plan", "-f", snap, "--json"], capture_output=True, text=True, env=env)
        try:
            d = json.loads(pl.stdout)
            secs = float((d.get("data") or d)["seconds"])
        except (ValueError, KeyError, TypeError):
            secs = None
        info.append({"secs": secs, "bpm": CS.declared_tempo(snap) or 120.0})
    starts, t = [], 0.0
    for i, r in enumerate(rows):
        if i:
            prev = rows[i - 1]
            bars = seams.get((prev["n"], r["n"]), default)
            ov = bars * 4 * 60.0 / info[i - 1]["bpm"]
            t = starts[-1] + (info[i - 1]["secs"] or prev["dur"]) - ov
            info[i]["ov"] = ov
        starts.append(t)
    mp3 = os.path.join(out_dir, "".join(ch for ch in album["album"] if ch not in '/\\:*?"<>|') + " (continuous mix).mp3")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(L.SR), "-ac", "2", "-i", "-"] + (
        ["-i", art, "-map", "0:a", "-map", "1:v", "-c:v", "png", "-disposition:v", "attached_pic"] if art else []) + [
        "-c:a", "libmp3lame", "-q:a", "0", "-id3v2_version", "3", "-metadata", f"title={album['album']} (continuous mix)",
        "-metadata", f"artist={album['artist']}", "-metadata", f"album={album['album']}", mp3]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    def parts():
        for i, (r, p) in enumerate(zip(rows, plan)):
            x = L.load(r["wav"]) * np.float32(10 ** (p["gain_db"] / 20))
            if i < len(rows) - 1 and info[i]["secs"]:
                x = x[:int(info[i]["secs"] * L.SR)]
            yield x, int(info[i].get("ov", 0) * L.SR)

    def emit(block):
        ff.stdin.write((np.clip(block, -1.0, 1.0) * 32767).astype("<i2").tobytes())

    mix_stream(parts(), emit)
    ff.stdin.close()
    ok = ff.wait() == 0
    tl = [{"n": r["n"], "title": r["title"], "start": round(st, 2), "overlap_in_s": round(info[i].get("ov", 0.0), 2)}
          for i, (r, st) in enumerate(zip(rows, starts))]
    with open(os.path.join(out_dir, "mixtape-tracklist.txt"), "w") as f:
        f.write("".join(f"{int(x['start'] // 60):02d}:{x['start'] % 60:05.2f}  {x['n']:2d}. {x['title']}\n" for x in tl))
    with open(os.path.join(out_dir, "mixtape.cue"), "w") as f:
        f.write(f'PERFORMER "{album["artist"]}"\nTITLE "{album["album"]}"\nFILE "{os.path.basename(mp3)}" MP3\n')
        for i, x in enumerate(tl, 1):
            mm, ss = divmod(x["start"], 60)
            f.write(f'  TRACK {i:02d} AUDIO\n    TITLE "{x["title"]}"\n    INDEX 01 {int(mm):02d}:{int(ss):02d}:{int((ss % 1) * 75):02d}\n')
    print(f"mixtape: {len(tl)} tracks, {starts[-1] / 60:.1f} min to the last start -> {mp3}{'' if ok else '  ENCODE FAILED'}")
    return {"file": os.path.basename(mp3) if ok else None, "tracklist": tl}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new")
    p.add_argument("album_id")
    p.add_argument("--spec", required=True)
    p = sub.add_parser("name")
    p.add_argument("album_id")
    p.add_argument("name")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("title")
    p.add_argument("id")
    p.add_argument("title")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("art")
    p.add_argument("album_id")
    p.add_argument("--prompt")
    p = sub.add_parser("status")
    p.add_argument("album_id", nargs="?")
    p = sub.add_parser("refresh")
    p.add_argument("album_id")
    p.add_argument("--ids")
    p = sub.add_parser("rebaseline")
    p.add_argument("album_id")
    p.add_argument("--ids")
    p.add_argument("--seeds", default="0,11")
    p.add_argument("--apply", action="store_true")
    p = sub.add_parser("release")
    p.add_argument("album_id")
    p.add_argument("--lufs", type=float, help="target integrated loudness (default: the album's median)")
    p.add_argument("--out", default="~/Music/Chirpers")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--jobs", type=int, default=3)
    p.add_argument("--legacy-limiter", action="store_true", help="legacy clamp limiter (true_peak is the default)")
    p.add_argument("--mix", action="store_true", help="also a continuous DJ mixtape: seams overlapped per mixplan.md")
    p.add_argument("--overlap-bars", type=float, default=16.0, help="seam overlap when mixplan.md doesn't give one")
    known, skip = [], False
    for i, x in enumerate(argv):            # climb.py's own flags (--as NAME, --no-git) go to its helpers, not argparse
        if skip:
            skip = False
            continue
        if x == "--as":
            skip = True
            continue
        if x != "--no-git":
            known.append(x)
    a = ap.parse_args(known)
    {"new": cmd_new, "name": cmd_name, "title": cmd_title, "art": cmd_art, "status": cmd_status,
     "refresh": cmd_refresh, "rebaseline": cmd_rebaseline, "release": cmd_release}[a.cmd](a, argv)


if __name__ == "__main__":
    main()
