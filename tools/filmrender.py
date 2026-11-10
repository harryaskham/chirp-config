#!/usr/bin/env python3
"""filmrender: draw an album's film as several processes side by side, join it, check it.

`chirp video --album FILE` draws the tracks one after another in one process, which uses few
cores well. The tracks' parts are independent (also in a continuous mix), so this runs a pool
of `chirp video --album FILE --only N` workers, the costliest tracks first, then one run without
`--only`, which reuses every part and joins them, and then checks the result.

    filmrender.py draw FILE -o OUT.mp4 [--size 3840x2160] [--workers 4] [--threads 5]
                  [--order 3,6,4,2,5,1,7,8] [--shutter 2] [--encoder hevc_vaapi] [--bin CHIRP]
    filmrender.py check FILE -o OUT.mp4

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


def base_cmd(a):
    cmd = [a.bin, "video", "--album", a.album, "-o", a.out, "--crf", str(a.crf)]
    if a.size:
        cmd += ["--size", a.size]
    if a.shutter and a.shutter > 1:
        cmd += ["--shutter", str(a.shutter)]
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
    log(lg, f"draw: {n} tracks, order {order}, {a.workers} workers x {a.threads} threads, size {a.size or 'as the file says'}, "
            f"shutter {a.shutter}, encoder {a.encoder or 'x264'}, bin {a.bin}")
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
            log(lg, f"worker {k}: track {t} starts")
            with open(wl, "a") as f:
                r = subprocess.run(base_cmd(a) + ["--only", str(t)], stdout=f, stderr=f, env=env)
            if r.returncode != 0:
                failed.append(t)
                log(lg, f"worker {k}: track {t} FAILED (exit {r.returncode}); see {wl}")
            else:
                log(lg, f"worker {k}: track {t} drawn in {(time.time() - t0) / 60:.1f} min")

    t0 = time.time()
    ws = [threading.Thread(target=worker, args=(k,)) for k in range(1, a.workers + 1)]
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
    ch = os.path.splitext(a.out)[0] + ".chapters.txt"
    if os.path.exists(ch):
        log(lg, "check: chapters: " + " | ".join(l.strip() for l in open(ch) if l.strip()))
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["draw", "check"])
    ap.add_argument("album")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--size")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--threads", type=int, default=5)
    ap.add_argument("--order", help="track numbers, the costliest first (default: as listed)")
    ap.add_argument("--shutter", type=int, default=1)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--encoder", help="CHIRP_VIDEO_ENCODER (hevc_vaapi for 4K)")
    ap.add_argument("--bin", default="chirp")
    a = ap.parse_args()
    a.album, a.out = os.path.abspath(os.path.expanduser(a.album)), os.path.abspath(os.path.expanduser(a.out))
    if a.cmd == "draw":
        draw(a)
    else:
        sys.exit(0 if check(a) else 1)


if __name__ == "__main__":
    main()
