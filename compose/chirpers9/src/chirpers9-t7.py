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
                    horns.add(at, ln * 0.96, ",".join(mtok(m) for m in ch), 84 if ln == 4.0 else 76)
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
                                                             "synth.layers.0.even=1 synth.layers.0.harmony=[-7]")
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
    if R8:
        spec = {tr["name"]: tr for tr in tracks}
        for new, old in (("tide5", "tide"), ("bass5", "bass"), ("e4w5", "e4")):
            tracks.append(dict(spec[old], name=new, score=T[new].score()))
    master = {"fx": [{"type": "eq", "bands": ["hp cutoff=25", "lowshelf cutoff=120 gain=5dB", "peak cutoff=160 gain=-2.5dB q=1.2",
                                              "peak cutoff=320 gain=-2dB q=0.8", "peak cutoff=1400 gain=-2.5dB q=0.7",
                                              "highshelf cutoff=8000 gain=1dB"]},
                     "glue threshold=-18dB ratio=2 attack=10ms release=150ms makeup=1dB",
                     {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                     {"type": "filter", "kind": "lp", "q": 0.707,
                      "cutoff": {"value": 20000, "mod": [{"src": "auto.close", "amount": 1}]}},
                     {"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.stop", "amount": 1}]},
                      "time": "2b", "curve": 1.6},
                     {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
              "auto": {"dyn": {"points": dyn}, "close": {"points": close}, "stop": {"points": stop}}}
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
