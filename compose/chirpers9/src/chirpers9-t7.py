#!/usr/bin/env python3
"""chirpers9-t7 (Accretion, track 7: the innermost orbit). Composed by chirper-two.

MARGINALLY BOUND. The album's crest: everything colliding, fastest (132 -> 150), densest - the mirror of t3 (Phase
Margin) and beyond it. t6 hands over sitting on Eb, the tide's unresolved pull; t7 TAKES it: its storm is in Eb, a
semitone above home, with every element transformed there - E1 in a three-speed stretto (x1, x2 squeezed, x2
stretched), E2's seven on the snare's ghosts, E3's undertow squeezed x2 on a reese, E4's four lights in their storm
minor at half harmonic rhythm, E5's orbit squeezed into a trill, E6's tide squeezed to a one-beat pulse, and E7, this
track's element, THE JET: the Lydian collection as one column of fifths, D A E B F# C# G#, fired upward and
accelerating (2 2 2 1 1 1 2 sixteenths: 11). Every cycle is phased to land on bar 120's downbeat, where the semitone
pull resolves Eb -> D and the album crests: the jet fires every cycle and a choir sings "each lap a little shorter".
Then the plunge, and an outfall at 150 that stops on E1's unresolved E for t8 to lift.

Writes songs/chirpers9-t7.yaml (or T7_OUT). Original music.
"""
import json
import math
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("T7_OUT", os.path.join(ROOT, "songs", "chirpers9-t7.yaml"))

# round 2 (section, w9 = bars 128-144, the crest's middle): T7_R2=lock (default) - THE TIDAL LOCK: the break drops to
# half time for 8 bars while the jet fires BACKWARDS (falling: redshift) and a vocoder - its carrier the jet's own
# column of fifths - speaks "every corner comes sooner"; then the jet rights itself and a snare rush rebuilds into
# bar 144. T7_R2=none reproduces v1.
R2 = os.environ.get("T7_R2", "lock") != "none"
# round 3 (palette): T7_R3=column (default) - two swaps away from album staples. The jet's octave double: nes-pulse-lead
# (4 songs) -> a7-column, a WAVETABLE (unused on the album, no preset uses one) whose frames add the harmonics 1, 3, 9,
# 27, 81, 243 - each a fifth (and an octave) above the last - scanned upward on every note: the jet's column of fifths
# built inside one sound. The floor: sub (6 songs) -> a7-floor, a sine with its octave, a slow swell and a little drive,
# easing in from bar 17 (the in-seam had +29 dB at 38-44 Hz against t6's body). T7_R3=none reproduces v2.
R3 = os.environ.get("T7_R3", "column") != "none"
# round 4 (section, w7 = bars 97-112, the spiral, flagged static; presence.py found E4, the hats and the ghosts BURIED
# there, 27-34 dB under the mix, and the E1 bells and E5 22-25 dB under): T7_R4=spiral (default) - THE SPIRAL TIGHTENS.
# The bass and the tide step back and the elements come forward one by one, each in its own lane: E1's three bells at
# bar 97, E5's orbit an octave UP at 101, E4's lights at 105, the hats and E2's ghosts at 109 with 32nd rolls; and the
# tide squeezes from one beat to a half (105) and a quarter (109) - a tremolo between Eb and D. =none reproduces v3.
R4 = os.environ.get("T7_R4", "spiral") != "none"
W9 = (128, 144)

BARS, BPB = 176, 4
TOTAL = BARS * BPB
SECTIONS = [("infall", 0, 16), ("approach", 16, 48), ("collision", 48, 80), ("slack", 80, 88), ("spiral", 88, 120),
            ("crest", 120, 152), ("plunge", 152, 160), ("outfall", 160, 176)]
CREST = 120
CREST16 = CREST * 16
SEAM_IN, SEAM_OUT = 132, 150

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(n):
    acc = 1 if "#" in n else (-1 if len(n) > 2 and n[1] == "b" else 0)
    return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + acc


def mtok(m):
    return f"m{m:g}"


def sec_of(bar):
    for name, a, b in SECTIONS:
        if a <= bar < b:
            return name
    return "outfall"


def shift(at):
    """The semitone: Eb before the crest, D from it."""
    return 1 if at < CREST * 4 else 0


# ---- the elements (written in D) ----------------------------------------------------------------------------
E1 = [("D4", 0.5), ("A4", 0.75), ("C5", 0.25), ("G4", 1.0), ("E4", 1.5)]                       # 5 beats with its rest
E2_HITS = {0: ("D", 112), 2: ("A", 84), 3: ("F", 98), 5: ("C", 76)}                          # of 7 sixteenths
E3_RIFF = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("Eb2", 0.5), ("Eb2", 0.75), ("Bb1", 0.75), ("C2", 0.75),
           ("C2", 0.75), ("G2", 0.5), ("C3", 1.0)]                                             # 7 beats
E4_MAJ = [(38, 45, 54, 60, 64), (34, 41, 50, 57, 60, 64), (33, 40, 48, 55, 59, 62), (38, 45, 48, 55, 59, 64)]
E4_MIN = [(38, 45, 53, 60, 64), (34, 41, 50, 56, 60, 64), (33, 40, 48, 55, 59, 62), (38, 45, 48, 55, 59, 64)]
E5 = [(0, "A4"), (1, "G#4"), (2, "A4"), (4, "E5"), (6, "A4"), (7, "G#4"), (8, "A4"), (10, "D5")]  # of 12 sixteenths
E6_X, E6_Y = (50, 54, 57, 61, 64, 68), (51, 55, 58, 62, 69)                                   # Dmaj9#11 | Ebmaj7#11
E7 = [("D3", 2), ("A3", 2), ("E4", 2), ("B4", 1), ("F#5", 1), ("C#6", 1), ("G#6", 2)]          # THE JET: 11 sixteenths
E7_LEN16 = 11

# round 5 (Harry, 6 Nov 00:30: "ugly chaos ... atonal ... missing aesthetics and catchiness/hook ... get musicality back
# and play with time and texture"): T7_R5=tonal (default) - TONE IS HOME. The storm (bars 17-120) is E-flat MINOR, all
# consonant: E3 v2 (D | Bb | C, no Neapolitan ground), E4's lights as plain sevenths and sus chords, E5 with G (not G#)
# in the storm, E6's tide squeezed between i and VI (Ebm(add9) | Cbmaj7, common tones Eb Gb Bb) instead of the Eb|D
# clash, the jet only its consonant first four notes (Eb Bb F C) until the crest. At bar 120 ONE clean modulation down
# a semitone into D MAJOR - E4's lights in major (D9, Bbmaj9, Am7, Dadd9), the tide resolved to Dmaj9 (no G#), the
# vocoder's carrier Dmaj9 - and THE HOOK: E1 stated plainly, upright, on a singing lead through the crest.
# T7_R5=none reproduces v4.
R5 = os.environ.get("T7_R5", "tonal") != "none"
STORM_I, STORM_VI = (51, 54, 58, 65), (47, 51, 54, 58)                     # Ebm(add9) | Cbmaj7 (B D# F# A#)
E5_STORM = [(p, "G4" if nt == "G#4" else nt) for p, nt in E5]
if R5:
    E3_RIFF = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("Bb1", 0.5), ("Bb1", 0.75), ("F2", 0.75), ("C2", 0.75),
               ("C2", 0.75), ("G2", 0.5), ("C3", 1.0)]                                       # E3 v2: D | Bb | C
    E4_MIN = [(38, 45, 53, 60, 64), (34, 41, 45, 50, 57, 60), (33, 40, 48, 55, 60, 64), (38, 45, 48, 55, 57, 62)]
    E4_MAJ = [(38, 45, 54, 60, 64), (34, 41, 50, 57, 60, 65), (33, 40, 48, 55, 60, 64), (38, 45, 50, 54, 57, 64)]
    E6_X = (50, 57, 64)                                                                      # open D-A-E at the crest
# the crest is D MIXOLYDIAN (E1's own mode: D A C G E): E3 locks as I | bVII | IV, the jet's column starts a tone lower
# (C G D A E B F#, the same collection), E5 takes G natural, E4's lights follow E3's chords (one harmonic rhythm)
E3_CREST = [("D2", 0.75), ("D2", 0.75), ("D3", 0.5), ("C2", 0.5), ("C2", 0.75), ("G1", 0.75), ("G1", 0.75),
            ("G1", 0.75), ("D2", 0.5), ("G2", 1.0)]
