#!/usr/bin/env python3
"""chirpers10-t7 "Extreme and Mean" (chirper-zero): one pattern of longs and shorts, the same at every size.

Euclid cuts a line "in extreme and mean ratio" when the whole is to the longer part as the longer is to the shorter.
A line cut so has no common measure: no unit, however small, goes a whole number of times into both parts. This piece
is that cut made in time, and it is the record's slow song (80 where the other six run 100 to 138).

There are two cells: a LONG of three sixteenths and a SHORT of two. And one rule, applied to every cell at once:

    a long becomes a long and a short;  a short becomes a long.

Start from one long and apply the rule over and over: L, LS, LSL, LSLLS, LSLLSLSL ... Each line is the line before
it followed by the line before that. The pattern never falls into a loop, yet every stretch of it comes back; and it
is the same at every size: group the cells as the rule made them and the groups are again longs and shorts in the
same order, 5 and 3 sixteenths, then 8 and 5, 13 and 8, 21 and 13 ... up to 233 and 144.

So the band plays ONE pattern at many sizes at once:

  cells of 3 and 2          the guitars' muted strokes (a long is two strokes and a rest, a short one stroke and a
                            rest), with the bass and the kick locked to them
  cells of 8 and 5          the string is let ring: an open low note
  cells of 13 and 8         a chord (on the long ones the root; on the short ones, from the third section, a tritone up)
  cells of 34 and 21        a crash
  cells of 55 and 34        the root: home on the long ones, a semitone up on the short ones
  cells of 233 and 144      THE SECTIONS OF THE SONG: the long ones heavy, the short ones quiet. Long, short, long,
                            long, short, long, short, long: the form is the riff, 78 times slower.

The whole song is the fourteenth line of the rule: 1597 sixteenths, and then one chord where the fifteenth would
begin. The kit keeps common time against all of it (the china in quarters, the snare on three) and starts its count
again at each section. A long section is fourteen bars and nine sixteenths; a short one is exactly nine bars.

In the quiet sections the rule is said another way, by the engine itself: a wire harp (Karplus-Strong, the first on
this record) is given no notes, only the rule as an L-system (the first on this record), written so that each short
cell is born one step up the scale from the long cell that made it. Its tune is therefore each phrase followed by
the phrase before it, one step higher. In the last section the harp plays over the band: the two sayings together.

v1 is the SKELETON (Harry, 17 Nov about 03:40: "open up 2 new song slots"; track 2's terms: mine, my title, a
skeleton first): the whole shape standing, bare.
"""
import bisect
import json
import os

OUT = os.environ.get("C10T7_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t7.yaml"))
BPM = 80
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
GEN = 14                                  # the song is the rule's fourteenth line
TOP = 9                                   # the cells that are the song's sections
# the harp: gain ; hall send ; gain in the last section, over the band ("" = it does not play there)
HARP = os.environ.get("C10T7_HARP", "-14dB;-10dB;-12.5dB")
PAD = os.environ.get("C10T7_PAD", "7.5dB;-9dB")        # the clean guitar's chords in the quiet sections: gain ; hall send
# the bass in the quiet sections, dB after its bus (its compressor holds a long soft note at the level of a hard short
# one, so a lower velocity does not make it quieter; this does)
QBASS = os.environ.get("C10T7_QBASS", "-4.5")
# v2, THE SAME TUNE AT EVERY SIZE: the three quiet sections were the same nine bars three times. Now the second has two
# harps and the third three, and each added harp plays THE SAME TUNE ON LARGER CELLS (5 and 3 sixteenths; then 8 and 5),
# an octave lower each: a canon in which the voices' speeds stand as the long cell to the short. Every note of a slower
# harp falls with a note of the faster ones. The second voice's gain ; the third's. "" = v1.
CANON = os.environ.get("C10T7_CANON", "-16dB;-18dB")
# v3, THE TUNE AT THE LARGEST SIZE A BREATH CAN HOLD: cells of 21 and 13 sixteenths (3.9 and 2.4 seconds) had no voice of
# their own. In the four-guitar sections a brass section (horns and trombones on the engine's physical lips: the record's
# first `wind` source) plays the harp's tune on those cells, one long note to a cell: strings plucked for the small
# sizes, breath for the large one. patch ; gain ; velocity ; semitones over the harp's pool (an octave up: at the harp's
# own octave its notes sat at 250-500 Hz and read 7 dB over the records there) ; a dip at its lowest notes (Hz : q : dB).
# "" = v2.
BRASS = os.environ.get("C10T7_BRASS", "brass;-13dB;0.8;12;400:1:-3")
# v4: the last 89 sixteenths of the second two-guitar riff. A steel above the fretted guitars
# bends its way through 55, then 34: the short line is literally the head of the long one.
# Dry and close, not a third wall of rhythm guitar. Empty regenerates v3.
STEEL = os.environ.get("C10T7_STEEL", "-12dB")
# v5: the last riff sheds its smallest strokes before the whole band signs the final chord.
PEEL = os.environ.get("C10T7_PEEL", "1")
# v6: a shared pitch, a rubbed rim on a long cell and a felt stroke on a short.
# Middle quiet section only. Track trims in dB (rim; mallet); empty gives v5.
BOWL = os.environ.get("C10T7_BOWL", "-16;-13")
# v7: in the return to F, the wall pair plays the riff three sizes larger.
# Empty restores v6; the v6 BOWL-empty switch still restores v5.
BIG_STROKES = os.environ.get("C10T7_BIG_STROKES", "1" if BOWL else "")
# v8: the horn borrows five notes from the lowest harp before the last
# quiet section. Empty restores v7; older rollback switches keep working.
REVEAL = os.environ.get("C10T7_REVEAL", "1") if BIG_STROKES and CANON and BRASS else ""
# v9: after 55 sixteenths the first riff's short children go to a pitched log drum.
# Track gain; empty restores v8. Keep the older rollback switches intact.
CHILD = os.environ.get("C10T7_CHILD", "-5dB") if REVEAL else ""
# v10: the heavy middle anticipates the bowl's chords; the last one opens into F minor.
PIVOT = os.environ.get("C10T7_PIVOT", "1") if CHILD else ""  # empty restores v9
# v11: after the wall pair has played the riff three sizes larger, the foot plays it
# one size smaller (cells of 2 and 1); bass and inside guitars follow. Empty = v10.
SMALLER = os.environ.get("C10T7_SMALLER", "1") if PIVOT else ""
# v12: THE GROUND RISES UNDER THE HARP (section round, 4:42.8-4:49.1, in the window 4:24-4:48 the map calls static:
# nothing entered or left between the harp's entry at 4:16 and the peel). With 89 sixteenths to go the last section
# is three cells: 34, 21, 34. The last was already a semitone up (the rule for cells of 34) and the 21 is where the
# riff starts to fall away. In the first 34 the harp over the band plays only A flat, C and E flat, and the horn's
# two breaths there are A flat and C: an A flat major chord that the band, chugging F under it, never let be one.
# Now for that one cell the four guitars and the bass move up a minor third, to the middle sections' A flat, and
# the same notes are heard as what they spell. The harp's last note in the cell is F: it falls home a sixteenth
# before the band does, on the crash where the outer guitars begin to peel. So the last 89 are a lift (A flat),
# home thinning (F), the semitone (G flat), and the chord. Nothing but the root moves: every stroke, the kit, the
# harp and the horn are as they were.
# semitones the ground rises for that cell. "" = v11.
LIFT = os.environ.get("C10T7_LIFT", "3") if SMALLER and PEEL else ""
# v13: FOUR KETTLEDRUMS (palette round; the middle quiet section, 2:38-3:05). One size of cell had no tune anywhere:
# 13 and 8 sixteenths. Under the band those cells are the chord; in the quiet sections they were only the foot, thirteen
# soft strokes on a kick. In the middle quiet section those thirteen strokes now go to four kettledrums (the engine's
# `kettle` mode set, the first on this record: the kettle's air pulls the head's modes to 1 : 1.5 : 2 : 2.44, so a drum
# sings a note), and the drums have the harp's tune at that size, an octave under the lower harp: A flat, then C flat
# and E flat, and on the last cell of all the one G flat. That last note is rolled, and while it is rolled the pedal
# lets the head down a semitone, so the roll arrives on F with the band: G flat falling to F is the riff's own short
# cell falling home. The clean E and B go UP to F and C there (v10); the drum comes down to meet them.
# The first quiet section keeps its foot and the third its foot: one harp, then drums with pitch, then three harps.
# track gain ; hall send ; the roll's strokes, first:last, in dB under a plain stroke ("" = one stroke on G flat, no roll,
# no pedal). "" = v12.
KETTLE = os.environ.get("C10T7_KETTLE", "-12dB;-12dB;-22:-8") if LIFT else ""
# v14: the opening says the rule's two letters on two sides. For the first
# cell of 55 sixteenths (0:00 to 0:10.3, before the log drum takes the short
# cells) the chords and ringing strings are still both guitars; of the
# clipped strokes, the ones in long cells are the left guitar's alone and the
# ones in short cells the right's: thirteen to eight. "1" as said; "2" swaps
# the sides at the crash on 34. Empty restores v13.
SIDES = os.environ.get("C10T7_SIDES", "1") if KETTLE else ""
# v15 (palette): THE BOW HOLDS THE ROOT. Every size of cell but one has a voice of its own: strokes (3 and 2), the
# ringing string (8 and 5), kettledrums (13 and 8), a breath of brass (21 and 13), a crash (34 and 21). Cells of 55 and
# 34 are the root (home on the long ones, a semitone up on the short ones), and nothing ever HELD a root: it was only
# struck again and again. 55 sixteenths is 10.3 seconds, more than a breath and just what one slow bow can hold. So in
# the return to F (3:05-3:49) a section of double basses (the library's `contrabass`, a bowed string on the engine's
# physical bow: the record's first) draws one bow to a cell: F, G flat, F, F, G flat. Plucked for the small sizes,
# breath for the large one (v3), the bow for the one above. It is also the first thing in a heavy section that sounds
# through the riff's rests. No vibrato (a section on a pedal; and it would beat against the guitars' own F).
# Benched at -8 dB on the low F (F1) and an octave up: 7.5 and 6.2 dB under the band, the rests 3 dB shallower, and
# on F1 2 dB more under 60 Hz, where the return already matched the records. The return read 1.1 dB under them at
# 60-120 Hz and 2.9 over at 250-500. So: the octave up (its fundamental is 87 Hz), 4.5 dB lower, and a dip on its
# third and fourth harmonics. patch ; track gain ; semitones over the low F ; the dip (Hz : q : dB).
# "" = v14; it is on only while every older switch is, so each of those still gives what it gave.
ARCO = os.environ.get("C10T7_ARCO", "contrabass synth.pitch.mod.0.amount=0 fx.0.mix=0.1;-12.5dB;12;300:0.9:-5") if all((
    SIDES, KETTLE, LIFT, SMALLER, PIVOT, CHILD, REVEAL, BIG_STROKES, BOWL, PEEL, STEEL, BRASS, CANON, QBASS, PAD, HARP)) else ""
