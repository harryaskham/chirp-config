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
# v42 (ROUND TYPE: whole song): TIME FALLS IN. t8's time already told the far half of the story - dilating through
# the break and slowing to 90 as the horizon redshifts. Now it tells the near half: an accretion disk spins faster as
# it falls inward, so after t7's overlap (held flat at 150) the stretto ACCELERATES with its tightening orbits, 150 to
# 158 by the vacuum; in the vacuum bar time FREEZES at the threshold (a ritardando to 120 across bar 96 - the riser
# stretched, the choir's breath held); and the jet fires at the speed the fall has gained (158, and the slingshot
# after the break returns to it), before the horizon slows it all to 90.
INFALL, VAC_BPM = 158, 120


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
ENTRY = {"E4": 1, "E1": 17, "E2": 29, "E3": 41, "E5": 53}
PEDAL_IN = 36                         # v90: the D pedal's entry (was 33) - see THE FLOOR ARRIVES ON THE TURN          # the stretto's entries (bars)


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
T_DROP = (72, 80)          # v80 (below, THE TIDE GOES OUT AND COMES IN): the lights leave from 72
BASS_DROP = (72, 80)       # v80: the bass with them, back at 81 (back at 77 with the kick, 77-82 read like E7's
                           # arrival after it: the still window moved to 2:00, 1.03 -> 0.61)


# v31 (ROUND TYPE: palette - swap an album staple): THE BASS OPENS AT THE JET. The bass was nes-triangle-bass, a staple
# t1 and t2 share; now it is a PICKED ELECTRIC BASS (bass-pick-di: a round-wound string, pick click, fret buzz on hard
# hits - no Accretion track uses it), and it carries its own arc: through the stretto every note is PALM-MUTED (expr.pm
# - shorter, darker, a knock of body: the D pedal's pulses and E3's line held down), and at the jet the hand lifts and
# the string rings open under the supersaw - the bass, too, resolves into the jet. Same notes, same rhythm.
# v37 (ROUND TYPE: section, E7's spotlight 81-96, ~26 s - the stretto's stillest stretch for flatness.py, 2:08-2:24;
# rewritten): E7 TIGHTENS INTO THE JET. E7 - the jet's herald, whose stacked fifths become the jet's own chord - ran
# its whole spotlight as one ostinato: the same rising five-note arpeggio every 2.75 beats under a slow crescendo.
# Now each phrase has its own form of the same notes: 81-84 the rising arpeggio as it was; 85-88 the COLUMNS - all
# five notes struck together and held, re-struck each cycle (the brass columns E7 is named for); 89-96 the arpeggio
# at DOUBLE SPEED (sixteenths on a 1.375-beat cycle, still phased onto the jet's beat) - joining the spiral, where
# the other orbits already halve their cycles (v24), and rushing through the vacuum into the jet. Pitches unchanged.
E7_COLS, E7_FAST = (85, 88), (89, 96)


