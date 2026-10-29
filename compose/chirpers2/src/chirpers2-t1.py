#!/usr/bin/env python3
"""chirpers2-t1 "Doors at Seven" (Odd Hours, the opener) - generator for songs/chirpers2-t1.yaml (chirper-zero).

MODAL HARD-BOP QUINTET whose meter changes with each chorus: a swung 7/4 head (4+3) -> an even-eighth 4/4 bridge ->
the head again -> the tenor solo in 4/4 swing -> the piano trio in a 3/4 jazz waltz -> tenor and drums trading twos in
7/4 -> the head out -> a coda. ~176 bpm. Physical tenor sax with a french horn a fourth below in the heads, piano,
a song-local finger-plucked UPRIGHT walking, a swung kit.

Motifs (compose/chirpers2/motifs.md):
  SEVEN DOORS  the head: eight 7/4 bars in C dorian / Db lydian with a G7alt turnaround; bar 2 climbs to a held Eb5,
               bar 4 to the lydian G5, bar 8 runs up the G7b9 arpeggio into C.
  WHOLE-STEP STAIR the bridge: four major-ninth chords falling in whole steps (Ebmaj9 Dbmaj9 Bmaj7#11 Bb7sus), the
               unison horns sequencing one figure down the stair.
Bar by bar: comping rhythm, walking line, ride/snare chatter and voicings are drawn per bar (seeded) so no two
adjacent bars match; the meter, swing and soloist change per chorus; a break bar at each seam.
Run: python3 compose/chirpers2/src/chirpers2-t1.py  (writes songs/chirpers2-t1.yaml)
"""
import json
import os
import random

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("T1_OUT") or os.path.join(ROOT, "songs", "chirpers2-t1.yaml")
MG = float(os.environ.get("T1_MG", "13"))
BPM = 176
SWING = float(os.environ.get("T1_SWING", "0.70"))
SCALAR = os.environ.get("T1_TEMPO", "scalar") == "scalar"  # a scalar tempo (compscore's rhythm grid reads it); meters dropped
MIX = os.environ.get("T1_MIX", "2")
TRIP = os.environ.get("T1_TRIP", "1") == "1"  # every 4th bar of the tenor solo phrases in quarter-note triplets (3 over 2)
DTRIP = os.environ.get("T1_DTRIP", "1") == "1"  # the drummer's second bar in the trades in triplet eighths
SUB = os.environ.get("T1_SUB", "-8")
REHARM = os.environ.get("T1_REHARM", "1") == "1"
TAGTRIP = os.environ.get("T1_TAGTRIP", "1") == "1"
TAGHORN = os.environ.get("T1_TAGHORN", "1") == "1"
LOCKED = os.environ.get("T1_LOCKED", "1") == "1"  # the waltz's last eight bars in locked hands: the piano's line harmonised in block chords
INTROTEN = os.environ.get("T1_INTROTEN", "1") == "1"
BSOLO = os.environ.get("T1_BSOLO", "1") == "1"
BTRIP = os.environ.get("T1_BTRIP", "1") == "1"
STAIRUP = os.environ.get("T1_STAIRUP", "1") == "1"
STAIRTRIP = os.environ.get("T1_STAIRTRIP", "0") == "1"
PLANES = os.environ.get("T1_PLANES", "")
OVERTURE = os.environ.get("T1_OVERTURE", "1") == "1"  # the tenor solo quotes the album's themes (the opener as overture): t2 t7 t8 t10 t4 t9  # the upright's string in two polarisations (pin df4ae6aa): "0.3" or "0.3,1.5" (planes, beat)  # the climbing stair's second bar of each pair in quarter-note triplets (THREE OVER TWO)  # the bridge returns after the head out, inverted: the WHOLE-STEP STAIR climbs (Bb7sus Bmaj7#11 Dbmaj9 Ebmaj9)  # the bass solo phrases every 4th bar in quarter-note triplets too  # a 16-bar upright solo in 4/4 after the waltz: the bass sings, the piano lays out every other bar, the ride drops  # the intro's last two bars: the tenor foreshadows SEVEN DOORS, soft  # the tag's last bar: the horns run up G7b9 in quarter-note triplets into C (the head's last bar, augmented across the beat)  # in the tag, the drummer answers the horns' turnaround in triplet eighths (bars 2 and 4)  # the head out reharmonised (Abmaj7#11 Cm11 Bbm9 Dbmaj7#11 Cm11 Fm9 Db7#11 G7alt), the horn in thirds, and a 4-bar TAG on the turnaround  # the upright's sine under the string (dB)  # 1 = v1 balance; 2 = kit -13 dB + highshelf -5 @4k, bass +4, master shelf +6 @150, highshelf -4 @6k

