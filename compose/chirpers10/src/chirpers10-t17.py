#!/usr/bin/env python3
"""So Far (Common Time t17), chirper-one. Generator for songs/chirpers10-t17.yaml.

Take a number. If it is even, halve it; if it is odd, treble it and add one. Go on until you reach one. Every
number anyone has tried gets there; nobody has proved that every number must. This song tries the first sixteen,
in order, and plays each walk in full.

A number n is two things at once: a length, n sixteenths, and a pitch, the n-th harmonic of the low F. So when a
number is HALVED its note falls an octave and takes half as long, and when it is trebled-and-one it leaps up a
twelfth and a hair and takes three times as long and a sixteenth. And it is a riff: write the number's odd part in
twos (5 is 101, 13 is 1101) and that is its phrase, a stroke for a one and a rest for a nought, said round and
round; each two in the number slows the phrase by a doubling. So 40, 20, 10, 5 is ONE phrase (stroke, rest, stroke)
said in half notes, in quarters, in eighths, in sixteenths; and a power of two is one stroke and its silence, which
is why every walk ends the same way: sixteen, eight, four, two, one, a ball coming to rest on the low F.

The kit is not in the rule: it keeps common time from the first bar to the last and the walks fall across it
where they fall. The seventh walk (7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1) is 288
sixteenths, eighteen bars exactly. Nobody can say how long a number will take without walking it: six takes three
and a half bars, seven eighteen, eight one.

One is not an end: three ones and one is four, and four, two, one goes round for ever, seven sixteenths a turn.
The song ends on that wheel, fifteen turns of it, which is what it takes to bring it back to a bar line.

v1 is the whole shape standing, bare: two guitars, bass, kit, and an ondes Martenot as the lead from end to end
(The Other Hand borrows one for a countersignature). Its ribbon slides: it IS the number, at its true height, and
where the number climbs past the top of the ribbon (70, 106, 160, 80) it is out of sight and the band goes on
without it.
"""
import argparse
import json
import math
from pathlib import Path

BPM, SUB, BAR, F1 = 130, 4, 16, 29
NOTES = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t17.yaml'
FIRST, LAST = 1, 16            # the numbers tried, in order
TURNS = 15                     # of the wheel four, two, one at the end
TOP = 98                       # the top of the ribbon (D7): above it the number is out of sight and the ondes rests
TILT = 2.5                     # dB off the ondes for every octave over middle C (a sine up there stood 2.5 dB under the band, 8 down low)
QUIET = (12, 13)               # two walks without the guitars: the rule heard plain on the ondes and the bass
# v2 (chirper-three; section round, 3:43.2-4:10.9, the top of the fifteenth walk and its first step down): THE SUMMIT
# HAS ITS FALL INSIDE IT. v1's note asked that 160 be the biggest thing in the song. It was ten bars on one chord and
# mostly air: the left guitar struck twice and rang for half of it. But 160 is not one number. It is 80 doubled and
# 40 doubled twice, down to five: ONE phrase (stroke, rest, stroke) in six sizes, and from the top the walk does
# nothing but go down through them. v1 played two sizes there (the number's own, two bars a place, on the left
# guitar; the smallest, in sixteenths, on the right guitar and the kick). Now the sizes between are heard too, each
# on what will have it next: TWO MORE GUITARS say eighty's phrase (a bar a place) a storey under the number, on the
# low A; the BASS says forty's (half a bar a place). At 80 the left guitar comes down to what the new pair is
# already playing; at 40 the pair stops and the whole band is on the riff the bass has had since the top. So the top
# is four guitars, every chord of the next thirty seconds already going, and the fall takes a storey off at a time.
# The hands stay in common time and go to the china for the ten bars of 160; a crash marks the top.
# Nothing is cut, repeated or moved: 18 notes are added on two new tracks, the bass's six notes become eighteen.
SUMMIT = (160, 80)             # the numbers of the fifteenth walk that carry the storeys under them
STOREY = ('ct-wall-stop-{}', -1, .5, -1, -6)  # the second pair: rig ; track gain ; pan ; octaves from the left guitar's chord ; dB at 380 Hz
SUMMIT_LOUDNESS = -9.81        # the loudness target with the storeys in: at -10 every other bar came out 0.17 to 0.18 dB quieter
# v4 (chirper-one, instrument): THE KIT. Read alone against the eleven records' drums (their drum stems, as a share
# of their mixes) and in the mix against their mixes, on the ninth walk and on the climb to 160 (raw), then on
# the finished song. What the read said of v3: the kit as a whole stood 1.3 to 1.8 dB over the records' drums, and
# the KICK alone was 44 to 50% of the whole mix's power: 77 to 88% of everything under 60 Hz, where the song read
# 1.4 to 1.7 dB over the records, with its drum on the low A (55 Hz) and so almost all under 60. The CYMBALS were
# 95% and more of 8-16 kHz, 1.2 to 1.5 over (3.2 in the climb). The kit held 6.6 dB more of 250-500 Hz than the
# records' drums do, where the song read 2.2 to 2.6 over. So:
#   the kick's drum is tuned a semitone up, to B flat (58 Hz: the fourth of the key, and it straddles 60 Hz as the
#     records' kicks do, half its weight on either side), and its fader comes down 1.5 dB
#   the cymbals get the album's shelf (2 dB off over 9 kHz); their fader stays where it was
#   the drums bus gets the album's top (2 dB off over 9 kHz, low-pass at 14.25 kHz, where this one had a low-pass
#     at 14.8 only) and a deeper, narrower cut for the box (7 dB at 340 Hz, q 1.2: the song is SHORT at 500 Hz to
#     1 kHz, so the album's wide cut at 400 Hz would have taken from the wrong place too)
# Tried and not kept: the kick's drum on C (65 Hz): the song went from 1.6 over to 2.6 UNDER below 60 Hz; and 3 dB
# off the cymbals over 9 kHz, or 1 dB off their fader: the long walks came out 0.6 to 1.3 and 0.2 to 0.8 under
# at 8-16 kHz, and the top (160) and the last walk, which were not over, lost the most.
# The kick's drum (its pitch) ; its fader ; the cymbals' fader ; their eq ; the drums bus's eq ; the loudness target.
KIT = {'kick': {'pitch': 'A#1'}, 'kick gain': 0.5, 'metal gain': 1.5, 'metal': ['highshelf cutoff=9000 gain=-2dB'],
       'bus': ['peak cutoff=340 q=1.2 gain=-7dB', 'highshelf cutoff=9000 gain=-2dB', 'lp cutoff=14250 q=0.8'], 'loudness': -9.81}
# v3 (chirper-alpha, instrument): THE BASS. See the note above the bass's track. Track gain ; the album's chain.
BASS = (0, [{'type': 'eq', 'bands': ['hp cutoff=29', 'peak cutoff=44 q=1.5 gain=-7dB', 'peak cutoff=90 q=1 gain=7.5dB',
                                       'peak cutoff=350 q=1 gain=-8dB', 'peak cutoff=1500 q=1 gain=4dB']},
             {'type': 'compressor', 'threshold': '-26dB', 'ratio': 8.0, 'attack': '12ms', 'release': '120ms', 'makeup': '2.5dB'},
             {'type': 'eq', 'bands': ['peak cutoff=170 q=1.2 gain=-3dB']}])
# (The album's bass is at 0.5 dB into that chain on a bus. Here the chain is on the track and the fader comes after
# it, so the fader is 0: benched, the bass alone then stands within 0.1 dB of the bus arrangement.)
BASS_LOUDNESS = -9.81
BASS_QUIET = -1.5              # dB on the bass's fader through the two quiet walks, where it is half the band (see the track)


# v5 (chirper-alpha, whole song): THE BAND IS AS BIG AS THE NUMBER. A number was three things here: its length, its
# note and its riff. It had no SIZE: every walk was one level from its first number to its last (the loud walks all
# within a decibel of each other, the scorer's variety 62 to 72), so 160 was no bigger than 13 and a walk reached one
# at the level it had left 52. v1 asked that the climb grow and 160 be the biggest thing in the song; v2 found the
# climb did not grow. Now it follows from the rule: the guitars' and the bass's faders stand at 1.25 dB for every
# doubling of the number being said. A halving is a step down, a trebling a step and a half up. So every walk
# RISES AND SETTLES AS ITS NUMBERS DO: seven climbs to 52 and is loudest there; fifteen's climb zigzags upward (46,
# 23, 70, 35, 106, 53) to 160, which is the biggest thing in the song because it is the biggest number in it; and
# every walk ends the same way, sixteen, eight, four, two, one, each a step smaller: the ball coming to rest. The
# song therefore opens small (one to six are small numbers) and grows into seven. The wheel at the end turns small.
# THE FOOT IS IN THE RULE (it plays the riff's strokes) and settles with the walk: sixteen, eight, four, two, one
# is a ball bouncing, each bounce sooner and lower. It never goes over its v4 level (its lane is capped at 0: at
# the top the limiter is already at work). The hands are outside the rule, as v1 has it, and keep their level:
# common time goes on while the walk settles. (First take, the foot at one level too: the finished file moved
# only 0.33 dB for each dB on the faders, the kit being half the mix; and 52, the top of the seventh walk, was
# still its quietest cell, because a big number's phrase is sparse.)
# The ondes keeps its own law (it is quieter the higher it is). No note is changed.
# dB for each doubling ; the number at which the band is as loud as it was (32: the guitars' power, averaged over
# the song by time, is then what it was, so the kit v4 set against them keeps its place) ; the last chord's size in
# dB (it is the bar line, not a number in a walk). Empty: v4.
SIZE = (1.25, 32, 0)
# v6 (chirper-three, instrument): THE GUITARS' BODY. The first pair had not been read. Read alone against the
# records' guitar heard alone (tools/cabspec.py) and in the mix against the eleven records' guitar stems, on the
# ninth walk and the climb (raw): the pair was 5 to 6 dB SHORT at 120-280 Hz both ways (141-282 Hz -6.3 and -4.9
# alone; -5.3 and -3.1 as a share of the mix), and the mix did not show it because the bass (2.9 dB over the
# records' basses there) and the foot were holding that band for them: at 120-250 Hz the bass had 35% of the mix
# and the two guitars 16%, where on the records the guitars stand 4.8 dB OVER the bass. A low-tuned guitar's
# weight is there (the low F's third to fifth harmonics), and this rig cuts it before the amp: its `tight` filter
# is at 220 Hz. So:
#   the pair's tight filter comes down to 180 Hz: more of the low string reaches the amp
#   the bass gives the band up: the last cut of its chain (170 Hz) goes from 3 dB to 5
# and the mix's own 120-250 Hz stays where it was in the long walks. Benched and not kept: the amp's mid, bass and
# resonance and the microphone's distance (none moved 141-282 Hz by more than 0.6 dB); an eq lift at 200 Hz (it put
# 1.3 dB into the pair's 250-500 Hz); the album's guitar bus (a 330 Hz cut and a short room: the pair is not over
# the records' guitars at 250-500 Hz, and the room filled the riff's rests, which are its noughts, to -28 dB); a
# scoop at 600 Hz (the mix is already short there in the climb); hard left and right (0.7 dB off the pair in the
# mix's read for a width the records' widest pair already has).
# IN THE TWO QUIET WALKS there are no guitars to give the band to, and the deeper cut took 0.66 dB off the bass
# alone there (K): its fader trim in those walks goes from -1.5 dB to -0.85, so it stands where v3 set it.
# the pair's tight filter, Hz (the library's is 220) ; the bass's cut at 170 Hz, dB (v3's chain has -3) ; the
# bass's fader in the quiet walks, dB (v3's BASS_QUIET is -1.5) ; the loudness target (raw, the whole song came
# out 0.029 LU quieter: the target moves by that, so the kit and the ondes keep their level). --without-body
# gives v5.
BODY = (180, -5, -0.85, -9.839)


