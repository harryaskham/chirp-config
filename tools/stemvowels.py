#!/usr/bin/env python3
"""Vowel transcription from a vocal stem: for every sung note of a song track, estimate the formants (F1, F2) of
the reference vocal over the note and map them onto chirp's voice-layer vowel axis (u 0 – o 0.25 – a 0.5 – e 0.75
– i 1), then write the track's score back with a per-note `^vow=X` articulation. Measured from audio — no lyric
text — so a synthesised singer follows the real vowel colour of each note.

  stemvowels.py VOCALS.wav SONG.yaml TRACK OUT.json [--key vox] [--style vow|builtin]

--style builtin writes the built-in `voice` patch's own marks instead of ^vow: its vowel is 0.5 (ah) moved by expr.u
(-0.5) and expr.i (+0.5), so X < 0.5 becomes ^u=(1-2X), X > 0.5 ^i=(2X-1), and 0.5 nothing. With the default ^vow, a
patch that doesn't bind expr.vow (the built-in voice, voice-spoken) ignores every vowel: chirper-three's micro round 21
scored byte-identical with and without them.

Envelope: cepstrally smoothed log spectrum (lifter below the pitch period, so the harmonics of a 100-400 Hz voice do
not pull the formants), averaged over the middle 60% of the note; F1 = strongest envelope peak in 230-1000 Hz,
F2 = strongest in max(F1+200, 650)-2800 Hz. Notes shorter than 0.12 s or near-silent in the stem keep the
previous note's vowel. Use with a patch whose vowel follows expr.vow (patches/maynard.yaml)."""
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drumtrans as D  # noqa: E402  (tempo map parsing)
import likeness as L  # noqa: E402

SR = 48000
VOWELS = {"u": (300, 870), "o": (460, 840), "a": (730, 1090), "e": (530, 1840), "i": (270, 2290)}
AXIS = [VOWELS[k] for k in "uoaei"]


def expand(tokens):
    out, i = [], 0
    while i < len(tokens):
        t = tokens[i]
        if t.startswith("["):
            depth, j, inner = 0, i, []
            while j < len(tokens):
                depth += tokens[j].count("[") - tokens[j].count("]")
                inner.append(tokens[j]); j += 1
                if depth == 0:
                    break
            m = re.match(r"^\[(.*)\]x(\d+)$", " ".join(inner))
            out += expand(m.group(1).split()) * int(m.group(2)); i = j
        else:
            out.append(t); i += 1
    return out


def _sub_block(text, sub):
    """(start, end) of an embedded song's block: `songs:` → `  SUB:` up to the next two-space key or top-level key."""
    m = re.search(r"^songs:\s*$", text, re.M)
    if not m:
        raise SystemExit("no songs: block (SONG/TRACK addresses an embedded song)")
    m2 = re.search(r"^  " + re.escape(sub) + r":\s*$", text[m.end():], re.M)
    if not m2:
        raise SystemExit(f"no embedded song {sub}")
    start = m.end() + m2.end()
    m3 = re.search(r"^(  [A-Za-z0-9_-]+:\s*$|[A-Za-z_])", text[start:], re.M)
    return start, (start + m3.start() if m3 else len(text))


def track_span(song, name):
    """(start, end) of a track's score string in the song text. NAME is a top-level track, or SUB/TRACK for a track
    of the embedded song SUB (Shadows: songs: {intro: {tracks: [...]}, ...} placed by `@intro/56b` tracks)."""
    text = open(song).read()
    lo, hi = 0, len(text)
    if "/" in name:
        sub, name = name.split("/", 1)
        lo, hi = _sub_block(text, sub)
    m = re.search(r'\{name: "?' + re.escape(name) + r'"?,[^\n]*?score: "([^"]*)"', text[lo:hi])   # quoted or not
    if not m:
        raise SystemExit(f"no track {name}")
    return lo + m.start(1), lo + m.end(1)


def track_offset(song, name):
    """Beats from the top song's start to where the track's beat 0 plays: 0 for a top-level track; for SUB/TRACK the
    `at:` of the top-level track that places `@SUB/…` (the first one, if SUB is placed more than once)."""
    if "/" not in name:
        return 0.0
    sub = name.split("/", 1)[0]
    text = open(song).read()
    t0 = re.search(r"^tracks:\s*$", text, re.M)
    body = text[t0.end():] if t0 else text
    k = body.find('"@' + sub + "/")
    if k < 0:
        raise SystemExit(f"no top-level track places @{sub}")
    starts = [mm.start() for mm in re.finditer(r"^  - ", body, re.M)]
    a = max([st for st in starts if st <= k], default=0)
    b = min([st for st in starts if st > k], default=len(body))
    m = re.search(r"\bat:\s*([0-9.]+)b", body[a:b])
    return float(m.group(1)) if m else 0.0


