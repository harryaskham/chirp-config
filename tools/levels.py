#!/usr/bin/env python3
"""levels.py — clipping and loudness check for rendered songs (Harry, 30 Oct: "do we have a clipping check? are we
clipping anywhere? are our overall levels good").

compscore's master term only checks the sample peak against the album's peak_max, plus rms and crest. The master
limiter caps sample peaks at the song's ceiling (config -1 dBFS), so the risks it cannot see are:
  - inter-sample (true) peaks over 0 dBTP, which clip in a DAC or after lossy encoding;
  - flat-topping: runs of samples pinned at the ceiling (hard clipping, or a limiter working too hard);
  - loudness mismatch across an album (integrated LUFS, ITU-R BS.1770-4 / EBU R128).

  levels.py WAV...                 measure rendered files
  levels.py --album ALBUM_ID       render each composed track of an album at seed 0 with the groove pin, then measure
  levels.py ... --json             machine-readable rows

Columns: sample peak (dBFS), true peak (dBTP, 4x oversampled), integrated loudness (LUFS), max short-term (3 s)
loudness, PLR (true peak - LUFS), % of samples within 0.1 dB of the track's peak, and the longest run of consecutive
samples IDENTICAL to it (within 1e-6; >= 4 means flat-topped: a clamp or hard clip writes the same value again and
again, while a clean 40 Hz sine stays within 0.01 dB of its crest for ~18 samples but repeats no value, wM 30 Oct).
Flags: TP>0 (inter-sample overs), TP>-1 (above the usual streaming ceiling), FLAT (a run of 4+ pinned samples), and
for an album LOUD/QUIET (more than 2 LU from its median).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)


def k_weight(x, sr):
    """BS.1770 K-weighting (pre-filter high shelf + RLB high-pass), coefficients derived for any sample rate."""
    from scipy import signal
    # stage 1: high shelf (+4 dB above ~1.5 kHz)
    f0, g, q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    k = np.tan(np.pi * f0 / sr)
    vh = 10 ** (g / 20)
    vb = vh ** 0.4996667741545416
    a0 = 1 + k / q + k * k
    b1 = [(vh + vb * k / q + k * k) / a0, 2 * (k * k - vh) / a0, (vh - vb * k / q + k * k) / a0]
    a1 = [1, 2 * (k * k - 1) / a0, (1 - k / q + k * k) / a0]
    # stage 2: RLB high-pass (~38 Hz)
    f0, q = 38.13547087602444, 0.5003270373238773
    k = np.tan(np.pi * f0 / sr)
    a0 = 1 + k / q + k * k
    b2 = [1, -2, 1]
    a2 = [1, 2 * (k * k - 1) / a0, (1 - k / q + k * k) / a0]
    return signal.lfilter(b2, a2, signal.lfilter(b1, a1, x, axis=0), axis=0)


def loudness(x, sr):
    """(integrated LUFS, max short-term LUFS) per BS.1770-4: 400 ms blocks, 75% overlap, -70 LUFS absolute gate,
    -10 LU relative gate; short-term is a 3 s window."""
    y = k_weight(x, sr)
    p = (y ** 2).sum(axis=1) if y.ndim > 1 else y ** 2   # channel weights 1.0 for L/R

    def blocks(win, hop):
        n, h = int(win * sr), int(hop * sr)
        if len(p) < n:
            return np.array([p.mean()]) if len(p) else np.array([1e-12])
        c = np.concatenate([[0.0], np.cumsum(p)])
        starts = np.arange(0, len(p) - n + 1, h)
        return (c[starts + n] - c[starts]) / n

    z = blocks(0.4, 0.1)
    lk = -0.691 + 10 * np.log10(z + 1e-20)
    z = z[lk > -70]
    if not len(z):
        return -70.0, -70.0
    rel = -0.691 + 10 * np.log10(z.mean()) - 10
    z = z[-0.691 + 10 * np.log10(z) > rel]
    integ = -0.691 + 10 * np.log10(z.mean())
    st = -0.691 + 10 * np.log10(blocks(3.0, 0.1) + 1e-20)
    return float(integ), float(st.max())


def true_peak(x, over=4, chunk=1 << 20):
    """Max |x| after 4x polyphase oversampling (chunked with overlap so long songs stay in memory)."""
    from scipy import signal
    pad = 64
    best = 0.0
    chans = x.T if x.ndim > 1 else x[None, :]
    for ch in chans:
        for s in range(0, len(ch), chunk):
            a, b = max(0, s - pad), min(len(ch), s + chunk + pad)
            u = signal.resample_poly(ch[a:b].astype(np.float64), over, 1)
            lo, hi = (s - a) * over, (min(len(ch), s + chunk) - a) * over
            best = max(best, float(np.abs(u[lo:hi]).max()))
    return best


def longest_run(mask):
    if not mask.any():
        return 0
    d = np.diff(np.concatenate([[0], mask.astype(np.int8), [0]]))
    return int((np.flatnonzero(d == -1) - np.flatnonzero(d == 1)).max())


def pinned_run(x, peak=None):
    """Longest run of samples identical to the peak (relative 1e-6): the signature of a clamp or hard clipper. A
    tolerance in dB (0.01) also counted the flat crest of clean low bass (40 Hz: ~18 samples at 48 kHz)."""
    a = np.abs(x)
    peak = float(a.max()) if peak is None else peak
    pinned = a >= peak * (1 - 1e-6)
    return max(longest_run(pinned[:, c]) for c in range(x.shape[1])) if x.ndim > 1 else longest_run(pinned)


def measure(path):
    import likeness as L
    x = L.load(path).astype(np.float64)
    sr = L.SR
    a = np.abs(x)
    peak = float(a.max()) or 1e-12
    pdb = 20 * np.log10(peak)
    near = a >= peak * 10 ** (-0.1 / 20)
    run = pinned_run(x, peak)
    tp = 20 * np.log10(true_peak(x) or 1e-12)
    integ, st = loudness(x, sr)
    flags = (["TP>0"] if tp > 0 else ["TP>-1"] if tp > -1 else []) + (["FLAT"] if run >= 4 else [])
    return {"file": path, "dur": round(len(x) / sr, 1), "peak_dbfs": round(pdb, 2), "true_peak_dbtp": round(tp, 2),
            "lufs": round(integ, 1), "st_max_lufs": round(st, 1), "plr": round(tp - integ, 1),
            "near_peak_pct": round(100 * float(near.mean()), 3), "longest_pinned_run": run, "flags": flags}


def render_album(album_id, work):
    import climb as C
    pin = open(os.path.join(ROOT, "tools", "groove-pin")).read().strip()
    reg = C.load()
    out = []
    for c in sorted((c for c in reg["climbs"] if c.get("album") == album_id or c["id"].startswith(album_id + "-")),
                    key=lambda c: int(c["id"].rsplit("t", 1)[-1]) if c["id"].rsplit("t", 1)[-1].isdigit() else 0):
        song = os.path.join(ROOT, c.get("song") or "")
        if not c.get("song") or not os.path.exists(song):
            continue
        snap = os.path.join(work, c["id"] + ".yaml")
        with open(song) as f, open(snap, "w") as g:
            g.write(f.read())
        wav = os.path.join(work, c["id"] + ".wav")
        env = dict(os.environ, RAYON_NUM_THREADS="4")
        env.pop("LD_LIBRARY_PATH", None)
        r = subprocess.run([pin, "render", "-f", snap, "--seed", "0", "-o", wav], capture_output=True, text=True, env=env)
        if r.returncode == 0:
            out.append((c["id"], (c.get("meta") or {}).get("title", ""), wav))
        else:
            print(f"{c['id']}: render failed: {r.stderr.strip()[-200:]}", file=sys.stderr)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("wavs", nargs="*")
    ap.add_argument("--album")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    rows = []
    with tempfile.TemporaryDirectory(prefix="levels-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None) as work:
        items = render_album(a.album, work) if a.album else [(os.path.basename(w), "", w) for w in a.wavs]
        for cid, title, wav in items:
            r = measure(wav)
            r.update({"id": cid, "title": title})
            rows.append(r)
    if len(rows) > 1:
        med = float(np.median([r["lufs"] for r in rows]))
        for r in rows:
            if r["lufs"] > med + 2:
                r["flags"].append("LOUD")
            elif r["lufs"] < med - 2:
                r["flags"].append("QUIET")
    if a.json:
        print(json.dumps(rows, indent=1))
        return
    print(f"{'track':16s} {'title':24s} {'dur':>6s} {'peak':>6s} {'TP':>6s} {'LUFS':>6s} {'STmax':>6s} {'PLR':>5s} "
          f"{'@peak%':>7s} {'run':>4s}  flags")
    for r in rows:
        print(f"{r['id'][:16]:16s} {r['title'][:24]:24s} {r['dur']:6.1f} {r['peak_dbfs']:6.2f} {r['true_peak_dbtp']:6.2f} "
              f"{r['lufs']:6.1f} {r['st_max_lufs']:6.1f} {r['plr']:5.1f} {r['near_peak_pct']:7.3f} "
              f"{r['longest_pinned_run']:4d}  {' '.join(r['flags'])}")
    if len(rows) > 1:
        lu = [r["lufs"] for r in rows]
        print(f"album: LUFS {min(lu):.1f}..{max(lu):.1f} (median {np.median(lu):.1f}, spread {max(lu) - min(lu):.1f} LU); "
              f"max true peak {max(r['true_peak_dbtp'] for r in rows):.2f} dBTP")


if __name__ == "__main__":
    main()
