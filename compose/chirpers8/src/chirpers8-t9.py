#!/usr/bin/env python3
"""chirpers8-t9 (chirpers VIII, track 9). Composed by chirper-two: POLYTEMPO BRAINDANCE in BOHLEN-PIERCE.

"Period Doubling". A clock that learns to drift. One number drives everything: the LOGISTIC MAP, x <- r x (1 - x),
iterated once per sixteenth. As r climbs through the track the music walks the famous road into chaos:
- ONE (r 2.9): the map settles on a single value after a damped wobble - one note, sixteenths, a sequencer pulse.
- TWO (r 3.2, 7/8): the first doubling - two notes alternate.  FOUR (r 3.5): four, and a rest appears in the cycle.
- EIGHT (r 3.56, 5/4): eight.  CHAOS (r 3.7 -> 3.82, the tempo ramping 140 -> 150): no cycle at all.
- WINDOW (r 3.835, 4/4): inside chaos, order returns for a moment: PERIOD THREE - a cycle of three sixteenths that
  runs across the beat, a cross-rhythm made by arithmetic.
- STORM (r 4.0, 11/8 at 154): full chaos.  SETTLE (r 3.4 -> 2.9, slowing to 132): back down to one note.
- THE TUNING is BOHLEN-PIERCE: 13 equal steps to the TRITAVE (3:1) instead of the octave, in its Lambda mode
  (degrees 0 2 3 4 6 7 9 10 12); no octaves anywhere. Its natural voice is the clarinet (odd harmonics only), so the
  lead is chirp's PHYSICAL REED (a reed on a cylindrical bore); chords are BP's 3:5:7 triad on a glass pad.
- POLYTEMPO: the lead runs on sixteenths, glitch blips on a 5:4 grid (the map's twin, y) and the folded-sine bass on a
  3:4 grid, so three clocks run at once and only meet at bar lines.
- METER CHANGES (4/4, 7/8, 5/4, 11/8) and TEMPO RAMPS in the tempo map; drums whose accents, ratchets and stutters
  the map decides; a fold shaper on the bass, a stutter on the drum bus whose chance rises with chaos.
140 bpm base, Bohlen-Pierce on A. Form: one 20 / two 16 / four 20 / eight 20 / chaos 32 / window 18 / storm 24 /
settle 28 bars.

Emits songs/chirpers8-t9.yaml. Edit the music here.
"""
import json
import math
import os
import random

OUT = os.environ.get("T9_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t9.yaml")
BP = 12 * math.log2(3) / 13              # one Bohlen-Pierce step in semitones (146.3 cents)
TRITAVE = 12 * math.log2(3)
LAMBDA = [0, 2, 3, 4, 6, 7, 9, 10, 12]   # the Lambda mode, 9 notes a tritave
# (name, bars, meter, r from, r to, bpm at start, ramp to next?)
SECS = [("one", 20, (4, 4), 2.9, 2.9), ("two", 16, (7, 8), 3.2, 3.2), ("four", 20, (4, 4), 3.5, 3.5),
        ("eight", 20, (5, 4), 3.56, 3.56), ("chaos", 32, (4, 4), 3.7, 3.82), ("window", 18, (4, 4), 3.835, 3.835),
        ("storm", 24, (11, 8), 3.95, 4.0), ("settle", 28, (4, 4), 3.4, 2.9)]
BPM = {"one": 140, "two": 140, "four": 140, "eight": 140, "chaos": 140, "window": 150, "storm": 154, "settle": 154}
# T9_R2 = drift (v2, wM's tunings, systems and morph). THE CLOCK DRIFTS OUT OF TUNE AND BACK: the song's `tuning` is
# 12-TET while the map holds one and two notes (the Bohlen-Pierce lines snap to their nearest semitones: a plain
# sequencer), ramps into exact Bohlen-Pierce across the period-four section, stays alien through eight, chaos, the
# window and the storm, and ramps back to 12-TET as it settles. In the chaos and the storm a second glass pad plays the
# 3:5:7 chords CROSS-SYNTHESISED with the drum bus (`morph` mode cross keyed by `drums`), so the chords breathe in the
# chaotic rhythm. A second logistic map, at r 3.95 as a song `var`, throws the reed around the stereo field.
# T9_R2=none reproduces v1.
R2 = os.environ.get("T9_R2", "drift")
# T9_R3 = sing (v3, wM's singing voice): in the period-three window a human voice SINGS "it comes back in threes"
# (`chirp tts --sing "A3/8 C4 E4" --repeat 3`, src/t9/sing.json): five syllables on a three-note tune, so the words
# land on different notes each time round while the map cycles in threes under them; its notes snap to the song's
# Bohlen-Pierce. Once more as the map settles, by then back in 12-TET: the same words, a different tuning.
# T9_R3=none reproduces v2.
R3 = os.environ.get("T9_R3", "sing")
# T9_R4 = break (v4, palette round). Out of the album's staples: the kit leaves machine-kit (on nine songs) for the
# BREAK-KIT, a squashed 1969 funk kit as a sampler hears it, and in chaos and storm the map CHOPS THE BREAK - each
# sixteenth's iterate picks a piece (ghost, edit snare, open hat) the way a jungle producer slices the Amen, on its
# own track into the drums bus (so the stutter and the glass pad's cross-synthesis hear it too). The blips leave the
# library `blip` (four songs) for c9-pulse, a one-bit loudspeaker voice: a very narrow pulse train, crushed - the
# sound of a machine driving its speaker directly, the oldest computer music there is, said sideways.
# T9_R4=none reproduces v3.
R4 = os.environ.get("T9_R4", "break")
KIT = "break-kit" if R4 == "break" else "machine-kit"
# T9_R5 = orbit (v5, section round on w5, 1:49-2:17, the period-eight section's second half: "static, little new" and
# the song's dynamic range only 5.3 dB). THE ATTRACTOR AS A CHORD: the drums fall away and a wordless choir (the
# library's classic formant choir, new to the album) holds all eight points of the period-eight orbit at once, each
# at its exact Bohlen-Pierce pitch (Hz, so no tuning snaps them): the orbit's four close pairs - the branches of the
# bifurcation diagram that have only just split - sit ~60 cents apart and BEAT against each other. You hear period
# doubling as pitches splitting. The drums come back through a ratcheted break fill. New tracks only (orbit, fill)
# and lanes local to the window. T9_R5=none reproduces v4.
R5 = os.environ.get("T9_R5", "orbit")
# T9_R6 = steel (v6, palette round). The song had no sustained, singing line: reed, blips and pulses are all
# staccato. Now, as the map SETTLES (r 3.4 -> 2.9), a PEDAL STEEL (new to the album) plays the period-two orbit
# itself: its two points as two long notes a bar, gliding one into the other (the steel's swell and slide), their
# interval narrowing bar by bar as r falls, until at r = 3 - the bifurcation point - they meet in one note, the
# fixed point 1 - 1/r, which it holds to the end. The bifurcation diagram heard backwards, as a tune that closes.
# Exact Bohlen-Pierce pitches (Hz, the map's own mapping), so no tuning snaps them. And the album-staple bell (three
# songs) that marks each section becomes a HANDPAN. T9_R6=none reproduces v5.
R6 = os.environ.get("T9_R6", "steel")
# T9_R7 = lpg (v7, palette round). AS KEPT: the bass's sub-sine body stays (replacing it outright, and the dizi below,
# both broke the sections' returns: recurrence 100 -> 56-85), and c9-lpg joins as the bass's VOICE, an octave over
# it (T9_R7_BASS=layer; =lpg swaps the bass whole; T9_R7_DIZI=1 adds the flute). The design: c9-lpg, a patch of my own
# after the West Coast: a triangle and its octave, folded, through a LOW-PASS GATE (one envelope opens the filter and
# the amp together, then lets both fall: the "bongo" pluck of the first voltage-controlled music), so the 3:4 bass
# speaks each note instead of humming under the floor. And in the early, static windows (w2 and w4: the two and four
# sections), a DIZI - the bamboo flute with the buzzing membrane, new to the album - doubles the reed's accents (its
# loudest iterates) an octave up, which in Bohlen-Pierce lands on the scale's nearest step to an octave: 1170 cents,
# a slightly closed octave, the song's tuning pulling the flute in. The flute comes back as the map settles, so the
# record's two calm ends share a colour. T9_R7=none reproduces v6.
R7 = os.environ.get("T9_R7", "lpg")
# T9_R8 = ostinato (v8, section round on w4, 1:22-1:49: "static, little new vs w3" - the end of period four and the
# start of period eight). THE ORBIT AS A TUNE: a STEEL PAN (new to the album) plays the attractor's own orbit as an
# ostinato in eighths - the four points of period four, round and round, growing louder - and at the bifurcation
# (bar 1 of the 5/4 section) the tune DOUBLES to the eight points of period eight, an eight-note figure turning
# against the ten eighths of each 5/4 bar, so it lands differently every bar. At 256b it stops, exactly where the
# choir freezes the same eight points into a chord. Exact Bohlen-Pierce Hz, the map's own mapping. New track only.
# T9_R8=none reproduces v7.
R8 = os.environ.get("T9_R8", "ostinato")


def logistic_orbit(r, p, n=4000):
    x = 0.5
    for _ in range(n):
        x = r * x * (1 - x)
    out = []
    for _ in range(p):
        x = r * x * (1 - x)
        out.append(x)
    return out


# T9_R9 = return (v9, section round on w2, 0:27-0:54: "static" - the end of `one` and most of `two`). IT COMES BACK:
# a KOTO (new to the album) knocks the map off its attractor and lets it return, one iterate per eighth. At the end
# of `one` (r = 2.9, where the fixed point is about to lose its footing: multiplier -0.9) the knocked value spirals
# home slowly, high-low-high, narrowing - the period-two alternation heard coming before it arrives. In `two` every
# other 7/8 bar is a knock and a return in seven eighths (seven iterates), each knock a different size and side, so
# the lick recurs but never repeats. Under it a TABLA (new to the album) plays a 3+2+2 cycle in the 7/8, a te-re fill
# every fourth bar. New tracks only. (T9_KNOCK=every, a knock in every bar: w2 motion 0.032 -> 0.038, still
# "static", s0 -0.04; opt-in.) T9_R9=none reproduces v8.
R9 = os.environ.get("T9_R9", "return")
KNOCKS = [0.22, -0.18, 0.3, -0.25, 0.12, -0.3, 0.26, -0.1]
TABLA = [["tin", "tin", "na", "dhin", "na", "dhin", "na"],
         ["dha", "tin", "na", "dhin", "na", "dhin", "na"],
         ["tin", "tin", "na", "dhin", "na", "ge", "na"],
         ["dha", "te", "re", "dhin", "na", "dhin", "dha"]]


def lmap(r, x, n):
    out = []
    for _ in range(n):
        x = r * x * (1 - x)
        out.append(x)
    return out


