#!/usr/bin/env python3
"""chirpers VIII, track 8 (chirper-zero): delay-line memory.

The first stores kept their words as sound travelling down a tube and played back into itself. This track is that
sound, heard from inside: ONE 16-bit word (the melody) is written once, then only ever recirculates - round a long
feedback line, a little worn each pass. A few bits flip as it goes (a seeded error rate that climbs), and every so
often a REFRESH rewrites the word from what is left (a majority vote of its last passes), so the tune mutates by
decay and repair and never quite repeats.

Tuning: a STRETCHED OCTAVE (each octave ~1210 cents, like a piano's inharmonic stretch): every pitch is written as
an absolute frequency, so unisons, fifths and octaves are all a hair wide - subtly off.

  INTRO 16     the word written: the FM chime alone into the line (1 bar), dry pads, the stretch audible
  A 36         the 909 and the 808 enter; the word goes round, its error rate climbing 0 -> 0.10
  REFRESH 8    the tape stops, the pad freezes, the word is rewritten from its last four passes
  C 32         the second groove: the refreshed word, the line's echoes torn into grains (cloud)
  D 16         corruption: the word stutters and chops, the errors at their worst
  E 28         repaired: the last groove, the word nearly itself again
  OUTRO 16     only the line: the echoes go round without the source until the tape runs out

Generated; edit and re-run:  python3 compose/chirpers8/src/chirpers8-t8.py
"""

import json
import re
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.environ.get("C8T8_OUT") or os.path.join(ROOT, "songs", "chirpers8-t8.yaml")

