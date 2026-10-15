#!/usr/bin/env python3
"""Background experiment queue for climbs: render + score song variants detached, a few at a time.

  bgexp.py run NAME SONG.yaml [--ref ref/X.wav] [--sections tools/X-sections.txt] [--slots 3] [--max-load L] [-- extra chirp render args]
  bgexp.py status [--since MINUTES] [PREFIX]
  bgexp.py wait NAME [NAME...]          # block until those finish (for scripts)

Each job waits until the 1-min load average is below --max-load (default 3x cores: don't pile onto a host storm
while the live groove plays) and for one of --slots concurrency slots (flock files), renders at nice 15 with the pinned build
($CHIRP or /tmp/lt/chirp-main/cli/chirp/target/release/chirp), then scores with likeness.py (sections + the
unrounded weighted total) and mixfeel.py; records the binary used (pin CHIRP to an immutable copy: a shared build path can be rebuilt under a queue) (punch/crest/vary per band), writing $BGEXP_DIR/NAME.json and
NAME.log ($BGEXP_DIR defaults to /tmp/lt/exp; give each climb its own so climbers don't wait on each other's slots). Never plays audio. Defaults (--ref/--sections) are the shadows climb's.
"""
import fcntl
import json
import os
import subprocess
import sys
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
EXP = os.environ.get("BGEXP_DIR", "/tmp/lt/exp")  # one queue (and slot set) per climber: BGEXP_DIR=/tmp/lt/exp-<id>
CHIRP = os.environ.get("CHIRP", "/tmp/lt/chirp-main/cli/chirp/target/release/chirp")
W = {"loudness": 0.14, "spectral": 0.22, "chroma": 0.22, "rhythm": 0.18, "ltas": 0.09, "stereo": 0.10}


def opt(args, flag, default):
    if flag in args:
        i = args.index(flag)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


def job(name, song, ref, sections, slots, extra, max_load=None):
    os.makedirs(EXP, exist_ok=True)
    out = f"{EXP}/{name}.json"
    state = {"name": name, "song": song, "state": "queued", "queued": time.time()}
    json.dump(state, open(out, "w"))
    lock = None
    max_load = max_load or 3.0 * (os.cpu_count() or 8)
    while lock is None:
        if os.getloadavg()[0] > max_load:  # host storm: don't pile on (the live groove underruns)
            time.sleep(10)
            continue
        for k in range(slots):
            f = open(f"{EXP}/slot-{k}.lock", "w")
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock = f
                break
            except BlockingIOError:
                f.close()
        if lock is None:
            time.sleep(3)
    st = os.stat(CHIRP)
    ver = subprocess.run([CHIRP, "--version"], capture_output=True, text=True).stdout.strip()
    state.update(state="rendering", started=time.time(), engine={"path": CHIRP, "size": st.st_size, "mtime": int(st.st_mtime), "version": ver})
    json.dump(state, open(out, "w"))
    wav = f"{EXP}/{name}.wav"
    with open(f"{EXP}/{name}.log", "w") as log:
        r = subprocess.run(["nice", "-n", "15", CHIRP, "render", "-f", song, "-o", wav, *extra], stdout=log, stderr=log, cwd=ROOT)
        if r.returncode != 0:
            state.update(state="failed", finished=time.time())
            json.dump(state, open(out, "w"))
            return
        state.update(state="scoring")
        json.dump(state, open(out, "w"))
        cuts = open(os.path.join(ROOT, sections)).read().split()[0]
        lk = subprocess.run(["nice", "-n", "10", sys.executable, f"{TOOLS}/likeness.py", "sections", ref, wav, cuts],
                            capture_output=True, text=True, cwd=ROOT)
        mf = subprocess.run(["nice", "-n", "10", sys.executable, f"{TOOLS}/mixfeel.py", ref, wav, cuts, "--json"],
                            capture_output=True, text=True, cwd=ROOT)
        log.write(lk.stderr + mf.stderr)
    try:
        d = json.loads(lk.stdout)
        secs = d["sections"]
        durs = [s["end"] - s["start"] for s in secs]
        exact = sum(sum(s[k] * w for k, w in W.items()) / 0.95 * du for s, du in zip(secs, durs)) / sum(durs)
        state.update(total=d["total"], exact=round(exact, 3), sections=[{k: round(v, 1) if isinstance(v, float) else v for k, v in s.items()} for s in secs])
    except Exception as e:  # noqa: BLE001
        state.update(error=f"likeness: {e}")
    try:
        state["mixfeel"] = json.loads(mf.stdout)
    except Exception as e:  # noqa: BLE001
        state["mixfeel_error"] = str(e)
    state.update(state="done", finished=time.time())
    json.dump(state, open(out, "w"))