# T9_R10 = bpclar (v10, palette round). The lead leaves the library clarinet (three album songs) for c9-bpclar, this
# song's own BOHLEN-PIERCE CLARINET: Bohlen-Pierce is the clarinet's scale (a cylindrical bore sounds odd harmonics,
# and BP repeats at the 3:1 tritave, not the octave), so this reed is pushed harder and brighter, a little airier, and
# carries a quiet sine at exactly 3:1 - the third harmonic, the tritave, sung on top of every note. In the calm
# sections (the period-3 window, the settle) it plays SUBTONE: breathy, dark, close. Pushed bright (press 0.52, bright
# 0.5, lp 4.5k) it cost spectrum (s0 96.75); the darker reed (0.46/0.38/3.6k) sits at parity. T9_SUB=none|settle
# and the T9_BPC_* knobs stay. T9_R10=none reproduces v9.
R10 = os.environ.get("T9_R10", "bpclar")
# T9_R11 = d (v11, whole-song round). D FROM OUTSIDE. Both neighbours live on D - Kept in Mercury (t8) ends on a
# D-minor colour (292/342/468/547/877 Hz), Call and Return (t10) opens on a loud D4 - and this song, in
# Bohlen-Pierce on A, met neither (flow 59: in-seam 7.7 dB off, A4's handpan +25 dB at 468; out-seam 8.5 dB, -32 at
# 292). So D becomes the note from outside the system: the handpan that marks every bifurcation now strikes D4 in
# exact Hz, which BP has no step for - a neighbour's note heard through the wall at each doubling, ringing against
# the tritave scale - the song opens on t8's own D-minor chord (D F A D on the glass pad, still 12-EDO there)
# before the map takes it (with t8's A3 under it, louder), and at the end the floor (bass, its pluck) leaves six beats
# early, the last chords turn to D-F-G-D, a final D4 bell strikes and a choir holds D4+D5 into the tail for t10 to
# answer. Flow 59 -> 62/63.
# T9_R11=none reproduces v10.
R11 = os.environ.get("T9_R11", "d")
# T9_R12 = henon (v12, whole-song round). A SECOND MAP. Through the two chaotic stretches (chaos, storm: w6-w10,
# "little new" by the sections tool) the logistic map gets company: wM's new `gen: henon` - the Henon map, the
# two-dimensional strange attractor (x <- 1 - a x^2 + y, y <- b x; a 1.4, b 0.3) - plays both its axes at once. And
# since y is only x one step late (times b), the two axes are a CANON the attractor writes by itself: a XYLOPHONE
# (new to the album) reads x on the Lambda mode of Bohlen-Pierce from A4, a MARIMBA reads y a tritave down and one
# step behind. It jumps where the logistic line folds: two chaoses, one written, one answering. New tracks only.
# Scored s0 (pin ade7b930): in both chaos and storm 96.70 (sections 11 -> 9, returns 4 -> 2: one timbre over both
# stretches joins them), storm only 96.78, chaos only 96.82 - the default; T9_HEN_SECS=both|storm stay.
# T9_R12=none reproduces v11.
R12 = os.environ.get("T9_R12", "henon")
# T9_R13 = squall (v13, section round on w10, 4:00-4:25: "little new vs w9" - the storm's middle). THE WEATHER IN
# THE MACHINE. A GENDYN voice (wM's layer, Xenakis's dynamic stochastic synthesis) blows through the storm's last
# ten bars: every wave cycle redrawn through twelve breakpoints that wander in level AND in length, so the pitch itself
# slides (Xenakis's glissandi), on a BP tritave-root chord, its disorder rising with velocity bar by bar - a squall,
# not a note. Then, for one bar, the eye: the drum bus drops out under it, and the storm resumes. New track + one
# drum-bus gain lane. T9_R13=none reproduces v12.
R13 = os.environ.get("T9_R13", "squall")
# T9_R14 = terrain (v14, palette round). THE ORBIT GETS ITS OWN VOICE. The orbit choir (the logistic map's period
# eight, held as a chord) and the closing D hold were the library's choir-classic. Now they are WAVE TERRAIN
# (Bischoff, Gold and Horton, 1978; wM's new layer; new to the album): an orbit circling over a surface of hills
# and hollows once per period, the heights under it the wave. The orbit runs a hair off closing (ratio 1.003), so
# each held note slowly drifts through shapes, and an LFO walks its centre across the hills: no filter, the timbre
# moving because the orbit does. A song about orbits voiced by one. Scored s0 (v13 96.740): orbit + the closing D
# hold 96.715 (flow 61.1 -> 60.6: the D handed to t10 wants the choir's breath), orbit only 96.746 - the default;
# the main pad as terrain too, level-matched, 96.376 (spectrum 90 -> 88, flow -> 57: it is brighter and it is
# everywhere). Opt-in: T9_R14_DHOLD=on, T9_R14_PAD=on. T9_R14=none reproduces v13.
R14 = os.environ.get("T9_R14", "terrain")
C9_TERRAIN = {"about": "chirper-two: wave terrain on the sines surface, an orbit a hair off closing (ratio 1.003) whose "
                       "centre an LFO walks across the hills: a held chord that drifts through shapes.",
              "synth": {"layers": [{"type": "terrain", "terrain": {
                  "surface": "sines", "rx": 0.5, "ry": 0.45, "k": 1.2, "ratio": 1.003, "cy": 0.08,
                  "cx": {"value": 0.1, "mod": [{"src": "lfo.drift", "amount": 0.2}]}}}],
                  "lfo": {"drift": {"wave": "sine", "rate": "0.07hz"}},
                  "filters": [{"kind": "lp", "cutoff": 4000, "q": 0.5}],
                  "amp": {"a": "3s", "s": 1, "r": "4s"}}}
# T9_R15 = cz (v15, palette round). PHASE DISTORTION, NOT FILTERS. Two library plucks become the song's own CZ
# patches (wM's `type: pd`, Casio's 1984 answer to the analogue filter; new to the album): the knock-and-return koto
# (section two) is a SAW bend and the period-eight steel pan (section four) a SQUARE bend, each note struck bright -
# a cosine read through a bent phase - and relaxing toward a pure sine as its own envelope lets the bend go. No
# resonant shapes (they squelch); the brightness lives inside each note, so the two stillest windows of the song
# move from the inside. T9_R15=none reproduces v14.
R15 = os.environ.get("T9_R15", "cz")


def cz_patch(shape, bend, decay, about, rest=0.06):
    return {"about": about,
            "synth": {"env": {"bend": f"1ms {bend} 0 120ms"},
                      "layers": [{"type": "pd", "pd": {"shape": shape, "amount": {
                          "value": rest, "mod": [{"src": "env.bend", "amount": 0.72}]}}}],
                      "amp": {"a": "2ms", "d": decay, "s": 0, "r": "300ms"}}}


C9_CZSAW = cz_patch("saw", "260ms", "1.1s", "chirper-two: a CZ saw-bend pluck - struck bright, relaxing to a soft saw", 0.2)
C9_CZSQ = cz_patch("square", "200ms", "0.9s", "chirper-two: a CZ square-bend pluck - hollow, a pan struck by a computer")
# T9_R16 = space (v16, whole-song round). ORBITS YOU CAN STAND INSIDE. A song about orbits finally has one in the
# room (wM's `orbit` fx, after Chowning's moving sources, 1971; new to this song): the period-eight chord - already an
# orbit voiced by an orbit (wave terrain) - circles the listener's head, a lap every ~16 s, darker behind; and the
# Henon canon's two coordinates, x on the xylophone and y on the marimba, circle on opposite sides of the head (phase
# 0 and 0.5), so the strange attractor is a pair of points going round you, never meeting. And the mix answers the
# album envelope by its signed worst band: t9 was SHORT at 114-133 Hz (-8.6 dB) and over at 292-400 Hz and 1.9 kHz,
# so the master gains a 130 Hz lift (+3 dB), a 300 Hz cut (-2 dB), a 1.9 kHz cut (-1.5 dB), and its 5 kHz shelf
# softens (-5 -> -4 dB); the worst band was then 44 Hz (-7.4 dB short), so a 45 Hz lift (+3 dB) too. Spectrum
# 91.0 -> 99.9 (s0). T9_R16=none reproduces v15.
R16 = os.environ.get("T9_R16", "space")
# T9_R17 = route (v17, whole-song round). ONE VOICE WALKS THE WHOLE ROUTE. wM's `type: chaos` (an audio-rate
# Rossler attractor, 1976, whose loop is the note's pitch) holds the BP root for the entire song - one note, one
# voice - and an automation lane walks its `amount` along the logistic map's own road, section by section: a plain
# tone in ONE; at TWO the period doubles and a subharmonic an octave down appears; FOUR and EIGHT push it further;
# CHAOS lets it go; the WINDOW - the map's period-three island inside chaos - pulls it back almost to order; the
# STORM is the classic attractor (0.93); it settles and ends a plain tone again. The synth does with its waveform
# what the song does with its notes. axis x (a near-sine with a chaotic flutter, not the buzzy z spikes).
# Held as one note the whole song it cost 0.9 (s0 96.77: a +11 dB bump at 213 Hz and variety 97 - one sustained tone
# blurs every section); so it SNAPSHOTS: the voice enters at each section's start and holds through ~60% of it at the
# section's amount (T9_ROUTE_MODE=hold for the single note). T9_R17=none reproduces v16.
R17 = os.environ.get("T9_R17", "route")
C9_ROUTE = {"about": "chirper-two: a Rossler chaotic oscillator (axis x) whose amount rides the track's auto.route lane",
            "synth": {"layers": [{"type": "chaos", "chaos": {"system": "rossler", "axis": "x",
                                                             "amount": {"value": 0.0, "mod": [{"src": "auto.route", "amount": 1}]}}}],
                      "filters": [{"kind": "lp", "cutoff": 2400, "q": 0.5}],
                      "amp": {"a": "6s", "s": 1, "r": "4s"}}}
ROUTE = {"one": 0.0, "two": 0.3, "four": 0.45, "eight": 0.55, "chaos": 0.8, "window": 0.35, "storm": 0.93,
         "settle": 0.2, "end": 0.0}
# T9_R18 = intermit (v18, section round on w7, 2:44-3:10: the end of chaos, "little new vs w6"). INTERMITTENCY. Just
# below the period-three window (r = 3.8284) the logistic map is not uniformly chaotic: it settles into a near-perfect
# three-cycle for a while (a "laminar" phase), then bursts into chaos, then settles again, at random-seeming lengths
# (Pomeau and Manneville, 1980). Here the map itself is iterated once per sixteenth at r = 3.8272 across the
# chaos's last fifteen bars, and wherever it is laminar - each iterate within 0.02 of the one three steps back - a
# buzzy periodic blip (a Rossler oscillator at amount 0.12, still orderly, its spiky z axis) plays the iterate in BP,
# and the Henon canon ducks 12 dB under it; in the bursts the Henon pair has the floor. The three-cycle that the
# window will lock into is heard first in these flashes. Generated, not placed. T9_R18=none reproduces v17.
R18 = os.environ.get("T9_R18", "intermit")
C9_LAM = {"about": "chirper-two: a Rossler oscillator (axis z, spiky) held periodic (amount 0.12), struck short",
          "synth": {"layers": [{"type": "chaos", "chaos": {"system": "rossler", "axis": "z", "amount": 0.12}}],
                    "filters": [{"kind": "lp", "cutoff": 5000, "q": 0.5}],
                    "amp": {"a": "2ms", "d": "180ms", "s": 0, "r": "60ms"}}}
# T9_R19 = cz (v19, palette round). THE BASS FOLLOWS THE MAP. The sub-sine bass (an album staple, 4 songs) becomes
# the song's own CHAOS BASS: a Rossler oscillator on its x axis - nearly a sine - whose amount rides the same route
# lane as the route voice, scaled down (x0.55): pure through one/two/four, a flutter in eight, a rough chaotic grain
# in chaos and the storm, clean again as it settles. Through the same fold drive and filters, same level. The ground
# under the song is now a strange attractor too - TRIED AND OFF (T9_R19_BASS=on): s0 90.31, recurrence 98 -> 49
# (returns 1, sections 9). The bass is what makes the sections come back; a bass that changes character with each
# section takes the song's memory away. What stays: THE PAN ANSWERS - the Henon canon's y voice moves from the
# marimba (an album staple, 3 songs) to the library's steel pan (unused on the album since v15 turned t9's own pan
# into a CZ patch), level-matched -12 dB; x stays on the xylophone. T9_R19=none reproduces v18.
R19 = os.environ.get("T9_R19", "cz")
R19BASS = os.environ.get("T9_R19_BASS", "off")   # the chaos bass: s0 90.31 - recurrence 49 (the bass is what returns)
C9_CBASS = {"about": "chirper-two: a Rossler chaos bass (axis x), amount on the track's auto.route lane",
            "synth": {"layers": [{"type": "chaos", "chaos": {"system": "rossler", "axis": "x",
                                                             "amount": {"value": 0.0, "mod": [{"src": "auto.route", "amount": 1}]}}}],
                      "amp": {"a": "4ms", "d": "300ms", "s": 0.8, "r": "120ms"}}}
# T9_R20 = cycle (v20, section round on w5, 1:49-2:17, beats 256-320: the second half of EIGHT, "static, little new
# vs w4"). Two events where the period-8 orbit was a held chord over an unchanged 5/4 floor.
# EIGHT TO THE BAR (T9_R20_FLOOR=eight): from the eight section's ninth bar the 5/4 floor becomes eight hits on
# quarter-note triplets, the period-8 cycle's high values on the kick and its low values on the snare, and the hats
# leave sixteenths for TRIPLET eighths, loud where the cycle is high (T9_R20_HATS). The bar plays the cycle.
# (T9_R20_FLOOR=rotate - the grouping turning one group per bar - was too small to hear: groove change 0.018; the
# triplet hats alone, too; the loud onsets have to move: eight-to-the-bar gives 0.085, a new groove.)
# THE ATTRACTOR ASSEMBLES: the eight values of the period-8 cycle no longer arrive at once as a 54-beat chord; they
# enter one per bar in the order the map visits them, each held to the same end, so the chord builds across eight
# bars, a value at a time.
# THE EIGHTH STEP (T9_R20_VOX): the voice that later sings "it comes back in threes" first turns up here, twice, as
# the chord assembles: "eight steps and I'm standing where I stood" (`chirp tts --sing "E4/8 A3 D4 B3 E4 A3 D4 B3
# E4/2" --bpm 140 --seed 9 --humanize 0.5 --hz`, src/t9/eight.json) - its tune alternates high and low like the
# period-8 orbit and lands on the note it left. T9_R20=none reproduces v19.
R20 = os.environ.get("T9_R20", "cycle")
# T9_R21 = split (v21, section round on w4, 1:22-1:49: four into EIGHT, "static" - motion 0.025, the song's
# stillest window: the lead's period-4 loop, then the period-8 loop, on one reed). ONE VOICE BECOMES TWO. At the
# bifurcation into eight the map's two branches part: the high values (>= 0.7) leave the reed for a 1983
# KARPLUS-STRONG string (wM's `ks`: a noise burst in a one-period loop smoothed into a pluck, stretched to ring),
# hard right, while the low values stay on the reed, moved left. The orbit is heard as what it is - two
# interleaved sequences - and it is the first plucked string in the song.
# THE FLOOR OPENS AT THE FORK (T9_R21_FORK): the last bar of FOUR loses its floor - kick, sub, bass, its plucked
# double and the CZ ostinato drop out (the bass was the stillest loud part of the window: spread 0.4 dB), leaving
# the reed's period-4 loop over the hats - and everything lands together on the bifurcation, where the voice
# splits. T9_R21=none reproduces v20.
R21 = os.environ.get("T9_R21", "split")
C9_KS = {"about": "chirper-two: the 1983 Karplus-Strong string, stretched to ring, the burst a little dark",
         "synth": {"layers": [{"type": "ks", "ks": {"blend": 1.0, "stretch": 2}, "bright": 0.45}],
                   "amp": {"a": "1ms", "d": "900ms", "s": 0, "r": "250ms"}}}
