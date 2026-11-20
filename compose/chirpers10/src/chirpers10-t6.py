#!/usr/bin/env python3
"""chirpers X (Common Time), track 6 by chirper-zero: CARRYING CAPACITY.

Harry, 16 Nov about 12:33: "make it unique". Three words, so what unique means here is mine to say and his to overrule.

THE IDEA. The other five songs are built from cycles I chose: wheels, clocks, bell rows, sums, stairs. This one has
no riff I wrote. It has ONE RULE and ONE DIAL. The rule is the oldest model of a population: next year's count is
this year's count, times how fast it breeds (the dial, r), times the room that is left:

        x  <-  r * x * (1 - x)

Every half bar the rule is applied once, and the number it gives (between 0 and 1) IS the half bar: how many of its
six places the band strikes, where the accent falls, and how high the accent is (see `cell`). Low numbers are a
single low note or nothing at all; high numbers are a full roll with a stab at the top of the neck.

THE FORM IS THE DIAL, and nothing else. Turned up slowly the rule does what it always does:
  - under 3 it settles: one half bar, the same for ever (a plain shuffle);
  - at 3 it splits: two half bars that alternate; then four; then eight (the riff doubles its own length);
  - past 3.57 it never repeats: the riff is through-composed by the rule, and still plainly the same riff;
  - inside that there are WINDOWS where it locks again, on cycles nobody asked for: five half bars, then three.
    Five and three against a bar of two: the record's odd meters, but here the rule finds them by itself;
  - at 4 it fills the whole range: screams, then nothing at all for a bar or more (a number near 1 is always
    followed by a number near 0, and near 0 the climb back is slow), then the climb. The band does not play in
    those holes; the machine's long 808 boom falls through them;
  - then the dial comes down through four, two, one, to 1, where the population dies out a note at a time.
It is ONE orbit from the first bar to the last: x is never reset, only the dial moves. This is the record's subject
taken sideways once more: long cycles over a steady pulse that line up, except that here nobody set the lengths.

UNLIKE THE OTHER FIVE (chirp-eco measured what they share): they are in straight sixteenths at 100 to 126; this is
in triplets (twelve-eight written as four-four) at 138. They sit on F and C; this is on E, in the eight-note
half-whole scale. They have one kit and a stick; this has a DRUM MACHINE (the engine's `machine` voices, new on this
record). And the tune over the top is not written into the song at all: the track `lead` carries no notes, only the
rule (`gen: logistic`, the engine's own, new on this record), with the dial's settings; the engine works the orbit
out again by itself and the generator checks that the two agree.

v1 is the skeleton: the whole dial, played bare.
"""
import json
import math
import os
import re

OUT = os.environ.get("C10T6_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t6.yaml"))
BPM = 138
E1 = 28
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ------------------------------------------------------------------------------------------------- the rule
OCT = [0, 1, 3, 4, 6, 7, 9, 10]          # the half-whole scale: sixteen rungs to two octaves
PRI = [0, 3, 2, 5, 1, 4]                 # the order a half bar's six places fill: the two beats, their pick-ups, the rest


def rung(x):
    return min(15, int(16 * x))


def cell(x):
    """x (0..1) -> (the places struck, which of them is the accent, the accent's rung). floor(7x) places are
    struck, in PRI order; the accent is chosen by how far x is through its seventh; its rung is floor(16x)."""
    k = min(6, int(7 * x))
    f = 7 * x - int(7 * x) if x < 6 / 7 else (x - 6 / 7) * 7
    slots = sorted(PRI[:k])
    return slots, (int(f * k) if k else -1), rung(x)


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def lock(x, lo, hi, period, n):
    """The dial setting in a window lo..hi from which the orbit, arriving at x, locks soonest onto its cycle of
    `period` (and whose cycle stays clear of the rule's edges, so that no rounding decides a note)."""
    best = None
    for i in range(201):
        r = lo + (hi - lo) * i / 200
        y, ys = x, []
        for _ in range(120):
            y = r * y * (1 - y)
            ys.append(y)
        t = next((j for j in range(n) if all(abs(ys[j + m] - ys[j + m + period]) < 2e-4 for m in range(period))), None)
        if t is None:
            continue
        clear = min(min(abs(v * q - round(v * q)) / q for q in (7, 16)) for v in ys[t:t + period])
        if clear > 0.001 and (best is None or (t, -clear) < (best[0], -best[2])):
            best = (t, r, clear)
    assert best, (lo, hi)
    return best[1]


# v3: THE BAND TELLS YOU WHERE THE RULE IS (whole-song round). Through v2 the riff changed under a band that did
# not: from 0:41 to 2:24 the finished file sat within 0.6 dB, four guitars and the same hat whether the rule was
# repeating or not, and the run down at the end changed the dial every four bars, before the rule had settled
# (its stretch "four" never once played its four half bars through). Three things, one idea:
#   - THE WALL AND THE OPEN HAT ARE FOR NEWS. Where the rule repeats, the band is two guitars and a closed hat:
#     a riff you know, played tight. Where it does not repeat (1:10, 1:44, the top, and the half bars in which
#     it is still finding a cycle), the second pair of guitars is in and the hat is open on every beat. So the
#     song steps where the rule changes state: up at 1:10, down at 1:27 (the lock on five is the leanest thing
#     in the middle of the song), up at 1:44, down at 2:01 and then built back a layer at a time (v2's layers:
#     the second pair of guitars now ARRIVES with the harmony the third time round), up at 2:24.
#   - THE TOP IS THE TOP: at the top of the dial every scream has the cymbal on it, ringing into the hole.
#   - THE DIAL COMES DOWN SLOWLY ENOUGH TO HEAR. Each setting on the way down now lasts until the rule has
#     settled and said its cycle: four (seven half bars of finding it, then the two-bar riff twice), two, and
#     then one: the shuffle of 0:14 comes home for six bars before the song dies out.
# the run down's half bars at four ; at two ; at one ; the velocity of the cymbal on a scream at the top. "" = v2.
TELL = os.environ.get("C10T6_TELL", "16;12;12;0.9")
DOWN = [int(v) for v in TELL.split(";")[:3]] if TELL else [8, 8, 8]

# name, half bars, the dial. A list is one setting for each half bar; a tuple (lo, hi, period) is a window.
DIAL = [
    ("growth", 16, lin(1.5, 2.8, 16)),
    ("one", 16, lin(2.8, 2.98, 16)),
    ("two", 16, [3.2] * 8 + [3.4] * 8),
    ("four", 16, [3.5] * 16),
    ("eight", 16, [3.555] * 16),
    ("chaos", 20, lin(3.6, 3.7, 20)),
    ("five", 20, (3.7383, 3.7410, 5)),
    ("chaos2", 16, [3.8] * 16),
    ("three", 18, (3.8290, 3.8405, 3)),
    ("six", 12, [3.845] * 12),
    ("full", 32, [3.995] * 32),
    ("down-four", DOWN[0], [3.5] * DOWN[0]),
    ("down-two", DOWN[1], [3.2] * DOWN[1]),
    ("down-one", DOWN[2], [2.8] * DOWN[2]),
    ("out", 4, [1.0] * 4),
]
X0 = 0.02


def orbit():
    """-> [(section, r, x before, x)] for every half bar, and each section's first half bar."""
    x, cells, starts = X0, [], {}
    for name, n, dial in DIAL:
        starts[name] = len(cells)
        rs = [lock(x, dial[0], dial[1], dial[2], n)] * n if isinstance(dial, tuple) else dial
        assert len(rs) == n, name
        for r in rs:
            x0, x = x, r * x * (1 - x)
            cells.append((name, r, x0, x))
    starts["end"] = len(cells)
    return cells, starts


CELLS, AT = orbit()
NC = len(CELLS)
NB = NC // 2 + 1


# ------------------------------------------------------------------------------------------------- the band
def add(tr, c, slot, len_slots, pitch, vel, **expr):
    """Half bar c, place `slot` (thirds of a beat), `len_slots` long."""
    n = {"at": round(c * 2 + slot / 3, 5), "len": round(len_slots / 3 * 0.96, 5), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, c, slot, vel, tr=None):
    if TUNE and ((piece == "k" and keyof(c)) or (piece == "b" and keyof(c) == 3)):
        piece += str(keyof(c))                # v7: the machine's kick (and its boom at the top) tuned to the ground
    tr = tr or {"k": "kick", "k1": "kick", "k2": "kick", "k3": "kick", "s": "snare", "p": "snare", "h": "hat", "o": "hat", "c": "cym", "b": "boom", "b3": "boom"}[piece]
    T.setdefault(tr, []).append({"at": round(c * 2 + slot / 3, 5), "len": 0.25, "pitch": piece, "vel": round(vel, 3)})


