#!/usr/bin/env python3
"""chirpers10-t2 "Odd Sympathy" (chirper-zero): one riff and two clocks.

In 1665 Huygens hung two pendulum clocks from one beam and found that, however he started them, within half an hour they
swung exactly against each other; he called it "an odd kind of sympathy". This is that, for two guitars.

Common Time (track 1) keeps one pulse and turns three cells of different lengths under it. This piece is the other way
round: ONE cell, one bar long, on two guitars, left and right, each with its own clock. They start in step. The right
guitar's clock runs a hair fast: it slips ahead of the left by a sixteenth, holds there, slips again, and so on, each
hold a canon of the riff with itself at a new distance, until it is half a bar ahead: exactly against the left. The riff
is written so that there, and only there, the two halves fit: every sixteenth of the bar has one guitar on it and never
both (the riff's second half is the negative of its first). What was a riff with holes is a machine with none.

The slips are the engine's track `warp` (the right-hand tracks' own clock against the song's); nothing is shifted by hand.

v1 is the SKELETON (Harry, 14 Nov: "should skeleton it and then climb both"): the whole shape standing, bare.
"""
import json
import math
import os

OUT = os.environ.get("C10T2_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t2.yaml"))
BPM = 108
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# THE RIFF: sixteen sixteenths. (position, length, kind): c a palm-muted chug on the open low string, o the string open,
# h a hook note. Its attacks are 0 1 3 6 | 10 12 13 15: of every pair of sixteenths half a bar apart exactly one is struck.
# Every note is short and the gaps are real rests (a riff with holes): the piece is about what fills them.
RIFF = [(0, 1, "c"), (1, 1, "c"), (3, 2, "o"), (6, 2, "h0"), (10, 1.5, "h1"), (12, 1, "c"), (13, 1, "c"), (15, 1, "h2")]
ATTACKS = [p for p, _, _ in RIFF]
assert all((p in ATTACKS) != ((p + 8) % 16 in ATTACKS) for p in range(16)), "the two halves must be each other's negative"
# the hook's notes are three of Common Time's four (Ab Gb B C over F): the tritone, the minor third, the fifth
HOOK = [F1 + 6, F1 + 3, F1 + 7]
CHUGS = [p for p, _, k in RIFF if k == "c"]

# THE FORM, in bars (4/4). The right guitar's lead over the left, in sixteenths, at each station.
FORM = [
    ("one clock", 0, 8, 0),          # the left guitar alone and a pendulum; the bass and kick join
    ("in step", 8, 24, 0),           # both, together
    ("slip", 24, 28, None),
    ("a sixteenth", 28, 32, 1),
    ("slip", 32, 36, None),
    ("an eighth", 36, 48, 2),
    ("slip", 48, 50, None),
    ("three", 50, 56, 3),
    ("slip", 56, 58, None),
    ("a quarter", 58, 74, 4),
    ("let go", 74, 98, None),        # no beam: clean guitars, the right one drifting all the way to half a bar
    ("against", 98, 122, 8),         # exactly against each other: the bar is full
    ("two clocks", 122, 130, 8),     # the guitars alone, then the ticks
]
NB = 130
# the right-hand clock (track `warp`): stretches in turn from the start; `to` is its shift in beats, negative = ahead
WARP = [
    {"over": "96b", "to": 0},
    {"over": "16b", "to": -0.25, "curve": "smooth"}, {"over": "16b", "to": -0.25},
    {"over": "16b", "to": -0.5, "curve": "smooth"}, {"over": "48b", "to": -0.5},
    {"over": "8b", "to": -0.75, "curve": "smooth"}, {"over": "24b", "to": -0.75},
    {"over": "8b", "to": -1.0, "curve": "smooth"}, {"over": "64b", "to": -1.0},
    {"over": "88b", "to": -2.0, "curve": "linear"},          # bars 74-96: the long drift, a little over 1% fast
]

