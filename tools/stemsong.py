#!/usr/bin/env python3
"""A first song from stems alone, for climbs without a tab: on a constant-tempo grid (bpm, phase, beats per bar
from onset autocorrelation), each part is transcribed from its Demucs stem —
  chords: at every onset, the stem's strongest pitch classes (≤3, ≥15% of the chroma) placed in the octave of
          their spectral peaks (piano, guitar, accordion …)
  line:   one note per onset, the strongest low peak (bass)
  voice:  a sung line, YIN pitch per note between vocal onsets (unvoiced notes skipped)
  pad:    per bar, the dominant pitch class (+ a strong second) held (atmospheres)
— with velocities from onset levels, starts quantised to --grid per beat and notes held to the next onset (capped).
Writes a song with one track per part, a hall bus and a gentle master; drums are added afterwards with
drumtrans.py (it needs the song's tempo) and the score climbs from there.

  stemsong.py OUT.yaml --stems DIR --bpm 140.6 --offset 0.33 --bpb 3 --parts STEM:PATCH:MODE[:GAIN] …
              [--grid 4] [--max-beats 3] [--tail 4s]

e.g. --parts piano:piano:chords:-2 bass:upright-bass:line:-4 vocals:voice:voice other:accordion:pad:-10"""
import os
import sys
import importlib.util

import numpy as np
from scipy.signal import find_peaks

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402

SR = 48000
spec = importlib.util.spec_from_file_location("sp", os.path.join(HERE, "stempitch.py"))
SP = importlib.util.module_from_spec(spec); spec.loader.exec_module(SP)
NAMES = "C C# D D# E F F# G G# A A# B".split()


def fmt(x):
    return f"{round(x, 4):.4f}".rstrip("0").rstrip(".")


def name(mi):
    return f"{NAMES[mi % 12]}{mi // 12 - 1}"


def env_flux(x, lo, hi, hop=240):
    n = len(x) // hop
    f = np.fft.rfftfreq(2048, 1 / SR); sel = (f >= lo) & (f <= hi); win = np.hanning(2048).astype(np.float32)
    fr = np.lib.stride_tricks.sliding_window_view(np.pad(x, (1024, 1024)), 2048)[::hop][:n]
    env = np.empty(n, dtype=np.float32)
    for i in range(0, n, 4096):
        sp = np.abs(np.fft.rfft(fr[i:i + 4096] * win, axis=1)) ** 2
        env[i:i + 4096] = 10 * np.log10(sp[:, sel].sum(1) + 1e-12)
    return env, np.maximum(np.diff(env, prepend=env[0]), 0)


def onsets(x, lo, hi, gap=0.09, pct=85):
    env, fl = env_flux(x, lo, hi)
    pk, _ = find_peaks(fl, height=np.percentile(fl, pct), distance=max(1, int(gap * SR / 240)))
    floor = np.percentile(env, 95) - 35
    return [(p * 240 / SR, float(env[min(p + 4, len(env) - 1)])) for p in pk if env[min(p + 4, len(env) - 1)] > floor]


def spectrum(seg, n=16384):
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n=max(n, len(seg)))); f = np.fft.rfftfreq(max(n, len(seg)), 1 / SR)
    return f, sp


def place(f, sp, pc, lo_m, hi_m):
    best, bm = -1.0, None
    for mi in range(lo_m, hi_m + 1):
        if mi % 12 != pc:
            continue
        fr = 440 * 2 ** ((mi - 69) / 12); sel = (f > fr * 0.985) & (f < fr * 1.015)
        v = sp[sel].max() if sel.any() else 0.0
        if v > best:
            best, bm = v, mi
    return bm


def chroma_of(f, sp, lo=60, hi=2000):
    m = (f >= lo) & (f <= hi); pcs = ((np.round(12 * np.log2(f[m] / 440)) + 9) % 12).astype(int)
    c = np.bincount(pcs, weights=sp[m] ** 2, minlength=12); return c / (c.sum() + 1e-12)


