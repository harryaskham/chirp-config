#!/usr/bin/env python3
"""Fair patch test: swap a part's patch, refit the master's per-section EQ for EACH candidate (the current patch too,
as the control), and score every candidate on held-out seeds. A plain swap is unfair when the master EQ lanes were
fitted to the old patch (Daydreaming's piano swaps lost for months that way).

  patchtest.py SONG TRACK[,TRACK2] PATCH[,PATCH2,...] [--zero eq,rq] [--refit eq] [--max 18] [--seeds 7,13]
               [--chirp BIN] [--work DIR] [--ref REF.wav] [--sections FILE]

For every candidate (the tracks' current patch first): the patch's NAME is swapped on every listed track (its params
kept); the master's automation lanes whose names start with a --zero prefix and end in a digit are flattened; a
default-seed render is fitted with sectioneq.py (--prefix = --refit, --max); the fitted lanes are written back and the
song is scored (likeness.py sections) on each --seeds seed. Prints one line per candidate; candidate songs stay in
--work (default /tmp/lt/patchtest-SONG). A YAML song with a one-line JSON `master:` (the songride/sectioneq form).
Results: Daydreaming piano 70.7 vs piano-additive 68.7 / tape-piano 63.6; Flim epiano 60.4 vs rhodes 59.2 /
dx-epiano 59.1 / toy-piano 57.9 — the incumbents won, but now fairly.
"""
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~/.config/chirp")


def sh(cmd, out=None):
    with open(out, "w") if out else open(os.devnull, "w") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, cwd=HOME, check=False)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    song, tracks, cands = a[0], a[1].split(","), a[2].split(",")
    sid = os.path.splitext(os.path.basename(song))[0]
    zero = opt("--zero", "eq,rq").split(","); refit = opt("--refit", "eq"); mx = opt("--max", "18")
    seeds = [int(x) for x in opt("--seeds", "7,13").split(",")]
    chirp = opt("--chirp", "/tmp/lt/chirp-two-a931418"); work = opt("--work", f"/tmp/lt/patchtest-{sid}")
    ref = opt("--ref", f"ref/{sid}.wav"); secs = opt("--sections", f"tools/{sid}-sections.txt")
    os.makedirs(work, exist_ok=True)
    base = open(os.path.join(HOME, song) if not os.path.isabs(song) else song).read()
    pat = lambda t: re.compile(r'(\{name: "?' + re.escape(t) + r'"?, patch: "?)([A-Za-z0-9_.-]+)')
    cur = None
    for t in tracks:
        m = pat(t).search(base)
        if not m:
            sys.exit(f"no track {t}")
        cur = cur or m.group(2)
    cands = [cur] + [c for c in cands if c != cur]
    secs_arg = open(os.path.join(HOME, secs)).read().split()
    for c in cands:
        s = base
        for t in tracks:
            s = pat(t).sub(lambda m: m.group(1) + c, s, count=1)
        m = re.search(r"^master: (\{.*\})$", s, re.M)
        mj = json.loads(m.group(1))
        for k in list(mj.get("auto", {})):
            if any(re.fullmatch(re.escape(z) + r"\d+", k) for z in zero):
                mj["auto"][k] = {"points": [["0s", 0.0]]}
        s0 = s[:m.start(1)] + json.dumps(mj) + s[m.end(1):]
        y0, w0 = f"{work}/{c}-0.yaml", f"{work}/{c}-0.wav"
        open(y0, "w").write(s0)
        sh(["nice", "-n", "15", chirp, "render", "-f", y0, "-o", w0])
        sh(["nice", "-n", "10", "python3", "tools/sectioneq.py", ref, w0, secs, "--max", mx, "--prefix", refit], out=f"{work}/{c}-eq.txt")
        os.path.exists(w0) and os.remove(w0)
        t = open(f"{work}/{c}-eq.txt").read()
        fit = json.loads(t[t.index("{"):])
        m = re.search(r"^master: (\{.*\})$", s0, re.M)
        mj = json.loads(m.group(1))
        mj["auto"].update(fit.get("auto", {}))
        y1 = f"{work}/{c}.yaml"
        open(y1, "w").write(s0[:m.start(1)] + json.dumps(mj) + s0[m.end(1):])
        tot = []
        for sd in seeds:
            w = f"{work}/{c}-s{sd}.wav"
            sh(["nice", "-n", "15", chirp, "render", "-f", y1, "--seed", str(sd), "-o", w])
            r = subprocess.run(["nice", "-n", "10", "python3", "tools/likeness.py", "sections", ref, w] + secs_arg,
                               capture_output=True, text=True, cwd=HOME)
            os.path.exists(w) and os.remove(w)
            tot.append(json.loads(r.stdout)["total"])
        tag = " (control)" if c == cur else ""
        print(f"{c:20s}{tag:10s} refit held-out {'/'.join(map(str, seeds))}: " + " ".join(f"{x:.2f}" for x in tot)
              + f"  mean {sum(tot) / len(tot):.2f}  → {y1}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
