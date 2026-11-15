#!/usr/bin/env python3
"""chirpers10-t3 "Plain Hunt" (chirper-zero): one row of six notes, rung in every order.

English church bells cannot play tunes: a bell swings full circle and can only be made to strike a little sooner or a
little later. So ringers ring CHANGES: the bells strike once each, in a row, and from one row to the next a bell may
only swap places with its neighbour. A method is a rule for the swaps that visits every possible order exactly once and
comes back to where it started ("rounds", the bells running down the scale). On five bells that is 120 rows, an EXTENT,
and until the last row nothing is ever heard twice.

Common Time (track 1) turns three cells of different lengths under one pulse; Odd Sympathy (track 2) slides one riff
against itself. This piece's long cycle is an ORDER: the riff is a row of six sixteenths, five notes that change places
by the ringers' rule and a low F that always comes last ("the tenor behind"), and it is rung through two extents, 240
rows, no two alike within either, each ending where it began. Six sixteenths against four beats also turn: the row and
the bar line meet every third bar.

  the row     bells 1 2 3 4 5 (6) = Eb C B Ab Gb (F): the album's hook notes, running down. Rounds is that scale.
  the hunt    bell 1 (the treble, the highest note) "plain hunts": its place in the row walks 1 2 3 4 5 5 4 3 2 1 and
              round again, all piece long. It is played open and loud, the kick goes with it, and a church bell doubles
              it: an accent that slides later and later through the riff, then earlier and earlier.
  the methods Plain Bob Doubles (called plain plain plain bob, three times) and Grandsire Doubles (plain bob plain bob
              plain single, twice): each is checked below to be a true extent.

v1 is the SKELETON (Harry, 14 Nov: "answered clips. unlock a third track slot!"; track 2's terms): the whole shape
standing, bare.
"""
import json
import math
import os

OUT = os.environ.get("C10T3_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t3.yaml"))
BPM = 96
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ---------------------------------------------------------------------------------------------------- the ringing
ROUNDS = (1, 2, 3, 4, 5)
PITCH = {1: 10, 2: 7, 3: 6, 4: 3, 5: 1, 6: 0}        # semitones above the ground: Eb C B Ab Gb, and the tenor F


def change(row, places):
    """One change: the bells in `places` (1-indexed) stay where they are; every other pair of neighbours swaps."""
    r, i = list(row), 0
    while i < len(r):
        if i + 1 in places:
            i += 1
        else:
            r[i], r[i + 1] = r[i + 1], r[i]
            i += 2
    return tuple(r)


def notation(s):
    return [set(int(c) for c in x) for x in s.split(".")]


PLAIN_BOB = {"p": notation("5.1.5.1.5.1.5.1.5.125"), "b": notation("5.1.5.1.5.1.5.1.5.145")}
GRANDSIRE = {"p": notation("3.1.5.1.5.1.5.1.5.1"), "b": notation("3.1.5.1.5.1.5.1.3.1"), "s": notation("3.1.5.1.5.1.5.1.3.123")}


def ring(method, calls):
    """The rows a touch produces, one lead (ten rows) to each call, starting from rounds (which is not itself rung)."""
    rows, r = [], ROUNDS
    for c in calls:
        for places in method[c]:
            r = change(r, places)
            rows.append(r)
    assert len(rows) == 120 and len(set(rows)) == 120 and rows[-1] == ROUNDS, "not a true extent"
    return rows


EXTENT_1 = ring(PLAIN_BOB, "pppb" * 3)
EXTENT_2 = ring(GRANDSIRE, "pbpbps" * 2)

# v5: THE ROW BECOMES A RIFF (whole song). Through v4 the row was six even sixteenths: a run. A riff has weight: long
# notes, repeated notes, an accent that means something. Now the bells have WEIGHTS, and they keep them wherever they
# stand in the row:
#   the treble (the highest note) is LONG: open, ringing, two sixteenths in the first extent and three in the second;
#   the tenor (the low F, always last) is REPEATED: two muted chugs in the first extent, three in the second (a gallop);
#   the four bells between are single muted sixteenths, as they were.
# So in the first extent a row is eight sixteenths, half a bar: every row starts on a beat, the tenor's two chugs
# close each half bar, and the long note walks through the sixteenths between as the treble hunts: an accent that
# slides later and later against a beat that does not move. In the second extent a row is ten sixteenths: heavier,
# and it turns against the bar again (the row and the bar line meet every fifth bar). The ringers' rule is untouched:
# the same 240 rows, in the same order. The song is faster (120 for 96) so that a row takes about the time it took.
# treble , tenor weight in the first extent ; in the second ; the tempo ; rows of rounds before the first extent ; rows
# of rounds at the landing. "" = v4 (six even sixteenths, 96).
RHYTHM = os.environ.get("C10T3_RHYTHM", "2,2;3,3;120;8;16")
if RHYTHM:
    W1, W2 = (tuple(int(x) for x in part.split(",")) for part in RHYTHM.split(";")[:2])
    BPM, ROUNDS_N, LAND_N = (int(x) for x in RHYTHM.split(";")[2:5])
