#!/usr/bin/env python3
"""drumpunch: how punchy and real our drums are against the record's drum stem, per hit class (the tone push,
micro/TONE.md). It answers "why does our kit sound like a drum machine", which a single transients number cannot.

  drumpunch.py --song ID [--from S --to S] [--song-file F] [--tracks a,b] [--set PATH=V …] [--seed N] [--json]
  drumpunch.py --clip CLIP_ID [same options]           (a micro clip's song and window)
  drumpunch.py --song ID --ours OURS.wav [--ref REF.wav] (files instead of the render / the stem)

Ref: the record's drum stem (ref/stems/bs_roformer_sw/ID/drums.wav, else htdemucs_6s). Ours: the song's drum tracks
rendered solo over the window (auto-detected from patch names: kit, drum, hat, snare, kick, tom, cymbal, ride, crash,
china, splash; or --tracks), with the groove's pin (CHIRP_SRC / tools/groove-pin as microscore uses).

Hits come from OUR score: the song is transcribed from and aligned to the record, so each clean kick (no snare/tom
within 30 ms; cymbals allowed) and clean snare is measured at the same moment on both sides (a global lag from the
low-band envelopes absorbs a fixed offset; each hit's peak is found within +-25 ms). Each class is measured in its own
band (kick 35-150 Hz, snare 150 Hz-12 kHz) so the bass bleeding into a separated stem stays out.
Per hit, on the class band's 1 ms RMS envelope: rise_ms (10% -> 90% of the peak), punch_db (peak vs the body 20-50 ms
later), decay_ms (peak -> -20 dB, capped at the next hit / 400 ms); kick sub_click_db (35-120 Hz vs 2-6 kHz, first
10 ms); snare body_crack_db (150-300 Hz vs 1.5-5 kHz) and wires_crack_db (5-12 kHz vs 1.5-5 kHz) over the hit.
Reported: each side's medians and the median PAIRED difference (ours - ref). Separated stems carry bleed: compare
candidates against the same ref; the separator floor (bs_roformer vs htdemucs on one song) is the noise to beat.
Score per class = 100 * exp(-mean(|median diff| / tolerance) / 2); total = kick .5, snare .5 over present classes.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import likeness as L  # noqa: E402

SR = L.SR
DRUM_PATCH = re.compile(r"kit|drum|hat|snare|kick|tom|cymbal|ride|crash|china|splash", re.I)
TOL = {"rise_ms": 1.5, "punch_db": 2.5, "decay_ms": 40.0, "sub_click_db": 4.0, "body_crack_db": 4.0,
       "wires_crack_db": 4.0}
CLASS_W = {"kick": 0.5, "snare": 0.5}
CLASS_KEYS = {"kick": ["rise_ms", "punch_db", "decay_ms", "sub_click_db"],
              "snare": ["rise_ms", "punch_db", "decay_ms", "body_crack_db", "wires_crack_db"]}


def mono(x):
    x = np.asarray(x, dtype=np.float64)
    return x.mean(1) if x.ndim == 2 else x


def bandpass(y, lo, hi):
    """Zero-phase FFT band-pass."""
    Y = np.fft.rfft(y)
    f = np.fft.rfftfreq(len(y), 1 / SR)
    Y[(f < lo) | (f >= hi)] = 0
    return np.fft.irfft(Y, len(y))


def envelope(y, win=48, hop=24):
    """1 ms RMS, 0.5 ms hop: (times s, rms)."""
    fr = np.lib.stride_tricks.sliding_window_view(y, win)[::hop]
    return (np.arange(len(fr)) * hop + win / 2) / SR, np.sqrt((fr ** 2).mean(1) + 1e-20)


def band_db(seg, lo, hi):
    if len(seg) < 64:
        return -120.0
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 8192)) ** 2
    f = np.fft.rfftfreq(8192, 1 / SR)
    return float(10 * np.log10(sp[(f >= lo) & (f < hi)].sum() + 1e-20))


# Each class is measured in its own band, so the bass bleeding into a separated stem and the other pieces do not
# contaminate it. Hits come from OUR score (the song is transcribed from and aligned to the record), so both sides are
# measured at the same, labelled moments.
BANDS = {"kick": (35, 150), "snare": (150, 12000)}
KICK = re.compile(r"^k\d*$")
SNARE = {"s", "sc", "so", "se", "rs"}
TOM = re.compile(r"^(t\d+|ft\d*)$")


def measure(y, yb, on, nxt):
    """Rise, punch and decay of one hit on its class band YB (1 ms RMS envelope)."""
    i0, i1 = int(max(0, on - 0.01) * SR), int(min(len(yb) / SR, on + 0.4) * SR)
    seg = yb[i0:i1]
    if len(seg) < int(0.06 * SR):
        return None
    t, e = envelope(seg)
    t = t + i0 / SR
    win = (t >= on - 0.01) & (t <= on + 0.025)
    if not win.any():
        return None
    idx = np.flatnonzero(win)
    p = idx[np.argmax(e[idx])]
    peak = e[p]
    if peak < 1e-5:
        return None
    pre = e[max(0, p - 80):p + 1]
    below10 = np.flatnonzero(pre < 0.1 * peak)
    below90 = np.flatnonzero(pre < 0.9 * peak)
    t10 = (below10[-1] if len(below10) else 0) * 0.5
    t90 = (below90[-1] + 1 if len(below90) else len(pre) - 1) * 0.5
    tp = t[p]
    b0, b1 = tp + 0.02, min(tp + 0.05, nxt - 0.003)
    body = e[(t >= b0) & (t <= b1)]
    if b1 - b0 < 0.01 or body.size == 0:
        return None
    lim = min(tp + 0.4, nxt)
    after = np.flatnonzero((t > tp) & (t <= lim) & (e < 0.1 * peak))
    return {"rise_ms": float(max(0.5, t90 - t10)), "punch_db": float(20 * np.log10(peak / (np.sqrt((body ** 2).mean()) + 1e-12))),
            "decay_ms": float((t[after[0]] - tp) * 1000 if len(after) else (lim - tp) * 1000)}


def beats_to_seconds(tempo):
    """A function beats -> seconds for a canonical tempo (a number, or [{at: 'Nb', bpm, ramp}])."""
    if not isinstance(tempo, list):
        bpm = float(tempo or 120)
        return lambda b: b * 60.0 / bpm
    pts = sorted((float(str(p["at"]).rstrip("b")), float(p["bpm"]), bool(p.get("ramp"))) for p in tempo)
    grid = np.arange(0, pts[-1][0] + 1e5, 1.0 / 64)[: int((pts[-1][0] + 4096) * 64)]
    bpm = np.empty(len(grid))
    for i, (at, bp, _) in enumerate(pts):
        nxt = pts[i + 1] if i + 1 < len(pts) else None
        m = (grid >= at) & ((grid < nxt[0]) if nxt else True)
        if nxt and nxt[2]:                                       # ramp into the next point
            bpm[m] = bp + (nxt[1] - bp) * (grid[m] - at) / max(1e-9, nxt[0] - at)
        else:
            bpm[m] = bp
    bpm[grid < pts[0][0]] = pts[0][1]
    secs = np.concatenate([[0.0], np.cumsum(60.0 / bpm[:-1] / 64)])
    return lambda b: float(np.interp(b, grid, secs))


def events(song_file):
    """[(seconds, {'kick','snare','tom'}, vel)] from the song's drum tracks (chirp plan)."""
    import chirpbin
    r = subprocess.run([chirpbin.resolve("chirp"), "plan", "-f", os.path.abspath(song_file), "--json"], capture_output=True,
                       text=True, cwd=os.path.dirname(os.path.abspath(song_file)))
    try:
        can = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"drumpunch: chirp plan failed for {song_file}: {r.stderr.strip()[-200:]}")
    to_s = beats_to_seconds(can.get("tempo"))
    out, tracks = [], []
    for t in can.get("tracks", []):
        p = t.get("patch")
        pname = p if isinstance(p, str) else ""
        kit = (can.get("patches", {}).get(pname) or {}).get("kit") if pname else (p or {}).get("kit") if isinstance(p, dict) else None
        if not kit and not DRUM_PATCH.search(pname):
            continue
        tracks.append(t.get("name"))
        for n in t.get("notes") or []:
            pieces = {x.strip() for x in str(n.get("pitch", "")).split(",")}
            cls = set()
            if any(KICK.match(x) for x in pieces):
                cls.add("kick")
            if pieces & SNARE:
                cls.add("snare")
            if any(TOM.match(x) for x in pieces):
                cls.add("tom")
            if cls and n.get("at") is not None:
                out.append((to_s(float(n["at"])), cls, float(n.get("vel", 1.0))))
    out.sort(key=lambda e: e[0])
    return out, tracks


