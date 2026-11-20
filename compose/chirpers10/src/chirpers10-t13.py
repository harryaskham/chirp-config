#!/usr/bin/env python3
"""Where It Was — Common Time, t13. A four-note tune becomes four rests.

The bar has twelve triplet eighths; the tune has eleven. Its four notes descend
Eb C Ab F. When the tune passes to a struck ring, each guitar attack it gives
away buys one group of muted notes in the negative of that tune. Then even the
ring is taken away. No tempo change; the drummer gives the ear a plain four.
"""
import argparse
import json
from collections import defaultdict
from math import lcm
from pathlib import Path

BPM, SUB, BAR, F = 96, 3, 12, 29
CELL = 11
LANDING = lcm(BAR, CELL)
HEADS = (0, 3, 7, 9)
TUNE = (10, 7, 3, 0)  # a falling answer to the album's F / Ab / C / Eb
FORM = [('chalk', 4 * BAR), ('the shape', LANDING), ('the handover', LANDING),
        ('where it was', LANDING), ('under glass', LANDING), ('lit through', LANDING),
        ('turn the sheet', LANDING), ('both sides', LANDING), ('one impression', 2 * BAR)]
PITCH = 'C Db D Eb E F Gb G Ab A Bb B'.split()
OUT = Path(__file__).resolve().parents[3] / 'songs/chirpers10-t13.yaml'