# v2: THE DRIFT GETS A SHAPE (bars 74-98; the window the section map called static). Three things, "" = v1:
# (1) the ground moves under the drifting ticks, a step at a time: F, Eb, Db, then C, the dominant, held until the band
#     comes back on F. The clocks arrive against each other ON the dominant and resolve with the band.
# (2) the pendulum lets go too. From bar 80 its tick-tock is a Risset rhythm (the engine's track `risset`, two copies an
#     octave of tempo apart, a cycle of four bars): it speeds up for ever and is never faster. On each fourth bar line the
#     tick is back on the bar, at the speed it started; at bar 96, where the guitars lock, the plain pendulum has it again.
# (3) the last six bars build: a dominant pedal on the bass, the kick on one and three, floor tom into the fill.
DRIFT = os.environ.get("C10T2_DRIFT", "0,-2,-4,-5;16:2;0.5")       # the roots' semitones ; risset cycle beats : layers ; pedal velocity
# v3: THE TWINS (palette round). The piece is one riff on two clocks, so the two guitars are ONE guitar twice: the library
# patch `ct-twin` on both sides (Common Time's rigs are a different amp a side), each with its own cone. It is dry: no
# plate, no eq after the cabinet, a gate; a rest is silence, so a canon of the riff with itself takes turns. What the two
# share is a small room on their bus, the beam the two clocks hang from.
# patch : left cone : right cone : track gain dB ; the room's kind : decay : mix ; master make-up dB. "" = v2 (Common
# Time's tight rig). The guitars sit 0.8 dB lower than v2's (alone, LUFS): the mix read 2 to 3 dB over the records at
# 2-4 kHz in every heavy window, and that band is the guitars'. The master makes up what the mix lost.
TWIN = os.environ.get("C10T2_TWIN", "ct-twin:4:5:3.2;room:0.35s:0.06;0.5")
# v4: THE HOLD AN EIGHTH APART (bars 36-48; the section map's "static" window). Until now every hold was the same riff
# on F with a different kick. At an eighth apart the canon does something no other distance does: the right guitar plays
# each hook note and the left answers it an eighth later (4 and 6, 8 and 10, 13 and 15). So this hold is built on the
# eighth, and on a ground of its own:
# (1) it moves to Ab, the hook's minor third: the first time the ground moves under the heavy guitars. The right guitar,
#     being ahead, gets there an eighth before the bar line.
# (2) the snare answers itself an eighth later too (a ghost stroke after each backbeat), the hat plays eighths, a china
#     marks the bar line.
# (3) the bass plays BOTH guitars' notes: the one line the two make at this distance.
# Two mix tries were measured and NOT taken (fields four and five, off by default): the bass track up 1.2 dB over the
# hold (on Ab the mix reads 1.6 dB under the records at 120-250 Hz) moved nothing, because the bass's bus compressor
# takes it back; and a 13 kHz low-pass on the hat cost the top it had just gained (8-16 kHz -0.1 -> -0.8).
# the root's semitones above F ; the ghost's velocity ; the china's velocity [; the bass's dB there ; the hat's low-pass Hz]. "" = v3.
EIGHTH = os.environ.get("C10T2_EIGHTH", "3;0.45;0.5")
# v5: TWO VOICES (whole-song round). The piece had no voice and no tune: a riff and its canon. It gets the same idea in
# speech: two voices, left and right, twins like the guitars, saying the same four lines, a syllable to each attack of
# the riff. The right voice is on the right guitar's clock (the same `warp`), so nothing is placed by hand:
#   in step (0:36)            the four lines SPOKEN (voice-talk), the two voices together: one voice
#   a quarter apart (2:13)    the four lines again, spoken, the right voice a beat ahead: each syllable said twice
#   against (3:46)            the last line only, BARKED (Common Time's bark), over and over: half a bar apart the two
#                             voices' syllables interlock as the guitars' notes do, sixteen to the bar, alternating sides
#   I cannot hear you through the wall / only the floor between us moves / whatever way you lean I lean /
#   against you until we agree
# (two clocks on one beam, from the inside; Huygens is not named.) Spoken first, because a recogniser reads the spoken
# voice 18 words of 24 on this rhythm and the bark 14: the words are learnt spoken, then barked.
# the talk's gain ; the bark's gain ; pan ; the bark's hall send ; dB the guitars' bus ducks under the talk. "" = v4.
VOICE = os.environ.get("C10T2_VOICE", "-6dB;3dB;0.5;-18dB;2")
# The spoken voice's eq. A clean male voice has a body the records' harsh voices do not (110 Hz and its harmonics up to
# the first formant): with Common Time's eq (hp 120, 300 Hz -6) the voiced holds read 7 dB over the records' voiced
# passages at 250-500 Hz; a high-pass alone (220, 450, 650 Hz) left 3 to 5 and cost words; this notch leaves 2 to 3
# and the recogniser reads as many words as before (18 of 24).
TALKEQ_V5 = "hp cutoff=300|peak cutoff=400 q=1 gain=-12dB"
TALKFX = os.environ.get("C10T2_TALKFX", "")
VOICE_LINES = [      # syllables (ARPAbet, from `chirp tts --print`); "up" = the line starts on the sixteenth before the bar line
    ("AY1|K AE1|N AA0 T|HH IY1 R|Y UW1|TH R UW1|DH AH0|W AO1 L", "up"),
    ("OW1 N|L IY0|DH AH0|F L AO1 R|B IH0|T W IY1 N|AH1 S|M UW1 V Z", os.environ.get("C10T2_L2", "down")),
    ("W AH2|T EH1|V ER0|W EY1|Y UW1|L IY1 N|AY1|L IY1 N", "up"),
    ("AH0|G EH1 N S T|Y UW1|AH0 N|T IH1 L|W IY1|AH0|G R IY1", "up"),
]
# v5 also: THE KIT'S TOP FALLS AS THE RECORDS' DOES (chirp-eco's reading by thirds: level with the records to 11.6 kHz,
# then ours stayed flat where theirs fall: +1.6 dB at 11.6-13.7 kHz, +4.7 at 13.7-16, +7.4 at 16-20; every piece of the
# kit carried it). A low-pass on the drums' bus and the overheads': Hz ; q. "" = v4.
DTOP = os.environ.get("C10T2_DTOP", "14250;0.8")     # v7: Common Time's fit (v5-v6 had 14500;0.7, which took 1.4 dB at 11.6-13.7 kHz that was not owed)
# v7: THE WORDS ARE HEARD (whole-song round). chirp-eco read v5's spoken holds with a recogniser IN THE MIX: 5 words of
# 24 in both (14 and 10 with the voices alone), and each voice 2 to 3 dB under the records' voices and near the mix a
# third as often. Three changes:
#   1. IN STEP THERE IS ONE VOICE, in the middle (track `tc`). Two tracks of one voice in unison smeared each other (14
#      words against 18 for one alone), and when the clocks agree there is one voice: it splits in two only when they part.
#   2. A QUARTER APART the two voices stand further apart (the pan below), so each ear has its own.
#   3. THE GUITARS BREATHE WITH THE SPEECH: a `pump` on the guitars' bus keyed from the voices' NOTES (not their sound, so
#      it is down by the syllable's first consonant, which a sidechain duck with a 20 ms attack never was), in place of
#      v5's 2 dB duck.
#      Under the one voice the guitars fall 5 dB at each syllable; under the two, 2.5 dB for each (two pumps, so 5 where
#      their syllables overlap: at 5 dB each the guitars were down nearly all the time and the hold lost its middle).
#   4. THE VOICE IS RE-VOICED. Measured alone, v5's spoken voice had most of its energy under 1 kHz and 11 to 12 dB less
#      at 1-4 kHz, where words are told apart and where the guitars are loudest: in the hold a quarter apart the two
#      voices WERE the mix's 250-500 Hz (2 dB under the whole band; the guitars 7 under), which is why that band read
#      4.5 dB over the records. Now a steep high-pass at 500 Hz and 8 dB more around 2.5 kHz: for the same level the
#      voice has 4 dB less at 250-500 Hz and 4 to 5 dB more at 1-4 kHz, and no more top. It costs words alone (the
#      recogniser reads 15 of 24, was 18). An 8 dB shelf above 1.2 kHz kept all 18 but put the holds' 4-8 kHz 2 dB
#      over the records; not taken.
# the centre voice's gain ; the two voices' gain ; their pan ; the pump's depth dB under the one voice : hold : release ;
# its depth under each of the two. "" = v6.
#      (Measured on the guitars alone, pumped against not: the engine starts a spoken syllable about 80 ms before its
#      written time, so that its vowel lands on the beat, and the pump falls with that start. A 90 ms hold had the
#      guitars back up 120 ms after the beat with the syllable sounding for another 120; the hold is now 250 ms.)
HEARD = os.environ.get("C10T2_HEARD", "-6.8dB;-4.5dB;0.8;5:250ms:100ms;2.5")
# v13: THE MIX AGAINST THE RECORDS, BY PART (whole-song round). Three of the four holds read against the eleven records
# were 1.5 to 1.9 dB over at 2-4 kHz and 0.9 to 1.6 over at 4-8 kHz, since v3, and the two with the china 1.1 and 1.5
# over at 8-16 kHz. Read part by part (each part alone against the mix, band by band, in step with no voice): the
# GUITARS are 78% of the mix's 2-4 kHz; the CYMBALS are 47% of 4-8 kHz and 85% of 8-16 kHz (the guitars 21% of 4-8).
#   1. The guitars' cabinet microphone moves off the cone's centre (mic 0.4 -> this). Benched on the two guitars alone:
#      nothing changes under 1 kHz, -0.1 dB at 1-2 kHz, -1.2 at 2-4 kHz, -1.9 at 4-8 kHz (0.6 gives -2.7 and -3.8: too
#      much for the hold an eighth apart, which is not over).
#   2. The cymbals' track comes down by this many dB (the china and the crashes).
#   3. The spoken voice's lift at 2.5 kHz is this many dB (was 8): it sits on the same band.
#   4. The master makes up what the guitars' loudness loses.
# the cabinet's mic ; the cymbals' trim, dB ; the voice's lift at 2.5 kHz, dB ; the master's make-up, dB. "" = v12.
MIX = os.environ.get("C10T2_MIX", "0.5;-1.5;6;0.55")
TALKEQ = os.environ.get("C10T2_TALKEQ", f"hp cutoff=500|hp cutoff=500|peak cutoff=2500 q=0.8 gain={MIX.split(';')[2] if MIX else 8}dB" if HEARD else TALKEQ_V5)
# Tried in the same round and NOT taken: the speech moved into the riff's holes (the same rhythm half a bar late falls
# exactly in the riff's gaps, C10T2_HOLES=8). It should have been easier to hear; nothing I can measure says so: the
# recogniser on the full mix read 10 and 8 words on the attacks against 7 and 11 in the holes (two seeds; base.en 5 and 7
# against 4 and 10), and the voice against the mix read the same (-5.4 and -5.6 dB). So the syllables stay on the riff.
HOLES = int(os.environ.get("C10T2_HOLES", "") or 0)
# Tried in the same round and NOT taken: the quarter hold on C (C10T2_QUARTER=7), which would have made the hook's three
# notes the grounds in rising order (Ab, B, C). Rendered and scored: the form's "returns" fell (compscore 98.84 / 99.60
# without it, 97.53 / 98.62 with), and it is right that they did. The song has three PILLARS, the simple distances
# (together, a beat apart, half a bar apart), and they say the same words over the same riff: they must stand on the
# same ground (F) for the distance to be the only thing that changed. The ODD distances (one, two, three sixteenths)
# are the excursions and take the hook's notes: Ab and B so far; the hold a sixteenth apart is still on F and can take C.
QROOT = int(os.environ.get("C10T2_QUARTER", "") or 0)
# v6: THE HOLD THREE SIXTEENTHS APART (bars 50-56, and the slip into it from bar 48). At this distance the two guitars
# strike TOGETHER five times a bar, more than at any other (sixteenths 0, 3, 10, 12, 13), and three of those are two
# different notes: the riff makes chords with itself (a tritone, a minor third, a fifth). So this hold is built on the
# hits: the band stops keeping time and strikes only where the guitars strike together (kick on all five, snare on the
# two chords at 3 and 10, china on the bar line, the bass on the five and resting between), while the two dry guitars
# play the whole riff through the gaps and the pendulum ticks under them. It stands on B, the hook's tritone: the second
# of the hook's notes to become a ground (Ab at an eighth, B here).
# the root's semitones above F ; the pendulum's velocity. "" = v5.
THREE = os.environ.get("C10T2_THREE", "6;0.42")
# v20: THE HOLD ON B ENDS IN PLAIN AGREEMENT (section round, 1:51-2:04). Harry on this hold: "The band agreeing; it
# builds". It did not yet build: its six bars were six times the same bar. Now it has a shape:
#   bars 50-52  as it was: the band strikes only the five places a bar where the two guitars strike together, and the
#               guitars play the whole riff through the gaps;
#   bars 52-55  the china joins the snare on the two places where the guitars make a chord with each other;
#   bar 55      the last bar: the GUITARS TOO play only where they agree. Five stabs from the whole band and silence
#               between them: a unison, a tritone, a minor third, a fifth (the chords the riff makes with itself
#               three sixteenths apart, heard with nothing else) and a last one where the right guitar, being ahead,
#               is already on the F the song goes to next; the china on every one. Then the right guitar starts to
#               slide again.
# So the hold says what it is about in its last bar, plainly.
# the bar the china joins the snare ; its velocity ; the bar of plain agreement ; the china's velocity in it. "" = v19.
AGREE = os.environ.get("C10T2_AGREE", "52;0.6;55;0.7") if THREE else ""
# v8: THE HOLD A SIXTEENTH APART (bars 28-32, 1:02-1:11) gets what only that distance has, and the last of the hook's
# notes as its ground. A sixteenth apart is as close as the two guitars come without being together: every note has a
# shadow a sixteenth before it, and between them they strike thirteen of the bar's sixteen sixteenths (only 4, 7 and 8
# are left). So here the band plays the UNION: the kick and the bass on every note of either guitar, and the drummer
# fills the three holes (a tom, the floor tom, the snare), so that for four bars every sixteenth of the bar is struck.
# The three odd distances now each show one thing: a sixteenth apart everything either guitar plays (the densest four
# bars before the end), an eighth apart the echo, three sixteenths apart only what they play together (the sparsest).
# It stands on C, the hook's third note: C a sixteenth apart, Ab an eighth, B three sixteenths; the song's three simple
# distances stay on F.
# the root's semitones above F ; the two toms' velocity ; the kick's velocity off the beat. "" = v7.
ONE = os.environ.get("C10T2_ONE", "7;0.8;0.8")
# v29, a fill with its rests played by the band. The two guitar clocks leave
# three shared holes a bar on C. The drummer carries a FOUR-stroke descent
# across those holes without resetting at the bar line. Empty restores v28.
HOLE_FILL = os.environ.get("C10T2_HOLE_FILL", "1")
# On C, with the kick and the bass on thirteen sixteenths of a bar, the hold read 1.4 dB over the records at 60-120 Hz
# (the bass's C2 is 65 Hz; on F its fundamental is under 60). The bass bus's fader comes down there, after its
# compressor (a gain on the bass track is taken back by the compressor). bar:bar:dB, ... "" = no ride.
LOWRIDE = os.environ.get("C10T2_LOWRIDE", "28:32:1.5" if ONE else "")        # v8-v16: 28:32:-1.5
# v9: THE OPENING (0:00-0:35) gets two things of its own.
#   1. For the first eight bars the right side was empty: one guitar hard left for eighteen seconds. From the bar the
#      bass and the kick come in, the right guitar plays the riff's CHUGS only (the same four sixteenths the kick is on):
#      the riff's skeleton arrives on the right, and the whole riff, with its hook, at 0:18. One clock; then the other
#      is heard starting.
#   2. The band STOPS for the last beat before the voice (0:35), and the voice's first word, "I", falls in the gap; the
#      band comes back on "cannot". The first word of the song is heard alone.
# the bar the right guitar's chugs join ; the first silent sixteenth of the bar before the voice. "" = v8.
OPEN = os.environ.get("C10T2_OPEN", "4;12")
# v10: THE SNARE'S CRACK (whole song; Common Time's v41 mend, the same fault). The snare went to the drums' bus, which is
# clipped, AND into the cymbals' room at -1.5 dB, which is not: its peak and half its loudness reached the mix through
# a bright 0.7 s room. Now it is nearly out of that room and a dry, unclipped bus beside the drums carries its crack.
# Here the snare was already the loudest track, and without its room the full sections read 0.3 to 0.5 dB quieter on the
# groove: so its track is at 6.5 dB (Common Time's is 7) and the master makes up 0.3 dB.
# the track's shelf (shelf:Hz:dB) ; its send to the cymbals' room, dB ; its gain ; dry : the send to the dry bus, dB ;
# the master's make-up, dB. "" = v9.
# v14: THE SNARE STEPS BACK (whole song), from the first true reading of this song's mix. Until today the reader
# (stembal) had frames that sat on this song's beat (108 bpm is 2.99 frames a beat) and misread its short holds by up
# to 2.6 dB; chirp-eco found and mended it, and read every hold part by part. The snare, the loudest track in every
# hold, holds most of 8-16 kHz in four of the six holds (58 to 72%) and most of 4-8 kHz in four; those bands read up
# to 2.7 and 1.3 dB over the records. Its track comes down 1.25 dB (6.5 -> 5.25) and its shelf above 7 kHz goes from
# 2 to 3 dB. (v10 to v13: "shelf:7000:-2;-12;6.5dB;dry:-10;0.3".)
SNARE = os.environ.get("C10T2_SNARE", "shelf:7000:-3;-1.5;3.5dB;dry:-10;0.3")      # v14-v16: shelf:7000:-3;-12;5.25dB;dry:-10;0.3
# v14: and the guitars hold most of 250-500 Hz, which reads 1.1 to 2.2 dB over the records in ALL six holds: one narrow
# cut on the guitars' bus (Hz : q : dB). Predicted on the two guitars alone (eqpred.py): about -1.7 dB at 250-500 Hz,
# -0.5 at 120-250 Hz and -0.4 at 500 Hz-1 kHz. "" = none (v13).
GBODY = os.environ.get("C10T2_GBODY", "330:1.2:-2")
# the master's make-up for the two, dB
V14_MAKEUP = float(os.environ.get("C10T2_V14MAKEUP", "0.15") or 0) if (GBODY or SNARE.split(";")[2:3] == ["5.25dB"]) else 0.0
SNARE_EQ = os.environ.get("C10T2_SNAREEQ", "300:0.7:-12")        # the dry bus's eq (Hz : q : dB)
# v10: TWO CLOCKS AT THE END (section round, 4:31-4:50). The song is named after two pendulum clocks that settled in
# opposition, and it ended with the guitars against each other but ONE pendulum (a ride bell). Now there are two clocks,
# left and right, one tick-tock each to the bar (a wooden tick on C, a tock on F a fifth below: the song's two poles),
# and they are in opposition: the left clock's tick is the right clock's tock. They start under the two guitars' last
# four bars and are left ticking with the clean guitars; the last sound of the song is one more swing.
# The sound is a drum machine's rim-shot circuit (`machine`, part rim; the album's first use of that source).
# gain ; pan ; tick's velocity : tock's ; hall send. "" = v9 (the ride-bell pendulum).
CLOCKS = os.environ.get("C10T2_CLOCKS", "-6dB;0.7;0.8:0.7;-12dB")
# v11: THE LETTING GO (section round, 2:40-2:53). At 2:44 the band simply stopped and the clean guitars began: the
# song's one hinge had no gesture. Now the hold a beat apart ends on a tom fill, and on the bar line the band strikes
# once more (a crash, the kick) and the guitars and the bass HOLD the open low F and let it die over the first bars
# of the drift, under the clean guitars' first ticks. Each guitar's last note is written on the bar line; the right one
# is on its own clock, a beat ahead, so it lets go a beat before the left: the last thing the canon does.
# how long the last note is written, in beats ; dB the guitars' bus has fallen ; over how many bars ; the bass's fall, dB.
# "" = v10.
LETGO = os.environ.get("C10T2_LETGO", "12;30;3.5;24")
# v12: THE LOCK IS HEARD BEFORE IT LANDS (section round, 3:29-3:38; the window 3:33-4:08). Two things in the build
# to the arrival against each other:
#   1. The right guitar's clock reaches half a bar ahead at bar 96, two bars before the band lands. From there the two
#      HEAVY guitars come back playing the riff's chugs only (as the right one did in the opening): half a bar apart
#      there is a chug pair on every beat, the sides taking turns in twos (left on one, right on two and three, left
#      on four). The skeleton locks first, rising; at the bar line the whole riff, the bass on F and the drums land,
#      and the hook's notes fill what was left.
#   2. The bass's pedal on C under the build was written to swell (its notes harder bar by bar) and its compressor had
#      all of it: alone it read -26.8 dB in every bar. Now the bass's bus rises under it.
# This needs the letting go's lanes (LETGO).
# the bar the chugs come in ; the guitars' bus there, dB : just before the landing ; the bass's bus at bar 92, dB. "" = v11.
LOCK = os.environ.get("C10T2_LOCK", "96;-9:-3;-10") if os.environ.get("C10T2_LETGO", "x") else ""
LOCK_BAR = int(LOCK.split(";")[0]) if LOCK else 96
# v15: TWO MUSIC BOXES (palette round). When the band lets go, what ticks on through the drift was two clean guitars:
# Common Time's clean guitar, the same players with the gain off. The song is about two clocks, and its drift is its
# quiet middle, fifty-three seconds of one riff on two identical instruments sliding apart. Now those two are MUSIC
# BOXES (the library's `music-box`, which no other track on the album uses): clockwork, a comb of steel tines, left and
# right, the right one on its own clock as before. They play the riff two octaves above where the guitars ticked it
# (a music box has no low notes), through the same dripping spring. They are also what is left at the very end, with
# the two clocks. The clean guitars leave the song.
# the patch ; semitones above the heavy riff ; gain ; pan ; hall send ; the dripping spring's mix (0 = none). "" = v14.
BOX = os.environ.get("C10T2_BOX", "music-box;48;-9dB;0.7;-9dB;0.22")        # v15-v16: -11dB
# v17: HARRY'S ANSWERS (whole song). On 14 Nov, 16:12-16:34 GMT, Harry answered the Questions page; five of his answers
# say something here is wrong, and each is acted on (his words in quotes):
#   1. THE SNARE, "Too dry": v10 took the snare out of the cymbals' room (its send to `oh` -1.5 -> -12 dB) because that
#      send is a path round the drums' clip. His ear says that path was the snare's air. The send is back at -1.5 dB;
#      the dry path beside it (the crack) stays, and the track comes down to keep the snare where v14 put it
#      (C10T2_SNARE's second and third fields).
#   2. THE HOLD ON C, "more bass": the bass's bus was 1.5 dB DOWN there (v8, a reading of the low end against the
#      records). It is 1.5 dB up now: 3 dB more bass (C10T2_LOWRIDE).
#   3. THE BUILD TO THE LANDING, "It gives the landing away": v12 brought the heavy guitars' chugs back two bars early.
#      They are out again: the guitars stay silent until the band lands at 3:38. The bass's swell under the build
#      stays (C10T2_EARLY: "1" = the early chugs).
#   4. THE PENDULUM IN THE DRIFT, "doesnt work at this tempo on this kit piece": the ride bell's ever-speeding tick is
#      out of the drift. It was also the loudest thing there, 5 dB over the two music boxes he kept ("Music boxes:
#      keep them"); the drift is theirs now, 2 dB up (C10T2_PEND: "1" = the pendulum; the boxes' gain is BOX's third).
#   5. THE ENDING, "Sounds like a click track": the two wooden clocks are gone. The song ends on the two music boxes,
#      half a bar apart, RUNNING DOWN as a music box does when its spring is spent: two bars in time, then every note
#      later than the last, and one last F from each, the right box's first (C10T2_END: bars in time ; how many times
#      slower the last note is than the first, less one ; the boxes' velocity ; the song's length in beats).
# Each "" (or the older value) gives v16.
EARLY = os.environ.get("C10T2_EARLY", "")
PEND = os.environ.get("C10T2_PEND", "")
END = os.environ.get("C10T2_END", "2;2.0;0.45;532")
if END:
    CLOCKS = ""
# v18: A PULSE UNDER THE DRIFT, AND THE LOCK IS SHAKEN (two more of Harry's answers; his words in quotes).
#   1. THE DRIFT, "It wants a pulse there" (after v17 took the pendulum out). Two bars after the band lets go, a
#      HEARTBEAT comes in under the two music boxes and stays to the landing: the bass in soft eighths on the ground
#      as it steps down (F, E flat, D flat, C), a closed hat on the quarters (eighths from 3:11) and a soft kick on
#      the bar line. It keeps the LEFT box's time, so the right box is heard to slide against something. The bass's
#      swell into the landing is this pulse rising (it was held notes).
#      the bar the pulse comes in ; the bass's bus there, dB ; at bar 92, dB ; the kick's velocity ; the hat's. "" = v17.
#   2. THE SLIP, "A thrill" and "add". One more, where the song had none: in the last section, with the two guitars
#      locked half a bar apart, the right one is SHAKEN: it runs two sixteenths further ahead over two bars and falls
#      back over the next two (the engine's `warp` again; nothing moved by hand), the beat thinned to a kick and a hat
#      as in the other slips, and the lock holds: a crash, and the last barks. Huygens's clocks did this when he
#      disturbed them.
#      the bar it starts ; bars out (and as many back) ; the right clock's shift at its furthest, beats. "" = v17.
#      v27 (Harry: "Too much: it buries the boxes"): 78;-18;-15;0.07;0.3. v18-v26: 78;-13;-10;0.28;0.55.
PULSE = os.environ.get("C10T2_PULSE", "78;-18;-15;0.07;0.3") if DRIFT and os.environ.get("C10T2_LETGO", "x") else ""
SHAKE = os.environ.get("C10T2_SHAKE", "106;2;-2.5")
if SHAKE:
    _sb, _sn, _far = int(SHAKE.split(";")[0]), int(SHAKE.split(";")[1]), float(SHAKE.split(";")[2])
    WARP = WARP + [{"over": f"{(_sb - 96) * 4}b", "to": -2.0}, {"over": f"{_sn * 4}b", "to": _far, "curve": "smooth"}, {"over": f"{_sn * 4}b", "to": -2.0, "curve": "smooth"}]
