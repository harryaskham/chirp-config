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
            toks.append(f"{head}/{ln:.5g}b@{vel}")
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
        for n, on, ln in E1:
            part("e1").add(beat + on, ln, n, 66 + min(24, (bar - 17) // 3))
        beat += 5.0
    # E2: the seven-sixteenth cell, pitched, on a pluck
    beat = phase_start("E2", ENTRY["E2"])
    while beat < JB - 0.01:
        for n, step, v in E2:
            part("e2").add(beat + step * 0.25, 0.25, n, v - 20)
        beat += 1.75
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
        for n, s in E5:
            part("e5").add(beat + s * 0.25, 0.25, n, 70 if s == 0 else 56)
        beat += 3.0
    # the D pedal everything shares (the triangle bass), in E2's rhythm, from 33
    beat = phase_start("E2", 33)
    while beat < JB - 0.01:
        for n, step, v in E2[:2]:
            if not (E3_LIGHT[0] <= beat + step * 0.25 < E3_LIGHT[1]):      # v13: E3's spotlight takes the bass
                part("bass").add(beat + step * 0.25, 0.25, "D2", v - 10)
        beat += 1.75
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


# ---------------------------------------------------------------- the jet (locked 4/4, major)
def write_jet():
    part("impact").add(JB, 4.0, "C3", 120)
    part("impact").add(b0(BREAK[1] + 1), 4.0, "C3", 108)           # v11: the jet fires again
    for bar in range(JET, HORIZON):
        t = b0(bar)
        k = (bar - JET) % 4
        part("lights").add(t, 4.0, chord(E4M[k]), 64 if in_break(bar) else 90)
        part("sub").add(t, 3.75, name_of(midi(E4M[k][0]) - 12 if midi(E4M[k][0]) >= 33 else midi(E4M[k][0])), 70 if in_break(bar) else 92)
        if in_break(bar):
            continue                                       # the breakdown: lights, sub and the choir only
        part("bass").add(t, 1.5, name_of(midi(E4M[k][0]) + 12), 104)
        part("bass").add(t + 2.5, 1.0, name_of(midi(E4M[k][1]) + 12), 88)
        # E1 re-barred into the bar (x 0.8), bright, on the pulse lead - except where the choir sings
        if (bar - JET) % 2 == 0:                  # v5 THE HOOK: E1 stated plainly, augmented to two bars, every two
            for n, on, ln in E1:                  # bars, loud - the album's tune heard clearly and often after the jet
                part("hook").add(t + on * 1.6, ln * 1.6, name_of(midi(n) + 12), 100)
                if bar > BREAK[1]:                # v16: after the break the hook is sung back in thirds
                    part("hook3").add(t + on * 1.6, ln * 1.6, name_of(third_below(midi(n) + 12)), 86)
        # the groove: half time at 150 (75 felt)
        part("kick").add(t, 0.5, "k", 112)
        part("kick").add(t + 2.5, 0.5, "k", 92)
        part("snare").add(t + 2, 0.5, "s", 104)
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
        lead += sung(b0(bar), TAKES[k])
        fifth += sung(b0(bar), TAKES[k], transpose=7, vel_scale=0.7)
        low += sung(b0(bar), TAKES[k], transpose=-12, vel_scale=0.8)
    return lead, fifth, low


# ---------------------------------------------------------------- the horizon
# v4 (ROUND TYPE: section, bars 141-160, ~35 s as the tempo slows): THE LAST IMAGES. At an event horizon what fell
# in is seen forever, frozen, stretched and reddened. So the horizon no longer just holds a sinking chord: each element
# returns ONCE on its own instrument, each SLOWER and LOWER than the one before - E7's column (brass) x2 a semitone
# down at 141, E5's orbit (marimba) x2 two down at 144, E1 (chip pulse) x3 three down at 147, E2 (glock) x4 four down
# at 152, two of E4's lights x2 five down at 155 - while the held light sinks on its lane beneath; the choir's last
# line ('and it was ours') returns at half speed on the same lane at 150, and the held 'ah' takes over from 157.
# (E8 stays sung once, at the jet.)
def echo(name, cell, bar, factor, transpose, vel):
    """cell: [(note, onset beats, length beats)] - placed at `bar`, augmented by `factor`, transposed."""
    for n, on, ln in cell:
        m = brighten(midi(n)) + transpose
        part(name).add(b0(bar) + on * factor, ln * factor, name_of(m), vel)


def write_horizon():
    a, z = HORIZON, BARS
    part("hold").add(b0(a), b0(z + 1) - b0(a) - 2, "D3,A3,D4,F#4", 80)
    part("hsub").add(b0(a), b0(z + 1) - b0(a) - 2, "D1", 84)
    echo("e7", [(nm, s * 0.25, ln * 0.25) for nm, s, ln in E7_JET], a, 2, 0, 84)     # v5: at pitch - slower,
    echo("e5", [(n, s * 0.25, 0.5) for n, s in E5], a + 3, 2, 0, 78)                   # quieter, darker; the
    echo("hook", E1, a + 6, 3, 0, 78)            # v16: the hook's goodbye, on its own flute   # pitch sink waits for
    echo("e2", [(n, st * 0.25, 0.25) for n, st, v in E2], a + 11, 4, 0, 66)            # the light alone (161)
    for i, k in enumerate((0, 1)):
        notes = [name_of(midi(n)) for n in E4M[k]]
        part("lights").add(b0(a + 14) + i * 10, 10.0, ",".join(notes), 60 - i * 6)


def horizon_line():
    """The choir's last line at half speed, at bar 150 (the lead's redshift lane sinks it)."""
    tk, at = TAKES[3], b0(HORIZON + 9)
    out = []
    for n in tk["notes"]:
        d = {"at": round(at + 2 * n["at"], 4), "len": 2 * n["len"], "ph": n["ph"], "pitch": n["pitch"],
             "vel": round(n["vel"] * 0.8, 3)}
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


# v17 (ROUND TYPE: whole song): HOME AT THE END. The horizon's held light sank 5 semitones on the redshift lane, so
# the record's last chord was A major - the dominant, away from home (Harry: tone is home). Now the light redshifts a
# full OCTAVE and lands on D again, an octave down: it falls all the way and arrives home - and the sub stays on D1
# underneath, the floor the light falls toward (it used to sink to A0 under everything). Also: E3's bass roots in its
# spotlight softer (vel 92 -> 76; they were the loudest thing there, -2.1).
REDSHIFT = -12.0


def horizon_lane(drop):
    """Redshift: 0 until the horizon, then sinking to `drop` semitones by the end."""
    return [["0b", 0.0], [f"{b0(SINK):g}b", 0.0], [f"{b0(BARS + 1):g}b", drop]]


# v9 (ROUND TYPE: section, the jet's choir 97-112; the voice engine is pinned - 8ebc9a86): the choir sings on the new
# voice engine - JOIN (each phrase's touching notes one breath: the formants glide from syllable to syllable, so the
# words are heard), INHALE (a breath in the rest before each phrase - the vacuum bar before the jet becomes the choir
# breathing in, and the jet lands on its first word) and S-shaped slides (glide_smooth). Lines legato inside a phrase;
# E5's rests in 'round and round...' stay, as quick breaths.
VOICE8 = {"about": "t8's choir lead: bright and open - a smaller tract, more air; joined phrases, a breath before each",
          "play": {"mono": True, "glide": "90ms", "glide_smooth": True},
          "synth": {"layers": [{"type": "voice", "tract": 0.92, "breath": 0.18, "ph_soft": 0.2, "pulse_rate": 5,
                                "join": True, "inhale": 0.45, "inhale_time": "350ms"}],
                    "pitch": {"value": 0, "mod": [{"src": "expr.f0", "amount": 0.01}, {"src": "auto.rs", "amount": 1}]},
                    "amp": {"a": "30ms", "d": "0s", "s": 1, "r": "300ms"}}}
# v12 (ROUND TYPE: whole song; voice batch 2 pinned - 65c7745c): THE MANY BECOME ONE. The 'choir' was three single
# voices. Now the jet's choir is a CHOIR - each part sung by several singers (singers: the lead in tune in the middle,
# the others with their own size, level, entry and drift; detune kept modest, 0.12 st, so it stays in tune - Harry's
# direction) and every vowel even - while the horizon's last line ('and it was ours', at half speed, sinking on the
# redshift lane) is sung by ONE voice alone on its own track: the many become one as the light leaves.
def choir_patch(singers, tract=0.92, third=False):
    pt = json.loads(json.dumps(VOICE8))
    pt["about"] = f"t8's choir part: {singers} singers on one line, even vowels, joined, a breath before each phrase"
    pt["synth"]["layers"][0].update({"singers": singers, "spread": 0.7, "detune": 0.12, "even": 1.0, "tract": tract})
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
    lead, fifth, low = choir()
    solo = horizon_line()                                        # v12: the last line, one voice alone
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
            tr("e1", "nes-pulse-lead", gain="-10dB", pan=-0.25, sends={"dly": "-12dB"}),
            tr("e2", "modal-glock", gain="-16dB", pan=0.35, sends={"dly": "-14dB"},
               fx=[ORBIT_FX], auto={"orb": {"points": orbit_lane("e2")}}),
            tr("e3", "strings-synth", gain="-16dB", pan=-0.1, sends={"hall": "-8dB"}, fx=["lp cutoff=1800", ORBIT_FX],
               auto={"orb": {"points": orbit_lane("e3")}}),
            tr("e5", "marimba", gain="-13dB", pan=0.2, sends={"room": "-10dB"},
               fx=[ORBIT_FX], auto={"orb": {"points": orbit_lane("e5")}}),
            tr("bass", "nes-triangle-bass", gain="-6dB"),
            tr("sub", SUB8, gain="-12dB"),
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
            tr("hook", "flute", gain="-2dB", pan=0.1, sends={"dly": "-14dB", "hall": "-12dB"}),   # v5
            {"name": "solo", "patch": SOLO8, "gain": "-7dB", "sends": {"hall": "-5dB", "dly": "-16dB"},   # v12 (last)
             "notes": solo, "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            tr("ask", "flute", gain="-9dB", pan=-0.15, sends={"hall": "-6dB", "dly": "-12dB"}),   # v14
            tr("hook3", "flute", gain="-7dB", pan=-0.2, sends={"dly": "-14dB", "hall": "-10dB"}),  # v16 (last)
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.8s mix=1 predelay=6ms", "hp cutoff=200"]},
                  "hall": {"fx": ["reverb kind=hall decay=4s mix=1 predelay=24ms", "hp cutoff=180"]},
                  "dly": {"fx": ["delay time=3/8 mix=1 feedback=0.32", "hp cutoff=400", "lp cutoff=6000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=240 q=0.8 gain=-2dB",
                                                   "highshelf cutoff=6000 gain=4dB"]},
                          {"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "8ms",
                           "release": "120ms", "makeup": "0dB"}]},
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print(f"wrote {OUT} bars {BARS} jet {JET} (beat {JB}) choir notes {len(lead)}")


if __name__ == "__main__":
    main()
