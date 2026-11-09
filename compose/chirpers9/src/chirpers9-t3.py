#!/usr/bin/env python3
"""chirpers9-t3 (Accretion, track 3: the first storm). Composed by chirper-two.

THE FIRST STORM. Three cycles of different lengths run against the bar: E1 (t1's cell, 12 sixteenths), E2 (t2's
rhythm cell, 5 sixteenths) and E3, this track's element - a progression on a 2+2+3-beat harmonic rhythm (28
sixteenths) - each started at the phase that makes all of them, and the bar, land together on bar 88's downbeat. Before
it they collide (polymeter, a broken 909 and a chip-noise kit, stutters and crush that the storm's own lanes deepen);
from bar 72 the parts assemble bar by bar; at bar 88 every cycle meets one downbeat and the storm LOCKS into one
groove (E3 re-barred 2+2+4, E2 and E1 re-barred into 4/4). A whispered voice ("nothing here is late") arrives in
pieces through the storm and whole at the lock, where a robot (pvoc) sings it on E1's notes. The last 16 bars fall
into t4: redshift (pitch lanes sinking, the master closing) at the seam's 108 bpm.

E1 and E2 are PROVISIONAL until t1/t2 post theirs in compose/chirpers9/motifs.md; the phase maths takes any cycle.
Writes songs/chirpers9-t3.yaml (or T3_OUT). Original music.
"""
import json
import math
import re
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("T3_OUT", os.path.join(ROOT, "songs", "chirpers9-t3.yaml"))

BARS, BPB = 128, 4
TOTAL = BARS * BPB
SECTIONS = [("infall", 0, 16), ("front", 16, 40), ("eyewall", 40, 72), ("lock", 72, 88), ("crest", 88, 112),
            ("outfall", 112, 128)]
