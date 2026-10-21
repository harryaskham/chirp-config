#!/usr/bin/env python3
"""griddrums: program drum parts on the record's beat grid from its drum stem, and check the result the way the
rhythm term hears it (chirper-zero's Hedphelym r12 programmer, made a tool).

  griddrums.py fit DRUMS.wav [--bpm 70-180] [--prefer 120] [--from A --to B]
      the 16th-note grid: BPM and T0 (a sixteenth the kick favours, so pattern slots are counted from it), comb-fitted
      to the stem's onsets (constant tempo), with the share of strong onsets within 20 ms of the grid as a confidence;
      grids that fit equally (straight eighths fit 60, 120 and 180) are decided by --prefer (narrow --bpm to be sure)
  griddrums.py program SONG DRUMS.wav SECTIONS.txt --bpm X --t0 Y -o OUT [--parts low:k:drums-kick,hi:h:drums-hats]
                       [--bands low=40-120,mid=150-1500,hi=5000-12000] [--on 3.5] [--contrast 3] [--drop 12] [--level-gap 18]
                       [--from A --to B] [--replace] [--patch KIT] [--force 'SECSTART=0.8;…']
      per band and section, the 16 slots' mean onset strengths pick the pattern (slots within --on dB of the strongest;
      a section whose slots differ by less than --contrast dB gets no hits; a slot more than --level-gap dB quieter
      than the section's loudest is bleed, not a part); every bar plays it, each hit's velocity
      from its own band level (2.5 dB per 0.1 around the section median), hits more than --drop dB under the median
      left out. PART = band:piece:track. --replace swaps the track's notes inside [from, to); otherwise a new track
      (TRACK, or TRACK-grid when it exists) on --patch or the song's first drums-* track's patch. Notes tracks only.
  griddrums.py fold REF.wav OURS.wav SECTIONS.txt --bpm X --t0 Y
      per section, the bar-folded (16 slots) onset envelope likeness's rhythm term uses (spectral flux, smoothed
      ±50 ms) for the record and for our render, as 0-9 strengths, with their correlation: a pattern the stem shows
      but the mix does not (or a gallop the mix gains) shows here before it costs the rhythm term.

The fit assumes a constant tempo (drum machines); check it with fold on the stem itself before programming.
"""
import json
import os
import sys
import tempfile

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402
import songfmt  # noqa: E402

SR = L.SR
FS = 1000                      # onset envelope rate for the grid fit and the programmer
BANDS = {"low": (40, 120), "mid": (150, 1500), "hi": (5000, 12000)}


