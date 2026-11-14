#!/usr/bin/env python3
"""compscore: the metric for COMPOSED songs (composition mode, compose/README.md), which have no record to match.

  compscore.py ID OUT.wav [--save] [--text] [--song FILE]

Prints JSON like likeness ({"total": …, "terms": {name: 0-100}, "weights": {…}, "detail": {…}}), so it works as a
climb's `metric` (`python3 tools/compscore.py ID OUT.wav`). --save also stores this render's features for the album
terms (ref/compose/ALBUM/features/ID.json): pass it when you record a kept version (`chirpers.py refresh` re-renders
the whole album and saves every song's). --text prints a readable table instead of JSON. --song names the song file
the render came from (default songs/ID.yaml): its declared `tempo` sets the rhythm term's beat grid.

Terms (0-100 each; the total is their weighted mean over the terms that apply; weights come from the album's
compose/ALBUM/album.json "weights", defaults below):
  human      Harry's latest rating for this song (rate.py), x10; a rating of an older version counts half.
  peer       other agents' latest ratings (not the song's owner), x10.
  structure  sections by likeness's novelty segmentation: a count suited to the length, unequal lengths.
             Opt-in album.json params.sections.novelty: one cut (default 0.15) or a list such as
             [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18]; with a list, structure, variety and recurrence are each
             averaged over the cuts, so a boundary near the cut counts fractionally instead of flipping them.
  variety    within-song contrast across sections: loudness range, timbre spread, onset-density change.
  recurrence motifs return: the share of later sections that closely match an earlier, non-adjacent one, in a
             middle band (none = no development of material; all = one idea looped).
  rhythm     rhythmic interest: the share of onset periodicity (local autocorrelation maxima, weighted by squared
             height, no cutoff) off the eighth-note grid of the song's declared tempo, in a middle band, at a plausible
             onset density. Without a declared tempo the beat is estimated. A crude polymeter proxy (real Meshuggah
             records score low: their cycles sit on the sixteenth grid); a beat-synchronous measure would be better.
  spectrum   the mix's long-term spectrum within a tolerance (album.json spectrum_tolerance_db, default 6 dB) of the
             album's genre envelope (the genre_refs' average): flags a broken mix (no low end, a harsh top), never a
             clean or ambient track for being one (at 3 dB the clean intro lost ~6 total points: anti-variety).
  master     level, peak and crest factor in the album's ranges.
  length     duration within the slot's target range.
  cohesion   timbre close enough to the rest of the album (the other songs' saved features).
  distinct   not a near-copy of another album song (pitch-class histogram, tempo, density). Tempo is the declared
             tempo when there is one (the onset estimate flips between near-equal peaks).
  flow       the bleed into and out of the neighbouring tracks: level and spectrum continuity at the joins. It does
             not apply to an album whose album.json says "bleed": false (its songs stand apart: a cold start after
             the last song's ring-out is not a fault).
Agents can add terms: a file compose/measures/NAME.py defining measure(ctx) -> (score 0-100 or None, detail) joins
the total with the album's weights[NAME] (default 0.05). ctx holds id, wav, x (stereo), F (likeness.Feat), dur,
album (album.json), slot, others ({id: features}), ratings, and helpers. Keep terms deterministic for a given render.
"""
import argparse
import glob
import importlib.util
import json
import os
import re
import sys

# a metric command runs from a plain shell: one BLAS thread, or a loaded box spins (chirper-one's first run, 28 Oct)
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402

DEFAULT_WEIGHTS = {"human": 0.30, "peer": 0.05, "structure": 0.12, "variety": 0.12, "recurrence": 0.10,
                   "rhythm": 0.08, "spectrum": 0.07, "master": 0.06, "length": 0.04, "cohesion": 0.03,
                   "distinct": 0.02, "flow": 0.03}
# obZen/Immutable masters measure rms -13.5..-10.9 dBFS, crest 10.6-10.9 dB, peaks at 0.0
SPECTRUM_TOL = 6.0        # dB beyond the genre envelope before the spectrum term counts (28 Oct: 3 dB punished the
                          # album's clean tracks, Seed Crystal 39.5 / Five Breaths 61.5, pushing them toward the metal)
DEFAULT_MASTER = {"rms": [-14.0, -9.5], "peak_max": 0.0, "crest": [9.0, 12.5]}


# ── album / registry plumbing ───────────────────────────────────────────────────────────────

def registry():
    with open(os.path.join(ROOT, "climbs.json")) as f:
        return json.load(f)


def climb_of(cid, reg=None):
    reg = reg or registry()
    c = next((c for c in reg["climbs"] if c["id"] == cid), None)
    if c is None:
        raise SystemExit(f"compscore: no climb {cid}")
    return c


def album_dir(album_id):
    return os.path.join(ROOT, "compose", album_id)


def cache_dir(album_id):
    return os.path.join(ROOT, "ref", "compose", album_id)


def load_album(album_id):
    with open(os.path.join(album_dir(album_id), "album.json")) as f:
        return json.load(f)


def ratings(album_id):
    path = os.path.join(album_dir(album_id), "ratings.jsonl")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def ramp(v, lo, hi):
    """0 at or below lo, 100 at or above hi, linear between."""
    if hi == lo:
        return 100.0 if v >= hi else 0.0
    return float(np.clip((v - lo) / (hi - lo), 0, 1) * 100)


def band(v, lo, hi, scale):
    """100 inside [lo, hi], decaying exp(-distance/scale) outside."""
    if lo <= v <= hi:
        return 100.0
    d = lo - v if v < lo else v - hi
    return float(100 * np.exp(-d / scale))


# ── features ────────────────────────────────────────────────────────────────────────────────

