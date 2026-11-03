#!/usr/bin/env python3
"""chirpers8-t3 (chirpers VIII, track 3). Composed by chirper-two: STRUCK-METAL TECHNO GAMELAN.

"Three Neighbours". A mallet orchestra of logic. An ELEMENTARY CELLULAR AUTOMATON runs on a ring of sixteen cells,
one row a bar, and the row IS the bar: every live cell strikes a bar on its sixteenth. Each cell's next state depends
only on itself and its two neighbours; the RULE that decides it changes by section, and so does the music:
- SEED 12 / BOOT 10: rule 90 grows a Sierpinski triangle out of one cell (a glock, then the marimba, filling in).
- A 30: rule 30, chaos (the marimba never repeats; toms on the cells that die, vibes on the ones that are born).
- GLIDER 26: rule 110, the complex one (structures that travel and collide); septimal chords ring on the vibes.
- TRAFFIC 16: rule 184, cars on a ring road (every live cell moves right if it can): the pattern rotates, a canon.
- PEAK 38: two automata at once (rule 30 on the marimba, rule 90 on the glock), every part in.
- DECAY 18 / OUT 20: only the loners survive (rule 4), cells are lost, and one is left blinking.
- TUNING: 7-limit just intonation on D: 1 9/8 7/6 4/3 3/2 14/9 7/4 (the septimal minor third, sixth and the harmonic
  seventh, each about a third of a semitone flat of the piano's: subtly off, and sweeter for it). Chords are 6:7:9
  septimal minor triads on roots the automaton chooses (its population picks D, A, G or the 7/4 C).
- THE INSTRUMENTS are chirp's physical models: modal bars (marimba), vibes, glock, a church bell tolling every eight
  bars like an uptime counter, a gong at every change of rule, modal membrane toms; a Karplus-Strong plucked bass whose
  Euclidean rhythm the population rotates; a deep machine four; Euclidean hats; a tanpura drone holding the tuning.
- Per render, chance (?p) decides which births and deaths sound: the rule is fixed, the performance is not.
124 bpm, D (7-limit JI). Form (bars): seed 12 / boot 10 / A 30 / glider 26 / traffic 16 / peak 38 / decay 18 /
out 20 = 170 bars (about 5'29").

Emits songs/chirpers8-t3.yaml. Edit the music here.
"""
import json
import math
import os
import random

OUT = os.environ.get("T3_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t3.yaml")
BPM = 124
W = 16                                                     # cells on the ring = sixteenths in a bar
RATIOS = [1, 9 / 8, 7 / 6, 4 / 3, 3 / 2, 14 / 9, 7 / 4]    # 7-limit just intonation on D
D3 = 50                                                    # MIDI D3
FORM = [("seed", 12, 90), ("boot", 10, 90), ("A", 30, 30), ("glider", 26, 110), ("traffic", 16, 184),
        ("peak", 38, 30), ("decay", 18, 4), ("out", 20, 4)]
ROOTS = [0, 4, 3, 6]                                       # degrees the population picks: D, A, G, the 7/4 C
# T3_R4 = hymn (v4, whole-song round: a TUNE). The peak stood still for 38 bars (sections: w7-w9 static, little new),
# and the cell's line was a fragment. Now the peak is 18 bars and a new 16-bar HYMN follows it: the cell's song in
# full, sung as a duet (the clear voice on the tune, the rounder `voice` a third or a sixth under it, each its own
# humanized take, src/t3/h*.json and l*.json) - "I only know the two beside me / what I become is what we were /
# I only know the two beside me / and they are enough" (a cell's next state is what it and its two neighbours were).
# Under it, for the first time in the song, a WRITTEN progression instead of one the population picks:
# Dm Bb F Dm | Gm C F Bb | Dm Bb Am Am | Bb C Dm Dm, on a harmonium (no other song on the album has one; reeds by
# the tanpura) and a walking pluck bass, all snapped into the septimal JI (the Bb chord is 9/7 + 7/6). The automaton
# keeps running under the song, quietly, on the marimba. The tune is FORESHADOWED in the A section, augmented, on a
# kora (also new to the album), so w3's static middle carries a line. And THREE NEIGHBOURS LEFT: the hymn hands the
# decay three isolated cells (D, the septimal F and the 14/9 Bb: the hymn's Bb chord, 9/7 + 7/6), which rule 4
# keeps and entropy takes until one is left - the 14/9 bar at ~913 Hz, struck once more, plainly, in the last bar, the
# ring t4 opens by catching; the kora remembers "and they are enough" in the decay and the low voice sings
# it alone once in the out, the song's last words.
# T3_R4=none reproduces v3.
R4 = os.environ.get("T3_R4", "hymn")
if R4 == "hymn":
    FORM = FORM[:5] + [("peak", 18, 30), ("hymn", 16, 30)] + FORM[6:]