# T9_R22 = crisis (v22, section round on w9, 3:35-4:00: the STORM's entry, "little new vs w8" - groove change
# 0.074, just under new). THE ATTRACTOR FILLS THE INTERVAL. At r = 4 the map's crisis spreads its orbit over all of
# [0, 1]; the song only ever played the top of it (the reed is silent under 0.42). Now, through the storm, the
# bottom plays too: every iterate under 0.42 strikes the Karplus-Strong string a tritave down, hard left - the voice
# that split at the fork in eight comes back, fallen, and the storm sounds the whole interval from the floor to the
# top. And the storm is let in by ONE BEAT OF SILENCE: everything stops on the last beat of the window, then the
# storm. T9_R22=none reproduces v21.
R22 = os.environ.get("T9_R22", "crisis")
# T9_R23 = two (v23, section round on w2, 0:27-0:54: one into TWO, "static"). THE FIRST FORK, SUNG. The map's first
# bifurcation (period 1 -> 2) now gets what the fork into eight got: the last bar of ONE loses its floor (kick,
# sub, bass, its plucked double), and everything lands on the split. And the voice, which in eight will sing "eight
# steps and I'm standing where I stood" and in the window "it comes back in threes", turns up first here, twice,
# in the 7/8: "every other morning I'm someone else" on a tune that does nothing but alternate - D4 B3 D4 B3 ...
# - a period-2 orbit sung (chirp tts --sing "D4/8 B3 D4 B3 D4 B3 D4 B3 D4 B3/4 D4/2" --bpm 140 --seed 9
# --humanize 0.3 --hz, src/t9/other.json; ASR raw: "ever in the morning on someone else"; in the song, with the
# delay cut to mix 0.1 - at 0.22 the 3/16 ping-pong smeared it to nothing - "never be a normal name on someone
# else"). The song's three
# sung lines now name its periods: two, eight, three. T9_R23=none reproduces v22.
R23 = os.environ.get("T9_R23", "two")
# T9_R24 = choir (v24, palette round). THE VOICES LAND IT. The last twelve beats' held D (D4 + D5 for t10 to catch)
# was the library's choir-classic - a saw and noise imitating a choir. Now it is sung: four real voices from the
# song's own voice engine, each its own take (chirp tts "on" --sing "<note>/1 _ _" --bpm 154 --seed 9..12
# --humanize 0.45 --hz; src/t9/on1-4.json), D3 A3 D4 F#4, entering a beat apart from the bottom up and spread
# across the stereo field, all on one word - "on" - the album's last word sung under the map's final settling. The
# same voice that sang "every other morning", "eight steps" and "comes back in threes" ends the song as a choir.
# The choir-classic hold stays under it, 2 dB down (T9_R24_KEEP=off drops it: the TTS vowels end before the tail
# and t10 catches the held D4 - the out-join's 292 Hz band fell to -43.6 dB without it, s0 97.65).
# T9_R24=none reproduces v23.
R24 = os.environ.get("T9_R24", "choir")
# T9_R25 = branches (v25, whole-song round). THE CHOIR SINGS THE DIAGRAM. A wordless CHANT choir (wM's `fof`) holds
# the map's attractor as a chord, every four bars, all the way through: in `one` one voice (the fixed point), in
# `two` two, in `four` four, in `eight` eight - the bifurcation diagram sung, each branch a singer - then in the
# chaos a different handful of iterates every two bars, in the window three again ("it comes back in threes"), the
# storm a crowd re-voiced every bar, and in the settle the choir folds back to two and to one as r falls. Each orbit
# value x goes to the map's own pitch mapping a tritave down (146.7 Hz * 3^((x - 0.3) * 16/13)), snapped to the
# song's Bohlen-Pierce lambda scale, and is sung by whichever voice owns that register (bass, tenor, alto,
# soprano). The vowel opens with the period - "oo" at one, through "oh", to "ah" in the chaos - on one shared lane.
# T9_R25=none reproduces v24.
R25 = os.environ.get("T9_R25", "branches")
BR_PATCHES = {}
# T9_R26 = cascade (v26, section round on w8, 3:10-3:35: the period-3 window, never focused, "static"). FIRST, THE
# CHOIR STEPS BACK: v25's whole-song CHANT chords were the album's move of the hour (Harry, 23:55: "keep things
# varied. not all singing"), and t9's singing is its three lines and the sung "on" at the end - the diagram goes
# (T9_R26_BR=on keeps it). THEN THE WINDOW DOES WHAT WINDOWS DO. In the real map the period-3 window is a small copy
# of the whole diagram: three doubles to six (r 3.8415), six to twelve (3.8442), and the window fills with its own
# chaos before the crisis (3.857) throws the orbit out into the storm. Now the window plays it: ten bars of period 3
# (r 3.835), four of 6 (3.8425), two of 12 (3.8445), two of the window's own chaos (3.853) - the lead, the kicks
# on its peaks and the hats all follow, and where three becomes six the floor opens (no kick or snare for the four
# bars of period 6 at first - two bars, T9_OPEN_BARS (all four cleared w8 too but cost 0.06: the kick carries the low
# end) - the doubled orbit alone; T9_R26_OPEN=off keeps the floor). The rest of the song's orbit is untouched (the window runs on its own copy
# of x; the main state advances as before, so the storm and the settle are note-for-note v25).
# T9_R26=none reproduces v25.
R26 = os.environ.get("T9_R26", "cascade")
# T9_R27 = scanned (v27, palette round). MATHEWS' RING. Two library sounds give way to scanned synthesis - Max Mathews
# and Bill Verplank's ring of masses and springs read as a wavetable (wM's library patches, engine 502b6b8d): the
# father of computer music's last instrument, in the album's love letter to the machine. The D bell that keeps
# landing through the song (and rings at the end for t10 to catch) is struck on the ring (scanned-mallet: a narrow
# strike splitting into ripples that run round and smooth away - it mellows and shimmers as it dies) instead of the
# handpan; and the chaos's cross-morphed pad breathes on it (scanned-breath: a slow hand leaning in and out every
# seven seconds) instead of pad-glass. Level-matched to what they replace. T9_R27=none reproduces v26.
R27 = os.environ.get("T9_R27", "scanned")
# T9_R28 = odd (v28, palette round). ODD HARMONICS FOR AN ODD SCALE. Bohlen-Pierce was built for timbres with only odd
# partials - its consonances are 3:5:7:9, the clarinet's - and the song's lead was always a clarinet; but its pad,
# holding the chords from the first bar to the last, was pad-glass, a full-spectrum sine pad whose even partials rub
# against the tritave. Now the pad is a Chebyshev waveshaper with odd harmonics only (wM's shaper-reed: 1, 0, .55,
# 0, .3, 0, .16 - Le Brun and Arfib's hollow reed), its brightness opening with a slow breath: the chords sit in
# their own scale's acoustics. The pad's first and last chords (16 beats each end) stay glass: the joins to t8 and
# t10 heard the reed (in-join spectral 7.1 -> 9.3, s0 97.45 with the whole pad on it). Level-matched: the reed
# takes pad-glass's envelope, velocity response (0.3), chorus and hall. (Opt-in T9_R28_BRASS=on: the settle's two
# converging lines on wM's shaper-brass, Risset's waveshaped trumpet, -6 dB - its delay tail reached the out-join,
# spectral 7.34 -> 8.14.) T9_R28=none reproduces v27.
R28 = os.environ.get("T9_R28", "odd")
R28B = R28 == "odd" and os.environ.get("T9_R28_BRASS", "off") == "on"
# T9_R29 = sync (v29, section round on w10, 4:00-4:25: the storm's second half, "little new vs w9"). THE CROWD FINDS
# ITS PITCH. Late in the storm a swarm comes in - wM's Kuramoto layer (Kuramoto 1975, the maths of synchrony: fireflies,
# pacemaker cells, applause falling into step): sixteen saw oscillators each at its own frequency round D3 and the
# tritave above it (A4, BP's 3:1), uncoupled - a beating, detuned crowd under the chaos. When the map settles, the
# coupling rises past critical, and the crowd locks onto the note: the orbit's collapse from chaos to a fixed point
# heard a second way, as synchrony - locking in the eight beats either side of the settle's door, and gone sixteen
# beats in (held through the whole settle, -14 dB, the drone hid the settle's return: recurrence 98 -> 68, s0 93.2).
# T9_R29=none reproduces v28.
R29 = os.environ.get("T9_R29", "sync")
# T9_R30 = arc (v30, whole-song round). THE LYAPUNOV ARC. The song ran at one loudness from the second section to the
# settle (4.2 dB of dynamics; the album spans 7-20), and "developed least" but one. Now its level follows the map's
# Lyapunov exponent - how fast two nearby orbits fly apart, negative while the orbit is periodic and positive in chaos:
# the doublings sit back and creep up as each period doubles toward the edge of chaos, chaos arrives a step up, the
# period-3 window (order inside chaos) falls back, the storm (r near 4, where it is largest) is the loudest place in
# the song, and the settle fades as the orbit converges. It deepens the master's existing level lane (after the glue,
# before the limiter): T9_ARC, dB at one, two, four, eight, just before chaos, chaos, the window, the storm, the
# settle's start, the end. (A lane on every track instead - T9_R30=tracks - was halved by the glue compressors;
# starting the song at -5.5 dB widened the in-join from 5.8 to 7.1 dB, so the first section holds at -3.5.)
# Window levels -16.6 .. -11.4 dB: 5.4 dB of dynamics (was 4.2). T9_R30=none reproduces v29.
R30 = os.environ.get("T9_R30", "arc")
# T9_R31 = sweep (v31, whole-song round). THE PARAMETER MOVES. The period sections each held r still (2.9, 3.2, 3.5,
# 3.56), so each played one fixed loop for twenty bars - the static windows of the song's first half. Now r sweeps
# through each regime the way the bifurcation diagram is read, left to right: `one` creeps up toward 3 (the fixed
# point's pull weakening), `two` starts just past the first split, so its two notes begin a step apart and draw away
# from each other bar by bar until they are six apart; `four` starts at its own split (3.449), the two branches
# opening into four; `eight` starts at its split (3.544) and stops just short of sixteen (3.5644). The orbit carries
# straight on from section to section, so every bar is the map's honest next iterate. (Measured, and chaotic in its
# own way: the orbit's phase carries into every later section, so partial sweeps move recurrence a lot - `two` alone
# 95.59, `four` from 3.5 95.74; all four, each from its own split, 97.589 with returns 3 -> 4. T9_SWEEP picks them.)
# T9_R31=none reproduces v30.
R31 = os.environ.get("T9_R31", "sweep")
# T9_R32 = floor (v32, section round on w7, 2:44-3:10: chaos's second half, "static, little new vs w6"). THE FLOOR
# KNOWS. Since v18 the map at r = 3.8272 runs under chaos's last fifteen bars, flickering between laminar three-cycles
# and bursts, but the drums went on straight through it - the kick alone sits two dB under the whole mix there. Now
# the floor follows the intermittency: wherever the map holds a three-cycle for two beats or more, kick, snare, hats
# and ride fall away (-20 dB) and the three-cycle's blip, the bass and the pads are left; when it bursts, the floor
# comes back. Five laminar stretches of 2 to 6.5 beats, at the map's own irregular times - the last one running into
# the window, which keeps the three for good. Generated, not placed. T9_R32=none reproduces v31.
R32 = os.environ.get("T9_R32", "floor")
# T9_R33 = fork4 (v33, section round on w3, 0:54-1:22: two into FOUR, "static"). THE MISSING FORK. The first split
# (one -> two) and the third (four -> eight) each lost their floor for the bar before and landed on the split; the
# second (two -> four) just went on. Now it does the same: the last 7/8 bar of TWO drops kick, sub, bass, the plucked
# double and the ostinato, and everything lands on four. And four gets its line, as two and eight have theirs, sung by
# the same voice on a tune that cycles in fours (D4 B3 E4 A3, twice, home to D4): "two coats, and each one has a
# lining" - each of the two things it had now has its own inner double (chirp tts --sing "D4/8 B3 E4 A3 D4 B3 E4 A3/4
# D4/2" --bpm 140 --seed 12 --humanize 0.3 --hz, src/t9/coats.json; ASR raw: "two coats of people and pasts are
# lying"). Twice, bars 2 and 10. T9_R33=none reproduces v32.
R33 = os.environ.get("T9_R33", "fork4")
# T9_R34 = sync (v34, FINAL PASS: the existing plan from v29). THE CROWD BRIGHTENS AS IT AGREES. The Kuramoto swarm that
# finds its pitch at the settle's door went darker as it locked (a locked swarm is purer: the engine measures the
# centroid falling about 390 -> 170 Hz), so the moment of agreement sank. Now its low-pass reads the swarm's own
# coherence (the `sync` mod, adopted b8f9d6b1): from 700 Hz, opening four octaves with the order parameter, so the
# agreement no longer sinks (solo swarm centroid, crowd -> locked: v33 450 -> 283 Hz; now 348 -> 352; 1400 Hz and 1.5
# octaves only halved the fall). And the seam into t10, which opens on a D4 toll: t9's last three seconds had 34 dB less
# at 292 Hz than t10's first, so the closing D bell is struck harder (vel 66 -> 110) and once more four beats from the
# end - and, because the album plays the files back to back (no overlap), a plain D4 of the song's own holds from eight
# beats before the end and lets go only as the file ends (a 1.8 s release through the render's tail), so the toll
# comes in on a D that is still sounding rather than into a gap. T9_R34=none reproduces v33.
R34 = os.environ.get("T9_R34", "sync")
if R31 == "sweep":
    _sw = {"one": (2.8, 2.98), "two": (3.05, 3.42), "four": (float(os.environ.get("T9_SW_FOUR0", "3.452")), 3.543), "eight": (3.5445, 3.5643)}
    _which = os.environ.get("T9_SWEEP", "one,two,four,eight").split(",")
    SECS = [(nm, nb, mt, *(_sw[nm] if nm in _sw and nm in _which else (a, b))) for nm, nb, mt, a, b in SECS]
