#!/usr/bin/env python3
"""Chirpers - All the Lights Left On (Chirpers VI), track 2: EVERY WINDOW (chirper-three).

ORCHESTRAL POST-ROCK (Mono's vein): a town seen from a hill at night, every window a life, and at dawn the windows
going dark one by one. Strings (violin, a cello section, contrabass), piano, celesta, a music box, brass, and the
band's tremolo guitars as part of the orchestra. One WINDOW THEME (8 bars over Dmaj7 | Bm9 | Gmaj7#11 | A6sus) is
heard through each window in a different voice, darkened at midnight, augmented by the brass at the summit, and
left to the piano alone at dawn.

  I    THE HILL           1-16    wind and the town's far murmur; a lone piano states the window theme
  II   WINDOWS            17-48   four windows, four lives, on the same harmony: celesta and cello; a kitchen radio
                                  playing a waltz (tinny, crackling); a music box; a violin alone
  III  THE STREETS        49-80   tremolo guitars, bass and drums join the strings: the first crescendo
  IV   MIDNIGHT           81-96   it drops to piano and cellos, the theme in B minor, and a bell strikes twelve
  V    ALL THE WINDOWS    97-128  the long crescendo: tremolo walls, full strings and contrabass, the brass carrying the
                                  theme augmented, rolling toms
  VI   DAWN               129-152 a farewell: every few bars one instrument leaves (a window going dark), until the
                                  piano is alone with the theme's first phrase, and the wind; since v3 the strings
                                  hold a soft B and F# under it: the day begins in B minor
"""
import json
import os
import random

OUT = os.environ.get("C6T2_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers6-t2.yaml")
BPM = 72
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SECTIONS = [("hill", 1, 16), ("windows", 17, 48), ("streets", 49, 80), ("midnight", 81, 96), ("all", 97, 128),
            ("dawn", 129, 152)]
BARS = SECTIONS[-1][2]
TOTAL = BARS * BAR


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def b0(bar):
    return (bar - 1) * BAR


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return "dawn"


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


# a chord a bar: (root for bass, voicing)
MAJOR = [(38, [54, 57, 61, 64]),     # Dmaj7    F#3 A3 C#4 E4
         (35, [54, 57, 61, 62]),     # Bm9      F#3 A3 C#4 D4
         (31, [54, 59, 61, 62]),     # Gmaj7#11 F#3 B3 C#4 D4
         (33, [52, 57, 59, 62])]     # A6sus    E3 A3 B3 D4
MINOR = [(35, [54, 59, 62, 66]),     # Bm       F#3 B3 D4 F#4
         (31, [55, 59, 62, 66]),     # Gmaj7    G3 B3 D4 F#4
         (28, [52, 55, 59, 62]),     # Em7      E3 G3 B3 D4
         (30, [54, 58, 61, 64])]     # F#7      F#3 A#3 C#4 E4
# THE WINDOW THEME (8 bars): (bar, beat, midi, beats)
THEME = [(0, 0, 78, 1.5), (0, 1.5, 76, 0.5), (0, 2, 74, 2), (1, 0, 73, 3), (1, 3, 71, 1), (2, 0, 74, 1.5),
         (2, 1.5, 73, 0.5), (2, 2, 71, 2), (3, 0, 69, 4), (4, 0, 78, 1.5), (4, 1.5, 81, 0.5), (4, 2, 78, 2),
         (5, 0, 76, 3), (5, 3, 74, 1), (6, 0, 73, 1.5), (6, 1.5, 71, 0.5), (6, 2, 67, 2), (7, 0, 69, 4)]
# in B minor at midnight: the same contour, darkened (each note lowered to the minor scale's nearest tone)
B_MINOR = {78: 78, 76: 76, 74: 74, 73: 73, 71: 71, 69: 69, 81: 79, 67: 67}