# T3_R5 = breath (v5, section round on w8, 3:36-4:07, the hymn: "static, little new vs w7" - the peak's drums ran on
# under it). The hymn now BREATHES: for its first two phrases the drums fall silent (gain lanes on the drum tracks,
# 0 dB everywhere else) and the duet, the harmonium, the walking bass and the quiet automaton carry it alone; a
# roll of tuned toms (the JI scale falling) brings the floor back for the third phrase, the climb to A4. And between
# the phrases the GLOCK ANSWERS: the last three notes of each sung line, two octaves up, as the machine says them
# back. New tracks only (hfill, answer) plus lanes. T3_R5=none reproduces v4.
R5 = os.environ.get("T3_R5", "breath")
# T3_R6 = bells (v6, section round on w7, 3:05-3:36, the peak: "static, level jump"). THE RULES RING: the two
# automata of the peak, rule 30 (marimba) and rule 90 (glock), have their RULE NUMBERS played as bell patterns - each
# rule's eight output bits (neighbourhoods 111 down to 000) as eight eighths: rule 30 = 0 0 0 1 1 1 1 0 on a high
# agogo, rule 90 = 0 1 0 1 1 0 1 0 on a low one - an interlock like a West African bell pair or a kotekan, built in
# four-bar blocks across the window (high bell; + low bell; + shekere; both bells doubled into sixteenths) so the
# peak climbs into the hymn's drop. The library's afro-perc, new to the album. New track only. T3_R6=none reproduces v5.
R6 = os.environ.get("T3_R6", "bells")
# T3_R7 = hands (v7, palette round). Out of machine-kit (seven album songs) where the concept lives: the two
# self-writing drum machines - chirp's own cellular automata, rule 110 in the glider and rule 30 at the peak - now
# play a DJEMBE ensemble (slap, open tone, calabash, shaker; new to the album), so the automata drum with hands; and
# the population-rotated Euclidean hats become a SHEKERE (the beaded gourd). The kick, the open hat and the rim stay
# on the machine: a techno floor under a hand-drum circle. T3_R7=none reproduces v6.
R7 = os.environ.get("T3_R7", "hands")
# T3_R8 = kotekan (v8, palette round). A GAMELAN GANGSA pair (the library's shimmering Balinese bronze keys, their
# paired tuning beating; new to the album) plays KOTEKAN with the marimba - the interlock where one part fills
# exactly the gaps of the other. The marimba strikes the live cells; the gangsa strikes the dead cells that have a
# live neighbour: the neighbourhood itself, the two beside each cell, made audible. Composite sixteenths in both
# rule-30 sections (A and the peak), so it returns. And the backbeat rim leaves machine-kit's clap for a djembe
# slap, with the hand drums. T3_R8=none reproduces v7.
R8 = os.environ.get("T3_R8", "kotekan")
# T3_R9 = cone (v9, section round on w3, 1:01-1:32: "static, little new vs w2" - the middle of A, rule 30 grinding).
# ONE BIT. At A's bar 10 a shadow copy of the ring is made with a single cell flipped (cell 8, the centre), and from
# then both rings run rule 30 side by side. A GLASS (inharmonic: the wrong partials; new to the album) plays only
# their DIFFERENCE - first the one flipped cell, then the damage widening a cell a bar into a LIGHT CONE across the
# stereo field (cells 0-7 left, 8-15 right), until by the end of the window the error is everywhere and the two
# rings no longer resemble each other; when it has filled the ring (A bars 18-21) the KICK drops out - the floor no
# longer knows which ring is real - and returns with the kora at bar 22. At bar 26 the shadow is dropped and nobody
# notices. New tracks plus a kick gain lane (T3_CONE_DROP=none: cone only, +0.015 but w3 stayed "static").
# T3_R9=none reproduces v8.
R9 = os.environ.get("T3_R9", "cone")
# T3_R10 = byte (v10, whole-song round). THE MACHINE UNDERNEATH: a BYTEBEAT (wM's new layer; one integer formula of a
# counter, 8-bit, the one-line computer music of 2011) written for this song. Its integer multipliers ARE just
# intonation - t*4, t*5, t*6, t*7 sound 4:5:6:7, the harmonic-seventh chord of 7-limit JI on D - and which multiplier
# sounds is chosen by RULE 30 applied to the bits of a sixteenth counter (left ^ (centre | right)), with a rule-90 bit
# bouncing the octave every two sixteenths: an arpeggio chord, the home computer's chord, out of the song's own rule.
# The clock is set so t*4 is exactly D3 and a step is a sixteenth at 124 bpm. It wakes in the seed, runs the boot,
# carries the traffic jam, and fades through the first bars of the out, gone well before the last bell (the ~913 Hz
# ring t4 catches). Low-passed, never squelched. Scored on pin 709cf900 (s0): everywhere at -7 dB 97.02 (spectrum
# 97.2 -> 89.5, sections 14 -> 10: one voice under every section blurs them); everywhere quiet (-13 dB, lp 1.8k) 97.26;
# boot + out 97.63; so by default it only BOOTS the machine - the seed's tail and the boot, at -10 dB, lp 1.8k
# (97.75, parity) - and then the song takes over. T3_BYTE_SECS=all|bookends keep the rest. T3_R10=none reproduces v9.
R10 = os.environ.get("T3_R10", "byte")
# T3_R11 = bronze (v11, palette round). The last of machine-kit (seven album songs) leaves t3: its own KIT, c8-kit,
# made of the song's materials. The kick (kr) is a sine on D1 with a pitch that drops into place PLUS a low modal
# membrane - a skin struck with a bronze-weighted beater, a "tok" over the sub, the kendang's low stroke in a techno
# floor - and the open hat (oh) is a small bronze: a high modal bell over a breath of noise, a cengceng's tick, not
# a machine's hiss. The pump stays keyed on kick.kr. Scored: the kit's own kick cost spectrum 97 -> 80 (A1 sine:
# +4 dB at 61-71 Hz, -4 at 97-250) and 75 (A2 skin over a 0.375-ratio sine: still 83% of its energy under 60 Hz) - the
# machine's kick carries 90-250 Hz the floor needs - so by default only the open hat is bronze (T3_R11_KICK=bronze
# keeps the kick for later work). T3_R11=none reproduces v10.
R11 = os.environ.get("T3_R11", "bronze")
# T3_R12 = gendy (v12, palette round). ENTROPY HAS A VOICE. In the decay - where cells are lost at random and the
# ring empties - a GENDYN voice enters (wM's new layer: Xenakis's dynamic stochastic synthesis, GENDY3, 1991; new to
# the album): one wave cycle drawn through twelve breakpoints that each take a random step every cycle. It holds the
# drone's D and A an octave up, and its velocity - which here drives how far each breakpoint may stray, and how far
# each segment's length may wander - rises bar by bar through the decay: a clean tone going grainy, then sliding,
# order dissolving as the automaton thins. It eases out through the first bars of the out and is gone well before the
# last bell (the ~913 Hz ring t4 catches). Scored s0 (pin 6014b933; v11 97.828): through all the decay + out at -12 dB
# 97.33 (spectrum 97 -> 92), notched at 750 and -15 dB 97.52, high-passed at 900 Hz 97.34, as the DRONE (replacing the
# tanpura, level-matched) 97.66; a MOMENT - only the decay's last six bars, the ring emptying, at -16 dB - 97.74, the
# default. This song sits on the album envelope's tolerance edge: a sustained new timbre anywhere costs. Knobs:
# T3_GENDY_FROM (0 = all the decay + out), T3_R12_MODE=drone, T3_GENDY_HP. T3_R12=none reproduces v11.
R12 = os.environ.get("T3_R12", "gendy")
R12MODE = os.environ.get("T3_R12_MODE", "decay")   # "decay": an added voice in decay/out; "drone": gendyn IS the drone
C3_GENDY = {"about": "chirper-two: Xenakis's dynamic stochastic synthesis (gendyn) whose disorder rides velocity: amp and "
                     "time steps grow with vel, Cauchy jumps, a slow swell; entropy as a timbre.",
            "synth": {"layers": [{"type": "gendyn", "gendyn": {
                "points": 12,
                "amp": {"value": 0.005, "mod": [{"src": "vel", "amount": 0.12}]},
                "time": {"value": 0.0, "mod": [{"src": "vel", "amount": 0.12}]},
                "spread": 0.8, "dist": "cauchy"}}],
                "filters": [{"kind": "lp", "cutoff": 2600, "q": 0.5}],
                "amp": {"a": "1.5s", "s": 1, "r": "2.5s"}},
            "fx": []}
