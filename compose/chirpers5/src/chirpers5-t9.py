#!/usr/bin/env python3
"""Chirpers - Soft Concrete (Chirpers V), track 9: LATE SHIFT (chirper-three).

LIQUID FUNK: the band plays the night shift. 174 bpm, A dorian.

Where the album's other tracks lead with reese, chops or piano, this one is PLAYED: a finger bass (bass-di) walking
a syncopated funk line instead of a reese, a cutting guitar chopping the off-beats, Rhodes comping, a horn section
stabbing the phrase ends, and only in the break a wah lead taking a solo. Under it wM's amen as a straight roller
(not swung: the swing is First Light's), a clean kick and snare, and a sub doubling the bass's roots.

Harmony (two bars each, the last pair one bar each): Am9 | D9 | Gmaj9 | F#m7b5 B7#9.

FORM (128 bars, 174 bpm, ~2:57):
  intro  1-16    Rhodes and the guitar's chops, filtered; the bass enters at 9
  build  17-32   the roller and kick come in under an opening filter; horns at the end
  drop   33-64   the band: roller, kick and snare, bass, guitar, Rhodes, horn stabs at phrase ends
  break  65-80   drums out: Rhodes and the bass, the WAH SOLO
  drop2  81-112  the band again, the horns answering every two bars
  outro  113-128 the drums leave, the guitar and Rhodes close the shift; since v2 the last four bars hold a Dbmaj9
                 (the D9 sliding down a half step), the closer's first chord
"""
import json
import os
import random

