#!/usr/bin/env python3
"""chirpers2-t7 (Odd Hours, track 7): "Cross Purposes". Composed by chirper-three.

GENTLE GIANT / ZAPPA COUNTERPOINT: a through-composed chamber-prog piece where the lines argue.

- THE SUBJECT: nine notes over a 7/8 + 5/8 pair, D F A G# E | G Eb F# D (semitones 0 3 7 6 2 | 5 1 4 0), angular
  and chromatic; its INVERSION is the countersubject.
- FORM (every bar changes something; the meters say how long each bar is, in eighths):
    0 CHORALE    the subject SUNG first: a slow mellotron-choir chorale, each note harmonised afresh (Dm Bb F E Am C
                 Cm D D5), flute on top, bass on the roots, no drums;
    1 STATEMENT  the subject HOCKETED note by note across marimba / flute / muted trumpet / guitar (the rotation turns
                 one place each time), then in unison, then inverted low under hocketed fragments;
    2 FUGUE      four entries (sax at D, trumpet at A, guitar inverted, bass), each continuing with the countersubject,
                 on their own 12-eighth cycle while the kit and chords walk t4's METER PALINDROME (6 5 7 8 7 5 6 eighths);
                 so each bar's texture differs; wurli stabs a new chord every bar;
    3 BLACK PAGE a PERCUSSION ORCHESTRA in sixteenth meters (11 13 9 15 11 13 7 17 sixteenths): the subject in
                 diminution on tuned toms + marimba, bass and kick on the threes, snare on the twos;
    4 CROSS      CROSS PURPOSES: horns + wurli in 7/8 cycles against flute + marimba + guitar in quarter-note
                 TRIPLETS (3 against 7, hats on the triplets), the subject
                 augmented in the bass, a ride bell on the 7 (12 bars of 4/4);
    4b SOLO      a ZAPPA GUITAR SOLO (wah lead) over a lydian vamp in 7/8 (Dmaj7#11 | E/D): subject fragments,
                 quintuplet runs up, sextuplet runs down, a high cry; 2+2+3 D-pedal bass, the Rhodes on the vamp;
    5 TRADES     sax and trumpet trade single bars, then pairs, over a meter wheel 7 5 6 9 (24 bars), walking bass;
                 each traded bar develops the subject (cyclic start, on the bar's chord, as written / inverted / retrograde);
                 the hushed part is a SWINGING BRUSH TRIO: flute and jazz guitar trade swung bars, a Rhodes through
                 wM's Bassman stack comps, the bass walks, chirper-two's brushes; the horns take the straight wake-up;
    6 STRETTO    subject entries every two eighths in every voice, the climax, a whole tone up (E) after a B7alt pivot,
                 over bars that GROW BY A 3 (t3's build: 2+2, 2+2+3, ... 2+2+3+3+3+3), wurli stabs on every group;
    7 CODA       THE ANSWER to chirper-two's t8: their 12-eighth CELL on two marimbas phasing an eighth a bar, the
                 subject augmented bass -> flute, the clock across; then the CHORALE returns singing the INVERSION
                 (fuller: trumpet and sax join, resolving to D major), and the final chord is built one hocketed note at a time.
- KIT: prog-kit, groupings follow each meter (7 = 2+2+3 or 3+2+2 alternating bar by bar, 5 = 3+2 / 2+3, 9 = 2+2+2+3,
  6 = 3+3, 8 = 3+3+2): kick on group starts, snare on the last group, hats on the eighths.

Emits songs/chirpers2-t7.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T7_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers2-t7.yaml")
BPM = 100
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
D4 = 62

SUBJ = [(0, 1), (3, 1), (7, 1), (6, 2), (2, 2), (5, 1), (1, 1), (4, 1), (0, 2)]   # (semitones from tonic, eighths)
INV = [(-p, d) for p, d in SUBJ]
SUBJ_LEN = 12                                                                         # 7 + 5 eighths

# One chord per bar, cycling: (root pitch class, intervals). Modal / quartal / altered.
PROG = [(2, [0, 3, 7, 10, 14]), (10, [0, 4, 7, 11, 18]), (4, [0, 3, 6, 10]), (9, [0, 4, 10, 13, 15]),
        (5, [0, 4, 7, 11, 18]), (7, [0, 4, 10, 14, 21]), (1, [0, 3, 6, 9]), (2, [0, 5, 10, 15])]

GROUPS = {5: [[3, 2], [2, 3]], 6: [[3, 3], [2, 2, 2]], 7: [[2, 2, 3], [3, 2, 2]], 8: [[3, 3, 2], [2, 3, 3]],
          9: [[2, 2, 2, 3], [3, 3, 3]], 12: [[3, 3, 3, 3], [2, 2, 2, 3, 3]]}


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Part:
    def __init__(self):
        self.ev = []                         # (start eighths, length eighths, head, vel)

    def add(self, st, ln, head, vel):
        self.ev.append((st, ln, head, int(max(1, min(127, vel)))))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-4:
                toks.append(f"R/{(s - pos) / 2:.4g}b")
            toks.append(f"{head}/{ln / 2:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{(total - pos) / 2:.4g}b")
        return " ".join(toks)


P = {k: Part() for k in ("mar", "flute", "tpt", "sax", "gtr", "keys", "bass", "kick", "snare", "hat", "toms", "ride",
                         "clock", "sub", "brush", "tap", "rhodes", "ttom", "mar2", "choir", "lead")}
BARS = []          # (start eighths, length eighths, section, index in section)
rng = random.Random(7)


def line(part, st, notes, base, vel, scale=1.0, art=1.0):
    """Place a (semitone, eighths) line from st; returns the end time."""
    t = st
    for p, d in notes:
        part.add(t, d * scale * art, nm(base + p), vel)
        t += d * scale
    return t


def chord_at(i):
    return PROG[i % len(PROG)]


def kit_bar(st, ln, k, vel=96, fill=False, hats=True, grp=None):
    """Kick on group starts, snare on the last group, hats on the eighths; the grouping alternates bar by bar."""
    if grp is None:
        opts = GROUPS.get(ln) or [[2] * (ln // 2) + ([ln % 2] if ln % 2 else [])]
        grp = opts[k % len(opts)]
    t = st
    for gi, g in enumerate(grp):
        if gi == len(grp) - 1 and len(grp) > 1:
            P["snare"].add(t, 1, "s", vel + 4)
        else:
            P["kick"].add(t, 1, "k", vel + (8 if gi == 0 else 0))
        t += g
    for e in range(int(ln) if hats else 0):
        accent = e == 0 or e in [sum(grp[:j]) for j in range(len(grp))]
        P["hat"].add(st + e, 1, "h", (vel - 14) if accent else (vel - 30))
    if rng.random() < 0.5 and ln >= 6:                                        # a ghost before the snare
        P["snare"].add(st + ln - grp[-1] - 0.5, 0.5, "g", vel - 40)
    if fill:
        for j, tom in enumerate(("t1", "t2", "t3", "ft")):
            P["toms"].add(st + ln - 2 + j * 0.5, 0.5, tom, vel + 2)


def bar(st, ln, sec, i):
    BARS.append((st, ln, sec, i))


def harmony_bar(st, ln, ci, vel=80, bass=True, stabs=True, walk=False, chord=None):
    root, iv = chord or chord_at(ci)
    if stabs:
        voic = [60 + ((root + x) % 12) for x in iv[1:]]
        head = ",".join(nm(m) for m in sorted(set(voic)))
        P["keys"].add(st, 0.8, head, vel)
        P["keys"].add(st + ln - 2, 0.8, head, vel - 12)
    if bass:
        b = 38 + ((root - 2) % 12)                                            # around D2
        if walk:
            nxt_root = chord_at(ci + 1)[0]
            tones = [b, b + iv[1], b + iv[2], b + 12 - 2]
            for e in range(int(ln)):
                if e == ln - 1:
                    tgt = 38 + ((nxt_root - 2) % 12)
                    P["bass"].add(st + e, 1, nm(tgt + (1 if rng.random() < 0.5 else -1)), vel + 4)
                else:
                    P["bass"].add(st + e, 1, nm(tones[e % len(tones)] + (12 if e % 4 == 3 else 0)), vel + (8 if e == 0 else 0))
        else:
            P["bass"].add(st, ln - 1, nm(b), vel + 10)
            P["bass"].add(st + ln - 1, 1, nm(b + 7), vel)


# ---------- 0 CHORALE ----------
CHORALE = [  # (melody semitones from D4, chord root pitch class, chord tones above the root)
    (0, 2, [0, 3, 7]),      # D   over Dm
    (3, 10, [0, 4, 7]),     # F   over Bb
    (7, 5, [0, 4, 7]),      # A   over F
    (6, 4, [0, 4, 7]),      # G#  over E
    (2, 9, [0, 3, 7]),      # E   over Am
    (5, 0, [0, 4, 7]),      # G   over C
    (1, 0, [0, 3, 7]),      # Eb  over Cm
    (4, 2, [0, 4, 7]),      # F#  over D
    (0, 2, [0, 7, 12]),     # D   over an open fifth
]


CHORALE_INV = [  # the close: the INVERSION sung, reharmonised, resolving to D major
    (0, 10, [0, 4, 7]),     # D   over Bb
    (-3, 7, [0, 4, 7]),     # B   over G
    (-7, 3, [0, 4, 7]),     # G   over Eb
    (-6, 4, [0, 4, 7]),     # G#  over E   (the opening's G#/E, mirrored)
    (-2, 9, [0, 3, 7]),     # C   over Am
    (-5, 5, [0, 4, 7]),     # A   over F
    (-1, 9, [0, 4, 7]),     # C#  over A
    (-4, 7, [0, 3, 7]),     # Bb  over Gm
    (0, 2, [0, 4, 7]),      # D   over D major: the dispute resolves
]


def sing(t, rows, v0, full=False, sec="chorale"):
    """A chorale: the melody on top of the mellotron choir, one note a half bar (the last a whole bar), each harmonised
    afresh; flute on the melody, bass on the roots; `full` adds the muted trumpet an octave under the melody and the
    sax on an inner voice."""
    for j, (p, root, iv) in enumerate(rows):
        ln = 8 if j == len(rows) - 1 else 4
        v = v0 + 3 * j
        mel = D4 + 12 + p
        inner = sorted({mel - 12 - ((mel - 12 - (48 + root + x)) % 12) for x in iv} - {mel})
        P["choir"].add(t, ln * 0.97, ",".join(nm(m) for m in inner + [mel]), v)
        P["flute"].add(t, ln * 0.95, nm(mel), v - 6)
        P["bass"].add(t, ln * 0.95, nm(36 + root), v)
        if full:
            P["tpt"].add(t, ln * 0.95, nm(mel - 12), v - 4)
            P["sax"].add(t, ln * 0.95, nm(inner[0]), v - 8)
        if j % 2 == 0:
            bar(t, 8, sec, j // 2)
        t += ln
    return t


def chorale(t):
    """The piece opens by SINGING the subject before arguing it (Gentle Giant's madrigal voices): a slow chorale, one
    note a half bar, the subject on top of a mellotron choir, each note harmonised afresh (Dm Bb F E Am C Cm D D5),
    the flute on the melody, the bass on the roots; no drums, rising into the hocket."""
    return sing(t, CHORALE, 54)


# ---------- 1 STATEMENT ----------
def statement(t):
    rot = ["mar", "flute", "tpt", "gtr"]
    for rep in range(2):                                       # the subject hocketed, rotation turning
        x = t
        for j, (p, d) in enumerate(SUBJ):
            who = rot[(j + rep) % 4]
            base = D4 - 12 if who == "gtr" else D4
            P[who].add(x, d * 0.9, nm(base + p), 78 + 6 * rep)
            x += d
        bar(t, 7, "statement", 2 * rep); bar(t + 7, 5, "statement", 2 * rep + 1)
        for k in range(2):
            P["hat"].add(t + 7 * k, 1, "h", 50)
        if rep == 1:
            harmony_bar(t, 7, 0, 70, stabs=False); harmony_bar(t + 7, 5, 1, 70, stabs=False)
        t += SUBJ_LEN
    for who, base, v in (("mar", D4, 96), ("flute", D4 + 12, 88), ("tpt", D4, 92), ("sax", D4 - 12, 90),
                         ("gtr", D4 - 12, 86)):                  # in unison, the band arrives
        line(P[who], t, SUBJ, base, v, art=0.9)
    bar(t, 7, "statement", 4); bar(t + 7, 5, "statement", 5)
    kit_bar(t, 7, 0, 92); kit_bar(t + 7, 5, 1, 92)
    harmony_bar(t, 7, 2, 84); harmony_bar(t + 7, 5, 3, 84)
    t += SUBJ_LEN
    line(P["sax"], t, INV, D4 - 12, 92); line(P["bass"], t, INV, D4 - 24, 96)          # inverted, low
    frag = [(0, "mar", 3), (3, "flute", 7), (6, "mar", 6), (8, "tpt", 2), (10, "flute", 5)]
    for o, who, p in frag:                                       # hocketed fragments answer above
        P[who].add(t + o, 1, nm(D4 + 12 + p), 80)
    bar(t, 7, "statement", 6); bar(t + 7, 5, "statement", 7)
    kit_bar(t, 7, 1, 94); kit_bar(t + 7, 5, 0, 94, fill=True)
    P["keys"].add(t, 0.8, "D4,F4,A4,C5,E5", 86)
    return t + SUBJ_LEN


# ---------- 2 FUGUE ----------
T4_PALINDROME = [6, 5, 7, 8, 7, 5, 6]     # chirper-two's t4 meters in eighths (3/4 5/8 7/8 4/4 7/8 5/8 3/4), borrowed
def fugue(t):
    a = t
    voices = [("sax", D4 - 12, SUBJ, 0), ("tpt", D4 + 7, SUBJ, 1), ("gtr", D4 - 12, INV, 2), ("bass", D4 - 24, SUBJ, 3)]
    for who, base, subj, k in voices:
        st = a + k * SUBJ_LEN
        e = line(P[who], st, subj, base, 92)
        cs = INV if subj is SUBJ else SUBJ
        e = line(P[who], e, cs, base + (5 if k % 2 else -2), 86)          # the countersubject, displaced
        if k < 2:
            line(P[who], e, SUBJ[:5], base + 3, 84)                       # a free tail on the subject's head
    # the kit and the chords walk chirper-two's t4 METER PALINDROME (3/4 5/8 7/8 4/4 7/8 5/8 3/4, there and back),
    # while the entries keep the subject's own 12-eighth cycle: the fugue floats across t4's mirrored barlines
    for i, ln in enumerate(T4_PALINDROME * 2 + [8]):              # 44 + 44 + 8 = 96 eighths
        bar(t, ln, "fugue", i)
        harmony_bar(t, ln, i, 76 + 2 * (i // 4), bass=(t - a < 3 * SUBJ_LEN))
        kit_bar(t, ln, i, 88 + i, fill=(i % 7 == 6))
        if i >= 8 and i % 2 == 0:                                 # the marimba doubles the inner voice's head
            line(P["mar"], t, SUBJ[:3], D4 + 12 + (i % 5), 74)
        t += ln
    return t


# ---------- 3 BLACK PAGE ----------
def black_page(t):
    """A PERCUSSION ORCHESTRA (after Zappa's Black Page, first a drum solo): the subject in diminution on TUNED TOMS
    (chirper-two's physical drum layer, borrowed from t4's tom choir and tightened), the marimba an octave above, bass
    and kick on the threes, snare on the twos; the flute, horns, guitar and keys fall silent."""
    meters16 = [11, 13, 9, 15, 11, 13, 7, 17]
    k = 0
    for i, m in enumerate(meters16):
        ln = m / 2                                               # eighths
        bar(t, ln, "black", i)
        x, j = 0.0, 0
        groups = []
        rest = m
        while rest > 0:                                          # 2s and 3s, alternating starts bar by bar
            g = 3 if ((j + i) % 2 == 0 and rest != 4) or rest == 3 else 2
            g = min(g, rest)
            groups.append(g)
            rest -= g
            j += 1
        for g in groups:
            p, _ = SUBJ[k % len(SUBJ)]
            st = t + x / 2
            v = 108 if x == 0 else 94
            P["ttom"].add(st, g / 2, nm(D4 - 12 + p), v)
            P["mar"].add(st, g / 2 * 0.8, nm(D4 + p), v - 8)
            if g == 3:
                P["bass"].add(st, g / 2 * 0.8, nm(D4 - 24 + p), v - 4)
                P["kick"].add(st, 0.5, "k", v - 6)
            else:
                P["snare"].add(st, 0.5, "s", v - 10)
            x += g
            k += 1
        t += ln
    return t


# ---------- 4 CROSS PURPOSES ----------
CROSS_KEY = 0  # tried 3 (cross purposes in F): recurrence unmoved (its matches are timbral), s11 -1.0; kept in D


def cross(t):
    a, z = t, t + 12 * 8
    K = CROSS_KEY
    x = a                                                         # horns + wurli: the subject's 7/8 bar, cycling
    n = 0
    while x < z:
        for p, d in SUBJ[:5]:
            if x < z:
                P["tpt" if n % 2 == 0 else "sax"].add(x, d * 0.85, nm(D4 + K + p + (12 if n % 2 == 0 else 0)), 88)
            x += d
        P["keys"].add(x - 7, 0.6, ",".join(nm(m + K) for m in ((62, 67, 72) if n % 2 else (64, 69, 74))), 74)
        P["ride"].add(x - 7, 1, "D5", 100)                         # the ride bell marks the 7
        n += 1
    x, n = a, 0                    # flute + marimba + guitar: QUARTER-NOTE TRIPLETS, six to the bar: 3 against the horns' 7
    fig = [(0, 4 / 3), (-5, 4 / 3), (-1, 4 / 3), (-4, 4 / 3), (0, 4 / 3), (2, 4 / 3)]
    while x < z - 1e-6:
        for p, d in fig:
            who = ("flute", "mar", "gtr")[n % 3]
            base = (D4 + 12 if who != "gtr" else D4) + K
            P[who].add(x, d * 0.9, nm(base + p + (3 if n % 4 == 3 else 0)), 82)
            x += d
        n += 1
    line(P["bass"], a, SUBJ * 4, D4 - 24 + K, 100, scale=2.0)      # the subject augmented, four times
    for i in range(12):
        bar(t, 8, "cross", i)
        kit_bar(t, 8, i, 94 + (i // 3) * 2, fill=(i == 11), hats=False)
        for q in range(6):                                          # the hats join the triplets
            P["hat"].add(t + q * 4 / 3, 0.5, "h", 80 if q % 3 == 0 else 62)
        t += 8
    return t


# ---------- 4b THE SOLO ----------
LYD = [0, 2, 4, 6, 7, 9, 11]          # D lydian


def lyd_note(i):
    return D4 + LYDIAN[i % 7] + 12 * (i // 7)


def solo(t):
    """A ZAPPA GUITAR SOLO over a lydian vamp in 7/8 (Dmaj7#11 | E/D), between cross purposes and the hush: the wah
    lead varies bar by bar between a subject fragment ending on a held note, a QUINTUPLET run up the scale, a SEXTUPLET
    run down, and a breath before a high cry; the bass holds a 2+2+3 D-pedal ostinato, the Rhodes stabs the vamp."""
    a = t
    srng = random.Random(29)
    for i in range(8):
        ln = 7
        bar(t, ln, "solo", i)
        kit_bar(t, ln, i, 96 + i)
        e_over_d = i % 2 == 1
        chord = "E4,Ab4,B4,D5" if e_over_d else "Gb4,A4,Db5,E5"
        for o in (0, 4):
            P["rhodes"].add(t + o, 1.5, chord, 76)
        for o, d, m in ((0, 2, 38), (2, 2, 38), (4, 1, 45), (5, 2, 49 if e_over_d else 50)):
            P["bass"].add(t + o, d * 0.9, nm(m), 96 if o == 0 else 84)
        kind = (0, 1, 2, 3, 1, 0, 2, 3)[i]
        v = 96 + i
        if kind == 0:                       # a subject fragment, the last note held
            k0 = (2 * i) % 9
            x = 0.0
            for j in range(4):
                p, _ = SUBJ[(k0 + j) % 9]
                d = 1 if j < 3 else 3.5
                P["lead"].add(t + x, d * 0.95, nm(D4 + 12 + p), v + (6 if j == 3 else 0))
                x += d
        elif kind == 1:                     # quintuplet sixteenths up the lydian scale: 5 to the beat for two beats
            s0 = srng.randrange(5, 9)
            for j in range(10):
                P["lead"].add(t + j * 0.4, 0.38, nm(lyd_note(s0 + j)), v - 6 + (8 if j % 5 == 0 else 0))
            P["lead"].add(t + 4, 3, nm(lyd_note(s0 + 11)), v + 6)
        elif kind == 2:                     # sextuplets down: 6 to the beat for two beats, then a low growl
            s0 = srng.randrange(12, 15)
            for j in range(12):
                P["lead"].add(t + j / 3, 0.32, nm(lyd_note(s0 - j)), v - 6 + (8 if j % 6 == 0 else 0))
            P["lead"].add(t + 4, 2.5, nm(lyd_note(s0 - 13)), v)
        else:                               # a breath, then the high cry (the #11 resolving up)
            P["lead"].add(t + 1.5, 2.5, nm(D4 + 24 + 8), v + 4)
            P["lead"].add(t + 4, 2.8, nm(D4 + 24 + 9), v + 8)
        t += ln
    return t


# ---------- 5 TRADES ----------
def improv_bar(who, st, ln, ci, prev, vel):
    root, iv = chord_at(ci)
    pool = sorted({(root + x) % 12 for x in iv} | {(root + 2) % 12, (root + 5) % 12})
    lo, hi = (55, 79) if who == "tpt" else (46, 70)
    p = prev
    x = 0.0
    while x < ln - 1:
        d = rng.choice([0.5, 0.5, 1, 1, 1, 1.5, 2]) if x < ln - 2 else 1
        step = rng.choice([-2, -1, 1, 2, 3, -3, 5, -4])
        p = max(lo, min(hi, p + step))
        while p % 12 not in pool and rng.random() < 0.75:
            p += 1 if step > 0 else -1
        P[who].add(st + x, d * 0.92, nm(p), vel + int(8 * rng.random()) + (6 if x == 0 else 0))
        x += d
    return p


SWING = 0.62          # where a swung off-beat eighth lands within its beat (0.5 straight, 0.667 triplet)


def swing(x):
    """Map a position in eighths onto a swung beat: the first eighth of each beat stretches to SWING of it."""
    beat = 2.0 * int(x // 2)
    f = x - beat
    return beat + (f * 2 * SWING if f <= 1 else 2 * SWING + (f - 1) * (2 - 2 * SWING))


def motif_bar(who, st, ln, i, vel, swung=False):
    """A traded bar as MOTIVIC DEVELOPMENT: the subject read cyclically from a moving start, transposed onto the bar's
    chord root, alternately as written, inverted and in retrograde, filling the bar less a breath."""
    root, _ = chord_at(i)
    lo = {"tpt": 62, "sax": 50, "flute": 74, "gtr": 55}[who]
    base = lo + ((root - lo) % 12)
    form = i % 3
    seq = SUBJ if form != 2 else SUBJ[::-1]
    k = (2 * i) % len(seq)
    x = 0.0
    while x < ln - 1 - 1e-6:
        p, d = seq[k % len(seq)]
        if form == 1:
            p = -p
        d = min(d, ln - 1 - x)
        a, b = (swing(x), swing(x + d)) if swung else (x, x + d)
        P[who].add(st + a, (b - a) * 0.92, nm(base + p), vel + (6 if x == 0 else 0))
        x += d
        k += 1


def walk_quarters(st, ln, ci, vel):
    """A walking bass on the quarters: chord tones up the bar, a chromatic approach into the next bar's root; an odd
    bar ends with a half-beat pickup."""
    root, iv = chord_at(ci)
    nxt = 38 + ((chord_at(ci + 1)[0] - 2) % 12)
    b = 38 + ((root - 2) % 12)
    tones = [b, b + iv[1], b + iv[2], b + (iv[3] if len(iv) > 3 else 12)]
    beats = int(ln // 2)
    for q in range(beats):
        last = q == beats - 1 and ln % 2 == 0
        m = (nxt + (1 if (ci + q) % 2 else -1)) if last else tones[q % len(tones)]
        P["bass"].add(st + 2 * q, 1.9, nm(m), vel + (6 if q == 0 else 0))
    if ln % 2:
        P["bass"].add(st + 2 * beats, 0.9, nm(nxt - 1), vel - 4)


def brush_bar(st, ln, i, vel):
    """chirper-two's brush kit (borrowed from t4): a sweep through the bar, taps on alternate beats, the ride on every
    beat with its swung skip, all under the soloists (no kick: the hush keeps its floor in the bass)."""
    P["brush"].add(st, ln * 0.95, "bs" if ln < 8 else "bsl", vel - 18)
    beats = int(ln // 2)
    for q in range(beats):
        x = st + 2 * q
        P["ride"].add(x, 0.9, "D5", vel - 50)
        if q % 2 == 1:
            P["tap"].add(x, 0.5, "bt", vel - 4)
            P["ride"].add(x + 2 * SWING, 0.4, "D5", vel - 56)


def trades(t):
    """A hushed chamber episode after the loud middle: the soloists trade quietly over a walking bass, the kit drops to
    the hat pedal marking each bar's groups, one soft wurli chord a bar; it wakes for the last wheel turn into the stretto."""
    wheel = [7, 5, 6, 9]
    pt, ps = 69, 58
    for i in range(24):
        ln = wheel[i % 4]
        late = i >= 20
        # the swung trio trades between FLUTE and JAZZ GUITAR (their own colours, not the fugue's horns); the horns take
        # the straight last wheel turn into the stretto
        pair = ("tpt", "sax") if late else ("flute", "gtr")
        who = pair[(i if i < 16 else i // 2) % 2]                 # single bars, then pairs
        v = (84 + i // 3) if late else (60 + i // 2)
        motif_bar(who, t, ln, i, v, swung=not late)
        bar(t, ln, "trades", i)
        if late:
            # the last bar pivots on B7alt, the dominant of E, where the stretto climbs
            harmony_bar(t, ln, i, 70 + i // 2, walk=True, chord=(11, [0, 4, 10, 13, 15]) if i == 23 else None)
            kit_bar(t, ln, i, 84 + i // 2, fill=(i == 23))
        else:
            walk_quarters(t, ln, i, 76)
            root, iv = chord_at(i)                               # a rootless Rhodes voicing through a Bassman, on the and
            P["rhodes"].add(t + swing(1), ln - 1.5, ",".join(nm(55 + ((root + x - 7) % 12)) for x in iv[1:]), 58)
            brush_bar(t, ln, i, 70)
        if i % 4 == 3:                                            # the marimba answers each wheel turn
            line(P["mar"], t + ln - 3, [(7, 1), (6, 1), (2, 1)], D4 + 12, 76)
        t += ln
    return t


# ---------- 6 STRETTO ----------
LIFT = 2      # the stretto climbs a whole tone (E) for the climax; the coda steps home to D


def stretto(t):
    a = t
    entries = [("bass", D4 - 24), ("gtr", D4 - 12), ("sax", D4 - 12), ("keys", D4), ("tpt", D4 + 7), ("mar", D4 + 12),
               ("flute", D4 + 12)]
    entries = [(who, base + LIFT) for who, base in entries]
    for j, (who, base) in enumerate(entries):
        e = line(P[who], a + 2 * j, SUBJ, base, 96 + j)
        line(P[who], e, INV, base, 92 + j)
    # the bars GROW BY A 3 each (chirper-one's t3 build, borrowed): 2+2, 2+2+3, ... 2+2+3+3+3+3, the accents piling
    # up under the crowding entries; the wurli stabs every group start
    for i in range(5):
        grp = [2, 2] + [3] * i
        ln = sum(grp)
        bar(t, ln, "stretto", i)
        kit_bar(t, ln, i, 102 + 2 * i, fill=(i == 4), grp=grp)
        x = t
        root, iv = chord_at(i + 3)
        for g in grp:
            P["keys"].add(x, 0.6, ",".join(nm(60 + ((root + LIFT + y) % 12)) for y in iv[1:]), 84 + 2 * i)
            x += g
        t += ln
    return t


# ---------- 7 CODA ----------
T8_CELL = [0, 4, 8, 4, 2, 4, 5, 4, 1, 4, 2, 6]      # chirper-two's CELL from t8 (Mallet Chamber in Phase), borrowed
LYDIAN = [0, 2, 4, 6, 7, 9, 11]                    # D lydian: its G# is also a note of the subject


def lyd(d, base):
    return base + LYDIAN[d % 7] + 12 * (d // 7)


def coda(t):
    """THE ANSWER (to chirper-two's t8, which sings this subject in its bridge): four bars of 12/8. Their CELL turns on a
    low marimba in D lydian while a second marimba plays it an eighth further ahead each bar (their phasing, compressed);
    the subject, augmented, passes from the bass to the flute; the clock's fives tick across their twelves."""
    line(P["bass"], t, SUBJ, D4 - 24, 92, scale=2.0)
    line(P["flute"], t + 24, SUBJ, D4 + 12, 84, scale=2.0)
    for i in range(4):
        st = t + 12 * i
        bar(st, 12, "coda", i)
        kit_bar(st, 12, i, 76 + 2 * i)
        harmony_bar(st, 12, 7 * i, 64, bass=False, stabs=(i % 2 == 0))
        for e, d in enumerate(T8_CELL):
            P["mar"].add(st + e, 0.9, nm(lyd(d, D4 - 12)), 74 + (8 if e in (0, 6) else 0))
            P["mar2"].add(st + e, 0.9, nm(lyd(T8_CELL[(e + i) % 12], D4)), 66 + (8 if e in (0, 6) else 0))
    t += 48
    t = sing(t, CHORALE_INV, 66, full=True, sec="coda")              # the close sings the inversion, resolving to D major
    stack = [("bass", D4 - 24), ("gtr", D4 - 12 + 3), ("sax", D4 - 12 + 7), ("keys", D4 + 6), ("tpt", D4 + 2),
             ("mar", D4 + 12 + 5), ("flute", D4 + 12 + 1)]               # the subject's pitch set, one note an eighth
    for j, (who, m) in enumerate(stack):
        P[who].add(t + j, 14 - j, nm(m), 84 + 3 * j)
    bar(t, 8, "coda", 2); bar(t + 8, 8, "coda", 3)
    P["kick"].add(t + 14, 1, "k", 118); P["snare"].add(t + 14, 1, "s", 116)
    P["toms"].add(t + 14, 1, "ft", 112)
    return t + 16


def clock(spans):
    """THE CLOCK: a toy piano ticking every 5 sixteenths (2.5 eighths), cycling the subject's pitches high up, accented
    every fourth tick: a gear that turns against every meter (3 vs 5 vs 7 under cross purposes) and lands somewhere new
    in each bar. It ticks through the fugue and cross purposes only, so the other sections keep their own density."""
    k = 0
    for name, v0 in (("fugue", 64), ("cross", 72), ("coda", 58)):  # where it is a third party to the argument
        a, z = spans[name]
        if name == "coda":
            z = a + 48                                            # across the answer, not the final stack
        x = a
        key = CROSS_KEY if name == "cross" else 0
        while x < z - 0.25:
            p, _ = SUBJ[k % len(SUBJ)]
            P["clock"].add(x, 1.0, nm(D4 + 24 + key + p), v0 + (14 if k % 4 == 0 else 0))
            x += 2.5
            k += 1


def sub_floor(spans):
    """The SUB: the bass doubled an octave down by a sine in the loud sections (the lows sat 11-17 dB under the album
    at 38-71 Hz; after chirper-one's 'low end under the fretless' in t2, transformed: it follows the whole bass line)."""
    quiet = (spans["trades"][0], [b for b in BARS if b[2] == "trades"][20][0])
    for st, ln, head, vel in P["bass"].ev:
        if quiet[0] <= st < quiet[1] or st < 2 * SUBJ_LEN:
            continue
        m = NAMES.index(head[:-1]) + 12 * (int(head[-1]) + 1) - 12        # an octave under the bass
        P["sub"].add(st, ln, nm(m + 12 if m < 26 else m), vel)           # never under D1 (37 Hz)


def dyn_lane():
    """Master dynamics (dB, after the glue): the trades hush by 6 dB until their last wheel turn."""
    sec = lambda e: e / 2 * 60 / BPM
    ts = [b for b in BARS if b[2] == "trades"]
    a, w = ts[0][0], ts[20][0]
    pts = [(0, 0.0), (a - 0.2, 0.0), (a + 1.0, -6.0), (w - 1.0, -6.0), (w + 0.5, 0.0)]
    return [[f"{sec(e):.2f}s", v] for e, v in pts]


def main():
    t = 0.0
    spans = {}
    for sec in (chorale, statement, fugue, black_page, cross, solo, trades, stretto, coda):
        a = t
        t = sec(t)
        spans[sec.__name__] = (a, t)
    total = t
    clock(spans)
    sub_floor(spans)
    MAR = {"about": "Cross Purposes' marimba (chirper-three): additive wooden-bar partials 1 / 3.93 / 9.2 with a mallet click.",
           "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [3.93, 0.32], [9.2, 0.07]]},
                                {"name": "click", "type": "noise", "level": {"value": "-70dB", "mod": [{"src": "env.ck", "amount": 40}]}}],
                     "env": {"ck": {"a": "0.2ms", "d": "5ms", "s": 0}},
                     "filters": ["hp cutoff=120"],
                     "amp": {"a": "1ms", "d": "650ms", "s": 0, "r": "80ms", "curve": 3}},
           "play": {"vel_sens": 0.6}}
    SUB = {"about": "Cross Purposes' sub (chirper-three): a sine an octave under the bass, a soft attack, sustained.",
           "synth": {"layers": [{"name": "sub", "wave": "sine"}], "amp": {"a": "8ms", "d": "300ms", "s": 0.7, "r": "60ms"}}}
    sn = dict(type="drum", beater="brush", decay="0.32s", sharp=20, reso=1.45, cavity=0.3, reso_level=0.5, shell=0.3,
              shell_hz=480, wires=0.5, gap=0.25, wire_tone="5.5k", strike=0.35, damp=0.3, slap=0.7, stereo=0.4)

    def piece(pitch, layer, amp, gain="0dB", filters=("hp cutoff=90",)):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": list(filters), "amp": amp},
                                                          "play": {"vel_sens": 0.7}}}
    BRUSHES = {"about": "Borrowed from chirper-two's t4 brush kit (Odd Hours): physical-layer brush taps (bt), sweeps "
                        "(bs, bsl) and a feathered felt kick (k), over room-kit.",
               "extends": "room-kit",
               "kit": {"bt": piece("E3", sn, {"a": "0.5ms", "d": "700ms", "s": 0, "r": "60ms", "curve": 2}),
                       "bs": piece("E3", dict(sn, sweep="0.55s"), {"a": "20ms", "d": "900ms", "s": 0, "r": "80ms", "curve": 1}, "-3dB"),
                       "bsl": piece("E3", dict(sn, sweep="1.2s"), {"a": "40ms", "d": "1.6s", "s": 0, "r": "120ms", "curve": 1}, "-3dB"),
                       "k": piece("G1", dict(type="drum", beater="felt", decay="0.5s", sharp=40, reso=1.0, cavity=0.25,
                                             reso_level=0.6, air=0.4, strike=0.25, damp=0.3, slap=0.3, stereo=0.2),
                                  {"a": "0.5ms", "d": "600ms", "s": 0, "r": "40ms", "curve": 2}, "6dB", ("hp cutoff=45",))}}
    TTOMS = {"about": "Cross Purposes' tuned toms (chirper-three): chirper-two's t4 tom choir (physical drum layer, "
                      "tune_sounding) tightened for the black page's sixteenths: crisper stick, half the decay.",
             "synth": {"layers": [{"type": "drum", "beater": "stick", "contact": 1.5, "decay": "0.55s", "sharp": 45,
                                   "reso": 1.0, "cavity": 0.25, "tune_sounding": True, "reso_level": 0.5, "air": 0.45,
                                   "strike": 0.3, "shell": 0.25, "slap": 0.6, "stereo": 0.5}],
                       "filters": ["hp cutoff=60"], "amp": {"a": "0.3ms", "d": "700ms", "s": 0, "r": "80ms", "curve": 3}},
             "play": {"vel_sens": 0.6}}
    tr = lambda name, patch, **kw: dict({"name": name, "patch": patch, "score": P[name].score(total)}, **kw)
    tracks = [
        tr("mar", "c3-marimba", pan="L40", gain="-4dB", sends={"room": "-10dB"}),
        tr("lead", "lead-wah", pan="L15", gain="-3dB", sends={"room": "-12dB"}),        # the Zappa solo
        tr("choir", "mellotron-choir", gain="-4dB", sends={"room": "-8dB"}),            # the opening chorale
        tr("mar2", "c3-marimba", pan="R45", gain="-6dB", sends={"room": "-10dB"}),     # the answer's phasing marimba
        tr("flute", "mellotron-flute", pan="R40", gain="-6dB", sends={"room": "-10dB"}),
        tr("tpt", "trumpet-mute", pan="L20", gain="-5dB", sends={"room": "-12dB"}),
        tr("sax", "tenor-sax-synth", pan="R20", gain="-5dB", sends={"room": "-12dB"}),
        tr("gtr", "starcaster-clean", pan="L60", gain="-6dB", sends={"room": "-12dB"}),
        tr("keys", "wurli", pan="R60", gain="-7dB", sends={"room": "-12dB"}),
        tr("rhodes", "rhodes-rotary", pan="R35", gain="-6dB", sends={"room": "-10dB"},      # the trio's comp: wM's amp,
           fx=[{"type": "amp", "model": "clean", "stack": "bassman", "gain": 0.35, "mix": 0.6}]),  # chirper-one's recipe
        tr("bass", "bass-di", gain="-3dB"),
        tr("sub", "c3-sub", gain="-9dB"),                                   # the sub floor under the loud sections
        tr("clock", "toy-piano", pan="R15", gain="-4dB", sends={"room": "-14dB"}),   # the CLOCK, every 5 sixteenths
        tr("kick", "prog-kit", out="drums"),
        tr("snare", "prog-kit", out="drums"),
        tr("hat", "prog-kit", out="drums", gain="-4dB"),
        tr("toms", "prog-kit", out="drums"),
        tr("ttom", "c3-ttoms", pan="L10", gain="2dB", sends={"room": "-12dB"}),    # the black page's tuned toms
        tr("ride", "modal-ride", out="drums", gain="-8dB"),
        tr("brush", "c3-brushes", out="drums", gain="-20dB"),          # chirper-two's brushes: the sweeps
        tr("tap", "c3-brushes", out="drums", gain="-14dB"),            # taps and the feathered kick
    ]
    head = [
        'about: "Chirpers - Odd Hours, track 7: Cross Purposes (chirper-three). Gentle Giant / Zappa counterpoint: a nine-note subject over 7/8 + 5/8, hocketed, fugued, black-paged, set at cross purposes (7 against 4), traded and stretto\'d. Generated by compose/chirpers2/src/chirpers2-t7.py."',
        f"tempo: {BPM}",
        'tail: "2s"',
        'ceiling: "-0.3dB"',
        "patches: " + json.dumps({"c3-marimba": MAR, "c3-sub": SUB, "c3-brushes": BRUSHES, "c3-ttoms": TTOMS}),
        "buses:",
        '  room: {fx: ["reverb kind=room decay=1.1s mix=1 predelay=12ms mono_below=150hz"]}',
        '  drums: {fx: [{"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "12ms", "release": "100ms", "makeup": "2dB"}, "reverb kind=room decay=0.8s mix=0.12 predelay=8ms mono_below=200hz"]}',
        'master: ' + json.dumps({"fx": ["glue threshold=-20dB ratio=2 attack=15ms release=200ms makeup=2dB",
                                       # the dynamic arc AFTER the glue (so it is not squashed back): the trades hush
                                       {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                       {"type": "gain", "gain": "6dB"}],
                                "auto": {"dyn": {"points": dyn_lane()}}}),
        "tracks:",
    ]
    with open(OUT, "w") as f:
        f.write("\n".join(head) + "\n")
        for d in tracks:
            f.write("  - " + json.dumps(d) + "\n")
    secs = total / 2 * 60 / BPM
    print(f"wrote {OUT}: {len(BARS)} bars, {total:.1f} eighths, {secs:.0f} s")


if __name__ == "__main__":
    main()
