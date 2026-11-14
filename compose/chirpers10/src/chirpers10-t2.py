#!/usr/bin/env python3
"""chirpers10-t2 "Odd Sympathy" (chirper-zero): one riff and two clocks.

In 1665 Huygens hung two pendulum clocks from one beam and found that, however he started them, within half an hour they
swung exactly against each other; he called it "an odd kind of sympathy". This is that, for two guitars.

Common Time (track 1) keeps one pulse and turns three cells of different lengths under it. This piece is the other way
round: ONE cell, one bar long, on two guitars, left and right, each with its own clock. They start in step. The right
guitar's clock runs a hair fast: it slips ahead of the left by a sixteenth, holds there, slips again, and so on, each
hold a canon of the riff with itself at a new distance, until it is half a bar ahead: exactly against the left. The riff
is written so that there, and only there, the two halves fit: every sixteenth of the bar has one guitar on it and never
both (the riff's second half is the negative of its first). What was a riff with holes is a machine with none.

The slips are the engine's track `warp` (the right-hand tracks' own clock against the song's); nothing is shifted by hand.

v1 is the SKELETON (Harry, 14 Nov: "should skeleton it and then climb both"): the whole shape standing, bare.
"""
import json
import math
import os

OUT = os.environ.get("C10T2_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t2.yaml"))
BPM = 108
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# THE RIFF: sixteen sixteenths. (position, length, kind): c a palm-muted chug on the open low string, o the string open,
# h a hook note. Its attacks are 0 1 3 6 | 10 12 13 15: of every pair of sixteenths half a bar apart exactly one is struck.
# Every note is short and the gaps are real rests (a riff with holes): the piece is about what fills them.
RIFF = [(0, 1, "c"), (1, 1, "c"), (3, 2, "o"), (6, 2, "h0"), (10, 1.5, "h1"), (12, 1, "c"), (13, 1, "c"), (15, 1, "h2")]
ATTACKS = [p for p, _, _ in RIFF]
assert all((p in ATTACKS) != ((p + 8) % 16 in ATTACKS) for p in range(16)), "the two halves must be each other's negative"
# the hook's notes are three of Common Time's four (Ab Gb B C over F): the tritone, the minor third, the fifth
HOOK = [F1 + 6, F1 + 3, F1 + 7]
CHUGS = [p for p, _, k in RIFF if k == "c"]

# THE FORM, in bars (4/4). The right guitar's lead over the left, in sixteenths, at each station.
FORM = [
    ("one clock", 0, 8, 0),          # the left guitar alone and a pendulum; the bass and kick join
    ("in step", 8, 24, 0),           # both, together
    ("slip", 24, 28, None),
    ("a sixteenth", 28, 32, 1),
    ("slip", 32, 36, None),
    ("an eighth", 36, 48, 2),
    ("slip", 48, 50, None),
    ("three", 50, 56, 3),
    ("slip", 56, 58, None),
    ("a quarter", 58, 74, 4),
    ("let go", 74, 98, None),        # no beam: clean guitars, the right one drifting all the way to half a bar
    ("against", 98, 122, 8),         # exactly against each other: the bar is full
    ("two clocks", 122, 130, 8),     # the guitars alone, then the ticks
]
NB = 130
# the right-hand clock (track `warp`): stretches in turn from the start; `to` is its shift in beats, negative = ahead
WARP = [
    {"over": "96b", "to": 0},
    {"over": "16b", "to": -0.25, "curve": "smooth"}, {"over": "16b", "to": -0.25},
    {"over": "16b", "to": -0.5, "curve": "smooth"}, {"over": "48b", "to": -0.5},
    {"over": "8b", "to": -0.75, "curve": "smooth"}, {"over": "24b", "to": -0.75},
    {"over": "8b", "to": -1.0, "curve": "smooth"}, {"over": "64b", "to": -1.0},
    {"over": "88b", "to": -2.0, "curve": "linear"},          # bars 74-96: the long drift, a little over 1% fast
]

