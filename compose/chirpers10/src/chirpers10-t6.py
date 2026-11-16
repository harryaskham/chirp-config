#!/usr/bin/env python3
"""chirpers X (Common Time), track 6 by chirper-zero: CARRYING CAPACITY.

Harry, 16 Nov about 12:33: "make it unique". Three words, so what unique means here is mine to say and his to overrule.

THE IDEA. The other five songs are built from cycles I chose: wheels, clocks, bell rows, sums, stairs. This one has
no riff I wrote. It has ONE RULE and ONE DIAL. The rule is the oldest model of a population: next year's count is
this year's count, times how fast it breeds (the dial, r), times the room that is left:

        x  <-  r * x * (1 - x)

Every half bar the rule is applied once, and the number it gives (between 0 and 1) IS the half bar: how many of its
six places the band strikes, where the accent falls, and how high the accent is (see `cell`). Low numbers are a
single low note or nothing at all; high numbers are a full roll with a stab at the top of the neck.

THE FORM IS THE DIAL, and nothing else. Turned up slowly the rule does what it always does:
  - under 3 it settles: one half bar, the same for ever (a plain shuffle);
  - at 3 it splits: two half bars that alternate; then four; then eight (the riff doubles its own length);
  - past 3.57 it never repeats: the riff is through-composed by the rule, and still plainly the same riff;
  - inside that there are WINDOWS where it locks again, on cycles nobody asked for: five half bars, then three.
    Five and three against a bar of two: the record's odd meters, but here the rule finds them by itself;
  - at 4 it fills the whole range: screams, then nothing at all for a bar or more (a number near 1 is always
    followed by a number near 0, and near 0 the climb back is slow), then the climb. The band does not play in
    those holes; the machine's long 808 boom falls through them;
  - then the dial comes down through four, two, one, to 1, where the population dies out a note at a time.
It is ONE orbit from the first bar to the last: x is never reset, only the dial moves. This is the record's subject
taken sideways once more: long cycles over a steady pulse that line up, except that here nobody set the lengths.

UNLIKE THE OTHER FIVE (chirp-eco measured what they share): they are in straight sixteenths at 100 to 126; this is
in triplets (twelve-eight written as four-four) at 138. They sit on F and C; this is on E, in the eight-note
half-whole scale. They have one kit and a stick; this has a DRUM MACHINE (the engine's `machine` voices, new on this
record). And the tune over the top is not written into the song at all: the track `lead` carries no notes, only the
rule (`gen: logistic`, the engine's own, new on this record), with the dial's settings; the engine works the orbit
out again by itself and the generator checks that the two agree.

v1 is the skeleton: the whole dial, played bare.
"""
import json
import os

OUT = os.environ.get("C10T6_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t6.yaml"))
BPM = 138
E1 = 28
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ------------------------------------------------------------------------------------------------- the rule
OCT = [0, 1, 3, 4, 6, 7, 9, 10]          # the half-whole scale: sixteen rungs to two octaves
PRI = [0, 3, 2, 5, 1, 4]                 # the order a half bar's six places fill: the two beats, their pick-ups, the rest


def rung(x):
    return min(15, int(16 * x))


def cell(x):
    """x (0..1) -> (the places struck, which of them is the accent, the accent's rung). floor(7x) places are
    struck, in PRI order; the accent is chosen by how far x is through its seventh; its rung is floor(16x)."""
    k = min(6, int(7 * x))
    f = 7 * x - int(7 * x) if x < 6 / 7 else (x - 6 / 7) * 7
    slots = sorted(PRI[:k])
    return slots, (int(f * k) if k else -1), rung(x)


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def lock(x, lo, hi, period, n):
    """The dial setting in a window lo..hi from which the orbit, arriving at x, locks soonest onto its cycle of
    `period` (and whose cycle stays clear of the rule's edges, so that no rounding decides a note)."""
    best = None
    for i in range(201):
        r = lo + (hi - lo) * i / 200
        y, ys = x, []
        for _ in range(120):
            y = r * y * (1 - y)
            ys.append(y)
        t = next((j for j in range(n) if all(abs(ys[j + m] - ys[j + m + period]) < 2e-4 for m in range(period))), None)
        if t is None:
            continue
        clear = min(min(abs(v * q - round(v * q)) / q for q in (7, 16)) for v in ys[t:t + period])
        if clear > 0.001 and (best is None or (t, -clear) < (best[0], -best[2])):
            best = (t, r, clear)
    assert best, (lo, hi)
    return best[1]