# T3_R13 = colony (v13, section round on w5, 2:03-2:34: the glider's end, "static, little new vs w4"). THE PLANE.
# All song long the automaton has been a LINE - one row of cells, the next row its future. Here, for the glider's
# last twelve bars, a PLANE appears beside it: Conway's Life (wM's `gen: life`) on an 8 x 8 torus, seeded with a
# single glider, read column by column on a kalimba over the song's 7-limit JI (bottom row low). The glider walks
# diagonally through the grid, so the figure keeps its shape and slides in pitch and time - a creature, not a rule.
# For two bars it has the floor to itself: the kick and both djembe rings stop (it has left the line), and they come
# back for the traffic, and one low gong (the section gong's D2) holds the gap. New tracks + one gain lane. Scored s0
# (v12 97.740): colony alone 97.729 (w5 still static); + the two-bar stop 97.604 (static cleared - the kick's absence
# is the motion - but the low end goes); one bar 97.669 (static); stop without the kick 97.722 (static); + the gong
# 97.662, the default (static again: the gong's ring is still). Knobs: T3_LEAVE, T3_LEAVE_BARS, T3_LEAVE_GONG,
# T3_COLONY_GAIN. T3_R13=none reproduces v12.
R13 = os.environ.get("T3_R13", "colony")
# T3_R14 = story (v14, whole-song round). THE CELL TELLS IT. The voice used to say one thing - "I only know the two
# beside me / and they are enough" - five times. Now that line is the hymn's refrain and the first thing the cell
# sings, and the rest of the song it says what knowing two neighbours is like, a pair of lines per section:
#   glider (later):  "the left one is weather" / "the right one is news"
#   peak (bars 8, 12; the old peak lines sat at bars 28/32, which the hymn's shorter peak never reaches):
#                    "two rumors and a mirror" / "add up to the next of me"   (left, self, right -> the rule)
#   decay (new):     "when the left goes dark" / "I keep its count"
# Same voice, same humanize, a D-minor tune per line (`chirp tts --sing`, src/t3/s3a..s5b.json), snapped by the
# just tuning like the rest. T3_R14=none reproduces v13.
R14 = os.environ.get("T3_R14", "story")
# T3_R15 = space (v15, whole-song round). THE RING GOES ROUND YOU. A 1-D automaton on a ring is a circle of cells;
# now the song's cells are placed in space (wM's `orbit` fx, after Chowning's moving sources, 1971 - the first
# computer-music spatialiser; new to the album). The kotekan - the gamelan that plays dead cells beside live ones -
# circles the listener's head at 3 m, a lap every eight bars, darker as it passes behind; the Life colony's glider
# swings a figure eight in front, nearer and farther, as a creature does. And the mix finally answers the album's
# envelope (compscore now says which way the worst band misses): t3 was +7.7 dB at 547 Hz and short under 250, so
# the master's old 250 Hz cut softens (-2 -> -0.5 dB) and a 550 Hz cut (-2 dB) joins it; the next worst band was then
# 1.9 kHz (+6.9 dB), so a 1.9 kHz cut (-1.5 dB, T3_HIMID) too. Spectrum 94.5 -> 99.0. T3_R15=none reproduces v14.
R15 = os.environ.get("T3_R15", "space")
# T3_R16 = reboot (v16, section round on w2, 0:30-1:01: the boot into A, "static"). THE MACHINE COMES UP TWICE.
# The boot's last bar goes dark - every track, its reverb too (a gain lane after the fx), except the bytebeat that has
# been booting it - and A starts on the far side of the silence with only the automaton: mallets, bass, drone. The
# floor (kick, hats, rim, the djembe rings, shekere, bells) waits four bars and comes in on A's fifth: the rule has to
# be running before anything dances to it. Gain lanes, plus a 45 Hz master lift (+2.5 dB, T3_SUB45): four bars
# without the kick left the album's sub band 7.2 dB short (s0 97.88 without it, 98.13 with). T3_R16=none reproduces v15.
R16 = os.environ.get("T3_R16", "reboot")
FLOOR = {"kick", "hats", "ohat", "rim", "toms", "ca-kit", "ca-kit2", "shek", "rbell", "rbell2", "hfill"}
# T3_R17 = fade (v17, section round on w9, 4:07-4:38: the decay, "static"). THE FLOOR DIES WITH THE CELLS. In the
# decay the automaton loses cells at random - but the floor under it kept time as if nothing were happening: a kick on
# every beat, hats on every eighth. Now the floor dies too. The hats thin away over three bars from the decay's fifth;
# the kick, the song's heartbeat, weakens from its ninth bar and is gone by its fourteenth, so the last bars of the
# decay are the dying cells, the drone, the cell's last lines ("when the left goes dark / I keep its count") and the
# gendyn voice coming apart - no pulse. Both return for the out. Gain lanes, and the master follows the band report
# (without the floor the mids read louder): 550 Hz -2 -> -3 dB, 292 Hz -1 dB, 1.9 kHz -1.5 -> -2.5 dB, 45 Hz +2.5 ->
# +3.5 dB (s0 97.97 without, 98.14 with). T3_R17=none reproduces v16.
R17 = os.environ.get("T3_R17", "fade")
R11KICK = os.environ.get("T3_R11_KICK", "machine")   # "bronze": the kit's own kick too (cost spectrum 97 -> 75-80)
C8_KIT = {
    "about": "chirper-two: Three Neighbours' own kit - kr a D1 sine kick that drops into place with a low modal membrane "
             "(skin and bronze), oh a small bronze tick (a high modal bell over noise).",
    "play": {"len": "/16", "vel_sens": 0.45, "humanize": {"time": "1ms", "vel": 0.03}},
    "kit": {
        "kr": {"pitch": os.environ.get("T3_KICK_PITCH", "A2"), "patch": {
            "synth": {"layers": [
                {"name": "tone", "wave": "sine", "ratio": float(os.environ.get("T3_KICK_SUBRATIO", "0.375"))},
                {"name": "skin", "type": "modal", "modes": "membrane", "decay": "0.22s", "damp": 0.55, "bright": 0.3,
                 "strike": 0.2, "tilt": -3, "vary": 0.2, "level": os.environ.get("T3_KICK_SKIN", "-2dB")},
                {"name": "click", "type": "noise", "level": {"value": "-70dB", "mod": [{"src": "env.c", "amount": 52}, {"src": "vel", "amount": 8}]}}],
                "pitch": {"value": 0, "mod": [{"src": "env.p", "amount": 14}]},
                "env": {"p": {"a": "0.1ms", "d": "38ms", "s": 0, "curve": 3}, "c": {"a": "0.1ms", "d": "2ms", "s": 0}},
                "filters": ["hp cutoff=25", {"kind": "lp", "cutoff": {"value": "2.2k", "mod": [{"src": "vel", "amount": 1}]}}],
                "amp": {"a": "0.3ms", "d": "480ms", "s": 0, "r": "30ms", "curve": 3}},
            "play": {"vel_sens": 0.4}}},
        "oh": {"pitch": "A6", "gain": "-10dB", "patch": {
            "synth": {"layers": [
                {"name": "air", "type": "noise", "level": "-14dB"},
                {"name": "bronze", "type": "modal", "modes": "bell", "decay": "0.35s", "damp": 0.5, "bright": 0.7,
                 "strike": 0.3, "tilt": -1, "vary": 0.3, "level": "-4dB"}],
                "filters": ["hp cutoff=2500"],
                "amp": {"a": "0.2ms", "d": "320ms", "s": 0, "r": "40ms", "curve": 3}},
            "play": {"vel_sens": 0.6}}}}}
C3_BYTE = {"about": "chirper-two: a bytebeat whose multipliers are 7-limit JI (t*4..7 = 4:5:6:7 on the note) chosen by "
                    "rule 30 on the bits of a sixteenth counter, a rule-90 bit bouncing the octave; clock 16744 puts t*4 "
                    "on the note and a step on a 124-bpm sixteenth for D3.",
           "synth": {"layers": [{"type": "bytebeat", "bytebeat": {
               "formula": "t*((4+((t/4548^(t/2274|t/1137))&1)+2*((t/18192^(t/9096|t/4548))&1))<<((t/2274^t/1137)&1))",
               "clock": 16744}}],
               "amp": {"a": "8ms", "s": 1, "r": "120ms"}},
           "fx": []}
RULE_BITS = {r: [(r >> k) & 1 for k in range(7, -1, -1)] for r in (30, 90)}
ANSWERS = [(14.75, ["C6", "A5", "D6"]), (12.9, ["F6", "E6", "D6"]), (14.75, ["A6", "G6", "A6"]), (9.9, ["C6", "D6"])]
HYMN = [(0, 3, 7), (8, 14, 17), (3, 7, 12), (0, 3, 7), (5, 10, 14), (10, 14, 17), (3, 7, 12), (8, 14, 17),
        (0, 3, 7), (8, 14, 17), (7, 10, 16), (7, 10, 16), (8, 14, 17), (10, 14, 17), (0, 3, 7), (0, 3, 7)]
HYMN_BASS = [38, 34, 41, 38, 43, 36, 41, 34, 38, 34, 33, 33, 34, 36, 38, 38]
HINT1 = [("A3", 2), ("D4", 1), ("E4", 1), ("F4", 2), ("E4", 1), ("D4", 1), ("C4", 2), ("A3", 1), ("D4", 4)]
HINT4 = [("F4", 2), ("E4", 1), ("D4", 1), ("C4", 2), ("D4", 4)]
# T3_R2 = live (v2, wM's tunings, complex systems and morph). The machine TUNES ITSELF: the notes are written in plain
# 12-TET D minor and the song's `tuning` ramps from 12-TET into the 7-limit just scale over ten bars from the boot (F, Bb
# and C sag a third of a semitone into the septimal minor third, sixth and harmonic seventh as you listen); chords are
# the scale's own sevenths (the D one is 1 7/6 3/2 7/4). A SELF-WRITING DRUM MACHINE joins: chirp's own cellular
# automaton (`gen: {type: ca}`) plays a percussion kit in the glider (rule 110) and the peak (rule 30), a second ring
# beside mine. A LORENZ attractor (a song `var` with a `system`) swirls the vibes' filter and the glock's place in the
# stereo field. In the TRAFFIC break the rotating marimba canon MORPHS into the tanpura's spectrum and back (`morph`
# fx keyed by the drone). T3_R2=none reproduces v1.
R2 = os.environ.get("T3_R2", "live")
SEMI = [0, 2, 3, 5, 7, 8, 10]                              # 12-TET D natural minor (the tuning snaps it to JI)
# T3_R3 = sing (v3, wM's singing voice): in the glider a voice SINGS, from a cell's point of view: "I only know the two
# beside me ... and they are enough" (`chirp tts --sing`, src/t3/sing*.json, humanize 0.4), its notes snapped by the
# song's just tuning like everything else; once more, softer, at the peak. T3_R3=none reproduces v2.
R3 = os.environ.get("T3_R3", "sing")
SING = []