# v2: THE DRIFT GETS A SHAPE (bars 74-98; the window the section map called static). Three things, "" = v1:
# (1) the ground moves under the drifting ticks, a step at a time: F, Eb, Db, then C, the dominant, held until the band
#     comes back on F. The clocks arrive against each other ON the dominant and resolve with the band.
# (2) the pendulum lets go too. From bar 80 its tick-tock is a Risset rhythm (the engine's track `risset`, two copies an
#     octave of tempo apart, a cycle of four bars): it speeds up for ever and is never faster. On each fourth bar line the
#     tick is back on the bar, at the speed it started; at bar 96, where the guitars lock, the plain pendulum has it again.
# (3) the last six bars build: a dominant pedal on the bass, the kick on one and three, floor tom into the fill.
DRIFT = os.environ.get("C10T2_DRIFT", "0,-2,-4,-5;16:2;0.5")       # the roots' semitones ; risset cycle beats : layers ; pedal velocity
# v3: THE TWINS (palette round). The piece is one riff on two clocks, so the two guitars are ONE guitar twice: the library
# patch `ct-twin` on both sides (Common Time's rigs are a different amp a side), each with its own cone. It is dry: no
# plate, no eq after the cabinet, a gate; a rest is silence, so a canon of the riff with itself takes turns. What the two
# share is a small room on their bus, the beam the two clocks hang from.
# patch : left cone : right cone : track gain dB ; the room's kind : decay : mix ; master make-up dB. "" = v2 (Common
# Time's tight rig). The guitars sit 0.8 dB lower than v2's (alone, LUFS): the mix read 2 to 3 dB over the records at
# 2-4 kHz in every heavy window, and that band is the guitars'. The master makes up what the mix lost.
TWIN = os.environ.get("C10T2_TWIN", "ct-twin:4:5:3.2;room:0.35s:0.06;0.5")
# v4: THE HOLD AN EIGHTH APART (bars 36-48; the section map's "static" window). Until now every hold was the same riff
# on F with a different kick. At an eighth apart the canon does something no other distance does: the right guitar plays
# each hook note and the left answers it an eighth later (4 and 6, 8 and 10, 13 and 15). So this hold is built on the
# eighth, and on a ground of its own:
# (1) it moves to Ab, the hook's minor third: the first time the ground moves under the heavy guitars. The right guitar,
#     being ahead, gets there an eighth before the bar line.
# (2) the snare answers itself an eighth later too (a ghost stroke after each backbeat), the hat plays eighths, a china
#     marks the bar line.
# (3) the bass plays BOTH guitars' notes: the one line the two make at this distance.
# Two mix tries were measured and NOT taken (fields four and five, off by default): the bass track up 1.2 dB over the
# hold (on Ab the mix reads 1.6 dB under the records at 120-250 Hz) moved nothing, because the bass's bus compressor
# takes it back; and a 13 kHz low-pass on the hat cost the top it had just gained (8-16 kHz -0.1 -> -0.8).
# the root's semitones above F ; the ghost's velocity ; the china's velocity [; the bass's dB there ; the hat's low-pass Hz]. "" = v3.
EIGHTH = os.environ.get("C10T2_EIGHTH", "3;0.45;0.5")
# v5: TWO VOICES (whole-song round). The piece had no voice and no tune: a riff and its canon. It gets the same idea in
# speech: two voices, left and right, twins like the guitars, saying the same four lines, a syllable to each attack of
# the riff. The right voice is on the right guitar's clock (the same `warp`), so nothing is placed by hand:
#   in step (0:36)            the four lines SPOKEN (voice-talk), the two voices together: one voice
#   a quarter apart (2:13)    the four lines again, spoken, the right voice a beat ahead: each syllable said twice
#   against (3:46)            the last line only, BARKED (Common Time's bark), over and over: half a bar apart the two
#                             voices' syllables interlock as the guitars' notes do, sixteen to the bar, alternating sides
#   I cannot hear you through the wall / only the floor between us moves / whatever way you lean I lean /
#   against you until we agree
# (two clocks on one beam, from the inside; Huygens is not named.) Spoken first, because a recogniser reads the spoken
# voice 18 words of 24 on this rhythm and the bark 14: the words are learnt spoken, then barked.
# the talk's gain ; the bark's gain ; pan ; the bark's hall send ; dB the guitars' bus ducks under the talk. "" = v4.
VOICE = os.environ.get("C10T2_VOICE", "-6dB;3dB;0.5;-18dB;2")
# The spoken voice's eq. A clean male voice has a body the records' harsh voices do not (110 Hz and its harmonics up to
# the first formant): with Common Time's eq (hp 120, 300 Hz -6) the voiced holds read 7 dB over the records' voiced
# passages at 250-500 Hz; a high-pass alone (220, 450, 650 Hz) left 3 to 5 and cost words; this notch leaves 2 to 3
# and the recogniser reads as many words as before (18 of 24).
TALKEQ = os.environ.get("C10T2_TALKEQ", "hp cutoff=300|peak cutoff=400 q=1 gain=-12dB")
VOICE_LINES = [      # syllables (ARPAbet, from `chirp tts --print`); "up" = the line starts on the sixteenth before the bar line
    ("AY1|K AE1|N AA0 T|HH IY1 R|Y UW1|TH R UW1|DH AH0|W AO1 L", "up"),
    ("OW1 N|L IY0|DH AH0|F L AO1 R|B IH0|T W IY1 N|AH1 S|M UW1 V Z", os.environ.get("C10T2_L2", "down")),
    ("W AH2|T EH1|V ER0|W EY1|Y UW1|L IY1 N|AY1|L IY1 N", "up"),
    ("AH0|G EH1 N S T|Y UW1|AH0 N|T IH1 L|W IY1|AH0|G R IY1", "up"),
]
# v5 also: THE KIT'S TOP FALLS AS THE RECORDS' DOES (chirp-eco's reading by thirds: level with the records to 11.6 kHz,
# then ours stayed flat where theirs fall: +1.6 dB at 11.6-13.7 kHz, +4.7 at 13.7-16, +7.4 at 16-20; every piece of the
# kit carried it). A low-pass on the drums' bus and the overheads': Hz ; q. "" = v4.
DTOP = os.environ.get("C10T2_DTOP", "14500;0.7")
T = {}


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def riff(tr, b0, b1, vel=0.85, up=0, clean=False, ramp=None, root=0):
    """The riff on a track, bars b0..b1. Heavy: chugs muted (`root` semitones above F). Clean (`up` semitones higher):
    every note a short tick."""
    up = up + root
    for b in range(b0, b1):
        v = vel * (ramp[0] + (ramp[1] - ramp[0]) * (b - b0) / max(1, b1 - b0 - 1)) if ramp else vel
        for p, ln, kind in RIFF:
            t = b * 16 + p
            if kind == "c":
                if clean:
                    add(tr, t, 1, F1 + up, v * 0.8)
                else:
                    add(tr, t, ln, F1 + root, v * (1.0 if p in (0, 12) else 0.9), pm=1)
            elif kind == "o":
                add(tr, t, 1 if clean else ln, F1 + up + (12 if clean else 0), v)
            else:
                add(tr, t, 2 if clean else ln, HOOK[int(kind[1])] + up, v * 1.05)


