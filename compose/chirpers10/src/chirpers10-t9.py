#!/usr/bin/env python3
"""chirpers10-t9 "In the Time Of" (chirper-zero): one riff of seven notes, and one beat that never changes.

"Five in the time of four" is how a musician says a quintuplet. This piece is that phrase taken as a form. The beat
is common time at 84 from the first bar to the last, and the kit keeps it plainly. The riff is seven notes long (a
low open note, two muted strokes, a hook note, a stroke, a hook note, a stroke), and the band deals it out at a
different number of notes to the beat in each section:

  one to the beat      bars 0-7     the riff is a slow tune, seven beats long: two guitars and a hat
  two                  bars 7-14    the bass and the kick come in
  three                bars 14-21   triplets: the snare, the china, each guitar doubled
  four                 bars 21-28   sixteenths; v2: the two hook notes pass between baritone and clavinet
  five                 bars 28-35   quintuplets: two guitars again; the bass holds through their muted strokes
  six                  bars 35-42   sextuplets: one beat of the kit alone before the lock
  seven                bars 42-56   septuplets: THE SEVEN STROKES ARE NOW EXACTLY ONE BEAT LONG. It locks:
                                    every beat begins with its open note. Six guitars; then a minor third up
  one again            bars 56-63   the riff at one to the beat once more, every note a chord
  one chord            bars 63-65

Before seven, a cell START and a quarter note coincide once every seven beats: beats one, four, three, two in
successive bars of their meeting. A seven-bar rung fits both the cell and the four-beat bar. The shape repeats
every seven strokes; the two answers (A flat/B and G flat/C in F) alternate, so the pitch phrase is twice as long.
The hat or china stays on the quarter. At seven, the kick and bass land on the head of every cell instead of
following all its strokes. What was a slow tune should now be a fast figure over a very plain walk.

v1 is the SKELETON (Harry, 18 Nov about 03:18: "for now youll build ahead ina enew song"): the whole shape standing,
bare.
"""
import json
import os

