#!/usr/bin/env python3
"""chirpers - Accretion (chirpers IX), track 4 (chirper-three): THE WARM THIRD. Relief: the first orbit closes.

t3's storm falls into t4 at 108 bpm holding D (its E3 begins on D minor). t4 LENSES it: the residue of the storm's
D minor chord hangs over the seam, and at bar 9 its third lifts - F to F# - and the first of E4's FOUR LIGHTS (D9)
takes the chord over. From there E4 is the clock: one chord per E1 cycle (5 beats), D9 / Bbmaj13#11 / Am11 / D9sus,
20 beats a turn, its changes falling across the 4/4 bar lines and meeting the bar every 5 bars.

DIFFICULT -> REWARDING, the relief's way: E1 (t1's seed, D A C G E, 5 beats) ASSEMBLES ITSELF on a handpan - one note
more every two cycles - until the cell is whole; the groove (half time, brushes) comes in beside it; and at bar 81,
where E1's 5-beat cycle, E4's 20-beat turn and the 4/4 bar all meet one downbeat (320 beats = 16 turns), THE VOICE
sings: a human voice, warm and close (the album's first person), four lines on E1 augmented and then retrograded,
coming home on D. The first full statement of the combined theme. The last 16 bars hand E1-E4 into t5 at 112.

E2 and E3 are carried as they are posted in compose/chirpers9/motifs.md (E3 here first as the storm's residue).
Writes songs/chirpers9-t4.yaml (or T4_OUT). Original music.
"""
import math
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("T4_OUT", os.path.join(ROOT, "songs", "chirpers9-t4.yaml"))
TAKES = json.load(open(os.path.join(HERE, "chirpers9-t4-takes.json")))["takes"]

BARS, BPB = 136, 4
TOTAL = BARS * BPB
SEAM_IN, SEAM_OUT = 108, 112          # mixplan: t3>t4 108, t4>t5 112, flat across each 16-bar overlap
SECTIONS = [("lens", 1, 16), ("A", 17, 40), ("B", 41, 64), ("rise", 65, 80), ("crest", 81, 100),
            ("relief", 101, 120), ("fall", 121, 136)]
CREST = 81                            # E1 (5), E4 (20) and the bar (4) all meet here: beat 320 = 16 turns of E4
LIFT = 9                              # the bar the storm's third lifts (F -> F#)


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
            name, _, arts = head.partition("^")                         # v32: articulations go after @vel
            toks.append(f"{name}/{ln:.5g}b@{vel}" + (f"^{arts}" if arts else ""))
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks) if toks else f"R/{total:g}b"


P = {}


def part(n):
    return P.setdefault(n, Part())


# ---------------------------------------------------------------- the elements
# E1, the seed (chirper-zero, t1): D A C G E in 5 beats - (note, onset beat, length)
E1 = [("D4", 0.0, 0.5), ("A4", 0.5, 0.75), ("C5", 1.25, 0.25), ("G4", 1.5, 1.0), ("E4", 2.5, 1.0)]
E1_CYCLE = 5.0
# E4, four lights (this track): one chord per E1 cycle
# v6 (ROUND TYPE: whole; Harry 6 Nov 00:30 - 'atonal, very tough listening... missing catchiness/hook'; album direction
# 'tone is home'): E4 v2. The four lights were D9 | Bbmaj13#11 | Am11 | D9sus - a borrowed Bb and F against the F#, an E
# (#11) over the Bb. Now all four sit in D MIXOLYDIAN, the scale E1 itself implies (its C is natural): D9 | Cmaj9 | Am11 |
# G6/9 - the bass walks down D C A G and comes home G -> D (plagal), one chord per E1 cycle as before.
E4 = [("D9", ("D2", "A2", "F#3", "C4", "E4")),
      ("Cmaj9", ("C2", "G2", "E3", "B3", "D4")),
      ("Am11", ("A1", "E2", "C3", "G3", "B3", "D4")),
      ("G6/9", ("G1", "D2", "B2", "E3", "A3"))]
E4_CYCLE = 20.0
# E3, the storm's progression (chirper-two, t3) - here only its first chord, the residue the relief lifts
STORM_DM = ("D3", "A3", "E4", "F4")