TICKS = ("ml", "mr") if BOX else ("cl", "cr")
TICK_UP = int(BOX.split(";")[1]) if BOX else 24
# v16: THE ECHO, HEARD NAKED (section round, 1:33-1:38; the window 1:11-1:46, "static"). The hold an eighth apart is
# the longest of the odd holds, twelve bars of one beat, and what only this distance has is the echo: every note of the
# right guitar is answered by the left an eighth later. For two bars in its middle the bass and the drums stop and the
# two dry guitars are alone, hard left and right, so the echo is heard as an echo; then a crash and the beat again.
# first bar : the bar the band comes back. "" = v15.
NAKED = os.environ.get("C10T2_NAKED", "42:44")
T = {}


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def riff(tr, b0, b1, vel=0.85, up=0, clean=False, ramp=None, root=0, only=None):
    """The riff on a track, bars b0..b1. Heavy: chugs muted (`root` semitones above F). Clean (`up` semitones higher):
    every note a short tick. `only`: just the notes at these sixteenths."""
    up = up + root
    for b in range(b0, b1):
        v = vel * (ramp[0] + (ramp[1] - ramp[0]) * (b - b0) / max(1, b1 - b0 - 1)) if ramp else vel
        for p, ln, kind in RIFF:
            if only is not None and p not in only:
                continue
            t = b * 16 + p
            if kind == "c":
                if clean:
                    add(tr, t, 1, F1 + up, v * 0.8)
                else:
                    add(tr, t, ln, F1 + root, v * (1.0 if p in (0, 12) else 0.9), pm=1)
            elif kind == "o":
                add(tr, t, 1 if clean else ln, F1 + up + (12 if clean else 0), v)
            else:
                add(tr, t, 2 if clean else ln, HOOK[int(kind[1])] + up, v * 1.05)


def bass(b0, b1, lead=0, vel=0.9, root=0, union=False, only=None):
    """The bass keeps the LEFT clock; where the right guitar is locked `lead` sixteenths ahead it takes its chugs too
    (`union`: every note of the right guitar's that the left has not, so the bass plays the two guitars' one line;
    `only`: just the left guitar's notes at these sixteenths)."""
    for b in range(b0, b1):
        seen = set()
        for p, ln, kind in RIFF:
            if only is not None and p not in only:
                continue
            add("bass", b * 16 + p, ln, root + (F1 if kind in "co" else HOOK[int(kind[1])]), vel)
            seen.add(p)
        if only is not None:
            continue
        if lead:
            for p, ln, kind in RIFF:
                q = (p - lead) % 16
                if q not in seen and (kind == "c" or union):
                    add("bass", b * 16 + q, 1, root + (F1 if kind in "co" else HOOK[int(kind[1])]), vel * 0.85)


# v19: THE VOICE IN TUNE, AND IN THE BAND (section round, 0:36-0:53: the four lines where the two clocks are in step).
# Harry, on the Questions page, of the spoken words: "yes but needs to be more realistic and in some kindof tune", and
# of how they sit: "On top, like a voice-over". Both were true by construction: the voice SPOKE on one pitch (a
# speaking pitch, not a note of the song), thinned to a telephone band, dry, with the guitars pumped 5 dB out of its
# way at every syllable. Here, in the first of its two passages:
#   1. IN TUNE. Each syllable already falls on an attack of the riff; now it is SUNG on that attack's note, two octaves
#      above the guitars: F F F B A-flat F F C, the riff itself (the three lines that start before the bar start on
#      the riff's last note, C). Benched alone, the same voice sung on these notes read as many words as spoken
#      (20 of 24 for 19).
#   2. IN THE BAND. It goes through the guitars' own room and a little of the hall; the guitars duck 2 dB under it,
#      not 5; and its level is set by presence against the band to where the eleven records' voices sit (-9.1 dB),
#      not over it (it was -6.3, the second loudest thing after the snare).
#      (Tried and not kept: opening its telephone band, a high-pass at 300 Hz for the two at 500. This voice's weight
#      is all at 250-1000 Hz, and sung at F3-C4 it put the voiced bars' 250-500 Hz 6.3 dB over the records, from 1.1.
#      So the band stays as v7 fitted it.)
#   3. DOUBLED. A second singer (`voice-hook`, another of the library's voices) sings the same line quietly on each
#      side: a voice with others behind it, as a band's singer has.
# The second spoken passage (2:13, the two voices a beat apart) is left as it was, on purpose, so the two can be heard
# against each other in the song until Harry says which.
# the MIDI note the riff's F is sung on ; the voice's gain ; the pump under it, dB ; its room (kind:decay:mix) ; its hall
# send ; the doubles (patch:gain:pan, or "") ; its eq. "" = v18.
SUNG = os.environ.get("C10T2_SUNG", "53;-10dB;2;room:0.35s:0.15;-16dB;voice-hook:-9.5dB:0.6;hp cutoff=500|hp cutoff=500|peak cutoff=2500 q=0.8 gain=6dB")
RIFF_NOTE = {0: 0, 1: 0, 3: 0, 6: 6, 10: 3, 12: 0, 13: 0, 15: 7, -1: 7}      # the riff's note at each of its attacks, semitones over F
# v27: HARRY'S THREE ANSWERS (17 Nov 00:25; his words in quotes).
#   1. "2: sung, in the band. Do the lines at 2:13 too". The second passage (the hold a quarter apart, the two voices a
#      beat apart, left spoken since v19 so that he could hear the two against each other) is SUNG now, the same way:
#      each voice on the riff's own notes at the riff's attacks, in the first passage's eq and room. The right voice is
#      the left a beat late, as the right guitar is: so the words come as a ROUND at the quarter, on the riff.
#      each of the two voices' gain ; their hall send. "" = v26 (spoken).
#      Benched by part against the first passage: the one centre voice there sits 9.2 dB under the mix and is half of
#      500 Hz-1 kHz; the two here sit 11.7 and 12.2 under (8.9 together) and together are as much of that band (-2.6
#      against -2.9). Spoken they were 9.6 and 9.8 under: on top, which is what he had turned down.
#   2. THE DRIFT'S PULSE, "Too much: it buries the boxes". It does: read stroke by stroke, the pulse's kick was 1 dB OVER
#      the music boxes' strokes and its hat 1 dB under them, and the hat was the whole of the mix from 4 kHz up. The
#      pulse stays (he asked for one) and goes UNDER: the bass 5 dB down until the swell into the landing, the kick's
#      velocity a quarter of what it was, the hat's about half (C10T2_PULSE, below).
#   3. THE HOLD ON C, "With its tone back: do it". The bass's three eq bands follow the ground there too, as on A flat
#      and B since v23 (C10T2_KEYEQ, below): its body and growl back, in place of fundamental.
SUNG2 = os.environ.get("C10T2_SUNG2", "-8dB;-16dB") if SUNG else ""


def say(line, bar, kind="talk", ring=True, one=False):
    """One line on both voices of a kind (spoken `tl`/`tr`, barked `vl`/`vr`): a syllable to each attack of the riff,
    none longer than two sixteenths and a bit (short syllables read better, and take turns better)."""
    phs, how = VOICE_LINES[line]
    pos = ATTACKS if how == "down" else [-1] + ATTACKS[:-1]
    for i, ph in enumerate(phs.split("|")):
        ln = (pos[i + 1] - pos[i]) if i < 7 else (6 if ring else (1 if how == "down" else 2))
        ln = min(ln, 2.2) if not (i == 7 and ring) else ln
        pitch = nm(65) if kind == "bark" else ("m41.5" if i == 7 else "m45.5")       # the talk falls at the end of a line
        sung = SUNG and (one or SUNG2) and kind == "talk"
        if sung:
            pitch = nm(int(SUNG.split(";")[0]) + RIFF_NOTE[pos[i]])
        for tr in (("vl", "vr") if kind == "bark" else (("tc",) + (("sl", "sr") if sung and SUNG.split(";")[5] else ())) if one else ("tl", "tr")):
            T.setdefault(tr, []).append({"at": round((bar * 16 + pos[i] + (HOLES if kind == "talk" else 0)) / 4, 4), "len": round(ln * 0.9 / 4, 4), "pitch": pitch, "vel": 0.9, "ph": ph})


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "g": "snare", "h": "hat", "c": "cym", "x": "cym", "cch": "cym", "rb": "ride", "rd": "ride"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece in ("h", "rb", "rd") else 0.25, "pitch": piece, "vel": round(vel, 3)})


def groove(b0, b1, lead, snare, cym, kvel=0.92):
    """A station's beat: the kick on every chug of either guitar (and the left's open string), the snare on `snare`,
    a cymbal on the quarter."""
    kicks = sorted(set(CHUGS + [3]) | {(p - lead) % 16 for p in CHUGS})
    for b in range(b0, b1):
        for p in kicks:
            drum("k", b * 16 + p, kvel * (1.0 if p % 4 == 0 else 0.9))
        for p in snare:
            drum("s", b * 16 + p, 0.95)
        for p in range(0, 16, 4):
            drum(cym, b * 16 + p, 0.6 if p == 0 else 0.5)
    drum("c", b0 * 16, 0.9)


def groove_eighth(b0, b1, lead, ghost, china):
    """The beat of the hold an eighth apart: built on the eighth. The kick as everywhere (every chug of either guitar);
    the snare on two and four, each answered a ghost stroke an eighth later, as each hook note is; the hat in eighths."""
    kicks = sorted(set(CHUGS + [3]) | {(p - lead) % 16 for p in CHUGS})
    for b in range(b0, b1):
        for p in kicks:
            drum("k", b * 16 + p, 0.92 * (1.0 if p % 4 == 0 else 0.9))
        for p in (4, 12):
            drum("s", b * 16 + p, 0.95)
            drum("g", b * 16 + p + 2, ghost)
        for p in range(0, 16, 2):
            drum("h", b * 16 + p, 0.62 if p % 4 == 0 else 0.48)
        drum("x", b * 16, china)
    drum("c", b0 * 16, 0.9)


def groove_three(b0, b1, tick):
    """The beat of the hold three sixteenths apart: no time-keeping, only the five places the two guitars strike
    together. The pendulum ticks under it."""
    hits = sorted(set(ATTACKS) & {(p - 3) % 16 for p in ATTACKS})
    assert hits == [0, 3, 10, 12, 13]
    for b in range(b0, b1):
        for p in hits:
            drum("k", b * 16 + p, 0.95)
        for p in (3, 10):
            drum("s", b * 16 + p, 0.95)
        drum("x", b * 16, 0.7)
        drum("rb", b * 16, tick * 1.12)
        drum("rb", b * 16 + 8, tick)
    drum("c", b0 * 16, 0.9)
    return hits


def groove_one(b0, b1, tomv, kv):
    """The beat of the hold a sixteenth apart: the kick on every note of either guitar; the three sixteenths neither
    plays go to a tom, the floor tom and the snare; the china on the quarter as in step."""
    union = sorted(set(ATTACKS) | {(p - 1) % 16 for p in ATTACKS})
    holes = [p for p in range(16) if p not in union]
    assert len(union) == 13 and holes == [4, 7, 8]
    for b in range(b0, b1):
        for p in union:
            drum("k", b * 16 + p, 0.92 if p % 4 == 0 else kv)
        if HOLE_FILL and not ON_THREE:
            # High tom, middle, floor, snare. The crack therefore lands on
            # beat two, just BEFORE beat three, then ON three to close the fill.
            strokes = (("t1", tomv), ("t2", tomv * .94), ("ft", tomv * 1.07), ("s", .95))
            for i, p in enumerate(holes):
                pc, v = strokes[((b - b0) * len(holes) + i) % len(strokes)]
                drum(pc, b * 16 + p, v)
        else:
            drum("t2", b * 16 + 4, tomv)
            drum("ft", b * 16 + 7, tomv)
            drum("s", b * 16 + 8, 0.95)
        for p in range(0, 16, 4):
            drum("x", b * 16 + p, 0.6 if p == 0 else 0.5)
    drum("c", b0 * 16, 0.9)


def fill(b, kind="toms"):
    """The last half bar before bar `b`."""
    if kind == "toms":
        for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
            drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)
    else:
        for i in range(8):
            drum("s", b * 16 - 8 + i, 0.5 + 0.06 * i)


# v21: THE CLOCK THAT OPENS THE SONG IS A MUSIC BOX (palette round). The song opened on the left guitar and a
# "pendulum": the kit's ride bell on one and three. Harry has now turned that pendulum down twice where it was
# exposed: under the drift ("doesnt work at this tempo on this kit piece") and at the end ("Sounds like a click
# track"); both went at v17, and the music boxes that replaced them he kept ("Music boxes: keep them", "An ending:
# keep it"). The same ride bell still opened the song, as exposed as anywhere: one guitar and a tick. Now the opening's
# clock is the LEFT MUSIC BOX: tick on the bar line (the riff's F, two octaves over the boxes' riff), tock on three
# (the C under it). One clock, on the left, with the left guitar; the instrument that takes the riff when the guitars
# let go (2:44) and that the song ends on. So the song begins and ends on the same clock.
# the track ; the tick's semitones over the song's low F ; the tock's ; the tick's velocity ; the tock's. "" = v20.
CLOCK = os.environ.get("C10T2_CLOCK", "ml;60;55;1.0;0.85") if BOX else ""


# v22: IN EVERY SLIP YOU HEAR THE TWO CLOCKS (palette round). Each time the right guitar slides a sixteenth further
# ahead (four slips: 0:53, 1:11, 1:46, 2:04) the kit thinned to a kick on the bar line and a hat counting quarters, "so
# the slip is heard". The hat goes, and two MUSIC BOXES take its place: a left one that ticks on one and tocks on
# three, on the song's clock, and a right one written on the same beats but on the RIGHT GUITAR'S clock (the track
# `warp`; nothing is shifted by hand). So as the right guitar slides, the right tick slides with it: in the first
# slip the two ticks start together and pull apart until they are a sixteenth apart; in each later slip they start
# as far apart as the hold before and widen by one more. The slip is the song's whole idea, and now each one states
# it with nothing but two clocks ticking: the same instrument that opens the song, takes the riff when the guitars let
# go, and ends it. Harry on the slips: "A thrill", and "add".
# the patch ; its gain ; the pan ; the tick's velocity ; the tock's ; the hall send ; the spring's mix. "" = v21.
SLIPCLOCK = os.environ.get("C10T2_SLIPCLOCK", "music-box;-7dB;0.7;1.0;0.85;-9dB;0.22") if BOX else ""


