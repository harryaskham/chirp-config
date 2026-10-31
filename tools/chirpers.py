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
  chirpers.py seam ALBUM_ID N [--swap BAR] [--out DIR]  one seam tN -> tN+1 as the live mix plays it: sub and
                                                     full-band level per bar (linear and the mixer swap), mp3s
  chirpers.py seams ALBUM_ID [--flam-ms MS] [--dead-s S]   audit a mixtape's DJ seams: beat drift across each
                                                     overlap (tempo ramps, mismatches), dead air after the last bar
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


SWAP_HZ = 120.0     # the bass swap's crossover (a DJ mixer's low EQ)


def bass_swap(out, inn, at, ln, sr=48000):
    """One overlap with a DJ's BASS SWAP (chirper-three, 31 Oct: a linear fade under a composed swap leaves a hole in
    the low end): both sides split at SWAP_HZ (Butterworth run forwards and backwards: an LR4 magnitude, zero phase,
    and high = x - low, so the bands sum back exactly); the highs crossfade linearly across the whole overlap, the lows
    stay the outgoing track's until sample AT and hand over to the incoming one across LN samples. Peaks are held at
    the louder input's peak by a smooth lookahead gain, so the mix still cannot pass it."""
    from scipy import ndimage, signal
    sos = signal.butter(2, SWAP_HZ, "low", fs=sr, output="sos")
    lo_o, lo_i = signal.sosfiltfilt(sos, out, axis=0), signal.sosfiltfilt(sos, inn, axis=0)
    n = len(out)
    t = np.linspace(0.0, 1.0, n, endpoint=False)[:, None]
    g = np.clip(1.0 - (np.arange(n) - at) / max(ln, 1), 0.0, 1.0)[:, None]      # the outgoing lows' gain
    y = lo_o * g + (out - lo_o) * (1 - t) + lo_i * (1 - g) + (inn - lo_i) * t
    ceil = max(float(np.abs(out).max(initial=0)), float(np.abs(inn).max(initial=0)))
    env = np.abs(y).max(axis=1)
    if ceil > 0 and env.max() > ceil:
        w = max(1, int(0.005 * sr))
        gain = np.minimum(1.0, ceil / np.maximum(env, 1e-12))
        gain = ndimage.uniform_filter1d(ndimage.minimum_filter1d(gain, 2 * w + 1), 2 * w + 1)
        y = y * np.minimum(gain, ceil / np.maximum(env, 1e-12))[:, None]
    return y.astype(np.float32)


def mix_stream(parts, emit, sr=48000):
    """Assemble a DJ mix: PARTS yields (x, overlap) or (x, overlap, swap) per track in order, x float stereo samples
    cut at the track's musical end (the last keeps its tail), overlap = samples it shares with the PREVIOUS track, swap
    = None or (at, length) samples for a bass swap inside that overlap (bass_swap). Without a swap each overlap is a
    linear crossfade (out*(1-t) + in*t), which never exceeds the louder input's sample peak, so the mix cannot clip.
    EMIT receives finished blocks in order; at most one track is held in memory."""
    held = None
    for part in parts:
        x, ov, sw = (tuple(part) + (None,))[:3]
        if held is None:
            held = x
            continue
        ov = int(max(0, min(ov, len(held), len(x))))
        if ov:
            emit(held[:-ov])
            if sw:
                mixed = bass_swap(held[-ov:], x[:ov], int(sw[0]), int(sw[1]), sr)
            else:
                t = np.linspace(0.0, 1.0, ov, endpoint=False, dtype=np.float32)[:, None]
                mixed = held[-ov:] * (1 - t) + x[:ov] * t
            held = np.concatenate([mixed, x[ov:]])
        else:
            emit(held)
            held = x
    if held is not None:
        emit(held)


def seam_table(album_id, root=None):
    """{(out_n, in_n): {column: cell}} from compose/ALBUM/mixplan.md's seam table ('| seam | ... |' then '| tN -> tM |
    ... |' rows); column names lower-cased."""
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
                out[(int(m.group(1)), int(m.group(2)))] = dict(zip(head, cells))
    return out


