#!/usr/bin/env python3
"""chirpers10-t14 "Slow Enough to Count" (chirper-three): a chord is a rhythm, too fast to count.

Harry, 19 Nov: "each climber can go crazy and make the song they want to mkae". This is the one I wanted to make.

THE IDEA. Strike anything steadily and fast enough and you stop hearing strokes: you hear a note. Twice as fast is
the octave above. So a pulse and a pitch are one thing at two speeds, and an interval is a polyrhythm: a fifth is
three against two, a fourth four against three, a minor third six against five. Every other song on this record
chooses its cycles and then chooses its notes. This one has ONE RULE that does both:

        what strikes every p sixteenths plays the note whose period is p (octaves are free: doubling is an octave)

THE TEMPO IS IN THE KEY. At 122.7756 a pulse every three sixteenths is F3 exactly six octaves down (174.61 Hz / 64).
Then, with no further choice:

  every 3, 6, 12 sixteenths   F        the dotted values: the djent chug
  every 1, 2, 4, 8, 16        C        COMMON TIME ITSELF: the beat is a C, the bar is a C, the backbeat is a C
  every 5, 10, 20             A flat   the fives
  every 9, 18                 B flat   a half bar and a sixteenth: it comes a sixteenth LATE every half bar
  every 15                    D flat   a bar less a sixteenth: it comes a sixteenth EARLY every bar
  (every 7: a D a third of a semitone sharp; every 11: a G flat a quarter-tone sharp. Not used yet. They are
  track 1's other two wheels: its five is this song's A flat.)

So threes against the kit's four are F over C, a fifth, the power chord. Add the fives and the groove is F minor
(periods 3, 4, 5 are frequencies 20:15:12, the minor triad). The three pulses come round together every 60
sixteenths and with the bar line every 240, fifteen bars: the record's long cycle, here the length of a chord.
Where the threes and the fives meet (every 15) is the note they are both harmonics of, D flat: play it and the
chord is D flat major with the kit's C on top. Every third three is a nine: B flat, the fifth below F. The harmony
of the song is which pulses are sounding; nothing else was chosen.

THE FORM is the proof, both ways.
  held        bar 0       three toms, tuned F3, C3 and A flat 2 (the album kit's own tuning), each rolled at its own
                          note: 174.6, 131.0 and 104.8 strokes a second. You hear a chord
  unwound     bars 1-7    the three rolls slow down together, an octave a bar, six octaves: buzz, purr, rattle, strokes
  counted     bars 7-22   they arrive in tempo: threes, fours, fives. The chord is still in the heads; its speed is now
                          a rhythm. Each time the three meet (every 60) a pulse is handed to the band: F (kick, bass,
                          two guitars), then A flat (two more guitars), then C: the cymbal and snare, common time
  minor       bars 22-37  the whole chord for one whole cycle of fifteen bars
  sixth       bars 37-52  the low D flat sounds wherever threes and fives meet: a bar less a sixteenth apart, so the
                          band's biggest stroke slides a sixteenth earlier every bar and is home after fifteen
  fourth      bars 52-67  the quiet middle, B flat minor: B flat every nine on the left, D flat every fifteen on the
                          right, the F pulse on the foot alone; the hands on the closed hat
  common      bars 67-75  everyone on C: sixteenths, eighths, quarters, the bar. The one plain stretch, and by the
                          rule the plainest thing a band can play is the dominant
  home        bars 75-90  F minor again, everything; the toms come back on their pulses for the last meeting
  wound       bars 90-96  the three toms alone speed up, an octave a bar, until the rhythm is the chord again
  one chord   bars 96-100 and the band plays it

v1 is the SKELETON: every voice is one note at one rate (with an accent on its octaves below), nothing else. There
are no fills, no lead, no words and no tuning yet: the notes are equal-tempered and the pulses are not (the fives
are a just minor third, 16 cents wider than the guitars' A flat).
"""
import json
import math
import os

OUT = os.environ.get("C10T14_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t14.yaml"))
F3 = 440 * 2 ** ((53 - 69) / 12)                 # 174.614 Hz
OCTAVES = 6
BPM = round(60 * F3 / 2 ** OCTAVES * 3 / 4, 4)    # a pulse every three sixteenths is F3, six octaves down
BAR = 16
# the three drums of the chord: the album kit's rack toms are already tuned to it. piece: period in sixteenths
DRUMS = {"t1": 3, "t2": 4, "t3": 5}
# the rolls: velocity ; dB a stroke loses for each octave of speed (3 dB an octave keeps the roll level from the
# held chord to the counted strokes: benched raw, every bar of the first ten within 1.1 dB) ; the same for the F
# tom, whose line stood 9.5 dB under the other two in the held chord (4.5 now) ; bars the chord is held at each end
ROLL = os.environ.get("C10T14_ROLL", "0.8;3;2.2;1")
FORM = [("held", 16), ("unwound", 96), ("counted", 240), ("minor", 240), ("sixth", 240), ("fourth", 240),
        ("common", 128), ("home", 240), ("wound", 96), ("one chord", 64)]
# (The toms' fader, C10T14_TOMS, is -1.5 dB. At the kit's usual 4 dB the three drums alone read as loud as the whole
# band in the finished file (-12.0 against -12.4 dB, K) and the song had 2 dB of dynamics from end to end.)
# v2 (chirper-alpha, whole song): THE BAND TUNES TO ITS OWN RHYTHM, AND THE RULE GETS A TUNE.
# (1) TUNED. The pulses are pure and the instruments were not: the fives are an A flat 16 cents over the guitars',
# the fifteens a D flat 14 cents over, the fours a C 2 cents over and the nines a B flat 2 cents under. The song
# now carries its own tuning: each note is the note its period says, to the cent. F is where it was; the two
# wheels not yet used are in the scale too (every 7 a D 33 cents sharp, every 11 a G flat 51 sharp), so a later
# round can write them as D and G flat. The kit's toms are not notes to the engine, so the A flat and C toms are
# retuned in the song's kit. Under distortion that is more than a nicety: the difference tones of a pure
# A flat, C and F (12:15:20) are 3, 5 and 8 of the same unit, which are A flat, F and D flat again, the song's
# own notes, where the tempered chord's fall between and beat. Empty: v1's equal temperament.
TUNED = os.environ.get("C10T14_TUNED", "1")
# WHAT THE TUNING CAN AND CANNOT DO, measured: on a sine every note lands within 0.3 cents of its pulse's note, and
# the bass within its own 4. The album's guitars are alive: a held string grows a vibrato of a fifth of a semitone
# at 5.3 Hz, every note is struck up to 5 cents off, and a saturated amp smears a chord's lines (the A flat pair
# alone, held, has a quarter of its energy within 5 cents of its note). Their average moves to the pulse's note;
# their life stays. TRIED AND NOT KEPT: the last chord on the same six rigs with the vibrato and the random
# detune off (six extra tracks): the lines were no sharper (share within 5 cents 0.14-0.55 either way), so the
# smear is the amp, not the vibrato. The last chord's A flat is therefore given to the one voice that can sing a
# single note over the band: the tune's last note (below).
# ratios over F for the eleven keys above it: G flat (the 11s), G, A flat (the 5s), A, B flat (the 9s), B, C (the
# 4s), D flat (the 15s), D (the 7s), E flat, E. The unused keys are plain five-limit.
JUST = ["12/11", "9/8", "6/5", "5/4", "4/3", "45/32", "3/2", "8/5", "12/7", "9/5", "15/8", "2/1"]
# (2) THE TUNE. v1 had no line. Under the rule a line needs no pitches written down: A NOTE LASTS AS LONG AS ITS
# PERIOD, so the tune is a list of lengths and the rule supplies the notes (two octaves over the drums' own:
# 3 is the F over the stave, 6 the F below it, 12 the F below that; 4, 8, 16 are C; 5, 10 are A flat; 9 is B flat;
# 15 is D flat). It therefore speeds up as it climbs and slows as it falls, like anything shorter being quicker.
# Every phrase is 60 sixteenths, one meeting of the three pulses.
#   A  12 8 6 5 4 3 4 5 5 8     up two octaves from the low F, each note quicker than the last, and half way back
#   B  3 3 4 5 6 8 10 9 12      down from the top, slowing, home to the low F through B flat
#   C  15 10 6 5 4 3 4 5 8      the same climb from the low D flat ('sixth')
#   D  3 4 5 6 5 6 10 6 15      and down to it
#   E  9 15 12 9 15             the quiet middle: B flat, D flat, F, slow and low
#   G  6 7.5 9 6 7.5 9 15       the same notes an octave up at twice the speed (a D flat of seven and a half)
#   S  3 4 5 6 7 8 9 10 11 12  THE WHOLE SCALE OF THE RULE, once, as the tune's last word: every period from three
#                              to twelve in order, so it falls two octaves and slows as it falls, and it passes
#                              through the two wheels the band never plays: the seven (a D a third of a semitone
#                              sharp) and the eleven (a G flat a quarter-tone sharp). It is 75 sixteenths, so its
#                              last note, the low F, is reached as the drums begin to wind up.
# In 'common' everything is C, so the tune can only change octave, and each octave is twice as fast: 16, 8 8,
# 4 4 4 4, then eight 2s, twice: the wind-up of the last bars, on a guitar, two minutes early.
# The second time a phrase comes round ('sixth', 'home') every note of eight or more is halved: two notes an octave
# up in the same time. The lead's echo is three sixteenths: by the rule, an F.
# the lead's track gain ; its velocity ; the echo's mix. Empty: no tune (with TUNED left on, the tuning alone).
TUNE = os.environ.get("C10T14_TUNE", "-1.5dB;0.85;0.18" if TUNED else "")
PHRASE = {"A": [12, 8, 6, 5, 4, 3, 4, 5, 5, 8], "B": [3, 3, 4, 5, 6, 8, 10, 9, 12], "C": [15, 10, 6, 5, 4, 3, 4, 5, 8],
          "D": [3, 4, 5, 6, 5, 6, 10, 6, 15], "E": [9, 15, 12, 9, 15], "G": [6, 7.5, 9, 6, 7.5, 9, 15],
          "S": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          "climb": [16, 8, 8, 4, 4, 4, 4] + [2] * 8}
NOTE_OF = {3: "F5", 6: "F4", 12: "F3", 2: "C6", 4: "C5", 8: "C4", 16: "C3", 2.5: "Ab5", 5: "Ab4", 10: "Ab3",
           4.5: "Bb4", 9: "Bb3", 7.5: "Db4", 15: "Db3", 7: "D4", 11: "Gb3"}
# v3 (chirper-two, instrument round: the held-chord rig): THE HELD CHORD STANDS STILL.
# v2's handoff: "a held chord on these rigs is a smear whatever the tuning ... an instrument round could give this
# song a held-chord rig that stands still ... and then the tuning would be heard; do not just turn the vibrato off,
# that was tried". Benched again, each rig alone on one held chord, 0.5 to 3.5 s after the stroke: the share of the
# energy from 80 Hz to 1.5 kHz that lies within 5 cents of the chord's own notes and their harmonics.
#   the wall on F2, A flat 2, C3 (the 'minor' meetings)    as written 27.6%   vibrato off 65.6%   and random detune off 75.7%
#   the F pair's rig on F1, C2, F2 (the last chord)        15.0%              66.8%               73.5%
#   the A flat pair's rig on A flat 2, C3, F3 (the same)   26.9%              61.8%               65.7%
#   all six on the last chord                              24.9%                                  78.4%
# So it is the vibrato after all, not the amp. On the m8 string the pitch's modulators are, in order, the pick's
# bite (0), the random detune (1) and the vibrato (2); with number 0 off instead, the share does not move (13.5%).
# And once the strings are still the tuning shows: the same still wall on the same chord in equal temperament has
# 59.6% on its lines, because there what the amp makes of three notes (their sums and differences) falls between
# them; tuned, it falls on them. Also benched on the still wall, and not kept (the chord's share moved 2 points at
# most): the string's second plane off, the plate off, half the amp's gain.
# WHO STANDS STILL. The wall pair plays nothing but held chords in this song, so its rig is simply still. The other
# four guitars chug, and a chug is over before a vibrato begins (380 ms); their strokes keep their life (each one
# struck up to 5 cents off). Only the last chord is held on them, seven seconds of it: that one chord moves to four
# more tracks, the same rigs standing still, so the band's chord is the chord the drums wound up to, note for note.
# THE CHORD'S THIRD. v2 gave the last chord's A flat to the tune's last note, and in the finished chord that one
# note is two thirds of everything between 250 Hz and 1 kHz (read against the records, by part). The lead's vibrato
# is wider than the rigs' (0.3 of a semitone at 6 Hz from 200 ms), so over seven seconds the chord's third was the
# least still thing in it: at the written A flat 4 the finished chord had a line 26.7 dB under its strongest. So
# the tune's last note, and only that one, goes to a fifth track: the same lead, holding still. Every other note
# of the tune keeps its vibrato: a line is sung, a chord is held.
# AND THEN THEY CAN BE TUNED. With the strings still, where each one sits can be read to a tenth of a cent, and
# the album's guitar string plays SHARP of the note it is given, more the higher (each note alone and still,
# harmonics 2 to 10, cents over the tuned note): the wall B flat 1 +3.5, F2 +3.9, C3 +4.6, F3 +4.9; the F pair's
# rig F1 to F2 +1.8 to +3.2; the A flat pair's A flat 2 +2.9, C3 +3.9, F3 +4.4; the lead F3 +3.3, A flat 4 +5.4,
# F4 +6.2, C5 +7.4. (The bass: +0.7. A sine: 0.3. It is the string, not the tuning; not its pick's bite and not
# its stiffness either: with each off the lead's A flat 4 reads +5.4 and +5.0. A bead for the engine.) So each
# still rig is tuned down by what it reads, and the held chords stand on the pulses' own notes: after the trim
# the lead's A flat 4 reads 0.0 and the wall's F2 -0.5.
# the strings' setting ; cents each still rig is tuned down (the F pair : the A flat pair : the walls : the lead),
# empty for none ; 'lead' if the tune's last note stands still too. Empty: v2.
STILL = os.environ.get("C10T14_STILL", "synth.pitch.mod.2.amount=0 synth.pitch.mod.1.amount=0;2.7:3.7:4.1:5.4;lead") if TUNED else ""


# v4 (chirper-one, whole song): THE DRUMMER FILLS, AND THE FILL IS THE CYCLE. The song had no fill anywhere (v1, v2
# and v3 all list it). Under the rule a fill needs no invention: twice as fast is the octave above, so the three
# drums of the chord (F every 3, C every 4, A flat every 5, which meet every 60 sixteenths) can say the WHOLE cycle
# in half the time or a quarter of it and still be playing their own notes. Every 1.5, 2 and 2.5 they meet after
# 30; every 0.75, 1 and 1.25 after 15. So a fill is the cycle in miniature, landing on the meeting it comes before:
# the band has taken 60 sixteenths to get there, the drums take 15. Two of them join end to end are the song's own
# beginning and end at one-fortieth the size: 30 then 15 (twice as fast, then four times) is the wind-up, an octave
# a step, as the last minute winds the drums up to the chord; 15 then 30 is the unwinding the song opens with.
#   0:55.8  the cycle in 15, into the meeting where the tune comes in (0:57.7)
#   1:06.8  the wind-up, 30 then 15, into 'sixth' (1:12.3)
#   1:36.2  the unwinding, 15 then 30, falling away into the quiet middle (1:41.6)
#   2:37.6  the cycle in 30, at the middle of 'home'; from 2:48.6 the drums are back at the band's own speed (v1)
#           and at 2:55.9 they wind up for good: so 'home' has them at twice the speed, then at speed, then gone
# The snare leaves for the fill, and the cymbal too while the drums go four times as fast (the feet keep the F
# pulse). With no cymbal through a whole fill the song read 10 to 14 dB under the records at 8-16 kHz for up to five
# and a half seconds: now never for more than 1.9. A stroke loses what the rolls'
# strokes lose for each octave of speed (C10T14_ROLL), so a fill is as loud as the counted drums, and it swells
# toward the meeting (or fades, where it unwinds). No other note is changed. Nothing in the quiet middle or in
# 'common' (there every voice is on C: only the C drum could speak).
# AND ONE DRUM WINDS UP ALONE, in 'common', where every voice is on C and only the C drum may speak. In the last
# bar before 'home' (2:24.7) v2's tune says eight 2s, the quickest thing a guitar can say here; the C drum goes on
# from there: eight strokes a sixteenth apart, eight at half that, eight at a quarter, eight at an eighth, and then
# its own note (131 strokes a second, the rate it was rolled at when the song began) until the bar line: six
# octaves in one bar, the song's ending a minute early and on one drum, and it lands on 'home'.
# velocity at the far end ; at the near end ; the fills, | between: SECTION+SIXTEENTH it lands on = the speeds in
# order ; the toms' gain in a fill, dB ; the one drum's wind-up: SECTION+SIXTEENTH it lands on : the drum : its
# first period in sixteenths : its gain, dB (empty = none). "" = v3. It is on only while STILL, TUNE and the toms'
# fader are, so each older switch still gives what it gave.
FILLS = os.environ.get("C10T14_FILLS", "0.6;0.92;minor+120=4|minor+240=2,4|sixth+240=4,2|home+120=2;0;common+128:t2:1:5.5") if STILL and TUNE and os.environ.get("C10T14_TOMS", "x") else ""

# v5 (chirper-alpha, instrument: THE LEAD). The tune's guitar is the library's `m8-lead-guitar` as it comes. Read alone
# (raw, 'sixth') it is all middle: of its own power 27% lies at 500 Hz-1 kHz, 45% at 1-2 kHz, 25% at 2-4 kHz, and
# ONE PERCENT above 4 kHz, where a pick is heard. In the quiet middle, on its lower notes, half of it is 500 Hz-1 kHz.
# v3's read against the album's eleven records found the same from the other side: wherever the tune plays the mix
# stands 2.8 dB over the records at 500 Hz-1 kHz ('sixth') and 4.6 over in the quiet middle, and the tune alone is 56%
# and 85% of that band, while 4-8 kHz and 8-16 kHz stand under. A lead that is a box and no pick.
# So, on the lead's track, after its amp, speaker, echo and room: THE BOX OUT (a peak at 700 Hz) and THE PICK IN (a
# shelf from 4 kHz). And THE FADER RIDES: v2 wrote -1.5 dB on the quiet middle's notes and v3 measured that it does
# nothing (a note's gain sits ahead of a saturated amp); the same 1.5 dB is now a ride on the fader through
# 'fourth', where it is a level. No note changes; the amp, the string and the vibrato are the library's.
# Benched first and not kept (the lead alone in both windows, and the mix read again with it):
#   the speaker's microphone at the cone's centre (0.15): 4-8 kHz +1.0 dB on the lead, nothing in the mix
#   the amp's mid at 0.45: 500 Hz-1 kHz -0.5 in the mix, but 1-2 and 2-4 kHz, already over, +0.2 and +0.4
#   the engine's modern speaker, microphone 0.1, with the box out: 500 Hz-1 kHz -1.6, but 2-4 kHz 1.1 further over
#   a gentler pair (-3 dB at 750, +3 dB at 4.5 kHz): half of this
# the box (Hz : q : dB) ; the pick (shelf Hz : dB) ; the fader's ride through 'fourth', dB ; the loudness target
# (a quieter lead makes the file measure quieter: at -10 every bar without the tune came out 0.4 dB louder, at
# -10.25 0.13; 1.12 dB of gain for each dB of target). "" = v4.
LEAD = os.environ.get("C10T14_LEAD", "700:0.8:-5;4000:5;-1.5;-10.36") if FILLS else ""


def still(patch, who):
    """The patch standing still, tuned down by its own sharpness. who: 0 the F pair, 1 the A flat pair, 2 the walls, 3 the lead."""
    if not STILL:
        return patch
    setting, trims, _ = STILL.split(";")
    down = f" synth.pitch.value={-float(trims.split(':')[who]) / 100:.3f}" if trims else ""
    return f"{patch} {setting}{down}"
