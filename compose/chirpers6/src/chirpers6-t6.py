#!/usr/bin/env python3
"""Chirpers - All the Lights Left On (Chirpers VI), track 6: THE LAST TRAIN (chirper-three).

Post-rock / post-metal in six movements, about ten minutes: a night journey. The THEME is a clean-guitar arpeggio
(Em9 | Cmaj7#11 | G6/B | Dsus2) with a long-note melody over it; it is never looped to fill time: it is stated alone,
answered, broken into fragments in the tunnel, ground into a five-eighths riff in the freight movement, sung augmented
over it, and returns in E MAJOR on arrival. Field sounds are part of the music: rain, wind, a train passing (rumble,
rail joints, a two-tone horn), radio static, and a station voice and a radio monologue made by the voice engine's
formants in a speech rhythm, words just out of reach.

  I   PLATFORM       1-24    rain, a train passing, the station voice; the lone guitar states the theme
  II  DEPARTURE      25-64   a second guitar answers, bass and drums enter patiently, the first crescendo (tremolo)
  III TUNNEL         65-88   everything drops: a drone, static, the radio monologue, the theme in fragments
  IV  FREIGHT        89-136  post-metal: the theme ground into a riff of FIVE eighths against the four, paired
                             chug rigs, fuzz bass; the melody augmented above it; a tremolo wall and feedback
  V   ARRIVAL        137-184 the theme in E major, the band climbing to the last peak; since v6 a wordless choir sings
                             the last peak (169-184)
  VI  EMPTY STATION  185-208 rain again, the station voice once more, the theme's first bar alone, unresolved
"""
import json
import os
import random

OUT = os.environ.get("C6T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers6-t6.yaml")
BPM = 84
BAR = 4.0
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SECTIONS = [("platform", 1, 24), ("departure", 25, 64), ("tunnel", 65, 88), ("freight", 89, 136),
            ("arrival", 137, 184), ("station", 185, 208)]
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
    return "station"


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


# THE THEME: eighth-note arpeggios, one chord a bar (MIDI), minor and (for the arrival) major
ARP_MINOR = [[52, 59, 66, 67, 71, 67, 66, 59],      # Em9      E3 B3 F#4 G4 B4 G4 F#4 B3
             [48, 55, 64, 66, 71, 66, 64, 55],      # Cmaj7#11 C3 G3 E4 F#4 B4 F#4 E4 G3
             [47, 55, 62, 64, 67, 64, 62, 55],      # G6/B     B2 G3 D4 E4 G4 E4 D4 G3
             [50, 57, 64, 69, 74, 69, 64, 57]]      # Dsus2    D3 A3 E4 A4 D5 A4 E4 A3
ARP_MAJOR = [[52, 59, 63, 68, 71, 68, 63, 59],      # E        E3 B3 D#4 G#4 B4 G#4 D#4 B3
             [49, 56, 64, 68, 71, 68, 64, 56],      # C#m7     C#3 G#3 E4 G#4 B4 G#4 E4 G#3
             [49, 57, 64, 69, 71, 69, 64, 57],      # Aadd9/C# C#3 A3 E4 A4 B4 A4 E4 A3
             [47, 54, 64, 66, 71, 66, 63, 54]]      # Bsus4->B B2 F#3 E4 F#4 B4 F#4 D#4 F#3
ROOTS_MINOR = [40, 36, 35, 38]                       # E2 C2 B1 D2
ROOTS_MAJOR = [40, 37, 33, 35]                       # E2 C#2 A1 B1
MELODY = [(0, 0, "B4", 4), (1, 0, "A4", 2), (1, 2, "G4", 2), (2, 0, "D5", 3), (2, 3, "B4", 1), (3, 0, "A4", 4)]
MELODY_MAJ = [(0, 0, "B4", 4), (1, 0, "C#5", 2), (1, 2, "B4", 2), (2, 0, "E5", 3), (2, 3, "C#5", 1), (3, 0, "D#5", 4)]