# v24: THE CLOCKS CHIME THE ECHO (section round, 1:38-1:46; the window 1:11-1:46, "little new"). The hold an eighth
# apart had three parts: six bars of its beat, two bars naked (the two guitars alone, so the echo is heard: every
# hook note of the right guitar answered by the left an eighth later), and then four bars of the same beat again. The
# last four are now what the first six were not: over the band TWO MUSIC BOXES play the riff's three hook notes, the
# left one on the song's clock and the right one on the right guitar's (the track `warp`; nothing is placed by hand).
# So each note chimes on the right and is answered on the left an eighth later, four octaves over the guitars: the
# echo the naked bars have just shown, said by the song's clocks. The echo is implied, then exposed, then rung.
# It is the first time the boxes play the riff's notes: until now they have only ticked (the opening, the slips);
# a minute later (2:44) they take the whole riff. And they go straight from this into the next slip's ticks.
# (First bench at 0 dB: the two boxes were the loudest things in the band and the four bars 1.8 dB up. At -6 dB they
# sat 4 to 5 dB under each guitar, but alone they were within 2.6 dB of the WHOLE mix from 500 Hz to 1 kHz, where
# their fundamentals are and the band has little: a pure tone holds its band at a level a guitar would not. -8 dB.)
# first bar : last ; the patch ; its gain ; the pan ; the hall send ; the spring's mix ; the velocity. "" = v23.
CHIME = os.environ.get("C10T2_CHIME", "44:48;music-box;-8dB;0.7;-9dB;0.22;0.9") if BOX else ""
HOOK_AT = [p for p, _, k in RIFF if k.startswith("h")]


# v25: THE GUITARS' CHEST, AND FOUR GUITARS AGAINST (whole-song round: the song read part by part and stretch by
# stretch against the eleven records, and its loudness read seam by seam with chirp-eco's seams.py).
#   1. THE TWO GUITARS WERE HOLLOW. Wherever no voice sings (in step, the hold an eighth apart, the hold three apart)
#      the band read 2.6 to 3.4 dB UNDER the records from 500 Hz to 1 kHz; where a voice sings it did not, because
#      the voice fills that band. So the guitars had no chest of their own. They get it (one eq band on each).
#   2. THE ARRIVAL WAS NO BIGGER THAN A HOLD. The song's whole aim is the bar where the two clocks are exactly against
#      each other (3:38). It comes out of the quiet drift, so it is a jump of 5 dB; but at -8.7 to -8.8 LUFS it is
#      exactly as loud as the hold a sixteenth apart at 1:00 (-8.8), and so is every hold between (-8.7 to -9.8, for
#      two and a half minutes). Now, when the clocks lock against each other, EACH CLOCK HAS TWO GUITARS: a second
#      take on each side, through another amplifier, microphone and cone, the right one on the right clock (`warp`).
#      It is still one riff on two clocks; the machine with no holes is four guitars wide. They leave where the band
#      does (4:31) and the two guitars end the song alone, as they began it.
# (First bench of the doubles, 1.5 dB under the main pair on paper and the microphone nearer the cone: they were the
# LOUDEST tracks in the band (this amplifier is hotter), the barked voices fell 2 dB behind them, and the stretch
# went from 1.0 to 2.8 dB over the records at 2-4 kHz, the band v13 had mended. So: 5.5 dB under on paper, which
# is about 3 under by ear's measure, and the microphone well off the cone.)
# the guitars' band: Hz : q : dB. "" = v24.
MIDS = os.environ.get("C10T2_MIDS", "700:0.9:2")
# With four guitars the barked voices read 0.7 dB further back; they get that back (the last field), so they sit
# against the band where they did.
# the doubles: amp model : mic : left cone : right cone ; their gain against the main pair's, dB ; pan ; first bar : last ;
# the barked voices' trim, dB. "" = v24.
FOUR = os.environ.get("C10T2_FOUR", "modern:0.6:6:7;-5.5;0.7;98:122;0.7") if TWIN else ""


# v26: THE TWO GUITARS TRADE A BAR (section round, 0:27-0:31, in the window 0:00-0:35 the map calls static: sixteen
# bars of one riff). The song is about two guitars with a clock each, and for its first half minute you cannot tell
# there are two: in step, hard left and right, they are one wide guitar. So before anything slips they show
# themselves: after four bars together the LEFT guitar plays the riff alone for a bar, then the RIGHT alone for a
# bar, then both again into the stop and the voice's first word. The bass and the kit go straight on underneath. You
# have now heard each of them by itself; when the right one starts to pull ahead at 0:53 you know who it is.
# the bar the left guitar has alone ; the bar the right has alone. "" = v25.
TRADE = os.environ.get("C10T2_TRADE", "12;13")


# v28: in the gap between the last two barks the inside pair sing the line that
# comes from BOTH clocks, at three times its length. The main pair keep the fast
# line audible underneath. Empty restores v27 exactly.
BRAID = os.environ.get("C10T2_BRAID", "1")
# v30, THE WHOLE MACHINE (whole-song round). The song is for the bar where the two clocks are exactly against each
# other, and its last pillar said so three times alike: the same four barks over the same beat at 3:47, 4:04 and
# 4:22. The third time is now the song's peak. For the band's last four bars the RHYTHM SECTION IS THE TWO CLOCKS:
#   the bass   plays every note of either guitar, sixteen to the bar: F F Ab F F F B C, twice. It is the tune the
#              inside guitars have just picked out slowly in the gap (v28), now at full speed and at the bottom;
#   the feet   play the left guitar: the kick on its eight attacks and nowhere else;
#   the hands  play the right guitar where it sounds: the snare on its low string, a tom for each hook note (floor
#              tom, middle, high for A flat, B and C). The china stays only where the hands are free (one and four).
# Sixteen strokes a bar and no two together; the second half of the bar is the first with hands and feet exchanged,
# which is how the riff was written. Until now the kick took both guitars' chugs and the snare kept a backbeat.
# bars from:to ; the toms' velocity : their notes' gain ; the snare's second stroke of a pair ; the snare on the right
# guitar's open string ; the loudness target (the passage is denser: every other bar keeps v29's mastering gain).
# "" = v29.
# (Benched raw on seed 0 against the same bars of v29. First try, toms at 0.85 and full gain, the snare's other
# strokes at 0.8 and 0.72: the four bars rose 0.47 LU, 1.9 dB at 250-500 Hz (the band v14 cut on this song; the toms
# were as much of it as the snare) and each barked syllable sat 0.8 dB further behind the band. As set here: +0.26 LU,
# +1.1 dB at 250-500 Hz, the barks 0.4 dB further back at the median and no further in their worst quarter. The
# snare on the beat sits where the backbeat sat, 1.8 dB under the mix in its first 60 ms; its second strokes 3.7
# under, the open string's 6.4, the toms 7 to 8.)
MACHINE = os.environ.get("C10T2_MACHINE", "118:122;0.8:-4.5dB;0.72;0.62;-10" if HOLE_FILL and BRAID and FOUR and SHAKE else "")
# v31: THE FAST CLOCK SOUNDS FAST (chirper-alpha; section round, 2:04.4-2:08.9, in the window 1:46-2:22 the map calls
# "little new"). The right guitar is the left guitar on a faster clock, and until now you heard that only in TIME: in
# every slip it arrives earlier and earlier. But a sound that arrives earlier and earlier is also HIGHER: a tape run
# fast, or anything heard through a delay that is shrinking, rises by exactly as much as it gains. In the last slip
# before the hold a beat apart (the fast one: a sixteenth in two bars) the right guitar's PITCH goes with its clock.
# Each of its notes is tuned by how fast its clock is running when it is struck. The slip eases in and out, so the
# guitar leans sharp, 87 cents at the middle (its clock 5.2% fast, not far short of the G flat above), and comes back
# into tune as it comes back into time: it is in tune again exactly when it locks a beat ahead, on F, where the two
# guitars' chugs meet on four. The left guitar, the bass and the two music boxes stay where they are: the ear has F all
# the way through. Nothing is tuned by hand: the cents are read off the track's `warp`.
# Only this slip. The two slow slips (0:53, 1:11) Harry signed off as they are ("A thrill"); the fast one at 1:46 has
# just changed ground to B and has no home to lean from. `48:50,56:58` would do both fast ones.
# bars from:to (several, comma-separated) ; how much of the clock's true shift (1 = exactly the clock's). "" = v30.
VARI = os.environ.get("C10T2_VARI", "56:58;1")
# v32: THROUGH THE WALL (chirper-alpha; section round, 1:20-1:33.3, the first six bars of the hold an eighth apart, in
# the window 1:11-1:46 the map calls "little new"). At this distance the left guitar is the right guitar's echo: every
# note of the right is answered by the left an eighth later. The hold showed that three ways and the first was only
# implied: six bars of its beat with both guitars at full, then two bars naked, then the music boxes chiming it. The
# six bars were one texture from the first bar to the last. Now the answer starts on the other side of a wall (the
# song's first line: "I cannot hear you through the wall / only the floor between us moves"). When the band lands on
# A flat the LEFT guitar is heard as a neighbour's is, its low end and nothing else, and over four bars the wall
# thins until it is all there: so the echo comes into focus as you listen. Two bars of the band whole, then it
# stops and the two guitars are alone. Walled, then naked, then rung. The right guitar, the bass and the kit are as
# they were; the left guitar's notes are the same notes (they move to a track of the same guitar behind a low-pass).
# Raw, seed 0, bar by bar from the landing: the walled guitar's brightness (spectral centroid) 250, 525, 1110, 1600,
# 1850, 1850 Hz against 1820 to 1970 open; it stands 5.7, 4.7, 2.8, 1.3, 0.5 and 0.2 dB under itself; the mix is
# 0.6, 0.7, 0.5, 0.3, 0.2 and 0.0 dB down, 1.7 dB of it at 1-4 kHz in the first two bars, and leans 1.4 to 1.7 dB
# further right in those two, under 1 dB after. Under 250 Hz nothing moves: the floor.
# (Benched with the wall gone a bar sooner: the opening was over in three bars. From 400 Hz: no different to speak of.)
# bars from:to ; the low-pass's cutoff as the hold begins, Hz ; the bar by which it is fully open (16 kHz) ; its q.
# "" = v31.
WALL = os.environ.get("C10T2_WALL", "36:42;300;42;0.7")
# v33: THE SNARE STAYS ON THREE (Harry, 19 Nov 02:20, on the card for v29's fill, "Keep the moving snare on C?":
# "Keep it on three"; he was played the same fill each bar and then the fill across the bars). So in the hold on C
# the drummer fills the three holes the same way in every bar again, middle tom, floor tom, and the snare ON three,
# as up to v28. v29's four strokes across three holes are behind this switch. "" = v32. It is on only while none
# of the older switches is set, so each of those still gives exactly what it gave.
# The switches there were at v32. With any of them set in the environment this one is off unless it is set too.
OLDER = """
         AGREE BOX BRAID CHIME CLOCK CLOCKS DRIFT DTOP EARLY EIGHTH END FOUR GBODY HEARD HOLE_FILL HOLES KEYEQ
         L2 LETGO LOCK LOWRIDE MACHINE MIDS MIX NAKED ONE OPEN PEND PULSE QUARTER SHAKE SLIPCLOCK SNARE
         SNAREEQ SUNG SUNG2 TALKEQ TALKFX THREE TRADE TWIN V14MAKEUP VARI VOICE WALL""".split()