def theme(name, start_bar, vel, shift=0, scale=1.0, mapping=None, bars=8, legato=0.95):
    for b, beat, m, ln in THEME:
        if b >= bars:
            continue
        mm = (mapping or {}).get(m, m) + shift
        part(name).add(b0(start_bar) + (b * BAR + beat) * scale, ln * scale * legato, nm(mm), vel)


def chords(name, a, z, table, vel, octave=0, every=1):
    for bar in range(a, z + 1):
        if (bar - a) % every:
            continue
        root, v = table[(bar - 1) % 4]
        part(name).add(b0(bar), BAR * every - 0.1, ",".join(nm(m + octave) for m in v), vel)


def field():
    part("wind").add(b0(1), b0(25) - 0.1, "C4", 62)
    part("town").add(b0(1), b0(49) - 0.1, "C4", 52)
    part("wind").add(b0(137), b0(153) - b0(137) - 0.1, "C4", 66)


def hill():
    theme("piano", 5, 70)
    chords("piano", 5, 12, MAJOR, 46, octave=-12)


def windows():
    hand = random.Random(2)
    # (a) celesta and cello: the theme an octave up on celesta, the cello answering on the roots
    theme("celesta", 17, 72)
    for bar in range(17, 25):
        root, v = MAJOR[(bar - 1) % 4]
        part("cello").add(b0(bar), 3.8, nm(root + 12), 70)
    # (b) a kitchen radio: a waltz-like lilt (one-two-three over the four), tinny strings, crackle
    for bar in range(25, 33):
        root, v = MAJOR[(bar - 1) % 4]
        for k, beat in enumerate((0, 1.333, 2.667)):
            part("radio").add(b0(bar) + beat, 1.2, nm(root + 24) if k == 0 else ",".join(nm(m + 12) for m in v[1:3]),
                              66 if k == 0 else 54)
    theme("radio", 25, 62, shift=0, bars=8)
    part("crackle").add(b0(25), b0(33) - b0(25) - 0.1, "C4", 60)
    # (c) a music box: the theme twice as fast, high, a little worn
    theme("mbox", 33, 76, shift=12, scale=0.5)
    theme("mbox", 37, 72, shift=12, scale=0.5)
    # (d) a violin alone: the theme slow and singing, a pad beneath
    theme("violin", 41, 78, shift=-12)
    chords("strings", 41, 48, MAJOR, 48, every=2)
    del hand