# (name, beats per bar, bars, swing)
FORM = [("intro", 7, 4, SWING), ("headA", 7, 8, SWING), ("bridge", 4, 8, 0.5), ("headA2", 7, 8, SWING),
        ("tenor", 4, 32, SWING), ("waltz", 3, 32, SWING), ("trades", 7, 8, SWING), ("headout", 7, 8, SWING),
        ("coda", 7, 4, SWING)]
if REHARM:
    FORM.insert(8, ("tag", 7, 4, SWING))
if STAIRUP:
    FORM.insert([n for n, *_ in FORM].index("headout") + 1, ("stairup", 4, 8, 0.5))
if BSOLO:
    FORM.insert([n for n, *_ in FORM].index("trades"), ("bsolo", 4, 16, SWING))
METER = {7: "7/4", 4: "4/4", 3: "3/4"}

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10, "B": 11}
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def mi(n):
    p, o = n[:-1], int(n[-1])
    return 12 * (o + 1) + NOTE[p]


def tok(n, d, v=None):
    return f"{n}/{d:g}b" + (f"@{int(max(1, min(127, v)))}" if v is not None else "")


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


# chords: (root midi for the bass, scale (pcs from root), voicing midis for the piano)
CH = {
    "Cm11": (36, [0, 2, 3, 5, 7, 9, 10], [51, 55, 58, 62, 65]),       # Eb G Bb D F
    "Dbmaj7#11": (37, [0, 2, 4, 6, 7, 9, 11], [53, 55, 60, 63, 65]),  # F G C Eb F
    "G7alt": (43, [0, 1, 3, 4, 6, 8, 10], [53, 59, 63, 68]),          # F B Eb Ab
    "Ebmaj9": (39, [0, 2, 4, 5, 7, 9, 11], [50, 55, 58, 65]),         # D G Bb F
    "Dbmaj9": (37, [0, 2, 4, 5, 7, 9, 11], [48, 53, 56, 63]),         # C F Ab Eb
    "Bmaj7#11": (35, [0, 2, 4, 6, 7, 9, 11], [51, 54, 58, 65]),       # D# F# A# E#
    "Bb7sus": (34, [0, 2, 3, 5, 7, 9, 10], [51, 56, 60, 65]),         # Eb Ab C F
    "Fm9": (41, [0, 2, 3, 5, 7, 9, 10], [51, 56, 60, 67]),            # Eb Ab C G
    "Bbm9": (34, [0, 2, 3, 5, 7, 9, 10], [49, 53, 56, 60]),           # Db F Ab C
    "Ebmaj7": (39, [0, 2, 4, 5, 7, 9, 11], [50, 55, 58, 62]),         # D G Bb D
    "Abmaj7#11": (44, [0, 2, 4, 6, 7, 9, 11], [55, 60, 62, 67]),      # G C D G
    "Ebm11": (39, [0, 2, 3, 5, 7, 9, 10], [54, 58, 61, 65]),          # Gb Bb Db F
    "Db7#11": (37, [0, 2, 4, 6, 7, 9, 10], [53, 55, 59, 63]),         # F G B Eb (the tritone sub for G7)
}
HEAD_CH = ["Cm11", "Cm11", "Dbmaj7#11", "Dbmaj7#11", "Cm11", "Cm11", "G7alt", "G7alt"]
OUT_CH = ["Abmaj7#11", "Cm11", "Bbm9", "Dbmaj7#11", "Cm11", "Fm9", "Db7#11", "G7alt"]  # the head out, reharmonised
TAG_CH = ["Db7#11", "G7alt", "Db7#11", "G7alt"]
BRIDGE_CH = ["Ebmaj9", "Ebmaj9", "Dbmaj9", "Dbmaj9", "Bmaj7#11", "Bmaj7#11", "Bb7sus", "Bb7sus"]
TENOR_CH = ["Cm11"] * 8 + ["Dbmaj7#11"] * 8 + ["Cm11"] * 8 + ["Ebm11"] * 4 + ["G7alt"] * 4
WALTZ_CH = (["Fm9"] * 4 + ["Bbm9"] * 4 + ["Ebmaj7"] * 4 + ["Abmaj7#11"] * 4) * 2

