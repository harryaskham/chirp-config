#!/usr/bin/env python3
"""Retime a part's notes to a stem's onsets: keep every note of a song track (pitches, order, articulations) but
move each onset inside a time range to the nearest onset detected in the stem (within --window seconds), so a
tab-grid part plays with the record's real timing (rubato, pushes, an odd grouping's offsets). Durations stretch
or shrink so each note still reaches the next one; notes with no stem onset nearby keep their tab time. Writes the
track's whole score (retimed inside the range) as a raw part for tab2song.

  stemretime.py STEM.wav SONG.yaml TRACK OUT.json --from S --to S [--key part] [--window 0.12] [--lo 80]
               [--hi 6000] [--grid 24] [--only-in T0-T1,…]

--only-in: retime only notes starting inside these ranges (s); others keep their time — keep a retime where its paired
per-section deltas win (Flim's drums: sections 2/6 up, 3/4 down)."""
import json
import os
import re
import sys

import numpy as np
from scipy.signal import find_peaks

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402
import drumtrans as D  # noqa: E402
import stemvowels as V  # noqa: E402

SR = 48000


def fmt(x):
    return f"{round(x, 4):.4f}".rstrip("0").rstrip(".")


def onsets(x, lo, hi, t0, t1):
    hop = 240; a, b = int(t0 * SR), int(t1 * SR); seg = x[a:b]
    n = len(seg) // hop
    win = np.hanning(2048).astype(np.float32); f = np.fft.rfftfreq(2048, 1 / SR); sel = (f >= lo) & (f <= hi)
    fr = np.lib.stride_tricks.sliding_window_view(np.pad(seg, (1024, 1024)), 2048)[::hop][:n]
    env = np.empty(n, dtype=np.float32)
    for i in range(0, n, 4096):
        sp = np.abs(np.fft.rfft(fr[i:i + 4096] * win, axis=1)) ** 2
        env[i:i + 4096] = 10 * np.log10(sp[:, sel].sum(1) + 1e-12)
    flux = np.maximum(np.diff(env, prepend=env[0]), 0)
    pk, _ = find_peaks(flux, height=np.percentile(flux, 85), distance=12)
    return t0 + pk * hop / SR


def main(a):
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    x = L.load(a[0]).mean(1); song, track = a[1], a[2]
    t0, t1, win, grid = opt("--from", 0.0), opt("--to", 1e9), opt("--window", 0.12), opt("--grid", 24)
    pts = D.tempo_points(song); tb = D.time_to_beat(pts)
    beats = np.array([b for b, _ in pts]); bpm = np.array([v for _, v in pts])
    secs = np.concatenate([[0.0], np.cumsum(np.diff(beats) * 60 / bpm[:-1])])

    def b2t(b):
        i = max(0, np.searchsorted(beats, b, side="right") - 1)
        return secs[i] + (b - beats[i]) * 60 / bpm[i]

    toks = V.track_tokens(song, track)
    ev, pos = [], 0.0                      # (start beat, length, body, rest-of-token, controls before it)
    pending = []                           # control tokens (bend=, ccN=, …) ride with the next note when it moves
    for t in toks:
        m = re.match(r"^([^/]+)/([0-9.]+)b(.*)$", t)
        if not m:
            if "=" in t:
                pending.append(t)
            continue
        ctl = []
        if m.group(1) not in ("R", "r", "_"):
            ctl, pending = pending, []
        ev.append([pos, float(m.group(2)), m.group(1), m.group(3), ctl]); pos += float(m.group(2))
    only = [tuple(float(v) for v in r.split("-")) for r in opt("--only-in", "").split(",")] if "--only-in" in a else None
    on = onsets(x, opt("--lo", 80.0), opt("--hi", 6000.0), max(0.0, t0 - 0.5), t1 + 0.5)
    moved = 0
    for e in ev:
        if e[2] in ("R", "r", "_"):
            continue
        ts = b2t(e[0])
        if not (t0 <= ts < t1) or not len(on):
            continue
        if only and not any(a0 <= ts < a1 for a0, a1 in only):
            continue   # outside --only-in: keeps its time
        k = int(np.argmin(np.abs(on - ts)))
        if abs(on[k] - ts) <= win:
            nb = round(tb(on[k]) * grid) / grid
            if abs(nb - e[0]) > 1e-9:
                moved += 1
            e.append(nb)
    # rebuild: notes at their (possibly moved) starts, each lasting to the next note's start (or its own length)
    notes = [(e[5] if len(e) > 5 else e[0], e[0] + e[1], e[2], e[3], e[4]) for e in ev if e[2] not in ("R", "r", "_")]
    notes.sort(key=lambda n: n[0])
    out, cur = [], 0.0
    for i, (s, e_end, body, rest, ctl) in enumerate(notes):
        if s < cur - 1e-9:
            s = cur
        nxt = notes[i + 1][0] if i + 1 < len(notes) else e_end
        end = min(max(e_end, s + 1 / grid), max(nxt, s + 1 / grid)) if nxt > s else s + 1 / grid
        if s > cur + 1e-9:
            out.append(f"R/{fmt(s - cur)}b")
        out.extend(ctl)
        out.append(f"{body}/{fmt(end - s)}b{rest}"); cur = end
    if pending:
        out.extend(pending)
    json.dump({opt("--key", "part"): {"score": " ".join(out)}}, open(a[3], "w"))
    print(f"{len(notes)} notes; {moved} moved to stem onsets within ±{win * 1000:.0f} ms in {t0:.0f}-{t1:.0f} s; {len(on)} stem onsets")


if __name__ == "__main__":
    main(sys.argv[1:])
