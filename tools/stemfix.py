#!/usr/bin/env python3
"""stemfix: fix a track's notes from its stem — octave errors, wrong neighbours, out-of-tune pitch classes
(chirper-zero's request: it hand-mapped planned notes back to score tokens to do this on Tha).

  stemfix.py SONG TRACK STEM.wav [-o OUT] [--fix octave,neighbour,tune] [--key "A minor"] [--from A --to B]
             [--min-gain DB] [--tune-cents C] [--at T,T…] [--top N] [--json] [--no-check]

Without -o it only reports (strongest evidence first). Treat the report as notes to audition, not truth: on
already-climbed songs (Tha v2, Xtal v3) applying every 6 dB suggestion scored -0.34 and -0.04 (noteacc pitch -1.0,
+0.1), and Tha's 14 at 9 dB -0.05 — what is left there is mostly stem bleed. Listen to a suggestion (audition.py
over its window, or render --from/--to), then apply the ones you trust with --at (onset times, as reported) or the
strongest few with --top N, and keep the result only if it scores.

For every pitched note of TRACK (a `notes` list, or a generated `score` string: names with octaves, mNN, NNNhz,
chords of those; drum letters and chord symbols are left alone) the stem's spectrum over the note's span (from
30 ms after its onset, at most 1 s) gives each candidate pitch a harmonic salience: the dB of its first six
harmonics over the dB halfway between them, weighted 1/h — so the octave below (whose odd harmonics are missing)
and the octave above (whose midpoints are the note's own odd harmonics) both score lower than the right pitch.

  octave     move a note ±12 when that pitch has --min-gain dB (default 9) more salience
  neighbour  move a note ±1/±2 semitones likewise; with --key only notes outside the key move, onto in-key pitches
  tune       (opt-in; noisy on dense parts and bled stems — e.g. Xtal's pitch classes scattered from +22 to -30 cents)
             per pitch class, the median cents offset of its notes' harmonics at or above 150 Hz (3+ notes); past
             --tune-cents (default 15) those notes are retuned by it (fractional pitch in notes lists, NNNhz tokens
             in scores)

Default --fix octave,neighbour. Every change needs positive salience (the stem must show the new pitch). An edit is
proven before writing: with humanization off, chirp plans the original and the fixed song and every voice must
match except the changed notes' keys, which must change exactly as reported (catches a token whose octave latched
onto the next).
"""
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import songfmt  # noqa: E402
import splitpart as SP  # noqa: E402
from likeness import SR, load  # noqa: E402

PCS = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE = re.compile(r"^([A-Ga-g])([#sb]?)(-?\d+)$")
MODES = {"major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10], "dorian": [0, 2, 3, 5, 7, 9, 10],
         "phrygian": [0, 1, 3, 5, 7, 8, 10], "lydian": [0, 2, 4, 6, 7, 9, 11], "mixolydian": [0, 2, 4, 5, 7, 9, 10],
         "locrian": [0, 1, 3, 5, 6, 8, 10]}


class Refused(ValueError):
    pass


def parse_pitch(s, a4):
    """A score pitch → MIDI float, or None when it is not an explicit pitch (drum letter, chord symbol, no octave)."""
    m = NOTE.match(s)
    if m:
        letter, acc, octv = m.groups()
        return 12 * (int(octv) + 1) + PCS[letter.lower()] + {"#": 1, "s": 1, "b": -1, "": 0}[acc]
    if re.fullmatch(r"m\d+(\.\d+)?", s):
        return float(s[1:])
    if re.fullmatch(r"\d+(\.\d+)?hz", s, re.I):
        return 69 + 12 * math.log2(float(s[:-2]) / a4)
    return None


def spell(midi, a4):
    if abs(midi - round(midi)) < 1e-6:
        q = int(round(midi))
        return f"{NAMES[q % 12]}{q // 12 - 1}"
    return f"{a4 * 2 ** ((midi - 69) / 12):.3f}hz"