def autocorr(o, maxlag):
    """np.correlate(o, o, 'full')[len(o) - 1:][:maxlag] by FFT: O(n log n). The direct form is O(n^2) and took 9
    minutes on chirper-one's 494 s outro (likeness.tempo 336 s, the rhythm term 197 s)."""
    n = len(o)
    m = 1 << int(np.ceil(np.log2(max(2, 2 * n))))
    f = np.fft.rfft(o, m)
    return np.fft.irfft(f * np.conj(f), m)[:min(maxlag, n)]


def tempo(onset, lo=60, hi=200):
    """likeness.tempo with the FFT autocorrelation (the same lags and argmax)."""
    o = onset - onset.mean()
    ac = autocorr(o, int(np.ceil(60 * L.FPS / lo)) + 2)
    lags = np.arange(len(ac))
    bpm = np.where(lags > 0, 60 * L.FPS / np.maximum(lags, 1), 0)
    ok = (bpm >= lo) & (bpm <= hi)
    return 60 * L.FPS / lags[ok][np.argmax(ac[ok])]


BAND_HZ = np.sqrt(np.geomspace(30, 16000, 41)[:-1] * np.geomspace(30, 16000, 41)[1:])   # likeness's 40 band centres


def worst_bands(mine, theirs, n=3):
    """The bands where MINE sticks out from THEIRS most: [(centre Hz, dB)] (chirper-one's join method)."""
    d = np.array(mine) - np.array(theirs)
    return [(int(round(BAND_HZ[i])), round(float(d[i]), 1)) for i in np.argsort(-np.abs(d))[:n]]


# Bands of likeness's 40 (30 Hz-16 kHz, log-spaced) that hold at least one FFT bin. At NFFT 4096 / 48 kHz (11.7 Hz bins)
# bands 0 (30-35 Hz) and 3 (48-56 Hz) are empty: they read a constant -100 dB floor in every profile, dragged its mean
# and added ~0.33 dB to every spectrum excess (chirper-zero, 30 Oct: Sodium's spectrum 86 would be ~96).
_BF = np.fft.rfftfreq(L.NFFT, 1 / L.SR)
_BE = np.geomspace(30, 16000, 41)
LIVE = np.array([bool(((_BF >= a) & (_BF < b)).any()) for a, b in zip(_BE[:-1], _BE[1:])])
PROFILE_V = 2   # bump when profile() changes, so cached genre envelopes are recomputed


def profile(F, i0=0, i1=None):
    """Level-normalised long-term spectrum (40 log bands, dB minus the mean of the bands that hold FFT bins; empty
    bands read 0 so they never differ between two profiles)."""
    p = F.logb[:, i0:i1].mean(1)
    out = p - p[LIVE].mean()
    out[~LIVE] = 0.0
    return out


NOVELTY = 0.15            # normalised checkerboard novelty a section boundary must reach (calibrated 28 Oct: real
                          # songs give 6-12 boundaries at 0.16, a looped bar none: its peak is 0.10)


