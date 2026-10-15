#!/usr/bin/env python3
"""Per-block tempo search for live references — no rendering: the tab already says when every drum hit falls, so
for any tempo map the predicted hit times can be scored directly against the record's drum-stem onsets.

Greedy, in bar order from --from-bar: for each block of --block bars, try bpm = previous ± --range in --step for
the block and everything after it, score the predicted hits of this block and the next --lookahead blocks against
the reference onset envelope (spectral flux of the drum stem, max-filtered ±--tol ms so near misses count, z-scored),
keep the best and fix the block. Kick/snare hits weigh 1, hats/cymbals --hat-weight (0.3: sixteenth hats alone
would lock onto a grid one note off). Writes the map with per-bar bpm overrides; the offset and bars before
--from-bar are kept.

  temposearch.py MAP.json SONG.yaml TRACK STEM.wav -o OUT.json [--from-bar 5] [--block 4] [--range 3] [--step 0.05]
                 [--lookahead 1] [--tol 20] [--hat-weight 0.3]

SONG.yaml is the song tab2song makes from MAP.json (its TRACK score gives the hits in song beats). 4/4 assumed.
Prints per block the chosen bpm and its score next to the input map's. Measure the result with likeness.

CAVEAT (Come Down, Tiny Desk): the hit score rose -0.10 -> +1.13 but likeness did not (37.6 vs 38.0): with a
repeating groove the hits can lock onto an alias of the record's onsets. Prefer dtwgrid.py --feature metric
--around-zero --window 0.25 --median 3 (chirper-three: 38.0 -> 47.3 there); use this only as a starting grid."""
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402

KICKSNARE = {"k", "s", "rs", "ss", "sc", "so", "se", "g", "rc", "sw", "sl"}


def expand(tokens):
    """Score tokens with [ … ]xN groups (nesting allowed) → flat token list."""
    out, stack = [], [[]]
    for t in tokens:
        if t == "|":
            continue
        if t.startswith("["):
            stack.append([]); t = t[1:]
            if not t:
                continue
        m = re.match(r"^(.*?)\](?:x(\d+))?$", t)
        if m:
            if m.group(1):
                stack[-1].append(m.group(1))
            grp = stack.pop() * int(m.group(2) or 1); stack[-1].extend(grp)
        else:
            stack[-1].append(t)
    return stack[0]


def hits(song, track):
    y = open(song).read()
    line = next(ln for ln in y.splitlines() if re.search(rf'name: "?{re.escape(track)}"?[,}}]', ln))
    toks = expand(re.search(r'score: "([^"]*)"', line).group(1).split())
    b, out = 0.0, []
    for t in toks:
        m = re.match(r"^([^/]+)/([0-9.]+)b(?:@(\d+))?", t)
        if not m:
            continue
        if m.group(1) not in ("R", "_"):
            pcs = set(m.group(1).split(","))
            w = 1.0 if pcs & KICKSNARE else None
            out.append((b, w, int(m.group(3) or 100)))
        b += float(m.group(2))
    return out


def tempo_of(mp, bars, off_beats):
    """Per-bar bpm list (index 1..bars) from the map's overrides (each holds until the next)."""
    o = {int(k): float(v) for k, v in mp.get("bpm", {}).items()}
    cur, res = o.get(1, 120.0), [None]
    for bar in range(1, bars + 1):
        cur = o.get(bar, cur); res.append(cur)
    return res


def times(bpm, offset, nbars):
    """Start time of each bar 1..nbars+1."""
    t = [None, offset]
    for bar in range(1, nbars + 1):
        t.append(t[-1] + 4 * 60 / bpm[bar])
    return t


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mpath, song, track, stem = a[:4]
    out = opt("-o", "")
    fb, blk, rng, step = opt("--from-bar", 5), opt("--block", 4), opt("--range", 3.0), opt("--step", 0.05)
    look, tol, hw = opt("--lookahead", 1), opt("--tol", 20.0), opt("--hat-weight", 0.3)
    mp = json.load(open(mpath))
    y = open(song).read()
    t0 = json.loads(re.search(r"^tempo: (\[.*\])$", y, re.M).group(1))
    off_beats = round(mp.get("offset", 0) * t0[0]["bpm"] / 60, 4)
    hs = [(b - off_beats, (w if w is not None else hw) * v / 100) for b, w, v in hits(song, track) if b >= off_beats - 1e-6]
    nbars = int(max(b for b, _ in hs) // 4) + 2
    bpm = tempo_of(mp, nbars, off_beats)
    F = L.Feat(L.load(stem)); env = F.onset.astype(float); fps = L.FPS
    k = max(1, int(round(tol / 1000 * fps)))
    env = np.array([env[max(0, i - k):i + k + 1].max() for i in range(len(env))])
    env = (env - env.mean()) / (env.std() + 1e-9)
    hb = np.array([b for b, _ in hs]); hwt = np.array([w for _, w in hs])

    def score(bpmlist, bar_a, bar_b):
        tt = times(bpmlist, mp.get("offset", 0.0), nbars)
        sel = (hb >= (bar_a - 1) * 4) & (hb < (bar_b - 1) * 4)
        if not sel.any():
            return 0.0
        bar = (hb[sel] // 4).astype(int) + 1; frac = hb[sel] - (bar - 1) * 4
        tsec = np.array([tt[b_] for b_ in bar]) + frac * 60 / np.array([bpm_ for bpm_ in (bpmlist[b_] for b_ in bar)])
        idx = np.clip((tsec * fps).astype(int), 0, len(env) - 1)
        return float(np.sum(env[idx] * hwt[sel]) / np.sum(hwt[sel]))

    orig = list(bpm)
    for a0 in range(fb, nbars, blk):
        b0, b1 = a0 + blk, min(nbars, a0 + blk * (1 + look))
        base = bpm[a0]; best = (-1e9, base)
        for cand in np.arange(base - rng, base + rng + 1e-9, step):
            trial = bpm[:a0] + [cand] * (len(bpm) - a0)
            s = score(trial, a0, b1)
            if s > best[0]:
                best = (s, cand)
        for bar in range(a0, len(bpm)):
            bpm[bar] = best[1]
        print(f"bars {a0:3d}-{b0 - 1:3d}: bpm {best[1]:7.2f} score {best[0]:+.3f} (input map {score(orig, a0, b0):+.3f} at {orig[a0]:.2f})")
    over = {str(bar): round(bpm[bar], 4) for bar in range(1, len(bpm)) if bar == 1 or abs(bpm[bar] - bpm[bar - 1]) > 1e-9}
    mp["bpm"] = over
    json.dump(mp, open(out, "w"), indent=1)
    print(f"wrote {out}: {len(over)} tempo changes; whole-song hit score {score(bpm, fb, nbars):+.3f} vs input {score(orig, fb, nbars):+.3f}")


if __name__ == "__main__":
    main(sys.argv[1:])