T = {}


def halved(phrase):
    """Every note of eight sixteenths or more becomes two an octave up: the same time, twice the speed."""
    return [x for p in phrase for x in ((p / 2, p / 2) if p >= 8 else (p,))]


# v6 (chirper-one, palette: the part the song lacks): THE TWO WHEELS THE BAND NEVER PLAYED. Three, four and five are
# the chord, and each is a drum: the kit's three toms are tuned to the notes their rolls are. Nine and fifteen have
# a section each. Seven and eleven had no player: v1 left them out, v2 tuned the song for them (every 7 is a D 33
# cents sharp, 12/7 over F; every 11 a G flat 51 cents sharp, 12/11) and let the tune touch each once, in its last
# scale. Now they are drums too: TWO TABLAS, for the second half of 'home' (2:41.3-2:55.9), where the song says
# "everything". One is struck every seven sixteenths on the left and is tuned to that D; the other every eleven on
# the right, tuned to that G flat. By the rule they could be nothing else. A tabla, because its head is loaded so
# that its overtones are in tune with it (1 2 3 4 5): a drum whose note is heard, so a note a third of a semitone
# from any key is one note and not a clang; the dayan comes tuned to D as it is, and here it is the seven's D. (In
# the Time Of keeps its tala on one; no other song has two, tuned as counts.) Like every voice here each accents
# its own register downward, with the drum's own
# strokes: the rim stroke (na, which rings an octave over the head's note) on plain counts, the open stroke (tin)
# on every second, the deep open centre (tun) on every fourth. They come in together on the meeting the drums'
# fill lands on, strike through the tune's last scale, which says their two notes by name (the seven's at 2:50.8,
# the eleven's at 2:55.0), strike together once more at 2:50.7, and stop where 'home' ends. (Through the whole of
# 'home' two marimbas on these counts cost the return its likeness to 'minor'; benched. With 'marimba' in the
# first field the wheels are marimbas again, on D5 and G flat 5 with their octaves: the first build of this round,
# set aside because Running Total already counts on a marimba all through.)
# the patch (a kit ending in -kit: bols; anything else: notes) ; the two tracks' gain ; how far left and right ;
# the section + the sixteenth they enter on ; velocity ; the loudness target. "" = v5.
WHEELS = os.environ.get("C10T14_WHEELS", "tabla-kit;-10dB;0.45;home+120;0.9;-10.36") if LEAD else ""


def tune(a, phrases, vel, **more):
    s = a
    for ph in phrases:
        ph = halved(PHRASE[ph[:-1]]) if ph.endswith("'") else PHRASE[ph]
        assert sum(ph) in (60, 64, 75), ph
        for p in ph:
            n = NOTE_OF[p]
            # the rule, checked: this note's frequency times its length is a whole number of octaves from F3 x 3
            pc = "C Db D Eb E F Gb G Ab A Bb B".split().index(n[:-1])
            ratio = eval(("1/1" if pc == 5 else JUST[(pc - 5) % 12 - 1])) * 2 ** (int(n[-1]) - 3 - (pc < 5))
            assert abs(math.log2(ratio * p / 3) - round(math.log2(ratio * p / 3))) < 1e-9, (n, p)
            add("tune", s, p - 0.3 / 0.96, n, vel, **more)
            s += p
    return s


def starts():
    at, s = {}, 0
    for name, n in FORM:
        at[name] = s
        s += n
    at["end"] = s
    return at


# v7 (chirper-two, palette: the part the song lacked): THE DRUMMER PLAYS THE WHOLE CHORD.
# In this song three, four and five are drums: three toms, when it begins and when it ends. In between the band has
# them, and the kit kept two of the three: the foot has the threes (F), the hands have common time (C). THE FIVES HAD
# NO DRUM: from the moment the A flat tom hands them over (0:28.3) they were two guitars and nothing else, the third
# of the chord with no stroke under it. Now they have one: three temple blocks, tuned to A flat in three octaves, on
# a new track. Like every voice here the part marks its count's octaves, and here the rule says how: a pulse every
# ten is the A flat an octave under a pulse every five, every twenty the octave under that. So the block struck every
# five is A flat 6 (1676.3 Hz, a pure minor third over F6), every second stroke is the block an octave lower, every
# fourth the one two octaves lower. Each block is tuned to how often it is struck.
# WHERE: wherever the A flat pair chugs the fives and no tom has them: 0:28.3-0:43.0 (the last half of 'counted'),
# 'minor', 'sixth', and 'home' until 2:48.6, where the A flat tom comes back and takes them: 156 strokes. One drum
# has the fives at a time. Not in the quiet middle (it has no fives), 'common' (everything is C) or the last chord.
# THE BLOCK is the library kit's wood block (a triangle at the note through a band-pass there, three milliseconds of
# stick) at the fives' notes, as three pieces of this song's kit: no library patch is touched. No other song on the
# album strikes a wood block.
# MEASURED (raw, seed 0). Alone the three read 1677.4, 839.1 and 419.2 Hz (+1.1, +1.9, +0.3 cents) and fall 20 dB
# in 31, 33 and 60 ms. In 'minor' each stroke lifts what is already within a third of an octave of its note by a
# median 4.1 dB (the high block), 5.8 and 7.2; in 'home' 4.4, 4.0 and 8.0. FIRST TAKE, all three at the kit's own
# -8 dB: the high block lifted its band 2.9 dB and half its strokes less than 3 (it sits where the tune and the F
# guitars are): it is 3 dB higher now (its peak rose 1.5: the drum bus clips at -13 dB and it touches that). A
# stroke's own tenth of a second is 8.0 dB under the mix's (the A flat guitars' strokes 7.8 each, the cymbal's 7.4).
# The loudness target goes from -10.36 to -10.333 so that every bar without a block keeps its gain (within 0.011 dB).
# the block track's gain ; where the blocks stand (pan) ; the three blocks' notes in Hz, for a plain stroke : every
# second : every fourth ; velocity ; the loudness target ("" = unchanged) ; the three blocks' own gains, dB. "" = v6.
FOOT = os.environ.get("C10T14_FOOT", "8dB;-0.3;1676.3:838.15:419.07;0.9;-10.333;-5:-8:-8" if WHEELS else "")
# v8 (chirper-three; instrument round: the four chord guitars' rig, the F pair and the A flat pair, and their
# still twins in the last chord). Read first against the eleven records (raw, 'minor' and 'home'): against the
# records' guitars the four stood 6.3 and 5.0 dB SHORT at 120-250 Hz and 4.7 and 6.2 OVER at 500 Hz-1 kHz, and held
# 36 to 38% of the mix's 250-500 Hz, where the mix stood 2.0 and 3.1 over. Three moves, each from that read:
#   the amp's tight filter 220 -> 180 Hz (body: the low string's own octave is let into the amp);
#   the 2.5 dB lift at 700 Hz on each track taken out (it was the box);
#   in its place 2 dB off at 330 Hz on each track (on the tracks, so the wall guitars keep what they had);
# and 0.45 dB on the four faders, so that the guitars stand where they stood against everything else.
# the amp's tight filter, Hz ; the band on each of the four tracks, in place of the 700 Hz lift ; dB on the four
# faders ; the loudness target ("" = unchanged). "" = v7.
RIG = os.environ.get("C10T14_RIG", "180;peak cutoff=330 q=1.2 gain=-2dB;0.45;-10.386" if FOOT else "")
# v9 (chirper-one, palette): THE BACKBEAT IS A C, AND NOW THE SNARE IS. The rule of this song is that what strikes
# every p sixteenths plays the note whose period is p, and its drums obey it: the three toms are tuned to the notes
# their rolls are (v2), the two tablas to the sevens' D and the elevens' G flat (v6), the three blocks to the fives'
# A flat (v7). The header says "the backbeat is a C". The snare that plays it was the album kit's, as it comes: its
# strongest line (the drum alone, before the kit's bus) stood at 245.0 Hz, a B: a tritone over the song's F and 116
# cents under its C, on every one of its 124 strokes. (The kit writes the head as A3, which this song's tuning reads
# as its own A, 218.27 Hz; the two heads and the air between them put the drum's line 11% over the head's.)
# THE SWAP: the song's own snare in place of the kit's (the staple all seventeen songs share). The same drum, the
# same heads, wires, shell and stick, with the batter head 118 cents higher: its line is 262.4 Hz, 3 cents over the
# song's C4 (261.92). And its body follows it: the kit lifts 5 dB at 200 Hz, under the old line; here that is 1 dB
# at 262 Hz, because the line now lies in 250-500 Hz where this song already reads over the records, and 3 dB comes
# off at 650 Hz, where the kit is furthest over the records' drums. The piece's own gain is set so the snare alone
# is as loud as it was (K, within 0.1 dB).
# the batter head (a key number: this song's tuning table reads it) ; the resonant head, times the batter ; the
# shell, Hz ; its level ; the bands after the 150 Hz high-pass (| between) ; the piece's gain, dB ; the loudness
# target ("" = unchanged). "" = v8 byte for byte.
SNARE = os.environ.get("C10T14_SNARE", "m58.18;1.5;500;0.3;peak cutoff=262 q=1 gain=1dB|peak cutoff=650 q=1 gain=-3dB;0.65;-10.365" if RIG else "")
# v10 (chirper-alpha; instrument round: THE KICK). The foot plays the threes, and the threes are an F: the last
# drum not on its note (v9: its thump is an A, a major third over the F, in a minor song). And the album's kick,
# read against the kicks in the eleven records' drum stems, has nothing at 90-120 Hz (-28.9 dB of its own 35-250
# Hz; theirs -13.6) and rings 84 ms to 20 dB down (theirs 37 to 49).
# THE RULE'S NOTE WAS TRIED FIRST AND THE BASS SAID NO: the drum on F1 is on the bass's own line, and two tones on
# one line add by phase: stroke by stroke the level at 30-60 Hz went from a spread of 2.4-3.1 dB to 4.7-5.4 (full
# renders, both seeds), the weakest stroke 0.5 to 1.4 dB weaker. So the DRUM goes to the chord's own third, a pure
# A flat (52.38 Hz, 6:5 over the bass; kit pieces are not retuned, so it is written as a key number), and the F IS
# THE CHEST: a bare sine on F2, 90 ms, on its own track with every kick stroke, straight to the mix (not a layer of
# the kick's patch: its drive is one ceiling; not through the kit's bus: its clip holds the kick's top). The kick
# alone then reads -16.1 at 90-120 Hz and 49 ms. The click's eq goes 10 -> 11.5 dB for what the lower drum lost.
# In 'common' the foot plays twos, a C: the chest on C2 there falls under the hole and on the bass's C (benched:
# 60-120 Hz 1.1 dB further under), so the seventh field is empty and the chest is F2 all through.
# the drum's note ; the kick's fader, dB ("" = as it was, 2) ; the chest's note ("" = no chest) ; its gain ; its
# decay, ms ; the kick's click, dB at 4.5 kHz on its track ("" = as it was, 10) ; the chest's note in 'common',
# where the foot plays twos and the twos are a C ("" = the same note all through) ; the loudness target ("" =
# unchanged). "" = v9.
KICK = os.environ.get("C10T14_KICK", "m32.1564;;F2;-3dB;90;11.5;;-10.388" if SNARE else "")
# v11 (chirper-three, section round: 'sixth', 1:12.3-1:41.6, the map's first flag "static, little new"): THE BAR IS
# A NOTE TOO, AND THE D FLAT IS A SEMITONE OVER IT. 'Sixth' is the section of the fifteens: the D flat that sounds
# every bar less a sixteenth, "so the band's biggest stroke slides a sixteenth earlier every bar and is home after
# fifteen". Slides against what? The bar. And by the rule the bar is a note as well: every sixteen is a C. Fifteen
# against sixteen is D flat against C, the semitone (16:15), and the fifteen bars the two take to meet again are
# one beat of that semitone: the section is as long as its own interval. Until now only one of the two was played.
# The D flat had both wall guitars and the bass; the bar line had a slightly louder cymbal; and the fifteens were
# one of the two counts in the song still without a drum (the nines are the other).
#   THE FIFTEENS GET THEIR DRUM: the kit's floor tom, tuned a pure fifth under the A flat tom (D flat 2, 69.8 Hz),
#     on every fifteen. With the three toms of the chord that is D flat, A flat, C, F: the section's own chord.
#   THE BAR GETS ITS DRUM AND ITS NOTE: the C tom on every bar line (the fours' drum, two octaves down in time),
#     and the LEFT wall guitar leaves the D flat for C on every bar line. The right wall keeps the D flat, as it
#     will through the quiet middle that follows, so its fifteens run unbroken from 1:12.3 to 2:11.
# So the two slowest things in the section are both struck, by a drum and a guitar each: together at 1:12.3 (where
# the crash stands for the bar's drum), then the D flat a sixteenth before the bar line, then two, three ... half a
# bar apart at 1:27, and closing again (under the fill) to meet on the first stroke of 'fourth'. The gap can be
# counted. (A first build rested the china on every bar line the C tom takes: 0.8 dB off the mix at 8-16 kHz,
# where the song is short. The left hand is free there, so it has the C tom and the china keeps its quarters.)
# THE CHORD: C3 and C4, read against C4 alone and C4 with C5 (raw): only with the C3 does the wall give the mix
# anything at 120-250 Hz, where 'sixth' stood 2.4 dB short of the records (0.6 of it back). The band now plays the
# whole of D flat, F, A flat, C; until now the C was the kit's alone.
# (Held, that C3 and the right's D flat 3 are 8.73 Hz apart, which is the section's 29.3 seconds 256 times over.
# I looked for that beat in the two walls alone and in the mix and no line stands out there: every stroke restarts
# its strings. The round claims the gap you can count, not a flutter.)
# THE DRUMS' LEVEL: at the kit's own level a stroke's first 80 ms stood 10.2 (floor tom) and 8.0 dB (C tom) under
# everything else; with 4 and 2 dB on the strokes they stand 7.9 and 7.1 under, where the song's blocks stand (7.8).
# THE HANDS. The right hand keeps the china's quarters and the left has the backbeat, so the left is free on every
# bar line (the C tom) and on all but two of the fifteens (the floor tom). On those two (1:19.7 and 1:34.3) the D
# flat lands on a backbeat: there the right hand leaves the china for the floor tom, and it leaves it once more
# under the crash at 1:12.3. In the fill before 'fourth' the C tom is already rolled, so it has the bar lines
# there; the floor tom keeps its fifteens under it. No other note changes.
# the bar's chord on a wall guitar ("" = both walls stay on the D flat) ; which wall, l or r ; the floor tom's
# note, a key number ("" = no drum on the fifteens) ; its velocity ; dB on its strokes ; the bar line's drum ("" =
# none) ; its velocity ; dB on its strokes ; the loudness target ("" = unchanged). "" = v10 byte for byte.
SEMITONE = os.environ.get("C10T14_SEMITONE", f"C3,C4;l;m{53 + 12 * math.log2(8 / 5) - 24:.4f};0.85;4;t2;0.8;2;" if KICK else "")
# v12 (chirper-alpha; whole song: 'minor' and 'home', the two F minor sections): THE BASS GOES ROUND THE CHORD. By
# the rule the threes are F, the fours C and the fives A flat, and every hand in the band keeps one wheel. The bass
# kept one too (F every six: 80 strokes of one note). Now it is the one player who goes from wheel to wheel: in each
# cycle of sixty it plays F every six with the threes (four strokes), C every eight with the kit's hands (two), A flat
# every ten with the fives (two), changing only on a stroke the two wheels share; 24 + 16 + 20 is the sixty, so it is
# home on F as the cycle comes round. The chord is heard one note at a time, from the bottom, each at its own speed.
# THE BUS: the album's bass chain sits around the note the bass is on; left on F it put its 90 Hz lift under the A
# flat (the bass alone 2.1 dB hotter there, 1.3 on C). So the lane that moves it by section now moves it by the note
# (fourth field): the bass alone reads within 0.3 dB of v11's over each stretch.
# COST: under 60 Hz the two sections are 0.7 to 0.9 dB further short of the records (1.2 to 1.6 while the bass is
# up); the scorer's 83 Hz band, the F's second line, 0.7 further under.
# NOT the A flat an octave down: 51.9 Hz is the kick's own line (52.4), and the strokes' spread at 30-60 Hz went
# 2.7 -> 5.6 dB (v10's finding from the other side).
# the bass's round of the chord, one cycle of sixty: note : its stroke's period : how long it stays (sixteenths),
# in turn ; the sections it is played in ; the loudness target ("" = unchanged) ; where the bass's bus stands for
# each of those notes, semitones over F ("" = it stays on F, the section's ground). "" = v11.
TURN = os.environ.get("C10T14_TURN", "F1:6:24,C2:8:16,Ab2:10:20;minor,home;;0,7,15" if SEMITONE else "")
# v13 (chirper-one, whole song: its frame): THE SONG IS COUNTED. The title says what the piece does (a chord slowed
# until it is slow enough to count) and nobody in it counted: twelve rounds and no voice. Under the rule a lyric
# needs no writing, as the tune needed no pitches: A NUMBER, SUNG, LASTS AS LONG AS IT SAYS, on the note of that
# length. 'Three' is three sixteenths long and an F, 'four' four and a C, 'five' five and an A flat. The voice
# sings only where the drums are alone, three places:
#   down    0:04.5-0:13.7, over the rolls unwinding: 'three four five six seven eight nine ten eleven twelve',
#           the tune's last phrase (S, the whole scale of the rule) as words. Each number is longer and lower than
#           the last, so the count slows as it falls, two octaves, with the drums; it is 75 sixteenths, and the
#           drums are in tempo as 'twelve' ends. Slow enough to count
#   named   0:13.7-0:21.0, the three drums alone in tempo: 'three four five', five times. Each drum's stroke is
#           named for exactly as long as it lasts, on its own note an octave over the drum; 3 + 4 + 5 is twelve,
#           an F, and five twelves are the sixty. Then the band comes in and the voice has said what it will play
#   up      2:57.8-3:06.9, over the rolls winding up: 'twelve eleven ten ... three', from the moment the tune's own
#           last note (its 'twelve', the low F) ends: quicker and higher with every number, two octaves, to the F
#           a moment before the band's last chord
# Two voices an octave apart (a man, and the same voice with a shorter tract), on the tune's own notes for those
# lengths and the octave under them; the seven is the D a third of a semitone sharp and the eleven the G flat a
# quarter-tone sharp, by the song's tuning, as on the tabla wheels. THE DRUMS MAKE THE ROOM: the song's quiet frame
# is its contrast with the band, and a first build with the voices 2 dB under the drums made those passages 2 dB
# louder (the scorer's level range 5.3 -> 4.0 dB). So the voices are 3 dB lower and the toms' fader comes down
# 1.6 dB while a voice counts: each passage is within a decibel of where it was.
# the voice's patch ; its fader ; the second voice's tract, an octave over the first ('' = one voice) ; its fader ;
# their eq bands (| between) ; the reverb on them ('' = dry) ; their velocity ; sixteenths of breath between two
# numbers ; which of the three places are sung (down = the count as the drums slow, named = 'three four five' over
# the three drums alone, up = the count back as they wind up) ; the loudness target ('' = unchanged) ; dB on the
# notes of 'named' (its three notes are the voices' highest and loudest) ; dB the count back has gained by its last
# number (it climbs into drums that are getting louder) ; dB on the toms' fader while a voice counts ('' = none):
# the drums make the room, so each passage is as loud as it was. '' = v12.
COUNT = os.environ.get("C10T14_COUNT", "voice-hook synth.layers.0.diction=3 synth.layers.0.effort_tilt=1;-15dB;0.86;-21dB;hp cutoff=150;"
                       "reverb kind=hall decay=2.2s mix=0.14 predelay=30ms;0.85;0.4;down,named,up;;-4.5;3;-1.6" if TURN else "")