def frames(F):
    """Per 0.5 s: z-scored spectral shape, chroma and level, each block weighted equally. Metal changes section by
    riff and level more than by spectrum (The Abysmal Eye's spectral novelty never passed 0.013)."""
    hop = int(L.FPS / 2)
    n = max(1, (F.n - hop) // hop)
    spec = np.stack([F.logb[:, i * hop:(i + 1) * hop].mean(1) for i in range(n)])
    spec = spec - spec.mean(1, keepdims=True)
    chro = np.stack([F.chroma[:, i * hop:(i + 1) * hop].mean(1) for i in range(n)])
    loud = np.array([F.logb[:, i * hop:(i + 1) * hop].mean() for i in range(n)])[:, None]

    def z(a):
        return (a - a.mean(0)) / (a.std(0) + 1e-9)
    return np.hstack([z(spec) / np.sqrt(spec.shape[1]), z(chro) / np.sqrt(12), z(loud)])


def novelty(X, half=16):
    """Checkerboard novelty on the frame self-similarity, normalised by the kernel's weight (so ~0 for static audio)."""
    from scipy import signal
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    S = Xn @ Xn.T
    k = np.ones((2 * half, 2 * half))
    k[:half, half:] = -1
    k[half:, :half] = -1
    k *= np.outer(signal.windows.hann(2 * half), signal.windows.hann(2 * half))
    k /= np.abs(k).sum()
    nov = np.zeros(len(S))
    for i in range(half, len(S) - half):
        nov[i] = (S[i - half:i + half, i - half:i + half] * k).sum()
    return nov


def section_bounds(F, dur, X=None, thr=None, nov=None):
    from scipy import signal
    if nov is None:
        X = frames(F) if X is None else X
        nov = novelty(X)
    pk, _ = signal.find_peaks(nov, height=NOVELTY if thr is None else thr, distance=16)
    cuts = [p / 2 for p in pk if 0 < p / 2 < dur]
    edges = [0.0] + cuts + [dur]
    return [(a, b) for a, b in zip(edges[:-1], edges[1:]) if b - a >= 1.0]


def novelty_thresholds(album):
    """The album's opt-in params.sections.novelty: one threshold, or a list scored as an ensemble (see ensemble()).
    None (the default) keeps the single NOVELTY cut."""
    v = (((album or {}).get("params") or {}).get("sections") or {}).get("novelty")
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return [float(v)]
    ths = sorted(float(t) for t in v)
    return ths or None


SECTION_TERMS = ("structure", "variety", "recurrence")


def ensemble(fn, ctx):
    """A form term averaged over the album's novelty-threshold ensemble, so a boundary whose novelty peak sits near the
    threshold counts fractionally. With one hard cut, texture-level changes near a boundary flip the section count and
    every form term with it (chirper-one, t3, 1 Nov: quieting the radio's static, or shortening its retune, moved
    the total 4-13 points via 7 -> 5 or 6 sections while the music hardly changed). The detail is the middle cut's,
    plus each cut's section count and score."""
    sets = ctx["section_sets"]
    runs = [fn({**ctx, "sections": secs}) for secs in sets]
    mid = runs[len(runs) // 2]
    if any(s is None for s, _ in runs):
        return mid
    d = dict(mid[1] or {})
    d["ensemble"] = {"novelty": ctx.get("novelty_thresholds"), "sections": [len(x) for x in sets],
                     "scores": [round(float(s), 2) for s, _ in runs]}
    return float(np.mean([s for s, _ in runs])), d


def section_feats(F, x, bounds, X=None):
    X = frames(F) if X is None else X
    out = []
    for a, b in bounds:
        i0, i1 = int(a * L.FPS), max(int(a * L.FPS) + 1, int(b * L.FPS))
        seg = x[int(a * L.SR):int(b * L.SR)]
        lvl = 10 * np.log10(float((seg.astype(float) ** 2).mean()) + 1e-12)
        on = F.onset[i0:i1]
        thr = np.percentile(F.onset, 75)
        dens = float(((on[1:-1] > on[:-2]) & (on[1:-1] >= on[2:]) & (on[1:-1] > thr)).sum()) / max(b - a, 1e-6)
        ch = F.chroma[:, i0:i1].mean(1)
        v = X[int(a * 2):max(int(a * 2) + 1, int(b * 2))].mean(0)
        out.append({"a": a, "b": b, "level": lvl, "profile": profile(F, i0, i1), "density": dens, "chroma": ch,
                    "vec": v})
    return out


def features(x, F, dur):
    """The per-song summary saved for the album terms."""
    n3 = int(3 * L.FPS)
    head, tail = x[:int(3 * L.SR)], x[-int(3 * L.SR):]
    lvl = lambda s: 10 * np.log10(float((s.astype(float) ** 2).mean()) + 1e-12)  # noqa: E731
    ch = F.chroma.mean(1)
    onsets = F.onset
    thr = np.percentile(onsets, 75)
    peaks = int(((onsets[1:-1] > onsets[:-2]) & (onsets[1:-1] >= onsets[2:]) & (onsets[1:-1] > thr)).sum())
    return {"dur": dur, "profile": profile(F).tolist(), "chroma": (ch / (ch.sum() + 1e-12)).tolist(),
            "tempo": float(tempo(F.onset)), "density": peaks / max(dur, 1e-6),
            "head": {"level": lvl(head), "profile": profile(F, 0, n3).tolist()},
            "tail": {"level": lvl(tail), "profile": profile(F, max(0, F.n - n3), None).tolist()}}


def window_feats(x, F, a, b):
    """Level and profile of seconds A..B of the render (the head/tail summary's shape)."""
    a, b = max(0.0, a), max(a + 0.1, b)
    s = x[int(a * L.SR):int(b * L.SR)]
    lvl = 10 * np.log10(float((s.astype(float) ** 2).mean()) + 1e-12) if len(s) else -120.0
    return {"level": lvl, "profile": profile(F, int(a * L.FPS), max(int(a * L.FPS) + 1, int(b * L.FPS))).tolist(),
            "at": round(a, 2)}


def mix_windows(me, x, F, album, slot, song, secs=3.0):
    """A mixtape album (compose/ALBUM/mixplan.md): add the bodies the listener hears either side of each crossfade,
    placed as the groove and release --mix place them. mix_head is SECS from this song's bar OVERLAP (its in-seam's
    crossfade done), mix_tail the SECS before its out-seam starts (the outgoing bar line OVERLAP bars before its last
    bar line, chirpers.seam_start). Other albums: unchanged (no keys added)."""
    n = (slot or {}).get("n")
    if not n or not os.path.exists(os.path.join(ROOT, "compose", album["id"], "mixplan.md")) or not os.path.exists(song):
        return
    import chirpers as CH
    try:
        pin = open(os.path.join(HERE, "groove-pin")).read().strip()
        tl = CH.song_timeline(pin, song)
        seams, default = CH.seam_overlaps(album["id"])
    except (OSError, ValueError, KeyError):
        return
    if not tl:
        return
    have = {t.get("n") for t in album.get("tracks", [])}
    if n - 1 in have:
        k = int(round(seams.get((n - 1, n), default) * 4))
        if k < len(tl["times"]):
            t0 = tl["times"][k]
            me["mix_head"] = dict(window_feats(x, F, t0, t0 + secs), bars=k / 4)
    if n + 1 in have:
        bars = seams.get((n, n + 1), default)
        t1 = CH.seam_start(tl, bars)
        me["mix_tail"] = dict(window_feats(x, F, t1 - secs, t1), bars=bars)


def others_features(album_id, cid):
    out = {}
    for p in glob.glob(os.path.join(cache_dir(album_id), "features", "*.json")):
        k = os.path.basename(p)[:-5]
        if k != cid:
            with open(p) as f:
                out[k] = json.load(f)
    return out


def genre_envelope(album):
    """The average level-normalised spectrum of the album's genre_refs (cached), or None."""
    refs = album.get("genre_refs") or []
    if not refs:
        return None
    path = os.path.join(cache_dir(album["id"]), "genre-envelope.json")
    if os.path.exists(path):
        with open(path) as f:
            d = json.load(f)
        if d.get("refs") == refs and d.get("v") == PROFILE_V:
            return np.array(d["envelope"])
    profs = []
    for r in refs:
        w = os.path.join(ROOT, "ref", f"{r}.wav")
        if os.path.exists(w):
            profs.append(profile(L.Feat(L.load(w))))
    if not profs:
        return None
    env = np.mean(profs, axis=0)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"refs": refs, "v": PROFILE_V, "envelope": env.tolist()}, f)
    return env


