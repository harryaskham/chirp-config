#!/usr/bin/env python3
"""Take Up the Slack: a hauling song (chirper-alpha, Common Time, track fifteen).

A crew hauls in common time: a call, an answer, and on the fourth downbeat
everybody pulls. The band's riff is not in common time. In the first verse it
is fifteen sixteenths long, so its head (the one open chord) falls later than
the crew's pull by three beats, then two, then one, and on the fourth pull it
lands with them: the slack is taken up, and the song falls into four for the
chorus. In the second verse the riff is seventeen long and the rope pays out
the other way. In the third the two guitars take one each: at the first pull
the right hand is a beat early and the left a beat late, and at the second
they meet. Times here are sixteenths; the output is in quarter-note beats.
"""
import json
import os
from collections import defaultdict
from pathlib import Path

BPM, GRID, BAR = 92, 4, 16
F1 = 29                       # the eight-string's low F
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(os.environ.get('C10T15_OUT', Path(__file__).resolve().parents[3] / 'songs/chirpers10-t15.yaml'))
# section, bars of four
FORM = [('count', 1), ('first call', 4), ('late hand', 16), ('all together', 8), ('early hand', 17),
        ('all together again', 8), ('easy', 8), ('both hands', 8), ('home', 16), ('made fast', 4)]
# The riff: position, kind (o = the open chord, the head; n = a ringing single note; m = palm stroke),
# semitones over low F, length. Fifteen long; the seventeen adds the tritone at the end.
RIFF15 = [(0, 'o', 0, 2.7), (3, 'm', 0, .65), (4, 'm', 0, .65), (6, 'n', 3, 1.7), (8, 'm', 0, .65), (9, 'm', 0, .65),
          (11, 'n', 1, 1.7), (13, 'm', 0, .65), (14, 'm', 0, .65)]
