#!/usr/bin/env python3
"""chirpers10-t8 "Common Measure" (chirper-zero): two riffs of different lengths, argued down to what they share.

Euclid finds the greatest common measure of two lengths by taking the less from the greater, again and again: what is
left over is set against the shorter one, and what that leaves against the leftover, until something goes in exactly.
That last length measures both. This piece is the algorithm played by two guitars, and it is the record's fast song
(160 where the other seven run 80 to 138).

The left guitar has a riff of 52 sixteenths (A); the right has one of 32 (B, two bars). Played together they meet
again only after 26 bars. Then, each section, the longer riff is cut down to WHAT WAS LEFT OVER: its own tail.

  the two given     bars 0-8      B alone on the right: the short riff, twice bare and twice with the band
  52 against 32     bars 8-34     A on the left, B on the right: one whole cycle, 26 bars
  20 against 32     bars 34-54    the left keeps only A's last 20 sixteenths (52 - 32): they meet every 10 bars
  20 against 12     bars 54-69    the right keeps only B's last 12 (32 - 20): every 3 bars and three quarters
  8 against 12      bars 69-81    the left keeps its last 8 (20 - 12): every bar and a half
  8 against 4       bars 81-89    the right keeps its last 4 (12 - 8): every half bar. Four goes into eight: it is found
  the measure       bars 89-105   both guitars, and two more, on the four sixteenths both riffs END with: one beat. The
                                  beat is the common measure; the cell climbs the record's hook notes as chords
  measured          bars 105-126  now the two riffs can be said together: all four guitars play A four times, then B
                                  four times, in unison, the kit's four in a bar under them (A is thirteen beats, B eight)
  one chord         bar 126

The bass and the kick go with the SHORTER riff of each pair (the one doing the measuring), so the rhythm section's
cycle shrinks section by section: two bars, a bar and a quarter, three beats, half a bar, a beat. WHAT IS LEFT OVER
IS HEARD ALONE: at the end of each pair the band stops and the longer riff plays its tail by itself (20 sixteenths,
then 12, 8, 4: the breaks shrink too), and that tail is the next section's riff. The kit keeps common time
throughout, its feel changing with each cut, and crashes wherever the two riffs meet, so the crashes come closer and
closer: 39 seconds apart, then 15, 5.6, 2.25, and at last the china on every beat. THE ARGUMENT NARROWS: each riff is
two takes a side until 8 against 12, where it is one; at 8 against 4 the bass and the kick drop out (the kick comes
back half way) and the snare counts every beat, louder and louder; two beats of nothing; then the measure, with every
guitar there is.

Track 7 (Extreme and Mean) is the cut that has no common measure, slow, never looping. This is its pair: the two
lengths here do have one, and the song is the finding of it. 52 and 32 are four times 13 and 8, so the algorithm takes
as long as it can (every quotient is one) and ends on four sixteenths: the beat of common time, where the record began.

v1 is the SKELETON (Harry, 17 Nov about 03:40: "open up 2 new song slots"; track 2's terms: mine, my title, a
skeleton first): the whole shape standing, bare.
"""
import json
import os
from math import log2

OUT = os.environ.get("C10T8_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t8.yaml"))
BPM = 160
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
# v2, THE TWO BELLS: each riff has a bell that rings where the riff begins again, the left riff's low and on the left, the
# right riff's a fourth higher and on the right. As the riffs are cut down the bells come faster and closer, and at the
# measure they ring together on every beat. gain, dB ; velocity ; velocity in the measure ; the low bell's dB over the
# high one's (it reads 2.4 dB quieter at the same gain). "" = v1 (no bells).
BELLS = os.environ.get("C10T8_BELLS", "-12;0.9;0.95;1.5")
# v3, WHAT WAS CUT AWAY COMES BACK: the long riff's head (the hook coming down: E flat, C, B, A flat, G flat, F) was the
# first thing the algorithm cut off, at 0:51. At the measure a lead guitar plays it again, each note held for two
# bars over the cell that measures it, against the chords climbing the same notes the other way. Then the F again and
# the F above. patch ; gain ; hall send ; semitones over the low F. "" = v2 (no lead).
HEAD = os.environ.get("C10T8_HEAD", "lead-monster;-12dB;-12dB;36")
# v4: in the one-guitar-per-side pair, the right riff's three rising notes are
# stretched to the distance between joint landings, then gathered back to tempo.
# Empty switches the section off, giving v3 exactly. This part is dry: let the
# bare last tail belong to the guitars.
BREATH = os.environ.get("C10T8_BREATH", "shaper-reed;-13dB")
# v5: the bass takes the measuring riff; the guitars answer with what's left.
BASS_BREAK = os.environ.get("C10T8_BASS_BREAK", "1")
# v6: the kit learns B's surviving tail in the measured coda. Empty = v5.
STICKS = os.environ.get("C10T8_STICKS", "1")
# v7: a different left-hand string spans exactly the length about to be
# subtracted, never the surviving tail. Track gain; empty restores v6.
SPAN = os.environ.get('C10T8_SPAN', '-11dB' if STICKS else '')
# v8: count the shorter riff on the china, play the leftover tail on a güiro.
# Empty = v7; the published SPAN and earlier rollback switches still work.
SCRAPER = os.environ.get('C10T8_SCRAPER', '-3dB' if SPAN else '')
# v9: felt piano folds the six-note head of A into three grips, then opens
# them again. Trim in dB. Empty restores v8 and earlier switches still work.
FELT = os.environ.get('C10T8_FELT', '-5dB' if SCRAPER else '')
# v10: one held B against two picked F cells. Empty restores v9. Keep the
# earlier rollback flags restoring the same versions their notes promised.
TWICE = os.environ.get('C10T8_TWICE', '1' if FELT else '')
# v11: after the loud final chord, put the two riffs back together by addition.
# Empty restores v10; the older version switches keep working.
AFTER = os.environ.get('C10T8_AFTER', '1' if TWICE and BREATH and BASS_BREAK else '')
# v12: one electronic key voices 20:12 as frequencies, 5:3. Swap only the
# inner left guitarist's pitched attacks in four middle answers. Empty = v11.
SIDEBANDS = os.environ.get('C10T8_SIDEBANDS', '-13.5dB' if AFTER else '')
# v13: B's frets go up one string while A's E-bow comes down its harmonics.
CONVERGE = os.environ.get('C10T8_CONVERGE', '1') if SIDEBANDS and SPAN else ''  # empty = v12
# v14: at every cut the leftover is still heard alone, but only up to the one
# beat both riffs end with. There the side that had stopped says its own
# ending (the same four sixteenths) with the bass, the foot and both bells:
# sixteen sixteenths alone, then eight, then four, then none. Empty = v13;
# it is on only while the older switches are, so each still gives what it gave.
SHARED = os.environ.get('C10T8_SHARED', '1' if CONVERGE and BELLS and HEAD else '')
# v15: the second half of the first bass break (1:13.5 to the cut). The bass
# has the left riff's twenty and lifts its three pitched notes off the thumb.
# The left guitar, silent since 1:06, comes back on just those notes and lets
# each ring until the next: the last one first, then two, then all three,
# and the fourth time the cut takes the line after its first note.
# Semitones over the bass's lifted notes ; which left guitar. On the main one
# the line read 2 dB over the bass it follows, and a note's own gain does
# nothing ahead of a saturated amp, so it is the inner take, 3.2 dB lower.
# Empty restores v14.
RING = os.environ.get('C10T8_RING', '12;dl' if SHARED and BASS_BREAK else '')
# v16 (palette): a koto says the rest of A. In 'measured' the felt piano
# already spells the riff's six-note head, three octaves over the guitars
# (v9). Where the piano stops, a koto goes on in the same octave with every
# note of the riff that is not a clipped stroke: F C B, F A flat, F E flat,
# B, F. So on the second, third and fourth A the whole tune is heard above
# six guitars, hammered and then plucked. On the fourth it stops where the
# bass takes the tail alone. Thirteen strings, each tuned by where its bridge
# stands, for a riff thirteen beats long.
# Semitones over the low F ; track gain. Benched at -6 dB: its notes read
# 9.4 dB under the raw mix (the piano's 7.3, in a thinner band), so -7.
# Empty restores v15; it is on only
# while every older switch is, so each of those still gives what it gave.
KOTO = os.environ.get('C10T8_KOTO', '36;-7dB' if all((
    RING, SHARED, CONVERGE, SIDEBANDS, AFTER, TWICE, FELT, SCRAPER, SPAN, STICKS, BASS_BREAK, BREATH, HEAD, BELLS)) else '')