ON_THREE = os.environ.get("C10T2_ON_THREE", "" if any("C10T2_" + k in os.environ for k in OLDER) else "1")
# v34 (chirper-three; section round, w5 2:22-2:57; the change is bars 71-73, 2:37.8-2:44.4): WHERE IT HAS STOOD.
# The hold a beat apart is the longest in the song, sixteen bars on F, and its last three, after the last sung
# line ("against you until we agree") and before the band lets go, were plain. Each earlier hold stood on a note of
# the hook: a sixteenth apart on C, an eighth apart on A flat, three sixteenths apart on B. Now those three bars
# stand where the song has stood, a bar each, in that order: C, A flat, B, and the band lets go on F. The riff, the
# kick, the snare, the ride and the fill are as written; only the ground moves (78 notes of the two guitars and the
# bass change pitch, none moves in time), and the bass's eq follows it as it does in the holds.
# AND THE CANON SHOWS AS HARMONY: each guitar changes on its own clock, so the right one gets to every ground a
# beat before the left. For one beat in each bar the two sides stand on different notes: C over the left's F under
# the word "agree" (a fifth), then A flat, then B, and at last the right guitar's F under the left's B, the hook's
# tritone, which closes when the left lets go a beat later (v11: "the last thing the canon does").
# the first bar : the ground of each bar from there, in semitones over F. "" = v33 (and it is on only while ON_THREE is).
STOOD = os.environ.get("C10T2_STOOD", "71:7,3,6" if ON_THREE else "")
# v35 (chirper-one; whole song): THE RIGHT CLOCK RUNS SHARP WHEN IT RUNS FAST. v31 gave one slip the law of a tape
# machine: what runs fast sounds sharp by exactly as much as it gains (the right guitar, 2:04). The song's CLOCKS are
# its music boxes ("A clock: keep it"), and wherever the right-hand clock runs free one of them is on it: the right
# tick through each slip (v22: "The slip made plain: keep them"), and the right box through the whole drift. They
# kept perfect pitch while their clock ran fast. Now their notes are tuned by how fast their clock is running when
# they are struck, read off the track's `warp` as v31's guitar is:
#   the drift         the right box is 19.8 cents sharp for the 22 bars it drifts (2:44.4-3:33.3: its clock is 1.15%
#                     fast, steadily), and in tune from the bar the two clocks stand exactly against each other, two
#                     bars before the band lands on it. Out of sympathy is out of tune; locked is in tune
#   the quick slips   (1:46, 2:04) the right tick leans sharp as it pulls ahead and comes back as it locks: 61, 87,
#                     61 cents. At 2:04 the right guitar leans with it (v31). The left tick stays true, so the two
#                     ticks are heard apart in time AND in pitch
# NOT the two slow slips (0:53, 1:11; 43 cents at most): built and benched, and not kept. The tick's spring answers
# an F6 that is 30 to 43 cents sharp 5 to 10 dB more than a true one and rings on, so three ticks in each stood out
# of the passage Harry signed off ("A thrill"). Not the shake at 3:56 ("Yes: a thrill") either.
# No note moves in time; no guitar, voice, bass or drum is touched. The box's spring also answers some of the
# drift's sharp notes more than the true ones (F most), so those carry a trim: the right box alone reads 0.5 dB
# over what it was through the drift (K), 2.0 in its first four bars, within 0.65 after.
# track=bars from:to,... ; track=... ; how much of the clock's true shift (1 = exactly the clock's) ; dB on the
# right box's sharp notes, by the note written. "" = v34.
FAST = os.environ.get("C10T2_FAST", "br=48:50,56:58;mr=74:96;1;F5=-4.2,F6=-6,A5=-4.8,B5=-2.2,Gb5=-2.1,C6=-2,C5=-1.2,Db6=-1,Db5=1.5" if STOOD else "")
# v36 (chirper-alpha; section round, w1 0:00-0:35; the change is bars 4 to 8): THE SECOND CLOCK IS SET GOING. Every
# slip in the song is the right-hand clock sliding against the left, but the song BEGAN in step: at bar 4 the right
# guitar simply came in with the left, and 'in step' was never something heard to happen. Now the right-hand clock
# is set going a sixteenth LATE and the beam pulls it in over four bars: the first slip (bars 24 to 28: a sixteenth
# ahead, on half a cosine) played backwards. The right guitar's sixteen chugs are the notes they were; they sound
# 139 ms after the left's at bar 4, 118 at bar 5, 69 at bar 6, 20 at bar 7 and 1 at the fill, and the band lands in
# step at bar 8. A second music box (the drift's right-hand one) ticks on that clock from bar 4, so the two ticks
# close as the two guitars do. The bass, kick and hat stay with the left. From bar 8 the clock is the one it was.
# Measured (each part alone): the chugs within 11 ms of what is written; the right box 1.5 to 4.4 dB under the left
# tick by tick with -2 dB on its ticks and -5.5 on its tocks (the patch deals each note its level: as it came the
# right tocks were 2.5 to 4 dB over the left's). Two boxes on one note add by phase where they nearly meet: one tock
# can read 4 dB under a single box.
# the bar the right-hand clock is set going : the bar it is in step ; how late it starts, beats ; dB on the right
# box's tick : its tock, against the left box's ("" = no box). "" = v35.
SETGOING = os.environ.get("C10T2_SETGOING", "4:8;0.25;-2:-5.5" if FAST else "")
# v37 (chirper-two; section round, w6 2:57-3:33, the drift's middle; the change is 2:57.8-3:20): ONLY THE FLOOR
# BETWEEN US MOVES. The drift is the song's quiet middle: two music boxes saying the riff for 49 seconds while the
# right one slides to half a bar ahead, and under them the ground steps down (F, E flat, D flat, C: v2). The song's
# four lines are sung in step (0:36) and a beat apart (2:13), and the last is barked when the clocks are against each
# other (3:46). In the drift nobody sang; and it is the one place where what the second line says is simply so: the
# band has let go, there is no beam, and the only thing that moves under the two clocks is the floor.
# So the two singers sing one line each there, SLOWLY: a syllable to each attack of the riff, as everywhere in this
# song, on the riff's own notes (F F F B A-flat F F C: the tune of 0:36), four times slower. The riff's sixteenths
# are beats; an unstressed syllable is not held; the last word rings.
#   the LEFT voice, on the song's clock: "only the floor between us moves", from 2:57.8, as the floor moves to E flat;
#   the RIGHT voice, on the right-hand clock (the track `warp`: nothing is placed by hand), so in time with its own
#   music box and a beat and a half before the ink: "whatever way you lean I lean", sounding 3:09.7 to 3:19.
# Then six bars of the boxes alone into the lock, the landing, and the last line barked by both.
# THEY ARE HEARD THROUGH THE WALL (the first line: "I cannot hear you through the wall"): the song's own singer
# (`voice-talk`, sung, as at 0:36), low-passed at 700 Hz, so they stay under the boxes' band: a murmur, not a lead.
# Harry on this passage's pulse: "Too much: it buries the boxes". So the voices were set by reading them against the
# boxes, syllable by syllable (raw, each part alone):
#   first bench (-12 dB, a 1.5 kHz filter): the voices stood 5.8 dB OVER the boxes on "only the", and the boxes' lead
#   over everything else in their own band (600 Hz-2.5 kHz) fell from +10.5 to -3.9 dB. This voice's syllables also
#   differ by 13 dB ("floor", on B, the loudest; "lean" on A flat the softest), so one fader could not hold them under;
#   as set: a fader ride, syllable by syllable (the last field), puts every syllable within 1 dB of the middle one
#   but "lean" (2.7 under); each stands 3.7 to 8.7 dB under the boxes (K) while it sounds; the boxes' lead in their
#   own band is +6.0 to +11.3 dB during the syllables (+7.9 to +10.6 by two bars, where v36 read +10.5 to +12.3);
#   the passage is 0.3 dB louder (K). The pulse, the bed, the swarm and the boxes are not touched.
# THE WORDS: a recogniser reads the two voices alone 4 words of 12 as set (8 before the ride; 7 with the filter at 1
# or 1.5 kHz) and none under the boxes. They are not there to be read: both lines have been sung twice by then, on
# these notes.
# Not done: the right voice does not run sharp with its clock, as its box does (v35): the ninth field gives it
# (it plans; not rendered).
# left voice's bar:line , right voice's bar:line (lines counted from 0) ; how many times slower than the riff ; the
# patch ; gain ; pan ; hall send ; eq bands ; the MIDI note the riff's F is sung on ; 1 = the right voice's pitch goes
# with its clock, as its box's does (v35) ; the loudness target ('' = unchanged) ; a fader ride, dB on each of the
# left voice's eight syllables : the right's ('' = none). "" = v36.
FLOOR = os.environ.get("C10T2_FLOOR", "80:1,86:2;4;voice-talk;-19dB;0.5;-10dB;hp cutoff=150|lp cutoff=700 q=0.7;53;0;;-3,2,0,-6.5,0,1.5,-1.5,4:-2,-3,-1.5,0,4,4,-2.5,2.5" if SETGOING else "")
if SETGOING:
    _g0, _g1 = (int(x) for x in SETGOING.split(";")[0].split(":"))
    assert WARP[0] == {"over": "96b", "to": 0} and 0 < _g0 < _g1 <= 24
    # the same device as every slip (the engine's `warp`; nothing is shifted by hand): the right-hand clock is late
    # when it starts and is in step by bar _g1. Before bar _g0 nothing on that clock sounds.
    WARP = [{"over": f"{_g0 * 4}b", "to": float(SETGOING.split(";")[1])}, {"over": f"{(_g1 - _g0) * 4}b", "to": 0, "curve": "smooth"},
            *([{"over": f"{(24 - _g1) * 4}b", "to": 0}] if _g1 < 24 else [])] + WARP[1:]


# v38 (chirper-one; section round, w7 3:33-4:08, the window longest without a section round; the change is the
# shake, 3:55.5-4:03.3): THE SHAKE IS HEARD ON THE TWO CLOCKS. In each of the four slips two music boxes tick, one on
# each clock (v22; Harry: "The slip made plain: keep them"). The shake (v18; "Yes: a thrill"), where the locked
# guitars are disturbed and fall back, was the one slip without them: a hat counted its quarters. Now the hat goes
# and the two boxes tick through it. The left one ticks on one and tocks on three, on the song's clock. The right one
# is written the same way on the right-hand clock (the track `warp`; nothing is placed by hand), which stands half a
# bar ahead there: so where the left says tick the right says tock, the first time the song says "against" with its
# clocks. Shaken, the right box runs ahead of the left by 40 ms, a sixteenth, most of an eighth, an eighth, and falls
# back the same way; its eighth note lands exactly on the left's, at the tom fill, half a bar before the crash.
# And its pitch goes with its clock (v35's law): 125, 179, 125 cents SHARP while it gains, true at the turn, then 116,
# 162, 116 cents FLAT while it falls back (the only place in the song a clock runs slow), and true again when it
# locks. Read alone, the three flat notes came 1.6 to 4.1 dB louder than true ones (the box's spring answers them),
# so they carry a trim. The guitars, the bass, the kick and the fill are v37's.
# dB on the left box's notes there against the slips' ; dB on the right box's eight notes, comma between ; how much of
# the clock's true shift its pitch takes (1 = exactly the clock's; 0 = in tune) ; the hat's velocity there ('' = no
# hat; v37 had 0.45) ; how much of the clock's shift the right GUITARS' pitch takes (0 = none: v37's guitars) ; the
# loudness target ('' = unchanged). "" = v37.
SHOOK = os.environ.get("C10T2_SHOOK", "0;0,0,0,0,-1.5,-3.5,-2.5,0;1;;0;" if FLOOR and SHAKE and SLIPCLOCK else "")


def stood():
    """-> [(bar, semitones over F), ...]: the bars of the hold a beat apart that stand where the earlier holds stood."""
    if not STOOD:
        return []
    first, grounds = STOOD.split(":")
    return [(int(first) + i, int(x)) for i, x in enumerate(grounds.split(","))]


def clock_speed(tau):
    """How fast the right-hand clock is running against the song's at its own beat `tau` (1 = together): the engine's
    `warp` moves a note written at tau to tau + shift(tau), so the track runs at 1 / (1 + shift'). A `smooth` stretch
    is half a cosine (lower.rs, WarpCurve::Smooth)."""
    b = d = 0.0
    for seg in WARP:
        over = float(seg["over"].rstrip("b"))
        if b <= tau < b + over:
            x = (tau - b) / over
            slope = (seg["to"] - d) / over * (math.pi / 2 * math.sin(math.pi * x) if seg.get("curve") == "smooth" else 1.0)
            return 1.0 / (1.0 + slope)
        b, d = b + over, seg["to"]
    return 1.0


def lean(tr="gr"):
    """v31: each note of a right-hand track in the VARI bars takes its clock's speed as pitch."""
    spans, depth = [tuple(int(v) for v in s.split(":")) for s in VARI.split(";")[0].split(",")], float(VARI.split(";")[1])
    for n in T[tr]:
        if any(b0 * 4 <= n["at"] < b1 * 4 for b0, b1 in spans):
            cents = 1200 * math.log2(clock_speed(n["at"])) * depth
            if abs(cents) >= 0.5:
                name = n["pitch"]
                midi = NAMES.index(name.rstrip("-0123456789")) + 12 * (int(name[len(name.rstrip("-0123456789")):]) + 1)
                n["pitch"] = f"m{midi + cents / 100:.3f}"


def run_sharp():
    """v35: each note of a music box on the right-hand clock, in the bars named, takes its clock's speed as pitch."""
    depth = float(FAST.split(";")[2])
    trim = {k: float(v) for k, v in (x.split("=") for x in FAST.split(";")[3].split(",") if x)}
    for part in FAST.split(";")[:2]:
        tr, bars = part.split("=")
        spans = [tuple(int(v) for v in s.split(":")) for s in bars.split(",")]
        for n in T.get(tr, []):
            if any(b0 * 4 <= n["at"] < b1 * 4 for b0, b1 in spans):
                cents = 1200 * math.log2(clock_speed(n["at"])) * depth
                if abs(cents) >= 0.5:
                    name = n["pitch"]
                    midi = NAMES.index(name.rstrip("-0123456789")) + 12 * (int(name[len(name.rstrip("-0123456789")):]) + 1)
                    n["pitch"] = f"m{midi + cents / 100:.3f}"
                    if tr == "mr" and name in trim:      # the box's spring answers some of the sharp notes more than the true ones
                        n["gain"] = f"{trim[name]:g}dB"


def the_floor_moves():
    """v37: one line each for two slow voices in the drift, a syllable to each attack of the riff as everywhere, the
    riff FLOOR's second field times slower; the right voice is written like the left and is on the right-hand clock."""
    f = FLOOR.split(";")
    slow, base = float(f[1]), int(f[7])
    rides = [[float(x) for x in r.split(",")] if r else [0.0] * 8 for r in (f[10].split(":") if len(f) > 10 and f[10] else ["", ""])]
    for (tr, part), ride in zip(zip(("fl", "fr"), f[0].split(",")), rides):
        if not part:
            continue
        bar, line = (int(x) for x in part.split(":"))
        phs, how = VOICE_LINES[line]
        pos = ATTACKS if how == "down" else [-1] + ATTACKS[:-1]
        for i, ph in enumerate(phs.split("|")):
            gap = (pos[i + 1] - pos[i]) if i < 7 else 3
            weak = any(x[-1] == "0" for x in ph.split() if x[-1].isdigit())      # an unstressed syllable is not held
            ln = min(gap, 1) if weak else 3 if i == 7 else min(gap, 2)           # in the riff's sixteenths; the last word rings
            T.setdefault(tr, []).append({"at": round(bar * 4 + pos[i] * slow / 4, 4), "len": round(ln * slow / 4 * 0.96, 4),
                                         "pitch": nm(base + RIFF_NOTE[pos[i]]), "vel": 0.8, "ph": ph, **({"gain": f"{ride[i]:g}dB"} if ride[i] else {})})
        if tr == "fr" and f[8] == "1":
            for n in T[tr]:
                cents = 1200 * math.log2(clock_speed(n["at"]))
                if abs(cents) >= 0.5:
                    name = n["pitch"]
                    midi = NAMES.index(name.rstrip("-0123456789")) + 12 * (int(name[len(name.rstrip("-0123456789")):]) + 1)
                    n["pitch"] = f"m{midi + cents / 100:.3f}"


def cents_of(n):
    """The cents a right-hand note's clock gives it where it is written (v31's and v35's law)."""
    return 1200 * math.log2(clock_speed(n["at"]))


def retune(n, cents):
    name = n["pitch"]
    midi = NAMES.index(name.rstrip("-0123456789")) + 12 * (int(name[len(name.rstrip("-0123456789")):]) + 1)
    n["pitch"] = f"m{midi + cents / 100:.3f}"