OUT = os.environ.get("C10T9_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t9.yaml"))
BPM = 84
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
# o an open low root, c a muted stroke, a number a hook note (semitones over the root). Two forms, taken in turn
CELLS = ["o c c 3 c 6 c".split(), "o c c 1 c 7 c".split()]
N = len(CELLS[0])
RUNG = 4 * N                              # beats: seven bars, four times round
PAWL = os.environ.get("C10T9_PAWL", "-9dB")  # off = the same skeleton without the cell marker
# v2 palette: a picked string and a keyed string take the two answers out of the
# four unison guitars for one rung. Gains in that order. Empty restores v1.
HANDS = os.environ.get("C10T9_HANDS", "-11.5dB;-4.5dB")
# v3: on the repeat at the top, the right guitar lets each hook pitch sound across
# the following mute. At the return that line belongs to a pair; the last cell
# strips back to the original two parts before the six-guitar F. Empty = v2.
RING = os.environ.get("C10T9_RING", "1")
# w3: the foot keeps four; the sticks take every fourth triplet. Gain of the
# ride-bell track; gain of the pedal-chick piece in this song's kit. Empty = v3.
CROSS = os.environ.get("C10T9_CROSS", "0.5dB;-8dB")
# v5, THE BASS IS LAST TO TURN: one seven-beat bass phrase each side of the
# two-to-three boundary. The guitars change speed but the bassist repeats the
# same six attacks at the old rate. Empty restores v4.
BASS_TURN = os.environ.get("C10T9_BASS_TURN", "1")
# v6: give each position inside the beat a pitch for the last two cycles
# of fives and first two of sixes. Empty restores v5. Keep the older v4 switch.
HEAD_TUNE = os.environ.get('C10T9_HEAD_TUNE', '1' if BASS_TURN else '')
# v7: after the lock modulates, count 1..7 without increasing the speed.
# All six picks lift together; bass and kick still walk. Empty restores v6.
CUT = os.environ.get('C10T9_CUT', '1' if HEAD_TUNE else '')
# v8: inside the fours the opening returns at one stroke per beat. Between
# the slow and fast guitar pairs the bass brings back its two-to-a-beat answer.
# Empty restores v7; preserve the older cascade of rollback switches.
SLOW_HAND = os.environ.get('C10T9_SLOW_HAND', '1') if CUT and HANDS and BASS_TURN else ''
# v9: stick on riff accents, foot on untouched quarters. Open-cymbal piece
# gain. Empty restores v8; disabling SLOW_HAND still gives v7.
CLUTCH = os.environ.get('C10T9_CLUTCH', '-16dB' if SLOW_HAND else '')
# v10: C under the last sixes, F–E above it. The lock supplies the last F.
# Empty restores v9; turning off the clutch still defaults to v8.
CADENCE = os.environ.get('C10T9_CADENCE', '1' if CLUTCH else '')
# v11: inside the F lock, fret the two coming answers on the high strings of
# the existing wall pair. Empty = v10; the published older switches still work.
FORETELL = os.environ.get('C10T9_FORETELL', '1' if CADENCE else '')
# v12: the last seven beats of the lock play 7, 6, 5, 4, 3, 2 and 1 strokes:
# 28 strokes, four whole cells, the head due on the slow chords. "plain"
# keeps the lock's single notes; any other value thickens them on the way down.
# Empty = v11; the published older switches still work.
GEAR = os.environ.get('C10T9_GEAR_DOWN', '1' if FORETELL else '')
# v13 palette: only at one stroke to the beat does a note last long enough to
# be HELD. Each speed on the way up had a guest of its own (open hat, ride
# bell, baritone and clavinet, the tap). The return to one gets a pipe organ:
# no other song on the record has one. It holds the riff's three pitches for
# 3 + 2 + 2 beats over the first two cells of the slow chords: principals and
# mixture, no reed. The opening stays two guitars and a hat.
# Note gain. Empty restores v12.
WIND = os.environ.get('C10T9_WIND', '-6dB' if GEAR else '')
# (With the pipes the loudness target is PIPE_LUFS, not -10: they add a little
# to the song, and every bar without them should keep v12's mastering gain.)
PIPE_LUFS = -9.98
# v14, section w4 (1:20-1:30): FIVE, COUNTED BY HAND. "Five in the time of four" is how a musician says a
# quintuplet; in North India it is a tala. For the first two turns of the fives a tabla plays jhaptal, the ten-beat
# cycle, at five strokes to the beat: dhin na | dhin dhin na, tin na | dhin dhin na. Its two-and-three fall inside
# every beat of the kit, and its ten strokes last two beats: the bass drum of the pair sounds on one and three and
# is left out on two and four, where the snare is. So three things now turn at once: the kit in four, the tabla
# in ten, the riff in seven. The riff's head (and its tap) lands on a different bol each time: first, third,
# fifth, second, fourth. In the last two beats the tabla plays a tihai, the thrice-said cadence (te re dha, three
# times, a stroke's rest between), whose last dha is the beat where the tap begins its tune: the five places in
# the beat have been counted, and the tap now gives each a pitch (v6). The kit does not change.
# Track gain ; the loudness target (every bar without the tabla keeps v13's mastering gain) ; how hard the hands
# play (a factor on every stroke; harder is brighter). Empty restores v13.
KHANDA = os.environ.get('C10T9_KHANDA', '-9dB;-9.96;1' if WIND else '')
# v15, whole song: THE SLOW TUNE UNDER THE FAST ONE. The song opens with the
# riff at one note to the beat and arrives, two minutes later, at seven to the
# beat, where the bass and the kick only walked: a low F on every beat for 32
# beats. The walk is now the OPENING. Under the lock on F the bass plays the
# riff at one note to the beat again, as the two guitars did at 0:00: F F F
# A-flat F B F, then F F F G-flat F C F, while six guitars play the same seven
# notes inside every one of those beats. Seven in the time of one, over one.
# It still strikes every beat with the kick; only nine of the 32 notes leave
# F. A slow cell is seven beats and the lock on F is 32, so the fifth cell
# gets as far as its first answer, A flat, on the last beat before the band
# moves up to A flat: the note the riff has always answered with is the key
# the song goes to, and the bass is there a beat early. (At 0:35 the bass is
# the last to turn; here it turns first.) The bass's eq follows each of those
# nine notes, as it follows the song's grounds. Empty restores v14.
AUGMENT = os.environ.get('C10T9_AUGMENT', '1' if KHANDA else '')
# v16 palette: SIX STRINGS. Every speed on the way up has a guest of its own
# but six, which shared the tap with five. Six strokes to the beat is one
# pass across a six-string guitar, a string to a stroke. A nylon-string guitar
# (the library's nylon; no other song on the record has one) is tuned to the
# six notes the tap gives the six places in the beat (v6): F, G flat, A flat,
# B, C, F. The tap names one string per cell, the next one up each time
# (seven strokes move the head on by one place). A string is silent until it
# is named and is plucked in its place in every beat after that: through the
# first seven beats the pass grows from one string to six, through the second
# seven it is whole, and the tap goes round again an octave above, pointing at
# each string in turn. Where the riff leaves the tap's high F alone across the
# footfall (v6), so does the guitar. It stops where the cadence starts.
# Track gain ; semitones from the riff's low F up to the lowest string ; the
# loudness target (every bar without it keeps v15's mastering gain).
# Empty restores v15.
# (First bench at -8 dB: 8.5 to 9.8 dB under everything else, K-weighted, with
# the tap at 14.1 under, and +2.0 dB on the passage at 250-500 Hz. So -11.
# An octave up, in unison with the tap, it took the tap's place instead.
# With the target left at -9.96 the rest of the song came out 0.008 dB lower.)
SIX = os.environ.get('C10T9_SIX', '-11dB;24;-9.95' if all((AUGMENT, PAWL, HEAD_TUNE, CROSS, RING)) else '')
PLACES = (0, 1, 3, 6, 7, 12)  # F, Gb, Ab, B, C, upper F: one for each place in a beat of six
# v17, section w6 (the lock on F, 2:05-2:22.9): SEVEN, HEARD AS THREE AND TWO AND TWO. "What was a slow tune
# should now be a fast figure over a very plain walk" (above). Measured, it was a wall over a walk: all six guitars
# played all seven strokes, and folded on the beat their level was the same from stroke to stroke (the open note
# and the two answers 0.4 dB over the four muted strokes; 1.1 dB in the whole mix). A saturated amp holds a muted
# stroke as loud as an open one, so six of them leave no figure, only its pitches. Now the riff is orchestrated as
# it is written. The lock still ARRIVES as the wall: six guitars on every stroke for the bass's first slow cell
# (seven beats). From the second cell the main pair alone keeps all seven strokes; the inner pair and the wall
# pair strike only the open note and the two answers, each one stroke long, and REST on the four muted strokes:
# long short short, long short, long short, in every beat, until the band goes up to A flat, where all six are on
# every stroke again. By subtraction: no stroke is added or moved; the main pair, the bass's slow tune (v15), the
# kit and the answers the wall pair frets ahead (v11) are as they were.
# Beats of full wall first ; the guitars that rest on the muted strokes ; how long they write their struck notes,
# in strokes (0.5 sounds one stroke long: these rigs ring half a stroke past the note) ; the loudness target (the
# lock is a little quieter; every other bar keeps v16's mastering gain: at -9.95 the rest of the song came out
# 0.11 dB louder, at -10.06 still 0.002). Empty restores v16.
SHAPE = os.environ.get('C10T9_SHAPE', '7;dl,dr,wl,wr;0.5;-10.062' if SIX and FORETELL else '')
# v18, section w6 (the lock on F, 2:10-2:22.9): SEVEN, COUNTED BY HAND. The tabla counted the fives in jhaptal (v14)
# and was not heard again. There is a tala of seven, rupak: tin tin na, dhin na, dhin na. It is three and two and
# two, which is what v17 made the lock; it is the one common tala that BEGINS on its empty beat, no bass drum on
# the one, and the riff begins on its open string; and its two dhins, the strokes where the bass drum sounds, are
# the fourth and sixth of seven, the riff's two answers. So at seven to the beat one turn of rupak is one beat
# long and is the riff, stroke for stroke (chirper-three saw it at r17). The tabla comes back for the last two and
# a half slow cells of the lock: first the right hand alone, tin tin na, tin na, tin na (2:10); then, at the next
# slow cell, the bass drum on the two answers (2:15); and in the last two beats a tihai, te re dha three times,
# three strokes' rest between, whose third dha is the band's first stroke in A flat (2:22.9), as the tihai at 1:30
# landed where the tap began its tune. No other part changes: the lock goes wall, figure, figure counted by hand,
# figure with the low drum, A flat.
# Beats into the lock where the tabla comes in ; beats after that where its bass drum joins ; the gain of its
# track here ; the loudness target (every bar without it keeps v17's mastering gain). Empty restores v17.
# (The same drums on a track of their own, `rupak`, at the fives' own fader. There they stand 8.0 to 9.1 dB under
# everything else, K-weighted, where the fives' stand 8.6; they hold half of 250 Hz-1 kHz (their treble drum is on
# F4, struck ten times a second) and the passage reads 2.3 to 3.2 dB over the eleven records in those two bands,
# where v17 had left it level and the fives read 2.8 and 1.2. Benched at -12 dB: 11.3 to 11.9 under the rest, 1.2 to
# 2.4 over the records, and the scorer stopped hearing the drums come back (89.863/86.324 against 91.068/91.746 on
# seeds 0/11). With '-12dB' the target is -10.055. A gain written on each note moved them only 0.4 dB for a dB.)
RUPAK = os.environ.get('C10T9_RUPAK', '14;7;-9dB;-10.047' if SHAPE and KHANDA else '')
# v19, section w7 (the gears, 2:35.0-2:40.0): EVERY TIME ONCE MORE. The gears play every speed of the song for one
# beat each, fastest first: seven strokes, six, five, four, three, two, one. Until now all six guitars played all
# of it, so it was the lock slowing down. On the way up each speed had its own band and its own guest, and none of
# them came back (the tabla alone, at seven, v18). Now each beat of the gears is that speed AS IT WAS, band and
# guest, the song run backwards in five seconds (chirper-zero's idea, his note of 18 Nov 22:06):
#   seven   six guitars, the wall                                   (as it was)
#   six     the main pair, and the nylon guitar's pass across its six strings, a string to a stroke
#   five    the main pair, and the tabla: dhin na dhin dhin na, half a turn of jhaptal
#   four    four guitars, and the answer that falls in that beat taken from them by the baritone and the clavinet
#           (TOGETHER, for the only time: on the way up they took the answers in turn)
#   three   four guitars, and the bell of the ride on all three strokes over the hat's foot
#   two     the main pair, the hat's foot and then the hat left open, as at 0:22
#   one     the main pair's one muted stroke and a closed hat, as the song began: no snare, no cymbal
# and then the slow chords with the pipes, as before. By subtraction for the band (no guitar stroke is added or
# moved; the bass and the foot are as they were) and sixteen strokes for the guests, every one of them the notes
# its player had on the way up, moved to A flat, the gears' ground. The nylon and the tabla are second instruments
# on tracks of their own (`six-ab`, `tabla-ab`): a guitar whose six open strings are the six places in A flat, and
# a pair of drums a minor third up (a tabla player retunes with a hammer, not in a beat).
# The A flat nylon's track gain ; the A flat tabla's ; the gain on the baritone's, the clavinet's and the open
# hat's one note each ; the loudness target (the gears are quieter by the guitars that rest; every other bar
# keeps v18's mastering gain). Empty restores v18.
# (At their faders from the way up, raw seed 0, each guest stood 9.2 to 10.2 dB under the rest of its beat, as it
# did there; but there it had twenty seconds to be noticed and here it has one beat. A gain written on a nylon,
# baritone or clavinet note moves it 0.3 dB for a dB, as chirper-one found of the tabla: hence the two tracks.)
REPRISE = os.environ.get('C10T9_REPRISE', '-7dB;-6dB;3dB;-10.085' if RUPAK and GEAR and SIX and KHANDA and HANDS and CROSS and CLUTCH else '')
# v20: SIX AS ONE (chirper-zero, 19 Nov). Harry on the card it-return-duet, "Does dropping to two guitars make the
# last chord land better?": "Prefer six throughout". At v3 (RING) the last cell of the return stripped back to the
# two guitars that began the song. Now the other four stay and all six play the riff, every stroke a chord: the
# one cell of the return where the six do the same thing. Mastered, its strokes read -7.9 to -8.8 LUFS momentary
# (v19 -10.1 to -11.2; the F chord it lands on -8.0). on ; the loudness target (every other bar keeps v19's
# mastering gain: level within 0.003 dB, both seeds). Empty restores v19.
GATHER = os.environ.get('C10T9_GATHER', '1;-10.029' if REPRISE and RING else '')
# v21: THE WALL PAIR GETS A SPEAKER (chirper-zero, 19 Nov, instrument round: wl and wr, 2:00 to the end; no note
# changes). The third pair was on the album's old wall rig: captured cabinet files, the patch's eq taking 10 dB off
# the top from 5 kHz, a 3 dB trim at 380 Hz. Alone against a record's guitar alone (tools/cabspec.py, 2:00-2:10):
# +5.9 at 630 Hz, +6.9 at 800, -12.3 at 8 kHz, -18.2 at 10 kHz: body and no string. It now stops at its amp and goes
# through the engine's cabinet, as the title track's wall and On Its Hinge's second pair do (Harry, 17 Nov, on a
# guitar heard alone: "The engine's cabinet is nearer"): -1.7 / +3.4 at 630 / 800 Hz, -1.3 / -3.2 at 8 / 10 kHz,
# mean distance 3.57 -> 1.89 dB. In the mix, against the records' passages without a voice, 250-500 Hz falls 0.1 to
# 1.2 dB in every stretch the pair plays (the six together at 2:55: +3.6 -> +2.4) and 500 Hz-1 kHz 0.3 to 0.8;
# 2-4 kHz rises 0.3 to 0.4.
# microphone (0 the cone's centre to 1 its edge; 0.3 was brighter still at 2.5-5 kHz, 0.5 takes the mix's short
# 4-8 kHz down further) ; the two cones (this song's own: the other pairs have 70 to 73) ; distance ; track gain
# (alone the pair is as loud as it was, -23.4 LUFS) ; the song's loudness target (the first two minutes null against
# v20). Empty restores v20.
WALL = os.environ.get('C10T9_WALL', '0.4;74,75;0.15;-1.3;-10.038' if GATHER else '')
# v22 (chirper-three; instrument round: the tabla, in its three places: the fives at 1:20, the sevens at 2:10 and its
# one beat in the gears at 2:36). THE TABLA GETS ITS HANDS. Read alone and in the mix (raw, seed 0), the library's
# drums at these speeds were not struck, they were held: a treble stroke had fallen 1.8 dB in 500 Hz-1 kHz when the
# next one came at the sevens (3.6 at the fives), so the drum was one long F5 with a ripple on it; it held 52% of
# the mix's 250-500 Hz and 55% of its 500 Hz-1 kHz in the sevens, where the mix read 2 dB over the records in
# both; and above 2 kHz a stroke's first 15 ms stood 35 dB under everything else: no finger at all.
# Now, on the tracks' own patch strings (the song's it-tabla and the library's kit are untouched):
#   ONE HEAD, ONE SOUND: the treble drum's strokes (na, tin, te, re) stop each other, and the bass drum's (ge,
#     gem), as a hand landing on a skin stops what it was doing (the kit's choke groups);
#   THE RING FALLS AWAY: na dies in 250 ms and tin in 300 (1.3 and 1.6 s), so a stroke has fallen 7 dB when the
#     next comes at the sevens and 13 at the fives;
#   THE STROKE HAS A FRONT: the drum's own third, fourth and fifth partials (1 to 1.75 kHz on F) are struck harder
#     (they die first, so they are the attack and not the ring), and the finger's click is 16 dB up and 40 ms long;
#   and the three faders come up 4.5 dB, so that the drum holds the share of 500 Hz-1 kHz the two composers gave
#     it (about half of the mix's, in both passages), now as strokes and not as a tone. (At 1.5 dB, where a stroke's
#     first 30 ms stood where it had against the band, the mix read nearest the records, but the drum held a third
#     of that band and the scorer no longer heard the sevens as the fives come back: 92.5 -> 85.1.)
# the ring of na ; of tin ; the finger, dB over the library's ; its length ; na's third, fourth and fifth partials ;
# tin's ; dB on the three tabla faders ; the loudness target ('' = unchanged) ; dB on the bass drum's two pieces (it
# is not changed, so it gives back what the faders add). Empty restores v21 byte for byte.
FINGERS = os.environ.get('C10T9_FINGERS', '250ms;300ms;16;40ms;0.8,0.65,0.45;0.65,0.45,0.25;4.5;-10.064;-4.5' if WALL and KHANDA else '')
WALK = []
ALL = ("gl", "gr", "dl", "dr", "wl", "wr")
MARKS = []
ROOTS = [(0, 0)]


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