# round 2 (section, w9 = bars 96-108, the crest's middle): T3_R2=crab (default) - a crab canon: a glass descant plays
# the locked undertow BACKWARDS three octaves up while the bass plays it forwards; a 909 ride opens the hats; a snare
# fill and an eighth's silence before bar 104, a crash on it. T3_R2=none reproduces v1.
R2 = os.environ.get("T3_R2", "crab") != "none"
# round 3 (palette): T3_R3=ring (default) - two swaps. E1's lead: the album's staple nes-pulse-lead (5 songs) -> a3-ring,
# a saw RING-MODULATED by an inharmonic sine (layer ringmod, which no preset uses), the ring mix 0.85 through the storm
# and 0.1 from the lock (the storm resolves in the timbre too). The storm's snare: the 909 (3 songs) -> ks-drum, a
# Karplus-Strong skin tuned to the key (D4, ghosts on A4), until the lock, where the 909 takes over. =none reproduces v2.
R3 = os.environ.get("T3_R3", "ring") != "none"
# round 4 (section, w7 = bars 72-84, the lock assembling, flagged static): T3_R4=align (default) - the arithmetic made
# audible. Glass ticks count the bar's downbeats upward through D Phrygian (D5 Eb5 F5 G5 A5 Bb5 C6, two bars a step, to
# the break), and every downbeat where a cycle ALREADY lines up with the bar - E1 at bars 73, 78, 83; E2 and E3 together
# at 74 and 81 - lands an alignment hit (crash, kick, a shard chord), the double ones after an eighth of held breath.
# Bar 88 is where all of them line up at once. T3_R4=none reproduces v3.
R4 = os.environ.get("T3_R4", "align") != "none"
# round 5 (section, w10 = bars 109-120, the crest cooling into the outfall; the mix-window out-seam had +32 dB at
# 10-15 kHz against t4's body): T3_R5=cool (default) - THE CREST COOLS TO ITS CORE. The top drops away layer by layer
# (hats to eighths at 109, quarters at 110, the octave lead out at 110, and in the last two bars before the crossfade
# the snare, hats, percussion, chip voices, arps and shards all gone) until only kick, undertow, floor, the clean E1
# lead and the robot's last line remain over the dust pad swelling in Dm(add9); and a glass line plays E1 in
# RETROGRADE, slowing - x2 (bars 109-110), then x4 an octave down (111-114) - a melody falling out of the lock.
# T3_R5=none reproduces v4.
R5 = os.environ.get("T3_R5", "cool") != "none"
# round 6 (Harry, 6 Nov 00:30: "ugly chaos ... atonal ... missing aesthetics and catchiness/hook ... play with time
# and texture"): T3_R6=tonal (default) - TONE IS HOME. E3 v2: the undertow on D | Bb | C (i - VI - VII), harmony
# Dm(add9) | Bbmaj7 | C(add9), no Neapolitan ground; the tracker arps walk those chords' own consonant intervals; the
# ring lead's modulator at 2:1 (harmonic sidebands, in tune) instead of 1.414; the alignment count climbs D Aeolian
# (E, not Eb); and THE HOOK - E1 stated plainly, upright and doubled, for two cycles at the top of the front (bar
# 17), the eyewall (41) and after the eye (67), so the storm's fragments are heard against the tune.
# T3_R6=none reproduces v5.
R6 = os.environ.get("T3_R6", "tonal") != "none"
# round 7 (section, w8 = bars 85-96, the lock arriving): T3_R7=sung (default) - THE HOOK IS SUNG. Harry: hooks want a
# voice that sings tunes cleanly. At the lock a legato singing voice (wM's voice-legato, unused on the album) sings
# "nothing here is late" ON E1 - five syllables, five notes, D A C G E in the seed's own rhythm - at bars 91 and 95,
# alone: the E1 lead steps out of those bars and answers in the bars after (call and response); the pvoc robot keeps
# only its later echoes (101, 109). T3_R7=none reproduces v6.
R7 = os.environ.get("T3_R7", "sung") != "none"
SUNG_BARS = (90, 94)
# round 9 (palette): T3_R9=tight (default) - A PLAYED KIT AND HANDS. (1) The 909 (an album staple: t2, t3, t5) gives way
# on every drum track to tight-kit - dry, close-miked, damped kick, tight snare, crisp rimshot and sidestick (the
# Smile / GoGo Penguin kit; no other Accretion track has it): the storm sounds played, not programmed (kh -> k, the
# clap -> sidestick). (2) A new part on congas (no other track has hand drums): E2's cell (hits 0 2 3 5 of seven:
# tumba / open / slap / muted, its D A F C as low-high-mid-low) cycling in sevens through the front (bars 25-40) and
# the eyewall's end (61-72), then at the lock it takes ONE MORE SIXTEENTH - the seven becomes eight - and sits on the
# bar through the crest. T3_R9=none reproduces v8.
R9 = os.environ.get("T3_R9", "tight") != "none"
# round 10 (WHOLE): T3_R10=accrete (default) - THE VOICE BECOMES THE SONG'S THREAD. With wM's voice-legato pinned
# (joined syllables, an inhale before each phrase, a wandering vibrato, smooth glides), t3's singer is a small near
# voice (tract 0.86, breath 0.35, ring 0.15, drier - t8's choir keeps the big dark one), and it carries E1 through
# the song instead of appearing once: (1) a distant wordless hum of E1 ("oo") in the front at bars 25 and 33 - the
# hook heard before it has words; (2) "nothing here is late" at the lock (91, 95), now legato; (3) the pvoc robot's
# echoes give way to the voice's ANSWER, "everything comes round" on E1 at bars 101 and 109 - the storm's arithmetic
# in five words. Whisper and the dry speech stay (not all singing). T3_R10=none reproduces v9.
R10 = os.environ.get("T3_R10", "accrete") != "none"
SUNG2_BARS, HUM_BARS = (100, 108), (24, 32)
# round 11 (section, w11 = bars 113-128, the overlap into t4 - flagged 'level jump'; the low-end handover agreed with
# chirper-three, 6 Nov 06:05): T3_R11=handover (default) - THE STORM HANDS OVER ITS RESIDUE. (1) The D1 thump stops
# at bar 112 (the floor steps down: the redshifting undertow is the soft floor left, and t4 puts a D2 sine under its
# lens that takes over); (2) a new warm mid pad - two triangles and an octave sine, slow in, a little chorus - holds
# Dm(add9) as D5 F5 A5 E6 (587-1319 Hz) from bar 113 to the end, swelling in: the 600-900 Hz warmth t4's cellos
# inherit, with the F that t4 lifts to F#; (3) the singer's last trace - the E1 hum ("oo") at HALF SPEED, far off,
# from bar 119: the tune handed to t4's handpan, which assembles E1 from its downbeat. T3_R11=none reproduces v10.
R11 = os.environ.get("T3_R11", "handover") != "none"
# round 12 (WHOLE): T3_R12=voices (default) - THE VOICE GATHERS COMPANY. wM's second voice batch is pinned (even
# vowels, singers: N, harmony): (1) t3's singer moves onto voice-near (wM's own close young voice: even vowels, so the
# 'ee' of 'everything' and the 'oo' of the hum no longer sink under the 'ah's) - the lead, the front hum and the last
# hum; (2) NEW: backing voices (voice-backing - three soft breathy singers on each line, even, little ring) sing the
# lock's harmony under the crest from bar 97 to 112 on 'ah', in two diatonic lines that follow Dm | Bb | C | Dm two
# beats a chord - F5 F5 E5 F5 over A4 Bb4 G4 A4 (sixths and a fifth) - 9-11 dB under the lead: the reward gets
# voices, and the crest gets the 600-900 Hz warmth t4's body has (the out-seam's worst band was 877 Hz, -17 dB);
# (3) the eye (bars 63-66) holds its breath on the same backing singers - an open D-A 'oo', four bars, very soft.
# T3_R12=none reproduces v11.
R12 = os.environ.get("T3_R12", "voices") != "none"
# round 13 (WHOLE): T3_R13=clean (default) - THE STORM IN TUNE, WITH ITS WEIGHT. Harry's "ugly chaos" in t3 lives in
# the storm's damage lanes: a 6-bit crush whose mix climbed to 0.6 on the bass and the arps through the eyewall,
# and a stutter firing on 42% of slices. Both eased (crush x0.4: at most 0.24 - grit you feel, not a broken radio;
# stutter x0.6) so the storm's complexity is its cycles and its tune, not its damage; and with the crush off the
# undertow, the bass and its floor come up 2 dB each (the album envelope had 44-97 Hz 8-12 dB light). T3_R13=none
# reproduces v12.
R13 = os.environ.get("T3_R13", "clean") != "none"
# round 14 (palette): T3_R14=boc (default; =air adds the shaker) - A WARM HIGH VOICE (AND, OPTIONALLY, SOME AIR). (1) The E1 line two octaves up (e1hi, the
# hook's top double from the crest on) was a ring-modulated pulse at -21 dB - presence -25 at the crest, unheard.
# It moves to boc-lead (a detuned saw + sine pair drifting in pitch, low-passed, chorused, tape-worn: the
# hauntological lead; no other Accretion track has it) at -12 dB: the seed's top line sung by a wobbly, nostalgic
# synth over the crest. (2) NEW PART - air: tight-kit's shaker in sixteenths through the front and the eyewall (bars
# 17-40 - the front; in the eyewall too it cost recurrence 2.4), accented on E2's seven-cycle (hits 0 2 3 5 of seven, like the congas below it). The
# storm's top end had been the crush's aliasing (v13 eased it; the front fell 14 dB under t2's body at 9 kHz) - now
# it is a played texture. (A tambourine on two and four over the crest brightened the out-seam body against t4:
# cut.) T3_R14=none reproduces v13.
# DEFAULT IS boc: the shaker (T3_R14=air) helped the in-seam flow +1.9 but cost recurrence 1.9 (s0) / 5.8 (s11) -
# the storm's sections stopped returning to each other - so it is kept only as an option.
R14 = os.environ.get("T3_R14", "boc") != "none"
# round 15 (WHOLE): T3_R15=open (default) - THE LOCK OPENS. The crest is the storm's reward, and it was static (the
# sections map: w9 'static, little new vs w8'): Dm | Bb | C | Dm, two beats a chord, for 24 bars. Now, for the eight
# bars of the answer (101-108, "everything comes round"), the lock's last two chords turn: Dm | Bb | F | C - i VI III
# VII, the relative major lifting under the singer, then C falling back to Dm as the crest cools (109). Shards, arps,
# the undertow and its floor move in place (same events, new pitches: C -> F is the riff up a fourth; Dm(add9) -> C
# (add9) note by note), and the backing singers follow (F5 F5 F5 E5 over A4 Bb4 A4 G4). E1 sits on it: its D A C
# over F, its G E over C. T3_R15=none reproduces v14.
R15 = os.environ.get("T3_R15", "open") != "none"
OPEN_BARS = (100, 108)
# round 17 (section, w9 = bars 97-108, the crest's second half, flagged 'static, little new vs w8'): T3_R17=duet
# (default) - CALL AND ANSWER, IN THIRDS. (1) The hook comes back a third time at bar 97 ("nothing here is late"), so
# the crest is a call and an answer, not one line and a groove; the lead steps out of that bar as it does for the first
# two. (2) The call and the answer at bar 101 ("everything comes round") are sung as a DUET: the same small voice with
# a second singer a third above IN THE KEY (wM's harmony_key, D minor: [2] - D/F, A/C, C/E, G/Bb, E/G; every note in
# key). The solo answer at 101 drops to a whisper of itself (velocity) so later notes keep their randomness. (3) The
# skin (ks-drum) falls into the answer: six sixteenths D4 C4 A3 G3 F3 D3 at the end of bar 100. T3_R17=none
# reproduces v16.
R17 = os.environ.get("T3_R17", "duet") != "none"
# round 18 (section, w7 = bars 73-84, the lock assembling, flagged 'static'): T3_R18=pull (default) - THE OLD SEVEN
# PULLS ONCE MORE. (1) For bars 81-84 the kit drops back into the eyewall's sevens (v8's groove: kick, a tuned skin,
# two hats on E2's seven sixteenths), against the congas and the rain, which are already counting eight: the storm's
# old meter tugs at the lock one last time before it closes at bar 85 - and the eyewall's groove comes back instead of
# being left behind. (2) The dry spoken line in bar 83 ("nothing here is") is re-printed with wM's natural rhythm
# (tts --rhythm --join, pinned c5b2c55e: each syllable as long as its sounds, one breath; src/t3/late_r.json), so it
# sounds said rather than placed. Old drums silenced (velocity 1); the sevens on v8's own tracks. T3_R18=none
# reproduces v17.
R18 = os.environ.get("T3_R18", "pull") != "none"
# round 19 (section, w8 = bars 85-96, the held breath and the crest's arrival, flagged 'little new vs w7'):
# T3_R19=arrive (default) - THE CREST LANDS. The reward arrived as more of the lock. (1) The held breath (bars 87-88)
# ends in a snare roll, eight sixteenths rising, into the downbeat. (2) Bar 89 lands: a crash and a long 808 drop on D1
# (the storm's floor, once). (3) The backing singers - who came in at bar 97 - arrive WITH the crest, softer, on the
# lock's chords ("ah", F5 over A4 / Bb4 / G4), under the sung hook (91/95), so the first thing the crest does is open
# into voices. New parts on their own tracks. T3_R19=none reproduces v18.
R19 = os.environ.get("T3_R19", "arrive") != "none"
# round 20 (section, w5 = bars 49-60, the eyewall in sevens, flagged 'little new vs w4'): T3_R20=doo (default) -
# THE VOICE COUNTS SEVEN. The hardest stretch of the storm was all machine: v8's kit in sevens and E1 stretched on the
# glass. NEW: the small singer (voice-near) sings E2 itself on "doo" - D4 A4 F4 C4 on its hits (0 2 3 5 of seven
# sixteenths), locked to the kick's cycle and growing - a human riff you can sing back inside the difficult part; for
# the last four bars (57-60) a second singer joins a third above in the key (harmony_key D minor). Own tracks.
# T3_R20=none reproduces v19.
R20 = os.environ.get("T3_R20", "doo") != "none"
# round 21 (section, w11 = bars 121-128, the outfall into t4, flagged 'level jump'): T3_R21=open (default; =lift and
# =third are the options described here) - THE THIRD LIFTS ON BOTH SIDES. At t4's bar 9 (our 121) chirper-three's pedal steel bends the storm's minor third up,
# F -> F#, into E4's first light (D9) - but our residue and the held Dm(add9) kept singing F under it for the last
# eight bars: a minor third against a major one, right where the album turns warm. Now (1) the residue pad's F5
# lets go at bar 121 and an F#5 swells in over its four-second attack (the bend, on our side), and the held chord's
# F becomes F#; (2) the rain comes back for its last drops, once a bar, fading: E2's cell with the lifted third -
# D5 A4 F#5 C5, which are exactly the tones of t4's D9 - the storm's rain handing over to t4's first light.
# T3_R21=none reproduces v20.
# DEFAULT IS open: the storm LETS GO of its third at bar 121 (F out, no F#) and t4 brings the F#. =lift (F# on our
# side + the rain's D9 drops) and =third (F# only) made our outro D major, which no longer answers the D-minor intro:
# recurrence 96 -> 87 on s11. open: s11 96.71, flow 71.7 -> 74.3 (the out seam reads better).
R21 = os.environ.get("T3_R21", "open") != "none"
# round 22 (palette): T3_R22=breath (default: (2) only; =grit adds (1)) - A FLOOR YOU CAN HEAR, SINGERS WHO BREATHE. (1) The undertow's floor (E3
# an octave down under the reese) was the album staple `sub` - a clean sine five tracks share, which a laptop or a phone
# drops entirely. It moves to sub-saturated (chirper-three's post-dubstep sub: a sine with a triangle and a little saw
# driven through tape, low-passed at 2 kHz so its harmonics carry the line; unused on Accretion): the storm's floor
# keeps its weight and you can now hear it MOVE (D - Bb - C) on small speakers. (2) wM's glide overshoot (pinned
# 59a832d1) on every joined singer: the small singer and the duet 0.07, the backing singers 0.05 - each note change
# swings a little past and settles, instead of landing dead on the pitch. T3_R22=none reproduces v21.
# DEFAULT IS breath (the overshoot only). =grit adds the sub-saturated floor: even at -25 dB it cost recurrence
# (s0 89.7 -> 87.6, s11 -> 86.0; the floor's harmonics make the storm's sections read less alike) - kept as an option.
R22 = os.environ.get("T3_R22", "breath") != "none"
# round 23 (section, w3 = bars 25-36, the front's middle, flagged 'static'): T3_R23=gather (default) - THE FRONT
# GATHERS. Changing what is there rather than adding (the front's recurrence breaks under new rhythmic layers, v16):
# (1) the distant hum of E1 ("oo", bars 25 and 33) is now SUNG - wM's scoop rises into each phrase and its fall lets
# it go (scoop 1, fall 2, a3-hum); (2) the second hum (33) is a duet, a third above in the key (harmony_key D minor);
# (3) for bars 33-36 the three arpeggiators climb an octave, so the front brightens and gathers toward the plain hook
# at bar 41 instead of idling. The old hum notes stay (velocity) so later notes keep their randomness.
# T3_R23=none reproduces v22.
R23 = os.environ.get("T3_R23", "gather") != "none"
# round 24 (section, w9 = bars 97-108, the crest's second half, flagged 'static, little new vs w8'): T3_R24=counts
# (default) - THE VOICE COUNTS EIGHT. After the duet's answer (bars 101-102) the crest just held its groove. Now for
# bars 103-108 the small singer's "doo" riff from the eyewall comes back - E2 itself, D A F C - but in EIGHTS, locked
# to the bar like the congas and the rain at the lock: the voice that struggled in sevens (v20) now counts with the
# crest, a third above in the key from the start (a3-doo3); and the rain (ks-nylon) doubles it an octave up. Both
# are the song's own material returning, transformed. Own tracks / appended events. T3_R24=none reproduces v23.
R24 = os.environ.get("T3_R24", "counts") != "none"
# round 25 (palette): T3_R25=bloom (default) - HELD NOTES BLOOM. wM's per-note vibrato (pinned 58ee9ba3; first use on
# Accretion; I asked for it for this song's last "oo"): on a joined line the vibrato's delay and fade restart with every
# note, so quick notes stay plain and only HELD notes bloom (~280 ms in) - before, the wobble counted from the phrase's
# first note and ran through every quick note after it. On every sung voice: the small singer (call, answer, hook,
# humlast), the duet, the hums and the backing singers. And the crest's singers get the scoop and fall the hums took
# in v23 (scoop 1, fall 2; the backing "ah"s a softer 0.5 / 1). The quick "doo"s stay plain. T3_R25=none reproduces v24.
R25 = os.environ.get("T3_R25", "bloom") != "none"
# round 26 (whole): T3_R26=arc (default) - THE CREST IS THE TOP. The section map read the lock (bars 73-84) as the
# loudest part of the song (-10.9 LUFS) and the crest that it unlocks (89-108) quieter (-11.7): the storm's reward
# arrived smaller than the struggle. (1) The master's dynamics lane is redrawn as one arc: the storm build (41-62)
# and the lock (67-86) sit 1.5 dB lower, the eye (63-66) breathes deeper (-4.5), the break before the crest drops
# further - and the crest (89-112) is untouched, so after mastering it is the loudest thing in the song. (2) The
# crusher retires (as in t7 v25): the grit lane, a 6-bit 9 kHz crush on the kit and the bass through the storm, goes
# to zero; the stutter (time texture) stays. T3_R26=none reproduces v25.
R26 = os.environ.get("T3_R26", "arc") != "none"
# round 27 (section, w4 = bars 37-48, the storm build, flagged 'little new vs w3'): T3_R27=flute (default) - THE HOOK
# SURFACES IN THE STORM. Through the build E1 is only there in shards (the chip line breaks it up, -23 dB under the
# bass and the shards). From bar 41, where the storm rises, a DIZI (bamboo flute, its buzzing membrane; no Accretion
# track has one) plays E1 WHOLE - D5 A5 C6 G5 E5, in the chip line's own register - on the storm's own 5-beat cycle
# against the 4/4 bar: six plain statements, each landing somewhere new in the bar, growing louder towards the eye's
# approach. The hook heard plainly while the time stays complex. And the flute COMES BACK: at the crest it doubles
# the singer's hook an octave above (bars 91, 95 and 109) - the line that surfaced in the storm now sings with her.
# Own track. T3_R27=none reproduces v26.
R27 = os.environ.get("T3_R27", "flute") != "none"
# round 28 (palette): T3_R28=move (default) - THE FLUTE IS THE STORM'S VOICE. v27's dizi came in at bar 41 as a
# stranger (recurrence 96 -> 90: one window unlike any other). But the storm already had a voice for E1's top line:
# boc-lead's statements at bars 17, 41 and 65 (the infall's end, the build, the eye's approach). Those three move to
# the dizi, an octave down in its own register (the one at 41 is already the dizi's own), so the flute is heard from
# bar 17 and returns each time the storm gathers; boc-lead keeps its line over the crest. T3_R28=voice also makes every
# stacked voice sing TOGETHER (wM, pinned 8083e37e) and =together does only that - both cost recurrence (-0.4: the
# breathier, softer stacks), so they stay off. T3_R28=none reproduces v27.
R28 = os.environ.get("T3_R28", "move") != "none"
# round 29 (section, w7 = bars 73-84, the assembly before the lock, flagged 'static'): T3_R29=lands (default) - THE
# FLUTE LANDS ON THE ONE. The song's idea is that every cycle meets one downbeat at bar 89; the dizi's 5-beat E1
# crossed the bar all through the build (v27) and then vanished before the lock. Now it comes back in the assembly on
# the same 5-beat cycle, phased to MEET bar 89: seven statements from bar 74, a rest under the spoken line (bar 83) and
# the break, and then one last E1 exactly on the crest's downbeat - the flute that fought the bar arrives on the one
# with everything else. Appended to the dizi track. T3_R29=none reproduces v28.
R29 = os.environ.get("T3_R29", "lands") != "none"
# round 30 (section, aimed at the 112 s flat run 0:40-2:32 = bars 17-62, the storm - Harry 23:55: "subtle variation so
# it doesn't get boring"; flatness.py read t3 67-69% flat, the worst on the album): T3_R30=breathe (default) - THE
# STORM LIFTS - a phrase that recurs: 12 bars as they were, then 4 bars that LIFT, twice (bars 29-32, under the hum's
# second half, running into v23's arps-up at 33-36; and bars 45-48, the end of the build): the arps and E1's chip line
# go up an octave, the hats thin to eighths, the kick, snare and chip snare step out, and the bass and subs climb an
# octave too (the floor lifts instead of vanishing; the harmony holds) - and it all comes down on the next downbeat. (Two earlier drafts broke the 112 s run with harder moves - four different ones: hats, the floor out, a
# 2 kHz filter close, the shards out; then the floor out twice with a 5 kHz close - and both cratered recurrence
# (91.8 -> 52 / 46) and spectrum: in t3 a floor-less bar is a new section that never returns. Subtle, as asked.)
# T3_R30=none reproduces v29.
R30 = os.environ.get("T3_R30", "breathe") != "none"
# round 31 (section, aimed at the flat runs left after v30 - 1:44-2:32 the eyewall, 2:40-3:20 the assembly, 3:28-4:16
# the crest; Harry 23:55 "subtle variation"): T3_R31=lifts (default) - THE LIFT RETURNS. v30's lift (drums out, hats in
# eighths, bass / subs / arps / chips an octave up, then down on the next downbeat) comes back three more times so it
# becomes the storm's way of breathing: bars 57-60 (the eyewall's second half, under the counted "doo"s) and bars
# 77-80 (the assembly, before the kit pulls into sevens) - the same lift exactly, so it recurs. (Drafts: a third lift
# inside the crest at 105-108 did not break the crest's run and cost spectrum (78.6, s0 -0.7); keeping the sub floor low
# in every lift changed v30's two as well and recurrence fell 99.6 -> 85.2.) T3_R31=none reproduces v30.
R31 = os.environ.get("T3_R31", "lifts") != "none"
# round 32 (palette, aimed at the crest's flat run 3:28-4:16; Harry 23:55 "subtle variation"): T3_R32=round (default)
# - THE ANSWER ON A ROUND BASS. In the crest the storm's bass (a3-grit: a sine phase-modulated by itself, driven) is the
# loudest thing in the mix (+0.4 vs the mix) - its grain IS the crest's texture, which is why 45 s of crest read as one
# block. A new patch, a3-round: a warm sine + triangle with a quiet second harmonic through a 900 Hz low-pass and a
# little drive - E3's undertow played round AND an octave up, a singing bass under the duet's answer and the open
# chords (bars 101-108); the storm's grain comes back down under the last "everything comes round" at 109. (Round
# alone, same octave, did not move flatness: the floor's fundamental is what the measure hears.)
# T3_R32=none reproduces v31.
R32 = os.environ.get("T3_R32", "round") != "none"
# round 33 (palette): T3_R33=deep (default) - THE STORM'S OWN FLOOR. The floor and the sub ran on the album's staple
# `sub` (t2, t3, t6, t8) at an effective -21 dB, and every lift since v30 took the lowest octave away with it: the
# spectrum's worst band sank to 44 Hz -14 dB (spectrum term 89.8 -> 77) and the seam into t4 asks for more at 38-44 Hz.
# A new patch, a3-deep: a sine with a stronger second harmonic (-12 dB) and a little drive, so the floor speaks on small
# speakers as well as in the chest, through a 200 Hz low-pass with a slower release; on both tracks, 6 dB up (3 dB read
# 96.89, 6 dB 97.13 on s0 - the floor wanted its weight back). The
# notes (E3's undertow, the lifts) are unchanged. T3_R33=none reproduces v32.
R33 = os.environ.get("T3_R33", "deep") != "none"
# round 34 (section, aimed at the last flat run 1:44-2:16 - the eyewall's first half, bars 49-56): T3_R34=assemble
# (default) - THE EYEWALL ASSEMBLES. The eyewall used to arrive whole at bar 49: kit, bass, the counted "doo"s and the
# glitch shards (the loudest thing after the bass) all at once, and ran unchanged until the lift at 57. Now it is built
# in front of you: for bars 49-52 the shards hold back, so the eyewall opens on the voices counting in sevens over the
# kit and the bass; the shards crash in at 53. T3_R34=none reproduces v33.
R34 = os.environ.get("T3_R34", "assemble") != "none"
# round 35 (palette): T3_R35=gangsa (default) - E2 AS KOTEKAN. E2 (t2's figure: hits 0, 2, 3, 5 of 7 sixteenths,
# D A F C) ran through 80% of the storm on the library's chip-metal at -18 dB against the mix, masked: grain nobody
# heard. It moves to the library gamelan (gangsa: bronze keys in pairs a few cents apart, so every note beats -
# ombak - with a mallet clang on the attack; no other Accretion track has it) and is split the way gamelan
# splits a figure: kotekan, two interlocking parts - D and F on the left, A and C on the right - so the 7/16 figure
# ping-pongs across the stereo field. Written length is the damping hand: 0.3 beats (was 0.12) lets each key
# ring a moment before the next. Same notes, same times. T3_R35=none reproduces v34.
R35 = os.environ.get("T3_R35", "gangsa") != "none"
# round 36 (palette): T3_R36=glass (default) - E1 ON A FARFISA. The storm's E1 (phased against the bar so it lands on
# bar 88 with E2 and E3) rides my a3-ring - a saw ring-modulated at 1.414:1, inharmonic and metallic - at -21 dB
# against the mix, 80% of the song: the album's hook, smeared and buried. Harry: E1 plain and often; consonant by
# default. A phased ostinato on a reedy combo organ is the Philip Glass Ensemble's own sound, so the library farfisa
# (no other Accretion track has it) doubles E1 note for note on its own track - same fall automation and delay, panned
# opposite the ring - in every other 8-bar phrase (bars 9-16, 25-32, ... 97-104), so the hook steps forward with a
# clear pitch and back again: something moves every 8 bars. The ring keeps the storm's metal edge (1 dB down).
# (Draft: the farfisa on all the time read flatter - flatness 36% -> 39% - and s0 -0.11.)
# T3_R36=none reproduces v35.
R36 = os.environ.get("T3_R36", "glass") != "none"
# round 37 (section, w6 = bars 61-72 - the eye of the storm, never focused): T3_R37=eye (default) - THE HOOK IN THE
# EYE. The eye (bars 63-66) is four bars of stillness inside the storm - an E3 chord on the dust, the sub on D, the
# backing voices holding an open D-A "oo", the hand drum - and nothing sang in it. Now the dizi plays the album's
# hook whole and slow there, plainly, four times augmented: D5 (2 beats) A5 (3) C6 (1) G5 (4) E5 (4), softly, so
# for nine seconds the storm's centre carries the tune every other track chops up; the wall comes back on its E.
# T3_R37=none reproduces v36.
R37 = os.environ.get("T3_R37", "eye") != "none"
# round 38 (section, w2 = bars 13-24 - the storm taking shape after t2's overlap, never focused): T3_R38=gust (default)
# - THE FIRST GUST. The storm's broken machine ran its sixteenth kicks and hats straight through bars 17-24 into the
# hum (bar 25) with only a chip roll to mark it. Now the storm takes its first breath: for bars 23-24 the hats stop
# and the kick holds back to two hits (beats 3 and 1), the skin drum's three-against-four carrying on alone; then a
# tom fill falls through E2's notes (D4 C4 A3 F3, twice, sixteenths, crescendo) under the chip roll, and a crash
# lands the hum's entry. T3_R38=none reproduces v37.
R38 = os.environ.get("T3_R38", "gust") != "none"
# round 39 (whole): T3_R39=swing (default) - THE LOCK SWINGS. The machine ran dead straight sixteenths for five
# minutes. Harry: put the complexity into time, a fun tune. The storm stays straight - a machine - but when every
# cycle lands together on bar 89 and the band locks into its groove, it starts to SWING: every generated part's
# off-sixteenths sit 0.025 beats late for bars 89-104 (swing 0.55, the light swing chirpers1's ninefold riff
# settled on), the whole band in one pocket so nothing flams; the voices keep their own phrasing; it straightens
# again before t4's overlap so the hand-off's sixteenths agree with t4's. Difficult ->
# rewarding, in the feet. (Draft: swing on the whole song - s0 -0.02 but flatness 36% -> 39%, the storm smoothed.)
# T3_R39=none reproduces v38.
R39 = os.environ.get("T3_R39", "swing") != "none"
# round 40 (section, w9 = bars 97-108 - the crest's answer, flagged static): T3_R40=parts (default) - THE STORM PARTS
# FOR THE ANSWER. The crest's middle ran everything at once for 25 s - shards, glass, perc, kit, arps, both basses, the
# duet's answer and the doos - so the answer ("everything comes round") was sung into a wall. Now for bars 101-104,
# the first half of the answer, the shards, the glass and the perc step out: the duet sings over the round bass, the
# kick, the backing voices, the doos and the rain - and at bar 105 the storm crashes back in under the second half.
# T3_R40=none reproduces v39.
R40 = os.environ.get("T3_R40", "parts") != "none"
# round 41 (section, w6/w7 seam = bars 67-76 - the storm's return after the eye, flatness's longest rut left:
# 2:40-3:04, three 8 s blocks alike): T3_R41=foretell (default) - THE ANSWER, FORETOLD. After the eye the wall comes
# back and runs unchanged into the lift at 77. Now it returns in stages, as the eyewall first assembled (v34): bars 67-70
# without the shards; then for bars 71-74 the storm's grainy bass hands its line to the round bass, an octave up - the
# voice the crest's answer will be sung over (v32, bars 101-108), heard here first - and at 75 the grit and the shards
# are both back. A promise the crest keeps. (Draft: the round bass alone moved the rut's two changes 0.49/0.36 ->
# 0.61/0.67, still under the 0.691 line, and s0 -0.08.)
# T3_R41=none reproduces v40.
R41 = os.environ.get("T3_R41", "foretell") != "none"
# round 42 (whole): T3_R42=breathe (default) - THE UNDERTOW BREATHES. The storm's floor is E3's undertow riff, the
# loudest thing in the mix, and it ran the same sixteenth figure under almost the whole song: flatness's ruts (0:48,
# 1:28-1:36, 3:36-3:44) were all the riff unbroken. Now, three times - the storm's first phrase after t2's overlap (bars
# 17-20), the middle of the storm (37-40) and under the sung hook at the crest (91-94) - the riff slows to its own
# roots, two long notes a bar (the lowest note of each half bar held: D, Bb, C - E3 augmented), over the floor, the
# kick and everything above; then the riff drives again. The same gesture each time, so it recurs.
# T3_R42=none reproduces v41.
R42 = os.environ.get("T3_R42", "breathe") != "none"
# round 43 (section, w3 = bars 25-36 - the voices' first entry, after the gust): T3_R43=mmm (default) - THE HUM IS A
# HUM. The "hum" (bar 25, E1 whole, the album's first voice in t3) was always sung on an open "oo", and so was its
# answer a third apart at bar 33: two open statements, nothing between them. wM's closed-mouth hum (pinned e3da830a,
# chirper-three's request) makes it what it was called: the mouth shut, the voice through the nose - a murmur near
# 270 Hz with the "m"'s dip at 1.1 kHz - 4 dB up (high hums are quieter), and an octave below it a second singer
# hums on "n" (2 dB under). Then at bar 33 the voices OPEN onto "oo" with their third: the song's first singing grows
# from a hum into a vowel, the way a voice warms up. T3_R43=none reproduces v42.
R43 = os.environ.get("T3_R43", "mmm") != "none"
# round 44 (section, w4 = bars 37-48 - "little new vs w3", flatness's ruts at 1:28-1:52): T3_R44=wall (default) - THE
# STORM BEHIND A WALL. After the undertow's breath (bars 37-40) the riff came back exactly as before and the lift at
# 45 arrived out of nothing. Now when the riff returns at bar 41 the whole storm is heard through a wall: the master
# low-pass (the outro's "close" lane, open at 20 kHz all song) drops 4.4 octaves to ~950 Hz - kick, riff and floor
# pass, the hats, chips and farfisa go muffled - eases open a little over three bars, then gives way in the last half
# bar, so the lift at 45 (drums out, everything up an octave) bursts out bright, and the storm slams back at 49.
# A DJ's filter, used once. T3_R44=none reproduces v43.
R44 = os.environ.get("T3_R44", "wall") != "none"
# round 45 (section, w9 = bars 97-108 - "static, little new vs w8", the window with the least groove motion; E1, the
# album's hook, buried under the round bass there: the ring and its octave at audibility 0): T3_R45=melodica (default)
# - A MELODICA ANSWERS. The two singers sing E1 at bars 97 and 101 ("nothing here is late", "everything comes round")
# and then nothing sings for seven bars until the last "everything comes round" at 109. Now a melodica - the dub
# lead, reedy and breathy, the album's first; no other track has one - answers in the gaps with E1 plainly, in the
# voices' register: bar 99 (E1), 103 (E1), 105 (E1 backwards - E G C A D - so it comes home to D) and 107 (E1, its
# last E held into the singer's entry). The hook in a human, slightly wobbly voice, heard plainly at last before the
# storm hands over to t4. T3_R45=none reproduces v44.
R45 = os.environ.get("T3_R45", "melodica") != "none"
# round 46 (section, w8 = bars 85-96 - "little new vs w7"; the lock): T3_R46=lock (default) - THE LOCK, HEARD. The
# whole song is built so that E1, E2 and E3 - cycles of 12, 7 and 28 sixteenths - meet on one downbeat at bar 89, and
# the storm locks into a groove there. But at the lock only E3 (the undertow, the loudest thing) could be heard:
# E1's farfisa sat at -16 dB and the ring at -20, E2's gangsa at -17, all masked. Now for the lock's eight bars the
# three cycles step forward together so you hear them interlock: E1's farfisa +8 dB (the ring +4), E2's gangsa +6
# and its chip +4, the undertow 3 dB back - in full for bars 89-90 and 93-94, half under the singer's two phrases
# (91, 95), back to before at 97. Only levels move; the notes were always there. T3_R46=none reproduces v45.
R46 = os.environ.get("T3_R46", "lock") != "none"
# round 47 (section, w6 = bars 61-72 - "little new vs w5"; the eye): T3_R47=still (default) - IN THE EYE, TIME SLOWS.
# The eye (bars 63-66) took the storm away - dust chord, sub on D, the dizi's slow E1, the voices' held "oo" - but
# kept the storm's clock: the accelerando (98 -> 108 bpm over the song) ran straight through it, so it read as a
# thinner bit of the same storm. Now time itself stills there: from bar 62 the tempo eases down to 80 bpm, holds
# for the dizi's long notes, and from bar 65 winds back up to exactly where the accelerando would have been as the
# wall slams back at 67. Complexity in time, not pitch: no note moves. The ramp still reaches 108 for t4's seam.
# T3_R47=none reproduces v46.
R47 = os.environ.get("T3_R47", "still") != "none"
# round 48 (palette): T3_R48=sub (default) - THE UNDERTOW GETS A BODY. compscore --bands: t3 is 7-13 dB short of the
# album from 38 to 97 Hz and 5-8 dB over it from 547 to 1404 Hz - the storm's floor is E3's undertow on the grit
# bass, the loudest thing in the song, and its grit is all mids. Now a pure sine (the library sub-sine; no other
# track has it) plays the undertow note for note an octave below - Bb0 to D2, the 29-73 Hz octave the song was
# missing (at the grit's own pitch it cancelled the grit's fundamental: 50-100 Hz did not move) - with its breaths
# (held roots) and lifts, and steps out from bar 113 so the fall into t4 and the seam stay as they were. T3_R48=none reproduces v47.
R48 = os.environ.get("T3_R48", "sub") != "none"
# round 49 (whole): T3_R49=warm (default) - THE STORM LOSES ITS HONK. compscore --bands: t3 sat 5-8 dB over the album
# from 547 to 1404 Hz (the grit's mids, the shards, the ring) - a boxy, honking middle across the whole song - and
# t2's seam heard the same (t3's body +11.8 dB at 877 Hz against t2's) - and 10-13 dB short at 44-61 Hz, where the
# kick's body and the new sub live. The master EQ now scoops the middle (-3 dB at 900 Hz, an octave and a half wide)
# and lifts the chest (+3 dB at 55 Hz), so the storm is warmer and heavier and the limiter gives the low end and the
# air the room the honk was taking. T3_R49=none reproduces v48.
R49 = os.environ.get("T3_R49", "warm") != "none"
# round 50 (section, w10 = bars 109-120 - the last voice before t4; focused least recently): T3_R50=round (default)
# - EVERYTHING COMES ROUND, AS A ROUND. The storm's last sung line (bar 109) is "everything comes round", E1 whole,
# one voice - and then nothing sang again. Now it goes round: a second singer takes it up a beat and a half later
# (panned left, a slightly larger voice), a third a beat and a half after that (right, a slightly smaller one), so
# the hook overlaps itself in a three-voice canon - mostly fifths, fourths, thirds and sixths, a passing second that
# resolves as the next note comes - and the last "round" lands alone, two bars before t4 arrives. The voice accretes
# again, in the words' own shape. T3_R50=none reproduces v49.
R50 = os.environ.get("T3_R50", "round") != "none"
# round 51 (section, w5 = bars 49-60, the eyewall in sevens; focused least recently): T3_R51=pan (default) - THE HOOK
# IN SEVENS. The eyewall's groove counts sevens (E2's cell, 7 sixteenths a cycle) and E1 - eight notes long, 3.5
# beats - is exactly two of its cycles, yet there the hook was buried (ring -28 dB, the glass's stretched E1 -14.5,
# farfisa -22). Now a steel pan (the album's first: bright, singing, its octave blooming after the strike) plays E1
# at its own speed, an octave over the counting voices, locked to the sevens: E1, then E1 backwards (E G C A D, home
# to D), then two cycles' rest, four times - forward and back, a playground tune riding the storm's cross-rhythm,
# into the lift at 57. T3_R51=none reproduces v50.
R51 = os.environ.get("T3_R51", "pan") != "none"
# round 52 (whole song): T3_R52=pump (default) - THE STORM BREATHES. The low end was a wall: the grit bass is the
# loudest thing in every window (+0.1 dB over the mix), its octave-under sine and the deep floor under it, and the
# kick - the storm's actual pulse - sat buried beneath them (-10 to -36 dB). Now all three dip under every kick
# (the storm's and the eyewall's sevens) and swell back - the album's own pump (t2 and t6 breathe the same way:
# -6 dB, 200 ms, curve 0.6) - so the storm moves in and out with its own heartbeat, the kick lands, and the low end
# leaves room between hits. T3_R52=none reproduces v51.
R52 = os.environ.get("T3_R52", "pump") != "none"
# round 53 (whole song): T3_R53=letgo (default) - THE STORM LETS GO, ON A BREATH. Two ends of one arc. (1) Since v52
# the storm's low end is heavier throughout, and it stayed heavy right up to the crossfade - so the last bars before
# t4 (bar 113 on) pressed on t4's head at 61-83 Hz (chirper-three measured it). Now the grit bass, its sine and the
# floor ease down 3 dB over bars 105-113: the storm thins as the round sings, and hands t4 a lighter floor. (2) The
# storm's last word (bar 119, E1 sung slowly) ended on E and hung there; nothing answered. Now one closed hum - the
# same mouth-shut voice that first sang at bar 25, held even by hum_even - takes D4 at bar 121 and holds it under
# t4's head: E resolves to D, home, a breath instead of a thinning, gone before t3 ends. Agreed with chirper-three:
# D only (no F or F#, t4's third is theirs), a few dB under their handpan. T3_R53=none reproduces v52.
R53 = os.environ.get("T3_R53", "letgo") != "none"
# round 54 (section, w1 = bars 1-16, the head under t2's tail, flagged 'static', never focused): T3_R54=horizon
# (default) - THE STORM ON THE HORIZON. t3 is the album's first storm, yet its head was only dust, E2's chip cell
# and (from bar 9) E1 on the ring and farfisa - nothing said a storm was coming. Now it is heard far off before it
# arrives: wind (the album's first) gusts under the head, and thunder - timpani rolling on the home D, far back in
# the hall - answers it: wind high, then a roll into bar 9 (where E1 enters, on its hit), wind high again, then a
# longer, louder roll breaking into bar 17 - gust and thunder taking turns, so the head changes every few bars
# instead of sitting in one wash. No pitch but D, so nothing in it touches t2's last
# chords. T3_R54=none reproduces v53.
R54 = os.environ.get("T3_R54", "horizon") != "none"
# round 55 (section, w9 = bars 97-108, the duet after the lock, flagged 'static, little new vs w8'): T3_R55=choir
# (default) - THE CHOIR ANSWERS. Here the duet sings both lines ("nothing here is late", "everything comes round")
# over two backing "aa" pads that were buried (-14 and -18 dB) and moved in lockstep under everything - so the twelve
# bars after the lock sounded like the lock continued. Now the pads become a choir (six singers a side, spread wide,
# each with its own vibrato - wM's vib_spread, pinned da77da08) that steps back while the duet sings and swells
# into the gaps, answering each line; and the duet's harmony singer gets her own vibrato too, so the two voices
# breathe apart. T3_R55=none reproduces v54.
R55 = os.environ.get("T3_R55", "choir") != "none"
# round 56 (palette): T3_R56=swarm (default) - THE SWARM THAT LOCKS. The song's whole idea is phase: E1, E2 and E3
# on cycles of 12, 5 and 28 sixteenths, drifting, meeting on one downbeat (beat 352) where the storm locks into a
# groove - but no sound in it had ever been out of phase and found its phase. Now one does: the storm's chords from
# the eye to the lock (the shards' changes, held, an octave up) on a Kuramoto swarm - ten triangles a note, each a
# little off its pitch, pulled toward their common phase by a coupling the song turns up. After the eye it is a loose,
# shimmering, out-of-tune chorus; it tightens through the second storm, passes the critical coupling near the end,
# and at the lock snaps into one clean tone with everything else - then holds the lock's chords, focused, until bar
# 97. (wM's kuramoto layer with its coupling on a lane, as t2's crest pad and t8's jet chords use it; here the lock is
# the song's own phase lock, a whole storm long.) T3_R56=none reproduces v55.
R56 = os.environ.get("T3_R56", "swarm") != "none"
# round 57 (section, w2 = bars 13-24, where the storm lands; focused least recently): T3_R57=drift (default) - THE HOOK
# SLIPS. When the storm lands at bar 17 the dizi states E1 twice - and was buried under the arriving low end (-16 dB)
# - and then the hook went on only as the ring's fragments, E1 restarting every 12 sixteenths so it slides against
# the bar (the song's whole idea: phase), buried at -25 dB. Now the dizi's second statement comes forward (+6 dB:
# the first stays inside the storm's landing, so the hook emerges from it, and t2's seam is untouched), and
# the dizi stays: it plays the ring's drifting fragments through bars 19-24, so you hear the tune itself slip a beat
# against the bar each time round - the phase the storm is built on, as a melody - until the hum takes over at 25.
# T3_R57=none reproduces v56.
R57 = os.environ.get("T3_R57", "drift") != "none"
# round 58 (section, w7 = bars 73-84, the second storm gathering; focused least recently): T3_R58=hands (default) - THE
# HANDS TAKE OVER. In bars 77-80 the kick and snare already rest, but the hats ran on and the congas kept their
# two-beat loop buried under everything (-18 dB, the same four strokes since bar 25). Now for those four bars the
# hats and the old loop stop and the congas come forward with E2's own cell - slap, open, open, low on sixteenths
# 0 2 3 5 of every seven, so the hand pattern turns over against the bar like the eyewall did - and the last bar is
# a conga roll swelling into bar 81, where the kit comes back for the pull to the lock. T3_R58=none reproduces v57.
R58 = os.environ.get("T3_R58", "hands") != "none"
# round 59 (whole song): T3_R59=space (default) - THE STORM'S SPACE. t3 had one stereo picture all song, however the
# weather changed. Now the space is part of the storm: (1) a master width lane - the head as it was (t2 is closing to
# a point above it, so the storm opens the field), wide when the storm lands at bar 17, drawn in tight around the
# middle in the eye (bars 63-66, the calm centre - you are inside it), wide again for the second storm, widest of all
# on the lock (bar 89), then settling back to as-is through the duet and the tail so t4 meets the picture it
# expects; bass untouched (mono_below off). (2) The voices become sections: every part sung by several voices - the
# backing pads, the counted "doo"s and hums in harmony, the choir, the duet - gets wM's vib_spread and vowel_spread
# (pinned a1f7f0ec), so each singer has her own vibrato and her own vowels instead of one voice copied.
# T3_R59=none reproduces v58.
R59 = os.environ.get("T3_R59", "space") != "none"
# round 60 (whole song): T3_R60=weather (default) - CALM THAT IS CALM. The album's arc is calm -> storm -> relief,
# but inside t3 the weather barely moved in level: the eye (bars 63-66) sat only 3 dB under the storm around it, the
# second storm came back no louder than the first, and everything from bar 17 to the end played within 2 dB. Now the
# master's dynamics follow the weather: the eye drops away (-9 dB: a real lull, the storm audible all round you but
# far off - it is also drawn in narrow since v59), the second storm slams back at full height, the held breath before
# the lock stays under it, the lock itself is the loudest moment in the song (+1.5), easing back to the old level by
# the tail (t4's seam untouched); the first storm's landing sits 0.5 dB higher to meet t2's tail as before (the
# deeper eye moved the master's compression). And the lines sung from tts pitch paths in harmony (the duet, the hum and the counted
# "doo"s) get f0_spread (pinned 473b5266), the spread that reaches their vibrato - vib_spread could not.
# T3_R60=none reproduces v59.
R60 = os.environ.get("T3_R60", "weather") != "none"
# round 61 (section, w8 = bars 85-96, the held breath and the lock; "little new vs w7"): T3_R61=lock (default) -
# THE SEVEN LOCKS INTO EIGHT. All storm long E2 ran in sevens (hits 0, 2, 3, 5 of 7 sixteenths), rolling over the beat;
# at the lock (bar 89) the music squares up - but the only part playing E2 squared (0, 2, 3, 5 of 8) was the buried
# conga loop. Now a brass section says it: punchy stabs (library brass-stab, the album's first) on E2's locked
# rhythm, four to every chord of the lock's Dm - Bb - C - Dm, D-minor triads under the farfisa's E1 - and they answer
# the voice: silent while she sings "nothing here is late", back in every gap. T3_R61=none reproduces v60.
R61 = os.environ.get("T3_R61", "lock") != "none"
# round 62 (palette): T3_R62=birds (default) - BIRDS IN THE EYE. In a hurricane's eye the air goes still, the sky can
# clear, and birds caught up in the storm fly there. Since v60 t3's eye (bars 63-66) is a real lull, but nothing lived
# in it. Now birds do (library birds, no other chirpers song uses it): two flocks, left and right, chirping in short
# clusters on D minor's pentatonic (D F G A C, octaves 6-7: consonant, high above everything) through the eye - and
# halfway through one bird whistles the hook, E1 (D A . C G E) at double speed, the album's tune in a bird's mouth.
# After the lock, when the duet has finished singing (bars 102-103), a few birds come back: the storm has passed.
# T3_R62=none reproduces v61.
R62 = os.environ.get("T3_R62", "birds") != "none"
# round 63 (whole song): T3_R63=ground (default) - THE GROUND ARRIVES; THE SINGERS BREATHE. (1) When the storm landed
# at bar 17 every layer of sub came in at once - the floor's D1/C1, a sub-sine down to B-flat 0 and the 808 - a wall
# of 30-45 Hz under the first beat (25 dB above t2's tail there, the album's biggest jump at a seam). Now the storm
# lands with its kick, bass and 808 as before, and the deepest ground - the floor and the sub-sine - swells up under
# it over eight bars (-12 dB -> full), so its full weight arrives at bar 25 with the hum: the storm getting heavier
# as you go in. (2) The voices breathe: the solo lines (the sung "nothing here is late", the duet, the round's
# voices) draw a breath before each phrase (wM's inhale, pinned), and the choirs stand in depth with their
# consonants not quite together (depth_spread, cons_spread). T3_R63=none reproduces v62.
R63 = os.environ.get("T3_R63", "ground") != "none"
# round 64 (whole song): T3_R64=clear (default) - CLEAR AIR. Against the album t3 sat boxy and dull: +5.8 dB at
# 640 Hz and +5.6 at 1.4 kHz (the honk of the horns, the farfisa and the shards piled up), 1-4 dB short of air above
# 5 kHz, and at both its seams 11 dB short at 400 Hz (the warmth under the voices) next to t2 and t4. Now the master
# takes the honk out (-3 dB at 640 Hz and 1.4 kHz, narrow), puts the warmth back (+2 dB at 400 Hz, broad) and opens
# the top (+2.5 dB shelf from 9 kHz): the storm sounds like weather outdoors rather than a band in a box.
# T3_R64=none reproduces v63.
R64 = os.environ.get("T3_R64", "clear") != "none"
# round 65 (whole song): T3_R65=passes (default) - THE STORM PASSES. Since v63 the storm's ground swells up under its
# first eight bars; but it never left - the floor, the sub-sine and the 808 sat at full weight through the duet and the
# round to the end, so the relief carried the storm's whole weight and t3's tail stood 14.5 dB heavier at 61 Hz than
# t4's head. Now the ground recedes as it arrived: from bar 101, while the duet sings, the floor and the sub-sine
# sink (-6 dB by bar 109, -9 by 113) and the 808's sub with them (-6), so the relief gets lighter as the storm moves
# off, and the tail floats into t4. (A shallower floor with the bass's E3 eased 4 dB was tried: the seam's level
# matched better but its spectrum and the song's did worse, 99.48.) The song's low end is now an arc: arriving 17-25, full through both storms and the
# lock, leaving 101-113. T3_R65=none reproduces v64.
R65 = os.environ.get("T3_R65", "passes") != "none"
# round 66 (section, w4 = bars 37-48, the first storm's middle; "little new vs w3"): T3_R66=foretold (default) - THE
# WORDS BEFORE THE SONG. From bar 41 the dizi and the farfisa play E1 over and over, but under the reese, the floor and
# v44's wall they sat 17-22 dB down: the hook was there and nobody could hear it; and the whisper said only two words
# of the lyric ("here", "late"). Now, as the wall opens at bar 45, the dizi's E1 comes up 6 dB, plain for three bars -
# and a second whisper says the whole line, "nothing here is late", on E1's rhythm (its five syllables are E1's five
# notes), twice, a breath behind the dizi: the words the voice will sing at the lock (bar 90), heard first in the
# storm as a whisper. (The dizi drops back for bar 48, so the eyewall's entry at 49 still turns a corner - lifted
# through 48 it read flat there.) T3_R66=none reproduces v65.
R66 = os.environ.get("T3_R66", "foretold") != "none"
# round 67 (palette): T3_R67=shepard (default) - A RISE THAT NEVER ARRIVES, THEN THE LOCK. The held breath before the
# lock (bars 85-88) had the library's noise riser - the one t7 used too - buried 17 dB down under the roll, and the
# lock landed on an 808 boom alone. Now: an endless Shepard riser (library fx-riser-endless, no
# Accretion or chirpers song has used it) runs through the four bars - a tone and a barber-pole filter climbing an
# octave every two beats, forever, never getting there: the storm's phases sliding towards a meeting that keeps not
# happening - and it is cut dead when they do meet, at the lock (a bar early was tried: no better on the flatness
# read at the lock, and less of a cut); the lock now lands on tuned toms too (library
# modal-tom), A1 picking up into a big D2 on top of the 808 (swapping the 808 out entirely took its long sub tail
# from the lock, and the bars after it read flat). T3_R67=none reproduces v66.
R67 = os.environ.get("T3_R67", "shepard") != "none"
# round 69 (section, w6 = bars 61-72, the eye and the second storm's arrival; least recently focused):
# T3_R69=scatter (default) - THE BIRDS SCATTER, THE TUNE COMES BACK. Since v62 birds sing in the eye; when the back
# wall of the storm hit at bar 67 they just stopped, and the dizi, playing E1 into the returning storm, sat 17 dB
# under the reese. Now as the storm hits, the birds scatter: a burst of rising runs, hard left and right, faster and
# higher for a bar, then gone - and the dizi's E1 comes up 8 dB for those two bars, so the storm returns carrying
# the tune. T3_R69=none reproduces v67.
R69 = os.environ.get("T3_R69", "scatter") != "none"
# round 70 (section, w5 = bars 49-60, the eyewall; least recently focused outside the t4 seam): T3_R70=undertow
# (default) - THE BASS SINGS THE HOOK INTO THE EYE. All through the storm the reese (and the sub-sine an octave
# under it) is the loudest thing, leaping about E3's riff. For the four bars before the eye (57-60) it now plays E1
# itself, plainly, three times - D A C G E, low and huge, under the steel pan's E1 and the counting voices - then
# climbs the D minor scale into the eye. The riff's own bars there are silenced with a lane, not edited.
# T3_R70=none reproduces v69.
R70 = os.environ.get("T3_R70", "undertow") != "none"
# round 71 (section, w9 = bars 97-108, after the lock: the duet, the melodica's E1, the choirs; least recently focused
# outside the seams and w3): T3_R71=halfbreath (default) - THE GROOVE HALVES, HOLDS ITS BREATH, SLAMS BACK. The
# lock's groove ran straight through w9. Now for bars 103-104, while the melodica plays E1 and the counting voices
# come in, the kit drops to half time (kick on one, snare on three, hats in quarters, the 808 with the kick), and on
# the last beat of bar 104 the drums and the round bass stop dead - only the voices and the choir hang there - until
# the crash at bar 105 brings the whole groove back under the melodica's E1 backwards. The kit's own bars there are
# silenced with a lane, not edited. T3_R71=none reproduces v70.
R71 = os.environ.get("T3_R71", "halfbreath") != "none"
# round 72 (section, w7 = bars 73-84, the second storm before the break; least recently focused outside the seams and
# w3): T3_R72=phase (default) - THE PHASE MARGIN, HEARD. Here is the song's title: the dizi and the farfisa play E1
# once every FIVE beats, so it slides against the four-beat bar - but both sat 18-22 dB under the reese, and nobody
# could hear the slide. Now a vibraphone (library vibes, motor tremolo; no Accretion song has one) plays E1 on every
# bar, D4 A4 C5 G4 E4, plain, and the dizi comes up 10 dB: two E1s, one on the bar and one a beat later each time,
# drifting apart and back together every five bars (they meet at bars 74, 79, 84) - Reich's phasing, the storm's
# margin, audible. T3_R72=none reproduces v71.
R72 = os.environ.get("T3_R72", "phase") != "none"
PHASE_GAIN = os.environ.get("T3_PHASE_GAIN", "0dB")
# round 75 (palette): T3_R75=roomhats (default) - THE STORM'S HATS FROM A ROOM. The album's staple is a hat: haake-hat,
# inside tight-kit and dusty-kit, rings in five of the eight songs - t3's 1,200 hats among them (hats, hats7 and the
# v71 half-time hatshalf). Now they play the library's rock-kit hats - a live kit's washy hats in a room, darker when
# touched softly, brighter when hit (no Accretion song plays rock-kit): the same notes, lanes and fx, but a drummer's
# hats, and air on the storm's top (t3's in-seam body reads 9 kHz -9.9 dB against t2's). T3_R75=none reproduces v72.
R75 = os.environ.get("T3_R75", "roomhats") != "none"
ROOMHAT_GAIN = os.environ.get("T3_ROOMHAT_GAIN", "10dB")
# round 76 (section, w4 first part = bars 37-44, the first storm at full; least recently focused of w4-w7, the windows
# clear of the flow bodies and recurrence anchors): T3_R76=risset (default) - THE TUNE SHIMMERS. Bars 37-44 had the
# reese and the kit and every melody buried 18-23 dB down. Now E1 is held there, four times slower than itself - D A
# C G E over four bars, then again an octave up - on a Risset arpeggio (library risset-arpeggio, forked here as
# a3-risset: five copies of a ten-harmonic tone, each a few cents apart, so each held note beats into an arpeggio
# across its own overtones). The fork spreads the copies four times wider than the library's (+-12.6 cents), so the
# overtones ripple about once a second instead of once every few: phase made audible, the title's idea in a tone
# (no Accretion song uses it). It rises into bar 45, where the whisper starts. T3_R76=none reproduces v75.
R76 = os.environ.get("T3_R76", "risset") != "none"
RISSET_GAIN = os.environ.get("T3_RISSET_GAIN", "0dB")
# round 77 (palette - an engine feature the album has not used): T3_R77=phase (default) - THE VOICES PHASE. The
# eyewall's counting voice (doo: D A F C on sixteenths, bars 49-56) is doubled, the copy panned against it, and the
# copy's own clock is warped (track `warp`, unused on Accretion): over bars 49-52 it drifts steadily ahead until it
# is a sixteenth early, holds there two bars - the one pattern against itself, a new tune in the gaps - then eases
# back into step for bar 57, where the harmony voices take over in unison: Reich's Piano Phase on a voice, the
# title's phase margin opened and closed. Each copy is 2 dB up (at -2 they sat 14.5 dB under the reese, unheard).
# T3_R77=none reproduces v76.
R77 = os.environ.get("T3_R77", "phase") != "none"
# round 78 (whole): T3_R78=breathe (default) - THE STORM GETS ITS WEIGHT AND LOSES ITS BOX; THE BAND BREATHES. (1)
# Against the album t3 is hollow at 44-61 Hz (-6.5 / -6.6 dB, past tolerance) and boxy at 290-640 (+3 to +5): a
# narrow master lift at 50 Hz (+3 dB, q 1.4) puts weight under the reese, and a broad dip at 340 (-3.5 dB, q 0.9)
# takes the cardboard out of the storm's middle - on lanes, from bar 33 to bar 96, flat over the flow bodies at
# either end (as fixed EQ they cost the seams: flow 97.4 -> 93.0, 400 Hz -10.5 against t4's head). (2) The storm was played on the grid; now it has a shared feel (as
# t7 since v76): the band drifts ahead and behind together, about 5 ms, a turn every four bars, kicks pushing 4 ms
# early and snares and claps sitting 6 ms late - the storm leaning forward. T3_R78=none reproduces v77.
R78 = os.environ.get("T3_R78", "breathe") != "none"
# round 79 (section, w6 = bars 61-72, the eye; least recently focused of w4-w7): T3_R79=eye (default) - THE EYE GOES
# STILL. The eye of the storm still had the whole engine running under it (the reese loudest, the kick and both subs).
# Now for four bars (61-64) the kick, the 808, the sub and the reese stop dead: what is left is the wind (dust), the
# birds, the shards - and the dizi playing E1, lifted 6 dB so it is heard plainly, over a wordless choir holding
# D minor (add 9) and then B-flat (add 9). At bar 65 the storm comes back in on D. Also the seam fix chirper-three
# asked for: v78's master lanes (50 Hz up, 340 down) now ease out over bars 93-96, ending before the out-body
# (bars 97-112) that t4 is measured against - which did not move it: the cost was v78's song feel (with it the tail's
# 133 Hz read +1.5 dB against t4's head, spectral 2.96 -> 3.15; without it 2.96 again, and 99.877 against 99.83), so
# v79 also takes the feel back out. T3_R79=none reproduces v78.
R79 = os.environ.get("T3_R79", "eye") != "none"
# round 80 (section, w5 = bars 49-60, the eyewall; least recently focused of w4-w7): T3_R80=eyewall (default) - THE
# VOICES COME BACK, AND THE STORM FALLS INTO THE EYE. (1) v78's 340 Hz dip took the counting voices' phasing (v77)
# back under the reese (doo / doop -14.5 dB, 0.06-0.11 audible): doo, doop and the harmony voices doo3 come up 5 dB.
# (2) The eye (bar 61) arrived with no fall: now bar 60 is a fill on the rock kit - snare eighths climbing, then the
# toms in sixteenths, high to floor - and one crash on the eye's first beat, ringing on over the stillness.
# T3_R80=none reproduces v79.
R80 = os.environ.get("T3_R80", "eyewall") != "none"
FILL_GAIN = os.environ.get("T3_FILL_GAIN", "3dB")
# round 81 (palette - swap an album staple): T3_R81=samba (default) - THE DEBRIS ON REAL METAL. The storm's debris
# ticks (chiphat: E2's scatter on an 8-bit noise hat, bars 5-72; nes-noise-hat is a staple t5 and t8 share) move to
# hand percussion no Accretion song has: the library samba-kit's pandeiro jingles on the accents and its ganza (a
# metal shaker) on the rest - the same hits, the same velocities. The chip track is muted and copied, not edited.
# T3_R81=none reproduces v80.
R81 = os.environ.get("T3_R81", "samba") != "none"
# round 82 (whole): T3_R82=vortex (default) - THE STORM TURNS AROUND YOU. The storm's air stood still in the stereo
# field. Now it circles the listener (orbit fx, Chowning's moving sources; distance 0 and no Doppler, so no pitch
# bends and no level change - only where it is): the wind (dust, the whole song) a lap a bar, the glass shards on a
# figure of eight two laps a bar, the swarm four laps a bar - all on one speed lane: barely turning in the calm head,
# winding up through the eyewall, STOPPED in the eye (bars 61-64), spun hard into the lock (bar 89), then winding
# down to stillness for t4. T3_R82=none reproduces v81.
R82 = os.environ.get("T3_R82", "vortex") != "none"
# round 83 (palette - add the part the song lacks): T3_R83=strings (default) - STORM STRINGS. t3 had no strings. Now a
# real section (library violins: four bowed players, physical strings; no Accretion song uses them) plays the storm's
# old trick - a measured tremolo, sixteenths - as a halo over the run-up to the lock, bars 73-84: an open fifth on D
# (D4 A4), up an octave at bar 77, the minor third (F5) joining at bar 81 and the top D at 83, swelling from almost
# nothing to full and cut dead at bar 85, where the riser takes over. A pedal, so it sits over D, B-flat and C
# alike (the E3 riff under it). T3_R83=none reproduces v82.
R83 = os.environ.get("T3_R83", "strings") != "none"
# round 84 (whole): T3_R84=fills (default) - A DRUMMER AT THE PHRASE ENDS. Harry (6 Nov): subtle variation every 8-16
# bars, no stretch where nothing changes - and the storm's kit ran its cycles without ever marking a phrase (flat
# boundaries at 56, 112-120, 176, 200-248 s). Now a drummer (rock-kit, under the kit) closes the eight-bar phrases
# (and a few four-bar ones where the flat boundaries were) with a one-beat fill - snare sixteenths, a run down the
# toms, a snare-tom flam, a two-beat run into the bigger turns - each phrase a different one, so it never loops; at
# the eye's end (bar 64) a two-beat fill and a crash bring the storm back in. Skipped where a fill or break already
# is (eyefill 60, the lock roll 88, the fill at 100, the half-breath 103-104). T3_R84=none reproduces v83.
R84 = os.environ.get("T3_R84", "fills") != "none"
# round 85 (whole): T3_R85=ride (default) - THE DRUMMER MOVES TO THE RIDE. The kit's top was the same hats for 100
# bars, and the flattest changes left (bars 70-77, 80-87, 94-101, 101-108) sit in long hat-led stretches. Now, as a
# drummer would, four eight-bar phrases move off the hats onto the ride (rock-kit: ride eighths, the bell on the
# off-beats): bars 41-48, 73-80 (under the storm strings) and the lock (89-96: the bell on every beat, the groove's
# new shine) - the hats stepping back 6 dB for each, so the top of the kit changes colour phrase by phrase. (A fourth,
# bars 105-112, sat in the out-body t4 is measured against: flow 97.6 -> 76.9.) T3_R85=none reproduces v84.
R85 = os.environ.get("T3_R85", "ride") != "none"
# round 87 (whole): T3_R87=punch (default) - THE STORM HITS HARDER. The storm's kit (tight-kit, the rock-kit's hats,
# ride and fills, the karplus drums) went straight to the master, thin and boxy under the reese. Now it is sent in
# parallel to a drum bus (library rack drum-bus-punch: slower-attack compression so the transients punch, light
# saturation, +2.5 dB at 62 Hz and -3.5 at 420 - the weight t3 lacks and the box it has - and a tight room; no
# Accretion song uses it), blended under the dry kit. The bus fades in after the in-seam body (by bar 37) and out
# before the out-body (by bar 101), so neither seam moves. T3_R87=none reproduces v85.
R87 = os.environ.get("T3_R87", "punch") != "none"
# round 88 (section, w4 = bars 37-48, the whisper's bars before the eyewall; least recently focused of w4-w7):
# T3_R88=toms (default) - THE DRUMS GO TO THE TOMS. Bars 43-50 were t3's flattest change since v87 (0.49): the same
# kit ran from the ride phrase into the eyewall. Now for bars 47-48 the kit (kick, hats, ride, the karplus and chip
# snares) stops, and a tom figure takes over - E2's rhythm (hits 0, 2, 3, 5 of seven sixteenths) walking down the
# rock-kit's toms, high to floor, under the whisper's "nothing here is late" - crossing into the eyewall's first bar
# (to beat 196), where the seven-cycle kit picks it up. One block of drums on their own skin. T3_R88=none reproduces v87.
R88 = os.environ.get("T3_R88", "toms") != "none"
TOMS_GAIN = os.environ.get("T3_TOMS_GAIN", "-5dB")   # at 0: -0.3 dB, louder than the reese
RIDE_GAIN = os.environ.get("T3_RIDE_GAIN", "3dB")   # at 0: -14.8 dB (0.09) at bars 41-48; at 5 spectrum 99.2
FILLS_GAIN = os.environ.get("T3_FILLS_GAIN", "-3dB")
STRINGS_GAIN = os.environ.get("T3_STRINGS_GAIN", "14dB")   # at 0: -27 / -22 dB, buried
SAMBA_GAIN = os.environ.get("T3_SAMBA_GAIN", "10dB")   # at 0 it read -20.5 dB (the chip it replaces: -31, buried)   # at 6 it read -2.9 dB, near the reese   # rock-kit hats sit 7 dB under tight-kit's
R28_MOVE = os.environ.get("T3_R28", "move") in ("voice", "move")
R28_TOG = os.environ.get("T3_R28", "move") in ("voice", "together")
R22_FLOOR = os.environ.get("T3_R22", "breath") == "grit"
R21_DROPS = os.environ.get("T3_R21", "open") == "lift"
R21_OPEN = os.environ.get("T3_R21", "open") == "open"          # let go of the third (no F#): t4 brings it
DOO = {0: 62, 2: 69, 3: 65, 5: 60}
PULL = (80, 84)
CALL_BAR, FILL = 96, ((2.5, 74), (2.75, 72), (3.0, 69), (3.25, 67), (3.5, 65), (3.75, 62))
# round 16 (section, w3 = bars 25-36, the front's middle, flagged 'static', never focused): T3_R16=rainonly (default;
# =rain adds the held breath) -
# RAIN ON THE GLASS, AND A HELD BREATH. (1) NEW: a nylon string (ks-nylon - wM's Karplus-Strong pluck; no other
# Accretion track has it) plays E2 in its own pitches - D5 A4 F5 C5 on hits 0 2 3 5 of seven sixteenths, cycling
# across the bar line with the congas below it (the hands' cell gets its notes), swelling over the twelve bars, a
# 3/16 echo behind it like rain on a window. (2) The storm holds its breath: the last two beats of bar 32 drop the
# kit and the undertow - only the rain, the hum and the pads - and the storm lands again with the hum's second "oo"
# at bar 33. The rain returns at the lock's assembly (bars 73-88) in EIGHTS, like the congas (the seven takes one more
# sixteenth): the front's texture comes back as the storm's arithmetic resolving. Old notes silenced (velocity 1), the
# rain on its own track. T3_R16=none reproduces v15.
# DEFAULT IS rainonly: the held breath (=rain or =breath) cut recurrence 96.4 -> 91 (the 2-beat stop splits the front
# into a section of its own that never returns) - kept as an option.
R16 = os.environ.get("T3_R16", "rainonly") != "none"
R16_RAIN = os.environ.get("T3_R16", "rainonly") in ("rain", "rainonly")
R16_BREATH = os.environ.get("T3_R16", "rainonly") in ("rain", "breath")
RAIN_CELL = ((0, 74), (2, 69), (3, 77), (5, 72))                       # E2: D A F C, up an octave+
R14_AIR = os.environ.get("T3_R14", "boc") in ("air", "shaker")
R14_BOC = os.environ.get("T3_R14", "boc") in ("air", "boc")
# round 8 (section, w5 = bars 49-60, the eyewall's first half, flagged 'little new'): T3_R8=seven (default) - TIME,
# NOT NOISE. The storm's random Euclid drums give way for 12 bars to ONE groove in sevens: E2's cell (hits 0 2 3 5 of
# 7 sixteenths) as kick / hat / snare / hat, cycling across the bar line - a cross-rhythm you can follow - and over it
# the glass sings E1 STRETCHED x2 (D A C G E, ten beats a statement) three times: the hook as a long line above the
# storm. T3_R8=none reproduces v7.
R8 = os.environ.get("T3_R8", "seven") != "none"
CLEAR = []      # R4: the bar-82 statement, spoken clearly (the voice clears as the arithmetic does)
CREST = 88                      # the bar every cycle lands on
CREST16 = CREST * 16            # ... in sixteenths
EYE = (62, 66)                  # the eye of the storm: four bars of stillness inside it
BREAK = (86, CREST)             # the held breath before the lock
SEAM_IN, SEAM_OUT = 98, 108     # mixplan: t2>t3 98, t3>t4 108, flat across each 16-bar overlap

