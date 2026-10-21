#!/usr/bin/env python3
"""Background experiment queue for climbs: render + score song variants detached, a few at a time.

  bgexp.py run NAME SONG.yaml [--ref ref/X.wav] [--sections tools/X-sections.txt] [--slots 3] [--max-load L] [--keep-wav] [-- extra chirp render args]
  bgexp.py status [--since MINUTES] [PREFIX]   total (the CLI total climbs record), exact (bgexp's legacy
                                               term recompute), raw (unrounded); a failed job's stage and error
  bgexp.py wait NAME [NAME...]          # block until those finish (for scripts)
  bgexp.py run NAME SONG --seeds 0,11 …   # one job per seed: NAME-0, NAME-11 (each with --set seed=S)
  bgexp.py compare A B                  # per-section deltas B - A; A and B may be seed families (NAME-0, NAME-11):
                                        # means over the seeds both finished

Each job waits until the 1-min load average is below --max-load (default 3x cores: don't pile onto a host storm
while the live groove plays) and for one of --slots concurrency slots (flock files), renders at nice 15 with the pinned build
($CHIRP or /tmp/lt/chirp-main/cli/chirp/target/release/chirp), then scores with likeness.py (sections + the
unrounded weighted total) and mixfeel.py; records the binary used (pin CHIRP to an immutable copy: a shared build path can be rebuilt under a queue) (punch/crest/vary per band), writing $BGEXP_DIR/NAME.json and
NAME.log ($BGEXP_DIR defaults to /tmp/lt/exp; give each climb its own so climbers don't wait on each other's slots). Never plays audio. Defaults (--ref/--sections) are the shadows climb's.
The render is deleted once scored (the score is what is kept; a render is ~60-150 MB and climbs run
hundreds): --keep-wav keeps it as $BGEXP_DIR/NAME.wav (tmpclean.py still sweeps it after 6 idle hours).
"""
import fcntl
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
import json
import os
import subprocess
import sys
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
EXP = os.environ.get("BGEXP_DIR", "/tmp/lt/exp")  # one queue (and slot set) per climber: BGEXP_DIR=/tmp/lt/exp-<id>
CHIRP = chirpbin.resolve("/tmp/lt/chirp-main/cli/chirp/target/release/chirp")
W = {"loudness": 0.14, "spectral": 0.22, "chroma": 0.22, "rhythm": 0.18, "ltas": 0.09, "stereo": 0.10, "master": 0.08}  # likeness weights, tempo excluded


def opt(args, flag, default):
    if flag in args:
        i = args.index(flag)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


def put(path, state):
    """Write a job's state atomically (status and wait never read a half-written file)."""
    tmp = f"{path}.tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, path)


def job(name, song, ref, sections, slots, extra, max_load=None, keep_wav=False):
    """A detached worker. It always ends terminal — done, or failed with the stage, the error and a traceback in
    NAME.log — whatever raises (bd-1a4f0e: a missing sections file after a good render left jobs `scoring` forever)."""
    os.makedirs(EXP, exist_ok=True)
    out = f"{EXP}/{name}.json"
    state = {"name": name, "song": song, "state": "queued", "queued": time.time()}
    put(out, state)
    wav = f"{EXP}/{name}.wav"
    try:
        _job(state, out, wav, name, song, ref, sections, slots, extra, max_load, keep_wav)
    except BaseException as e:  # noqa: BLE001
        import traceback
        state.update(state="failed", stage=state.get("state"), error=f"{type(e).__name__}: {e}", finished=time.time())
        if os.path.exists(wav):   # the render completed: keep it (tmpclean sweeps it after 6 idle hours)
            state["wav"] = f"{wav} (kept: the render completed, then {state['stage']} failed)"
        try:
            with open(f"{EXP}/{name}.log", "a") as log:
                log.write("\n" + traceback.format_exc())
        except OSError:
            pass
        put(out, state)
        if not isinstance(e, Exception):
            raise