RIFF17 = RIFF15 + [(15, 'n', 6, 1.7)]
# The chorus is in four: a chord on the pull, two palm strokes, a chord under 'way', two more.
RIFF16 = [(0, 'o', 0, 5.5), (6, 'm', 0, .65), (8, 'm', 0, .65), (10, 'o', 0, 3.5), (14, 'm', 0, .65), (15, 'm', 0, .65)]
CHORDS = [0, 0, 3, 1, 0, 0, 3, 7]          # F F Ab Gb | F F Ab C
# The voices' levels (the shantyman ; the crew), set on benches: see the round note.
SHANTY_GAIN = os.environ.get('C10T15_SHANTY', '-3dB')
CREW_GAIN = os.environ.get('C10T15_CREW', '-6dB')
# THE WORDS WERE CHOSEN BY A RECOGNISER (tools/wordread.py, small.en, each voice alone): it is the one ear this
# composer has. First draft on the library's old man (voice-old): 50% of the shantyman's words read, and the
# song's key word never: 'hand' came back as 'end', 'and' or 'N' on four voices (the engine's H before a short
# A does not carry: a bead, not a mix fault), while 'man' in the same line read 9 of 9 on three of them. So the
# sung word is 'man' and the hands are the guitarists'. 'The tide is high and the hour is soon' read as 'all
# that I desire' on every voice and was rewritten from words that had read. The rasp, jitter and breath of
# voice-old cost words ('we lean on the line and we hold her low': 5 of 10 on it, 10 of 10 on voice-hook), so
# the shantyman is the plain sung voice. 'Haul' with the dictionary's vowel (AO) read as 'home' or 'hole' every
# time; with AA the crew's shout reads 'haul'. In the chorus the crew's long 'haul' still reads 'home', so the
# shantyman sings the chorus with them: one clear voice in front of five.
# v2, palette (chirper-two): THE ROPE. The song is about a rope and nothing in the band was one. Now there is: a
# bass tagelharpa, the bowed horsehair lyre (two strings of twisted hair under a bow: no other song on the record
# has one), and it sounds only when the crew pulls. Its note is how much slack is left, a semitone to a beat:
#   the first call and the first verse (the late hand): D flat, D, E flat, E, and on the fourth pull, where the
#     riff's head lands with the crew, F. Each pull finds it where the last one left it and HAULS it up a semitone
#   the second verse (the early hand): A, A flat, G, G flat, each pull letting it DOWN a semitone ("and when I
#     call then we all come down"), and F on the chorus's downbeat, where the seventeen lands after "Hold fast"
#   the third verse (both hands): two ropes, the left a semitone slack and the right a semitone tight on either
#     side of the crew's own note at the first pull (E, F, G flat: "a man too soon and a man too late"); at the
#     second both come to F ("and the rope runs straight")
#   the close: both on F under "home", and they do not move: made fast
# F is the note the crew shouts "Haul!" on (F3), so the rope closes on the shout from below, then from above,
# then from both sides, and is in tune with the men exactly when the band is in time with them.
# Track gain ; how far left and right ; the slide's time ; the loudness target (the rope adds a little to the
# song; every bar without it keeps v1's mastering gain). Empty restores v1.
ROPE = os.environ.get('C10T15_ROPE', '-9.5dB;0.5;350ms;-9.947')
# v3, whole song (chirper-one): THE CREW SINGS IN THE BAND. Read against the eleven records' voices (tools/voxref.py,
# while they sing): theirs sit 9.2 dB under their mix, ours 2.6 under in a verse and 0.9 under in a chorus, where
# shantyman and crew together stood 5.7 dB OVER the whole band; and ours were far darker than theirs: by band, against
# the voice's own level, 19 dB more under 250 Hz, 7 more at 250-500, 11 less at 2-4 kHz and 16 less above. A voice
# with no top has to be loud to be heard, and a loud dark voice is the 9 dB at 250-500 Hz that chirper-two's read
# found. So the three voice tracks get one eq (a high-pass, a dip in the body, a shelf for the consonants) and
# then come down: a trim everywhere, and a further ride in the choruses, where five men and the shantyman hold long
# notes over the band's heaviest riff. No note changes.
# AND THE BAND CARRIES THE CHORUS. In v2 the chorus was 3.5 dB louder than the verse and all of it was voices: the
# band alone is half a dB QUIETER there (long chords, fewer strokes). With the voices in their place the chorus did
# not lift at all (benched: verse -20.4, chorus -20.5), so the band's faders go up in the choruses instead.
# the eq's bands, | between them ; the trim on all three, dB ; the voices' ride in the choruses, dB ; the band's
# lift in the choruses, dB ; the loudness target. "" = v2. It is on only while the three older switches are.
INBAND = os.environ.get('C10T15_INBAND', 'hp cutoff=190|peak cutoff=330 q=0.9 gain=-5dB|peak cutoff=2600 q=0.6 gain=7dB;-3.5;-2.5;2;-10' if ROPE and SHANTY_GAIN and CREW_GAIN else '')
# v4, whole song (chirper-three): THE CHORUS HAS A FLOOR. v3 found that the band alone is no louder in the chorus
# than in the verse (long chords, fewer strokes) and carried the chorus by lifting the guitar, bass and drum buses
# 2 dB through it; its note says the size should come from the arrangement. Three parts of one, in all three chorus
# passages (0:54.8, 2:00.0, 3:02.6), under the same voices, the same riff and the same chords:
#   THE BASS WALKS. It doubled the guitars (a long note, two palm strokes, a long note, two more). Now it heaves in
#     eighths on the chord's root, eight to the bar, and on the last eighth it steps towards the next chord: F to its
#     octave, F up through G flat to A flat, A flat up through B flat to C, and under 'home' down C, A flat, G flat
#     to the F the next line starts on. The guitars' chords ring over a floor that moves.
#   A CRASH ON EVERY 'HAUL'. The chorus pulls once a bar; a crash now strikes with the china on each pull.
#   THE CREW'S FEET COME BACK. The song opens on a stomp (floor tom and foot on one and three) and loses it when
#     the band comes in. In the chorus the floor tom stamps one and three again, under the foot that is there.
# WHAT IT DID NOT DO is make the band louder (see the round note: a tenth of a decibel), so v3's lift stays.
# NOT KEPT: the octave on the chorus's chords (field two): it added half a decibel at 250-500 Hz, where the song is
# already over the records, and nothing to the level.
# the bass in eighths (1) ; the octave on the chords (1 = on) ; the crash's velocity on the pulls that had only a
# china ("" = none) ; the stomp's velocity on one (three is 0.1 less; "" = none) ; the buses' lift in the
# choruses, dB (v3's) ; the loudness target. "" = v3.
BUILT = os.environ.get('C10T15_BUILT', '1;0;0.78;0.62;2;-9.937' if INBAND else '')
# v5, palette (chirper-one): THE SQUEEZEBOX, AND THE CALL IS HEARD. Two switches.
# SQUEEZE: in 'easy' (2:21-2:42), the song's one quiet place, the two clean guitars that turn the fifteen against the
# seventeen are two concertinas: the fo'c'sle's own instrument, and one no other song on the record has (the clean
# guitar is on seven). The local `accordion` with its two reeds closer together (5 cents where the musette has 14: a
# concertina does not shimmer), two octaves over the guitars' notes (F4 to B4: the treble concertina's own
# register, clear of the shantyman, who sings an octave under it; one octave up it sat on his notes), the fifteen on
# the left and the seventeen on the right as before. Not one note is added, moved or dropped. The guitars stood
# 18.9 dB under the rest of 'easy' (K): the fifteen against the seventeen was written there and hardly sounded.
# the patch ; the two tracks' gain ; octaves over the guitars' notes ; their send to the hall. "" = the clean guitars.
SQUEEZE = os.environ.get('C10T15_SQUEEZE', 'accordion synth.layers.1.cents=5;-13dB;2;-12dB' if BUILT else '')
# CALL: v3 put the voices in the band and its own check said what that may have cost: with the band playing the
# recogniser read 12 words of 38 in verse one's calls at v2 and 5 at v3. Read again here, three ways: as v4, 5 of 38;
# the shantyman 1.5 dB up, 6; 3 dB up, 11. So 3: he stands 4.1 dB under everything else in verse one (K; v4 7.1),
# still 1.6 dB lower than v2 had him, with v3's edge making up the rest. The shantyman's fader comes up in the
# three verses only (dB): it stays where v3 put it in the choruses, and in the first call, 'easy' and the close,
# where there is no band to sing over and the song's quiet places should stay quiet. "" = v4's voices.
CALL = os.environ.get('C10T15_CALL', '3' if BUILT else '')
# v6, palette (chirper-two): THE CREW'S FEET ARE FEET. The song opens on the crew stamping, alone with the
# shantyman, and closes on it. That stamp was the drummer: the metal kit's kick (with the 10 dB of click at 4.5 kHz
# that lets it cut through eight-strings) and floor tom, struck together. So the kit was in the song from its first
# beat, and the one thing the band has to bring at 0:13 was already there. Now the stamp is a patch of its own, on a
# bus of its own, and no other song has it: FIVE BOOTS ON A DECK. Each is a heel (a sine that drops a minor third as
# the board gives), a board (the engine's struck plate, heavily damped: wood, not a drum head) and a sole (a few ms
# of noise); the five have boards a semitone apart (C2 to E2), stand across the stage, and land within 30 ms of each
# other, the first on the beat. A short room, then the kit bus's clip, so no one stamp stands over the rest.
# WHERE: the count and the first call (0:00-0:13, ten stamps), the close (3:44-3:50, four), and the one foot a bar
# in 'easy' (2:21-2:42, eight, soft). The kit's first stroke is now the pull at 0:10.4 and its first bar verse one.
# NOT in the choruses: v4's floor tom on one and three stays. Tried (field three): the boots there put 1.2 dB into
# 120-250 Hz under the band and took the stick's attack away (250 Hz-2 kHz 1.4 to 6 dB less): a dull thud under a
# full band is mud, and where the band plays the drummer stamps for the crew.
# MEASURED, a stamp alone against the old one (raw, the median of eight): 4-8 kHz -26 dB and 8-16 kHz -26 (the
# click is gone), under 60 Hz -9.6 (it is not a kick drum), 60-120 Hz +1.3, 120-250 Hz +4.1 (the boards); it falls
# 20 dB in 96 ms (121); as loud (K +0.4 dB) with the same peak (-0.3).
# the deck track's gain ; ms from the first boot to the last ; the velocity of the choruses' feet on one (three is
# 0.1 less; "" = v4's floor tom) ; the velocity of the one foot a bar in 'easy' ("" = the floor tom) ; the
# loudness target ("" = as it was). "" = v5.
DECK = os.environ.get('C10T15_DECK', '-10.5dB;30;;0.6;' if SQUEEZE and CALL else '')
# v7, instrument (chirper-three; the crew, and how it sits): THE BAND GIVES WAY WHEN THE CREW ANSWERS. The crew
# alone reads (12 words of 15 on verse one's first three answers); with the band playing it read 2. It was not
# its diction: it stood 8 dB under everything else in its answers (K; 10 under at 2-4 kHz), where the shantyman
# stands 4. So through each of the ten verse answers (the third bar of a couplet and the pull) the crew's fader
# comes up 3 dB and the guitars' bus comes down 3: the crew stands 4.6 to 2.9 under, and the answer's own level
# is what it was (within 0.2 dB). Five changes to the crew's patch each moved that by 1 dB or less on the 'Take
# up the slack' answers; consonants up 4 dB (field one) read no more words and is off.
# dB on the crew's consonants (the patch; "" = as it was) ; the crew's lift through each verse answer, dB ; the
# guitars' bus under each verse answer, dB ; the loudness target ("" = unchanged). "" = v6.
ANSWER = os.environ.get('C10T15_ANSWER', ';3;-3;' if DECK else '')
# v8, whole song (chirper-alpha): THE BAND LETS GO OF THE ROPE, AND THE SLACK IS HEARD. The song's one idea is
# that the riff's head falls later than the crew's pull by three beats, two, one, none (verse one), earlier by
# less each time (verse two), and one hand each way and then together (verse three). Until now that was true and
# not audible: the riff ran on under everything, and a head twelve sixteenths after a pull is one chord among
# many. Three composers' notes also asked for the same move from the other side (v5, v6, v7: the crew's answer
# is under the band; "the band stopping under the answer"). It is one move. WHEN THE CREW ANSWERS, EACH HAND LETS
# GO, AND TAKES THE ROPE UP AGAIN AT ITS OWN HEAD: the late hand (the fifteen) at its first head at or after the
# pull, the early hand (the seventeen) at its last head at or before it. Nothing is written: the riff's cycle
# goes on counting and its strokes inside the rest are left out, the kit's time with them; the pull keeps its
# drum and its china; and while the whole band is out the crew answers over its own boots (v6's deck), two to the
# bar, as it does in the first call. So verse one: the crew sings 'Take up the slack', pulls, and the band comes
# in three beats late; then two; then one; and on the fourth pull, 'All together', it lands WITH the pull. Verse
# two: the band waits a little longer each time (the first time it does not wait at all) and comes in before the
# pull: ten sixteenths early, six, two. Verse three: the right guitar a beat early and alone, the pull, the left
# guitar and the bass a beat late; then both on the pull.
# v7's ride stays where the band is still under the crew (verse two); in verses one and three the guitars' dip
# goes (there is nothing under the answer to dip, and the head is not to arrive 3 dB down).
# the shortest rest a hand takes, sixteenths ; the boots' velocity on one ; on three ; the loudness target
# ("" = unchanged). "" = v7.
LETGO = os.environ.get('C10T15_LETGO', '4;0.72;0.62;-10.084' if ANSWER else '')
# v9 (chirper-one, whole song): THE READ, AND WHO HOLDS WHAT. The song had not been read against the album's eleven
# records since v3, five kept versions ago, and every one of those versions moved the voices or the band. Read whole
# at v8 (finished file, each band as a share of the mix): every stretch with the band stands 4.0 to 6.9 dB over the
# records at 250-500 Hz and 3.2 to 4.6 over at 500 Hz-1 kHz, the verses 1.8 to 2.1 dB worse at 250-500 than at v3
# (the shantyman's 3 dB, the crew's 3 dB, the stops). Read by part against the records' own stems (raw, verse one and
# chorus one): THE VOICES are 42% and 32% of the mix (4.9 and 3.8 dB over the records' voices) and hold 79% and 64% of
# 250-500 Hz and 82% and 80% of 500 Hz-1 kHz; their box, 250-500 Hz, stands 4.2 dB over their own level's share.
# THE TWO GUITARS are 10% and 15% of the mix (4.6 and 2.9 dB under the records' guitars) and their shape is wrong
# where a low-tuned guitar's weight is: 6.5 dB short at 120-250 Hz against the record's guitar heard alone, because
# this rig cuts the low string before the amp (its `tight` filter, at 220 Hz; chirper-three found the same on So Far).
# Two changes, each benched on the part alone:
#   the first pair's tight filter comes down to 150 Hz: the pair alone +4.1 dB at 120-250 Hz, +1.7 at 60-120,
#     0.2 or less everywhere else (180 Hz gave +2.0)
#   the three voices lose 3.5 dB of box at 400 Hz (q 0.8) and get 1.5 dB back on their faders, which is what the cut
#     took from their level (K): 250-500 Hz -1.8 dB, 500 Hz-1 kHz -0.6, 2-4 kHz +1.3. As loud as the three rounds
#     before this set them, and more of it is consonant.
# Not touched: the guitars' fader and their 700 Hz lift (they would come up under the shantyman's words), the bass,
# the kit, the second pair.
# the first pair's tight filter, Hz ; the voices' extra band ; dB back on their faders ; the loudness target.
# '' = v8 byte for byte.
WEIGHT = os.environ.get('C10T15_WEIGHT', '150;peak cutoff=400 q=0.8 gain=-3.5dB;1.5;-10.084' if LETGO and os.environ.get('C10T15_DECKCLIP', 'x') else '')
# v10 (chirper-two, whole song): A MAN TOO LATE, A MAN TOO QUICK. The words have said it since v1: "a man too late
# is a man let go" (verse one), "a man too quick is a man alone" (verse two), "a man too soon and a man too late /
# we meet in the middle and the rope runs straight" (verse three). The band was that man and had no voice: since v8
# its hands let go under the crew's answer and take the rope up at their own head, late or early, but a head is a
# chord. Now each hand has a man, the band's own (the record's barked voice, which this song had not used), and
# WHERE HIS HAND TAKES THE ROPE UP HE SHOUTS "HAUL!", the crew's word, at his own time. Verse one, the late man
# (left): the crew sings "Take up the slack", pulls and shouts; three beats later the band comes in and its man
# shouts after them; then two beats late; then one; and on the fourth pull, "All together", his shout is the crew's.
# Verse two, the quick man (right): ten sixteenths BEFORE the crew's pull, then six, then two (the pull cuts him
# off), and with them on the chorus's first "Haul". Verse three, both: the right a beat too soon, the pull, the
# left a beat too late; and at the second pull both at once, from either side: in the middle. In the last eight
# bars of 'home' both pull with the crew on every "Haul". 26 shouts at 18 moments; no other note is touched.
# The voice is the record's bark (kidman with words, as Common Time and Odd Sympathy carry it), one man a little
# larger than the other. Its eq is not theirs: on this one vowel the album's setting read 2 dB over the records'
# voices at 500 Hz-1 kHz (where this song is already over) and 2 to 6 short above; as set it is within 1.8 dB of
# them from 500 Hz to 16 kHz (tools/voxref.py). LEVEL: alone, a shout is as loud as the crew's own "Haul" (K -24.4
# against -24.6). By the album's yardstick (voxref: the voice against the whole mix while it sounds; the records'
# voices -9.2 dB): verse one -10.6, verse two -11.4, 'home' -9.0. A shout against everything else sounding with
# it (raw, K): the late man 3.5, 5.2, 5.6 dB under; the quick man 6.4, 4.9, 3.0; verse three's 2.0 and 6.8; with
# the crew (the fader's lift, one voice among seven and the whole band landing) 6.5, 5.7, 6.5; in 'home' 6.1 to 8.1.
# NOT A WORD, AND I SAY SO: the recogniser hears the bark's "Haul" as "Ah!" or "Oh" in eight spellings (the engine's
# 'haul', bd-43d2e1): it is a shout on the crew's vowel, told by where it falls.
# gain ; how far left and right the two men stand ; their note ; sixteenths a shout lasts ; velocity ; the velocity
# of their shouts in the last eight bars of 'home' ("" = none there) ; the size of each man's tract (late:early) ;
# the loudness target ("" = unchanged) ; eq bands (| between) ; send to the hall ; dB more where one man shouts
# with the crew, and where both do (one:both). "" = v9.
MAN = os.environ.get('C10T15_MAN', '5.5dB;0.5;F4;3;0.9;0.9;1.06:0.96;-10.06;hp cutoff=440|peak cutoff=700 q=1.2 gain=-3dB|peak cutoff=1800 q=0.7 gain=6dB|peak cutoff=5500 q=1.2 gain=-2dB;-18dB;4:1' if WEIGHT else '')
# v11 (chirper-alpha; an instrument round: THE KICK). Read alone against the kicks in the eleven records' drum
# stems (hit by hit, 5 to 125 ms after each): the album's kick has its line at 54 Hz (theirs 50), NOTHING at 90-120 Hz
# (-28.8 dB as a share of its 35-250 Hz; theirs -13.6, their leanest -19.4) and rings 84 ms to 20 dB down (theirs
# 37 to 49). So the drum is tuned to the song (A flat, 52 Hz: its own third, where the stock drum is an A the album
# has no use for) and gets a CHEST: a bare sine an octave over the drum, a sixteenth of a second long, on its own
# track, struck with every kick at the kick's velocity and sent straight to the mix. With it the kick alone reads
# -13.8 at 90-120 Hz, its click -9.1 against the low band (theirs -10.2), 52 ms to 20 dB down.
# Why a track and not a layer of the kick's patch: the patch's drive shares one ceiling among its layers (a chest
# inside it took 2.4 dB off the click and 1.0 off the sub), and the kit bus's clip holds the kick's top (a decibel
# of fader bought 0.2). Why the drum's tail is not shortened to the records' 44 ms: here the kick is 62% of the mix
# under 60 Hz, and alone the short one has 4.2 dB less there; that waits for a bass that holds the sub.
# The click's eq goes 10 -> 11.5 dB: a semitone down the drum has 1.4 dB less of it.
# the drum's note ; the chest's note ("" = no chest) ; its gain ; its decay, ms ; the kick's click, dB at 4.5 kHz
# on its track ("" = as it was, 10) ; the loudness target ("" = unchanged). "" = v10.
KICK = os.environ.get('C10T15_KICK', 'Ab1;Ab2;-4dB;90;11.5;-10.08' if MAN else '')
# v12 (chirper-zero; instrument round: the guitars; no stroke, word, stop or other fader of v11 is changed): THE
# HANDS GET TEETH. The song's two guitars are the two hands on the rope, and a hand that hauls should bite. Read by
# the stroke against six records' guitar stems at their own chugs (tools/riffpunch.py --strokes; "scoop" is how much
# more a stroke carries at 1-4 kHz than at 400 Hz-1 kHz): the records 11.3 dB (6.5 to 12.7); the first pair 4.6,
# the wall pair 4.8. A thud where the records clank, and for the reason found on Extreme and Mean (v23): every
# muted stroke is written at a full palm, which closes the string's own filter 3.4 octaves, to 1 kHz, BEFORE the
# amp; then the pair's eq lifted 700 Hz by 2.5 dB (a lift that dates from a yardstick with the records' voices in
# it), and the wall pair ran through captured cabinet files with nothing over 6 kHz (10 kHz 18 dB under the
# record's lone guitar).
#   the first pair   the palm closes the filter 2 octaves (2.75 kHz); the microphone a little nearer the cone's
#       centre (0.5 -> 0.42); the 700 Hz lift goes and 800 Hz comes DOWN 4 dB (alone, 630 and 800 Hz stood 6.6 and
#       8.4 dB over the record's lone guitar; now 0.9 and 2.3); 2.5 dB at 185 Hz gives back the chest the brighter
#       string cost; the fader comes up 1 dB, because a guitar with less at 700 Hz covers less of the shantyman
#   the wall pair    stops at its amp and plays through the engine's cabinet (as on In the Time Of, On Its Hinge,
#       Common Time and Extreme and Mean), its microphone further out than the first pair's (0.5), as a second
#       pair's is; 3 dB at 220 Hz for the chest the cabinet files had; its 380 Hz trim goes with the old rig
# MEASURED, alone: the stroke's scoop 4.6 -> 11.5 (first pair), 4.8 -> 8.2 (wall pair), 5.0 -> 11.0 (all four in
# chorus two); against the record's lone guitar, third-octave by third-octave (tools/cabspec.py, mean distance
# 100 Hz-10 kHz): the first pair 2.88 -> 1.85 dB, the wall pair 3.61 -> 1.87, all four together 2.78 -> 1.65.
# TWO READS GO THE OTHER WAY and are in the round note: by the stroke the guitars carry more over 6 kHz than the
# records' separated stems (which lose their top), and the stroke's low end falls faster than any record's.
# the palm's reach, octaves (the rig's own is -3.4) ; the first pair's microphone ; its fader ; its eq bands (|
# between) ; the wall pair's microphone ; its cones, left,right ; the microphone's distance ; its fader ; its eq
# bands ; the loudness target. "" = v11.
TEETH = os.environ.get('C10T15_TEETH', '-2;0.42;1.7dB;peak cutoff=185 q=1.2 gain=2.5dB|peak cutoff=800 q=1.2 gain=-4dB;0.5;94,95;0.15;-0.7dB;'
                                       'peak cutoff=220 q=1 gain=3dB;-9.944' if KICK else '')
