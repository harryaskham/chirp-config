#!/usr/bin/env python3
"""Drum-stem transcription onto a kit's own pieces: every onset in a drum stem is decomposed (non-negative least
squares) into the spectral templates of the pieces of the kit that will play it, so simultaneous hits separate
and the weights become velocities (dynamics, ghost notes). Times are converted to beats through the song's own
tempo map and quantised finely; the output is one score per piece family (kick, snare, hats, toms, cymbals,
hand drums, claps), each with per-hit velocities, ready to drop into a song (tab2song.py "raw" parts).

  drumtrans.py STEM.wav SONG.yaml TEMPLATES.wav PIECES.json OUT.json [--from S] [--to S] [--grid 24] [--gain-db G]
               [--share 0.12] [--floor 0.06] [--labels TRACK] [--shift S] [--vel-gamma G] [--kit-levels [--source-gain-db D]]

--kit-levels (opt-in; bd-6f5e5a) reads each hit in units of its own piece's velocity-120 level from TEMPLATES.wav, so
a kick rendered 20 dB louder than a hat no longer reads as harder playing; the stem's overall gain is one number,
--source-gain-db (the stem's level relative to the kit render) or else taken from the kick and snare (their
95th-percentile hit = velocity 120). Without it (the default, unchanged), one calibration covers every piece.

--shift S moves every hit S seconds later (latency compensation: onsets are detected on the rising edge,
a rendered hit peaks at its start — Pneuma's high band matched best at +21 ms).

--labels TRACK learns each piece's template from the stem itself: the median feature of the stem onsets that
fall within 60 ms of that piece's hits in TRACK of SONG.yaml (a rough transcription, e.g. from a tab).

TEMPLATES.wav: the kit rendered with each piece of PIECES.json at velocities 40, 80, 120, one hit every 2 s in
that order (piece-major). SONG.yaml supplies the tempo map (a `tempo:` number or JSON list). The transcription
is an aid: listen-free checks are tools/likeness.py against the stem."""
import json
import os
import re
import sys

import numpy as np
from scipy import signal
from scipy.ndimage import maximum_filter1d

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR, NFFT, HOP = 48000, 2048, 256
FPS = SR / HOP
EDGES = np.geomspace(30, 16000, 41)
WIN = int(0.07 * FPS)          # 70 ms after the onset
NEED = {}  # piece -> (hits, dB its p95 hit needs beyond velocity 120), filled by a calibrated transcription

FAMILIES = {"kick": ["k"], "snare": ["s", "rc", "sw", "sl", "ss", "sz", "sc", "so", "se", "g"],
            "hats": ["h", "h1", "h2", "h3", "hs", "oh", "hf", "hp"], "toms": ["t", "t1", "t2", "t3", "ft", "ft2"],
            "cymbals": ["c", "rd", "rds", "rde", "rb", "x", "sp", "st", "cbl"], "hand": ["te", "na", "tun", "ge"],
            "claps": ["cp"]}   # the 909/electro kits' clap (bd-dfa7eb: selected cp hits were dropped at export)


def bands(x, chunk=60.0):
    """Band powers per HOP frame, computed in chunks (a 12-minute stem at a 5 ms hop would need GBs at once)."""
    x = np.asarray(x, dtype=np.float32)
    n = (len(x) - NFFT) // HOP + 1
    out = np.empty((len(EDGES) - 1, max(n, 0)), dtype=np.float32)
    f = np.fft.rfftfreq(NFFT, 1 / SR)
    sel = [(f >= a) & (f < b) for a, b in zip(EDGES[:-1], EDGES[1:])]
    win = np.hanning(NFFT).astype(np.float32)
    step = int(chunk * FPS)
    for k0 in range(0, n, step):
        k1 = min(n, k0 + step)
        idx = (np.arange(k0, k1)[:, None] * HOP + np.arange(NFFT)[None, :])
        P = np.abs(np.fft.rfft(x[idx] * win, axis=1)) ** 2
        out[:, k0:k1] = np.stack([P[:, m].sum(1) for m in sel])
    return out.astype(np.float64) + 1e-12