def events(track, segs, a4):
    """[(onset s, dur s, [midi…], ref)] of the track's explicit pitched notes; ref locates the note for the edit."""
    out = []
    if isinstance(track.get("notes"), list):
        for i, n in enumerate(track["notes"]):
            p = n.get("pitch")
            if isinstance(p, (int, float)):
                t = beats_to_s(SP.to_beats(n["at"], segs), segs)
                ln = n.get("len", "0.25s")
                d = beats_to_s(SP.to_beats(ln, segs) + SP.to_beats(n["at"], segs), segs) - t if str(ln).endswith("b") \
                    else float(str(ln).rstrip("s"))
                out.append((t, max(d, 0.05), [float(p)], ("notes", i)))
        return out
    if not isinstance(track.get("score"), str):
        raise Refused("the track has neither a notes list nor a score string")
    toks = track["score"].split()
    pos, last = 0.0, None
    for i, tok in enumerate(toks):
        if tok == "|":
            continue
        m = SP.TOK.match(tok)
        if not m:
            raise Refused(f"score token {tok!r} (only PITCH/Nb@V^marks, R/Nb, _/Nb and | are supported)")
        head, dur = m.group("head"), float(m.group("dur"))
        if head == "_" and last is not None:
            t, d0, ps, ref = out[last]
            out[last] = (t, beats_to_s(pos + dur, segs) - t, ps, ref)
        elif head not in SP.RESTS and head != "_":
            ps = [parse_pitch(x, a4) for x in head.split(",")]
            if ps and all(p is not None for p in ps):
                t = beats_to_s(pos, segs)
                out.append((t, beats_to_s(pos + dur, segs) - t, ps, ("score", i)))
                last = len(out) - 1
            else:
                last = None
        else:
            last = None
        pos += dur
    return out


def beats_to_s(b, segs):
    t = 0.0
    for i, (b0, bpm) in enumerate(segs):
        b1 = segs[i + 1][0] if i + 1 < len(segs) else float("inf")
        if b <= b1:
            return t + (b - b0) * 60 / bpm
        t += (b1 - b0) * 60 / bpm
    return t


class Stem:
    def __init__(self, path):
        x = load(path).mean(1).astype(np.float32)
        self.specs = {}
        for n in (8192, 16384):
            f, tt, Z = signal.stft(x, SR, nperseg=n, noverlap=n - 1200, boundary=None, padded=False)
            self.specs[n] = (f, tt, np.abs(Z).astype(np.float32))

    def spectrum(self, t, d, low):
        f, tt, M = self.specs[16384 if low else 8192]
        a, b = t + 0.03, t + min(max(d, 0.06), 1.0)
        sel = (tt >= a) & (tt <= b)
        if not sel.any():
            sel = np.zeros(len(tt), bool)
            sel[int(np.argmin(np.abs(tt - (a + b) / 2)))] = True
        return f, M[:, sel].mean(1) + 1e-9

    @staticmethod
    def amp(f, spec, hz):
        k = hz / (f[1] - f[0])
        i = int(round(k))
        if i < 1 or i + 1 >= len(spec):
            return None
        return float(spec[i - 1:i + 2].max())

    def salience(self, f, spec, midi, a4):
        f0 = a4 * 2 ** ((midi - 69) / 12)
        s = w = 0.0
        for h in range(1, 7):
            on, mid = self.amp(f, spec, h * f0), self.amp(f, spec, (h + 0.5) * f0)
            if on is None or mid is None or h * f0 > 8000:
                break
            s += (20 * math.log10(on) - 20 * math.log10(mid)) / h
            w += 1 / h
        return s / w if w else float("-inf")

    def cents(self, f, spec, midi, a4):
        """Median cents offset of up to four harmonic peaks at or above 150 Hz (where a bin is under 34 cents;
        parabolic interpolation), or None."""
        f0, df, out = a4 * 2 ** ((midi - 69) / 12), f[1] - f[0], []
        for h in [h for h in range(1, 9) if h * f0 >= 150][:4]:
            k = int(round(h * f0 / df))
            lo, hi = max(1, k - 3), min(len(spec) - 2, k + 3)
            if hi <= lo:
                break
            i = lo + int(np.argmax(spec[lo:hi + 1]))
            a, b, c = (math.log(spec[i - 1]), math.log(spec[i]), math.log(spec[i + 1]))
            den = a - 2 * b + c
            if den >= 0:          # not a peak (flat or a valley): no estimate from this harmonic
                continue
            frac = min(0.5, max(-0.5, 0.5 * (a - c) / den))
            out.append(1200 * math.log2(((i + frac) * df) / (h * f0)))
        return float(np.median(out)) if out else None


