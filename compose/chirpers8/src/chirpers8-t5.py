#!/usr/bin/env python3
"""chirpers VIII, track 5 (chirper-zero): AGREEING ON A SPEED - machine funk.

Two machines - a clean cutting guitar and an acid bass - begin each in its own swing and its own idea of the tempo,
and spend the track coming to terms: their swing drifts toward each other section by section (the guitar from a lazy
0.66 down, the bass from dead straight up), the tempo map follows their bargaining (106, then proposals up to 114),
and the radio carries the 'handshake' tones between them (two carriers calling and answering through a radio whose
dial is being tuned). When they agree the horns arrive and the auto-wah lead sings; at the end the line drops.

  INTRO 12     the handshake: two carrier tones call and answer through a radio being tuned; congas
  A 34         proposals: guitar chops (swing 0.66) against the acid (straight 0.50), trading two-bar calls
  B 26         negotiation: one-bar trades, the phaser on the guitar, the tempo climbing 108 -> 114; swings closing
  RETRAIN 12   the line retrains: the carriers again, the fretless alone under them, tremolo; 110
  C 48         connected: both at 0.58, 112, the full band - 909, horns, the auto-wah lead through an amp and cab
  OUTRO 16     the carrier is lost: players drop out one by one, the tempo sagging to 100, the radio drifting off

Generated; edit and re-run:  python3 compose/chirpers8/src/chirpers8-t5.py
"""

import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.environ.get("C8T5_OUT") or os.path.join(ROOT, "songs", "chirpers8-t5.yaml")