def bass(b0, b1, lead=0, vel=0.9, root=0, union=False):
    """The bass keeps the LEFT clock; where the right guitar is locked `lead` sixteenths ahead it takes its chugs too
    (`union`: every note of the right guitar's that the left has not, so the bass plays the two guitars' one line)."""
    for b in range(b0, b1):
        seen = set()
        for p, ln, kind in RIFF:
            add("bass", b * 16 + p, ln, root + (F1 if kind in "co" else HOOK[int(kind[1])]), vel)
            seen.add(p)
        if lead:
            for p, ln, kind in RIFF:
                q = (p - lead) % 16
                if q not in seen and (kind == "c" or union):
                    add("bass", b * 16 + q, 1, root + (F1 if kind in "co" else HOOK[int(kind[1])]), vel * 0.85)


def say(line, bar, kind="talk", ring=True):
    """One line on both voices of a kind (spoken `tl`/`tr`, barked `vl`/`vr`): a syllable to each attack of the riff,
    none longer than two sixteenths and a bit (short syllables read better, and take turns better)."""
    phs, how = VOICE_LINES[line]
    pos = ATTACKS if how == "down" else [-1] + ATTACKS[:-1]
    for i, ph in enumerate(phs.split("|")):
        ln = (pos[i + 1] - pos[i]) if i < 7 else (6 if ring else (1 if how == "down" else 2))
        ln = min(ln, 2.2) if not (i == 7 and ring) else ln
        pitch = nm(65) if kind == "bark" else ("m41.5" if i == 7 else "m45.5")       # the talk falls at the end of a line
        for tr in (("vl", "vr") if kind == "bark" else ("tl", "tr")):
            T.setdefault(tr, []).append({"at": round((bar * 16 + pos[i]) / 4, 4), "len": round(ln * 0.9 / 4, 4), "pitch": pitch, "vel": 0.9, "ph": ph})


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "g": "snare", "h": "hat", "c": "cym", "x": "cym", "cch": "cym", "rb": "ride", "rd": "ride"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece in ("h", "rb", "rd") else 0.25, "pitch": piece, "vel": round(vel, 3)})