def _col(row, prefix):
    return next((v for k, v in row.items() if k.startswith(prefix)), "")


def seam_overlaps(album_id, default_bars=16, root=None):
    """{(out_n, in_n): bars} from compose/ALBUM/mixplan.md's seam table ('| tN -> tM | ... | overlap (bars) | ...');
    unknown seams use DEFAULT_BARS."""
    import re
    out = {}
    for k, row in seam_table(album_id, root).items():
        v = re.search(r"\d+(\.\d+)?", _col(row, "overlap"))
        if v:
            out[k] = float(v.group(0))
    return out, default_bars


def seam_swaps(album_id, root=None):
    """{(out_n, in_n): bar | 'mid' | None} from an optional 'swap' column. Only the cell's LEADING token counts (the
    composers write their measurements after it: 'no (measured: linear sub range 3.3 dB ...)'): a number is the bar
    into the overlap where the bass swap lands, mid/yes/on the midpoint, no/off/none/- none; seams without a cell, or
    whose cell starts with anything else, are absent (the default)."""
    import re
    out = {}
    for k, row in seam_table(album_id, root).items():
        m = re.match(r"\s*([0-9]+(?:\.[0-9]+)?|[a-z-]+)", _col(row, "swap").lower())
        if not m:
            continue
        tok = m.group(1)
        if re.fullmatch(r"[0-9.]+", tok):
            out[k] = float(tok)
        elif tok in ("mid", "yes", "on", "true"):
            out[k] = "mid"
        elif tok in ("no", "off", "none", "-", "false"):
            out[k] = None
    return out


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
        tl = song_timeline(pin, snap)
        info.append({"secs": tl["secs"] if tl else None, "tl": tl, "bpm": CS.declared_tempo(snap) or 120.0})
    starts, t = [], 0.0
    for i, r in enumerate(rows):
        if i:
            prev, tl = rows[i - 1], info[i - 1]["tl"]
            bars = seams.get((prev["n"], r["n"]), default)
            if tl:     # the outgoing bar line BARS bars before its last bar, as the live mix places it
                ov = tl["secs"] - seam_start(tl, bars)
                info[i - 1]["bpm"] = tl["bpm"](tl["end_beat"] - 0.01)
            else:
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

    swaps = seam_swaps(a.album_id)

    def swap_of(i):
        """(at, length) samples for the bass swap into track I (the per-seam mixplan cell beats --swap), or None."""
        if not i:
            return None
        k = (rows[i - 1]["n"], rows[i]["n"])
        want = swaps.get(k, a.swap) if k in swaps else a.swap
        if want is None or want is False:
            return None
        bars = seams.get(k, default)
        bpm = info[i - 1]["bpm"]
        at_bars = bars / 2 if want in ("mid", True) else float(want)
        return int(at_bars * 4 * 60.0 / bpm * L.SR), int(60.0 / bpm * L.SR)

    def parts():
        for i, (r, p) in enumerate(zip(rows, plan)):
            x = L.load(r["wav"]) * np.float32(10 ** (p["gain_db"] / 20))
            if i < len(rows) - 1 and info[i]["secs"]:
                x = x[:int(info[i]["secs"] * L.SR)]
            yield x, int(info[i].get("ov", 0) * L.SR), swap_of(i)

    def emit(block):
        ff.stdin.write((np.clip(block, -1.0, 1.0) * 32767).astype("<i2").tobytes())

    mix_stream(parts(), emit, L.SR)
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


def _beats(at):
    """A tempo point's `at` in beats ('640b'; a bare number is beats)."""
    t = str(at).strip()
    return float(t[:-1]) if t.endswith("b") else float(t)


