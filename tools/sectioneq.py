#!/usr/bin/env python3
"""Per-section master EQ for songs that are not built from section tracks: one master `eq` with a fixed set of
bands whose gains step at the section boundaries, driven by master automation lanes (`auto.eqN`). Each section's
gains are a least-squares fit (exact biquad responses, a little ridge) of the 1/3-octave long-term difference
between the candidate and the reference over that section — the dense sections stop dictating the quiet ones'
EQ (chirper-two's mastereq.py fits one stage for the whole mix; chirper-zero found per-section fits worth more).

  sectioneq.py REF.wav CAND.wav[,CAND2,...] SECTIONS.txt [--scale 1.0] [--max 9] [--only 0,2,5 | --sections 1,3,6]
               [--ramp 0.05] [--prefix eq] [--apply SONG -o OUT]

Prints a `master:` JSON block (auto lanes + eq stage) to merge into a song's master (append the eq after the glue).
--prefix P names the lanes P0..P6 (default eq): use another prefix when the song already has eq lanes
(an eqride.py ride or an earlier sectioneq) — appending with the same names silently REPLACES them (Pneuma: -4.5).
--only fits just those sections (others stay flat): check each section separately — a fit can chase content
the arrangement lacks. --only counts from 0 (as it always has); --sections counts from 1 like widthfit and
sectionlevel. Both print the chosen sections with their times.
--apply SONG -o OUT writes the fitted stage into SONG instead of printing the block (chirper-zero's request): the eq
goes right after the master glue, else before a clip, else at the end (masterstack's rule), its lanes into the
master's auto; a lane name already in the master is refused (the message names a free --prefix). SONG may be flow
YAML with a one-line master (what the tools write), a native JSON song, or a tab2song map (head.master); OUT is
written atomically in SONG's format after chirp plans it."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import likeness as L  # noqa: E402

SR = 48000
BANDS = [("lowshelf", 45, 0.7), ("peak", 90, 1.0), ("peak", 250, 1.0), ("peak", 700, 1.0), ("peak", 1800, 1.0),
         ("peak", 4000, 1.0), ("highshelf", 10000, 0.7)]
CENTERS = 1000 * 2 ** (np.arange(-14, 14) / 3)          # 1/3-octave centres ~40 Hz – 16 kHz
CENTERS = CENTERS[(CENTERS >= 40) & (CENTERS <= 16000)]


def biquad_db(kind, f0, q, gain_db, f):
    """RBJ cookbook magnitude response (dB) at frequencies f."""
    A = 10 ** (gain_db / 40); w0 = 2 * np.pi * f0 / SR; al = np.sin(w0) / (2 * q); c = np.cos(w0)
    if kind == "peak":
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    elif kind == "lowshelf":
        s = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * c + s), 2 * A * ((A - 1) - (A + 1) * c), A * ((A + 1) - (A - 1) * c - s)]
        a = [(A + 1) + (A - 1) * c + s, -2 * ((A - 1) + (A + 1) * c), (A + 1) + (A - 1) * c - s]
    else:
        s = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * c + s), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - s)]
        a = [(A + 1) - (A - 1) * c + s, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - s]
    z = np.exp(-1j * 2 * np.pi * f / SR)
    h = (b[0] + b[1] * z + b[2] * z * z) / (a[0] + a[1] * z + a[2] * z * z)
    return 20 * np.log10(np.abs(h) + 1e-12)


def third_octave(x):
    from scipy import signal as sg
    f, P = sg.welch(x, SR, nperseg=8192)
    out = []
    for c in CENTERS:
        sel = (f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))
        out.append(10 * np.log10(P[sel].sum() + 1e-20))
    return np.array(out)


def solve(A, b):
    """Gaussian elimination with partial pivoting (tiny systems; numpy.linalg crashes against some system
    LAPACK builds)."""
    A = np.array(A, dtype=float); b = np.array(b, dtype=float); n = len(b)
    for i in range(n):
        p = i + int(np.argmax(np.abs(A[i:, i])))
        A[[i, p]], b[[i, p]] = A[[p, i]], b[[p, i]]
        for j in range(i + 1, n):
            f = A[j, i] / A[i, i]
            A[j, i:] -= f * A[i, i:]; b[j] -= f * b[i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x


def fit(dev, mx=9.0, ridge=0.15):
    """Gains g (dB) for BANDS so that their summed response ≈ −dev (6 dB unit responses, linearised)."""
    M = np.stack([biquad_db(k, f0, q, 6.0, CENTERS) / 6.0 for k, f0, q in BANDS], axis=1)
    A = M.T @ M + ridge * np.eye(len(BANDS))
    g = solve(A, M.T @ (-dev))
    return np.clip(g, -mx, mx)


PREFIXES = ["eq", "rq", "sq", "tq", "uq", "vq"]


def _kind(f):
    return f.split()[0] if isinstance(f, str) else f.get("type")


def merge(ms, block):
    """Insert block's eq into master ms (after glue, else before clip, else last) and its lanes; → position note."""
    auto = ms.setdefault("auto", {})
    clash = sorted(set(block["auto"]) & set(auto))
    if clash:
        used = set(auto)
        free = next((p for p in PREFIXES if not any(u == p or u.startswith(p) and u[len(p):].isdigit() for u in used)), None)
        raise SystemExit(f"sectioneq: the master already has lane(s) {', '.join(clash)}: pass --prefix {free or 'P'} "
                         "(the same names would silently replace them)")
    fx = ms.setdefault("fx", [])
    glue = [k for k, f in enumerate(fx) if _kind(f) == "glue"]
    clip = [k for k, f in enumerate(fx) if _kind(f) == "clip"]
    at = glue[0] + 1 if glue else clip[0] if clip else len(fx)
    fx.insert(at, block["eq"])
    auto.update(block["auto"])
    return f"eq stage at master fx {at} ({'after glue' if glue else 'before clip' if clip else 'appended'})"