# ── measures ────────────────────────────────────────────────────────────────────────────────

def m_human(ctx):
    rs = [r for r in ctx["ratings"] if r.get("id") == ctx["id"] and r.get("who") == "harry" and "score" in r]  # notes skip
    if not rs:
        return None, {}
    r = rs[-1]
    stale = bool(r.get("version")) and r.get("version") != ctx.get("version")
    return 10.0 * float(r["score"]), {"rating": r["score"], "version": r.get("version"), "stale": stale,
                                      "note": r.get("note"), "weight_scale": 0.5 if stale else 1.0}


def m_peer(ctx):
    owner = ctx.get("owner")
    latest = {}
    for r in ctx["ratings"]:
        if r.get("id") == ctx["id"] and r.get("who") not in ("harry", owner, None) and "score" in r:
            latest[r["who"]] = float(r["score"])
    if not latest:
        return None, {}
    return 10.0 * float(np.mean(list(latest.values()))), {"raters": sorted(latest)}


def m_length(ctx):
    lo, hi = (ctx["slot"] or {}).get("length", [0, 1e9])
    return band(ctx["dur"], lo, hi, 30.0), {"dur": round(ctx["dur"], 1), "target": [lo, hi]}


def m_master(ctx):
    t = {**DEFAULT_MASTER, **(ctx["album"].get("master") or {})}
    x = ctx["x"].astype(float)
    rms = 10 * np.log10(float((x ** 2).mean()) + 1e-12)
    peak = 20 * np.log10(float(np.abs(x).max()) + 1e-12)
    crest = 20 * np.log10(float(np.percentile(np.abs(x), 99.9)) + 1e-9) - rms
    s = (band(rms, *t["rms"], 3.0) * (100.0 if peak <= t["peak_max"] + 0.01 else 60.0) / 100 * band(crest, *t["crest"], 3.0) / 100)
    return s, {"rms_db": round(rms, 2), "peak_db": round(peak, 2), "crest_db": round(crest, 2)}


def m_spectrum(ctx):
    env = ctx.get("envelope")
    if env is None:
        return None, {}
    ours = profile(ctx["F"])
    tol = float(ctx["album"].get("spectrum_tolerance_db", SPECTRUM_TOL))
    dev = np.maximum(0, np.abs(ours - env) - tol)
    w = int(np.argmax(np.abs(ours - env)))
    # worst_band_db is signed like worst_bands_hz_db (+ = this song louder than the album there): the worst band can be a
    # DEFICIT, e.g. a new mid layer makes loudness normalisation leave the bass short (chirper-three, t4 v32, 3 Nov)
    return float(100 * np.exp(-dev.mean() / 3.0)), {"mean_excess_db": round(float(dev.mean()), 2), "worst_band": w,
                                                    "worst_band_hz": int(round(BAND_HZ[w])),
                                                    "worst_band_db": round(float(ours[w] - env[w]), 1)}


def spectrum_bands(ctx):
    """Per live band: (Hz, ours - envelope dB, dB beyond tolerance, spectrum points if that band alone came within
    tolerance). The whole picture behind spectrum's worst_band, for fixing several bands from one render (3 Nov)."""
    env = ctx.get("envelope")
    if env is None:
        return []
    ours = profile(ctx["F"])
    tol = float(ctx["album"].get("spectrum_tolerance_db", SPECTRUM_TOL))
    diff = ours - env
    dev = np.maximum(0, np.abs(diff) - tol)
    now = 100 * np.exp(-dev.mean() / 3.0)
    out = []
    for i in np.flatnonzero(LIVE):
        gain = 100 * np.exp(-(dev.sum() - dev[i]) / len(dev) / 3.0) - now
        out.append((int(round(BAND_HZ[i])), round(float(diff[i]), 1), round(float(dev[i]), 1), round(float(gain), 2)))
    return out


def m_structure(ctx):
    secs, dur = ctx["sections"], ctx["dur"]
    n = len(secs)
    lo, hi = max(2.0, dur / 50.0), max(3.0, dur / 15.0)
    count = band(n, lo, hi, 2.0)
    lens = np.array([s["b"] - s["a"] for s in secs])
    cv = float(lens.std() / lens.mean()) if n > 1 else 0.0
    shape = band(cv, 0.2, 1.0, 0.3)   # records measure 0.36-0.93 (Combustion .91, Daydreaming .88, Pyramid .93); a 0.7
                                       # edge also flipped The Long Unwinding between seeds (one merged boundary: .66 vs .86)
    return 0.6 * count + 0.4 * shape, {"sections": n, "target": [round(lo, 1), round(hi, 1)], "length_cv": round(cv, 2)}


def m_variety(ctx):
    secs = ctx["sections"]
    if len(secs) < 2:
        return 0.0, {"sections": len(secs)}
    lv = np.array([s["level"] for s in secs])
    loud = ramp(lv.max() - lv.min(), 1.0, 6.0)
    profs = np.stack([s["profile"] for s in secs])
    d = [np.abs(profs[i] - profs[j]).mean() for i in range(len(secs)) for j in range(i + 1, len(secs))]
    timbre = ramp(float(np.mean(d)), 0.5, 2.5)
    dens = np.array([s["density"] for s in secs])
    dcv = float(dens.std() / (dens.mean() + 1e-9))
    rhythm = ramp(dcv, 0.03, 0.2)
    return (loud + timbre + rhythm) / 3, {"level_range_db": round(float(lv.max() - lv.min()), 1),
                                          "timbre_spread_db": round(float(np.mean(d)), 2), "density_cv": round(dcv, 2)}


def _sim(s, t):
    """Cosine of two sections' mean combined frames (spectral shape, chroma, level; z-scored within the song)."""
    a, b = s["vec"], t["vec"]
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


