#!/usr/bin/env python3
"""On Its Hinge — one guitar phrase with two possible walks underneath it.

One cell = twelve eighths. The quick drummer counts six quarters (144/min);
without changing the riff, the broad drummer counts four dotted quarters (96).
A pump organ already breathes in the second time while the first is playing.
Times are in sixteenths here, in regular quarter-note beats in the output.
"""
import argparse
import json
import os
from collections import defaultdict
from pathlib import Path

BPM, SUB, CELL, HOME = 144, 4, 24, 34  # B flat on the next string up from low F
FORM = [('latch', 4), ('quick', 12), ('lean', 8), ('broad', 12), ('bellows', 8),
        ('shoulder', 12), ('swing', 16), ('home', 8), ('shut', 2)]
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t11.yaml'
ORGAN = os.getenv('C10T11_REED', '-9dB')
PUMP = os.getenv('C10T11_PUMP', '-13dB')
# v2: the pitched drum answers the anticipated notes on the next broad footfall.
# Track gain; semitones above the riff. Empty = published v1.
KETTLE = os.getenv('C10T11_KETTLE', '-7dB;0')
# v3: at home the delayed note changes hands, from the opening harmonic
# to a bowed metal rod. Empty restores v2; KETTLE empty still defaults to v1.
ROD = os.getenv('C10T11_ROD', '-9dB' if KETTLE else '')
# v4: keep a double stop ringing over each of the last five changes of feet.
# Register in semitones. Empty restores v3; older version switches still work.
STAY = os.getenv('C10T11_STAY', '0' if ROD else '')
# v5: the muted half of the heavy riff is heard on skins before it is picked.
# Empty restores v4 (and the older switches retain their published defaults).
PICKUP = os.getenv('C10T11_PICKUP', '1' if STAY else '')
# v6: F stays in the clean guitar while the bass changes what that F means.
# Clean harmonic's trim in the middle (dB). Empty restores v5.
PIVOT = os.getenv('C10T11_PIVOT', '4.5' if PICKUP else '')
# v7: a reed phrase around (not inside) the control. Register over low Bb;
# empty restores v6. The four notes come straight from the open guitar strokes.
COUNTER = os.getenv('C10T11_COUNTER', '24' if PIVOT else '')
# v8: open the broad phrases of the swing around a fixed release. Register
# above the original answer in semitones; empty restores v7 byte for byte.
EARLY = os.getenv('C10T11_EARLY', '12' if COUNTER else '')
# v9: when the band stops, the organ is still breathing the broad walk. It
# comes in under the last chord on the dyad it held at 0:50 and keeps it for
# one more cell alone, at the level it always had. That dyad (F, D flat) has
# no root: on the next downbeat the kettle, which only ever had D flat, F and
# C, lands its first B flat and the reeds close.
# The dyad's trim in dB (benched 0, 6 and 10: 0 already stands 10 dB under
# the chord) ; the kettle's B flat in semitones over the low string (empty: no
# kettle) ; its velocity. Empty restores v8 exactly.
BREATH = os.getenv('C10T11_BREATH', '0;0;0.9' if EARLY else '')
if BREATH:
    FORM[-1] = ('shut', 3)