# v7 (chirper-two; the draw was a palette round and this is the song's whole palette of pitches: I chose it, and
# say so in the round note): THE NUMBERS ARE AT THEIR TRUE HEIGHT. The rule says a number is "the n-th harmonic of
# the low F", and the ondes "IS the number, at its true height". Until now it was the semitone NEAREST that harmonic
# (`height`), and so were the guitars' chords and the bass. The nearest semitone is 31 cents off for 7, 14 and 28; 49
# off for 11 and 22; 41 off for 13, 26 and 52; 45 off for 35 and 70; 28 for 23 and 46; 27 for 53 and 106; 14 for 5 and
# its doublings up to 160. Now every pitched note is the harmonic itself (the engine's fractional key numbers, which
# the album had not used): the ondes at n times the low F, exactly; the guitars' chord and the bass on the same
# harmonic brought down by octaves, the chord's fifth a pure 3:2 over it. The low string's muted strokes are the
# fundamental, as they were, so every chord and every note of the ondes is now an overtone of the string the band
# is chugging on. 986 notes move, by up to 49 cents; no note is added, dropped, moved in time or changed in length
# or level.
# WHAT IT DOES TO THE WALK. "When a number is trebled-and-one it leaps up a twelfth and a hair." In semitones the hair
# was either a semitone or nothing, by the luck of the rounding. True, it is 1/(3n) of the number: a tone at 3 -> 10,
# a semitone at 5 -> 16, 80 cents at 7 -> 22, 63 at 9 -> 28, 52 at 11 -> 34, 44 at 13 -> 40, 34 at 17 -> 52, 25 at
# 23 -> 70, 16 at 35 -> 106, 11 at 53 -> 160: the bigger the number, the finer the hair, and a halving is a pure
# octave every time. The size of the number can be heard in the size of the hair.
# MEASURED (the pitched band alone, raw): the ondes's line against the harmonic, for 10, 11, 13, 14, 15: +13.7,
# +49.2, -40.9, +31.3, +11.8 cents before; 0.0, -0.3, -0.2, -0.1, 0.0 after. Every walk's level is within 0.10 dB
# (K) of v6's and the loudness target is not moved. --equal gives v6.
# v8 (chirper-one, whole song): THE HANDS REMEMBER. The walks merge. Seven's walk (7, 22, 11, 34, 17, 52, 26, 13, 40,
# 20, 10, 5, 16, 8, 4, 2, 1) is the whole of nine's after three numbers, of fourteen's after one, and eleven's is its
# last fifteen: between 0:58 and 3:03 the song says that one thirty-second passage three more times, and from 1:37 to
# 3:03 the only number it has not said before is twelve. Then the fifteenth walk's first nine numbers (68 seconds, the climb
# and the top) are all new, and its last nine are the oldest ground there is. The band is in the rule and plays a
# number the same way every time. The hands are not in the rule and kept one count through all of it (v1 gave each
# walk a feel by hand). NOW THE HANDS KNOW WHERE THEY HAVE BEEN: from the seventh walk on, what they play under a
# number depends on how many walks have said it before.
#   a number never said before: half time, the snare on three alone. Nobody knows where this goes.
#   said once before:           the backbeat, two and four.
#   said twice before:          the backbeat, and a closed hat fills in the eighths between the cymbal's quarters.
#   said three times or more:   double time, the snare on every off-beat.
#   a power of two (16, 8, 4, 2, 1), however often said: the backbeat. Every walk ends there; the ball comes to rest.
# They never leave common time: every stroke is on a beat or half way between two.
# WHAT THAT MAKES OF THE SONG: seven is found in half time; at 10 (said by three and six) the hands recognise the
# way home. Nine finds 9, 28, 14 in half time and at 7 the backbeat comes in: we have been here. Eleven is the
# third telling and gets the hat; fourteen the fourth, double time: the passage is fastest when it is best known.
# Then fifteen: 68 seconds no walk has trodden, in half time, climbing to 160 and its china; and at 40, said by five
# walks before, double time to the bottom. The two quiet walks keep their stick on the rim.
# BENCHED (raw): the hat at 10 dB stood 25.8 dB (K) under everything else in the eleventh walk, not a part anyone
# would hear; at 15 it is set where it reads. The double-time snare at the backbeat's own weight stood 6.6 dB under
# everything else in the fourteenth walk (v7's snare there: 12.0) and held 46% of 250-500 Hz and 54% of 8-16 kHz:
# four strokes a bar are each 2.5 dB lighter than the backbeat's two.
# the first walk that remembers ; the hat's fader, dB ; its velocity ; the double-time snare's velocity ; its
# trim, dB ; the loudness target. --without-memory gives v7.
MEMORY = (7, 15, 0.5, 0.9, -2.5, -9.826)
# v9 (chirper-zero; section round, 4:10.8 to the end of the fifteenth walk and the sixteenth, 3:56-4:25; and what
# follows from it on the wheel): SOMEBODY COUNTS THE WAY HOME. The song is its rule and nobody has said the rule. A
# number has been a length, a height and a riff; here, for the first time, it is also a WORD. The fifteenth walk
# spends sixty-eight seconds where no walk has been (46, 23, 70, 35, 106, 53, 160, 80). At forty it lands on ground
# five walks have crossed, the hands go to double time (v8), and a voice says the numbers as they come, each on
# the sixteenth where its number begins: forty. twenty. ten. five. sixteen. eight. four. two. Each word has as long
# as its number, so the count is the ball coming to rest, said: 4.6 seconds, 2.3, 1.2, 0.6, then 1.8, 0.9, 0.5, 0.2.
# The sixteenth walk is the one everybody knows (it is the end of every walk since three), and FIVE MORE VOICES
# say it with the first: sixteen, eight, four, two, one.
# THE VOICE IS IN THE RULE FOR ITS NOTE: a number is the n-th harmonic of the low F, so the voice says it on that
# harmonic brought into its own octave. Forty, twenty, ten and five are one note (five, the pure third over F3:
# a halving is an octave, and an octave is the same note to a voice), and sixteen to one are F. The count is two
# notes, and the step between them is the song's "twelfth and a hair" at 5 -> 16.
# THE WHEEL (four, two, one, seven sixteenths a turn, fifteen turns) cannot stop, and neither can the count: the
# wheel turns twice without a word, then the one voice says it, ONE WORD A TURN, each where its number is in the
# turn (four . . | . two . | . . one), three tellings, each further off. Fifteen turns are three times five, so the
# last word of the song is "one", a sixteenth before the last bar line.
# The fifteenth walk's own "one" is a sixteenth long and is not said: the next walk's "sixteen" is on its heels.
# first number said ; the one voice (patch ; track gain, dB) ; the five (patch ; gain, dB) ; their eqs ; dB more on the
# words whose vowels have nothing over 1 kHz on this engine ("four", "two") ; the wheel's three tellings, dB ;
# the last word, dB ; the loudness target. --without-count gives v8.
COUNT = {'from': 40,
         'one': ('voice-hook synth.layers.0.diction=3 synth.layers.0.effort.value=0.8 synth.layers.0.speech=0.6', -10),
         'five': ('voice-choir synth.layers.0.diction=3 synth.layers.0.effort.value=0.8 synth.layers.0.speech=0.6 fx.0.mix=0.05', -14),
         'eq': ['hp cutoff=220', 'peak cutoff=380 q=0.9 gain=-7dB', 'peak cutoff=2600 q=0.6 gain=7dB'],
         'eq five': ['hp cutoff=240', 'peak cutoff=380 q=0.9 gain=-10dB', 'peak cutoff=2600 q=0.6 gain=7dB'],
         'lift': {'F AO1 R': 2, 'T UW1': 3}, 'wheel': (-3, -4, -5), 'last': -2, 'loudness': -9.781}
# a number as it is said: syllables (ARPAbet) and how long each has, in beats (they touch; the last rings)
SAY = {40: [('F AO1 R', 1.0), ('T IY0', .7)], 20: [('T W EH1 N', .75), ('T IY0', .6)], 10: [('T EH1 N', 1.0)], 5: [('F AY1 V', 1.0)],
       16: [('S IH0 K', .5), ('S T IY1 N', 1.1)], 8: [('EY1 T', 1.0)], 4: [('F AO1 R', .85)], 2: [('T UW1', .5)], 1: [('W AH1 N', .9)]}

# v10 (chirper-two, whole song): THE ONE THAT WAS ADDED. The rule's odd step is "three times the number, AND ONE".
# v1 wrote that the ondes then "leaps up a twelfth and a hair". The twelfth could be heard. The hair could not: the
# ondes landed on the new number at once, and nothing in the band held still enough to show a hair anyway. v7 put
# every note on its exact harmonic (moves of 14 to 49 cents), and then the rigs took it back: the ondes's vibrato
# swung 18 cents either way, a held string grew one of 20, every stroke was detuned at random by up to 5 cents (the
# bass by 4), and the strings sounded 2 to 4 cents sharp of the note they were given (these chords; bd-d2ee40).
# (1) THE ONE (`ONE`). Where a number is trebled-and-one, the ondes arrives on THREE TIMES THE LAST NUMBER, a new
#     note, stays there for one sixteenth, and its ribbon is pushed up the hair to the number itself, which it holds
#     for the other 3n sixteenths. The one added to the length is the one added to the height. Three times a number
#     is that number's own twelfth: the ondes lands in tune with the chord the band has just left and is pushed off
#     it onto the one the band has just struck. THE HAIR SHRINKS AS THE NUMBERS GROW, and that is the rule heard:
#     9 to 10 is a tone (182 cents, 3 times), 15 to 16 a semitone (112, the leading note into every walk's last
#     halvings: 11 times), then 21 to 22 (80.5, 3 times), 27 to 28 (63.0, once), 33 to 34 (51.7, 4 times), 39 to 40
#     (43.8, 5 times), 45 to 46 (38.1, once), 51 to 52 (33.6, 4 times): 32 in all, from 0:00.8 to 4:19.5. On the
#     piano's notes the same slides are a semitone or nothing (into 22 a semitone; into 34 and 52 nothing): the
#     shrinking hair exists only at the true heights. No note of the band, the kit or the voices is changed.
#     NOT IN IT: 70, 106 and 160 are above the ribbon's top, so the hairs of 23, 35 and 53 (25, 16 and 11 cents)
#     are still unheard; and the wheel's four ("three ones and one") is a fourth, not a hair, and the count has the
#     wheel now (v9): ONE's second field gives it (it plans; not rendered).
# (2) THE RIGS STAND ON THE NUMBER (`STILL`). The four guitars: `tune_sounding` (engine batch 64, new today: the
#     string sounds the note it is given), no vibrato on a held note, no random detune. The bass: no random detune.
#     The ondes: its vibrato 5 cents either way where it was 18 (it stays a voice; with none its line was 0.4 to 1.1
#     cents wide, a test tone: benched alone, not put in the song). No note changes: 308 held guitar notes lose the
#     vibrato, all 2171 notes of the guitars and the bass the random detune.
# MEASURED (raw, each alone unless said; 0.6 to 3.2 s into a held note; cents from the written harmonic, and the
# width that holds the middle 80% of a line's energy). First pair, the chord at 3:43.2: -2.7 and -0.3, lines 38 and
# 39 wide; now -0.2 and -0.6, 5 and 3 wide. Second pair, the same chord: +5.6, +4.8, +7.8, lines 39 to 44 wide; now
# +2.8, +1.5, +1.4, 6 to 17 wide (its lowest note is 55 Hz, where the reading itself is 48 wide). The bass's last F:
# -3.8, now 0.0. The four guitars and the bass together on that chord: the fifth's lines 39 wide, now 9. The ondes
# (the seventh walk, pitch read back from the audio): held, 31 to 35 cents from its 10th to its 90th percentile,
# now 9 to 11; and at each trebling it is within 1.3 cents of three times the last number 60 to 110 ms in, within 13
# of the number at 200 ms, within 0.6 from half a second on.
# THE FINISHED FILE (seed 0): every walk within 0.08 dB of v9 (K), the last chord 0.21 lower; the target is not moved.
# STILL: what each pitched rig is given so that it sounds the number it is written. --without-still gives the rigs of v9.
STILL = {'strings': ' synth.layers.0.tune_sounding=true synth.pitch.mod.1.amount=0 synth.pitch.mod.2.amount=0',
         'bass': ' synth.pitch.mod.1.amount=0', 'ondes': ' synth.pitch.mod.0.amount=0.05'}
# ONE: sixteenths the ondes stays on three times the number before it is pushed up to three times and one ; whether the
# wheel's four (three ones and one) is entered that way too. --without-one gives the ondes's notes of v9.
ONE = (1, False)
# v11 (chirper-one, whole song: the lead): UNDER THE CEILING. v1: "where the number climbs past the top of the ribbon
# (70, 106, 160, 80) it is out of sight and the band goes on without it." So the lead was silent for 48 of the 68
# seconds of the fifteenth walk's climb and top (3:12.7-3:20.8, 3:24.8-3:37.0 and 3:43.2-4:10.8): the song's biggest
# numbers had no voice, and the top, the biggest thing in the song, was 27.7 seconds of band alone.
# Now the ondes presses against the top of its ribbon: a number over the top is sung in the highest octave of it
# the ribbon reaches. A number over the top is always even here, so that octave is a number the walk is about to
# come down to: 70 is sung where 35 will be, 106 where 53 will be, 160 and 80 where 40 will be. The ondes gets
# there first and is struck again each time the number changes. At the top that is one note three times, 18.5,
# 9.2 and 4.6 seconds long (160, 80, 40: a ball bouncing under a ceiling), and only then does the ribbon fall its
# octaves (20, 10, 5). When the voice says "forty" (v9) the ondes has been singing forty for 27.7 seconds.
# AND THE THREE SMALLEST HAIRS ARE IN THE SONG (v10 left them "above the ribbon's top and unheard"): a trebled
# number over the top gets v10's push an octave or two down, where a hair is the same hair in cents: into 70 from
# 69 (25 cents), into 106 from 105 (16), into 160 from 159 (11: at the summit the hair is the finest there is,
# about the width of the ondes's own vibrato, so it is in the song and very likely not in the ear).
# Seven notes are added to the ondes; no other part changes. Under the ceiling the ondes keeps its own law (v1:
# quieter the higher it is) and stands 13.4 to 14.9 dB under everything else (K, raw), where its true notes
# around them stand 10.4 to 14.3. Benched 1.5 dB up and not kept: the band its note is in (1-2 kHz, or 2-4 kHz
# at 106) then read 1.0 to 1.8 dB further over the records in the finished file.
# dB on the ondes's notes under the ceiling ; the loudness target. --without-ceiling gives v10.
CEILING = (0.0, -9.75)
# v12 (chirper-two, whole song): SAID SO FAR. v9 gave the song a voice where the fifteenth walk "lands on ground five
# walks have crossed", and five more voices for the sixteenth, "the one everybody knows". That is a law, and it was
# kept for the last thirty seconds. Here it runs from the first bar, and nothing is placed by hand:
#   A NUMBER IS SAID WHEREVER AN EARLIER WALK HAS CROSSED IT. Nobody says a number no walk has reached yet.
#   The one voice says it; once three earlier walks have crossed it, the five say it as well.
# (v8's hands already play by the same count.) The words are v9's, on v9's two tracks, in v9's voices, each on its
# number's harmonic in the voice's octave, each on the sixteenth where its number begins.
# WHAT COMES OF IT:
#   the opening teaches the rule in seventeen seconds. 0:00.3 "one". 0:05.8 "two". Then "four, two", and the five's
#   first word, ONE (0:06.8): one has been crossed three times. "five, sixteen, eight, four, TWO, ONE". "three, ten,
#   five, sixteen, eight, FOUR, TWO, ONE": the five learn the ending from its last word backwards, a word a walk,
#   and their FOUR, TWO, ONE (0:16.6) is the count-in to the seventh walk, where the band comes in whole (0:17.4).
#   the seventh walk is 28 seconds of new ground and nobody speaks. At 0:45.3 it meets ten: "ten", and everyone,
#   FIVE, SIXTEEN, EIGHT, FOUR, TWO: the end of every walk is the song's refrain, and from here everyone says it
#   (the ends of 7, 8, 9, 10, 11 and 14).
#   the ninth walk says nothing for 9, 28, 14, and at 0:58.3 it meets seven: the one voice recites seven's walk
#   alone (seven, twenty-two, eleven, thirty-four, seventeen, fifty-two, twenty-six, thirteen, forty, twenty) and
#   everyone has it from ten. Ten is everyone's from its first number; eleven is the one voice's to twenty.
#   by the fourteenth walk everyone has it from eleven (2:33.1) to one: thirty seconds.
#   the fifteenth walk is 68 seconds where no walk has been, the climb and the top, and nobody speaks, as before:
#   v9's "forty" at 4:10.8 (not a note of it changed) is no longer the first word in the song. It is the voice
#   coming back when the ground is known again.
# TWO THINGS OUTSIDE THE LAW, both chosen: the two quiet walks (twelve, thirteen) stay wordless, "the rule heard
# plain" (v1), though all but the 12 of them is known ground (the 'quiet' field gives the one voice there; it made
# the song's one quiet place 1.2 dB louder); and from forty in the fifteenth walk the one voice is alone, as v9
# has it, though everyone knows that ground. And a walk's last "one" is a sixteenth long: a voice that has the next
# walk's first number to say leaves it out (v9's own rule: "the next walk's 'sixteen' is on its heels").
# MEASURED (raw, seed 0; each word while it sounds, against everything else, K): the one voice alone -5.3 to +0.9
# dB, median -3.3; with the five -5.9 to +0.3, median -2.5; v9's own thirteen words read the same way -5.8 to
# -0.8, median -3.4. So they stand where v9 set its words. Six of the new words came out 3 to 5 dB under the rest
# (three, thirteen, fourteen, seventeen, twenty-two, fifty-two) and are lifted, a word at a time. The five stand
# 5.7 dB under the one where both speak (v9: 7.2): 1.5 dB more of them, so that "everyone" is a little more than
# one. THE WORDS, to a recogniser: the voices alone, the first twelve numbers of the ninth walk right, the ten
# words where seven lands right, the opening 15 of 18 ("sixteen" twice written "6", as v9 found). Under the band
# its count is not a measure: v9's own passage, the same audio, read 12, 8 and 3 of 13 in three cuts.
# THE FINISHED FILE (seed 0): the counted stretches are 0.4 to 1.0 dB louder (K). The loudness target moves -9.75
# -> -9.48 for that, so the band keeps its mastering gain: from the top to the last chord within 0.002 dB of v11
# (-79 dB or lower gain-matched), the climb and the seventh walk's new ground within 0.01.
# THE COST: the scorer reads 1.5 / 0.7 lower (level range 4.8 -> 4.4 dB: the opening is 0.9 dB louder); and v9's
# "for the first time it is also a WORD" at forty is given up for a voice that has been there all along.
# how many earlier walks must have crossed a number before the five say it with the one ; dB on the one voice's
# words ; on the five's ; on the one voice's words in the two quiet walks ; dB on whole words, by number (over COUNT's
# 'lift', which is by syllable) ; the loudness target. --without-said gives v11.
SAID = {'everyone': 3, 'one': 0, 'five': 1.5, 'quiet': None, 'lift': {3: 2.5, 13: 3, 14: 1, 17: 2.5, 22: 2, 52: 3.5}, 'loudness': -9.48}
SAY.update({3: [('TH R IY1', .7)], 6: [('S IH1 K S', 1.0)], 7: [('S EH1', .45), ('V AH0 N', .8)], 11: [('IH0', .3), ('L EH1', .5), ('V AH0 N', .8)],
            13: [('TH ER1', .5), ('T IY1 N', 1.1)], 14: [('F AO1 R', .6), ('T IY1 N', 1.1)], 17: [('S EH1', .45), ('V AH0 N', .5), ('T IY1 N', 1.1)],
            22: [('T W EH1 N', .6), ('T IY0', .45), ('T UW1', 1.0)], 26: [('T W EH1 N', .6), ('T IY0', .45), ('S IH1 K S', 1.0)],
            34: [('TH ER1', .55), ('T IY0', .45), ('F AO1 R', 1.0)], 52: [('F IH1 F', .55), ('T IY0', .45), ('T UW1', 1.0)]})

