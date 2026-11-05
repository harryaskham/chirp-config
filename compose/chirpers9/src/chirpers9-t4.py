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
            toks.append(f"{head}/{ln:.5g}b@{vel}")
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
E4 = [("D9", ("D2", "A2", "F#3", "C4", "E4")),
      ("Bbmaj13#11", ("Bb1", "F2", "D3", "A3", "C4", "E4")),
      ("Am11", ("A1", "E2", "C3", "G3", "B3", "D4")),
      ("D9sus", ("D2", "A2", "C3", "G3", "B3", "E4"))]
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


def write_lights():
    vel = {"A": 62, "B": 70, "rise": 76, "crest": 92, "relief": 82, "fall": 60}
    beat = b0(17)
    while beat < b0(BARS + 1) - 0.01:
        bar = int(beat // BPB) + 1
        s = sec_of(bar)
        v = vel[s] + (min(14, (bar - 65) * 1) if s == "rise" else 0)
        if s == "fall":
            v = max(30, vel["fall"] - (bar - 121) * 2)
        k, name, notes = chord_at(beat)
        part("lights").add(beat, E1_CYCLE, head(notes), v)
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
        n = n[:-1] + str(int(n[-1]) + 1)                    # an octave up, out of the cellos' way
        v = 44 + (8 if pos == 0 else 0) + (10 if sec_of(bar) == "crest" else 0)
        part("felt").add(beat, 0.5, n, v)


def write_seed():
    # E1 ASSEMBLES ITSELF: from the downbeat, one note more every two cycles, then whole; later in other shapes
    cyc = 0
    beat = 0.0
    while beat < b0(121) - 0.01:
        bar = int(beat // BPB) + 1
        s = sec_of(bar)
        k = min(5, 1 + cyc // 2)
        if s in ("crest",):
            beat += E1_CYCLE; cyc += 1
            continue                                         # the voice carries it at the crest
        cell = E1[:k] if s in ("lens", "A") else E1
        for n, on, ln in cell:
            v = 70 if on == 0 else 60
            if s == "relief":
                v += 6
            part("seed").add(beat + on, ln, n, v)
        if s in ("B", "rise", "relief"):
            # a second voice in canon two beats behind, a fifth below (A G E D B): the cell answering itself
            for n, on, ln in E1:
                m = midi(n) - 7
                part("canon").add(beat + 2 + on, ln, f"m{m}", 50)
        beat += E1_CYCLE
        cyc += 1
    # the fall: E1 augmented x2, the last statement handed over the seam
    beat = b0(121)
    while beat < b0(BARS + 1) - 10:
        for n, on, ln in E1:
            part("seed").add(beat + 2 * on, 2 * ln, n, 54)
        beat += 2 * E1_CYCLE


def write_bass():
    beat = b0(17)
    while beat < b0(129) - 0.01:
        k, name, notes = chord_at(beat)
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
E2_MAJ = [("D5", 0, 100), ("A5", 2, 76), ("F#5", 3, 88), ("C5", 5, 70)]          # sixteenth steps of 7
E3_INV = [("D3", 0.0, 0.75), ("D3", 0.75, 0.75), ("D2", 1.5, 0.5), ("C#3", 2.0, 0.5), ("C#3", 2.5, 0.75),
          ("F#3", 3.25, 0.75), ("E3", 4.0, 0.75), ("E3", 4.75, 0.75), ("A2", 5.5, 0.5), ("E2", 6.0, 1.0)]


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
    beat = phase_start(7.0, 41)
    while beat < b0(121) - 0.01:
        s = sec_of(int(beat // BPB) + 1)
        for n, on, ln in E3_INV:
            part("e3").add(beat + on, ln, n, 74 + vel.get(s, -20))
        beat += 7.0


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
    low = {"D9": "D1", "Bbmaj13#11": "Bb1", "Am11": "A1", "D9sus": "D1"}
    beat = b0(41)
    while beat < b0(AFTERGLOW[0]) - 0.01:
        k, name, notes = chord_at(beat)
        part("sub").add(beat, E1_CYCLE - 0.25, low[name], 96 if sec_of(int(beat // BPB) + 1) == "crest" else 84)
        beat += E1_CYCLE


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
            part("ride").add(t, 1.0, "rd", 64)
            part("ride").add(t + 1.5, 1.0, "rd", 52)
            part("ride").add(t + 3, 1.0, "rd", 56)
    part("snare").add(b0(CREST), 2.0, "sw", 100)                 # the swish at the crest


def sung_notes(at_beat, takes, transpose=0):
    out = []
    t = at_beat
    for tk in takes:
        for n in tk["notes"]:
            d = {"at": round(t + n["at"], 4), "len": n["len"], "ph": n["ph"],
                 "pitch": f"m{midi_of(n['pitch']) + transpose}", "vel": n["vel"]}
            if n.get("expr_path"):
                d["expr_path"] = n["expr_path"]
            out.append(d)
        t += 10.0                                                   # each line is E1 augmented: 10 beats
    return out


def midi_of(p):
    return int(float(p[1:])) if p.startswith("m") else midi(p)


VOICE = {"about": "t4's voice: a warm, close, human singer - slightly larger tract, soft breath, covered vowels",
         "play": {"mono": True, "glide": "40ms"},
         "synth": {"layers": [{"type": "voice", "tract": 1.02, "breath": 0.12, "formant_bw": 1.6, "ph_soft": 0.35,
                               "consonant_level": "-4dB", "pulse_rate": 5}],
                   "pitch": {"value": 0, "mod": [{"src": "expr.f0", "amount": 0.01}]},
                   "amp": {"a": "40ms", "d": "0s", "s": 1, "r": "250ms"}}}


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
    hold_breath()
    voice = sung_notes(b0(CREST), TAKES) + sung_notes(b0(101), TAKES[2:])
    tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": f"{b0(17):g}b", "bpm": SEAM_IN},
             {"at": f"{b0(121):g}b", "bpm": SEAM_OUT, "ramp": True}]
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
            tr("felt", "piano-muted", gain="-16dB", pan=0.25, sends={"room": "-8dB"}),
            tr("seed", "handpan", gain="-9dB", pan=-0.2, sends={"hall": "-10dB"}),
            tr("canon", "kalimba", gain="-17dB", pan=0.35, sends={"hall": "-8dB"}),
            tr("bass", "upright-bass", gain="-9dB",
               fx=[{"type": "filter", "kind": "peak", "cutoff": 250, "q": 1.0, "gain": "-4dB"}]),
            tr("sub", SUB, gain="-14dB"),
            tr("air", "djembe", gain="4dB", pan=0.3, sends={"room": "-14dB"}),   # v4 palette: a hand shaker
            tr("kick", "brush-kit", gain="-8dB"),
            tr("snare", "brush-kit", gain="-10dB", pan=0.05, sends={"room": "-10dB"}),
            tr("hat", "brush-kit", gain="-16dB", pan=0.2),
            tr("ride", "brush-kit", gain="-15dB", pan=-0.25),
            {"name": "voice", "patch": VOICE, "gain": "-8dB", "pan": 0.0,
             "sends": {"hall": "-9dB", "dly": "-16dB"}, "notes": voice},
            tr("e2", "harp", gain="-17dB", pan=0.4, sends={"hall": "-10dB", "dly": "-16dB"}),     # v2: listed last
            tr("e3", "vibes", gain="-16dB", pan=-0.35, sends={"hall": "-10dB"}),
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.8s mix=1 predelay=6ms", "hp cutoff=200"]},
                  "hall": {"fx": ["reverb kind=hall decay=3.2s mix=1 predelay=20ms", "hp cutoff=180"]},
                  "dly": {"fx": ["delay time=3/8 mix=1 feedback=0.3", "hp cutoff=400", "lp cutoff=5000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=240 q=0.8 gain=-3dB",
                                                   "highshelf cutoff=6000 gain=5dB"]},
                          {"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "8ms",
                           "release": "120ms", "makeup": "0dB"}]},
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print(f"wrote {OUT} bars {BARS} crest {CREST} voice notes {len(voice)}")


if __name__ == "__main__":
    main()