# v17 (palette): the timeline. A is thirteen beats long and B eight, and the
# most even way to spread eight strokes over thirteen beats is what the
# algorithm this song plays gives when it is run on a rhythm. A pair of claves
# (a patch of the song's own) plays it against A, from A's fourth statement
# (0:26.6, after the opening the card plays) to the first cut: four times
# eight in thirteen, and over the last head, which is as long as B, five in
# eight: the next pair's two numbers. Not one stroke is written here: the
# track's score is the pairs of numbers and the engine's Euclidean rhythm
# lays them out. Pitch ; track gain ; pan ; A's first statement with it
# (counted from 0). Benched at -6 dB the strokes read 5.7 dB under the mix,
# 2.5 over the left bell that marks the same riff; at -9.5 they sit under it.
# Empty restores v16.
TIMELINE = os.environ.get('C10T8_TIMELINE', 'c7;-9.5dB;-0.3;3' if KOTO else '')
# v18 (palette): where the claves keep the timeline, the hi-hat's eighths go
# to a shekere: the same strokes, the same accents, on a beaded gourd in the
# place the hat had. The hat is on all thirteen songs; this passage now has
# the song's own percussion instead (bell, sticks, shaker; the scraper comes
# at 0:56) and the kit keeps only kick and backbeat until the cut.
# Track gain ; pan ; the beads' top in Hz. The library's shekere (afro-perc
# `sk`, closed at 11 kHz) at 0 dB sat 1.7 dB under the hat and took 1.4 dB
# off the passage at 8-16 kHz: the hat left and little came. So the song has
# its own, open to 14 kHz, 3 dB up, with a little of the overheads' room
# (none: 0.4 dB short at 8-16 kHz; the hat's own send of 4.5 dB: 2.2 dB
# over there and 1.4 at 4-8 kHz). Track gain ; pan ; the beads' top in Hz ;
# overhead send. Empty restores v17.
SHAKER = os.environ.get('C10T8_SHAKER', '3dB;-0.45;14000;-5dB' if TIMELINE else '')
# v19 (section w4): the foot crosses over. The bass and the kick go together
# with the shorter riff of every pair, so at each cut they jump to the other
# side as one. At 8 against 4 they both drop out, and when the kick comes
# back (2:07.5) it is on the right, with the cell. Now it crosses before it
# leaves: for the last meetings of 8 against 12, after the reed has gone, the
# kick plays the right riff's strokes (the three rising notes and the cell)
# and the bass stays with the left. It is the only place in the song where
# the bass and the foot are on opposite sides: the argument divides even
# them, just before the answer is found. By subtraction: every stroke of the
# right riff already had a kick under it; the kick gives up the six a cycle
# that were the left's alone. The snare and the hat keep common time, as
# they do throughout. It begins after the first backbeat (1:57.4): the reed
# card's clip runs to 1:57.3. The value is the number of meetings. Empty
# restores v18.
CROSS = os.environ.get('C10T8_CROSS', '2' if SHAKER else '')
# v20: TWO OF HARRY'S ANSWERS, built as given (chirper-zero, 19 Nov).
# cm-bass-break, "Does the riff come through better on the bass?": "Prefer the full riff". The first bass break
# (1:06-1:21, the second half of 20 against 32) gives the riff back: the four guitars play both riffs to the cut,
# the bass is back under them, and v15's ringing line over that break is not called. The second break (1:32) and
# the bass tails in 'measured' stay: he was asked about the first only, and called the tails "good".
# cm-reed, "Does the reed bring out the guitar riff?": "Keep it, but quieter". 4 dB off the reed while it shadows
# the right guitar (it stood 6.4 to 8.6 dB under the rest of the raw mix; now 10.4 to 12.6); the afterword's reed
# keeps its level (a gain on a lane, not the fader).
# which bass breaks give way (1 = 1:06, 2 = 1:32; comma list, or nothing) ; dB on the reed up to 8 against 4 ;
# the loudness target (every other bar keeps v19's mastering gain: within 0.01 dB, both seeds). Empty restores v19.
# The scorer falls 7.5 and 3.3 points (it counted the break as a returning section); kept on his answer.
FULL = os.environ.get('C10T8_FULL', '1;-4;-10.045' if CROSS and BASS_BREAK and BREATH else '')
# v21 (chirper-alpha; section w3, 1:06-1:32): EACH RIFF HAS ITS OWN NOTE. Since v20 gave the riff back to the
# guitars the thirty seconds from 1:00 are the song's static window (its map says so, and v20's handoff). The
# song's own arithmetic has something to say there that it has not said yet. Two lengths are also two NOTES: a
# thing that comes round every 20 sixteenths and a thing that comes round every 32 stand to each other as two
# strings whose lengths are 20 and 32, and two strings 5 to 8 sound a minor sixth. So every pair in this song is
# an interval, and Euclid's steps are a cadence: 52 against 32 is 13 to 8 (a sixth between the minor and the
# major, the roughest); 20 against 32 is 5 to 8, a minor sixth; 20 against 12 is 5 to 3, a major sixth; 8 against
# 12 a fifth; 8 against 4 an octave; and the measure is a unison. The argument comes to rest in pitch as it does
# in time. THIS ROUND SAYS TWO OF THOSE STEPS, the two in this window: from 1:06, where the two riffs meet
# again, each side has a bowed guitar string that sounds THE RIFF'S OWN NOTE once for each time the riff comes
# round, and holds it as long as the riff lasts: on the left A flat (every 20), on the right the C below it
# (every 32): the longer riff is the lower note and the slower pulse. At the cut (1:21) the left riff is what
# it was, so its note stays; the right riff is cut from 32 to 12, so its note goes up an octave and a fourth,
# to the F above the A flat, and comes round nearly three times as often. They stop where the bass takes the
# riff (1:32). No riff, bell, bass or drum stroke is changed: all four guitars keep both riffs (his answer).
# The notes are the pure ones (8:5, then 5:3), set so that the F is the band's own F.
# THE STRINGS STAND STILL AND ARE TUNED DOWN, as track fourteen's held chords are (v3 there): an interval is only
# pure between notes that do not move. The library's e-bow has a vibrato of 18 cents either way from 0.9 s and
# strikes each note up to 3 cents off; both are off here. And it reads SHARP, as every string of this engine does
# (bead bd-d2ee40): alone and still, C4 +3.5 cents, A flat 4 +6.0, F5 +9.3. So each note is written that much flat
# (the third field, cents for the 32's, the 20's and the 12's note); after it they read within 1.2 cents of the
# pure notes (a first trim, taken with the random detune still on, was 3 cents too much on two of them).
# gain ; the note the measure itself would have (MIDI; a riff's note is that, lower by its length over four) ;
# cents each note is written flat, by riff length 32 : 20 : 12 ; velocity ; the loudness target. "" = v20.
# (Level: benched raw at -12 dB the two strings stood 6.2 and 5.4 dB under the rest of the band, K-weighted; he asked
# for the reed 'quieter' from there, and it now stands 10.4 to 12.6 under. At -17 dB the strings stand 11.2 and 10.4 under.)
OWN = os.environ.get('C10T8_OWN', '-17dB;96.01955;3.5:6.0:9.3;0.85;-10.015' if FULL else '')
# v22 (chirper-two; section w1, the opening half minute, which the map calls static and no round had worked; the
# same joint comes once more 5.6 s into w2): THE ANSWER PASSES BY.
# The two riffs end with the same four sixteenths, the cell, and the song takes two minutes to find that this one
# beat is their common measure. But the answer is in the first cycle already. Three times 52 is 156 and five times
# 32 is 160: at 0:26.6 the left riff ends and one beat later the right riff ends. Eight times 32 is 256 and five
# times 52 is 260: at 0:36.0 the right ends and one beat later the left. Two such riffs can never come closer than
# that without meeting (every distance between their endings is a multiple of their measure, and the measure is the
# least of them), so twice in the 39 seconds the two endings are said back to back: the cell on one side, then the
# cell on the other. It was always in the notes; under a full band nobody could hear it.
# NOW THE BAND STOPS FOR IT, as it does for what is left over at every cut. For the beat in which the first riff
# ends, its two guitars play the cell ALONE: the other side, the bass, the foot and the hands all rest. For the
# next beat the other side answers with the same cell, as written (the bass and the foot are back; the first side
# has begun its riff again), and the hands still rest. Then the hands come back.
#   0:26.25  the left pair alone   0:26.625 the right pair answers   0:27.0   the kit's hands return, with the shekere
#   0:35.625 the right pair alone  0:36.0   the left pair answers    0:36.375 the snare's backbeat, the left riff's head
# BY SUBTRACTION: 26 strokes are taken out and three notes end early (the right riff's B before the first break:
# it is one stroke now, and the C after it is the one note of either riff that is not said); nothing is added. The
# bells are untouched, so at each place the two of them ring one beat apart in the open.
# MEASURED (finished file, seed 0, K-weighted, the bare beat): at 0:26.25 the left channel stands 6.8 dB over the
# right (0.6 under before) and what is over 6 kHz falls 11.6 dB; at 0:35.625 the right stands 8.8 dB over the left
# (level before) and over 6 kHz falls 13.8 dB. Every other bar keeps v21's gain within 0.018 dB (both seeds).
# which of the two places get the break (1 = 0:26.25, 2 = 0:35.6; comma list) ; the loudness target ("" = unchanged).
# Empty restores v21.
PASS = os.environ.get('C10T8_PASS', '1,2;' if OWN else '')



