#!/usr/bin/env python3
"""chirpers2-t4 (Odd Hours, track 4). Composed by chirper-two: a CHAMBER JAZZ BRUSH TRIO with a singing tom choir.

Everything is a palindrome:
- METERS, bar by bar: 3/4 5/8 7/8 4/4 7/8 5/8 3/4 (44 eighths a phrase). The bridge reads it from the centre out
  (4/4 7/8 5/8 3/4 5/8 7/8 4/4). Swung eighths in the 3/4 and 4/4 bars, straight in the odd ones.
- HARMONY: Dm9 | Bbmaj7#11 | G13sus | CENTRE | G13sus | Bbmaj7#11 | Dm9. The centre bar's chords move each time the
  phrase comes round (the only door out of the mirror). Harmonic rhythm breathes with the meter: one chord in 3/4
  and 5/8 bars, two in 7/8 (4+3) and in 4/4.
- MELODY: each bar's line is the retrograde (pitch and rhythm) of its mirror bar's, so the whole head reads the same
  backwards, and the centre bar is a palindrome itself.
- ORCHESTRATION: the melody passes bar by bar (klangfarbenmelodie) trumpet -> piano -> tom choir -> trumpet ->
  tom choir -> piano -> trumpet, a palindrome of colours.
The TOM CHOIR is a melodic instrument made of physical membrane toms (chirp `type: drum`, bd-7d117e: tuned with
`tune_sounding`, two-mic `stereo`); the kit plays BRUSHES (`beater: brush`, taps and `sweep`s).

Emits songs/chirpers2-t4.yaml. Edit the music here.
"""
import json
import os