def chord_at(beat):
    """E4's chord sounding at a beat (index, name, voicing)."""
    k = int((beat % E4_CYCLE) // E1_CYCLE)
    return (k,) + E4[k]


def head(notes):
    return ",".join(notes)


# ---------------------------------------------------------------- parts
def write_lens():
    # the storm's residue: t3's D minor (add9) hangs over the seam; at LIFT its F lifts to F# and fades into D9
    for bar in range(1, LIFT):
        v = 64 - (bar - 1) * 3
        part("residue").add(b0(bar), BPB, head(STORM_DM), v)
    lifted = ("D3", "A3", "E4", "F#4")
    part("residue").add(b0(LIFT), 4 * BPB, head(lifted), 50)
    # the first light: D9 alone, swelling in from the lift to the end of the lens
    part("lights").add(b0(LIFT), b0(17) - b0(LIFT), head(E4[0][1]), 52)
    # v11 (ROUND TYPE: section, the lens 1-16; rewritten): THE WARM THIRD, BENT. (1) The floor - agreed with
    # chirper-two for the t3 seam: the sine holds t3's low D (D1) through the residue, rises an octave with the
    # chord at the lift, and fades out by bar 24, so the low end steps down across the seam instead of falling off it.
    # (2) The lift made audible: a pedal steel sings A4 - F4 and BENDS the minor third up to the major (F -> F#4, a
    # slow 700 ms glide) at the lift, the album's turn from minor to major and the song's title, then settles E4 - D4
    # as E1's full statement begins.
    for bar, note, v in ((1, "D1", 38), (5, "D1", 34)):
        part("sub").add(b0(bar), 4 * BPB - 0.05, note, v)
    for bar, v in ((LIFT, 36), (13, 30), (17, 24), (21, 18)):
        part("sub").add(b0(bar), 4 * BPB - 0.05, "D2", v)
    line = ((5, 2, "A4", 70), (7, 2, "F4", 74), (LIFT, 4, "F#4", 80), (13, 2, "E4", 70), (15, 2, "D4", 66))
    for i, (bar, bars, note, v) in enumerate(line):
        tie = 0.1 if i + 1 < len(line) else -0.25                # touching notes glide (the steel is mono legato)
        part("steel").add(b0(bar), bars * BPB + tie, note, v)


def write_lights():
    vel = {"A": 62, "B": 70, "rise": 76, "crest": 92, "relief": 82, "fall": 60}
    beat = b0(17)
    while beat < b0(BARS + 1) - 0.01:
        bar = int(beat // BPB) + 1
        s = sec_of(bar)
        v = vel[s] + (min(14, (bar - 65) * 1) if s == "rise" else 0)
        if s == "fall":
            v = max(24, vel["fall"] - 6 - (bar - 121) * 2)
        k, name, notes = chord_at(beat)
        if s == "fall":
            notes = E4[0][1]                      # v6: the fall holds the first light alone (the lens mirrored; no
        part("lights").add(beat, E1_CYCLE, head(notes), v)   # second chord against t5's head)
        beat += E1_CYCLE


def write_felt():
    # E4 broken into eighths, rising through each voicing then turning, from B to the fall
    for i in range(int((b0(121) - b0(41)) / 0.5)):
        beat = b0(41) + i * 0.5
        bar = int(beat // BPB) + 1
        k, name, notes = chord_at(beat)
        pos = int(round((beat % E1_CYCLE) / 0.5))           # 0..9 within the chord
        seq = list(notes[1:]) + list(reversed(notes[2:-1]))
        n = seq[pos % len(seq)]
        n = n[:-1] + str(int(n[-1]) + 2)                    # v13: two octaves up - the glock rings above the band
        v = 44 + (8 if pos == 0 else 0) + (10 if sec_of(bar) == "crest" else 0)
        part("felt").add(beat, 0.5, n, v)


# v12 (ROUND TYPE: whole song; voice batch 2 pinned - 65c7745c): THE VOICE IS THE THROUGH-LINE. It sang only at the
# crest; now it accretes inside the song: in B it HUMS E1 - the hook, on 'oo', in unison with the handpan, on alternate
# cycles (a verse before words) - at the crest it finds the words, and in the relief it hums the hook again after the
# last lines (hum -> words -> hum). E1's notes touch, so each hum is one joined breath; 'even' keeps the held 'oo' level
# with the band. The duet a third above comes down 3 dB (it sat only 4 dB under the lead).
# v13 (ROUND TYPE: palette): the FELT PIANO (piano-muted - a dark, mid instrument; the song's spectrum ran +9 dB hot
# at 750-877 Hz and 10-17 dB short above 7 kHz) becomes a GLOCKENSPIEL (unused on the album): the same E4 broken into
# eighths an octave up, now a pure ringing ping above the band - the four lights glittering - 10 dB lower so the
# constant eighths glitter rather than glare (presence in B about -15).
# v35 (ROUND TYPE: section, A's first phrase 17-24 plus its hand-off, ~27 s; rewritten): THE FIRST HUM. The song's
# voice - 'the voice at its most human so far' - was silent for its first 100 seconds (her first hum at bar 46), and
# A's first phrase was the handpan's E1 over lights, sub and bass, a loop (flatness 0.54-0.64 there). Now, as A
# begins (17), she enters very softly, humming one long note per light down the chords' thirds - F#4 over D9, E4
# over Cmaj9, C4 over Am11, B3 over G6/9 - and comes home to D4 over the next D9, held and fading as the clarinet
# takes the hook (96); then she is silent again until B. The human voice arrives under the hook in the first phrase.
# On its own track (hum1), closed-mouthed: little breath and a 4 kHz low-pass - the open voice's air there read +28 dB
# at 15 kHz against t3's body and cost the t3 -> t4 seam (flow 82.3 -> 76.3).
FIRST_HUM = [(64, 5, "F#4", 0.42), (69, 5, "E4", 0.46), (74, 5, "C4", 0.48), (79, 5, "B3", 0.46), (84, 10, "D4", 0.40)]


def hum1_patch():
    """Her voice, closed-mouthed: little breath (the open voice's air read +28 dB at 15 kHz against t3's body)."""
    p = json.loads(json.dumps(VOICE))
    p["synth"]["layers"][0]["breath"] = 0.12
    p["synth"]["layers"][0].pop("taper", None)            # v61: the t3 seam's stand-in keeps its square ends
    return p


def first_hum():
    return [{"at": float(at), "len": float(ln), "ph": "UW1", "pitch": f"m{midi_of(n)}", "vel": v}
            for at, ln, n, v in FIRST_HUM]


def hums():
    out = []
    beat = 0.0
    while beat < b0(121) - 0.01:
        bar = int(beat // BPB) + 1
        cyc = int(round(beat / E1_CYCLE))
        if cyc % 2 == 0 and ((sec_of(bar) == "B" and beat >= b0(45)) or (beat >= b0(108) and beat + 5 <= b0(121))):
            for i, (n, on, ln) in enumerate(E1):
                last = i == len(E1) - 1
                fuller = beat >= ANSWER_FROM - 1e-6                        # v26: alone over the lights, a little fuller
                d = {"at": round(beat + on, 4), "len": ln + (0.75 if last else 0.0), "ph": "UW1",
                     "pitch": f"m{midi_of(n)}", "vel": (0.6 if on else 0.66) if fuller else (0.5 if on else 0.56)}
                if sec_of(bar) == "B":                                     # v41: B's hums with the mouth closed
                    d.update(vel=B_HUM_VEL[1 if on else 0], expr={"hum": B_HUM})
                out.append(d)
        beat += E1_CYCLE
    # v17 (ROUND TYPE: section, the fall 121-136, ~34 s; rewritten): WHAT FALLS IS KEPT. The t4 -> t5 seam sagged
    # 12.7 dB (t4's tail began at -12.3 dB, t5's head sits near -23, and the residue SWELLED as the orbit closed): now
    # the fall is a real diminuendo - the handpan from 58 down three a cycle, the residue fading, the lights lower. And
    # as the handpan's E1 disassembles (one note fewer every two cycles: E, then G, then C, then A, until only D is
    # left), the singer hums each note as it falls away - once, softly, held a little: the voice keeps what the orbit
    # loses, and between them the handpan and the voice still make E1, until the lone D is left for t5's D9.
    beat, cyc, prevk = b0(121), 0, 5
    while beat < b0(BARS + 1) - 0.01:
        k = max(1, 5 - cyc // 2)
        if k < prevk:
            n, on, ln = E1[k]
            out.append({"at": round(beat + on, 4), "len": ln + 1.5, "ph": "UW1", "pitch": f"m{midi_of(n)}", "vel": 0.42})
        prevk = k
        beat += E1_CYCLE
        cyc += 1
    return out


# v26 (ROUND TYPE: section, the relief's second half 108.5-120, ~26 s; rewritten): SHE HUMS, THE HANDS ANSWER. The
# relief was the handpan's E1 every cycle over the lights, the singer humming E1 on alternate cycles IN UNISON with
# it - a doubling that blurred both, and nothing moved for 26 seconds. Now, from her first hum in the relief, the
# handpan falls silent on her cycles (the hook hers alone over the lights, her hum a little fuller) and on the cycles
# between it ANSWERS with E1 in retrograde - the same rhythm, the pitches reversed (E G C A D), each answer ending on
# D, home: the crest's retrograde lines 'come home' the same way. It sets up the fall, where the voice keeps the
# notes the hands let go.
ANSWER_FROM = 430.0                         # her first hum in the relief (bar 108.5)


def hums_at(beat):
    """True on the cycles the singer hums E1 in the relief (as hums() places them)."""
    cyc = int(round(beat / E1_CYCLE))
    return cyc % 2 == 0 and beat >= b0(108) and beat + 5 <= b0(121)


def write_seed():
    # E1 ASSEMBLES ITSELF: from the downbeat, one note more every two cycles, then whole; later in other shapes
    cyc = 0
    beat = 0.0
    while beat < b0(121) - 0.01:
        bar = int(beat // BPB) + 1
        s = sec_of(bar)
        k = min(5, 1 + cyc // 2)
        if s in ("crest", "rise"):                 # v6: the hook rests through the rise, so the crest's sung E1
                                                    # arrives as its return (and the build is texture: canon, harp, vibes)
            beat += E1_CYCLE; cyc += 1
            continue                                         # the voice carries it at the crest
        cell = E1[:k] if s in ("lens", "A") else E1
        if s == "relief" and beat >= ANSWER_FROM - 1e-6:            # v26: she hums, the hands answer
            if hums_at(beat):
                cell = []                                            # her cycle: the hook is hers alone
            else:
                cell = [(n, on, ln) for (n, _, _), (_, on, ln) in zip(E1[::-1], E1)]   # E1 backwards: home on D
        for n, on, ln in cell:
            v = 70 if on == 0 else 60
            if s == "relief":
                v += 6
            part("seed").add(beat + on, ln, n, v)
        if s in ("B", "rise", "relief"):
            # a second voice in canon two beats behind, a fifth below (A G E D B): the cell answering itself
            for n, on, ln in E1:
                m = midi(n) - 5                       # v6: a fourth below (A E G D B, all in key; a fifth gave F)
                part("canon").add(beat + 2 + on, ln, f"m{m}", 50)
        beat += E1_CYCLE
        cyc += 1
    # v5 (ROUND TYPE: section, bars 121-136, ~34 s; rewritten): THE ORBIT CLOSES - the fall MIRRORS the lens. The seed,
    # which assembled itself one note more every two cycles from the downbeat, now DISASSEMBLES: whole at 121, one note
    # fewer every two cycles (5 5 4 4 3 3 2 2 1 ...) until only its D is left - the D t5 picks up under its D9 pad. Over
    # it the storm's residue returns LIFTED (D3 A3 E4 F#4, the voicing bar 9 lifted it to, on the same strings-synth),
    # swelling slightly as the orbit closes. (Was: E1 augmented x2 over the fading lights.)
    beat, cyc = b0(121), 0
    while beat < b0(BARS + 1) - 0.01:
        k = max(1, 5 - cyc // 2)
        v = 58 - min(26, cyc * 3)                    # v17: a real diminuendo into t5's quiet head (was 66 - 2/cycle)
        for n, on, ln in E1[:k]:
            part("seed").add(beat + on, ln, n, v + (4 if on == 0 else 0))
        beat += E1_CYCLE
        cyc += 1
    for i, bar in enumerate(range(121, BARS + 1, 4)):
        part("residue").add(b0(bar), 4 * BPB, head(("D3", "A3", "E4", "F#4")), 46 - 3 * i)   # v17: fades (was swelling)


# v21 (ROUND TYPE: section, B's second half 49-64, ~35 s; rewritten): TWO VOICES TALKING. chirpers.py sections had
# this window 'static' (the least motion of any full window) and the rise after it 'little new' against it: B ran
# 24 bars on one texture. Now, from bar 49, the duet hums E1 back a third above on the cycles the singer leaves empty
# - the two voices trade the hook, call and answer - and the bass walks: five quarters through each chord's tones and
# a step into the next root (D F# A F# D | C E G E B | A C E C A | G B D E C - all in D mixolydian), so the harmony
# moves under them.
B2 = (49, 65)
WALK = {"D9": ("D2", "F#2", "A2", "F#2", "D2"), "Cmaj9": ("C2", "E2", "G2", "E2", "B1"),
        "Am11": ("A1", "C2", "E2", "C2", "A1"), "G6/9": ("G1", "B1", "D2", "E2", "C2")}


def b2_duet():
    out = []
    beat = math.ceil(b0(B2[0]) / E1_CYCLE) * E1_CYCLE          # on E1's own grid (the singer's hums are on the even cycles)
    while beat < b0(B2[1]) - 0.01:
        if int(round(beat / E1_CYCLE)) % 2 == 1:
            for i, (n, on, ln) in enumerate(E1):
                last = i == len(E1) - 1
                out.append({"at": round(beat + on, 4), "len": ln + (0.75 if last else 0.0), "ph": "UW1",
                            "pitch": f"m{third_above(midi_of(n))}", "vel": 0.62 if on else 0.66})
        beat += E1_CYCLE
    return out


def write_bass():
    beat = b0(17)
    while beat < b0(129) - 0.01:
        k, name, notes = chord_at(beat)
        if b0(B2[0]) <= beat < b0(B2[1]):
            for i, (n, v) in enumerate(zip(WALK[name], (88, 76, 80, 72, 70))):
                part("bass").add(beat + i, 1.0, n, v)
            beat += E1_CYCLE
            continue
        root = notes[0]
        fifth = notes[1]
        part("bass").add(beat, 2.0, root, 92)
        part("bass").add(beat + 3.0, 1.0, fifth, 74)
        part("bass").add(beat + 4.5, 0.5, root, 66)
        beat += E1_CYCLE


# v2 (ROUND TYPE: whole): THE COMBINED THEME. t4 now carries E2 and E3 as the brief asks, each TRANSFORMED for the
# relief and each PHASED (like E1 and E4) so a cycle lands exactly on the crest's downbeat (beat 320):
# - E2 'seven' (chirper-one, t2) in the MAJOR: D A F# C (its minor third lifted, like the storm's at bar 9), on a
#   harp, its seven sixteenths turning against the bar from 25 (320 - 128 x 1.75 = 96: it starts on bar 25 exactly).
# - E3 'the undertow' (chirper-two, t3) INVERTED around D: D D D | C# C# F# | E E A E - the flat second becomes a
#   leading tone, the storm's drag becomes a lift - on vibes an octave up, its 2+2+3 against everything from 42.5.
# Before the crest they turn against the 4/4 and the 5s; at 81 E1 (the voice), E2, E3 and E4 meet one downbeat: the
# first full statement of the combined theme.
E2_MAJ = [("D6", 0, 100), ("A6", 2, 76), ("F#6", 3, 88), ("C6", 5, 70)]          # sixteenth steps of 7
# v16 (ROUND TYPE: whole song): MAKE ROOM FOR THE VOICE. The song ran +9 dB hot at 600-1000 Hz against the album
# (compscore --bands) - the band a voice lives in, and t4's brief is the voice at its most human. Counting
# fundamentals: the harp's E2 put 75% of its 880 notes there (D5 A5 F#5 C5, on its seven-sixteenth cycle from bar 25
# to 120) and the glock half of its. E2 moves an octave up (D6 A6 F#6 C6): sparkle above the singer instead of chatter
# inside her band. (Moving the glock's low notes up too cost structure - 92.9 -> 89.4 / 99 -> 92.9: its register
# marks B to the relief - so the glock stays.)
E3_INV = [("D3", 0.0, 0.75), ("D3", 0.75, 0.75), ("D2", 1.5, 0.5), ("F#3", 2.0, 0.5), ("F#3", 2.5, 0.75),
          ("B2", 3.25, 0.75), ("E3", 4.0, 0.75), ("E3", 4.75, 0.75), ("A2", 5.5, 0.5), ("E2", 6.0, 1.0)]
# v6: E3 v2 (chirper-two: D | Bb | C) inverted around D - D D D | F# F# B | E E A E (I - iii - ii, all in D; was C#)


def phase_start(cycle, entry_bar, target=None):
    target = b0(CREST) if target is None else target
    k = int((target - b0(entry_bar)) // cycle)
    return target - k * cycle


# v3 (ROUND TYPE: section, bars 79-92): THE HELD BREATH. The crest is where the voice is at its most human, so the
# band makes room for it: on the last beat of bar 80 the rhythm section, the felt piano, the canon and the chip air
# stop (the lights sustain); the first line ('around the warm stone', bars 81 - 83.5) is sung over the lights, harp
# and vibes alone, with only the convergence downbeat struck (kick and swish); first try: the band came back at bar 83
# beat 3 (a 5.4 s stop, under the section detector's minimum: one seed lost a boundary elsewhere, -4.3); now the stop
# holds through both E1-augmented lines and the band comes back at bar 86 for the retrograde lines. Measured: the brush kit sits ~18-36 dB under the mix (the sub is its bulk),
# so the stop that the ear hears is the upright resting, the sub and the lights stepping back.
BREATH = (b0(CREST) - 1.0, b0(CREST))                 # the last beat of bar 80
STOP = (b0(CREST), b0(86))                            # stop-time under the first two lines (E1 augmented); the band
                                                      # returns at bar 86 - an E4 turn (beat 340, D9) - for the two
                                                      # retrograde lines that come home


# v9 (ROUND TYPE: palette): TWO SWAPS onto patches no other Accretion track uses - the canon (E1 answering itself a
# fourth below) moves from a kalimba (shared) to a NYLON guitar, warm fingerpicked strings beside the handpan; and
# E3's inverted undertow (and its octave in the rise) moves from vibes (shared) to a PEDAL STEEL, notes swelling in and
# gliding between pitches - D D D | F# F# B | E E A E as a slow, singing slide.

# v8 (ROUND TYPE: section, the rise 65-80, ~35 s; rewritten): THE GATHERING. The hook rests here, so the rise is
# made of TIME and TEXTURE (Harry: complexity goes there): soft kicks on E2's seven-sixteenth cycle (phased like the
# harp) pull a second pulse against the 4/4 snare and grow toward the crest; the harp's E2 comes forward as the
# rhythmic lead; from bar 73 every felt-piano eighth gets a sixteenth echo an octave up, a shimmer thickening into the
# held breath; the vibes double E3's inverted undertow an octave up. All in key; nothing new, just gathered.
RISE = (65, 80)


def gather():
    lo, hi = b0(RISE[0]), b0(RISE[1] + 1)
    beat = phase_start(1.75, 25)
    while beat < hi - 0.01:
        if beat >= lo - 1e-6:
            prog = (beat - lo) / (hi - lo)
            part("kick").add(beat, 0.25, "k", int(60 + 40 * prog))
        beat += 1.75
    for name, dv in (("e2", 16),):
        P[name].ev = [(s, ln, h, v + dv) if lo <= s < hi else (s, ln, h, v) for s, ln, h, v in P[name].ev]
    extra = []
    for s, ln, h, v in P["felt"].ev:
        if b0(73) <= s < hi and "," not in h:
            extra.append((s + 0.25, 0.25, f"m{midi_of(h) + 12}", v - 10))
    for e in extra:
        P["felt"].ev.append(e)
    extra = []
    for s, ln, h, v in P["e3"].ev:
        if lo <= s < hi:
            extra.append((s, ln, f"m{midi_of(h) + 12}", v - 12))
    part("e3hi").ev.extend(extra)


def hold_breath():
    def cut(names, lo, hi, keep=lambda e: False):
        for n in names:
            if n in P:
                P[n].ev = [e for e in P[n].ev if keep(e) or not (lo - 1e-6 <= e[0] < hi - 1e-6)]
    cut(["kick", "snare", "hat", "ride", "felt", "canon", "air", "bass", "sub"], *BREATH)
    cut(["kick", "snare", "hat", "ride", "air"], *STOP, keep=lambda e: abs(e[0] - b0(CREST)) < 1e-6)
    cut(["bass"], *STOP)                                  # the upright rests under the first line
    if "sub" in P:                                        # the floor strikes the convergence downbeat, then falls away
        P["sub"].ev = [(s, 1.0 if abs(s - STOP[0]) < 1e-6 else ln, h, v) for s, ln, h, v in P["sub"].ev
                       if abs(s - STOP[0]) < 1e-6 or not (STOP[0] <= s < STOP[1])]
    soften = {"felt": 8, "lights": 16}                    # and what carries the energy steps back (measured: the sub
    for n, dv in soften.items():                          # is the mix's bulk, the lights next), leaving the voice
        if n in P:
            P[n].ev = [(s, ln, h, v - dv) if STOP[0] <= s < STOP[1] else (s, ln, h, v) for s, ln, h, v in P[n].ev]


def write_combined():
    vel = {"A": -14, "B": -8, "rise": -4, "crest": 0, "relief": -4}
    beat = phase_start(1.75, 25)
    while beat < b0(121) - 0.01:
        s = sec_of(int(beat // BPB) + 1)
        for n, step, v in E2_MAJ:
            part("e2").add(beat + step * 0.25, 0.5, n, v + vel.get(s, -20))
        beat += 1.75
    beat = phase_start(7.0, A_GATHER[1])                 # v14: E3 joins at 33 (was 41), still phased onto the crest
    while beat < b0(121) - 0.01:
        s = sec_of(int(beat // BPB) + 1)
        for n, on, ln in E3_INV:
            part("e3").add(beat + on, ln, n, 74 + vel.get(s, -20))
        beat += 7.0


# v23 (ROUND TYPE: palette): ONE SWAP. The sine sub - the album's most-shared patch (five songs) - becomes
# SUB-SATURATED (a sine with a triangle and a little saw driven together, low-passed at 2 kHz): t4's floor plays E4's
# roots at D1 C1 A1 G1 (33-55 Hz), mostly below what laptop speakers and many headphones reproduce; the saturated
# sub's own harmonics (66-165 Hz) carry the same line there, so the warm floor is heard on both (Harry). At -20 dB
# (was -19) it measures 1-2 dB under the sine, which was the loudest part in B (-4.9).
SUB = {"about": "t4's sub: a sine under E4's roots, a breath of drive", "synth": {"layers": [{"wave": "sine"}],
       "amp": {"a": "15ms", "d": "0s", "s": 1, "r": "200ms"}}, "fx": ["drive drive=0.12"]}
EUCLID_7_16 = [i for i in range(16) if (i * 7) % 16 < 7]      # 7 hits spread over 16 sixteenths


# v4 (ROUND TYPE: palette): ONE SWAP. The CHIP NOISE 'air' (nes-noise-hat, an album staple - three songs; in t4 38 dB
# under the mix) becomes the djembe kit's SHAKER on the same 7-in-16 euclid, +18 dB: a hand, not a shift register,
# for the warm track, and audible. Tried and REFUSED: the sine sub (the album's top staple) as a bowed contrabass
# (contrabass-tight) - real harmonics (40% of its energy 60-250 Hz vs the sine's 5%), but its strokes cut extra
# section boundaries (8) and cost recurrence: 85.07 / 85.85 alone, 87.79 / 85.05 with the shaker.
def write_sub():
    # E4's roots an octave below the cellos' bass notes (D1, Bb1, A1, D1 - the deep end the warm mix lacked)
    low = {"D9": "D1", "Cmaj9": "C1", "Am11": "A1", "G6/9": "G1"}
    # v27 (ROUND TYPE: whole song): THE FLOOR UNDER BOTH DOORS. compscore's flow compares t4's body either side of
    # each 16-bar crossfade - section A after the t3 seam, the relief before the t5 seam - and both lacked the deep
    # floor their neighbours have (38 Hz -19.9 dB against t3, 44 Hz 16 dB short of t5): the sub entered only at B
    # (41) and stepped out for the relief. Now it plays E4's roots softly through A (from 17, velocity 72) and the
    # relief (101-120, velocity 70), on its own grid as before: weight from the theme's first statement to its last.
    # The kit and air still step out for the relief, so it still breathes.
    beat = math.ceil(b0(17) / E1_CYCLE) * E1_CYCLE
    while beat < b0(121) - 0.01:
        k, name, notes = chord_at(beat)
        s = sec_of(int(beat // BPB) + 1)
        v = {"crest": 96, "A": 72, "relief": 70}.get(s, 84)
        part("sub").add(beat, E1_CYCLE - 0.25, low[name], v)
        beat += E1_CYCLE


# v14 (ROUND TYPE: section, A's second half 25-40, ~35 s; rewritten): THE THEME GATHERS. Section A was the handpan's
# E1 over the lights and the bass, with the harp's E2 from 25 - E3 waited for B, so the 'first full statement of the
# combined theme' was not combined until later, and nothing sounded above 4 kHz for forty bars. Now the shaker's first
# whispers arrive with the harp at 25 (only the first hit of its seven-in-sixteen), E3's undertow joins on the pedal
# steel at 33 - E1 + E2 + E3 + E4 together for the first time - and the handpan steps back a little to let them in.
# The shaker stays a whisper through A (first hit only): with its full euclid A sounded like B and the two sections
# blurred (85.30 / 85.89, recurrence 99 -> 60) - B keeps the full euclid as its own.
A_GATHER = (25, 33)
# v15 (ROUND TYPE: palette): the RIDE (the brush kit's, buried ~20 dB under the mix) becomes a MODAL RIDE (modal-ride,
# unused on the album): a dense plate struck on the bow with a long shimmering decay, pitched on the song's D. Three
# rounds showed t4's missing air above 7 kHz would not come from pitched parts (glock, ganza): a cymbal's wash is
# where air lives. Same part - three strokes a bar through the crest and the relief.
RIDE = "D4"


def gather_a():
    lo, hi = b0(A_GATHER[1]), b0(41)
    P["seed"].ev = [(s, ln, h, v - 6) if lo <= s < hi else (s, ln, h, v) for s, ln, h, v in P["seed"].ev]
    for bar in range(A_GATHER[0], 41):
        for i in EUCLID_7_16[:1]:                        # only the first hit: B keeps the full euclid as its own
            part("air").add(b0(bar) + i * 0.25, 0.25, "sh", (42 if i == 0 else 32) + (bar - A_GATHER[0]) // 2)


def write_air():
    # the chip's noise channel: a 7-in-16 euclid of sixteenths (polymeter against E1's 5 and E4's 20), quiet
    for bar in range(41, AFTERGLOW[0]):
        for i in EUCLID_7_16:
            v = 58 if i == 0 else 46
            part("air").add(b0(bar) + i * 0.25, 0.25, "sh", v + (8 if sec_of(bar) == "crest" else 0))


AFTERGLOW = (101, 120)        # v2: after the crest the kit, the chip air and the sub step out - the relief breathes


def write_drums():
    for bar in range(41, AFTERGLOW[0]):
        s = sec_of(bar)
        t = b0(bar)
        part("kick").add(t, 0.5, "k", 100 if s == "crest" else 92)
        if s in ("rise", "crest", "relief"):
            part("kick").add(t + 2.5, 0.5, "k", 70)
        part("snare").add(t + 2, 0.5, "s", 88 if s == "crest" else 78)
        for e in range(8):
            part("hat").add(t + e * 0.5, 0.25, "h", 52 if e % 2 else 40)
        if s in ("crest", "relief"):
            part("ride").add(t, 1.0, RIDE, 64)
            part("ride").add(t + 1.5, 1.0, RIDE, 52)
            part("ride").add(t + 3, 1.0, RIDE, 56)
    part("snare").add(b0(CREST), 2.0, "sw", 100)                 # the swish at the crest


def sung_notes(at_beat, takes, transpose=0):
    out = []
    t = at_beat
    for tk in takes:
        ns = tk["notes"]
        for i, n in enumerate(ns):
            ln = n["len"]
            if i + 1 < len(ns) and ns[i + 1]["at"] - n["at"] - ln < 0.5:
                ln = ns[i + 1]["at"] - n["at"]             # v7: legato inside a line - touching notes, one breath (join)
            swell = 0.86 + 0.14 * math.sin(math.pi * i / max(1, len(ns) - 1))      # v18: the phrase breathes
            d = {"at": round(t + n["at"], 4), "len": round(ln, 4), "ph": n["ph"],
                 "pitch": f"m{midi_of(n['pitch']) + transpose}", "vel": round(n["vel"] * swell, 3)}
            if n.get("expr_path"):
                d["expr_path"] = n["expr_path"]
            out.append(d)
        t += 10.0                                                   # each line is E1 augmented: 10 beats
    return out


def midi_of(p):
    return int(float(p[1:])) if p.startswith("m") else midi(p)


# v7 (ROUND TYPE: section, the crest 79-92): THE BREATH AND THE DUET. (wM's join/inhale are in the library patch
# but not yet in the pinned engine, so the breath is made by hand.) A soft band-passed breath swells over the held
# beat of bar 80 and stops at the downbeat - the singer breathing in before 'around the warm stone' - and again before
# the band returns at 86. There a second, lighter singer joins the two retrograde lines ('I kept your far side / and
# turned toward you') a diatonic third above in D Mixolydian: a duet, two people, not t8's choir. Lines are legato.
# v10 (ROUND TYPE: palette - an engine feature the album had not used): both singers move onto the VOICE ENGINE
# (groove pin 8ebc9a86): JOIN (each line's touching notes one breath - the glottis and tract carry on, the formants
# glide from syllable to syllable), a real INHALE before each line, a WANDERING vibrato (rate and depth drift on slow
# curves, entering late as a singer's does) and S-shaped slides (glide_smooth). The lead is warm and slow-vibrato'd;
# the duet a third above is lighter, breathes less and wavers quicker. The hand-made noise breath (v7) stays as the
# band's breath around the singer's own (retiring it cost the crest's edges: structure on seed 0 83.9 -> 79.9).
# v18 (ROUND TYPE: whole song): THE BREATHING SINGER. The voice now runs through the whole song (hums in B, lines at
# the crest, hums in the relief, the kept notes of the fall), so making her more human moves every section: her BREATH
# follows her loudness (my own patch had replaced the voice's velocity-linked breath and effort with flat values) -
# soft hums come out airy and close, full sung lines toned and pressed - and every sung line BREATHES as a phrase, a
# gentle swell into its middle easing off at its end, where the takes' notes were flat. The duet likewise.
# v22 (ROUND TYPE: whole song): THE SINGER'S GESTURES. She runs through the whole song (hums in B, the lines at the
# crest, the sung hook, the relief, the kept notes of the fall), and t4's brief is the voice at its most human - so
# she takes wM's three singing gestures at once: each phrase SCOOPS into its first note from just over a semitone
# below (1.2 st, ~85 ms), its last note FALLS two semitones as the breath runs out, and every leap swings a little
# past its note and settles (glide_overshoot 0.07). The lighter duet scoops 1, falls 1.5, overshoots 0.05.
def BREATHES(base):
    return {"value": base, "mod": [{"src": "vel", "amount": -0.34}]}


EFFORT = {"value": 0.3, "mod": [{"src": "vel", "amount": 0.45}]}
VOICE = {"about": "t4's voice: a warm, close, human singer - slightly larger tract, soft breath, covered vowels; "
                  "joined lines, a real breath before each, a wandering vibrato (v10)",
         "play": {"mono": True, "glide": "110ms", "glide_smooth": True, "scoop": 1.2, "fall": 2.0,
                  "glide_overshoot": 0.07},                 # v22: she scoops in, falls off, swings past leaps
         "synth": {"layers": [{"type": "voice", "tract": 1.02, "breath": BREATHES(0.42), "effort": EFFORT, "formant_bw": 1.6, "ph_soft": 0.35,
                               "consonant_level": "-4dB", "pulse_rate": 5, "join": True, "inhale": 0.4,
                               "even": 1.0}],
                   "lfo": {"vib": {"wave": "sine", "rate": "5.2hz", "delay": "300ms", "fade": "500ms",
                                   "retrig": True, "wander": 0.7}},
                   "pitch": {"value": 0, "mod": [{"src": "expr.f0", "amount": 0.01}, {"src": "lfo.vib", "amount": 0.2}]},
                   "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "250ms"}}}
# v37 (ROUND TYPE: whole song): A LIVED-IN VOICE. 'The voice at its most human so far' - and the most human thing
# about a voice is its imperfection. wM's AGE (pinned 44372fb9) gives her some of it, 0.45 (0.3 measured too faint to hear: HNR -1 dB):
# the folds leak a little air and close softly, the period and level waver a little from cycle to cycle, and a slow
# 4.5-6.5 Hz tremor, whose rate wanders, rides under her own vibrato. Her first closed-mouth hum (hum1) is the same
# singer and keeps it. The DUET stays young (age 0): two voices of different ages, singing the same tune a third
# apart - a warm, weathered lead and a lighter, cleaner second. A different voice from t8's bright choir and its
# young solo.
VOICE["synth"]["layers"][0]["age"] = 0.45
# v41 (ROUND TYPE: section, B's hums 45-56, ~27 s; rewritten - wM's closed-mouth HUM, pinned e3da830a): HUMMED, AND
# ANSWERED. Through B she hums the hook on the even cycles and her duet answers a third above on the odd ones - both
# on an open 'oo', the air over them. Now she hums with her MOUTH CLOSED (hum 0.8, at m: the nasal murmur near 270 Hz,
# no air), and the duet answers OPEN: closed and open trading every cycle, a call and its reply. Bound per note, so
# her sung words elsewhere stay open (and hum1 and the relief's hums, whose air the t5 seam wants, are untouched).
# High hums run ~7 dB quieter (wM), so hers come up (0.5/0.56 -> B_HUM_VEL).
VOICE["synth"]["layers"][0].update({"hum": "expr.hum", "hum_at": "m"})
B_HUM_VEL = (0.95, 0.9)                           # (the first note of each cycle, the rest)
B_HUM = 0.8                                       # not quite sealed: fully closed (1.0) took B's air with it - t4's
                                                  # 14.8 kHz band, already short of the album, fell 0.5 dB (-0.045)
# v61 (ROUND TYPE: whole song): EVERY PHRASE LETS GO. 'The voice at its most human so far' - and a sung phrase that
# ends at full tone and stops, as hers did, is the machine's tell: a singer runs out of air. wM's TAPER (pinned
# 251180c1; the sag was chirper-three's ask): on a joined line the phrase's LAST note keeps full tone for its first 30%,
# then lets go - quieter (-9 dB), darker, breathier, the pitch sagging up to 15 cents. Now on every line she sings -
# the verse, the closed hums of B, the crest's words, the relief - at 0.6 (wM's recipe for a soloist), and on the
# young duet at 0.4 (a younger singer holds a little longer). Notes inside a phrase are untouched; hum1 is excluded.
VOICE["synth"]["layers"][0]["taper"] = 0.6
VOICE2_TAPER = 0.4

VOICE2 = {"about": "t4's second singer (v7): lighter and a little brighter, a third above in the duet; joined (v10)",
          "play": {"mono": True, "glide": "90ms", "glide_smooth": True, "scoop": 1.0, "fall": 1.5,
                   "glide_overshoot": 0.05},
          "synth": {"layers": [{"type": "voice", "tract": 0.95, "breath": BREATHES(0.46), "effort": EFFORT, "formant_bw": 1.4, "ph_soft": 0.35,
                                "consonant_level": "-6dB", "pulse_rate": 5, "join": True, "inhale": 0.3,
                                "taper": VOICE2_TAPER}],
                    "lfo": {"vib": {"wave": "sine", "rate": "5.6hz", "delay": "250ms", "fade": "400ms",
                                    "retrig": True, "wander": 0.6}},
                    "pitch": {"value": 0, "mod": [{"src": "expr.f0", "amount": 0.01}, {"src": "lfo.vib", "amount": 0.16}]},
                    "amp": {"a": "50ms", "d": "0s", "s": 1, "r": "250ms"}}}
BREATH_AIR = {"about": "t4's breath (v7): band-passed air swelling in, stopped at the phrase",
          "synth": {"layers": [{"color": "pink"}],
                    "filters": [{"kind": "bp", "cutoff": 1700, "q": 0.8}],
                    "amp": {"a": "380ms", "d": "0s", "s": 1, "r": "25ms"}}}
MIXO = [2, 4, 6, 7, 9, 11, 0]                       # D Mixolydian pitch classes, degree order


def third_above(m):
    pc = m % 12
    k = MIXO.index(pc)
    up = (MIXO[(k + 2) % 7] - pc) % 12
    return m + up


# v19 (ROUND TYPE: section, the crest's second half 91-100, ~21 s; rewritten): THE HOOK, SUNG BACK. The voice's four
# lines end at bar 91, and the handpan and the canon rest through the crest (the voice carries E1 there) - so the
# second half of t4's climax had no hook at all: ten bars of band led by the sub and the lights. Now, after a bar of
# air, the singer sings E1 ITSELF on an open 'ah', full-voiced, four times (cycles 73-76, bars 92-97), and on the last
# two the duet joins a third above - the hook in two voices; then the voices rest and the handpan answers with E1,
# the nylon canon a fourth below two beats behind (cycles 77-79), carrying it straight into the relief.
SUNG_HOOK = range(73, 77)                 # E1 cycles (5 beats each): bars 92.25 - 97
HANDS_HOOK = range(77, 80)                # bars 97.25 - 101, into the relief's own seed and canon


# v25 (ROUND TYPE: section, the crest's full-band half 86-96, ~22 s in the window 81-96; rewritten): THE THEME,
# COMBINED. chirpers.py sections read the crest as 'little new' against the rise - and measured, the crest was the
# rise with a voice on top: E2 (the harp) at -19.7 and E3 (the steel) at -20.3 under the singer, so 'the first full
# statement of the combined theme' was heard as E1 and E4 only; and the kit was quieter than in the rise (kick -14.8
# vs -9.5). Now, when the band returns at 86, E2 and E3 come forward 6 dB on a gain lane - the harp's sparkle above
# her (D6 A6 F#6 C6) and the steel's slide below her - so all four elements are heard around the voice at once, and
# the kit plays its fullest (+20 velocity): the cycles converge audibly at the crest. The held breath (81-85) is as
# it was.
CREST_FX = "gain gain=0dB+auto.cr*1"
CREST_FULL = (86, 97)


def crest_lane():
    a, z = b0(CREST_FULL[0]), b0(CREST_FULL[1])
    return [["0b", 0.0], [f"{a - 0.5:g}b", 0.0], [f"{a:g}b", 6.0], [f"{z - 1:g}b", 6.0], [f"{z:g}b", 0.0]]


# v31 (ROUND TYPE: section, bars 33-48, ~34 s - the as-heard flat run 1:09-2:05 (eco's --mix view) and seed 11's
# 0:56-2:00; rewritten): THE BREATH BEFORE B. The sub (v27's floor, the loudest thing here at -4.8) ran unbroken
# from A into B, and E3's arrival - the steel's first statement in the song - sat at -17, unheard. Now:
#   33-40 E3 ARRIVES: the steel sings 8 dB up for its first eight bars (its own spotlight), then settles;
#   37-40 A BREATH: the sub, the bass and the shaker's whispers step away - the handpan, the lights and the singing
#         steel alone - and a brush swish swells into
#   41    THE LANDING: kit, sub and bass arrive together on one downbeat, and B begins.
STEEL_LIGHT = (33, 40)
BREATH_B = (37, 40)


def steel_lane():
    a, z = b0(STEEL_LIGHT[0]), b0(STEEL_LIGHT[1] + 1)
    return [["0b", 0.0], [f"{a - 0.5:g}b", 0.0], [f"{a:g}b", 8.0], [f"{z - 2:g}b", 8.0], [f"{z:g}b", 0.0]] \
        + crest_lane()[1:]


def breath_before_b():
    lo, hi = b0(BREATH_B[0]), b0(BREATH_B[1] + 1)
    for n in ("sub", "bass", "air"):
        if n in P:
            out = []
            for s, ln, h, v in P[n].ev:
                if lo - 1e-6 <= s < hi - 1e-6:
                    continue
                if s < lo - 1e-6 < s + ln:
                    ln = lo - s
                out.append((s, ln, h, v))
            P[n].ev = out
    part("snare").add(hi - 2.0, 2.0, "sw", 74)                   # the swish into 41


# v32 (ROUND TYPE: section, bars 41-56, ~34 s - B's first half, still read flat on seed 11 (1:28-2:00); rewritten):
# THE LIGHTS SHIMMER. B opened as a loop: the handpan's E1 over and over, the voice humming the same E1 from 46, the
# lights holding their bowed chords under the newly landed kit. Now, as the kit, sub and bass land at 41, the four
# lights take up BOWED TREMOLO (the cellos' ^trem) for eight bars - the same chords, but trembling with the energy of
# the landing - and at 49 the bows settle back to long strokes as the hats give way to the ride (v28) and the duet
# answers her (v21). Texture and time, not pitch. (Tried: tremolo sul ponticello - glassier, no better for the tools,
# colder than this song; flatness.py cannot see a tremolo inside its 8 s blocks - this one is for the ear.)
LIGHTS_TREM = (41, 48)


def lights_shimmer():
    lo, hi = b0(LIGHTS_TREM[0]), b0(LIGHTS_TREM[1] + 1)
    inside = lambda s, h: lo - 1e-6 <= s < hi - 1e-6 and "^" not in h
    P["lights"].ev = [(s, ln, h + "^trem", min(127, v + 16)) if inside(s, h) else (s, ln, h, v)   # tremolo plays
                      for s, ln, h, v in P["lights"].ev]                                          # ~2.6 dB under


# v33 (ROUND TYPE: section, the crest 86-100, ~32 s - its lowest-change stretch for flatness.py on both seeds,
# 3:12-3:28; rewritten): EVERYONE SINGS THE HOOK. Under lines 3-4 and the sung hook the band played one unchanging
# full texture. Now:
#   bar 91, in the gap after '...toward you', the kit, the sub and the bass STOP for one bar - the lights hold, her
#        last word rings - and a brush fill swells over beats 3-4 into a swish that lands the hook at 92 (the crest's
#        own stop-time, 81, in miniature);
#   92-96 the floor sings it: the upright leaves its roots and doubles her E1 two octaves down, note for note
#        (D A C G E), so voice, duet and bass converge on the hook - the album's cycles converging at the crest.
CREST_STOP = 91
HOOK_BASS = [("D2", 0.0, 0.5, 88), ("A2", 0.5, 0.75, 76), ("C3", 1.25, 0.25, 70), ("G2", 1.5, 1.0, 80),
             ("E2", 2.5, 2.5, 84)]


def everyone_sings():
    lo, hi = b0(CREST_STOP), b0(CREST_STOP + 1)
    for n in ("kick", "snare", "hat", "ride", "air", "bass", "sub"):
        if n not in P:
            continue
        out = []
        for s, ln, h, v in P[n].ev:
            if lo - 1e-6 <= s < hi - 1e-6:
                continue
            if s < lo - 1e-6 < s + ln:
                ln = lo - s
            out.append((s, ln, h, v))
        P[n].ev = out
    for i in range(8):                                                   # the fill, beats 3-4 of bar 91
        part("snare").add(lo + 2 + i * 0.25, 0.25, "s", 44 + i * 8)
    part("snare").add(hi, 2.0, "sw", 96)                                 # the swish that lands the hook
    a, z = SUNG_HOOK[0] * E1_CYCLE, (SUNG_HOOK[-1] + 1) * E1_CYCLE
    P["bass"].ev = [e for e in P["bass"].ev if not (a - 1e-6 <= e[0] < z - 1e-6)]
    for c in SUNG_HOOK:
        for n, off, ln, v in HOOK_BASS:
            part("bass").add(c * E1_CYCLE + off, ln, n, v)


# v34 (ROUND TYPE: section, the relief 101-120, ~40 s, its answers rewritten): THE REED ANSWERS HER. In the relief
# she hums E1 and the handpan answers with its retrograde (E G C A D). Now, through the float (105-112: the sub and
# the bass away), the CLARINET answers her instead - the reed that took the hook from the handpan for one phrase in A
# (v29) comes back: breath answering breath, all air - legato, each note held at most a beat and a half longer so no
# answer covers her next hum. At 113, when the floor returns, the handpan takes the answers back: the struck metal
# returns with the gravity. (Tried: the reed through the whole relief to 120 - the relief's body went darker than
# t5's head, flow 82.3 -> 79.6 at the t4 -> t5 seam.)
REED_FROM = ANSWER_FROM


def reed_answers():
    lo, hi = REED_FROM, b0(FLOAT[1] + 1)
    taken = sorted(e for e in P["seed"].ev if lo - 1e-6 <= e[0] < hi - 1e-6)
    P["seed"].ev = [e for e in P["seed"].ev if not (lo - 1e-6 <= e[0] < hi - 1e-6)]
    for k, (s, ln, h, v) in enumerate(taken):
        nxt = taken[k + 1][0] if k + 1 < len(taken) else s + ln + 2.0
        part("clar").add(s, max(ln, min(nxt - s, ln + 1.5)), h, min(96, v + 2))


# v36 (ROUND TYPE: whole song): THE ARC. Measured (8 s loudness over the whole song): t4's shape never showed in its
# level - from 0:40 to 4:16 nearly everything sat within 0.4-2 dB of the peak, the crest no louder than A, and the
# RELIEF (4:08) the loudest moment of all; the master compressor and the loudness target ironed the arc flat. Now one
# proportional gain lane across every track shapes it - each section keeps its colour (the scorer compares shape, not
# level: t8 v33's lesson) - A and B sit back, the rise climbs into the crest, the crest is the top, and the relief
# settles back as relief should, the fall following it down. Lane values are about twice what is heard (the master
# compressor gives back about half).
ARC = [(1, -3.0), (65, -3.0), (81, 0.0), (101, 0.0), (105, -6.0), (BARS + 1, -6.0)]   # the lens with A and B


def arc(song):
    pts = [[f"{b0(bar):g}b", db] for bar, db in ARC]
    for tr_ in song["tracks"]:
        tr_["fx"] = list(tr_.get("fx") or []) + ["gain gain=0dB+auto.ar*1"]
        tr_["auto"] = dict(tr_.get("auto") or {}, ar={"points": pts})


# v38 (ROUND TYPE: section, the rise 65-80, ~35 s - with the crest's second half the stillest stretch left for
# flatness.py, 2:24-2:48; rewritten): THE LEAD CHANGES HANDS, AND THE LIGHTS GO OUT. The rise was the lights' chords
# climbing over sub, air and kick, the hook resting (v6), the elements that converge at the crest masked under it.
# A first try raised E2 and E3 together as a steady layer through 69-80 and made the rise MORE uniform (a new 32 s
# still run, refused); so now each phrase SWAPS who leads, and one cuts: 65-68 the lights alone (as v30 thinned
# them); 69-72 E2's harp steps forward for those four bars only; 73-76 the LIGHTS GO OUT - the chords stop, and E3's
# pedal-steel line and its octave double play alone over kick, sub and the swelling air; 77-80 the lights return at
# full under the build, and the crest lands on all of it.
LEADS = {"e2": [(69, 72, 7.0), (92, 96, 6.0)], "e3": [(73, 76, 8.0), (92, 96, 6.0)], "e3hi": [(73, 76, 8.0)],   # v52: 92-96
         "duet": [(49, 56, 7.0), (113, 120, 10.0)]}        # v41: the duet's open reply to her closed hum, heard;
                                                          # v44: and the warm third over her relief hums
LIGHTS_OUT = (73, 76)


def lead_lanes(song):
    for tr_ in song["tracks"]:
        if tr_["name"] in LEADS:
            pts = [["0b", 0.0]]
            for a_, z_, db in LEADS[tr_["name"]]:
                a, z = b0(a_), b0(z_ + 1)
                pts += [[f"{a - 1:g}b", 0.0], [f"{a:g}b", db], [f"{z - 1:g}b", db], [f"{z:g}b", 0.0]]
            tr_["fx"] = list(tr_.get("fx") or []) + ["gain gain=0dB+auto.ld*1"]
            tr_["auto"] = dict(tr_.get("auto") or {}, ld={"points": pts})


def lights_out():
    lo, hi = b0(LIGHTS_OUT[0]), b0(LIGHTS_OUT[1] + 1)
    out = []
    for s, ln, h, v in P["lights"].ev:
        if lo - 1e-6 <= s < hi - 1e-6:
            continue
        if s < lo - 1e-6 < s + ln:
            ln = lo - s
        out.append((s, ln, h, v))
    P["lights"].ev = out


# v39 (ROUND TYPE: whole song): THE HOOK NEVER STAYS IN ONE HAND. The rule the song has grown into, now kept across
# the whole of it: no instrument carries E1 for more than eight bars running. Audited per eight-bar phrase - lens and
# A the handpan, 25-32 the clarinet (v29), 33-40 the handpan, B 49-56 the handpan an octave up (v28), 57-64 the drop,
# the rise resting (v6), the crest sung, the relief hummed and answered by the reed (v34), the fall coming apart (v17)
# - one gap was left: the handpan carried it for SIXTEEN bars, 33-48, straight across A into B, where it is the
# loudest thing (and B's other turn, the cellos' tremolo, is invisible to the ear at that level - seed 11 read a 32 s
# still run there, 1:28-2:00). So at B the reed takes it back: 41-48 the handpan rests and the clarinet sings E1
# legato at pitch, as it did at 25-32 - and at 49 the handpan returns an octave up with the ride (v28): reed, then
# struck bell - a contrast of touch as well as hand. (Tried first: the felt glockenspiel carrying E1 an octave up -
# bells into bells, in the very register the handpan climbs to at 49: sixteen bars of bright bell E1, stiller than
# before - seed 0 grew its own 32 s run.)
B_HAND = (41, 48)


def reed_takes_b():
    lo, hi = b0(B_HAND[0]), b0(B_HAND[1] + 1)
    inside = lambda s: lo - 1e-6 <= s < hi - 1e-6
    taken = sorted(e for e in P["seed"].ev if inside(e[0]))
    P["seed"].ev = [e for e in P["seed"].ev if not inside(e[0])]
    for k, (s, ln, h, v) in enumerate(taken):
        nxt = taken[k + 1][0] if k + 1 < len(taken) else min(hi, s + 2.5)
        part("clar").add(s, max(ln, nxt - s), h, min(96, v + 4))


# v40 (ROUND TYPE: whole song): HUMAN TIME. 'The voice at its most human' - and Harry: complexity in TIME. t4's time
# was a grid: 108, then one long ramp to 112 for t5. Now the band BREATHES the way players do into the boundaries that
# matter, then picks the tempo up again: a ritardando across the last bar before B (6%, after the breath before B),
# before the crest (8%) and before the relief (10%, the exhale), each landing a tempo on the downbeat. Every other
# point stays on the old line, so both seams keep exactly the tempo t3 and t5 expect (108 in, 112 by bar 121).
BREATHS = [(41, 0.06), (81, 0.08), (101, 0.10)]       # (the downbeat it breathes into, how much it broadens)


def base_bpm(beat):
    if beat <= b0(17):
        return float(SEAM_IN)
    return SEAM_IN + (SEAM_OUT - SEAM_IN) * min(1.0, (beat - b0(17)) / (b0(121) - b0(17)))


def human_time():
    pts = [{"at": "0b", "bpm": SEAM_IN}, {"at": f"{b0(17):g}b", "bpm": SEAM_IN}]
    for bar, slow in BREATHS:
        a, z = b0(bar) - BPB, b0(bar)
        ramp = a > b0(17)
        pts.append(dict({"at": f"{a:g}b", "bpm": round(base_bpm(a), 3)}, **({"ramp": True} if ramp else {})))
        pts.append({"at": f"{z - 0.25:g}b", "bpm": round(base_bpm(z) * (1 - slow), 3), "ramp": True})
        pts.append({"at": f"{z:g}b", "bpm": round(base_bpm(z), 3)})
    pts.append({"at": f"{b0(121):g}b", "bpm": SEAM_OUT, "ramp": True})
    return pts


# v43 (ROUND TYPE: section, the crest's end 92-100 and its hand-off to the relief, ~25 s; rewritten): SHE HOLDS THE
# LAST NOTE. The crest's sung hook (four E1 cycles, 92-97, her 'ah' with the duet a third above - the loudest thing in
# the song) stopped at 97, and the crest's last bars ran on as band alone until the relief's first words at 101 ('I
# kept your far side'). Now she HOLDS the hook's last note (E4, the duet G4 above it) through 97-100 - over the band,
# into the breath of the ritardando (v40) - fading as she runs out (a diminuendo lane, -7 dB across the hold), then a
# half-beat breath and the words. The climax ends on a held human note instead of a gap. (The band stays: v30 found
# that thinning it at 97 merged into a 32 s still run.)
HOLD_FROM, HOLD_FADE = 96, -7.0


def hold_the_last(notes):
    end = b0(101) - 0.5
    last = max((n for n in notes if b0(HOLD_FROM) - 1e-6 <= n["at"] < b0(HOLD_FROM + 1) - 1e-6), key=lambda n: n["at"])
    last["len"] = round(end - last["at"], 4)


def hold_lanes(song):
    a, z = b0(HOLD_FROM + 1), b0(101) - 0.5
    pts = [["0b", 0.0], [f"{a:g}b", 0.0], [f"{z:g}b", HOLD_FADE], [f"{z + 0.25:g}b", 0.0]]
    for tr_ in song["tracks"]:
        if tr_["name"] in ("voice", "duet"):
            tr_["fx"] = list(tr_.get("fx") or []) + ["gain gain=0dB+auto.hd*1"]
            tr_["auto"] = dict(tr_.get("auto") or {}, hd={"points": pts})


# v44 (ROUND TYPE: section, the relief's last eight bars 113-120, ~18 s plus its approach - the stillest block
# left for flatness.py, 4:08; rewritten): THE WARM THIRD. Through the relief's last bars she hums alone - the lights,
# the handpan back, the clarinet's answers, no drums - and the duet that sang the crest with her had gone. Now it
# hums WITH her, a third above in the key (the song's own name, sung at its exhale): one voice becomes two in thirds
# for the relief's last eight bars, softly, before the fall. The duet's hum is open, so it also gives the t5 seam a
# little of the air it wants (t4's relief runs short of t5's top end).
WARM_THIRD = (113, 120)


# v56 (ROUND TYPE: section, B 53-60, 1:53-2:10): THE ANSWER CLOSES IN. B's voices were one exchange said eight times
# over twenty bars - every 2.5 bars she hums E1 (closed, 0.8) and five beats later the young duet answers it a third
# above, open: lovely, and unchanged from 45 to 64 (the 1:44 and 2:00 blocks still; thinning the ride there, v55,
# was refused - the motion had to come from the voices). Now the conversation moves toward the song's title: at 53.5
# the duet answers after only 2.5 beats (the canon tightening), and from 56 it sings WITH her, a third above, while
# her hum opens (0.8 -> 0.35) - into the band's drop at 57, two voices in open thirds alone: the warm third, glimpsed
# an hour of music early (it arrives in full at 113).
CLOSE_IN = [(53.5, 2.5), (56.0, 0.0), (58.5, 0.0)]       # (her cycle's first bar, the duet's delay in beats)
OPEN_HUM = 0.6                     # 0.35 opened her too far: -3.7 in the drop, the third buried 10 dB under, spectrum -0.13
TOGETHER_VEL = 1.5                 # the duet as a partner when it sings with her, not a shadow


def answer_closes_in(song):
    tr_ = {x["name"]: x for x in song["tracks"]}
    voice, duet = tr_["voice"]["notes"], tr_["duet"]["notes"]
    cyc = 10.0                                                         # E1's 5 beats... her cycle is 2.5 bars
    lo, hi = b0(CLOSE_IN[0][0]), b0(CLOSE_IN[-1][0]) + cyc
    answers = sorted([n for n in duet if b0(CLOSE_IN[0][0]) + 1 <= n["at"] < hi + 5], key=lambda n: n["at"])
    first = [n for n in answers if abs(n["at"] - (b0(CLOSE_IN[0][0]) + 5.0)) < 1e-3]
    assert first, "the duet's answer to the 53.5 cycle not found"
    cell = [n for n in answers if first[0]["at"] - 1e-3 <= n["at"] < first[0]["at"] + 5.0]
    cell = [dict(n, at=round(n["at"] - first[0]["at"], 4)) for n in cell]
    keep = [n for n in duet if not (b0(CLOSE_IN[0][0]) + 1 <= n["at"] < hi + 5)]
    for bar, delay in CLOSE_IN:
        for n in cell:
            v = n.get("vel", 0.7) * (TOGETHER_VEL if delay == 0.0 else 1.0)
            keep.append(dict(n, at=round(b0(bar) + delay + n["at"], 4), vel=round(min(1.0, v), 3)))
        if delay == 0.0:
            for n in voice:
                if b0(bar) - 1e-3 <= n["at"] < b0(bar) + 5.0 - 1e-3:
                    n["expr"] = dict(n.get("expr") or {}, hum=OPEN_HUM)
    tr_["duet"]["notes"] = sorted(keep, key=lambda n: n["at"])


def warm_third(voice):
    lo, hi = b0(WARM_THIRD[0]), b0(WARM_THIRD[1] + 1)
    return [dict(n, pitch=f"m{third_above(midi_of(n['pitch']))}", vel=round(n["vel"] * 0.75, 3))
            for n in voice if lo - 1e-6 <= n["at"] < hi - 1e-6 and n.get("ph") == "UW1"]


# v45 (ROUND TYPE: section, the relief's last eight bars 113-120, the stillest block left at 4:08; rewritten): THE
# TWO VOICES ALONE. v44 gave these bars the warm third (the duet humming a third above her), evenly over a band that
# never moved. Now, two bars in, the band steps out - lights, bass, clarinet - and the two voices hum in thirds
# over the handpan and the sub alone, bare and close (115-118), and the band comes back for the fall's door (119). Placed with
# care: the t4 -> t5 seam measures the 3 s before the out-seam starts (bar 121 - about 119.6-121, compscore's
# mix_tail); a first try cut 117-120 and swung that body's low end by 30 dB (refused, round 47).
VOICES_ALONE = (115, 118)


def voices_alone():
    lo, hi = b0(VOICES_ALONE[0]), b0(VOICES_ALONE[1] + 1)
    for n in ("lights", "bass", "clar"):                          # the sub stays under them (all four out: -0.085)
        out = []
        for s, ln, h, v in P[n].ev:
            if lo - 1e-6 <= s < hi - 1e-6:
                continue
            if s < lo - 1e-6 < s + ln:
                ln = lo - s
            out.append((s, ln, h, v))
        P[n].ev = out


# v46 (ROUND TYPE: section, the rise 65-80, ~35 s - its first half the stillest block left, 2:24 at 0.44;
# rewritten): THE LIGHTS CLIMB. The rise was built on the sub and E4's lights (-5.3 / -6.2, the loudest things in
# 65-72), and the lights held one voicing all the way: a section called the rise that never rose. Now the four lights
# CLIMB through it - every two or three chords the lowest note above the root goes up over the top (an inversion, the
# root kept on the floor), so the chords' top line rises D4 / E4 -> B4 -> E5 across the rise, the same harmony
# lifting toward the crest - and the crest (81) opens back at home, the voicing falling into the arrival.
CLIMB_STEPS = [0, 0, 0, 1, 1, 2, 2, 2, 3, 3]      # inversions per lights chord across the rise


def lights_climb():
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    lo, hi = b0(RISE[0]), b0(RISE[1] + 1)
    out, i = [], 0
    for s, ln, h, v in P["lights"].ev:
        if lo - 1e-6 <= s < hi - 1e-6 and "," in h:
            ms = sorted(midi_of(x) for x in h.split(","))
            root, rest = ms[0], ms[1:]
            for _ in range(CLIMB_STEPS[min(i, len(CLIMB_STEPS) - 1)]):
                m = rest.pop(0)
                while m <= max(rest):
                    m += 12
                rest.append(m)
            h = ",".join(f"{names[m % 12]}{m // 12 - 1}" for m in [root] + rest)
            i += 1
        out.append((s, ln, h, v))
    P["lights"].ev = out


# v47 (ROUND TYPE: whole song): A VERSE. In 136 bars she sang words only at the crest - the chorus, 'around the warm
# stone / the cold half sleeping / I kept your far side / and turned toward you' - and for the eighty bars before it
# only hummed (the filtered first hum in A, the closed hums in B): a chorus with no verse, the voice at its most human
# saying nothing until the top. Now A's last phrase - the one place in A she was silent (33-40: handpan, sub, the
# four lights, the steel) - has her FIRST WORDS, two lines: 'four lights were turning / I counted them home' (the
# element t4 brings, named as the lights play; 'home' the key), sung on E1 INVERTED around A4 - A D B E G, the hook's
# own rhythm and intervals upside down, all in key and consonant over the four lights - so the chorus keeps E1 itself
# for its arrival. Softer than the chorus (x0.88); the handpan rests under her two lines (E1 against its inversion
# would rub C against B), the hook changing hands again. Takes made with the chorus's own tool and settings
# (chirpers9-t4-takes.json 'verse').
VERSE = json.load(open(os.path.join(HERE, "chirpers9-t4-takes.json")))["verse"]
VERSE_AT, VERSE_VEL = 130.0, 0.88                    # bar 33.5, on E1's grid; two lines of ten beats


def verse():
    return [dict(n, vel=round(n["vel"] * VERSE_VEL, 3)) for n in sung_notes(VERSE_AT, VERSE)]


def hands_rest_for_verse():
    lo, hi = VERSE_AT - 1e-6, VERSE_AT + 10.0 * len(VERSE) - 1e-6
    P["seed"].ev = [e for e in P["seed"].ev if not lo <= e[0] < hi]


# v48 (ROUND TYPE: section, A's second phrase 25-32 and the turn into the verse, ~18 s - the 0:56 block, 0.49 / 0.28,
# the stillest in A; rewritten): THE CLARINET FINDS THE VERSE. Here the clarinet held E1 alone (v31's swap), cycle
# after identical cycle over the sub and the lights, and then her verse (v47) arrived on E1 INVERTED with nothing to
# lead to it. Now the clarinet turns the hook over in its hands as it goes - its last cycles alternate the hook and
# its MIRROR (115: A D B E G, 120: the hook again, 125: the mirror) - so when she sings 'four lights were turning' at
# 130 she is taking up, with words, the tune the clarinet has just found: a transformation heard happening, as the
# album does with every element. Same register as her verse (D4 -> A4, A4 -> D4, C5 -> B3, G4 -> E4, E4 -> G4).
MIRROR_CYCLES = (115.0, 125.0)                       # beats where the clarinet's cycle plays the mirror


def clarinet_finds_the_verse():
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    out = []
    for s, ln, h, v in P["clar"].ev:
        if any(c - 1e-6 <= s < c + E1_CYCLE - 1e-6 for c in MIRROR_CYCLES) and "," not in h:
            m = 131 - midi_of(h)
            h = f"{names[m % 12]}{m // 12 - 1}"
        out.append((s, ln, h, v))
    P["clar"].ev = out


# v49 (ROUND TYPE: section, B's dialogue 49-56, ~17 s - the 1:44 block, 0.56; rewritten): THE HANDS LISTEN. v41 made
# B's second quarter a dialogue - she hums E1 closed, the young duet answers open a third above, cycle by cycle - but
# under it the ride (-5.6) and the handpan playing E1 itself (-6.4) led, and both voices sat at -11.8, heard a third
# of the time: the conversation happened behind the band. Now for its first four bars (49-52) the handpan steps out
# and LISTENS - the hook is the two voices' alone, traded over the ride, the lights, the sub and the air - and at 53
# the hands come back in under them, as if answering too. (The sub stays: a floorless four bars cost spectrum in t4
# v45; and the ride stays: without it too the voices came further forward but its air was missed, -0.035.)
HANDS_LISTEN = (49, 52)


# v53 (ROUND TYPE: section, rise 65-68, 2:21-2:28): THE RISE PULLS BACK. The rise's first half was B's band carried
# straight on - sub, lights, bass, kick, snare, handpan, glock - and the harp's E2 arriving at 69 slid in under it:
# the stillest block in the song by the measure (2:24, 0.48) and a rise with no breath before it. Now the rise starts
# from a held breath: for four bars only the lights (beginning their climb), the sub (the floor stays - without it the
# album's low end goes) and the kick's gathering seven-sixteenth pulse - the time the rise is made of, heard alone for
# once. The bass, the snare, the handpan and the glock rest; at 69 they all come back WITH the harp's E2: an arrival,
# where there was a continuation. (Harry, 6 Nov: every 8-16 bars something moves - a drop-out among them.)
RISE_BACK = (65, 68)
RISE_REST = ("bass", "snare", "seed", "felt", "hat")


def rise_pulls_back():
    lo, hi = b0(RISE_BACK[0]), b0(RISE_BACK[1] + 1)
    for n in RISE_REST:
        out = []
        for s, ln, h, v in P[n].ev:
            if lo - 1e-6 <= s < hi - 1e-6:
                continue
            if s < lo - 1e-6 < s + ln:
                ln = lo - s
            out.append((s, ln, h, v))
        P[n].ev = out


# v57 (ROUND TYPE: palette): THE RISE IS BOWED. E3 rode three pedal-steel tracks (e3, e3hi, steel) - one instrument
# tripling one element - and in the rise (65-80) its line an octave up was the third copy. Now that line is BOWED: a
# solo violin (violin, unused on the album: a waveguide string on a resonant body, delayed vibrato), and since a violin
# starts at G3 the line climbs an octave higher (D4-F#5) - one human string singing E3 up into the crest, in the song
# where the voice and everything near it is most human.
E3HI_PATCH, E3HI_GAIN, E3HI_UP = "violin", "-8dB", 12      # the steel copy sat at -22 (unheard); at -15 the violin -14/-18


# v58 (ROUND TYPE: section, A 29-32, 1:01-1:08): A OPENS UPWARD. A's middle was eight bars of one texture - the
# lights, bass, sub, shaker, the harp's E2 and the clarinet finding the verse - the stillest block clear of both seams
# (0:56, 0.48). Now the four bars before her verse lift away from the floor: the bass and the shaker rest (the sub
# stays - the album's low end), the lights' two top notes rise an octave (B_OPEN's re-voicing, here as A's first
# breath upward), and the clarinet's mirrored line is left in the open; at 33 the bass and shaker come back under her
# verse - an arrival, where there was a continuation.
A_OPEN = (29, 33)
A_REST = ("bass", "air")


def a_opens_upward():
    lo, hi = b0(A_OPEN[0]), b0(A_OPEN[1])
    for n in A_REST:
        out = []
        for s, ln, h, v in P[n].ev:
            if lo - 1e-6 <= s < hi - 1e-6:
                continue
            if s < lo - 1e-6 < s + ln:
                ln = lo - s
            out.append((s, ln, h, v))
        P[n].ev = out
    ev = []
    for s, ln, h, v in P["lights"].ev:
        if lo - 1e-6 <= s < hi - 1e-6 and "," in h:
            ns = sorted(h.split(","), key=midi_of)
            h = ",".join(ns[:-2] + [f"m{midi_of(x) + 12}" for x in ns[-2:]])
        ev.append((s, ln, h, v))
    P["lights"].ev = ev


# v63 (ROUND TYPE: section, the crest's sung hook 92-98, 3:13-3:28; rewritten): THE HOOK IN THE CLEAR. The crest's
# second half is where the singer sings the album's hook itself (v19: E1 on 'ah', four cycles, the duet a third above
# on the last two) - over the same full band that had played the six bars before it, so the 8 s windows at 3:12 and
# 3:20 read flat (0.65, 0.60) and the hook in two voices was one more layer in a wall. Now the hook is set apart:
#   92    THE LIGHTS LIFT: as she begins it, the four lights' chords rise an octave (D9 Cmaj9 Am11 G6/9 up high);
#   94.75 THE BAND STEPS OUT: when the duet joins, the kit, ride, shaker, sub and bass stop - the two voices sing the
#         hook over the raised lights and E2/E3 alone, the combined theme with no floor under it;
#   97    THE BAND RETURNS on the bar's downbeat with a brush swish and the lights' D9 back down, the handpan answering.
HOOK_LIFT = (92.0, 97.0)
HOOK_CLEAR = (94.75, 97.0)
HOOK_CLEAR_BAND = ("kick", "snare", "hat", "ride", "air", "sub", "bass")   # with the sub kept (v63b) the crest went
#                                    flatter still (seed 11: a 40 s run 3:12-3:52) - the floor going is the contrast


# v64 (ROUND TYPE: section, B's first half 45-56, 1:38-2:03; rewritten): SHE HUMS IN A SMALLER ROOM. B moves every
# four bars (41 the landing, 45 her closed hums, 49 the ride's lift, 53 the duet closing in, 57 the drop) - but under
# every move the same floor ran on: the sub the loudest thing in B (-6.6 .. -8.8), the shaker and the kit steady, so
# the 8 s windows at 1:28, 1:44 and 2:00 read alike (seed 5: a 32 s run 1:28-2:00). Now her two intimate moments
# get a smaller room: at her first hum (45-48) and as the duet closes in (53-56) the sub rises an octave (into the
# 71-97 Hz the song lacks, not out of it), the shaker steps out and the kick keeps only its downbeats - and the full
# floor comes back with the ride's lift at 49 and the drop's turn at 57.
SMALL_ROOM = [(45, 49), (53, 57)]


def smaller_room():
    for a_, z_ in SMALL_ROOM:
        a, z = b0(a_), b0(z_)
        inside = lambda s: a - 1e-6 <= s < z - 1e-6
        P["sub"].ev = [(s, ln, f"m{midi_of(h) + 12}" if inside(s) else h, v) for s, ln, h, v in P["sub"].ev]
        P["air"].ev = [e for e in P["air"].ev if not inside(e[0])]
        P["kick"].ev = [e for e in P["kick"].ev if not inside(e[0]) or abs((e[0] - b0(1)) % 4.0) < 1e-6]


def hook_in_the_clear():
    lo, hi = b0(HOOK_LIFT[0]), b0(HOOK_LIFT[1])
    P["lights"].ev = [(s, ln, ",".join(f"m{midi_of(x) + 12}" for x in h.split(",")) if lo - 1e-6 <= s < hi - 1e-6
                       else h, v) for s, ln, h, v in P["lights"].ev]
    a, z = b0(HOOK_CLEAR[0]), b0(HOOK_CLEAR[1])
    for n in HOOK_CLEAR_BAND:
        if n not in P:
            continue
        out = []
        for s, ln, h, v in P[n].ev:
            if a - 1e-6 <= s < z - 1e-6:
                continue
            if s < a - 1e-6 < s + ln:
                ln = a - s
            out.append((s, ln, h, v))
        P[n].ev = out
    part("snare").add(z, 2.0, "sw", 92)                 # the swish the band returns on (as at the crest's 81)


def rise_bowed():
    P["e3hi"].ev = [(s, ln, ",".join(f"m{midi_of(x) + E3HI_UP}" for x in h.split(",")), v) for s, ln, h, v in P["e3hi"].ev]


def hands_listen():
    lo, hi = b0(HANDS_LISTEN[0]), b0(HANDS_LISTEN[1] + 1)
    for n in ("seed",):                                   # the ride stays: without it -0.035 (its air)
        out = []
        for s, ln, h, v in P[n].ev:
            if lo - 1e-6 <= s < hi - 1e-6:
                continue
            if s < lo - 1e-6 < s + ln:
                ln = lo - s
            out.append((s, ln, h, v))
        P[n].ev = out


# v50 (ROUND TYPE: palette - the part the song lacks): THE WARM STONE. The chorus begins 'around the warm stone', and
# nothing in the song was a stone. Now a SINGING BOWL (unused on the album: a felt strike, then slow-beating bronze
# partials ringing ~14 s - modes 1 : 2.71 : 5.15 : 8.2, about D G F# D over a D, all in key) is struck three times,
# at the song's three thresholds: 81, the crest's downbeat where every cycle converges (D4, ringing through the held
# breath); 101, the relief, as the kit steps out (A3); 121, the fall, the stone left ringing as t5 arrives (D3). A
# palette that was all hands, strings and breath gets one sound that is struck and left. (Not the felt piano back on
# the 'felt' track - v13 took it off for a +9 dB hot 750-877 Hz and a dull top.)
BOWL_GAIN = "-5dB"                    # at -12 it sat at -19 to -21 under the mix, unheard
BOWL = [(81, "D4", 0.62), (101, "A3", 0.5), (121, "D3", 0.45)]


# v54 (ROUND TYPE: palette - add the part the song lacks): A BREEZE. t4's brief is one word - relief - and after the
# crest (all four elements at once) the relief had everything but air: compscore --bands puts the song 3-7 dB under
# the album above 5 kHz (14.8 kHz -6.8) and 6.5 dB over it at 1.4 kHz. Now a breeze moves through the relief and
# stirs a set of WIND CHIMES (chimes, unused on the album: thin metal tubes, bright inharmonic partials, a long
# shimmer), tuned as real chimes are to a consonant pentatonic set in the key (D6 E6 F#6 A6 B6): a few strikes as the
# crest lets go (99-100), two gusts through the relief - the second fuller - and stillness again by 116, clear of
# the t5 seam (its 3 s window begins at 119.6).
CHIME_GAIN = "-8dB"                     # at -12 the first gust sat under -15.6, the second -11.1 (heard 27%)
CHIME_SET = ("D6", "E6", "F#6", "A6", "B6")
GUSTS = [(99.0, 101.5, 0.6), (103.0, 107.0, 1.0), (109.0, 115.5, 1.5)]   # (from bar, to bar, strikes per beat at the peak)


def breeze():
    import random
    rng, out = random.Random(41), []
    for a, z, peak in GUSTS:
        s, e = b0(a), b0(z)
        t = s
        while t < e:
            x = (t - s) / (e - s)
            dens = peak * math.sin(math.pi * x) ** 1.5 + 0.08
            t += rng.expovariate(dens)
            if t >= e:
                break
            v = round((30 + 50 * math.sin(math.pi * (t - s) / (e - s)) * rng.uniform(0.6, 1.0)) / 127, 3)
            out.append({"at": round(t, 3), "len": 4.0, "pitch": f"m{midi(rng.choice(CHIME_SET))}", "vel": v})
    return out


def warm_stone():
    return [{"at": b0(bar), "len": 16.0, "pitch": f"m{midi(n)}", "vel": v} for bar, n, v in BOWL]


# v51 (ROUND TYPE: palette): THE ROUND, RINGING. The canon - E1 at the fifth (A E G D B) answering the handpan's hook
# as a round, through B (41-65) and the relief (97-120) - was on a nylon guitar 24.5 dB under the mix: a round nobody
# heard, on the dullest string in a song that runs short of top (v13: 10-17 dB under the album above 7 kHz; the t5
# seam still -16 at 14.8 kHz). Now a TWELVE-STRING (unused on the album): the same notes on paired courses, the octave
# string ringing above each - a jangle of shimmer where the song is thin - and 9 dB up (at +4 it still sat at -19
# to -22), so the round is heard.
def crest_kit():
    a, z = b0(CREST_FULL[0]), b0(CREST_FULL[1])
    for n in ("kick", "snare"):
        P[n].ev = [(s, ln, h, min(127, v + 20)) if a <= s < z else (s, ln, h, v) for s, ln, h, v in P[n].ev]


# v28 (ROUND TYPE: section, B 41-64, ~52 s - the longest flat run, 1:28-2:24; rewritten): B TURNS EVERY EIGHT BARS.
# Harry (6 Nov 23:55, listening to t4): 'lots of contiguous music with very little change or dynamism... add subtle
# variation so it doesnt get boring' - something should move every 8-16 bars, keeping groove, key and identity.
# tools/flatness.py had B as one 56 s flat run (v21's call and answer and walking bass were too fine to register).
# Now B turns at each eight-bar phrase: 41-48 as it was; 49-56 the handpan's E1 lifts an OCTAVE (a register shift,
# sparkle over the hums and the duet's answers) and the hats give way to the ride on every eighth (the octave lift
# alone did not register); 57-60 a DROP-OUT - kit, shaker, ride, sub and bass step away and
# the lights, handpan, harp, steel and the two voices are left alone for four bars - and a brush roll swells back in
# at the end of 60; 61-64 the lights are RE-VOICED, their two top notes an octave up, opening into the rise.
B_LIFT, B_DROP, B_OPEN = (49, 57), (57, 61), (61, 65)


def b_turns():
    inside = lambda s, w: b0(w[0]) - 1e-6 <= s < b0(w[1]) - 1e-6
    P["seed"].ev = [(s, ln, f"m{midi_of(h) + 12}" if inside(s, B_LIFT) and "," not in h else h, v)
                    for s, ln, h, v in P["seed"].ev]
    P["hat"].ev = [e for e in P["hat"].ev if not inside(e[0], B_LIFT)]          # 49-56: the hats give way to the
    P["ride"].ev = [e for e in P["ride"].ev if not inside(e[0], B_LIFT)]        # ride on every eighth - a brighter
    for bar in range(*B_LIFT):                                                  # wash, the same groove
        for e in range(8):
            part("ride").add(b0(bar) + e * 0.5, 0.75, RIDE, 70 if e % 2 == 0 else 54)
    for n in ("kick", "snare", "hat", "ride", "air", "sub", "bass"):
        if n in P:
            P[n].ev = [e for e in P[n].ev if not inside(e[0], B_DROP)]
    for i in range(8):                                                # the roll back in, end of bar 60
        part("snare").add(b0(B_DROP[1]) - 2 + i * 0.25, 0.25, "s", 40 + i * 8)
    ev = []
    for s, ln, h, v in P["lights"].ev:
        if inside(s, B_OPEN) and "," in h:
            ns = sorted(h.split(","), key=midi_of)
            ns = ns[:-2] + [f"m{midi_of(x) + 12}" for x in ns[-2:]]
            h = ",".join(ns)
        ev.append((s, ln, h, v))
    P["lights"].ev = ev


# v29 (ROUND TYPE: palette - a re-orchestration): THE HOOK CHANGES HANDS. Harry (6 Nov 23:55): something should move
# every 8-16 bars, groove/key/identity kept; flatness.py still had section A as one 48 s flat run (0:40-1:28). A
# clarinet counter-line under it was tried first and did not land (chord tones in the handpan's own band: the
# texture did not change, at -12 or -7 dB). Instead, for bars 25-32 the HANDPAN RESTS and a CLARINET (a patch no
# Accretion track uses: a reed on a cylindrical bore, dark and woody low down) PLAYS ITS E1 - the same notes at the
# same times, D4 A4 C5 G4 E4 every five beats, but breathed and legato (each cycle's last E4 held to the next
# downbeat) - and at 33, as E3's steel enters, the handpan takes the hook back. The hook never leaves; its surface
# goes from struck metal to breath for one phrase.
SWAP = (25, 32)

# v30 (ROUND TYPE: whole song): THE BAND TURNS EVERY PHRASE. Harry (6 Nov 23:55): no ~30 s where nothing changes -
# something should move every 8-16 bars, groove/key/identity kept. flatness.py had three runs left after v28/v29:
# the rise (2:24-2:56, bars 66-81), the crest's second half (3:12-3:44, 88-103) and the relief (3:44-4:24, 103-122).
# Each now turns on its loud elements (presence.py: lights, sub, shaker, kick / voice, handpan, ride / voice, lights,
# sub); the voice, the hook and the harmony are untouched:
#   65-72 the rise starts from the heartbeat - hats and shaker out, the gathering kick pulse, snare, lights and bass;
#   73-80 they return, the shaker filling every sixteenth and swelling, with the glock's octaves: a second step;
#   92-96 under the sung hook the hats give way to a ride wash on every eighth;
#   105-112 the floor lifts away - sub and bass out while she hums and the handpan answers; back at 113. The relief
#   now breathes in stages: the kit out at 101, the floor away at 105, back at 113, the fall at 121. (Tried: the kit
#   leaving four bars early, at 97 - it merged with the relief's own afterglow into one still stretch, 3:28-4:00.)
RISE_THIN, RISE_FILL = (65, 72), (73, 80)
CREST_WASH = (92, 96)
# v52 (ROUND TYPE: section, the crest's second half 92-100, ~15 s - the 3:20 block, 0.57; rewritten): ALL FOUR AT
# ONCE. Here she sings E1 on 'ah' cycle after cycle - the sung hook - over E2's harp (D6 A6 F#6 C6, its seven
# sixteenths) and E3's steel (the inverted undertow) and E4's lights: the album's first full statement of the
# combined theme, the cycles converging. But measured, only she was there: the harp and the steel at -15, heard 0%,
# under v30's ride wash (-7.0, the loudest thing after her) - even with v25's +6 dB crest lane. Now, for these five
# bars, the harp and the steel come forward another 6 dB (LEADS) and the ride wash plays a third softer, so the four
# elements are heard together once: her hook, the harp's sparkle above her, the steel's slide below, the lights.
WASH_VEL = (46, 36)                  # +4 dB and (56, 44) cost half but left the harp and steel heard 24%
FLOAT = (105, 112)


def phrase_turns():
    def span(r):
        return b0(r[0]) - 1e-6, b0(r[1] + 1) - 1e-6

    def drop(names, r, keep=lambda e: False):
        lo, hi = span(r)
        for n in names:
            if n in P:
                P[n].ev = [e for e in P[n].ev if keep(e) or not (lo <= e[0] < hi)]

    drop(["hat", "air"], RISE_THIN)
    for bar in range(RISE_FILL[0], RISE_FILL[1] + 1):
        k = bar - RISE_FILL[0]
        for i in range(16):
            if i not in EUCLID_7_16:
                part("air").add(b0(bar) + i * 0.25, 0.25, "sh", 34 + 2 * k)
    drop(["hat", "ride"], CREST_WASH)
    for bar in range(CREST_WASH[0], CREST_WASH[1] + 1):
        for e in range(8):
            part("ride").add(b0(bar) + e * 0.5, 0.75, RIDE, WASH_VEL[e % 2])          # v52: softer (was 68 / 54)
    drop(["sub", "bass"], FLOAT)


def hook_changes_hands():
    lo, hi = b0(SWAP[0]), b0(SWAP[1] + 1)
    taken = sorted(e for e in P["seed"].ev if lo - 1e-6 <= e[0] < hi - 1e-6)
    P["seed"].ev = [e for e in P["seed"].ev if not (lo - 1e-6 <= e[0] < hi - 1e-6)]
    for k, (s, ln, h, v) in enumerate(taken):
        nxt = taken[k + 1][0] if k + 1 < len(taken) else min(hi, s + 2.5)
        part("clar").add(s, max(ln, nxt - s), h, min(96, v + 4))


def crest_hook():
    voice, duet = [], []
    for j, c in enumerate(SUNG_HOOK):
        beat = c * E1_CYCLE
        for i, (n, on, ln) in enumerate(E1):
            last = i == len(E1) - 1
            v = round((0.68 if on == 0 else 0.62) * (0.92 + 0.04 * j), 3)   # an answer, not a second climax
            d = {"at": round(beat + on, 4), "len": ln + (0.75 if last else 0.0), "ph": "AA1",
                 "pitch": f"m{midi_of(n)}", "vel": v}
            voice.append(d)
            if j >= 2:
                duet.append(dict(d, pitch=f"m{third_above(midi_of(n))}", vel=round(v * 0.65, 3)))
    for c in HANDS_HOOK:
        beat = c * E1_CYCLE
        for n, on, ln in E1:
            part("seed").add(beat + on, ln, n, 66 if on == 0 else 58)
            part("canon").add(beat + 2 + on, ln, f"m{midi(n) - 5}", 48)
    breath = {"at": SUNG_HOOK[0] * E1_CYCLE - 0.7, "len": 0.7, "pitch": "C4", "vel": 0.5}
    return voice, duet, breath


def main():
    write_lens()
    write_lights()
    write_felt()
    write_seed()
    write_bass()
    write_drums()
    write_sub()
    write_air()
    write_combined()
    gather_a()
    gather()
    hold_breath()
    crest_kit()
    b_turns()
    hook_changes_hands()
    phrase_turns()
    breath_before_b()
    lights_shimmer()
    everyone_sings()
    reed_answers()
    lights_out()
    reed_takes_b()
    voices_alone()
    lights_climb()
    hands_rest_for_verse()
    clarinet_finds_the_verse()
    hands_listen()
    rise_bowed()
    a_opens_upward()
    rise_pulls_back()
    hook_in_the_clear()
    smaller_room()
    hook_v, hook_d, hook_b = crest_hook()                           # v19: the hook, sung back (91-100)
    voice = sorted(sung_notes(b0(CREST), TAKES) + sung_notes(b0(101), TAKES[2:]) + hums() + hook_v + verse(),
                   key=lambda d: d["at"])
    duet = [dict(n, pitch=f"m{third_above(midi_of(n['pitch']))}", vel=round(n["vel"] * 0.8, 3))
            for n in sung_notes(b0(CREST) + 20, TAKES[2:]) + sung_notes(b0(101), TAKES[2:])] + hook_d + b2_duet()   # v7: lines 3-4 at
                                                                  # 86-90 and their return in the afterglow (101-105)
    duet.sort(key=lambda d: d["at"])
    hold_the_last(voice)                                          # v43: she holds the hook's last note to the relief
    hold_the_last(duet)
    duet = sorted(duet + warm_third(voice), key=lambda d: d["at"])   # v44: the duet hums with her, a third above
    breaths = [{"at": b0(CREST) - 0.85, "len": 0.85, "pitch": "C4", "vel": 0.55},
               {"at": b0(CREST) + 20 - 0.75, "len": 0.75, "pitch": "C4", "vel": 0.45}, hook_b]
    tempo = human_time()
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "chirpers - Accretion (chirpers IX), track 4 by chirper-three: the warm third. The storm's D minor "
                 "lifts to D major; E4's four lights (D9, Bbmaj13#11, Am11, D9sus, one per E1 cycle) carry the seed "
                 "as it assembles itself, and where every cycle meets, a human voice sings it.",
        "tempo": tempo,
        "loudness": -11,
        "volume": "0dB",
        "tail": "3s",
        "event_stable": True,
        "tracks": [
            tr("residue", "strings-synth", gain="-14dB", pan=-0.1, sends={"hall": "-6dB"},
               fx=["lp cutoff=2200"]),
            tr("lights", "cellos", gain="-12dB", sends={"hall": "-8dB"},
               fx=[{"type": "filter", "kind": "peak", "cutoff": 220, "q": 0.9, "gain": "-6dB"}]),
            tr("felt", "glock", gain="-18dB", pan=0.25, sends={"room": "-8dB"}),   # v13 palette: the felt piano -> glockenspiel
            tr("seed", "handpan", gain="-5dB", pan=-0.2, sends={"hall": "-10dB"}),
            tr("canon", "twelve-string", gain="-8dB", pan=0.35, sends={"hall": "-8dB"}),   # v51 palette: nylon -> 12-string
            tr("bass", "upright-bass", gain="-9dB",
               fx=[{"type": "filter", "kind": "peak", "cutoff": 250, "q": 1.0, "gain": "-4dB"}]),
            tr("sub", "sub-saturated", gain="-20dB"),                     # v23: the floor you can hear
            tr("air", "djembe", gain="4dB", pan=0.3, sends={"room": "-14dB"}),   # v4 palette: a hand shaker
            tr("kick", "brush-kit", gain="-8dB"),
            tr("snare", "brush-kit", gain="-4dB", pan=0.05, sends={"room": "-10dB"}),
            tr("hat", "brush-kit", gain="-2dB", pan=0.2),
            tr("ride", "modal-ride", gain="-24dB", pan=-0.25, sends={"room": "-12dB"}),   # v15 palette (was brush-kit rd)
            {"name": "voice", "patch": VOICE, "gain": "-8dB", "pan": 0.0,
             "sends": {"hall": "-9dB", "dly": "-16dB"}, "notes": voice},
            tr("e2", "harp", gain="-17dB", pan=0.4, sends={"hall": "-10dB", "dly": "-16dB"},     # v2: listed last
               fx=[CREST_FX], auto={"cr": {"points": crest_lane()}}),                         # v25
            tr("e3", "pedal-steel", gain="-11dB", pan=-0.35, sends={"hall": "-10dB"},
               fx=[CREST_FX], auto={"cr": {"points": steel_lane()}}),
            {"name": "duet", "patch": VOICE2, "gain": "-15dB", "pan": 0.18, "sends": {"hall": "-8dB"}, "notes": duet},
            {"name": "breath", "patch": BREATH_AIR, "gain": "2dB", "pan": 0.0, "sends": {"room": "-12dB"},
             "notes": breaths},
            tr("e3hi", E3HI_PATCH, gain=E3HI_GAIN, pan=0.35, sends={"hall": "-8dB"}),     # v8: E3 up in the rise; v57 violin
            tr("steel", {"extends": "pedal-steel play.glide=700ms"}, gain="-13dB", pan=0.15,
               sends={"hall": "-6dB"}),                              # v11: the lens's bent third
            tr("clar", "clarinet", gain="-5dB", pan=-0.3, sends={"hall": "-10dB"}),   # v29
            {"name": "hum1", "patch": hum1_patch(), "gain": "-8dB", "pan": 0.0, "fx": ["lp cutoff=4000"],
             "sends": {"hall": "-9dB"}, "notes": first_hum()},                    # v35 (last: event_stable)
            {"name": "bowl", "patch": "singing-bowl", "gain": BOWL_GAIN, "pan": -0.15, "notes": warm_stone()},   # v50
            {"name": "chimes", "patch": "chimes", "gain": CHIME_GAIN, "pan": 0.4, "notes": breeze()},             # v54 (last)
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.8s mix=1 predelay=6ms", "hp cutoff=200"]},
                  "hall": {"fx": ["reverb kind=hall decay=3.2s mix=1 predelay=20ms", "hp cutoff=180"]},
                  "dly": {"fx": ["delay time=3/8 mix=1 feedback=0.3", "hp cutoff=400", "lp cutoff=5000"]}},
        # v20 (ROUND TYPE: whole song): OPEN THE WINDOW. compscore --bands: t4 ran +6.5 to +9.4 dB hot from 468 to
        # 1643 Hz and -8 to -11.5 dB dark above 6.7 kHz against the album - boxy and dull, the whole song. Few
        # fundamentals live there (the harp and glock, both quiet): it is the harmonics and formants of the handpan,
        # cellos, strings and voice. So the master takes a broad two-octave scoop centred on 900 Hz (-4 dB, Q 0.6)
        # and its 6 kHz shelf rises from +5 to +8 dB: the same warm song, with air in it. (Milder, -3 / +7 dB: 95.65 /
        # 95.32 - the same structure cost, less spectrum.)
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=240 q=0.8 gain=-3dB",
                                                   "peak cutoff=900 q=0.6 gain=-4dB",
                                                   "highshelf cutoff=6000 gain=8dB"]},
                          {"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "8ms",
                           "release": "120ms", "makeup": "0dB"}]},
    }
    lead_lanes(song)
    hold_lanes(song)
    arc(song)
    answer_closes_in(song)
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print(f"wrote {OUT} bars {BARS} crest {CREST} voice notes {len(voice)}")


if __name__ == "__main__":
    main()