def clean(evs, cls, gap=0.03):
    """Times of CLS hits with no other kick/snare/tom within GAP s (cymbals and hats are allowed)."""
    times = [e[0] for e in evs]
    out = []
    for i, (t, c, _) in enumerate(evs):
        if c != {cls}:
            continue
        lo, hi = i, i
        while lo > 0 and t - times[lo - 1] < gap:
            lo -= 1
        while hi + 1 < len(evs) and times[hi + 1] - t < gap:
            hi += 1
        if lo == i and hi == i:
            out.append(t)
    return out


def lag(ref, ours, max_s=0.1):
    """Seconds by which OURS runs late against REF (low-band envelope cross-correlation)."""
    a, b = bandpass(mono(ref), 35, 150), bandpass(mono(ours), 35, 150)
    n = min(len(a), len(b))
    if n < SR:
        return 0.0
    ea = envelope(a[:n], 240, 240)[1]
    eb = envelope(b[:n], 240, 240)[1]                      # 5 ms frames
    ea, eb = ea - ea.mean(), eb - eb.mean()
    k = int(max_s * SR / 240)
    best = max(range(-k, k + 1), key=lambda d: float(np.dot(ea[max(0, -d):len(ea) - max(0, d)], eb[max(0, d):len(eb) - max(0, -d)])))
    return best * 240 / SR