def _job(state, out, wav, name, song, ref, sections, slots, extra, max_load, keep_wav):
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
    put(out, state)
    with open(f"{EXP}/{name}.log", "w") as log:
        r = subprocess.run(["nice", "-n", "15", CHIRP, "render", "-f", song, "-o", wav, *extra], stdout=log, stderr=log, cwd=ROOT)
        if r.returncode != 0:
            if os.path.exists(wav):
                os.remove(wav)
            state.update(state="failed", stage="rendering", error=f"render exited {r.returncode} (see {name}.log)",
                         finished=time.time())
            put(out, state)
            return
        state.update(state="scoring")
        put(out, state)
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
        exact = sum(sum(s.get(k, 0) * w for k, w in W.items()) / sum(W.values()) * du for s, du in zip(secs, durs)) / sum(durs)
        state.update(total=d["total"], exact=round(exact, 3), sections=[{k: round(v, 1) if isinstance(v, float) else v for k, v in s.items()} for s in secs])
        # bd-fd060e: which convention each number is (compare a candidate with its baseline on the SAME field)
        if "total_raw" in d:
            state["total_raw"] = d["total_raw"]
        if "coverage" in d:   # bd-066928: a render shorter than the sections is scored on its covered part only
            state["coverage"] = d["coverage"]
        state["conventions"] = {"total": "likeness CLI total (legacy-v1): the field climbs record as their best",
                                "exact": "bgexp legacy: a term-weighted recomputation from 1-decimal section terms, "
                                         "tempo excluded — not a raw score",
                                "total_raw": "likeness raw-v1: the CLI formula on unrounded terms"}
    except Exception as e:  # noqa: BLE001
        # no score: a failure (the render stays for a rescore), not a `done` without a total
        state.update(state="failed", stage="scoring", error=f"likeness: {e}", finished=time.time(),
                     wav=f"{wav} (kept: the render completed, then scoring failed)")
        put(out, state)
        return
    try:
        state["mixfeel"] = json.loads(mf.stdout)
    except Exception as e:  # noqa: BLE001
        state["mixfeel_error"] = str(e)
    if not keep_wav:
        try:
            os.remove(wav)
            state["wav"] = "deleted after scoring (--keep-wav keeps it)"
        except OSError:
            pass
    state.update(state="done", finished=time.time())
    put(out, state)


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
            # total: the CLI convention climbs record; exact: bgexp's legacy recompute; raw: unrounded (bd-fd060e)
            raw = f" raw {d['total_raw']:8.4f}" if "total_raw" in d else ""
            line += (f" total {d.get('total', float('nan')):7.3f} exact {d['exact']:7.3f}{raw}  "
                     + " ".join(f"{s['total']:5.1f}" for s in d["sections"]))
            cov = d.get("coverage") or {}
            if cov and not cov.get("complete", True):
                line += f"  SHORT: render {cov.get('candidate_seconds')} s < sections {cov.get('requested_end')} s"
            mf = d.get("mixfeel")
            if mf:
                line += "  | sub punch " + "/".join(f"{s['ours']['sub']['punch']:.1f}" for s in mf)
                line += "  pres crest " + "/".join(f"{s['ours']['pres']['crest']:.1f}" for s in mf)
        elif d.get("state") == "failed":
            line += f" {d.get('stage', '?')}: {str(d.get('error', ''))[:90]}"
        elif d.get("state") in ("rendering", "scoring"):
            line += f" ({time.time() - d.get('started', time.time()):.0f} s)"
        print(line)
    for (path, size, mtime), tag in engines.items():
        print(f"engine {tag}: {path} ({size} bytes, built {time.strftime('%H:%M', time.localtime(mtime))})")
    if rows and rows[-1].get("mixfeel"):
        mf = rows[-1]["mixfeel"]
        print(f"{'(reference)':14s} {'':9s} {'':7s}  {'':29s}  | sub punch " + "/".join(f"{s['ref']['sub']['punch']:.1f}" for s in mf)
              + "  pres crest " + "/".join(f"{s['ref']['pres']['crest']:.1f}" for s in mf))


def _done(name):
    """{seed-or-'': job} of finished jobs: NAME itself, else its seed family NAME-<int>."""
    one = f"{EXP}/{name}.json"
    if os.path.exists(one):
        d = json.load(open(one))
        return {"": d} if d.get("state") == "done" else {}
    out = {}
    for f in os.listdir(EXP) if os.path.isdir(EXP) else []:
        tail = f[len(name) + 1:-5] if f.startswith(name + "-") and f.endswith(".json") else ""
        if tail.isdigit():
            d = json.load(open(f"{EXP}/{f}"))
            if d.get("state") == "done":
                out[tail] = d
    return out


TERMS = ("loudness", "spectral", "chroma", "rhythm", "ltas", "stereo", "master")


