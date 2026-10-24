#!/usr/bin/env python3
"""gainsweep: the per-part gain sweep (chirper-zero's recipe step 3; tab-imported parts are never level-calibrated):
every part (or group) at +-DB on the climb's own metric over seeds, then optionally follow the winners.

  gainsweep.py SONG [--db 4] [--seeds 0,11] [--tracks 'kit:kick+snare+hat,bass,lead'] [--skip a,b] [-j 2]
               [--follow [--min 0.2] [--steps 3] -o OUT] [--id ID --ref R --sections S] [--json]

Groups default to every track on its own (--tracks names groups `name:trk+trk` or single tracks; --skip leaves tracks
out). The metric is the climb's (climbs.json `metric`: its reference and sections file, rendered with the adopted
groove pin via tools/seedscore.py); every candidate is the mean over --seeds and is reported as a delta to the base.
--follow applies the winners (mean delta >= --min) best first onto the running song, each kept only if it still
gains there, and extends a kept winner by further +-DB steps while it keeps gaining (at most --steps); -o writes
the result. Gains keep their form: "XdB" strings and {value, mod} lanes shift in dB; linear numbers (the engine reads a
bare number as a multiplier) become dB strings. Track gains of 0 / -inf are left alone.
Results so far: Pulk/Pull +1.5 (organ -8, e-piano +6, lead -8), Knives Out +2.0 (hats +12, snare +3, kick -3),
Let Down +3.6, Karma Police +1.7..+5 per part; Hunting Bears and Like Spinning Plates were already at their optimum.
"""
import argparse
import copy
import json
import math
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import songfmt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def gain_db(g):
    """A track gain as dB (None: absent = 0 dB; -inf for silence); raises on forms it can't shift."""
    if g is None:
        return 0.0
    if isinstance(g, dict):
        return gain_db(g.get("value"))
    if isinstance(g, (int, float)):
        return 20 * math.log10(g) if g > 0 else -math.inf
    s = str(g).strip().lower().replace(" ", "")
    if s in ("-inf", "-infdb"):
        return -math.inf
    m = re.fullmatch(r"([-+]?[0-9.]+)(db|%)?", s)
    if not m:
        raise ValueError(f"gain {g!r}")
    v, unit = float(m.group(1)), m.group(2)
    if unit == "db":
        return v
    v = v / 100 if unit == "%" else v
    return 20 * math.log10(v) if v > 0 else -math.inf


def shifted(g, d):
    """The gain G moved by D dB, keeping a {value, mod} lane's shape."""
    if isinstance(g, dict):
        return {**g, "value": shifted(g.get("value"), d)}
    return f"{gain_db(g) + d:+.1f}dB"


def apply(song, moves):
    """A copy of SONG with each {track: dB} moved."""
    s = copy.deepcopy(song)
    for t in s.get("tracks", []):
        if t.get("name") in moves:
            t["gain"] = shifted(t.get("gain"), moves[t["name"]])
    return s


def groups_of(song, spec, skip):
    names = [t.get("name") for t in song.get("tracks", []) if t.get("name")]
    live = {t["name"] for t in song.get("tracks", []) if t.get("name") and math.isfinite(gain_db(t.get("gain")))}
    if spec:
        out = []
        for g in spec.split(","):
            label, _, trks = g.partition(":")
            members = (trks or label).split("+")
            bad = [m for m in members if m not in names]
            if bad:
                raise SystemExit(f"gainsweep: no track(s) {', '.join(bad)} (tracks: {', '.join(names)})")
            out.append((label, members))
        return out
    return [(n, [n]) for n in names if n in live and n not in skip]


def metric_paths(cid):
    """(ref, sections) from the climb's metric (climbs.json), else ref/ID.wav and tools/ID-sections.txt."""
    ref, secs = f"ref/{cid}.wav", f"tools/{cid}-sections.txt"
    try:
        c = next(c for c in json.load(open(os.path.join(ROOT, "climbs.json")))["climbs"] if c["id"] == cid)
        m = re.search(r"sections\s+(\S+)\s+OUT\.wav\s+\$\(cat\s+(\S+)\)", c.get("metric") or "")
        if m:
            ref, secs = m.group(1), m.group(2)
    except (OSError, StopIteration, ValueError):
        pass
    return os.path.join(ROOT, ref), os.path.join(ROOT, secs)


class Scorer:
    """Scores song dicts on the climb's metric (seed means), writing each variant beside the song (relative paths
    in it keep resolving) and removing it afterwards."""

    def __init__(self, song_path, ref, sections, seeds, score_fn=None):
        self.path, self.ref, self.sections, self.seeds = os.path.abspath(song_path), ref, sections, seeds
        self.n = 0
        if score_fn is None:
            import seedscore
            score_fn = lambda p: seedscore.score(p, seeds, ref, sections)  # noqa: E731
        self.fn = score_fn

    def __call__(self, song, label):
        self.n += 1
        d, base = os.path.dirname(self.path), os.path.basename(self.path)
        stem, ext = os.path.splitext(base)
        tmp = os.path.join(d, f".gainsweep-{os.getpid()}-{self.n}-{re.sub(r'[^A-Za-z0-9]+', '_', label)}{ext}")
        with open(tmp, "w") as f:
            f.write(json.dumps(song, indent=1) + "\n" if ext == ".json" else songfmt.dump_yaml(song))
        try:
            return self.fn(tmp)
        finally:
            os.unlink(tmp)


