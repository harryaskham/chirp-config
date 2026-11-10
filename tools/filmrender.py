#!/usr/bin/env python3
"""filmrender: draw an album's film as several processes side by side, join it, check it.

`chirp video --album FILE` draws the tracks one after another in one process, which uses few
cores well. The tracks' parts are independent (also in a continuous mix), so this runs a pool
of `chirp video --album FILE --only N` workers, the costliest tracks first, then one run without
`--only`, which reuses every part and joins them, and then checks the result.

    filmrender.py prepare FILE --dir DIR [--songs SNAPSHOT_DIR]
    filmrender.py draw FILE -o OUT.mp4 [--size 3840x2160] [--workers 4] [--threads 5]
                  [--order 3,6,4,2,5,1,7,8] [--shutter 2] [--encoder hevc_vaapi] [--bin CHIRP]
                  [--fps 60] [--plan 3:6,6:4,4:3,2:3,1:2,5:2,7:1,8:1]
    filmrender.py check FILE -o OUT.mp4
    filmrender.py finish FILE -o OUT.mp4 [--final OUT-final.mp4]

`finish` makes the file to publish from a joined HEVC film, without re-encoding: tagged `hvc1`
(Apple's players do not open `hev1`), with the HEVC level its size and frame rate need (the
GPU encoder marks 2160p60 as level 5.0, which is 2160p30's), and the index at the front. It
checks the copy has the same frames and length before saying so, and leaves OUT as it is.

With --plan every track is drawn at once, each by its own process with its own number of
threads (TRACK:THREADS, the dearest tracks the most), so they all finish at about the same
time and no core waits for a long track to end: the best use of the cores when the tracks'
costs are known. Without it, --workers processes of --threads threads take the tracks in
--order.

`prepare` freezes what the film reads: it copies every song (from the album file, or tNN.song
from a listen snapshot with --songs) and every programme into DIR, writes DIR/video.yaml that
points at the copies, and DIR/manifest.json with a hash of each (and of the prefab kits, the mix
and its release.json). Draw DIR/video.yaml; `draw` and `check` say if anything in the manifest
has changed since.

Rules (docs/vis.md, "Album finals"):
  - Run it as its own guarded user unit, never from a shell (a runtime restart kills what a shell
    started, and the groove's guard can only pause units named guarded-*):
        systemd-run --user --collect --unit=guarded-soft-film -p CPUSchedulingPolicy=idle \\
            -p Nice=15 python3 tools/filmrender.py draw ... 
  - workers x threads should not exceed the CPUs free for it (the groove keeps four).
  - Nothing the film reads may change while it draws (songs, vis/, the binary): a part is keyed
    on them, so a change makes later workers redraw. Use a pinned binary (--bin).
  - A stopped run is resumed by running it again: finished parts are reused.

It writes OUT.log (progress, one line an event) and OUT.parts/worker-N.log (chirp's own output).
"""
import argparse, json, os, queue, re, subprocess, sys, threading, time