# v14 (chirper-two; whole song: its shape): THE QUIET MIDDLE IS QUIET. The header has called 'fourth' (1:41.6-2:11.0)
# "the quiet middle" since v1, and it was played by the two loudest rigs in the song: the wall guitars, one chord
# each, with the snare on the backbeat. Measured on v13's finished file it stood 2.4 dB under 'sixth' before it and
# 2.8 under 'common' after it: the song had no valley, and its plainest, loudest stretch ('common', everyone on C)
# came in on nothing. Now:
#   THE NINES AND THE FIFTEENS ARE A CLEAN PAIR. The walls rest for the section; the same 43 strokes (B flat every
#     nine on the left, D flat every fifteen on the right, the same lengths) go to two clean guitars, an octave up
#     (octaves are free), strummed over 20 ms. It is the song's first clean guitar. Under this song's rule a clean
#     chord must stand on its note, so the library's ct-clean is made still: no chorus, no vibrato, no random detune,
#     and `tune_sounding` (the string on its note). Its six notes read -0.9 to +0.3 cents from the just B flat, F,
#     D flat and A flat (as it comes: +1.9 to +4.5). The pair's last B flat stops at the bar line (the wall's rang two
#     sixteenths on under the band's first C).
#   THE BACKBEAT GOES TO THE RIM: the snare's 30 strokes there are the kit's cross-stick (its own knock and wood, not
#     tuned: overriding its two frequencies changed nothing I could measure), 3.7 dB under everything else in its
#     first 60 ms where the snare stood 2.0 over.
#   THE FOOT, THE HAT AND THE TUNE COME DOWN: 5 dB off the kick's (and its chest's) strokes, 2 off the hat's, 3 more
#     on the lead's ride. The bass is as it was, so the middle now rests on it.
# NO NOTE'S TIME OR PITCH CLASS CHANGES: the rule is played as before, by other hands.
# MEASURED (raw, seed 0, 'fourth'): the guitars -25.9 -> -29.0 dB K, the lead -27.2 -> -30.2, the kit -26.7 -> -31.5,
# the bass -29.6 as it was; the mix -21.1 -> -23.9. A clean stroke falls 11.2 (the nines) and 15.3 dB (the fifteens)
# before the next one; the walls' fell 8.2 and 11.5: the two wheels are plainer as strokes.
# FINISHED (three seeds): 'fourth' 2.6 dB quieter (K); it stands 5.0 to 5.1 under 'sixth' and 5.3 to 5.5
# under 'common' (v13: 2.4 to 2.5 and 2.8 to 2.9). The target -10.388 -> -10.62 (the quieter middle made the file
# measure quieter and the master lifted every other bar 0.37 dB; 1.6 dB of gain for each dB of target): every other
# section is v13's within 0.005 dB.
# the clean pair's patch ; its fader ; semitones over the walls' chords (octaves are free) ; velocity ; its eq, band|band
# ('' = none) ; a reverb of its own ('' = none) ; dB on each stroke in 'fourth' of the kick and its chest : the snare :
# the hat ; the backbeat's piece there : overrides on the kit for it : dB on its strokes ('' = it stays on the snare) ;
# dB more on the lead's ride through 'fourth' ; the loudness target ('' = unchanged). "" = v13 byte for byte.
CLEAN = os.environ.get("C10T14_CLEAN", "ct-clean fx.3.mix=0 synth.pitch.mod.0.amount=0 synth.pitch.mod.1.amount=0 synth.layers.0.tune_sounding=true strum=20ms;"
                       "7.3dB;12;0.9;peak cutoff=350 q=0.9 gain=-5dB|peak cutoff=2800 q=0.8 gain=3dB;reverb kind=hall decay=1.6s mix=0.1 predelay=20ms;"
                       "-5:-5:-2;ss::14;-3;-10.62" if COUNT else "")
# v15 (chirper-one; section round, w4, 1:33-2:05: the quiet middle, 'fourth', 1:41.6-2:11.0): THE MIDDLE IS COUNTED.
# v13 gave the song two voices that count only where the drums are alone, at its two ends; v14 made the middle quiet
# (two clean guitars, B flat every nine sixteenths and D flat every fifteen, a rim, a soft foot) and left "room" for
# the tune there to be something other than the distorted lead. The tune in 'fourth' IS those numbers: its notes
# last nine (B flat), fifteen (D flat) and twelve (F) sixteenths, with a quick turn of six and seven and a half
# between. So in the one place the band is slow and quiet enough, the voices come back and sing the tune as what it
# is: "nine, fifteen, twelve, nine, fifteen", each number as long as it says, on the tune's own note (the high voice
# an octave over), while the left guitar strums B flat every nine and the right D flat every fifteen. The lead
# rests on every note that is sung and answers with the quick turn, which has no whole number to say (seven and a
# half). Per half of the section: five numbers sung, five notes played, two sung. The count is no longer a frame:
# it is heard at the start, in the middle and at the end.
# which of each half's twelve notes are sung ; octaves over the tune's note for the low voice and the high ; dB on
# those notes ; how the two syllables of 'fifteen' share its fifteen sixteenths ; the loudness target ('' =
# unchanged) ; overrides on the voice's patch here ; the two faders ; the eq here, band|band (any of the last three
# puts the middle's singing on tracks of its own, said and said-high, so the frame's voices are not touched).
# "" = v14 byte for byte.
MIDDLE = os.environ.get("C10T14_MIDDLE", "0,1,2,3,4,10,11;0,1;0;4:11;;synth.layers.0.consonant_level=6dB;-15.5dB,-21.5dB;"
                                         "hp cutoff=150|peak cutoff=2500 q=0.7 gain=5dB" if CLEAN else "")
# v16 (chirper-zero; instrument round: THE THREE DRUMS OF THE CHORD, the toms on F, C and A flat; 4,361 strokes,
# none moved). The song is these three drums: rolled at their own notes they are its first chord, slowed they are
# its count, and nobody had given them a round. Read alone (lines.py, tom.py in the bench):
#   THEY WERE HALF BOX. The held chord had a fifth of its energy at 500 Hz-1 kHz (-7.2 dB re the whole; its three
#   notes' band, 90-220 Hz, -1.7) and nothing over 4 kHz (-36): a hum with a honk in it, and no stick. By part the
#   kit stood 8.4 dB over the records' kits at 500 Hz-1 kHz, the most on the album, and of the kit's pieces the
#   toms held the most of the mix there (-9.4 dB; the snare -12.1, the blocks -13.4).
#   THEY COULD NOT BE COUNTED. The album tom rings 1.3 s and here a stroke lands about every 0.16 s: where the three
#   arrive in tempo alone (0:14-0:21), a stroke had fallen 2.9 dB when the next landed.
#   THE THREE NOTES WERE NOT LEVEL in the held chord: F 2.0 dB under the other two.
# So, on the three drums only (the deep drum of 'sixth' is left): the head's upper modes roll off twice as fast
# (tilt -2 > -6: the box goes at the head, not with an eq); the head rings 0.55 s (1.3) and the amp 0.7 s (1.8);
# the stick is heard (its noise -66 > -50 dB, the 4 kHz band +2 > +5 dB). Fader -1.5 > +1 dB: the held chord is as
# loud as it was (K -24.2 > -24.1), the count 0.5 dB under where it was.
# overrides inside each of the three drums' patches ; the toms' fader ; the loudness target ('' = unchanged; the
# shorter drums measure quieter, and at v15's -10.62 the quiet middle, where no tom plays, came out 0.04 dB louder).
# "" = v15 byte for byte.
HEADS = os.environ.get("C10T14_HEADS", "synth.layers.0.tilt=-6 synth.layers.0.decay=0.55s synth.amp.d=0.7s synth.layers.1.level.value=-50dB "
                                       "synth.filters.1.gain=5dB;1dB;-10.66" if MIDDLE else "")
# v17 (chirper-one; whole song): THE THREE GATHER. The threes, the fours and the fives come round together every 60
# sixteenths, and the rule itself writes a figure there that nobody played: their LAST strokes before a meeting fall
# on three sixteenths in a row (the fives at 55, the fours at 56, the threes at 57: A flat, C, F, the chord going up),
# then two empty sixteenths, the meeting, two empty, and their FIRST strokes after it on three in a row (63, 64, 65:
# F, C, A flat, the chord coming down). The three drums the song is made of had left the band after 'counted'; now at
# each meeting inside 'minor', 'sixth' and 'home' that has no fill of its own they come back and say it, each on its
# own pulse (no new strike time: the block, the china and the kick already land there), and the guitars, the walls and
# the bass rest for those five sixteenths so that the kit gathers alone and the band lands on the meeting.
# In 'home' they gather from TWO strokes back: the fives at 50 and 55, the fours at 52 and 56, the threes at 54 and
# 57: A flat . C . F, A flat, C, F, the gaps closing (2, 2, 1, 1, 1): the wind-up in a second; and they leave the same
# way, slowing: the unwinding. The band rests the whole ten sixteenths there.
# where (section:meeting,meeting:strokes back|…; a meeting followed by < is gathered into but not left; strokes
# back 1 if not given) ; who rests from the first of those strokes to the meeting ('' = nobody) ; the last three
# velocities in (A flat, C, F) ; the meeting's (all three; '' = none) ; the first three out (F, C, A flat; '' = none)
# ; velocity off for each stroke further back ; the loudness target ('' = unchanged). "" = v16 byte for byte.
GATHER = os.environ.get("C10T14_GATHER", "minor:60,180|sixth:60,120,180|home:60,180<:2;gl,gr,dl,dr,wl,wr,bass;0.85,0.92,1;1;0.8,0.7,0.6;0.15;" if HEADS else "")
# v18 (chirper-three; whole-song round, 20 Nov). THE FIFTEEN BECOMES THE BAR. The song says a pulse and a note are one
# thing, and until now it said so with one tempo: whatever was struck, the count itself never moved. From 'common'
# (2:10.97, beat 268) to the end the sixteenth is 15/16 as long. So every pulse is 16/15 as fast, and by the song's
# own rule every note is 16/15 as high: a just semitone (111.7 cents), the step from C to D flat. One pulse crosses
# the change untouched. The D flat that 'sixth' and 'fourth' strike every fifteen sixteenths (1832.6 ms) is sixteen
# of the new sixteenths: it becomes the bar, and the bar-line chord of 'common', written C, sounds its D flat. The
# band comes in around a pulse that was already there and counts sixteen to it where it counted fifteen. 'home' is
# then the whole chord a semitone up and a fifteenth faster, the rolls wind up to the notes of the faster count, and
# the last chord stands a semitone over the chord the song opened on: the count went up, so the chord did.
# HOW: on the finished document. Each part that plays on both sides is parted at the change (its later notes go to
# NAME-up, appended last). A pitched part there keeps its written notes and takes a tuning of its own (the song's
# scale, every step times the ratio); the kit's tuned pieces (kick, snare, the three toms, the floor tom, the blocks,
# the two tablas) are retuned in song-local copies of their kits; cymbals and hat are not notes and stay. Positions,
# lengths and automation points from the change on are written 15/16 as far from it; the song's declared tempo stays
# one number. No stroke is added, dropped or reordered: 7,780 notes before and after.
# MEASURED (t14-r18): the bass's C of 'common' 69.832 Hz (written 69.846; the old C2 +111.4 cents); the kick's strokes
# there 229.00 ms apart (written 229.08; 244.35 before); the D flat pulse repeats every 1830 ms on both sides of the
# change, 139.64 Hz on the clean guitar before and 139.82 Hz on the wall pair after (written 139.69); each lifted
# part alone lies on its old self when moved down 110 to 116 cents (toms 110, guitars 110, lead 112, voices 112,
# snare 114, blocks 114, kick 116); the last chord's F, C and A flat, eight lines from F1 to A flat 5, within 3.1 cents
# of the written notes times 16/15 on the song's own seed. Everything before the change is v17: within 0.016 dB and -63 dB or lower on seeds 0, 11
# and 1 (not bit for bit: parting a track moves its later random draws). After it the same strokes are another take.
# THE SCORER FALLS TWELVE POINTS AND IT IS THE KEY AND THE TEMPO ALONE: 98.262 / 98.767 / 98.725 -> 85.998 / 86.436
# / 86.644 on seeds 0 / 11 / 1, all of it recurrence (100 -> 19.66 / 22.02 / 21.77): it matches sections by their
# pitch classes and no longer finds 'home' to be 'minor' come back. Proof (undo.py): v18's own render with everything
# from the change on played back at 15/16 speed, which takes the tempo and the key back out by tape, scores 98.307,
# recurrence 100. Kept on judgment.
# the section from which the song is lifted ; the ratio, new tempo over old (and so new pitch over old) ; the
# loudness target ("" = unchanged). "" = v17 byte for byte.
GEAR = os.environ.get("C10T14_GEAR", "common;16/15;" if GATHER else "")
# a number is as long as it says, on the note of that length (the tune's own notes, NOTE_OF); two syllables share it
NUMBER = {3: [("TH R IY1", 3)], 4: [("F AO1 R", 4)], 5: [("F AY1 V", 5)], 6: [("S IH1 K S", 6)], 7: [("S EH1", 3), ("V AH0 N", 4)],
          8: [("EY1 T", 8)], 9: [("N AY1 N", 9)], 10: [("T EH1 N", 10)], 11: [("IH0", 2), ("L EH1", 4), ("V AH0 N", 5)],
          12: [("T W EH1 L V", 12)]}
AT = starts()


def add(tr, s, length, pitch, vel, **more):
    """A note at sixteenth `s` (any real number), `length` sixteenths long."""
    n = {"at": round(s / 4, 5), "len": round(length / 4 * 0.96, 5), "pitch": pitch, "vel": round(vel, 3)}
    n.update(more)
    T.setdefault(tr, []).append(n)


def drum(piece, s, vel, **more):
    tr = {"k": "kick", "s": "snare", "t1": "toms", "t2": "toms", "t3": "toms", "ft": "toms", "c": "cym", "x": "cym", "h": "hat"}[piece]
    T.setdefault(tr, []).append({"at": round(s / 4, 5), "len": 2.0 if tr == "cym" else 0.25, "pitch": piece, "vel": round(vel, 3), **more})


# ------------------------------------------------------------------------------------------------ the two rolls
def wind():
    """-> [(piece, sixteenths after the start of the wind-up, octaves of speed)] for the wind-up and the held chord
    after it. The pattern runs at 2**(t/16) times the tempo for 16*OCTAVES sixteenths (an octave a bar), then holds.
    A stroke falls wherever the pattern's own position is a multiple of the drum's period."""
    hold = BAR * int(ROLL.split(";")[3])
    span = BAR * OCTAVES
    k = BAR / math.log(2)
    top = k * (2 ** OCTAVES - 1)                  # the pattern's position when it reaches full speed
    out = []
    for piece, p in DRUMS.items():
        u = 0
        while True:
            t = BAR * math.log2(1 + u / k) if u <= top else span + (u - top) / 2 ** OCTAVES
            if t >= span + hold - 1e-9:
                break
            out.append((piece, t, min(OCTAVES, t / BAR)))
            u += p
    return sorted(out, key=lambda x: x[1]), span + hold


def rolls():
    vel, per_octave, f_tom = (float(v) for v in ROLL.split(";")[:3])
    strokes, length = wind()
    assert length == AT["counted"] == AT["one chord"] + BAR * int(ROLL.split(";")[3]) - AT["wound"]
    for piece, t, octs in strokes:
        g = {"gain": f"{-(f_tom if piece == 't1' else per_octave) * octs:.2f}dB"} if octs > 1e-9 else {}
        drum(piece, AT["wound"] + t, vel, **g)                    # wound up at the end ...
        if t > 1e-9:
            drum(piece, AT["counted"] - t, vel, **g)              # ... and the same strokes backwards at the start


# ------------------------------------------------------------------------------------------------ the pulses
def every(a, z, p, fn, phase=0):
    """fn(s, i) for each stroke of the pulse with period p (sixteenths) from a up to z, counted from a."""
    s, i = a + phase, 0
    while s < z - 1e-9:
        fn(s, i)
        s, i = s + p, i + 1


def chug(pair, a, z, p, low, top):
    """The pair of guitars strikes `low` every p sixteenths: palm-muted, open with the octave on every second
    stroke, and with `top` (a chord) on every fourth. A voice accents its own octaves below."""
    def stroke(s, i):
        for tr in pair:
            if i % 4 == 0:
                add(tr, s, min(p, 3) - 0.2, top, 1.0)
            elif i % 2 == 0:
                add(tr, s, min(p, 2) - 0.2, top.split(",")[0] + "," + top.split(",")[-1], 0.95)
            else:
                add(tr, s, 1, low, 0.88, expr={"pm": 1.0})
    every(a, z, p, stroke)


def common_time(a, z, kick=None, cym="x", snare=0.95, foot=1.0):
    """The kit's hands keep common time: a C in three octaves. The cymbal on the beat (4), the snare on two and
    four (8, half a cycle out). The kick goes with the pulse it is given."""
    assert a % 4 == 0
    for s in range(a, z, 4):                    # by the bar line, wherever in the bar the hands come in
        drum(cym, s, 0.6 if s % BAR == 0 else 0.5)
        if s % BAR in (4, 12):
            drum("s", s, snare)
    if kick:
        every(a, z, kick, lambda s, i: drum("k", s, foot * (1.0 if i % 4 == 0 else 0.86)))


G_F, G_AB, WALL = ("gl", "gr"), ("dl", "dr"), ("wl", "wr")


def f_pulse(a, z, low="F1", top="F1,C2,F2", kick=True):
    chug(G_F, a, z, 3, low, top)
    if kick:
        every(a, z, 3, lambda s, i: drum("k", s, 1.0 if i % 4 == 0 else 0.86))


def bass(a, z, p, pitch, ring):
    every(a, z, p, lambda s, i: add("bass", s, ring, pitch, 0.95 if i % 2 == 0 else 0.85))