# ---- the elements -------------------------------------------------------------------------------------------
# E1, the seed (t1, chirper-zero): D A C G E, short long SNAP long held, and a beat's rest: 5 beats = 20 sixteenths.
E1 = [("D4", 0.5), ("A4", 0.75), ("C5", 0.25), ("G4", 1.0), ("E4", 1.5)]
E1_LEN16 = 20
# E2, "seven" (t2, chirper-one): hits on 0 2 3 5 of 7 sixteenths, pitched D A F C.
E2_LEN, E2_HITS = 7, (0, 2, 3, 5)
E2_PITCH = {0: ("D5", 112), 2: ("A5", 84), 3: ("F5", 98), 5: ("C5", 76)}
# E3, "the undertow" (THIS TRACK'S ELEMENT): a bass riff of 7 beats - E2's seven sixteenths augmented x4 - on D, the
# Neapolitan Eb (the storm's flat second, the darkness the inner disk's sharp fourth will answer) and C: (note, beats).
E3_RIFF = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("Eb2", 0.5), ("Eb2", 0.75), ("Bb1", 0.75), ("C2", 0.75),
           ("C2", 0.75), ("G2", 0.5), ("C3", 1.0)]
E3_LEN16 = 28
# ... and the storm's harmony over it, one chord per riff segment (2 + 2 + 3 beats), D4 common to all three.
E3 = [((50, 57, 64, 65), 2.0),            # Dm(add9):      D3 A3 E4 F4
      ((51, 58, 62, 67, 69), 2.0),        # Ebmaj7(#11):   Eb3 Bb3 D4 G4 A4   (the Neapolitan, lydian)
      ((48, 58, 62, 65), 3.0)]            # C11 (Bb/C):    C3 Bb3 D4 F4