# v16 (palette): THE IRON SAYS FIVE AND THREE, on a bar cut the same way. In the heavy sections one size had no voice:
# cells of 5 and 3 sixteenths (the second harp has them in the quiet sections; under the band they were only an accent).
# For the first 89 sixteenths of the tutti in A flat (1:54.4-2:11.1, before the walls take the bowl's chords) a hammer
# on iron strikes the head of every such cell: thirteen long, eight short. With it every size from the stroke to the
# root sounds at once, each on its own voice: strokes, iron, the ringing string, the chord, a breath of brass, a crash,
# the root. The kit goes on counting four against it, and the two meet only where a cell's head falls on a beat.
# THE BAR (`em-iron`, a new song-local patch): its overtones are cut in extreme and mean ratio. Each partial is to the
# next as the long cell is to the short (1 : 1.618 : 2.618 : 4.236 : 6.854 ...), so each partial's frequency is the SUM
# of the two below it: the rule the riff is made by, in the sound. Two bars: a long cell is struck on the bar tuned to
# the ground, a short cell on a bar a golden cut shorter (833 cents up, between a minor and a major sixth), and every
# partial of the short bar is a partial of the long one: the short bar is the long bar without its lowest note, as a
# short cell is a long cell without its first stroke. The fourth partial lies two octaves and a semitone over the
# first, so a stroke on A flat already holds the A the ground rises to at 2:04.7.
# track gain ; pan ; semitones over the guitars' low string ; the long bar's first partial (its level against the
# second; 1 is a plain bar: kept lower because the tutti is already over the records at 250-500 Hz).
# Benched at -9 dB: 5.8 dB under the band and 8 dB OVER it at 600-1200 Hz on each stroke, a soloist. At -15: 11.8 under,
# a stroke on the long bar 2.4 dB over the band at 600-1200 Hz for its first 60 ms, on the short bar 1.7 under.
# "" = v15; it is on only while ARCO is.
IRON = os.environ.get("C10T7_IRON", "-15dB;-0.3;36;0.5") if ARCO else ""
PHI = (1 + 5 ** 0.5) / 2
# v17 (section w5, 1:36-2:00): ONE STROKE AND A REST, AT THE SIZE OF THE ROOT. Everywhere else in the song a quiet
# section stands between two heavy ones. Between the third section and the fourth (the form is L S L L S L S L) there
# is nothing: the riff in F and G flat runs straight into the tutti in A flat, behind eight sixteenths of tom fill
# that the guitars play through. The rule already says what belongs there. A short cell is ONE STROKE AND A REST; the
# third section's last cell of 34 is a short one (the root's size: 55 and 34), and 34 is 21 and 13. So the band plays
# its 21 and RESTS its 13: from 1:51.9 the two guitars, the bass and the foot stop, the largest rest in the song, 2.4
# seconds, where the smallest is one sixteenth. The kit does not stop: it is not in the pattern, it keeps common time,
# and its china goes on counting quarters through the hole. In the hole the steel's last bend, A flat falling to F,
# is heard alone: the note the band is about to move to, let go. Then the drummer, who has kept four against the
# pattern for 114 seconds, says it: the toms play exactly the five strokes the guitars leave out (two, the ringing
# one, two; the old fill was eight even sixteenths ending on the snare), one sixteenth of china, and the tutti lands.
# The other four heavy sections keep their fill. The toms' five strokes: velocities. "" = v16; on only while IRON is.
REST = os.environ.get("C10T7_REST", "0.8,0.68,0.93,0.86,1") if IRON else ""
# A hole of 2.4 seconds makes the file measure 0.028 dB quieter, so every other bar came out that much louder. This
# target gives those bars the gain they had in v16.
REST_LUFS = -10.028