# v10: before the organ arrives, one guitar says the riff from its middle.
# The two halves have their answers in the same places, so D flat and F sound
# together; the clipped strokes no longer coincide. Semitones the turned
# guitar's answers sit above the written ones. Empty restores v9 exactly.
HALF = os.getenv('C10T11_HALF', '12' if BREATH else '')
# v11: the last changes of feet get the grounds of 1:30. Each time the broad
# walk comes back in the second half of the swing, the bass leaves the
# guitars' B flat at the half cell (where the two walks agree, and where the
# band already re-enters) and plants G flat, then E flat, then F under the
# unchanged riff. The quick cells and 'home' stay on B flat. Semitones from
# the low B flat, one for each broad phrase; empty restores v10.
GROUND = os.getenv('C10T11_GROUND', '-4,-7,-5' if HALF else '')
# v12: before the quiet bridge the riff shows its bones. The song opens on the
# riff's open notes alone (harmonics) and comes home on them as ringing
# chords; in the last cell before the bridge the band plays them once in
# between, as stops: no clipped strokes, and guitars, bass and kick strike
# only the four open notes while the broad walk goes on. The opening's
# harmonic plays them too, for the first time since 0:10.
# How many cells thin out: 1 = the last cell only; 2 = the cell before it
# loses its second half's clipped strokes first; 3 = one more cell does that
# and the last two are bare. Scored on seeds 0/11/5 against v11's
# 97.6/94.4/99.3 without the harmonic: 97.0/93.8/99.2, 95.8/93.5/98.9 and
# 90.6/92.3/97.8. Empty restores v11.
BONES = os.getenv('C10T11_BONES', '1' if GROUND else '')
# v13: each walk at half speed, once, on its own riff's joints. The first riff
# is two halves of twelve sixteenths (chord, clipped strokes, answer, twice);
# the second (LIFT) is three groups of eight (two clipped strokes and a chord,
# three times). Six quick steps and four broad ones fit the first; the second
# has been walked in four (1:50) and in six (the swing), never on its groups.
# 1:20-1:27.5, the plain cells before the bones: the broad four at half speed.
#   Two steps a cell, on the riff's two chords, the backbeat on the half cell
#   where both walks agree. The bridge's two toms then keep that count.
# 1:50-2:00, the ten seconds the second riff has to itself: the quick six at
#   half speed. Three steps a cell, one on the head of each group; the
#   backbeat falls on every other step, so it takes two cells to come round.
#   At 2:00 the kettle starts landing on the broad steps and the drummer goes
#   to four with it, against the riff's three.
# Guitars, bass, kick and organ are as written, as at 1:00.
# Cells walked in two before the bones ; cells of the shoulder walked in three
# (4 = until the kettle; 12 = all of it). 0 leaves either out. Empty: v12.
HALFSPEED = os.getenv('C10T11_HALFSPEED', '3;4' if BONES else '')
# v14 (section w7): the first groove comes back, once. The song opens on the
# first riff over the six quick steps, on two guitars and a closed hat, and
# after the hinge at 1:00 that is never heard again: from there the first
# riff is only ever walked in four, and in the swing the quick six carries
# the heavy riff. Now the two-cell quick phrase in the swing's second half
# (2:45-2:50) is the opening again: the wall pair rests after its held
# double stop, the outer pair and the bass enter at the half cell on the
# first riff, the kick goes back to its places and the china hands the six
# steps to the hat. It is 1:00 the other way round: the riff of 2:40 stays
# and the feet change, broad to quick. The single quick cells after it keep
# the heavy riff and the wall. Empty restores v13.
RETURN = os.getenv('C10T11_RETURN', '1' if HALFSPEED else '')
# v15 (instrument: the second pair of guitars, wallL and wallR; chirper-alpha
# found the fault at v14 and benched the album's own trim for it). The pair
# joins at 1:50 on the album's wall rig, which was still on captured cabinet
# files with a 10 dB shelf cut from 5 kHz: under the twin pair it was all
# body and no string. Alone, against a guitar heard alone on the records
# (tools/cabspec.py, third-octaves, 2:20-2:30): +9.6 at 315 Hz, +6.8 at 400,
# +8.2 at 500, +11.6 at 630; -13 at 8 kHz and -19 at 10 kHz. In the song it
# held two thirds to three quarters of 250-500 Hz, and every stretch from
# 1:50 read 2.7 to 4.1 dB over the records there (their passages without a
# voice; this song has none) and 0.8 to 1.9 over at 500 Hz-1 kHz.
# Now the pair stops at its amp (the files and the patch's own eq are off)
# and goes through the engine's cabinet, as the title track's wall rig does
# and as the twin pair here already did (Harry, 17 Nov, on the title track's
# guitar heard alone: "The engine's cabinet is nearer"). Same amp, same
# notes. Alone it reads +1.3 / +2.2 / +3.1 / +3.3 at 315 / 400 / 500 /
# 630 Hz and -1.1 / -3.0 at 8 / 10 kHz: no third-octave from 315 Hz to
# 12.5 kHz further than 3.4 dB from the record's guitar (it was 18.9).
# microphone, 0 the cone's centre to 1 its edge (0.3 put the pair 3 to 4.5 dB
# over the record's guitar at 2.5-5 kHz and home 1.8 over at 2-4 kHz; 0.5
# left the mix's 4-8 kHz, already short, shorter) ; the left and right
# speakers' cones (the title track's wall pair) ; distance ; track gain (the
# pair alone as loud as the album's trim would have made it: -25.1 LUFS).
# Empty restores v14 byte for byte.
SECOND = os.getenv('C10T11_SECOND', '0.4;14,15;0.15;-1.4' if RETURN else '')
# v16: THE BOW IS A BOW (chirper-zero, 19 Nov). Harry on the card oih-rod, "Which last note suits the returning
# riff?": "I can't hear the bow". He was right twice over. (1) WHAT PLAYED IT was the library's waterphone with its
# bow cut to 150 ms: at F4 one sine and one partial at 848 Hz (every other harmonic 60 dB down), flat from 150 ms
# to its end. Nothing in it is a bow: no stroke, no swell, no vibrato, no string. (2) WHERE IT PLAYED: under the outer
# guitars' chord it stood within 4 dB of the band in three third-octaves (315, 400, 800 Hz) and added 0.3 to 0.4 LU.
# NOW: (a) THE INSTRUMENT is a bowed string on a body, the engine's waveguide (stick and slip, the cello's
# string and box): at F4 its harmonics 2 to 7 stand -10 -12 -13 -15 -17 -19 dB under the first; each stroke starts
# 8 dB down and swells to its peak in 300 ms; vibrato 20 cents each way at 5.6 Hz from 150 ms in (measured on its
# fifth harmonic). Song-local patch `oih-bow`; the track is still `rod`. (b) THE NOTE CHANGES HANDS ALL THE WAY: v3
# took the inner pair of guitars off the delayed answer. On the two answers the bow has alone (3:17 and 3:19.5) the
# outer pair now lets go of it too: the bass and the kick keep the answer, the bow carries it, and the band comes
# back on the next beat (on the last one, the cadence). The six answers at 3:07-3:20 are now: pluck over two
# guitars, the same, pluck and bow over two guitars twice, then the bow alone twice.
# MEASURED (raw bench, 3:10.8-3:20.8; momentary loudness, the band's chords at -17 LUFS): the answer the bow has
# alone reads -20.6 then -19.0 where v15 (two guitars and the waterphone) read -19.3 then -19.0; the last C -20.9
# then -19.8 (v15 -19.8, -20.0): the bow carries what the guitars carried. Without the bow those holes read -22.4
# and -26.0. Under the pluck and the outer guitars the bow adds 0.9 to 1.5 LU (the waterphone 0.3 to 0.4) and stands
# within 4 dB of the band in five third-octaves. Tried and dropped: the bow an octave up (the engine's string jumps
# to its second mode there unless it has a violin's body, and the violin's first harmonic stood 18 dB over the
# band); a string with no body (thin: Harry on Still Owing's, "bow instr sounds not great"); a longer hold across the
# next chord (it added 1.8 LU on top of the full band).
# track gain ; the four bow notes' lengths in beats (the last ends at the cadence) ; 1 = the outer guitars give up
# the answers the bow has alone ; the swell in dB, ms to its peak, the string's level at rest in dB. '' = v15.
BOW = os.getenv('C10T11_BOW', '-6dB;1.75,1.75,1.75,1.2;1;8,300,-2' if SECOND and ROD else '')
# v17: THE STRING, NOT ITS HOOT (chirper-zero, 19 Nov, half an hour after v16, on v16's own stamped read). The read
# against the records caught what my bench had not asked: the stretch 3:00-3:20 went from +0.8 to +3.1 dB at
# 250-500 Hz, from four notes. The bowed string's first harmonic (349 Hz) stood 10 to 19 dB over its others (2 to 7:
# -10 -12 -13 -15 -17 -19), so most of what v16 added was one low tone: a hoot with a string behind it, and the same
# fault as the waterphone's in kind. A low shelf in the patch (-8 dB below 600 Hz) brings the string forward: at F4
# harmonics 2 to 7 now read -6 -5 -6 -8 -10 -12 (a bowed string's sawtooth, near enough), and the fader comes up 4 dB so
# the answer the bow has alone is as loud as it was (-20.6 then -19.1 LUFS momentary, raw bench; v16 -20.6, -19.0).
# Over the bench's ten seconds 250-500 Hz is +1.7 dB on v15 where v16 was +3.8; the last C sits 1.3 LU lower than at
# v16 (-21.1 before the cadence), which a swell into a cadence can afford. Tried: a high-pass at 500 Hz (the C, an
# octave under its corner, lost 2.6 LU) and at 700 (thin: the first four harmonics level).
# the shelf's corner in Hz ; its gain in dB ; the track's gain. '' = v16.
STRING = os.getenv('C10T11_STRING', '600;-8;-2dB' if BOW else '')
# v18 (chirper-one, section w3, 1:15-1:20): THE BROAD WALK AT DOUBLE SPEED, THEN AT HALF. The song's rule is that the
# riff never changes and the walk does. v13 walked each walk at half speed once; no walk had ever been walked faster.
# The first riff is two halves of twelve sixteenths (chord, clipped strokes, answer, twice). Walked in the broad four
# a cell is a bar. In the last two plain cells before v13's half-speed walk the drummer now takes the broad four at
# double speed: eight steps a cell, a dotted eighth each, the backbeat on every other one. So each HALF of the riff
# is a bar of four with its own two backbeats: kick with the chord on one, snare on two and four. Then at 1:20 the
# same walk at half speed makes a bar of two cells. In thirty seconds the one riff is heard under four steps a cell
# (1:00), the organ's six over them (1:10), eight (1:15), two (1:20), and then its bones. The drop from eight to
# two is the song's one double-time into half-time. Guitars, bass and kick are as written, as at 1:00.
# THE ORGAN TURNS WITH THE WALK. Under the four its upper note sighs from D flat to C once every four cells (two
# cells each, ten seconds: 0:50, 1:00). In the doubled cells it tells that sigh at double speed: D flat for one
# cell, C for the next (it used to hold C through both), so the turn into double time is heard in the harmony too,
# on the downbeat where the hands change.
# How many cells before the half-speed walk go at double speed ; 1 = the organ's sigh doubles too. Empty restores
# v17 byte for byte.
DOUBLE = os.getenv('C10T11_DOUBLE', '2;1' if STRING and ORGAN and PUMP else '')
# v19 (chirper-zero, instrument round): THE SNARE LOSES ITS BOX AND GETS ITS CRACK. Read alone at its own hits as
# tools/drumpunch.py reads a record's snare (six records' drum stems): its body (150-300 Hz) stood 5.0 dB OVER its
# crack (1.5-5 kHz), where five of the six records have it 0 to 4.4 UNDER (median -3.2; the sixth is The
# Faultless's fat snare, which the album's kit was once fitted toward), and its wires (5-12 kHz) 2.6 over the crack
# (records -0.6 to +1.4). In the mix the snare held the band from 250 to 500 Hz (54% of it in the quick six) and
# the kit stood 4.7 dB over the records' kits there and 2.7 under them from 4 to 8 kHz, where the whole mix read
# 1.8 to 3.4 under the records in every loud section. So the drum itself is retuned, in this song only: the kit's
# 5 dB of body at 200 Hz becomes a 2 dB cut, the stick's contact is shorter (0.6 -> 0.35: a harder, brighter
# stroke), more slap (1.2 -> 1.6), the wires a little tighter and voiced lower (0.85 -> 0.95, 7 kHz -> 5 kHz), so
# their hiss sits in the band that was empty and not above it (at 5.8 kHz the mix's 8-16 kHz rose 0.5 dB).
# AFTER, alone: body-crack +5.0 -> -3.4, wires-crack +2.6 -> -0.1, punch 13.2 -> 14.5 dB (records 13.8), each
# stroke as loud as it was (-25.0 -> -24.6 dB).
# the body's dB at 200 Hz ; the stick's contact ; slap ; the wires' tone Hz ; wires ; the loudness target (what
# plays without the snare keeps the gain it had). '' = v18.
SNARE = os.getenv('C10T11_SNARE', '-2;0.35;1.6;5000;0.95;-9.98' if DOUBLE else '')
# v20 (chirper-three, section w6, 2:30-2:40): THE KETTLE STAYS IN FOUR, AND THE DRUMMER FINDS THE STEP THAT HOLDS
# BOTH. The heavy riff comes back at 2:30 for four cells, walked in six for the first time. From 2:00 to 2:20 the
# kettle answered its D flat, F and C on the next BROAD footfall, with the drummer in four beside it. Now it comes
# back with the riff and lands where it always landed, though the drummer has gone to six: the F and the C fall
# where the two walks agree (the half cell and the cell's head), and the D flat falls between two quick steps. That
# one stroke is the whole difference between the walks, and it is heard alone.
# In the last two cells the drummer takes the quick six at double speed: twelve steps a cell, an eighth each, the
# step both walks are made of (chirper-one's v18 handoff named it). Each group of the heavy riff (two clipped
# strokes and a chord) becomes a bar of four eighths with its own two backbeats, and those backbeats (2 6 10 14
# 18 22) contain the broad walk's (6 and 18): the kettle's D flat is on a backbeat again. At 2:40 the broad walk
# is what is left, and the kettle's last C lands on its first footfall, as it did at 2:20.
# Guitars, bass and kick are as written. The kettle keeps to D flat, F and C: its first B flat is still the last
# note of the song.
# cells of the phrase's end walked in twelve ; cells of the phrase the kettle answers in, from its head ; dB on the
# kettle's strokes there ; the china's velocity in the twelve, times ; the loudness target ('' = unchanged).
# Empty restores v19 byte for byte.
TWELVE = os.getenv('C10T11_TWELVE', '2;4;0;1;-9.965' if SNARE and KETTLE else '')
# v21 (chirper-two, section w5, 1:46-2:13; the change is 1:47.5-1:50, the bridge's last cell): THE SECOND RIFF
# COMES IN BY ITS CLIPPED STROKES. The song's first riff was heard on skins before it was picked (v5, 0:02.5-0:10:
# "nothing invented for a fill"). The second riff, the heavier one, had no such door: at 1:50 the quiet bridge
# stopped and four guitars, bass and kit began at once, the biggest step in the song, with nothing before it. Its
# shape is two clipped strokes and a chord, three times a cell. So in the bridge's last cell:
#   - THE TOMS SAY ITS SIX CLIPPED STROKES, the three pairs that head its three groups, high tom, middle, floor,
#     each stroke harder than the last. The two toms that kept the broad count through the bridge (one on each
#     half cell) give way to them: two becomes three one cell before the drummer walks in three (1:50, v13);
#   - THE SECOND PAIR OF GUITARS COMES IN A HAND AT A TIME: the left one alone with the second pair of strokes
#     (1:48.3), the right one with it for the third (1:49.2), then all four at 1:50. (Harry, on this song's
#     guitars: "Let one come in early".) They play the riff's own clipped strokes on the open string and nothing
#     else; the chord, the bass and the kick still wait for 1:50;
#   - the last half second is left as it was: the clean guitar's leading note (v6) rings on after the last
#     stroke, and then the riff. The organ, the bass, the hat's six and the clean guitar are not touched.
# MEASURED (raw, seed 0; the cell in its three groups, K-weighted): the mix -24.4, -26.1, -27.6 before and -24.3,
# -24.2, -23.4 now, so the cell no longer dies away into the riff, it holds; the riff's first group is -20.3
# either way (4.1 dB over the bridge's cell heads, as it was). The toms stand 5.8, 1.5 and 2.6 dB under
# everything else; the guitars 7.0 under (the left alone, 10 dB to the left) and 4.1 under (both). The leading
# note stands 6.3 dB under everything else in its half second where it stood 4.7 (the floor tom's ring). The
# shoulder's first cell is within 0.01 dB of v20's.
# Rendered and not kept: the toms beginning a group earlier, on the last pair of the cell before (the walk in
# three then runs unbroken for four groups into the riff): the scorer's cost grows by half and the quiet cell
# before loses its ending. Not built in (reasoned, not rendered; `all` in the third field gives it): the riff's
# own last note (C) on the early guitars, which would sound over the leading note.
# groups of the second riff's clipped strokes the toms say before it (4 = from the last pair of the cell before;
# 3 = the last cell; 1 = its last pair only; 0 = none) ; the guitars that say them early, in the order they come
# in, the last with the last group ('' = none) ; `m` = clipped strokes only, `all` = and the riff's last note ;
# the toms' first and last velocity ; the loudness target ('' = unchanged). Empty restores v20 byte for byte.
TAIL = os.getenv('C10T11_TAIL', '3;wallL,wallR;m;0.42,0.86;' if TWELVE else '')
# v22 (chirper-alpha; section w8, 3:06-3:29, the one window nobody had worked; the change is 3:07.5-3:20, the last
# five cells of 'home', and one stroke at 3:20): THE STRIDE LENGTHENS UNTIL THE DOOR SHUTS. The riff never changes
# and the walk under it does: six quick steps to a cell or four broad ones, and each at half speed (three, two:
# v13). Home came back on four and stayed on four for all eight cells, then three chords. Now its last five cells
# are every walk the song has, in order of stride, a cell each: six (one last quick turn), four (with the crash,
# as written), three, two, one. Only the drummer's hands change (the ride on each step, the backbeat on every
# second step): the chords, the bass, the kick under them and the bow are as written. The walk of one step has its
# backbeat a whole cell later, which is the first of the three closing chords: the song's last snare falls there.
# The backbeat's gaps from 3:05, in sixteenths: 12, 10, 8, 8, 10, 12, 14, 28, 36, and the last is the chord.
# (The snare stroke a sixteenth before each of the bow's last three answers is among those that leave: the half
# second before each is 0.5 to 0.7 dB quieter; the bow as it enters stands where v17 left it.)
# the walks of home's last cells, steps a cell, one a cell, ending with its last ('' in the list = none) ; 1 = the
# one-step walk's backbeat falls on the first chord of 'shut' ; the loudness target ('' = unchanged). '' = v21.
STRIDE = os.getenv('C10T11_STRIDE', '6,4,3,2,1;1;' if TAIL else '')
# v23 (chirper-one, section w7, 2:40-3:06): THE ORGAN BREATHES THE OTHER WALK AT EACH CHANGE OF FEET. The song's first
# idea is that the reed organ is already in the second time while the band is in the first: at 0:40 it says the
# riff's four open notes on the four broad steps while the drummer walks six, and at 1:10 on the six quick steps
# while he walks four. It then leaves at 1:50 and is not heard again until the band has stopped. The swing is where
# the drummer changes feet cell by cell, and in its last six cells the guitars rest for the first half of five of
# them over one held double stop: five holes with a walk in them and nothing across it. Now the organ is back for
# those six cells (2:45-3:00) with the same sentence in the same register, always in the walk the drummer is NOT in
# (four steps over his six, six over his four), carried across the cell lines as it was at 1:10; the holes show it
# and the riff covers it, five times. It stops at home, where the bell and the bow answer.
# Where a guitar is sounding the riff's folded answer (C: every fourth cell the high fifth folds down to the second)
# the organ's D flat folds with it to C, the sigh it has had since 0:50: twice, at 2:50.4 in a hole, over the held
# B flat and C, and at 2:54.4 under the riff. Otherwise it would say D flat against a held C.
# the first cell of the swing it plays ; dB on its notes in the first of those cells and the last (a line between) ;
# the bellows pedal's depth on them, as at 0:40 ; the loudness target ('' = unchanged) ; 1 = the D flat folds to C
# where a guitar sounds C. '' = v22 byte for byte.
ACROSS = os.getenv('C10T11_ACROSS', '10;-1.5,1.5;0.25;;1' if STRIDE else '')
# v24 (chirper-alpha; whole song, 0:59.6-3:20): THE LONGER THE STEP, THE BIGGER THE ROOM. All that happens at 1:00 is a
# different backbeat, and a slower step leaves a longer wait between backbeats. That wait was empty: the snare is a
# crack of 40 ms. Now a backbeat that has longer to wait than the quick walk's (more than 8 sixteenths) is struck a
# second time into a hall that only its echo comes back from, and the hall is as long as the wait: 12 sixteenths
# (the broad four, 57 strokes), 16 (the walk in three, 8), 24 (the walk in two, 3), 36 or more (the stroke before the
# bridge, home's last two and the song's last, on the first closing chord: 4). The quick walk's get nothing. So the
# room opens at the hinge, opens and shuts with every change of feet in the swing, and grows as the stride lengthens
# until the door shuts. No note is touched: the copies are four tracks (far-N) into four buses (room-N); the snare
# track, its bus and everything else are v23's.
# What is heard is half a second of room, not a tail to the next backbeat (a full band covers that): raw, against
# everything else, the broad walk's room stands 3.0 dB under at 40-200 ms, 9.6 under at 200-600 ms, 23 under after.
# The return is cut below 800 Hz because the bow (Harry: "I can't hear the bow") and v23's organ live at 230-350 Hz:
# cut at 300 it took 2.4 dB off the bow in its own third-octave and 14 off one organ note; at 800 it takes nothing.
# the longest wait, in sixteenths, that gets no room ; the rooms, by the wait each one fills (a stroke goes to the
# first that is long enough, the last for anything longer) ; a room's decay, in waits ; the rooms' faders, dB, one
# each ; the kind of room ; the return's low cut (24 dB an octave) and high cut, Hz ; its predelay, ms ; the
# loudness target ('' = unchanged). '' = v23 byte for byte.
ROOM = os.getenv('C10T11_ROOM', '8;12,16,24,36;3;0,0,1,3.5;hall;800,6000;25;-9.83' if ACROSS else '')
# v25 (chirper-three; section round on w4, 1:20-1:46, the one window nobody had marked; the change is the bridge,
# 1:30-1:48.3): THE BOW SAYS THE RIFF ONCE, AS LONG AS THE BRIDGE. The song's law is that the riff never changes and
# the walk under it does; the walks have gone at half speed (v13), double (v18), in twelve (v20) and down to one step
# (v22). The riff itself had never been slowed. The bridge is eight cells and the riff is one, so the bow (four
# notes at the very end, until now) plays the first riff's four open notes EIGHT TIMES SLOWER, each at its own place:
# B flat at 1:30.0 (the chord at 0), D flat at 1:35.8 (the answer at 7), B flat at 1:40.0 (the chord at 12), F at
# 1:45.8 (the delayed answer at 19). Each is held until the riff's next clipped stroke, eight times later, stops it;
# the last of those falls at 1:48.33, which is where v21 brings the first guitar in on its clipped strokes. So the
# slow riff's last mute IS the guitar's entry. Over the bridge's four grounds the same four notes are root, fifth,
# fifth, root (B flat over B flat, D flat over G flat, B flat over E flat, F over F), and the two answers come in
# 0.83 s after their grounds, as they are late in the riff. Nothing else is touched: a track of its own, last.
# The bow's strokes here are 2.5 and 3.3 s long, not 0.7: the swell takes 1.2 s to its peak (the end's: 0.3), and
# the string is trimmed 5 cents down (it read 3 to 8 cents sharp; now within 3).
# MEASURED (raw, each note against everything else, K): -7.3, -9.7, -6.3, -9.7 dB; the organ's melody over the same
# stretches -6.6 to -5.4 (it was -5.6 to -4.9), the clean guitar -11.0 to -8.9 (-10.5 to -8.4). The bow's first
# harmonic stands 6 to 13 dB over what else is in its third-octave. The bridge is 0.4 to 0.5 dB louder; the target
# moves -9.83 -> -9.81 so that every stretch the bow does not sound in is within 0.006 dB of v24 on three seeds.
# THE SCORE FALLS (93.6 / 95.2 / 94.3 -> 92.3 / 94.4 / 91.7) and is kept on judgment: the recurrence term had been
# counting the quiet bridge as a return of the quiet opening (0:00-0:10), and with a bow in it the two match less
# (0.53 -> 0.50 on a ramp that starts at 0.45). It does not follow the bow's level (-13 dB: the same).
# how many times slower (the bridge is eight cells) ; the bow's register over the low string, semitones (the end's
# bow: 24) ; 'mute' = each note held until the riff's next clipped stroke, 'next' = until the next note ; its track's
# fader ; overrides on the bow for these long strokes ; the loudness target ('' = unchanged). '' = v24 byte for byte.
LONG = os.getenv('C10T11_LONG', '8;24;mute;-10dB;synth.env.swell.a=1200ms synth.env.swell.d=1500ms synth.pitch.value=-0.05;-9.81' if ROOM and BOW and ROD else '')
# v26 (chirper-two; instrument round: THE CYMBALS, the hand that keeps the walk). No stroke is added, moved or
# struck harder; the crash, the snare, the kick and the toms are as they were.
# The song's law is that the riff never changes and the walk under it does, and the walk is kept on metal: the
# closed hat from 0:10 to 1:50, the china from 1:50 to 3:00, the ride at home. Four notes in a row named the
# cymbals as the next instrument. Read alone and against everything else (raw, K, a stroke's first 60 ms):
#   THE HAT stood 14.4 to 14.9 dB under the band (the snare 0 to 3.6 over, the kick 0 to 2 under) and was 3% of
#       the mix's 4-8 kHz and 33 to 41% of its 8-16 kHz: the library's haake-hat is high-passed at 8 kHz, so it
#       had 5.3 dB LESS of itself at 4-8 kHz than at 8-16, and was 25 dB down 30 ms after the stick: a tick.
#   THE CHINA stood 11.0 to 11.4 under, 18 to 22% of the 4-8 kHz and 72 to 76% of the 8-16 kHz: as much at 8-16 as
#       at 4-8 (+0.4 dB).
#   THE RIDE stood 21.7 under: 28 strokes that keep the walk at home, and v22's lengthening stride, not heard.
#   THE RECORDS: their drum stems carry 4.7 to 7.4 dB more at 4-8 kHz than at 8-16 (median 5.9); this kit 3.1 to
#       4.7 (5.6 at home). The mix read 1.2 to 2.1 dB short at 4-8 kHz in every loud section but the swing (0.6),
#       and level or over at 8-16 kHz except at home (-2.8). By part the kit was 1.0 to 2.2 short at 4-8 kHz in
#       'broad', the shoulder and home; the guitars were level there. So the shortfall was the cymbals'.
# WHAT CHANGED.
#   THE HAT HAS A BODY: high-passed at 4 kHz, 60 ms long (45), a shelf of -8 dB over 8 kHz and +4 dB at 5.5 kHz,
#       fader 12 -> 15.5 dB. Alone: +9.0 dB at 4-8 kHz, -0.1 at 8-16; 3.8 dB MORE at 4-8 than at 8-16 now; its
#       centre 10.9 -> 6.6 kHz; 19.5 dB down after 30 ms. It stands 10.7 to 11.3 under the band. In the quiet
#       bridge its strokes carry -3.5 dB, so that it stands where it stood beside the organ and the bow (11.1; 11.3).
#   THE CHINA IS A LOWER, LOUDER PLATE: its peak 8 kHz +3 dB -> 5 kHz +6 dB, tilt 3 -> 0, bright 1 -> 0.6, its
#       2.2 kHz honk off, high-pass 1.2 -> 3 kHz, 3 dB up in the kit. Alone: +5.9 dB at 4-8 kHz, +4.8 at 2-4,
#       -0.3 at 8-16 (6.7 dB more at 4-8 than at 8-16 now; its centre 7.3 -> 5.6 kHz). It stands 7.6 and 8.1 under
#       the band in the shoulder. In the swing, where it is struck most often, each stroke carries -1.5 dB (9.3
#       under): at one level the kit read 1.7 dB over the records' kits at 4-8 kHz there and level at 1:50 (now
#       1.3 over there by part, and the mix +0.3).
#   THE RIDE IS HEARD: 9 dB up in the kit; it stands 12.9 under the band. Its tone is not touched.
# THE READ against the records' voiceless passages: all nine loud windows nearer (the mean of eight 0.885 -> 0.785;
# home 1.122 -> 0.867, the kettle 1.044 -> 0.922, the shoulder 0.722 -> 0.611, the swing 0.633 -> 0.533 and
# 0.833 -> 0.700). 4-8 kHz: quick -1.2 -> -0.8, broad -1.9 -> -1.7, the shoulder -1.5 -> -0.5, the kettle -2.1 ->
# -0.8, home -1.6 -> -1.1, the swing -0.6 -> +0.3 with its 8-16 kHz +1.3 -> +0.6. By part, the kit against the
# records' kits at 4-8 kHz: -1.0 -> -0.7 ('broad'), -1.6 -> 0.0 and +0.1 (the shoulder), -2.2 -> -1.3 (home);
# the kit's 4-8 minus 8-16 kHz: 5.5, 5.3, 4.6 (quick, lean, broad), 6.2, 5.9, 6.0 (the china's sections), 4.4 at
# home (the ride is a wash with its top on).
# COSTS: the kit's 2-4 kHz, already over the records' kits, is 0.4 to 0.5 further over where the china plays; the
# quiet bridge has 3 dB less above 8 kHz (the hat was all of it); the five seconds at double speed (1:15) read 0.03
# further; the swing is 0.06 dB louder and the twelve (2:35) 0.12 to 0.14. The bow's eight notes stand where they
# stood, to 0.1 dB.
# The target moves -9.81 -> -9.778 (slope 1.83, measured): the opening, which has no cymbal, is within 0.007 dB
# of v25 on three seeds.
# overrides on the closed hat (haake-hat) ; the hat's fader ; its eq, band|band ; a note gain on its strokes in the
# quiet bridge ; overrides on the china (the kit's x) ; the china's gain in the kit ; a note gain on its strokes in
# the swing (2:20-3:00, where it is struck most often) ; the ride edge's gain in the kit (rde) ; the loudness target
# ('' = unchanged). '' = v25 byte for byte.
CYMBALS = os.getenv('C10T11_CYMBALS', 'filters.0.cutoff.value=4k amp.d=60ms;15.5dB;highshelf cutoff=8000 gain=-8dB|peak cutoff=5500 q=0.8 gain=4dB;-3.5dB;'
                    'synth.filters.0.cutoff=3000 synth.filters.1.gain=0dB synth.filters.2.cutoff=5k synth.filters.2.gain=6dB synth.layers.0.tilt=0 synth.layers.0.bright=0.6;'
                    '-3.5dB;-1.5dB;0dB;-9.778' if LONG else '')