def name(n):
    return PITCH[n % 12] + str(n // 12 - 1)


# v18 (chirper-three, whole song: the mix; no note changes): THE BAND, READ PART BY PART. This song's band is the
# one So Far (track seventeen) began with: the bass on a bare track, the library's kick, one cut on the drums bus.
# So Far's was read against the eleven records part by part over three rounds (its v3, v4 and v6); this one never
# was. The same read here, on 'where it was' and 'the shape' (raw), said: the KICK alone was 53% of the whole
# mix's power in 'where it was' (75% of everything under 60 Hz, where the song stood 2.5 dB over the records), the
# kit 6.5 dB over the records' drums at 250-500 Hz, and the BASS 10.4 dB under everything else and 7 dB short of
# the records' basses at 1-2 kHz, where a bass line is followed. So, of So Far's three moves, the two this
# song's read supports, each fitted here:
#   the bass goes through the album's chain (tracks 1, 7, 8, 14, 17) with a smaller lift at 90 Hz (5.5 dB for
#     7.5: in the two sections read raw the song was not short at 60-120 Hz) and its fader at -1
#   the kick's drum is tuned a semitone up, to B flat (its weight straddles 60 Hz as the records' kicks do), its
#     fader comes down 1.5 dB, and the kick and the snare each lose 4 dB of box at 340 Hz
# NOT TAKEN, on this song's read: the cymbals' shelf and the bus's lower low-pass (the song is 2.2 to 2.7 dB SHORT
# at 8-16 kHz as it is); the guitars' lower tight filter (they are 2.1 dB under the records' guitars at 120-250 Hz
# in 'where it was', not 5.3, and the mix is already 0.9 over there).
# The box cut is on the two tracks, not on the drums bus, so that the toms, which play alone in 'chalk' and 'under
# glass', are not touched: those two sections have no bass, kick, snare or guitar, and before the master they are
# sample for sample v17's (raw residual -98 dB). AFTER THE MASTER THEY ARE QUIETER: v17's kick was driving the
# limiter, and the loudness target was being reached by turning everything up under it; with the kick in its
# place the same target needs less gain (see the round note for how much).
# the bass's fader and chain ; the kick's drum and fader ; the box cut on the kick and the snare ; the loudness
# target. --v17 restores v17.
BAND = {'bass': (-1, [{'type': 'eq', 'bands': ['hp cutoff=29', 'peak cutoff=44 q=1.5 gain=-7dB', 'peak cutoff=90 q=1 gain=5.5dB',
                                               'peak cutoff=350 q=1 gain=-8dB', 'peak cutoff=1500 q=1 gain=4dB']},
                      {'type': 'compressor', 'threshold': '-26dB', 'ratio': 8.0, 'attack': '12ms', 'release': '120ms', 'makeup': '2.5dB'},
                      {'type': 'eq', 'bands': ['peak cutoff=170 q=1.2 gain=-3dB']}]),
        'kick': ({'pitch': 'A#1'}, 0.5),
        'box': 'peak cutoff=340 q=1.2 gain=-4dB',
        'loudness': -10.035}   # v17's own (see the round note: the master's gain is NOT what it was, and cannot be)
# v19 (chirper-zero, instrument round): THE HI-HAT CAN BE HEARD. The drummer plays a hi-hat on every beat of the
# shape, the handover, where it was and both sides (162 strokes), on the cymbals' track at the cymbals' fader: 12.5
# dB under where every other song on the record has its hat. On its own strokes it stood 25 dB under the mix
# (tools/presence.py calls a part buried at -25; the record's other hats stand 12 to 15 under: Odd Sympathy -12.0,
# Common Measure -14.3, Plain Hunt -14.4, On Its Hinge -15.2). Nothing was missing from the band it lives in: the
# mix read within 1 dB of the records at 8-16 kHz there, because the snare's wires and the kick's click held it
# (in 'where it was' the kick alone held 41% of 8-16 kHz). So the top of the song was a click and a crack and no
# metal. The hat comes up to the record's own level (the kit's hi-hat -10 -> +0.5 dB on this track only; the ride,
# the china and the crashes on the same track are not touched), and the kick gives up what it has above 9 kHz,
# which is not its click (that is at 4.3 kHz) and is where the hat lives.
# AFTER: the hat on its strokes -24.7 / -25.2 -> -14.3 / -14.8 dB against the mix (the shape / where it was), 44% of
# the mix's 8-16 kHz; the kick's strokes -3.1 -> -3.1, its share of 4-8 kHz unchanged. The mix against the records
# at 8-16 kHz: the shape -1.0 -> -0.1, where it was -0.5 -> -0.1, the handover +0.5 -> +1.4 (the cost), lit through
# +1.4 -> +0.6, turn the sheet +1.8 -> +1.3 (the kick's fizz gone from under the ride).
# the hi-hat's gain in the kit on the metal track, dB ; one more band on the kick's eq ; the loudness target.
# --v18 restores v18.
HAT = {'gain': 0.5, 'kick': 'lp cutoff=9000', 'loudness': -10.03}
# v20 (chirper-three, section w2: 0:30.0-0:37.5, the last three bars of 'the shape', which the map flags and no
# round had worked): THE TUNE IS MADE WHOLE BEFORE IT IS TAKEN APART. From 0:37.5 the tune is given away a note at
# a time, in the order E flat, C, A flat, F. Until now it went into that as it had been since 0:10: the first note
# a fifth (the one chord in it), the other three single low notes. Now, in the three cells before the handover,
# each of those three is made a fifth as well, one more a cell, in the order they will go: C at 0:31.2, A flat too
# at 0:34.4, F too at 0:37.1. The last cell is the whole tune in fifths, as the return plays it from 2:55 and the
# slow last statement at 3:22; the next thing heard is the crash, the ring's E flat and no band.
# And the two clocks close. The tune is eleven ticks long and the bar twelve, so its first note falls one tick
# nearer the bar line every cell: three ticks after it at 0:30, two, one, and on it at 0:37.5. The drummer plants
# those three bar lines on the floor tom, harder each time, as he planted the opening's (0:02.5-0:10), and the foot
# goes with it. So the distance is heard: tom, (F), tune; tom with the F, tune; (F), tom, tune; and together.
# Both guitars only gain the upper note of each fifth; no note moves. The bass, the snare and the hat are as written.
# cells before the handover whose tune is made whole ; the floor tom's three strokes ; the foot's on the bar line ;
# the loudness target. --v19 restores v19 byte for byte.
WHOLE = {'cells': 3, 'tom': (.70, .77, .84), 'foot': .9, 'loudness': -10.03}
# v21 (chirper-one, section w6, the map's first flag; the change is 2:45.8-2:52.7, the last of the side-to-side
# trade before its closing statement): SPUN FAST ENOUGH, BOTH FACES SHOW AT ONCE. v15 spun the sheet: the tune
# changes side once a cell, then twice a cell, then at every note, "a card with a picture on each face, spun
# fast enough, shows both at once". It never did show both: at every note there was still one face a cell. Now
# the turning goes one step further each cell (a cell a side, two notes a side, a note a side) and then the two
# faces are played TOGETHER for two cells: the left guitar the front (E flat, C, A flat, F on 0, 3, 7, 9), the
# right guitar the back (F, A flat, C, E flat on 0, 2, 4, 8), in the one cell.
# What that makes was already in the tune and has not been heard: the two faces strike seven of the cell's
# eleven places between them and leave FOUR. The tune was four notes in seven rests; its negative seven strokes
# round four holes; the two faces at once are seven notes round four rests of their own (1, 5, 6, 10). And it is
# one riff: after the first chord the sides alternate at every note, right left right, left right left, and the
# pitches go up the record's hook and come back down the tune: A flat, C, C, A flat, E flat, F.
# The bass and the foot play all seven (the lower note where both strike). Nothing plays the muted strokes: the
# first time the four rests are EMPTY but for the ride and the backbeat; the second time the two wooden boxes,
# together for the only time in the song, say the four rests (v4: "a different material for the holes").
# The ring rings the front in both cells, as it does wherever the front is said. The closing statement on the
# right (2:52.7), the fill and the return are as written; so are the six cells on the wiw-turned card and the
# cell after them.
# the cell (of the trade's twelve) that turns at every note ; the cells where both faces are played at once ;
# the boxes' strokes in the four rests of each of those cells (0 = left empty) ; the foot's on the first note
# and the rest ; the loudness target. --v20 restores v20 byte for byte.
FUSED = {'every': 8, 'cells': (9, 10), 'wood': (0, .95), 'foot': (.95, .84), 'loudness': -10.03}
# v22 (chirper-alpha; section w4, 'under glass', 1:32.5-2:00, the quiet middle; the window least recently worked):
# THE TITLE IS SUNG, A WORD AT A TIME, FROM ITS END. In 'under glass' the bass finds the tune again from its last
# note: F; then A flat, F; then C, A flat, F; then all four. Each find is said three times (three cells): the bass
# alone, then with the ring remembering, then with the ring caught up. The tune is four notes and so is a line of
# four words. Now the middle cell of each three is SUNG, on the notes found so far, each note its own word, and
# since the notes come back last first so do the words: "was"; "it was"; "where it was"; "right where it was".
# The song says its name once, at 1:55.4, in the cell after the tune is whole again, and it is the first voice in
# the song (the record asks for voices, different ones in different parts: a close, soft one here).
# THE BASS AND THE RING REST WHILE IT IS SUNG. Sung over them the words did not survive: the recogniser read 3 of
# the 10 words with the fretless under the voice (0 of 10 with the voice and the fretless alone; 9 of 10 with the
# voice alone, where only the lone first "was" is missed), and with the bass out but the ring striking the same
# notes in the same octave it read 5 of 10 on two seeds of three. So each find is now said by three in turn: the
# bass finds it, the voice names it (over the toms and the held glass), the bass and the ring keep it. Ten
# fretless notes and six ring notes are left out; nothing else is touched (the toms keep bar time under the voice).
# THE WORDS were chosen by the recogniser, voice alone: "right" read on every voice tried; "back", "still" and
# "there" did not ("back" -> egg, make, take). THE VOICE: the library's close voice with its clearest diction,
# on the tune's notes two octaves over the bass (F3 to E flat 4), behind a 150 Hz high-pass and 4 dB less at
# 330 Hz (the section already stood 4.8 dB over the records at 250-500 Hz), at the level the bass's own statement
# of the same notes has the cell before (-1.9 to +1.8 dB, the line growing as it fills).
# the tune's four words, first note to last ; how each is sung ; which of a group's three cells is sung (0 the cell
# where the bass finds the note, 1 the next, 2 the cell where the ring has caught it) ; the voice ; its fader, dB ;
# its place ; how far over the bass it sings, semitones ; how hard ; how long the last word is held, ticks ; its
# send to the chamber ; its eq ; the loudness target. --v21 restores v21 byte for byte.
SAID = {'words': ('right', 'where', 'it', 'was'),
        'ph': {'right': 'R AY1 T', 'where': 'W EH1 R', 'it': 'IH1 T', 'was': 'W AA1 Z'},
        'takes': (1,), 'alone': True, 'patch': 'voice-near synth.layers.0.diction=3', 'gain': -12.5, 'pan': 0, 'up': 24, 'vel': .8,
        'last': 2.5, 'send': '-12dB',
        'fx': [{'type': 'eq', 'bands': ['hp cutoff=150', 'peak cutoff=330 q=0.9 gain=-4dB']}], 'loudness': -10.03}

# v23 (chirper-two; section w7, 3:00-3:27, 'both sides' and the close; the change is 3:06.0-3:12.8 and one word at
# 3:26.25): THE WORD LEFT OUT. Two earlier rounds meet. v16: over the four short negatives the ring brings the tune
# back into its holes last note first (F; A flat, F; C, A flat, F), and in the fourth cell it has E flat, C, A flat
# and leaves the F out: the one hole left empty, where it was. v22: in the quiet middle the title is sung a note a
# word, from its end. Now each note the ring brings back is SUNG ON ITS WORD (nine notes, nine syllables, an octave
# under the ring): "was" (3:06.0); "it was" (3:07.9); "where it was" (3:09.4); "right where it" (3:11.0) - and where
# the ring leaves its F out, the voice leaves out "was" (3:12.9). The line has been heard whole once, at 1:55; the
# listener finishes it. The band answers with the tune at 3:13.3, as before. The word is given back once, on the
# song's last note (3:26.25, the slow close's low F): "was".
# No other note changes. It is a second voice, not the first (Harry, 12 Nov: different voices in different
# parts): the middle's is the library's close, soft one; this is its legato voice with the ring and the effort
# turned up, and DRY, so that nothing of "it" rings into the hole.
# FITTED TO THE RECORDS' VOICES, as So Far's were (its v13; tools/voxref.py). Five library voices alone, as they
# come, all read as body with no middle: +13 to +18 dB under 250 Hz, -6 to -13 at 1-2 kHz, -8 to -15 at 2-4 kHz
# against the records' vocal stems. With a high-pass at 350 Hz, a low shelf of -12 dB at 900 Hz and 3 dB out at
# 420 Hz, this one is within 2.6 dB of them from 250 Hz to 8 kHz (+1.1, +0.9, -2.4, +1.0, +2.6). "It" is lifted
# 4.5 dB (a short closed vowel: 5 dB under the others once the body is gone): the nine syllables then lie within
# 2.7 dB of one another.
# THE LEVEL WAS SET ON THE FINISHED FILE, NOT THE BENCH. Raw, at -14 dB, the voice read -9.3 dB against the mix
# while it sings (the records' voices: -9.2). In the finished file the same voice read -5.6 to -6.1: the limiter
# takes the band's strokes down and leaves what lies between them, so a voice between strokes comes UP when
# mastered. At -16 dB it reads, as mastered, -7.2 to -7.7 whole and -5.5 to -5.9 at 1-4 kHz (records -9.2 and
# -7.1) on three seeds: 1.5 to 2 dB over the records' place, and left there (the words are the whole point of
# these seven seconds, and the records' voices are screams that need less). The median syllable, as mastered,
# stands 6.5 to 7.0 dB under everything else over its length and 0.6 to 1.3 under in the band's rest where it begins.
# The last word has 2 dB more than the others (as mastered -7.5 to -7.7 against the last chord).
# the voice ; its fader, dB ; its place ; semitones over the bass ; how hard ; how long a cell's last word is held,
# ticks ; how long the last word before the hole is, ticks ; dB on single words ; the word on the song's last note:
# how long, ticks, and dB (None: it is never said) ; its eq ; the loudness target.
# --v22 restores v22.
UNSAID = {'patch': 'voice-legato synth.layers.0.diction=3 synth.layers.0.ring=1.0 synth.layers.0.effort.value=0.9 fx.0.mix=0', 'gain': -16.0, 'pan': 0,
          'up': 24, 'vel': .9, 'last': 2.0, 'cut': 1.5, 'lift': {'it': 4.5}, 'end': (5.5, 2.0),
          'fx': [{'type': 'eq', 'bands': ['hp cutoff=350', 'lowshelf cutoff=900 gain=-12dB', 'peak cutoff=420 q=1 gain=-3dB']}], 'loudness': -10.03}
# v24 (chirper-one; section w5, 'lit through', 2:00-2:30, the window longest without a round; the change is
# 2:02.3-2:13.7, its five cells on F): THE POINTS MELT INTO THE LINE. Since v14 the tune comes back here as a LINE:
# the first cell struck as it always was (four points), then a hand on the ring and each note held until the next.
# The change from points to a line was a cut: struck at 2:00.0, held from 2:02.3. Now it is heard happening. Each
# held note of the five cells on F begins with a touched harmonic on the clean guitar (the opening's guitar, which
# has not played since 0:10), at the held note's own pitch: a point with the line growing out of it. In the first
# of the five cells the harmonic is a little over the held note's start; it gives way cell by cell as the hand
# firms, and by the fifth the line has taken it in. Over A flat (2:13.7) the line is alone, as v14 wrote it.
# Benched raw, the harmonics alone against the held line alone, each note's first 150 ms: see the round note.
# The harmonic is the string touched at its quarter (two octaves over the stopped note: E flat 3, C3, A flat 2 and
# F2 stopped, sounding the line's E flat 5, C5, A flat 4, F4). The patch's compressor is opened (it flattened the
# fade) and its body under 500 Hz is cut: this is a glint, not a second guitar.
# the cells of 'lit through' it sounds in (first, last) ; the guitar ; its fader ; its side ; its room ; the node (4:
# the string touched at its quarter) ; how hard ; dB on the first cell's notes and the last's (the strike gives way) ;
# dB on each of the tune's four notes, E flat C A flat F (the lowest string's harmonic is the weakest here) ; its eq ;
# the loudness target. --v23 restores v23.
GLINT = {'cells': (1, 5), 'patch': 'ct-clean synth.layers.0.pinch=1 synth.layers.0.node=4 fx.0.threshold=0dB', 'gain': 0.0, 'pan': .06,
         'send': '-9dB', 'node': 4, 'vel': .8, 'grow': (-2.5, -7.0), 'lift': (0.0, 0.0, 0.0, 4.0),
         'fx': [{'type': 'eq', 'bands': ['hp cutoff=500']}], 'loudness': -10.03}


# v25 (chirper-zero; instrument round: the snare, 84 backbeats; no stroke moves): THE SNARE RINGS A TONE LOWER, AND
# LONGER. By part the kit stood 6.4 dB over the records' kits at 500 Hz-1 kHz, the most on the album, and the
# snare is why: alone, beside six records' snare strokes (tools/snarespec.py), it read 5.07: its note a band too
# high (200 Hz -13.3, 250 Hz +9.1), a box at 1 kHz (+8.9), and it was a TICK: it fell 20 dB in 38 ms (the records'
# 66) and stood 15.4 dB out of its own tail (13.8). In the Time Of v26 found the box in the head's mode count, so:
# ten modes; the drum a tone lower (A3 -> G3); the kit's +5 dB at 200 Hz to -3 (the note itself is there now); the
# stick's slap 1.2 -> 0.8. AND IT RINGS: a looser head (damp 0.3 -> 0.15), the head's decay 0.18 -> 0.38 s, the
# amp's 140 -> 260 ms, the wires up and nearer (0.85 -> 0.95, gap 0.1 -> 0.05). With ten modes and a lower note a
# new hump stood at 630-800 Hz (+7.3, +6.7): a cut there. THE MIX CHOSE THE TOP: with the wires longer and no
# shelf the mix read 0.12 worse, 8-16 kHz 0.8 further over; with 4 dB off above 6 kHz it reads a little nearer
# than v24 (0.799 -> 0.789, weighted by where the snare plays; 8-16 kHz +1.0 -> +0.1). ALONE: 5.07 -> 2.89; body
# against crack +1.1 -> -1.4 (records -2.9); punch 15.4 -> 13.9 dB; it falls 20 dB in 38 -> 52 ms. Fader 3 ->
# 1.5 dB: a stroke stands as far out of the band (+7.4 -> +7.5 dB, K). The side stick and the grace are left.
# the drum's note ; overrides inside the snare's patch ; its track's eq ; its fader ; the loudness target (a longer
# snare measures louder: at v24's -10.03 the stretches with no snare came out 0.05 to 0.06 dB quieter).
# --v24 restores v24.
SNARE = {'pitch': 'G3',
         'patch': 'synth.layers.0.mode_count=10 synth.filters.1.gain=-3dB synth.layers.0.slap=0.8 synth.amp.d=260ms synth.layers.0.decay=0.38s '
                  'synth.layers.0.damp=0.15 synth.layers.0.wires=0.95 synth.layers.0.gap=0.05',
         'eq': ['peak cutoff=340 q=1.2 gain=-4dB', 'peak cutoff=690 q=1.5 gain=-5dB', 'peak cutoff=3500 q=1 gain=2dB', 'highshelf cutoff=6000 gain=-4dB'],
         'gain': '1.5dB', 'loudness': -10.0}


def the_snare_rings_lower(doc):
    """v25: the album kit's snare with ten head modes, a tone lower, on a looser head with its wires nearer."""
    t = next(t for t in doc['tracks'] if t['name'] == 'snare')
    t['patch'] += ''.join(f' kit.s.patch.{o}' for o in SNARE['patch'].split()) + f" kit.s.pitch={SNARE['pitch']}"
    t['fx'] = [{'type': 'eq', 'bands': SNARE['eq']}]
    t['gain'] = SNARE['gain']
    if SNARE['loudness']: doc['loudness'] = SNARE['loudness']


# v26 (chirper-alpha; palette round: one new instrument, on the back of the sheet, 2:29.8-2:52.7): THE BACK OF THE
# SHEET IS WOOD. In 'turn the sheet' the front of the sheet (the tune falling, on the left) has always had a struck
# voice over its guitar: the ring, a mallet on metal. The back (the tune read from its other end, rising F, A flat,
# C, E flat on 0, 2, 4, 8: the record's own hook, and the place Harry chose for it) had its guitar, and wooden
# boxes in its holes (v4: "a different material for the holes"), and no struck voice. Now it has: a XYLOPHONE, in
# its lowest octave, the ring's own (F4 to E flat 5), strikes the back's four notes wherever the back is said: the
# four back cells of the trade and the two cells where both faces are played at once, where ring and bars share
# one line of seven notes between them (24 strokes). Metal says the front, wood says the back, notes and holes.
# No other song on the record has a xylophone. Nothing else changes; no note of the band moves.
#   THE READ THAT CHOSE IT (raw, stroke by stroke, a part alone against everything else): in this passage the ring
#   stands 10.2 dB (K) under the mix at its strokes and -1.1 at its own pitch (in the handover: 0.0 and +2.7). The
#   bars at -14 dB stand 8.1 under the mix, +3.0 at their pitch (-5.1 to +9.1) and +13.2 in their best third-octave
#   (none of 24 under 0). An octave higher (F5 to E flat 6) the same bars read -1.0 at their pitch: not kept. A
#   marimba read better still (+9.7 against +6.2 at one fader) and is the thing to try if the xylophone is a toy.
#   TWENTY MILLISECONDS BEHIND THE STRING. Struck on the band's own stroke the bars raised the mix's peak there by
#   a median 1.0 dB and the master took the band down 0.7 dB for a tenth of a second at each (worst 1.8). Twenty
#   milliseconds behind, the peak rises 0.17 dB (the ring's own strokes: 0.31) and the band gives 0.3 to 0.4.
#   AGAINST THE ELEVEN RECORDS 'turn the sheet' was short at 250 Hz-1 kHz (-1.3, -1.2); with the bars +0.4, -0.4,
#   and all nine bands read 0.87 -> 0.68. Every other section is v25's within 0.01 dB.
# the bars' patch ; fader, dB ; place ; semitones over the guitar's note ; velocity on a cell's first note and the
# others ; length, ticks ; how far behind the string they strike, ticks (0.096 = 20 ms) ; send to the chamber ; track fx ; dB on the ring through 'turn the sheet' (0: as it was) ;
# the loudness target (None: unchanged). --v25 restores v25. (--verso '{"gain": -9}': fields changed for a bench.)
VERSO = {'patch': 'xylophone fx.0.mix=0', 'gain': -14, 'pan': .2, 'up': 36, 'vel': (.9, .8), 'len': 1.45, 'late': .096, 'send': '-12dB', 'fx': None,
         'ring': 0, 'loudness': None}


def compose(phrase_return=True, recover=True, wood=True, wood_gain=-12, held_back=True, afterimage=True, drum_memory=True, edges=True,
            rim=True, rim_gain=-18, turned=True, hole=True, mold=True, fretless=True, fretless_gain=-10.0,
            lit=True, held_gain=-16.0, grip='0.12:0.55:0.7', spin=True, refill=True, whole_scale=True, trades=True, band=True,
            hat=True, made_whole=True, fused=True, said=True, said_gain=None, said_takes=None, unsaid=True, glint=True, verso=True):
    # Previous versions remain reproducible, including their track lists.
    recover = recover and phrase_return
    wood = wood and recover
    held_back = held_back and wood
    afterimage = afterimage and held_back
    drum_memory = drum_memory and afterimage
    edges = edges and drum_memory
    rim = rim and edges
    turned = turned and rim
    hole = hole and turned
    mold = mold and hole
    fretless = fretless and mold
    lit = lit and fretless
    spin = spin and lit
    refill = refill and spin
    trades = trades and refill
    band = BAND if band and trades else None
    hat = HAT if hat and band else None
    made_whole = WHOLE if made_whole and hat else None
    fused = FUSED if fused and made_whole else None
    said = SAID if said and fused else None
    unsaid = UNSAID if unsaid and said else None
    glint = GLINT if glint and unsaid else None
    verso = VERSO if verso and glint else None
    if said and (said_gain is not None or said_takes):
        said = {**said, **({'gain': said_gain} if said_gain is not None else {}),
                **({'takes': tuple(int(x) for x in said_takes.split(','))} if said_takes else {})}
    marks = {}
    # v12: THE NEGATIVE IN PITCH. The tune takes four of the scale's seven
    # notes; the three it leaves out lie one between each pair it steps
    # across: D-flat between E-flat and C, B-flat between C and A-flat, G
    # between A-flat and F. Nothing lies between F and the next E-flat.
    SCALE = (0, 2, 3, 5, 7, 8, 10)
    BETWEEN = tuple(([n for n in SCALE if lo < n < hi] or [0])[0] for hi, lo in zip(TUNE, TUNE[1:] + (TUNE[-1],)))
    assert BETWEEN == (8, 5, 2, 0) and sorted(set(TUNE) | set(BETWEEN)) == list(SCALE)
    # v10: the sheet turned over. Read from its other end the cell strikes on
    # 0, 2, 4, 8 and the four notes rise, F A-flat C E-flat: the record's own
    # hook, which this tune was written as the falling answer to.
    BACK_HEADS = tuple(sorted((CELL - k) % CELL for k in HEADS))
    BACK_TUNE = TUNE[::-1]
    assert BACK_HEADS == (0, 2, 4, 8) and [F + n for n in BACK_TUNE] == [F, F + 3, F + 7, F + 10]
    # v15: THE SHEET SPINS. In the side-to-side trade the tune changes side
    # once a cell: one face of the sheet, then the other. After the six cells
    # on the wiw-turned card and one more, the sheet is turned faster: twice a
    # cell for two cells (two notes a side), then at every note for two cells.
    # A card with a picture on each face, spun fast enough, shows both at
    # once; and the next section is 'both sides'. The last cell is one whole
    # statement on the right, as written, with the fill; then both guitars.
    # The muted strokes and the box stay opposite the note they follow, so
    # each guitar now plays its gap INTO its note: wood or mutes, then the
    # string, on the same side. No note is added, removed or moved in time;
    # only its side. In mono the passage keeps its notes and its level
    # (0.1 dB); all that is left there is each note's change of amplifier.
    def face(i, j):
        if spin and fused:                            # v21: one step faster each cell
            if i == fused['every'] - 1: return 1 - j // 2
            if i == fused['every']: return 1 - j % 2
            return i % 2
        if spin and 7 <= i <= 8: return 1 - j // 2   # right, right, left, left
        if spin and 9 <= i <= 10: return 1 - j % 2   # right, left, right, left
        return i % 2
    parts = defaultdict(list)
    def put(tr, at, dur, p, v, mute=False, slide=False, ph=None):
        event = dict(at=round(at / SUB, 6), len=round(dur / SUB, 6),
                     pitch=name(p) if isinstance(p, int) else p, vel=round(v, 3))
        if ph:
            event['ph'] = ph                    # a sung syllable
        if mute:
            event['expr'] = {'pm': 1.0}
        if slide:
            event['expr'] = {'h': 1.0}  # the left hand arrives; no new pluck
        parts[tr].append(event)

    def drums(piece, t, v):
        track = {'k': 'kick', 's': 'snare', 'h': 'metal', 'x': 'metal',
                 'rde': 'metal', 'c': 'metal'}.get(piece, 'skins')
        put(track, t, 3.6 if piece in ('rde', 'c', 'x') else 0.8, piece, v)

    sides = ('left', 'right')
    def guitars(t, p, d, v, rigs=sides, mute=False, fifth=False):
        for rig in rigs:
            pitch = name(p) + ',' + name(p + 7) if fifth else p
            put(rig, t, d, pitch, v, mute)

    def last_exchange(start, span):
        """Twelve cells for the two sides to finish their sentences, 3:25's cadence untouched."""
        n = span // CELL
        assert n == 12

        def say(first, size, back=False):
            # Keep the contour AND its irregular spacing. Four times as broad
            # it is a line of ringing chords, not twelve more turns of the riff.
            heads, tune = (BACK_HEADS, BACK_TUNE) if back else (HEADS, TUNE)
            for j, k in enumerate(heads):
                t = start + (first*CELL + size*k)
                gap = size * ((heads + (CELL,))[j+1] - k)
                p = F + tune[j]
                dur = min(9.5, gap * .72)
                guitars(t, p, dur, .97 if j in (0,3) else .90, fifth=True)
                put('bass', t, gap-.37, p, .93)
                drums('k', t, .97 if j in (0,3) else .88)

        def trade(first, pairs):
            """v1's return: the tune for a cell on both guitars' ringing fifths, then its negative for a cell."""
            for i in range(2 * pairs):
                for j, k in enumerate(HEADS):
                    end = (HEADS + (CELL,))[j+1]
                    t = start + (first+i)*CELL + k
                    if i % 2 == 0:
                        guitars(t, F + TUNE[j], end-k-.35, .99, fifth=True)
                        put('bass', t, end-k-.3, F + TUNE[j], .90)
                        drums('k', t, .98)
                        continue
                    for n in range(k+1, end):
                        a = start + (first+i)*CELL + n
                        guitars(a, F, .61, .94 if n == k+1 else .76, mute=True)
                        put('bass', a, .65, F, .82 if n == k+1 else .68)
                        drums('k', a, .93 if n == k+1 else .73)

        def answer(first, count, stop=False, scale_last=False):
            for i in range(count):
                for j,k in enumerate(HEADS):
                    end = (HEADS + (CELL,))[j+1]
                    for pos in range(k+1, end):
                        # At the last answer the drummer lifts his sticks and the
                        # strings leave the last beat free for the slower coda.
                        if stop and i==count-1 and pos>=CELL-SUB:
                            continue
                        t = start + (first+i)*CELL + pos
                        v = .93 if pos==k+1 else .76
                        # v16: in the cell where the ring has the three missing
                        # notes, the strokes take the notes between them (v12).
                        p = F + BETWEEN[j] if scale_last and i==count-1 else F
                        guitars(t, p, .61, v, mute=True)
                        put('bass', t, .65, p, v-.1)
                        drums('k', t, v)

        if trades:
            # v17 (chirper-zero, 19 Nov), TWO OF HARRY'S ANSWERS. wiw-return, "Which return makes the four
            # notes stick?": "Short trades". So the return opens as it did at v1, the take he chose: the tune
            # a cell, its negative a cell, twice (2:55.0-3:04.2), every stroke as v1 wrote it. The one long
            # statement (v2: the tune four times as broad on ringing chords) is gone. The four negatives the
            # ring refills (v16) follow as they were, so the band is on the negative side for five cells
            # running while the ring brings the tune back into the holes.
            trade(0, 2)
        else:
            say(0,4)                                                  # one long statement
        answer(4,4,scale_last=refill and whole_scale)                 # four short negatives
        if refill:
            # v16: THE RING COMES BACK INTO THE HOLES, LAST ONE FIRST (3:06-3:13).
            # The tune left the band a note at a time from its front (the
            # handover: E-flat, then C, A-flat, F), each note passing to the
            # struck ring; then the ring went too. The bass found it again from
            # its last note (under glass). 'Both sides' has said the two sides
            # in turn ever since v1: a statement, then negatives whose four
            # holes are empty, and no ring at all until the slow close. Now,
            # over the four short negatives, the ring refills the holes from
            # the back, as the bass did: F alone; A-flat and F; C, A-flat, F.
            # The band's muted strokes do not change, so the tune and its
            # negative sound in one cell, each in the other's gaps: both sides
            # of the sheet at once, for the first time. In the fourth cell the
            # ring has the three notes that were still missing, E-flat, C,
            # A-flat, and the F that came back first is the one hole left
            # empty: where it was. The band then says all four in two cells.
            # AND IN THAT FOURTH CELL THE STROKES COME DOWN THE SCALE (v12's
            # negative in pitch, heard once at 1:12-1:25 and not since): each
            # gap takes the note between the two around it, so ring and band
            # between them say the whole scale once, in turn: E-flat, D-flat
            # D-flat, C, B-flat B-flat B-flat, A-flat, G, the hole, low F.
            # (The drummer does the same at 3:20: three strokes, the fourth held
            # back for the close.)
            # The first of the four cells is still the tail of the wiw-return
            # excerpt (to 3:05.2); the ring's first note is at 3:06.0. The close
            # on wiw-turned starts at 3:13.2: a ring F at 3:12.9 rang 0.7 s into
            # it (first bench: -21 dB against the excerpt's first half second),
            # which is the other reason that F is the hole, and why the last
            # A-flat is let go early.
            for i in range(4):
                for j in range(3-i, len(HEADS) - (i == 3)):
                    last = i == 3 and j == 2
                    put('ring', start + (4+i)*CELL + HEADS[j], .8 if last else 1.45, F + TUNE[j] + 36, .91 if j == 3-i else .79)
                    if unsaid:              # v23: each note the ring brings back is sung on its word; the fourth cell's F is not
                        gap = (HEADS + (CELL,))[j+1] - HEADS[j]
                        put('unsaid', start + (4+i)*CELL + HEADS[j], unsaid['cut'] if last else unsaid['last'] if j == 3 else gap,
                            F + TUNE[j] + unsaid['up'], unsaid['vel'], ph=said['ph'][said['words'][j]])
                        if unsaid['lift'].get(said['words'][j]):
                            parts['unsaid'][-1]['gain'] = f"{unsaid['lift'][said['words'][j]]:g}dB"
        # then in two cells, then in one: and since v10 that last quick one
        # is the other side of the sheet, rising, so the slow close answers it.
        # v17: wiw-turned, "The tune now also runs backwards, rising: keep it?": "Keep it at 2:30, not before the
        # close". The quick last statement (3:17.9) falls again, as before v10; the trade at 2:30 keeps its rising answers.
        say(8,2); say(10,1,back=turned and not trades)
        answer(11,1,stop=True)

    def old_fourth_beat(start):
        """The intro put F on beat four. It echoes there while the tune walks off.
        Keep the opening THREE heavy cells: these are 'The tune' on wiw-negative.
        Its clip ends precisely when the right player changes from E-flat to F.
        """
        foot = HEADS[-1]
        furthest = len(HEADS)
        first = furthest-2
        echo_at = start + first*BAR + foot
        meet_at = start + 2*furthest*CELL + foot
        parts['right'] = [e for e in parts['right'] if not echo_at <= round(e['at']*SUB) < meet_at]
        for i in range(first, 2*furthest):
            # The first three F's keep bar time (12 ticks); the next three
            # close the gap in ten ticks each. Leave the low unison F at meet_at.
            late = (furthest-abs(furthest-i))*(BAR-CELL)
            offset = i*CELL+foot+late
            # Ring across the next E-flat and C, but lift for its A-flat.
            gate = (i+1)*CELL+HEADS[-2]-offset-.4
            guitars(start+offset,F+12,gate,.91,rigs=('right',),fifth=True)

    def recovery(start, span):
        """The glass chord occupies only the missing head. The bass finds a new note
        at the end of one cell, then plays it in its proper place in the next."""
        repeats, remainder = divmod(span, CELL*len(HEADS))
        assert repeats >= 2 and remainder == 0
        # v13: in the quiet middle the bassist puts the pick down. The tune is
        # rebuilt on a fretless bass (no other song on the record has one):
        # plucked with the finger, each note blooming after its start. And a
        # note is FOUND before it is played: at the end of a cell the hand
        # slides up the string from F to the new note without plucking again,
        # and in the next cell that note is plucked in its proper place.
        low = 'fretless' if fretless else 'bass'
        for i in range(repeats*len(HEADS)):
            group, take = divmod(i, repeats)
            first = len(HEADS)-1-group
            a = start + i*CELL
            if HEADS[first]:
                dyad = ('F3,C4', 'Ab3,Eb4', 'Eb3,Bb3')[group]
                # v9: a held glass tone, not a pluck: it stands exactly as long
                # as the tune's head is still missing, and lifts for the bass.
                put('rim' if rim else 'glass', a, HEADS[first]-.65, dyad, .82)
            pickup = take==repeats-1 and first>0
            for j in range(first, len(HEADS)):
                k = HEADS[j]; end = (HEADS+(CELL,))[j+1]
                # Shorten F by one triplet tick to make a breath for the pickup.
                if pickup and j==len(HEADS)-1: end -= 1
                # (v13: no breath; the F is held into the pickup, so the one
                # string slides up from it.)
                sounding = end-k+.30 if fretless and pickup and j==len(HEADS)-1 else end-k-.20
                if not (said and said['alone'] and take in said['takes']):     # v22: the bass rests while it is sung
                    put(low,a+k,sounding,F+TUNE[j], .93 if j==first else .84)
                # First time, the bassist says it alone. The ring remembers the
                # old tail on the second turn and catches the newest note last.
                # (v22: in the cell that is sung the voice takes the ring's turn)
                if take and (j>first or take==repeats-1) and not (said and said['alone'] and take in said['takes']):
                    put('ring',a+k,min(1.7,end-k-.25),F+TUNE[j]+24,.71)
            if pickup:
                put(low,a+CELL-1,.78,F+TUNE[first-1],.86,slide=fretless)
            if said and take in said['takes']:
                # v22: the notes found so far are sung, each on its own word; touching, so one breath
                for j in range(first, len(HEADS)):
                    k = HEADS[j]; end = (HEADS+(CELL,))[j+1]
                    put('said', a+k, end-k if j < len(HEADS)-1 else said['last'], F+TUNE[j]+said['up'], said['vel'],
                        ph=said['ph'][said['words'][j]])
        for beat in range(span//SUB):
            i,k = divmod(beat*SUB,CELL); group,take = divmod(i,repeats)
            first = len(HEADS)-1-group
            if take==0 and k>=HEADS[first]: continue  # no tom over the discovery
            q=beat%4
            if q in (0,2): drums('ft' if q==0 else 't2',start+beat*SUB,.55 if q==0 else .4)
        for off,piece in zip((3,2,1),('t1','t2','ft')):
            drums(piece,start+span-off,.59+(3-off)*.1)

    def both_faces(a, n):
        """v21: one cell with the front on the left guitar and the back on the right, and nothing in the gaps."""
        front, turned_over = dict(zip(HEADS, TUNE)), dict(zip(BACK_HEADS, BACK_TUNE))
        struck = sorted(set(front) | set(turned_over))
        rests = [k for k in range(CELL) if k not in struck]
        assert len(struck) == CELL - len(HEADS) and len(rests) == len(HEADS)   # seven notes round four rests
        for k in struck:
            # no note rings into a rest: the trade's stab (1.4 ticks), or up to the next rest
            stop = min(q for q in rests if q > k) - k - .1
            for rig, side in (('left', front), ('right', turned_over)):
                if k in side:
                    guitars(a + k, F + side[k], min(1.4, stop), .94, rigs=(rig,), fifth=list(side).index(k) in (0, 3))
            nxt = min([q for q in struck if q > k] + [CELL])
            put('bass', a + k, min(nxt - k - .3, stop), F + min(side[k] for side in (front, turned_over) if k in side), .90)
            drums('k', a + k, fused['foot'][0] if k == 0 else fused['foot'][1])
        for j, k in enumerate(HEADS):
            put('ring', a + k, 1.45, F + TUNE[j] + 36, .91 if j == 0 else .79)
        if verso:                       # v26: and the bars ring the back, as they do wherever the back is said
            for j, k in enumerate(BACK_HEADS):
                put('bars', a + k + verso['late'], verso['len'], F + BACK_TUNE[j] + verso['up'], verso['vel'][0] if j == 0 else verso['vel'][1])
        if fused['wood'][n]:
            for q, k in enumerate(rests):
                # v4's sticking for the gaps: the centre of the box for a rest, the slap for the second of two
                piece = 'cs' if k - 1 in rests else 'cb'
                for side in sides:
                    put('box-' + side, a + k, .65, piece, fused['wood'][n] if piece == 'cs' else fused['wood'][n] - .15)

    def box_stroke(cell, cells, head, slot, end):
        """The box borrows the negative; it never doubles the borrowed chug.
        Let the last pair of cells return to two guitars before the cadence card.
        """
        first = slot == head+1
        multi = end-head > 2
        if 2 <= cell < 4:
            take = multi and slot == end-1  # hear just the two rim answers
        elif 4 <= cell < cells-4:
            take = True
        elif cells-4 <= cell < cells-2:
            take = not first   # give the starts of the groups back first
        else:
            take = False
        if not take: return None
        # 2 + 3 + 1 + 1: centre/slap, centre/ghost/slap, centre, slap.
        if slot==end-1 and (multi or end==CELL): return 'cs'
        return 'cb' if first else 'cg'

    def hands_remember(start, span, section):
        """One sticking for the four missing notes. Remove backbeats wherever
        it speaks; the descent is in the touch, not four tuned drums."""
        def rest(tracks, a, b):
            for tr in tracks:
                parts[tr] = [e for e in parts[tr] if not a <= round(e['at']*SUB) < b]
        def stroke(at, j):
            if j==len(HEADS)-1:             # a left-hand grace into the last F
                put('snare',at-.15,.12,'g',.77)
            piece,vel = (('s',.89),('s',.61),('ss',.91),('s',.85))[j]
            put('snare',at,.8,piece,vel)
        cells = span//CELL
        if section=='the handover':
            # In the middle cell of each group the drum learns just the new
            # mallet attack. The last cell is left intact before the review clip.
            repeats = cells//len(HEADS)
            for j,k in enumerate(HEADS):
                a = start+(j*repeats+repeats//2)*CELL
                rest(('snare',),a,a+CELL)
                stroke(a+k,j)
        elif section=='where it was':
            # State the four on the holes of the low riff, then hear them with
            # no strings or kick for one cell. The quarter hat never disappears.
            # Both cells are well after the 65–71.875 s comparison.
            for i in (cells-4,cells-3):
                a=start+i*CELL
                rest(('snare',),a,a+CELL)
                if i==cells-3: rest(('left','right','bass','kick'),a,a+CELL)
                for j,k in enumerate(HEADS): stroke(a+k,j)
        elif section=='both sides':
            # The last negative has a beat of silence: don't fill it. Carry
            # the unplayed fourth stroke to the actual low F of the slow coda.
            a = start+span-CELL
            rest(('snare',),a,a+CELL)
            for j,k in enumerate(HEADS[:-1]): stroke(a+k,j)
        elif section=='one impression':
            stroke(start+2*HEADS[-1],len(HEADS)-1)

    start = 0
    for section, span in FORM:
        marks[section] = (start, span)
        if section == 'chalk':
            # Four little statements at the bar line, a spare slot to breathe.
            for b in range(span // BAR):
                for j, k in enumerate(HEADS):
                    t = start + b * BAR + k
                    put('ring', t, 1.6, F + 36 + TUNE[j], .83 if j == 0 else .7)
                    if b >= 2:
                        put('glass', t, 1.75, F + 24 + TUNE[j], .79)
                if b >= 1:
                    drums('ft', start + b * BAR, .52 + b * .08)
        elif section == 'under glass' and recover:
            recovery(start, span)
        elif section == 'one impression':
            # The four-note song, its proportions intact, twice as slow. No triplet ticks.
            for j, k in enumerate(HEADS):
                t, p = start + 2*k, F + TUNE[j]
                dur = (span - 2*k - .2) if j == 3 else 2.8
                guitars(t, p, dur, .95, fifth=True)
                put('bass', t, dur, p, .93)
                put('ring', t, dur, p + 36, .86)
                drums('k', t, 1)
                if j == 3:
                    drums('c', t, .85)
                    if unsaid and unsaid['end']:        # v23: the word left out at 3:12.9 is the song's last
                        put('unsaid', t, unsaid['end'][0], p + unsaid['up'], unsaid['vel'], ph=said['ph'][said['words'][3]])
                        if unsaid['end'][1]:
                            parts['unsaid'][-1]['gain'] = f"{unsaid['end'][1]:g}dB"
        else:
            assert span % CELL == 0 and span % BAR == 0
            # Kit is on bar time, not cell time. Two distinct feels either side of the break.
            for beat in range(span // SUB):
                t, q = start + beat*SUB, beat % 4
                if phrase_return and section == 'both sides' and t >= start+span-SUB:
                    continue
                if section == 'under glass':
                    if q in (0, 2):
                        drums('ft' if q == 0 else 't2', t, .55 if q == 0 else .4)
                    continue
                if q == 2 or (section in ('the handover', 'turn the sheet', 'both sides') and q == 0 and beat > 0 and beat % 8 == 4):
                    drums('s', t, .98 if q == 2 else .73)
                cym = 'rde' if section in ('lit through','turn the sheet') else 'h'
                if beat == 0 and section not in ('where it was',):
                    drums('c', t, .76)
                elif section == 'both sides' and q == 0:
                    drums('x', t, .59)
                else:
                    drums(cym, t, .66 if q == 0 else .52)
                if section == 'turn the sheet' and beat % 2:
                    drums('h', t + 2, .43)
            if phrase_return and section == 'both sides':
                last_exchange(start, span)
                if drum_memory: hands_remember(start, span, section)
                start += span
                continue
            half = span // CELL // 2
            for i in range(span // CELL):
                # Halfway through 'lit through' the same four scale tones sit over Ab; the
                # subsequent return of low F should therefore feel like a physical drop.
                on_ab = section == 'lit through' and i >= half
                pedal = F + (3 if on_ab else 0)
                # The seven chugs needn't be duplicated by the entire band.
                # Bass keeps the little strokes on the way out; kick keeps them
                # on the way back. The two guitars frame opposite ends of each gap.
                # (v11: the first cell's gap is now empty, so the cell that states
                # the first group in full, as v8 left the first cell, is the second.)
                lead_in = edges and section=='the handover' and int(hole)<i<span//CELL-1
                follow = edges and section=='lit through' and i>0 and not on_ab
                # v10: in the side-to-side trade the right player's turns are the
                # back of the sheet. Front and back make one palindrome of two
                # cells, in pitch and in spacing; the holes, the box and the foot
                # mirror with it. The last pair of cells stays as written.
                back = turned and section == 'turn the sheet' and i % 2 == 1 and i < span//CELL - 2
                # v11: THE HOLE COMES FIRST. A note passes to the ring every third
                # cell, and until now the muted strokes it buys were there at once:
                # the gap was never heard empty. Now the cell in which a note is
                # given away leaves its gap EMPTY (two ticks, then three, then one
                # and one): the guitars, the bass and the foot let go, and you hear
                # where it was, with the ring sounding across it. The strokes arrive
                # the cell after, where the snare learns that note (v7). The first
                # hole is the handover's own downbeat: crash, ring, and no band
                # until the C.
                # (Two fuller forms were benched and are not here. The ring striking
                # each note WITH the guitars the cell before: 14 to 17 dB under the
                # chord, not heard. The band resting for the whole cell when the last
                # note goes: the scorer's first heavy section stopped matching its
                # return, 100 -> 88.5 and 77.7, and it is a second cell without the
                # band before the first, at 1:25, has been heard.)
                given = hole and section == 'the handover' and i % 3 == 0
                # v12: in 'where it was' every stroke of the negative sat on low
                # F. After the three cells on the review card, each gap takes the
                # note that lies between the two missing notes around it: two
                # D-flats, three B-flats, a G, and F where nothing lies between.
                # So the strokes come down the scale and the holes are the steps
                # they skip. Two cells at a time: the bass alone under both
                # guitars' F, then the left guitar with it, then both, the last
                # of those being the cell where the snare says the four holes
                # (the whole scale, drum and strings in turn). After the cell
                # with no band the negative is on F again, for the bass to start
                # the tune from in the quiet middle.
                learned = (i - 3) // 2 if mold and section == 'where it was' and 3 <= i <= 8 else -1
                if fused and spin and section == 'turn the sheet' and i in fused['cells']:
                    both_faces(start + i*CELL, fused['cells'].index(i))
                    continue
                heads, tune = (BACK_HEADS, BACK_TUNE) if back else (HEADS, TUNE)
                for j, k in enumerate(heads):
                    t, p = start + i*CELL + k, F + tune[j]
                    end = heads[j+1] if j+1 < len(heads) else CELL
                    hand = section == 'the handover' and j < 1 + i // 3
                    overt = section == 'the shape' or (section == 'the handover' and not hand)
                    shadow = section == 'where it was' or hand
                    if overt:
                        # v20: in the last cells of 'the shape' one more note a cell is a fifth, top down
                        whole = made_whole and section == 'the shape' and 0 < j <= i - (span//CELL - 1 - made_whole['cells'])
                        guitars(t, p, min(2, end-k-.25), .98 if j == 0 else .89,
                                fifth=(j == 0) or bool(whole))
                        put('bass', t, min(2, end-k-.2), p, .92)
                        drums('k', t, .99 if j == 0 else .86)
                    empty = given and j == i // 3
                    assert not empty or hand
                    if lit and section == 'lit through' and 0 < i < span//CELL - 1:
                        # v14: LIT THROUGH. The tune has only ever been points: a
                        # strike that dies. Here, where it comes back over its own
                        # negative, a hand is on the ring and each note is held
                        # until the next: the four points are one line. The first
                        # cell is struck as before (the return as it was), and in
                        # the last the hand lets go, so the sheet turns on a struck
                        # ring and its tail, as it did.
                        put('held', t, end-k-.04, p+36, .91 if j == 0 else .79)
                        if glint and glint['cells'][0] <= i <= glint['cells'][1]:
                            # v24: each held note begins as a touched harmonic on the clean guitar, at the
                            # held note's own pitch, and rings under the hand until the next
                            first, last = glint['cells']
                            put('glint', t, end-k-.1, p + 36 - 12 * {2: 1, 4: 2}[glint['node']], glint['vel'])
                            g = glint['grow'][0] + (glint['grow'][1] - glint['grow'][0]) * (i - first) / max(1, last - first) + glint['lift'][j]
                            if g:
                                parts['glint'][-1]['gain'] = f'{g:g}dB'
                    elif hand or section == 'lit through' or (section == 'turn the sheet' and i % 2 == 0):
                        # across a hole the ring is let ring up to the next note
                        put('ring', t, end-k-.25 if empty else 1.45, p+36, .91 if j == 0 else .79)
                    if verso and back:
                        # v26: the back of the sheet has a struck voice of its own, in wood
                        put('bars', t + verso['late'], verso['len'], p + verso['up'], verso['vel'][0] if j == 0 else verso['vel'][1])
                    if section == 'under glass':
                        # Rebuild the tune from its LOW end while the clean string holds dyads.
                        if j >= 3 - i//3:
                            put('bass', t, end-k-.2, p, .89)
                            put('ring', t, 1.7, p+24, .71)
                        if j == 0:
                            dyad = ('F3,C4', 'Ab3,Eb4', 'Eb3,Bb3')[i // 4]
                            put('glass', t, CELL-.8, dyad, .82)
                    if section in ('lit through','turn the sheet','both sides'):
                        # Hocket from side to side, then both shapes in the same stereo space.
                        if section == 'turn the sheet':
                            guitars(t, p, 1.4, .94, rigs=(sides[face(i, j)],), fifth=j in (0,3))
                        elif section == 'both sides' and i % 2 == 0:
                            guitars(t, p, end-k-.35, .99, fifth=True)
                        if section != 'both sides' or i % 2 == 0:
                            put('bass', t, end-k-.3, p if section != 'lit through' else pedal, .90)
                        if section == 'both sides' and i % 2 == 0:
                            drums('k', t, .98)
                        shadow = section != 'both sides' or i % 2 != 0
                    if afterimage and on_ab:
                        # On Ab the holes coalesce into four strokes of lengths
                        # 2, 3, 1, 1. Keep the mallet's four actual places empty
                        # on both strings: the right strings first echo its pitch,
                        # then anticipate the NEXT pitch in the same gap.
                        turn = i-half
                        lead = turn >= half//2
                        borrowed = F + 12 + TUNE[(j + int(lead)) % len(HEADS)]
                        length = end-k-1
                        guitars(t+1, borrowed, length-.23, .95, ('right',))
                        # Give the first two answers the old clipped pulse. Then
                        # the low guitar and foot strike each group only once.
                        for n in range(length if turn<2 else 1):
                            dur = .61 if turn<2 else length-.30
                            guitars(t+1+n, pedal, dur, .94 if not n else .76,
                                    ('left',), mute=turn<2 or length==1)
                            drums('k',t+1+n,.93 if not n else .73)
                        continue
                    if shadow and not empty:
                        opposite = (sides[1-face(i, j)],) if section == 'turn the sheet' else sides
                        for n in range(k+1, end):
                            a = start + i*CELL + n
                            reinforce = (not lead_in or n==end-1) and (not follow or n==k+1)
                            piece = box_stroke(i,span//CELL,k,n,end) if wood and section=='turn the sheet' else None
                            if piece:
                                put('box-'+opposite[0], a, .65, piece, .90 if piece=='cs' else .80)
                            elif reinforce:
                                for rig in opposite:
                                    moved = learned > sides.index(rig)
                                    guitars(a, F + BETWEEN[j] if moved else pedal, .61, .94 if n == k+1 else .76, (rig,), mute=True)
                            if section in ('where it was','the handover','both sides'):
                                put('bass', a, .65, F + BETWEEN[j] if learned >= 0 else pedal, .82 if n == k+1 else .68)
                            if (not lead_in or reinforce) and (section != 'turn the sheet' or n == k+1):
                                drums('k', a, .93 if n == k+1 else .73)
            if held_back and section=='the shape':
                old_fourth_beat(start)
            if made_whole and section == 'the shape':
                # v20: the last bar lines before the landing, on the floor tom and the foot
                for n, vel in enumerate(made_whole['tom']):
                    t = start + span - (len(made_whole['tom']) - n) * BAR
                    drums('ft', t, vel)
                    if not any(abs(e['at'] * SUB - t) < 1e-6 for e in parts['kick']):
                        drums('k', t, made_whole['foot'])
            if section in ('the shape','under glass','turn the sheet'):
                for off, piece in zip((3,2,1), ('t1','t2','ft')):
                    drums(piece, start + span - off, .59+(3-off)*.1)
        if drum_memory and section in ('the handover','where it was','one impression'):
            hands_remember(start, span, section)
        start += span

    def track(tr, patch, gain, pan=0, **kw):
        ns = sorted(parts.pop(tr), key=lambda n:n['at'])
        assert ns and all(n['at'] >= 0 and n['at'] < start/SUB for n in ns)
        return dict(name=tr, patch=patch, gain=f'{gain}dB', pan=pan, notes=ns, **kw)
    tracks = [track('left','ct-twin fx.2.cone=73',1,-.9),
              track('right','ct-twin fx.1.model=gojira fx.2.cone=74',1,.9),
              track('bass','ct-bass',band['bass'][0],fx=band['bass'][1]) if band else
              track('bass','ct-bass',-.5,fx=[{'type':'eq','bands':['hp cutoff=29','peak cutoff=320 q=1 gain=-4dB']}]),
              track('ring','scanned-mallet',-13,.06,sends={'chamber':'-12dB'}),
              track('glass','ct-clean',-2,-.18,sends={'chamber':'-9dB'}),
              track('kick','ct-kit-where-it-was' if band else 'ct-kit',band['kick'][1] if band else 2,
                    out='drums',fx=[{'type':'eq','bands':['peak cutoff=4300 q=0.8 gain=7dB']+([band['box']] if band else [])+
                                                 ([hat['kick']] if hat else [])}]),
              # The short wooden click and the flam grace were 21–26 dB
              # under the accent on the stock kit. Bring up those two pieces
              # only; the old backbeat and its fader stay where they were.
              track('snare','ct-kit'+(' kit.ss.gain=7dB kit.g.gain=-5dB' if drum_memory else ''),3,
                    out='drums',sends={'chamber':'-14dB'},**({'fx':[{'type':'eq','bands':[band['box']]}]} if band else {})),
              track('metal','ct-kit'+(f" kit.h.gain={hat['gain']}dB" if hat else ''),1.5,out='drums'), track('skins','ct-kit',3,out='drums')]
    if rim:
        # The library's FM glass pad, made to speak and stop like a rubbed rim:
        # 160 ms in, 220 ms out, its own long hall nearly shut (the song's
        # chamber carries it, as it carried the guitar it replaces). Benched
        # at -9 dB the tone WAS the bridge (+2.8 dB on the section); at -18 it
        # holds just under where the pluck's attack stood and the section
        # is within 0.2 dB of v8.
        tracks.append(track('rim','pad-glass synth.amp.a=160ms synth.amp.r=220ms synth.env.glint.a=300ms '
                            'synth.env.glint.r=220ms fx.1.mix=0.05',rim_gain,-.18,sends={'chamber':'-9dB'}))
    if wood:
        for side,pan in zip(sides,(-.58,.58)):
            tracks.append(track('box-'+side,'cajon kit.cb.pitch=F2 kit.cs.gain=4dB kit.cg.gain=1dB fx.0.mix=0.06',wood_gain,pan))
    if fretless:
        # The library's fretless on the same notes read 8.5 dB over the picked
        # bass and 16 to 30 dB over it above 500 Hz (a bridge pickup, a bright
        # room): a different lead, not the same bassist. Closed above 1.8 kHz,
        # a slower slide than the patch's so the three finds are heard, no chorus.
        # At -9 dB it stood 1.5 dB over the picked line (K) and the section
        # gained 1.5 dB at 250-500 Hz, where it already read 4 over the
        # records: so -10, and the picked bass's own dip at 320 Hz.
        tracks.append(track('fretless','fretless-bass play.glide=150ms fx.2.mix=0',fretless_gain,0,
                            fx=[{'type':'eq','bands':['hp cutoff=29','peak cutoff=320 q=1 gain=-4dB','lp cutoff=1800 q=0.6']}]))
    if said:
        tracks.append(track('said', said['patch'], said['gain'], said['pan'], sends={'chamber': said['send']},
                            **({'fx': said['fx']} if said['fx'] else {})))
    if glint:
        tracks.append(track('glint', glint['patch'], glint['gain'], glint['pan'], sends={'chamber': glint['send']},
                            **({'fx': glint['fx']} if glint['fx'] else {})))
    if unsaid:
        tracks.append(track('unsaid', unsaid['patch'], unsaid['gain'], unsaid['pan'], **({'fx': unsaid['fx']} if unsaid['fx'] else {})))
    patches = {}
    if band:
        patches['ct-kit-where-it-was'] = {'extends': 'ct-kit', 'kit': {'k': band['kick'][0]}}
    if lit:
        # The song's own ring (the library's scanned-mallet: the same strike,
        # speed and smoothing) with the one thing a mallet has not got: a hand.
        # The engine's scanned `push` holds the ring toward the strike's shape,
        # so the note neither dies nor mellows while it is held; how firmly is
        # how bright. The lane `hand` leans in over the F cells (round, then
        # the middle ripples) and a little further over A-flat. No other song
        # on the record uses `push`.
        # Benched at -19 dB the held notes' fundamentals stood level with the
        # band at their pitch (the struck ring's stand 1 to 7 dB over it in the
        # strike); at -16 they stand 1 to 7 over for the whole note, the line
        # is 16 dB under the mix at 2:02 and 12.5 under at 2:25 as the hand
        # firms, and the section is within 0.11 dB of v13.
        a, span = marks['lit through']
        soft, firm, most = (float(x) for x in grip.split(':'))
        b = lambda cell: f'{(a + cell*CELL)/SUB:g}b'
        cells = span // CELL
        patches['wiw-held'] = {
            'about': "Where It Was: the ring, held (chirper-alpha, 18 Nov). The song's scanned mallet with a hand on it: `push` holds the ring of masses toward the strike's shape, so a note sings until it is let go instead of dying. The lane `hand` is how firmly: about 0.1 keeps only the broad shape (round), 0.5 the middle ripples (bright).",
            'synth': {'layers': [{'type': 'scanned', 'decay': '3s', 'scanned': {'speed': 1.6, 'width': 0.08, 'smooth': 0.5,
                                  'push': {'value': 0, 'mod': [{'src': 'auto.hand', 'amount': 1}]}}}],
                      'amp': {'a': '1ms', 'd': 0, 's': 1, 'r': '260ms'}},
            'gain': '-2.3dB'}
        tracks.append(track('held', 'wiw-held', held_gain, .06, sends={'chamber': '-12dB'},
                            auto={'hand': {'curve': 0, 'points': [['0b', soft], [b(1), soft], [b(cells//2), firm],
                                                                    [b(cells-2), most], [b(cells-1), most]]}}))
    if verso:
        tracks.append(track('bars', verso['patch'], verso['gain'], verso['pan'], sends={'chamber': verso['send']},
                            **({'fx': verso['fx']} if verso['fx'] else {})))
        if verso['ring']:
            a, span = marks['turn the sheet']
            ring = next(t for t in tracks if t['name'] == 'ring')
            ring['gain'] = {'value': ring['gain'], 'mod': [{'src': 'auto.face', 'amount': 1}]}
            ring['auto'] = {'face': {'curve': 0, 'points': [['0b', 0], [f'{(a - 1) / SUB:g}b', 0], [f'{a / SUB:g}b', verso['ring']],
                                                           [f'{(a + span - 1) / SUB:g}b', verso['ring']], [f'{(a + span) / SUB:g}b', 0]]}}
    assert not parts
    return {'about':'Where It Was. A four-note tune on eleven triplet eighths; the band learns to play its negative. Common Time t13 '+('v17.' if trades else 'v16.' if refill else 'v15.' if spin else 'v14.' if lit else 'v13.' if fretless else 'v12.' if mold else 'v11.' if hole else 'v10.' if turned else 'v9.' if rim else 'v8.' if edges else 'v7.' if drum_memory else 'v6.' if afterimage else 'v5.' if held_back else 'v4.' if wood else 'v3.' if recover else 'v2.' if phrase_return else 'v1.'),
            'tempo': BPM, 'seed': 1, 'event_stable': True, 'length':f'{start//SUB}b', 'tail':'3s',
            # v16: nine ring notes make the whole song 0.01 LU louder to the meter, so at -10 every other bar
            # (the five card excerpts among them) came out 0.008 to 0.011 dB quieter: the target moves by that.
            # v17: the trade is quieter to the meter than the long statement it replaces; -10.035 keeps every other
            # bar at v16's mastering gain (within 0.002 dB, both seeds).
            'ceiling':'-1dB', 'true_peak':True, 'loudness':glint['loudness'] if glint else unsaid['loudness'] if unsaid else said['loudness'] if said else fused['loudness'] if fused else made_whole['loudness'] if made_whole else hat['loudness'] if hat else band['loudness'] if band else -10.035 if trades else -9.99 if refill else -10,
            'buses':{'drums':{'fx':['reverb kind=room decay=0.45s mix=0.07',
                                     'glue threshold=-22dB ratio=2 attack=18ms release=120ms',
                                     {'type':'eq','bands':['peak cutoff=390 q=0.9 gain=-4dB','lp cutoff=14800']}]},
                     'chamber':{'fx':['reverb kind=chamber mix=1 decay=1.1s predelay=14ms low_cut=280 high_cut=7200']}},
            'master':{'fx':[{'type':'eq','bands':['hp cutoff=25']}]}, **({'patches': patches} if patches else {}), 'tracks':tracks}


# v27 (chirper-one; instrument round: the bass drum, 368 strokes; no stroke moves): THE BASS DRUM GETS A CHEST.
# v25's handoff put the kick first: "the kit is still +6.0 at 500 Hz-1 kHz by part and the snare is not why". Read
# alone beside six records' bass drums by thirds of an octave (kickspec.py, new this round, a twin of
# tools/snarespec.py; in ~/.local/state/chirper-one/common-time/t13-v27/), the kick's middle is NOT why either:
# its knock against its thump (400 Hz-1.6 kHz less 40-125 Hz) reads -25.0 where the records' stems read -25.9 at
# their kicks. What it lacks is what chirper-alpha found on Take Up the Slack (v11 there): NOTHING AT 90-120 Hz
# (-31.3 dB as a share of its own 35-250 Hz; the records' median -13.6, the leanest -19.4). The drum is one sine
# at 58 Hz and its odd harmonics (175, 291 Hz: the patch's drive), so on anything that cannot play 58 Hz it is a
# click and a buzz. Now each stroke has a CHEST: a bare sine an octave over the drum (B flat 2, 116.5 Hz), 90 ms,
# on a track of its own (`chest`), outside the drums' bus. Alone the drum reads -15.1 there now. THE LEVEL WAS
# CHOSEN ON THE FINISHED FILE: at -6 dB a stroke lifted the mix's 90-140 Hz by 3.3 dB in 'the shape' and only 0.8
# to 1.7 in the five denser sections; at -3 dB, 5.4 and 1.8 to 2.9. The mix's read against the eleven records is
# the same either way (no section moves more than 0.05).
# WHAT DID NOT WORK, so nobody tries again: the same as the patch's own knock layer (ratio 2, 70 ms, up to +10 dB:
# 90-120 Hz stayed at -31 to -32: the patch's drive is one ceiling, as alpha found) ; a smaller pitch sweep or a
# shorter one (the low middle rose) ; AND A SHORTER TAIL: the drum falls 20 dB in 79 ms where the records take 37
# to 49, and at 140 ms of decay it fell in 45, but the finished mix lost 0.8 to 1.6 dB under 60 Hz in all six band
# sections (four of them were already short there), read worse against the eleven records in four, and recurrence
# fell 100 -> 95 on both seeds. The tail holds part of this song's sub (the bass's root is F1, under the drum): it
# stays. A cut at 230 Hz went with that take and is not kept either (no gain on the mix's read).
# 'chest': its note, its fader (dB), its decay (ms), its envelope's curve (None: no chest) ; 'tail': the drum's own
# decay (None: the kit's 210 ms) ; 'eq': the kick's track eq (None: as it was) ; 'gain' ; 'loudness' (None:
# unchanged). --v26 restores v26. (--kick '{"chest": ["A#2", -3, 90, 3]}': fields changed for a bench.)
KICK = {'chest': ('A#2', -3.0, 90, 3), 'tail': None, 'eq': None, 'gain': None, 'loudness': None}


def the_kick_gets_a_chest(doc):
    """v27: each stroke of the bass drum has a chest: a bare sine an octave over the drum, on a track of its own."""
    kick = next(t for t in doc['tracks'] if t['name'] == 'kick')
    if KICK['tail']: kick['patch'] += f" kit.k.patch.synth.amp.d={KICK['tail']}"
    if KICK['eq']: kick['fx'] = [{'type': 'eq', 'bands': list(KICK['eq'])}]
    if KICK['gain']: kick['gain'] = KICK['gain']
    if KICK['chest']:
        note, gain, d, curve = KICK['chest']
        doc['patches'] = {**doc.get('patches', {}), 'wiw-chest': {'extends': '808', 'synth': {'layers': ['sine'], 'pitch': {'value': 0, 'mod': []}, 'drive': 0, 'filters': [],
                          'amp': {'a': '2ms', 'd': f'{d:g}ms', 's': 0, 'r': '20ms', 'curve': curve}}, 'play': {'mono': False, 'glide': '0ms', 'gate': 1}}}
        chest = {'name': 'chest', 'patch': 'wiw-chest', 'gain': f'{gain:g}dB', 'pan': 0,
                 'notes': [{'at': n['at'], 'len': round(d / 1000 * BPM / 60, 4), 'pitch': note, 'vel': n['vel']} for n in kick['notes']]}
        doc['tracks'].insert(doc['tracks'].index(kick) + 1, chest)
    if KICK['loudness']: doc['loudness'] = KICK['loudness']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT)
    previous = parser.add_mutually_exclusive_group()
    previous.add_argument('--v1', action='store_true', help='reproduce the original alternating-cell return')
    previous.add_argument('--v2', action='store_true', help='restore the sustained glass and doubled bass in the clean middle')
    previous.add_argument('--v3', action='store_true', help='restore both guitar parts in the side-to-side trade')
    previous.add_argument('--v4', action='store_true', help='keep the two guitars in unison through the first heavy section')
    previous.add_argument('--v5', action='store_true', help='restore the seven muted strokes over the A-flat pedal')
    previous.add_argument('--v6', action='store_true', help='restore the original backbeat in the negative and its returns')
    previous.add_argument('--v7', action='store_true', help='restore the doubled chugs on both sides of the break')
    previous.add_argument('--v8', action='store_true', help='restore the plucked clean dyads in the quiet middle')
    previous.add_argument('--v9', action='store_true', help='restore the falling tune on every turn of the trade and before the close')
    previous.add_argument('--v10', action='store_true', help='restore the muted strokes in the cell where each note is handed over')
    previous.add_argument('--v11', action='store_true', help='restore low F under every stroke of the negative')
    previous.add_argument('--v12', action='store_true', help='restore the picked bass in the quiet middle')
    previous.add_argument('--v13', action='store_true', help="restore the struck ring through 'lit through'")
    previous.add_argument('--v14', action='store_true', help='restore one side a cell through the whole side-to-side trade')
    previous.add_argument('--v15', action='store_true', help='restore the empty holes in the four short negatives of the last exchange')
    previous.add_argument('--v16', action='store_true', help='restore the one long statement at the return and the rising phrase before the close')
    previous.add_argument('--v17', action='store_true', help='restore the band before it was read part by part (the bare bass, the library kick, the guitars as the rig comes)')
    previous.add_argument('--v18', action='store_true', help='restore the hi-hat at the cymbals\' fader, 25 dB under the mix, and the kick with its top')
    previous.add_argument('--v19', action='store_true', help='restore the single notes of the tune in the three cells before the handover, and their bar lines unmarked')
    previous.add_argument('--v20', action='store_true', help='restore the side-to-side trade turning twice a cell for two cells and at every note for two, one face at a time')
    previous.add_argument('--v21', action='store_true', help="restore the quiet middle with nobody singing")
    previous.add_argument('--v22', action='store_true', help="restore 'both sides' with nobody singing as the ring brings the tune back")
    previous.add_argument('--v23', action='store_true', help="restore the held line of 'lit through' without a harmonic on each of its notes")
    previous.add_argument('--v24', action='store_true', help="restore the album's snare as it comes: a tone higher, shorter, with its box")
    previous.add_argument('--v25', action='store_true', help="restore the back of the sheet with no struck voice of its own (no wooden bars)")
    previous.add_argument('--v26', action='store_true', help="restore the album's bass drum as it comes: no chest, its long tail")
    parser.add_argument('--verso', help='a bench: VERSO fields to change, as a JSON object')
    parser.add_argument('--kick', help='a bench: KICK fields to change, as a JSON object')
    parser.add_argument('--said-gain', type=float, default=None, help="the sung voice's track gain in dB (default: SAID's)")
    parser.add_argument('--said-takes', default=None, help="which of each group's three cells is sung, e.g. 1 or 1,2 (default: SAID's)")
    parser.add_argument('--wood-gain', type=float, default=-12, help='cajon track gain in dB')
    parser.add_argument('--rim-gain', type=float, default=-18, help='held glass track gain in dB')
    parser.add_argument('--fretless-gain', type=float, default=-10.0, help='fretless bass track gain in dB')
    parser.add_argument('--held-gain', type=float, default=-16.0, help='held ring track gain in dB')
    parser.add_argument('--grip', default='0.12:0.55:0.7', help="how firmly the hand holds the ring: at 2:02 : at the A-flat : at its most")
    parser.add_argument('--strokes-on-f', action='store_true', help="keep low F under every stroke of the fourth short negative (the ring's refill only)")
    args = parser.parse_args()
    if args.verso:
        VERSO.update(json.loads(args.verso))
    doc = compose(not args.v1, not args.v2, not args.v3, args.wood_gain, not args.v4, not args.v5, not args.v6, not args.v7,
                  not args.v8, args.rim_gain, not args.v9, not args.v10, not args.v11, not args.v12, args.fretless_gain,
                  not args.v13, args.held_gain, args.grip, not args.v14, not args.v15, not args.strokes_on_f, not args.v16, not args.v17,
                  not args.v18, not args.v19, not args.v20, not args.v21, args.said_gain, args.said_takes, not args.v22, not args.v23,
                  not (args.v24 or args.v25))
    if not args.v24 and any(t['name'] == 'glint' for t in doc['tracks']):     # only on the whole song as v24 has it
        the_snare_rings_lower(doc)
        if not args.v25 and VERSO['loudness']:
            doc['loudness'] = VERSO['loudness']
    if args.kick:
        KICK.update(json.loads(args.kick))
    if not any(v for k, v in vars(args).items() if k[0] == 'v' and k[1:].isdigit()) and any(t['name'] == 'bars' for t in doc['tracks']):   # only on the whole song as v26 has it
        the_kick_gets_a_chest(doc)
    # Same line-oriented YAML as the other generators: JSON flow values, one track per line.
    args.out.write_text('\n'.join(k+': '+json.dumps(v) if k!='tracks' else
                        'tracks:\n'+'\n'.join('  - '+json.dumps(t) for t in v) for k,v in doc.items())+'\n')
