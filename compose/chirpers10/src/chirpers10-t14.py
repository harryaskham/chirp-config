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
AT = starts()


def add(tr, s, length, pitch, vel, **more):
    """A note at sixteenth `s` (any real number), `length` sixteenths long."""
    n = {"at": round(s / 4, 5), "len": round(length / 4 * 0.96, 5), "pitch": pitch, "vel": round(vel, 3)}
    n.update(more)
    T.setdefault(tr, []).append(n)


def drum(piece, s, vel, **more):
    tr = {"k": "kick", "s": "snare", "t1": "toms", "t2": "toms", "t3": "toms", "c": "cym", "x": "cym", "h": "hat"}[piece]
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
    bass(a, a + 240, 6, "F1", 5)
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
    bass(a, a + 240, 6, "F1", 5)
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
    if FILLS:
        fills()
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
    for name, semis in (("sixth", -4), ("fourth", 5), ("common", 7), ("home", 0)):
        b = AT[name] / 4
        key += [[f"{b - 0.02:g}b", key[-1][1] if key else 0], [f"{b:g}b", semis]]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    top = {"fx": [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]}
    kit = "ct-kit-here"
    tracks = [
        {"name": "gl", "patch": main.format(140), "gain": "0.7dB", "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(141), "gain": "0.7dB", "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(142), "gain": "-2.5dB", "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(143), "gain": "-2.5dB", "pan": 0.75, "out": "gtrs", **mids},
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
    assert {t["name"] for t in tracks} >= set(T), set(T) - {t["name"] for t in tracks}
    for t in tracks:
        t["notes"] = T.get(t["name"], [])
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
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": kit_here}} | wheel_patches,
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
    if TUNED:
        doc = {k: v for k, v in list(doc.items())[:2]} | {"tuning": {"steps": JUST, "root": "F3", "map": "keys"}} | {k: v for k, v in list(doc.items())[2:]}
    return doc


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
        open(OUT, "w").write(dump(song()))