else:
    W1, W2, ROUNDS_N, LAND_N = (1, 1), (1, 1), 16, 24
L1, L2 = 4 + sum(W1), 4 + sum(W2)                  # a row's length in each extent, sixteenths
assert (40 * L1) % 16 == 0 and (40 * L2) % 16 == 0 and (ROUNDS_N * L1) % 16 == 0 and (LAND_N * L1) % 16 == 0
T1, T2 = 40 * L1 // 16, 40 * L2 // 16              # bars in a third of each extent (forty rows)
# ---------------------------------------------------------------------------------------------------- the form (bars)
INTRO, BAND = 0, 4
PART1 = BAND + ROUNDS_N * L1 // 16
MIDDLE = PART1 + 3 * T1
PART2 = MIDDLE + 8
LAND = PART2 + 3 * T2
END = LAND + LAND_N * L1 // 16         # the landing is rung as the band first rang rounds: the first extent's row
NB = END + 3


def meet(length):
    """Bars between meetings of the row and the bar line (a crash there); every fourth bar where they always meet."""
    c = math.lcm(length, 16) // 16
    return c if c > 1 else 4


KEYS_1 = (0, 3, 6)        # the ground of each third of the first extent: F, Ab, B
KEYS_2 = (0, 3, 7)        # and of the second: F, Ab, C (so the landing on F is a fall of a fifth)
G4 = ("gl", "gr", "gl2", "gr2")
BELL_LAND = float(os.environ.get("C10T3_BELLLAND", "-5"))
KICK_ALL = float(os.environ.get("C10T3_KICKALL", "-3"))
CYM_BUSY = float(os.environ.get("C10T3_CYMBUSY", "-3"))
# v2: THE TOWER GETS ITS VOICES AND A GONG (palette round). Where the bells ring alone (the opening, the middle, the
# end) they rang over a bowed drone and a synth pad: `contrabass-tight` and `juno-pad`, which all three songs of the
# album use. Both leave this song. Under the bells there is now a CHANT: two low men's voices a fifth apart (F and C),
# the library's `fof-chant` (Rodet's CHANT bass, one grain per formant per period, no filters, the mouth moving slowly
# between "o" and "u"), which no other track on the album uses and whose source (`fof`) the album had not used. And a
# GONG (`modal-gong`, a tam-tam on the modal layer) is struck twice: when the first extent comes round (2:17) and on
# the last chord (4:52).
# The CHANT voice has no weight of its own (its sound is its mouth's resonance, 250-500 Hz; nothing under 120 Hz), so
# a floor goes under it where the bowed bass was: a BASS TAGELHARPA (`tagelharpa-bass`, a bowed horsehair lyre, coarse
# and beating), on the low F. It too is new to the album.
# the chant's patch ; its gain ; its hall send ; the gong's patch ; its gain ; its note ; the floor's patch ; its gain.
# "" = v1 (the drone and the pad).
TOWER = os.environ.get("C10T3_TOWER", "fof-chant;-15.5dB;-6dB;modal-gong;-13dB;F1;tagelharpa-bass;-21dB")
# v3: THE SECOND EXTENT STARTS ON THE BASS, AND THE BASS HAS TEETH (palette round). Until now nothing but the drums'
# pattern told the second extent from the first. Now its bass is two basses: the album's `ct-bass`, which keeps the
# weight, and over it the library's `bass-fuzz` (a bass string through a FOLDING fuzz; here the fold is the engine's
# `wavefold`, which the album had not used), high-passed so that only its teeth are added: 1-4 kHz, where ct-bass
# has little. No other track on the album uses it. And the extent opens on it: for its first eight rows (three bars,
# until the row and the bar line meet again) the guitars rest and the bass, the kick, the snare and the bell carry
# the row; then the four guitars come in on the crash.
# the patch string ; its gain ; its high-pass, Hz ; rows the guitars rest at the start ; its gain in those rows, dB over. "" = v2.
# v10 (Harry, of the bass alone at 2:32: "Too long alone"): four rows, not eight: two and a half bars for five. The
# guitars come in where the fifth row starts, on a crash.
FUZZ = os.environ.get("C10T3_FUZZ", "bass-fuzz fx.0.shape=wavefold;4dB;180;4;4")
# v10: THE CHANT CHANTS (Harry, asked whether the chant under the bells sounded like men chanting: "dont hear
# chamts"). It was two held notes, a fifth apart, 7 dB under the bells: a pad. Now the two voices SING A LINE: a note
# to each row the bells ring (every three beats), stepping round the low F on the riff's own scale (F, G flat, A
# flat), the upper voice a fifth above the lower the whole way, as the oldest two-part chant goes; and they are
# louder. The bowed floor under them holds as it did.
# the lower voice's line under the opening's bells | under the middle's | under the last tolls (semitones over F) ;
# the gap between notes, beats ; the chant's gain (it was -15.5 dB). "" = v9.
CHANT = os.environ.get("C10T3_CHANT", "0,1,0,3,0|0,0,1,0,3,1,0,1,0|0,1,0;0.25;-11.5dB") if TOWER else ""
# v4: THE CLIMB (section round, 3:52-4:30: the last third of the second extent, which the section map called static:
# fifteen bars of the row with the kick on every note). Over it a LEAD GUITAR now plays the row's own notes the other
# way and sixteen times slower than the band's eighths would be: from the ground up, C D-flat E-flat G-flat G B-flat,
# two bars to a note, and then the octave C held for the last three bars. The band's row falls and falls; the lead
# climbs once, slowly, and arrives at the top as the extent comes round and the band lands on F. It is the song's
# first lead, on the library's `lead-monster` (a sustaining 8-string through a 5150 with a delay and a big room),
# which no other track on the album uses. For the last four bars the snare is on every beat.
# The four guitars' bus comes down a little under the lead, so the climb is not louder than the landing it leads to.
# the patch ; its gain ; its lowest note (MIDI) ; bars to a note ; the snare's velocity on the added beats ; the
# guitars' bus under the lead, dB. "" = v3.
CLIMB = os.environ.get("C10T3_CLIMB", "lead-monster;-12dB;72;%s;0.85;-1.5" % ("3" if RHYTHM else "2"))
if CLIMB:                # the bar the lead starts: it leaves room for six notes and the octave (held four bars at most since v5)
    _per = float(CLIMB.split(";")[3])
    _top = min(4, T2 - 6 * _per) if RHYTHM else T2 - 6 * _per
    CLIMB_B0 = PART2 + 2 * T2 + (T2 - 6 * _per - _top)
    CLIMB_B0 = int(CLIMB_B0) if CLIMB_B0 == int(CLIMB_B0) else CLIMB_B0