def turning_bass(a, sec):
    """v12: the bass goes round the chord. In each cycle of sixty it plays with one wheel at a time, each note struck
    at its own period, and changes wheel on a stroke the two wheels share."""
    if not TURN or sec not in TURN.split(";")[1].split(","):
        return bass(a, a + 240, 6, "F1", 5)
    steps = [(n, int(p), int(span)) for n, p, span in (x.split(":") for x in TURN.split(";")[0].split(","))]
    assert sum(span for _, _, span in steps) == 60
    for c in range(a, a + 240, 60):
        s = c
        for note, p, span in steps:
            assert (s - a) % (p // 2) == 0, (note, s - a)                          # it enters on a stroke of its own wheel
            every(s, s + span, p, lambda t, i, note=note, p=p, z=s + span: add("bass", t, min(p, z - t) - 1, note, 0.95 if i % 2 == 0 else 0.85))
            s += span


def meet(s, chord=None, ring=12):
    drum("c", s, 0.9)
    if chord:
        for tr in WALL:
            add(tr, s, ring, chord, 0.95)


def fills():
    """The cycle in miniature before a meeting: see FILLS."""
    far, near, where, trim, alone = FILLS.split(";")
    per_octave, f_tom = (float(v) for v in ROLL.split(";")[1:3])
    for item in where.split("|"):
        spot, speeds = item.split("=")
        sec, off = spot.split("+")
        speeds = [int(k) for k in speeds.split(",")]
        assert all(60 % k == 0 for k in speeds) and int(off) % 60 == 0
        end = AT[sec] + int(off)
        a = end - sum(60 // k for k in speeds)
        swell = speeds == sorted(speeds)                      # faster and faster swells; slower and slower fades
        t = a
        for k in speeds:
            for piece, p in DRUMS.items():
                def stroke(s, i, piece=piece, k=k):
                    x = (s - a) / (end - a)
                    v = float(far) + (float(near) - float(far)) * (x if swell else 1 - x)
                    drum(piece, s, v, gain=f"{float(trim) - (f_tom if piece == 't1' else per_octave) * math.log2(k):.2f}dB")
                every(t, t + 60 // k, p / k, stroke)
            hands_off(t, t + 60 // k, ("cym", "hat", "snare") if k >= 4 else ("snare",))
            t += 60 // k
    if alone:
        spot, piece, first, lift = alone.split(":")
        sec, off = spot.split("+")
        end = AT[sec] + int(off)
        own, p, t = DRUMS[piece] / 2 ** OCTAVES, float(first), end - BAR
        a = t
        while t < end - 1e-9:
            n = min(8 * p, end - t) if p > own + 1e-12 else end - t        # eight strokes, then twice as fast
            g = f"{float(lift) - (f_tom if piece == 't1' else per_octave) * math.log2(DRUMS[piece] / p):.2f}dB"
            every(t, t + n, p, lambda s, i, g=g: drum(piece, s, float(far) + (float(near) - float(far)) * (s - a) / BAR, gain=g))
            t, p = t + n, max(p / 2, own)
        hands_off(a, end)


def hands_off(a, end, which=("cym", "hat", "snare")):
    """The hands are on the toms from a to end: no cymbal (the crash at a meeting stays), hat or snare."""
    for tr in which:
        if tr in T:
            T[tr] = [n for n in T[tr] if n["pitch"] == "c" or not a / 4 - 1e-6 <= n["at"] < end / 4 - 1e-6]


def bar_and_d_flat():
    """v11: in 'sixth' the fifteens get a drum and the bar gets a drum and a note: see SEMITONE."""
    chord, side, ft, ft_vel, ft_db, bar_drum, bar_vel, bar_db = SEMITONE.split(";")[:8]
    a = AT["sixth"]
    z = a + dict(FORM)["sixth"]
    rolled = min([n["at"] * 4 for n in T.get("toms", []) if a <= n["at"] * 4 < z], default=z)   # the fill before 'fourth'
    lift = lambda db: {"gain": f"{float(db):.2f}dB"} if float(db or 0) else {}
    if chord:
        tr = "w" + side
        T[tr] = [n for n in T[tr] if not a / 4 - 1e-6 <= n["at"] < z / 4 - 1e-6]
        every(a, z, BAR, lambda s, i: add(tr, s, BAR - 1, chord, 0.95))
    if bar_drum:
        for s in range(a + BAR, z, BAR):
            if s < rolled - 1e-9:
                drum(bar_drum, s, float(bar_vel), **lift(bar_db))
    if ft:
        every(a, z, 15, lambda s, i: drum("ft", s, float(ft_vel), **lift(ft_db)))
        # the right hand leaves the china where the floor tom lands with the crash or on a backbeat
        taken = {s for s in range(a, z, 15) if s == a or s % BAR in (4, 12)}
        T["cym"] = [n for n in T["cym"] if not (n["pitch"] == "x" and any(abs(n["at"] * 4 - s) < 1e-6 for s in taken))]


def compose():
    T.clear()
    rolls()
    # counted: the three drums in tempo; at each meeting a pulse is handed to the band
    a = AT["counted"]
    for piece, p in DRUMS.items():
        gone = {"t1": 60, "t3": 120, "t2": 180}[piece]
        every(a, a + gone, p, lambda s, i, piece=piece: drum(piece, s, 0.8))
    f_pulse(a + 60, a + 240)
    bass(a + 60, a + 240, 6, "F1", 5)
    chug(G_AB, a + 120, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a + 180, a + 240)
    for s in (60, 120, 180):
        meet(a + s)
    # minor: the whole chord, one whole cycle
    a = AT["minor"]
    f_pulse(a, a + 240)
    turning_bass(a, "minor")
    chug(G_AB, a, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a, a + 240)
    for s in (0, 60, 120, 180):
        meet(a + s, "F2,Ab2,C3")
    # sixth: where the threes and the fives meet, the note they are both harmonics of
    a = AT["sixth"]
    f_pulse(a, a + 240, low="F2", top="F2,F3")
    chug(G_AB, a, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a, a + 240)
    bass(a, a + 240, 15, "Db1", 14)
    every(a, a + 240, 15, lambda s, i: [add(tr, s, 14, "Db2,Ab2,Db3", 0.95) for tr in WALL])
    drum("c", a, 0.9)
    # fourth: THE QUIET MIDDLE. B flat every nine on the left, D flat every fifteen on the right, and no guitar
    # chugging between them: the F pulse is the foot alone, softly, so every third kick still lands with the B flat.
    # The hands go to the closed hat.
    a = AT["fourth"]
    common_time(a, a + 240, kick=3, cym="h", snare=0.8, foot=0.75)
    bass(a, a + 240, 9, "Bb1", 8)
    every(a, a + 240, 9, lambda s, i: add("wl", s, 8, "Bb1,F2,Bb2", 0.95))
    every(a, a + 240, 15, lambda s, i: add("wr", s, 14, "Db2,Ab2,Db3", 0.95))
    drum("c", a, 0.9)
    # common: everyone on C, which is common time
    a, z = AT["common"], AT["home"]
    every(a, z, 1, lambda s, i: [add(tr, s, 1, "C2", 0.88, expr={"pm": 1.0}) if i % 4 else add(tr, s, 0.8, "C2,C3", 1.0 if i % 16 == 0 else 0.95) for tr in G_F])
    every(a, z, 2, lambda s, i: [add(tr, s, 1, "C3", 0.88, expr={"pm": 1.0}) if i % 4 else add(tr, s, 1.8, "C3,C4", 0.95) for tr in G_AB])
    every(a, z, 16, lambda s, i: [add(tr, s, 12, "C2,C3", 0.95) for tr in WALL])
    bass(a, z, 4, "C2", 3.5)
    common_time(a, z, kick=2)
    for s in (a, a + 64):
        drum("c", s, 0.9)
    # home: F minor, everything; the three drums again for the last meeting
    a = AT["home"]
    f_pulse(a, a + 240)
    turning_bass(a, "home")
    chug(G_AB, a, a + 240, 5, "Ab2", "Ab2,Ab3")
    common_time(a, a + 240)
    every(a, a + 240, 12, lambda s, i: [add(tr, s, 11, "F2,C3,F3", 0.95) for tr in WALL])
    for s in (0, 60, 120, 180):
        drum("c", a + s, 0.9)
    for piece, p in DRUMS.items():
        every(a + 180, a + 240, p, lambda s, i, piece=piece: drum(piece, s, 0.8))
    # one chord: what the drums have become, on the band
    a, ring = AT["one chord"], FORM[-1][1] - 4
    held = "-still" if STILL else ""
    for tr in G_F:
        add(tr + held, a, ring, "F1,C2,F2", 1.0)
    for tr in G_AB:
        add(tr + held, a, ring, "Ab2,C3,F3", 1.0)
    for tr in WALL:
        add(tr, a, ring, "F2,C3,F3", 1.0)
    add("bass", a, ring, "F1", 0.95)
    drum("k", a, 1.0)
    drum("c", a, 0.95)
    if TUNE:
        vel = float(TUNE.split(";")[1])
        tune(AT["minor"] + 120, ["A", "B"], vel)
        tune(AT["sixth"], ["C", "D", "C'", "D"], vel)
        tune(AT["fourth"], ["E", "G", "E", "G"], vel - 0.15, gain="-1.5dB")
        assert tune(AT["common"], ["climb", "climb"], vel) == AT["home"]
        assert tune(AT["home"], ["A", "B", "A'", "S"], vel) == AT["wound"] + 15
        # THE LAST CHORD'S THIRD. In v1 the band's last chord was led by C and the low F and its A flat was not
        # among the six strongest lines: under a power chord the guitars' minor third does not carry. The tune
        # holds it: the fives' note, over the chord the drums wound up to
        add("tune-still" if STILL and STILL.split(";")[2] else "tune", AT["one chord"], FORM[-1][1] - 4, "Ab4", vel)
    if COUNT:                                                     # v13: the voice counts where the drums are alone
        f = COUNT.split(";")
        who = [("count", -1)] + ([("count-high", 0)] if f[2] else [])

        def say(s, numbers, db=0.0):
            for p in numbers:
                n = NOTE_OF[p]
                for i, (ph, n16) in enumerate(NUMBER[p]):
                    end = i == len(NUMBER[p]) - 1
                    for tr, octave in who:
                        add(tr, s, (n16 - (float(f[7]) if end else 0)) / 0.96, n[:-1] + str(int(n[-1]) + octave), float(f[6]), ph=ph,
                            **({"gain": f"{db:g}dB"} if db else {}))
                    s += n16
            return s
        if "down" in f[8]:        # three to twelve, slowing as it falls, and the drums are in tempo as 'twelve' ends
            assert say(AT["counted"] - sum(range(3, 13)), range(3, 13)) == AT["counted"]
        if "named" in f[8]:       # the three drums alone, each named for as long as its own stroke: five times is the sixty
            assert say(AT["counted"], (3, 4, 5) * 5, float(f[10] or 0)) == AT["counted"] + 60
        if "up" in f[8]:          # twelve to three, quickening as it climbs, from where the tune's last note ends
            s = AT["wound"] + 15
            for k, p in enumerate(range(12, 2, -1)):
                s = say(s, (p,), float(f[11] or 0) * k / 9)
            assert s == AT["wound"] + 90
    if FILLS:
        fills()
    if SEMITONE:
        bar_and_d_flat()
    if FOOT:                                                      # v7: wherever the A flat pair chugs the fives, the left foot strikes them
        vel = float(FOOT.split(";")[3])
        # (in 'counted' the A flat tom has the fives until +120, in 'home' it has them again from +180: one drum at a time)
        for sec, off, to in (("counted", 120, 240), ("minor", 0, 240), ("sixth", 0, 240), ("home", 0, 180)):
            every(AT[sec] + off, AT[sec] + to, 5, lambda s, i: T.setdefault("block", []).append(
                {"at": round(s / 4, 5), "len": 0.25, "pitch": "b3" if i % 4 == 0 else "b2" if i % 2 == 0 else "b1",
                 "vel": round(vel * (1.0 if i % 4 == 0 else 0.93 if i % 2 == 0 else 0.85), 3)}))
    if WHEELS:
        sec, off = (WHEELS.split(";")[3].split("+") + ["0"])[:2]
        vel = float(WHEELS.split(";")[4])
        for tr, p, note in (("seven", 7, "D"), ("eleven", 11, "Gb")):
            def stroke(s, i, tr=tr, note=note):
                if WHEELS.split(";")[0].endswith("-kit"):
                    bol, v = ("tun", vel) if i % 4 == 0 else ("tin", vel * 0.93) if i % 2 == 0 else ("na", vel * 0.85)
                    T.setdefault(tr, []).append({"at": round(s / 4, 5), "len": 0.25, "pitch": bol, "vel": round(v, 3)})
                elif i % 4 == 0:
                    add(tr, s, 4, f"{note}4,{note}5,{note}6", vel)
                elif i % 2 == 0:
                    add(tr, s, 4, f"{note}5,{note}6", vel * 0.93)
                else:
                    add(tr, s, 4, f"{note}5", vel * 0.85)
            every(AT[sec] + int(off), AT[sec] + dict(FORM)[sec], p, stroke)
    for tr in T:
        T[tr].sort(key=lambda n: (n["at"], n["pitch"]))
    return AT["end"]


def song():
    end = compose()
    key = []                                    # the low bus's eq follows the bass's ground, in semitones over F
    grounds = [(AT[name], semis) for name, semis in (("sixth", -4), ("fourth", 5), ("common", 7), ("home", 0))]
    if TURN and TURN.split(";")[3]:             # v12: and, where the bass goes round the chord, each note of the round
        spans = [int(x.split(":")[2]) for x in TURN.split(";")[0].split(",")]
        for sec in TURN.split(";")[1].split(","):
            for c in range(AT[sec], AT[sec] + 240, 60):
                s = c
                for span, semis in zip(spans, TURN.split(";")[3].split(",")):
                    if not any(at == s for at, _ in grounds):
                        grounds.append((s, float(semis)))
                    s += span
            if not any(at == AT[sec] + 240 for at, _ in grounds):
                grounds.append((AT[sec] + 240, float(TURN.split(";")[3].split(",")[0])))
    for at, semis in sorted(grounds):
        b = at / 4
        key += [[f"{b - 0.02:g}b", key[-1][1] if key else 0], [f"{b:g}b", semis]]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    f_pair, a_pair = "0.7dB", "-2.5dB"
    if RIG:                                     # v8: the chord guitars' body, box and fader
        main, dbl = (r + f" fx.1.tight={RIG.split(';')[0]}" for r in (main, dbl))
        mids = {"fx": [{"type": "eq", "bands": [RIG.split(";")[1]]}]}
        f_pair, a_pair = (f"{float(g[:-2]) + float(RIG.split(';')[2]):g}dB" for g in (f_pair, a_pair))
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    top = {"fx": [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]}
    kit = "ct-kit-here"
    tracks = [
        {"name": "gl", "patch": main.format(140), "gain": f_pair, "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(141), "gain": f_pair, "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(142), "gain": a_pair, "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(143), "gain": a_pair, "pan": 0.75, "out": "gtrs", **mids},
        {"name": "wl", "patch": still("ct-wall-stop-l", 2), "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": still("ct-wall-stop-r", 2), "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": os.environ.get("C10T14_TOMS", "-1.5dB"), "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, **top},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, **top},
    ]
    if TUNE:
        gain, _, echo = TUNE.split(";")
        lead = {"name": "tune", "patch": f"m8-lead-guitar fx.4.mix={echo} fx.5.mix=0.15", "gain": gain, "pan": 0}
        if LEAD:
            box, pick, ride = (x.split(":") for x in LEAD.split(";")[:3])
            lead["fx"] = [{"type": "eq", "bands": [f"peak cutoff={box[0]} q={box[1]} gain={box[2]}dB", f"highshelf cutoff={pick[0]} gain={pick[1]}dB"]}]
            if ride[0] and float(ride[0]):
                a, z = AT["fourth"] / 4, AT["common"] / 4
                lead["gain"] = {"value": gain, "mod": [{"src": "auto.ride", "amount": 1}]}
                lead["auto"] = {"ride": {"curve": 0, "points": [["0b", 0], [f"{a - 0.25:g}b", 0], [f"{a:g}b", float(ride[0])],
                                                               [f"{z - 0.25:g}b", float(ride[0])], [f"{z:g}b", 0]]}}
        tracks.append(lead)
    if STILL:
        # the last chord's four other guitars: the same rigs, faders, sides and eq, standing still
        tracks += [{**t, "name": t["name"] + "-still", "patch": still(t["patch"], i // 2)} for i, t in enumerate(tracks[:4])]
        if TUNE and STILL.split(";")[2]:
            tracks += [{**t, "name": "tune-still", "patch": still(t["patch"], 3)} for t in tracks if t["name"] == "tune"]
    wheel_patches = {}
    if WHEELS:
        patch, gain, pan = WHEELS.split(";")[:3]
        if patch.endswith("-kit"):
            # two drums of the same make, each tuned to the note its count is: D4 12/7 over F3, G flat 4 12/11 over F4
            for name, note, side in (("seven", 53 + 12 * math.log2(12 / 7), -1), ("eleven", 65 + 12 * math.log2(12 / 11), 1)):
                wheel_patches["sc-" + name] = {"extends": patch, "kit": {b: {"pitch": f"m{note:.4f}", "pan": side * float(pan)} for b in ("na", "tin", "tun")}}
                tracks.append({"name": name, "patch": "sc-" + name, "gain": gain})
        else:
            tracks += [{"name": "seven", "patch": patch, "gain": gain, "pan": -float(pan)}, {"name": "eleven", "patch": patch, "gain": gain, "pan": float(pan)}]
    if FOOT:
        tracks.append({"name": "block", "patch": kit, "gain": FOOT.split(";")[0], "out": "drums"})
    if COUNT:                                                     # v13: the voice that counts, and its octave
        f = COUNT.split(";")
        fx = ([{"type": "eq", "bands": f[4].split("|")}] if f[4] else []) + ([f[5]] if f[5] else [])
        tracks.append({"name": "count", "patch": f[0], "gain": f[1], "pan": -0.12, **({"fx": fx} if fx else {})})
        if f[2]:
            tracks.append({"name": "count-high", "patch": f"{f[0]} synth.layers.0.tract={f[2]}", "gain": f[3], "pan": 0.12, **({"fx": fx} if fx else {})})
        if len(f) > 12 and f[12] and float(f[12]):                # the toms give the voices room
            pts, b = [["0b", 0]], lambda s16: f"{s16 / 4:g}b"
            for place, a, z in (("down", AT["counted"] - 75, AT["counted"]), ("named", AT["counted"], AT["counted"] + 60), ("up", AT["wound"] + 15, AT["wound"] + 90)):
                if place in f[8]:
                    if pts[-1][0] == b(a) and pts[-1][1] == 0:        # two places end to end: one stretch
                        pts[-2:] = [[b(z - 2), float(f[12])], [b(z), 0]]
                    else:
                        pts += [[b(a - 2), 0], [b(a), float(f[12])], [b(z - 2), float(f[12])], [b(z), 0]]
            toms = next(t for t in tracks if t["name"] == "toms")
            assert isinstance(toms["gain"], str)
            toms["gain"] = {"value": toms["gain"], "mod": [{"src": "auto.count", "amount": 1}]}
            toms["auto"] = {**toms.get("auto", {}), "count": {"points": pts, "curve": 0}}
    assert {t["name"] for t in tracks} >= set(T), set(T) - {t["name"] for t in tracks}
    for t in tracks:
        t["notes"] = T.get(t["name"], [])
    chest_patch = {}
    if KICK:
        _, fader, note, gain, decay, click, twos, _ = KICK.split(";")
        at = next(i for i, t in enumerate(tracks) if t["name"] == "kick")
        if fader:
            tracks[at]["gain"] = f"{fader}dB"
        a, z = AT["common"] / 4, AT["home"] / 4
        if click:
            tracks[at]["fx"] = [{"type": "eq", "bands": [f"peak cutoff=4500 q=0.8 gain={click}dB"]}]
        if note:
            # a bare sine an octave over the drum, struck with every kick at its velocity, straight to the mix (past the
            # kit bus's clip, which holds the kick's top, and outside the kick's own drive, which shares one ceiling)
            chest_patch["sc-chest"] = {"extends": "808", "synth": {"layers": ["sine"], "pitch": {"value": 0, "mod": []}, "drive": 0, "filters": [],
                                                                  "amp": {"a": "2ms", "d": f"{decay}ms", "s": 0, "r": "20ms", "curve": 3}},
                                        "play": {"mono": False, "glide": "0ms", "gate": 1}}
            tracks.insert(at + 1, {"name": "chest", "patch": "sc-chest", "gain": gain, "pan": 0,
                                   "notes": [{"at": n["at"], "len": round(float(decay) / 1000 * BPM / 60, 4), "pitch": twos if twos and a <= n["at"] < z else note, "vel": n["vel"]}
                                             for n in tracks[at]["notes"]]})
    low = [
        {"type": "eq", "bands": [
            {"kind": "peak", "cutoff": {"value": 44, "mod": [{"src": "auto.key", "amount": 0.08333}]}, "q": 1.5, "gain": "-7dB"},
            {"kind": "peak", "cutoff": {"value": 90, "mod": [{"src": "auto.key", "amount": 0.08333}]}, "q": 1.0, "gain": "7.5dB"},
            {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"},
            {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
        {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
        {"type": "eq", "bands": [{"kind": "peak", "cutoff": {"value": 170, "mod": [{"src": "auto.key", "amount": 0.08333}]}, "q": 1.2, "gain": "-3dB"}]},
    ]
    kit_here = {"x": {"pan": 0.35}, "t1": {"pan": -0.5}, "t2": {"pan": 0.0}, "t3": {"pan": 0.5}}
    if TUNED:
        # C3 a pure fourth under the F tom and A flat 2 a pure sixth under it: the notes their rolls are
        kit_here["t2"]["pitch"] = f"m{48 + 12 * math.log2(3 / 2) - 7:.4f}"
        kit_here["t3"]["pitch"] = f"m{44 + 12 * math.log2(6 / 5) - 3:.4f}"
    if SNARE:
        note, reso, shell_hz, shell, body, own = SNARE.split(";")[:6]
        kit_here["s"] = {"pitch": note, "gain": f"{own}dB", "patch": {"synth": {
            "layers": [{"type": "drum", "beater": "stick", "contact": 0.6, "decay": "0.18s", "sharp": 30, "reso": float(reso), "cavity": 0.3,
                        "reso_level": 0.7, "shell": float(shell), "shell_hz": float(shell_hz), "wires": 0.85, "gap": 0.1, "wire_tone": "7k",
                        "strike": 0.3, "damp": 0.3, "slap": 1.2}],
            "filters": ["hp cutoff=150"] + [x for x in body.split("|") if x]}}}
    if KICK:
        kit_here["k"] = {"pitch": KICK.split(";")[0]}
    if SEMITONE and SEMITONE.split(";")[2]:
        # the floor tom, a pure fifth under the A flat tom: the fifteens' D flat
        kit_here["ft"] = {"pitch": SEMITONE.split(";")[2]}
    if FOOT:
        # three wood blocks an octave apart, each the library kit's wood block at the fives' own note: a triangle at the
        # note through a band-pass there, and three milliseconds of stick
        for piece, hz, ring, own in zip(("b1", "b2", "b3"), (float(x) for x in FOOT.split(";")[2].split(":")), (70, 80, 95), FOOT.split(";")[5].split(":")):
            kit_here[piece] = {"gain": f"{own}dB", "pan": float(FOOT.split(";")[1]), "patch": {"synth": {
                "amp": {"a": "0.1ms", "curve": 4, "d": f"{ring}ms", "r": "15ms", "s": 0}, "env": {"c": {"a": "0.1ms", "d": "3ms", "s": 0}},
                "filters": [f"bp cutoff={hz:g} q=2"],
                "layers": [f"triangle fixed={hz:g}", {"type": "noise", "level": {"value": "-66dB", "mod": [{"src": "env.c", "amount": 50}]}}]}}}
    doc = {
        "about": ("chirpers X (Common Time), track 14 by chirper-three: Slow Enough to Count. A chord is a rhythm too fast to count. "
                  "At this tempo a pulse every three sixteenths is an F six octaves down, common time is a C and the fives are an A flat, "
                  "so threes against fours against fives are F minor. Three toms tuned to the chord are rolled at their own notes, slowed "
                  "six octaves until they can be counted, handed to the band a pulse at a time, and wound back up into the chord at the end. "
                  + ("The band is tuned to the pulses' own notes, and a lead plays a tune in which every note lasts as long as its period." if TUNED and TUNE else "v1 is the skeleton.")),
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(WHEELS.split(";")[5]) if WHEELS else float(LEAD.split(";")[3]) if LEAD and TUNE else -10, "seed": 1, "tail": "5s", "length": f"{end // 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": kit_here}} | wheel_patches | chest_patch,
        "buses": {
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB",
                                                      "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6",
                          {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            "low": {"fx": low, "auto": {"key": {"points": [["0b", 0]] + key, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": "2.7dB"}]},
        "tracks": tracks,
    }
    if FOOT and FOOT.split(";")[4]:
        doc["loudness"] = float(FOOT.split(";")[4])
    if RIG and RIG.split(";")[3]:
        doc["loudness"] = float(RIG.split(";")[3])
    if SNARE and SNARE.split(";")[6]:
        doc["loudness"] = float(SNARE.split(";")[6])
    if KICK and KICK.split(";")[7]:
        doc["loudness"] = float(KICK.split(";")[7])
    if SEMITONE and SEMITONE.split(";")[8]:
        doc["loudness"] = float(SEMITONE.split(";")[8])
    if TURN and TURN.split(";")[2]:
        doc["loudness"] = float(TURN.split(";")[2])
    if COUNT and COUNT.split(";")[9]:
        doc["loudness"] = float(COUNT.split(";")[9])
    if CLEAN:
        the_quiet_middle(doc)
    if MIDDLE and COUNT:
        the_middle_is_counted(doc)
    if HEADS:
        the_three_drums(doc)
    if TUNED:
        doc = {k: v for k, v in list(doc.items())[:2]} | {"tuning": {"steps": JUST, "root": "F3", "map": "keys"}} | {k: v for k, v in list(doc.items())[2:]}
    return doc


def the_three_drums(doc):
    """v16: the chord's three drums (t1 F, t2 C, t3 A flat) lose their box at the head, ring shorter and get a stick."""
    inside, fader, loud = HEADS.split(";")
    t = next(t for t in doc["tracks"] if t["name"] == "toms")
    t["patch"] += "".join(f" kit.{piece}.patch.{o}" for piece in ("t1", "t2", "t3") for o in inside.split())
    if fader:
        t["gain"] = dict(t["gain"], value=fader) if isinstance(t["gain"], dict) else fader
    if loud:
        doc["loudness"] = float(loud)


def the_middle_is_counted(doc):
    """v15: in 'fourth' the voices sing the tune's long notes as their numbers, and the lead rests on them."""
    sung, octaves, db, fif, loud, more, faders, eq = MIDDLE.split(";")
    f = COUNT.split(";")
    a, z = AT["fourth"] / 4, AT["common"] / 4
    track = {t["name"]: t for t in doc["tracks"]}
    notes = sorted((n for n in track["tune"]["notes"] if a <= n["at"] < z), key=lambda n: n["at"])
    assert len(notes) % 12 == 0, len(notes)
    said = {int(i) for i in sung.split(",")}
    number = {**NUMBER, 15: [("F IH0 F", int(fif.split(":")[0])), ("T IY1 N", int(fif.split(":")[1]))]}
    voices = [("count", int(octaves.split(",")[0]))] + ([("count-high", int(octaves.split(",")[1]))] if f[2] else [])
    if more or faders or eq:                # the same two singers on tracks of their own: the frame's are not touched
        for k, (tr, octave) in enumerate(list(voices)):
            new = {**{x: y for x, y in track[tr].items() if x != "notes"}, "name": tr.replace("count", "said"), "notes": []}
            if more:
                new["patch"] += " " + more
            if faders:
                new["gain"] = faders.split(",")[k]
            if eq:
                new["fx"] = [{"type": "eq", "bands": eq.split("|")}] + [x for x in new.get("fx", []) if not (isinstance(x, dict) and x.get("type") == "eq")]
            doc["tracks"].append(new); track[new["name"]] = new
            voices[k] = (new["name"], octave)
    gone = []
    for i, n in enumerate(notes):
        if i % 12 not in said:
            continue
        p = round(((notes[i + 1]["at"] if i + 1 < len(notes) else z) - n["at"]) * 4, 3)
        assert p == int(p) and int(p) in number, p
        p, s = int(p), n["at"] * 4
        assert sum(k for _, k in number[p]) == p
        for j, (ph, n16) in enumerate(number[p]):
            end = j == len(number[p]) - 1
            for tr, octave in voices:
                track[tr]["notes"].append({"at": round(s / 4, 5), "len": round((n16 - (float(f[7]) if end else 0)) / 4, 5),
                                           "pitch": n["pitch"][:-1] + str(int(n["pitch"][-1]) + octave), "vel": float(f[6]), "ph": ph,
                                           **({"gain": f"{float(db):g}dB"} if db and float(db) else {})})
            s += n16
        gone.append(n)
    track["tune"]["notes"] = [n for n in track["tune"]["notes"] if not any(n is g for g in gone)]
    for tr, _ in voices:
        track[tr]["notes"].sort(key=lambda n: n["at"])
    if loud:
        doc["loudness"] = float(loud)


def the_quiet_middle(doc):
    """v14: in 'fourth' the nines and the fifteens leave the two wall guitars for a clean pair; the kit and the lead come down."""
    patch, gain, semis, vel, eq, verb, kit, rim, ride, loud = CLEAN.split(";")
    a, z = AT["fourth"] / 4, AT["common"] / 4
    track = {t["name"]: t for t in doc["tracks"]}
    names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    up = lambda chord: ",".join(names[(names.index(n[:-1]) + int(semis)) % 12] + str(int(n[-1]) + (names.index(n[:-1]) + int(semis)) // 12) for n in chord.split(","))
    for wall, name, chord, period in (("wl", "clean-l", "Bb1,F2,Bb2", 9), ("wr", "clean-r", "Db2,Ab2,Db3", 15)):
        t = track[wall]
        moved = [n for n in t["notes"] if a <= n["at"] < z]
        # every stroke the wall has in the quiet middle is this chord on this wheel, and all of them go
        assert moved and all(n["pitch"] == chord for n in moved) and all(abs((n["at"] - a) * 4 % period) < 1e-6 for n in moved), wall
        t["notes"] = [n for n in t["notes"] if not a <= n["at"] < z]
        fx = ([{"type": "eq", "bands": eq.split("|")}] if eq else []) + ([verb] if verb else [])
        doc["tracks"].append({"name": name, "patch": patch, "gain": gain, "pan": t["pan"], "out": "gtrs", **({"fx": fx} if fx else {}),
                              # (a clean chord does not ring on under the band's first stroke of 'common': the wall's last one did)
                              "notes": [{**n, "pitch": up(chord), "vel": float(vel), "len": round(min(n["len"], z - n["at"] - 0.05), 5)} for n in moved]})
    kick, snare, hat = kit.split(":")
    for who, db in ((("kick", "chest"), kick), (("snare",), snare), (("hat",), hat)):
        for name in who:
            for n in track[name]["notes"]:
                if a <= n["at"] < z and float(db) and not (name == "snare" and rim):
                    n["gain"] = f"{float(n.get('gain', '0dB').rstrip('dB')) + float(db):g}dB"
    if rim:
        piece, over, db = rim.split(":")
        for n in track["snare"]["notes"]:
            if a <= n["at"] < z:
                assert n["pitch"] == "s" and "gain" not in n and "patch" not in n
                n.update({"pitch": piece, "gain": f"{float(db):g}dB"}, **({"patch": f"{track['snare']['patch']} {over}"} if over else {}))
    if float(ride or 0):
        lead = track["tune"]
        was = float(LEAD.split(";")[2])
        pts = lead["auto"]["ride"]["points"]
        assert sum(1 for q in pts if q[1] == was) == 2
        lead["auto"]["ride"]["points"] = [[q[0], q[1] + float(ride) if q[1] == was else q[1]] for q in pts]
    if loud:
        doc["loudness"] = float(loud)


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


def the_three_gather(doc):
    """v17: at the meetings of three, four and five the three drums play the pulses' last strokes in and first strokes out; the band rests on the way in."""
    where, rest, vin, vmeet, vout, back, loud = GATHER.split(";")
    tr = {t["name"]: t for t in doc["tracks"]}
    toms = tr["toms"]["notes"]
    have = {(round(n["at"] * 4), n["pitch"]) for n in toms}
    def stroke(s16, piece, vel):
        if (s16, piece) not in have:
            toms.append({"at": s16 / 4, "len": 0.25, "pitch": piece, "vel": round(float(vel), 3)})
            have.add((s16, piece))
    for entry in where.split("|"):
        sec, offs, deep = (entry.split(":") + ["1"])[:3]
        deep = int(deep)
        for off in offs.split(","):
            leave = not off.endswith("<")
            m = AT[sec] + int(off.rstrip("<"))
            for name, period in (("kick", 3), ("cym", 4), ("block", 5)):                     # a meeting of all three, and the kit is already there
                at = {round(n["at"] * 4) for n in tr[name]["notes"]}
                assert all(m - period * k in at and (not leave or m + period * k in at) for k in range(1, deep + 1)) and (name != "kick" or m in at), (sec, off, name)
            for k in range(1, deep + 1):
                for (piece, period), vel in zip((("t3", 5), ("t2", 4), ("t1", 3)), vin.split(",")):
                    stroke(m - period * k, piece, float(vel) - float(back or 0) * (k - 1))    # each pulse's last strokes before
            if vmeet:
                for piece in ("t3", "t2", "t1"):
                    stroke(m, piece, vmeet)
            if leave and vout:
                for k in range(1, deep + 1):
                    for (piece, period), vel in zip((("t1", 3), ("t2", 4), ("t3", 5)), vout.split(",")):
                        stroke(m + period * k, piece, float(vel) - float(back or 0) * (k - 1))   # and its first strokes after
            for name in filter(None, rest.split(",")):
                keep = []
                for n in tr[name]["notes"]:
                    a = round(n["at"] * 4); z = n["at"] * 4 + n["len"] * 4
                    if m - 5 * deep <= a < m:
                        continue                                                             # it rests
                    if a < m - 5 * deep < z:
                        n = dict(n, len=round((m - 5 * deep - a) * 0.96 / 4, 4))             # and lets go where the rest begins
                    keep.append(n)
                tr[name]["notes"] = keep
    toms.sort(key=lambda n: n["at"])
    if loud:
        doc["loudness"] = float(loud)


def the_fifteen_becomes_the_bar(doc):
    """v18: from `where` on, the tempo is `ratio` times what it was and, because in this song a pulse IS a note, so is
    every pitch. Runs last, on the finished document: every beat position stays where it was written (the tempo is a
    map), each part that plays on both sides is parted in two (the part after the change goes to a track of its own,
    appended last, transposed; a kit's tuned pieces are retuned), and the bass bus's eq follows."""
    import copy
    where, ratio, loud = GEAR.split(";")
    num, den = (int(x) for x in ratio.split("/"))
    semis = round(12 * math.log2(num / den), 5)
    at = AT[where] / 4                                                   # beats
    # THE LIFTED PARTS KEEP THEIR WRITTEN NOTES AND TAKE A TUNING OF THEIR OWN: the song's just scale, every step times
    # the ratio. (A `transpose` counts keys through the scale, whose steps are not equal: read on the last chord, F
    # and C came out 165 cents up and A flat 84. A tuning's root must be a written note at its equal-tempered pitch
    # and a chord cannot be written in hertz. So the root is moved to a key the lifted parts never play, E, a semitone
    # under F: each step is then the old step over F, times the ratio, plus that semitone; E flat, also never played,
    # takes what is left under the octave.)
    old = [1.0] + [float(x.split("/")[0]) / float(x.split("/")[1]) for x in doc["tuning"]["steps"][:-1]]     # F, G flat ... E, over F
    assert doc["tuning"]["root"] == "F3" and doc["tuning"]["map"] == "keys" and len(old) == 12
    cents = [round(100 + 1200 * math.log2(r * num / den), 3) for r in old[:10]]                               # F ... D, over E
    cents.append(round((cents[-1] + 1200) / 2, 3))                                                            # E flat (unplayed)
    assert all(a < b for a, b in zip(cents, cents[1:])) and cents[-1] < 1200
    lifted_tuning = {"steps": cents + ["2/1"], "root": "E3", "map": "keys"}
    lifted_kits = {}

    def lifted_kit(name):
        if name not in lifted_kits:
            kit = copy.deepcopy(doc["patches"][name])
            if name == "ct-kit-here":
                kit["kit"]["t1"]["pitch"] = "m53"                        # the album kit's F3, said as a number so it can move
            for piece, v in kit["kit"].items():
                if str(v.get("pitch", "")).startswith("m") and piece not in ("x", "c", "h"):
                    v["pitch"] = f"m{float(v['pitch'][1:]) + semis:.4f}"
                if piece in ("b1", "b2", "b3"):                          # the blocks are tuned by a fixed frequency and a band-pass on it
                    hz = float(v["patch"]["synth"]["layers"][0].split("fixed=")[1])
                    v["patch"]["synth"]["layers"][0] = f"triangle fixed={hz * num / den:.2f}"
                    v["patch"]["synth"]["filters"][0] = f"bp cutoff={hz * num / den:.2f} q=2"
            doc["patches"][name + "-up"] = kit
            lifted_kits[name] = name + "-up"
        return lifted_kits[name]

    def lift(tr):
        first, _, rest = tr["patch"].partition(" ")
        if "kit" in doc["patches"].get(first, {}):
            tr["patch"] = lifted_kit(first) + (" " + rest if rest else "")
        else:
            assert not any(w[:2] in ("Eb", "E0", "E1", "E2", "E3", "E4", "E5", "E6", "D#") for n in tr["notes"] for w in str(n["pitch"]).split(",")), tr["name"]
            tr["tuning"] = lifted_tuning

    twins = []
    for tr in doc["tracks"]:
        after = [n for n in tr["notes"] if n["at"] >= at - 1e-9]
        if not after or tr["name"] in ("cym", "hat"):                    # a cymbal is not a note
            continue
        if len(after) == len(tr["notes"]):
            lift(tr)
            continue
        twin = copy.deepcopy(tr)
        twin["name"], twin["notes"] = tr["name"] + "-up", after
        tr["notes"] = [n for n in tr["notes"] if n["at"] < at - 1e-9]
        lift(twin)
        twins.append(twin)
    doc["tracks"] += twins
    for p in doc["buses"]["low"]["auto"]["key"]["points"]:               # the bass bus's eq is keyed to the ground, in semitones over F
        if float(p[0].rstrip("b")) >= at - 1e-9:
            p[1] = round(p[1] + semis, 4)
    # THE TEMPO IS WRITTEN INTO THE POSITIONS, NOT INTO A TEMPO MAP: the song keeps its one declared tempo (the album's
    # tools read beats as seconds at one tempo: rests, presence, the palette, the cards' "who plays here"), and from
    # the change on every stroke, length and automation point stands den/num as far from it as it was written.
    # (Rendered both ways: the same audio.) From there a bar is 3.75 beats of the declared tempo.
    def moved(b):
        return b if b < at - 1e-9 else round(at + (b - at) * den / num, 6)

    for tr in doc["tracks"]:
        for n in tr["notes"]:
            if n["at"] >= at - 1e-9:
                n["at"], n["len"] = moved(n["at"]), round(n["len"] * den / num, 6)

    def lanes(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "points":
                    for p in v:
                        p[0] = f"{moved(float(p[0].rstrip('b'))):g}b"
                else:
                    lanes(v)
        elif isinstance(o, list):
            for v in o:
                lanes(v)
    lanes(doc["tracks"])
    lanes(doc["buses"])
    doc["length"] = f"{moved(float(doc['length'].rstrip('b'))):g}b"
    doc["about"] += (f" From {int(at * 60 / BPM // 60)}:{at * 60 / BPM % 60:04.1f} the count is {num}/{den} as fast, so by the song's own rule"
                     " every note is too: the D flat struck every fifteen becomes the bar, and the song ends a just semitone"
                     " above the chord it began on.")
    if loud:
        doc["loudness"] = float(loud)


# v19 (chirper-one; section round, w5, 2:05-2:36, the window that holds v18's change of gear and had never been
# focused; the change is 2:10.97-2:12.80, one bar): SIXTEEN IS SAID. chirper-three's v18: the D flat struck every
# fifteen sixteenths through the quiet middle is sixteen of the faster sixteenths, so it becomes the bar. Through
# the middle (v15) the two voices sing the tune's long notes as their numbers, each as long as it says, and the last
# thing they sing is "fifteen", on that D flat, ending on the change. Now they sing it once more: the same note,
# the same length to the millisecond, and its new name: "six-teen" (six of the new sixteenths and ten). The same
# sound twice, counted two ways: v18's change, in the song's own words.
# And the band lets it be heard. In the first bar of 'common' everyone strikes the bar line once, the D flat's
# pulse come round on time and for the first time on the whole band (the crash, the kick, the guitars, the walls,
# the bass), and stops; the lead, whose note this is, leaves it to the voices, and they hold the D flat alone for
# the bar. At the next bar line, one more turn of the D flat's own clock, the band comes in on a crash, counting
# sixteen to it. So the pulse that crosses the change is heard crossing it, is named, and then the band gathers
# round it (v18's open list: "the seam is not prepared ... a bar on the D flat's own clock would announce the bar").
# (First bench: the wall pair's chord held through the bar under the voices, as written. It is the voices' own note
# and its octave, and it took the word: the recogniser wrote "16" only with the voices 10 dB up, as loud as the
# band. So the walls strike and stop with everyone else.)
# 67 strokes are taken out of the bar, four voice notes and one crash put in; the voices are on their own tracks
# of the middle (`said`, `said-high`: the unlifted scale, where D flat is D flat), so nothing else of theirs moves.
# bars of the section the band waits ; the longest a stroke on its first bar line may ring, new sixteenths ('' = as
# written) ; who leaves the bar wholly ; the word, `phonemes:new sixteenths` | ... ; who sings it and on what,
# `track=note` , ... ; dB on its notes ; the cymbal's piece and velocity where the band comes in ('' = none) ;
# the loudness target ('' = unchanged). '' = v18 byte for byte.
SIXTEEN = os.environ.get("C10T14_SIXTEEN", "1;2;tune-up;S IH1 K S:6|T IY1 N:10;said=Db3,said-high=280.68hz;3;c:0.9;" if GEAR else "")


def sixteen_is_said(doc):
    """v19: the first bar of the lifted section is the D flat's pulse alone, and the voices give it its new name."""
    bars, ring, leave, word, who, gain, crash, target = SIXTEEN.split(";")
    num, den = (int(x) for x in GEAR.split(";")[1].split("/"))
    t0, six = AT[GEAR.split(";")[0]] / 4, den / num / 4               # the change, in declared beats ; a new sixteenth
    t1 = t0 + int(bars) * 16 * six
    tr = {t["name"]: t for t in doc["tracks"]}
    singers = dict(x.split("=") for x in who.split(","))
    out = 0
    for name, t in tr.items():
        if name in singers or not t.get("notes"):
            continue
        keep = [n for n in t["notes"] if not (t0 - 1e-6 <= n["at"] < t1 - 1e-6) or (abs(n["at"] - t0) < 1e-6 and name not in leave.split(","))]
        out += len(t["notes"]) - len(keep)
        t["notes"] = keep
        for n in keep:
            if ring and abs(n["at"] - t0) < 1e-6 and n["len"] > float(ring) * six:
                n["len"] = round(float(ring) * six, 4)
    assert sum(1 for t in tr.values() for n in t.get("notes") or [] if abs(n["at"] - t0) < 1e-6 and t["name"] not in singers) >= 8, "the band strikes the change"
    for name, pitch in singers.items():
        assert not any(n["at"] + n["len"] > t0 + 1e-6 for n in tr[name]["notes"]), "the singers have finished 'fifteen' at the change"
        at = t0
        for part in word.split("|"):
            ph, n16 = part.split(":")
            last = part == word.split("|")[-1]
            tr[name]["notes"].append({"at": round(at, 4), "len": round((int(n16) - (0.4 if last else 0)) * six, 4), "pitch": pitch, "vel": 0.85, "ph": ph,
                                      **({"gain": f"{float(gain):g}dB"} if float(gain) else {})})
            at += int(n16) * six
        assert abs(at - t1) < 1e-6 or int(bars) != 1, "the word is as long as the bar"
    if crash:
        piece, vel = crash.split(":")
        assert any(abs(n["at"] - t1) < 1e-4 for n in tr["cym"]["notes"]), "the cymbal already strikes where the band comes in"
        tr["cym"]["notes"].append({"at": round(t1, 4), "len": 2 * six * 4, "pitch": piece, "vel": float(vel)})
        tr["cym"]["notes"].sort(key=lambda n: n["at"])
    if target:
        doc["loudness"] = float(target)
    return out


# v20 (chirper-three; instrument round: THE RIFF GUITARS' MUTED STROKE, both pairs: 688 of the 1236 notes on gl, gr, dl,
# dr and their lifted halves). No note changes; the wall pair and the last chord's tracks are not touched.
# THE READ (tools/riffpunch.py --strokes beside six records' strokes; the records: the low end's fall after a stroke
# -1.1, never over +0.3; teeth, 1-4 kHz over 400 Hz-1 kHz through a stroke, 11.3, never under 6.5). The first pair
# (the gojira rig as v8 left it): fall -0.22, +2.81, +3.36, +0.62 and teeth 7.7, 5.6, 5.8, 7.4 in 'minor', 'sixth',
# 'common', 'home': the low end died after the stroke in three sections of four and there were no teeth in two, and
# worst of all in 'common', the low C the whole song arrives at. The second pair (the modern rig, A flat and C an
# octave higher; 'sixth', 'common', 'home'): fall -1.15, +0.80, -2.19, teeth 8.1, 7.6, 8.5, and a hit too large for
# its body (punch 4.78, 4.21, 5.00; the records 3.5 to 4.2). By part the guitars stood 1.9 to 5.3 dB over the
# records' guitars at 500 Hz-1 kHz.
# ONE CONTROL AT A TIME (first pair; minor, sixth, home): the palm closing the string's filter two octaves, not 3.4,
# alone: teeth 9.5, 7.1, 9.1 and the fall no better (+0.66, +2.69, +0.55) ; the pick half as soft under the palm
# alone: the fall -0.56, +1.51, +0.46, teeth no better ; both: -1.20, +1.32, +0.01 and 9.9, 6.7, 8.4. On the second
# pair the filter alone is the cure (punch 4.13, 4.32; teeth 10.3, 10.5) and the pick is a cost (the fall -2.06,
# -2.66, under the records' range; in 'common' +2.04 at 0.7 and +1.94 at 0.85): so it has the filter and not the pick.
# THEN THE BODY. The cure took 2.3 to 3.0 dB of the pairs' 60-250 Hz and made the stroke brighter. First pair: +5 dB
# at 190 Hz gives its 120-250 Hz back (alone: 0.0, +0.1 against v19), -3 dB at 650 Hz takes the box (-2.4, -2.5),
# and its microphone moves 0.5 -> 0.55 so its top is where it was in 'minor' and 'home' (within 0.5 dB at 2-16 kHz;
# in 'common', where 84 of its 113 strokes are muted, 2-4 kHz is 1.5 dB up). In 'common' the low C's own fundamental
# (70 Hz) had lost 4.5 dB: a band at 72 Hz comes up 4 dB for as long as 'common' lasts (a lane on the lifted
# tracks: -1.9). Second pair: +2 dB at 105 Hz (its 60-120 Hz -2.2, -1.9 -> -0.6, -0.4) and its microphone 0.35 ->
# 0.4; no fader moves (the second pair against the first -3.16 -> -3.00, -3.21 -> -3.22, -2.72 -> -2.57 dB K).
# AFTER. First pair: the fall -1.20, +0.71, +1.20, -0.26 ; teeth 11.1, 7.8, 10.7, 9.7 ('minor' at the records'
# median on both; teeth inside their range in all four; the fall inside it in two, NOT CURED in 'sixth', whose
# stroke is an octave up, and 'common'). Second pair: teeth 9.9, 9.4, 10.1 ; punch 4.51, 3.75, 4.89. The eight
# tracks alone beside a record's guitar alone (tools/cabspec.py, after the bar): 2.31 -> 1.97, 2.69 -> 2.40, 2.40
# -> 2.08. By part at 500 Hz-1 kHz: +1.9, +2.2, +4.7, +4.4, +5.3 -> 0.0, +0.9, +3.9, +3.2, +4.9.
# THE MIX'S READ IS LEVEL, and that is the truth of it: against the records' passages without a voice, mean of five
# sections, 1.187 -> 1.171 ; against all eleven 1.238 -> 1.280. The first candidate, with the microphones where
# they were, read further on both (2-4 kHz, already 0.8 to 1.6 over in the loud sections, rose 0.3 to 0.6). WHY the
# mix does not follow the guitars: in 'common' and 'home' THE LEAD holds 39 to 42% of the mix's power at 500 Hz-1
# kHz, 40 to 46% at 1-2 kHz and 42 to 44% at 2-4 kHz, and the wall pair 25 to 31% at 500 Hz-1 kHz; the eight riff
# tracks 8 to 18% at 500 Hz-1 kHz (shares read on the first candidate). The mix's +3.0 and +2.5 dB at 500 Hz-1 kHz
# and 1-2 kHz in 'home' are theirs.
# COSTS: the second pair's low end falls faster in 'common' (+0.80 -> +1.72) ; the first pair's stroke is cleaner
# (grain 0.39, 0.32, 0.37, 0.39 -> 0.35, 0.26, 0.26, 0.34; the records 0.3 to 0.4) and rises 1 to 1.75 ms sooner in
# 'sixth' and 'home' (13.5, 13.25: the records' lower edge) ; 'common' is 0.15 to 0.21 dB louder in the finished
# file ; the other guitar sections 0.07 dB lower to 0.01 higher. Where no riff guitar sounds (the opening, 'fourth',
# 'wound', the last chord) the file is within 0.025 dB of v19 on three seeds; the target is not moved.
BITE = os.environ.get("C10T14_BITE", "synth.filters.0.cutoff.mod.0.amount=-2 synth.layers.0.soft=expr.pm*0.5 fx.2.mic=0.55;"
                      "peak cutoff=190 q=1 gain=5dB|peak cutoff=650 q=1 gain=-3dB;72:1.4:4:common;"
                      "synth.filters.0.cutoff.mod.0.amount=-2 fx.2.mic=0.4;peak cutoff=105 q=1 gain=2dB;" if SIXTEEN else "")


def the_chug_bites(doc):
    """v20: the two riff pairs' muted stroke gets its teeth and keeps its low end; the last chord's tracks are not touched."""
    over_a, eq_a, follow, over_b, eq_b, target = BITE.split(";")
    pairs = {"gl": 0, "gr": 0, "gl-up": 0, "gr-up": 0, "dl": 1, "dr": 1, "dl-up": 1, "dr-up": 1}

    def beat(s16):                                                 # a section's start in declared beats (v18's change of gear)
        gear = GEAR.split(";") if GEAR else None
        if not gear or s16 <= AT[gear[0]]:
            return s16 / 4
        num, den = (int(x) for x in gear[1].split("/"))
        return (AT[gear[0]] + (s16 - AT[gear[0]]) * den / num) / 4
    seen = 0
    for t in doc["tracks"]:
        k = pairs.get(t["name"])
        if k is None:
            continue
        seen += 1
        over, eq = ((over_a, eq_a), (over_b, eq_b))[k]
        if over:
            t["patch"] += " " + over
        t["fx"] = json.loads(json.dumps(t["fx"]))                  # its own objects: the last chord's tracks share the old ones
        assert t["fx"][0]["type"] == "eq", t["fx"]
        if eq:
            t["fx"][0]["bands"] += eq.split("|")
        if k == 0 and follow:
            hz, q, db, section = follow.split(":")
            names = [n for n, _ in FORM]
            a, z = beat(AT[section]), beat(AT[names[names.index(section) + 1]])
            if any(a <= n["at"] < z for n in t["notes"]):          # only the track that plays there
                t["fx"][0]["bands"].append({"kind": "peak", "cutoff": float(hz), "q": float(q),
                                            "gain": {"value": "0dB", "mod": [{"src": "auto.chug", "amount": 1}]}})
                t["auto"] = {**t.get("auto", {}), "chug": {"curve": 0, "points": [
                    ["0b", 0], [f"{a - .02:g}b", 0], [f"{a:g}b", float(db)], [f"{z - .02:g}b", float(db)], [f"{z:g}b", 0]]}}
    assert seen == len(pairs), seen
    if target:
        doc["loudness"] = float(target)


# v21 (chirper-zero; instrument round: the wall pair, 96 chords on wl, wr and their lifted halves): THE WALL COMES
# OUT OF ITS BOX. The pair that holds the chord under the riff and the tune (minor, sixth, common, home, the last
# chord) was the one guitar here still on the library's impulse response. Read alone beside a record's guitars
# (tools/cabspec.py; 'home', F2 C3 F3) it stood 5.10 from them: a box, +8.9, +9.2, +11.3, +8.8 dB at 400, 500, 630
# and 800 Hz, and no top at all (-12.7, -18.2, -13.8 dB at 8, 10 and 12.5 kHz). chirper-three's shares (v20) say
# whose the mix's middle is: the pair holds 25 to 31% of the mix's 500 Hz-1 kHz in 'common' and 'home' and 18 to
# 24% of its 250-500 Hz, where the mix stands +2.1 and +3.0 dB over the records.
# Harry, 17 Nov, of the wall pairs: onto the engine's cabinet. Done on tracks 9, 11, 1, 7, 15 and 8; now here.
#   the engine's 4x12 (mic 0.4, 15 cm, cones 144 / 145), the library IR off, the patch's own eq flat   3.51
#   mic 0.5 / 0.3 / 30 cm                                                                           3.56 / 3.57 / 3.55
#   and a chest, 190 Hz +5 dB                                                                           2.98
#   and the rig's own middle out, 600 Hz q 0.9 -6 dB, the chest a little wider (200 Hz q 0.8 +6 dB)     2.40
#   (the amp's mid control: nothing; a 2.6 kHz cut: 2.46; a notch at 400 Hz: 2.57)
# THE FADER: at -0.3 dB the pair alone is as loud as it was (-24.1 LUFS); the mix read best a decibel under that
# (the pair has a top now, and the mix's 2-4 kHz is already over): -1.3 dB.
# THE MIX (stembal --voice, the four sections the pair plays in, weighted by its chords): the rows WITHOUT a voice
# 1.329 -> about 1.17 (250-500 Hz +1.80 -> +1.17, 500 Hz-1 kHz +2.19 -> +1.3); the rows WITH a voice 1.271 ->
# about 1.29, level: against sung records 500 Hz-1 kHz was already 1.4 dB short and is now 2.3. Nobody sings in
# these sections (the tune is a guitar), so the first is the yardstick; the second is said because chirper-three
# asked that the tune be read against it. If an ear wants that middle back it belongs to the TUNE (its eq cuts
# 700 Hz by 5 dB), not to the wall's box.
# THE TARGET -10.66 -> -10.72: with the pair a decibel down the master came up 0.07 dB where no wall plays; at
# -10.72 'fourth' (the quiet middle) nulls against v20 at -0.004 dB.
# C10T14_WALLCAB = the microphone ; the two cones ; its distance in metres ; the track's eq after the cabinet,
# band|band ; the fader ; the loudness target. '' = v20 byte for byte. On only while BITE is.
WALLCAB = os.environ.get("C10T14_WALLCAB", "0.4;144,145;0.15;peak cutoff=200 q=0.8 gain=6dB|peak cutoff=600 q=0.9 gain=-6dB;-1.3dB;-10.72" if BITE else "")


# v22 (chirper-one; section round, window 1, 0:00-0:31: the unwinding, 0:02.0-0:07.8). THE CHORD FALLS THROUGH THE
# FLOOR. The song's first sentence is that a chord is a rhythm too fast to count, and it is said by three drums
# alone: the rolls slow an octave a bar until they are threes, fours and fives. But a drum keeps its own pitch
# while its roll slows, so the NOTE that the roll's speed is was never heard to fall. Three sines now sound each
# roll's own stroke rate (174.6, 131.0 and 104.8 Hz when the unwinding starts) and fall with it, an octave a bar,
# one note each with its pitch on a lane, through a high-pass at 40 Hz: the chord sinks, goes under hearing about
# 0:06, and what is left is the strokes, by then slow enough to count (the voices begin "three" at 0:04.5).
# NOT IN THE HELD BAR: a sine on a rolled drum's own note adds or cancels with it by phase (benched: the mix's
# C3 line 6.8 dB DOWN with the sine there, its F3 1.8 up). So the sines come in over a second as the roll leaves
# the drums' notes; from there the two add as powers within 0.6 dB.
# HOW (for whoever wants a glide): `play.mono` with `glide` restarts the envelope at every note (a 1 s attack
# never rose: the sines read 19 dB under what the fader gives); a lane on the TRACK (`auto`) riding the patch's
# `synth.pitch` (in semitones) moves one held note exactly: the F sine read 160.4, 134.8, 113.5, 95.6, 80.2 Hz
# where the roll's rate is 160.1, 134.7, 113.2, 95.2, 80.1.
# the sines' fader ; their attack ; the floor: a high-pass on each, Hz ; bars the fall is written for ; their pans
# (the F, the C, the A flat: the three drums' own places) ; the loudness target ('' = unchanged). '' = v21 byte for
# byte. On only while WALLCAB is.
FLOOR = os.environ.get("C10T14_FLOOR", "-14dB;1000ms;40;3;-0.5,0,0.5;" if WALLCAB else "")


def the_chord_falls_through_the_floor(doc):
    """v22: as the three rolls slow, three sines sound each roll's own stroke rate and fall with it, an octave a bar, until they are under hearing."""
    fader, attack, floor, bars, pans, target = FLOOR.split(";")
    start, bars = AT["unwound"] / 4, int(bars)
    assert start == BAR / 4 * int(ROLL.split(";")[3]) and "sc-floor" not in doc["patches"]
    doc["patches"]["sc-floor"] = {"extends": "808", "synth": {"layers": ["sine"], "pitch": {"value": 0, "mod": [{"src": "auto.fall", "amount": 1.0}]},
                                                               "drive": 0, "filters": [], "amp": {"a": attack, "d": 0, "s": 1, "r": "80ms"}},
                                  "play": {"mono": False, "glide": "0ms", "gate": 1}}
    for (name, period), pan in zip((("floor-f", DRUMS["t1"]), ("floor-c", DRUMS["t2"]), ("floor-a", DRUMS["t3"])), pans.split(",")):
        doc["tracks"].append({"name": name, "patch": "sc-floor", "gain": fader, "pan": float(pan),
                              "notes": [{"at": start, "len": BAR / 4 * bars, "pitch": f"{F3 * 3 / period:.3f}hz", "vel": 0.8}],
                              "auto": {"fall": {"points": [["0b", 0], [f"{start:g}b", 0], [f"{start + BAR / 4 * bars:g}b", -12 * bars]], "curve": 0}},
                              "fx": [{"type": "eq", "bands": [f"hp cutoff={floor} q=0.7", f"hp cutoff={floor} q=0.7"]}]})
    if target:
        doc["loudness"] = float(target)


def the_wall_comes_out_of_its_box(doc):
    """v21: the wall pair on the engine's cabinet (the library IR off, the patch's eq flat), a chest and the rig's
    middle out on the track; the fader a decibel under equal loudness alone."""
    mic, cones, distance, eq, fader, target = WALLCAB.split(";")
    cone = dict(zip("lr", (int(c) for c in cones.split(","))))
    flat = " fx.3.mix=0 fx.4.bands.0.gain=0dB fx.4.bands.1.gain=0dB fx.4.bands.2.gain=0dB fx.4.bands.3.gain=0dB"
    seen = 0
    for t in doc["tracks"]:
        if t["name"] not in ("wl", "wr", "wl-up", "wr-up"):
            continue
        seen += 1
        head, _, rest = t["patch"].partition(" ")
        t["patch"] = head + flat + (" " + rest if rest else "")
        t["fx"] = [{"type": "cab", "model": "4x12-modern", "mic": float(mic), "distance": float(distance), "cone": cone[t["name"][1]]}]
        if eq:
            t["fx"].append({"type": "eq", "bands": eq.split("|")})
        if fader:
            t["gain"] = fader
    assert seen == 4, seen
    if target:
        doc["loudness"] = float(target)


# v23 (chirper-three; instrument round: THE LEAD, the tune's guitar: 139 notes, 0:57.7-2:54.7, and the last chord's).
# THE TUNE IS THE VOICE. Three reads, three cures; no note changes and no other track changes.
# (1) ITS NOTES. The lead alone, echo and room off, every note of 0.3 s or longer against its written note in the
#   song's tuning (108 notes; pitch.py): the median note stood 5.6, 4.1 and 5.6 cents SHARP on seeds 1, 0 and 11 (the
#   high F 12.2), in a song whose notes are ratios of the count and whose clean guitars and still chords are on
#   them. It is the plucked string (the bead v3 asked for; `tune_sounding` since engine batch 64). With the switch:
#   -0.4, -1.4, -0.6; the mean distance 6.3, 6.1, 6.9 -> 3.4, 4.2, 3.5. What is left (-20 to +10 note to note) is the
#   player: its vibrato and its random detune, kept. The last chord's note keeps v3's trim (read -2.8, -1.1, +0.5
#   as it is; -3.5, -0.3, -1.1 with the switch and no trim: no better, left).
# (2) ITS ECHO. v2 made the echo three sixteenths: by the rule, an F. v18 (mine) wrote the change of gear into the
#   positions and left the tempo, so from 2:10.97 the echo was still three OLD sixteenths: 366.56 ms measured, where
#   three of the lifted count are 343.61. Every repeat fell 22.9 ms behind the count, and by the rule it said the old
#   F. Now 343.65 measured. (The echoes together are 21 dB under the dry lead: small, but the rule's. When the song
#   goes back to a tempo map, bd-10e881, this override must come out: 3/16 then follows by itself.)
# (3) ITS TONE AND LEVEL, read as what it is here, the song's voice (tools/voxref.py: the lead alone and the mix,
#   beside eleven records' voices and their mixes). Its own shape less the records' voices', 'minor' and 'sixth' /
#   'common' and 'home': 500 Hz-1 kHz -4.0 / -3.5, 2-4 kHz +5.1 / +5.7, 4-8 kHz +2.0 / +1.8. Its level against the
#   whole mix while it plays: -6.6 / -6.6 dB (the records' voices -9.2, their middle half -9.7 to -8.9), and at
#   1-4 kHz -3.4 / -3.3 (the records -7.1). So: a thin, biting lead, 2.6 dB louder than a record's voice and 3.8
#   louder where the ear is sharpest; and the mix stood 1.3 to 2.5 dB over the records at 2-4 kHz in its four
#   sections, with the lead 45 to 47% of that band. v5's eq (700 Hz -5 dB, a shelf of +5 dB from 4 kHz) was fitted
#   when the wall pair was a box; v21 took the wall's box out. NOW: the 700 Hz cut eased to 2 dB, 6 dB out at
#   2.8 kHz (q 0.8), the shelf moved to 6 kHz (+6 dB: the pick, without the bite), the fader -1.5 -> -2.5 dB.
#   AFTER: shape 500 Hz-1 kHz -0.8 / -0.3, 2-4 kHz +0.8 / +1.8, 4-8 kHz -1.6 / -1.5; level -8.3 / -8.8, at 1-4 kHz
#   -5.7 / -6.0. The mix beside the records with their voices, the lead's four sections: 0.800, 1.233, 1.478, 1.122
#   -> 0.678, 0.922, 1.167, 0.856; its 2-4 kHz +1.3, +1.4, +2.5, +1.7 -> -0.3, +0.1, +1.1, +0.5. The lead's share of
#   the mix's 2-4 kHz 45-47% -> 14-17%.
# THE QUIET MIDDLE ('fourth') IS NOT RE-VOICED: nothing there was read, and it is chirper-two's. Wherever the fader
#   already rides, lanes put the three bands and the fader back to v22's (the lead alone there nulls against v22's
#   at -82 dB with the string as it was); only its notes are truer.
# HELD: a quieter lead makes the file measure quieter and the master turned everything else up 0.30 to 0.54 dB, so
#   the target goes -10.72 -> -11.05 (1.0 dB of gain per dB on the band, 1.6 on the sparse stretches): every stretch
#   without the lead is within 0.021 dB of v22 on three seeds (-60.8 dB or lower), 'fourth' within 0.014.
# COSTS: the tune is 2.8 to 4.0 dB less forward by the meter (-4.7, -4.8, -5.4, -4.7 -> -7.5, -7.8, -9.4, -8.1 dB K
#   against everything else); beside the records' VOICELESS passages the mix is 1 dB further over at 500 Hz-1 kHz
#   in 'minor', 'sixth' and 'home' (+1.7, +1.5, +1.8 -> +2.8, +2.4, +2.7); the last chord is 0.14 to 0.33 dB lower;
#   the scorer's master term falls 4.5 points (the file's RMS is 0.14 dB lower): kept on judgment.
# the string: overrides on the moving lead (`tune`, `tune-up`; the last note keeps v3's trim) ; the lifted lead's
# echo in LIFTED sixteenths ('' = the old count's) ; its eq, three bands: the box | the bite | the pick (a shelf) ;
# dB on its fader ; 'ride' = wherever the fader already rides (the quiet middle) the eq and the fader stay as they
# were, on lanes ('' = the new eq everywhere) ; the loudness target ('' = unchanged). '' = v22 byte for byte. On
# only while FLOOR is.
VOICE = os.environ.get("C10T14_VOICE", "synth.layers.0.tune_sounding=true;3;peak cutoff=700 q=0.8 gain=-2dB|peak cutoff=2800 q=0.8 gain=-6dB|highshelf cutoff=6000 gain=6dB;-1;ride;-11.05" if FLOOR else "")


def the_tune_is_the_voice(doc):
    """v23: the lead on its notes, its echo on the lifted count, and its tone and level where the records put a voice."""
    string, echo, eq, db, keep, target = VOICE.split(";")
    spec = lambda band: dict(x.split("=") for x in band.split()[1:])
    num = lambda v: float(v.rstrip("dB"))
    old = None
    for t in doc["tracks"]:
        if t["name"] not in ("tune", "tune-up", "tune-still"):
            continue
        assert t["patch"].startswith("m8-lead-guitar") and len(t["fx"]) == 1 and t["fx"][0]["type"] == "eq", t["name"]
        if string and t["name"] != "tune-still":
            t["patch"] += " " + string
        if echo and GEAR and t["name"] != "tune":                  # v18 wrote the tempo into the positions: the echo kept the old sixteenth
            up, down = (int(x) for x in GEAR.split(";")[1].split("/"))
            t["patch"] += f" fx.4.time={float(echo) * 60 / BPM / 4 * down / up * 1000:.3f}ms"
        if eq:
            old = old or [spec(b) for b in t["fx"][0]["bands"]]    # v5's: a peak and a shelf
            assert len(old) == 2 and t["fx"][0]["bands"][1].startswith("highshelf"), t["fx"]
            box, bite, pick = eq.split("|")
            ride = t["auto"]["ride"]["points"]
            if keep == "ride" and any(v for _, v in ride):
                lane = lambda v: {"curve": 0, "points": [[at, round(v, 4) if was else 0] for at, was in ride]}
                t["fx"] = [{"type": "eq", "bands": [
                    {"kind": "peak", "cutoff": num(spec(box)["cutoff"]), "q": num(spec(box)["q"]), "gain": {"value": spec(box)["gain"], "mod": [{"src": "auto.box", "amount": 1}]}},
                    {"kind": "peak", "cutoff": num(spec(bite)["cutoff"]), "q": num(spec(bite)["q"]), "gain": {"value": spec(bite)["gain"], "mod": [{"src": "auto.bite", "amount": 1}]}},
                    {"kind": "highshelf", "cutoff": {"value": num(spec(pick)["cutoff"]), "mod": [{"src": "auto.pickhz", "amount": 1}]},
                     "gain": {"value": spec(pick)["gain"], "mod": [{"src": "auto.pick", "amount": 1}]}}]}]
                assert num(old[0]["cutoff"]) == num(spec(box)["cutoff"]) and num(old[0]["q"]) == num(spec(box)["q"]), "the box must stay where v5 put it for the lane to give v22 back"
                t["auto"] = {**t["auto"], "box": lane(num(old[0]["gain"]) - num(spec(box)["gain"])), "bite": lane(-num(spec(bite)["gain"])),
                             "pickhz": lane(math.log2(num(old[1]["cutoff"]) / num(spec(pick)["cutoff"]))),     # an eq's cutoff rides in octaves
                             "pick": lane(num(old[1]["gain"]) - num(spec(pick)["gain"]))}
                if db:
                    t["auto"]["ride"] = {**t["auto"]["ride"], "points": [[at, round(was - float(db), 4) if was else 0] for at, was in ride]}
            else:
                t["fx"] = [{"type": "eq", "bands": [box, bite, pick]}]
        if db:
            t["gain"] = {**t["gain"], "value": f"{num(t['gain']['value']) + float(db):g}dB"}
    if target:
        doc["loudness"] = float(target)


# v24 (chirper-zero; section round on the map's first flag, w3, 1:02-1:33, 'static, little new': the change is
# 1:19.7-1:34.3, two turns of the sixty inside 'sixth'). HALF AS FAST IS AN OCTAVE DOWN. The song's first sentence
# is that a pulse and a pitch are one thing at two speeds, and "twice as fast is the octave above". The drums prove
# it at both ends of the song (the chord unwinds into a rhythm, the rhythm winds up into the chord); the BAND never
# had: from its first stroke to its last chord every pulse runs at one speed. And the song had no breakdown.
# By its rule they are the same thing. From one meeting of the three pulses to the next but one (the second and
# third of the four turns of 'sixth'; both gathers of v17 are already there, and the band already stops before each)
# the two riff pairs, the foot and the backbeat play AT HALF SPEED, and the pairs and the foot's chest play AN OCTAVE
# LOWER, because that is what half speed is: the threes become sixes, an F an octave down (F1, the eight-string's
# lowest string, which the riff had never used: it has sat on F2 all song); the fives become tens, the A flat an
# octave down; the backbeat comes once a bar instead of twice, on three: still a C. Each pair plays its own four-
# stroke figure (ring, mute, chord, mute) at half the rate, starting again at each meeting; the strokes are as long
# as they were, so there is air between them (benched ringing twice as long: fuller, and the mix read further from
# the records on both yardsticks; with the chest left on F2 the passage lost 1.4 dB under 60 Hz). NOTHING ELSE SLOWS: the D flat on the fifteens and the C on the bar lines (the walls, the bass, the
# deep drum, the C tom: v11's semitone) walk on at their own speed and are heard better for it; the china keeps its
# quarters; the blocks keep the fives; the tune sings over it; the three drums gather at full speed at both
# meetings, and at 1:34.3 the band lands back at speed and at pitch, into the fill that was already there.
# the section ; the meeting it starts at and the one it ends at, sixteenths from the section's start ; semitones on
# the two riff pairs ; semitones on the chest ; the backbeat's place in sixteenths after a meeting's phase, once a
# bar ('' = every second backbeat as written) ; how many times longer the ringing strokes last ; the loudness
# target ('' = unchanged). '' = v23 byte for byte. On only while VOICE is.
OCTAVE = os.environ.get("C10T14_OCTAVE", "sixth;60;180;-12;-12;12;1;-11.109" if VOICE else "")


def half_as_fast_is_an_octave_down(doc):
    """v24: between two meetings of the three pulses the riff pairs, the kick, its chest and the snare play at half
    speed, the pairs and the chest an octave lower (see OCTAVE). Runs last, on the finished document."""
    sect, m0, m1, semis, chest, backbeat, ring, target = OCTAVE.split(";")
    a, z = AT[sect] + int(m0), AT[sect] + int(m1)
    assert int(m0) % 60 == 0 and int(m1) % 60 == 0 and z > a, "it starts and ends where the three pulses meet"
    names = "C Db D Eb E F Gb G Ab A Bb B".split()

    def moved(pitch, st):
        def one(q):
            k = names.index(q.rstrip("0123456789")) + 12 * (int(q[len(q.rstrip("0123456789")):]) + 1) + st
            return names[k % 12] + str(k // 12 - 1)
        return ",".join(one(q) for q in pitch.split(","))

    def s16(n):
        return round(n["at"] * 4, 3)

    def inside(n):
        return a <= s16(n) < z

    by = {t["name"]: t for t in doc["tracks"]}
    for pair, p in (("gl", 3), ("gr", 3), ("dl", 5), ("dr", 5)):
        t = by[pair]
        was = [n for n in t["notes"] if inside(n)]
        mute = next(n for n in was if (n.get("expr") or {}).get("pm"))
        open_ = max((n for n in was if not (n.get("expr") or {}).get("pm")), key=lambda n: n["len"])
        lens = sorted({round(n["len"], 4) for n in was if not (n.get("expr") or {}).get("pm")})[-2:]   # the chord's and the ringing stroke's, as written
        new = []
        for n in was:
            rel = s16(n) - a
            if rel % (2 * p):
                continue
            c = rel % 60                                               # the figure starts again at each meeting
            k = round(c / (2 * p))
            if k % 2:
                m = {**mute, "at": n["at"], "pitch": moved(mute["pitch"], int(semis))}
            else:
                m = {"at": n["at"], "len": round(min((lens[-1] if k % 4 == 0 else lens[0]) * float(ring), (55 - c) / 4 - 0.01), 4),
                     "pitch": moved(open_["pitch"], int(semis)), "vel": 1.0 if k % 4 == 0 else 0.95}
            assert c + m["len"] * 4 <= 55, (pair, rel, m)                   # v17: the band rests from 55 to the meeting
            new.append(m)
        t["notes"] = sorted([n for n in t["notes"] if not inside(n)] + new, key=lambda n: n["at"])
    for name in ("kick", "chest"):
        t = by[name]
        keep = []
        for n in t["notes"]:
            if inside(n):
                rel = s16(n) - a
                if rel % 6:
                    continue
                n = {**n, "vel": 1.0 if (rel % 60) % 24 == 0 else 0.86}
                if name == "chest":
                    n["pitch"] = moved(n["pitch"], int(chest))
            keep.append(n)
        t["notes"] = keep
    t = by["snare"]
    stroke = next(n for n in t["notes"] if inside(n))
    if backbeat == "":
        keep = [n for n in t["notes"] if not (a < s16(n) < z) or (s16(n) - a) % 16 == 0]
    else:
        keep = [n for n in t["notes"] if not (a < s16(n) < z)] + [{**stroke, "at": (a + r) / 4} for r in range(int(backbeat), z - a, 16)]
    t["notes"] = sorted(keep, key=lambda n: n["at"])
    if target:
        doc["loudness"] = float(target)


# v25 (chirper-zero; section round, w6, 2:36-3:11, the map's flag "little new"; the change is the song's last
# sentence before its chord, 'wound', 2:53.1-3:04.1). THE CHORD RISES OUT OF THE FLOOR, AND THE COUNT BACK UP IS TWO
# VOICES. Two things chirper-one and chirper-three both left written down as the next thing here.
# (1) THE MIRROR of v22. The form is the proof both ways: at the start the three rolls slow from a chord to a count
# and v22 let the chord itself be heard sinking under them; at the end the same strokes run backwards, an octave a
# bar faster, until they are the chord again, and the note that their speed IS was not heard coming. Three sines
# now sound each roll's own stroke rate through the last three bars of the wind-up and rise with it, through the
# same floor (a high-pass at 40 Hz), into the notes the drums are rolled at when the band plays the chord: after
# the change of gear those are 186.25, 139.69 and 111.75 Hz (v22's 174.6, 131.0 and 104.8 times 16/15). Each is one
# note with its pitch on the track's lane, written here in the finished document's own beats (the gear's moved
# positions), so nothing has to be lifted. They let go as the chord lands (a sine on a rolled drum's own note adds
# or cancels with it by phase: v22's finding; so they do not stay for the held roll).
# (2) THE OCTAVE VOICES. chirper-one's v19 finding: two voices on one patch an exact octave apart are locked, and
# how they add is the seed's; his cure there was the high voice 8 cents over its octave, and he and chirper-three
# both listed this count ("twelve, eleven ... three", 2:54.8-3:03.4) as still exact. The high voice is now 8 cents
# over here too (its patch's pitch; the low voice is the one on the notes).
# the sines' fader ; bars the rise is written for ; the floor, Hz ; their release ; their pans (F, C, A flat: the
# drums' own places) ; cents on the high voice of the count back up ('' = none) ; the loudness target ('' =
# unchanged). '' = v24 byte for byte. On only while OCTAVE is. The target -11.109 -> -11.1034: the wind-up's last
# three bars are 0.46 dB louder and the master had turned everything else down 0.0055 dB; three targets and a line.
RISE = os.environ.get("C10T14_RISE", "-14dB;3;40;80ms;-0.5,0,0.5;8;-11.1034" if OCTAVE else "")


def the_chord_rises_out_of_the_floor(doc):
    """v25: through the wind-up's last bars three sines sound each roll's own stroke rate and rise with it into the
    last chord; the count back up's high voice stands 8 cents over its octave. Runs last, on the finished document."""
    fader, bars, floor, release, pans, cents, target = RISE.split(";")
    num, den = (int(x) for x in GEAR.split(";")[1].split("/"))
    at = AT[GEAR.split(";")[0]] / 4
    end = at + (AT["one chord"] / 4 - at) * den / num                    # where the band plays the chord, in the document's beats
    bar = BAR / 4 * den / num
    start = end - int(bars) * bar
    toms = next(t for t in doc["tracks"] if t["name"] == "toms-up")
    assert abs(min(n["at"] for n in toms["notes"] if n["at"] >= start - 1e-6) - start) < bar and "sc-rise" not in doc["patches"]
    doc["patches"]["sc-rise"] = {"extends": "808", "synth": {"layers": ["sine"], "pitch": {"value": 0, "mod": [{"src": "auto.rise", "amount": 1.0}]},
                                                              "drive": 0, "filters": [], "amp": {"a": "1000ms", "d": 0, "s": 1, "r": release}},
                                 "play": {"mono": False, "glide": "0ms", "gate": 1}}
    for (name, period), pan in zip((("rise-f", DRUMS["t1"]), ("rise-c", DRUMS["t2"]), ("rise-a", DRUMS["t3"])), pans.split(",")):
        doc["tracks"].append({"name": name, "patch": "sc-rise", "gain": fader, "pan": float(pan),
                              "notes": [{"at": round(start, 6), "len": round(end - start, 6), "pitch": f"{F3 * 3 / period * num / den:.3f}hz", "vel": 0.8}],
                              "auto": {"rise": {"points": [["0b", -12 * int(bars)], [f"{start:g}b", -12 * int(bars)], [f"{end:g}b", 0]], "curve": 0}},
                              "fx": [{"type": "eq", "bands": [f"hp cutoff={floor} q=0.7", f"hp cutoff={floor} q=0.7"]}]})
    if cents:
        high = next(t for t in doc["tracks"] if t["name"] == "count-high-up")
        assert "synth.pitch.value" not in high["patch"]
        high["patch"] += f" synth.pitch.value={float(cents) / 100:g}"
    if target:
        doc["loudness"] = float(target)


# v26 (chirper-zero; instrument round: the two sung octave pairs still exact: the count at the opening, 0:04.5-0:21,
# and the middle's numbers, 1:41.6-2:12.8; no note changes). THE OCTAVE HOLDS.
# Two voices of one patch an exact octave apart share every partial the upper one has, and each note's two streams
# start by the draw: so where their partials meet they add or cancel for the WHOLE note, by luck. Read alone on eight
# seeds (0 1 2 3 5 7 11 13), note by note: the count's level moved 3.08 dB with the seed on the average note (5.8 at
# worst; 13 of 28 notes over 3 dB), the middle's 4.13 (9.0 at worst; 14 of 22). AND AT THE SONG'S OWN SEED the luck
# is in the file: the middle says "fifteen" six times, and in the finished file its held "teen" stood 5.6 dB apart
# from one saying to the next (-18.7 -23.1 -18.1 -20.3 -17.5 -18.8 in the voices' band).
# EACH PAIR BY ITS OWN READ; the cures differ because the fault sits in different places.
#   THE COUNT: short notes on many pitches. The upper voice 12 cents over the octave (v25's cure, read here on 3, 5,
#   8, 12, 16 and 20 cents: 12 is where it is steady): 3.08 -> 1.81 dB with the seed, 13 notes over 3 dB -> 1.
#   THE MIDDLE: twelve of its 22 notes are D flat and held for more than a second, and on "teen" the vowel's low
#   formant (about 280 Hz) IS the upper voice's fundamental lying on the lower voice's second partial: one pair of
#   partials carries the word. The cents alone even the words (4.13 -> 1.72) but turn that pair through itself INSIDE
#   each held note: a "teen" in the finished file then swung 6.0 dB where it swung 1.9. A high-pass alone (the upper
#   voice gives the low note to the lower: 150 -> 500 Hz, its fader +2 dB so the pair is as loud as it was on the
#   average seed) stops the swing but is half a cure (2.38). BOTH TOGETHER: 4.13 -> 1.51 dB with the seed (worst 9.0
#   -> 2.5; none over 3), and a held note swings 2.9 dB where it swung 3.2 as shipped.
# BENCHED AND NOT TAKEN: the upper voice with a vibrato of its own (half a cure); both voices' draws switched off
# (the two streams still start apart: no cure); the high-pass on the count back up (no cure there: read). The count
# back up (v25, 8 cents) is not touched.
# per upper voice, | between: track : cents over ('' = none) : its high-pass in Hz ('' = as it was) : dB on its fader
# ('' = none) ; the loudness target ('' = unchanged). On only while RISE is. '' = v25 byte for byte.
PAIRS = os.environ.get("C10T14_PAIRS", "count-high:12::|said-high:12:500:2;-11.1128" if RISE else "")


def the_octave_holds(doc):
    """v26: each exact octave pair's upper voice, by its own read (see PAIRS). No note changes."""
    specs, target = PAIRS.split(";")
    for spec in specs.split("|"):
        name, cents, hp, db = spec.split(":")
        t = next(t for t in doc["tracks"] if t["name"] == name)
        assert t["patch"].startswith("voice-hook") and "synth.pitch.value" not in t["patch"] and isinstance(t["gain"], str), (name, t["patch"])
        if cents:
            t["patch"] += f" synth.pitch.value={float(cents) / 100:g}"
        if hp:
            e = t["fx"][0]
            assert e["type"] == "eq" and e["bands"][0] == "hp cutoff=150", e
            t["fx"] = [{**e, "bands": [f"hp cutoff={float(hp):g}"] + list(e["bands"][1:])}] + list(t["fx"][1:])   # new objects: tracks may share theirs
        if db:
            t["gain"] = f"{float(t['gain'][:-2]) + float(db):g}dB"
    if target:
        doc["loudness"] = float(target)


# v27 (chirper-zero; instrument round: THE SNARE, 85 full strokes, none moved; the rim strokes of 'fourth' are another
# piece and are not touched): THE BACKBEAT STOPS RINGING AT ITS BOX. The notes are beside the function.
# fields of the snare's own drum model (kit.s.patch.synth.layers.0), space between ; its filter list after the 150 Hz
# high-pass, | between ('' = as v9 left it) ; the piece's gain, dB ('' = as it is) ; the loudness target ('' =
# unchanged). In both kits (the lifted half's too). On only while PAIRS is. '' = v26 byte for byte.
DAMPED = os.environ.get("C10T14_DAMPED", "decay=0.13s damp=0.9 wires=0.72;peak cutoff=262 q=1 gain=-1dB|peak cutoff=650 q=1 gain=-3dB;2.65;-11.16" if PAIRS else "")


def the_backbeat_stops_ringing(doc):
    """v27: the snare's head is damped and shorter. No note, track, bus or send changes: only the piece `s` of the
    song's two kits (new objects: nothing else that shares them is changed in place)."""
    fields, body, own, target = DAMPED.split(";")

    def num(v):
        try:
            return float(v) if "." in v else int(v)
        except ValueError:
            return v
    for name in ("ct-kit-here", "ct-kit-here-up"):
        if name not in doc["patches"]:
            continue
        kit = doc["patches"][name]
        s = kit["kit"]["s"]
        layer = dict(s["patch"]["synth"]["layers"][0])
        assert layer["type"] == "drum" and s["patch"]["synth"]["filters"][0] == "hp cutoff=150", s
        for f in fields.split():
            k, v = f.split("=", 1)
            assert k in layer or k == "mode_count", k              # a field of the drum's model
            layer[k] = num(v)
        synth = {**s["patch"]["synth"], "layers": [layer] + list(s["patch"]["synth"]["layers"][1:])}
        if body:
            synth["filters"] = ["hp cutoff=150"] + [x for x in body.split("|") if x]
        doc["patches"][name] = {**kit, "kit": {**kit["kit"], "s": {**s, "patch": {**s["patch"], "synth": synth}, **({"gain": f"{float(own):g}dB"} if own else {})}}}
    if target:
        doc["loudness"] = float(target)


# v28 (chirper-zero; section round, w2, 0:31-1:02, the one window no round had worked: the change is 0:50.3-0:57.7,
# the second turn of the sixty inside 'minor'). TWICE AS FAST IS THE OCTAVE ABOVE. The mirror of v24, and the half
# of the song's first sentence the band had never played: "twice as fast is the octave above". The drums say it at
# both ends and in every fill; since v24 the band says "half as fast is an octave down" in 'sixth'. In 'minor',
# which is the chord at speed, nothing ever left that speed: from the C's handover (0:35.7) to the tune (0:57.7)
# the band played three turns alike. Now, from the meeting the three drums gather into (0:50.3) to the meeting
# the tune comes in on (0:57.7), the two riff pairs, the foot and the foot's chest SAY THE WHOLE TURN TWICE IN THE
# TIME OF ONE, AN OCTAVE HIGHER: the threes become a stroke every sixteenth and a half on F2 (the riff's own four-
# stroke figure, ring, mute, chord, mute, each stroke half as long), the fives a stroke every two and a half on
# A flat 3, the chest F3 (the F drum's own note), and the backbeat comes every four instead of every eight, on the
# off-beats of the china's quarters: still a C. By the rule every one of them is still on its own note. The first
# strokes after the meeting fall at 1.5 (F), 2 (C, the snare) and 2.5 (A flat): v17's figure of three in a row,
# which the three drums say at 3, 4 and 5 over them, said at twice the speed under it. NOTHING ELSE SPEEDS UP: the
# bass goes round the chord at its own speed (chirper-alpha's v12), the wall holds, the china keeps its quarters,
# the blocks keep the fives, and chirper-one's fill (the cycle in fifteen: four times as fast) comes where it
# came: so the last second and a half is the band at twice the speed under the drums at four times, an octave a
# step, and the band lands at speed and at pitch as the tune begins.
# READ (raw, by band): the kick's band repeats at a sixteenth and a half (the envelope's likeness to itself at that
# lag, 30-60 Hz: -0.41 -> +0.89); the snare's at four (500 Hz-1 kHz +0.07 -> +0.30). The guitars' stroke rate is
# NOT read in the mix's envelope (a saturated chug is flat); alone each pair's figure repeats twice as often (the F
# pair at 3 where it was 6: +0.28 -> +0.85; the A flat pair at 2.5: -0.43 -> +0.50). BENCHED with the chest left
# on F2: 60-120 Hz +1.1 dB instead of -0.4, 120-250 +0.2 instead of +1.8; the rule's octave kept.
# the section ; the meeting it starts at and the one it ends at, sixteenths from the section's start ; semitones on
# the two riff pairs ; semitones on the foot's chest ; the backbeat's place in sixteenths after the meeting, then
# every four ; how many times as long each stroke lasts ; dB on the four riff tracks' strokes there ('' = none: a
# note's gain goes into the amp) ; the loudness target ('' = unchanged). '' = v27 byte for byte. On only while
# DAMPED is.
TWICE = os.environ.get("C10T14_TWICE", "minor;60;120;12;12;2;0.5;;-11.142" if DAMPED else "")


def twice_as_fast_is_the_octave_above(doc):
    """v28: between two meetings of the three pulses the riff pairs, the kick and its chest say the whole turn of sixty
    twice in the time of one, the pairs and the chest an octave higher, and the backbeat comes twice as often (see
    TWICE). Runs last, on the finished document; the mirror of half_as_fast_is_an_octave_down."""
    sect, m0, m1, semis, chest, backbeat, short, gain, target = TWICE.split(";")
    a, z = AT[sect] + int(m0), AT[sect] + int(m1)
    assert int(m0) % 60 == 0 and z - a == 60, "one turn of the sixty, from a meeting to the next"
    names = "C Db D Eb E F Gb G Ab A Bb B".split()

    def moved(pitch, st):
        def one(q):
            k = names.index(q.rstrip("0123456789")) + 12 * (int(q[len(q.rstrip("0123456789")):]) + 1) + st
            return names[k % 12] + str(k // 12 - 1)
        return ",".join(one(q) for q in pitch.split(","))

    def s16(n):
        return round(n["at"] * 4, 3)

    def inside(n):
        return a <= s16(n) < z

    def twice(n, st, length=1.0):
        """One written stroke, said at half its distance from the meeting, and again half a turn later."""
        out = []
        for again in (0, 30):
            m = {**n, "at": round((a + (s16(n) - a) / 2 + again) / 4, 5), "len": round(n["len"] * length, 4)}
            if st:
                m["pitch"] = moved(n["pitch"], st)
            out.append(m)
        return out

    by = {t["name"]: t for t in doc["tracks"]}
    for pair, p in (("gl", 3), ("gr", 3), ("dl", 5), ("dr", 5)):
        t = by[pair]
        was = [n for n in t["notes"] if inside(n)]
        assert [s16(n) - a for n in was] == list(range(0, 60, p)), (pair, "the whole turn, every stroke of it")
        new = [m for n in was for m in twice(n, int(semis), float(short))]
        if gain:
            new = [{**m, "gain": gain} for m in new]
        t["notes"] = sorted([n for n in t["notes"] if not inside(n)] + new, key=lambda n: n["at"])
    for name in ("kick", "chest"):
        t = by[name]
        was = [n for n in t["notes"] if inside(n)]
        assert [s16(n) - a for n in was] == list(range(0, 60, 3)), name
        new = [m for n in was for m in twice(n, int(chest) if name == "chest" else 0)]
        t["notes"] = sorted([n for n in t["notes"] if not inside(n)] + new, key=lambda n: n["at"])
    t = by["snare"]
    was = [n for n in t["notes"] if a < s16(n) < z]
    stroke, last = was[0], max(s16(n) for n in was)                    # v4: the snare leaves for the fill; it still does
    new = [{**stroke, "at": q / 4} for q in range(a + int(backbeat), int(last) + 4, 4) if q > a]   # the meeting's own stroke stays
    t["notes"] = sorted([n for n in t["notes"] if not (a < s16(n) < z)] + new, key=lambda n: n["at"])
    if target:
        doc["loudness"] = float(target)


# v29 (chirper-zero; palette round; the quiet middle, 'fourth', 1:41.6-2:11.0; the backbeat's 30 rim strokes get a
# piece of the song's own, and 43 strokes on two new blocks; no other note, sound or fader changes): THE VALLEY
# KEEPS TIME ON THREE WOODS.
# Every drum in this song is on the note its count is: the toms, the snare (v9), the tablas (v6), the blocks (v7).
# The valley's backbeat was the one that was not. chirper-two made the valley (v14) and wrote down what it lacked:
# "(3) The rim on the rule's C: a designed piece in the song's kit (a knock at 523.84 Hz, a wood at 1396.9, the F
# three octaves up); the note-level override of the library piece did nothing measurable. (4) My v7 idea, a soft
# block each for the nines and the fifteens." chirper-one carried both under v15; nobody built either.
# WHY THE OVERRIDE DID NOTHING (the rim alone, dry: off its bus and its sends): the library's side stick is over in
# 10 ms (-19, -45, -63 dBFS by hundredths of a second). It is a click; for that moment its knock stands at 539.8 Hz,
# 52 cents over the rule's C. With his two frequencies and nothing else it reads in the mix the same to the hertz
# (513.4 and 1439.9 against 513.1 and 1440.3): what is read there is the KIT'S ROOM, whose first 60 ms answer any
# click at 513, 720 and 1440 Hz. The piece has to RING before its tuning can be heard.
# THE RIM is the library's stick whole, click and filters as they were, but the knock and the wood each have an
# envelope of their own that falls in a straight line: the knock a sine on C over 150 ms (4.5 dB every hundredth of
# a second: a tock, not a tone), the wood a triangle on the threes' F over 60 ms. Dry: 523.7 and 1397.1 Hz. Its gain
# is -14.4 dB (the library's -5), so a stroke is as loud as it was (K, first 70 ms: -29.7 > -30.0 raw).
# THE BLOCKS are chirper-two's v7 block (a triangle and a 3 ms click through a band-pass on the note): B flat with
# every strum of the left clean guitar (the nines, 27), D flat with every strum of the right (the fifteens, 16).
# ONE MULTIPLIER: each wood is on its own count's rate NINE OCTAVES UP (x512; the toms are on theirs six up): 8 ->
# C 523.84 Hz, 9 -> B flat 465.64, 15 -> D flat 279.38 (and the rim's wood, 3 -> F 1396.91). So the rim and the left
# block are a 9:8 tone apart and tick 9 against 8: interval and rhythm are one ratio, on two pieces of wood, slowly
# enough to count. They fall together at 1:46.0, 1:54.8 and 2:03.6 (the third time with the low block too).
# MEASURED, finished, seed 1, new less old: the rim's strokes K +0.02 dB, the third octave on C +2.7 ; the blocks'
# own third octaves +5.2 and +4.9 dB at their strokes ; the section K -0.03 dB, 250-500 Hz +0.39 ; every other
# stretch is v28 (+0.0013 dB). The read against the records: 'fourth' 2.767 > 2.856 / 2.644 > 2.744 (250-500 Hz,
# already over there: the voices' body), the other eight stretches the same. In the kit's room the rim reads 519.7
# Hz, 14 cents under its C: the room's line at 513 Hz is in every stroke's tail.
# the section ; THE RIM: the count its knock is the note of : the count its wood is the note of : ms the knock's
# level takes to fall : ms the wood's : the piece's gain, dB ('' = the library's side stick stays) ; THE BLOCKS: the
# two counts (the tracks whose strokes they double are clean-l and clean-r) : ms each rings : each piece's gain, dB :
# each one's pan : the new track's fader, dB : velocity ('' = no blocks) ; the loudness target ('' = unchanged).
# '' = v28 byte for byte. On only while TWICE is.
WOODS = os.environ.get("C10T14_WOODS", "fourth;8:3:150:60:-14.4;9:15:92:110:-6.5:-8:-0.5:0.5:6:0.8;" if TWICE else "")


def the_valley_keeps_time_on_three_woods(doc):
    """v29: in 'fourth' the backbeat's rim rings on the rule's C, and a block each doubles the nines (B flat) and the
    fifteens (D flat): three woods, each on the note its own count is, nine octaves up."""
    sec, rim, blocks, target = WOODS.split(";")
    a = AT[sec] / 4
    z = a + dict(FORM)[sec] / 4
    hz = lambda count: round(BPM * 4 / 60 * 512 / float(count), 2)     # the count's own rate, nine octaves up
    track = {t["name"]: t for t in doc["tracks"]}
    kit = dict(doc["patches"]["ct-kit-here"]["kit"])
    if rim:
        knock, wood, kms, wms, gain = rim.split(":")
        strokes = [n for n in track["snare"]["notes"] if a <= n["at"] < z]
        assert strokes and all(n["pitch"] == "ss" for n in strokes) and "ss" not in kit, sec
        # the library's side stick whole (prog-kit's `ss`: a click, a knock, a wood), but the knock and the wood each
        # have an envelope of their own that falls in a straight line, so the knock RINGS; and both are on the rule
        kit["ss"] = {"gain": f"{float(gain):g}dB", "pitch": "C4", "patch": {"play": {"vel_sens": 0.5}, "synth": {
            "amp": {"a": "0.1ms", "d": "400ms", "r": "30ms", "s": 0},
            "env": {"c": {"a": "0.1ms", "d": "6ms", "s": 0}, "k": {"a": "0.1ms", "curve": 0.0, "d": f"{kms}ms", "s": 0},
                    "w": {"a": "0.1ms", "curve": 0.0, "d": f"{wms}ms", "s": 0}},
            "filters": ["hp cutoff=300", "peak cutoff=1.8k q=1.5 gain=5dB", "lp cutoff=7k"],
            "layers": [{"fixed": hz(knock), "level": {"mod": [{"amount": 56.0, "src": "env.k"}], "value": "-60dB"}, "name": "knock", "wave": "sine"},
                       {"fixed": hz(wood), "level": {"mod": [{"amount": 54.0, "src": "env.w"}, {"amount": 2, "src": "rand"}], "value": "-66dB"}, "name": "wood", "wave": "triangle"},
                       {"level": {"mod": [{"amount": 60.0, "src": "env.c"}, {"amount": 6, "src": "vel"}], "value": "-66dB"}, "name": "click", "type": "noise"}]}}}
    new = None
    if blocks:
        c1, c2, r1, r2, g1, g2, p1, p2, fader, vel = blocks.split(":")
        notes = []
        for piece, count, ring, gain, pan, hand in (("w" + c1, c1, r1, g1, p1, "clean-l"), ("w" + c2, c2, r2, g2, p2, "clean-r")):
            mine = [n for n in track[hand]["notes"] if a <= n["at"] < z]
            # every stroke that hand has in the section is on this count: the block is struck with each of them
            assert mine and all(abs((n["at"] - a) * 4 % float(count)) < 1e-6 for n in mine) and piece not in kit, hand
            # chirper-two's block (v7), on this count's note
            kit[piece] = {"gain": f"{gain}dB", "pan": float(pan), "patch": {"synth": {
                "amp": {"a": "0.1ms", "curve": 4, "d": f"{ring}ms", "r": "15ms", "s": 0}, "env": {"c": {"a": "0.1ms", "d": "3ms", "s": 0}},
                "filters": [f"bp cutoff={hz(count)} q=2"],
                "layers": [f"triangle fixed={hz(count)}", {"type": "noise", "level": {"value": "-66dB", "mod": [{"src": "env.c", "amount": 50}]}}]}}}
            notes += [{"at": n["at"], "len": 0.25, "pitch": piece, "vel": float(vel)} for n in mine]
        assert "wood" not in track
        new = {"name": "wood", "patch": "ct-kit-here", "gain": f"{fader}dB", "out": "drums", "notes": sorted(notes, key=lambda n: (n["at"], n["pitch"]))}
    doc["patches"] = {**doc["patches"], "ct-kit-here": {**doc["patches"]["ct-kit-here"], "kit": kit}}
    if new:
        doc["tracks"].append(new)
    if target:
        doc["loudness"] = float(target)


if __name__ == "__main__":
    if os.environ.get("C10T14_SHOW"):
        beat = 60 / BPM
        print(f"tempo {BPM}: a sixteenth {beat / 4 * 1000:.3f} ms")
        for p in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16):
            print(f"  every {p:2d} sixteenths = {4 / (p * beat) * 2 ** OCTAVES:8.2f} Hz, six octaves up")
        gear = GEAR.split(";") if GEAR else None

        def secs(s16):                                             # v18: from the change on a sixteenth is den/num as long
            if not gear or s16 <= AT[gear[0]]:
                return s16 / 4 * beat
            num, den = (int(x) for x in gear[1].split("/"))
            return (AT[gear[0]] + (s16 - AT[gear[0]]) * den / num) / 4 * beat
        for name, n in FORM:
            print(f"  {name:10s} bar {AT[name] / 16:6.2f}  {secs(AT[name]):7.2f}s  {n} sixteenths")
        compose()
        print({k: len(v) for k, v in T.items()})
    else:
        doc = song()
        if GATHER:
            the_three_gather(doc)
        if GEAR:
            the_fifteen_becomes_the_bar(doc)
        if SIXTEEN:
            sixteen_is_said(doc)
        if BITE:
            the_chug_bites(doc)
        if WALLCAB:
            the_wall_comes_out_of_its_box(doc)
        if FLOOR:
            the_chord_falls_through_the_floor(doc)
        if VOICE:
            the_tune_is_the_voice(doc)
        if OCTAVE:
            half_as_fast_is_an_octave_down(doc)
        if RISE:
            the_chord_rises_out_of_the_floor(doc)
        if PAIRS:
            the_octave_holds(doc)
        if DAMPED:
            the_backbeat_stops_ringing(doc)
        if TWICE:
            twice_as_fast_is_the_octave_above(doc)
        if WOODS:
            the_valley_keeps_time_on_three_woods(doc)
        open(OUT, "w").write(dump(doc))
