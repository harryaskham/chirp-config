#!/usr/bin/env python3
"""drumtune: per-piece drum tuning against the record (chirper-two, obZen chroma specialist).

  drumtune.py SONG.yaml REF_DRUM_STEM.wav OUR_DRUM_SOLO.wav [--seed 0] [--lo 60 --hi 400] [--min-hits 20]

For every drum voice group (programme name + nominal Hz) in the song's planned IR, averages the power spectrum
10-110 ms after each onset in the record's drum stem and in OUR drum solo (same onsets: our clock), lists each
side's prominent peaks, and proposes the nominal pitch that would move our strongest in-range peak onto the
record's: nominal * record_peak / our_peak. The proposal is evidence for an A/B, not a tuning truth: stems bleed
bass/guitar (a record peak that follows the riff's root from section to section is bleed), simultaneous pieces
share windows, and a peak can be a membrane mode rather than the fundamental. Read the per-hit argmax agreement
before trusting it. Never feed reference audio to the synth.
"""
import argparse
import collections
import json
import os
import subprocess as S
import sys

import numpy as np
from scipy.signal import find_peaks

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # ~/.config/chirp (promoted from ref/evidence/chirper-two)
sys.path.insert(0, os.path.join(CFG, "tools"))
import likeness as L  # noqa: E402

PIN = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "groove-pin")).read().strip()
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nm(f):
    m = 12 * np.log2(f / 440) + 69
    r = int(round(m))
    return f"{N[r % 12]}{r // 12 - 1}{int(round(100 * (m - r))):+d}c"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song")
    ap.add_argument("ref_stem")
    ap.add_argument("our_solo")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--lo", type=float, default=60)
    ap.add_argument("--hi", type=float, default=400)
    ap.add_argument("--min-hits", type=int, default=20)
    ap.add_argument("--json")
    a = ap.parse_args()
    ir = json.loads(S.run([PIN, "plan", "-f", a.song, "--seed", str(a.seed), "--ir", "--json"], capture_output=True,
                          text=True, check=True, cwd=CFG).stdout)["data"]["ir"]
    rate, pn = ir["rate"], [p["name"] for p in ir["programs"]]
    groups = collections.defaultdict(list)
    for v in ir["voices"]:
        name = pn[v["program"]]
        if "kit" in name or "tom" in name or "hat" in name:
            groups[(name, round(v["hz"], 1))].append(v["start"] / rate)
    R, OURS = L.load(a.ref_stem).mean(1), L.load(a.our_solo).mean(1)
    n = 8192
    f = np.fft.rfftfreq(n, 1 / L.SR)
    m = (f >= a.lo) & (f <= a.hi)
    w = np.hanning(4800)

    def spectra(x, ts):
        out = []
        for t in ts:
            i = int((t + 0.01) * L.SR)
            seg = x[i:i + 4800]
            if len(seg) == 4800:
                out.append(np.abs(np.fft.rfft(seg * w, n)) ** 2)
        return out

    def peaks(S_):
        A = np.mean(S_, 0)
        db = 10 * np.log10(A[m] + 1e-30)
        pi, _ = find_peaks(db, prominence=2)
        top = pi[np.argsort(-db[pi])][:5]
        return [(float(f[m][i]), round(float(db[i] - db.max()), 1)) for i in top]

    rows = []
    for (name, hz), ts in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(ts) < a.min_hits:
            continue
        rs, os_ = spectra(R, ts), spectra(OURS, ts)
        rp, op = peaks(rs), peaks(os_)
        agree = collections.Counter(nm(f[m][np.argmax(s[m])]).rstrip("c").split("+")[0].split("-")[0] for s in rs)
        row = {"piece": name, "nominal_hz": hz, "hits": len(ts), "span": [round(min(ts), 1), round(max(ts), 1)],
               "record_peaks": [(round(p, 1), nm(p), d) for p, d in rp], "our_peaks": [(round(p, 1), nm(p), d) for p, d in op],
               "record_hit_argmax": agree.most_common(4)}
        if rp and op:
            row["proposal_nominal_hz"] = round(hz * rp[0][0] / op[0][0], 1)
        rows.append(row)
        print(f"{name}@{hz} n={len(ts)} {row['span'][0]}-{row['span'][1]}s\n  REF " +
              " ".join(f"{p}({q},{d})" for p, q, d in row["record_peaks"]) + f"  argmax {row['record_hit_argmax']}\n  OUR " +
              " ".join(f"{p}({q},{d})" for p, q, d in row["our_peaks"]) +
              (f"\n  -> nominal {hz} x {rp[0][0]:.1f}/{op[0][0]:.1f} = {row['proposal_nominal_hz']} Hz"
               " (strongest-to-strongest; check modes/bleed)" if "proposal_nominal_hz" in row else ""))
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
