#!/usr/bin/env python3
"""chromadiag: likeness-exact chroma diagnosis (chirper-two, obZen chroma specialist).

Recomputes likeness.sections' chroma term EXACTLY (same 16384 STFT, 100-4000 Hz, per-frame normalisation,
0.5 s windows, centred cosine, per-section crop) from RAW per-pitch-class power, so the raw power can be
split before normalising:

  * by REGISTER (sub-bands of 100-4000 Hz), and
  * by SOURCE (our solo renders; the record's separated stems),

and then asks ORACLE questions: "if our pitch content in this register / this source matched the record's
(keeping our own level there), what would the section chroma be?". The gain names where the chroma points
are, before anyone edits notes. Oracles are diagnostics; reference audio is never synthesis input.

  chromadiag.py ID REF.wav OURS.wav --sections FILE [--src NAME=OUR.wav:REFSTEM.wav ...] [--json OUT]

Content oracle (default): our per-frame power in the part is kept, its 12-bin distribution replaced by the
record's (the part's pitch content, not its level). Share oracle: the part's per-frame share of 100-4000 Hz
power set to the record's, keeping our pitch distribution (balance, not notes).
Source power adds approximately (independent sources; cross terms ignored): the residual
(mix - sum of sources) is reported so that approximation can be judged.
"""
import argparse
import json
import os
import sys

import numpy as np
from scipy import signal

ROOT = os.path.dirname(os.path.abspath(__file__))
for up in range(5):
    cand = os.path.join(ROOT, *[".."] * up, "tools")
    if os.path.exists(os.path.join(cand, "likeness.py")):
        sys.path.insert(0, os.path.abspath(cand))
        break
import likeness as L  # noqa: E402

SR, HOP, NFFT = L.SR, L.HOP, L.NFFT
FPS = L.FPS
REGISTERS = [(100, 200), (200, 400), (400, 800), (800, 1600), (1600, 4000)]
NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")


def mono(stereo):
    return stereo.mean(axis=1)


def n_frames(nsamp):
    return 1 + (nsamp - NFFT) // HOP if nsamp >= NFFT else 0


def raw_pc(x, regs=None):
    """Raw per-pitch-class power on likeness's coarse chroma grid: {(lo,hi): array(12, frames)}; the
    full 100-4000 band is the sum over REGISTERS (they tile it exactly, edges belong to one band)."""
    regs = regs or REGISTERS
    f2, _, Z2 = signal.stft(x, SR, nperseg=16384, noverlap=16384 - 4 * HOP, boundary=None, padded=False)
    m2 = np.abs(Z2) ** 2
    out = {}
    for i, (lo, hi) in enumerate(regs):
        last = i == len(regs) - 1
        sel = (f2 >= lo) & ((f2 <= hi) if last else (f2 < hi))
        pcs = np.round(12 * np.log2(f2[sel] / 440.0) + 9).astype(int) % 12
        mm = m2[sel]
        out[(lo, hi)] = np.stack([mm[pcs == pc].sum(0) for pc in range(12)])
    return out