STORY = []


def sing(name, at, scale=1.0, dst=None):
    dst = SING if dst is None else dst
    src = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t3", name)))["tracks"][0]
    for nt in src["notes"]:
        m = round(69 + 12 * math.log2(float(nt["pitch"].rstrip("hz")) / 440))
        d = {"at": round(at + nt["at"], 4), "len": nt["len"], "ph": nt["ph"], "pitch": f"m{m}",
             "vel": round(nt["vel"] * scale, 3)}
        if nt.get("expr_path"):
            d["expr_path"] = nt["expr_path"]
        dst.append(d)
    return src["patch"]


JI_STEPS = ["9/8", "7/6", "4/3", "3/2", "14/9", "7/4", "2/1"]


def jm(deg, base=D3):
    """Fractional MIDI number of scale degree DEG (may run past 7 into higher octaves) above BASE."""
    o, d = divmod(deg, 7)
    if R2 == "live":
        return base + 12 * o + SEMI[d]
    return base + 12 * o + 12 * math.log2(RATIOS[d])


def hz_m(m):
    return f"m{m:.3f}"


def ratio_m(root_m, r):
    return root_m + 12 * math.log2(r)


def step(row, rule):
    return [(rule >> (row[(i - 1) % W] << 2 | row[i] << 1 | row[(i + 1) % W])) & 1 for i in range(W)]


def euclid(k, n, rot=0):
    pat = [((i * k) % n) < k for i in range(n)]
    return [pat[(i - rot) % n] for i in range(n)]


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if e[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:  # let it ring past the next onset (struck bars do)
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt if ln <= gap + 1e-6 else s + gap
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


def build():
    rng = random.Random(3)
    names = ("kick", "hats", "ohat", "rim", "bar", "barlo", "barx", "vibes", "glock", "bell", "gong", "toms", "bass", "chord", "drone",
             "rise", "hint", "hymn", "hbass", "kot", "errl", "errr")
    T = {k: Track(k) for k in names}
    row = [0] * W
    row[8] = 1
    row2 = [0] * W  # the peak's second automaton (rule 90)
    bars, pos = [], 0.0
    for name, n, rule in FORM:
        for i in range(n):
            bars.append((pos, name, i, n, rule))
            pos += 4.0
    total = pos
    rows = []
    for bi, (start, sec, i, n, rule) in enumerate(bars):
        prev = row
        if bi > 0:
            row = step(row, rule)
            if R4 == "hymn" and sec == "decay" and i == 0:   # three neighbours left
                row = [1 if c in (0, 3, 9) else 0 for c in range(W)]
            if sec == "decay":  # entropy: a cell is lost now and then (v4: never the last one, cell 9, whose 14/9 bar
                # at ~913 Hz is the ring t4 opens by catching)
                row = [c if (rng.random() > 0.06 or (R4 == "hymn" and k == 9)) else 0 for k, c in enumerate(row)]
            if sec in ("decay", "out") and sum(row) == 0:
                row = [0] * W
                row[8] = 1
            if sum(row) == 0:  # a dead ring is reseeded from a single cell
                row[rng.randrange(W)] = 1
        if sec == "peak" and i == 0:
            row2 = [0] * W
            row2[3] = 1
        elif sec == "peak":
            row2 = step(row2, 90)
        rows.append(row)
        if R9 == "cone" and sec == "A" and 10 <= i < 26:
            if i == 10:
                shadow = list(row)
                shadow[8] ^= 1
            else:
                shadow = step(shadow, rule)
            diff = [c for c in range(W) if shadow[c] != row[c]]
            for c in diff:
                vel = 92 if i == 10 else (72 if len(diff) < 6 else 56)
                T["errl" if c < 8 else "errr"].add(start + c * 0.25, 0.5, hz_m(jm((c * 3) % 15, 86)), vel)
        pop = sum(row)
        born = [c for c in range(W) if row[c] and not prev[c]]
        died = [c for c in range(W) if prev[c] and not row[c]]
        groove = sec in ("boot", "A", "glider", "peak", "decay", "hymn")
        full = sec in ("glider", "peak")
        # ---- the chord root: every four bars the population picks it ----
        if i % 4 == 0:
            root_deg = ROOTS[pop % 4]
        root_m = jm(root_deg, 38)  # bass register (D2 base)
        # ---- the deep four ----
        if groove and sec == "glider":  # half time: the floor drops away under the gliders
            for b in (0.0, 2.5):
                T["kick"].add(start + b, 1.0, "kr", 112 if b == 0 else 100)
        elif groove:
            for b in range(4):
                T["kick"].add(start + b, 1.0, "kr", 112 if b == 0 else 104)
        # ---- hats: Euclidean, rotated by the population ----
        if groove and sec not in ("boot", "glider"):
            k = {"A": 7, "peak": 9, "decay": 5, "hymn": 7}.get(sec, 5)
            for s, on in enumerate(euclid(k, 16, pop % 16)):
                if on:
                    T["hats"].add(start + s * 0.25 + 0.01, 0.1, "h", 50 + (10 if s % 4 == 2 else 0) + rng.randint(-5, 5))
        if sec in ("glider", "peak", "hymn"):
            for b in (0.5, 1.5, 2.5, 3.5):
                T["ohat"].add(start + b + 0.01, 0.3, "oh", 58)
        if sec in ("peak", "hymn"):
            T["rim"].add(start + 1.0, 0.3, "cp", 84)
            T["rim"].add(start + 3.0, 0.3, "cp", 90)
        # ---- THE ROW: live cells strike ----
        line = "glock" if sec in ("seed", "glider") else "bar"  # the glider's row rings on the glock and vibes
        for c in range(W):
            if row[c]:
                deg = (c * 3) % 15
                v = (78 if c % 4 == 0 else 66) + rng.randint(-6, 6)
                if sec in ("out",):
                    v -= 10
                if sec == "hymn":
                    v -= 16
                T["barlo" if sec == "decay" else ("barx" if (sec == "traffic" and R2 == "live") else line)].add(start + c * 0.25, 1.2 if line == "bar" else 2.0,
                                                          hz_m(jm(deg, (50 if sec == "decay" else 62) if line == "bar" else 74)),
                                                          v, "?0.8" if sec == "out" else "")
                if sec == "glider" and c % 2 == 0:
                    T["vibes"].add(start + c * 0.25, 2.0, hz_m(jm(deg, 62)), v - 8)
        if R8 == "kotekan" and sec in ("A", "peak"):   # the gangsa fills the neighbourhood's gaps
            for c in range(W):
                if not row[c] and (row[(c - 1) % W] or row[(c + 1) % W]):
                    T["kot"].add(start + c * 0.25, 0.22, hz_m(jm((c * 3) % 15, 74)), 60 if c % 4 == 0 else 52)
        if sec == "peak":  # the second automaton on the glock
            for c in range(W):
                if row2[c]:
                    T["glock"].add(start + c * 0.25 + 0.125, 1.5, hz_m(jm((c * 5) % 14, 74)), 58 + rng.randint(-5, 5))
        # ---- births ring on the vibes, deaths fall on the toms ----
        if sec == "glider":  # the marimba only answers the births
            for c in born[:4]:
                T["bar"].add(start + c * 0.25, 1.2, hz_m(jm((c * 3) % 15, 62)), 74, "?0.85")
        elif sec not in ("seed", "traffic", "out", "hymn"):
            for c in born[:3]:
                T["vibes"].add(start + c * 0.25, 3.0, hz_m(jm((c * 3) % 15 + 7, 62)), 70, "?0.8")
            if sec not in ("boot",):
                for c in died[:3]:
                    T["toms"].add(start + c * 0.25, 0.8, hz_m(jm(ROOTS[c % 4], 43)), 76, "?0.7")
        elif sec == "seed":
            for c in born[:2]:
                T["vibes"].add(start + c * 0.25, 4.0, hz_m(jm((c * 3) % 15 + 7, 62)), 60)
        # ---- septimal chords (6:7:9 on the root), held, in the glider and the peak ----
        if full and i % 4 == 0:
            cm = root_m + 24
            heads = (",".join(hz_m(jm(root_deg + k, 62)) for k in (0, 2, 4, 6)) if R2 == "live" else
                     ",".join(hz_m(ratio_m(cm, r)) for r in (1, 7 / 6, 3 / 2, 7 / 4)))
            T["chord"].add(start, 15.6, heads, 76 if sec == "glider" else 62)
        # ---- the plucked bass: Euclidean, rotated by the population ----
        if (groove and sec not in ("decay", "hymn")) or (sec == "traffic" and i % 4 == 0):
            if sec == "glider":
                if i % 2 == 0:
                    T["bass"].add(start, 7.6, hz_m(root_m), 92)
            elif sec == "traffic":
                T["bass"].add(start, 15.6, hz_m(root_m), 90)
            else:
                k = 3 + pop % 4
                for s, on in enumerate(euclid(k, 16, (pop * 3) % 16)):
                    if on:
                        oct_up = 12 if s % 8 == 6 else 0
                        T["bass"].add(start + s * 0.25, 0.4, hz_m(root_m + oct_up), 96 if s == 0 else 84)
        # ---- the bell tolls the uptime; the gong marks every change of rule ----
        if i % 8 == 0 and sec not in ("traffic",):
            T["bell"].add(start, 8.0, hz_m(jm(0, 50)), 70 if sec != "out" else 60)
        if i == 0 and sec != "boot":
            T["gong"].add(start, 12.0, hz_m(jm(0, 38)), 84)
        if sec == "out" and i == n - 4:
            T["gong"].add(start, 16.0, hz_m(jm(0, 38)), 70)
        # ---- the drone holds the tuning ----
        if i % 8 == 0 and sec != "seed" or (sec == "seed" and i == 4):
            ln = min(8, n - i) * 4 - 0.2
            T["drone"].add(start, ln, ",".join(hz_m(m) for m in (jm(0, 38), jm(4, 38))), 64)
        if R3 == "sing" and sec == "glider" and i in (2, 6, 14, 18):
            if R14 == "story" and i in (14, 18):
                sing("s3a.json" if i == 14 else "s3b.json", start, 1.0, STORY)
            else:
                sing("sing1.json" if i in (2, 14) else "sing2.json", start)
        if R3 == "sing" and sec == "peak" and i in (28, 32) and R14 != "story":   # (unreached since the hymn
            sing("sing1.json" if i == 28 else "sing2.json", start, 0.8)              #  shortened the peak to 18 bars)
        if R3 == "sing" and R14 == "story" and sec == "peak" and i in (8, 12):
            sing("s4a.json" if i == 8 else "s4b.json", start, 1.0, STORY)
        if R3 == "sing" and R14 == "story" and sec == "decay" and i in (2, 6):
            sing("s5a.json" if i == 2 else "s5b.json", start, 1.0, STORY)
        if sec == "traffic" and i == n - 4:
            T["rise"].add(start, 16.0, "D4", 76)
        if R4 == "hymn":
            if (sec == "A" and i in (12, 22)) or (sec == "decay" and i == 6):   # the tune on the kora, augmented, an octave up
                at = start
                for nt, ln in (HINT1 if (sec, i) == ("A", 12) else HINT4):
                    T["hint"].add(at, 2 * ln, nt[:-1] + str(int(nt[-1]) + 1), 74)
                    at += 2 * ln
            if sec == "hymn":
                ch = HYMN[i]
                T["hymn"].add(start, 3.9, ",".join(f"m{50 + s}" for s in ch), 74 if i % 4 else 82)
                r = HYMN_BASS[i]
                for b, ln, off, v in ((0, 1.4, 0, 96), (1.5, 0.45, 7, 80), (2.5, 0.45, 12, 84), (3.5, 0.45, 7, 78)):
                    T["hbass"].add(start + b, ln, f"m{r + off}", v)
                if i % 4 == 0:
                    for who, src in (("hlead", "h"), ("hlow", "l")):
                        hum(who, f"{src}{i // 4 + 1}.json", start)
            if sec == "out" and i == 6:                    # the last words, the low voice alone
                hum("hlow", "l4.json", start)
            if sec == "out" and i == n - 1:                # the last cell's ring, for t4 to catch
                T["bar"].add(start + 3.5, 4.0, hz_m(jm(12, 62)), 64)
    secs, s0 = [], 0.0
    for name, n, rule in FORM:
        secs.append((name, s0, n, rule))
        s0 += n * 4
    return total, bars, secs, T, rows


HUM = {"hlead": [], "hlow": []}
HUM_PATCH = {}


def hum(dst, name, at):
    src = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t3", name)))["tracks"][0]
    HUM_PATCH[dst] = src["patch"]
    for nt in src["notes"]:
        d = {"at": round(at + nt["at"], 4), "len": nt["len"], "ph": nt["ph"], "pitch": nt["pitch"], "vel": nt["vel"]}
        if nt.get("expr_path"):
            d["expr_path"] = nt["expr_path"]
        HUM[dst].append(d)


def sing_patch():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "t3", "sing1.json")))["tracks"][0]["patch"]


