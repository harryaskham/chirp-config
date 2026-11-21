#!/usr/bin/env python3
"""The Other Hand: two guitarists read the same strip from opposite ends.
The strip holds 19 sixteenths; a drummer outside it counts quarters in four.
An attack is reflected about tick 9, including its pitch and articulation;
this is a backwards performance, not backwards audio. --map prints real times.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

BPM, GRID, STRIP = 104, 4, 19
# section lengths are strips, not bars
FORM = [('pencil', 4), ('ink', 12), ('opposite', 16), ('carbon', 8),
        ('thumbprint', 10), ('raised', 12), ('turn over', 12), ('one hand', 8), ('signed', 3)]
# position, semitones above F1, type. Four open notes, five dry consonants.
ROW = [(0,0,'o'), (2,0,'m'), (3,3,'o'), (6,0,'m'), (7,0,'m'),
       (10,1,'o'), (13,0,'m'), (15,7,'o'), (17,0,'m')]
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t12.yaml'
# v9: per-note trim of the pedal hat that keeps counting under the last four strips.
FOOT_COUNT = '-3dB'
# Seventeen quiet seconds lower the song's integrated loudness by 0.15 LU. Ask for
# that much less, so the mastering gain on everything before the page is v8's.
PAGE_LOUDNESS = -10.15
# v10: the ribbon's one long note over the opposed guitars, against its track's level.
PALINDROME_TRIM = '-3dB'
# v11 (chirper-alpha, whole song): THE KIT GETS THE ALBUM'S EAR. The song had been read against the album's eleven
# records once, at v1, on one stretch (+3.3 dB at 250-500 Hz, 2.4 short at 60-120), and nothing was done. Read whole
# and by part at v10 (stembal, each band as a share of the mix, against the records' passages without a voice): every
# stretch with a backbeat stood 2.6 to 6.1 dB over at 250-500 Hz (the unison opening 1.2) and 1.7 to 3.1 short at
# 60-120 Hz. Part by part, the SNARE held half of 250-500 Hz wherever it plays two and four, and the kick most of the
# rest; the kick is also 56 to 77% of 60-120 Hz. Every other song of the album that uses this kit cuts its bus at
# 400 Hz (4 to 6 dB); this one, alone, did not. So the drums' bus gets the album's eq, after its clip: the cut at
# 400 Hz, the small lift at 5.5 kHz and the shelf over 9 kHz as Common Time's kit has them, and one band of its own:
# a lift at 92 Hz, because here the foot plays only the four open notes of a strip and the bass only two, so the
# low end is few strokes and each has to carry more. No note changes.
# (Benched: the same lift on the kick's own track, before the bus's compressor and clip, bought 0.5 dB of the band
# for 3 dB of eq; on the bus after them 3 dB buys 1.0. At 4.5 dB the tuned toms' answers at 3:36 read 1.4 over.)
KIT_EQ = ['peak cutoff=92 q=1.2 gain=3.5dB', 'peak cutoff=400 q=0.8 gain=-6dB', 'peak cutoff=5500 q=0.9 gain=1dB', 'highshelf cutoff=9000 gain=-2dB']
# With the snare's body out of the way the ribbon's long note (v10, mine) was nearly all of its own octave (1.0 dB
# under the mix there) and that stretch still read 4.1 over. Two dB less: 14.7 under the whole mix, where the
# signature at the close stands (14.1), and still the strongest partial near it in nine frames of ten.
PALINDROME_TRIM_KIT = '-5dB'
# v12: the steel's notes on the four strips on C. A fifth up, all four of its notes lie inside 250-500 Hz, where it
# already held three quarters of the band: at its own level those strips read 7.6 dB over the eleven records there
# (6.3 on F) and the steel stood 0.6 dB further forward against the band (K). With this trim on each of those notes
# the band reads what it read on F.
STEEL_ON_C = '-1.5dB'
# v13 (chirper-three, palette): THE THUMBPRINT IS LEFT BY THUMBS. In 'thumbprint' (1:49.6-2:17.0) a wordless voice
# calls and a clean guitar answers with the same four notes read from the other end; nothing else plays until two
# toms join half way. The answer moves from the clean guitar (ct-clean, a staple of six songs here) to a THUMB
# PIANO: the library's kalimba, on no other song of the record. Same forty notes at the same times and
# velocities, two octaves up, where a kalimba lives (A-flat 4 to E-flat 5): the answer was an octave under the
# voice and is now an octave over it, and where the voice climbs for two strips (2:06-2:11.5) they share an octave.
# And it is played as the instrument is: two thumbs, the tines laid out alternately left and right as they rise
# (A-flat left, A right, B left, E-flat right), a track to a thumb. So the tune read forwards is LEFT, LEFT, RIGHT,
# RIGHT and read backwards RIGHT, RIGHT, LEFT, LEFT: turning the strip over swaps the hands. The song's other thumb
# is the bass player's (from 1:06, on its card); this is the section its name was waiting for. The clean guitar
# still opens the song, rings the fold's F and closes the page.
# (Benched, raw seed 0. FIRST: the same notes at the guitar's own pitch (A-flat 2 to E-flat 3): a kalimba down there
# is nearly a pure fundamental at 104-156 Hz, a soft bass and not a tine, and at -2 dB it was 20 dB over the guitar
# it replaced. An octave up it stood in the voice's own octave. KEPT, two octaves up at -23.5 dB: alone it is within
# 1.1 dB of the guitar (K, first 150 ms of each note) and the voice stands 8.6 dB over it where it stood 8.3 over
# the guitar. The tine's overtone is lifted 8 dB: 12 to 18 dB under the fundamental in a note's first 30 ms, where
# the library's is 20 to 26. The section loses the guitar's pick: -1.2 dB at 2-4 kHz and -2.7 at 4-8 kHz; every
# band under 2 kHz is within 0.6 dB.)
# the patch (the song's chamber in place of its own room ; each tine rings 0.6 s after the thumb leaves it ; the
# overtone's level) ; each thumb's track gain ; how far each sits from centre ; semitones over the guitar's notes.
TINES = ('kalimba fx.0.mix=0 synth.amp.r=600ms synth.layers.2.level.value=-18dB', '-23.5dB', .4, 24)
# With the swap the song reads 0.007 LU louder to the meter, so at v12's target every other bar came out 0.004 to
# 0.010 dB quieter (seeds 0 and 11). Ask for that much more.
THUMBS_LOUDNESS = -10.143
# v14 (chirper-alpha, palette): THE CARBON IS TAKEN ON A SECOND AMP. 'Carbon' (1:27.7-1:49.6) is one guitarist and
# eight strips, and it has always gone page, copy, page, copy: on the first strip of each pair the hand plays the
# whole strip, on the second only its four open notes, the strokes that were pressed hard enough to go through (the palm
# strokes do not transfer), while the drummer's tuned heads take over the voice's words. But page and copy were
# the same sound: the same saturated amp, which presses every stroke alike. Now the copy is taken on a second amp
# from the same guitar and the same cabinet: a clean one, short of breaking up. The four notes of each odd strip
# move to it (sixteen notes; nothing added, nothing moved). On it a stroke shows its pressure: the note speaks,
# then falls, where the ink holds level; it is fainter and has no fizz. The page strips, the voice, the heads,
# the bass and the foot are as they were. It is the song's first clean electric note that is not the high clean
# guitar's: 'thumbprint', all clean, follows. (The clean voicing is on this record otherwise only inside ct-glass,
# in three other songs.)
# (Benched, raw seed 0, the sixteen notes alone. Turning the ink amp down does nothing: at gain 0.3 without its
# boost, or on the crunch voicing at 0.5, the notes read within 0.4 dB, 30 Hz of centroid and 0.3 dB of crest of
# the ink: the compressor and screamer in front keep it saturated. The clean voicing at 0.6: centroid 2110 ->
# 1770 Hz, 1.4 dB less of its power over 2 kHz, crest 12.5 -> 15.5 dB, and the second half of each note 3.3 dB
# under the first where the ink's is 1.0 under. At 0.35 it is a bare pick (crest 17.9); with the microphone moved
# off the cone it goes dull (1360 Hz). Kept: 0.6, on the ink's own cone. At the ink's own fader the clean notes
# read 5.3 dB under it (K); at 3.8 dB they stand 2.0 under: a copy is fainter, but it has to read.)
# the amp ; the copy's track gain.
COPY = ('ct-twin fx.1.model=clean fx.1.gain=0.6 fx.1.boost=0dB fx.2.cone=37', '3.8dB')
# The copy strips are quieter to the meter (the fizz is most of what it hears), so at v13's target every other bar
# came out 0.042 dB louder (seed 0). Ask for that much less.
COPY_LOUDNESS = -10.185
# v15 (chirper-alpha): HARRY'S THREE ANSWERS, 19 Nov 02:31, and the guitars.
# (1) 'Can you follow the ringing line as it changes hands?' (the pedal steel in 'turn over', my v2; asked at v11
# beside the same bars with the steel taken out): "Prefer both heavy". So in 'turn over' (2:49.9-3:22.8) the hand
# reading back is a heavy guitar again, as it was in v1: both hands heavy, one reading the strip forwards and one
# back, changing chairs on every strip. The steel is out of the song. v12's move to C on the last four strips
# stands, now on both guitars. --with-steel gives v14.
# (2) 'Do the bass pops help you follow the two guitars?' -> "Keep the pops": kept. (3) 'Can you follow both
# guitars when one turns back?' -> "I can follow both": kept.
HEAVY_LOUDNESS = -10.185
# THE TWO HANDS' RIG (the round was drawn as an instrument round; Harry, 19 Nov: "better guitars"). With both hands
# heavy the song is two guitars from end to end, and against the album's eleven records its guitar stretches all
# read the same way (finished file, each band as a share of the mix): 500 Hz-1 kHz 1.6 to 2.0 dB short, 2-4 kHz 2.2
# to 2.7 over, 4-8 kHz 0.6 to 1.4 short. In those stretches the two guitars ARE those bands (raw, 'ink': within 0.8
# dB of the whole mix from 500 Hz to 4 kHz, two thirds of 4-8 kHz), so it is the rig: a honk at 3 kHz with too
# little body under it and too little edge over it. Three changes, each benched on the guitars alone and then read
# in the mix:
#   the amp     the album's own voicing (`gojira`, as tracks 4, 7, 8, 9, 14 and 15 have it): +1.5 dB at 500 Hz-1 kHz,
#               -3.2 at 120-250 and -1.7 at 250-500 (the boxiness under the body)
#   the mic     nearer the cone's centre (0.4 -> 0.25): +1.8 dB at 4-8 kHz. (The album's usual 0.5 goes the other
#               way: benched, it cost this song a further 1.1 dB there.)
#   the honk    one cut at 2.6 kHz after the cabinet: 2-4 kHz -1.5 dB net of the brighter mic
#   THE FADERS STAY where they were. The pair alone reads 1.07 dB quieter on the new rig; a first take gave that
#   back at the fader and the mix read worse for it (2-4 kHz only 0.5 dB better, and the stretches were already
#   1 to 2.5 dB short at 60-120 Hz, which is the kit and bass the guitars stand over).
# Not kept: the amp's presence at 0.7 (0.1 dB); treble 0.35 (took 4-8 kHz down with 2-4); a shelf over 5 kHz
# (the cut under it ate it). The second amp of 'carbon' (the copy) is not touched. --stock-rig keeps the old rig.
HANDS_RIG = ('fx.1.model=gojira fx.2.mic=0.25', None, ['peak cutoff=2600 q=1.4 gain=-3.5dB'])

# v16 (chirper-one, section w7, 2:55.4-3:06.3): THE PAGE IS TURNED OVER. The song reads its strip from both ends; it
# had never turned it upside down. In 'turn over', after the first pair of strips, the page is turned top to bottom
# for two pairs (four strips): every open chord stands as far BELOW the low F as it stood above it, brought up an
# octave so it stays on the neck. A flat (a minor third up) becomes D (a minor third down), G flat (a semitone up)
# becomes E (a semitone down), C (a fifth up) becomes B flat (a fifth down). The rhythm, the palm strokes, the
# chairs, the bass's F and the kit are as written; both hands are heavy, as Harry chose. What turns is the colour:
# the strip's F, A flat, G flat, C is the dark side of F; F, D, E, B flat is its bright side. Where the two hands
# meet (ticks 3 and 15) they used to make A flat major seventh over the bass's F; turned over they make B flat
# major seventh over it. Then the page is turned back for the last pair on F, whose closing C is left ringing and
# becomes the ground (v12), and the section ends on C as before. A crash marks each turn of the page.
# The strips of 'turn over' read upside down (first, one past the last) ; the crash's velocity on each turn (0: no
# crash) ; the loudness target. --without-turned-page gives v15.
TURNED = (2, 6, 0.8, -10.185)
# v17 (chirper-alpha, section w2, 0:27-0:55; the change is one strip, 0:41.1-0:43.85): THE OTHER HAND READS IT ALONE
# FIRST. 'Opposite' (0:43.85) is the song's subject arriving: the right hand reads the strip from the far end while
# the left reads on. But the listener has never heard the strip read backwards by itself: at the first note of it
# both readings are already going, and for the three strips before it the two guitars are in plain unison (the
# map's most static stretch of this window). The backwards strip is only ever heard alone at 3:52.9, on the facing
# page, when the song is over.
# So on the last strip of 'ink' the band gives the downbeat (the left hand's F, the bass, the foot) and lifts off.
# The right guitar, on its own side, reads the whole strip from the far end, alone: C, G flat, A flat, F where the
# riff goes F, A flat, G flat, C, and its five palm strokes in their mirrored places. Only the hat goes on counting
# quarters in four, as it does all song: the count the strip turns against, heard bare for once. Then the crash,
# and both hands read at once. What is played in the break is note for note what the right hand plays in every
# strip of 'opposite'; nothing is new but the silence round it.
# How many of ink's last strips the right hand reads alone ; the hat keeps counting through them ; the band gives
# the downbeat ; the loudness target. --without-first-reading gives v16.
# (One guitar for 2.6 s lowers the song's integrated loudness: at v16's target every other bar came out 0.03 dB
# louder where the band is loud and 0.065 where it is quiet. Asking for 0.065 less overshot by as much again: here
# a decibel of target moves a quiet bar 1.9 dB and a loud one 0.9. So 0.035 less.)
READING = (1, True, True, -10.22)
# v18 (chirper-zero, instrument round): THE TWO HANDS GET A CHEST. The song is two guitars, and for 2.7 s at 0:41 and
# 16 s at the close it is ONE guitar and a count. Read three ways at v17:
#   ALONE against the records' guitar heard alone (tools/cabspec.py, the pair in 'opposite'): 8.3 dB short at
#     141-282 Hz, the worst band it has; mean distance 3.34 dB.
#   BY PART against the eleven records' guitar stems, with the groups named (guitar=left,right,copy; four stretches):
#     120-250 Hz 7.5 dB short (the records' middle half is 1.5 wide), while the KIT stood 3.0 over there and 5.1 over
#     at 250-500: the foot held half of the mix's 120-250 Hz and the guitars about a sixth.
#   THE MIX on the no-voice rows: within 1.2 dB at 120-250 Hz everywhere: the kick was standing in for the guitars'
#     chest, so the mix did not show it. (v15's amp voicing took 3.2 dB out of the guitars there; its read was
#     against the records' passages WITH a voice, the only read there was that night.)
# So the band changes hands, and the mix stays where it is:
#   the two hands   after the cabinet, before v15's cut: +7 dB at 180 Hz (q 1), and 1.5 dB off at 800 Hz, which is
#                   the rig's nose (6.7 over the record's lone guitar) and gives back what the chest's share took
#                   from the mix's 500 Hz-1 kHz
#   the kit's bus   3 dB off at 190 Hz (q 1.2), after the album's eq: the foot gives the guitars their band
# AFTER: alone 141-282 Hz -8.3 -> -3.2, mean distance 3.34 -> about 2.4. By part the guitars 120-250 Hz -7.5 ->
# -1.8, 250-500 -2.5 -> -0.2; the kit 120-250 +3.0 -> +0.7, 250-500 +5.1 -> +3.7. The mix: see the round note.
# Benched and not kept: the amp's tight filter at 150 Hz (141-282 Hz only 2.8 dB better, the rest as it was); the
# rig as it was before v15 (nearer the record alone, 2.34, but it brings back the honk v15 cut and is 1.8 dB darker
# where the mix is already short); the strings bus's lift at 730 Hz taken out (the mix went 0.7 short at 500 Hz-
# 1 kHz in 'ink' and 'turn over'); the chest with no give from the kit (the mix 1.0 to 1.7 over at 120-250).
# the bands before v15's on each hand ; one more band on the kit's bus ; the loudness target (with the kit 3 dB
# lighter at 190 Hz the song measures quieter and at v17's target the master lifted everything 0.31 dB: 'pencil',
# which has neither guitar nor kit, is the yardstick. THE MASTER'S GAIN JUMPS here: at -10.3075 'pencil' is 0.11 dB
# under v17's, at -10.305 it is 0.10 over, and nothing between; -10.32 is the low side, clear of the jump).
# --without-chest gives v17.
CHEST = (['peak cutoff=180 q=1 gain=7dB', 'peak cutoff=800 q=1.2 gain=-1.5dB'], 'peak cutoff=190 q=1.2 gain=-3dB', -10.32)
# v19 (chirper-three, palette): THE COUNT HAS ANOTHER HAND TOO. In 'opposite' (0:43.85-1:27.7) everything is read
# from both ends at once: the strip, by the two guitars; the meetings, by the bass and then the thumb. One thing is
# not: the count. The drummer's hat counts quarters in four straight through, from outside the strip. Read each
# strip's count from its far end, as the right hand reads its notes (a stroke on tick t goes to tick 18 - t), and
# because a strip is nineteen sixteenths the answer is not the count again. On every other strip it falls exactly
# BETWEEN the beats, and on the strips between those it falls exactly ON them. So for one strip (2.7 s) count and
# mirror make eighths, hat and answer in turn, and for the next they strike together in quarters; eight times.
# The seam of every strip, which nothing in the kit has ever marked, can now be heard as that change.
# THE PART is clapped: one pair of hands, on the right, beside the guitar that reads backwards. No other song on
# the record has clapping hands (Carrying Capacity's drum machine has a clap voice, a circuit's). THE PATCH is the
# song's own (the library's cajon kit has a clap, a 70 ms burst of noise over 900 Hz; a single clap is shorter and
# has a note of its own, the air between the palms): 20 ms of noise through a peak where cupped hands sound
# (1.3 kHz: read against 1.0, 1.7 and 2.4), in a small room, a few milliseconds loose in time.
# MEASURED (raw, a stroke's first 30 ms against everything else, K): the hat -12.5 dB, the snare +4.2; a clap
# between the beats -6.1, on the beat -11.0. THE TARGET: at v18's -10.32 the master's gain jumped 0.1 to 0.23 dB on
# seed 0 (not on seeds 11 and 1); at -10.34 every other bar is within 0.017 dB on all three.
# the patch ; the fader ; where the clapper stands ; velocity on the mirror of the bar's first beat and elsewhere ;
# the loudness target (None: unchanged). --without-palmas gives v18.
PALMAS = ({'kit': {'pa': {'patch': {'synth': {'amp': {'a': '0.1ms', 'curve': 3, 'd': '20ms', 'r': '10ms', 's': 0},
                                              'filters': ['hp cutoff=500', 'peak cutoff=1300 q=1.6 gain=10dB', 'lp cutoff=7000'],
                                              'layers': [{'type': 'noise'}]}}}},
           'play': {'vel_sens': 0.6, 'humanize': {'time': '4ms', 'vel': 0.06}},
           'fx': ['reverb kind=room decay=0.3s mix=0.18 predelay=3ms']},
          '-4dB', .45, (.9, .74), -10.34)


def pitch(m): return PITCH[m % 12] + str(m // 12 - 1)
def strip(back=False):
    return sorted(((STRIP-1-t if back else t), p, k) for t,p,k in ROW)

# v20 (chirper-one, instrument round: the snare drum, every stroke; v18's and v19's handoffs asked for it): THE SNARE
# LOSES ITS BOX AND GETS ITS CRACK. Read alone at its own strokes the way tools/drumpunch.py reads a snare on a
# record, the album kit's snare stood here at body against crack +2.0 dB (six records' drums: -3.2, between -4.4 and
# +0.2 on five of them) and wires against crack +2.8 (records 0.0, -0.6 to +1.4): a box with hiss over it. By part
# against the records' drums the kit was 4.1 over at 250-500 Hz and 5.4 over at 500 Hz-1 kHz, 70 and 78% of it the
# snare, and 2.1 short at 4-8 kHz. On Its Hinge's snare (its v19: the same drum, the same fault) read TOO THIN here
# with that song's settings (body against crack -6.3; -4.1 with this kit bus's cut at 190 Hz taken out: v18's chest
# round took 2.2 dB of the snare's body with it, and the strokes are no softer here). So, fitted here: the body's
# lift at 200 Hz 5 -> 1.5 dB; a harder stroke (contact 0.6 -> 0.35) with more slap (1.2 -> 1.6); the wires tighter
# and voiced lower (0.85 -> 0.95, 7 kHz -> 5 kHz), so they fill 4-8 kHz; 3 dB off the drum's box at 650 Hz on its
# track; its fader 2 -> 1 dB, so a stroke is as loud as it was. No note changes; nothing else is touched.
# BUILT, RENDERED AND NOT KEPT (fields four and five): each hand giving back 3 dB above 4 kHz with its fader 0.45 up
# ('highshelf cutoff=4000 gain=-3dB', 0.45). By part the hands hold 4.3 dB more of 4-8 kHz than the records' guitars
# and 8.1 more of 8-16 kHz, and with that the three fullest sections read nearer the records; but where a guitar is
# nearly alone ('one hand', 'facing page', 'carbon') the mix is already short up there and went shorter. It belongs
# with the cymbals' round (chirper-zero's v18 handoff: "when the cymbals have their top").
# the snare's settings ; a band on the snare's track ; its fader ; a band added to each hand's eq (None: none) ;
# dB on each hand's fader ; the loudness target (None: unchanged). --without-crack gives v19.
CRACK = (' kit.s.patch.synth.filters.1.gain=1.5dB kit.s.patch.synth.layers.0.contact=0.35 kit.s.patch.synth.layers.0.slap=1.6'
         ' kit.s.patch.synth.layers.0.wire_tone=5000 kit.s.patch.synth.layers.0.wires=0.95',
         'peak cutoff=650 q=1 gain=-3dB', '1dB', None, 0, None)

# v21 (chirper-two, section w3, 0:55-1:23, and on to the end of 'opposite' at 1:27.7): THE OTHER FOOT. In 'opposite'
# everything has come to be read from both ends: the strip by the two hands, the meetings by the bass and the thumb,
# the count by the clapper (v19). One thing still sided with the left hand: the drummer's foot. The bass drum plays
# the forward reading's four open notes (ticks 0, 3, 10, 15) and nothing of the right hand's. A drummer has two feet.
# FROM STRIP 4 (0:54.8, where the ribbon starts to draw the line both hands make) the other foot reads from the far
# end: the right hand's open notes, 3, 8, 15, 18. The hands meet at 3 and 15 and one foot is enough there, so what
# is new is two strokes a strip, at 8 and 18. The six kicks, 0 3 8 10 15 18, are their own mirror, and they are the
# six moments the ribbon's line stands on. To the ear: a stroke into every strip's first beat (18, then 0), which
# marks the seam, and a pair either side of the centre nobody plays (8, then 10).
# FROM STRIP 12 (1:16.7, where the thumb's pops change ends) each foot plays its hand's palm strokes too. The two
# readings between them strike every sixteenth of the strip but three: 4, 9 and 14. So for the last four strips the
# feet run in sixteenths with three holes, and two of the holes are where the thumb pops (4 and 14: Harry, "Keep the
# pops"); the third is the centre. It stops with the right hand, on the tie at tick 15 of the last strip.
# THE OTHER DRUM is a second bass drum, a minor third up (the album kit's kick at C2 where the left foot's is at A1),
# a little right of centre, beside the hand it follows. At C2 it fills the band this song has been short in since
# v11: read as chirper-one read v20 (the finished file, each band's share against the eleven records), 60-120 Hz in
# 'opposite' goes -1.0 -> -0.1 and under 60 Hz does not move; the same drum at A1 or G1 put its weight under 60 Hz
# instead (+1.2, +1.4 dB there in strips 4-11, benched). THE SHORT STROKES are the same two drums struck lighter
# and stopped sooner (each note carries its own patch: the drum's decay 210 -> 90 ms; 4 and 1 dB down), so that
# sixteen kicks a strip do not sit on the band: with full-length strokes the run read 0.6 dB heavier under 60 Hz.
# MEASURED (raw, a stroke's first 70 ms, K): the left foot's open stroke -20.6 dB, 1.2 over everything else at that
# moment; the other foot's -21.4, 3.5 over (less is playing at 8 and 18); a short stroke -28.7 and -28.9, 4.2 and
# 6.1 UNDER everything else (v19's clap between the beats: 6.1 under). The snare under the run: 0.4 dB lower (the
# kit bus's compressor). As mastered the run is 0.01 dB louder than the same strips of v20 and the band's 1-4 kHz
# in it 0.4 dB lower; strips 4-11 0.05 louder. The target is not moved: every other bar is within 0.011 dB on
# seed 0 and 0.002 on the song's own seed; on seed 11 the master sits 0.08 to 0.12 dB higher throughout (this
# song's master jumps: v18, v19 and v20 each met it).
# the other drum (its patch, its fader, where it stands, the band on its track) ; the strip of 'opposite' from which
# the other foot plays its hand's open notes ; the strip from which each foot plays its hand's palm strokes too ;
# how those are struck (velocity ; dB on the left foot's ; dB on the other's ; what makes the stroke a short one) ;
# the loudness target (None: unchanged). --without-other-foot gives v20.
FEET = {'patch': 'ct-kit kit.k.pitch=C2', 'gain': '0.5dB', 'pan': .3, 'eq': 'peak cutoff=4400 q=0.84 gain=6dB',
        'from': 4, 'run': 12, 'mute': (.6, -4, -1, 'kit.k.patch.synth.amp.d=90ms'), 'loudness': None}


# v22 (chirper-alpha; palette round: one new sound, on the facing page, 3:52.9-3:58.4): THE WET INK'S IMAGE IS PLAYED
# BACKWARDS. "Close a book on wet ink and the other page takes its mirror image": on the facing page the right hand
# reads the strip from its far end, so the NOTES are mirrored; the SOUND never was. A mirror image of a sound is that
# sound backwards. So the left hand is there after all, on tape: its strip as ink first wrote it (alone, forwards, on
# its own rig), recorded inside the song (the engine's resampling: a `songs` entry and a `sample` layer) and played
# in reverse on its own side, one sixteenth early. Backwards it has the right hand's notes in the right hand's
# order, and with that sixteenth each of them ENDS on the instant the right hand strikes the same note: the left side
# holds each ringing note until the right hand takes it, and swells into each palm stroke. Nothing leaves the song.
# NB `chirp render --solo blot` is silent (a sample of a song inside the song does not render alone): subtract mixes.
# how many of the facing page's strips carry it ; its fader against the left hand's own level ; how many sixteenths
# before the strip the tape starts ; the loudness target (None: unchanged). --without-blot gives v21.
BLOT = {'strips': 2, 'gain': '-2.5dB', 'ahead': 1, 'loudness': None}
# v23 (chirper-zero, instrument round: the bass, 161 notes; no note moves): THE BASS LEANS ON ITS OCTAVE, AND THE
# MIDDLE IT LEAVES GOES TO THE TWO HANDS. Alone, beside eleven records' bass stems (tools/bassspec.py), this bass
# was the furthest on the album: 7.1 (In the Time Of's was 6.4 before its v24). It stood +14 dB at 40 and 50 Hz,
# -10 and -8 at 80 and 100, where a record's bass has its weight, and +6 to +10 from 315 to 630 Hz: a sub and a
# box. So the album's cure (In the Time Of v24, Take Up the Slack v15): the note's octave up 6 dB at 110 Hz, the
# box cut (540 Hz -6), the grind moved to 1150 Hz and raised, the sine under the note down 8 dB (-9 -> -17: the
# root here is F1, 43.7 Hz, so the sine IS the note's fundamental and it stays; -20 was benched and not taken),
# and the patch's low-pass opened 4 -> 6 kHz. Alone 7.12 -> 4.28 ('ink'), 7.23 -> 4.67 ('raised').
# BUT THE BOX HAD BEEN STANDING IN FOR THE GUITARS: with the bass cured and nothing else the mix read WORSE (1.102
# -> 1.130; 'ink' and 'one hand' 0.3 to 0.6 further short from 250 Hz to 1 kHz). So the two hands take the middle: on
# their tracks +2.5 dB at 330 Hz, the 800 Hz cut 1.5 -> 0.5, +2 dB at 1.3 kHz (the mix was 1.2 to 3.0 short at
# 1-2 kHz in every stretch), the chest 7 -> 8 dB, v15's cut at 2.6 kHz 3.5 -> 4. AND THE HAND LIFTS (chirper-
# alpha's finding, So Far v15; Extreme and Mean v27): the palm closes the string's filter 2 octaves, not 3.4, and
# weighs 0.6 of what it did. A muted stroke's low end died through the stroke (+1.3 / +2.0 dB, the first 20 ms
# against 40-80; six records -1.1, -2.2 to +0.3): now -0.6 / -0.2; the noise between its harmonics 0.43 / 0.45 ->
# 0.37 / 0.42 (0.40). The tape of the left hand (v22) is the left hand's own rig, so it changes with it.
# THE MIX against the eleven records, six stretches, all nine bands: 1.102 -> 0.950, every stretch nearer (0.881
# before the hands and the bass were each trimmed to be as loud alone as they were).
# overrides on the bass's patch ; octaves the palm closes the hands' filter ; the palm's weight ; the hands' track
# eq ; dB on the hands' and the bass's faders (each is then as loud alone as it was) ; the loudness target (a fuller
# middle measures louder: at v22's -10.34 the master turned 'pencil', which has neither guitar nor bass, down
# 0.64 dB; at -9.99 it is where v22 had it). --without-lean gives v22.
LEAN = {'bass': 'fx.2.bands.0.gain=12dB fx.2.bands.1.gain=6dB fx.2.bands.2.cutoff=540 fx.2.bands.2.q=0.7 fx.2.bands.2.gain=-6dB '
                'fx.2.bands.3.cutoff=1150 fx.2.bands.3.q=1.2 fx.2.bands.3.gain=6dB synth.layers.1.level=-17dB fx.2.bands.3.gain=10dB fx.2.bands.5.cutoff=6000',
        'palm': -2, 'weight': 0.6,
        'eq': ['peak cutoff=180 q=1 gain=8dB', 'peak cutoff=330 q=1 gain=2.5dB', 'peak cutoff=800 q=1.2 gain=-0.5dB',
               'peak cutoff=1300 q=1 gain=2dB', 'peak cutoff=2600 q=1.4 gain=-4dB'],
        'trim': -1.1, 'loudness': -9.99}


def lean(doc):
    """v23: the bass on the album's leaner chain; the two hands (and the left hand's tape) with a lighter palm and the
    middle the bass gave up."""
    hands = [t for t in doc['tracks'] if t['name'] in ('left', 'right')] + [t for s in doc.get('songs', {}).values() for t in s['tracks']]
    for t in hands:
        if isinstance(t['patch'], str) and t['patch'].startswith('ct-twin '):
            cut = t['patch'].find(' play.humanize.time=0ms')        # the tape's copy of the left hand ends with its own two play fields
            t['patch'] = (t['patch'] + f" synth.filters.0.cutoff.mod.0.amount={LEAN['palm']}" if cut < 0 else
                          t['patch'][:cut] + f" synth.filters.0.cutoff.mod.0.amount={LEAN['palm']}" + t['patch'][cut:])
            for n in t['notes']:
                if (n.get('expr') or {}).get('pm'): n['expr']['pm'] = round(n['expr']['pm'] * LEAN['weight'], 4)
            t['fx'] = [{'type': 'eq', 'bands': LEAN['eq']}]
    bass = next(t for t in doc['tracks'] if t['name'] == 'bass')
    bass['patch'] += ' ' + LEAN['bass']
    for t in hands + [bass]:                # each is as loud alone as it was (the hands +1.1 LU, the bass +1.0 to +1.2 before the trim)
        if isinstance(t['gain'], dict): t['gain'] = dict(t['gain'], value=f"{float(t['gain']['value'][:-2]) + LEAN['trim']:g}dB")
        else: t['gain'] = f"{float(t['gain'][:-2]) + LEAN['trim']:g}dB"
    if LEAN['loudness']: doc['loudness'] = LEAN['loudness']


# v24 (chirper-alpha; section round, w4, 'carbon', 1:27.7-1:49.6): THE COUNT IS COPIED TOO, AT ITS OWN LENGTH.
# The song's first line says the strip is read "under an unbroken count of four", and in 'carbon' the count was
# one soft snare a bar: no hat, and the bass drum follows the hand, not the bar. The hand's strips go page, copy,
# page, copy; the drummer copied nothing. Now his bars do the same, and his page is a BAR, sixteen sixteenths,
# where the hand's is a strip of nineteen. A page bar (bars 1, 3, 5, 7, 9) is the count as 'ink' has it: the
# sticks on the hat, every quarter. On a copy bar (2, 4, 6, 8 and the half bar that ends the section) the sticks
# are up and the FOOT's hat keeps the four quarters: fainter, no sizzle, the count on the sheet beneath. It is the
# sound the song ends on (v9, the facing page: "the sticks are down; the foot goes on counting"), heard here two
# minutes early, and for the same reason. 38 strokes, 20 of the sticks and 18 of the foot; nothing else changes.
# Because sixteen is not nineteen the two sheets slip. Bar 1 lies wholly under a page strip of the hand and bar 2
# 13 of 16 sixteenths under a copy strip; then 10, 7, 4 and 1; bar 7 (1:41.5) not at all: the drummer's page lies
# under the hand's copy and the bar after it the other way about. Then they come back: the last half bar, a copy,
# lies wholly under the hand's last copy strip, and 'thumbprint' begins.
# (Benched, raw, stroke by stroke against everything else in the stroke's best third-octave, first 80 ms. The
# sticks: +25.2 off the snare's beat (ink's hat under two guitars: +7.9). The foot at the facing page's own
# setting (0.5 / 0.4, -3 dB) read -4.1 / -1.9, the edge of hearing: the facing page is far barer (+28.0 there).
# At 0.6 / 0.5 and +3 dB it reads +4.3 on first beats and +6.1 on the others (+7.0 off the snare's beat). The
# nine strokes on the snare's own beat are under it (-7.6 to -20.3), as on any kit.
# FIRST TAKES NOT KEPT. A side stick on the copy bars' one and three, in place of their snare: the album kit's
# side stick is a 5 ms click at 500 Hz and 1.3 kHz, and under one guitar and the voice it read -8.3 / -5.4 on the
# kit's bus and +0.7 / +4.5 only at +12 dB. And the copy bar as the sticks' first beat alone, "only the stroke
# that was pressed goes through" (rendered whole: 98.702 / 98.701 / 98.725): it reads (+10.0), but it leaves the
# count broken every other bar, which is the one thing this song says the count is not.)
# the sticks' velocity on a page bar's first beat and its others ; a copy bar: the kit piece, its velocity by the
# beat of the bar ('0' is the first; a beat left out is not played) and each stroke's own gain ; the loudness
# target (None: unchanged). --without-counted-copy gives v23. (--counted '{"copy": [...]}': fields for a bench.)
COUNTED = {'page': (.65, .48), 'copy': ('hp', {'0': .6, '1': .5, '2': .5, '3': .5}, '3dB'), 'loudness': None}

# v25 (chirper-one; section round, w7, 2:55.4-3:06.3 inside 'turn over'): THE DRUMMER TURNS THE PAGE OVER TOO.
# For those four strips the two hands read the strip upside down (v16, mine: every chord as far below the low F as
# it stood above). The drummer went on as if nothing had happened: his foot on the left hand's four open notes, his
# sticks counting quarters on the china, the snare on two and four. Now HIS KIT IS TURNED TOP TO BOTTOM ABOUT THE
# SNARE, as the page is about the low F: what was at the top (the count, on the china) is at the bottom, and what
# was at the bottom (the strip's four open notes, on the bass drum) is at the top. So for eleven seconds THE FOOT
# COUNTS, four to the bar, and THE STICKS READ THE STRIP on the china, a stroke on each of the left hand's open
# chords. The snare is the fold and stays. In that no stroke is added, dropped or moved: 19 quarters and 16 open
# notes change places. Then the page is turned back (3:06.3) and so is he.
# It is the only place in the song where the bass drum keeps the bar: everywhere else it follows a hand.
# AND THE TURN IS PLAYED, read from both ends as everything here is. Into the turned page the sticks come DOWN the
# kit from the fold: the snare's backbeat that was already there (2:54.8), then three toms, high, middle, floor, on
# the last three sixteenths before the crash. Out of it they come back UP: floor, middle, high on the last three
# sixteenths, and the fourth stroke is the snare that was already on the first tick of the page turned back
# (3:06.3). The same four drums, read from the other end. Six strokes, the round's only new ones.
# 'foot': the turned bass drum's velocity on a bar's first beat and on the others ; 'sticks': the kit piece that
# reads the strip, its velocity where the foot's stroke was full and where it was light, and each stroke's own gain
# (None: the track's) ; 'turns': the three toms from the fold down, their velocities in that order, each stroke's
# own gain (None: no toms at the turns) ; 'loudness' (None: unchanged). --without-turned-kit gives v24.
# (--kit '{...}': a bench.)
KIT_TURNED = {'foot': (.98, .9), 'sticks': ('x', .72, .6, None), 'turns': (('t1', 't3', 'ft'), (.82, .9, .98), None), 'loudness': None}


# v26 (chirper-alpha; section round, w1, 0:00-0:27; the change is 'pencil', 0:00.0-0:10.96): THE PAGE IS RULED, AND
# THE LINE IS DRAWN FROM BOTH ENDS.
# (1) THE COUNT. The song is two readings of one strip "under an unbroken count of four", and the count began with
# the ink, at 0:11. The song ENDS with the foot alone closing the hat in quarters under the facing page's last four
# strips (v9: 19 strokes, the sticks down). It now BEGINS with those 19 strokes, at the same touch, under the
# pencil's four: the first sound of the song and its last are the voice's F with the foot, on the first beat of
# bar 1 and of bar 109, and the facing page is the image of a count that was there. The bar line the foot draws is
# the one ink's hat goes on with (the ink begins on the fourth beat of bar 5, and now that is heard). With it the
# sketch is heard as what it is: a line of nineteen sixteenths over bars of sixteen, starting three sixteenths
# later in the bar each time it comes round. (The count is still not unbroken: 'thumbprint', 1:49.6-2:17.0, and
# 'signed', 3:44.7-3:52.9, have nothing on the quarter, and this round leaves them so.)
# (2) THE LINE. The voice sang the whole line three times alike. A pencil does not write a line three times, it
# finds it, and here everything is read from both ends: so first the line's two ends (F ... C), then the next
# note from the front (F, A flat ... C), then the last from the back, and the line is whole. "One note, two, then
# all four" is how the mouth hands its line to the drummer in 'carbon'; here it is how the line is found. Every
# note is where and as long as the finished line has it, so what is heard in the gaps is the foot: three counts
# between the first two notes the song has. The ribbon's whole line in the fourth strip (v7) is as it was.
# (3) THE OTHER HAND'S FIRST MARKS ARE THE TWO MEETINGS. The clean string answered with its whole reading twice.
# The first time it now plays only ticks 3 and 15, where the two readings strike together: C under the voice's
# A flat, A flat under its C. What the song is about is said before either hand has a guitar.
# 19 strokes of the foot in; 3 of the voice's notes and 2 of the string's out; no other note changes.
# The pencil is quieter (raw, strip by strip, K: -35.2, -35.6, -34.6, -34.6 becomes -38.2, -36.8, -34.6, -34.7), and
# at the old target the master turned every other section down 0.02 dB (the loudness meter's gate, I take it: not
# checked). The target goes -9.99 -> -9.966 and every other section is where it was (the slope here is 0.9).
# FIRST TAKE NOT KEPT: each unfinished strip's notes HELD to the next one drawn and 4 and 3 dB lighter (a line
# between two points): it hides where the missing notes will come and covers the count the round put there.
# It is still reachable: --ruled '{"hold": true, "mouth": [[[0, 15], "-4dB"], [[0, 3, 15], "-3dB"], null], "loudness": -9.951}'.
# 'foot': the kit piece that rules the page, its velocity on a bar's first beat and on the others, each stroke's own
# gain (None for the whole field: no count in 'pencil') ; 'mouth': for the pencil's first three strips, the ticks
# of the strip the voice sings and how lightly, as each note's own gain (None for a strip: all four, as written) ;
# 'wire': the same for the clean string's two strips, the third and fourth ; 'hold': a note of an unfinished strip
# is held to the next one drawn (False: every note as short as the finished line has it) ; 'loudness' (None:
# unchanged). --without-ruled-page gives v25. (--ruled '{...}': a bench.)
RULED = {'foot': ('hp', .5, .4, FOOT_COUNT), 'mouth': (((0, 15), None), ((0, 3, 15), None), None), 'wire': (((3, 15), None), None), 'hold': False, 'loudness': -9.966}


def ruled(doc, sections):
    """v26: in 'pencil' the foot keeps the count (as it does under the facing page), and the line is sketched from
    its two ends inward: two notes, three, then all four; the other hand first marks the two places they meet."""
    _, start, count = next(s for s in sections if s[0] == 'pencil')
    a, b = start / GRID, (start + count * STRIP) / GRID
    hat, mouth, wire = (next(t for t in doc['tracks'] if t['name'] == n) for n in ('hat', 'mouth', 'wire'))
    assert not [n for n in hat['notes'] if a <= n['at'] < b]
    if RULED['foot']:
        piece, first, rest, trim = RULED['foot']
        hat['notes'] = sorted(hat['notes'] + [{'at': float(beat), 'len': round(1.15 / GRID, 5), 'pitch': piece, 'vel': first if beat % 4 == 0 else rest,
                                               **({'gain': trim} if trim else {})} for beat in range(int(-(-a // 1)), int(-(-b // 1)))], key=lambda e: e['at'])
    for track, plan, first_strip in ((mouth, RULED['mouth'], 0), (wire, RULED['wire'], count - len(RULED['wire']))):
        for i, strip_ in enumerate(plan):
            if strip_ is None: continue
            keep, light = strip_
            s0 = start + (first_strip + i) * STRIP
            there = [n for n in track['notes'] if s0 <= round(n['at'] * GRID) < s0 + STRIP]
            ticks = [round(n['at'] * GRID) - s0 for n in there]
            assert len(there) == 4 and set(keep) <= set(ticks), (track['name'], i, ticks)
            track['notes'] = [n for n in track['notes'] if not (s0 <= round(n['at'] * GRID) < s0 + STRIP) or round(n['at'] * GRID) - s0 in keep]
            drawn = [n for n in there if round(n['at'] * GRID) - s0 in keep]
            for n, nxt in zip(drawn, drawn[1:] + [None]):
                if RULED['hold'] and nxt:
                    n['len'] = round((round(nxt['at'] * GRID) - round(n['at'] * GRID) - .23) / GRID, 5)
                if light:
                    n['gain'] = light
    if RULED['loudness']: doc['loudness'] = RULED['loudness']


def turned_kit(doc, sections):
    """v25: over the strips of 'turn over' that are read upside down, the count and the strip change places on the kit."""
    _, start, _ = next(s for s in sections if s[0] == 'turn over')
    a, b = (start + TURNED[0] * STRIP) / GRID, (start + TURNED[1] * STRIP) / GRID
    foot, brass = (next(t for t in doc['tracks'] if t['name'] == n) for n in ('foot', 'brass'))
    strip_ = [n for n in foot['notes'] if a <= n['at'] < b]
    count = [n for n in brass['notes'] if a <= n['at'] < b and n['pitch'] == 'x']
    assert len(strip_) == 4 * (TURNED[1] - TURNED[0]) and all(n['at'] % 1 == 0 for n in count) and len(count) == int(-(-b // 1)) - int(-(-a // 1)), (len(strip_), len(count))
    full = max(n['vel'] for n in strip_)
    piece, hard, soft, trim = KIT_TURNED['sticks']
    foot['notes'] = sorted([n for n in foot['notes'] if not a <= n['at'] < b] +
                           [{**strip_[0], 'at': n['at'], 'vel': KIT_TURNED['foot'][0 if n['at'] % 4 == 0 else 1]} for n in count], key=lambda e: e['at'])
    brass['notes'] = sorted([n for n in brass['notes'] if not (a <= n['at'] < b and n['pitch'] == 'x')] +
                            [{**count[0], 'at': n['at'], 'pitch': piece, 'vel': hard if n['vel'] == full else soft, **({'gain': trim} if trim else {})} for n in strip_], key=lambda e: e['at'])
    if KIT_TURNED['turns']:
        toms, vels, trim = KIT_TURNED['turns']
        skins, snare = (next(t for t in doc['tracks'] if t['name'] == n) for n in ('skins', 'snare'))
        s16 = lambda n: round(n['at'] * GRID)
        down, up = round(a * GRID), round(b * GRID)                       # the tick the page turns on, and turns back on
        assert any(s16(n) == down - 4 for n in snare['notes']) and any(s16(n) == up for n in snare['notes'])   # the fold is already there, at both ends
        assert not [n for n in skins['notes'] if down - 8 <= s16(n) < up + 8]
        new = [(down - 3 + i, t, v) for i, (t, v) in enumerate(zip(toms, vels))] + [(up - 3 + i, t, v) for i, (t, v) in enumerate(zip(toms[::-1], vels[::-1]))]
        skins['notes'] = sorted(skins['notes'] + [{**skins['notes'][0], 'at': k / GRID, 'pitch': t, 'vel': v, **({'gain': trim} if trim else {})} for k, t, v in new], key=lambda e: e['at'])
    if KIT_TURNED['loudness']: doc['loudness'] = KIT_TURNED['loudness']


def counted(doc, sections):
    """v24: in 'carbon' the drummer's bars go page, copy as the guitarist's strips do. A page bar is his count as
    'ink' has it, the hat on every quarter; a copy bar is what went through: its first and third beats, fainter."""
    _, start, count = next(s for s in sections if s[0] == 'carbon')
    a, b = start / GRID, (start + count * STRIP) / GRID
    hat = next(t for t in doc['tracks'] if t['name'] == 'hat')
    assert not [n for n in hat['notes'] if a <= n['at'] < b]
    for beat in range(int(-(-a // 1)), int(-(-b // 1))):
        if (beat // 4 - int(a) // 4) % 2 == 0:
            piece, v, trim = 'h', COUNTED['page'][0 if beat % 4 == 0 else 1], None
        else:
            piece, v, trim = COUNTED['copy'][0], COUNTED['copy'][1].get(str(beat % 4)), COUNTED['copy'][2]
        if v:
            hat['notes'].append({'at': float(beat), 'len': round(1.15 / GRID, 5), 'pitch': piece, 'vel': v, **({'gain': trim} if trim else {})})
    hat['notes'].sort(key=lambda e: e['at'])
    if COUNTED['loudness']: doc['loudness'] = COUNTED['loudness']


def build(drum_hand=True, crease=True, mirror_bass=True, picking_hand=True, signature=True, ties=True, facing=True, palindrome=True, album_kit=True, dominant=True, thumbs=True, copy=True, heavy=True, turned=True, rig=HANDS_RIG, reading=True, chest=True, palmas=True, crack=True, feet=True, blot=True):
    crease = crease and drum_hand  # --without-drum-hand still reproduces v2
    mirror_bass = mirror_bass and crease  # --without-crease still reproduces v3
    picking_hand = picking_hand and mirror_bass  # --without-mirror-bass still gives v4
    signature = signature and picking_hand       # --without-picking-hand still gives v5
    ties = ties and signature                    # --without-signature still gives v6
    facing = facing and ties                     # --without-ties still gives v7
    palindrome = palindrome and facing           # --without-facing-page still gives v8
    album_kit = album_kit and palindrome         # --without-palindrome still gives v9
    dominant = dominant and album_kit            # --without-album-kit still gives v10
    thumbs = thumbs and dominant                 # --without-dominant still gives v11
    copy = copy and thumbs                       # --without-thumbs still gives v12
    heavy = heavy and copy                       # --without-carbon-copy still gives v13
    rig = rig if heavy else None                 # --with-steel still gives v14
    turned = turned and heavy and rig is not None  # --stock-rig is v15's notes on the old rig
    reading = reading and turned                 # --without-turned-page still gives v15
    palmas = PALMAS if palmas and chest and reading and rig is not None else None   # --without-chest still gives v17
    crack = CRACK if crack and palmas and all([drum_hand, crease, mirror_bass, picking_hand, signature, ties, facing, palindrome, album_kit, dominant, thumbs, copy, heavy, turned]) else None   # every older flag gives exactly what it gave
    feet = FEET if feet and crack else None      # --without-crack still gives v19
    blot = BLOT if blot and feet else None       # --without-other-foot still gives v20
    ev = defaultdict(list); sections = []; tie_gains = {}; start = 0
    def put(tr, t, n, dur, v, mute=False, **expr):
        e = {'at':round(t/GRID, 5), 'len':round(dur/GRID, 5), 'pitch':pitch(n) if isinstance(n,int) else n, 'vel':v}
        if mute: expr['pm'] = 1
        if expr: e['expr'] = expr
        ev[tr].append(e)
    def kit(tr,t,p,v): put(tr,t,p,3.8 if p in ('c','x','rde') else 1.15,v)
    def chord(root): return pitch(root)+','+pitch(root+7)
    front,back = strip(),strip(True)
    opens = [{t:p for t,p,k in r if k=='o'} for r in (front,back)]
    # The right picking hand tries the reflection before the fretted tune does.
    # The nearest three palm strokes move first; then all five move, twice.
    # Recompute the gaps from each new row: an early mute chokes the open note.
    by_centre = sorted((t for t,_,k in front if k=='m'), key=lambda t: abs(2*t-(STRIP-1)))
    def turn_mutes(how_many):
        move = set(by_centre[:how_many])
        r = sorted((STRIP-1-t if t in move else t, p, k) for t,p,k in front)
        assert len({t for t,_,_ in r}) == len(r)
        return r
    meetings = sorted(opens[0].keys() & opens[1].keys())
    assert meetings == [3,15]
    # Immediately inside the shared attacks is a reflected pair of gaps.
    # Neither guitar picks at 4 or 14. Leave the silent centre, tick 9, alone.
    gaps = [meetings[0]+1, meetings[1]-1]
    assert sum(gaps) == STRIP-1 and set(gaps).isdisjoint(t for t,_,_ in front+back)
    taps = (2,7,13,17)
    assert set(taps) <= {t for t,_,k in front if k=='m'}
    for sec,count in FORM:
        sections.append((sec,start,count))
        for i in range(count):
            a = start + i*STRIP
            slapping = mirror_bass and sec == 'opposite' and i >= count//2
            # F all through the introduction and first traversal. The quiet centre
            # moves to its minor third; the high answer alone bends on the way home.
            root = 29 + (3 if sec in ('carbon','thumbprint') else 1 if sec=='raised' and i<count//2 else 0)
            # v12: THE FOURTH NOTE IS A GROUND. The strip has four open notes:
            # F, A-flat, G-flat, C. The song has stood on the first three, in
            # that order (F; A-flat from 'carbon'; G-flat in 'raised'), and
            # never on the fourth. The last four strips of 'turn over' move up
            # to C. The forward hand's last open chord in a strip IS C: on the
            # strip before, it is left ringing (its closing palm stroke is not
            # played) and becomes the ground. And 'one hand' begins on C: read
            # from the far end, the strip's first open chord is that same C,
            # and it comes down C, G-flat, A-flat, F. So the form reads the
            # strip forwards, a ground at a time, before the signature reads
            # it backwards in four chords.
            lifted = dominant and sec=='turn over' and i >= count-4
            if lifted: root += dict((t,p) for t,p,k in ROW if k=='o')[max(t for t,p,k in ROW if k=='o')]
            pivot = dominant and sec=='turn over' and i == count-5
            # v4: fold the last three G-flat strips about their shared, silent
            # centre. The two open meetings at 3 and 15 are the first fold's
            # edges. The second keeps half that span; the last keeps just the
            # centre. The independent quarter-note count stays outside the fold.
            centre = STRIP // 2
            step = i - (count//2 - 3)
            folding = crease and sec=='raised' and 0 <= step < 3
            radius = (centre - min(opens[0].keys() & opens[1].keys())) * (2-step)//2 if folding else centre
            def inside(t): return abs(t-centre) <= radius
            if folding:
                assert centre not in {t for t,_,_ in front+back}
                put('wire',a+centre,29+36,(2,5,STRIP-centre-.25)[step],.88)
            # In 'carbon' the mouth hands its line to the drummer from the tail
            # backwards: one note, two, then all four. In 'one hand' the drummer
            # answers two full strips, at the guitarists' timing this time.
            tom_reply = drum_hand and sec=='one hand' and i in (count-3,count-1)
            # v17: the last strip(s) of 'ink' are the other hand's first reading, alone
            alone = reading and sec=='ink' and i >= count-READING[0]
            if sec=='signed':
                # No counting-out: the last two chord changes are read right to left.
                if i==0: cadence=[(0,7,5),(8,1,7)]
                elif i==1: cadence=[(0,3,11)]
                else: cadence=[(0,0,STRIP-1)]
                for t,p,dur in cadence:
                    for tr in ('left','right'): put(tr,a+t,chord(root+p),dur,.95)
                    put('bass',a+t,root+p,dur,.92); kit('foot',a+t,'k',.95)
                    if i==2: kit('brass',a+t,'c',.84); put('mouth',a+t,root+24,dur,.78)
                continue
            if sec=='pencil' or sec=='thumbprint':
                # A wordless VOSIM voice has time to open its vowel: the two hands
                # are a sung call and an unhurried clean answer, never two walls.
                if sec=='pencil':
                    for t,p in opens[0].items(): put('mouth',a+t,root+24+p,2.4,.78)
                    if i>=2:
                        for t,p in opens[1].items(): put('wire',a+t,root+12+p,2.4,.82)
                else:
                    for t,p in opens[i%2].items():
                        put('mouth',a+t,root+24+p+(12 if i in (6,7) else 0),2.1,.84)
                    for t,p in opens[1-i%2].items():
                        # v13: the answer is a thumb piano's; the tines alternate sides as they rise
                        side = ('left','right')[sorted(opens[0].values()).index(p) % 2]
                        put('tines-'+side if thumbs else 'wire',a+t,root+12+p+(TINES[3] if thumbs else 0),2.6,.86)
                    if i>=count//2:
                        for t in (3,15): kit('skins',a+t,'ft' if t==3 else 't1',.71)
                continue
            rightback = sec in ('opposite','carbon','raised') or (sec=='turn over' and i%2==0)
            leftback = sec=='turn over' and i%2==1 or sec=='one hand'
            for tr,rev in [('left',leftback),('right',rightback or sec=='one hand')]:
                # Carbon is one guitarist with a delayed memory, not a stereo solo.
                if sec=='carbon' and tr=='right': continue
                if sec=='ink' and i<4 and tr=='right': continue
                if sec=='turn over' and rev and not heavy:
                    # (v2 to v14) The hand reading back picks up a volume steel. First hold just
                    # the two meeting notes (C, Ab); then fill in the reflected tune.
                    # The other hand still chugs. Swap chairs on every new strip.
                    stops = [t for t in sorted(opens[1]) if i>=4 or t in (3,15)]
                    end = 10 if i==count-1 else STRIP
                    stops = [t for t in stops if t<end]
                    for j,t in enumerate(stops):
                        until = stops[j+1] if j+1<len(stops) else end
                        put('steel-'+tr,a+t,root+24+opens[1][t],until-t-.12,.87)
                        if lifted: ev['steel-'+tr][-1]['gain'] = STEEL_ON_C
                    continue
                r = back if rev or (alone and tr=='right') else front
                if picking_hand and sec=='ink' and tr=='right':
                    lap = i - count//2
                    if 0 <= lap < 3:
                        r = turn_mutes((len(by_centre)+1)//2 if lap==0 else len(by_centre))
                last_open = max(t for t,_,k in r if k=='o')
                for j,(t,p,k) in enumerate(r):
                    if not inside(t): continue
                    if alone and tr=='left' and (t or not READING[2]): continue      # v17: the downbeat, then the hand lifts off
                    if pivot and t > last_open: continue     # v12: nothing damps the C that is about to be the ground
                    if tom_reply and not (i==count-1 and t==STRIP-1): continue
                    if sec=='one hand' and k=='m' and (i>=4 or t%2): continue
                    if sec=='carbon' and k=='m' and i%2: continue
                    if sec=='turn over' and i==count-1 and t>=10: continue
                    gap = (r[j+1][0] if j+1<len(r) else STRIP)-t
                    if pivot and t == last_open: gap = STRIP-t
                    dur = .64 if k=='m' else min(gap-.23, 3.45)
                    n = root+p
                    if turned and sec=='turn over' and TURNED[0] <= i < TURNED[1]:
                        n = root+(12-p)%12       # v16: the page upside down
                    if picking_hand and sec=='ink' and tr=='right' and k=='m' and t not in by_centre and not alone:
                        # The travelling strokes are up-picks. Keep them short,
                        # but lift the palm a little so they cut through the note
                        # still ringing on the left. Ordinary down-picks stay put.
                        put(tr,a+t,n,dur,.84,pm=.55,up=1)
                    else:
                        # v14: an odd strip of 'carbon' is the copy, and it is taken on the second amp
                        amp = 'copy' if copy and sec=='carbon' and i%2 else tr
                        assert amp==tr or (tr=='left' and k=='o')
                        put(amp,a+t,chord(n) if k=='o' and sec in ('raised','turn over','one hand') else n,dur,.94 if k=='o' else .79,k=='m')
            if sec=='carbon':
                n_take = min(4, 2**(i//2)) if drum_hand and i%2 else 0
                for j,(t,p) in enumerate(sorted(opens[1].items())):
                    if j < len(opens[1])-n_take:
                        put('mouth',a+t,root+24+p,2.15,.84)
                    else:
                        # Lead the missing word on a vacated palm stroke, never
                        # double it. The four head pitches are the same tune.
                        put('drum-hand',a+taps[j],'head'+str(root+12+p),2.3,.86)
                for t in (3,15): put('bass',a+t,root,3,.87); kit('foot',a+t,'k',.87)
            else:
                # In the opposing voices the bass recognises only the two common
                # open attacks; the contrasting pitches form Ab/C then C/Ab.
                apart = sec in ('opposite','turn over','raised')
                rb = opens[1 if leftback else 0]
                for t,p in rb.items():
                    if not inside(t): continue
                    if alone and (t or not READING[2]): continue
                    if sec=='turn over' and i==count-1 and t>=10: continue
                    if tom_reply:
                        put('drum-hand',a+t,'head'+str(root+12+p),2.3,.92)
                        # One low pedal on the first beat of the answer; leave
                        # the rest to the drum pitches, not the bass doubling them.
                        if t==min(rb):
                            put('bass',a+t,root,3,.92); kit('foot',a+t,'k',.95)
                    else:
                        if not apart or t in (3,15):
                            put('thumb' if slapping else 'bass',a+t,root+(0 if apart else p),3 if apart else 1.7,.92)
                        kit('foot',a+t,'k',.98 if t in (0,3,15,18) else .83)
                if slapping:
                    # Pop AFTER the first thumb and BEFORE its reflection. First
                    # quote the forward guitarist's pitches, then the other's.
                    lap = i - count//2
                    source = opens[int(lap >= (count-count//2)//2)]
                    for j,(cross,gap) in enumerate(zip(meetings,gaps)):
                        if j == 1 and lap < 2: continue
                        # A-flat is the next section's ground. The last two
                        # pickups ring across the low F to point the way to it.
                        dur = .83
                        if j == 1 and i >= count-2:
                            dur = STRIP-gap-.4 if i == count-1 else 2.5
                        put('thumb',a+gap,root+12+source[cross],dur,.78 if j==0 else .72,pop=1)
                if sec=='raised':
                    for t in (3,15):
                        if inside(t): put('mouth',a+t,root+24+opens[1][t],2.65,.85)
                    if folding and step>0:
                        # Even when the guitars no longer meet here, the foot
                        # remembers ONE of their two meetings. Hold that last
                        # low G-flat up to the clean F, not across its attack.
                        anchor = min(opens[0].keys() & opens[1].keys())
                        put('bass',a+anchor,root,centre-anchor-.4,.92)
                        kit('foot',a+anchor,'k',.98)
                    if crease and i==count//2:
                        # The high F has told us the key already. Meet the
                        # returning left guitar three octaves down, then go
                        # back to the bass's two meetings a strip; no crash.
                        put('bass',a,root,2.7,.95)
                if sec=='opposite' and i in (3,7,11,15): kit('skins',a+17,'ft',.84)
            # The drummer counts through the strip seams, not from strip zero.
            for t in range(a, a+STRIP):
                if sec=='turn over' and i==count-1 and t>=a+10: break
                if t%GRID: continue
                beat=t//GRID
                if sec=='carbon':
                    if beat%4==2: kit('snare',t,'s',.76)
                else:
                    if alone:
                        if READING[1]: kit('hat',t,'h',.65 if beat%4==0 else .48)
                        continue
                    if beat%4==(2 if sec in ('ink','one hand') else 1) or (sec not in ('ink','one hand') and beat%4==3): kit('snare',t,'s',.94)
                    if sec in ('raised','turn over'): kit('brass',t,'x' if sec=='turn over' else 'rde',.72 if beat%4==0 else .60)
                    elif not tom_reply or t-a not in opens[1]:
                        kit('hat',t,'h',.65 if beat%4==0 else .48)
                        # v19: the count read from the strip's far end, clapped
                        if palmas and sec=='opposite': put('palmas',a+STRIP-1-(t-a),'pa',1,palmas[3][0 if beat%4==0 else 1])
            if sec in ('ink','opposite','raised','one hand') and i==0: kit('brass',a,'c',.88)
            if turned and sec=='turn over' and i in TURNED[:2] and TURNED[2]: kit('brass',a,'c',TURNED[2])
        start+=count*STRIP
    if ties:
        # At each key change the two transpositions of this four-note hook
        # share just one pitch class. Keep it sounding: third -> root at
        # carbon, flat second -> minor third at raised. No new clock or patch.
        marks = {name:t for name,t,_ in sections}
        def bridge(section, old_root, new_root):
            outgoing = {(old_root+v)%12:t for t,v in opens[1].items()}
            incoming = {(new_root+v)%12:t for t,v in opens[1].items()}
            pc, = outgoing.keys() & incoming.keys()
            seam = marks[section]
            return seam-STRIP+outgoing[pc], seam+incoming[pc], pc
        tick = lambda n: round(n['at']*GRID)
        a,b,pc = bridge('carbon',29,32)
        pop = next(n for n in ev['thumb'] if tick(n)==a-1)
        vowel = next(n for n in ev['mouth'] if tick(n)==b)
        assert pop['pitch']==pitch(36+pc) and vowel['pitch']==pitch(48+pc)
        ev['right'] = [n for n in ev['right'] if not a<=tick(n)<b]
        put('right',a,pop['pitch']+','+vowel['pitch'],b-a-.3,.90)
        # The saturated rig doesn't decay like the popped string. Let it
        # withdraw across the quieter strip rather than stay as loud as the riff.
        tie_gains['right'] = [(marks['carbon'],0),(b-.3,-8),(b+GRID,-8),(b+2*GRID,0)]

        a,b,pc = bridge('raised',32,30)
        vowel = next(n for n in ev['mouth'] if tick(n)==a)
        assert vowel['pitch']==pitch(48+pc)
        ev['mouth'] = [n for n in ev['mouth'] if not a<tick(n)<=b]
        vowel['len'] = round((b-a-.3)/GRID,5)
        seam = marks['raised']
        # The same mouth is exposed before this seam and inside two amps
        # after it. Open its fader only while it is carrying A through the band.
        tie_gains['mouth'] = [(seam,0),(seam+GRID,3),(b-.3,3),(b+1,0)]
        next_open = seam+min(t for t in opens[1] if t>b-seam)
        # The upper sound still belongs to the vowel: single low strings on
        # the right until that player catches its A3, then let that octave
        # ring to the closing G-flat without the intervening palm stroke.
        for n in ev['right']:
            t = tick(n)
            if seam<=t<b and t-seam in opens[1]: n['pitch']=n['pitch'].split(',')[0]
            if t==b:
                n['pitch']=n['pitch'].split(',')[0]+','+vowel['pitch']
                n['len']=round((next_open-b-.3)/GRID,5)
        ev['right'] = [n for n in ev['right'] if not b<tick(n)<next_open]
    if signature:
        # The mouth teaches its last opening strip to a ribbon instrument. The
        # same hand signs forwards against the guitars' backward cadence.
        _, p0, strips = next(s for s in sections if s[0]=='pencil')
        learn = p0 + (strips-1)*STRIP
        def lesson(n): return learn <= round(n['at']*GRID) < learn+STRIP
        taught = [n for n in ev['mouth'] if lesson(n)]
        tune = [p for _,p in sorted(opens[0].items())]
        assert len(taught) == len(tune)
        ev['ribbon'] = [{**n, 'pitch':pitch(29+36+p)} for n,p in zip(taught,tune)]
        ev['mouth'] = [n for n in ev['mouth'] if not lesson(n)]
        _, sign, _ = next(s for s in sections if s[0]=='signed')
        stabs = [n for n in ev['right'] if n['at']*GRID >= sign]
        assert len(stabs) == len(tune)
        for j,(n,p) in enumerate(zip(stabs,tune)):
            tick = round(n['at']*GRID)
            # Keep the right guitarist's low string for its original length;
            # the fifth, not the weight, goes to the answering instrument.
            n['pitch'] = n['pitch'].split(',')[0]
            dur = round(n['len']*GRID)
            put('ribbon',tick,29+36+p,dur,.84 if j==len(tune)-1 else .85)
            if j == len(tune)-1:
                # Slide C5 down to F4 at the fold without a second note-on.
                curve = []
                for t in range(dur+1):
                    u = max(0.,min(1.,(t-(STRIP//2-GRID))/GRID))
                    curve.append(round((tune[0]-p)*u*u*(3-2*u),4))
                ev['ribbon'][-1]['expr_path'] = {'ribbon':curve}
    if palindrome:
        # THE LINE BOTH HANDS MAKE. Read from opposite ends, the two guitars'
        # open notes add up to something neither plays: F, C over A-flat,
        # G-flat, G-flat, C over A-flat, F. Its top is the same from either
        # end. The ribbon, which learned the tune forwards and will sign it at
        # the close, draws that top once without lifting: it is on each note
        # when a guitar strikes it and holds G-flat across the silent centre,
        # from the right hand's G-flat to the left's. Four strips, the second
        # half of the plain opposition; it stops where the thumb starts.
        _, opp, strips = next(s for s in sections if s[0]=='opposite')
        first, laps = strips//4, strips//4
        top = {t:max(opens[0].get(t,-1), opens[1].get(t,-1)) for t in opens[0].keys()|opens[1].keys()}
        assert [top[t] for t in sorted(top)] == [0,7,1,1,7,0] and all(top[t]==top[STRIP-1-t] for t in top)
        # It stays on C for two ticks on the inner side of each meeting, on
        # G-flat between the two hands' G-flats, and on F from a tick before
        # the strip's last note to a tick after the next strip's first.
        # Between those, a straight slide: so the drawn line is its own mirror.
        centre, hold = STRIP//2, []
        for t,v in sorted(top.items()):
            if t in meetings: hold += [(t,v), (t+(2 if t<centre else -2), v)]
            elif t in (0, STRIP-1): hold.append((1 if t==0 else STRIP-2, v))
            else: hold.append((t,v))
        hold = [(-2, top[STRIP-1])] + sorted(hold) + [(STRIP+1, top[0])]
        def at(t):
            for (a,va),(b,vb) in zip(hold, hold[1:]):
                if a <= t <= b: return va + (vb-va)*(t-a)/(b-a)
        strip_curve = [round(at(t),4) for t in range(STRIP)]
        assert all(strip_curve[t]==strip_curve[STRIP-1-t] for t in range(STRIP))
        assert all(strip_curve[t]==v for t,v in top.items())
        begin = opp + first*STRIP
        put('ribbon', begin, 29+36, laps*STRIP, .85)      # it lets go on the thumb's first strip
        # The engine reaches point k of a path at (k+1)/N of the note (benched:
        # with a point for each tick AND one for the end, the first strip ran a
        # tick late and the last a quarter). So N is the note's ticks, and
        # point k is where the line should be at tick k+1.
        ev['ribbon'][-1]['expr_path'] = {'ribbon': (strip_curve*laps + [strip_curve[0]])[1:]}
        # An unbroken tone over single-string riffs carries further than the
        # same fader does over the closing chords: at the track's level it stood
        # 9.8 dB under the band, where the signature stands 14.1 under.
        ev['ribbon'][-1]['gain'] = PALINDROME_TRIM_KIT if album_kit else PALINDROME_TRIM
    if facing:
        # THE FACING PAGE. Close a book on wet ink and the other page takes its
        # mirror image. The song's first six strips (the pencil's four, then
        # the left guitar's first two in ink) are read from the far end by the
        # other hand. Six, because then the backward reading's last note, F,
        # is the only strip ending that falls on the drummer's ONE: bar 109.
        mirrored = 6
        page = start
        last = page + mirrored*STRIP - 1
        assert last % (4*GRID) == 0 and [n for n,_,c in sections[:2]] == ['pencil','ink'] and sections[0][2] == 4
        sections.append(('facing page', page, mirrored))
        for j in range(mirrored):
            a = page + j*STRIP
            source = mirrored-1-j           # the opening strip this one reflects
            for t in range(a, a+STRIP):
                if t%GRID: continue
                beat = t//GRID
                if source >= 4:             # ink's count: a hat in quarters, the snare on three
                    kit('hat',t,'h',.65 if beat%4==0 else .48)
                    if beat%4==2: kit('snare',t,'s',.94)
                else:                       # the sticks are down; the foot goes on counting
                    kit('hat',t,'hp',.5 if beat%4==0 else .4)
                    ev['hat'][-1]['gain'] = FOOT_COUNT
            if source >= 4:
                # Ink began with the left hand alone, forwards, and a crash on
                # its first note. The right hand alone, backwards, ends on it.
                for i,(t,p,k) in enumerate(back):
                    gap = (back[i+1][0] if i+1<len(back) else STRIP)-t
                    dur = .64 if k=='m' else 3.45 if source==4 and t==STRIP-1 else min(gap-.23, 3.45)
                    put('right',a+t,29+p,dur,.94 if k=='o' else .79,k=='m')
                for t,p in opens[1].items():
                    put('bass',a+t,29+p,1.7,.92); kit('foot',a+t,'k',.98 if t in (0,3,15,18) else .83)
                if source == 4: kit('brass',a+STRIP-1,'c',.88)
                continue
            if source >= 2:                 # the clean guitar answered backwards; now it leads, forwards
                for t,p in opens[0].items(): put('wire',a+t,29+12+p,2.4,.82)
            for t,p in opens[1].items():    # ribbon, then the mouth: C, G-flat, A-flat, F
                if source == 3: put('ribbon',a+t,29+36+p,2.4,.78)
                else: put('mouth',a+t,29+24+p,2.4,.78)
        # The song began with a short F on the one. It ends on the same F, held.
        ev['mouth'][-1]['len'] = round(8/GRID,5)
        assert round(ev['mouth'][-1]['at']*GRID) == last
        start = last + 8
    assert all(0<=e['at']<start/GRID and e['at']+e['len'] <= start/GRID for tr in ev.values() for e in tr)
    if feet:
        # v21: after everything else is written, so that each foot reads what its hand plays in the end (the
        # right hand's last strip stops on the tie at tick 15, and so does its foot).
        _, opp, strips = next(s for s in sections if s[0]=='opposite')
        for i in range(feet['from'], strips):
            a = opp + i*STRIP
            kicked = {round(e['at']*GRID) for e in ev['foot'] if a <= round(e['at']*GRID) < a+STRIP}
            for hand,drum in (('left','foot'),('right','other-foot')):
                for e in list(ev[hand]):
                    t = round(e['at']*GRID)
                    if not a <= t < a+STRIP or t in kicked: continue     # where the hands meet, one foot is enough
                    muted = bool(e.get('expr',{}).get('pm'))
                    if muted and i < feet['run']: continue
                    kicked.add(t)
                    # an open note is struck as hard as the left foot strikes its mirror
                    kit(drum,t,'k',feet['mute'][0] if muted else .98 if STRIP-1-(t-a) in (0,3,15,18) else .83)
                    if muted:
                        ev[drum][-1]['gain'] = f"{feet['mute'][1 if hand=='left' else 2]:g}dB"
                        ev[drum][-1]['patch'] = ('ct-kit' if hand=='left' else feet['patch'])+' '+feet['mute'][3]
    def track(name,patch,gain,pan=0,out=None,fx=None):
        d=dict(name=name,patch=patch,gain=gain,pan=pan,notes=sorted(ev[name],key=lambda e:e['at']))
        if out: d['out']=out
        if fx: d['fx']=fx
        return d
    # One physical hand-width mute per guitar. The chamber belongs to the two
    # exposed sounds only, so the rests between the chugs stay dry.
    palm=' synth.layers.0.mute=expr.pm*0.56 synth.layers.0.mute_width=0.10'
    room=['reverb kind=chamber mix=0.12 decay=0.85s predelay=12ms']
    tracks=[track('left','ct-twin fx.2.cone=37'+palm,'0.5dB',-.92,'strings'),
            track('right','ct-twin fx.2.cone=41'+palm,'0.5dB',.92,'strings'),
            track('mouth','vosim-voice synth.amp.a=11ms synth.amp.r=78ms','-14dB',-.12,fx=room),
            track('wire','ct-clean','-4dB',.21,fx=room),track('bass','ct-bass','0dB',0,'low'),
            track('foot','ct-kit','2dB',0,'drums',[{'type':'eq','bands':['peak cutoff=4400 q=0.84 gain=6dB']}]),
            track('snare','ct-kit'+(crack[0] if crack else ''),crack[2] if crack else '2dB',0,'drums',[{'type':'eq','bands':[crack[1]]}] if crack and crack[1] else None),track('hat','ct-kit','11dB',-.18,'drums'),
            track('brass','ct-kit','-4.5dB',.15,'drums'),track('skins','ct-kit','1.5dB',0,'drums')]
    for tr in tracks:
        if tr['name'] in tie_gains:
            tr['gain']={'value':tr['gain'],'mod':[{'src':'auto.carry','amount':1}]}
            pts=[['0b',0]]+[[f'{t/GRID:g}b',db] for t,db in tie_gains[tr['name']]]
            tr['auto']={'carry':{'points':pts,'curve':0}}
    if mirror_bass:
        # Let the upper string ring without choking the low thumb. Same bass
        # bus as the picked part; no low-octave double or added kick.
        tracks.append(track('thumb','slap-bass play.mono=false','-4.5dB',0,'low'))
    if crease:
        # Bring the quiet middle's clean guitar up on the fader for the first
        # two strokes under the distorted pair, then return to its original
        # level for the exposed one. No gain change in either of its old parts.
        _, onset, strips = next(s for s in sections if s[0]=='raised')
        first = onset + (strips//2-3)*STRIP
        wire = next(t for t in tracks if t['name']=='wire')
        wire['gain']={'value':wire['gain'],'mod':[{'src':'auto.crease','amount':1}]}
        points=[['0b',0],[f'{first/GRID:g}b',0]]
        for j,boost in enumerate((6,4,0)):
            middle=(first+j*STRIP+STRIP//2)/GRID
            points.extend([[f'{middle-.5:g}b',boost],[f'{middle+.5:g}b',boost]])
        wire['auto']={'crease':{'curve':0,'points':points}}
    # Shorten the borrowed pedal's swell enough to speak on the strip's last
    # sixteenth. No echo crossing into the other player's chair, or over the stop.
    steel = 'pedal-steel synth.amp.a=85ms synth.amp.r=80ms fx.1.mix=0 fx.2.mix=0 play.glide=65ms'
    for side,pan in [('left',-.77),('right',.77)]:
        if not heavy: tracks.append(track('steel-'+side,steel,'-5.5dB',pan,'strings'))
    assert heavy == (not ev['steel-left'] and not ev['steel-right'])
    if rig:
        for t in tracks:
            if t['name'] in ('left','right'):
                t['patch'] = t['patch'].replace('ct-twin ', 'ct-twin '+rig[0]+' ')
                if rig[1] and isinstance(t['gain'], dict): t['gain']['value'] = rig[1]   # the right hand's fader has a lane (v7's ties)
                elif rig[1]: t['gain'] = rig[1]
                if rig[2]: t['fx'] = [{'type':'eq','bands':(CHEST[0] if chest and reading else [])+rig[2]+([crack[3]] if crack and crack[3] else [])}]
                if crack and crack[4]:      # v20: the hands' faders, so the band is as loud as it was with their top given back
                    if isinstance(t['gain'],str): t['gain'] = f"{float(t['gain'][:-2])+crack[4]:g}dB"
                    else: t['gain'] = dict(t['gain'],value=f"{float(t['gain']['value'][:-2])+crack[4]:g}dB")
    if thumbs:
        for side,way in [('left',-1),('right',1)]:
            tracks.append(track('tines-'+side,TINES[0],TINES[1],way*TINES[2],fx=room))
    if drum_hand:
        # Seven fixed drums for the two keys, lowest at the drummer's right.
        pitches = sorted({base+p for base in (41,44) for p in opens[1].values()})
        heads = {'head'+str(m): {'patch':'modal-tom','pitch':pitch(m),
                 'pan':round(.45-.8*j/(len(pitches)-1),3)} for j,m in enumerate(pitches)}
        # The mouth is a much quieter partner than the heavy guitars. Bring the
        # rack up between passages, while the stick is off it.
        beats = {name:t/GRID for name,t,_ in sections}
        drums = track('drum-hand',{'kit':heads},
                      {'value':'0dB','mod':[{'src':'auto.touch','amount':1}]},out='drums')
        drums['auto'] = {'touch':{'curve':0,'points':[['0b',-13],
                         [f"{beats['thumbprint']:g}b",-13],[f"{beats['one hand']:g}b",0]]}}
        tracks.append(drums)
    if signature:
        patch = {'extends':'ondes synth.amp.r=90ms fx.0.mix=0.1 fx.0.decay=1.1s fx.1.mix=0.04 fx.1.decay=0.8s',
                 'synth':{'pitch':{'value':0,'mod':[{'src':'lfo.vib','amount':.13},{'src':'expr.ribbon','amount':1}]}}}
        ribbon = track('ribbon',patch,{'value':'-14.5dB','mod':[{'src':'auto.sign','amount':-1.5}]},
                       {'value':-.2,'mod':[{'src':'auto.sign','amount':.78}]})
        ribbon['auto'] = {'sign':{'points':[['0b',0],[f'{(learn+STRIP)/GRID:g}b',0],[f'{sign/GRID:g}b',1]],'curve':0}}
        if facing:
            # Back beside the mouth, at its first level, to hand the tune home.
            ribbon['auto']['sign']['points'] += [[f'{page/GRID:g}b',1],[f'{(page+2*STRIP)/GRID:g}b',0]]
        tracks.append(ribbon)
    if copy:
        # The same guitar, the same chair and the same cabinet as the left hand; only the amp differs.
        left = next(t for t in tracks if t['name']=='left')
        tracks.append(track('copy',COPY[0]+palm,COPY[1],left['pan'],'strings'))
    if palmas: tracks.append(track('palmas',palmas[0],palmas[1],palmas[2]))
    if feet: tracks.append(track('other-foot',feet['patch'],feet['gain'],feet['pan'],'drums',[{'type':'eq','bands':[feet['eq']]}]))
    tape = None
    if blot:
        # v22: the left hand's strip as ink first wrote it, alone and forwards, recorded on its own rig and PLAYED
        # BACKWARDS on its own side, a sixteenth early: each note of it swells up to the instant the right hand, reading
        # the strip from the far end, strikes the same note.
        left = next(t for t in tracks if t['name']=='left')
        _, page, mirrored = next(s for s in sections if s[0]=='facing page')
        fwd = strip()
        notes = []
        for i,(t,p,k) in enumerate(fwd):
            gap = (fwd[i+1][0] if i+1<len(fwd) else STRIP)-t
            notes.append({'at':round(t/GRID,5),'len':round((.64 if k=='m' else min(gap-.23,3.45))/GRID,5),'pitch':pitch(29+p),
                          'vel':.94 if k=='o' else .79,**({'expr':{'pm':1}} if k=='m' else {})})
        tape = {'the-ink-on-tape':{'tempo':BPM,'length':f'{STRIP/GRID:g}b','tail':'0s','seed':1,
                                   'tracks':[{'name':'left','patch':left['patch']+' play.humanize.time=0ms play.humanize.vel=0',
                                              'gain':left['gain'],**({'fx':left['fx']} if left.get('fx') else {}),'notes':notes}]}}
        for j in range(blot['strips']):
            put('blot',page+j*STRIP-blot['ahead'],'C4',STRIP,1)
        tracks.append(track('blot',{'about':"The Other Hand: the left hand's strip on tape, played backwards (the wet ink's image on the facing page).",
                                    'play':{'gate':1},'synth':{'amp':{'a':'3ms','s':1,'r':'6ms'},
                                    'layers':[{'type':'sample','song':'the-ink-on-tape','root':'C4','reverse':True}]}},
                            blot['gain'],left['pan'],'strings'))
    buses={'strings':{'fx':[{'type':'eq','bands':['peak cutoff=360 q=0.8 gain=-2dB','peak cutoff=730 q=1 gain=1.5dB']}]},
           'drums':{'fx':['reverb kind=room mix=0.10 decay=0.53s predelay=7ms',{'type':'glue','threshold':'-22dB','ratio':2.5,'attack':'18ms','release':'120ms'},'clip ceiling=-13dB']},
           'low':{'fx':[{'type':'eq','bands':['peak cutoff=48 q=1.4 gain=-4dB','peak cutoff=98 q=1 gain=3dB','peak cutoff=310 q=0.9 gain=-4dB']},{'type':'compressor','threshold':'-24dB','ratio':5,'attack':'14ms','release':'115ms'}]}}
    if album_kit: buses['drums']['fx'].append({'type':'eq','bands':KIT_EQ+([CHEST[1]] if chest and reading and rig else [])})
    doc=dict(about='The Other Hand — chirpers, Common Time, track twelve. One strip of attacks read forwards and back under an unbroken count of four.',tempo=BPM,seed=1,length=f'{start/GRID:g}b',tail='1.3s',ceiling='-1dB',loudness=(feet['loudness'] if feet and feet['loudness'] else crack[5] if crack and crack[5] else palmas[4] if palmas and palmas[4] else CHEST[2] if chest and reading and rig else READING[3] if reading else HEAVY_LOUDNESS if heavy else COPY_LOUDNESS if copy else THUMBS_LOUDNESS if thumbs else PAGE_LOUDNESS) if facing else -10,event_stable=True,buses=buses,master={'fx':[{'type':'eq','bands':['hp cutoff=24']},'gain gain=2dB']},tracks=tracks)
    if tape:
        doc = {**{k:v for k,v in doc.items() if k!='tracks'},'songs':tape,'tracks':doc['tracks']}
        if blot['loudness']: doc['loudness'] = blot['loudness']
    return doc,sections

def dump(d):
    return '\n'.join('tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) if k=='tracks' else k+': '+json.dumps(v) for k,v in d.items())+'\n'

# v27 (chirper-zero; instrument round: the two hands' muted stroke, 513 strokes): THE STROKE GETS ITS FRONT BACK.
# v23 cured the stroke's low end by lifting the palm and said its cost: the attack over the body fell (both hands
# together 3.37 / 3.65 -> 2.95 / 3.21 in 'ink' and 'raised'; six records 3.63, 3.5 to 4.2; riffpunch --strokes:
# the attack's peak against 30 to 60 ms later). Read ONE HAND AT A TIME it was 2.45 / 2.66.
# NOTHING AT THE STRING MOVES IT ON THIS RIG (one control at a time, the left hand, 'ink' / 'raised'): the pick
# half as soft 2.41 / 2.56; the thump off 2.51 / 2.66; pick_hard, click, the pick's noise +8 dB, a deader string
# under the palm: nothing; the palm's filter back to 3.4 octaves 2.53 / 2.73; a fuller palm (0.8) 2.75 / 2.93 but
# the low end's fall +0.63 / +1.43 (v23's cure undone). The track's eq is part of it (with no eq 3.02 / 3.23;
# the 2.6 kHz cut alone costs 0.25) but the eq is the mix's (v19, v23). WHAT MOVES IT IS AFTER THE STRING:
#   the amp's sag 0.2 -> 0.5 (the supply gives under the hit and recovers)             2.70 / 2.88
#   the front compressor let the pick through (attack 2 -> 15 ms) and held longer
#     (release 60 -> 200 ms)                                                            2.60 / 2.84
#   those and the palm's filter at 3.4 octaves                                          3.06 / 3.10
#   and the engine's transient shaper after the eq, attack +3 dB, body -1 dB            3.49 / 3.45
# Both hands together 2.96 / 3.21 -> 3.75 / 3.80. The low end's fall stays inside (-0.73 / +0.01 -> -0.64 /
# -0.31), the rise 17.5 -> 14.5 / 15.25 ms (theirs 13.5 to 23.5), the scoop -7.5 / -7.7 -> -6.9 / -7.3 (theirs
# to -6.5: the edge). The tone does not move (the rig alone against a record's, 2.46 -> 2.38 and 2.73 -> 2.67);
# the faders come up 1.2 dB so the two hands alone are as loud as before (the shaped stroke is quieter between
# its fronts). THE TAPE IS NOT RE-RECORDED: the left hand's strip on tape (the blot under the facing page) keeps
# the sound it was taped with (it cannot be benched alone: bd-4942f3).
# The shaper at attack +4 read 3.61 / 3.52 alone and 3.81 / 4.00 together (the top of the records' range).
SNAP = {'patch': 'fx.1.sag=0.5 fx.0.attack=15ms fx.0.release=200ms synth.filters.0.cutoff.mod.0.amount=-3.4',
        'shaper': 'transient attack=3 sustain=-1', 'trim': 1.2, 'tape': False, 'loudness': None}


def snap(doc):
    """v27: the two hands' stroke gets its front back: the amp sags, the compressor lets the pick through, the palm
    closes the filter as far as it did, and a transient shaper after the eq lifts each front over its body."""
    hands = [t for t in doc['tracks'] if t['name'] in ('left', 'right')]
    if SNAP['tape']: hands += [t for s in doc.get('songs', {}).values() for t in s['tracks']]
    for t in hands:
        if isinstance(t['patch'], str) and t['patch'].startswith('ct-twin '):
            cut = t['patch'].find(' play.humanize.time=0ms')        # the tape's copy ends with its own two play fields
            t['patch'] = t['patch'] + ' ' + SNAP['patch'] if cut < 0 else t['patch'][:cut] + ' ' + SNAP['patch'] + t['patch'][cut:]
            if SNAP['shaper']: t['fx'] = t['fx'] + [SNAP['shaper']]
            if isinstance(t['gain'], dict): t['gain'] = dict(t['gain'], value=f"{float(t['gain']['value'][:-2]) + SNAP['trim']:g}dB")
            else: t['gain'] = f"{float(t['gain'][:-2]) + SNAP['trim']:g}dB"
    if SNAP['loudness']: doc['loudness'] = SNAP['loudness']


# v28 (chirper-one; palette round: ONE INSTRUMENT ADDED, the part the song lacked, on an engine feature the album
# had not used: the drum layer's BRUSH, dragged). THE PENCIL. The song's first section is called 'pencil' and
# everything in it is a metaphor for one: a voice finds a line from its two ends, a clean string marks where the
# two readings meet (v26). Now each of those notes is also a MARK: under every note the voice and the string play
# there, a pencil stroke of 0.3 s. The voice's strokes are drawn from the left edge to the middle, the string's
# (the other hand's) from the right edge to the middle: the line is drawn from both ends, in the room as well.
# ON THE FACING PAGE (3:58.4 on), whose last four strips are the pencil's four read by the other hand, the strokes
# come back the other way round: the voice's from the right, the string's from the left. 15 strokes and 20.
# THE SOUND: no noise generator: a wire brush DRAGGED (`beater: brush`, `sweep: 300ms`) over a small head tuned to
# F5 that rings 40 ms, so what is heard is the friction, coloured by a surface: it swells in and fades out and
# no two strokes are alike (their peaks fall 80 to 220 ms in). Through 600 Hz-6.5 kHz its weight is at 2-4 kHz
# (centroid 3.1 kHz): under the foot's hat, which is above 8 kHz, and over the voice.
# Benched: the same on G5 with the drum as it comes (a rubbed drum: as much at 500 Hz-1 kHz as at 2-4 kHz, centroid
# 2.3 kHz) ; on C6, ringing 50 ms (its weight at 1-4 kHz, 2.8 kHz) ; on C6 unfiltered (a hiss, 6.7 kHz, the hat's place) ; and this
# one 4 dB louder (the strokes 3 to 10 dB under the voice, hat and string, and 'pencil' 0.8 to 1.0 dB louder
# finished: too much for a pencil).
# 'patch' ; 'pitch': the head's note ; 'gain': the two tracks' fader ; 'eq' ; 'vel' ; 'stroke': the shortest and
# longest stroke, beats ; 'reach': where a stroke starts and ends (pan; the voice's side is negative) ; 'pages':
# the sections and which way round (1 as written, -1 mirrored) ; 'loudness' (None: unchanged).
# --without-pencil gives v27 byte for byte. (--pencil '{...}': a bench.)
PENCIL = {'patch': {'about': "The Other Hand: the pencil. A wire brush dragged across a small, tight, damped head: a mark being made on paper.",
                    'synth': {'layers': [{'type': 'drum', 'beater': 'brush', 'sweep': '300ms', 'decay': '40ms', 'slap': 1.3}],
                              'amp': {'a': '1ms', 'd': 0, 's': 1, 'r': '60ms'}}},
          'pitch': 'F5', 'gain': '-14dB', 'eq': ('hp cutoff=600', 'lp cutoff=6500'), 'vel': 0.7, 'stroke': (0.5, 0.7),
          'reach': (0.75, -0.05), 'pages': {'pencil': 1, 'facing page': -1}, 'loudness': None}


def the_pencil(doc, sections):
    """v28: under every note the voice and the clean string play in 'pencil' and on the facing page, a pencil stroke:
    left to right under the voice and right to left under the string; on the facing page the other way."""
    track = {t['name']: t for t in doc['tracks']}
    assert 'pencil' not in track and 'pencil-back' not in track
    for name, src, side in (('pencil', 'mouth', -1), ('pencil-back', 'wire', 1)):
        notes, points = [], []
        for page, way in PENCIL['pages'].items():
            _, start, count = next(x for x in sections if x[0] == page)
            a, b = start / GRID, (start + count * STRIP) / GRID
            for n in sorted((n for n in track[src]['notes'] if a <= n['at'] < b), key=lambda n: n['at']):
                ln = round(min(max(n['len'], PENCIL['stroke'][0]), PENCIL['stroke'][1]), 4)
                notes.append({'at': n['at'], 'len': ln, 'pitch': PENCIL['pitch'], 'vel': PENCIL['vel']})
                points += [[f"{n['at']:g}b", side * way * PENCIL['reach'][0]], [f"{n['at'] + ln - .002:g}b", side * way * PENCIL['reach'][1]]]
        assert notes and all(y['at'] - x['at'] >= x['len'] for x, y in zip(notes, notes[1:])), name
        new = {'name': name, 'patch': PENCIL['patch'], 'gain': PENCIL['gain'], 'pan': {'value': 0, 'mod': [{'src': 'auto.across', 'amount': 1}]},
               'auto': {'across': {'points': points, 'curve': 0}}, 'notes': notes}
        if PENCIL['eq']: new['fx'] = [{'type': 'eq', 'bands': list(PENCIL['eq'])}]
        doc['tracks'].append(new)
    if PENCIL['loudness']: doc['loudness'] = PENCIL['loudness']


# v29 (chirper-alpha; instrument round: the hi-hat, both its strokes, 255 strokes: 199 by the sticks, 56 by the
# foot). THE COUNT IS STRUCK ON METAL. No note changes and no other part; the hat track's fader stays where it was.
# The song is "one strip read forwards and back under an unbroken count of four", and the count was the album
# kit's closed hat as it comes: white noise and three squares through an 8 kHz high-pass, 45 ms. READ ALONE (raw,
# own seed): the sticks' stroke had 74% of its power over 8 kHz and 2% under 4 kHz (centroid 11.9 kHz) and was
# 20 dB down in 20 ms: a tick of hiss. Beside the top of the eleven records' drums (tools/cymspec.py, shapes) it
# stood 11.2 dB away on average, +20 dB at 12.5 kHz: the records' metal has its weight at 4-6 kHz. IN THE MIX it
# stood 15 to 21 dB over everything else at 8-16 kHz and 3 to 7 dB UNDER everything else at 4-8 kHz: the count was
# in the top octave and nowhere else.
# NOW both strokes are a cymbal's plate (the engine's modal layer, `modes: cymbal`, which the album kit's crash and
# china use and no hat on the album does), lightly damped and driven a little, as the china is:
#   the sticks (`h`): the plate struck near its edge, with a stick's tick (4 ms of noise) on the front, 50 ms to
#     fall 20 dB, through a 2.5 kHz high-pass and a shelf that takes 9 dB off the top from 9 kHz: centroid 7.0 kHz,
#     20% / 54% / 26% under 4 kHz / at 4-8 / over 8; 3.2 dB from the records' top (11.2).
#   the foot (`hp`): THE SAME PLATE, closed: no tick, a slower front, a darker strike, 32 ms, 1.5-9 kHz: centroid
#     5.2 kHz, 39% / 48% / 13%; 1.0 from the records' top (8.1).
# THE LEVEL is set on the mix: the top octave keeps what the old hat gave it ('ink', raw: 8-16 kHz -0.8 -> -0.9
# against the records' rows with no voice) and the octave below gains (4-8 kHz -0.8 -> -0.4). At that level a
# stick stroke stands 8.3 dB under everything else (K; it was 12.1) and 1 to 5 dB OVER everything else at 4-8 kHz.
# Benched and not kept (cand.py): the plate at damping 0.1 to 0.5 with a 120-150 ms decay (10 to 21 ms, a tick
# again; the 50 ms came with damping 0.02, a 400 ms decay, a gentler amp curve and the drive, changed together); the album's other recipe (the library hat opened to 4.5 kHz with
# an eq: 6.3 from the records, 16 ms); the 808's six squares (7.5); the plate on F5, and two plates a fourth apart
# (the same within 0.3 dB in every third of an octave from 2 kHz: the note does not tune this mode set); a
# gentler shelf (the mix's two top bands within 0.2 dB) and a steeper one (half a decibel less top octave in the
# mix); 2 dB lower and 1 dB higher.
# 'h': the sticks' stroke, 'hp': the foot's (kit pieces over the album kit's; None leaves a piece as it comes) ;
# 'gain': the hat track's fader (None: unchanged) ; 'loudness' (None: unchanged).
# --without-plates gives v28 byte for byte. (--plates '{...}': a bench.)
def _plate(bright, strike):
    return {'type': 'modal', 'modes': 'cymbal', 'name': 'plate', 'bright': bright, 'damp': 0.02, 'decay': '400ms', 'strike': strike, 'tilt': 1, 'vary': 0.5}


PLATES = {'h': {'pitch': 'C5', 'gain': '-16dB', 'choke': 'hat', 'patch': {'play': {'vel_sens': 0.6}, 'synth': {
              'amp': {'a': '0.2ms', 'd': '70ms', 's': 0, 'r': '20ms', 'curve': 2}, 'env': {'att': {'a': '0.1ms', 'd': '4ms', 's': 0}},
              'filters': ['hp cutoff=2500', 'peak cutoff=5500 q=0.8 gain=2dB', 'highshelf cutoff=9000 gain=-9dB'],
              'layers': [_plate(0.9, 0.9), {'name': 'tick', 'type': 'noise', 'level': {'value': '-66dB', 'mod': [{'src': 'env.att', 'amount': 40}, {'src': 'vel', 'amount': 6}]}}],
              'drive': 0.3}}},
          'hp': {'pitch': 'C5', 'gain': '-23dB', 'choke': 'hat', 'patch': {'play': {'vel_sens': 0.6}, 'synth': {
              'amp': {'a': '0.5ms', 'd': '45ms', 's': 0, 'r': '15ms', 'curve': 2}, 'filters': ['hp cutoff=1500', 'lp cutoff=9000'],
              'layers': [_plate(0.6, 1.0)], 'drive': 0.3}}},
          'gain': None, 'loudness': None}


def the_count_is_struck_on_metal(doc):
    """v29: the hat's two strokes are a cymbal's plate, struck (the sticks) and closed (the foot), not filtered noise."""
    hat = next(t for t in doc['tracks'] if t['name'] == 'hat')
    assert hat['patch'] == 'ct-kit' and {n['pitch'] for n in hat['notes']} <= {'h', 'hp'}
    kit = {k: PLATES[k] for k in ('h', 'hp') if PLATES[k]}
    if kit: hat['patch'] = {'extends': 'ct-kit', 'kit': kit}
    if PLATES['gain']: hat['gain'] = PLATES['gain']
    if PLATES['loudness']: doc['loudness'] = PLATES['loudness']


# v30 (chirper-zero; palette round. THE SWAP, NAMED: none taken out; ONE INSTRUMENT ADDED, a sound no song on the
# record has: a typewriter's MARGIN BELL. One new track, `bell`, 18 strokes: 12 in 'ink' (0:10.96-0:43.85) and 6 in
# 'one hand' (3:22.8-3:44.7). No other note, sound or fader changes.) THE MARGIN BELL.
# The song is a strip of nineteen sixteenths read from both ends under a count of four, and everything in it is
# named for writing: pencil, ink, carbon, the ribbon, a thumbprint, signed, the facing page. A strip is a LINE. The
# machine that writes a line in ink through a ribbon has a bell fixed near the right margin: it rings once, a few
# characters before the line is full, and the other hand throws the carriage back. Nothing in the song marked the
# line: the drummer counts four and never says nineteen, so the strip's length is something the listener has to
# work out from the riff. Now the line has its bell, where a typewriter's is: on the row's last open note (its
# fifteenth place, the C), four places before the end. And because the bell is fixed to a PLACE ON THE LINE, when it
# rings tells which end the line is being read from: read forwards it rings late (the strip's sixteenth
# sixteenth); read from the other end it rings early (the fourth), with the same C.
#   'ink'       the line is read forwards eleven times: the bell rings late each time, on the left while the left
#               hand reads alone (strips 1-4), in the middle once both hands read (5-11). On the twelfth strip the
#               other hand reads it alone from the far end (v17): the bell rings EARLY, on the right. That is the
#               first sign of what 'opposite' is about to do.
#   'one hand'  both hands read from the far end as one: the bell rings early, in the middle, on the six strips
#               where the hands play the C (the strip the drummer answers alone, and the last, have none).
# It is not in 'opposite', 'raised' or 'turn over' (two readers at once would be two bells a strip over the pops,
# the claps and the second foot; Harry: "I can follow both", "Prefer both heavy") nor on the pencilled pages.
# The bell: a small steel cup struck once (four partials at 1, 2.32, 4.25 and 6.63, the upper ones falling first,
# and a 4 ms clapper), on C7: the row's C, five octaves over the guitars' (2093 Hz, in the octave where 'one hand'
# stood 2 to 3 dB short of the records). Where each stroke falls is READ FROM THE GUITARS' OWN NOTES (the higher of
# a hand's open notes at the fourth and sixteenth sixteenths is the C), so it follows whatever the hands do.
# --without-bell gives v29 byte for byte. (--bell '{...}': a bench.)
BELL = {'patch': {'about': "The Other Hand: the margin bell. A typewriter's small steel cup bell, struck once by its clapper a few places before the end of the line.",
                  'synth': {'amp': {'a': '0.2ms', 'curve': 3, 'd': '1500ms', 'r': '600ms', 's': 0}, 'env': {'h': {'a': '0.2ms', 'd': '4ms', 's': 0}},
                            'layers': [{'type': 'additive', 'damp': 3.0, 'partials': [[1, 1], [2.32, 0.45], [4.25, 0.22], [6.63, 0.08]]},
                                       {'type': 'noise', 'level': {'value': '-60dB', 'mod': [{'src': 'env.h', 'amount': 36}]}}]}},
        'pitch': 'C7', 'gain': '-16dB', 'vel': .7, 'len': 2,
        'lines': ('ink', 'one hand'),                       # the sections whose lines have the bell
        'pan': {'left': -.45, 'right': .45, 'both': 0},     # who is reading: where the bell is
        'room': 'reverb kind=room decay=0.5s mix=0.1 predelay=8ms',
        # the bell's eighteen strokes lower the song's measured loudness a hair: with the target left at -9.966 every
        # stretch it is not in came out 0.005 to 0.015 dB quieter. This much holds the loud ones where they were.
        'loudness': -9.963}


def the_margin_bell(doc, sections):
    """v30: a typewriter's margin bell on the row's last open note, in 'ink' and 'one hand'; when it rings in the
    strip tells which end the line is read from."""
    track = {t['name']: t for t in doc['tracks']}
    assert 'bell' not in track
    low = lambda p: min(PITCH.index(x[:-1]) + 12 * int(x[-1]) for x in str(p).split(','))
    notes, points = [], []
    for sec in BELL['lines']:
        _, start, count = next(x for x in sections if x[0] == sec)
        for i in range(count):
            a = start + i * STRIP
            where = {}
            for hand in ('left', 'right'):
                opens = {round(n['at'] * GRID - a): low(n['pitch']) for n in track[hand]['notes']
                         if a <= n['at'] * GRID < a + STRIP and not (n.get('expr') or {}).get('pm')}
                if 3 in opens and 15 in opens: where[hand] = 15 if opens[15] > opens[3] else 3
            if not where: continue                                   # nobody plays the C on this line: no bell
            assert len(set(where.values())) == 1, (sec, i, where)     # two readers from two ends: not a line for one bell
            t = (a + next(iter(where.values()))) / GRID
            who = 'both' if len(where) == 2 else next(iter(where))
            notes.append({'at': round(t, 5), 'len': BELL['len'], 'pitch': BELL['pitch'], 'vel': BELL['vel']})
            if points: points.append([f"{t - .06:g}b", points[-1][1]])   # the bell stays where its last reader was until the next rings
            points.append([f"{t - .05:g}b", BELL['pan'][who]])
    for x, y in zip(notes, notes[1:]): x['len'] = round(min(x['len'], y['at'] - x['at'] - .05), 5)
    assert notes and all(y['at'] - x['at'] > x['len'] > 1 for x, y in zip(notes, notes[1:]))
    new = {'name': 'bell', 'patch': BELL['patch'], 'gain': BELL['gain'], 'pan': {'value': 0, 'mod': [{'src': 'auto.reader', 'amount': 1}]},
           'auto': {'reader': {'points': [['0b', points[0][1]]] + points, 'curve': 0}}, 'notes': notes}
    if BELL['room']: new['fx'] = [BELL['room']]
    doc['tracks'].append(new)
    if BELL['loudness']: doc['loudness'] = BELL['loudness']


# v31 (chirper-zero; instrument round: THE CHINA, the 52 strokes the sticks play in 'turn over', 2:49.9-3:22.8, and
# nowhere else in the song. No note, velocity or fader changes.) THE CHINA IS A PLATE, NOT A HISS.
# chirper-alpha's v29 handoff named it: "THE NEXT INSTRUMENT HERE IS THE CHINA": 'turn over' the one section over
# the records at 8-16 kHz, and the china alone far from their top. Read this round (bench t12-china):
#   WHO HOLDS THE BAND (the raw mix of 'turn over' with the `brass` track muted): the china adds 4.4 dB at 8-16 kHz
#   and 1.1 at 4-8 kHz. It is most of the top octave there; nobody else can be the excess.
#   THE CHINA ALONE beside the top of the eleven records' drum stems (tools/cymspec.py, a shape): +5.0, +6.9 and
#   +14.2 dB at 10, 12.5 and 16 kHz, 3.31 away on average. The kit's china is a modal plate with `bright` 1 and a
#   lift at 8 kHz: its upper modes are as loud as its body, so above 8 kHz it reads as air rather than as metal.
#   THE FIT is the one Still Owing's china took at v35 (the same kit piece; read here before it was believed, since
#   on Plain Hunt the same fields made the china worse): the plate's `bright` 1 -> 0.6 and its 8 kHz lift moved to
#   5 kHz, where the records' drum tops have their weight. Alone: +0.0, -0.7, +4.6 at 10, 12.5, 16 kHz; 1.08 away.
#   Its level is NOT moved: alone it is 0.3 dB louder (K), and each stroke stands 7.0 dB under the band (7.2 before;
#   the records' chinas 4.8 to 7.4). A decibel less (benched) read a hair better beside the records and put the
#   stroke under their range: not taken.
#   THE MIX of 'turn over' beside the records (nobody sings there): 0.689 -> 0.500; 8-16 kHz +2.9 -> +1.0, and
#   4-8 kHz +0.7 -> +1.0 (the cost: the energy moves down an octave, to where the section was already a little
#   over). `bright` 0.7 (benched) left 8-16 kHz at +2.1.
# The sticks' two jobs in the section are untouched: the count in quarters, and the strip's four open notes while
# the page is upside down (chirper-one's v25). The crashes and the ride's edge on the same track are other pieces
# and are not changed.
# 'kit': overrides on the kit's china (piece x) for the `brass` track ; 'loudness': the target (None: unchanged).
# --without-china gives v30 byte for byte. (--china '{...}': fields for a bench.)
# The darker plate asks 0.01 dB less of the master: with the target left at -9.963 every other stretch came out 0.010
# to 0.028 dB quieter. This much holds them where they were (each within 0.001 dB, 77 to 85 dB left).
CHINA = {'kit': 'kit.x.patch.synth.layers.0.bright=0.6 kit.x.patch.synth.filters.2.cutoff=5000', 'loudness': -9.9525}


def the_china_is_a_plate(doc):
    """v31: the china's own tone (see CHINA): overrides on piece x of the `brass` track's kit. No note changes."""
    t = next(t for t in doc['tracks'] if t['name'] == 'brass')
    assert t['patch'] == 'ct-kit' and any(n['pitch'] == 'x' for n in t['notes']), t['patch']
    if CHINA['kit']: t['patch'] = t['patch'] + ' ' + CHINA['kit']
    if CHINA['loudness']: doc['loudness'] = CHINA['loudness']


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('-o','--out',type=Path,default=OUT); ap.add_argument('--map',action='store_true'); ap.add_argument('--without-drum-hand',action='store_true',help='regenerate v2'); ap.add_argument('--without-crease',action='store_true',help='regenerate v3')
    ap.add_argument('--without-mirror-bass',action='store_true',help='regenerate v4')
    ap.add_argument('--without-picking-hand',action='store_true',help='regenerate v5')
    ap.add_argument('--without-signature',action='store_true',help='regenerate v6')
    ap.add_argument('--without-ties',action='store_true',help='regenerate v7, without the two common-tone handoffs')
    ap.add_argument('--without-facing-page',action='store_true',help='regenerate v8, ending on the signed chord')
    ap.add_argument('--without-palindrome',action='store_true',help='regenerate v9, without the ribbon over the opposed guitars')
    ap.add_argument('--without-album-kit',action='store_true',help="regenerate v10, the kit's bus without the album's eq")
    ap.add_argument('--without-dominant',action='store_true',help="regenerate v11, 'turn over' on F throughout")
    ap.add_argument('--without-thumbs',action='store_true',help="regenerate v12, the clean guitar answering the voice in 'thumbprint'")
    ap.add_argument('--without-carbon-copy',action='store_true',help="regenerate v13, the copy strips of 'carbon' on the ink's own amp")
    ap.add_argument('--with-steel',action='store_true',help="regenerate v14, the pedal steel reading back in 'turn over'")
    ap.add_argument('--without-turned-page',action='store_true',help="regenerate v15, 'turn over' read the right way up throughout")
    ap.add_argument('--without-first-reading',action='store_true',help="regenerate v16, the last strip of 'ink' in unison")
    ap.add_argument('--without-chest',action='store_true',help="regenerate v17, the two hands without their chest and the kit's bus without its cut at 190 Hz")
    ap.add_argument('--without-palmas',action='store_true',help="regenerate v18, the count in 'opposite' without its other hand")
    ap.add_argument('--without-crack',action='store_true',help="regenerate v19, the album kit's snare as it comes and the two hands with their top")
    ap.add_argument('--without-other-foot',action='store_true',help="regenerate v20, the foot in 'opposite' with the left hand only")
    ap.add_argument('--without-blot',action='store_true',help="regenerate v21, the facing page without the left hand's tape played backwards")
    ap.add_argument('--without-lean',action='store_true',help="regenerate v22, the bass on the album's old chain and the two hands at a full palm")
    ap.add_argument('--without-counted-copy',action='store_true',help="regenerate v23, 'carbon' with one soft snare a bar and no count")
    ap.add_argument('--counted',help='a bench: COUNTED fields to change, as a JSON object')
    ap.add_argument('--without-turned-kit',action='store_true',help="regenerate v24, the kit the right way up through 'turn over'")
    ap.add_argument('--kit',help='a bench: KIT_TURNED fields to change, as a JSON object')
    ap.add_argument('--without-ruled-page',action='store_true',help="regenerate v25, 'pencil' with no count and the line sung whole three times")
    ap.add_argument('--ruled',help='a bench: RULED fields to change, as a JSON object')
    ap.add_argument('--without-snap',action='store_true',help="regenerate v26, the two hands' stroke without its front (the amp's sag, the compressor, the palm's filter, the transient shaper)")
    ap.add_argument('--snap',help='a bench: SNAP fields to change, as a JSON object')
    ap.add_argument('--without-pencil',action='store_true',help="regenerate v27: no pencil strokes under the voice and the clean string in 'pencil' and on the facing page")
    ap.add_argument('--pencil',help='a bench: PENCIL fields to change, as a JSON object')
    ap.add_argument('--without-plates',action='store_true',help="regenerate v28: the hat as the album kit's comes (noise through a high-pass)")
    ap.add_argument('--plates',help='a bench: PLATES fields to change, as a JSON object')
    ap.add_argument('--without-bell',action='store_true',help="regenerate v29: no margin bell in 'ink' and 'one hand'")
    ap.add_argument('--bell',help='a bench: BELL fields to change, as a JSON object')
    ap.add_argument('--without-china',action='store_true',help="regenerate v30: the china in 'turn over' as the album kit's comes")
    ap.add_argument('--china',help='a bench: CHINA fields to change, as a JSON object')
    ap.add_argument('--stock-rig',action='store_true',help="v15's notes on the two hands' rig as it was up to v14 (not a version)"); a=ap.parse_args()
    doc,sections=build(not a.without_drum_hand,not a.without_crease,not a.without_mirror_bass,not a.without_picking_hand,not a.without_signature,not a.without_ties,not a.without_facing_page,not a.without_palindrome,not a.without_album_kit,not a.without_dominant,not a.without_thumbs,not a.without_carbon_copy,not a.with_steel,not a.without_turned_page,None if a.stock_rig else HANDS_RIG,not a.without_first_reading,not a.without_chest,not a.without_palmas,not a.without_crack,not a.without_other_foot,not a.without_blot)
    if not a.without_lean and 'songs' in doc: lean(doc)      # only on the whole song as v22 has it (the tape is there when every older switch is on)
    if a.counted: COUNTED.update(json.loads(a.counted))
    if not a.without_counted_copy and not a.without_lean and 'songs' in doc: counted(doc, sections)      # only on the whole song as v23 has it
    if a.kit: KIT_TURNED.update(json.loads(a.kit))
    if not a.without_turned_kit and not a.without_counted_copy and not a.without_lean and 'songs' in doc: turned_kit(doc, sections)      # only on the whole song as v24 has it
    if a.ruled: RULED.update(json.loads(a.ruled))
    if not a.without_ruled_page and not a.without_turned_kit and not a.without_counted_copy and not a.without_lean and 'songs' in doc: ruled(doc, sections)      # only on the whole song as v25 has it
    if a.snap: SNAP.update(json.loads(a.snap))
    if not a.without_snap and not a.without_ruled_page and not a.without_turned_kit and not a.without_counted_copy and not a.without_lean and 'songs' in doc: snap(doc)      # only on the whole song as v26 has it
    if a.pencil: PENCIL.update(json.loads(a.pencil))
    if not a.without_pencil and not a.without_snap and not a.without_ruled_page and not a.without_turned_kit and not a.without_counted_copy and not a.without_lean and 'songs' in doc: the_pencil(doc, sections)      # only on the whole song as v27 has it
    if a.plates: PLATES.update(json.loads(a.plates))
    if not a.without_plates and not a.without_pencil and not a.without_snap and not a.without_ruled_page and not a.without_turned_kit and not a.without_counted_copy and not a.without_lean and 'songs' in doc: the_count_is_struck_on_metal(doc)      # only on the whole song as v28 has it
    if a.bell: BELL.update(json.loads(a.bell))
    if not a.without_bell and not a.without_plates and not a.without_pencil and not a.without_snap and not a.without_ruled_page and not a.without_turned_kit and not a.without_counted_copy and not a.without_lean and 'songs' in doc: the_margin_bell(doc, sections)      # only on the whole song as v29 has it
    if a.china: CHINA.update(json.loads(a.china))
    if not a.without_china and not a.without_bell and not a.without_plates and not a.without_pencil and not a.without_snap and not a.without_ruled_page and not a.without_turned_kit and not a.without_counted_copy and not a.without_lean and 'songs' in doc: the_china_is_a_plate(doc)      # only on the whole song as v30 has it
    if a.map:
        for sec,t,n in sections: print(f'{sec:12s} {t/GRID*60/BPM:6.2f}s — {(t+n*STRIP)/GRID*60/BPM:6.2f}s')
    else: a.out.write_text(dump(doc))