def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# o an open low root, c a muted stroke, r a rest, - a held place, a number a hook note (semitones over the root)
A = ("10 - - 7 - - 6 - 3 - - 1 - - o - "          # the hook coming down in threes and twos
     "c c r c c r c r o c c r 7 - 6 - "
     "o c c 3 - c o c c 10 - c "                   # (its last 20 begin here)
     "6 - c c o - c c").split()                    # (its last 8)
B = ("o r c c r c c r o r c c r 1 - r "
     "o c c r "
     "3 - - 6 - - 7 - "                            # (its last 12 begin here)
     "o - c c").split()                            # (its last 4: the measure)
assert len(A) == 52 and len(B) == 32 and A[-4:] == B[-4:]
G = B[-4:]

# the algorithm: (left riff, right riff); the shorter of each pair carries the bass and the kick
PAIRS = []
_l, _r = A, B
while len(_l) != len(_r):
    PAIRS.append((_l, _r))
    if len(_l) > len(_r):
        _l = _l[-(len(_l) - len(_r)):] if len(_l) - len(_r) > 0 else _l
    else:
        _r = _r[-(len(_r) - len(_l)):]
assert [(len(a), len(b)) for a, b in PAIRS] == [(52, 32), (20, 32), (20, 12), (8, 12), (8, 4)] and _l[-4:] == G and _r == G
REPS = [1, 2, 4, 8, 16]                   # how many times each pair runs its whole cycle
INTRO = 8 * 16
HOOK = [0, 3, 6, 1, 7, 10, 0, 0]          # the measure's roots, two bars each: the record's hook notes in their order


def lcm(a, b):
    x, y = a, b
    while y:
        x, y = y, x % y
    return a * b // x


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


def say(riff, t, gtrs, low=False, root=0, chord=False, stop=None, bass=True):
    """One statement of a riff from sixteenth t (cut at `stop`), on the guitars `gtrs`; with the kick, and the bass
    unless `bass` is off, if `low`."""
    for i, k in enumerate(riff):
        if k in "r-" or (stop is not None and t + i >= stop):
            continue
        n = 1
        while i + n < len(riff) and riff[i + n] == "-":
            n += 1
        at = t + i
        if k == "c":
            for tr in gtrs:
                add(tr, at, 1, F1 + root, 0.88, pm=1)
            if low:
                if bass:
                    add("bass", at, 1, F1 + root, 0.88)
                drum("k", at, 0.88)
        else:
            semi = 0 if k == "o" else int(k)
            pitch = ",".join(nm(F1 + root + j) for j in (0, 7, 12)) if chord and k == "o" else F1 + root + semi
            for tr in gtrs:
                add(tr, at, n, pitch, 1.0 if k == "o" else 0.95)
            if low:
                if bass:
                    add("bass", at, n, F1 + root + semi, 0.95)
                drum("k", at, 0.95)


def beat(s0, s1, cym="h", step=2, vel=0.5, snare=(4, 12)):
    for q in range(s0, s1, step):
        drum(cym, q, vel + (0.05 if (q - s0) % 16 == 0 else 0))
    for q in range(s0, s1, 16):
        for b in snare:
            if q + b < s1:
                drum("s", q + b, 0.95)


def fill(s):
    """The last half bar before sixteenth s."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, s - 8 + i, 0.6 + 0.045 * i)


ALL = ("gl", "gr", "dl", "dr", "wl", "wr")
def bell(side, s16, root=0, vel=None):
    if BELLS:
        add("bell-" + side, s16, 1, F1 + root + (55 if side == "l" else 60), float(BELLS.split(";")[1]) if vel is None else vel)


MARKS = [("the two given", 0)]            # (name, first sixteenth)
ROOTS = [(0, 0)]


def bass_break(start, stop, short, long, short_side, long_side):
    """The shorter riff is already in the bass and foot. Give it the stage.

    Leave the longer guitar only the remainder at the end of each cycle, in
    its original place. Its last exposed tail, beyond stop, is untouched.
    """
    def keep(track, p):
        if not start <= p < stop:
            return True
        return track in long_side and (p - start) % len(long) >= len(short)

    for tr in short_side + long_side:
        T[tr] = [n for n in T[tr] if keep(tr, round(n['at'] * 4))]
    pop_tail(start, stop, short)


def pop_tail(start, stop, riff):
    # Thumb the low F; take only the changing, pitched notes up one string octave.
    # Same attacks and rests, so the kick and the picking hand keep their pattern.
    for note in T['bass']:
        p = round(note['at'] * 4)
        if start <= p < stop:
            token = riff[(p - start) % len(riff)]
            if token.isdigit():
                note['pitch'] = nm(F1 + 12 + int(token))


def unfold_head(start, pass_no):
    """The head of the *whole* A, back in the coda: six notes, heard in pairs.
    Second A: play each pair as a chord. Third: unroll the lower key halfway.
    Fourth: the two hands play the original descent at the original times.
    """
    end = A.index('c')  # the first muted stroke ends the descending head
    heads = [(i, int(k) if k.isdigit() else 0) for i,k in enumerate(A[:end]) if k != '-']
    assert len(heads) == 6 and 1 <= pass_no <= 3
    # Always leave the main takes playing. Only their doubles give up notes;
    # the second twin pair rejoins on the third A, the wall pair after each head.
    for tr in (('wl', 'wr', 'dl', 'dr') if pass_no == 1 else ('wl', 'wr')):
        T[tr] = [n for n in T[tr] if not start <= round(n['at']*4) < start+end]
    for j in range(0, len(heads), 2):
        first, upper = heads[j]; second, lower = heads[j+1]
        stop = heads[j+2][0] if j+2 < len(heads) else end
        enter = first + (second-first)*(pass_no-1)/2
        # Open voicings on the first two passes. The last closes up into one
        # register, so the piano hands the actual six-note line back intact.
        upper_end = second if pass_no == 3 else stop
        add('felt', start+first, upper_end-first-.20, F1+36+upper, .92)
        add('felt', start+enter, stop-enter-.20, F1+(36 if pass_no==3 else 24)+lower, .84, soft=.35)


def the_rest_on_thirteen_strings(start, upto):
    """After the piano's head: the notes of A that are not clipped strokes, each ringing to the next."""
    head = A.index('c')
    up = int(KOTO.split(';')[0])
    notes = [(i, 0 if k == 'o' else int(k)) for i, k in enumerate(A) if head <= i < upto and k not in 'cr-']
    for (i, semi), following in zip(notes, [i for i, _ in notes[1:]] + [upto]):
        # The open F is the string the tune keeps coming back to: softer than the notes that move.
        add('koto', start + i, min(following - i, 6) - .15, F1 + up + semi, .93 if semi else .84)