RETURN = (0.45, 0.75)     # a section's return strength ramps 0 -> 1 as its best match to an earlier non-adjacent
                          # section goes 0.45 -> 0.75. A hard 0.6 cut flipped Seed Crystal between seeds (one section
                          # matched 0.62 on seed 0, 0.598 on seed 11: recurrence 57.4 vs 18.9, total 88.1 vs 82.6)


def m_recurrence(ctx):
    secs = ctx["sections"]
    if len(secs) < 3:
        return 30.0, {"sections": len(secs)}
    best = [max(_sim(secs[i], secs[j]) for j in range(0, i - 1)) for i in range(2, len(secs))]
    frac = float(np.mean([np.clip((b - RETURN[0]) / (RETURN[1] - RETURN[0]), 0, 1) for b in best]))
    # the band of returning material is the album's to tune (Harry, 30 Oct: the metric is the composers'): a slow
    # post-rock crescendo is cut into many similar sections, so it can want a higher ceiling than 0.7
    lo, hi = (((ctx.get("album") or {}).get("params") or {}).get("recurrence") or {}).get("band", (0.25, 0.7))
    return band(frac, float(lo), float(hi), 0.15), {"returns": sum(b >= 0.6 for b in best), "of": len(best),
                                                    "share": round(frac, 3), "best_matches": [round(b, 2) for b in best]}


def fine_onset(x, hop):
    """Spectral-flux onsets (40 log bands, 30 Hz-16 kHz) at HOP samples: the rhythm term's opt-in finer grid."""
    from scipy import signal
    m = x.mean(axis=1) if x.ndim > 1 else x
    nfft = max(4 * hop, 512)
    f, _, Z = signal.stft(m, L.SR, nperseg=nfft, noverlap=nfft - hop, boundary=None, padded=False)
    mag = np.abs(Z)
    edges = np.geomspace(30, 16000, 41)
    b = np.stack([(mag[(f >= a) & (f < c)] ** 2).sum(0) for a, c in zip(edges[:-1], edges[1:])]) + 1e-10
    return np.concatenate([[0], np.maximum(np.diff(10 * np.log10(b), axis=1), 0).sum(0)])


def m_rhythm(ctx):
    # the album's params.rhythm (the composers' to set, Harry 30 Oct): `hop` (samples; default the 1024 feature hop,
    # 46.9 frames/s, where a 16th at house tempo is ~6 frames), `grid` (divisions of the beat counted ON the grid:
    # 2 = eighths, the default; 4 = 16ths) and `band` (the off-grid share's target, default 0.1..0.6). On a clean
    # 120 bpm kick + 16th-hat loop the default reads straight 16ths as off-grid (0.39) and swing as LESS off-grid
    # (0.10 at 20%, 0.01 at 50%); {hop: 256, grid: 4} reads 0.00 / 0.00 / 0.09 / 0.13 at 0 / 20 / 33 / 50% swing.
    # `map: true` reads a tempo-mapped song in beat time (see below). It is honest about ramps both ways: chirpers8-t12 v8's
    # 112 -> 126 accelerando reads off-grid 0.10 on one 121 grid (the ramp's smear) and 0.00 in beat time (rhythm 96.7 -> 56.0)
    rp = ((ctx.get("album") or {}).get("params") or {}).get("rhythm") or {}
    hop, div = int(rp.get("hop") or L.HOP), float(rp.get("grid") or 2)
    if hop == L.HOP:
        on, fps = ctx["F"].onset, L.FPS
    else:
        on, fps = fine_onset(ctx["x"], hop), L.SR / hop
    # `map: true` (opt-in): read the onsets in beat time on the song's tempo map, so a ramp's pulse sits on one grid.
    # Without it the grid is the map's median point BPM, which an extra point can move (chirper-three, 1 Nov: one
    # 121 point moved t12's grid 121 -> 123 and its accelerando read metronomic, -3.8)
    warped = bool(rp.get("map")) and bool(ctx.get("tempo_map")) and bool(ctx.get("bpm"))
    if warped:
        on = warp_onset(on, fps, ctx["tempo_map"], float(ctx["bpm"]))
    o = on - on.mean()
    ac = autocorr(o, int(4 * fps) + 2)
    ac = ac / (ac[0] + 1e-12)
    lags = np.arange(2, min(len(ac) - 1, int(4 * fps)))
    # every positive local maximum, weighted by its squared height: no cutoff. A fixed 0.15 cut made the term depend on
    # global normalisation: chirper-two's silent stop-starts in Splinterwork (sparse loud hits) shrank every peak,
    # the off-grid ones fell under 0.15 and rhythm went 100 -> 45; Pyramid Song (top peak 0.17) scored 17.
    pk = lags[(ac[lags] > ac[lags - 1]) & (ac[lags] >= ac[lags + 1]) & (ac[lags] > 0)]
    if len(pk) == 0:
        return 0.0, {}
    # the pulse: the song's declared tempo when we have it; else the strongest autocorrelation peak between 0.25 and
    # 1.2 s (a tempo estimate's rounding would make every multiple drift off-grid: a looped 120 BPM bar read 122)
    beat = [k for k in pk if 0.25 * fps <= k <= 1.2 * fps] or list(pk)
    est = 60 * fps / float(max(beat, key=lambda k: ac[k]))
    bpm = float(ctx.get("bpm") or est)
    P = 60 * fps / bpm
    grid = P / div
    tol = 1.5 * fps / L.FPS
    off = [k for k in pk if min(k % grid, grid - k % grid) > max(tol, 0.04 * k)]
    share = float(sum(ac[k] ** 2 for k in off) / sum(ac[k] ** 2 for k in pk))
    dens = ctx["density"]
    lo, hi = rp.get("band") or (0.1, 0.6)
    return 0.7 * band(share, float(lo), float(hi), 0.1) + 0.3 * band(dens, 1.5, 10.0, 2.0), {
        "tempo": round(bpm, 1), "declared": bool(ctx.get("bpm")), "pulse_estimate": round(est, 1),
        "offgrid_share": round(share, 2), "onsets_per_s": round(dens, 2), **({"tempo_map": True} if warped else {})}