def sweep(song, groups, db, scorer, jobs=2):
    """{label: {'+': delta, '-': delta, 'base': mean}} for each group at +-db."""
    base = scorer(song, "base")["mean"]
    jobs_list = [(label, sign, members) for label, members in groups for sign in (1, -1)]

    def one(job):
        label, sign, members = job
        r = scorer(apply(song, {m: sign * db for m in members}), f"{label}{'+' if sign > 0 else '-'}")
        return label, sign, round(r["mean"] - base, 2)

    out = {label: {"base": base} for label, _ in groups}
    with ThreadPoolExecutor(max(1, jobs)) as ex:
        for label, sign, d in ex.map(one, jobs_list):
            out[label]["+" if sign > 0 else "-"] = d
    return base, out


def follow(song, groups, res, db, scorer, min_gain=0.2, steps=3):
    """Apply winners best first; keep each only if it gains on the running song, then extend it while it gains."""
    members = dict(groups)
    ranked = sorted(((max(r["+"], r["-"]), label, 1 if r["+"] >= r["-"] else -1) for label, r in res.items()),
                    reverse=True)
    cur, cur_score = song, scorer(song, "follow-base")["mean"]
    kept = []
    for gain, label, sign in ranked:
        if gain < min_gain:
            break
        total = 0.0
        for _ in range(max(1, steps)):
            cand = apply(cur, {m: sign * db for m in members[label]})
            sc = scorer(cand, f"follow-{label}")["mean"]
            if sc - cur_score < min_gain:
                break
            cur, cur_score, total = cand, sc, total + sign * db
        if total:
            kept.append((label, total, cur_score))
    return cur, cur_score, kept


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song")
    ap.add_argument("--db", type=float, default=4.0)
    ap.add_argument("--seeds", default="0,11")
    ap.add_argument("--tracks")
    ap.add_argument("--skip", default="")
    ap.add_argument("-j", type=int, default=2)
    ap.add_argument("--follow", action="store_true")
    ap.add_argument("--min", type=float, default=0.2)
    ap.add_argument("--steps", type=int, default=3)
    ap.add_argument("-o")
    ap.add_argument("--id")
    ap.add_argument("--ref")
    ap.add_argument("--sections")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.follow and not a.o:
        ap.error("--follow writes its result: give -o OUT")
    cid = a.id or os.path.splitext(os.path.basename(a.song))[0]
    ref, secs = metric_paths(cid)
    ref, secs = a.ref or ref, a.sections or secs
    for p in (ref, secs):
        if not os.path.exists(p):
            raise SystemExit(f"gainsweep: missing {p} (give --ref/--sections)")
    song = songfmt.load(a.song)
    groups = groups_of(song, a.tracks, {x for x in a.skip.split(",") if x})
    scorer = Scorer(a.song, ref, secs, tuple(int(x) for x in a.seeds.split(",")))
    base, res = sweep(song, groups, a.db, scorer, a.j)
    report = {"base": base, "db": a.db, "seeds": a.seeds, "parts": {k: {"+": v["+"], "-": v["-"]} for k, v in res.items()}}
    if not a.json:
        print(f"gainsweep {cid}: base {base:.2f} (seeds {a.seeds}); each part at +-{a.db:g} dB, delta to base:")
        for label, r in sorted(res.items(), key=lambda kv: -max(kv[1]["+"], kv[1]["-"])):
            best = max(r["+"], r["-"])
            mark = f"  <- {'+' if r['+'] >= r['-'] else '-'}{a.db:g} dB" if best >= a.min else ""
            print(f"  {label:24s} +{a.db:g}: {r['+']:+6.2f}   -{a.db:g}: {r['-']:+6.2f}{mark}")
    if a.follow:
        cur, score, kept = follow(song, groups, res, a.db, scorer, a.min, a.steps)
        out = a.o
        with open(out, "w") as f:
            f.write(json.dumps(cur, indent=1) + "\n" if out.endswith(".json") else songfmt.dump_yaml(cur))
        report.update({"followed": [{"part": k, "db": d, "score": s} for k, d, s in kept], "final": score, "out": out})
        if not a.json:
            moves = ", ".join(f"{k} {d:+g} dB" for k, d, _ in kept) or "none kept"
            print(f"follow: {moves}; {base:.2f} -> {score:.2f} ({score - base:+.2f}) -> {out} "
                  f"(check every seed, then ride/width: the refit resets fades)")
    if a.json:
        print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