HEAD = [  # SEVEN DOORS: eight bars of 7/4 (tenor; the horn a fourth below)
    [("C5", 1.5), ("Bb4", 0.5), ("G4", 1), ("F4", 1), ("Eb4", 1), ("F4", 2)],
    [("G4", 0.5), ("Bb4", 0.5), ("C5", 0.5), ("D5", 0.5), ("Eb5", 3), ("R", 2)],
    [("F5", 1), ("Eb5", 0.5), ("C5", 0.5), ("Ab4", 2), ("G4", 1), ("Ab4", 2)],
    [("Bb4", 0.5), ("C5", 0.5), ("Db5", 1), ("Eb5", 1), ("F5", 1), ("G5", 3)],
    [("Eb5", 1.5), ("D5", 0.5), ("C5", 1), ("Bb4", 1), ("G4", 3)],
    [("F4", 0.5), ("G4", 0.5), ("Bb4", 1), ("C5", 0.5), ("D5", 0.5), ("F5", 4)],
    [("Eb5", 1), ("Db5", 1), ("B4", 1), ("Ab4", 1), ("F4", 1), ("Eb4", 2)],
    [("D4", 1), ("F4", 0.5), ("Ab4", 0.5), ("B4", 1), ("D5", 1), ("C5", 3)],
]
BRIDGE = [  # WHOLE-STEP STAIR: one figure sequenced down the falling major chords (4/4, unison horns, straight)
    [("Bb4", 1), ("D5", 1), ("F5", 1.5), ("Eb5", 0.5)], [("D5", 2), ("Bb4", 1), ("G4", 1)],
    [("Ab4", 1), ("C5", 1), ("Eb5", 1.5), ("Db5", 0.5)], [("C5", 2), ("Ab4", 1), ("F4", 1)],
    [("F#4", 1), ("A#4", 1), ("C#5", 1.5), ("B4", 0.5)], [("A#4", 2), ("F4", 1), ("D#4", 1)],
    [("F4", 1), ("Ab4", 1), ("C5", 1), ("Eb5", 1)], [("D5", 1.5), ("C5", 0.5), ("Bb4", 2)],
]
NOTE.update({"A#": 10, "C#": 1, "D#": 3, "F#": 6})


# THE OVERTURE: tenor-solo bars that quote the album's other tracks, each fitted to the solo's chord (motifs.md)
OVERTURE_Q = {
    0: [("G4", .5), ("Bb4", .5), ("C5", .5), ("D5", .5), ("C5", .5), ("Bb4", .5), ("G4", .5), ("F4", .5)],  # t2 TURNSTILE THEME (chirper-one), C dorian 5 7 8 9 8 7 5 4 ...
    1: [("Eb4", .5), ("G4", 3.5)],                                                                       # ... 3 5
    4: [("C5", .5), ("Eb5", .5), ("G5", .5), ("F#5", 1), ("D5", 1), ("R", .5)],                           # t7 THE SUBJECT (chirper-three), from C
    5: [("F5", .5), ("Db5", .5), ("E5", .5), ("C5", 1), ("R", 1.5)],
    8: [("Db4", .5), ("Ab4", .5), ("Eb5", .5), ("Ab4", .5), ("F4", .5), ("Ab4", .5), ("Bb4", .5), ("Ab4", .5)],  # t8 THE CELL (chirper-two), Db lydian
    9: [("Eb4", .5), ("Ab4", .5), ("F4", .5), ("C5", 2.5)],
    16: [("C5", 1.5), ("Bb4", 1.5), ("G4", 1)],                                                          # t10 CORO (chirper-zero), in C
    17: [("F4", 1.5), ("G4", 2.5)],
    20: [("G4", 1), ("F4", .5), ("Eb4", .5), ("D4", 1), ("R", 1)],                                       # t4 MIRROR MELODY (chirper-two), a step down
    21: [("C5", .5), ("D5", .5), ("Eb5", 1), ("D5", .5), ("C5", .5), ("R", 1)],
    24: [("C5", .5), ("F5", 3.5)],                                                                       # t9 EXPOSURE (chirper-zero): a fourth up into Ebm11's 9th
    25: [("Bb4", .5), ("Eb5", 3), ("R", .5)],
}


def line(notes, vel=92, shift=0):
    return J(*[R(d) if n == "R" else tok(nm(mi(n) + shift), d, vel) for n, d in notes])


# ------------------------------------------------------------------ the rhythm section, per bar
def walk(c, nxt, beats, rng, two=False):
    """Walking bass: chord root on 1, scale/chord tones through the bar, a chromatic or scale approach into the next
    root on the last beat. `two`: half notes (the intro, the coda, the bridge's first bars)."""
    root, sc, _ = CH[c]
    nroot = CH[nxt][0]
    base = root if root >= 33 else root + 12
    if two:
        out, left = [], beats
        while left > 0:
            d = 2 if left >= 2 else left
            out.append(tok(nm(base if not out else base + 7), d, 92))
            left -= d
        return J(*out)
    pcs = [base + s for s in sc] + [base + 12 + s for s in sc]
    notes = [base]
    cur = 0
    for i in range(1, beats - 1):
        cur = max(0, min(len(pcs) - 1, cur + rng.choice([1, 1, 2, 2, -1, 3])))
        if rng.random() < 0.25:  # a chord tone instead of the scale step
            cur = rng.choice([0, 2, 4, 7]) if cur < 7 else rng.choice([7, 9, 11])
        notes.append(pcs[cur])
    tgt = nroot if nroot >= 33 else nroot + 12
    while tgt - notes[-1] > 7:
        tgt -= 12 if tgt - 12 >= 31 else 0
        if tgt - notes[-1] > 7 and tgt < 43:
            break
    notes.append(tgt + rng.choice([1, -1, -1]))  # chromatic approach from above or below
    vels = [96] + [84 + rng.randint(-4, 4) for _ in notes[1:]]
    return J(*[tok(nm(n), 1, v) for n, v in zip(notes, vels)])