def shake_on_the_clocks():
    """v38: the two music boxes tick through the shake. The left one ticks on one and tocks on three, on the song's
    clock. The right one is written the same way on the right-hand clock, which is half a bar ahead there: so its tock
    sounds with the left's tick. Its eight notes are those that SOUND in the shake's four bars; each is tuned by how
    fast its clock is running where it is written."""
    f = SHOOK.split(";")
    s0, s1 = _sb, _sb + 2 * _sn
    lg, rg, depth, gdepth = float(f[0]), [float(x) for x in f[1].split(",")], float(f[2]), float(f[4] or 0)
    v1, v2 = float(SLIPCLOCK.split(";")[3]), float(SLIPCLOCK.split(";")[4])
    tick, tock = nm(F1 + 60), nm(F1 + 55)
    T["hat"] = [n for n in T["hat"] if not (s0 * 4 <= n["at"] < s1 * 4)]
    if f[3]:
        for b in range(s0, s1):
            for q in range(0, 16, 4):
                drum("h", b * 16 + q, float(f[3]))
    for b in range(s0, s1):
        for at, pitch, v in ((b * 4, tick, v1), (b * 4 + 2, tock, v2)):
            T.setdefault("bl", []).append({"at": at, "len": 0.5, "pitch": pitch, "vel": v, **({"gain": f"{lg:g}dB"} if lg else {})})
    i = 0
    for b in range(s0, s1):              # written half a bar after where it sounds when the clocks are locked
        for at, pitch, v in ((b * 4 + 2, tock, v2), (b * 4 + 4, tick, v1)):
            n = {"at": at, "len": 0.5, "pitch": pitch, "vel": v, **({"gain": f"{rg[i]:g}dB"} if rg[i] else {})}
            if depth and abs(cents_of(n) * depth) >= 0.5:
                retune(n, cents_of(n) * depth)
            T.setdefault("br", []).append(n)
            i += 1
    if gdepth:                           # (off: the guitars of the shake are the ones Harry heard)
        for tr in ("gr", "gr2"):
            for n in T.get(tr, []):
                if (s0 - 1) * 4 <= n["at"] < (s1 + 1) * 4 and abs(cents_of(n) * gdepth) >= 0.5:
                    retune(n, cents_of(n) * gdepth)


def sing_the_lock():
    start = 114*16 + 4       # after the left voice's held syllable
    width, stretch, lead = 16, 3, 8
    end = start + width*stretch  # before the right voice's next pickup
    row = {t:kind for t, _, kind in RIFF}
    for tr, offset in (("gl2", 0), ("gr2", lead)):
        # At this station the right guitar sounds eight ticks BEFORE the ink.
        T[tr] = [n for n in T[tr] if not start <= round(n['at']*4)-offset < end]
    for i in range(width):
        left = i in row
        j = i if left else (i+lead) % width
        kind = row[j]
        key = F1 if kind in ('c','o') else HOOK[int(kind[1])]
        # Same eight pitches twice, but no one plays the same half twice. Keep
        # the short palm strokes separate from the open string and hook notes.
        add('gl2' if left else 'gr2', start+i*stretch+(0 if left else lead),
            1.65 if kind=='c' else 2.8, key+24, .87 if kind=='c' else .96,
            **({'pm':1} if kind=='c' else {}))


def whole_machine(b0, b1, toms, pair, openv):
    """The band's last bars, half a bar apart: the bass on all sixteen, the feet on the left clock, the hands on the
    right. Written where the right guitar SOUNDS: the kit and the bass keep the song's time."""
    lead, tomv, tomg = 8, float(toms.split(":")[0]), toms.split(":")[1]
    right = {(p - lead) % 16: kind for p, _, kind in RIFF}
    assert sorted(ATTACKS + list(right)) == list(range(16)), "no hole, and no sixteenth twice"
    for tr in ("kick", "snare", "toms", "bass"):
        T[tr] = [n for n in T.get(tr, []) if not (b0 * 4 <= n["at"] < b1 * 4)]
    # a drummer has two hands: the china only on the beats the left guitar's chugs take
    T["cym"] = [n for n in T["cym"] if not (b0 * 4 <= n["at"] < b1 * 4 and n["pitch"] == "x" and round(n["at"] * 4) % 16 in right)]
    bass(b0, b1, lead, vel=0.95, union=True)
    for n in T["bass"]:                  # a line of sixteen: no note rings into the next (the B is a semitone under the C)
        if b0 * 4 <= n["at"] < b1 * 4:
            n["len"] = min(n["len"], round(0.98 / 4, 4))
    for b in range(b0, b1):
        for p in ATTACKS:
            drum("k", b * 16 + p, 0.92 * (1.0 if p % 4 == 0 else 0.9))
        for q, kind in sorted(right.items()):
            if kind == "c":
                drum("s", b * 16 + q, 0.95 if q % 4 == 0 else pair)
            elif kind == "o":
                drum("s", b * 16 + q, openv)
            else:
                drum({"h0": "t2", "h1": "ft", "h2": "t1"}[kind], b * 16 + q, tomv)
                T["toms"][-1]["gain"] = tomg


def slip_clock(b0, b1, root=0):
    """The two clocks through a slip: the same ticks on `bl` (the song's time) and `br` (the right guitar's)."""
    v1, v2 = float(SLIPCLOCK.split(";")[3]), float(SLIPCLOCK.split(";")[4])
    up = 60 if root == 0 else 48                 # F6 and C6 on F; an octave lower on another ground
    for b in range(b0, b1):
        for tr in ("bl", "br"):
            T.setdefault(tr, []).append({"at": b * 4, "len": 0.5, "pitch": nm(F1 + root + up), "vel": v1})
            T.setdefault(tr, []).append({"at": b * 4 + 2, "len": 0.5, "pitch": nm(F1 + root + up - 5), "vel": v2})


# v23: THE BASS'S TONE FOLLOWS THE KEY (a mix round, found on Plain Hunt at its v11). The bass's bus has an eq cut to
# the low F: a notch on its fundamental (44 Hz), a lift on its octave (90 Hz), a compressor after them, a cut at four
# times the fundamental (170 Hz). When the ground moves the fundamental climbs into the lift, the compressor clamps on
# it and everything above it is pushed down. Alone, the bass's 120-250 Hz is 7.2 dB under its total on F, 12.4 on
# A flat, 12.4 on B and 18.3 on C; its 1-2 kHz growl 16.0, 19.0, 21.6, 25.5. So in the holds on A flat and B the bass
# lost its body, and on C nearly all of it: which is very likely what Harry heard when he asked for "more bass" on C.
# Now the three bands follow the ground (a lane `key` on the bus, semitones over F; the engine bends a frequency in
# octaves) IN THE HOLDS ON A FLAT AND B. The hold on C is left exactly as it is: Harry signed it off ("Enough") with
# 3 dB more bass, and whether it should have its tone back in place of that is on the Questions page.
# bar from : bar to : semitones over F, comma-separated. "" = v22.
# v27 (Harry, on the card that asked: "With its tone back: do it"): the hold on C too (28:32:7). v23-v26: 36:48:3,48:56:6.
KEYEQ = os.environ.get("C10T2_KEYEQ", "28:32:7,36:48:3,48:56:6")


def key_f(hz):
    return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}


def box_clock(b0, b1):
    tr, up1, up2, v1, v2 = CLOCK.split(";")
    for b in range(b0, b1):
        T.setdefault(tr, []).append({"at": b * 4, "len": 0.5, "pitch": nm(F1 + int(up1)), "vel": float(v1)})          # tick
        T.setdefault(tr, []).append({"at": b * 4 + 2, "len": 0.5, "pitch": nm(F1 + int(up2)), "vel": float(v2)})      # tock


def pendulum(b0, b1, vel=0.42):
    for b in range(b0, b1):
        drum("rb", b * 16, vel * 1.12)       # tick
        drum("rb", b * 16 + 8, vel)          # tock


