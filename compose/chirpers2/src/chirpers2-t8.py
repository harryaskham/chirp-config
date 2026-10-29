#!/usr/bin/env python3
"""chirpers2-t8 (Odd Hours, track 8). Composed by chirper-two: MALLET CHAMBER IN PHASE.

A kit-less vibes-and-marimba quartet: process music meets chamber jazz.
- CELL: one 12-eighth figure on two marimbas, written as scale degrees over the chord (in Eb lydian:
  Eb4 Bb4 F5 Bb4 G4 Bb4 | C5 Bb4 F4 Bb4 G4 D5). Marimba 2 plays the same cell, PHASED: it steps one eighth ahead
  every four bars, and the fourth bar of each step blurs half an eighth ahead (a sixteenth off the grid), so the two
  parts slide out of unison through every offset. After twelve steps the process comes back to unison.
- 12/8 AGAINST 4/4: the marimbas and the frame drum feel the bar in four dotted quarters; the bowed bass walks half
  notes in 4/4 (an 8-beat cycle against the 6-beat bar, realigning every four bars, where the chord changes).
- VIBES (motor tremolo): a long melody whose every four-bar phrase is a PALINDROME (pitches and durations read the
  same backwards: Palindrome for Brushes and Toms' idea, t4), sung over the phasing.
- HARMONY moves slowly, four bars a chord: Ebmaj7#11 | Cm9 | Abmaj9 | Bb13sus (one diatonic collection, the A of
  Eb lydian turning to Ab); the bridge goes up a minor third (Gbmaj7#11 | Ebm9 | Bmaj9 | Db13sus) and inverts the cell.
- FORM (seven sections): cell / phase / melody / bridge / peak / unison / coda.
The frame drum is chirp's physical membrane (`type: drum`, one head, felt and brush): dum, tek and sweeps.

Emits songs/chirpers2-t8.yaml. Edit the music here.
"""
import json
import os

OUT = os.environ.get("T8_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers2-t8.yaml")
BPM = 112
# Round 2 (v2): D = dynamics (the bridge drops away: soft marimbas, no sub; the peak grows: the phasing marimba in
# octaves, sixteenth fills on the frame drum); A = the bowed bass takes the CELL in augmentation (dotted quarters)
# through the bridge, a counter-line; S = SUBJECT answered: in the bridge's second half the borrowed marimba sings
# its first song's tune, t7 Cross Purposes' SUBJECT (chirper-three; exactly one 12/8 bar), then its inversion.
R2 = set(filter(None, os.environ.get("T8_R2", "D,A,S").split(","))) - {"none"}
# Round 3 (v3): V = a VIBES SOLO, a new 8-bar section after the melody (chords every two bars; the high marimba
# rests and the low one keeps the cell; sixteenth runs, dotted-eighth groups and triplet falls; the frame drum ghosts
# dotted eighths, eight against the bar's four dotted quarters); T = the peak's melody in THIRDS (four mallets);
# E = the coda's vibes ECHOED a dotted eighth later (t9 Slow Shutter's dotted-eighth clock, at the t8/t9 seam).
# R = the vibes kept in a real vibraphone's range, F3..F6 (v1-v2 climbed to D7 on the Abmaj9 phrases)
R3 = set(filter(None, os.environ.get("T8_R3", "V,T,E,R").split(","))) - {"none"}


def vr(m):
    """A vibes note: folded into F3..F6 when R is on."""
    if "R" in R3:
        while m > 89:
            m -= 12
        while m < 53:
            m += 12
    return m