# v18 (whole song): THE BASS DOES NOT REST. The song's card asks whether a slow song at 80 is heavy or only slow.
# In the riff a long cell is two strokes and a rest and a short cell one stroke and a rest, and every part that
# played the strokes kept the rests: guitars, kick and bass together. So wherever the strokes are muted (three cells
# in five) a third to a half of the cell was silence in every part, the low end included: at this tempo a rest is
# 0.19 s. The rests are the rule and stay where they are, in the guitars and the foot. But the bass no
# longer keeps them: the stroke before a rest is held through it, to the next stroke. The low string sounds from the
# head of a cell to the head of the next, and what is cut into strokes and rests is cut over a floor that does not
# go away. It starts when the kit arrives: the first nine bars (to 0:27) are the bare rule, every part resting, as
# before; from the bar where the snare and the china come in, in every heavy section, the bass holds. The rest of
# v17 at 1:51.9 (thirteen sixteenths) is still a rest for everyone: only a rest of one sixteenth is held through.
# Sixteenths into the song where the bass starts to hold ; the loudness target (every quiet bar keeps v17's
# mastering gain). "" = v17; it is on only while REST is.
HOLD = os.environ.get("C10T7_HOLD", "144;-10.028") if REST else ""
# v19: HARRY'S THREE ANSWERS (19 Nov 02:26, on the review page; they came in a minute before v18 was recorded and I
# had not seen them). On "heavy, or only slow?": "yeah but really make it chug if slow. play with breakdowns". On the
# last chord: "Chug right through" (not "Let the riff fall away"). On the steel: "Keep the steel".
# A chug is the stroke AND its rest, in every part at once: v18's bass, holding through the rests, was less of one,
# not more. So the bass keeps the rests again, with the guitars and the foot, as in v17 (v18's hold stays behind
# this switch). And the last riff no longer falls away (v5's peel, from 55 sixteenths to go: the outer guitars left
# at 34, the inner pair at 21, the bass and the foot at 13): all four guitars, the bass and the kit now play every
# stroke up to the last chord. The steel stays as it is.
# the bass: 'rests' or 'held' ; the last riff: 'through' or 'peel' ; the loudness target (ten seconds more of the
# whole band made the file measure louder: at -10.028 every other bar came out 0.08 dB under v17, at -9.951 0.02 to 0.05 over).
# "" = v18; 'rests;peel;-10.028' = v17. It is on only while HOLD is, so each older switch still gives what it gave.
CHUG = os.environ.get("C10T7_CHUG", "rests;through;-9.951") if HOLD else ""
# v19, the other half (chirper-two, palette round: the chug's own rig): THE STROKE STOPS. "Really make it chug": a
# chug is the stroke and its rest, and measured on the parts alone the rest was not one. After a muted stroke the
# guitar's level through the following sixteenth was 9 dB under the stroke (its string is let go over 90 ms into an
# amp that holds whatever it is given at full level), and the bass's 8 dB under (its own release, then two
# compressors' recovery). Neither the palm mute's damping nor the rig's gate moves that (benched: nothing at all);
# the string's release does. So this song's guitars let go in a fiftieth of a second, twins and walls: no stroke
# of theirs is written differently, every one is where it was and as long; what changes is how each one ENDS, the
# chords and ringing notes too (they stop on the rest, where they rang 90 ms into it). The bass plays in the quiet
# sections as well, long soft notes that should end as they did, so its rig is left alone: instead, in the heavy
# sections only, each bass note that has a rest after it is written that much shorter, and its own release ends
# where the rest begins.
# the twins' release ; the walls' ; sixteenths off a bass note before a rest ; the loudness target. "" = the song
# with CHUG alone.
# (The target is v18's own, so the file measures what the album's files measure. The rests are emptier, so at that
# loudness everything stands 0.3 dB higher than with CHUG alone: the heavy sections read what they read in v18,
# within 0.2 dB, with the strokes higher and the rests lower inside them. At -10.206 the quiet sections kept their
# gain exactly (-0.001 dB, residual -80 dB: no note or sound of theirs changes) and the file read -10.3.)
# (The walls' plate was benched too: without it the tutti's rests are 1.5 dB emptier, no more, because what sounds
# through them there is the brass, the iron and the kit's room. It stays.)
TIGHT = os.environ.get("C10T7_TIGHT", "20ms;20ms;0.45;-10.028") if CHUG else ""
# v20 (chirper-alpha, whole song): THE BREAKDOWNS (Harry, 19 Nov 02:26: "yeah but really make it chug if slow. play
# with breakdowns"). v19 made the chug; this is the other half. The kit already plays half time at 80, so a
# breakdown here cannot be 'half time'. It is the song's own rule instead, and nothing is written for it:
#     THE BAND RESTS WHERE THE RIFF TWO SIZES UP RESTS.
# The riff is a long cell of 3 (stroke, stroke, rest) and a short of 2 (stroke, rest). Two sizes up the same riff
# is a long cell of 8 (three sixteenths struck, two struck, THREE AT REST) and a short of 5 (three struck, TWO AT
# REST). In a breakdown the guitars, the bass and the foot go on playing their small strokes exactly where they
# were, but only where that larger riff strikes; where it rests, they rest. So the chug comes in the shape of the
# chug: a chord and a stroke, three quarters of a second of nothing; a ringing string and a stroke, under half a
# second of nothing. No stroke is moved or added: A BREAKDOWN IS NOT PLAYED, IT IS LEFT OUT. And since v19 the
# stroke stops, so what is left out is silence under the kit, which keeps common time as it does everywhere.
# The rule goes on upward, and the song plays with that: four sizes up the rests are 8 and 5 sixteenths (1.5 and
# 0.9 seconds), six sizes up 21 (3.9 seconds).
#   1:27.4-1:37.7  the two-guitar section, its third cell of 55, before the steel: the rests of two sizes up.
#   4:32.4-4:42.8  the last section, its third cell of 55, under the harp: the RESTS GROW. Its first 21 sixteenths
#                  rest two sizes up; the next 13 four sizes up as well (one chord, one stroke, 1.7 seconds of
#                  nothing); the last 21 six sizes up: the band is gone, and what is left is the harp, alone as
#                  in the quiet sections, saying the same rule. Then the ground rises (v12) and the riff chugs
#                  right through to the last chord (his other answer), every stroke of it.
# The horn leaves both cells whole: in a breakdown everything that is not the chug goes.
# section : sixteenths into it : how many sizes of rest are open in each of the cell's three parts (21, 13, 21);
# ... ; the loudness target. "" = v19.
# (The target: with twenty seconds of the song part silence the file measures quieter, and at v19's target every
# other bar came out 0.07 to 0.22 dB higher. At -10.153 every bar outside the two cells keeps v19's gain within
# 0.008 dB, residual -68 dB or lower, on both seeds; the file reads -10.2 LUFS.)
BREAK = os.environ.get("C10T7_BREAK", "2:89:1,1,1;7:89:1,2,3;-10.153") if TIGHT else ""


# v21 (chirper-one, whole song): THE KIT BREAKS DOWN TOO. In v20's two breakdowns the band rests where the riff two
# sizes up rests, and the hands went on keeping common time over the holes: china in quarters, snare on three. A
# band that stops under a kit that does not sounds like guitars dropping out (v20's own doubt, and chirper-two's
# design before it: "the kit is the cure"). So in a breakdown THE HANDS GO OVER TO THE RIFF, the one place in the
# song they leave common time: where the band plays, the china strikes the head of each long cell and the snare the
# head of each short one; where the band rests, the hands rest. Two sizes up the riff is a long of 8 (three struck,
# two struck, three at rest) and a short of 5 (three struck, two at rest), so what the hands play is that riff
# itself: china, snare, rest for a long; china, rest for a short. The kit says stroke, stroke, rest at the size the
# band is resting at. A crash already at the head of a cell stands for the china there. And in the second
# breakdown, once the band has played its last stroke (4:37.1), the kit is gone too: the harp is alone for 4.1
# seconds, as v20's own description had it. Then the kit comes back first, with the fill it ends every heavy
# section with (two strokes on each tom, two on the snare, over the last eight sixteenths), and the riff comes in
# on the crash: a breakdown that ends in silence is called back by the drums.
# the hands' piece on a long cell's head ; on a short's ; their velocities ; 'fill' if the kit calls the band back
# out of a breakdown that ends at rest ; the loudness target (at v20's -10.153 every other bar came out 0.06 dB
# lower: the fill and the hands' harder strokes measure louder than the count they replace). "" = v20.
HANDS = os.environ.get("C10T7_HANDS", "x;s;0.8;0.95;fill;-10.118") if BREAK and os.environ.get("C10T7_MASTER", "x") else ""


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


def word(n):
    """Line n of the rule: W1 = L, W2 = LS, Wn = W(n-1) W(n-2)."""
    a, b = "L", "LS"
    for _ in range(n - 2):
        a, b = b, b + a
    return a if n == 1 else b


SIZE = [(3, 2)]                           # SIZE[k] = (a long's sixteenths, a short's) at size k
for _k in range(GEN):
    SIZE.append((SIZE[-1][0] + SIZE[-1][1], SIZE[-1][0]))


def cells(k):
    """The song at size k: (start sixteenth, 'L' or 'S', length)."""
    out, t = [], 0
    for c in word(GEN - k):
        n = SIZE[k][c == "S"]
        out.append((t, c, n))
        t += n
    return out


LEV = [cells(k) for k in range(GEN)]
STARTS = [[c[0] for c in lv] for lv in LEV]
TOTAL = LEV[0][-1][0] + LEV[0][-1][2]
assert TOTAL == 1597 and all(lv[-1][0] + lv[-1][2] == TOTAL for lv in LEV) and SIZE[TOP] == (233, 144)
assert all(set(STARTS[k + 1]) <= set(STARTS[k]) for k in range(GEN - 1))     # every size's cells begin where smaller cells do
RANK = {}
for _k, _s in enumerate(STARTS):
    for _p in _s:
        RANK[_p] = _k                     # the largest size of cell that begins here


def at_size(k, p):
    """The size-k cell that sixteenth p lies in."""
    return LEV[k][bisect.bisect_right(STARTS[k], p) - 1]


LIFT_SPAN = (TOTAL - SIZE[7][0], TOTAL - SIZE[6][0])        # v12: from 89 to go until 55 to go
assert at_size(5, LIFT_SPAN[0]) == (LIFT_SPAN[0], "L", LIFT_SPAN[1] - LIFT_SPAN[0])      # one long cell of 34, crash to crash


SECS = LEV[TOP]                           # eight: L S L L S L S L
KEY = [0, 0, 0, 3, 3, 0, 0, 0]            # home, a minor third up for the middle pair, home (the rule's own grouping: 3 + 2 + 3)
WIDE = {3, 5, 7}                          # four guitars


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym", "rde": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 1.0 if piece == "rde" else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


ROOTS = []                                # (sixteenth, the bass's root in semitones over F1): the low bus's eq follows it