def status(prefix="", since=None):
    rows = []
    for f in sorted(os.listdir(EXP)) if os.path.isdir(EXP) else []:
        if not f.endswith(".json") or not f.startswith(prefix):
            continue
        try:
            d = json.load(open(f"{EXP}/{f}"))
        except Exception:  # noqa: BLE001
            continue
        if since and d.get("queued", 0) < time.time() - since * 60:
            continue
        rows.append(d)
    rows.sort(key=lambda d: d.get("queued", 0))
    engines = {}
    for d in rows:
        e = d.get('engine'); tag = ''
        if e:
            key = (e['path'], e['size'], e['mtime']); tag = engines.setdefault(key, chr(ord('A') + len(engines)))
        line = f"{d['name']:14s} {d['state']:9s}{tag:2s}"
        if d.get("state") == "done" and "exact" in d:
            line += f" {d['exact']:7.3f}  " + " ".join(f"{s['total']:5.1f}" for s in d["sections"])
            mf = d.get("mixfeel")
            if mf:
                line += "  | sub punch " + "/".join(f"{s['ours']['sub']['punch']:.1f}" for s in mf)
                line += "  pres crest " + "/".join(f"{s['ours']['pres']['crest']:.1f}" for s in mf)
        elif d.get("state") in ("rendering", "scoring"):
            line += f" ({time.time() - d.get('started', time.time()):.0f} s)"
        print(line)
    for (path, size, mtime), tag in engines.items():
        print(f"engine {tag}: {path} ({size} bytes, built {time.strftime('%H:%M', time.localtime(mtime))})")
    if rows and rows[-1].get("mixfeel"):
        mf = rows[-1]["mixfeel"]
        print(f"{'(reference)':14s} {'':9s} {'':7s}  {'':29s}  | sub punch " + "/".join(f"{s['ref']['sub']['punch']:.1f}" for s in mf)
              + "  pres crest " + "/".join(f"{s['ref']['pres']['crest']:.1f}" for s in mf))


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd = a.pop(0)
    if cmd == "run":
        extra = a[a.index("--") + 1:] if "--" in a else []
        a = a[:a.index("--")] if "--" in a else a
        ref = opt(a, "--ref", "ref/shadows.wav")
        sections = opt(a, "--sections", "tools/shadows-sections.txt")
        slots = int(opt(a, "--slots", "3"))
        max_load = float(opt(a, "--max-load", "0")) or None
        name, song = a[0], os.path.abspath(a[1])
        if os.fork() == 0:
            os.setsid()
            if os.fork() == 0:
                fd = os.open(os.devnull, os.O_RDWR)
                for k in (0, 1, 2):
                    os.dup2(fd, k)
                job(name, song, ref, sections, slots, extra, max_load)
            os._exit(0)
        print(f"queued {name}")
    elif cmd == "status":
        since = opt(a, "--since", None)
        status(a[0] if a else "", float(since) if since else None)
    elif cmd == "wait":
        while any(json.load(open(f"{EXP}/{n}.json")).get("state") not in ("done", "failed") for n in a):
            time.sleep(5)
        status()


if __name__ == "__main__":
    main()