def novelty(B):
    lb = np.log(B)
    ref = maximum_filter1d(lb, size=3, axis=1)          # SuperFlux-style: vs. the max of the previous frames
    d = np.maximum(lb[:, 3:] - ref[:, :-3], 0).sum(0)
    return np.concatenate([np.zeros(3), d])


def pick(nov, delta=1.5, dist=0.025):
    med = signal.medfilt(nov, 2 * int(0.5 * FPS) + 1)
    mad = signal.medfilt(np.abs(nov - med), 2 * int(0.5 * FPS) + 1) + 1e-9
    pk, _ = signal.find_peaks(nov, height=med + delta * mad * 3, distance=max(1, int(dist * FPS)))
    return pk


A1, A2 = int(0.03 * FPS), int(0.12 * FPS)   # attack (0-30 ms) and body (30-120 ms) windows


def feat(B, k):
    """Magnitude per band in the attack (0-30 ms) and body (30-120 ms) after frame k, each minus what was already
    sounding just before: the body separates a fast kick from a ringing floor tom, the attack sticks from beaters."""
    pre = B[:, max(0, k - 4):max(1, k - 1)].mean(1)
    att = B[:, k:k + A1].sum(1) - 0.8 * pre * A1
    body = B[:, k + A1:k + A2].sum(1) - 0.8 * pre * (A2 - A1)
    return np.sqrt(np.maximum(np.concatenate([att, body]), 0))


def templates(path, pieces):
    x = L.load(path).mean(1)
    B = bands(x)
    T, gamma, n120 = [], [], []
    for i, p in enumerate(pieces):
        norms, vecs = [], []
        for j, v in enumerate((40, 80, 120)):
            t0 = (3 * i + j) * 2.0
            k0 = int(t0 * FPS)
            nov = novelty(B[:, max(0, k0 - 8):k0 + 12])
            k = max(0, k0 - 8) + int(np.argmax(nov))
            f = feat(B, k)
            vecs.append(f); norms.append(np.linalg.norm(f) + 1e-12)
        lx, ly = np.log([40, 80, 120]), np.log(norms)
        g = float(((lx - lx.mean()) * (ly - ly.mean())).sum() / ((lx - lx.mean()) ** 2).sum())   # magnitude ∝ vel^g
        T.append(vecs[2] / norms[2]); gamma.append(max(0.3, g)); n120.append(norms[2])
    return np.array(T).T, np.array(gamma), np.array(n120)


def track_hits(song_path, track_name):
    """(seconds, piece) for every kit hit of a song track written as `piece/LENb` tokens (as tab2song writes them),
    through the song's tempo map."""
    text = open(song_path).read()
    m = re.search(r'\{name: "?' + re.escape(track_name) + r'"?,[^\n]*?score: "([^"]*)"', text)   # quoted or not
    if not m:
        raise SystemExit(f"no track {track_name} in {song_path}")
    pts = tempo_points(song_path)
    beats = np.array([b for b, _ in pts]); bpm = np.array([v for _, v in pts])
    secs = np.concatenate([[0.0], np.cumsum(np.diff(beats) * 60 / bpm[:-1])])
    def b2t(b):
        i = max(0, np.searchsorted(beats, b, side="right") - 1)
        return secs[i] + (b - beats[i]) * 60 / bpm[i]
    out, pos = [], 0.0
    toks = m.group(1).replace("|", " ").split()
    def expand(ts):        # [a b]xN repeats
        res, i = [], 0
        while i < len(ts):
            t = ts[i]
            if t.startswith("["):
                depth, j, inner = 0, i, []
                while j < len(ts):
                    depth += ts[j].count("[") - ts[j].count("]")
                    inner.append(ts[j]); j += 1
                    if depth == 0: break
                body = " ".join(inner); mm = re.match(r"^\[(.*)\]x(\d+)$", body)
                res += expand(mm.group(1).split()) * int(mm.group(2)); i = j
            else:
                res.append(t); i += 1
        return res
    for t in expand(toks):
        mm = re.match(r"^([^/]+)/([0-9.]+)b", t)
        if not mm:
            continue
        if not mm.group(1).startswith(("R", "r")):
            for pc in mm.group(1).split(","):
                out.append((b2t(pos), pc))
        pos += float(mm.group(2))
    return out