def heavy(i, s0, n):
    twins, walls = ("gl", "gr"), ("wl", "wr")
    # The first 55 sixteenths of this return stay in unison, as do the
    # 89 after the exchange. Both seams fall at the head of a size-3 cell.
    spread_at, together_at = s0 + SIZE[6][0], s0 + SIZE[8][0]
    for p, kind, ln in LEV[0]:
        if not s0 <= p < s0 + n:
            continue
        big = BIG_STROKES and i == 5 and spread_at <= p < together_at
        gtrs = twins + walls if i in WIDE and not big else twins
        r = RANK[p]
        root = KEY[i] + (1 if at_size(6, p)[1] == "S" else 0)
        if LIFT and LIFT_SPAN[0] <= p < LIFT_SPAN[1]:
            root += int(LIFT)
        if not ROOTS or ROOTS[-1][1] != root:
            ROOTS.append((p, root))
        if r >= 3:                        # a chord: the root on a long cell of 13, a tritone up on a short one of 8
            up = 6 if at_size(3, p)[1] == "S" and i >= 2 else 0
            for tr in gtrs:
                add(tr, p, ln, ",".join(nm(F1 + root + up + j) for j in (0, 7, 12)), 1.0)
            if big:
                # Magnify each one-sixteenth stroke by three substitutions:
                # L = hit(5), hit(3), rest(5); S = hit(5), rest(3).
                # The second attack turns the fifth upside down; it is not
                # a new chord. Let go before each next stroke.
                first, second = SIZE[1]
                base = F1 + root + up
                for tr in walls:
                    add(tr, p, first - 0.5, f"{nm(base)},{nm(base + 7)}", 0.97)
                    if at_size(3, p)[1] == "L":
                        add(tr, p + first, second - 0.5, f"{nm(base + 7)},{nm(base + 12)}", 0.92)
            add("bass", p, ln, F1 + root + up, 0.95)
            drum("k", p, 0.95)
            if r >= 5:
                drum("c", p, 0.9 if r >= 8 else 0.75)
        elif r == 2:                      # the string let ring
            for tr in gtrs:
                add(tr, p, 2, F1 + root, 1.0)
            add("bass", p, 2, F1 + root, 0.95)
            drum("k", p, 0.95)
            if ln == 3:
                for tr in gtrs:
                    add(tr, p + 2, 1, F1 + root, 0.85, pm=1)
                add("bass", p + 2, 1, F1 + root, 0.85)
                drum("k", p + 2, 0.85)
        else:                             # muted: a long is two strokes and a rest, a short one stroke and a rest
            for j in range(2 if ln == 3 else 1):
                v = (0.95 if r == 1 else 0.88) if j == 0 else 0.8
                for tr in gtrs:
                    add(tr, p + j, 1, F1 + root, v, pm=1)
                add("bass", p + j, 1, F1 + root, v)
                drum("k", p + j, v)
    # the kit keeps common time and starts its count again with the section
    kit_from = SIZE[8][0] if i == 0 else 0            # the first nine bars: no snare or china yet, a hat in quarters
    for q in range(0, n, 4):
        if q < kit_from:
            drum("h", s0 + q, 0.45)
        else:
            drum("x", s0 + q, 0.55 if q % 16 == 0 else 0.5)
    for q in range(8, n - 9, 16):
        if q >= kit_from:
            drum("s", s0 + q, 0.95)
    for j, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):      # the nine-sixteenth bar ends in a fill
        drum(pc, s0 + n - 8 + j, 0.6 + 0.045 * j)


def quiet(i, s0, n):
    key = KEY[i]
    for p, kind, ln in LEV[5]:            # cells of 34 and 21: the chord. F minor on the long ones, D flat on the short ones
        if not s0 <= p < s0 + n:
            continue
        ch, low = ((41, 48, 56), 0) if kind == "L" else ((37, 44, 53), 8)
        exposed = REVEAL and i == 6 and p == s0 + SIZE[6][0]
        if BOWL and i == 4:
            # Ab minor to E major: one bowl on Cb/B belongs to both. The clean
            # guitar leaves it out of its long chords and rests on the short
            # ones. Damp the rim before the mallet falls so the strokes speak.
            shared = 56 + key
            assert any((x + key - shared) % 12 == 0 for x in ch)
            if kind == "L":
                add("pad", p, ln - 1, ",".join(nm(x + key) for x in ch if (x + key - shared) % 12), 0.8)
                add("rim", p, ln - 2, shared, 0.82)
            else:
                add("mallet", p, ln - 1, shared, 0.85)
        elif not exposed:
            add("pad", p, ln - 1, ",".join(nm(x + key) for x in ch), 0.8)
        # In the exposed phrase the bass gives one low F, then leaves the
        # repeated Cs to the slow harp. The ride and foot keep their parts.
        add("bass", p, SIZE[2][0] - 1 if exposed else ln - 2, F1 + key + low, 0.3)
        ROOTS.append((p, key + low))
    for p, kind, ln in LEV[3]:
        if s0 <= p < s0 + n:
            drum("k", p, 0.3)
    for q in range(0, n, 4):
        drum("rde", s0 + q, 0.4)


def steel_answer():
    # Song arithmetic, not a separate clock: 233 = 144 + (55 + 34). Wait for the first
    # 144. The chords already mark the heads; the bar comes in *after* them. On the
    # second telling the extra high answer is missing, leaving the drum fill exposed.
    start = SECS[2][0] + SIZE[8][0]
    for length in SIZE[6]:
        for offset, duration, pitch, bend, velocity in (
            (3, 9, 65, 3, .82),          # F up to Ab
            (15, 5, 75, -3, .70),        # Eb down to C
            (21, 5, 68, -3, .80),        # Ab down to F; eight sixteenths of space
            (34 + 3, 12, 72, 3, .90),    # C up to Eb, only in the long telling
        ):
            if offset + duration <= length:
                add("bar", start + offset, duration, pitch, velocity)
                T["bar"][-1]["expr_path"] = {"bend": [0, 0, bend * .2, bend * .82, bend, bend, bend]}
        start += length
    assert start == SECS[3][0]


def peel_last_riff():
    # Count down *toward* the endpoint in the riff's own sizes. For 21 sixteenths
    # the outer pair rings the big cells above the inside chug; the inside pair
    # then inherits one held chord. First the feet, then the harp, horn and fill
    # have the figure to themselves. The final low F is composed as before.
    a, b, c, d = (TOTAL - SIZE[k][0] for k in (6, 5, 4, 3))  # 55, 34, 21, 13 to go
    for tr in ('wl', 'wr', 'gl', 'gr', 'bass', 'kick', 'cym'):
        kept = []
        for note in T[tr]:
            p = round(4 * note['at'])
            if a <= p < TOTAL:
                if tr in ('wl', 'wr', 'gl', 'gr'):
                    outside = tr in ('wl', 'wr')
                    if (outside and p >= b) or (not outside and p >= c):
                        continue
                    if outside or p >= b:
                        if p not in STARTS[3]:
                            continue
                        note = {**note, 'len': round((at_size(3, p)[2] - 1) / 4, 4)}
                elif p >= (c if tr == 'cym' else d):
                    continue
            kept.append(note)
        T[tr] = kept