# v13 (chirper-alpha; whole song: the last chorus, 'home', 3:02.6-3:41.7): SEVENTEEN, SIXTEEN AND FIFTEEN PULLS LAND
# ON ONE CHORD. The song is three counts: the crew pulls every sixteen, the left hand's riff is fifteen long, the
# right hand's seventeen. The verses play one against another for a few bars and the choruses throw the riffs away
# (all four guitars play the crew's four), so the record's own rule, long cycles over one pulse that land together
# after a long wait, had never happened in this song: no stretch was long enough. Fifteen bars is 240 sixteenths:
# sixteen fifteens exactly, and fourteen seventeens and two. So in the last chorus the two hands go back to their
# own lengths under the crew: the left hand hauls its fifteen from the downbeat (a sixteenth earlier against the
# pull every bar), the right hand its seventeen from an eighth after it (a sixteenth later every bar), and fifteen
# bars on the left has pulled seventeen times, the crew sixteen, the right fifteen, and all land on the one long
# chord under 'haul her home', which was already there. The second pair of guitars, the bass and the foot keep the
# chorus in four as written; each hand's stroke takes the chord of the bar it falls in. Nothing else changes.
# 'Home' reads 0.2 dB louder after the master at the same raw level (the hands' strokes no longer pile on the
# walls'), so the target moves and every other section has the gain it had.
# the left hand's riff length ; the right hand's ; the bar of 'home' (from 0) on whose downbeat both land ; dB on the
# two hands' faders through it ; dB on the wall pair's ; the loudness target ("" = unchanged). "" = v12.
LONG = os.environ.get('C10T15_LONG', '15;17;15;0;0;-9.9' if TEETH else '')
# v14 (chirper-one, whole song): THE SQUEEZEBOX PLAYS THE CHORUS. The song's hook is the chorus ('Haul away, haul
# away home'), and it was carried by the crew's voices alone, whose words a reader makes nothing of with the band
# playing (0 of the chorus's words, every round that has read them). The fo'c'sle's instrument was already in the
# song, in one place: the two concertinas of 'easy' (v5), which came from nowhere at 2:21 and were not heard again.
# Now it has the tune. CHORUS ONE is the crew alone, as it was. In CHORUS TWO (2:00.0) a concertina, half left,
# plays the chorus's tune an octave over the crew: their notes where they sing them, a passing note in the breath
# after 'haul' and two sixteenths up into the next bar, so the eight bars are one line. Then 'easy' is the two
# concertinas alone, as it was: the instrument has been heard coming. In 'HOME' (3:02.6) it plays the tune through
# the whole last chorus, and the second time round (3:23.5) the other concertina joins it a third higher, in the
# song's own scale, to the last long 'home'. So the chorus grows each time it comes: voices; voices and a
# squeezebox; and two in thirds over v13's two hands coming apart, with something beside the crew that stays in four.
# Two new tracks (the patch of 'easy'), 180 notes. Nothing else is changed.
# Benched raw against everything else and against the voices alone (K, whole stretch): see the round note. The
# box's own weight (its fundamentals, 350-620 Hz) is cut 8 dB at 430 Hz: the choruses already stand 2.4 to 2.9 dB
# over the records there, and what a concertina is heard by over a band is its reed (1-8 kHz).
TUNE = os.environ.get('C10T15_TUNE', '' if any(k.startswith('C10T15_') and k not in ('C10T15_OUT', 'C10T15_SHOW', 'C10T15_TUNE', 'C10T15_SUB') for k in os.environ)
                      else '-4.5dB;0.35;-12dB;-3;hp cutoff=300|peak cutoff=430 q=0.8 gain=-8dB|peak cutoff=2500 q=0.7 gain=3dB;-9.85')
# the chorus's tune as a concertina plays it, an octave over the crew: their notes where they sing them, a passing
# note in the breath after 'haul', and two sixteenths up into the next bar. (sixteenth, length, note), a bar a line.
BOX_TUNE = [[(0, 6, 'C5'), (6, 2, 'Bb4'), (8, 2, 'Ab4'), (10, 4, 'F4'), (14, 1, 'Ab4'), (15, 1, 'Bb4')],
            [(0, 6, 'C5'), (6, 2, 'Bb4'), (8, 2, 'Ab4'), (10, 2, 'C5'), (12, 2, 'F4'), (14, 1, 'C5'), (15, 1, 'Db5')],
            [(0, 6, 'Eb5'), (6, 2, 'Db5'), (8, 2, 'C5'), (10, 6, 'Ab4')],
            [(0, 4, 'Gb4'), (4, 2, 'Gb4'), (6, 2, 'Ab4'), (8, 4, 'Gb4'), (12, 2, 'F4'), (14, 1, 'Ab4'), (15, 1, 'Bb4')],
            [(0, 6, 'C5'), (6, 2, 'Bb4'), (8, 2, 'Ab4'), (10, 4, 'F4'), (14, 1, 'Ab4'), (15, 1, 'Bb4')],
            [(0, 6, 'C5'), (6, 2, 'Bb4'), (8, 2, 'Ab4'), (10, 2, 'C5'), (12, 2, 'F4'), (14, 1, 'C5'), (15, 1, 'Db5')],
            [(0, 6, 'Eb5'), (6, 2, 'Db5'), (8, 2, 'C5'), (10, 4, 'Ab4'), (14, 2, 'Bb4')],
            [(0, 4, 'C5'), (4, 4, 'Eb5'), (8, 8, 'F5')]]