def groove(b0, b1, lead, snare, cym, kvel=0.92):
    """A station's beat: the kick on every chug of either guitar (and the left's open string), the snare on `snare`,
    a cymbal on the quarter."""
    kicks = sorted(set(CHUGS + [3]) | {(p - lead) % 16 for p in CHUGS})
    for b in range(b0, b1):
        for p in kicks:
            drum("k", b * 16 + p, kvel * (1.0 if p % 4 == 0 else 0.9))
        for p in snare:
            drum("s", b * 16 + p, 0.95)
        for p in range(0, 16, 4):
            drum(cym, b * 16 + p, 0.6 if p == 0 else 0.5)
    drum("c", b0 * 16, 0.9)


def groove_eighth(b0, b1, lead, ghost, china):
    """The beat of the hold an eighth apart: built on the eighth. The kick as everywhere (every chug of either guitar);
    the snare on two and four, each answered a ghost stroke an eighth later, as each hook note is; the hat in eighths."""
    kicks = sorted(set(CHUGS + [3]) | {(p - lead) % 16 for p in CHUGS})
    for b in range(b0, b1):
        for p in kicks:
            drum("k", b * 16 + p, 0.92 * (1.0 if p % 4 == 0 else 0.9))
        for p in (4, 12):
            drum("s", b * 16 + p, 0.95)
            drum("g", b * 16 + p + 2, ghost)
        for p in range(0, 16, 2):
            drum("h", b * 16 + p, 0.62 if p % 4 == 0 else 0.48)
        drum("x", b * 16, china)
    drum("c", b0 * 16, 0.9)


def fill(b, kind="toms"):
    """The last half bar before bar `b`."""
    if kind == "toms":
        for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
            drum(pc, b * 16 - 8 + i, 0.6 + 0.045 * i)
    else:
        for i in range(8):
            drum("s", b * 16 - 8 + i, 0.5 + 0.06 * i)


def pendulum(b0, b1, vel=0.42):
    for b in range(b0, b1):
        drum("rb", b * 16, vel * 1.12)       # tick
        drum("rb", b * 16 + 8, vel)          # tock