# v13 (chirper-two, instrument: the two voices): THE VOICES GET THE RECORDS' VOICE. v12 made the two voices speak
# for two minutes, and the read stamped after it showed what they are made of: the counted stretches stood 3.5 to
# 5.5 dB over the eleven records at 250-500 Hz where v11 had 2.0 to 2.5, and v9's own passage had the same mark (3.4
# and 5.6). Read alone against the records' voices (tools/voxref.py, their eleven vocal stems; v12, raw):
#   TONE, the voice's own energy by band, ours minus theirs: +19 dB under 250 Hz, +5.2 at 250-500, +0.2 at 500-1k,
#   -6.5 at 1-2 kHz, +0.2 at 2-4, +3.8 to +7.0 at 4-8. A voice of body with no middle: where words are told apart
#   it was 6 dB short, and it was loud by what is under them.
#   LEVEL while it sings, voice minus the whole mix: -4.8 dB (the records' -9.2, their middle half -9.7 to -8.9);
#   at 1-4 kHz -4.4 (theirs -7.1). In the counted stretches the two voices held as much of the mix's 250-500 Hz as
#   everything else together (-0.4 to -1.3 dB against the rest) and MORE of 500 Hz-1 kHz (+0.1 to +3.7).
# So, on both voices, after v9's bands: a high-pass at 450 Hz, 6 dB out at 450, 7 dB in at 1.3 kHz (the middle that
# was missing), 3 dB back out of v9's lift at 2.8 kHz, and the top eased at 6.5 kHz (3 dB on the one, 6 on the
# five, whose top was 7 over); both faders down 3.5 dB. And THE WORDS ARE EVENED, by number: with the body gone a
# word is as loud as its vowel has middle, and "two", whose vowel has nothing over 1 kHz on this engine (v9), fell
# to 13.8 dB under everything else where "ten" stood 3.7 under. Twelve words are trimmed (two +6 ... ten -3.5).
# AS SET (real renders, raw, seed 0). TONE minus the records' voices, 250 Hz to 4 kHz: -1.1, +0.1, -1.5, +1.6 (both,
# the fourteenth walk); -0.5, +0.1, -0.9, +1.5 (the one, the ninth); +0.5, +0.1, -2.0, +1.8 (v9's passage). Still
# apart: under 250 Hz +5 to +8 (it is 25 dB under the voice's own total there) and 4-8 kHz +3.1 to +5.7 (a count
# needs its consonants; the records scream). LEVEL: -8.9, -9.4, -9.4 whole; -5.9, -6.4, -6.9 at 1-4 kHz.
# EVERY WORD against everything else while it sounds (K): -10.8 to -5.2, median -7.6; by word, the medians lie
# between -8.1 and -6.9 (v12: -5.2 to -0.4). To a recogniser the voices alone read better than v12's: the opening
# 17 of 18 (15: both "sixteen" are now read), seven's landing 10 of 10, the ninth walk's recital all of it.
# THE MIX'S READ, before recording this time (ours minus the records, 250-500 Hz ; 500 Hz-1 kHz), v12 -> v13:
#   the ninth walk from seven +3.5 ; +2.1 -> +2.1 ; +0.5 (v11 +2.0 ; -0.3)   the fourteenth +4.0 ; +2.5 -> +2.3 ; +1.0
#   (v11 +2.3 ; +0.1)   ten and eleven +5.5 ; +2.4 -> +3.5 ; +0.5   the opening +5.3 ; +3.1 -> +4.1 ; +0.3
#   v9's passage: 40 to 1 +3.4 ; +2.6 -> +2.6 ; +1.0   sixteen to one +5.6 ; +3.1 -> +3.6 ; +1.5
# What is left over at 250-500 Hz is the band's own, as v11 had it. THE COST: on the wheel the voice had been
# filling a hole in the band, and the read there goes from +0.6 ; -0.6 to -1.7 ; -3.4.
# THE FINISHED FILE: the loudness target moves -9.48 -> -9.64 (the voices carry less), so the wordless stretches
# are v12's within 0.02 dB; the counted ones are 0.2 to 0.5 dB quieter than v12 (0.2 to 0.5 over v11).
# more eq bands on the one voice, after v9's ; on the five ; dB on both faders ; dB on whole words, by number,
# wherever they are said (v9's words and v12's) ; the loudness target.
# --without-clear gives v12.
CLEAR = {'one': ['hp cutoff=450', 'peak cutoff=450 q=0.8 gain=-6dB', 'peak cutoff=1300 q=0.8 gain=7dB', 'peak cutoff=2800 q=1 gain=-3dB', 'peak cutoff=6500 q=0.8 gain=-3dB'],
         'five': ['hp cutoff=450', 'peak cutoff=450 q=0.8 gain=-6dB', 'peak cutoff=1300 q=0.8 gain=7dB', 'peak cutoff=2800 q=1 gain=-3dB', 'peak cutoff=6500 q=0.8 gain=-6dB'],
         'gain': -3.5, 'even': {2: 6, 3: 1, 5: -2, 7: -2, 10: -3.5, 11: -1, 14: 1.5, 16: 1.5, 17: 1, 20: 1.5, 22: 2.5, 34: 2.5}, 'loudness': -9.64}


# v14 (chirper-zero; instrument round: the china, 314 of the cymbals' 620 strokes, the timekeeper wherever the band is loud):
# THE CHINA IS A PLATE, NOT AIR. No stroke moves. The song stood 2.1 to 3.4 dB over the eleven records at 8-16 kHz in
# nine of its ten stretches, and one instrument held that band: the cymbals' track was 95% of the mix's 8-16 kHz in
# 'seven' and 74% in 'fourteen', and on that track the china's strokes read 4 to 6 dB under the whole mix in their own
# tenth of a second where the ride's edge and the crashes read 12 to 15 under. Alone, beside the top of the records'
# drum stems (thirds of an octave, cspec.py), the kit's china was 4.1, 4.9 and 8.2 dB over at 10, 12.5 and 16 kHz:
# their metal has its weight at 4 to 6 kHz and falls 9 dB by 12.5 kHz; ours was flat to 10 kHz.
#   THE PLATE: its brightness 1 -> 0.65 (that, not its tilt, is what fills the top octave: tilt 3 -> 1 alone moved
#       16 kHz by 0.8 dB), tilt 3 -> 1, the patch's lift at 8 kHz moved to 5 kHz (3 -> 3.5 dB), its 2.2 kHz honk
#       flat. Alone it is within 0.7 dB of the records' top from 10 to 16 kHz and its distance over 2-16 kHz is 0.69
#       where 2.33. The stroke rings as long as it did (11.4 dB down a quarter of a second on where 12.0).
#   ITS LEVEL: with its weight in the band the ear weighs most it is 1.2 dB louder (K) at the same fader, so the
#       piece comes down 2 dB: 0.8 dB quieter than it was on that measure, 4.6 to 7.0 under the mix on its strokes.
# The ride's edge and the crashes share the track and are untouched. The kit's drive on the china stays (without it
# the stroke is 21 dB down in a quarter of a second, a splash).
#   UNDER THE WALLS: in '160 and 80' the wall pair comes in and the band is 3 dB louder against one cymbal; that
#       stretch was the one place the song was not over the records at the top (-0.6 at 8-16 kHz). There the china's
#       strokes get 4 dB (a note gain, on the 40 strokes while the walls play), so it keeps the place against the
#       band that it has everywhere else, and the stretch stays where it was.
# kit overrides on the cymbals' track ; dB on the china's strokes while the walls play ; the loudness target.
# --without-china gives v13.
CHINA = {'kit': 'kit.x.patch.synth.layers.0.tilt=1 kit.x.patch.synth.layers.0.bright=0.65 kit.x.patch.synth.filters.2.cutoff=5000 '
                'kit.x.patch.synth.filters.2.gain=3.5dB kit.x.patch.synth.filters.1.gain=0dB kit.x.gain=-8.5dB', 'walls': 4, 'loudness': -9.65}
# v15 (chirper-alpha; instrument round: the two guitars' muted stroke, 841 strokes on the low string): THE HAND ON
# THE STRING. No stroke moves. Read beside six records' strokes (riffpunch --strokes) the chug had no teeth (the
# stroke's 1-4 kHz 6.0 dB over its 400 Hz-1 kHz; the records 11.3) and, a measure nobody had acted on, its low end
# died: 100-250 Hz in the first 20 ms stood 2.3 to 2.5 dB OVER 40-80 ms, where on every record it holds or grows
# (-1.1; -2.2 to +0.3). The album's cure for the teeth (the palm closes the filter 2 octaves, not 3.4) made that
# worse alone (+3.5, and more noise between the harmonics than any record). What moves it is the palm's WEIGHT:
# every muted stroke was written at a full palm (pm 1.0); at 0.55 the low end holds (+0.3 to +0.6) and all five
# measures are in the records' range or a third of a decibel off it. So:
#   - the palm closes the string's filter 2 octaves;
#   - THE HAND'S WEIGHT FOLLOWS THE NUMBER: each muted stroke's pm is 1 at one and `light` at `top`, linear in the
#     number's octaves (as v5's size): 0.88 at three, 0.75 at ten, 0.6 at forty, 0.45 at 160. A walk's chug opens
#     as it climbs and closes as it settles;
#   - the microphone 0.4 -> 0.45: with it at 0.4 the mix's 2-4 kHz went past the records in five stretches of seven.
# After, on 342 clean muted strokes: low end +2.65 -> +0.34, teeth 5.2 -> 8.7, grain 0.43 -> 0.37. The mix is where
# it was (mean distance 0.85 -> 0.81). Costs: the guitars' 120-250 Hz 1.9 dB further short by part (the mix did not
# ask for it back); the open chords a little darker. The target -9.65 -> -9.606 holds the two quiet walks still.
# octaves the palm closes the string's filter at a full mute (the rig's own: -3.4) ; the microphone (the rig's: 0.4;
# lower is brighter) ; the palm's weight at one ; at
# `top` and over ; the number at which the hand is lightest ; the loudness target (None: unchanged).
# --without-hand gives v14.
HAND = {'palm': -2, 'mic': 0.45, 'heavy': 1.0, 'light': 0.45, 'top': 160, 'loudness': -9.606}
# v16 (chirper-three; palette round: two instruments of the kit, the two v8 gave the hands to remember with).
# THE BELL KNOWS WHICH WAY. No stroke is added, dropped or moved.
#   THE TICK. v8's sign for a number said twice before is a closed hat on the off-beat eighths (62 strokes). Read at
#       its strokes in the eleventh walk it was not there: 14.9 dB (K) under everything else, and in its best
#       third-octave (12.7 kHz, under the cymbals and the snare's wires) a median 6.1 dB UNDER what else was there;
#       40 of 53 strokes at -4 or lower. Its strokes go to two agogo bells (`afro-perc`, on no other track of the
#       album), tuned to the low string as everything pitched here is, and WHICH bell is the rule: an EVEN number
#       will be halved, an octave, and rings F (the string's 16th harmonic, 698.5 Hz); an ODD one will be trebled, a
#       twelfth, and rings C (the 24th, 1047.7 Hz). The hands know the ground, so they know which way it goes next.
#       At -19 dB the bell is 13.6 dB under everything else (1.3 louder than the hat was) and reads +3.5 in its own
#       third-octave; 29 of 53 strokes at +3 or more, 2 at -4 or lower.
#   THE SNARE is the album kit's as it comes; four songs have fitted theirs. Here it held 72% of the kit's 250-500 Hz,
#       71% of its 500 Hz-1 kHz and 51% of the MIX's 8-16 kHz in fourteen; alone its body stood 4.3 dB over its crack
#       (six records' snares: 3.2 under) and its wires 2.8 over (level). Now: the 200 Hz lift +5 -> -3 dB, a cut of
#       its own at 650 Hz (a third filter inside the drum, not on the track: the stick on the rim in the two quiet
#       walks shares the track and nulls against v15 at -80 dB), the wires lower (0.85 -> 0.7) and darker (7 -> 5
#       kHz), a longer contact. After: body 2.9 under the crack, wires 1.1 over; the kit by part +3.4 -> +1.5 at
#       250-500 Hz, +6.8 -> +5.0 at 500 Hz-1 kHz, +1.6 -> +0.7 at 8-16 kHz. A backbeat stands 7.5 dB over everything
#       else in its first 30 ms (9.3). BENCHED AND NOT KEPT: the drum retuned to the string's sixth harmonic (C4): its
#       body left 120-250 Hz for 250 Hz-1 kHz, where the kit is over.
#   COST: the two stretches in half time (seven, the climb) read 0.08 and 0.11 further from the eleven records (they
#       were level or short at 250-500 Hz and 8-16 kHz already); eleven and fourteen 0.08 and 0.04 nearer.
# 'snare': overrides on the snare drum (kit piece s; its third filter is new) ; 'fader': dB (None = as it was) ;
# 'bell': the patch that takes the hat's strokes, with the two bells' notes ; 'gain', 'pan', 'vel': its track ;
# 'loudness': the target (None = unchanged). --without-bell gives v15.
BELL = {'snare': 'kit.s.patch.synth.filters.1.gain=-3dB kit.s.patch.synth.layers.0.wire_tone=5000 kit.s.patch.synth.layers.0.wires=0.7 '
                 'kit.s.patch.synth.layers.0.contact=0.9 kit.s.patch.synth.filters.2.kind=peak kit.s.patch.synth.filters.2.cutoff=650 '
                 'kit.s.patch.synth.filters.2.q=0.8 kit.s.patch.synth.filters.2.gain=-8dB', 'fader': None,
        'bell': 'afro-perc kit.al.pitch=m77 kit.ah.pitch=m84.02 play.humanize.time=0ms play.humanize.vel=0', 'gain': -19, 'pan': -0.25, 'vel': 0.8,
        'loudness': None}