def log(path, msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    with open(path, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def dur(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def songs_in(album):
    """How many songs the album file lists (its `songs:` entries)."""
    n, inside = 0, False
    for line in open(album):
        if re.match(r"^songs:\s*$", line):
            inside = True
        elif inside and re.match(r"^\s+-\s", line):
            n += 1
        elif inside and re.match(r"^\S", line):
            inside = False
    return n


def mix_audio(album):
    """The continuous mix's WAV, if the album file is a mix."""
    inside = False
    for line in open(album):
        if re.match(r"^mix:\s*$", line):
            inside = True
        elif inside:
            m = re.match(r"^\s+audio:\s*(.+?)\s*$", line)
            if m:
                return os.path.expanduser(m.group(1).strip().strip('"').strip("'"))
            if re.match(r"^\S", line):
                inside = False
    return None


def sha(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def release_of(album):
    inside = False
    for line in open(album):
        if re.match(r"^mix:\s*$", line):
            inside = True
        elif inside:
            m = re.match(r"^\s+release:\s*(.+?)\s*$", line)
            if m:
                return os.path.expanduser(m.group(1).strip().strip('"').strip("'"))
            if re.match(r"^\S", line):
                inside = False
    return None


def prepare(a):
    import shutil
    cfg = os.path.expanduser("~/.config/chirp")
    d = os.path.abspath(os.path.expanduser(a.dir))
    os.makedirs(f"{d}/songs", exist_ok=True)
    os.makedirs(f"{d}/vis", exist_ok=True)
    out, n, inside, files = [], 0, False, {}
    for line in open(a.album).read().split("\n"):
        if re.match(r"^songs:\s*$", line):
            inside = True
        elif inside and re.match(r"^\s+-\s*\{", line):
            n += 1
            mf = re.search(r"file:\s*([^,}]+)", line)
            mv = re.search(r"vis:\s*([^,}]+)", line)
            if not mf or not mv:
                sys.exit(f"filmrender: song {n} needs file: and vis: on its line")
            src = os.path.join(a.songs, f"t{n:02d}.song") if a.songs else os.path.expanduser(mf.group(1).strip())
            if not os.path.isabs(src):
                src = os.path.join(os.path.dirname(a.album), src)
            song = f"{d}/songs/{n:02d}.yaml"
            shutil.copyfile(src, song)
            v = mv.group(1).strip()
            vsrc = os.path.expanduser(v) if v.endswith((".yaml", ".yml")) else f"{cfg}/vis/{v}.yaml"
            if not os.path.exists(vsrc):
                sys.exit(f"filmrender: song {n}: no programme at {vsrc} (a built-in look cannot be frozen)")
            vis = f"{d}/vis/{n:02d}-{os.path.basename(vsrc)}"
            shutil.copyfile(vsrc, vis)
            line = line[:mf.start(1)] + song + line[mf.end(1):]
            mv = re.search(r"vis:\s*([^,}]+)", line)
            line = line[:mv.start(1)] + vis + line[mv.end(1):]
            files[song] = f"song {n} from {src}"
            files[vis] = f"programme {n} from {vsrc}"
        elif inside and re.match(r"^\S", line):
            inside = False
        out.append(line)
    if n == 0:
        sys.exit(f"filmrender: no songs in {a.album}")
    # The mix and its tracklist are frozen too: copies in DIR, so the film reads the same
    # sound whatever happens to the originals, and its parts stay good if the originals move
    # (a part is keyed by the mix's path). `check` says whether the original still matches.
    sources = {}
    for key, src, name in (("audio", mix_audio(a.album), "mix.wav"), ("release", release_of(a.album), "release.json")):
        if not src:
            continue
        if not os.path.exists(src):
            print(f"filmrender: {key} is not there yet: {src}")
            continue
        dst = f"{d}/{name}"
        if not (os.path.exists(dst) and sha(dst) == sha(src)):
            shutil.copyfile(src, dst)
        inside = False
        for i, line in enumerate(out):
            if re.match(r"^mix:\s*$", line):
                inside = True
            elif inside and re.match(rf"^\s+{key}:", line):
                out[i] = re.match(r"^\s+", line).group(0) + f'{key}: "{dst}"'
                break
            elif inside and re.match(r"^\S", line):
                inside = False
        files[dst] = "the mix" if key == "audio" else "the mix's tracklist"
        sources[dst] = src
    open(f"{d}/video.yaml", "w").write("\n".join(out))
    man = {"album": a.album, "files": {}}
    for f, what in files.items():
        man["files"][f] = {"what": what, "sha": sha(f)}
        if f in sources:
            man["files"][f]["source"] = sources[f]
    # What the programmes use by name and cannot be copied: the prefab kits.
    for f in sorted(os.listdir(f"{cfg}/vis")):
        if f.startswith("kit-") and f.endswith(".yaml"):
            man["files"][f"{cfg}/vis/{f}"] = {"what": "prefab", "sha": sha(f"{cfg}/vis/{f}")}
    json.dump(man, open(f"{d}/manifest.json", "w"), indent=1)
    print(f"prepared {n} songs in {d}: draw {d}/video.yaml ({len(man['files'])} files in the manifest)")


def changed(album):
    """Files of the manifest beside the album file (if it was prepared) that differ now."""
    mf = os.path.join(os.path.dirname(album), "manifest.json")
    if not os.path.exists(mf):
        return None
    bad = []
    for f, e in json.load(open(mf))["files"].items():
        if not os.path.exists(f):
            bad.append(f"{f} (gone)")
        elif sha(f) != e["sha"]:
            bad.append(f"{f} ({e['what']})")
    return bad


def sources(album):
    """(frozen copy, where it came from, whether that is still the same) for a prepared album."""
    mf = os.path.join(os.path.dirname(album), "manifest.json")
    if not os.path.exists(mf):
        return []
    out = []
    for f, e in json.load(open(mf))["files"].items():
        src = e.get("source")
        if not src:
            m = re.match(r"^(?:song|programme) \d+ from (.+)$", e.get("what", ""))
            src = m.group(1) if m else None
        if src:
            out.append((f, src, os.path.exists(src) and sha(src) == e["sha"]))
    return out


def base_cmd(a):
    cmd = [a.bin, "video", "--album", a.album, "-o", a.out, "--crf", str(a.crf)]
    if a.size:
        cmd += ["--size", a.size]
    if a.shutter and a.shutter > 1:
        cmd += ["--shutter", str(a.shutter)]
    if a.fps:
        cmd += ["--fps", str(a.fps)]
    return cmd


def draw(a):
    n = songs_in(a.album)
    if n == 0:
        sys.exit(f"filmrender: no songs in {a.album}")
    order = [int(x) for x in a.order.split(",")] if a.order else list(range(1, n + 1))
    if sorted(order) != list(range(1, n + 1)):
        sys.exit(f"filmrender: --order must name each of the {n} tracks once")
    os.makedirs(os.path.splitext(a.out)[0] + ".parts", exist_ok=True)
    lg = os.path.splitext(a.out)[0] + ".log"
    env = dict(os.environ, RAYON_NUM_THREADS=str(a.threads))
    if a.encoder:
        env["CHIRP_VIDEO_ENCODER"] = a.encoder
    ch = changed(a.album)
    if ch is None:
        log(lg, "draw: this album file was not prepared (no manifest beside it): nothing guards its songs and programmes")
    elif ch:
        log(lg, f"draw: NOT started: changed since prepare: {ch}")
        sys.exit(1)
    plan = {}
    if a.plan:
        for item in a.plan.split(","):
            t, th = item.split(":")
            plan[int(t)] = int(th)
        if sorted(plan) != list(range(1, n + 1)):
            sys.exit(f"filmrender: --plan must give each of the {n} tracks its threads")
        order = sorted(plan, key=lambda t: -plan[t])
    log(lg, f"draw: {n} tracks, " + (f"plan {plan} ({sum(plan.values())} threads)" if plan else f"order {order}, {a.workers} workers x {a.threads} threads")
            + f", size {a.size or 'as the file says'}, fps {a.fps or 'as the file says'}, shutter {a.shutter}, encoder {a.encoder or 'x264'}, bin {a.bin}")
    q = queue.Queue()
    for t in order:
        q.put(t)
    failed = []

    def worker(k):
        wl = os.path.join(os.path.splitext(a.out)[0] + ".parts", f"worker-{k}.log")
        while True:
            try:
                t = q.get_nowait()
            except queue.Empty:
                return
            t0 = time.time()
            e = dict(env, RAYON_NUM_THREADS=str(plan[t])) if plan else env
            log(lg, f"worker {k}: track {t} starts" + (f" on {plan[t]} threads" if plan else ""))
            with open(wl, "a") as f:
                r = subprocess.run(base_cmd(a) + ["--only", str(t)], stdout=f, stderr=f, env=e)
            if r.returncode != 0:
                failed.append(t)
                log(lg, f"worker {k}: track {t} FAILED (exit {r.returncode}); see {wl}")
            else:
                log(lg, f"worker {k}: track {t} drawn in {(time.time() - t0) / 60:.1f} min")

    t0 = time.time()
    ws = [threading.Thread(target=worker, args=(k,)) for k in range(1, (n if plan else a.workers) + 1)]
    for w in ws:
        w.start()
    for w in ws:
        w.join()
    if failed:
        log(lg, f"NOT joined: tracks {sorted(failed)} failed")
        sys.exit(1)
    log(lg, f"all parts drawn in {(time.time() - t0) / 3600:.2f} h; joining")
    jl = os.path.join(os.path.splitext(a.out)[0] + ".parts", "join.log")
    with open(jl, "w") as f:
        r = subprocess.run(base_cmd(a), stdout=f, stderr=f, env=env)
    tail = open(jl).read().replace("\r", "\n").strip().split("\n")[-1]
    log(lg, f"join: exit {r.returncode}: {tail[:200]}")
    if r.returncode != 0 or "0 drawn" not in tail:
        log(lg, "the join drew parts again or failed: something the film reads changed while it drew; check before use")
    ok = check(a, lg)
    log(lg, "DONE" if ok and r.returncode == 0 else "DONE WITH PROBLEMS")
    sys.exit(0 if ok and r.returncode == 0 else 1)


def check(a, lg=None):
    lg = lg or os.path.splitext(a.out)[0] + ".log"
    if not os.path.exists(a.out):
        log(lg, f"check: {a.out} is not there")
        return False
    v = dur(a.out)
    ok = v > 0
    info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames",
                           "-of", "compact", a.out], capture_output=True, text=True).stdout.strip().replace("\n", " ; ")
    log(lg, f"check: {a.out}: {v:.3f} s, {os.path.getsize(a.out) / 1e9:.2f} GB; {info}")
    mix = mix_audio(a.album)
    if mix and os.path.exists(mix):
        m = dur(mix)
        good = abs(v - m) < 0.1
        ok = ok and good
        log(lg, f"check: the mix is {m:.3f} s; the film differs by {v - m:+.3f} s ({'ok' if good else 'WRONG LENGTH'})")
    moved = changed(a.album)
    if moved:
        ok = False
        log(lg, f"check: CHANGED since prepare (the film may mix old and new): {moved}")
    elif moved is not None:
        log(lg, "check: nothing in the manifest has changed since prepare")
    # Where a frozen copy came from (the songs, the mix): is the original still the same?
    for f, src, same in sources(a.album):
        log(lg, f"check: {os.path.basename(f)} is {'the same as' if same else 'NOT what is now at'} {src}"
                + ("" if same else " (the film was drawn on the frozen copy; redraw from a new prepare if the new one is wanted)"))
    ch = os.path.splitext(a.out)[0] + ".chapters.txt"
    if os.path.exists(ch):
        log(lg, "check: chapters: " + " | ".join(l.strip() for l in open(ch) if l.strip()))
    return ok


# HEVC levels: (level_idc, most luma samples a picture, most luma samples a second).
HEVC_LEVELS = [(120, 2_228_224, 66_846_720), (123, 2_228_224, 133_693_440), (150, 8_912_896, 267_386_880),
               (153, 8_912_896, 534_773_760), (156, 8_912_896, 1_069_547_520), (180, 35_651_584, 1_069_547_520)]


def probe(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=codec_name,codec_tag_string,level,width,height,r_frame_rate,nb_frames", "-of", "json", f],
                         capture_output=True, text=True).stdout
    st = (json.loads(out or "{}").get("streams") or [{}])[0]
    num, _, den = str(st.get("r_frame_rate", "0/1")).partition("/")
    st["fps"] = float(num) / float(den or 1) if float(den or 1) else 0.0
    return st


def finish(a):
    lg = os.path.splitext(a.out)[0] + ".log"
    if not os.path.exists(a.out):
        log(lg, f"finish: {a.out} is not there")
        return False
    st = probe(a.out)
    if st.get("codec_name") != "hevc":
        log(lg, f"finish: {a.out} is {st.get('codec_name')}, not HEVC: nothing to do, publish it as it is")
        return True
    final = os.path.abspath(os.path.expanduser(a.final)) if a.final else os.path.splitext(a.out)[0] + "-final.mp4"
    w, h, fps = int(st["width"]), int(st["height"]), st["fps"]
    need = next((l for l, ps, sr in HEVC_LEVELS if w * h <= ps and w * h * fps <= sr), 180)
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", a.out, "-map", "0:v:0", "-map", "0:a?", "-map_chapters", "0",
           "-c", "copy", "-tag:v", "hvc1"]
    if int(st.get("level") or 0) < need:
        cmd += ["-bsf:v", f"hevc_metadata=level={need / 30:g}"]
    cmd += ["-movflags", "+faststart", final]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        log(lg, f"finish: ffmpeg failed: {r.stderr.strip()[-300:]}")
        return False
    ft = probe(final)
    same = ft.get("nb_frames") == st.get("nb_frames") and abs(dur(final) - dur(a.out)) < 0.05
    ok = same and ft.get("codec_tag_string") == "hvc1" and int(ft.get("level") or 0) >= need
    log(lg, f"finish: {final}: {w}x{h} at {fps:g} frames a second, tag {ft.get('codec_tag_string')}, level {int(ft.get('level') or 0) / 30:g} "
            f"(was {st.get('codec_tag_string')}, {int(st.get('level') or 0) / 30:g}; needs {need / 30:g}), {ft.get('nb_frames')} frames, "
            f"{dur(final):.3f} s, {os.path.getsize(final) / 1e9:.2f} GB: {'ok' if ok else 'NOT the same as the joined film: do not publish'}")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["prepare", "draw", "check", "finish"])
    ap.add_argument("album")
    ap.add_argument("-o", "--out")
    ap.add_argument("--final", help="finish: the file to write (default OUT-final.mp4)")
    ap.add_argument("--dir", help="prepare: where the frozen copies go")
    ap.add_argument("--songs", help="prepare: a listen snapshot's directory (tNN.song) to take the songs from")
    ap.add_argument("--size")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--threads", type=int, default=5)
    ap.add_argument("--order", help="track numbers, the costliest first (default: as listed)")
    ap.add_argument("--shutter", type=int, default=1)
    ap.add_argument("--fps", type=float, help="frames a second (default: as the album file says)")
    ap.add_argument("--plan", help="TRACK:THREADS,… every track at once, each on its own threads")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--encoder", help="CHIRP_VIDEO_ENCODER (hevc_vaapi for 4K)")
    ap.add_argument("--bin", default="chirp")
    a = ap.parse_args()
    a.album = os.path.abspath(os.path.expanduser(a.album))
    if a.cmd == "prepare":
        if not a.dir:
            sys.exit("filmrender: prepare needs --dir")
        return prepare(a)
    if not a.out:
        sys.exit("filmrender: draw and check need -o OUT.mp4")
    a.out = os.path.abspath(os.path.expanduser(a.out))
    if a.cmd == "draw":
        draw(a)
    elif a.cmd == "finish":
        sys.exit(0 if finish(a) else 1)
    else:
        sys.exit(0 if check(a) else 1)


if __name__ == "__main__":
    main()
