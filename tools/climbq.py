#!/usr/bin/env python3
"""Background experiment queue for climbs: submit render+score jobs, let a worker run several at once (niced), and
read results later — so variants of several parts of a song (or several climbs) are measured in parallel while you
keep working.

  climbq.py submit NAME --song FILE [--set PATH=V …] [--solo T …] [--from S --to S] [--metric sections|none]
                        [--ref ref/bleed.wav] [--sections tools/bleed-sections.txt] [--keep]
  climbq.py worker [-j 3] [--idle-exit 900] [--max-load L]   run queued jobs, N at a time (no new job while the
                                                  1-min load is ≥ L, default 3× cores); exits after idle seconds
  climbq.py status                                pending / running / done with headline scores
  climbq.py result NAME                           the full result JSON

Queue dir: $CLIMBQ (default /tmp/climbq). Binary: $CHIRP (default chirp). Renders run at nice 15. A job's WAV is
deleted after scoring unless --keep (then it stays at $CLIMBQ/wav/NAME.wav). Start the worker detached, e.g.
`(setsid nohup python3 tools/climbq.py worker -j 3 >> /tmp/climbq/worker.log 2>&1 < /dev/null &)`."""
import json
import os
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
Q = os.environ.get("CLIMBQ", "/tmp/climbq")
C = os.environ.get("CHIRP", "chirp")
for d in ("jobs", "running", "done", "wav"):
    os.makedirs(os.path.join(Q, d), exist_ok=True)


def submit(a):
    name = a[0]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    multi = lambda k: [a[i + 1] for i, x in enumerate(a) if x == k]
    job = {"name": name, "song": os.path.abspath(opt("--song")), "sets": multi("--set"), "solo": multi("--solo"),
           "from": opt("--from"), "to": opt("--to"), "metric": opt("--metric", "sections"),
           "ref": os.path.join(ROOT, opt("--ref", "ref/bleed.wav")),
           "sections": os.path.join(ROOT, opt("--sections", "tools/bleed-sections.txt")),
           "keep": "--keep" in a, "submitted": time.time()}
    for d in ("running", "done"):
        p = os.path.join(Q, d, name + ".json")
        if os.path.exists(p):
            os.unlink(p)
    json.dump(job, open(os.path.join(Q, "jobs", name + ".json"), "w"))
    print(f"queued {name}")


def run(job):
    wav = os.path.join(Q, "wav", job["name"] + ".wav")
    cmd = ["nice", "-n", "15", C, "render", "-f", job["song"], "-o", wav]
    for s in job["sets"]:
        cmd += ["--set", s]
    for s in job["solo"]:
        cmd += ["--solo", s]
    if job["from"]:
        cmd += ["--from", job["from"]]
    if job["to"]:
        cmd += ["--to", job["to"]]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    res = dict(job, render_s=round(time.time() - t0, 1))
    if r.returncode:
        res["error"] = (r.stderr or r.stdout)[-400:]
        return res
    if job["metric"] == "sections":
        bounds = open(job["sections"]).read().strip()
        m = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(HERE, "likeness.py"), "sections", job["ref"], wav, bounds],
                           capture_output=True, text=True, cwd=ROOT)
        try:
            d = json.loads(m.stdout)
            res["total"] = d["total"]
            res["sections"] = [s["total"] for s in d["sections"]]
            res["components"] = [{k: round(s[k], 1) for k in ("loudness", "spectral", "chroma", "rhythm", "ltas", "stereo")} for s in d["sections"]]
        except ValueError:
            res["error"] = m.stderr[-400:]
    if not job["keep"] and os.path.exists(wav):
        os.unlink(wav)
    else:
        res["wav"] = wav
    return res


def worker(a):
    n = int(a[a.index("-j") + 1]) if "-j" in a else 3
    idle_exit = float(a[a.index("--idle-exit") + 1]) if "--idle-exit" in a else 900
    max_load = float(a[a.index("--max-load") + 1]) if "--max-load" in a else 3 * (os.cpu_count() or 8)   # wait out host storms
    lock = threading.Lock(); active = []; last = time.time()

    def take():
        with lock:
            jobs = sorted(os.listdir(os.path.join(Q, "jobs")), key=lambda f: os.path.getmtime(os.path.join(Q, "jobs", f)))
            for f in jobs:
                src, dst = os.path.join(Q, "jobs", f), os.path.join(Q, "running", f)
                try:
                    os.rename(src, dst)
                    return json.load(open(dst))
                except OSError:
                    continue
        return None

    def go(job):
        res = run(job)
        res["finished"] = time.time()
        json.dump(res, open(os.path.join(Q, "done", job["name"] + ".json"), "w"))
        try:
            os.unlink(os.path.join(Q, "running", job["name"] + ".json"))
        except OSError:
            pass
        print(time.strftime("%H:%M:%S"), job["name"], res.get("total", res.get("error", "done")), flush=True)

    print(time.strftime("%H:%M:%S"), f"worker up: -j {n}, binary {C}", flush=True)
    while True:
        active = [t for t in active if t.is_alive()]
        if len(active) < n and os.getloadavg()[0] < max_load:
            job = take()
            if job:
                t = threading.Thread(target=go, args=(job,), daemon=True); t.start(); active.append(t); last = time.time()
                continue
        if not active and time.time() - last > idle_exit:
            print(time.strftime("%H:%M:%S"), "idle — exiting", flush=True)
            return
        time.sleep(2)


def status(_):
    for d in ("jobs", "running"):
        names = sorted(f[:-5] for f in os.listdir(os.path.join(Q, d)))
        print(f"{'pending' if d == 'jobs' else 'running'}: {', '.join(names) or '-'}")
    done = sorted(os.listdir(os.path.join(Q, "done")), key=lambda f: os.path.getmtime(os.path.join(Q, "done", f)))
    for f in done:
        r = json.load(open(os.path.join(Q, "done", f)))
        if "error" in r:
            head = "ERROR: " + r["error"][-80:].replace("\n", " ")
        else:
            head = r.get("total", "rendered → " + r.get("wav", "?"))
        print(f"done {r['name']:24s} {head}  {r.get('sections', '')}  ({r.get('render_s', '?')} s)")


def result(a):
    print(open(os.path.join(Q, "done", a[0] + ".json")).read())


if __name__ == "__main__":
    cmd, rest = sys.argv[1], sys.argv[2:]
    {"submit": submit, "worker": worker, "status": status, "result": result}[cmd](rest)