def compose():
    # one clock: no introduction (Common Time has the long wait; this starts). The left guitar alone with the riff and a
    # pendulum; then the bass and the kick under it
    pendulum(0, 8)
    T.setdefault("home", []).append({"at": 0, "len": 32.2, "pitch": "F1", "vel": 0.55})
    riff("gl", 0, 8, vel=0.85)
    bass(4, 8)
    for b in range(4, 8):
        for p in CHUGS:
            drum("k", b * 16 + p, 0.85)
        for p in range(0, 16, 4):
            drum("h", b * 16 + p, 0.45)
    fill(8)
    # in step
    riff("gl", 8, 24)
    riff("gr", 8, 24)
    bass(8, 24)
    groove(8, 24, 0, snare=(8,), cym="x")
    for name, b0, b1, lead in FORM[2:10]:
        if lead == 2 and EIGHTH:         # the hold an eighth apart: its own ground and its own beat (v4)
            root, ghost, china = [float(x) for x in EIGHTH.split(";")[:3]]
            riff("gl", b0, b1, root=int(root))
            riff("gr", b0, b1, root=int(root))
            bass(b0, b1, lead, root=int(root), union=True)
            groove_eighth(b0, b1, lead, ghost, china)
            continue
        riff("gl", b0, b1)
        riff("gr", b0, b1)
        bass(b0, b1, lead or 0)
        if lead is None:                 # a slip: the beat thins to a kick on the bar line and a hat, so the slip is heard
            for b in range(b0, b1):
                drum("k", b * 16, 0.85)
                for p in range(0, 16, 4):
                    drum("h", b * 16 + p, 0.45)
            fill(b1, "snare" if b1 - b0 < 4 else "toms")
        else:
            groove(b0, b1, lead, snare=(4, 12) if lead in (2, 4) else (8,), cym="h" if lead == 2 else "rd" if lead == 4 else "x")
    # let go: the heavy guitars stop; two clean guitars tick the riff, the right one drifting from a quarter to half a bar
    # ahead; the swarm (sixteen oscillators finding a common phase) locks as they arrive
    if DRIFT:
        roots = [int(x) for x in DRIFT.split(";")[0].split(",")]
        edges = [74, 80, 86, 92, 98]
        lvl = lambda b: 0.8 + 0.3 * (b - 74) / 23
        for r, b0, b1 in zip(roots, edges, edges[1:]):
            for tr in ("cl", "cr"):
                riff(tr, b0, b1, vel=0.5, up=24 + r, clean=True, ramp=(lvl(b0), lvl(b1 - 1)))
            T.setdefault("home", []).append({"at": b0 * 4, "len": (b1 - b0) * 4 + 0.2, "pitch": nm(F1 + r), "vel": 0.55})
            for iv in (12, 19):
                T.setdefault("air", []).append({"at": b0 * 4, "len": (b1 - b0) * 4 + 0.2, "pitch": nm(F1 + r + iv), "vel": 0.45})
        pendulum(74, 80)
        T["tick"] = [{"at": 0, "len": 2.0, "pitch": "rb", "vel": 0.47}, {"at": 2, "len": 2.0, "pitch": "rb", "vel": 0.42}]   # one tick-tock: the pattern the Risset rhythm turns
        pendulum(96, 98)
        pv = float(DRIFT.split(";")[2])
        for b in range(86, 98):
            drum("k", b * 16, 0.4 + 0.03 * (b - 86))
            if b >= 92:
                drum("k", b * 16 + 8, 0.35 + 0.03 * (b - 86))
                T.setdefault("bass", []).append({"at": b * 4, "len": 3.9, "pitch": nm(F1 + 7), "vel": round(pv + 0.04 * (b - 92), 3)})
        for i, t in enumerate(range(96 * 16, 98 * 16 - 8, 4)):
            drum("ft", t, 0.4 + 0.05 * i)
    else:
        for tr in ("cl", "cr"):
            riff(tr, 74, 98, vel=0.5, up=24, clean=True, ramp=(0.8, 1.1))
        pendulum(74, 98)
        for b in range(86, 98):
            drum("k", b * 16, 0.4 + 0.03 * (b - 86))
        T.setdefault("home", []).append({"at": 74 * 4, "len": 96.2, "pitch": "F1", "vel": 0.55})
        for n in ("F2", "C3"):
            T.setdefault("air", []).append({"at": 74 * 4, "len": 96.2, "pitch": n, "vel": 0.45})
    for n in ("F3", "C4"):
        T.setdefault("swarm", []).append({"at": 74 * 4, "len": 96.0, "pitch": n, "vel": 0.7})
    fill(98)
    # against: half a bar apart. Every sixteenth has one guitar on it
    riff("gl", 98, 122, vel=0.9)
    riff("gr", 98, 122, vel=0.9)
    bass(98, 122, 8, vel=0.95)
    groove(98, 122, 8, snare=(4, 12), cym="x")
    for b in range(102, 122, 4):
        drum("c", b * 16, 0.85)
    if VOICE:
        for i in range(4):                       # in step: the four lines, together
            say(i, 16 + 2 * i)
        for i in range(4):                       # a quarter apart: the four lines, each syllable said twice a beat apart
            say(i, 60 + 2 * i)
        say(2, 68)
        say(3, 70)
        for b0 in (102, 110, 118):               # against: the last line, four times round, the two voices interlocked
            for k in range(4):
                say(3, b0 + k, "bark", ring=(k == 3))
    # two clocks: the guitars alone, still against each other; then only the ticks
    riff("gl", 122, 126, vel=0.85)
    riff("gr", 122, 126, vel=0.85)
    drum("c", 122 * 16, 0.9)
    pendulum(122, 130)
    for tr in ("cl", "cr"):
        riff(tr, 126, 130, vel=0.45, up=24, clean=True, ramp=(1.0, 0.6))
    T.setdefault("home", []).append({"at": 126 * 4, "len": 16.0, "pitch": "F1", "vel": 0.5})


