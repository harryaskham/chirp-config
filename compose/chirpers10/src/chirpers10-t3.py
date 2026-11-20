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
# v18: THE CHANT IS MEN, AND THEY HAVE WORDS (Harry, 17 Nov 00:26, asked "Do you hear men chanting now?": "I hear it,
# but it is a synth, not men"). The line he heard was right and the singer was wrong: `fof-chant` is one formant
# voice with a mouth that moves on an LFO between "o" and "u": no consonants, no breath, no second man. The same line
# is now sung by the engine's SINGING voice as a choir (`voice-choir`: five singers on a line, each with his own
# size, entry and drifting tuning), with larger tracts (basses), and the upper voice a fifth above is five more,
# sized to their part: ten men, in the oldest two-part chant (the fifth above, the whole way). And they sing WORDS,
# because a mouth that makes consonants is what tells a man from an organ stop: what bells have had cast on them
# for centuries. Under the opening's bells "vivos voco" (I call the living); when the bells come round in the middle
# "mortuos plango, vivos voco" (I mourn the dead, I call the living); after the last tolls "orate" (pray).
# the patch ; its gain ; its hall send ; the words, a syllable to each note of the line (ARPAbet), the three lines
# split by "/". "" = v17 (`fof-chant`).
MONKS = os.environ.get("C10T3_MONKS", "voice-choir synth.layers.0.harmony=[7] synth.layers.0.part_size=1 synth.layers.0.tract=1.18 synth.layers.0.vib_spread=1;-5.5dB;-9dB;"
                       "V IY1|V OW0 S|V OW1|K OW0|OW1/M AO1 R|T UW0|OW0 S|P L AA1 N|G OW0|V IY1|V OW0 S|V OW1|K OW0/OW1|R AA1|T EY0") if CHANT else ""
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
# v14: THE CLIMB IS TREMOLO-PICKED (palette round). The climb was seven notes held three bars each on a sustaining
# lead: on top of the band like an organ (my own doubt since v8, and a choice on the card nobody has answered). The
# last stretch is the song's hardest: the kick is on every sixteenth. Now the lead is on it: the same seven notes,
# each PICKED on every sixteenth with the kick (tremolo picking, the oldest way a metal lead holds a note), on
# another lead: the library's `lead-slap` (the 8-string through a 5150 with one 95 ms echo and a tight room: dry,
# close, where `lead-monster` had a long delay and a big room; `lead-monster` is Running Total's lead too, so the
# two songs' leads are now different instruments). It gets harder as it climbs.
# the patch ; its gain ; the stroke, in sixteenths ; the strokes' velocity at the foot of the climb ; at the top. "" = v13.
TREM = os.environ.get("C10T3_TREM", "lead-slap;-12dB;1;0.8;1.0") if CLIMB else ""
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
# v11: THE BASS'S TONE FOLLOWS THE KEY (whole song; the first read of the song part by part against the eleven
# records). The bass's bus has an eq cut to the low F: a notch on its fundamental (44 Hz), a lift on its octave (90 Hz),
# a compressor after them, then a cut at four times the fundamental (170 Hz). That is right on F. When the ground
# moves up to A flat, B or C the fundamental climbs INTO the lift, the compressor clamps on it, and everything above it
# is pushed down: alone, the bass's 120-250 Hz is 12.1 dB under its total on F, 15.7 on A flat, 18.9 on B, and its
# 1-2 kHz growl 18.8, 22.5, 26.3. So on B and C the bass is all fundamental, and read against the records those
# stretches are 1.2 and 0.7 dB over at 60-120 Hz and 2.1 and 2.6 under at 120-250.
# Now those three eq bands move with the key: a lane on the bass's bus carries the ground in semitones over F (0, 3, 6
# or 7) and each band's frequency follows it (the engine bends a frequency in octaves: a twelfth of the lane). The
# bass keeps the shape it has on F wherever the song goes.
# "1" = on. "" = v10.
KEYEQ = os.environ.get("C10T3_KEYEQ", "1")
# v12: THE HARMONY IS HEARD IN THE FIRST CYCLE TOO (section round, 1:26-1:36; the map called 1:04-1:36 static and
# nothing entered in it but crashes). Harry on the harmony guitars of the second cycle: "Keep it, louder". They were
# kept out of the first cycle so that the second would have something of its own. But the riff laid bare is in both
# cycles at the same place, and he kept that ("Shape: keep all three"): a thing that returns. So the harmony now makes
# a first, short appearance where the second cycle has its long one: the LAST LEAD of the stretch on A flat (four bars,
# 1:26-1:34), and it joins the break after it an octave up, as it does at 4:09. The second cycle still has more of
# it (eleven bars), after its own break.
# (Tried first and not kept: the stretch put together a pair of guitars at a time, each rig alone for five bars. On
# the bench one pair alone was 1.2 dB down for ten bars after the five bare ones, the guitars 3 dB under the bass;
# and Harry had just called five bars of bass alone "Too long alone". With the lone pair made as loud as the four,
# nothing would be heard: through this cabinet the two amps differ by less than 1.5 dB in any band.)
# the rows of the first extent in harmony (from:to; the call after them is played in unison). "" = v11.
HARM1 = os.environ.get("C10T3_HARM1", "70:78") if HARM else ""
CALLS_1 = [L for L, c in enumerate("pppb" * 3) if c != "p"]
CALLS_2 = [L for L, c in enumerate("pbpbps" * 2) if c != "p"]
BREAKS, BREAK_HITS = [], []          # the calls' spans (sixteenths) and the kit's notes in them


# v13: THE BELL IN THE HUNT (section round, 2:40-3:12: the second extent's first stretch, which the section map
# called static: twenty-five bars of the riff on F under one beat). The second extent is Grandsire, and what makes
# Grandsire Grandsire is that TWO bells hunt: the treble, and one more, "the bell in the hunt", which walks through
# the row with it; and what a call does in Grandsire is put a DIFFERENT bell into the hunt. Through twelve versions
# only the treble's walk could be heard (the long open note, the kick). Now, from the second lead of the stretch
# (2:44), the bell in the hunt is heard too: its note is left open on the guitars and the drummer's left hand strikes
# it on that bell's own tom (the toms the kit already rings the calls on). So each row has two accents, and they
# walk through the row against each other, cross, and part. After the call at 2:55 the accent is on another note
# and another tom: the third bell has gone into the hunt in place of the second. The ringers' rule made audible.
# (The tom sounds with the snare where the backbeat falls, three rows in eight: leaving it out there broke the walk.)
# the rows of the second extent in which it is marked ; its tom's velocity ; its guitar note's. "" = v12.
HUNT2 = os.environ.get("C10T3_HUNT2", "10:38;0.8;0.95")
HUNT_HITS = []