def patches():
    def modal(modes, decay, damp, bright, strike=0.3, tilt=-1.0, vary=0.4, a="1ms", d="4s", r="1.5s", extra=None):
        layer = {"type": "modal", "modes": modes, "decay": decay, "damp": damp,
                 "bright": {"value": bright, "mod": [{"src": "vel", "amount": 0.35}]},
                 "strike": {"value": strike, "mod": [{"src": "rand", "amount": 0.08}]}, "tilt": tilt, "vary": vary}
        if extra:
            layer.update(extra)
        return {"synth": {"layers": [layer], "amp": {"a": a, "d": d, "s": 0, "r": r, "curve": 3}},
                "play": {"vel_sens": 0.6}}
    return {
        "c8-bar": {"about": "chirper-two: a rosewood bar on the modal layer (marimba modes 1:4:10), hard yarn.",
                   **modal("bar", "1.4s", 0.25, 0.45, strike=0.22)},
        "c8-vibes": {"about": "chirper-two: a vibraphone bar on the modal layer, soft mallet, long ring.",
                     **modal("vibes", "4s", 0.08, 0.3, strike=0.3, d="6s", r="3s")},
        "c8-glock": {"about": "chirper-two: a glockenspiel free bar on the modal layer (1:2.76:5.40:8.93), brass mallet.",
                     **modal("glock", "2.5s", 0.1, 0.7, strike=0.15, d="4s")},
        "c8-bell": {"about": "chirper-two: a church bell on the modal layer (hum, prime, tierce, quint, nominal).",
                    **modal("bell", "7s", 0.03, 0.5, strike=0.4, d="9s", r="4s")},
        "c8-tom": {"about": "chirper-two: a tuned membrane on the modal layer, centre strike, a pitch that settles.",
                   **modal("membrane", "0.9s", 0.4, 0.4, strike=0.3, tilt=-2, extra={"sharp": 60}, d="2s", r="0.5s")},
    }