# v27 (chirper-three; instrument round: the two riff guitars' muted stroke, 702 of their 1182 notes; and A REPAIR OF MY
# OWN v25). No note changes.
# THE GUITARS. gl and gr were the album rig as it ships. Beside six records' strokes (riffpunch --strokes; quick verse,
# heavy riff, swing, home) the chug had NO TEETH (through a stroke, 1-4 kHz over 400 Hz-1 kHz: 5.0, 4.5, 4.8, 8.2 dB;
# the records 11.3, never under 6.5) and ITS LOW END DIED AFTER THE STROKE (100-250 Hz in the first 20 ms over 40-80
# ms: +1.66, +1.61, +2.70, -0.45; the records -1.1, never over +0.3). One control at a time on the heavy riff: the
# palm closing the string's filter two octaves, not 3.4, gives teeth and makes the fall worse (+2.16); the pick half
# as soft under the palm does NOTHING alone here (+1.76: on Still Owing it was the whole cure); together +0.72, and
# with the pick at 0.4 and the chest lifted +0.16. AFTER: the fall -0.64, -0.02, -0.80, -1.50; teeth 7.4, 7.4, 7.4, 7.6: every section
# inside the records' range on both, where three of four were outside on both. The brighter stroke read 0.96 dB
# louder alone (K) and the master turned the whole song down 0.5 dB for it, so the two faders give 1 dB back and the
# chest (190 Hz) is lifted to hold 120-250 Hz: alone the pair is level with v26 (K +0.06, 120-250 Hz 0.0) and the latch,
# where no guitar plays, is within 0.01 dB of v26 on seeds 0 and 1 (0.10 under on seed 11) with the target unmoved.
# THE MIX is where it was against the records' voiceless passages (0.752 -> 0.752: nearer in three stretches, further
# in three) and 0.05 further against all eleven (the guitars are 1 dB lower at 500 Hz-1 kHz, where the mix was short).
# Not kept: cancelling the bus's 720 Hz lift on these two (it fitted the pair alone and took 0.6 to 1.2 dB of the
# mix's 500 Hz-1 kHz in every stretch); the faders left up (the mix read nearer, 0.719, and every quiet passage came out 0.5 dB lower).
# COSTS: the stroke's punch in the swing and home 3.53, 3.51 -> 3.30, 3.39 (records 3.5 to 4.2); the noise between
# its harmonics 0.39 -> 0.30 in three sections (0.40); the scorer's spectrum term 0.4 lower on each seed (its worst
# band, 38 Hz, 10.1 -> 10.4 under; the pair has 4.3 dB less under 60 Hz, the likely reason, not separated).
# THE REPAIR. v25 trimmed the long bow 5 cents down because the bowed string 'read 3 to 8 cents sharp'. Most of that
# was not the string: a bowed layer has `vary` (a player's intonation, drawn by the seed), the patch does not set it,
# and I read ONE seed (chirper-zero, 20 Nov). The four notes alone, cents off the written note: as v25 left them,
# seed 0: -1.3 +2.8 +0.8 -0.7 (what I reported); seed 11: +0.4 -1.2 -0.6 +3.9; THE SONG'S OWN SEED, 1: -2.6 -3.2
# -4.3 -0.5, flat. With `vary` 0 and no trim: +0.8 +1.1 +1.1 +1.6 on every seed (the string's own share; the engine's
# `tune_sounding` for a bowed layer will take that when the pin moves). The D flat's level, which `vary` moved 3.5 dB
# between seeds, is now the same on each (2.8 dB lower than it was at the song's seed).
# overrides on the two riff guitars' rigs (gl, gr) ; an eq on each, band|band ('' = none) ; dB on their two faders
# ('' = as they were) ; what the long bow's patch takes in place of v25's pitch trim ('' = the long bow as it was) ;
# the loudness target ('' = unchanged). '' = v26 byte for byte.
PICK = os.getenv('C10T11_PICK', 'synth.layers.0.soft=expr.pm*0.4 synth.filters.0.cutoff.mod.0.amount=-2;peak cutoff=190 q=1.2 gain=6.5dB;-1;'
                 'synth.layers.0.vary=0;' if CYMBALS else '')