def in_the_hunt(extent):
    """For each row of a Grandsire extent, the bell (not the treble) that is hunting: the one whose walk through
    the lead's first eight rows only turns at the front or the back."""
    def hunts(seq, b):
        pos, last, stayed = [r.index(b) for r in seq], None, False
        for a, c in zip(pos, pos[1:]):
            d = c - a
            if abs(d) > 1 or (d == 0 and a not in (0, 4)):
                return False
            if d == 0:
                stayed = True
                continue
            if last is not None and d != last and not stayed:
                return False
            last, stayed = d, False
        return True
    out = []
    for j in range(len(extent) // 10):
        seq = [ROUNDS if j == 0 else extent[10 * j - 1]] + list(extent[10 * j:10 * j + 8])
        bells = [b for b in (2, 3, 4, 5) if hunts(seq, b)]
        assert len(bells) == 1, "one bell in the hunt to a lead"
        out += bells * 10
    return out


# v15: THE TREBLE IS A TREBLE, AND IN GRANDSIRE TWO BELLS RING (palette round). Through the band's passages a church
# bell rings the treble's place in every row. It was the same great bell as the tower's, hum and all: a note every
# second with seven seconds of ring, so three or four were always sounding, and alone that bell was within 3 to 5 dB
# of the WHOLE band from 500 Hz to 1 kHz in every stretch, and within 4.5 dB at 250-500 Hz in the last one (where
# the band reads 3.3 dB over the records). A treble is the lightest bell of a ring; the weight is the tenor's.
#   1. In the band the row's bell is now its own instrument (`treble`): the same bell with its hum, the octave under
#      its note, taken down (a high-pass just under its note, which follows the key). The tower's bells (the opening,
#      the middle, the landing) are untouched: they are the ones Harry called ominous.
#   2. In the second cycle the BELL IN THE HUNT rings too. Grandsire is the method with two hunting bells, and since
#      v13 the second one is marked by a tom and an open note for a stretch; now it is a BELL, through the whole
#      second cycle, a third to a fifth under the treble and softer. So two bells walk through each row against each
#      other, and at every call the lower one changes its note: C, then B, then A flat, then back (over the ground).
#      The first cycle has one bell in the hunt and one bell ringing; the second has two and two.
# the high-pass under the treble's note on F, Hz : its q ; the second bell's velocity (the treble's is 0.6). "" = v14.
TREBLE = os.environ.get("C10T3_TREBLE", "420:0.7;0.45")


# v16: THE LANDING LANDS (palette round). The whole second cycle leads to one bar: the extent comes round, the lead
# reaches the top of its climb, and the band lands on rounds on F (5:02). chirp-eco's seams.py read that bar in the
# finished file: the climb -9.7 LUFS, the landing -9.6. Parts come and go there (the lead and the fuzz leave, the
# first pair of doubles comes back) and nothing arrives. Two things, both instruments the song already has, in a
# place they have never been:
#   1. BOTH RIGS. The first cycle's doubles (gl2/gr2) and the second cycle's (jl/jr, the small cabinet) have never
#      sounded together: one replaced the other at 4:12. On the landing all six guitars play rounds: the two rings
#      of the two methods, home together.
#   2. THE LEAD'S LAST NOTE. The lead picks its top note for four bars and stopped a sixteenth before the landing:
#      the climb's last note was never played. Now it is: one stroke of that C on the landing's first beat, let ring.
# the guitars added on the landing (comma-separated) ; beats the lead's last note rings (0 = none) ; its velocity. "" = v15.
HOME = os.environ.get("C10T3_HOME", "jl,jr;8;1.0") if RIG2 and CLIMB else ""


# v17: THE HARMONY OPENS (section round, 3:59-4:09, in the window 3:44-4:16 the map calls static in tone and "little
# new"). The second cycle's harmony guitars play the riff a third above it for two whole leads, nineteen rows of
# the same interval: Harry kept them ("Keep it, louder") and they then stood still. Now they move as twin guitars
# do: the first lead in THIRDS, as it was; the second lead in SIXTHS (four steps up the riff's own six-note scale
# where it was two: the tenor F takes C, G flat takes E flat, A flat takes F, B takes G flat, C takes A flat, the
# treble's E flat takes B). The harmony climbs a fourth as the stretch nears the key change, hands the top of the
# band to the call (unison, an octave up) and then to the lead's climb. Thirds, sixths, unison, lead.
# the row of the second extent from which the harmony is wider ; its scale steps up there. "" = v16 (thirds throughout).
SIXTHS = os.environ.get("C10T3_SIXTHS", "70;4") if HARM else ""
# v19, the handstroke gap (section, first extent on B). The head of every pair of
# these rows is the SAME bell. The two inner guitars stop doubling and ring it
# to each other. Main guitars, bass, kick, snare and actual bells keep the grid.
HANDSTROKE = os.environ.get("C10T3_HANDSTROKE", "1") if W1 == (2, 2) else ""
# v20: hear the pair *about to swap* as an interval on the inner guitars.
# Incoming bell's register above the row; empty restores v19.
CROSS = os.environ.get("C10T3_CROSS", "12" if HANDSTROKE else "")
# v21: half-muffled backstrokes from the last four rounds through the first
# eight changes. The tower bells and the lead's two home rows are not muffled.
# Empty restores v20; switching off v20's crossings still restores v19.
MUFFLE = os.environ.get('C10T3_MUFFLE', '3.5' if CROSS and TREBLE and W1==(2,2) else '')
# v22: THE TOWER RINGS THE HUNT (whole song). The tower's own bells had only ever rung rounds: every change in the
# song was the guitars'. When the first extent comes round (2:16) the tower now rings the method the song is named
# for, slowly and bare: ten changes of plain hunt, the treble struck a little harder so its walk to the back and
# home can be followed, the tenor behind. They are the orders the band's first nine riffs had (0:16), and the tenth
# is rounds. The chant sings a note to each change from the first; the drummer comes back by ringing that last row
# with the tower (a tom to each bell, the snare for the tenor) in place of his fill, and the bass sets off.
# the treble's velocity (the other bells keep 0.8, the tenor 0.896). "" = v21 (rounds, nine times). It is on only
# while every earlier switch is, so each of them still gives exactly what it gave at v21.
TOWERHUNT = os.environ.get('C10T3_TOWERHUNT', '0.95' if all((MUFFLE, MONKS, FORM, FUZZ, HUNT, HUNT2, HARM1, SIXTHS, HOME, TREM, KEYEQ)) else '')
# v23: ONE LEAD AT TWO SPEEDS (section round, 1:06-1:26, in the window 1:04-1:36 the map calls "little new"). Each
# third of the first extent has a figure for the inner pair of guitars (the crossings on F, the handstroke on B),
# and A flat had none: after the bare lead the four simply played two leads in unison. Now, when the whole riff
# comes back, only the outer pair and the bass take it. The inner pair rings the SAME lead at half the speed, an
# octave up and every bell open: a bar to a row, the treble a quarter note, the tenor two muted eighths. So one lead
# is rung once slowly while it and the next are rung fast under it, as the tower rings over the band at the
# landing, but here with the changes. Both leave from home together and come home together at 1:24; and at the
# fast riff's first home (1:15) the slow treble, then lying behind, falls on the same beat as the fast one.
# (First bench, an octave up and at the pair's own level: the riff's second harmonics are the slow notes'
# fundamentals, and read in the mix the slow note was the strongest pitch in only 42% of its notes. Two octaves up it
# was 54%, but still 1.3 dB under the outer pair, where the harmony guitars Harry kept sit 1.2 dB over it. With the
# inner pair's fader 2 dB up for these ten bars it was 62%, and the stretch read 0.15 LU OVER the harmony's entrance
# it leads to (1:26), which is meant as a step up. So 1 dB: the stretch stays under that entrance.)
# the rows of the first extent under the slow ring (from:to; it rings the first half of them) ; semitones it is above
# the riff ; the velocity of its bells (the treble's is 1.0) ; the inner pair's fader while it rings, dB. "" = v22.
SLOW = os.environ.get('C10T3_SLOW', '50:70;24;0.92;1' if TOWERHUNT and W1 == (2, 2) else '')
# v24, THE RINGERS' TIME: a row of the second extent is ten sixteenths and the kit's bar is sixteen, so row and bar
# line meet every eighth row (five bars). Between two such meetings in the A-flat third, where the kit is in half time,
# the drummer counts the ROW instead: china on its head and its middle, the snare on the middle. Half time at five
# sixteenths to the pulse, eight bars of it where there were five; he is back in four at the next meeting, on a crash.
# The rows of the second extent (from:to). "" = v23.
ROWTIME = os.environ.get('C10T3_ROWTIME', '48:56' if SLOW else '')
# v25: THE FIRST FOUR RUNGS (chirper-alpha; section round, 1:56-2:14: the last two leads of the first cycle, in the
# window 1:36-2:08 the map calls static in tone, nothing entering in it). The second cycle ends with the lead climbing
# the row's own notes from the ground up, seven rungs, to the landing (Harry: "It pulls, and it lands"). The first
# cycle ends on the same kind of stretch (the kick on every sixteenth, the snare hunting) and had nothing over it. It
# now has the START of that climb: the same lead, picked on every sixteenth the same way, climbs the first four rungs
# of the row on B: B, C, D, two bars each, and then F, held three bars until the call. The fourth rung of the row on
# B is F, the song's home: the lead holds F, a tritone over a band still on B, the band answers with the call (the
# whole band in unison, the kit ringing the row), comes round, and lands on that F (2:16). So the first cycle's climb
# stops where the ground is going; the second cycle's (on C, all seven rungs, three bars each) goes to the top. As
# the riff laid bare and the harmony are in both cycles ("Shape: keep all three", "Keep it"), the second climb is now
# a thing that returns, and is finished.
# The snare's hunt, the china, the kick and every guitar and bass note are as they were. The lead stops where the call
# starts, two seconds before the chord, so that its ring has died by 2:16 (it reads 48 dB under the chord's first
# second): the tower's passage is as it was.
# the rows of the first extent under it (from:to) ; rows to a rung (the last rung takes what is left) ; rungs ; the
# strokes' velocity at the foot ; at the top. "" = v24.
FIRST = os.environ.get('C10T3_FIRST', '100:118;4;4;0.75;0.95' if ROWTIME and TREM and W1 == (2, 2) else '')
# v26: NEARLY HOME (chirper-one; whole song). chirper-alpha, reading the rows at v25: the second extent's fourth lead
# (3:09.5-3:19.5) is the song's first eight changes BACKWARDS. The band is unwinding its own opening, and after the
# eighth row one plain change would bring it round: the piece would be over at 3:19.5, a hundred seconds early. That
# is what a call is for. The conductor calls a bob and the ringing is turned away, up to A flat.
# Nothing in the song said so. The tower has rung only where the band is home (the opening, the middle, the landing),
# and it is the tower that now hears home coming: for the last six of those rows its bells ring over the band, the
# first time they do so before the landing. They ring the band's own rows at their own pace, three beats to a row
# where the band takes two and a half: the tower sets off on a row three beats before the band reaches it, the band
# gains half a beat a row, and both finish the last row on the same beat (3:19.5). The treble is struck harder, as
# in the middle, so its walk down to the front can be followed: fourth, fifth, fifth, fourth, third, second. The next
# row is rounds. The band plays the bob (the whole band in unison, the kit ringing the row); the tower does not ring
# again until 5:02, when the extent does come round and it rings what it was kept from here.
# The band's own little bells (the one on the treble, the one on the bell in the hunt) rest while the tower rings,
# as they do on the landing, and the bell on the treble is back on the first note of the bob: the note rounds would
# have begun with.
# (First bench, the fader at -7 dB: the tower 10.2 dB under everything else, K-weighted, where the landing's is 8.5
# under; but its hum added 1.5 dB at 250-500 Hz to a stretch that already reads 2.3 over the eleven records. At -9
# it is 12 under: the landing stays the larger event.)
# the tower's rows ; its fader while it rings over the band, dB (the landing's is BELL_LAND). "" = v25.
NEARLY = os.environ.get('C10T3_NEARLY', '6;-9' if FIRST and TOWERHUNT and TREBLE and FORM else '')
# v27: THE PAIR (section round, w6; 2:44.5-2:54.5, the second extent's second lead, which the map still calls static).
# Grandsire is the method in which TWO bells hunt, and they hunt as a pair: the bell in the hunt walks the treble's own
# path through the row, two rows behind it. Since v13 the second one has been marked (an open note, its tom, since v15
# its own small bell) but every guitar still played both in unison with the riff: two accents, never a chord. For
# this one lead, the first in which the second bell is marked, the inner guitars play each of the two hunting bells
# as its PARTNER's note, an octave up: over the treble's long E flat they hold C (a sixth), and on the bell in the
# hunt's C they strike E flat (a tenth). So the pair is heard as a pair: wherever either of them is in the row, both
# notes sound, and with the tenor's F under them they are the open fifth and seventh of the ground. It is the second
# cycle's first harmony, a minute before the harmony guitars (3:47), and it is made of nothing but the two bells the
# method singles out. The outer guitars, the bass and the kit play what they played; after the bob at 2:54.5 a
# different bell goes into the hunt and the inner pair turns to the crossings (v20).
# One note to an amp (the outer pair keeps the written note, the inner pair has the partner's), so no amp has a chord
# to grind. No note is added, removed or moved: sixteen notes on each inner guitar change pitch.
# the rows of the second extent ; semitones over the partner's written note ; trim on those notes, dB. "" = v26.
PAIR = os.environ.get('C10T3_PAIR', '10:18;12;0' if NEARLY and HUNT2 and CROSS else '')
# v28 (chirper-three; section round, w10; the change is the landing's last three bars, 5:12.0-5:18.0): THE BAND
# RINGS DOWN. Bells are not stopped, they are LOWERED: the ringers let them swing a little less at every stroke, the
# rows come round quicker and the strokes close up, until the bells strike all but together and then hang still.
# The landing was rounds sixteen times, the last as the first, and then one chord. Now its first ten rounds stand as
# they were (the arrival Harry heard is untouched), and the last six seconds are the same rounds coming down: a row
# to seven sixteenths (the tenor gives up its second stroke), to six (the treble gives up its length: six even
# strokes), to a beat (the row as a sextuplet), to an eighth, and last to a sixteenth, four times. Down to the
# sextuplets it is the band's unison, as the whole landing is. Faster than that no hand can pick it and no amp can
# say it, so the row is dealt out as a ring is hung: ONE BELL TO EACH OF THE SIX GUITARS, the treble on the far left
# and the tenor on the far right, each struck in its turn, so the row crosses the room twice; at a sixteenth they are
# all but together (a ring 'fires'). The foot follows the treble and the tenor as it always has
# (so it ends in sixteenths), the snare strikes with the four last rows, and the chord at 5:18 is what it was.
# The tower's own bells, the lead's last note, the china and the backbeat are untouched; no row of either extent is
# touched: these are rounds. Sixteen rounds become twenty-three, in the same eight bars.
# how many of the landing's last rows are rung down ; each row's length in sixteenths (they fill those rows' time) ;
# the dealt strokes' velocity ; their height over the riff's own notes, semitones ; how much of its row a bell dealt
# at an eighth rings for (1 = the whole row: all six ringing at once, and nothing crosses the room). "" = v27.
LOWER = os.environ.get('C10T3_LOWER', '6;7,7,6,6,6,4,4,2,2,1,1,1,1;0.97;0;0.5' if PAIR and HOME and W1 == (2, 2) else '')
# v29 (chirper-three; whole song: the opening, 2:17 and the last tolls): THE MEN SING OUT (Harry, 19 Nov 02:22, on the
# chant card: "chant louder, no need for new card/question"). The ten men were 5 to 6 dB under the bells. They are
# not only turned up: they SING harder (every note struck 0.9 for 0.6, which in the voice is more effort and less
# breath, 5.3 dB), the fader comes up 1 dB, and their consonants are held 3 dB back so the S of "vivos" does not
# lead the vowels up (the words' noise was already 11 dB over everything else at 4-8 kHz). At 2:17 and under the
# last tolls that is 6 dB: the men level with everything else that sounds. The opening gets 4.5: any more and the
# eight seconds before the band are as loud as the band's first eight. The bells, the drone and the gong are as
# they were. The patch is a new song-local one (`ph-monks-forte`); `ph-monks` is as chirper-zero left it.
# dB on the chant's fader ; what is added to the choir's patch ; how hard the men sing (the notes' velocity; 0.6 = as
# before) ; dB on the opening's notes alone (the band's entry at 0:08 has to stay a step up) ; the loudness target
# with the men louder (the song's own, -10, is fitted to v28). "" = v28.
LOUDER = os.environ.get('C10T3_LOUDER', '1;synth.layers.0.consonant_level=-3dB;0.9;-1.8;-9.89' if LOWER and MONKS else '')
NEAR_END = PART2 * 4 + 38 * L2 / 4                 # beats: where the fourth lead's bob starts
NEAR_AT = NEAR_END - 3 * int(NEARLY.split(';')[0]) if NEARLY else NEAR_END
NEARLY_PTS = [[f"{NEAR_AT - 1:g}b", 0], [f"{NEAR_AT:g}b", float(NEARLY.split(';')[1])],
              [f"{NEAR_END + 4.5:g}b", float(NEARLY.split(';')[1])], [f"{NEAR_END + 5:g}b", 0]] if NEARLY else []


# v30 (chirper-two, section round, w2 0:32-1:04, which nobody had marked; the change is 0:53.0-0:54.0): THE CONDUCTOR
# CALLS. Since v6 the band breaks wherever a ringing conductor would call a bob or a single: nine times, and nobody
# has ever called. A method does not change course by itself: one ringer, the conductor, shouts "Bob!" as the treble
# strikes in second place on its way down to lead, a row before the lead end, and the ringers change what they would
# have rung. Here he does, once: at the song's FIRST call. As the treble's bell strikes in seconds in the row before
# the call (row 37 of the first extent, 0:53.125) a man shouts the word. The band stops to hear it: the four guitars
# rest for the whole row, and the bass and the kit for all of it but the tenor's two low F's (0:53.75), which ring
# behind as the tenor always does and are the way back in. Then the call's two rows, in unison, as they were. The
# treble's own bell rings on through the stop, so the row is still marked where the hunt has reached.
# ONCE: the other eight calls are not called (praise is local; and a word said nine times is a tic). The voice is the
# engine's SPEAKING voice (`voice-speech`, which the album had not used: a spoken, not sung, glottis), pressed, on C4
# with a shout's pitch (up 160 cents, then down to 450 under where it began), into the tower's hall.
# MEASURED (raw, while he speaks): he stands at the level of the band he replaces (K -18.7 against -18.9, his peak
# -6.6 against -6.8) and 11.7 dB over what still sounds under him (the bell). THE RECOGNISER reads the word alone as
# "Bob!"; cut from the song it writes "Oh", whatever rests under him (tried: guitars only; guitars and bass; all of
# the band; a 3 kHz lift; a rap voice; a longer vowel). So: a man is heard to call, and the vowel; the two b's are
# not proven in the song.
# his patch ; his gain ; the row of the first extent he calls in (the four guitars rest for it) ; his note ; its
# length, sixteenths ; from which sixteenth of the row ; the pitch's path through the word, cents ; his send to the
# hall ; the word (ARPAbet) ; his eq's bands (comma between; empty: none) ; who else rests besides the guitars
# (tracks, comma between; empty: nobody) : for how many of the row's sixteenths (6 leaves the tenor's two chugs).
# "" = v29.
CALLED = os.environ.get('C10T3_CALLED', 'voice-speech synth.layers.0.join=true synth.layers.0.effort.value=0.7 synth.layers.0.effort_tilt=1 synth.layers.0.ring=0.6;'
                        '-18dB;37;C4;3.2;1;0,120,160,100,-50,-250,-450;-14dB;B AA1 B;;bass,kick,snare,cym,hat,toms:6' if LOUDER and FORM and W1 == (2, 2) else '')


# v31 (chirper-alpha; section round, w8 3:44-4:16, the map's first flagged window; the changes are at
# 3:50.75-3:53.25, 3:57.0-4:02.0 and 4:05.75-4:08.25): THE CHANGES FALL INTO TWO CHORDS. The row's bells are the
# scale's every other note twice over: bells 1, 3 and 5 are a major triad, and bells 2 and 4 with the tenor are a
# minor triad a tritone away (on this ground D major and A flat minor). Mostly the changes shuffle the two
# together. But eight rows of this lead and the next keep the odd bells side by side and the even bells side by
# side, and one of them is the row every ringer knows by name: QUEENS, 1 3 5 2 4 (3:58.25), the two triads
# running down; its mirror, 4 2 5 3 1, is here too (3:52.0). Since v7 the harmony guitars play each bell's
# next-but-one note of the scale (from 3:59.5 the next-but-three: thirds, then sixths), which on these rows is
# another note of the SAME triad: so for those eight rows everything the band sounds is one chord, then the
# other. Nobody wrote that; the method and the harmony Harry kept ("Sixths: keep them") do it. But every note is a
# muted sixteenth, gone before the next, and it goes by as a riff like any other.
# On those rows the INNER pair of guitars now lets the chords ring. In each run of bells that makes a triad, the
# left inner guitar holds the first bell struck and the right inner guitar the second, an octave up: one note to
# an amp, as in v27. Where the odd bells lead (the four rows from 3:57.0, Queens the second): D major held for
# five sixteenths, then A flat minor's third and fifth held for five, over the tenor's three strokes, which are
# its root. Four times: D, A flat minor, D, A flat minor... Where the even bells lead (the two rows at 3:50.75
# and the two at 4:05.75, the last before the bob): the even pair is two quick notes, then D major is held
# through the treble's long note up to the tenor, which the pair then plays as written.
# The outer guitars, the bass, the harmony guitars, the bells and the kit play what they played.
# (Level, benched raw on rows 63-71: as written the pair stands 6.2 to 7.1 dB under everything else row by row,
# K-weighted; holding, at the same fader, it stood 6.0 to 8.3 under and the rows were 0.06 dB quieter: an inner
# voice. With the pair's fader 2 dB up on those rows it stands 4.8 to 5.1 under and the rows read 0.3 to 0.4 dB
# louder.)
# the rows of the second extent it may happen in ; semitones over the written note ; the held notes' velocity ;
# the inner pair's fader on those rows, dB ; the loudness target ("" = unchanged). "" = v30.
CHORDS = os.environ.get('C10T3_CHORDS', '60:78;12;0.95;2;' if CALLED and HARM and W1 == (2, 2) else '')
# v32 (chirper-zero, instrument round): THE TREBLE BELL IS STRUCK. Through the band's passages a church bell rings
# the treble's place in every row (v15 took its hum out and gave the second cycle a second bell). It is the song's
# accent: the one note whose place in the riff slides. READ ALONE AND IN THE MIX at v31: the bell held 37% of
# everything the mix has between 500 Hz and 1 kHz in the first cycle and 32% in the second (-4.3 and -4.9 dB re
# the whole mix's band: as much as the four rhythm guitars together), and the mix read 2.2 to 2.7 dB over the
# records there in every band passage. And it was not heard as strikes: a note every 0.9 s on a bell that rang
# seven seconds, every partial as long as every other, so a strike stood 9.7 dB over the ring it landed on in the
# first cycle and 7.1 in the second (two bells), and tools/presence.py could tell only 14 of 37 strikes from the
# ring in the first cycle and 3 of 40 in the second. The strike was no brighter than the ring (a third of its
# power over 1.2 kHz in both): a bell that is hummed, not struck.
# A BELL'S UPPER PARTIALS DIE FIRST, and a treble is the lightest bell of the ring. So, on this track only (the
# tower's bells at the opening, the middle, 3:10 and the landing are the ones Harry called ominous and are not
# touched): the higher a partial the sooner it dies (`damp` 0.03 -> 1.2: the nominal rings 1.8 s, the partial two
# octaves over the note 0.9 s, where each rang 7), the strike is brighter (`tilt` -1 -> +3 dB an octave: the
# nominal as loud as the prime at the strike, as on a cast bell), and the bell is a small one (4 s where it rang
# 7; let go after 2 s where it was 4). The fader is not moved.
# AFTER: a strike stands 17.9 and 16.0 dB over the ring it lands on; presence.py tells every strike in the first
# cycle and 19 of 40 in the second; each against the mix -11.6 -> -12.3 and -10.9 -> -12.5 dB (K); the strike has
# 55% of its power over 1.2 kHz and the ring 27%. The bell's share of the mix's 500 Hz-1 kHz: -4.3 -> -7.0 and
# -4.9 -> -7.9 dB. THE MIX against the records (no-voice rows) at 500 Hz-1 kHz: first cycle +2.2 -> +1.2, its
# third lead +2.2 -> +1.3, second cycle +2.7 -> +1.7, the harmony +2.6 -> +1.8, the last stretch +2.2 -> +1.1;
# no other band moves more than 0.3; the landing (no treble) is as it was.
# the modes' damp ; their tilt, dB an octave ; the bell's decay ; its release ; the loudness target. "" = v31.
STRUCK = os.environ.get('C10T3_STRUCK', '1.2;3;4s;2s;-9.982' if TREBLE and CHORDS else '')
# v33 (chirper-one, instrument round: the snare drum, all 288 strokes; v32's handoff named it): THE SNARE STEPS BACK
# AND ITS WIRES COME OUT. The same drum as On Its Hinge's and The Other Hand's, and a different fault in each song.
# Here, read alone at its strokes the way tools/drumpunch.py reads a snare on a record, it was not a box (body
# against crack -4.7; six records -3.2): it had NO WIRES (wires against crack -5.6; records 0.0, -0.6 to +1.4),
# because its track took 3 dB off above 7 kHz, and it was TOO LOUD IN THE MIDDLE: by part against the records' drums
# the kit stood 2.6, 5.0, 3.3 and 3.9 dB over from 250 Hz to 4 kHz in the first cycle (4.5, 8.4, 4.2, 2.8 in the
# second), 62 to 96% of it the snare. So: the track's shelf at 7 kHz goes; the wires are tighter (0.85 -> 1.1); the
# crack comes down 4 dB round 2.5 kHz and the box 3 dB at 650 Hz; the body's lift at 200 Hz is 3.5 dB (5); the
# fader 3.5 -> 1.5 dB. No note changes; the send to the snare's dry bus and the kit's bus are as they were.
# the body's lift at 200 Hz, dB (the kit's is 5) ; the wires (0.85) ; the snare track's eq bands, comma between (it
# was 'highshelf cutoff=7000 gain=-3dB') ; its fader (3.5dB) ; the loudness target ('' = unchanged). '' = v32.
# It is on only while no other C10T3_ switch is set, so every older switch gives exactly what it gave.
SNARE = os.environ.get('C10T3_SNARE', '3.5;1.1;peak cutoff=2500 q=0.7 gain=-4dB,peak cutoff=650 q=1 gain=-3dB;1.5dB;-10.067' if STRUCK and not any(
    k.startswith('C10T3_') and k not in ('C10T3_OUT', 'C10T3_SHOW', 'C10T3_SNARE', 'C10T3_RAISE', 'C10T3_SLOWKIT', 'C10T3_OVER', 'C10T3_TENOR') for k in os.environ) else '')
# v34 (chirper-alpha; whole song: its frame; the change is the band's entrance, 0:08-0:12): THE BAND IS RUNG UP.
# The song is a ringing performance from end to end, and since v28 the band is LOWERED at the end. But ringers do not
# start by ringing: a ring is RAISED first, the bells chiming fast and close while they hang low, each stroke taking
# longer as they swing higher, until they are up and ringing rounds at full length. The song had the end of that
# and not the beginning. Now the band's first four rounds are v28's strokes in the other order: the six guitars one
# stroke, four times, with the snare (a ring that fires); the row dealt across the room at an eighth, twice; once
# to the beat; a row of six sixteenths, two of seven; and at 0:12 the row is its full eight and is the riff. The
# kit's bar (china, backbeat, crash) is the same bar; the tower, the men and v21's wrapped rows are untouched.
# how many of the band's first rounds are rung up ; each row's length in sixteenths (they fill those rows' time, and
# never shorten) ; the dealt strokes' velocity ; their height over the riff's own notes, semitones ; how much of its
# row a bell dealt at an eighth rings for ; the loudness target ("" = unchanged). "" = v33 (and, like SNARE, setting
# it does not switch SNARE off).
RAISE = os.environ.get('C10T3_RAISE', '4;1,1,1,1,2,2,4,6,7,7;0.97;0;0.5;' if SNARE and LOWER and W1 == (2, 2) else '')
# v35 (chirper-one; section round, the window 1:04-1:36; the change is 1:06-1:26): THE DRUMMER RINGS THE SLOW LEAD.
# v23 put one lead at two speeds here: the outer pair and the bass ring two leads fast while the inner pair rings the
# first of them once, slowly, two octaves up, a bar to a row. The kit did not know: it kept the backbeat and the hat in
# eighths through it, as before and after, and the map still called the window static, its rhythm the most repeated
# in the song (0.070 bar to bar; the song's median 0.150). The kit already rings the row in every call (a crash for
# the treble, a tom for each of the four bells between, the snare on the tenor), at full speed, for one bar. NOW IT
# RINGS THIS WHOLE LEAD AT THE INNER PAIR'S SPEED, ten bars, stroke for stroke with them: a tom to each of the four
# bells between (t1 t2 t3 ft, high to low as the bells are), so each bar is the four toms in a new order, by the
# ringers' rule; the treble on the RIDE'S BELL (the kit's one bell, not struck anywhere else in the song), which
# walks through the bar an eighth later each bar, to beat three, and back to the downbeat; the tenor's two eighths
# on the snare, on four and its 'and', every bar ('the tenor behind'). The backbeat and the hat's eighths rest for
# the ten bars (two hands); the hat's foot keeps the quarters. The kick, written with the fast rows, the crashes at
# the fast riff's homes, and every guitar and bass note are untouched. At 1:26 the backbeat and the hat come back
# with the harmony guitars.
# The ringing toms are on a track of their own, 3.5 dB under the song's toms and 3 dB down at 350 Hz: at the fills'
# level they stood level with the whole band at 120-500 Hz (the mix +2.4 dB there; now +1.3 and +0.7).
# the toms' velocity ; the piece that is the treble ; its velocity ; the tenor's two snare strokes' velocities ; the
# kit's tracks whose beat rests while he rings (comma-separated) ; the ride track's fader ; the ringing toms' fader
# (a track of their own: the song's toms, 4dB, are its fills and calls) ; their eq bands (| between) ; the velocity of
# the hat's foot on the quarters ('' = none) ; the loudness target ('' = unchanged). '' = v34 (and, like RAISE,
# setting it does not switch SNARE off).
SLOWKIT = os.environ.get('C10T3_SLOWKIT', '0.8;rb;0.9;0.9,0.95;snare,hat;-3dB;0.5dB;peak cutoff=350 q=1 gain=-3dB;0.75;' if RAISE and SLOW else '')
# v36 (chirper-alpha; whole song: its summit, 5:02.0-5:17.9; one new track, `men`): FULGURA FRANGO. The tower's men
# sing what is cast on bells: "vivos voco" at the opening, "mortuos plango, vivos voco" in the middle, "orate" after the
# tolls (v18). The inscription has a third clause, fulgura frango (I break the lightning), and the men had never sung
# with the band: since v1 the tower's bells come over the band at the landing and the men, who sing a note to each of
# the tower's rows everywhere else, were silent there. Now they sing "fulgura frango", twice, over the full band: a
# syllable to each of the ten slow rows, on the line they opened the song with and its way back down, the fifth above
# as always, an octave above the tower's own, and hard; the last "go" holds through the ringing down and stops an
# eighth before the last chord. The level is the tower's own balance: at 2:17 the men stand 1.0 dB over the bells (K),
# here 0.5 over the landing's bells, which is 8.4 dB under everything else. Each syllable's strongest third-octave
# reads +4.6 over everything else in it (-0.4 to +8.7); above 2 kHz the men are 26 to 33 dB under the band, so the
# vowels are heard and the words are not. The "u" is the one in "book": with the one in "food" the first two
# syllables stood 10 to 15 dB under the rest. The cut at 300 Hz is there because the landing's 250-500 Hz is already
# 4.7 dB over the records' (62% of it the bells); with the men it is 6.0, and 500 Hz-1 kHz 0.2 -> 2.3.
# the men's line over the landing, a note to each row the tower rings there (semitones over F) ; its words, a
# syllable a note ; how far above the tower's men they sing, semitones ; what is added to the choir's patch ; their
# fader ; their hall send ; their eq bands ('|' between; '' = none) ; how hard they sing, first note and last (a line
# between) ; the loudness target ('' = unchanged). '' = v35 byte for byte.
OVER = os.environ.get('C10T3_OVER', '0,1,0,3,0,3,1,0,1,0;F UH1 L|G UH0|R AA0|F R AA1 N|G OW0|F UH1 L|G UH0|R AA0|F R AA1 N|G OW0;12;'
                      'synth.layers.0.effort.value=0.4 synth.layers.0.effort_tilt=1 synth.layers.0.consonant_level=-3dB synth.layers.0.tract=1.1;'
                      '-11dB;-9dB;hp cutoff=250|peak cutoff=300 q=1 gain=-6dB;0.9,1.0;' if SLOWKIT and MONKS and LOUDER and LOWER and RHYTHM else '')
CHORD_ROWS = []


def two_chords():
    """v31: on the rows that keep the odd bells together and the even bells together, the inner pair holds each
    triad's first two bells until its last is struck (after the even pair, that is the tenor)."""
    r0, r1 = (int(x) for x in CHORDS.split(';')[0].split(':'))
    up, vel = int(CHORDS.split(';')[1]), float(CHORDS.split(';')[2])
    done = []
    for k in range(r0, r1):
        row = EXTENT_2[k]
        odd = [i for i, b in enumerate(row) if b % 2]
        if odd not in ([0, 1, 2], [2, 3, 4]):
            continue
        a = PART2 * 4 + k * L2 / 4                           # the row's first beat
        n = 3 if odd == [0, 1, 2] else 2                     # the places of the first run
        for tr in ('gl2', 'gr2'):
            mine = sorted((x for x in T[tr] if a <= x['at'] < a + L2 / 4), key=lambda x: x['at'])
            bells, tenor = mine[:5], mine[5:]
            assert len(mine) == 8 and len({x['pitch'] for x in tenor}) == 1, (k, tr, len(mine))
            ends = (bells[n]['at'], a + L2 / 4 if n == 3 else tenor[0]['at'])     # after the even pair the tenor completes it
            first = 0 if tr == 'gl2' else 1                  # which bell of each run this guitar holds
            keep = [] if tr == 'gl2' else [bells[0], bells[n]]
            for run, end in zip((0, n), ends):
                x = bells[run + first]
                midi = NAMES.index(x['pitch'][:-1]) + 12 * (int(x['pitch'][-1]) + 1) + up
                keep.append({'at': x['at'], 'len': round((end - x['at']) * 0.98, 5), 'pitch': nm(midi), 'vel': vel})
            if n == 2:
                keep += tenor                                # the odd run ends at the tenor, which the pair then plays as written
            T[tr] = [x for x in T[tr] if not a <= x['at'] < a + L2 / 4] + keep
        done.append(k)
    assert 69 in done and EXTENT_2[69] == (1, 3, 5, 2, 4), 'Queens'
    CHORD_ROWS[:] = done


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


def coming_pairs(extent, k, hunt=0):
    """For ordinary rows of leads three and four: two bells which trade places
    in the next row. Sound both at the first place; neither reattacks at the
    second. The hunting bell(s), home rows and calls keep their own accents.
    """
    if not CROSS or not (20 <= k < 38 and k % 10 < 8):
        return None
    pairs = {}
    row, after = extent[k:k + 2]
    for i, (a, b) in enumerate(zip(row, row[1:])):
        if 1 not in (a, b) and hunt not in (a, b) and after[i:i + 2] == (b, a):
            pairs[a], pairs[b] = (a, b), ()
    return pairs


def row_notes(row, s16, root, w=(1, 1), kicks="hunt", bell=True, gtrs=True, teeth=False, mode="", trs=None, hunt=0, ring2=0, pairs=None, partner=0):
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
                if pairs and b in pairs and tr in ("gl2", "gr2"):
                    if pairs[b]:
                        # One bell per amp: the outgoing bell on the left,
                        # the incoming one already sounding above it on the right.
                        a, incoming = pairs[b]
                        pitch = PITCH[a] if tr == "gl2" else PITCH[incoming] + int(CROSS)
                        add(tr, t, 1.9, F1 + root + pitch, 0.94)
                    continue
                # Grandsire's two hunting bells leave fewer working pairs to
                # cross. Give those few chords space: between them, the inner
                # amps ring just the two hunters and the tenor's final stroke.
                if pairs is not None and (hunt or ring2) and tr in ("gl2", "gr2"):
                    if b not in (1, hunt, ring2) and not (b == 6 and j == n - 1):
                        continue
                if partner and b in (1, partner) and tr in ("gl2", "gr2") and not call:
                    # v27: each hunting bell as its partner's note, above the outer pair's written one
                    add(tr, t + j, n if b == 1 else 1, F1 + root + PITCH[partner if b == 1 else 1] + int(PAIR.split(";")[1]),
                        v if b == 1 else float(HUNT2.split(";")[2]))
                    if float(PAIR.split(";")[2]):
                        T[tr][-1]["gain"] = f"{float(PAIR.split(';')[2]):g}dB"
                elif b == 1 or call:
                    add(tr, t + j, n if b == 1 else 1, F1 + root + PITCH[b], v)
                elif b == hunt:                             # v13: the bell in the hunt is left open
                    add(tr, t + j, 1, F1 + root + PITCH[b], float(HUNT2.split(";")[2]))
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
        if b == hunt and not call:                          # v13: and struck on its own tom
            HUNT_HITS.append(({2: "t1", 3: "t2", 4: "t3", 5: "ft"}[b], t, float(HUNT2.split(";")[1])))
        if bell and b == 1:
            T.setdefault("treble" if TREBLE else "bell", []).append({"at": round(t / 4, 4), "len": 1.5, "pitch": nm(F1 + root + PITCH[1] + 36), "vel": 0.6})
        elif bell and TREBLE and b == ring2 and not call:   # v15: the bell in the hunt rings too
            T.setdefault("treble", []).append({"at": round(t / 4, 4), "len": 1.5, "pitch": nm(F1 + root + PITCH[b] + 36), "vel": float(TREBLE.split(";")[1])})
        t += n


def handstroke(k, s16, root):
    """Two rows to a bar: say their shared first bell twice, leave air before the next pair."""
    row = EXTENT_1[k]
    back, second_lead = k % 2, k // 10 % 2
    assert row[0] == EXTENT_1[k ^ 1][0]
    tr = ("gl2", "gr2")[back ^ second_lead]      # trade hands for the second lead
    at = s16 - back                             # second stroke anticipates beat three
    up = 12 * (1 + back * second_lead)           # last four replies clear the first by an octave
    head = F1 + root + PITCH[row[0]] + up
    # Distinguish the hands even in mono: a ringing octave stopped on two
    # strings, answered by one shorter picked string. No added pitch class.
    pitch = head if back else f"{nm(head)},{nm(head + 12)}"
    add(tr, at, 3.5 if back else 5, pitch, .96)
    # Close on the ground. The first hand makes room for the early answer;
    # the answering hand chokes its second chug one sixteenth before the bar.
    for j in range(1 + back):
        add(tr, at + L1 - W1[1] + j, .8, F1 + root, .88, pm=1)


def slow_ring(r0, r1, up, vel):
    """Rows r0 .. halfway to r1 of the first extent on the inner guitars at half speed, over rows r0..r1-1."""
    half = (r1 - r0) // 2
    assert r0 % 10 == 0 and (r1 - r0) % 20 == 0 and KEYS_1[r0 // 40] == KEYS_1[(r1 - 1) // 40], "whole leads, in one key"
    # where the fast riff is at home the slow treble is with it: behind at the first, leading at the second
    assert EXTENT_1[r0 + half // 2 - 1].index(1) == 4 and EXTENT_1[r0 + half - 1].index(1) == 0
    t, root = PART1 * 16 + r0 * L1, KEYS_1[r0 // 40]
    for k in range(r0, r0 + half):
        for b in EXTENT_1[k] + (6,):
            n = W1[0] if b == 1 else W1[1] if b == 6 else 1
            for tr in G4[2:]:
                if b == 6:
                    for j in range(n):
                        add(tr, t + 2 * j, 2, F1 + root + up, 0.9, pm=1)
                else:
                    add(tr, t, 2 * n, F1 + root + PITCH[b] + up, 1.0 if b == 1 else vel)
            t += 2 * n
    assert t == PART1 * 16 + r1 * L1


def slow_kit():
    """v35: while the inner pair rings one lead at half speed (v23), the kit rings it with them: a bar to a row, the
    treble on the ride's bell, a tom to each of the four bells between (high to low as the bells are, as in a call),
    the snare on the tenor's two eighths. Its backbeat and its hat rest; the kick, written with the fast rows, and the
    crashes at the fast riff's homes are untouched."""
    f = SLOWKIT.split(";")
    r0, r1 = (int(x) for x in SLOW.split(";")[0].split(":"))
    half = (r1 - r0) // 2
    a, z = PART1 * 16 + r0 * L1, PART1 * 16 + r1 * L1
    assert a % 16 == 0 and z - a == half * 16 and W1 == (2, 2), "a bar to a slow row"
    assert not any(lead_mode(k, CALLS_1).startswith("call") for k in range(r0, r1))
    for tr in [x for x in f[4].split(",") if x]:
        T[tr] = [n for n in T[tr] if not (a / 4 <= n["at"] < z / 4 and n["pitch"] in ("s", "h"))]
    t, sv = a, [float(x) for x in f[3].split(",")]
    for k in range(r0, r0 + half):
        for b in EXTENT_1[k] + (6,):
            n = W1[0] if b == 1 else W1[1] if b == 6 else 1
            if b == 1:
                drum(f[1], t, float(f[2]))
            elif b == 6:
                for j in range(n):
                    if not any(x["at"] == round((t + 2 * j) / 4, 4) for x in T["snare"]):     # (a backbeat left in keeps its own stroke on four)
                        drum("s", t + 2 * j, sv[j])
            else:
                T.setdefault("slowtoms", []).append({"at": round(t / 4, 4), "len": 0.25, "pitch": {2: "t1", 3: "t2", 4: "t3", 5: "ft"}[b], "vel": float(f[0])})
            t += 2 * n
    assert t == z
    if f[8]:                             # the hand has left the hat: the foot keeps it
        for q in range(a, z, 4):
            T["hat"].append({"at": round(q / 4, 4), "len": 0.5, "pitch": "hf", "vel": float(f[8])})


def ringers_time(r0, r1):
    """From one meeting of row and bar line to the next, the kit keeps the row. No guitar, bass or kick note moves:
    the kick was always written with the rows."""
    a, z = PART2 * 16 + r0 * L2, PART2 * 16 + r1 * L2
    assert a % 16 == 0 and z % 16 == 0 and (z - a) // 16 == meet(L2), "from one meeting to the very next"
    assert KEYS_2[r0 // 40] == KEYS_2[(r1 - 1) // 40] and L2 % 2 == 0
    assert not any(lead_mode(k, CALLS_2).startswith("call") for k in range(r0, r1))
    kind = (FORM.split(";")[3] if FORM else "bac")[r0 // 40]
    assert kind == "a", "half time: one snare to a bar, so one to a row"
    for tr, piece in (("snare", "s"), ("cym", "x")):
        T[tr] = [n for n in T[tr] if not (a / 4 <= n["at"] < z / 4 and n["pitch"] == piece)]
    for t in range(a, z, L2):
        drum("x", t, 0.6)
        drum("x", t + L2 // 2, 0.5)
        drum("s", t + L2 // 2, 0.95)
    if not any(n["at"] == z / 4 and n["pitch"] == "c" for n in T["cym"]):
        drum("c", z, 0.8)                # back in four, where they meet


def half_muffled():
    """One face of a bell's clapper is wrapped: only the backstroke is dark.
    Count rows relative to the first change so the alternation carries across
    the bar where the tune starts permuting. The outer players keep every pitch.
    """
    def backstroke(note):
        tick = round(note['at']*4) - PART1*16
        row, place = divmod(tick, L1)
        return -(ROUNDS_N//2) <= row < 8 and row%2==1, place

    for tr in G4:
        kept = []
        for n in T[tr]:
            mute, place = backstroke(n)
            if mute:
                # The inside pair gives up the row, except the tenor's two F's.
                if tr in G4[2:] and place < L1-W1[1]:
                    continue
                n['len'] = round(n['len']*.42,4)
                n['expr'] = {**n.get('expr',{}),'pm':1.0}
            kept.append(n)
        T[tr] = kept
    # Same treble, pitch and striking time; different contact, not a quieter
    # fader on the tower. Copy the events to a separately damped modal voice.
    open_notes, wrapped = [], []
    for n in T['treble']:
        (wrapped if backstroke(n)[0] else open_notes).append(n)
    T['treble'],T['wrapped'] = open_notes,wrapped


def slow_rounds(b0, rows, root=0, vel=0.8):
    """The bells alone, ringing rounds: a row every three beats (eighth notes), the tenor a little harder."""
    for r in range(rows):
        for i in range(6):
            T.setdefault("bell", []).append({"at": b0 * 4 + (r * 6 + i) * 0.5, "len": 3.0, "pitch": nm(F1 + root + PITCH[i + 1] + 36), "vel": round(min(1.0, vel * (1.12 if i == 5 else 1.0)), 3)})


def tower_hunt(at):
    """The tower's bells ring plain hunt from beat `at`: ten changes, a row every three beats, coming round."""
    rows, r = [], ROUNDS
    for i in range(10):
        r = change(r, {5} if i % 2 == 0 else {1})
        rows.append(r)
    # the song's title, whole: the first nine are the rows the band began the first extent with; the tenth is home
    assert rows[-1] == ROUNDS and len(set(rows)) == 10 and rows[:9] == EXTENT_1[:9]
    for k, row in enumerate(rows):
        for i, b in enumerate(row + (6,)):
            vel = float(TOWERHUNT) if b == 1 else 0.896 if b == 6 else 0.8
            T.setdefault("bell", []).append({"at": at + (k * 6 + i) * 0.5, "len": 3.0, "pitch": nm(F1 + PITCH[b] + 36), "vel": vel})
    return at + 30


def nearly_home():
    """The tower rings the last rows before the second extent's fourth lead is called, and stops a change from rounds."""
    rows, k1 = int(NEARLY.split(';')[0]), 38
    assert lead_mode(k1, CALLS_2) == 'call0' and KEYS_2[(k1 + 1) // 40] == 0, 'the lead ends in a call, on F'
    assert list(EXTENT_2[k1 - 8:k1]) == list(EXTENT_1[7::-1]), "the song's first eight changes, backwards"
    assert change(EXTENT_2[k1 - 1], {5}) == ROUNDS and EXTENT_2[k1] != ROUNDS, 'a plain change from rounds; the bob is not one'
    assert NEAR_AT >= PART2 * 4 + (k1 - 8) * L2 / 4 and NEAR_AT * 2 == int(NEAR_AT * 2)
    for k, row in enumerate(EXTENT_2[k1 - rows:k1]):
        band = PART2 * 4 + (k1 - rows + k) * L2 / 4          # where the band starts this row: the tower is ahead of it
        assert 0 <= band - (NEAR_AT + 3 * k) <= 3 and band + L2 / 4 <= NEAR_END
        for i, b in enumerate(row + (6,)):
            vel = float(TOWERHUNT) if b == 1 else 0.896 if b == 6 else 0.8
            T['bell'].append({"at": NEAR_AT + (k * 6 + i) * 0.5, "len": 3.0, "pitch": nm(F1 + PITCH[b] + 36), "vel": vel})
    T['treble'] = [n for n in T['treble'] if not NEAR_AT <= n['at'] < NEAR_END]


def ring_down():
    """v28: the landing's last rows as rounds lowered in peal (see LOWER)."""
    out, sizes, vel = int(LOWER.split(';')[0]), [int(x) for x in LOWER.split(';')[1].split(',')], float(LOWER.split(';')[2])
    up, hold = int(LOWER.split(';')[3]), float(LOWER.split(';')[4])
    assert sum(sizes) == out * L1, (sum(sizes), out * L1)
    gl, gr, gl2, gr2 = G4
    jl, jr = HOME.split(';')[0].split(',')
    ring = (gl, gl2, jl, jr, gr2, gr)                       # as a ring is hung: the treble far left, the tenor far right
    t = END * 16 - out * L1
    for n in sizes:
        if n >= 6:                                          # still the riff: 7 = the tenor struck once, 6 = the treble short too
            row_notes(ROUNDS, t, 0, (n - 5, 1), bell=False, trs=ring)
        else:
            step = n / 6 if n > 1 else n / 12               # at a sixteenth the six are all but one stroke
            for i, b in enumerate(ROUNDS + (6,)):
                if n >= 4:                                  # a row to the beat: the last speed a hand can pick, still in unison
                    for tr in ring:
                        add(tr, t + i * step, step, F1 + PITCH[b], 1.0 if b == 1 else 0.9, **({} if b == 1 else {'pm': 1}))
                    add('bass', t + i * step, step, F1 + PITCH[b], 0.95 if b in (1, 6) else 0.85)
                else:                                       # one bell to a guitar, struck in its turn: at an eighth each rings half
                    # a row, so the sound crosses the room; at a sixteenth they are together and ring the whole stroke
                    add(ring[i], t + i * step, min(n * (hold if n > 1 else 1), END * 16 - t - i * step), F1 + PITCH[b] + up, vel)
            drum('k', t, 0.95)
            if n > 1:
                drum('k', t + 5 * step, 0.9)                # the foot goes with the tenor while the tenor is a stroke of its own
            if n < 4:
                add('bass', t, n, F1, 0.95)                 # the tenor under the dealt rows
            if n == 1:                                      # the snare strikes with the rows that are all but one stroke
                T['snare'] = [e for e in T['snare'] if e['at'] != round(t / 4, 4)]
                drum('s', t, round(0.86 + 0.04 * (t - (END * 16 - 4)), 3))
        t += n
    assert t == END * 16


def ring_up():
    """v34: the band's first rows as rounds raised in peal: the strokes of ring_down() in the other order (see RAISE)."""
    f = RAISE.split(';')
    rows, sizes, vel, up, hold = int(f[0]), [int(x) for x in f[1].split(',')], float(f[2]), int(f[3]), float(f[4])
    assert sum(sizes) == rows * L1 and sizes == sorted(sizes) and rows <= ROUNDS_N // 2, (sum(sizes), rows * L1)
    gl, gr, gl2, gr2 = G4
    jl, jr = HOME.split(';')[0].split(',')
    ring = (gl, gl2, jl, jr, gr2, gr)                       # as a ring is hung: the treble far left, the tenor far right
    t = BAND * 16
    for j, n in enumerate(sizes):
        if n >= 6:                                          # nearly the riff: 6 = the treble and the tenor short, 7 = the tenor short
            row_notes(ROUNDS, t, 0, (n - 5, 1))
        else:
            step = n / 6 if n > 1 else n / 12               # at a sixteenth the six are all but one stroke
            for i, b in enumerate(ROUNDS + (6,)):
                if n >= 4:                                  # a row to the beat: the first speed a hand can pick, in unison
                    for tr in G4:
                        add(tr, t + i * step, step, F1 + PITCH[b], 1.0 if b == 1 else 0.9, **({} if b == 1 else {'pm': 1}))
                    add('bass', t + i * step, step, F1 + PITCH[b], 0.95 if b in (1, 6) else 0.85)
                else:                                       # one bell to a guitar, struck in its turn
                    add(ring[i], t + i * step, n * (hold if n > 1 else 1), F1 + PITCH[b] + up, vel)
            drum('k', t, 0.95)
            if n > 1:
                drum('k', t + 5 * step, 0.9)                # the foot goes with the tenor once the tenor is a stroke of its own
            if n < 4:
                add('bass', t, n, F1, 0.95)                 # the tenor under the dealt rows
            if n == 1:                                      # the snare strikes with the rows that are all but one stroke
                T['snare'] = [e for e in T['snare'] if e['at'] != round(t / 4, 4)]
                drum('s', t, round(0.98 - 0.04 * j, 3))
        t += n
    assert t == BAND * 16 + rows * L1


def rounds_on_the_toms(b):
    """The last row before bar `b` is rounds on the tower. The kit rings it too, as it rings a call: the treble is
    left to the bell, then a tom to each bell between, high to low, and the snare for the tenor."""
    for i, (pc, v) in enumerate((("t1", 0.66), ("t2", 0.74), ("t3", 0.82), ("ft", 0.9), ("s", 0.95)), 1):
        drum(pc, b * 16 - 12 + 2 * i, v)


def chant(at, beats, line=None, first=None, step=3.0):
    """Two low voices a fifth apart over a bowed floor. Held (v2); or, with `line` (v10), singing a note to each
    row of the bells from `first`, `step` beats apart, the last note held to the end."""
    T.setdefault("drone", []).append({"at": at, "len": beats, "pitch": "F1", "vel": 0.5})
    if CHANT and line is not None:
        steps, gap = [int(x) for x in CHANT.split(";")[0].split("|")[line].split(",")], float(CHANT.split(";")[1])
        for i, d in enumerate(steps):
            t0 = first + i * step
            ln = (at + beats - t0) if i == len(steps) - 1 else step - gap
            if MONKS:                                                # v18: one line; the patch sings the fifth above it
                words = MONKS.split(";")[3].split("/")[line].split("|")
                assert len(words) == len(steps), (line, len(words), len(steps))
                T.setdefault("chant", []).append({"at": round(t0, 4), "len": round(ln, 4), "pitch": nm(41 + d), "vel": float(LOUDER.split(";")[2]) if LOUDER else 0.6, "ph": words[i],
                                                  **({"gain": f"{float(LOUDER.split(';')[3]):g}dB"} if LOUDER and line == 0 and float(LOUDER.split(";")[3]) else {})})
                continue
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
    for r in range(int(RAISE.split(';')[0]) if RAISE else 0, ROUNDS_N):
        row_notes(ROUNDS, BAND * 16 + r * L1, 0, W1)
    beat(BAND, PART1, "a", meet(L1))
    if RAISE:                            # v34: the band's first rounds are rung up, as its last are rung down
        ring_up()
    fill(PART1)
    # the first extent: Plain Bob Doubles. Forty rows on F, forty on Ab, forty on B
    bare = [int(x) for x in FORM.split(";")[2].split(":")] if FORM else [0, 0]
    for k, row in enumerate(EXTENT_1):
        s16, root = PART1 * 16 + k * L1, KEYS_1[k // 40]
        # First two leads on B only. The home rows and the hunting snare from
        # row 100 are left alone: the four strings fall back into unison there.
        split = HANDSTROKE and 80 <= k < 100 and k % 10 < 8
        slow = bool(SLOW) and int(SLOW.split(";")[0].split(":")[0]) <= k < int(SLOW.split(";")[0].split(":")[1])
        called = bool(CALLED) and k == int(CALLED.split(";")[2])
        row_notes(row, s16, root, W1, kicks="all" if k >= 80 else "hunt",
                  mode=lead_mode(k, CALLS_1) or ("bare" if bare[0] <= k < bare[1] else ""),
                  trs=G4[:2] if split or slow else None, pairs=coming_pairs(EXTENT_1, k), **({"gtrs": False} if called else {}))
        if called:                       # v30: the conductor calls the bob; the guitars rest for the row he calls in
            f = CALLED.split(";")
            assert lead_mode(k, CALLS_1) == "" and lead_mode(k + 1, CALLS_1) == "call0", "he calls in the row before the call"
            path = [float(c) for c in f[6].split(",")]
            T.setdefault("conductor", []).append({"at": round((s16 + float(f[5])) / 4, 4), "len": round(float(f[4]) / 4, 4), "pitch": f[3], "vel": 1.0, "ph": f[8],
                                                  "expr": {"f0": path[0]}, "expr_path": {"f0": path[1:]}})
        if split:
            handstroke(k, s16, root)
    if SLOW:                             # v23: the inner pair rings one lead at half speed over two
        slow_ring(*(int(x) for x in SLOW.split(";")[0].split(":")), int(SLOW.split(";")[1]), float(SLOW.split(";")[2]))
    for i, kind in enumerate("abc"):
        beat(PART1 + T1 * i, PART1 + T1 * (i + 1), kind, 10 ** 6 if FORM else meet(L1))
        fill(PART1 + T1 * (i + 1))
    if HUNT:                             # v9: the snare leaves the backbeat and follows the treble
        r0, r1 = (int(x) for x in HUNT.split(";")[0].split(":"))
        t0, t1 = PART1 * 16 + r0 * L1, PART1 * 16 + r1 * L1
        T["snare"] = [n for n in T["snare"] if not (t0 / 4 <= n["at"] < t1 / 4)]
        for k in range(r0, r1):
            drum("s", PART1 * 16 + k * L1 + EXTENT_1[k].index(1), float(HUNT.split(";")[1]))
    if FIRST:                            # v25: the lead's first four rungs, over the first cycle's last two leads, up to the call
        r0, r1 = (int(x) for x in FIRST.split(";")[0].split(":"))
        per, rungs, v0, v1 = int(FIRST.split(";")[1]) * L1, int(FIRST.split(";")[2]), float(FIRST.split(";")[3]), float(FIRST.split(";")[4])
        a16, z16 = PART1 * 16 + r0 * L1, PART1 * 16 + r1 * L1
        base, ladder = F1 + KEYS_1[r0 // 40] + 36, sorted(PITCH.values())       # three octaves over the ground, as the second climb is
        assert KEYS_1[r0 // 40] == KEYS_1[(r1 - 1) // 40] and a16 % 16 == 0 and per % 16 == 0 and per * (rungs - 1) < z16 - a16, "whole bars to a rung, in one key"
        assert lead_mode(r1, CALLS_1) == "call0" and r1 + 2 == 120, "it stops where the extent's last call starts"
        assert (base + ladder[rungs - 1]) % 12 == F1 % 12, "the last rung is the song's home"
        for t in range(a16, z16, int(TREM.split(";")[2])):
            v = v0 + (v1 - v0) * (t - a16) / (z16 - a16) + (0.05 if t % 4 == 0 else 0.0)
            add("lead", t, int(TREM.split(";")[2]), base + ladder[min(rungs - 1, (t - a16) // per)], min(1.0, v))
    # it has come round. One chord, and the bells alone again: rounds, slowly, over a drone and a pad
    hit(MIDDLE, 6)
    if TOWERHUNT:                        # v22: the tower rings the hunt, and comes round on the bar the bass sets off
        assert tower_hunt(MIDDLE * 4 + 2) == PART2 * 4
    else:
        slow_rounds(MIDDLE + 1, 9)
    if TOWER:
        gong(MIDDLE * 4, 0.9)
        chant(MIDDLE * 4 + 2, 29.5, line=1, first=MIDDLE * 4 + 2 if TOWERHUNT else (MIDDLE + 1) * 4)
    else:
        T.setdefault("home", []).append({"at": MIDDLE * 4, "len": 31.5, "pitch": "F1", "vel": 0.5})
        for p in ("F2", "C3"):
            T.setdefault("air", []).append({"at": (MIDDLE + 1) * 4, "len": 27.5, "pitch": p, "vel": 0.45})
    if TOWERHUNT:
        rounds_on_the_toms(PART2)
    else:
        fill(PART2)
    # the second extent: Grandsire Doubles, on F, Ab and C
    h0, h1 = (int(x) for x in HUNT2.split(";")[0].split(":")) if HUNT2 else (0, 0)
    hunting = in_the_hunt(EXTENT_2) if HUNT2 or TREBLE else []
    p0, p1 = (int(x) for x in PAIR.split(";")[0].split(":")) if PAIR else (0, 0)
    assert not PAIR or (h0 <= p0 and p1 <= h1 and p1 <= 20 and len(set(hunting[p0:p1])) == 1), "one marked pair, before the crossings"
    for k, row in enumerate(EXTENT_2):
        row_notes(row, PART2 * 16 + k * L2, KEYS_2[k // 40], W2, kicks="all" if k >= 80 else "hunt",
                  gtrs=not FUZZ or k >= int(FUZZ.split(";")[3]), teeth=bool(FUZZ),
                  mode=lead_mode(k, CALLS_2) or ("bare" if bare[0] <= k < bare[1] else ""),
                  trs=G4B if RIG2 and k >= int(RIG2.split(";")[5]) else G4,
                  pairs=coming_pairs(EXTENT_2, k, hunting[k] if hunting else 0),
                  **({"hunt": hunting[k]} if h0 <= k < h1 else {}), **({"ring2": hunting[k]} if TREBLE else {}),
                  **({"partner": hunting[k]} if p0 <= k < p1 and k % 10 < 8 else {}))
    if NEARLY:                           # v26: the tower hears home coming, a change before the bob
        nearly_home()
    if FUZZ and FORM and int(FUZZ.split(";")[3]) % 10 not in (8, 9, 0):     # v10: the guitars' entry is not at a home any more: its own crash
        drum("c", PART2 * 16 + int(FUZZ.split(";")[3]) * L2, 0.85)
    for i, kind in enumerate(FORM.split(";")[3] if FORM else "bac"):
        beat(PART2 + T2 * i, PART2 + T2 * (i + 1), kind, 10 ** 6 if FORM else meet(L2))
        fill(PART2 + T2 * (i + 1))
    for piece, t, v in HUNT_HITS:        # v13: the tom of the bell in the hunt (with the snare where the backbeat falls: three rows in eight)
        drum(piece, t, v)

    def harmony(extent, calls, r0, r1, part, length, w, keys):
        """The riff a third above (two steps up its own scale) and an octave up, on `hl`/`hr`, over rows r0..r1-1; the
        two rows of the call after them in unison an octave up."""
        steps, up, scale = int(HARM.split(";")[4]), int(HARM.split(";")[5]), sorted(PITCH.values())
        for k in range(r0, r1 + 2):
            t, root, call = part * 16 + k * length, keys[k // 40], lead_mode(k, calls).startswith("call")
            assert call == (k >= r1), "the harmony must end on a call"
            for b in tuple(extent[k]) + (6,):
                n = w[0] if b == 1 else w[1] if b == 6 else 1
                wide = SIXTHS and part == PART2 and k >= int(SIXTHS.split(";")[0])       # v17: the second lead in sixths
                i = scale.index(PITCH[b]) + (0 if call else int(SIXTHS.split(";")[1]) if wide else steps)
                pitch = F1 + root + up + scale[i % 6] + 12 * (i // 6)
                for j in range(n if b == 6 else 1):
                    for tr in ("hl", "hr"):
                        if b == 1 or call:
                            add(tr, t + j, n if b == 1 else 1, pitch, 1.0)
                        else:
                            add(tr, t + j, 1, pitch, (0.95 if j == 0 else 0.9) if b == 6 else 0.85, pm=1)
                t += n

    if HARM:                             # v7: the riff in harmony, on two more guitars
        r0, r1 = (int(x) for x in HARM.split(";")[3].split(":"))
        harmony(EXTENT_2, CALLS_2, r0, r1, PART2, L2, W2, KEYS_2)
    if HARM1:                            # v12: and, briefly, in the first cycle
        r0, r1 = (int(x) for x in HARM1.split(":"))
        harmony(EXTENT_1, CALLS_1, r0, r1, PART1, L1, W1, KEYS_1)
    if CLIMB:                            # v4: the lead climbs the row, slowly, over the last third; the snare on every beat at the end
        base, per, sv = int(CLIMB.split(";")[2]), float(CLIMB.split(";")[3]), float(CLIMB.split(";")[4])
        b0 = CLIMB_B0
        top = b0 + 6 * per
        if TREM:                         # v14: every note of the climb picked on the sixteenth, harder as it climbs
            n16, v0, v1 = int(TREM.split(";")[2]), float(TREM.split(";")[3]), float(TREM.split(";")[4])
            a16, z16 = int(round(b0 * 16)), LAND * 16 - 1
            for t in range(a16, z16, n16):
                i = min(6, int((t - a16) // (per * 16)))
                v = v0 + (v1 - v0) * (t - a16) / (z16 - a16) + (0.05 if t % 4 == 0 else 0.0)
                add("lead", t, n16, base + (sorted(PITCH.values()) + [12])[i], min(1.0, v))
        else:
            for i, iv in enumerate(sorted(PITCH.values())):
                T.setdefault("lead", []).append({"at": (b0 + i * per) * 4, "len": round(per * 4 - 0.06, 4), "pitch": nm(base + iv), "vel": 0.85})
            T.setdefault("lead", []).append({"at": top * 4, "len": round((LAND - top) * 4 - 0.25, 4), "pitch": nm(base + 12), "vel": 0.95})
        for b in range(LAND - 4, LAND):
            for q in (0, 8):
                drum("s", b * 16 + q, sv)
    # the landing: rounds on F, twenty-four times, and the bells ring rounds over the band at half its speed
    for r in range(LAND_N - (int(LOWER.split(';')[0]) if LOWER else 0)):
        row_notes(ROUNDS, LAND * 16 + r * L1, 0, W1, bell=False, **({"trs": G4 + tuple(HOME.split(";")[0].split(","))} if HOME else {}))
    if HOME and float(HOME.split(";")[1]):          # v16: the climb's last note, struck on the landing and let ring
        T.setdefault("lead", []).append({"at": LAND * 4, "len": float(HOME.split(";")[1]), "pitch": nm(int(CLIMB.split(";")[2]) + 12), "vel": float(HOME.split(";")[2])})
    beat(LAND, END, "c", meet(L1))
    if LOWER:
        ring_down()
    slow_rounds(LAND, int((END - LAND) * 4 / 3) if RHYTHM else 12, vel=0.9)
    if OVER:                             # v36: the men sing over the band, a note to each of those rows
        steps, words, v = [int(x) for x in OVER.split(";")[0].split(",")], OVER.split(";")[1].split("|"), [float(x) for x in OVER.split(";")[7].split(",")]
        assert len(steps) == len(words) == int((END - LAND) * 4 / 3), (len(steps), len(words))
        for i, (d, w) in enumerate(zip(steps, words)):
            t0 = LAND * 4 + 3 * i
            T.setdefault("men", []).append({"at": t0, "len": round((END * 4 - t0 if i == len(steps) - 1 else 3) - float(CHANT.split(";")[1]), 4),
                                            "pitch": nm(41 + int(OVER.split(";")[2]) + d), "vel": round(v[0] + (v[1] - v[0]) * i / (len(steps) - 1), 3), "ph": w})
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
    if ROWTIME:
        ringers_time(*(int(x) for x in ROWTIME.split(":")))
    if SLOWKIT:
        slow_kit()
    if MUFFLE and TREBLE:
        half_muffled()
    if CHORDS:
        two_chords()


def key_f(hz):
    """An eq frequency that follows the key: the lane `key` is the ground in semitones over F; the engine bends in octaves."""
    return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}


# v37 (chirper-one; section round, w6, 2:40-3:12, which the map still calls static after three rounds of fine work
# on the inner guitars; the change is 2:57.0-3:07.0, the bass only): THE BASS RINGS THE TENOR. The row is five bells
# that change places and a sixth that never does: "the tenor behind", the low F that covers every row, the thing
# the changes are heard against. In a tower the tenor is the BASS bell. Here the bass has always played all six: it
# doubles the riff note for note, so the song's ground is as busy as its changes. For ONE lead, the first rung with
# the new bell in the hunt (the second extent's rows 20-27, after the first bob), the bass is the tenor and nothing
# else: it rests while the five bells change places above it and strikes the tenor's three low F's at the end of
# every row, a little harder. So each row is said twice over: the changes light (the guitars, the kick under the
# treble, the tom on the bell in the hunt), the cover heavy (everyone). The lead's two home rows are in unison
# again, as written, and then the tower comes over the band (3:10.5). And the inner guitars, which play the
# crossings there (v20) and had only the last of the tenor's three strokes, strike all three with the outer pair:
# the cover is everyone. 40 notes of the bass and 40 of its fuzz are taken out; 16 are added on each inner guitar,
# every one at a time the outer guitars already strike; nothing is moved.
# the rows of the second extent ; the tracks ; `rest`: they rest on the five changing bells (`hold`: they hold the
# tenor's F under them from the row's first stroke) ; the velocities of the tenor's three strokes ; the loudness
# target ('' = unchanged) ; who joins the cover, `track<the track whose three tenor strokes it takes` (the inner
# guitars have only the last of the three in these rows; '' = nobody). '' = v36 byte for byte. Like RAISE, SLOWKIT
# and OVER, setting it does not switch SNARE off.
TENOR = os.environ.get('C10T3_TENOR', '20:28;bass,fuzz;rest;1.0,0.95,0.95;;gl2<gl,gr2<gr' if OVER else '')


def the_bass_rings_the_tenor(doc):
    """v37: over those rows the bass plays only the tenor's three strokes at the end of each row."""
    rows, names, how, vels, target, join = TENOR.split(';')
    r0, r1 = (int(x) for x in rows.split(':'))
    vels = [float(x) for x in vels.split(',')]
    for name in names.split(','):
        t = next(t for t in doc['tracks'] if t['name'] == name)
        for k in range(r0, r1):
            a, b = PART2 * 4 + 2.5 * k, PART2 * 4 + 2.5 * (k + 1)
            row = [n for n in t['notes'] if a - 1e-6 <= n['at'] < b - 1e-6]
            tenor = row[-3:]
            assert len(row) == 8 and all(n['pitch'] == nm(F1) for n in tenor) and not any(n['pitch'] == nm(F1) for n in row[:-3]), (name, k, row)
            for n in row[:-3]:
                t['notes'].remove(n)
            for n, v in zip(tenor, vels):
                n['vel'] = v
            if how == 'hold':
                t['notes'].append({'at': a, 'len': round(tenor[0]['at'] - a - 0.01, 4), 'pitch': nm(F1), 'vel': 0.85})
        t['notes'].sort(key=lambda n: n['at'])
    for pair in [x for x in join.split(',') if x]:
        to, src = (next(t for t in doc['tracks'] if t['name'] == x) for x in pair.split('<'))
        for k in range(r0, r1):
            a, b = PART2 * 4 + 2.5 * k, PART2 * 4 + 2.5 * (k + 1)
            tenor = [n for n in src['notes'] if a - 1e-6 <= n['at'] < b - 1e-6][-3:]
            assert all(n['pitch'] == nm(F1) for n in tenor), (pair, k, tenor)
            have = [n for n in to['notes'] if a - 1e-6 <= n['at'] < b - 1e-6]
            assert all(n['at'] + n['len'] <= tenor[0]['at'] + 1e-6 or n['at'] >= tenor[0]['at'] for n in have), (pair, k)    # nothing of its own rings into the cover
            to['notes'] += [dict(n) for n in tenor if not any(abs(m['at'] - n['at']) < 1e-6 for m in have)]
        to['notes'].sort(key=lambda n: n['at'])
    if target:
        doc['loudness'] = float(target)


def song():
    compose()
    # the ground, in semitones over F, from the bar each stretch begins
    grounds = [(0, 0), (PART1 + T1, KEYS_1[1]), (PART1 + 2 * T1, KEYS_1[2]), (MIDDLE, 0), (PART2 + T2, KEYS_2[1]), (PART2 + 2 * T2, KEYS_2[2]), (LAND, 0)]
    KEY_LANE = [["0b", 0]]
    for (b, k), (_, prev) in zip(grounds[1:], grounds):
        KEY_LANE += [[f"{b * 4 - 0.02:g}b", prev], [f"{b * 4:g}b", k]]
    HARM_DIP = []
    if HARM and CLIMB:        # the guitars' bus comes down a little while six guitars play (the lane is the climb's)
        h0, h1 = (PART2 * 4 + int(x) * L2 / 4 for x in HARM.split(";")[3].split(":"))
        HARM_DIP = [[f"{h0 - 0.5:g}b", 0], [f"{h0:g}b", float(HARM.split(";")[7])], [f"{h1 + 2 * L2 / 4 - 0.25:g}b", float(HARM.split(";")[7])], [f"{h1 + 2 * L2 / 4:g}b", 0]]
        if HARM1:        # v12: the same under the first cycle's harmony
            g0, g1 = (PART1 * 4 + int(x) * L1 / 4 for x in HARM1.split(":"))
            HARM_DIP = [[f"{g0 - 0.5:g}b", 0], [f"{g0:g}b", float(HARM.split(";")[7])], [f"{g1 + 2 * L1 / 4 - 0.25:g}b", float(HARM.split(";")[7])], [f"{g1 + 2 * L1 / 4:g}b", 0]] + HARM_DIP
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
        {"name": "snare", "patch": kit + (" kit.s.patch.synth.filters.1.gain={}dB kit.s.patch.synth.layers.0.wires={}".format(*SNARE.split(";")[:2]) if SNARE else ""),
         "gain": SNARE.split(";")[3] if SNARE else "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": SNARE.split(";")[2].split(",") if SNARE else ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        # the cymbals' fader: down where the china plays eighths (the last third of each extent, and the landing)
        {"name": "cym", "patch": kit, "gain": {"value": "-4.5dB", "mod": [{"src": "auto.busy", "amount": 1}]}, "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air,
         "auto": {"busy": {"points": [["0b", 0]] + [pt for b0, b1 in ((PART1 + 2 * T1, PART1 + 3 * T1), (PART2 + 2 * T2, END)) for pt in ([f"{b0 * 4 - 0.5}b", 0], [f"{b0 * 4}b", CYM_BUSY], [f"{b1 * 4 - 0.5}b", CYM_BUSY], [f"{b1 * 4}b", 0])], "curve": 0}}},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "lead", "patch": (TREM or CLIMB).split(";")[0], "gain": (TREM or CLIMB).split(";")[1], "pan": 0, "sends": {"hall": "-12dB"}}] if CLIMB else []),
        # the bells' fader: down in the landing, where twelve slow rows of six ring into one another over the full band
        {"name": "bell", "patch": "modal-bell", "gain": {"value": os.environ.get("C10T3_BELL", "-18dB"), "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0.1, "sends": {"hall": "-8dB"},
         "auto": {"lvl": {"points": [["0b", 0], *NEARLY_PTS, [f"{LAND * 4 - 1}b", 0], [f"{LAND * 4}b", BELL_LAND], [f"{END * 4 - 1}b", BELL_LAND], [f"{END * 4}b", 0]], "curve": 0}}},
        *([{"name": "treble", "patch": "modal-bell" + ((lambda d, t, dc, r: f" synth.layers.0.damp={d} synth.layers.0.tilt={t} synth.layers.0.decay={dc} synth.amp.r={r}")(*STRUCK.split(";")[:4]) if STRUCK else ""),
            "gain": os.environ.get("C10T3_BELL", "-18dB"), "pan": 0.1, "sends": {"hall": "-8dB"},
            "fx": [{"type": "eq", "bands": [{"kind": "hp", "cutoff": key_f(float(TREBLE.split(";")[0].split(":")[0])) if KEYEQ else float(TREBLE.split(";")[0].split(":")[0]),
                                             "q": float(TREBLE.split(";")[0].split(":")[1])}]}],
            **({"auto": {"key": {"points": KEY_LANE, "curve": 0}}} if KEYEQ else {})}] if TREBLE else []),
        *([{"name": "chant", "patch": ("ph-monks-forte" if LOUDER and LOUDER.split(";")[1] else "ph-monks") if MONKS else TOWER.split(";")[0], "gain": (f"{float(MONKS.split(';')[1][:-2]) + float(LOUDER.split(';')[0]):g}dB" if LOUDER else MONKS.split(";")[1]) if MONKS else CHANT.split(";")[2] if CHANT else TOWER.split(";")[1],
            "pan": -0.1, "sends": {"hall": MONKS.split(";")[2] if MONKS else TOWER.split(";")[2]}},
           {"name": "gong", "patch": TOWER.split(";")[3], "gain": TOWER.split(";")[4], "pan": 0.2, "sends": {"hall": "-8dB"}},
           {"name": "drone", "patch": TOWER.split(";")[6], "gain": TOWER.split(";")[7], "pan": 0.2, "sends": {"hall": "-12dB"}}] if TOWER else
          [{"name": "home", "patch": "contrabass-tight", "gain": "-9dB", "pan": 0.3, "sends": {"hall": "-12dB"}},
           {"name": "air", "patch": "juno-pad", "gain": "-13dB", "pan": 0.15, "sends": {"hall": "-8dB"}}]),
    ]
    if SLOW and len(SLOW.split(";")) > 3 and float(SLOW.split(";")[3]):      # v23: the inner pair's fader while it carries a line of its own
        s0, s1 = (PART1 * 4 + int(x) * L1 / 4 for x in SLOW.split(";")[0].split(":"))
        for t in tracks:
            if t["name"] in G4[2:]:
                t["gain"] = {"value": GD, "mod": [{"src": "auto.slow", "amount": 1}]}
                t["auto"] = {"slow": {"points": [["0b", 0], [f"{s0 - 0.02:g}b", 0], [f"{s0:g}b", float(SLOW.split(";")[3])],
                                                 [f"{s1 - 0.02:g}b", float(SLOW.split(";")[3])], [f"{s1:g}b", 0]], "curve": 0}}
    if CHORD_ROWS and float(CHORDS.split(";")[3]):                          # v31: and while it holds the two chords
        up, pts = float(CHORDS.split(";")[3]), []
        for k in CHORD_ROWS:
            a, z = PART2 * 4 + k * L2 / 4, PART2 * 4 + (k + 1) * L2 / 4
            if pts and pts[-1][0] == a:
                pts[-2:] = [[z - 0.02, up], [z, 0]]
            else:
                pts += [[a - 0.02, 0], [a, up], [z - 0.02, up], [z, 0]]
        pts = [[f"{b:g}b", v] for b, v in pts]
        for t in tracks:
            if t["name"] in G4[2:]:
                if isinstance(t["gain"], dict):
                    assert float(t["auto"]["slow"]["points"][-1][0][:-1]) < PART2 * 4 and t["auto"]["slow"]["points"][-1][1] == 0
                    t["auto"]["slow"]["points"] += pts
                else:
                    t["gain"] = {"value": GD, "mod": [{"src": "auto.slow", "amount": 1}]}
                    t["auto"] = {"slow": {"points": [["0b", 0]] + pts, "curve": 0}}
    if MUFFLE and TREBLE:
        treble = next(t for t in tracks if t['name']=='treble')
        tracks.append({**treble,'name':'wrapped','sends':{'hall':'-18dB'},
                       'fx':[*treble['fx'],f'gain gain={MUFFLE}dB'],
                       'patch':'modal-bell synth.layers.0.bright.value=0.18 synth.layers.0.bright.mod.0.amount=0.12 synth.layers.0.damp=0.46 synth.layers.0.decay=420ms synth.amp.r=140ms synth.amp.d=600ms'})
    if CALLED:
        s16 = PART1 * 16 + int(CALLED.split(";")[2]) * L1                    # whoever else rests while he calls (the kit's beat is written after the rows)
        who, _, n16 = CALLED.split(";")[10].partition(":")
        for tr in [x for x in who.split(",") if x]:
            T[tr] = [n for n in T.get(tr, []) if not (s16 / 4 <= n["at"] < (s16 + int(n16 or L1)) / 4)]
        tracks.append({"name": "conductor", "patch": CALLED.split(";")[0], "gain": CALLED.split(";")[1], "pan": 0, "sends": {"hall": CALLED.split(";")[7]},
                       **({"fx": [{"type": "eq", "bands": CALLED.split(";")[9].split(",")}]} if CALLED.split(";")[9] else {})})
    if SLOWKIT and T.get("ride"):                                           # v35: the ride's bell, on a track of its own
        tracks.append({"name": "ride", "patch": kit, "gain": SLOWKIT.split(";")[5], "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air})
    if SLOWKIT and T.get("slowtoms"):
        tracks.append({"name": "slowtoms", "patch": kit, "gain": SLOWKIT.split(";")[6], "out": "drums", "sends": {"oh": "-1.5dB"},
                       **({"fx": [{"type": "eq", "bands": SLOWKIT.split(";")[7].split("|")}]} if SLOWKIT.split(";")[7] else {})})
    if OVER:                                                                # v36: the men over the band, on a track of their own
        tracks.append({"name": "men", "patch": "ph-monks-over", "gain": OVER.split(";")[4], "pan": -0.1, "sends": {"hall": OVER.split(";")[5]},
                       **({"fx": [{"type": "eq", "bands": OVER.split(";")[6].split("|")}]} if OVER.split(";")[6] else {})})
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    return {
        "about": ("chirpers X (Common Time), track 3 by chirper-zero: \"Plain Hunt\". One row of six sixteenths (Eb C B Ab Gb and a low F "
                  "that always comes last) rung in every order by the bell-ringers' rule that a note may only swap places with its "
                  "neighbour: two extents, 240 rows, none repeated within either, each coming back to the scale it began on. The "
                  "highest note walks through the row and back all piece long, with the kick and a church bell on it. "
                  + ("Since v5 the highest note is long and the low F repeated, so the row is a riff: eight sixteenths in the first "
                     "extent, ten in the second." if RHYTHM else "v1 is the skeleton.")),
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(OVER.split(";")[8]) if OVER and OVER.split(";")[8] else float(SLOWKIT.split(";")[9]) if SLOWKIT and SLOWKIT.split(";")[9] else float(RAISE.split(";")[5]) if RAISE and RAISE.split(";")[5] else float(SNARE.split(";")[4]) if SNARE and SNARE.split(";")[4] else float(STRUCK.split(";")[4]) if STRUCK else float(CHORDS.split(";")[4]) if CHORDS and CHORDS.split(";")[4] else float(LOUDER.split(";")[4]) if LOUDER else -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    **({"ph-monks": {"about": "chirper-zero: Plain Hunt's chant - the library's voice-choir (five singers on a line) with basses' tracts, and a second five a fifth above sized to their part: ten men singing words",
                                     "extends": MONKS.split(";")[0]}} if MONKS else {}),
                    **({"ph-monks-forte": {"about": "chirper-three: Plain Hunt's ten men (ph-monks) singing out, on Harry's 'chant louder'",
                                           "extends": MONKS.split(";")[0] + " " + LOUDER.split(";")[1]}} if LOUDER and LOUDER.split(";")[1] else {}),
                    **({"ph-monks-over": {"about": "chirper-alpha: Plain Hunt's ten men (ph-monks) singing over the whole band at the landing, an octave up and hard",
                                          "extends": MONKS.split(";")[0] + " " + OVER.split(";")[3]}} if OVER else {})},
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
            "low": ({"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                     {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                            {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                            {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}],
                     "auto": {"key": {"points": KEY_LANE, "curve": 0}}} if KEYEQ else
                    {"fx": [{"type": "eq", "bands": ["peak cutoff=44 q=1.5 gain=-7dB", "peak cutoff=90 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                            {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                            {"type": "eq", "bands": ["peak cutoff=170 q=1.2 gain=-3dB"]}]}),
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
    doc = song()
    if TENOR:
        the_bass_rings_the_tenor(doc)
    open(OUT, "w").write(dump(doc))