def band_flux(x, lo, hi):
    """Positive flux of x's lo-hi band energy, cube-root compressed and normalised (a quiet event counts little,
    unlike a dB derivative, which turns filter ringing in a silent band into onsets)."""
    sos = signal.butter(4, [lo, min(hi, SR / 2 - 100)], "bandpass", fs=SR, output="sos")
    h = signal.sosfilt(sos, x)                       # causal: no pre-ringing before an onset
    cs = np.concatenate([[0.0], np.cumsum(h ** 2)])
    w = 240
    c = ((cs[w:] - cs[:-w])[::SR // FS] / w) ** (1 / 3)
    d = np.concatenate([[0.0], np.maximum(np.diff(c), 0)])
    return d / (d.max() + 1e-20)


def band_env(x, lo, hi):
    """(level dB, positive dB derivative) of x's lo-hi band at FS (5 ms energy windows)."""
    sos = signal.butter(4, [lo, min(hi, SR / 2 - 100)], "bandpass", fs=SR, output="sos")
    h = signal.sosfiltfilt(sos, x)
    cs = np.concatenate([[0.0], np.cumsum(h ** 2)])
    w = 240
    e = (cs[w:] - cs[:-w])[::SR // FS] / w
    e = np.maximum(e, e.max() * 1e-6 + 1e-20)   # a floor 60 dB under the band's peak: near-silence has no onsets
    edb = 10 * np.log10(e)
    return edb, np.concatenate([[0.0], np.maximum(np.diff(edb), 0)])


def grid_score(times, six, tol=0.020):
    """(chance-corrected share of onset times within tol of the best-phased grid of spacing six, that phase)."""
    ph = times % six
    bins = max(8, int(round(six / 0.002)))
    h = np.bincount((ph / six * bins).astype(int) % bins, minlength=bins)
    w = max(1, int(round(tol / six * bins)))
    win = np.convolve(np.concatenate([h[-w:], h, h[:w]]), np.ones(2 * w + 1), "valid")
    i = int(np.argmax(win))
    share = win[i] / len(times)
    chance = min(1.0, 2 * tol / six)
    return (share - chance) / (1 - chance + 1e-9), (i + 0.5) / bins * six


def fit(x, lo_bpm=70, hi_bpm=180, t0=None, t1=None, prefer=120.0):
    a, b = int((t0 or 0) * SR), int(t1 * SR) if t1 else len(x)
    seg = x[a:b]
    envs = {name: band_env(seg, *rng) for name, rng in BANDS.items()}
    onset = sum(band_flux(seg, *rng) for rng in BANDS.values())
    pk, _ = signal.find_peaks(onset, height=np.percentile(onset, 98), distance=int(0.05 * FS))
    times = pk / FS
    if len(times) < 16:
        raise SystemExit("griddrums: too few onsets in the stem to fit a grid")
    # coarse: every tempo; grids that fit the onsets equally well (60/120/180 for straight eighths) are told apart by
    # a prior — the one nearest --prefer (log scale) among those within 0.02 of the best
    coarse = [(grid_score(times, 60 / bpm / 4), bpm) for bpm in np.arange(lo_bpm, hi_bpm + 0.025, 0.05)]
    top = max(sc for (sc, _), _ in coarse)
    (sc0, ph0), bpm0 = min(((g, b) for g, b in coarse if g[0] >= top - 0.02), key=lambda gb: abs(np.log(gb[1] / prefer)))
    best = (sc0, bpm0, ph0)
    for step, span in ((0.005, 0.1), (0.0005, 0.01)):
        for bpm in np.arange(best[1] - span, best[1] + span, step):
            sc, ph = grid_score(times, 60 / bpm / 4)
            if sc > best[0]:
                best = (sc, bpm, ph)
    score, bpm, phase = best
    # the ±20 ms window leaves a plateau of equally good tempos: refine by least squares — each onset near the grid
    # assigned to its sixteenth, then t = phase + n * six fitted (twice)
    six = 60 / bpm / 4
    for _ in range(2):
        n = np.round((times - phase) / six)
        near = np.abs(times - (phase + n * six)) < 0.020
        if near.sum() >= 8 and np.ptp(n[near]) > 0:
            nn, tt = n[near], times[near]          # closed-form line fit (no LAPACK: lstsq is unreliable on this host)
            six = float(((nn - nn.mean()) * (tt - tt.mean())).sum() / ((nn - nn.mean()) ** 2).sum())
            phase = float(tt.mean() - six * nn.mean())
    bpm = 60 / (4 * six)
    phase = phase % six
    beat = 60 / bpm
    # the downbeat: of the 16 sixteenths in a bar, the one the low band (kick) is strongest on (a beat start)
    low = envs["low"][1]
    bar, six = 4 * beat, beat / 4
    scores = []
    for j in range(16):
        idx = ((phase + j * six + np.arange(0, len(low) / FS, bar)) * FS).astype(int)
        idx = idx[(idx >= 15) & (idx < len(low) - 15)]
        scores.append(np.mean([low[i - 15:i + 15].max() for i in idx]) if len(idx) else 0)
    T0 = (t0 or 0) + phase + int(np.argmax(scores)) * six
    off = ((times + (t0 or 0) - T0) / six) % 1
    near = np.minimum(off, 1 - off) * six < 0.020
    return {"bpm": round(float(bpm), 3), "t0": round(float(T0), 3), "sixteenth_s": round(six, 6),
            "on_grid": round(float(near.mean()), 3), "grid_score": round(float(score), 3), "onsets": int(len(times))}


def program(song, drums, cuts, bpm, T0, parts, bands, on_db=3.5, contrast=3.0, drop=12.0, t_from=None, t_to=None,
            replace=False, patch=None, force=None, log=print, level_gap=18.0):
    """→ (new song dict, {track: hits}). Notes tracks only."""
    six = 60 / bpm / 4
    t_from = cuts[0] if t_from is None else t_from
    t_to = cuts[-1] if t_to is None else t_to
    out = json.loads(json.dumps(song))
    tpl = next((t for t in out["tracks"] if str(t.get("name", "")).startswith("drums")), None)
    counts = {}
    for band, piece, name in parts:
        if band not in bands:
            raise SystemExit(f"griddrums: unknown band {band!r} ({', '.join(bands)})")
        edb, de = band_env(drums, *bands[band])
        notes = []
        for s0, s1 in zip(cuts, cuts[1:]):
            if s1 <= t_from or s0 >= t_to:
                continue
            a, b = max(s0, t_from), min(s1, t_to)
            ns = [n for n in range(int(np.ceil((a - T0) / six)), int((b - T0) / six) + 1)
                  if a <= T0 + n * six < b and 15 <= int((T0 + n * six) * FS) < len(de) - 45]
            if not ns:
                continue
            at = {n: int((T0 + n * six) * FS) for n in ns}
            strength = {n: de[at[n] - 15:at[n] + 25].max() for n in ns}
            level = {n: edb[at[n]:at[n] + 40].max() for n in ns}
            sl = np.array([np.mean([strength[n] for n in ns if n % 16 == k] or [0]) for k in range(16)])
            sdb = 10 * np.log10(sl / (sl.max() + 1e-12) + 1e-9)
            spec = (force or {}).get(round(s0, 2))
            if spec is not None:
                sdb = np.array([0.0 if k in spec else -99.0 for k in range(16)])
            if sdb.max() - sdb.min() < contrast:
                log(f"{name} {a:.1f}-{b:.1f}: no pattern (contrast {sdb.max() - sdb.min():.1f} dB)")
                continue
            lv = np.array([np.mean([level[n] for n in ns if n % 16 == k] or [-200]) for k in range(16)])
            pat = {k for k in range(16) if sdb[k] >= -on_db and (spec is not None or lv[k] >= lv.max() - level_gap)}
            med = float(np.median([level[n] for n in ns if n % 16 in pat]))
            kept = 0
            for n in ns:
                if n % 16 in pat and level[n] >= med - drop:
                    notes.append({"at": f"{T0 + n * six:.6f}s", "len": f"{six:.6f}s", "pitch": piece,
                                  "vel": round(float(np.clip(0.75 + (level[n] - med) / 25, 0.3, 1.0)), 4)})
                    kept += 1
            log(f"{name} {a:.1f}-{b:.1f}: pattern {sorted(pat)} hits {kept}")
        tr = next((t for t in out["tracks"] if t.get("name") == name), None)
        if tr is not None and replace:
            if not isinstance(tr.get("notes"), list):
                raise SystemExit(f"griddrums: --replace needs {name!r} to be a notes track")
            keep = [x for x in tr["notes"] if not (t_from <= float(str(x["at"]).rstrip("s")) < t_to)]
            tr["notes"] = sorted(keep + notes, key=lambda x: float(str(x["at"]).rstrip("s")))
        else:
            p = patch or (tpl or {}).get("patch")
            if not p:
                raise SystemExit("griddrums: no drums-* track to take a kit from: pass --patch KIT")
            new = {"name": name + ("-grid" if tr is not None else ""), "patch": p, "gain": (tpl or {}).get("gain", "0dB"),
                   "notes": notes}
            for k in ("out",):
                if tpl and k in tpl:
                    new[k] = tpl[k]
            out["tracks"].append(new)
        counts[name] = len(notes)
    return out, counts


def fold(ref, ours, cuts, bpm, T0):
    """Per section: (start, end, ref 16 strengths, ours 16 strengths, correlation) of likeness's smoothed onset."""
    fps = SR / L.HOP
    six = 60 / bpm / 4
    sm = np.ones(5) / 5
    envs = [np.convolve(L.Feat(x).onset, sm, "same") for x in (ref, ours)]
    rows = []
    for s0, s1 in zip(cuts, cuts[1:]):
        ns = [n for n in range(int(np.ceil((s0 - T0) / six)), int((s1 - T0) / six) + 1) if s0 <= T0 + n * six < s1]
        if len(ns) < 16:
            continue
        pats = []
        for e in envs:
            v = [e[max(0, int(round((T0 + n * six) * fps)) - 1):int(round((T0 + n * six) * fps)) + 2].max()
                 if int(round((T0 + n * six) * fps)) + 1 < len(e) else 0.0 for n in ns]
            pats.append(np.array([np.mean([v[i] for i, n in enumerate(ns) if n % 16 == k] or [0]) for k in range(16)]))
        a, b = pats
        r = float(np.corrcoef(a, b)[0, 1]) if a.std() > 0 and b.std() > 0 else float("nan")
        rows.append((s0, s1, a, b, r))
    return rows


def digits(v):
    return "".join(str(int(round(9 * x / v.max()))) if v.max() > 0 else "0" for x in v)


def main(argv):
    a = list(argv)

    def opt(k, d=None):
        if k in a:
            i = a.index(k)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return d

    if not a or a[0] not in ("fit", "program", "fold"):
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    cmd = a.pop(0)
    t_from, t_to = opt("--from"), opt("--to")
    t_from, t_to = (float(t_from) if t_from else None), (float(t_to) if t_to else None)
    if cmd == "fit":
        lo, hi = (float(v) for v in opt("--bpm", "70-180").split("-"))
        print(json.dumps(fit(L.load(a[0]).mean(1).astype(np.float64), lo, hi, t_from, t_to, float(opt("--prefer", 120)))))
        return
    bpm, t0 = float(opt("--bpm")), float(opt("--t0"))
    if cmd == "fold":
        cuts = [float(v) for v in open(a[2]).read().split(",")]
        for s0, s1, r, o, c in fold(L.load(a[0]), L.load(a[1]), cuts, bpm, t0):
            flag = "  <- differs" if not c >= 0.5 else ""
            print(f"{s0:7.1f}-{s1:7.1f} s  ref {digits(r)}  ours {digits(o)}  r {c:+.2f}{flag}")
        return
    out = opt("-o")
    bands = dict(BANDS)
    for spec in (opt("--bands", "") or "").split(","):
        if spec.strip():
            k, rng = spec.split("=")
            bands[k] = tuple(float(v) for v in rng.split("-"))
    parts = [p.split(":") for p in opt("--parts", "low:k:drums-kick").split(",")]
    force = {}
    for spec in (opt("--force", "") or "").split(";"):
        if spec.strip():
            k, slots = spec.split("=")
            force[round(float(k), 2)] = {int(v) for v in slots.split(".")}
    kw = dict(on_db=float(opt("--on", 3.5)), contrast=float(opt("--contrast", 3.0)), drop=float(opt("--drop", 12.0)),
              level_gap=float(opt("--level-gap", 18.0)),
              patch=opt("--patch"), replace="--replace" in a)
    a = [x for x in a if x != "--replace"]
    if len(a) != 3 or not out:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    song_path, drums_path, secs = a
    text = songfmt.read(song_path)
    doc = songfmt.load(song_path)
    cuts = [float(v) for v in open(secs).read().split(",")]
    new, counts = program(doc, L.load(drums_path).mean(1).astype(np.float64), cuts, bpm, t0, parts, bands,
                          t_from=t_from, t_to=t_to, force=force, **kw)
    body = (json.dumps(new, **songfmt.json_style(song_path)[0]) + songfmt.json_style(song_path)[1]
            if text.lstrip().startswith("{") else songfmt.dump_yaml(new))
    d = os.path.dirname(os.path.abspath(out)) or "."
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(song_path)[1], prefix=".griddrums-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body)
        songfmt.plan_hash(tmp)
        os.replace(tmp, out)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    print(f"wrote {out}: " + ", ".join(f"{k} {v} hits" for k, v in counts.items()))


if __name__ == "__main__":
    main(sys.argv[1:])