def tempo_fn(points):
    """bpm(beat) from a canonical tempo map: a `ramp` point glides linearly (in beats) from the previous point's BPM;
    otherwise the tempo steps at the point."""
    pts = sorted(((_beats(p["at"]), float(p["bpm"]), bool(p.get("ramp"))) for p in points), key=lambda q: q[0])

    def bpm(b):
        cur = pts[0][1]
        for i, (at, v, ramp) in enumerate(pts):
            if b < at:
                if ramp and i:
                    a0, v0 = pts[i - 1][0], pts[i - 1][1]
                    return v0 + (v - v0) * (b - a0) / max(at - a0, 1e-9)
                return cur
            cur = v
        return cur
    return bpm


def beat_times(bpm, b0, n, step=1 / 32):
    """Seconds from beat B0 to each whole beat B0+k, k = 0..N (integrating 60/bpm in 1/32-beat steps)."""
    out, t, b = [0.0], 0.0, b0
    for _ in range(n):
        for _ in range(int(round(1 / step))):
            t += 60.0 / bpm(b + step / 2) * step
            b += step
        out.append(t)
    return out


def song_timeline(pin, song, beats_per_bar=4):
    """A song's beat clock from chirp plan: {bpm (fn of beat), secs (musical end), times (seconds of each whole beat
    past the end), end_beat (its last bar line at or before the musical end), dead (seconds after that bar line)}; None
    when the song does not plan."""
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        d = d.get("data") or d
        tm = (d.get("canonical") or {}).get("tempo")
        tm = tm if isinstance(tm, list) else [{"at": "0b", "bpm": float(tm or 120)}]
        secs = float(d["seconds"])
    except (ValueError, KeyError, TypeError):
        return None
    bpm = tempo_fn(tm)
    times, b = [0.0], 0
    while times[-1] <= secs:                          # whole beats past the musical end
        times.append(times[-1] + beat_times(bpm, b, 1)[1])
        b += 1
    end = (b - 1) + (secs - times[b - 1]) / (times[b] - times[b - 1])     # the musical end, in (fractional) beats
    last_bar = int((end + 1e-3) // beats_per_bar) * beats_per_bar        # a song ending ON a bar line keeps it
    return {"bpm": bpm, "secs": secs, "times": times, "end_beat": last_bar, "dead": max(0.0, secs - times[last_bar])}


def seam_start(tl, bars, beats_per_bar=4):
    """Seconds into the outgoing song where the incoming one starts: its bar line BARS bars before the last bar line
    at the musical end (the live DJ mix's placement)."""
    return tl["times"][max(0, tl["end_beat"] - int(round(bars * beats_per_bar)))]


def seam_report(album_id, pin, beats_per_bar=4):
    """Per seam: the outgoing track's tempo across its last OVERLAP bars vs the incoming track's across its first, and
    how far their beats drift apart by the end of the crossfade (the live DJ mix starts the incoming track on the
    outgoing bar line OVERLAP bars before the musical end and never tempo-syncs). Per track: dead air after the last
    bar line (the render tail past the music, which the flow term hears)."""
    album = load_album(album_id)
    seams, default = seam_overlaps(album_id)
    songs = {}
    for t in album.get("tracks", []):
        song = os.path.join(ROOT, "songs", f"{t['id']}.yaml")
        tl = song_timeline(pin, song, beats_per_bar) if os.path.exists(song) else None
        if tl:
            songs[t["n"]] = dict(tl, id=t["id"])
    rows = []
    for n in sorted(songs):
        if n + 1 not in songs:
            continue
        a, c = songs[n], songs[n + 1]
        ov = seams.get((n, n + 1), default)
        k = int(round(ov * beats_per_bar))
        start = a["end_beat"] - k
        to, ti = beat_times(a["bpm"], start, k), beat_times(c["bpm"], 0, k)
        drift = [1000 * (x - y) for x, y in zip(to, ti)]
        rows.append({"seam": f"t{n} -> t{n + 1}", "overlap_bars": ov,
                     "out_bpm": (round(a["bpm"](start), 2), round(a["bpm"](a["end_beat"] - 0.01), 2)),
                     "in_bpm": (round(c["bpm"](0), 2), round(c["bpm"](k - 0.01), 2)),
                     "drift_ms": round(drift[-1], 1), "max_drift_ms": round(max(drift, key=abs), 1)})
    return songs, rows


def cmd_seams(a, argv=None):
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    songs, rows = seam_report(a.album_id, pin)
    print(f"{'seam':12} {'bars':>4}  {'out bpm (over the overlap)':>26}  {'in bpm':>16}  {'drift ms':>8}  flags")
    for r in rows:
        o, i = r["out_bpm"], r["in_bpm"]
        flags = []
        if o[0] != o[1]:
            flags.append("RAMP-OUT")
        if i[0] != i[1]:
            flags.append("RAMP-IN")
        if abs(r["max_drift_ms"]) >= a.flam_ms:
            flags.append(f"FLAM (>= {a.flam_ms:g} ms)")
        print(f"{r['seam']:12} {r['overlap_bars']:>4g}  {o[0]:>12g} -> {o[1]:<11g}  {i[0]:>7g} -> {i[1]:<6g}  "
              f"{r['max_drift_ms']:>8.1f}  {' '.join(flags)}")
    dead = [(n, s) for n, s in sorted(songs.items()) if s["dead"] > a.dead_s]
    if dead:
        print("dead air after the last bar line (the flow term hears it; the live mix and release --mix cut it):")
        for n, s in dead:
            print(f"  t{n:<3} {s['dead']:.2f} s")
    if a.json:
        print(json.dumps({"seams": rows, "dead": {f"t{n}": round(s["dead"], 2) for n, s in songs.items()}}))


def cmd_seam(a, argv=None):
    """One seam as the live mix plays it: per-bar levels across the overlap (linear crossfade and the mixer bass swap)
    and mp3s of each with 8 bars either side."""
    sys.path.insert(0, HERE)
    import likeness as L
    from scipy import signal
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    album = load_album(a.album_id)
    by_n = {t["n"]: t for t in album.get("tracks", [])}
    n = a.n
    if n not in by_n or n + 1 not in by_n:
        raise SystemExit(f"seam: {a.album_id} has no t{n} -> t{n + 1}")
    ids = [by_n[n]["id"], by_n[n + 1]["id"]]
    songs = [os.path.join(ROOT, "songs", f"{i}.yaml") for i in ids]
    work = tempfile.mkdtemp(prefix="chirp-seam-")
    try:
        wavs = a.wavs or [os.path.join(work, f"{i}.wav") for i in ids]
        if not a.wavs:
            procs = [subprocess.Popen(["nice", "-n", "12", pin, "render", "-f", sg, "--seed", str(a.seed), "-o", w],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.PIPE) for sg, w in zip(songs, wavs)]
            for pr, sg in zip(procs, songs):
                if pr.wait():
                    raise SystemExit(f"seam: render failed: {sg}: {pr.stderr.read().decode()[-300:]}")
        tl = song_timeline(pin, songs[0])
        if not tl:
            raise SystemExit(f"seam: {songs[0]} does not plan")
        seams, default = seam_overlaps(a.album_id)
        bars = a.bars or seams.get((n, n + 1), default)
        sr = L.SR
        start, end = seam_start(tl, bars), tl["secs"]
        bpm_end = tl["bpm"](tl["end_beat"] - 0.01)
        bar = 4 * 60.0 / bpm_end
        x, y = L.load(wavs[0]), L.load(wavs[1])
        i0, i1 = int(start * sr), int(end * sr)
        ov = i1 - i0
        out, inn = x[i0:i1], y[:ov]
        sw = a.swap if a.swap is not None else seam_swaps(a.album_id).get((n, n + 1), "mid")
        at_bars = bars / 2 if sw in (None, "mid", True) else float(sw)
        t = np.linspace(0.0, 1.0, ov, endpoint=False, dtype=np.float32)[:, None]
        variants = {"linear": out * (1 - t) + inn * t,
                    "swap": bass_swap(out, inn, int(at_bars * bar * sr), int(bar / 4 * sr), sr)}
        sos = signal.butter(4, SWAP_HZ, "low", fs=sr, output="sos")
        nb = int(round(ov / (bar * sr)))
        print(f"{ids[0]} -> {ids[1]}: overlap {bars:g} bars from {start:.2f} s to {end:.2f} s of {ids[0]} "
              f"({bpm_end:g} bpm at the seam); swap at bar {at_bars:g}")

        def per_bar(v, low):
            m = signal.sosfilt(sos, v.mean(axis=1)) if low else v.mean(axis=1)
            return np.array([10 * np.log10(np.mean(m[int(k * bar * sr):int((k + 1) * bar * sr)] ** 2) + 1e-12)
                             for k in range(nb)])
        print(f"{'':18}" + "".join(f"{k + 1:>6}" for k in range(nb)) + "   range   std")
        rows = {}
        for name, v in [("tail alone", out * 1.0), ("head alone", inn * 1.0)] + list(variants.items()):
            for low in (True, False):
                d = per_bar(v, low)
                rows[(name, low)] = d
                lab = f"{name} {'sub' if low else 'all'}"
                print(f"{lab:18}" + "".join(f"{q:6.1f}" for q in d) + f"  {d.max() - d.min():5.1f} {d.std():5.2f}")
        os.makedirs(a.out, exist_ok=True)
        ctx = int(8 * bar * sr)
        for name, v in variants.items():
            clip = np.concatenate([x[max(0, i0 - ctx):i0], v, y[ov:ov + ctx]])
            mp3 = os.path.join(a.out, f"{a.album_id}-t{n}-t{n + 1}-{name}.mp3")
            ff = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-",
                                 "-c:a", "libmp3lame", "-q:a", "2", mp3], input=clip.astype("<f4").tobytes())
            print(f"{name}: {mp3}" + ("" if ff.returncode == 0 else "  (encode failed)"))
        if a.json:
            print(json.dumps({f"{k[0]}|{'sub' if k[1] else 'all'}": [round(float(q), 2) for q in v] for k, v in rows.items()}))
    finally:
        shutil.rmtree(work, ignore_errors=True)


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
    p.add_argument("--swap", nargs="?", const="mid", default=None, type=lambda v: v if v == "mid" else float(v),
                   help="--mix: a DJ bass swap in every overlap, at its midpoint or BAR bars in (mixplan.md's swap column wins)")
    p = sub.add_parser("seam", help="one seam as the live mix plays it: per-bar levels (linear and the mixer swap), mp3s")
    p.add_argument("album_id")
    p.add_argument("n", type=int, help="the seam tN -> tN+1")
    p.add_argument("--wavs", nargs=2, metavar=("OUT_WAV", "IN_WAV"), help="use these renders instead of rendering")
    p.add_argument("--bars", type=float, help="overlap bars (default: mixplan.md's, else 16)")
    p.add_argument("--swap", type=lambda v: v if v == "mid" else float(v), help="swap bar into the overlap (default: "
                   "mixplan.md's swap cell, else the midpoint)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--pin", help="chirp binary (default: tools/groove-pin)")
    p.add_argument("--out", default="/tmp/chirp-seams", help="where the mp3s go")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("seams", help="audit a mixtape's DJ seams: tempo drift across each overlap, dead air at the ends")
    p.add_argument("album_id")
    p.add_argument("--pin", help="chirp binary (default: tools/groove-pin)")
    p.add_argument("--flam-ms", type=float, default=10.0, help="flag a seam whose beats drift this far apart")
    p.add_argument("--dead-s", type=float, default=0.5, help="flag a track with more dead air than this after its last bar")
    p.add_argument("--json", action="store_true")
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
     "refresh": cmd_refresh, "rebaseline": cmd_rebaseline, "release": cmd_release, "seams": cmd_seams, "seam": cmd_seam}[a.cmd](a, argv)


if __name__ == "__main__":
    main()