OUT = os.environ.get("T4_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers2-t4.yaml")
BPM = 132
SWING = float(os.environ.get("T4_SWING", "0.62"))  # where a swung off-beat eighth lands (0.667 = triplet: tried, rhythm flat, recurrence lost)
# Round 2 (songwriting, v2): C = MIRROR CANON (head 2: the tom choir sings the line inverted, in contrary motion);
# H = TOM CHORALE (a new section after the piano solo: the harmonic palindrome as tom-choir chords over sweeps);
# Q = SEVEN DOORS answered (t1 Doors at Seven's head cell, quoted by Cierre too: the trumpet opens the trades with
# it in D, the tom choir answers with its retrograde); D = dotted-eighth ride hemiola across the peak (chirper-one).
R2 = set(filter(None, os.environ.get("T4_R2", "C,H,Q,D").split(","))) - {"none"}
# Round 3 (v3): N = t2 Turnstile Hours' NIGHT CELL on the fretless through the bridge (chirper-one's 13-step cycle
# cut across the palindrome's meters: a counter-line); V = the tom chorale's voicings turn over on the way back (the
# top voice drops an octave in the mirror bars); X = in the trades the toms answer a sixteenth late (an echo).
R3 = set(filter(None, os.environ.get("T4_R3", "N,V,X").split(","))) - {"none"}
NIGHT = [1, None, 5, 1, 7, None, 4, 5, 1, None, 3, 5, 7]
# Round 4 (v4): F = a DRUM FEATURE after the trades, a palindrome in itself: brushes alone for the first three bars,
# the centre bar split between brushes and tom choir, then the tom choir sings the brushes' rhythms backwards
# (bar 6-k is bar k's retrograde, on the sixteenth grid); C = the coda quotes t8 Mallet Chamber in Phase's CELL on
# piano, running unbroken across the meters (12 eighths against 44), so it phases against the palindrome.
R4 = set(filter(None, os.environ.get("T4_R4", "F,C").split(","))) - {"none"}
SOLO = {0: [0, 3, 6, 8, 9, 11], 1: [0, 2, 3, 6, 8], 2: [0, 3, 4, 7, 10, 12, 13], 3: [0, 3, 5, 7, 8, 10, 12, 15]}
PENT = ["D3", "F3", "G3", "A3", "C4", "D4", "F4"]
T8_CELL = [0, 4, 8, 4, 2, 4, 5, 4, 1, 4, 2, 6]  # t8's cell, scale degrees
# Round 5 (v5): G = the palindrome GROWS FROM ITS CENTRE before the intro: the centre bar alone (4/4), then the
# middle three (7/8 4/4 7/8), then the middle five (5/8 7/8 4/4 7/8 5/8), each playing the head at its place in the
# full mirror (melody, harmony and colour), softly over a D pedal; then the intro's full seven.
R5 = set(filter(None, os.environ.get("T4_R5", "G").split(","))) - {"none"}
# Round 6 (v6): S = the form SHRINKS BACK after the coda (the middle five, the middle three, the centre alone): the
# growth is a palindrome too, and the song ends on its axis; R = rhodes pads under the seed and the shrink.
R6 = set(filter(None, os.environ.get("T4_R6", "S,R").split(","))) - {"none"}
# Round 7 (v7): B = a FRETLESS SOLO after the piano solo, over the bridge's mirrored meters: the night cell (t2,
# chirper-one) breaks free, cycling on and climbing an octave every other cycle, the centre bar one long held note
# two octaves up (the axis); D = a soft ride under the shrink.
R7 = set(filter(None, os.environ.get("T4_R7", "B,D").split(","))) - {"none"}
# Round 8 (v8): K = tom-choir BACKGROUNDS under the piano solo's second phrase (rolled guide-tone dyads, swelling
# through each chord, the voices swapping in the mirror bars, like horn backgrounds); W = head 2's trumpet bars on
# a FRENCH HORN: the return in a warmer colour.
R8 = set(filter(None, os.environ.get("T4_R8", "K,W").split(","))) - {"none"}
# Round 9 (v9): P = the French horn doubles the trumpet an octave down at the PEAK (a brass climax, and the horn
# heard before it takes head 2); Q = in the fretless solo's odd bars (5/8, 7/8) the night cell falls in DOTTED
# EIGHTHS, across the bar instead of on it.
R9 = set(filter(None, os.environ.get("T4_R9", "P,Q").split(","))) - {"none"}
# Round 10 (v10): T = THE BRIDGE THEME (the bridge had no tune): a new palindrome over the bridge's mirrored meters,
# (offset, eighths, scale degree) per bar, bars 4-6 the retrograde of 2-0 and the centre bar a palindrome itself.
# The trumpet sings it the first time; the second time the roles reverse: the tom choir sings it and the trumpet
# holds the chord's ninth above, softly.
R10 = set(filter(None, os.environ.get("T4_R10", "T").split(","))) - {"none"}
# Round 11 (v11): K = a CANON in head 1: the rhodes follows the melody two beats behind, an octave down, so the line
# spills across the changing meters and every bar hears the previous bar's tune against its own.
R11 = set(filter(None, os.environ.get("T4_R11", "K").split(","))) - {"none"}
# Round 12 (v12): C = the trades' last phrase turns COLLECTIVE: trumpet and tom choir play together in every bar
# (the tom an answer a third below, still a sixteenth late), a climax before the drum feature; S = the SEED is sung
# by the tom choir alone (the drums plant the palindrome), over the rhodes.
R12 = set(filter(None, os.environ.get("T4_R12", "C,S").split(","))) - {"none"}
# Round 13 (v13): U = head 2 goes UP A WHOLE STEP (every pitched part: the palindrome returns in E, the coda falls
# back home to D); K = the drummer picks up STICKS for the collective trades (the peak's stick snare, ride hemiola
# and centre crash arrive a section early).
R13 = set(filter(None, os.environ.get("T4_R13", "U").split(","))) - {"none"}  # K tried: brighter, -0.1
# Round 14 (v14): L = a LINK bar before head 2: the trumpet alone over one brush sweep, a palindromic pivot into E
# (A B C# E. C# B A); A = in the coda the tom choir answers the piano's t8 cell in CANON, a beat behind, an octave
# down.
R14 = set(filter(None, os.environ.get("T4_R14", "L,A").split(","))) - {"none"}
# Round 15 (v15): B = t3 Glass Arithmetic's BRAID answered (chirper-one: two loops of 5 and 7 running across the
# bar lines): in the intro, two PALINDROMIC loops braid across the palindromic meters, the piano's 7 (0 1 3 4 3 1 0 in
# eighths) and the rhodes' 5 (0 2 4 2 0 in quarters), on each moment's chord, never meeting the 44-eighth phrase.
R15 = set(filter(None, os.environ.get("T4_R15", "B").split(","))) - {"none"}
# Round 16 (v16): W = t5 The Kettle Modulates' THIRDS WALK answered (chirper-one: up a major third to a m7, down a
# minor third to a maj7, climbing a semitone every two bars): the trades' third phrase walks Bbmaj7 Dm7 Bmaj7 D#m7
# Cmaj7 Em7 C#maj7, a bar each, and the collective phrase resolves up a semitone to Dm9.
R16 = set(filter(None, os.environ.get("T4_R16", "W").split(","))) - {"none"}
WALK = [(10, "maj7"), (2, "m7"), (11, "maj7"), (3, "m7"), (0, "maj7"), (4, "m7"), (1, "maj7")]
# Round 17 (v17): A = an ARCO BASS (the bow): a bowed bass enters only in the chorale and the shrink, singing each
# chord's root long under the tom chords, and holding the D pedal as the mirror closes; M = the master's top shelf
# lowered (+2 -> +0.5 dB): the brushes' air sat 9 dB over the genre.
R17 = set(filter(None, os.environ.get("T4_R17", "A,M").split(","))) - {"none"}
# Round 18 (v18): P = TRIPLETS ACROSS THE MIRROR: in the piano solo's first phrase the right hand phrases in
# triplet quarters (three against two, floating over the bridge meters), a palindromic line (0 2 4 6 4 2) on each
# chord, and the ride bell joins the triplet pulse.
R18 = set(filter(None, os.environ.get("T4_R18", "P").split(","))) - {"none"}
# Round 19 (v19): M = t10 Cierre's MONTUNO answered (chirper-zero: x.x.xx.x | .xx.x.xx): at the peak the piano's
# left hand leaves its comping for the montuno, one 16-eighth cycle running unbroken across the meter palindrome
# (44 eighths a phrase), so the figure is displaced anew in every bar, each hit the chord of its moment.
R19 = set(filter(None, os.environ.get("T4_R19", "M").split(","))) - {"none"}
MONTUNO = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1]
# Round 20 (v20): X = t9 Slow Shutter's EXPOSURE answered (chirper-zero: one long colour tone a bar, approached by
# a leap): in the coda the French horn sings each bar's colour (the voicing's top: a 9th, 11th or 13th), leaping up
# a sixth into it, above the piano's t8 cell and the tom canon.
R20 = set(filter(None, os.environ.get("T4_R20", "X").split(","))) - {"none"}
# Round 21 (v21): S = t7 Cross Purposes' SUBJECT answered (chirper-three; in D, like this track): in the drum
# feature the tom choir sings it BACKWARDS (D F# Eb G E G# A F D) on the brushes' retrograde rhythms, the borrowed
# tune cycling through the palindromic solo.
R21 = set(filter(None, os.environ.get("T4_R21", "S").split(","))) - {"none"}
SUBJ_RETRO = [0, 4, 1, 5, 2, 6, 7, 3, 0]  # t7's subject (0 3 7 6 2 5 1 4 0) read backwards, semitones over D3
BTHEME = {0: [(0, 3, 4), (3, 1, 3), (4, 4, 2)], 1: [(0, 2, 1), (2, 2, 2), (4, 3, 4)], 2: [(0, 5, 6)],
          3: [(0, 2, 4), (2, 2, 5), (4, 2, 4)]}  # t2's night cell, degrees on eighths (None = rest)
TRIP = "T" in os.environ.get("T4_OPTS", "")  # triplet brush ghosts before the backbeats (off: no gain)
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
PC = {n: i for i, n in enumerate(NAMES)}
PC.update({"Db": 1, "D#": 3, "Gb": 6, "G#": 8, "A#": 10})


def midi(n):
    """'D4' -> 62."""
    name, octv = (n[:-1], int(n[-1])) if n[-2] not in "-" else (n[:-2], int(n[-2:]))
    return 12 * (octv + 1) + PC[name]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


