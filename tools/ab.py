#!/usr/bin/env python3
"""ab.py: chirper-two's RNG-safe patch-parameter A/B harness for obZen chroma candidates.

  ab.py BASE.yaml OUTDIR TAG 'TRACK<TAB>OLD<TAB>NEW' [...] --sections FILE --ref REF.wav [--seeds 0,11]
        [--allow-field hz] [--expect-programs]

Applies exact text replacements INSIDE one track's line of the song (the track's `- {name: "TRACK", ...}` line
only), plans base and candidate IR at every seed and refuses unless voice count, order, start, release, end,
seed, vel, key and every non-allowed field are identical (only --allow-field fields may differ). Then renders
each seed (nice 15, RAYON 1, load <= 48) and scores with likeness sections --strict-coverage.
Base renders/scores are cached per seed in OUTDIR/base-s{seed}.*.
"""
import argparse
import json
import os
import re
import subprocess as S
import sys
import time

PIN = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "groove-pin")).read().strip()
CFG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # ~/.config/chirp (promoted from ref/evidence/chirper-two)


def gate():
    while os.getloadavg()[0] > 48:
        time.sleep(30)


def plan(song, seed):
    p = S.run([PIN, "plan", "-f", song, "--seed", str(seed), "--ir", "--json"], capture_output=True, text=True,
              check=True, cwd=CFG)
    return json.loads(p.stdout)["data"]["ir"]


def render(song, seed, out):
    if os.path.exists(out):
        return
    gate()
    env = dict(os.environ, RAYON_NUM_THREADS="1")
    tmp = f"{out[:-4]}.tmp{os.getpid()}.wav"   # atomic: parallel batches may share a cached base render
    with open(out + ".log", "w") as f:
        S.run(["nice", "-n", "15", PIN, "render", "-f", song, "--seed", str(seed), "-o", tmp], stdout=f,
              stderr=S.STDOUT, check=True, cwd=CFG, env=env)
    os.replace(tmp, out)


def score(ref, wav, sections, out):
    if os.path.exists(out):
        return json.load(open(out))
    gate()
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    env.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    p = S.run(["nice", "-n", "10", "python3", "tools/likeness.py", "sections", ref, wav,
               *open(sections).read().split(), "--strict-coverage"], capture_output=True, text=True, check=True,
              cwd=CFG, env=env)
    tmp = f"{out}.tmp{os.getpid()}"
    open(tmp, "w").write(p.stdout)
    os.replace(tmp, out)
    return json.loads(p.stdout)


def is_track_line(line, track):
    """A song file's flow-mapping line for TRACK, whatever its key order (rngsafe and drumtrans write
    {patch: ..., name: ...}); the original matched only lines starting '- {name: ...'."""
    return line.lstrip().startswith("- {") and re.search(r'(?:\{|, )name: "' + re.escape(track) + '"', line) is not None


def edit(text, track, old, new):
    lines = text.split("\n")
    hits = [i for i, ln in enumerate(lines) if is_track_line(ln, track)]
    assert len(hits) == 1, (track, hits)
    i = hits[0]
    assert lines[i].count(old) == 1, (track, old, lines[i].count(old))
    lines[i] = lines[i].replace(old, new)
    return "\n".join(lines)


def ir_diff(a, b, allow, voices=()):
    """Field changes per voice. ALLOW fields may change on any voice; VOICES ('program@hz' of the BASE voice)
    may additionally change hz/key/seed (a retuned piece legitimately rekeys its own events, nothing else).
    Programmes may differ only in name (a patch-variant label)."""
    va, vb = a["voices"], b["voices"]
    assert len(va) == len(vb), ("voice count", len(va), len(vb))
    pa = [p["name"] for p in a["programs"]]
    changed, bad = {}, {}
    for x, y in zip(va, vb):
        own = f"{pa[x['program']]}@{round(x['hz'], 1)}" in voices
        for k in x:
            if x[k] != y.get(k):
                changed[k] = changed.get(k, 0) + 1
                if k not in allow and not (own and k in ("hz", "key", "seed")):
                    bad[k] = bad.get(k, 0) + 1
    for p, q in zip(a["programs"], b["programs"]):
        extra = [k for k in set(p) | set(q) if k != "name" and p.get(k) != q.get(k)]
        if extra and "programs" not in allow:
            bad["program:" + p["name"]] = extra
    if len(a["programs"]) != len(b["programs"]):
        bad["program_count"] = (len(a["programs"]), len(b["programs"]))
    return changed, bad


def summ(sc):
    w = [s["end"] - s["start"] for s in sc["sections"]]
    ch = sum(wi * s["chroma"] for wi, s in zip(w, sc["sections"])) / sum(w)
    return {"total": sc["total"], "total_raw": round(sc["total_raw"], 4), "chroma": round(ch, 3),
            "sections_total": [s["total"] for s in sc["sections"]], "sections_chroma": [s["chroma"] for s in sc["sections"]]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("outdir")
    ap.add_argument("tag")
    ap.add_argument("edits", nargs="+")
    ap.add_argument("--sections", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--seeds", default="0,11")
    ap.add_argument("--allow-field", action="append", default=[])
    ap.add_argument("--allow-voices", action="append", default=[], help="BASEPROGRAM@HZ voices that may rekey")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    text = open(a.base).read()
    for e in a.edits:
        track, old, new = e.split("\t")
        text = edit(text, track, old, new)
    cand = os.path.join(a.outdir, f"{a.tag}.yaml")
    open(cand, "w").write(text)
    seeds = [int(s) for s in a.seeds.split(",")]
    res = {"tag": a.tag, "edits": a.edits, "seeds": {}}
    for s in seeds:
        bi, ci = plan(a.base, s), plan(cand, s)
        changed, bad = ir_diff(bi, ci, set(a.allow_field), set(a.allow_voices))
        progs_same = bi["programs"] == ci["programs"]
        res.setdefault("ir", {})[str(s)] = {"changed_fields": changed, "programs_identical": progs_same}
        if bad:
            res["refused"] = bad
            print(json.dumps(res, indent=1))
            sys.exit(f"IR guard refused: non-allowed voice fields changed {bad}")
    for s in seeds:
        bw, cw = os.path.join(a.outdir, f"base-s{s}.wav"), os.path.join(a.outdir, f"{a.tag}-s{s}.wav")
        render(a.base, s, bw)
        render(cand, s, cw)
        b = summ(score(a.ref, bw, a.sections, bw[:-4] + ".score.json"))
        c = summ(score(a.ref, cw, a.sections, cw[:-4] + ".score.json"))
        res["seeds"][str(s)] = {"base": b, "cand": c, "d_total": round(c["total"] - b["total"], 3),
                                "d_raw": round(c["total_raw"] - b["total_raw"], 4), "d_chroma": round(c["chroma"] - b["chroma"], 3)}
    json.dump(res, open(os.path.join(a.outdir, f"{a.tag}.result.json"), "w"), indent=1)
    print(a.tag, " ".join(f"s{s}: total {r['base']['total']}->{r['cand']['total']} ({r['d_total']:+.3f}, raw {r['d_raw']:+.4f}) "
                          f"chroma {r['base']['chroma']:.2f}->{r['cand']['chroma']:.2f} ({r['d_chroma']:+.2f})"
                          for s, r in res["seeds"].items()), "| IR changed:", res["ir"])


if __name__ == "__main__":
    main()