# v28 (chirper-two; section round on w2, 0:26-0:53, flagged static; the window worked is the hinge's own thirty
# seconds, 0:40-1:10, so it runs on into w3): THE DOOR IS AJAR. The song has two drummers (its first line: the quick
# drummer counts six, the broad drummer four) and a door between them: at 1:00 it swings and "all that happens is a
# different backbeat" (v24). The organ is already in the other time from 0:40. Now so is the other drummer, heard
# through the door. Through 'lean' the BROAD drummer's backbeat (the second and fourth of his four steps: sixteenths
# 6 and 18 of the cell, where no quick step falls) is struck WET ONLY into the room that backbeat will have after
# the hinge (v24's room-12): no stick, only the room, and through a door: a low-pass on what goes in, 1.2 kHz at
# 0:40.6 opening to the room's own 6 kHz by 0:59.4, as the strokes come up. At 1:00 the snare itself lands where
# its echo has been. Then the two change rooms: for four cells the QUICK drummer's backbeat (sixteenths 4, 12, 20)
# is heard the same way, dying away as the door closes (1:00.4-1:09.6), and at 1:10 the organ takes the six, as it
# always did. One new last track, `door`: 28 snare strokes into room-12; no other track, bus or note changes.
#   MEASURED (raw, K, the room's return against everything else in the 40-200 ms after each stroke; v24's own
#       room after the hinge reads -3.3 to -1.0 this way): BEFORE the hinge -16.1, -16.7, -14.6, -14.9, -13.5
#       (0:40.6-0:45.6), then -9.2 to -11.1 (to 0:50.6), -5.0 to -8.5 (to 0:58.1), and -2.5 on the last (0:59.4).
#       In the room's own band, 800 Hz-6 kHz: -10 rising to 0. AFTER the hinge: -7.5, -10.8, -11.4, -9.7, then
#       -14 falling to -25 by 1:09.6: an afterimage of a cell and a half, 4 dB or more under the new backbeat's room.
#   His second stroke of each cell in 'lean' carries 3 dB less: the band is thinner at three quarters of the cell
#       and the same stroke stood 4 to 5 dB further forward there.
#   FINISHED, three seeds: 0:50-1:00 +0.12 to +0.15 dB, 0:40-0:50 +0.03, 1:00-1:10 +0.04 to +0.05; every other
#       section 0.01 to 0.03 dB lower: the target is not moved. AGAINST THE RECORDS: 'lean' 1.122 -> 1.056 (their
#       mixes; 1-2 kHz -1.1 -> -0.8), 'broad' 1.178 -> 1.156; the other thirteen windows read as they did.
# cells of 'lean' the broad drummer is heard in through the door (from:to, from its head) ; dB on his first and his
# last stroke (a line between) ; the room he is in (one of v24's, by its wait in sixteenths) ; the track's fader ;
# the loudness target ('' = unchanged) ; the door: a low-pass on what goes into that room, Hz when it is least open
# and when it is widest (a straight line in octaves between; '' = no door, the room as v24 built it) ; dB on his
# second stroke of each cell (three quarters through, where the band is thinner) ; cells of 'broad' in which the
# quick drummer is still heard, from the hinge ('' = he is not) ; dB on his first and last stroke there.
# '' = v27 byte for byte.
AJAR = os.getenv('C10T11_AJAR', '0:8;-4,-1;12;0dB;;1200,6000;-3;0:4;-4,-14' if PICK and ROOM and SNARE else '')
# v29 (chirper-one; whole song from 1:48, on the one guitar rig nobody had read: the two WALL guitars, 235 and 231
# notes, 136 and 132 of them under the palm, through the heavy riff, the swing and home): THE WALLS KEEP THEIR LOW END
# TOO. v27 gave the riff pair its hard pick; the walls beside them were still the old stroke. Read alone beside six
# records' guitars at their own chugs (riffpunch --strokes, 1:55-2:15, 69 strokes): their low end died after a stroke
# (+2.25 dB; the records -1.1, none over +0.3) and they had few teeth (-8.7; the records -11.3). The wall rig has
# no soft pick (chirper-zero, Take Up the Slack v18): its fall is the palm's THUMP. Thump 0.5 -> 0.2 with the palm's
# filter at two octaves: fall -1.83, teeth -11.1, all five measures inside the records' ranges. (Thump 0 alone: fall
# -1.96 but teeth -9.0; thump 0 with the filter: fall -3.08, past the records' lowest.) The harder stroke takes the
# walls' chest (2.4 and 2.6 dB at 60-250 Hz alone) and 1.1 dB of their 500 Hz-1 kHz, where the mix is already short:
# lifts at 170 and 700 Hz give them back, and the faders come down so the walls alone are as loud.
# the tracks ; what is added to each one's patch ; bands on each track's eq after its cabinet, band|band ; dB on each
# fader ; the loudness target ('' = unchanged). '' = v28 byte for byte. On only while AJAR is.
WALLS = os.getenv('C10T11_WALLS', 'wallL,wallR;synth.layers.0.thump.mod.0.amount=0.2 synth.filters.0.cutoff.mod.0.amount=-2;peak cutoff=170 q=0.9 gain=3dB|peak cutoff=700 q=1 gain=1.5dB;-0.5;' if AJAR else '')
# v30 (chirper-zero; the draw was a whole-song round and I spent it on the one drum that plays in every section the
# band does and that nobody had read: the KICK, 332 strokes. No note changes; the fader is not moved). THE FOOT HAS A
# BEATER. Alone beside the six records' bass drums (tools/kickspec.py, shapes) the album kit's kick as it comes stood
# 7.54 away and its click read -28.1 where theirs read -12.5: a thud and a box (+9 to +14 dB at 250-630 Hz) with
# nothing on the front, though the track already lifted 4.5 kHz by 8 dB: there was nothing there to lift. The kick
# plays the riff's own accents (its first, fifth, eighth, thirteenth and eighteenth sixteenths), so the riff's low
# strokes had no edge either. The drum's beater is its third layer, a 4 ms burst of noise, 64 dB down as it comes:
# here it is 24 dB up, and a low-pass at 7 kHz follows the track's eq.
# WHAT THE MIX REFUSED, AND WHY IT IS THIS RUNG (all read stretch by stretch beside the records with nobody singing):
#   the beater at -34 dB with no low-pass (alone 3.65 with the drive down, the best read alone): every stretch
#     worse, ten stretches' sum 7.94 -> 10.46: the noise reaches 16 kHz and the mix's top octave went 2.4 dB over.
#   the drum's drive down (0.35 -> 0.1: the box out, alone 2 dB nearer): the mix lost 0.7 dB at 120-250 Hz where
#     the riff stretches are already short; the box is filling that band for the band. Left.
#   the drum's tick (its fourth layer, a 4.4 kHz triangle): alone WORSE (8.07): a spike. Left where it was.
#   the drum TUNED TO THE RIFF'S B FLAT (a semitone up, its wander out): the low end got LESS even, not more: at
#     the thirty kicks struck with the bass's B flat in 'quick' the 40-80 Hz level's spread stroke to stroke went
#     from 0.99 dB (SD; 3.4 from loudest to quietest) to 2.15 (6.4): on one note the drum and the string add or
#     cancel by their phase; a semitone apart they slide past each other inside every stroke. Left on its A.
#   with the low-pass: -44 dB sum 7.91, -40 dB 7.98, -36 dB (low-pass 6 kHz) 8.04, against 7.94: LEVEL. Four
#     stretches closer (lean, broad, kettle, home: 4-8 kHz was short there), two the same, four further (the swing
#     and the shoulder, where the china already fills it). Alone 5.77 / 5.39 / 5.03. THE MIX IS NEUTRAL; -40 is
#     kept on the drum's own read, and that is said in the note.
# what is added to the kick's patch ; bands added to its track's eq, band|band ; dB on its fader ; the loudness
# target ('' = unchanged). '' = v29 byte for byte. On only while WALLS is.
BEATER = os.getenv('C10T11_BEATER', 'kit.k.patch.synth.layers.2.level.value=-40dB;lp cutoff=7000 q=0.7;;-9.753' if WALLS else '')
# v31 (chirper-zero; section round, w6, 2:13-2:40: flagged static; the change is 2:30-2:40). THE WALK IS AN INTERVAL.
# (The notes are below, beside the switch's use in make().)
# semitones the wall pair's chords go up, phrase by phrase ; first cell of the swing ; cells in each phrase ; the
# loudness target ('' = unchanged). '' = v30 byte for byte. On only while BEATER is.
ABOVE = os.getenv('C10T11_ABOVE', '7,19;4;2,2;-9.759' if BEATER else '')
# v32 (chirper-zero; a whole-song draw spent on the bass, the last instrument of the band still as the album ships
# it; 352 notes, none moved): THE BASS SPEAKS UNDER THE FIRST RIFF. (The notes are below, beside the switch's use.)
# overrides on the bass's patch ; the beats that get them, from:to (to not included): those notes go to a last track
# of their own, and `bass` keeps the rest untouched ; that track's name ; the loudness target ('' = unchanged).
# '' = v31 byte for byte. On only while ABOVE is.
SPEAKS = os.getenv('C10T11_SPEAKS', 'fx.2.bands.3.cutoff=1150 fx.2.bands.3.q=1.2 fx.2.bands.3.gain=9dB fx.2.bands.1.gain=11dB '
                   'fx.2.bands.0.gain=9dB synth.layers.1.level=-12dB;0:210;bass-first;' if ABOVE else '')
# v33 (chirper-zero; section round on w1, 0:00-0:26, the window longest unworked (v5, 18 Nov); the change is 'latch',
# 0:00-0:10): THE DOOR OPENS AS IT SHUTS. chirper-alpha's v22 ends the song on every walk it has, in order of stride,
# a cell each (six, four, three, two, one, and the last backbeat is the latch), and his handoff named the same
# thought at the other end as not built: the song began on four cells with no walk at all. Now the walks arrive in
# those four cells in the reverse order: ONE step (a tick with the first bell note), TWO, THREE, FOUR, and the quick
# SIX is the band at 0:10, as written. Only the drummer's hands are new (walk(), as everywhere: the closed hat on
# each step, the backbeat on every second step): ten ticks and four backbeats. The bell, the toms' and the guitars'
# clipped strokes (v5) and everything from 0:10 are as written.
# AND THE ROOM COMES WITH IT, by v24's rule and v24's own code (the longer the step, the bigger the room): the new
# backbeats wait 20, 22, 12 and 10 sixteenths, so the first two are struck into the hall of the walk in two and the
# next two into the broad walk's; from 0:10 the quick walk is dry. The door opens on the big room and the room closes
# as the walk finds its feet; at the end it does the opposite.
# IT ARRIVES, it is not there: the backbeats come in at about a third of the band's stroke and rise (alone, K, 120 ms:
# -32.7, -29.6, -25.6, -29.3 dB; the band's first three -21.5, -24.1, -22.4), the ticks at 0.7 of the band's rising to
# it. Raw, the four cells read -30.9, -28.9, -28.1, -27.2 dB (K; they read -31.0, -29.1, -28.4, -27.9): the step up
# into the band at 0:10 is 4.1 dB where it was 4.8.
# the walks of the latch's cells, steps a cell, a cell each ('' in the list = none) ; the piece that keeps the steps ;
# the backbeats' velocity as a share of the band's walk, in the first cell and the last (a line between) ; the same
# for the ticks ; the loudness target ('' = unchanged). On only while SPEAKS is. '' = v32 byte for byte.
# (Backbeats at '0,0' are not struck: the ticks alone, and so no room.)
OPENS = os.getenv('C10T11_OPENS', '1,2,3,4;h;0.32,0.58;0.7,1;-9.7535' if SPEAKS else '')


def BOW_PATCH():
    swell,rise,rest=BOW.split(';')[3].split(',')
    return {'about':'chirper-zero: a bowed string for On Its Hinge (the engine\'s bowed waveguide on the cello\'s body). Each stroke starts soft and swells to its peak, '
                    'then eases; the vibrato comes in early because the notes are short. Not a library patch.',
            'synth':{**({'filters':['lowshelf cutoff=%g gain=%gdB'%tuple(float(v) for v in STRING.split(';')[:2])]} if STRING else {}),
                     'layers':[{'type':'bowed','body':0.8,'body_size':2.2,'bow_attack':'50ms','bow_pos':0.12,'bow_speed':0.55,'bright':0.5,'pressure':0.78,'rosin':0.2,'speak':0.6,
                                'level':{'value':f'{float(rest):g}dB','mod':[{'src':'env.swell','amount':float(swell)}]}}],
                     'env':{'swell':{'a':f'{float(rise):g}ms','d':'900ms','s':0.5,'r':'150ms'}},
                     'lfo':{'vib':{'wave':'sine','rate':'5.6hz','delay':'80ms','fade':'180ms','retrig':True}},
                     'pitch':{'value':0,'mod':[{'src':'lfo.vib','amount':0.2}]},
                     'amp':{'a':'25ms','d':'0s','s':1,'r':'160ms'}},
            'fx':['reverb kind=hall decay=1.8s mix=0.18'],'gain':'0dB'}
BROAD = CELL // 4
# Offset, duration, semitones, open power chord / single ringing note / palm mute.
# The two short strokes before the Db and the delayed F are the tell in both walks.
RIFF = [(0,3.55,0,'p'), (4,0.65,0,'m'), (5,0.65,0,'m'), (7,2.7,3,'n'),
        (11,0.68,0,'m'), (12,2.0,0,'p'), (15,0.72,0,'m'), (17,0.75,0,'m'),
        (19,2.55,7,'n'), (22,0.83,0,'m')]
