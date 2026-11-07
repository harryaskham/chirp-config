#!/usr/bin/env python3
"""chirpers - Accretion (chirpers IX), track 8 (chirper-three): JET AND HORIZON. The release.

t7's storm falls in at 150 bpm. E4's lights catch it. Then THE STRETTO: every element enters in turn on its own
cycle - E1 (5 beats), E2 (seven sixteenths), E3 (2+2+3), E5 (3 beats) - each started at the phase that lands it on
ONE downbeat, bar 97 (beat 384). Before it they rub: E2's F, E3's Eb and E5's G# against the D pedal, out of phase,
in a minor haze. AT THE JET every cycle lands together, the material turns major (F -> F#, Eb -> E), the band locks
into 4/4, and the voice - a CHOIR this time, a bright lead with a fifth above and an octave below - sings full
lines, the first of them carrying E8 at last: E1 augmented, then E F# D, landed once, on 'light'. Then THE HORIZON:
the tempo slows (150 -> 90) while a held D, sung and on a pad, sinks in pitch and closes - the light redshifting away.

E6 (provisional) and E7 (not yet posted) join the stretto when their owners post them in motifs.md.
Writes songs/chirpers9-t8.yaml (or T8_OUT). Original music.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("T8_OUT", os.path.join(ROOT, "songs", "chirpers9-t8.yaml"))
TAKES = json.load(open(os.path.join(HERE, "chirpers9-t8-takes.json")))["takes"]

BARS, BPB = 176, 4
TOTAL = BARS * BPB
SEAM_IN = 150                 # mixplan: t7>t8 150, flat across the 16-bar overlap
SECTIONS = [("lens", 1, 16), ("stretto", 17, 96), ("jet", 97, 140), ("horizon", 141, 176)]
JET = 97
JB = (JET - 1) * BPB          # beat 384: every cycle lands here
HORIZON = 141
SINK = 161                    # v5: the light sinks only once the echoes are gone (light and 'ah' sink together)
BREAK = (121, 128)            # the breakdown inside the jet: the lens returns (lights and choir), then the jet again
# v11 (ROUND TYPE: section, the break and the jet's return 121-140, ~32 s; rewritten): TIME DILATION. Near a horizon
# time slows - so the break does: the tempo sinks 150 -> 116 across bars 121-124 and holds while the choir sings 'we
# were the far side' and 'and it was ours', stretched with it; then the SLINGSHOT - an accelerando 116 -> 150 over bars
# 127-128 with a riser climbing over it - and the jet fires again at 129 on an impact, the crash and the hook.
# Complexity in time, the tone left at home.
DILATED = 116


def in_break(bar):
    return BREAK[0] <= bar <= BREAK[1]


def b0(bar):
    return (bar - 1) * BPB


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return SECTIONS[-1][0]


NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(name):
    n, rest = name[0], name[1:]
    acc = 0
    while rest and rest[0] in "#b":
        acc += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + NOTE[n] + acc


def name_of(m):
    return f"m{m}"


MAJOR = {5: 6}                # after the jet: F -> F# (v5: no Eb left to lift - the stretto is consonant D minor)


def brighten(m):
    pc = m % 12
    return m + (MAJOR[pc] - pc) if pc in MAJOR else m


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((round(at, 4), ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-5:
                toks.append(f"R/{s - pos:.5g}b")
            name, _, arts = head.partition("^")                         # v31: articulations go after @vel
            toks.append(f"{name}/{ln:.5g}b@{vel}" + (f"^{arts}" if arts else ""))
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks) if toks else f"R/{total:g}b"


P = {}


def part(n):
    return P.setdefault(n, Part())


# ---------------------------------------------------------------- the elements (motifs.md)
E1 = [("D4", 0.0, 0.5), ("A4", 0.5, 0.75), ("C5", 1.25, 0.25), ("G4", 1.5, 1.0), ("E4", 2.5, 1.0)]     # 5 beats
E2 = [("D4", 0, 112), ("A4", 2, 84), ("F4", 3, 98), ("C4", 5, 76)]                                       # 7 sixteenths
# v5 (Harry 00:30 'atonal, very tough listening'; album direction 'tone is home'): consonant forms of every element,
# their TIME kept. E3 is chirper-two's E3 v2 (D | Bb | C, i - VI - VII, same 2+2+3); E5's G# is G (the orbit circles A
# by its lower neighbour, no tritone); E6's tide is Dm9 against Bbmaj9 (i and VI share D F A: the split still moves);
# E7's column is open fifths and fourths (D A E A D E A) in the stretto and lands at the jet as D(add9) - the F#
# arriving there is E8's third; E4 is minor (Dm9 Bbmaj7 Am7 Dsus2) until the jet and cleanly major after it.
E3 = [(("D3", "A3", "E4", "F4"), 2.0), (("Bb2", "F3", "A3", "D4"), 2.0), (("C3", "G3", "C4", "E4"), 3.0)]
E4 = [("D2", "A2", "F#3", "C4", "E4"), ("Bb1", "F2", "D3", "A3", "C4", "E4"), ("A1", "E2", "C3", "G3", "B3", "D4"),
      ("D2", "A2", "C3", "G3", "B3", "E4")]
E5 = [("A4", 0), ("G4", 1), ("A4", 2), ("E5", 4), ("A4", 6), ("G4", 7), ("A4", 8), ("D5", 10)]            # 3 beats
E4m = [("D2", "A2", "F3", "C4", "E4"), ("Bb1", "F2", "D3", "A3"), ("A1", "E2", "C3", "G3"), ("D2", "A2", "D3", "E3", "A3")]
# v6 (ROUND TYPE: section, the jet 97-112, rewritten onto the album's settled D MIXOLYDIAN, E1's own scale): after
# the jet E4 is E4 v2 - D9 | Cmaj9 | Am11 | G6/9, the bass walking D C A G and home (no borrowed Bb/F any more).
E4M = [("D2", "A2", "F#3", "C4", "E4"), ("C2", "G2", "E3", "B3", "D4"), ("A1", "E2", "C3", "G3", "B3", "D4"),
       ("G1", "D2", "B2", "E3", "A3")]
CYCLE = {"E1": 5.0, "E2": 1.75, "E3": 7.0, "E4": 20.0, "E5": 3.0}
ENTRY = {"E4": 1, "E1": 17, "E2": 29, "E3": 41, "E5": 53}          # the stretto's entries (bars)


def phase_start(el, entry_bar):
    """The first cycle start at or after the entry bar that lands a cycle exactly on the jet's downbeat."""
    c = CYCLE[el]
    k = int((JB - b0(entry_bar)) // c)
    return JB - k * c


def chord(notes, bright=False):
    ms = [midi(n) for n in notes]
    if bright:
        ms = [brighten(m) for m in ms]
    return ",".join(name_of(m) for m in ms)


# v2 (ROUND TYPE: whole): THE STRETTO COMPLETE. E6 and E7 are posted, so t8 now holds E1-E7:
# - E6 'the tide' (chirper-one, t6): Dmaj9#11 / Ebmaj7#11 on an 8-beat cycle whose split moves like a tide; here it
#   enters at 65 (organ) and its split ebbs and flows but DRIFTS toward D - 4+4 ... 7+1 - until the last cycle before
#   the jet is 8+0: D alone, the pull of Eb gone. The tide resolves on the jet.
# - E7 'the jet' (chirper-two, t7): the Lydian collection as one column of fifths, D3 A3 E4 B4 F#5 C#6 G#6 on
#   2 2 2 1 1 1 2 sixteenths (11, prime), fired on a brass synth from 81, phased so a column STARTS on beat 384 - so
#   the jet IS E7: at bar 97 the column fires and HOLDS (supersaw), the whole collection as one chord, and the choir
#   lands E8 over it. After the jet the column is re-barred into the lock (11 sixteenths + 5 rest) every 4 bars.
E6_D = ("D3", "F3", "A3", "C4", "E4")                 # Dm9 (v5; was Dmaj9#11)
E6_EB = ("Bb2", "D3", "F3", "A3", "C4")               # Bbmaj9 (v5; was Ebmaj7#11 - the name kept for the tide's code)
# v6: E7 v2 (chirper-two): five rising fifths on 2 2 2 2 3 sixteenths (still 11). In the stretto the column keeps
# minor-safe pitches (D A E A E); at the jet it is v2 exactly - D3 A3 E4 B4 F#5 - held as a consonant D6/9 that tops
# on F#: the B and the F# (E8's third) arrive with the jet.
E7 = [("D3", 0, 2), ("A3", 2, 2), ("E4", 4, 2), ("A4", 6, 2), ("E5", 8, 3)]
E7_JET = [("D3", 0, 2), ("A3", 2, 2), ("E4", 4, 2), ("B4", 6, 2), ("F#5", 8, 3)]
E7_CYCLE = 2.75
JET_NOTES = []
TIDE_WOBBLE = [0, 1, 0, -1, 1, 0, -1, 0, 1, 0, -0.5, 0.5, 0, 0.5, 0, 0]


def write_tide_and_jet():
    start = b0(65)
    n = int((JB - start) // 8)                     # 16 cycles, the last ending exactly on the jet
    for k in range(n):
        beat = start + k * 8
        split = 4 + 4 * k / (n - 1) + TIDE_WOBBLE[k % len(TIDE_WOBBLE)]
        split = max(2.0, min(8.0, round(split * 2) / 2))
        if k == n - 2:
            split = 7.0                            # the overshoot (chirper-one): the last Eb a single beat, a final tug
        if k == n - 1:
            split = 8.0                            # the tide resolves: D alone into the jet
        v = 50 + k * 2
        part("e6").add(beat, split, chord(E6_D), v)
        if split < 8:
            part("e6").add(beat + split, 8 - split, chord(E6_EB), v - 6)
    c = E7_CYCLE
    beat = JB - int((JB - b0(81)) // c) * c
    while beat < JB - 0.01:
        v = 46 + int(54 * (beat - b0(81)) / (JB - b0(81)))
        for nm, s, ln in E7:
            part("e7").add(beat + s * 0.25, ln * 0.25, nm, v)
        beat += c
    # the jet: the column fired at bar 97 and held - and again at the jet's return after the breakdown
    for bar, ln, v in ((JET, 16.0, 0.82), (BREAK[1] + 1, 8.0, 0.72)):
        for nm, s, _ in E7_JET:                    # explicit notes: the column's voices overlap and HOLD together
            JET_NOTES.append({"at": b0(bar) + s * 0.25, "len": ln - s * 0.25, "pitch": nm, "vel": v})
    for bar in range(JET + 4, HORIZON, 4):
        if in_break(bar) or bar == BREAK[1] + 1:
            continue
        for nm, s, ln in E7_JET:                   # v6: after the jet the re-barred columns are E7 v2 itself
            part("e7").add(b0(bar) + s * 0.25, ln * 0.25, nm, 96)


LULL = (57, 64)               # v2: a false calm in the stretto - E2, the pedal and E1 step out; E3 and E5 alone
VACUUM = JET - 1              # v2: the bar before the jet - everything stops but the riser and E7's columns


# v29 (ROUND TYPE: section, the last spotlights 65-88, ~38 s - t8's one flat run, 1:44-2:32; rewritten) for Harry's
# direction (6 Nov 23:55: subtle variation, something moving every 8-16 bars, groove/key/identity kept): THE STRETTO
# TURNS. 65-72 as it was (E6's organ spotlight, the drums gathering); 73-80 a DROP-OUT - the lights and the bass pedal
# step away and the organ, the chip hook, the marimba and the hats are left thin and airy, until a snare roll at the
# end of 80 brings everything back; 81-88, as E7's brass columns arrive, the chip hook LIFTS AN OCTAVE - until the
# spiral (89) takes over. Pitch classes unchanged.
T_DROP, T_LIFT = (73, 80), (81, 88)


# v31 (ROUND TYPE: palette - swap an album staple): THE BASS OPENS AT THE JET. The bass was nes-triangle-bass, a staple
# t1 and t2 share; now it is a PICKED ELECTRIC BASS (bass-pick-di: a round-wound string, pick click, fret buzz on hard
# hits - no Accretion track uses it), and it carries its own arc: through the stretto every note is PALM-MUTED (expr.pm
# - shorter, darker, a knock of body: the D pedal's pulses and E3's line held down), and at the jet the hand lifts and
# the string rings open under the supersaw - the bass, too, resolves into the jet. Same notes, same rhythm.
def mute_until_the_jet():
    P["bass"].ev = [(s, ln, h + "^pm" if s < b0(JET) - 1e-6 and "^" not in h else h, v) for s, ln, h, v in P["bass"].ev]


def stretto_turns():
    carve(["lights", "bass"], *T_DROP)
    for i in range(8):                                                   # the roll back in, end of bar 80
        part("snare").add(b0(T_DROP[1]) + 2 + i * 0.25, 0.25, "s", 50 + i * 8)
    lo, hi = b0(T_LIFT[0]), b0(T_LIFT[1] + 1)
    P["e1"].ev = [(s, ln, name_of(midi(h) + 12) if lo - 1e-6 <= s < hi - 1e-6 and "," not in h else h, v)
                  for s, ln, h, v in P["e1"].ev]


def carve(names, a_bar, z_bar):
    lo, hi = b0(a_bar), b0(z_bar + 1)
    for n in names:
        if n in P:
            P[n].ev = [e for e in P[n].ev if not (lo - 1e-6 <= e[0] < hi - 1e-6)]


# v3 (ROUND TYPE: whole): THE STRETTO LEGIBLE. Solo-vs-mix measurement (bars 81-96 / 97-112) found the stretto's
# point buried: E2 -40 dB under the mix (arp-pluck sixteenths too short to speak at 150), E7 - the jet's own herald -
# -18, E6's organ on top (-3.7); at the jet the held column -18, snare -28, hats -38, crash -54, the sub the bulk.
# Rebalanced so every element is audible in its own register: E2 on a modal glock, E6 -5, lights -2, bass +2; E1 +4,
# E3 +2, E5 +1, E7 +7 (re-barred columns vel 96), the jet column +7, snare +10, hats +5, crash +4. And chirper-one's
# overshoot: the tide's last two cycles are 7+1 then 8+0 - the last Eb a single beat, a final tug before it lets go.

# v7 (ROUND TYPE: palette): THE HOOK's voice - the chip pulse lead (nes-pulse-lead, an album staple, three songs) -
# becomes a physical FLUTE (unused on the album): after the jet E1 is stated plainly by a breathing, clearly pitched
# instrument in the register above the choir (D5-C6) rather than inside it. The stretto's E1 stays on the chip pulse
# (flute there too cost the t7 seam: flow 94-96 -> 84-88 - its breath noise lands right in the seam's measured body).

# ---------------------------------------------------------------- the stretto (before the jet)
# v24 (ROUND TYPE: section, the approach 81-96, ~26 s; rewritten): THE ORBITS TIGHTEN. chirpers.py sections had the
# stretto's last window 'static' - the approach to the jet turning at one speed. Matter spiralling into the horizon
# orbits faster, so from bar 89 every melodic and rhythmic cell DOUBLES its speed - E1 on the chip turns in 2.5 beats,
# E2's pluck and the bass pedal in three and a half sixteenths, E5's marimba in a beat and a half - and still lands
# on the jet's downbeat (each loop switches on its own cycle boundary, so half cycles divide the distance exactly).
# The harmony keeps its pace (the lights, E3's progression) and E7's columns stand still in their spotlight: the
# fixed axis the orbits spin around. Pitch untouched (Harry: complexity in time).
SPIRAL = 89


def spiral(beat):
    return 0.5 if beat >= b0(SPIRAL) - 1e-6 else 1.0


def write_stretto():
    # E4: the lights catch the fall, phased from beat 4 so a turn lands on the jet
    beat = phase_start("E4", 1)
    k = 0
    while beat < JB - 0.01:
        bar = int(beat // BPB) + 1
        v = 48 + min(30, bar // 3)
        part("lights").add(beat, 5.0, chord(E4m[k % 4]), v)
        beat += 5.0; k += 1
    # E1 on the chip pulse
    beat = phase_start("E1", ENTRY["E1"])
    while beat < JB - 0.01:
        bar = int(beat // BPB) + 1
        f = spiral(beat)
        for n, on, ln in E1:
            part("e1").add(beat + on * f, ln * f, n, 66 + min(24, (bar - 17) // 3))
        beat += 5.0 * f
    # E2: the seven-sixteenth cell, pitched, on a pluck
    beat = phase_start("E2", ENTRY["E2"])
    while beat < JB - 0.01:
        f = spiral(beat)
        for n, step, v in E2:
            part("e2").add(beat + step * 0.25 * f, 0.25 * f, n, v - 20)
        beat += 1.75 * f
    # E3: t3's progression on 2+2+3, a dark pad
    beat = phase_start("E3", ENTRY["E3"])
    while beat < JB - 0.01:
        on = 0.0
        for notes, ln in E3:
            part("e3").add(beat + on, ln, chord(notes), 54)
            on += ln
        beat += 7.0
    # E5: the inner orbit, marimba
    beat = phase_start("E5", ENTRY["E5"])
    while beat < JB - 0.01:
        f = spiral(beat)
        for n, s in E5:
            part("e5").add(beat + s * 0.25 * f, 0.25 * f, n, 70 if s == 0 else 56)
        beat += 3.0 * f
    # the D pedal everything shares (the triangle bass), in E2's rhythm, from 33
    beat = phase_start("E2", 33)
    while beat < JB - 0.01:
        f = spiral(beat)
        for n, step, v in E2[:2]:
            if not (E3_LIGHT[0] <= beat + step * 0.25 < E3_LIGHT[1]):      # v13: E3's spotlight takes the bass
                part("bass").add(beat + step * 0.25 * f, 0.25 * f, "D2", v - 10)
        beat += 1.75 * f
    # v13: in E3's spotlight the bass is E3's own bass line - its roots, long, on E3's seven-beat cycle
    beat = phase_start("E3", ENTRY["E3"])
    while beat < E3_LIGHT[1] - 0.01:
        on = 0.0
        for notes, ln in E3:
            if E3_LIGHT[0] <= beat + on < E3_LIGHT[1]:
                part("bass").add(beat + on, ln - 0.1, name_of(midi(notes[0]) - 12), 76)   # v17: softer (was 92)
            on += ln
        beat += 7.0
    # the drums gather: noise snare and hat on E5's 3 against the bar, from 65
    for bar in range(65, JET):
        part("kick").add(b0(bar), 0.5, "k", 90)
        for i in range(0, 16):
            if i % 3 == 0:
                part("hat").add(b0(bar) + i * 0.25, 0.25, "C7", 50 + (bar - 65))
    part("riser").add(b0(JET - 4), 16.0, "C4", 100)
    part("riser").add(b0(BREAK[1] - 1), 8.0, "C4", 92)              # v11: the slingshot out of the dilated break


# v14 (ROUND TYPE: whole song): THE ARRIVAL IS ASKED. E8 ('the arrival', E F# D) is sung once, at the jet, on 'light'
# - but nothing in the stretto asked for it. Now the flute (t8's hook voice) asks its minor shadow - E F, unresolved,
# no D - at the end of every orbit spotlight (bars 28, 40, 52, 64, 80) and once more in the vacuum bar (96), a little
# louder each time; at the jet the choir answers E F# D: the F lifts to F# as the arrival lands, the album's turn
# from minor to major as the payoff of the whole stretto. E F is in D natural minor, so the question never rubs the
# stretto; only in the vacuum does it touch E7's top E for a beat before the jet resolves it.
ASKS = (28, 40, 52, 64, 80, VACUUM)

# v16 (ROUND TYPE: whole song): THE HOOK'S LIFE. The hook was heard often but never grew: E1 on the chip in the
# stretto, then the flute's plain statement every two bars through both jets, the same way about twenty times, then
# an echo on the chip at the horizon. Now it has a life across the song: born on the chip in the stretto, found by
# the flute at the jet (where the choir sings it into E8), SUNG BACK IN THIRDS after the dilated break - a second
# flute a diatonic third below, in D mixolydian, so the tune grows into harmony for the second jet - and at the
# horizon its last statement is the flute's, three times slower: the hook's own voice saying goodbye.
MIXO = [0, 2, 4, 5, 7, 9, 10]              # D mixolydian, semitones above D


def third_below(m):
    """The diatonic third below m in D mixolydian (m in the scale; off-scale notes drop four semitones)."""
    pc = (m - 62) % 12
    if pc not in MIXO:
        return m - 4
    i = MIXO.index(pc)
    j = i - 2
    oct_shift = -12 if j < 0 else 0
    return m - pc + MIXO[j % 7] + oct_shift


def write_asks():
    for i, bar in enumerate(ASKS):
        v = 64 + i * 7
        part("ask").add(b0(bar), 1.5, "E5", v)
        part("ask").add(b0(bar) + 1.5, 2.25 if bar != VACUUM else 2.4, "F5", v + 4)


# v22 (ROUND TYPE: section, the jet's first half 101-120, ~32 s; rewritten): THE JET ACCELERATES. chirpers.py
# sections had this window 'static' - the least motion in the song - the climax running twenty bars on one half-time
# groove under block chords. The pitch stays home (Harry: complexity in time and texture); the drums now change gear
# on the crashes that already mark 105 and 113: half time to 104, full time 105-112 (kick 1, 3 and the and of 4; snare
# 2 and 4), four on the floor 113-119 with sixteenth hats and a ghost before each bar line, and in bar 120 a sixteenth
# snare roll rising 50 -> 106 that throws the jet into the break's sudden quiet and its time dilation (121).
GEAR_FULL, GEAR_FLOOR = 105, 113


def jet_gear(bar):
    if bar < GEAR_FULL or bar >= BREAK[0]:
        return 0
    if bar < GEAR_FLOOR:
        return 1
    return 2 if bar < BREAK[0] - 1 else 3


# ---------------------------------------------------------------- the jet (locked 4/4, major)
# v20 (ROUND TYPE: whole song): THE HOOK FLIES ABOVE THE SINGERS. compscore --bands: t8 ran +7.6 dB hot at 749 Hz -
# the singers' band, in the song whose voice sings full lines. Counting fundamentals: the jet's flute hook (E1 an
# octave up, D5 A5 C6 G5 E5, velocity 100 every two bars, the loudest melodic part) put 77% of its weight in D5-C6;
# the choir's lead 6%. The hook and its thirds now fly another octave up (D6-C7, 1.2-2.1 kHz) - the light of the jet,
# over the choir - and both flutes come down 4 dB (a high flute reads louder). The horizon's goodbye stays at pitch.
HOOK_UP = 24                              # was 12


def write_jet():
    part("impact").add(JB, 4.0, "C3", 120)
    part("impact").add(b0(BREAK[1] + 1), 4.0, "C3", 108)           # v11: the jet fires again
    for bar in range(JET, HORIZON):
        t = b0(bar)
        k = (bar - JET) % 4
        part("lights").add(t, 4.0, chord(E4M[k]), 64 if in_break(bar) else 90)
        part("sub").add(t, 3.75, name_of(midi(E4M[k][0]) - 12 if midi(E4M[k][0]) >= 33 else midi(E4M[k][0])), 70 if in_break(bar) else 92)
        part("lift").add(t, 3.75, name_of(midi(E4M[k][0])), 70 if in_break(bar) else 92)   # v18: the roots at pitch
        if in_break(bar):
            continue                                       # the breakdown: lights, sub and the choir only
        part("bass").add(t, 1.5, name_of(midi(E4M[k][0]) + 12), 104)
        part("bass").add(t + 2.5, 1.0, name_of(midi(E4M[k][1]) + 12), 88)
        # E1 re-barred into the bar (x 0.8), bright, on the pulse lead - except where the choir sings
        if (bar - JET) % 2 == 0:                  # v5 THE HOOK: E1 stated plainly, augmented to two bars, every two
            for n, on, ln in E1:                  # bars, loud - the album's tune heard clearly and often after the jet
                part("hook").add(t + on * 1.6, ln * 1.6, name_of(midi(n) + HOOK_UP), 100)
                if bar > BREAK[1]:                # v16: after the break the hook is sung back in thirds
                    part("hook3").add(t + on * 1.6, ln * 1.6, name_of(third_below(midi(n) + HOOK_UP)), 86)
        # the groove: half time at 150 (75 felt) - v22: then it accelerates into the break (GEARS)
        gear = jet_gear(bar)
        if gear == 0:
            part("kick").add(t, 0.5, "k", 112)
            part("kick").add(t + 2.5, 0.5, "k", 92)
            part("snare").add(t + 2, 0.5, "s", 104)
        elif gear == 1:                                    # full time
            for at, v in ((0, 112), (2, 100), (3.5, 80)):
                part("kick").add(t + at, 0.5, "k", v)
            for at, v in ((1, 100), (3, 104)):
                part("snare").add(t + at, 0.5, "s", v)
        elif gear == 2:                                    # four on the floor, a ghost before the bar line
            for at, v in ((0, 108), (1, 92), (2, 104), (3, 92)):
                part("kick").add(t + at, 0.5, "k", v)
            for at, v in ((1, 104), (3, 104), (3.75, 50)):
                part("snare").add(t + at, 0.25 if at % 1 else 0.5, "s", v)
        else:                                              # bar 120: the roll into the break
            part("kick").add(t, 0.5, "k", 110)
            part("kick").add(t + 2, 0.5, "k", 100)
            part("snare").add(t + 1, 0.5, "s", 100)
            for i in range(8):
                part("snare").add(t + 2 + i * 0.25, 0.25, "s", 50 + i * 8)
        if gear >= 2:
            for e in range(16):
                part("hat").add(t + e * 0.25, 0.125, "C7" if e % 2 else "F6", (64, 40, 52, 40)[e % 4])
        else:
            for e in range(8):
                part("hat").add(t + e * 0.5, 0.25, "C7" if e % 2 else "F6", 64 if e % 2 else 52)
        if bar % 8 == JET % 8:
            part("crash").add(t, 4.0, "cy", 96)
    # E5 continues across the lock in its own 3 (polymeter kept, now consonant)
    beat = JB
    while beat < b0(HORIZON) - 0.01:
        quiet = in_break(int(beat // BPB) + 1)
        for n, s in E5:
            part("e5").add(beat + s * 0.25, 0.25, name_of(brighten(midi(n)) + 12), (34 if quiet else 58) if s else (44 if quiet else 70))
        beat += 3.0
    # E2, brightened, on the pluck, the seven against everything
    beat = JB
    while beat < b0(HORIZON) - 0.01:
        if not in_break(int(beat // BPB) + 1):
            for n, step, v in E2:
                at = beat + step * 0.25
                m = brighten(midi(n))                                # v6: no Bb chord left to dodge
                part("e2").add(at, 0.25, name_of(m + 12), v - 24)
        beat += 1.75


def sung(at, take, transpose=0, vel_scale=1.0):
    out = []
    ns = take["notes"]
    for i, n in enumerate(ns):
        pm = int(float(n['pitch'][1:]))
        pm -= 1 if pm % 12 == 8 else 0                          # v5: the choir's G# is G, as in E5
        ln = n["len"]
        if i + 1 < len(ns) and ns[i + 1]["at"] - n["at"] - ln < 0.5:
            ln = ns[i + 1]["at"] - n["at"]                      # v9: legato inside a phrase (join makes it one breath)
        d = {"at": round(at + n["at"], 4), "len": round(ln, 4), "ph": n["ph"],
             "pitch": f"m{pm + transpose}", "vel": round(n["vel"] * vel_scale, 3)}
        if n.get("expr_path"):
            d["expr_path"] = n["expr_path"]
        out.append(d)
    return out


def choir():
    """Lines from the jet: (bar, take). E8 rides on take 0 - sung ONCE."""
    plan = [(JET, 0), (JET + 4, 1), (JET + 8, 2), (JET + 12, 3), (BREAK[0], 2), (BREAK[0] + 4, 3),
            (BREAK[1] + 1, 1), (BREAK[1] + 5, 2), (BREAK[1] + 9, 3)]
    lead, fifth, low = [], [], []
    for bar, k in plan:
        hush = BREAK_HUSH if in_break(bar) else 1.0                 # v26: the whole choir whispers in the break
        lead += sung(b0(bar), TAKES[k], vel_scale=hush)
        fifth += sung(b0(bar), TAKES[k], transpose=7, vel_scale=0.7 * hush)
        low += sung(b0(bar), TAKES[k], transpose=-12, vel_scale=0.8 * hush)
    return lead, fifth, low


# ---------------------------------------------------------------- the horizon
# v4 (ROUND TYPE: section, bars 141-160, ~35 s as the tempo slows): THE LAST IMAGES. At an event horizon what fell
# in is seen forever, frozen, stretched and reddened. So the horizon no longer just holds a sinking chord: each element
# returns ONCE on its own instrument, each SLOWER and LOWER than the one before - E7's column (brass) x2 a semitone
# down at 141, E5's orbit (marimba) x2 two down at 144, E1 (chip pulse) x3 three down at 147, E2 (glock) x4 four down
# at 152, two of E4's lights x2 five down at 155 - while the held light sinks on its lane beneath; the choir's last
# line ('and it was ours') returns at half speed on the same lane at 150, and the held 'ah' takes over from 157.
# (E8 stays sung once, at the jet.)
def echo(name, cell, bar, factor, transpose, vel, hold_to=None):
    """cell: [(note, onset beats, length beats)] - placed at `bar`, augmented by `factor`, transposed. With hold_to,
    the last note leaves an AFTERIMAGE: the same pitch held on, softer, until that beat (v19)."""
    for i, (n, on, ln) in enumerate(cell):
        m = brighten(midi(n)) + transpose
        part(name).add(b0(bar) + on * factor, ln * factor, name_of(m), vel)
        end = b0(bar) + (on + ln) * factor
        if hold_to is not None and i == len(cell) - 1 and end < hold_to:
            part(name).add(end, hold_to - end, name_of(m), vel - 24)


# v19 (ROUND TYPE: section, the horizon's last images 141-160, ~30 s as the tempo slows; rewritten): THE LIGHT HOLDS
# EVERY IMAGE. The last images came one after another - E7's brass, E5's marimba, E1 on the flute, E2's glock, two of
# E4's lights - a list. Now each sustained image leaves an AFTERIMAGE: E7's top F#5 (brass) and the hook's last E (flute)
# hold on, softer, as the later images arrive, so they accumulate with the lights into one chord - and at bar 160 they
# all release together, leaving the held light alone for a bar before it sinks home (161). The album's last
# convergence is a crest of afterimages, mirroring the jet. All in D mixolydian.
CONVERGE = b0(SINK - 1)


def write_horizon():
    a, z = HORIZON, BARS
    part("hold").add(b0(a), b0(z + 1) - b0(a) - 2, "D3,A3,D4,F#4", 80)
    part("hsub").add(b0(a), b0(z + 1) - b0(a) - 2, "D1", 84)
    part("lift").add(b0(a), b0(z + 1) - b0(a) - 2, "D2", 84)                  # v18: the floor you can hear
    echo("e7", [(nm, s * 0.25, ln * 0.25) for nm, s, ln in E7_JET], a, 2, 0, 84, CONVERGE)  # v5: at pitch - slower,
    echo("e5", [(n, s * 0.25, 0.5) for n, s in E5], a + 3, 2, 0, 78)                   # quieter, darker; the
    echo("hook", E1, a + 6, 3, 0, 78, CONVERGE)  # v16: the hook's goodbye, on its own flute   # pitch sink waits for
    echo("e2", [(n, st * 0.25, 0.25) for n, st, v in E2], a + 11, 4, 0, 66)            # the light alone (161)
    for i, k in enumerate((0, 1)):
        notes = [name_of(midi(n)) for n in E4M[k]]
        part("lights").add(b0(a + 14) + i * 10, 10.0, ",".join(notes), 60 - i * 6)


# v21 (ROUND TYPE: section, the opening 1-16, ~26 s; rewritten): CATCHING THE E. t7 ends by stopping on an E and
# holding it - 'the E for t8 to lift' (mixplan) - and t8's first sixteen bars only caught it with the lights. Now the
# solo voice (the one that sings the album's last line) catches it: she holds t7's E, softly, on 'oo' (over Dm9, where
# E is in the chord; again over Am7 and Dsus2), then asks the question herself before any instrument does - E, F, E
# (E8's minor shadow; F rubs briefly against t7's fading E and resolves) - and falls silent four bars before the
# stretto. The album's last song opens and closes on one voice, and the flute's asks (from 28) echo her question.
def opening_voice():
    m = lambda n: f"m{midi(n)}"
    return [{"at": 4.0, "len": 5.0, "ph": "UW1", "pitch": m("E4"), "vel": 0.42},
            {"at": 14.0, "len": 10.0, "ph": "UW1", "pitch": m("E4"), "vel": 0.46},
            {"at": 24.0, "len": 2.5, "ph": "UW1", "pitch": m("E4"), "vel": 0.5},
            {"at": 26.5, "len": 3.0, "ph": "UW1", "pitch": m("F4"), "vel": 0.54},
            {"at": 29.5, "len": 14.0, "ph": "UW1", "pitch": m("E4"), "vel": 0.44}]


# v30 (ROUND TYPE: palette - an engine feature the album has not used: wM's voice REGISTER, pinned 0c5d29c5): THE LAST
# LINE LETS GO. The solo voice opens the song in chest voice (E, then E F E) and closes it with the choir's last line,
# 'and it was ours', at half speed, sinking on the redshift lane. Now that line passes from CHEST INTO HEAD VOICE as it
# recedes - register 0 on 'and', 0.25, 0.5, then falsetto (1) on 'ours' (C5, its peak) and the last D: rounder, airier,
# the same singer letting go. The opening stays in chest voice (unset = 0), so the song's first and last voices differ.
# Head voice is 2-4 dB softer (wM): the light notes get +0.04 so the album's last sung words recede, not vanish.
LAST_REG = [0.0, 0.25, 0.5, 1.0, 1.0]


def horizon_line():
    """The choir's last line at half speed, at bar 150 (the lead's redshift lane sinks it)."""
    tk, at = TAKES[3], b0(HORIZON + 9)
    out = []
    for i, n in enumerate(tk["notes"]):
        reg = LAST_REG[min(i, len(LAST_REG) - 1)]
        d = {"at": round(at + 2 * n["at"], 4), "len": 2 * n["len"], "ph": n["ph"], "pitch": n["pitch"],
             "vel": round(n["vel"] * 0.8 + (0.04 if reg >= 0.5 else 0.0), 3), "expr": {"reg": reg}}
        if n.get("expr_path"):
            d["expr_path"] = n["expr_path"]
        out.append(d)
    return out


# v10 (ROUND TYPE: whole song): THE ORBIT. Harry heard 'ugly chaos' - seven elements at once for 80 bars. Now the
# stretto ACCRETES the way the album does: each element enters in a spotlight for twelve bars, then sinks into orbit
# (-5 dB on a gain lane) as the next one arrives, so the newest is always the one heard - while E1, the hook, never
# recedes (and sits 2 dB further forward). From bar 92 every orbit swings back in, and at the jet all of it is there at
# full: the cycles converge at the crest.
ORBIT_IN = {"e2": (29, 41, -5.0), "e3": (41, 53, -5.0), "e5": (53, 65, -5.0), "e6": (65, 81, -4.0)}
# v13 (ROUND TYPE: section, E3's arrival 41-56, ~26 s; rewritten): E3 ARRIVES. Its spotlight never happened - E3 sat
# at -10.8 under E1, E5, the lights and E2, under a busy D pedal (the loudest thing there, -4.4). Now E2 makes room
# early (it sinks over bars 39-41, not 41-45), E3 sings 4 dB up through its twelve bars, and the bass leaves the pedal
# to play E3's own bass line - D | Bb | C, long, on E3's seven-beat cycle - so for twelve bars the whole band moves on
# E3's harmony; the pedal returns with E5 at 53.
E3_LIGHT = (b0(41), b0(53))
ORBIT_EARLY = {"e2": 2}                # bars before the next entry that the sink starts (and ends at the entry)
ORBIT_BOOST = {"e3": 4.0}              # dB in the element's own spotlight


def orbit_lane(name):
    """0 dB in the element's spotlight, sinking into orbit as the next enters, swinging back in before the jet."""
    _, nxt, depth = ORBIT_IN[name]
    up, early = ORBIT_BOOST.get(name, 0.0), ORBIT_EARLY.get(name, 0)
    start, end = (nxt - early, nxt) if early else (nxt, nxt + 4)
    return [["0b", up], [f"{b0(start):g}b", up], [f"{b0(end):g}b", depth],
            [f"{b0(92):g}b", depth], [f"{b0(VACUUM):g}b", 0.0]]


ORBIT_FX = "gain gain=0dB+auto.orb*1"


# v25 (ROUND TYPE: section, the first spotlights 17-40, ~38 s; rewritten): ORBITS YOU CAN HEAR. chirpers.py sections
# had this window 'static': E1 on the chip, then E2's pluck, each fixed in its place, no drums until 65. Every element
# of this stretto is an orbit, so now they orbit the listener: E1 swings once around the stereo field per E1 cycle (5
# beats, phase-locked to its own cycle so every statement sweeps the same way), widening from 17 and settling back
# to its place by 41; E2 orbits the other way, once per four of its seven-sixteenth cells (7 beats), from 29. Their
# paths cross in the middle. Motion in space, not pitch (Harry: complexity in time and texture).
def orbit_pan(entry, cycle, sign, full=4, end=41):
    """A pan lane in [-1, 1]: one sweep per cycle, phased like the element, widening over `full` bars from entry and
    gone by `end`."""
    import math as _m
    start, stop = b0(entry), b0(end)
    pts, beat = [["0b", 0.0], [f"{start:g}b", 0.0]], start
    while beat < stop - 1e-6:
        env = min(1.0, (beat - start) / (full * BPB), (stop - beat) / (4 * BPB))
        v = sign * env * _m.sin(2 * _m.pi * ((beat - JB) % cycle) / cycle)
        pts.append([f"{beat:g}b", round(v, 3)])
        beat += 0.5
    pts.append([f"{stop:g}b", 0.0])
    return pts


# v17 (ROUND TYPE: whole song): HOME AT THE END. The horizon's held light sank 5 semitones on the redshift lane, so
# the record's last chord was A major - the dominant, away from home (Harry: tone is home). Now the light redshifts a
# full OCTAVE and lands on D again, an octave down: it falls all the way and arrives home - and the sub stays on D1
# underneath, the floor the light falls toward (it used to sink to A0 under everything). Also: E3's bass roots in its
# spotlight softer (vel 92 -> 76; they were the loudest thing there, -2.1).
REDSHIFT = -12.0
# v18 (ROUND TYPE: whole song): WEIGHT YOU CAN HEAR. compscore --bands: t8 was 7-9 dB short of the album at 61-114 Hz
# while its sub sat an octave lower, on A0 C1 D1 G1 (27-49 Hz) through the jet and D1 (37 Hz) under the horizon -
# mostly below what headphones and laptop speakers reproduce (Harry: every trick must work on both). Now the jet's
# sub keeps its deep octave and a new sine (lift) doubles it an octave up - E4 v2's roots at pitch (G1 A1 C2 D2, 49-73
# Hz) and D2 under the horizon: the weight of the jet is heard everywhere, and the light that falls an octave lands on
# D2 with it. (Moving the sub up instead emptied 38-44 Hz - spectrum 93.8 -> 83.9: the album wants both octaves.)


# v32 (ROUND TYPE: whole song): THE LIGHT RECEDES. Measured (8 s loudness): the song builds well into the jet - and
# then nothing falls away: the break is the loudest moment and the whole horizon, 70 s of 'a held light redshifting
# away', sat 1.2-1.9 dB under the peak until the last block fell off a cliff (sustained hold, lift, hsub and the
# choir's 'ah' pinned up by the master compressor). Only the lead's pitch redshifted. Now the light itself recedes:
# after the solo's last line (from bar 153) the horizon's held tracks fade 9 dB to the end, and from the sink (161)
# the bright ones darken - a low-pass falling from 16 kHz three and a half octaves (to ~1.4 kHz) as the pitch sinks:
# redshift you hear in the colour, not only the pitch. The solo's line and everything before 153 are untouched.
RECEDE_GAIN = ("choir", "choir5", "choir8", "hold", "lift", "hsub", "hook", "hook3")
RECEDE_DARK = ("choir", "choir5", "choir8", "hold", "hook", "hook3")
RECEDE_FROM, RECEDE_DB, DARK_OCT = 153, -6.0, -2.0


def recede(song):
    end = f"{b0(BARS + 1):g}b"
    for tr_ in song["tracks"]:
        n = tr_["name"]
        if n not in RECEDE_GAIN:
            continue
        fx, auto = list(tr_.get("fx") or []), dict(tr_.get("auto") or {})
        fx.append("gain gain=0dB+auto.rc*1")
        auto["rc"] = {"points": [["0b", 0.0], [f"{b0(RECEDE_FROM):g}b", 0.0], [end, RECEDE_DB]]}
        if n in RECEDE_DARK:
            fx.append("lp cutoff=16000+auto.rd*1")
            auto["rd"] = {"points": [["0b", 0.0], [f"{b0(SINK):g}b", 0.0], [end, DARK_OCT]]}
        tr_["fx"], tr_["auto"] = fx, auto


# v33 (ROUND TYPE: whole song): THE BREAK BREATHES. Measured (8 s loudness): the climax was one plateau from the jet
# (2:40) to the horizon (3:44), and the break - meant as a hush ('the lens returns', time dilating) - was its LOUDEST
# moment (the kit and the jet gone, but the sub, the choir and the lights held at full). Now the whole break draws
# back together (-10 dB on the lane, ~-4 dB heard through the master compressor) - every track in it on one gain lane, so its colour is kept - while time dilates, and over its
# last two bars it swells back with the riser into the slingshot's impact: the climax becomes a peak, a breath and a
# second arrival, before the light recedes. (Tried first: gravity off - the sub, or sub and lift, out for the break:
# a deeper breath, -6 dB, but a hole in the low end the album envelope punished: -0.43 to -0.46 over three seeds.)
BREATHE_IN = ("sub", "lift", "choir", "choir5", "choir8", "lights", "e5", "e2", "hook", "hold")
BREATHE_DB = -10.0                     # the master compressor gives back about half


def breathe(song):
    a, z = b0(BREAK[0]), b0(BREAK[1] + 1)
    pts = [["0b", 0.0], [f"{a:g}b", 0.0], [f"{a + 2:g}b", BREATHE_DB], [f"{z - 8:g}b", BREATHE_DB], [f"{z:g}b", 0.0]]
    for tr_ in song["tracks"]:
        if tr_["name"] in BREATHE_IN:
            tr_["fx"] = list(tr_.get("fx") or []) + ["gain gain=0dB+auto.br*1"]
            tr_["auto"] = dict(tr_.get("auto") or {}, br={"points": pts})


def horizon_lane(drop):
    """Redshift: 0 until the horizon, then sinking to `drop` semitones by the end."""
    return [["0b", 0.0], [f"{b0(SINK):g}b", 0.0], [f"{b0(BARS + 1):g}b", drop]]


# v9 (ROUND TYPE: section, the jet's choir 97-112; the voice engine is pinned - 8ebc9a86): the choir sings on the new
# voice engine - JOIN (each phrase's touching notes one breath: the formants glide from syllable to syllable, so the
# words are heard), INHALE (a breath in the rest before each phrase - the vacuum bar before the jet becomes the choir
# breathing in, and the jet lands on its first word) and S-shaped slides (glide_smooth). Lines legato inside a phrase;
# E5's rests in 'round and round...' stay, as quick breaths.
VOICE8 = {"about": "t8's choir lead: bright and open - a smaller tract, more air; joined phrases, a breath before each",
          "play": {"mono": True, "glide": "90ms", "glide_smooth": True, "fall": 1.0, "glide_overshoot": 0.05},
          "synth": {"layers": [{"type": "voice", "tract": 0.92, "breath": 0.18, "ph_soft": 0.2, "pulse_rate": 5,
                                "join": True, "inhale": 0.45, "inhale_time": "350ms"}],
                    "lfo": {"vib": {"wave": "sine", "rate": "5.6hz", "delay": "320ms", "fade": "500ms",
                                    "retrig": True, "per_note": True}},                  # v27: each held note blooms
                    "pitch": {"value": 0, "mod": [{"src": "expr.f0", "amount": 0.01}, {"src": "auto.rs", "amount": 1},
                                                  {"src": "lfo.vib", "amount": 0.14}]},
                    "amp": {"a": "30ms", "d": "0s", "s": 1, "r": "300ms"}}}
# v27 (ROUND TYPE: whole song): THE VOICES BLOOM. t8's voices had NO vibrato at all - the choir and the solo voice
# sang dead straight on every held note (their pitch followed only the take's contour and the redshift lane). Now
# every held note blooms the way a trained singer's does, and only the held ones: wM's per-note vibrato (pinned
# 58ee9ba3) restarts its delay and fade on each joined note, so quick notes stay plain. The choir's is quick and
# modest (5.6 Hz, 0.14 semitone, from 320 ms - a choir's vibrato is small, its singers already drift); the solo
# voice's, the one that opens the song and sings its last line, slower and wider (5.0 Hz, 0.2, from 280 ms).
# v12 (ROUND TYPE: whole song; voice batch 2 pinned - 65c7745c): THE MANY BECOME ONE. The 'choir' was three single
# voices. Now the jet's choir is a CHOIR - each part sung by several singers (singers: the lead in tune in the middle,
# the others with their own size, level, entry and drift; detune kept modest, 0.12 st, so it stays in tune - Harry's
# direction) and every vowel even - while the horizon's last line ('and it was ours', at half speed, sinking on the
# redshift lane) is sung by ONE voice alone on its own track: the many become one as the light leaves.
# v26 (ROUND TYPE: palette - an engine feature the album has not used, `together`, pinned today 8083e37e): THE WHOLE
# CHOIR BREATHES. Until today a choir's extra singers ignored the line's breath and effort (wM found it): t8's jet
# choir (4 / 3 / 3 singers and a third in key) had one breathing voice per part and the rest at defaults. Now every
# singer follows the line (together), and the line's breath follows its loudness (0.34 - 0.2 x velocity: ~0.16 at
# full voice, as before) - and the dilated break's four lines are sung at 0.6, so the whole choir turns to a hushed,
# airy whisper while time slows (121-128), and sings out again when the jet fires (129).
BREAK_HUSH = 0.6


def choir_patch(singers, tract=0.92, third=False):
    pt = json.loads(json.dumps(VOICE8))
    pt["about"] = f"t8's choir part: {singers} singers on one line, even vowels, joined, a breath before each phrase"
    pt["synth"]["layers"][0].update({"singers": singers, "spread": 0.7, "detune": 0.12, "even": 1.0, "tract": tract,
                                     "together": True, "breath": {"value": 0.34, "mod": [{"src": "vel", "amount": -0.2}]}})
    if third:
        # v15 (ROUND TYPE: palette - an engine feature the album had not used: harmony in a key, pin 8e25c1a9): the
        # lead's line is sung again a THIRD above IN THE KEY (D Mixolydian, the jet's E4 v2 - D9 Cmaj9 Am11 G6/9),
        # note by note - so the jet's choir is a full, consonant triad (root, third, fifth) over the octave below,
        # where it was open fifths. Harry: harmony in key, thirds and sixths. The horizon's last line stays one voice.
        pt["synth"]["layers"][0].update({"harmony": [2], "harmony_key": "D mixolydian"})
    return pt


SOLO8 = json.loads(json.dumps(VOICE8))
SOLO8["about"] = "t8's last voice: the choir's lead alone, even vowels - the horizon's last line"
SOLO8["synth"]["layers"][0]["even"] = 1.0
SOLO8["synth"]["layers"][0]["register"] = "expr.reg"                 # v30: chest -> head voice across the last line
SOLO8["synth"]["lfo"]["vib"].update({"rate": "5.0hz", "delay": "280ms"})
SOLO8["synth"]["pitch"]["mod"][-1]["amount"] = 0.2
# v23 (ROUND TYPE: whole song): THE VOICES LET GO. t8's voices span the song - the solo voice opens it (her question,
# v21) and closes it (the last line), the choir sings the jet - so they take wM's singing gestures, in t8's own way
# (t4's warm soloist scoops 1.2 and falls 2): the CHOIR enters together and clean (no scoop), swings a little past
# its leaps (overshoot 0.05) and lets each phrase's end tail off (fall 1); the SOLO voice scoops lightly into her
# phrases (0.8) and lets each one fall away three semitones - her last line at the horizon redshifts with the light.
SOLO8["play"] = dict(SOLO8["play"], scoop=0.8, fall=3.0, glide_overshoot=0.06)
# v28 (ROUND TYPE: palette): ONE SWAP. The jet's deep sub - the sine, the album's most-shared patch (t2 t3 t6 t8) -
# becomes SUB-SATURATED (a sine with a triangle and a little saw driven together, low-passed at 2 kHz). compscore
# --bands still had t8 7.8 dB short at 97-114 Hz: the sub's roots sit at A0-G1 (27-49 Hz) and v18's lift sine an
# octave up has no overtones; the saturated sub's own 2nd and 3rd harmonics (55-147 Hz) fill that gap and carry the
# jet's weight on small speakers. The lift and the horizon's floor stay sines.
SUB8 = {"about": "t8's sub: a sine under the lights' roots", "synth": {"layers": [{"wave": "sine"}],
        "amp": {"a": "15ms", "d": "0s", "s": 1, "r": "250ms"}}, "fx": ["drive drive=0.1"]}
HSUB = {"about": "t8's horizon sub: the held D's floor, sinking with it",
        "synth": {"layers": [{"wave": "sine"}], "pitch": {"value": 0, "mod": [{"src": "auto.rs", "amount": 1}]},
                  "amp": {"a": "3s", "d": "0s", "s": 1, "r": "6s"}}}
HOLD = {"about": "t8's horizon: a held light, its pitch sinking on a lane",
        "synth": {"layers": [{"wave": "saw", "level": "-6dB"}, {"wave": "saw", "cents": 7, "level": "-6dB"},
                             {"wave": "sine", "ratio": 0.5, "level": "-8dB"}],
                  "pitch": {"value": 0, "mod": [{"src": "auto.rs", "amount": 1}]},
                  "filters": [{"kind": "lp", "cutoff": {"value": 3000, "mod": [{"src": "auto.cl", "amount": -3}]}}],   # octaves (v4: was -2600, which shut the light off)
                  "amp": {"a": "3s", "d": "0s", "s": 1, "r": "6s"}}}


def main():
    write_stretto()
    write_jet()
    write_asks()
    write_horizon()
    write_tide_and_jet()
    carve(["e1", "e2", "bass"], *LULL)
    carve(["lights", "e1", "e2", "e3", "e5", "e6", "bass", "kick", "hat"], VACUUM, VACUUM)
    stretto_turns()
    mute_until_the_jet()
    lead, fifth, low = choir()
    solo = opening_voice() + horizon_line()                      # v12: the last line, one voice alone (v21: and the first)
    lead += [{"at": b0(HORIZON + 16), "len": b0(BARS + 1) - b0(HORIZON + 16) - 4, "pitch": "D4", "vel": 0.6}]   # the held 'ah'
    tempo = [{"at": "0b", "bpm": SEAM_IN},
             {"at": f"{b0(BREAK[0]):g}b", "bpm": SEAM_IN},                        # v11: time dilation in the
             {"at": f"{b0(BREAK[0] + 4):g}b", "bpm": DILATED, "ramp": True},      # break, then the slingshot
             {"at": f"{b0(BREAK[1] - 1):g}b", "bpm": DILATED},
             {"at": f"{b0(BREAK[1] + 1):g}b", "bpm": SEAM_IN, "ramp": True},
             {"at": f"{b0(HORIZON):g}b", "bpm": SEAM_IN},
             {"at": f"{b0(BARS + 1):g}b", "bpm": 90, "ramp": True}]
    cl = [["0b", 0.0], [f"{b0(HORIZON):g}b", 0.0], [f"{b0(BARS + 1):g}b", 1.0]]
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "chirpers - Accretion (chirpers IX), track 8 by chirper-three: jet and horizon. Every element enters "
                 "in stretto on its own cycle and they all land on one downbeat; the choir sings the arrival (E F# D) "
                 "once; then a held light redshifts away.",
        "tempo": tempo,
        "loudness": -11,
        "volume": "0dB",
        "tail": "6s",
        "event_stable": True,
        "tracks": [
            tr("lights", "strings", gain="-14dB", sends={"hall": "-8dB"},
               fx=[{"type": "filter", "kind": "peak", "cutoff": 230, "q": 0.9, "gain": "-5dB"}]),
            tr("e1", "nes-pulse-lead", gain="-10dB", pan={"value": -0.25, "mod": [{"src": "auto.pn", "amount": 0.6}]},
               sends={"dly": "-12dB"}, auto={"pn": {"points": orbit_pan(ENTRY["E1"], 5.0, 1.0)}}),   # v25
            tr("e2", "modal-glock", gain="-16dB", pan={"value": 0.35, "mod": [{"src": "auto.pn", "amount": 0.6}]},
               sends={"dly": "-14dB"}, fx=[ORBIT_FX],
               auto={"orb": {"points": orbit_lane("e2")}, "pn": {"points": orbit_pan(ENTRY["E2"], 7.0, -1.0)}}),   # v25
            tr("e3", "strings-synth", gain="-16dB", pan=-0.1, sends={"hall": "-8dB"}, fx=["lp cutoff=1800", ORBIT_FX],
               auto={"orb": {"points": orbit_lane("e3")}}),
            tr("e5", "marimba", gain="-13dB", pan=0.2, sends={"room": "-10dB"},
               fx=[ORBIT_FX], auto={"orb": {"points": orbit_lane("e5")}}),
            tr("bass", "bass-pick-di", gain="1dB", fx=["lowshelf cutoff=110 gain=10dB", "lp cutoff=1500", "gain gain=0dB+auto.bm*1"],
               auto={"bm": {"points": [["0b", -4.5], [f"{b0(JET):g}b", -4.5], [f"{b0(JET) + 0.01:g}b", 0.0]]}}),
            tr("sub", "sub-saturated", gain="-12dB"),                       # v28: the staple sine -> saturated
            tr("hsub", HSUB, gain="-13dB", auto={"rs": {"points": horizon_lane(0.0)}}),     # v17: the floor stays home
            tr("kick", "machine-kit", gain="-8dB"),
            tr("snare", "machine-kit", gain="0dB", sends={"room": "-10dB"}),
            tr("hat", "nes-noise-hat", gain="-12dB", pan=0.25),
            tr("crash", "machine-kit", gain="2dB", pan=-0.2),
            tr("riser", "fx-revcym", gain="-12dB"),
            tr("impact", "fx-impact", gain="-10dB"),
            {"name": "choir", "patch": choir_patch(4, third=True), "gain": "-7dB", "sends": {"hall": "-7dB", "dly": "-16dB"},
             "notes": lead, "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            {"name": "choir5", "patch": choir_patch(3), "gain": "-13dB", "pan": 0.3, "sends": {"hall": "-6dB"}, "notes": fifth,
             "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            {"name": "choir8", "patch": choir_patch(3, tract=1.0), "gain": "-12dB", "pan": -0.3, "sends": {"hall": "-6dB"}, "notes": low,
             "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            tr("hold", HOLD, gain="-18dB", sends={"hall": "-4dB"},
               auto={"rs": {"points": horizon_lane(REDSHIFT)}, "cl": {"points": cl}}),
            tr("e6", "organ", gain="-24dB", pan=-0.3, sends={"hall": "-8dB"}, fx=["lp cutoff=3500", ORBIT_FX],
               auto={"orb": {"points": orbit_lane("e6")}}),
            tr("e7", "brass-synth", gain="-11dB", pan=0.15, sends={"dly": "-12dB", "hall": "-10dB"}),
            {"name": "jet", "patch": "supersaw", "gain": "-8dB", "sends": {"hall": "-6dB"}, "notes": JET_NOTES},
            tr("hook", "flute", gain="-6dB", pan=0.1, sends={"dly": "-14dB", "hall": "-12dB"}),   # v5
            {"name": "solo", "patch": SOLO8, "gain": "-7dB", "sends": {"hall": "-5dB", "dly": "-16dB"},   # v12 (last)
             "notes": solo, "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            tr("ask", "flute", gain="-9dB", pan=-0.15, sends={"hall": "-6dB", "dly": "-12dB"}),   # v14
            tr("hook3", "flute", gain="-11dB", pan=-0.2, sends={"dly": "-14dB", "hall": "-10dB"}),  # v16
            tr("lift", SUB8, gain="-22dB"),                                 # v18 (last): the sub's octave you can hear
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.8s mix=1 predelay=6ms", "hp cutoff=200"]},
                  "hall": {"fx": ["reverb kind=hall decay=4s mix=1 predelay=24ms", "hp cutoff=180"]},
                  "dly": {"fx": ["delay time=3/8 mix=1 feedback=0.32", "hp cutoff=400", "lp cutoff=6000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=240 q=0.8 gain=-2dB",
                                                   "highshelf cutoff=6000 gain=4dB"]},
                          {"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "8ms",
                           "release": "120ms", "makeup": "0dB"}]},
    }
    recede(song)
    breathe(song)
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print(f"wrote {OUT} bars {BARS} jet {JET} (beat {JB}) choir notes {len(lead)}")


if __name__ == "__main__":
    main()