BPM = 118
BAR = 16
STRETCH = float(os.environ.get("C8T8_STRETCH", "1210")) / 1200   # cents per octave / 1200
SEED = 8
HUM = os.environ.get("C8T8_HUM", "8")    # the store powering up: a low D hum (808, stretched D1) under the first intro bars, fading as the word is written; value = bars
HUMA = os.environ.get("C8T8_HUMA", "4")   # the hum starts on A1 (t7's drone, the fifth of D) and falls to D1 after this many bars: the seam is one held A that resolves
SHAKE = os.environ.get("C8T8_SHAKE", "40")  # the line's own clock: a dusty shaker on every sixteenth through the grooves (A, C, E), accents on the off-sixteenths - the high, fine grain of the floor; value = velocity
DARKPOS = os.environ.get("C8T8_DARKPOS", "end")  # 'end': the tape-running-out low-pass goes LAST on the master (it sat first, so the master tape's hiss was added after it and the tail stayed bright: +36 dB at 10-15 kHz over t9's head)
LZ = os.environ.get("C8T8_LZ", "1.5")   # the line's wear wanders: a Lorenz attractor (a var, stepped every beat) drives the line tape's `warp` (its wow and flutter depth), 0 up to LZ - the memory degrades unevenly, never the same way twice
VOX = os.environ.get("C8T8_VOX", "-18")   # a spoken word into the store: a humanized voice speaks into the store - v22: 'nothing is kept.' / 'nothing is kept. it only goes around.' / 'it only goes around.' (WORDS; was 'say it back to me') - (intro bar 9, the refresh's second bar, the outro's first) and is sent hard into the line, so the words go round and wear away with the tune; value = dry gain dB
OUTPAD = os.environ.get("C8T8_OUTPAD", "88")   # the pads stay up through the outro's last eight bars (velocity OUTPAD, low voicing kept), so the dark tail still holds 300-470 Hz for t9's glass pads to land on
CHOP = os.environ.get("C8T8_CHOP", "1")   # recall, corrupted: through D the word's previous bar comes back CHOPPED (8 slices, '0 r1 2 2 . r5 6 _': repeats, reversals, a hole, a glimpse of the live bar) - memory read back wrong
VINYL = os.environ.get("C8T8_VINYL", "") # the medium wears: vinyl on the line - crackle 0.05 rising to 0.35 into D, 0.15 for the repair, 0.5 in the outro where the line is alone; dust 0.3, wear 0.3
EQFIX = os.environ.get("C8T8_EQFIX", "2")   # (a measurement) the master toward the album's colour: -3 dB at 150 Hz, +4 dB at 1 kHz and 3 kHz, no +2 dB air shelf
ORGAN = os.environ.get("C8T8_ORGAN", "")   # the operator's console: a reedy combo organ pulsing eighths on the chord's two upper tones an octave up (stretched, two voices) through A, C and E - minimalist machine-pulse in the 1-3 kHz the track lacked; value = velocity
OUTUP = os.environ.get("C8T8_OUTUP", "")   # the memory floats up as it fades: the outro's last eight bars voice the pads an octave higher (the 290-470 Hz t9's glass pads open in)
HUMOCT = os.environ.get("C8T8_HUMOCT", "55")   # the A hum doubled an octave up (A2, ~110 Hz: where t7's drone is strongest) for its four bars - velocity
EQ3 = os.environ.get("C8T8_EQ3", "1")   # the last narrow holes against the album envelope: +5 dB at 1.03 and 3.08 kHz (q 3), +3 dB around 100 Hz, -2.5 dB at 1.65 kHz
WORDEND = os.environ.get("C8T8_WORDEND", "64")   # one last read: the word itself returns, faint, in the outro's last four bars (the line had been alone) - its 300-900 Hz chime meeting t9's head; value = velocity
SUNG = os.environ.get("C8T8_SUNG", "-16")   # the words become a song: 'it only travels' (v22, WORDS; was 'say it back to me') SUNG once (tts --sing, A4 F4 D4 E4 D4 on the stretched octave) at the outro's ninth bar, into the line - the memory's last voice is a tune; value = dry gain dB
HEADDARK = os.environ.get("C8T8_HEADDARK", "8")   # the mercury warms up: the master low-pass (the tape-running-out one) also starts closed (~5 kHz) and opens over the first HEADDARK bars - a delay line had to reach its working temperature before it held a word; t7 v7's tail reads my 12-15 kHz air +14-17 dB over it
HEADDARKV = float(os.environ.get("C8T8_HEADDARKV", "0.6"))   # how closed it starts (0.6 ~ 5 kHz, 0.8 ~ 3.3 kHz)
HUMV = int(os.environ.get("C8T8_HUMV", "85"))   # the A hum's 808 velocity: t7 v7's tail sits 5.5 dB under my head
SAYHEAD = os.environ.get("C8T8_SAYHEAD", "move")   # t7 ends with its voice in the room, singing; here the voice answers at once: 'say it back to me' two beats into the record ('move': instead of at bar 9; 'add': as well), into the line as before
BACKREV = os.environ.get("C8T8_BACKREV", "0.6")   # 'say it BACK to me': on the word 'back', every time (spoken and sung), a granular cloud reading the voice's last quarter-second plays it backwards (reverse 1) - the word itself played back the wrong way, as a tape would - swelling in for the word and gone for 'to me'; value = the cloud's peak mix
WORDPRES = os.environ.get("C8T8_WORDPRES", "")   # presence on the melody, not the master: the record still sits 6.2-7.3 dB under the album at 1, 3 and 4.9 kHz; a broad peak (2.5 kHz, q 0.6) of WORDPRES dB on the dx-epiano word
EQ4 = os.environ.get("C8T8_EQ4", "1")   # the three narrow holes left (1025, 3078, 4929 Hz at -6.7/-7.2/-6.2 against the album, neighbours ~0): narrow master peaks (q 4) of +2/+2.5/+1.5 dB x EQ4 - a broad presence lift on the melody overfills 1.6-2.2 kHz instead
WTABLE = os.environ.get("C8T8_WTABLE", "-26")   # the word as a waveform: a wavetable whose frames ARE the stored word - frame per 4 bars, harmonic 1 always, harmonics 2-17 present where the word's 16 bits are set (gain 1/h^0.7) - holding each chord's root an octave up under the band; as bits flip and refresh repairs them the drone's timbre wears and mends with the memory; value = gain dB
WT = {"notes": [], "frames": []}
PLATEHIT = os.environ.get("C8T8_PLATEHIT", "rE")   # the write, struck: when the refresh rewrites the word, a metal plate is struck once (the modal layer's plate modes, a stretched D) and the strike goes into the line, so the write itself goes round the memory; 'r' at the refresh, 'rE' also as the repaired E begins
FILL = os.environ.get("C8T8_FILL", "0.7")   # the memory's continuity illusion: while the refresh rewrites the word (its first 4 bars, the word unread) a follow-noise on the word keeps sounding in the word's own colours (held 8 s from its last notes), so the line seems to run on through the gap - the Huggins/Zwicker fill the engine's follow-noise was made for; value = tone (0 smooth .. 1 pitched, ringing on the word's notes)
WORDS = os.environ.get("C8T8_WORDS", "new")   # 'new': the voices stop asking 'say it back to me' four times (plain, and read 'say listed') and tell what a delay line is, sideways, a different line each time - 'nothing is kept.' (the word written), 'nothing is kept. it only goes around.' (the refresh), 'it only goes around.' (the outro); the sung line becomes 'it only travels' (same tune). voice-spoken, chosen by whisper (the spoken lines read back word-perfect dry)
STRIDE = os.environ.get("C8T8_STRIDE", "C5D7")   # the same bits, read through another address map: the word's bit i sounds scale slot (i x stride) mod 8 - stride 3 everywhere before (D A F | F C A | G D: interlocking leaps); 'C5' reads the refreshed word in C with stride 5 (D D G A C F F A: a new tune from the same data), 'D7' the corrupted D with stride 7 (a leap, then falling down the scale); E is read the old way again (the tune comes home); e.g. 'C5D7'
UPPAD = os.environ.get("C8T8_UPPAD", "mellotron-choir")   # the two upper pad voices' instrument (the lower two stay on juno-pad, which carries the low end): e.g. mellotron-choir - tape-stored voices played back, a memory medium
UPPADGAIN = os.environ.get("C8T8_UPPADGAIN", "-24")
KITOWN = os.environ.get("C8T8_KITOWN", "F1")   # PALETTE: the kick leaves the 909 kit (a staple) for the machine layer's synthesised kick, tuned to KITOWN (a note: 'A1' the dominant, 'D2' the root) - a pitched kick in the song's key
LATER = os.environ.get("C8T8_LATER", "-8")   # WHOLE ROUND: a second sung line, in E - 'it comes later on' (tts --sing "A4/8 G4/8 F4/4 E4/8 D4/2", seed 7; whisper reads it exactly on seeds 3, 5 and 7), sung once at E bar 12 a semitone up with E: what a delay line does, said plainly and sideways - the answer the outro's 'it only travels' completes. Own track, listed last; nearly dry (line -16, room -14). Value = dry gain dB
LATERDROP = os.environ.get("C8T8_LATERDROP", "1")   # with LATER: the word steps aside for the voice - for E bars 12-13 the word, its marimba, the zeros, the hats and the clap are kept at velocity 1 (no dice move), so 'it comes later on' is heard over pads, bass and kick (in the full mix whisper heard nothing; soloed it reads exactly)
HANDS = os.environ.get("C8T8_HANDS", "clap")   # PALETTE: the clap and the rim leave the 909 kit for the machine layer's own synthesised clap and rim ('clap', 'rim', or 'both'): with v36's kick, the kit is the song's own
ECHOCH = os.environ.get("C8T8_ECHOCH", "84")   # SECTION ROUND (w8, E: static): it comes later on - the sung line's tune (A4 G4 F4 E4 D4, as sung at E bar 12) comes back on the tape choir (mellotron-choir, wordless, its own track echoch listed last) four bars later and again four bars after that, softer each time: the delay line handing the phrase back. Lifted with E. Value = first velocity
TUNEKS = os.environ.get("C8T8_TUNEKS", "1:-15")   # SECTION ROUND (w3, A bars 16-31: little new vs w2): the tune circulates before it is sung - the word's sung tune (A4 F4 D4 E4 D4, as sung later) plucked on a Karplus-Strong string (engine 8f150090: a noise burst in a one-period loop, the delay line as an instrument) every four bars through A's second half, quieter each pass, the last pass slower: the memory already holding the tune that the voice will only sing in E. A notes-only track in that window. Value 'blend:gain'
MARKS = os.environ.get("C8T8_MARKS", "0.75")   # SECTION ROUND (E's second half): the word leaves the wood for a delay loop - from E bar 16 the marimba doubling the repaired word (MARE) hands over to Karplus-Strong (engine 8f150090, as published in 1983): a burst of noise circulating in a one-period loop, averaged on each pass until only the tone survives - a recirculating delay line losing its detail, the song's own mercury memory as an instrument. The marimba keeps E's first half (struck by hand), the loop its second (kept by the machine). Value = the loop's blend (1 a string, lower toward the paper's drum)
ROBOSUNG = os.environ.get("C8T8_ROBOSUNG", "-12")   # SECTION ROUND (the later sung line's window): the line is sung back by the machine as well - a vocoder twin of the later sung line (sungl), its words shaping a held D minor chord of saws (D2 A2 D3 F3) band by band: the memory's tune, said back by the machine that keeps it. Value = gain dB
DUFFBASS = os.environ.get("C8T8_DUFFBASS", "700")   # PALETTE: the bass leaves the 808 for the machine's own oscillation - a Duffing oscillator held in its locked regime (amount 0.2: periodic, wM's table), a nonlinear spring ringing at the note's pitch, low-passed: the same system that breaks the word up as it decays (v56), here steady, under it. Value = lp cutoff Hz
WORDWARP = os.environ.get("C8T8_WORDWARP", "0.5")   # WHOLE ROUND: the word arrives late as it decays - a delay line's word comes round on the tank's clock, not the machine's, and drifts as the mercury warms; regeneration re-times it. The word (and its decay double) runs on its own clock (the engine's per-track warp): drifting steadily late through the intro and A (to WORDWARP beats behind the band), re-locked in one bar at the refresh, drifting late again through C, D and E, re-locked at the outro. Value = beats of lag at full decay
DECFIX = os.environ.get("C8T8_DECFIX", "")   # v56's decay double peaks at lane 0.55, which wM's regime table puts in Duffing's locked window (0.4-0.625): it broke up mid-way and then re-locked before each refresh. DECFIX scales its amount so the peak sits in the chaotic band (1.3 x 0.55 = 0.715, inside 0.625-0.85): the word really comes apart just before it is regenerated
SUNGMID = os.environ.get("C8T8_SUNGMID", "16")   # WHOLE ROUND on the singing: the voice is heard before E - 'it comes later on' (the line sung at E bar 12) is first sung in the middle of the song, at C bar SUNGMID, in C's own D minor (E's is lifted a step), with its canon a bar behind a third below (v69): the line promises its own return, and comes later on. Value = bar of C
WORDLEVEL = os.environ.get("C8T8_WORDLEVEL", "3")   # WHOLE ROUND: the word recedes as it decays - the word's orbit (radius 2 + 8 x the decay lane, v60) gets the engine's orbit `level` (8f150090: the distance that plays at full level; farther is fainter, about 1/distance): within WORDLEVEL metres it is as it was; as the memory decays and the orbit widens to 10 m the word grows faint as well as far, then each refresh brings it back up close and full. Value = metres
CANON = os.environ.get("C8T8_CANON", "4")   # WHOLE ROUND on the singing: the memory sings it back - every sung line (sungl at E bar 12, sungv/sungv2 in the outro) is followed by itself CANON beats later, a diatonic third below in D minor on the stretched octave, 6 dB under, panned across, sent hard into the line: a delay line's echo that returns transposed, so each line becomes a two-part canon with its own recall
RIMKS = os.environ.get("C8T8_RIMKS", "-12")   # PALETTE: the pulse in the mercury - the rimshot that ticks through the song (the 909's, an album staple in three songs) becomes a tuned drop, a Karplus-Strong pluck (1983: a delay line fed back through an averaging filter - the same machine as a mercury delay-line memory, a pulse circulating and losing its edge each pass) on D6, the tonic, on the stretched octave: each tick of the rhythm is a pulse going round the line. Value = gain dB
ECHOFOF = os.environ.get("C8T8_ECHOFOF", "")   # (off from v79: the album's FOF wave, not this song's; -20 twin was v77) PALETTE: the choir that answers the sung line in E and sings the tune at half speed in the outro (v42/v44; VOSIM 'oh' since v62) is now CHANT's - Rodet's FOF singing (IRCAM 1979-84, engine 91b04b25: every pitch period one decaying grain per formant, no filters), an alto on 'o' opening toward 'a' over each note, vibrato 5.5 Hz after 300 ms, a small scoop: computer music's own classic singing voice answers the human (Harry's bar: t10's sung passage). Value = gain dB
DUET = os.environ.get("C8T8_DUET", "")   # (off from v79: a copy of t10's duet move, not this song's; 4 was v76) SECTION ROUND (E's sung line, w8): a second singer - 'it comes later on' at E bar 12 is sung as a duet: a separate take (tts --sing "F4/8 E4/8 D4/4 C4/8 A3/2", seed 21, humanize 0.35: mostly a third below, opening onto the fifth at 'on') with the first, a touch behind, on the other side and a few dB under, lifted with E; the canon (v69) still answers a bar later, so the line is three voices - two singing together, the memory a bar behind (Harry, of t10's sung duet: 'that is the bar'). Value = dB under the line
REWRITE = os.environ.get("C8T8_REWRITE", "-18")   # SECTION ROUND (the refresh, 8 bars): the harmonics written back - a delay line loses its detail (the decay's low-pass, chaos and hiss) and regeneration restores it; through the refresh a held D (D3 + D4, the tonic, on the stretched octave) is Chebyshev-waveshaped (Le Brun & Arfib 1979, engine 817a5de6) with its index on a lane rising 0 -> 1 across the eight bars, so it grows from a bare sine to its full harmonic series one harmonic at a time - the word's spectrum rewritten - then lets go as C starts. A notes-only track. Value = gain dB
BRASSA = os.environ.get("C8T8_BRASSA", "-16")   # SECTION ROUND (w2, A's first bars: level jump): the word announced - as the word is first stored (A), its tune (A4 F4 D4 E4 D4, the sung line's) is stated twice on Risset's brass: Chebyshev waveshaping (Le Brun & Arfib 1979, engine 817a5de6) with the index on a breath envelope and velocity, so each note brightens as it is blown and louder is brighter - the computer trumpet Risset made at Bell Labs by analysing a real one. A notes-only track at A bars 0 and 8, on the stretched octave. Value = gain dB
WORDSCAN = os.environ.get("C8T8_WORDSCAN", "18")   # WHOLE ROUND: the word kept in a rippling medium - a mercury delay line stores the word as a wave travelling through matter; scanned synthesis (Verplank, Mathews & Shaw 2000, engine ee46ab71) plays a ring of masses and springs read round at the pitch, its moving shape the timbre. The word (dx-epiano, all song) gets a twin on that ring (static push: the push mod is unstable, reported), with the word's own warp, orbit and lanes, WORDSCAN dB under it: every bit of the word now also ripples in a medium as it is read. Value = dB under the word
SAYARRIVE = os.environ.get("C8T8_SAYARRIVE", "15")   # SECTION ROUND (w1, the intro): the answer arrives - 'say it back to me', t8's first words (answering t7's voice across the seam), spirals in from ~15 m to 1 m over its first three bars (an orbit whose radius lane falls 15 -> 1, with the engine's orbit level, 2 m: far is faint), so the chip voice is heard coming from where t7 left off before it is close. Value = start radius in metres
LPCNUDGE = os.environ.get("C8T8_LPCNUDGE", "")   # v63's lpc 'say' was nudged 0.07 beats early for lpc's lag; engine ee46ab71 compensates, so the nudge is off ('') from v72
SAYLPC = os.environ.get("C8T8_SAYLPC", "plain")   # SECTION ROUND (w1, the intro: static): the first explanation in a speech chip - the intro's spoken line (say, bar 8: what a delay line keeps) goes through LPC (engine 78e838c5): 'plain' (LPC-10, inflecting) or 'toy' (5-bit monotone on D3, the tonic); the later lines (say2 at the refresh, say3 at the outro) stay as they are. Notes 0.07 beats early for LPC's ~35 ms
ECHOVOS = os.environ.get("C8T8_ECHOVOS", "-10")   # PALETTE: the choir that answers the sung line in E and sings the tune at half speed in the outro (v42/v44: mellotron-choir, a tape of voices) is sung by the machine instead - our own VOSIM 'oh' (two pulse trains, F1 ~450 Hz, F2 ~800 Hz, drifting on slow sines, a slow swell): the memory answering in the synthetic voice of the time it would be read back in. Value = gain dB
LINEHISS = os.environ.get("C8T8_LINEHISS", "-44")   # WHOLE ROUND: the line's noise floor - a delay line's signal sinks toward its noise as it decays, and regeneration is what clears it: a high, thin hiss (white noise above 7 kHz, held under the whole song) rides v56's decay lane, rising as the memory decays (up to +12 dB), cleared at the refresh, rising again through C, D and E, cleared at the outro. Value = its base gain dB
WORDFADE = os.environ.get("C8T8_WORDFADE", "8")   # WHOLE ROUND: the word drifts as it decays - v52's orbit (the word circling the listener, a lap every 8 bars) now takes v56's decay lane on its radius (orbit mods, engine 206fbfb8): as the memory decays through the intro and A the word's circle widens and it drifts away from the listener (quieter, darker behind), at the refresh it is back close, it drifts again through C, D and E, and the outro's last refresh brings it home. Value = metres of drift at full decay per unit of the lane
HOOT = os.environ.get("C8T8_HOOT", "-14")   # PALETTE: the program counter (v-era COUNTER: 1..16 in binary through C, on marimba) is played the way the first computers played music - CSIRAC, whose memory was mercury delay lines, played tunes in 1951 by pulsing a loudspeaker straight from its instruction bus: a raw square 'hoot' (a sine bent all the way to a square, phase distortion; short, a little lp), the machine's own voice counting. Value = gain dB
PDPADS = os.environ.get("C8T8_PDPADS", "-23")   # PALETTE: the lower pads (pad0, pad1: juno-pad, an album staple) become Casio CZ phase distortion - a reso_trap whose resonance breathes on a slow sine, the bed of a 1984 home computer under the tape choir above (t2 v53's pad, here in D minor). Value = gain dB
TANKTEMP = os.environ.get("C8T8_TANKTEMP", "3")   # WHOLE ROUND: the tank's temperature - a mercury delay line's delay moves with its temperature (the tanks were kept heated, a thermostat cycling around 40 C), and the machine's clock had to follow it: the tempo now breathes with the thermostat, a slow sine around 118 bpm (a cycle every 16 bars, points every two bars, ramped), so the whole song's clock is very slightly warm and cool by turns. Value = bpm amplitude
DECAY = os.environ.get("C8T8_DECAY", "-22")   # WHOLE ROUND: the memory decays and is refreshed - a delay line loses its bits unless it is regenerated, so the word gets a double on a chaos voice (engine f3872739: a Duffing oscillator, one loop of its two wells per period of the note) whose amount rises all through the intro and A (clean, then the period doubles, then from ~0.35 the voice breaks up between its wells), snaps back to clean at the refresh, decays again through C, D and E, and is refreshed for good at the outro: the word kept, against the physics. Value = gain dB
EBRK = os.environ.get("C8T8_EBRK", "12,4")   # SECTION ROUND (w8, E's first half: static): a breath before the words - E bars EBRK ('start,len') lose the kit (kick, hats, clap, rim, shaker), so the line, the pads and the bass hold alone and the sung line at E bar 16 enters out of the quiet, the drums landing back under it
LIFEPD = os.environ.get("C8T8_LIFEPD", "-28")   # PALETTE: the Life cells (v47: gen life 8x8 on glass, C bar 20 through D) are played on the instrument of the machines that ran Life at home - Casio CZ phase distortion (1984): a sine bent toward a square for an instant on each note and let go (the CZ pluck), so each live cell is a small bright click of a home computer. Value = gain dB
FLYBY = os.environ.get("C8T8_FLYBY", "20,1")   # SECTION ROUND (w9, E's end: little new vs w8): the last read flies past - v46's second readback (E bars 24-27, the word's four notes a semitone up) moves to its own track and passes the listener left to right, one fly-by across the four bars (orbit path=line, engine c7606671), the Doppler drop on each note as it goes by: the memory read out of the line one last time and carried away. Value = 'radius,doppler'
WORDORB = os.environ.get("C8T8_WORDORB", "rate=1/8 radius=2 mix=0.7")   # WHOLE ROUND: the word recirculates - a mercury delay line keeps a word by sending it round and round, so the word (dx-epiano, its bits all song) goes round the listener: an orbit (engine c7606671, after Chowning's moving sources, 1971) circling the head, darker behind, a lap every few bars, all song. Value = the orbit fx's args
CBRK = os.environ.get("C8T8_CBRK", "28,4")   # SECTION ROUND (w6, C bars 20-31: little new vs w5, where more texture failed): the kit steps out - for C bars CBRK ('start,len') kick, hats, open hats, clap, rim and shaker stop, and what is left is the line itself: the Life cells, the VOSIM voice reading the word, the bass and the pads, until the kit comes back for D
VOSWORD = os.environ.get("C8T8_VOSWORD", "90")   # WHOLE ROUND: the memory speaks its word - after the program counter, through C bars 20-31 (w6, 'little new vs w5', where Life alone reads as texture), a VOSIM voice (engine 1a5a0572; Kaegi and Tempelaars, 1978: two pulse-train layers make a vowel, their formants swept by a slow jaw and tongue) sings the word's bits as the dx-epiano plays them, an octave down: the oldest computer voice reading what the line holds. Value = velocity
GENDY = os.environ.get("C8T8_GENDY", "-12")   # SECTION ROUND (w3, A bars 16-31: little new vs w2): the mercury trembles - under A's second half a gendyn drone (engine 6014b933; Xenakis's dynamic stochastic synthesis: a 12-point wave whose levels, and a little of its segment lengths, random-walk every cycle) holds each chord's root an octave over the bass, four bars a chord (D Bb G A), never quite the same wave twice: the line's medium, a liquid that won't sit still. Low-passed at 1.5 kHz, into the line. Value = gain dB
HUMGAIN = os.environ.get("C8T8_HUMGAIN", "-18dB")   # the store powering up, quieter: the in seam read t8's head 6.1 dB louder than t7's tail, and the hum (97/114 Hz +13.7) was the loud thing
ESTABLE = os.environ.get("C8T8_ESTABLE", "1")   # event_stable: each note's dice from its track, beat and pitch, so later edits stay local (switching it on re-rolls the take once)
LIFE = os.environ.get("C8T8_LIFE", "C20")   # WHOLE ROUND: the memory is alive - after the program counter stops (C bar 20), a Game of Life (engine ade7b930's gen: life, B3/S23 on an 8 x 8 torus, seeded with an R-pentomino) plays the stored bits on glass: a playhead reads one column a sixteenth, live cells sound (up to three, rows on the song's scale, bottom low), each pass across the grid one generation, into the mercury line. 'C20' runs from C bar 20 through D; 'D' through D only
READBACK2 = os.environ.get("C8T8_READBACK2", "70")   # SECTION ROUND (w9, 4:20-4:52, E's end into the outro: little new vs w8): the memory is read back once more before the end - the refresh's bytebeat returns over E's last four bars, on the same roots lifted with E (D#4 B3 G#3 A#3), so the line's own overtone arpeggio leads into the outro where the choir keeps the promise. Value = velocity
READBACK = os.environ.get("C8T8_READBACK", "90")   # WHOLE ROUND: the refresh reads the memory back as a bytebeat (engine 709cf900): one formula on the counter t, t*(8+8*(t>>12&3)) - a saw stepping up the harmonic series 1 2 3 4 about once a beat, so the read-back rings as an arpeggio of its own overtones - one note a bar on the chord roots (D Bb G A) in the refresh's first four bars, low-passed, into the mercury line. Value = velocity
ECHOEND = os.environ.get("C8T8_ECHOEND", "84,0,0")   # the latest it can come: the sung line's tune returns once more on the tape choir across the outro's last eight bars, an octave down and at half speed (A3 G3 F3 E3 D3), then again lower still, the last D held to the end - so the song ends on the line it promised, and the tail holds the 250/470 Hz t9's head opens on. Value = velocity
PUMPON = os.environ.get("C8T8_PUMPON", "-6")   # WHOLE ROUND: the pads and the bass breathe with the kick again - their sidechain pump was keyed on 'kick.k', and v36's machine kick has no kit pieces, so it never fired after v36 (wM's plan warning, 2 Nov); now it keys on every kick note. Value = depth dB (e.g. -6 as designed)
SAYTTS = os.environ.get("C8T8_SAYTTS", "1")   # PALETTE: the spoken voices that tell what a delay line is (say, say2, say3: voice-spoken) speak as a computer - voice-tts, the library's 1990s desktop text-to-speech; the words and their timing unchanged
COUNTER = os.environ.get("C8T8_COUNTER", "78")   # SECTION ROUND (w5, C bars 4-19, static): the program counter - a marimba (its own track ctr, listed last) counts 1..16 in binary, one number a bar: bit k set strikes beat k, on D G C F (fourths, k = 0..3), so each bar's rhythm is the next address and the line runs through all sixteen patterns while the word is refreshed. Value = velocity
OWNHATS = os.environ.get("C8T8_OWNHATS", "300")   # PALETTE: the hats leave the 909 kit for the machine layer's synthesised hat - closed (60 ms) on hats and hats2, the open ones (OWNHATS ms) on their own track ohat, listed last (the open hits stay on hats/hats2 at velocity 1, so no dice move): with v36's kick and v37's clap, the whole groove is the song's own
PDPADP = {"about": "a CZ pad: reso_trap, its resonance breathing", "synth": {"layers": [{"type": "pd", "pd": {"shape": "reso_trap", "amount": {"value": float(os.environ.get("C8T8_PDRES", "0.12")), "mod": [{"src": "lfo.sweep", "amount": 0.15}]}}}], "amp": "500ms 0.8 0.85 1s"}}
HPATCH = {"about": "the machine layer's closed hat", "synth": {"layers": [{"type": "machine", "machine": {"part": "hat", "decay": "60ms"}}]}}
CPATCH = {"about": "the machine layer's clap", "synth": {"layers": [{"type": "machine", "machine": {"part": "clap", "decay": "200ms"}}]}}
RPATCH = {"about": "the machine layer's rim", "synth": {"layers": [{"type": "machine", "machine": {"part": "rim"}}]}}
KPATCH = {"about": "the machine layer's kick, tuned in the key", "synth": {"layers": [{"type": "machine", "machine": {"part": "kick", "punch": 24, "decay": "380ms", "click": 0.5, "drive": 0.25}}]}}
WRITEIN = os.environ.get("C8T8_WRITEIN", "100")   # SECTION ROUND (w1, the intro): the word is WRITTEN before it is kept - sixteen bars, sixteen bits: in bar b only bits 0..b sound (the unwritten ones are kept at velocity 1, so no dice move) and the bit just written is struck harder (WRITEIN velocity); the whole word stands when A begins
EUP = os.environ.get("C8T8_EUP", "1")   # WHOLE ROUND: the repaired word a step higher - E (and with 'n,outro' the outro too, with the sung line) rises EUP semitones on the stretched octave: every pitched part of the section (word, zeros, marimba, pads, organ, hum, bass) moves together. Value = 'semitones' or 'semitones,outro'
_KEY = [0]
TRAVSPLIT = os.environ.get("C8T8_TRAVSPLIT", "-16")   # WHOLE ROUND: only the word 'travels' travels - the sung 'it only travels' went whole into the delay line (send -4 dB) and blurred; now 'it only' sings nearly dry (line send TRAVSPLIT dB, room -14) and only 'travels' goes into the line, on its own track (sungv2, listed last), so the line repeats the one word that says what it does
MARE = os.environ.get("C8T8_MARE", "-8")   # WHOLE ROUND: the repaired word in wood - through E the word's bits are doubled an octave down on a marimba (modal-marimba, the library's physical mallet from chirper-two's t3): the stored word, struck by hand. Its own track, listed last. Value = velocity offset
CKICK = os.environ.get("C8T8_CKICK", "lock")   # WHOLE ROUND: contrast between the grooves - A and E keep four on the floor, but C (the refreshed word, the new stride-5 tune) puts the kick on a 3-3-2: 'tres' 1, the and-of-2, 4 (0 6 12), or 'lock' with the bass (0 6 10). The grid kicks stay at velocity 1 (the dice of every later kick stay put); the new hits play on kick2, listed last
SKEW = os.environ.get("C8T8_SKEW", "local")   # SECTION ROUND, window 7 (D; 'little new vs w6'): the clock skews in the corruption - through D the hats leave the grid for dotted eighths (every 3 sixteenths, three against four), the open hat with them; E's repair puts them back
CPADUP = os.environ.get("C8T8_CPADUP", "1")   # SECTION ROUND, window 6 (2:42-3:15, C bars 20-31; 'little new vs w5'): the refreshed store opens out - for C's last twelve bars the pads (four voices) move up an octave, so the harmony brightens and lifts before the corruption (D) closes in
A2LIFT = os.environ.get("C8T8_A2LIFT", "1")   # SECTION ROUND, window 3 (A bars 16-31, 'little new vs w2'; a fading low-pass and a quiet rim both failed): the tune grows halfway through A - from A bar 16 the word's upper half takes the octave leaps C and E have (bits 8 and 12 up an octave), so A's second half is brighter and the leap is heard first here
ZEROS = os.environ.get("C8T8_ZEROS", "-18")   # SECTION ROUND, window 8 (E bars 4-19, the repaired word at its loudest; flagged static): the zeros sound. For sixteen bars the word's UNSET bits play too, an octave up on a glass chime (fb-crystal, which no other song here uses), filling the rests between the set ones - a hocket of ones and zeros. They fill in by four-bar steps (bit positions 0 mod 4, then 0-1, 0-2, all), so the window builds and then the zeros go quiet again. Gain in dB
ARC = os.environ.get("C8T8_ARC", "4")   # an energy arc: A to E sat at one level for four minutes (-10.0..-10.4 dB a section). A gain lane last on the master (after the compressor) holds A ARC dB down as the groove enters, eases up through C and D and is open from E - the repaired word the loudest place in the record
DARK = os.environ.get("C8T8_DARK", "8")  # the tape running out: a master low-pass closing over the outro's last bars (the hiss and the line's top go first); value = bars
FORM = [("intro", 16), ("A", 36), ("refresh", 8), ("C", 32), ("D", 16), ("E", 28), ("outro", 16)]
TRACKS = ("word", *(("zeros",) if ZEROS else ()), "pad0", "pad1", "pad2", "pad3", "org0", "org1", "hum", "hum2", "bass", "kick", "shk", "hats", "clap", "rim") + (("hats2",) if os.environ.get("C8T8_SKEW", "local") == "local" else ()) + (("kick2",) if os.environ.get("C8T8_CKICK", "lock") else ()) + (("ohat",) if os.environ.get("C8T8_OWNHATS", "300") else ()) + (("ctr",) if os.environ.get("C8T8_COUNTER", "78") else ()) + (("mar",) if os.environ.get("C8T8_MARE", "-8") else ()) + (("vos",) if os.environ.get("C8T8_VOSWORD", "90") else ())

