#!/usr/bin/env python3
"""DTW-anchored beat grid for a tab2song map: fixes the grid where riffs alias.

  dtwgrid.py MAP.json RENDER.wav REF.wav [--block 4] [--window 0.08] [--frame 0.1] [--minconf 0.1] [--clamp 0.15]
            [--ref-onsets REF_STEM.wav --render-onsets OUR_SOLO.wav] [--keep-below] [--bars A-B] [--feature flux|metric] [--around-zero] [-o OUT.json] [--report]

RENDER.wav must be a render of the song MAP.json generates (so its bar times are the map's). Two signals:

  * DTW (scorealign.py features, --frame s) maps every render bar onto the recording unambiguously, to about
    one frame (+-0.1 s) — too coarse for the rhythm metric (~20 ms) but never off by a whole riff cell.
  * Onset correlation (5 ms flux of the 80-250 Hz and 2.5-6 kHz bands, summed) per block of --block bars is
    precise but periodic: with steady eighths the peaks repeat every eighth (beatgrid.py's pulse phase locks to
    the wrong one, and its unwrap fails across tempo changes).

--ref-onsets/--render-onsets correlate other signals with the same timelines instead of the two mixes — e.g.
the reference's drum stem against a drums-only render of the same song: drums are the sharpest timing evidence
(10-20 ms drifts collapse a 5 ms flux correlation). --keep-below: blocks under --minconf keep their current
timing (lag 0) instead of taking the DTW lag — for a refinement pass on an already-aligned map. --feature metric: correlate likeness.py's own onset envelope (spectral flux,
~21 ms frames, smoothed +-50 ms as the rhythm term does; interpolated to 5 ms) instead of the sharp 5 ms band
flux — where the 5 ms flux is too noisy to correlate (Laid to Rest's breakdown: flux 0.09-0.28, metric 0.5-0.7),
and it aligns exactly what the rhythm term scores. --around-zero: search +-window around the current timing instead of the DTW lag (a refinement pass where DTW
itself anchors poorly). --bars A-B: only
blocks starting inside measures A..B move (the rest keep their timing) — splice a good region in. Caveats: DTW
anchors poorly where the render does not resemble the record yet (Pneuma's drum-solo middle and outro lost 1-2.5
per section: lags of +0.5..+1.2 s) — check per-section scores and splice with --bars/--keep-below; and stem-timed
parts (drumtrans/stemvox/stemnotes output) are in beats, so re-transcribe them on the new grid. Per block, the lag is the onset-correlation peak within +-window s of the DTW lag. Block starts move to where
the band played them (blocks whose onset correlation is below --minconf — sections the transcription or the
instruments don't match yet — take the DTW lag itself; a block's tempo change is clamped to +-clamp); every kept measure gets a "bpm" override so each block spans its real duration (the
shape inside a block scales together) and the map's offset moves with the first block. Regenerate, render,
and re-run: --report prints the residual lags only.
"""
import importlib.util
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402
import mixfeel as M  # noqa: E402


def load_mod(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metric_onset(path):
    F = L.Feat(L.load(path))
    o = np.convolve(F.onset, np.ones(5) / 5, "same")
    t = np.arange(len(o)) / L.FPS
    return np.interp(np.arange(0, t[-1], 0.005), t, o)


def flux(path):
    E = M.envelopes(L.load(path))
    return np.maximum(np.diff(E[1]), 0) + np.maximum(np.diff(E[4]), 0)   # 5 ms frames


def main():
    a = sys.argv[1:]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d  # noqa: E731
    mpath, render, ref = a[0], a[1], a[2]
    block, window, frame = int(opt("--block", "4")), float(opt("--window", "0.08")), float(opt("--frame", "0.1"))
    minconf, clamp = float(opt("--minconf", "0.1")), float(opt("--clamp", "0.15"))
    bar_range = tuple(int(v) for v in opt("--bars", "").split("-")) if "--bars" in a else None
    T2S, SA = load_mod("t2s", "tab2song.py"), load_mod("sa", "scorealign.py")
    mp = json.load(open(mpath))
    cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(os.path.dirname(HERE), mp["cache"])
    keep = [m for m in T2S.corrected_timeline(cache, mp) if not m["skip"]]
    t, starts = mp.get("offset", 0.0), []
    for m in keep:
        starts.append(t)
        t += m["beats"] * 60 / m["bpm"]
    end = t
    A, dt = SA.feats(render, frame)
    B, _ = SA.feats(ref, frame)
    ci, rj, _ = SA.dtw(A, B, int(15 / dt))
    f = SA.mapping(ci, rj, dt)
    feat = metric_onset if opt("--feature", "flux") == "metric" else flux
    fo = feat(opt("--render-onsets", render))
    fr = feat(opt("--ref-onsets", ref))
    blocks = list(range(0, len(keep), block))
    lags, confs = [], []
    for bi in blocks:
        s0 = starts[bi]
        s1 = starts[bi + block] if bi + block < len(keep) else end
        dtw_lag = s0 - float(f([s0])[0])               # + = render later than the recording
        if "--around-zero" in a:
            dtw_lag = 0.0
        i0, i1 = int(s0 * 200), int(s1 * 200)
        o = fo[i0:i1] - fo[i0:i1].mean()
        best = (-9.0, dtw_lag)
        for k in range(int((dtw_lag - window) * 200), int((dtw_lag + window) * 200) + 1):
            j0, j1 = i0 - k, i1 - k
            if j0 < 0 or j1 > len(fr):
                continue
            r = fr[j0:j1] - fr[j0:j1].mean()
            c = float((o * r).sum() / (np.linalg.norm(o) * np.linalg.norm(r) + 1e-9))
            if c > best[0]:
                best = (c, k / 200)
        lags.append(best[1] if best[0] >= minconf else (0.0 if "--keep-below" in a else dtw_lag))
        if bar_range and not (bar_range[0] <= keep[bi]["m"] <= bar_range[1]):
            lags[-1] = 0.0
        confs.append(best[0])
    if "--report" in a:
        al = np.abs(lags)
        print(f"{len(blocks)} blocks; lag (ms): " + " ".join(f"{l * 1000:+.0f}" for l in lags))
        print(f"residual |lag| median {np.median(al) * 1000:.0f} ms, p90 {np.percentile(al, 90) * 1000:.0f} ms")
        return
    real = [starts[bi] - lag for bi, lag in zip(blocks, lags)]
    bpm = dict(mp.get("bpm", {}))
    for n, bi in enumerate(blocks):
        span_ours = (starts[blocks[n + 1]] if n + 1 < len(blocks) else end) - starts[bi]
        span_real = (real[n + 1] if n + 1 < len(blocks) else end - lags[-1]) - real[n]
        scale = span_ours / span_real if span_real > 0 else 1.0
        scale = min(1 + clamp, max(1 - clamp, scale))
        for m in keep[bi:bi + block]:
            bpm[str(m["m"])] = round(m["bpm"] * scale, 4)
    mp["bpm"] = bpm
    mp["offset"] = round(real[0], 4)
    text = json.dumps(mp, indent=2) + "\n"
    open(opt("-o", mpath), "w").write(text)
    print(f"{len(blocks)} blocks; lag (ms): " + " ".join(f"{l * 1000:+.0f}" for l in lags))
    print("confidence: " + " ".join(f"{c:.2f}" for c in confs))
    print(f"offset {mp['offset']} s")


if __name__ == "__main__":
    main()