E7_CREST = [("C3", 2), ("G3", 2), ("D4", 2), ("A4", 1), ("E5", 1), ("B5", 1), ("F#6", 2)]
# round 6 (palette + the agreed seams): T7_R6=harmonic (default). PALETTE: the E1 stretto's bells were inharmonic
# (vosim-bell, modal-bell: partials off the key - part of what Harry heard as atonal) -> dx-epiano (DX7 E.Piano 1, an
# FM tine at 14:1, harmonic) for the x1 voice and scanned-mallet (a struck tone on a scanned ring that mellows, read
# at pitch) for the x2-stretched voice; both unused on the album. And three agreed moves: E7 v2 (five rising fifths,
# D A E B F# on 2 2 2 2 3 sixteenths - holds as a consonant D6/9, tops on the third); the head lands on Ebmaj7 (Eb G Bb
# D, no #11) over t6's B-flat tail - V -> I, the album's one modulation at a seam; and the crest's tide IS E6 v3
# (chirper-one: D(add9) | C(add9)/D, I and bVII of D Mixolydian, its 8-beat split moving 4+4 .. 7+1 .. 1+7).
# T7_R6=none reproduces v5.
R6 = os.environ.get("T7_R6", "harmonic") != "none"
# round 7 (WHOLE): T7_R7=clear (default) - THE STORM YOU CAN HEAR INTO. presence.py over the collision (bars 49-80)
# found a wall of low end - bass -1 dB vs the mix, kick -5, floor -7, tide -8 - with every element under it buried:
# the E1 bells -26..-30, E4 -32, the hats -32, E2's ghosts -28, the bytebeat -43. So: (1) the HOOK in the storm: E1
# stated plainly in E-FLAT MINOR on the crest's own hook lead, two cycles at bars 17, 33, 49 and 73 - the same tune
# the crest will sing in D major, heard first in the dark; (2) the mix: reese -4.5 dB, floor -3, tide -4, kick -2;
# the E1 bells +6..8, E4 +10, E5 +4, hats +10, ghosts +6; (3) the bytebeat cut (inaudible noise); (4) the
# stutter/crush lanes eased (glitch x0.6, grit x0.5): texture, not damage. T7_R7=none reproduces v6.
R7 = os.environ.get("T7_R7", "clear") != "none"
# round 8 (section, w5 = bars 65-80, the collision's second half, flagged 'static, little new'): T7_R8=open (default)
# - THE STORM OPENS INTO A PROGRESSION. For 32+ bars the storm's harmony had flickered Ebm|Cb a beat at a time; here it
# walks i - VI - III - VII (Ebm(add9) | Cbmaj7 | Gb(add9) | Db(add9), two bars each, twice): the tide pulses the
# chords (quarters, then eighths in the second pass - the pull quickening), the reese drives roots in eighths with
# octave kicks, and the pad stabs answer on the offbeats. E1 (Eb Bb Db Ab F) sits as colour over every chord. Old
# parts are silenced (velocity 1), not deleted, so later events keep their randomness. T7_R8=none reproduces v7.
R8 = os.environ.get("T7_R8", "open") != "none"
# round 9 (section, w3 = bars 33-48, the approach's second half, flagged 'static, little new vs w2'): T7_R9=sung
# (default) - THE STORM GETS A SINGER, AND A WAY IN. (1) wM's legato voice (voice-legato, now in the groove pin), made
# larger and more projected than t3's small near voice (tract 1.06, ring 0.4), sings "every corner" ON E1 in E-flat
# minor (Eb Bb Db Ab F - five syllables, five notes) at bars 33 and 41, alone: the hook lead's bar-33 statement steps
# aside. The words come back whole at the crest ("every corner comes sooner", the vocoder): the line is sung half
# here and finished in the orbit. (2) The approach no longer just stops at the collision: a snare roll thickens
# from bar 45 (eighths, sixteenths, then 32nds), bar 48 turns to a snare-and-tom fill with the kick out, and the
# collision lands with an open hat and clap. T7_R9=none reproduces v8.
R9 = os.environ.get("T7_R9", "sung") != "none"
SUNG7_BARS = (32, 40)
# round 10 (palette): T7_R10=legato (default) - THE CHOIR SINGS, THE SEAM SWELLS. (1) The choir that sings "each lap a
# little shorter" (collision fragments, the slack, the crest: six parts, three of them on voice-speech, an album
# staple) moves to wM's voice-legato - joined syllables, an inhale before each phrase, wandering vibrato - with one
# tract per part so it sounds like three singers, not one copied (D 1.08, F#/Gb 1.0, A/Bb 0.94; breath 0.25, ring
# 0.35). Same notes, same words: sung now, not spoken in tune. (2) The E4 held under the t8 seam (a sine on 'sub',
# the album's commonest patch) becomes ambient-swell - the clean guitar faded in by the volume knob into a long
# wash - restruck every two bars from 167: the handover note breathes. T7_R10=none reproduces v9.
R10 = os.environ.get("T7_R10", "legato") != "none"
CHOIR_TRACT = {"0": 1.08, "1": 1.0, "2": 0.94}
# round 11 (section, w2 = bars 17-32, the approach's first half, flagged 'level jump'): T7_R11=drop (default) - THE
# STORM ARRIVES IN TWO STEPS, NOT ONE SLAM. At bar 17 the whole storm (Eb1 floor, reese, break) used to land at once
# (+10 dB over the infall, and the Eb1 floor 28 dB over t6's body). Now bars 17-24 have no floor: the reese carries
# the undertow with a high-passed octave-up double (thin, nasal, wound tight) on top, the break and the E-flat-minor
# hook carrying; bar 24 empties its kick under a one-bar riser; and at bar 25 the Eb1 floor DROPS in - the first real
# weight of the track arrives as an event. (Silencing the reese too left 71-83 Hz 17 dB under t6: kept.) Old notes
# are silenced (velocity 1), new parts on their own tracks. T7_R11=none reproduces v10.
R11 = os.environ.get("T7_R11", "drop") != "none"
# round 12 (section, w4 = bars 49-64, the collision's first half, flagged 'little new vs w3'): T7_R12=answer (default) -
# THE SINGER STAYS IN THE STORM, AND THE STORM TAKES A BREATH. (1) The storm's singer (w3's "every corner") comes
# back at bars 53 and 61, now doubled a fifth below with wM's new `harmony` (-7: Ab Eb Gb Db Bb under Eb Bb Db Ab F -
# every note in E-flat minor) and even vowels: a darker, wider answer to the choir's "each lap" fragment between
# them (bar 57). (2) Bars 61-64 drop to HALF TIME - kick on one, snare on three, hats in eighths - a held breath
# before the progression (w5) lands at bar 65 in full time. Old drum notes silenced (velocity 1), new parts on their
# own tracks. T7_R12=none reproduces v11.
R12 = os.environ.get("T7_R12", "answer") != "none"
SUNG5_BARS = (52, 60)
# round 13 (WHOLE): T7_R13=sung (default) - ONE SINGER THROUGH THE ORBIT. The track's words are one line, begun in
# the storm and finished at the crest - but the finish was a vocoder (an effect). Now the storm's own singer finishes
# it: at the tidal lock (bars 131 and 135) she sings "every corner comes sooner" in D Mixolydian, on E1 (D A C G E)
# and a cadence home (D E D) - the storm's minor fragment answered whole in the major; the second time doubled a fifth
# above (harmony +7: A E G D B, every note in the mode). The vocoder steps out. And every sung part gets wM's even
# vowels (the storm singer, its fifth, the three-part choir), so no 'ee' or 'oo' sinks under an 'ah'. T7_R13=none
# reproduces v12.
R13 = os.environ.get("T7_R13", "sung") != "none"
SUNGC_BARS = (130, 134)
# round 14 (section, w1 = bars 1-16, the infall over t6's tail, flagged 'static'): T7_R14=wheel (default) - THE HEAD
# TURNS. For sixteen bars the infall held one Ebmaj7 on the tide. Now the tide walks I - vi - IV - V in E-flat, four
# bars a chord - Ebmaj7 | Cm9 | Abmaj9 | Bbsus4 -> Bb7 - every chord consonant over t6's B-flat tail and its held D
# (chirper-one's old voice: the 7th, the 9th, the #11, the 3rd), and the last bar's Bb7 is the dominant that the
# storm's E-flat minor resolves (bar 17: D -> Eb, the leading tone). The Eb1 floor stays as a pedal. Old holds
# silenced (velocity 1), the progression on its own track. T7_R14=none reproduces v13.
R14 = os.environ.get("T7_R14", "wheel") != "none"
# round 15 (section, w9 = bars 129-144, the tidal lock - flagged 'static, little new vs w8'): T7_R15=bow (default) -
# A BOWED VOICE AGAINST THE SINGER. (1) NEW: an erhu (a bowed two-string fiddle - a singing tone, bow hair, long
# portamento; no other Accretion track has it) answers the singer in the half-time lock: one long bowed note a
# phrase, A4 - G4 - F#4 - E4, sliding home to D4 at the rebuild - falling while she rises (contrary motion); then in the
# rebuild it takes E1 itself, stretched x2 (D4 A4 C5 G4 E4), and holds A4 up through the snare rush. (2) The singer's
# second statement (bar 135) harmonised a THIRD above in the mode (wM's harmony_key, now pinned: [2] in D
# Mixolydian) instead of a fixed fifth - sweeter, every note in key. T7_R15=none reproduces v14.
R15 = os.environ.get("T7_R15", "bow") != "none"
# round 16 (palette): T7_R16=brass (default) - THE HOOK GOES BRASS. t7 no longer shares a staple with any other track,
# so the palette move is the part that matters most: the hook (E1 stated plainly - in E-flat minor through the storm,
# bars 17/49/73, and in D Mixolydian at the crest) was the song's own two-saw lead. It moves to horn-section (tenor sax
# and trumpet in tight unison, breath on the attack, a little detune between the players; no other Accretion track has
# brass) an octave down, into the horns' warm middle: a brass riff over a drum-and-bass crest, the seed as a fanfare.
# T7_R16=none reproduces v15.
R16 = os.environ.get("T7_R16", "brass") != "none"
# round 17 (palette): T7_R17=horns (default) - A HORN CHOIR UNDER THE BRASS. The crest's chords (E3 v2 at the crest:
# D | C | G) lived only on the tide (saws + noise) and E4's mallet lights. NEW: French horns (horn - warm, round, dark,
# a soft swelling attack; no other Accretion track has them) swell on every chord through the crest, in the horns'
# middle - A3 D4 F#4 A4 | G3 C4 E4 G4 | G3 B3 D4 G4, smooth voice-leading, the top voice falling F# E D (E8's three
# notes turned round, a glance at t8) - under v16's brass hook, so the reward sounds like an orchestra arriving. They
# rest in the tidal lock (bars 129-136: the singer and the erhu) and come back with the rebuild.
# T7_R17=none reproduces v16.
R17 = os.environ.get("T7_R17", "horns") != "none"
HORN_CHORDS = [((57, 62, 66, 69), 2.0), ((55, 60, 64, 67), 2.0), ((55, 59, 62, 67), 4.0)]
# round 18 (whole): T7_R18=thread (default) - THE SINGER THREADS THE SONG. The voice sang in the approach (bars 33/41),
# the collision (53/61), the slack's choir (83-87) and the crest (125-150) - and then not at all for the 36 bars of
# the spiral (88-124), the build she should be leading. (1) She sings "every corner" in the spiral: alone at bar 105,
# then at 113 with a second singer a THIRD ABOVE IN THE KEY (harmony_key, E-flat minor: Eb/Gb, Bb/Db, Db/F, Ab/Cb,
# F/Ab), the line climbing into the crest. (2) Her harmonised statements in the collision (53/61) move from a fixed
# fifth below to the same keyed third above - sweeter, every note in key. So the hook is SUNG at every stage of the
# orbit, and the harmony is always a third in the mode (E-flat minor in the storm, D Mixolydian at the crest, v15).
# T7_R18=none reproduces v17.
R18 = os.environ.get("T7_R18", "thread") != "none"
SPIRAL_SUNG = (104, 112)
# round 19 (palette): T7_R19=breath (default; =wood adds (1)) - WOOD AND BREATH. (1) E1's middle bell was the Game Boy wave channel
# (a7-gb), a chip beside the brass hook, the horn choir, the erhu and the voices this song has grown. It moves to
# modal-marimba (a rosewood bar on the modal layer, hard yarn; no other Accretion track has it): E1 in warm wood
# between the e-piano and the scanned mallet. E5's orbit keeps the chip - the inner orbit's one digital sparkle.
# (2) Every singer gets wM's glide overshoot (pinned 59a832d1; play.glide_overshoot): on each note change the pitch
# swings a little past the new note and settles, as a real singer's does, instead of landing dead on it - 0.08 on the
# soloists and their harmonies, 0.05 on the choir. T7_R19=none reproduces v18.
# DEFAULT IS breath (the overshoot alone). =wood adds the marimba E1 bell: even at -14 dB it cost flow 99.5 -> 93.3
# and spectrum 94.9 -> 94.2 (the wood's mids thicken both seam bodies) - kept as an option.
R19 = os.environ.get("T7_R19", "breath") != "none"
R19_WOOD = os.environ.get("T7_R19", "breath") == "wood"
# round 20 (section, w7 = bars 97-112, the spiral, flagged 'static'): T7_R20=lament (default) - THE SPIRAL TURNS.
# The spiral sat on one chord (E-flat minor) for 32 bars: the elements came in one by one, but nothing moved under them.
# Now from bar 101 the harmony spirals DOWN, four bars a chord, the old lament: Db(add9) - Cbmaj7 - Bb7sus4, and home
# to E-flat minor at bar 113, where the singer's duet lands (the turn resolves exactly where she returns home). The
# tide keeps v4's squeeze (one beat, a half at 105, a quarter at 109) on the new chords; the reese walks the roots;
# E4's lights (105) take the chord tones; the E-flat floor holds underneath as a pedal. E1's bells and E5's orbit sit
# in all three chords; the jet's C and G flatten to Cb and Gb for the Cbmaj7 bars. Old notes silenced (velocity 1),
# the new parts on their own tracks. T7_R20=none reproduces v19.
R20 = os.environ.get("T7_R20", "lament") != "none"
SPIRAL_PROG = [(100, 37, (49, 53, 56, 63)), (104, 35, (47, 51, 54, 58)), (108, 34, (51, 53, 56, 58))]
# round 21 (section, w3 = bars 33-48, the approach, flagged 'static'): T7_R21=reply (default) - THE BRASS ANSWERS
# HER. The storm singer sings "every corner" at bars 33 and 41, and then the groove just carries on. Now the brass
# (the hook's horn-section, an octave down since v16) answers each line two bars later - a falling reply in E-flat
# minor that comes home to the tonic: Ab4 Bb4 Db5 Bb4 Ab4 F4 Eb4 - over a soft French-horn E-flat minor held for the
# two bars (the crest's horn choir, glimpsed once early). A call and response where there was one voice and a loop.
# Own tracks. T7_R21=none reproduces v20.
R21 = os.environ.get("T7_R21", "reply") != "none"
# round 22 (palette): T7_R22=gesture (default) - SUNG, NOT PLACED. wM's scoop and fall (pinned e986de70; first use
# on the album): every phrase's first note now rises in from below and its last note sags as it dies, as a singer
# does - the notes in between untouched (overshoot from v19 still swings between them). The soloist and her harmonies
# scoop 1 semitone and fall 2.5 (her lines sit in delay and space, which mask a smaller fall); the three-tract choir
# 0.6 / 1.5; and the erhu (a7-erhu = erhu + scoop 1.5, fall 1) slides into each bowed note as a player does.
# T7_R22=none reproduces v21.
R22 = os.environ.get("T7_R22", "gesture") != "none"
REPLY_BARS = (34, 42)
# round 23 (section, w4 = bars 49-64, the collision's first half, flagged 'static, little new vs w3'): T7_R23=impact
# (default) - THE COLLISION LANDS. The collision arrived as more of the approach. (1) Bar 49 hits: one long 808 drop on
# E-flat (the orbit's floor, once). (2) The brass that carries the hook turns section: short stabs on the "and" of 2
# and 4 (Gb3 Bb3 Eb4 - the E-flat minor triad, common to both of the tide's chords, Ebm(add9) and Cbmaj7) through
# bars 49-52 and 55-60, stepping out while the singer sings (53-54) and before the half-time (61-64).
# Own tracks. T7_R23=none reproduces v22.
R23 = os.environ.get("T7_R23", "impact") != "none"
# round 24 (palette): T7_R24=organ (default) - THE LIGHTS ON A HAMMOND. E4's four lights (the chord stabs in the
# storm, the collision's i-VI-III-VII, the spiral's lament and the crest) were a Casio CZ pad - a thin digital chord
# among the brass, the horn choir, the erhu and the voices this song has grown. They move to hammond-b3 (drawbars, a
# percussion pop and key click, a Leslie; no other Accretion track has an organ): soul-jazz stabs that sit with the
# horns, the same notes and rhythm. Same track gains (the patches differ by 1 dB). T7_R24=none reproduces v23.
R24 = os.environ.get("T7_R24", "organ") != "none"
# round 25 (whole): T7_R25=polish (default) - THE ORCHESTRA WITHOUT THE STATIC. Since v16 the song has grown brass,
# a horn choir, an erhu, an organ and a singer who threads every stage - and through the storm and the spiral all of
# it still ran into a 7-bit, 12 kHz bit-crusher (the grit lane, on the kit, the reese, the lights, the hook's family):
# harsh damage under an orchestra. (1) The crusher retires (grit lane to zero); the stutter (the glitch lane, a time
# texture) stays as it was. (2) Every singer's vibrato is per note (wM, pinned 58ee9ba3): quick notes plain, held
# ones bloom, a little earlier for this tempo (delay 180 ms, fade 300 ms). (3) THE TUTTI: at the crest's last climb
# (bars 146-147, the hook's two statements before the choir's last "each lap") the horn choir leaves its chords and
# plays E1 itself an octave under the brass, and the erhu plays it an octave over - the whole orchestra on the seed,
# once, at the album's hardest crest. Old horn chords there silenced (velocity 1). T7_R25=none reproduces v24.
R25 = os.environ.get("T7_R25", "polish") != "none"
# round 26 (section, w8 = bars 113-128, the spiral's end into the crest, never focused): T7_R26=turn (default) - THE
# KEY TURNS. The spiral ran in E-flat minor right up to bar 120 and the crest simply dropped a semitone into D: the
# album's hardest crest arrived without being prepared. Now bars 117-120 turn the key: the band leaves E-flat minor
# for E-FLAT MAJOR (bars 117-118, the storm's own chord brightened - and D's Neapolitan) and then A7sus4 -> A7 (bars
# 119-120, D's dominant), so the crest's D lands as an arrival. The brass sings the storm's E1 (Eb Bb Db Ab F) over
# the major chord, then falls A4 G4 E4 - E4 C#4 onto the hook's D; the horn choir holds the chords, voice-leading
# into the crest's first chord (C#4 -> D4). Bass, pad, organ and sub move with them (new tracks); the old pitched
# parts there are silenced (velocity 1) or cut at bar 117. The drums and the riser keep going. T7_R26=none reproduces v25.
R26 = os.environ.get("T7_R26", "turn") != "none"
# round 27 (whole): T7_R27=air (default) - AIR. The song has grown an orchestra but its top had gone dull (spectrum's
# worst band 14.8 kHz -8 dB; the seam from t6 -11.5 dB there; the crusher's fizz left in v25), and the dusty break has
# no shimmer of its own. (1) A SHAKER (the kit's own sh) runs 16ths under the storm and the spiral wherever the hats
# play - quiet, accented on the "e" and "a" - the D&B drive the storm lacked. (2) The crest gets a RIDE (modal-ride):
# quarter-note bell-bow with an off-beat lift through bars 121-152, so the crest opens as well as gets louder.
# (3) Every choir and harmony part sings TOGETHER (wM, pinned 8083e37e): the harmony singers follow the lead's breath,
# effort and vowel instead of a plain default voice. (4) The master's air shelf +1 dB. T7_R27=none reproduces v26.
R27 = os.environ.get("T7_R27", "air") != "none"
# round 28 (palette): T7_R28=timp (default) - TIMPANI. The song has grown an orchestra - brass, a horn choir, an erhu,
# an organ, a ride - but its impacts were still an 808 (the album's staple: t3, t5, t7). A new patch, a7-timp: a
# kettle drum on the modal layer (a membrane struck off-centre, long ring) over a sine fundamental, so it sings a
# pitch, with a felt-mallet thump. It marks the song's four arrivals: a roll on E-flat into the collision (bar 48,
# replacing the 808), a roll on A - D's dominant - through the key's turn and the crest landing on D (bar 120),
# the tutti's two hits on D (bars 146-147), and the plunge (bar 153). T7_R28=none reproduces v27.
R28 = os.environ.get("T7_R28", "timp") != "none"
# round 29 (palette, aimed at the flat runs - Harry 23:55: "subtle variation so it doesn't get boring"; flatness.py
# read t7 47% flat, 0:32-1:28 and 3:28-4:24 56 s each): T7_R29=lines (default) - TWO COUNTER-LINES THAT COME AND GO.
# (1) A MUTED TRUMPET (trumpet-mute; no Accretion track has one) in the approach, bars 25-32 - the 12 bars between the
# hook and the singer where only the groove ran: an E-flat minor line (Bb Db Eb, Ab Gb Ab Bb, Eb Gb Ab Bb ... F Eb),
# twice, the second time climbing to Eb5 to hand over to her at bar 33. (2) MELLOTRON STRINGS (mellotron-strings;
# none on the album) at the crest, bars 137-144 - the stretch where the hook just cycles: a half-note counter-melody
# over D | C | G | G (F#5 E5 D5 B4 / A4 G4 B4 D5 / F#5 G5 B5 D5 / A5 G5 F#5 E5), holding D5 into the tutti. Both
# enter and leave on 8-bar lines - and THE BAND MAKES ROOM for them (a quiet line alone did not move flatness.py at
# all): under the trumpet's first phrase (bars 25-28) the kick, snare, ghosts and bass drop out - hats, shaker and the
# tide carry the pulse - and return at 29; when the strings enter (bars 137-140) the kick and bass drop out under the
# hook, the horns and the ride, and come back at 141 for the climb into the tutti. T7_R29=none reproduces v28.
R29 = os.environ.get("T7_R29", "lines") != "none"
# round 30 (section, aimed at the flat runs 0:56-1:28 and 1:28-2:00 - the approach's second half and the collision;
# Harry 23:55 "subtle variation"): T7_R30=lift (default) - THE FLOOR LIFTS. What t3 v30 taught: in a dense song the
# bass dominates both the flatness measure and the sections, so it should MOVE, not vanish. Twice, 16 bars apart:
# (1) bars 45-48, before the collision, the kick, snare, ghosts and perc step out, the hats thin to eighths and the
# reese and the floor climb an octave over the timpani's roll - so the collision's drop at 49 lands from a height;
# (2) bars 57-60, the middle of the collision (under the brass stabs), the same lift - drums out, hats in eighths,
# the reese and the floor an octave up - coming down into the half-time breath at 61 - lift, breath, then the collision resumes at 65. (A first draft lifted
# inside the half-time itself; flatness did not see it there.) T7_R30=none reproduces v29.
R30 = os.environ.get("T7_R30", "lift") != "none"
# round 31 (section, aimed at the last flat run 3:52-4:24 - the crest's second half, bars 135-154): T7_R31=float
# (default) - THE CREST FLOATS. v29 dropped the kick and the bass out under the strings' entry (137-140), but in a
# crest the run went on to 4:24. Now the crest's last climb takes the song's own lift (v30): at bars 149-152, under the
# choir's last "each lap", the drums step out, the hats thin to eighths and the reese and the floor go an octave UP -
# floating after the tutti - and the timpani's plunge at 153 lands it. (A draft that also turned v29's drop-out at
# 137-140 into a lift made the crest flat from 3:28 instead: there the missing floor is the stronger move.)
# T7_R31=none reproduces v30.
R31 = os.environ.get("T7_R31", "float") != "none"
# round 32 (palette): T7_R32=kettle (default) - REAL KETTLES, AND VOICES THAT BREAK. Two engine features made for or
# first used here: (1) wM's `modes: kettle` (pinned 07876a82, built for this song): v28's timpani were a membrane with a
# helper sine that still read as a tom; now the modal head is a kettle - the (n,1) family pulled by the air to
# 1 : 1.5 : 2 : 2.5, the principal tone singing over a short thump - struck where players strike (0.7), and the helper
# sine is gone. (2) Registers (wM, pinned 0c5d29c5): the choir's alto and soprano now break into head voice above C5 and
# the soloist above B4 - the top of every line turns rounder and airier, the way a singer's voice lifts (the soprano 1 dB
# up for head voice's softness). T7_R32=none reproduces v31.
R32 = os.environ.get("T7_R32", "kettle") != "none"
# round 33 (section, w6 = bars 81-96, the slack into the spiral, never focused): T7_R33=answer (default) - THE TRUMPET
# ANSWERS THE CHOIR. In the slack the choir sings "each lap" twice over the frozen E-flat minor chord (bars 83 and 86)
# and nothing answers it; the spiral then simply starts. The muted trumpet from the approach (v29) comes back to
# answer: after the first line it falls Db5 Bb4 Ab4 Gb4 F4 (bar 84), after the second it climbs Gb4 Ab4 Bb4 Db5 to a
# held Eb5 that carries the slack over the edge into the spiral (bars 87-88). Call and response, and the trumpet becomes
# a recurring voice rather than a one-off. Appended to the trumpet track. T7_R33=none reproduces v32.
R33 = os.environ.get("T7_R33", "answer") != "none"
# round 34 (whole): T7_R34=plain (default) - THE HOOK IN PLAIN SIGHT, AND THE FLOOR UNDER IT. Harry: E1 is the album's
# hook and should be heard plainly and often. In t7 the E1 ostinato runs through half the song on three chip lines
# (epiano, the gameboy lead, the mallet), but presence.py heard them at -17..-20 dB against the mix, masked nearly
# all the time: the hook was wallpaper. All three come up 2 dB (the wide copies too), so the figure you hum reads all
# the way through, and the floor comes up under them so the balance holds: the reese's sine body from -3 dB to +3 dB
# and the Eb sub 5 dB up (presence -8.4 -> -4.1). Draft: chips +4 dB with a lighter floor cost s0 0.66 (spectrum
# 92 -> 86: the mix tipped up). T7_R34=none reproduces v33.
R34 = os.environ.get("T7_R34", "plain") != "none"
# round 35 (palette): T7_R35=koto (default) - THE HOOK ON PLUCKED STRINGS. v34 raised the E1 ostinato and found the
# limit: more gain tipped the mix. The loudest-masked of its three lines was the library dx-epiano (e1a and its wide
# copy), a soft FM tine that melts into the organ and the choir. It moves to the library koto (no other Accretion
# track has it): ivory picks near the bridge, a twang on every attack and a singing decay that carries E1's long notes -
# so the hook reads by articulation, not level, and sits beside the erhu as the orbit's plucked-and-bowed pair.
# (Also: the silent boom track - one velocity-1 event since v28 - leaves the album's 808 staple for the kettle.)
# T7_R35=none reproduces v34.
R35 = os.environ.get("T7_R35", "koto") != "none"
# round 36 (palette): T7_R36=log (default) - THE LOW E1 ON A LOG DRUM. The E1 ostinato's low line (e1c and its wide copy:
# D3-C#4, under the koto and the chip lead) ran on the library scanned-mallet, a soft woody blur. It moves to the
# library log-drum (no other Accretion track has it): the Amapiano log drum - a short boomy pitched sine with a woody
# click, a pitch drop and a slight glide, the bouncing bass-percussion of South African house. The hook bounces in
# the bottom of the orbit, and the floor gets body where t7 was thin. It steps out (-24 dB on an automation lane) in
# the five bars-wide holes the floor already leaves - the drop-outs at 25-28 and 137-140, the lifts at 45-48, 57-60
# and 149-152 - so those still open up. (Draft without the lane: s0 99.167 but a new 32 s flat run 0:48-1:20 - the
# log drum filled the approach's drop-out.) T7_R36=none reproduces v35.
R36 = os.environ.get("T7_R36", "log") != "none"
# round 37 (section, w3 = bars 33-48 - the approach's second half, flagged static): T7_R37=echo (default) - SHE HUMS
# THE ANSWER BACK. In the approach the singer has one bar ("every corner", bars 33 and 41), the horns answer
# (35, 43), and then the groove runs alone for two bars each time. Now she hums the horns' answer back on "oo"
# two bars later (Ab4 Bb4 Db5 Bb4 Ab4 F4 Eb4, bars 37-38), softly, behind a longer echo; and the second time it floats
# over the lift (bars 45-46, the drums out). Call, answer, echo: the voice grows without giving away the words
# (the line completes only at the crest). T7_R37=none reproduces v36.
R37 = os.environ.get("T7_R37", "echo") != "none"
# round 38 (whole): T7_R38=arc (default) - ONE ARC TO THE HARDEST CREST. The master dyn lane had the collision at 0 dB
# and the crest only 1 dB above it: by level the innermost orbit's crest - the album's hardest - was hardly higher
# than the first storm, and the spiral sat level too. Redrawn as one climb (t3 v26's lesson): approach -4 -> -3.5 dB,
# collision -3.5, the slack deeper (-6.5 -> -5.5), the spiral climbing -4 -> -1, the crest untouched at +1 (the glue
# and limiter eat most of it: measured, the crest now sits 1.5-1.9 dB above the collision instead of 0.1-0.4; a
# gentler draft at -2 got 1.0-1.3). The head's start under t6 and the plunge and outfall into t8 are unchanged.
# T7_R38=none reproduces v37.
R38 = os.environ.get("T7_R38", "arc") != "none"
# round 39 (palette): T7_R39=age (default) - THE CHOIR HAS AGED. wM's `age` (pinned 44372fb9): the folds leak air,
# the line wavers and a slow 4.5-6.5 Hz tremor shakes it, each singer on their own phase. The crest choir sings
# "each lap a little shorter" (bars 125 and 141) - the orbit decaying, time running out - with the same young voices
# that sang "each lap" in the collision. Now the crest's three singers (vd0-vd2) sing on aged copies of their
# patches (age 0.4): the same words, older - weathered by the laps between. The collision's choir stays young,
# so the voice ages across the song (and meets t6's old voice, age 0.8, across the album). T7_R39=none reproduces v38.
R39 = os.environ.get("T7_R39", "age") != "none"
# round 40 (section, w5 = bars 65-80 - the collision's second half, "little new vs w4"): T7_R40=decay (default) - THE
# ORBIT LOSES ENERGY. The collision ran at full strength right up to the slack's frozen chord at bar 81 and then simply
# stopped. Now its last four bars lose their parts one by one, the way an orbit sheds energy: at bar 77 the hats and
# the shaker go, at 78 the snare, the ghosts and the perc, at 79 the E1 chips and E5's trill, at 80 the kick - so the
# bass, the tide, the organ and the horns carry the collision down into the slack. T7_R40=none reproduces v39.
R40 = os.environ.get("T7_R40", "decay") != "none"
# round 41 (section, w8/w9 seam = bars 121-134 - the crest's first fifteen bars, flatness's deepest rut: three 8 s
# blocks alike at 3:28-3:52, changes 0.31 and 0.18): T7_R41=breath (default) - THE FLOOR HOLDS ITS BREATH. The reese
# drives its E7 riff (ten notes a bar) under the whole crest - the loudest thing in the mix - so the choir's "each lap a
# little shorter" and the tidal lock ("every corner comes sooner", bar 131) sat on one unbroken floor. Now for bars
# 125-130 - under the choir's line and up to the lock - the riff stops: the reese holds a D2 a bar at a time (its first
# note of each bar, sustained) over the sub's D, the kick and the horns carry on - and at bar 131 the riff comes back
# with the lock. (Drafts: 4 bars, 127-130, on D2 or D3 - the rut's changes 0.31/0.18 -> 0.6/0.25 only: four bars
# straddle two of flatness's 8 s blocks.)
# T7_R41=none reproduces v40.
R41 = os.environ.get("T7_R41", "breath") != "none"
# round 42 (whole): T7_R42=breathe (default) - THE ORBIT BREATHES. v41 let the floor hold its breath once, under the
# crest choir, and it broke t7's deepest rut; t3 v42 found the same gesture works across a whole song. The reese riff
# is the loudest thing in t7 and ran unbroken under its other ruts too (flatness: the approach's second half 1:04-1:12,
# the spiral 2:48, the crest's end 4:00-4:08). Now the riff breathes there as well - bars 37-40 (under the singer's
# second "every corner" and her hummed echo), 96-100 (the spiral, before her line at 105) and 141-144 (the crest's
# end, between the band's drop-out and the lift): in each half bar its lowest note is held, the rest let go - the
# riff slowed to its own roots - then it drives again. With v41's breath at 125-130 the gesture comes four times,
# once in each part of the orbit. T7_R42=none reproduces v41.
R42 = os.environ.get("T7_R42", "breathe") != "none"
# round 43 (section, w3 = bars 33-48 - the approach's second half, still flatness's rut at 1:04-1:12): T7_R43=open
# (default) - SHE HUMS INTO AN OPEN FLOOR. v42's breath (bars 37-40) slowed the reese to its roots but the sub's
# E-flat pedal held on underneath, so the floor barely changed. Now the sub lets go too for those four bars - only
# the reese's held roots and the kick under the singer's echo - and the echo itself (v37: the horns' answer hummed
# back, bars 37-38 and 45-46) becomes a true closed-mouth hum (wM's hum, pinned e3da830a: hum 1 at m, 3 dB up -
# high hums are quieter): she hums the answer back, mouth shut, into the open floor. T7_R43=none reproduces v42.
R43 = os.environ.get("T7_R43", "open") != "none"
# round 44 (palette): T7_R44=thump (default) - A BODY UNDER THE BREAK. t7's kick is the dusty kit's - a lo-fi
# break kick, all knock and no chest - and compscore's spectrum has said for many rounds that t7 is 10 dB short at
# 61 Hz, the band a dance kick lives in. Now a second kick sits under every hit of the break (and of the crest's
# half-time): the album's first tuned kick, a7-thump - the 909's sine kick with its pitch moved from G1 to Bb1
# (58 Hz: the fifth of the storm's Eb and E4's Bb colour in D, never against either), low-passed at 180 Hz so only
# its body speaks, 2 dB over the dusty kick's own level (the reese and floor mask it below that), through the same glitch and grit lanes. The break keeps its dust on
# top and gets a chest. T7_R44=none reproduces v43.
R44 = os.environ.get("T7_R44", "thump") != "none"
# round 45 (section, w10 = bars 145-160 - "static, little new vs w9"): T7_R45=redshift (default) - THE PLUNGE FALLS.
# In the plunge's last four bars (157-160) the drums and the floor have already gone and E1's stretto (koto and chip)
# and the jet (E7) carry on exactly as they did in the crest, so the plunge never plunged. Now those three lines fall:
# for four bars they bend down a whole octave, slowly then faster (0, -3 by 159, -6 by 160, -12 at its end) - E1 and
# E7 redshifted as they cross the horizon - while the modal bell alone holds its E above them, the note t8 lifts.
# They come back at pitch with the outfall. The falling copies are new tracks (e1apl, e1bpl, jetpl) on new patches
# (koto-pl, a7-gb-pl, a7-jet-pl: the same instruments with the lane on their pitch - the oscillators really bend; a
# pitch-shifter fx left a 38 Hz grain rumble the t8 seam heard), while the originals just let go of those bars.
# T7_R45=none reproduces v44.
R45 = os.environ.get("T7_R45", "redshift") != "none"
# round 46 (palette): T7_R46=orbit (default) - THE SPIRAL FALLS FOREVER. An orbit is falling that never arrives,
# and the spiral (bars 89-120, the inspiral before the crest) had no sound for that: its pads were the tide's chords,
# pulsing. Now under the whole spiral a Shepard-Risset pad - t2's endless fall come back (chirper-one's shepard-fall
# on D under t2's infall, "the infall that never lands") - glides DOWN an octave every 8 seconds and never gets lower, on E-flat and B-flat (the pedal and its fifth: in every
# chord the spiral moves through, Ebm9, Cbmaj7, Db add9). It enters with the spiral at 89 and lets go just before
# the crest lands on D at 121, so the endless fall stops exactly where the orbit locks: t2's fall, landing at last. Patch a7-orbit =
# shepard-pad with both layers down. T7_R46=none reproduces v45.
R46 = os.environ.get("T7_R46", "orbit") != "none"
# round 47 (palette): T7_R47=clav (default) - E4 ON A CLAVINET. E4 (the album's chords: D9, Bbmaj13#11, Am11, D9sus,
# in t7 a semitone up in the storm) is comped all through the approach, collision, spiral and crest - 367 short stabs
# of a five-note voicing on 0.35 beats, on and off the beat - on the hammond, whose sustained drawbar tone smeared into
# the tide and the choir: presence put it at -13.6 dB in the crest, audibility 0. Now a clavinet (the album's only
# one; the library's physical clav) doubles every stab: a string struck by a tangent and choked by its felt the moment
# the key lifts, so each 0.35-beat stab gets a hard funky pluck on top of the organ's body, panned opposite it - the
# harmony becomes rhythm, the groove of E4 heard. (Replacing the organ outright lost its 16' drawbar - t7's 97 Hz,
# 10.7 dB short then - and cost 0.39.) The section variants (collision offbeats, spiral) are doubled too.
# T7_R47=none reproduces v46.
R47 = os.environ.get("T7_R47", "clav") != "none"
# round 48 (section, w4 = bars 49-64, "static, little new vs w3"; the collision): T7_R48=collide (default) - THE
# COLLISION HEARD. The collision (bars 49-80) is where t7's pieces first crash together, but in it only the floor and
# the kick could be heard (presence: bass -2.8, sub -3.2, kick -6.7 vs the mix) - the break's backbeat snare sat at
# -20.5, the jet's two- and three-note fragments (E7 trying to fire) at -17.9, the brass stabs on the off-beats at
# -16.4, all masked: a kick-and-bass groove. Now for the collision's 32 bars those three step forward together on one
# lane: the snare +7 dB (a backbeat you hear), the jet +9 (its fragments spark: it tries to fire, and fires whole at
# the crest), the stabs +5. Levels only; the notes were always there. T7_R48=none reproduces v47.
R48 = os.environ.get("T7_R48", "collide") != "none"
# round 49 (section, w5 = bars 65-80, "little new vs w4"; the collision's second half): T7_R49=stop (default) - THE
# COLLISION STOPS DEAD. For 32 bars the collision ran one groove and no event broke it. Now in its middle, bars
# 69-70, the band plays STOP-TIME: everything hits together on the downbeat and on the "and" of two - kick, reese,
# floor, tide, the byte, E4's off-beat chords, E1 and E5 where they land there - each cut to a stab, and between the
# hits silence: no hats, no ghosts, no shaker, nothing ringing; then bar 71 slams the groove back in. Two impacts,
# twice: a collision you hear. No note is added or moved; the others let go. T7_R49=none reproduces v48.
R49 = os.environ.get("T7_R49", "stop") != "none"
# round 50 (palette): T7_R50=clap (default) - A CLAP ON THE BACKBEAT, AN EVEN HUM. (1) t7's backbeat is the dusty
# kit's snare - a lo-fi break snare, all body and no crack - and outside the collision (v48 lifted it there) it is
# masked almost everywhere (the crest: -16.8 dB vs the mix). Now every backbeat (its 206 hits and the crest's
# half-time four) is doubled by the electro kit's 808-style clap (the album's first): the break keeps its dust, and
# the 2 and 4 crack. Same glitch, grit and collision lanes as the snare. (2) The echo hum (v43: the singer humming
# the horns' answer back, mouth shut) had 3 dB added by hand because closed hums fade on high notes; it now uses wM's
# hum_even (pinned 1d916569), which holds a hum at the open voice's loudness note by note, and the hand gain goes.
# T7_R50=none reproduces v49.
R50 = os.environ.get("T7_R50", "clap") != "none"
# round 51 (section, w2 = bars 17-32, the approach's first half; focused least recently): T7_R51=call (default) - A
# CALL BEFORE THE ANSWER. When the storm lands at bar 17 the horns state E1 once (two bars), and the muted trumpet
# answers from bar 25 - but between them six bars passed with only E1's koto stretto, masked (-16 dB): the call was
# heard once and the answer came out of nothing. Now the horns call AGAIN at bar 21, the same two bars - E1 plainly
# twice, a riff you can expect - and bar 24 ends in a fill (the dusty kit's snare and tom in sixteenths, swelling,
# an open hat on the trumpet's downbeat) that hands the trumpet its entrance. T7_R51=none reproduces v50.
R51 = os.environ.get("T7_R51", "call") != "none"
# round 52 (section, w1 = bars 1-16, the infall, flagged 'static'; focused least recently): T7_R52=jet (default) -
# THE JET SEEN FROM FAR OFF. For its first 29 s t7 was the tide's four-bar chords over a held sub and nothing else:
# Harry's 30 s where nothing changes. Now E7, the jet (this track's own element: rising fifths on 2 2 2 2 3
# sixteenths), is seen from far away before the storm lands: a glockenspiel, far back in the space, spells it from
# B-flat (Bb F C G D - notes common to t6's D minor tail and t7's E-flat, so it is consonant on both sides of the
# crossfade). Bar 5: its first three notes, a beat apart. Bar 9: all five, still a beat apart. Bar 13: at its real
# speed, three times round its 11-sixteenth loop against the bar - the jet coming closer every four bars, until
# the storm lands at 17. T7_R52=none reproduces v51.
R52 = os.environ.get("T7_R52", "jet") != "none"
# round 53 (section, w9 = bars 129-144, the crest's heart; focused least recently): T7_R53=clear (default) - THE
# MACHINERY STOPS, THEN REASSEMBLES. Bars 137-140 were meant as the crest's lift (kick and bass drop out; the horns
# play E1, strings and the high jet come in) but the machinery never stopped: E1's stretto on three instruments,
# E5's trill, the organ and clavinet comping, the ride and the ghost notes all ran straight through every bar of the
# crest, so the lift was a mush and the horns' E1 was half heard. Now for those four bars the machinery stops - the
# horns' E1, the strings, the jet and the tide alone - and then it comes back one layer a bar under the snare rush:
# ride and ghosts at 141, the organ and clav at 142, the log drum and koto at 143, the glass and E5 at 144, all of it
# running again for the drop at 145. The organ barely follows velocity (vel_sens 0.25), so its "silenced" notes
# still sounded - here and through v49's stop-time (bars 69-70), which never quite stopped: a gain lane now closes
# the organ (and the clavinet copying it) for both, opening only for the stop-time's four stabs. T7_R53=none
# reproduces v52.
R53 = os.environ.get("T7_R53", "clear") != "none"
# round 54 (whole song): T7_R54=body (default) - BODY AND BREATH. Against the album's envelope t7 was thin where a
# groove lives and hard where ears tire: 61-114 Hz sat 10-11 dB short (the kick's and the reese's body) and 1.4-4.9 kHz
# 3-6 dB over (the clav, the organ's bite, the hats - harsh by the crest). And the reese - E3's undertow, the loudest
# thing in every window - ran as one wall over the kick. Now (1) the master gives the body back (+4 dB around 95 Hz)
# and takes the edge off (-3 dB around 2.6 kHz), and (2) the reese and the floor dip under every kick (the album's
# pump, as t2/t3/t6: -5/-6 dB, 200 ms, curve 0.6), so the innermost orbit hits and breathes instead of droning.
# T7_R54=none reproduces v53.
R54 = os.environ.get("T7_R54", "body") != "none"
# round 55 (section, w11 = bars 161-176, the outfall under t8's head; flagged 'static, level jump', never worked;
# agreed with chirper-three 8 Nov 01:40): T7_R55=heart (default) - THE LAST HEARTBEAT. After the plunge the
# outfall was the tide's open fifths, the bell's held E and the break's kick thudding on in half notes - sixteen bars
# of the same, under t8's opening. Now the kick becomes a heartbeat (a thump and its softer echo) that slows as the
# orbit decays: every two beats, then every two and a half, then every five - and from t8's bar 2 its beats land on
# t8's own chord changes (its strings move on a five-beat cycle), each fainter, gone by beat 694; t7's pulse hands
# itself to t8's. No new pitch (t8 is D natural minor; nothing near E4-F4). And the plunge's octave bend (bars
# 157-160) no longer drags its lowest notes into the sub: a 90 Hz high-pass on the falling copies takes out the
# 38 Hz rumble that sat 12 dB over t8 at the seam. T7_R55=none reproduces v54.
R55 = os.environ.get("T7_R55", "heart") != "none"
# round 56 (whole song): T7_R56=inspiral (default) - THE ORBIT YOU CAN HEAR. t7 is the innermost orbit, the last stable
# circle before the fall, and E5 is the album's orbit - yet in t7 it sat still, a glass trill parked left of centre
# and mostly masked. Now it orbits the listener (Chowning's moving source: the engine's orbit fx, centred on the
# head so there is no Doppler - nothing goes out of tune): a lap every four bars in the approach, faster through the
# collision, easing in the slack, a lap a bar in the spiral, two a bar at the crest, and six a bar as the plunge
# takes it in - while its radius shrinks from eight metres to half a metre: an inspiral, the whole song long. The
# spiral's falling Shepard pad circles with it, and so does the tide (E6's chords, t7's main pad - opposite the
# trill, so where the trill is masked the motion is still heard in the pad). T7_R56=none reproduces v55.
R56 = os.environ.get("T7_R56", "inspiral") != "none"
# round 57 (section, w7 = bars 97-112, the spiral's second half; focused least recently): T7_R57=sooner (default) -
# EVERY CORNER COMES SOONER. The spiral's singer sings "every corner" (E1, in E-flat) at bar 105 and again, in
# harmony, at bar 113 - and between them eight bars of nothing sung. Now the words do what they say: the phrase comes
# round again eight beats later in another voice (left), then six, then four and a half (right, left), and then only
# its first word, "every" (E-flat, B-flat, D-flat: one chord, so the overlaps stay sweet), sooner and sooner - two
# and a half beats, two, one and a half, one and a quarter, one - an accelerando of voices that lands on the
# harmonised statement at bar 113. T7_R57=none reproduces v56.
R57 = os.environ.get("T7_R57", "sooner") != "none"
TURN = [(116, 39, 27, (51, 55, 58, 63)), (118, 33, 33, (52, 55, 57, 62)), (119, 33, 33, (52, 55, 57, 61))]
STAB_BARS = [48, 49, 50, 51, 54, 55, 56, 57, 58, 59]
REPLY = [(68, 0.5), (70, 0.5), (73, 1.0), (70, 0.5), (68, 0.5), (65, 1.0), (63, 2.0)]
BOW_LINE = [(128, 69, 7.6), (130, 67, 7.6), (132, 66, 7.6), (134, 64, 7.8), (136, 62, 7.5)]
HEAD_WHEEL = [(0, (51, 55, 58, 62)), (4, (48, 51, 55, 58, 62)), (8, (44, 51, 55, 58, 60)), (12, (46, 51, 53, 58)),
              (14, (46, 50, 53, 56))]
