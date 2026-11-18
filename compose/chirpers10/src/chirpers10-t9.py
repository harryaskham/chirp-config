#!/usr/bin/env python3
"""chirpers10-t9 "In the Time Of" (chirper-zero): one riff of seven notes, and one beat that never changes.

"Five in the time of four" is how a musician says a quintuplet. This piece is that phrase taken as a form. The beat
is common time at 84 from the first bar to the last, and the kit keeps it plainly. The riff is seven notes long (a
low open note, two muted strokes, a hook note, a stroke, a hook note, a stroke), and the band deals it out at a
different number of notes to the beat in each section:

  one to the beat      bars 0-7     the riff is a slow tune, seven beats long: two guitars and a hat
  two                  bars 7-14    the bass and the kick come in
  three                bars 14-21   triplets: the snare, the china, each guitar doubled
  four                 bars 21-28   sixteenths; v2: the two hook notes pass between baritone and clavinet
  five                 bars 28-35   quintuplets: two guitars again; the bass holds through their muted strokes
  six                  bars 35-42   sextuplets: one beat of the kit alone before the lock
  seven                bars 42-56   septuplets: THE SEVEN STROKES ARE NOW EXACTLY ONE BEAT LONG. It locks:
                                    every beat begins with its open note. Six guitars; then a minor third up
  one again            bars 56-63   the riff at one to the beat once more, every note a chord
  one chord            bars 63-65

Before seven, a cell START and a quarter note coincide once every seven beats: beats one, four, three, two in
successive bars of their meeting. A seven-bar rung fits both the cell and the four-beat bar. The shape repeats
every seven strokes; the two answers (A flat/B and G flat/C in F) alternate, so the pitch phrase is twice as long.
The hat or china stays on the quarter. At seven, the kick and bass land on the head of every cell instead of
following all its strokes. What was a slow tune should now be a fast figure over a very plain walk.

v1 is the SKELETON (Harry, 18 Nov about 03:18: "for now youll build ahead ina enew song"): the whole shape standing,
bare.
"""
import json
import os

OUT = os.environ.get("C10T9_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t9.yaml"))
BPM = 84
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
# o an open low root, c a muted stroke, a number a hook note (semitones over the root). Two forms, taken in turn
CELLS = ["o c c 3 c 6 c".split(), "o c c 1 c 7 c".split()]
N = len(CELLS[0])
RUNG = 4 * N                              # beats: seven bars, four times round
PAWL = os.environ.get("C10T9_PAWL", "-9dB")  # off = the same skeleton without the cell marker
# v2 palette: a picked string and a keyed string take the two answers out of the
# four unison guitars for one rung. Gains in that order. Empty restores v1.
HANDS = os.environ.get("C10T9_HANDS", "-11.5dB;-4.5dB")
ALL = ("gl", "gr", "dl", "dr", "wl", "wr")
MARKS = []
ROOTS = [(0, 0)]


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