# ---------------- the palindrome ----------------
METERS = [6, 5, 7, 8, 7, 5, 6]          # eighths per bar
BRIDGE = [8, 7, 5, 6, 5, 7, 8]          # read from the centre out
SWUNG = {6: True, 8: True, 5: False, 7: False}
GROUP = {5: (3, 2), 7: (2, 2, 3), 6: (2, 2, 2), 8: (2, 2, 2, 2)}

# chords: (root midi in octave 2-3, voicing intervals above the root for the piano, scale for lines)
CH = {
    "Dm9": (50, [3, 7, 10, 14], [0, 2, 3, 5, 7, 9, 10]),
    "Bbmaj7#11": (46, [4, 7, 11, 18], [0, 2, 4, 6, 7, 9, 11]),
    "G13sus": (43, [5, 10, 14, 21], [0, 2, 5, 7, 9, 10]),
    "Fmaj7/G": (43, [10, 14, 17, 21], [0, 2, 4, 5, 7, 9, 10]),
    "Ebmaj9": (51, [4, 7, 11, 14], [0, 2, 4, 7, 9, 11]),
    "Abmaj7#11": (44, [4, 7, 11, 18], [0, 2, 4, 6, 7, 9, 11]),
    "Emaj9": (52, [4, 7, 11, 14], [0, 2, 4, 7, 9, 11]),
    "Amaj7": (45, [4, 7, 11, 16], [0, 2, 4, 7, 9, 11]),
    "Fm9": (53, [3, 7, 10, 14], [0, 2, 3, 5, 7, 8, 10]),
    "Dbmaj7#11": (49, [4, 7, 11, 18], [0, 2, 4, 6, 7, 9, 11]),
    "Cm11": (48, [3, 10, 14, 17], [0, 2, 3, 5, 7, 9, 10]),
    "F13": (41, [4, 10, 14, 21], [0, 2, 4, 7, 9, 10]),
    "Dm(maj9)": (50, [3, 7, 11, 14], [0, 2, 3, 5, 7, 9, 11]),
}
# the centre bar's door, phrase by phrase
CENTRES = [("Ebmaj9", "Abmaj7#11"), ("Emaj9", "Amaj7"), ("Fm9", "Dbmaj7#11"), ("Cm11", "F13")]
for _pc, _k in WALK:
    CH[f"walk{_pc}{_k}"] = (41 + (_pc - 5) % 12, [4, 7, 11, 14] if _k == "maj7" else [3, 7, 10, 14],
                            [0, 2, 4, 6, 7, 9, 11] if _k == "maj7" else [0, 2, 3, 5, 7, 9, 10])


def low(root):
    """A chord root in the bass's register, E1..D#2 (an upright's bottom octave)."""
    r = root % 12
    return 28 + (r - 4) % 12


def bar_chords(meter, centre, mirror_pos):
    """The chords of a bar (a list of (start eighth, chord name)) at palindrome position 0..6."""
    side = ["Dm9", "Bbmaj7#11", "G13sus", None, "G13sus", "Bbmaj7#11", "Dm9"][mirror_pos]
    if side is None:
        return [(0, centre[0]), (4, centre[1])]
    if meter == 7:  # 4 + 3: the sus resolves sideways
        return [(0, side), (4, "Fmaj7/G")] if side == "G13sus" else [(0, side), (4, side)]
    return [(0, side)]


# ---------------- the head melody: bar k is the retrograde of bar 6-k ----------------
# (eighth offset, length in eighths, note); bars 0..3 are written, 4..6 are their mirrors.
HEAD = [
    [(0, 2, "A4"), (2, 1, "G4"), (3, 1, "F4"), (4, 2, "E4")],                     # 3/4  Dm9
    [(0, 1, "D5"), (1, 1, "E5"), (2, 3, "F5")],                                    # 5/8  Bbmaj7#11
    [(0, 1, "C5"), (1, 1, "D5"), (2, 1, "E5"), (3, 2, "A4"), (5, 2, "G4")],        # 7/8  G13sus | Fmaj7/G
    None,                                                                          # 4/4  the centre (per chord)
]


def centre_line(centre):
    """The centre bar's own palindrome on its two chords: up the first chord, mirrored down the second."""
    r0, v0, _ = CH[centre[0]]
    a = [r0 + 24 + v0[1], r0 + 24 + v0[2], r0 + 24 + v0[3]]
    return [(0, 1, nm(a[0])), (1, 1, nm(a[1])), (2, 2, nm(a[2])), (4, 2, nm(a[2])), (6, 1, nm(a[1])), (7, 1, nm(a[0]))]


def retro(line, meter):
    return sorted((meter - (o + ln), ln, n) for o, ln, n in line)


def head_bar(pos, meter, centre):
    if pos == 3:
        return centre_line(centre)
    if pos < 3:
        return HEAD[pos]
    return retro(HEAD[6 - pos], meter)


VOICE = ["tpt", "pno", "tom", "tpt", "tom", "pno", "tpt"]  # the colour palindrome


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, mark=""):
        self.ev.append((round(at, 4), max(0.05, round(ln, 4)), head, int(max(1, min(127, vel))), mark))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue  # one event per onset (chords are written as one head)
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, mark) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}" + (f"^{mark}" if mark else ""))
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


def swing_at(bar_start, e8, swung):
    """Beat position of eighth e8 within a bar starting at bar_start (beats)."""
    b = bar_start + e8 / 2
    if swung and e8 % 2 == 1:
        b = bar_start + (e8 - 1) / 2 + SWING
    return b