def m_cohesion(ctx):
    oth = ctx["others"]
    if not oth:
        return None, {}
    mean = np.mean([np.array(v["profile"]) for v in oth.values()], axis=0)
    d = float(np.abs(profile(ctx["F"]) - mean).mean())
    return band(d, 0.0, 3.0, 3.0), {"from_album_db": round(d, 2), "songs": len(oth)}


def distinct_tempo(cid, feats, bpm=None):
    """A song's tempo for `distinct`: its declared tempo (BPM, a map's median) when it has one, else the onset
    autocorrelation estimate. The estimate has near-equal peaks on these songs and a coarse lag grid: Accretion's t2 read
    187.5 for a declared 90, and t8 flipped 156 -> 87.9 when its sixteenth-note ostinatos dropped out, landing on t4's
    exact estimate, so distinct read t8 as a 0.956 copy of t4 (29.5) (chirper-three, 8 Nov). Others' declared tempos
    are read from their song files at comparison time, so stale caches don't matter."""
    if bpm:
        return float(bpm)
    if feats.get("bpm"):
        return float(feats["bpm"])
    for ext in ("yaml", "json"):
        p = os.path.join(ROOT, "songs", f"{cid}.{ext}")
        if os.path.exists(p):
            t = declared_tempo(p)
            if t:
                return t
    return float(feats["tempo"])


def m_distinct(ctx):
    oth = ctx["others"]
    if not oth:
        return None, {}
    me = ctx["me"]
    mt = distinct_tempo(ctx.get("id"), me, ctx.get("bpm"))
    worst, who = 0.0, None
    for k, v in oth.items():
        c = max(0.0, L._cos(np.array(me["chroma"]) - 1 / 12, np.array(v["chroma"]) - 1 / 12))
        t = float(np.exp(-abs(np.log2(mt / distinct_tempo(k, v))) * 12))
        d = float(np.exp(-abs(me["density"] - v["density"]) / 1.0))
        s = (c + t + d) / 3
        if s > worst:
            worst, who = s, k
    return float(100 * np.clip((1 - worst) / 0.15, 0, 1)), {"closest": who, "similarity": round(worst, 3)}


def m_flow(ctx):
    if ctx["album"].get("bleed") is False:
        # The album says its songs do not bleed into one another, so there is no join to keep level across. (14 Nov:
        # Common Time's second song starts at once after the epic's quiet ending, 35 dB up, as written; the term read
        # 11.4 for BOTH songs and took 4.0 points off the epic, 100.00 to 96.03 on the same audio, the moment the
        # second song existed.)
        return None, {"skipped": 'the album says "bleed": false'}
    oth, slot, tracks = ctx["others"], ctx["slot"] or {}, ctx["album"].get("tracks", [])
    n = slot.get("n")
    joins, scores = {}, []
    for side, nb in (("in", n - 1 if n else None), ("out", n + 1 if n else None)):
        t = next((t for t in tracks if t.get("n") == nb), None)
        if not t or t["id"] not in oth:
            continue
        mine = ctx["me"]["head" if side == "in" else "tail"]
        theirs = oth[t["id"]]["tail" if side == "in" else "head"]
        how = None
        mk_mine, mk_theirs = ("mix_head", "mix_tail") if side == "in" else ("mix_tail", "mix_head")
        if mk_mine in ctx["me"]:      # a mixtape seam: the bodies either side of the crossfade, not the faded ends
            if mk_theirs in oth[t["id"]]:
                mine, theirs = ctx["me"][mk_mine], oth[t["id"]][mk_theirs]
                how = f"mix: bodies either side of the {mine.get('bars', 0):g}-bar crossfade"
            else:
                how = f"back to back: {t['id']}'s saved features predate the mix windows (re-score it with --save)"
        jump = abs(mine["level"] - theirs["level"])
        spec = float(np.abs(np.array(mine["profile"]) - np.array(theirs["profile"])).mean())
        # graded far out (chirper-two: at a 4 dB decay a 14 dB join and a 23 dB one both scored ~0, so join work had
        # no gradient). For scale: obZen's real joins jump 35-77 dB (its tracks decay to silence), spectra 5-8 dB.
        s = 0.5 * band(jump, 0, 6.0, 12.0) + 0.5 * band(spec, 0, 3.0, 3.0)
        joins[side] = {"with": t["id"], "level_jump_db": round(jump, 1), "spectral_db": round(spec, 2),
                       "worst_bands_hz_db": worst_bands(mine["profile"], theirs["profile"])}   # + = this song louder
        if how:
            joins[side]["measured"] = how
        scores.append(s)
    if not scores:
        return None, {}
    return float(np.mean(scores)), joins


BUILTIN = {"human": m_human, "peer": m_peer, "structure": m_structure, "variety": m_variety,
           "recurrence": m_recurrence, "rhythm": m_rhythm, "spectrum": m_spectrum, "master": m_master,
           "length": m_length, "cohesion": m_cohesion, "distinct": m_distinct, "flow": m_flow}


def plugins():
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "compose", "measures", "*.py"))):
        name = os.path.basename(p)[:-3]
        spec = importlib.util.spec_from_file_location(f"compmeasure_{name}", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "measure"):
            out[name] = mod.measure
    return out


# ── scoring ─────────────────────────────────────────────────────────────────────────────────