OUT = os.environ.get("C5T9_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers5-t9.yaml")
BPM = 174
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SECTIONS = [("intro", 1, 16), ("build", 17, 32), ("drop", 33, 64), ("break", 65, 80), ("drop2", 81, 112),
            ("outro", 113, 128)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def x16(bar, step):
    return b0(bar) + step / 4


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "outro"


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((at, ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-5:
                toks.append(f"R/{s - pos:.5g}b")
            base, _, mods = head.partition("^")
            toks.append(f"{base}/{ln:.5g}b@{vel}" + (f"^{mods}" if mods else ""))
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks)


P = {}


def part(n):
    return P.setdefault(n, Part())


# (root midi in octave 2, voicing) per bar of the 8-bar cycle
CYCLE = [(45, [55, 60, 64, 67, 71]), (45, [55, 60, 64, 67, 71]),        # Am9   (G3 C4 E4 G4 B4)
         (38, [54, 57, 60, 64, 66]), (38, [54, 57, 60, 64, 66]),        # D9    (F#3 A3 C4 E4 F#4)
         (43, [54, 59, 62, 66, 69]), (43, [54, 59, 62, 66, 69]),        # Gmaj9 (F#3 B3 D4 F#4 A4)
         (42, [57, 60, 64, 66, 69]),                                     # F#m7b5 (A3 C4 E4 F#4 A4... )
         (47, [57, 62, 63, 66, 69])]                                     # B7#9  (A3 D4 D#4 F#4 A4)


def chord(bar):
    return CYCLE[(bar - 1) % 8]


ROLL = [0, 3, 2, 7, 4, 5, 10, 6]      # the roller (eighth-note amen slices), straight


def drums():
    hand = random.Random(1)
    for bar in range(17, 125):
        sec = sec_of(bar)
        if sec == "break" or (sec == "outro" and bar > 116):
            continue
        roll = sec in ("drop", "drop2") or (sec == "build" and bar >= 21)
        if roll:
            for k, sl in enumerate(ROLL):
                mod = "^tune=2" if (bar % 4 == 0 and k == 6) else ""
                part("roll").add(b0(bar) + k / 2, 0.5, nm(36 + sl + (16 if bar % 2 == 0 and k >= 4 else 0)) + mod,
                                 (94 if k in (0, 4) else 76) + hand.randint(-6, 6))
        if sec in ("drop", "drop2") or (sec == "build" and bar >= 25):
            part("kick").add(x16(bar, 0), 0.5, "k", 110)
            part("kick").add(x16(bar, 10), 0.5, "k", 98)
            for s in (4, 12):
                part("snare").add(x16(bar, s), 0.5, "s", 104 + hand.randint(-4, 4))


# THE FUNK LINE (finger bass), one bar per chord bar: (sixteenth, semitones from the root, length in 16ths, vel)
LINE_A = [(0, 0, 3, 100), (3, 12, 1, 70), (4, 0, 1, 52), (6, 10, 2, 84), (8, 7, 2, 90), (10, 0, 1, 60),
          (11, 3, 2, 80), (14, 5, 1, 74), (15, 7, 1, 82)]
LINE_B = [(0, 0, 2, 100), (2, 0, 1, 50), (3, 12, 2, 80), (6, 10, 1, 70), (7, 7, 3, 88), (11, 5, 1, 70),
          (12, 3, 2, 84), (14, 2, 1, 70), (15, 0, 1, 76)]


def bass():
    hand = random.Random(2)
    for bar in range(9, 121):
        sec = sec_of(bar)
        root, _ = chord(bar)
        line = LINE_A if bar % 2 else LINE_B
        if sec == "intro":
            line = [n for n in line if n[0] in (0, 8)]                   # it enters with roots and fifths only
        for s, iv, ln, v in line:
            late = 0.0       # (late ghosts tried in v3: the rhythm smeared, 81 -> 70)
            part("bass").add(x16(bar, s) + late, ln / 4 * 0.9, nm(root - 12 + iv), v + hand.randint(-5, 5))
        if sec in ("drop", "drop2", "build"):
            part("sub").add(b0(bar), BAR - 0.05, nm(root - 12), 90)


def band():
    hand = random.Random(3)
    for bar in range(1, 125):
        sec = sec_of(bar)
        root, voic = chord(bar)
        v = ",".join(nm(m) for m in voic)
        # Rhodes: on the one and the and-of-2 (re-struck without the root)
        part("keys").add(b0(bar), 1.4, v, 70 + hand.randint(-5, 5))
        if sec != "intro" or bar > 4:
            part("keys").add(b0(bar) + 1.5, 1.0, ",".join(nm(m) for m in voic[1:]), 58 + hand.randint(-5, 5))
        # the cutting guitar: off-eighth chops (and a sixteenth push before 3 and before the next bar)
        if sec != "break" and bar <= 124:
            for s in (2, 6, 7, 10, 14, 15):
                if s in (7, 15) and hand.random() < 0.5:
                    continue
                part("gtr").add(x16(bar, s), 0.18, ",".join(nm(m + 12) for m in voic[1:4]),
                                (82 if s in (2, 10) else 66) + hand.randint(-6, 6))
        # horn stabs: the end of every fourth bar in the drops (every second in drop 2), and the build's last bar
        stab = (sec == "drop" and bar % 4 == 0) or (sec == "drop2" and bar % 2 == 0) or bar == 32
        if stab:
            top = ",".join(nm(m + 12) for m in voic[2:5])
            for s, ln, vv in ((10, 0.4, 96), (12, 0.25, 84), (14, 0.9, 104)):
                part("horns").add(x16(bar, s), ln, top, vv)


SOLO = [  # the wah solo over the break (bar offset, sixteenth, note, length 16ths)
    (0, 0, "E5", 4), (0, 6, "G5", 2), (0, 8, "A5", 6), (1, 0, "G5", 2), (1, 2, "E5", 2), (1, 4, "D5", 4), (1, 10, "B4", 6),
    (2, 0, "C5", 3), (2, 3, "D5", 3), (2, 6, "E5", 2), (2, 8, "F#5", 8), (3, 4, "E5", 2), (3, 6, "D5", 2), (3, 8, "B4", 8),
    (4, 0, "A4", 2), (4, 2, "C5", 2), (4, 4, "E5", 2), (4, 6, "G5", 2), (4, 8, "B5", 8), (5, 2, "A5", 2), (5, 4, "G5", 4),
    (5, 10, "E5", 6), (6, 0, "F#5", 4), (6, 6, "A5", 2), (6, 8, "C6", 6), (7, 0, "B5", 4), (7, 6, "A5", 2), (7, 8, "F#5", 8)]


def last_chord():
    """THE SHIFT ENDS (v2, chirper-zero's seam note): the outro's D9 slides down a half step into a held DBMAJ9 for
    the last four bars - the Rhodes, a soft horn swell, the bass and sub on Db - ringing into the next track, which is
    Streetlights Off opening on the same chord. No dead air: the band hands its last chord to the closer."""
    v = [56, 60, 63, 65, 68]                                   # Ab3 C4 Eb4 F4 Ab4 over Db: Dbmaj9 (no root up top)
    part("keys").add(b0(125), 4 * BAR - 0.2, ",".join(nm(m) for m in [49] + v), 74)
    part("horns").add(b0(125) + 0.5, 4 * BAR - 0.7, ",".join(nm(m + 12) for m in (60, 65, 68)), 52)
    part("bass").add(b0(125), 2 * BAR, nm(37), 90)
    part("sub").add(b0(125), 4 * BAR - 0.2, nm(25), 84)


def solo():
    hand = random.Random(4)
    for start in (65, 73):
        for bo, s, n, ln in SOLO:
            part("wah").add(x16(start + bo, s), ln / 4 * 0.92, n, 84 + hand.randint(-8, 8))


LEVEL = {"intro": -4, "build": -2, "drop": 0, "break": -4, "drop2": 0, "outro": -4}


def lanes():
    sec = lambda beats: beats * 60 / BPM
    dyn = []
    for name, a, z in SECTIONS:
        t0 = sec(b0(a))
        if dyn:
            dyn.append([f"{max(0.0, t0 - 0.2):.3f}s", dyn[-1][1]])
        dyn.append([f"{t0:.3f}s", float(LEVEL[name])])
    lp = [["0s", 0.0], [f"{sec(b0(17)):.3f}s", 0.0], [f"{sec(b0(33)) - 0.05:.3f}s", 1.0], [f"{sec(b0(33)):.3f}s", 1.0]]
    return dyn, lp


def main():
    drums()
    bass()
    band()
    solo()
    last_chord()
    dyn, lp = lanes()
    pump = {"type": "pump", "on": "kick", "depth": "-6dB", "attack": "3ms", "release": "230ms", "curve": 0.6}
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "Chirpers - Soft Concrete (Chirpers V), track 9 by chirper-three: LATE SHIFT. Liquid funk: a played "
                 "band (finger bass, cutting guitar, Rhodes, horns, a wah solo) over wM's amen as a straight roller. "
                 "Generated by compose/chirpers5/src/chirpers5-t9.py.",
        "tempo": BPM,
        "tail": "1.2s",                  # v2: no dead air into the closer
        "ceiling": "-1.0dB",
        "true_peak": True,
        "volume": "0dB",
        "buses": {"drums": {"fx": [{"type": "compressor", "threshold": "-16dB", "ratio": 4, "attack": "1ms",
                                     "release": "70ms", "makeup": "2dB"},
                                    "clip ceiling=-11dB knee=0.7 link=true"]},
                  "space": {"fx": ["reverb kind=room decay=1.6s mix=1 predelay=15ms", "hp cutoff=300", "lp cutoff=8000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=26", "peak cutoff=300 q=0.8 gain=-2dB",
                                                    "highshelf cutoff=9000 gain=-2dB"]},
                          {"type": "filter", "kind": "lp", "cutoff": {"value": 800, "mod": [{"src": "auto.lp", "amount": 18500}]}},
                          {"type": "tape", "drive": 0.2, "mix": 0.4, "hiss": "-68dB", "wow": 1, "flutter": 1, "seed": 9},
                          {"type": "compressor", "threshold": "-22dB", "ratio": 2.5, "attack": "15ms", "release": "150ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+13dB"},
                          {"type": "compressor", "threshold": "-5dB", "ratio": 10, "attack": "0.3ms", "release": "60ms",
                           "makeup": "0dB"},
                          "limiter ceiling=-1.2dB release=80ms"],
                   "auto": {"dyn": {"points": dyn}, "lp": {"points": lp}}},
        "tracks": [
            tr("kick", "tight-kit", gain="-4dB", out="drums"),
            tr("snare", "tight-kit", gain="-5dB", out="drums", sends={"space": "-14dB"}),
            tr("roll", "amen-chops", gain="-8dB", out="drums", fx=["hp cutoff=120", pump]),
            tr("bass", "bass-di", gain="-4dB", fx=[{"type": "eq", "bands": ["peak cutoff=150 q=0.9 gain=3dB"]},  # v3: body
                                                   {"type": "compressor", "threshold": "-18dB", "ratio": 4,
                                                    "attack": "5ms", "release": "80ms", "makeup": "3dB"}, pump]),
            tr("sub", "808", gain="-12dB", fx=[pump]),
            tr("keys", "epiano-tine synth.tine.sense=0.4 play.release.patch=epiano-damper play.release.decay=2s",
               gain="-7dB", pan=-0.2, sends={"space": "-10dB"},
               lfo={"kp": {"wave": "sine", "rate": "20b"}},
               fx=[{"type": "pan", "pan": {"value": -0.2, "mod": [{"src": "lfo.kp", "amount": 0.2}]}}]),
            tr("gtr", "cutting-guitar", gain="-10dB", pan=0.3, sends={"space": "-14dB"}),
            tr("horns", "horn-section", gain="-9dB", pan=0.1, sends={"space": "-8dB"}),
            tr("wah", "lead-wah", gain="-8dB", pan=-0.05, sends={"space": "-8dB"}),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars, {TOTAL * 60 / BPM:.0f} s")


if __name__ == "__main__":
    main()