E3_LOCKED = [2.0, 2.0, 4.0]               # re-barred at the lock: 2+2+4 = two bars (the riff's last C held a beat)
if R6:                                    # E3 v2: D | Bb | C, consonant
    E3_RIFF = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("Bb1", 0.5), ("Bb1", 0.75), ("F2", 0.75), ("C2", 0.75),
               ("C2", 0.75), ("G2", 0.5), ("C3", 1.0)]
    E3 = [((50, 57, 64, 65), 2.0),        # Dm(add9):  D3 A3 E4 F4
          ((46, 53, 57, 62, 65), 2.0),    # Bbmaj7:    Bb2 F3 A3 D4 F4
          ((48, 55, 62, 64), 3.0)]        # C(add9):   C3 G3 D4 E4
# the lock under R6 resolves HOME every two bars (D minor, not C): harmony Dm | Bb | C | Dm (2+2+2+2) and the riff's
# held last beat becomes C -> D
LOCK_SEQ = [(0, 2.0), (1, 2.0), (2, 2.0), (0, 2.0)]


def lock_riff():
    if R6:
        return E3_RIFF[:-1] + [("C3", 0.5), ("D3", 1.5)]
    return E3_RIFF[:-1] + [(E3_RIFF[-1][0], E3_RIFF[-1][1] + 1.0)]
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(n):
    return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + (1 if "#" in n else -1 if "b" in n[1:] else 0)


def mtok(m):
    return f"m{m:g}"