# the heavy rig: Common Time's tight rig on the engine's own cabinet (sounds.md), one a side
HEAVY = (" fx.0.mix=0 synth.layers.0.soft=expr.pm fx.2.tight=220 fx.3.mix=0"
         + "".join(f" fx.4.bands.{i}.gain=0dB" for i in range(7)))
CLEAN = "ct-clean synth.layers.0.inharm=0.00008"
DRIP = {"type": "reverb", "kind": "spring", "drip": 1, "decay": "1.8s", "mix": 0.22}     # the spring that drips (engine feature 5)
# the swarm, as in Common Time: sixteen saws to a note pulled toward a common phase by a coupling the `sync` lane sets
SWARM = {"about": "chirper-zero: the swarm - sixteen saws to a note, each at its own pitch (60 cents' spread), pulled toward their common phase by a coupling the track's `sync` lane sets (0 a crowd, 1 the critical point, 3 locked); a low-pass opens as they agree. As in Common Time (track 1).",
         "synth": {"layers": [{"type": "kuramoto", "kuramoto": {"count": 16, "spread": 60, "coupling": {"value": 0, "mod": [{"src": "auto.sync", "amount": 1}]}}}],
                   "filters": [{"kind": "lp", "cutoff": {"value": 350, "mod": [{"src": "sync", "amount": 2.6}]}}], "amp": {"a": "1.5s", "d": 0, "s": 1, "r": "3s"}}, "gain": "-9.5dB"}


def risset_tick():
    """The Risset pendulum's track settings. With two copies the one at the written speed starts a cycle alone, part-way
    through the pattern; the track starts early by just as much as puts its first tick on bar 80's bar line (and so on
    every fourth bar line after, where the cycle comes round)."""
    c, k = DRIFT.split(";")[1].split(":")
    c, k = float(c), int(k)
    assert k == 2, "the hand-over to the plain pendulum is seamless only with two copies"
    L = 4.0                                                    # the pattern: a tick and a tock, four beats
    p0 = (0.5 * c / math.log(2)) % L                           # where in the pattern the written-speed copy starts
    lead = c * math.log2(1 + (L - p0) / (c / math.log(2)))     # beats until its first tick
    return {"at": f"{80 * 4 - lead:.4f}b", "risset": {"cycle": f"{c:g}b", "layers": k, "length": f"{16 * 4 + lead:.4f}b"}}