def compose():
    if STEEL:
        steel_answer()
    for i, (s0, kind, n) in enumerate(SECS):
        (heavy if kind == "L" else quiet)(i, s0, n)
        if BRASS and i in WIDE:
            big = [c for c in LEV[4] if s0 <= c[0] < s0 + n]
            for (p, _, ln), step in zip(big, harp_tune(5)):
                if REVEAL and i == 5 and p >= s0 + n - SIZE[5][0]:
                    continue  # these last two breaths become the next harp's phrase below
                add("brass", p, ln - 1, POOL[step] + KEY[i] + int(BRASS.split(";")[3]), float(BRASS.split(";")[2]))
            if REVEAL and i == 5:
                q = SECS[i + 1][0]
                centre, width = q + SIZE[6][0], SIZE[5][0]
                low_cells = [cell for cell in LEV[2] if q <= cell[0] < q + SECS[i + 1][2]]
                steps = harp_tune(8 - 2)
                assert len(steps) == len(low_cells)
                for (p, _, ln), step in zip(low_cells, steps):
                    if centre <= p < centre + width:
                        here = q - width + p - centre
                        assert here in STARTS[2] and at_size(2, here)[2] == ln
                        add("brass", here, ln - 1, POOL[step] + KEY[i + 1] + 12, float(BRASS.split(";")[2]))
    if LIFT:
        # what the lift is for: there the harp and the horn already spell the major triad on the new ground,
        # and the harp's last note is the home the band falls back to
        s0 = SECS[7][0]
        here = [POOL[st] for (p, _, _), st in zip([c for c in LEV[0] if c[0] >= s0], harp_tune(9)) if LIFT_SPAN[0] <= p < LIFT_SPAN[1]]
        horn = [POOL[st] for (p, _, _), st in zip([c for c in LEV[4] if c[0] >= s0], harp_tune(5)) if LIFT_SPAN[0] <= p < LIFT_SPAN[1]]
        assert {(x - POOL[0] - int(LIFT)) % 12 for x in here[:-1] + horn} == {0, 4, 7} and (here[-1] - POOL[0]) % 12 == 0
    if PEEL and not (CHUG and CHUG.split(";")[1] == "through"):
        peel_last_riff()
    for tr in ("gl", "gr", "wl", "wr"):                   # where the fifteenth line would begin: one chord
        add(tr, TOTAL, 32, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", TOTAL, 32, F1, 0.95)
    drum("k", TOTAL, 0.95)
    drum("c", TOTAL, 0.95)
    ROOTS.append((TOTAL, 0))


RULES = {"A": "A", "p": "p", "q": "q[+Br]", "B": "A", "r": "pq"}      # Apq is a long, Br a short; the short is born a step up


def harp_gen(depth, n, pool):
    return {"type": "lsystem", "axiom": "Apq", "rules": RULES, "depth": depth, "n": n, "len": "/16", "notes": " ".join(nm(x) for x in pool)}


def harp_gen_at(k, n, pool):
    """The same L-system on the cells of size k (SIZE[k] sixteenths): a long is A and its rests, a short B and its rests."""
    ln, sn = SIZE[k]
    abc = "abcdefghijklmnopqrstuvwxyz"
    lr, sr = abc[:ln - 1], abc[ln - 1:ln - 1 + sn - 1]
    rules = {"A": "A", "B": "A"}
    for c in lr[:-1]:
        rules[c] = c
    rules[lr[-1]] = lr[-1] + "[+B" + sr + "]"                     # the short cell is born a step up, as at size 0
    for j, c in enumerate(sr):
        rules[c] = lr[j] if j < len(sr) - 1 else lr[len(sr) - 1:]     # a short's rests grow into a long's
    return {"type": "lsystem", "axiom": "A" + lr, "rules": rules, "depth": 8 - k, "n": n, "len": "/16", "notes": " ".join(nm(x) for x in pool)}


def harp_tune(depth):
    """What the engine's turtle will play (for the notes and the docs): the pool step of each cell."""
    s = "Apq"
    for _ in range(depth):
        s = "".join(RULES.get(c, c) for c in s)
    pos, stack, out = 0, [], []
    for c in s:
        if c == "+":
            pos += 1
        elif c == "[":
            stack.append(pos)
        elif c == "]":
            pos = stack.pop()
        elif c.isupper():
            out.append(pos)
    return out


POOL = [53, 56, 60, 63, 65, 68, 72, 75]   # F3 Ab3 C4 Eb4 F4 Ab4 C5 Eb5 (F minor seventh, broken): step 0 sounds once, step 1 at cells 1 2 3 5 8 13 21 34


def short_children():
    """The harp's tune, on only the cells born short. No new strike times."""
    s0 = SECS[0][0]
    long_span, short_span = SIZE[6]
    end = SIZE[8][0]
    band = [cell for cell in LEV[0] if s0 <= cell[0] < s0 + end]
    steps = harp_tune(8)
    assert len(steps) == len(band) and long_span + short_span + long_span == end
    low_hits, high_hits = set(), set()
    for (p, kind, ln), step in zip(band, steps):
        if p < s0 + long_span or kind != "S":
            continue
        # First tell it on Gb in the bass register. When the ground falls to
        # F, let the same contour speak an octave higher and finish its phrase.
        low = p < s0 + long_span + short_span
        root = KEY[0] + int(at_size(6, p)[1] == "S")
        add("log", p, ln - 1, POOL[step] + root - (24 if low else 12), .88)
        if low:
            T["log"][-1]["gain"] = "-2dB"       # match the five low strikes to the bass they take
            low_hits.add(p)
        else:
            high_hits.add(p)
    take = low_hits | high_hits
    T["bass"] = [n for n in T["bass"] if round(n["at"] * 4) not in take]
    # Low, the drum takes the foot's stroke too. High, the foot returns
    # under it while the right guitar leaves it the attack instead.
    T["kick"] = [n for n in T["kick"] if round(n["at"] * 4) not in low_hits]
    T["gr"] = [n for n in T["gr"] if round(n["at"] * 4) not in high_hits]


def one_size_smaller():
    """Run the rule backwards once: a long of three is a long of two and a short
    of one; a short of two is one long. So 'stroke stroke rest' becomes 'stroke
    rest stroke'. No cell head moves, and the wall pair keeps the riff's own size.
    """
    s0, _, n = SECS[5]
    start = s0 + SIZE[8][0]               # all four guitars are back on the small riff
    follow = start + SIZE[4][0]           # 21 later the players nearest the foot go with it
    stop = start + SIZE[6][0]             # 55: the horn's five notes get the old lock
    assert stop == s0 + n - SIZE[5][0] and follow in STARTS[4]

    def at(tr, p):
        found = [e for e in T[tr] if round(e["at"] * 4) == p]
        assert len(found) == 1, (tr, p, found)
        return found[0]

    for p, kind, _ in LEV[0]:
        if not start <= p < stop or kind != "L" or RANK[p] == 2:
            continue                      # a short is one stroke at either size; a ringing cell is 2 + 1 already
        for tr in ("kick",) + (("bass", "gl", "gr") if p >= follow else ()):
            head = at(tr, p)
            if RANK[p] < 3:               # the second muted stroke crosses into the rest
                at(tr, p + 1)["at"] = round((p + 2) / 4, 4)
            elif tr == "kick":           # under a chord the walls hold: two sixteenths, then one
                drum("k", p + 2, 0.85)
            else:
                head["len"] = round(2 / 4 * 0.98, 4)
                add(tr, p + 2, 1, head["pitch"].split(",")[0], 0.85, **({} if tr == "bass" else {"pm": 1}))


def kettles():
    """The foot's thirteen soft strokes in the middle quiet section, on four tuned drums, with the tune at their size."""
    s0, _, n = SECS[4]
    cells3 = [c for c in LEV[3] if s0 <= c[0] < s0 + n]
    steps = harp_tune(8 - 3)
    assert len(cells3) == len(steps) == 13
    heads = {p for p, _, _ in cells3}
    foot = [k for k in T["kick"] if round(k["at"] * 4) in heads]
    assert len(foot) == 13 and all(k["vel"] == 0.3 for k in foot)
    T["kick"] = [k for k in T["kick"] if round(k["at"] * 4) not in heads]
    drums = sorted({POOL[st] + KEY[4] - 12 for st in steps})
    assert [nm(x) for x in drums] == ["Ab2", "B2", "Eb3", "Gb3"]         # 32, 29, 26 and 23 inches: each inside its drum's range
    loud = KETTLE.split(";")[2]
    for j, ((p, _, ln), st) in enumerate(zip(cells3, steps)):
        pitch = POOL[st] + KEY[4] - 12
        if j < 12 or not loud:
            # the head of a chord (cells of 34 and 21) is struck a little harder than the strokes inside it
            add("kettle", p, ln - 0.5, pitch, 0.62 if p in STARTS[5] else 0.5)
            continue
        # The last cell: the tune's top note, rolled, swelling; over its last three sixteenths the pedal comes up
        # and the head falls a semitone to F.
        # A roll is not a rhythm: a timpanist times the sticks to the head, so that each stroke pushes the skin the
        # way it is already going. Here that is done by counting the head's own cycles: every stroke falls 14 cycles
        # after the last, three of them 12 (65 to 80 ms, about 13 strokes a second, on no grid). An even number,
        # because the kettle's second mode is a fifth up, three cycles to the principal's two: after 13 cycles of the
        # one the other is half a turn out.
        # (First bench: strokes every 75 ms, which at 185 Hz is 13.875 cycles; each arrived an eighth of a turn out of
        # step with the last, the fifth cancelled the first, and the roll had a hole 14 dB deep a third of a second in.
        # Second: 13s and 14s; the principal held and the fifth above it was gone by the middle of the roll.)
        end, strokes = p + ln, 20
        assert st == max(steps) and steps.count(st) == 1 and end == SECS[5][0] and (pitch - 1 - F1) % 12 == 0
        first, last = (float(x) for x in loud.split(":"))
        sec, fine = 15 / BPM, 2000                                   # seconds to a sixteenth ; steps to a sixteenth

        def pedal_from(start):
            def pedal(t):
                u = min(1.0, max(0.0, (t - start) / 2.6))
                return round(-u * u * (3 - 2 * u), 4) + 0.0          # (+ 0.0: no minus zero in the file)
            return pedal

        def turns(pedal):
            """The head's cycles since the first stroke, at each fine step of the cell."""
            out, total = [0.0], 0.0
            for i in range(ln * fine):
                total += 440 * 2 ** ((pitch + pedal(p + (i + 0.5) / fine) - 69) / 12) * sec / fine
                out.append(total)
            return out

        # The pedal starts where the whole roll is a whole number of cycles: the stroke with the band is in step too.
        lo, hi = end - 3.6, end - 2.6
        whole = int(turns(pedal_from(end - 3))[-1]) // 2 * 2
        short = (14 * strokes - whole) // 2                          # how many of the gaps are 12 cycles, not 14
        assert 0 <= short <= strokes // 4
        gaps = [12 if (k + 1) * short // strokes > k * short // strokes else 14 for k in range(strokes)]
        assert sum(gaps) == whole
        assert turns(pedal_from(lo))[-1] < whole < turns(pedal_from(hi))[-1]
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if turns(pedal_from(mid))[-1] < whole else (lo, mid)
        pedal = pedal_from(round(lo, 4))
        phase = turns(pedal)
        assert abs(phase[-1] - whole) < 0.01 and pedal(end - 0.2) == -1.0
        for k in range(strokes):
            want = sum(gaps[:k])
            t = p + next(i for i, c in enumerate(phase) if c >= want - 1e-6) / fine
            ln16 = end - 0.05 - t
            pts = max(1, round(ln16 / 0.2))
            u = k / strokes
            T.setdefault("kettle", []).append({
                "at": round(t / 4, 5), "len": round(ln16 / 4, 5), "pitch": nm(pitch), "vel": 0.5 if k == 0 else round(0.25 + 0.35 * u, 3),
                "expr": {"pedal": pedal(t)},
                # the engine reaches point i of a path at (i + 1) / N of the note
                "expr_path": {"pedal": [pedal(t + (i + 1) * ln16 / pts) for i in range(pts)]}})
            if k:
                # The first stroke is the tune's note; the roll under it starts as a murmur. Strokes in step add
                # up, so each is far smaller than a stroke heard alone: a trim, from the first to the last. (At -6
                # the last half second stood 7 to 9 dB over everything else there, which is the guitar's swelling
                # A flat of v10: the roll is to lead that in, not cover it.)
                T["kettle"][-1]["gain"] = f"{first + (last - first) * u ** 1.6:.1f}dB"
        add("kettle", end, 6, pitch - 1, 0.85)                           # and lands with the band


def two_common_tones():
    """Ab minor and E major share two notes. First move a finger, then move the ground."""
    s, quiet_in, back = (SECS[i][0] for i in (3, 4, 5))
    first, again = s + SIZE[7][0], s + SIZE[8][0]
    cells = [c for c in LEV[5] if first <= c[0] < quiet_in]
    assert "".join(kind for _, kind, _ in cells) == "LSLSL"  # question, then question with a return
    home = F1 + KEY[3]
    first_up, last_up = [p for p, kind, _ in cells if kind == "S"]

    def tick(n):
        return round(n["at"] * 4)

    def rest(tracks, start, end):
        for tr in tracks:
            T[tr] = [n for n in T[tr] if not start <= tick(n) < end]

    def ground(p):
        return home - 4 if p >= again and at_size(5, p)[1] == "S" else home

    # The left amp plays the quiet guitarist's Ab2/Eb3 and raises just the fifth.
    # The right picks B3 during each long and lets it ring across the short.
    rest(("wl", "wr"), first, quiet_in)
    for p, kind, ln in cells:
        short = kind == "S"
        add("wl", p, ln - .4, ",".join(nm(home + i) for i in (12, 19 + int(short))), .92)
        if not short:
            middle = p + SIZE[4][0]
            add("wr", p, middle - p - .25, home + 27, .92)
            following = SIZE[4][0] if p + ln < quiet_in else 0
            add("wr", middle, p + ln + following - middle - .25, home + 27, .90)

    # On the first E the bass holds Ab. Keep its octaves but not an Eb in the
    # inside guitar chord. The second E drops into root position with the chugs.
    for tr in ("bass", "gl", "gr"):
        for n in T[tr]:
            p = tick(n)
            if not first <= p < quiet_in:
                continue
            root = ground(p)
            intervals = (0,)
            if "," in n["pitch"]:
                intervals = (0, 12) if first_up <= p < again else (0, 7, 12)
            n["pitch"] = ",".join(nm(root + i) for i in intervals)
    ROOTS[:] = sorted([(p, r) for p, r in ROOTS if not first <= p < quiet_in]
                      + [(p, ground(p) - F1) for p, _, _ in cells])
    rest(("gl", "gr"), first_up + SIZE[3][0], again)  # eight sixteenths of space for the question
    T["brass"] = [n for n in T["brass"] if tick(n) != first_up and not quiet_in - SIZE[3][0] <= tick(n) < quiet_in]
    next(n for n in T["brass"] if tick(n) == last_up)["pitch"] = nm(home + 44)  # E5 on the answer

    # The mallet strikes B3 on the short cells. The clean guitarist answers the
    # first with E3; the second becomes a broken E chord on the way home to F.
    p, _, ln = next(c for c in LEV[5] if c[0] >= quiet_in and c[1] == "S")
    delay = SIZE[0][0]
    add("pad", p + delay, ln - delay - 1, home + 20, .78)
    final, kind, ln = at_size(5, back - 1)
    assert kind == "S" and final + ln == back
    wait, carry = SIZE[1][0], SIZE[3][0]
    add("pad", final + wait, ln - wait - .5, home + 20, .78)
    rest(("wl", "wr"), back, back + carry)
    # E/B moves to F/C. Ab3 is the common note this time, carried on one string
    # through the change. Only the left of the outside pair picks on the one.
    arrival = back - SIZE[2][0]
    assert arrival == final + carry
    add("wr", arrival, back + carry - 1 - arrival, home + 24, .88)
    add("wl", back, carry - .5, ",".join(nm(F1 + i) for i in (24, 31)), .96)


def the_bow_holds_the_root():
    """One bow to each cell of 55 or 34 in the return to F; the last lifts with the band."""
    i = 5
    s0, _, n = SECS[i]
    held = [c for c in LEV[6] if s0 <= c[0] < s0 + n]
    assert sum(c[2] for c in held) == n and [c[1] for c in held] == list("LSLLS")
    for j, (p, kind, ln) in enumerate(held):
        add("arco", p, ln - (1 if j == len(held) - 1 else 0.25), F1 + int(ARCO.split(";")[2]) + KEY[i] + (kind == "S"), 0.8)


def the_iron_says_five_and_three():
    """One stroke to each cell of 5 or 3 in the first 89 sixteenths of the tutti in A flat. No stroke of the band moves."""
    i = 3
    s0, end = SECS[i][0], SECS[i][0] + SIZE[7][0]
    said = [c for c in LEV[1] if s0 <= c[0] < end]
    assert sum(c[2] for c in said) == SIZE[7][0] and [c[1] for c in said].count("L") == 13 and len(said) == 21
    for p, kind, ln in said:
        ground = KEY[i] + (at_size(6, p)[1] == "S")
        add("iron", p, ln - 0.5, F1 + ground + int(IRON.split(";")[2]), 0.92 if kind == "L" else 0.84, cut=kind == "S")


def one_stroke_and_a_rest():
    """The third section's last cell of 34 as a short cell says it: 21 played, 13 rested. The toms say the rested strokes."""
    s0, _, n = SECS[2]
    end = s0 + n
    hole, fill = end - SIZE[4][1], end - 8
    assert at_size(6, hole) == (end - SIZE[6][1], "S", SIZE[6][1]) and at_size(4, hole) == (hole, "S", SIZE[4][1])
    tick = lambda note: round(note["at"] * 4)
    left_out = [tick(note) for note in T["gl"] if fill <= tick(note) < end]
    for tr in ("gl", "gr", "bass", "kick"):
        assert [tick(note) for note in T[tr] if fill <= tick(note) < end] == left_out
        T[tr] = [note for note in T[tr] if not hole <= tick(note) < end]
    for tr in ("toms", "snare"):                 # the old fill: six toms and two snares in even sixteenths
        T[tr] = [note for note in T[tr] if not fill <= tick(note) < end]
    vels = [float(v) for v in REST.split(",")]
    assert len(left_out) == len(vels) == 5 and left_out[0] == fill
    for p, piece, vel in zip(left_out, ("t1", "t1", "t2", "ft", "ft"), vels):
        drum(piece, p, vel)


def the_bass_does_not_rest():
    """In the heavy sections the bass holds the stroke before each one-sixteenth rest through it."""
    start = int(HOLD.split(";")[0])
    notes = sorted(T["bass"], key=lambda n: n["at"])
    held = 0
    for i, (s0, kind, n) in enumerate(SECS):
        if kind != "L":
            continue
        inside = [x for x in notes if max(s0, start) <= round(x["at"] * 4) < s0 + n]
        for a, b in zip(inside, inside[1:]):
            gap = round(b["at"] * 4) - round(a["at"] * 4)
            if gap == 2 and abs(a["len"] - round(1 / 4 * 0.98, 4)) < 1e-6:     # one stroke, one rest
                a["len"] = round(2 / 4 * 0.98, 4)
                held += 1
    assert held > 200, held


def the_stroke_stops():
    """In the heavy sections a bass note with a rest after it ends early enough for its release to be over by the rest."""
    off = float(TIGHT.split(";")[2])
    tick = lambda note: round(note["at"] * 4)
    done = 0
    for s0, kind, n in SECS:
        if kind != "L":
            continue
        inside = sorted((x for x in T["bass"] if s0 <= tick(x) < s0 + n), key=lambda x: x["at"])
        for a, b in zip(inside, inside[1:] + [{"at": (s0 + n) / 4}]):
            long16 = round(a["len"] * 4 / 0.98)                  # as written, in sixteenths
            if tick(b) - tick(a) > long16 and long16 >= 1:       # a rest follows
                a["len"] = round((long16 - off) / 4 * 0.98, 4)
                done += 1
    assert done > 200, done


def the_rests_grow():
    """A breakdown: the band rests where the riff two (four, six) sizes up rests. No stroke moves, none is added."""
    tick = lambda note: round(note["at"] * 4)
    rests, whole = [], []
    for spec in BREAK.split(";")[:-1]:
        i, off, depths = spec.split(":")
        s0 = SECS[int(i)][0] + int(off)
        assert at_size(6, s0) == (s0, "L", SIZE[6][0])          # a long cell of 55: its parts are 21, 13 and 21
        parts = [c for c in LEV[4] if s0 <= c[0] < s0 + SIZE[6][0]]
        depths = [int(d) for d in depths.split(",")]
        assert len(parts) == len(depths) == 3
        whole.append((s0, s0 + SIZE[6][0]))
        for (p, _, n), depth in zip(parts, depths):
            for k in range(2, 2 * depth + 1, 2):
                for q, kind, m in LEV[k]:                       # a cell of size k rests for its last cell of size k - 2
                    a, z = q + m - SIZE[k - 2][kind == "S"], q + m
                    if p <= a and z <= p + n:
                        rests.append((a, z))
    inside = lambda t, spans: any(a <= t < z for a, z in spans)
    gone = {}
    for tr in ("gl", "gr", "wl", "wr", "bass", "kick"):
        keep = [n for n in T[tr] if not inside(tick(n), rests)]
        gone[tr] = len(T[tr]) - len(keep)
        T[tr] = keep
    # a crash at the head of a cell is that cell's stroke; the china in quarters and the snare are the kit's time and stay
    T["cym"] = [n for n in T["cym"] if not (n["pitch"] == "c" and inside(tick(n), rests))]
    T["brass"] = [n for n in T["brass"] if not inside(tick(n), whole)]
    assert gone["gl"] == gone["gr"] == gone["bass"] == gone["kick"] > 0, gone
    if HANDS:
        on_long, on_short, v_long, v_short = HANDS.split(";")[:4]
        crashes = {tick(n) for n in T["cym"] if n["pitch"] == "c"}
        # the hands leave common time for the cell ...
        T["cym"] = [n for n in T["cym"] if n["pitch"] == "c" or not inside(tick(n), whole)]
        T["snare"] = [n for n in T["snare"] if not inside(tick(n), whole)]
        # ... and strike with the band: the head of each small cell that still sounds
        for q, kind, m in LEV[0]:
            if inside(q, whole) and not inside(q, rests):
                if kind == "S":
                    drum(on_short, q, float(v_short))
                elif q not in crashes:
                    drum(on_long, q, float(v_long))
        if HANDS.split(";")[4]:
            for a, z in whole:
                if all(inside(t, rests) for t in range(z - 8, z)):
                    for j, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):      # as heavy() ends a section
                        drum(pc, z - 8 + j, 0.6 + 0.045 * j)
    return rests


def letters_on_two_sides():
    """Long cells left, short cells right, for the song's first cell of 55. Nothing is added."""
    s0, end = SECS[0][0], SECS[0][0] + SIZE[6][0]
    turn = s0 + SIZE[5][0] if SIDES == "2" else end
    def stays(track, n):
        p = round(n["at"] * 4)
        if not s0 <= p < end or not n.get("expr"):
            return True                                # chords, ringing strings and everything after
        side = ("gl", "gr")[(at_size(0, p)[1] == "S") != (p >= turn)]
        return track == side
    for tr in ("gl", "gr"):
        T[tr] = [n for n in T[tr] if stays(tr, n)]


def song():
    compose()
    if PIVOT:
        two_common_tones()
    if CHILD:
        short_children()
    if SMALLER:
        one_size_smaller()
    if KETTLE:
        kettles()
    if SIDES:
        letters_on_two_sides()
    if ARCO:
        the_bow_holds_the_root()
    if IRON:
        the_iron_says_five_and_three()
    if REST:
        one_stroke_and_a_rest()
    if HOLD and not (CHUG and CHUG.split(";")[0] == "rests"):
        the_bass_does_not_rest()
    if BREAK:
        the_rests_grow()                 # before the stroke stops: the bass's last note before each new rest is let go in time too
    if TIGHT:
        the_stroke_stops()
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}" + (" synth.amp.r=" + TIGHT.split(";")[0] if TIGHT else "")
    let_go = lambda patch, field: patch + (" synth.amp.r=" + TIGHT.split(";")[field] if TIGHT else "")
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    hg, hh, h8 = HARP.split(";")
    harps = [(i, s0, 8, 144, [x + KEY[i] + (12 if i == 6 else 0) for x in POOL], hg) for i, (s0, kind, n) in enumerate(SECS) if kind == "S"]
    if h8:
        harps.append((7, SECS[7][0], 9, 233, [x + 12 for x in POOL], h8))
    tracks = [
        {"name": "gl", "patch": main.format(50), "gain": "-0.7dB", "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(51), "gain": "-0.7dB", "pan": 1, "out": "gtrs", **mids},
        {"name": "wl", "patch": let_go("ct-wall-stop-l", 1), "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": let_go("ct-wall-stop-r", 1), "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        *[{"name": f"harp{i + 1}", "patch": "em-harp", "gain": g, "pan": 0.25, "at": f"{s0 / 4:g}b", "sends": {"hall": hh},
           "gen": [harp_gen(d, n, pool)]} for i, s0, d, n, pool, g in harps],
        *([{"name": f"harp{i + 1}{'bc'[k - 1]}", "patch": "em-harp", "gain": CANON.split(";")[k - 1], "pan": (-0.3, 0.0)[k - 1],
            "at": f"{SECS[i][0] / 4:g}b", "sends": {"hall": hh},
            "gen": [harp_gen_at(k, 144, [x + KEY[i] + (12 if i == 6 else 0) - 12 * k for x in POOL])]}
           for i, k in ((4, 1), (6, 1), (6, 2))] if CANON else []),
        *([{"name": "brass", "patch": BRASS.split(";")[0], "gain": BRASS.split(";")[1], "pan": 0,
            "fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*BRASS.split(";")[4].split(":"))]}]}] if BRASS else []),
        {"name": "pad", "patch": "ct-glass", "gain": PAD.split(";")[0], "pan": -0.3, "sends": {"hall": PAD.split(";")[1]}},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
    ]
    if PIVOT:
        # Bring the already vibrating Ab3 up AFTER the amp; no second pick when the band enters.
        t = next(t for t in tracks if t["name"] == "wr")
        back = SECS[5][0]
        at = back - SIZE[2][0]
        points = [(0, 0), (at - 2, 0), (at - 1, -14), (at, -14), (back - 1, -6), (back, 0)]
        t["gain"] = {"value": t["gain"], "mod": [{"src": "auto.carry", "amount": 1}]}
        t["auto"] = {"carry": {"points": [[f"{p / 4:g}b", v] for p, v in points], "curve": 0}}
    if STEEL:
        tracks.append({"name": "bar", "patch": "em-steel", "gain": STEEL, "pan": 0.12,
                       "fx": [{"type": "eq", "bands": ["hp cutoff=440 q=0.707", "peak cutoff=1650 q=0.8 gain=3.5dB"]}]})
    if BOWL:
        rim, mallet = BOWL.split(";")
        room = " fx.0.mix=0.1 fx.0.decay=1s"
        tracks.extend([
            {"name": "rim", "patch": "singing-bowl-rim synth.amp.r=200ms" + room, "gain": rim + "dB", "pan": 0},
            {"name": "mallet", "patch": "singing-bowl synth.amp.d=2.6s synth.amp.r=200ms" + room, "gain": mallet + "dB", "pan": 0},
        ])
    if REVEAL:
        # Keep the turtles running. Damp the faster strings to expose their
        # slow relative: 144 = 34 + 21 + 34 + 21 + 34 sixteenths.
        span = SECS[6][2]
        for name, margin in (("harp7", SIZE[5][0]), ("harp7b", SIZE[6][0])):
            t = next(tr for tr in tracks if tr["name"] == name)
            # Automation on these offset tracks counts from the harp's first
            # pluck, not from beat zero of the song.
            lo, hi = margin, span - margin
            pts = [["0b", 0], [f"{(lo - 2) / 4:.8g}b", 0], [f"{lo / 4:.8g}b", -60],
                   [f"{(hi - .25) / 4:.8g}b", -60], [f"{hi / 4:.8g}b", 0]]
            t["gain"] = {"value": t["gain"], "mod": [{"src": "auto.damp", "amount": 1}]}
            t["auto"] = {"damp": {"points": pts, "curve": 0}}
    if CHILD:
        tracks.append({"name": "log", "patch": "log-drum play.glide=0ms play.gate=1 synth.env.p.d=35ms synth.amp.r=45ms",
                       "gain": CHILD, "pan": .4, "out": "drums"})
    if KETTLE:
        tracks.append({"name": "kettle", "patch": "em-kettle", "gain": KETTLE.split(";")[0], "pan": -0.1, "sends": {"hall": KETTLE.split(";")[1]}})
    if ARCO:
        # Straight to the mix, not through the bass guitar's compressor: a held note there would hold the chugs down.
        tracks.append({"name": "arco", "patch": ARCO.split(";")[0], "gain": ARCO.split(";")[1], "pan": 0.05,
                       "fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*ARCO.split(";")[3].split(":"))]}]})
    if IRON:
        tracks.append({"name": "iron", "patch": "em-iron", "gain": IRON.split(";")[0], "pan": float(IRON.split(";")[1])})
    for t in tracks:
        if "gen" not in t:
            t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", ROOTS[0][1]]], ROOTS[0][1]
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p / 4 - 0.02:g}b", prev], [f"{p / 4:g}b", r]]
            prev = r
    qpts = [["0b", 0]]
    for s0, kind, n in SECS:
        if kind == "S":
            qpts += [[f"{s0 / 4 - 0.02:g}b", 0], [f"{s0 / 4:g}b", float(QBASS)], [f"{(s0 + n) / 4 - 0.02:g}b", float(QBASS)], [f"{(s0 + n) / 4:g}b", 0]]
    return {
        "about": ("chirpers X (Common Time), track 7 by chirper-zero: Extreme and Mean. Two cells, a long of three sixteenths and a short "
                  "of two, and one rule: a long becomes a long and a short, a short becomes a long. The pattern it makes never loops and "
                  "is the same at every size, so the band plays it at many sizes at once: muted strokes, open notes, chords, crashes, "
                  "the root, and the song's own sections (long ones heavy, short ones quiet). The kit keeps common time against it. In "
                  "the quiet sections a wire harp has no notes, only the rule (the engine's L-system). The slow song: 80. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(HANDS.split(";")[5]) if HANDS else float(BREAK.split(";")[-1]) if BREAK else float(TIGHT.split(";")[3]) if TIGHT else float(CHUG.split(";")[2]) if CHUG else float(HOLD.split(";")[1]) if HOLD else REST_LUFS if REST else -10, "seed": 1, "tail": "5s", "length": f"{(TOTAL + 32) / 4:g}b", "event_stable": True,
        "patches": {
            **({"em-steel": {
                "extends": "pedal-steel synth.amp.a=75ms synth.amp.r=140ms fx.0.mix=0.08 fx.1.mix=0 fx.2.mix=0 play.glide=0ms",
                "about": "The moving bar against the two fretted guitars. Keep the pedal steel's vibrato, bend by hand within each note, and damp it before the band answers.",
                "synth": {"pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 0.06}, {"src": "expr.bend", "amount": 1}]}},
            }} if STEEL else {}),
            **({"em-kettle": {
                "about": ("Extreme and Mean's kettledrums (chirper-alpha, 18 Nov): the modal layer's `kettle` set (Rossing's 65 cm drum: the "
                          "air in the kettle tunes the head's modes near 1 : 1.5 : 2 : 2.44, so it sings the note it is given), struck a "
                          "quarter of the way in from the rim, with a felt head's soft thud. `expr.pedal` is the pedal, in semitones: "
                          "the head follows it while it rings."),
                "synth": {"pitch": {"value": 0, "mod": [{"src": "expr.pedal", "amount": 1}]},
                          "layers": [{"name": "head", "type": "modal", "modes": "kettle", "strike": {"value": 0.72, "mod": [{"src": "rand", "amount": 0.05}]},
                                      "decay": "5s", "damp": 0.2, "sharp": 10, "vary": 0.3},
                                     {"name": "felt", "type": "noise", "color": "brown",
                                      "level": {"value": "-60dB", "mod": [{"src": "env.att", "amount": 36}, {"src": "vel", "amount": 6}]}}],
                          "env": {"att": {"a": "0.5ms", "d": "16ms", "s": 0}},
                          "filters": ["hp cutoff=45", "lp cutoff=2400"],
                          "amp": {"a": "0.3ms", "d": "5s", "s": 0, "r": "350ms", "curve": 2}},
                "play": {"vel_sens": 0.6, "gate": 1, "poly": 32}}} if KETTLE else {}),
            **({"em-iron": {
                "about": ("Extreme and Mean's iron (chirper-three, 18 Nov): a struck bar whose overtones are cut in extreme and mean "
                          "ratio. Each partial is to the next as 1.618 to 1 (1 : 1.618 : 2.618 : 4.236 : 6.854 : 11.09 : 17.94), so each "
                          "partial's frequency is the sum of the two below it. `expr.cut` 1 is the bar a golden cut shorter (833 cents "
                          "up): all of its partials are partials of the long bar. A hammer's click, a short ring, no sustain."),
                "synth": {"pitch": {"value": 0, "mod": [{"src": "expr.cut", "amount": round(12 * __import__("math").log2(PHI), 4)}]},
                          "layers": [{"name": "bar", "type": "additive", "damp": 0.45,
                                      "partials": [[round(PHI ** k, 6), g] for k, g in enumerate(
                                          (float(IRON.split(";")[3]), 1, 0.9, 0.75, 0.5, 0.3, 0.15))]},
                                     {"name": "hammer", "type": "noise", "color": "white",
                                      "level": {"value": "-60dB", "mod": [{"src": "env.tap", "amount": 44}, {"src": "vel", "amount": 6}]}}],
                          "env": {"tap": {"a": "0.2ms", "d": "5ms", "s": 0}},
                          "filters": ["hp cutoff=300", "lp cutoff=9500"],
                          "amp": {"a": "0.3ms", "d": "650ms", "s": 0, "r": "50ms", "curve": 2}},
                "play": {"vel_sens": 0.5, "gate": 1, "poly": 8, "humanize": {"time": "0ms", "vel": 0}},
                "fx": ["reverb kind=room decay=0.5s mix=0.1 predelay=6ms"]}} if IRON else {}),
            "ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
            "em-harp": {"about": ("Extreme and Mean's wire harp (chirper-zero, 17 Nov): the library's ks-harp (Karplus-Strong, stretch 3) with a "
                                  "release long enough for a sixteenth-long pluck to ring on."),
                        "gain": "-5dB",
                        "synth": {"amp": {"a": "1ms", "d": 0, "s": 1, "r": "2.5s"},
                                  "layers": [{"type": "ks", "bright": 0.8, "decay": "5s", "ks": {"blend": 1, "stretch": 3}}]}},
        },
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                    {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]},
                           {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.quiet", "amount": 1}]}}],
                    "auto": {"key": {"points": pts, "curve": 0}, "quiet": {"points": qpts, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T7_MASTER", "2.7dB")}]},
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
    if os.environ.get("C10T7_SHOW"):
        sec = 15 / BPM
        for i, (s0, kind, n) in enumerate(SECS):
            print(f"section {i + 1} {kind} {'heavy' if kind == 'L' else 'quiet'}  sixteenths {s0}-{s0 + n}  bars {s0 / 16 + 1:.2f}-{(s0 + n) / 16 + 1:.2f}  "
                  f"{int(s0 * sec) // 60}:{s0 * sec % 60:04.1f}-{int((s0 + n) * sec) // 60}:{(s0 + n) * sec % 60:04.1f}  key +{KEY[i]}")
        print("the first 34 cells:", "".join(c[1] for c in LEV[0][:34]))
        print("their sizes:       ", "".join(str(min(RANK[c[0]], 9)) for c in LEV[0][:34]))
        print("the harp's steps:  ", "".join(str(x) for x in harp_tune(8)))
    else:
        open(OUT, "w").write(dump(song()))