def raw_tempo(song):
    """The song file's top-level tempo as written: a number (or numeric string), a tempo map (a list of points) or
    None. A JSON song's `tempo`; a YAML song's top-level `tempo:` line (generator-written songs use YAML songfmt's
    restricted parser rejects). Raises on an unreadable file."""
    with open(song) as f:
        text = f.read()
    if text.lstrip().startswith("{"):
        return json.loads(text).get("tempo")
    m = re.search(r"^tempo:\s*([0-9.]+)\s*(?:#.*)?$", text, re.M)
    t = m.group(1) if m else None
    if t is None:
        # a tempo MAP: a flow list on the tempo: line, or a block list below it (until the next top-level key)
        m = re.search(r"^tempo:[ \t]*(\[.*\])[ \t]*$", text, re.M)
        if m:
            t = json.loads(m.group(1))
        else:
            m = re.search(r"^tempo:[ \t]*\n((?:[ \t-].*\n?)+)", text, re.M)
            t = [{"bpm": b} for b in re.findall(r"\bbpm:\s*([0-9.]+)", m.group(1))] if m else None
    return t


def tempo_points(song):
    """The song's tempo map as [(beat, bpm, ramp)], sorted as the engine sorts it (stable, by beat; a point at beat 0
    added when the first is later), when the map changes tempo and every position is in beats (`"64b"` or a number);
    else None: a single tempo, a constant map, positions in bars or seconds, a block map without positions, an
    unreadable file. A point with no bpm holds the previous point's (a meter change)."""
    try:
        t = raw_tempo(song)
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    if not isinstance(t, list) or not t:
        return None
    pts, prev = [], None
    for p in t:
        if not isinstance(p, dict):
            return None
        at = p.get("at", 0)
        m = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*b?\s*", at) if isinstance(at, str) else None
        if isinstance(at, (int, float)) and not isinstance(at, bool):
            beat = float(at)
        elif m:
            beat = float(m.group(1))
        else:
            return None
        try:
            bpm = float(p["bpm"]) if p.get("bpm") is not None else prev
        except (TypeError, ValueError):
            return None
        if bpm is None or not 1.0 <= bpm <= 1000.0:
            return None
        pts.append((beat, bpm, bool(p.get("ramp")) and p.get("bpm") is not None))
        prev = bpm
    pts.sort(key=lambda q: q[0])
    if pts[0][0] > 0:
        pts.insert(0, (0.0, pts[0][1], False))
    if len({b for _, b, _ in pts}) < 2:
        return None
    return pts


def tempo_segments(pts):
    """The engine's tempo segments for POINTS (chirp-core tempo.rs): arrays b0, t0, bpm0, k (BPM change per beat;
    a segment ramps when the NEXT point ramps and lies later)."""
    b0, t0, v0, k = [], [], [], []
    for i, (b, bpm, _) in enumerate(pts):
        nxt = pts[i + 1] if i + 1 < len(pts) else None
        kk = (nxt[1] - bpm) / (nxt[0] - b) if nxt and nxt[2] and nxt[0] > b else 0.0
        t = 0.0 if not b0 else t0[-1] + _seg_secs(v0[-1], k[-1], b - b0[-1])
        b0.append(b)
        t0.append(t)
        v0.append(bpm)
        k.append(kk)
    return np.array(b0), np.array(t0), np.array(v0), np.array(k)


def _seg_secs(bpm0, k, db):
    db = np.asarray(db, dtype=float)
    k = np.asarray(k, dtype=float)
    flat = np.abs(k) < 1e-12
    ks = np.where(flat, 1.0, k)
    ramp = 60.0 / ks * np.log(np.maximum((bpm0 + ks * db) / bpm0, 1e-9))
    return np.where(flat, db * 60.0 / bpm0, ramp)


def map_secs(segs, beats):
    """Seconds at BEATS (an array) on the tempo map SEGS."""
    b0, t0, v0, k = segs
    i = np.clip(np.searchsorted(b0, beats, side="right") - 1, 0, len(b0) - 1)
    return t0[i] + _seg_secs(v0[i], k[i], np.asarray(beats, dtype=float) - b0[i])


def map_beats(segs, secs):
    """Beats at SECS (a scalar) on the tempo map SEGS."""
    b0, t0, v0, k = segs
    i = int(np.clip(np.searchsorted(t0, secs, side="right") - 1, 0, len(b0) - 1))
    dt = secs - t0[i]
    if abs(k[i]) < 1e-12:
        return float(b0[i] + dt * v0[i] / 60.0)
    return float(b0[i] + v0[i] * (np.exp(k[i] * dt / 60.0) - 1.0) / k[i])


def warp_onset(on, fps, pts, ref):
    """The onset curve ON (frames at FPS) resampled into beat time on the tempo map PTS: REF bpm's frames per beat,
    so a beat lasts the same number of frames everywhere and a ramp's pulse sits on one grid."""
    segs = tempo_segments(pts)
    r = fps * 60.0 / ref
    total = map_beats(segs, len(on) / fps)
    beats = np.arange(int(total * r)) / r
    return np.interp(map_secs(segs, beats) * fps, np.arange(len(on)), on)


def declared_tempo(song):
    """The song file's top-level tempo (BPM), or None: see raw_tempo."""
    try:
        t = raw_tempo(song)
        if isinstance(t, list):
            # a map's points (ramps inside a track, as The Endless Stair's mix plan asks): the median BPM. Without
            # this every mapped song fell back to the autocorrelation estimate, and one landing on half tempo had its
            # eighth off-beats read as off-grid (chirper-zero, 31 Oct: t15 and t16 read rhythm 100 that way)
            b = [float(p["bpm"]) for p in t if isinstance(p, dict) and p.get("bpm") is not None]
            return float(np.median(b)) if b else None
        return float(t) if t else None
    except (OSError, ValueError, TypeError, AttributeError):
        return None


