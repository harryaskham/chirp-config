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
    if R52:                                                 # ... and the weight it takes on average is given back at 66 Hz
        master["fx"][0]["bands"] = list(master["fx"][0]["bands"]) + ["peak cutoff=66 gain=2dB q=0.8"]
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
        "patches: " + json.dumps(patches),
        "buses: " + json.dumps({"space": {"gain": "-5dB", "fx": ["hp cutoff=250", "reverb kind=plate decay=2.2s mix=1"]}}),
        "master: " + json.dumps(master),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(OUT, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
