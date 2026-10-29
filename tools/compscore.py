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
  distinct   not a near-copy of another album song (pitch-class histogram, tempo, density).
  flow       the bleed into and out of the neighbouring tracks: level and spectrum continuity at the joins.
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


def profile(F, i0=0, i1=None):
    """Level-normalised long-term spectrum (40 log bands, dB minus their mean)."""
    p = F.logb[:, i0:i1].mean(1)
    return p - p.mean()


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


def section_bounds(F, dur, X=None):
    from scipy import signal
    X = frames(F) if X is None else X
    pk, _ = signal.find_peaks(novelty(X), height=NOVELTY, distance=16)
    cuts = [p / 2 for p in pk if 0 < p / 2 < dur]
    edges = [0.0] + cuts + [dur]
    return [(a, b) for a, b in zip(edges[:-1], edges[1:]) if b - a >= 1.0]


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
        if d.get("refs") == refs:
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
        json.dump({"refs": refs, "envelope": env.tolist()}, f)
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
    return float(100 * np.exp(-dev.mean() / 3.0)), {"mean_excess_db": round(float(dev.mean()), 2),
                                                    "worst_band": int(np.argmax(np.abs(ours - env)))}


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
    return band(frac, 0.25, 0.7, 0.15), {"returns": sum(b >= 0.6 for b in best), "of": len(best), "share": round(frac, 3),
                                         "best_matches": [round(b, 2) for b in best]}


def m_rhythm(ctx):
    F = ctx["F"]
    o = F.onset - F.onset.mean()
    ac = autocorr(o, int(4 * L.FPS) + 2)
    ac = ac / (ac[0] + 1e-12)
    lags = np.arange(2, min(len(ac) - 1, int(4 * L.FPS)))
    # every positive local maximum, weighted by its squared height: no cutoff. A fixed 0.15 cut made the term depend on
    # global normalisation: chirper-two's silent stop-starts in Splinterwork (sparse loud hits) shrank every peak,
    # the off-grid ones fell under 0.15 and rhythm went 100 -> 45; Pyramid Song (top peak 0.17) scored 17.
    pk = lags[(ac[lags] > ac[lags - 1]) & (ac[lags] >= ac[lags + 1]) & (ac[lags] > 0)]
    if len(pk) == 0:
        return 0.0, {}
    # the pulse: the song's declared tempo when we have it; else the strongest autocorrelation peak between 0.25 and
    # 1.2 s (a tempo estimate's rounding would make every multiple drift off-grid: a looped 120 BPM bar read 122)
    beat = [k for k in pk if 0.25 * L.FPS <= k <= 1.2 * L.FPS] or list(pk)
    est = 60 * L.FPS / float(max(beat, key=lambda k: ac[k]))
    bpm = float(ctx.get("bpm") or est)
    P = 60 * L.FPS / bpm
    grid = P / 2
    off = [k for k in pk if min(k % grid, grid - k % grid) > max(1.5, 0.04 * k)]
    share = float(sum(ac[k] ** 2 for k in off) / sum(ac[k] ** 2 for k in pk))
    dens = ctx["density"]
    return 0.7 * band(share, 0.1, 0.6, 0.1) + 0.3 * band(dens, 1.5, 10.0, 2.0), {
        "tempo": round(bpm, 1), "declared": bool(ctx.get("bpm")), "pulse_estimate": round(est, 1),
        "offgrid_share": round(share, 2), "onsets_per_s": round(dens, 2)}


def m_cohesion(ctx):
    oth = ctx["others"]
    if not oth:
        return None, {}
    mean = np.mean([np.array(v["profile"]) for v in oth.values()], axis=0)
    d = float(np.abs(profile(ctx["F"]) - mean).mean())
    return band(d, 0.0, 3.0, 3.0), {"from_album_db": round(d, 2), "songs": len(oth)}


def m_distinct(ctx):
    oth = ctx["others"]
    if not oth:
        return None, {}
    me = ctx["me"]
    worst, who = 0.0, None
    for k, v in oth.items():
        c = max(0.0, L._cos(np.array(me["chroma"]) - 1 / 12, np.array(v["chroma"]) - 1 / 12))
        t = float(np.exp(-abs(np.log2(me["tempo"] / v["tempo"])) * 12))
        d = float(np.exp(-abs(me["density"] - v["density"]) / 1.0))
        s = (c + t + d) / 3
        if s > worst:
            worst, who = s, k
    return float(100 * np.clip((1 - worst) / 0.15, 0, 1)), {"closest": who, "similarity": round(worst, 3)}


def m_flow(ctx):
    oth, slot, tracks = ctx["others"], ctx["slot"] or {}, ctx["album"].get("tracks", [])
    n = slot.get("n")
    joins, scores = {}, []
    for side, nb in (("in", n - 1 if n else None), ("out", n + 1 if n else None)):
        t = next((t for t in tracks if t.get("n") == nb), None)
        if not t or t["id"] not in oth:
            continue
        mine = ctx["me"]["head" if side == "in" else "tail"]
        theirs = oth[t["id"]]["tail" if side == "in" else "head"]
        jump = abs(mine["level"] - theirs["level"])
        spec = float(np.abs(np.array(mine["profile"]) - np.array(theirs["profile"])).mean())
        # graded far out (chirper-two: at a 4 dB decay a 14 dB join and a 23 dB one both scored ~0, so join work had
        # no gradient). For scale: obZen's real joins jump 35-77 dB (its tracks decay to silence), spectra 5-8 dB.
        s = 0.5 * band(jump, 0, 6.0, 12.0) + 0.5 * band(spec, 0, 3.0, 3.0)
        joins[side] = {"with": t["id"], "level_jump_db": round(jump, 1), "spectral_db": round(spec, 2),
                       "worst_bands_hz_db": worst_bands(mine["profile"], theirs["profile"])}   # + = this song louder
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

def declared_tempo(song):
    """The song file's top-level tempo (BPM), or None. A JSON song's `tempo`; a YAML song's top-level `tempo:` line
    (generator-written songs use YAML songfmt's restricted parser rejects)."""
    try:
        with open(song) as f:
            text = f.read()
        if text.lstrip().startswith("{"):
            t = json.loads(text).get("tempo")
        else:
            m = re.search(r"^tempo:\s*([0-9.]+)\s*(?:#.*)?$", text, re.M)
            t = m.group(1) if m else None
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
    secs = section_feats(F, x, section_bounds(F, music_end(x, L.SR), X), X)
    me = features(x, F, dur)
    return {"id": cid, "wav": wav, "x": x, "F": F, "dur": dur, "album": album, "slot": slot, "sections": secs,
            "me": me, "density": me["density"], "others": others_features(album["id"], cid),
            "ratings": ratings(album["id"]), "owner": climb.get("owner"),
            "version": (climb.get("best") or {}).get("version"), "envelope": genre_envelope(album),
            "bpm": declared_tempo(song or os.path.join(ROOT, climb.get("song") or f"songs/{cid}.yaml"))}


def score(ctx, extra=None):
    weights = {**DEFAULT_WEIGHTS, **(ctx["album"].get("weights") or {})}
    terms, detail, used = {}, {}, {}
    for name, fn in {**BUILTIN, **(extra or {})}.items():
        s, d = fn(ctx)
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