# v3: THE BAND TELLS YOU WHERE THE RULE IS (whole-song round). Through v2 the riff changed under a band that did
# not: from 0:41 to 2:24 the finished file sat within 0.6 dB, four guitars and the same hat whether the rule was
# repeating or not, and the run down at the end changed the dial every four bars, before the rule had settled
# (its stretch "four" never once played its four half bars through). Three things, one idea:
#   - THE WALL AND THE OPEN HAT ARE FOR NEWS. Where the rule repeats, the band is two guitars and a closed hat:
#     a riff you know, played tight. Where it does not repeat (1:10, 1:44, the top, and the half bars in which
#     it is still finding a cycle), the second pair of guitars is in and the hat is open on every beat. So the
#     song steps where the rule changes state: up at 1:10, down at 1:27 (the lock on five is the leanest thing
#     in the middle of the song), up at 1:44, down at 2:01 and then built back a layer at a time (v2's layers:
#     the second pair of guitars now ARRIVES with the harmony the third time round), up at 2:24.
#   - THE TOP IS THE TOP: at the top of the dial every scream has the cymbal on it, ringing into the hole.
#   - THE DIAL COMES DOWN SLOWLY ENOUGH TO HEAR. Each setting on the way down now lasts until the rule has
#     settled and said its cycle: four (seven half bars of finding it, then the two-bar riff twice), two, and
#     then one: the shuffle of 0:14 comes home for six bars before the song dies out.
# the run down's half bars at four ; at two ; at one ; the velocity of the cymbal on a scream at the top. "" = v2.
TELL = os.environ.get("C10T6_TELL", "16;12;12;0.9")
DOWN = [int(v) for v in TELL.split(";")[:3]] if TELL else [8, 8, 8]

# name, half bars, the dial. A list is one setting for each half bar; a tuple (lo, hi, period) is a window.
DIAL = [
    ("growth", 16, lin(1.5, 2.8, 16)),
    ("one", 16, lin(2.8, 2.98, 16)),
    ("two", 16, [3.2] * 8 + [3.4] * 8),
    ("four", 16, [3.5] * 16),
    ("eight", 16, [3.555] * 16),
    ("chaos", 20, lin(3.6, 3.7, 20)),
    ("five", 20, (3.7383, 3.7410, 5)),
    ("chaos2", 16, [3.8] * 16),
    ("three", 18, (3.8290, 3.8405, 3)),
    ("six", 12, [3.845] * 12),
    ("full", 32, [3.995] * 32),
    ("down-four", DOWN[0], [3.5] * DOWN[0]),
    ("down-two", DOWN[1], [3.2] * DOWN[1]),
    ("down-one", DOWN[2], [2.8] * DOWN[2]),
    ("out", 4, [1.0] * 4),
]
X0 = 0.02


def orbit():
    """-> [(section, r, x before, x)] for every half bar, and each section's first half bar."""
    x, cells, starts = X0, [], {}
    for name, n, dial in DIAL:
        starts[name] = len(cells)
        rs = [lock(x, dial[0], dial[1], dial[2], n)] * n if isinstance(dial, tuple) else dial
        assert len(rs) == n, name
        for r in rs:
            x0, x = x, r * x * (1 - x)
            cells.append((name, r, x0, x))
    starts["end"] = len(cells)
    return cells, starts