def compose():
    # one clock: no introduction (Common Time has the long wait; this starts). The left guitar alone with the riff and a
    # pendulum; then the bass and the kick under it
    if CLOCK:
        box_clock(0, 8)
    else:
        pendulum(0, 8)
    T.setdefault("home", []).append({"at": 0, "len": 32.2, "pitch": "F1", "vel": 0.55})
    riff("gl", 0, 8, vel=0.85)
    if OPEN:                             # v9: the other guitar's chugs join with the bass and the kick: the riff's skeleton, on the right
        riff("gr", int(OPEN.split(";")[0]), 8, vel=0.85, only=CHUGS)
    if SETGOING and SETGOING.split(";")[2] and CLOCK:     # v36: and the right-hand clock has its own tick from the bar it is set going
        g1, g2 = SETGOING.split(";")[2].split(":")
        for b in range(int(SETGOING.split(";")[0].split(":")[0]), 8):
            T.setdefault(TICKS[1], []).append({"at": b * 4, "len": 0.5, "pitch": nm(F1 + int(CLOCK.split(";")[1])), "vel": float(CLOCK.split(";")[3]), "gain": f"{g1}dB"})
            T.setdefault(TICKS[1], []).append({"at": b * 4 + 2, "len": 0.5, "pitch": nm(F1 + int(CLOCK.split(";")[2])), "vel": float(CLOCK.split(";")[4]), "gain": f"{g2}dB"})
    bass(4, 8)
    for b in range(4, 8):
        for p in CHUGS:
            drum("k", b * 16 + p, 0.85)
        for p in range(0, 16, 4):
            drum("h", b * 16 + p, 0.45)
    fill(8)
    # in step
    riff("gl", 8, 24)
    riff("gr", 8, 24)
    bass(8, 24)
    groove(8, 24, 0, snare=(8,), cym="x")
    if TRADE:                            # v26: a bar each, alone (the clocks are in step here, so written time is sounding time)
        bl_, br_ = (int(x) for x in TRADE.split(";"))
        T["gr"] = [n for n in T["gr"] if not (bl_ * 4 <= n["at"] < bl_ * 4 + 4)]
        T["gl"] = [n for n in T["gl"] if not (br_ * 4 <= n["at"] < br_ * 4 + 4)]
    if OPEN:                             # v9: the band stops for the last beat before the voice, and its first word falls in the gap
        g0 = 15 * 4 + int(OPEN.split(";")[1]) / 4
        for tr in ("gl", "gr", "bass", "kick", "snare", "cym", "hat", "ride", "toms"):
            T[tr] = [n for n in T.get(tr, []) if not (g0 <= n["at"] < 64)]
        drum("c", 16 * 16, 0.9)
    agree_cut = None
    for name, b0, b1, lead in FORM[2:10]:
        if lead == 2 and EIGHTH:         # the hold an eighth apart: its own ground and its own beat (v4)
            root, ghost, china = [float(x) for x in EIGHTH.split(";")[:3]]
            riff("gl", b0, b1, root=int(root))
            riff("gr", b0, b1, root=int(root))
            bass(b0, b1, lead, root=int(root), union=True)
            groove_eighth(b0, b1, lead, ghost, china)
            if NAKED:                    # v16: two bars of the hold with the two guitars alone: the echo, heard naked
                n0, n1 = [int(v) for v in NAKED.split(":")]
                for tr in ("bass", "kick", "snare", "cym", "toms", "hat"):
                    T[tr] = [n for n in T.get(tr, []) if not (n0 * 4 <= n["at"] < n1 * 4)]
                drum("c", n1 * 16, 0.9)
            if CHIME:                    # v24: the two boxes chime the hook, an eighth apart, over the hold's last bars
                c0, c1 = [int(v) for v in CHIME.split(";")[0].split(":")]
                for tr in ("el", "er"):
                    riff(tr, c0, c1, vel=float(CHIME.split(";")[6]), up=TICK_UP, clean=True, root=int(root), only=HOOK_AT)
            continue
        if THREE and (lead == 3 or (b0, b1) == (48, 50)):     # the hold three sixteenths apart and the slip into it, on B (v6)
            root, tick = int(THREE.split(";")[0]), float(THREE.split(";")[1])
            riff("gl", b0, b1, root=root)
            riff("gr", b0, b1, root=root)
            if lead == 3:
                hits = groove_three(b0, b1, tick)
                bass(b0, b1, root=root, only=hits)
                if AGREE:
                    c0, cv, sb, sv = int(AGREE.split(";")[0]), float(AGREE.split(";")[1]), int(AGREE.split(";")[2]), float(AGREE.split(";")[3])
                    for b in range(c0, b1):                  # the china joins the snare on the two chords
                        if b != sb:
                            for q in (3, 10):
                                drum("x", b * 16 + q, cv)
                    for q in hits:                           # the last bar: the china on every hit
                        if q:
                            drum("x", sb * 16 + q, sv)
                    # and the guitars play only where they agree (the right guitar's turn comes after the loop: some
                    # of what it sounds in this bar is written in the next section)
                    T["gl"] = [n for n in T["gl"] if not (sb * 16 <= round(n["at"] * 4) < (sb + 1) * 16) or round(n["at"] * 4) % 16 in hits]
                    agree_cut = (sb, hits)
            else:
                bass(b0, b1, root=root)
                for b in range(b0, b1):
                    drum("k", b * 16, 0.85)
                    for p in (range(0, 16, 4) if not SLIPCLOCK else ()):
                        drum("h", b * 16 + p, 0.45)
                if SLIPCLOCK:
                    slip_clock(b0, b1, root)
                fill(b1, "snare")
            continue
        if ONE and lead == 1:            # the hold a sixteenth apart: the union, on C (v8)
            root, tomv, kv = int(ONE.split(";")[0]), float(ONE.split(";")[1]), float(ONE.split(";")[2])
            riff("gl", b0, b1, root=root)
            riff("gr", b0, b1, root=root)
            bass(b0, b1, lead, root=root, union=True)
            groove_one(b0, b1, tomv, kv)
            continue
        root = QROOT if (lead == 4 or (b0, b1) == (56, 58)) else 0      # the quarter hold and the slip into it, on C (tried at v7, off)
        riff("gl", b0, b1, root=root)
        riff("gr", b0, b1, root=root)
        bass(b0, b1, lead or 0, root=root)
        if lead is None:                 # a slip: the beat thins to a kick on the bar line and a hat, so the slip is heard
            for b in range(b0, b1):
                drum("k", b * 16, 0.85)
                for p in (range(0, 16, 4) if not SLIPCLOCK else ()):
                    drum("h", b * 16 + p, 0.45)
            if SLIPCLOCK:
                slip_clock(b0, b1, root)
            fill(b1, "snare" if b1 - b0 < 4 else "toms")
        else:
            groove(b0, b1, lead, snare=(4, 12) if lead in (2, 4) else (8,), cym="h" if lead == 2 else "rd" if lead == 4 else "x")
    if agree_cut:                        # v20: the right guitar is written three sixteenths later than it sounds in that bar
        sb, hits = agree_cut             # (its clock), so its notes are chosen by where they SOUND
        T["gr"] = [n for n in T["gr"] if not (sb * 16 + 3 <= round(n["at"] * 4) < (sb + 1) * 16 + 3) or (round(n["at"] * 4) - 3) % 16 in hits]
    if LETGO:                            # v11: the band's last hit, and the guitars and bass hold the open F and let it die
        hold = float(LETGO.split(";")[0])
        fill(74, "toms")
        drum("c", 74 * 16, 0.9)
        drum("k", 74 * 16, 0.95)
        for tr in ("gl", "gr"):
            add(tr, 74 * 16, hold * 4, F1, 0.9)
        add("bass", 74 * 16, (2.5 if PULSE else 8) * 4, F1, 0.9)
    # let go: the heavy guitars stop; two clean guitars tick the riff, the right one drifting from a quarter to half a bar
    # ahead; the swarm (sixteen oscillators finding a common phase) locks as they arrive
    if DRIFT:
        roots = [int(x) for x in DRIFT.split(";")[0].split(",")]
        edges = [74, 80, 86, 92, 98]
        lvl = lambda b: 0.8 + 0.3 * (b - 74) / 23
        for r, b0, b1 in zip(roots, edges, edges[1:]):
            for tr in TICKS:
                riff(tr, b0, b1, vel=0.5, up=TICK_UP + r, clean=True, ramp=(lvl(b0), lvl(b1 - 1)))
            T.setdefault("home", []).append({"at": b0 * 4, "len": (b1 - b0) * 4 + 0.2, "pitch": nm(F1 + r), "vel": 0.55})
            for iv in (12, 19):
                T.setdefault("air", []).append({"at": b0 * 4, "len": (b1 - b0) * 4 + 0.2, "pitch": nm(F1 + r + iv), "vel": 0.45})
        if PEND:
            pendulum(74, 80)
            T["tick"] = [{"at": 0, "len": 2.0, "pitch": "rb", "vel": 0.47}, {"at": 2, "len": 2.0, "pitch": "rb", "vel": 0.42}]   # one tick-tock: the pattern the Risset rhythm turns
            pendulum(96, 98)
        pv = float(DRIFT.split(";")[2])
        for b in range(86, 98):
            drum("k", b * 16, 0.4 + 0.03 * (b - 86))
            if b >= 92:
                drum("k", b * 16 + 8, 0.35 + 0.03 * (b - 86))
                if not PULSE:
                    T.setdefault("bass", []).append({"at": b * 4, "len": 3.9, "pitch": nm(F1 + 7), "vel": round(pv + 0.04 * (b - 92), 3)})
        if PULSE:                            # v18: the heartbeat under the drift
            p0, kv, hv = int(PULSE.split(";")[0]), float(PULSE.split(";")[3]), float(PULSE.split(";")[4])
            for r, b0, b1 in zip(roots, edges, edges[1:]):
                for b in range(max(b0, p0), b1):
                    for e in range(8):
                        add("bass", b * 16 + e * 2, 1.3, F1 + 12 + r, 0.6 if e % 2 == 0 else 0.5)
                    for e in range(0, 8, 2 if b < 86 else 1):
                        drum("h", b * 16 + e * 2, hv if e % 2 == 0 else hv * 0.8)
                    if b < 86:
                        drum("k", b * 16, kv)
        for i, t in enumerate(range(96 * 16, 98 * 16 - 8, 4)):
            drum("ft", t, 0.4 + 0.05 * i)
    else:
        for tr in TICKS:
            riff(tr, 74, 98, vel=0.5, up=TICK_UP, clean=True, ramp=(0.8, 1.1))
        pendulum(74, 98)
        for b in range(86, 98):
            drum("k", b * 16, 0.4 + 0.03 * (b - 86))
        T.setdefault("home", []).append({"at": 74 * 4, "len": 96.2, "pitch": "F1", "vel": 0.55})
        for n in ("F2", "C3"):
            T.setdefault("air", []).append({"at": 74 * 4, "len": 96.2, "pitch": n, "vel": 0.45})
    for n in ("F3", "C4"):
        T.setdefault("swarm", []).append({"at": 74 * 4, "len": 96.0, "pitch": n, "vel": 0.7})
    if LOCK and EARLY:                   # v12: the lock is heard before it lands: both heavy guitars, chugs only, half a bar apart
        riff("gl", LOCK_BAR, 98, vel=0.85, only=CHUGS)
        riff("gr", LOCK_BAR, 98, vel=0.85, only=CHUGS)
    fill(98)
    # against: half a bar apart. Every sixteenth has one guitar on it
    riff("gl", 98, 122, vel=0.9)
    riff("gr", 98, 122, vel=0.9)
    if FOUR:                             # v25: each clock has two guitars
        f0, f1 = (int(x) for x in FOUR.split(";")[3].split(":"))
        riff("gl2", f0, f1, vel=0.9)
        riff("gr2", f0, f1, vel=0.9)
        # the right clock is half a bar ahead, so what is written from the bar line sounds half a bar before it: the
        # main right guitar has always come in there (a pickup into the landing); its double waits for the landing
        T["gr2"] = [n for n in T["gr2"] if n["at"] >= f0 * 4 + 2]
        if BRAID and f0 <= 114 and f1 >= 118:
            sing_the_lock()
    bass(98, 122, 8, vel=0.95)
    groove(98, 122, 8, snare=(4, 12), cym="x")
    for b in range(102, 122, 4):
        drum("c", b * 16, 0.85)
    if SHAKE:                            # v18: the lock is shaken and holds: the beat thins as in the other slips, the bass keeps the left guitar
        s0, s1 = _sb, _sb + 2 * _sn
        for tr in ("kick", "snare", "cym", "hat", "ride", "toms", "bass"):
            T[tr] = [n for n in T.get(tr, []) if not (s0 * 4 <= n["at"] < s1 * 4)]
        bass(s0, s1)
        for b in range(s0, s1):
            drum("k", b * 16, 0.85)
            for q in range(0, 16, 4):
                drum("h", b * 16 + q, 0.45)
        fill(s1, "toms")                 # (the crash on the bar it holds is the section's own)
    if MACHINE:                          # v30: the band's last four bars
        m0, m1 = (int(x) for x in MACHINE.split(";")[0].split(":"))
        whole_machine(m0, m1, MACHINE.split(";")[1], *(float(x) for x in MACHINE.split(";")[2:4]))
    if VOICE:
        for i in range(4):                       # in step: the four lines, together
            say(i, 16 + 2 * i, one=bool(HEARD))
        for i in range(4):                       # a quarter apart: the four lines, each syllable said twice a beat apart
            say(i, 60 + 2 * i)
        say(2, 68)
        say(3, 70)
        for b0 in (102, 110, 118):               # against: the last line, four times round, the two voices interlocked
            for k in range(4):
                say(3, b0 + k, "bark", ring=(k == 3))
    # two clocks: the guitars alone, still against each other; then only the ticks
    riff("gl", 122, 126, vel=0.85)
    riff("gr", 122, 126, vel=0.85)
    drum("c", 122 * 16, 0.9)
    if CLOCKS:
        tv, kv = [float(v) for v in CLOCKS.split(";")[2].split(":")]
        # both clocks are WRITTEN alike (tick on one, tock on three); the right one is on the right guitar's clock (`warp`),
        # half a bar ahead by now, so its tock falls where the left one ticks: nothing is placed by hand. The last
        # instant of the song (bar 130's first beat) is the left clock's tick and the right clock's tock, together.
        for b in range(122, 131):
            for tr in ("pl", "pr"):
                T.setdefault(tr, []).append({"at": b * 4, "len": 0.5, "pitch": "C5", "vel": tv})
                if b < 130 or tr == "pr":
                    T.setdefault(tr, []).append({"at": b * 4 + 2, "len": 0.5, "pitch": "F4", "vel": kv})
    elif not END:
        pendulum(122, 130)
    if END:                              # v17: the two music boxes run down
        nt, slow, bv, total = [float(v) for v in END.split(";")]
        t0, x0, span = 126 * 4, nt * 4, 16 - nt * 4
        late = lambda x: x if x <= x0 else x + slow * (x - x0) ** 3 / (3 * span ** 2)       # a beat's place once the spring runs down
        for tr in TICKS:
            k = len(T.get(tr, []))
            riff(tr, 126, 130, vel=bv, up=TICK_UP, clean=True, ramp=(1.0, 0.6))
            add(tr, 130 * 16, 16, F1 + TICK_UP, bv * 0.6)                               # one last F, on what would have been the bar line
            for n in T[tr][k:]:
                x = n["at"] - t0
                n["len"] = round(n["len"] * (1 + slow * (max(0.0, x - x0) / span) ** 2), 4)
                n["at"] = round(t0 + late(x), 4)
        T.setdefault("home", []).append({"at": 126 * 4, "len": total - 126 * 4 - 2, "pitch": "F1", "vel": 0.5})
    else:
        for tr in TICKS:
            riff(tr, 126, 130, vel=0.32 if BOX else 0.45, up=TICK_UP, clean=True, ramp=(1.0, 0.6))     # (the boxes softer at the end: the two clocks are the point there)
        T.setdefault("home", []).append({"at": 126 * 4, "len": 16.0, "pitch": "F1", "vel": 0.5})
    if VARI:                             # v31: in the last slip before the hold a beat apart the right guitar's pitch goes with its clock
        lean("gr")
    if FAST:                             # v35: and the right-hand music boxes' pitch goes with their clock, in every slip and through the drift
        run_sharp()
    if SHOOK:                            # v38: the shake is heard on the two clocks
        shake_on_the_clocks()
    if FLOOR:                            # v37: two slow voices in the drift, a line each
        the_floor_moves()
    if WALL and TWIN:                    # v32: the left guitar's notes in those bars are played behind the wall
        w0, w1 = (int(v) for v in WALL.split(";")[0].split(":"))
        T["wl"] = [n for n in T["gl"] if w0 * 4 <= n["at"] < w1 * 4]
        T["gl"] = [n for n in T["gl"] if not (w0 * 4 <= n["at"] < w1 * 4)]
    for bar_, semi in stood():           # v34: each guitar on its own clock, so the right one gets to each ground a beat early
        for tr in ("gl", "gr", "bass"):
            for n in T[tr]:
                if bar_ * 4 <= n["at"] < (bar_ + 1) * 4:
                    n["pitch"] = nm(NAMES.index(n["pitch"][:-1]) + 12 * (int(n["pitch"][-1]) + 1) + semi)


# the heavy rig: Common Time's tight rig on the engine's own cabinet (sounds.md), one a side
HEAVY = (" fx.0.mix=0 synth.layers.0.soft=expr.pm fx.2.tight=220 fx.3.mix=0"
         + "".join(f" fx.4.bands.{i}.gain=0dB" for i in range(7)))
CLEAN = "ct-clean synth.layers.0.inharm=0.00008"
DRIP = {"type": "reverb", "kind": "spring", "drip": 1, "decay": "1.8s", "mix": 0.22}     # the spring that drips (engine feature 5)
# the swarm, as in Common Time: sixteen saws to a note pulled toward a common phase by a coupling the `sync` lane sets
SWARM = {"about": "chirper-zero: the swarm - sixteen saws to a note, each at its own pitch (60 cents' spread), pulled toward their common phase by a coupling the track's `sync` lane sets (0 a crowd, 1 the critical point, 3 locked); a low-pass opens as they agree. As in Common Time (track 1).",
         "synth": {"layers": [{"type": "kuramoto", "kuramoto": {"count": 16, "spread": 60, "coupling": {"value": 0, "mod": [{"src": "auto.sync", "amount": 1}]}}}],
                   "filters": [{"kind": "lp", "cutoff": {"value": 350, "mod": [{"src": "sync", "amount": 2.6}]}}], "amp": {"a": "1.5s", "d": 0, "s": 1, "r": "3s"}}, "gain": "-9.5dB"}


def risset_tick():
    """The Risset pendulum's track settings. With two copies the one at the written speed starts a cycle alone, part-way
    through the pattern; the track starts early by just as much as puts its first tick on bar 80's bar line (and so on
    every fourth bar line after, where the cycle comes round)."""
    c, k = DRIFT.split(";")[1].split(":")
    c, k = float(c), int(k)
    assert k == 2, "the hand-over to the plain pendulum is seamless only with two copies"
    L = 4.0                                                    # the pattern: a tick and a tock, four beats
    p0 = (0.5 * c / math.log(2)) % L                           # where in the pattern the written-speed copy starts
    lead = c * math.log2(1 + (L - p0) / (c / math.log(2)))     # beats until its first tick
    return {"at": f"{80 * 4 - lead:.4f}b", "risset": {"cycle": f"{c:g}b", "layers": k, "length": f"{16 * 4 + lead:.4f}b"}}