def transcribe(x, mode, grid_b, dur_s):
    """→ list of (t_start, t_end, [midi…], level)."""
    out = []
    if mode == "pad":
        return out
    lo, hi = {"chords": (80, 4000), "line": (30, 400), "voice": (150, 4000)}[mode]
    ons = onsets(x, lo, hi, gap=0.12 if mode == "voice" else 0.09)
    for i, (t, lvl) in enumerate(ons):
        e = ons[i + 1][0] if i + 1 < len(ons) else min(t + 1.0, dur_s)
        seg = x[int((t + 0.02) * SR):int(min(e, t + 0.3) * SR)]
        if len(seg) < 2048:
            continue
        f, sp = spectrum(seg)
        if mode == "chords":
            c = chroma_of(f, sp); pcs = [k for k in np.argsort(c)[::-1][:3] if c[k] >= 0.15]
            notes = sorted({m for m in (place(f, sp, k, 40, 84) for k in pcs) if m is not None})
        elif mode == "line":
            m_ = (f >= 30) & (f <= 300); notes = [int(round(69 + 12 * np.log2(f[m_][np.argmax(sp[m_])] / 440)))]
        else:
            fr = [seg[j:j + int(0.04 * SR)] for j in range(0, len(seg) - int(0.04 * SR), int(0.02 * SR))]
            f0 = [v for v in (SP.yin(q, 120, 900, 0.25) for q in fr) if v]
            if not fr or len(f0) < 0.5 * len(fr):
                continue
            notes = [int(round(69 + 12 * np.log2(np.median(f0) / 440)))]
        if notes:
            out.append((t, e, notes, lvl))
    return out


def pad(x, bpm, offset, bpb, dur_s):
    out, bar = [], bpb * 60 / bpm
    t = offset
    while t + bar <= dur_s:
        seg = x[int(t * SR):int((t + bar) * SR)]
        if 10 * np.log10(np.mean(seg ** 2) + 1e-12) > -55:
            f, sp = spectrum(seg, 32768); c = chroma_of(f, sp, 60, 2000); o = np.argsort(c)[::-1]
            if c[o[0]] >= 0.22:
                ns = [place(f, sp, o[0], 48, 84)]
                if c[o[1]] >= 0.5 * c[o[0]]:
                    ns.append(place(f, sp, o[1], 48, 84))
                out.append((t, t + bar, sorted({n for n in ns if n is not None}), 10 * np.log10(np.mean(seg ** 2) + 1e-12)))
        t += bar
    return out


def score(events, bpm, offset, grid, max_beats):
    b0 = offset * bpm / 60
    q = lambda t: b0 + round((t * bpm / 60 - b0) * grid) / grid
    ref = np.percentile([e[3] for e in events], 90) if events else 0
    toks, cur = [], 0.0
    for s, e, notes, lvl in events:
        bs = q(s); be = min(q(e), bs + max_beats)
        if bs < cur - 1e-9:
            continue
        if be <= bs:
            be = bs + 1 / grid
        if bs > cur + 1e-9:
            toks.append(f"R/{fmt(bs - cur)}b")
        v = int(np.clip(100 + 1.8 * (lvl - ref), 35, 125))
        toks.append(f"{','.join(name(n) for n in notes)}/{fmt(be - bs)}b@{v}"); cur = be
    return " ".join(toks)


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    out, stems = a[0], opt("--stems", "")
    bpm, offset, bpb, grid, mb = opt("--bpm", 120.0), opt("--offset", 0.0), opt("--bpb", 4), opt("--grid", 4), opt("--max-beats", 3.0)
    parts = a[a.index("--parts") + 1:]
    parts = parts[:next((i for i, p in enumerate(parts) if p.startswith("--")), len(parts))]
    tracks = []
    for spec_ in parts:
        bits = spec_.split(":"); stem, patch, mode = bits[:3]; gain = bits[3] if len(bits) > 3 else "0"
        x = L.load(os.path.join(stems, stem + ".wav")).mean(1); dur = len(x) / SR
        ev = pad(x, bpm, offset, bpb, dur) if mode == "pad" else transcribe(x, mode, grid, dur)
        sc = score(ev, bpm, offset, grid, bpb * 60 / bpm * 1e9 if mode == "pad" else mb)
        tracks.append((f"{stem}-{mode}", patch, gain, sc, len(ev)))
        print(f"{stem}:{mode} → {patch}: {len(ev)} events", file=sys.stderr)
    lines = [f"tempo: {bpm}", f"tail: {opt('--tail', '4s')}", "buses:", '  hall: {fx: ["reverb kind=hall decay=2.6s mix=1 predelay=20ms"]}',
             "master: [\"glue threshold=-16dB ratio=2 attack=10ms release=150ms makeup=2dB\"]", "tracks:"]
    for n, p, g, sc, _ in tracks:
        lines.append(f'  - {{name: "{n}", patch: "{p}", gain: "{g}dB", sends: {{"hall": "-10dB"}}, score: "{sc}"}}')
    open(out, "w").write("\n".join(lines) + "\n")
    print(f"wrote {out}: {len(tracks)} tracks", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