# v6: THE METHOD IS HEARD (whole song). Through v5 the two long stretches were a riff that changed and a kit that did
# not: nothing told the ear where the ringing was in its course (the section map called three windows static). The
# method has a shape, and now the band plays it:
#   HOME. Each LEAD (ten rows) ends with the treble leading twice: the long note is first in the riff two riffs
#     running, the one moment its slide stops. A crash goes on each of those two long notes, and
#     the kit no longer crashes by the bar count. So the phrases are the leads: five bars in the first extent; in the
#     second six and a quarter, so each home falls a beat later in the bar than the last.
#   THE CALL. Where the conductor would call (a bob or a single: three times in the first extent, six in the second)
#     those two riffs are a break for the whole band in unison: every note open and loud, the kick with every note,
#     and the kit stops its beat and RINGS THE ROW: a crash for the treble, a tom for each of the four bells between
#     (high to low as the bells are), the snare on the tenor's chugs. In the first extent the calls are the last bar of
#     each third (the turnaround into the key change); in the second there is one in the middle of each third too.
#   THE HUNT LAID BARE. For one lead in each cycle, the first on A flat (0:56-1:06 and 3:22-3:34), the guitars play
#     only the long note and the low chugs, and the bass alone keeps the four notes between: the long note is heard
#     sliding against the chugs with nothing in the way. Then the whole riff comes back. It is in both cycles at the
#     same place, so the second time it is a thing that returns.
# (Tried and not kept: the kit's three beats in the second cycle in the first cycle's order, `abc`. I expected the
# scorer to hear the second cycle as more of a return; it heard less of one, 0.192 for 0.224 of its sections.)
# the two cymbals at home ; the velocity of a call's notes ; the rows of each extent laid bare (from:to) ; the kit's
# beat in each third of the second extent. "" = v5.
FORM = os.environ.get("C10T3_FORM", "c,c;1.0;40:50;bac")
# v7: THE RIFF IN HARMONY (section round, 3:47-4:12: the second half of the second cycle's stretch on A flat, which the
# section map called static and "little new"). After the break at 3:44 the riff comes back with a SECOND VOICE: two
# more guitars, one a side inside the four, play the riff an octave up and a third above (two steps up the riff's own
# six-note scale: F takes A flat, G flat takes B, A flat takes C, B takes E flat, C takes F, E flat takes G flat), in
# the riff's own rhythm: the long note long, the chugs chugged. They are on a third amp (`mark`, the four are on a
# 5150 and a `nolly`), their own cones. At the break at 4:09 they join the unison an octave up, and when the key
# moves to C (4:12) they stop: the high register is the lead's from there.
# the patch string ({} = the cone) ; the gain ; the pan ; the rows of the second extent in harmony (from:to; the call
# after them is played in unison) ; scale steps up ; semitones up ; the two cones ; the guitars' bus under them, dB
# (six guitars for four: without it the stretch was as loud as the stretch on C it leads to). "" = v6.
# v10 (Harry: "Keep it, louder"): the two harmony guitars 3 dB up (-3 dB -> 0 dB) and the bus 1.2 dB under them (it was 0.7).
HARM = os.environ.get("C10T3_HARM", "ct-twin fx.1.model=mark fx.2.mic=0.55 fx.2.cone={};0dB;0.45;60:78;2;12;18,19;-1.2")
# v8: THE LAST STRETCH HAS ITS OWN RIG (palette round). Both cycles were played on the same four guitars: a 5150 take
# and a `nolly` take a side, all through the engine's modern 4x12. Now, from where the key moves to C and the lead
# begins to climb (4:12) until the landing, the SECOND pair is another rig:
# a `gojira` amp through the engine's 1x12 cabinet (which no song on the album had used: all five cabinets are in use
# now). Alone on the same notes and as loud as the pair it replaces: 3 to 8 dB less under 250 Hz, 1.6 dB more at
# 500-1000 Hz (a small box honks: 5 dB before the one eq band here), 5.8 dB more at 4-8 kHz and 9.4 more above. So the
# first pair keeps the weight and the second pair is all bite. At the landing the four come back: the return is a
# return of the rig too.
# (Tried first: the new pair through the WHOLE second cycle. The scorer heard the second cycle as less of a return of
# the first: its two matching stretches fell from 0.82 and 0.71 to 0.73 and 0.53, the share of returning sections from
# 0.34 to 0.25, the total to 98.79 / 99.36. So the new colour goes where the music is new, the stretch on C, which
# matched nothing before.)
# And the FUZZ over the bass, which was meant as teeth only, is cut to its teeth: read against the eleven records the
# second cycle was 2.2 dB over at 250-500 Hz where the first is 1.2, and part by part the fuzz held a fifth of that
# band. Its high-pass goes from 180 Hz to the last field here.
# the patch string ({} = the cone) ; its gain ; the two cones ; one eq band on it ; the fuzz's high-pass, Hz ; the
# row of the second extent it starts at. "" = v7.
RIG2 = os.environ.get("C10T3_RIG2", "ct-twin fx.1.model=gojira fx.2.model=1x12 fx.2.mic=0.5 fx.2.cone={};1dB;16,17;700:1:-4;500;80")
G4B = ("gl", "gr", "jl", "jr") if RIG2 else ("gl", "gr", "gl2", "gr2")
# v9: THE SNARE HUNTS (section round, 1:56-2:14: the last two leads of the first cycle; the map called 1:36-2:08
# static and found nothing entering in it). The first cycle had no event of its own at its end (the second has the
# lead's climb). Its last stretch keeps the backbeat for two leads; then, for the last two, the SNARE LEAVES THE
# BACKBEAT AND FOLLOWS THE LONG NOTE: one stroke to each riff, exactly where the treble is. So the snare does what the
# song is named for: it hunts. Through each lead it slides a sixteenth later each half bar, out to the back of the
# riff and home again (bar by bar it falls on sixteenths 1 and 10, 3 and 12, 4 and 11, 2 and 9, then 0 and 8), and
# in the lead's last bar it lands on beats one and three with the two crashes that mark home. The china's eighths and
# the kick go on as they were, so the bar is still there to be pushed against. As many snare strokes as before.
# the rows of the first extent where the snare hunts (from:to) ; its velocity. "" = v8.
HUNT = os.environ.get("C10T3_HUNT", "100:118;0.95")
CALLS_1 = [L for L, c in enumerate("pppb" * 3) if c != "p"]
CALLS_2 = [L for L, c in enumerate("pbpbps" * 2) if c != "p"]
BREAKS, BREAK_HITS = [], []          # the calls' spans (sixteenths) and the kit's notes in them


