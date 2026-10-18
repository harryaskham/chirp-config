#!/usr/bin/env python3
"""Cross-climb check: re-score every enabled climb under two setups and report the deltas.

A shared change — an engine build, a built-in or shared patch, a default — has to be judged on
every song, not the one it was found on (skill: "Changing a default needs a cross-song check").
Each side is a binary plus an optional config directory and extra render arguments; every enabled
climb's current `song` is rendered with both and scored with its own registry metric. CPU cost
comes from the receipts (`timings.cpu_ms`, load-independent), so a change that wins a little but
costs a lot shows up too.

  crossclimb.py --b-bin /tmp/lt/chirp-new                 # an engine build vs the installed chirp
  crossclimb.py --b-cfg /tmp/cfg-copy                     # a patch change in a private config copy
  crossclimb.py --b-args "--volume 0dB" --songs bleed,pneuma -j 4
  crossclimb.py --b-cfg /tmp/cfg-copy --refit            # library fixes: let each side's master adapt first

Renders go to /tmp/crossclimb/<id>-{a,b}.wav (removed afterwards unless --keep).
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/tmp/crossclimb"


def first_json(text):
    i = text.find("{")
    return json.loads(text[i:]) if i >= 0 else None


def side(name, binary, cfg, extra, threads, refit=False):
    env = dict(os.environ)
    # One render thread by default: idle rayon workers spin, which counts as CPU time and would
    # triple a song's apparent cost; songs run in parallel instead (-j).
    env["RAYON_NUM_THREADS"] = str(threads)
    if cfg:
        env["XDG_CONFIG_HOME"] = os.path.dirname(os.path.abspath(cfg)) if os.path.basename(cfg.rstrip("/")) == "chirp" else cfg
    return {"name": name, "bin": binary, "env": env, "args": shlex.split(extra or ""), "refit": refit}


def run_one(climb, s, keep):
    wav = f"{OUT}/{climb['id']}-{s['name']}.wav"
    song = os.path.join(ROOT, climb["song"])
    p = subprocess.run([s["bin"], "render", "-f", song, *s["args"], "-o", wav, "--json"],
                       capture_output=True, text=True, env=s["env"], cwd=ROOT)
    rc = first_json(p.stdout) or {}
    if rc.get("status") != "success":
        return {"error": ((rc.get("error") or {}).get("message") or p.stderr.strip())[:160]}
    data = rc.get("data") or {}
    dur = data.get("duration") or 0
    cpu = (data.get("timings") or {}).get("cpu_ms")
    raw = None
    if s.get("refit"):
        raw = score(climb, wav)
        # Let this side's master adapt before scoring: fit mastereq.py's residual EQ to the render and append
        # it to the song's master (canonical JSON renders like the YAML). Both sides get the same treatment, so
        # a library fix is not judged against masters fitted to the old library.
        ref = re.search(r"(ref/\S+\.wav)", climb["metric"])
        eq = subprocess.run([sys.executable, os.path.join(ROOT, "tools/mastereq.py"), ref.group(1), wav, "--json"],
                            capture_output=True, text=True, cwd=ROOT) if ref else None
        plan = subprocess.run([s["bin"], "plan", "--json", "-f", song], capture_output=True, text=True,
                              env=s["env"], cwd=ROOT)
        try:
            stage = json.loads(eq.stdout)["eq"]
            canon = json.loads(plan.stdout)["data"]["canonical"]
        except (AttributeError, ValueError, KeyError, TypeError):
            return {"error": "refit: " + ((eq.stderr if eq else "no ref in metric") or plan.stderr)[-160:]}
        m = canon.get("master")
        if isinstance(m, list):
            canon["master"] = m + [stage]
        else:
            m = m or {}
            m["fx"] = list(m.get("fx") or []) + [stage]
            canon["master"] = m
        doc = f"{OUT}/{climb['id']}-{s['name']}-refit.json"
        json.dump(canon, open(doc, "w"))
        p = subprocess.run([s["bin"], "render", "-f", doc, *s["args"], "-o", wav, "--json"],
                           capture_output=True, text=True, env=s["env"], cwd=ROOT)
        if (first_json(p.stdout) or {}).get("status") != "success":
            return {"error": "refit render: " + p.stderr.strip()[-160:]}
    got = score(climb, wav)
    if not keep:
        os.path.exists(wav) and os.remove(wav)
    if isinstance(got, str):
        return {"error": got}
    # With --refit a side scores its better of raw and re-fitted: a refit that hurts a song (its own section
    # masters beat a generic EQ) must not handicap both sides alike and hide a loss (Saturnine, tight-kit air).
    best = max(got, raw) if isinstance(raw, float) else got
    return {"score": best, "raw": raw, "refit": got if raw is not None else None,
            "rt": (cpu / 1000 / dur) if cpu and dur else None, "short": SHORT.get(wav)}


SHORT = {}   # render path -> the metric's coverage summary, when the render did not cover its sections (bd-066928)


def score(climb, wav):
    metric = climb["metric"].replace("OUT.wav", wav)
    m = subprocess.run(metric, shell=True, capture_output=True, text=True, cwd=ROOT)
    doc = first_json(m.stdout) or {}
    if "total" not in doc:
        return "metric: " + (m.stderr.strip() or m.stdout.strip())[-160:]
    cov = doc.get("coverage") or {}
    if cov and not cov.get("complete", True):
        SHORT[wav] = cov
    else:
        SHORT.pop(wav, None)
    return float(doc["total"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a-bin", default="chirp", help="baseline binary (default: chirp on PATH)")
    ap.add_argument("--b-bin", help="candidate binary (default: the baseline's)")
    ap.add_argument("--a-cfg", help="baseline config dir (XDG_CONFIG_HOME, or a .../chirp dir)")
    ap.add_argument("--b-cfg", help="candidate config dir")
    ap.add_argument("--a-args", default="", help="extra render args for the baseline")
    ap.add_argument("--b-args", default="", help="extra render args for the candidate")
    ap.add_argument("--songs", help="comma-separated climb ids (default: every enabled climb)")
    ap.add_argument("-j", type=int, default=3, help="songs in parallel (default 3)")
    ap.add_argument("--threads", type=int, default=1, help="render threads per song (default 1: clean CPU cost)")
    ap.add_argument("--refit", action="store_true",
                    help="also refit each side's master (mastereq.py residual EQ) and score each side at its better of raw and "
                         "refit: masters fitted to the current library double-correct a library fix, but a generic refit "
                         "can also hurt a song (CPU: the first render)")
    ap.add_argument("--keep", action="store_true", help="keep the renders")
    ap.add_argument("--json", action="store_true", help="print the rows as JSON")
    a = ap.parse_args()
    if not (a.b_bin or a.b_cfg or a.b_args or a.a_cfg or a.a_args):
        ap.error("the two sides are identical: give --b-bin, --b-cfg or --b-args")
    os.makedirs(OUT, exist_ok=True)
    climbs = [c for c in json.load(open(os.path.join(ROOT, "climbs.json")))["climbs"]
              if c.get("enabled") and c.get("song") and os.path.exists(os.path.join(ROOT, c["song"]))]
    if a.songs:
        want = set(a.songs.split(","))
        climbs = [c for c in climbs if c["id"] in want]
    sa = side("a", a.a_bin, a.a_cfg, a.a_args, a.threads, a.refit)
    sb = side("b", a.b_bin or a.a_bin, a.b_cfg, a.b_args, a.threads, a.refit)

    def both(c):
        return c["id"], run_one(c, sa, a.keep), run_one(c, sb, a.keep)

    rows = []
    with ThreadPoolExecutor(max_workers=max(1, a.j)) as ex:
        for cid, ra, rb in ex.map(both, climbs):
            rows.append({"id": cid, "a": ra, "b": rb})
            if not a.json:
                if "error" in ra or "error" in rb:
                    print(f"{cid:30s} ERROR a: {ra.get('error', 'ok')} | b: {rb.get('error', 'ok')}", flush=True)
                else:
                    rt = lambda r: f"{r['rt']:.2f}" if r.get("rt") is not None else "  - "
                    rf = lambda r: (f" (raw {r['raw']:.2f}, refit {r['refit']:.2f})"
                                    if isinstance(r.get("raw"), float) and isinstance(r.get("refit"), float) else "")
                    sh = next((r["short"] for r in (ra, rb) if r.get("short")), None)
                    flag = (f"   SHORT: render {sh.get('candidate_seconds')} s < sections {sh.get('requested_end')} s"
                            if sh else "")   # compared over the covered part only (bd-066928)
                    print(f"{cid:30s} {ra['score']:7.2f} -> {rb['score']:7.2f}  {rb['score'] - ra['score']:+6.2f}"
                          f"   cpu x RT {rt(ra)} -> {rt(rb)}{rf(ra)}{rf(rb)}{flag}", flush=True)
    ok = [r for r in rows if "score" in r["a"] and "score" in r["b"]]
    if a.json:
        print(json.dumps(rows, indent=1))
        return
    if ok:
        d = [r["b"]["score"] - r["a"]["score"] for r in ok]
        worse = [r["id"] for r, x in zip(ok, d) if x < -0.1]
        better = [r["id"] for r, x in zip(ok, d) if x > 0.1]
        print(f"\n{len(ok)} songs: mean {sum(d) / len(d):+.2f}, sum {sum(d):+.2f}; "
              f"better {len(better)} ({', '.join(better)}), worse {len(worse)} ({', '.join(worse)})")
        print("A default may change only when this is neutral or positive across the songs it touches.")
    sys.exit(1 if len(ok) < len(rows) else 0)


if __name__ == "__main__":
    main()