def learned_templates(B, on, labels, pieces, tol=0.06):
    """Templates from the stem itself: the median feature of the onsets within `tol` of a labelled hit of each
    piece (labels: a rough transcription — tab hits). Returns (bands×pieces, counts)."""
    ot = on / FPS
    T, counts = [], []
    for p in pieces:
        lt = np.array([t for t, q in labels if q == p])
        if len(lt) == 0:
            T.append(None); counts.append(0); continue
        idx = [k for k, t in zip(on, ot) if np.min(np.abs(lt - t)) < tol]
        if len(idx) < 3:
            T.append(None); counts.append(len(idx)); continue
        F = np.array([feat(B, k) for k in idx])
        v = np.median(F / (np.linalg.norm(F, axis=1, keepdims=True) + 1e-12), axis=0)
        T.append(v / (np.linalg.norm(v) + 1e-12)); counts.append(len(idx))
    keep = [i for i, t in enumerate(T) if t is not None]
    return np.array([T[i] for i in keep]).T, [pieces[i] for i in keep], counts


def nnls(A, y, sweeps=60):
    """Non-negative least squares by coordinate descent (the problems are tiny: bands × pieces). Plain numpy:
    scipy.optimize.nnls crashes against some system BLAS builds."""
    AtA, Aty = A.T @ A, A.T @ y
    x = np.zeros(A.shape[1])
    d = np.diag(AtA) + 1e-12
    for _ in range(sweeps):
        for j in range(len(x)):
            g = Aty[j] - AtA[j] @ x + d[j] * x[j]
            x[j] = max(0.0, g / d[j])
    return x, None


def tempo_points(song_path):
    text = open(song_path).read()
    m = re.search(r"^tempo:\s*(.+)$", text, re.M)
    v = json.loads(m.group(1)) if m.group(1).strip().startswith("[") else float(m.group(1))
    if isinstance(v, (int, float)):
        return [(0.0, float(v))]
    return [(float(str(p["at"]).rstrip("b")), float(p["bpm"])) for p in v]


def time_to_beat(points):
    beats = np.array([b for b, _ in points]); bpm = np.array([v for _, v in points])
    secs = np.concatenate([[0.0], np.cumsum(np.diff(beats) * 60 / bpm[:-1])])
    def f(t):
        i = max(0, np.searchsorted(secs, t, side="right") - 1)
        return beats[i] + (t - secs[i]) * bpm[i] / 60
    return f


def fmt(b):
    return f"{round(b, 4):.4f}".rstrip("0").rstrip(".")