def paired(ref, ours, evs, t0, shift):
    """Per class: paired measures at our clean hits (times relative to the window start T0)."""
    yr, yo = mono(ref), mono(ours)
    res = {}
    for cls, (lo, hi) in BANDS.items():
        rb, ob = bandpass(yr, lo, hi), bandpass(yo, lo, hi)
        ts = [t - t0 for t in clean(evs, cls)]
        rows = []
        for i, t in enumerate(ts):
            if t < 0.02 or t > len(yo) / SR - 0.1:
                continue
            nxt = ts[i + 1] if i + 1 < len(ts) else t + 0.4
            mo = measure(yo, ob, t, nxt)
            mr = measure(yr, rb, t - shift, nxt - shift)
            if not mo or not mr:
                continue
            for m, y, tt in ((mo, yo, t), (mr, yr, t - shift)):
                s0 = max(0, int(tt * SR))
                att, seg = y[s0:s0 + int(0.01 * SR)], y[s0:s0 + int(min(0.1, max(0.03, nxt - t)) * SR)]
                if cls == "kick":
                    m["sub_click_db"] = band_db(att, 35, 120) - band_db(att, 2000, 6000)
                else:
                    crack = band_db(seg, 1500, 5000)
                    m["body_crack_db"] = band_db(seg, 150, 300) - crack
                    m["wires_crack_db"] = band_db(seg, 5000, 12000) - crack
            rows.append((mr, mo))
        if rows:
            res[cls] = rows
    return res


def compare(pairs):
    """Per class: medians of each side, the median paired difference, a score; the weighted total."""
    res, tot, wsum = {}, 0.0, 0.0
    for cls, rows in pairs.items():
        keys = CLASS_KEYS[cls]
        med = lambda side, k: round(float(np.median([r[side][k] for r in rows])), 2)  # noqa: E731
        diffs = {k: round(float(np.median([r[1][k] - r[0][k] for r in rows])), 2) for k in keys}
        score = float(100 * np.exp(-np.mean([abs(v) / TOL[k] for k, v in diffs.items()]) / 2))
        res[cls] = {"n": len(rows), "ref": {k: med(0, k) for k in keys}, "ours": {k: med(1, k) for k in keys},
                    "diff": diffs, "score": round(score, 1)}
        tot += CLASS_W[cls] * score
        wsum += CLASS_W[cls]
    return {"total": round(tot / wsum, 2) if wsum else None, "classes": res}