def song():
    compose()
    cab = lambda cone: [{"type": "cab", "model": "4x12-modern", "mic": 0.25, "distance": 0.15, "cone": cone}]
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    b = lambda bar: f"{bar * 4}b"
    eb, hlp = ([float(x) for x in EIGHTH.split(";")[3:5]] if EIGHTH and len(EIGHTH.split(";")) > 4 else (0, 0))
    vo = VOICE.split(";") if VOICE else None
    dtop = [f"lp cutoff={DTOP.split(';')[0]} q={DTOP.split(';')[1]}"] if DTOP else []
    tw = TWIN.split(";")[0].split(":") if TWIN else None
    beam = TWIN.split(";")[1].split(":") if TWIN else None
    spec = [
        *([{"name": "gl", "patch": f"{tw[0]} fx.2.cone={tw[1]}", "gain": f"{tw[3]}dB", "pan": -1, "out": "gtrs"},
           {"name": "gr", "patch": f"{tw[0]} fx.2.cone={tw[2]}", "gain": f"{tw[3]}dB", "pan": 1, "out": "gtrs", "warp": WARP}] if TWIN else
          [{"name": "gl", "patch": "ct-chug-l" + HEAVY, "gain": "3.3dB", "pan": -1, "out": "gtrs", "fx": cab(12)},
           {"name": "gr", "patch": "ct-chug-r" + HEAVY, "gain": "3.3dB", "pan": 1, "out": "gtrs", "fx": cab(13), "warp": WARP}]),
        {"name": "cl", "patch": CLEAN, "gain": "1dB", "pan": -0.7, "sends": {"hall": "-9dB"}, "fx": [DRIP]},
        {"name": "cr", "patch": CLEAN, "gain": "1dB", "pan": 0.7, "sends": {"hall": "-9dB"}, "fx": [DRIP], "warp": WARP},
        *([{"name": tr, "patch": "voice-talk", "gain": vo[0], "pan": sgn * float(vo[2]),
            "fx": [{"type": "eq", "bands": TALKEQ.split("|")}],
            **({"warp": WARP} if tr == "tr" else {})} for tr, sgn in (("tl", -1), ("tr", 1))] if VOICE else []),
        *([{"name": tr, "patch": "kidman synth.layers.0.diction=2 synth.layers.0.speech=1", "gain": vo[1], "pan": sgn * float(vo[2]), "sends": {"hall": vo[3]},
            "fx": [{"type": "eq", "bands": ["hp cutoff=440", "peak cutoff=1400 q=0.8 gain=4.5dB", "peak cutoff=5500 q=1.2 gain=-4dB", "highshelf cutoff=7000 gain=-6dB"] + dtop}],      # the bark's hiss falls with the kit's top
            **({"warp": WARP} if tr == "vr" else {})} for tr, sgn in (("vl", -1), ("vr", 1))] if VOICE else []),
        {"name": "bass", "patch": "ct-bass", "gain": {"value": "0.5dB", "mod": [{"src": "auto.hold", "amount": 1}]} if EIGHTH and eb else "0.5dB", "pan": 0, "out": "low",
         **({"auto": {"hold": {"points": [["0b", 0], [b(35.9), 0], [b(36), eb], [b(48), eb], [b(48.1), 0]], "curve": 0}}} if EIGHTH and eb else {})},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "8dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-3dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"},
         "fx": [{"type": "eq", "bands": air[0]["bands"] + [f"lp cutoff={hlp:g} q=0.7"]}] if EIGHTH and hlp else air},
        {"name": "ride", "patch": kit, "gain": "6dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "tick", "patch": kit, "gain": "6dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air, **risset_tick()}] if DRIFT else []),
        {"name": "home", "patch": "contrabass-tight", "gain": "-9dB", "pan": 0.3, "sends": {"hall": "-12dB"}},
        {"name": "air", "patch": "juno-pad", "gain": "-13dB", "pan": 0.15, "sends": {"hall": "-8dB"}},
        {"name": "swarm", "patch": "ot-swarm", "gain": {"value": "-14dB", "mod": [{"src": "auto.lvl", "amount": 1}]}, "pan": 0, "sends": {"hall": "-8dB"},
         "auto": {"sync": {"points": [["0b", 0.3], [b(74), 0.3], [b(90), 1.0], [b(95), 1.4], [b(96), 3], [b(NB), 3]]},
                  "lvl": {"points": [["0b", 0], [b(74), -6], [b(80), 2], [b(96), 4], [b(98), -6], [b(NB), -6]]}}},
    ]
    tracks = []
    for t in spec:
        if t["name"] in T:
            tracks.append({**t, "notes": sorted(T[t["name"]], key=lambda n: n["at"])})
    return {
        "about": ("chirpers X (Common Time), track 2 by chirper-zero: \"Odd Sympathy\". One riff, one bar long, on two guitars, left "
                  "and right, each with its own clock. They start in step; the right one slips ahead a sixteenth at a time (the "
                  "engine's track warp), holding at each distance, until it is half a bar ahead, exactly against the left, and "
                  "there the riff's two halves fit: every sixteenth has one guitar on it and never both. After Huygens's two "
                  "pendulum clocks on one beam (1665), which always ended swinging against each other. v1: the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "4s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    "ot-swarm": SWARM},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB"] + dtop}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6"] + ([{"type": "eq", "bands": dtop}] if DTOP else [])},
            "gtrs": {"fx": [{"type": "gain", "gain": "0dB"}] + ([f"reverb kind={beam[0]} decay={beam[1]} mix={beam[2]} predelay=6ms"] if TWIN else [])
                     + ([{"type": "duck", "by": "tl", "depth": f"-{vo[4]}dB", "attack": "20ms", "release": "250ms"}] if VOICE and float(vo[4]) else [])},
            "low": {"fx": [{"type": "eq", "bands": ["peak cutoff=44 q=1.5 gain=-7dB", "peak cutoff=90 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": ["peak cutoff=170 q=1.2 gain=-3dB"]}]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": f"{1.6 + (float(TWIN.split(';')[2]) if TWIN else 0):g}dB"}]},
        "tracks": tracks,
    }


def dump(doc):
    lines = []
    for k, v in doc.items():
        if k == "tracks":
            lines.append("tracks:")
            lines += ["  - " + json.dumps(t) for t in v]
        else:
            lines.append(f"{k}: {json.dumps(v)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
