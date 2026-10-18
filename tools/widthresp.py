#!/usr/bin/env python3
"""Width-stage response: what each band-width coefficient does to the seven measured side/mid bands (bd-33c6c3).

The master width stage (dsp/fx.rs `Width`) splits the SIDE signal with a cascade of Butterworth low-passes
(Cytomic SVF, Q 1/sqrt2) at its crossovers: each piece is a low-pass of what is left, so the pieces sum back
exactly, and piece i is scaled by the width of the crossover below it — `bands: [[f_k, w_k] …]` sets the side
gain from f_k UP to the next crossover (lower-edge semantics; below the first crossover: unchanged). The pieces
overlap (12 dB/oct, crossovers ~3x apart) and differ in phase, so a measured band (likeness: 20-60-150-400-1.2k
-3.5k-8k-16k) is a complex sum of several coefficients: the response is NOT diagonal. On the MM tail widths
(wb4 1.951, wb5 4.215, wb6 4.493) the 1.2-3.5k band measures x4.08 (its own coefficient: 1.95), 400-1.2k x1.76
(coefficient 1) and 150-400 x0.70 (cancellation near a crossover). widthfit's per-band ratio therefore
mis-steers whenever neighbouring widths differ: lowering wb4 there widens 3.5-8k.

The model here is exact for the stage (it matches engine renders to <0.01 dB); mid is untouched. A render's side
spectrum predicts any other widths: each frequency's side power scales by |H(new)|^2/|H(old)|^2 (assuming the
master chain after the stage is linear on the side, as in the MM tail: mid unchanged to numerical precision).

  widthresp.py matrix [--widths w0,…,w6] [--wav RENDER.wav --at A-B]
        coefficient -> measured-band response: each band's S/M gain and d log2(band)/d log2(w_k) (input side
        spectrum: white, or the render's in A-B seconds)
  widthresp.py probe [--bin CHIRP] [--widths w0,…,w6]
        render a hard-left noise probe through the engine's stage alone (width 1, bass_width 1, mono_below 0, no
        other fx): the unity-stage residue vs no stage (16-bit steps) and model vs measured per band (dB) at the
        widths (default: the MM v14 tail, 6,.364,1.533,1.251,1.951,4.215,4.493). The matrix and the errors are
        local to the widths given: the response depends on every width.
  widthresp.py probe --tones 100,250,700,2000,5000,11000 [--bin CHIRP] [--widths …]
        a multisine probe: hard-left tones, each tone's side/mid gain against the model's |H| at that frequency
  widthresp.py predict RENDER.wav --at A-B --from w0,…,w6 --to w0,…,w6 [--bands 1200-3500,3500-8000]
  … [--crossover legacy|lr4]   which stage topology to model and probe (default legacy; lr4: see below)
        a render's side/mid per measured band and side/mid dBFS in Butterworth bands, now and predicted

widthfit.py --joint uses this model to solve all seven widths of a section together.

Crossover `lr4` (bd-85ba39, opt-in, experimental): `--crossover lr4` on matrix/probe/predict models the stage's
phase-aligned Linkwitz-Riley split instead. Each lower edge splits what is left with LP4/HP4 (two identical Cytomic
SVF sections, Q 1/sqrt2, prewarped); lower branches pass every later edge's allpass AP2 = LP4+HP4, and mid passes the
same cascade. With t_i = tan(pi f/SR)/tan(pi fc_i/SR), l_i = 1/(1+t_i^4), h_i = 1-l_i, the band weights
b_i = l_i * prod_{j<i} h_j (and prod_j h_j above the last edge) are real, non-negative and sum to 1, so the side gain
is A * sum_i g_i b_i with A = prod_i AP2_i common to mid and side: a convex combination of the widths (no overshoot,
monotonic in each). Unity widths are flat in magnitude but not waveform-neutral (the allpass). The legacy stage
stays the default everywhere; do not fit legacy lanes with this model, or this model's lanes with the legacy one.
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000
FREQS = [20, 60, 150, 400, 1200, 3500, 8000]
CHIRP = os.environ.get("CHIRP", "/tmp/lt/pins/chirp-a931418")


def svf_lp(f, fc):
    """The engine's Cytomic SVF low-pass (Q 1/sqrt2, bilinear with prewarping) at frequencies f."""
    fc = min(max(fc, 10.0), SR * 0.49)
    t = np.tan(np.pi * np.asarray(f, float) / SR) / np.tan(np.pi * fc / SR)
    return 1 / (1 + 1j * np.sqrt(2) * t - t * t)


