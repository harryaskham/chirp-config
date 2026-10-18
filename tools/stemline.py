#!/usr/bin/env python3
"""Monophonic line transcription from a stem onto a song's tempo map (the pitched counterpart of drumtrans.py):
for a bass (or any single-line part) whose tab rhythm does not follow the record, take the notes from the stem —
onsets from the stem's flux in the part's band, each note's pitch from the strongest spectral peak between that
onset and the next (so a recording's real register wins: Pneuma's A2 over the tab's D1), velocity from the
onset's level — quantised to a beat grid of the song's own tempo map and held until the next onset (or a rest
where the stem falls silent). Writes a raw part for tab2song covering only the chosen bars (rests elsewhere).

  stemline.py STEM.wav SONG.yaml MAP.json OUT.json --bars 285-352 [--key line] [--lo 30] [--hi 300]
             [--grid 12] [--min-gap 0.07] [--shift 0.0]

SONG.yaml supplies the tempo map (tab2song output of MAP.json); MAP.json supplies the bar layout."""
import json
import os
import sys
import importlib.util

import numpy as np
from scipy.signal import find_peaks

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402
import drumtrans as D  # noqa: E402

spec = importlib.util.spec_from_file_location("bc", os.path.join(HERE, "barchroma.py"))
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
SR = 48000


def fmt(x):
    return f"{round(x, 4):.4f}".rstrip("0").rstrip(".")


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    x = L.load(a[0]).mean(1); mp = json.load(open(a[2]))
    lo_f, hi_f, grid, gap, shift = opt("--lo", 30.0), opt("--hi", 300.0), opt("--grid", 12), opt("--min-gap", 0.07), opt("--shift", 0.0)
    # bar range → time range through the map's corrected timeline
    root = os.path.dirname(HERE)
    cache = mp["cache"] if os.path.isabs(mp["cache"]) else os.path.join(root, mp["cache"])
    tl = B.T.performed_timeline(cache, mp)  # the performed clock: skips and repeats (bd-8e945f)
    b0, b1 = (int(v) for v in opt("--bars", "1-100000").split("-"))
    t, t0, t1 = mp.get("offset", 0.0), None, None
    for m in tl:
        if m["m"] == b0 and t0 is None: t0 = t   # its first play; t1 ends its last
        t += m["beats"] * 60 / m["bpm"]
        if m["m"] == b1: t1 = t
    # tempo map (song beats ↔ seconds)
    tb = D.time_to_beat(D.tempo_points(a[1]))
    # onsets: log-energy flux in the part's band, 5 ms hop
    hop = 240; n = len(x) // hop
    f = np.fft.rfftfreq(2048, 1 / SR); sel = (f >= lo_f) & (f <= hi_f)
    frames = np.lib.stride_tricks.sliding_window_view(np.pad(x, (1024, 1024)), 2048)[::hop][:n]
    win = np.hanning(2048).astype(np.float32)
    env = np.empty(n, dtype=np.float32)
    for i in range(0, n, 4096):
        sp = np.abs(np.fft.rfft(frames[i:i + 4096] * win, axis=1)) ** 2
        env[i:i + 4096] = 10 * np.log10(sp[:, sel].sum(1) + 1e-12)
    flux = np.maximum(np.diff(env, prepend=env[0]), 0)
    k0, k1 = int(t0 * SR / hop), int(t1 * SR / hop)
    pk, _ = find_peaks(flux[k0:k1], height=np.percentile(flux[k0:k1], 80), distance=max(1, int(gap * SR / hop)))
    on = (pk + k0) * hop / SR
    level_floor = np.percentile(env[k0:k1], 90) - 30
    notes = []
    for i, s in enumerate(on):
        e = on[i + 1] if i + 1 < len(on) else t1
        seg = x[int(s * SR):int(min(e, s + 0.5) * SR)]
        if len(seg) < 1024 or env[int(s * SR / hop)] < level_floor:
            continue
        spc = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n=max(16384, len(seg)))); ff = np.fft.rfftfreq(max(16384, len(seg)), 1 / SR)
        m = (ff >= lo_f) & (ff <= hi_f)
        f0 = ff[m][np.argmax(spc[m])]
        midi = int(round(69 + 12 * np.log2(f0 / 440)))
        lvl = float(env[int(s * SR / hop)])
        notes.append((s, e, midi, lvl))
    if not notes:
        raise SystemExit("no notes")
    ref = np.percentile([n_[3] for n_ in notes], 90)
    name = lambda mi: f"{B.NAMES[mi % 12]}{mi // 12 - 1}"
    q = lambda tt: round(tb(tt + shift) * grid) / grid
    toks, cur = [], 0.0
    beat0, beat1 = q(t0), q(t1)
    if beat0 > 0:
        toks.append(f"R/{fmt(beat0)}b"); cur = beat0
    for s, e, midi, lvl in notes:
        bs, be = q(s), min(q(e), beat1)
        if bs < cur:
            continue
        if be <= bs:
            be = bs + 1 / grid
        if bs > cur:
            toks.append(f"R/{fmt(bs - cur)}b")
        vel = int(np.clip(100 + 2.0 * (lvl - ref), 40, 127))
        toks.append(f"{name(midi)}/{fmt(be - bs)}b@{vel}")
        cur = be
    json.dump({opt("--key", "line"): {"score": " ".join(toks)}}, open(a[3], "w"))
    print(f"bars {b0}-{b1} = {t0:.1f}-{t1:.1f} s: {len(notes)} notes; pitches {sorted({name(n_[2]) for n_ in notes})[:12]}")


if __name__ == "__main__":
    main(sys.argv[1:])