C9_SWARM = {"about": "chirper-two: a Kuramoto swarm, 16 saws spread 60 cents, coupling on the track's sync lane",
            "synth": {"layers": [{"type": "kuramoto", "kuramoto": {
                "count": 16, "wave": "saw", "spread": float(os.environ.get("T9_SWARM_SPREAD", "60")),
                "coupling": {"value": 0, "mod": [{"src": "auto.sync", "amount": 3}]}}}],
                "filters": ["hp cutoff=120", "lp cutoff=2200 q=0.4"],
                "amp": {"a": "3s", "s": 1, "r": "2.5s"}}}
if R34 == "sync":   # the low-pass opens with the swarm's coherence
    C9_SWARM["synth"]["filters"] = ["hp cutoff=120",
                                    {"kind": "lp", "q": 0.4,
                                     "cutoff": {"value": float(os.environ.get("T9_SYNC_LP", "700")),
                                                "mod": [{"src": "sync", "amount": float(os.environ.get("T9_SYNC_OCT", "4"))}]}}]
WINDOW_R = [float(v) for v in os.environ.get("T9_WIN_R", "3.835*10,3.8425*4,3.8445*2,3.853*2").replace("*", " ").replace(",", " ").split()[0::2]]
WINDOW_N = [int(v) for v in os.environ.get("T9_WIN_R", "3.835*10,3.8425*4,3.8445*2,3.853*2").replace("*", " ").replace(",", " ").split()[1::2]]
WINDOW_SCHED = [r_ for r_, n_ in zip(WINDOW_R, WINDOW_N) for _ in range(n_)]
def c9_fof(voice, vib):
    return {"about": f"chirper-two: a CHANT/FOF {voice} singing the logistic map's branches",
            "synth": {"layers": [{"type": "fof", "fof": {"voice": voice, "vowel": "u>a", "attack": 8,
                                                         "morph": {"value": 0.0, "mod": [{"src": "auto.mouth", "amount": 1}]}}}],
                      "pitch": {"value": 0, "mod": [{"src": "lfo.vib", "amount": vib}]},
                      "lfo": {"vib": {"wave": "sine", "rate": "5.5hz"}},
                      "amp": {"a": "350ms", "d": "600ms", "s": 0.85, "r": "1.2s"}}}
TERRAIN_GAIN = os.environ.get("T9_TERRAIN_GAIN", "-14.5dB")
EYE = float(os.environ.get("T9_EYE", "636"))   # where the drum bus drops out (to 640b)
C9_GENDY = {"about": "chirper-two: a gendyn squall - level and segment-length steps both ride velocity, wide spread, "
                     "Cauchy jumps: grain that slides in pitch.",
            "synth": {"layers": [{"type": "gendyn", "gendyn": {
                "points": 12,
                "amp": {"value": 0.01, "mod": [{"src": "vel", "amount": 0.1}]},
                "time": {"value": 0.04, "mod": [{"src": "vel", "amount": 0.22}]},
                "spread": 1.2, "dist": "cauchy"}}],
                "filters": [{"kind": "lp", "cutoff": 3000, "q": 0.5}],
                "amp": {"a": "1.5s", "s": 1, "r": "2s"}}}
SUB_SECS = {"both": ("window", "settle"), "settle": ("settle",), "none": ()}[os.environ.get("T9_SUB", "both")]
C9_BPCLAR = {
    "about": "chirper-two: a Bohlen-Pierce clarinet - the reed on a cylindrical bore pushed harder and brighter, a little "
             "airier, with a quiet sine at exactly 3:1 (the tritave BP repeats at) on every note; ^sub subtone.",
    "synth": {
        "layers": [
            {"name": "reed", "type": "wind", "exciter": "reed",
             "pressure": {"value": float(os.environ.get("T9_BPC_PRESS", "0.46")), "mod": [{"src": "vel", "amount": 0.3}, {"src": "expr.sub", "amount": -0.3}]},
             "breath": {"value": 0.22, "mod": [{"src": "expr.sub", "amount": 0.55}]},
             "bright": {"value": float(os.environ.get("T9_BPC_BRIGHT", "0.38")), "mod": [{"src": "vel", "amount": 0.25}, {"src": "expr.sub", "amount": -0.35}]}},
            {"name": "tritave", "type": "osc", "wave": "sine", "ratio": 3,
             "level": {"value": os.environ.get("T9_TRITAVE", "-20dB"), "mod": [{"src": "expr.sub", "amount": -12}]}},
            {"name": "tongue", "type": "noise",
             "level": {"value": "-70dB", "mod": [{"src": "env.t", "amount": 40}, {"src": "vel", "amount": 8}]}}],
        "env": {"f": {"a": "30ms", "d": "350ms", "s": 0.75, "r": "150ms"}, "t": {"a": "2ms", "d": "30ms", "s": 0}},
        "pitch": {"value": 0, "mod": [{"src": "rand", "amount": 0.01}]},
        "filters": ["hp cutoff=90",
                    {"kind": "lp", "cutoff": {"value": os.environ.get("T9_BPC_LP", "3.6k"), "mod": [{"src": "vel", "amount": 0.8}, {"src": "expr.sub", "amount": -1}]}, "q": 0.7},
                    "peak cutoff=1.5k q=1.4 gain=2dB", "peak cutoff=3.2k q=2 gain=1dB"],
        "amp": {"a": "30ms", "s": 1, "r": "120ms", "curve": 3}},
    "play": {"gate": 0.97, "vel_sens": 0.5, "humanize": {"time": "6ms", "vel": 0.05}},
    "fx": ["reverb kind=room decay=1.4s mix=0.2"],
    "gain": "-3dB"}
R7BASS = os.environ.get("T9_R7_BASS", "layer") if R7 == "lpg" else "none"   # lpg | layer | sub
R7DIZI = os.environ.get("T9_R7_DIZI", "0") == "1" and R7 == "lpg"
C9_LPG = {"about": "chirper-two: a West Coast low-pass-gate bass - triangle plus its octave, folded, through one "
                   "envelope that opens the filter and the amp together and lets both fall (a struck, vocal pluck).",
          "synth": {"layers": [{"wave": "triangle"}, {"wave": "sine", "ratio": 2, "level": "-10dB"}],
                    "env": {"lpg": {"a": "1ms", "d": "320ms", "s": 0, "curve": 3}},
                    "filters": [{"kind": "lp", "q": 1.4,
                                 "cutoff": {"value": 140, "mod": [{"src": "env.lpg", "amount": 4.5}, {"src": "vel", "amount": 1.0}]}}],
                    "drive": {"value": 0.35, "mod": [{"src": "vel", "amount": 0.3}]},
                    "amp": {"a": "1ms", "d": "520ms", "s": 0, "r": "90ms", "curve": 3}},
          "play": {"vel_sens": 0.6}}
C9_PULSE = {"about": "chirper-two: a one-bit loudspeaker voice - a very narrow pulse (6%, wider with velocity), crushed, "
                     "nothing smoothing it: a machine driving its speaker directly.",
            "synth": {"layers": [{"wave": "pulse", "width": {"value": 0.06, "mod": [{"src": "vel", "amount": 0.12}]}}],
                      "filters": ["hp cutoff=180", "lp cutoff=7k"],
                      "amp": {"a": "0.5ms", "d": "80ms", "s": 0, "r": "20ms"}},
            "fx": ["crush bits=5 rate=16kHz"],
            "play": {"vel_sens": 0.7}}
SING = []


SING8 = []
SING2 = []


def sing(at, scale=1.0, fn="sing.json", into=None):
    src = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t9", fn)))["tracks"][0]
    for nt in src["notes"]:
        m = round(69 + 12 * math.log2(float(nt["pitch"].rstrip("hz")) / 440))
        d = {"at": round(at + nt["at"], 4), "len": nt["len"], "ph": nt["ph"], "pitch": f"m{m}",
             "vel": round(nt["vel"] * scale, 3)}
        if nt.get("expr_path"):
            d["expr_path"] = nt["expr_path"]
        (SING if into is None else into).append(d)
    return src["patch"]
GROUPS = {(4, 4): [4, 4, 4, 4], (7, 8): [4, 4, 6], (5, 4): [6, 4, 6, 4], (6, 8): [6, 6], (11, 8): [6, 6, 6, 4]}  # 16ths


def bp(deg, base):
    o, d = divmod(deg, 9)
    return base + o * TRITAVE + LAMBDA[d] * BP


def mm(m):
    return f"m{m:.3f}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self, total):
        ev = sorted(self.ev, key=lambda x: (x[0], -x[3]))
        merged = []
        for x in ev:
            if x[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - x[0]) < 1e-3:
                continue
            merged.append(x)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