def onepole_lp(f, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    return (1 - a) / (1 - a * np.exp(-2j * np.pi * np.asarray(f, float) / SR))


def lr4_weights(f, freqs=FREQS):
    """The lr4 stage's band weights at frequencies f: [below the first edge, above edge 0, …, above the last] (they
    sum to 1), and the common allpass A (bd-85ba39's transfer contract)."""
    f = np.asarray(f, float)
    edges = sorted(min(max(float(fc), 20.0), 20000.0) for fc in freqs)[:16]
    weights, through, A = [], np.ones_like(f), np.ones_like(f, dtype=complex)
    for fc in edges:
        fc = min(max(min(fc, SR * 0.45), 10.0), SR * 0.49)
        t = np.tan(np.pi * f / SR) / np.tan(np.pi * fc / SR)
        lo = 1 / (1 + t ** 4)
        weights.append(lo * through)
        through = through * (1 - lo)
        A = A * (1 - t * t - 1j * np.sqrt(2) * t) / (1 - t * t + 1j * np.sqrt(2) * t)
    return weights + [through], A


def response(f, widths, freqs=FREQS, width=1.0, bass_width=1.0, mono_below=120.0, gentle=False, crossover="legacy"):
    """Complex side gain of a width stage at frequencies f (the per-sample code in dsp/fx.rs `Width`). With
    crossover="lr4" the gain is relative to the stage's mid, which passes the same allpass A (|A| = 1)."""
    if crossover not in ("legacy", "lr4"):
        raise ValueError(f"crossover {crossover!r}: legacy or lr4")
    if mono_below > 0:
        hp = 1 - onepole_lp(f, mono_below)
        hp = hp if gentle else hp * hp
        rest = hp * width + (1 - hp) * bass_width
    else:
        rest = np.full(np.shape(f), float(width), complex)
    if crossover == "lr4":
        weights, A = lr4_weights(f, freqs)
        gains = [1.0] + [float(np.clip(w, 0, 8)) for w in widths[:len(weights) - 1]]
        return A * rest * sum(g * b for g, b in zip(gains, weights))
    acc, g = 0, 1.0
    for i, fc in enumerate(freqs):
        lo = svf_lp(f, min(fc, SR * 0.45)) * rest
        acc = acc + g * lo
        rest = rest - lo
        g = float(np.clip(widths[i], 0, 8))
    return acc + g * rest


def spectra(st):
    """(f, side PSD, mid PSD) — likeness.stereo_bands' Welch estimate."""
    m, sd = st.mean(1), (st[:, 0] - st[:, 1]) / 2
    f, pm = signal.welch(m, SR, nperseg=8192)
    _, ps = signal.welch(sd, SR, nperseg=8192)
    return f, ps, pm


def band_ratios(f, ps, pm):
    """likeness.stereo_bands from PSDs: sqrt(side/mid energy) per measured band."""
    return np.array([np.sqrt(ps[(f >= a) & (f < b)].sum() / (pm[(f >= a) & (f < b)].sum() + 1e-20)) for _, a, b in L.BANDS7])


def predict_ratios(f, ps, pm, w_from, w_to, **stage):
    """A render's measured band S/M after its stage's widths change from w_from to w_to."""
    g = np.abs(response(f, w_to, **stage)) ** 2 / np.maximum(np.abs(response(f, w_from, **stage)) ** 2, 1e-12)
    return band_ratios(f, ps * g, pm)


def jacobian(f, ps, pm, widths, step=0.05, **stage):
    """d log2(measured band j) / d log2(w_k), by central differences (rows: measured bands, columns: w_k)."""
    J = np.zeros((7, 7))
    for k in range(7):
        up, dn = np.array(widths, float), np.array(widths, float)
        up[k] *= 2 ** step
        dn[k] *= 2 ** -step
        J[:, k] = (np.log2(predict_ratios(f, ps, pm, widths, up, **stage))
                   - np.log2(predict_ratios(f, ps, pm, widths, dn, **stage))) / (2 * step)
    return J


def _solve(A, b):
    """Gauss-Jordan with partial pivoting for the small normal equations. No LAPACK: with ~/.nix-profile/lib on
    LD_LIBRARY_PATH (pocket4's zshrc) numpy loads an ABI-mismatched openblas LAPACK — solve/inv/det crash and
    lstsq/svd return wrong values (matmul is fine)."""
    n = len(b)
    M = np.hstack([np.array(A, float), np.array(b, float).reshape(-1, 1)])
    for c in range(n):
        p = c + int(np.argmax(np.abs(M[c:, c])))
        M[[c, p]] = M[[p, c]]
        if abs(M[c, c]) < 1e-15:
            continue
        M[c] /= M[c, c]
        for r in range(n):
            if r != c:
                M[r] -= M[r, c] * M[c]
    return M[:, -1]


def fit_joint(f, ps, pm, w0, target, lo=0.2, hi=2.5, cap=6.0, strength=1.0, ridge=0.02, **stage):
    """Widths for one section solving every measured band together: minimise the likeness stereo residuals
    log2((pred+0.02)/(target+0.02)) over u = log2(w/w0) in [log2 lo, log2 hi] (absolute 0.05..cap), with a small
    ridge so bands without side energy keep their widths (bounded Levenberg-Marquardt, LAPACK-free). strength < 1
    shrinks the step (as widthfit's ratio**S)."""
    w0 = np.maximum(np.array(w0, float), 0.05)
    live = np.array([pm[(f >= a) & (f < b)].sum() > 0 and ps[(f >= a) & (f < b)].sum() > 0 for _, a, b in L.BANDS7])

    def resid(u):
        r = predict_ratios(f, ps, pm, w0, w0 * 2 ** u, **stage)
        e = np.log2((r + 0.02) / (target + 0.02))
        return np.concatenate([np.where(live, e, 0.0), ridge * u])

    lb = np.minimum(np.maximum(np.log2(lo), np.log2(0.05 / w0)), 0.0)
    ub = np.maximum(np.minimum(np.log2(hi), np.log2(cap / w0)), 0.0)
    u, lam, h = np.zeros(7), 1e-2, 1e-3
    r = resid(u)
    for _ in range(80):
        J = np.zeros((len(r), 7))
        for k in range(7):
            d = np.zeros(7)
            d[k] = h if u[k] + h <= ub[k] else -h
            J[:, k] = (resid(u + d) - r) / d[k]
        g, A = J.T @ r, J.T @ J
        step = _solve(A + lam * np.diag(np.diag(A) + 1e-9), -g)
        un = np.clip(u + step, lb, ub)
        rn = resid(un)
        if rn @ rn < r @ r - 1e-12:
            moved = np.abs(un - u).max()
            u, r, lam = un, rn, max(lam / 3, 1e-7)
            if moved < 1e-5:
                break
        else:
            lam *= 4
            if lam > 1e6:
                break
    return w0 * 2 ** (u * strength)


def stereo_term(r_pred, target):
    """likeness' stereo score for band ratios (the per-band mean |log2| error, as in compare())."""
    return 100 * np.exp(-np.mean(np.abs(np.log2((r_pred + 0.02) / (target + 0.02)))) * 1.5)


def side_dbfs(st, lo, hi, gain=None, f_gain=None):
    """Side and mid dBFS of st in a Butterworth band lo..hi (as chirper-three's tail profile), the side optionally
    re-filtered by a frequency-domain gain (predicted widths)."""
    sos = signal.butter(4, [lo, hi], btype="bandpass", fs=SR, output="sos")
    y = signal.sosfilt(sos, st, axis=0)
    mid, side = y.mean(1), (y[:, 0] - y[:, 1]) / 2
    if gain is not None:
        S = np.fft.rfft(side)
        side = np.fft.irfft(S * gain(np.fft.rfftfreq(len(side), 1 / SR)), len(side))
    db = lambda v: float(10 * np.log10(np.mean(v * v) + 1e-14))  # noqa: E731
    return db(side), db(mid)


def widths_arg(s):
    v = [float(x) for x in s.split(",")]
    if len(v) != 7:
        sys.exit("widths: seven comma-separated values (wb0..wb6)")
    return v


def probe(binary, widths, seconds=12, crossover="legacy"):
    """Hard-left noise through the engine's width stage: (neutral max diff in 16-bit steps, measured, model). With
    crossover="lr4" the neutral control's residue is the allpass's waveform change, not rounding."""
    d = tempfile.mkdtemp(prefix="widthresp-")
    try:
        def render(ws, tag):
            song = {"tempo": 60, "patches": {"nz": {"synth": {"layers": ["noise"], "amp": "1ms 0 1 5ms"}}},
                    "tracks": [{"name": "n", "patch": "nz", "pan": -1, "gain": "-12dB", "score": f"gate=1 C4/{seconds}b"}]}
            if ws is not None:
                # the stage alone and explicitly neutral elsewhere: width 1, bass_width 1, no bass split
                song["master"] = {"fx": [{"type": "width", "width": 1.0, "bass_width": 1.0, "mono_below": 0,
                                          "bands": [[fc, w] for fc, w in zip(FREQS, ws)]}]}
                if crossover != "legacy":
                    song["master"]["fx"][0]["crossover"] = crossover
            p, out = os.path.join(d, f"{tag}.yaml"), os.path.join(d, f"{tag}.wav")
            with open(p, "w") as fh:
                json.dump(song, fh)
            r = subprocess.run([binary, "render", "-f", p, "-o", out], capture_output=True, text=True)
            if r.returncode:
                sys.exit(f"widthresp: {binary} render failed: {r.stderr.strip()[-300:]}")
            return L.load(out)[SR:(seconds - 1) * SR]
        none, neutral, x = render(None, "none"), render([1] * 7, "neutral"), render(widths, "w")
        res = (none - neutral) * 32768
        f, ps, pm = spectra(none)
        if crossover != "legacy":   # the unity stage's own band S/M against no stage (magnitude-neutral by design)
            return (float(np.abs(res).max()), float(np.sqrt(np.mean(res * res))), L.stereo_bands(neutral) / L.stereo_bands(none)), \
                L.stereo_bands(x), predict_ratios(f, ps, pm, [1] * 7, widths, mono_below=0, crossover=crossover)
        return (float(np.abs(res).max()), float(np.sqrt(np.mean(res * res)))), L.stereo_bands(x), \
            predict_ratios(f, ps, pm, [1] * 7, widths, mono_below=0)
    finally:
        import shutil
        shutil.rmtree(d, True)


def tone_probe(binary, widths, tones, seconds=10, crossover="legacy"):
    """Hard-left sine tones through the engine's stage alone: per tone (Hz, measured side/mid gain, model |H|)."""
    d = tempfile.mkdtemp(prefix="widthresp-")
    try:
        song = {"tempo": 60, "patches": {"s": {"synth": {"layers": ["sine"], "amp": "1ms 0 1 5ms"}}},
                "tracks": [{"name": f"t{i}", "patch": "s", "pan": -1, "gain": "-24dB", "score": f"gate=1 {t:g}hz/{seconds}b"}
                           for i, t in enumerate(tones)],   # one track per tone (a chord of hz notes does not parse)
                "master": {"fx": [{"type": "width", "width": 1.0, "bass_width": 1.0, "mono_below": 0,
                                   "bands": [[fc, w] for fc, w in zip(FREQS, widths)]}]}}
        if crossover != "legacy":
            song["master"]["fx"][0]["crossover"] = crossover
        p, out = os.path.join(d, "t.yaml"), os.path.join(d, "t.wav")
        with open(p, "w") as fh:
            json.dump(song, fh)
        r = subprocess.run([binary, "render", "-f", p, "-o", out], capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"widthresp: {binary} render failed: {r.stderr.strip()[-300:]}")
        x = L.load(out)[2 * SR:(seconds - 1) * SR]
        win = np.hanning(len(x))
        M = np.abs(np.fft.rfft(x.mean(1) * win))
        S = np.abs(np.fft.rfft((x[:, 0] - x[:, 1]) / 2 * win))
        fr = np.fft.rfftfreq(len(x), 1 / SR)
        rows = []
        for t in tones:
            k = int(np.argmin(np.abs(fr - t)))
            k = k - 2 + int(np.argmax(M[k - 2:k + 3]))
            if crossover == "legacy":
                rows.append((t, float(S[k] / M[k]), float(np.abs(response(np.array([fr[k]]), widths, mono_below=0))[0])))
            else:
                rows.append((t, float(S[k] / M[k]),
                             float(np.abs(response(np.array([fr[k]]), widths, mono_below=0, crossover=crossover))[0])))
        return rows
    finally:
        import shutil
        shutil.rmtree(d, True)


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d  # noqa: E731
    cmd = a[0]
    names = [n for n, _, _ in L.BANDS7]
    xo = opt("--crossover", "legacy")
    if xo not in ("legacy", "lr4"):
        sys.exit(f"widthresp: --crossover {xo}: legacy or lr4")
    st_ = {} if xo == "legacy" else {"crossover": xo}
    if cmd == "matrix":
        w = widths_arg(opt("--widths", "1,1,1,1,1,1,1"))
        if "--wav" in a:
            t0, t1 = (float(v) for v in opt("--at", "0-1e9").split("-"))
            f, ps, pm = spectra(L.load(opt("--wav", ""))[int(t0 * SR):int(t1 * SR)])
            w_from = widths_arg(opt("--render-widths", ",".join(map(str, w))))
            ps = ps * np.abs(response(f, w, **st_)) ** 2 / np.maximum(np.abs(response(f, w_from, **st_)) ** 2, 1e-12)
        else:
            f = np.linspace(1, SR / 2, 8193)
            ps = pm = np.ones_like(f)
        g = band_ratios(f, ps * np.abs(response(f, w, **st_)) ** 2, pm) / band_ratios(f, ps, pm)
        print("widths  " + " ".join(f"{v:7.3f}" for v in w))
        print("gain    " + " ".join(f"{v:7.3f}" for v in g) + "   (measured band S/M x, per band)")
        J = jacobian(f, ps, pm, w, **st_)
        print("d log2(band) / d log2(w_k)   rows: measured bands, columns: wb0..wb6")
        for j, n in enumerate(names):
            print(f"{n:7} " + " ".join(f"{v:7.3f}" for v in J[j]))
        off = np.abs(J - np.diag(np.diag(J))).sum(1) / np.maximum(np.abs(np.diag(J)), 1e-9)
        print("off/diag " + " ".join(f"{v:7.2f}" for v in off) + "   (0 = a band answers only its own width)")
    elif cmd == "probe":
        w = widths_arg(opt("--widths", "6,0.364,1.533,1.251,1.951,4.215,4.493"))   # MM v14 tail (bd-33c6c3)
        if "--tones" in a:   # a multisine probe: each tone's side/mid gain against |H| at that frequency
            print("tone Hz   measured   model   error dB")
            for t, m_, h in tone_probe(opt("--bin", CHIRP), w, [float(v) for v in opt("--tones", "").split(",")], **st_):
                print(f"{t:7g}  {m_:8.4f} {h:8.4f}   {20 * np.log10(h / m_):+.4f}")
            return
        ctl, meas, model = probe(opt("--bin", CHIRP), w, **st_)
        if xo == "legacy":
            peak, rms = ctl
            print(f"neutral control: unity stage (width 1, bass_width 1, mono_below 0) vs no stage: residue max {peak:.1f}, "
                  f"rms {rms:.3f} 16-bit steps (float rounding in the split-and-sum)")
        else:
            peak, rms, unity = ctl
            print(f"neutral control ({xo}): unity stage vs no stage: band S/M within "
                  f"{np.max(np.abs(20 * np.log10(unity))):.4f} dB (magnitude-flat); waveform residue max {peak:.1f}, "
                  f"rms {rms:.3f} 16-bit steps (the allpass phase, by design)")
        print("band     measured   model   error dB")
        for n, m_, p_ in zip(names, meas, model):
            print(f"{n:7}  {m_:8.3f} {p_:7.3f}   {20 * np.log10(p_ / m_):+.3f}")
    elif cmd == "predict":
        st = L.load(a[1])
        t0, t1 = (float(v) for v in opt("--at", "0-1e9").split("-"))
        seg = st[int(t0 * SR):int(t1 * SR)]
        w0, w1 = widths_arg(opt("--from", "")), widths_arg(opt("--to", ""))
        f, ps, pm = spectra(seg)
        print("band     now      predicted")
        for n, r0, r1 in zip(names, band_ratios(f, ps, pm), predict_ratios(f, ps, pm, w0, w1, **st_)):
            print(f"{n:7}  {r0:7.3f}  {r1:7.3f}")
        gain = lambda fr: np.abs(response(fr, w1, **st_)) / np.maximum(np.abs(response(fr, w0, **st_)), 1e-9)  # noqa: E731
        for band in opt("--bands", "1200-3500,3500-8000").split(","):
            lo, hi = (float(v) for v in band.split("-"))
            s0, m0 = side_dbfs(seg, lo, hi)
            s1, _ = side_dbfs(seg, lo, hi, gain)
            print(f"{band:>10} Hz: side {s0:8.3f} -> {s1:8.3f} dBFS ({s1 - s0:+.3f}), mid {m0:8.3f} (unchanged)")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