def shape(notes, bar):
    """v7, RETURNS CHANGE (chirper-one's note): each four-bar statement of the arpeggio takes a different shape -
    rising, falling (the same notes reversed), or with its top lifted an octave - so no phrase repeats exactly."""
    v = ((bar - 1) // 4) % 3
    if v == 1:
        return list(reversed(notes))
    if v == 2:
        return [m + 12 if k in (3, 4, 5) else m for k, m in enumerate(notes)]
    return list(notes)


def theme(bar, arp, vel, name="gtr1", every=1, octave=0):
    for k, m in enumerate(shape(arp[(bar - 1) % 4], bar)):
        if k % every:
            continue
        part(name).add(b0(bar) + k / 2, 0.55 * every, nm(m + octave), vel - (6 if k % 2 else 0))


def field():
    """Rain, wind, the train passing, static (the field layer)."""
    for a, z, v in ((1, 26, 64), (65, 89, 52), (183, 209, 70)):
        part("rain").add(b0(a), b0(z) - b0(a) - 0.1, "C4", v)
    part("wind").add(b0(65), b0(89) - b0(65) - 0.1, "C4", 56)
    part("wind").add(b0(187), b0(209) - b0(187) - 0.1, "C4", 50)
    # THE TRAIN (bars 3-10): a rumble swelling and fading, rail joints clacking in pairs, a two-tone horn
    part("rumble").add(b0(3), b0(11) - b0(3), "E1", 80)
    x, gap = b0(4), 1.2
    while x < b0(10):
        for d in (0.0, 0.22):
            part("clack").add(x + d, 0.15, "rs", 70)
        x += gap
        gap = max(0.55, gap * 0.94) if x < b0(7) else min(1.4, gap * 1.08)
    for at in (b0(5) + 2, b0(5) + 3.2):
        part("horn").add(at, 1.0, "A3,C#4", 72)
    part("static").add(b0(65), b0(89) - b0(65) - 0.1, "C4", 66)


# THE STATION VOICE speaks (v3, ARPAbet through chirp's voice engine, as chirper-two's The Mast does): the platform's
# announcement, and at the end, slower and lower, its answer (the album's title in it)
PA_FIRST = [["p-l-ae1-t", "f-ao1-r-m", "t-uw1"], ["dh-ah0", "l-ae1-s-t", "t-r-ey1-n", "ih1-z", "n-aw1", "d-ih0", "p-aa1-r", "t-ih0-ng"]]
RADIO_WORDS = [["ih1-z", "eh1-n", "iy0", "w-ah2-n", "s-t-ih1-l", "ah0", "w-ey1-k"],
               ["dh-ah0", "l-ay1-n-z", "aa1-r", "d-aw1-n", "p-ae1-s-t", "dh-ah0", "r-ih1", "v-er0"],
               ["k-iy1-p", "g-ow1", "ih0-ng"], ["k-iy1-p", "g-ow1", "ih0-ng"]]
PA_LAST = [["dh-ah0", "l-ae1-s-t", "t-r-ey1-n", "hh-ae1-z", "g-ao1-n"], ["dh-ah0", "l-ay1-t-s", "aa1-r", "l-eh1-f-t", "aa1-n"]]


def speak(name, start, lines, step=0.6, base="A2"):
    t = start
    for line in lines:
        for k, syl in enumerate(line):
            last = k == len(line) - 1
            f0 = "0>-30>-90" if last else ("0>15>0" if k == 0 else "0>-10")
            part(name).add(t, 0.92 * step, f"{base}^ph={syl}^f0={f0}", 86 - (6 if syl.endswith("0") else 0))
            t += step
        t += 1.5                                             # a breath between lines
    return t


def voices():
    """THE STATION VOICE (bars 5-6 and, changed and slower, 189-190) and THE RADIO MONOLOGUE (the tunnel): the voice
    engine's formants gliding vowel to vowel in a speech rhythm, words just out of reach through a band-pass."""
    speak("pa", b0(5), PA_FIRST)
    speak("pa", b0(189), PA_LAST, step=0.8, base="G2")      # slower, lower: the last announcement
    # THE RADIO IN THE TUNNEL (v5): a broadcast drifting in and out: wordless murmur between stations, and three
    # phrases surfacing from the static - a voice someone in the dark is tuning towards
    hand = random.Random(66)
    for a, z in ((69, 71), (74, 77), (80, 83)):
        x = b0(a)
        while x < b0(z):
            phrase = hand.randint(4, 8)
            pitch = hand.choice([50, 52, 53])
            for i in range(phrase):
                ln = hand.choice([0.25, 0.25, 0.5, 0.5, 0.75])
                part("radio").add(x, ln * 0.85, nm(pitch + hand.choice([0, 0, 2, -1, 3]) - (i // 4)), 70 + hand.randint(-8, 8))
                x += ln
            x += hand.choice([0.75, 1.0, 1.5])
    speak("words", b0(71), [RADIO_WORDS[0]], step=0.7, base="F#2")
    speak("words", b0(77), [RADIO_WORDS[1]], step=0.7, base="F#2")
    speak("words", b0(83), RADIO_WORDS[2:], step=0.8, base="F#2")

def platform_departure():
    hand = random.Random(1)
    for bar in range(13, 65):
        sec = sec_of(bar)
        theme(bar, ARP_MINOR, 70 if bar < 25 else 76, "gtr1", every=2 if bar < 17 else 1)
        if bar >= 33:                                                   # the second guitar answers: the melody
            for bo, s, n, ln in MELODY:
                if (bar - 33) % 4 == bo:
                    part("gtr2").add(b0(bar) + s, ln * 0.95, n, 74)
        if bar >= 33:
            part("bass").add(b0(bar), 3.9, nm(ROOTS_MINOR[(bar - 1) % 4]), 84)
            if bar >= 41:
                part("sub").add(b0(bar), 3.9, nm(ROOTS_MINOR[(bar - 1) % 4] - 12), 90)
        if 41 <= bar < 49:                                              # drums enter patiently: toms and ride
            for b in range(4):
                part("kit").add(b0(bar) + b, 0.5, "rd", 60 + 4 * (bar - 41))
            part("kit").add(b0(bar), 0.5, "t2", 70)
        if bar >= 49:
            if bar % 4 == 0:                                           # v7: a tom fill closing each phrase
                for j, piece in enumerate(("t1", "t1", "t2", "t3")):
                    part("kit").add(b0(bar) + 3 + j / 4, 0.25, piece, 104 + 4 * j)
            for b in range(4):
                part("kit").add(b0(bar) + b, 0.5, "k" if b in (0, 2) else "s", 96 if b in (1, 3) else 100)
                part("kit").add(b0(bar) + b + 0.5, 0.25, "h" if bar < 57 else "c", 70 if bar < 57 else 84)
            # THE TREMOLO: a clean guitar picking chord tones in sixteenths, rising through the crescendo
            for k in range(16):
                m = ARP_MINOR[(bar - 1) % 4][4 + (k // 4) % 4]
                part("trem").add(b0(bar) + k / 4, 0.24, nm(m + 12), 58 + (bar - 49) * 3 + hand.randint(-4, 4))


def tunnel():
    part("drone").add(b0(65), b0(89) - b0(65) - 0.1, "E2,B2", 70)
    # the theme in FRAGMENTS: two or three notes of the arpeggio, far apart, through a long delay
    for bar in (67, 70, 74, 77, 81, 84):
        arp = ARP_MINOR[(bar - 1) % 4]
        for k in (0, 2, 4)[: 2 + bar % 2]:
            part("frag").add(b0(bar) + k, 1.5, nm(arp[k] + 12), 62)


RIFF = [0, 0, 3, 2, -2]       # THE RIFF (v3): FIVE eighths against the four, the theme's intervals ground low
# (E E G F# D); the seven-against-four is chirper-zero's Night Freight


def freight():
    hand = random.Random(4)
    x, i = b0(89), 0
    while x < b0(133):
        iv = RIFF[i % 5]
        breath = any(b0(br) + 2 <= x < b0(br + 1) for br in (104, 120))   # v7: the riff stops for half a bar
        if iv is not None and not breath:
            m = 28 + iv                                                  # E1 (an 8-string's low E)
            v = 108 if i % 5 == 0 else 92
            for side in ("chugl", "chugr"):
                part(side).add(x, 0.45, nm(m), v + hand.randint(-4, 4))
            part("fbass").add(x, 0.45, nm(m + 12), v)
            if i % 5 in (0, 3):
                part("kit").add(x, 0.5, "k", 110)
        x += 0.5
        i += 1
    for bar in range(89, 133):
        part("kit").add(b0(bar) + 2, 0.5, "s", 112)                       # half-time snare on 3
        if bar % 8 == 0 and bar not in (104, 120):                         # v7: a snare roll into the next phrase
            for j in range(8):
                part("kit").add(b0(bar) + 2 + j / 4, 0.25, "s", 100 + 2 * j)
        for b in range(4):
            part("kit").add(b0(bar) + b, 0.5, "rd" if bar < 105 else "c", 76)
        if bar >= 113:                                                    # the melody AUGMENTED over the riff
            for bo, s, n, ln in MELODY:
                if (bar - 113) % 8 == 2 * bo:
                    part("lead").add(b0(bar) + 2 * s, 2 * ln * 0.97, n, 88)
        if bar >= 121:                                                    # THE TREMOLO WALL
            for k in range(16):
                part("wall").add(b0(bar) + k / 4, 0.24, "E3,B3,E4", 70 + (bar - 121) * 3)
    part("fbk").add(b0(133), 4 * BAR - 0.1, "B4", 90)                     # feedback: one note, held, howling


def arrival():
    hand = random.Random(5)
    for bar in range(137, 185):
        theme(bar, ARP_MAJOR, 78, "gtr1")
        if bar >= 145:
            for bo, s, n, ln in MELODY_MAJ:
                if (bar - 145) % 4 == bo:
                    part("lead").add(b0(bar) + s, ln * 0.95, n, 90 if bar >= 161 else 80)
        part("bass").add(b0(bar), 3.9, nm(ROOTS_MAJOR[(bar - 1) % 4]), 88)
        part("sub").add(b0(bar), 3.9, nm(ROOTS_MAJOR[(bar - 1) % 4] - 12), 92)
        if bar >= 141 and bar % 4 == 0:                                   # v7: a tom fill closing each phrase
            for j, piece in enumerate(("t1", "t2", "t3", "t3")):
                part("kit").add(b0(bar) + 3 + j / 4, 0.25, piece, 106 + 3 * j)
        if bar >= 141:
            for k in range(8):                                             # driving eighths on the floor tom
                part("kit").add(b0(bar) + k / 2, 0.4, "t3" if bar < 153 else "k", 84 if k % 2 else 96)
            if bar >= 153:
                part("kit").add(b0(bar) + 1, 0.5, "s", 106)
                part("kit").add(b0(bar) + 3, 0.5, "s", 108)
                part("kit").add(b0(bar), 0.5, "c", 96 if bar % 4 == 1 else 80)
        if bar >= 161:                                                     # the tremolo, high, soaring
            for k in range(16):
                m = ARP_MAJOR[(bar - 1) % 4][4 + (k // 4) % 4]
                part("trem").add(b0(bar) + k / 4, 0.24, nm(m + 12), 70 + hand.randint(-4, 4))


CHORDS_MAJOR = [[52, 56, 59, 64], [49, 56, 61, 64], [49, 57, 61, 64], [47, 54, 59, 63]]   # E C#m7 A/C# B (choir)


def choir():
    """THE ARRIVAL SINGS (v6): at the last peak only (bars 169-184), a wordless choir: the arrival's chords held and
    the E-major melody in long notes an octave down, swelling bar by bar. The journey has had machines, rain and broken
    radios; at the arrival, voices."""
    for bar in range(169, 185):
        k = (bar - 1) % 4
        v = 56 + (bar - 169) * 3
        part("choir").add(b0(bar), BAR - 0.1, ",".join(nm(m) for m in CHORDS_MAJOR[k]), v)
        for bo, s, n, ln in MELODY_MAJ:
            if (bar - 169) % 4 == bo:
                base, octv = n[:-1], int(n[-1]) - 1
                part("choirlead").add(b0(bar) + s, ln * 0.97, f"{base}{octv}", v + 10)


def station():
    for bar in (193, 194, 197, 198, 201):                                 # the theme's first bar, alone, sparse
        theme(bar, ARP_MINOR, 60, "gtr1", every=2)


LEVEL = {"platform": -10, "departure": -4, "tunnel": -12, "freight": 0, "arrival": 0, "station": -11}


def dyn_lane():
    sec = lambda beats: beats * 60 / BPM
    pts = []
    for name, a, z in SECTIONS:
        t0 = sec(b0(a))
        if pts:
            pts.append([f"{max(0.0, t0 - 0.3):.3f}s", pts[-1][1]])
        pts.append([f"{t0:.3f}s", float(LEVEL[name])])
    # the departure's crescendo: from -6 at bar 41 to 0 at the peak (bar 57)
    pts = [p for p in pts if not (sec(b0(41)) < float(p[0][:-1]) < sec(b0(65)))]
    i = [k for k, p in enumerate(pts) if float(p[0][:-1]) >= sec(b0(65))][0]
    pts[i:i] = [[f"{sec(b0(41)):.3f}s", -6.0], [f"{sec(b0(57)):.3f}s", 0.0], [f"{sec(b0(65)) - 0.3:.3f}s", 0.0]]
    return pts


def em_lane():
    """The low-pass closed at Freight's first downbeat (400 Hz), opening over four bars."""
    sec = lambda beats: beats * 60 / BPM
    a = b0(89)
    pts = [(0, 0.0), (a - 0.05, 0.0), (a, 1.0), (a + 4, 0.8), (a + 8, 0.5), (a + 12, 0.2), (a + 16, 0.0), (TOTAL, 0.0)]
    # (a frequency's mod amount is in OCTAVES: -5 x 1 = 18 kHz / 32 = ~560 Hz; -17600 or -60 silenced the section)
    return [[f"{sec(b):.3f}s", v] for b, v in pts]


def ts_lane():
    """The tape stop over Arrival's last two beats (bar 184, beats 3-4); released as the empty station begins."""
    sec = lambda beats: beats * 60 / BPM
    a = b0(184) + 2
    pts = [(0, 0.0), (a - 0.02, 0.0), (a, 1.0), (b0(185) - 0.02, 1.0), (b0(185), 0.0), (TOTAL, 0.0)]
    return [[f"{sec(b):.3f}s", v] for b, v in pts]


def main():
    field()
    voices()
    platform_departure()
    tunnel()
    freight()
    arrival()
    station()
    choir()
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    # THE TUNING (v5): the radio's band-pass drifts +-0.6 octave around 1.4 kHz on a 7-bar LFO (OCTAVES), crushed
    TUNING = [{"type": "filter", "kind": "bp", "q": 1.1, "cutoff": {"value": 1400, "mod": [{"src": "lfo.tune", "amount": 0.6}]}},
              {"type": "crush", "bits": 8, "rate": 11000, "mix": 0.5}]
    radio_fx = [{"type": "filter", "kind": "bp", "cutoff": 1400, "q": 1.2}, {"type": "crush", "bits": 8, "rate": 11000, "mix": 0.6}]
    song = {
        "about": "Chirpers - All the Lights Left On (Chirpers VI), track 6 by chirper-three: THE LAST TRAIN. Post-rock / "
                 "post-metal in six movements: a night journey from a rainy platform through a tunnel and a freight "
                 "movement to an arrival, the theme transformed each time. Generated by compose/chirpers6/src/chirpers6-t6.py.",
        "tempo": BPM,
        "tail": "4s",
        "ceiling": "-1.0dB",
        "true_peak": True,
        "volume": "0dB",
        "patches": {"c6-voice": {"synth": {"layers": ["saw", "pulse level=-6dB", {"type": "noise", "level": "-18dB"}],
                                           "amp": {"a": "15ms", "d": "60ms", "s": 0.7, "r": "60ms"},
                                           "fx": [{"type": "formant", "q": 7, "mix": 1,
                                                   "vowel": {"value": 0.5, "mod": [{"src": "rand", "amount": 0.5}]}}]}},
                    "c6-horn": {"synth": {"layers": ["saw", "square level=-6dB"], "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "200ms"},
                                          "filters": ["lp cutoff=1200"]}},
                    "c6-rumble": {"synth": {"layers": [{"type": "noise", "color": "brown"}], "amp": {"a": "6s", "d": "0s", "s": 1, "r": "6s"},
                                            "filters": ["lp cutoff=180"]}},
                    "c6-static": {"synth": {"layers": [{"type": "noise"}], "amp": {"a": "2s", "d": "0s", "s": 1, "r": "2s"},
                                            "filters": ["bp cutoff=3000 q=0.7"]}},
                    "c6-drone": {"synth": {"layers": ["saw", "saw detune=7"], "amp": {"a": "4s", "d": "0s", "s": 1, "r": "4s"},
                                           "filters": ["lp cutoff=500"]}}},
        "buses": {"hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=40ms", "hp cutoff=200"]},
                  "station": {"fx": ["reverb kind=hall decay=2.5s mix=0.5 predelay=60ms", "hp cutoff=300", "lp cutoff=4000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=350 q=0.8 gain=-1dB",
                                                    "highshelf cutoff=5000 gain=-4dB"]},   # v2: darker, the low end kept
                          # v4: THE TRAIN LEAVES THE TUNNEL: Freight starts behind a closed low-pass that opens over its
                          # first four bars, the riff approaching muffled then bursting into the open
                          {"type": "filter", "kind": "lp",
                           "cutoff": {"value": 18000, "mod": [{"src": "auto.em", "amount": -5}]}},   # (OCTAVES)
                          # v4: THE TRAIN STOPS: the end of Arrival winds down on a tape stop, a train braking to a halt
                          {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]},
                           "time": "2b", "up": "0.05b", "curve": 0.6, "mix": 1},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2, "attack": "20ms", "release": "200ms",
                           "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          {"type": "gain", "gain": "+10dB"},
                          "limiter ceiling=-1.2dB release=120ms"],
                   "auto": {"dyn": {"points": dyn_lane()}, "em": {"points": em_lane()}, "ts": {"points": ts_lane()}}},
        "tracks": [
            tr("rain", "rain", gain="-14dB"),
            tr("wind", "wind", gain="-16dB"),
            tr("rumble", "c6-rumble", gain="-6dB", lfo={"rp": {"wave": "sine", "rate": "32b"}},
               fx=["hp cutoff=45", {"type": "pan", "pan": {"value": 0, "mod": [{"src": "lfo.rp", "amount": 0.7}]}}]),
            tr("clack", "metal-kit-phys", gain="-14dB", fx=["lp cutoff=2500"], sends={"hall": "-10dB"}),
            tr("horn", "c6-horn", gain="-16dB", sends={"hall": "-4dB"}),
            tr("static", "c6-static", gain="-26dB", fx=[{"type": "crush", "bits": 6, "rate": 8000, "mix": 0.5}]),
            tr("pa", "voice-speech", gain="-6dB", fx=[{"type": "filter", "kind": "bp", "cutoff": 1500, "q": 0.9},
                                                     {"type": "crush", "bits": 10, "rate": 16000, "mix": 0.4}],
               sends={"station": "-2dB"}),          # v3: the station voice SPEAKS, through a PA
            tr("radio", "c6-voice", gain="-13dB", lfo={"tune": {"wave": "sine", "rate": "28b"}},
               fx=TUNING + [{"type": "pitch", "semitones": 0, "formant": -2}]),     # between stations
            tr("words", "voice-speech", gain="-5dB", lfo={"tune": {"wave": "sine", "rate": "28b"}},
               fx=TUNING, sends={"hall": "-14dB"}),                                  # v5: the radio's words
            tr("gtr1", "starcaster-clean", gain="-8dB", pan=-0.3, sends={"hall": "-10dB"}),
            tr("gtr2", "m8-clean", gain="-10dB", pan=0.3, sends={"hall": "-8dB"}),
            tr("trem", "m8-clean", gain="-13dB", pan=0.15, sends={"hall": "-6dB"}),
            tr("frag", "starcaster-clean", gain="-10dB", pan=0.2, sends={"hall": "-2dB"},
               fx=[{"type": "delay", "time": "3/8", "feedback": 0.55, "mix": 0.45}]),
            tr("drone", "c6-drone", gain="-18dB", fx=["hp cutoff=50"], sends={"hall": "-6dB"}, lfo={"df": {"wave": "sine", "rate": "28b"}}),
            tr("bass", "bass-fuzz", gain="-5dB"),
            tr("sub", "808", gain="-12dB", fx=[{"type": "pump", "on": "kit.k", "depth": "-6dB", "release": "400ms",
                                               "curve": 0.6}]),   # v2: a sub under the theme's movements
            tr("kit", "room-kit", gain="-3dB", sends={"hall": "-14dB"}),
            tr("chugl", "m8-chug-l", gain="-10dB", pan=-0.7),
            tr("chugr", "m8-chug-r", gain="-10dB", pan=0.7),
            tr("fbass", "m8-bass-dist", gain="-6dB"),
            tr("lead", "lead-tape", gain="-9dB", sends={"hall": "-8dB"}),
            tr("wall", "m8-fuzz", gain="-16dB", sends={"hall": "-6dB"}),
            tr("fbk", "m8-fuzz", gain="-14dB", sends={"hall": "-4dB"}),
            tr("choir", "choir", gain="-10dB", sends={"hall": "-4dB"}),              # v6: the arrival sings
            tr("choirlead", "choir", gain="-8dB", pan=0.05, sends={"hall": "-4dB"}),
        ],
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {BARS} bars, {TOTAL * 60 / BPM:.0f} s")


if __name__ == "__main__":
    main()