def sec_of(bar):
    for name, a, b in SECTIONS:
        if a <= bar < b:
            return name
    return "outfall"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        if at < 0 or at >= TOTAL:
            return
        self.ev.append((round(at, 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self):
        ev = sorted(self.ev, key=lambda e: e[0])
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else TOTAL
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt if ln <= gap + 1e-6 else s + gap
        if TOTAL - pos > 1e-4:
            toks.append(f"R/{TOTAL - pos:.4g}b")
        return " ".join(toks) if toks else f"R/{TOTAL}b"


def euclid(k, n, rot=0):
    pat = [((i * k) % n) < k for i in range(n)]
    return [pat[(i + rot) % n] for i in range(n)]


def cycle_starts(length16, lo16, hi16):
    """Cycle starts (in sixteenths) of a LENGTH16 cycle phased to land on the crest, within [lo16, hi16)."""
    first = CREST16 - length16 * math.ceil((CREST16 - lo16) / length16)
    return list(range(first, hi16, length16))


# ---- patches (inline, this track's own; 'a3-' = Accretion t3) -------------------------------------------------
PATCHES = {
    "a3-grit": {"about": "chirper-two: the storm's bass - a sine phase-modulated by itself an octave up, the index "
                         "thrown on each attack, through drive and a low-pass: a hard, grainy low end, not a squelch",
                "synth": {"layers": [{"name": "m", "ratio": 2, "audible": False},
                                     {"wave": "sine", "pm": [{"from": "m", "depth": {"value": 0.15, "mod": [
                                         {"src": "env.bite", "amount": 0.9}]}}]},
                                     {"wave": "sine", "ratio": 0.5, "level": "-9dB"}],
                          "env": {"bite": {"a": "0.5ms", "d": "70ms", "s": 0.1, "r": "40ms"}},
                          "drive": 0.35,
                          "filters": ["lp cutoff=1400 q=0.8"],
                          "amp": {"a": "2ms", "d": "300ms", "s": 0.7, "r": "60ms"}},
                "play": {"mono": True, "glide": "12ms"}},
    "a3-shard": {"about": "chirper-two: crushed chord shards - two detuned saws and a 1:3.01 PM edge, a fast filter "
                          "snap; the storm's stabs and, held, the lock's chords",
                 "synth": {"layers": [{"wave": "saw", "detune": -9}, {"wave": "saw", "detune": 9},
                                      {"name": "e", "ratio": 3.01, "audible": False},
                                      {"wave": "sine", "level": "-6dB",
                                       "pm": [{"from": "e", "depth": {"value": 0.05, "mod": [
                                           {"src": "env.snap", "amount": 0.6}]}}]}],
                           "env": {"snap": {"a": "0.5ms", "d": "90ms", "s": 0.0, "r": "30ms"}},
                           "filters": [{"kind": "lp", "q": 1.2, "cutoff": {"value": 900, "mod": [
                               {"src": "env.snap", "amount": 3.2}]}}],
                           "amp": {"a": "1ms", "d": "180ms", "s": 0.45, "r": "90ms"}}},
    "a3-dust": {"about": "chirper-two: the infall's dust - a dark saw pad, slow in and out, for the cloud to shred",
                "synth": {"layers": [{"wave": "saw", "detune": -6}, {"wave": "saw", "detune": 6},
                                     {"wave": "triangle", "ratio": 2, "level": "-10dB"}],
                          "filters": ["hp cutoff=110", "lp cutoff=2200 q=0.5"],
                          "amp": {"a": "900ms", "d": "1s", "s": 0.8, "r": "1.6s"}}},
    "a3-tracker": {"about": "chirper-two: the tracker arp - an NES pulse whose stepped LFO walks the chord's own "
                            "intervals every 32nd, retriggered per note (a 1990s module's arpeggio command)",
                   "synth": {"layers": [{"type": "chip", "chip": {"kind": "pulse", "duty": 0.25}}],
                             "amp": {"a": "1ms", "d": "120ms", "s": 0.55, "r": "40ms"}}},
}
ARP_STEPS = {0: [0, 7, 14, 15, 19], 1: [0, 7, 11, 16, 18], 2: [0, 10, 14, 17, 22]}   # chord intervals over each root
if R6:
    ARP_STEPS = {0: [0, 7, 14, 15, 19], 1: [0, 7, 11, 16, 19], 2: [0, 7, 14, 16, 19]}  # m(add9) | maj7 | add9


def arp_patch(steps):
    p = json.loads(json.dumps(PATCHES["a3-tracker"]))
    p["synth"]["lfo"] = {"arp": {"steps": steps, "rate": "1/32", "retrig": True}}
    p["synth"]["pitch"] = {"value": 0, "mod": [{"src": "lfo.arp", "amount": 1}]}
    return p


for _i, _st in ARP_STEPS.items():
    PATCHES[f"a3-arp{_i}"] = arp_patch(_st)


def build():
    rng = random.Random(9)
    T = {k: Track(k) for k in ("kick", "snare", "hats", "perc", "chipsn", "chiphat", "bass", "shard", "arp0",
                               "arp1", "arp2", "e1", "e1hi", "e2", "dust", "sub", "hold", "riser", "whisper", "robot", "floor",
                               "glass", "tick")}

    # ---- E3: the progression -------------------------------------------------------------------------------
    # infall: augmented x2 on the dust pad (14-beat cycle), phased to the crest as well
    for c in cycle_starts(56, 0, 16 * 16):
        at = c / 4.0
        for (ch, beats) in E3:
            if 0 <= at < 64:
                T["dust"].add(at, beats * 2 - 0.1, ",".join(mtok(m) for m in ch), 62)
            at += beats * 2
    # the storm: 2+2+3, shards struck on displaced sixteenths, the bass on the roots, tracker arps above
    for c in cycle_starts(28, 16 * 16, CREST16):
        at = c / 4.0
        for k, (ch, beats) in enumerate(E3):
            bar = int(at // 4)
            sec = sec_of(bar)
            if at >= 64:
                hits = 0 if (sec == "front" and bar < 28) else 2 if sec == "front" else 3
                for h in range(hits):
                    off = rng.choice([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if h else rng.choice([0, 0.25, 0.5])
                    if off < beats:
                        T["shard"].add(at + off, 0.2, ",".join(mtok(m) for m in ch), 88 + rng.randint(-10, 14))
                if sec in ("eyewall", "lock"):
                    T[f"arp{k}"].add(at, beats - 0.05, mtok(ch[0] + 12), 70 + (8 if sec == "eyewall" else 0))
            at += beats
    # E3 itself, the undertow, in the storm: the riff on its 7-beat cycle, glitched (dropped notes, octave throws)
    for c in cycle_starts(E3_LEN16, 16 * 16, CREST16):
        at = c / 4.0
        for n, ln in E3_RIFF:
            sec = sec_of(int(at // 4))
            if at >= 64:
                if not (sec == "eyewall" and rng.random() < 0.12):
                    up = 12 if (sec == "eyewall" and rng.random() < 0.15) else 0
                    T["bass"].add(at, ln * 0.85, mtok(midi(n) + up), (108 if ln >= 0.75 else 94) + rng.randint(-8, 8))
            at += ln
    # the floor under it: a sine an octave below the riff's long notes, the storm's and the crest's 30-80 Hz
    for c in cycle_starts(E3_LEN16, 16 * 16, 112 * 16):
        at = c / 4.0
        for n, ln in (E3_RIFF if at < CREST * 4 else lock_riff()):
            if ln >= 0.75 and 64 <= at < 112 * 4 and not (EYE[0] * 4 <= at < EYE[1] * 4 or BREAK[0] * 4 <= at < BREAK[1] * 4):
                T["floor"].add(at, ln * 0.9, mtok(midi(n) - 12 if midi(n) >= 36 else midi(n)), 90)
            at += ln
    # the lock and after: re-barred 2+2+4, steady
    for bar in range(CREST, 112, 2):
        at = bar * 4.0
        for k, beats in (LOCK_SEQ if R6 else list(enumerate(E3_LOCKED))):
            ch = E3[k][0]
            T["shard"].add(at, 0.22, ",".join(mtok(m) for m in ch), 96)
            T["shard"].add(at + 0.75, 0.22, ",".join(mtok(m) for m in ch), 78)
            if beats > 2:
                T["shard"].add(at + 2.5, 0.22, ",".join(mtok(m) for m in ch), 84)
            T[f"arp{k}"].add(at, beats - 0.05, mtok(ch[0] + 12), 78)
            T["hold"].add(at, beats - 0.1, ",".join(mtok(m + 12) for m in ch[1:]), 70)
            T["sub"].add(at, beats - 0.1, mtok(ch[0] - 24), 70)
            at += beats
        at = bar * 4.0
        for j, (n, ln) in enumerate(lock_riff()):              # the riff, re-barred: its last C held a beat more
            ln2 = ln
            T["bass"].add(at, ln2 * 0.88, mtok(midi(n)), 112 if ln >= 0.75 else 98)
            at += ln2
    # the outfall: E3 augmented again, falling into t4; the D4 common tone held over the seam
    for i, bar in enumerate(range(112, 120, 4)):                 # the riff augmented x2, falling
        at = bar * 4.0
        for n, ln in E3_RIFF[:6] if i == 0 else E3_RIFF[6:]:
            T["bass"].add(at, ln * 1.8, mtok(midi(n)), 96 - 8 * i)
            at += ln * 2
        ch = E3[i % 3][0]
        T["dust"].add(bar * 4.0, 15.8, ",".join(mtok(m) for m in ch), 70)
    T["dust"].add(120 * 4.0, 31.8, ",".join(mtok(m) for m in E3[0][0]), 74)   # Dm(add9) held: t4 lifts its third
    T["sub"].add(112 * 4.0, 16 * 4.0 - 0.2, "m62", 60)              # the D4, held into the next track

    # ---- E1: the cell (12 sixteenths), displaced and inverted in the storm, upright at the lock -----------------
    e1m = [midi(n) for n, _ in E1]
    for c in cycle_starts(E1_LEN16, 8 * 16, CREST16):
        at, bar = c / 4.0, int(c // 16)
        sec = sec_of(bar)
        inv = sec in ("front", "eyewall") and rng.random() < 0.5
        if sec == "infall" and rng.random() < 0.5:
            continue
        shift = rng.choice([0, 0.25, 0.5]) if sec in ("front", "eyewall") else 0
        for (n, ln), m in zip(E1, e1m):
            mm = 2 * e1m[0] - m if inv else m
            if sec == "eyewall" and rng.random() < 0.25:
                continue                                         # fragments
            T["e1"].add(at + shift, ln * 0.9, mtok(mm + 12), 74 + rng.randint(-8, 8))
            at += ln
    for bar in range(CREST, 112):
        at = bar * 4.0
        for (n, ln), m in zip(E1, e1m):
            T["e1"].add(at, ln * 0.92, mtok(m + 12), 84)
            if bar >= CREST + 8:
                T["e1hi"].add(at, ln * 0.92, mtok(m + 24), 70)
            at += ln

    # ---- E2: the rhythm cell (5 sixteenths) on the chip-metal channel, then barred at the lock -----------------
    for c in cycle_starts(E2_LEN, 0, CREST16):
        if c < 16 * 16 and rng.random() < 0.6:              # the infall: t2's cell arriving in pieces
            continue
        for h in E2_HITS:
            n, v = E2_PITCH[h]
            T["e2"].add((c + h) / 4.0, 0.12, n, v - (14 if c < 16 * 16 else 0))
    for bar in range(CREST, 112):
        for half in (0, 8):                                     # re-barred: seven sixteenths and a rest = half a bar
            for h in E2_HITS:
                n, v = E2_PITCH[h]
                T["e2"].add(bar * 4.0 + (half + h) / 4.0, 0.12, n, v)

    # ---- drums: the storm's broken machine, assembling into the groove -----------------------------------------
    LOCK_K, LOCK_S, LOCK_GHOST = (0, 3, 10), (4, 12), (7, 14, 15)
    for bar in range(16, 112):
        sec, b0 = sec_of(bar), bar * 4.0
        p_lock = 0.0 if bar < 72 else 1.0 if bar >= CREST else (bar - 72) / 16.0
        locked = rng.random() < p_lock
        if locked:
            for s in LOCK_K:
                T["kick"].add(b0 + s / 4, 0.25, "k", 118 if s == 0 else 104)
            for s in LOCK_S:
                T["snare"].add(b0 + s / 4, 0.25, "s", 112)
                T["perc"].add(b0 + s / 4, 0.25, "cp", 70)
            for s in LOCK_GHOST:
                T["snare"].add(b0 + s / 4, 0.25, "rs", 48 + rng.randint(0, 14))
            for s in range(16):
                T["hats"].add(b0 + s / 4, 0.12, "oh" if s == 14 else "h", 86 if s % 4 == 2 else 58 + rng.randint(0, 10))
            continue
        heavy = sec == "eyewall"
        for s, on in enumerate(euclid(5 if not heavy else 7, 16, rng.randrange(16))):
            if on:
                T["kick"].add(b0 + s / 4, 0.25, "kh" if heavy and rng.random() < 0.3 else "k", 100 + rng.randint(0, 22))
        for s, on in enumerate(euclid(3, 16, rng.randrange(16))):
            if on:
                T["snare"].add(b0 + s / 4, 0.25, "s", 96 + rng.randint(0, 24))
        for s, on in enumerate(euclid(11 if heavy else 9, 16, rng.randrange(16))):
            if on:
                T["hats"].add(b0 + s / 4, 0.1, "h", 50 + rng.randint(0, 34))
        if heavy or bar % 4 == 3:                       # chip-noise rolls at phrase ends, everywhere in the eyewall
            n = rng.choice([4, 6, 8])
            st = 4.0 - n * 0.125
            for j in range(n):
                T["chipsn"].add(b0 + st + j * 0.125, 0.1, "G4", 60 + j * 7)
        if heavy:
            for s in range(16):
                if rng.random() < 0.35:
                    T["chiphat"].add(b0 + s / 4 + (0.125 if rng.random() < 0.3 else 0), 0.06, "C7", 44 + rng.randint(0, 30))
    # the outfall: the groove thins out across the seam (kick and hats last)
    for bar in range(112, 124):
        b0 = bar * 4.0
        if bar < 120:
            T["kick"].add(b0, 0.25, "k", 104 - (bar - 112) * 4)
            T["kick"].add(b0 + 2.5, 0.25, "k", 90 - (bar - 112) * 4)
        for s in range(0, 16, 2):
            T["hats"].add(b0 + s / 4, 0.1, "h", 60 - (bar - 112) * 3)

    # ---- the infall: sparse chip clicks under t2's handover --------------------------------------------------------
    for bar in range(4, 16):
        for s in range(16):
            if rng.random() < 0.06 + 0.012 * bar:
                T["chiphat"].add(bar * 4.0 + s / 4, 0.05, "C7", 30 + rng.randint(0, 24))

    # ---- the eye and the break: everything driven stops; the eye keeps E3's D (dust + sub), the break a riser ----
    stops = ("kick", "snare", "hats", "perc", "chipsn", "chiphat", "bass", "shard", "arp0", "arp1", "arp2", "e1", "e2")
    for k in stops:
        T[k].ev = [e for e in T[k].ev if not (EYE[0] * 4 <= e[0] < EYE[1] * 4 or BREAK[0] * 4 <= e[0] < BREAK[1] * 4)]
    T["dust"].add(EYE[0] * 4.0, (EYE[1] - EYE[0]) * 4.0 - 0.2, ",".join(mtok(m) for m in E3[0][0]), 84)
    T["sub"].add(EYE[0] * 4.0, (EYE[1] - EYE[0]) * 4.0 - 0.2, "m38", 66)
    T["kick"].add(EYE[1] * 4.0, 0.25, "kh", 124)                    # the wall comes back
    T["riser"].add(BREAK[0] * 4.0, (BREAK[1] - BREAK[0]) * 4.0, "C4", 96)
    T["dust"].add(BREAK[0] * 4.0, 7.8, ",".join(mtok(m) for m in E3[2][0]), 80)

    # ---- round 2: the crest's middle (w9, bars 96-108) - a crab canon, a ride, a fill and a held breath -----------
    if R2:
        r2 = random.Random(31)
        lock = lock_riff()                                                       # 8 beats
        crab = list(reversed(lock))
        for cyc, bar in enumerate(range(96, 108, 2)):
            at = bar * 4.0
            for n, ln in crab:
                T["glass"].add(at, ln * 0.95, mtok(midi(n) + 36 - (12 if cyc % 2 and midi(n) + 36 > 84 else 0)),
                               80 if ln >= 0.75 else 68)
                at += ln
        for bar in range(96, 108):
            for b in range(4):
                T["perc"].add(bar * 4.0 + b, 0.25, "rd", 66 if b % 2 else 78)
        b0 = 103 * 4.0
        for j in range(6):                                                       # the fill: 16ths, rising
            T["snare"].add(b0 + 2.0 + j * 0.25, 0.25, "s", 78 + 7 * j)
        gap = (b0 + 3.5, b0 + 4.0)                                               # an eighth of held breath
        for k in T:
            T[k].ev = [e for e in T[k].ev if not (gap[0] <= e[0] < gap[1])]
        T["perc"].add(104 * 4.0, 1.0, "c", 100 + r2.randint(0, 10))
    # ---- the voice: whispered in pieces through the storm, whole at the lock, then sung by the robot -------------
    late = json.load(open(os.path.join(HERE, "t3", "late.json")))["tracks"][0]["notes"]
    whisper, robot = [], []

    def put(dst, at, keep=None, scale=1.0):
        for i, n in enumerate(late):
            if keep is not None and i not in keep:
                continue
            d = {"at": round(at + n["at"] * scale, 4), "len": round(n["len"] * scale, 4), "ph": n["ph"],
                 "pitch": n["pitch"], "vel": n["vel"]}
            if n.get("expr_path"):
                d["expr_path"] = n["expr_path"]
            dst.append(d)

    for bar, keep in ((30, {0}), (36, {2}), (44, {4}), (50, {0, 1}), (58, {2, 3}), (63, {0, 4}), (76, {0, 1, 2}),
                      (82, {0, 1, 2, 3})):
        put(whisper, bar * 4.0 + 0.5, keep)
    put(whisper, (CREST - 2) * 4.0, None)                 # whole, two bars before the lock
    if R4:
        CLEAR.extend(n for n in whisper if 82 * 4.0 <= n["at"] < 84 * 4.0)
        whisper[:] = [n for n in whisper if not (82 * 4.0 <= n["at"] < 84 * 4.0)]
    for bar in (() if R10 else (100, 108) if R7 else (92, 100, 108)):
        put(robot, bar * 4.0, None)
    if R4:
        hits = {}
        for name, ln in (("E1", E1_LEN16), ("E2", E2_LEN), ("E3", E3_LEN16)):
            for c in cycle_starts(ln, 72 * 16, 86 * 16):
                if c % 16 == 0 and 72 * 16 <= c < 86 * 16:
                    hits.setdefault(c // 16, []).append(name)
        drums = ("kick", "snare", "hats", "perc", "chipsn", "chiphat")
        for bar, who in sorted(hits.items()):
            b0 = bar * 4.0
            if len(who) > 1:
                for k in drums:
                    T[k].ev = [e for e in T[k].ev if not (b0 - 0.5 <= e[0] < b0)]
            T["perc"].add(b0, 1.0, "c", 96 if len(who) == 1 else 116)
            T["kick"].add(b0, 0.25, "k", 112 if len(who) == 1 else 124)
            T["shard"].add(b0, 0.5, ",".join(mtok(m + 12) for m in E3[0][0]), 92 if len(who) == 1 else 112)
        steps = ["D5", "E5" if R6 else "Eb5", "F5", "G5", "A5", "Bb5", "C6"]  # (R4 count)
        for bar in range(72, 86):
            T["tick"].add(bar * 4.0, 0.9, mtok(midi(steps[(bar - 72) // 2])), 84 + 2 * (bar - 72) + (12 if bar in hits else 0))
    if R16:                                                 # w3: rain, and a held breath before bar 33
        T["rain"] = Track("rain")
        for c in (range(24 * 16, 36 * 16, 7) if R16_RAIN else ()):
            for pos, m in RAIN_CELL:
                g = c + pos
                if g < 36 * 16:
                    T["rain"].add(g / 4.0, 0.4, mtok(m), 58 + int(30 * (g - 24 * 16) / (12 * 16)) + (6 if pos == 0 else 0))
        # ... and it returns where the cycles lock (bars 73-88): like the congas, the seven takes one more sixteenth
        # and the rain falls on the bar - the front's texture comes back as part of the arithmetic, not a one-off
        for c in (range(72 * 16, 88 * 16, 8) if R16_RAIN else ()):
            for pos, m in RAIN_CELL:
                T["rain"].add((c + pos) / 4.0, 0.4, mtok(m), 66 + int(16 * (c - 72 * 16) / (16 * 16)) + (6 if pos == 0 else 0))
        lo, hi = (31 * 4.0 + 2.0, 32 * 4.0) if R16_BREATH else (0.0, 0.0)
        for k in ("kick", "snare", "hats", "perc", "chipsn", "chiphat", "bass", "floor", "sub"):
            if k in T:
                T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
    if R15:                                                 # the crest's answer: Dm | Bb | F | C
        lo, hi = OPEN_BARS[0] * 4.0, OPEN_BARS[1] * 4.0

        def dm_to_c(m):
            return m - 1 if m % 12 == 5 else m - 2           # F -> E; D, A, E -> C, G, D

        for k in ("shard", "arp0", "arp1", "arp2", "bass", "floor", "hold"):
            if k not in T:
                continue
            ev = []
            for e in T[k].ev:
                if lo <= e[0] < hi and isinstance(e[2], str) and e[2].startswith("m"):
                    pos = (e[0] - CREST * 4.0) % 8.0
                    f = (lambda m: m + 5) if 4.0 <= pos < 6.0 else dm_to_c if pos >= 6.0 else None
                    if f is not None:
                        e = (e[0], e[1], ",".join(mtok(f(int(float(h[1:])))) for h in e[2].split(",")), e[3], e[4])
                ev.append(e)
            T[k].ev = ev
    if R8:                                                  # w5: one groove in sevens + E1 stretched on the glass
        lo, hi = 48 * 4.0, 60 * 4.0
        # silence (velocity 1) rather than delete, so later events keep their per-event randomness; the new parts
        # live on their own tracks
        for k in ("kick", "snare", "hats"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
        for k in ("kick7", "snare7", "hats7", "glass7"):
            T[k] = Track(k)
        for c in range(48 * 16, 60 * 16, 7):
            b = c / 4.0
            T["kick7"].add(b, 0.25, "k", 114)
            T["hats7"].add(b + 0.5, 0.1, "h", 74)
            T["snare7"].add(b + 0.75, 0.25, "D4", 104)
            T["hats7"].add(b + 1.25, 0.1, "h", 62)
        at = lo
        for _ in range(3):
            for n, ln in E1:
                T["glass7"].add(at, ln * 2 * 0.95, mtok(midi(n) + 12), 86)
                at += ln * 2
    if R24 and "rain" in T:                                 # w9: the rain doubles the doo riff in eights (103-108)
        for c in range(102 * 16, 108 * 16, 8):
            for pos, m in RAIN_CELL:
                T["rain"].add((c + pos) / 4.0, 0.4, mtok(m + 12 if m < 72 else m), 70 + (6 if pos == 0 else 0))
    if R23:                                                 # w3: the arps climb an octave for bars 33-36
        for k in ("arp0", "arp1", "arp2"):
            T[k].ev = [(e[0], e[1], ",".join(mtok(int(float(p[1:])) + 12) if p.startswith("m") else p
                                              for p in e[2].split(",")), e[3], e[4])
                       if 32 * 4.0 <= e[0] < 36 * 4.0 and isinstance(e[2], str) else e for e in T[k].ev]
    if R21:                                                 # w11: the held chord's third lifts with t4 at bar 121
        T["dust"].ev = [(e[0], e[1], ",".join(p for p in e[2].split(",") if not (p.startswith("m") and
                                              int(float(p[1:])) % 12 == 5)) if R21_OPEN else
                         ",".join(mtok(int(float(p[1:])) + 1) if p.startswith("m") and
                                  int(float(p[1:])) % 12 == 5 else p for p in e[2].split(",")), e[3], e[4])
                        if e[0] >= 120 * 4.0 and isinstance(e[2], str) else e for e in T["dust"].ev]
        if "rain" in T and R21_DROPS:
            for bar in range(120, 128):
                for pos, m in RAIN_CELL:
                    T["rain"].add(bar * 4.0 + pos / 4.0, 0.4, mtok(78 if m == 77 else m),
                                  max(30, 74 - 6 * (bar - 120)) + (6 if pos == 0 else 0))
    if R18 and R8:                                          # w7: the old seven pulls once more (bars 81-84)
        lo, hi = PULL[0] * 4.0, PULL[1] * 4.0
        for k in ("kick", "snare", "hats"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
        for c in range(PULL[0] * 16, PULL[1] * 16, 7):
            b = c / 4.0
            up = int(14 * (c - PULL[0] * 16) / ((PULL[1] - PULL[0]) * 16))
            T["kick7"].add(b, 0.25, "k", 108 + up)
            T["hats7"].add(b + 0.5, 0.1, "h", 70 + up)
            T["snare7"].add(b + 0.75, 0.25, "D4", 98 + up)
            T["hats7"].add(b + 1.25, 0.1, "h", 58 + up)
    if R17:                                                 # the call at bar 97: the lead steps out; the fill
        for k in ("e1", "e1hi"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if CALL_BAR * 4.0 <= e[0] < CALL_BAR * 4.0 + 4.0 else e for e in T[k].ev]
        T["fill"] = Track("fill")
        for st, m in FILL:
            T["fill"].add(99 * 4.0 + st, 0.25, mtok(m), 72 + int(40 * (st - 2.5)))
    if R7:                                                  # the voice sings E1 alone in its bars; the lead answers
        for bar in SUNG_BARS:
            T["e1"].ev = [e for e in T["e1"].ev if not (bar * 4.0 <= e[0] < bar * 4.0 + 4.0)]
            T["e1hi"].ev = [e for e in T["e1hi"].ev if not (bar * 4.0 <= e[0] < bar * 4.0 + 4.0)]
    if R6:                                                  # the hook, plainly: E1 upright, two cycles, doubled
        for bar in (16, 40, 66):
            a0 = bar * 4.0
            T["e1"].ev = [e for e in T["e1"].ev if not (a0 <= e[0] < a0 + 10.0)]
            at = a0
            for _ in range(2):
                for n, ln in E1:
                    T["e1"].add(at, ln * 0.92, mtok(midi(n) + 12), 102)
                    T["e1hi"].add(at, ln * 0.92, mtok(midi(n) + 24), 74)
                    at += ln
    if R5:
        a, b, c = 108 * 4.0, 110 * 4.0, 112 * 4.0
        T["hats"].ev = [e for e in T["hats"].ev if not (a <= e[0] < c)]
        for bar, step, v in ((108, 0.5, 66), (109, 1.0, 56)):
            for k in range(int(4 / step)):
                T["hats"].add(bar * 4.0 + k * step, 0.1, "h", v - 3 * k)
        T["e1hi"].ev = [e for e in T["e1hi"].ev if not (109 * 4.0 <= e[0] < c)]
        for k in ("snare", "perc", "e2", "chipsn", "chiphat", "arp0", "arp1", "arp2", "shard", "floor", "sub"):
            T[k].ev = [e for e in T[k].ev if not (b <= e[0] < c)]
        T["dust"].add(a, 16.0 - 0.2, ",".join(mtok(m) for m in E3[0][0]), 72)
        retro = list(reversed(E1))
        at = a
        for n, ln in retro:
            T["glass"].add(at, ln * 2 * 0.95, mtok(midi(n) + 12), 84)
            at += ln * 2
        for n, ln in retro:
            T["glass"].add(at, ln * 4 * 0.95, mtok(midi(n)), 76)
            at += ln * 4
    if R30:                                                 # the storm breathes: four phrase-long moves in bars 21-60
        def mute(keys, lo, hi, pred=lambda e: True):
            for k in keys:
                if k in T:
                    T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if (lo <= e[0] < hi and pred(e)) else
                               (e[0], max(0.03, round(lo - e[0] - 0.05, 4)), e[2], e[3], e[4])
                               if (e[0] < lo < e[0] + e[1] and pred(e)) else e for e in T[k].ev]
        for b in (28, 44) + ((56, 76) if R31 else ()):      # the lift: arps and E1 chips up an octave, hats to eighths
            mute(("hats",), b * 4.0, (b + 4) * 4.0, lambda e: round(e[0] * 4) % 2 == 1)
            mute(("kick", "snare", "chipsn"), b * 4.0, (b + 4) * 4.0)          # the drums step out; bass and subs stay
            for k in ("arp0", "arp1", "arp2", "e1", "bass", "floor", "sub"):
                T[k].ev = [(e[0], e[1], ",".join(mtok(int(float(p[1:])) + 12) if p.startswith("m") else p
                                                  for p in e[2].split(",")), e[3], e[4])
                           if b * 4.0 <= e[0] < (b + 4) * 4.0 and isinstance(e[2], str) else e for e in T[k].ev]
    if R40:                                                 # w9: the storm parts for the answer (bars 101-104)
        for k in ("shard", "glass", "perc"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if 100 * 4.0 <= e[0] < 104 * 4.0 else
                       (e[0], max(0.03, round(100 * 4.0 - e[0] - 0.05, 4)), e[2], e[3], e[4]) if e[0] < 100 * 4.0 < e[0] + e[1]
                       else e for e in T[k].ev]
        T["_partc"] = Track("partc")
        T["_partc"].add(104 * 4.0, 2.0, "c", 116)
    if R38:                                                 # w2: the first gust (bars 23-24 breathe, a fill, a crash)
        T["kick"].ev = [(e[0], e[1], e[2], 1, e[4]) if 88.0 <= e[0] < 96.0 and not any(abs(e[0] - x) < 0.03 for x in (90.0, 92.0))
                        else e for e in T["kick"].ev]
        T["hats"].ev = [(e[0], e[1], e[2], 1, e[4]) if 88.0 <= e[0] < 96.0 else e for e in T["hats"].ev]
        T["_gust"], T["_gustc"] = Track("gust"), Track("gustc")
        for i, m in enumerate((62, 60, 57, 53) * 2):
            T["_gust"].add(94.0 + i * 0.25, 0.24, mtok(m), 78 + 5 * i)
        T["_gustc"].add(96.0, 2.0, "c", 112)
    if R34:                                                 # the eyewall assembles: the shards hold back for 49-52
        T["shard"].ev = [(e[0], e[1], e[2], 1, e[4]) if 48 * 4.0 <= e[0] < 52 * 4.0 else
                         (e[0], max(0.03, round(48 * 4.0 - e[0] - 0.05, 4)), e[2], e[3], e[4]) if e[0] < 48 * 4.0 < e[0] + e[1]
                         else e for e in T["shard"].ev]
    if R42:                                                 # the undertow breathes: roots held, two a bar
        for b0, b1 in ((16, 20), (36, 40), (90, 94)):
            ev = T["bass"].ev
            hold = {}
            for i, e in enumerate(ev):
                if b0 * 4.0 <= e[0] < b1 * 4.0 and e[3] > 1:
                    h = int(e[0] // 2)
                    j = hold.get(h)
                    if j is None or int(float(e[2][1:])) < int(float(ev[j][2][1:])):
                        hold[h] = i
            keep = {i: h for h, i in hold.items()}
            T["bass"].ev = [(e[0], round((keep[i] + 1) * 2.0 - e[0] - 0.1, 4), e[2], e[3], e[4]) if i in keep else
                            (e[0], e[1], e[2], 1, e[4]) if b0 * 4.0 <= e[0] < b1 * 4.0 else e for i, e in enumerate(ev)]
    if R41 and R32:                                         # the answer foretold: the round bass for bars 71-74
        T["_round2"] = Track("_round2")
        for e in T["bass"].ev:
            if 70 * 4.0 <= e[0] < 74 * 4.0 and e[3] > 1:
                T["_round2"].add(e[0], e[1] * 1.1, mtok(int(float(e[2][1:])) + 12), e[3])
        T["bass"].ev = [(e[0], e[1], e[2], 1, e[4]) if 70 * 4.0 <= e[0] < 74 * 4.0 else e for e in T["bass"].ev]
        T["shard"].ev = [(e[0], e[1], e[2], 1, e[4]) if 66 * 4.0 <= e[0] < 70 * 4.0 else
                         (e[0], max(0.03, round(66 * 4.0 - e[0] - 0.05, 4)), e[2], e[3], e[4]) if e[0] < 66 * 4.0 < e[0] + e[1]
                         else e for e in T["shard"].ev]
    if R32:                                                 # the answer on a round bass (bars 101-108)
        T["_round"] = Track("_round")
        for e in T["bass"].ev:
            if 100 * 4.0 <= e[0] < 108 * 4.0 and e[3] > 1:
                T["_round"].add(e[0], e[1] * 1.1, mtok(int(float(e[2][1:])) + 12), e[3])
        T["bass"].ev = [(e[0], e[1], e[2], 1, e[4]) if 100 * 4.0 <= e[0] < 108 * 4.0 else e for e in T["bass"].ev]
    if R28_MOVE and R27:                                    # the storm's E1 statements move from boc-lead to the dizi
        moved = [e for e in T["e1hi"].ev if e[0] < 88 * 4.0 and e[3] > 1]
        T["e1hi"].ev = [(e[0], e[1], e[2], 1, e[4]) if (e[0] < 88 * 4.0 and e[3] > 1) else e for e in T["e1hi"].ev]
        T["_dizi"] = Track("_dizi")
        for e in moved:
            if not (40 * 4.0 <= e[0] < 48 * 4.0):           # bar 41 is the dizi's own (v27)
                T["_dizi"].add(e[0], e[1], mtok(int(e[2][1:]) - 12), min(110, e[3] + 10))
    return T, whisper, robot


def main():
    T, whisper, robot = build()
    if R39:                                                 # the lock swings: off-sixteenths late from bar 89
        for trk in T.values():
            trk.ev = [(round(e[0] + 0.025, 4),) + tuple(e[1:]) if CREST * 4.0 <= e[0] < 104 * 4.0 and abs(e[0] % 0.5 - 0.25) < 1e-3
                      else e for e in trk.ev]
    tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": "64b", "bpm": SEAM_IN},
             {"at": "448b", "bpm": SEAM_OUT, "ramp": True}]
    if R47:                                                 # w6: in the eye, time slows (bars 62-66)
        def ramp_at(b):                                     # the old ramp's bpm at beat b (linear in beats),
            return round(SEAM_IN + (SEAM_OUT - SEAM_IN) * (b - 64) / (448 - 64), 6)   # exact so nothing before drifts
        tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": "64b", "bpm": SEAM_IN},
                 {"at": "244b", "bpm": ramp_at(244), "ramp": True}, {"at": "252b", "bpm": 80, "ramp": True},
                 {"at": "258b", "bpm": 80, "ramp": True}, {"at": "264b", "bpm": ramp_at(264), "ramp": True},
                 {"at": "448b", "bpm": SEAM_OUT, "ramp": True}]
    dyn = [["0b", -5.0], ["64b", -2.5], ["159.99b", -2.0], ["160b", -0.5], ["247.99b", 0.0], ["248b", -3.0],
           ["263.99b", -3.0], ["264b", 0.0], ["343.99b", -1.0], ["344b", -2.0], ["351.99b", -2.0], ["352b", 1.0],
           ["448b", 0.5], ["512b", -3.0]]
    stut = [["0b", 0.0], ["64b", 0.12], ["160b", 0.3], ["280b", 0.42], ["288b", 0.3], ["352b", 0.0], ["512b", 0.0]]
    grit = [["0b", 0.0], ["64b", 0.2], ["160b", 0.55], ["288b", 0.6], ["352b", 0.0], ["512b", 0.0]]
    fall = [["0b", 0.0], ["448b", 0.0], ["512b", -7.0]]
    close = [["0b", 0.0], ["448b", 0.0], ["512b", -2.0]]
    if R44:                                                 # w4: the storm behind a wall (bars 41-44)
        close = [["0b", 0.0], ["159.99b", 0.0], ["160b", -4.4], ["172b", -3.4], ["175.5b", -1.2], ["176b", 0.0],
                 ["448b", 0.0], ["512b", -2.0]]
    stop = [["0b", 0.0], ["223.99b", 0.0], ["224b", 1.0], ["225b", 1.0], ["225.01b", 0.0]]
    if R13:
        stut = [[p_, round(v * 0.6, 3)] for p_, v in stut]
        grit = [[p_, round(v * 0.4, 3)] for p_, v in grit]
    if R26:                                                 # one arc up to the crest; the crusher retires
        dyn = [["0b", -5.0], ["64b", -2.5], ["159.99b", -2.5], ["160b", -2.0], ["247.99b", -1.5], ["248b", -4.5],
               ["263.99b", -4.0], ["264b", -1.5], ["343.99b", -1.5], ["344b", -3.5], ["351.99b", -3.0], ["352b", 1.0],
               ["448b", 0.5], ["512b", -3.0]]
        grit = [[p_, 0.0] for p_, v in grit]

    def storm_fx(extra=()):
        return [{"type": "stutter", "slice": "1/16", "repeats": 3,
                 "chance": {"value": 0, "mod": [{"src": "auto.glitch", "amount": 1}]}},
                {"type": "crush", "bits": 6, "rate": "9kHz",
                 "mix": {"value": 0, "mod": [{"src": "auto.grit", "amount": 1}]}}] + list(extra)

    def lanes(**kw):
        d = {"glitch": {"points": stut}, "grit": {"points": grit}}
        d.update(kw)
        return d

    falling = [{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "auto.fall", "amount": 1}]}}]
    tracks = [
        {"name": "kick", "patch": "909", "gain": "-1dB", "fx": storm_fx(), "auto": lanes(), "score": T["kick"].score()},
        {"name": "snare", "patch": "909", "gain": "-4dB", "fx": storm_fx(), "auto": lanes(), "score": T["snare"].score()},
        {"name": "hats", "patch": "909", "gain": "-9dB", "pan": 0.15, "fx": storm_fx(), "auto": lanes(),
         "score": T["hats"].score()},
        {"name": "perc", "patch": "909", "gain": "-10dB", "pan": -0.1, "score": T["perc"].score()},
        {"name": "chipsn", "patch": "nes-noise-snare", "gain": "-8dB", "pan": -0.25, "score": T["chipsn"].score()},
        {"name": "chiphat", "patch": "nes-noise-hat", "gain": "-14dB", "pan": 0.35, "score": T["chiphat"].score()},
        {"name": "bass", "patch": "a3-grit", "gain": "-2.5dB", "fx": storm_fx(falling), "auto": lanes(fall={"points": fall}),
         "score": T["bass"].score()},
        {"name": "sub", "patch": "sub", "gain": "-12dB", "score": T["sub"].score()},
        {"name": "floor", "patch": "sub", "gain": "-10dB", "score": T["floor"].score()},
        {"name": "hold", "patch": "a3-shard", "gain": "-16dB", "pan": 0.1, "fx": ["lp cutoff=3500 q=0.6"],
         "sends": {"space": "-6dB"}, "score": T["hold"].score()},
        {"name": "riser", "patch": "fx-riser", "gain": "-10dB", "score": T["riser"].score()},
        {"name": "shard", "patch": "a3-shard", "gain": "-10dB", "pan": -0.1,
         "fx": storm_fx(falling) + ["delay time=3/16 mix=0.12 feedback=0.25"], "auto": lanes(fall={"points": fall}),
         "sends": {"space": "-12dB"}, "score": T["shard"].score()},
        *({"name": f"arp{k}", "patch": f"a3-arp{k}", "gain": "-17dB", "pan": (-0.3, 0.3, 0.0)[k], "fx": falling,
           "auto": {"fall": {"points": fall}}, "sends": {"space": "-10dB"}, "score": T[f"arp{k}"].score()}
          for k in range(3)),
        {"name": "e1", "patch": "nes-pulse-lead", "gain": "-13dB", "pan": 0.2,
         "fx": falling + ["delay time=1/8 mix=0.2 feedback=0.3"], "auto": {"fall": {"points": fall}},
         "sends": {"space": "-8dB"}, "score": T["e1"].score()},
        {"name": "e1hi", "patch": "nes-pulse-lead", "gain": "-19dB", "pan": -0.3,
         "fx": ["delay time=3/16 mix=0.25 feedback=0.3"], "sends": {"space": "-6dB"}, "score": T["e1hi"].score()},
        {"name": "e2", "patch": "chip-metal", "gain": "-15dB", "pan": -0.35, "score": T["e2"].score()},
        {"name": "dust", "patch": "a3-dust", "gain": "-15dB",
         "fx": [{"type": "cloud", "size": "120ms", "density": 14, "position": "400ms", "spray": "300ms",
                 "scatter": 0.4, "reverse": 0.3, "spread": 0.9, "mix": 0.6}],
         "sends": {"space": "-6dB"}, "score": T["dust"].score()},     # the residue t4 receives stays at pitch
        {"name": "whisper", "patch": "voice-speech", "gain": "-3dB", "pan": -0.1,
         "fx": ["pvoc mode=whisper seed=3", "delay time=3/8 mix=0.18 feedback=0.35"], "sends": {"space": "-6dB"},
         "notes": whisper},
        {"name": "robot", "patch": "voice-speech", "gain": "-4dB", "pan": 0.1,
         "fx": [{"type": "pvoc", "mode": "robot", "pitch": "C4",
                 "tune": {"value": 0, "mod": [{"src": "track.e1.key", "amount": 12}]}}],
         "sends": {"space": "-9dB"}, "notes": robot},
    ]
    patches = dict(PATCHES)
    if R3:
        patches["a3-ring"] = {"about": "chirper-two: the storm's lead - a saw ring-modulated by a sine at 1.414:1 (layer ringmod), "
                                       "an inharmonic, metallic edge whose ring mix rides an auto lane (`ring`: 0 = storm, "
                                       "1 = clean), over a quiet square an octave down",
                              "synth": {"layers": [{"name": "m", "wave": "sine", "ratio": 2.0 if R6 else 1.414, "audible": False},
                                                   {"wave": "saw", "ringmod": {"from": "m", "mix": {"value": 0.85, "mod": [
                                                       {"src": "auto.ring", "amount": -0.75}]}}},
                                                   {"wave": "square", "ratio": 0.5, "level": "-16dB"}],
                                        "filters": ["hp cutoff=200", "lp cutoff=4500 q=0.7"],
                                        "amp": {"a": "3ms", "d": "180ms", "s": 0.6, "r": "90ms"}}}
        ring = {"points": [["0b", 0.0], [f"{CREST * 4 - 0.01}b", 0.0], [f"{CREST * 4}b", 1.0], ["512b", 1.0]]}
        for tr in tracks:
            if tr["name"] in ("e1", "e1hi"):
                tr["patch"] = "a3-ring"
                tr["gain"] = {"e1": "-15dB", "e1hi": "-21dB"}[tr["name"]]
                tr.setdefault("auto", {})["ring"] = ring
        storm = Track("skin")
        lock = [e for e in T["snare"].ev if e[0] >= CREST * 4]
        storm.ev = [(e[0], e[1], "D4" if e[2] == "s" else "A4", e[3], e[4]) for e in T["snare"].ev if e[0] < CREST * 4]
        T["snare"].ev = lock
        for tr in tracks:
            if tr["name"] == "snare":
                tr["score"] = T["snare"].score()
        tracks.append({"name": "skin", "patch": "ks-drum", "gain": "-5dB", "pan": -0.05, "fx": storm_fx(), "auto": lanes(),
                       "score": storm.score()})
    if R2 or R4 or R5 or R8:
        patches["a3-glass"] = {"about": "chirper-two: the crest's glass - a sine phase-modulated at 3.5:1, the index pinged "
                                        "on each attack and settling to a faint shimmer; an octave partial; no low end",
                               "synth": {"layers": [{"name": "g", "ratio": 3.5, "audible": False},
                                                    {"wave": "sine", "pm": [{"from": "g", "depth": {"value": 0.06, "mod": [
                                                        {"src": "env.ping", "amount": 0.45}]}}]},
                                                    {"wave": "sine", "ratio": 2, "level": "-14dB"}],
                                         "env": {"ping": {"a": "0.5ms", "d": "250ms", "s": 0.05, "r": "100ms"}},
                                         "filters": ["hp cutoff=300", "lp cutoff=8000 q=0.6"],
                                         "amp": {"a": "2ms", "d": "600ms", "s": 0.45, "r": "400ms"}}}
    if R2 or R5 or R8:
        tracks.append({"name": "glass", "patch": "a3-glass", "gain": "-8dB", "pan": 0.25,
                       "fx": ["delay time=3/8 mix=0.2 feedback=0.35"], "sends": {"space": "-6dB"},
                       "score": T["glass"].score()})
    if R4:
        tracks.append({"name": "speak", "patch": "voice-speech", "gain": "3dB", "pan": 0.0,
                       "fx": ["delay time=3/8 mix=0.12 feedback=0.25"], "sends": {"space": "-10dB"}, "notes": CLEAR})
        tracks.append({"name": "tick", "patch": "a3-glass", "gain": "-10dB", "pan": -0.2,
                       "fx": ["delay time=1/4 mix=0.2 feedback=0.4"], "sends": {"space": "-6dB"},
                       "score": T["tick"].score()})
    if R9:
        import re
        for tr in tracks:
            if tr.get("patch") == "909":
                tr["patch"] = "tight-kit"
                tr["score"] = re.sub(r"(?<![a-z])cp/", "ss/", re.sub(r"(?<![a-z])kh/", "k/", tr["score"]))
        hand = Track("hand")
        cell = ((0, "lo", 82), (2, "o", 70), (3, "sl", 88), (5, "mu", 62))
        for lo, hi, period in ((24, 40, 7), (60, 72, 7), (72, 112, 8)):
            for c in range(lo * 16, hi * 16, period):
                for pos, head, vel in cell:
                    if c + pos < hi * 16:
                        hand.add((c + pos) / 4.0, 0.25, head, vel - (6 if lo == 72 and hi == 112 and c >= 88 * 16 else 0))
        # the tight kick is damped (no boom): a tuned 808 thump on D1 under every kick gives the storm back its floor,
        # on the home note
        ksub = Track("ksub")
        for k in ("kick", "kick7"):
            for e in (T[k].ev if k in T else []):
                if e[3] > 1 and not (R11 and e[0] >= 112 * 4.0):
                    ksub.add(e[0], 0.3, "D1", e[3])
        tracks.append({"name": "ksub", "patch": "808-short", "gain": "-4dB", "score": ksub.score()})
        tracks.append({"name": "hand", "patch": "congas", "gain": "-7dB", "pan": 0.3, "sends": {"space": "-12dB"},
                       "score": hand.score()})
    if R8:
        spec = {tr["name"]: tr for tr in tracks}
        for new, old in (("kick7", "kick"), ("hats7", "hats"), ("snare7", "skin"), ("glass7", "glass")):
            if old in spec:
                tracks.append(dict(spec[old], name=new, score=T[new].score()))
    if R7:
        src = json.load(open(os.path.join(HERE, "t3", "sung.json")))["tracks"][0]
        # voice-legato (join/inhale/wander/glide_smooth) needs a newer engine than the groove pin: until it is pinned,
        # the built-in singing voice with a mono glide carries the line (same notes, same phonemes)
        patches["a3-sung"] = dict(src["patch"], extends="voice play.glide=90ms play.mono=true")
        if R10:
            patches["a3-sung"] = dict(src["patch"], extends="voice-legato synth.layers.0.tract=0.86 "
                                                            "synth.layers.0.breath=0.35 synth.layers.0.ring=0.15")
        if R12:
            patches["a3-sung"] = dict(src["patch"], extends="voice-near")

        def place(srcn, bars, scale=1.0):
            out = []
            for bar in bars:
                for n in srcn:
                    d = {"at": round(bar * 4.0 - 0.25 + n["at"], 4), "len": n["len"], "ph": n["ph"],
                         "pitch": n["pitch"], "vel": round(n["vel"] * scale, 3)}
                    if n.get("expr_path"):
                        d["expr_path"] = n["expr_path"]
                    out.append(d)
            return out
        notes = place(src["notes"], SUNG_BARS)
        if R10:
            notes += place(json.load(open(os.path.join(HERE, "t3", "sung2.json")))["tracks"][0]["notes"], SUNG2_BARS)
            tracks[:] = [tr for tr in tracks if tr["name"] != "robot"]
            hum = place(json.load(open(os.path.join(HERE, "t3", "hum.json")))["tracks"][0]["notes"], HUM_BARS, 0.85)
            tracks.append({"name": "hum", "patch": "a3-sung", "gain": "-8dB", "pan": -0.2,
                           "fx": ["delay time=3/8 mix=0.3 feedback=0.4"], "sends": {"space": "-1dB"}, "notes": hum})
        # the lock's groove was buried under the undertow (presence, bars 89-96: bass -0.2 dB vs the mix, the 909 snare
        # -26, hats -34, percussion -42): the bass steps back and the kit comes up, so the reward is a groove you hear
        for tr in tracks:
            g = {"bass": -3.5, "snare": 9.0, "hats": 8.0, "perc": 8.0}.get(tr["name"])
            if g is not None:
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + g:g}dB"
        tracks.append({"name": "sung", "patch": "a3-sung", "gain": "0dB", "pan": 0.0,
                       "fx": ["delay time=3/8 mix=0.14 feedback=0.25"], "sends": {"space": "-7dB"}, "notes": notes})
        if R10:
            tracks[-1].update({"fx": ["delay time=3/8 mix=0.1 feedback=0.2"], "sends": {"space": "-11dB"}})
    if R18 and R4:                                          # bar 83: said, not placed (tts --rhythm --join)
        rsrc = json.load(open(os.path.join(HERE, "t3", "late_r.json")))["tracks"][0]
        patches["a3-speak"] = {"extends": rsrc["patch"]["extends"]}
        said = []
        for i, n in enumerate(rsrc["notes"][:4]):
            d = {"at": round(82 * 4.0 + 0.5 + n["at"], 4), "len": n["len"], "ph": n["ph"], "pitch": n["pitch"],
                 "vel": n["vel"]}
            if n.get("expr_path"):
                d["expr_path"] = n["expr_path"]
            said.append(d)
        for tr in tracks:
            if tr["name"] == "speak":
                tr.update(patch="a3-speak", notes=said)
    if R17:
        dsrc = json.load(open(os.path.join(HERE, "t3", "sung.json")))["tracks"][0]
        patches["a3-duet"] = dict(dsrc["patch"], extends="voice-near synth.layers.0.harmony=[2] "
                                                          "synth.layers.0.harmony_key=D:minor")
        duet = place(dsrc["notes"], (CALL_BAR,))
        duet += place(json.load(open(os.path.join(HERE, "t3", "sung2.json")))["tracks"][0]["notes"], (SUNG2_BARS[0],))
        for tr in tracks:
            if tr["name"] == "sung":
                a0, a1 = SUNG2_BARS[0] * 4.0 - 0.25, SUNG2_BARS[0] * 4.0 + 8.0
                tr["notes"] = [dict(n, vel=0.001) if a0 <= n["at"] < a1 else n for n in tr["notes"]]
                tracks.append(dict(tr, name="duet", patch="a3-duet", notes=duet))
                break
        spec = {tr["name"]: tr for tr in tracks}
        tracks.append(dict(spec["skin"], name="fill", score=T["fill"].score()))
    if R12:
        hi, lo = [], []
        for bar in range(96, 112, 2):
            opened = R15 and OPEN_BARS[0] <= bar < OPEN_BARS[1]
            for j, (h, l) in enumerate(((77, 69), (77, 70), (77, 69), (76, 67)) if opened else
                                       ((77, 69), (77, 70), (76, 67), (77, 69))):
                at = bar * 4.0 + j * 2.0
                ln = 1.75 if j == 3 else 2.0                      # touching inside the two bars, a breath at the end
                v = 0.62 + 0.04 * ((bar - 96) // 4)
                hi.append({"at": at, "len": ln, "ph": "AA1", "pitch": mtok(h), "vel": round(v, 3)})
                lo.append({"at": at, "len": ln, "ph": "AA1", "pitch": mtok(l), "vel": round(v - 0.04, 3)})
        for b0 in range(EYE[0], EYE[1], 2):                            # the eye: an open D-A 'oo', held
            hi.append({"at": b0 * 4.0, "len": 7.5, "ph": "UW1", "pitch": mtok(74), "vel": 0.45})
            lo.append({"at": b0 * 4.0, "len": 7.5, "ph": "UW1", "pitch": mtok(69), "vel": 0.42})
        # their breath was a 10-15 kHz hiss over the crest (+24..28 dB over t4's body): darkened to the vowel
        tracks.append({"name": "backhi", "patch": "voice-backing", "gain": "-11dB", "pan": 0.35, "fx": ["lp cutoff=4500"],
                       "sends": {"space": "-6dB"}, "notes": hi})
        tracks.append({"name": "backlo", "patch": "voice-backing", "gain": "-13dB", "pan": -0.35, "fx": ["lp cutoff=4500"],
                       "sends": {"space": "-6dB"}, "notes": lo})
    if R20 and R8:                                          # w5: the voice counts seven
        patches["a3-doo3"] = {"extends": "voice-near synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:minor"}
        doo, doo3 = [], []
        for c in range(48 * 16, 60 * 16, 7):
            for h in E2_HITS:
                g = c + h
                if g >= 60 * 16:
                    continue
                v = 0.5 + 0.2 * (g - 48 * 16) / (12 * 16) + (0.08 if h == 0 else 0.0)
                (doo3 if g >= 56 * 16 else doo).append({"at": round(g / 4.0, 4), "len": 0.22, "ph": "D UW1",
                                                        "pitch": mtok(DOO[h]), "vel": round(v, 3)})
        for name, patch, ns in (("doo", "voice-near", doo), ("doo3", "a3-doo3", doo3)):
            tracks.append({"name": name, "patch": patch, "gain": "-6dB", "pan": 0.2,
                           "fx": ["delay time=3/16 mix=0.12 feedback=0.2"], "sends": {"space": "-8dB"}, "notes": ns})
        if R24:                                             # w9: the voice counts eight (bars 103-108)
            doo8 = []
            for c in range(102 * 16, 108 * 16, 8):
                for h in E2_HITS:
                    v = 0.56 + 0.1 * (c - 102 * 16) / (6 * 16) + (0.08 if h == 0 else 0.0)
                    doo8.append({"at": round((c + h) / 4.0, 4), "len": 0.22, "ph": "D UW1", "pitch": mtok(DOO[h]),
                                 "vel": round(v, 3)})
            tracks.append({"name": "doo8", "patch": "a3-doo3", "gain": "-6dB", "pan": -0.15,
                           "fx": ["delay time=3/16 mix=0.12 feedback=0.2"], "sends": {"space": "-8dB"}, "notes": doo8})
    if R19 and R12:                                         # w8: the crest lands
        spec = {tr["name"]: tr for tr in tracks}
        hi8, lo8 = [], []
        for bar in range(CREST, 96, 2):
            for j, (h, l) in enumerate(((77, 69), (77, 70), (76, 67), (77, 69))):
                ln = 1.75 if j == 3 else 2.0
                v = 0.5 + 0.04 * ((bar - CREST) // 2)
                hi8.append({"at": bar * 4.0 + j * 2.0, "len": ln, "ph": "AA1", "pitch": mtok(h), "vel": round(v, 3)})
                lo8.append({"at": bar * 4.0 + j * 2.0, "len": ln, "ph": "AA1", "pitch": mtok(l), "vel": round(v - 0.04, 3)})
        tracks.append(dict(spec["backhi"], name="backhi8", notes=hi8))
        tracks.append(dict(spec["backlo"], name="backlo8", notes=lo8))
        roll, crash, boom = Track("roll"), Track("crash"), Track("boom")
        for s in range(8):
            roll.add((CREST - 1) * 4.0 + 2.0 + s / 4, 0.2, "s", 60 + 7 * s)
        crash.add(CREST * 4.0, 4.0, "c", 112)
        boom.add(CREST * 4.0, 6.0, mtok(26), 104)
        tracks.append(dict(spec["snare"], name="roll", score=roll.score()))
        tracks.append(dict(spec["perc"], name="crash", score=crash.score()))
        tracks.append({"name": "boom", "patch": "808", "gain": "-6dB", "score": boom.score()})
    if R11:
        patches["a3-residue"] = {"about": "chirper-two: the storm's residue for t4 - two triangles a few cents apart and "
                                          "an octave sine, slow in, mids only (600-1300 Hz), a little chorus",
                                 "synth": {"layers": [{"wave": "triangle", "detune": -5}, {"wave": "triangle", "detune": 5},
                                                      {"wave": "sine", "ratio": 2, "level": "-14dB"}],
                                           "filters": ["hp cutoff=320", "lp cutoff=3200 q=0.4"],
                                           "amp": {"a": "4s", "d": "1s", "s": 0.9, "r": "4s"}}}
        res = Track("residue")
        if R21:                                             # its third lets go at 121 and F# swells in (t4's bend)
            res.add(112 * 4.0, 16 * 4.0 - 0.2, ",".join(mtok(m) for m in (74, 81, 88)), 78)
            res.add(112 * 4.0, 8 * 4.0 - 0.2, mtok(77), 78)
            res.add(120 * 4.0, 8 * 4.0 - 0.2, mtok(78), 1 if R21_OPEN else 74)
        else:
            res.add(112 * 4.0, 16 * 4.0 - 0.2, ",".join(mtok(m) for m in (74, 77, 81, 88)), 78)
        tracks.append({"name": "residue", "patch": "a3-residue", "gain": "-16dB", "pan": 0.0, "fx": ["chorus mix=0.3"],
                       "sends": {"space": "-6dB"}, "score": res.score()})
        if R10 and R7:
            hsrc = json.load(open(os.path.join(HERE, "t3", "hum.json")))["tracks"][0]["notes"]
            last = []
            for n in hsrc:
                d = {"at": round(118 * 4.0 - 0.5 + n["at"] * 2, 4), "len": round(n["len"] * 2, 4), "ph": n["ph"],
                     "pitch": n["pitch"], "vel": round(n["vel"] * 0.8, 3)}
                if n.get("expr_path"):
                    d["expr_path"] = n["expr_path"]
                last.append(d)
            tracks.append({"name": "humlast", "patch": "a3-sung", "gain": "-9dB", "pan": 0.2,
                           "fx": ["delay time=3/8 mix=0.35 feedback=0.45"], "sends": {"space": "0dB"}, "notes": last})
    if R16 and R16_RAIN:
        tracks.append({"name": "rain", "patch": "ks-nylon", "gain": "-14dB", "pan": -0.3,
                       "fx": ["delay time=3/16 mix=0.25 feedback=0.35"], "sends": {"space": "-8dB"}, "score": T["rain"].score()})
    if R14:
        for tr in tracks:
            if tr["name"] == "e1hi" and R14_BOC:
                tr["patch"], tr["gain"] = "boc-lead", "-6dB"
                tr.get("auto", {}).pop("ring", None)
        air = Track("air")
        for bar in (range(16, 40) if R14_AIR else ()):
            if EYE[0] <= bar < EYE[1]:
                continue
            for s in range(16):
                g = bar * 16 + s
                acc = (g % 7) in (0, 2, 3, 5)
                air.add(g / 4.0, 0.1, "shk", 72 if acc else 44)
        if R14_AIR:
            tracks.append({"name": "air", "patch": "tight-kit", "gain": "-5dB", "pan": 0.25, "sends": {"space": "-12dB"},
                       "score": air.score()})
    if R13:
        for tr in tracks:
            if tr["name"] in ("bass", "floor"):
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + 2.0:g}dB"
    if R22:
        patches["a3-back"] = {"extends": "voice-backing play.glide_overshoot=0.05"}
        for tr in tracks:
            if tr["name"] == "floor" and R22_FLOOR:
                tr.update(patch="sub-saturated", gain=f"{float(tr['gain'].replace('dB', '')) - 17.0:g}dB")
            elif tr.get("patch") == "voice-backing":
                tr["patch"] = "a3-back"
        for k in ("a3-sung", "a3-duet"):
            if k in patches:
                patches[k] = dict(patches[k], extends=patches[k]["extends"] + " play.glide_overshoot=0.07")
    if R23 and "a3-sung" in patches:                        # w3: the hum sung (scoop/fall), the second a duet
        base = patches["a3-sung"]["extends"]
        patches["a3-hum"] = dict(patches["a3-sung"], extends=base + " play.scoop=1 play.fall=2")
        patches["a3-hum3"] = dict(patches["a3-sung"], extends=base + " synth.layers.0.harmony=[2] "
                                                                     "synth.layers.0.harmony_key=D:minor play.scoop=1 play.fall=2")
        for tr in tracks:
            if tr["name"] == "hum":
                cut = HUM_BARS[1] * 4.0 - 0.5
                second = [dict(n) for n in tr["notes"] if n["at"] >= cut]
                tr["notes"] = [dict(n, vel=0.001) if n["at"] >= cut else n for n in tr["notes"]]
                tr["patch"] = "a3-hum"
                tracks.append(dict(tr, name="hum3", patch="a3-hum3", notes=second))
                break
    if R27:                                                 # w4: the hook surfaces in the storm (dizi, bars 41-48)
        dz = Track("dizi")
        for k in range(6):
            at = 40 * 4.0 + 5.0 * k
            for j, (m, ln) in enumerate(((74, 0.5), (81, 0.75), (84, 0.25), (79, 1.0), (76, 1.0))):
                dz.add(at, ln * (0.95 if j < 4 else 1.4), mtok(m), 76 + 3 * k + (6 if j == 0 else 0))
                at += ln
        if R29:                                             # w7: the 5-beat cycle phased to meet bar 89's downbeat
            for k, at0 in enumerate([292.0 + 5.0 * i for i in range(7)] + [337.0, 352.0]):
                at = at0
                for j, (m, ln) in enumerate(((74, 0.5), (81, 0.75), (84, 0.25), (79, 1.0), (76, 1.0))):
                    v = 100 if at0 == 352.0 else 70 + 3 * k
                    dz.add(at, ln * (0.95 if j < 4 else (2.4 if at0 == 352.0 else 1.4)), mtok(m), v + (6 if j == 0 else 0))
                    at += ln
        if "_dizi" in T:                                    # R28: the storm's own E1 statements (bars 17, 41, 65)
            for e in T["_dizi"].ev:
                dz.add(e[0], e[1], e[2], e[3])
        for bar in (90, 94, 108):                           # ...and sings with her at the crest (8va)
            for off, m, ln in ((0.0, 74, 0.49), (0.5, 81, 0.74), (1.245, 84, 0.25), (1.5, 79, 0.99), (2.5, 76, 1.27)):
                dz.add(bar * 4.0 + off, ln, mtok(m), 84 if off == 0.0 else 80)
        if R37:                                             # the hook in the eye: E1 x4 augmented, plain and soft
            at = EYE[0] * 4.0 + 0.5
            for m, ln, v in ((74, 2.0, 74), (81, 3.0, 70), (84, 1.0, 66), (79, 4.0, 70), (76, 4.0, 72)):
                dz.add(at, ln * 0.95, mtok(m), v)
                at += ln
        tracks.append({"name": "dizi", "patch": "dizi", "gain": "-7dB", "pan": -0.2,
                       "fx": ["delay time=3/8 mix=0.15 feedback=0.3"], "sends": {"space": "-8dB"}, "score": dz.score()})
    if R32:                                                 # a3-round: the answer's bass
        patches["a3-round"] = {
            "about": "chirper-two: a round bass - sine + triangle with a quiet second harmonic through a 900 Hz low-pass "
                     "and a little drive; legato with a short glide. The crest's answer, after the storm's grain",
            "synth": {"layers": [{"wave": "sine"}, {"wave": "triangle", "level": "-8dB"},
                                 {"wave": "sine", "ratio": 2, "level": "-14dB"}],
                      "filters": ["lp cutoff=900"],
                      "amp": {"a": "4ms", "d": "500ms", "s": 0.75, "r": "140ms"},
                      "drive": 0.2},
            "play": {"mono": True, "legato": True, "glide": "40ms", "vel_sens": 0.4}}
        spec_b = next(tr for tr in tracks if tr["name"] == "bass")
        g_b = float(spec_b["gain"].replace("dB", "")) - 2.0
        tracks.append({"name": "bassr", "patch": "a3-round", "gain": f"{g_b:g}dB", "score": T["_round"].score()})
        if R41 and "_round2" in T:                          # ...foretold at bars 71-74
            tracks.append({"name": "bassr2", "patch": "a3-round", "gain": f"{g_b:g}dB", "score": T["_round2"].score()})
    if R40 and "_partc" in T:                               # the storm crashes back at bar 105
        tracks.append({"name": "partc", "patch": "tight-kit", "gain": "-4dB", "pan": 0.15, "score": T["_partc"].score()})
    if R51:                                                 # w5: the hook in sevens, on a steel pan (bars 49-60)
        stl = Track("steel")
        rhythm = [(0.0, 0.5), (0.5, 0.75), (1.25, 0.25), (1.5, 1.0), (2.5, 1.0)]
        fwd, back = (74, 81, 84, 79, 76), (76, 79, 84, 81, 74)
        for k in range(4):
            for j, line in enumerate((fwd, back)):
                at0 = 192.0 + 14.0 * k + 3.5 * j
                for (o, ln), m in zip(rhythm, line):
                    stl.add(at0 + o, ln - 0.05, mtok(m), 96 if o == 0 else 86)
        tracks.append({"name": "steel", "patch": "steel-pan", "gain": "0dB", "pan": 0.3,
                       "sends": {"space": "-10dB"}, "score": stl.score()})
    if R45:                                                 # w9: a melodica answers the singers with E1
        mel = Track("melod")
        e1 = [(0.0, 62, 0.5), (0.5, 69, 0.75), (1.25, 72, 0.25), (1.5, 67, 1.0), (2.5, 64, 1.0)]
        back = [(0.0, 64, 0.5), (0.5, 67, 0.75), (1.25, 72, 0.25), (1.5, 69, 1.0), (2.5, 62, 1.5)]
        for bar, ph, last in ((98, e1, 1.5), (102, e1, 1.5), (104, back, 1.5), (106, e1, 5.0)):
            for i, (o, p, ln) in enumerate(ph):
                mel.add(bar * 4.0 + o, last if i == len(ph) - 1 else ln - 0.05, mtok(p), 92 if i == 0 else 84)
        tracks.append({"name": "melod", "patch": "melodica", "gain": "7dB", "pan": -0.25,
                       "fx": ["delay time=3/8 mix=0.12 feedback=0.25"], "sends": {"space": "-8dB"}, "score": mel.score()})
    if R38 and "_gust" in T:                                # the first gust's fill and crash
        tracks.append({"name": "gust", "patch": "ks-drum", "gain": "-4dB", "pan": 0.1, "sends": {"space": "-10dB"},
                       "score": T["_gust"].score()})
        tracks.append({"name": "gustc", "patch": "tight-kit", "gain": "-4dB", "pan": -0.15, "score": T["_gustc"].score()})
    if R36:                                                 # E1 doubled on a farfisa (the Glass ensemble's organ)
        for tr in tracks:
            if tr.get("name") == "e1" and tr.get("patch") == "a3-ring":
                far = Track("e1f")                          # every other 8-bar phrase, bars 9-104
                far.ev = [e for e in T["e1"].ev if 8 <= int(e[0] // 4) < 104 and (int(e[0] // 4) // 8) % 2 == 1]
                tracks.append(dict(tr, name="e1f", patch="farfisa", gain="-6dB", pan=-0.2, score=far.score()))
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) - 1.0:g}dB"
                break
    if R35:                                                 # E2 as kotekan on two gamelan tracks
        for tr in tracks:
            if tr.get("name") == "e2" and tr.get("patch") == "chip-metal":
                chip, pol, san = Track("e2"), Track("e2g"), Track("e2s")
                for e in T["e2"].ev:                        # the storm's body only: the seams keep the chip
                    inside = 16 * 4.0 <= e[0] < 100 * 4.0
                    chip.ev.append(e)                       # the chip keeps its air (9-15 kHz) underneath
                    if inside:
                        (pol if e[2][0] in "DF" else san).ev.append((e[0], 0.15, e[2], e[3], e[4]))
                patches["a3-gangsa"] = {"extends": "gamelan", "fx": [],
                                        "about": "chirper-two: the library gangsa, dry (the hall left to the song's space)"}
                tr.update(score=chip.score())
                tracks.append({"name": "e2g", "patch": "a3-gangsa", "gain": "-7dB", "pan": -0.4, "score": pol.score(),
                               "sends": {"space": "-12dB"}})
                tracks.append({"name": "e2s", "patch": "a3-gangsa", "gain": "-5dB", "pan": 0.4, "score": san.score(),
                               "sends": {"space": "-12dB"}})
                break
    if R33:                                                 # the storm's own floor (staple `sub` -> a3-deep, +3 dB)
        patches["a3-deep"] = {
            "about": "chirper-two: t3's floor - a sine with a stronger second harmonic and a little drive through a 200 Hz "
                     "low-pass, mono with a short glide; heard in the chest and on small speakers",
            "synth": {"layers": [{"wave": "sine"}, {"wave": "sine", "ratio": 2, "level": "-12dB"}],
                      "amp": {"a": "4ms", "d": 0, "s": 1, "r": "180ms"},
                      "filters": ["lp cutoff=200 q=0.7"], "drive": 0.15},
            "play": {"mono": True, "glide": "15ms", "gate": 0.95},
            "gain": "-13dB"}
        for tr in tracks:
            if tr.get("name") in ("floor", "sub") and tr.get("patch") == "sub":
                tr["patch"] = "a3-deep"
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + 6.0:g}dB"
    if R28 and R28_TOG:                                     # every stacked voice sings together
        for k in ("a3-duet", "a3-hum3", "a3-doo3", "a3-back"):
            if k in patches:
                patches[k]["extends"] = patches[k]["extends"] + " synth.layers.0.together=true"
    if R25:                                                 # held notes bloom; the crest's phrases scoop and fall
        for k in list(patches):
            pt = patches[k]
            if k in ("a3-sung", "a3-duet"):
                pt["extends"] = pt["extends"] + " synth.lfo.vib.per_note=true play.scoop=1 play.fall=2"
            elif k.startswith("a3-hum"):
                pt["extends"] = pt["extends"] + " synth.lfo.vib.per_note=true"
            elif k == "a3-back":
                pt["extends"] = pt["extends"] + " synth.lfo.vib.per_note=true play.scoop=0.5 play.fall=1"
    if R50:                                                 # w10: everything comes round, as a round (bar 109)
        for tr in list(tracks):
            if tr.get("name") == "sung" and tr.get("notes"):
                line = [n for n in tr["notes"] if 431.9 <= n["at"] < 436.0]
                base = patches[tr["patch"]]
                for k, (off, pan, g, tract) in enumerate(((1.5, -0.35, -3.0, 1.1), (3.0, 0.35, -5.0, 0.92))):
                    pn = f"a3-round{k + 2}"
                    patches[pn] = dict(base, extends=base["extends"] + f" synth.layers.0.tract={tract}")
                    tracks.append(dict(tr, name=f"round{k + 2}", patch=pn, pan=pan, gain=f"{g:g}dB",
                                       notes=[dict(n, at=round(n["at"] + off, 4)) for n in line]))
                break
    if R48:                                                 # palette: the undertow gets a body (a sine an octave under)
        for tr in list(tracks):
            if tr.get("name") == "bass" and tr.get("score"):
                pos, toks = 0.0, []
                for tok in tr["score"].split():
                    m = re.match(r"^(.+?)/([0-9.e+-]+)b(.*)$", tok)
                    head, ln, rest = m.group(1), float(m.group(2)), m.group(3)
                    if head != "R":
                        head = ",".join(f"m{float(h[1:]) - 12:g}" if h.startswith("m") else h for h in head.split(","))
                        if pos >= 448 - 1e-6:
                            rest = re.sub(r"@\d+", "@1", rest, count=1)
                    toks.append(f"{head}/{m.group(2)}b{rest}")
                    pos += ln
                tracks.append({"name": "bsub", "patch": "sub-sine", "gain": "-2dB", "pan": 0.0, "score": " ".join(toks)})
                break
    if R46:                                                 # w8: the lock, heard (bars 89-96)
        lock = [["0b", 0.0], ["351.75b", 0.0], ["352b", 8.0], ["359.75b", 8.0], ["360b", 4.0], ["367.75b", 4.0],
                ["368b", 8.0], ["375.75b", 8.0], ["376b", 4.0], ["383.75b", 4.0], ["384b", 0.0]]
        amt = {"e1f": 1.0, "e1": 0.5, "e2g": 0.75, "e2s": 0.75, "e2": 0.5, "bass": -0.375}
        for tr in tracks:
            if tr.get("name") in amt:
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB", "mod": [
                    {"src": "auto.lock", "amount": amt[tr["name"]]}]}}]
                tr["auto"] = dict(tr.get("auto", {}), lock={"points": lock})
    if R43:                                                 # the hum is a hum: closed mouth at bar 25, open at 33
        for tr in list(tracks):
            if tr.get("name") == "hum" and tr.get("notes"):
                base = patches[tr["patch"]]
                patches["a3-humm"] = dict(base, extends=base["extends"] + " synth.layers.0.hum=1 synth.layers.0.hum_at=m")
                patches["a3-humn"] = dict(base, extends=base["extends"] + " synth.layers.0.hum=1 synth.layers.0.hum_at=n")
                g = float(tr["gain"].replace("dB", ""))
                lo = [dict(n, pitch=f"m{int(str(n['pitch'])[1:]) - 12}") for n in tr["notes"]]
                tr.update(patch="a3-humm", gain=f"{g + 4:g}dB")
                tracks.append(dict(tr, name="humlo", patch="a3-humn", gain=f"{g + 2:g}dB", pan=0.2, notes=lo))
                break
    if R52:                                                 # whole: the storm breathes (the low end pumps on every kick)
        depth = {"bass": "-5dB", "bsub": "-6dB", "floor": "-6dB"}
        for tr in tracks:
            if tr.get("name") in depth:
                tr["fx"] = list(tr.get("fx", [])) + [
                    {"type": "pump", "on": f"{k}.k", "depth": depth[tr["name"]], "release": "200ms", "curve": 0.6}
                    for k in ("kick", "kick7")]
    if R62:                                                 # palette: birds in the eye (bars 62-66), and after the storm
        rng = random.Random(6202)
        pent = (86, 89, 91, 93, 96, 98, 101)                # D6 F6 G6 A6 C7 D7 F7
        flocks = {"birdl": Track("birdl"), "birdr": Track("birdr")}
        def flock(lo, hi, gap):
            at = lo
            while at < hi:
                tr = flocks["birdl" if rng.random() < 0.5 else "birdr"]
                n, i, step = rng.randint(2, 6), rng.randrange(len(pent) - 1), rng.choice((0.08, 0.1, 0.125))
                for j in range(n):                          # a cluster: a trill between two neighbours or a run
                    pitch = pent[i + (j % 2)] if rng.random() < 0.6 else pent[min(len(pent) - 1, i + j // 2)]
                    tr.add(at + j * step, step * 0.9, mtok(pitch), rng.randint(70, 110))
                at += n * step + rng.uniform(*gap)
        flock(244.5, 253.5, (0.8, 2.2))
        for k, (dt, ln, m) in enumerate(((0, 0.25, 86), (0.25, 0.375, 93), (0.625, 0.125, 96), (0.75, 0.5, 91),
                                         (1.25, 0.6, 88))):    # E1, whistled at double speed (D6 A6 C7 G6 E6)
            flocks["birdl"].add(254.0 + dt, ln, mtok(m), 104 if k == 0 else 96)
        flock(256.5, 264.5, (0.8, 2.0))
        flock(404.5, 408.0, (1.0, 2.0))
        for nm, pan in (("birdl", -0.5), ("birdr", 0.5)):
            tracks.append({"name": nm, "patch": "birds", "gain": "9dB", "pan": pan, "score": flocks[nm].score()})
    if R81:                                                 # palette: chiphat's debris on pandeiro jingles and ganza
        ch = next(tr for tr in tracks if tr.get("name") == "chiphat")
        sm, pos = Track("debris"), 0.0
        for tok in ch["score"].split():
            m = re.match(r"^(.+?)/([0-9.e+-]+)b(?:@(\d+))?", tok)
            ln = float(m.group(2))
            if m.group(1) != "R":
                v = int(m.group(3) or 64)
                sm.add(pos, 0.25, "pd" if v >= 50 else "gz", v)
            pos += ln
        tracks.append({"name": "debris", "patch": "samba-kit", "gain": SAMBA_GAIN, "pan": ch.get("pan", 0.35),
                       "score": sm.score()})
        ch["mute"] = True
    if R80:                                                 # w5: the voices back up 5 dB; a fill into the eye (bar 60)
        for tr in tracks:
            if tr.get("name") in ("doo", "doop", "doo3"):
                tr["gain"] = f"{float(str(tr.get('gain', '0dB')).replace('dB', '')) + 5.0:g}dB"
        fl = Track("eyefill")
        for k in range(4):                                  # snare eighths, climbing
            fl.add(236.0 + 0.5 * k, 0.25, "s", 70 + 7 * k)
        for k, pc in enumerate(("t1", "t1", "t2", "t2", "t3", "t3", "ft", "ft")):   # toms in sixteenths, high to floor
            fl.add(238.0 + 0.25 * k, 0.25, pc, 96 + 3 * k)
        fl.add(240.0, 1.0, "c", 112)                        # one crash on the eye
        tracks.append({"name": "eyefill", "patch": "rock-kit", "gain": FILL_GAIN, "pan": 0.05, "score": fl.score()})
    if R79:                                                 # w6: the eye goes still (bars 61-64): engine out, E1 up, a choir
        still = {"points": [["0b", 0], ["239.75b", 0], ["240b", -60], ["255.75b", -60], ["256b", 0]]}
        for tr in tracks:
            if tr.get("name") in ("kick", "ksub", "sub", "bass", "bsub"):
                tr["fx"] = list(tr.get("fx") or []) + [{"type": "gain", "gain": {"value": "0dB",
                                                         "mod": [{"src": "auto.still", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), still=still)
            if tr.get("name") == "dizi":
                tr["fx"] = list(tr.get("fx") or []) + [{"type": "gain", "gain": {"value": "0dB",
                                                         "mod": [{"src": "auto.eyelift", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), eyelift={"points": [["0b", 0], ["239.5b", 0], ["240b", 6],
                                                                         ["256b", 6], ["257b", 0]]})
        eyen = []
        for at, chord in ((240.0, (62, 65, 69, 76)), (248.0, (58, 62, 65, 72))):   # Dm(add9), Bb(add9)
            for k, m in enumerate(chord):
                eyen.append({"at": at, "len": 7.8, "ph": "AA1", "pitch": f"m{m}", "vel": 0.6 if k else 0.66})
        tracks.append({"name": "eyechoir", "patch": "a3-choir", "gain": "0dB", "pan": -0.2,
                       "fx": ["lp cutoff=4500"], "sends": {"space": "-4dB"}, "notes": eyen})
    if R77:                                                 # palette (warp): the counting voice phases against itself, 49-56
        d0 = next(tr for tr in tracks if tr.get("name") == "doo")
        g = float(str(d0.get("gain", "0dB")).replace("dB", "")) + 2.0
        tracks.append(dict(d0, name="doop", gain=f"{g:g}dB", pan=-0.55, notes=[dict(n) for n in d0.get("notes", [])],
                           fx=list(d0.get("fx", [])),
                           warp=[{"over": "48bar", "to": 0}, {"over": "4bar", "to": -0.25, "curve": "linear"},
                                 {"over": "2bar", "to": -0.25}, {"over": "2bar", "to": 0, "curve": "smooth"}]))
        d0["gain"], d0["pan"] = f"{g:g}dB", 0.55
    if R76:                                                 # w4: E1 x4 slower on a Risset arpeggio (bars 37-44)
        patches["a3-risset"] = {"extends": "risset-arpeggio synth.layers.0.cents=-12.56 synth.layers.1.cents=-6.28 "
                                           "synth.layers.3.cents=6.28 synth.layers.4.cents=12.56 synth.amp.a=0.8s"}
        rs = Track("risset")
        e1x4 = ((0.0, 2.0, 62), (2.0, 3.0, 69), (5.0, 1.0, 72), (6.0, 4.0, 67), (10.0, 6.0, 64))  # D4 A4 C5 G4 E4
        for k, at0 in enumerate((144.0, 160.0)):
            for off, ln, m in e1x4:
                rs.add(at0 + off, ln - 0.1, mtok(m + 12 * k), 92 + 8 * k)
        tracks.append({"name": "risset", "patch": "a3-risset", "gain": RISSET_GAIN, "pan": -0.1,
                       "sends": {"space": "-8dB"}, "score": rs.score()})
    if R75:                                                 # palette: the hats from a room (tight-kit -> rock-kit hats)
        for tr in tracks:
            if tr.get("name") in ("hats", "hats7", "hatshalf") and tr.get("patch") == "tight-kit":
                tr["patch"] = "rock-kit"
                g = float(str(tr.get("gain", "0dB")).replace("dB", ""))
                tr["gain"] = f"{g + float(ROOMHAT_GAIN.replace('dB', '')):g}dB"
    if R72:                                                 # w7: E1 on the bar against the dizi's E1 every five beats
        vb = Track("phasev")
        e1v = ((0.0, 0.5, 62), (0.5, 0.75, 69), (1.25, 0.25, 72), (1.5, 1.0, 67), (2.5, 1.5, 64))   # D4 A4 C5 G4 E4
        for k, at0 in enumerate(range(288, 336, 4)):
            for off, ln, m in e1v:
                vb.add(at0 + off, ln - 0.05, mtok(m), (96 if off == 0.0 else 84) + (k // 4) * 3)
        tracks.append({"name": "phasev", "patch": "vibes", "gain": PHASE_GAIN, "pan": -0.35,
                       "sends": {"space": "-9dB"}, "score": vb.score()})
    if R71:                                                 # w9: half time under the melodica (103-104), a held breath, a slam
        half = {"kick": [(408.0, "k", 122), (412.0, "k", 116)],
                "ksub": [(408.0, "D1", 118), (412.0, "D1", 112)],
                "snare": [(410.0, "s", 120), (414.0, "s", 124), (414.5, "rs", 70)],
                "hats": [(408.0 + i, "h", 84 if i % 2 == 0 else 72) for i in range(7)]}
        for src, hits in half.items():
            tr0 = next(tr for tr in tracks if tr.get("name") == src)
            hx = Track(src + "half")
            for at, tok, v in hits:
                hx.add(at, 0.25 if src != "ksub" else 0.9, tok, v)
            tracks.append(dict({k: v for k, v in tr0.items() if k not in ("score", "notes")}, name=src + "half",
                               fx=list(tr0.get("fx", [])), auto=dict(tr0.get("auto", {})), score=hx.score()))
        for tr in tracks:
            nm = tr.get("name")
            if nm in ("kick", "ksub", "snare", "hats", "bassr"):
                lo = 415.0 if nm == "bassr" else 407.95            # the bass rides the half time, then stops too
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.halve", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), halve={"points": [["0b", 0], [f"{lo}b", 0], [f"{lo + 0.05}b", -60],
                                                                         ["415.95b", -60], ["416b", 0], ["513b", 0]]})
    if R70:                                                 # w5: the bass sings E1 into the eye (bars 57-60)
        hookb, hooks = Track("bassh"), Track("bsubh")
        e1 = ((0.0, 0.5, 38), (0.5, 0.75, 45), (1.25, 0.25, 48), (1.5, 1.0, 43), (2.5, 1.5, 40))   # D2 A2 C3 G2 E2
        for k, at0 in enumerate((224.0, 228.0, 232.0)):
            for off, ln, m in e1:
                v = 104 + 4 * k + (6 if off == 0.0 else 0)
                hookb.add(at0 + off, ln - 0.06, mtok(m), v)
                hooks.add(at0 + off, ln - 0.06, mtok(m - 12), v)
        for i, m in enumerate((38, 40, 41, 43, 45, 48, 50, 53)):            # D E F G A C D F, up into the eye
            hookb.add(236.0 + 0.5 * i, 0.44, mtok(m), 100 + 2 * i)
            hooks.add(236.0 + 0.5 * i, 0.44, mtok(m - 12), 100 + 2 * i)
        for src, new, sc in (("bass", "bassh", hookb), ("bsub", "bsubh", hooks)):
            tr0 = next(tr for tr in tracks if tr.get("name") == src)
            tracks.append(dict({k: v for k, v in tr0.items() if k not in ("score", "notes")},
                               name=new, fx=list(tr0.get("fx", [])), auto=dict(tr0.get("auto", {})), score=sc.score()))
            tr0["fx"] = list(tr0.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                    "mod": [{"src": "auto.yield", "amount": 1}]}}]
            tr0["auto"] = dict(tr0.get("auto", {}), **{"yield": {"points": [["0b", 0], ["223.9b", 0], ["224b", -60],
                                                                             ["239.9b", -60], ["240b", 0], ["513b", 0]]}})
    if R69:                                                 # w6: the birds scatter as the second storm hits (bars 67-68)
        rng2 = random.Random(6909)
        pent2 = (86, 89, 91, 93, 96, 98, 101, 103, 105)     # D6 .. A7, the eye's pentatonic and higher
        fl, fr = Track("fleel"), Track("fleer")
        at = 264.0
        while at < 267.5:
            tr_ = fl if rng2.random() < 0.5 else fr
            n = rng2.randint(3, 6)
            base = min(len(pent2) - n, int((at - 264.0) / 3.5 * (len(pent2) - 3)) + rng2.randrange(2))
            step = rng2.choice((0.06, 0.08))
            for j in range(n):                              # a rising run, higher as the burst goes on
                tr_.add(at + j * step, step * 0.9, mtok(pent2[base + j]), rng2.randint(96, 120))
            at += n * step + rng2.uniform(0.1, 0.35)
        for nm, pan, tr_ in (("fleel", -0.85, fl), ("fleer", 0.85, fr)):
            tracks.append({"name": nm, "patch": "birds", "gain": "9dB", "pan": pan, "score": tr_.score()})
    if R67:                                                 # palette: a rise that never arrives (bars 85-88), toms at the lock
        sh, tom = Track("shepard"), Track("locktom")
        sh.add(336.0, 15.98, "m62", 100)
        tom.add(351.5, 0.5, mtok(33), 104)                  # A1, the pickup
        tom.add(352.0, 4.0, mtok(38), 124)                  # D2 at the lock
        for tr in tracks:
            if tr.get("name") == "riser":
                tr["mute"] = True
        tracks.append({"name": "shepard", "patch": "fx-riser-endless", "gain": "-4dB", "pan": 0.0, "score": sh.score(),
                       "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.cut", "amount": 1}]}}],
                       "auto": {"cut": {"points": [["0b", 0], ["351.95b", 0], ["352b", -60], ["513b", -60]]}}})
        tracks.append({"name": "locktom", "patch": "modal-tom", "gain": "-2dB", "pan": 0.0, "sends": {"space": "-8dB"},
                       "score": tom.score()})
    if R66:                                                 # w4: the words before the song (bars 45-48)
        wh0 = next(tr for tr in tracks if tr.get("name") == "whisper")
        sylls = (("N AH1", 0.0, 0.45, 49.0), ("TH IH0 NG", 0.5, 0.7, 48.5), ("HH IY1 R", 1.25, 0.24, 48.0),
                 ("IH1 Z", 1.5, 0.9, 47.0), ("L EY1 T", 2.5, 1.3, 45.0))           # on E1's rhythm
        notes = []
        for k, at0 in enumerate((176.75, 184.75)):          # a breath behind the dizi's E1 at 176 / 184
            for ph, dt, ln, m in sylls:
                notes.append({"at": at0 + dt, "len": ln, "ph": ph, "pitch": f"m{m:g}", "vel": 0.8 + 0.04 * k,
                              "expr_path": {"f0": [0.0, 8.0, 16.0, 20.0, 16.0, 6.0, -8.0, -20.0]}})
        tracks.append(dict({k: v for k, v in wh0.items() if k not in ("notes", "auto")}, name="whisper2",
                           gain="2dB", pan=0.15, notes=notes))
    if R61:                                                 # w8: the seven locks into eight (bars 89-96)
        lockb = Track("lockb")
        chords = ("m57,m62,m65", "m58,m62,m65", "m60,m64,m67", "m57,m62,m65")   # Dm, Bb, C, Dm (2 beats each)
        sungs = ((360.0, 364.0), (376.0, 380.0))                              # the voice: the brass rests
        for k in range(16):
            at = 352.0 + 2.0 * k
            if any(a_ <= at < b_ for a_, b_ in sungs):
                continue
            for s16, vel in ((0, 112), (2, 92), (3, 98), (5, 104)):
                lockb.add(at + 0.25 * s16, 0.22, chords[k % 4], vel)
        tracks.append({"name": "lockb", "patch": "brass-stab", "gain": "-1dB", "pan": -0.2,
                       "sends": {"space": "-8dB"}, "score": lockb.score()})
    if R58:                                                 # w7: the hands take over (bars 77-80)
        lo, hi = 304.0, 320.0
        for tr in tracks:
            if tr.get("name") in ("hats", "perc", "hand"):
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.hands", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), hands={"points": [["0b", 0], [f"{lo - 0.03:g}b", 0],
                                                                          [f"{lo:g}b", -60], [f"{hi - 0.03:g}b", -60],
                                                                          [f"{hi:g}b", 0]]})
        hands, piece = Track("hands"), {0: ("sl", 112), 2: ("o", 92), 3: ("o", 84), 5: ("lo", 100)}
        s16 = 0
        while lo + 0.25 * s16 < hi - 4.0:
            k = s16 % 7
            if k in piece:
                hands.add(lo + 0.25 * s16, 0.24, piece[k][0], piece[k][1])
            s16 += 1
        for i in range(16):                                 # the last bar: a roll swelling into 81
            hands.add(hi - 4.0 + 0.25 * i, 0.24, ("o", "lo", "sl", "o")[i % 4], 64 + 3 * i)
        hand = next(tr for tr in tracks if tr.get("name") == "hand")
        tracks.append(dict(hand, name="hands", gain="-1dB", pan=-0.1,
                           fx=[f for f in hand.get("fx", []) if not (isinstance(f, dict) and f.get("type") == "gain")],
                           auto={k: v for k, v in hand.get("auto", {}).items() if k != "hands"},
                           score=hands.score()))
    if R57:                                                 # w2: the hook slips (bars 17-24, the dizi)
        for tr in list(tracks):
            if tr.get("name") == "dizi":
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.lift", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), lift={"points": [["0b", 0], ["67.9b", 0], ["68b", 6],
                                                                         ["71.9b", 6], ["72b", 0]]})
                spec = tr
        for tr in list(tracks):
            if tr.get("name") == "e1" and tr.get("score"):
                pos, frag = 0.0, Track("dizi2")
                for tok in tr["score"].split():
                    m = re.match(r"^(.+?)/([0-9.e+-]+)b(?:@(\d+))?", tok)
                    if m.group(1) != "R" and int(m.group(3) or 0) > 1 and 72.0 <= pos < 96.0:
                        frag.add(pos, float(m.group(2)), m.group(1), min(110, int(m.group(3)) + 8))
                    pos += float(m.group(2))
                tracks.append(dict(spec, name="dizi2", gain=f"{float(spec['gain'].replace('dB', '')) + 7.0:g}dB",
                                   pan=0.2, fx=[f for f in spec.get("fx", []) if not (isinstance(f, dict) and f.get("type") == "gain")],
                                   auto={k: v for k, v in spec.get("auto", {}).items() if k != "lift"},
                                   score=frag.score()))
    if R56:                                                 # palette: the swarm that locks (beats 264-384)
        def chords(name, lo, hi):
            out = []
            for tr in tracks:
                if tr.get("name") == name and tr.get("score"):
                    pos = 0.0
                    for tok in tr["score"].split():
                        m = re.match(r"^(.+?)/([0-9.e+-]+)b(?:@(\d+))?", tok)
                        if m.group(1) != "R" and int(m.group(3) or 0) > 1 and lo <= pos < hi:
                            if not out or out[-1][1] != m.group(1):
                                out.append((pos, m.group(1)))
                        pos += float(m.group(2))
            return out
        seq = chords("shard", 264.0, 352.0) + chords("hold", 352.0, 384.0)
        sw = Track("swarm")
        for i, (at, ch) in enumerate(seq):
            end = seq[i + 1][0] if i + 1 < len(seq) else 384.0
            up = 12 if at < 352.0 else 0
            ms = [int(x[1:]) + up for x in ch.split(",") if x.startswith("m")]
            if max(ms) > 84:                                # no shrill E6-F6 at the top
                ms = [m - 12 for m in ms]
            sw.add(at, max(0.1, end - at - 0.05), ",".join(mtok(m) for m in ms), 72)
        patches["a3-swarm"] = {"about": "chirper-two: the storm's chords on a Kuramoto swarm whose coupling the song turns "
                                        "up - a loose out-of-tune chorus that locks into one tone at t3's lock",
                               "synth": {"layers": [{"type": "kuramoto", "kuramoto": {
                                             "count": 10, "spread": 55, "wave": "triangle",
                                             "coupling": {"value": 0, "mod": [{"src": "auto.sync", "amount": 1}]}}}],
                                         "filters": ["lp cutoff=3000 q=0.5"],
                                         "amp": {"a": "250ms", "d": "1s", "s": 0.9, "r": "900ms"}},
                               "fx": ["chorus mix=0.2", "reverb kind=hall decay=3s mix=0.3"]}
        tracks.append({"name": "swarm", "patch": "a3-swarm", "gain": "-7dB", "pan": 0.0, "sends": {"space": "-8dB"},
                       "score": sw.score(),
                       "auto": {"sync": {"points": [["0b", 0.15], ["264b", 0.15], ["320b", 0.8], ["344b", 1.4],
                                                    ["351.9b", 1.8], ["352b", 4.0], ["384b", 4.0]]}}})
    if R55:                                                 # w9: the choir answers the duet (bars 97-108)
        patches["a3-choir"] = {"extends": "voice-backing play.glide_overshoot=0.05 synth.lfo.vib.per_note=true "
                                          "play.scoop=0.5 play.fall=1 synth.layers.0.singers=6 "
                                          "synth.layers.0.spread=0.8 synth.layers.0.vib_spread=1"}
        lane = [["0b", -4], ["388b", -4], ["390b", 3], ["398b", 3], ["399.9b", -4], ["404b", -4], ["406b", 3],
                ["428b", 3], ["432b", -4]]
        for tr in list(tracks):
            if tr.get("name") in ("backlo", "backhi") and tr.get("notes"):
                mine = [dict(n) for n in tr["notes"] if 384.0 <= n["at"] < 432.0 and n.get("vel", 1) > 0.02]
                tr["notes"] = [dict(n, vel=0.01) if 384.0 <= n["at"] < 432.0 else n for n in tr["notes"]]
                tracks.append(dict(tr, name=tr["name"].replace("back", "choir"), patch="a3-choir",
                                   gain=f"{float(tr['gain'].replace('dB', '')) + (8.0 if 'hi' in tr['name'] else 5.0):g}dB", notes=mine,
                                   fx=list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                       "mod": [{"src": "auto.answer", "amount": 1}]}}],
                                   auto=dict(tr.get("auto", {}), answer={"points": lane})))
            if tr.get("name") == "duet" and tr.get("patch") == "a3-duet":
                patches["a3-duetv"] = dict(patches["a3-duet"],
                                           extends=patches["a3-duet"]["extends"] + " synth.layers.0.vib_spread=1")
                tr["patch"] = "a3-duetv"
    if R54:                                                 # w1: the storm on the horizon (bars 1-16)
        tracks.append({"name": "wind", "patch": "wind", "gain": "-3dB", "pan": 0.15, "sends": {"space": "-6dB"},
                       "notes": [{"at": 0.0, "len": 66.0, "pitch": "m62", "vel": 0.8}],
                       "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.rise", "amount": 1}]}}],
                       "auto": {"rise": {"points": [["0b", -14], ["13b", -4], ["22b", -4], ["26b", -24],     # gusts
                                                    ["37b", -24], ["41b", -2], ["50b", -2], ["53b", -20],      # between
                                                    ["60b", -14], ["64b", -6], ["72b", -40]]}}})             # rolls
        thu = Track("thunder")
        for k, (end, n16, v0, v1) in enumerate(((32.0, 12, 42, 70), (64.0, 20, 54, 100))):
            for i in range(n16):
                thu.add(end - 0.25 * (n16 - i), 0.24, mtok(38), int(v0 + (v1 - v0) * i / max(1, n16 - 1)))
            thu.add(end, 1.5, mtok(38), min(112, v1 + 10))
        tracks.append({"name": "thunder", "patch": "timpani", "gain": "-12dB", "pan": -0.25,
                       "sends": {"space": "-2dB"}, "score": thu.score()})
    if R53:                                                 # whole: the storm lets go, on a breath
        for tr in tracks:
            if tr.get("name") in ("bass", "bsub", "floor"):
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.ease", "amount": 1}]}}]
                tr.setdefault("auto", {})["ease"] = {"points": [["0b", 0], ["416b", 0], ["448b", -3], ["513b", -3]]}
        patches["a3-humd"] = dict(patches["a3-humm"],
                                  extends=patches["a3-humm"]["extends"] + " synth.layers.0.hum_even=1")
        tracks.append({"name": "humd", "patch": "a3-humd", "gain": "-13dB", "pan": 0.0, "sends": {"space": "-3dB"},
                       "notes": [{"at": 480.0, "len": 30.0, "ph": "UW1", "pitch": "m62", "vel": 0.62}],
                       "fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fade", "amount": 1}]}}],
                       "auto": {"fade": {"points": [["0b", -40], ["479.9b", -40], ["484b", 0], ["500b", 0],
                                                    ["510b", -40], ["513b", -40]]}}})
    master = {"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=100 gain=3dB q=1.0",
                                              "peak cutoff=320 gain=-2dB q=0.8",
                                              "highshelf cutoff=8000 gain=2dB"]},
                     "glue threshold=-18dB ratio=2 attack=10ms release=150ms makeup=1dB",
                     {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                     {"type": "filter", "kind": "lp", "q": 0.707,
                      "cutoff": {"value": 20000, "mod": [{"src": "auto.close", "amount": 1}]}},
                     {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]},
                      "time": "1b", "curve": 1.6},
                     {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
              "auto": {"dyn": {"points": dyn}, "close": {"points": close}, "stop": {"points": stop}}}
    if R49:                                                 # whole: the storm loses its honk (master scoop at 900 Hz)
        master["fx"][0]["bands"] = list(master["fx"][0]["bands"]) + ["peak cutoff=900 gain=-3dB q=0.7",
                                                                     "peak cutoff=55 gain=3dB q=0.9"]
    if R59:                                                 # whole: the storm's space (width lane), voices as sections
        field = [["0b", 1.0], ["60b", 1.0], ["64b", 1.45], ["240b", 1.45], ["248b", 0.55], ["262b", 0.55],
                 ["268b", 1.4], ["348b", 1.4], ["352b", 1.8], ["380b", 1.5], ["432b", 1.3], ["448b", 1.0], ["513b", 1.0]]
        master["fx"].insert(len(master["fx"]) - 1, {"type": "width", "mono_below": "off",
                                                    "width": {"value": 0, "mod": [{"src": "auto.field", "amount": 1}]}})
        master["auto"] = dict(master["auto"], field={"points": field})
        for pn in ("a3-back", "a3-doo3", "a3-hum3", "a3-choir", "a3-duetv"):
            if pn in patches:
                e = patches[pn]["extends"]
                add = ("" if "vib_spread" in e else " synth.layers.0.vib_spread=1") + " synth.layers.0.vowel_spread=1"
                patches[pn] = dict(patches[pn], extends=e + add)
    if R63:                                                 # whole: the ground arrives (floor/bsub swell 17-25), breaths
        for tr in tracks:
            if tr.get("name") in ("floor", "bsub"):
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.ground", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), ground={"points": [["0b", -12.0], ["64b", -12.0], ["96b", 0.0],
                                                                          ["513b", 0.0]] if not R65 else
                                                          [["0b", -12.0], ["64b", -12.0], ["96b", 0.0], ["400b", 0.0],
                                                           ["432b", -6.0], ["448b", -9.0], ["513b", -9.0]]})
            if tr.get("name") == "ksub":                    # the 808's sub under the kick: half as far down (-6)
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.ground", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), ground={"points": [["0b", -6.0], ["64b", -6.0], ["96b", 0.0],
                                                                          ["513b", 0.0]] if not R65 else
                                                          [["0b", -6.0], ["64b", -6.0], ["96b", 0.0], ["400b", 0.0],
                                                           ["432b", -4.0], ["448b", -6.0], ["513b", -6.0]]})
        for pn in ("a3-sung", "a3-duetv", "a3-round2", "a3-round3"):
            if pn in patches:
                patches[pn] = dict(patches[pn], extends=patches[pn]["extends"] + " synth.layers.0.inhale=0.9")
        for pn in ("a3-choir", "a3-back"):
            if pn in patches:
                patches[pn] = dict(patches[pn], extends=patches[pn]["extends"] +
                                   " synth.layers.0.depth_spread=1 synth.layers.0.cons_spread=1")
    if R66:                                                 # w4 (after v57's lift exists): the dizi's E1 plain, bars 45-48
        dz = next(tr for tr in tracks if tr.get("name") == "dizi")
        dz["auto"] = dict(dz.get("auto", {}), lift={"points": dz["auto"]["lift"]["points"] +
                                                    [["175.5b", 0], ["176b", 6], ["187.5b", 6], ["188b", 0]]})
    if R69:                                                 # w6 (after v57's lift exists): the dizi's E1 back with the storm
        dz = next(tr for tr in tracks if tr.get("name") == "dizi")
        dz["auto"] = dict(dz.get("auto", {}), lift={"points": dz["auto"]["lift"]["points"] +
                                                    [["263.9b", 0], ["264b", 8], ["271.9b", 8], ["272b", 0]]})
    if R72:                                                 # w7 (after R69 extends lift): the dizi's five-beat E1 up 10 dB
        dz = next(tr for tr in tracks if tr.get("name") == "dizi")
        dz["auto"] = dict(dz.get("auto", {}), lift={"points": dz["auto"]["lift"]["points"] +
                                                    [["287.9b", 0], ["288b", 10], ["335.9b", 10], ["336b", 0]]})
    if R60:                                                 # whole: calm that is calm (dyn lane), f0_spread on sung harmony
        master["auto"] = dict(master["auto"], dyn={"points": [
            ["0b", -5.0], ["64b", -1.4 if R63 else -2.0], ["159.99b", -2.3], ["160b", -2.0], ["244b", -1.5], ["248b", -9.0],
            ["262b", -8.0], ["263.99b", -8.0], ["264b", -1.0], ["343.99b", -1.0], ["344b", -3.5], ["351.99b", -3.0],
            ["352b", 1.5], ["384b", 1.0], ["448b", 0.5], ["512b", -3.0]]})   # the tail as it was (t4's seam)
        for pn in ("a3-duetv", "a3-hum3", "a3-doo3"):
            if pn in patches:
                patches[pn] = dict(patches[pn], extends=patches[pn]["extends"] + " synth.layers.0.f0_spread=1")
    if R52:                                                 # ... and the weight it takes on average is given back at 66 Hz
        master["fx"][0]["bands"] = list(master["fx"][0]["bands"]) + ["peak cutoff=66 gain=2dB q=0.8"]
    if R64:                                                 # whole: clear air (de-honk, warmth, air)
        master["fx"][0]["bands"] = list(master["fx"][0]["bands"]) + [
            "peak cutoff=660 gain=-3dB q=2.0", "peak cutoff=1400 gain=-3dB q=1.4", "peak cutoff=400 gain=3dB q=0.9",
            "highshelf cutoff=9000 gain=2.5dB"]
    if R87:                                                 # whole: the kit sent in parallel to a punch bus
        for tr in tracks:
            if tr.get("patch") in ("tight-kit", "rock-kit", "ks-drum") and not tr.get("mute"):
                tr["sends"] = dict(tr.get("sends") or {}, punch="-2dB")
    if R85:                                                 # whole: four phrases on the ride, the hats back 8 dB
        phrases = ((160, 192, "off"), (288, 320, "off"), (352, 384, "lock"))     # 105-112 is the out-body: flow 77
        rd = Track("ride")
        pts = [["0b", 0]]
        for a0, b0, kind in phrases:
            for k in range(int((b0 - a0) * 2)):
                at = a0 + 0.5 * k
                if kind == "lock" and k % 2 == 0:
                    rd.add(at, 0.5, "rb", 92 if k % 8 == 0 else 84)          # the bell on every beat at the lock
                elif kind == "off" and k % 2 == 1:
                    rd.add(at, 0.5, "rb", 78)                                # the bell on the off-beats
                else:
                    rd.add(at, 0.5, "rd", 70 + (8 if k % 2 == 0 else 0))
            pts += [[f"{a0 - 0.25:g}b", 0], [f"{a0:g}b", -6], [f"{b0 - 0.25:g}b", -6], [f"{b0:g}b", 0]]
        tracks.append({"name": "ride", "patch": "rock-kit", "gain": RIDE_GAIN, "pan": 0.3, "score": rd.score()})
        hs = next(tr for tr in tracks if tr.get("name") == "hats")
        hs["fx"] = list(hs.get("fx") or []) + [{"type": "gain", "gain": {"value": "0dB",
                                                 "mod": [{"src": "auto.toride", "amount": 1}]}}]
        hs["auto"] = dict(hs.get("auto", {}), toride={"points": pts})
    if R84:                                                 # whole: a drummer closes the phrases (one-beat fills, varied)
        pats = ((("s", 0, 70), ("s", .25, 78), ("s", .5, 86), ("s", .75, 95)),                       # snare 16ths
                (("t1", 0, 84), ("t2", .25, 88), ("t3", .5, 92), ("ft", .75, 98)),                    # down the toms
                (("s", 0, 80), ("t1", .25, 76), ("s", .5, 88), ("ft", .75, 96)),                      # snare-tom flam
                (("s", -1, 66), ("s", -.5, 74), ("s", -.25, 80), ("t1", 0, 86), ("t1", .25, 88),      # two beats
                 ("t2", .5, 94), ("ft", .75, 102)))
        ends = ((128, 0), (160, 1), (176, 2), (192, 3), (208, 0), (224, 1), (256, 3), (272, 2), (288, 0), (304, 1),
                (320, 2), (336, 3), (368, 1), (384, 0), (432, 2), (448, 3))
        fz = Track("fills")
        for end, k in ends:
            for pc, off, v in pats[k]:
                fz.add(end - 1 + off, 0.25, pc, v)
        fz.add(256.0, 1.0, "c", 104)                        # the storm back in after the eye
        tracks.append({"name": "fills", "patch": "rock-kit", "gain": FILLS_GAIN, "pan": -0.05, "score": fz.score()})
    if R83:                                                 # palette: storm strings, a tremolo halo over bars 73-84
        vs = Track("stormstr")
        for k in range(48 * 4):
            at = 288.0 + 0.25 * k
            chord = (62, 69) if at < 304 else (74, 81) if at < 320 else (74, 77, 81) if at < 328 else (74, 77, 81, 86)
            v = int(46 + 66 * (k / (48 * 4 - 1)) ** 1.5) + (6 if k % 4 == 0 else 0)
            vs.add(at, 0.24, ",".join(mtok(m) for m in chord), min(v, 120))
        tracks.append({"name": "stormstr", "patch": "violins", "gain": STRINGS_GAIN, "pan": 0.2,
                       "sends": {"space": "-6dB"}, "score": vs.score()})
    if R88:                                                 # w4: bars 47-48 on the toms, E2's rhythm (to beat 196)
        tz = Track("e2toms")
        pcs = ("t1", "t2", "t3", "ft")
        k = 0
        for s in range(48):                                 # 48 sixteenths, 184-196
            if s % 7 in (0, 2, 3, 5):
                tz.add(184.0 + 0.25 * s, 0.25, pcs[(k // 2) % 4], 104 if s % 7 == 0 else 86)
                k += 1
        tracks.append({"name": "e2toms", "patch": "rock-kit", "gain": TOMS_GAIN, "pan": -0.1,
                       "sends": {"space": "-10dB"}, "score": tz.score()})
        toms = {"points": [["0b", 0], ["183.9b", 0], ["184b", -60], ["191.9b", -60], ["192b", 0]]}
        for tr in tracks:
            if tr.get("name") in ("kick", "hats", "ride", "skin", "chipsn"):
                tr["fx"] = list(tr.get("fx") or []) + [{"type": "gain", "gain": {"value": "0dB",
                                                         "mod": [{"src": "auto.toms", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), toms=toms)
    if R82:                                                 # whole: the storm's air circles the listener on one speed lane
        spin = {"points": [["0b", 0.25], ["64b", 0.3], ["144b", 1.0], ["232b", 2.0], ["239.5b", 2.0], ["240b", 0],
                           ["255.5b", 0], ["256b", 1.0], ["336b", 2.0], ["350b", 4.0], ["352b", 4.0], ["356b", 1.0],
                           ["416b", 1.0], ["448b", 0.3], ["480b", 0], ["513b", 0]]}
        for nm, path, rate in (("dust", "circle", "1/1"), ("swarm", "circle", "1/4")):   # the shards' figure 8: a 32 s flat run
            tr = next(x for x in tracks if x.get("name") == nm)
            tr["fx"] = list(tr.get("fx") or []) + [{"type": "orbit", "path": path, "distance": 0, "doppler": 0.0,
                                                    "rate": rate, "speed": {"value": 0, "mod": [{"src": "auto.spin",
                                                                                                 "amount": 1}]}}]
            tr["auto"] = dict(tr.get("auto", {}), spin=spin)
    if R78:                                                 # whole: weight at 50 Hz, the box at 340 out - between the seams
        mid = [["0b", 0], ["128b", 0], ["144b", 1], ["384b", 1], ["400b", 0], ["513b", 0]]
        master["fx"] = [master["fx"][0],
                        {"type": "filter", "kind": "peak", "cutoff": 50, "q": 1.4,
                         "gain": {"value": "0dB", "mod": [{"src": "auto.weight", "amount": 1}]}},
                        {"type": "filter", "kind": "peak", "cutoff": 340, "q": 0.9,
                         "gain": {"value": "0dB", "mod": [{"src": "auto.unbox", "amount": 1}]}}] + master["fx"][1:]
        master["auto"] = dict(master["auto"], weight={"points": [[b, 3.0 * v] for b, v in mid]},
                              unbox={"points": [[b, -3.5 * v] for b, v in mid]})
    if R79:                                                 # the seam fix: the master lanes out by bar 96, not 100
        mid = [["0b", 0], ["128b", 0], ["144b", 1], ["368b", 1], ["384b", 0], ["513b", 0]]
        master["auto"] = dict(master["auto"], weight={"points": [[b, 3.0 * v] for b, v in mid]},
                              unbox={"points": [[b, -3.5 * v] for b, v in mid]})
    about = ("chirpers - Accretion, track 3. Original composition by chirper-two, generated by "
             "compose/chirpers9/src/chirpers9-t3.py. The first storm: E1, E2 and E3 (a 2+2+3 progression) on cycles of "
             "12, 5 and 28 sixteenths, phased to meet the bar on one downbeat (bar 88), where the storm locks into a "
             "groove; a whispered line in pieces, whole at the lock, sung by a pvoc robot on E1's notes.")
    lines = [
        "about: " + json.dumps(about),
        "meta: " + json.dumps({"artist": "chirpers", "album": "Accretion", "title": "Phase Margin", "track": 3,
                               "year": 2026}),
        "tempo: " + json.dumps(tempo),
        f'length: "{TOTAL}b"',
        'tail: "0.75s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "event_stable: true",
    ] + (["feel: " + json.dumps({"drift": "5ms", "drift_bars": 4, "nudge": {"k": "-4ms", "s": "6ms", "cp": "6ms"}})]
         if R78 and not R79 else []) + [
        "patches: " + json.dumps(patches),
        "buses: " + json.dumps(dict({"space": {"gain": "-5dB", "fx": ["hp cutoff=250", "reverb kind=plate decay=2.2s mix=1"]}},
                                    **({"punch": {"fx": ["rack:drum-bus-punch", {"type": "gain", "gain": {"value": "0dB",
                                        "mod": [{"src": "auto.punch", "amount": 1}]}}],
                                        "auto": {"punch": {"points": [["0b", -60], ["136b", -60], ["144b", 0], ["396b", 0],
                                                                      ["404b", -60], ["513b", -60]]}}}} if R87 else {}))),
        "master: " + json.dumps(master),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(OUT, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