# the same a third higher, in the song's own scale (F G flat A flat B flat C D flat E flat)
BOX_THIRD = {'F4': 'Ab4', 'Gb4': 'Bb4', 'Ab4': 'C5', 'Bb4': 'Db5', 'C5': 'Eb5', 'Db5': 'F5', 'Eb5': 'Gb5', 'F5': 'Ab5'}
# v15 (chirper-zero; instrument round: the bass, with the kick's low end, because they are one job): THE SUB CHANGES
# HANDS. No note moves. chirper-one's read by part under v14 named it (the bass 9.6 to 12.8 dB over the records'
# basses under 60 Hz and 1.8 to 4.6 under them at 60-120 Hz: 'its weight is an octave too low'), and alpha's v11 left
# the other half open ('the drum's tail is not shortened: that waits for a bass that holds the sub'). On the eleven
# records it is the other way round: their basses sit 16 dB under their drums below 60 Hz, their weight an octave
# up at 80 Hz, and the kick holds the floor (In the Time Of v24 found it and could only go halfway, for want of
# this kick). Here the kit read 1.7 dB SHORT of the records' kits under 60 Hz while the bass stood 11.0 over.
#   THE BASS LEANS ON ITS OCTAVE (In the Time Of v24's chain, further): the patch's sine sub 11 dB down (it is what
#       drives the bass's two compressors: with less of it the string comes up); the lift at 110 Hz 6 -> 12 dB, at
#       220 Hz 8 -> 6; the box cut (450 Hz +2 -> 540 Hz -6 dB, wide); the grind moved up to 1150 Hz. Alone beside
#       eleven records' basses (tools/bassspec.py, verse one): 40 Hz +14.3 -> +9.8, 80 Hz -7.0 -> -1.6, 100 Hz
#       -6.6 -> -1.3, 400-630 Hz +5.5..+10.4 -> +0.8..+5.2; distance 6.01 -> 3.82.
#   THE KICK TAKES THE FLOOR, AND IS NO LONGER FOR IT: the drum's amp decay 210 -> 160 ms, and 6 dB at 55 Hz on its
#       own track (the kit bus's clip gives back 2.4 of them; on the bus, after the clip, 4 dB did the same but
#       reached the five men's boots, which share that bus), its click 11.5 -> 13 dB to stay where it was. Alone
#       (alpha's kickref.py): 2.4 dB more under 60 Hz and 1.7 more at 60-120 Hz, its click where it was, 52 ms to
#       20 dB down where 50 (the same lift with the decay untouched: 70 ms; the records 44).
#   'EASY' IS WHY THE SINE IS NOT OFF: no kick plays there and the bass must carry its own floor (sine off, the
#       stretch fell 10.4 dB under 60 Hz; as set, 0.8).
# the bass's patch overrides ; the kick's amp decay ; a band on the kick's eq ; its click, dB at 4.5 kHz ; the
# loudness target. "" = v14.
SUB = os.environ.get('C10T15_SUB', 'fx.2.bands.0.gain=12dB fx.2.bands.1.gain=6dB fx.2.bands.2.cutoff=540 fx.2.bands.2.q=0.7 fx.2.bands.2.gain=-6dB '
                                   'fx.2.bands.3.cutoff=1150 fx.2.bands.3.q=1.2 fx.2.bands.3.gain=6dB synth.layers.1.level=-20dB;160ms;'
                                   'peak cutoff=55 q=0.7 gain=6dB;13;-9.8' if TUNE else '')
BARK = 'kidman synth.layers.0.diction=2 synth.layers.0.speech=1'
# five men: the kit piece, where in the spread his foot lands (0..1), how hard against the others, his board's
# note, where he stands, how long his board rings (ms)
BOOTS = [('b1', 0.0, 1.0, 'D2', -0.15, 150), ('b2', 0.23, 0.88, 'C2', 0.4, 170), ('b3', 0.47, 0.94, 'Eb2', -0.5, 135),
         ('b4', 0.7, 0.82, 'Db2', 0.15, 160), ('b5', 1.0, 0.9, 'E2', 0.6, 125)]


# the boot itself: the board's level ; its brightness ; its damping ; the low-pass over all three ; the sole's
# level at its peak, dB ; the amp curve ; the heel's level ; how far the heel's note drops, semitones
BOOT = os.environ.get('C10T15_BOOT', '6dB;0.9;0.7;6k;-4;2;1dB;3')


def boot(ring):
    """One boot on a deck board: the heel's thud (a sine that drops as the board gives), the board itself (a
    struck plate, heavily damped: wood, not a drum head) and the sole (a few ms of noise)."""
    board, bright, damp, lp, sole, curve, heel, drop = BOOT.split(';')
    return {'synth': {
        'amp': {'a': '0.5ms', 'd': f'{ring}ms', 's': 0, 'r': '40ms', 'curve': float(curve)},
        'env': {'p': {'a': '0.3ms', 'd': '30ms', 's': 0}, 's': {'a': '0.3ms', 'd': '10ms', 's': 0}},
        'layers': [{'wave': 'sine', 'level': heel},
                   {'type': 'modal', 'modes': 'plate', 'decay': f'{ring / 1000:g}s', 'damp': float(damp), 'bright': float(bright), 'strike': 0.3, 'level': board},
                   {'type': 'noise', 'color': 'pink', 'level': {'value': '-60dB', 'mod': [{'src': 'env.s', 'amount': 60 + float(sole)}]}}],
        'filters': [f'lp cutoff={lp} q=0.5'],
        'pitch': {'value': 0, 'mod': [{'src': 'env.p', 'amount': float(drop)}, {'src': 'rand', 'amount': 0.3}]}},
        'play': {'vel_sens': 0.6}}


WALK = {(0, 0): {14: 12}, (0, 3): {14: 1}, (3, 7): {14: 5}, (7, 0): {12: 3, 14: 1}}     # eighth: semitones over low F
# one bow, the pitch sliding inside the note (mono, legato); no chance detuning from note to note and less than half
# of the library's unsteady bowing (12 cents either way there, 5 here): taut is in tune
HAWSER = ('tagelharpa-bass play.mono=true play.legato=true play.glide={} play.glide_smooth=true '
          'synth.pitch.mod.0.amount=0 synth.pitch.mod.1.amount=0.05')
SHANTY = 'voice-hook synth.layers.0.diction=3 synth.layers.0.effort_tilt=1 play.phrase_arc=0.5'
CREW = 'voice-choir synth.layers.0.tract=1.12 synth.layers.0.diction=3 synth.layers.0.effort_tilt=1 fx.0.mix=0.14'

PH = {'oh': 'OW1', 'the': 'DH AH0', 'line': 'L AY1 N', 'is': 'IH0 Z', 'long': 'L AO1 NG', 'and': 'AH0 N D',
      'load': 'L OW1 D', 'slow': 'S L OW1', 'a': 'AH0', 'hand': 'HH AE1 N D', 'too': 'T UW1', 'late': 'L EY1 T',
      'let': 'L EH1 T', 'go': 'G OW1', 'we': 'W IY1', 'lean': 'L IY1 N', 'on': 'AA1 N', 'hold': 'HH OW1 L D',
      'her': 'HH ER0', 'low': 'L OW1', 'when': 'W EH1 N', 'i': 'AY1', 'call': 'K AO1 L', 'then': 'DH EH1 N',
      'way': 'W EY1', 'tide': 'T AY1 D', 'high': 'HH AY1', 'hour': 'AW1 R', 'soon': 'S UW1 N', 'quick': 'K W IH1 K',
      'lone': 'L OW1 N', 'wait': 'W EY1 T', 'for': 'F ER0', 'word': 'W ER1 D', 'our': 'AW1 R', 'own': 'OW1 N',
      'all': 'AO1 L', 'come': 'K AH1 M', 'down': 'D AW1 N', 'meet': 'M IY1 T', 'in': 'IH0 N', 'mid': 'M IH1',
      'dle': 'D AH0 L', 'rope': 'R OW1 P', 'runs': 'R AH1 N Z', 'straight': 'S T R EY1 T', 'take': 'T EY1 K',
      'up': 'AH1 P', 'slack': 'S L AE1 K', 'haul': 'HH AA1 L', 'to': 'T AH0', 'ge': 'G EH1', 'ther': 'DH ER0',
      'home': 'HH OW1 M', 'now': 'N AW1', 'make': 'M EY1 K', 'fast': 'F AE1 S T', 'who': 'HH UW1', 'will': 'W IH1 L',
      'with': 'W IH1 DH', 'me': 'M IY1', 'man': 'M AE1 N', 'comes': 'K AH1 M Z', 'ea': 'IY1', 'sy': 'Z IY0', 'ride': 'R AY1 D', 'oo': 'UW1'}
# A call is two bars and a pickup: syllable, start, length, pitch. Stresses fall on 0, 4, 12 and the next downbeat.
T = [(-4, 2), (-2, 2), (0, 3), (3, 1), (4, 4), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)]
T3 = [(-2, 2), (0, 2), (2, 1), (3, 1), (4, 4), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)]
T4 = [(-2, 2), (0, 3), (3, 1), (4, 4), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)]
M1 = 'C3 Eb3 F3 F3 Ab3 F3 Eb3 F3 Eb3 C3'          # falls to the fifth below: a question
M2 = 'C3 Eb3 F3 F3 Ab3 F3 Eb3 Eb3 Eb3 F3'         # comes home
M3 = 'F3 Ab3 Ab3 Ab3 C4 Ab3 F3 Ab3 F3 Eb3'        # leans up
M4 = 'F3 Ab3 Ab3 C4 Ab3 F3 Ab3 F3 F3'             # and calls the pull