# the word's 16 bits -> pitches (D minor, spread so neighbours leap): D4 F4 G4 A4 C5 D5 F5 A5
SC = [62, 65, 67, 69, 72, 74, 77, 81]
WORD0 = [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0]
CHORDS = [(38, [53, 57, 60, 64]), (34, [53, 57, 60, 62]), (31, [50, 53, 57, 58]), (33, [49, 55, 57, 60])]   # Dm9 Bbmaj9 Gm9 A7sus


def hz(m):
    """MIDI note -> frequency on the stretched octave (A4 = 440 stays put)."""
    return f"{440 * 2 ** ((m + _KEY[0] - 69) / 12 * STRETCH):.2f}hz"


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total():
    return sum(nb for _, nb in FORM) * BAR


def err_rate(sec, b, nb):
    """The memory's error rate per bit per pass."""
    return {"intro": 0.0, "A": 0.10 * b / nb, "refresh": 0.0, "C": 0.02 + 0.12 * b / nb, "D": 0.25,
            "E": 0.05 * (1 - b / nb), "outro": 0.0}[sec]


def build():
    rng = random.Random(SEED)
    ev = {k: [] for k in TRACKS}

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    word, history = list(WORD0), []
    for sec, nb in FORM:
        _KEY[0] = int(EUP.split(",")[0]) if EUP and (sec == "E" or (sec == "outro" and "outro" in EUP)) else 0
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            # the word: one pass a bar (each set bit a sixteenth); bits flip at the error rate, a refresh rebuilds it
            if sec == "refresh" and b == 0 and history:
                last = history[-4:]
                word = [1 if sum(h[i] for h in last) * 2 >= len(last) else 0 for i in range(16)]
            e = err_rate(sec, b, nb)
            word = [bit ^ (1 if rng.random() < e else 0) for bit in word]
            history.append(list(word))
            if WTABLE and b % 4 == 0 and sec in ("A", "C", "D", "E"):
                rr = (CHORDS[(b // 4) % 4] if sec != "refresh" else CHORDS[0])[0]
                WT["notes"].append((at, hz(rr + 12), 4 * BAR, 72))
                WT["frames"].append([[1, 1.0]] + [[i + 2, round(1 / (i + 2) ** 0.7, 3)] for i, bit in enumerate(word) if bit])
            last_read = WORDEND and sec == "outro" and b >= nb - 4
            if sec not in ("outro", "refresh") or (sec == "refresh" and b >= 4) or last_read:
                for i, bit in enumerate(word):
                    if bit:
                        sd = {k: int(v) for k, v in re.findall(r"([A-Z])(\d)", STRIDE)}.get(sec, 3) if STRIDE else 3
                        p = SC[(i * sd) % 8] + (0 if i < 8 else 12 if (sec in ("C", "E") or (A2LIFT and sec == "A" and b >= 16)) and i % 4 == 0 else 0)
                        wv = int(WORDEND) if last_read else (86 if i % 4 == 0 else 70)
                        if WRITEIN and sec == "intro":
                            rate = 2 if "x2" in WRITEIN else 1   # 'x2': two bits a bar, the word whole by bar 8
                            hi = rate * b + rate - 1
                            wv = 1 if i > hi else (int(WRITEIN.split(",")[0]) if i > hi - rate else wv)
                        add("word", at + i, hz(p), 1, wv)
                    elif ZEROS and sec == "E" and 4 <= b < 20 and i % 4 <= (b - 4) // 4:
                        p = SC[(i * 3) % 8] + 12
                        add("zeros", at + i, hz(p), 1, 52 + 4 * ((b - 4) // 4) + (6 if i % 4 == 0 else 0))
            r, v = CHORDS[(b // 4) % 4] if sec != "refresh" else CHORDS[0]
            # pads: long chords, every 4 bars
            if b % 4 == 0 and sec != "D":
                for j, n in enumerate(v):   # one voice per track: frequencies cannot stack in a chord token
                    add(f"pad{j}", at, hz(n + (12 if (OUTUP and sec == "outro" and b >= nb - 8) or (CPADUP and sec == "C" and b >= 20) else 0)), 4 * BAR, int(OUTPAD) if OUTPAD and sec == "outro" and b >= nb - 8 else (64 if sec in ("intro", "outro") else 72))
            if HUM and sec == "intro" and b < int(HUM) and HUMA and b < int(HUMA):
                if b == 0:
                    add("hum", at, hz(33), int(HUMA) * BAR, HUMV)
                    if HUMOCT:
                        add("hum2", at, hz(45), int(HUMA) * BAR, int(HUMOCT))
            elif HUM and sec == "intro" and b < int(HUM) and (b % 4 == 0 or (HUMA and b == int(HUMA))):
                add("hum", at, hz(26), (4 - b % 4) * BAR, 110 - 6 * (b // 4))
            if ORGAN and sec in ("A", "C", "E"):
                for j, n in enumerate(v[2:]):
                    for q in range(0, 16, 2):
                        add(f"org{j}", at + q, hz(n + 12), 1, int(ORGAN) + (10 if q % 4 == 0 else 0))
            groove = sec in ("A", "C", "D", "E")
            if groove:
                ck = CKICK and sec == "C"
                cpos = (0, 6, 12) if CKICK == "tres" else (0, 6, 10)
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, (116 if q == 0 else 108) if not ck or q in cpos else 1)
                if ck:
                    for q in cpos:
                        if q not in (0, 4, 8, 12):
                            add("kick2", at + q, "k", 1, 108)
                if SKEW and sec == "D":
                    for k3 in range(-(-(BAR - (b * BAR) % 3) // 3)):
                        q = ((3 - (b * BAR) % 3) % 3) + 3 * k3
                        if q < 16:
                            add("hats2" if SKEW == "local" else "hats", at + q, "oh" if (b * BAR + q) % 6 == 0 else "h", 1, 70 if (b * BAR + q) % 6 == 0 else 58)
                if not (SKEW and sec == "D") or SKEW == "local":
                  quiet = SKEW == "local" and sec == "D"   # the grid hats keep their places (velocity 1) so the per-note dice of every later hat stay put
                  for q in range(16):
                    if q % 4 == 2:
                        add("hats", at + q, "oh", 1, 1 if quiet else 72)
                    elif q % 2 == 1:
                        add("hats", at + q, "h|?0.85", 1, 1 if quiet else 52)
                if SHAKE and sec in ("A", "C", "E"):
                    for q in range(16):
                        add("shk", at + q, "sh", 1, int(SHAKE) + (14 if q % 2 else 0) - (8 if q % 4 == 0 else 0))
                if sec in ("C", "E"):
                    add("clap", at + 4, "cp", 1, 92)
                    add("clap", at + 12, "cp", 1, 96)
                if sec in ("C", "D"):   # a Euclidean (5, 16) rim
                    for q in (0, 3, 6, 10, 13):
                        add("rim", at + q, "rs", 1, 64)
                add("bass", at, hz(r), 3, 100)
                add("bass", at + 6, hz(r), 2, 88)
                add("bass", at + 10, hz(r + 12 if b % 2 else r), 3, 92)
    if MARE:
        e0, e1 = sec_start("E"), sec_start("outro")
        ev["mar"] = [(a, f"{float(h[:-2]) / 2:.2f}hz" if h.endswith("hz") else h, l, max(1, v + int(MARE))) for (a, h, l, v) in ev["word"] if e0 <= a < e1]
    _KEY[0] = 0
    if LATERDROP and LATER:
        u = sec_start("E") + 12 * BAR
        w = u + 2 * BAR
        for k in ("word", "mar", "zeros", "hats", "clap"):
            if k in ev:
                ev[k] = [(a, h, l, 1 if u <= a < w else v) for (a, h, l, v) in ev[k]]
    if COUNTER:
        c0 = sec_start("C")
        ev["ctr"] = []
        for i in range(16):
            n = i + 1
            for k in range(4):
                if n >> k & 1:
                    ev["ctr"].append((c0 + (4 + i) * BAR + 4 * k, hz((62, 67, 72, 77)[k]), 3, int(COUNTER) + (8 if k == 0 else 0)))
            if n == 16:
                ev["ctr"].append((c0 + (4 + i) * BAR, hz(50), 8, int(COUNTER) + 10))   # 16 = 10000: the carry, out of four bits - a low D
    for _sec, _brk in (("C", CBRK), ("E", EBRK)):
        if not _brk:
            continue
        bs, bl = (int(x) for x in _brk.split(","))
        u, w = sec_start(_sec) + bs * BAR, sec_start(_sec) + (bs + bl) * BAR
        for k in ("kick", "kick2", "hats", "hats2", "ohat", "clap", "rim", "shk"):
            if k in ev:
                ev[k] = [e for e in ev[k] if not (u <= e[0] < w)]
    if VOSWORD:
        c20, c32 = sec_start("C") + 20 * BAR, sec_start("C") + 32 * BAR
        ev["vos"] = [(a, f"{float(h[:-2]) / 2:.2f}hz", max(l, 2), int(VOSWORD)) for (a, h, l, v) in ev["word"] if c20 <= a < c32 and h.endswith("hz") and v > 1]
    if OWNHATS:
        ev["ohat"] = sorted((a, "A4", 4, v) for k in ("hats", "hats2") if k in ev for (a, h, l, v) in ev[k] if h == "oh")
        for k in ("hats", "hats2"):
            if k in ev:
                ev[k] = [(a, "A4" + h[1:] if h.startswith("h") else "A4", l, 1 if h == "oh" else v) for (a, h, l, v) in ev[k]]
    if HANDS:
        if HANDS in ("clap", "both"):
            ev["clap"] = [(a, "C4" if h == "cp" else h, l, v) for (a, h, l, v) in ev["clap"]]
        if HANDS in ("rim", "both"):
            ev["rim"] = [(a, "E5" if h == "rs" else h, l, v) for (a, h, l, v) in ev["rim"]]
    if KITOWN:
        for k in ("kick", "kick2"):
            if k in ev:
                ev[k] = [(a, KITOWN if h == "k" else h, 2, v) for (a, h, l, v) in ev[k]]
    return {k: stream(ev[k], total()) for k in TRACKS}


def stream(events, tot):
    events.sort()
    out, t = [], 0
    for at, head, ln, vel in events:
        if at < t:
            continue
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        h, _, chance = head.partition("|")
        out.append(f"{h}/{ln / 4:g}b@{int(vel)}{chance}")
        t = at + ln
    if t < tot:
        out.append(f"R/{(tot - t) / 4:g}b")
    return " ".join(out)


def wt_score():
    out, t = [], 0
    for at, head, ln, vel in WT["notes"]:
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        out.append(f"{head}/{ln / 4:g}b@{vel}")
        t = at + ln
    return " ".join(out)


def lane(points):
    spb = 60 / BPM
    return {"points": [[f"{t16 / 4 * spb:.3f}s", v] for t16, v in points]}


def sung_track(gain):
    """The sung line (tts --sing --print writes m-notes), its pitches moved onto the stretched octave in Hz."""
    src = json.load(open(os.path.join(HERE, "chirpers8-t8-sung-travels.json" if WORDS else "chirpers8-t8-sung.json")))["tracks"][0]
    off = (sec_start("outro") + 8 * BAR) / 4
    up = int(EUP.split(",")[0]) if EUP and "outro" in EUP else 0
    notes = [dict(n, at=round(n["at"] + off, 4), pitch=hz(float(n["pitch"][1:]) + up)) for n in src["notes"]]
    if TRAVSPLIT:
        return [{"name": "sungv", "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": -0.1,
                 "fx": ["hp cutoff=180"], "sends": {"line": f"{TRAVSPLIT}dB", "room": "-14dB"}, "notes": notes[:3]},
                {"name": "sungv2", "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": -0.1,
                 "fx": ["hp cutoff=180"], "sends": {"line": "-4dB", "room": "-10dB"}, "notes": notes[3:]}]
    return {"name": "sungv", "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": -0.1,
            "fx": ["hp cutoff=180"], "sends": {"line": "-4dB", "room": "-10dB"}, "notes": notes}


def canon_of(tr, lag):
    """The memory sings it back: the sung track again, LAG beats later, a diatonic third below in D minor, on the same stretched octave."""
    down = {9: 4, 7: 3, 5: 3, 4: 4, 2: 4, 0: 3, 10: 3, 11: 4, 1: 4, 3: 3, 6: 3, 8: 4}   # pitch class -> semitones down to the third below
    lg2 = __import__("math").log2
    lift = (int(EUP.split(",")[0]) if EUP and (tr["name"] == "sungl" or (tr["name"] != "sungc" and "outro" in EUP)) else 0)   # E (and the outro, if lifted) sits a step up: thirds in that key
    out = []
    for n in tr["notes"]:
        m = 69 - _KEY[0] + 12 * lg2(float(str(n["pitch"])[:-2]) / 440) / STRETCH
        out.append(dict(n, at=round(n["at"] + lag, 4), pitch=hz(m - down[int(round(m + _KEY[0] - lift)) % 12])))
    g = float(str(tr["gain"]).replace("dB", "")) - 6
    return {"name": tr["name"] + "-canon", "patch": tr["patch"], "gain": f"{g:g}dB", "pan": -tr.get("pan", 0) * 3,
            "fx": tr.get("fx", []), "sends": {"line": "-2dB", "room": "-10dB"}, "notes": out}


def later_track(gain):
    """'it comes later on', sung at E bar 12 on the stretched octave, lifted with E."""
    src = json.load(open(os.path.join(HERE, "chirpers8-t8-sung-later.json")))["tracks"][0]
    off = (sec_start("E") + 12 * BAR) / 4
    up = int(EUP.split(",")[0]) if EUP else 0
    notes = [dict(n, at=round(n["at"] + off, 4), pitch=hz(float(n["pitch"][1:]) + up)) for n in src["notes"]]
    return {"name": "sungl", "patch": src.get("patch", "voice-speech"), "gain": f"{gain}dB", "pan": 0.1,
            "fx": ["hp cutoff=180"], "sends": {"line": "-16dB", "room": "-14dB"}, "notes": notes}


def reversed_back(tr, offs16, w0, w1):
    """A reverse grain cloud on one word of a voice track (word at beats w0..w1 of the take), at each offset (sixteenths)."""
    if not BACKREV:
        return tr
    pts = [["0b", 0]]
    for o in offs16:
        b = o / 4
        pts += [[f"{b + w0 - 0.05:.3f}b", 0], [f"{b + w0 + 0.2:.3f}b", 1], [f"{b + w1:.3f}b", 1], [f"{b + w1 + 0.35:.3f}b", 0]]
    tr["fx"] = [*tr["fx"], {"type": "cloud", "mix": {"value": 0, "mod": [{"src": "auto.rb", "amount": float(BACKREV)}]}, "density": 22, "size": "120ms",
                            "position": "200ms", "spray": "80ms", "pitch": 0, "reverse": 1.0, "spread": 0.5, "seed": 4}]
    tr["auto"] = {**tr.get("auto", {}), "rb": {"points": pts}}
    return tr


def voice(file, name, offs16, gain, fx, sends):
    """A humanized tts line (tts --print) at each offset (sixteenths)."""
    src = json.load(open(os.path.join(HERE, file)))["tracks"][0]
    notes, fv = [], []
    for o16 in offs16:
        off = o16 / 4
        notes += [dict(n, at=round(n["at"] + off, 4)) for n in src["notes"]]
        fv += [[f"{float(t[:-1]) + off:.3f}b", v] for t, v in src["auto"]["fv"]["points"]]
    return {"name": name, "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": 0.15,
            "fx": [*src["fx"], *fx], "auto": {"fv": {"points": fv}}, "sends": sends, "notes": notes}


def song():
    doc = song0()
    if SAYTTS:
        for t in doc["tracks"]:
            if isinstance(t, dict) and t["name"] in ("say", "say2", "say3") and t.get("patch") == "voice-spoken":
                t["patch"] = "voice-tts"
    if TRAVSPLIT:
        trs = doc["tracks"]
        i = next(k for k, t in enumerate(trs) if isinstance(t, list))
        a, b = trs[i]
        trs[i] = a
        trs.append(b)   # 'travels' listed last
    if LATER:
        doc["tracks"].append(later_track(LATER))
        if DUET:
            src = json.load(open(os.path.join(HERE, "chirpers8-t8-sung-duet.json")))["tracks"][0]
            off = (sec_start("E") + 12 * BAR) / 4 + 0.03
            up = int(EUP.split(",")[0]) if EUP else 0
            du = later_track(LATER)
            du.update(name="sungld", pan=-0.3, gain=f"{float(LATER) - float(DUET):g}dB",
                      notes=[dict(n, at=round(n["at"] + off, 4), pitch=hz(float(n["pitch"][1:]) + up)) for n in src["notes"]])
            doc["tracks"].append(du)
        if SUNGMID:
            mid = later_track(LATER)
            src = json.load(open(os.path.join(HERE, "chirpers8-t8-sung-later.json")))["tracks"][0]
            off = (sec_start("C") + int(SUNGMID) * BAR) / 4
            mid.update(name="sungc", pan=-0.1, notes=[dict(n, at=round(n["at"] + off, 4), pitch=hz(float(n["pitch"][1:]))) for n in src["notes"]])
            doc["tracks"].append(mid)
    if OWNHATS or COUNTER or VOSWORD:
        T = build()   # one build for the song-level tracks (each build adds to the wavetable's frames)
    if OWNHATS:
        doc["tracks"].append({"name": "ohat", "patch": {"about": "the machine layer's open hat", "synth": {"layers": [{"type": "machine", "machine": {"part": "hat", "decay": f"{OWNHATS}ms"}}]}},
                              "gain": "-11dB", "pan": 0.15, "score": "swing16=0.56 " + T["ohat"]})
    if COUNTER:
        doc["tracks"].append({"name": "ctr", "patch": ({"about": "CSIRAC's hooter: a raw square from the bus", "synth": {"layers": [{"type": "pd", "pd": {"shape": "square", "amount": 0.92}}],
                                                                  "amp": "1ms 0.8 0.55 70ms", "filters": [{"kind": "lp", "cutoff": 3200, "q": 0.7}]}} if HOOT else "modal-marimba"),
                              "gain": f"{HOOT}dB" if HOOT else "-10dB", "pan": -0.3, "sends": {"room": "-12dB"}, "score": T["ctr"]})
    if ECHOCH:
        up = int(EUP.split(",")[0]) if EUP else 0
        evs = []
        for k, bar in enumerate((16, 20)):
            t0 = sec_start("E") + bar * BAR
            q = 0
            for m, ln in ((69, 2), (67, 2), (65, 4), (64, 2), (62, 8)):
                evs.append((t0 + q, hz(m + up), ln, int(ECHOCH) - 14 * k))
                q += ln
        if ECHOEND:
            o0 = sec_start("outro")
            uo = up if (EUP and "outro" in EUP) else 0
            eo = [int(x) for x in ECHOEND.split(",")[1:]] or [-12, -24]
            for k, (bar, oc) in enumerate(((8, eo[0]), (12, eo[1]))):
                t0, q = o0 + bar * BAR, 0
                for m, ln in ((69, 4), (67, 4), (65, 8), (64, 4), (62, 16)):
                    last = k == 1 and m == 62
                    evs.append((t0 + q, hz(m + oc + uo), (total() - t0 - q) if last else ln, int(ECHOEND.split(",")[0]) - 6 * k))
                    q += ln
        doc["tracks"].append({"name": "echoch", "patch": ({"about": "a VOSIM 'oh' choir", "synth": {"layers": [{"type": "vosim", "vosim": {"formant": {"value": 450, "mod": [{"src": "lfo.jaw", "amount": 0.15}]}, "pulses": 3, "decay": 0.7}},
                                                                            {"type": "vosim", "level": 0.5, "vosim": {"formant": {"value": 800, "mod": [{"src": "lfo.tongue", "amount": 0.2}]}, "pulses": 4, "decay": 0.72}}], "amp": "180ms 0.85 0.85 700ms"}} if ECHOVOS else "mellotron-choir"),
                              **({"lfo": {"jaw": "sine rate=1/3", "tongue": "tri rate=1/5"}} if ECHOVOS else {}),
                              "gain": f"{ECHOVOS}dB" if ECHOVOS else os.environ.get("C8T8_ECHOGAIN", "-10dB"), "pan": 0.25, "sends": {"line": "-12dB", "room": "-10dB"},
                              "score": stream(evs, total())})
    if READBACK:
        r0 = sec_start("refresh")
        evs = [(r0 + i * BAR, n, BAR, int(READBACK)) for i, n in enumerate(("D4", "A#3", "G3", "A3"))]
        e24 = sec_start("E") + 24 * BAR
        evs2 = [(e24 + i * BAR, n, BAR, int(READBACK2)) for i, n in enumerate(("D#4", "B3", "G#3", "A#3"))] if READBACK2 else []
        if not FLYBY:
            evs += evs2
        doc["tracks"].append({"name": "readback", "patch": {"synth": {"layers": [{"type": "bytebeat", "bytebeat": {"formula": "t*(8+8*(t>>12&3))", "clock": 8000}}]}},
                              "gain": os.environ.get("C8T8_READGAIN", "-20dB"), "pan": -0.2, "fx": [{"type": "filter", "kind": "lp", "cutoff": 2400, "q": 0.7}],
                              "sends": {"line": "-8dB", "room": "-12dB"}, "score": stream(evs, total())})
    if LIFE:
        l0 = sec_start("C") + 20 * BAR if LIFE == "C20" else sec_start("D")
        nsteps = (sec_start("E") - l0)
        doc["tracks"].append({"name": "life", "patch": ({"about": "a CZ pluck for the Life cells", "synth": {"layers": [{"type": "pd", "pd": {"shape": "square", "amount": {"value": 0.1, "mod": [{"src": "env.p", "amount": 0.8}]}}}],
                                                                   "env": {"p": "1ms 1 0 120ms"}, "amp": "1ms 0.6 0 300ms"}} if LIFEPD else "glass"),
                              "gain": f"{LIFEPD}dB" if LIFEPD else os.environ.get("C8T8_LIFEGAIN", "-26dB"), "pan": -0.15, "at": f"{l0 / 4:g}b", "seed": 88,
                              "sends": {"line": "-10dB", "room": "-12dB"}, **({"fx": [{"type": "filter", "kind": "lp", "cutoff": int(os.environ["C8T8_LIFELP"]), "q": 0.7}]} if os.environ.get("C8T8_LIFELP") else {}),
                              "gen": {"type": "life", "width": 8, "height": 8, "init": "center", "n": nsteps, "poly": 3,
                                      "notes": "D4 F4 G4 A4 C5 D5 F5 A5", "len": "/16"}})   # note names: hz can't stack in a chord (poly 3); within a few cents of hz()'s stretch
    if ESTABLE:
        doc["event_stable"] = True
    if GENDY:
        a0 = sec_start("A")
        gev = [(a0 + b * BAR, hz(CHORDS[(b // 4) % 4][0] + 12), 4 * BAR, 84) for b in range(16, 32, 4)]
        doc["tracks"].append({"name": "gdy", "patch": {"about": "a gendyn drone: the mercury trembling", "synth": {"layers": [{"type": "gendyn", "gendyn": {"points": 12, "amp": 0.04, "time": 0.01, "spread": 0.1, "dist": "cauchy"}}]}},
                              "gain": f"{GENDY}dB", "pan": 0.1, "fx": [{"type": "filter", "kind": "lp", "cutoff": 1500, "q": 0.7}],
                              "sends": {"line": "-10dB", "room": "-12dB"}, "score": stream(gev, total())})
    if VOSWORD:
        doc["tracks"].append({"name": "vos", "gain": os.environ.get("C8T8_VOSGAIN", "-12dB"), "pan": 0.2, "lfo": {"jaw": "sine rate=1/2", "tongue": "tri rate=3/4"},
                              "patch": {"synth": {"layers": [{"type": "vosim", "vosim": {"formant": {"value": 600, "mod": [{"src": "lfo.jaw", "amount": 0.45}]}, "pulses": 3, "decay": 0.7}},
                                                             {"type": "vosim", "level": 0.55, "vosim": {"formant": {"value": 1500, "mod": [{"src": "lfo.tongue", "amount": 0.6}]}, "pulses": 4, "decay": 0.75}}],
                                                  "amp": "10ms 0.8 0.7 120ms"}},
                              "sends": {"line": "-12dB", "room": "-12dB"}, "score": T["vos"]})
    if FLYBY and READBACK and READBACK2:
        rad, dop = FLYBY.split(",")
        e24 = sec_start("E") + 24 * BAR
        ph = (-(e24 / 4) / 16) % 1
        evs2 = [(e24 + i * BAR, n, BAR, int(READBACK2)) for i, n in enumerate(("D#4", "B3", "G#3", "A#3"))]
        doc["tracks"].append({"name": "readback2", "patch": {"synth": {"layers": [{"type": "bytebeat", "bytebeat": {"formula": "t*(8+8*(t>>12&3))", "clock": 8000}}]}},
                              "gain": os.environ.get("C8T8_FLYGAIN", "-14dB"),
                              "fx": [{"type": "filter", "kind": "lp", "cutoff": 2400, "q": 0.7}, f"orbit path=line rate=1/4 radius={rad} distance=2 doppler={dop} phase={ph:.4f}"],
                              "sends": {"line": "-8dB", "room": "-12dB"}, "score": stream(evs2, total())})
    if DECAY:
        st_ = {k: sec_start(k) for k in ("refresh", "outro")}
        dec = {"points": [["0b", 0], [f"{st_['refresh'] / 4 - 0.25:g}b", 0.55], [f"{st_['refresh'] / 4:g}b", 0],
                          [f"{st_['outro'] / 4 - 0.25:g}b", 0.55], [f"{st_['outro'] / 4:g}b", 0], [f"{total() / 4:g}b", 0]]}
        if LINEHISS:
            doc["tracks"].append({"name": "hiss", "gain": f"{LINEHISS}dB", "auto": {"dec": dec},
                                  "patch": {"synth": {"layers": ["white"], "amp": "2s 1 1 2s", "filters": [{"kind": "hp", "cutoff": 7000, "q": 0.7}, {"kind": "lp", "cutoff": 11000, "q": 0.7}]}},
                                  "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dec", "amount": 22}]}}],
                                  "score": f"C4/{total() / 4 - 2:g}b"})
        if WORDFADE and WORDORB:
            for t_ in doc["tracks"]:
                if isinstance(t_, dict) and t_.get("name") == "word":
                    t_["auto"] = dict(t_.get("auto", {}), dec=dec)
                    t_["fx"] = [f for f in t_["fx"] if not (isinstance(f, str) and f.startswith("orbit "))] + [
                        {"type": "orbit", "rate": "1/8", "radius": {"value": 2, "mod": [{"src": "auto.dec", "amount": float(WORDFADE)}]}, "mix": 0.7, **({"level": float(WORDLEVEL)} if WORDLEVEL else {})}]
        doc["tracks"].append({"name": "decay", "gain": f"{DECAY}dB", "pan": 0.1, "auto": {"dec": dec},
                              "patch": {"synth": {"layers": [{"type": "chaos", "chaos": {"system": "duffing", "axis": "x", "amount": {"value": 0, "mod": [{"src": "auto.dec", "amount": float(DECFIX) if DECFIX else 1}]}}}],
                                                  "amp": "8ms 0.8 0.6 250ms", "filters": [{"kind": "lp", "cutoff": int(os.environ.get("C8T8_DECLP", "2500"))}]}},
                              "sends": {"line": "-10dB"}, "score": T["word"]})
        if WORDWARP:
            fl = dict(FORM)
            wv = float(WORDWARP)
            warp = [{"over": f"{fl['intro'] + fl['A']}bar", "to": wv, "curve": "linear"}, {"over": "1bar", "to": 0, "curve": "smooth"}, {"over": f"{fl['refresh'] - 1}bar", "to": 0},
                    {"over": f"{fl['C'] + fl['D'] + fl['E']}bar", "to": wv, "curve": "linear"}, {"over": "1bar", "to": 0, "curve": "smooth"}]
            for t_ in doc["tracks"]:
                if isinstance(t_, dict) and t_.get("name") in ("word", "decay"):
                    t_["warp"] = warp
    if SAYLPC:
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "say":
                t_["fx"] = [{"plain": "lpc", "toy": "lpc pitch=D3 bits=5"}[SAYLPC], *t_.get("fx", [])]
                for n in t_.get("notes", []):
                    n["at"] = round(max(0.0, n["at"] - (0.07 if LPCNUDGE else 0)), 4)
                if SAYARRIVE:
                    r0 = float(SAYARRIVE)
                    t_["auto"] = dict(t_.get("auto", {}), app={"points": [["0b", 1], ["12b", 0], [f"{total() / 4:g}b", 0]]})
                    t_["fx"] = [*t_["fx"], {"type": "orbit", "rate": "1/2", "radius": {"value": 1, "mod": [{"src": "auto.app", "amount": r0 - 1}]}, "level": 2, "mix": 0.85}]
    if DUFFBASS:
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "bass" and t_.get("patch") == "808":
                t_["patch"] = {"about": "a Duffing oscillator held periodic, as a bass", "synth": {"layers": [{"type": "chaos", "chaos": {"system": "duffing", "axis": "x", "amount": 0.2}}, "sine"],
                                                                                              "amp": "4ms 1 0.75 160ms", "filters": [{"kind": "lp", "cutoff": int(DUFFBASS)}]}}
                if os.environ.get("C8T8_DUFFBASSG", "-16"):
                    t_["gain"] = os.environ.get("C8T8_DUFFBASSG", "-16") + "dB"
    if ROBOSUNG:
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") == "sungl":
                twin = json.loads(json.dumps(t_))
                twin.update(name="sungl-robo", gain=f"{ROBOSUNG}dB", pan=-0.2)
                twin["fx"] = [*t_.get("fx", []), {"type": "vocoder", "notes": "D2,A2,D3,F3", "bands": 20, "noise": 0.12, "attack": "4ms", "release": "70ms"}]
                doc["tracks"].append(twin)
    if MARKS:
        xb = (sec_start("E") + 16 * BAR) / 4
        xf = {"points": [["0b", 0], [f"{xb - 0.25:g}b", 0], [f"{xb:g}b", 1], [f"{total() / 4:g}b", 1]]}
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") == "mar":
                ks = json.loads(json.dumps(t_))
                t_["auto"] = dict(t_.get("auto", {}), xf=xf)
                t_["fx"] = [*t_.get("fx", []), {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.xf", "amount": -60}]}}]
                ks.update(name="marks", auto=dict(ks.get("auto", {}), xf=xf),
                          patch={"about": "Karplus-Strong 1983: a noise burst in a one-period averaging loop", "synth": {"layers": [{"type": "ks", "ks": {"blend": float(MARKS), "stretch": 2, "tune": True}}], "amp": "1ms 1 1 400ms"}})
                ks["fx"] = [*ks.get("fx", []), {"type": "gain", "gain": {"value": "-60dB", "mod": [{"src": "auto.xf", "amount": 60}]}}]
                doc["tracks"].append(ks)
    if TUNEKS:
        kb, kg = TUNEKS.split(":")
        a0 = sec_start("A") / 4 + 16 * BAR / 4
        tune = [(0.0, "A4", 1.0), (1.0, "F4", 0.5), (1.5, "D4", 0.5), (2.0, "E4", 1.0), (3.0, "D4", 1.7)]
        notes = []
        for r in range(4):
            st_ = a0 + r * 4 * BAR / 4
            sc = 2.0 if r == 3 else 1.0
            notes += [{"at": round(st_ + o * sc, 3), "pitch": p_, "len": round(l_ * sc, 3), "vel": round(0.8 - 0.1 * r, 2)} for o, p_, l_ in tune]
        doc["tracks"].append({"name": "tuneks", "gain": f"{kg}dB", "pan": -0.25, "sends": {"line": "-12dB"},
                              "patch": {"about": "Karplus-Strong 1983", "synth": {"layers": [{"type": "ks", "ks": {"blend": float(kb), "stretch": 3, "tune": True}}], "amp": "1ms 1 1 800ms"}},
                              "notes": notes})
    if CANON:
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") in ("sungv", "sungv2", "sungl", "sungc") and t_.get("notes"):
                doc["tracks"].append(canon_of(t_, float(CANON)))
    if WORDSCAN:
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") == "word":
                tw = json.loads(json.dumps(t_))
                tw["name"] = "wordscan"
                tw["patch"] = {"about": "scanned synthesis (Mathews 2000): a ring of masses and springs read round at the pitch",
                               "synth": {"layers": [{"type": "scanned", "scanned": {"speed": 0.8, "width": 0.5, "smooth": 0.5, "push": 0.1}, "decay": "2.5s"}], "amp": "4ms 1 0.7 500ms"}}
                tw["gain"] = f"{float(str(t_['gain']).replace('dB', '')) - float(WORDSCAN):g}dB"
                tw["pan"] = -t_.get("pan", 0)
                doc["tracks"].append(tw)
                break
    if BRASSA:
        a0 = sec_start("A") / 4
        tune = [(0.0, 69, 1.0), (1.0, 65, 0.5), (1.5, 62, 0.5), (2.0, 64, 1.0), (3.0, 62, 2.5)]
        notes = []
        for r, st_ in enumerate((a0, a0 + 8 * BAR / 4)):
            notes += [{"at": round(st_ + o, 3), "pitch": hz(m - 12 * r), "len": l_, "vel": 0.85 - 0.15 * r} for o, m, l_ in tune]
        doc["tracks"].append({"name": "brass", "gain": f"{BRASSA}dB", "pan": 0.2, "sends": {"line": "-10dB", "room": "-12dB"},
                              "patch": {"about": "Risset's brass by Chebyshev waveshaping (1979)", "synth": {"layers": [{"type": "shaper", "shaper": {"harmonics": [1, 0.8, 0.6, 0.45, 0.35, 0.25, 0.18, 0.12, 0.08, 0.05], "index": {"value": 0.05, "mod": [{"src": "env.blow", "amount": 0.7}, {"src": "vel", "amount": 0.25}]}}}],
                                        "amp": "40ms 200ms 0.8 150ms", "env": {"blow": {"a": "60ms", "d": "300ms", "s": 0.7, "r": "150ms"}}}},
                              "notes": notes})
    if REWRITE:
        r0, r1 = sec_start("refresh") / 4, sec_start("C") / 4
        doc["tracks"].append({"name": "rewrite", "gain": f"{REWRITE}dB", "pan": 0.0, "sends": {"line": "-8dB", "room": "-12dB"},
                              "auto": {"rw": {"points": [["0b", 0], [f"{r0:g}b", 0], [f"{r1 - 1:g}b", 1], [f"{r1:g}b", 1], [f"{total() / 4:g}b", 1]]}},
                              "patch": {"about": "Chebyshev waveshaping (1979): the harmonic series written back by the index",
                                        "synth": {"layers": [{"type": "shaper", "shaper": {"harmonics": [1, 0.5, 0.33, 0.25, 0.2, 0.17, 0.14, 0.12, 0.11, 0.1, 0.09, 0.08], "index": {"value": 0, "mod": [{"src": "auto.rw", "amount": 1}]}}}],
                                                  "amp": "2s 1 1 1.5s"}},
                              "notes": [{"at": r0, "pitch": hz(50), "len": r1 - r0, "vel": 0.8}, {"at": r0, "pitch": hz(62), "len": r1 - r0, "vel": 0.6}]})
    if ECHOFOF:
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") == "echoch":
                if os.environ.get("C8T8_ECHOFOFT", "1"):   # a twin (the VOSIM choir kept): replacing it cost 0.07 (the outro seam)
                    t_ = json.loads(json.dumps(t_)); t_["name"] = "echoch-fof"; doc["tracks"].append(t_)
                t_["patch"] = {"about": "CHANT (Rodet, IRCAM 1979-84): FOF formant-grain singing, alto",
                               "synth": {"layers": [{"type": "fof", "fof": {"voice": "alto", "vowel": "o>a", "attack": "3ms", "morph": {"value": 0, "mod": [{"src": "env.mouth", "amount": 0.7}]}}}],
                                         "pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 0.2}, {"src": "env.scoop", "amount": -0.3}]},
                                         "lfo": {"vib": {"wave": "sine", "rate": "5.5hz", "delay": "300ms", "fade": "400ms"}},
                                         "env": {"scoop": {"a": "1ms", "d": "120ms", "s": 0}, "mouth": {"a": "900ms", "d": 0, "s": 1, "r": "300ms"}}, "amp": "250ms 0 1 900ms"}}
                t_["gain"] = f"{ECHOFOF}dB"
                t_.pop("lfo", None)
    if RIMKS:
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "rim" and isinstance(t_.get("score"), str):
                d6 = hz(86)
                t_["score"] = __import__("re").sub(r"(?<![A-Za-z])rs/", f"{d6}/", t_["score"])
                t_["patch"] = {"about": "Karplus-Strong (1983): a pulse circulating in a delay line", "synth": {"layers": [{"type": "ks", "bright": 0.75, "ks": {"blend": 0.3, "stretch": 1, "tune": True}}], "amp": "1ms 1 0 120ms"}}
                t_["gain"] = f"{RIMKS}dB"
    return doc


def song0():
    SAYOFFS = ([sec_start("intro") + 8] if SAYHEAD else []) + ([] if SAYHEAD == "move" else [sec_start("intro") + 8 * BAR]) + [sec_start("refresh") + BAR, sec_start("outro")]
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    end = total()
    pump = {"type": "pump", "on": "kick" if (KITOWN and PUMPON) else "kick.k", "depth": f"{PUMPON or -6}dB" if (KITOWN and PUMPON) else "-6dB", "attack": "2ms", "release": "180ms", "curve": 0.7}   # PUMPON: since v36's machine kick plays notes, not kit pieces, 'kick.k' never fired (wM's plan warning); key on the kick track itself
    ts = lane([(0, 0), (st["refresh"] - 8, 0), (st["refresh"] - 1, 1), (st["refresh"], 0), (end, 0)])
    cloudmix = lane([(0, 0), (st["C"], 0), (st["C"] + 8 * BAR, 0.5), (st["D"], 0.8), (st["E"], 0.25), (st["outro"], 0.6), (end, 0.8)])
    frz = lane([(0, 0), (st["refresh"], 0), (st["refresh"] + 1, 1), (st["refresh"] + 6 * BAR, 1), (st["refresh"] + 8 * BAR, 0), (end, 0)])
    chl = lane([(0, 0), (st["D"], 0), (st["D"] + 1, 1), (st["E"] - 1, 1), (st["E"], 0), (end, 0)])
    stut = lane([(0, 0), (st["D"], 0), (st["D"] + 1, 0.8), (st["E"], 0), (end, 0)])
    darkf = {"type": "filter", "kind": "lp", "q": 0.7, "cutoff": {"value": 20000, "mod": [{"src": "auto.lp", "amount": -3.4}]}}
    return {
        "about": "chirpers VIII, track 8 by chirper-zero: delay-line memory. A 16-bit word recirculating round a feedback "
                 "line, decaying and refreshed; a stretched octave. Generated by compose/chirpers8/src/chirpers8-t8.py.",
        **({"vars": {"wear": {"system": {"type": "lorenz", "axis": "x", "dt": 0.01, "stride": 8, "n": 700, "range": [0, float(LZ)], "skip": 40},
                               "every": "1/4", "smooth": "400ms"}}} if LZ else {}),
        "tempo": ([{"at": f"{8 * k}b", "bpm": round(BPM + float(TANKTEMP) * __import__("math").sin(2 * __import__("math").pi * k * 2 / 16), 3), **({"ramp": True} if k else {})}
                   for k in range(total() // (2 * BAR) + 1)] if TANKTEMP else BPM), "ceiling": "-1dB", "loudness": -11, "seed": SEED, "tail": "2s",
        "master": {"fx": [*([darkf] if DARK and DARKPOS != "end" else []),
                          {"type": "tapestop", "time": "2b", "up": "0.25b", "curve": 2.0, "mix": 1,
                           "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}},
                          {"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=300 q=0.8 gain=-2dB", "highshelf cutoff=6000 gain=2dB"] if not EQFIX else
                           (["highpass cutoff=30", "peak cutoff=150 q=0.9 gain=-3dB", "peak cutoff=300 q=0.8 gain=-2dB", "peak cutoff=1000 q=1.2 gain=4dB", "peak cutoff=3000 q=1.4 gain=4dB"]
                            if EQFIX != "2" else
                            ["highpass cutoff=30", "peak cutoff=150 q=0.9 gain=-3.5dB", "peak cutoff=300 q=0.8 gain=-2dB", "peak cutoff=1000 q=1.4 gain=6dB",
                             "peak cutoff=3000 q=1.4 gain=5dB", "highshelf cutoff=9000 gain=-1.5dB",
                             *(["peak cutoff=1030 q=3 gain=5dB", "peak cutoff=3080 q=3 gain=5dB", "peak cutoff=100 q=1 gain=3dB", "peak cutoff=1650 q=2 gain=-2.5dB"] if EQ3 else []),
                             *([f"peak cutoff=1025 q=4 gain={2 * float(EQ4):g}dB", f"peak cutoff=3078 q=4 gain={2.5 * float(EQ4):g}dB",
                                f"peak cutoff=4929 q=4 gain={1.5 * float(EQ4):g}dB"] if EQ4 else [])])},
                          {"type": "tape", "drive": 0.1, "mix": 0.5, "wow": 5, "flutter": 1.5, "drift": 1, "hiss": "-62dB", "seed": 8},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          *([darkf] if DARK and DARKPOS == "end" else []),
                          *([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.arc", "amount": float(ARC)}]}}] if ARC else [])],
                   "auto": {"ts": ts, **({"arc": lane([(0, 0), (sec_start("A") - 1, 0), (sec_start("A"), -1), (sec_start("refresh"), -0.7), (sec_start("C"), -0.6),
                                                        (sec_start("D"), -0.35), (sec_start("E") - 1, -0.35), (sec_start("E"), 0), (end, 0)])} if ARC else {}), **({"lp": lane([*([(0, HEADDARKV), (int(HEADDARK) * BAR, 0)] if HEADDARK else [(0, 0)]), (end - int(DARK) * BAR, 0), (end - 2 * BAR, 0.86), (end, 1)])} if DARK else {})}},
        "buses": {
            "line": {"fx": [{"type": "delay", "time": "1bar", "feedback": 0.78, "mix": 1, "tone": 3200, "ping_pong": True},
                            {"type": "tape", "drive": 0.15, "mix": 0.7, "wow": 9, "flutter": 2.5, "drift": 1.5, "hiss": "-58dB", "seed": 3,
                             **({"warp": {"value": 0, "mod": [{"src": "var.wear", "amount": 1}]}} if LZ else {})},
                            *([{"type": "vinyl", "crackle": {"value": 0, "mod": [{"src": "auto.vc", "amount": 1}]}, "dust": 0.3, "wear": 0.3,
                                "noise": "-66dB", "rumble": 0.1, "seed": 8}] if VINYL else []),
                            {"type": "cloud", "mix": {"value": 0, "mod": [{"src": "auto.cm", "amount": 1}]}, "density": 18, "size": "90ms",
                             "spray": 0.4, "pitch": 0, "spread": 0.8, "seed": 5},
                            "hp cutoff=200"],
                     "auto": {"cm": cloudmix, **({"vc": lane([(0, 0.05), (st["D"], 0.35), (st["E"], 0.15), (st["outro"], 0.5), (end, 0.5)])} if VINYL else {})}},
            "room": {"fx": ["reverb kind=plate decay=2.4s mix=1 predelay=20ms", "hp cutoff=250"]},
            "pads": {"fx": [pump, {"type": "freeze", "mix": {"value": 0, "mod": [{"src": "auto.fz", "amount": 1}]}, "size": "400ms", "hold": 1}],
                     "auto": {"fz": frz}, "sends": {"room": "-10dB"}},
        },
        "tracks": [
            *([{"name": "zeros", "patch": "fb-crystal", "gain": f"{ZEROS}dB", "pan": 0.3, "sends": {"room": "-14dB"}, "score": T["zeros"]}] if ZEROS else []),
            {"name": "word", "patch": "dx-epiano", "gain": "-9dB", "pan": -0.1,
             "fx": [{"type": "stutter", "chance": {"value": 0, "mod": [{"src": "auto.sc", "amount": 1}]}, "slice": "1/16", "repeats": 3,
                     "decay": 0.3, "mix": 1, "seed": 8},
                    *([{"type": "chop", "slices": 8, "pattern": "0 r1 2 2 . r5 6 _", "mix": {"value": 0, "mod": [{"src": "auto.ch", "amount": 1}]}}] if CHOP else []),
                    *([f"peak cutoff=2500 q=0.6 gain={WORDPRES}dB"] if WORDPRES else []),
                    *([{"type": "follow-noise", "tone": float(FILL), "hold": "8s", "mix": {"value": 0, "mod": [{"src": "auto.hole", "amount": 1}]}}] if FILL else []),
                    *([f"orbit {WORDORB}"] if WORDORB else [])],
             "auto": {"sc": stut, **({"ch": chl} if CHOP else {}),
                      **({"hole": {"points": [["0b", 0], [f"{sec_start('refresh') / 4 - 0.05:g}b", 0], [f"{sec_start('refresh') / 4 + 0.25:g}b", 1],
                                              [f"{sec_start('refresh') / 4 + 15.5:g}b", 1], [f"{sec_start('refresh') / 4 + 16:g}b", 0]]}} if FILL else {})}, "sends": {"line": "-4dB", "room": "-12dB"}, "score": T["word"]},
            *([{"name": f"org{j}", "patch": "farfisa", "gain": "-17dB", "pan": (-0.35, 0.35)[j], "sends": {"room": "-14dB"}, "score": T[f"org{j}"]} for j in range(2)] if ORGAN else []),
            *([{"name": "plate", "gain": "-15dB", "pan": -0.15,
                "patch": {"about": "a struck metal plate: the modal layer's plate modes, a long dense ring",
                          "synth": {"layers": [{"type": "modal", "modes": "plate", "decay": "5s", "strike": 0.45, "bloom": 0.2,
                                                "bright": {"value": 0.55, "mod": [{"src": "vel", "amount": 0.3}]}}],
                                    "amp": {"a": "1ms", "d": "6s", "s": 0, "r": "3s", "curve": 3}},
                          "play": {"vel_sens": 0.6}},
                "sends": {"line": "-6dB", "room": "-10dB"},
                "score": " ".join(f"R/{(a - b) / 4:g}b {hz(50)}/{4 * BAR / 4:g}b@100" if b < a else f"{hz(50)}/{4 * BAR / 4:g}b@100"
                                  for a, b in zip([sec_start(x) for x in (["refresh"] + (["E"] if "E" in PLATEHIT else []))],
                                                  [0] + [sec_start("refresh") + 4 * BAR]))}] if PLATEHIT else []),
            *([{"name": "wtab", "gain": f"{WTABLE}dB", "pan": 0.05, "out": "pads",
                "patch": {"about": "the stored word as a waveform: its 16 bits are the table's harmonics 2-17",
                          "synth": {"layers": [{"type": "wavetable", "frames": WT["frames"],
                                                "position": {"value": 0, "mod": [{"src": "auto.wp", "amount": 1}]}}],
                                    "amp": {"a": "800ms", "d": "1s", "s": 0.85, "r": "2s"}}},
                "auto": {"wp": {"points": [["0b", 0]] + [[f"{at / 4:g}b", round(k / max(1, len(WT['frames']) - 1), 4)] for k, (at, *_x) in enumerate(WT["notes"])]}},
                "score": wt_score()}] if WTABLE else []),
            *[{"name": f"pad{j}", "patch": (UPPAD if UPPAD and j >= 2 else PDPADP if PDPADS else "juno-pad"), "gain": f"{UPPADGAIN if UPPAD and j >= 2 else (PDPADS if PDPADS else -20)}dB",
               **({"lfo": {"sweep": f"sine rate=1/{12 + 4 * j}"}, "fx": ["chorus mix=0.3", *([f"peak cutoff=1400 q=0.8 gain=-{os.environ.get('C8T8_PDCUT', '5')}dB"] if os.environ.get("C8T8_PDCUT", "5") else [])]} if PDPADS and j < 2 else {}), "pan": (-0.4, -0.15, 0.15, 0.4)[j], "out": "pads", "score": T[f"pad{j}"]} for j in range(4)],
            *([{"name": "hum2", "patch": "sub-sine", "gain": "-14dB", "score": T["hum2"]}] if HUMOCT else []),
            *([{"name": "hum", "patch": "808", "gain": HUMGAIN, "fx": [{"type": "filter", "kind": "lp", "cutoff": 120, "q": 0.7}], "score": T["hum"]}] if HUM else []),
            {"name": "bass", "patch": "808", "gain": "-9dB", "fx": [pump], "score": T["bass"]},
            {"name": "kick", "patch": KPATCH if KITOWN else "909", "gain": os.environ.get("C8T8_KITGAIN", "-3dB") if KITOWN else "-3dB", "score": T["kick"]},
            *([{"name": "shk", "patch": "dusty-kit", "gain": "-12dB", "pan": 0.3, "fx": [{"type": "filter", "kind": "hp", "cutoff": 3500, "q": 0.7}], "score": T["shk"]}] if SHAKE else []),
            {"name": "hats", "patch": HPATCH if OWNHATS else "909", "gain": "-9dB", "pan": 0.15, "score": "swing16=0.56 " + T["hats"]},
            {"name": "clap", "patch": CPATCH if HANDS in ("clap", "both") else "909", "gain": os.environ.get("C8T8_HANDSGAIN", "-13dB") if HANDS in ("clap", "both") else "-9dB", "sends": {"room": "-8dB"}, "score": T["clap"]},
            *([(sung_track(f"{SUNG}dB") if WORDS else reversed_back(sung_track(f"{SUNG}dB"), [sec_start("outro") + 8 * BAR], 1.758, 2.253))] if SUNG else []),
            *([reversed_back(voice("chirpers8-t8-say.json", "say", SAYOFFS, f"{VOX}dB",
                     ["hp cutoff=180"], {"line": "-2dB", "room": "-12dB"}), SAYOFFS, 1.421, 2.188)] if VOX and not WORDS else []),
            *([voice(f, nm, [o], f"{VOX}dB", ["hp cutoff=180"], {"line": "-2dB", "room": "-12dB"})
               for f, nm, o in zip(("chirpers8-t8-say-kept.json", "chirpers8-t8-say-both.json", "chirpers8-t8-say-around.json"), ("say", "say2", "say3"), SAYOFFS[-3:])]
              if VOX and WORDS else []),
            {"name": "rim", "patch": RPATCH if HANDS in ("rim", "both") else "909", "gain": "-12dB", "pan": -0.3, "sends": {"line": "-14dB"}, "score": T["rim"]},
            *([{"name": "hats2", "patch": HPATCH if OWNHATS else "909", "gain": "-9dB", "pan": 0.15, "score": "swing16=0.56 " + T["hats2"]}] if SKEW == "local" else []),   # last, so no other track's dice move
            *([{"name": "kick2", "patch": KPATCH if KITOWN else "909", "gain": os.environ.get("C8T8_KITGAIN", "-3dB") if KITOWN else "-3dB", "score": T["kick2"]}] if CKICK else []),
            *([{"name": "mar", "patch": "modal-marimba", "gain": "-12dB", "pan": 0.2, "score": T["mar"]}] if MARE else []),
        ],
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "vars", "tempo", "ceiling", "loudness", "seed", "tail", "event_stable", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