def song():
    compose()
    cab = lambda cone: [{"type": "cab", "model": "4x12-modern", "mic": 0.25, "distance": 0.15, "cone": cone}]
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    b = lambda bar: f"{bar * 4}b"
    eb, hlp = ([float(x) for x in EIGHTH.split(";")[3:5]] if EIGHTH and len(EIGHTH.split(";")) > 4 else (0, 0))
    vo = VOICE.split(";") if VOICE else None
    hd = HEARD.split(";") if HEARD else None
    sn = SNARE.split(";") if SNARE else None
    lowride = [["0b", 0]]                    # the bass bus's fader by section, after its compressor (a key moves the low end)
    for seg in (LOWRIDE.split(",") if LOWRIDE else []):
        b0, b1, db = [float(x) for x in seg.split(":")]
        lowride += [[f"{b0 * 4 - 1:g}b", 0], [f"{b0 * 4:g}b", db], [f"{b1 * 4 - 1:g}b", db], [f"{b1 * 4:g}b", 0]]
    if LETGO:                                # the bass's held F dies with the guitars'
        if PULSE:                            # v18: the bass comes back as the heartbeat, low, and rises into the landing
            lowride += [[f"{74 * 4}b", 0], [f"{76 * 4}b", -float(LETGO.split(";")[3])], [f"{int(PULSE.split(';')[0]) * 4 - 1}b", -float(LETGO.split(";")[3])],
                        [f"{int(PULSE.split(';')[0]) * 4}b", float(PULSE.split(";")[1])], [f"{92 * 4}b", float(PULSE.split(";")[2])], [f"{98 * 4}b", 0]]
        else:
            lowride += [[f"{74 * 4}b", 0], [f"{76 * 4}b", -float(LETGO.split(";")[3])], [f"{88 * 4}b", -float(LETGO.split(";")[3])]]
            lowride += [[f"{92 * 4}b", float(LOCK.split(";")[2])], [f"{98 * 4}b", 0]] if LOCK else [[f"{90 * 4}b", 0]]      # v12: the bass's pedal swells into the lock
    lowride = lowride if len(lowride) > 1 else None
    key_lane = [["0b", 0]]                   # v23: the ground under the bass's eq, semitones over F
    for seg in (KEYEQ.split(",") + [f"{b_}:{b_ + 1}:{semi}" for b_, semi in stood()] if KEYEQ else []):
        k0, k1, semi = [float(x) for x in seg.split(":")]
        if key_lane[-1][0] == f"{k0 * 4:g}b":     # one hold straight into the next
            key_lane = key_lane[:-2] + [[f"{k0 * 4 - 0.02:g}b", key_lane[-2][1]], [f"{k0 * 4:g}b", semi]]
        else:
            key_lane += [[f"{k0 * 4 - 0.02:g}b", 0], [f"{k0 * 4:g}b", semi]]
        key_lane += [[f"{k1 * 4 - 0.02:g}b", semi], [f"{k1 * 4:g}b", 0]]
    talkfx = ([TALKFX] if TALKFX else []) + ([{"type": "eq", "bands": TALKEQ.split("|")}] if TALKEQ else [])
    sg = SUNG.split(";") if SUNG and HEARD and VOICE else None
    s2 = SUNG2.split(";") if SUNG2 and sg else None
    pump = [{"type": "pump", "on": tr, "depth": f"-{(sg[2] if sg else hd[3].split(':')[0]) if tr == 'tc' else hd[4]}dB", "attack": "4ms", "hold": hd[3].split(":")[1], "release": hd[3].split(":")[2]}
            for tr in ("tc", "tl", "tr")] if VOICE and HEARD and float(hd[3].split(":")[0]) else []
    dtop = [f"lp cutoff={DTOP.split(';')[0]} q={DTOP.split(';')[1]}"] if DTOP else []
    tw = TWIN.split(";")[0].split(":") if TWIN else None
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff={} q={} gain={}dB".format(*MIDS.split(":"))]}]} if MIDS else {}
    fo = FOUR.split(";")[0].split(":") if FOUR else None
    mic = f" fx.2.mic={MIX.split(';')[0]}" if MIX else ""
    beam = TWIN.split(";")[1].split(":") if TWIN else None
    spec = [
        *([{"name": "gl", "patch": f"{tw[0]}{mic} fx.2.cone={tw[1]}", "gain": f"{tw[3]}dB", "pan": -1, "out": "gtrs", **mids},
           {"name": "gr", "patch": f"{tw[0]}{mic} fx.2.cone={tw[2]}", "gain": f"{tw[3]}dB", "pan": 1, "out": "gtrs", **mids, "warp": WARP},
           *([{"name": "gl2", "patch": f"{tw[0]} fx.1.model={fo[0]} fx.2.mic={fo[1]} fx.2.cone={fo[2]}", "gain": f"{float(tw[3]) + float(FOUR.split(';')[1]):g}dB",
               "pan": -float(FOUR.split(";")[2]), "out": "gtrs", **mids},
              {"name": "gr2", "patch": f"{tw[0]} fx.1.model={fo[0]} fx.2.mic={fo[1]} fx.2.cone={fo[3]}", "gain": f"{float(tw[3]) + float(FOUR.split(';')[1]):g}dB",
               "pan": float(FOUR.split(";")[2]), "out": "gtrs", **mids, "warp": WARP}] if FOUR else [])] if TWIN else
          [{"name": "gl", "patch": "ct-chug-l" + HEAVY, "gain": "3.3dB", "pan": -1, "out": "gtrs", "fx": cab(12)},
           {"name": "gr", "patch": "ct-chug-r" + HEAVY, "gain": "3.3dB", "pan": 1, "out": "gtrs", "fx": cab(13), "warp": WARP}]),
        *([{"name": tr, "patch": BOX.split(";")[0], "gain": BOX.split(";")[2], "pan": sgn * float(BOX.split(";")[3]), "sends": {"hall": BOX.split(";")[4]},
            **({"fx": [{**DRIP, "mix": float(BOX.split(";")[5])}]} if float(BOX.split(";")[5]) else {}), **({"warp": WARP} if tr == "mr" else {})}
           for tr, sgn in (("ml", -1), ("mr", 1))] if BOX else
          [{"name": "cl", "patch": CLEAN, "gain": "1dB", "pan": -0.7, "sends": {"hall": "-9dB"}, "fx": [DRIP]},
           {"name": "cr", "patch": CLEAN, "gain": "1dB", "pan": 0.7, "sends": {"hall": "-9dB"}, "fx": [DRIP], "warp": WARP}]),
        *([{"name": tr, "patch": SLIPCLOCK.split(";")[0], "gain": SLIPCLOCK.split(";")[1], "pan": sgn * float(SLIPCLOCK.split(";")[2]),
            "sends": {"hall": SLIPCLOCK.split(";")[5]}, "fx": [{**DRIP, "mix": float(SLIPCLOCK.split(";")[6])}],
            **({"warp": WARP} if tr == "br" else {})} for tr, sgn in (("bl", -1), ("br", 1))] if SLIPCLOCK else []),
        *([{"name": tr, "patch": CHIME.split(";")[1], "gain": CHIME.split(";")[2], "pan": sgn * float(CHIME.split(";")[3]),
            "sends": {"hall": CHIME.split(";")[4]}, "fx": [{**DRIP, "mix": float(CHIME.split(";")[5])}],
            **({"warp": WARP} if tr == "er" else {})} for tr, sgn in (("el", -1), ("er", 1))] if CHIME else []),
        *([{"name": "tc", "patch": "voice-talk", "gain": sg[1], "pan": 0, "sends": {"hall": sg[4]},
            "fx": [{"type": "eq", "bands": sg[6].split("|")}, "reverb kind={} decay={} mix={} predelay=6ms".format(*sg[3].split(":"))]}]
          + ([{"name": tr, "patch": sg[5].split(":")[0], "gain": sg[5].split(":")[1], "pan": sgn * float(sg[5].split(":")[2]), "sends": {"hall": sg[4]},
               "fx": [{"type": "eq", "bands": sg[6].split("|")}, "reverb kind={} decay={} mix={} predelay=6ms".format(*sg[3].split(":"))]}
              for tr, sgn in (("sl", -1), ("sr", 1))] if sg[5] else []) if sg else
          [{"name": "tc", "patch": "voice-talk", "gain": hd[0], "pan": 0, "fx": talkfx}] if VOICE and HEARD else []),
        *([{"name": tr, "patch": "voice-talk", "gain": s2[0] if s2 else hd[1] if HEARD else vo[0], "pan": sgn * float(hd[2] if HEARD else vo[2]),
            **({"sends": {"hall": s2[1]}} if s2 else {}),
            "fx": [{"type": "eq", "bands": sg[6].split("|")}, "reverb kind={} decay={} mix={} predelay=6ms".format(*sg[3].split(":"))] if s2 else talkfx,
            **({"warp": WARP} if tr == "tr" else {})} for tr, sgn in (("tl", -1), ("tr", 1))] if VOICE else []),
        *([{"name": tr, "patch": "kidman synth.layers.0.diction=2 synth.layers.0.speech=1",
            "gain": f"{float(vo[1][:-2]) + float(FOUR.split(';')[4]):g}dB" if FOUR and len(FOUR.split(";")) > 4 else vo[1], "pan": sgn * float(vo[2]), "sends": {"hall": vo[3]},
            "fx": [{"type": "eq", "bands": ["hp cutoff=440", "peak cutoff=1400 q=0.8 gain=4.5dB", "peak cutoff=5500 q=1.2 gain=-4dB", "highshelf cutoff=7000 gain=-6dB"] + dtop}],      # the bark's hiss falls with the kit's top
            **({"warp": WARP} if tr == "vr" else {})} for tr, sgn in (("vl", -1), ("vr", 1))] if VOICE else []),
        {"name": "bass", "patch": "ct-bass", "gain": {"value": "0.5dB", "mod": [{"src": "auto.hold", "amount": 1}]} if EIGHTH and eb else "0.5dB", "pan": 0, "out": "low",
         **({"auto": {"hold": {"points": [["0b", 0], [b(35.9), 0], [b(36), eb], [b(48), eb], [b(48.1), 0]], "curve": 0}}} if EIGHTH and eb else {})},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        ({"name": "snare", "patch": kit, "gain": sn[2], "out": "drums", "sends": {"oh": sn[1] + "dB", "snr": sn[3].split(":")[1] + "dB"},
          "fx": [{"type": "eq", "bands": [f"highshelf cutoff={sn[0].split(':')[1]} gain={sn[0].split(':')[2]}dB"]}]} if SNARE else
         {"name": "snare", "patch": kit, "gain": "8dB", "out": "drums", "sends": {"oh": "-1.5dB"}}),
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": f"{-3 + (float(MIX.split(';')[1]) if MIX else 0):g}dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"},
         "fx": [{"type": "eq", "bands": air[0]["bands"] + [f"lp cutoff={hlp:g} q=0.7"]}] if EIGHTH and hlp else air},
        {"name": "ride", "patch": kit, "gain": "6dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "tick", "patch": kit, "gain": "6dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air, **risset_tick()}] if DRIFT and PEND else []),
        {"name": "home", "patch": "contrabass-tight", "gain": "-9dB", "pan": 0.3, "sends": {"hall": "-12dB"}},
        {"name": "air", "patch": "juno-pad", "gain": "-13dB", "pan": 0.15, "sends": {"hall": "-8dB"}},
        *([{"name": tr, "patch": "ot-clock", "gain": CLOCKS.split(";")[0], "pan": sgn * float(CLOCKS.split(";")[1]), "sends": {"hall": CLOCKS.split(";")[3]},
            **({"warp": WARP} if tr == "pr" else {})} for tr, sgn in (("pl", -1), ("pr", 1))] if CLOCKS else []),
        {"name": "swarm", "patch": "ot-swarm", "gain": {"value": "-14dB", "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0, "sends": {"hall": "-8dB"},
         "auto": {"sync": {"points": [["0b", 0.3], [b(74), 0.3], [b(90), 1.0], [b(95), 1.4], [b(96), 3], [b(NB), 3]]},
                  "lvl": {"points": [["0b", 0], [b(74), -6], [b(80), 2], [b(96), 4], [b(98), -6], [b(NB), -6]]}}},
        # v32: the left guitar behind the wall: the same guitar, amplifier, cone, fader and place as `gl`, with a
        # low-pass after it whose cutoff the lane `wall` opens (in octaves over its starting place) to 16 kHz
        *([{"name": "wl", "patch": f"{tw[0]}{mic} fx.2.cone={tw[1]}", "gain": f"{tw[3]}dB", "pan": -1, "out": "gtrs",
            "fx": mids.get("fx", []) + [{"type": "filter", "kind": "lp", "q": float(WALL.split(";")[3]),
                                          "cutoff": {"value": float(WALL.split(";")[1]), "mod": [{"src": "auto.wall", "amount": 1}]}}],
            "auto": {"wall": {"curve": 0, "points": [["0b", 0], [b(int(WALL.split(";")[0].split(":")[0])), 0],
                                                      [b(float(WALL.split(";")[2])), round(math.log2(16000 / float(WALL.split(";")[1])), 3)],
                                                      [b(NB), round(math.log2(16000 / float(WALL.split(";")[1])), 3)]]}}}] if WALL and TWIN else []),
        # v37: the drift's two slow voices, left and right, the right one on the right-hand clock
        *([{"name": tr, "patch": FLOOR.split(";")[2], "gain": FLOOR.split(";")[3], "pan": sgn * float(FLOOR.split(";")[4]), "sends": {"hall": FLOOR.split(";")[5]},
            "fx": [{"type": "eq", "bands": FLOOR.split(";")[6].split("|")}], **({"warp": WARP} if tr == "fr" else {})}
           for tr, sgn in (("fl", -1), ("fr", 1))] if FLOOR else []),
    ]
    tracks = []
    for t in spec:
        if t["name"] in T:
            tracks.append({**t, "notes": sorted(T[t["name"]], key=lambda n: n["at"])})
    return {
        "about": ("chirpers X (Common Time), track 2 by chirper-zero: \"Odd Sympathy\". One riff, one bar long, on two guitars, left "
                  "and right, each with its own clock. They start in step; the right one slips ahead a sixteenth at a time (the "
                  "engine's track warp), holding at each distance, until it is half a bar ahead, exactly against the left, and "
                  "there the riff's two halves fit: every sixteenth has one guitar on it and never both. After Huygens's two "
                  "pendulum clocks on one beam (1665), which always ended swinging against each other. v1: the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": float(SHOOK.split(";")[5]) if SHOOK and SHOOK.split(";")[5] else float(MACHINE.split(";")[4]) if MACHINE and float(MACHINE.split(";")[4]) != -10 else -10, "seed": 1, "tail": "4s", "length": f"{int(float(END.split(';')[3])) if END else NB * 4 + (4 if CLOCKS else 0)}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    "ot-swarm": SWARM,
                    **({"ot-clock": {"about": "chirper-zero: a clock's tick - a drum machine's rim-shot circuit (the `machine` layer, part rim), 16-20 ms long; it follows the note's pitch (C5 the tick, F4 the tock)",
                                     "synth": {"amp": {"a": "0.1ms", "d": "0s", "r": "300ms"}, "layers": [{"type": "machine", "machine": {"part": "rim"}}]}}} if CLOCKS else {})},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB"] + dtop}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6"] + ([{"type": "eq", "bands": dtop}] if DTOP else [])},
            **({"snr": {"fx": [{"type": "eq", "bands": [f"peak cutoff={SNARE_EQ.split(':')[0]} q={SNARE_EQ.split(':')[1]} gain={SNARE_EQ.split(':')[2]}dB"]}]}} if SNARE else {}),
            "gtrs": {**({"auto": {"go": {"points": [["0b", 0], [f"{74 * 4}b", 0], [f"{(74 + float(LETGO.split(';')[2])) * 4:g}b", -float(LETGO.split(";")[1])],
                                                    *([[f"{(LOCK_BAR - 0.75) * 4:g}b", -float(LETGO.split(";")[1])], [f"{(LOCK_BAR - 0.5) * 4:g}b", float(LOCK.split(";")[1].split(":")[0])],
                                                       [f"{98 * 4 - 0.125:g}b", float(LOCK.split(";")[1].split(":")[1])], [f"{98 * 4}b", 0]] if LOCK and EARLY else
                                                      [[f"{96 * 4}b", -float(LETGO.split(";")[1])], [f"{97 * 4}b", 0]])], "curve": 0}}} if LETGO else {}),
                     "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.go", "amount": 1}]} if LETGO else "0dB"}]
                           + ([{"type": "eq", "bands": [f"peak cutoff={GBODY.split(':')[0]} q={GBODY.split(':')[1]} gain={GBODY.split(':')[2]}dB"]}] if GBODY else []) + ([f"reverb kind={beam[0]} decay={beam[1]} mix={beam[2]} predelay=6ms"] if TWIN else [])
                     + (pump if HEARD else [{"type": "duck", "by": "tl", "depth": f"-{vo[4]}dB", "attack": "20ms", "release": "250ms"}] if VOICE and float(vo[4]) else [])},
            "low": {"fx": ([{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                     {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                            {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                            {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}] if KEYEQ else
                           [{"type": "eq", "bands": ["peak cutoff=44 q=1.5 gain=-7dB", "peak cutoff=90 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                            {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                            {"type": "eq", "bands": ["peak cutoff=170 q=1.2 gain=-3dB"]}])
                           + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}}] if lowride else []),
                    **({"auto": {**({"ride": {"points": lowride, "curve": 0}} if lowride else {}), **({"key": {"points": key_lane, "curve": 0}} if KEYEQ else {})}} if lowride or KEYEQ else {})},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": f"{1.6 + (float(TWIN.split(';')[2]) if TWIN else 0) + (float(SNARE.split(';')[4]) if SNARE and SNARE.split(';')[4:] else 0) + (float(MIX.split(';')[3]) if MIX else 0) + V14_MAKEUP:g}dB"}]},
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