def lead_mode(k, calls):
    """What row k of an extent is: `call` (the two rows of a called lead end), `home` (of a plain one), or neither."""
    if not FORM or k % 10 < 8:
        return ""
    return ("call" if k // 10 in calls else "home") + str(k % 10 - 8)


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "g": "snare", "h": "hat", "c": "cym", "x": "cym", "rb": "ride", "rd": "ride"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece in ("h", "rb", "rd") else 0.25, "pitch": piece, "vel": round(vel, 3)})


def row_notes(row, s16, root, w=(1, 1), kicks="hunt", bell=True, gtrs=True, teeth=False, mode="", trs=None):
    """One row on the band from `s16`: the five bells in the row's order, then the tenor. The treble is open and loud
    and w[0] sixteenths long; the tenor is w[1] muted chugs; every other bell one muted sixteenth. The kick goes with
    the treble and each of the tenor's chugs (`all`: on every sixteenth); a church bell doubles the treble three
    octaves up."""
    t = s16
    call, bare = mode.startswith("call"), mode == "bare"
    if call:
        BREAKS.append((s16, s16 + 4 + sum(w)))
    for b in tuple(row) + (6,):
        n = w[0] if b == 1 else w[1] if b == 6 else 1
        for j in range(n if b == 6 else 1):                 # the tenor's chugs; any other bell is one note
            v = 1.0 if b == 1 else (0.95 if j == 0 else 0.9) if b == 6 else 0.85
            if call:
                v = float(FORM.split(";")[1])
            for tr in ((trs or G4) if gtrs else ()):
                if bare and b not in (1, 6):
                    continue
                if b == 1 or call:
                    add(tr, t + j, n if b == 1 else 1, F1 + root + PITCH[b], v)
                else:
                    add(tr, t + j, 1, F1 + root + PITCH[b], v, pm=1)
            for tr in (("bass", "fuzz") if teeth else ("bass",)):
                add(tr, t + j, n if b == 1 else 1, F1 + root + PITCH[b], v if call else (0.95 if j == 0 else 0.9) if b in (1, 6) else 0.85)
        for j in range(n):
            if b in (1, 6) and (j == 0 or b == 6):
                drum("k", t + j, 0.95 if j == 0 else 0.9)
            elif call and j == 0:
                drum("k", t, 0.9)
            elif kicks == "all":
                drum("k", t + j, 0.62)
        if call:                                            # the kit rings the row
            if b == 1:
                BREAK_HITS.append(("c" if mode.endswith("0") else "x", t, 0.9))
            elif b == 6:
                BREAK_HITS.extend(("s", t + j, round(0.95 - 0.05 * (n - 1 - j), 3)) for j in range(n))
            else:
                BREAK_HITS.append(({2: "t1", 3: "t2", 4: "t3", 5: "ft"}[b], t, 0.85))
        elif mode.startswith("home") and b == 1:
            BREAK_HITS.append((FORM.split(";")[0].split(",")[int(mode[-1])], t, 0.8 if mode.endswith("0") else 0.7))
        if bell and b == 1:
            T.setdefault("bell", []).append({"at": round(t / 4, 4), "len": 1.5, "pitch": nm(F1 + root + PITCH[1] + 36), "vel": 0.6})
        t += n