def transcribe(stem, song, tpl_wav, pieces, t0=0.0, t1=None, grid=24, gain_db=0.0, share=0.12, floor=0.06, labels=None, shift=0.0, vel_gamma=None,
               kit_levels=False, source_gain_db=None):
    x = L.load(stem).mean(1)
    B = bands(x)
    on_all = pick(novelty(B))
    kit_curve = None
    if labels is not None:
        all_pieces = list(pieces)
        T, pieces, counts = learned_templates(B, on_all, labels, pieces)
        gamma = np.ones(len(pieces))
        print("learned templates: " + ", ".join(f"{p}×{c}" for p, c in zip(pieces, counts)), file=sys.stderr)
        if tpl_wav and tpl_wav != "-" and os.path.exists(tpl_wav):
            # Per-piece velocity calibration through the kit's own rendered level curves: the stem's
            # amplitudes are comparable across pieces only through how loud each of OUR pieces plays.
            _, kg, kn = templates(tpl_wav, all_pieces)
            kit_curve = {p: (kg[all_pieces.index(p)], kn[all_pieces.index(p)]) for p in pieces}
    else:
        T, gamma, n120 = templates(tpl_wav, pieces)
        if vel_gamma:    # kits behind a bus compressor barely grow with velocity (gamma floors at 0.3): invert linearly
            gamma = np.full(len(pieces), float(vel_gamma))
    # weight bands so cymbal/hat bands count as much as the kick's: inverse of the stem's typical magnitude
    w = 1 / (np.median(np.sqrt(B), axis=1) + 1e-9)
    w = np.concatenate([w, w]) / w.mean()
    Tw = T * w[:, None]
    Tw = Tw / np.linalg.norm(Tw, axis=0, keepdims=True)
    scale = 10 ** (-gain_db / 20)
    on = on_all
    tb = time_to_beat(tempo_points(song))
    raw = []
    for k in on:
        t = k / FPS
        if t < t0 or (t1 is not None and t > t1):
            continue
        y = feat(B, k) * w
        ny = np.linalg.norm(y)
        if ny < 1e-9:
            continue
        c, _ = nnls(Tw, y)
        sh = (c ** 2) / (ny ** 2 + 1e-12)
        for i in np.nonzero((sh >= share) & (c / ny >= floor))[0]:
            # amplitude relative to the vel-120 template (unweighted norms ~ weighted norms up to a per-piece
            # constant absorbed by the template normalisation) → velocity through the piece's own curve
            amp = c[i] * scale / (np.linalg.norm(T[:, i] * w) + 1e-12) * (np.linalg.norm(T[:, i]) + 1e-12)
            raw.append((t, i, amp))
    if kit_curve:
        # one global gain G (stem units per kit unit) from the anchors (kick, snare: p95 hit ~ vel 120), then
        # every hit through its own piece's curve: vel = 120 * (amp / (G * level120)) ** (1 / gamma)
        amps = {p: np.array([amp for _, i, amp in raw if pieces[i] == p]) for p in pieces}
        anchors = [p for p in ("k", "s") if p in amps and len(amps[p]) > 10] or [p for p in pieces if len(amps[p])]
        G = float(np.median([np.percentile(amps[p], 95) / kit_curve[p][1] for p in anchors]))
        velf = lambda i, amp: 120 * (amp / (G * kit_curve[pieces[i]][1])) ** (1 / kit_curve[pieces[i]][0])
        for p in pieces:
            if len(amps[p]):
                v95 = float(np.percentile([velf(pieces.index(p), a) for a in amps[p]], 95))
                need = 20 * kit_curve[p][0] * np.log10(v95 / 120)
                NEED[p] = (len(amps[p]), need)
                hint = f"  → raise the piece ~{need:+.1f} dB" if v95 > 127 else ""
                print(f"  {p}: {len(amps[p])} hits, p95 velocity {v95:.0f}{hint}", file=sys.stderr)
        events = [(t, pieces[i], int(np.clip(velf(i, amp), 1, 127))) for t, i, amp in raw]
    elif kit_levels:
        # bd-6f5e5a (opt-in): each hit in units of ITS OWN piece's velocity-120 level (a hit as loud as that piece's
        # vel-120 template is 1, whatever the piece), then one global source gain G: given (--source-gain-db), or
        # from the anchors (kick and snare: their 95th-percentile hit is velocity 120), as the --labels path does
        units = [(t, i, amp / (n120[i] + 1e-12)) for t, i, amp in raw]
        if source_gain_db is not None:
            G, how = 10 ** (source_gain_db / 20), "given"
        else:
            per = {}
            for _, i, u in units:
                per.setdefault(pieces[i], []).append(u)
            anchors = [p for p in ("k", "s") if len(per.get(p, [])) > 10] or list(per)
            G = float(np.median([np.percentile(per[p], 95) for p in anchors])) if anchors else 1.0
            how = f"95th-percentile hit of {','.join(anchors) or 'none'} at 120"
        print(f"drumtrans: kit levels: source gain {20 * np.log10(max(G, 1e-12)):+.2f} dB ({how})", file=sys.stderr)
        events = [(t, pieces[i], int(np.clip(round(120 * (u / max(G, 1e-12)) ** (1 / gamma[i])), 1, 127))) for t, i, u in units]
    else:
        # velocity: through each piece's own level curve, with one global calibration so the 95th-percentile
        # hit lands at 120 (the stem's absolute level is arbitrary). Pieces' own levels are NOT taken into account
        # (a quieter piece reads as softer playing): --kit-levels does (bd-6f5e5a)
        v0 = np.array([amp ** (1 / gamma[i]) for _, i, amp in raw]) if raw else np.ones(1)
        cal = 120 / (np.percentile(v0, 95) + 1e-12)
        events = [(t, pieces[i], int(np.clip(cal * amp ** (1 / gamma[i]), 1, 127))) for t, i, amp in raw]
    # a piece in no family takes part in the decomposition (it absorbs energy) but has nowhere to go: say so
    # instead of losing its hits silently (bd-dfa7eb)
    homed = {p for ms in FAMILIES.values() for p in ms}
    lost = {}
    for _, p, _ in events:
        if p not in homed:
            lost[p] = lost.get(p, 0) + 1
    if lost:
        print("drumtrans: not exported (no family in FAMILIES): "
              + ", ".join(f"{p} {n} hits" for p, n in sorted(lost.items())), file=sys.stderr)
    out = {}
    for fam, members in FAMILIES.items():
        ev = sorted((round(tb(t + shift) * grid) / grid, p, v) for t, p, v in events if p in members)
        merged = {}
        for b, p, v in ev:                     # one hit per grid slot: the loudest
            if b not in merged or v > merged[b][1]:
                merged[b] = (p, v)
        if not merged:
            continue
        toks, cur = [], 0.0
        keys = sorted(merged)
        for i, b in enumerate(keys):
            if b > cur + 1e-9:
                toks.append(f"R/{fmt(b - cur)}b")
            nxt = keys[i + 1] if i + 1 < len(keys) else b + 1
            p, v = merged[b]
            toks.append(f"{p}/{fmt(nxt - b)}b@{v}")
            cur = nxt
        out[fam] = {"score": " ".join(toks), "hits": len(merged)}
    return out, len(on)