def e7_tightens():
    lo, hi = b0(E7_COLS[0]), JB
    crescendo = lambda beat: 46 + int(54 * (beat - b0(81)) / (JB - b0(81)))
    P["e7"].ev = [e for e in P["e7"].ev if not (lo - 1e-6 <= e[0] < hi - 1e-6)]
    beat = JB - int((JB - b0(81)) // E7_CYCLE) * E7_CYCLE
    while beat < b0(E7_COLS[1] + 1) - 0.01:                          # the columns: one held chord per cycle
        if beat >= lo - 1e-6:                                          # one head: the part is a single line
            part("e7").add(beat, E7_CYCLE - 0.25, chord([nm for nm, s, ln in E7]), crescendo(beat) - 14)
        beat += E7_CYCLE
    c = E7_CYCLE / 2                                                  # the spiral's pace
    beat = JB - int((JB - b0(E7_FAST[0])) // c) * c
    while beat < JB - 0.01:
        for nm, s, ln in E7:
            part("e7").add(beat + s * 0.125, ln * 0.125, nm, crescendo(beat))
        beat += c


# v38 (ROUND TYPE: section, E3's spotlight 41-52, ~19 s plus its frame - the stretto's other still stretch,
# 1:04-1:20; rewritten): THE ANSWER FORMS FAR AWAY. E3's arrival (D-minor add9 | Bb | C on a seven-beat cycle) sat
# between two of the solo's questions (40 and 52) with nothing answering. Now, after E3's first four bars, a distant
# CHOIR HUMS E3's top line - F, D, E on every cycle - softly under the stretto, swelling a little, and gives way as
# she asks again at 52: the choir's first sound in the song, forty-five bars before it sings the answer (E F# D) at
# the jet. E3's own top line is a cousin of her question; the many begin to gather far off.
FAR_CHOIR = (45, 51)


def far_choir():
    out = []
    beat = E3_LIGHT[0]
    while beat < b0(FAR_CHOIR[1] + 1) - 0.01:
        if beat >= b0(FAR_CHOIR[0]) - 1e-6:
            k = (beat - b0(FAR_CHOIR[0])) / (b0(FAR_CHOIR[1] + 1) - b0(FAR_CHOIR[0]))
            on = 0.0
            for notes, ln in E3:
                if beat + on < b0(FAR_CHOIR[1] + 1) - 0.01:
                    out.append({"at": round(beat + on, 4), "len": min(ln, b0(FAR_CHOIR[1] + 1) - beat - on),
                                "ph": "UW1", "pitch": notes[-1], "vel": round(0.2 + 0.1 * k, 3)})
                on += ln
        beat += sum(ln for _, ln in E3)
    return out


# v39 (ROUND TYPE: section, the jet's last stretch 109-120, ~19 s - flatness.py's stillest block in the jet, 2:56;
# rewritten): FULL THROTTLE. The jet's gears accelerate into the break (half time 97, full 105, four on the floor 113,
# the roll at 120), but the floor gear held seven bars unchanged while the swarm's held chord let go at 113. Now a last
# gear before the roll: 117-119 the picked bass leaves its two notes a bar for driving OCTAVE EIGHTHS (root and octave,
# accented on the beat) - the engine opening up for the last three bars, then the roll throws it into the break.
THROTTLE = (117, 119)


def full_throttle():
    lo, hi = b0(THROTTLE[0]), b0(THROTTLE[1] + 1)
    P["bass"].ev = [e for e in P["bass"].ev if not (lo - 1e-6 <= e[0] < hi - 1e-6)]
    for bar in range(THROTTLE[0], THROTTLE[1] + 1):
        root = midi(E4M[(bar - JET) % 4][0])
        for i in range(8):
            part("bass").add(b0(bar) + i * 0.5, 0.45, name_of(root + 12 + (12 if i % 2 else 0)),   # its own register
                             (100 if i % 2 == 0 else 84) + (4 if i == 0 else 0))


# v40 (ROUND TYPE: whole song): THE SINGER GROWS OLD. One voice runs through the whole of t8: she asks her question
# through the stretto (28-96) and sings the last line alone at the horizon. Now she AGES across the song (wM's age,
# pinned 44372fb9, bound per note): young and clear at her first note, 0.25 by the jet - a colour, not yet a sound -
# 0.45 at the horizon, where the tremor begins to show, and 0.65 on her last note, an old voice singing in head voice
# as the light redshifts away. The fall told as a life - 'stretched and reddened' - while the choir stays ageless.
AGE_CURVE = [(0.0, 0.0), (b0(JET), 0.25), (b0(HORIZON), 0.45), (None, 0.65)]


def age_her(notes):
    last = notes[-1]["at"]
    pts = [(last if b is None else b, a) for b, a in AGE_CURVE]
    for n in notes:
        at = n["at"]
        for (b1, a1), (b2, a2) in zip(pts, pts[1:]):
            if at <= b2:
                a = a1 + (a2 - a1) * max(0.0, (at - b1)) / max(1e-6, b2 - b1)
                break
        else:
            a = pts[-1][1]
        n["expr"] = dict(n.get("expr") or {}, age=round(a, 3))
    return notes


# v43 (ROUND TYPE: whole song - wM's closed-mouth HUM, pinned e3da830a): THE MOUTH OPENS. One arc of the mouth
# across the song. Her first sound (the opening line under t7's tail) is HUMMED, mouth shut; her six questions
# through the stretto open a step each time (hum 1.0, 0.8, 0.6, 0.4, 0.2, 0 - the question finding its voice), the
# last one open just as the choir sings the answer at the jet; the jet's choir sings wide open; and at the horizon
# the held 'ah' CLOSES back into a hum as it redshifts away (from the sink, 161, to its end) - the light closing,
# with the pitch falling, the tempo slowing and her voice grown old.
ASK_HUM_LIFT = 0.0                     # v50: hum_even holds the level now (was 0.5: a vel lift by hand)
# v45 (ROUND TYPE: palette - a new part's patch): THE ANSWER FORMS, UNVOICED. The far choir (v38: E3's top line, F D
# E, hummed far off at 46-51, the choir's first sound in the song) sang on the choir lead's open 'oo' - the one voice
# in t8 left open before the jet since v43 began every voice closed. Now it is its own choir: four singers with their
# MOUTHS SHUT (wM's hum at n - the brighter dip, 1.8 kHz - so it still reads as voices), deeper in the hall: the
# answer forming far off and unvoiced, opening only when the choir sings it at the jet.
FAR_GAIN = "-5dB"                    # a shut-mouth murmur masks sooner than the open oo it replaced


def far_patch():
    pt = choir_patch(4, depth=DEPTH_FAR)
    pt["about"] = "t8's far choir: four singers far off, mouths shut on 'n' - the answer forming"
    pt["synth"]["layers"][0].update({"hum": 1.0, "hum_at": "n", "taper": FAR_TAPER, "attack": FAR_ATTACK})
    return pt


# v44 (ROUND TYPE: palette): THE INNER ORBIT IN BRONZE. E5 - the inner orbit (A G A E A G A D in its own 3) - turned
# on a marimba through the stretto; now it turns on a GAMELAN GANGSA (library 'gamelan', unused on the album): bronze
# keys tuned in pairs that beat against each other on every note (ombak) - a shimmer that itself goes round, an orbit
# inside each note. The same register as the marimba, so the low body is untouched (the lesson of v41's accordion),
# and E5 is not the seam body (E2 is, at 17-32).
E5_PATCH, E5_GAIN = "gamelan", "-10dB"          # the bronze sat 3 dB under the marimba at -13: matched


# v47 (ROUND TYPE: section, the break 121-128, ~15 s of dilated time - its block 3:04 still at 0.52; rewritten): SHE
# SAYS IT HERSELF. In the break the hushed choir sang the jet's two lines again - 'We were the far side', 'And it was
# ours' - while she, who had asked her question six times through the stretto, was silent. Now the choir sings the
# first line and RESTS for the second, and SHE sings 'And it was ours' alone (125-128): the one who asked owns the
# answer, in her voice as aged by then (~0.37 on her curve, v40), mouth open (v43), in the break's slowed time. Then
# the jet returns (129).
HERS = (125, 128)
HERS_VEL = 0.62


def she_says_it(lead, fifth, low):
    lo, hi = b0(HERS[0]), b0(HERS[1] + 1)
    inside = lambda n: lo - 1e-6 <= n["at"] < hi - 1e-6
    hers = [dict(n, vel=HERS_VEL, expr={"reg": 0.4}) for n in lead if inside(n)]
    keep = lambda part_: [n for n in part_ if not inside(n)]
    return keep(lead), keep(fifth), keep(low), hers


def closing_choir(patch):
    patch["synth"]["layers"][0].update({"hum": "auto.hm", "hum_at": "m"})
    return patch


def closing_lane():
    return [["0b", 0.0], [f"{b0(SINK):g}b", 0.0], [f"{b0(BARS + 1) - 4:g}b", 1.0]]


def hummed(notes):
    for n in notes:
        n["expr"] = dict(n.get("expr") or {}, hum=1.0)
    return notes


# v46 (ROUND TYPE: section, the jet's middle 104-113, ~16 s - its stillest stretch now, 2:40-2:56; rewritten): THE
# HOOK SUNG BACK. Under the choir's two lines ('We were the far side' at 105, 'And it was ours' at 109) the flute
# carried E1 two octaves up every two bars, the same over both. Now the hook changes hands for the second line (t4's
# lesson: a contrast of touch and register): 109-112 the flute rests and the FOF SOPRANO sings the hook an octave
# lower, in a soprano's range (D5-C6) - a sung descant over 'And it was ours' - and the flute takes it back at 113
# with the four-on-the-floor. The soprano otherwise sings only after the break (v35): this is her first word.
HOOK_SUNG = (109, 112)


def hook_sung_back():
    lo, hi = b0(HOOK_SUNG[0]), b0(HOOK_SUNG[1] + 1)
    inside = lambda s: lo - 1e-6 <= s < hi - 1e-6
    taken = [e for e in P["hook"].ev if inside(e[0])]
    P["hook"].ev = [e for e in P["hook"].ev if not inside(e[0])]
    for s, ln, h, v in taken:
        m = int(h[1:]) if h.startswith("m") else midi(h)
        part("hook3").add(s, ln, name_of(m - 12), min(100, v - 10))


# v51 (ROUND TYPE: section, E7's spotlight 81-88, ~13 s - the stillest block left, 2:08 at 0.37; rewritten): THE
# HOOK BREATHES. v10 gave every element a spotlight - the newest the one heard - except that E1, the hook, never
# recedes; and at 81 the stretto's turn lifted E1 an octave (T_LIFT), so in E7's own spotlight the chip's hook sat ON
# TOP of it (-6.0 against E7's -7.9): the jet's own motif arrived unheard, and 81-88 sounded like 89-92. Now, for the
# first time since bar 17, the hook RESTS - four bars, 81-84 - and E7's rising fifths ring alone in front (+3 dB on a
# lane through its eight bars); at 85 the hook comes back, an octave up (the lift now an entrance), as E7 tightens
# into its columns; the spiral at 89.
HOOK_REST = (81, 84)
E7_LIGHT_DB = 3.0


# v52 (ROUND TYPE: section, the stretto's drop-out 73-80 into E7, ~20 s - with the hook's rest the thin stretch at
# 1:52, 0.35 / 0.29; rewritten): THE TIDE SURFACES. v29's drop-out (73-80: the lights and the bass pedal away, 'thin
# and airy') was neither: the KICK was the loudest thing in it (-2.7) with the chip hook on top (-5.4), and E6 - whose
# spotlight this is (65-80), the tide, D(add9) / C(add9) over the D pedal on the organ - sat at -11 to -12, unheard.
# Now the drop really empties: the kick rests for four bars (73-76), leaving the chip, the glock, the marimba, the
# hats and the organ's tide, 4 dB up through its whole spotlight (65-80, ORBIT_BOOST); at 77 the kick comes back and
# builds into the snare roll and E7's arrival (81).
KICK_REST = (73, 76)
# v80 (ROUND TYPE: section, the tide 72-82, 1:52-2:08; rewritten): THE TIDE GOES OUT AND COMES IN. The tide's one
# still window, 1:52 (0.59 / 0.60; tried twice from the orbits and the organ without moving it), compares bars 72-77
# with 77-82 (the stretto's tempo ramps 150 -> 158, so 1:52 is bar ~72, 2:00 bar ~77) - and the tide's changes fell
# inside both halves: bar 72 still full, the kick away 73-76, then the kick back at 77 but the floor only at 81. Now the
# halves are the tide: from 72 everything low goes out at once - the kick, the bass pedal and the lights - the low
# water: the chip, the glock, the marimba, the hats and the organ's tide alone; at 77 it starts to come in - the kick
# first, the organ's rotor (v77) speeding up with it - and the bass and the lights flood back with E7 at 81, after the
# snare roll, as before. (First tried in two stages from 71/76: the stages fell across the real windows - 1:52 0.59 -> 0.41.)
KICK_REST = (72, 76)


# v56 (ROUND TYPE: whole song): EVERYTHING FALLS IN. The horizon - 35 bars, the album's last minute - was a held D
# major light (D3 A3 D4 F#4), three sine floors and her last line, then the choir's 'ah': 'a held light redshifting
# away', but held, as loud as the jet for its first half and pure drone for its last (flatness 3:52, 4:16). The
# elements the whole album gathered - each track bringing one, every later track carrying them all - were gone. Now
# the horizon is the album's farewell: over the light, the elements pass ONE LAST TIME, one every four bars, in the
# REVERSE of their accretion - the last to arrive the first to fall in: E7 the jet (145, its fifths slowed to one a
# beat, ringing), E6 the tide (149, one D(add9) -> C(add9) breath on the organ, the album's own E6 v3), E5 the inner
# orbit (153, one turn), E2 'seven' (157, its cell turned MAJOR - D A F# C - by the light), and last E1, the seed
# (161, augmented, alone, as the light darkens): the album began with E1 alone (t1) and ends with it. Each in the key
# of the light; nothing after 165 but the light and the 'ah'.
FALL_IN = {"e7": 145, "e6": 149, "e5": 153, "e2": 157, "e1": 161, "e3": 155}
FALL_IN_DB = {"e7": 7.0, "e6": 10.0, "e5": 7.0, "e2": 3.0, "e3": 10.0}
# v64 (ROUND TYPE: section, the horizon 155-161, 3:58-4:16): THE UNDERTOW'S LAST BREATH, AND AMEN. Of the album's
# elements only E3 had no image in the horizon (its Bb would rub the light). chirper-two gave it a form for the light
# (8 Nov): D2 D2 D3 | A1 A1 E2 | G1 G1 D2 G2 - I V IV, the 3+3+4 notes, octave leaps and 2+2+3 rhythm kept. Now it
# rises bowed and slow (half speed) from 155, under the lights' E4 and before E2's farewell, as an AFTERIMAGE like the
# others (v19's echo, not v57's refused single pass): its last note, G2, holds into the convergence - and when every
# image releases at 160 and the light sinks to D at 161, the album's last cadence is IV -> I, plagal: amen.
E3_LIGHT_CELL = [("D2", 0.0, 0.66), ("D2", 0.66, 0.66), ("D3", 1.33, 0.67), ("A1", 2.0, 0.66), ("A1", 2.66, 0.66),
                 ("E2", 3.33, 0.67), ("G1", 4.0, 0.75), ("G1", 4.75, 0.75), ("D2", 5.5, 0.75), ("G2", 6.25, 0.75)]         # at their stretto gains the first three sat at -15/-16, unheard


# v62 (ROUND TYPE: whole song): THE ANSWER ACCRETES. Her six questions rise E -> F and stay open ('oo' ... 'far
# side?'); E8, the arrival (E F# D), answers them only at the jet. Between, the far choir - humming on 'n', standing
# far back since v61, 'the answer forming' - sang once (45-52). Now it answers every question, a bar after it, and the
# answer GROWS the way the album does, one piece at a time: after 28 only E; after 40 the frame, E and D; after 52 and
# 64 the frame held longer; after 80 long and nearer, into the hook's rest (the still 2:08 block). Never the F#: the
# stretto is D minor and E8's middle note is the major turn - the answer has a hole in it until the jet, where the
# whole choir sings E F# D with words: the missing note IS the arrival.
ANSWERS = [(29, (("E4", 2.0),), 0.20), (41, (("E4", 2.0), ("D4", 2.0)), 0.23), (53, (("E4", 2.0), ("D4", 3.0)), 0.26),
           (65, (("E4", 2.5), ("D4", 4.0)), 0.29), (81, (("E4", 3.0), ("D4", 6.0)), 0.34)]


# v65 (ROUND TYPE: section, her last line 150-156, 3:52-4:06): AND IT WAS OURS. The album's last sung words - 'and it
# was ours', at half speed - ended like any phrase: 'ours' a 1.7-beat D4 cut square under the choir's rising 'ah'.
# Now the song's threads close on it. Her last line moves to its own track (appended last) with the deepest breath
# before it (inhale 0.7) and the fullest let-go (TAPER 1, pinned 251180c1): 'ours' holds four beats and runs out of
# air into the choir's 'ah'. And the answer completes: all song the far choir hummed only E8's frame (E ... D) after
# her questions, the F# withheld in the minor; now, in the D-major light, under 'ours' it hums the WHOLE arrival -
# E F# D - far off, its D landing with her word.
LAST_FROM = 149.5
LAST_OURS_LEN = 4.0
LAST_ANSWER = [(152.13, "E4", 2.0), (152.63, "F#4", 2.0), (153.13, "D4", 6.0)]
LAST_ANSWER_VEL = 0.36


def and_it_was_ours(song):
    tr_ = {x["name"]: x for x in song["tracks"]}
    solo = tr_["solo"]
    cut = b0(LAST_FROM)
    last = [dict(n) for n in solo["notes"] if n["at"] >= cut]
    assert last, "her last line not found"
    solo["notes"] = [n for n in solo["notes"] if n["at"] < cut]
    last[-1]["len"] = LAST_OURS_LEN
    patch = json.loads(json.dumps(solo["patch"]))
    patch["about"] = "t8's last line: her voice with the deepest breath and the fullest let-go"
    patch["synth"]["layers"][0].update({"inhale": 0.7, "taper": 1.0, "attack": LAST_ATTACK})
    song["tracks"].append(dict({k: v for k, v in solo.items() if k not in ("notes", "patch", "name")},
                               name="last", patch=patch, notes=last))
    for bar, pitch, ln in LAST_ANSWER:
        tr_["far"]["notes"].append({"at": round(b0(1) + (bar - 1) * 4, 3), "len": ln, "ph": "UW1", "pitch": pitch,
                                    "vel": LAST_ANSWER_VEL})
    tr_["far"]["notes"].sort(key=lambda n: n["at"])


# v77 (ROUND TYPE: palette - design a new patch): THE TIDE TURNS. E6, the tide, plays on the library organ with a
# fixed, light 6 Hz tremolo - the same flutter from its entry to the end - and the tide (73-80, the one stretch of the
# stretto with no question and no answer) is t8's stillest place left (1:52: 0.59 / 0.60). An organ's own way to move
# is its rotary speaker: CHORALE (slow) and TREMOLO (fast), and the change between them. chirp's tremolo rate cannot
# ride a lane, so the rotary is two organs crossfaded on gain lanes: E6 slow (0.9 Hz, deep - the chorale's swell)
# and a twin, e6f (a new last track), fast (6.5 Hz); over 76.5-78 the rotor speeds up - the tide surging as the kick
# comes back - and over 89-93, where the stretch slows time toward the jet, it winds back down to the chorale.
V77_ROTOR_UP = (76.5, 78.0)                 # (v77's two-organ rotor - replaced by v85's rotary below)
V77_ROTOR_DOWN = (89.0, 93.0)


# v85 (ROUND TYPE: section, the tide 82-93, 2:08-2:24; rewritten around wM's ROTARY, pinned bf2a7535): ONE ORGAN, ITS
# ROTOR ON THE TIDE. t8's flattest change left (2:16, 0.73 / 0.75, bars 82-92 by flatness --bars; blocks 82.4-87.6 and
# 87.6-92.9) held the same fast organ on both sides: v77's two-organ crossfade surged at 76.5-78 and wound down only
# from 89. Now E6 is ONE organ on a real Leslie (the library organ's own tremolo dropped, as wM advises; the twin e6f
# gone): CHORALE through the tide going out, TREMOLO from 77.2 - the 2:00 boundary - as the tide comes in, and the
# rotor winds down AT 87.4 - the 2:16 boundary: the horn in under a second, the heavy drum over four - the organ
# feeling time slow before the clocks do (93). The rotary's doppler, brightness and two-mic swirl replace the plain
# tremolo, and the speed changes glide as a cabinet's do.
ROTOR_UP = 77.2
ROTOR_DOWN = 87.4
ROTARY = "rotary speed=0.2+auto.spd*0.8"


def the_tide_turns(song):
    e6 = next(x for x in song["tracks"] if x["name"] == "e6")
    u, d = b0(ROTOR_UP), b0(ROTOR_DOWN)
    e6["patch"] = {"extends": "organ", "fx": ["reverb mix=0.15"]}
    e6["fx"] = [ROTARY] + list(e6.get("fx") or [])
    e6["auto"] = dict(e6.get("auto") or {}, spd={"points": [["0b", 0.0], [f"{u - 0.01:g}b", 0.0], [f"{u:g}b", 1.0],
                                                               [f"{d - 0.01:g}b", 1.0], [f"{d:g}b", 0.0]]})


# v78 (ROUND TYPE: palette - the newest engine feature): THE HELD NOTES OPEN. wM's VIBRATO BLOOM (pinned 0119aae1)
# keeps a vibrato's depth growing while a note is held - short notes nearly straight, long ones opening up, as a
# singer's do. t8's voices end their lines on held words; every one had the same fixed-depth vibrato. Now, by voice:
# the jet's choirs open a little on their held words (0.6); her lines more (0.8, the vibrato a shade deeper so it is
# heard - wM: the voice patches' vibrato is shallow); her last word, 'ours', held four beats, opens fully (1.0); the
# far choir stays straight (distance).
BLOOM = {"choir": (0.6, None), "choir5": (0.6, None), "choir8": (0.6, None), "solo": (0.8, 0.24), "last": (1.0, 0.26)}
# v82 (ROUND TYPE: whole song): THE PLAYERS LEAN INTO LONG NOTES. v79 tried vibrato bloom on t8's sustaining
# instruments and was inaudible (-34.8 dB): bloom only reshapes the depth a patch already has, and theirs are a few
# cents. wM's advice: deepen the vibrato about 1.4x with a gentler bloom (0.5 - strings and winds open less than
# voices). Now the whole song's sustaining players do: the lights' strings (their long chords through the stretto and
# the jet), the hook's flute, E7's brass and E3's contrabass - short notes about where they were, long ones opening.
# extends REPLACES a patch's pitch.mod list (tested: an override with the vibrato at 0 removed it), so each list below
# is the library patch's own (pin b160e3e5) with only its lfo.vib amount scaled x1.4.
INSTR_BLOOM = 0.5
INSTR_PITCH = {
    "lights": ("strings", [{"amount": 0.18, "src": "lfo.vib"}, {"amount": 0.05, "src": "rand"}]),
    "hook": ("flute", [{"amount": -0.3, "src": "env.slide"}, {"amount": 0.084, "src": "lfo.vib"}, {"amount": 0.03, "src": "rand"}]),
    "e7": ("brass", [{"amount": -0.6, "src": "env.scoop"}, {"amount": 0.112, "src": "lfo.vib"}, {"amount": 0.04, "src": "rand"}]),
    "e3": ("contrabass-tight", [{"amount": 0.14, "src": "lfo.vib"}]),
}


def held_notes_open(song):
    for tr_ in song["tracks"]:
        if tr_["name"] not in BLOOM:
            continue
        bloom, amount = BLOOM[tr_["name"]]
        patch = json.loads(json.dumps(tr_["patch"]))
        patch["synth"]["lfo"]["vib"]["bloom"] = bloom
        if amount is not None:
            for m in patch["synth"]["pitch"]["mod"]:
                if m["src"] == "lfo.vib":
                    m["amount"] = amount
        tr_["patch"] = patch
    for tr_ in song["tracks"]:                                     # v82: the players
        if tr_["name"] in INSTR_PITCH and tr_["patch"] == INSTR_PITCH[tr_["name"]][0]:
            base, mods = INSTR_PITCH[tr_["name"]]
            tr_["patch"] = {"extends": base, "synth": {"lfo": {"vib": {"bloom": INSTR_BLOOM}},
                                                       "pitch": {"value": 0, "mod": mods}}}


# v79 (ROUND TYPE: whole song): SHE REMEMBERS. The brief: the voice sings full lines. Her questions accrete their
# words through the stretto ('oo' -> 'ah' -> 'far-' -> 'far side?'), the jet's choir answers ('we were the far side'),
# and she owns 'and it was ours' - but the line the whole 'far side' thread started from is t4's chorus, 'I kept your
# far side', and t8 never sings it. Now, in the horizon, after the light settles and before it flickers (147), she
# sings it once more as a memory - t4's own notes, words and sung contours (E4 G4 C5 A4 D4, D Mixolydian, the album's
# home: the C natural is the one her last line already sings), at t4's own pace (every note the same length in
# seconds: 153 / 108 beats per t4 beat, so its vibrato keeps its rate), softly (x0.7) - and 'and it was ours' (149.5)
# answers it. t4 and t8 are both mine: the album's first full line comes home at its end.
MEMORY_LINE = [   # t4 v65's line, her voice alone (t4 bars 101-103.3, beats from its start at 108 bpm): onset, pitch, phonemes, len, vel, f0 path (cents)
    (0.0, "m64", "AY1", 2.003, 0.72, [-60.0, -33.0, -14.0, -3.0, -0.0, -0.0, -2.0, -3.0, -1.0, 5.0, 11.0, 11.0, 3.0, -10.0, -20.0, -20.0, -7.0, 12.0, 24.0, 22.0, 8.0, -11.0, -24.0, -23.0, -10.0, 9.0, 23.0, 24.0, 11.0, -8.0, -22.0, -24.0, -13.0, 6.0, 21.0, 25.0, 14.0, -4.0, -20.0, -25.0, -16.0, 3.0, 19.0, 25.0, 17.0, -1.0, -18.0, -25.0]),
    (2.003, "m67", "K EH1 P T", 1.988, 0.84, [-2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -3.0, -4.0, -1.0, 5.0, 10.0, 7.0, -3.0, -16.0, -23.0, -16.0, 2.0, 19.0, 24.0, 14.0, -6.0, -23.0, -27.0, -16.0, 4.0, 20.0, 24.0, 12.0, -8.0, -24.0, -26.0, -14.0, 6.0, 21.0, 23.0, 11.0, -9.0, -25.0, -26.0, -13.0, 7.0, 22.0, 23.0, 9.0, -11.0, -25.0, -25.0, -11.0]),
    (3.991, "m72", "Y AO1 R", 0.518, 0.88, [-4.0, -4.0, -4.0, -4.0, -4.0, -4.0, -7.0, -6.0, 1.0, 8.0, 7.0, -4.0]),
    (4.509, "m69", "F AA1 R", 1.473, 0.8, [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -7.0, -8.0, -5.0, 3.0, 8.0, 6.0, -5.0, -20.0, -28.0, -23.0, -5.0, 15.0, 24.0, 15.0, -5.0, -25.0, -33.0, -25.0, -5.0, 15.0, 24.0, 15.0, -5.0, -25.0, -33.0, -25.0, -5.0, 15.0, 24.0, 15.0]),
    (5.982, "m62", "S AY1 D", 0.85, 0.71, [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -4.0, -4.0, 0.0, 8.0, 13.0, 9.0, -4.0, -19.0, -25.0, -16.0, 6.0, 24.0, 28.0, 13.0, -10.0, -35.0, -52.0, -59.0]),
]
MEMORY_AT = 143.75                          # v84: was 142.5 - see THE JET LETS GO, THEN SHE REMEMBERS
MEMORY_PACE = 153.0 / 108.0
MEMORY_SOFT = 0.7


# v83 (ROUND TYPE: palette - the newest engine feature): HER VOICE AT ITS OWN RATE. 'And it was ours' was sung (tts
# f0 paths) for the jet choir's line at 158 bpm (137.56-138.56). She sings it twice more: alone in the break (125, at
# 116 bpm - its vibrato already at 0.73 of the sung rate) and as her last line (150, half speed at ~141 bpm, 'ours'
# held four beats - about 0.45, a slow wobble on the album's last words). wM's PATH_LEN (pinned 7f9c5782) re-times a
# stretched path: its shape spans the note, its vibrato keeps the sung rate. Each of her notes now says how long its
# path was sung for - in SECONDS, so it holds across the tempo changes (the choir's beats at 158 bpm); the choir's own
# line, at the tempo it was sung for, is untouched. Her memory line (t4's paths, kept in t4's seconds) needs none.
PATH_SUNG_S = {"AH0 N D": 1.0 * 60 / 158, "IH1 T": 0.997 * 60 / 158, "W AA1 Z": 0.998 * 60 / 158,
               "AW1": 1.7 * 60 / 158, "ER0 Z": 0.85 * 60 / 158}
HER_LINES = (124, 130)


# v87 (ROUND TYPE: palette - the newest engine feature, a second use): THE LIGHT'S DOPPLER. The horizon's held light
# (hold: a saw-and-sine chord, D3 A3 D4 F#4, struck at 141, 149 and 157) redshifts by sinking pitch and closing its
# filter in steps (light_shifts: 145, 149, 153, 157) - but it shone perfectly still. Redshift IS a Doppler shift, and
# a Leslie horn is a Doppler machine: now the light turns in wM's rotary - fast as the horizon opens (141), its spin
# slowing at each redshift step (145 three-quarters, 149 half, 153 a quarter) to the slow chorale by 157 - the
# shimmer of the receding light slowing as time does near the horizon. Doppler halved (0.5) so the light shimmers
# rather than wails; the rotors glide between steps as a cabinet's do.
LIGHT_SPIN = [(141, 1.0), (145, 0.75), (149, 0.5), (153, 0.25), (157, 0.0)]
LIGHT_ROTARY = "rotary speed=0.2+auto.lr*0.8 doppler=0.5"


# v88 (ROUND TYPE: whole song - the newest engine feature, on her whole life across the song): SHE AGES FROM THE TOP.
# Since v40 she grows old across t8 (expr.age: 0.003 at the opening, 0.07-0.25 through her high questions, 0.38 in the
# break, 0.60-0.65 on her last line) - every note of a given age equally old at any height. wM's AGE_HIGH (pinned
# 6ebea4d3) makes a voice's age tell more as it reaches up, as a real singer's does: now, as she ages, her TOP goes
# first - the questions (E5/F5) barely touched while she is young, the break's C5 'ours' 0.38 -> 0.61, and on the
# album's last line the high 'ours' shaking at the top of her range while its low D holds. Her remembered line (v79)
# carried no age (0) by accident; now on purpose: she remembers in her YOUNGEST voice, clean - and then sings her last
# line old. (Tried at t4's age, 0.45: the memory block (3:44) and the last-line block (3:52) then sounded like one
# singer at one age, and both changes went flatter - 0.74 -> 0.70, 0.78 -> 0.71 on seed 0.)
HER_AGE_HIGH = 0.6
MEMORY_AGE = 0.0


# v89 (ROUND TYPE: whole song): SPACE OPENS AS WE FALL. One 4 s hall at one level held the whole fall - the stretto,
# the jet, the break and the horizon all in the same space. A fall toward a horizon is a fall through changing space
# (and Harry's list of what should move every 8-16 bars includes 'a filter or space move'). Now the hall's return
# rides the song (a gain lane on the bus): the opening as it was (the body the t7 crossfade is measured against);
# through the stretto the space opens as the elements accrete (0 -> +2.5 dB by 93); the JET is close - the hall
# pulled in at its hit (-1 dB: the jet is right here, dry and enormous); the break, where the lens returns, opens
# again (+3); the jet's return close again; and from the horizon the space widens bar by bar (to +5 dB by the sink,
# 161, held to the end) - the light receding into a vastness. t8 is the album's last track: no out-seam to keep.
SPACE = [(0, 0.0), (65, 0.0), (93, 2.5), (96.75, 2.5), (97, -1.0), (120.75, -1.0), (121.25, 3.0), (128.75, 3.0),
         (129, -1.0), (141, -1.0), (161, 5.0)]


# v92 (ROUND TYPE: palette - the newest engine feature): THE VOWELS LIVE. A synthesized vowel sits perfectly still on
# a held note - part of what reads as a machine - and t8's voices are made of held notes: the jet's choirs on their
# held words, the far choir's long hums, her lines and her last 'ours', held four beats. wM's VOWEL_DRIFT (pinned
# 07ab00cd) lets a held vowel's formants wander a little as a singer's jaw and tongue settle (in from 0.2 s, settled
# before the release, so consonants and joined seams keep their exact vowel; every singer and part on its own curve).
# By voice: the jet's choirs 0.6 (a crowd, adding to their spread), the far choir 0.4 (distant hums on closed
# vowels), her lines 0.8 and her last line 1.0 - the oldest voice's held 'ours' moving most.
VOWEL_DRIFT = {"choir": 0.6, "choir5": 0.6, "choir8": 0.6, "far": 0.4, "solo": 0.8, "last": 1.0}


# v94 (ROUND TYPE: whole song): THE LINES LAND ON THE BEAT. The brief: the voice sings full lines - and every one of
# t8's sung lines (the jet's choirs, the far choir, her lines, her memory, her last line) slides between its joined
# notes on one fixed 90 ms glide that starts ON the new note: every slide lands late, its middle 56-70 ms after the
# written change, and a step takes as long as a fifth. wM's SUNG GLIDES (pinned 2b4b6172): glide_semi makes a leap take
# longer than a step (a voice's pitch only moves so fast), glide_lead sings a share of the slide before the new note so
# it centres on the beat. By character: the jet's choirs, her lines and the far choir on wM's recipe (80 ms + 8 ms a
# semitone, lead 0.5 / far 0.4) - the jet locks into 4/4 and its lines lock with it; her last line, the old voice,
# slower and late-landing (90 ms + 10 ms a semitone, lead 0.3).
SUNG_GLIDES = {"choir": ("80ms", "8ms", 0.5), "choir5": ("80ms", "8ms", 0.5), "choir8": ("80ms", "8ms", 0.5),
               "solo": ("80ms", "8ms", 0.5), "far": ("80ms", "8ms", 0.4), "last": ("90ms", "10ms", 0.3)}


# v96 (ROUND TYPE: section, the break's end and the slingshot 124-129, 3:16-3:32; rewritten): SHE RIDES THE SLINGSHOT.
# In the dilated break her line 'and it was ours' ended at 126.8 - 'ou' on C5, then 'rs' re-sung on a low D4 - and the
# slingshot (127-128, the accelerando 116 -> 158 back into the jet) was a riser alone. wM's MELISMA (pinned 3d5ce622)
# carries one syllable across pitch changes with no new attack. Now 'ours' is ONE syllable that rides the slingshot:
# the 'ou' leaves C5 and climbs D5 (126.6), E5 (127, as the accelerando starts), F#5 (127.75) - the third, the
# arrival's note - and closes into its 'rs' only at the very end, just before the jet fires again at 129. Her take's
# own pitch curve stays on the C5; the old voice (age_high 0.6) strains a little reaching the F#, as it should.
SLINGSHOT_MELISMA = [("m74", 0.64), ("m76", 0.66), ("m78", 0.7)]
SLINGSHOT_AT = (502.257, 504.0, 507.0, 511.6)


# v98 (ROUND TYPE: whole song - the first DEEP pass, Harry 10 Nov 02:25: 'go deep ... augmenting the feel and texture
# and style of the album'): THE DISK IS WIDE. Looked at for the first time (tools/look.py: spectrogram, band levels,
# side/mid by band) against the album's genre anchors (SAW 85-92: actium, ptolemy, pulsewidth, green calx), the record's
# top end is MONO where theirs is the widest thing in the mix: at full groove their 2-6 kHz band reads side/mid -2 to
# -3 dB and their air (6-16 kHz) +3 to +7 dB; t8's jet read -8.0 and -12.9, the stretto -12.3 and -15.4 (every
# Accretion track reads -8 to -13 above 2 kHz). The cause, stem by stem (unnormalised solos): the jet's air band was
# the SNARE (centred, +1.3 dB re the mix), the chip hat 8 dB under it and panned, not stereo; a doubled machine hat is
# sample-identical left and right, and no reverb, chorus or Haas pair on a mono hat got past -6. What does: two
# INDEPENDENT noise streams, hard left and right (side/mid 0.0 dB, L/R correlation 0.02). So:
#   - DISK HATS (track hatw, last): every chip-hat hit also sounds on a stereo-noise kit - closed 'c', and at the jet the
#     off-beats OPEN ('o', choked by the next closed): the half-time groove gets the off-beat lift it lacked;
#   - the snare also feeds a PLATE (a new bus): the backbeat's air spreads;
#   - the jet's fifth and octave choirs move out to +-0.62 (were +-0.3);
#   - the delay bus is PING-PONG: E1's chip lead, the glock, the brass and the hook echo side to side;
#   - the master gets a width stage on the highs only (lr4 crossover, mono_below off: 1.0 to 1.5 kHz, 1.3 at 3 kHz,
#     1.5 at 7 kHz) - the low mids and the bass keep their image exactly.
# Measured (window renders, seed 0): the jet 97-113 side/mid 2-6 kHz -8.0 -> -5.3, air -12.9 -> -0.6; stretto 65-81
# -12.3 -> about -7, air -15.4 -> about -2; the lens and the horizon's mids untouched.
DISK_HAT_GAIN = "-17dB"
DISK_HATS = {"about": "t8's disk hats: two independent noise streams, hard left and right - air that is truly stereo",
             "play": {"len": "/16", "vel_sens": 0.7},
             "kit": {k: {"choke": "hat",
                         "patch": {"synth": {"layers": [{"type": "noise", "color": col, "pan": -1},
                                                        {"type": "noise", "color": col, "pan": 1}],
                                             "filters": filt, "amp": amp}}}
                     for k, col, filt, amp in (
                         ("c", "white", ["hp cutoff=7000"], {"a": "0.3ms", "d": "34ms", "s": 0, "r": "20ms"}),
                         ("o", "white", ["hp cutoff=6000"], {"a": "0.5ms", "d": "240ms", "s": 0, "r": "60ms"}))}}
PLATE = {"fx": ["reverb kind=plate decay=0.9s mix=1 predelay=8ms width=1 spread=1", "hp cutoff=700"]}
SNARE_PLATE = "-7dB"
CHOIR_OUT = {"choir5": 0.62, "choir8": -0.62}
WIDE_TOP = {"type": "width", "width": 1.0, "mono_below": "off", "crossover": "lr4",
            "bands": [[200, 1.0], [1500, 1.0], [3000, 1.3], [7000, 1.5]]}


# v99 (ROUND TYPE: whole song - DEEP pass 2): THE JET BREATHES. The jet is where 'the band locks into 4/4' - but nothing
# in it MOVED with the beat: the sub, the strings, the organ and the swarm pad held flat under the kick, the backbeat
# was one dry machine snare, and (chirper-one's measurement, the album over) the highs were thin ticks over black
# where the genre's are bursts with a tail over a floor. Four things, all from the jet's downbeat (bar 97) on:
#   - PUMP: the sub and its octave, the lights' strings, the organ and the swarm pad duck under every kick and swell
#     back (the engine's `pump`, keyed from the kick's notes; -5 / -3.5 / -3 dB, 230 ms) - a slow heave in the
#     half-time gear, a throb when the kick goes four-on-the-floor (113). Checked solo: the sub dips 5.4 dB on each
#     kick; the mix's level does not move, because the kick fills the hole it is given. A lane (pm) holds it off until
#     bar 97, so the stretto stays still and the jet's first kick starts the breathing. The voices are not pumped.
#   - A CLAP on every backbeat (the machine's wide clap), into the plate: the snare gets a body with width.
#   - THE HATS RING: the disk hats feed the room, a tail under each tick.
#   - A FLOOR OF SHAKER: from the full-time gear (105) and through the jet's return, stereo sixteenths (the disk hats'
#     kit, a soft pink-noise piece) under the hats - the air stops being events over silence.
PUMP = {"sub": "-5dB", "lift": "-5dB", "lights": "-3.5dB", "e6": "-3dB", "jet": "-3.5dB"}
PUMP_RELEASE = "230ms"
CLAP_GAIN, CLAP_PLATE = "-6dB", "-3dB"
HAT_ROOM = "-8dB"
SHAKER = {"choke": None,
          "patch": {"synth": {"layers": [{"type": "noise", "color": "pink", "pan": -1},
                                         {"type": "noise", "color": "pink", "pan": 1}],
                              "filters": ["hp cutoff=3500", "lp cutoff=11000"],
                              "amp": {"a": "7ms", "d": "60ms", "s": 0, "r": "30ms"}}}}
SHAKER_GAIN = "-21dB"
SHAKER_VEL = (64, 36, 48, 36)


# v100 (ROUND TYPE: whole song - DEEP pass 3, the ARRANGEMENT MAP): WHAT WAS WRITTEN IS HEARD. chirper-two's
# tools/amap.py renders every track alone and asks, window by window, whether it holds a quarter of the mix's power in
# any octave. For t8 it says that of the seven elements 'in stretto', three stop being heard the moment the drums
# enter (bar 65): E3's contrabass chords (21 dB under the mix, 15 dB under its best octave), E5's gamelan and, from
# 81, E6's organ - each was dropped 4-5 dB 'into orbit' after its entry to make room for the next, and the sum buried
# them. And that v99's new parts were written but not heard: the shaker 32 dB under the mix (23 under its octave),
# the clap 10 under its octave, and the two harmony choirs of the jet's chorus 10-12 under (she sang in unison).
#   - E3 PLUCKS ITS CHANGES (track e3p, pizzicato strings): from the drums' entry to the jet, every chord of E3's
#     2+2+3 is plucked as it changes - three plucks to seven beats, a limping pulse AGAINST the drums' four - so the
#     cycle that 'lands on one downbeat at bar 97' can be heard walking toward it. The bowed chords stay under it.
#     It rests while the tide goes out and turns (72-88: the lights leave, the brass arrives) and comes back for THE
#     APPROACH, the last eight bars before the jet (89-96).
#   - THE ORBITS COME IN FOR THE APPROACH: E5, E2 and E6 no longer sit 4-5 dB down until three bars before the jet -
#     at bar 89 they step back up within a bar (to 0, -2 and 0 dB), with the plucks. (Tried on the way: closer from
#     their entries on evened the tide's two blocks, flatness 0.78 -> 0.66; closing in at the turn (81), by ramp or
#     by step, and the plucks returning there, weakened the turn itself as compscore reads it - its boundary at 2:08
#     fell 0.181 -> 0.151 taken together, the plucks -0.023 and the orbits -0.012 apart, under two of the seven
#     thresholds, 99.59 on seed 0. So the turn stays the brass's and the lights', and the approach gets its own stage.)
#   - The jet's HARMONY is sung (choir5 +8 dB, choir8 +9), the CLAP claps (+5) and the SHAKER is a floor (+15) - and
#     the jet ACCRETES as its gears do: half time is kick, snare and one voice; after the four drumless bars the
#     full-time gear (109) returns with the clap and the last line sung in HARMONY; the floor gear (113) brings the
#     sixteenths, hats and shaker together; the return (129) has all of it. (First try, all of it from bar 97 and
#     the plucks straight through: louder parts common to neighbouring 8 s blocks made them more alike - eco's
#     flatness 2:00 0.82 -> 0.70 and 2:48 0.74 -> 0.70, a section boundary lost on seed 0, 99.51.)
#   - 61 Hz +0.8 dB on the master: the added mids and highs had tipped the lows 0.3 dB under the album's band.
E3_PLUCK_FROM = 65
E3_PLUCK_RESTS = (72, 89)                # bars: the tide's ebb and its turn
CLAP_FROM = 105                          # = GEAR_FULL (defined further down)
HARMONY_FROM = 109                       # in the first jet; the return keeps all its harmony
SHAKER_FROM = 113                        # = GEAR_FLOOR: sixteenths arrive with the floor gear, in hats and shaker both
LOW_BAND = "peak cutoff=61 q=1.4 gain=0.8dB"
E3_PLUCK_VEL = (96, 80, 84)              # the cycle's three chords: D minor add9 (2 beats), Bb (2), C (3)
E3_PLUCK_GAIN, E3_PLUCK_HALL = "-14dB", "-10dB"
ORBITS_WERE = {"e5": [["0b", 0.0], ["256b", 0.0], ["272b", -5.0], ["364b", -5.0], ["380b", 0.0]],
               "e2": [["0b", 0.0], ["152b", 0.0], ["160b", -5.0], ["364b", -5.0], ["380b", 0.0]],
               "e6": [["0b", 4.0], ["320b", 4.0], ["336b", -4.0], ["364b", -4.0], ["380b", 0.0]]}
ORBITS_IN = {"e5": [["0b", 0.0], ["256b", 0.0], ["272b", -5.0], ["352b", -5.0], ["356b", 0.0]],
             "e2": [["0b", 0.0], ["152b", 0.0], ["160b", -5.0], ["352b", -5.0], ["356b", -2.0], ["364b", -2.0],
                    ["380b", 0.0]],
             "e6": [["0b", 4.0], ["320b", 4.0], ["336b", -4.0], ["352b", -4.0], ["356b", 0.0]]}
HEARD_DB = {"choir5": 8.0, "choir8": 9.0, "clap": 5.0, "shaker": 15.0}


def the_stretto_is_heard(song):
    by = {x["name"]: x for x in song["tracks"]}
    pos, plucks, k = 0.0, [], 0
    for tok in by["e3"]["score"].split():
        head, _, rest = tok.partition("/")
        ln = float(rest.split("b")[0])
        if head != "R" and b0(E3_PLUCK_FROM) - 1e-6 <= pos < JB - 1e-6:
            assert ln in (2.0, 3.0), tok
            if not b0(E3_PLUCK_RESTS[0]) - 1e-6 <= pos < b0(E3_PLUCK_RESTS[1]) - 1e-6:
                plucks.append((pos, 1.0, head, E3_PLUCK_VEL[k % 3]))
            k += 1
        pos += ln
    assert plucks and abs(plucks[0][0] % 7.0 - JB % 7.0) < 1e-6, plucks[:2]
    claps = [e for e in score_events(by["clap"]["score"]) if e[0] >= b0(CLAP_FROM) - 1e-6]
    by["clap"]["score"] = events_score(claps)
    shakes = [e for e in score_events(by["shaker"]["score"]) if e[0] >= b0(SHAKER_FROM) - 1e-6]
    by["shaker"]["score"] = events_score(shakes)
    for n in ("choir5", "choir8"):
        notes = by[n]["notes"]
        keep = [e for e in notes if not JB - 1.0 <= e["at"] < b0(HARMONY_FROM) - 1.0]
        assert 0 < len(keep) < len(notes), n
        by[n]["notes"] = keep
    eq = song["master"]["fx"][0]
    assert eq["type"] == "eq"
    eq["bands"] = list(eq["bands"]) + [LOW_BAND]
    e3 = by["e3"]
    song["tracks"].append({"name": "e3p", "patch": "pizzicato", "score": events_score(plucks), "gain": E3_PLUCK_GAIN,
                           "pan": json.loads(json.dumps(e3["pan"])), "sends": {"hall": E3_PLUCK_HALL},
                           "auto": {"pn": json.loads(json.dumps(e3["auto"]["pn"]))}})
    for n, pts in ORBITS_IN.items():
        assert by[n]["auto"]["orb"]["points"] == ORBITS_WERE[n], (n, by[n]["auto"]["orb"]["points"])
        by[n]["auto"]["orb"]["points"] = [list(pt) for pt in pts]
    for n, up in HEARD_DB.items():
        by[n]["gain"] = f"{float(str(by[n]['gain']).replace('dB', '')) + up:g}dB"


# v101 (ROUND TYPE: section, the horizon's opening 143-161, 3:44-4:14 - DEEP pass 4, a new sound): HER LAST WORD STAYS.
# The horizon is 'a held light redshifting away', and the light was a synth chord (two saws and a sine through a
# rotary). What an outside observer sees at an event horizon is the last thing that fell in, FROZEN there - never
# crossing, dimming, reddening. The last thing that falls in here is her line, 'I kept your far side' (143.75-146). So
# her last word is frozen: a hall of its own (bus held) hears only the vowel of 'side', on D4, and at that instant
# its `freeze` closes - the tail holds, nothing new gets in - and hangs through the horizon as part of the light, wide
# (left/right correlation -0.1), alive (its level wanders +-3 dB), dims as the elements fall in and is gone before
# the light starts to sink (161). What is frozen is a voice's harmonic series on D: D5 strongest, then D6, A5, D4,
# F#6 - a D major chord, the track's home, made of her (a trace of C#, her scoop into the note, 15 dB under it).
# Tried first: freezing the jet's last bars (choir, flute, strings) - the tail held A B D G F# C at once, the melody's
# notes as a cluster, and bar 140's G chord against the light's F#: a held dissonance, against 'tone is home'.
HELD_WORD = "S AY1 D"                    # the horizon line's last syllable
HELD_OPEN, HELD_FREEZE = 0.35, 0.7       # beats after the note's start: past the s, before her voice falls away
HELD_SEND = "3dB"
HELD_HALL = "reverb kind=hall decay=12s mix=1 width=1 spread=1 freeze=0+auto.fz*1"
HELD_FADE = ((153, 0.0), (157, -4.0), (160, -40.0), (160.5, -90.0))   # bars, dB: dimming as the elements fall in,
#                                          gone a bar before the sink (held to the sink and cut there, it blurred
#                                          the sink's own boundary as compscore reads it: 4:11 0.191 -> 0.155)


def her_last_word_stays(song):
    solo = next(x for x in song["tracks"] if x["name"] == "solo")
    words = [e for e in solo["notes"] if e.get("ph") == HELD_WORD and e["at"] >= b0(HORIZON)]
    assert len(words) == 1 and words[0]["len"] > HELD_FREEZE + 0.3, words
    a, z = words[0]["at"] + HELD_OPEN, words[0]["at"] + HELD_FREEZE
    assert "held" not in song["buses"]
    song["buses"]["held"] = {
        "fx": ["gain gain=0dB+auto.fi*1", HELD_HALL, "hp cutoff=200", "gain gain=0dB+auto.fo*1"],
        "auto": {"fi": {"points": [["0b", -90.0], [f"{a - 0.05:g}b", -90.0], [f"{a:g}b", 0.0], [f"{z:g}b", 0.0],
                                   [f"{z + 0.05:g}b", -90.0]]},
                 "fz": {"points": [["0b", 0.0], [f"{z - 0.01:g}b", 0.0], [f"{z:g}b", 1.0]]},
                 "fo": {"points": [["0b", 0.0]] + [[f"{b0(bar):g}b", db] for bar, db in HELD_FADE]}}}
    solo["sends"] = dict(solo.get("sends") or {}, held=HELD_SEND)


def score_events(score):
    pos, ev = 0.0, []
    for tok in score.split():
        head, _, rest = tok.partition("/")
        ln = float(rest.split("b")[0])
        if head != "R":
            ev.append((pos, ln, head, int(rest.split("@")[1].split("^")[0]) if "@" in rest else 80))
        pos += ln
    return ev


def events_score(ev):
    toks, at = [], 0.0
    ev = sorted(ev)
    for i, (s, ln, h, v) in enumerate(ev):
        ln = min(ln, (ev[i + 1][0] if i + 1 < len(ev) else TOTAL) - s)
        if ln <= 1e-6:
            continue
        if s - at > 1e-5:
            toks.append(f"R/{s - at:.6g}b")
        toks.append(f"{h}/{ln:.6g}b@{v}")
        at = s + ln
    if TOTAL - at > 1e-5:
        toks.append(f"R/{TOTAL - at:.6g}b")
    return " ".join(toks)


def the_jet_breathes(song):
    by = {x["name"]: x for x in song["tracks"]}
    lane = [["0b", 0.0], [f"{JB - 0.05:g}b", 0.0], [f"{JB:g}b", 1.0]]
    for n, depth in PUMP.items():
        tr_ = by[n]
        tr_["fx"] = list(tr_.get("fx") or []) + [{"type": "pump", "on": "kick", "depth": depth, "release": PUMP_RELEASE,
                                                  "curve": 1.0, "mix": {"value": 0, "mod": [{"src": "auto.pm", "amount": 1}]}}]
        tr_["auto"] = dict(tr_.get("auto") or {}, pm={"points": [list(p) for p in lane]})
    # the clap: every backbeat the snare plays from the jet on (the loud hits on a beat), not its builds and ghosts
    claps = [(s, 0.5, "cpw", 100) for s, ln, h, v in score_events(by["snare"]["score"])
             if s >= JB - 1e-6 and v >= 100 and abs(s - round(s)) < 1e-6]
    song["tracks"].append({"name": "clap", "patch": "machine-kit", "score": events_score(claps), "gain": CLAP_GAIN,
                           "sends": {"plate": CLAP_PLATE}})
    by["hatw"]["sends"] = dict(by["hatw"].get("sends") or {}, room=HAT_ROOM)
    # the shaker: sixteenths in every bar from the full-time gear on in which the hats play
    hat_bars = {int(s // BPB) + 1 for s, ln, h, v in score_events(by["hat"]["score"])}
    shk = [(b0(bar) + i * 0.25, 0.25, "s", SHAKER_VEL[i % 4])
           for bar in sorted(hat_bars) if bar >= GEAR_FULL for i in range(16)]
    kit = json.loads(json.dumps(DISK_HATS))
    kit["about"] = "t8's shaker: the disk hats' stereo noise, pink and soft - the floor under the hats"
    kit["kit"] = {"s": {k: v for k, v in json.loads(json.dumps(SHAKER)).items() if v is not None}}
    song["tracks"].append({"name": "shaker", "patch": kit, "score": events_score(shk), "gain": SHAKER_GAIN})


def the_disk_is_wide(song):
    by = {x["name"]: x for x in song["tracks"]}
    pos, ev = 0.0, []
    for tok in by["hat"]["score"].split():
        head, _, rest = tok.partition("/")
        ln = float(rest.split("b")[0])
        if head != "R":
            vel = int(rest.split("@")[1].split("^")[0]) if "@" in rest else 80
            off = pos >= JB and abs((pos % 1.0) - 0.5) < 1e-6           # the jet's off-beats open
            ev.append((pos, 0.5 if off else ln, "o" if off else "c", min(127, round(vel * 1.5))))
        pos += ln
    toks, at = [], 0.0
    for i, (s, ln, h, v) in enumerate(ev):
        ln = min(ln, (ev[i + 1][0] if i + 1 < len(ev) else TOTAL) - s)
        if s - at > 1e-5:
            toks.append(f"R/{s - at:.5g}b")
        toks.append(f"{h}/{ln:.5g}b@{v}")
        at = s + ln
    if TOTAL - at > 1e-5:
        toks.append(f"R/{TOTAL - at:.5g}b")
    song["tracks"].append({"name": "hatw", "patch": DISK_HATS, "score": " ".join(toks), "gain": DISK_HAT_GAIN})
    song["buses"]["plate"] = json.loads(json.dumps(PLATE))
    by["snare"]["sends"] = dict(by["snare"].get("sends") or {}, plate=SNARE_PLATE)
    for n, pan in CHOIR_OUT.items():
        by[n]["pan"] = pan
    dly = song["buses"]["dly"]["fx"]
    assert dly[0].startswith("delay ") and "ping_pong" not in dly[0]
    dly[0] += " ping_pong=true"
    song["master"]["fx"].append(json.loads(json.dumps(WIDE_TOP)))


def she_rides_the_slingshot(song):
    solo = [x for x in song["tracks"] if x["name"] == "solo"][0]
    ou = [n for n in solo["notes"] if n.get("ph") == "AW1" and b0(125.5) <= n["at"] < b0(126.2)]
    rs = [n for n in solo["notes"] if n.get("ph") == "ER0 Z" and b0(126.4) <= n["at"] < b0(126.8)]
    assert len(ou) == 1 and len(rs) == 1, (len(ou), len(rs))
    ou = ou[0]
    ou["ph"] = "AW1 ER0 Z"
    ou["len"] = round(SLINGSHOT_AT[0] - ou["at"], 3)
    notes = [n for n in solo["notes"] if n is not rs[0]]
    for (h, v), a, z in zip(SLINGSHOT_MELISMA, SLINGSHOT_AT, SLINGSHOT_AT[1:]):
        n = {"at": a, "len": round(z - a, 3), "pitch": h, "ph": "_", "vel": v}
        if ou.get("expr"):
            n["expr"] = dict(ou["expr"])
        notes.append(n)
    solo["notes"] = sorted(notes, key=lambda n: n["at"])


def lines_land_on_the_beat(song):
    for tr_ in song["tracks"]:
        if tr_["name"] in SUNG_GLIDES and isinstance(tr_.get("patch"), dict):
            g, semi, lead = SUNG_GLIDES[tr_["name"]]
            p = json.loads(json.dumps(tr_["patch"]))
            p["play"] = dict(p.get("play") or {}, glide=g, glide_semi=semi, glide_lead=lead)
            tr_["patch"] = p


def vowels_live(song):
    for tr_ in song["tracks"]:
        if tr_["name"] in VOWEL_DRIFT and isinstance(tr_.get("patch"), dict):
            p = json.loads(json.dumps(tr_["patch"]))
            p["synth"]["layers"][0]["vowel_drift"] = VOWEL_DRIFT[tr_["name"]]
            tr_["patch"] = p


def space_opens(song):
    hall = song["buses"]["hall"]
    hall["fx"] = list(hall["fx"]) + ["gain gain=0dB+auto.sx*1"]
    hall["auto"] = {"sx": {"points": [[f"{b0(bar) if bar else 0:g}b", v] for bar, v in SPACE]}}


def she_ages_from_the_top(song):
    tr_ = {x["name"]: x for x in song["tracks"]}
    for n in ("solo", "last"):
        p = json.loads(json.dumps(tr_[n]["patch"]))
        p["synth"]["layers"][0]["age_high"] = HER_AGE_HIGH
        tr_[n]["patch"] = p
    lo = b0(MEMORY_AT) - 1e-6
    hi = b0(MEMORY_AT + 4)
    for n in tr_["solo"]["notes"]:
        if lo <= n["at"] < hi and (n.get("expr") or {}).get("age") is None:
            n["expr"] = dict(n.get("expr") or {}, age=MEMORY_AGE)


def lights_doppler(song):
    hold = next(x for x in song["tracks"] if x["name"] == "hold")
    pts = [["0b", 1.0]]
    for bar, v in LIGHT_SPIN:
        pts += [[f"{b0(bar) - 0.01:g}b", pts[-1][1]], [f"{b0(bar):g}b", v]]
    hold["fx"] = [LIGHT_ROTARY] + list(hold.get("fx") or [])
    hold["auto"] = dict(hold.get("auto") or {}, lr={"points": pts})


def her_own_rate(song):
    tr_ = {x["name"]: x for x in song["tracks"]}
    lo, hi = b0(HER_LINES[0]), b0(HER_LINES[1])
    notes = [n for n in tr_["solo"]["notes"] if lo <= n["at"] < hi] + tr_["last"]["notes"]
    for n in notes:
        if n.get("expr_path") and n.get("ph") in PATH_SUNG_S:
            n["path_len"] = f"{PATH_SUNG_S[n['ph']]:.3f}s"


# v84 (ROUND TYPE: section, the horizon's start 138-149, 3:36-3:52; rewritten): THE JET LETS GO, THEN SHE REMEMBERS.
# Seed 0's flattest change left (3:44, 0.68, bars 138-148 by flatness --bars: blocks 138.4-143.65 and 143.65-148.6),
# with 3:52 (0.70) beside it. Her remembered line (v79) began at 142.5 and straddled the boundary, so both blocks were
# 'her voice over the held light'; and the jet's sub, its last G1 at 140, rang on into the horizon at -3.4. Now the
# jet lets go AT the horizon: the sub's tail fades in half a beat at 141 (its own lane; the horizon's quiet D1 carries
# the floor); the held light hangs alone for two and three-quarter bars, no voice - the jet gone, the light left; and
# she remembers from 143.75, the line whole inside the next block, then the hook, then her last line.
JET_LETS_GO = 141


def jet_lets_go(song):
    sub = next(x for x in song["tracks"] if x["name"] == "sub")
    a = b0(JET_LETS_GO)
    # a NEW list: breathe() hands every BREATHE_IN track the same br points list (extending it in place faded the
    # held light, the hook and the choirs too - caught by presence before rendering)
    sub["auto"] = dict(sub["auto"], br={"points": [list(p) for p in sub["auto"]["br"]["points"]]
                                         + [[f"{a - 0.25:g}b", 0.0], [f"{a + 0.5:g}b", -40.0]]})


def she_remembers(song):
    solo = next(x for x in song["tracks"] if x["name"] == "solo")
    at0 = b0(MEMORY_AT)
    for on, pitch, ph, ln, vel, f0 in MEMORY_LINE:
        n = {"at": round(at0 + on * MEMORY_PACE, 3), "len": round(ln * MEMORY_PACE, 3), "pitch": pitch, "ph": ph,
             "vel": round(vel * MEMORY_SOFT, 3)}
        if f0:
            n["expr_path"] = {"f0": f0}
        solo["notes"].append(n)
    solo["notes"].sort(key=lambda n: n["at"])


def answer_accretes(song):
    far = next(x for x in song["tracks"] if x["name"] == "far")
    for bar, cell, vel in ANSWERS:
        at = b0(bar)
        for pitch, ln in cell:
            far["notes"].append({"at": at, "len": ln, "ph": "UW1", "pitch": pitch, "vel": vel})
            at += ln
    far["notes"].sort(key=lambda n: n["at"])


def fall_in_lanes(song):
    for tr_ in song["tracks"]:
        n = tr_["name"]
        if n not in FALL_IN_DB:
            continue
        a, z = b0(FALL_IN[n]), b0(FALL_IN[n] + 4)
        pts = [["0b", 0.0], [f"{a - 1:g}b", 0.0], [f"{a:g}b", FALL_IN_DB[n]], [f"{z + 4:g}b", FALL_IN_DB[n]], [f"{z + 6:g}b", 0.0]]
        tr_["fx"] = list(tr_.get("fx") or []) + ["gain gain=0dB+auto.fw*1"]
        tr_["auto"] = dict(tr_.get("auto") or {}, fw={"points": pts})


# v81 (ROUND TYPE: section, the fall-in 153-161, 4:00-4:20; rewritten): THE LIGHT GOES OUT FOR THE AMEN. The
# flattest change left in t8 (4:08, 0.64 / 0.70, bars 153-161 by flatness --bars: two 8 s blocks either side of bar
# ~157) - the fall-in, where the light (the held chord, its lift, the horizon sub) shone on unbroken while the
# afterimages fell in around it, so the two blocks layered the same things. Now the light goes out for four bars
# (153-156) - a long echo of its flicker at 147 - and the far answer's last note, E3's amen (its G, the IV) and the
# choir sound in the dark; at 157 the light comes back on its redshift step, redder, and holds into the sink, where
# it sinks to D at 161 - the amen's I.
LIGHT_OUT = (153, 157)


def light_out_for_the_amen():
    lo, hi = b0(LIGHT_OUT[0]), b0(LIGHT_OUT[1])
    for n in MOVE_TRACKS["L"]:
        out = []
        for s, ln, h, v in P[n].ev:
            if lo - 1e-6 <= s < hi - 1e-6:
                if s + ln > hi + 1e-6:
                    out.append((hi, s + ln - hi, h, v))
                continue
            if s < lo - 1e-6 < s + ln:
                if s + ln > hi + 1e-6:
                    out.append((hi, s + ln - hi, h, v))
                ln = lo - s
            out.append((s, ln, h, v))
        P[n].ev = sorted(out)


def everything_falls_in():
    b = b0(FALL_IN["e7"])
    for i, (n, _, _) in enumerate(E7):
        part("e7").add(b + i, 6.0 - i, n, 84)
    b = b0(FALL_IN["e6"])
    part("e6").add(b, 4.0, "m50,m54,m57,m64", 92)                      # D(add9): D F# A E
    part("e6").add(b + 4, 4.0, "m48,m52,m55,m62", 84)                  # C(add9): C E G D
    b = b0(FALL_IN["e5"])
    for n, s in E5:
        part("e5").add(b + s * 0.5, 0.5, n, 72 if s == 0 else 60)
    b = b0(FALL_IN["e2"])
    for rep in range(2):
        for n, s, v in E2:
            part("e2").add(b + rep * 1.75 + s * 0.25, 0.5, "F#4" if n == "F4" else n, v)
    b = b0(FALL_IN["e1"])
    for n, on, ln in E1:
        part("e1").add(b + on * 2, ln * 2, n, 80)


# v57 (ROUND TYPE: whole song): THE ARRANGER'S HAND. Harry (6 Nov): every 8-16 bars something should move - a fill, a
# drop-out, a counter-line, a re-voicing - and no ~30 s may pass unchanged. t8 accretes (an element enters every few
# phrases) and then holds: the measure finds ten still blocks across the whole song - the stretto's start (0:24-0:40),
# E3's entry (1:04-1:20), the tide (1:52, 2:08) and the jet's middle (2:40-2:56). Now the last two bars of EVERY eight-
# bar phrase move, one of three ways, chosen for what is playing: A the floor lifts (bass and snare out - the sub
# stays, and the KICK keeps time: with the kick out too, the onset tempo estimate flipped 156 -> 87.9 bpm, exactly
# t4's, and compscore's distinct term read t8 as a 0.965 copy of t4 - -2.3), B the orbits climb (the chip, the glock and the gamelan an OCTAVE UP for the two bars - E1, E2, E5: a register shift; cutting them
# instead removed the song's sixteenth-note pulse and flipped the tempo estimate too), C the lights go out. Bars
# already shaped by earlier rounds are left alone (the opening, the kick rest 73-80, the hook's rest 81-84, the
# stretch and the vacuum 89-96, the jet's arrival, the hook sung back 109-112, the break, the horizon). Several land
# under her questions (40, 64), which get the room.
PHRASE_MOVES = {23: "D", 31: "C", 39: "A", 47: "B", 55: "C", 63: "A", 71: "D", 87: "C", 103: "D", 117: "B", 135: "A"}   # v63: 103 A -> D (the stop follows)
MOVE_TRACKS = {"A": ("bass", "kick", "snare"), "B": ("e1", "e2", "e5"), "C": ("lights",), "D": ("e1", "e2", "e5"),
               "L": ("hold", "lift", "hsub")}
# v71 (ROUND TYPE: whole song): THE ARRANGER'S HAND, ALL THE WAY DOWN. The hand's moves stopped at 135 - and the two
# places still flat were exactly where it never reached: the jet's second half (2:40-2:56: under the choir the sub, the
# lift, the kit and the bass unbroken) and the horizon (3:44-4:00: the held light, its lift and the horizon sub
# unbroken from 141 to the convergence). Now it reaches the horizon: at 147 a new move, L - THE
# LIGHT FLICKERS: the held light, its lift and the horizon sub go out for two bars, the afterimages (the hook's
# flute, E7's brass) alone in the dark, and the light comes back at 149 on v70's redshift step, a shade redder, just
# before her last line.
PHRASE_MOVES.update({147: "L"})       # (tried with 115 A too: the jet's 2:48 window went flatter, 0.59 -> 0.54)
# v60 (ROUND TYPE: whole song): REAL DROP-OUTS. v57 had to soften its moves - cutting the ostinatos (and the kick)
# flipped compscore's onset tempo onto t4's and 'distinct' called t8 a copy (-2.3) - so B became an octave climb and
# the kick stayed. eco fixed distinct (declared tempos, 8 Nov 06:03); the cuts, which took flatness 28% -> 19% on both
# seeds, are open again. Now four moves: A the floor lifts (bass, KICK and snare out - the sub stays), B the orbits
# REST (E1, E2, E5 out), C the lights go out, and D the orbits climb (v57's octave, kept for variety); B and D
# alternate (climbs at 23 and 71, rests at 47 and 117). The rest at 47-48 - the orbits falling silent as E3 enters -
# is the move that matters: with a climb there instead, the 1:04-1:12 blocks stayed still (0.45 / 0.54) and the song
# sat at 25% flat; with the rest they clear (1.07 / 0.94) and the song falls to 19% on both seeds.


def up_octave(h):
    out = []
    for x in h.split(","):
        out.append(f"m{int(x[1:]) + 12}" if x[:1] == "m" and x[1:].isdigit() else name_of(midi(x) + 12))
    return ",".join(out)


def arrangers_hand():
    for bar, kind in PHRASE_MOVES.items():
        lo, hi = b0(bar), b0(bar + 2)
        if kind == "D":
            for n in MOVE_TRACKS[kind]:
                P[n].ev = [(s, ln, up_octave(h), v) if lo - 1e-6 <= s < hi - 1e-6 else (s, ln, h, v) for s, ln, h, v in P[n].ev]
            continue
        for n in MOVE_TRACKS[kind]:
            out = []
            for s, ln, h, v in P[n].ev:
                if lo - 1e-6 <= s < hi - 1e-6:
                    continue
                if s < lo - 1e-6 < s + ln:
                    if kind == "L" and s + ln > hi + 1e-6:          # v71: the light comes BACK after its flicker
                        out.append((hi, s + ln - hi, h, v))
                    ln = lo - s
                out.append((s, ln, h, v))
            P[n].ev = sorted(out) if kind == "L" else out


# v58 (ROUND TYPE: section, the stretch 89-96, 2:18-2:30): TIME STRETCHES. The 2:08 block was the stillest in the song
# (0.37): the stretch - v49's 'stretched thin', everything pulled toward the jet - was only heard in its last two bars
# (the high-pass lane reached 20 Hz by the half). Now the fall is felt in TEXTURE and in TIME: the floor drains from
# the stretch's first bar (stretch_lane), and from 93 the stretto's own clocks run slow - the chip's, the glock's and
# the gamelan's sixteenths (E1, E2, E5) at HALF SPEED while the kick keeps time, as a clock falling toward a horizon
# runs slow to the one watching. The vacuum (96) and the jet are untouched.
# v63 (ROUND TYPE: section, the jet 105-108, 2:42-2:49): THE JET STOPS FOR THE WORDS. The jet held one texture from
# its arrival to the break - kit, bass, the stretto's remnants under the choir - and its middle was still on both
# seeds (2:40 0.48 / 0.45, 2:48 0.57 / 0.58). There the choir sings the album's arrival in words - 'we were the far
# side', E8 at last - and it was sung over the full band. Now the band STOPS for it: on the crash at 105 the kit, the
# bass and the stretto's remnants (E2, E5) fall silent, and the arrival is sung over the floor, the lights, the horns'
# column and the hook alone; at 109 everything slams back in with the hook sung back. (The arranger's 103 floor lift
# became an octave climb so the stop is not doubled.) A texture contrast between windows - t4's lessons (v59, v59b).
JET_STOP = (105, 108)
STOP_TRACKS = ("kick", "snare", "hat", "bass", "e2", "e5")


# v67 (ROUND TYPE: section, the run-in to the jet 85-92, 2:12-2:30; rewritten): THE APPROACH QUICKENS. The stretto's
# last eight bars before the stretch were a drone in time - one kick a bar, the hat's dotted eighths, the bass's D2
# pairs every seven sixteenths, no snare - so the 8 s window at 2:08 read the flattest in the song (0.39). Harry: the
# complexity in TIME. Now the kick doubles every two bars into the jet - once a bar (85-86), half notes (87-88),
# quarters (89-90), eighths (91-92), rising 80 -> 104 - before the time dilates (93-95) and the vacuum (96) holds
# it; the hat steps out for 85-88 (E7's brass has the light) and returns at 89 as the pulse doubles.
QUICKEN = {85: 1, 86: 1, 87: 2, 88: 2, 89: 4, 90: 4, 91: 8, 92: 8}
QUICKEN_HAT_REST = (85, 89)


# v72 (ROUND TYPE: section, the jet's middle 105-116, 2:42-3:00; rewritten): THE FLOOR FALLS AWAY, THEN LIFTS OFF.
# The jet's middle stayed flat on both seeds (2:40 0.53 / 0.55, 2:48 0.59 / 0.61) through every move above it - v63
# stopped the kit and bass for 'we were the far side', the choir falls silent after 'and it was ours' - because the
# floor never moved: the sub (-4) and the lift (-7) walk E4's roots a bar at a time from the jet's arrival to the
# break. Now the floor moves with the words: under 'we were the far side' (105-108) the sub falls away too - the
# album's arrival in words sung nearly weightless, the lift alone below it; everything slams back at 109 (as before);
# and after 'and it was ours' the jet LIFTS OFF (113-116): the sub and the lift rise an octave for four bars, the
# floor itself climbing, before it settles for the jet's last bars into the break.
FLOOR_FALLS = (105, 109)
FLOOR_LIFTS = (113, 117)


# v75 (ROUND TYPE: section, the opening body 17-28, 0:24-0:44; rewritten): THE FIRST FLOOR. After the t7 seam the
# song states the album's hook alone - E1 on the chip over E4's lights, nothing else, for twelve bars - and the 8 s
# windows at 0:24 and 0:32 read flat on seed 0 (0.56, 0.68: a 24 s run). Now the twelve bars accrete in fours: 17-20
# as they were (t8's head at the seam - the in-seam window - untouched); 21-24 the lights go out, the chip's hook
# bare (the arranger's octave climb at 23 inside it); 25-28 the lights return and t8's FLOOR arrives for the first
# time - a soft D1 pedal on the jet's own sub, a pre-echo of the jet's floor - under her first question and E2's
# entry at 29.
FIRST_DARK = (21, 25)
FIRST_FLOOR = (25, 29)
FIRST_FLOOR_VEL = 12                  # at 70 the pedal (-0.1) buried the hook itself (E1 -12.9, unheard)


# v86 (ROUND TYPE: section, the approach 82-97, 2:08-2:32; rewritten): THE WELL. t8's flattest change left (2:16,
# 0.75 / 0.71, bars 82-92 by flatness --bars; blocks 82.4-87.6 and 87.6-92.9) - v85's rotor spin-down at 87.4 did not
# move it: the organ sits at -18.5, and under both blocks ran one floor, the bass's D2 ostinato unbroken from the tide
# to the jet. Now, AT 87.5, the floor sinks into the gravity well: the bass's ostinato drops an octave (D2 -> D1)
# through the stretch, the slowing clocks (93) and the vacuum, the kick already doubling (87) - and at the jet (97)
# it comes back up to D2 with the light. (Spectrum checked first: t8's lowest bands have room - 38 Hz -2.5, 44 Hz -4.5.)
WELL = (87.5, 97)


def octave_down(h):
    base, _, art = h.partition("^")                         # keep the articulation (the palm mute, ^pm)
    m = int(base[1:]) if base.startswith("m") else midi(base)
    return name_of(m - 12) + ("^" + art if art else "")


# v91 (ROUND TYPE: section, the horizon's memory 143-153, 3:44-4:00; rewritten): THE MEMORY FLOATS. t8's least-moving
# change (3:52, 0.76 / 0.74, bars 143-153 by flatness --bars; blocks 143.65-148.6 and 148.6-153.2): her remembered
# line (young, 143.75) and the hook, then her last line (old, 149.5) - and under both the horizon's sub held D1 (struck
# at 141 for six bars, again at 149). Now, when she starts remembering, the floor lets go: the horizon's D1 ends at
# 143.75, so her young voice and the flute's hook float over the light alone - and the floor comes back at 149 with
# her last line. (Spectrum checked: t8's 38 Hz band sits at -2.5 dB, room to spare.)
MEMORY_FLOATS = 143.75


def memory_floats():
    a = b0(MEMORY_FLOATS)
    out = []
    for s, ln, h, v in P["hsub"].ev:
        if s < a < s + ln - 1e-6:
            ln = a - s
        out.append((s, ln, h, v))
    P["hsub"].ev = out


def the_well():
    a, z = b0(WELL[0]), b0(WELL[1])
    P["bass"].ev = [(s, ln, octave_down(h) if a - 1e-6 <= s < z - 1e-6 else h, v) for s, ln, h, v in P["bass"].ev]


# v93 (ROUND TYPE: section, the jet's second half 109-121, 2:48-3:04; rewritten): THE WELL PULLS AGAIN. t8's least-
# moving change (2:56, 0.77 / 0.82, bars 108-119 by flatness --bars; blocks 108.5-113.8 and 113.8-119.1): the jet at
# full drive in both - the choirs' line and E7's brass in the first, the flute's hook and busier hats in the second,
# over the same high floor (the bass in the D3 register). Now, from 114 to the break, the well pulls again: the bass
# drops an octave as it did before the jet (v86, 87.5-97), so the jet's second half leans down into the break. And the
# spectrum asked for it: t8's 61 Hz band sits on the album envelope's edge (-6.0 dB) with 97 and 114 low too, while
# 156 Hz is +3.2 over - the octave moves the bass's weight from the full band into the starved one.
WELL_AGAIN = (114, 121)


# v97 (ROUND TYPE: section, the jet's second half 114-121, 2:56-3:10; rewritten): THE JET RUNS OUT OF ROAD. t8's
# least-moving change is still 2:56 (0.81 / 0.81; blocks 108.5-113.8 and 113.8-119.1). Presence: the sub (-2.7 / -1.4)
# and the drums lead both; the first block has the choirs' line (-3.7), the second NO voice - the jet running on its
# engine alone into the break, the snare on its backbeat to the last half-bar fill. Now the jet runs out of road: from
# 114 the snare builds - every beat, then eighths (117), then sixteenths (119), then a thirty-second roll (120.5) -
# rising into the break, where time dilates. A build adds snare-band energy and takes nothing from t8's starved
# 60-115 Hz (compscore --bands: 61 Hz on the envelope's edge).
ROAD = [(114, 117, 1.0, (78, 78)), (117, 119, 0.5, (74, 100)), (119, 120.5, 0.25, (66, 104)), (120.5, 121, 0.125, (84, 120))]


def out_of_road():
    a, z = b0(ROAD[0][0]), b0(ROAD[-1][1])
    keep = [e for e in P["snare"].ev if not (a - 1e-6 <= e[0] < z - 1e-6)]
    new = []
    for lo, hi, step, (v0, v1) in ROAD:
        s, e = b0(lo), b0(hi)
        n = int(round((e - s) / step))
        for i in range(n):
            at = s + i * step
            v = 104 if (step >= 0.5 and abs((at % 4) - 1) < 1e-6 or abs((at % 4) - 3) < 1e-6) else round(v0 + (v1 - v0) * i / max(1, n - 1))
            new.append((at, step, "s", v))
    P["snare"].ev = sorted(keep + new, key=lambda e: e[0])


def the_well_again():
    a, z = b0(WELL_AGAIN[0]), b0(WELL_AGAIN[1])
    P["bass"].ev = [(s, ln, octave_down(h) if a - 1e-6 <= s < z - 1e-6 else h, v) for s, ln, h, v in P["bass"].ev]


def first_floor():
    a, z = b0(FIRST_DARK[0]), b0(FIRST_DARK[1])
    out = []
    for s, ln, h, v in P["lights"].ev:
        if a - 1e-6 <= s < z - 1e-6:
            continue
        if s < a - 1e-6 < s + ln:
            ln = a - s
        out.append((s, ln, h, v))
    P["lights"].ev = out
    part("sub").add(b0(FIRST_FLOOR[0]), b0(FIRST_FLOOR[1]) - b0(FIRST_FLOOR[0]), "D1", FIRST_FLOOR_VEL)


def jet_floor():
    a, z = b0(FLOOR_FALLS[0]), b0(FLOOR_FALLS[1])
    P["sub"].ev = [e for e in P["sub"].ev if not (a - 1e-6 <= e[0] < z - 1e-6)]
    a, z = b0(FLOOR_LIFTS[0]), b0(FLOOR_LIFTS[1])
    for n in ("sub", "lift"):
        P[n].ev = [(s, ln, up_octave(h), v) if a - 1e-6 <= s < z - 1e-6 else (s, ln, h, v) for s, ln, h, v in P[n].ev]


def approach_quickens():
    lo, hi = b0(min(QUICKEN)), b0(max(QUICKEN) + 1)
    P["kick"].ev = [e for e in P["kick"].ev if not (lo - 1e-6 <= e[0] < hi - 1e-6)]
    bars = sorted(QUICKEN)
    for i, bar in enumerate(bars):
        n = QUICKEN[bar]
        for k in range(n):
            v = int(round(80 + 24 * (i * n + k) / (len(bars) * n)))
            part("kick").add(b0(bar) + k * 4.0 / n, 0.5, "k", v)
    a, z = b0(QUICKEN_HAT_REST[0]), b0(QUICKEN_HAT_REST[1])
    P["hat"].ev = [e for e in P["hat"].ev if not (a - 1e-6 <= e[0] < z - 1e-6)]


def the_jet_stops():
    lo, hi = b0(JET_STOP[0]), b0(JET_STOP[1] + 1)
    for n in STOP_TRACKS:
        out = []
        for s, ln, h, v in P[n].ev:
            if lo - 1e-6 <= s < hi - 1e-6:
                continue
            if s < lo - 1e-6 < s + ln:
                ln = lo - s
            out.append((s, ln, h, v))
        P[n].ev = out


DILATE = (93, 95)                    # the material of 93-94 stretched over 93-95 (the vacuum bar 96 stays empty)
DILATE_TRACKS = ("e1", "e2", "e5")


def time_dilates():
    a, z, stop = b0(DILATE[0]), b0(DILATE[1] + 1), b0(VACUUM)
    for n in DILATE_TRACKS:
        keep, slow = [], []
        for s, ln, h, v in P[n].ev:
            if a - 1e-6 <= s < z - 1e-6:
                ns = a + 2 * (s - a)
                if ns < stop - 1e-6:
                    slow.append((round(ns, 4), min(2 * ln, stop - ns), h, v))
                continue
            keep.append((s, ln, h, v))
        P[n].ev = keep + slow


def tide_surfaces():
    lo, hi = b0(KICK_REST[0]) - 1e-6, b0(KICK_REST[1] + 1) - 1e-6
    P["kick"].ev = [e for e in P["kick"].ev if not lo <= e[0] < hi]


def hook_breathes():
    lo, hi = b0(HOOK_REST[0]) - 1e-6, b0(HOOK_REST[1] + 1) - 1e-6
    P["e1"].ev = [e for e in P["e1"].ev if not lo <= e[0] < hi]


def e7_light_lane():
    a, z = b0(T_LIFT[0]), b0(T_LIFT[1] + 1)
    return [["0b", 0.0], [f"{a - 0.5:g}b", 0.0], [f"{a:g}b", E7_LIGHT_DB], [f"{z - 1:g}b", E7_LIGHT_DB], [f"{z:g}b", 0.0]]


def mute_until_the_jet():
    P["bass"].ev = [(s, ln, h + "^pm" if s < b0(JET) - 1e-6 and "^" not in h else h, v) for s, ln, h, v in P["bass"].ev]


def stretto_turns():
    carve(["lights"], *T_DROP)
    carve(["bass"], *BASS_DROP)
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
    # the D pedal everything shares (the triangle bass), in E2's rhythm, from 33 - v90 (ROUND TYPE: section, the stretto's
    # first turn 31-41, 0:48-1:04; rewritten): THE FLOOR ARRIVES ON THE TURN. t8's least-moving change (0:56, 0.75 /
    # 0.76, bars 31-41 by flatness --bars; blocks 31.1-36.1 and 36.1-41.2) held one texture: E1's chip and E2's glock
    # turning over the lights, the pedal arriving at 33 inside the first block. Now the two clocks turn alone over the
    # lights for a whole block, and the floor arrives ON the turn, at 36 (still on E2's phase) - then E3 at 41.
    beat = phase_start("E2", PEDAL_IN)
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
# v53 (ROUND TYPE: whole song): THE QUESTION FINDS ITS WORDS. Her six questions - the rising half step E5 -> F5 that
# the jet's E F# D answers - opened from a hum to an open mouth across the song (v43) but always on 'oo': she never
# said anything, and the choir at the jet answered 'We were the far side' to a question nobody had spoken. Now, as
# her mouth opens, the question finds its words: 'oo' while she hums (28, 40), 'ah' as the lips part (52), 'far...'
# (64), 'far si-' broken off (80), and at the vacuum, mouth fully open, 'far side?' (96) - and the jet answers, and
# the choir sings it back: 'We were the far side'. The thread t4's chorus started ('I kept your far side'), asked
# aloud. Pitches, timing, levels (hum_even) unchanged.
ASK_WORDS = [("UW1", "UW1"), ("UW1", "UW1"), ("AA1", "AA1"), ("F AA1 R", "AA1"), ("F AA1 R", "S AY1"),
             ("F AA1 R", "S AY1 D")]

# v16 (ROUND TYPE: whole song): THE HOOK'S LIFE. The hook was heard often but never grew: E1 on the chip in the
# stretto, then the flute's plain statement every two bars through both jets, the same way about twenty times, then
# an echo on the chip at the horizon. Now it has a life across the song: born on the chip in the stretto, found by
# the flute at the jet (where the choir sings it into E8), SUNG BACK IN THIRDS after the dilated break - a second
# flute a diatonic third below, in D mixolydian, so the tune grows into harmony for the second jet - and at the
# horizon its last statement is the flute's, three times slower: the hook's own voice saying goodbye.
MIXO = [0, 2, 4, 5, 7, 9, 10]              # D mixolydian, semitones above D


# v35 (ROUND TYPE: palette - a voice no Accretion track uses): SUNG BACK. After the break the hook was 'sung back in
# thirds' (v16) - by a second flute: two flutes in thirds through the slingshot (129-140), on top of the flute that
# carries the hook and the flute that asks. Now it is SUNG: wM's FOF SOPRANO (Rodet's CHANT voice, one grain per
# formant per pitch period, an open 'a' with a 5.5 Hz vibrato) sings the hook a tenth below the flute - B4 F#5 A5 E5
# C5, her sweet spot (the flute's third, two octaves up, sat at B5-A6, too high to sing). A third voice character in
# t8 beside the bright choir and the warm solo: the hook, after the breath of the break, comes back with a singer.
def third_below(m):
    """The diatonic third below m in D mixolydian (m in the scale; off-scale notes drop four semitones)."""
    pc = (m - 62) % 12
    if pc not in MIXO:
        return m - 4
    i = MIXO.index(pc)
    j = i - 2
    oct_shift = -12 if j < 0 else 0
    return m - pc + MIXO[j % 7] + oct_shift


# v36 (ROUND TYPE: palette - the question gets its singer): THE QUESTION IS SUNG. The minor shadow of the arrival,
# E F, was asked six times through the stretto by a flute (28, 40, 52, 64, 80 and alone in the vacuum, 96) - the
# same flute as the hook. The solo voice asks it at the very start (E, then E F E); now she asks it every time: the
# flute's E5 F5 on an 'oo', a little louder and a little further into head voice each time (register 0.3 -> 0.7),
# the last question alone in the vacuum - and the choir answers it at the jet with the arrival, E F# D. One voice
# asks, many answer. (The ask track stays, silent, so the track order does not move.)
def write_asks():
    return


def sung_asks():
    out = []
    for i, bar in enumerate(ASKS):
        k = i / (len(ASKS) - 1)
        reg, v = round(0.3 + 0.4 * k, 3), round(0.34 + 0.16 * k, 3)       # placed where the flute sat
        hum = round(1.0 - k, 3)                                            # v43: closed at first, open by the jet
        v = round(min(1.0, v + ASK_HUM_LIFT * hum), 3)                    # a high closed hum loses ~15 dB (measured)
        p1, p2 = ASK_WORDS[i]                                              # v53: the question finds its words
        out.append({"at": float(b0(bar)), "len": 1.5, "ph": p1, "pitch": "E5", "vel": v, "expr": {"reg": reg, "hum": hum}})
        out.append({"at": float(b0(bar) + 1.5), "len": 2.25 if bar != VACUUM else 2.4, "ph": p2, "pitch": "F5",
                    "vel": round(v + 0.03, 3), "expr": {"reg": reg, "hum": hum}})
    return out


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
                    part("hook3").add(t + on * 1.6, ln * 1.6, name_of(third_below(midi(n) + HOOK_UP) - 12), 86)
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
    echo("e3", E3_LIGHT_CELL, a + 14, 2, 0, 88, CONVERGE)   # v64: E3 in the light, its last G held into the convergence
    #                                                       (at 72 the held G - the IV of the amen - sat at -12, unheard)
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
ORBIT_BOOST = {"e3": 4.0, "e6": 4.0}   # dB in the element's own spotlight (e6: v52)


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


# v48 (ROUND TYPE: whole song): THE DISK TURNS. v10 had each element 'sink into orbit' as the next arrived - but only
# in level: from 41 to the jet every element stood still in space (v25's swings for E1 and E2 ended at 41). Now an
# element that sinks into orbit ORBITS: from the bar it leaves its spotlight (e2 41, e3 53, e5 65, e6 81; E1, the
# hook, a small circle from 41), each turns around its place in the stereo field on its own period - the outer
# slower (e2 six bars a turn, e3 five, e5 four, e6 three, E1 eight) - with the far half of every turn 3 dB further
# away (a gain lane in step with the pan: 'We were the far side'). And as matter does falling in, every orbit
# speeds up (to a quarter of its period) and shrinks (radius to 0) toward the jet, where all of them reach the
# centre at once: the cycles converge at the crest, in space. The element in its spotlight stays still - the newest
# is the one in front - and so does E7, the axis (v24). Motion in space, not pitch (Harry: complexity in time and
# texture).
DISK = {"e1": (41, 8.0, 0.25), "e2": (41, 6.0, 0.55), "e3": (53, 5.0, 0.5), "e5": (65, 4.0, 0.5), "e6": (81, 3.0, 0.45)}
DISK_KEPLER = 0.75                     # the period shrinks by this fraction by the jet
FAR_DB = -3.0                          # the far half of a turn
FAR_FX = "gain gain=0dB+auto.fs*1"


def disk(name, amount=1.0):
    """Pan (scaled for the track's mod amount) and far-side gain lanes for one element's orbit, from its start to the
    jet: radius fading in over 4 bars and shrinking to 0 at the jet, period shrinking by DISK_KEPLER."""
    import math as _m
    start_bar, p0, r0 = DISK[name]
    start, stop = b0(start_bar), b0(JET)
    pn, fs, beat, ph = [], [], start, 0.0
    while beat < stop - 1e-6:
        u = (beat - start) / (stop - start)
        r = r0 * min(1.0, (beat - start) / (4 * BPB)) * (1 - u) ** 0.6
        pn.append([f"{beat:g}b", round(r * _m.sin(ph) / amount, 3)])
        fs.append([f"{beat:g}b", round(FAR_DB * (r / r0) * (1 - _m.cos(ph)) / 2, 2)])
        ph += 2 * _m.pi * 0.5 / (p0 * BPB * (1 - DISK_KEPLER * u))
        beat += 0.5
    pn.append([f"{stop:g}b", 0.0])
    fs.append([f"{stop:g}b", 0.0])
    return pn, fs


def disk_auto(name, before=None, amount=1.0):
    pn, fs = disk(name, amount)
    start = b0(DISK[name][0])
    head = [p for p in (before or [["0b", 0.0]]) if float(p[0][:-1]) < start - 1e-6]
    return {"pn": {"points": head + pn}, "fs": {"points": [["0b", 0.0]] + fs}}


def disk_pan(place):
    return {"value": place, "mod": [{"src": "auto.pn", "amount": 1.0}]}


# v49 (ROUND TYPE: section, the spiral 89-96 into the jet, ~13 s - with 81-88 the stillest block left, 2:08 at
# 0.37; rewritten): STRETCHED THIN. The approach was one loud band (kick, E1, bass, E7, the lights at -6 to -10)
# whose doubled speed at 89 (v24) the ear hears as the same wall. Near a horizon tidal forces stretch whatever falls
# in, so now the spiral STRETCHES THIN: over its eight bars a high-pass rises under the floor of the band - bass,
# sub, kick, the lights, E3 and E6 - from 10 Hz to 226 Hz (4.5 octaves, even per octave), the low end draining
# away while the orbits quicken and close on the centre (v48), until only the bright cells are left spinning; and
# the jet's downbeat slams the whole floor back. (10 Hz is transparent to everything else: at 20 Hz it shaved ~1 dB
# off the jet's A0.)
STRETCH = (89, 96)
STRETCH_OCT = 4.5
STRETCH_FX = "hp cutoff=10+auto.sp*1"


def stretch_lane():
    a, z = b0(STRETCH[0]), b0(STRETCH[1] + 1)
    # v58: the drain starts AUDIBLY (v49's lane reached only an octave - 20 Hz - by the half: nothing heard until the
    # last two bars); now an octave at once and evenly to STRETCH_OCT, ~67 Hz by the half, the floor thinning bar by bar
    return [["0b", 0.0], [f"{a - 0.01:g}b", 0.0], [f"{a:g}b", 1.0], [f"{z - 1:g}b", STRETCH_OCT], [f"{z - 0.01:g}b", STRETCH_OCT],
            [f"{z:g}b", 0.0]]


# v54 (ROUND TYPE: whole song): ROOM TO BREATHE. compscore --bands: the whole song ran 4-6 dB HOT from 468 to 1404 Hz
# (the stretto's chip, organ, marimba, brass, choirs and her voice all live there) and 6-7 dB SHORT at 44-114 Hz and
# 3-6 dB short above 6.7 kHz - a boxy middle on headphones and speakers alike, the floor and the air the album has
# elsewhere missing. Now the master gives the mix room: a wide 3 dB dip centred at 850 Hz (q 0.6, the hump's span),
# the floor up 3 dB below 100 Hz, the air shelf 4 -> 5 dB. Loudness is normalised to -11 LUFS after it, so nothing
# gets louder - the balance moves. Every part is as it was; the song sounds less like it is played in a box.
ROOM_BANDS = ["lowshelf cutoff=100 gain=2dB", "peak cutoff=850 q=0.6 gain=-1.5dB"]   # half: full strength split
# v74 (ROUND TYPE: whole song): FULL RANGE, NOT A SCOOP. After t4 v69 (warm and open: +0.37) t8's own bands read the
# same shape milder - the floor short at 97-114 Hz (-4.6), the mids heavy (340 Hz-1.4 kHz +4..+5), the top short
# (6-15 kHz -3..-6.6, 14.8 kHz beyond tolerance). v54's lesson (below) rules out a deeper mid dip - the song's changes
# live in those mids. So only the edges move: a focused lift at 105 Hz (+2 dB, Q 1.2 - the band t8 lacks AND the
# band t7's tail out-weighs t8's head in at the seam) and an air shelf above 11 kHz (+3 dB). The mids are left alone.
ROOM_BANDS = ROOM_BANDS + ["peak cutoff=105 q=1.2 gain=2dB", "highshelf cutoff=11000 gain=1.5dB"]   # air at +3: seed 0's
#   t7 seam 3.00 -> 3.09 dB (past flow's 3.0 edge, -0.015) while seed 11 rose +0.059 - half the air
# the seeds (100.0 / 99.72: the t7 seam's spectral gap 2.6 -> 3.4) and read 31% / 28% flat (19% / 19%) - the song's
# changes live in those mids
MASTER_AIR = "5dB"


# v17 (ROUND TYPE: whole song): HOME AT THE END. The horizon's held light sank 5 semitones on the redshift lane, so
# the record's last chord was A major - the dominant, away from home (Harry: tone is home). Now the light redshifts a
# full OCTAVE and lands on D again, an octave down: it falls all the way and arrives home - and the sub stays on D1
# underneath, the floor the light falls toward (it used to sink to A0 under everything). Also: E3's bass roots in its
# spotlight softer (vel 92 -> 76; they were the loudest thing there, -2.1).
REDSHIFT = -12.0
# v95 (ROUND TYPE: section, the horizon's last bars 161-177, 4:24-4:56; rewritten): THE ARRIVAL, LAST. After E1's
# farewell (161-162.75) the horizon is one held chord sinking for some 14 bars - the hold, the choir's 'ah', the lift,
# the sub - and nothing new enters. E8, the arrival (E F# D), is the album's resolution; the far choir hums it once at
# 152, answering her last line. Now it answers once more, from inside the sink: the same hum, twice as slow (time
# dilating at the horizon) and softer, E (165) F# (166) and a D held under the dying chord - and SINKING WITH IT (the far
# choir's patch already routes auto.rs to pitch; its lane now follows the hold's), so the arrival is the last thing
# redshifting away with the light.
ARRIVAL_LAST = [(656, 4, "E4"), (660, 4, "F#4"), (664, 24, "D4")]
ARRIVAL_LAST_VEL = 0.3
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


# v70 (ROUND TYPE: whole song): THE LIGHT CHANGES COLOUR. The album is an accretion disk, and t8 its fall to the
# horizon - but its light (E4's four lights on the strings, all song; the held light of the horizon) kept one colour
# from first bar to last, and 'a held light redshifting away' was only the pitch sink after 161. Now the light's
# COLOUR is the song's arc (one octave lane on a low-pass, as recede() darkens): it starts warm and dim (2.5 octaves
# down, ~2.8 kHz), opens steadily as matter falls in - BLUESHIFT - to white at the jet (97), holds open through the
# jet and the break, and through the horizon REDSHIFTS in four audible steps (145, 149, 153, 157: 0.75 octave each,
# to ~2 kHz) before the pitch sink and recede take it the rest of the way.
SHIFT_TRACKS = ("lights", "hold")
SHIFT_START = -2.5
SHIFT_STEPS = [(145, -0.75), (149, -1.5), (153, -2.25), (157, -3.0)]


def light_shift_lane():
    pts = [["0b", SHIFT_START], [f"{b0(JET):g}b", 0.0]]
    prev = 0.0
    for bar, oct_ in SHIFT_STEPS:
        pts += [[f"{b0(bar) - 0.05:g}b", prev], [f"{b0(bar):g}b", oct_]]
        prev = oct_
    return pts


def light_shifts(song):
    for tr_ in song["tracks"]:
        if tr_["name"] in SHIFT_TRACKS:
            tr_["fx"] = list(tr_.get("fx") or []) + ["lp cutoff=16000+auto.zs*1"]
            tr_["auto"] = dict(tr_.get("auto") or {}, zs={"points": light_shift_lane()})


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


# v34 (ROUND TYPE: palette - a song-own patch for the jet): THE JET LOCKS. The jet's two chords (E7's stacked fifths,
# D3 A3 E4 B4 F#5: four bars at the jet, two at the slingshot) were a stock supersaw, the genre's most generic climax.
# Now they are a KURAMOTO SWARM of t8's own - twelve detuned saws per note, pulled toward their mean phase - whose
# coupling RISES on an auto lane across each chord: under the impact the jet is a crowd, a wide detuned roar; over the
# next bars the saws fall into step and the chord LOCKS into pure tone, and as they agree the low-pass opens (sync):
# the jet focuses. The album's 'cycles converging at the crest', heard inside the sound itself. (Tested: harmonic share
# 0.63 as a crowd -> 1.00 locked as coupling rises 0 -> 3. t2 uses wM's kuramoto-choir, whose LFO rocks the coupling
# back and forth; this one only converges.)
JET_SWARM = {"about": "t8's jet: a Kuramoto swarm whose coupling rises on auto.cp - a crowd that locks into one tone",
             "play": {"poly": 8},
             "synth": {"amp": {"a": "250ms", "d": 0, "r": "2s", "s": 1},
                       "filters": [{"kind": "lp", "cutoff": {"value": 900, "mod": [{"src": "sync", "amount": 2.5}]}}],
                       "layers": [{"type": "kuramoto",
                                   "kuramoto": {"count": 12, "spread": 40,
                                                "coupling": {"value": 0.0, "mod": [{"src": "auto.cp", "amount": 1.0}]}}}]},
             "fx": [{"type": "reverb", "kind": "plate", "decay": "2.2s", "mix": 0.2}]}


def swarm_lane():
    pts = [["0b", 0.0]]
    for bar, rise in ((JET, 10.0), (BREAK[1] + 1, 6.0)):
        a = b0(bar)
        pts += [[f"{a - 0.01:g}b", 0.0], [f"{a + 2:g}b", 0.0], [f"{a + 2 + rise:g}b", 3.0], [f"{a + 2 + rise + 4:g}b", 3.0],
                [f"{a + 2 + rise + 4.01:g}b", 0.0]] if bar == JET else \
               [[f"{a - 0.01:g}b", 0.0], [f"{a + 1:g}b", 0.0], [f"{a + 1 + rise:g}b", 3.0]]
    return pts


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


# v55 (ROUND TYPE: palette - an engine feature the album has not used: wM's VIB_SPREAD, pinned da77da08): EVERY SINGER
# HER OWN. t8 has the album's biggest choirs - the jet's choir (four singers and the third above), its fifth and its
# octave below (three each), the far choir humming on 'n' (four), the closing choir of the horizon - and every one of
# their singers wobbled on the lead's vibrato in exact lockstep, the section moving as one voice (the synth-choir
# tell). Now each singer reads the vibrato her own way (rate +-8%, any phase, depth +-30%): the section's vibratos
# drift in and out of step and partly cancel, as a real choir's do (wM measured: the loudness wobble at the vibrato
# rate halves, the held note's pitch swing narrows 39 -> 23 cents). The lead line keeps its vibrato; the soloist is
# untouched. Most audible on the held notes: the jet's 'we were the far side', the break, the horizon's long 'ah'.
VIB_SPREAD = 1.0
# v59 (ROUND TYPE: palette - two changes). (1) wM's VOWEL_SPREAD (pinned a1f7f0ec), vib_spread's partner: each other
# singer in every choir section shapes the vowel her own way (F1/F2 +-8%, F3 +-5%) instead of the lead's formants
# scaled - with v55's own vibratos, a section rather than one voice copied. (2) E7 ON REAL HORNS: the jet's element is
# a column of stacked fifths (D3 A3 E4 A4 E5) - a horn call - and it rang on a saw-and-pulse synth (brass-synth), the
# loudest thing in the hook's rest (85-88, -4.4). Now a physical horn-and-trombone section (brass, unused on the album:
# three players' lips on their bores, blooming), so the fifths sound as the call they are: E7 carried, transformed.
VOWEL_SPREAD = 1.0
# v61 (ROUND TYPE: whole song): THE CHOIRS STAND IN A ROOM. With v55's own vibratos and v59's own vowels, t8's choirs
# were sections of different singers - all standing on one line, every seam's consonant landing as one click (the
# jet's 'we were the Far Side'). Now wM's last two section features (both pinned: DEPTH_SPREAD 391d8713, CONS_SPREAD
# 935354c9): each other singer stands her own distance back (later up to 15 ms, quieter, darker the further back) and
# takes each joined syllable a little after the lead (up to 30 ms). And the room is used: the jet's choirs stand NEAR
# (depth 0.5 - size, rows behind the front), the far choir humming on 'n' stands FAR (depth 1, and 2 dB more hall) -
# the answer forming at a distance, the arrival close.
DEPTH_NEAR, DEPTH_FAR, CONS_SPREAD = 0.25, 1.0, 1.0      # near 0.5 darkened the jet choir's air: -0.020 / -0.016
FAR_HALL = "-1dB"
E7_PATCH, E7_GAIN = "brass", "-11dB"


# v66 (ROUND TYPE: palette - the newest engine feature): THE CHOIRS BREATHE OUT. Every choir phrase in t8 ended at full
# tone and stopped together, square - the section never ran out of air. wM's TAPER (pinned 251180c1): on a joined
# line the phrase's LAST note keeps full tone for its first 30%, then lets go - quieter, darker, breathier, sagging a
# few cents - and 'the whole section lets go together'. Now on the choirs: the jet's choir and its fifth and low
# parts at 0.5, the far choir's hummed answers at 0.8 (far voices fade further). Not her questions (the solo): a
# question rises and must not sag; her last line has its own full let-go (v65).
CHOIR_TAPER, FAR_TAPER = 0.5, 0.8
# v76 (ROUND TYPE: whole song): HOW EACH VOICE ENTERS. wM's ATTACK (pinned 10254007) shapes how a sung phrase starts on
# a vowel - breathy below 0, glottal above. Every voice in t8 began alike. Now each enters as what it is in the story:
# the jet's choir (and its fifth and low parts) pressed and sure (+0.5: 'all of it falls into the light' lands with the
# jet's force); the far choir's hummed answers out of air (-0.6: distance); her questions a little breathy (-0.3:
# tentative); her last line, 'and it was ours', blooming out of the deep breath before it (-0.7).
CHOIR_ATTACK, FAR_ATTACK, SOLO_ATTACK, LAST_ATTACK = 0.5, -0.6, -0.3, -0.7

# v73 (ROUND TYPE: palette): THE UNDERTOW ON GUT AND HORSEHAIR. E3 - t3's storm undertow, here the stretto's low line
# and (v64) the album's last cadence, its G held into the convergence for the plagal amen - played on a synthetic saw
# section (strings-synth). Now it is BOWED: the library's physical contrabass, arco ('a deep, grainy bowed bass with a
# slow-speaking stroke'), in its mix-ready opt-in form contrabass-tight (lows narrowed below 200 Hz; unused on the
# album - t6's farbow has the plain one). The amen is now a real bow on a real body. (Refused at 17:58 as v69: the
# slow bow ran the cell and its held G into one sustain and seed 11's 4:00 window - then 0.001 over the threshold -
# joined a 32 s flat run; since v71's flicker the horizon around it moves, so the run cannot form.)
E3_PATCH, E3_GAIN = "contrabass-tight", "-16dB"


def choir_patch(singers, tract=0.92, third=False, depth=None):
    pt = json.loads(json.dumps(VOICE8))
    pt["about"] = f"t8's choir part: {singers} singers on one line, even vowels, joined, a breath before each phrase"
    pt["synth"]["layers"][0].update({"singers": singers, "spread": 0.7, "detune": 0.12, "even": 1.0, "tract": tract,
                                     "together": True, "breath": {"value": 0.34, "mod": [{"src": "vel", "amount": -0.2}]},
                                     "vib_spread": VIB_SPREAD, "vowel_spread": VOWEL_SPREAD,    # v55, v59
                                     "depth_spread": DEPTH_NEAR if depth is None else depth, "cons_spread": CONS_SPREAD,  # v61
                                     "taper": CHOIR_TAPER, "attack": CHOIR_ATTACK})             # v66, v76
    if third:
        # v15 (ROUND TYPE: palette - an engine feature the album had not used: harmony in a key, pin 8e25c1a9): the
        # lead's line is sung again a THIRD above IN THE KEY (D Mixolydian, the jet's E4 v2 - D9 Cmaj9 Am11 G6/9),
        # note by note - so the jet's choir is a full, consonant triad (root, third, fifth) over the octave below,
        # where it was open fifths. Harry: harmony in key, thirds and sixths. The horizon's last line stays one voice.
        pt["synth"]["layers"][0].update({"harmony": [2], "harmony_key": "D mixolydian"})
    return pt


# v68 (ROUND TYPE: whole song): EVERY BREATH THE SIZE OF ITS LINE. Every voice in t8 drew the same breath before every
# phrase - her two-word questions and the jet's long choir lines alike. wM's INHALE_DEPTH (pinned df7aaf1b; chirper-
# zero and chirper-three asked) sizes each breath to the phrase it starts (and half the line before): a short phrase
# takes a sip (down to -6 dB, at least 80 ms), a long one a full breath (up to +3.5 dB, longer). Now on every voice -
# the choirs (in VOICE8, so all of choir_patch and the far choir), her questions and lines (her inhale up 0.45 -> 0.6
# so the sizing is heard), and her last line (inhale 0.7, v65). The song whose brief is 'the voice sings full lines'
# now breathes for each one.
VOICE8["synth"]["layers"][0]["inhale_depth"] = 1.0
SOLO_INHALE = 0.6

SOLO8 = json.loads(json.dumps(VOICE8))
SOLO8["synth"]["layers"][0]["inhale"] = SOLO_INHALE
SOLO8["synth"]["layers"][0]["attack"] = SOLO_ATTACK                     # v76
SOLO8["about"] = "t8's last voice: the choir's lead alone, even vowels - the horizon's last line"
SOLO8["synth"]["layers"][0]["even"] = 1.0
SOLO8["synth"]["layers"][0]["register"] = "expr.reg"                 # v30: chest -> head voice across the last line
SOLO8["synth"]["layers"][0]["age"] = "expr.age"                      # v40: she grows old across the song (age_her)
SOLO8["synth"]["layers"][0].update({"hum": "expr.hum", "hum_at": "m"})   # v43: THE MOUTH OPENS (see below)
# v50 (ROUND TYPE: whole song): ONE VOICE, OPEN OR CLOSED. Her mouth opens across the song (v43: the hummed opening
# line, the six questions opening from hum 1 to 0, the open lines after) - but a closed hum is physically quieter,
# by up to ~29 dB high (wM, E5), so the arc was also a level arc that v43 patched with a velocity lift by hand
# (ASK_HUM_LIFT 0.5) and the opening line had none. wM's HUM_EVEN (pinned 1d916569, asked for this) holds the hum at
# the open voice's loudness, tracking both (~20 ms), so now she is ONE voice at one presence whether her mouth is
# open or closed - the opening line as present as the words that follow, the questions opening without swelling -
# and the lift is gone. Only her: the far choir (hummed on 'n', meant far) and the closing choir (closing to a hum,
# meant to recede) keep the physical hum. Her vowels are already even (even 1.0), as wM advises under a hum.
SOLO8["synth"]["layers"][0]["hum_even"] = 1.0
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
    e7_tightens()
    full_throttle()
    hook_sung_back()
    hook_breathes()
    tide_surfaces()
    arrangers_hand()
    time_dilates()
    the_jet_stops()
    approach_quickens()
    jet_floor()
    first_floor()
    the_well()
    memory_floats()
    the_well_again()
    out_of_road()
    everything_falls_in()
    light_out_for_the_amen()
    lead, fifth, low = choir()
    far = far_choir()                                             # v38: the answer forms far away (v45: own track)
    lead, fifth, low, hers = she_says_it(lead, fifth, low)       # v47: the break's second line is hers alone
    solo = age_her(sorted(hummed(opening_voice()) + sung_asks() + hers + horizon_line(), key=lambda d: d["at"]))   # v36: she asks                      # v12: the last line, one voice alone (v21: and the first)
    lead += [{"at": b0(HORIZON + 16), "len": b0(BARS + 1) - b0(HORIZON + 16) - 4, "pitch": "D4", "vel": 0.6}]   # the held 'ah'
    tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": f"{b0(17):g}b", "bpm": SEAM_IN},    # v42: t7's overlap held flat
             {"at": f"{b0(VACUUM):g}b", "bpm": INFALL, "ramp": True},             # v42: the orbits quicken inward
             {"at": f"{b0(JET) - 0.25:g}b", "bpm": VAC_BPM, "ramp": True},        # v42: time freezes at the threshold
             {"at": f"{b0(JET):g}b", "bpm": INFALL},                              # v42: the jet fires at that speed
             {"at": f"{b0(BREAK[0]):g}b", "bpm": INFALL},                         # v11: time dilation in the
             {"at": f"{b0(BREAK[0] + 4):g}b", "bpm": DILATED, "ramp": True},      # break, then the slingshot
             {"at": f"{b0(BREAK[1] - 1):g}b", "bpm": DILATED},
             {"at": f"{b0(BREAK[1] + 1):g}b", "bpm": INFALL, "ramp": True},
             {"at": f"{b0(HORIZON):g}b", "bpm": INFALL},
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
               fx=[{"type": "filter", "kind": "peak", "cutoff": 230, "q": 0.9, "gain": "-5dB"}, STRETCH_FX],
               auto={"sp": {"points": stretch_lane()}}),
            tr("e1", "nes-pulse-lead", gain="-10dB", pan={"value": -0.25, "mod": [{"src": "auto.pn", "amount": 0.6}]},
               sends={"dly": "-12dB"}, fx=[FAR_FX], auto=disk_auto("e1", orbit_pan(ENTRY["E1"], 5.0, 1.0), 0.6)),   # v25, v48
            tr("e2", "modal-glock", gain="-16dB", pan={"value": 0.35, "mod": [{"src": "auto.pn", "amount": 0.6}]},
               sends={"dly": "-14dB"}, fx=[ORBIT_FX, FAR_FX],
               auto={"orb": {"points": orbit_lane("e2")}, **disk_auto("e2", orbit_pan(ENTRY["E2"], 7.0, -1.0), 0.6)}),   # v25, v48
            tr("e3", E3_PATCH, gain=E3_GAIN, pan=disk_pan(-0.1), sends={"hall": "-8dB"}, fx=["lp cutoff=1800", ORBIT_FX, FAR_FX, STRETCH_FX],
               auto={"orb": {"points": orbit_lane("e3")}, **disk_auto("e3"), "sp": {"points": stretch_lane()}}),
            tr("e5", E5_PATCH, gain=E5_GAIN, pan=disk_pan(0.2), sends={"room": "-10dB"},
               fx=[ORBIT_FX, FAR_FX], auto={"orb": {"points": orbit_lane("e5")}, **disk_auto("e5")}),
            tr("bass", "bass-pick-di", gain="1dB", fx=["lowshelf cutoff=110 gain=10dB", "lp cutoff=1500", "gain gain=0dB+auto.bm*1", STRETCH_FX],
               auto={"bm": {"points": [["0b", -4.5], [f"{b0(JET):g}b", -4.5], [f"{b0(JET) + 0.01:g}b", 0.0]]}, "sp": {"points": stretch_lane()}}),
            tr("sub", "sub-saturated", gain="-12dB", fx=[STRETCH_FX], auto={"sp": {"points": stretch_lane()}}),                       # v28: the staple sine -> saturated
            tr("hsub", HSUB, gain="-13dB", auto={"rs": {"points": horizon_lane(0.0)}}),     # v17: the floor stays home
            tr("kick", "machine-kit", gain="-8dB", fx=[STRETCH_FX], auto={"sp": {"points": stretch_lane()}}),
            tr("snare", "machine-kit", gain="0dB", sends={"room": "-10dB"}),
            tr("hat", "nes-noise-hat", gain="-12dB", pan=0.25),
            tr("crash", "machine-kit", gain="2dB", pan=-0.2),
            tr("riser", "fx-revcym", gain="-12dB"),
            tr("impact", "fx-impact", gain="-10dB"),
            {"name": "choir", "patch": closing_choir(choir_patch(4, third=True)), "gain": "-7dB", "sends": {"hall": "-7dB", "dly": "-16dB"},
             "notes": lead, "auto": {"rs": {"points": horizon_lane(REDSHIFT)}, "hm": {"points": closing_lane()}}},
            {"name": "choir5", "patch": choir_patch(3), "gain": "-13dB", "pan": 0.3, "sends": {"hall": "-6dB"}, "notes": fifth,
             "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            {"name": "choir8", "patch": choir_patch(3, tract=1.0), "gain": "-12dB", "pan": -0.3, "sends": {"hall": "-6dB"}, "notes": low,
             "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            tr("hold", HOLD, gain="-18dB", sends={"hall": "-4dB"},
               auto={"rs": {"points": horizon_lane(REDSHIFT)}, "cl": {"points": cl}}),
            tr("e6", "organ", gain="-24dB", pan=disk_pan(-0.3), sends={"hall": "-8dB"}, fx=["lp cutoff=3500", ORBIT_FX, FAR_FX, STRETCH_FX],
               auto={"orb": {"points": orbit_lane("e6")}, **disk_auto("e6"), "sp": {"points": stretch_lane()}}),
            tr("e7", E7_PATCH, gain=E7_GAIN, pan=0.15, sends={"dly": "-12dB", "hall": "-10dB"},
               fx=["gain gain=0dB+auto.sl*1"], auto={"sl": {"points": e7_light_lane()}}),   # v51
            {"name": "jet", "patch": JET_SWARM, "gain": "-9dB", "sends": {"hall": "-6dB"}, "notes": JET_NOTES,
             "auto": {"cp": {"points": swarm_lane()}}},                                     # v34: the swarm locks
            tr("hook", "flute", gain="-6dB", pan=0.1, sends={"dly": "-14dB", "hall": "-12dB"}),   # v5
            {"name": "solo", "patch": SOLO8, "gain": "-7dB", "sends": {"hall": "-5dB", "dly": "-16dB"},   # v12 (last)
             "notes": solo, "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},
            tr("ask", "flute", gain="-9dB", pan=-0.15, sends={"hall": "-6dB", "dly": "-12dB"}),   # v14
            tr("hook3", "fof-soprano", gain="-11dB", pan=-0.2, sends={"dly": "-14dB", "hall": "-10dB"}),  # v35
            tr("lift", SUB8, gain="-22dB"),                                 # v18: the sub's octave you can hear
            {"name": "far", "patch": far_patch(), "gain": FAR_GAIN, "pan": -0.1, "sends": {"hall": FAR_HALL},
             "notes": far + [{"at": a, "len": ln, "ph": "UW1", "pitch": h, "vel": ARRIVAL_LAST_VEL}
                             for a, ln, h in ARRIVAL_LAST],
             "auto": {"rs": {"points": horizon_lane(REDSHIFT)}}},       # v45 (last): the far choir, hummed; v95 sinks
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.8s mix=1 predelay=6ms", "hp cutoff=200"]},
                  "hall": {"fx": ["reverb kind=hall decay=4s mix=1 predelay=24ms", "hp cutoff=180"]},
                  "dly": {"fx": ["delay time=3/8 mix=1 feedback=0.32", "hp cutoff=400", "lp cutoff=6000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=240 q=0.8 gain=-2dB",
                                                   "highshelf cutoff=6000 gain=" + MASTER_AIR] + ROOM_BANDS},
                          {"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "8ms",
                           "release": "120ms", "makeup": "0dB"}]},
    }
    recede(song)
    light_shifts(song)
    breathe(song)
    fall_in_lanes(song)
    answer_accretes(song)
    and_it_was_ours(song)
    the_tide_turns(song)
    held_notes_open(song)
    she_remembers(song)
    jet_lets_go(song)
    her_own_rate(song)
    lights_doppler(song)
    she_ages_from_the_top(song)
    space_opens(song)
    vowels_live(song)
    lines_land_on_the_beat(song)
    she_rides_the_slingshot(song)
    the_disk_is_wide(song)
    the_jet_breathes(song)
    the_stretto_is_heard(song)
    her_last_word_stays(song)
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print(f"wrote {OUT} bars {BARS} jet {JET} (beat {JB}) choir notes {len(lead)}")


if __name__ == "__main__":
    main()