def line(words, rhythm, tune):
    words, tune = words.split(), tune.split()
    assert len(words) == len(rhythm) == len(tune), (words, len(rhythm), len(tune))
    return [(w, t, d, p) for w, (t, d), p in zip(words, rhythm, tune)]


CALLS = {
    'first call': [line('oh who will come and haul with me', [(-2, 2), (0, 3), (3, 1), (4, 4), (8, 4), (12, 3), (15, 1), (16, 8)],
                        'C3 F3 F3 Ab3 F3 Eb3 Eb3 C3')],
    'late hand': [line('oh the line is long and the load is slow', T, M1),
                  line('and a man too late is a man let go', T, M2),
                  line('we lean on the line and we hold her low', T3, M3),
                  line('and when i call then a way we go', T4, M4)],
    'early hand': [line('oh the wait is long and the word comes soon', T, M1),
                   line('and a man too quick is a man a lone', T, M2),
                   line('we wait for the call and we hold our own', T3, M3),
                   line('and when i call then we all come down', T4, M4)],
    'both hands': [line('a man too soon and a man too late', T4, 'Eb3 F3 F3 Ab3 F3 Eb3 F3 Eb3 C3'),
                   line('we meet in the mid dle and the rope runs straight',
                        [(-2, 2), (0, 2), (2, 1), (3, 1), (4, 2), (6, 2), (8, 2), (10, 2), (12, 3), (15, 1), (16, 8)],
                        'F3 Ab3 Ab3 Ab3 C4 C4 Ab3 F3 Ab3 F3 F3')],
}
# The answer fills the third bar; the pull is the fourth bar's downbeat.
SLACK = line('take up the slack haul', [(32, 4), (36, 2), (38, 2), (40, 6), (48, 5)], 'Ab3 F3 Eb3 F3 F3')
ALL = line('all to ge ther haul', [(32, 4), (36, 2), (38, 2), (40, 6), (48, 5)], 'Ab3 Ab3 C4 Ab3 C4')
CHORUS = [line('haul a way', [(0, 6), (8, 2), (10, 6)], 'C4 Ab3 F3'),
          line('haul a way home', [(0, 6), (8, 2), (10, 2), (12, 4)], 'C4 Ab3 C4 F3'),
          line('haul a way', [(0, 6), (8, 2), (10, 6)], 'Eb4 C4 Ab3'),
          line('all to ge ther now', [(0, 4), (4, 2), (6, 2), (8, 4), (12, 4)], 'Gb3 Gb3 Ab3 Gb3 F3'),
          line('haul a way', [(0, 6), (8, 2), (10, 6)], 'C4 Ab3 F3'),
          line('haul a way home', [(0, 6), (8, 2), (10, 2), (12, 4)], 'C4 Ab3 C4 F3'),
          line('haul a way', [(0, 6), (8, 2), (10, 6)], 'Eb4 C4 Ab3'),
          line('haul her home', [(0, 4), (4, 4), (8, 8)], 'C4 Eb4 F4')]