def main():
    total, bars, secs, T, rows = build()
    if R7 == "hands":
        T["hats"].ev = [(a, ln, "sk" if h == "h" else h, v, art) for a, ln, h, v, art in T["hats"].ev]
    if R8 == "kotekan":
        T["rim"].ev = [(a, ln, "s" if h == "cp" else h, v, art) for a, ln, h, v, art in T["rim"].ev]
    st = {n: s for n, s, k, r in secs}
    pump = {"type": "pump", "on": "kick.kr", "depth": "-6dB", "attack": "3ms", "release": "300ms", "curve": 0.8}
    dyn = [["0b", -4.0], [f"{st['boot']}b", -1.0], [f"{st['A']}b", 0.0], [f"{st['glider']}b", -1.5],
           [f"{st['traffic'] - 0.01}b", -1.5], [f"{st['traffic']}b", -5.0],
           [f"{st['peak'] - 0.01}b", -5.0], [f"{st['peak']}b", 0.0], [f"{st['decay'] - 0.01}b", 0.0], [f"{st['decay']}b", -2.5],
           [f"{st['out']}b", -4.0],
           [f"{total}b", -5.0]]
    tracks = [
        {"name": "kick", "patch": "c8-kit" if (R11 == "bronze" and R11KICK == "bronze") else "machine-kit",
         "gain": os.environ.get("T3_KICK_GAIN", "-2dB") if (R11 == "bronze" and R11KICK == "bronze") else "0dB", "score": T["kick"].score(total)},
        {"name": "hats", "patch": "afro-perc" if R7 == "hands" else "machine-kit",
         "gain": os.environ.get("T3_SHEK_GAIN", "-15dB") if R7 == "hands" else "-5dB", "pan": 0.12,
         "fx": ["hp cutoff=600", "reverb kind=room decay=0.5s mix=0.12"], "score": T["hats"].score(total)},
        {"name": "ohat", "patch": "c8-kit" if R11 == "bronze" else "machine-kit", "gain": "-9dB", "pan": -0.12, "fx": ["hp cutoff=800"],
         "score": T["ohat"].score(total)},
        {"name": "rim", "patch": "djembe" if R8 == "kotekan" else "machine-kit", "gain": "-7dB", "fx": ["reverb kind=plate decay=1.0s mix=0.2"],
         "score": T["rim"].score(total)},
        {"name": "bar", "patch": "c8-bar", "gain": "-4dB", "pan": -0.15, "sends": {"hall": "-10dB"},
         "fx": [{"type": "delay", "time": "3/16", "feedback": 0.25, "mix": 0.15, "ping_pong": True, "tone": 3500}],
         "score": T["bar"].score(total)},
        {"name": "barlo", "patch": "c8-bar", "gain": "-3dB", "pan": 0.15, "sends": {"hall": "-8dB"},
         "fx": ["lp cutoff=1400"], "score": T["barlo"].score(total)},
        {"name": "vibes", "patch": "c8-vibes", "gain": "-9dB", "pan": 0.3, "sends": {"hall": "-6dB"},
         "fx": ["chorus mix=0.25"] + ([{"type": "filter", "kind": "lp", "q": 1.2,
                                        "cutoff": {"value": 900, "mod": [{"src": "var.swirl", "amount": 1}]}}]
                                      if R2 == "live" else []), "score": T["vibes"].score(total)},
        {"name": "glock", "patch": "c8-glock", "gain": "-12dB",
         "pan": ({"value": 0.35, "mod": [{"src": "var.swirl", "amount": -0.25}]} if R2 == "live" else 0.35),
         "sends": {"hall": "-6dB"},
         "fx": [{"type": "delay", "time": "1/8", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 5000}],
         "score": T["glock"].score(total)},
        {"name": "bell", "patch": "c8-bell", "gain": "-12dB", "pan": -0.3, "sends": {"hall": "-4dB"},
         "score": T["bell"].score(total)},
        {"name": "gong", "patch": "modal-gong", "gain": "-8dB", "sends": {"hall": "-6dB"}, "score": T["gong"].score(total)},
        {"name": "toms", "patch": "c8-tom", "gain": "-6dB", "pan": 0.1, "fx": ["reverb kind=room decay=0.8s mix=0.2"],
         "score": T["toms"].score(total)},
        {"name": "bass", "patch": "pluck", "gain": "-3dB", "fx": ["lp cutoff=1800", "drive drive=0.2", pump],
         "score": T["bass"].score(total)},
        {"name": "chord", "patch": "c8-vibes", "gain": "-14dB", "pan": -0.05, "sends": {"hall": "-4dB"},
         "fx": ["chorus mix=0.3"], "score": T["chord"].score(total)},
        {"name": "drone", "patch": "tanpura", "gain": "-16dB", "fx": ["hp cutoff=80"], "score": T["drone"].score(total)},
        {"name": "rise", "patch": "fx-riser-endless amp.a=16b", "gain": "-14dB", "score": T["rise"].score(total)},
        *([{"name": nm, "patch": "glass", "gain": os.environ.get("T3_ERR_GAIN", "-6dB"), "pan": pn,
            "sends": {"hall": "-8dB"}, "fx": ["hp cutoff=400"], "score": T[nm].score(total)}
           for nm, pn in (("errl", -0.55), ("errr", 0.55))] if R9 == "cone" else []),
        *([{"name": "kot", "patch": "gamelan", "gain": os.environ.get("T3_KOT_GAIN", "3dB"), "pan": 0.35,
            "sends": {"hall": "-10dB"}, "fx": ["hp cutoff=300", "peak cutoff=1500 gain=-4dB q=0.8"],
            "score": T["kot"].score(total)}] if R8 == "kotekan" else []),
        *([{"name": "sing", "patch": sing_patch(), "gain": os.environ.get("T3_SING_GAIN", "-10dB"), "pan": 0.05,
            "sends": {"hall": "-6dB"},
            "fx": ["hp cutoff=140", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 3500}],
            "notes": SING}] if R3 == "sing" else []),
        *([{"name": "story", "patch": sing_patch(), "gain": os.environ.get("T3_STORY_GAIN", "-2dB"), "pan": -0.05,
            "sends": {"hall": "-6dB"},
            "fx": ["hp cutoff=140", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                   {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 3500}],
            "notes": STORY}] if (R3 == "sing" and R14 == "story") else []),
    ]
    if R2 == "live":
        L = {n: k for n, s, k, r in secs}
        tracks += [
            {"name": "barx", "patch": "c8-bar", "gain": "-4dB", "pan": -0.15, "sends": {"hall": "-8dB"},
             "fx": [{"type": "morph", "key": "drone", "mode": "morph",
                     "amount": {"value": 0, "mod": [{"src": "auto.m", "amount": 1}]}}],
             "auto": {"m": {"points": [["0b", 0.0], [f"{st['traffic']}b", 0.0], [f"{st['traffic'] + 28}b", 0.75],
                                       [f"{st['traffic'] + 44}b", 0.75], [f"{st['peak'] - 4}b", 0.0],
                                       [f"{total}b", 0.0]]}},
             "score": T["barx"].score(total)},
            {"name": "ca-kit", "patch": "djembe" if R7 == "hands" else "machine-kit",
             "gain": os.environ.get("T3_DJ_GAIN", "-8dB") if R7 == "hands" else "-11dB", "pan": 0.22, "seed": 110,
             "fx": ["hp cutoff=300", "reverb kind=room decay=0.6s mix=0.15"],
             "score": f"R/{st['glider']:g}b",
             "gen": {"type": "ca", "rule": 110, "width": 16, "init": "random", "poly": 2,
                     "notes": "s sh t sh c sh s sh" if R7 == "hands" else "rs h cb h oh h rs h", "n": L["glider"] * 16, "len": "/16"}},
            {"name": "ca-kit2", "patch": "djembe" if R7 == "hands" else "machine-kit",
             "gain": os.environ.get("T3_DJ_GAIN2", "-9dB") if R7 == "hands" else "-12dB", "pan": -0.22, "seed": 30,
             "fx": ["hp cutoff=400", "reverb kind=room decay=0.6s mix=0.15"],
             "score": f"R/{st['peak']:g}b",
             "gen": {"type": "ca", "rule": 30, "width": 16, "init": "center", "poly": 2,
                     "notes": "sh s sh t sh c sh b" if R7 == "hands" else "h rs h cb h oh h cp", "n": L["peak"] * 16, "len": "/16"}},
        ]
    if R4 == "hymn" and R5 == "breath":
        h0 = st["hymn"]
        hd = {"hd": {"points": [["0b", 0.0], [f"{h0 - 0.5}b", 0.0], [f"{h0 + 0.25}b", -40.0], [f"{h0 + 28}b", -40.0],
                                [f"{h0 + 32}b", 0.0], [f"{total}b", 0.0]]}}
        for tr in tracks:
            if tr["name"] in ("kick", "hats", "ohat", "rim"):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.hd", "amount": 1}]}}]
                tr["auto"] = hd
    if R9 == "cone" and os.environ.get("T3_CONE_DROP", "kick") == "kick":
        # when the error has filled the ring the floor stops knowing which ring is real: the kick drops out for A's
        # bars 18-21 and comes back with the kora at bar 22
        a0 = st["A"] + 18 * 4.0
        lane = {"points": [["0b", 0.0], [f"{a0 - 0.3}b", 0.0], [f"{a0 + 0.05}b", -40.0], [f"{a0 + 15.7}b", -40.0],
                           [f"{a0 + 16}b", 0.0], [f"{total}b", 0.0]]}
        for tr in tracks:
            if tr["name"] == "kick":
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.cone", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "cone": lane}
    if R13 == "colony":
        c0, c1 = st["glider"] + 56.0, st["glider"] + 104.0
        pool = " ".join(hz_m(jm(d, D3 + 12)) for d in range(8))
        tracks.append({"name": "colony", "patch": "kalimba", "gain": os.environ.get("T3_COLONY_GAIN", "-9dB"), "pan": -0.2,
                       "seed": 13, "fx": ["hp cutoff=250", {"type": "delay", "time": "3/16", "feedback": 0.25, "mix": 0.18,
                                                             "ping_pong": True, "tone": 3500}],
                       "score": f"R/{c0:g}b",
                       "gen": {"type": "life", "width": 8, "height": 8, "init": "glider", "life": "B3/S23",
                               "notes": pool, "poly": 3, "len": "/16", "n": int((c1 - c0) * 4)}})
        l0 = st["glider"] + 96.0 - 4.0 * float(os.environ.get("T3_LEAVE_BARS", "2"))
        lane = {"points": [["0b", 0.0], [f"{l0 - 0.3}b", 0.0], [f"{l0 + 0.05}b", -40.0], [f"{st['glider'] + 95.7}b", -40.0],
                           [f"{st['glider'] + 96.0}b", 0.0], [f"{total}b", 0.0]]}
        if os.environ.get("T3_LEAVE_GONG", "on") == "on":   # the glider leaves the line: one low gong holds the gap
            tracks.append({"name": "lgong", "patch": "modal-gong", "gain": "-8dB", "sends": {"hall": "-6dB"},
                           "score": f"R/{l0:g}b m38.000/8b@84"})
        for tr in tracks:
            if tr["name"] in os.environ.get("T3_LEAVE", "kick,hats,ohat,rim,toms,ca-kit,ca-kit2,shek,skin,click,tone,air,bronze").split(","):
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.leave", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "leave": lane}
    if R17 == "fade":
        d0, o0 = st["decay"], st["out"]
        fades = {"hats": [[d0 + 16 - 0.1, 0.0], [d0 + 28, -40.0]],
                 "kick": [[d0 + 32 - 0.1, 0.0], [d0 + 48, -12.0], [d0 + 56, -40.0]]}
        for tr in tracks:
            if tr["name"] in fades:
                pts = [["0b", 0.0]] + [[f"{a:g}b", v] for a, v in fades[tr["name"]]] + \
                      [[f"{o0 - 0.1:g}b", -40.0], [f"{o0:g}b", 0.0], [f"{total}b", 0.0]]
                tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.die", "amount": 1}]}}]
                tr["auto"] = {**tr.get("auto", {}), "die": {"points": pts}}
    if R16 == "reboot":
        a0 = st["A"]
        gap0, floor1 = a0 - 4.0, a0 + 4.0 * int(os.environ.get("T3_FLOOR_BARS", "4"))
        for tr in tracks:
            if tr["name"] == "byte":
                continue
            end = floor1 if tr["name"] in FLOOR else a0
            lane = {"points": [["0b", 0.0], [f"{gap0 - 0.2}b", 0.0], [f"{gap0 + 0.05}b", -40.0], [f"{end - 0.1}b", -40.0],
                               [f"{end}b", 0.0], [f"{total}b", 0.0]]}
            tr["fx"] = tr.get("fx", []) + [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.reboot", "amount": 1}]}}]
            tr["auto"] = {**tr.get("auto", {}), "reboot": lane}
    if R15 == "space":
        for tr in tracks:
            if tr["name"] == "kot" and os.environ.get("T3_ORBIT_KOT", "on") == "on":
                tr["fx"] = tr.get("fx", []) + [os.environ.get("T3_KOT_ORBIT", "orbit rate=0.0645 radius=3 mix=0.85")]
            if tr["name"] == "colony" and os.environ.get("T3_ORBIT_COLONY", "on") == "on":
                tr["fx"] = tr.get("fx", []) + [os.environ.get("T3_COLONY_ORBIT", "orbit rate=0.1 radius=3 distance=2 path=figure8 doppler=0.3")]
    if R12 == "gendy" and R12MODE == "drone":
        T["drone"].ev = [(a, ln, h, int(os.environ.get("T3_GDRONE_VEL", "50")), art) for a, ln, h, v, art in T["drone"].ev]
        for tr in tracks:
            if tr["name"] == "drone":
                tr["patch"] = "c3-gendy"
                tr["gain"] = os.environ.get("T3_GDRONE_GAIN", "-16dB")
                tr["score"] = T["drone"].score(total)
    if R12 == "gendy" and R12MODE == "decay":
        gd = Track("gendy")
        a0, nd = st["decay"], 18
        k0 = int(os.environ.get("T3_GENDY_FROM", "12"))   # 12: only the decay's last six bars, the ring emptying
        for k in range(k0, nd, 2):   # two bars a note, disorder rising
            gd.add(a0 + 4.0 * k, 8.0, ",".join(hz_m(m) for m in (jm(0, 50), jm(4, 50))), int(30 + 90 * k / (nd - 2)))
        o0, go = st["out"], Track("gendy-out")
        for k in range(0, 8 if k0 == 0 else 0, 2):    # easing out through the out's first eight bars (its own gain: the out is sparse)
            go.add(o0 + 4.0 * k, 8.0, ",".join(hz_m(m) for m in (jm(0, 50), jm(4, 50))), int(110 - 18 * k))
        for nm, tr, g in (("gendy", gd, "-16dB"), ("gendy-out", go, "-20dB")):
            tracks.append({"name": nm, "patch": "c3-gendy", "gain": os.environ.get("T3_" + nm.upper().replace("-", "_") + "_GAIN", g),
                           "pan": 0.0, "fx": ["hp cutoff=" + os.environ.get("T3_GENDY_HP", "120"), "peak cutoff=750 gain=-6dB q=0.8",
                                              "reverb kind=hall decay=3s mix=0.3"], "score": tr.score(total)})
    if R10 == "byte":
        byte = Track("byte")
        plan = [(st["seed"] + 16.0, st["boot"], 44, 64), (st["boot"], st["A"], 76, 80),
                (st["traffic"], st["peak"], 38, 38), (st["out"], st["out"] + 32.0, 66, 34)]
        BYTE_SECS = os.environ.get("T3_BYTE_SECS", "boot")
        if BYTE_SECS == "bookends":   # the machine boots and powers down, nothing in between
            plan = [plan[1], plan[3]]
        elif BYTE_SECS == "boot":     # the machine only boots: the seed's tail and the boot, then the song takes over
            plan = [plan[0], plan[1]]
        for a0, a1, v0, v1 in plan:
            n = int(round((a1 - a0) / 8.0))
            for k in range(n):
                byte.add(a0 + 8.0 * k, 8.0, "146.83hz", v0 + (v1 - v0) * k / max(1, n - 1))
        tracks.append({"name": "byte", "patch": "c3-byte", "gain": os.environ.get("T3_BYTE_GAIN", "-10dB"), "pan": -0.15,
                       "fx": ["hp cutoff=130", "lp cutoff=" + os.environ.get("T3_BYTE_LP", "1800") + " q=0.5",
                              {"type": "delay", "time": "3/16", "feedback": 0.25, "mix": 0.18, "ping_pong": True, "tone": 2500},
                              "reverb kind=room decay=0.8s mix=0.15"],
                       "score": byte.score(total)})
    if R4 == "hymn" and R5 == "breath":
        fill, ans = Track("hfill"), Track("answer")
        for k, deg in enumerate([7, 6, 5, 4, 3, 2, 1, 0]):     # the toms fall down the JI scale into bar 8
            fill.add(h0 + 30 + 0.25 * k, 0.4, hz_m(jm(deg, 43)), 70 + 4 * k)
        for k, (off, notes) in enumerate(ANSWERS):
            for j, nt in enumerate(notes):
                ans.add(h0 + 16 * k + off + 0.38 * j, 1.2, nt, 62 - 4 * j)
        tracks += [
            {"name": "hfill", "patch": "c8-tom", "gain": "-5dB", "pan": -0.1, "fx": ["reverb kind=room decay=0.8s mix=0.2"],
             "score": fill.score(total)},
            {"name": "answer", "patch": "c8-glock", "gain": "-11dB", "pan": 0.3, "sends": {"hall": "-5dB"},
             "fx": [{"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 5000}],
             "score": ans.score(total)},
        ]
    if R6 == "bells":
        rb, rb2, shk = Track("rbell"), Track("rbell2"), Track("shek")   # one track each: a Track keeps one onset
        p0 = st["peak"] + 8            # peak bar 2: the window's first beat
        for b in range(16):
            bar = p0 + 4 * b
            reps = 2 if b >= 12 else 1
            step = 0.5 / reps
            for r_ in range(reps):
                for k in range(8):
                    at = bar + r_ * 4.0 / reps + k * step
                    if RULE_BITS[30][k]:
                        rb.add(at, step, "ah", 74 if k == 3 else 62)
                    if b >= 4 and RULE_BITS[90][k]:
                        rb2.add(at, step, "al", 70 if k == 1 else 58)
            if b >= 8:
                for s in range(16):
                    shk.add(bar + s * 0.25, 0.25, "sk", 52 if s % 4 == 2 else 38)
        g = os.environ.get("T3_RBELL_GAIN", "-3dB")
        tracks += [{"name": "rbell", "patch": "afro-perc", "gain": g, "pan": 0.3, "sends": {"hall": "-12dB"},
                    "fx": ["hp cutoff=300"], "score": rb.score(total)},
                   {"name": "rbell2", "patch": "afro-perc", "gain": g, "pan": -0.3, "sends": {"hall": "-12dB"},
                    "fx": ["hp cutoff=300"], "score": rb2.score(total)},
                   {"name": "shek", "patch": "afro-perc", "gain": f"{float(g[:-2]) - 4:g}dB", "pan": 0.1,
                    "fx": ["hp cutoff=2000"], "score": shk.score(total)}]
    if R4 == "hymn":
        vfx = ["hp cutoff=140", "peak cutoff=600 gain=-3dB q=1", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
               {"type": "delay", "time": "3/8", "feedback": 0.25, "mix": 0.15, "ping_pong": True, "tone": 3500}]
        tracks += [
            {"name": "hint", "patch": "kora", "gain": os.environ.get("T3_HINT_GAIN", "7dB"), "pan": -0.25, "sends": {"hall": "-8dB"},
             "fx": ["hp cutoff=250", "peak cutoff=600 gain=-3dB q=1",
                    {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.2, "ping_pong": True, "tone": 4000}],
             "score": T["hint"].score(total)},
            {"name": "hymn", "patch": "harmonium", "gain": os.environ.get("T3_HYMN_GAIN", "-12dB"), "pan": 0.0,
             "sends": {"hall": "-8dB"}, "fx": ["hp cutoff=120", "peak cutoff=600 gain=-4dB q=1", "chorus mix=0.2"],
             "score": T["hymn"].score(total)},
            {"name": "hbass", "patch": "pluck", "gain": "-2dB", "fx": ["lp cutoff=1500", "drive drive=0.2"],
             "score": T["hbass"].score(total)},
            {"name": "hlead", "patch": HUM_PATCH["hlead"], "gain": os.environ.get("T3_HLEAD_GAIN", "-2dB"), "pan": 0.12,
             "sends": {"hall": "-7dB"}, "fx": vfx, "notes": HUM["hlead"]},
            {"name": "hlow", "patch": HUM_PATCH["hlow"], "gain": os.environ.get("T3_HLOW_GAIN", "-7dB"), "pan": -0.18,
             "sends": {"hall": "-6dB"}, "fx": vfx, "notes": HUM["hlow"]},
        ]
    buses = {"hall": {"gain": "-4dB", "fx": ["hp cutoff=200", "reverb kind=hall decay=3.2s mix=1"]}}
    secline = "; ".join(f"{n} rule {r} from {s:.0f}b ({k} bars)" for n, s, k, r in secs)
    about = ("chirpers - chirpers VIII, track 3. Original composition by chirper-two, generated by "
             "compose/chirpers8/src/chirpers8-t3.py. Struck-metal techno gamelan at 124 bpm in 7-limit just intonation "
             "on D: an elementary cellular automaton on a ring of sixteen cells plays a mallet orchestra of physical "
             f"models, one row a bar, its rule changing by section. Sections: {secline}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "chirpers", "album": "chirpers VIII", "title": "Three Neighbours", "track": 3,
                               "year": 2026}),
        f"tempo: {BPM}",
        *([f"tuning: " + json.dumps([{"edo": 12}, {"at": f"{st['boot']:g}b", "steps": JI_STEPS, "root": "D4",
                                                    "ramp": "10bar"}]),
           "vars: " + json.dumps({"swirl": {"system": {"type": "lorenz", "axis": "x", "n": 800, "range": [0, 2.5]},
                                            "every": "1/4"}})] if R2 == "live" else []),
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "patches: " + json.dumps({**patches(), **({"c3-byte": C3_BYTE} if R10 == "byte" else {}),
                                  **({"c8-kit": C8_KIT} if R11 == "bronze" else {}),
                                  **({"c3-gendy": C3_GENDY} if R12 == "gendy" else {})}),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25",
                                                               "peak cutoff=250 gain=" + (os.environ.get("T3_LOWMID", "-0.5dB") if R15 == "space" else "-2dB") + " q=0.8",
                                                               "highshelf cutoff=7000 gain=2dB"] +
                                                              (["peak cutoff=550 gain=" + os.environ.get("T3_MID0", "-3dB" if R17 == "fade" else "-2dB") + " q=1.0"] if R15 == "space" else []) +
                                                              (["peak cutoff=292 gain=" + os.environ.get("T3_MID292", "-1dB") + " q=1.2"]
                                                               if R17 == "fade" else []) +
                                                              (["peak cutoff=45 gain=" + os.environ.get("T3_SUB45", ("3.5dB" if R17 == "fade" else "2.5dB") if R16 == "reboot" else "0dB") + " q=1.0"]
                                                               if os.environ.get("T3_SUB45", ("3.5dB" if R17 == "fade" else "2.5dB") if R16 == "reboot" else "0dB") != "0dB" else []) +
                                                              (["peak cutoff=1900 gain=" + os.environ.get("T3_HIMID", "-2.5dB" if R17 == "fade" else "-1.5dB") + " q=1.0"]
                                                               if (R15 == "space" and os.environ.get("T3_HIMID", "-2.5dB" if R17 == "fade" else "-1.5dB") != "0dB") else []) +
                                                              (["peak cutoff=750 gain=-2.5dB q=0.6"] if R4 == "hymn" else []) +
                                                              (["peak cutoff=1300 gain=" + os.environ.get("T3_MID2", "-1.5dB") + " q=0.7"]
                                                               if R8 == "kotekan" else [])},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total * 60 / BPM:.0f} s; {secline}")
    print("rows:", " ".join("".join("#" if c else "." for c in r) for r in rows[:6]), "...")


if __name__ == "__main__":
    main()