def plan_fixes(doc, track, stem, fixes, key, t0, t1, min_gain, tune_cents):
    segs = SP.tempo_segments(doc.get("tempo", 120))
    a4 = float(doc.get("a4", 440))
    ev = [e for e in events(track, segs, a4) if (t0 is None or e[0] >= t0) and (t1 is None or e[0] < t1)]
    scale = None
    if key:
        root, _, mode = key.strip().partition(" ")
        r = parse_pitch(root + "4", a4)
        if r is None or (mode or "major").lower() not in MODES:
            raise Refused(f"--key {key!r}: e.g. 'A minor', 'F# dorian'")
        scale = {(int(r) + iv) % 12 for iv in MODES[(mode or "major").lower()]}
    changes, tuning = [], defaultdict(list)
    for t, d, ps, ref in ev:
        for j, p in enumerate(ps):
            f, spec = stem.spectrum(t, d, p < 48)
            here = stem.salience(f, spec, p, a4)
            cands = []
            if "octave" in fixes:
                cands += [p - 12, p + 12]
            if "neighbour" in fixes and (scale is None or int(round(p)) % 12 not in scale):
                cands += [q for q in (p - 2, p - 1, p + 1, p + 2) if scale is None or int(round(q)) % 12 in scale]
            best = max(((stem.salience(*stem.spectrum(t, d, q < 48), q, a4), q) for q in cands), default=None)
            if best and best[0] > 0 and best[0] - here >= min_gain:
                changes.append({"t": round(t, 3), "ref": ref, "member": j, "old": p, "new": best[1],
                                "gain_db": round(best[0] - here, 1), "why": "octave" if abs(best[1] - p) == 12 else "neighbour"})
            elif "tune" in fixes and here > 3:
                c = stem.cents(f, spec, p, a4)
                if c is not None and abs(c) < 50:
                    tuning[int(round(p)) % 12].append((c, t, ref, j, p))
    retuned = {}
    for pc, rows in tuning.items():
        if len(rows) >= 3:
            med = float(np.median([r[0] for r in rows]))
            if abs(med) >= tune_cents:
                retuned[NAMES[pc]] = round(med, 1)
                for c, t, ref, j, p in rows:
                    changes.append({"t": round(t, 3), "ref": ref, "member": j, "old": p, "new": round(p + med / 100, 3),
                                    "gain_db": None, "why": f"tune {med:+.1f}c"})
    return sorted(changes, key=lambda c: c["t"]), retuned, len(ev)


def apply(doc, name, changes):
    out = json.loads(json.dumps(doc))
    tr = next(t for t in out["tracks"] if t.get("name") == name)
    a4 = float(doc.get("a4", 440))
    if isinstance(tr.get("notes"), list):
        for c in changes:
            tr["notes"][c["ref"][1]]["pitch"] = c["new"]
        return out
    toks = tr["score"].split(" ")
    by_tok = defaultdict(dict)
    for c in changes:
        by_tok[c["ref"][1]][c["member"]] = c["new"]
    # tokens are split on single spaces so the score's other whitespace survives; map token indices accordingly
    words = [i for i, w in enumerate(toks) if w]
    for ti, members in by_tok.items():
        wi = words[ti]
        m = SP.TOK.match(toks[wi])
        heads = m.group("head").split(",")
        for j, q in members.items():
            heads[j] = spell(q, a4)
        toks[wi] = ",".join(heads) + "/" + m.group("dur") + "b" + m.group("tail")
    tr["score"] = " ".join(toks)
    return out