W5_PROG = [(39, (51, 54, 58, 65)), (35, (47, 51, 54, 58)), (42, (54, 58, 61, 68)), (37, (49, 53, 56, 63))]
E7_V2 = [("D3", 2), ("A3", 2), ("E4", 2), ("B4", 2), ("F#5", 3)]
EB_MAJ7 = (51, 55, 58, 62)
E6V3_D, E6V3_C = (50, 57, 62, 64, 66), (50, 55, 60, 62, 64)                  # D(add9) | C(add9)/D
if R6:
    E7 = E7_V2
    E7_CREST = E7_V2
CREST_CHORDS = [((62, 66, 69, 76), 2.0), ((60, 64, 67, 74), 2.0), ((59, 62, 67, 69), 4.0)]   # D(add9) | C(add9) | G(add9)


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


def cycle_starts(length16, lo16, hi16, crest16=CREST16):
    first = crest16 - length16 * math.ceil((crest16 - lo16) / length16)
    return list(range(first, hi16, length16))


PATCHES = {
    "a7-reese": {"about": "chirper-two: the inner orbit's bass - two saws 14 cents apart beating against a sine, low-"
                          "passed with no resonance: a reese that rolls rather than squelches",
                 "synth": {"layers": [{"wave": "saw", "detune": -7}, {"wave": "saw", "detune": 7},
                                      {"wave": "sine", "level": "-3dB"}],
                           "drive": 0.25, "filters": ["lp cutoff=850 q=0.6"],
                           "amp": {"a": "3ms", "d": "200ms", "s": 0.85, "r": "70ms"}},
                 "play": {"mono": True, "glide": "15ms"}},
    "a7-gb": {"about": "chirper-two: a Game Boy wave channel with its own 32-step table (a bent saw with a notch): the "
                       "squeezed stretto voice and E5's trill",
              "synth": {"layers": [{"type": "chip", "chip": {"kind": "wave", "clock": 2097152,
                                                             "table": [15, 14, 13, 12, 12, 11, 10, 9, 9, 8, 7, 7, 6, 5,
                                                                       4, 4, 3, 2, 2, 1, 0, 0, 8, 12, 14, 15, 15, 14,
                                                                       12, 9, 5, 2]}}],
                        "amp": {"a": "1ms", "d": "90ms", "s": 0.5, "r": "40ms"}}},
    "a7-jet": {"about": "chirper-two: the jet - a hard-synced saw whose slave sweeps up an octave and a half on every "
                        "note, over a square an octave down: bright, fired, never squelchy",
               "synth": {"layers": [{"name": "master", "wave": "sine", "audible": False},
                                    {"wave": "saw", "sync": "master", "semi": {"value": 3, "mod": [{"src": "env.fire", "amount": 18}]}},
                                    {"wave": "square", "ratio": 0.5, "level": "-8dB"}],
                         "env": {"fire": {"a": "0.5ms", "d": "160ms", "s": 0.0, "r": "40ms"}},
                         "filters": ["hp cutoff=180", "lp cutoff=7000 q=0.6"],
                         "amp": {"a": "1ms", "d": "220ms", "s": 0.5, "r": "120ms"}}},
    "a7-tide": {"about": "chirper-two: the squeezed tide - a breathy saw pad with a quick swell, for E6's one-beat pull",
                "synth": {"layers": [{"wave": "saw", "detune": -5}, {"wave": "saw", "detune": 5},
                                     {"type": "noise", "level": "-22dB"}],
                          "filters": ["hp cutoff=150", "lp cutoff=2600 q=0.5"],
                          "amp": {"a": "40ms", "d": "300ms", "s": 0.7, "r": "200ms"}}},
}