def music_end(x, sr, floor_db=-60.0, win=0.1):
    """Seconds to the end of the last 100 ms window above FLOOR_DB (dBFS RMS): where the music stops. A tapestop on
    the last bar leaves seconds of digital silence, which section_bounds read as a section of its own (chirper-zero:
    Window Seat's brake moved recurrence 74-79 -> 100 and the total 92.25 -> 96.65, 29 Oct). The full length still
    counts for length, master and the album joins: on the record the silence is there."""
    n = int(win * sr)
    if n <= 0 or len(x) < n:
        return len(x) / sr
    m = x.astype(float).mean(1) if x.ndim > 1 else x.astype(float)
    k = len(m) // n
    rms = np.sqrt((m[:k * n].reshape(k, n) ** 2).mean(1))
    loud = np.nonzero(20 * np.log10(rms + 1e-12) > floor_db)[0]
    return len(x) / sr if not len(loud) else min(len(x) / sr, (loud[-1] + 1) * win)


def build_ctx(cid, wav, climb, album, song=None):
    x = L.load(wav)
    F = L.Feat(x)
    dur = len(x) / L.SR
    slot = next((t for t in album.get("tracks", []) if t.get("id") == cid), None)
    X = frames(F)
    end, ths, sets = music_end(x, L.SR), novelty_thresholds(album), None
    if ths is None:
        secs = section_feats(F, x, section_bounds(F, end, X), X)
    else:
        nov = novelty(X)
        sets = [section_feats(F, x, section_bounds(F, end, X, thr=t, nov=nov), X) for t in ths]
        secs = sets[len(sets) // 2]
    me = features(x, F, dur)
    me["bpm"] = declared_tempo(song or os.path.join(ROOT, climb.get("song") or f"songs/{cid}.yaml"))
    mix_windows(me, x, F, album, slot, song or os.path.join(ROOT, climb.get("song") or f"songs/{cid}.yaml"))
    return {"id": cid, "wav": wav, "x": x, "F": F, "dur": dur, "album": album, "slot": slot, "sections": secs,
            "section_sets": sets, "novelty_thresholds": ths,
            "me": me, "density": me["density"], "others": others_features(album["id"], cid),
            "ratings": ratings(album["id"]), "owner": climb.get("owner"),
            "version": (climb.get("best") or {}).get("version"), "envelope": genre_envelope(album),
            "bpm": declared_tempo(song or os.path.join(ROOT, climb.get("song") or f"songs/{cid}.yaml")),
            "tempo_map": tempo_points(song or os.path.join(ROOT, climb.get("song") or f"songs/{cid}.yaml"))}


def score(ctx, extra=None):
    weights = {**DEFAULT_WEIGHTS, **(ctx["album"].get("weights") or {})}
    terms, detail, used = {}, {}, {}
    for name, fn in {**BUILTIN, **(extra or {})}.items():
        s, d = ensemble(fn, ctx) if name in SECTION_TERMS and len(ctx.get("section_sets") or []) > 1 else fn(ctx)
        detail[name] = d
        if s is None:
            continue
        w = float(weights.get(name, 0.05)) * float((d or {}).get("weight_scale", 1.0))
        if w <= 0:
            continue
        terms[name] = round(float(s), 2)
        used[name] = w
    tot = sum(used[k] * terms[k] for k in used) / sum(used.values()) if used else 0.0
    return {"total": round(tot, 3), "terms": terms, "weights": {k: round(v, 3) for k, v in used.items()},
            "detail": detail}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("wav")
    ap.add_argument("--save", action="store_true", help="store this render's features for the album terms")
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--song", help="the song file the render came from (default: the climb's song)")
    ap.add_argument("--bands", action="store_true", help="print spectrum's per-band picture: signed dB vs the album "
                    "envelope (+ = louder), dB beyond tolerance, and the points fixing each band alone would give")
    a = ap.parse_args(argv)
    climb = climb_of(a.id)
    album_id = climb.get("album") or (climb.get("compose") or {}).get("album")
    if not album_id:
        raise SystemExit(f"compscore: {a.id} is not a composition (no album id)")
    album = load_album(album_id)
    ctx = build_ctx(a.id, a.wav, climb, album, a.song)
    res = score(ctx, plugins())
    if a.save:
        d = os.path.join(cache_dir(album_id), "features")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f"{a.id}.json"), "w") as f:
            json.dump(ctx["me"], f)
    if a.bands:
        w = res["weights"].get("spectrum", 0.0)
        print(f"{a.id}: total {res['total']:.2f}, spectrum {res['terms'].get('spectrum', float('nan')):.1f} (w {w:.3f}); "
              "bands vs the album envelope (+ = louder)")
        print("      Hz   dB vs env  beyond tol  fix alone: spectrum / total")
        for hz, d, over, gain in spectrum_bands(ctx):
            bar = ("+" if d > 0 else "-") * min(20, int(round(abs(d))))
            fix = f"+{gain:.2f} / +{gain * w:.2f}" if over > 0 else ""
            print(f"  {hz:6d}  {d:+8.1f}  {over:9.1f}   {fix:20s} {bar}")
        return
    if a.text:
        print(f"{a.id}: total {res['total']:.2f}")
        for k, v in sorted(res["terms"].items(), key=lambda kv: -res["weights"][kv[0]]):
            print(f"  {k:10s} {v:6.1f}  (w {res['weights'][k]:.3f})  {json.dumps(res['detail'].get(k), default=float)[:110]}")
        for k, d in sorted(res["detail"].items()):   # detail-only terms (a plugin awaiting a weight): shown, not counted
            if k not in res["terms"] and d and d.get("score") is not None:
                print(f"  {k:10s} {float(d['score']):6.1f}  (detail only)  {json.dumps(d, default=float)[:110]}")
        return
    print(json.dumps(res, default=float))


if __name__ == "__main__":
    main()