# Round 4 (v4): B = a BLUR BREAK after the bridge: the two marimbas alone for four bars, the high one stuck a THIRD
# of an eighth behind (the phase caught between steps: neither unison nor the next offset), Eb lydian to Bb13sus;
# Q = the peak's frame drum plays FIVE against the bar's four dotted quarters (teks 1.2 beats apart).
R4 = set(filter(None, os.environ.get("T8_R4", "B,Q").split(","))) - {"none"}
# Round 5 (v5): H = the PEAK REHARMONISED up a cycle of major thirds, Ebmaj7#11 | Gmaj7#11 | Bmaj7#11 | Bb13sus
# (the cell and the palindromes ride the new chords; the lift of the climax); G = the coda's echo GROWS, a dotted
# eighth behind at first and a dotted quarter by the end: the phasing process reaches the melody itself.
R5 = set(filter(None, os.environ.get("T8_R5", "H,G").split(","))) - {"none"}
PEAK = [(63, "maj7#11"), (67, "maj7#11"), (59, "maj7#11"), (58, "13sus")]  # Eb4, G4, B3, Bb3
# Round 6 (v6): X = TRADES after the vibes solo: 8 bars, the vibes and the LOW MARIMBA trading two-bar phrases
# (chords every two bars). In the marimba's bars the high marimba keeps the cell half a bar out of phase and the
# low one solos: a quintuplet run up, dotted eighths down, a roll on a colour tone.
R6 = set(filter(None, os.environ.get("T8_R6", "X").split(","))) - {"none"}
# Round 7 (v7): M = the melody section's second half REHARMONISED, a chord a bar: a chromatic descent Abmaj9 | Gm9 |
# Gbmaj7#11 | Fm9 (the third phrase; the fourth keeps Bb13sus: a turnaround there unsettled the form on some seeds);
# the vibes' palindrome takes each note's own bar's chord, so one mirror is heard over moving harmony.
R7 = set(filter(None, os.environ.get("T8_R7", "M").split(","))) - {"none"}
REHARM = [(68, "maj9"), (67, "m9"), (66, "maj7#11"), (65, "m9"), (58, "13sus"), (58, "7alt"), (60, "m9"), (58, "7alt")]
# Round 8 (v8): S = the bowed bass SINGS in the bridge's second half: a palindromic melody in its upper register
# (half up, half back, on the bridge's chords), a counter-melody to the marimba's t7 subject, the sub holding the
# root; 5 = the vibes solo's runs in QUINTUPLETS (ten notes over two beats).
R8 = set(filter(None, os.environ.get("T8_R8", "S,5").split(","))) - {"none"}
# Round 9 (v9): C = the opening PHASE section COMPRESSED to 12 bars (a step every three bars, the third a blur), so
# the process gets going sooner; U = a TUTTI on the peak's last bar: vibes, both marimbas, bowed bass and frame drum
# play the cell together in rhythmic unison, the arrival before the return to unison.
R9 = set(filter(None, os.environ.get("T8_R9", "C,U").split(","))) - {"none"}
# Round 10 (v10): D = a DUET before the peak (4 bars, after the marimbas' blur): the vibes and the bowed bass alone,
# the vibes singing a palindrome over Cm9 -> Bb13sus and the bass answering note against note in CONTRARY MOTION;
# marimbas alone, then vibes and bass alone, then everyone.
R10 = set(filter(None, os.environ.get("T8_R10", "D").split(","))) - {"none"}
# Round 11 (v11): M = a BASS MARIMBA (song-local: wooden-bar partials 1 / 4, a 1.3 s ring, no low cut): the cell's
# dotted-quarter notes two octaves under the high marimba through the phase, melody, solo, trades and peak, and the
# whole cell in the unison: three marimbas, the process given a floor.
R11 = set(filter(None, os.environ.get("T8_R11", "M").split(","))) - {"none"}
# Round 12 (v12): 3 = THREE-WAY TRADES: the trades' last turn goes to the BASS MARIMBA (vibes, low marimba, vibes,
# bass marimba): a triplet arpeggio up and dotted quarters down, then triplet quarters falling to a held root, the
# low marimba back on the cell beneath it.
R12 = set(filter(None, os.environ.get("T8_R12", "3").split(","))) - {"none"}
# Round 13 (v13), answering the answers: K = t7 Cross Purposes' CLOCK (chirper-three, whose coda now phases this
# track's cell): in the unison, the t7 SUBJECT's pitches two octaves up on a toy piano, one every five sixteenths,
# turning across the 12/8; S = t9 Slow Shutter's SHUTTER (chirper-zero, whose dawn borrows these vibes): in the coda
# the frame drum plays its 3+3+3+2 grouping over the last two bars, an 11-eighth cycle against the 12-eighth bar
# (over the whole coda it blurred the pulse: rhythm -2).
R13 = set(filter(None, os.environ.get("T8_R13", "K").split(","))) - {"none"}  # S tried: on-grid strokes, rhythm -2
# Round 14 (v14): I = the opening ASSEMBLED FROM THE FLOOR: the bass marimba plays the cell's dotted-quarter
# skeleton alone for a bar, then the low marimba's cell joins it (and the frame drum after); F = the coda ends on the
# bass marimba's low Eb, ringing under the vibes' last echo.
R14 = set(filter(None, os.environ.get("T8_R14", "I,F").split(","))) - {"none"}
# Round 15 (v15): G = TRUE PHASING at the peak: instead of stepping an eighth every four bars, the high marimba
# DRIFTS a quarter of an eighth every bar (offsets 8, 8.25, 8.5 ... 11.75, arriving at 12 = unison), the gradual
# phase the discrete steps imitated, at the climax.
R15 = set(filter(None, os.environ.get("T8_R15", "G").split(","))) - {"none"}
# Round 16 (v16): R = a ROLLED MARIMBA CHORALE (4 bars between the unison and the coda): the home chords as
# marimba rolls (each hand a two-note roll in alternating 32nds, swelling and dying away through the bar), the bass
# marimba ringing the roots and the bow beneath: the instrument's own lyric voice, after the process ends.
R16 = set(filter(None, os.environ.get("T8_R16", "R").split(","))) - {"none"}
# Round 17 (v17): Q = FOUR AGAINST THREE: in the melody, the solo and the trades the frame drum's ghosts become
# QUADRUPLETS, sixteen even strokes across the 12/8 bar (a straight 4/4 sixteenth feel laid over the marimbas'
# triple eighths), accented every fourth.
R17 = set(filter(None, os.environ.get("T8_R17", "Q").split(","))) - {"none"}
# Round 18 (v18): S7 = t1 Doors at Seven's SEVEN DOORS head (chirper-zero; quoted by t4 and t10 too) on the vibes
# in the bridge's first half: its opening two bars as scale degrees, set in 12/8 (C. Bb G F | Eb. F. | G Bb C D.
# Eb~~), on the bridge's chords, then a held colour tone; the album's front door heard through the mallets.
R18 = set(filter(None, os.environ.get("T8_R18", "S7").split(","))) - {"none"}
DOORS = [[(0, 3), (-1, 1), (-3, 1), (-4, 1), (-5, 3), (-4, 3)], [(-3, 1), (-1, 1), (0, 1), (1, 3), (2, 6)]]
# Round 19 (v19): G = t3 Glass Arithmetic's GLASS TUNE answered back (chirper-one, whose v9 runs this track's cell
# through its 3+2 breakdown): in the phase section's second half the vibes enter softly with it, chord-tone indices
# 0 2 4 3 1 4 2 0 in dotted eighths (eight to the 12/8 bar, exactly), over the stepping marimbas.
R19 = set(filter(None, os.environ.get("T8_R19", "G").split(","))) - {"none"}
GLASS = [0, 2, 4, 3, 1, 4, 2, 0]
SUBJECT = [(0, 1), (3, 1), (7, 1), (6, 2), (2, 2), (5, 1), (1, 1), (4, 1), (0, 2)]  # t7: semitones, eighths
BAR = 6.0  # a 12/8 bar, in quarter beats

NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


SCALES = {"maj7#11": [0, 2, 4, 6, 7, 9, 11], "m9": [0, 2, 3, 5, 7, 9, 10], "maj9": [0, 2, 4, 5, 7, 9, 11],
          "13sus": [0, 2, 4, 5, 7, 9, 10], "7alt": [0, 1, 3, 4, 6, 8, 10]}
HOME = [(63, "maj7#11"), (60, "m9"), (68, "maj9"), (58, "13sus")]     # Eb4, C4, Ab4, Bb3
BRIDGE = [(66, "maj7#11"), (63, "m9"), (59, "maj9"), (61, "13sus")]   # Gb4, Eb4, B3, Db4


def deg(chord, d):
    root, kind = chord
    sc = SCALES[kind]
    return root + 12 * (d // 7) + sc[d % 7]


CELL = [0, 4, 8, 4, 2, 4, 5, 4, 1, 4, 2, 6]
CELL_INV = [8 - d for d in CELL]  # the bridge's cell: the same figure upside down

# Vibes half-phrases: (degree above the chord's root an octave up, eighths); each sums to 24 and is mirrored.
HALVES = [
    [(4, 6), (5, 3), (6, 3), (8, 4), (9, 2), (7, 6)],
    [(2, 4), (4, 2), (7, 6), (6, 3), (4, 3), (5, 6)],
    [(9, 6), (8, 2), (6, 4), (4, 3), (5, 3), (1, 6)],
    [(0, 3), (2, 3), (4, 6), (7, 4), (11, 2), (9, 6)],
]


def palindrome(half):
    """half + its retrograde; the centre note (end of half, start of the mirror) is one held note."""
    back = list(reversed(half))
    return half[:-1] + [(half[-1][0], half[-1][1] * 2)] + back[1:]


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel):
        self.ev.append((round(at, 4), max(0.05, round(ln, 4)), head, int(max(1, min(127, vel)))))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if e[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


FORM = [("cell", 4), ("phase", 12 if "C" in R9 else 16), ("melody", 16)] + ([("solo", 8)] if "V" in R3 else []) + \
       ([("trades", 8)] if "X" in R6 else []) + \
       [("bridge", 16)] + ([("blur", 4)] if "B" in R4 else []) + ([("duet", 4)] if "D" in R10 else []) + [("peak", 16), ("unison", 8)] + ([("chorale", 4)] if "R" in R16 else []) + [("coda", 6)]
LEVEL = {"cell": 70, "phase": 76, "melody": 82, "bridge": 74, "peak": 96, "unison": 80, "coda": 60, "solo": 84,
         "blur": 76, "trades": 86, "duet": 70, "chorale": 66}
if "D" in R2:
    LEVEL.update({"bridge": 62, "peak": 104, "unison": 76})


def build():
    T = {k: Track(k) for k in ("m1", "m2", "vib", "echo", "bass", "sub", "fd", "bm", "clock")}
    import random
    rng = random.Random(8)
    bars, b = [], 0
    for name, n in FORM:
        for i in range(n):
            bars.append((b * BAR, name, i, n))
            b += 1
    total = len(bars) * BAR
    step = 0  # marimba 2's phase offset in eighths; it climbs 0..11 over phase, melody and peak
    for bi, (start, sec, i, n) in enumerate(bars):
        v = LEVEL[sec]
        prog = BRIDGE if sec == "bridge" else (PEAK if sec == "peak" and "H" in R5 else HOME)
        chord = prog[(i // 4) % 4] if sec not in ("cell", "coda") else HOME[0]
        if sec in ("solo", "trades"):
            chord = HOME[(i // 2) % 4]
        if sec == "melody" and "M" in R7 and 8 <= i < 12:
            chord = REHARM[i - 8]
        bmsolo = "3" in R12 and "M" in R11 and sec == "trades" and i >= 6  # the bass marimba's turn
        mar = sec == "trades" and (i // 2) % 2 == 1 and not bmsolo  # the low marimba's turn
        if bmsolo:
            if i == 6:
                arp = [0, 2, 4, 6, 7, 9]
                for s, dg in enumerate(arp):  # a triplet arpeggio up
                    T["bm"].add(start + s / 3, 0.32, nm(deg(chord, dg) - 24 + 12), v - 6 + 2 * s)
                for q, dg in enumerate([8, 6, 4]):  # dotted quarters down
                    T["bm"].add(start + 2 + q * 1.5, 1.4, nm(deg(chord, dg) - 24 + 12), v - 2 - 2 * q)
            else:
                for s, dg in enumerate([7, 6, 4, 3, 2, 1]):  # triplet quarters falling
                    T["bm"].add(start + s * 2 / 3, 0.62, nm(deg(chord, dg) - 24 + 12), v - 4 - s)
                T["bm"].add(start + 4, 1.9, nm(deg(chord, 0) - 24 + 12), v)
        if sec == "blur":
            chord = HOME[0] if i < 2 else HOME[3]
        if sec == "chorale":
            chord = HOME[i % 4]
            for tr, degs, base in (("m1", (0, 4), -12), ("m2", (2, 6), 0)):
                p1, p2 = (deg(chord, d) + base for d in degs)
                for r in range(40):  # 32nds for five beats, alternating the two notes, swelling then dying
                    sw = 1 - abs(r - 20) / 20
                    T[tr].add(start + r * 0.125, 0.12, nm(p1 if r % 2 == 0 else p2), int(v - 24 + 22 * sw))
            if "M" in R11:
                bp = deg(chord, 0) - 24
                while bp < 33:
                    bp += 12
                T["bm"].add(start, BAR * 0.9, nm(bp), v - 2)
            broot = chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12
            T["bass"].add(start, BAR * 0.97, nm(broot), v - 8)
            continue
        if sec == "duet":
            chord = HOME[1] if i < 2 else HOME[3]
            if i == 0:  # the duet: one palindrome, the bass in contrary motion beneath it
                at = start
                for d, ln in palindrome(HALVES[3]):
                    ch = HOME[1] if at - start < 2 * BAR else HOME[3]
                    T["vib"].add(at, ln / 2 * 0.98, nm(vr(deg(ch, d) + 12)), v + 2)
                    broot = ch[0] - 24 if ch[0] - 24 >= 28 else ch[0] - 12
                    T["bass"].add(at, ln / 2 * 0.97, nm(deg((broot, ch[1]), max(0, 9 - d))), v - 2)
                    at += ln / 2
            if i % 2 == 0:
                T["fd"].add(start, 2 * BAR * 0.9, "sw", v - 18)
                T["sub"].add(start, 2 * BAR * 0.95, nm((chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12) - 12), v - 10)
            continue
        if sec == "coda":
            chord = HOME[i // 2 % 2 * 0]  # the coda rests on the home chord
        cell = CELL_INV if sec == "bridge" else CELL
        # ---- the marimbas ----
        if sec == "cell" and "I" in R14 and "M" in R11:  # the floor first
            for e in range(0, 12, 3):
                bp = deg(chord, cell[e]) - 24
                while bp > 52:
                    bp -= 12
                while bp < 33:
                    bp += 12
                T["bm"].add(start + e / 2, 1.4, nm(bp), v - 2 + (6 if e == 0 else 0))
        if sec == "cell" and "I" in R14 and i == 0:
            pass  # the low marimba waits a bar
        elif mar:  # the low marimba solos
            if i % 2 == 0:
                d0 = rng.choice([0, 1, 2])
                for s in range(10):  # a quintuplet run up over two beats
                    T["m1"].add(start + s * 0.2, 0.19, nm(deg(chord, d0 + s) - 12), v - 8 + s)
                for g in range(4):
                    T["m1"].add(start + 2 + g * 0.75, 0.7, nm(deg(chord, d0 + 9 - 2 * g) - 12), v - 2 - 2 * g)
            else:
                tone = deg(chord, rng.choice([4, 6])) - 12
                for r in range(16):  # a roll: 32nds for two beats, swelling
                    T["m1"].add(start + r * 0.125, 0.12, nm(tone), v - 20 + r)
                for q in range(4):
                    T["m1"].add(start + 2 + q * 0.5 + (0.5 if q >= 2 else 0), 0.45, nm(deg(chord, [4, 2, 1, 0][q]) - 12), v - 4)
            for e in range(12):  # the high marimba keeps the cell, half a bar out
                T["m2"].add(start + ((e + 6) % 12) / 2, 0.45, nm(deg(chord, cell[e])), v - 16 + (6 if e % 3 == 0 else 0))
        elif sec != "coda":
            for e in range(12):
                acc = 10 if e % 3 == 0 else 0
                T["m1"].add(start + e / 2, 0.45, nm(deg(chord, cell[e]) - 12), v - 8 + acc)  # the low marimba
        if sec in ("phase", "melody", "peak"):
            span = 3 if sec == "phase" and "C" in R9 else 4
            k = {"phase": 0, "melody": 4, "peak": 8}[sec] + i // span
            off = k + (0.5 if i % span == span - 1 else 0.0)  # the blur bar: half an eighth on toward the next step
            if sec == "peak" and "G" in R15:
                off = 8 + i * 0.25  # the drift
            for e in range(12):
                at = start + ((e + off) % 12) / 2
                p2 = deg(chord, cell[e])
                head = nm(p2) + ("," + nm(p2 - 12) if sec == "peak" and "D" in R2 else "")  # octaves at the peak (below)
                T["m2"].add(at, 0.45, head, v - 12 + (8 if e % 3 == 0 else 0))
        elif sec == "unison" or (sec == "bridge" and i < 8):
            for e in range(12):
                T["m2"].add(start + e / 2, 0.45, nm(deg(chord, cell[e]) + (0 if sec == "unison" else 12)), v - 14)
        elif sec == "bridge" and "S" in R2:  # t7's SUBJECT on the bar's chord root, then its inversion
            sign = 1 if i % 2 == 0 else -1
            at = start
            for semi, ln in SUBJECT:
                T["m2"].add(at, ln / 2 * 0.9, nm(chord[0] + 12 + sign * semi), v - 4)
                at += ln / 2
        elif sec == "bridge":  # canon at half a bar, a third above
            for e in range(12):
                T["m2"].add(start + ((e + 6) % 12) / 2, 0.45, nm(deg(chord, cell[e] + 2)), v - 12)
        elif sec == "blur":  # stuck a third of an eighth behind
            for e in range(12):
                T["m2"].add(start + (e + 1 / 3) / 2, 0.45, nm(deg(chord, cell[e])), v - 6 + (8 if e % 3 == 0 else 0))
        if "M" in R11 and sec in ("phase", "melody", "solo", "trades", "peak", "unison") and not mar and not bmsolo:
            for e in range(12):
                if sec == "unison" or e % 3 == 0:
                    bp = deg(chord, cell[e]) - 24
                    while bp > 52:
                        bp -= 12
                    while bp < 33:
                        bp += 12
                    T["bm"].add(start + e / 2, 1.4 if e % 3 == 0 else 0.45, nm(bp), v - 6 + (6 if e % 6 == 0 else 0))
        if sec == "phase" and "G" in R19 and i >= n // 2:  # the glass tune, answered
            for g, ix in enumerate(GLASS):
                T["vib"].add(start + g * 0.75, 0.7, nm(vr(deg(chord, 2 * ix) + 12)), v - 14 + (6 if g % 4 == 0 else 0) + 2 * (i - n // 2))
        # ---- the vibes ----
        if sec in ("melody", "peak", "unison") and i % 4 == 0:
            half = HALVES[(i // 4 + (2 if sec == "peak" else 0)) % 4]
            phrase = palindrome(half)
            at, mid = start, len(phrase) // 2
            ph_chord = chord
            for j, (d, ln) in enumerate(phrase):
                if sec == "melody" and "M" in R7 and i == 8:  # each note takes its own bar's chord
                    chord = REHARM[min(3, int((at - start) // BAR))]
                swell = 12 - 4 * abs(j - mid)  # dynamics mirror too: up to the centre, back down
                head = nm(vr(deg(chord, d) + 12))
                if sec == "peak" and "T" in R3:  # four mallets: a diatonic third under the line
                    head += "," + nm(vr(deg(chord, d - 2) + 12))
                T["vib"].add(at, ln / 2 * 0.98, head, v - 4 + swell)
                at += ln / 2
            chord = ph_chord
        elif sec == "bridge" and i < 8 and "S7" in R18:  # SEVEN DOORS, then a held colour tone
            if i % 4 < 2:
                at = start
                for d, ln in DOORS[i % 4]:
                    T["vib"].add(at, ln / 2 * 0.95, nm(vr(deg(chord, d + 7) + 12)), v + 2)
                    at += ln / 2
            elif i % 4 == 2:
                T["vib"].add(start, 2 * BAR * 0.95, nm(vr(deg(chord, 6) + 12)), v - 6)
        elif sec == "bridge" and i % 4 == 0:
            for j, d in enumerate([4, 6, 9, 8, 8, 9, 6, 4]):
                T["vib"].add(start + j * 3, 2.9, nm(vr(deg(chord, d) + 12)), v - 10 + (6 if j in (3, 4) else 0))
        elif sec in ("solo", "trades") and not mar and not bmsolo:  # the vibes solo (and the vibes' bars of the trades): a run, dotted-eighth groups, a triplet fall, a held note
            if i % 2 == 0:
                d0 = rng.choice([0, 2, 4])
                if "5" in R8:
                    for s in range(10):  # a quintuplet run up: ten notes over two beats
                        T["vib"].add(start + s * 0.2, 0.19, nm(vr(deg(chord, d0 + s))), v - 10 + s * 2)
                else:
                    for s in range(8):  # a sixteenth run up
                        T["vib"].add(start + s * 0.25, 0.24, nm(vr(deg(chord, d0 + s))), v - 10 + s * 2)
                top = d0 + 8
                for g in range(4):  # dotted-eighth groups, stepping down by thirds
                    T["vib"].add(start + 2 + g * 0.75, 0.7, nm(vr(deg(chord, top - 2 * g))), v - 2 - g * 2)
            else:
                d1 = rng.choice([7, 8, 9])
                for s in range(6):  # a triplet fall
                    T["vib"].add(start + s / 3, 0.32, nm(vr(deg(chord, d1 - s))), v - 4 - s)
                T["vib"].add(start + 2, 2.9, nm(vr(deg(chord, rng.choice([2, 4, 6])))), v - 2)
                T["vib"].add(start + 5, 0.45, nm(vr(deg(chord, 4))), v - 12)
                T["vib"].add(start + 5.5, 0.45, nm(vr(deg(chord, 5))), v - 10)
        elif sec == "coda" and i == 0:  # one mirror, slowed by a quarter: five bars of the six
            phrase = palindrome(HALVES[0][:3] + [(9, 6)])  # a short mirror, slowing
            at = start
            for j, (d, ln) in enumerate(phrase):
                T["vib"].add(at, ln / 2 * 1.2, nm(vr(deg(HOME[0], d) + 12)), v)
                if "E" in R3:  # the echo, a dotted eighth behind (t9's clock); with G it drifts to a dotted quarter
                    lag = 0.75 + (0.75 * j / max(1, len(phrase) - 1) if "G" in R5 else 0)
                    T["echo"].add(at + lag, ln / 2 * 1.1, nm(vr(deg(HOME[0], d) + 12)), v - 14 + (4 if "G" in R5 else 0))
                at += ln / 2 * 1.25
        # ---- the bowed bass: half notes in 4/4 against the 12/8 ----
        if sec in ("phase", "melody", "peak", "unison", "solo", "trades") and not (sec == "phase" and i < 4):
            for h in range(3):
                beat = start + 2 * h
                cyc = int(round(beat / 2)) % 4  # position in the 8-beat (4/4 bar) cycle
                d = [0, 4, 1, 2][cyc] if (i % 4) < 3 else [0, 6, 5, 4][cyc]
                note = deg((chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12, chord[1]), d)
                acc = 10 if cyc == 0 else 0
                head = nm(note) + ("," + nm(note + 12) if sec == "peak" and cyc == 0 else "")
                T["bass"].add(beat, 1.95, head, v - 10 + acc)
                if cyc in (0, 2):  # the sub: the 4/4 bar's strong beats an octave under the bow
                    T["sub"].add(beat, 1.9, nm(note - 12 if note - 12 >= 24 else note), v - 8 + acc)
        elif sec == "bridge" and "S" in R8 and i >= 8:  # the bass sings: a 4-bar palindrome, high in its range
            root = chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12
            if i % 4 == 0:
                half = [(4, 6), (6, 3), (7, 3), (9, 6), (8, 6)]  # 24 eighths
                at = start
                for d, ln in palindrome(half):
                    T["bass"].add(at, ln / 2 * 0.97, nm(deg((root + 12, chord[1]), d)), v + 4)
                    at += ln / 2
            T["sub"].add(start, BAR * 0.95, nm(root - 12 if root - 12 >= 24 else root), v - 4)  # the floor, firmer
        elif sec == "bridge" and "A" in R2:  # the cell in augmentation: dotted quarters, three bars a statement
            root = chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12
            if i % 4 < 3:
                for q in range(4):
                    d = CELL_INV[(i % 4) * 4 + q]
                    bn = deg((root, chord[1]), d)
                    T["bass"].add(start + q * 1.5, 1.45, nm(bn), v + (6 if q == 0 else 0))
                    if q == 0:
                        T["sub"].add(start, BAR * 0.95, nm(root - 12 if root - 12 >= 24 else root), v - 12)
            else:
                T["bass"].add(start, BAR * 0.98, nm(root), v - 2)
        elif sec == "bridge":
            root = chord[0] - 24 if chord[0] - 24 >= 28 else chord[0] - 12
            bn = root if i % 2 == 0 else deg((root, chord[1]), 4)
            T["bass"].add(start, BAR * 0.98, nm(bn), v - 6)
            T["sub"].add(start, BAR * 0.95, nm(bn - 12 if bn - 12 >= 24 else bn), v - 10)
        elif sec == "coda" and i < 4:
            T["bass"].add(start, BAR * 0.98, nm(HOME[0][0] - 24), v - 14)
        # ---- the frame drum ----
        fd = T["fd"]
        if sec == "cell" and i >= 2:
            fd.add(start, 1, "dum", v - 14)
        elif sec in ("solo", "trades"):  # dotted-eighth ghosts: eight against the four dotted quarters
            fd.add(start, 1, "dum", v - 8)
            fd.add(start + 3, 1, "dum", v - 14)
            if "Q" in R17:
                for q in range(16):
                    fd.add(start + q * 0.375 + (0.01 if q in (0, 8) else 0), 0.2, "tek" if q % 4 == 0 else "gh",
                           v - (14 if q % 4 == 0 else 26))
            else:
                for g in range(8):
                    fd.add(start + g * 0.75 + (0.01 if g in (0, 4) else 0), 0.25, "tek" if g % 2 == 0 else "gh",
                           v - (14 if g % 2 == 0 else 24))
        elif sec in ("phase", "melody", "unison"):
            fd.add(start, 1, "dum", v - 6)
            fd.add(start + 3, 1, "dum", v - 12)
            fd.add(start + 1.5, 0.5, "tek", v - 12)
            fd.add(start + 4.5, 0.5, "tek", v - 10)
            if sec == "melody" and "Q" in R17:
                for q in range(16):
                    if q % 4:
                        fd.add(start + q * 0.375, 0.2, "gh", v - 30 + (4 if q % 2 == 0 else 0))
            elif sec == "melody":
                for e in (2, 5, 8, 11):
                    fd.add(start + e / 2, 0.3, "gh", v - 30)
        elif sec == "bridge":
            fd.add(start, 3, "sw", v - 10)
            fd.add(start + 3, 3, "sw", v - 16)
        elif sec == "peak":
            fd.add(start, 1, "dum", v - 2)
            fd.add(start + 3, 1, "dum", v - 8)
            if "Q" in R4:  # five against four: teks 1.2 beats apart
                for q in range(5):
                    fd.add(start + q * 1.2 + (0.02 if q == 0 else 0), 0.3, "tek", v - 10 + (6 if q == 0 else 0))
            else:
                for e in (3, 9):
                    fd.add(start + e / 2, 0.5, "tek", v - 6)
                for e in (2, 5, 8, 11):
                    fd.add(start + e / 2, 0.25, "gh", v - 26)
            fd.add(start + 4.75, 0.25, "tek", v - 16)  # a sixteenth grace into the third dotted quarter
            if i % 4 == 3:
                if "D" in R2:  # a sixteenth fill into the next phrase
                    for s16 in range(8):
                        fd.add(start + 4 + s16 * 0.25, 0.25, "tek" if s16 % 2 == 0 else "gh", v - 16 + s16 * 2)
                else:
                    fd.add(start + 5, 1, "sw", v - 12)
        elif sec == "coda" and i == 0:
            fd.add(start, 6, "sw", v - 18)
    if "F" in R14 and "M" in R11:  # the last floor: a low Eb under the final echo
        last = [bb for bb in bars if bb[1] == "coda"][-1]
        T["bm"].add(last[0] + 1.5, BAR * 0.9, nm(HOME[0][0] - 24), LEVEL["coda"] + 6)
    if "K" in R13:  # t7's clock through the unison
        un = [bb for bb in bars if bb[1] == "unison"]
        s0, s1 = un[0][0], un[-1][0] + BAR
        k, at = 0, s0
        while at < s1 - 1e-6:
            semi = SUBJECT[k % len(SUBJECT)][0]
            T["clock"].add(at, 0.5, nm(HOME[0][0] + 24 + semi), LEVEL["unison"] - 14 + (12 if k % 4 == 0 else 0))
            k += 1
            at += 1.25
    if "S" in R13:  # Slow Shutter's 3+3+3+2 against the coda's twelves
        co = [bb for bb in bars if bb[1] == "coda"]
        s0, s1 = co[-2][0], co[-1][0] + BAR  # the last two bars: the shutter heard as t9 approaches
        e, g = 0, 0
        while s0 + e / 2 < s1 - 1e-6:
            T["fd"].add(s0 + e / 2, 0.3, "dum" if g % 4 == 0 else "tek", LEVEL["coda"] - (6 if g % 4 == 0 else 14) - e // 12)
            e += [3, 3, 3, 2][g % 4]
            g += 1
    if "U" in R9:  # the tutti: the peak's last bar, everyone on the cell
        last = [bb for bb in bars if bb[1] == "peak"][-1]
        start, chord, v = last[0], (PEAK if "H" in R5 else HOME)[3], LEVEL["peak"]
        for e in range(12):
            p0 = deg(chord, CELL[e])
            acc = 12 if e % 3 == 0 else 0
            T["vib"].add(start + e / 2, 0.45, nm(vr(p0 + 12)), v - 8 + acc)
            T["bass"].add(start + e / 2, 0.45, nm(p0 - 24 if p0 - 24 >= 28 else p0 - 12), v - 6 + acc)
            T["fd"].add(start + e / 2, 0.3, "dum" if e % 3 == 0 else "tek", v - 8 + acc)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    marimba = {"about": "Cross Purposes' marimba (chirper-three, Odd Hours t7), borrowed: additive wooden-bar "
                        "partials 1 / 3.93 / 9.2 with a mallet click.",
               "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [3.93, 0.32], [9.2, 0.07]]},
                                    {"name": "click", "type": "noise", "level": {"value": "-70dB", "mod": [{"src": "env.ck", "amount": 40}]}}],
                         "env": {"ck": {"a": "0.2ms", "d": "5ms", "s": 0}}, "filters": ["hp cutoff=120"],
                         "amp": {"a": "1ms", "d": "650ms", "s": 0, "r": "80ms", "curve": 3}},
               "play": {"vel_sens": 0.6}}
    vibes = {"about": "chirper-two's vibraphone for Odd Hours t8: aluminium-bar partials 1 / 4 / 10 (tuned bars), a "
                      "soft yarn-mallet tick, a long ring, and the MOTOR: a 5.2 Hz tremolo on the bar.",
             "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.16], [10.0, 0.025]],
                                   "level": {"value": "0dB", "mod": [{"src": "lfo.motor", "amount": 3}]}},
                                  {"name": "tick", "type": "noise", "level": {"value": "-72dB", "mod": [{"src": "env.tk", "amount": 36}]}}],
                       "env": {"tk": {"a": "0.3ms", "d": "4ms", "s": 0}},
                       "lfo": {"motor": {"wave": "sine", "rate": "5.2hz"}},
                       "filters": ["hp cutoff=150", "lp cutoff=7k"],
                       "amp": {"a": "2ms", "d": "3.2s", "s": 0, "r": "500ms", "curve": 2}},
             "play": {"vel_sens": 0.55}}
    head = dict(type="drum", beater="felt", decay="0.7s", sharp=25, strike=0.2, damp=0.25, slap=0.4, air=0.3,
                stereo=0.3)

    def piece(pitch, layer, amp, gain="0dB"):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [layer], "filters": ["hp cutoff=55"],
                                                                    "amp": amp}, "play": {"vel_sens": 0.7}}}
    frame = {"about": "chirper-two's frame drum for Odd Hours t8: one physical membrane (bd-7d117e), low: a felt "
                      "'dum' in the centre, a 'tek' near the rim, finger ghosts and brush sweeps.",
             "extends": "room-kit",
             "kit": {"dum": piece("E2", dict(head, decay="0.9s"), {"a": "0.5ms", "d": "1.1s", "s": 0, "r": "80ms", "curve": 2}, "8dB"),
                     "tek": piece("A2", dict(head, strike=0.85, sharp=40, contact=0.6, damp=0.45),
                                  {"a": "0.3ms", "d": "300ms", "s": 0, "r": "40ms"}),
                     "gh": piece("A2", dict(head, strike=0.7, damp=0.6, contact=0.5),
                                 {"a": "0.3ms", "d": "150ms", "s": 0, "r": "30ms"}, "-4dB"),
                     "sw": piece("A2", dict(head, beater="brush", sweep="1.4s", strike=0.5),
                                 {"a": "60ms", "d": "1.8s", "s": 0, "r": "200ms", "curve": 1}, "-2dB")}}
    sub = {"about": "chirper-two's sub for Odd Hours t8: a soft sine an octave under the bowed bass (after chirper-three's "
                    "c3-sub in Cross Purposes).",
           "synth": {"layers": [{"name": "sub", "wave": "sine"}], "amp": {"a": "30ms", "d": "400ms", "s": 0.75, "r": "150ms"}}}
    bassmar = {"about": "chirper-two's bass marimba for Odd Hours t8: wide wooden bars, partials 1 / 4 (tuned for the "
                        "low register), a soft yarn mallet, a 1.3 s ring and no low cut: the marimbas' floor.",
               "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.22], [9.8, 0.03]]},
                                    {"name": "click", "type": "noise", "level": {"value": "-74dB", "mod": [{"src": "env.ck", "amount": 34}]}}],
                         "env": {"ck": {"a": "0.3ms", "d": "6ms", "s": 0}}, "filters": ["hp cutoff=32", "lp cutoff=3k"],
                         "amp": {"a": "2ms", "d": "1.3s", "s": 0, "r": "120ms", "curve": 3}},
               "play": {"vel_sens": 0.6}}
    out = {"c3-marimba": marimba, "c2-vibes": vibes, "c2-frame": frame, "c2-sub": sub}
    if "M" in R11:
        out["c2-bass-marimba"] = bassmar
    return out


def main():
    total, bars, sec, T = build()
    hall = "reverb kind=hall decay=2.4s mix=0.22 predelay=20ms"
    tracks = [
        {"name": "marimba-1", "patch": "c3-marimba", "pan": -0.5, "gain": "-3dB", "fx": [hall], "score": T["m1"].score(total)},
        {"name": "marimba-2", "patch": "c3-marimba", "pan": 0.5, "gain": "-4dB", "fx": [hall], "score": T["m2"].score(total)},
        {"name": "vibes", "patch": "c2-vibes", "pan": 0.05, "gain": "0dB", "fx": [hall], "score": T["vib"].score(total)},
        {"name": "bass", "patch": "tagelharpa-bass-bowed", "pan": -0.05, "gain": "1dB", "score": T["bass"].score(total)},
        {"name": "sub", "patch": "c2-sub", "gain": "-4dB", "score": T["sub"].score(total)},
        {"name": "frame", "patch": "c2-frame", "pan": 0.15, "gain": "0dB",
         "fx": ["reverb kind=room decay=1.0s mix=0.15"], "score": T["fd"].score(total)},
    ]
    if "K" in R13:
        tracks.append({"name": "clock", "patch": "toy-piano", "pan": 0.3, "gain": "-6dB", "fx": [hall],
                       "score": T["clock"].score(total)})
    if "M" in R11:
        tracks.insert(2, {"name": "bass-marimba", "patch": "c2-bass-marimba", "pan": -0.2, "gain": "0dB", "fx": [hall],
                          "score": T["bm"].score(total)})
    if "E" in R3:
        tracks.insert(3, {"name": "vibes-echo", "patch": "c2-vibes", "pan": -0.45, "gain": "-3dB", "fx": [hall],
                          "score": T["echo"].score(total)})
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Odd Hours, track 8. Original composition by chirper-two, generated by "
             "compose/chirpers2/src/chirpers2-t8.py. Mallet chamber in phase: two marimbas phase one 12-eighth cell "
             "through all twelve offsets and back to unison; vibes sing palindromic phrases; a bowed bass walks 4/4 "
             f"against the 12/8; a physical frame drum. 112 bpm. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Odd Hours", "title": "Mallet Chamber in Phase",
                               "track": 8, "year": 2026}),
        f"tempo: {BPM}",
        'meter: "12/8"',
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-0.3dB"',
        'volume: "4dB"',
        "patches: " + json.dumps(patches()),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=35", "highshelf cutoff=6000 gain=-1.5dB"]},
                                        "glue threshold=-20dB ratio=1.4 attack=20ms release=250ms makeup=1dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