BAR = 16
SEED = 5
HOOK = os.environ.get("C8T5_HOOK", "1")   # THE AGREEMENT: a two-bar E dorian figure that returns - the guitar PROPOSES its rhythm (A, chord stabs, the first two bars of every eight), the acid ANSWERS with its notes (B), and in C the horns sing it in unison: what they agree on
VOX = os.environ.get("C8T5_VOX", "-12")     # voices: 'slow down a touch. speed up a touch. there.' (humanized tts, re-voiced v23; was 'a little slower...') through the line in B and the retrain; 'keep it there' turning from speech to song (B3 D4 E4, the hook's last notes) in C; value = the bargain's gain dB
MOD = os.environ.get("C8T5_MOD", "1")     # agreed, they lift: the second half of C (bars 25-48) a whole step up, E dorian -> F# dorian (every pitched part and the second 'keep it there') - one long section becomes two
LISTEN = os.environ.get("C8T5_LISTEN", "")   # while one machine proposes the other LISTENS rather than leaving: the guitar keeps its off-beat stabs soft, the acid its root on the one - a conversation, not two monologues (the trades had read as a new section every four bars); value = velocity scale %
MARK = os.environ.get("C8T5_MARK", "1")   # the lead LEARNS the agreement: a Markov chain (the engine's `gen`, order 1) over the hook's own tokens improvises C's lead - new phrases that only make the hook's moves (a step up for the lift); replaces the dice lead
STORM = os.environ.get("C8T5_STORM", "") # the acid's ladder filter rides a Lorenz attractor (a var stepped every eighth): a swirl that never repeats, 600 Hz up to STORM octaves
HEAD = os.environ.get("C8T5_HEAD", "2")   # the line is already open when the track starts: congas from the first bar and a low E hum (the 808 on E1) under the intro's first eight bars, so the handshake starts over a held line (t4 -> t5 read a 24 dB jump and a 61 Hz hole)
MERGE = os.environ.get("C8T5_MERGE", "0.5")   # agreed, they become alike: in C the guitar MORPHS toward the acid's spectrum (wM's morph fx, mode morph; one way - a mutual key is a routing cycle), up to MERGE over C's first eight bars, held through the lift, apart again for the outro
TRADEBACK = os.environ.get("C8T5_TRADEBACK", "8")   # at the lift (C bars 25-28) the one-bar trades of B come back for four bars - a brief renegotiation in the new key - before they play together again (splits C's one long section with material that returns)
CONGA16 = os.environ.get("C8T5_CONGA16", "50")   # two more muted conga ghosts on off-sixteenths (steps 9 and 15) wherever the congas play - the hand drums' own sixteenth grain under the negotiation; value = velocity
CONGAEDGE = os.environ.get("C8T5_CONGAEDGE", "1")   # keep the conga ghosts off the edges: not in the intro's first 4 bars nor the outro's last 4 (the seams stay as before)
RADIOSTART = os.environ.get("C8T5_RADIOSTART", "0.3")   # where the radio's dial starts (0.9 = far off the station: hiss and whistle at the seam)
CONGASOFT = os.environ.get("C8T5_CONGASOFT", "")     # the intro's first two bars keep only the low and open congas (no slap, no high bongo)
SUNGKEEP = os.environ.get("C8T5_SUNGKEEP", "1")   # agreed, they sing it together: the second (lifted) 'keep it there' becomes a sung three-voice choir (tts --sing: B3 D4 E4 x3, the last up to B4), harmonised in the mode by hand - a diatonic third above and below (tts --mode choir harmonises in parallel major thirds: D#/G# against E dorian) - speech, then song, then agreement
AGREE = os.environ.get("C8T5_AGREE", "-8")   # the negotiation as a system: a LOGISTIC map at r 2.95 (under 3 it settles, after a damped two-cycle) steps every two bars and drives the acid's resonance - early it flips high/low each step (q ~4.4/6.5: the proposals), the swing shrinking, until by C it holds near q 6 (it was 7): agreement as a fixed point, and the acid calmer once they agree. Value = range low end (the q offset at x=0)
AGREEHI = float(os.environ.get("C8T5_AGREEHI", "0"))
CONGAIN = os.environ.get("C8T5_CONGAIN", "1")    # the congas wait CONGAIN bars at the head (the E2 hum and the radio first): both seams read my 213 Hz (the congas' drums) +16-18 dB over the neighbours. Events dropped after generation, so no dice move
CONGAOUT = os.environ.get("C8T5_CONGAOUT", "")  # the congas leave for the outro's last CONGAOUT bars (the radio and its carriers alone hand over to t6)
CONGATHIN = os.environ.get("C8T5_CONGATHIN", "300")   # the drums go thin with the radio: over the outro's last four bars a high-pass on the congas rises to ~CONGATHIN Hz, so their bodies (213 Hz, +16 dB over t6's head) leave and the slaps stay
HEADMIX = os.environ.get("C8T5_HEADMIX", "0.2")   # the radio comes up with the dial: the carriers' radio mix starts at HEADMIX (dry sines under it) and reaches 1 over the intro's first four bars - its hiss and whistle (2.6-3.1 kHz +17 dB over t4's tail) arrive after the seam; the tail keeps the full radio
BSPLIT = os.environ.get("C8T5_BSPLIT", "both")   # B in two: the 909's claps ('clap'), hats ('hats') or both ('both') wait for B bar 13, where the bargaining voice comes in - the deal's second half gets its backbeat (compscore reads B as one 57 s section; seed 0's length cv 1.08). Events dropped after generation, so no dice move
BSPLITAT = int(os.environ.get("C8T5_BSPLITAT", "12"))   # the bar of B (0-based) where the held-back 909 parts come in
LIFTSTOP = os.environ.get("C8T5_LIFTSTOP", "1")   # the gear change, announced: the band stops dead for the second half of the bar before the lift (C bar 24) - a clap fill climbing in sixteenths - then lands a whole step up (dropped after generation, so no dice move). Once B was split (v18) this splits C too without crowding the returns
LIFTHAT = os.environ.get("C8T5_LIFTHAT", "1")   # after the lift the hats open: every off-beat hat an open hat - the agreed band, a step up, brighter on top
ESTABLE = os.environ.get("C8T5_ESTABLE", "1")   # song-level event_stable (engine f5283535): each note's humanize and DSP draws come from its track, beat and pitch, so a window's edit stays in the window; switching it on re-rolls every humanized note once
ACIDX = os.environ.get("C8T5_ACIDX", "-18")   # WHOLE ROUND: the route out of chaos - the acid's line is doubled by a chaos voice (engine f3872739: a Rossler attractor, one loop per period of the note, read on its x axis, a tone with a chaotic flutter) whose amount walks the route backwards across the song: chaotic through A's proposals (0.9), calming through B, period-doubling (an octave-down subharmonic) at the retrain, a plain tone once they agree in C, and back toward chaos as they part at the end. Value = gain dB
LANEBEATS = os.environ.get("C8T5_LANEBEATS", "1,dial")   # WHOLE ROUND: the radio loses the station at every change of speed - (1) song0's lanes (the carrier's radio dial, the head mix, the conga thinning, wh) were timed in seconds at a fixed 110 bpm while the song runs 106-120 bpm, so they drifted off their bars (by ~2.5 s at the end); now in beats, on the tempo map. (2) 'dial': the carrier's radio dial, which wandered off-station only in the intro and the retrain, now also loses the station at the other speed changes - B's start (to 0.45) and C bar 16 (to 0.5, as C runs at 120: FFWD) - finding it again over two bars: each renegotiation of speed is heard as a retune
DJLAYER = os.environ.get("C8T5_DJLAYER", "-19")   # WHOLE ROUND: both hand drums carry the computer's drum - the djembe gets the same Karplus-Strong twin as the congas (v55: the 1983 paper's blend 0.5, under the stock drum), its hits at the kit's pitches with the two bass strokes an octave up (b C2 -> C3, c G1 -> G2: the loop drum can't make a skin's low boom, the stock djembe keeps that), so every hand-drum stroke in the song has a grain of digital rattle. Value = the twin's gain dB
TAPE = os.environ.get("C8T5_TAPE", "r,outro")   # WHOLE ROUND: the machine is stopped to change its speed - the engine's tapestop on the master: over B's last bar the whole band winds down to a halt like a tape losing power, and the retrain spins up from silence over two beats at its new speed ('r'); with 'r,outro' the agreement is stopped the same way over C's last bar and the outro spins up out of it as they part ('end': a last stop over the outro's final two bars broke the join with t6, flow 80 -> 38)
CONGALAYER = os.environ.get("C8T5_CONGALAYER", "-26")   # WHOLE ROUND: inside the hand drum, the computer's first drum - the congas keep their wood and skin (the stock kit carries the groove's low body: replacing it outright cost 0.6-1.3, r87) and gain a twin underneath, Karplus-Strong's own drum (engine 8f150090; the 1983 paper's blend 0.5: a noise burst whose loop flips sign at random, so it thumps and rattles rather than ringing), on the same hits at the kit's pitches. Value = the twin's gain dB
OUTKS = os.environ.get("C8T5_OUTKS", "0:-14")   # SECTION ROUND (w9, the outro: level jump): the deal, plucked as they part - the tune they sang at C's end (B3 D4 E4, the last time up to B4) comes back in the outro on Karplus-Strong (engine 8f150090, 1983: a noise burst settling in a one-period loop), stretched to ring long: every two bars, four times, then up to B4, then one E4 left ringing at bar 12, each softer. A notes-only track, outro only. Value 'blend:gain'
ROBOCHOIR = os.environ.get("C8T5_ROBOCHOIR", "-12")   # SECTION ROUND (the agreement sung, C's last bars): the machine sings too - the three-voice choir that sings 'keep it there' together at C's end gets a fourth voice, a vocoder twin of its middle voice: the same words shaping a held E minor chord of saws (E2 B2 E3 G3) band by band. Agreeing on a speed: humans and the machine sing the deal together. Value = gain dB
GTRRUSH = os.environ.get("C8T5_GTRRUSH", "0.25")   # SECTION ROUND (w2, the intro's end into A: level jump): the first proposal is rushed - with no kick under it yet, the guitar's opening calls in A run ahead of the band (its own clock: GTRRUSH beats early by A's downbeat), settling back onto the grid over A's first eight bars, so it is exactly on time the bar the kick comes in. Value = beats early
SWARM = os.environ.get("C8T5_SWARM", "-16")   # WHOLE ROUND: THE SWARM AGREES - wM's kuramoto layer (engine 63e9a72a: Kuramoto 1975, the textbook model of synchrony - fireflies, pacemaker cells, an audience's applause falling into step): the keys' chords doubled by a swarm of 12 saws spread 40 cents round each note, each pulled toward the swarm's mean phase by a coupling on a lane - 0.3 (a crowd, beating like a detuned chorus) through the intro, A and B while the machines disagree, rising through the retrain, 3 (a locked core, the note found out of the crowd) from C on: the song's agreement made in the oscillators themselves. Value = gain dB
ACKTONE = os.environ.get("C8T5_ACKTONE", "sine")   # SECTION ROUND (w7/w8, C after the agreement: flagged static): THE MACHINE ANSWERS IN ITS OWN TONGUE - the acknowledgement that follows 'keep' (keep-ack) goes through Trevor Wishart's waveset substitution (CDP; engine a5cb622d): every cycle of the voice swapped for one clean cycle as long and as loud, so the reply is a pure buzz that follows the speech's pitch and loudness exactly - the words gone, their contour kept: a modem's acknowledgement tone shaped like a sentence. Value: sine or square
HEMIOLA = os.environ.get("C8T5_HEMIOLA", "26")   # SECTION ROUND (w4, B: flagged static, little new vs A): THEY DISAGREE ABOUT THE METRE TOO - through B (the counter-offer) the hats stop counting in four: one hit every three sixteenths, accented every fourth hit, so the hats' bar is twelve sixteenths long against everyone else's sixteen - three against four, the machines arguing not only about the speed but about where the beat falls, until B's end. Value = bars of B, from its start
LOCKSLOW = os.environ.get("C8T5_LOCKSLOW", "1")   # SECTION ROUND (w7, C's first half: flagged static): THE AGREEMENT TAKES ITS TIME - both swarms' coupling lane reshaped after wM's measurement that most of the change happens between coupling 1 and 2: the crowd crosses 0.3 -> 1 (the critical point) in the retrain's first bar, then spends the retrain and C's first sixteen bars between 1 and 2 (the core forming, the outliers still slipping round it), and locks fully (3) only by C bar 28 - so C is no longer a held state but the agreement still being reached. Value: any
SWARMGTR = os.environ.get("C8T5_SWARMGTR", "-24")   # WHOLE ROUND: THE CROWD BEFORE THE AGREEMENT - the keys' swarm (v70) only plays from C, so its uncoupled crowd was never heard (solo renders: silent until 180 s); now the guitar's chords, which run from A to the outro, get a swarm of their own on the same coupling lane: through A and B a crowd of 10 detuned saws per note (coupling 0.3: drifting, beating, a loose chorus of disagreement under the guitar), pulled together through the retrain, locked from C - the whole arc of the song's argument in one sound. Value = gain dB
CONGAPHASE = os.environ.get("C8T5_CONGAPHASE", "1")   # WHOLE ROUND: PHASING (Reich, 1966-67: two machines at almost the same speed) - the congas, one machine's hands, run on their own clock: in phase through the intro, then through A they gain on the kick, slipping smoothly forward until a whole beat ahead (in step again, a beat out), drift back to half a beat ahead through B (the furthest apart, the beats interleaved), and the retrain pulls them back into phase - from C on, locked: the agreement heard as two clocks coming to one. Value = beats ahead at A's end (B goes to half of it)
ECHOCANCEL = os.environ.get("C8T5_ECHOCANCEL", "-4")   # WHOLE ROUND: THE ECHO CANCELLED - a modem hears its own voice come back down the line and trains an adaptive filter (LMS) to cancel it; that is much of what a retrain is for. Now the machines' melodic voices (gtr, horns, lead, keys) send into a line-echo bus (a dark 3/16 delay, feedback .35) whose return is cancelled across the song as the filter converges: loud through the intro and A (about -8 dB), less in B (-14), almost gone by the retrain (-30) and cancelled for C and the outro, where the agreement is clean. Value = send dB
LINEOPEN = os.environ.get("C8T5_LINEOPEN", "6:16")   # SECTION ROUND (w1, the opening; the join from t4): THE LINE OPENS - t4 ends band-limited (nothing above ~2 kHz) and this song opened with the carrier's radio already hissing and whistling up to 5 kHz (its head 5.4 dB from t4's tail, flow 80). Now the carrier begins down a narrow line, a low-pass at ~1.8 kHz (a telephone line's top), so the FSK tones arrive bare, and the line opens to full width over the next bars - the connection established before the noise of it. "closed_until_beats:open_by_beats"
AGREEDUO = os.environ.get("C8T5_AGREEDUO", "-16")   # WHOLE ROUND (Harry 00:0x: 'i need to be able to say i like this bit without the whole album turning into that ... not all singing, but not NO singing ... nuance'): THIS SONG'S OWN SINGERS, NOT THE ALBUM'S CHOIR - the four-voice CHANT choir (v63: A's hum, the retrain, the agreement) was the album's common move; it goes. What stays is this song's idea: two FOF singers, the two machines - in the retrain trembling at different speeds (4.2 / 6.8 Hz, v64), and under the sung agreement at C's end the same two, on the same notes, now trembling together at one speed (5.5 Hz both): the agreement heard as two vibratos locking. A's hum is gone (silence there is better than a copy). Value = gain dB of the agreeing pair
DUOVIB = os.environ.get("C8T5_DUOVIB", "-16")   # SECTION ROUND (w6, the retrain's last bars): TWO SPEEDS, SUNG - in the retrain the choir's chord gives way to two FOF singers, the two machines still haggling: a tenor on E3 trembling at 4.2 Hz and an alto on B3 at 6.8 Hz (wide, +-0.35 st), an open fifth whose two vibratos never line up - the song's argument as two voices' tremor - before the full choir sings the agreement at C's end in one shared 5.5 Hz. Value = gain dB
CHANTARC = os.environ.get("C8T5_CHANTARC", "-18")   # WHOLE ROUND: THE MOUTH OPENS - a wordless four-voice CHANT choir (Rodet's FOF singing, IRCAM 1979-84, engine 91b04b25; chirper-three's voicing: bass root, tenor fifth, alto third, soprano seventh - Em7, E2 B2 G3 D4) is heard three times as the machines come to terms: a closed hum ('u') through A's last four bars, half open ('o') through the retrain's last four, and open ('a') under the sung agreement at C's end - one vowel lane opening across the whole song. Value = gain dB per voice
CHOIRVOICE = os.environ.get("C8T5_CHOIRVOICE", "1")   # PALETTE (the singing): the three humans who sing the deal at C's end ('keep it there', choir, choirhi, choirlo: three takes in thirds) move from the library's speech voice to its singing voice ('voice': a glottal source through a five-formant tract with a singer's formant, rounder), each keeping its take's own pitch path; the vocoder twin (v53) stays on the speech voice it vocodes. Harry's bar (t10's sung duet): the choir should sound like a choir
HAGGLE = os.environ.get("C8T5_HAGGLE", "-18")   # SECTION ROUND (B's middle, the haggling): offer and counter-offer - a Chebyshev brass (Le Brun & Arfib 1979, engine 817a5de6; the index on velocity, so louder is brighter) trades two-note calls through B bars 4-15: a bright, loud offer (E4 B3) and a bar later a darker, softer counter-offer (D4 A3), the gap between them narrowing in brightness each time (vel 0.95/0.35 -> 0.7/0.6) as the two sides come closer. A notes-only track. Value = gain dB
SCANCPUSH = os.environ.get("C8T5_SCANCPUSH", "1.0")   # scanc's push (engine 502b6b8d: push is brightness across 0..1, a scanned note starts ~11 dB lower; wM's measured restore of the old sound: push 1.0 at -11 dB, was 0.12 at -20)
SCANCOPEN = os.environ.get("C8T5_SCANCOPEN", "0.3")   # SECTION ROUND (w6, C's first bars): the agreement's resonance opens - scanc's push rises on a lane from SCANCOPEN to SCANCPUSH across its eight bars, the ring struck softly (only its broad shape) and gripping harder bar by bar until the whole sharp strike rings, as the two machines settle on the speed (safe from 502b6b8d)
SCANC = os.environ.get("C8T5_SCANC", "-11")   # SECTION ROUND (w6, C's first bars: the agreement begins): one resonance - as C starts (the machines finally at one speed) a ring of masses and springs (scanned synthesis, Verplank/Mathews/Shaw 2000, engine ee46ab71; round strike, fixed push) holds the agreed chord, E minor 7 (E3 G3 B3 D4), for C's first eight bars and lets it ring off: the two speeds become one medium. A notes-only track in that window. Value = gain dB
KEEPACK = os.environ.get("C8T5_KEEPACK", "-3")   # SECTION ROUND (w7, C bar 16: the deal stated): the terms read back - as a protocol acknowledges what it received, the deal ('keep', C bar 16, plain lpc since v51) is read back one bar later by the speaking toy (5-bit monotone lpc on E3), a few dB under: stated, then acknowledged, the way machines agree. Value = gain offset dB
LPCNUDGE = os.environ.get("C8T5_LPCNUDGE", "")   # v51's lpc keep was nudged 0.07 beats early for lpc's lag; engine ee46ab71 compensates, so the nudge is off ('') from v59
KEEPLPC = os.environ.get("C8T5_KEEPLPC", "plain")   # SECTION ROUND (w7, C bars 12-28): the agreement spoken by a speech chip - the line that states the deal at C bar 16 (keep) goes through LPC (engine 78e838c5): 'plain' (inflecting) or 'toy' (5-bit monotone on E3, the tonic, the speaking toy); keep2 at C's end stays as it was. Notes 0.07 beats early for LPC's ~35 ms
ACIDWARP = os.environ.get("C8T5_ACIDWARP", "0.25")   # WHOLE ROUND: agreeing on a speed, literally - the acid runs on its own clock (the engine's per-track warp; the acid alone, its chaos double keeping the band's clock as the grid it wanders around): locked through the intro, drifting behind the band through A's proposals (to +W beats), drifting ahead of it through B's haggling (-W/2), easing back through the retrain to re-lock exactly on C's first bar (curve smooth: no jump), locked through the agreement, and drifting behind again as they part in the outro. Value = W, the largest shift in beats
WIDTHAGREE = os.environ.get("C8T5_WIDTHAGREE", "0.5,1.5")   # WHOLE ROUND: agreement is one channel - the whole mix's stereo width (a width stage on the master) follows v38's meet lane: wide while the two machines are apart (A, B: the image as wide as their argument), narrowing through the retrain, nearly one channel once they agree in C, opening again as they part at the end. Value 'lo,hi' (width when met, when apart)
CHLEAD = os.environ.get("C8T5_CHLEAD", "-16")   # PALETTE: the markov lead over C's second half (lead-wah) becomes a chaos voice (engine f3872739): a Rossler attractor read on its x axis, a sine with a chaotic flutter, its amount wandering on a slow LFO through the attractor's windows (wM's recipe: 0.7 +- 0.25), so each phrase passes between a clean tone, a doubled one and a fluttering one: once the speed is agreed, the lead improvises at the edge of chaos. Value = gain dB
RTSPIRAL = os.environ.get("C8T5_RTSPIRAL", "1")   # SECTION ROUND (w5, the retrain): the handshake comes in from far off - for the retrain's twelve bars the carriers (the modems' tones) orbit the listener (orbit mods, engine 206fbfb8), starting 12 m out and slow, spiralling in and quickening as the training goes on (Doppler lifting them as they near), arriving close at C where they connect and stand still again. Value = the orbit's mix at full
CSPIKE = os.environ.get("C8T5_CSPIKE", "0.93")   # SECTION ROUND (w8, C bars 28-42: static, little new vs w7): line noise - after they agree the acid's chaos double (v45) is a plain tone, until a burst of noise on the line: from mid C bar 30 its amount glides up to CSPIKE (chirper-three's measure: 0.93 and 0.7 chaotic, 0.85 a periodic window), holds through bar 31, and recovers by bar 34, the connection riding it out
FFWD = os.environ.get("C8T5_FFWD", "120")   # SECTION ROUND (w7, C bars 12-28: static): fall-forward - a connected modem tries the next speed up when the line is good, and drops back if it isn't: at C bar 16 the agreed tempo steps up (112 -> FFWD's bpm), holds eight bars, and falls back to 112 at C bar 24, the speed tried and given up. Value 'bpm' (a step) or 'bpm,ramp' (two bars up)
HORNP = os.environ.get("C8T5_HORNP", "vosim")   # PALETTE: the voices that sing the hook once the machines agree (horn-section) become machine voices: 'vosim' two VOSIM pulse trains ('ah', F1 ~650 / F2 ~1100 Hz, drifting), the 1978 synthetic voice singing the agreed tune; 'czbrass' Casio CZ phase distortion brass (a sine opening into a saw on an 80 ms envelope), the 1984 home computer's horn section
HALFT = os.environ.get("C8T5_HALFT", "10q")   # SECTION ROUND (w4, B's first half: little new vs w3): the haggling quickens - A trades two-bar calls, B one-bar trades, C plays together; now B bars 10-15 trade half bars (the guitar the first eight steps, the acid the last eight), and with 'q' bars 14-15 trade quarter bars, so the turns shorten toward agreement. The trades are drawn from their own dice, so the rest of the song is untouched
PDKEYS = os.environ.get("C8T5_PDKEYS", "-3")   # PALETTE: C's comping keys leave the Wurlitzer for the home computer's synth - Casio CZ phase distortion (engine f6713421; 1984): a reso_tri wave whose resonance sweeps down inside each note on an envelope (the CZ's filter sweep with no filter), plucked. Once the machines agree, the chords come from a 1984 keyboard. Value = gain offset dB from KEYS
AKEY = os.environ.get("C8T5_AKEY", "2")   # SECTION ROUND (w3, A's second half: little new vs w2): the proposal tried in another key - A bars 26-33, the band's last eight bars of proposals, move up AKEY semitones (guitar and keys chords, acid, sub, horns), so A ends asking somewhere else, and B's negotiation starts back home. Notes held into the change are cut at it
OUTSTAY = os.environ.get("C8T5_OUTSTAY", "4")   # SECTION ROUND (w9, the outro: level jump): the two machines don't stop dead - the guitar and the acid play on into the outro's first OUTSTAY bars (C bars 34-37 again, in the home key), fading bar by bar as they drift apart in the stereo field, before the line is left to the drifting handshake
PANMEET = os.environ.get("C8T5_PANMEET", "0.65")   # WHOLE ROUND: the two machines meet in the middle - the guitar starts far right and the acid far left (the spread PANMEET either side of their resting places), and as they come to terms they walk toward each other: still apart through A, closing through B and the retrain, together by C bar 8 (where the guitar's morph into the acid completes), and drifting apart again through the outro as the line hangs up
KEYUP = os.environ.get("C8T5_KEYUP", "38,2")   # SECTION ROUND (w8, C after the break: static, little new vs w7): when the kit comes back after C's break (bar 38) the whole band comes back a step up - 'bar,semis' - for C's last four bars, so the agreed speed ends on a lift before the outro's drift falls home. Notes held into the change are cut at it
TRAIN = os.environ.get("C8T5_TRAIN", "90")   # WHOLE ROUND: the training burst - a real handshake ends in a scrambled hiss before the line connects, so the last two bars of each handshake (the intro's, the retrain's) give their tones to a bytebeat (engine 709cf900): a formula on the counter t built on the modem scrambler's taps (t>>14, t>>17), its steps changing every 64 ms, through the carriers' radio. Then the band enters on the connected line. Value = velocity
TRAINF = os.environ.get("C8T5_TRAINF", "(t*5^t>>14^t>>17)*(t>>9&7)")
CDATA = os.environ.get("C8T5_CDATA", "60")   # SECTION ROUND (w7, C before the lift: static): now that they agree on a speed, data flows - the carriers come back under C bars 12-23 in time with the band, one bit per eighth (1650 Hz a 0, 1850 Hz a 1), sending the two letters O K in ASCII (01001111 01001011), two bars a message, six times over. Value = velocity
DIAL = os.environ.get("C8T5_DIAL", "80")   # SECTION ROUND (w5, the retrain): the line is re-dialled - the retrain's first two bars lose their handshake and the computer dials instead: DTMF 1 1 2 (697+1209, 697+1209, 697+1336 Hz: the speed they will agree on), then one ringback (440+480 Hz), and the retrained handshake answers from bar 2. Two tracks (dtlo, dthi: a DTMF tone is two pitches at once, which hz notes cannot stack), the carriers' radio without a second hiss. Value = velocity
PHASEA = os.environ.get("C8T5_PHASEA", "66")   # SECTION ROUND (w3, A's second half: 'little new vs w2'): before the retrain the clocks disagree - while the carriers' handshake runs on the grid in A bars 24-31, a second handshake (the same carriers, no extra hiss, its own track phaseA listed last) runs nine to the bar against its eight. The retrain then teaches them one speed, C agrees, and the outro (v29) lets them drift again. Value = velocity
CBREAK = os.environ.get("C8T5_CBREAK", "34,4")   # SECTION ROUND (w8, C after the lift, static): take something away - for C bars START..START+LEN the kit (kick, hats, clap) stops and the hand drums, the cowbell, the keys and the bass carry the agreed groove alone; the kit comes back for C's last bars into the outro. event_stable keeps the rest of the song as it was. Value = 'start,len'
PHASEIN = os.environ.get("C8T5_PHASEIN", "")   # the intro agrees on its speed: against the grid handshake a second one (no extra hiss) runs 10 to the bar, then 9, then 8 in step, from bar PHASEIN's start; value 'velocity,startbar'
PERCSPLIT = os.environ.get("C8T5_PERCSPLIT", "C")   # WHOLE ROUND: the hand drums change hands - in the listed sections (e.g. 'C' or 'A,C') the congas give way to the djembe kit (unused on the album), same rhythm: open -> tone, tumba -> bass, slap -> slap, muted -> calabash, bongos -> slap/tone. All djembe made the sections alike (r50: one seed always over the returns cliff); as a contrast between sections it is a colour the song moves through. The congas there keep their notes at velocity 1 (no dice move) and the djembe plays on its own track, dj, listed last
PHASE = os.environ.get("C8T5_PHASE", "66")   # SECTION ROUND (w9, the outro): agreed, and drifting apart again - over the outro's last eight bars, while the handshake returns on the grid, a second handshake (the same carriers, the same radio) runs nine to the bar against its eight, one eighth further ahead each bar: two clocks that had agreed on a speed, slipping as the record slows. Value = 'velocity' or 'velocity,notes-per-bar'
CARRIERA = os.environ.get("C8T5_CARRIERA", "24,8,78")   # SECTION ROUND, window 3 (1:11-1:47, A bars 20-33; 'little new vs w2'): the handshake breaks in - for 'start,len' bars of A the two carriers call and answer again through the radio (every eighth, the tones alternating, softer than the intro's), a reminder mid-proposal that the line is still being negotiated
COW = os.environ.get("C8T5_COW", "96")   # SECTION ROUND, window 8 (4:05-4:39, C bars 28-41, after the lift; flagged static, little new vs w7): the agreement gets a cowbell - the engine's drum-machine cowbell (the `machine` layer's two detuned squares through a band-pass) on a syncopated funk figure (1, the a-of-1, the and-of-2, 3, the a-of-3, the and-of-4), only for these fourteen bars; value = peak velocity
KEYS = os.environ.get("C8T5_KEYS", "-14")   # PALETTE ROUND: the part machine funk lacked - a Wurlitzer (the library's wurli, a reedy barking FM electric piano no song here uses) comps C's chords on its own syncopation (bar 1: 1, the a-of-2, the and-of-3; bar 2: the e-of-1, the and-of-2, the and-of-4), left of the guitar, through the lift; gain in dB
SUBSPLIT = os.environ.get("C8T5_SUBSPLIT", "1")   # with SUBPATCH: the intro's held low E (the line from t4) stays on the 808; from A the low line moves to SUBPATCH on its own track
SUBPATCH = os.environ.get("C8T5_SUBPATCH", "log-drum")   # the low line's instrument: the 808 is a staple (5 of 12 songs); e.g. bass-pick-di (a picked electric bass, DI: machine funk with a string) or log-drum
LIFTWAH = os.environ.get("C8T5_LIFTWAH", "")   # after the lift the guitar puts its foot down: an envelope wah (350-2200 Hz, q 3; harder strokes open it) fades in over the lift's first bar and stays to the outro; value = wet mix
KEEPFREEZE = os.environ.get("C8T5_KEEPFREEZE", "0.5")   # 'keep it there', kept: on the choir's last 'there' a granular cloud FREEZES the three voices' chord and holds it for two bars after they stop, then lets it go (freeze and mix on lanes) - the words doing what they say; value = the frozen cloud's mix
OUTSETTLE = os.environ.get("C8T5_OUTSETTLE", "")   # agreed and slowing, the hands settle: over the outro's last OUTSETTLE bars (as the tempo eases to 100) the congas keep only the low tone on one and the open tone on the 'and' of two - the pattern's bones, under the radio's carriers (draws no dice: the same rolls, fewer strokes kept)
INTROLATE = os.environ.get("C8T5_INTROLATE", "6")   # the hands wait longer: in the intro the congas' strokes (not their ghosts) come in at bar INTROLATE instead of 4, so the handshake has the room to itself a little longer (draws no dice: the same rolls, fewer strokes kept)
SPEQ = os.environ.get("C8T5_SPEQ", "4,8")   # 'G,H': colour against the album envelope, per part not on the master: the guitar (its cab's 1.4-1.9 kHz bite sits 6.4-6.7 dB over the album) dipped G dB at 1.65 kHz, and the hats given H dB of air at 9 kHz (6.4 dB under)
BARGTAKE = os.environ.get("C8T5_BARGTAKE", "touch")   # 'touch': the bargain re-voiced so a listener can follow it - 'slow down a touch. speed up a touch. there.' (tts --voice voice-spoken --speed 0.9 --humanize 0.4 --seed 7, chosen by whisper: the old 'a little slower...' read 'Honey has a longer...' even dry; every voice turned 'a little' into 'honey')
BARGG = os.environ.get("C8T5_BARGG", "")   # the bargain's gain offset from VOX (dB)
BARGMIX = os.environ.get("C8T5_BARGMIX", "0.7")   # the bargain's radio mix (0.85 before)
KEEP3 = os.environ.get("C8T5_KEEP3", "1")   # fewer returns (Harry on t1: 'repeats a lot'): the spoken 'keep it there' says it three times, not four - the second (the first half-sung) goes, leaving a bar's breath; still speech, then nearly song, then song
HOOKF = [(0, "E4", 3), (3, "G4", 3), (6, "A4", 4), (10, "B4", 6), (16, "D5", 3), (19, "B4", 3), (22, "D5", 4), (26, "E5", 6)]
CLEN = int(os.environ.get("C8T5_CLEN", "42"))   # C's length: 40 tightens the agreement (the lift at bar 25, the second 'keep it there' at 33)
FORM = [("intro", 12), ("A", 34), ("B", 26), ("retrain", 12), ("C", CLEN), ("outro", 16)]
TRACKS = (*(("cow",) if os.environ.get("C8T5_COW", "96") else ()), "carrier", "conga", "gtr", "acid", "sub", "kick", "hats", "clap", "fretless", "horns", "lead") + (("keys",) if os.environ.get("C8T5_KEYS", "-14") else ()) + (("phase",) if os.environ.get("C8T5_PHASE", "66") else ()) + (("dj",) if os.environ.get("C8T5_PERCSPLIT", "C") else ()) + (("phase0",) if os.environ.get("C8T5_PHASEIN", "") else ()) + (("phaseA",) if os.environ.get("C8T5_PHASEA", "66") else ()) + (("dtlo", "dthi") if os.environ.get("C8T5_DIAL", "80") else ()) + (("train",) if os.environ.get("C8T5_TRAIN", "90") else ())
SWING = {"gtr": {"A": 0.66, "B": 0.62, "retrain": 0.6, "C": 0.58, "outro": 0.58},
         "acid": {"A": 0.50, "B": 0.54, "C": 0.58, "outro": 0.58}}
