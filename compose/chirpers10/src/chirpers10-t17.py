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


def compose(lead_gain=-7.0, storeys=True, low_bus=True, kit=True, sized=True, body=True, tuned=True, memory=True, count=True, still=True, one=True, ceiling=True):
    low_bus = low_bus and storeys  # --without-storeys still gives v1
    sized = sized and kit and low_bus
    body = body and sized
    tuned = tuned and body
    memory = memory and tuned
    count = COUNT if count and memory else None
    still = STILL if still and count else {}                 # --without-count still gives v8
    one = ONE if one and count else None
    ceiling = CEILING if ceiling and one and still else None  # every older switch still gives what it gave
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
                g = trim + count['lift'].get(ph, 0)
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
        tracks += [{'name': 'count', 'patch': count['one'][0], 'gain': f"{count['one'][1]}dB", 'pan': 0, 'notes': one, 'fx': [{'type': 'eq', 'bands': count['eq']}]},
                   {'name': 'crowd', 'patch': count['five'][0], 'gain': f"{count['five'][1]}dB", 'pan': 0, 'notes': five, 'fx': [{'type': 'eq', 'bands': count['eq five']}]}]
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
    return doc, marks, wheel, end


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--lead-gain', type=float, default=-7.0, help="the ondes' track gain in dB")
    ap.add_argument('--form', action='store_true', help='print where each walk starts')
    ap.add_argument('--without-storeys', action='store_true', help='regenerate v1: 160 and 80 without the phrases of 80 and 40 under them')
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
    doc, marks, wheel, end = compose(a.lead_gain, not a.without_storeys, not a.without_low_bus, not a.without_kit and not a.without_low_bus and not a.without_storeys, not a.without_size, not a.without_body, not a.equal, not a.without_memory, not a.without_count, not a.without_still, not a.without_one, not a.without_ceiling)
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