def twice_under_one(start, long, short):
    """The last exact division, played in the hands rather than just marked by bells."""
    size, unit = len(long), len(short)
    assert size == 2*unit and long[-unit:] == short == G
    # Let the first eight announce the pair as written. On successive turns
    # the left lets its B through more of the riff instead of choking it on F.
    # Four, six, then all eight places. Hold the full span twice: the first
    # time the right hand picks every stroke, the second just its two open Fs.
    for i, span in enumerate((unit, unit+unit//2, size, size), 1):
        at = start + i*size
        T['gl'] = [n for n in T['gl'] if not at <= round(n['at']*4) < at+span]
        add('gl', at, span, F1 + 12 + int(long[0]), .94)
        if i == 4:
            T['gr'] = [n for n in T['gr'] if not (at <= round(n['at']*4) < at+size and n.get('expr', {}).get('pm'))]


def measured_drums(start, stop):
    """Four statements of B: keep time, play its tail, anticipate it, land it."""
    tail = PAIRS[2][1]  # the twelve B still had after 32 minus 20
    assert B[-len(tail):] == tail and tail[-len(G):] == G
    notes = [i for i, token in enumerate(tail) if token.isdigit()]
    shells = ("ft", "t2", "t1")
    assert len(notes) == len(shells)
    first_b = stop - 4 * len(B)
    beat(start, first_b, cym="x", step=4, vel=.5)
    # Quote the kit's first two bars: only the hat counts quarters. B is
    # now in all the guitars instead of one, so the opening returns changed.
    beat(first_b, first_b + len(B), cym="h", step=4, vel=.45, snare=())
    T["kick"] = [n for n in T["kick"] if not first_b <= round(n["at"] * 4) < first_b + len(B)]
    T["cym"] = [n for n in T["cym"] if not (n["pitch"] == "c" and round(n["at"] * 4) == first_b)]
    for rep in (1, 2, 3):
        base = first_b + rep * len(B)
        tail_at = base + len(B) - len(tail)
        lead = len(tail) - len(G) if rep == 2 else 0
        phrase = tail_at - lead
        # No continuous backbeat under the shell phrase. In the third B, a
        # short closed hat in the head leaves air around the coming bass solo.
        beat(base, phrase, cym="h" if rep == 2 else "x", step=4, vel=.5)
        velocities = {1: (.78, .85, .92), 2: (.66, .74, .83), 3: (.87, .93, .99)}[rep]
        for i, piece, v in zip(notes, shells, velocities):
            drum(piece, phrase + i, v)
        common = base + len(B) - len(G)
        if rep == 2:
            # After the drummer's early answer, leave the three popped notes
            # to the bassist. Foot comes back for the shared one-beat cell.
            if BASS_BREAK:
                T["kick"] = [n for n in T["kick"] if not tail_at <= round(n["at"] * 4) < common]
        elif rep == 1:
            drum("s", common, .92)
        else:
            # Replace the stock eight-stroke fill with the actual o - c c.
            drum("ft", common, .92)
            drum("s", common, .92)
            for i, token in enumerate(G):
                if token == "c":
                    drum("s", common + i, .70 if i == len(G) - 2 else .89)


def afterword(start):
    """The Euclidean cuts in reverse: one beat, then 8, 12, 20, 32, 52 ticks.
    These are the original pitches AND rests, not a scale pasted over the sums.
    Each new head has the other riff's length. The other player lends it a
    voice; the surviving tail answers in the riff's own voice. The common
    four places at the end of every statement belong to the bass alone.
    """
    t = start
    phrases = [G] + [max(pair, key=len) for pair in reversed(PAIRS)]
    for i, riff in enumerate(phrases):
        tail = G if i < 2 else phrases[i-2]
        cut = len(riff) - len(tail)
        assert riff[cut:] == tail and tail[-len(G):] == G
        if i:
            assert cut == len(phrases[i-1])
        for k, token in enumerate(riff):
            if token in ('r', '-'):
                continue
            n = 1
            while k+n < len(riff) and riff[k+n] == '-':
                n += 1
            if k >= len(riff)-len(G) or token == 'c':
                add('bass', t+k, .67 if token=='c' else n-.12, F1, .77 if token=='c' else .94)
                continue
            # A is the keys' phrase, B the reed's. At the cut the lending
            # instrument lets go: no drums or loud guitar marking the seam.
            piano = (i%2 == 1) != (k < cut)
            semi = 0 if token=='o' else int(token)
            add('felt' if piano else 'breath', t+k, n-.12, F1+(24 if piano else 36)+semi, .88)
        t += len(riff)
    assert (t-start)%16 == 0
    return t


def compose():
    # the two given: B alone on the right, twice bare (a hat in quarters) and twice with the band
    for i in range(4):
        say(B, i * 32, ("gr", "dr") if i >= 2 else ("gr",), low=i >= 2)
        bell("r", i * 32)
    beat(0, 64, cym="h", step=4, vel=0.45, snare=())
    beat(64, INTRO)
    t = INTRO
    for (left, right), reps in zip(PAIRS, REPS):
        a, b = len(left), len(right)
        cyc = lcm(a, b)
        n = cyc * reps
        MARKS.append((f"{a} against {b}", t))
        k = PAIRS.index((left, right))
        last = k == len(PAIRS) - 1
        # WHAT IS LEFT OVER IS HEARD ALONE: for the last |a - b| sixteenths of a pair the longer riff plays its tail by
        # itself (that tail is the next section's riff). The last pair leaves nothing over: two beats of silence instead
        stop = t + n - (8 if last else abs(a - b))
        # THE ARGUMENT NARROWS: the last two pairs are one guitar a side, and the last has no bass; the measure gets everything
        gl, gr = (("gl", "dl"), ("gr", "dr")) if k < 3 else (("gl",), ("gr",))
        kick_from = t + n // 2 if last else t          # the last pair: the guitars alone for its first half, then the kick

        def grow(q, t=t, stop=stop):                   # in the last pair the bells grow with the snare (0.5 to 0.9)
            return 0.5 + 0.4 * (q - t) / (stop - t)
        for i in range(n // a):
            at = t + i * a
            if SPAN and k == 0 and i >= n // a - 4:
                # 52 - 32 = 20. The main left guitar keeps all 52. Its double
                # takes up the E-bow for 32, then picks the last 20 as before.
                say(left, at, gl[:1])
                say(left[b:], at + b, gl[1:])
                h = n // a - i                # 4, 3, 2, then the open string
                add('span', at, b, F1 + 12, .89, nh=h if h>1 else 0)
            else:
                say(left, at, gl, low=a < b and at >= kick_from, stop=stop if last or a < b else None, bass=not last)
            if not (last or a < b) or t + i * a < stop:
                bell("l", t + i * a, vel=grow(t + i * a) if last else None)
        for i in range(n // b):
            # In v4 the right guitarist lets the reed take the three pitched
            # attacks. His four-place tail and bell still give the riff its
            # full twelve places. First one of every two statements answers,
            # then he waits; at landing six the pitches meet in octaves.
            leave_head = BREATH and k == 3 and i*b < 5*cyc and (i % 2 == 0 or i*b >= 3*cyc)
            played = ["r" if token.isdigit() else token for token in right] if leave_head else right
            say(played, t + i * b, gr, low=b < a and t + i * b >= kick_from, stop=stop if last or b < a else None, bass=not last)
            if not (last or b < a) or t + i * b < stop:
                bell("r", t + i * b, vel=grow(t + i * b) if last else None)
        if SHARED and not last:
            # What the two riffs have in common is the only thing they say together at a cut.
            cell_at = t + n - len(G)
            longer, others = (left, gr) if a > b else (right, gl)
            assert stop <= cell_at and longer[-len(G):] == G and (t + n - stop - len(G)) in (16, 8, 4, 0)
            say(G, cell_at, others, low=True)
            bell("l", cell_at)
            bell("r", cell_at)
        if last and TWICE:
            twice_under_one(t, left, right)
        if BASS_BREAK and k in (1, 2) and str(k) not in FULL.split(';')[0].split(','):
            # On the second half of each pair the measuring hand switches side:
            # A's twenty places against B's twelve-place answer, then the reverse
            # subtraction with twelve in the bass and eight in the answer.
            args = (left, right, gl, gr) if a < b else (right, left, gr, gl)
            bass_break(t + n // 2, stop, *args)
        if k == 0:
            fill(t)
        drum("c", t, 0.9)
        for i in range(1, reps):                       # a crash wherever the two riffs meet again
            if cyc >= 24:
                drum("c", t + i * cyc, 0.75 if cyc >= 60 else 0.65)
        # the kit keeps common time, and its feel changes with each cut
        if k == 0:
            beat(t, stop)                                              # a hat in eighths, the snare on two and four
        elif k == 1:
            beat(t, stop, cym="x", step=4)                             # the china in quarters
        elif k == 2:
            beat(t, stop, cym="x", step=4, snare=(8,))                 # half time: the snare on three
        elif k == 3:
            beat(t, stop)                                              # the hat again, the backbeat back
            if BREATH:
                # Right begins Ab-- B-- C-. Give each note first a whole
                # landing (24 sixteenths), then three times and twice its
                # written length, then let the reed meet the actual guitar.
                heads = [(i, int(token)) for i, token in enumerate(right) if token.isdigit()]
                assert [i for i, _ in heads] == [0, 3, 6]
                for j, (_, pitch) in enumerate(heads):
                    add("breath", t + j * cyc, cyc - 2, F1 + 36 + pitch, 0.79 + 0.035 * j)
                for h, stretch in ((3, 3), (4, 2), (5, 1)):
                    for j, (i, pitch) in enumerate(heads):
                        # The two quicker answers overblow an octave; come
                        # back down when both play the three pitches together.
                        add("breath", t + h * cyc + i * stretch, (3 if j < 2 else 2) * stretch - 0.3,
                            F1 + (48 if stretch > 1 else 36) + pitch, 0.86 + 0.035 * j)
                # Answer down on F, then let the last two meetings and the
                # right riff's exposed tail go by without the reed.
                add("breath", t + 5 * cyc + 8, cyc - 10, F1 + 36, 0.84)
        else:
            beat(t, stop, snare=())                                    # the snare on every beat, growing
            beats = list(range(t, stop, 4))
            for j, q in enumerate(beats):
                drum("s", q, 0.45 + 0.55 * j / (len(beats) - 1))
        t += n
    # the measure: every guitar on the four sixteenths both riffs end with; the cell climbs the hook notes as chords
    MARKS.append(("the measure", t))
    drum("c", t, 0.95)
    for j, root in enumerate(HOOK):
        ROOTS.append((t + j * 32, root))
        for i in range(8):
            say(G, t + j * 32 + i * 4, ALL, low=True, root=root, chord=True)
            for side in "lr":
                bell(side, t + j * 32 + i * 4, root, float(BELLS.split(";")[2]) if BELLS else 0)
        if j:
            drum("c", t + j * 32, 0.7)
        if HEAD:
            head = [int(k) if k.isdigit() else 0 for k in A[:16] if k not in "-rc"] + [0, 12]
            add("lead", t + j * 32, 32, F1 + int(HEAD.split(";")[3]) + head[j], 0.9)
    beat(t, t + 256, cym="x", step=4, vel=0.5)
    t += 256
    # measured: the two riffs said together, in unison, the beat under them
    MARKS.append(("measured", t))
    fill(t)
    drum("c", t, 0.95)
    s = t
    for j, riff in enumerate((A, A, A, A, B, B, B, B)):
        # Once on each complete riff, hand its tail back to the bass soloist.
        # The last B reunites everybody; the low F at the end is unchanged.
        recall = A[-20:] if j == 3 else B[-12:] if j == 6 else []
        if BASS_BREAK and recall:
            split = len(riff) - len(recall)
            say(riff[:split], s, ALL, low=True)
            say(recall, s + split, (), low=True)
            pop_tail(s + split, s + len(riff), recall)
        else:
            say(riff, s, ALL, low=True)
        if FELT and 1 <= j <= 3:
            unfold_head(s, j)
        if KOTO and 1 <= j <= 3:
            the_rest_on_thirteen_strings(s, len(riff) - len(recall))
        bell("l", s)
        bell("r", s)
        if s > t:
            drum("c", s, 0.7)
        s += len(riff)
    if STICKS:
        measured_drums(t, s)
    else:
        beat(t, s, cym="x", step=4, vel=0.5)
        fill(s)
    MARKS.append(("one chord", s))
    for tr in ALL:
        add(tr, s, 32, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", s, 32, F1, 0.95)
    drum("k", s, 0.95)
    drum("c", s, 0.95)
    bell("l", s)
    bell("r", s)
    ROOTS.append((t, 0))
    stop = s + 32
    if AFTER:
        MARKS.append(('put back', stop))
        return afterword(stop)
    return stop


def measure_the_shell(doc):
    """Let the china state the five-beat measure, then give B's remaining three beats to wood."""
    left, right = PAIRS[1]  # 20 against 32 sixteenths, i.e. five beats inside eight
    a, b = len(left), len(right)
    assert a % len(G) == b % len(G) == 0
    pair_at = next(t for name,t in MARKS if name == f'{a} against {b}')
    start, stop = pair_at + b, pair_at + 4*b
    cym = next(t for t in doc['tracks'] if t['name']=='cym')
    tail = right[a:]
    assert tail == PAIRS[2][1] and tail[-len(G):] == G
    def in_answer(n):
        tick = round(n['at']*4)
        return n['pitch']=='x' and start <= tick < stop and (tick-start) % b >= a
    assert sum(map(in_answer,cym['notes'])) == 3*len(tail)//len(G)
    cym['notes'] = [n for n in cym['notes'] if not in_answer(n)]
    hits = []
    for s in range(start,stop,b):
        strokes = 0
        for i,k in enumerate(tail):
            beat = (s+a+i)/4
            if k.isdigit():
                # Five ridges in one sweep. Push, pull, push on B's three
                # rising notes, not on three quarter notes. The last is shorter.
                forward = (0,.075,.126,.163,.193)
                ridges = forward if strokes%2==0 else [forward[-1]-t for t in reversed(forward)]
                for dt,v in zip(ridges,(.68,.84,1,.84,.60)):
                    hits.append({'at':round(beat+dt*(.76 if strokes==2 else 1),4),
                                 'len':.057,'pitch':'ridge','vel':round(v*(.83,.9,1)[strokes],3)})
                strokes += 1
            elif k in ('o','c'):
                # The four-place common cell: knock, hold, two clipped knocks.
                hits.append({'at':beat,'len':.28 if k=='o' else .12,'pitch':'shell',
                             'vel':.94 if k=='o' else .80 if i==len(tail)-1 else .68})
    doc['patches']['cm-gourd'] = {
        'about':'One hollow gourd: a stick drawn over five ridges, then its handle knocking the shell.',
        'kit':{
            'ridge':{'pitch':'G5','gain':'-2dB','patch':{'synth':{
                'layers':[{'type':'noise','level':'-2dB'}, {'wave':'sine','level':'-14dB'},
                          {'wave':'sine','ratio':2.37,'level':'-7dB'}],
                'filters':['hp cutoff=780','lp cutoff=8500'],
                'amp':{'a':'0.5ms','d':'29ms','s':0,'r':'11ms'}}}},
            'shell':{'pitch':'G4','patch':{'synth':{
                'layers':[{'type':'additive','partials':[[1,.85],[2.37,.7],[4.12,.33]]},
                          {'type':'noise','level':{'value':'-54dB','mod':[{'src':'env.wood','amount':40}]}}],
                'env':{'wood':{'a':'0.3ms','d':'7ms','s':0}},
                'amp':{'a':'0.5ms','d':'90ms','s':0,'r':'16ms','curve':3}}}}}}
    doc['tracks'].append({'name':'gourd','patch':'cm-gourd','gain':SCRAPER,'pan':.18,'out':'drums','notes':hits})


def difference_key(doc):
    """Twenty less twelve leaves eight. On the key, five minus three leaves two."""
    long, short = PAIRS[2]
    a, b, unit = len(long), len(short), len(G)
    assert (a//unit, b//unit, a-b) == (5, 3, 8)
    start = next(t for name,t in MARKS if name == f'{a} against {b}')
    # The bass takes the shorter riff in the second half of this pair. Let its
    # first answer and the last exposed tail stay on both original guitars.
    lap_count = lcm(a,b)*REPS[2]//(2*a)
    assert lap_count == 6
    halfway = start + lap_count*a
    modes = [('five','three'), ('both','both'), ('both','product'), ('product','product')]
    remove, keys = set(), []
    for lap, hands in enumerate(modes, 1):
        at = halfway + lap*a + b
        pitched = [(i,k) for i,k in enumerate(long[b:]) if k.isdigit() or k=='o']
        for (i,k), mode in zip(pitched,hands,strict=True):
            dur = 1
            while b+i+dur < a and long[b+i+dur]=='-': dur += 1
            # Teach the two tones and their product on ONE unit (F2). Only
            # once the product is established does it take the player's B–F.
            unit_note = F1 + 12 + (int(k) if lap==len(modes) and k.isdigit() else 0)
            remove.add(at+i)
            keys.append({'at':(at+i)/4, 'len':dur*.98/4, 'pitch':nm(unit_note), 'vel':.91,
                         'expr':{'three':int(mode in ('three','both')), 'five':int(mode!='three'),
                                 'product':int(mode=='product')},
                         # Same sine RMS for one tone, two tones, or their product.
                         'gain':{'three':'0dB','five':'0dB','both':'-3dB','product':'3dB'}[mode]})
    double = next(t for t in doc['tracks'] if t['name']=='dl')
    assert len(remove)==8 and sum(round(n['at']*4) in remove for n in double['notes'])==8
    double['notes'] = [n for n in double['notes'] if round(n['at']*4) not in remove]
    switch = lambda src: {'value':'-96dB','mod':[{'src':'expr.'+src,'amount':96}]}
    doc['patches']['cm-sidebands'] = {
        'about':'One struck electronic key. Two oscillators at the fifth and third harmonics of the written note; the ring circuit makes their sum and difference.',
        'synth': {'layers':[
            {'name':'reference','wave':'sine','ratio':b/unit,'audible':False},
            {'wave':'sine','ratio':b/unit,'level':switch('three')},
            {'wave':'sine','ratio':a/unit,'level':switch('five'),
             'ringmod':{'from':'reference','mix':'expr.product'}},
            {'type':'noise','level':{'value':'-76dB','mod':[{'src':'env.contact','amount':48}]}}],
            'env':{'contact':{'a':'0.2ms','d':'5ms','s':0}},
            'amp':{'a':'2ms','d':'340ms','s':.22,'r':'45ms','curve':2}},
        'play':{'gate':1,'vel_sens':.6}}
    doc['tracks'].append({'name':'residue','patch':'cm-sidebands','gain':SIDEBANDS,
                          'pan':-.48,'out':'gtrs','notes':keys})


def meet_the_bow():
    """The picked string climbs by B's own frets to the E-bow's last open F."""
    left, right = PAIRS[0]
    a, b = len(left), len(right)
    end = INTRO + lcm(a, b) * REPS[0]
    stop = end - (a - b)  # beyond here only A's remainder is heard
    frets = (int(k) if k.isdigit() else 0 for k in right if k.isdigit() or k == 'o')
    up = list(dict.fromkeys(frets)) + [12]
    assert up == [0, 1, 3, 6, 7, 12]
    first = end - len(up) * b
    figure = right[:b // 4]
    strokes = [i for i, k in enumerate(figure) if k not in 'r-']
    assert strokes == [0, 2, 3, 5, 6]
    # First tie the back of each pair into the preceding stroke, then the front.
    # Five picks, four, three, two, one, all on the original grid.
    takes = [strokes, strokes[:-1], [0, 2, 5], [0, 5], [0]]
    for j, semi in enumerate(up):
        at = first + j * b
        until = min(stop, at + 2 * len(figure))
        T['dr'] = [n for n in T['dr'] if not at <= round(n['at'] * 4) < until]
        if j == len(up) - 1:
            # Both strings reach F2. Release the pick a beat before the bow;
            # A's last C–B can lead into the exposed twenty on the left.
            add('dr', at, until - at - len(G) - .25, F1 + semi, .96)
            T['gr'] = [n for n in T['gr'] if not until - len(G) <= round(n['at'] * 4) < until]
            continue
        # One player takes the opening figure, the other replies under the ringing note.
        T['gr'] = [n for n in T['gr'] if not at < round(n['at'] * 4) < at + len(figure)]
        kept = takes[j]
        for i, nxt in zip(kept, kept[1:] + [len(figure)]):
            dur = max(p for p in strokes if i <= p < nxt) + 1 - i
            if len(kept) == 1:
                dur = 2 * len(figure) - .5  # carry C through the reply without another pick
            add('dr', at + i, dur, F1 + semi, .96 if i == 0 else .88, **({'pm': 1} if i and dur == 1 else {}))
        if len(kept) > 1:
            add('dr', at + len(figure), len(figure) - .5, F1 + semi, .96)


def ring_the_lifted():
    """The left guitar holds what the bass pops, in the half of the break no card covers."""
    up, who = RING.split(';')
    left, right = PAIRS[1]
    marks = dict(MARKS)
    t = marks[f'{len(left)} against {len(right)}']
    n = lcm(len(left), len(right)) * REPS[1]
    start, stop = t + n // 2, t + n - (len(right) - len(left))
    half = start + 4 * len(left)                                     # the first four statements are the card's excerpt
    assert half + 3 * len(left) < stop
    assert not [x for x in T[who] if half <= round(x['at'] * 4) < stop]
    lifted = sorted((round(x['at'] * 4), x['pitch']) for x in T['bass']
                    if half <= round(x['at'] * 4) < stop and x['pitch'] != nm(F1))
    names = {nm(m): m for m in range(F1, F1 + 40)}
    for k, base in enumerate(range(half, stop, len(left))):
        pops = [(p, names[pitch]) for p, pitch in lifted if base <= p < base + len(left)]
        cell = min(base + len(left) - len(G), stop)                  # the shared beat stays the bass's and the foot's
        keep = pops[-(k + 1):] if base + len(left) <= stop else pops    # one more each time; the cut statement has what it has
        for (p, midi), end in zip(pops, [q for q, _ in pops[1:]] + [cell]):
            if (p, midi) in keep:
                add(who, p, end - p - 0.3, midi + int(up), 0.9)


def each_riff_has_its_note():
    """From the second meeting of 20 against 32 to the bass break in 20 against 12: a bowed string a side, the
    riff's own note for the riff's own length, every time it comes round."""
    top, vel = float(OWN.split(';')[1]), float(OWN.split(';')[3])
    flat = dict(zip((32, 20, 12), (float(c) / 100 for c in OWN.split(';')[2].split(':'))))
    at = dict(MARKS)
    t1, t2 = at['20 against 32'], at['20 against 12']
    note = lambda length: f'm{top - 12 * log2(length / 4) - flat[length]:.4f}'
    own = lambda length: top - 12 * log2(length / 4)
    assert t2 - t1 == 320 and all(abs(own(x) - y) < 0.001 for x, y in ((20, 68.1564), (32, 60.0196), (12, 77.0)))   # A flat 4, C4, F5
    spans = [(t1 + 160, t2 - 12, 20, 32),          # the second cycle, up to the tail that is heard alone
             (t2, t2 + 120, 20, 12)]               # the first half of the next pair, up to the bass's break
    for start, stop, left, right in spans:
        for tr, length in (('own-l', left), ('own-r', right)):
            for q in range(start, stop, length):
                add(tr, q, min(length, stop - q), note(length), vel)


def the_foot_crosses_over():
    """The last meetings of 8 against 12: the kick with the right riff, the bass still with the left."""
    left, right = PAIRS[3]
    t = dict(MARKS)[f'{len(left)} against {len(right)}']
    cyc = lcm(len(left), len(right))
    end = t + cyc * REPS[3]
    start = end - int(CROSS) * cyc + 4
    rights = {i for i, token in enumerate(right) if token not in 'r-'}
    lefts = {i for i, token in enumerate(left) if token not in 'r-'}
    place = lambda n: round(n['at'] * 4)
    inside = [n for n in T['kick'] if start <= place(n) < end]
    # every stroke of the right riff in the passage already has the kick: nothing is added
    assert {place(n) for n in inside} >= {q for q in range(start, end) if (q - t) % len(right) in rights}
    assert all((place(n) - t) % len(left) in lefts for n in inside)
    T['kick'] = [n for n in T['kick'] if not (start <= place(n) < end and (place(n) - t) % len(right) not in rights)]
    assert len(inside) - len([n for n in T['kick'] if start <= place(n) < end]) == 6 * int(CROSS) - 1


def song():
    total = compose()
    if CONVERGE:
        meet_the_bow()
    if RING and '1' not in FULL.split(';')[0].split(','):   # v20: no first break, so nothing is lifted there to ring
        ring_the_lifted()
    if CROSS:
        the_foot_crosses_over()
    if OWN:
        each_riff_has_its_note()
    assert total % 16 == 0 and all(m[1] % 16 == 0 for m in MARKS)
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"            # each riff is two takes: a second through another amp, microphone and cone
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    tracks = [
        {"name": "gl", "patch": main.format(60), "gain": os.environ.get("C10T8_MAIN", "0.7dB"), "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(61), "gain": os.environ.get("C10T8_MAIN", "0.7dB"), "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(62), "gain": os.environ.get("C10T8_DBL", "-2.5dB"), "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(63), "gain": os.environ.get("C10T8_DBL", "-2.5dB"), "pan": 0.75, "out": "gtrs", **mids},
        {"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        *([{"name": "bell-" + side, "patch": "cm-bell", "gain": f"{float(BELLS.split(';')[0]) + (float(BELLS.split(';')[3]) if side == 'l' else 0):g}dB", "pan": pan}
           for side, pan in (("l", -0.6), ("r", 0.6))] if BELLS else []),
        *([{"name": "lead", "patch": HEAD.split(";")[0], "gain": HEAD.split(";")[1], "pan": 0, "sends": {"hall": HEAD.split(";")[2]}}] if HEAD else []),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
    ]
    if FELT:
        tracks.append({'name':'felt','patch':'piano-muted fx.0.mix=0.06','gain':FELT,'pan':-.10})
    if BREATH:
        timbre, gain = BREATH.split(";")
        tracks.append({"name": "breath", "patch": timbre, "gain": gain, "pan": 0.12})
        if FULL and float(FULL.split(';')[1]):
            # v20: quieter where it shadows the right guitar (to the end of 8 against 12); its lines in the afterword keep their level
            upto = dict(MARKS)['8 against 4'] / 4
            tracks[-1]['fx'] = [{'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.quieter', 'amount': 1}]}}]
            tracks[-1]['auto'] = {'quieter': {'points': [['0b', float(FULL.split(';')[1])], [f'{upto:g}b', float(FULL.split(';')[1])], [f'{upto + 0.01:g}b', 0]], 'curve': 0}}
    if KOTO:
        # Opposite the piano (-0.10), a little wider. Less of the patch's hall: the guitars' room is short.
        tracks.append({'name': 'koto', 'patch': 'koto fx.0.mix=0.08', 'gain': KOTO.split(';')[1], 'pan': .28})
    if SPAN:
        # Close the tone control in the gap between spans. The selected family
        # should descend; a high multiple of the second node can otherwise mask it.
        def holds(values):
            points = [['0b',values[0]]]
            for i,note in enumerate(T['span'][1:]):
                points += [[f"{note['at']-1:g}b",values[i]], [f"{note['at']:g}b",values[i+1]]]
            return {'points':points,'curve':0}
        pole = {'value':90,'mod':[{'src':'auto.tone','amount':1}]}
        tracks.append({'name':'span','patch':'ebow synth.layers.0.pick=0.11 synth.layers.0.pickup=0.13 fx.1.gain=0.20 synth.amp.a=135ms synth.amp.r=42ms fx.3.mix=0 fx.4.mix=0',
                       'gain':{'value':SPAN,'mod':[{'src':'auto.trim','amount':1}]},'pan':-.69,
                       'auto':{'tone':holds([log2(h) for h in (4,3,2,1)]),
                               'trim':holds([0,0,12,5])},
                       'fx':[{'type':'eq','bands':[{'kind':'lp','cutoff':pole,'q':1.05}]}]})
    if OWN:
        # the e-bow of v7, dry, a little closer to the bridge; one a side, where each riff's bell is
        bowed = ('ebow synth.layers.0.pick=0.11 synth.layers.0.pickup=0.13 fx.1.gain=0.20 synth.amp.a=135ms synth.amp.r=42ms fx.3.mix=0 fx.4.mix=0'
                 ' synth.pitch.mod.0.amount=0 synth.pitch.mod.1.amount=0')
        tracks += [{'name': 'own-l', 'patch': bowed, 'gain': OWN.split(';')[0], 'pan': -.6},
                   {'name': 'own-r', 'patch': bowed, 'gain': OWN.split(';')[0], 'pan': .6}]
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", 0]], 0
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p / 4 - 0.02:g}b", prev], [f"{p / 4:g}b", r]]
            prev = r
    doc = {
        "about": ("chirpers X (Common Time), track 8 by chirper-zero: Common Measure. Two riffs of different lengths, 52 sixteenths on the "
                  "left guitar and 32 on the right, and Euclid's way of finding what measures both: take the less from the greater. "
                  "Each section the longer riff is cut down to what was left over, its own tail: 52 against 32, 20 against 32, 20 "
                  "against 12, 8 against 12, 8 against 4. Four goes into eight: the measure is one beat, the four sixteenths both "
                  "riffs end with, and then the two riffs are played whole, together. The fast song: 160. v1 is the skeleton."),
        # The quiet afterword adds 12 seconds to the loudness measurement.
        # Don't turn the existing 3:12 up to compensate: the four comparison
        # clips on that stretch have already been put in front of Harry.
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(OWN.split(';')[4]) if OWN else float(FULL.split(';')[2]) if FULL else -10.17 if AFTER else -10,
        "seed": 1, "tail": "5s", "length": f"{total // 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    **({"cm-bell": {
                        "about": ("Common Measure's bell (chirper-zero, 17 Nov): the library's agogo bell (afro-perc's `ah`: three partials at 1, "
                                  "2.4 and 3.9 and a 4 ms click) as a patch that takes a pitch, so the two bells can sit on the song's fifth "
                                  "and root and follow the chords."),
                        "synth": {"amp": {"a": "0.2ms", "curve": 3, "d": "240ms", "r": "30ms", "s": 0},
                                  "env": {"h": {"a": "0.2ms", "d": "4ms", "s": 0}},
                                  "layers": [{"type": "additive", "damp": 0.3, "partials": [[1, 1], [2.4, 0.4], [3.9, 0.15]]},
                                             {"type": "noise", "level": {"value": "-60dB", "mod": [{"src": "env.h", "amount": 40}]}}]}}} if BELLS else {})},
        "buses": {
            **({"hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]}} if HEAD else {}),
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
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}],
                    "auto": {"key": {"points": pts, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T8_MASTER", "2.7dB")}]},
        "tracks": tracks,
    }
    if SCRAPER:
        measure_the_shell(doc)
    if SIDEBANDS:
        difference_key(doc)
    if TIMELINE:
        the_timeline(doc)
    if SHAKER:
        the_shekere(doc)
    if PASS:
        the_answer_passes_by(doc)
    return doc


def the_answer_passes_by(doc):
    """Where the two riffs end one beat apart, the band stops and the two endings are heard: one side, then the other."""
    which, target = PASS.split(';')
    left, right = PAIRS[0]
    start = dict(MARKS)[f'{len(left)} against {len(right)}']
    cyc = lcm(len(left), len(right))
    # every place in the cycle where a statement of one riff ends exactly one cell before a statement of the other
    near = sorted((start + min(i * len(left), j * len(right)), 'l' if i * len(left) < j * len(right) else 'r')
                  for i in range(1, cyc // len(left)) for j in range(1, cyc // len(right))
                  if abs(i * len(left) - j * len(right)) == len(G))
    assert near == [(start + 156, 'l'), (start + 256, 'r')] and left[-len(G):] == right[-len(G):] == G
    side = {'l': ('gl', 'dl', 'wl'), 'r': ('gr', 'dr', 'wr')}
    low = ('bass', 'kick')                      # they go with the shorter riff, the right; for the one beat they rest
    hands = ('snare', 'hat', 'toms', 'cym', 'shaker')
    track = {t['name']: t for t in doc['tracks']}
    place = lambda n: round(n['at'] * 4)
    gone = 0
    for k, (end, first) in enumerate(near):
        if str(k + 1) not in which.split(','):
            continue
        a = end - len(G)
        for name in side['r' if first == 'l' else 'l'] + low + hands:   # the first beat: the two guitars whose riff is ending, alone
            t = track.get(name)
            if not t or 'notes' not in t:
                continue
            gone += sum(1 for n in t['notes'] if a <= place(n) < end)
            t['notes'] = [n for n in t['notes'] if not a <= place(n) < end]
            for n in t['notes']:                                     # what was still ringing stops where the break begins
                if name not in hands + ('kick',) and place(n) < a < n['at'] * 4 + n['len'] * 4:
                    n['len'] = round((a - place(n)) / 4 * 0.98, 4)
        for name in hands:                                           # the second beat: the other side answers; still no hands
            t = track.get(name)
            if t and 'notes' in t:
                gone += sum(1 for n in t['notes'] if end <= place(n) < end + len(G))
                t['notes'] = [n for n in t['notes'] if not end <= place(n) < end + len(G)]
        # what is heard in the first beat is the cell and nothing else: an open root and two muted strokes
        for name in side[first][:2]:
            cell = [(place(n) - a, n['pitch']) for n in track[name]['notes'] if a <= place(n) < end]
            assert cell == [(0, nm(F1)), (2, nm(F1)), (3, nm(F1))], (name, cell)
    if target:
        doc['loudness'] = float(target)
    return gone


def the_timeline(doc):
    """Eight in thirteen on claves, by the engine's own Euclid; then five in eight."""
    pitch, gain, pan, first = TIMELINE.split(';')
    left, right = PAIRS[0]
    a, b = len(left) // len(G), len(right) // len(G)              # thirteen beats and eight
    nxt = len(PAIRS[1][0]) // len(G)                              # five: what is left of A after the first cut
    start = dict(MARKS)[f'{len(left)} against {len(right)}']
    whole = lcm(len(left), len(right)) // len(left) - 1           # the last statement is cut after its head
    assert (a, b, nxt) == (13, 8, 5) and len(left) - len(right) == len(PAIRS[1][0]) and 0 <= int(first) < whole
    doc['patches']['cm-clave'] = {
        'about': ("Common Measure's claves (chirper-two, 18 Nov): a rosewood stick as a free bar on the modal layer (the glock "
                  "set's 1 : 2.76 : 5.40), struck hard and gone in a tenth of a second. A tock, not a bell: the second mode sits "
                  "10 dB under the first and the third 21 under. Takes a pitch (C7, 2.1 kHz, is a clave's)."),
        'synth': {'amp': {'a': '0.2ms', 'd': '300ms', 's': 0, 'r': '40ms'},
                  'layers': [{'type': 'modal', 'modes': 'glock', 'decay': '180ms', 'damp': 0.25, 'bright': 0.9, 'strike': 0.5, 'tilt': 0}]},
        'play': {'vel_sens': 0.5}}
    score = ' '.join([f'{pitch}({b},{a})/4@100'] * (whole - int(first)) + [f'{pitch}({nxt},{b})/4@100'])
    doc['tracks'].append({'name': 'clave', 'patch': 'cm-clave', 'gain': gain, 'pan': float(pan),
                          'at': f'{(start + int(first) * len(left)) // 4}b', 'score': score})


def the_shekere(doc):
    """The hat's strokes under the claves, on a shekere. No stroke is added or moved."""
    gain, pan, top, oh = SHAKER.split(';')
    left, right = PAIRS[0]
    b0 = float(next(t for t in doc['tracks'] if t['name'] == 'clave')['at'].rstrip('b'))
    b1 = (dict(MARKS)[f'{len(left)} against {len(right)}'] + lcm(len(left), len(right)) - len(left) + len(right)) / 4   # where the band stops
    hat = next(t for t in doc['tracks'] if t['name'] == 'hat')
    moved = [n for n in hat['notes'] if b0 <= n['at'] < b1]
    assert moved and all(n['pitch'] == 'h' for n in moved)
    hat['notes'] = [n for n in hat['notes'] if not b0 <= n['at'] < b1]
    doc['patches']['cm-shekere'] = {
        'about': ("Common Measure's shekere (chirper-two, 18 Nov): the library's beaded gourd (afro-perc's `sk`: a soft-edged burst of "
                  "noise between 3 kHz and its top) with the top opened, so it can stand where a closed hi-hat stood."),
        'kit': {'sk': {'gain': '-6dB', 'patch': {'synth': {
            'layers': [{'type': 'noise'}], 'filters': ['hp cutoff=3k', f'lp cutoff={top}'],
            'amp': {'a': '6ms', 'd': '90ms', 's': 0, 'r': '30ms'}}}}},
        'play': {'humanize': {'time': '5ms', 'vel': 0.08}, 'vel_sens': 0.6}}
    doc['tracks'].append({'name': 'shaker', 'patch': 'cm-shekere', 'gain': gain, 'pan': float(pan), 'out': 'drums', 'sends': {'oh': oh},
                          'notes': [{**n, 'pitch': 'sk'} for n in moved]})


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
    if os.environ.get("C10T8_SHOW"):
        end = compose()
        sec = 15 / BPM
        for (name, s0), (_, s1) in zip(MARKS, MARKS[1:] + [("", end)]):
            print(f"{name:16s} bars {s0 // 16 + 1:3d}-{s1 // 16 + 1:3d}  {int(s0 * sec) // 60}:{s0 * sec % 60:04.1f}-{int(s1 * sec) // 60}:{s1 * sec % 60:04.1f}")
    else:
        open(OUT, "w").write(dump(song()))