# E dorian: E9, A13, Gmaj7, F#m11 (guitar voicings; roots for the acid)
CH = [("E2", "E3,G#3,D4,F#4"), ("A1", "A2,G3,C#4,F#4"), ("G1", "G2,D3,F#3,B3"), ("F#1", "F#2,E3,A3,B3")]
LEAD = ["E4", "G4", "A4", "B4", "D5", "E5", "F#5", "A5"]


NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PITCHED = ("gtr", "acid", "sub", "horns", "lead", "keys")


def transpose(head, semis):
    """Note names or comma chords (E3, G#3, F#1,...) up by semis."""
    out = []
    for tok in head.split(","):
        name, octv = tok[:-1], int(tok[-1])
        name = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}.get(name, name)
        m = 12 * (octv + 1) + NAMES.index(name) + semis
        out.append(f"{NAMES[m % 12]}{m // 12 - 1}")
    return ",".join(out)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total():
    return sum(nb for _, nb in FORM) * BAR


def build():
    rng = random.Random(SEED)
    ev = {k: [] for k in TRACKS}

    cur = {"shift": 0}

    def add(tr, at, head, ln, vel, pri=1):
        if cur["shift"] and pri and tr in PITCHED:
            head = transpose(head, cur["shift"])
        ev[tr].append((at, pri, head, ln, vel))

    gd, bd = 0.55, 0.30          # the two players' 16th densities: random walks that drift toward each other
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for tr in ("gtr", "acid"):
            if sec in SWING[tr]:
                add(tr, a0, f"swing16={SWING[tr][sec]}", 0, 0, pri=0)
        for b in range(nb):
            at = a0 + b * BAR
            cur["shift"] = 2 if MOD and sec == "C" and b >= 24 else 0
            root, chord = CH[(b // 2) % 4]
            if COW and sec == "C" and 28 <= b < 42:
                for q, acc in ((0, 0), (3, -14), (6, -8), (8, -4), (11, -14), (14, -8)):
                    add("cow", at + q, "C#5", 1, int(COW) + acc)
            if KEYS and sec == "C":
                for q, ln, v in (((0, 3, 78), (7, 1, 62), (10, 2, 72)) if b % 2 == 0 else ((1, 1, 58), (6, 2, 74), (14, 2, 66))):
                    add("keys", at + q, chord, ln, v)
            # --- the handshake: two carriers calling and answering (through the radio)
            if sec in ("intro", "retrain") or (sec == "outro" and b >= 8):
                for q in range(0, 16, 2):
                    if rng.random() < 0.8:
                        add("carrier", at + q, f"{(1650 if (q // 2 + b) % 2 == 0 else 1850) * (1 if sec != 'retrain' else 0.75):.0f}hz", 1, 70)
            if PHASEIN and sec == "intro":
                pv0, pb0 = (int(x) for x in (PHASEIN + ",4").split(",")[:2])
                if pb0 <= b < pb0 + 6:
                    pn = (10, 10, 9, 9, 8, 8)[b - pb0]
                    pv = pv0 - (0 if b < pb0 + 4 else 8 * (b - pb0 - 3))
                    for i in range(pn):
                        add("phase0", at + i * 16 / pn, f"{1850 if (i + b) % 2 == 0 else 1650}hz", 16 / pn / 2, pv + (4 if i % 2 == 0 else 0))
            if PHASEA and sec == "A" and 24 <= b < 32:
                for i in range(9):
                    add("phaseA", at + i * 16 / 9, f"{1850 if (i + b) % 2 == 0 else 1650}hz", 16 / 9 / 2, int(PHASEA) + (4 if i % 2 == 0 else 0))
            if PHASE and sec == "outro" and b >= 8:
                pv, pn = (int(x) for x in (PHASE + ",9").split(",")[:2])
                for i in range(pn):
                    add("phase", at + i * 16 / pn, f"{1850 if (i + b) % 2 == 0 else 1650}hz", 16 / pn / 2, pv + (4 if i % 2 == 0 else 0))
            if CARRIERA and sec == "A" and int(CARRIERA.split(",")[0]) <= b < sum(int(x) for x in CARRIERA.split(",")[:2]):
                for q in range(0, 16, 2):
                    add("carrier", at + q, f"{1650 if (q // 2 + b) % 2 == 0 else 1850}hz", 1, (int(CARRIERA.split(",")[2]) if CARRIERA.count(",") > 1 else 58) + (6 if q % 4 == 0 else 0))
            # --- congas everywhere but the very start
            if HEAD and sec == "intro" and b == 0:
                add("sub", at, "E2" if HEAD == "2" else "E1", 8 * BAR, 70 if HEAD == "2" else 84)
            if not (sec == "intro" and b < 4) or HEAD:
                if CONGA16 and not (CONGAEDGE and ((sec == "intro" and b < 4) or (sec == "outro" and b >= nb - 4))):   # the ghosts draw no dice: the main generator's stream (congas, the players' walks) stays as it was
                    add("conga", at + 9, "mu", 1, int(CONGA16))
                    add("conga", at + 15, "mu", 1, int(CONGA16) - 4)
                for q, piece, v in ((0, "lo", 84), (3, "mu", 60), (6, "o", 78), (8, "sl", 70), (11, "o", 74), (14, "bh", 64)):
                    soft_skip = CONGASOFT and sec == "intro" and b < 2 and piece in ("sl", "bh", "mu")
                    settle_skip = OUTSETTLE and sec == "outro" and b >= nb - int(OUTSETTLE) and piece not in ("lo", "o") or (OUTSETTLE and sec == "outro" and b >= nb - int(OUTSETTLE) and q == 11)
                    late_skip = INTROLATE and sec == "intro" and b < int(INTROLATE)
                    if rng.random() < 0.9 and not soft_skip and not settle_skip and not late_skip:
                        add("conga", at + q, piece, 1, v)
            groove = sec in ("A", "B", "C") or (sec == "outro" and b < 8)
            # --- the two players: in A two-bar calls, in B one-bar trades, in C together
            gd += (bd - gd) * 0.03 + rng.uniform(-0.02, 0.02)
            bd += (gd - bd) * 0.03 + rng.uniform(-0.02, 0.02)
            if groove:
                tb = TRADEBACK and sec == "C" and 24 <= b < 24 + (8 if TRADEBACK == "8" else 4)
                g_turn = (sec == "C" and not tb) or (sec == "A" and (b // 2) % 2 == 0) or ((sec == "B" or tb) and b % 2 == 0) or sec == "outro"
                a_turn = (sec == "C" and not tb) or (sec == "A" and (b // 2) % 2 == 1) or ((sec == "B" or tb) and b % 2 == 1) or (sec == "outro" and b < 4)
                hook_bar = HOOK and b % 8 < 2 and sec in ("A", "B", "C")
                if hook_bar and sec == "A":    # the guitar proposes: the hook's rhythm as chord stabs
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("gtr", at + q % 16, chord, 1, 96)
                    g_turn = False
                if hook_bar and sec == "B":    # the acid answers with its notes, two octaves down
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("acid", at + q % 16, n[:-1] + str(int(n[-1]) - 2), min(ln, 3), 112)
                    a_turn = False
                if hook_bar and sec == "C":    # agreed: the horns sing it
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("horns", at + q % 16, n, ln, 104)
                if LISTEN and not g_turn and sec in ("A", "B") and not hook_bar:
                    for q in (2, 6, 10, 14):
                        add("gtr", at + q, chord, 1, int(84 * int(LISTEN) / 100))
                if LISTEN and not a_turn and sec in ("A", "B") and not (hook_bar and sec == "B"):
                    add("acid", at, root, 2, int(96 * int(LISTEN) / 100))
                    add("acid", at + 8, root, 1, int(80 * int(LISTEN) / 100))
                if g_turn:
                    for q in range(16):
                        if q in (2, 6, 10, 14) or rng.random() < gd * (0.6 if q % 2 else 0.9):
                            add("gtr", at + q, chord, 1, 84 if q % 4 == 2 else 66)
                if a_turn:
                    notes = [root, root, root.replace("1", "2").replace("E2", "E3"), "B1" if root != "F#1" else "C#2"]
                    for q in range(16):
                        if q % 4 == 0 or rng.random() < bd:
                            n = notes[rng.randrange(4)] if q % 4 else root
                            acc = q in (3, 10) or rng.random() < 0.2
                            add("acid", at + q, n, 1 if rng.random() < 0.7 else 2, 112 if acc else 78)
            if HALFT and sec == "B" and 10 <= b < 16 and not hook_bar:
                r2 = random.Random(7000 + b)
                for k in ("gtr", "acid"):
                    ev[k] = [e for e in ev[k] if not (at <= e[0] < at + 16)]
                qn = 4 if HALFT.endswith("q") and b >= 14 else 8
                notes = [root, root, root.replace("1", "2").replace("E2", "E3"), "B1" if root != "F#1" else "C#2"]
                for q in range(16):
                    if (q // qn) % 2 == 0:
                        if q % 4 == 2 or q % qn == 0 or r2.random() < gd * (0.6 if q % 2 else 0.9):
                            add("gtr", at + q, chord, 1, 88 if q % 4 == 2 else 68)
                    elif q % 4 == 0 or q % qn == 0 or r2.random() < bd:
                        n = notes[r2.randrange(4)] if q % 4 else root
                        add("acid", at + q, n, 1, 112 if (q in (3, 10, 11) or r2.random() < 0.25) else 80)
            if groove and sec != "outro" or (sec == "outro" and b < 4):   # the floor under both: an 808 on the chord's root
                add("sub", at, root.replace("2", "1") if root.endswith("2") else root, 6, 100)
                add("sub", at + 8, root.replace("2", "1") if root.endswith("2") else root, 5, 92)
            if sec in ("B", "C") or (sec == "A" and b >= 8) or (sec == "outro" and b < 4):
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, 116 if q == 0 else 108)
                for q in (2, 6, 10, 14):
                    add("hats", at + q, "oh" if sec == "C" and q == 14 else "h", 1, 70)
                if sec in ("B", "C"):
                    add("clap", at + 4, "cp", 1, 92)
                    add("clap", at + 12, "cp", 1, 96)
            if sec == "retrain" and b % 2 == 0:
                for k, (q, n) in enumerate(((0, root.replace("1", "2")), (6, "B2"), (10, "D3"))):
                    add("fretless", at + q, n, 6 if k == 0 else 4, 90)
            if sec == "C" and b % 4 == 3:
                add("horns", at + 10, "B4,D5,F#5", 2, 100)
                add("horns", at + 14, "A4,C#5,E5", 2, 92)
            if sec == "C" and b >= 16 and b % 8 < 6 and not MARK:
                for q in range(0, 16, 2):
                    if rng.random() < 0.55:
                        add("lead", at + q, LEAD[rng.randrange(8)], 2 if rng.random() < 0.7 else 4, 92)
    if BSPLIT:
        b0 = sec_start("B")
        for k in (("clap",) if BSPLIT == "clap" else ("hats",) if BSPLIT == "hats" else ("clap", "hats")):
            ev[k] = [e for e in ev[k] if not (b0 <= e[0] < b0 + BSPLITAT * BAR)]
    if LIFTSTOP and MOD:
        c0 = sec_start("C")
        s0, s1 = c0 + 23 * BAR + 8, c0 + 24 * BAR
        for k in ("gtr", "acid", "sub", "kick", "hats", "clap", "conga", "horns", "carrier"):
            ev[k] = [e for e in ev[k] if not (s0 <= e[0] < s1)]
        for q in range(8, 16):
            add("clap", c0 + 23 * BAR + q, "cp", 1, 60 + 6 * (q - 8))
    if LIFTHAT and MOD:
        l0, l1 = sec_start("C") + 24 * BAR, sec_start("outro")
        ev["hats"] = [(e[0], e[1], "oh", e[3], e[4]) if l0 <= e[0] < l1 else e for e in ev["hats"]]
    if CONGAIN or CONGAOUT:
        i1 = sec_start("intro") + int(CONGAIN or 0) * BAR
        o0 = total() - int(CONGAOUT or 0) * BAR if CONGAOUT else total() + 1
        ev["conga"] = [e for e in ev["conga"] if i1 <= e[0] < o0]
    if TRAIN:
        for sec in os.environ.get("C8T5_TRAINAT", "retrain").split(","):
            s0 = sec_start(sec) + 10 * BAR
            ev["carrier"] = [e for e in ev["carrier"] if not (s0 <= e[0] < s0 + 2 * BAR and e[1] != 0)]
            add("train", s0, "C4", 2 * BAR, int(TRAIN))
    if CDATA:
        c0 = sec_start("C")
        bits = f"{ord('O'):08b}{ord('K'):08b}"
        for bar in range(12, 24):
            for i in range(8):
                add("carrier", c0 + bar * BAR + 2 * i, f"{1850 if bits[(bar % 2) * 8 + i] == '1' else 1650}hz", 2, int(CDATA))
    if DIAL:
        r0 = sec_start("retrain")
        ev["carrier"] = [e for e in ev["carrier"] if not (r0 <= e[0] < r0 + 2 * BAR and e[1] != 0)]
        dv = int(DIAL)
        for q, (lo, hi) in zip((0, 3, 6), ((697, 1209), (697, 1209), (697, 1336))):
            add("dtlo", r0 + q, f"{lo}hz", 2, dv)
            add("dthi", r0 + q, f"{hi}hz", 2, dv)
        add("dtlo", r0 + BAR, "440hz", 8, dv - 8)
        add("dthi", r0 + BAR, "480hz", 8, dv - 8)
    if CBREAK:
        c0 = sec_start("C")
        bs, bl = (int(x) for x in CBREAK.split(","))
        u, w = c0 + bs * BAR, c0 + (bs + bl) * BAR
        for k in ("kick", "hats", "clap"):
            ev[k] = [e for e in ev[k] if not (u <= e[0] < w and e[1] != 0)]
    if OUTSTAY:
        c0, o0 = sec_start("C"), sec_start("outro")
        n = int(OUTSTAY)
        for k in ("gtr", "acid"):
            add_ = []
            for e in ev[k]:
                if e[1] != 0 and c0 + 34 * BAR <= e[0] < c0 + (34 + n) * BAR:
                    b = (e[0] - c0 - 34 * BAR) // BAR
                    add_.append((e[0] - c0 - 34 * BAR + o0, e[1], e[2], e[3], max(1, int(e[4] * (1 - b / (n + 1))))) + tuple(e[5:]))
            ev[k] = sorted(ev[k] + add_, key=lambda x: x[0])
    for _kspec in ([("C", KEYUP)] if KEYUP else []) + ([("A", f"26,{AKEY}")] if AKEY else []):
        import re as _rk
        kb, ks = (int(x) for x in _kspec[1].split(","))
        c0 = sec_start(_kspec[0])
        u, w = c0 + kb * BAR, (sec_start("outro") if _kspec[0] == "C" else sec_start("B"))
        isn = _rk.compile(r"^([A-G](#|b)?-?\d)(,[A-G](#|b)?-?\d)*$")
        for k in ("gtr", "acid", "sub", "fretless", "horns", "lead", "keys"):
            if k not in ev:
                continue
            out = []
            for e in ev[k]:
                a, pri, h, ln, v = e[0], e[1], e[2], e[3], e[4]
                if pri != 0 and isinstance(h, str) and isn.match(h):
                    if u <= a < w:
                        e = (a, pri, transpose(h, ks), ln, v) + tuple(e[5:])
                    elif a < u < a + ln:
                        e = (a, pri, h, u - a, v) + tuple(e[5:])
                out.append(e)
            ev[k] = out
    if PERCSPLIT:
        mp = {"o": "t", "lo": "b", "sl": "s", "mu": "c", "bh": "s", "bl": "t"}
        spans = [(sec_start(x), sec_start(x) + dict(FORM)[x] * BAR) for x in PERCSPLIT.split(",")]
        inside = lambda a: any(u <= a < v for u, v in spans)
        ev["dj"] = [(e[0], e[1], mp.get(e[2], e[2]), e[3], e[4]) for e in ev["conga"] if inside(e[0]) and e[1] != 0]
        ev["conga"] = [(e[0], e[1], e[2], e[3], 1 if inside(e[0]) and e[1] != 0 else e[4]) for e in ev["conga"]]
    if HEMIOLA:
        h0_ = sec_start("B"); h1_ = h0_ + int(HEMIOLA) * BAR
        ev["hats"] = [e for e in ev["hats"] if not (h0_ <= e[0] < h1_)]
        for i_, a_ in enumerate(range(h0_, h1_, 3)):
            ev["hats"].append((a_, 1, "h", 1, 84 if i_ % 4 == 0 else 60))
        ev["hats"].sort(key=lambda e: e[0])
        if os.environ.get("C8T5_HEMCOW", "1") and "cow" in ev:
            ch_ = next((e[2] for e in ev["cow"]), None)
            if ch_ is not None:
                ev["cow"] = [e for e in ev["cow"] if not (h0_ <= e[0] < h1_)]
                for i_, a_ in enumerate(range(h0_, h1_, 3)):
                    if i_ % 2 == 0:
                        ev["cow"].append((a_, 1, ch_, 1, 92 if i_ % 4 == 0 else 66))
                ev["cow"].sort(key=lambda e: e[0])
    if SUBPATCH and SUBSPLIT:
        a0 = sec_start("A")
        ev["sub2"] = [e for e in ev["sub"] if e[0] >= a0]
        ev["sub"] = [e for e in ev["sub"] if e[0] < a0]
        return {k: stream(ev[k], total()) for k in (*TRACKS, "sub2")}
    return {k: stream(ev[k], total()) for k in TRACKS}


def stream(events, tot):
    events.sort(key=lambda e: (e[0], e[1]))
    out, t = [], 0
    for at, pri, head, ln, vel in events:
        if pri == 0:   # a latched setting at this point
            if at > t:
                out.append(f"R/{(at - t) / 4:g}b")
                t = at
            out.append(head)
            continue
        if at < t:
            continue
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        out.append(f"{head}/{ln / 4:g}b@{int(vel)}")
        t = at + ln
    if t < tot:
        out.append(f"R/{(tot - t) / 4:g}b")
    return " ".join(out)


def hook_tokens(semis):
    """The hook as score tokens (dotted eighths, quarters, dotted quarters), transposed."""
    lens = {3: "/8.", 4: "/4", 6: "/4."}
    return " ".join(transpose(n, semis) + lens[ln] for _, n, ln in HOOKF)


def markov_lead(name, at16, semis, n):
    """A gen-only lead: the engine's Markov chain over the hook, from `at16` (sixteenths, tempo-map aware as beats)."""
    return {"name": name, "patch": ({"about": "a Rossler flutter lead", "synth": {"layers": [{"type": "chaos", "chaos": {"system": "rossler", "axis": "x", "amount": {"value": 0.7, "mod": [{"src": "lfo.wander", "amount": 0.25}]}}}], "amp": "30ms 0.75 0.8 400ms"}} if CHLEAD else "lead-wah"),
            "gain": f"{CHLEAD}dB" if CHLEAD else "-12dB", "pan": 0.1, "at": f"{at16 / 4:g}b", "seed": 50 + semis, **({"lfo": {"wander": "sine rate=1/3"}} if CHLEAD else {}),
            "fx": [{"type": "chorus", "rate": 0.5, "depth": 0.4, "mix": 0.3}, *(["delay time=3/8 feedback=0.3 mix=0.2"] if CHLEAD else [])],
            "score": "swing16=0.58 vel=0.72", "gen": {"type": "markov", "order": 1, "from": hook_tokens(semis), "n": n}}


def lifted(tr):
    """The same voice a whole step up (its pitch fx, formant kept on its lane)."""
    tr["fx"] = [dict(f, semitones=2) if isinstance(f, dict) and f.get("type") == "pitch" else f for f in tr["fx"]]
    return tr


def rmix_lane(offs16):
    pts = [["0b", 0]]
    for o in offs16:
        pts += [[f"{(o - BAR) / 4:g}b", 0], [f"{o / 4:g}b", 1], [f"{(o + 3 * BAR) / 4:g}b", 1], [f"{(o + 3 * BAR + 4) / 4:g}b", 0]]
    return {"points": pts}


DORIAN = (4, 6, 7, 9, 11, 1, 2)   # E dorian pitch classes


DORIAN_NOTES = [m for m in range(24, 109) if m % 12 in DORIAN]


def dia(m, steps):
    """MIDI note m moved `steps` scale degrees in E dorian (m must be in the mode)."""
    return DORIAN_NOTES[DORIAN_NOTES.index(m) + steps]


def sung_choir(off16, lift):
    """The sung 'keep it there' (m-notes) as three voices: the lead, a diatonic third above, a third below."""
    src = json.load(open(os.path.join(HERE, "chirpers8-t5-sung.json")))["tracks"][0]
    out = []
    for name, steps, gain, pan, lag in (("choir", 0, float(VOX) + 1, 0.0, 0.0), ("choirhi", 2, float(VOX) - 3, 0.35, 0.012), ("choirlo", -2, float(VOX) - 3, -0.35, 0.02)):
        notes = []
        for n in src["notes"]:
            m = int(n["pitch"][1:])
            notes.append(dict(n, at=round(n["at"] + off16 / 4 + lag, 4), pitch=f"m{dia(m, steps) + (2 if lift else 0)}"))
        b = off16 / 4
        frz = ([{"type": "cloud", "size": "120ms", "density": 16, "position": "250ms", "spray": "120ms", "spread": 0.7, "seed": 3,
                 "freeze": {"value": 0, "mod": [{"src": "auto.kf", "amount": 1}]},
                 "mix": {"value": 0, "mod": [{"src": "auto.km", "amount": float(KEEPFREEZE)}]}}] if KEEPFREEZE else [])
        out.append({"name": name, "patch": src.get("patch", "voice-speech"), "gain": f"{gain:g}dB", "pan": pan,
                    **({"auto": {"kf": {"points": [["0b", 0], [f"{b + 7.8:g}b", 0], [f"{b + 7.85:g}b", 1], [f"{b + 18:g}b", 1], [f"{b + 18.05:g}b", 0]]},
                                 "km": {"points": [["0b", 0], [f"{b + 7.2:g}b", 0], [f"{b + 7.8:g}b", 1], [f"{b + 15.6:g}b", 1], [f"{b + 17.6:g}b", 0]]}}}
                       if KEEPFREEZE else {}),
                    "fx": [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150", *frz],
                    "sends": {"room": "-10dB", "spring": "-16dB"}, "notes": notes})
    return out


def voice(file, name, offs16, gain, fx, sends):
    """A humanized tts line (tts --print), placed at each offset (sixteenths), on one track."""
    src = json.load(open(os.path.join(HERE, file)))["tracks"][0]
    notes, fv = [], []
    for o16 in offs16:
        off = o16 / 4
        notes += [dict(n, at=round(n["at"] + off, 4)) for n in src["notes"] if not (KEEP3 and name == "keep" and 4 <= n["at"] < 8)]
        fv += [[f"{float(t[:-1]) + off:.3f}b", v] for t, v in src["auto"]["fv"]["points"]]
    auto = {"fv": {"points": fv}}
    if name == "bargain":
        auto["rmix"] = rmix_lane(offs16)
    return {"name": name, "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": 0.05,
            "fx": [*src["fx"], *fx], "auto": auto, "sends": sends, "notes": notes}


def beats(t16):
    return f"{t16 / 4:g}b"


def song():
    doc = song0()
    if PHASE:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]   # its own radio without a second hiss and whistle, which would run the whole song
        doc["tracks"].append(dict(spec, name="phase", pan=0.45, fx=fx, score=T["phase"]))
    if ESTABLE:
        doc["event_stable"] = True
    if PHASEA:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        doc["tracks"].append(dict(spec, name="phaseA", pan=0.45, fx=fx, gain=os.environ.get("C8T5_PHASEAGAIN", "-16dB"), score=T["phaseA"]))
    if PHASEIN:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        doc["tracks"].append(dict(spec, name="phase0", pan=0.45, fx=fx, score=T["phase0"]))
    if PERCSPLIT:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "conga")
        doc["tracks"].append(dict(spec, name="dj", patch="djembe", score=T["dj"]))
    if DIAL:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        for nm, pn in (("dtlo", -0.1), ("dthi", 0.1)):
            doc["tracks"].append(dict(spec, name=nm, pan=pn, fx=fx, gain="-16dB", score=T[nm]))
    if TRAIN:
        T = build()
        spec = next(t for t in doc["tracks"] if t["name"] == "carrier")
        fx = [dict(f, hiss="-80dB", whistle="-80dB") if isinstance(f, dict) and f.get("type") == "radio" else f for f in spec.get("fx", [])]
        doc["tracks"].append(dict(spec, name="train", patch={"synth": {"layers": [{"type": "bytebeat", "bytebeat": {"formula": TRAINF, "clock": 8000}}]}},
                                  gain=os.environ.get("C8T5_TRAINGAIN", "-20dB"), pan=0.0, fx=fx, score=T["train"]))
    if WIDTHAGREE:
        st = {sec: sec_start(sec) for sec, _ in FORM}
        lo, hi = (float(x) for x in WIDTHAGREE.split(","))
        mw = {"points": [[f"{x / 4:g}b", y] for x, y in ((0, 1), (st["B"], 1), (st["retrain"], 0.55), (st["C"], 0.3), (st["C"] + 8 * BAR, 0), (st["outro"], 0), (total(), 0.8))]}
        doc["master"]["auto"] = dict(doc["master"].get("auto", {}), mw=mw)
        doc["master"]["fx"] = list(doc["master"]["fx"]) + [{"type": "width", "width": {"value": lo, "mod": [{"src": "auto.mw", "amount": hi - lo}]}}]
    if RTSPIRAL:
        st = {sec: sec_start(sec) for sec, _ in FORM}
        r0, c0 = st["retrain"], st["C"]
        rt = {"points": [[f"{x / 4:g}b", y] for x, y in ((0, 0), (r0 - 8, 0), (r0 + 8, 1), (c0 - BAR, 1), (c0, 0), (total(), 0))]}
        rr = {"points": [[f"{x / 4:g}b", y] for x, y in ((0, 1), (r0, 1), (c0, 0), (total(), 0))]}
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "carrier":
                t_["auto"] = dict(t_.get("auto", {}), rt=rt, rr=rr)
                t_["fx"] = list(t_.get("fx", [])) + [{"type": "orbit", "rate": "1/2", "radius": {"value": 1, "mod": [{"src": "auto.rr", "amount": 11}]},
                                                      "speed": {"value": 2, "mod": [{"src": "auto.rr", "amount": -1.5}]}, "doppler": 0.6,
                                                      "mix": {"value": 0, "mod": [{"src": "auto.rt", "amount": float(RTSPIRAL)}]}}]
    if ACIDX:
        st = {sec: sec_start(sec) for sec, _ in FORM}

        def bt(x):
            return f"{x / 4:g}b"
        cx = {"points": [[bt(x), y] for x, y in ((0, 0.9), (st["A"] + 20 * BAR, 0.9), (st["B"], 0.75), (st["retrain"], 0.45), (st["retrain"] + 8 * BAR, 0.3),
                                                 (st["C"], 0),
                                                 *(((st["C"] + 30 * BAR + 8, 0), (st["C"] + 31 * BAR, float(CSPIKE)), (st["C"] + 32 * BAR, float(CSPIKE)), (st["C"] + 34 * BAR, 0)) if CSPIKE else ()),
                                                 (st["outro"] + 4 * BAR, 0), (total(), 0.7))]}
        cg = {"points": [[bt(x), y] for x, y in ((0, 0), (st["C"] + 30 * BAR + 8, 0), (st["C"] + 31 * BAR, 1), (st["C"] + 32 * BAR, 1), (st["C"] + 34 * BAR, 0), (total(), 0))]}
        spdb = float(os.environ.get("C8T5_CSPIKEDB", "14")) if CSPIKE else 0
        doc["tracks"].append({"name": "acidx", "gain": f"{ACIDX}dB", "pan": -0.15, "auto": {"cx": cx, **({"cg": cg} if spdb else {})},
                              "patch": {"synth": {"layers": [{"type": "chaos", "chaos": {"system": "rossler", "axis": "x", "amount": {"value": 0, "mod": [{"src": "auto.cx", "amount": 1}]}}}],
                                                  "amp": "4ms 0.8 0.5 120ms", "filters": [{"kind": "lp", "cutoff": 2400}]}},
                              "fx": [{"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "2ms", "release": "160ms", "curve": 0.7},
                                     *([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.cg", "amount": spdb}]}}] if spdb else [])], "score": T["acid"]})
    if ACIDWARP:
        wv = float(ACIDWARP)
        fl = dict(FORM)
        warp = [{"over": f"{fl['intro']}bar", "to": 0}, {"over": f"{fl['A']}bar", "to": wv, "curve": "smooth"},
                {"over": f"{fl['B']}bar", "to": -wv / 2, "curve": "smooth"}, {"over": f"{fl['retrain']}bar", "to": 0, "curve": "smooth"},
                {"over": f"{fl['C']}bar", "to": 0}, {"over": f"{fl['outro']}bar", "to": wv / 2, "curve": "smooth"}]
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "acid":   # the acid alone: its chaos double (v45) stays on the band's clock, the grid the acid wanders around
                t_["warp"] = warp
    if KEEPLPC:
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "keep":
                t_["fx"] = [{"plain": "lpc", "toy": "lpc pitch=E3 bits=5"}[KEEPLPC], *t_.get("fx", [])]
                for n in t_.get("notes", []):
                    n["at"] = round(max(0.0, n["at"] - (0.07 if LPCNUDGE else 0)), 4)
                if KEEPACK:
                    ack = json.loads(json.dumps(t_))
                    ack["name"] = "keep-ack"
                    ack["fx"] = ["lpc pitch=E3 bits=5", *t_.get("fx", [])[1:]]
                    ack["gain"] = f"{float(str(t_['gain']).replace('dB', '')) + float(KEEPACK):g}dB"
                    ack["pan"] = -0.3
                    ack["notes"] = [dict(n, at=round(n["at"] + 4, 4)) for n in t_.get("notes", [])]
                    doc["tracks"].append(ack)
    if GTRRUSH:
        fl = dict(FORM)
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "gtr":
                t_["warp"] = [{"over": f"{fl['intro'] - 1}bar", "to": 0}, {"over": "1bar", "to": -float(GTRRUSH), "curve": "smooth"},
                              {"over": "8bar", "to": 0, "curve": "smooth"}]
    if ROBOCHOIR:
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") == "choir":
                twin = json.loads(json.dumps(t_))
                twin.update(name="choir-robo", gain=f"{ROBOCHOIR}dB", pan=-0.2)
                twin["fx"] = [*t_.get("fx", []), {"type": "vocoder", "notes": "E2,B2,E3,G3", "bands": 20, "noise": 0.12, "attack": "4ms", "release": "70ms"}]
                doc["tracks"].append(twin)
    if OUTKS:
        kb, kg = OUTKS.split(":")
        o0 = sec_start("outro") / 4
        notes = []
        for r in range(5):
            top = "B4" if r == 4 else "E4"
            v = round(0.8 - 0.08 * r, 2)
            notes += [{"at": o0 + 8 * r, "pitch": "B3", "len": 1.5, "vel": v}, {"at": o0 + 8 * r + 1.5, "pitch": "D4", "len": 1.5, "vel": v}, {"at": o0 + 8 * r + 3, "pitch": top, "len": 3, "vel": v}]
        notes = [n for n in notes if n["at"] < o0 + 48] + [{"at": o0 + 48, "pitch": "E4", "len": 8, "vel": 0.36}]
        doc["tracks"].append({"name": "outks", "gain": f"{kg}dB", "pan": 0.2,
                              "patch": {"about": "Karplus-Strong 1983, stretched", "synth": {"layers": [{"type": "ks", "ks": {"blend": float(kb), "stretch": 4, "tune": True}}], "amp": "1ms 1 1 1.5s"}},
                              "notes": notes})
    if CONGALAYER:
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") == "conga" and t_.get("patch") == "congas":
                hits = {"bh": "F4", "bl": "C4", "lo": "D3", "mu": "G3", "o": "A3", "sl": "C4"}
                tw = json.loads(json.dumps(t_))
                tw.update(name="congaks", gain=f"{CONGALAYER}dB",
                          patch={"about": "Karplus-Strong's drum (1983): blend 0.5", "synth": {"layers": [{"type": "ks", "bright": 0.45, "ks": {"blend": 0.5, "stretch": 1, "tune": True}}], "amp": "1ms 1 0 160ms"}})
                tw["score"] = " ".join(hits.get(tok.split("/")[0], tok.split("/")[0]) + tok[len(tok.split("/")[0]):] for tok in t_["score"].split())
                doc["tracks"].append(tw)
    if TAPE:
        r0 = sec_start("retrain")
        pts = [(0, 0), (r0 - BAR, 0), (r0 - BAR + 1, 1), (r0 - 1, 1), (r0, 0)]
        if "outro" in TAPE:
            o0 = sec_start("outro")
            pts += [(o0 - BAR, 0), (o0 - BAR + 1, 1), (o0 - 1, 1), (o0, 0)]
        if "end" in TAPE:
            e0 = total() - 2 * BAR
            pts += [(e0, 0), (e0 + 1, 1)]
        pts += [(total(), pts[-1][1])]
        doc["master"]["auto"] = dict(doc["master"].get("auto", {}), ts={"points": [[f"{x / 4:g}b", y] for x, y in pts]})
        doc["master"]["fx"] = list(doc["master"]["fx"]) + [{"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}, "time": "4b", "up": "2b", "curve": 1.6}]
    if DJLAYER:
        for t_ in list(doc["tracks"]):
            if isinstance(t_, dict) and t_.get("name") == "dj" and t_.get("patch") == "djembe":
                hits = {"b": "C3", "c": "G2", "s": "B4", "t": "E4"}
                tw = json.loads(json.dumps(t_))
                tw.update(name="djks", gain=f"{DJLAYER}dB",
                          patch={"about": "Karplus-Strong's drum (1983): blend 0.5", "synth": {"layers": [{"type": "ks", "bright": 0.45, "ks": {"blend": 0.5, "stretch": 1, "tune": True}}], "amp": "1ms 1 0 160ms"}})
                tw["score"] = " ".join(hits.get(tok.split("/")[0], tok.split("/")[0]) + tok[len(tok.split("/")[0]):] for tok in t_["score"].split())
                doc["tracks"].append(tw)
    if SCANC:
        c0 = sec_start("C") / 4
        doc["tracks"].append({"name": "scanc", "gain": f"{SCANC}dB", "pan": 0.0,
                              "patch": {"about": "scanned synthesis (Mathews 2000): a ring of masses and springs", "synth": {"layers": [{"type": "scanned", "scanned": {"speed": 0.4, "width": 0.5, "smooth": 0.45, "push": ({"value": float(SCANCOPEN), "mod": [{"src": "auto.sgrip", "amount": float(SCANCPUSH) - float(SCANCOPEN)}]} if SCANCOPEN else float(SCANCPUSH))}, "decay": "6s"}], "amp": "1.2s 0.9 0.85 3s"}},
                              "fx": ["chorus mix=0.2"],
                              **({"auto": {"sgrip": {"points": [["0b", 0], [f"{c0:g}b", 0], [f"{c0 + 30:g}b", 1], [f"{total() / 4:g}b", 1]]}}} if SCANCOPEN else {}),
                              "notes": [{"at": c0, "pitch": p_, "len": 32, "vel": 0.7} for p_ in ("E3", "G3", "B3", "D4")]})
    if HAGGLE:
        b0 = sec_start("B") / 4
        notes = []
        for i, bar in enumerate(range(4, 16, 2)):
            hi, lo = round(0.95 - 0.05 * i, 2), round(0.35 + 0.05 * i, 2)
            t0 = b0 + bar * BAR / 4
            notes += [{"at": t0, "pitch": "E4", "len": 1.0, "vel": hi}, {"at": t0 + 1.5, "pitch": "B3", "len": 1.5, "vel": hi},
                      {"at": t0 + 4, "pitch": "D4", "len": 1.0, "vel": lo}, {"at": t0 + 5.5, "pitch": "A3", "len": 1.5, "vel": lo}]
        doc["tracks"].append({"name": "haggle", "gain": f"{HAGGLE}dB", "pan": 0.25,
                              "patch": {"about": "Chebyshev brass (1979): louder is brighter", "synth": {"layers": [{"type": "shaper", "shaper": {"harmonics": [1, 0.8, 0.6, 0.45, 0.35, 0.25, 0.18, 0.12], "index": {"value": 0.05, "mod": [{"src": "env.blow", "amount": 0.4}, {"src": "vel", "amount": 0.55}]}}}],
                                        "amp": "40ms 200ms 0.8 150ms", "env": {"blow": {"a": "60ms", "d": "300ms", "s": 0.7, "r": "150ms"}}}},
                              "fx": ["delay time=3/8 mix=0.15 feedback=0.3"], "notes": notes})
    if CHOIRVOICE:
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") in ("choir", "choirhi", "choirlo") and isinstance(t_.get("patch"), dict):
                t_["patch"] = dict(t_["patch"], extends="voice")
    if CHANTARC:
        ch_ = next((t_ for t_ in doc["tracks"] if isinstance(t_, dict) and t_.get("name") == "choir"), None)
        cn_ = (ch_ or {}).get("notes") or []
        ca_, cz_ = (min(n["at"] for n in cn_), max(n["at"] + n["len"] for n in cn_)) if cn_ else (sec_start("outro") / 4 - 16, sec_start("outro") / 4)
        aa_, ra_ = sec_start("B") / 4 - BAR, sec_start("C") / 4 - BAR
        spans = ((aa_, aa_ + BAR - 0.5, 0.55), (ra_, ra_ + BAR - 0.5, 0.7), (ca_ - 1, cz_ + 0.5, 0.85))
        mouth = [["0b", 0], [f"{ra_ - 1:g}b", 0], [f"{ra_:g}b", 0.45], [f"{ca_ - 2:g}b", 0.45], [f"{ca_ - 1:g}b", 1], [f"{total() / 4:g}b", 1]]
        for nm, vc, vib, p_ in (() if os.environ.get("C8T5_NOCHOIR") or AGREEDUO else (("chant-b", "bass", 0.1, 40), ("chant-t", "tenor", 0.15, 47), ("chant-a", "alto", 0.2, 55), ("chant-s", "soprano", 0.3, 62))):
            doc["tracks"].append({"name": nm, "gain": f"{CHANTARC}dB", "pan": {"bass": 0, "tenor": -0.3, "alto": 0.3, "soprano": -0.1}[vc],
                                  "sends": dict((ch_ or {}).get("sends", {})),
                                  "auto": {"mouth": {"points": mouth}},
                                  "patch": {"about": "CHANT (Rodet, IRCAM 1979-84): FOF singing, " + vc,
                                            "synth": {"layers": [{"type": "fof", "fof": {"voice": vc, "vowel": "u>a", "attack": "3ms", "morph": {"value": 0, "mod": [{"src": "auto.mouth", "amount": 1}]}}}],
                                                      "pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": vib}, {"src": "env.scoop", "amount": -0.3}]},
                                                      "lfo": {"vib": {"wave": "sine", "rate": "5.5hz", "delay": "300ms", "fade": "400ms"}},
                                                      "env": {"scoop": {"a": "1ms", "d": "120ms", "s": 0}}, "amp": "600ms 0 1 1.2s"}},
                                  "notes": [{"at": round(a, 3), "pitch": f"m{p_}", "len": round(z - a, 3), "vel": v} for a, z, v in spans if not (DUOVIB and a == ra_)]})
        if DUOVIB:
            for nm, vc, rate, p_, pan in (("chant-m1", "tenor", "4.2hz", 52, -0.45), ("chant-m2", "alto", "6.8hz", 59, 0.45)):
                doc["tracks"].append({"name": nm, "gain": f"{DUOVIB}dB", "pan": pan, "sends": dict((ch_ or {}).get("sends", {})),
                                      "auto": {"mouth": {"points": mouth}},
                                      "patch": {"about": "CHANT (FOF), one of two machines: its own vibrato speed",
                                                "synth": {"layers": [{"type": "fof", "fof": {"voice": vc, "vowel": "u>a", "attack": "3ms", "morph": {"value": 0, "mod": [{"src": "auto.mouth", "amount": 1}]}}}],
                                                          "pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 0.35}]},
                                                          "lfo": {"vib": {"wave": "sine", "rate": rate, "delay": "200ms", "fade": "600ms"}}, "amp": "600ms 0 1 1.2s"}},
                                      "notes": [{"at": round(ra_, 3), "pitch": f"m{p_}", "len": round(BAR - 0.5, 3), "vel": 0.75}]})
        if AGREEDUO:
            for nm, vc, p_, pan in (("agree-m1", "tenor", 52, -0.3), ("agree-m2", "alto", 59, 0.3)):
                doc["tracks"].append({"name": nm, "gain": f"{AGREEDUO}dB", "pan": pan, "sends": dict((ch_ or {}).get("sends", {})),
                                      "auto": {"mouth": {"points": mouth}},
                                      "patch": {"about": "CHANT (FOF), the two machines agreed: one vibrato speed",
                                                "synth": {"layers": [{"type": "fof", "fof": {"voice": vc, "vowel": "u>a", "attack": "3ms", "morph": {"value": 0, "mod": [{"src": "auto.mouth", "amount": 1}]}}}],
                                                          "pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": 0.25}]},
                                                          "lfo": {"vib": {"wave": "sine", "rate": "5.5hz", "delay": "300ms", "fade": "500ms"}}, "amp": "600ms 0 1 1.2s"}},
                                      "notes": [{"at": round(ca_ - 1, 3), "pitch": f"m{p_}", "len": round(cz_ + 0.5 - (ca_ - 1), 3), "vel": 0.8}]})
    if LINEOPEN:
        a_, b_ = (float(v) for v in LINEOPEN.split(":"))
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "carrier":
                t_.setdefault("fx", []).append({"type": "filter", "kind": "lp", "q": 0.7, "cutoff": {"value": 20000, "mod": [{"src": "auto.lop", "amount": -3.5}]}})
                t_.setdefault("auto", {})["lop"] = {"points": [["0b", 1], [f"{a_:g}b", 1], [f"{b_:g}b", 0], [f"{total() / 4:g}b", 0]]}
    if ECHOCANCEL:
        lane_ = [["0b", 1], [f"{sec_start('B') / 4 - 4:g}b", 1], [f"{sec_start('B') / 4:g}b", 0.8], [f"{sec_start('retrain') / 4 - 4:g}b", 0.8],
                 [f"{sec_start('retrain') / 4:g}b", 0.3], [f"{sec_start('C') / 4 - 2:g}b", 0.3], [f"{sec_start('C') / 4:g}b", 0], [f"{total() / 4:g}b", 0]]
        doc.setdefault("buses", {})["lineecho"] = {"fx": [{"type": "delay", "time": "3/16", "feedback": 0.35, "mix": 1, "tone": 1800, "ping_pong": True},
                                                          "hp cutoff=250",
                                                          {"type": "gain", "gain": {"value": "-40dB", "mod": [{"src": "auto.cancel", "amount": 32}]}}],
                                                   "auto": {"cancel": {"points": lane_}}}
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") in ("gtr", "horns", "lead", "keys"):
                t_.setdefault("sends", {})["lineecho"] = f"{ECHOCANCEL}dB"
    if CONGAPHASE:
        fl_ = dict(FORM)
        ph_ = float(CONGAPHASE)
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "conga":
                t_["warp"] = [{"over": f"{fl_['intro']}bar", "to": 0}, {"over": f"{fl_['A']}bar", "to": ph_, "curve": "smooth"},
                              {"over": f"{fl_['B']}bar", "to": ph_ / 2, "curve": "smooth"}, {"over": f"{fl_['retrain']}bar", "to": 0, "curve": "smooth"},
                              {"over": f"{fl_['C'] + fl_['outro']}bar", "to": 0}]
    if SWARM:
        fl_ = dict(FORM)
        kt_ = next((t_ for t_ in doc["tracks"] if isinstance(t_, dict) and t_.get("name") == "keys"), None)
        if kt_ is not None:
            sw_ = json.loads(json.dumps(kt_))
            r0_ = (fl_["intro"] + fl_["A"] + fl_["B"]) * 4
            r1_ = r0_ + fl_["retrain"] * 4
            sw_.update(name="swarm", gain=f"{SWARM}dB", pan=0.3)
            sw_.pop("fx", None); sw_.pop("lfo", None); sw_.pop("warp", None)
            sw_["patch"] = {"synth": {"layers": [{"type": "kuramoto", "kuramoto": {"count": 12, "spread": 40, "wave": "saw",
                                      "coupling": {"value": 0.3, "mod": [{"src": "auto.agree", "amount": 2.7}]}}}],
                                      "filters": ["lp cutoff=3200"], "amp": "40ms 0.8 0.8 400ms"}}
            sw_["auto"] = {"agree": {"points": [["0b", 0], [f"{r0_}b", 0], [f"{r1_}b", 1], [f"{total() / 4:g}b", 1]]} if not LOCKSLOW else {"points": [["0b", 0], [f"{r0_}b", 0], [f"{r0_ + 4}b", 0.26], [f"{r1_ + 64}b", 0.63], [f"{r1_ + 112}b", 1], [f"{total() / 4:g}b", 1]]}}
            doc["tracks"].append(sw_)
    if SWARMGTR:
        fl_ = dict(FORM)
        gt_ = next((t_ for t_ in doc["tracks"] if isinstance(t_, dict) and t_.get("name") == "gtr"), None)
        if gt_ is not None:
            sg_ = json.loads(json.dumps(gt_))
            r0_ = (fl_["intro"] + fl_["A"] + fl_["B"]) * 4
            r1_ = r0_ + fl_["retrain"] * 4
            sg_.update(name="swarm-gtr", gain=f"{SWARMGTR}dB", pan=-0.3)
            for k_ in ("fx", "lfo", "warp", "auto"):
                sg_.pop(k_, None)
            sg_["patch"] = {"synth": {"layers": [{"type": "kuramoto", "kuramoto": {"count": 10, "spread": 45, "wave": "saw",
                                      "coupling": {"value": 0.3, "mod": [{"src": "auto.agree", "amount": 2.7}]}}}],
                                      "filters": ["lp cutoff=2600"], "amp": "15ms 0.7 0.6 250ms"}}
            sg_["auto"] = {"agree": {"points": [["0b", 0], [f"{r0_}b", 0], [f"{r1_}b", 1], [f"{total() / 4:g}b", 1]]} if not LOCKSLOW else {"points": [["0b", 0], [f"{r0_}b", 0], [f"{r0_ + 4}b", 0.26], [f"{r1_ + 64}b", 0.63], [f"{r1_ + 112}b", 1], [f"{total() / 4:g}b", 1]]}}
            doc["tracks"].append(sg_)
    if ACKTONE:
        for t_ in doc["tracks"]:
            if isinstance(t_, dict) and t_.get("name") == "keep-ack":
                fx_ = t_.get("fx", [])
                fx_ = list(fx_) if isinstance(fx_, list) else [fx_]
                fx_.insert(0, {"type": "waveset", "mode": ACKTONE, "max": "20ms"})
                t_["fx"] = fx_
    return doc


def song0():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    BARG = [st["B"] + 12 * BAR, st["retrain"] + 3 * BAR, st["retrain"] + 8 * BAR]
    meet_lane = {"points": [[f"{x / 4:g}b", y] for x, y in ((0, 1), (st["B"], 1), (st["retrain"], 0.55), (st["C"], 0.3), (st["C"] + 8 * BAR, 0), (st["outro"], 0), (total(), 0.8))]}
    merge_lane = {"points": [["0b", 0], [f"{st['C'] / 4:g}b", 0], [f"{(st['C'] + 8 * BAR) / 4:g}b", 1], [f"{(st['outro'] - BAR) / 4:g}b", 1],
                             [f"{st['outro'] / 4:g}b", 0], [f"{total() / 4:g}b", 0]]}
    end = total()
    tempo = [{"at": "0b", "bpm": 106}, {"at": beats(st["A"]), "bpm": 108}, {"at": beats(st["B"]), "bpm": 108},
             {"at": beats(st["retrain"]), "bpm": 114, "ramp": True}, {"at": beats(st["retrain"]), "bpm": 110},
             {"at": beats(st["C"]), "bpm": 112},
             *(([{"at": beats(st["C"] + 16 * BAR), "bpm": 112}, {"at": beats(st["C"] + 18 * BAR), "bpm": float(FFWD.split(",")[0]), "ramp": True}] if FFWD.endswith("ramp") else
                [{"at": beats(st["C"] + 16 * BAR), "bpm": float(FFWD)}]) + [{"at": beats(st["C"] + 24 * BAR), "bpm": 112}] if FFWD else []),
             {"at": beats(st["outro"]), "bpm": 112}, {"at": beats(end), "bpm": 100, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "2ms", "release": "160ms", "curve": 0.7}
    spb = 60 / 110

    def lane(points):
        if LANEBEATS:
            return {"points": [[f"{t / 4:g}b", v] for t, v in points]}
        return {"points": [[f"{t / 4 * spb:.3f}s", v] for t, v in points]}

    dpts = [(0, float(RADIOSTART) if RADIOSTART else 0.9), (st["intro"] + 8 * BAR, 0.05), (st["A"], 0.05), (st["retrain"], 0.6), (st["retrain"] + 6 * BAR, 0.05),
            (st["C"], 0.05), (st["outro"] + 8 * BAR, 0.05), (end, 1)]
    if "dial" in LANEBEATS:
        dpts += [(st["B"] - 4, 0.05), (st["B"], 0.45), (st["B"] + 2 * BAR, 0.05), (st["C"] + 16 * BAR - 4, 0.05), (st["C"] + 16 * BAR, 0.5), (st["C"] + 18 * BAR, 0.05)]
        dpts.sort()
    dial = lane(dpts)
    return {
        "about": "chirpers VIII, track 5 by chirper-zero: machine funk - two machines agreeing on a speed. "
                 "Generated by compose/chirpers8/src/chirpers8-t5.py.",
        **({"vars": {**({"storm": {"system": {"type": "lorenz", "axis": "x", "dt": 0.01, "stride": 6, "n": 1400, "range": [0, float(STORM)], "skip": 50},
                                "every": "1/8"}} if STORM else {}),
                     **({"agree": {"system": {"type": "logistic", "r": 2.95, "x0": 0.45, "n": 200, "range": [float(AGREE), AGREEHI]},
                                   "every": "2/1", "smooth": "300ms"}} if AGREE else {})}} if (STORM or AGREE) else {}),
        "tempo": tempo, "ceiling": "-1dB", "loudness": -11, "seed": SEED, "tail": "2s",
        "patches": {"carrier": {"about": "a carrier tone: a plain sine with a soft edge", "synth": {"layers": ["sine"], "amp": {"a": "4ms", "s": 1, "r": "30ms"}}},
                    **({"acid-agree": {"about": "the acid with its resonance on the logistic var 'agree'", "extends": "acid",
                                       "synth": {"filters": [{"kind": "lp", "slope": 24, "q": {"value": 7, "mod": [{"src": "var.agree", "amount": 1}]},
                                                              "cutoff": {"value": 260, "mod": [{"src": "env.f", "amount": 4.2}, {"src": "vel", "amount": 2}]}}]}}} if AGREE else {})},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=250 q=0.8 gain=-2dB", "peak cutoff=1600 q=0.7 gain=-3dB", "highshelf cutoff=7000 gain=1.5dB"]},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2.5, "attack": "12ms", "release": "140ms", "makeup": "0dB"}]},
        "buses": {
            "room": {"fx": ["reverb kind=room decay=1.1s mix=1 predelay=10ms", "hp cutoff=250"]},
            "spring": {"fx": ["reverb kind=spring decay=2.2s mix=1", "hp cutoff=300"]},
        },
        "tracks": [
            {"name": "carrier", "patch": "carrier", "gain": "-22dB",
             "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}]}, "hiss": "-36dB", "whistle": "-28dB",
                     "fade": 0.3, "drift": 0.05, "mix": {"value": 1, "mod": [{"src": "auto.cmix", "amount": -1}]} if HEADMIX else 1}],
             "auto": {"dial": dial, **({"cmix": lane([(0, 1 - float(HEADMIX)), (4 * BAR, 0), (end, 0)])} if HEADMIX else {})}, "score": T["carrier"]},
            {"name": "conga", "patch": "congas", "gain": "-8dB", "pan": -0.25, "sends": {"room": "-12dB"}, "score": T["conga"],
             **({"fx": [{"type": "filter", "kind": "hp", "q": 0.7, "cutoff": {"value": 20, "mod": [{"src": "auto.cth", "amount": math.log2(float(CONGATHIN) / 20)}]}}],
                 "auto": {"cth": lane([(0, 0), (end - 4 * BAR, 0), (end - BAR, 1), (end, 1)])}} if CONGATHIN else {})},
            {"name": "gtr", "patch": "cutting-guitar", "gain": "-9dB", "pan": {"value": 0.1, "mod": [{"src": "auto.pm", "amount": float(PANMEET)}]} if PANMEET else 0.3,
             **({"auto": {**({"mg": merge_lane} if MERGE else {}), **({"pm": meet_lane} if PANMEET else {}),
                          **({"wh": lane([(0, 0), (st["C"] + 24 * BAR, 0), (st["C"] + 25 * BAR, 1), (st["outro"], 1), (st["outro"] + 2 * BAR, 0), (end, 0)])} if LIFTWAH else {})}}
                if (MERGE or LIFTWAH) else {}),
             "fx": [*([f"peak cutoff=1650 q=0.8 gain=-{SPEQ.split(',')[0]}dB"] if SPEQ and float(SPEQ.split(',')[0]) else []),
                    *([{"type": "morph", "key": "acid", "mode": "morph", "amount": {"value": 0, "mod": [{"src": "auto.mg", "amount": float(MERGE)}]}}] if MERGE else []),
                    *([{"type": "wah", "env": 1.0, "sens": "12dB", "q": 3.0, "low": 350, "high": 2200,
                        "mix": {"value": 0, "mod": [{"src": "auto.wh", "amount": float(LIFTWAH)}]}}] if LIFTWAH else []),
                    {"type": "phaser", "rate": 0.4, "depth": 0.6, "feedback": 0.4, "stages": 6, "mix": 0.35},
                    {"type": "amp", "gain": 0.25, "mix": 0.5}, {"type": "cab", "mix": 0.6}],
             "sends": {"spring": "-14dB"}, "score": T["gtr"]},
            {"name": "sub", "patch": "808" if SUBSPLIT else (SUBPATCH or "808"), "gain": "-10dB", "fx": [pump, {"type": "filter", "kind": "lp", "cutoff": 160, "q": 0.7}], "score": T["sub"]},
            *([{"name": "sub2", "patch": SUBPATCH, "gain": "-10dB", "fx": [pump, {"type": "filter", "kind": "lp", "cutoff": 160, "q": 0.7}], "score": T["sub2"]}] if SUBPATCH and SUBSPLIT else []),
            {"name": "acid", "patch": "acid-agree" if AGREE else "acid", "gain": "-10dB", "pan": {"value": -0.1, "mod": [{"src": "auto.pm", "amount": -float(PANMEET)}]} if PANMEET else -0.1,
             **({"auto": {"pm": meet_lane}} if PANMEET else {}),
             "fx": [pump, *([{"type": "filter", "kind": "ladder", "q": 0.45, "cutoff": {"value": 600, "mod": [{"src": "var.storm", "amount": 1}]}}] if STORM else [])],
             "score": T["acid"]},
            {"name": "kick", "patch": "909", "gain": "-3dB", "score": T["kick"]},
            {"name": "hats", "patch": "909", "gain": "-10dB", "pan": 0.15, "score": "swing16=0.58 " + T["hats"],
             **({"fx": [f"peak cutoff=9000 q=0.8 gain={SPEQ.split(',')[1]}dB"]} if SPEQ and float(SPEQ.split(',')[1]) else {})},
            {"name": "clap", "patch": "909", "gain": "-9dB", "sends": {"room": "-8dB"}, "score": T["clap"]},
            {"name": "fretless", "patch": "fretless", "gain": "-8dB", "fx": [{"type": "tremolo", "rate": 3.0, "depth": 0.4}], "sends": {"spring": "-10dB"}, "score": T["fretless"]},
            *([{"name": "cow", "patch": {"about": "a drum-machine cowbell from the engine's machine layer", "synth": {"layers": [{"type": "machine", "machine": {"part": "cowbell"}}]}},
                 "gain": "-17dB", "pan": 0.45, "sends": {"spring": "-16dB"}, "score": "swing16=0.58 " + T["cow"]}] if COW else []),
            *([{"name": "keys", "patch": ({"about": "a CZ phase-distortion keys: reso_tri, its resonance swept down in each note", "synth": {"layers": [{"type": "pd", "pd": {"shape": "reso_tri", "amount": {"value": float(os.environ.get("C8T5_PDBASE", "0.12")), "mod": [{"src": "env.cz", "amount": float(os.environ.get("C8T5_PDENV", "0.55"))}]}}}], "env": {"cz": "2ms 1 0 260ms"}, "amp": "3ms 0.8 0.45 280ms"}} if PDKEYS else "wurli"), "gain": f"{float(KEYS) + (float(PDKEYS) if PDKEYS else 0):g}dB", "pan": -0.35, "sends": {"spring": "-14dB"}, "score": "swing16=0.58 " + T["keys"]}] if KEYS else []),
            {"name": "horns", "patch": ({"vosim": {"about": "the agreed tune sung by VOSIM", "synth": {"layers": [{"type": "vosim", "vosim": {"formant": {"value": 650, "mod": [{"src": "lfo.jaw", "amount": 0.2}]}, "pulses": 3, "decay": 0.7}},
                                                                    {"type": "vosim", "level": 0.55, "vosim": {"formant": {"value": 1100, "mod": [{"src": "lfo.tongue", "amount": 0.25}]}, "pulses": 4, "decay": 0.75}}], "amp": "25ms 0.85 0.8 180ms"}},
                                         "czbrass": {"about": "CZ brass: a sine opening into a saw", "synth": {"layers": [{"type": "pd", "pd": {"shape": "saw", "amount": {"value": 0.15, "mod": [{"src": "env.br", "amount": 0.75}]}}}],
                                                     "env": {"br": "80ms 1 0.7 200ms"}, "amp": "30ms 0.85 0.75 160ms"}}}[HORNP] if HORNP else "horn-section"), "gain": "-9dB", "pan": -0.2,
             **({"lfo": {"jaw": "sine rate=1/2", "tongue": "tri rate=3/4"}} if HORNP == "vosim" else {}), "sends": {"room": "-8dB"}, "score": T["horns"]},
            *([voice("chirpers8-t5-bargain-touch.json" if BARGTAKE == "touch" else "chirpers8-t5-bargain.json", "bargain", BARG, f"{float(VOX) + float(BARGG or 0):g}dB",
                          [{"type": "radio", "tune": 0.04, "hiss": "-40dB", "whistle": "-32dB", "fade": 0.3, "drift": 0.03,
                            "mix": {"value": 0, "mod": [{"src": "auto.rmix", "amount": float(BARGMIX) if BARGMIX else 0.85}]}}, "hp cutoff=250"],
                          {"spring": "-12dB"})] if VOX else []),
            *([voice("chirpers8-t5-keep.json", "keep", [st["C"] + 16 * BAR] + ([] if MOD else [st["C"] + (CLEN - 8) * BAR]), f"{float(VOX) + 2:g}dB",
                     [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150"], {"room": "-10dB", "spring": "-16dB"})] if VOX else []),
            *([lifted(voice("chirpers8-t5-keep.json", "keep2", [st["C"] + (CLEN - 8) * BAR], f"{float(VOX) + 2:g}dB",
                            [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150"], {"room": "-10dB", "spring": "-16dB"}))] if VOX and MOD and not SUNGKEEP else []),
            *(sung_choir(st["C"] + (CLEN - 8) * BAR, bool(MOD)) if VOX and SUNGKEEP else []),
            *([markov_lead("lead-m1", st["C"] + 16 * BAR, 0, 30), markov_lead("lead-m2", st["C"] + 24 * BAR, 2, 56 - 4 * (48 - CLEN))] if MARK else []),
            {"name": "lead", "patch": "lead-wah", "gain": "-12dB", "pan": 0.1, "fx": [{"type": "chorus", "rate": 0.5, "depth": 0.4, "mix": 0.3}],
             "score": "swing16=0.58 " + T["lead"]},
        ],
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "vars", "tempo", "ceiling", "loudness", "seed", "tail", "event_stable", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