# v17 (chirper-alpha; palette round: the ondes's diffuser). THE LOW STRING ANSWERS. No note is added, dropped or moved.
#   The ondes Martenot's third speaker, the palme, is a soundboard strung with strings that ring with what is played.
#   The library's `ondes` strings it with a tempered octave, C4 to B4; this song's numbers are true harmonics of the
#   low F, so they are not on those strings (5, 7, 11, 13 lie 14 to 49 cents off the keys), and the engine's strings
#   ring 5 to 10 cents flat of even the notes they are given (bd-ce14dd). Nothing was answering.
#   NOW ONE STRING is strung behind the ondes, tuned to the low F itself. Every number here is a harmonic of that
#   string, so it answers every number at the number's own pitch, and nothing else. (Given 0.85 cents sharp, 43.675
#   Hz, it reads 0.0 cents at harmonics 5 to 52; given as 43.6535 it rang 0.8 flat and 5 to 7.5 dB weaker up high.)
#   HOW MUCH OF IT IS HEARD IS THE SONG'S MEMORY (v8's rule for the kit, here for the ondes): on a number no walk has
#   said before the string is shut; said once before 0.2; twice 0.4; three times or more 0.6. So seven and the climb
#   of fifteen are dry, and every walk's way home, and the whole of thirteen, rings on behind itself.
#   THE NOTE IS NO LOUDER. The string sings in step with the note, so with it open the ondes read +3.4 to +5.0 dB;
#   the fader comes down by ground (0, -1.1, -2.2, -3.3 dB; half that from 34 up, where the string answers less),
#   and the two together read -1.1 to +2.4 dB on v16's note, the first 150 ms within 0.2. What is new is THE TRAIL:
#   in the second after a number has gone, the ring against everything else at its pitch reads +1.8 to +11.5 in
#   thirteen (the ondes and the bass alone: 13, 40, 20, 10, 5, 16, 8) and -7.7 to +2.2 on seven's way home under
#   the full band (20, 10, 5, 16, 8, 4; -4 is about the edge of detection).
#   THE WHEEL (4 2 1, fifteen turns, all on the string's own octaves) would build up: 0.3 there, -2.8 dB.
#   COST: against the eleven records the seven stretches where it is open read 2.59 -> 2.89 at 250-500 Hz (nearer
#   at 500 Hz-1 kHz, 1.31 -> 1.20); thirteen is 0.42 dB louder; short low numbers (1, 2, 4, 5) stand 1.5 to 2.6 dB
#   lower against the band, the trim taking more than a string can give in under half a second.
# 'hz': the string (the low F, less the 0.85 cents the engine's comb rings flat) ; 'decay': how long it rings ;
# 'mix': how much of it is heard on ground that is new, said once before, twice, three times or more ; 'trim': dB on
# the ondes's fader on the same four grounds (the string sings in step with the note, so the two together are
# louder than the note was) ; 'high': from this number up the trim is this much of itself (the string answers a high
# number less) ; 'wheel': the mix and the trim on the wheel and the last note ; 'ramp': beats over which both move ;
# 'loudness': the target (None = unchanged). --without-string gives v16. (--string '{"mix": [...]}': a bench.)
STRING = {'hz': 43.675, 'decay': '8s', 'mix': (0, 0.2, 0.4, 0.6), 'trim': (0, -1.1, -2.2, -3.3), 'high': (34, 0.5), 'wheel': (0.3, -2.8),
          'ramp': 0.25, 'loudness': -9.589}
# v18 (chirper-one, whole song): THE HORN HOLDS THE NUMBER BEING TRIED. A natural horn in F has no valves: its notes
# are the harmonics of its tube, and the tube of a horn in F sounds this song's low F (43.65 Hz). Its sixteen open
# notes ARE the first sixteen numbers, the seventh, eleventh, thirteenth and fourteenth as flat or sharp as the tube
# makes them (Harry: 'True harmonics: keep them'). So a horn can say which number a walk is trying, and nothing in
# the song did: a walk begins on its number and never comes back to it (no walk does; that is the conjecture's other
# half), and thirty seconds in nobody could tell seven's walk from nine's. Now the horn sounds the walk's number as
# the walk begins and HOLDS it to the walk's end, taking a new breath wherever the walk is trebled (the leap) and at
# least every `cap` sixteenths. Over the song it climbs its own tube a step a walk: C3, F3, A3, C4, the flat seventh,
# F4, G4, A4, the eleventh, [the two quiet walks stay plain], the fourteenth, E5, F5: the steps close as the numbers
# rise. And when a walk comes home to one, the low F, the number it left is still sounding above it, as one of
# that F's own harmonics: it was inside the one all along.
# 'walks': which (one and two are over in half a second, and a horn cannot speak in a sixteenth; twelve and
# thirteen are QUIET, "the rule heard plain"; the wheel tries nothing) ; 'patch' (no vibrato: a harmonic is where it
# is; its filter a little open) ; 'gain' dB ; 'high': from this walk on, this many dB more (its note is then over
# 500 Hz; under that the song is over the records at 250-500 Hz, hence the shelf) ; 'call': dB on a walk's first
# note, the call ; 'pedal': dB on every breath after it (the long walks stood 0.7 to 1.1 dB further over at
# 250-500 Hz with the pedal as loud as the call) ; 'pan' ; 'vel' ; 'breath' sixteenths of rest before a new note ;
# 'cap' the longest held note where a number boundary allows ; 'eq' ; 'loudness' (None = unchanged).
# --without-horn gives v17. (--horn '{"gain": -9}': a bench.)
HORN = {'walks': (3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16), 'patch': 'horn synth.pitch.mod.0.amount=0 fx.0.mix=0.2 synth.filters.1.cutoff.value=1100',
        'gain': -12.0, 'high': (12, 3.0), 'call': 3.0, 'pedal': -2.0, 'pan': -0.15, 'vel': 0.6, 'breath': 1, 'cap': 80,
        'eq': ['hp cutoff=110', 'lowshelf cutoff=450 gain=-6dB'], 'loudness': None}
# v19 (chirper-two; section round, w10, 4:25-4:46: the wheel, never worked and flagged 'static in tone'). THE WHEEL IS
# TURNED BY EVERYTHING THE SONG HAS GATHERED: THE HORN COMES TO REST AT THE WHEEL'S OWN SIZE, AND THE BELLS KEEP ITS
# TIME. No stroke of the band, the ondes or the count changes. Two instruments the song found late (v16's two bells,
# v18's horn) were both silent on its last twelve seconds; v18's note left the wheel alone.
# (1) THE HORN. It reached sixteen (F5) at 4:23.1. Every walk ends sixteen, eight, four, two, one, 'a ball coming to
# rest', and the wheel is FIFTEEN turns because that brings it back to a bar line; fifteen is also 8 + 4 + 2 + 1. So
# the horn says eight, four, two, one down its tube (F4, F3, F2, and its pedal note, the low F itself) and each
# number lasts that many TURNS of the wheel: 8, 4, 2, 1 (6.5, 3.2, 1.6, 0.8 s), ending on the last bar line. A number
# here is a length and a height; this is the same law with a turn of the wheel for its unit. It is the one place the
# song's ending gesture is heard slowly enough to follow.
# (2) THE BELLS. v16's rule: an even number will be halved and rings F, an odd one will be trebled and rings C. On the
# wheel that is F on four, F on two, C on one, every turn: low, low, high in 4 + 2 + 1 sixteenths, an agogo's timeline
# in seven against the kit's common time, drifting across the bar and landing on the bar line. The C is the wheel's
# hidden three: one is odd, so it is trebled (the twelfth) and one is added, which is four. On the last bar line the
# bell rings the next four (F), as the ondes does: one is not an end.
# MEASURED, raw (K, against everything else): the horn's notes stand -15.0, -16.0, -16.3, -17.5 (v18's calls -12.8 to
# -18.3), in tune to 0.0 cents on F4 to F2; while it holds eight it is 57% of the mix's 250-500 Hz. The bells at
# -21 dB: in their own third-octaves a stroke stands +3.3 (F) and +4.8 (C) over everything else (v16's edge of being
# heard: +0.5); they are 23% of the wheel's 500 Hz-1 kHz. AGAINST THE ELEVEN RECORDS the wheel was hollow (v13's
# cost): 250-500 Hz -2.6 -> +0.1, 500 Hz-1 kHz -4.9 -> -3.5 (the rows with a voice; without: -3.1 -> -0.3, -1.3 ->
# +0.1); all nine bands 2.000 -> 1.578 (1.533 -> 1.100). FINISHED, seeds 1 / 0 / 11: the wheel +0.12 / +0.22 /
# +0.28 dB (K); every other stretch within 0.02 dB, so the target is not moved. Scores 94.989 / 95.149 (v18
# 95.020 / 95.101): level.
# 'horn': the numbers the horn says on the wheel, each for that many TURNS (a turn is four, two, one: seven
# sixteenths) ; 'gain': dB on each of them (the note's own gain; the track's fader is HORN's) ; 'breath': sixteenths
# of rest before each ; 'bell': the wheel's numbers on which the bell rings (v16's two bells: the odd one, C, on an
# odd number; the even one, F, on an even) ; 'bell gain': dB on those strokes ; 'bell vel' ; 'last': the bell rings
# the next four on the last bar line, as the ondes does ; 'loudness' (None = unchanged). --without-wheel gives v18. (--wheel '{"gain": [0, 0, 0, 0]}': a bench.)
WHEEL = {'horn': (8, 4, 2, 1), 'gain': (2.5, 4.5, 6.0, 8.0), 'breath': 1, 'bell': (4, 2, 1), 'bell gain': -2.0, 'bell vel': 0.8, 'last': True, 'loudness': None}
# v20 (chirper-alpha; instrument round: the ondes; 40 of its notes are shaped, none is added, moved or retuned).
# THE ONDES IS PLAYED WITH BOTH HANDS.
#   An ondes Martenot is played with two hands: the right is on the ribbon and gives the pitch; the left is on a
#   key in the drawer, the touche d'intensite, and gives the level: no sound comes out until it is pressed, and how
#   it is pressed is the whole of the instrument's expression. This ondes had only the right. Every number was one
#   level from its first sixteenth to its last, and here a number is as long as it is big: 160 was a sine standing
#   still for eighteen and a half seconds.
#   READ FIRST (the ondes alone against everything else, raw, in the third-octave round its note; about -4 is the
#   edge of hearing): the numbers up to sixteen stand clear (+3 to +17), and the BIG ones, which are the song's high points,
#   were at or under the edge: 52 -3.7 and -3.2, 46 -2.6, 106 -5.6, 53 -5.0, 160 -5.2, 80 -3.2. Two of the song's
#   laws run against each other there: the band is as big as the number (v5: 1.25 dB a doubling) and the ondes is
#   quieter the higher it is (v1: 2.5 dB an octave), and a big number is a high one.
#   NOW THE LEFT HAND PLAYS, and it follows the song's own law: a number over sixteen swells and falls back, and
#   the swell is 2 dB at its crest for every doubling of the number over sixteen (22: 0.9, 40: 2.6, 52: 3.4, 106:
#   5.5, 160: 6.6). The crest is five eighths of the way through the note; it starts and ends where it did, so each
#   new number still comes in under the last one's ring. Numbers up to sixteen are played as they were: the way
#   home (16, 8, 4, 2, 1) is not touched.
#   THE KEY IS AHEAD OF THE SPEAKERS, as on the instrument: both layers of the patch follow it (an inline patch,
#   `expr.touch` in dB, a path of eight points on each note), so the low string (v17) and the hall ring with what
#   the hand lets through. The ribbon is not touched: every note is where it was (Harry: 'True harmonics: keep
#   them').
#   MEASURED (same read; whole note, then the crest's quarter of it): 52 -3.7 -> -1.0, +1.2 at the crest (seven) and
#   -3.2 -> -0.7, -2.0 (nine); 46 -2.6 -> -0.2, -0.6; 70 +0.4 -> +3.6, +5.0; 106 -5.6 -> -1.2, +0.4; 53 -5.0 ->
#   -2.2, -2.1; 160 -5.2 -> +0.1, -0.6; 80 -3.2 -> +0.5, +1.0. The sixteen notes from 34 up: median -0.7 -> +1.6.
#   COST, against the eleven records (the mix): at the top (160 and 80) 1-2 kHz stands 0.6 dB further over (+1.6 ->
#   +2.2); the climb 2-4 kHz +0.5 -> +0.8; forty to one 1-2 kHz +0.1 -> +0.5; seven is 0.07 nearer; the ten
#   stretches' mean distance 1.066 -> 1.078. A swell of 3 dB a doubling was not tried, for that reason.
#   The song came out louder and the master turned everything else down 0.08 dB: the target goes -9.589 -> -9.521
#   (two steps; 1.23 dB of level for each dB of target).
# 'per': dB at the crest for each doubling of the number over 'over' ; 'over': numbers up to this are played as they
# were ; 'crest': where in the note the hand is furthest down ; 'points': how many points draw the hand's path ;
# 'least': the shortest note that is shaped, in beats ; 'loudness' (None = unchanged). --without-touch gives v19.
# (--touch '{"per": 3}': a bench.)
# v21 (chirper-one; whole song: the two guitars, 636 and 840 strokes, every walk): THE GUITARS' WEIGHT MOVES DOWN.
# Four handoffs have called "250-500 Hz in seven to fourteen, the bass's" the real next round. Read by part first
# (walk nine, each group alone, raw): of the mix's 250-500 Hz the guitars are 45%, the ondes 21%, the kit 14%, the
# horn 12%, the voices 5% and the BASS 3%. The by-part read's "+5.7" is the bass's own shape, not what it adds;
# nothing done to the bass can move that band. A third of it is the ondes and the horn, which no record has: the
# song's own, left alone. What a guitar round CAN do is put the guitars where the records' guitars are: alone
# against the six records' guitar stems they stood 3.2 dB short at 120-250 Hz and 4.2 over at 500 Hz-1 kHz (1.3
# over at 250-500). So: the amp looser (tight 180 -> 150 Hz) and a little at 150 Hz for the chest; a cut at 700 Hz
# and a smaller one at 350; the fader up 0.6 dB so the two are as loud. And with the amp loose the palm's THUMP
# makes a muted stroke's low end die (In the Time Of v29's finding, true here): thump off.
# the tracks ; what is added to each one's patch ; the bands of an eq on each ; dB on each fader ; the loudness
# target (None = unchanged). --without-weight = v20 byte for byte ; --weight JSON changes fields for a bench.
WEIGHT = {'tracks': ('left', 'right'), 'rig': 'fx.1.tight=150 synth.layers.0.thump.mod.0.amount=0',
          'eq': ('peak cutoff=350 q=1 gain=-2dB', 'peak cutoff=700 q=1 gain=-3dB', 'peak cutoff=150 q=1 gain=1.5dB'), 'gain': 0.6, 'loudness': None}