def to_hop(ch, n):
    """likeness's mapping of the coarse chroma grid onto the hop grid (repeat 4, edge pad)."""
    ch = np.repeat(ch, 4, axis=1)
    pad = n - ch.shape[1]
    if pad > 0:
        return np.pad(ch, ((0, 0), (max(0, pad // 2), max(0, pad - pad // 2))), mode="edge")[:, :n]
    return ch[:, :n]


def norm(ch):
    return ch / (ch.sum(0, keepdims=True) + 1e-9)


def windows(chn, n):
    w2 = int(FPS / 2)
    return [chn[:, i:i + w2].mean(1) for i in range(0, n - w2, w2)]


def cosc(a, b):
    return L._cos(a - 1 / 12, b - 1 / 12)


def score(Rraw, Craw, n):
    """Section chroma (0-100, likeness's max(0, mean cos)) and the per-window cosines."""
    rw, cw = windows(norm(to_hop(Rraw, n)), n), windows(norm(to_hop(Craw, n)), n)
    cs = [cosc(a, b) for a, b in zip(rw, cw)]
    return 100 * max(0, float(np.mean(cs))), cs, rw, cw


def total(d):
    return sum(d.values())


def content_oracle(ours, theirs):
    """OURS' per-frame power, THEIRS' per-frame pitch distribution."""
    return norm(theirs) * ours.sum(0, keepdims=True)


def load_seg(path, a, b, quantise):
    x = L.load(path)
    seg = x[int(a * SR):int(b * SR)]
    if quantise:  # likeness writes the candidate crop as 16-bit WAV
        seg = (np.clip(seg, -1, 1) * 32767).astype(np.int16).astype(np.float32) / 32767
    return seg


def analyse(ref, ours, bounds, srcs):
    R_full, C_full = L.load(ref), L.load(ours)
    S = {k: (L.load(o), L.load(r)) for k, (o, r) in srcs.items()}
    rows = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        rs = R_full[int(a * SR):int(b * SR)]
        cs = C_full[int(a * SR):int(b * SR)]
        cs = (np.clip(cs, -1, 1) * 32767).astype(np.int16).astype(np.float32) / 32767
        n = min(n_frames(len(rs)), n_frames(len(cs)))
        Rr, Cr = raw_pc(mono(rs)), raw_pc(mono(cs))
        Rt, Ct = total(Rr), total(Cr)
        base, cos_w, rw, cw = score(Rt, Ct, n)
        row = {"start": a, "end": b, "chroma": round(base, 2), "windows": len(cos_w),
               "neg_windows": int(sum(c < 0 for c in cos_w)),
               "ref_top": [NAMES[i] for i in np.argsort(-np.mean(rw, 0))[:4]],
               "our_top": [NAMES[i] for i in np.argsort(-np.mean(cw, 0))[:4]]}
        # register oracles
        reg = {}
        for k in REGISTERS:
            c2 = Ct - Cr[k] + content_oracle(Cr[k], Rr[k])
            share = Cr[k].sum(0, keepdims=True) / (Ct.sum(0, keepdims=True) + 1e-12)
            rshare = Rr[k].sum(0, keepdims=True) / (Rt.sum(0, keepdims=True) + 1e-12)
            c3 = Ct - Cr[k] + Cr[k] / np.maximum(share, 1e-12) * rshare  # share oracle (frame-wise)
            reg[f"{k[0]}-{k[1]}"] = {"content": round(score(Rt, c2, n)[0] - base, 2),
                                     "share": round(score(Rt, c3, n)[0] - base, 2),
                                     "our_share": round(float(np.median(share)), 3),
                                     "ref_share": round(float(np.median(rshare)), 3)}
        row["register_oracle"] = reg
        # source oracles
        if S:
            src_ours, src_ref = {}, {}
            for k, (o, r) in S.items():
                os_ = o[int(a * SR):int(b * SR)]
                rs_ = r[int(a * SR):int(b * SR)]
                src_ours[k] = total(raw_pc(mono(os_)))[:, :Ct.shape[1]]
                src_ref[k] = total(raw_pc(mono(rs_)))[:, :Rt.shape[1]]
            sumo, sumr = sum(src_ours.values()), sum(src_ref.values())
            row["source_residual_db"] = {
                "ours": round(float(10 * np.log10(np.abs(Ct - sumo).sum() / Ct.sum())), 1),
                "ref": round(float(10 * np.log10(np.abs(Rt - sumr).sum() / Rt.sum())), 1)}
            so = {}
            for k in S:
                c2 = Ct - src_ours[k] + content_oracle(src_ours[k], src_ref[k])
                oshare = src_ours[k].sum() / Ct.sum()
                rshare = src_ref[k].sum() / Rt.sum()
                c3 = Ct - src_ours[k] + src_ours[k] * (rshare / max(oshare, 1e-12)) * (Ct.sum() / Ct.sum())
                so[k] = {"content": round(score(Rt, c2, n)[0] - base, 2),
                         "share": round(score(Rt, c3, n)[0] - base, 2),
                         "our_share": round(float(oshare), 3), "ref_share": round(float(rshare), 3),
                         "solo_vs_ref_stem": round(score(src_ref[k], src_ours[k], n)[0], 2),
                         "ref_stem_vs_ref_mix": round(score(Rt, src_ref[k], n)[0], 2),
                         "our_solo_vs_ref_mix": round(score(Rt, src_ours[k], n)[0], 2)}
            row["source_oracle"] = so
        rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref")
    ap.add_argument("ours")
    ap.add_argument("--sections", required=True)
    ap.add_argument("--src", action="append", default=[], help="NAME=OUR_SOLO.wav:REF_STEM.wav")
    ap.add_argument("--json")
    a = ap.parse_args()
    bounds = [float(v) for v in open(a.sections).read().replace(",", " ").split()]
    srcs = {}
    for s in a.src:
        k, v = s.split("=", 1)
        o, r = v.split(":", 1)
        srcs[k] = (o, r)
    rows = analyse(a.ref, a.ours, bounds, srcs)
    w = np.array([r["end"] - r["start"] for r in rows])
    summ = {"chroma": round(float(np.dot(w, [r["chroma"] for r in rows]) / w.sum()), 3)}
    for key in ("register_oracle", "source_oracle"):
        if key in rows[0]:
            summ[key] = {k: {m: round(float(np.dot(w, [r[key][k][m] for r in rows]) / w.sum()), 2)
                             for m in ("content", "share")} for k in rows[0][key]}
    out = {"summary": summ, "sections": rows}
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    print(json.dumps(summ, indent=1))
    for r in rows:
        print(f"{r['start']:7.2f}-{r['end']:7.2f} chroma {r['chroma']:5.1f} neg {r['neg_windows']:2d}/{r['windows']:2d} "
              f"ref {','.join(r['ref_top'])} ours {','.join(r['our_top'])} | reg "
              + " ".join(f"{k}:{v['content']:+.1f}/{v['share']:+.1f}" for k, v in r["register_oracle"].items())
              + ((" | src " + " ".join(f"{k}:{v['content']:+.1f}/{v['share']:+.1f}" for k, v in r["source_oracle"].items()))
                 if "source_oracle" in r else ""))


if __name__ == "__main__":
    main()