COMP4 = [  # piano comping rhythms in 4/4 (onsets, durations), Charleston and its relatives
    [(0, 1.5), (1.5, 0.5)], [(1.5, 1)], [(0.5, 0.5), (2.5, 1)], [(0, 0.5), (3.5, 0.5)], [(1, 0.5), (2.5, 0.5)],
    [(1.5, 0.5), (3, 1)], [(0, 1)], [(2.5, 1.5)]]


def comp(c, beats, rng, vel=70, b=0):
    """Piano comp for one bar: rhythm cells drawn per bar (4/4 cells; 7/4 = a 4 cell + a 3 cell; 3/4 = 2&/1)."""
    _, _, v = CH[c]
    v = list(v)
    if b % 2:  # drop-2-ish re-voicing on alternate bars
        v = sorted(v[1:] + [v[0] + 12])
    ch = ",".join(nm(n) for n in v)
    if beats == 4:
        cells = [rng.choice(COMP4)]
        offs = [0]
    elif beats == 7:
        cells = [rng.choice(COMP4), rng.choice([[(0.5, 0.5), (2, 1)], [(1.5, 1.5)], [(0, 1), (2.5, 0.5)]])]
        offs = [0, 4]
    else:
        cells = [rng.choice([[(1.5, 0.5)], [(1, 1)], [(0, 0.5), (2, 1)], [(0.5, 0.5), (1.5, 1.5)]])]
        offs = [0]
    ev = sorted((o + a, d) for o, cell in zip(offs, cells) for a, d in cell)
    out, pos = [], 0.0
    for a, d in ev:
        if a < pos:
            continue
        out.append(R(a - pos))
        d = min(d, beats - a)
        out.append(tok(ch, d, vel + rng.randint(-6, 6)))
        pos = a + d
    out.append(R(beats - pos))
    return J(*out)


def ride(beats, rng, b, sec, vel=82):
    """The swung kit, one bar: ride 'ding ding-a', hi-hat foot on 2 and 4 (and 6 in 7/4), a feathered kick on 1,
    snare comping drawn per bar (chatter on off-beats), a crash on the section's first bar."""
    n8 = beats * 2
    hits = {i: [] for i in range(n8)}
    for q in range(beats):  # ride on every quarter, the skip note on the 'and' of 2 and 4 (and 6)
        hits[2 * q].append("rd")
        if q % 2 == 1:
            hits[2 * q + 1].append("rd")
        if q % 2 == 1:
            hits[2 * q].append("hf")
    hits[0].append("k")
    if sec != "waltz":
        for _ in range(rng.randint(1, 3)):
            hits[rng.randrange(1, n8, 2) if rng.random() < 0.7 else rng.randrange(0, n8)].append("so")
        if rng.random() < 0.3:
            hits[rng.randrange(2, n8)].append("k")
    if b == 0:
        hits[0].append("c")
    out = []
    for i in range(n8):
        if hits[i]:
            v = vel + (6 if i == 0 else 0) - (10 if i % 2 else 0)
            out.append(",".join(dict.fromkeys(hits[i])) + f"/0.5b@{v}")
        else:
            out.append(R(0.5))
    return J(*out)