def streets():
    hand = random.Random(3)
    for bar in range(49, 81):
        root, v = MAJOR[(bar - 1) % 4]
        part("bass").add(b0(bar), 3.8, nm(root + (12 if root < 38 else 0)), 84)
        part("strings").add(b0(bar), 3.9, ",".join(nm(m + 12) for m in v), 56 + (bar - 49))
        for k in range(16):                                           # tremolo: chord tones in sixteenths
            m = v[(k // 4) % 4] + 12
            part("trem").add(b0(bar) + k / 4, 0.24, nm(m), 52 + (bar - 49) + hand.randint(-4, 4))
        if bar >= 57:
            for b in range(4):
                part("kit").add(b0(bar) + b, 0.5, "k" if b in (0, 2) else "s", 88 + (bar - 57) // 2)
                part("kit").add(b0(bar) + b + 0.5, 0.25, "rd", 60 + (bar - 57))
        else:
            part("kit").add(b0(bar), 0.5, "t2", 62 + 2 * (bar - 49))
    theme("lead", 57, 84)
    theme("lead", 65, 88)
    theme("lead", 73, 94, shift=12)
    for bar in (73, 77):
        part("kit").add(b0(bar), 1.0, "c", 100)


def midnight():
    chords("cellos", 81, 96, MINOR, 66, octave=-12)
    theme("piano", 81, 62, mapping=B_MINOR, shift=-12)
    theme("piano", 89, 58, mapping=B_MINOR, shift=-12, bars=4)
    for k in range(12):                                               # a bell strikes twelve
        part("bell").add(b0(87) + k * 1.5, 1.4, "D3", 92 - 2 * k)


def all_windows():
    hand = random.Random(5)
    for bar in range(97, 129):
        root, v = MAJOR[(bar - 1) % 4]
        g = bar - 97
        part("bass").add(b0(bar), 3.8, nm(root + (12 if root < 38 else 0)), 92)
        part("cb").add(b0(bar), 3.9, nm(root), 70 + g // 2)            # the contrabass under everything
        part("strings").add(b0(bar), 3.9, ",".join(nm(m + 12) for m in v), 64 + g)
        part("cellos").add(b0(bar), 3.9, nm(root + 12) + "," + nm(v[0]), 64 + g)
        for k in range(16):
            m = v[(k // 4) % 4] + 12
            part("trem").add(b0(bar) + k / 4, 0.24, nm(m), 64 + g // 2 + hand.randint(-4, 4))
            if bar >= 113:
                part("wall").add(b0(bar) + k / 4, 0.24, nm(v[(k // 2) % 4] + 24), 70 + (bar - 113) * 2)
        if bar < 105:                                                 # rolling toms, building
            for k in range(8):
                part("kit").add(b0(bar) + k / 2, 0.4, "t3" if k % 2 else "t2", 70 + g * 2)
        else:
            for b in range(4):
                part("kit").add(b0(bar) + b, 0.5, "k" if b in (0, 2) else "s", 104)
                part("kit").add(b0(bar) + b + 0.5, 0.25, "c" if bar >= 121 else "rd", 80)
    # THE BRASS carries the theme AUGMENTED (twice as slow) from the summit's approach
    theme("brass", 105, 92, shift=-12, scale=2.0, bars=8)
    theme("violin", 121, 96, shift=0, bars=8)


# DAWN: the farewell - each window goes dark: (instrument, last bar it plays)
FAREWELL = [("brass", 130), ("kit", 132), ("wall", 132), ("trem", 134), ("bass", 136), ("cb", 138),
            ("strings", 140), ("cellos", 142), ("violin", 144)]


def dawn():
    hand = random.Random(6)
    for bar in range(129, 145):
        root, v = MAJOR[(bar - 1) % 4]
        alive = {n for n, last in FAREWELL if bar <= last}
        if "brass" in alive:
            part("brass").add(b0(bar), 3.9, ",".join(nm(m - 12) for m in v[:3]), 76)
        if "kit" in alive:
            for b in range(4):
                part("kit").add(b0(bar) + b, 0.5, "k" if b in (0, 2) else "s", 90)
        if "wall" in alive:
            for k in range(16):
                part("wall").add(b0(bar) + k / 4, 0.24, nm(v[(k // 2) % 4] + 24), 76)
        if "trem" in alive:
            for k in range(16):
                part("trem").add(b0(bar) + k / 4, 0.24, nm(v[(k // 4) % 4] + 12), 64 + hand.randint(-4, 4))
        if "bass" in alive:
            part("bass").add(b0(bar), 3.8, nm(root + (12 if root < 38 else 0)), 84)
        if "cb" in alive:
            part("cb").add(b0(bar), 3.9, nm(root), 70)
        if "strings" in alive:
            part("strings").add(b0(bar), 3.9, ",".join(nm(m + 12) for m in v), 64)
        if "cellos" in alive:
            part("cellos").add(b0(bar), 3.9, nm(root + 12), 64)
    theme("violin", 137, 74, bars=8)
    theme("piano", 145, 60, bars=4)                                   # the piano alone: the theme's first phrase
    # v3: THE DAY BEGINS IN B MINOR: under the wind, the strings hold a soft B and F# for the last four bars, the
    # piano's half cadence on A answered by the relative minor; it carries into Night Freight's B-minor quayside
    part("strings").add(b0(149), 4 * BAR - 0.2, "B3,F#4", 40)
    part("cb").add(b0(149) + 2, 4 * BAR - 2.2, "B1", 34)


LEVEL = {"hill": -10, "windows": -8, "streets": -3, "midnight": -9, "all": 0, "dawn": -6}


def dyn_lane():
    sec = lambda beats: beats * 60 / BPM
    pts = []
    for name, a, z in SECTIONS:
        t0 = sec(b0(a))
        if pts:
            pts.append([f"{max(0.0, t0 - 0.4):.3f}s", pts[-1][1]])
        pts.append([f"{t0:.3f}s", float(LEVEL[name])])
    return pts


def main():
    field()
    hill()
    windows()
    streets()
    midnight()
    all_windows()
    dawn()
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "Chirpers - All the Lights Left On (Chirpers VI), track 2 by chirper-three: EVERY WINDOW. Orchestral "
                 "post-rock: a town seen from a hill at night, every window a life, and at dawn the instruments leave "
                 "one by one as the windows go dark. Generated by compose/chirpers6/src/chirpers6-t2.py.",
        "tempo": BPM,
        "tail": "1.2s",                  # v3: no dead air into Night Freight
        "ceiling": "-1.0dB",
        "true_peak": True,
        "patches": {"c2-bell": {"synth": {"layers": [{"type": "additive", "partials": [[0.5, 0.6], [1, 1.0], [1.19, 0.5],
                                                                                        [1.56, 0.45], [2, 0.4], [2.51, 0.3],
                                                                                        [3.0, 0.2], [4.07, 0.15]]}],
                                          "amp": {"a": "2ms", "d": "4s", "s": 0, "r": "3s"}}}},
        "buses": {"hall": {"fx": ["reverb kind=hall decay=4.8s mix=1 predelay=45ms", "hp cutoff=180"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=42", "peak cutoff=300 q=0.9 gain=-4dB",
                                                    "highshelf cutoff=6000 gain=1dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2, "attack": "25ms", "release": "250ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+11dB"},
                          "limiter ceiling=-1.2dB release=120ms"],
                   "auto": {"dyn": {"points": dyn_lane()}}},
        "tracks": [
            tr("wind", "wind", gain="-16dB", fx=["hp cutoff=60"]),
            tr("town", "sm-crowd", gain="-30dB", fx=["lp cutoff=1200"], sends={"hall": "-6dB"}),   # the far town
            tr("piano", "piano", gain="-6dB", sends={"hall": "-8dB"}),
            tr("celesta", "celesta", gain="-10dB", pan=0.2, sends={"hall": "-6dB"}),
            tr("cello", "cello", gain="-8dB", pan=-0.2, sends={"hall": "-8dB"}),
            tr("radio", "strings-saw", gain="-14dB", pan=0.35,
               fx=[{"type": "filter", "kind": "bp", "cutoff": 1300, "q": 1.2}, {"type": "crush", "bits": 8, "rate": 9000, "mix": 0.5}]),
            tr("crackle", "rain", gain="-30dB", fx=["hp cutoff=2000"], pan=0.35),
            tr("mbox", "music-box", gain="-10dB", pan=-0.3, sends={"hall": "-6dB"}),
            tr("violin", "violin", gain="-8dB", pan=0.15, sends={"hall": "-6dB"}),
            tr("strings", "strings", gain="-10dB", sends={"hall": "-6dB"}),
            tr("cellos", "cellos", gain="-9dB", pan=-0.25, sends={"hall": "-8dB"}),
            tr("cb", "contrabass", gain="-5dB", sends={"hall": "-12dB"}),
            tr("bass", "bass-pick-di", gain="-4dB"),
            tr("trem", "m8-clean", gain="-13dB", pan=0.3, sends={"hall": "-6dB"}),
            tr("wall", "m8-fuzz", gain="-18dB", pan=-0.3, sends={"hall": "-6dB"}),
            tr("lead", "starcaster-clean", gain="-8dB", pan=-0.1, sends={"hall": "-8dB"}),
            tr("brass", "brass", gain="-10dB", sends={"hall": "-6dB"}),
            tr("bell", "c2-bell", gain="-12dB", sends={"hall": "-2dB"}),
            tr("kit", "room-kit", gain="-5dB", sends={"hall": "-12dB"}),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars, {TOTAL * 60 / BPM:.0f} s")


if __name__ == "__main__":
    main()