def voices(path):
    r = subprocess.run([chirpbin.resolve("chirp"), "--json", "plan", "-f", os.path.abspath(path), "--ir"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    try:
        return json.loads(r.stdout)["data"]["ir"]["voices"]
    except (ValueError, KeyError, TypeError):
        raise Refused(f"chirp plan failed on {path}: {(r.stderr or r.stdout).strip()[-300:]}")


def prove(doc, fixed, name, changes, text, song, d):
    def planned(x):
        fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(song)[1], prefix=".stemfix-", dir=d)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(SP.render_text(SP.dehumanize(x, {name}), text, song))
            return voices(tmp)
        finally:
            os.remove(tmp)
    a, b = planned(doc), planned(fixed)
    shape = lambda vs: Counter((v["start"], v["end"], round(v["vel"], 6), v["release"]) for v in vs)  # noqa: E731
    keys = lambda vs: Counter(round(v["key"], 3) for v in vs)  # noqa: E731
    if shape(a) != shape(b):
        raise Refused("the fix moved or re-timed voices; nothing written")
    gone, came = keys(a) - keys(b), keys(b) - keys(a)
    want_gone = Counter(round(c["old"], 3) for c in changes) - Counter(round(c["new"], 3) for c in changes)
    want_came = Counter(round(c["new"], 3) for c in changes) - Counter(round(c["old"], 3) for c in changes)
    if gone != want_gone or came != want_came:
        raise Refused("the fix changed other notes' pitches (a latched octave?); nothing written")


def main(argv):
    a = list(argv)

    def opt(flag, default=None):
        if flag in a:
            i = a.index(flag)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return default

    flags = {x for x in a if x in ("--json", "--no-check")}
    a = [x for x in a if x not in flags]
    out, key = opt("-o"), opt("--key")
    fixes = set(opt("--fix", "octave,neighbour").split(","))
    t0, t1 = opt("--from"), opt("--to")
    min_gain, tune_cents = float(opt("--min-gain", 9)), float(opt("--tune-cents", 15))
    at, top = opt("--at"), opt("--top")
    if len(a) != 3 or fixes - {"octave", "neighbour", "tune"}:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    song, name, stem_path = a
    try:
        text = songfmt.read(song)
        doc = songfmt.load(song)
        tr = [t for t in doc.get("tracks", []) if isinstance(t, dict) and t.get("name") == name]
        if len(tr) != 1:
            raise Refused(f"track {name!r} not found (or not unique)")
        segs = SP.tempo_segments(doc.get("tempo", 120))
        ft = lambda v: None if v is None else beats_to_s(SP.to_beats(v, segs), segs)  # noqa: E731
        changes, retuned, n = plan_fixes(doc, tr[0], Stem(stem_path), fixes, key, ft(t0), ft(t1), min_gain, tune_cents)
        changes.sort(key=lambda c: (c["gain_db"] is None, -(c["gain_db"] or 0), c["t"]))   # strongest evidence first
        if at:
            want = [float(x) for x in at.split(",") if x.strip()]
            changes = [c for c in changes if any(abs(c["t"] - w) < 0.011 for w in want)]
        if top:
            changes = changes[:int(top)]
        report = {"notes": n, "changes": [{k: c[k] for k in ("t", "old", "new", "gain_db", "why")} for c in changes],
                  "retuned_pitch_classes": retuned}
        if "--json" in flags:
            print(json.dumps(report))
        else:
            print(f"{n} notes measured; {len(changes)} change(s)" + (f"; retuned {retuned}" if retuned else ""))
            for c in changes:
                print(f"  {c['t']:8.3f} s  {spell(c['old'], float(doc.get('a4', 440)))} -> "
                      f"{spell(c['new'], float(doc.get('a4', 440)))}  {c['why']}"
                      + (f" (+{c['gain_db']} dB)" if c["gain_db"] is not None else ""))
        if not out or not changes:
            return
        fixed = apply(doc, name, changes)
        d = os.path.dirname(os.path.abspath(out)) or "."
        if "--no-check" not in flags:
            prove(doc, fixed, name, changes, text, song, d)
        fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(song)[1], prefix=".stemfix-", dir=d)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(SP.render_text(fixed, text, song))
            os.replace(tmp, out)
            tmp = None
        finally:
            if tmp and os.path.exists(tmp):
                os.remove(tmp)
        if "--json" not in flags:
            print(f"wrote {out}" + ("" if "--no-check" in flags else " (proven: only the reported pitches changed)"))
    except (Refused, SP.Refused, songfmt.Unsupported) as e:
        raise SystemExit(f"stemfix: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