CELLS, AT = orbit()
NC = len(CELLS)
NB = NC // 2 + 1


# ------------------------------------------------------------------------------------------------- the band
def add(tr, c, slot, len_slots, pitch, vel, **expr):
    """Half bar c, place `slot` (thirds of a beat), `len_slots` long."""
    n = {"at": round(c * 2 + slot / 3, 5), "len": round(len_slots / 3 * 0.96, 5), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, c, slot, vel, tr=None):
    tr = tr or {"k": "kick", "s": "snare", "p": "snare", "h": "hat", "o": "hat", "c": "cym", "b": "boom"}[piece]
    T.setdefault(tr, []).append({"at": round(c * 2 + slot / 3, 5), "len": 0.25, "pitch": piece, "vel": round(vel, 3)})


def note(r):
    return E1 + 12 * (r // 8) + OCT[r % 8]


def play(c, x, gtrs, bass=True, kick=True, harm=()):
    """`harm`: the guitars that take an accent from the octave up two rungs higher."""
    slots, ai, r = cell(x)
    for i, s in enumerate(slots):
        nxt = slots[i + 1] if i + 1 < len(slots) else 6
        if i == ai:                           # the accent: a fretted note; from the octave up, a fifth on it
            p = note(r)
            for tr in gtrs:
                q = note(r + 2) if tr in harm and r >= 8 else p
                add(tr, c, s, nxt - s, nm(q) if r < 8 else f"{nm(q)},{nm(q + 7)}", 1.0)
            if bass:
                add("bass", c, s, nxt - s, note(r % 8), 0.95)
            if kick:
                drum("k", c, s, 1.0)
        else:                                 # a muted chug on the open low string
            for tr in gtrs:
                add(tr, c, s, 1, E1, 0.88, pm=1)
            if bass:
                add("bass", c, s, 1, E1, 0.85)
            if kick:
                drum("k", c, s, 0.86)


# v2: WHAT A BAND CAN DO ONCE THE RIFF REPEATS (section round, 1:51-2:19: the window of three, which the map called
# static). While the rule never repeats, nobody can arrange it: every half bar is news, so the band plays it in
# unison. In a window the same three half bars come round again and again, and a band that has heard a riff twice
# starts to arrange it. So the window is now told that way, a layer for each time round:
#   - it FINDS the cycle: the dial moves at 1:58 and for three half bars the rule is still settling; the snare keeps
#     the back beat of the stretch before. On the first scream of the cycle proper (2:01) the cymbal and the clap
#     mark it and the snare drops to half time: the groove changes when the rule locks, not when the dial moves;
#   - the second time round, a second chip answers in the hole (the cycle has one: a single low note, then nothing
#     for most of a half bar): it plays the cycle's own three notes as one triplet, the cycle inside itself, and
#     its last note is the note the band plays next;
#   - the third time round, the second pair of guitars takes the scream two rungs higher (a third), so the scream
#     is a four-note chord and no longer a fifth;
#   - both go on through the six (2:14).
# the time round at which the answer starts ; at which the harmony starts ; the answer's gain ; its register
# (semitones over the riff's) ; its pan. "" = v1.
LOCK = os.environ.get("C10T6_LOCK", "2;3;-14dB;24;0.4")


def lock_head(sec, period, rhythm=False):
    """The first half bar of `sec` that begins the cycle proper: its highest number, once the cycle repeats
    (`rhythm`: once the places struck repeat, whatever the accent does)."""
    a, b = AT[sec], AT[sec] + dict((n, k) for n, k, _ in DIAL)[sec]
    same = (lambda i, j: cell(CELLS[i][3])[0] == cell(CELLS[j][3])[0]) if rhythm else (lambda i, j: cell(CELLS[i][3]) == cell(CELLS[j][3]))
    t = next(j for j in range(a, b - period) if all(same(i, i + period) for i in range(j, b - period)))
    return next(j for j in range(t, t + period) if CELLS[j][3] == max(CELLS[i][3] for i in range(t, t + period)))


# v4: THE WAY UP HAS EVENTS, AND THE TOP IS THE SUM (whole-song round; both were costs of v3, said in its note).
# v3 saved the second pair of guitars for the stretches that do not repeat, which left the first minute on two
# guitars with nothing happening at 0:42 and 0:56 but the riff doubling its length; and at the top (2:24) the band
# DROPPED what it had just learned in the window of three (the chord on the scream, the chip's answer).
#   - THE HAT COUNTS FINER AS THE RIFF GETS LONGER. One and two: the machine's hat on the beat (two to a half
#     bar). Four (0:42): the shuffle's four places. Eight (0:56): all six, running. Then at 1:10 it opens, on the
#     beat, with the wall. The first minute builds on the machine alone.
#   - EIGHT IS A RIFF SAID TWICE, AND A BAND ARRANGES A REPEAT (v2's rule): the second time (1:03) the tune has a
#     second voice, a third above it. Like the tune it has no notes in the song: it is the engine's logistic
#     generator again, the same orbit read off a ladder two rungs higher (in this scale two rungs are always a
#     minor third).
#   - THE TOP KEEPS WHAT THE SONG HAS LEARNED: the screams stay chords (the second pair two rungs up, as from
#     2:06), and wherever the three's shape turns up again inside the chaos (a scream, then one low note: it
#     does, twice, because the top of the dial is next door to that window) the chip answers as it did there.
# hats to a half bar at four ; at eight ; the velocity of the two pick-up places ; of the other two ; the second
# voice's gain ; its pan ; 1 = the top keeps the chord and the answer. "" = v3.
UP = os.environ.get("C10T6_UP", "4;6;0.45;0.38;-20dB;-0.4;1")
HATS = {"four": int(UP.split(";")[0]), "eight": int(UP.split(";")[1])} if UP else {}
HEAD3 = lock_head("three", 3) if LOCK else None
HEAD4D = lock_head("down-four", 4, rhythm=True) if TELL else None
# v5: THE FIRST LOCK GOES WITH THE CYCLE (section round, 1:23-1:51: the window of five). There are two things a
# band can do with a cycle that does not fit the bar. It can hold the bar and let the cycle turn against it: that
# is the window of three (2:01), where the snare stays on the bar's third beat and the riff comes round under it,
# three against two. Or it can drop the bar and go with the cycle. Through v4 both windows did the first. Now the
# window of five does the second: for its seventeen seconds the song is IN five. The cycle is ten beats long, and
# the machine plays it as a drummer counts ten: four, four and two. The snare is on the third beat of each four
# (the first of them lands on the cycle's one lonely low note), and both beats of the two are snare, a push into
# the cycle's head, where the cymbal is. Nothing in that stretch marks the song's own bar but the hat, which never
# stops keeping the beat; after four times round, ten bars have gone by and the two meet again.
# the snare's beats in the ten-beat cycle ; those of them with the clap ; the cymbal's velocity on each head. "" = v4.
FIVE = os.environ.get("C10T6_FIVE", "3,7,9,10;3,7;0.85")
HEAD5 = lock_head("five", 5) if FIVE else None
assert not FIVE or HEAD5 == AT["five"], "the window of five is written for a cycle that locks at once"
assert LOCK or not TELL, "C10T6_TELL builds on C10T6_LOCK"

G = ("gl", "gr")
G2 = ("gl2", "gr2")
BACK = {"one", "two", "four", "eight", "chaos", "chaos2", "full", "down-four", "down-two", "down-one"}   # the snare on two and four
HALF = {"five", "three", "six"}                                                                          # the snare on three only
WIDE = {"chaos", "chaos2", "three", "full"} if TELL else {"four", "eight", "chaos", "five", "chaos2", "three", "six", "full"}   # four guitars
LEAD = {"two", "four", "eight", "chaos", "five", "chaos2", "three", "six", "full", "down-four", "down-two"}


def compose():
    for c, (sec, r, x0, x) in enumerate(CELLS):
        first = c == AT[sec]
        if sec == "growth":
            gtrs = () if c < 8 else ("gl",)
            play(c, x, gtrs, bass=c >= 4)
        elif sec == "out":
            play(c, x, G)
        elif LOCK and (sec == "six" or (sec == "three" and c >= HEAD3)):
            turn = (c - HEAD3) // 3 + 1                       # which time round the cycle this is
            layered = turn >= int(LOCK.split(";")[1])
            play(c, x, G + (G2 if layered or not TELL else ()), harm=G2 if layered else ())
            if len(cell(x)[0]) == 1 and turn >= int(LOCK.split(";")[0]):     # the hole: the cycle's three notes, as a triplet
                for i, (cc, v) in enumerate(((c - 1, 0.8), (c, 0.7), (c + 1, 0.9))):
                    add("echo", c, 3 + i, 1, note(rung(CELLS[cc][3])) + int(LOCK.split(";")[3]), v)
        elif UP and UP.split(";")[6] == "1" and sec == "full":
            play(c, x, G + G2, harm=G2)
            if len(cell(x)[0]) == 1 and len(cell(CELLS[c - 1][3])[0]) == 6:      # the three's shape again: the chip answers
                for i, (cc, v) in enumerate(((c - 1, 0.8), (c, 0.7), (c + 1, 0.9))):
                    add("echo", c, 3 + i, 1, note(rung(CELLS[cc][3])) + int(LOCK.split(";")[3]), v)
        else:
            play(c, x, G + (G2 if sec in WIDE else ()))
        # the steady pulse: the machine's hat on every beat, opened on the last beat before a new setting
        finding = LOCK and sec == "three" and c < HEAD3       # the dial has moved and the rule has not settled yet
        news = TELL and cell(x)[0] and (sec in ("chaos", "chaos2", "full") or finding or (sec == "down-four" and c < HEAD4D))
        if sec != "out":
            for s in (0, 3):
                last = c + 1 < NC and CELLS[c + 1][0] != sec and s == 3
                drum("o" if last or news else "h", c, s, 0.75 if (s == 0 and c % 2 == 0) else 0.55)
            for s in {2: (), 4: (2, 5), 6: (1, 2, 4, 5)}[HATS.get(sec, 2)]:      # v4: the hat counts finer as the riff gets longer
                drum("h", c, s, float(UP.split(";")[2 if s in (2, 5) else 3]))
        if TELL and sec == "full" and len(cell(x)[0]) == 6:   # the top: the cymbal on every scream
            drum("c", c, cell(x)[0][cell(x)[1]], float(TELL.split(";")[3]))
        if FIVE and sec == "five":                            # v5: the machine counts the cycle, not the bar
            k = (c - HEAD5) % 5
            for b in (int(v) for v in FIVE.split(";")[0].split(",")):
                if (b - 1) // 2 == k:
                    drum("s", c, 0 if b % 2 else 3, 1.0 if b % 2 else 0.9)
                    if str(b) in FIVE.split(";")[1].split(","):
                        drum("p", c, 0 if b % 2 else 3, 0.8)
            if k == 0 and not first:
                drum("c", c, 0, float(FIVE.split(";")[2]))
        elif sec in BACK or finding:
            drum("s", c, 3, 0.95)
        elif sec in HALF and c % 2 == 1:
            drum("s", c, 0, 1.0)
            drum("p", c, 0, 0.8)
        if LOCK and sec == "three":
            if c == HEAD3:                                    # it locks: the cymbal and the clap on the cycle's first scream
                drum("c", c, 0, 0.95)
                if c % 2 == 0:                                # (on a bar's third beat the half-time snare brings its own clap)
                    drum("p", c, 0, 0.9)
        elif first and sec not in ("growth", "out") and not (TELL and sec == "down-four"):   # (the last scream's cymbal is still ringing there)
            drum("c", c, 0, 0.9)
        # a hole (a half bar with nothing in it) after sound: the boom falls through it
        if sec not in ("growth", "out") and not cell(x)[0] and c and cell(CELLS[c - 1][3])[0]:
            drum("b", c, 0, 0.95)


def lead_gens():
    """The lead's part is the rule itself: one `logistic` system for each run of half bars on one dial setting,
    started from the orbit's own number there, so the engine walks the same orbit the band is playing."""
    pool = " ".join(nm(note(r) + 36) for r in range(16))
    gens, c = [], 0
    while c < NC:
        sec, r, x0, _ = CELLS[c]
        n = 1
        while c + n < NC and CELLS[c + n][0] == sec and CELLS[c + n][1] == r:
            n += 1
        gens.append((c, n, sec, {"type": "logistic", "r": r, "x0": x0, "n": n, "len": "/2", "notes": pool, "rest": round(1 / 7, 6)}))
        c += n
    return gens


def second_voice():
    """Eight's second statement: the same orbit, read off the lead's ladder two rungs higher (a minor third)."""
    c = AT["eight"] + 8
    pool = " ".join(nm(note(r + 2) + 36) for r in range(16))
    return c, {"type": "logistic", "r": CELLS[c][1], "x0": CELLS[c][2], "n": 8, "len": "/2", "notes": pool, "rest": round(1 / 7, 6)}


def song():
    compose()
    kit = "cc-machine"
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    gens = [g for g in lead_gens() if g[2] in LEAD]
    lead_at = gens[0][0]
    assert all(a[0] + a[1] == b[0] for a, b in zip(gens, gens[1:])), "the lead's runs must follow one another"
    tracks = [
        {"name": "gl", "patch": main.format(30), "gain": "0.8dB", "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(31), "gain": "0.8dB", "pan": 1, "out": "gtrs", **mids},
        {"name": "gl2", "patch": dbl.format(32), "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **mids},
        {"name": "gr2", "patch": dbl.format(33), "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **mids},
        {"name": "lead", "patch": "nes-pulse-lead", "gain": os.environ.get("C10T6_LEAD", "-18dB"), "pan": 0, "at": f"{lead_at * 2}b",
         "sends": {"hall": "-12dB"}, "gen": [g[3] for g in gens]},
        *([{"name": "echo", "patch": "nes-pulse-lead layers.0.chip.duty=0.125", "gain": LOCK.split(";")[2], "pan": float(LOCK.split(";")[4]),
            "sends": {"hall": "-12dB"}}] if LOCK else []),
        *([{"name": "lead2", "patch": "nes-pulse-lead", "gain": UP.split(";")[4], "pan": float(UP.split(";")[5]), "at": f"{second_voice()[0] * 2}b",
            "sends": {"hall": "-12dB"}, "gen": [second_voice()[1]]}] if UP else []),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "boom", "patch": kit, "gain": os.environ.get("C10T6_BOOM", "0dB"), "out": "drums"},
        {"name": "kick", "patch": kit, "gain": os.environ.get("C10T6_KICK", "0dB"), "out": "drums"},
        {"name": "snare", "patch": kit, "gain": os.environ.get("C10T6_SNARE", "0dB"), "out": "drums", "sends": {"hall": "-18dB"},
         "fx": [{"type": "eq", "bands": ["peak cutoff=350 q=1 gain=-5dB"]}]},      # its second oscillator sits in the guitars' low mids
        {"name": "cym", "patch": kit, "gain": os.environ.get("C10T6_CYM", "0dB"), "out": "drums"},
        {"name": "hat", "patch": kit, "gain": os.environ.get("C10T6_HAT", "0dB"), "out": "drums"},
    ]
    for t in tracks:
        if "gen" not in t:
            t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])
    long_amp = {"a": "0.1ms", "d": "6s", "s": 1, "r": "2.5s"}

    def piece(part, pitch, gain, pan=0.0, choke=None, **m):
        p = {"pitch": pitch, "gain": gain, "pan": pan, "patch": {"synth": {"amp": long_amp, "layers": [{"type": "machine", "machine": {"part": part, **m}}]}}}
        if choke:
            p["choke"] = choke
        return p

    machine = {
        "about": ("Carrying Capacity's drum machine (chirper-zero, 16 Nov): the engine's `machine` voices, the first on this record. "
                  "k a 909-style kick resting on the song's E with its click up; s the two-oscillator snare; p the clap; "
                  "b the 808's long boom on E; "
                  "h and o the six-square hat, closed and open (they choke each other); c the cymbal."),
        "play": {"len": "/16", "vel_sens": 0.5},
        "kit": {
            "k": piece("kick", "E1", os.environ.get("C10T6_K", "-14dB"), click=0.8, drive=0.35, decay="180ms"),
            "s": piece("snare", "G3", os.environ.get("C10T6_S", "-5.5dB"), snappy=0.5, drive=0.2),
            "p": piece("clap", "C4", os.environ.get("C10T6_P", "0dB")),
            "b": piece("boom", "E1", os.environ.get("C10T6_B", "-5dB"), decay="5s", drive=0.5),
            "h": piece("hat", "C6", os.environ.get("C10T6_H", "0dB"), pan=-0.3, choke="hat"),
            "o": piece("hat", "C6", os.environ.get("C10T6_O", "-3dB" if TELL else "0dB"), pan=-0.3, choke="hat", decay="380ms"),   # v3: open on every beat of the news: 3 dB down
            "c": piece("cymbal", "C6", os.environ.get("C10T6_C", "-6dB"), pan=0.3),
        },
    }
    return {
        "about": ("chirpers X (Common Time), track 6 by chirper-zero: Carrying Capacity. No riff was written. There is one rule, "
                  "x <- r x (1 - x), applied once every half bar, and the number it gives is the half bar: how many of its six "
                  "places the band strikes, where the accent falls and how high. The form is the dial r turned up from 1.5 to 4 "
                  "and back down: the riff settles, splits in two, four, eight, stops repeating, locks by itself on five half "
                  "bars and then on three, fills the whole range, and dies out. Triplets at 138, on E, with a drum machine; "
                  "the lead has no notes, only the rule (the engine's own logistic generator). v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{NB * 4}b", "event_stable": True,
        "patches": {"cc-machine": machine},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4.5s mix=1 predelay=30ms low_cut=150"]},
            "drums": {"fx": [{"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            # ct-bass's bus, as on the other songs, with its bands moved down a semitone to E
            "low": {"fx": [{"type": "eq", "bands": ["peak cutoff=41.5 q=1.5 gain=-7dB", "peak cutoff=85 q=1 gain=7.5dB", "peak cutoff=350 q=1 gain=-8dB", "peak cutoff=1500 q=1 gain=4dB"]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": ["peak cutoff=160 q=1.2 gain=-3dB"]}]},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T6_MASTER", "2.7dB")}]},
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


def show(x):
    slots, ai, r = cell(x)
    s = ["."] * 6
    for i, sl in enumerate(slots):
        s[sl] = "%X" % r if i == ai else "0"
    return "".join(s)


if __name__ == "__main__":
    if os.environ.get("C10T6_SHOW"):
        for name, n, _ in DIAL:
            a = AT[name]
            print(f"{name:10s} bar {a // 2:3d} r {CELLS[a][1]:.4f}..{CELLS[a + n - 1][1]:.4f}  " + " ".join(show(c[3]) for c in CELLS[a:a + n]))
    else:
        open(OUT, "w").write(dump(song()))
