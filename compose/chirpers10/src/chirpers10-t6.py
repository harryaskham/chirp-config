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
    ("down-four", 8, [3.5] * 8),
    ("down-two", 8, [3.2] * 8),
    ("down-one", 8, [2.8] * 8),
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


def play(c, x, gtrs, bass=True, kick=True):
    slots, ai, r = cell(x)
    for i, s in enumerate(slots):
        nxt = slots[i + 1] if i + 1 < len(slots) else 6
        if i == ai:                           # the accent: a fretted note; from the octave up, a fifth on it
            p = note(r)
            for tr in gtrs:
                add(tr, c, s, nxt - s, nm(p) if r < 8 else f"{nm(p)},{nm(p + 7)}", 1.0)
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


G = ("gl", "gr")
G2 = ("gl2", "gr2")
BACK = {"one", "two", "four", "eight", "chaos", "chaos2", "full", "down-four", "down-two", "down-one"}   # the snare on two and four
HALF = {"five", "three", "six"}                                                                          # the snare on three only
WIDE = {"four", "eight", "chaos", "five", "chaos2", "three", "six", "full"}                              # four guitars
LEAD = {"two", "four", "eight", "chaos", "five", "chaos2", "three", "six", "full", "down-four", "down-two"}


def compose():
    for c, (sec, r, x0, x) in enumerate(CELLS):
        first = c == AT[sec]
        if sec == "growth":
            gtrs = () if c < 8 else ("gl",)
            play(c, x, gtrs, bass=c >= 4)
        elif sec == "out":
            play(c, x, G)
        else:
            play(c, x, G + (G2 if sec in WIDE else ()))
        # the steady pulse: the machine's hat on every beat, opened on the last beat before a new setting
        if sec != "out":
            for s in (0, 3):
                last = c + 1 < NC and CELLS[c + 1][0] != sec and s == 3
                drum("o" if last else "h", c, s, 0.75 if (s == 0 and c % 2 == 0) else 0.55)
        if sec in BACK:
            drum("s", c, 3, 0.95)
        elif sec in HALF and c % 2 == 1:
            drum("s", c, 0, 1.0)
            drum("p", c, 0, 0.8)
        if first and sec not in ("growth", "out"):
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
            "o": piece("hat", "C6", os.environ.get("C10T6_O", "0dB"), pan=-0.3, choke="hat", decay="380ms"),
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
