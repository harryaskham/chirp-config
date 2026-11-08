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
    pt["synth"]["layers"][0].update({"hum": 1.0, "hum_at": "n"})
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
MOVE_TRACKS = {"A": ("bass", "kick", "snare"), "B": ("e1", "e2", "e5"), "C": ("lights",), "D": ("e1", "e2", "e5")}
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
                    ln = lo - s
                out.append((s, ln, h, v))
            P[n].ev = out


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
# the seeds (100.0 / 99.72: the t7 seam's spectral gap 2.6 -> 3.4) and read 31% / 28% flat (19% / 19%) - the song's
# changes live in those mids
MASTER_AIR = "5dB"


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


def choir_patch(singers, tract=0.92, third=False, depth=None):
    pt = json.loads(json.dumps(VOICE8))
    pt["about"] = f"t8's choir part: {singers} singers on one line, even vowels, joined, a breath before each phrase"
    pt["synth"]["layers"][0].update({"singers": singers, "spread": 0.7, "detune": 0.12, "even": 1.0, "tract": tract,
                                     "together": True, "breath": {"value": 0.34, "mod": [{"src": "vel", "amount": -0.2}]},
                                     "vib_spread": VIB_SPREAD, "vowel_spread": VOWEL_SPREAD,    # v55, v59
                                     "depth_spread": DEPTH_NEAR if depth is None else depth, "cons_spread": CONS_SPREAD})  # v61
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
    everything_falls_in()
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
            tr("e3", "strings-synth", gain="-16dB", pan=disk_pan(-0.1), sends={"hall": "-8dB"}, fx=["lp cutoff=1800", ORBIT_FX, FAR_FX, STRETCH_FX],
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
             "notes": far, "auto": {"rs": {"points": [["0b", 0.0]]}}},       # v45 (last): the far choir, hummed
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
    breathe(song)
    fall_in_lanes(song)
    answer_accretes(song)
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print(f"wrote {OUT} bars {BARS} jet {JET} (beat {JB}) choir notes {len(lead)}")


if __name__ == "__main__":
    main()