def slow_rounds(b0, rows, root=0, vel=0.8):
    """The bells alone, ringing rounds: a row every three beats (eighth notes), the tenor a little harder."""
    for r in range(rows):
        for i in range(6):
            T.setdefault("bell", []).append({"at": b0 * 4 + (r * 6 + i) * 0.5, "len": 3.0, "pitch": nm(F1 + root + PITCH[i + 1] + 36), "vel": round(min(1.0, vel * (1.12 if i == 5 else 1.0)), 3)})


def chant(at, beats, line=None, first=None, step=3.0):
    """Two low voices a fifth apart over a bowed floor. Held (v2); or, with `line` (v10), singing a note to each
    row of the bells from `first`, `step` beats apart, the last note held to the end."""
    T.setdefault("drone", []).append({"at": at, "len": beats, "pitch": "F1", "vel": 0.5})
    if CHANT and line is not None:
        steps, gap = [int(x) for x in CHANT.split(";")[0].split("|")[line].split(",")], float(CHANT.split(";")[1])
        for i, d in enumerate(steps):
            t0 = first + i * step
            ln = (at + beats - t0) if i == len(steps) - 1 else step - gap
            for base, v in ((41, 0.6), (48, 0.5)):                   # F2 and the C above it
                T.setdefault("chant", []).append({"at": round(t0, 4), "len": round(ln, 4), "pitch": nm(base + d), "vel": v})
        return
    for p, v in (("F2", 0.6), ("C3", 0.5)):
        T.setdefault("chant", []).append({"at": at, "len": beats, "pitch": p, "vel": v})


def gong(at, vel):
    T.setdefault("gong", []).append({"at": at, "len": 12.0, "pitch": TOWER.split(";")[5], "vel": vel})


def beat(b0, b1, kind, per=3):
    """The kit over a stretch (the kick is written with the rows). a: half time, the snare on three, china on the
    quarters. b: the backbeat, the hat in eighths. c: the backbeat, china in eighths."""
    for b in range(b0, b1):
        for p in ((8,) if kind == "a" else (4, 12)):
            drum("s", b * 16 + p, 0.95)
        if kind == "b":
            for p in range(0, 16, 2):
                drum("h", b * 16 + p, 0.62 if p % 4 == 0 else 0.48)
        else:
            for p in range(0, 16, 4 if kind == "a" else 2):
                drum("x", b * 16 + p, (0.6 if p == 0 else 0.5) if kind == "a" else (0.52 if p % 4 == 0 else 0.42))
        if (b - b0) % per == 0:              # where the row and the bar line meet
            drum("c", b * 16, 0.9 if b == b0 else 0.7)