def compare(a, b):
    """Per-section deltas B - A (means over the seeds both finished, when A and B are seed families)."""
    ja, jb = _done(a), _done(b)
    keys = sorted(set(ja) & set(jb), key=lambda k: (k != "", int(k) if k.isdigit() else -1))
    if not keys:
        sys.exit(f"bgexp compare: no finished jobs in common for {a} and {b} (seeds: {sorted(ja)} vs {sorted(jb)})")
    if [len(ja[k]["sections"]) for k in keys] != [len(jb[k]["sections"]) for k in keys]:
        sys.exit("bgexp compare: the jobs have different sections")
    mean = lambda js, f: sum(f(j) for j in js) / len(js)  # noqa: E731
    A, B = [ja[k] for k in keys], [jb[k] for k in keys]
    seeds = ",".join(k for k in keys if k) or "the one job each"
    ta, tb = mean(A, lambda j: j.get("total_raw", j["total"])), mean(B, lambda j: j.get("total_raw", j["total"]))
    print(f"{b} vs {a} (seeds {seeds}): total {ta:.3f} -> {tb:.3f}  {tb - ta:+.3f}")
    for i, sa in enumerate(A[0]["sections"]):
        va = mean(A, lambda j: j["sections"][i]["total"])
        vb = mean(B, lambda j: j["sections"][i]["total"])
        moves = {t: mean(B, lambda j: j["sections"][i].get(t, 0)) - mean(A, lambda j: j["sections"][i].get(t, 0))
                 for t in TERMS if t in sa}
        top = sorted(moves.items(), key=lambda kv: -abs(kv[1]))[:2]
        print(f"  {sa['start']:7.1f}-{sa['end']:7.1f} s  {va:5.1f} -> {vb:5.1f}  {vb - va:+5.1f}   "
              + "  ".join(f"{t} {v:+.1f}" for t, v in top))


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd = a.pop(0)
    if cmd == "run":
        extra = a[a.index("--") + 1:] if "--" in a else []
        a = a[:a.index("--")] if "--" in a else a
        ref_default, sections_default = "--ref" not in a, "--sections" not in a
        ref = opt(a, "--ref", "ref/shadows.wav")
        sections = opt(a, "--sections", "tools/shadows-sections.txt")
        slots = int(opt(a, "--slots", "3"))
        max_load = float(opt(a, "--max-load", "0")) or None
        keep_wav = "--keep-wav" in a
        seeds = opt(a, "--seeds", None)
        a = [x for x in a if x != "--keep-wav"]
        name, song = a[0], os.path.abspath(a[1])
        defaulted = [f for f, d in (("--ref", ref_default), ("--sections", sections_default)) if d]
        if defaulted and not os.path.basename(song).startswith("shadows"):
            print(f"bgexp: warning: no {' or '.join(defaulted)}: {os.path.basename(song)} will be scored against the "
                  f"shadows climb's (pass --ref ref/ID.wav --sections tools/ID-sections.txt)", file=sys.stderr)
        # caller errors now, not a failed job later (the worker still guards: files can vanish while it queues)
        for what, path, dflt in (("song", song, False), ("--ref", os.path.join(ROOT, ref), ref_default),
                                 ("--sections", os.path.join(ROOT, sections), sections_default)):
            if not os.path.isfile(path):
                sys.exit(f"bgexp: {what} {path} does not exist"
                         + (" (the default: --ref/--sections default to the shadows climb's)" if dflt else ""))
        # --seeds 0,11: one job per seed, NAME-S with --set seed=S (compare NAME … averages them)
        for n, ex in ([(f"{name}-{v.strip()}", extra + ["--set", f"seed={v.strip()}"]) for v in seeds.split(",") if v.strip()]
                      if seeds else [(name, extra)]):
            if os.fork() == 0:
                os.setsid()
                if os.fork() == 0:
                    fd = os.open(os.devnull, os.O_RDWR)
                    for k in (0, 1, 2):
                        os.dup2(fd, k)
                    job(n, song, ref, sections, slots, ex, max_load, keep_wav)
                os._exit(0)
            print(f"queued {n}")
    elif cmd == "compare":
        if len(a) != 2:
            sys.exit("bgexp compare A B")
        compare(*a)
    elif cmd == "status":
        since = opt(a, "--since", None)
        status(a[0] if a else "", float(since) if since else None)
    elif cmd == "wait":
        while any(json.load(open(f"{EXP}/{n}.json")).get("state") not in ("done", "failed") for n in a):
            time.sleep(5)
        status()


if __name__ == "__main__":
    main()