def build():
    rng = random.Random(7)
    names = ("kick", "snare", "ghost", "hats", "perc", "bass", "sub", "e1a", "e1b", "e1c", "e4", "e5", "tide",
             "jet", "jethi", "byte", "hold", "riser")
    T = {k: Track(k) for k in names}

    # ---- E7, THE JET: fragments in the collision (it tries to fire), more in the spiral, whole from the crest -----
    for c in cycle_starts(E7_LEN16, 48 * 16, 160 * 16):
        at = c / 4.0
        bar = int(at // 4)
        sec = sec_of(bar)
        if sec in ("slack",):
            continue
        if sec == "collision":
            n = rng.choice([2, 3, 3, 4]) if rng.random() < 0.55 else 0
        elif sec == "spiral":
            n = min(7, 3 + (bar - 88) // 8 + rng.randint(0, 1))
            if R5:
                n = min(n, 4)
        elif sec in ("crest", "plunge"):
            n = 7
        else:
            n = 0
        for i, (nt, l16) in enumerate((E7_CREST if R5 and at >= CREST * 4 else E7)[:n]):
            m = midi(nt) + shift(at)
            T["jet"].add(at, l16 / 4 * 0.9, mtok(m), 84 + 4 * i)
            if sec == "crest":
                T["jethi"].add(at, l16 / 4 * 0.9, mtok(m + 12), 70 + 3 * i)
            at += l16 / 4

    # ---- E1: a three-speed stretto (x1 vosim bell, x2 squeezed on the Game Boy, x2 stretched on the modal bell) ----
    for trk, scale, lo, vel in (("e1a", 1.0, 16, 80), ("e1b", 0.5, 32, 72), ("e1c", 2.0, 16, 74)):
        L16 = int(20 * scale)
        for c in cycle_starts(L16, lo * 16, 160 * 16):
            at = c / 4.0
            bar = int(at // 4)
            sec = sec_of(bar)
            if sec == "slack" or (sec == "approach" and trk == "e1b"):
                continue
            for nt, ln in E1:
                if sec == "collision" and rng.random() < 0.18:
                    at += ln * scale
                    continue
                T[trk].add(at, ln * scale * 0.9, mtok(midi(nt) + shift(at) + (12 if trk == "e1b" else 0)
                                                     - (12 if trk == "e1c" else 0)), vel + rng.randint(-6, 6))
                at += ln * scale
    # the outfall: E1 stretched x4, stopping on its E - held, for t8 to lift
    at = 160 * 4.0
    for nt, ln in E1:
        T["e1c"].add(at, ln * 4 * 0.95 if nt != "E4" else (TOTAL - at - 0.25), mtok(midi(nt) - 12 + 12), 78)
        at += ln * 4
    if R10:                                                                   # E4 under the seam, swelling
        for bar in range(166, 176, 2):
            T["hold"].add(bar * 4.0, 8.0 - 0.25, "m64", 70 - (bar - 166) * 2)
    else:
        T["hold"].add(166 * 4.0, (TOTAL - 166 * 4.0) - 0.25, "m64", 66)       # E4 under the seam
    T["tide"].add(164 * 4.0, (TOTAL - 164 * 4.0) - 0.25, "m50,m57,m64", 74)    # D A E, open: no third - t8 brings it

    # ---- E3, the undertow, squeezed x2 on the reese (3.5 beats), barred at the crest (4 beats) --------------------
    for c in cycle_starts(14, 16 * 16, CREST16):
        at = c / 4.0
        sec = sec_of(int(at // 4))
        for nt, ln in E3_RIFF:
            if sec != "slack" and not (sec == "collision" and rng.random() < 0.1):
                T["bass"].add(at, ln / 2 * 0.85, mtok(midi(nt) + shift(at) + (12 if sec == "collision" and rng.random() < 0.12 else 0)),
                              104 if ln >= 0.75 else 92)
            at += ln / 2
    for bar in range(CREST, 152):
        at = bar * 4.0
        for j, (nt, ln) in enumerate(E3_CREST if R5 else E3_RIFF):
            l2 = (ln + (1.0 if j == len(E3_RIFF) - 1 else 0)) / 2
            T["bass"].add(at, l2 * 0.88, mtok(midi(nt)), 110 if ln >= 0.75 else 96)
            at += l2
    for bar in range(0, 152, 2):                                              # the floor (Eb1 from t6's blur, D1 at the crest)
        if sec_of(bar) != "slack":
            T["sub"].add(bar * 4.0, 7.8, mtok(26 + shift(bar * 4.0)), 70)

    # ---- E4, four lights at half harmonic rhythm (10 beats): storm minor in Eb, its major in D from the crest -----
    for c in cycle_starts(40, 16 * 16, 152 * 16):
        at = c / 4.0
        for k in range(4):
            sec = sec_of(int(at // 4))
            if sec not in ("slack", "infall") and not (R5 and at >= CREST * 4):
                ch = (E4_MIN if at < CREST * 4 else E4_MAJ)[k]
                s = shift(at)
                for off in ((0, 0.75, 1.5) if sec in ("collision", "spiral") else (0, 1.5)):
                    if off < 2.5:
                        T["e4"].add(at + off, 0.35, ",".join(mtok(m + 12 + s) for m in ch[1:]), 86 if off == 0 else 70)
            at += 2.5
    if R5:                                                                   # the crest: E4's lights on E3's chords
        for bar in range(CREST, 152, 2):
            at = bar * 4.0
            for ch, ln in CREST_CHORDS:
                for off in (0.0, 1.5) if ln == 2.0 else (0.0, 1.5, 2.5):
                    T["e4"].add(at + off, 0.35, ",".join(mtok(m) for m in ch), 88 if off == 0 else 72)
                at += ln

    # ---- E5, the inner orbit: squeezed x2 into a trill (6 sixteenths) in the storm, itself from the crest -------
    for c in cycle_starts(6, 16 * 16, CREST16):
        at = c / 4.0
        if sec_of(int(at // 4)) in ("slack", "approach") and int(at // 4) < 32:
            continue
        for pos, nt in (E5_STORM if R5 else E5):
            T["e5"].add(at + pos / 8.0, 0.11, mtok(midi(nt) + shift(at)), 70 + (10 if pos == 0 else 0))
    for c in cycle_starts(12, CREST16, 152 * 16):
        for pos, nt in (E5_STORM if R5 else E5):
            T["e5"].add(c / 4.0 + pos / 4.0, 0.2, mtok(midi(nt)), 76 + (10 if pos == 0 else 0))

    # ---- E6, the tide squeezed to a one-beat pull (Eb | D) in the storm; frozen on Eb in the slack; D at the crest -
    for bar in range(48, CREST):
        sec = sec_of(bar)
        for b in range(4):
            at = bar * 4.0 + b
            if sec == "slack":
                continue
            ch = E6_Y if b % 2 == 0 else E6_X
            if R5:
                ch = STORM_I if b % 2 == 0 else STORM_VI
            T["tide"].add(at, 0.9, ",".join(mtok(m) for m in ch), 66 if sec == "collision" else 72)
    T["tide"].add(80 * 4.0, 32.0 - 0.2, ",".join(mtok(m) for m in (STORM_I if R5 else E6_Y)), 80)  # the slack: frozen
    for i, bar in enumerate(range(CREST, 152, 2)):
        if R6:                                                               # E6 v3: D | C/D, the split moving
            split = [4, 5, 6, 7, 4, 3, 2, 1][i % 8]
            T["tide"].add(bar * 4.0, split - 0.1, ",".join(mtok(m) for m in E6V3_D), 70)
            T["tide"].add(bar * 4.0 + split, 8 - split - 0.1, ",".join(mtok(m) for m in E6V3_C), 66)
            continue
        T["tide"].add(bar * 4.0, 7.8, ",".join(mtok(m) for m in E6_X), 70)        # resolved: D only

    # ---- the bytebeat underneath the collision: one held note per bar lets the formula unfold -----------------------
    for bar in range(48, 80):
        T["byte"].add(bar * 4.0, 3.9, mtok(39 + 12 * (bar % 2)), 60)

    # ---- drums: a dusty break at 132-150, E2's seven on the ghost snares ----------------------------------------
    BREAKS = [((0, 10), (4, 12)), ((0, 3, 10), (4, 12)), ((0, 6, 10), (4, 13)), ((0, 10, 14), (4, 12))]
    for bar in range(16, 160):
        sec, b0 = sec_of(bar), bar * 4.0
        if sec == "slack":
            continue
        if sec == "plunge" and bar >= 156:
            continue
        ks, ss = BREAKS[0] if sec in ("approach",) and bar < 24 else rng.choice(BREAKS)
        if sec == "crest":
            ks, ss = BREAKS[(bar // 2) % 2]
        for s in ks:
            T["kick"].add(b0 + s / 4, 0.25, "k", 116 if s == 0 else 100)
        for s in ss:
            T["snare"].add(b0 + s / 4, 0.25, "s", 112)
        for s in range(16):
            if sec == "approach" and s % 2:
                continue
            T["hats"].add(b0 + s / 4, 0.1, "oh" if (s == 14 and sec == "crest") else "h",
                          (80 if s % 4 == 0 else 56) + rng.randint(0, 12))
        if sec in ("collision", "spiral") and rng.random() < 0.3:
            n = rng.choice([4, 6, 8])
            for j in range(n):
                T["perc"].add(b0 + 4.0 - (n - j) * 0.125, 0.1, "sn", 56 + 8 * j)
    for c in cycle_starts(7, 16 * 16, 152 * 16):                               # E2's seven on the ghosts
        if sec_of(int(c // 64)) == "slack":
            continue
        for h, (_, v) in E2_HITS.items():
            T["ghost"].add((c + h) / 4.0, 0.12, "rs" if h == 0 else "sn", v - 40)

    # ---- the infall: t6's Eb taken up, its tide lensed; the outfall thins to the E --------------------------------
    T["tide"].add(0.0, 32.0 - 0.2, ",".join(mtok(m) for m in (EB_MAJ7 if R6 else E6_Y)), 70)
    T["tide"].add(32.0, 32.0 - 0.2, ",".join(mtok(m) for m in (EB_MAJ7 if R6 else E6_Y)), 74)
    for c in cycle_starts(7, 4 * 16, 16 * 16):
        for h, (_, v) in E2_HITS.items():
            if rng.random() < 0.55:
                T["ghost"].add((c + h) / 4.0, 0.12, "rs", v - 54)
    T["riser"].add((CREST - 2) * 4.0, 8.0, "C4", 96)
    if R2:
        r2 = random.Random(29)
        lo, mid, hi = W9[0] * 4.0, 136 * 4.0, W9[1] * 4.0
        for k in ("kick", "snare", "hats", "perc"):
            T[k].ev = [e for e in T[k].ev if not (lo <= e[0] < hi)]
        T["ghost"].ev = [e if not (lo <= e[0] < mid) else (e[0], e[1], e[2], max(1, e[3] - 14), e[4]) for e in T["ghost"].ev]
        for bar in range(W9[0], 136):                                      # half time: the orbit's tidal lock
            b0 = bar * 4.0
            T["kick"].add(b0, 0.25, "k", 118)
            if bar % 2:
                T["kick"].add(b0 + 2.75, 0.25, "k", 92)
            T["snare"].add(b0 + 2.0, 0.25, "s", 116)
            for s in range(0, 16, 2):
                T["hats"].add(b0 + s / 4, 0.1, "oh" if s == 6 else "h", 74 if s % 4 == 0 else 52 + r2.randint(0, 10))
        for bar in range(136, W9[1]):                                      # the rebuild
            b0 = bar * 4.0
            ks, ss = ((0, 10), (4, 12)) if bar % 2 == 0 else ((0, 3, 10), (4, 12))
            for s in ks:
                T["kick"].add(b0 + s / 4, 0.25, "k", 116 if s == 0 else 100)
            for s in ss:
                T["snare"].add(b0 + s / 4, 0.25, "s", 112)
            for s in range(16):
                T["hats"].add(b0 + s / 4, 0.1, "h", (80 if s % 4 == 0 else 56) + r2.randint(0, 12))
            if bar >= 142:                                                 # the rush
                for s in range(16 if bar == 143 else 8):
                    st = (0 if bar == 143 else 2.0) + s / 4
                    T["perc"].add(b0 + st, 0.12, "sn", 50 + int(60 * ((bar - 142) * 16 + s) / 24))
        T["perc"].add(hi, 0.5, "oh", 112)
        for k in ("jet", "jethi"):                                         # the jet falls (retrograde) for 8 bars
            T[k].ev = [e for e in T[k].ev if not (lo <= e[0] < mid)]
        retro = list(reversed(E7_CREST if R5 else E7))
        for c in cycle_starts(E7_LEN16, W9[0] * 16, 136 * 16):
            at = c / 4.0
            if at < lo:
                continue
            for i, (nt, l16) in enumerate(retro):
                T["jet"].add(at, l16 / 4 * 0.9, mtok(midi(nt)), 108 - 4 * i)
                at += l16 / 4
    for bar in range(160, 168):                                               # the last pulse into t8
        T["kick"].add(bar * 4.0, 0.25, "k", 92 - 4 * (bar - 160))
    for bar in range(160, 172):
        for s in range(0, 16, 4):
            T["hats"].add(bar * 4.0 + s / 4, 0.1, "h", 54 - (bar - 160) * 2)
    if R14:                                                                   # w1: the head turns
        T["tide"].ev = [(e[0], e[1], e[2], 1, e[4]) if e[0] < 16 * 4.0 else e for e in T["tide"].ev]
        T["tide1"] = Track("tide1")
        for k, (bar, ch) in enumerate(HEAD_WHEEL):
            end = HEAD_WHEEL[k + 1][0] if k + 1 < len(HEAD_WHEEL) else 16
            T["tide1"].add(bar * 4.0, (end - bar) * 4.0 - 0.2, ",".join(mtok(m) for m in ch), 70 + 2 * k)
    if R12:                                                                   # w4: half time before the turn
        lo, hi = 60 * 4.0, 64 * 4.0
        for k in ("kick", "snare", "ghost", "hats", "perc"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
        T["kickh"], T["snareh"], T["hatsh"] = Track("kickh"), Track("snareh"), Track("hatsh")
        for bar in range(60, 64):
            b0 = bar * 4.0
            T["kickh"].add(b0, 0.25, "k", 118)
            T["kickh"].add(b0 + 1.75, 0.25, "k", 84)
            T["snareh"].add(b0 + 2.0, 0.25, "s", 116)
            for i in range(8):
                T["hatsh"].add(b0 + i * 0.5, 0.1, "h" if i % 2 == 0 else "oh", 70 if i % 2 == 0 else 60)
    if R11:                                                                   # w2: the storm in two steps
        lo, hi = 16 * 4.0, 24 * 4.0
        T["bassup"], T["drop"] = Track("bassup"), Track("drop")
        for e in T["bass"].ev:
            if lo <= e[0] < hi:
                T["bassup"].add(e[0], e[1], mtok(int(float(e[2][1:])) + 12), e[3] - 12)
        for k in ("sub",):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
        T["kick"].ev = [(e[0], e[1], e[2], 1, e[4]) if 23 * 4.0 <= e[0] < hi else e for e in T["kick"].ev]
        T["drop"].add(22 * 4.0, 8.0, "C4", 90)
    if R9:                                                                    # w3: a way into the collision
        T["kick"].ev = [(e[0], e[1], e[2], 1, e[4]) if 47 * 4.0 <= e[0] < 48 * 4.0 else e for e in T["kick"].ev]
        T["roll"] = Track("roll")
        for bar, step in ((44, 0.5), (45, 0.5), (46, 0.25)):
            n = int(4 / step)
            for i in range(n):
                prog = ((bar - 44) * 4 + i * step) / 12.0
                T["roll"].add(bar * 4.0 + i * step, step * 0.8, "s", 46 + 46 * prog)
        for i in range(16):                                                   # bar 48: snare and tom, crescendo
            at = 47 * 4.0 + i * 0.25
            head = "t" if i % 4 in (2, 3) and i < 12 else "s"
            T["roll"].add(at, 0.2, head, 92 + i)
            if i >= 12:
                T["roll"].add(at + 0.125, 0.1, "s", 96 + i)
        T["roll"].add(48 * 4.0, 1.0, "oh", 112)
        T["roll"].add(48 * 4.0, 0.25, "cp", 110)
    if R8:                                                                    # w5: i - VI - III - VII, twice
        lo, hi = 64 * 4.0, 80 * 4.0
        for k in ("tide", "bass", "e4"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
        for k in ("tide5", "bass5", "e4w5"):
            T[k] = Track(k)
        for bar in range(64, 80):
            root, ch = W5_PROG[((bar - 64) // 2) % 4]
            second = bar >= 72
            step = 0.5 if second else 1.0
            for i in range(int(4 / step)):
                T["tide5"].add(bar * 4.0 + i * step, step * 0.9, ",".join(mtok(m) for m in ch), (70 if i % 2 == 0 else 60) if second else 68)
            for i in range(8):
                m = root + (12 if i in (2, 6) else 0) + (7 if i == 7 else 0)
                T["bass5"].add(bar * 4.0 + i * 0.5, 0.42, mtok(m), 108 if i % 4 == 0 else 94)
            for off in (1.5, 3.5):
                T["e4w5"].add(bar * 4.0 + off, 0.35, ",".join(mtok(m + 12) for m in ch[1:]), 84 if off == 1.5 else 76)
    if R20:                                                                   # w7: the spiral turns (bars 101-112)
        lo, hi = 100 * 4.0, 112 * 4.0
        for k in ("tide", "bass", "e4"):
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
        for k in ("jet", "jethi"):                                            # Cbmaj7 bars: C -> Cb, G -> Gb
            T[k].ev = [(e[0], e[1], mtok(int(float(e[2][1:])) - 1), e[3], e[4])
                       if 104 * 4.0 <= e[0] < 108 * 4.0 and e[2].startswith("m") and int(float(e[2][1:])) % 12 in (0, 7)
                       else e for e in T[k].ev]
        for k in ("tide7", "bass7", "e4w7"):
            T[k] = Track(k)
        for bar in range(100, 112):
            root, ch = [(r, c) for b0, r, c in SPIRAL_PROG if b0 <= bar][-1]
            step = 1.0 if bar < 104 else 0.5 if bar < 108 else 0.25
            for i in range(int(4 / step)):
                T["tide7"].add(bar * 4.0 + i * step, step * 0.9, ",".join(mtok(m) for m in ch), 66 if i % 2 == 0 else 58)
            for i in range(8):
                m = root + (12 if i in (2, 6) else 0)
                T["bass7"].add(bar * 4.0 + i * 0.5, 0.42, mtok(m), 98 if i % 4 == 0 else 86)
            if bar >= 104:
                for off in (1.5, 3.5):
                    T["e4w7"].add(bar * 4.0 + off, 0.35, ",".join(mtok(m + 12) for m in ch[1:]), 82 if off == 1.5 else 74)
    if R26:                                                                   # w8: the key turns (bars 117-120)
        lo, hi = 116 * 4.0, 120 * 4.0
        for k in ("tide", "bass", "sub", "e4", "jet", "jethi", "e5", "e1a", "e1b", "e1c", "tide7", "bass7", "e4w7"):
            if k not in T:
                continue
            T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else
                       (e[0], max(0.03, round(lo - e[0] - 0.05, 4)), e[2], e[3], e[4]) if e[0] < lo < e[0] + e[1] else e
                       for e in T[k].ev]
        for k in ("tide8", "bass8", "sub8", "e4w8"):
            T[k] = Track(k)
        for bar in range(116, 120):
            root, sroot, ch = [(r, s, c) for b0, r, s, c in TURN if b0 <= bar][-1]
            for i in range(8):
                T["tide8"].add(bar * 4.0 + i * 0.5, 0.45, ",".join(mtok(m) for m in ch), 66 if i % 2 == 0 else 58)
                m = root + (12 if i in (2, 6) else 0)
                T["bass8"].add(bar * 4.0 + i * 0.5, 0.42, mtok(m), 98 if i % 4 == 0 else 86)
            for off in (1.5, 3.5):
                T["e4w8"].add(bar * 4.0 + off, 0.35, ",".join(mtok(m + 12) for m in ch[1:]), 82 if off == 1.5 else 74)
        for b0, b1, s in ((116, 118, 27), (118, 120, 33)):
            T["sub8"].add(b0 * 4.0, (b1 - b0) * 4.0 - 0.1, mtok(s), 70)
    if R30:                                                                   # the floor lifts (45-48, 61-64)
        def up(keys, lo, hi):
            for k in keys:
                if k in T:
                    T[k].ev = [(e[0], e[1], ",".join(mtok(int(float(p[1:])) + 12) if p.startswith("m") else p
                                                      for p in e[2].split(",")), e[3], e[4])
                               if lo <= e[0] < hi and isinstance(e[2], str) else e for e in T[k].ev]
        for b in (44, 56) + ((148,) if R31 else ()):
            up(("bass", "sub", "bass5", "bass7"), b * 4.0, (b + 4) * 4.0)
        for lo, hi in ((44 * 4.0, 48 * 4.0), (56 * 4.0, 60 * 4.0)) + (((148 * 4.0, 152 * 4.0),) if R31 else ()):
            for k in ("kick", "snare", "ghost", "perc"):
                if k in T:
                    T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else e for e in T[k].ev]
            T["hats"].ev = [(e[0], e[1], e[2], 1, e[4]) if (lo <= e[0] < hi and round(e[0] * 4) % 2 == 1) else e
                            for e in T["hats"].ev]
    if R29:                                                                   # the band makes room (25-28, 137-140)
        for lo, hi, ks in ((24 * 4.0, 28 * 4.0, ("kick", "snare", "ghost", "bass", "sub")),
                           (136 * 4.0, 140 * 4.0, ("kick", "bass", "sub"))):
            for k in ks:
                if k in T:
                    T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else
                               (e[0], max(0.03, round(lo - e[0] - 0.05, 4)), e[2], e[3], e[4]) if e[0] < lo < e[0] + e[1]
                               else e for e in T[k].ev]
    if R27:                                                                   # air: shaker under storm/spiral, ride on the crest
        r27 = random.Random(27)
        hat_bars = {int(e[0] // 4) for e in T["hats"].ev if e[3] > 1}
        T["shaker"], T["ride"] = Track("shaker"), Track("ride")
        for bar in sorted(hat_bars):
            if 16 <= bar < 80 or 88 <= bar < 116:
                for s in range(16):
                    v = (58 if s % 4 in (1, 3) else 44) + r27.randint(0, 8) + (bar - 16) // 8
                    T["shaker"].add(bar * 4.0 + s / 4.0, 0.12, "sh", v)
            elif 120 <= bar < 152:
                for s in range(0, 16, 2):
                    v = (84 if s % 4 == 0 else 62) + r27.randint(0, 6)
                    T["ride"].add(bar * 4.0 + s / 4.0, 1.6, "m62", v)
    if R42:                                                                   # the orbit breathes (37-40, 96-100, 141-144)
        for b0, b1 in ((36, 40), (95, 100), (140, 144)):
            for k in ("bass", "bass5", "bass7", "bass8"):
                if k not in T:
                    continue
                ev = T[k].ev
                hold = {}
                for i, e in enumerate(ev):
                    if b0 * 4.0 <= e[0] < b1 * 4.0 and e[3] > 1 and str(e[2]).startswith("m"):
                        h = int(e[0] // 2)
                        j = hold.get(h)
                        if j is None or int(float(e[2][1:])) < int(float(ev[j][2][1:])):
                            hold[h] = i
                keep = {i: h for h, i in hold.items()}
                T[k].ev = [(e[0], round((keep[i] + 1) * 2.0 - e[0] - 0.1, 4), e[2], e[3], e[4]) if i in keep else
                           (e[0], e[1], e[2], 1, e[4]) if b0 * 4.0 <= e[0] < b1 * 4.0 else e for i, e in enumerate(ev)]
    if R41:                                                                   # the floor holds its breath (125-130)
        firsts = {}
        for i, e in enumerate(T["bass"].ev):
            b = int(e[0] // 4)
            if 124 <= b < 130 and e[3] > 1 and (b not in firsts or e[0] < T["bass"].ev[firsts[b]][0]):
                firsts[b] = i
        keep = set(firsts.values())
        T["bass"].ev = [(e[0], round((int(e[0] // 4) + 1) * 4.0 - e[0] - 0.15, 4), mtok(38), e[3], e[4]) if i in keep else
                        (e[0], e[1], e[2], 1, e[4]) if 124 * 4.0 <= e[0] < 130 * 4.0 else e for i, e in enumerate(T["bass"].ev)]
    if R40:                                                                   # w5: the orbit loses energy (77-80)
        for b0, ks in ((76, ("hats", "hatsw", "shaker")), (77, ("snare", "ghost", "ghostw", "perc")),
                       (78, ("e1a", "e1b", "e1c", "e1aw", "e1bw", "e1cw", "e5", "e5w")), (79, ("kick",))):
            lo, hi = b0 * 4.0, 80 * 4.0
            for k in ks:
                if k in T:
                    T[k].ev = [(e[0], e[1], e[2], 1, e[4]) if lo <= e[0] < hi else
                               (e[0], max(0.03, round(lo - e[0] - 0.05, 4)), e[2], e[3], e[4]) if e[0] < lo < e[0] + e[1]
                               else e for e in T[k].ev]
    if R49:                                                 # w5: the collision stops dead (bars 69-70, stop-time)
        lo, hi, keep = 68 * 4.0, 70 * 4.0, (272.0, 273.5, 276.0, 277.5)
        sil = ("ghost", "shaker", "perc", "ghostw", "hatsw")

        def stop(k, e):
            if lo <= e[0] < hi:
                if k not in sil and any(abs(e[0] - p) < 1e-3 for p in keep):
                    return (e[0], min(e[1], 0.4), e[2], e[3], e[4])
                return (e[0], e[1], e[2], 1, e[4])
            if e[0] < lo < e[0] + e[1] and e[3] > 1:
                return (e[0], max(0.03, round(lo - e[0] - 0.05, 4)), e[2], e[3], e[4])
            return e
        for k in T:
            T[k].ev = [stop(k, e) for e in T[k].ev]
    if R53:                                                 # w9: the machinery stops (137-140), then reassembles
        lo = 136 * 4.0
        back = {"ride": 140, "ghost": 140, "e4": 141, "e4w5": 141, "e1c": 142, "e1a": 142, "e1b": 143, "e5": 143}

        def clear(k, e):
            hi = back[k] * 4.0
            if lo <= e[0] < hi:
                return (e[0], e[1], e[2], 1, e[4])
            if e[0] < lo < e[0] + e[1] and e[3] > 1:
                return (e[0], max(0.03, round(lo - e[0] - 0.05, 4)), e[2], e[3], e[4])
            return e
        for k in back:
            T[k].ev = [clear(k, e) for e in T[k].ev]
    if R55:                                                 # w11: the kick gives way to the last heartbeat
        T["kick"].ev = [(e[0], e[1], e[2], 1, e[4]) if 640.0 <= e[0] < 704.0 else e for e in T["kick"].ev]
    return T


def voice_tracks():
    out = []
    for f, place in (("lap_eb.json", [(56, "frag"), (66, "frag"), (82, "whole"), (85, "whole")]),
                     ("lap.json", [(124, "whole"), (132, "whole"), (140, "whole"), (148, "whole")])):
        src = json.load(open(os.path.join(HERE, "t7", f)))["tracks"][:3]
        for k, tr in enumerate(src):
            notes = []
            for bar, how in place:
                for i, n in enumerate(tr["notes"]):
                    if how == "frag" and i not in ((0, 1) if bar == 56 else (2, 3, 4)):
                        continue
                    d = {"at": round(bar * 4.0 + n["at"], 4), "len": n["len"], "ph": n["ph"], "pitch": n["pitch"],
                         "vel": n["vel"]}
                    if n.get("expr_path"):
                        d["expr_path"] = n["expr_path"]
                    notes.append(d)
            out.append((f"{'eb' if 'eb' in f else 'd'}{k}", tr, notes))
    return out


def main():
    T = build()
    tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": "64b", "bpm": SEAM_IN},
             {"at": f"{160 * 4}b", "bpm": SEAM_OUT, "ramp": True}]
    dyn = [["0b", -4.0], ["64b", -2.0], ["191.99b", -1.5], ["192b", 0.0], ["319.99b", 0.0], ["320b", -4.0],
           ["351.99b", -3.0], ["352b", -1.0], ["479.99b", 0.0], ["480b", 1.0], ["607.99b", 1.0], ["608b", -1.0],
           ["640b", -2.0], ["704b", -4.0]]
    if R38:                                                 # one arc to the hardest crest
        dyn = [["0b", -4.0], ["64b", -4.0], ["191.99b", -3.5], ["192b", -3.5], ["319.99b", -3.5], ["320b", -6.5],
               ["351.99b", -5.5], ["352b", -4.0], ["479.99b", -1.0], ["480b", 1.0], ["607.99b", 1.0], ["608b", -1.0],
               ["640b", -2.0], ["704b", -4.0]]
    glitch = [["0b", 0.0], ["64b", 0.1], ["192b", 0.35], ["319b", 0.45], ["320b", 0.0], ["352b", 0.25], ["479b", 0.1],
              ["480b", 0.0], ["704b", 0.0]]
    grit = [["0b", 0.0], ["64b", 0.15], ["192b", 0.5], ["320b", 0.0], ["352b", 0.4], ["479b", 0.2], ["480b", 0.0],
            ["704b", 0.0]]
    close = [["0b", 0.0], ["640b", 0.0], ["704b", -2.0]]
    stop = [["0b", 0.0], ["623.99b", 0.0], ["624b", 1.0], ["626b", 1.0], ["626.01b", 0.0]]

    def storm(extra=()):
        return [{"type": "stutter", "slice": "1/16", "repeats": 3,
                 "chance": {"value": 0, "mod": [{"src": "auto.glitch", "amount": 1}]}},
                {"type": "crush", "bits": 7, "rate": "12kHz", "mix": {"value": 0, "mod": [{"src": "auto.grit", "amount": 1}]}}] + list(extra)

    if R7:
        glitch = [[p, round(v * 0.6, 3)] for p, v in glitch]
        grit = [[p, round(v * 0.5, 3)] for p, v in grit]
    if R25:                                                                  # the crusher retires
        grit = [[p, 0.0] for p, v in grit]
    lanes = {"glitch": {"points": glitch}, "grit": {"points": grit}}
    tracks = [
        {"name": "kick", "patch": "dusty-kit", "gain": "0dB", "fx": storm(), "auto": lanes, "score": T["kick"].score()},
        {"name": "snare", "patch": "dusty-kit", "gain": "-3dB", "fx": storm(), "auto": lanes, "score": T["snare"].score()},
        {"name": "ghost", "patch": "dusty-kit", "gain": "-9dB", "pan": -0.15, "score": T["ghost"].score()},
        {"name": "hats", "patch": "dusty-kit", "gain": "-10dB", "pan": 0.2, "fx": storm(), "auto": lanes,
         "score": T["hats"].score()},
        {"name": "perc", "patch": "dusty-kit", "gain": "-9dB", "pan": 0.1, "score": T["perc"].score()},
        {"name": "bass", "patch": "a7-reese", "gain": "-2.5dB", "fx": storm(), "auto": lanes, "score": T["bass"].score()},
        {"name": "sub", "patch": "sub", "gain": "-10dB", "score": T["sub"].score()},
        {"name": "e1a", "patch": "vosim-bell", "gain": "-14dB", "pan": -0.3, "sends": {"space": "-8dB"},
         "score": T["e1a"].score()},
        {"name": "e1b", "patch": "a7-gb", "gain": "-18dB", "pan": 0.35, "fx": ["delay time=3/16 mix=0.18 feedback=0.3"],
         "score": T["e1b"].score()},
        {"name": "e1c", "patch": "modal-bell", "gain": "-13dB", "pan": 0.0, "sends": {"space": "-6dB"},
         "score": T["e1c"].score()},
        {"name": "hold", "patch": "ambient-swell" if R10 else "sub", "gain": "-8dB", "score": T["hold"].score()},
        {"name": "e4", "patch": "cz-pad", "gain": "-16dB", "fx": storm(), "auto": lanes, "sends": {"space": "-10dB"},
         "score": T["e4"].score()},
        {"name": "e5", "patch": "a7-gb", "gain": "-17dB", "pan": -0.4, "score": T["e5"].score()},
        {"name": "tide", "patch": "a7-tide", "gain": "-15dB", "sends": {"space": "-6dB"}, "score": T["tide"].score()},
        {"name": "jet", "patch": "a7-jet", "gain": "-12dB", "pan": 0.15, "fx": ["delay time=1/8 mix=0.15 feedback=0.3"],
         "sends": {"space": "-8dB"}, "score": T["jet"].score()},
        {"name": "jethi", "patch": "nes-pulse-lead", "gain": "-20dB", "pan": -0.2, "score": T["jethi"].score()},
        {"name": "byte", "patch": "bytebeat-chip", "gain": "-26dB", "fx": ["hp cutoff=400"], "score": T["byte"].score()},
        {"name": "riser", "patch": "fx-riser", "gain": "-10dB", "score": T["riser"].score()},
    ]
    patches = dict(PATCHES)
    if R3:
        cols = [[[1, 1.0]]]
        for h, g in ((3, 0.7), (9, 0.55), (27, 0.42), (81, 0.3), (243, 0.2)):
            cols.append(cols[-1] + [[h, g]])
        patches["a7-column"] = {"about": "chirper-two: the jet's column inside one sound - a wavetable whose six frames add the "
                                         "harmonics 1, 3, 9, 27, 81, 243 (each a fifth and an octave above the last), "
                                         "scanned upward by an envelope on every note",
                                "synth": {"layers": [{"type": "wavetable", "frames": cols,
                                                      "position": {"value": 0.0, "mod": [{"src": "env.burn", "amount": 1.0}]}}],
                                          "env": {"burn": {"a": "140ms", "d": "0ms", "s": 1.0, "r": "60ms"}},
                                          "filters": ["hp cutoff=250", "lp cutoff=9000 q=0.6"],
                                          "amp": {"a": "2ms", "d": "250ms", "s": 0.55, "r": "120ms"}}}
        patches["a7-floor"] = {"about": "chirper-two: the inner orbit's floor - a sine with its octave (-9 dB), a slow swell and "
                                        "a little drive, low-passed: a floor that breathes in rather than sits",
                               "synth": {"layers": [{"wave": "sine"}, {"wave": "sine", "ratio": 2, "level": "-9dB"}],
                                         "drive": 0.15, "filters": ["lp cutoff=240 q=0.6"],
                                         "amp": {"a": "350ms", "d": "0ms", "s": 1.0, "r": "450ms"}}}
        T["sub"].ev = [(e[0], e[1], e[2], int(e[3] * (0.45 if e[0] < 64 else min(1.0, 0.45 + 0.55 * (e[0] - 64) / 96.0))), e[4])
                       for e in T["sub"].ev]
        for tr in tracks:
            if tr["name"] == "jethi":
                tr.update(patch="a7-column", gain="-17dB", score=T["jethi"].score())
            if tr["name"] == "sub":
                tr.update(patch="a7-floor", gain="-9dB", score=T["sub"].score())
    if R4:
        lo, hi = 96 * 4.0, 112 * 4.0
        lift = {"e1a": (96, 9), "e1b": (96, 10), "e1c": (96, 7), "e5": (100, 11), "e4": (104, 17), "hats": (104 + 4, 15),
                "ghost": (108, 10)}

        def db(g):
            return float(g.replace("dB", ""))
        spec = {tr["name"]: tr for tr in tracks}
        for k, (start, boost) in lift.items():
            a = start * 4.0
            moved = [e for e in T[k].ev if a <= e[0] < hi]
            T[k].ev = [e for e in T[k].ev if not (a <= e[0] < hi)]
            if k == "e5":
                moved = [(e[0], e[1], mtok(float(e[2][1:]) + 12), e[3], e[4]) for e in moved]
            w = Track(k + "w")
            w.ev = moved
            if k == "hats":
                for bar in range(108, 112):
                    for b in range(4):
                        for j in range(2):
                            w.add(bar * 4.0 + b + 0.75 + j * 0.125, 0.06, "h", 60 + 10 * j)
            spec[k]["score"] = T[k].score()
            nw = dict(spec[k], name=k + "w", gain=f"{db(spec[k]['gain']) + boost:g}dB", score=w.score())
            tracks.append(nw)
        X, Y = ",".join(mtok(m) for m in E6_X), ",".join(mtok(m) for m in E6_Y)
        if R5:
            X, Y = ",".join(mtok(m) for m in STORM_VI), ",".join(mtok(m) for m in STORM_I)
        T["tide"].ev = [e if not (lo <= e[0] < 104 * 4.0) else (e[0], e[1], e[2], int(e[3] * 0.7), e[4])
                        for e in T["tide"].ev if not (104 * 4.0 <= e[0] < hi)]
        for bar in range(104, 112):
            step = 0.5 if bar < 108 else 0.25
            for i in range(int(4 / step)):
                T["tide"].add(bar * 4.0 + i * step, step * 0.92, Y if i % 2 == 0 else X, 48)
        T["bass"].ev = [e if not (lo <= e[0] < hi) else (e[0], e[1], e[2], int(e[3] * 0.72), e[4]) for e in T["bass"].ev]
        spec["tide"]["score"] = T["tide"].score()
        spec["bass"]["score"] = T["bass"].score()
    if R2:
        cv = json.load(open(os.path.join(HERE, "t7", "corner.json")))["tracks"][0]
        vnotes = []
        for bar in (130, 134):
            for n in cv["notes"]:
                d = {"at": round(bar * 4.0 + n["at"], 4), "len": n["len"], "ph": n["ph"], "pitch": n["pitch"], "vel": n["vel"]}
                if n.get("expr_path"):
                    d["expr_path"] = n["expr_path"]
                vnotes.append(d)
        vfx = [dict(cv["fx"][0], notes="D2,A2,E3,A3,D4" if R5 else "D2,A2,E3,G#3,C#4", mix=0.62), "lp cutoff=5000", "chorus mix=0.25",
               "delay time=3/8 mix=0.2 feedback=0.3"]
        patches["a7-vocoder-voice"] = cv["patch"]
    for name, tr, notes in voice_tracks():
        if R2 and name.startswith("d"):
            notes = [n for n in notes if not (W9[0] * 4.0 <= n["at"] < 136 * 4.0)]
        p = tr["patch"]
        if not isinstance(p, str):
            patches["a7-voice"] = p
            p = "a7-voice"
        if R10:
            k = name[-1]
            p = f"a7-choir{k}"
            patches[p] = {"extends": f"voice-legato synth.layers.0.tract={CHOIR_TRACT[k]} synth.layers.0.breath=0.25 "
                                     "synth.layers.0.ring=0.35" + (" synth.layers.0.even=1" if R13 else ""),
                          "synth": {"pitch": {"mod": [{"amount": 0.01, "src": "expr.f0"}], "value": 0}}}
        tracks.append({"name": f"v{name}", "patch": p, "gain": tr.get("gain", "0dB"), "pan": tr.get("pan", 0.0),
                       "fx": ["chorus", "delay time=1/4 mix=0.15 feedback=0.25"], "sends": {"space": "-6dB"},
                       "notes": notes})
    if R2 and not R13:
        tracks.append({"name": "vocoder", "patch": "a7-vocoder-voice", "gain": "3dB", "pan": 0.0, "fx": vfx,
                       "sends": {"space": "-8dB"}, "notes": vnotes})
    if R13:                                                   # the singer finishes the line at the tidal lock
        cs = json.load(open(os.path.join(HERE, "t7", "sung_crest.json")))["tracks"][0]
        base = ("voice-legato synth.layers.0.tract=1.06 synth.layers.0.ring=0.4 synth.layers.0.breath=0.2 "
                "synth.layers.0.even=1")
        patches["a7-sungc"] = dict(cs["patch"], extends=base)
        patches["a7-sungc5"] = dict(cs["patch"], extends=base + (" synth.layers.0.harmony=[2] synth.layers.0.harmony_key=D:mixolydian"
                                                                  if R15 else " synth.layers.0.harmony=[7]"))
        for name, bar, patch in (("sungc", SUNGC_BARS[0], "a7-sungc"), ("sungc5", SUNGC_BARS[1], "a7-sungc5")):
            nn = []
            for n in cs["notes"]:
                d = {"at": round(bar * 4.0 - 0.25 + n["at"], 4), "len": n["len"], "ph": n["ph"], "pitch": n["pitch"],
                     "vel": n["vel"]}
                if n.get("expr_path"):
                    d["expr_path"] = n["expr_path"]
                nn.append(d)
            tracks.append({"name": name, "patch": patch, "gain": "1dB", "pan": 0.0,
                           "fx": ["delay time=3/8 mix=0.16 feedback=0.3"], "sends": {"space": "-7dB"}, "notes": nn})
    if R6:
        for tr in tracks:
            if tr["name"] in ("e1a", "e1aw"):
                tr["patch"] = "dx-epiano"
            if tr["name"] in ("e1c", "e1cw"):
                tr["patch"] = "scanned-mallet"
        # the tail keeps the modal bell (from the plunge on: its hum carries the seam's 60-100 Hz, and its E is the handover)
        tail = Track("e1ctail")
        tail.ev = [e for e in T["e1c"].ev if e[0] >= 152 * 4.0]
        T["e1c"].ev = [e for e in T["e1c"].ev if e[0] < 152 * 4.0]
        spec = {tr["name"]: tr for tr in tracks}
        spec["e1c"]["score"] = T["e1c"].score()
        tracks.append(dict(spec["e1c"], name="e1ctail", patch="modal-bell", score=tail.score()))
    if R5:
        hook = Track("hook")
        rests = [(124 * 4.0, 124 * 4.0 + 6), (128 * 4.0, 136 * 4.0), (140 * 4.0, 140 * 4.0 + 6), (148 * 4.0, 148 * 4.0 + 6)]
        for c in cycle_starts(20, CREST16, 152 * 16):
            at = c / 4.0
            if at < CREST * 4 or any(a <= at < b for a, b in rests):
                continue
            for nt, ln in E1:
                hook.add(at, ln * 0.92, mtok(midi(nt) + 12), 92 if nt == "D4" else 84)
                at += ln
        if R7:                                              # the hook in the storm: E1 in E-flat minor, plainly
            for bar in (16, 32, 48, 72):
                at = bar * 4.0
                for _ in range(2):
                    for nt, ln in E1:
                        v = 1 if (R9 and bar in SUNG7_BARS) else (90 if nt == "D4" else 82)
                        hook.add(at, ln * 0.92, mtok(midi(nt) + 13), v)
                        at += ln
        patches["a7-hook"] = {"about": "chirper-two: the crest's hook - two saws 8 cents apart over a quiet square, a "
                                       "gentle low-pass, mono with a short glide: a plain singing lead for E1, stated upright",
                              "synth": {"layers": [{"wave": "saw", "detune": -4}, {"wave": "saw", "detune": 4},
                                                   {"wave": "square", "level": "-10dB"}],
                                        "filters": ["lp cutoff=3200 q=0.7"],
                                        "amp": {"a": "8ms", "d": "220ms", "s": 0.75, "r": "180ms"}},
                              "play": {"mono": True, "glide": "25ms"}}
        if R17:
            horns = Track("horns")
            for bar in range(CREST, 152, 2):
                if 128 <= bar < 136:
                    continue
                at = bar * 4.0
                for ch, ln in HORN_CHORDS:
                    v = 1 if (R25 and 144 <= bar < 148) else (84 if ln == 4.0 else 76)
                    horns.add(at, ln * 0.96, ",".join(mtok(m) for m in ch), v)
                    at += ln
            tracks.append({"name": "horns", "patch": "horn", "gain": "-8dB", "pan": -0.1,
                           "sends": {"space": "-5dB"}, "score": horns.score()})
        if R16:                                                # an octave down, into the horns' middle
            hook.ev = [(e[0], e[1], mtok(int(float(e[2][1:])) - 12), e[3], e[4]) for e in hook.ev]
        tracks.append({"name": "hook", "patch": "horn-section" if R16 else "a7-hook", "gain": "-1dB" if R16 else "-9dB",
                       "pan": 0.05, "fx": ["delay time=3/8 mix=0.18 feedback=0.3"], "sends": {"space": "-8dB"},
                       "score": hook.score()})
    if R7:
        adj = {"bass": -4.5, "sub": -3.0, "tide": -4.0, "kick": -2.0, "e1a": 8.0, "e1b": 6.0, "e1c": 7.0, "e4": 10.0,
               "hats": 10.0, "ghost": 6.0, "e5": 4.0}
        for tr in tracks:
            if tr["name"] in adj:
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + adj[tr['name']]:g}dB"
        tracks[:] = [tr for tr in tracks if tr["name"] != "byte"]
    if R14:
        spec = {tr["name"]: tr for tr in tracks}
        tracks.append(dict(spec["tide"], name="tide1", score=T["tide1"].score()))
    if R15:
        bow = Track("bow")
        for bar, m, ln in BOW_LINE:
            bow.add(bar * 4.0, ln, mtok(m), 84 + (bar - 128))
        at = 138 * 4.0
        for _ in range(2):                                                    # E1 stretched x2, twice
            for nt, ln in E1:
                if at < 141 * 4.0:
                    bow.add(at, ln * 2 * 0.97, mtok(midi(nt)), 90)
                at += ln * 2
        bow.add(141 * 4.0, 12.0 - 0.3, mtok(69), 98)                          # A4 up through the rush
        tracks.append({"name": "bow", "patch": "erhu", "gain": "-6dB", "pan": -0.15,
                       "fx": ["delay time=3/8 mix=0.12 feedback=0.25"], "sends": {"space": "-6dB"}, "score": bow.score()})
    if R12:
        spec = {tr["name"]: tr for tr in tracks}
        for new, old in (("kickh", "kick"), ("snareh", "snare"), ("hatsh", "hats")):
            tracks.append(dict(spec[old], name=new, score=T[new].score()))
        if R9:
            src5 = json.load(open(os.path.join(HERE, "t7", "sung.json")))["tracks"][0]
            patches["a7-sung5"] = dict(src5["patch"], extends="voice-legato synth.layers.0.tract=1.06 "
                                                             "synth.layers.0.ring=0.4 synth.layers.0.breath=0.2 "
                                                             "synth.layers.0.even=1 " + (
                                                                 "synth.layers.0.harmony=[2] synth.layers.0.harmony_key=Eb:minor"
                                                                 if R18 else "synth.layers.0.harmony=[-7]"))
            n5 = []
            for bar in SUNG5_BARS:
                for n in src5["notes"]:
                    d = {"at": round(bar * 4.0 - 0.25 + n["at"], 4), "len": n["len"], "ph": n["ph"],
                         "pitch": n["pitch"], "vel": n["vel"]}
                    if n.get("expr_path"):
                        d["expr_path"] = n["expr_path"]
                    n5.append(d)
            tracks.append({"name": "sung5", "patch": "a7-sung5", "gain": "-1dB", "pan": 0.0,
                           "fx": ["delay time=3/8 mix=0.14 feedback=0.3"], "sends": {"space": "-7dB"}, "notes": n5})
    if R11:
        spec = {tr["name"]: tr for tr in tracks}
        tracks.append(dict(spec["bass"], name="bassup", fx=list(spec["bass"].get("fx", [])) + ["hp cutoff=170"],
                           score=T["bassup"].score()))
        tracks.append(dict(spec["riser"], name="drop", score=T["drop"].score()))
    if R9:
        spec = {tr["name"]: tr for tr in tracks}
        tracks.append(dict(spec["snare"], name="roll", score=T["roll"].score()))
        src = json.load(open(os.path.join(HERE, "t7", "sung.json")))["tracks"][0]
        patches["a7-sung"] = dict(src["patch"], extends="voice-legato synth.layers.0.tract=1.06 synth.layers.0.ring=0.4 "
                                                        "synth.layers.0.breath=0.2" + (" synth.layers.0.even=1" if R13 else ""))
        notes = []
        for bar in SUNG7_BARS:
            for n in src["notes"]:
                d = {"at": round(bar * 4.0 - 0.25 + n["at"], 4), "len": n["len"], "ph": n["ph"], "pitch": n["pitch"],
                     "vel": n["vel"]}
                if n.get("expr_path"):
                    d["expr_path"] = n["expr_path"]
                notes.append(d)
        tracks.append({"name": "sung", "patch": "a7-sung", "gain": "0dB", "pan": 0.0,
                       "fx": ["delay time=3/8 mix=0.12 feedback=0.25"], "sends": {"space": "-8dB"}, "notes": notes})
        if R18:                                            # the spiral: alone at 105, a keyed third above at 113
            patches["a7-sung3"] = dict(patches["a7-sung"], extends=patches["a7-sung"]["extends"] +
                                       " synth.layers.0.harmony=[2] synth.layers.0.harmony_key=Eb:minor")
            for name, patch, bar in (("sungs", "a7-sung", SPIRAL_SUNG[0]), ("sungs3", "a7-sung3", SPIRAL_SUNG[1])):
                ns = []
                for n in src["notes"]:
                    d = {"at": round(bar * 4.0 - 0.25 + n["at"], 4), "len": n["len"], "ph": n["ph"],
                         "pitch": n["pitch"], "vel": n["vel"]}
                    if n.get("expr_path"):
                        d["expr_path"] = n["expr_path"]
                    ns.append(d)
                tracks.append({"name": name, "patch": patch, "gain": "0dB", "pan": 0.0,
                               "fx": ["delay time=3/8 mix=0.14 feedback=0.3"], "sends": {"space": "-7dB"}, "notes": ns})
    if R8:
        spec = {tr["name"]: tr for tr in tracks}
        for new, old in (("tide5", "tide"), ("bass5", "bass"), ("e4w5", "e4")):
            tracks.append(dict(spec[old], name=new, score=T[new].score()))
    if R20:
        spec = {tr["name"]: tr for tr in tracks}
        for new, old in (("tide7", "tide"), ("bass7", "bass"), ("e4w7", "e4")):
            tracks.append(dict(spec[old], name=new, score=T[new].score()))
    if R26:                                                 # w8: the key turns - band, horn choir and brass
        spec = {tr["name"]: tr for tr in tracks}
        for new, old in (("tide8", "tide"), ("bass8", "bass"), ("sub8", "sub"), ("e4w8", "e4")):
            tracks.append(dict(spec[old], name=new, score=T[new].score()))
        turnh, turnb = Track("turnh"), Track("turnb")
        for b0, ln, ch in ((116, 8.0, (51, 55, 58, 63)), (118, 4.0, (52, 55, 57, 62)), (119, 4.0, (52, 55, 57, 61))):
            turnh.add(b0 * 4.0, ln * 0.97, ",".join(mtok(m) for m in ch), 80 if b0 == 116 else 86)
        at = 116 * 4.0
        for nt, ln in [("Eb4", 0.5), ("Bb4", 0.75), ("Db5", 0.25), ("Ab4", 1.0), ("F4", 1.0), ("Eb4", 4.5),
                       ("A4", 1.5), ("G4", 1.5), ("E4", 1.0), ("E4", 1.0), ("C#4", 3.0)]:
            turnb.add(at, ln * 0.92, mtok(midi(nt)), 92 if ln >= 1.5 else 84)
            at += ln
        tracks.append(dict(spec["horns"] if "horns" in spec else spec["hook"], name="turnh", gain="-7dB",
                           score=turnh.score()))
        tracks.append(dict(spec["hook"], name="turnb", score=turnb.score()))
    if R23:
        spec = {tr["name"]: tr for tr in tracks}
        stabs, boom = Track("stabs"), Track("boom")
        for bar in STAB_BARS:
            for off, v in ((1.5, 84), (3.5, 78)):
                stabs.add(bar * 4.0 + off, 0.3, ",".join(mtok(m) for m in (54, 58, 63)), v)
        boom.add(48 * 4.0, 6.0, mtok(27), 1 if R28 else 104)       # R28: the timpani take the impact
        tracks.append(dict(spec["hook"], name="stabs", gain="-3dB", score=stabs.score()))
        tracks.append({"name": "boom", "patch": "808", "gain": "-6dB", "score": boom.score()})
    if R21:
        spec = {tr["name"]: tr for tr in tracks}
        reply, hornsa = Track("reply"), Track("hornsa")
        for bar in REPLY_BARS:
            at = bar * 4.0
            for m, ln in REPLY:
                reply.add(at, ln * 0.94, mtok(m), 92 if m == 63 else 84)
                at += ln
            hornsa.add(bar * 4.0, 7.6, ",".join(mtok(m) for m in (51, 54, 58, 63)), 70)
        tracks.append(dict(spec["hook"], name="reply", score=reply.score()))
        tracks.append({"name": "hornsa", "patch": "horn", "gain": "-12dB", "pan": -0.1,
                       "sends": {"space": "-5dB"}, "score": hornsa.score()})
    if R19:
        for tr in tracks:
            if R19_WOOD and tr["name"] in ("e1b", "e1bw"):
                tr.update(patch="modal-marimba", gain={"e1b": "-14dB", "e1bw": "-11dB"}[tr["name"]])
        for k, pt in patches.items():
            if k.startswith("a7-sung") or k.startswith("a7-choir"):
                pt["extends"] = pt["extends"] + (" play.glide_overshoot=0.05" if k.startswith("a7-choir")
                                                 else " play.glide_overshoot=0.08")
    if R25 and R17:                                         # the tutti: E1 on horns (8vb) and erhu (8va) with the brass
        tut_h, tut_b = Track("tutti"), Track("tuttib")
        for at0 in (580.0, 585.0):
            at = at0
            for nt, ln in E1:
                tut_h.add(at, ln * 0.94, mtok(midi(nt) - 12), 96)
                tut_b.add(at, ln * 0.96, mtok(midi(nt) + 12), 94)
                at += ln
        tracks.append({"name": "tutti", "patch": "horn", "gain": "-2dB", "pan": -0.1, "sends": {"space": "-5dB"},
                       "score": tut_h.score()})
        tracks.append({"name": "tuttib", "patch": "erhu", "gain": "-6dB", "pan": -0.15,
                       "fx": ["delay time=3/8 mix=0.12 feedback=0.25"], "sends": {"space": "-6dB"}, "score": tut_b.score()})
    if R29:                                                 # counter-lines that come and go
        tr_, st_ = Track("trumpet"), Track("strings")
        A = [(1.0, "Bb4", .5), (1.5, "Db5", .5), (2.0, "Eb5", 1.0), (3.0, "Db5", .5), (3.5, "Bb4", 1.5), (5.0, "Ab4", 1.0),
             (6.0, "Gb4", .5), (6.5, "Ab4", .5), (7.0, "Bb4", 1.0), (9.0, "Eb4", .5), (9.5, "Gb4", .5), (10.0, "Ab4", .5),
             (10.5, "Bb4", 1.0), (11.5, "Ab4", .5)]
        for base, tail in ((24 * 4.0, [(12.0, "Gb4", 1.0), (13.0, "F4", 1.0), (14.0, "Eb4", 2.0)]),
                           (28 * 4.0, [(12.0, "Bb4", 1.0), (13.0, "Db5", 1.0), (14.0, "Eb5", 2.0)])):
            for off, nt, ln in A + tail:
                tr_.add(base + off, ln * 0.9, mtok(midi(nt)), 88 if off in (2.0, 14.0) else 78)
        if R33:                                             # w6: the trumpet answers the choir in the slack
            for at, nt, ln, v in ((333.0, "Db5", .5, 80), (333.5, "Bb4", .5, 76), (334.0, "Ab4", 1.0, 80), (335.0, "Gb4", .5, 76),
                                  (335.5, "F4", 2.0, 82), (345.0, "Gb4", .5, 78), (345.5, "Ab4", .5, 80), (346.0, "Bb4", 1.0, 84),
                                  (347.0, "Db5", 1.0, 86), (348.0, "Eb5", 3.5, 90)):
                tr_.add(at, ln * 0.92, mtok(midi(nt)), v)
        line = ["F#5", "E5", "D5", "B4", "A4", "G4", "B4", "D5", "F#5", "G5", "B5", "D5", "A5", "G5", "F#5", "E5"]
        for i, nt in enumerate(line):
            st_.add(136 * 4.0 + 2.0 * i, 1.95, mtok(midi(nt)), 70 + i)
        st_.add(144 * 4.0, 8.0, mtok(midi("D5")), 84)
        tracks.append({"name": "trumpet", "patch": "trumpet-mute", "gain": "-4dB", "pan": 0.25, "sends": {"space": "-8dB"},
                       "score": tr_.score()})
        tracks.append({"name": "strings", "patch": "mellotron-strings", "gain": "-4dB", "pan": -0.2, "sends": {"space": "-6dB"},
                       "score": st_.score()})
    if R28:                                                 # timpani: the four arrivals
        patches["a7-timp"] = {
            "about": "chirper-two: a kettle drum - a membrane struck off-centre with a long ring, over a sine fundamental "
                     "so it sings its pitch, and a felt-mallet thump; rolls are fast restrikes",
            "synth": {"layers": [
                {"name": "head", "type": "modal", "modes": "membrane",
                 "strike": {"value": 0.72, "mod": [{"src": "rand", "amount": 0.05}]},
                 "bright": {"value": 0.3, "mod": [{"src": "vel", "amount": 0.35}]},
                 "decay": "3s", "damp": 0.25, "tilt": -4, "sharp": 40, "vary": 0.2},
                {"wave": "sine", "level": "-4dB"},
                {"name": "mallet", "type": "noise", "level": {"value": "-66dB", "mod": [{"src": "env.att", "amount": 44},
                                                                                          {"src": "vel", "amount": 6}]}}],
                "env": {"att": {"a": "0.2ms", "d": "12ms", "s": 0}},
                "filters": ["hp cutoff=28", "lp cutoff=5k"],
                "amp": {"a": "1ms", "d": "3s", "s": 0, "r": "400ms", "curve": 3}},
            "play": {"vel_sens": 0.6}}
        tp = Track("timp")

        def roll(b0, b1, m, v0, v1):
            n = int(round((b1 - b0) * 8))
            for i in range(n):
                tp.add(b0 + i * 0.125, 0.4, mtok(m), int(v0 + (v1 - v0) * i / max(1, n - 1)))

        roll(47 * 4.0, 48 * 4.0, 39, 40, 100)               # into the collision: E-flat
        tp.add(48 * 4.0, 4.0, mtok(39), 122)
        roll(119 * 4.0, 120 * 4.0, 45, 36, 104)             # the turn: A, D's dominant
        tp.add(120 * 4.0, 4.0, mtok(38), 124)               # the crest lands on D
        for at in (580.0, 585.0):                            # the tutti
            tp.add(at, 3.0, mtok(38), 112)
        tp.add(152 * 4.0, 4.0, mtok(38), 118)                # the plunge
        tracks.append({"name": "timp", "patch": "a7-timp", "gain": "-11dB", "pan": -0.1, "sends": {"space": "-6dB"},
                       "score": tp.score()})
    if R27:                                                 # air: the new tracks, choirs together, the air shelf
        tracks.append({"name": "shaker", "patch": "dusty-kit", "gain": "0dB", "pan": 0.3, "score": T["shaker"].score()})
        tracks.append({"name": "ride", "patch": "modal-ride", "gain": "-31dB", "pan": -0.3, "sends": {"space": "-12dB"},
                       "score": T["ride"].score()})
        for k, pt in patches.items():
            if (k.startswith("a7-sung") or k.startswith("a7-choir")) and ("harmony" in pt["extends"] or "singers" in pt["extends"]
                                                                          or "choir" in pt["extends"] or "backing" in pt["extends"]):
                pt["extends"] = pt["extends"] + " synth.layers.0.together=true"
    if R25:
        for k, pt in patches.items():
            if k.startswith("a7-sung") or k.startswith("a7-choir"):
                pt["extends"] = pt["extends"] + " synth.lfo.vib.per_note=true synth.lfo.vib.delay=180ms synth.lfo.vib.fade=300ms"
    if R32:                                                 # real kettles; voices that break into head voice
        if "a7-timp" in patches:
            tp_ = patches["a7-timp"]
            tp_["about"] = ("chirper-two: a kettle drum - wM's modes=kettle (the (n,1) family near 1 : 1.5 : 2 : 2.5 over a "
                            "short thump) struck at 0.7 with a 3 s ring, and a felt-mallet touch; rolls are fast restrikes")
            head = dict(tp_["synth"]["layers"][0], modes="kettle", strike={"value": 0.7, "mod": [{"src": "rand", "amount": 0.04}]})
            mallet = tp_["synth"]["layers"][2]
            tp_["synth"]["layers"] = [head, dict(mallet, level={"value": "-70dB", "mod": mallet["level"]["mod"]})]
        for k, pt in patches.items():
            if k in ("a7-choir1", "a7-choir2"):
                pt["extends"] = pt["extends"] + " synth.layers.0.passaggio=C5"
            elif k.startswith("a7-sung"):
                pt["extends"] = pt["extends"] + " synth.layers.0.passaggio=B4"
        for tr in tracks:
            if tr.get("name") == "timp":                    # the helper sine's weight is gone: +3 dB
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + 3.0:g}dB"
            if tr.get("patch") == "a7-choir2":
                tr["gain"] = f"{float(str(tr.get('gain', '0dB')).replace('dB', '')) + 1.0:g}dB"
    if R39:                                                 # the crest choir has aged (wM's age 0.4)
        for tr in tracks:
            if tr.get("name") in ("vd0", "vd1", "vd2") and str(tr.get("patch", "")).startswith("a7-choir"):
                old = tr["patch"] + "-old"
                if old not in patches:
                    patches[old] = dict(patches[tr["patch"]], extends=patches[tr["patch"]]["extends"] + " synth.layers.0.age=0.4")
                tr["patch"] = old
    if R37 and "a7-sung" in patches:                        # w3: she hums the horns' answer back
        echo = []
        for b0 in (144.0, 176.0):
            at = b0
            for k, (m, ln) in enumerate(((68, 0.5), (70, 0.5), (73, 1.0), (70, 0.5), (68, 0.5), (65, 1.0), (63, 2.0))):
                echo.append({"at": at, "len": round(ln * (0.96 if k < 6 else 0.9), 3), "ph": "UW1" if k else "M UW1",
                             "pitch": f"m{m}", "vel": round(0.62 + (0.06 if k == 2 else 0.0) - (0.04 if b0 == 144.0 else 0.0), 3)})
                at += ln
        tracks.append({"name": "echo", "patch": "a7-sung", "gain": "-4dB", "pan": 0.15,
                       "fx": ["delay time=3/8 mix=0.2 feedback=0.35"], "sends": {"space": "-4dB"}, "notes": echo})
    if R43:                                                 # w3: she hums into an open floor
        for tr in tracks:
            if tr.get("name") == "sub":
                T["sub"].ev = [(e[0], e[1], e[2], 1, e[4]) if 36 * 4.0 <= e[0] < 40 * 4.0 else e for e in T["sub"].ev]
                tr["score"] = T["sub"].score()
            if tr.get("name") == "echo" and tr.get("patch") == "a7-sung":
                patches["a7-sung-hum"] = dict(patches["a7-sung"],
                                              extends=patches["a7-sung"]["extends"] + " synth.layers.0.hum=1 synth.layers.0.hum_at=m")
                tr["patch"] = "a7-sung-hum"
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + 3.0:g}dB"
    if R36:                                                 # the low E1 on a log drum (scanned-mallet -> log-drum)
        for tr in tracks:
            if tr.get("name") in ("e1c", "e1cw") and tr.get("patch") == "scanned-mallet":
                tr["patch"] = "log-drum"
                pts = [["0b", 0.0]]
                for b0, b1 in ((24, 28), (44, 48), (56, 60), (136, 140), (148, 152)):
                    pts += [[f"{b0 * 4 - 0.02:g}b", 0.0], [f"{b0 * 4}b", -24.0], [f"{b1 * 4 - 0.02:g}b", -24.0], [f"{b1 * 4}b", 0.0]]
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.hole", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), hole={"points": pts})
    if R35:                                                 # the hook on plucked strings (dx-epiano -> koto)
        for tr in tracks:
            if tr.get("name") in ("e1a", "e1aw") and tr.get("patch") == "dx-epiano":
                tr["patch"] = "koto"
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) - 2.0:g}dB"
            if tr.get("name") == "boom" and tr.get("patch") == "808":
                tr["patch"] = "a7-timp"
    if R34:                                                 # the hook in plain sight; the floor under it
        for tr in tracks:
            if tr.get("name") in ("e1a", "e1b", "e1c", "e1aw", "e1bw", "e1cw"):
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + 2.0:g}dB"
            if tr.get("name") in ("sub", "sub8"):
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) + 5.0:g}dB"
        rl = patches["a7-reese"]["synth"]["layers"]
        assert rl[2].get("wave") == "sine" and rl[2].get("level") == "-3dB", rl
        rl[2] = dict(rl[2], level="3dB")
    if R24:
        for tr in tracks:
            if tr.get("patch") == "cz-pad":
                tr["patch"] = "hammond-b3"
    if R22:
        for k, pt in patches.items():
            if k.startswith("a7-sung"):
                pt["extends"] = pt["extends"] + " play.scoop=1 play.fall=2.5"
            elif k.startswith("a7-choir"):
                pt["extends"] = pt["extends"] + " play.scoop=0.6 play.fall=1.5"
        patches["a7-erhu"] = {"extends": "erhu play.scoop=1.5 play.fall=1"}
        for tr in tracks:
            if tr["name"] == "bow":
                tr["patch"] = "a7-erhu"
    if R52:                                                 # w1: the jet seen from far off (bars 5, 9, 13)
        star, jet = Track("star"), (70, 77, 84, 91, 98)       # E7 from B-flat: Bb4 F5 C6 G6 D7
        for i, m in enumerate(jet[:3]):
            star.add(16.0 + i, 0.9, mtok(m), 64 + 4 * i)
        for i, m in enumerate(jet):
            star.add(32.0 + i, 0.9, mtok(m), 70 + 3 * i)
        for k in range(3):
            for i, m in enumerate(jet):
                star.add(48.0 + 2.75 * k + 0.5 * i, 0.45 if i < 4 else 0.7, mtok(m), 76 + 4 * k + 2 * i)
        tracks.append({"name": "star", "patch": "glock", "gain": "-9dB", "pan": 0.35,
                       "fx": ["delay time=3/8 mix=0.25 feedback=0.35"], "sends": {"space": "-4dB"},
                       "score": star.score()})
    if R53:                                                 # the organ ignores velocity: close it by lane (w5, w9)
        f = 0.03
        pts = [["0b", 0]]
        edges = [(272.0, 272.4), (273.5, 273.9), (276.0, 276.4), (277.5, 277.9)]
        prev = 272.0
        pts += [[f"{272.0 - f:g}b", 0]]
        for a, b in edges:
            if a > prev:
                pts += [[f"{prev:g}b", -60], [f"{a - f:g}b", -60], [f"{a:g}b", 0]]
            pts += [[f"{b:g}b", 0]]
            prev = b + f
        pts += [[f"{prev:g}b", -60], [f"{280.0 - f:g}b", -60], ["280b", 0],
                [f"{544.0 - f:g}b", 0], ["544b", -60], [f"{564.0 - f:g}b", -60], ["564b", 0]]
        for tr in tracks:
            if tr.get("patch") == "hammond-b3":
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.hush", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), hush={"points": pts})     # (auto dicts are shared)
    if R51:                                                 # w2: a call before the answer (bars 21-22, fill at 24)
        for tr in list(tracks):
            if tr.get("name") == "hook" and tr.get("score"):
                pos, call = 0.0, Track("hook2")
                for tok in tr["score"].split():
                    m = re.match(r"^(.+?)/([0-9.e+-]+)b(?:@(\d+))?(.*)$", tok)
                    head, ln, vel, art = m.group(1), float(m.group(2)), m.group(3), m.group(4)
                    if head != "R" and 64 <= pos < 72 and int(vel or 0) > 1:
                        g = re.search(r"\^gate=([0-9.]+)", art)
                        call.add(pos + 16.0, ln * (float(g.group(1)) if g else 1.0), head, int(vel) - 4)
                    pos += ln
                tracks.append(dict(tr, name="hook2", gain=f"{float(tr['gain'].replace('dB', '')) + 3.0:g}dB",
                                   pan=-0.15, score=call.score()))
                break
        fill = Track("fill24")
        for i, piece in enumerate(("s", "s", "t", "t", "s", "s", "t", "s")):
            fill.add(94.0 + 0.25 * i, 0.2, piece, 72 + 6 * i)
        fill.add(96.0, 0.5, "oh", 112)
        tracks.append({"name": "fill24", "patch": "dusty-kit", "gain": "-2dB", "pan": 0.0, "score": fill.score()})
    if R50:                                                 # palette: a clap on the backbeat, an even hum
        for tr in list(tracks):
            if tr.get("name") in ("snare", "snareh") and tr.get("score"):
                sc = " ".join(re.sub(r"^s/", "cp/", tok) for tok in tr["score"].split())
                tracks.append(dict(tr, name=tr["name"].replace("snare", "clap"), patch="electro-kit",
                                   gain=f"{float(tr['gain'].replace('dB', '')) + 5.0:g}dB", score=sc))   # +5: masked below
            if tr.get("name") == "echo" and tr.get("patch") == "a7-sung-hum":
                patches["a7-sung-hum-even"] = dict(patches["a7-sung-hum"],
                                                   extends=patches["a7-sung-hum"]["extends"] + " synth.layers.0.hum_even=1")
                tr["patch"] = "a7-sung-hum-even"
                tr["gain"] = f"{float(tr['gain'].replace('dB', '')) - 3.0:g}dB"
    if R48:                                                 # w4: the collision heard (bars 49-80)
        coll = [["0b", 0.0], ["191.75b", 0.0], ["192b", 1.0], ["319.75b", 1.0], ["320b", 0.0]]
        amt = {"snare": 7.0, "jet": 9.0, "stabs": 5.0, "clap": 7.0}   # (the clap exists from v50 on)
        for tr in tracks:
            if tr.get("name") in amt:
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB", "mod": [
                    {"src": "auto.coll", "amount": amt[tr["name"]]}]}}]
                tr["auto"] = dict(tr.get("auto", {}), coll={"points": coll})
    if R47:                                                 # palette: E4's comping on a clavinet
        for tr in list(tracks):                             # the organ keeps its body (its 16' drawbar is t7's
            if tr.get("name") in ("e4", "e4w", "e4w5", "e4w7", "e4w8") and tr.get("patch") == "hammond-b3":   # 97 Hz)
                tracks.append(dict(tr, name=tr["name"] + "c", patch="clav",
                                   gain=f"{float(tr['gain'].replace('dB', '')) + 3.0:g}dB", pan=-float(tr.get("pan", 0.0)) or 0.2,
                                   fx=list(tr.get("fx", [])) + [{"type": "filter", "kind": "hp", "cutoff": 250, "q": 0.707}]))
    if R46:                                                 # palette: the spiral falls forever (a falling Shepard pad)
        sh = {"center": "520hz", "cycle": "8s", "octaves": 9, "width": 1.3, "down": True}
        patches["a7-orbit"] = {"about": "chirper-two: the library shepard-pad gliding DOWN - an endless fall (t7's spiral)",
                               "fx": ["chorus mix=0.3", "reverb kind=hall decay=5s mix=0.35"], "gain": "-6dB",
                               "play": {"gate": 1.0, "vel_sens": 0.3},
                               "synth": {"amp": {"a": "1.5s", "r": "2.5s", "s": 1},
                                         "filters": [{"cutoff": "5k", "kind": "lp", "q": 0.6}],
                                         "layers": [{"type": "shepard", "shepard": dict(sh)},
                                                    {"type": "shepard", "cents": 7, "level": "-4dB", "shepard": dict(sh)}]}}
        orb = Track("orbit")
        orb.add(88 * 4.0, 32 * 4.0 - 0.75, ",".join(mtok(m) for m in (51, 58)), 90)
        tracks.append({"name": "orbit", "patch": "a7-orbit", "gain": "-12dB", "pan": 0.0, "sends": {"space": "-12dB"},
                       "score": orb.score()})
    if R45:                                                 # w10: the plunge falls (bars 157-160), the bell holds E
        lo, hi = 156 * 4.0, 160 * 4.0
        lane = [["0b", 0.0], [f"{lo:g}b", 0.0], [f"{lo + 8:g}b", -3.0], [f"{lo + 12:g}b", -6.0], [f"{hi - 0.1:g}b", -12.0],
                [f"{hi:g}b", 0.0]]
        for tr in list(tracks):
            if tr.get("name") not in ("e1a", "e1b", "jet") or not tr.get("score"):
                continue
            pos, orig, copy, start = 0.0, [], [], None
            for tok in tr["score"].split():
                m = re.match(r"^(.+?)/([0-9.e+-]+)b(?:@(\d+))?(.*)$", tok)
                head, ln = m.group(1), float(m.group(2))
                if lo - 1e-6 <= pos < hi - 1e-6:
                    if start is None:
                        start = pos
                    if head != "R":
                        orig.append(re.sub(r"@\d+", "@1", tok, count=1))
                        g = re.search(r"\^gate=([0-9.]+)", tok)
                        ring = ln * (float(g.group(1)) if g else 1.0)
                        c = tok
                        if pos + ln > hi - 0.05:
                            c = c.replace(f"/{m.group(2)}b", f"/{max(0.03, hi - 0.05 - pos):.4g}b", 1)
                            c = re.sub(r"\^gate=[0-9.]+", "", c)
                        elif pos + ring > hi - 0.05:
                            c = re.sub(r"\^gate=[0-9.]+", "", c)
                        copy.append(c)
                    else:
                        orig.append(tok)
                        copy.append(f"R/{min(ln, hi - pos):.4g}b" if pos + ln > hi else tok)
                else:
                    orig.append(tok)
                pos += ln
            if start is None:
                continue
            tr["score"] = " ".join(orig)
            pl = tr["patch"] + "-pl"                        # the same instrument, its oscillators bent by the lane
            patches[pl] = {"extends": tr["patch"], "synth": {"pitch": {"value": 0, "mod": [{"src": "auto.plunge", "amount": 1}]}}}
            tracks.append(dict(tr, name=tr["name"] + "pl", patch=pl, score=f"R/{start:.6g}b " + " ".join(copy),
                               auto=dict(tr.get("auto", {}), plunge={"points": lane})))
    if R44:                                                 # palette: a tuned body under the break's kick
        patches["a7-thump"] = {"extends": "909", "kit": {"k": {"pitch": "Bb1"}}}
        for tr in list(tracks):
            if tr.get("name") in ("kick", "kickh") and tr.get("score"):
                g = float(tr["gain"].replace("dB", ""))
                tracks.append(dict(tr, name=tr["name"] + "9", patch="a7-thump", gain=f"{g + 2:g}dB",
                                   fx=list(tr.get("fx", [])) + [{"type": "filter", "kind": "lp", "cutoff": 180, "q": 0.707}]))
    if R57:                                                 # w7: every corner comes sooner (bars 105-112)
        spec = next(tr for tr in tracks if tr.get("name") == "sungs")
        line = [n for n in spec["notes"] if 415.9 <= n["at"] < 420.0]
        full, frag = line, line[:3]
        plan = {"a": [(424.0, full), (434.5, full), (440.5, frag), (444.0, frag), (446.25, frag)],
                "b": [(430.0, full), (438.0, frag), (442.5, frag), (445.25, frag)]}
        for side, (tract, pan) in (("a", (1.12, -0.45)), ("b", (0.94, 0.45))):
            pn = f"a7-sooner-{side}"
            patches[pn] = dict(patches[spec["patch"]],
                               extends=patches[spec["patch"]]["extends"] + f" synth.layers.0.tract={tract}")
            notes = []
            for k, (at0, ph) in enumerate(plan[side]):
                for n in ph:
                    v = min(0.85, n["vel"] * (0.8 + 0.06 * k))
                    notes.append(dict(n, at=round(at0 + n["at"] - line[0]["at"], 4), vel=round(v, 3)))
            tracks.append(dict(spec, name=f"sooner{side}", patch=pn, pan=pan, gain="-1dB", notes=notes))
    if R56:                                                 # whole: E5 orbits the listener and spirals in
        spin = [["0b", 0.25], ["192b", 0.25], ["200b", 0.5], ["320b", 0.5], ["336b", 0.25], ["352b", 0.75],
                ["480b", 1.5], ["600b", 2.0], ["639.9b", 6.0], ["640b", 0.25]]
        fall = [["0b", 8.0], ["192b", 6.0], ["320b", 5.0], ["352b", 5.0], ["480b", 3.0], ["600b", 2.5],
                ["639.9b", 0.6], ["640b", 8.0]]
        orb = {"type": "orbit", "path": "circle", "distance": 0, "doppler": 0.0, "rate": "1/1",
               "speed": {"value": 0, "mod": [{"src": "auto.spin", "amount": 1}]},
               "radius": {"value": 0, "mod": [{"src": "auto.fall", "amount": 1}]}}
        for tr in tracks:
            if tr.get("name") in ("e5", "e5w", "orbit") or str(tr.get("name", "")).startswith("tide"):
                ph = 0.0 if tr["name"].startswith("e5") else 0.5     # the tide opposite the trill
                tr["fx"] = list(tr.get("fx", [])) + [dict(orb, phase=ph)]
                tr["auto"] = dict(tr.get("auto", {}), spin={"points": spin}, fall={"points": fall})
    if R55:                                                 # w11: the last heartbeat; the plunge out of the sub
        beats = [640.0, 642.0, 644.0, 646.5, 649.0, 651.5, 654.0, 659.0, 664.0, 669.0, 674.0, 679.0, 684.0, 689.0,
                 694.0]                                     # from 644 on t8's five-beat chord grid
        heart = Track("heart")
        for i, b in enumerate(beats):
            v = int(round(104 - 60 * i / (len(beats) - 1)))
            heart.add(b, 0.25, "k", v)
            heart.add(b + 0.375, 0.25, "k", int(v * 0.55))
        spec = {tr["name"]: tr for tr in tracks}
        tracks.append(dict(spec["kick"], name="heart", score=heart.score()))
        tracks.append(dict(spec["kick9"], name="heart9", score=heart.score()))
        for tr in tracks:
            if tr.get("name") == "kick":                    # the dusty kick still thuds at vel 1: close it by lane
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "gain", "gain": {"value": "0dB",
                                                      "mod": [{"src": "auto.rest", "amount": 1}]}}]
                tr["auto"] = dict(tr.get("auto", {}), rest={"points": [["0b", 0], ["639.97b", 0], ["640b", -60]]})
            if tr.get("name") in ("e1apl", "e1bpl", "jetpl"):
                tr["fx"] = list(tr.get("fx", [])) + [{"type": "filter", "kind": "hp", "cutoff": 90, "q": 0.707}]
    if R54:                                                 # whole: the reese and floor breathe under the kick
        depth = {"bass": "-5dB", "bassup": "-5dB", "bass5": "-5dB", "bass7": "-5dB", "bass8": "-5dB",
                 "sub": "-6dB", "sub8": "-6dB"}
        for tr in tracks:
            if tr.get("name") in depth:
                tr["fx"] = list(tr.get("fx", [])) + [
                    {"type": "pump", "on": f"{k}.k", "depth": depth[tr["name"]], "release": "200ms", "curve": 0.6}
                    for k in ("kick", "kickh")]
    master = {"fx": [{"type": "eq", "bands": ["hp cutoff=25", "lowshelf cutoff=120 gain=5dB", "peak cutoff=160 gain=-2.5dB q=1.2",
                                              "peak cutoff=320 gain=-2dB q=0.8", "peak cutoff=1400 gain=-2.5dB q=0.7",
                                              "highshelf cutoff=8000 gain=" + ("2dB" if R27 else "1dB")]},
                     "glue threshold=-18dB ratio=2 attack=10ms release=150ms makeup=1dB",
                     {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                     {"type": "filter", "kind": "lp", "q": 0.707,
                      "cutoff": {"value": 20000, "mod": [{"src": "auto.close", "amount": 1}]}},
                     {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]},
                      "time": "2b", "curve": 1.6},
                     {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
              "auto": {"dyn": {"points": dyn}, "close": {"points": close}, "stop": {"points": stop}}}
    if R54:                                                 # whole: the body given back, the edge taken off
        master["fx"][0]["bands"] = list(master["fx"][0]["bands"]) + ["peak cutoff=95 gain=4dB q=0.8",
                                                                     "peak cutoff=2600 gain=-3dB q=0.6"]
    about = ("chirpers - Accretion, track 7. Original composition by chirper-two, generated by "
             "compose/chirpers9/src/chirpers9-t7.py. The innermost orbit: every element transformed in a storm a semitone "
             "above home (Eb), all cycles phased to land on bar 120 where the pull resolves to D and E7, the jet - the "
             "Lydian collection as one column of fifths, fired upward - crests the album.")
    lines = [
        "about: " + json.dumps(about),
        "meta: " + json.dumps({"artist": "chirpers", "album": "Accretion", "title": "Marginally Bound", "track": 7,
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
        "buses: " + json.dumps({"space": {"gain": "-5dB", "fx": ["hp cutoff=250", "reverb kind=hall decay=2.4s mix=1"]}}),
        "master: " + json.dumps(master),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(OUT, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