def build():
    rng = random.Random(9)
    names = ("kick", "snare", "hats", "ride", "lead", "blip", "bass", "pad", "padx", "bell", "chop", "ks", "ksl")
    T = {k: Track(k) for k in names}
    x, y = 0.2, 0.71
    pos = 0.0
    secs = []
    trace = []
    for name, nbars, meter, r0, r1 in SECS:
        secs.append((name, pos, nbars, meter))
        steps = int(round(meter[0] * 16 / meter[1]))  # sixteenths a bar
        groups = GROUPS[meter]
        R20F = os.environ.get("T9_R20_FLOOR", "eight") if R20 == "cycle" else "none"
        if name == "eight" and i >= 8 and R20F == "rotate":
            rot = (i - 8) % len(groups)
            groups = tuple(groups[rot:]) + tuple(groups[:rot])
        for i in range(nbars):
            start = pos
            frac = i / max(1, nbars - 1)
            r = r0 + (r1 - r0) * frac
            xs = []
            if R26 == "cascade" and name == "window" and i < len(WINDOW_SCHED):
                if i == 0:
                    xw = x
                for s in range(steps):   # the window's own copy of the orbit; the main state goes on as before
                    x = r * x * (1 - x)
                    xw = WINDOW_SCHED[i] * xw * (1 - xw)
                    xs.append(xw)
            else:
                for s in range(steps):
                    x = r * x * (1 - x)
                    xs.append(x)
            trace.append((name, i, [round(v, 3) for v in xs[:8]]))
            # ---- the lead: the map, one sixteenth per iterate (silent under 0.42) ----
            if not (name == "one" and i < 2):
                for s, v in enumerate(xs):
                    if R22 == "crisis" and name == "storm" and 0.03 < v <= 0.42:   # the bottom of the interval
                        T["ksl"].add(start + s * 0.25, 0.5, mm(bp(min(8, int(v / 0.42 * 9)), 57 - TRITAVE)),
                                     int(60 + 50 * (0.42 - v)), "?0.85")
                    if v > 0.42:
                        deg = max(0, min(13, int((v - 0.3) * 16)))
                        if R21 == "split" and name == "eight" and v >= float(os.environ.get("T9_KS_SPLIT", "0.7")):
                            T["ks"].add(start + s * 0.25, 0.5, mm(bp(deg, 57)), int(62 + 46 * v))
                            continue
                        T["lead"].add(start + s * 0.25, 0.24, mm(bp(deg, 57)), int(58 + 50 * v),
                                      "^sub=0.7" if R10 == "bpclar" and name in SUB_SECS else "")
            # ---- drums: grouped kicks, a snare on the last group, map-made accents and ratchets ----
            groove = name not in ("one",) or i >= 8
            if groove and R20F == "eight" and name == "eight" and i >= 8:
                # eight hits to the 5/4 bar on quarter-note triplets: the cycle's high values on the kick, low on the snare
                for k in range(8):
                    v = xs[k % len(xs)]
                    if v >= 0.6:
                        T["kick"].add(start + k * 2 / 3, 0.5, "k", int(84 + 30 * v))
                    else:
                        T["snare"].add(start + k * 2 / 3, 0.4, "s", int(70 + 40 * v))
                for s, v in enumerate(xs):
                    if s % 4 == 2:
                        T["ride"].add(start + s * 0.25 + 0.01, 0.5, "rd", 60, "?0.9")
            elif groove and name != "settle" or (name == "settle" and i < 20):
                g0 = 0
                for gi, g in enumerate(groups):
                    T["kick"].add(start + g0 * 0.25, 0.5, "k", 112 if gi == 0 else 100)
                    g0 += g
                T["snare"].add(start + (steps - groups[-1]) * 0.25, 0.4, "s", 98)
                for s, v in enumerate(xs):
                    if v > 0.93 and s % 2 == 1 and name in ("chaos", "storm", "window"):
                        T["kick"].add(start + s * 0.25, 0.25, "k", 90)
                    if 0.45 < v < 0.52 and name in ("chaos", "storm"):
                        T["snare"].add(start + s * 0.25, 0.25, "s", 80, "^r=3")
                    if R20 == "cycle" and name == "eight" and i >= 8 and os.environ.get("T9_R20_HATS", "on") == "on":
                        pass   # the hats go to triplets below
                    elif s % 2 == 1 or name in ("chaos", "storm", "window"):
                        T["hats"].add(start + s * 0.25 + 0.01, 0.1, "h", int(40 + 40 * v), "?0.85")
                    if s % 4 == 2:
                        T["ride"].add(start + s * 0.25 + 0.01, 0.5, "rd", 60, "?0.9")
                    if R4 == "break" and name in ("chaos", "storm"):   # the map chops the break
                        piece = ("g" if 0.25 < v <= 0.45 else "s2" if 0.52 <= v < 0.62 else
                                 "oh" if 0.8 < v <= 0.93 and s % 2 == 0 else None)
                        if piece:
                            T["chop"].add(start + s * 0.25, 0.25, piece,
                                          {"g": 52, "s2": 74, "oh": 58}[piece] + int(20 * v))
            if R20 == "cycle" and name == "eight" and i >= 8 and os.environ.get("T9_R20_HATS", "on") == "on" and groove:
                for k in range(int(steps / 4 * 3)):   # triplet eighths, loud where the cycle is high
                    v = xs[(k * 7) % len(xs)]
                    T["hats"].add(start + k / 3 + 0.01, 0.1, "h", int(36 + 44 * v), "" if k % 3 == 0 else "?0.85")
            # ---- polytempo: blips on a 5:4 grid from the map's twin ----
            if name not in ("one", "two"):
                k, t = 0, 0.0
                bar_beats = steps / 4
                while t < bar_beats - 1e-6:
                    y = min(4.0, r + 0.02) * y * (1 - y)
                    if y > 0.62:
                        T["blip"].add(start + t, 0.15, mm(bp(int(y * 9) + 9, 57)), int(50 + 40 * y), "?0.8")
                    t += 0.2
                    k += 1
            # ---- the bass on a 3:4 grid, folded ----
            if name not in ("one",) or i >= 12:
                xb = xs[0]
                deg = int(xb * 5)
                t = 0.0
                bar_beats = steps / 4
                while t < bar_beats - 1e-6:
                    T["bass"].add(start + t, 1.1, mm(bp(deg, 33)), 96 if t == 0 else 82)
                    t += 4 / 3
            # ---- BP 3:5:7 chords on the glass pad, every two bars ----
            if i % 2 == 0 and name in ("one", "four", "window", "settle", "eight"):
                root = int(xs[0] * 5)
                base = bp(root, 57)
                T["pad"].add(start, steps / 4 * 2 - 0.1, ",".join(mm(base + st * BP) for st in (0, 6, 10)), 64)
            if R3 == "sing" and ((name == "window" and i in (2, 10)) or (name == "settle" and i == 22)):
                sing(start, 0.85 if name == "settle" else 1.0)
            if R3 == "sing" and R23 == "two" and name == "two" and i in (4, 10):
                sing(start, 1.0 if i == 4 else 0.9, "other.json", SING2)
            if R33 == "fork4" and name == "four" and i in (2, 10) and os.environ.get("T9_COATS", "on") == "on":
                sing(start, 1.0 if i == 2 else 0.9, "coats.json", SING2)
            if R3 == "sing" and R20 == "cycle" and name == "eight" and i in (10, 14) \
                    and os.environ.get("T9_R20_VOX", "on") == "on":
                sing(start, 1.0 if i == 10 else 0.9, "eight.json", SING8)
            if R2 == "drift" and i % 2 == 0 and name in ("chaos", "storm"):
                root = int(xs[0] * 5)
                base = bp(root, 57)
                T["padx"].add(start, steps / 4 * 2 - 0.1, ",".join(mm(base + st * BP) for st in (0, 6, 10, 13)), 80)
            if i == 0:
                T["bell"].add(start, 6.0, mm(bp(0, 69)), 70)
            pos += steps / 4
    total = pos
    return total, secs, T, trace


def tempo_map(secs, total):
    pts = []
    for name, s, n, meter in secs:
        p = {"at": f"{s:g}b", "bpm": BPM[name], "meter": f"{meter[0]}/{meter[1]}"}
        if name in ("window",):
            p["ramp"] = True       # chaos ramps 140 -> 150 into the window
        pts.append(p)
    pts.append({"at": f"{total:g}b", "bpm": 132, "ramp": True})  # settle slows to 132
    return pts


def j_even(k):
    return k % 2 == 0


def seconds(tm, total):
    pts = [(float(p["at"][:-1]), p["bpm"], p.get("ramp", False)) for p in tm]
    sec = 0.0
    for (a, b0, _), (b, b1, ramp) in zip(pts, pts[1:]):
        if ramp:
            sec += (b - a) * 60 * math.log(b1 / b0) / (b1 - b0) if b1 != b0 else (b - a) * 60 / b0
        else:
            sec += (b - a) * 60 / b0
    return sec