LAST_ANSWER = max(t for t,_,_,kind in RIFF if kind=='n')
# In the heavier verse the answers arrive BEFORE the root, and hang over the
# drummer's next footfall. A different phrase, not the first riff cut or sped up.
LIFT = [(0,0.70,0,'m'), (2,0.70,0,'m'), (3,3.65,3,'p'), (8,0.65,0,'m'),
        (10,0.7,0,'m'), (11,3.8,7,'p'), (16,0.7,0,'m'), (18,1.1,0,'m'),
        (20,3.5,2,'n')]


def note(n):
    return PITCH[n%12] + str(n//12 - 1)


def chord(*ns):
    return ','.join(note(n) for n in ns)


def make():
    notes = defaultdict(list)
    marks = {}
    def put(tr, at, dur, p, v, mute=False):
        ev = dict(at=round(at/SUB, 5), len=round(dur/SUB, 5), pitch=note(p) if isinstance(p,int) else p, vel=round(v,3))
        if mute:
            ev['expr'] = {'pm': 1.0}
        notes[tr].append(ev)
    def drum(p, at, v):
        tr = {'k':'kick', 's':'snare', 'h':'hat', 'rde':'metal', 'x':'metal', 'c':'metal'}.get(p,'skins')
        put(tr, at, 4.5 if p in ('x','rde','c') else 1.2, p, v)
    def walk(start, period, bronze, back=True, soft=1.0, tick=1.0):
        for j,t in enumerate(range(0,CELL,period)):
            drum(bronze, start+t, ((.68 if j==0 else .52) if bronze=='h' else (.65 if j==0 else .54))*tick)
            if back and j%2==1:
                drum('s',start+t,(.98 if j==1 else .91)*soft)
    def answer(i,semi):
        # Every fourth cell its high fifth folds down to the major second instead.
        return 2 if i%4==3 and semi==7 else semi
    def strings(at, dur, midi, typ, vel, wide=False):
        pitch=chord(midi,midi+7) if typ=='p' else midi
        for tr in (('gl','gr','wallL','wallR') if wide else ('gl','gr')):
            put(tr, at, dur, pitch, vel, typ=='m')
    def reed(start,i,melody=False,top=None):
        if not ORGAN: return
        if melody:
            # The two answers from the riff, each granted half a cell to ring.
            for k,semi in enumerate((3,answer(i,7))):
                # After the heavy band stops, let the bass and harmonic speak
                # one broad step before the organ. Its second note is not delayed.
                wait = BROAD if PIVOT and i==0 and k==0 else 0
                put('bellows', start+k*CELL/2+wait, CELL/2-.5-wait, HOME+36+semi, .90)
        else:
            # F4 under Db5/C5: the upper bench makes the bellows motion less buried.
            put('bellows',start,CELL-.15,chord(HOME+31,HOME+36+(top if top is not None else 2 if i%4 in (2,3) else 3)),.78)
    def other_walk(start, cell, step):
        # Two cells = five seconds. The same four-note sentence fits twice at
        # four steps a cell, three times at six. Carry it across cell boundaries.
        tune = [s for _,_,s,k in RIFF if k!='m']
        steps = CELL//step
        for j in range(steps):
            pos = (cell*steps+j) % len(tune)
            put('bellows',start+j*step,step*(.80,.70,.52,.92)[pos],
                HOME+int(COUNTER)+tune[pos],(.89,.84,.78,.92)[pos])

    def swing_slow(i):
        return i<4 or 8<=i<10 or (12<=i<16 and i%2==0)
    across_at, across_db = [0], []
    def across(start, i, count, slow):
        # v23: the sentence of other_walk, in the walk the kit is not in, its place carried from cell to cell
        first = int(ACROSS.split(';')[0]); g0, g1 = (float(x) for x in ACROSS.split(';')[1].split(','))
        tune = [s for _,_,s,k in RIFF if k!='m']
        step = SUB if slow else BROAD
        lift = g0 + (g1-g0)*(i-first)/max(1, count-1-first)
        for j in range(CELL//step):
            pos = across_at[0] % len(tune); across_at[0] += 1
            put('bellows', start+j*step, step*(.80,.70,.52,.92)[pos], HOME+int(COUNTER)+tune[pos], (.89,.84,.78,.92)[pos])
            if lift:
                notes['bellows'][-1]['gain'] = f'{round(lift,2):g}dB'
            if tune[pos]==3:
                across_db.append(notes['bellows'][-1])

    def main_riff(start,i,lift=False,wide=False,lend=False,carry_out=False,count_in=False,bass_floor=None,plant=None,bare=0,quick_in=False):
        pattern = LIFT if lift else RIFF
        meet = CELL//2             # both walks hit 12: three quarters or two dotted quarters
        last = max(t for t,_,_,kind in pattern if kind=='n')
        if count_in:
            for foot in range(0,meet,4 if lift or quick_in else BROAD):
                drum('k',start+foot,.98 if not foot else .85)
        for pos,d,s,kind in pattern:
            t=pos
            if kind=='m' and (bare>1 or (bare and t>=meet)):
                continue  # the clipped stroke, with its bass note and its kick, is left out
            if count_in and t<meet:
                if lift and kind=='p' and t+d>meet:
                    d -= meet-t; t=meet   # untie the anticipation: keep the original release
                else:
                    continue
            m=HOME+answer(i,s); v=.87 if kind=='m' else .96
            if lend and kind!='m':
                if kind=='n':
                    continue  # C is now the drum's alone, at the following cell head.
                d=min(d,BROAD-t%BROAD-.25)  # release the chord just before the footfall
            if carry_out and t>=last:
                strings(start+t,d,m,kind,v)   # outside pair still finishes the old riff
                if t==last:
                    gate=CELL-t+meet-.20
                    put('wallL',start+t,gate,HOME+int(STAY),.94)
                    put('wallR',start+t,gate,m+int(STAY),.94)
            else:
                strings(start+t,d,m,kind,v,wide)
            if plant is not None and t>=meet:
                # One long note under the second half of the riff: the lowest
                # the bass goes under distortion, an octave-and-more of floor.
                if t==meet:
                    put('bass',start+t,CELL-meet-.3,plant,.93)
            elif kind!='m' or t in (4,15,16):
                # The first hint: the riff is unchanged over Gb. Its Db still
                # has a bass fifth; the guitar's F is now the major seventh.
                low = m if bass_floor is None else bass_floor + (7 if s==3 else 0)
                put('bass',start+t,d,low,.91,kind=='m')
            if pos in ((0,3,8,11,18) if lift else (0,4,7,12,17)):
                drum('k',start+t,.98 if kind!='m' or t==0 else .82)
            elif bare and kind=='n':
                # Its kick used to fall on the clipped stroke before it. With
                # that gone the foot goes to the late answer itself, as at home.
                drum('k',start+t,.98)
    start=0
    for section,count in FORM:
        marks[section]=start
        for i in range(count):
            a=start+CELL*i
            if section=='latch':
                for t,d,s,kind in RIFF:
                    if kind=='m': continue
                    put('latch',a+t,d*1.1,HOME+24+answer(i,s),.77)
                if PICKUP and i:
                    # Nothing invented for a fill: the two clipped strokes
                    # before Db, the single hits, and the later pair are all
                    # muted slots of the riff the band is about to play.
                    for t,d,_,kind in RIFF:
                        if kind!='m' or (i==1 and t>=CELL//2): continue
                        if i==count-1 or (i==count-2 and t<CELL//2):
                            put('gl',a+t,d,HOME,.84,True)
                            # The other amp catches the last three strokes. The
                            # full chord, the bass and the kick still wait for 0:10.
                            if i==count-1 and t>=CELL//2:
                                put('gr',a+t,d,HOME,.84,True)
                        else:
                            # High drum at the front of the phrase, low at the
                            # back; very last stroke is a pickup to the repeat.
                            piece = 't1' if t<CELL//2 else ('t2' if t==22 else 'ft')
                            drum(piece,a+t,(.32 if t in (4,15) else .23) + .16*(i-1))
                elif not PICKUP and i>=2:
                    for t,p in ((0,'t1'),(CELL//2,'ft')): drum(p,a+t,.60)
                if OPENS:
                    # v33: the walks arrive in order of stride, a cell each, before the quick six at 0:10
                    strides=[int(x) if x else 0 for x in OPENS.split(';')[0].split(',')]
                    if i<len(strides) and strides[i]:
                        line=lambda f:(lambda lo,hi:lo+(hi-lo)*i/max(1,count-1))(*(float(x) for x in OPENS.split(';')[f].split(',')))
                        walk(a,CELL//strides[i],OPENS.split(';')[1],back=line(2)>0,soft=line(2),tick=line(3))
            elif section=='shut':
                if i==0:
                    for t,s in ((0,3),(6,2),(12,0)):
                        dur = CELL+11.5 if t==12 else 5.3
                        strings(a+t,dur,HOME+s,'p',.96,True)
                        put('bass',a+t,dur,HOME+s,.94); drum('k',a+t,.9)
                    put('glass',a+12,CELL+11.5,HOME+31,.82); drum('c',a+12,.92)
                    if STRIDE and STRIDE.split(';')[1]=='1':
                        drum('s',a,.98)             # v22: the backbeat of the walk of one step
                    if BREATH and ORGAN:
                        # No new attack after the band's last one: the reeds
                        # start under the chord and are simply left sounding.
                        put('bellows',a+12,count*CELL-12.5,chord(HOME+31,HOME+36+3),.78)
                        trim,low,touch=(BREATH.split(';')+['',''])[:3]
                        if float(trim):
                            notes['bellows'][-1]['gain']=f'{float(trim):g}dB'
                        if KETTLE and low:
                            put('kettle',a+count*CELL,10,HOME+int(low),float(touch))
                            marks['close']=3
            elif section=='bellows':
                reed(a,i,True)
                # Two phrases on each ground: Bb, Gb, Eb, F. The upper F is
                # fifth, major seventh, ninth, then root; it never transposes.
                turn = 4*i//count
                floor = HOME + ((0,-4,-7,-5)[turn] if PIVOT else 0)
                # v21: the second riff's clipped strokes (three pairs, the heads of its three groups) on the toms
                # before it is picked, high to low; the two toms that kept the broad count give way to them.
                said = []
                if TAIL:
                    pairs = [(t,u) for (t,_,_,k),(u,_,_,k2) in zip(LIFT,LIFT[1:]) if k=='m' and k2=='m']
                    assert pairs==[(0,2),(8,10),(16,18)]
                    groups = int(TAIL.split(';')[0])
                    back = (count-1-i)*len(pairs)             # groups between this cell's end and the shoulder
                    said = [(g,pr) for g,pr in enumerate(pairs) if back+len(pairs)-g<=groups]
                for t in (0,12):
                    put('bass',a+t,9.5,floor+(0 if t==0 else 7),.76)
                    if not said or t<said[0][1][0]:
                        drum('ft' if t==0 else 't2',a+t,.57)
                if said:
                    v0,v1 = (float(x) for x in TAIL.split(';')[3].split(','))
                    for g,pr in said:
                        for k,t in enumerate(pr):
                            n = 2*(groups-(back+len(pairs)-g))+k          # 0 .. 2*groups-1 through the whole fill
                            drum(('t1','t2','ft')[g] if back==0 else 'ft',a+t,round(v0+(v1-v0)*n/(2*groups-1),3))
                    if i==count-1 and TAIL.split(';')[1]:
                        # the guitars come in a hand at a time: the last named with the last group, each one
                        # before it a group earlier (Harry on this song's guitars: "Let one come in early")
                        hands = TAIL.split(';')[1].split(',')
                        for h,name in enumerate(hands):
                            first = pairs[max(0,len(pairs)-len(hands)+h)][0]
                            for t,d,sm,k in LIFT:
                                if t>=first and (k=='m' or (TAIL.split(';')[2]=='all' and t>pairs[-1][1])):
                                    put(name,a+t,d,HOME+sm,.87 if k=='m' else .96,k=='m')
                if PIVOT:
                    put('glass',a,CELL-1,HOME+19,.80)
                    # Answer below the harmonic at the riff's original Db/F
                    # attacks. Only on the final F does the suspended Bb go to A.
                    for t,_,_,k in RIFF:
                        if k=='n':
                            inner = (15,12,8,12)[turn] - int(i==count-1 and t==LAST_ANSWER)
                            put('glass',a+t,min(5,CELL-t-.2),HOME+inner,.82)
                else:
                    for t,d,s,k in RIFF:
                        if k!='m': put('glass',a+t,d,HOME+24+answer(i,s),.76)
                if i>=count//2:
                    for t in range(0,CELL,4): drum('h',a+t,.46 if t else .6)
            elif section=='home':
                # The open attacks keep their original positions; the spaces between
                # are now holes, or a single muted pickup on alternate cells.
                for t,d,s,k in RIFF:
                    if k=='m' and not (i%2 and t in (4,5)): continue
                    m=HOME+answer(i,s); dur=d if k=='m' else min(5.5,CELL-t-.2)
                    # Keep the first quarter of the return as it was. For the
                    # high answer only, the outer guitars stay and the second
                    # pair give up their chord to a different kind of metal.
                    late = bool(ROD) and i>=count//4 and t==LAST_ANSWER
                    # v16: where the bow has the note to itself, the outer
                    # guitars let go of it too; the bass and the kick keep it.
                    alone = late and bool(BOW) and BOW.split(';')[2]=='1' and i>=3*count//4
                    if not alone: strings(a+t,dur,m,'m' if k=='m' else 'p',.94,not late)
                    if late:
                        if i<3*count//4:
                            # Same octave and touch as the note in 'latch'.
                            put('latch',a+t,d*1.1,m+24,.77)
                        if i>=count//2:
                            # Its bow swells an octave below the sounding
                            # harmonic; carry through the next downbeat, but
                            # lift early on the last C so the cadence is clear.
                            if BOW:
                                put('rod',a+t,float(BOW.split(';')[1].split(',')[i-count//2])*SUB,m+24,.88)
                            else:
                                put('rod',a+t,CELL-t+2 if i<count-1 else CELL-t-1.6,m+24,.88)
                    if k!='m': put('bass',a+t,dur,m,.94); drum('k',a+t,.98)
                # v22: in the last cells the stride lengthens a cell at a time
                strides = [int(x) for x in STRIDE.split(';')[0].split(',')] if STRIDE else []
                walk(a,CELL//strides[i-(count-len(strides))] if i>=count-len(strides) else 6,'rde')
                if i in (0,4): drum('c',a,.84)
            else:
                slow=section in ('broad','shoulder')
                if section=='swing':
                    slow = swing_slow(i)
                # v14: the quick phrase of two cells in the swing's second half
                again = bool(RETURN) and section=='swing' and i in (count//2+2,count//2+3)
                assert not again or (not slow and swing_slow(count//2+1) and swing_slow(count//2+4))
                lifted=section=='shoulder' or (section=='swing' and not slow and not again)
                reply = bool(KETTLE) and section=='shoulder' and i>=count//3
                # After the first two-cell broad statement, only the kit attacks
                # the new walk until its midpoint. Do not carry into 'home'.
                split = bool(STAY) and section=='swing'
                count_in = split and i>count//2 and slow!=swing_slow(i-1)
                carry_out = split and count//2<=i<count-1 and slow!=swing_slow(i+1)
                floor = HOME-4 if PIVOT and section=='quick' and count//3<=i<count//2 else None
                thin = 0
                if BONES and section=='broad':
                    back = count-1-i            # cells before the bridge
                    thin = 2 if back==0 or (back==1 and int(BONES)>=3) else int(back<int(BONES))
                plant = None
                if GROUND and split and slow and i>=count//2:
                    # 8-9, 12 and 14: the broad phrases among the last five
                    # changes. The first cell of each is planted at its half;
                    # a second cell walks the riff's rhythm on that ground.
                    heads = [k for k in range(count//2,count) if swing_slow(k) and not swing_slow(k-1)]
                    ground = HOME+int(GROUND.split(',')[max(n for n,k in enumerate(heads) if k<=i)])
                    if i in heads: plant = ground
                    else: floor = ground
                main_riff(a,i,lift=lifted,wide=section in ('shoulder','swing') and not again,lend=reply and i>=2*count//3,
                          carry_out=carry_out,count_in=count_in,bass_floor=floor,plant=plant,
                          bare=thin,quick_in=again)
                if thin==2 and i==count-1:
                    # Same octave and touch as the opening. It rings into the
                    # stops, and the bridge's clean F takes over from it.
                    for t,d,s,k in RIFF:
                        if k!='m': put('latch',a+t,d*1.1,HOME+24+answer(i,s),.77)
                if reply:
                    for t,_,s,k in LIFT:
                        if k=='m': continue
                        landing=(t//BROAD+1)*BROAD
                        put('kettle',a+landing,2.1 if k=='p' else 3.7,
                            HOME+answer(i,s)+int(KETTLE.split(';')[1]), .93 if k=='p' else .98)
                bronze = 'x' if section in ('shoulder','swing') and not again else 'h'
                steps = first = 0
                if HALFSPEED:
                    two,three = (int(x) for x in HALFSPEED.split(';'))
                    if section=='broad' and count-1-two<=i<count-1:
                        steps,first = 2,count-1-two
                    elif DOUBLE and section=='broad' and count-1-two-int(DOUBLE.split(';')[0])<=i<count-1-two:
                        steps,first = 8,count-1-two-int(DOUBLE.split(';')[0])
                    elif section=='shoulder' and i<three:
                        steps,first = 3,0
                phrase = TWELVE and section=='swing' and 4<=i<8     # v20: the first quick phrase of the swing
                if phrase:
                    assert lifted and not slow and swing_slow(3) and swing_slow(8)
                    fast,stay,trim,ring = TWELVE.split(';')[:4]
                    if i>=8-int(fast):
                        steps,first = 12,8-int(fast)
                    if i<4+int(stay):
                        for t,_,s,k in LIFT:
                            if k=='m': continue
                            put('kettle',a+(t//BROAD+1)*BROAD,2.1 if k=='p' else 3.7,
                                HOME+answer(i,s)+int(KETTLE.split(';')[1]), .93 if k=='p' else .98)
                            if float(trim): notes['kettle'][-1]['gain'] = f'{float(trim):g}dB'
                if steps:
                    hit = False
                    for j,t in enumerate(range(0,CELL,CELL//steps)):
                        bar = j%4==0 if steps in (8,12) else j==0   # at double speed each half of the riff is a bar
                        drum(bronze,a+t,(.68 if bar else .52) if bronze=='h' else (.65 if bar else .54)*(float(ring) if steps==12 else 1))
                        if (steps*(i-first)+j)%2:
                            drum('s',a+t,(.98 if j%4==1 else .91) if steps in (8,12) else .91 if hit else .98); hit = True
                else:
                    walk(a,6 if slow else 4,bronze)
                if ACROSS and COUNTER and ORGAN and section=='swing' and i>=int(ACROSS.split(';')[0]):
                    across(a,i,count,slow)
                if COUNTER and ORGAN and section=='lean' and i<2:
                    other_walk(a,i,BROAD)  # organ anticipates the four; drummer still plays six
                elif COUNTER and ORGAN and section=='broad' and 4<=i<6:
                    other_walk(a,i-4,SUB)  # keep one memory of the six after the kit changes
                elif steps==8 and DOUBLE.split(';')[1]=='1' and i<count-4: reed(a,i,top=2 if (i-first)%2 else 3)
                elif section=='lean' or (section=='broad' and i<count-4): reed(a,i)
                if section in ('quick','shoulder','swing') and i==0: drum('c',a,.88)
                if section=='broad' and i==count-1:
                    for t,p in ((18,'t1'),(20,'t2'),(22,'ft')):drum(p,a+t,.73)
        start+=count*CELL
    if EARLY:
        start_swing = marks['swing']
        calls = [(t,d,s) for t,d,s,k in RIFF if k=='n']
        first = calls[0][0]
        assert len(calls)==2 and calls[1][0]==first+CELL//2
        attacks = (first, BROAD, SUB, 0)  # late; broad foot; quick foot; downbeat
        assert all(swing_slow(i) for i in range(len(attacks))) and not swing_slow(len(attacks))
        pair = ('wallL','wallR')
        for i, attack in enumerate(attacks):
            if i==0: continue  # hear the whole riff once after the kettle's last C
            a = start_swing + CELL*i
            for tr in pair:
                notes[tr] = [n for n in notes[tr] if not a <= n['at']*SUB < a+CELL]
            for which,(old,d,semi) in enumerate(calls):
                head = which*(CELL//2)
                now, off = head+attack, old+d
                # The low fifth occupies the front of the same space. As one
                # player's answer opens, the other player's chord closes.
                if attack:
                    put(pair[1-which],a+head,attack-.28,chord(HOME,HOME+7),.91)
                put(pair[which],a+now,off-now,HOME+int(EARLY)+answer(i,semi),.96)
                stop,gate,_,_ = next(n for n in RIFF if n[0]>=off and n[3]=='m')
                put(pair[which],a+stop,gate,HOME,.84,True)  # catch the ring on the original clipped stroke
                # The facing amp and bass keep the old attack: the high voice
                # starts alone, the octave joins late, and they release together.
                same_side = ('gl','gr')[which]
                notes[same_side] = [n for n in notes[same_side] if n['at']*SUB!=a+old]
        # The fourth answer is C, not F. The same hand takes it up one fret
        # to the first Db of the quick riff, then rejoins the low guitars.
        turn = start_swing + len(attacks)*CELL
        landing,gate,semi,_ = next(n for n in LIFT if n[3]=='p')
        notes['wallR'] = [n for n in notes['wallR'] if not turn <= n['at']*SUB <= turn+landing]
        put('wallR',turn+landing,gate,HOME+int(EARLY)+semi,.96)
    if HALF:
        # Last four cells of the quick verse (0:30-0:40). First the right hand
        # only trades the two answers; then it plays the whole riff starting
        # at the half cell, where both walks agree; then the left hand does.
        # The fourth cell, with its C, is the written unison again. Bass and
        # kick stay with the written riff throughout.
        quick, half = marks['quick'], CELL//2
        for i,(tr,turned) in zip(range(8,11), (('gr',False),('gr',True),('gl',True))):
            a = quick + CELL*i
            assert answer(i,7)==7 and not swing_slow(4)
            written = [n for n in notes[tr] if a <= n['at']*SUB < a+CELL]
            assert len(written)==len(RIFF)
            notes[tr] = [n for n in notes[tr] if n not in written]
            for pos,d,semi,kind in RIFF:
                if turned:
                    at = (pos+half) % CELL
                else:
                    at = pos
                    if kind=='n':
                        # Same place and gate, the other half's pitch.
                        semi = next(s for t,_,s,k in RIFF if k=='n' and t==(pos+half)%CELL)
                m = HOME+semi+(int(HALF) if kind=='n' else 0)
                put(tr,a+at,d,chord(m,m+7) if kind=='p' else m,.87 if kind=='m' else .96,kind=='m')
    # The control comparison for the hinge: all non-drum attacks, pitches, gates,
    # velocities and expressions repeat exactly. Drums are counted independently.
    hinge=marks['broad']/SUB; span=4*CELL/SUB
    def window(tr,a,b):return [dict(e,at=round(e['at']-a,5)) for e in notes[tr] if a<=e['at']<b]
    if ACROSS and ACROSS.split(';')[4:] and ACROSS.split(';')[4]=='1':
        for ev in across_db:                    # v23: the organ's D flat folds to C where a guitar is sounding C
            if any(n['at'] < ev['at']+ev['len'] and ev['at'] < n['at']+n['len'] and any(x[:-1]=='C' for x in str(n['pitch']).split(','))
                   for g in ('gl','gr','wallL','wallR') for n in notes[g]):
                ev['pitch'] = note(HOME+int(COUNTER)+2)
    for tr in ['gl','gr','wallL','wallR','latch','glass','bass','bellows','kick']:
        assert window(tr,hinge-span,hinge)==window(tr,hinge,hinge+span),tr
    assert [len(window('hat',a,a+span)) for a in (hinge-span,hinge)]==[24,16]
    assert [len(window('snare',a,a+span)) for a in (hinge-span,hinge)]==[12,8]
    SECOND_PATCH=(' fx.3.mix=0'+''.join(f' fx.4.bands.{i}.gain=0dB' for i in range(4))) if SECOND else ''
    SECOND_GAIN=(SECOND.split(';')[3]+'dB') if SECOND else '-3dB'
    def second_fx(right):
        if not SECOND:return None
        mic,cones,dist=SECOND.split(';')[:3]
        return [{'type':'cab','model':'4x12-modern','mic':float(mic),'distance':float(dist),'cone':int(cones.split(',')[right])}]
    def tr(name,patch,gain,pan=0,out=None,fx=None):
        d={'name':name,'patch':patch,'gain':gain,'pan':pan,'notes':sorted(notes[name],key=lambda n:n['at'])}
        if out:d['out']=out
        if fx:d['fx']=fx
        return d
    # The twin pair supplies the pick; the second pair joins after the exposed
    # bellows, on a wider-bodied amp. Both play actual rests. Since v15 both
    # pairs go through the engine's cabinet (SECOND).
    SNARE_PATCH = (' kit.s.patch.synth.filters.1.gain={}dB kit.s.patch.synth.layers.0.contact={} kit.s.patch.synth.layers.0.slap={}'
                   ' kit.s.patch.synth.layers.0.wire_tone={} kit.s.patch.synth.layers.0.wires={}').format(*SNARE.split(';')[:5]) if SNARE else ''
    tracks=[tr('gl','ct-twin fx.1.model=gojira fx.2.cone=81','0.5dB',-1,'gtrs'),
            tr('gr','ct-twin fx.1.model=gojira fx.2.cone=82','0.5dB',1,'gtrs'),
            tr('wallL','ct-wall-stop-l'+SECOND_PATCH,SECOND_GAIN,-.72,'gtrs',second_fx(0)),tr('wallR','ct-wall-stop-r'+SECOND_PATCH,SECOND_GAIN,.72,'gtrs',second_fx(1)),
            tr('latch','ct-bell','6.5dB',0),tr('glass','ct-bell','-1.5dB',-.20),
            tr('bass','ct-bass','0.7dB',0,'low'),tr('kick','ct-kit','2dB',0,'drums',[{'type':'eq','bands':['peak cutoff=4500 q=0.8 gain=8dB']}]),
            tr('snare','ct-kit'+SNARE_PATCH,'3dB',0,'drums'),tr('hat','ct-kit','12dB',-.28,'drums'),
            tr('metal','ct-kit','-4dB',.25,'drums'),tr('skins','ct-kit','3dB',0,'drums')]
    if PIVOT:
        # A long harmonic is much quieter than the old picked figure. Lift it
        # in the bridge only; the same guitar's final F stays at its old gain.
        glass = next(t for t in tracks if t['name']=='glass')
        glass['gain'] = {'value':glass['gain'],'mod':[{'src':'auto.pivot','amount':1}]}
        end = marks['shoulder']/SUB
        glass['auto'] = {'pivot':{'curve':0,'points':[['0b',float(PIVOT)],
                          [f'{end:g}b',float(PIVOT)],[f'{end+1:g}b',0]]}}
    if ORGAN:
        pump=[{'type':'pump','every':'3/8','attack':'12ms','hold':'28ms','release':'395ms','depth':PUMP,'curve':0.65}] if PUMP else []
        organ = tr('bellows','harmonium',ORGAN,.12,fx=pump)
        if COUNTER and pump:
            # The fingers make these attacks. Leave only a little of the deep
            # pedal duck on them; full bellows depth returns for the held dyads.
            wet=[['0b',1.0]]
            for tick in (marks['lean'], marks['broad']+4*CELL):
                b0,b1=tick/SUB,(tick+2*CELL)/SUB
                wet += [[f'{b0:g}b',1.0],[f'{b0+.01:g}b',.25],
                        [f'{b1-.01:g}b',.25],[f'{b1:g}b',1.0]]
            if ACROSS:
                b0,b1=(marks['swing']+int(ACROSS.split(';')[0])*CELL)/SUB,marks['home']/SUB
                wet += [[f'{b0:g}b',1.0],[f'{b0+.01:g}b',float(ACROSS.split(';')[2])],
                        [f'{b1-.01:g}b',float(ACROSS.split(';')[2])],[f'{b1:g}b',1.0]]
            pump[0]['mix']={'value':0,'mod':[{'src':'auto.hand','amount':1}]}
            organ['auto']={'hand':{'points':wet,'curve':0}}
        tracks.append(organ)
    if KETTLE:
        tracks.append(tr('kettle','timpani fx.0.mix=0.07 synth.amp.r=240ms',KETTLE.split(';')[0],-.15))
    if ROD:
        # Shorter bow and smaller water movement than the ambient patch: the
        # dissonant upper partials carry the sound, not a detuned six-second hall.
        if BOW:
            tracks.append(tr('rod','oih-bow',STRING.split(';')[2] if STRING else BOW.split(';')[0],-.15))
        else:
            tracks.append(tr('rod','waterphone synth.amp.a=150ms synth.amp.r=135ms synth.pitch.mod.0.amount=0.12 synth.pitch.mod.1.amount=0.18 fx.0.decay=0.8s fx.0.mix=0.09',ROD,-.15))
    doc={'about':'On Its Hinge — chirpers, Common Time, track eleven. A twelve-eighth riff in B flat; the drummer swaps six quick steps for four broad ones, on an unchanged riff. The reed organ breathes the broad walk before the kit takes it.' + (' The kettledrum answers the heavy riff on the next broad steps, then takes its last C.' if KETTLE else ''),
         'tempo':BPM,'seed':1,'length':f'{start//SUB+marks.pop("close",0)}b','tail':'4s','ceiling':'-1dB','loudness':float(STRIDE.split(';')[2]) if STRIDE and STRIDE.split(';')[2] else float(TAIL.split(';')[4]) if TAIL and TAIL.split(';')[4] else float(TWELVE.split(';')[4]) if TWELVE and TWELVE.split(';')[4] else float(SNARE.split(';')[5]) if SNARE else -10,'event_stable':True,
         'buses':{'drums':{'fx':['reverb kind=room decay=0.62s mix=0.13 predelay=7ms',{'type':'glue','threshold':'-22dB','ratio':2.5,'attack':'20ms','release':'135ms'},'clip drive=0dB ceiling=-13dB',{'type':'eq','bands':['peak cutoff=400 q=0.8 gain=-5dB','highshelf cutoff=9000 gain=-2dB']}]},
                  'gtrs':{'fx':[{'type':'eq','bands':['peak cutoff=350 q=1 gain=-2dB','peak cutoff=720 q=0.9 gain=2dB']},'reverb kind=room decay=0.35s mix=0.06 predelay=6ms']},
                  'low':{'fx':[{'type':'eq','bands':['peak cutoff=58 q=1.5 gain=-6dB','peak cutoff=116 q=1 gain=5dB','peak cutoff=350 q=1 gain=-6dB','peak cutoff=1500 q=1 gain=3dB']},{'type':'compressor','threshold':'-26dB','ratio':6,'attack':'12ms','release':'120ms','makeup':'2dB'}]}},
         'master':{'fx':[{'type':'eq','bands':['hp cutoff=24']},'gain gain=2.7dB']},'tracks':tracks}
    if BOW and ROD:
        doc['patches']={'oih-bow':BOW_PATCH()}
    if ROOM:
        # v24: a copy of each backbeat that waits longer than the quick walk's goes, wet only, into the room that is
        # as long as its wait (the first listed that is long enough; the longest for anything longer).
        dry,waits,scale,faders,kind,cuts,pre,target=ROOM.split(';')
        waits=[int(x) for x in waits.split(',')]
        faders=dict(zip(waits,faders.split(',')))
        strokes=sorted(notes['snare'],key=lambda n:n['at'])
        end=start/SUB
        for n,nxt in zip(strokes,[m['at'] for m in strokes[1:]]+[end+CELL]):
            wait=(nxt-n['at'])*SUB
            if wait>float(dry)+1e-6:
                notes[f"far-{next((w for w in waits if w>=wait-1e-6),waits[-1])}"].append(dict(n))
        lo,hi=cuts.split(',')
        for w in waits:
            if notes[f'far-{w}']:
                tracks.append(tr(f'far-{w}','ct-kit'+SNARE_PATCH,faders[w]+'dB',0,f'room-{w}'))
                doc['buses'][f'room-{w}']={'fx':[f'reverb kind={kind} decay={w/SUB*60/BPM*float(scale):.4g}s mix=1 predelay={pre}ms high_cut={hi} width=1',
                                                 {'type':'eq','bands':[f'hp cutoff={lo}',f'hp cutoff={lo}']}]}
        if target:
            doc['loudness']=float(target)
    if LONG:
        # v25: the first riff's four open notes, each at its own place in the cell times `slow`, each held until the
        # riff's next clipped stroke (times `slow`) stops it. A track of its own, last, so that no other part moves.
        slow,up,hold,fader,over,target=LONG.split(';')
        slow=int(slow); a=marks['bellows']
        assert slow*CELL<=dict(FORM)['bellows']*CELL and hold in ('mute','next')
        opens=[t for t,_,_,kind in RIFF if kind!='m']
        for t,_,semi,kind in RIFF:
            if kind!='m':
                catch=next(u for u,_,_,k in RIFF if u>t and k=='m')
                until=catch if hold=='mute' or t==opens[-1] else next(u for u in opens if u>t)-.25
                put('longbow',a+slow*t,slow*(until-t),HOME+int(up)+semi,.88)
        tracks.append(tr('longbow','oih-bow'+(' '+over if over else ''),fader,-.15))
        if target:
            doc['loudness']=float(target)
    if CYMBALS:
        # v26: the same strokes on the same three cymbals; only how each one sounds, and how loud it is, changes.
        hat,hat_fader,hat_eq,bridge,china,china_gain,china_swing,ride_gain,target=CYMBALS.split(';')
        h=next(t for t in tracks if t['name']=='hat'); m=next(t for t in tracks if t['name']=='metal')
        assert h['patch']=='ct-kit' and m['patch']=='ct-kit' and 'fx' not in h and 'fx' not in m
        if hat:      # the kit's h is the library's haake-hat by name: a kit of this song's own gives it its overrides
            doc.setdefault('patches',{})['oih-kit']={'extends':'ct-kit','kit':{'h':{'patch':'haake-hat '+hat,'gain':'-10dB','choke':'hat'}}}
            h['patch']='oih-kit'
        if hat_fader: h['gain']=hat_fader
        if hat_eq: h['fx']=[{'type':'eq','bands':hat_eq.split('|')}]
        if bridge:   # the quiet bridge keeps the hat where it stood against the organ, the clean guitar and the bow
            a=marks['bellows']/SUB; b=a+dict(FORM)['bellows']*CELL/SUB
            for n in h['notes']:
                if a<=n['at']<b: n['gain']=bridge
        if china_swing:   # the swing strikes the china most often: each stroke a little less, so the plate stands where it does at 1:50
            a=marks['swing']/SUB; b=a+dict(FORM)['swing']*CELL/SUB
            for n in m['notes']:
                if n['pitch']=='x' and a<=n['at']<b: n['gain']=china_swing
        over=['kit.x.patch.'+o for o in china.split()]+([f'kit.x.gain={china_gain}'] if china_gain else [])+([f'kit.rde.gain={ride_gain}'] if ride_gain else [])
        if over: m['patch']=' '.join([m['patch']]+over)
        if target:
            doc['loudness']=float(target)
    if PICK:
        # v27: no note changes. The two riff guitars' rigs, and the long bow's intonation.
        over,eq,fader,bow,target=PICK.split(';')
        for t in tracks:
            if t['name'] in ('gl','gr'):
                assert 'fx' not in t
                if over: t['patch']+=' '+over
                if eq: t['fx']=[{'type':'eq','bands':eq.split('|')}]
                if fader: t['gain']=f"{float(t['gain'][:-2])+float(fader):g}dB"
            if t['name']=='longbow' and bow:
                t['patch']=' '.join([x for x in t['patch'].split() if not x.startswith('synth.pitch.value=')]+[bow])
        if target:
            doc['loudness']=float(target)
    if AJAR:
        # v28: through 'lean' the broad drummer's backbeat (the second and fourth of his four steps) is struck, wet only,
        # into the room that backbeat will have after the hinge: the other walk heard through a door that is opening.
        # After the hinge the quick drummer's backbeat (his second, fourth and sixth steps) is heard the same way, dying
        # away as the door closes: at the hinge the two drummers change rooms.
        import math
        cells,ramp,room,fader,target,shut,second,later,fade=AJAR.split(';')
        assert f'room-{room}' in doc['buses']
        near=lambda a: sorted((n for n in notes['snare'] if a/SUB<=n['at']<(a+CELL)/SUB),key=lambda n:n['at'])
        quick,broad=near(marks['broad']-CELL),near(marks['broad'])                # the two backbeats, either side of the hinge
        assert [round(n['at']*SUB-marks['broad']+CELL) for n in quick]==[CELL//6,CELL//2,5*CELL//6] and [round(n['at']*SUB-marks['broad']) for n in broad]==[CELL//4,3*CELL//4]
        lanes=[]
        for span,sect,model,(g0,g1),trim in ((cells,'lean',broad,[float(x) for x in ramp.split(',')],float(second or 0)),)+(((later,'broad',quick,[float(x) for x in fade.split(',')],0.0),) if later else ()):
            c0,c1=(int(x) for x in span.split(':'))
            assert 0<=c0<c1<=dict(FORM)[sect]
            places=[round(n['at']*SUB)%CELL for n in model]
            hits=[(marks[sect]+c*CELL+q)/SUB for c in range(c0,c1) for q in places]
            assert not any(abs(n['at']-t)<1e-6 for n in notes['snare'] for t in hits), 'the near drummer does not strike there'
            for i,t in enumerate(hits):
                g=g0+(g1-g0)*i/max(1,len(hits)-1)+(trim if i%len(places)==1 else 0)
                notes['door'].append({'at':round(t,4),'len':model[i%len(places)]['len'],'pitch':'s','vel':model[i%len(places)]['vel'],**({'gain':f'{g:.3g}dB'} if abs(g)>1e-9 else {})})
            lanes+=[[f'{hits[0]:g}b',0 if sect=='lean' else 1],[f'{hits[-1]:g}b',1 if sect=='lean' else 0]]
        tracks.append(tr('door','ct-kit'+SNARE_PATCH,fader,0,f'room-{room}'))
        if shut:
            f0,f1=(float(x) for x in shut.split(','))
            tracks[-1]['fx']=[{'type':'eq','bands':[{'kind':'lp','cutoff':{'value':f0,'mod':[{'src':'auto.open','amount':round(math.log2(f1/f0),4)}]},'q':0.7}]}]
            tracks[-1]['auto']={'open':{'points':lanes,'curve':0}}
        if target:
            doc['loudness']=float(target)
    if WALLS:
        # v29: the two wall guitars' muted stroke, on the wall rig's own controls (see WALLS).
        names,over,bands,fader,target=WALLS.split(';')
        for name in names.split(','):
            t=next(t for t in doc['tracks'] if t['name']==name)
            assert t['patch'].startswith('ct-wall') and isinstance(t['gain'],str),(name,t['patch'],t['gain'])
            if over: t['patch']=t['patch']+' '+over
            if bands: t['fx']=list(t.get('fx') or [])+[{'type':'eq','bands':bands.split('|')}]
            if fader: t['gain']=f"{float(t['gain'][:-2])+float(fader):g}dB"
        if target:
            doc['loudness']=float(target)
    if BEATER:
        # v30: the kick's beater, band-limited (see BEATER).
        over,bands,fader,target=BEATER.split(';')
        t=next(t for t in doc['tracks'] if t['name']=='kick')
        assert t['patch']=='ct-kit' and isinstance(t['gain'],str) and len(t.get('fx') or [])==1 and t['fx'][0]['type']=='eq',(t['patch'],t['gain'],t.get('fx'))
        if over: t['patch']=t['patch']+' '+over
        if bands: t['fx']=[{'type':'eq','bands':list(t['fx'][0]['bands'])+bands.split('|')}]
        if fader: t['gain']=f"{float(t['gain'][:-2])+float(fader):g}dB"
        if target:
            doc['loudness']=float(target)
    if ABOVE:
        # v31: THE WALK IS AN INTERVAL. The riff never changes and the walk does: four steps to the cell, or six, and
        # from 2:35 twelve (v20). Six steps against four is three against two, and three against two is a fifth;
        # twelve against four is three against one, a twelfth (an octave and a fifth): the walks stand to each other
        # as the riff's own B flat stands to its F. From 2:30, where the heavy riff is walked in six for the first
        # time, the wall pair plays the riff's chords a fifth above the twin pair for the two cells of the six, and
        # a twelfth above for the two cells of the twelve; at 2:40 the broad four is what is left and the pair is
        # back on the riff. (v8 had already sent its answers up an octave over the three broad phrases before, and
        # an octave is the same walk.) The twin pair, the bass and the kick keep the riff as written; the wall
        # pair's clipped strokes stay on the low string; v8's D flat 3 at 2:30.3 is not touched. 23 chords re-voiced;
        # no note is added, dropped or moved in time.
        semis,first,cells,target=ABOVE.split(';')
        a0=(marks['swing']+int(first)*CELL)/SUB
        def up(pitch,semi):
            m=PITCH.index(pitch[:-1])+12*(int(pitch[-1])+1)+semi; return f'{PITCH[m%12]}{m//12-1}'
        for semi,n_cells in zip((int(x) for x in semis.split(',')),(int(x) for x in cells.split(','))):
            a1=a0+n_cells*CELL/SUB
            for name in ('wallL','wallR'):
                t=next(t for t in doc['tracks'] if t['name']==name)
                for n in t['notes']:
                    low=min(PITCH.index(q[:-1])+12*(int(q[-1])+1) for q in n['pitch'].split(','))<48   # not v8's D flat 3
                    if a0<=n['at']<a1 and not (n.get('expr') or {}).get('pm') and low:
                        n['pitch']=','.join(up(q,semi) for q in n['pitch'].split(','))
            a0=a1
        if target:
            doc['loudness']=float(target)
    if SPEAKS:
        # v32: THE BASS SPEAKS UNDER THE FIRST RIFF. The guitars (v27, v29), the snare (v19), the cymbals (v26) and
        # the kick (v30) have each been read beside the records' own and fitted; the bass was the album's as it
        # ships. Alone beside eleven records' basses (tools/bassspec.py) it read 6.1 to 6.9 dB out: a sub (50-63 Hz
        # +8 to +11), a box (315-630 Hz +5 to +9) and no string (1-1.25 kHz 8 and 12 short).
        # WHO HOLDS WHAT WAS READ BY MUTING (in 'lean'): the bass gives the mix 1.6 dB under 60 Hz (the kick 7.4),
        # 4.9 at 60-120, 3.2 at 120-250 and 0.2 at most above that; the mix's excess at 250 Hz-1 kHz there is the
        # organ's (3.6, 3.1), not the bass's. So the cure the other songs' basses took (the box cut out) is REFUSED
        # HERE BY THE MIX: with the box 6 dB down the bass read 4.2 to 5.4 alone and the five band stretches read
        # 0.33 FURTHER from the records in sum. What both reads accept, and the mix chose the amounts of:
        #   the patch's 220 Hz band +8 -> +11 dB and its 110 Hz band +6 -> +9 (under the first riff the mix was 1.1
        #   to 1.4 short at 120-250 Hz, and the bass is what holds that band);
        #   the sine under the string 3 dB lower (the root is B flat at 58 Hz: the string has a fundamental of its
        #   own there, and under 60 Hz the mix stood 1.1 to 1.7 over);
        #   its upper band moved from 900 Hz to a grind at 1150 Hz, +9 dB: the string's own noise, where a record's
        #   bass has it (13 dB, or the shelf above it opened, read better alone and worse in the mix: it stops at 9).
        # ONLY UNDER THE FIRST RIFF (0:10-1:27.5: 'quick', 'lean', 'broad'), where two guitars are all that is over
        # it. The bridge's walk (B flat, G flat, E flat, F under the organ) lost 1.4 dB of floor with this voice in
        # the first bench, because its lowest notes ARE the sine. The rest of the song was then given it and read in
        # all fifteen stamp windows: those three passages came 0.11 to 0.14 closer to the records and six later ones
        # went further (the wall pair arrives at 1:50 with a low end of its own, so 120-250 Hz went over; 'bones'
        # and 'shut' lost too).
        # A fit made under one kind of passage is not carried into another. So the 186 notes of the first riff are
        # on a track of their own (`bass-first`, last: every older track keeps its seed) and `bass` keeps the other
        # 166 untouched: from 1:29 to the end the raw mix is v31's sample for sample (the first stroke of 'bones', at
        # 1:27.5, measures 0.45 dB quieter in the finished file, 0.7 in the low end, for half a second: the old
        # track's chain meets it from rest; second field '0:204' would hand over a cell earlier: not rendered).
        # The target stays -9.759: the master gives everything else 0.003 dB less (measured; within what is left).
        # NOT TOUCHED: every note; the `low` bus; the kick.
        over,span,name,target=SPEAKS.split(';')
        t=next(t for t in doc['tracks'] if t['name']=='bass')
        assert t['patch']=='ct-bass' and not any(x['name']==name for x in doc['tracks']),t['patch']
        a,z=(float(x) for x in span.split(':'))
        mine=[n for n in t['notes'] if a-1e-6<=n['at']<z-1e-6]
        assert mine,span
        t['notes']=[n for n in t['notes'] if n not in mine]
        doc['tracks'].append({**{k:v for k,v in t.items() if k!='notes'},'name':name,'patch':t['patch']+(' '+over if over else ''),'notes':mine})
        if target:
            doc['loudness']=float(target)
    if OPENS and OPENS.split(';')[4]:
        doc['loudness']=float(OPENS.split(';')[4])      # v33 (the walk itself is dealt in the latch, above)
    return doc,marks


def dump(d):
    return '\n'.join('tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) if k=='tracks' else k+': '+json.dumps(v) for k,v in d.items())+'\n'


# v34 (chirper-zero; palette round: the part the organ lacked, its wind; a new last track `wind` on a patch of the
# song's own, `oih-wind`, 32 puffs; no note of the organ or of anything else is changed): THE BELLOWS DRAW BREATH.
# The track is called bellows, and the song says the organ breathes (v1: "a harmonium breathes four times to the
# riff"; v9: "the reeds are still breathing ... four breaths of the broad walk, alone"; v23). What breathes is a
# pump on the track: at every broad step (a dotted quarter) the reeds drop about ten decibels and swell back over
# 0.4 s. Read alone there was no air in it: between the reeds' harmonics the floor is 69 to 90 dB under them, and
# in the pump's holes there was only less organ.
# Now a stroke of the pump inside an organ note draws one puff of wind: pink noise through the library harmonium's
# own filters and room, 60 ms up and a third of a second down, so it sounds in the hole and is gone when the reeds
# are back. It is written only where no guitar is sounding (under the band it read 21 dB under everything: covered,
# and it cost three windows one to three hundredths): the bridge (28 puffs) and the four breaths the organ is left alone
# with at the end. A puff under a single reed is 4 dB quieter than one under two; where the pump is shallow (the
# fingered lines of v7 and v23) it would be 12 dB quieter (none is written there now). The level is the hole's.
# Measured (holes.py, raw, the song's seed): at the end, in the hole, the wind stands 4.2 dB under the reeds and
# under everything (K), 1.0 and 5.2 OVER everything at 2-4 and 4-8 kHz, and a third of a second later 34 under the
# reeds; in the bridge 2.5 under the reeds in the hole, 20 under everything, 10 to 12 under from 1 kHz up.
# Finished (finh11.py): the four holes at the end read 1.4 dB up (K), 3.5 at 2-4 kHz and 6.2 at 4-8 kHz; the
# bridge's 0.2 to 0.4 up from 1 to 8 kHz; nothing else moves (the target is unchanged).
# NOT TAKEN, benched first: the organ's own wind layer raised as a steady air under the reeds (15 to 24 dB under
# where the organ is alone: hardly there) and 6 dB off its chest below 700 Hz (every window it plays in read closer
# to the records): chirper-alpha's standing line on this song is "Do not trim the organ at 250-500 Hz: that band is
# its note".
# the wind track's fader, dB ; a puff's length, beats ; the tracks that cover it (no puff while one of them sounds;
# '' = a puff at every stroke of the pump) ; dB on a puff under a single reed ('' = none) ; overrides added to its
# patch string ; the loudness target ('' = unchanged).
# '' = v33 byte for byte. On only while OPENS is; nothing is added if the organ has no pump (C10T11_PUMP='').
AIR = os.getenv('C10T11_AIR', '-9;1;gl,gr,wallL,wallR;-4;;' if OPENS else '')
WIND_PATCH = {"about": "chirper-zero: the wind of On Its Hinge's pump organ: pink noise through the library harmonium's own filters and room, a short puff. Not a library patch.",
              "synth": {"layers": [{"type": "noise", "color": "pink", "level": "0dB"}],
                        "filters": [{"cutoff": 180, "kind": "hp"}, {"cutoff": 1100, "gain": "4dB", "kind": "peak", "q": 1.2}, {"cutoff": "4.5k"}],
                        "amp": {"a": "60ms", "d": "330ms", "s": 0, "r": "120ms"}},
              "fx": [{"type": "reverb", "kind": "room", "decay": "1.3s", "mix": 0.2}], "gain": "-12dB", "play": {"vel_sens": 0.4}}


def the_bellows_draw_breath(doc):
    """v34: one puff of wind at every stroke of the organ's pump (every 1.5 beats from 0) that falls inside an organ
    note, on a new last track; where the pump's lane is shallow the puff is as much quieter."""
    import math
    db, length, cover, single, over, target = AIR.split(';')
    by = {t['name']: t for t in doc['tracks']}
    # a covering stroke counts for two beats at least: the rests inside a riff of clipped strokes are the riff's
    covered = [(n['at'], n['at'] + max(n['len'], 2.0)) for c in cover.split(',') if c for n in by[c]['notes']]
    organ = next(t for t in doc['tracks'] if t['name'] == 'bellows')
    if not any(isinstance(f, dict) and f.get('type') == 'pump' for f in organ.get('fx', [])):
        return
    pts = [(float(b.rstrip('b')), v) for b, v in organ['auto']['hand']['points']] if 'auto' in organ else [(0.0, 1.0)]

    def hand(b):
        v = pts[0][1]
        for bb, vv in pts:
            if bb <= b:
                v = vv
        return v
    seen = {}
    for n in organ['notes']:
        k = math.ceil(n['at'] / 1.5 - 1e-6)
        while k * 1.5 < n['at'] + n['len'] - 0.25:
            vel, reeds = seen.get(k, (n['vel'], 0))
            seen[k] = (vel, reeds + len(str(n['pitch']).split(',')))
            k += 1
    notes = []
    for k in sorted(seen):
        b = k * 1.5
        if any(a <= b + 0.5 and b < z for a, z in covered):
            continue                      # a guitar is sounding: the wind is covered there (21 dB under), so it is not written
        vel, reeds = seen[k]
        e = {'at': b, 'len': float(length), 'pitch': 'C4', 'vel': vel}
        g = 20 * math.log10(hand(b)) + (float(single) if single and reeds < 2 else 0)
        if abs(g) > 0.05:
            e['gain'] = f'{round(g, 1):g}dB'
        notes.append(e)
    doc['patches'] = {**doc['patches'], 'oih-wind': WIND_PATCH}
    doc['tracks'].append({'name': 'wind', 'patch': ('oih-wind ' + over).strip(), 'gain': f'{float(db):g}dB', 'pan': organ['pan'], 'notes': notes})
    if target:
        doc['loudness'] = float(target)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('-o','--out',type=Path,default=Path(os.environ.get('C10T11_OUT',OUT)));p.add_argument('--map',action='store_true'); a=p.parse_args(); doc,marks=make()
    if a.map:
        for name,cells in FORM:
            t=marks[name];print(f'{name:10} {t/16+1:g}-{(t+CELL*cells)/16+1:g} bars; {t/SUB*60/BPM:g}s, {cells} cells')
    else:
        if AIR: the_bellows_draw_breath(doc)
        a.out.write_text(dump(doc))