def note(r):
    return E1 + 12 * (r // 8) + OCT[r % 8]


def keyof(c):
    """How many minor thirds over E the band stands at half bar c (see KEYS, v6)."""
    if not KEYS:
        return 0
    k5, k3, kt = (int(v) for v in KEYS.split(";")[:3])
    return 0 if c >= AT["down-four"] else kt if c >= AT["full"] else k3 if c >= HEAD3 else k5 if c >= AT["five"] else 0


def gup(c):
    """Semitones the guitars, the lead and the chips are over the E version at half bar c."""
    return 3 * keyof(c)


def bup(c):
    """The same for the bass: at the top it goes under, not over."""
    return int(KEYS.split(";")[3]) if KEYS and AT["full"] <= c < AT["down-four"] else 3 * keyof(c)


# v10: the guitars detect a repeat by playing it. The left stays with the
# rhythm section; the right reads back by the period of the next locked riff.
# Only the fingering travels: the guitarist stays on the current ground.
READ_BACK = os.environ.get("C10T6_READ_BACK", "1")


def play(c, x, gtrs, bass=True, kick=True, harm=()):
    sec = CELLS[c][0]
    lag = 5 if sec in ("chaos", "five") else 3 if sec in ("chaos2", "three") else 0
    if READ_BACK and lag:
        then = CELLS[c - lag][3]
        if cell(then) != cell(x):
            right = tuple(tr for tr in gtrs if tr in ("gr", "gr2"))
            play_cell(c, then, right, False, False, harm)
            gtrs = tuple(tr for tr in gtrs if tr not in right)
    play_cell(c, x, gtrs, bass, kick, harm)


def play_cell(c, x, gtrs, bass, kick, harm):
    """`harm`: the guitars that take an accent from the octave up two rungs higher."""
    slots, ai, r = cell(x)
    for i, s in enumerate(slots):
        nxt = slots[i + 1] if i + 1 < len(slots) else 6
        if i == ai:                           # the accent: a fretted note; from the octave up, a fifth on it
            p = note(r) + gup(c)
            for tr in gtrs:
                q = note(r + 2) + gup(c) if tr in harm and r >= 8 else p
                add(tr, c, s, nxt - s, nm(q) if r < 8 else f"{nm(q)},{nm(q + 7)}", 1.0)
            if bass:
                add("bass", c, s, nxt - s, note(r % 8) + bup(c), 0.95)
            if kick:
                drum("k", c, s, 1.0)
        else:                                 # a muted chug on the open low string
            for tr in gtrs:
                add(tr, c, s, 1, E1 + gup(c), 0.88, pm=1)
            if bass:
                add("bass", c, s, 1, E1 + bup(c), 0.85)
            if kick:
                drum("k", c, s, 0.86)


# v2: WHAT A BAND CAN DO ONCE THE RIFF REPEATS (section round, 1:51-2:19: the window of three, which the map called
# static). While the rule never repeats, nobody can arrange it: every half bar is news, so the band plays it in
# unison. In a window the same three half bars come round again and again, and a band that has heard a riff twice
# starts to arrange it. So the window is now told that way, a layer for each time round:
#   - it FINDS the cycle: the dial moves at 1:58 and for three half bars the rule is still settling; the snare keeps
#     the back beat of the stretch before. On the first scream of the cycle proper (2:01) the cymbal and the clap
#     mark it and the snare drops to half time: the groove changes when the rule locks, not when the dial moves;
#   - the second time round, a second chip answers in the hole (the cycle has one: a single low note, then nothing
#     for most of a half bar): it plays the cycle's own three notes as one triplet, the cycle inside itself, and
#     its last note is the note the band plays next;
#   - the third time round, the second pair of guitars takes the scream two rungs higher (a third), so the scream
#     is a four-note chord and no longer a fifth;
#   - both go on through the six (2:14).
# the time round at which the answer starts ; at which the harmony starts ; the answer's gain ; its register
# (semitones over the riff's) ; its pan. "" = v1.
LOCK = os.environ.get("C10T6_LOCK", "2;3;-14dB;24;0.4")


def lock_head(sec, period, rhythm=False):
    """The first half bar of `sec` that begins the cycle proper: its highest number, once the cycle repeats
    (`rhythm`: once the places struck repeat, whatever the accent does)."""
    a, b = AT[sec], AT[sec] + dict((n, k) for n, k, _ in DIAL)[sec]
    same = (lambda i, j: cell(CELLS[i][3])[0] == cell(CELLS[j][3])[0]) if rhythm else (lambda i, j: cell(CELLS[i][3]) == cell(CELLS[j][3]))
    t = next(j for j in range(a, b - period) if all(same(i, i + period) for i in range(j, b - period)))
    return next(j for j in range(t, t + period) if CELLS[j][3] == max(CELLS[i][3] for i in range(t, t + period)))


# v4: THE WAY UP HAS EVENTS, AND THE TOP IS THE SUM (whole-song round; both were costs of v3, said in its note).
# v3 saved the second pair of guitars for the stretches that do not repeat, which left the first minute on two
# guitars with nothing happening at 0:42 and 0:56 but the riff doubling its length; and at the top (2:24) the band
# DROPPED what it had just learned in the window of three (the chord on the scream, the chip's answer).
#   - THE HAT COUNTS FINER AS THE RIFF GETS LONGER. One and two: the machine's hat on the beat (two to a half
#     bar). Four (0:42): the shuffle's four places. Eight (0:56): all six, running. Then at 1:10 it opens, on the
#     beat, with the wall. The first minute builds on the machine alone.
#   - EIGHT IS A RIFF SAID TWICE, AND A BAND ARRANGES A REPEAT (v2's rule): the second time (1:03) the tune has a
#     second voice, a third above it. Like the tune it has no notes in the song: it is the engine's logistic
#     generator again, the same orbit read off a ladder two rungs higher (in this scale two rungs are always a
#     minor third).
#   - THE TOP KEEPS WHAT THE SONG HAS LEARNED: the screams stay chords (the second pair two rungs up, as from
#     2:06), and wherever the three's shape turns up again inside the chaos (a scream, then one low note: it
#     does, twice, because the top of the dial is next door to that window) the chip answers as it did there.
# hats to a half bar at four ; at eight ; the velocity of the two pick-up places ; of the other two ; the second
# voice's gain ; its pan ; 1 = the top keeps the chord and the answer. "" = v3.
UP = os.environ.get("C10T6_UP", "4;6;0.45;0.38;-20dB;-0.4;1")
HATS = {"four": int(UP.split(";")[0]), "eight": int(UP.split(";")[1])} if UP else {}
HEAD3 = lock_head("three", 3) if LOCK else None
HEAD4D = lock_head("down-four", 4, rhythm=True) if TELL else None
# v6: FOUR KEYS, ONE SCALE (whole-song round). Through v5 the song never left E: three and a half minutes on one
# pedal, every stretch told apart by rhythm alone. The scale it is written in has a property no ordinary scale
# has: moved up a minor third it is THE SAME EIGHT NOTES. So the band can change key and not change a note of its
# scale, and four such steps come back to where they began: E, G, B flat, D flat, E. The song now takes that
# road, one step at each change of state that v3 gave the band:
#   - 1:27, the lock on five: everything a minor third up, on G (and the wall at 1:44 stays there);
#   - 2:01, the lock on three (on the cymbal, not on the dial): on B flat, the far side of the circle from E;
#   - 2:24, the top of the dial: on D flat. The guitars' screams are now the highest notes of the song (B3 and
#     its fifth, D4 on the second pair), and the BASS does not go up with them: it goes UNDER, to the D flat
#     below its E, the lowest note it plays anywhere. The top has the song's top and its bottom;
#   - 2:52, the dial comes down: E. For the guitars a fall of a sixth onto the open string; for the bass one
#     more minor third UP, from that low D flat to the E it started on. Four steps up, and home.
# It is a long cycle that lines up, in pitch this time: the record's subject once more.
# The tune and the chips go with the band (the engine's generators are given the same ladder, moved); the
# machine's kick and boom stay on E, which is in the scale in every one of the four keys.
# steps of a minor third over E at the lock on five ; at the lock on three ; at the top ; the bass's semitones
# from E at the top. "" = v5.
KEYS = os.environ.get("C10T6_KEYS", "1;2;3;-3") if LOCK and TELL else ""
# v7: THE MACHINE TUNES ITS KICK TO THE GROUND (whole-song round, on two costs of v6 said in its note). v6 moved the
# band through four keys and left the machine's kick and boom on E, "which is in the scale in all four". In the
# scale is not the same as in tune with the floor: a kick resting on E (41 Hz) under guitars and a bass on G (49 Hz)
# or B flat (58 Hz) is two low notes a third or a tritone apart in the one octave where intervals are mud. Anyone
# who programs a drum machine tunes its kick to the song's key; this song has four. So the kick now rests on G
# where the ground is G, and at the top, where the bass goes under to its low D flat, the kick and the long boom
# go down there with it. On B flat it rests on F, the fifth under the ground, not on B flat itself: benched on
# B flat (58 Hz) nothing in the band sat under 58 Hz and the bottom octave read 6.7 dB under the records.
# AND the bottom octave on G and B flat (v6: 2.8 to 2.9 dB under the records): the bass bus's cut at the bass's
# own fundamental no longer follows the bass up from E. It was made for E; up a third or a tritone the fundamental
# is where a bass is heard, and the band needs it.
# the kick's note on G ; on B flat ; at the top ; the boom's at the top ; `fixed` = the bass bus's 41.5 Hz cut stays
# where it is ("" = it follows the key, as v6). "" = v6.
TUNE = os.environ.get("C10T6_TUNE", "G1;F1;Db1;Db1;fixed") if KEYS else ""
# v5: THE FIRST LOCK GOES WITH THE CYCLE (section round, 1:23-1:51: the window of five). There are two things a
# band can do with a cycle that does not fit the bar. It can hold the bar and let the cycle turn against it: that
# is the window of three (2:01), where the snare stays on the bar's third beat and the riff comes round under it,
# three against two. Or it can drop the bar and go with the cycle. Through v4 both windows did the first. Now the
# window of five does the second: for its seventeen seconds the song is IN five. The cycle is ten beats long, and
# the machine plays it as a drummer counts ten: four, four and two. The snare is on the third beat of each four
# (the first of them lands on the cycle's one lonely low note), and both beats of the two are snare, a push into
# the cycle's head, where the cymbal is. Nothing in that stretch marks the song's own bar but the hat, which never
# stops keeping the beat; after four times round, ten bars have gone by and the two meet again.
# the snare's beats in the ten-beat cycle ; those of them with the clap ; the cymbal's velocity on each head. "" = v4.
FIVE = os.environ.get("C10T6_FIVE", "3,7,9,10;3,7;0.85")
HEAD5 = lock_head("five", 5) if FIVE else None
assert not FIVE or HEAD5 == AT["five"], "the window of five is written for a cycle that locks at once"
assert LOCK or not TELL, "C10T6_TELL builds on C10T6_LOCK"

G = ("gl", "gr")
G2 = ("gl2", "gr2")
G3 = ("gl3", "gr3")
BACK = {"one", "two", "four", "eight", "chaos", "chaos2", "full", "down-four", "down-two", "down-one"}   # the snare on two and four
HALF = {"five", "three", "six"}                                                                          # the snare on three only
WIDE = {"chaos", "chaos2", "three", "full"} if TELL else {"four", "eight", "chaos", "five", "chaos2", "three", "six", "full"}   # four guitars
LEAD = {"two", "four", "eight", "chaos", "five", "chaos2", "three", "six", "full", "down-four", "down-two"}


def compose():
    for c, (sec, r, x0, x) in enumerate(CELLS):
        first = c == AT[sec]
        if sec == "growth":
            gtrs = () if c < 8 else ("gl",)
            play(c, x, gtrs, bass=c >= 4)
        elif sec == "out":
            play(c, x, G)
        elif LOCK and (sec == "six" or (sec == "three" and c >= HEAD3)):
            turn = (c - HEAD3) // 3 + 1                       # which time round the cycle this is
            layered = turn >= int(LOCK.split(";")[1])
            apart = (c - AT["six"]) // 3 if UNWIND and sec == "six" else -1            # v20: which time round the six
            left = [apart >= int(v) for v in UNWIND.split(";")[:3]] if apart >= 0 else [False] * 3
            layered = layered and not left[0]
            play(c, x, (G[:1] if left[2] else G) + (G2 if layered or not TELL else ()), harm=G2 if layered else ())
            if len(cell(x)[0]) == 1 and turn >= int(LOCK.split(";")[0]) and not left[1]:     # the hole: the cycle's three notes, as a triplet
                for i, (cc, v) in enumerate(((c - 1, 0.8), (c, 0.7), (c + 1, 0.9))):
                    add("echo", c, 3 + i, 1, note(rung(CELLS[cc][3])) + int(LOCK.split(";")[3]) + gup(c), v)
        elif UP and UP.split(";")[6] == "1" and sec == "full":
            play(c, x, G + G2, harm=G2)
            if len(cell(x)[0]) == 1 and len(cell(CELLS[c - 1][3])[0]) == 6:      # the three's shape again: the chip answers
                for i, (cc, v) in enumerate(((c - 1, 0.8), (c, 0.7), (c + 1, 0.9))):
                    add("echo", c, 3 + i, 1, note(rung(CELLS[cc][3])) + int(LOCK.split(";")[3]) + gup(c), v)
        else:
            play(c, x, G + (G2 if sec in WIDE else ()))
        # the steady pulse: the machine's hat on every beat, opened on the last beat before a new setting
        finding = LOCK and sec == "three" and c < HEAD3       # the dial has moved and the rule has not settled yet
        news = TELL and cell(x)[0] and (sec in ("chaos", "chaos2", "full") or finding or (sec == "down-four" and c < HEAD4D))
        if sec != "out":
            for s in (0, 3):
                last = c + 1 < NC and CELLS[c + 1][0] != sec and s == 3
                drum("o" if last or news else "h", c, s, 0.75 if (s == 0 and c % 2 == 0) else 0.55)
            for s in {2: (), 4: (2, 5), 6: (1, 2, 4, 5)}[HATS.get(sec, 2)]:      # v4: the hat counts finer as the riff gets longer
                drum("h", c, s, float(UP.split(";")[2 if s in (2, 5) else 3]))
        if TELL and sec == "full" and len(cell(x)[0]) == 6:   # the top: the cymbal on every scream
            drum("c", c, cell(x)[0][cell(x)[1]], float(TELL.split(";")[3]))
        if FIVE and sec == "five":                            # v5: the machine counts the cycle, not the bar
            k = (c - HEAD5) % 5
            for b in (int(v) for v in FIVE.split(";")[0].split(",")):
                if (b - 1) // 2 == k:
                    drum("s", c, 0 if b % 2 else 3, 1.0 if b % 2 else 0.9)
                    if str(b) in FIVE.split(";")[1].split(","):
                        drum("p", c, 0 if b % 2 else 3, 0.8)
            if k == 0 and not first:
                drum("c", c, 0, float(FIVE.split(";")[2]))
        elif sec in BACK or finding:
            drum("s", c, 3, 0.95)
        elif sec in HALF and c % 2 == 1:
            drum("s", c, 0, 1.0)
            drum("p", c, 0, 0.8)
        if LOCK and sec == "three":
            if c == HEAD3:                                    # it locks: the cymbal and the clap on the cycle's first scream
                drum("c", c, 0, 0.95)
                if c % 2 == 0:                                # (on a bar's third beat the half-time snare brings its own clap)
                    drum("p", c, 0, 0.9)
        elif first and sec not in ("growth", "out") and not (TELL and sec == "down-four"):   # (the last scream's cymbal is still ringing there)
            drum("c", c, 0, 0.9)
        # a hole (a half bar with nothing in it) after sound: the boom falls through it
        if sec not in ("growth", "out") and not cell(x)[0] and c and cell(CELLS[c - 1][3])[0]:
            drum("b", c, 0, 0.95)


# v8: THE MACHINE AND THE RECORD'S KIT TOGETHER (Harry, 17 Nov 00:29, on the card "a drum machine under the guitars.
# Keep it?": "The machine and the record's kit together"). The record's kit is the one the other five songs share
# (`ct-kit`, its room and overheads as on Running Total). It plays the DRUMMER'S part and the machine keeps the
# MACHINE'S:
#   - the drummer: the kick on every note of the riff, the snare wherever the machine's snare falls, a crash where a
#     section starts and the china on every scream at the top. (Benched and left out: the china on the half bar
#     wherever the machine's hat is open. With it the wall stood 1.5 dB over the records at 4-8 kHz and 2.5 at
#     8-16 kHz: the open hat is already that stretch's cymbal. The last field turns it on.)
#   - the machine: everything it had. Its hat still counts (finer as the riff grows), its clap and its long boom are
#     its own, and its kick, tuned to each key (v7), is now the BOTTOM of a kick whose beater and skin are the kit's:
#     the kit's kick is high-passed, so the low octave is still the tuned one and nothing fights it there.
#   - THE PAIR WEIGHS WHAT THE ONE DID: stroke for stroke the kit's kick is 2 dB under the machine's (the machine is
#     the kick's body, the kit its beater) and the kit's snare level with the machine's to 2 dB over it (it has the
#     crack), and each pair is within a quarter of a decibel of the machine's one before.
#   - THE SONG STARTS AND ENDS ON THE MACHINE ALONE: while the rule is still growing (0:00-0:14) there is no drummer;
#     he comes in, on a crash, when the riff first settles and both guitars are in; the last two bars are the
#     machine's again.
# the kit's kick gain ; its snare ; its cymbals ; the kick's high-pass, Hz ; the machine's kick trim, dB ; its snare
# trim, dB ; the china's velocity on the half bar ; the kit kick's click (its 4.5 kHz lift, dB; the other songs have
# 10) ; the machine's cymbal trim, dB ; a dip on the kit's snare (Hz : q : dB: its body sits where the machine's
# snare was already cut, in the guitars' low mids) ; the kit bus's shelf at 9 kHz, dB (the other songs have -2: here
# the machine's hat already holds that band). "" = v7 (the machine alone).
KIT = os.environ.get("C10T6_KIT", "-3.5dB;-1.4dB;-5.5dB;130;-2.5;-3.6;0;5;-2;330:1:-4;-4.5")


def third_pair():
    """At the top a third pair plays what the first pair plays, each side its own side's part as it stands after
    the crests (where the first pair leaves an accent to the two ringing strings, so does the third). The scream,
    a fifth from the octave up, it plays an octave down."""
    lo, hi = 2 * AT["full"], 2 * AT["down-four"]
    for src, tr in zip(G, G3):
        for n in T[src]:
            if lo <= n["at"] < hi:
                m = dict(n)
                if "," in m["pitch"]:
                    low = [NAMES.index(q[:-1]) + 12 * int(q[-1]) for q in m["pitch"].split(",")]     # an octave under
                    assert len(low) == 2 and low[1] - low[0] == 7
                    m["pitch"] = ",".join(nm(q) for q in low)
                T.setdefault(tr, []).append(m)


def kit_part():
    """The record's kit, written from the machine's own part (so the two can never disagree)."""
    t0, t1 = AT["one"] * 2, AT["out"] * 2
    heads = {AT[name] * 2 for name, _, _ in DIAL}
    inside = lambda n: t0 <= n["at"] < t1
    T["dkick"] = [{**n, "pitch": "k"} for n in T.get("kick", []) if inside(n)]
    T["dsnare"] = [{**n} for n in T.get("snare", []) if inside(n) and n["pitch"] == "s"]
    T["dcym"] = [{**n, "len": 2.0, "pitch": "c" if n["at"] in heads or n["vel"] >= 0.95 else "x"} for n in T.get("cym", []) if inside(n)]
    struck = {n["at"] for n in T["dcym"]}
    ride = float(KIT.split(";")[6])
    for c, (sec, r, x0, x) in enumerate(CELLS):          # the china on the half bar where the machine's hat is open
        if ride and t0 <= c * 2 < t1 and c * 2 not in struck and sec != "full" and any(
                n["pitch"] == "o" and n["at"] == c * 2 for n in T.get("hat", [])) and sec in ("chaos", "chaos2", "three", "down-four"):
            T["dcym"].append({"at": c * 2, "len": 2.0, "pitch": "x", "vel": ride})


def lead_gens():
    """The lead's part is the rule itself: one `logistic` system for each run of half bars on one dial setting,
    started from the orbit's own number there, so the engine walks the same orbit the band is playing."""
    gens, c = [], 0
    while c < NC:
        sec, r, x0, _ = CELLS[c]
        pool = " ".join(nm(note(r_) + 36 + gup(c)) for r_ in range(16))
        n = 1
        while (c + n < NC and CELLS[c + n][0] == sec and CELLS[c + n][1] == r and keyof(c + n) == keyof(c)
               and (c + n in ROOM_CELLS) == (c in ROOM_CELLS)):
            n += 1
        gens.append((c, n, sec, {"type": "logistic", "r": r, "x0": x0, "n": n, "len": "/2", "notes": pool,
                                 "rest": 1 if c in ROOM_CELLS else round(1 / 7, 6)}))       # v24: the chip rests while somebody sings
        c += n
    return gens


def hair_gens():
    """v26: the second voice. The tune's own runs from the lock on five to the end of the second wall (same dial,
    same ladder, the same rests under the singers), walked from a number HAIR's first field away and never reset."""
    x, out = CELLS[AT["five"]][2] + float(HAIR.split(";")[0]), []
    end = AT[HOME.split(";")[0]] if HOME else AT["three"]                 # v27: it goes on, and the window of three brings it home
    unheard = set(HOME.split(";")[1].split(",")) if HOME else set()
    home = since = end
    if ONE:                                                               # v28: and on, unheard, to the top's last bars
        since, end = AT["full"] + int(HEARD.split(";")[4] if HEARD and HEARD.split(";")[4] else ONE.split(";")[1]), AT[ONE.split(";")[0]]   # v30: heard from the top's first bar
    for c, n, sec, g in lead_gens():
        if AT["five"] <= c < end:
            k = min(n, max(0, since - c)) if c >= home else 0                    # this many half bars of the run are walked and not heard
            for at, m, quiet in ((c, k, True), (c + k, n - k, sec in unheard)):
                if m:
                    out.append({**g, "x0": x, "n": m, **({"rest": 1} if quiet else {})})
                    for i in range(m):
                        x = CELLS[at + i][1] * x * (1 - x)
    assert sum(g["n"] for g in out) == end - AT["five"]
    return out


def one_voice():
    """v28: the half bar of the way down from which the second voice plays the tune's own note and never another (computed)."""
    x = CELLS[AT["five"]][2] + float(HAIR.split(";")[0])
    for c in range(AT["five"], AT["full"]):
        x = CELLS[c][1] * x * (1 - x)
    last = AT["full"]
    for c in range(AT["full"], NC):
        x, t = CELLS[c][1] * x * (1 - x), CELLS[c][3]          # what each plays in half bar c: the number after the step
        if (x < 1 / 7) != (t < 1 / 7) or (x >= 1 / 7 and min(15, int(x * 16)) != min(15, int(t * 16))):
            last = c + 1
    return last


def low_bus():
    """ct-bass's bus. v6: the three bands that sit on the bass's own notes go with the bass from key to key."""
    comp = {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"}
    if not KEYS:
        return {"fx": [{"type": "eq", "bands": ["peak cutoff=41.5 q=1.5 gain=-7dB", "peak cutoff=85 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                       comp, {"type": "eq", "bands": ["peak cutoff=160 q=1.2 gain=-3dB"]}]}

    def kf(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", 0]], 0
    for c in (AT["five"], HEAD3, AT["full"], AT["down-four"]):
        pts += [[f"{c * 2 - 0.02:g}b", prev], [f"{c * 2:g}b", bup(c)]]
        prev = bup(c)
    low = 41.5 if TUNE and TUNE.split(";")[4] == "fixed" else kf(41.5)
    return {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": low, "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": kf(85), "q": 1.0, "gain": "7.5dB"},
                                            "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                   comp, {"type": "eq", "bands": [{"kind": "peak", "cutoff": kf(160), "q": 1.2, "gain": "-3dB"}]}],
            "auto": {"key": {"points": pts, "curve": 0}}}


def second_voice():
    """Eight's second statement: the same orbit, read off the lead's ladder two rungs higher (a minor third)."""
    c = AT["eight"] + 8
    pool = " ".join(nm(note(r + 2) + 36) for r in range(16))
    return c, {"type": "logistic", "r": CELLS[c][1], "x0": CELLS[c][2], "n": 8, "len": "/2", "notes": pool, "rest": round(1 / 7, 6)}


# v9: on alternate laps of the doubling riff the keys take the two outside
# notes from the guitars. Upper/lower hand in dB; empty gives v8 exactly.
TINES = os.environ.get("C10T6_TINES", "-14;-13")


def periodic_tines():
    """Keep the bass and both kits playing the orbit under the ringing keys."""
    sections = (("one", 1), ("two", 2), ("four", 4), ("eight", 8),
                ("down-four", 4), ("down-two", 2), ("down-one", 1))
    exchanges, stays = [], {}
    keep = WITH.split(";")[0].split(",") if WITH else []
    side = {sec: WITH.split(";")[1] for sec in keep}
    lift = {sec: float(WITH.split(";")[3]) for sec in keep}
    if EIGHT:                                   # v25: and through eight's one lap of the keys
        keep, side["eight"], lift["eight"] = keep + ["eight"], EIGHT.split(";")[0], float(EIGHT.split(";")[2])
    for sec, period in sections:
        a = AT[sec]
        b = a + next(n for name, n, _ in DIAL if name == sec)
        if period == 1:
            a = b - 4                           # a single pitch to introduce / close the exchange
        if sec == "down-four" and HEAD4D is not None:
            a = HEAD4D                          # wait for the return to settle
        for lap, start in enumerate(range(a, b - period + 1, period)):
            if period != 1 and lap % 2 == 0:
                continue                        # guitars state a whole lap first
            cycle = range(start, start + period)
            end = (start + period) * 2
            exchanges.append((start * 2, end))
            if sec in keep:
                stays[(start * 2, end)] = G[0] if side[sec] == "l" else G[1]
            for hand, choose in (("high", max), ("low", min)):
                if period == 1 and hand == "low":
                    continue
                c = choose(cycle, key=lambda i: CELLS[i][3])  # by x, not by its rounded fret
                slots, accent, r = cell(CELLS[c][3])
                if not slots:
                    continue
                beat = round(2 * c + slots[accent] / 3, 5)
                pitch = note(r) + gup(c) + (24 if hand == "high" else 12)
                T.setdefault("tine-" + hand, []).append({"at": beat, "len": round((end - beat) * .97, 5),
                                                       "pitch": nm(pitch), "vel": .86 if hand == "high" else .82,
                                                       **({"gain": f"{lift[sec]:g}dB"} if sec in keep and lift[sec] else {})})
    back = set()                                # v25: the other guitar's own strokes on the accents the second half of eight moves
    if EIGHT and EIGHT.split(";")[1] == "moved":
        a = AT["eight"] + 8
        for c in range(a + 4, a + 8):
            now, then = cell(CELLS[c][3]), cell(CELLS[c - 4][3])
            if now != then:
                back.add(round((c * 6 + now[0][now[1]]) / 3, 5))
        other = G[1] if side["eight"] == "l" else G[0]
        assert len(back) == 3 and all(any(n["at"] == at for n in T[other]) for at in back), back
    for tr in G:
        gone = [span for span in exchanges if stays.get(span) != tr]                  # v23: one guitar plays on
        mine = back if EIGHT and tr != stays.get((AT["eight"] * 2 + 16, AT["eight"] * 2 + 32)) else ()
        T[tr] = [n for n in T[tr] if n["at"] in mine or not any(a <= n["at"] < b for a, b in gone)]
    if FORK:
        hold_the_split()


def hold_the_split():
    """In the first bifurcation, let the two fret values sound as an interval.
    Only play laps already given to guitars; the piano's replies stay bare.
    No new pitch class or attack: the high branch waits for its low partner.
    """
    def accent(c):
        slots,i,r = cell(CELLS[c][3])
        return round(c*2+slots[i]/3,5),note(r)+gup(c)
    for c in range(AT['two'], AT['four'], 2):
        high,h = accent(c); low,l = accent(c+1)
        if h<=l or not any(n['at']==high for n in T['gr']):
            continue  # no descending pair, or the tines have this lap
        assert any(n['at']==low for n in T['gl'])
        end = (c+2)*2
        for tr,at,midi in (('gr',high,h+int(FORK)), ('gl',low,l)):
            # Keep the pick on the original accent and lift both fretting
            # hands just before the pianist answers. The floor keeps its gallop.
            T[tr] = [n for n in T[tr] if not at<=n['at']<end]
            T[tr].append({'at':at,'len':round(end-.12-at,5),'pitch':nm(midi),'vel':.94})


# v11: the right player's harmonic is tuned by the number of unoccupied slots.
# Once the cell is full enough to shuffle, the thumb lifts for a fretted G.
# A song-local clean rig, dry enough to stop in the gaps. Empty restores v10.
GROWTH_TOUCH = os.environ.get("C10T6_GROWTH_TOUCH", "-3dB")


def growth_harmonics():
    end = AT['one']
    touch_only, single = set(), {}
    for c in range(AT['growth'], end):
        slots, ai, r = cell(CELLS[c][3])
        if not slots:
            continue                    # no pitched sound before the first occupied slot
        hit = slots[ai]
        stop = slots[ai + 1] if ai + 1 < len(slots) else len(PRI)
        partial = 1 + len(PRI) - len(slots)
        # Touch a node on the actual fretted string, not a higher MIDI note.
        # The string rings up to the orbit's next stroke, never across it.
        contact = min(1., (end - 1 - c) / 4)
        pitch = note(r) + gup(c)
        add('touch', c, hit, stop - hit - .12, pitch, .93, node=partial, contact=contact)
        at = T['touch'][-1]['at']
        if contact == 1:
            touch_only.add(at)
        elif contact >= .5:
            single[at] = nm(pitch)
    # The left player arrives with just the low shuffle, not another attack
    # masking the harmonic. Its accents come back as roots and then fifths.
    T['gl'] = [dict(n, pitch=single[n['at']]) if n['at'] in single else n
               for n in T['gl'] if n['at'] not in touch_only]


# v12: two crests inside 'full' almost repeat. The inner left sings the accents
# on both; on their return the inner right remembers the timing of the first.
# Octave of the singing line in semitones. Empty restores v11.
CREST = os.environ.get('C10T6_CREST', '12' if GROWTH_TOUCH else '')


def crest_lines():
    # Separate phrases at the orbit's actual empty half-bars. Compare the
    # pitches, not just the count: these are not two copies pasted into the song.
    runs = []
    for c in range(AT['full'], AT['down-four']):
        slots, ai, r = cell(CELLS[c][3])
        if slots:
            if not runs or runs[-1][-1][0]+1 != c:
                runs.append([])
            runs[-1].append((c, slots[ai], r))
    seen = {}
    for run in runs:
        key = tuple(r for _, _, r in run)
        old = seen.get(key)
        if len(run) >= 4 and old and [s for _,s,_ in old] != [s for _,s,_ in run]:
            break
        seen[key] = run
    else:
        return

    def sing(tr, dest, attacks, upper):
        start, stop = dest[0][0], dest[-1][0]+1
        T[tr] = [n for n in T[tr] if not 2*start <= n['at'] < 2*stop]
        onsets = [c*6 + hit for (c,_,_), (_,hit,_) in zip(dest, attacks)] + [stop*6]
        for (c,_,r), a, b in zip(dest, onsets, onsets[1:]):
            # Cut even the last string before the empty cell. The lower hand
            # uses the harmony the doubles already played on the high accents.
            pitch = note(r) + int(CREST) if upper else note(r+2 if r>=8 else r)
            gate = b-a-.18 if upper else min(b-a-.18, 2.4)
            add(tr, c, a-6*c, gate, pitch+gup(c), .94)

    sing('gl2', old, old, True)
    sing('gl2', run, run, True)
    sing('gr2', run, old, False)
    # The first and last accents still belong to everybody. Between them the
    # rhythm pair plays the chugs but leaves the accents to the two ringing
    # strings, including the one late answer. Neither kick is ducked or moved.
    space = {round(2*c + hit/3, 5) for (c, now, _), (_, then, _) in zip(run[1:-1], old[1:-1])
             for hit in (now, then)}
    for tr in G:
        T[tr] = [n for n in T[tr] if n['at'] not in space]


# v13: in the last window the clean guitar remembers its opening notes.
# Empty restores v12; switching off CREST still gives the pre-crest version.
LAST_TOUCH = os.environ.get("C10T6_LAST_TOUCH", "1") if CREST and TINES else ""
# Upper branch's register above the original accent (in semitones).
# Empty restores v13, and LAST_TOUCH empty still defaults to v12.
FORK = os.environ.get('C10T6_FORK', '12' if LAST_TOUCH else '')


# v15: on the way down the right guitar already plays the riff the rule is
# settling on (it learned these cycles on the way up); the left, the bass and
# both kits still play the orbit. The two sides agree when the rule locks.
# Empty restores v14. It is on only while every earlier switch is, so each
# of them still gives exactly what it gave at v14 (TUNE implies KEYS and TELL).
AHEAD = os.environ.get('C10T6_AHEAD', '1' if all((FORK, READ_BACK, KIT, TUNE, FIVE, UP)) else '')


def know_the_way():
    """Half bars where the orbit has not yet reached its cycle: the right hand plays the settled lap instead."""
    told = []
    for sec, period in (('down-four', 4), ('down-two', 2)):
        a = AT[sec]
        b = a + next(n for name, n, _ in DIAL if name == sec)
        # The settled lap: the first locked four, or the last two half bars.
        ref = HEAD4D if sec == 'down-four' else b - period
        # Leave the hole after the last scream, and the single low note that
        # follows it, to the boom: the right hand starts when the riff does.
        first = next(c for c in range(a, ref) if len(cell(CELLS[c][3])[0]) > 2) if sec == 'down-four' else a
        for c in range(first, ref):
            goal = CELLS[ref + (c - ref) % period][3]
            if cell(goal) == cell(CELLS[c][3]):
                continue
            T['gr'] = [n for n in T['gr'] if not 2 * c <= n['at'] < 2 * c + 2]
            play_cell(c, goal, ('gr',), False, False, ())
            told.append(c)
    return told


# v16: WHAT THE DOUBLING MOVED (section round, 0:55-1:23; the guitars' lap of eight, 0:56-1:03). Eight is four said
# twice, and the rule changes very little the second time: the same strokes in every half bar, the same first
# accent, and then three accents that have MOVED (the low B from the first beat to the second; the chord from B flat
# to B and two places later; the E a place earlier). Those three are all the news there is in a riff that repeats,
# and since v3 the second pair of guitars is for news. So it is heard here for the first time, nine seconds before
# it arrives as the wall: three chords, each struck on a moved accent and HELD to the next while the first pair
# goes on chugging under it. Where the accent is a low single note the pair plays it as the chord an octave up;
# where it is a chord, two rungs over the first pair (as it will from 2:06). That makes B, then B minor seventh,
# then E minor seventh: the riff's last bar is a cadence home, and the keys answer it. The drummer, who has now
# heard the first half, marks each with the china. The machine marks nothing: it only counts.
# (First bench: the three struck no longer than the first pair's own accents, a triplet eighth for two of them.
# They read 0.8 to 1.1 dB over v15 for a third of a second: an accent nobody would hear as an arrival.)
# the china's velocity on a moved accent ; the gap before the next chord, in places. "" = v15.
MOVED = os.environ.get("C10T6_MOVED", "0.8;0.3") if AHEAD else ""


def moved_accents():
    """-> the beats of the accents in the second half of eight's first lap that are not where the first half had them."""
    a, found = AT["eight"], []
    for c in range(a + 4, a + 8):
        now, then = cell(CELLS[c][3]), cell(CELLS[c - 4][3])
        if now == then:
            continue
        slots, ai, r = now
        assert slots == then[0], "the doubling moves accents, not strokes"
        found.append((c * 6 + slots[ai], c, r))
    ends = [p for p, _, _ in found[1:]] + [(a + 8) * 6]          # each rings to the next; the last to the end of the lap
    for (p, c, r), end in zip(found, ends):
        q = (note(r + 2) if r >= 8 else note(r) + 12) + gup(c)
        for tr in G2:
            add(tr, c, p - c * 6, end - p - float(MOVED.split(";")[1]), f"{nm(q)},{nm(q + 7)}", 1.0)
    marks = [round(p / 3, 5) for p, _, _ in found]
    assert len(marks) == 3 and all(any(n["at"] == at for n in T[tr]) for at in marks for tr in G), "the guitars' own lap"
    return marks


# v17 (whole song): the hand on the dial. The machine only works the rule out;
# it cannot know the dial is about to move. The drummer can: the form is
# his. Until now he had no toms and played no fill. On the last bar before
# each turn of the dial his hands say the riff's own strokes on the toms
# (his feet keep the kick; where his snare or china falls the hands are
# there): floor to high when the dial is going up, high to floor when it is
# coming down. No stroke is added to the rule. Not into 'one' (he is not
# playing yet) and not into 'out' (the ending folds as it did).
# Track gain ; first stroke's velocity ; last stroke's ; trim in dB where only
# two guitars play (one fader left the fills 4 dB hotter against the lean band
# than against the wall, and the bar 1.2 dB up). Empty restores v16.
TOMS = os.environ.get("C10T6_TOMS", "0.1dB;0.62;0.95;-6") if MOVED and KIT else ""


def hand_on_the_dial():
    v0, v1, lean = (float(v) for v in TOMS.split(";")[1:4])
    names = [name for name, _, _ in DIAL]
    hands = {n["at"] for tr in ("dsnare", "dcym") for n in T[tr]}
    turns = []
    for after in names[2:-1]:
        c = AT[after]
        up = CELLS[c][1] > CELLS[c - 1][1]
        strokes = sorted(n["at"] for n in T["dkick"] if (c - 2) * 2 <= n["at"] < c * 2 and n["at"] not in hands)
        assert len(strokes) >= 3, after
        ladder = ("ft", "t2", "t1") if up else ("t1", "t2", "ft")
        wall = any((c - 2) * 2 <= n["at"] < c * 2 for n in T.get("gl2", []))
        for i, at in enumerate(strokes):
            T.setdefault("dtoms", []).append({"at": at, "len": 0.25, "pitch": ladder[i * 3 // len(strokes)],
                                              "vel": round(v0 + (v1 - v0) * i / (len(strokes) - 1), 3),
                                              **({} if wall or not lean else {"gain": f"{lean:g}dB"})})
        turns.append((after, up, wall))
    # (v20: the bar before the top is no longer a wall, so by this function's own rule its fill carries the lean trim)
    assert len(turns) == 12 and [u for _, u, _ in turns] == [True] * 9 + [False] * 3 and sum(w for _, _, w in turns) == (4 if UNWIND else 5) - ('again' in ROOM_PARTS)
    # (v24: nor is the bar before the six, where the second pair waits for the singers: by the same rule its fill is trimmed)


# v18 (whole song): at the top the drummer is the population. The top of
# the dial was marked by cymbals and holes, not by size (v3, v4, held since).
# It is the one place the rule crashes to nothing and grows back, and both
# kits kept the backbeat straight through it. Now the drummer stops with
# the band: in the empty half bars only the machine counts (its snare, its
# closed hat, the boom). When the riff grows back he comes back with it on
# the toms, floor to high, on the riff's own strokes, up to the next
# scream: the hand that rises before each turn of the dial (v17) is the
# regrowth here. No stroke is added to the rule. The value is a trim in dB
# on these toms: untrimmed, the half bar before each scream came up so far
# that the scream's own step shrank by up to a decibel. Empty restores v17.
REGROW = os.environ.get("C10T6_REGROW", "-2") if TOMS else ""
# v19 (chirper-one; whole song): TWO, FOUR, SIX. Since v3 the band's size says where the rule is: two guitars where
# it repeats, four where it does not. The top of the dial had the same four as the walls at 1:10 and 1:44, and its
# size was named as not achieved at v3 and v4 ("marked by the cymbals and the holes, not by size"). Read in the
# finished file at v18, the loudest second of the song was not at the top at all: it was just after it, where the
# dial comes down (2:52), and the windows before it (2:01-2:24) stood over the top's loudest scream as well.
# At the top the rule fills the whole range: it is the one place the population reaches the room there is. So at
# the top, and only there, a THIRD pair of guitars plays (a third amp, the engine's `mark`, which this song had not
# used; inside the other two pairs): every half bar the band plays there, with the first pair, note for note as
# that pair stands after v12's crests (where it leaves an accent to the two ringing strings, so does the third).
# And the scream, a fifth at the top of the neck with the second pair's third above it, gets a FLOOR: the third
# pair plays it an octave down, so each scream is three chords deep. In the holes they are silent with everyone.
# (First bench at the second pair's level, -3.5 dB: 7 to 8 dB under everything else on the screams (K), which read
# +0.7 dB; the top's loudest second then stood 0.1 dB over the windows before it. A pair that is there to be the
# top has to be heard as one: -1 dB.)
# the patch ({} = the cone) ; its gain ; its pan ; the two cones ; the song's loudness target (every bar outside
# the top keeps v18's mastering gain: with the target left at -10 the rest of the song came out 0.06 dB lower).
# "" = v18.
SIX = os.environ.get("C10T6_SIX", "ct-twin fx.1.model=mark fx.2.mic=0.55 fx.2.cone={};-1dB;0.45;34,35;-9.94") if REGROW else ""
# v20 (whole song: the step INTO the top): WHAT THE WINDOW BUILT, THE SIX TAKES APART. Read in the finished file at
# v19 the song does not step from 1:10 to 3:00: wall, lock, wall, lock, six and top stand within a decibel of each
# other, and the stretch at the top of the dial, six guitars and all, reads a decibel UNDER the six before it (its
# holes; and the limiter takes half a decibel more off its screams than off anything else). Three rounds today made
# the top bigger. This one makes what comes before it smaller, and the rule says how.
# In the window of three the band arranges a riff it has heard twice, a layer each time round (v2): the chip's answer
# in the hole the second time, the second pair of guitars and the third above the scream the third time. And "both
# go on through the six". But the six is where that lock comes apart: the dial has moved, the cycle of three has
# split in two, and the next thing the rule does is fill the whole range. So through the six the band now takes its
# arrangement apart again, a layer each time round and last in, first out: the first time round all of it; the
# second, the second pair is gone and the scream is a bare fifth; the third, the chip no longer answers and the hole
# holds its one low note; the fourth, the right guitar is gone too, and the left guitar, the bass and the two kits
# say the cycle once more, as the song began (the left guitar was the first in, at 0:07). Then the top: six guitars,
# a new key, the cymbal. One guitar, then six.
# Nothing is added and nothing moves: 76 notes on gl2, gr2, gr and the chip are left out. The tune, the bass and
# both kits are as they were; the drummer's three rising toms before the turn (v17) are now over a lean band, not a
# wall, so by v17's own rule they carry its lean trim (-6 dB).
# the time round the six (0-3) from which the second pair is gone ; the chip's answer ; the right guitar ; the song's
# loudness target (the six is quieter, so with the target left at -9.94 every other bar came out 0.07 dB louder,
# and on one seed that was enough for the scorer to cut the opening at 0:14 and not 0:08).
# "" = v19.
UNWIND = os.environ.get("C10T6_UNWIND", "1;2;3;-10.006") if SIX and LOCK and TELL else ""
# v21 (chirper-one; section w1, 0:00-0:27; the change is 0:17.4-0:24.3): THE WOBBLE BEFORE THE DOUBLING. At 0:14 the
# rule has settled on ONE half bar, and the two guitars played it together twelve times running, the only stretch
# of the song with no detail of its own. But the dial is moving all through it, from 2.8 to 2.98, and at 3 the one
# splits in two. That split is not sudden. Near it, anything that disturbs the fixed point swings to the other side
# of it on the next turn, and back, and dies away more slowly the closer the dial gets: the doubling is a wobble
# before it is a riff. The notes cannot show it (the rule is already sitting on its point), so the hands do. Four
# times the two guitars play the half bar together, as before. Then the ACCENT, the one fretted chord, goes from
# side to side: left, right, left, right, the other guitar leaving that chord out and keeping the chugs. Then the
# WHOLE half bar does: left, right, left, right, one guitar at a time. Then the keys take the accent for two bars,
# as they did (v9), and at 0:27.8 the rule doubles: what the hands were doing, the notes now do. The bass, both
# kits and the keys are as they were; 20 guitar notes are left out and none is added or moved.
# half bars into the one at which the accent starts to change sides ; at which the whole half bar does ; the song's
# loudness target (those seven seconds are quieter, so with v20's target every other bar came out 0.027 dB louder).
# "" = v20.
FLIP = os.environ.get("C10T6_FLIP", "4;8;-10.033") if UNWIND and TINES else ""
# v22 (chirper-three; section w8, 3:14.8-3:32; the change is 3:16.5-3:21.7): THE WOBBLE DIES AWAY. v21's note asked
# for its mirror on the way down and said to read the passage first. Read: on the way up the hands had to invent the
# wobble, because the rule was sitting on its point. On the way down THE RULE REALLY DOES IT. At 3:16.5 the dial drops
# from 3.2 to 2.8 and the two half bars have to become one; the count does not go there, it rings down onto it,
# alternately under and over where it will rest (9/14 of the room, the carrying capacity at this setting), about a
# third smaller every bar: 0.190 under, 0.051 over, 0.048 under, 0.032 over, 0.028, 0.020, 0.018, 0.013. The notes
# already say so (the accent's fret goes D, A flat, F, G, F, G, G, G) and since v13 the clean string takes the accent
# whenever the count is under. But both guitars played all eight half bars together, so the settling had no size.
# Now each side of the resting point has a side of the room, and how much changes sides is the size of the swing:
# for four half bars ONE GUITAR AT A TIME (under: the right guitar's chugs with the clean string, which sits on the
# right; over: the left guitar alone, with the fretted chord); for two more only the CHORD keeps its side, both
# guitars chugging; then two half bars together, the one at rest, before the keys and the clean string take it as
# they did. It is v21 backwards and quicker: twelve half bars to build at 0:17, six to die, because the dial is no
# longer near 3. By subtraction: 14 guitar notes are left out, none is added or moved; the bass, both kits, the keys
# and the clean string are as they were.
# half bars of one guitar at a time ; half bars in which only the chord keeps its side ; the guitar that has the
# half bars under the resting point (r or l) ; the song's loudness target (those five seconds are quieter, so with
# v21's target every other bar came out 0.014 to 0.018 dB louder on three seeds). "" = v21.
SETTLE = os.environ.get("C10T6_SETTLE", "4;2;r;-10.049") if FLIP and LAST_TOUCH else ""
# v23 (chirper-three; section round, w2 0:27.8-0:55.7: 'two' and 'four'): ONE GUITAR STAYS WITH THE KEYS (Harry,
# 19 Nov 02:25, on the card that played 0:43: "Keep one guitar with the keys"; its other answers were "Keep the
# exchange" and "Prefer guitars both times"). Since v9 the guitars state a lap of the doubling riff and leave the
# next to two ringing keys, with only the bass and the two kits under them. Now the LEFT guitar, the song's first
# (it enters alone at 0:07), plays on through the keys' laps: the figure it would have played, as the rule gives
# it. The RIGHT guitar still leaves, so the exchange is still there, between the right guitar and the keys, over a
# left hand that does not stop. In 'two' the right guitar's held high note (v14) and the keys now answer each
# other across one unbroken figure; in 'four' (the card's passage) the keys' two notes ring over the riff they
# were taken from. The keys, the bass and both kits are note for note v22's; nothing is added that the rule did
# not already write: these are the left guitar's own notes, which v9 took out.
# the sections whose key laps keep a guitar ; which guitar (l or r) ; the song's loudness target ; dB on the keys'
# notes in those laps (with a guitar under them they lost 2 dB of their place against everything else). "" = v22.
# (The exchange also runs at 'one', 'eight' and on the way down: those are as they were. See the round note.)
WITH = os.environ.get("C10T6_WITH", "two,four;l;-9.966;2") if SETTLE and TINES else ""
# v24 (chirper-zero, whole song): THE SONG IS SUNG, AND THE LINE IS AS LONG AS THE CYCLE (Harry, 19 Nov 02:25, on the
# card "Should Carrying Capacity have a sung line?": "Develop both lines"; the others were "Keep it instrumental" and
# "Keep just the first line"). chirper-alpha's trial (round 14, not adopted until he answered) had one singer take
# the chip's five notes at 1:36 as "make some room" and the three's three notes at 2:09 as "no more room", the
# guitars leaving the space. Both are in now, as he heard them, and developed by the song's own rules:
#   - A BAND THAT HAS HEARD A RIFF TWICE ARRANGES IT (v2), so each line is sung twice, on the last two laps of its
#     lock, and the second time a second singer is two rungs higher: in this scale always a minor third (v4's rule
#     for the chip's second voice). The guitars stay out for both laps and their cue back in follows the second.
#   - AT THE TOP (2:24) THERE IS NO ROOM EXCEPT IN THE HOLES. The rule crashes to nothing three half bars long twice
#     up there (2:25, 2:46); both singers say "no more room" into each, the three's own notes moved to the top's
#     key, well under the screams around them. The two shorter holes stay empty.
#   - ON THE WAY DOWN THE LINE IS AS LONG AS THE CYCLE. The lock on five had five notes and the lock on three had
#     three. Coming down, on the keys' laps, where no guitar plays: at four, "make some more room", a syllable to
#     the half bar (the two lines made one); at two, "more room"; at one, where the rule comes to rest (3:23.5),
#     "room", on the note it rests on. Every pitch is the half bar's own accent, folded into one octave.
#   - THE VOICE. As on the card (`voice-near`, a bigger tract) it was 8 to 10 dB over the records' sung passages at
#     250-500 Hz and 6 to 10 under at 1-4 kHz in the mix, and 'room', the word, was its quietest syllable (10 dB
#     under 'some', nearly all of it under 500 Hz). So: the eq this record's other sung song uses (t15) with a deeper
#     cut at 330, half of the singer's ring, and 4 dB on 'room' wherever it is sung (not on the note it is carried over).
# NOTHING IS ADDED TO THE RULE'S RIFF: the guitars lose 56 strokes each in the four sung laps, the second pair 20,
# the chip's answer six and the lead chip rests in the sung half bars; the bass and both kits keep every place.
# the first singer's gain ; the second's ; which developments (again, top, down) ; the song's loudness target ; dB on
# each line (five once, again ; three once, again ; the top ; four, two, one: set on finished files so that a sung
# lap weighs what the band's lap before it does, and the top's holes stay 3 to 5 LU under the screams) ; the
# voice's eq (high-pass / peaks, Hz:q:dB) ; its ring ; dB on 'room'. "" = v23.
ROOM = os.environ.get("C10T6_ROOM", "-11dB;-14dB;again,top,down;-9.925;0,-2,0,-2.5,-6,-3.5,-3,0;190/330:0.9:-7/2600:0.6:7;0.5;4") if WITH and LAST_TOUCH and FIVE and LOCK and UP and KEYS else ""
ROOM_PARTS = set(ROOM.split(";")[2].split(",")) if ROOM else set()
# v25 (chirper-three; section round, w3 0:55.7-1:23.5: 'eight'): THE LEFT HAND GOES ON THROUGH THE LONGEST LAP
# (Harry, 19 Nov 02:25: "Keep one guitar with the keys"). v23 built his answer in 'two' and 'four'. The exchange's
# longest lap, the seven seconds of 'eight' at 1:02.6 where the riff is eight half bars long, still lost both
# guitars. Now the left guitar plays on through it: the 32 strokes the rule writes there, which v9 took out. The
# right guitar still leaves, and comes back before the wall on the three accents that the lap's second half moves
# (v16's: 1:07.4, 1:08.6, 1:09.0): its own strokes there and nothing else. The cadence the second pair marked in
# the lap before is pointed at again from the right, over a left hand that has not stopped. With a guitar under
# them the keys lost 1.9 dB of their place and the chip's two voices 2.3 (raw, K), so the keys' two notes are
# 2 dB up and the chip's second voice 3: the keys stand where they did, the chip 1.2 dB under.
# which guitar stays through eight's lap of the keys (l or r) ; how the other comes back ("moved" = on the three
# accents the lap's second half moves ; "" = at the wall, as before) ; dB on the keys' two notes there ; the
# song's loudness target ; dB on the chip's second voice (it plays only in that lap). "" = v24.
EIGHT = os.environ.get("C10T6_EIGHT", "l;moved;2;-9.868;3") if ROOM else ""
# v26 (chirper-alpha; section round, w4 1:23.5-1:51, and on to the end of the second wall at 1:58.3): A HAIR UNDER.
# What this rule is known for has not been said in the song: start it twice from almost the same number and, where
# it repeats, nothing comes of the difference; where it does not, the two are soon strangers. This window holds one
# of each, the lock on five (1:27) and the second wall (1:44.3). So from the lock the chip's tune has a SECOND VOICE:
# the rule again, started five thousandths under the tune's own number and never reset (like the tune it has no
# notes in the song: it is the engine's generator, with a different x0). What the rule does with it, computed:
#   - in the lock it plays the five with the tune, note for note, once round; the second time its last note is a
#     step under the tune's (F under G). It has fallen onto a five of its own, one note different.
#   - (through the two sung laps both chips rest, as the tune has since v24);
#   - at the wall the two start together, four notes in unison; then the second voice goes on saying the five for
#     four half bars while the tune does not, then runs the tune's own figure two half bars ahead of it, and ends
#     on one note three times (it has come close to the rule's resting number, 0.737, and a number that close
#     stays a while before it is thrown off).
# A FINDING, in the arithmetic and not put there: the five the song has played since v1 is the rule's UNSTABLE
# five. At this dial setting there are two five-cycles side by side (the window has only just opened); the song's
# number sits on the one that repels (anything near it moves away 2.7 times a lap; the tune itself drifts 0.0017
# in four laps and the dial moves on before it shows), and the second voice, a hair under, falls onto the one
# that holds (0.674 a lap), whose last note is that step lower. A hair OVER the tune's number plays the five once
# and then wanders for the rest of the lock: so the hair goes under.
# how far from the tune's number the second voice starts at the lock ; its gain ; its pan ; the song's loudness
# target ("" = unchanged). "" = v25.
# (Level, benched raw: at the tune's own fader, -18 dB, and off to the right; at -20 it stood 3.9 dB under the tune
# and 17 to 18 under the band, K-weighted, where the tune stands 13 to 14 under.)
HAIR = os.environ.get("C10T6_HAIR", "-0.005;-18dB;0.45;-9.84") if EIGHT else ""
# v27 (chirper-two; section round, w5 1:51.3-2:19.1, and on to the top at 2:24.3): THE STRANGER COMES HOME, A STEP
# AHEAD. v26 started the rule twice, a hair apart, and by the end of the second wall the two were strangers; there
# the second voice stopped. It is the other half of what the rule is known for that had not been said: a window
# that repeats CATCHES whatever comes into it. So the second voice does not stop at 1:58.3. It walks on, never
# reset, from wherever the wall left it (0.725, where the tune is at 0.775), into the window of three. Computed,
# and nothing in it is put there:
#   - the tune locks at once (the dial was set for the tune's number). The second voice does not: for twelve half
#     bars it circles the three and misses, Db6 B5 D6, B5 Ab6 D5, Db6 F6 G5, G6 D5 Db6, against the tune's
#     Ab6 Db5 Ab5. Its high note comes a half bar AFTER the tune's (2:01.7, 2:04.3), then WITH it and a semitone
#     under (2:06.1); for three half bars running it is a semitone off the tune (2:05.2, 2:06.1, 2:07.0). Once
#     it is near, what is off shrinks by 0.56 a lap, on alternate sides;
#   - (through the two sung laps both chips rest, as they have since v24 and v26; it locks there, unheard, at 2:10.4);
#   - at the six (2:13.9) it comes back, and it is HOME: the tune's own three notes, one half bar AHEAD of the
#     tune. Db5 Bb5 Ab6, then Db5 Ab5 Ab6 three times, against Ab6 Db5 Ab5: a round, in fifths and octaves (the
#     one note still out, Bb5 for Ab5 at 2:14.8, a sixth, is the last to come in). Its Ab6 falls on the half bar BEFORE
#     each of the band's screams (2:15.7, 2:18.3, 2:20.9), and the last of them, 2:23.5, is the pick-up into the
#     top. The rule decides the phase, not the song: the same tune, but nobody chose which step it would be on.
# So the window holds the whole of it: two strangers in the wall, one home and one circling, the singers, a round.
# MEASURED (raw, seed 0; home.py reads the notes back from the audio: they are the computed ones). The second
# voice stands 13.0 to 17.8 dB under everything else, half bar by half bar (K), the tune 10.4 to 15.2; it is 1.9
# dB under the tune in the three and in the six, as v26 set it in the wall. In the finished file every section
# before 1:58.3 and from 2:24.8 on is within 0.02 dB of v26; the target is not moved.
# the section at which the second voice stops (it walks on from the wall, never reset) ; sections in which it walks
# but is not heard ; the song's loudness target ("" = unchanged). "" = v26.
HOME = os.environ.get("C10T6_HOME", "full;;") if HAIR else ""
# v28 (chirper-alpha; section round, w7 2:46-3:14): TWO VOICES BECOME ONE. v26: started a hair apart, where the rule
# does not repeat the two are soon strangers. v27: a window that repeats catches whatever comes into it, on some
# step of its round. What was left (chirper-two computed it and left it for the song's last minute): where the
# rule SETTLES, two starts end as one voice. The second voice walks on from where v27 stops it, unheard, through
# the top. Computed, and nothing in it is put there (what each plays in a half bar is the number after the step):
#   - in the top the two are strangers, meet by chance at 2:40.0 (0.00007 apart) and, the top being what it is,
#     are apart again ten half bars later;
#   - 2:48.7, where it is heard again: G5 under the tune's A flat 5, A flat 6 under its B flat 6, B5 over its
#     B flat 5 (a semitone, a tone, a semitone), and both land on the top's last note, B6 (2:51.3);
#   - on the way down the tune goes alone for two notes (the second voice's number is under the rest line), the
#     second voice has one last note of its own (A flat 4 under B flat 5, 2:54.8), and from 2:55.7 it plays the
#     tune's note in every half bar to the end of the song: one voice (0.00045 apart there, nothing by 3:02).
# Once it is the tune it is taken in: its fader falls from 6 dB under where it was to 20 under by the end of the
# four (3:06.1), where it stops; the song's last minute is the tune alone, as it was.
# the section at which the second voice stops ; the half bar of the top from which it is heard again (it walks on,
# unheard, from where HOME leaves it) ; dB on its fader where it becomes the tune : where it stops ; the loudness
# target ("" = unchanged). "" = v27.
ONE = os.environ.get("C10T6_ONE", "down-two;28;-6:-20;") if HOME else ""
# v29 (chirper-two; drawn as a whole-song round, on the sung voice, which three handoffs name as the next thing
# here; what is kept is 1:35.7-1:44.3, the two sung laps of the lock on five): "MAKE SOME ROOM" CAN BE MADE OUT.
# The read against the records (v27, v28) has the sung laps 5 to 10 dB over at 250-500 Hz and 5 to 9 under at
# 2-4 kHz. WHAT THE SINGERS ARE (tools/voxref.py, each line alone against the records' vocal stems, v28):
# "make some room" is within 2.4 dB of them from 500 Hz to 4 kHz and 6 over at 250-500; "no more room" is three
# dark vowels between nasals, 12 to 14 dB short at 1-2 kHz and 20 short at 2-4 kHz. And a sung lap weighs what
# the band's lap before it does (v24's rule), so the voice carries the lap, by its body.
# TRIED ON EVERY LINE, AND NOT KEPT THERE:
#   the singer's own controls (ring, effort, a smaller tract, rasp): the dark lines' top moves 2 to 3 dB.
#   eq at the same lap loudness: 1.3 to 2.9 dB off 250-500 Hz and nothing else (take the body out and the fader
#     has to put it back); a lift at 1.3 kHz made 500 Hz-1 kHz worse.
#   AN EDGE: each singer's body (200-700 Hz) driven hard on a bus of its own and only 1.8-3.5 kHz of that kept:
#     upper harmonics made from the voice itself. On every line the read came right (the three's sung laps:
#     250-500 Hz +5.1 -> +1.8, 2-4 kHz -9.4 -> -2.5), but on the dark lines the edge was as loud as the voice
#     (1 dB under, K): they have no top of their own for it to lean on, and it is a buzz with no vowel in it.
#     Alone, a recogniser that read 19 of the nine lines' 25 words on v28 read 10 and 12 on two builds ("No, no
#     room", "They said No"), and the score fell 4.6 and 3.9.
# KEPT: the edge and a leaner eq where the line has consonants and bright vowels for it to sit behind: "make some
# room", both times. The two laps' ten and five notes move to a pair of tracks of their own (the same singers, the
# same notes): hp 220, 9 dB out at 330 Hz, a low shelf of -6 dB at 800 Hz (v24's 7 dB lift at 2.6 kHz is not
# needed: the edge is there), the edge 6 to 7 dB under the voice (K), the faders 3.6 dB up so that the laps weigh
# what they did (as mastered, two seeds: -0.3 to +0.3 dB). Every other sung line is v28's, sample for sample
# before the master.
# IN THOSE TWO LAPS, the mix against the records: 250-500 Hz +7.2 -> +4.2, 500 Hz-1 kHz +2.4 -> +1.1, 2-4 kHz
# -1.7 -> -0.3 (1-2 kHz +2.8 -> +3.1). ALONE, the recogniser wrote "Makes a broom. Makes a broom." on v28 and on
# every build without the edge or with a weaker one (nine), and "Make some room. Make some room." on every build
# with it at this strength (five, this one among them): 25 of the nine lines' 25 words now, where v28 read 19.
# the lines' eq (engine bands, | between) ; dB on both singers' faders for them ; the loudness target ('' =
# unchanged) ; dB on each line (five once, again ; three once, again ; the top ; four, two, one), added to v24's ;
# WHICH LINES: the half bars of the lock on five they start in, first-last ; THE EDGE ('' = none): the band of the
# voice it is made from, Hz : how hard that is driven (0..1) : its bias : the band kept of it (high-pass xN - low-pass
# xM) : how much of it is added, dB. "" = v28.
BODY = os.environ.get("C10T6_BODY", "hp cutoff=220|peak cutoff=330 q=0.9 gain=-9dB|lowshelf cutoff=800 gain=-6dB;3.6;;0.8,-0.1,0,0,0,0,0,0;10-20;200-700:0.82:0.3:1800x2-3500x2:-7") if ONE and ROOM else ""
EDGE = BODY.split(";")[5] if BODY else ""
MAKE_SOME_ROOM = (["M EY1 K", "_", "S AH1 M", "R UW1 M", "_"], [3, 8, 13, 18, 24], [.94, .88, .90, .95, .90])
NO_MORE_ROOM = (["N OW1", "M AO1 R", "R UW1 M"], [4, 6, 14], [.90, .92, .95])


def sung(c, key=None):
    """The accent's note at half bar c, folded into one singer's octave (G3 to G flat 4), in the key of half bar `key`."""
    return 55 + (note(cell(CELLS[c][3])[2]) + gup(c if key is None else key) - 55) % 12


def room_lines():
    """-> [(first half bar, half bars, [(place, syllable, velocity, pitch)], singers, what the guitars do)]."""
    if not ROOM:
        return []
    five = lambda a: [(s, ph, v, sung(a + j)) for j, (ph, s, v) in enumerate(zip(*MAKE_SOME_ROOM))]
    three = lambda a, src, last=None: [(last if last and j == 2 else s, ph, v, sung(src + j, a)) for j, (ph, s, v) in enumerate(zip(*NO_MORE_ROOM))]
    on = lambda a, words: [(6 * j, ph, .93, sung(a + j)) for j, ph in enumerate(words)]       # a syllable to the half bar, on its first beat
    trim = [float(v) for v in ROOM.split(";")[4].split(",")]      # five once, again ; three once, again ; the top ; four, two, one
    if BODY and BODY.split(";")[3]:                               # v29: each line weighs what it did with the new chain
        trim = [round(a + float(b), 2) for a, b in zip(trim, BODY.split(";")[3].split(","))]
    once = "out" if "again" in ROOM_PARTS else "leave"            # the guitars' cue back in comes after the last sung lap
    lines = [(HEAD5 + 10, 5, five(HEAD5 + 10), 1, once, trim[0]), (HEAD3 + 9, 3, three(HEAD3 + 9, HEAD3 + 9), 1, once, trim[2])]
    if "again" in ROOM_PARTS:
        lines += [(HEAD5 + 15, 5, five(HEAD5 + 15), 2, "leave", trim[1]), (HEAD3 + 12, 3, three(HEAD3 + 12, HEAD3 + 12), 2, "leave", trim[3])]
    if "top" in ROOM_PARTS:
        empty = lambda c: not cell(CELLS[c][3])[0]
        holes = [c for c in range(AT["full"] + 1, AT["down-four"] - 3)
                 if all(empty(c + i) for i in range(3)) and not empty(c - 1) and not empty(c + 3)]
        assert len(holes) == 2, holes
        # (in the hole there is no accent for 'room' to wait for: it comes on the beat and has the rest of the hole)
        lines += [(c, 3, three(c, HEAD3, 12), 2, "hole", trim[4]) for c in holes]
    if "down" in ROOM_PARTS:
        four, two, one = HEAD4D + 4, AT["down-two"] + 6, AT["down-one"] + 8
        lines += [(four, 4, on(four, ["M EY1 K", "S AH1 M", "M AO1 R", "R UW1 M"]), 1, "hole", trim[5]),
                  (two, 2, on(two, ["M AO1 R", "R UW1 M"]), 1, "hole", trim[6]),
                  (one, 2, on(one, ["R UW1 M"]), 1, "hole", trim[7])]
    return sorted(lines)


ROOM_CELLS = {c for first, n, *_ in room_lines() for c in range(first, first + n)}


def sing_room():
    lift = float(ROOM.split(";")[7]) if ROOM.split(";")[7:] else 0
    for first, n, words, singers, guitars, trim in room_lines():
        for j, (at, ph, v, p) in enumerate(words):
            stop = words[j + 1][0] if j + 1 < len(words) else n * 6 - .35
            gain = trim + (lift if ph == "R UW1 M" else 0)              # 'room' is the word, and 'oo' is this voice's quietest vowel
            apart = ""
            if BODY:                                                    # v29: the lines that get the new chain, on a pair of their own
                a, b = (AT["five"] + int(v) for v in BODY.split(";")[4].split("-"))
                apart = "-e" if a <= first < b else ""
            for tr, up in (("room" + apart, 0), ("room2" + apart, 3))[:singers]:   # the second singer two rungs up: always a minor third
                add(tr, first, at, (stop - at) / .96, p + up, v)
                T[tr][-1]["ph"] = ph
                if gain:
                    T[tr][-1]["gain"] = f"{gain:g}dB"
        inside = lambda e: first * 2 <= e["at"] < (first + n) * 2
        if guitars in ("leave", "out"):
            # (chirper-alpha's trial.) The bass and both kits keep every place. The guitars make room: the first pair
            # keeps only its last fretted accent, as the cue back in ("leave"; none while another sung lap follows:
            # "out"); the second pair waits until the line is over; the chip's answer leaves its space to 'more'.
            for tr in G:
                T[tr] = [e for e in T[tr] if not (inside(e) and (guitars == "out" or e.get("expr", {}).get("pm") or e["at"] < (first + n - 1) * 2))]
            for tr in G2 + ("echo",):
                T[tr] = [e for e in T.get(tr, []) if not inside(e)]


def room_is_there():
    """The lines in the holes and on the keys' laps take nobody's place: no guitar plays under them."""
    for first, n, words, _, guitars, _ in room_lines():
        if guitars == "hole":
            a, b = first * 2 + words[0][0] / 3 - 1e-6, (first + n) * 2 - 1e-6
            assert not [e for tr in G + G2 + G3 for e in T.get(tr, []) if a <= e["at"] < b], (first, "a guitar plays under the line")


def wobble_before_the_doubling():
    a, b = AT["one"], AT["two"]
    accent, whole = (a + int(v) for v in FLIP.split(";")[:2])
    assert a < accent <= whole < b
    for c in range(accent, b):
        resting = G[1 - (c - accent) % 2]                    # the left guitar has the first one
        mine = lambda n: 2 * c - 1e-6 <= n["at"] < 2 * c + 2 - 1e-6
        if c >= whole:
            T[resting] = [n for n in T[resting] if not mine(n)]
        else:
            T[resting] = [n for n in T[resting] if not (mine(n) and "expr" not in n)]     # the chugs carry expr.pm


def the_wobble_dies_away():
    a = AT["down-one"]
    whole, accent = (int(v) for v in SETTLE.split(";")[:2])
    under = G[1] if SETTLE.split(";")[2] == "r" else G[0]
    assert all(any(2 * c <= n["at"] < 2 * c + 2 for n in T[tr]) for tr in G for c in range(a, a + whole + accent)), "both guitars must be playing there"
    for c in range(a, a + whole + accent):
        _, rate, _, x = CELLS[c]
        side = under if x < 1 - 1 / rate else G[1 - G.index(under)]      # which side of its resting point the count is on
        resting = G[1 - G.index(side)]
        mine = lambda n: 2 * c - 1e-6 <= n["at"] < 2 * c + 2 - 1e-6
        if c < a + whole:
            T[resting] = [n for n in T[resting] if not mine(n)]
        else:
            T[resting] = [n for n in T[resting] if not (mine(n) and "expr" not in n)]     # the chugs carry expr.pm


def crash_and_regrowth():
    v0, v1 = (float(v) for v in TOMS.split(";")[1:3])
    a, z = AT["full"], AT["down-four"]
    struck = lambda c: sorted(n["at"] for n in T["dkick"] if c * 2 <= n["at"] < c * 2 + 2)
    hands = {n["at"] for tr in ("dsnare", "dcym") for n in T[tr]}
    holes, growths, c = [], [], a
    while c < z:
        if struck(c):
            c += 1
            continue
        h0 = c
        while c < z and not struck(c):
            c += 1
        holes.append((h0, c))
        g0 = c
        while c < z and len(struck(c)) < 6:          # up to the next scream, which is all six places
            c += 1
        growths.append((g0, c))
    assert [h1 - h0 for h0, h1 in holes] == [3, 2, 2, 3], holes
    T["dsnare"] = [n for n in T["dsnare"] if not any(h0 * 2 <= n["at"] < h1 * 2 for h0, h1 in holes)]
    for g0, g1 in growths:
        strokes = sorted(n["at"] for n in T["dkick"] if g0 * 2 <= n["at"] < g1 * 2 and n["at"] not in hands)
        if len(strokes) < 2:                         # the last time it is back in one step: nothing to climb
            continue
        assert not [n for n in T["dtoms"] if g0 * 2 <= n["at"] < g1 * 2]
        for i, at in enumerate(strokes):
            T["dtoms"].append({"at": at, "len": 0.25, "pitch": ("ft", "t2", "t1")[i * 3 // len(strokes)],
                               "vel": round(v0 + (v1 - v0) * i / (len(strokes) - 1), 3),
                               **({"gain": f"{float(REGROW):g}dB"} if float(REGROW) else {})})


def last_string():
    """Use alternate sides of the fixed point, then the last occupied cells."""
    out = AT["out"]
    tines = {n["at"]: n for n in T["tine-high"]}
    take = set()
    for c in range(AT["down-one"], out):
        _, rate, _, x = CELLS[c]
        if x >= 1 - 1 / rate:
            continue
        slots, ai, r = cell(x)
        if not slots:
            continue
        hit = slots[ai]
        at = round(2 * c + hit / 3, 5)
        p = note(r) + gup(c)
        # Below equilibrium the fourth harmonic takes the fretted accent,
        # or (in the piano exchange) the same note the key was sounding.
        if at in tines:
            assert tines[at]["pitch"] == nm(p + 24)
            T["touch"].append({**tines[at], "pitch": nm(p), "vel": .93, "expr": {"node": 4., "contact": 1.}})
        else:
            stop = slots[ai + 1] if ai + 1 < len(slots) else len(PRI)
            add("touch", c, hit, stop - hit - .12, p, .93, node=4, contact=1)
        take.add(at)
    for tr in ("tine-high", *G):
        T[tr] = [n for n in T[tr] if n["at"] not in take]

    opening = [n for n in T["touch"] if n["at"] < 2 * AT["one"]]
    closing = [(c, x) for c, (_, _, _, x) in enumerate(CELLS) if c >= out and len(cell(x)[0]) == 1]
    gates = {}
    for i, ((c, x), memory) in enumerate(zip(closing, opening)):
        slots, ai, _ = cell(x)
        at = round(2 * c + slots[ai] / 3, 5)
        # The opening accents receded into a growing band. Pick the first
        # out over the heavy string, touch the last one lightly.
        gain = 6 - 8 * i / max(1, len(closing) - 1)
        T["touch"].append({**memory, "at": at, "gain": f"{gain:g}dB"})
        # All three cells have one occupied place, but the amount above that
        # threshold is draining away. It sets the left guitar's gate only.
        frac = (len(PRI) + 1) * x - len(slots)
        gates[at] = round((1 + (len(PRI) - 1) * frac) / 3 * .96, 5)
    T["gr"] = [n for n in T["gr"] if n["at"] not in gates]
    # With less than two slots of gesture, leave the low note to bass and
    # machine. Neither the three footfalls nor the empty last cell is edited.
    T["gl"] = [dict(n, len=min(n["len"], gates[n["at"]])) if n["at"] in gates else n for n in T["gl"]
               if n["at"] not in gates or gates[n["at"]] >= 2 * .96 / 3]


def song():
    compose()
    if ROOM:
        sing_room()
    if FLIP:
        wobble_before_the_doubling()
    if CREST:
        crest_lines()
    if SIX:
        third_pair()        # after the crests: it follows the first pair as they left it
    if GROWTH_TOUCH:
        growth_harmonics()
    if AHEAD:
        know_the_way()      # before the keys take their laps: those stay as they were
    if TINES:
        periodic_tines()
    if LAST_TOUCH:
        last_string()
    if SETTLE:
        the_wobble_dies_away()      # after the last string: under the resting point the accent is already the clean guitar's
    moved = moved_accents() if MOVED else []
    if KIT:
        kit_part()
        T["dcym"] += [{"at": at, "len": 2.0, "pitch": "x", "vel": float(MOVED.split(";")[0])} for at in moved]
        if TOMS:
            hand_on_the_dial()
        if REGROW:
            crash_and_regrowth()
    kt = KIT.split(";") if KIT else None
    kit = "cc-machine"
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    gens = [g for g in lead_gens() if g[2] in LEAD]
    lead_at = gens[0][0]
    assert all(a[0] + a[1] == b[0] for a, b in zip(gens, gens[1:])), "the lead's runs must follow one another"
    tracks = [
        {"name": "gl", "patch": main.format(30), "gain": "0.8dB", "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(31), "gain": "0.8dB", "pan": 1, "out": "gtrs", **mids},
        {"name": "gl2", "patch": dbl.format(32), "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **mids},
        {"name": "gr2", "patch": dbl.format(33), "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **mids},
        *([{"name": tr, "patch": SIX.split(";")[0].format(cone), "gain": SIX.split(";")[1], "pan": side * float(SIX.split(";")[2]), "out": "gtrs", **mids}
           for tr, cone, side in zip(G3, SIX.split(";")[3].split(","), (-1, 1))] if SIX else []),
        {"name": "lead", "patch": "nes-pulse-lead", "gain": os.environ.get("C10T6_LEAD", "-18dB"), "pan": 0, "at": f"{lead_at * 2}b",
         "sends": {"hall": "-12dB"}, "gen": [g[3] for g in gens]},
        *([{"name": "echo", "patch": "nes-pulse-lead layers.0.chip.duty=0.125", "gain": LOCK.split(";")[2], "pan": float(LOCK.split(";")[4]),
            "sends": {"hall": "-12dB"}}] if LOCK else []),
        *([{"name": "lead2", "patch": "nes-pulse-lead", "gain": f"{float(UP.split(';')[4][:-2]) + float(EIGHT.split(';')[4]):g}dB" if EIGHT and float(EIGHT.split(";")[4]) else UP.split(";")[4], "pan": float(UP.split(";")[5]), "at": f"{second_voice()[0] * 2}b",
            "sends": {"hall": "-12dB"}, "gen": [second_voice()[1]]}] if UP else []),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "boom", "patch": kit, "gain": os.environ.get("C10T6_BOOM", "0dB"), "out": "drums"},
        {"name": "kick", "patch": kit, "gain": os.environ.get("C10T6_KICK", "0dB"), "out": "drums"},
        {"name": "snare", "patch": kit, "gain": os.environ.get("C10T6_SNARE", "0dB"), "out": "drums", "sends": {"hall": "-18dB"},
         "fx": [{"type": "eq", "bands": ["peak cutoff=350 q=1 gain=-5dB"]}]},      # its second oscillator sits in the guitars' low mids
        {"name": "cym", "patch": kit, "gain": os.environ.get("C10T6_CYM", "0dB"), "out": "drums"},
        {"name": "hat", "patch": kit, "gain": os.environ.get("C10T6_HAT", "0dB"), "out": "drums"},
        *([{"name": "dkick", "patch": "ct-kit-here", "gain": kt[0], "out": "kit",
            "fx": [{"type": "eq", "bands": [f"hp cutoff={kt[3]}", f"peak cutoff=4500 q=0.8 gain={kt[7]}dB"]}]},
           {"name": "dsnare", "patch": "ct-kit-here", "gain": kt[1], "out": "kit", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
            "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"] + (["peak cutoff={} q={} gain={}dB".format(*kt[9].split(":"))] if kt[9:] and kt[9] else [])}]},
           {"name": "dcym", "patch": "ct-kit-here", "gain": kt[2], "out": "kit", "sends": {"oh": "4.5dB"},
            "fx": [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]}] if KIT else []),
    ]
    if GROWTH_TOUCH:
        tracks.append({'name':'touch', 'pan':.52, 'gain':GROWTH_TOUCH,
                       'patch':'ct-clean synth.layers.0.node=expr.node synth.layers.0.pinch=expr.contact '
                               'synth.layers.0.pickup=0.075 synth.layers.0.soft=1 synth.layers.0.choke=55ms '
                               'synth.amp.r=45ms play.gate=1 fx.3.mix=0'})
    if TINES:
        patch = "rhodes synth.amp.s=0.35 synth.amp.r=90ms fx.2.mix=0.04"
        high, low = (float(v) for v in TINES.split(";"))
        for name, gain, pan in (("high", high, .32), ("low", low, -.32)):
            tracks.append({"name": "tine-" + name, "patch": patch, "gain": f"{gain:g}dB",
                           "pan": pan, "fx": ["hp cutoff=120"]})
    if TOMS:
        tracks.append({"name": "dtoms", "patch": "ct-kit-here", "gain": TOMS.split(";")[0], "out": "kit", "sends": {"oh": "-1.5dB"}})
    if ROOM:
        room_is_there()
        voice = ("voice-near synth.layers.0.tract={} synth.layers.0.breath.value=0.13 synth.layers.0.effort.value=0.55 "
                 "synth.layers.0.diction=3 synth.layers.0.inhale=0.1 play.glide=35ms"
                 + (f" synth.layers.0.ring={ROOM.split(';')[6]}" if ROOM.split(";")[6:] and ROOM.split(";")[6] else ""))
        hp, *peaks = ROOM.split(";")[5].split("/") if ROOM.split(";")[5:] and ROOM.split(";")[5] else ("", )
        tone = ([{"type": "eq", "bands": [f"hp cutoff={hp}"] + ["peak cutoff={} q={} gain={}dB".format(*b.split(":")) for b in peaks]}]
                if hp else ["hp cutoff=150 q=0.7"])
        tracks.append({"name": "room", "patch": voice.format(1.04), "gain": ROOM.split(";")[0], "pan": 0, "fx": tone})
        if "room2" in T:
            tracks.append({"name": "room2", "patch": voice.format(0.98), "gain": ROOM.split(";")[1], "pan": 0.25, "fx": tone})
    if HAIR:
        tracks.append({"name": "hair", "patch": "nes-pulse-lead", "gain": HAIR.split(";")[1], "pan": float(HAIR.split(";")[2]),
                       "at": f"{AT['five'] * 2}b", "sends": {"hall": "-12dB"}, "gen": hair_gens()})
        if ONE and ONE.split(";")[2]:
            # once it is the tune it is taken in: its fader falls from the half bar the two become one to where it stops
            a, z = (float(v) for v in ONE.split(";")[2].split(":"))
            met, end = (one_voice() - AT["five"]) * 2, (AT[ONE.split(";")[0]] - AT["five"]) * 2      # a lane's beats count from the track's `at`
            tracks[-1]["gain"] = {"value": HAIR.split(";")[1], "mod": [{"src": "auto.melt", "amount": 1}]}
            tracks[-1]["auto"] = {"melt": {"points": [["0b", 0], [f"{met - 0.02:g}b", 0], [f"{met}b", a], [f"{end}b", z]], "curve": 0}}
    if BODY:    # v29: the same two singers on a second pair of tracks, for the lines named: their own eq, and a send
        e = BODY.split(";")     # each to a bus that makes upper harmonics out of the voice's body
        tone = [{"type": "eq", "bands": e[0].split("|")}]
        fader = lambda g: f"{float(g[:-2]) + float(e[1]):g}dB"
        tracks.append({"name": "room-e", "patch": voice.format(1.04), "gain": fader(ROOM.split(";")[0]), "pan": 0, "fx": tone,
                       **({"sends": {"edge": "0dB"}} if EDGE else {})})
        if "room2-e" in T:
            tracks.append({"name": "room2-e", "patch": voice.format(0.98), "gain": fader(ROOM.split(";")[1]), "pan": 0.25, "fx": tone,
                           **({"sends": {"edge2": "0dB"}} if EDGE else {})})
    for t in tracks:
        if "gen" not in t:
            t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    long_amp = {"a": "0.1ms", "d": "6s", "s": 1, "r": "2.5s"}

    def piece(part, pitch, gain, pan=0.0, choke=None, **m):
        p = {"pitch": pitch, "gain": gain, "pan": pan, "patch": {"synth": {"amp": long_amp, "layers": [{"type": "machine", "machine": {"part": part, **m}}]}}}
        if choke:
            p["choke"] = choke
        return p

    KG = os.environ.get("C10T6_K", f"{-14 + float(kt[4]):g}dB" if KIT else "-14dB")
    machine = {
        "about": ("Carrying Capacity's drum machine (chirper-zero, 16 Nov): the engine's `machine` voices, the first on this record. "
                  "k a 909-style kick resting on the song's E with its click up; s the two-oscillator snare; p the clap; "
                  "b the 808's long boom on E; "
                  "h and o the six-square hat, closed and open (they choke each other); c the cymbal."),
        "play": {"len": "/16", "vel_sens": 0.5},
        "kit": {
            "k": piece("kick", "E1", KG, click=0.8, drive=0.35, decay="180ms"),
            "s": piece("snare", "G3", os.environ.get("C10T6_S", f"{-5.5 + float(kt[5]):g}dB" if KIT else "-5.5dB"), snappy=0.5, drive=0.2),
            "p": piece("clap", "C4", os.environ.get("C10T6_P", "0dB")),
            "b": piece("boom", "E1", os.environ.get("C10T6_B", "-5dB"), decay="5s", drive=0.5),
            "h": piece("hat", "C6", os.environ.get("C10T6_H", "0dB"), pan=-0.3, choke="hat"),
            "o": piece("hat", "C6", os.environ.get("C10T6_O", "-3dB" if TELL else "0dB"), pan=-0.3, choke="hat", decay="380ms"),   # v3: open on every beat of the news: 3 dB down
            "c": piece("cymbal", "C6", os.environ.get("C10T6_C", f"{-6 + float(kt[8]):g}dB" if KIT else "-6dB"), pan=0.3),
            **({f"k{i + 1}": piece("kick", TUNE.split(";")[i], KG, click=0.8, drive=0.35, decay="180ms") for i in range(3)} if TUNE else {}),
            **({"b3": piece("boom", TUNE.split(";")[3], os.environ.get("C10T6_B", "-5dB"), decay="5s", drive=0.5)} if TUNE else {}),
        },
    }
    return {
        "about": ("chirpers X (Common Time), track 6 by chirper-zero: Carrying Capacity. No riff was written. There is one rule, "
                  "x <- r x (1 - x), applied once every half bar, and the number it gives is the half bar: how many of its six "
                  "places the band strikes, where the accent falls and how high. The form is the dial r turned up from 1.5 to 4 "
                  "and back down: the riff settles, splits in two, four, eight, stops repeating, locks by itself on five half "
                  "bars and then on three, fills the whole range, and dies out. Triplets at 138, on E, with a drum machine; "
                  "the lead has no notes, only the rule (the engine's own logistic generator). v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(BODY.split(";")[2]) if BODY and BODY.split(";")[2] else float(ONE.split(";")[3]) if ONE and ONE.split(";")[3] else float(HOME.split(";")[2]) if HOME and HOME.split(";")[2] else float(HAIR.split(";")[3]) if HAIR and HAIR.split(";")[3] else float(EIGHT.split(";")[3]) if EIGHT else float(ROOM.split(";")[3]) if ROOM else float(WITH.split(";")[2]) if WITH else float(SETTLE.split(";")[3]) if SETTLE else float(FLIP.split(";")[2]) if FLIP else float(UNWIND.split(";")[3]) if UNWIND else float(SIX.split(";")[4]) if SIX else -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"cc-machine": machine,
                    **({"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}}} if KIT else {})},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": [{"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            # ct-bass's bus, as on the other songs, with its bands moved down a semitone to E
            "low": low_bus(),
            # v8: the record's kit, on the other songs' drum bus, room and overheads
            **({"kit": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                               {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                               "clip drive=0dB ceiling=-13dB",
                               {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", f"highshelf cutoff=9000 gain={kt[10] if kt[10:] else -2}dB", "lp cutoff=14250 q=0.8"]}]},
                "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
                "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]}} if KIT else {}),
            **(edge_buses() if EDGE else {}),
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T6_MASTER", "2.7dB")}]},
        "tracks": tracks,
    }


def edge_buses():
    """v29: one bus a singer (two voices through one would beat against each other in it): the voice's body, driven
    hard, and only the band over it kept."""
    band, drive, bias, kept, added = EDGE.split(":")
    lo, hi = band.split("-")
    out, lp = kept.split("-")
    hp, _, n = out.partition("x")
    lp, _, m = lp.partition("x")
    bus = {"fx": [{"type": "eq", "bands": [f"hp cutoff={lo}", f"lp cutoff={hi}"]},
                  {"type": "drive", "drive": float(drive), "bias": float(bias)},
                  {"type": "eq", "bands": [f"hp cutoff={hp}"] * int(n or 1) + [f"lp cutoff={lp}"] * int(m or 1)},
                  {"type": "gain", "gain": f"{added}dB"}]}
    return {"edge": bus, **({"edge2": json.loads(json.dumps(bus))} if "room2-e" in T else {})}


# v30 (chirper-alpha; whole song, 0:27.8-3:16): THE RULE IS HEARD. The chip tune is the rule said plainly, one note for
# each half bar's number, and three rounds built on it (v26, v27, v28). Its fader was set in v1 (-18 dB) and never read.
# Read raw, the tune alone against everything else: 12.4 to 16.4 dB under the band (K) in every section, and in the
# third-octave round its own note a median 0.6 to 2.7 dB UNDER everything else there (the edge of being heard, for the
# whole song); at the top 6.1 under, 20 of its 26 notes at -4 or lower: not heard, in the song's climax. So:
#   - the three chips that are the rule (lead, lead2, hair) come up 3 dB in every half bar where a guitar plays and 7
#     through the top, on a lane stepped at the half bars; where the guitars rest (the keys' laps, the sung laps, the
#     holes) they stay where they were, because there they were already heard. The answers (echo) are not touched.
#   - the second voice is heard from the top's FIRST bar (v28: only from its last four half bars), so the top says the
#     whole of it: two strangers (2:24.3-2:39.1; at 2:33.9 and 2:34.8 it sings alone into the rule's hole), the chance
#     meeting (2:40.0-2:45.2: one line; the second voice 6 dB down while it is the tune's own note), the parting
#     (2:48.7, v28) and one voice (2:55.7, v28).
# After: the tune 9.4 to 13.4 under the band, 8.7 at the top; its median note -0.6 to +2.3 against everything else in
# its third-octave, 0.0 at the top (2 of 26 at -4 or lower). First take, not kept: 4 and 8-9 dB with the answers too
# (the two chips only 3 to 5 dB under the whole band at the top). The target is not moved: the band gives 0.16 to 0.31 dB.
# dB on the chips wherever a guitar is playing ; dB more through the top ; the chips ; the loudness target ("" =
# unchanged) ; the half bar of the top from which the second voice is heard ("" = ONE's own, 28) ; dB on the second
# voice in the half bars of the top where it plays the tune's own note (the chance meeting). "" = v29.
HEARD = os.environ.get("C10T6_HEARD", "3;4;lead,lead2,hair;;0;-6") if BODY else ""


def the_rule_is_heard(doc, less=0., less_top=0.):
    """The chips come forward wherever a guitar is playing (most at the top), and stay where they were in every hole.
    `less`, `less_top` (v31): dB of that lift given back, away from the top and at it."""
    base, top, chips, target, since, met = HEARD.split(";")
    if less or less_top:
        base, top = float(base) - less, float(top) + less - less_top
    by = {t["name"]: t for t in doc["tracks"]}
    n = sum(d[1] for d in DIAL)
    busy = [False] * (n + 1)
    for g in ("gl", "gr", "gl2", "gr2", "gl3", "gr3"):
        for note_ in by.get(g, {}).get("notes") or []:
            for h in range(int(note_["at"] // 2), int((note_["at"] + note_["len"] - 1e-6) // 2) + 1):
                busy[min(h, n)] = True
    up = [(float(base) + (float(top) if AT["full"] <= h < AT["down-four"] else 0)) if busy[h] else 0. for h in range(n + 1)]
    for name in chips.split(","):
        t = by.get(name)
        if t is None:
            continue
        at = float(str(t.get("at", "0b")).rstrip("b"))
        h0 = int(at // 2)
        pts = [["0b", up[h0]]]
        for h in range(h0 + 1, n + 1):
            if up[h] != up[h - 1]:
                pts += [[f"{round(2 * h - at - 0.02, 5):g}b", up[h - 1]], [f"{round(2 * h - at, 5):g}b", up[h]]]
        own = list(up)
        if name == "hair" and since and float(met):                 # the chance meeting: where the two play one note, the second is taken in
            x = CELLS[AT["five"]][2] + float(HAIR.split(";")[0])
            for c in range(AT["five"], AT["full"] + int(ONE.split(";")[1])):
                x, tune = CELLS[c][1] * x * (1 - x), CELLS[c][3]
                if c >= AT["full"] + int(since) and x >= 1 / 7 and tune >= 1 / 7 and min(15, int(x * 16)) == min(15, int(tune * 16)):
                    own[c] += float(met)
        pts = [["0b", own[h0]]]
        for h in range(h0 + 1, n + 1):
            if own[h] != own[h - 1]:
                pts += [[f"{round(2 * h - at - 0.02, 5):g}b", own[h - 1]], [f"{round(2 * h - at, 5):g}b", own[h]]]
        gain = t["gain"] if isinstance(t["gain"], dict) else {"value": t["gain"], "mod": []}
        t["gain"] = {"value": gain["value"], "mod": list(gain["mod"]) + [{"src": "auto.heard", "amount": 1}]}
        t["auto"] = {**(t.get("auto") or {}), "heard": {"points": pts, "curve": 0}}
    if target:
        doc["loudness"] = float(target)
    return up


# v31 (chirper-three; whole song, every guitar stroke from 0:07 to the end): THE SIX GET THEIR TEETH. The cure of
# Extreme and Mean v23, Take Up the Slack v12 and Common Measure v24 on this song, on three rigs at once, read
# with `riffpunch.py --strokes` and fitted to this song's own mix. Not one note moves.
#   THE STROKES WERE A THUD. Their scoop (400 Hz-1 kHz less 1-4 kHz through a stroke) read -3.6 on the first pair,
#       -6.7 on the second and -3.8 on the third, where six records' strokes read -11.3 (-12.7 to -6.5). Alone against
#       a record's guitar alone (`cabspec.py`) the wall stood 5 to 8 dB over from 500 to 800 Hz.
#   THE PALM comes off the string a little on all six (3.4 octaves closed at a full mute -> 2), the 700 Hz lift goes
#       from all six, the first and third pairs take 2 dB out at 800 Hz, and each gets 2.5 dB at 185 Hz (the chest the
#       opener string costs: by part the guitars' 120-250 Hz went -4.6 -> -6.4 without it).
#   THE MICROPHONES are this song's own: the first pair's stays (it plays alone from 0:07 to 1:09 and on the way down,
#       where the mix was 0.8 to 2.3 dB short at 2-4 kHz); the second pair's goes out 0.35 -> 0.47 and the third's
#       0.55 -> 0.6, because where they join (the walls, the top) the mix was already over there.
#   THE FADERS go up 0.5 dB: with the middle gone the six read 0.4 to 0.7 dB quieter alone (K); now +0.1 and -0.2.
#   THE TUNE GIVES SOME BACK. The square-wave tune lives where the guitars' middle was, so with no other change v30's
#       reading of it (its own third-octave against everything else) rose 0.6 to 3.8 dB. v30 lifted the chips 3 dB
#       wherever a guitar plays (7 at the top) to make it heard; 1.5 dB of that is given back (0.5 at the top), and
#       the tune reads where v30 left it (within 0.8 dB; `six` 2.1 over) while standing 1.1 to 1.6 dB lower against
#       the band (0.4 at the top).
# AFTER: scoop -8.8 / -9.1 (first pair, the wall / two), -10.3, -7.8: all inside the records' range. Alone, the wall
#   2.84 -> 1.98 from the record's guitar and the top 3.50 -> 2.78. The mix against the records' passages with no
#   voice 1.80 -> 1.57, nearer in all six stretches read (500 Hz-1 kHz 3.8 -> 2.3 over); against all eleven 1.33 ->
#   1.24, the two walls 0.02 and 0.06 further (they read 1.4 and 1.5 over at 2-4 kHz; 0.4 and 0.8 before). The keys
#   over the left guitar (Harry: "Keep one guitar with the keys") read -2.2 -> -0.6 in `two`. NOT CURED: the low
#   end's fall after a stroke (tight: +2.1 to +2.8 where the records read -1.1).
# the palm's octaves at a full mute ; the first pair's eq, band|band ; the second pair's ; the third pair's ; the three
# rigs' microphones, first,second,third ("" in a place = as it was) ; dB on the six faders ; dB of v30's lift on the
# chips given back, away from the top,at the top ; the loudness target ("" = unchanged). "" = v30 byte for byte.
TEETH = os.environ.get("C10T6_TEETH", "-2;peak cutoff=185 q=1.2 gain=2.5dB|peak cutoff=800 q=1.2 gain=-2dB;peak cutoff=185 q=1.2 gain=2.5dB;"
                       "peak cutoff=185 q=1.2 gain=2.5dB|peak cutoff=800 q=1.2 gain=-2dB;,0.47,0.6;0.5;1.5,0.5;-9.9" if HEARD else "")


def the_six_get_their_teeth(doc):
    """v31: the muted strokes' teeth on all three rigs (the palm, the mids, the microphones)."""
    palm, *eqs, mics, fader, _, target = TEETH.split(";")
    for t in doc["tracks"]:
        if t["name"] in ("gl", "gr", "gl2", "gr2", "gl3", "gr3"):
            k = int(t["name"][2:] or 1) - 1
            mic = mics.split(",")[k]
            if mic:
                assert t["patch"].count("fx.2.mic=") == 1
                t["patch"] = re.sub(r"fx\.2\.mic=[0-9.]+", f"fx.2.mic={mic}", t["patch"])
            if palm:
                t["patch"] += f" synth.filters.0.cutoff.mod.0.amount={palm}"
            t["fx"] = [{"type": "eq", "bands": eqs[k].split("|")}] if eqs[k] else []
            if not t["fx"]:
                del t["fx"]
            if fader and float(fader):
                t["gain"] = f"{float(t['gain'][:-2]) + float(fader):g}dB"
    if target:
        doc["loudness"] = float(target)


# v32 (chirper-alpha; whole-song round; 1:35 to 3:05, six places; no note is written): THE AMP IS LEFT ON.
# The rule is x <- r x (1 - x), once every half bar, and the clock is what makes it double and run wild. The same
# rule with NO clock (dP/dt = r P (1 - P / K)) can only do one thing: grow to its ceiling and stay. A guitar amp
# left on does exactly that. Its output reaches the strings, comes back through the pickup, and is amplified again:
# a loop with gain and a soft ceiling, and the power of what it howls obeys that equation. So wherever all six
# guitars take their hands off (a rest of 2.6 beats or more: twelve, of which ten with the dial past 3), the right guitar's amp is
# such a loop, and the engine works it out: one bus per root, whose own output comes back into it one period of the
# last root struck later (`returns`, the engine's feedback routing: its first use on this record), through a
# band-pass (Q 24) on that root's 64th harmonic and a tanh. THE DIAL IS THE LOOP'S GAIN: k dB over unity for each
# unit r stands past 3 (five 0.19, three 0.22, the top 0.26, down-four 0.13, down-two 0.05); at 3 or under it is
# stable and never opens (0:24, 3:23), which is the rule's own first threshold. The loop opens on the right
# guitar's last stroke (the seed) and shuts on the next stroke of any guitar: the chord cuts it off.
# THE PITCH is the root just struck, six octaves up: G7 (3135 Hz) in the lock on five, B flat 7 (3728) in the
# three, B7 (3949) in the top's holes (the scream is on B), E7 (2637) on the way down.
# THE PLAYER sets one thing, the head start (how much of the guitar reaches the loop, per root): so that under the
# two sung laps of five and of three the howl is at half its ceiling as the SECOND singer comes in (5.3 s of 8.5;
# 3.65 s of 5.0): what a band does the second time round (v2, v24).
# MEASURED (raw; the right guitar with what it feeds, less the right guitar): the amp's power against the logistic
# curve K / (1 + (K/P0 - 1) exp(-r t)): median miss 0.35 dB in five (r 1.94 a second), 0.18 in three (r 2.61).
# Outside the rests the amp stands 57 to 60 dB under the mix. The numbers of each rest are in the round note.
# THE FIRST PITCH TRIED WAS THE 24TH HARMONIC (D6 1176 Hz at five, F6, G flat 6: a fifth over the root) AND IT TOOK
# THE WORDS: a recogniser given the six sung lines in the mix read 9 of 18 words without the amp and 5 with it; the
# top's first hole lost "more room" at every level tried, down to 10 dB lower. It sat on the vowels' second
# formant. Six octaves over the root it is above them: the lines read the same with it and without.
# dB of loop gain over unity for each unit the dial stands past 3 ; which harmonic of the last root struck the loop
# is tuned to ; the loop's band-pass Q ; the shortest rest of all six guitars that opens it, in beats ; whose amp
# (the track that feeds the loop) ; the amp's fader ; its pan ; its colour (effects after the loop, '|' between) ;
# how much of the guitar reaches the loop (the seed) ; sections where the amp stays shut (names, comma between) ;
# the loudness target ("" = unchanged). "" = v31 byte for byte.
AMP = os.environ.get("C10T6_AMP", "0.26;64;24;2.6;gr;-30dB;0.5;drive shape=tanh drive=0.3 bias=0.3|cab model=4x12-modern mic=0.5 distance=0.15;g=-30,bb=-25,b=0,e=-14;;" if TEETH else "")
RATE = 48000


def the_amp_is_left_on(doc):
    """v32: wherever all six guitars rest, the right guitar's amp is a loop with gain: its own output comes back
    into it one period of the last root later, through a band-pass on that root's 24th harmonic and a tanh. The
    loop's gain over unity is the dial: k dB for each unit r stands past 3, half bar by half bar. Nothing is written."""
    k, harm, q, least, who, fader, pan, colour, seed, shut, target = AMP.split(";")
    k, harm, q, least = float(k), int(harm), float(q), float(least)
    midi = lambda name: NAMES.index(name[:-1]) + 12 * (int(name[-1]) + 1)
    ev = sorted((n["at"], n["at"] + n["len"]) for t in doc["tracks"] if t["name"] in G + G2 + G3 for n in t["notes"])
    mine = sorted((n["at"], n["pitch"]) for t in doc["tracks"] if t["name"] == who for n in t["notes"])
    rests, end = [], 0
    for a, b in ev:
        if end and a - end >= least:
            struck = [x for x in mine if x[0] < end]
            if struck:
                rests.append((struck[-1][0], a, min(midi(v) for v in struck[-1][1].split(","))))
        end = max(end, b)
    unity = -20 * math.log10(q / math.tanh(1))       # the band-pass passes its centre at Q; tanh(x) / tanh(1) at 1.313
    lanes = {}
    for a, b, root in rests:
        c0, c1 = int(a // 2), int(math.ceil(b / 2))
        over = [(max(a, 2 * c), k * (CELLS[c][1] - 3)) for c in range(c0, c1) if 2 * c < b]
        if max(v for _, v in over) <= 0 or CELLS[c0][0] in shut.split(","):
            continue                                     # at or under 3 the loop never passes unity: it stays shut
        lane = lanes.setdefault((root - 28) % 12 + 28, [])
        for at, v in over:
            lane += [[round(at - .02, 5), lane[-1][1] if lane else 0], [round(at, 5), round(20 + v, 4)]]
        lane += [[round(b - .02, 5), lane[-1][1]], [round(b, 5), 0]]
    feeds = {}
    for root, lane in sorted(lanes.items()):
        name = "howl-" + NAMES[root % 12].lower()
        frames = round(RATE / (440 * 2 ** ((root - 69) / 12)))
        f0 = harm * RATE / frames
        doc["buses"][name] = {
            "fx": [{"type": "eq", "bands": [f"bp cutoff={f0:.2f} q={q:g}"]},
                   {"type": "gain", "gain": {"value": f"{unity - 20:.4f}dB", "mod": [{"src": "auto.open", "amount": 1}]}},
                   {"type": "drive", "shape": "tanh", "drive": 0, "oversample": 1}],
            "returns": [{"from": name, "gain": "0dB", "time": f"{(frames + .2) * 1000 / RATE:.4f}ms"}],
            "auto": {"open": {"points": [["0b", 0]] + [[f"{at:g}b", v] for at, v in lane], "curve": 0}},
            "out": "amp"}
        feeds[name] = dict(v.split("=") for v in seed.split(","))[name[5:]] + "dB"
    if feeds:
        doc["buses"]["amp"] = {"fx": [f for f in colour.split("|") if f], "gain": fader, "pan": float(pan), "out": "gtrs"}
        t = next(t for t in doc["tracks"] if t["name"] == who)
        t["sends"] = {**t.get("sends", {}), **feeds}
    if target:
        doc["loudness"] = float(target)


# v33 (chirper-three; whole song: THE ROOM THAT IS LEFT). Nothing is written; no note, fader or sound of any part changes.
# The rule has three factors: x, the count (how many places a half bar strikes, since v1); r, the dial (the form,
# since v1); and (1 - x), "the room that is left". The third was never played, in a song called Carrying Capacity
# whose singers sing "no more room". NOW IT IS THE ROOM. The players who play the rule (the six guitars, the string
# touched at the first bass note, and the drummer's snare and toms; not the machine, which is in no room, nor the
# bass, the chips or the singers) send into one hall, and what reaches it is multiplied, half bar by half bar, by
# (1 - x): the rule's own factor, nothing chosen. A crowded half bar is dry and close; a sparse one rings.
# SO THE FORM IS HEARD AS DEPTH. The string at 0:03.5 rings in an empty hall (x 0.19: the room 11.4 dB under the mix
# and as loud as the string itself) and the room closes as the count grows (9 dB shut at 'one', and steady). At 3
# it SPLITS with the riff: near, far, near, far (what is sent 1.5 dB apart at 0:28, 11.6 by 0:37), then four depths, eight; five
# in the lock on five, three in the three. At the top the scream has no room at all (58 dB shut), its last ring
# opens into all of it, and the climb back from nothing is the farthest thing in the song (the room 6 to 7 dB
# under the mix on its first low notes, 2:28 and 2:31). On the way down the two depths close up again; and when the
# dial reaches 1 and the count dies, the room is all there is: the last strokes stand 4 dB over their own room and
# the file's last four seconds are 2.2 to 4.0 dB louder than v32's.
# MEASURED (raw, the room alone = this mix less v32's; a half bar OPEN is one with (1 - x) over -6 dB, SHUT under
# -14): the room against the mix, open / shut: two -13.5 / -20.8 ; four -13.0 / -20.8 ; eight -12.1 / -20.8 ; the
# first wall -9.9 / -18.1 ; the second -8.8 / -23.1 ; six -9.4 / -27.4 ; down-four -14.6 / -24.5 ; the last two
# strokes' half bars -8.6, -10.4. A shut half bar's room is the tail of the open one before it (the hall is 2 s; a half bar 0.87).
# THE HALL has nothing under 400 Hz or over 5 kHz: with 200 Hz the top read 0.5 dB further over at 250-500 Hz, now 0.3.
# THE MIX'S READ is level: against the records' passages without a voice, mean of six stretches, 1.570 -> 1.598 ;
# against all eleven 1.241 -> 1.235 (250 Hz-2 kHz, already over, is 0.0 to 0.3 dB further over).
# THE TARGET moves -9.9 -> -9.71 so that what is NOT in the room stands where it stood: the machine alone before
# the first string is within 0.026 dB of v32 on three seeds (at -9.9 it fell 0.36; a sparse stretch moves 1.96 dB
# for a dB of target here, the band 1.1). The band's sections are 0.09 to 0.38 dB louder: that is the room.
# THE SCORER: 86.733 / 83.716 / 83.512 -> 88.094 / 87.184 / 85.117 (seeds 0, 11, 1). NOT CLAIMED: 5.3 to 5.6 of its
# rhythm term on every seed is its off-grid share moving up towards the 0.10 the term wants (no stroke moved: the
# room rings between the strokes; not separated further), and seed 11's recurrence (+15.6) is this song's swing.
# COSTS: a room on high-gain guitars is a wash if it is too loud, and nobody has heard this level (the if/thens are
# in the round's next-note) ; the walls and the six are 0.2 to 0.4 dB louder ; the amp's howl (v32) now starts over a
# ringing room, not a dead rest (the howl is not in the room; not re-read).
VACANT = os.environ.get("C10T6_VACANT", "gl=0,gr=0,gl2=0,gr2=0,gl3=0,gr3=0,touch=0,dsnare=-6,dtoms=-6;"
                        "reverb kind=hall decay=2s mix=1 predelay=25ms low_cut=400 high_cut=5000;-4dB;1;-60;-9.71" if AMP else "")


# v34 (chirper-zero; section round, w3 0:55.7-1:23.5; the change is the two bars before the first wall, 1:06.1-
# 1:09.6; nothing else in the song changes): THE DIAL DOES NOT JUMP. The form is the dial, and every turn of it is
# played but one. From eight (3.555) to the first wall (3.6) the song stepped over the most famous stretch of the
# rule: past 3.564407 the riff is sixteen half bars long, past 3.568759 thirty-two, past 3.569692 sixty-four, past
# 3.569891 a hundred and twenty-eight, and at 3.569946 the doublings pile up against one point, beyond which it
# never repeats. Each stretch is 4.67 times shorter than the one before (Feigenbaum's number). The band cannot
# play it: a riff of sixteen half bars is eight said twice with differences smaller than a fret, and it would
# need fourteen seconds to say once. THE CHIP CAN. Its second voice, which lives only in eight's last lap, says
# four notes at the riff's pace and then the dial is turned steadily through the whole cascade in the two bars
# that are left, and EVERY TIME THE CYCLE DOUBLES THE CHIP STEPS TWICE AS FAST, because that is the only way to
# say a cycle twice as long in the time there is: 19 notes in triplets while the cycle is sixteen, 8 twice as
# fast while it is thirty-two, 3 at four times, 2 at eight times (18 ms each), and the wall. The grid fits the
# rule: read at each note's middle the dial is inside that note's own stretch, all 32 (asserted). Nothing is
# written: the track still carries no notes, only the rule, the dial's setting for each step and where x stood,
# and it is the same orbit, never reset. What it plays is the tune of eight folding up: the same eight pitches,
# a third over the tune, faster and faster until an old console's trick happens by itself and the run is a chord.
# beats before the wall in which the dial is turned through the cascade ; notes at each doubling (triplet
# eighths, then twice as fast each time) ; dB on the second voice while it runs ('' = none) ; the loudness
# target ('' = unchanged). On only while VACANT is. "" = v33 byte for byte.
CASCADE = os.environ.get("C10T6_CASCADE", "8;19,8,3,2;;" if VACANT else "")
FEIGENBAUM = (3.564407, 3.568759, 3.569692, 3.569891, 3.569946)   # the riff becomes 16, 32, 64, 128 half bars long ; the doublings pile up


def the_dial_does_not_jump(doc):
    """v34: the chip's second voice plays the period-doubling cascade between eight and the first wall."""
    beats, counts, lift, target = CASCADE.split(";")
    beats, counts = float(beats), [int(v) for v in counts.split(",")]
    t = next(t for t in doc["tracks"] if t["name"] == "lead2")
    assert len(t["gen"]) == 1 and t["gen"][0]["n"] == 8 and t["gen"][0]["len"] == "/2" and beats % 2 == 0, t["gen"]
    first = t["gen"][0]
    keep = 8 - int(beats // 2)                   # half bars the voice still says at the riff's pace
    x = first["x0"]
    for _ in range(keep):
        x = first["r"] * x * (1 - x)
    gens, at, div = [dict(first, n=keep)], 0.0, 12
    for k, n in enumerate(counts):
        for _ in range(n):
            r = round(FEIGENBAUM[0] + (FEIGENBAUM[4] - FEIGENBAUM[0]) * (at + 2 / div) / beats, 6)
            assert FEIGENBAUM[k] <= r < FEIGENBAUM[k + 1], (k, r)      # the dial, at this note's middle, is in this doubling
            gens.append({**first, "r": r, "x0": x, "n": 1, "len": f"/{div}"})
            x = r * x * (1 - x)
            at += 4 / div
        div *= 2
    assert abs(at - beats) < 1e-9, at
    t["gen"] = gens
    if lift and float(lift):
        t["gain"]["mod"].append({"src": "auto.run", "amount": 1})
        t["auto"]["run"] = {"points": [["0b", 0], [f"{16 - beats - 0.02:g}b", 0], [f"{16 - beats:g}b", float(lift)], ["16b", float(lift)], ["16.02b", 0]], "curve": 0}
    if target:
        doc["loudness"] = float(target)


def the_room_that_is_left(doc):
    """v33: the rule's third factor is played. What each named part sends into one room is multiplied, half bar by
    half bar, by (1 - x): the room that is left. Nothing is written and no part's own sound changes."""
    who, room, fader, power, least, target = VACANT.split(";")
    lane, last = [], None
    for c in range(NC):
        v = round(max(float(least), 20 * float(power) * math.log10(max(1 - CELLS[c][3], 1e-9))), 2)
        if last is None:
            lane.append(["0b", v])
        elif v != last:
            lane += [[f"{2 * c - .02:g}b", last], [f"{2 * c:g}b", v]]
        last = v
    doc["buses"]["vacant"] = {"fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.left", "amount": 1}]}}, room],
                              "auto": {"left": {"points": lane, "curve": 0}}, "gain": fader}
    sends = dict(v.split("=") for v in who.split(","))
    for t in doc["tracks"]:
        if t["name"] in sends:
            t["sends"] = {**t.get("sends", {}), "vacant": f"{float(sends.pop(t['name'])):g}dB"}
    assert not sends, sends
    if target:
        doc["loudness"] = float(target)


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


def show(x):
    slots, ai, r = cell(x)
    s = ["."] * 6
    for i, sl in enumerate(slots):
        s[sl] = "%X" % r if i == ai else "0"
    return "".join(s)


if __name__ == "__main__":
    if os.environ.get("C10T6_SHOW"):
        for name, n, _ in DIAL:
            a = AT[name]
            print(f"{name:10s} bar {a // 2:3d} r {CELLS[a][1]:.4f}..{CELLS[a + n - 1][1]:.4f}  " + " ".join(show(c[3]) for c in CELLS[a:a + n]))
    else:
        doc = song()
        if HEARD:
            the_rule_is_heard(doc, *(float(v or 0) for v in (TEETH.split(";")[6].split(",") if TEETH else ())))
        if TEETH:
            the_six_get_their_teeth(doc)
        if AMP:
            the_amp_is_left_on(doc)
        if VACANT:
            the_room_that_is_left(doc)
        if CASCADE:
            the_dial_does_not_jump(doc)
        open(OUT, "w").write(dump(doc))