def build():
    T = {k: Track(k) for k in ("tpt", "pno", "tom", "bass", "drums", "rhodes", "pno_lh", "horn", "arco")}
    bars = []   # (start beat, meter, pos, section, phrase index, centre)
    sec = []

    def add_phrase(section, meters, centre, pidx, off=0):
        start = bars[-1][0] + bars[-1][1] / 2 if bars else 0.0
        for pos, m in enumerate(meters):
            bars.append((start, m, pos + off, section, pidx, centre))
            start += m / 2

    if "G" in R5:  # the seed: 1, 3, 5 bars of the mirror (the centre rotation is not advanced)
        for L in (1, 3, 5):
            off = (7 - L) // 2
            add_phrase("seed", METERS[off:off + L], CENTRES[0], -1, off)
        sec.append(("seed", 0.0, len(bars)))

    form = [("intro", METERS, 2), ("head", METERS, 2), ("bridge", BRIDGE, 2), ("trade", METERS, 4)] + ([("drums", METERS, 1)] if "F" in R4 else []) + [
            ("piano", BRIDGE, 2)] + ([("bsolo", BRIDGE, 1)] if "B" in R7 else []) + ([("chorale", METERS, 1)] if "H" in R2 else []) + [("peak", METERS, 2)] + ([("link", None, 1)] if "L" in R14 else []) + [("head2", METERS, 2), ("coda", METERS, 1 if "S" in R6 else 2)]  # the form mirrors too
    p = 0
    for name, meters, n in form + ([("unseed", None, 3)] if "S" in R6 else []):
        if meters is None and name == "link":  # the link: one 4/4 bar at the centre's place
            first = len(bars)
            add_phrase(name, [8], CENTRES[0], -3, 3)
            sec.append((name, bars[first][0], 1))
            continue
        if meters is None:  # the shrink: 5, 3, 1 bars of the mirror, the coda's centre held
            first = len(bars)
            for L in (5, 3, 1):
                off = (7 - L) // 2
                add_phrase(name, METERS[off:off + L], CENTRES[0], -2, off)
            sec.append((name, bars[first][0], len(bars) - first))
            continue
        first = len(bars)
        for k in range(n):
            add_phrase(name, meters, CENTRES[p % len(CENTRES)], p)
            p += 1
        sec.append((name, bars[first][0], len(bars) - first))
    total = bars[-1][0] + bars[-1][1] / 2 + 4.0  # a ring-out

    # dynamics: each phrase swells to its centre bar; sections set the level
    LEVEL = {"link": 64, "bsolo": 76, "seed": 44, "unseed": 44, "intro": 50, "head": 68, "bridge": 74, "trade": 84, "piano": 70, "peak": 104, "head2": 64, "coda": 48,
             "chorale": 62, "drums": 84}
    # the bass's role per section: a two-feel under the heads, a pedal under the bridge, walking under the solos
    BASS = {"link": "none", "bsolo": "solo", "seed": "pedal", "unseed": "pedal", "intro": "two", "head": "two", "bridge": "pedal", "trade": "walk", "piano": "walk", "peak": "walk",
            "head2": "two", "coda": "two", "chorale": "pedal", "drums": "tacet"}

    def dyn(i):
        start, m, pos, section, pidx, centre = bars[i]
        return LEVEL[section] + 10 - 3 * abs(pos - 3)

    tom_k = [0]  # the drum feature's tom-note counter
    for i, (start, m, pos, section, pidx, centre) in enumerate(bars):
        swung = SWUNG[m]
        v = dyn(i)
        chords = bar_chords(m, centre, pos) if m in (5, 6, 7, 8) else [(0, "Dm9")]
        if section == "trade" and "W" in R16 and pidx == sorted({b[4] for b in bars if b[3] == "trade"})[2]:
            pc, kd = WALK[pos]
            chords = [(0, f"walk{pc}{kd}")]
        if section == "bridge":  # the bridge's meters are read from the centre: harmony follows its own mirror
            chords = bar_chords(m, centre, [3, 2, 1, 0, 1, 2, 3][pos] if pos != 3 else 0)
            if pos == 0 or pos == 6:
                chords = [(0, centre[0]), (4, centre[1])]
        name0 = chords[0][1]

        # ---- bass (fretless): its role changes by section; walking quarters in swung bars, grouped in odd ones ----
        role = BASS[section]
        if section == "bridge" and "N" in R3:
            role = "night"
            first = min(b[0] for b in bars if b[3] == "bridge")
            e0 = int(round((start - first) * 2))  # eighths since the bridge began: the 13-cycle runs on through bars
            for e in range(m):
                d = NIGHT[(e0 + e) % 13]
                if d is None:
                    continue
                cn = name0
                for c8, cnn in chords:
                    if c8 <= e:
                        cn = cnn
                root, voic, scale = CH[cn]
                note = low(root) + scale[(d - 1) % len(scale)]
                T["bass"].add(swing_at(start, e, swung), 0.45, nm(note), v - 6 + (8 if (e0 + e) % 13 == 0 else 0))
        if role == "solo":  # the fretless solo: the night cell set free
            first = min(b[0] for b in bars if b[3] == "bsolo")
            e0 = int(round((start - first) * 2))
            root, voic, scale = CH[name0]
            if pos == 3:
                T["bass"].add(start, m / 2 * 0.95, nm(low(root) + 24), v + 4)
            elif m in (5, 7) and "Q" in R9:  # dotted eighths across the odd bar
                k = e0
                for q in range(int((m / 2) // 0.75) + (1 if (m / 2) % 0.75 > 0.3 else 0)):
                    while NIGHT[k % 13] is None:
                        k += 1
                    d = NIGHT[k % 13]
                    r2, _, sc2 = CH[name0]
                    note = low(r2) + 12 + sc2[(d - 1) % len(sc2)] + (12 if (k // 13) % 2 else 0)
                    T["bass"].add(start + q * 0.75, 0.7, nm(note), v + (6 if q == 0 else 0))
                    k += 1
            else:
                for e in range(m):
                    k = e0 + e
                    d = NIGHT[k % 13]
                    if d is None:
                        continue
                    cn = name0
                    for c8, cnn in chords:
                        if c8 <= e:
                            cn = cnn
                    r2, _, sc2 = CH[cn]
                    note = low(r2) + 12 + sc2[(d - 1) % len(sc2)] + (12 if (k // 13) % 2 else 0)
                    at = swing_at(start, e, swung)
                    if k % 13 == 0 and k:  # a sixteenth grace from a semitone below into each new cycle
                        T["bass"].add(at - 0.25, 0.22, nm(note - 1), v - 6)
                    T["bass"].add(at, 0.45, nm(note), v + (8 if k % 13 == 0 else 0))
        elif role == "night":
            pass
        elif role == "tacet":
            if pos == 3:
                T["bass"].add(start, 1.0, "D2", v - 4)
        elif role == "pedal":
            T["bass"].add(start, m / 2 * 0.95, "D2", v - 6)
        elif role == "two":
            for ci, (c8, cn) in enumerate(chords):
                T["bass"].add(start + c8 / 2, ((chords[ci + 1][0] if ci + 1 < len(chords) else m) - c8) / 2 * 0.9,
                              nm(low(CH[cn][0])), v - 4)
        for ci, (c8, cn) in enumerate(chords if role == "walk" else []):
            root, voic, scale = CH[cn]
            end8 = chords[ci + 1][0] if ci + 1 < len(chords) else m
            if swung:
                for q8 in range(c8, end8, 2):
                    k = (q8 - c8) // 2
                    step = [0, scale[2] if len(scale) > 2 else 4, 7, 10 if 10 in scale else 9][k % 4]
                    note = low(root) + step
                    if q8 + 2 >= end8 and ci + 1 < len(chords):  # chromatic approach into the next chord
                        note = low(CH[chords[ci + 1][1]][0]) - 1
                    T["bass"].add(start + q8 / 2, 0.95, nm(note), v - 6)
            else:
                g8 = c8
                for gi, g in enumerate(GROUP[m]):
                    if g8 >= end8:
                        break
                    note = low(root) + (0 if gi == 0 else 7 if gi == 1 else 12)
                    T["bass"].add(start + g8 / 2, g / 2 * 0.9, nm(note), v - 4 + (4 if gi == 0 else 0))
                    g8 += g

        # ---- the melody (head sections), with the colour palindrome ----
        if section in ("head", "head2", "peak", "seed", "unseed"):
            line = head_bar(pos, m, centre)
            if section == "head2" and pos == 3:   # the return: the centre bar a fifth lower, half time
                line = [(o, ln, nm(midi(n) - 7)) for o, ln, n in line]
            if section == "unseed" or (section == "seed" and "S" in R12):  # the tom choir sings it all
                voice = "tom"
            else:
                voice = VOICE[pos] if section != "peak" else ("tpt" if pos % 2 == 0 else "tom")
                if section == "head2" and voice == "tpt" and "W" in R8:
                    voice = "horn"
            for o, ln, n in line:
                at = swing_at(start, o, swung)
                T[voice].add(at, ln / 2 * 0.95, n if voice != "tom" else nm(midi(n) - 12), v + 4)
                if section == "head" and "K" in R11:  # the canon, two beats behind on the rhodes
                    T["rhodes"].add(at + 2.0, ln / 2 * 0.9, nm(midi(n) - 12), v - 2)
                if section == "peak" and voice == "tpt":  # unison in the piano an octave down at the peak
                    T["pno"].add(at, ln / 2 * 0.9, nm(midi(n) - 12), v)
                    if "P" in R9 and "W" in R8:  # and the horn, an octave down: brass
                        T["horn"].add(at, ln / 2 * 0.95, nm(midi(n) - 12), v - 4)
                if section == "head2" and "C" in R2 and voice != "tom":  # the mirror canon: inverted about D5,
                    T["tom"].add(at, ln / 2 * 0.95, nm(2 * 74 - midi(n) - 12), v)  # an octave down, contrary motion
        # ---- trading: trumpet takes the 3/4 and 7/8 bars, the tom choir the 5/8 and 4/4 ----
        first_trade = section == "trade" and pidx == min(b[4] for b in bars if b[3] == "trade")
        if first_trade and "Q" in R2 and pos in (0, 1):
            # SEVEN DOORS (t1), its opening cell in D: D5. C5 A4 G4 F4 on the trumpet; the toms answer backwards
            cell = [(0, 3, "D5"), (3, 1, "C5"), (4, 1, "A4"), (5, 1, "G4")] if pos == 0 else \
                   [(0, 1, "G3"), (1, 1, "A3"), (2, 1, "C4"), (3, 2, "D4")]
            for o, ln, n in cell:
                T["tpt" if pos == 0 else "tom"].add(swing_at(start, o, swung), ln / 2 * 0.95, n, v + 6)
        elif section == "trade":
            collective = "C" in R12 and pidx == max(b[4] for b in bars if b[3] == "trade")
            voices = ["tpt", "tom"] if collective else ["tpt" if m in (6, 7) else "tom"]
            root, voic, scale = CH[name0]
            # a line built from the head's own cells, transposed onto this chord and varied per phrase
            cell = HEAD[[0, 1, 2, 2][min(pos, 3)]] if pos != 3 else centre_line(centre)
            shift = [0, 2, -3, 5][pidx % 4]
            for voice in voices:
                for j, (o, ln, n) in enumerate(cell):
                    if o >= m:
                        continue
                    deg = scale[(j * 2 + pidx + (2 if collective and voice == "tom" else 0)) % len(scale)]
                    note = root + 24 + deg + shift if voice == "tpt" else root + 12 + deg
                    at = swing_at(start, o, swung) + (0.25 if voice == "tom" and "X" in R3 else 0)
                    T[voice].add(at, min(ln, m - o) / 2 * 0.9, nm(note), v + (6 if j == 0 else 0) - (4 if collective and voice == "tom" else 0))
        if section == "bridge" and "T" in R10:  # the bridge theme
            src = BTHEME[min(pos, 6 - pos)]
            line = src if pos <= 3 else [(m - o - ln, ln, dg) for o, ln, dg in reversed(src)]
            second = pidx == max(b[4] for b in bars if b[3] == "bridge")
            for o, ln, dg in line:
                cn = name0
                for c8, cnn in chords:
                    if c8 <= o:
                        cn = cnn
                r0, _, sc = CH[cn]
                note = r0 + 24 + sc[dg % len(sc)] + 12 * (dg // len(sc))
                while note > 79:
                    note -= 12
                at = swing_at(start, o, swung)
                if second:
                    T["tom"].add(at, ln / 2 * 0.95, nm(note - 12), v + 2)
                else:
                    T["tpt"].add(at, ln / 2 * 0.95, nm(note), v)
            if second:  # the trumpet holds the ninth above, softly
                r0, _, sc = CH[name0]
                n9 = r0 + 24 + sc[1] + 12
                while n9 > 81:
                    n9 -= 12
                T["tpt"].add(start, m / 2 * 0.9, nm(n9), v - 16)
        if section == "intro" and "B" in R15:  # the braid
            first = min(b[0] for b in bars if b[3] == "intro")
            e0 = int(round((start - first) * 2))
            for e in range(m):
                cn = name0
                for c8, cnn in chords:
                    if c8 <= e:
                        cn = cnn
                r0, _, sc = CH[cn]
                k = e0 + e
                d7 = [0, 1, 3, 4, 3, 1, 0][k % 7]
                n7 = r0 + 24 + sc[d7 % len(sc)]
                while n7 > 76:
                    n7 -= 12
                T["pno"].add(swing_at(start, e, swung), 0.45, nm(n7), v - 4 + (6 if k % 7 == 0 else 0))
                if k % 2 == 0:
                    d5 = [0, 2, 4, 2, 0][(k // 2) % 5]
                    n5 = r0 + 12 + sc[d5 % len(sc)]
                    while n5 > 64:
                        n5 -= 12
                    T["rhodes"].add(swing_at(start, e, swung), 0.9, nm(n5), v - 2 + (6 if (k // 2) % 5 == 0 else 0))
        # ---- piano: comping (rootless voicings), or the melody when VOICE says so ----
        comp = []
        for c8, cn in chords:
            root, voic, scale = CH[cn]
            vo = ",".join(nm(root + 12 + x) for x in voic) if root < 48 else ",".join(nm(root + x) for x in voic)
            comp.append((c8, vo))
        if "A" in R17 and section == "chorale":  # the bow (in the shrink too, it made the two alike: variety -6)
            for ci, (c8, cn) in enumerate(chords):
                r0 = CH[cn][0]
                end8 = chords[ci + 1][0] if ci + 1 < len(chords) else m
                T["arco"].add(start + c8 / 2, (end8 - c8) / 2 * 0.97,
                              nm(low(r0) if section == "chorale" else 38), v - 2)
        if section == "chorale":  # the tom choir as a chorale: the bar's chords, three toms each
            for ci, (c8, cn) in enumerate(chords):
                root, voic, scale = CH[cn]
                end8 = chords[ci + 1][0] if ci + 1 < len(chords) else m
                top = root + 24 if root < 48 else root + 12
                ch3 = (top - 12 + voic[0], top + voic[1] - 12, top + voic[3] - 12)
                if pos > 3 and "V" in R3:  # the mirror bars: the voicing turns over (top voice under the others)
                    ch3 = (ch3[2] - 12, ch3[0], ch3[1])
                T["tom"].add(start + c8 / 2, (end8 - c8) / 2 * 0.95, ",".join(nm(x) for x in ch3), v + 8)
        elif section == "piano":  # piano solo: right hand lines over left-hand shells
            for c8, vo in comp:
                T["pno_lh"].add(start + c8 / 2, 1.0, vo, v - 10)
            if "K" in R8 and pidx == max(b[4] for b in bars if b[3] == "piano"):  # tom-choir backgrounds
                for ci, (c8, cn) in enumerate(chords):
                    r0, vc, _ = CH[cn]
                    end8 = chords[ci + 1][0] if ci + 1 < len(chords) else m
                    base = r0 + 12 if r0 < 48 else r0
                    while base > 50:
                        base -= 12
                    lo, hi = base + 12 + vc[0], base + 12 + vc[1]
                    dy = (lo, hi) if pos <= 3 else (hi - 12, lo)
                    for e in range(c8, end8):
                        T["tom"].add(swing_at(start, e, swung), 0.45, f"{nm(dy[0])},{nm(dy[1])}",
                                     v - 22 + 4 * (e - c8))
            root, voic, scale = CH[name0]
            trip = "P" in R18 and pidx == min(b[4] for b in bars if b[3] == "piano")
            if trip:  # triplet quarters across the bar
                first = min(b[0] for b in bars if b[3] == "piano")
                j = int(-(-(start - first) // (2 / 3)))
                while first + j * 2 / 3 < start + m / 2 - 1e-6:
                    at = first + j * 2 / 3
                    e = int((at - start) * 2)
                    cn = name0
                    for c8, cnn in chords:
                        if c8 <= e:
                            cn = cnn
                    r0, _, sc = CH[cn]
                    dg = [0, 2, 4, 6, 4, 2][j % 6]
                    note = r0 + 24 + sc[dg % len(sc)] + (12 if dg >= len(sc) else 0)
                    while note > 84:
                        note -= 12
                    T["pno"].add(at, 0.6, nm(note), v - 2 + (8 if j % 3 == 0 else 0))
                    T["drums"].add(at, 0.3, "rb", v - 18 + (6 if j % 3 == 0 else 0))
                    j += 1
            for e8 in range(m if not trip else 0):
                if (e8 + pidx) % 3 == 2:
                    continue  # breath: a rest every third eighth
                deg = scale[(e8 * 3 + pos + pidx) % len(scale)]
                note = root + 24 + deg + (12 if (e8 + pos) % 5 == 0 else 0)
                T["pno"].add(swing_at(start, e8, swung), 0.45, nm(note), v - 2 + (8 if e8 == 0 else 0))
        else:
            pattern = {6: [(1, 1), (4, 2)], 8: [(1, 1), (3, 1), (6, 2)], 5: [(0, 3)], 7: [(0, 2), (4, 3)]}[m]
            if pidx % 2:  # every other phrase: anticipations instead
                pattern = {6: [(0, 2), (5, 1)], 8: [(0, 2), (4, 1), (7, 1)], 5: [(3, 2)], 7: [(2, 2), (6, 1)]}[m]
            if section == "peak" and "M" in R19:  # the montuno
                first = min(b[0] for b in bars if b[3] == "peak")
                e0 = int(round((start - first) * 2))
                for e in range(m):
                    if MONTUNO[(e0 + e) % 16]:
                        cn_vo = [vo for c8, vo in comp if c8 <= e][-1]
                        T["pno_lh"].add(swing_at(start, e, swung), 0.4, cn_vo,
                                        v - 12 + (6 if (e0 + e) % 8 == 0 else 0))
            elif section in ("chorale", "drums", "link") or (section == "unseed" and "R" in R6):
                pass  # (the shrink: the rhodes alone carries the chords)
            elif not (section in ("head", "head2") and VOICE[pos] == "pno"):
                for o, ln in pattern:
                    cn_vo = [vo for c8, vo in comp if c8 <= o][-1]
                    T["pno_lh"].add(swing_at(start, o, swung), ln / 2 * 0.9, cn_vo, v - 16)
            else:
                T["pno_lh"].add(start, m / 2 * 0.9, comp[0][1], v - 16)
        # ---- rhodes through a Bassman stack: pads in the bridge, chords in the peak ----
        if section in ("bridge", "peak") or (section in ("seed", "unseed") and "R" in R6):
            for c8, vo in comp:
                T["rhodes"].add(start + c8 / 2, (m - c8) / 2 * 0.95, vo, v - (8 if section in ("bridge", "peak") else 4))

        # ---- drums: brushes (sticks at the peak) ----
        d = T["drums"]
        peak = section == "peak" or ("K" in R13 and "C" in R12 and section == "trade"
                                      and pidx == max(b[4] for b in bars if b[3] == "trade"))
        if section == "link":
            d.add(start, m / 2 * 0.95, "bsl", v - 16)
            for o, ln, n in [(0, 1, "A4"), (1, 1, "B4"), (2, 1, "C#5"), (3, 2, "E5"), (5, 1, "C#5"), (6, 1, "B4"),
                             (7, 1, "A4")]:
                T["tpt"].add(swing_at(start, o, swung), ln / 2 * 0.95, n, v + 2 + (6 if o == 3 else 0))
            continue
        if section == "chorale" or section == "unseed":
            d.add(start, m / 2 * 0.95, "bsl", v - 14)
            if section == "unseed" and "D" in R7:
                for bt in range(m // 2):
                    d.add(start + bt, 0.5, "rd", v - 20)
            continue
        if section == "drums":  # the drum feature: brushes, the split centre, the tom choir's retrograde
            L16 = m * 2
            src = SOLO[min(pos, 6 - pos)]
            hits = src if pos <= 3 else sorted(L16 - 1 - s for s in src)
            for j, s in enumerate(hits):
                at = start + s / 4
                acc = 10 if j == 0 or s % 4 == 0 else 0
                if pos < 3 or (pos == 3 and s < 8):
                    d.add(at, 0.25, "k" if j == 0 else ("st" if acc else "bt"), v - 8 + acc)
                    if j == 0:
                        d.add(at, m / 2 * 0.9, "bs", v - 20)
                else:
                    k = j if pos == 3 else len(hits) - 1 - j
                    if "S" in R21:
                        tom_k[0] += 1
                        T["tom"].add(at, 0.24, nm(50 + SUBJ_RETRO[(tom_k[0] - 1) % 9]), v - 2 + acc)
                    else:
                        T["tom"].add(at, 0.24, PENT[(k + pos) % len(PENT)], v - 2 + acc)
            d.add(start, 0.5, "hf", v - 18)
            continue
        if peak and "D" in R2:  # dotted eighths on the ride across the peak's bars, against every meter
            first = min(b[0] for b in bars if b[3] == "peak")
            k = int(-(-(start - first) // 0.75))
            while first + k * 0.75 < start + m / 2 - 1e-6:
                d.add(first + k * 0.75, 0.3, "rb", v - 10 + (8 if k % 4 == 0 else 0))
                k += 1
        if swung:
            beats = m // 2
            if not peak:
                d.add(start, beats * 0.95, "bsl" if section in ("intro", "coda") else "bs", v - 18)  # the sweep
            for bt in range(beats):
                if bt % 2 == 1 or (beats == 3 and bt == 2):
                    d.add(start + bt, 0.5, "st" if peak else "bt", v - 4)
                    d.add(start + bt, 0.5, "hf", v - 20)
                    if TRIP and bt >= 1 and not peak:  # the brush's triplet: two ghosts leading into the backbeat
                        d.add(start + bt - 2 / 3, 0.3, "bt", v - 24)
                        d.add(start + bt - 1 / 3, 0.3, "bt", v - 18)
                d.add(start + bt, 0.5, "rd", v - 14)                          # ride on the beat
                if bt % 2 == 1:
                    d.add(start + bt + SWING, 0.3, "rd", v - 22)               # and the skip
            d.add(start, 0.5, "k", v - 26 if not peak else v - 6)            # feathered
        else:
            g8 = 0
            for gi, g in enumerate(GROUP[m]):
                d.add(start + g8 / 2, g / 2 * 0.9, ("st" if peak else "bt") if gi else "k", v - (6 if gi else 18))
                if not peak and gi == 0:
                    d.add(start + g8 / 2, m / 2 * 0.9, "bs", v - 20)
                d.add(start + g8 / 2, 0.4, "rd", v - 16)
                g8 += g
        if peak and pos == 3:
            d.add(start, 0.5, "c", 110)
        if section == "coda" and pos == 6:
            d.add(start + 2, 2.0, "bsl", 60)
        if section == "coda" and "X" in R20 and "W" in R8:  # exposure: one colour a bar, leapt into
            r0, vc, _ = CH[name0]
            col = r0 + 12 + vc[-1]
            while col > 72:
                col -= 12
            while col < 60:
                col += 12
            T["horn"].add(start, 0.45, nm(col - 9), v - 6)
            T["horn"].add(start + 0.5, (m - 1) / 2 * 0.95, nm(col), v + 2)
        if section == "coda" and "C" in R4 and pidx == min(b[4] for b in bars if b[3] == "coda"):
            first = min(b[0] for b in bars if b[3] == "coda")
            e0 = int(round((start - first) * 2))
            for e in range(m):
                dg = T8_CELL[(e0 + e) % 12]
                T["pno"].add(start + e / 2, 0.45, nm(62 + 12 * (dg // 7) + [0, 2, 3, 5, 7, 9, 10][dg % 7]),
                             v - 6 + (8 if (e0 + e) % 12 == 0 else 0))
                if "A" in R14:  # the tom choir's canon, a beat behind, an octave down
                    T["tom"].add(start + e / 2 + 1.0, 0.45, nm(50 + 12 * (dg // 7) + [0, 2, 3, 5, 7, 9, 10][dg % 7]),
                                 v - 10 + (6 if (e0 + e) % 12 == 0 else 0))

    # coda: the tom choir sings the head's opening cell backwards alone, the piano's last chord rings
    last = bars[-1][0] + bars[-1][1] / 2
    for k, (o, ln, n) in enumerate(reversed(HEAD[0])):
        T["tom"].add(last + o / 2, ln / 2, nm(midi(n) - 12), 70 - 3 * k)
    T["pno_lh"].add(last + 2.0, 2.0, "D3,A3,C4,E4,F4,G4", 62)
    T["bass"].add(last + 2.0, 2.0, "D2", 60)
    if "U" in R13:  # head 2 up a whole step: transpose every pitched event inside it
        h2 = [b for b in bars if b[3] == "head2"]
        lo, hi = h2[0][0], h2[-1][0] + h2[-1][1] / 2
        for name, tr in T.items():
            if name == "drums":
                continue
            tr.ev = [(s, ln, ",".join(nm(midi(x) + 2) for x in head.split(",")) if lo - 1e-6 <= s < hi - 1e-6 else head,
                      vel, mark) for s, ln, head, vel, mark in tr.ev]
    return total, bars, sec, T


def kit():
    snare = dict(type="drum", beater="brush", decay="0.32s", sharp=20, reso=1.45, cavity=0.3, reso_level=0.5,
                 shell=0.3, shell_hz=480, wires=0.5, gap=0.25, wire_tone="5.5k", strike=0.35, damp=0.3, slap=0.7,
                 stereo=0.4)

    def piece(pitch, layer, amp, gain="0dB", filters=("hp cutoff=90",)):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": list(filters),
                                                                    "amp": amp}, "play": {"vel_sens": 0.7}}}
    samp = {"a": "0.5ms", "d": "700ms", "s": 0, "r": "60ms", "curve": 2}
    return {"brush-kit": {
        "about": "chirper-two's brush kit for Odd Hours t4: room-kit's hats, ride and cymbals; snare and kick on the "
                 "physical drum layer (bd-7d117e): brush taps (bt), sweeps (bs, bsl), a stick snare for the peak (st), "
                 "a feathered felt kick.",
        "extends": "room-kit",
        "kit": {
            "bt": piece("E3", snare, samp),
            "bs": piece("E3", dict(snare, sweep="0.55s"), {"a": "20ms", "d": "900ms", "s": 0, "r": "80ms", "curve": 1}, "-3dB"),
            "bsl": piece("E3", dict(snare, sweep="1.2s"), {"a": "40ms", "d": "1.6s", "s": 0, "r": "120ms", "curve": 1}, "-3dB"),
            "st": piece("E3", dict(snare, beater="stick", slap=1.0), {"a": "0.2ms", "d": "450ms", "s": 0, "r": "40ms"}),
            "k": piece("G1", dict(type="drum", beater="felt", decay="0.5s", sharp=40, reso=1.0, cavity=0.25,
                                  reso_level=0.6, air=0.4, strike=0.25, damp=0.3, slap=0.3, stereo=0.2),
                       {"a": "0.5ms", "d": "600ms", "s": 0, "r": "40ms", "curve": 2}, "6dB", ("hp cutoff=45",)),
        }}}


def main():
    total, bars, sec, T = build()
    tom = {"synth": {"layers": [{"type": "drum", "beater": "stick", "contact": 1.5, "decay": "1.1s", "sharp": 35,
                                 "reso": 1.0, "cavity": 0.25, "tune_sounding": True, "reso_level": 0.5, "air": 0.45,
                                 "strike": 0.3, "shell": 0.25, "slap": 0.5, "stereo": 0.5}],
                     "filters": ["hp cutoff=60"], "amp": {"a": "0.3ms", "d": "1.4s", "s": 0, "r": "120ms", "curve": 3}},
           "play": {"vel_sens": 0.6}}
    tracks = [
        {"name": "trumpet", "patch": "trumpet-mute", "pan": 0.2, "gain": "-1dB",
         "fx": ["reverb kind=hall decay=1.8s mix=0.18"], "score": T["tpt"].score(total)},
        *([{"name": "horn", "patch": "horn", "pan": 0.25, "gain": "-3dB", "fx": ["reverb kind=hall decay=1.8s mix=0.2"],
             "score": T["horn"].score(total)}] if "W" in R8 else []),
        {"name": "piano", "patch": "piano-recorded", "pan": -0.15, "gain": "-2dB", "score": T["pno"].score(total)},
        {"name": "piano-lh", "patch": "piano-recorded", "pan": -0.25, "gain": "-6dB", "score": T["pno_lh"].score(total)},
        {"name": "toms", "patch": tom, "pan": -0.05, "gain": "3dB",
         "fx": ["reverb kind=room decay=0.9s mix=0.15"], "score": T["tom"].score(total)},
        {"name": "bass", "patch": "fretless", "gain": "-1dB", "score": T["bass"].score(total)},
        *([{"name": "arco", "patch": "tagelharpa-bass-bowed", "pan": -0.1, "gain": "-4dB",
            "score": T["arco"].score(total)}] if "A" in R17 else []),
        {"name": "drums", "patch": "brush-kit", "gain": "0dB", "fx": ["reverb kind=room decay=0.8s mix=0.12"],
         "score": T["drums"].score(total)},
        {"name": "rhodes", "patch": "rhodes-rotary", "pan": 0.3, "gain": "-11dB",
         "fx": [{"type": "amp", "model": "clean", "stack": "bassman", "gain": 0.35, "mix": 0.6}],
         "score": T["rhodes"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Odd Hours, track 4. Original composition by chirper-two, generated by "
             "compose/chirpers2/src/chirpers2-t4.py. A chamber-jazz brush trio with a singing tom choir; everything is "
             "a palindrome: meters 3/4 5/8 7/8 4/4 7/8 5/8 3/4, the harmony, the melody (each bar the retrograde of its "
             f"mirror) and the orchestration. 132 bpm. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Odd Hours", "title": "Palindrome for Brushes and Toms",
                               "track": 4, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'ceiling: "-0.3dB"',
        'volume: "5dB"',
        "patches: " + json.dumps(kit()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=32", "peak cutoff=800 q=0.7 gain=-3dB",
                                                                   "highshelf cutoff=5000 gain=%s" % ("0.5dB" if "M" in R17 else "2dB")]},
                                        "glue threshold=-20dB ratio=1.3 attack=25ms release=250ms makeup=1dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