def trip_bar(c, beats, rng, lo, hi, vel=96):
    """A bar phrased in quarter-note triplets (/6 = 2/3 beat): the line steps through the chord's scale three notes
    per two beats, crossing the bar's swing - the hard-bop horn's 3-over-2."""
    root, sc, _ = CH[c]
    pcs = sorted({(root + x) % 12 for x in sc})
    pool = [m for m in range(lo, hi + 1) if m % 12 in pcs]
    i = rng.randrange(len(pool) // 3, 2 * len(pool) // 3)
    step = rng.choice([1, -1])
    out = []
    for k in range(int(beats * 3 // 2)):
        out.append(f"{nm(pool[i])}/6@{vel + (6 if k % 3 == 0 else -4)}")
        i = max(0, min(len(pool) - 1, i + step * rng.choice([1, 1, 2])))
    rem = beats - (beats * 3 // 2) * 2 / 3
    return J(*out, R(rem))


def drum_trip(beats, rng, vel=96):
    """The drummer's triplet answer: triplet eighths (/12) around snare and toms, kick on each beat."""
    out = []
    for i in range(beats * 3):
        p = ["s", "t1", "t2", "s", "ft", "t2"][(i + rng.randrange(2)) % 6]
        if i % 3 == 0:
            p += ",k"
        out.append(f"{p}/12@{vel + (8 if i % 3 == 0 else -10) + rng.randint(-6, 4)}")
    return J(*out)


def drum_solo(beats, rng, vel=96):
    """Two bars of the drummer's answer in the trades: snare/tom phrases in swung eighths, kick punctuation."""
    out = []
    for i in range(beats * 2):
        r = rng.random()
        p = "s" if r < 0.35 else ("t1" if r < 0.55 else ("t2" if r < 0.7 else ("ft" if r < 0.82 else ("k" if r < 0.9 else ""))))
        if i % 4 == 0:
            p = (p + ",k") if p and p != "k" else "k"
        out.append(f"{p}/0.5b@{vel + rng.randint(-14, 8)}" if p else R(0.5))
    return J(*out)


DOR = [0, 2, 3, 5, 7, 9, 10]
RHYTHMS = [  # solo phrase rhythms (durations in beats), chosen per bar for variety
    [0.5] * 8, [1, 0.5, 0.5, 0.5, 0.5, 1], [0.5, 0.5, 1, 0.5, 0.5, 1], [1.5, 0.5, 0.5, 0.5, 1], [0.5] * 6 + [1],
    [1, 1, 0.5, 0.5, 1], [0.5, 0.5, 0.5, 0.5, 2]]


def solo(c, beats, rng, lo, hi, vel=94, rest_p=0.0):
    """A composed bebop-ish line for one bar over chord c: scale steps with chord-tone landings, chromatic passing
    tones, an arc within the bar; rhythm drawn from RHYTHMS (fitted to the bar)."""
    root, sc, _ = CH[c]
    pcs = sorted({(root + s) % 12 for s in sc})
    pool = [m for m in range(lo, hi + 1) if m % 12 in pcs]
    durs = []
    while sum(durs) < beats - 1e-9:
        r = rng.choice(RHYTHMS)
        for d in r:
            if sum(durs) + d > beats + 1e-9:
                durs.append(beats - sum(durs))
                break
            durs.append(d)
    durs = [d for d in durs if d > 1e-9]
    i = rng.randrange(len(pool) // 3, 2 * len(pool) // 3)
    up = rng.random() < 0.5
    out = []
    for k, d in enumerate(durs):
        if rng.random() < rest_p and k > 0:
            out.append(R(d))
            continue
        n = pool[i]
        if d == 0.5 and rng.random() < 0.15 and 0 < i < len(pool) - 1:
            n = pool[i] + (1 if up else -1)  # chromatic passing tone
        out.append(tok(nm(n), d, vel + rng.randint(-8, 6) + (6 if d >= 1 else 0)))
        step = rng.choice([1, 1, 1, 2]) * (1 if up else -1)
        i = i + step
        if i <= 0 or i >= len(pool) - 1 or rng.random() < 0.18:
            up = not up
            i = max(0, min(len(pool) - 1, i))
    return J(*out)


# ------------------------------------------------------------------ arrangement
def thirds(notes, chs):
    """The horn a diatonic third under the tenor: the chord-scale tone 3 or 4 semitones below (else a fourth)."""
    out = []
    for (n, d), c in zip(notes, chs):
        if n == "R":
            out.append((n, d))
            continue
        root, sc, _ = CH[c]
        pcs = {(root + x) % 12 for x in sc}
        m = mi(n)
        h = next((m - k for k in (3, 4, 5) if (m - k) % 12 in pcs), m - 5)
        out.append((nm(h), d))
    return out


def locked(piece, c):
    """Locked hands (Shearing / Garland): each melody note doubled an octave below, with the two chord tones nearest
    under it filling the octave - the line becomes a moving block of chords."""
    root, sc, v = CH[c]
    pcs = sorted({n % 12 for n in v} | {root % 12})
    out = []
    for t in piece.split():
        if t.startswith("R/"):
            out.append(t)
            continue
        head, rest = t.split("/", 1)
        m = mi(head)
        under = [n for n in range(m - 11, m) if n % 12 in pcs][-2:]
        out.append(",".join(nm(n) for n in [m - 12] + under + [m]) + "/" + rest)
    return " ".join(out)


def chords_for(sec, nb):
    if sec in ("intro", "coda"):
        return ["Cm11", "Cm11", "Dbmaj7#11", "Dbmaj7#11"][:nb]
    if sec == "headout" and REHARM:
        return OUT_CH
    if sec == "tag":
        return TAG_CH
    if sec in ("headA", "headA2", "headout"):
        return HEAD_CH
    if sec == "bridge":
        return BRIDGE_CH
    if sec == "stairup":
        return ["Bb7sus", "Bb7sus", "Bmaj7#11", "Bmaj7#11", "Dbmaj9", "Dbmaj9", "Ebmaj9", "Ebmaj9"]
    if sec == "tenor":
        return TENOR_CH
    if sec == "waltz":
        return WALTZ_CH
    if sec == "trades":
        return ["Cm11"] * nb
    if sec == "bsolo":
        return ["Cm11"] * 8 + ["Dbmaj7#11"] * 4 + ["G7alt"] * 4
    return ["Cm11"] * nb


def build():
    names = ("tenor", "horn", "piano", "bass", "kit")
    T = {n: [] for n in names}
    tempo, beat0 = [], 0.0
    rng = random.Random(7)
    for si, (sec, beats, nb, sw) in enumerate(FORM):
        tempo.append({"at": f"{beat0:g}b", "bpm": BPM, "meter": METER[beats]})
        chs = chords_for(sec, nb)
        for b in range(nb):
            c = chs[b]
            nxt = chs[b + 1] if b + 1 < nb else (chords_for(FORM[si + 1][0], FORM[si + 1][2])[0] if si + 1 < len(FORM) else c)
            bar = {n: R(beats) for n in names}
            if sec == "intro":
                bar["piano"] = comp(c, beats, rng, vel=58, b=b)
                if INTROTEN and b >= 2:  # the doors heard through the wall: SEVEN DOORS' bar 2 and bar 4 climbs, soft
                    bar["tenor"] = line(HEAD[1] if b == 2 else HEAD[3], vel=66)
                bar["bass"] = walk(c, nxt, beats, rng, two=True)
                bar["kit"] = J(*([tok("rd", 1, 60 + 4 * b)] + [tok("rd", 1, 52)] * (beats - 1)))
            elif sec in ("headA", "headA2", "headout", "tag"):
                hb = HEAD[b] if sec != "tag" else HEAD[6 + b % 2]
                bar["tenor"] = line(hb, vel=96 + (4 if sec in ("headout", "tag") else 0))
                bar["horn"] = line(hb, vel=84, shift=-5)
                if REHARM and sec in ("headout", "tag"):
                    bar["horn"] = line(thirds(hb, [c] * len(hb)), vel=86)
                bar["piano"] = comp(c, beats, rng, vel=68, b=b)
                bar["bass"] = walk(c, nxt, beats, rng)
                bar["kit"] = ride(beats, rng, b, sec)
                if TAGHORN and sec == "tag" and b == nb - 1:
                    run = ["D4", "F4", "Ab4", "B4", "D5", "F5"]
                    bar["tenor"] = J(*[f"{n}/6@{100 + 2 * i}" for i, n in enumerate(run)], tok("Eb5", 3, 108))
                    bar["horn"] = J(*[f"{nm(mi(n) - (3 if i % 2 else 4))}/6@{88 + 2 * i}" for i, n in enumerate(run)], tok("C5", 3, 96))
                if TAGTRIP and sec == "tag" and b % 2 == 1:
                    bar["kit"] = drum_trip(beats, rng, vel=90)
            elif sec == "bridge":
                bar["tenor"] = line(BRIDGE[b], vel=94)
                bar["horn"] = line(BRIDGE[b], vel=86, shift=-12)
                bar["piano"] = comp(c, beats, rng, vel=66, b=b)
                bar["bass"] = walk(c, nxt, beats, rng, two=(b < 2))
                bar["kit"] = ride(beats, rng, b, sec, vel=78)
            elif sec == "stairup":  # the stair climbs back: the bridge's figure pairs in reverse order, the horn a third under
                hb = BRIDGE[[6, 7, 4, 5, 2, 3, 0, 1][b]]
                bar["tenor"] = line(hb, vel=98)
                bar["horn"] = line(thirds(hb, [c] * len(hb)), vel=88)
                if STAIRTRIP and b % 2 == 1:
                    ns = [n for n, _ in hb if n != "R"][:3]
                    hs = [n for n, _ in thirds([(n, 1) for n in ns], [c] * 3)]
                    bar["tenor"] = J(*[f"{n}/6@{100 + 2 * i}" for i, n in enumerate(ns)], tok(ns[-1], 2, 96))
                    bar["horn"] = J(*[f"{n}/6@{88 + 2 * i}" for i, n in enumerate(hs)], tok(hs[-1], 2, 86))
                bar["piano"] = comp(c, beats, rng, vel=70, b=b)
                bar["bass"] = walk(c, nxt, beats, rng)
                bar["kit"] = ride(beats, rng, b, sec, vel=84)
            elif sec == "tenor":
                bar["tenor"] = (trip_bar(c, beats, rng, 55, 79, vel=92 + b // 4) if TRIP and b % 4 == 2
                                else solo(c, beats, rng, 51, 79, vel=88 + b // 4, rest_p=0.08 if b % 4 == 3 else 0.0))
                if OVERTURE and b in OVERTURE_Q:
                    bar["tenor"] = line(OVERTURE_Q[b], vel=94 + b // 4)
                bar["piano"] = comp(c, beats, rng, vel=64 + b // 4, b=b)
                bar["bass"] = walk(c, nxt, beats, rng)
                bar["kit"] = ride(beats, rng, b, sec, vel=80 + b // 4)
            elif sec == "waltz":
                bar["piano"] = J(solo(c, beats, rng, 60, 86, vel=80, rest_p=0.1 if b % 4 == 3 else 0.0))
                if LOCKED and b >= 24:
                    bar["piano"] = locked(bar["piano"], c)
                bar["horn"] = comp(c, beats, rng, vel=40, b=b) if b >= 16 else R(beats)  # the horn pads the second half
                bar["bass"] = walk(c, nxt, beats, rng, two=(b % 8 < 2))
                bar["kit"] = ride(beats, rng, b, sec, vel=70)
            elif sec == "bsolo":  # the upright sings: a line in its upper register, phrased in two-bar breaths
                bar["bass"] = (trip_bar(c, beats, rng, 43, 62, vel=100) if BTRIP and b % 4 == 2
                               else solo(c, beats, rng, 40, 62, vel=98, rest_p=0.12 if b % 2 == 1 else 0.0))
                bar["piano"] = comp(c, beats, rng, vel=50, b=b) if b % 2 == 0 else R(beats)
                bar["kit"] = ride(beats, rng, b, sec, vel=64)
            elif sec == "trades":  # tenor two bars, drums two bars
                if (b // 2) % 2 == 0:
                    bar["tenor"] = solo(c, beats, rng, 55, 82, vel=98)
                    bar["piano"] = comp(c, beats, rng, vel=70, b=b)
                    bar["bass"] = walk(c, nxt, beats, rng)
                    bar["kit"] = ride(beats, rng, b, sec, vel=86)
                else:
                    bar["kit"] = drum_trip(beats, rng) if DTRIP and b % 2 == 1 else drum_solo(beats, rng)
            elif sec == "coda":  # the vamp thins to the held last chord: Cm(add9) over the low C, the horn on the 9th
                if b < 2:
                    bar["piano"] = comp(c, beats, rng, vel=60, b=b)
                    bar["bass"] = walk(c, nxt, beats, rng, two=True)
                    bar["kit"] = ride(beats, rng, b, sec, vel=70)
                    bar["tenor"] = line(HEAD[b], vel=86)
                elif b == 2:
                    last = ",".join(nm(n) for n in (48, 55, 62, 63, 67))
                    bar["piano"] = tok(last, beats * 2, 72)
                    bar["bass"] = tok("C2", beats * 2, 90)
                    bar["tenor"] = tok("D5", beats * 2, 80)
                    bar["horn"] = tok("G4", beats * 2, 70)
                    bar["kit"] = J(tok("rd,c", 1, 72), R(beats * 2 - 1))
                else:
                    for n in names:
                        bar[n] = ""
            if b == nb - 1 and sec not in ("coda",):  # THE BREAK: the band stops at the bar's middle, the drums fill
                half = beats // 2 + (beats % 2) * 0.5 if beats != 3 else 1.5
                for n in names:
                    if n != "kit":
                        bar[n] = J(cut(bar[n], half), R(beats - half))
                n16 = int((beats - half) * 4)
                fill = [("s" if i % 3 else "t1" if i % 2 else "t2") + f"/0.25b@{78 + 3 * i}" for i in range(n16 - 2)]
                bar["kit"] = J(cut(bar["kit"], half), *fill, tok("c,k", 0.5, 112))
            for n in names:
                T[n].append((bar[n], beats, sw, b == 0))
            beat0 += beats
    return T, tempo, beat0


def cut(piece, beats):
    out, pos = [], 0.0
    for t in piece.split():
        if pos >= beats - 1e-9:
            break
        head, rest = t.split("/", 1)
        k = min([i for i in (rest.find("@"), rest.find("^")) if i >= 0] or [len(rest)])
        dur, tail = rest[:k], rest[k:]
        d = float(dur[:-1]) if dur.endswith("b") else 4.0 / float(dur)  # beats, or a note value (/6 = 2/3 beat)
        if d <= beats - pos + 1e-9:
            out.append(t)
        else:
            out.append(f"{head}/{beats - pos:.6g}b{tail}")
        pos += d
    if pos < beats - 1e-9:
        out.append(R(beats - pos))
    return " ".join(out)


def section_times():
    t, out = 0.0, {}
    for sec, beats, nb, _ in FORM:
        d = beats * nb * 60 / BPM
        out[sec] = (t, t + d)
        t += d
    return out


def master():
    bands = (["lowshelf cutoff=120 gain=3dB", "peak cutoff=700 q=0.7 gain=-2dB"] if MIX == "1" else
             ["lowshelf cutoff=150 gain=6dB", "peak cutoff=700 q=0.7 gain=-2dB", "highshelf cutoff=6000 gain=-4dB"])
    fx = [{"type": "eq", "bands": bands},
          {"type": "compressor", "threshold": "-22dB", "ratio": 2, "attack": "15ms", "release": "200ms", "makeup": "0dB"},
          {"type": "gain", "gain": f"+{MG:g}dB"}]
    st = section_times()
    lv = {"intro": -7, "headA": -2, "bridge": -3, "headA2": -1, "tenor": 0, "waltz": -6, "trades": 1, "headout": 2, "tag": 3, "coda": -3, "bsolo": -5, "stairup": 3}
    pts = [["0s", lv["intro"]]]
    for sec, *_ in FORM[1:]:
        a = st[sec][0]
        pts += [[f"{a - 0.5:.2f}s", pts[-1][1]], [f"{a:.2f}s", lv[sec]]]
    pts += [[f"{st['coda'][1] + 10:.2f}s", lv["coda"]]]
    fx.append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}})
    return {"fx": fx, "auto": {"dyn": {"points": pts}}}


UPRIGHT = {
    "about": "Doors at Seven's upright (chirper-zero): the pluck string model played by fingers - soft, round, a "
             "short thump, little buzz, a dark top - with a sine underneath; walking-bass dynamics.",
    "synth": {
        "layers": [
            {"name": "string", "type": "pluck", "stiff": 0.12, "buzz": 0.02, "pick": 0.45,
             **({"planes": float(PLANES.split(",")[0])} if PLANES else {}),
             **({"beat": float(PLANES.split(",")[1])} if "," in PLANES else {}),
             "decay": {"value": "1.6s", "mod": [{"src": "vel", "amount": 0.3}]},
             "bright": {"value": 0.3, "mod": [{"src": "vel", "amount": 0.2}, {"src": "rand", "amount": 0.04}]}},
            {"name": "sub", "wave": "sine", "level": f"{SUB}dB"},
            {"name": "thump", "type": "noise", "level": {"value": "-60dB", "mod": [{"src": "env.th", "amount": 34}]}},
        ],
        "pitch": {"value": 0, "mod": [{"src": "env.tw", "amount": 0.2}, {"src": "rand", "amount": 0.03}]},
        "env": {"tw": {"a": "0.2ms", "d": "60ms", "s": 0}, "th": {"a": "0.5ms", "d": "18ms", "s": 0}},
        "amp": {"a": "3ms", "s": 1, "r": "80ms"},
    },
    "play": {"mono": True, "gate": 0.92, "humanize": {"time": "6ms", "vel": 0.08}, "vel_sens": 0.5},
    "fx": [{"type": "eq", "bands": ["lowshelf cutoff=90 gain=2dB", "peak cutoff=250 q=0.9 gain=2dB", "highshelf cutoff=2500 gain=-9dB"]},
           {"type": "compressor", "threshold": "-24dB", "ratio": 3, "attack": "10ms", "release": "120ms", "makeup": "2dB"}],
    "gain": "-12dB",
}


def song():
    T, tempo, total = build()

    def sc(name):
        out, cur = [], None
        for s, beats, sw, first in T[name]:
            if s == "":
                continue
            if sw != cur:
                s = f"swing={sw:g} " + s
                cur = sw
            out.append(s)
        return " | ".join(out)

    tracks = [
        {"name": "tenor", "patch": "tenor-sax", "gain": "-5dB", "pan": 0.15, "sends": {"room": "-11dB"}, "score": sc("tenor")},
        {"name": "horn", "patch": "horn", "gain": "-9dB", "pan": -0.2, "sends": {"room": "-9dB"}, "score": sc("horn")},
        {"name": "piano", "patch": "piano", "gain": "-7dB", "pan": -0.1, "sends": {"room": "-12dB"}, "score": sc("piano")},
        {"name": "bass", "patch": "upright", "gain": "0dB", "score": sc("bass")},
        {"name": "kit", "patch": "room-kit", "gain": "-8dB", "score": sc("kit")},
    ]
    if MIX == "2":
        tracks[3]["gain"] = "4dB"
        tracks[4]["gain"] = "-13dB"
        tracks[4]["fx"] = [{"type": "eq", "bands": ["highshelf cutoff=4000 gain=-5dB"]}]
    return {
        "about": ("Chirpers - Odd Hours, track 1: Doors at Seven (the opener; original composition, chirper-zero; "
                  "generator compose/chirpers2/src/chirpers2-t1.py). A modal hard-bop quintet whose meter changes "
                  "with each chorus: swung 7/4 head (C dorian / Db lydian, G7alt turnaround) -> even-eighth 4/4 bridge "
                  "(a whole-step stair of major chords) -> head -> tenor solo in 4/4 -> piano trio in a 3/4 jazz waltz "
                  "-> tenor and drums trading twos in 7/4 -> head out -> coda on Cm(add9). 176 bpm, swing 0.62."),
        "tempo": BPM if SCALAR else tempo, "ceiling": "-0.1dB", "tail": "3s",
        "patches": {"upright": UPRIGHT},
        "buses": {"room": {"fx": ["reverb kind=room decay=1.2s size=0.6 mix=1 predelay=12ms"]}},
        "master": master(),
        "tracks": tracks,
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "tail", "patches", "master")]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