def add(tr, beat, length, pitch, vel, **expr):
    n = {"at": round(beat, 5), "len": round(length * 0.98, 5), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, beat, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "hp": "hat", "c": "cym", "x": "cym", "rbs": "crossbell"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(beat, 5), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


def one_again(tr, cell, pos, midi, pitch, length, returning):
    """Voicing and duration for one stroke at the two bookends; None is a rest."""
    hook = pos in (3, 5)
    after_hook = pos in (4, 6)
    if not returning and cell < len(CELLS):
        return pitch, length             # teach both cells in their original register
    if returning and GATHER and cell == RUNG // N - 1:
        return pitch, length             # v20: the fourth cell of the return is all six on the one riff, every stroke a chord
    if not returning or cell == RUNG // N - 1:
        if tr not in ("gl", "gr"):
            return None                  # fourth cell of the return: the first two players
        if tr == "gr" and after_hook:
            return None
        if tr == "gr" and hook:
            return midi + 12, 1.85       # across the mute which the left hand still plays
        return midi, length
    if tr in ("wl", "wr"):
        # The wide pair gets only the answers, the same notes as the opening's
        # right hand with the fifth below them. The mutes no longer choke them.
        return (f"{nm(midi + 7)},{nm(midi + 12)}", 1.85) if hook else None
    if tr in ("dl", "dr"):
        if cell == len(CELLS):           # third cell: the inner pair goes over the wide pair
            return (midi + 24, 1.85) if hook else None
        if hook:
            return None                  # first two cells: this pair plays the pedal, not the answers
    return pitch, length


def keep_lock_stroke(beat, slot):
    """Two eight-beat sentences on the fixed septuplet grid; third is untouched."""
    if beat < N+1:
        return slot < min(beat+1,N)  # admit the head first; both hooks arrive in turn
    if beat < 2*(N+1):
        return slot >= beat-(N+1)    # take the head away first; only the tail, then air
    return True


def deal(b0, beats, k, gtrs, low=True, root=0, chords="", cut=False):
    """Deal the cell. Chord letters: o = cell head, h = hook, c = clipped pedal fifth on a mute."""
    for i in range(beats * k):
        kind = CELLS[(i // N) % len(CELLS)][i % N]
        at = b0 + i / k
        midi = F1 + root + (0 if kind in ("o", "c") else int(kind))
        part = kind if kind in ("o", "c") else "h"
        pitch = midi
        if part in chords:
            intervals = (0, 7) if part == "c" else (0, 7, 12)
            pitch = ",".join(nm(midi + j) for j in intervals)
        mute = part == "c"
        vel = 0.82 if mute else 1.0 if part == "o" else 0.95
        if HANDS and k == 4 and part == "h":
            # Sixteen cells in this rung. Exchange jobs after eight, not at a
            # bar line: the reversal follows the riff, halfway through bar four.
            first_answer = i % N == 3
            picked = first_answer != (i >= beats * k // 2)
            if picked:
                add("picked", at, 1.55 / k, midi + 12, 0.94)
            else:
                add("keyed", at, 0.85 / k, midi + 24, 0.96)
        else:
            for tr in gtrs:
                if cut and not keep_lock_stroke(i//N, i%N):
                    continue
                note = pitch, (0.65 if mute else 1) / k
                if RING and k == 1:
                    note = one_again(tr, i // N, i % N, midi, *note, returning=bool(chords))
                if note is not None:
                    voice, length = note
                    add(tr, at, length, voice, vel, **({"pm": 1} if mute else {}))
        if not low:
            continue
        if k == N:                              # the beat and cell are now one: a footfall, not a kick roll
            if part == "o":
                slow = CELLS[(i // N // N) % len(CELLS)][i // N % N] if AUGMENT and root == 0 else "o"
                walk = midi + (0 if slow in ("o", "c") else int(slow))
                add("bass", at, 1, walk, 0.96 if slow == "o" else 0.9 if slow == "c" else 0.98)
                if walk != midi:
                    WALK.append((at, walk - F1))
                drum("k", at, 1)
        elif k >= 3:
            if not mute:                        # three accents held through the guitar ticks: 3 + 2 + 2
                add("bass", at, min((3 if part == "o" else 2) / k, b0 + beats - at), midi, 0.93)
                drum("k", at, 0.97 if part == "o" else 0.86)
        else:
            add("bass", at, (0.68 if mute else 1) / k, midi, vel)
            drum("k", at, vel)


def gear_down(b0, root, cell0):
    """Every speed of the song, fastest first, one beat each. The riff never restarts."""
    strokes = []
    for step, k in enumerate(range(N, 0, -1)):
        for j in range(k):
            i = len(strokes)
            kind = CELLS[(cell0 + i // N) % len(CELLS)][i % N]
            strokes.append((b0 + step + j / k, k, kind))
    low = []                                     # the bass and foot do what they did at each speed
    for at, k, kind in strokes:
        part = kind if kind in ("o", "c") else "h"
        mute = part == "c"
        midi = F1 + root + (0 if part != "h" else int(kind))
        vel = 0.82 if mute else 1.0 if part == "o" else 0.95
        chords = "o" if GEAR == "plain" or k > 5 else "oh" if k > 3 else "ohc"
        pitch = midi
        if part in chords:
            pitch = ",".join(nm(midi + x) for x in ((0, 7) if mute else (0, 7, 12)))
        for tr in ALL:
            add(tr, at, (0.65 if mute else 1) / k, pitch, vel, **({"pm": 1} if mute else {}))
        if k == N:
            if part == "o":
                low.append((at, 1, midi, 0.96, 1))
        elif k >= 3:
            if not mute:
                low.append((at, (3 if part == "o" else 2) / k, midi, 0.93, 0.97 if part == "o" else 0.86))
        else:
            low.append((at, (0.68 if mute else 1) / k, midi, vel, vel))
    for (at, length, midi, vel, foot), nxt in zip(low, low[1:] + [(b0 + N,)]):
        add("bass", at, min(length, nxt[0] - at), midi, vel)
        drum("k", at, foot)


def beat(b0, b1, cym="x", vel=0.5, snare=(1, 3)):
    for b in range(b0, b1):
        drum(cym, b, vel + (0.05 if (b - b0) % 4 == 0 else 0))
        if (b - b0) % 4 in snare:
            drum("s", b, 0.95)


def last_to_turn(seam):
    """The two cells in eighths take exactly as long as three cells in triplets."""
    lo, hi = seam - N, seam + N
    T["bass"] = [n for n in T["bass"] if not lo <= n["at"] < hi]
    # Let the second bass cell speak once in the clear before the new tempo
    # of the guitars crosses it. They strike its F, damp the strings and come
    # back for its last pickup; the foot and hat never leave the old grid.
    exposed = seam - N / 2
    for tr in ("gl", "gr"):
        T[tr] = [n for n in T[tr] if not exposed < n["at"] < seam - .5]
    for start in (lo, seam):
        for j, cell in enumerate(CELLS):
            at = start + j * N / 2
            # A low open F; the thumb-to-octave leap on the first answer; the
            # second answer back close to the floor. The chugs are guitar alone.
            heads = [i for i, stroke in enumerate(cell) if stroke != "c"]
            for i, end in zip(heads, heads[1:] + [N]):
                midi = F1 if i == 0 else F1 + int(cell[i]) + (12 if i == heads[1] else 0)
                add("bass", at + i / 2, (end - i) / 2 - .09, midi, .97 if i == 0 else .9)


def tune_the_heads(seam):
    """The same scale under two clocks. The cell of seven advances two slots
    at five to the beat but only one at six. No tap or quarter moves in time.
    Let the highest tap in each cycle cross the footfall without the low riff.
    """
    degrees = PLACES
    holes = set()
    for event in T['pawl']:
        at = event['at']
        if not seam-2*N <= at < seam+2*N:
            continue
        speed = 5 if at < seam else 6
        # Integer subdivisions; never take a remainder on a rounded timestamp.
        tick = round((at-seam)*speed)
        slot = tick % speed
        event['pitch'] = nm(F1 + 36 + degrees[slot])
        if slot == speed-1:
            event['len'] = round(2.5/speed*.98, 5)
            holes.update(round(seam+(tick+j)/speed, 5) for j in range(3))
    for tr in ('gl','gr','bass','kick'):
        T[tr] = [e for e in T[tr] if e['at'] not in holes]


def six_strings(seam):
    """Two turns of seven beats at six to the beat: 84 strokes, a string to a stroke."""
    speed = N - 1
    up = int(SIX.split(';')[1])
    taps = {e['at']: e for e in T['pawl'] if seam <= e['at'] < seam + 2*N}
    alone = set()
    for tick in range(0, 2*N*speed, N):
        tap = taps[round(seam + tick/speed, 5)]
        # The guitar's strings are the tap's notes, an octave under it.
        assert tap['pitch'] == nm(F1 + 36 + PLACES[tick % speed]) and tick % (N*speed) // N == tick % speed
        if tick % speed == speed - 1:
            alone.update(range(tick, tick + 3))
    for tick in range(2*N*speed):
        turn, since = divmod(tick, N*speed)
        string = tick % speed
        if (turn == 0 and since < N*string) or tick in alone:
            continue
        at = seam + tick/speed
        named = since % N == 0                 # the stroke the tap falls on
        # Each string rings through the next one and is damped; before the
        # strokes left to the tap, and before the cadence, the hand stops it.
        rings = 1 if tick + 1 in alone else 2
        add('six', at, min(rings/speed, seam + 2*N - .03 - at), F1 + up + PLACES[string],
            .95 if named else .82 if string == 0 else .7)


def before_the_lock(seam):
    """Two turns of seven beats. Keep counting six right up to the kit break;
    it is the harmony, not an early switch to quarters, that prepares the lock.
    """
    speed = N-1
    start, half, stop = seam-2*N, seam-N, seam-1
    resolve = half+N/2
    T['bass'] = [e for e in T['bass'] if not start<=e['at']<seam]
    for i in range(2*speed):
        at = start+i*N/speed
        if at<stop:
            # The dominant pedal is picked at CELL heads, still drifting past
            # the kit. Shorten the partial last cell before the kit's beat.
            add('bass',at,min(.88*N/speed,stop-at),F1+7,.92)
    # The left player never lets the sixes go. Against the bass's C the right
    # holds a fourth, then a major third. F2 is in the existing landing chord.
    T['gr'] = [e for e in T['gr'] if not half<=e['at']<seam]
    for a,b,semi in ((half,resolve,12),(resolve,stop,11)):
        lo = F1+semi
        add('gr',a,b-a-.06,f'{nm(lo)},{nm(lo+12)}',.92)
    for e in T['pawl']:
        if resolve<=e['at']<seam:
            e['pitch'] = nm(F1+36-1)
            e['len'] = min(e['len'],round(stop-e['at']-.02,5))


def chord_before_the_line(seam):
    """The head of a locked cell forecasts its own pitches; the low strings catch them."""
    bar = 4
    start, stop = seam + 2*bar, seam + 6*bar
    for tr, which in (('wl', 0), ('wr', 1)):
        tops = []
        for n in T[tr]:
            at = n['at']
            if not start <= at < stop or at != int(at):
                continue
            phrase_bar = int(at-start)//bar
            if (which==0 and phrase_bar==3) or (which==1 and phrase_bar==0):
                continue  # the left introduces the idea; the right finishes it
            cell = CELLS[int(at-seam) % len(CELLS)]
            slot, interval = [(i,int(k)) for i,k in enumerate(cell) if k not in ('o','c')][which]
            # Keep the low root and fifth at their full speed. Exchange the
            # octave string, with its own gate; don't add another downbeat.
            root, fifth, octave = n['pitch'].split(',')
            assert octave == nm(F1+12)
            n['pitch'] = root + ',' + fifth
            tops.append(dict(n, pitch=nm(F1+24+interval), len=round(slot/N,5)))
        T[tr].extend(tops)


def slow_hand(start):
    """One slow cell, two bass cells and four fast cells occupy seven beats."""
    # Quote the actual bass phrase from v5, not a second transcription of it.
    source = 2 * RUNG - N
    phrase = [n for n in T['bass'] if source <= n['at'] < source + N]
    assert len(phrase) == sum(tok != 'c' for cell in CELLS for tok in cell)
    end = start + len(CELLS) * N
    T['bass'] = [n for n in T['bass'] if not start <= n['at'] < end]
    for j in range(len(CELLS)):
        T['bass'].extend({**n, 'at': start + j*N + n['at'] - source} for n in phrase)
    # The foot picks out the three pitched strokes on the first slow pass.
    # On the second it is back with the fast side; china and snare stay in four.
    T['kick'] = [n for n in T['kick'] if not start <= n['at'] < start + N]
    for i, k in enumerate(CELLS[0]):
        if k != 'c':
            drum('k', start + i, .97 if k == 'o' else .86)
    for j, cell in enumerate(CELLS):
        head = start + j*N
        outer, inner = ('gr', 'dr') if j % 2 == 0 else ('gl', 'dl')
        for tr in (outer, inner):
            T[tr] = [n for n in T[tr] if not head <= n['at'] < head + N]
        for i, k in enumerate(cell):
            at = head + i
            if k == 'c':
                add(inner, at, .56, F1, .79, pm=1)
            else:
                # The outer guitarist rings through the inner player's mutes,
                # not through the next pitch or the seam into five.
                until = next((p for p in range(i+1, N) if cell[p] != 'c'), N)
                pitch = F1 + 12 if k == 'o' else F1 + 24 + int(k)
                add(outer, at, until - i - .14, pitch, .97 if k == 'o' else .94)


def work_the_hats(start):
    """Four cells of eighths: two players' jobs on a single hi-hat.
    Striking on a footfall gives one closed attack, never two stacked hits.
    Between footfalls the cymbals open; the following step chokes the wash.
    """
    first = N                              # leave the first cell of eighths plain
    last = first + 2*len(CELLS)*N          # back to the old beat before the card
    lo, hi = start+first/2, start+last/2
    T['hat'] = [e for e in T['hat'] if not lo<=e['at']<hi]
    for i in range(first,last):
        at = start+i/2
        k = CELLS[(i//N)%len(CELLS)][i%N]
        if i%2==0:                        # foot presses on every quarter
            drum('hp' if k=='c' else 'h', at, .60 if k=='c' else .58)
        elif k!='c':                      # long enough to cross the footfall if left open
            add('hat', at, 1.25, 'oh', .59 if k=='o' else .53)


def crossbeat(b):
    """Last five bars of the threes. All positions derived from one 12-stroke bar."""
    for bar, voices in enumerate(('bbb','bbb','bss','sbs','sss')):
        a = b + 4*bar
        for q in range(4):
            drum('hp', a+q, .85 if q==0 else .74)
        if bar < 2:                 # establish three against the existing backbeat
            for q in (1,3): drum('s', a+q, .88)
        for j,voice in enumerate(voices):
            at = a + j*4/3
            if voice=='b': drum('rbs', at, .88 if j==0 else .81)
            else: drum('s', at, (.72,.83,.97)[j] if bar==4 else .88)


def hold_the_ones(b):
    """Two cells: the open F for its three beats, each answer through its mute.
    What the bass does from three to the beat on, a pipe can do at one."""
    for cell, strokes in enumerate(CELLS):
        heads = [i for i, k in enumerate(strokes) if k != 'c']
        assert heads == [0, 3, 5]
        for i, end in zip(heads, heads[1:] + [N]):
            midi = F1 + 24 + (0 if strokes[i] == 'o' else int(strokes[i]))
            add('wind', b + cell*N + i, end - i - .1, midi, .8)
            T['wind'][-1]['gain'] = WIND


def count_the_five(b0, beats):
    """Jhaptal at five to the beat for `beats` beats, the last two a tihai that lands on the beat after them.
    A dhin is the ringing treble stroke and the bass drum together, written as two notes: the library's own
    compound stroke tunes its bass a twelfth under the treble, which would be B flat here."""
    theka = (("tin", "ge", .9), ("na", "", .62), ("tin", "ge", .8), ("tin", "ge", .68), ("na", "", .74),
             ("tin", "", .88), ("na", "", .62), ("tin", "ge", .8), ("tin", "ge", .68), ("na", "", .74))
    assert beats % 2 == 0 and b0 % 4 == 0, "whole turns, the first on a bar line"
    body = (beats - 2) * 5

    hard = float(KHANDA.split(";")[2])

    def bol(piece, at, vel, length=.19):
        T.setdefault("tabla", []).append({"at": round(at, 5), "len": length, "pitch": piece, "vel": round(min(1, vel * hard), 3)})

    for i in range(body):
        treble, low, vel = theka[i % 10]
        swell = .9 + .1 * i / body
        bol(treble, b0 + i / 5, vel * swell)
        if low:                                 # the wrist slides the bass drum up on each bar line
            bol("gem" if i % 20 == 0 else low, b0 + i / 5, vel * swell * .9)
    for said in range(3):
        at = b0 + beats - 2 + said * 4 / 5
        for j, closed in enumerate(("te", "re")):
            # The closed strokes are the quietest the drum has: 14 dB under the mix where the dha is 8. Struck
            # harder they came up half a dB, so these six notes are turned up instead.
            bol(closed, at + j / 5, .9)
            T["tabla"][-1]["gain"] = "4dB"
        bol("na", at + 2 / 5, .9 + .05 * said, 1.5 if said == 2 else .19)
        bol("ge", at + 2 / 5, .86 + .06 * said, 1.5 if said == 2 else .19)
    assert abs(T["tabla"][-1]["at"] - (b0 + beats)) < 1e-9


def three_two_two(b):
    """The lock on F after its first slow cell: four guitars strike the open note and the answers and rest between."""
    first, who, stab = int(SHAPE.split(';')[0]), SHAPE.split(';')[1].split(','), float(SHAPE.split(';')[2])
    for tr in who:
        here = lambda n: b + first <= n['at'] < b + 32 - 1e-9
        keep = [n for n in T[tr] if not (here(n) and (n.get('expr') or {}).get('pm'))]
        assert len(T[tr]) - len(keep) == 4 * (32 - first), (tr, len(T[tr]) - len(keep))
        for n in keep:
            if here(n) and n['len'] <= 1 / N + 1e-9:      # the struck notes; the answers fretted ahead keep their length
                n['len'] = round(stab / N, 4)
        T[tr] = keep


def seven_by_hand(b):
    """Rupak at seven to the beat in the lock on F that starts at beat b; a tihai lands on the A flat."""
    field = RUPAK.split(';')
    start, low_at = int(field[0]), int(field[1])
    hard = float(KHANDA.split(';')[2])
    theka = (('tin', .88), ('tin', .66), ('na', .72), ('tin', .84), ('na', .64), ('tin', .8), ('na', .68))
    b0, end = b + start, b + 32
    body = (32 - start - 2) * N

    def bol(piece, at, vel, length=.13):
        T.setdefault('rupak', []).append({'at': round(at, 5), 'len': length, 'pitch': piece, 'vel': round(min(1, vel * hard), 3)})

    for i in range(body):
        treble, vel = theka[i % N]
        swell = .88 + .12 * i / body
        bol(treble, b0 + i / N, vel * swell)
        if i % N in (3, 5) and i // N >= low_at:        # the dhins: the riff's two answers
            bol('gem' if i == low_at * N + 3 else 'ge', b0 + i / N, vel * swell * .9)
    for said in range(3):                               # te re dha _ _ _ , te re dha _ _ _ , te re DHA
        at = end - 2 + said * 6 / N
        for j, closed in enumerate(('te', 're')):
            bol(closed, at + j / N, .9)
            T['rupak'][-1]['gain'] = '4dB'              # as at 1:30: the closed strokes are the drum's quietest
        last = said == 2
        bol('na', at + 2 / N, .9 + .05 * said, .5 if last else .13)
        if not last:                                    # the third dha's low drum is the band, in A flat
            bol('ge', at + 2 / N, .86 + .06 * said)
    assert abs(T['rupak'][-1]['at'] - end) < 1e-9


def every_time_once_more(b0, root, cell0):
    """The gears from beat b0, each beat with the band and the guest its speed had on the way up."""
    strokes = []
    for step, k in enumerate(range(N, 0, -1)):
        for j in range(k):
            i = len(strokes)
            strokes.append((b0 + step + j / k, k, CELLS[(cell0 + i // N) % len(CELLS)][i % N]))
    for step, k in enumerate(range(N, 0, -1)):          # the band each speed had
        band = ALL if k == N else ("gl", "gr", "dl", "dr") if k in (3, 4) else ("gl", "gr")
        for tr in ALL:
            if tr not in band:
                T[tr] = [n for n in T[tr] if not b0 + step <= n["at"] < b0 + step + 1 - 1e-9]
    at6, at5, at4, at3, at2, at1 = (b0 + N - k for k in (6, 5, 4, 3, 2, 1))
    for j, place in enumerate(PLACES):                  # six: one pass across the nylon's strings
        add("six-ab", at6 + j / 6, 2 / 6, F1 + int(SIX.split(";")[1]) + root + place, 0.95 if j == 0 else 0.82)
    first = 4 * RUNG                                    # five: the first five strokes the tabla played, on A flat drums
    T["tabla-ab"] = [{**n, "at": round(n["at"] - first + at5, 5)} for n in T["tabla"] if first <= n["at"] < first + 1 - 1e-9]
    assert len({n["at"] for n in T["tabla-ab"]}) == 5
    for at, k, kind in strokes:                         # four: both hands on the answer; the guitars leave it to them
        if k == 4 and kind not in ("o", "c"):
            midi = F1 + root + int(kind)
            for tr in ALL:
                T[tr] = [n for n in T[tr] if abs(n["at"] - at) > 1e-6]
            add("picked", at, 1.55 / k, midi + 12, 0.94)
            T["picked"][-1]["gain"] = REPRISE.split(";")[2]
            add("keyed", at, 0.85 / k, midi + 24, 0.96)
            T["keyed"][-1]["gain"] = REPRISE.split(";")[2]
    drop = lambda tr, piece, beats: [n for n in T[tr] if not (n["pitch"] == piece and any(abs(n["at"] - q) < 1e-6 for q in beats))]
    T["cym"] = drop("cym", "x", (at3, at2, at1))        # where the sticks were on the bell and the hat, not the china
    T["snare"] = drop("snare", "s", (at1,))             # the song began without a snare
    drum("hp", at3, 0.85)                               # three: the bell of the ride on every stroke, over the foot
    for j in range(3):
        drum("rbs", at3 + j / 3, 0.88 if j == 0 else 0.81)
    drum("hp", at2, 0.60)                               # two: the foot, then the hat left open across the next beat
    add("hat", at2 + 0.5, 1.25, "oh", 0.53)
    T["hat"][-1]["gain"] = REPRISE.split(";")[2]
    drum("h", at1, 0.45)                                # one: the opening's closed hat (it shuts the open one)


def fill(b):
    """The last two beats before beat b."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, b - 2 + i / 4, 0.6 + 0.045 * i)


def compose():
    T.clear()
    MARKS.clear()
    WALK.clear()
    ROOTS[:] = [(0, 0)]
    names = ["one to the beat", "two", "three", "four", "five", "six"]
    b = 0
    for k in range(1, 7):
        MARKS.append((names[k - 1], b))
        gtrs = ("gl", "gr", "dl", "dr") if k in (3, 4) else ("gl", "gr")
        deal(b, RUNG - int(k == N - 1), k, gtrs, low=k >= 2)
        if k == 3 and CROSS:
            cross_at = b + RUNG - 5*4
            beat(b, cross_at)
            crossbeat(cross_at)
        elif k < 3:
            beat(b, b + RUNG, cym="h", vel=0.45, snare=())
        else:
            beat(b, b + RUNG)
        if PAWL and k in (5, 6):
            # Tap each cell head, NOT each beat. Its 7 partials come from the cell itself. The tone crosses
            # from the three open strokes to the four muted ones; the kick takes its job when the cell locks.
            for i in range(0, (RUNG - int(k == N - 1)) * k, N):
                phase = (b + i / k - 4 * RUNG) / (2 * RUNG)
                add("pawl", b + i / k, 0.23, F1 + 36, 0.91, turn=round(0.12 + 0.70 * phase, 4))
        for j in range(0, RUNG, N):                      # where the riff comes round to the beat again
            if k >= 2:
                drum("c", b + j, 0.9 if j == 0 else 0.7)
        b += RUNG
    if CLUTCH:
        work_the_hats(RUNG)
    if BASS_TURN:
        last_to_turn(2 * RUNG)
    if SLOW_HAND:
        slow_hand(4 * RUNG - len(CELLS)*N)
    if PAWL and HEAD_TUNE:
        tune_the_heads(5 * RUNG)
    if KHANDA:
        count_the_five(4 * RUNG, 2 * N)
    if SIX:
        six_strings(5 * RUNG)
    if CADENCE and PAWL:
        before_the_lock(b)
    # seven to the beat: the riff is one beat long
    MARKS.append(("seven: it locks", b))
    fill(b)
    drum("c", b, 0.95)
    deal(b, 32, 7, ALL, chords="o")
    if FORETELL:
        chord_before_the_line(b)
    if SHAPE:
        three_two_two(b)
    if RUPAK:
        seven_by_hand(b)
    ROOTS.append((b + 32, 3))
    deal(b + 32, 24 - (N if GEAR else 0), 7, ALL, root=3, chords="o", cut=bool(CUT))
    if GEAR:
        gear_down(b + 56 - N, 3, 24 - N)
    drum("c", b + 32, 0.9)
    for j in range(4, 56, 4):
        if j != 32:
            drum("c", b + j, 0.65)
    beat(b, b + 56)
    if REPRISE:
        every_time_once_more(b + 56 - N, 3, 24 - N)
    b += 56
    # one to the beat again, every note a chord
    MARKS.append(("one again", b))
    ROOTS.append((b, 0))
    if not GEAR:
        fill(b)                                  # the gears are the fill now
    deal(b, RUNG, 1, ALL, chords="ohc")
    beat(b, b + RUNG, snare=(2,))
    for j in range(0, RUNG, N):
        drum("c", b + j, 0.95 if j == 0 else 0.8)
    if WIND:
        hold_the_ones(b)
    b += RUNG
    MARKS.append(("one chord", b))
    for tr in ALL:
        add(tr, b, 8, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", b, 8, F1, 0.95)
    drum("k", b, 0.95)
    drum("c", b, 0.95)
    return b + 8


def song():
    total = compose()
    assert total % 4 == 0 and all(m[1] % 4 == 0 for m in MARKS)
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"            # each side is two takes from three to the beat on
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    tracks = [
        {"name": "gl", "patch": main.format(70), "gain": os.environ.get("C10T9_MAIN", "0.7dB"), "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(71), "gain": os.environ.get("C10T9_MAIN", "0.7dB"), "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(72), "gain": os.environ.get("C10T9_DBL", "-2.5dB"), "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(73), "gain": os.environ.get("C10T9_DBL", "-2.5dB"), "pan": 0.75, "out": "gtrs", **mids},
        *([{"name": tr, "patch": f"ct-wall-stop-{side} fx.3.mix=0" + "".join(f" fx.4.bands.{i}.gain=0dB" for i in range(4)),
            "gain": WALL.split(";")[3] + "dB", "pan": pan, "out": "gtrs",
            "fx": [{"type": "cab", "model": "4x12-modern", "mic": float(WALL.split(";")[0]), "distance": float(WALL.split(";")[2]), "cone": int(cone)}]}
           for tr, side, pan, cone in zip(("wl", "wr"), "lr", (-0.75, 0.75), WALL.split(";")[1].split(","))] if WALL else
          [{"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
           {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall}]),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "pawl", "patch": "it-pawl", "gain": PAWL, "pan": -0.15}] if PAWL else []),
        *([{"name": "picked", "patch": "baritone fx.3.mix=0.07 fx.4.mix=0.09",
            "gain": HANDS.split(";")[0], "pan": -0.56},
           {"name": "keyed", "patch": "clav", "gain": HANDS.split(";")[1], "pan": 0.56}] if HANDS else []),
    ]
    if CROSS:
        tracks.append({"name": "crossbell", "patch": kit, "gain": CROSS.split(';')[0], "pan": 0.30,
                       "out": "drums", "sends": {"oh": "0dB"}, "fx": air})
    if WIND:
        # The library's cathedral rings for 5.5 s. A smaller room: the review
        # excerpt that follows these pipes (2:53.2) must stay dry.
        tracks.append({"name": "wind", "patch": "organ-pipe fx.0.decay=1.6s fx.0.mix=0.22", "gain": "0dB", "pan": 0.1})
    if KHANDA:
        tracks.append({"name": "tabla", "patch": "it-tabla", "gain": KHANDA.split(";")[0], "pan": 0.2})
    if SIX:
        tracks.append({"name": "six", "patch": "it-six", "gain": SIX.split(";")[0], "pan": 0.3})
    if RUPAK:
        tracks.append({"name": "rupak", "patch": "it-tabla", "gain": RUPAK.split(";")[2], "pan": 0.2})
    if REPRISE:
        tracks.append({"name": "tabla-ab", "patch": "it-tabla-ab", "gain": REPRISE.split(";")[1], "pan": 0.2})
        tracks.append({"name": "six-ab", "patch": "it-six-ab", "gain": REPRISE.split(";")[0], "pan": 0.3})
    if FINGERS:                                 # v22: the tabla's hands, on its three tracks' own patch strings
        na, tin, click, clen, pna, ptin, lift = FINGERS.split(";")[:7]
        bayan = FINGERS.split(";")[8] if len(FINGERS.split(";")) > 8 else ""
        hands = " ".join([f"kit.{pc}.choke=dayan" for pc in ("na", "tin", "te", "re")] + [f"kit.{pc}.choke=bayan" for pc in ("ge", "gem")]
                         + [f"kit.na.patch.synth.amp.d={na}", f"kit.tin.patch.synth.amp.d={tin}",
                            f"kit.na.patch.synth.layers.1.level.value={-148 + float(click):g}dB",
                            f"kit.tin.patch.synth.layers.1.level.value={-150 + float(click):g}dB",
                            f"kit.na.patch.synth.env.c.d={clen}", f"kit.tin.patch.synth.env.c.d={clen}",
                            "kit.na.patch.synth.layers.0.partials=[[2,1],[3,{}],[4,{}],[5,{}],[1,0.12]]".format(*pna.split(",")),
                            "kit.tin.patch.synth.layers.0.partials=[[1,0.75],[2,1],[3,{}],[4,{}],[5,{}]]".format(*ptin.split(","))]
                         + ([f"kit.ge.gain={bayan}dB", f"kit.gem.gain={bayan}dB"] if bayan and float(bayan) else []))
        for t in tracks:
            if t["name"] in ("tabla", "rupak", "tabla-ab"):
                t["patch"] += " " + hands
                t["gain"] = f"{float(t['gain'][:-2]) + float(lift):g}dB"
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", 0]], 0
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p - 0.02:g}b", prev], [f"{p:g}b", r]]
            prev = r
    if CADENCE and PAWL:
        # The old F-centred EQ takes the body out of a held C. Move the
        # existing three key-following bands with it; reset in the kit break.
        land = dict(MARKS)['seven: it locks']; start = land-2*N
        pts += [[f'{start-.02:g}b',0],[f'{start:g}b',7],[f'{land-1:g}b',7],[f'{land-.02:g}b',0]]
        pts.sort(key=lambda point: float(point[0].removesuffix('b')))
    if WALK:
        # One beat on each note of the slow tune. Take away any step the song's
        # own grounds make inside that beat (the move to A flat follows the
        # bass's A flat), and come back to whatever ground is next.
        when = lambda point: float(point[0].removesuffix('b'))
        for at, semis in WALK:
            after = [r for q, r in ROOTS if q <= at + 1][-1]
            pts = [point for point in pts if not at < when(point) <= at + 1]
            pts += [[f'{at - .02:g}b', 0], [f'{at:g}b', semis], [f'{at + .98:g}b', semis], [f'{at + 1:g}b', after]]
        pts.sort(key=when)
    return {
        "about": ("chirpers X (Common Time), track 9 by chirper-zero: In the Time Of. One riff of seven notes and one beat that never "
                  "changes (84). The band deals the riff out at one note to the beat, then two, three, four, five, six, drifting "
                  "across the beat and coming round to it every seven beats; at seven to the beat the riff is exactly one beat long "
                  "and locks. The bass and kick walk in quarters underneath. Then once more at one to the beat, every stroke a chord. "
                  "v1 is the skeleton.") + (" At four to the beat the two hook notes pass between a baritone guitar and a clavinet; they exchange roles halfway." if HANDS else "")
                 + ((" One guitar lets the two answers ring across the pedal on the opening repeat. At the return the wide pair takes them, then all six play the last cell as one before landing on F." if GATHER else
                     " One guitar lets the two answers ring across the pedal on the opening repeat. At the return the wide pair takes them, then the original two guitars play the last cell before everyone lands on F.") if RING else ""),
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(FINGERS.split(";")[7]) if FINGERS and FINGERS.split(";")[7] else float(WALL.split(";")[4]) if WALL else float(GATHER.split(";")[1]) if GATHER else float(REPRISE.split(";")[3]) if REPRISE else float(RUPAK.split(";")[3]) if RUPAK else float(SHAPE.split(";")[3]) if SHAPE else float(SIX.split(";")[2]) if SIX else float(KHANDA.split(";")[1]) if KHANDA else PIPE_LUFS if WIND else -10, "seed": 1, "tail": "5s", "length": f"{total}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}, **({'hp': {'gain': CROSS.split(';')[1]}} if CROSS else {}),
                            **({'oh': {'patch':'haake-hat amp.d=1.05s amp.r=180ms amp.curve=2.2',
                                       'gain':CLUTCH,'pan':-.45,'choke':'hat'}} if CLUTCH else {})}},
                    **({"it-pawl": {"synth": {"layers": [{"type": "wavetable", "frames": [
                        [[j, round(1 / j**0.45, 4)] for j, x in enumerate(CELLS[0], 1) if x != "c"],
                        [[j, round(1 / j**0.45, 4)] for j, x in enumerate(CELLS[0], 1) if x == "c"]],
                        "position": {"value": 0, "mod": [{"src": "expr.turn", "amount": 1}]}}],
                        "amp": {"a": "3ms", "d": "105ms", "s": 0.22, "r": "42ms"}}}} if PAWL else {}),
                    # the library's tabla, its treble drum on F and its bass drum on the riff's low F
                    **({"it-tabla": {"extends": "tabla-kit", "kit": {**{pc: {"pitch": "F4"} for pc in ("na", "tin", "te")},
                                                                    "re": {"pitch": "Eb4"}, "ge": {"pitch": "F2"}, "gem": {"pitch": "F2"}}}} if KHANDA else {}),
                    # the same drums a minor third up, for the one beat of fives in the gears (which are on A flat)
                    **({"it-tabla-ab": {"extends": "tabla-kit", "kit": {**{pc: {"pitch": "Ab4"} for pc in ("na", "tin", "te")},
                                                                       "re": {"pitch": "Gb4"}, "ge": {"pitch": "Ab2"}, "gem": {"pitch": "Ab2"}}}} if REPRISE else {}),
                    **({"it-six-ab": {"extends": "nylon", "play": {"tuning": " ".join(nm(F1 + int(SIX.split(";")[1]) + 3 + j) for j in PLACES)}}} if REPRISE else {}),
                    # the library's nylon-string guitar, its six open strings the six places in the beat
                    **({"it-six": {"extends": "nylon", "play": {"tuning": " ".join(nm(F1 + int(SIX.split(";")[1]) + j) for j in PLACES)}}} if SIX else {})},
        "buses": {
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
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T9_MASTER", "2.7dB")}]},
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
    if os.environ.get("C10T9_SHOW"):
        end = compose()
        sec = 60 / BPM
        for (name, b0), (_, b1) in zip(MARKS, MARKS[1:] + [("", end)]):
            print(f"{name:16s} bars {b0 // 4 + 1:3d}-{b1 // 4 + 1:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}")
    else:
        open(OUT, "w").write(dump(song()))
