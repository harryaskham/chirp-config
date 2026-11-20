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


if __name__ == "__main__":
    if os.environ.get("C10T14_SHOW"):
        beat = 60 / BPM
        print(f"tempo {BPM}: a sixteenth {beat / 4 * 1000:.3f} ms")
        for p in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16):
            print(f"  every {p:2d} sixteenths = {4 / (p * beat) * 2 ** OCTAVES:8.2f} Hz, six octaves up")
        for name, n in FORM:
            print(f"  {name:10s} bar {AT[name] / 16:6.2f}  {AT[name] / 4 * beat:7.2f}s  {n} sixteenths")
        compose()
        print({k: len(v) for k, v in T.items()})
    else:
        doc = song()
        if GATHER:
            the_three_gather(doc)
        open(OUT, "w").write(dump(doc))