def suggest_family_gains(min_hits=20):
    """Track gain per family (dB, >= 0) so its pieces reach the stem's level after the kit's bus (piece gains
    are squashed by a kit-bus compressor; track gain sits after it): the median need of its populated pieces."""
    out = {}
    for fam, members in FAMILIES.items():
        needs = [NEED[p][1] for p in members if p in NEED and NEED[p][0] >= min_hits]
        if needs:
            out[fam] = round(max(0.0, float(np.median(needs))), 1)
    return out


def template_song(kit, pieces, family_gains=None):
    """Template song: each piece at velocities 40/80/120, 2 s apart, on its own track at its family's gain — the
    templates then measure each piece's level after the kit bus and track gain, as it plays in the song."""
    fam_of = {p: f for f, ms in FAMILIES.items() for p in ms}
    tracks = []
    for i, p in enumerate(pieces):
        g = (family_gains or {}).get(fam_of.get(p, ""), 0.0)
        notes = " ".join(f"{p}/2@{v}" for v in (40, 80, 120))
        tracks.append({"name": f"tpl-{p}", "patch": kit, "gain": f"{g}dB", "score": (f"R/{6 * i}b " if i else "") + notes})
    return {"tempo": 60, "tail": "2s", "tracks": tracks}


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--template-song":
        fg = json.load(open(a[a.index("--family-gains") + 1])) if "--family-gains" in a else None
        json.dump(template_song(a[1], json.load(open(a[2])), fg), open(a[3], "w"))
        sys.exit()
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    pieces = json.load(open(a[3]))
    labels = track_hits(a[1], a[a.index("--labels") + 1]) if "--labels" in a else None
    res, n_on = transcribe(a[0], a[1], a[2], pieces, opt("--from", 0.0), (opt("--to", -1.0) if "--to" in a else None),
                           opt("--grid", 24), opt("--gain-db", 0.0), opt("--share", 0.12), opt("--floor", 0.06), labels,
                           opt("--shift", 0.0), opt("--vel-gamma", 0.0) or None, "--kit-levels" in a,
                           float(a[a.index("--source-gain-db") + 1]) if "--source-gain-db" in a else None)
    json.dump(res, open(a[4], "w"))
    if "--suggest-gains" in a:
        sg = suggest_family_gains()
        json.dump(sg, open(a[a.index("--suggest-gains") + 1], "w"))
        print("suggested family gains (dB): " + json.dumps(sg), file=sys.stderr)
    print(f"{n_on} onsets → " + ", ".join(f"{k} {v['hits']}" for k, v in res.items()))