def track_tokens(song, name):
    a, b = track_span(song, name)
    return expand(open(song).read()[a:b].replace("|", " ").split())


def envelope(x, f0max=420.0):
    """Mean cepstrally smoothed log-magnitude envelope (dB) of frames of x; returns (freqs, env)."""
    n = 2048
    if len(x) < n:
        x = np.pad(x, (0, n - len(x)))
    frames = [x[i:i + n] for i in range(0, len(x) - n + 1, n // 2)]
    lift = int(SR / f0max * 0.8)            # keep quefrencies below ~80% of the shortest pitch period
    envs = []
    for fr in frames:
        spec = np.abs(np.fft.rfft(fr * np.hanning(n))) + 1e-9
        c = np.fft.irfft(np.log(spec))
        c[lift:-lift] = 0
        envs.append(np.fft.rfft(c).real)
    return np.fft.rfftfreq(n, 1 / SR), 20 / np.log(10) * np.mean(envs, axis=0)


def formants(f, env):
    def peak(lo, hi):
        sel = (f >= lo) & (f <= hi)
        k = np.argmax(env[sel]); return float(f[sel][k])
    f1 = peak(230, 1000)
    f2 = peak(max(f1 + 200, 650), 2800)
    return f1, f2


def to_axis(f1, f2):
    """Project (F1, log F2) onto the u–o–a–e–i polyline; returns t in 0..1."""
    p = np.array([f1 / 1000, np.log2(f2 / 1000)])
    pts = [np.array([a / 1000, np.log2(b / 1000)]) for a, b in AXIS]
    best, bt = 1e9, 0.5
    for k in range(4):
        a, b = pts[k], pts[k + 1]
        d = b - a
        s = np.clip(np.dot(p - a, d) / np.dot(d, d), 0, 1)
        dist = np.linalg.norm(p - (a + s * d))
        if dist < best:
            best, bt = dist, (k + s) / 4
    return round(float(bt), 2)


def run(stem, song, track, key="vox", style="vow"):
    x = L.load(stem).mean(1)
    pts = D.tempo_points(song)
    beats = np.array([b for b, _ in pts]); bpm = np.array([v for _, v in pts])
    secs = np.concatenate([[0.0], np.cumsum(np.diff(beats) * 60 / bpm[:-1])])

    def b2t(b):
        i = max(0, np.searchsorted(beats, b, side="right") - 1)
        return secs[i] + (b - beats[i]) * 60 / bpm[i]

    floor = 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9) - 20
    toks, out, pos, last, stats = track_tokens(song, track), [], 0.0, 0.5, []
    for t in toks:
        m = re.match(r"^([^/]+)/([0-9.]+)b(.*)$", t)
        if not m:
            out.append(t); continue
        body, ln, rest = m.group(1), float(m.group(2)), m.group(3)
        if body in ("R", "r", "_"):
            out.append(t); pos += ln; continue
        a, e = b2t(pos), b2t(pos + ln)
        dur = e - a
        v = last
        if dur >= 0.12:
            seg = x[int((a + 0.2 * dur) * SR):int((e - 0.2 * dur) * SR)]
            if len(seg) and 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) > floor:
                f1, f2 = formants(*envelope(seg))
                v = to_axis(f1, f2); stats.append((f1, f2, v))
        last = v
        out.append(f"{body}/{m.group(2)}b{rest}{mark(v, style)}")
        pos += ln
    return {key: {"score": " ".join(out), "notes": len(stats)}}, stats


def mark(v, style="vow"):
    """The per-note vowel articulation: ^vow=X (patches binding expr.vow), or the built-in voice's ^u / ^i."""
    if style != "builtin":
        return f"^vow={v}"
    if abs(v - 0.5) < 0.005:
        return ""
    return f"^u={round(1 - 2 * v, 3)}" if v < 0.5 else f"^i={round(2 * v - 1, 3)}"


if __name__ == "__main__":
    a = sys.argv[1:]
    key = a[a.index("--key") + 1] if "--key" in a else "vox"
    style = a[a.index("--style") + 1] if "--style" in a else "vow"
    res, stats = run(a[0], a[1], a[2], key, style)
    json.dump(res, open(a[3], "w"))
    if stats:
        vs = np.array([s[2] for s in stats])
        hist = {k: int(((vs >= lo) & (vs < hi)).sum()) for k, lo, hi in (("u", 0, .125), ("o", .125, .375), ("a", .375, .625), ("e", .625, .875), ("i", .875, 1.01))}
        print(f"{len(stats)} notes measured; vowels {hist}; median F1 {np.median([s[0] for s in stats]):.0f} F2 {np.median([s[1] for s in stats]):.0f}")