# v22 (chirper-three; palette round, one instrument: the wall pair, 3:43.2-4:10.6, its nine chords): THE WALL AT 160
# GETS A SPEAKER. The two wall guitars play only at the top of the song (160, then 80 and 40), and there they are most
# of it: 78% of the mix's 250-500 Hz, 69% of its 500 Hz-1 kHz, 44% of 1-2 kHz. They were the last guitars on the album
# (but the paused t4 and Still Owing's `weight`) still on the library rig's captured cabinet files; Harry's answer of
# 17 Nov on the walls was "The engine's cabinet is nearer", and seven songs have made the swap. Read alone beside the
# records' guitar alone (cabspec, after the bar): 4.31; nothing under 100 Hz (the 80 Hz third 15.6 dB short, where the
# chord's fifth is: 81.9 Hz), a box (+9.4 at 315 Hz, +5.5, +5.9 at 400, 500) and no top (-12.1, -17.3, -12.9 at 8, 10,
# 12.5 kHz). And the MIX at the top stood 2.5 dB short at 60-120 Hz (2.9 beside the voiceless records) and 2.2 over at
# 250-500: the top's bass note is the fifth harmonic's (54.6 Hz), so the bass's weight is under 60 Hz there (alone:
# 60-120 Hz 5 dB lower than in the climb, under 60 Hz 8 dB higher) and nothing held 60-120 but the kick.
# NOW: the captured cabinet and the patch's own eq off, the engine's 4x12 (microphone 0.4, a cone each), then an eq:
# +6 dB at 95 Hz (between the chord's fifth and its octave, 81.9 and 109.1 Hz), +2 at 700 Hz, -3 at 1.5 kHz; the old
# track eq (6 dB out at 380 Hz, a cure for the captured cabinet's box) goes; fader +2 dB, which holds the pair's level
# (alone +0.14 dB K; against everything else -2.0 -> -1.8 dB at the top).
# READ: alone 4.31 -> 2.50 (80 Hz -15.6 -> -1.1; 315 Hz +9.4 -> +4.4; 8, 10, 12.5 kHz -> -2.5, -4.2, -3.2). The mix at
# the top beside the voiceless records 1.211 -> 0.611 and beside all eleven 1.444 -> 1.044 (60-120 Hz -2.5 -> -0.3,
# 250-500 +2.2 -> +0.2, 1-2 kHz +2.1 -> +1.0); in 80 and 40, 1.578 -> 1.156 and 1.778 -> 1.589. The pair's share of the
# mix's 60-120 Hz 12% -> 53%, of 250-500 Hz 78% -> 71%, of 500 Hz-1 kHz 69% -> 51%. Outside 3:43.2-4:11 the finished
# file is within 0.027 dB of v21 on three seeds (-58.9 dB or lower); the top is 0.01 to 0.13 dB lower; target unmoved.
# COSTS: the pair now holds half of the mix's 60-120 Hz at the top, and alone it is 4.6 dB over the records' guitar
# from 71 to 141 Hz (it was 3.1 short; the 80 Hz third is level, the 100 Hz third +9.7 because the chord's octave is
# in it): the lift is set by the MIX's hole, not by the guitar alone. With no lift and the old fader (benched) the pair
# alone is level with the records' there (+0.4); with a lift of 2 dB the mix is still about 1.6 to 2.0 short at 60-120 Hz
# (the bench's arithmetic, less the 0.7 dB it proved too kind by on the one kept) and the pair a third of that band. 141-282 Hz alone -2.5 -> -5.2. The mix beside the records WITH a voice is 3.0 short at
# 500 Hz-1 kHz at the top (was 1.1; beside the voiceless +1.2 -> -0.7). The pair's peaks are 3.1 dB higher alone.
# NOT THE CURE (benched): the old cabinets with 8 dB at 95 Hz (there is nothing there to lift: the 80 Hz third still
# 9.8 short, the top still 14 to 19 short) ; the bass, 5 dB at 109 Hz after its compressor (its octave is 7 dB under
# its fundamental at the top: the mix's 60-120 Hz moved 0.7 dB and its under-60 0.6 the wrong way) ; microphone 0.5.
# the tracks ; what is added to each one's patch (the captured cabinet and the patch's own eq off) ; the engine's
# cabinet: its microphone and a cone for each track ; the bands of the eq after it ; dB on each fader ; the loudness
# target (None = unchanged). --without-speaker = v21 byte for byte ; --speaker JSON changes fields for a bench.
SPEAKER = {'tracks': ('wall-left', 'wall-right'),
           'rig': 'fx.3.mix=0 fx.4.bands.0.gain=0dB fx.4.bands.1.gain=0dB fx.4.bands.2.gain=0dB fx.4.bands.3.gain=0dB',
           'mic': 0.4, 'cones': (101, 102),
           'eq': ('peak cutoff=95 q=1 gain=6dB', 'peak cutoff=700 q=1 gain=2dB', 'peak cutoff=1500 q=1 gain=-3dB'), 'gain': 2.0, 'loudness': None}

TOUCH = {'per': 2.0, 'over': 16, 'crest': 0.625, 'points': 8, 'least': 1.0, 'loudness': -9.521}

# v23 (chirper-two; instrument round: the bass drum, 968 strokes, in every walk but twelve and thirteen; no stroke is
# added, moved or removed): THE BASS DRUM IS FITTED. It is the album kit's stock drum, retuned to B flat by v4 and
# never read at the stroke until v22's note did (and left it). Alone beside six records' kicks (kickspec, shapes):
# 9.15 from them; nothing at 100-125 Hz (4 dB short) with 11 dB too much at 160-200 Hz and 16 at 315 (its drive's
# third and fifth harmonics: 175 and 291 Hz); its low end 20 dB down only after 118 ms (79 by chirper-alpha's
# measure; the records 37 to 49), and 368 of its strokes are a sixteenth (115 ms) from the next, so in a run each
# stroke landed on the last one's tail (16.7 dB under its top). And in the MIX the song was over at 4-8 kHz in nine
# of ten windows (+0.4 to +1.5), which was this drum's click as much as any cymbal.
#   THE TAIL 210 -> 170 ms (20 dB down after 96 ms; 62 by the other measure; a run's strokes 20.0 dB apart). Shorter
#       read better alone and WORSE in the mix (130 ms with a decibel more fader: the song 0.7 to 1.6 dB short
#       under 60 Hz in six windows that had been within 0.5): this drum is most of the song's sub, so its tail is
#       the mix's to choose, as on Common Measure.
#   A CHEST: a bare sine an octave over the drum (B flat 2, 116.5 Hz, 90 ms), on every stroke with the stroke's own
#       velocity and the drum's own size lane, its own track past the drums bus, -9 dB. -6, -9 and -13 dB read
#       alike in the mix (within 0.03); no chest at all read 0.02 worse; the middle is kept.
#   THE BUZZ: -5 dB at 175 Hz and -2 at 291, narrow. Deeper at 291 and a third cut at 408 Hz read the same over all
#       and took 0.7 dB from the climb's 250-500 Hz, where the song is already 2.6 short: not kept.
#   THE CLICK: the 4.3 kHz lift 7 -> 4 dB. By the mix: at 7 the song's 4-8 kHz is over in nine windows, at 3 under in
#       three; at 4 it is within 0.6 in nine. The drum's first 30 ms then stand 0.1 to 0.4 dB lower against
#       everything else (K), its first 90 ms under 150 Hz 0.0 to 0.3 higher.
#   THE FADER +0.6 dB (for the shorter tail), and the target re-fitted on the walks with no bass drum (twelve and
#       thirteen, 2:07-2:28): -9.521 -> -9.467.
#   AFTER: alone 9.15 -> 8.31 (967 strokes: 9.16 -> 8.32); the song against the eleven records, ten windows:
#       1.040 -> 0.919 beside their mixes (nearer in nine, one the same), 1.096 -> 1.044 beside their passages with
#       no voice, 1.241 -> 1.087 with one (all ten nearer); under 250 Hz alone 0.910 -> 0.737.
# what is added to the kick track's patch (overrides inside the kit's bass drum) ; the bands of the kick track's eq
# (None = as they were) ; the chest: semitones over the drum, its length in ms, its fader in dB (None = no chest) ;
# dB on the kick's fader ; the loudness target (None = unchanged). --without-fitted = v22 byte for byte ; --fitted
# JSON changes fields for a bench.
FITTED = {'kick': 'kit.k.patch.synth.amp.d=170ms',
          'eq': ('peak cutoff=4300 q=0.8 gain=4dB', 'peak cutoff=175 q=3 gain=-5dB', 'peak cutoff=291 q=3 gain=-2dB'),
          'chest': (12, 90, -9.0), 'gain': 0.6, 'loudness': -9.467}

# v24 (chirper-zero; instrument round): THE SNARE IS ONE OF THE STRING'S HARMONICS. Every pitched thing in this song
# is a true harmonic of the low F string (Harry on the heights: "True harmonics: keep them") except the drum that
# lands on every backbeat. The album's snare sounds 1.8 semitones over its written note: 244.3 Hz, between the
# string's fifth harmonic (218.27 Hz) and its sixth (261.9), 5.6 times the string, and a different pitch on each
# stroke (the kit's random pitch, 43 cents from the lowest stroke to the highest). It is not hidden: in the FINISHED
# file, at the 61 backbeats of walks nine to eleven, the mix rises 11.2 dB round that line when the snare lands.
# Now the snare's written note is its sounding note (the engine's drum fields of 20 Nov, tune_sounding + tune_exact)
# and that note is the string's FIFTH HARMONIC, 218.27 Hz (m56.863, the height the count sings most after F):
# read dry 218.6 Hz, +3 cents, every stroke within 4 cents. The random pitch is off; the stroke's own 16 ms chirp
# stays (without it this is another drum). The fifth and not the sixth, because there the drum's note also sits
# where six records' snares have theirs: alone (tools/snarespec.py) 4.95 -> 3.11, its 200 Hz band from 16.7 dB
# under theirs to 2.6 over (on the sixth harmonic it read 6.52, on the eleventh's octave 4.66). The whole drum moves
# down 195 cents with its note, which took 2 dB off its top: a shelf at 7 kHz gives that back, and the fader
# +0.1 dB makes it as loud alone as it was.
# the snare's pitch ; what is added inside its patch (kit.s.patch.) ; its track's eq bands (None = none) ; dB on its
# fader ; the loudness target (None = unchanged). --without-fifth = v23 byte for byte ; --fifth JSON for a bench.
FIFTH = {'pitch': 'm56.863',
         'patch': 'synth.layers.0.tune_sounding=true synth.layers.0.tune_exact=true synth.pitch.mod.1.amount=0',
         'eq': ('highshelf cutoff=7000 gain=2dB',), 'gain': 0.1, 'loudness': None}


def true(ratio):
    """A pitch as its exact ratio over the low F: the engine's fractional key number (a whole one is written as its name)."""
    m = F1 + 12 * math.log2(ratio)
    return name(round(m)) if abs(m - round(m)) < 1e-9 else f'm{m:.3f}'


def over(n):
    """Harmonic n brought down into the octave over the low F: its ratio, from 1 up to 2."""
    while n >= 2:
        n /= 2
    return n