# ── rendering ours, finding the ref ─────────────────────────────────────────────────────────

def ref_stem(song):
    for sep in ("bs_roformer_sw", "htdemucs_6s", "htdemucs"):
        p = os.path.join(ROOT, "ref", "stems", sep, song, "drums.wav")
        if os.path.exists(p):
            return p
    raise SystemExit(f"drumpunch: no drum stem for {song} under ref/stems/")


def render_ours(song_file, t0, t1, tracks, seed, sets):
    import microscore as M
    snap = os.path.join(os.path.dirname(os.path.abspath(song_file)), f".drumpunch-{os.getpid()}-{os.path.basename(song_file)}")
    shutil.copy(song_file, snap)
    try:
        extra = [x for t in tracks for x in ("--solo", t)] + [x for s in sets for x in ("--set", s)]
        return M.render_range(snap, t0, t1, seed, extra)
    finally:
        os.unlink(snap)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--song", help="climb id (its song file gives the hits; its record's drum stem is the ref)")
    ap.add_argument("--clip", help="a micro clip: its song and window")
    ap.add_argument("--from", dest="t0", type=float)
    ap.add_argument("--to", dest="t1", type=float)
    ap.add_argument("--song-file", help="a candidate song file (default songs/ID.yaml): its hits and its render")
    ap.add_argument("--tracks", help="drum tracks to render solo (default: those with a kit/drum patch)")
    ap.add_argument("--set", action="append", default=[], help="chirp render --set PATH=V for ours (a patch candidate)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--ref", help="a WAV for the ref side instead of the drum stem (cut to the window)")
    ap.add_argument("--ours", help="a WAV for our side instead of rendering (the window's render)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song, t0, t1 = a.song, a.t0, a.t1
    if a.clip:
        cl = next((c for c in json.load(open(os.path.join(ROOT, "micro", "clips.json")))["clips"] if c["id"] == a.clip), None)
        if not cl:
            raise SystemExit(f"drumpunch: no clip {a.clip}")
        song, t0, t1 = cl["song"], cl["from"], cl["to"]
    if not song:
        raise SystemExit("drumpunch: --song ID or --clip ID")
    song_file = a.song_file or os.path.join(ROOT, "songs", f"{song}.yaml")
    evs, auto_tracks = events(song_file)
    tracks = a.tracks.split(",") if a.tracks else auto_tracks
    stem = a.ref or ref_stem(song)
    full = L.load(stem)
    t0 = t0 or 0.0
    t1 = t1 or len(full) / SR
    ref_x = full[int(t0 * SR):int(t1 * SR)]
    ours_x = L.load(a.ours) if a.ours else render_ours(song_file, t0, t1, tracks, a.seed, a.set)
    evs = [e for e in evs if t0 <= e[0] < t1]
    shift = lag(ref_x, ours_x)
    res = compare(paired(ref_x, ours_x, evs, t0, shift))
    res.update(label=f"{song} {t0:g}-{t1:g} s", tracks=tracks, lag_ms=round(shift * 1000, 1),
               ref=os.path.relpath(stem, ROOT) if stem.startswith(ROOT) else stem)
    if a.json:
        print(json.dumps(res))
        return
    print(f"drumpunch {res['label']} (tracks {','.join(tracks)}; ref {res['ref']}; ours late by {res['lag_ms']} ms): "
          f"total {res['total']}")
    for cls, r in res["classes"].items():
        print(f"  {cls:5s} {r['score']:5.1f} ({r['n']} clean hits)  "
              + "  ".join(f"{k} {r['ref'][k]:.1f}->{r['ours'][k]:.1f}" for k in r["diff"]))


if __name__ == "__main__":
    main()