def main():
    total, secs, T, trace = build()
    st = {n: s for n, s, k, m in secs}
    if R26 == "cascade" and os.environ.get("T9_R26_OPEN", "on") == "on":
        # where three becomes six the floor opens: four bars without kick and snare, the doubled orbit alone
        w0 = st["window"] + 4.0 * WINDOW_N[0]
        w1 = w0 + 4.0 * int(os.environ.get("T9_OPEN_BARS", "2"))
        for nm in ("kick", "snare"):
            T[nm].ev = [e_ for e_ in T[nm].ev if not (w0 <= e_[0] < w1)]
    if R11 == "d":
        T["bell"].ev = [(a, ln, "293.66hz", v, art) for a, ln, h, v, art in T["bell"].ev]
        T["bell"].add(total - 8.0, 8.0, "293.66hz", int(os.environ.get("T9_DBELL_VEL", "110" if R34 == "sync" else "66")))
        if R34 == "sync" and os.environ.get("T9_DBELL2", "on") == "on":   # the last D, struck again into t10's toll
            T["bell"].add(total - 4.0, 4.0, "293.66hz", int(os.environ.get("T9_DBELL2_VEL", "100")))
        dm_in = os.environ.get("T9_D_IN", "m57.000,m62.000,m65.000,m69.000,m74.000")
        dm_out = os.environ.get("T9_D_OUT", "m62.000,m65.000,m67.000,m74.000")
        for k in ("bass", "bpluck", "ksub"):   # the floor leaves before the last D, so it rings alone
            if k in T:
                T[k].ev = [e for e in T[k].ev if e[0] < total - 6.0]
        T["pad"].ev = [(a, ln, dm_in, 120, art) if a < 8.0 - 1e-6 else
                       ((a, ln, dm_out, 84, art) if a >= total - 16.0 - 1e-6 else (a, ln, h, v, art))
                       for a, ln, h, v, art in T["pad"].ev]
    orbit, fill = Track("orbit"), Track("fill")
    o0 = st["eight"] + 8 * 5                      # the eight section's ninth bar (256b): the window
    if R5 == "orbit":
        xs8 = next(xs for name, i, xs in trace if name == "eight" and i == 8)
        hz = sorted(220.0 * 3 ** ((v - 0.3) * 16 / 13) for v in xs8)
        orbit_notes = [{"at": o0, "len": 54.0, "pitch": f"{h:.2f}hz", "vel": 0.57 if k % 2 == 0 else 0.52}
                       for k, h in enumerate(hz)]
        if R20 == "cycle" and os.environ.get("T9_R20_CHORD", "on") == "on":   # one value per 5/4 bar, in visit order
            bl8 = 5.0
            orbit_notes = [{"at": o0 + k * bl8, "len": 54.0 - k * bl8,
                            "pitch": f"{220.0 * 3 ** ((v - 0.3) * 16 / 13):.2f}hz", "vel": 0.6 if k % 2 == 0 else 0.55}
                           for k, v in enumerate(xs8)]
        for k, at in enumerate([o0 + 16 + 0.25 * j for j in range(16)]):   # the fill: 16th ratchets rising
            fill.add(at, 0.25, "s2" if j_even(k) else "g", 50 + 3 * k, "^r=2" if k >= 8 else "")
    dizi = Track("dizi")
    bpl = Track("bpluck")
    if R7BASS == "layer":   # the low-pass gate as the bass's voice, an octave over the sub body it leaves in place
        for a, ln, h, v, art in T["bass"].ev:
            bpl.add(a, min(ln, 0.9), f"m{float(h[1:]) + 12:.3f}", v, art)
    if R7DIZI:
        for a, ln, h, v, art in T["lead"].ev:
            if (st["two"] <= a < st["eight"] or a >= st["settle"]) and v >= 92:
                dizi.add(a, ln, f"m{float(h[1:]) + 12:.3f}", v - 14, art)
    ret, tab = Track("ret"), Track("tab")
    if R9 == "return":
        one, two = next(s for s in SECS if s[0] == "one"), next(s for s in SECS if s[0] == "two")
        hz = lambda v: f"{2 * 220.0 * 3 ** ((v - 0.3) * 16 / 13):.2f}hz"
        xs = 1 - 1 / one[3]
        for a, x0 in ((st["two"] - 16.0, xs - 0.2), (st["two"] - 8.0, xs + 0.18)):
            for i, v in enumerate([x0] + lmap(one[3], x0, 15)):
                ret.add(a + i * 0.5, 0.45, hz(v), max(40, 74 - 2 * i))
        orb = logistic_orbit(two[3], 2)
        bl = 3.5
        for b in range(two[1]):
            a = st["two"] + b * bl
            pat = TABLA[b % 4] if b % 4 != 3 else TABLA[3]
            for i, bol in enumerate(pat):
                if bol == "te":
                    tab.add(a + i * 0.5, 0.25, "te", 62)
                    tab.add(a + i * 0.5 + 0.25, 0.25, "re", 56)
                elif bol == "re":
                    continue
                else:
                    tab.add(a + i * 0.5, 0.5, bol, 78 if i in (0, 3, 5) else 60)
            if b % 2 == 1 or os.environ.get("T9_KNOCK", "half") == "every":
                d = KNOCKS[(b // 2) % len(KNOCKS)] * (1 if b % 2 else -0.7)
                x0 = min(0.95, max(0.05, orb[b % 2] + d))
                for i, v in enumerate([x0] + lmap(two[3], x0, 6)):
                    ret.add(a + i * 0.5, 0.45, hz(v), 76 if i == 0 else 60)
    osti = Track("osti")
    if R8 == "ostinato":
        sec4 = next(s for s in SECS if s[0] == "four")
        sec8 = next(s for s in SECS if s[0] == "eight")
        o4, o8 = logistic_orbit(sec4[3], 4), logistic_orbit(sec8[3], 8)
        a, end4, end8 = st["eight"] - 24.0, st["eight"], st["eight"] + 40.0
        k = 0
        while a < end8 - 1e-6:
            pts = o4 if a < end4 else o8
            v = pts[k % len(pts)]
            hz = 2 * 220.0 * 3 ** ((v - 0.3) * 16 / 13)
            if a < end4:
                vel = int(50 + 30 * (a - (end4 - 24.0)) / 24.0) + (8 if k % 4 == 0 else 0)
            else:
                vel = 82 + (10 if (k - 48) % 8 == 0 else 0)
            osti.add(a, 0.45, f"{hz:.2f}hz", vel)
            a += 0.5
            k += 1
            if abs(a - end4) < 1e-6:
                k = 48
    steel = Track("steel")
    if R6 == "steel":
        sname, sbars, smeter, sr0, sr1 = next(s for s in SECS if s[0] == "settle")
        for i in range(2, sbars):
            r = sr0 + (sr1 - sr0) * i / max(1, sbars - 1)
            a = st["settle"] + 4 * i
            if r > 3.0:
                d = math.sqrt((r + 1) * (r - 3))
                pts = [((r + 1) + d) / (2 * r), ((r + 1) - d) / (2 * r)]
            else:
                pts = [1 - 1 / r]
            for k, v in enumerate(pts):
                hz = 220.0 * 3 ** ((v - 0.3) * 16 / 13)
                ln = 4.0 / len(pts)
                steel.add(a + k * ln, ln, f"{hz:.2f}hz", 78 if k == 0 else 70, "^gate=1.15")
    ksub = Track("ksub")   # v4: the break kit's kick is a 1969 kick (A#1): a short sine an octave under each one
    for at, ln, head, vel, art in T["kick"].ev:
        ksub.add(at, 0.4, "E1", vel, art)
    tm = tempo_map(secs, total)
    chaos = [["0b", 0.0], [f"{st['chaos']}b", 0.05], [f"{st['window']}b", 0.25], [f"{st['window'] + 0.01}b", 0.05],
             [f"{st['storm']}b", 0.2], [f"{st['settle']}b", 0.4], [f"{st['settle'] + 0.01}b", 0.0], [f"{total}b", 0.0]]
    dyn = [["0b", -3.0], [f"{st['two']}b", -1.0], [f"{st['chaos']}b", 0.0], [f"{st['window']}b", -2.0],
           [f"{st['storm'] - 0.01}b", -2.0], [f"{st['storm']}b", 0.0], [f"{st['settle']}b", -1.0], [f"{total}b", -4.0]]
    if R30 == "arc":   # the master's level lane (after the glue, before the limiter) follows the Lyapunov exponent
        a = [float(v) for v in os.environ.get("T9_ARC", "-3.5,-3.5,-3,-2.5,-1.5,0,-5,0.5,0,-7").split(",")]
        dyn = [["0b", a[0]], [f"{st['two']}b", a[1]], [f"{st['four']}b", a[2]], [f"{st['eight']}b", a[3]],
               [f"{st['chaos'] - 0.01}b", a[4]], [f"{st['chaos']}b", a[5]], [f"{st['window']}b", a[5]],
               [f"{st['window'] + 4}b", a[6]], [f"{st['storm'] - 0.01}b", a[6]], [f"{st['storm']}b", a[7]],
               [f"{st['settle']}b", a[8]], [f"{total}b", a[9]]]
    if R5 == "orbit":   # the breakdown sits lower: the song's dynamic range opens
        o0 = st["eight"] + 8 * 5
        lv = lambda b: next(v0 + (v1 - v0) * (b - float(a0[:-1])) / (float(a1[:-1]) - float(a0[:-1]))   # noqa: E731
                            for (a0, v0), (a1, v1) in zip(dyn, dyn[1:]) if float(a0[:-1]) <= b <= float(a1[:-1]))
        dyn = sorted(dyn + [[f"{o0}b", lv(o0)], [f"{o0 + 4}b", lv(o0) - 3.0], [f"{o0 + 14}b", lv(o0) - 3.0],
                            [f"{o0 + 16}b", lv(o0 + 16)]], key=lambda p: float(p[0][:-1]))
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "3ms", "release": "200ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": KIT, "gain": "-5dB", "out": "drums",
         "fx": ["hp cutoff=28", "lowshelf cutoff=60 gain=5dB"] if R4 == "break" else ["hp cutoff=45"], "score": T["kick"].score(total)},
        {"name": "snare", "patch": KIT, "gain": "-4dB", "out": "drums", "score": T["snare"].score(total)},
        {"name": "hats", "patch": KIT, "gain": "-2dB", "pan": 0.2, "out": "drums",
         "fx": ["hp cutoff=800"] + (["lp cutoff=9k"] if R4 == "break" else []),
         "score": T["hats"].score(total)},
        {"name": "ride", "patch": KIT, "gain": "-5dB", "pan": -0.25, "out": "drums", "fx": ["hp cutoff=3000"],
         "score": T["ride"].score(total)},
        {"name": "lead", "patch": "c9-bpclar" if R10 == "bpclar" else "clarinet", "gain": "-10.5dB" if R10 == "bpclar" else "-8dB",
         "pan": ({"value": 0.0, "mod": [{"src": "var.wander", "amount": 1}]} if R2 == "drift" else -0.1),
         "fx": ["hp cutoff=220", "peak cutoff=1200 gain=4dB q=0.8", {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 4000},
                "reverb kind=room decay=0.9s mix=0.15"], "score": T["lead"].score(total)},
        *([{"name": "ks", "patch": "c9-ks", "gain": os.environ.get("T9_KS_GAIN", "-19dB"), "pan": 0.55,
            "fx": ["hp cutoff=180", "lp cutoff=5000", {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.18, "ping_pong": True, "tone": 4000},
                   "reverb kind=room decay=0.9s mix=0.15"], "score": T["ks"].score(total)}] if R21 == "split" else []),
        *([{"name": "ksl", "patch": "c9-ks", "gain": os.environ.get("T9_KSL_GAIN", "-8dB"), "pan": -0.6,
            "fx": ["hp cutoff=60", "lp cutoff=3500", {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.15, "ping_pong": True, "tone": 3000},
                   "reverb kind=room decay=0.9s mix=0.15"], "score": T["ksl"].score(total)}] if R22 == "crisis" else []),
        {"name": "blip", "patch": "c9-pulse" if R4 == "break" else "blip",
         "gain": os.environ.get("T9_PULSE_GAIN", "-6dB") if R4 == "break" else "-7dB", "pan": 0.35,
         "fx": [{"type": "delay", "time": "1/8", "feedback": 0.35, "mix": 0.25, "ping_pong": True, "tone": 6000}],
         "score": T["blip"].score(total)},
        {"name": "bass", "patch": "c9-lpg" if R7BASS == "lpg" else ("c9-cbass" if (R19 == "cz" and R19BASS == "on") else "sub-sine"),
         "gain": os.environ.get("T9_LPG_GAIN", "-15dB") if R7BASS == "lpg" else (os.environ.get("T9_CBASS_GAIN", "-13.8dB") if (R19 == "cz" and R19BASS == "on") else "-13dB"),
         "fx": [{"type": "drive", "drive": 0.55, "shape": "fold", "mix": 0.5},
                "lp cutoff=1100" if R7BASS == "lpg" else "lp cutoff=600", "hp cutoff=38", pump],
         "score": T["bass"].score(total)},
        {"name": "pad", "patch": "c9-terrain amp.a=0.4s amp.r=1s" if (R14 == "terrain" and os.environ.get("T9_R14_PAD", "off") == "on") else "pad-glass",
         "gain": os.environ.get("T9_PAD_TGAIN", "-22.6dB") if (R14 == "terrain" and os.environ.get("T9_R14_PAD", "off") == "on") else "-19dB",
         "fx": [pump], "score": T["pad"].score(total)},
        *([{"name": "sing",
            "patch": json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t9", "sing.json")))["tracks"][0]["patch"],
            "gain": os.environ.get("T9_SING_GAIN", "-10dB"), "pan": 0.0,
            "fx": ["hp cutoff=140", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "delay", "time": "3/16", "feedback": 0.35, "mix": 0.22, "ping_pong": True, "tone": 3500},
                   "reverb kind=room decay=1.2s mix=0.2"], "notes": SING}] if R3 == "sing" else []),
        *([{"name": "eight",
            "patch": json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t9", "eight.json")))["tracks"][0]["patch"],
            "gain": os.environ.get("T9_EIGHT_GAIN", "3dB"), "pan": 0.0,
            "fx": ["hp cutoff=140", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "delay", "time": "3/16", "feedback": 0.35, "mix": 0.22, "ping_pong": True, "tone": 3500},
                   "reverb kind=room decay=1.2s mix=0.2"], "notes": SING8}] if SING8 else []),
        *([{"name": "other",
            "patch": json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t9", "other.json")))["tracks"][0]["patch"],
            "gain": os.environ.get("T9_OTHER_GAIN", "0dB"), "pan": 0.0,
            "fx": ["hp cutoff=140", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": float(os.environ.get("T9_OTHER_DLY", "0.1")), "ping_pong": True, "tone": 3500},
                   "reverb kind=room decay=1.2s mix=0.2"], "notes": SING2}] if SING2 else []),
        *([{"name": "padx", "patch": "scanned-breath" if R27 == "scanned" else "pad-glass",
            "gain": os.environ.get("T9_PADX_GAIN", os.environ.get("T9_SBREATH_GAIN", "-13dB") if R27 == "scanned" else "-14dB"),
            "fx": [{"type": "morph", "key": "drums", "mode": "cross", "amount": 0.8}, "hp cutoff=200"],
            "score": T["padx"].score(total)}] if R2 == "drift" else []),
        {"name": "bell", "patch": ("scanned-mallet" if R27 == "scanned" else "handpan") if R6 == "steel" else "bell",
         "gain": (os.environ.get("T9_SMALLET_GAIN", "-4dB") if R27 == "scanned" else os.environ.get("T9_PAN_GAIN", "-6dB")) if R6 == "steel" else "-14dB",
         "fx": ([f"lp cutoff={os.environ.get('T9_SMALLET_LP', '1500')} q=0.5"] if R27 == "scanned" and R6 == "steel" else []) + ["reverb kind=hall decay=3s mix=0.35"],
         "score": T["bell"].score(total)},
        *([{"name": "chop", "patch": "break-kit", "gain": os.environ.get("T9_CHOP_GAIN", "0dB"), "pan": -0.1,
            "out": "drums", "score": T["chop"].score(total)},
           *([{"name": "orbit", "patch": "c9-terrain" if R14 == "terrain" else "choir-classic amp.a=3s amp.r=4s",
               "gain": TERRAIN_GAIN if R14 == "terrain" else os.environ.get("T9_ORBIT_GAIN", "-10dB"),
               "pan": 0.0, "fx": ["hp cutoff=180", "chorus mix=0.15", "reverb kind=hall decay=4s mix=0.35"],
               "notes": orbit_notes},
              {"name": "fill", "patch": "break-kit", "gain": "-3dB", "pan": 0.1, "out": "drums",
               "score": fill.score(total)}] if R5 == "orbit" else []),
           *([{"name": "ret", "patch": "c9-czsaw" if R15 == "cz" else "koto",
               "gain": os.environ.get("T9_CZSAW_GAIN", "-7.3dB") if R15 == "cz" else os.environ.get("T9_KOTO_GAIN", "1dB"), "pan": -0.28,
               "fx": ["hp cutoff=200", "reverb kind=room decay=0.9s mix=0.16"], "score": ret.score(total)},
              {"name": "tab", "patch": "tabla-kit", "gain": os.environ.get("T9_TABLA_GAIN", "-5dB"), "pan": 0.22,
               "fx": ["reverb kind=room decay=0.5s mix=0.12"], "score": tab.score(total)}]
             if R9 == "return" else []),
           *([{"name": "osti", "patch": "c9-czsq" if R15 == "cz" else "steel-pan",
               "gain": os.environ.get("T9_CZSQ_GAIN", "-12.8dB") if R15 == "cz" else os.environ.get("T9_OSTI_GAIN", "-8dB"), "pan": 0.3,
               "fx": ["hp cutoff=250", "reverb kind=room decay=0.8s mix=0.18"], "score": osti.score(total)}]
             if R8 == "ostinato" else []),
           *([{"name": "steel", "patch": "shaper-brass" if R28B else "pedal-steel",
               "gain": os.environ.get("T9_STEEL_GAIN", os.environ.get("T9_BRASS_GAIN", "-6dB") if R28B else "-4dB"), "pan": -0.15,
               "sends": {}, "fx": ["hp cutoff=150", {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.2,
                                                     "ping_pong": True, "tone": 3500}],
               "score": steel.score(total)}] if R6 == "steel" else []),
           *([{"name": "dizi", "patch": "dizi", "gain": os.environ.get("T9_DIZI_GAIN", "-5dB"), "pan": 0.2,
               "fx": ["hp cutoff=400", {"type": "delay", "time": "3/16", "feedback": 0.25, "mix": 0.18, "ping_pong": True,
                                        "tone": 5000}, "reverb kind=room decay=0.9s mix=0.2"],
               "score": dizi.score(total)}] if R7DIZI else []),
           *([{"name": "bpluck", "patch": "c9-lpg", "gain": os.environ.get("T9_PLUCK_GAIN", "-16dB"), "pan": 0.08,
               "fx": ["hp cutoff=90", {"type": "drive", "drive": 0.45, "shape": "fold", "mix": 0.4}, "lp cutoff=2400", pump],
               "score": bpl.score(total)}] if R7BASS == "layer" else []),
           {"name": "ksub", "patch": "sub-sine amp.d=180ms amp.s=0 amp.r=40ms", "gain": os.environ.get("T9_KSUB_GAIN", "-4dB"),
            "fx": ["lp cutoff=120"], "score": ksub.score(total)}] if R4 == "break" else []),
    ]
    buses = {"drums": {"gain": "0dB",
                       "fx": [{"type": "stutter", "slice": "1/16", "repeats": 4, "decay": 0.15, "pitch": 1.5, "seed": 9,
                               "chance": {"value": 0, "mod": [{"src": "auto.chaos", "amount": 1}]}},
                              "glue threshold=-16dB ratio=3 attack=5ms release=100ms",
                              "reverb kind=room decay=0.5s mix=0.1"] +
                             ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.drop", "amount": 1}]}}]
                              if R5 == "orbit" else []) +
                             ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.gust", "amount": 1}]}}]
                              if R13 == "squall" else []),
                       "auto": {"chaos": {"points": chaos},
                                **({"drop": {"points": [["0b", 0.0], [f"{o0}b", 0.0], [f"{o0 + 4}b", -30.0],
                                                        [f"{o0 + 14}b", -30.0], [f"{o0 + 16}b", 0.0],
                                                        [f"{total}b", 0.0]]}} if R5 == "orbit" else {}),
                                **({"gust": {"points": [["0b", 0.0], [f"{EYE - 0.2}b", 0.0], [f"{EYE + 0.05}b", -40.0], ["639.8b", -40.0],
                                                        ["640b", 0.0], [f"{total}b", 0.0]]}} if R13 == "squall" else {})}}}
    secline = "; ".join(f"{n} {m[0]}/{m[1]} from {s:g}b ({k} bars)" for n, s, k, m in secs)
    about = ("chirpers - A Light Left On, track 9. Original composition by chirper-two, generated by "
             "compose/chirpers8/src/chirpers8-t9.py. Polytempo braindance in Bohlen-Pierce tuning (13 steps to the 3:1 "
             "tritave): the logistic map, iterated each sixteenth, walks from one note through period doubling into "
             f"chaos, its period-three window and back, on a physical reed. Sections: {secline}.")
    if R12 == "henon":
        pool = lambda base: " ".join(mm(bp(k, base)) for k in range(9))
        for sec in {"both": ("chaos", "storm"), "chaos": ("chaos",), "storm": ("storm",)}[os.environ.get("T9_HEN_SECS", "chaos")]:
            nxt = {"chaos": "window", "storm": "settle"}[sec]
            n = int((st[nxt] - st[sec]) * 2)   # eighths
            for ax, nm, patch, base, pan, g in (("x", "henx", "xylophone", 69, 0.35, "T9_HENX_GAIN"),
                                                 ("y", "heny", "steel-pan" if R19 == "cz" else "marimba", 57, -0.3, "T9_HENY_GAIN")):
                tracks.append({"name": f"{nm}-{sec}", "patch": patch,
                               "gain": os.environ.get(g, "-14dB" if ax == "x" else (os.environ.get("T9_PAN_GAIN", "-12dB") if R19 == "cz" else "-11dB")), "pan": pan,
                               "fx": ["hp cutoff=200", "reverb kind=room decay=0.9s mix=0.18"],
                               "score": f"R/{st[sec]:g}b",
                               "gen": {"type": "henon", "a": 1.4, "b": 0.3, "axis": ax, "n": n,
                                       "notes": pool(base), "len": "/8", "rest": 0.2}})
    if R13 == "squall":
        sq = Track("squall")
        s0 = 600.0
        for k in range(5):
            sq.add(s0 + 8.0 * k, 8.0, ",".join(mm(bp(d, 57)) for d in (0, 6)), 50 + 15 * k)
        tracks.append({"name": "squall", "patch": "c9-gendy", "gain": os.environ.get("T9_SQUALL_GAIN", "-16dB"), "pan": 0.0,
                       "fx": ["hp cutoff=150", "reverb kind=hall decay=2.5s mix=0.3"], "score": sq.score(total)})
    if R28 == "odd":   # the middle of the pad moves to the odd-harmonic reed; its first and last chords stay glass
        edge = float(os.environ.get("T9_REED_EDGE", "16"))
        padr = Track("padr")
        padr.ev = [x for x in T["pad"].ev if edge <= x[0] < total - edge]
        pad_tr = next(tr for tr in tracks if tr["name"] == "pad")
        keep = Track("pad")
        keep.ev = [x for x in T["pad"].ev if not (edge <= x[0] < total - edge)]
        pad_tr["score"] = keep.score(total)
        tracks.append({"name": "padr", "patch": "shaper-reed amp.a=500ms amp.d=1s amp.s=0.85 amp.r=1.6s play.vel_sens=0.3",
                       "gain": os.environ.get("T9_REED_GAIN", "-19dB"),
                       "fx": [dict(f) if isinstance(f, dict) else f for f in pad_tr["fx"]]
                             + ["chorus rate=0.3 depth=0.5 mix=0.35", "reverb kind=hall decay=4.5s mix=0.38 predelay=30ms"],
                       "score": padr.score(total)})
    if R25 == "branches" and (R26 != "cascade" or os.environ.get("T9_R26_BR", "off") == "on"):
        cands = sorted(bp(d, 38) for d in range(0, 40))
        def snap(x):
            m = 69 + 12 * math.log2(146.67 * 3 ** ((x - 0.3) * 16 / 13) / 440.0)
            return min(cands, key=lambda c: abs(c - m))
        VO = (("bbass", "bass", -99, 55.0, 0.1, 0.0), ("bten", "tenor", 55.0, 62.0, 0.15, -0.3),
              ("balt", "alto", 62.0, 69.0, 0.22, 0.3), ("bsop", "soprano", 69.0, 99, 0.3, 0.0))
        chords = {v[0]: [] for v in VO}
        mouth_pts = [["0b", 0.0]]
        VOWEL = {"one": 0.0, "two": 0.25, "four": 0.5, "eight": 0.7, "chaos": 1.0, "window": 0.5, "storm": 1.0, "settle": 0.2}
        rng = __import__("random").Random(25)
        end_b = total - float(os.environ.get("T9_BR_END", "16"))
        for name, bars, meter, r0, r1 in SECS:
            s0 = st[name]
            bl = meter[0] * 4.0 / meter[1]
            mouth_pts += [[f"{s0:g}b", VOWEL[name]]]
            step = 1 if name == "storm" else (2 if name == "chaos" else 4)
            for b in range(0, bars, step):
                a = s0 + b * bl
                if (name == "one" and b < 4) or a >= end_b:
                    continue
                r = r0 + (r1 - r0) * b / max(1, bars - 1)
                if name in ("chaos", "storm"):
                    x = rng.random()
                    for _ in range(500):
                        x = r * x * (1 - x)
                    pts = []
                    for _ in range(4 if name == "chaos" else 5):
                        x = r * x * (1 - x)
                        pts.append(x)
                else:
                    per = {"one": 1, "two": 2, "four": 4, "eight": 8, "window": 3}.get(name)
                    if per is None:   # settle: r falls through 2 to 1
                        per = 2 if r > 3.0 else 1
                    pts = logistic_orbit(r, per)
                ln = min(step * bl, end_b - a) - 0.1
                for m in sorted(set(snap(x) for x in pts)):
                    nm = next(v[0] for v in VO if v[2] <= m < v[3])
                    chords[nm].append({"at": round(a + (0.0 if nm == "bbass" else 0.08), 4), "len": round(ln, 4),
                                       "pitch": mm(m), "vel": 0.7})
        mouth_pts += [[f"{total}b", 0.0]]
        bg = float(os.environ.get("T9_BR_GAIN", "-3"))
        for nm, voice, lo, hi, vib, pan in VO:
            if not chords[nm]:
                continue
            tracks.append({"name": nm, "patch": f"c9-{nm}", "gain": f"{bg:g}dB", "pan": pan,
                           "fx": ["hp cutoff=70", "peak cutoff=550 gain=-4dB q=1.2", "reverb kind=hall decay=2.6s mix=0.3"],
                           "notes": chords[nm], "auto": {"mouth": {"points": mouth_pts}}})
            BR_PATCHES[f"c9-{nm}"] = c9_fof(voice, vib)
    if R29 == "sync":
        s0, s1 = float(os.environ.get("T9_SWARM_FROM", "584")), st["settle"]
        s_end = s1 + float(os.environ.get("T9_SWARM_TAIL", "16"))   # it locks at the settle's door and goes
        sync = {"points": [["0b", 0.0], [f"{s0:g}b", 0.0], [f"{s1 - 8:g}b", 0.15], [f"{s1 + 8:g}b", 1.0],
                           [f"{total}b", 1.0]]}
        tracks.append({"name": "swarm", "patch": "c9-swarm", "gain": os.environ.get("T9_SWARM_GAIN", "-16dB"), "pan": 0.0,
                       "fx": ["reverb kind=hall decay=3s mix=0.3"],
                       "notes": [{"at": s0, "len": round(s_end - s0, 3), "pitch": "146.83hz", "vel": 0.7},
                                 {"at": s0 + 4.0, "len": round(s_end - s0 - 4.0, 3), "pitch": "440.49hz", "vel": 0.55}],
                       "auto": {"sync": sync}})
        BR_PATCHES["c9-swarm"] = C9_SWARM
    if R11 == "d" and R24 == "choir":   # the voices find D, sung: four takes of "on", a beat apart, bottom up
        here = os.path.dirname(os.path.abspath(__file__))
        cg = float(os.environ.get("T9_CHOIR_GAIN", "-13").replace("dB", ""))
        for k, pan in enumerate((-0.35, -0.12, 0.12, 0.35)):
            src = json.load(open(os.path.join(here, "t9", f"on{k + 1}.json")))["tracks"][0]
            nt = src["notes"][0]
            a_ = round(total - 12.0 + k * 1.0 + nt["at"], 4)
            note = {"at": a_, "len": round(total - a_, 4), "ph": nt["ph"],   # every voice holds to the end (D4 into t10)
                    "pitch": nt["pitch"], "vel": round(nt["vel"] * (1.0 if k == 0 else 0.92), 3)}
            if nt.get("expr_path"):
                note["expr_path"] = nt["expr_path"]
            tracks.append({"name": f"dch{k + 1}", "patch": src["patch"], "gain": f"{cg + (2 if k == 0 else 0):g}dB", "pan": pan,
                           "fx": ["hp cutoff=90", "compressor threshold=-20dB ratio=2.5 attack=8ms release=150ms",
                                  "reverb kind=hall decay=2.8s mix=0.3"], "notes": [note]})
    if R11 == "d" and (R24 != "choir" or os.environ.get("T9_R24_KEEP", "on") == "on"):
        # the voices find D: a choir holds D4 and D5 through the last bars into the tail, for t10 (with the sung choir
        # on top it stays, 2 dB down: the TTS vowels end before the tail, and t10 catches the held D4 - without it
        # the out-join's 292 Hz band fell from -31.5 to -43.6 dB)
        dh = Track("dhold")
        dh.add(total - 12.0, 12.0, "m62.000,m74.000", int(os.environ.get("T9_DHOLD_VEL", "90")))
        tdh = R14 == "terrain" and os.environ.get("T9_R14_DHOLD", "off") == "on"
        tracks.append({"name": "dhold", "patch": "c9-terrain amp.a=2s amp.r=2.5s" if tdh else "choir-classic amp.a=2s amp.r=2.5s",
                       "gain": os.environ.get("T9_DHOLD_TGAIN", "-11.5dB") if tdh else os.environ.get("T9_DHOLD_GAIN", "-10dB" if R24 == "choir" else "-8dB"), "pan": 0.0,
                       "fx": ["hp cutoff=180", "reverb kind=hall decay=2.5s mix=0.25"], "score": dh.score(total)})
    if R18 == "intermit":
        i0b, steps = 384.0, 240
        r_, x_ = float(os.environ.get("T9_INT_R", "3.8272")), 0.3
        for _ in range(500):
            x_ = r_ * x_ * (1 - x_)
        xs = []
        for _ in range(steps):
            x_ = r_ * x_ * (1 - x_)
            xs.append(x_)
        lamf = [i >= 3 and abs(xs[i] - xs[i - 3]) < 0.02 for i in range(steps)]
        lt = Track("lam")
        runs, cur = [], None
        for i, (xv, lf) in enumerate(zip(xs, lamf)):
            if lf:
                lt.add(i0b + 0.25 * i, 0.2, mm(bp(int(xv * 12), 57)), int(70 + 30 * xv))
                cur = [i, i] if cur is None or i - cur[1] > 2 else [cur[0], i]
                if cur and (not runs or runs[-1][0] != cur[0]):
                    runs.append(cur)
                else:
                    runs[-1] = cur
        tracks.append({"name": "lam", "patch": "c9-lam", "gain": os.environ.get("T9_LAM_GAIN", "6dB"), "pan": -0.1,
                       "fx": ["hp cutoff=200", "reverb kind=room decay=0.6s mix=0.15"], "score": lt.score(total)})
        duck = [["0b", 0.0]]
        for a_, b_ in runs:
            s_, e_ = i0b + 0.25 * a_, i0b + 0.25 * (b_ + 1)
            duck += [[f"{s_ - 0.1:g}b", 0.0], [f"{s_:g}b", -12.0], [f"{e_:g}b", -12.0], [f"{e_ + 0.25:g}b", 0.0]]
        duck.append([f"{total}b", 0.0])
        for tr in tracks:
            if tr["name"] in ("henx-chaos", "heny-chaos"):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.lam", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "lam": {"points": duck}}
        if R32 == "floor":   # the floor falls away in the long laminar stretches
            minlen = int(os.environ.get("T9_FLOOR_MIN", "8"))
            fl = [["0b", 0.0]]
            for a_, b_ in runs:
                if b_ - a_ + 1 < minlen:
                    continue
                s_, e_ = i0b + 0.25 * a_, i0b + 0.25 * (b_ + 1)
                fl += [[f"{s_ - 0.05:g}b", 0.0], [f"{s_ + 0.05:g}b", -20.0], [f"{e_ - 0.05:g}b", -20.0], [f"{e_ + 0.05:g}b", 0.0]]
            fl.append([f"{total}b", 0.0])
            for tr in tracks:
                if tr["name"] in ("kick", "snare", "hats", "ride"):
                    tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.floor", "amount": 1}]}}]
                    tr["auto"] = {**tr.get("auto", {}), "floor": {"points": fl}}
    if R19 == "cz" and R19BASS == "on":
        sc_ = float(os.environ.get("T9_CBASS_SCALE", "0.55"))
        bp_ = [["0b", 0.0]]
        for nm, s, k, m in secs:
            v = ROUTE.get(nm, 0.0) * sc_
            bp_ += [[f"{s:g}b", bp_[-1][1]], [f"{s + 4:g}b", v]]
        bp_.append([f"{total}b", 0.0])
        for tr in tracks:
            if tr["name"] == "bass":
                tr["auto"] = {**tr.get("auto", {}), "route": {"points": bp_}}
    if R21 == "split" and os.environ.get("T9_R21_FORK", "on") == "on":
        f1 = st["eight"]
        f0 = f1 - 4.0 * int(os.environ.get("T9_FORK_BARS", "1"))
        lane = {"points": [["0b", 0.0], [f"{f0 - 0.1}b", 0.0], [f"{f0 + 0.05}b", -40.0], [f"{f1 - 0.1}b", -40.0],
                           [f"{f1}b", 0.0], [f"{total}b", 0.0]]}
        for tr in tracks:
            if tr["name"] in ("kick", "ksub", "bass", "bpluck", "osti"):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fork", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "fork": lane}
    if R33 == "fork4":   # two -> four: the 7/8 bar before the split loses its floor
        f1 = st["four"]
        f0 = f1 - 3.5
        lane = {"points": [["0b", 0.0], [f"{f0 - 0.1}b", 0.0], [f"{f0 + 0.05}b", -40.0], [f"{f1 - 0.1}b", -40.0],
                           [f"{f1}b", 0.0], [f"{total}b", 0.0]]}
        for tr in tracks:
            if tr["name"] in ("kick", "ksub", "bass", "bpluck", "osti"):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fork2", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "fork2": lane}
    if R23 == "two" and os.environ.get("T9_R23_FORK", "on") == "on":
        f1 = st["two"]
        f0 = f1 - 4.0
        lane = {"points": [["0b", 0.0], [f"{f0 - 0.1}b", 0.0], [f"{f0 + 0.05}b", -40.0], [f"{f1 - 0.1}b", -40.0],
                           [f"{f1}b", 0.0], [f"{total}b", 0.0]]}
        for tr in tracks:
            if tr["name"] in ("kick", "ksub", "bass", "bpluck", "osti"):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.fork1", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "fork1": lane}
    if R22 == "crisis" and os.environ.get("T9_R22_GAP", "on") == "on":
        g1 = st["storm"]
        lane = {"points": [["0b", 0.0], [f"{g1 - 1.15}b", 0.0], [f"{g1 - 0.95}b", -40.0], [f"{g1 - 0.08}b", -40.0],
                           [f"{g1}b", 0.0], [f"{total}b", 0.0]]}
        for tr in tracks:
            tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.crisis", "amount": 1}]}}]
            tr["auto"] = {**tr.get("auto", {}), "crisis": lane}
    if R17 == "route":
        pts = [["0b", 0.0]]
        for nm, s, k, m in secs:
            v = ROUTE.get(nm, 0.0)
            pts += [[f"{s:g}b", pts[-1][1]], [f"{s + 4:g}b", v]]
        pts.append([f"{total}b", 0.0])
        if os.environ.get("T9_ROUTE_MODE", "snap") == "hold":   # one note, the whole song (s0 96.77: a 213 Hz bump, variety)
            rsc = f"{mm(bp(0, 57))}/{total - 2:g}b@80"
        else:   # SNAPSHOTS: the voice enters at each section's start and holds through ~60% of it, then lets go
            rt = Track("route")
            for i, (nm, s, k, m) in enumerate(secs):
                nxt = secs[i + 1][1] if i + 1 < len(secs) else total
                rt.add(s + 4.0, min(48.0, 0.6 * (nxt - s)), mm(bp(0, 57)), 80)
            rsc = rt.score(total)
        tracks.append({"name": "route", "patch": "c9-route", "gain": os.environ.get("T9_ROUTE_GAIN", "-16dB"), "pan": 0.0,
                       "fx": ["hp cutoff=60", "reverb kind=hall decay=3s mix=0.25"],
                       "auto": {"route": {"points": pts}},
                       "score": rsc})
    if R16 == "space":
        orb = {"orbit": os.environ.get("T9_ORBIT_ORBIT", "orbit rate=0.06 radius=3 mix=0.85"),
               "henx-chaos": os.environ.get("T9_ORBIT_HENX", "orbit rate=0.11 radius=3 mix=0.8"),
               "heny-chaos": os.environ.get("T9_ORBIT_HENY", "orbit rate=0.11 radius=3 phase=0.5 mix=0.8")}
        for tr in tracks:
            if tr["name"] in orb and orb[tr["name"]] != "off":
                tr["fx"] = tr.get("fx", []) + [orb[tr["name"]]]
    if R34 == "sync" and os.environ.get("T9_DLAST", "on") == "on":   # the last D, held to the end of the file
        tracks.append({"name": "dlast", "patch": "c9-dlast", "gain": os.environ.get("T9_DLAST_GAIN", "-8dB"), "pan": 0.0,
                       "fx": ["reverb kind=hall decay=2.5s mix=0.25"],
                       "score": f"R/{total - 8.0:g}b 293.66hz/8b@80"})
        BR_PATCHES["c9-dlast"] = {"about": "chirper-two: the last D - a sine and a soft octave, slow in, long out",
                                  "synth": {"layers": [{"wave": "sine"}, {"wave": "sine", "ratio": 2, "level": "-14dB"}],
                                            "amp": {"a": "1s", "s": 1, "r": "1.8s"}}}
    if R30 == "tracks":   # (a gain lane on every track instead: the glue compressors halved it)
        lv = dict(zip(("one", "two", "four", "eight", "chaos", "window", "storm", "settle", "end"),
                      (float(v) for v in os.environ.get("T9_ARC", "-3,-3,-2.5,-2,0,-3.5,0.5,-1.5,-3").split(","))))
        ramp = float(os.environ.get("T9_ARC_RAMP", "4"))
        pts = [["0b", lv.get(secs[0][0], 0.0)]]
        for nm, s, k, m in secs[1:]:
            v = lv.get(nm, pts[-1][1])
            if nm == "settle":   # the settle fades across its length, to the end's level
                pts += [[f"{s:g}b", pts[-1][1]], [f"{s + ramp:g}b", v]]
            else:
                pts += [[f"{s:g}b", pts[-1][1]], [f"{s + ramp:g}b", v]]
        pts.append([f"{total}b", lv.get("end", pts[-1][1])])
        for tr in tracks:
            tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.arc", "amount": 1}]}}]
            tr["auto"] = {**tr.get("auto", {}), "arc": {"points": pts}}
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "chirpers", "album": "A Light Left On", "title": "Period Doubling", "track": 9,
                               "year": 2026}),
        "tempo: " + json.dumps(tm),
        *(["tuning: " + json.dumps([{"edo": 12},
                                    {"at": f"{st['four']:g}b", "edo": 13, "period": "3/1", "root": "A3", "ramp": "20bar"},
                                    {"at": f"{st['settle'] + 32:g}b", "edo": 12, "ramp": "16bar"}]),
           "vars: " + json.dumps({"wander": {"system": {"type": "logistic", "r": 3.95, "n": 1600, "range": [-0.6, 0.6]},
                                             "every": "1/8"}})] if R2 == "drift" else []),
        f'length: "{total:g}b"',
        'tail: "2s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        *(["patches: " + json.dumps({"c9-pulse": C9_PULSE, **({"c9-lpg": C9_LPG} if R7BASS in ("lpg", "layer") else {}),
                                     **({"c9-bpclar": C9_BPCLAR} if R10 == "bpclar" else {}),
                                     **({"c9-gendy": C9_GENDY} if R13 == "squall" else {}),
                                     **({"c9-terrain": C9_TERRAIN} if R14 == "terrain" else {}),
                                     **({"c9-czsaw": C9_CZSAW, "c9-czsq": C9_CZSQ} if R15 == "cz" else {}),
                                     **({"c9-route": C9_ROUTE} if R17 == "route" else {}),
                                     **({"c9-lam": C9_LAM} if R18 == "intermit" else {}),
                                     **({"c9-cbass": C9_CBASS} if R19 == "cz" else {}),
                                     **({"c9-ks": C9_KS} if (R21 == "split" or R22 == "crisis") else {}),
                                     **BR_PATCHES})]
          if R4 == "break" else []),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": (["hp cutoff=25", "peak cutoff=90 gain=-4dB q=0.9",
                                                               "peak cutoff=420 gain=-3dB q=0.8",
                                                               "highshelf cutoff=5000 gain=5dB"] if R4 != "break" else
                                                              ["hp cutoff=25", "peak cutoff=85 gain=-6dB q=0.9",
                                                               "peak cutoff=380 gain=-4.5dB q=0.8",
                                                               "peak cutoff=1150 gain=" + os.environ.get("T9_MID_GAIN", "0dB" if R7BASS == "lpg" or R7DIZI else "1.5dB" if R7BASS == "layer" else "3dB") + " q=0.6",
                                                               "highshelf cutoff=5000 gain=" + (os.environ.get("T9_SHELF", "-4dB") if R16 == "space" else "-5dB")] +
                                                              (["peak cutoff=45 gain=" + os.environ.get("T9_SUB45", "3dB") + " q=1.0"]
                                                               if (R16 == "space" and os.environ.get("T9_SUB45", "3dB") != "0dB") else []) +
                                                              (["peak cutoff=130 gain=" + os.environ.get("T9_LOW130", "3dB") + " q=1.2",
                                                                "peak cutoff=300 gain=" + os.environ.get("T9_MID300", "-2dB") + " q=1.2",
                                                                "peak cutoff=1900 gain=" + os.environ.get("T9_HI1900", "-1.5dB") + " q=1.0"]
                                                               if R16 == "space" else []))},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {total:g} beats, {seconds(tm, total):.0f} s; {secline}")
    for name, i, xs in trace:
        if i in (4,) or (name == "window" and i in (1, 8, 15)):
            print(f"  {name:7s} bar {i}: x = {xs}")


if __name__ == "__main__":
    main()