def apply_to(song, block, out):
    """Merge block into SONG's master and write OUT atomically in SONG's format (planned by chirp first)."""
    import songfmt
    import tempfile
    text = songfmt.read(song)
    if text.lstrip().startswith("{"):
        doc = json.loads(text)
        holder = doc["head"] if isinstance(doc.get("head"), dict) and "parts" in doc else doc if "tracks" in doc else None
        if holder is None:
            raise SystemExit(f"sectioneq: {song} is neither a song (tracks) nor a tab2song map (head/parts)")
        where = merge(holder.setdefault("master", {"fx": []}), block)
        style, nl = songfmt.json_style(song)
        body = json.dumps(doc, **style) + nl
        is_map = holder is not doc
    else:
        lines = text.splitlines(keepends=True)
        idx = [k for k, ln in enumerate(lines) if ln.startswith("master:")]
        if idx:
            try:
                ms = songfmt.flow_whole(lines[idx[0]][len("master:"):].strip(), f"{song}: master")
            except songfmt.Unsupported:
                raise SystemExit(f"sectioneq: {song}'s master is not the one-line form the tools write; merge by hand")
        else:
            ms = {"fx": []}
        where = merge(ms, block)
        line = "master: " + json.dumps(ms, ensure_ascii=False) + "\n"
        if idx:
            lines[idx[0]] = line
        else:
            t = [k for k, ln in enumerate(lines) if ln.startswith("tracks:")]
            lines.insert(t[0] if t else len(lines), line)
        body, is_map = "".join(lines), False
    d = os.path.dirname(os.path.abspath(out)) or "."
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(song)[1], prefix=".sectioneq-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body)
        if not is_map:
            songfmt.plan_hash(tmp)   # must plan (exits with chirp's error otherwise)
        os.replace(tmp, out)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    return where


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    scale, mx, ramp = opt("--scale", 1.0), opt("--max", 9.0), opt("--ramp", 0.05)
    prefix = a[a.index("--prefix") + 1] if "--prefix" in a else "eq"
    bounds = [float(v) for v in open(a[2]).read().split(",")]
    only = {int(v) for v in opt("--only", "").split(",") if v != ""} if "--only" in a else None
    if "--sections" in a:
        if only is not None:
            sys.exit("sectioneq: --only (from 0) or --sections (from 1), not both")
        only = {int(v) - 1 for v in opt("--sections", "").split(",") if v != ""}
        if min(only, default=0) < 0:
            sys.exit("sectioneq: --sections counts from 1")
    if only is not None:
        print("sectioneq: fitting " + ", ".join(f"section {k + 1} (index {k}, {bounds[k]:g}-{bounds[k + 1]:g} s)"
                                                 for k in sorted(only) if k + 1 < len(bounds)) + "; others stay flat",
              file=sys.stderr)
    # CAND may be several renders (comma-separated; the same song at different seeds): their spectra are averaged per
    # section, so the fit follows the arrangement, not one seed's draws
    R, Cds = L.load(a[0]).mean(1), [L.load(f).mean(1) for f in a[1].split(",")]
    gains = []
    for k, (s0, s1) in enumerate(zip(bounds, bounds[1:])):
        if only is not None and k not in only:
            gains.append(np.zeros(len(BANDS))); continue
        r = third_octave(R[int(s0 * SR):int(s1 * SR)])
        c = np.mean([third_octave(Cd[int(s0 * SR):int(min(s1, len(Cd) / SR) * SR)]) for Cd in Cds], axis=0)
        dev = (c - c.mean()) - (r - r.mean())
        g = fit(dev, mx) * scale
        gains.append(g)
        print(f"section {k} {s0:7.1f}-{s1:7.1f}: deviation rms {np.sqrt((dev ** 2).mean()):.1f} dB → gains " +
              " ".join(f"{b[1]}:{v:+.1f}" for b, v in zip(BANDS, g)), file=sys.stderr)
    auto, bands = {}, []
    for j, (kind, f0, q) in enumerate(BANDS):
        pts = []
        for k, (s0, s1) in enumerate(zip(bounds, bounds[1:])):
            v = round(float(gains[k][j]), 2)
            pts += [[f"{round(s0 if k == 0 else s0 + ramp, 3)}s", v], [f"{round(s1, 3)}s", v]]
        pts = [[ "0s", pts[0][1]]] + pts
        auto[f"{prefix}{j}"] = {"points": pts}
        bands.append({"kind": kind, "cutoff": f0, "q": q, "gain": {"value": "0dB", "mod": [{"src": f"auto.{prefix}{j}", "amount": 1}]}})
    block = {"auto": auto, "eq": {"type": "eq", "bands": bands}}
    if "--apply" in a:
        if "-o" not in a:
            sys.exit("sectioneq: --apply SONG needs -o OUT")
        out = a[a.index("-o") + 1]
        print(f"{apply_to(a[a.index('--apply') + 1], block, out)}, lanes {prefix}0-{len(BANDS) - 1} -> {out}")
    else:
        print(json.dumps(block))