def add(tr, beat, length, pitch, vel, **expr):
    n = {"at": round(beat, 5), "len": round(length * 0.98, 5), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, beat, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(beat, 5), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


def deal(b0, beats, k, gtrs, low=True, root=0, chords=""):
    """Deal the cell. Chord letters: o = cell head, h = hook, c = clipped pedal fifth on a mute."""
    for i in range(beats * k):
        kind = CELLS[(i // N) % len(CELLS)][i % N]
        at = b0 + i / k
        midi = F1 + root + (0 if kind in ("o", "c") else int(kind))
        part = kind if kind in ("o", "c") else "h"
        pitch = midi
        if part in chords:
            intervals = (0, 7) if part == "c" else (0, 7, 12)
            pitch = ",".join(nm(midi + j) for j in intervals)
        mute = part == "c"
        vel = 0.82 if mute else 1.0 if part == "o" else 0.95
        if HANDS and k == 4 and part == "h":
            # Sixteen cells in this rung. Exchange jobs after eight, not at a
            # bar line: the reversal follows the riff, halfway through bar four.
            first_answer = i % N == 3
            picked = first_answer != (i >= beats * k // 2)
            if picked:
                add("picked", at, 1.55 / k, midi + 12, 0.94)
            else:
                add("keyed", at, 0.85 / k, midi + 24, 0.96)
        else:
            for tr in gtrs:
                add(tr, at, (0.65 if mute else 1) / k, pitch, vel, **({"pm": 1} if mute else {}))
        if not low:
            continue
        if k == N:                              # the beat and cell are now one: a footfall, not a kick roll
            if part == "o":
                add("bass", at, 1, midi, 0.96)
                drum("k", at, 1)
        elif k >= 3:
            if not mute:                        # three accents held through the guitar ticks: 3 + 2 + 2
                add("bass", at, min((3 if part == "o" else 2) / k, b0 + beats - at), midi, 0.93)
                drum("k", at, 0.97 if part == "o" else 0.86)
        else:
            add("bass", at, (0.68 if mute else 1) / k, midi, vel)
            drum("k", at, vel)


def beat(b0, b1, cym="x", vel=0.5, snare=(1, 3)):
    for b in range(b0, b1):
        drum(cym, b, vel + (0.05 if (b - b0) % 4 == 0 else 0))
        if (b - b0) % 4 in snare:
            drum("s", b, 0.95)


def fill(b):
    """The last two beats before beat b."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, b - 2 + i / 4, 0.6 + 0.045 * i)


def compose():
    T.clear()
    MARKS.clear()
    ROOTS[:] = [(0, 0)]
    names = ["one to the beat", "two", "three", "four", "five", "six"]
    b = 0
    for k in range(1, 7):
        MARKS.append((names[k - 1], b))
        gtrs = ("gl", "gr", "dl", "dr") if k in (3, 4) else ("gl", "gr")
        deal(b, RUNG - int(k == N - 1), k, gtrs, low=k >= 2)
        if k < 3:
            beat(b, b + RUNG, cym="h", vel=0.45, snare=())
        else:
            beat(b, b + RUNG)
        if PAWL and k in (5, 6):
            # Tap each cell head, NOT each beat. Its 7 partials come from the cell itself. The tone crosses
            # from the three open strokes to the four muted ones; the kick takes its job when the cell locks.
            for i in range(0, (RUNG - int(k == N - 1)) * k, N):
                phase = (b + i / k - 4 * RUNG) / (2 * RUNG)
                add("pawl", b + i / k, 0.23, F1 + 36, 0.91, turn=round(0.12 + 0.70 * phase, 4))
        for j in range(0, RUNG, N):                      # where the riff comes round to the beat again
            if k >= 2:
                drum("c", b + j, 0.9 if j == 0 else 0.7)
        b += RUNG
    # seven to the beat: the riff is one beat long
    MARKS.append(("seven: it locks", b))
    fill(b)
    drum("c", b, 0.95)
    deal(b, 32, 7, ALL, chords="o")
    ROOTS.append((b + 32, 3))
    deal(b + 32, 24, 7, ALL, root=3, chords="o")
    drum("c", b + 32, 0.9)
    for j in range(4, 56, 4):
        if j != 32:
            drum("c", b + j, 0.65)
    beat(b, b + 56)
    b += 56
    # one to the beat again, every note a chord
    MARKS.append(("one again", b))
    ROOTS.append((b, 0))
    fill(b)
    deal(b, RUNG, 1, ALL, chords="ohc")
    beat(b, b + RUNG, snare=(2,))
    for j in range(0, RUNG, N):
        drum("c", b + j, 0.95 if j == 0 else 0.8)
    b += RUNG
    MARKS.append(("one chord", b))
    for tr in ALL:
        add(tr, b, 8, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", b, 8, F1, 0.95)
    drum("k", b, 0.95)
    drum("c", b, 0.95)
    return b + 8


def song():
    total = compose()
    assert total % 4 == 0 and all(m[1] % 4 == 0 for m in MARKS)
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"            # each side is two takes from three to the beat on
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    tracks = [
        {"name": "gl", "patch": main.format(70), "gain": os.environ.get("C10T9_MAIN", "0.7dB"), "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(71), "gain": os.environ.get("C10T9_MAIN", "0.7dB"), "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(72), "gain": os.environ.get("C10T9_DBL", "-2.5dB"), "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(73), "gain": os.environ.get("C10T9_DBL", "-2.5dB"), "pan": 0.75, "out": "gtrs", **mids},
        {"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        *([{"name": "pawl", "patch": "it-pawl", "gain": PAWL, "pan": -0.15}] if PAWL else []),
        *([{"name": "picked", "patch": "baritone fx.3.mix=0.07 fx.4.mix=0.09",
            "gain": HANDS.split(";")[0], "pan": -0.56},
           {"name": "keyed", "patch": "clav", "gain": HANDS.split(";")[1], "pan": 0.56}] if HANDS else []),
    ]
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", 0]], 0
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p - 0.02:g}b", prev], [f"{p:g}b", r]]
            prev = r
    return {
        "about": ("chirpers X (Common Time), track 9 by chirper-zero: In the Time Of. One riff of seven notes and one beat that never "
                  "changes (84). The band deals the riff out at one note to the beat, then two, three, four, five, six, drifting "
                  "across the beat and coming round to it every seven beats; at seven to the beat the riff is exactly one beat long "
                  "and locks. The bass and kick walk in quarters underneath. Then once more at one to the beat, every stroke a chord. "
                  "v1 is the skeleton.") + (" At four to the beat the two hook notes pass between a baritone guitar and a clavinet; they exchange roles halfway." if HANDS else ""),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{total}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    **({"it-pawl": {"synth": {"layers": [{"type": "wavetable", "frames": [
                        [[j, round(1 / j**0.45, 4)] for j, x in enumerate(CELLS[0], 1) if x != "c"],
                        [[j, round(1 / j**0.45, 4)] for j, x in enumerate(CELLS[0], 1) if x == "c"]],
                        "position": {"value": 0, "mod": [{"src": "expr.turn", "amount": 1}]}}],
                        "amp": {"a": "3ms", "d": "105ms", "s": 0.22, "r": "42ms"}}}} if PAWL else {})},
        "buses": {
            "drums": {"fx": ["reverb kind=room decay=0.7s mix=0.1 predelay=8ms",
                             {"type": "glue", "threshold": "-24dB", "ratio": 2.5, "attack": "20ms", "release": "140ms", "knee": 6.0},
                             "clip drive=0dB ceiling=-13dB",
                             {"type": "eq", "bands": ["peak cutoff=400 q=0.8 gain=-6dB", "peak cutoff=5500 q=0.9 gain=1dB", "highshelf cutoff=9000 gain=-2dB", "lp cutoff=14250 q=0.8"]}]},
            "oh": {"fx": ["reverb kind=room decay=0.7s mix=1 predelay=4ms low_cut=5000 high_cut=12000 spread=0.6", {"type": "eq", "bands": ["lp cutoff=14250 q=0.8"]}]},
            "snr": {"fx": [{"type": "eq", "bands": ["peak cutoff=300 q=0.7 gain=-12dB"]}]},
            "gtrs": {"fx": [{"type": "eq", "bands": ["peak cutoff=330 q=1.2 gain=-2dB"]}, "reverb kind=room decay=0.35s mix=0.06 predelay=6ms"]},
            "low": {"fx": [{"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(44), "q": 1.5, "gain": "-7dB"}, {"kind": "peak", "cutoff": key_f(90), "q": 1.0, "gain": "7.5dB"},
                                                    {"kind": "peak", "cutoff": 350, "q": 1.0, "gain": "-8dB"}, {"kind": "peak", "cutoff": 1500, "q": 1.0, "gain": "4dB"}]},
                           {"type": "compressor", "threshold": "-26dB", "ratio": 8.0, "attack": "12ms", "release": "120ms", "makeup": "2.5dB"},
                           {"type": "eq", "bands": [{"kind": "peak", "cutoff": key_f(170), "q": 1.2, "gain": "-3dB"}]}],
                    "auto": {"key": {"points": pts, "curve": 0}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T9_MASTER", "2.7dB")}]},
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
    if os.environ.get("C10T9_SHOW"):
        end = compose()
        sec = 60 / BPM
        for (name, b0), (_, b1) in zip(MARKS, MARKS[1:] + [("", end)]):
            print(f"{name:16s} bars {b0 // 4 + 1:3d}-{b1 // 4 + 1:3d}  {int(b0 * sec) // 60}:{b0 * sec % 60:04.1f}-{int(b1 * sec) // 60}:{b1 * sec % 60:04.1f}")
    else:
        open(OUT, "w").write(dump(song()))