def name(p):
    return NOTES[p % 12] + str(p // 12 - 1)


def walk(n):
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


def parts_of(n):
    """n = odd * 2**twos -> (odd, unit in sixteenths)."""
    unit = 1
    while n % 2 == 0:
        n //= 2
        unit *= 2
    return n, unit


def height(n):
    """The n-th harmonic of the low F, to the nearest semitone over F1."""
    return round(12 * math.log2(n))


def phrase(m):
    """Number m's phrase, once round: [(sixteenths in, sixteenths to its next stroke, whether it is a head)]."""
    odd, unit = parts_of(m)
    bits = bin(odd)[2:]
    strokes = [u for u in range(odd) if bits[u % len(bits)] == '1']
    return [(u * unit, ((strokes[i + 1] if i + 1 < len(strokes) else odd) - u) * unit, u % len(bits) == 0) for i, u in enumerate(strokes)]


def compose(lead_gain=-7.0, storeys=True, low_bus=True, kit=True, sized=True, body=True, tuned=True, memory=True, count=True, still=True, one=True, ceiling=True, said=True, clear=True):
    low_bus = low_bus and storeys  # --without-storeys still gives v1
    sized = sized and kit and low_bus
    body = body and sized
    tuned = tuned and body
    memory = memory and tuned
    count = COUNT if count and memory else None
    still = STILL if still and count else {}                 # --without-count still gives v8
    one = ONE if one and count else None
    ceiling = CEILING if ceiling and one and still else None  # every older switch still gives what it gave
    told = SAID if said and ceiling else None                 # (`said` is v9's own list below)
    clear = CLEAR if clear and told else None
    T = {k: [] for k in ('left', 'right', 'bass', 'kick', 'snare', 'metal', 'stone') + (('wall-left', 'wall-right') if storeys else ()) + (('hat',) if memory else ())}
    lifted = []

    def put(tr, at, dur, p, v, mute=False):
        e = dict(at=round(at / SUB, 6), len=round(dur / SUB, 6), pitch=name(p) if isinstance(p, int) else p, vel=round(v, 3))
        if mute:
            e['expr'] = {'pm': 1.0}
        T[tr].append(e)

    # ---- the walks, end to end
    cells, marks, t = [], [], 0          # (start, n, which walk, first of its walk); where each walk starts
    for k in range(FIRST, LAST + 1):
        marks.append((k, t))
        for i, n in enumerate(walk(k)):
            cells.append((t, n, k, i == 0))
            t += n
    wheel = t
    for _ in range(TURNS):
        for i, n in enumerate((4, 2, 1)):
            cells.append((t, n, 0, False))
            t += n
    assert wheel == 2311 and t % BAR == 0, (wheel, t)      # the wheel brings the song back to a bar line
    end = t

    for j, (at, n, k, first) in enumerate(cells):
        odd, unit = parts_of(n)
        bits = bin(odd)[2:]
        strokes = [u for u in range(odd) if bits[u % len(bits)] == '1']
        pc = height(n) % 12
        root = F1 + pc + (12 if n >= 16 else 0)             # the guitars fall an octave with the number, once
        ratio = over(n) * (2 if n >= 16 else 1)             # v7: the same place, exactly
        assert abs(12 * math.log2(ratio) - (root - F1)) <= 0.5, n
        chord = true(ratio) + ',' + true(ratio * 1.5) if tuned else name(root) + ',' + name(root + 7)
        low_note = true(over(n)) if tuned else F1 + pc      # the bass's
        sides = () if k in QUIET else ('left',) if 0 < k < 7 else ('left', 'right')   # the second guitar comes in with the first long walk
        # Where a phrase is said in half notes or slower (40, 80, 160: stroke, rest, stroke at eight, sixteen and
        # thirty-two sixteenths a place) the right guitar says the SAME phrase small under it, in sixteenths, muted on
        # the low string, with the kick: five against the kit's four, the number's fast self under its slow one.
        # A power of two has no phrase but its one stroke, and keeps its silence.
        under = unit >= 8 and odd > 1 and 'right' in sides
        storey = storeys and k == 15 and n in SUMMIT        # v2: forty's phrase is the bass's here, eighty's the second pair's
        for i, u in enumerate(strokes):
            s = at + u * unit
            gap = ((strokes[i + 1] if i + 1 < len(strokes) else odd) - u) * unit
            head = u % len(bits) == 0                        # the phrase's first stroke: the number's own note
            if head:
                ring = min(gap, 32) * (0.93 if gap > 1 else 1.0)
                for g in sides:
                    put(g, s, min(ring, 1.8) if under and g == 'right' else ring, chord, 0.99 if u == 0 else 0.93)
                if (k == 0 or k >= 3) and not storey:
                    put('bass', s, ring, low_note, 0.95 if u == 0 else 0.9)
                    if k in QUIET:
                        T['bass'][-1].update(vel=0.7, gain='-5dB')
            else:                                            # every other stroke is the low string, muted: the fundamental
                for g in sides:
                    put(g, s, min(unit, 2) * 0.9, F1, 0.84, mute=True)
                if (k == 0 or k >= 3) and k not in QUIET and not storey:
                    put('bass', s, min(unit, 2) * 0.8, F1, 0.82)
            if k not in QUIET:
                put('kick', s, 0.8, 'k', 0.97 if u == 0 else 0.86)
        if storey:
            for c in range(n // 40):
                for off, gap, head in phrase(40):            # exactly what the bass plays at 40 itself
                    put('bass', at + 40 * c + off, *((min(gap, 32) * 0.93, low_note, 0.95 if off == 0 else 0.9) if head else (1.6, F1, 0.82)))
            low = root + 12 * STOREY[3]
            for c in range(n // 80):
                for off, gap, head in phrase(80):
                    for g in ('wall-left', 'wall-right'):
                        if head:
                            put(g, at + 80 * c + off, min(gap, 32) * 0.93, ','.join(true(ratio * 2 ** STOREY[3] * q) for q in (1, 1.5, 2)) if tuned else
                                ','.join(name(low + i) for i in (0, 7, 12)), 0.97 if off == 0 else 0.93)
                        else:
                            put(g, at + 80 * c + off, 1.8, F1, 0.84)
                    if head:
                        lifted.append(at + 80 * c + off)
        if under:
            taken = {u * unit for u in strokes} | {u * unit + 1 for u in strokes if u % len(bits) == 0}
            for q in range(n):
                if bits[(q % odd) % len(bits)] == '1' and q not in taken:
                    put('right', at + q, 0.9, F1, 0.72, mute=True)
                    put('kick', at + q, 0.8, 'k', 0.78)
        # the ondes is the number itself: its true height, for its whole length. It slides down the octave when the
        # number is halved (the ribbon) and lifts off before a leap, so the leap is a new note.
        p = F1 + height(n)
        nxt = cells[j + 1][1] if j + 1 < len(cells) else None
        leap = nxt is None or nxt > n or F1 + height(nxt) > TOP
        if p <= TOP:
            # v10: a trebled number is three times the last one AND ONE. The ondes arrives on three times the last
            # number (a new note: it lifted off before the leap), stays there for the one sixteenth that was added
            # to the length, and its ribbon is pushed up the hair to the number itself.
            was = cells[j - 1] if j else None
            trebled = bool(one and was and was[1] % 2 and n == 3 * was[1] + 1 and (was[2] == k and k or one[1]))
            lift = 0.5 if leap and n > 1 else 0
            if trebled:
                put('stone', at, one[0], true(n - 1), 0.74)
                put('stone', at + one[0], n - one[0] - lift, true(n), 0.74)
            else:
                put('stone', at, n - lift, true(n) if tuned else p, 0.82 if first else 0.74)
            if p > 60:
                for e in T['stone'][-2 if trebled else -1:]:
                    e['gain'] = f'{-TILT * (p - 60) / 12:.1f}dB'
        elif ceiling:
            # v11: the number is over the top of the ribbon. The ondes sings it in the highest octave it can reach
            # (a number over the top is always even, so that is where the walk will come down to), struck as a new
            # note for every number, with v10's push where the number was trebled-and-one: the hair is the same hair.
            m, down = n, 1
            while F1 + height(m) > TOP:
                assert m % 2 == 0, n
                m, down = m // 2, down * 2
            was = cells[j - 1]
            trebled = bool(was[1] % 2 and n == 3 * was[1] + 1 and was[2] == k)
            if trebled:
                put('stone', at, one[0], true((n - 1) / down), 0.74)
                put('stone', at + one[0], n - one[0] - 0.5, true(m), 0.74)
            else:
                put('stone', at, n - 0.5, true(m), 0.74)
            for e in T['stone'][-2 if trebled else -1:]:
                e['gain'] = f'{-TILT * (F1 + height(m) - 60) / 12 + ceiling[0]:.1f}dB'

    for s in lifted:                                          # the foot goes with the second pair's chords
        hit = [e for e in T['kick'] if e['at'] == round(s / SUB, 6)]
        assert hit, s
        hit[0]['vel'] = max(hit[0]['vel'], 0.95)
    top = next(at for at, n, k, _ in cells if n == 160)
    # ---- the kit keeps common time, whatever the walks do
    walks_at = {at: k for k, at in marks}
    feel = lambda k: 'back' if k in (9, 10, 11, 15) else 'half'
    which = lambda s: max((k for k, at in marks if at <= s), default=1) if s < wheel else 0
    paths = {k: set(walk(k)) for k in range(FIRST, LAST + 1)}

    def known(k, n):
        """How the hands play number n in walk k (v8): 1 new, 2 said once before, 3 twice, 4 three times or more."""
        said = 1 + sum(n in paths[j] for j in range(FIRST, k))
        return min(said, 2 if n & (n - 1) == 0 else 4)
    for s in range(0, end, 4):                               # quarters
        k = which(s)
        beat = (s % BAR) // 4
        now = next(n for at, n, _, _ in reversed(cells) if at <= s)
        slow = parts_of(now)[1] >= 4
        if s >= marks[2][1]:                                 # the cymbals come in with three
            put('metal', s, 3.6, 'x' if storeys and top <= s < top + 160 else 'rde' if slow or k in QUIET else 'x', (0.62 if beat == 0 else 0.5) - (0.12 if k in QUIET else 0))
            if k in QUIET:
                if beat == 2:
                    put('snare', s, 0.8, 'ss', 0.72)         # a stick across the rim
            elif memory and k >= MEMORY[0]:
                lv = known(k, now)
                if (lv == 1 and beat == 2) or (lv in (2, 3) and beat in (1, 3)):
                    put('snare', s, 0.8, 's', 0.96)
                if lv == 3:
                    put('hat', s + 2, 0.8, 'h', MEMORY[2])
                if lv == 4:
                    put('snare', s + 2, 0.8, 's', MEMORY[3])
                    T['snare'][-1]['gain'] = f'{MEMORY[4]}dB'
            elif (feel(k) == 'half' and beat == 2) or (feel(k) == 'back' and beat in (1, 3)):
                put('snare', s, 0.8, 's', 0.96)
        if beat == 0 and s >= marks[2][1] and k not in QUIET and not any(e['at'] == s / SUB for e in T['kick']):
            put('kick', s, 0.8, 'k', 0.9)                    # the bar's own downbeat
    for k, at in marks:
        if k >= 3:
            put('metal', at, 3.6, 'c', 0.9 if k in (7, 9, 14, 15) else 0.5 if k in QUIET else 0.78)
    put('metal', wheel, 3.6, 'c', 0.85)
    if storeys:
        put('metal', top, 3.6, 'c', 0.9)
    # the last bar line: four again
    for g in ('left', 'right'):
        put(g, end, 30, name(F1) + ',' + (true(1.5) if tuned else name(F1 + 7)) + ',' + name(F1 + 12), 1.0)
    put('bass', end, 30, F1, 0.97); put('kick', end, 0.8, 'k', 1.0); put('metal', end, 3.6, 'c', 0.95)
    put('stone', end, 28, F1 + 24, 0.8)
    length = end + 2 * BAR

    def track(tr, patch, gain, pan=0, **kw):
        ns = sorted(T.pop(tr), key=lambda e: e['at'])
        assert ns and all(0 <= e['at'] < length / SUB for e in ns)
        return dict(name=tr, patch=patch, gain=f'{gain}dB', pan=pan, notes=ns, **kw)
    palm = ' synth.layers.0.mute=expr.pm*0.6 synth.layers.0.mute_width=0.1'
    quiet = {}
    if low_bus:
        # In the two quiet walks (twelve, thirteen) the bass and the ondes are alone, and v1 plays the bass 5 dB down
        # there. The chain's compressor gives most of that back (the stretch came out 0.6 dB louder in the finished
        # file: the song's one quiet place would have lost a tenth of its drop), and a trim on the notes is undone
        # the same way (tried: 1.5 dB off each note moved the stretch 0.02 dB). So the trim is on the fader, after
        # the chain, for those two walks only.
        a, z = (dict(marks)[QUIET[0]] / SUB, dict(marks)[QUIET[-1] + 1] / SUB)
        trim = BODY[2] if body else BASS_QUIET
        quiet = {'auto': {'quiet': {'curve': 0, 'points': [['0b', 0], [f'{a - 0.02:g}b', 0], [f'{a:g}b', trim],
                                                           [f'{z - 0.02:g}b', trim], [f'{z:g}b', 0]]}}}
    drum = 'ct-kit-so-far' if kit else 'ct-kit'
    size = None
    if sized:
        pts, prev = [], None
        for at, n, _, _ in cells:
            v = round(SIZE[0] * math.log2(n / SIZE[1]), 2)
            if v != prev:
                pts += ([[f'{at / SUB - 0.02:g}b', prev]] if prev is not None and at else []) + [[f'{at / SUB:g}b', v]]
                prev = v
        pts += [[f'{end / SUB - 0.02:g}b', prev], [f'{end / SUB:g}b', SIZE[2]]]
        size = {'curve': 0, 'points': pts}

    def sized_track(t, cap=None):
        """The fader follows the number: after the amp and after the bass's chain, where a level is still a level.
        With `cap` the lane never goes over it (the foot settles with the walk and does not hit harder at the top)."""
        if size:
            t['gain'] = t['gain'] if isinstance(t['gain'], dict) else {'value': t['gain'], 'mod': []}
            t['gain']['mod'].append({'src': 'auto.size', 'amount': 1})
            t.setdefault('auto', {})['size'] = size if cap is None else {'curve': 0, 'points': [[b, min(v, cap)] for b, v in size['points']]}
        return t
    tight = f' fx.1.tight={BODY[0]}' if body else ''                 # v6: more of the low string into the amp
    chain = BASS[1][:-1] + [{'type': 'eq', 'bands': [f'peak cutoff=170 q=1.2 gain={BODY[1]}dB']}] if body else BASS[1]
    strings = still.get('strings', '')
    tracks = [sized_track(track('left', 'ct-twin fx.2.cone=97' + tight + palm + strings, 1, -.9)),
              sized_track(track('right', 'ct-twin fx.1.model=gojira fx.2.cone=98' + tight + palm + strings, 1, .9)),
              *([sized_track(track('wall-' + side, STOREY[0].format(side[0]) + strings, STOREY[1], sign * STOREY[2],
                                   fx=[{'type': 'eq', 'bands': [f'peak cutoff=380 q=1 gain={STOREY[4]}dB']}]))   # the album's cut for this rig, deeper
                 for side, sign in (('left', -1), ('right', 1))] if storeys else []),
              # v3: THE BASS GETS THE ALBUM'S CHAIN (the `low` bus of tracks 1, 7, 8 and 14, here on the bass's own track). v1 and v2 had the bass on a bare track. Read against the album's
              # eleven records the long walks stood 1.9 to 2.3 dB over at 20-60 Hz and 1.5 to 2.0 short at 60-120, and
              # the bass sat 10.8 dB under the rest of the band (K, the ninth walk), its level moving 4.7 dB from note
              # to note. Tracks 1, 7, 8 and 14 put this same bass through one chain: its weight moved from the
              # fundamental (44 Hz, the low F) to the octave above (90 Hz), the box out at 350 Hz, 4 dB of string at
              # 1.5 kHz, and a compressor at 8:1. With it the bass stands 9.0 dB under the rest, steadier (3.3 dB), and
              # it holds more of 60-120 Hz and less of 20-60. It cannot mend 20-60 Hz alone: the kick is 78% of it.
              sized_track({**track('bass', 'ct-bass' + still.get('bass', ''), BASS[0], fx=chain, **quiet),
                           'gain': {'value': f'{BASS[0]}dB', 'mod': [{'src': 'auto.quiet', 'amount': 1}]}}) if low_bus else
              track('bass', 'ct-bass', -.5, fx=[{'type': 'eq', 'bands': ['hp cutoff=29', 'peak cutoff=320 q=1 gain=-4dB']}]),
              # The ondes' diffuser is an octave of strings from middle C up (262-494 Hz) that ring with every note, and
              # its low notes sit there too: in the seventh walk it held 45% of 250-500 Hz, where the song read 3.1 to
              # 3.8 dB over the records. Half the halo, and 3 dB off the track at 350 Hz.
              track('stone', 'ondes fx.0.mix=0.15' + still.get('ondes', ''), lead_gain, .1, fx=[{'type': 'eq', 'bands': ['peak cutoff=350 q=0.9 gain=-3dB']}]),
              sized_track(track('kick', drum, KIT['kick gain'] if kit else 2, out='drums', fx=[{'type': 'eq', 'bands': ['peak cutoff=4300 q=0.8 gain=7dB']}]), cap=0),
              track('snare', drum, 3, out='drums'),
              track('metal', drum, KIT['metal gain'] if kit else 1.5, out='drums', **({'fx': [{'type': 'eq', 'bands': KIT['metal']}]} if kit and KIT['metal'] else {})),
              *([track('hat', drum, MEMORY[1], out='drums', fx=[{'type': 'eq', 'bands': KIT['metal']}])] if memory else [])]
    assert not T
    if count:
        def word(at, n, trim=0, ring=None):
            """The number n said from sixteenth `at`, on its own harmonic in the voice's octave (F3 up)."""
            out, t = [], at / SUB
            for ph, ln in SAY[n]:
                g = trim + count['lift'].get(ph, 0) + (clear['even'].get(n, 0) if clear else 0)
                out.append({'at': round(t, 6), 'len': ring or ln, 'pitch': true(4 * over(n)), 'vel': 0.9, 'ph': ph, **({'gain': f'{g:g}dB'} if g else {})})
                t += ln
            return out
        said = [(at, n, k) for at, n, k, _ in cells if k in (15, 16)]
        said = said[[n for _, n, _ in said].index(count['from']):]
        one = [e for at, n, k in said if not (k == 15 and n == 1) for e in word(at, n)]
        five = [e for at, n, k in said if k == 16 for e in word(at, n)]
        for turn in range(TURNS):                             # the wheel: two turns of nothing, then a word a turn
            if turn % 5 >= 2:
                i = turn % 5 - 2
                last = turn == TURNS - 1
                one += word(wheel + 7 * turn + (0, 4, 6)[i], (4, 2, 1)[i], count['last'] if last else count['wheel'][turn // 5], ring=.85 if i == 0 else .6 if i == 1 else None)
        if told:
            # v12: a number is said wherever an earlier walk has crossed it: by the one voice, and by the five as
            # well once `everyone` walks have. Nobody says a number no walk has reached yet. In the two quiet walks
            # the one voice says it alone and lower. A walk's last "one" is a sixteenth long: a voice that has the
            # next walk's first number to say leaves it out (v9: "the next walk's 'sixteen' is on its heels").
            crossed = lambda k, n: sum(n in paths[j] for j in range(FIRST, k))
            who = lambda k, n: (() if not crossed(k, n) or (k in QUIET and told['quiet'] is None) else
                                ('one',) if k in QUIET or crossed(k, n) < told['everyone'] else ('one', 'five'))

            def tell(at, n, trim):
                out, t = [], at / SUB
                for ph, ln in SAY[n]:
                    g = trim + told['lift'].get(n, 0) + count['lift'].get(ph, 0) + (clear['even'].get(n, 0) if clear else 0)
                    out.append({'at': round(t, 6), 'len': ln, 'pitch': true(4 * over(n)), 'vel': 0.9, 'ph': ph, **({'gain': f'{g:g}dB'} if g else {})})
                    t += ln
                return out
            for at, n, k, _ in cells:
                if 0 < k < 15:
                    for v in who(k, n):
                        if n == 1 and v in who(k + 1, k + 1):
                            continue
                        (one if v == 'one' else five).extend(tell(at, n, told['quiet'] if k in QUIET else told[v]))
            for part in (one, five):
                part.sort(key=lambda e: e['at'])
                assert all(a['at'] + a['len'] <= b['at'] + 1e-6 for a, b in zip(part, part[1:])), 'a word runs into the next'
        tracks += [{'name': 'count', 'patch': count['one'][0], 'gain': f"{count['one'][1] + (clear['gain'] if clear else 0):g}dB", 'pan': 0, 'notes': one,
                    'fx': [{'type': 'eq', 'bands': count['eq'] + (clear['one'] if clear else [])}]},
                   {'name': 'crowd', 'patch': count['five'][0], 'gain': f"{count['five'][1] + (clear['gain'] if clear else 0):g}dB", 'pan': 0, 'notes': five,
                    'fx': [{'type': 'eq', 'bands': count['eq five'] + (clear['five'] if clear else [])}]}]
    doc = {'about': 'So Far. Halve it if it is even; treble it and add one if it is odd. The first sixteen numbers, each walked to one: '
                    'a number is its length in sixteenths, its harmonic over the low F and its own riff. Common Time t17 v1.'
                    + (' v2: at the top of the fifteenth walk (160) two more guitars and the bass already say the phrases of 80 and 40.' if storeys else ''),
           'tempo': BPM, 'seed': 1, 'event_stable': True, 'length': f'{length // SUB}b', 'tail': '4s',
           'ceiling': '-1dB', 'true_peak': True, 'loudness': BASS_LOUDNESS if low_bus else SUMMIT_LOUDNESS if storeys else -10,
           'buses': {'drums': {'fx': ['reverb kind=room decay=0.45s mix=0.07',
                                      'glue threshold=-22dB ratio=2 attack=18ms release=120ms',
                                      {'type': 'eq', 'bands': KIT['bus'] if kit else ['peak cutoff=390 q=0.9 gain=-4dB', 'lp cutoff=14800']}]}},
           **({'patches': {'ct-kit-so-far': {'extends': 'ct-kit', 'kit': {'k': KIT['kick']}}}} if kit else {}),
           'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=25']}]}, 'tracks': tracks}
    if kit:
        doc['loudness'] = KIT['loudness']
    if body:
        doc['loudness'] = BODY[3]
    if memory:
        doc['loudness'] = MEMORY[5]
    if count:
        doc['loudness'] = count['loudness']
        doc['about'] += ' v9: from forty in the fifteenth walk a voice says the numbers as they come; five more say the sixteenth walk; one word a turn on the wheel.'
    if ceiling:
        doc['loudness'] = ceiling[1]
    if told:
        doc['loudness'] = told['loudness']
    if clear:
        doc['loudness'] = clear['loudness']
    return doc, marks, wheel, end


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--lead-gain', type=float, default=-7.0, help="the ondes' track gain in dB")
    ap.add_argument('--form', action='store_true', help='print where each walk starts')
    ap.add_argument('--without-storeys', action='store_true', help='regenerate v1: 160 and 80 without the phrases of 80 and 40 under them')
    ap.add_argument('--string', help='a bench: STRING fields to change, as a JSON object')
    ap.add_argument('--horn', help='a bench: HORN fields to change, as a JSON object')
    ap.add_argument('--wheel', help='a bench: WHEEL fields to change, as a JSON object')
    ap.add_argument('--touch', help='a bench: TOUCH fields to change, as a JSON object')
    ap.add_argument('--without-fifth', action='store_true', help="regenerate v23: the snare between two of the string's harmonics, a different pitch on every stroke")
    ap.add_argument('--fifth', help="JSON over FIFTH's fields, for a bench")
    ap.add_argument('--without-fitted', action='store_true', help="regenerate v22: the album kit's bass drum as v4 tuned it, with no chest")
    ap.add_argument('--fitted', help="JSON over FITTED's fields, for a bench")
    ap.add_argument('--without-speaker', action='store_true', help="regenerate v21: the wall pair through the album's captured cabinets")
    ap.add_argument('--speaker', help="JSON over SPEAKER's fields, for a bench")
    ap.add_argument('--without-weight', action='store_true', help="regenerate v20: the two guitars' rig and eq as they were")
    ap.add_argument('--weight', help="JSON over WEIGHT's fields, for a bench")
    ap.add_argument('--without-touch', action='store_true', help="regenerate v19: the ondes with one hand, every number at one level from its start to its end")
    ap.add_argument('--without-wheel', action='store_true', help="regenerate v18: on the wheel the horn is silent and no bell rings")
    ap.add_argument('--without-horn', action='store_true', help="regenerate v17: nothing holds the number a walk is trying")
    ap.add_argument('--without-string', action='store_true', help="regenerate v16: the ondes through its own palme only, a tempered octave of strings that its harmonics do not ring")
    ap.add_argument('--without-bell', action='store_true', help="regenerate v15: the album's snare as it comes, and a closed hat where a number has been said twice before")
    ap.add_argument('--without-hand', action='store_true', help="regenerate v14: every muted stroke at a full palm, which closes the string's filter to 1 kHz")
    ap.add_argument('--without-china', action='store_true', help="regenerate v13: the kit's own china at the kit's level")
    ap.add_argument('--without-clear', action='store_true', help="regenerate v12: the two voices' eq and faders as v9 set them")
    ap.add_argument('--without-said', action='store_true', help="regenerate v11: nobody says a number before forty in the fifteenth walk")
    ap.add_argument('--without-ceiling', action='store_true', help="regenerate v10: the ondes rests while the number is over the top of its ribbon (70, 106, 160, 80)")
    ap.add_argument('--without-one', action='store_true', help="the ondes's notes of v9: it lands on a trebled number at once")
    ap.add_argument('--without-still', action='store_true', help="the rigs of v9: vibrato and a random detune on the strings and the bass, the ondes's wide vibrato (with --without-one: regenerate v9)")
    ap.add_argument('--without-count', action='store_true', help="regenerate v8: nobody says the numbers")
    ap.add_argument('--without-memory', action='store_true', help="regenerate v7: the hands keep the feel v1 gave each walk, whatever has been said before")
    ap.add_argument('--equal', action='store_true', help='regenerate v6: every number at the nearest semitone to its harmonic, not at the harmonic')
    ap.add_argument('--without-body', action='store_true', help="regenerate v5: the first pair's tight filter at 220 Hz and the bass's 170 Hz cut at 3 dB")
    ap.add_argument('--without-size', action='store_true', help="regenerate v4: every number at one level")
    ap.add_argument('--without-kit', action='store_true', help="regenerate v3: the kit before the kick was retuned and the cymbals and the bus had the album's eq")
    ap.add_argument('--without-low-bus', action='store_true', help="regenerate v2: the bass on its bare track, before it had the album's chain")
    a = ap.parse_args()
    doc, marks, wheel, end = compose(a.lead_gain, not a.without_storeys, not a.without_low_bus, not a.without_kit and not a.without_low_bus and not a.without_storeys, not a.without_size, not a.without_body, not a.equal, not a.without_memory, not a.without_count, not a.without_still, not a.without_one, not a.without_ceiling, not a.without_said, not a.without_clear)
    newest = not a.equal and not any(v for k, v in vars(a).items() if k.startswith('without_') and k not in ('without_china', 'without_hand', 'without_bell', 'without_string', 'string', 'without_horn', 'horn', 'without_wheel', 'wheel', 'without_touch', 'touch', 'without_weight', 'weight', 'without_speaker', 'speaker', 'without_fitted', 'fitted', 'without_fifth', 'fifth'))
    if not a.without_china and newest:
        metal = next(t for t in doc['tracks'] if t['name'] == 'metal')   # every older switch still gives what it gave
        metal['patch'] += ' ' + CHINA['kit']
        walls = [n['at'] for t in doc['tracks'] if t['name'] == 'wall-left' for n in t['notes']]
        under = [n for n in metal['notes'] if n['pitch'] == 'x' and min(walls) <= n['at'] < min(walls) + 40]   # 160 sixteenths: the top
        assert len(under) == 40, len(under)
        for n in under:
            n['gain'] = f"{CHINA['walls']}dB"
        doc['loudness'] = CHINA['loudness']
    if not a.without_hand and not a.without_china and newest:
        said = [(at + sum(walk(k)[:i]), n) for k, at in marks for i, n in enumerate(walk(k))]      # (sixteenth, the number being said)
        said += [(wheel + 7 * turn + off, n) for turn in range(TURNS) for off, n in ((0, 4), (4, 2), (6, 1))]
        assert said == sorted(said) and said[-1][0] + 1 == end, (said[-1], end)
        for t in doc['tracks']:
            if t['name'] in ('left', 'right'):
                t['patch'] += f" synth.filters.0.cutoff.mod.0.amount={HAND['palm']} fx.2.mic={HAND['mic']}"
                for e in t['notes']:
                    if 'expr' in e:
                        n = next(n for at, n in reversed(said) if at <= round(e['at'] * SUB))
                        e['expr'] = {'pm': round(HAND['heavy'] - (HAND['heavy'] - HAND['light']) * min(1.0, math.log2(n) / math.log2(HAND['top'])), 3)}
        if HAND['loudness'] is not None:
            doc['loudness'] = HAND['loudness']
    if not a.without_bell and not a.without_hand and not a.without_china and newest:
        said = [(at + sum(walk(k)[:i]), n) for k, at in marks for i, n in enumerate(walk(k))]      # (sixteenth, the number being said)
        number = lambda beat: next(n for at, n in reversed(said) if at <= round(beat * SUB))
        snare = next(t for t in doc['tracks'] if t['name'] == 'snare')
        snare['patch'] += ' ' + BELL['snare']           # on the drum itself: the stick on the rim (the quiet walks) shares the track and is not touched
        if BELL['fader'] is not None:
            snare['gain'] = f"{BELL['fader']:g}dB"
        j = next(j for j, t in enumerate(doc['tracks']) if t['name'] == 'hat')
        hat = doc['tracks'][j]
        # even: it will be halved, an octave: the string's sixteenth harmonic, F. Odd: it will be trebled, a twelfth: the twenty-fourth, C.
        doc['tracks'][j] = {'name': 'bell', 'patch': BELL['bell'], 'gain': f"{BELL['gain']:g}dB", 'pan': BELL['pan'],
                            'notes': [{'at': e['at'], 'len': 0.25, 'pitch': 'ah' if number(e['at']) % 2 else 'al', 'vel': BELL['vel']} for e in hat['notes']]}
        if BELL['loudness'] is not None:
            doc['loudness'] = BELL['loudness']
    if not a.without_string and not a.without_bell and not a.without_hand and not a.without_china and newest:
        said = [(at + sum(walk(k)[:i]), n, k) for k, at in marks for i, n in enumerate(walk(k))]   # (sixteenth, the number being said, its walk)
        said += [(wheel + 7 * turn + off, n, LAST + 1) for turn in range(TURNS) for off, n in ((0, 4), (4, 2), (6, 1))]
        paths = {k: set(walk(k)) for k in range(FIRST, LAST + 1)}
        told = lambda k, n: min(4, 1 + sum(n in paths[j] for j in range(FIRST, min(k, LAST + 1))))  # 1 new .. 4 said three times or more
        if a.string:
            STRING.update(json.loads(a.string))

        def lane(values, wheel_v, high=1.0):
            pts, was = [], None
            for at, n, k in said:
                v = wheel_v if k > LAST else round(values[told(k, n) - 1] * (high if n >= STRING['high'][0] else 1), 3)
                if was is None:
                    pts.append(['0b', v])
                elif v != was:
                    pts += [[f"{at / SUB - STRING['ramp']:g}b", was], [f'{at / SUB:g}b', v]]
                was = v
            return {'points': pts, 'curve': 0}
        stone = next(t for t in doc['tracks'] if t['name'] == 'stone')
        stone['fx'] = stone['fx'] + [{'type': 'sympathetic', 'notes': f"{STRING['hz']:g}hz", 'decay': STRING['decay'],
                                      'mix': {'value': 0, 'mod': [{'src': 'auto.known', 'amount': 1}]}}]
        stone['auto'] = {'known': lane(STRING['mix'], STRING['wheel'][0])}
        if any(STRING['trim']) or STRING['wheel'][1]:
            stone['gain'] = {'value': stone['gain'], 'mod': [{'src': 'auto.even', 'amount': 1}]}
            stone['auto']['even'] = lane(STRING['trim'], STRING['wheel'][1], STRING['high'][1])
        if STRING['loudness'] is not None:
            doc['loudness'] = STRING['loudness']
    if not a.without_horn and not a.without_string and not a.without_bell and not a.without_hand and not a.without_china and newest:
        if a.horn:
            HORN.update(json.loads(a.horn))
        notes = []
        for k, at in marks:
            if k not in HORN['walks']:
                continue
            w, pos, start, held = walk(k), at, at, 0
            for i, n in enumerate(w):
                leapt = i > 0 and w[i - 1] % 2 == 1                        # this number was reached by trebling: a new breath
                if i > 0 and (leapt or held + n > HORN['cap']):
                    notes.append((start, pos - start))
                    start, held = pos, 0
                pos += n
                held += n
            notes.append((start, pos - start))
        which = lambda s16: next(k for k, at in reversed(marks) if at <= s16)
        firsts = {at for k, at in marks}
        lift = lambda s: (HORN['high'][1] if HORN['high'] and which(s) >= HORN['high'][0] else 0) + (HORN['call'] if s in firsts else HORN['pedal'])
        doc['tracks'].append({'name': 'horn', 'patch': HORN['patch'], 'gain': f"{HORN['gain']:g}dB", 'pan': HORN['pan'],
                              **({'fx': [{'type': 'eq', 'bands': list(HORN['eq'])}]} if HORN['eq'] else {}),
                              'notes': [{'at': round(s / SUB, 6), 'len': round(max(1, d - HORN['breath']) / SUB, 6), 'pitch': true(which(s)), 'vel': HORN['vel'],
                                         **({'gain': f"{lift(s):g}dB"} if lift(s) else {})} for s, d in notes]})
        if HORN['loudness'] is not None:
            doc['loudness'] = HORN['loudness']
    if not a.without_wheel and not a.without_horn and not a.without_string and not a.without_bell and not a.without_hand and not a.without_china and newest:
        if a.wheel:
            WHEEL.update(json.loads(a.wheel))
        turn = sum(n for off, n in ((0, 4), (4, 2), (6, 1)))               # seven sixteenths
        assert sum(WHEEL['horn']) <= TURNS and wheel + TURNS * turn == end
        horn = next(t for t in doc['tracks'] if t['name'] == 'horn')
        at = wheel + (TURNS - sum(WHEEL['horn'])) * turn                   # the last of them ends on the last bar line
        for n, g in zip(WHEEL['horn'], WHEEL['gain']):
            horn['notes'].append({'at': round(at / SUB, 6), 'len': round((n * turn - WHEEL['breath']) / SUB, 6), 'pitch': true(n), 'vel': HORN['vel'],
                                  **({'gain': f'{g:g}dB'} if g else {})})
            at += n * turn
        assert at == end
        if WHEEL['bell']:
            bell = next(t for t in doc['tracks'] if t['name'] == 'bell')
            for k in range(TURNS):
                for off, n in ((0, 4), (4, 2), (6, 1)):
                    if n in WHEEL['bell']:
                        bell['notes'].append({'at': round((wheel + k * turn + off) / SUB, 6), 'len': 0.25, 'pitch': 'ah' if n % 2 else 'al', 'vel': WHEEL['bell vel'],
                                              **({'gain': f"{WHEEL['bell gain']:g}dB"} if WHEEL['bell gain'] else {})})
            if WHEEL['last'] and 4 in WHEEL['bell']:
                bell['notes'].append({'at': round(end / SUB, 6), 'len': 0.25, 'pitch': 'al', 'vel': WHEEL['bell vel'],
                                      **({'gain': f"{WHEEL['bell gain']:g}dB"} if WHEEL['bell gain'] else {})})
        if WHEEL['loudness'] is not None:
            doc['loudness'] = WHEEL['loudness']
    if not a.without_touch and not a.without_wheel and not a.without_horn and not a.without_string and not a.without_bell and not a.without_hand and not a.without_china and newest:
        if a.touch:
            TOUCH.update(json.loads(a.touch))
        said = [(at + sum(walk(k)[:i]), n) for k, at in marks for i, n in enumerate(walk(k))]      # (sixteenth, the number being said)
        number = lambda beat: next((n for at, n in reversed(said) if at <= round(beat * SUB)), 0)
        stone = next(t for t in doc['tracks'] if t['name'] == 'stone')
        # the key is ahead of the speakers: both of the patch's layers follow it, so the string and the hall ring with what it lets through
        stone['patch'] = {'extends': stone['patch'],
                          'synth': {'layers': [{'name': 'main', 'wave': 'sine', 'level': {'value': '0dB', 'mod': [{'src': 'expr.touch', 'amount': 1}]}},
                                               {'name': 'edge', 'wave': 'triangle', 'level': {'value': '-22dB', 'mod': [{'src': 'vel', 'amount': 12}, {'src': 'expr.touch', 'amount': 1}]}}]}}
        crest, pts = TOUCH['crest'], TOUCH['points']
        shape = lambda u: math.sin(math.pi / 2 * u / crest) ** 2 if u <= crest else math.cos(math.pi / 2 * (u - crest) / (1 - crest)) ** 2
        for e in stone['notes']:
            n = number(e['at'])
            if round(e['at'] * SUB) < wheel and n > TOUCH['over'] and e['len'] >= TOUCH['least']:
                peak = TOUCH['per'] * math.log2(n / TOUCH['over'])
                e['expr'] = {**e.get('expr', {}), 'touch': 0}
                e['expr_path'] = {'touch': [round(peak * shape((i + 1) / pts), 2) for i in range(pts)]}
        if TOUCH['loudness'] is not None:
            doc['loudness'] = TOUCH['loudness']
    if not a.without_weight and not a.without_touch and not a.without_wheel and not a.without_horn and not a.without_string and not a.without_bell and not a.without_hand and not a.without_china and newest:
        if a.weight:
            WEIGHT.update(json.loads(a.weight))
        for name in WEIGHT['tracks']:
            t = next(t for t in doc['tracks'] if t['name'] == name)
            assert t['patch'].startswith('ct-twin') and isinstance(t['gain'], dict) and not t.get('fx'), (name, t['patch'], t['gain'])
            if WEIGHT['rig']:
                t['patch'] = t['patch'] + ' ' + WEIGHT['rig']
            if WEIGHT['eq']:
                t['fx'] = [{'type': 'eq', 'bands': list(WEIGHT['eq'])}]
            if WEIGHT['gain']:
                t['gain'] = {**t['gain'], 'value': f"{float(t['gain']['value'].rstrip('dB')) + WEIGHT['gain']:g}dB"}
        if WEIGHT['loudness'] is not None:
            doc['loudness'] = WEIGHT['loudness']
    if not a.without_speaker and not a.without_weight and not a.without_touch and not a.without_wheel and not a.without_horn and not a.without_string and not a.without_bell and not a.without_hand and not a.without_china and newest:
        if a.speaker:
            SPEAKER.update(json.loads(a.speaker))
        for name, cone in zip(SPEAKER['tracks'], SPEAKER['cones']):
            t = next(t for t in doc['tracks'] if t['name'] == name)
            assert t['patch'].startswith('ct-wall-stop') and isinstance(t['gain'], dict), (name, t['patch'], t['gain'])
            t['patch'] = t['patch'] + ' ' + SPEAKER['rig']
            t['fx'] = [{'type': 'cab', 'model': '4x12-modern', 'mic': SPEAKER['mic'], 'distance': 0.15, 'cone': cone}] + ([{'type': 'eq', 'bands': list(SPEAKER['eq'])}] if SPEAKER['eq'] else [])
            if SPEAKER['gain']:
                t['gain'] = {**t['gain'], 'value': f"{float(t['gain']['value'].rstrip('dB')) + SPEAKER['gain']:g}dB"}
        if SPEAKER['loudness'] is not None:
            doc['loudness'] = SPEAKER['loudness']
    if not a.without_fitted and not a.without_speaker and not a.without_weight and not a.without_touch and not a.without_wheel and not a.without_horn and not a.without_string and not a.without_bell and not a.without_hand and not a.without_china and newest:
        if a.fitted:
            FITTED.update(json.loads(a.fitted))
        kick = next(t for t in doc['tracks'] if t['name'] == 'kick')
        assert kick['patch'] == 'ct-kit-so-far' and isinstance(kick['gain'], dict) and len(kick['fx']) == 1 and kick['fx'][0]['type'] == 'eq'
        if FITTED['kick']:
            kick['patch'] += ' ' + FITTED['kick']
        if FITTED['eq']:
            kick['fx'] = [{'type': 'eq', 'bands': list(FITTED['eq'])}]
        if FITTED['gain']:
            kick['gain'] = {**kick['gain'], 'value': f"{float(kick['gain']['value'].rstrip('dB')) + FITTED['gain']:g}dB"}
        if FITTED['chest']:
            semis, ms, fader = FITTED['chest']
            sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            drum = sharps.index(KIT['kick']['pitch'][:-1]) + 12 * (int(KIT['kick']['pitch'][-1]) + 1) + semis
            doc['patches']['sf-chest'] = {'extends': '808', 'synth': {'layers': ['sine'], 'pitch': {'value': 0, 'mod': []}, 'drive': 0, 'filters': [],
                                                                     'amp': {'a': '2ms', 'd': f'{ms:g}ms', 's': 0, 'r': '20ms', 'curve': 3}},
                                          'play': {'mono': False, 'glide': '0ms', 'gate': 1}}
            # the chest is as big as the number, as the drum is: it takes the kick's own lane
            doc['tracks'].append({'name': 'chest', 'patch': 'sf-chest', 'gain': {**kick['gain'], 'value': f'{fader:g}dB'}, 'pan': 0, 'auto': kick['auto'],
                                  'notes': [{'at': e['at'], 'len': 0.25, 'pitch': sharps[drum % 12] + str(drum // 12 - 1), 'vel': e['vel']} for e in kick['notes']]})
        if FITTED['loudness'] is not None:
            doc['loudness'] = FITTED['loudness']
        if not a.without_fifth:                                    # only on the whole song as v23 has it
            if a.fifth:
                FIFTH.update(json.loads(a.fifth))
            snare = next(t for t in doc['tracks'] if t['name'] == 'snare')
            assert 'kit.s.pitch=' not in snare['patch'] and isinstance(snare['gain'], str) and not snare.get('fx'), (snare['patch'], snare['gain'])
            snare['patch'] += ' kit.s.pitch=' + FIFTH['pitch'] + ''.join(f' kit.s.patch.{o}' for o in FIFTH['patch'].split())
            if FIFTH['eq']:
                snare['fx'] = [{'type': 'eq', 'bands': list(FIFTH['eq'])}]
            if FIFTH['gain']:
                snare['gain'] = f"{float(snare['gain'].rstrip('dB')) + FIFTH['gain']:g}dB"
            if FIFTH['loudness'] is not None:
                doc['loudness'] = FIFTH['loudness']
    if a.form:
        spb = 60 / BPM / SUB
        for k, at in marks:
            w = walk(k)
            print(f'{k:3d}  {at:5d}  bar {at // BAR + 1:3d}+{at % BAR:<2d} {at * spb:6.1f}s  {sum(w):4d} sixteenths  ' + ' '.join(map(str, w)))
        print(f'wheel {wheel:5d}  bar {wheel // BAR + 1}+{wheel % BAR}  {wheel * spb:6.1f}s ; last bar line {end} = bar {end // BAR + 1}, {end * spb:.1f}s')
    else:
        # Same line-oriented YAML as the other generators: JSON flow values, one track per line.
        a.out.write_text('\n'.join(k + ': ' + json.dumps(v) if k != 'tracks' else
                                   'tracks:\n' + '\n'.join('  - ' + json.dumps(t) for t in v) for k, v in doc.items()) + '\n')