def fill(b):
    """The last half bar before bar `b`."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)


def hit(b, beats, root=0):
    """One chord from the whole band, left to ring."""
    for tr in G4:
        add(tr, b * 16, beats * 4, ",".join(nm(F1 + root + i) for i in (0, 7, 12, 19)), 0.95)
    add("bass", b * 16, beats * 4, F1 + root, 0.95)
    drum("k", b * 16, 0.95)
    drum("c", b * 16, 0.95)


def compose():
    # the bells alone: rounds, slowly, five times; a drone under them. No band.
    slow_rounds(INTRO, 5)
    if TOWER:
        chant(0, 15.5, line=0, first=0)
    else:
        T.setdefault("home", []).append({"at": 0, "len": 15.5, "pitch": "F1", "vel": 0.5})
    # the band takes the row up at twice the speed: rounds, sixteen times, the row turning against the bar
    for r in range(ROUNDS_N):
        row_notes(ROUNDS, BAND * 16 + r * L1, 0, W1)
    beat(BAND, PART1, "a", meet(L1))
    fill(PART1)
    # the first extent: Plain Bob Doubles. Forty rows on F, forty on Ab, forty on B
    bare = [int(x) for x in FORM.split(";")[2].split(":")] if FORM else [0, 0]
    for k, row in enumerate(EXTENT_1):
        row_notes(row, PART1 * 16 + k * L1, KEYS_1[k // 40], W1, kicks="all" if k >= 80 else "hunt",
                  mode=lead_mode(k, CALLS_1) or ("bare" if bare[0] <= k < bare[1] else ""))
    for i, kind in enumerate("abc"):
        beat(PART1 + T1 * i, PART1 + T1 * (i + 1), kind, 10 ** 6 if FORM else meet(L1))
        fill(PART1 + T1 * (i + 1))
    if HUNT:                             # v9: the snare leaves the backbeat and follows the treble
        r0, r1 = (int(x) for x in HUNT.split(";")[0].split(":"))
        t0, t1 = PART1 * 16 + r0 * L1, PART1 * 16 + r1 * L1
        T["snare"] = [n for n in T["snare"] if not (t0 / 4 <= n["at"] < t1 / 4)]
        for k in range(r0, r1):
            drum("s", PART1 * 16 + k * L1 + EXTENT_1[k].index(1), float(HUNT.split(";")[1]))
    # it has come round. One chord, and the bells alone again: rounds, slowly, over a drone and a pad
    hit(MIDDLE, 6)
    slow_rounds(MIDDLE + 1, 9)
    if TOWER:
        gong(MIDDLE * 4, 0.9)
        chant(MIDDLE * 4 + 2, 29.5, line=1, first=(MIDDLE + 1) * 4)
    else:
        T.setdefault("home", []).append({"at": MIDDLE * 4, "len": 31.5, "pitch": "F1", "vel": 0.5})
        for p in ("F2", "C3"):
            T.setdefault("air", []).append({"at": (MIDDLE + 1) * 4, "len": 27.5, "pitch": p, "vel": 0.45})
    fill(PART2)
    # the second extent: Grandsire Doubles, on F, Ab and C
    for k, row in enumerate(EXTENT_2):
        row_notes(row, PART2 * 16 + k * L2, KEYS_2[k // 40], W2, kicks="all" if k >= 80 else "hunt",
                  gtrs=not FUZZ or k >= int(FUZZ.split(";")[3]), teeth=bool(FUZZ),
                  mode=lead_mode(k, CALLS_2) or ("bare" if bare[0] <= k < bare[1] else ""),
                  trs=G4B if RIG2 and k >= int(RIG2.split(";")[5]) else G4)
    if FUZZ and FORM and int(FUZZ.split(";")[3]) % 10 not in (8, 9, 0):     # v10: the guitars' entry is not at a home any more: its own crash
        drum("c", PART2 * 16 + int(FUZZ.split(";")[3]) * L2, 0.85)
    for i, kind in enumerate(FORM.split(";")[3] if FORM else "bac"):
        beat(PART2 + T2 * i, PART2 + T2 * (i + 1), kind, 10 ** 6 if FORM else meet(L2))
        fill(PART2 + T2 * (i + 1))
    if HARM:                             # v7: the riff in harmony, on two more guitars
        r0, r1 = (int(x) for x in HARM.split(";")[3].split(":"))
        steps, up, scale = int(HARM.split(";")[4]), int(HARM.split(";")[5]), sorted(PITCH.values())
        for k in range(r0, r1 + 2):
            t, root, call = PART2 * 16 + k * L2, KEYS_2[k // 40], lead_mode(k, CALLS_2).startswith("call")
            assert call == (k >= r1), "the harmony must end on a call"
            for b in tuple(EXTENT_2[k]) + (6,):
                n = W2[0] if b == 1 else W2[1] if b == 6 else 1
                i = scale.index(PITCH[b]) + (0 if call else steps)
                pitch = F1 + root + up + scale[i % 6] + 12 * (i // 6)
                for j in range(n if b == 6 else 1):
                    for tr in ("hl", "hr"):
                        if b == 1 or call:
                            add(tr, t + j, n if b == 1 else 1, pitch, 1.0)
                        else:
                            add(tr, t + j, 1, pitch, (0.95 if j == 0 else 0.9) if b == 6 else 0.85, pm=1)
                t += n
    if CLIMB:                            # v4: the lead climbs the row, slowly, over the last third; the snare on every beat at the end
        base, per, sv = int(CLIMB.split(";")[2]), float(CLIMB.split(";")[3]), float(CLIMB.split(";")[4])
        b0 = CLIMB_B0
        for i, iv in enumerate(sorted(PITCH.values())):
            T.setdefault("lead", []).append({"at": (b0 + i * per) * 4, "len": round(per * 4 - 0.06, 4), "pitch": nm(base + iv), "vel": 0.85})
        top = b0 + 6 * per
        T.setdefault("lead", []).append({"at": top * 4, "len": round((LAND - top) * 4 - 0.25, 4), "pitch": nm(base + 12), "vel": 0.95})
        for b in range(LAND - 4, LAND):
            for q in (0, 8):
                drum("s", b * 16 + q, sv)
    # the landing: rounds on F, twenty-four times, and the bells ring rounds over the band at half its speed
    for r in range(LAND_N):
        row_notes(ROUNDS, LAND * 16 + r * L1, 0, W1, bell=False)
    beat(LAND, END, "c", meet(L1))
    slow_rounds(LAND, int((END - LAND) * 4 / 3) if RHYTHM else 12, vel=0.9)
    # the end: one chord, and the tenor tolls
    hit(END, 10)
    if TOWER:
        gong(END * 4, 1.0)
        chant(END * 4 + 2, 9.5, line=2, first=END * 4 + 2, step=4.0)     # two beats after each toll: the bell, then the voices
    for i, v in enumerate((0.9, 0.7, 0.5)):
        T.setdefault("bell", []).append({"at": (END + i) * 4, "len": 4.0, "pitch": nm(F1 + 36), "vel": v})
    # v6: in a call the kit stops its beat (and the fill that led to a key change goes: the call is the fill) and rings the row
    for tr in ("snare", "hat", "cym", "toms"):
        T[tr] = [n for n in T.get(tr, []) if not any(a / 4 <= n["at"] < z / 4 for a, z in BREAKS)]
    for piece, t, v in BREAK_HITS:
        drum(piece, t, v)
    for a, z in BREAKS:                  # and the band comes back in on a crash
        if not any(a2 == z for a2, _ in BREAKS) and not any(n["at"] == z / 4 and n["pitch"] == "c" for n in T["cym"]):
            drum("c", z, 0.8)


def song():
    compose()
    HARM_DIP = []
    if HARM and CLIMB:        # the guitars' bus comes down a little while six guitars play (the lane is the climb's)
        h0, h1 = (PART2 * 4 + int(x) * L2 / 4 for x in HARM.split(";")[3].split(":"))
        HARM_DIP = [[f"{h0 - 0.5:g}b", 0], [f"{h0:g}b", float(HARM.split(";")[7])], [f"{h1 + 2 * L2 / 4 - 0.25:g}b", float(HARM.split(";")[7])], [f"{h1 + 2 * L2 / 4:g}b", 0]]
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    dtop = ["lp cutoff=14250 q=0.8"]
    main = "ct-twin fx.1.model='5150' fx.2.mic=0.5 fx.2.cone={}"            # the takes it had: a 5150
    dbl = "ct-twin fx.1.model='nolly' fx.2.mic=0.35 fx.2.cone={}"           # a second take a side through another amp, microphone and cone
    GM, GD = os.environ.get("C10T3_GMAIN", "-0.7dB"), os.environ.get("C10T3_GDBL", "-1.5dB")        # each pair as loud as the other, alone; the four as loud as Odd Sympathy's two
    tracks = [
        {"name": "gl", "patch": main.format(10), "gain": GM, "pan": -1, "out": "gtrs"},
        {"name": "gr", "patch": main.format(11), "gain": GM, "pan": 1, "out": "gtrs"},
        {"name": "gl2", "patch": dbl.format(16), "gain": GD, "pan": -0.75, "out": "gtrs"},
        {"name": "gr2", "patch": dbl.format(17), "gain": GD, "pan": 0.75, "out": "gtrs"},
        *([{"name": tr, "patch": RIG2.split(";")[0].format(RIG2.split(";")[2].split(",")[i]), "gain": RIG2.split(";")[1], "pan": (-0.75, 0.75)[i], "out": "gtrs",
            "fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*RIG2.split(";")[3].split(":"))]}]} for i, tr in enumerate(("jl", "jr"))] if RIG2 else []),
        *([{"name": tr, "patch": HARM.split(";")[0].format(HARM.split(";")[6].split(",")[i]), "gain": HARM.split(";")[1],
            "pan": (-1, 1)[i] * float(HARM.split(";")[2]), "out": "gtrs"} for i, tr in enumerate(("hl", "hr"))] if HARM else []),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        # the kick's fader: down where it plays every sixteenth (the last third of each extent)
        *([{"name": "fuzz", "patch": FUZZ.split(";")[0], "gain": {"value": FUZZ.split(";")[1], "mod": [{"src": "auto.open", "amount": 1}]}, "pan": 0,
            "fx": [{"type": "eq", "bands": [f"hp cutoff={RIG2.split(';')[4] if RIG2 else FUZZ.split(';')[2]}"]}],
            "auto": {"open": {"points": [["0b", float(FUZZ.split(";")[4])], [f"{PART2 * 4 + int(FUZZ.split(';')[3]) * L2 / 4 - 0.5:g}b", float(FUZZ.split(";")[4])],
                                         [f"{PART2 * 4 + int(FUZZ.split(';')[3]) * L2 / 4:g}b", 0]], "curve": 0}}}] if FUZZ else []),
        {"name": "kick", "patch": kit, "gain": {"value": "2dB", "mod": [{"src": "auto.all", "amount": 1}]}, "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}],
         "auto": {"all": {"points": [["0b", 0]] + [pt for b0, n in ((PART1 + 2 * T1, T1), (PART2 + 2 * T2, T2)) for pt in ([f"{b0 * 4 - 0.5}b", 0], [f"{b0 * 4}b", KICK_ALL], [f"{(b0 + n) * 4 - 0.5}b", KICK_ALL], [f"{(b0 + n) * 4}b", 0])], "curve": 0}}},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        # the cymbals' fader: down where the china plays eighths (the last third of each extent, and the landing)
        {"name": "cym", "patch": kit, "gain": {"value": "-4.5dB", "mod": [{"src": "auto.busy", "amount": 1}]}, "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air,
         "auto": {"busy": {"points": [["0b", 0]] + [pt for b0, b1 in ((PART1 + 2 * T1, PART1 + 3 * T1), (PART2 + 2 * T2, END)) for pt in ([f"{b0 * 4 - 0.5}b", 0], [f"{b0 * 4}b", CYM_BUSY], [f"{b1 * 4 - 0.5}b", CYM_BUSY], [f"{b1 * 4}b", 0])], "curve": 0}}},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "lead", "patch": CLIMB.split(";")[0], "gain": CLIMB.split(";")[1], "pan": 0, "sends": {"hall": "-12dB"}}] if CLIMB else []),
        # the bells' fader: down in the landing, where twelve slow rows of six ring into one another over the full band
        {"name": "bell", "patch": "modal-bell", "gain": {"value": os.environ.get("C10T3_BELL", "-18dB"), "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0.1, "sends": {"hall": "-8dB"},
         "auto": {"lvl": {"points": [["0b", 0], [f"{LAND * 4 - 1}b", 0], [f"{LAND * 4}b", BELL_LAND], [f"{END * 4 - 1}b", BELL_LAND], [f"{END * 4}b", 0]], "curve": 0}}},
        *([{"name": "chant", "patch": TOWER.split(";")[0], "gain": CHANT.split(";")[2] if CHANT else TOWER.split(";")[1], "pan": -0.1, "sends": {"hall": TOWER.split(";")[2]}},
           {"name": "gong", "patch": TOWER.split(";")[3], "gain": TOWER.split(";")[4], "pan": 0.2, "sends": {"hall": "-8dB"}},
           {"name": "drone", "patch": TOWER.split(";")[6], "gain": TOWER.split(";")[7], "pan": 0.2, "sends": {"hall": "-12dB"}}] if TOWER else
          [{"name": "home", "patch": "contrabass-tight", "gain": "-9dB", "pan": 0.3, "sends": {"hall": "-12dB"}},
           {"name": "air", "patch": "juno-pad", "gain": "-13dB", "pan": 0.15, "sends": {"hall": "-8dB"}}]),
    ]
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    return {
        "about": ("chirpers X (Common Time), track 3 by chirper-zero: \"Plain Hunt\". One row of six sixteenths (Eb C B Ab Gb and a low F "
                  "that always comes last) rung in every order by the bell-ringers' rule that a note may only swap places with its "
                  "neighbour: two extents, 240 rows, none repeated within either, each coming back to the scale it began on. The "
                  "highest note walks through the row and back all piece long, with the kick and a church bell on it. "
                  + ("Since v5 the highest note is long and the low F repeated, so the row is a riff: eight sixteenths in the first "
                     "extent, ten in the second." if RHYTHM else "v1 is the skeleton.")),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}}},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB"] + dtop}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": dtop}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.under", "amount": 1}]}}] if CLIMB else [])
                           + [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"],
                     **({"auto": {"under": {"points": [["0b", 0]] + HARM_DIP + [[f"{CLIMB_B0 * 4 - 0.5}b", 0], [f"{CLIMB_B0 * 4}b", float(CLIMB.split(";")[5])],
                                                       [f"{LAND * 4 - 0.5}b", float(CLIMB.split(";")[5])], [f"{LAND * 4}b", 0]], "curve": 0}}} if CLIMB else {})},
            "low": {"fx": [{"type": "eq", "bands": ["peak cutoff=44 q=1.5 gain=-7dB", "peak cutoff=90 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": ["peak cutoff=170 q=1.2 gain=-3dB"]}]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T3_MASTER", "2.7dB" if RHYTHM else "3.1dB")}]},
        "tracks": tracks,
    }


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