def name(m):
    return PITCH[m % 12] + str(m // 12 - 1)


def make():
    ev = defaultdict(list)
    marks = {}

    def put(tr, t, dur, p, v, mute=False, **more):
        e = {'at': round(t / GRID, 5), 'len': round(dur / GRID, 5), 'pitch': name(p) if isinstance(p, int) else p, 'vel': round(v, 3)}
        if mute:
            e['expr'] = {'pm': 1}
        e.update(more)
        ev[tr].append(e)

    def kit(t, piece, v):
        tr = {'k': 'kick', 's': 'snare', 'h': 'hat', 'hp': 'hat', 'x': 'cym', 'c': 'cym', 'rde': 'cym'}.get(piece, 'toms')
        put(tr, t, 3.8 if tr == 'cym' else 1.15, piece, v)

    def sing(tr, t0, syllables, v=.8, loud=()):
        # Notes touch inside a phrase (one breath); a gap of more than a sixteenth is a new phrase.
        for j, (w, t, d, p) in enumerate(syllables):
            nxt = syllables[j + 1][1] if j + 1 < len(syllables) else None
            if nxt is not None and nxt - (t + d) <= 1:
                d = nxt - t
            put(tr, t0 + t, d - (0 if nxt is not None and nxt - t == d else .4), p, .98 if w in loud else v, ph=PH[w])

    def stroke(trs, t, kind, semi, dur, root=F1, bass=True, kick=True, whole=False):
        p = root + semi
        for tr in trs:
            put(tr, t, dur, name(p) + ',' + name(p + 7) + (',' + name(p + 12) if whole else '') if kind == 'o' else p,
                .96 if kind == 'o' else .94 if kind == 'n' else .86, kind == 'm')
        if bass:
            put('bass', t, dur, p, .92 if kind != 'm' else .86, kind == 'm')
        if kick:
            kit(t, 'k', .98 if kind != 'm' else .82)

    def cycle(trs, riff, length, a, b, head, rests=(), **kw):
        # every stroke of the riff between a and b, the cycle placed so that a head falls on `head`
        # (v8: but none inside a rest, and the stroke before a rest stops where it begins)
        k0 = -((head - a) // length) - 1
        for k in range(k0, (b - head) // length + 2):
            for pos, kind, semi, dur in riff:
                t = head + k * length + pos
                if a <= t < b and not any(r0 <= t < r1 for r0, r1 in rests):
                    stroke(trs, t, kind, semi, min([dur, b - t - .1] + [r0 - t - .1 for r0, _ in rests if t < r0]), **kw)

    def hand(c, length, anchor, late):
        """v8: one hand's rest in the couplet at c: from the answer's start to its own head, the first at or after the
        pull for a late hand, the last at or before it for an early one (`anchor` is any head). None if too short."""
        if not LETGO:
            return None
        pull = c + 3 * BAR
        head = anchor + length * (-((anchor - pull) // length) if late else (pull - anchor) // length)
        return (c + 2 * BAR, head) if head - (c + 2 * BAR) >= float(LETGO.split(';')[0]) else None

    def feet(a, spans):
        """v8: the crew's boots, two to the bar, wherever the whole band has let go."""
        for r0, r1 in spans:
            for t in range(r0, r1, BAR // 2):
                stamp(t, float(LETGO.split(';')[1 if (t - a) % BAR == 0 else 2]))

    def haul(tr, t, slack, was=None, dur=9, v=.9):
        """The rope at a pull: found where the last pull left it (`was`), then hauled to `slack` semitones from the crew's F."""
        if not ROPE:
            return
        if was is not None:
            put(tr, t, 2, F1 + 24 + was, v)
            put(tr, t + 1.5, dur - 1.5, F1 + 24 + slack, v)
        else:
            put(tr, t, dur, F1 + 24 + slack, v)

    def shout(who, t, room=None, v=None, lift=None):
        """v10: a man of the band shouts 'Haul!' where his hand takes the rope up (`room`: sixteenths before the crew's
        own pull; `lift`: which of the switch's two lifts his fader takes, when he shouts WITH the crew)."""
        if not MAN:
            return
        f = MAN.split(';')
        for w in who:
            put('man-' + w, t, float(f[3]) if not room else min(float(f[3]), room - .1), f[2], float(f[4]) if v is None else v, ph=PH['haul'])
            if lift is not None and float(f[10].split(':')[lift]):
                ev['lift:man-' + w].append((t, float(f[3]), float(f[10].split(':')[lift])))

    def stamp(t, v):
        """v6: five boots on the deck, not quite together."""
        spread = float(DECK.split(';')[1]) / (60000 / BPM / GRID)        # ms -> sixteenths
        for piece, where, hard, _, _, _ in BOOTS:
            put('deck', t + where * spread, 1.15, piece, v * hard)

    def stomp(t, v=.7):
        if DECK:
            return stamp(t, v)
        kit(t, 'ft', v)
        kit(t, 'k', v)

    def couplets(sec, a, n, answers, shout=True):
        for i in range(n):
            c = a + i * 4 * BAR
            sing('shanty', c, CALLS[sec][i])
            sing('crew', c, answers[i], .86, loud=('haul',))
            if shout:
                put('shanty', c + 48, 4.5, F1 + 24, .98, ph=PH['haul'])   # he pulls with them
            kit(c + 48, 'ft', .92)
            kit(c + 48, 'x', .9)

    def chorus(a, bars, wide, last_long=False, high=False, pickup=False, hands=None, box=()):
        gtrs = ('gl', 'gr', 'wl', 'wr') if wide else ('gl', 'gr')
        if hands:
            # v13: the two hands haul their own lengths under the crew's four, each stroke on the chord of the bar
            # it falls in, and both land on the downbeat of bar `land`; the walls, the bass and the foot stay in four
            left, right, land = hands
            for tr, riff, length in (('gl', RIFF15 if left == 15 else RIFF17, left), ('gr', RIFF17 if right == 17 else RIFF15, right)):
                head = a + land * BAR
                first = head - length * ((head - a) // length)         # its first head at or after the section's start
                for k in range((head - first) // length):
                    for pos, kind, semi, dur in riff:
                        t = first + k * length + pos
                        stroke((tr,), t, kind, semi, min(dur, head - t - .1), F1 + CHORDS[((t - a) // BAR) % 8], bass=False, kick=False)
        for b in range(bars):
            t0 = a + b * BAR
            root = F1 + CHORDS[b % 8]
            final = b % 8 == 7
            if hands:
                gtrs = ('wl', 'wr') if b < hands[2] else ('gl', 'gr', 'wl', 'wr')
            built = BUILT.split(';') if BUILT else None
            ends = last_long and b == bars - 1                        # the song's last chorus bar: one long chord, as it was
            walks = bool(built and built[0] == '1') and not ends
            for pos, kind, semi, dur in RIFF16:
                if final and pos:
                    continue          # the last bar is one held chord under 'home'
                stroke(gtrs, t0 + pos, kind, semi, (15.5 if last_long and b == bars - 1 else 11.5) if final else dur, root,
                       bass=not walks, whole=bool(built and built[1] == '1'))
            if walks:                 # v4: the bass in eighths on the root, stepping to the next chord on the last
                step = WALK.get((CHORDS[b % 8], CHORDS[(b + 1) % 8]), {})
                for q in range(0, BAR, 2):
                    put('bass', t0 + q, 1.8, F1 + step[q] if q in step else root, .92 if q % 4 == 0 else .84)
            words = CHORUS[b % 8]
            sing('crew', t0, words, .9, loud=('haul',))
            for who in (box[b // 8] if b // 8 < len(box) else ()):          # v14: the squeezebox plays the chorus
                for pos, dur, note in BOX_TUNE[b % 8]:
                    put('tune-' + who, t0 + pos, dur - .15, BOX_THIRD[note] if who == 'r' else note, .8)
            mine = words
            if final and pickup:
                # he lets the last word go early: his next call starts before the bar is out
                mine = words[:-1] + [(words[-1][0], words[-1][1], 3.5, words[-1][3])]
            sing('shanty', t0, mine, .88, loud=('haul',))        # he sings the chorus with them
            if high:
                # a second gang a fourth over the pulls only (F over C, A flat over E flat: the song's own notes)
                w, t, d, p = words[0]
                if w == 'haul':
                    put('crew-high', t0 + t, d - .4, {'C4': 'F4', 'Eb4': 'Ab4'}[p], .9, ph=PH[w])
            if high and MAN and MAN.split(';')[5] and b >= bars - 8 and words[0][0] == 'haul':
                shout(('late', 'early'), t0, v=float(MAN.split(';')[5]))     # v10: the last time through, both men pull with the crew
            kit(t0, 'c' if b % 4 == 0 else 'x', .9 if b % 4 == 0 else .74)
            if built and built[2] and b % 4 and words[0][0] == 'haul':
                kit(t0, 'c', float(built[2]))                         # v4: a crash on every pull, over the china that was there
            if built and built[3] and not ends and DECK and DECK.split(';')[2]:
                stamp(t0, float(DECK.split(';')[2])), stamp(t0 + 8, float(DECK.split(';')[2]) - .1)     # v6: the feet are feet
            elif built and built[3] and not ends:
                kit(t0, 'ft', float(built[3])), kit(t0 + 8, 'ft', float(built[3]) - .1)     # v4: the crew's feet
            for q in (4, 8, 12):
                if not (final and q == 12):
                    kit(t0 + q, 'x', .6)
            if final:
                kit(t0 + 4, 's', .94)
                for t, p in ((12, 't1'), (13, 't2'), (14, 'ft'), (15, 'ft')):
                    if not (last_long and b == bars - 1):
                        kit(t0 + t, p, .82)
            else:
                kit(t0 + 4, 's', .94)
                kit(t0 + 12, 's', .94)

    def beat(a, bars, bronze, back=(8,), skip_last_beat=True, rests=()):
        out = lambda t: any(r0 <= t < r1 for r0, r1 in rests)        # v8: the kit's time rests with the hands
        for b in range(bars):
            t0 = a + b * BAR
            last = b == bars - 1
            step = 2 if bronze == 'h' else 4
            for q in range(0, BAR, step):
                if last and skip_last_beat and q >= 12 or out(t0 + q):
                    continue
                kit(t0 + q, bronze, (.65 if q % 4 == 0 else .48) if bronze == 'h' else (.72 if q == 0 else .58))
            for q in back:
                if not (last and skip_last_beat and q >= 12) and not out(t0 + q):
                    kit(t0 + q, 's', .94)

    start = 0
    for sec, bars in FORM:
        marks[sec] = start
        a, b = start, start + bars * BAR
        if sec == 'count':
            stomp(a), stomp(a + 8)
        elif sec == 'first call':
            for k in range(bars):
                stomp(a + k * BAR, .72), stomp(a + k * BAR + 8, .62)
            couplets(sec, a, 1, [SLACK])
            haul('rope-l', a + 48, -4, -5)
        elif sec == 'late hand':
            # 15 against 16: the head is 12, 8, 4 and 0 sixteenths after the four pulls
            rests = [r for r in (hand(a + i * 4 * BAR, 15, a, True) for i in range(4)) if r]
            cycle(('gl', 'gr'), RIFF15, 15, a, b, a, rests=rests)
            couplets(sec, a, 4, [SLACK, SLACK, SLACK, ALL])
            for i in range(4):
                haul('rope-l', a + i * 4 * BAR + 48, i - 3, i - 4)
            beat(a, bars, 'h', rests=rests)
            feet(a, rests)
            for i, (_, head) in enumerate(rests):
                shout(('late',), head, lift=0 if head == a + i * 4 * BAR + 48 else None)   # v10: three beats late, two, one, and with the crew
            for t, p in ((12, 't1'), (13, 't1'), (14, 't2'), (15, 'ft')):
                kit(b - BAR + t, p, .82)
        elif sec == 'early hand':
            # 17 against 16: 3, 7, 11 and 15 after; one more bar and it lands on the chorus
            rests = [r for r in (hand(a + i * 4 * BAR, 17, a, False) for i in range(4)) if r]
            cycle(('gl', 'gr'), RIFF17, 17, a, b, a, rests=rests)
            couplets(sec, a, 4, [SLACK, SLACK, SLACK, SLACK])
            for i in range(4):
                haul('rope-r', a + i * 4 * BAR + 48, 4 - i, 5 - i)
            haul('rope-r', b, 0, 1)                    # the seventeen lands on the chorus
            beat(a, bars - 1, 'x', skip_last_beat=False, rests=rests)
            feet(a, rests)
            for r0, head in rests:
                shout(('early',), head, r0 + BAR - head)   # v10: ten sixteenths too soon, six, two (the pull cuts him off)
            shout(('early',), b, lift=0)               # and with the crew on the chorus
            hold = b - BAR
            sing('shanty', hold, line('hold fast', [(0, 6), (8, 6)], 'Ab3 C4'), .95)
            kit(hold, 'x', .8)
            for t, p in ((8, 's'), (9, 's'), (10, 't1'), (11, 't1'), (12, 't2'), (13, 't2'), (14, 'ft'), (15, 'ft')):
                kit(hold + t, p, .7 + .03 * (t - 8))
        elif sec in ('all together', 'all together again'):
            chorus(a, bars, wide=sec != 'all together', pickup=sec == 'all together', box=(('l',),) if TUNE and sec != 'all together' else ())
        elif sec == 'home':
            chorus(a, bars, wide=True, last_long=True, high=True, hands=tuple(int(x) for x in LONG.split(';')[:3]) if LONG else None,
                   box=(('l',), ('l', 'r')) if TUNE else ())
        elif sec == 'easy':
            land = marks_next['both hands'] + 7 * BAR
            for tr, riff, length in (('clean-l', RIFF15, 15), ('clean-r', RIFF17, 17)):
                k = -((land - a) // length) - 1
                while land + k * length < b:
                    for pos, kind, semi, dur in riff:
                        t = land + k * length + pos
                        if kind != 'm' and a <= t < b:
                            put(tr, t, 3.4, F1 + 12 + semi + (12 * int(SQUEEZE.split(';')[2]) if SQUEEZE else 0), .7)
                    k += 1
            for k, semi in enumerate((0, 0, 1, 1, 0, 0, 3, 1)):
                put('bass', a + k * BAR, 15, F1 + semi, .7)
                if DECK and DECK.split(';')[3]:
                    stamp(a + k * BAR, float(DECK.split(';')[3]))
                else:
                    kit(a + k * BAR, 'ft', .6)
                for q in (0, 4, 8, 12):
                    kit(a + k * BAR + q, 'hp', .42)
            sing('shanty', a, line('ea sy', [(0, 4), (4, 10)], 'F3 Eb3'), .55)
            sing('shanty', a + BAR, line('ea sy', [(0, 4), (4, 10)], 'F3 C3'), .55)
            sing('shanty', a + 2 * BAR, line('let her ride', [(0, 4), (4, 4), (8, 16)], 'Eb3 F3 Ab3'), .6)
            sing('shanty', a + 4 * BAR, line('ea sy', [(0, 4), (4, 10)], 'F3 Eb3'), .55)
            sing('shanty', a + 5 * BAR, line('ea sy', [(0, 4), (4, 10)], 'F3 C3'), .55)
            sing('shanty', a + 6 * BAR, line('with the tide', [(0, 4), (4, 4), (8, 16)], 'Eb3 F3 F3'), .6)
            for k, p in enumerate(('F3', 'Gb3', 'F3', 'Eb3')):
                put('crew', a + 2 * k * BAR, 2 * BAR - 2, p, .42, ph=PH['oo'])
        elif sec == 'both hands':
            land = a + 7 * BAR
            late = [r for r in (hand(a + i * 4 * BAR, 15, land, True) for i in range(2)) if r]
            early = [r for r in (hand(a + i * 4 * BAR, 17, land, False) for i in range(2)) if r]
            cycle(('gl',), RIFF15, 15, a, land, land, rests=late)                      # the late hand, with the bass
            cycle(('gr',), RIFF17, 17, a, land, land, bass=False, kick=False, rests=early)   # the early hand
            for k in range(-8, 1):                                          # the foot marks its heads too
                if a <= land + 17 * k < land:
                    kit(land + 17 * k, 'k', .98)
            stroke(('gl', 'gr', 'wl', 'wr'), land, 'o', 0, 11.5)
            kit(land, 'c', .92)
            couplets(sec, a, 2, [SLACK, ALL])
            for i in range(2):
                haul('rope-l', a + i * 4 * BAR + 48, i - 1, i - 2, v=.75)
                haul('rope-r', a + i * 4 * BAR + 48, 1 - i, 2 - i, v=.75)
            beat(a, bars, 'x', back=(4, 12), rests=late)     # v8: the kit's time is back when both hands are
            feet(a, early)                                   # and the boots stamp while both are out
            for r0, head in early:
                shout(('early',), head, r0 + BAR - head, lift=1 if head == land else None)   # v10: a man too soon (the right), a beat before the pull
            for _, head in late:
                shout(('late',), head, lift=1 if head == land else None)                     # and a man too late (the left); then both, in the middle
            for t, p in ((12, 't1'), (13, 't2'), (14, 'ft'), (15, 'ft')):
                kit(b - BAR + t, p, .84)
        elif sec == 'made fast':
            for k in range(2):
                stomp(a + k * BAR, .72), stomp(a + k * BAR + 8, .62)
            sing('crew', a, line('take up the slack', [(0, 4), (4, 2), (6, 2), (8, 8)], 'Ab3 F3 Eb3 F3'), .8)
            sing('shanty', a, line('and make her fast', [(18, 2), (20, 4), (24, 2), (26, 5.5)], 'Eb3 F3 Eb3 C3'), .8)
            stroke(('gl', 'gr', 'wl', 'wr'), a + 2 * BAR, 'o', 0, 22)
            kit(a + 2 * BAR, 'c', .92), kit(a + 2 * BAR, 'ft', .9)
            put('crew', a + 2 * BAR, 14, 'F3', .9, ph=PH['home'])
            put('shanty', a + 2 * BAR, 14, 'F3', .9, ph=PH['home'])
            haul('rope-l', a + 2 * BAR, 0, dur=14, v=.8)
            haul('rope-r', a + 2 * BAR, 0, dur=14, v=.8)
        start = b
    return ev, marks, start


# 'easy' needs to know where 'both hands' begins before the loop reaches it
marks_next = {}
_t = 0
for _s, _n in FORM:
    marks_next[_s] = _t
    _t += _n * BAR


def in_the_choruses(db, also=None):
    """A fader ride: `db` through each chorus, moving over the half beat before it and the last half beat of it
    (and through the sections of `also`, each by its own figure)."""
    value = lambda name_: db if name_ in ('all together', 'all together again', 'home') else (also or {}).get(name_, 0)
    was = value(FORM[0][0])
    points, beat = [['0b', was]], 0
    for name_, bars in FORM + [('end', 0)]:
        v = value(name_)
        if v != was:
            points += [[f'{beat - 0.5:g}b', was], [f'{beat:g}b', v]]
        beat, was = beat + 4 * bars, v
    return points


def answers(db, only=('late hand', 'early hand', 'both hands')):
    """A lane: `db` through each of the ten verse answers (the third bar of a couplet and the pull after it),
    moving over the half beat before it and the half beat after."""
    points, at = [['0b', 0]], 0
    for name_, bars in FORM:
        if name_ in only:
            for i in range(2 if name_ == 'both hands' else 4):
                c = at + i * 4 * BAR
                points += [[f'{(c + 30) / GRID:g}b', 0], [f'{(c + 32) / GRID:g}b', db], [f'{(c + 54) / GRID:g}b', db], [f'{(c + 56) / GRID:g}b', 0]]
        at += bars * BAR
    return points


def voices(tr):
    """The shantyman and the two crews: as v2, or (v3) with one eq, a trim, and a ride down in the choruses."""
    said = ANSWER.split(';') if ANSWER else None
    crew = CREW + (f' synth.layers.0.consonant_level={said[0]}dB' if said and said[0] else '')
    out = [tr('shanty', SHANTY, SHANTY_GAIN, -.08, sends={'hall': '-16dB'}), tr('crew', crew, CREW_GAIN, .1),
           tr('crew-high', crew, CREW_GAIN, -.2)]
    if not INBAND:
        return out
    bands, trim, ride = INBAND.split(';')[:3]
    if WEIGHT:                              # v9: less box, the same level
        cut = bands.split('|')
        bands = '|'.join(cut[:2] + [WEIGHT.split(';')[1]] + cut[2:])
        trim = f"{float(trim) + float(WEIGHT.split(';')[2]):g}"
    eq = [{'type': 'eq', 'bands': bands.split('|')}]
    points = in_the_choruses(float(ride))
    for t in out:
        t['fx'] = eq
        t['gain'] = {'value': f"{float(t['gain'][:-2]) + float(trim):g}dB", 'mod': [{'src': 'auto.ride', 'amount': 1}]}
        t['auto'] = {'ride': {'points': points, 'curve': 0}}
    if CALL:                                # the shantyman: up outside the choruses, where v3 left him inside them
        t = out[0]
        t['gain'] = {**t['gain'], 'value': f"{float(SHANTY_GAIN[:-2]) + float(trim) + float(CALL):g}dB"}
        t['auto'] = {'ride': {'points': in_the_choruses(float(ride) - float(CALL), {k: -float(CALL) for k in ('count', 'first call', 'easy', 'made fast')}), 'curve': 0}}
    if said and said[1] and float(said[1]):  # v7: the crew comes up through its verse answers
        t = out[1]
        t['gain'] = {**t['gain'], 'mod': t['gain']['mod'] + [{'src': 'auto.answer', 'amount': 1}]}
        t['auto'] = {**t['auto'], 'answer': {'points': answers(float(said[1])), 'curve': 0}}
    return out


def with_the_crew(t, lifts):
    """v10: a man's fader comes up for the shouts he gives WITH the crew (one voice among seven there, and the whole band lands)."""
    if lifts:
        points = [['0b', 0]]
        for at, dur, db in sorted(lifts):
            points += [[f'{(at - 2) / GRID:g}b', 0], [f'{(at - 1) / GRID:g}b', db], [f'{(at + dur + 1) / GRID:g}b', db], [f'{(at + dur + 2) / GRID:g}b', 0]]
        t['gain'] = {'value': t['gain'], 'mod': [{'src': 'auto.with', 'amount': 1}]}
        t['auto'] = {'with': {'points': points, 'curve': 0}}
    return t


def tracks_of(ev):
    def tr(name_, patch, gain, pan=0, out=None, fx=None, sends=None):
        d = {'name': name_, 'patch': patch, 'gain': gain, 'pan': pan, 'notes': sorted(ev[name_], key=lambda n: n['at'])}
        if out: d['out'] = out
        if sends: d['sends'] = sends
        if fx: d['fx'] = fx
        return d
    lift = [{'type': 'eq', 'bands': ['peak cutoff=700 q=0.9 gain=2.5dB']}]
    tight = f" fx.1.tight={WEIGHT.split(';')[0]}" if WEIGHT else ''     # v9: more of the low string into the amp
    dip = [{'type': 'eq', 'bands': ['peak cutoff=380 q=1 gain=-3dB']}]
    air = [{'type': 'eq', 'bands': ['highshelf cutoff=9000 gain=-2dB']}]
    hair = [{'type': 'eq', 'bands': ['peak cutoff=180 q=0.8 gain=-8dB']}]
    if TEETH:                                # v12: the palm opens, the lift goes, the wall pair on the engine's cabinet
        palm, mic, tgain, teq, wmic, wcones, wdist, wgain, weq, _ = TEETH.split(';')
        twin = lambda cone: f'ct-twin fx.1.model=gojira{tight} fx.2.mic={mic} fx.2.cone={cone} synth.filters.0.cutoff.mod.0.amount={palm}'
        wall = lambda side: f'ct-wall-stop-{side} fx.3.mix=0 ' + ' '.join(f'fx.4.bands.{i}.gain=0dB' for i in range(4))
        speaker = lambda cone: [{'type': 'cab', 'model': '4x12-modern', 'mic': float(wmic), 'distance': float(wdist), 'cone': int(cone)},
                                {'type': 'eq', 'bands': weq.split('|')}]
        lift = [{'type': 'eq', 'bands': teq.split('|')}]
        cl, cr = wcones.split(',')
        guitars = [tr('gl', twin(92), tgain, -1, 'gtrs', lift), tr('gr', twin(93), tgain, 1, 'gtrs', lift),
                   tr('wl', wall('l'), wgain, -.75, 'gtrs', speaker(cl)), tr('wr', wall('r'), wgain, .75, 'gtrs', speaker(cr))]
    else:
        guitars = [tr('gl', 'ct-twin fx.1.model=gojira' + tight + ' fx.2.mic=0.5 fx.2.cone=92', '0.7dB', -1, 'gtrs', lift),
                   tr('gr', 'ct-twin fx.1.model=gojira' + tight + ' fx.2.mic=0.5 fx.2.cone=93', '0.7dB', 1, 'gtrs', lift),
                   tr('wl', 'ct-wall-stop-l', '-3.5dB', -.75, 'gtrs', dip), tr('wr', 'ct-wall-stop-r', '-3.5dB', .75, 'gtrs', dip)]
    return [
        *guitars,
        *([{**tr('clean-' + side, SQUEEZE.split(';')[0], SQUEEZE.split(';')[1], pan, sends={'hall': SQUEEZE.split(';')[3]}), 'name': 'squeeze-' + side}
           for side, pan in (('l', -.6), ('r', .6))] if SQUEEZE else
          [tr('clean-l', 'ct-clean', '-6dB', -.6, sends={'hall': '-12dB'}), tr('clean-r', 'ct-clean', '-6dB', .6, sends={'hall': '-12dB'})]),
        *([{**tr('tune-' + side, SQUEEZE.split(';')[0], TUNE.split(';')[0] if side == 'l' else f"{float(TUNE.split(';')[0][:-2]) + float(TUNE.split(';')[3]):g}dB",
                 sign * float(TUNE.split(';')[1]), fx=[{'type': 'eq', 'bands': TUNE.split(';')[4].split('|')}] if TUNE.split(';')[4] else None,
                 sends={'hall': TUNE.split(';')[2]})} for side, sign in (('l', -1), ('r', 1))] if TUNE else []),
        tr('bass', 'ct-bass', '0.5dB', 0, 'low'),
        tr('kick', 'ct-kit', '2dB', 0, 'drums', [{'type': 'eq', 'bands': ['peak cutoff=4500 q=0.8 gain=10dB']}]),
        tr('snare', 'ct-kit', '3.5dB', 0, 'drums', [{'type': 'eq', 'bands': ['highshelf cutoff=7000 gain=-3dB']}], {'oh': '-1.5dB', 'snr': '-10dB'}),
        tr('toms', 'ct-kit', '4dB', 0, 'drums', sends={'oh': '-1.5dB'}),
        tr('cym', 'ct-kit', '-4.5dB', .3, 'drums', air, {'oh': '4.5dB'}),
        tr('hat', 'ct-kit', '14dB', -.4, 'drums', air, {'oh': '4.5dB'}),
        *voices(tr),
        # (the big lyre played this high is mostly fundamental: at a pull it stood over the whole band at 120-250 Hz
        # and 8 to 14 dB under it from 500 Hz up. Eight dB off its body, so that what is heard is the hair)
        *([tr('rope-l', HAWSER.format(ROPE.split(';')[2]), ROPE.split(';')[0], -float(ROPE.split(';')[1]), fx=hair),
           tr('rope-r', HAWSER.format(ROPE.split(';')[2]), ROPE.split(';')[0], float(ROPE.split(';')[1]), fx=hair)] if ROPE else []),
        *([tr('deck', 'deck', DECK.split(';')[0], 0, 'boards')] if DECK else []),
        *([with_the_crew(tr('man-' + w, BARK + f' synth.layers.0.tract={size}', MAN.split(';')[0], side * float(MAN.split(';')[1]),
                            fx=[{'type': 'eq', 'bands': MAN.split(';')[8].split('|')}], sends={'hall': MAN.split(';')[9]}), ev['lift:man-' + w])
           for w, side, size in zip(('late', 'early'), (-1, 1), MAN.split(';')[6].split(':'))] if MAN else []),
    ]


def build():
    ev, marks, end = make()
    low = [{'type': 'eq', 'bands': ['peak cutoff=44 q=1.5 gain=-7dB', 'peak cutoff=90 q=1 gain=7.5dB', 'peak cutoff=350 q=1 gain=-8dB', 'peak cutoff=1500 q=1 gain=4dB']},
           {'type': 'compressor', 'threshold': '-26dB', 'ratio': 8, 'attack': '12ms', 'release': '120ms', 'makeup': '2.5dB'},
           {'type': 'eq', 'bands': ['peak cutoff=170 q=1.2 gain=-3dB']}]
    buses = {
        'hall': {'fx': ['reverb kind=hall decay=3.2s mix=1 predelay=30ms low_cut=150']},
        'drums': {'fx': ['reverb kind=room decay=0.7s mix=0.1 predelay=8ms',
                         {'type': 'glue', 'threshold': '-24dB', 'ratio': 2.5, 'attack': '20ms', 'release': '140ms', 'knee': 6.0},
                         'clip drive=0dB ceiling=-13dB',
                         {'type': 'eq', 'bands': ['peak cutoff=400 q=0.8 gain=-6dB', 'peak cutoff=5500 q=0.9 gain=1dB', 'highshelf cutoff=9000 gain=-2dB', 'lp cutoff=14250 q=0.8']}]},
        'oh': {'fx': ['reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6', {'type': 'eq', 'bands': ['lp cutoff=14250 q=0.8']}]},
        'snr': {'fx': [{'type': 'eq', 'bands': ['peak cutoff=300 q=0.7 gain=-12dB']}]},
        'gtrs': {'fx': [{'type': 'eq', 'bands': ['peak cutoff=330 q=1.2 gain=-2dB']}, 'reverb kind=room decay=0.35s mix=0.06 predelay=6ms']},
        'low': {'fx': low},
    }
    lift = float(BUILT.split(';')[4]) if BUILT else float(INBAND.split(';')[3]) if INBAND else 0
    if lift:
        for name_ in ('gtrs', 'low', 'drums', 'oh', 'snr'):
            buses[name_]['fx'] = buses[name_]['fx'] + [{'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.lift', 'amount': 1}]}}]
            buses[name_]['auto'] = {'lift': {'points': in_the_choruses(lift), 'curve': 0}}
    said = ANSWER.split(';') if ANSWER else None
    if said and said[2] and float(said[2]):   # v7: the guitars give way under each verse answer
        buses['gtrs']['fx'] = buses['gtrs']['fx'] + [{'type': 'gain', 'gain': {'value': '0dB', 'mod': [{'src': 'auto.duck', 'amount': 1}]}}]
        under = answers(float(said[2]), ('early hand',)) if LETGO else answers(float(said[2]))   # v8: only where the band is still under the crew
        buses['gtrs']['auto'] = {**buses['gtrs'].get('auto', {}), 'duck': {'points': under, 'curve': 0}}
    doc = {'about': 'Take Up the Slack — chirpers, Common Time, track fifteen. A hauling song: the crew pulls in four, the riff is fifteen long, then seventeen, and each verse the slack between them is taken up.',
           'tempo': BPM, 'seed': 1, 'length': f'{end // GRID}b', 'tail': '3s', 'ceiling': '-1dB', 'loudness': float(BUILT.split(';')[5]) if BUILT else float(INBAND.split(';')[4]) if INBAND else float(ROPE.split(';')[3]) if ROPE else -10, 'event_stable': True,
           'buses': buses, 'master': {'fx': [{'type': 'eq', 'bands': ['hp cutoff=24']}, {'type': 'gain', 'gain': '2.7dB'}]},
           'tracks': tracks_of(ev)}
    if DECK:
        doc['patches'] = {'deck': {'kit': {piece: {'patch': boot(ring), 'pitch': note, 'pan': pan} for piece, _, _, note, pan, ring in BOOTS}}}
        # the deck: a short room, then the kit bus's clip, so no one stamp stands over the rest (five thuds add up by chance)
        doc['buses']['boards'] = {'fx': [{'type': 'eq', 'bands': ['hp cutoff=38']}, 'reverb kind=room decay=0.45s mix=0.14 predelay=5ms',
                                         f"clip drive=0dB ceiling={os.environ.get('C10T15_DECKCLIP', '-12dB')}"]}
        if DECK.split(';')[4]:
            doc['loudness'] = float(DECK.split(';')[4])
    if said and said[3]:
        doc['loudness'] = float(said[3])
    if LETGO and LETGO.split(';')[3]:
        doc['loudness'] = float(LETGO.split(';')[3])
    if WEIGHT:
        doc['loudness'] = float(WEIGHT.split(';')[3])
    if MAN and MAN.split(';')[7]:
        doc['loudness'] = float(MAN.split(';')[7])
    if KICK:
        drum, note, gain, decay, click, target = KICK.split(';')
        doc['patches'] = {**doc.get('patches', {}), 'slack-kit': {'extends': 'ct-kit', 'kit': {'k': {'pitch': drum}}}}
        at = next(i for i, t in enumerate(doc['tracks']) if t['name'] == 'kick')
        doc['tracks'][at]['patch'] = 'slack-kit'
        if click:
            doc['tracks'][at]['fx'] = [{'type': 'eq', 'bands': [f'peak cutoff=4500 q=0.8 gain={click}dB']}]
        if note:
            doc['patches']['slack-chest'] = {'extends': '808', 'synth': {'layers': ['sine'], 'pitch': {'value': 0, 'mod': []}, 'drive': 0, 'filters': [],
                                                                       'amp': {'a': '2ms', 'd': f'{decay}ms', 's': 0, 'r': '20ms', 'curve': 3}},
                                             'play': {'mono': False, 'glide': '0ms', 'gate': 1}}
            chest = {'name': 'chest', 'patch': 'slack-chest', 'gain': gain, 'pan': 0,
                     'notes': [{'at': n['at'], 'len': round(float(decay) / 1000 * BPM / 60, 4), 'pitch': note, 'vel': n['vel']} for n in doc['tracks'][at]['notes']]}
            if lift:                         # it goes straight to the mix, past the kit's bus and its clip: so it takes the choruses' lift itself
                chest['gain'] = {'value': gain, 'mod': [{'src': 'auto.lift', 'amount': 1}]}
                chest['auto'] = {'lift': {'points': in_the_choruses(lift), 'curve': 0}}
            doc['tracks'].insert(at + 1, chest)
        if target:
            doc['loudness'] = float(target)
    if TEETH and TEETH.split(';')[9]:
        doc['loudness'] = float(TEETH.split(';')[9])
    if LONG:
        home = sum(n for s_, n in FORM[:[s_ for s_, _ in FORM].index('home')]) * BAR
        for names, db in ((('gl', 'gr'), float(LONG.split(';')[3])), (('wl', 'wr'), float(LONG.split(';')[4]))):
            if db:
                span = [['0b', 0], [f'{(home - 2) / GRID:g}b', 0], [f'{home / GRID:g}b', db],
                        [f'{(home + int(LONG.split(";")[2]) * BAR - 2) / GRID:g}b', db], [f'{(home + int(LONG.split(";")[2]) * BAR) / GRID:g}b', 0]]
                for t in doc['tracks']:
                    if t['name'] in names:
                        t['gain'] = {'value': t['gain'], 'mod': [{'src': 'auto.long', 'amount': 1}]}
                        t['auto'] = {**t.get('auto', {}), 'long': {'points': span, 'curve': 0}}
        if LONG.split(';')[5]:
            doc['loudness'] = float(LONG.split(';')[5])
    if TUNE and TUNE.split(';')[5]:
        doc['loudness'] = float(TUNE.split(';')[5])
    return doc, marks


def the_sub_changes_hands(doc):
    """v15: the bass leans on its octave and the kick, shorter, takes the floor."""
    bass, decay, band, click, target = SUB.split(';')
    for t in doc['tracks']:
        if t['name'] == 'bass' and bass:
            t['patch'] += ' ' + bass
        if t['name'] == 'kick':
            if decay:
                t['patch'] += f' kit.k.patch.synth.amp.d={decay}'
            bands = t['fx'][0]['bands']
            if click:
                assert bands[0].startswith('peak cutoff=4500 '), bands
                bands[0] = f'peak cutoff=4500 q=0.8 gain={click}dB'
            if band:
                t['fx'][0]['bands'] = bands + [band]
    if target:
        doc['loudness'] = float(target)


def dump(d):
    return '\n'.join('tracks:\n' + '\n'.join('  - ' + json.dumps(t) for t in v) if k == 'tracks' else k + ': ' + json.dumps(v) for k, v in d.items()) + '\n'


if __name__ == '__main__':
    doc, marks = build()
    if SUB:
        the_sub_changes_hands(doc)
    if os.environ.get('C10T15_SHOW'):
        for sec, bars in FORM:
            t = marks[sec]
            print(f'{sec:20s} bar {t // BAR + 1:3d}  {t / GRID * 60 / BPM:7.2f} s  {bars} bars')
    else:
        OUT.write_text(dump(doc))
