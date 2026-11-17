#!/usr/bin/env python3
"""chirpers10-t8 "Common Measure" (chirper-zero): two riffs of different lengths, argued down to what they share.

Euclid finds the greatest common measure of two lengths by taking the less from the greater, again and again: what is
left over is set against the shorter one, and what that leaves against the leftover, until something goes in exactly.
That last length measures both. This piece is the algorithm played by two guitars, and it is the record's fast song
(160 where the other seven run 80 to 138).

The left guitar has a riff of 52 sixteenths (A); the right has one of 32 (B, two bars). Played together they meet
again only after 26 bars. Then, each section, the longer riff is cut down to WHAT WAS LEFT OVER: its own tail.

  the two given     bars 0-8      B alone on the right: the short riff, twice bare and twice with the band
  52 against 32     bars 8-34     A on the left, B on the right: one whole cycle, 26 bars
  20 against 32     bars 34-54    the left keeps only A's last 20 sixteenths (52 - 32): they meet every 10 bars
  20 against 12     bars 54-69    the right keeps only B's last 12 (32 - 20): every 3 bars and three quarters
  8 against 12      bars 69-81    the left keeps its last 8 (20 - 12): every bar and a half
  8 against 4       bars 81-89    the right keeps its last 4 (12 - 8): every half bar. Four goes into eight: it is found
  the measure       bars 89-105   both guitars, and two more, on the four sixteenths both riffs END with: one beat. The
                                  beat is the common measure; the cell climbs the record's hook notes as chords
  measured          bars 105-126  now the two riffs can be said together: all four guitars play A four times, then B
                                  four times, in unison, the kit's four in a bar under them (A is thirteen beats, B eight)
  one chord         bar 126

The bass and the kick go with the SHORTER riff of each pair (the one doing the measuring), so the rhythm section's
cycle shrinks section by section: two bars, a bar and a quarter, three beats, half a bar, a beat. WHAT IS LEFT OVER
IS HEARD ALONE: at the end of each pair the band stops and the longer riff plays its tail by itself (20 sixteenths,
then 12, 8, 4: the breaks shrink too), and that tail is the next section's riff. The kit keeps common time
throughout, its feel changing with each cut, and crashes wherever the two riffs meet, so the crashes come closer and
closer: 39 seconds apart, then 15, 5.6, 2.25, and at last the china on every beat. THE ARGUMENT NARROWS: each riff is
two takes a side until 8 against 12, where it is one; at 8 against 4 the bass and the kick drop out (the kick comes
back half way) and the snare counts every beat, louder and louder; two beats of nothing; then the measure, with every
guitar there is.

Track 7 (Extreme and Mean) is the cut that has no common measure, slow, never looping. This is its pair: the two
lengths here do have one, and the song is the finding of it. 52 and 32 are four times 13 and 8, so the algorithm takes
as long as it can (every quotient is one) and ends on four sixteenths: the beat of common time, where the record began.

v1 is the SKELETON (Harry, 17 Nov about 03:40: "open up 2 new song slots"; track 2's terms: mine, my title, a
skeleton first): the whole shape standing, bare.
"""
import json
import os

OUT = os.environ.get("C10T8_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "songs", "chirpers10-t8.yaml"))
BPM = 160
F1 = 29
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
T = {}
# v2, THE TWO BELLS: each riff has a bell that rings where the riff begins again, the left riff's low and on the left, the
# right riff's a fourth higher and on the right. As the riffs are cut down the bells come faster and closer, and at the
# measure they ring together on every beat. gain, dB ; velocity ; velocity in the measure ; the low bell's dB over the
# high one's (it reads 2.4 dB quieter at the same gain). "" = v1 (no bells).
BELLS = os.environ.get("C10T8_BELLS", "-12;0.9;0.95;1.5")


def nm(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# o an open low root, c a muted stroke, r a rest, - a held place, a number a hook note (semitones over the root)
A = ("10 - - 7 - - 6 - 3 - - 1 - - o - "          # the hook coming down in threes and twos
     "c c r c c r c r o c c r 7 - 6 - "
     "o c c 3 - c o c c 10 - c "                   # (its last 20 begin here)
     "6 - c c o - c c").split()                    # (its last 8)
B = ("o r c c r c c r o r c c r 1 - r "
     "o c c r "
     "3 - - 6 - - 7 - "                            # (its last 12 begin here)
     "o - c c").split()                            # (its last 4: the measure)
assert len(A) == 52 and len(B) == 32 and A[-4:] == B[-4:]
G = B[-4:]

# the algorithm: (left riff, right riff); the shorter of each pair carries the bass and the kick
PAIRS = []
_l, _r = A, B
while len(_l) != len(_r):
    PAIRS.append((_l, _r))
    if len(_l) > len(_r):
        _l = _l[-(len(_l) - len(_r)):] if len(_l) - len(_r) > 0 else _l
    else:
        _r = _r[-(len(_r) - len(_l)):]
assert [(len(a), len(b)) for a, b in PAIRS] == [(52, 32), (20, 32), (20, 12), (8, 12), (8, 4)] and _l[-4:] == G and _r == G
REPS = [1, 2, 4, 8, 16]                   # how many times each pair runs its whole cycle
INTRO = 8 * 16
HOOK = [0, 3, 6, 1, 7, 10, 0, 0]          # the measure's roots, two bars each: the record's hook notes in their order


def lcm(a, b):
    x, y = a, b
    while y:
        x, y = y, x % y
    return a * b // x


def add(tr, s16, len16, pitch, vel, **expr):
    n = {"at": round(s16 / 4, 4), "len": round(len16 / 4 * 0.98, 4), "pitch": nm(pitch) if isinstance(pitch, int) else pitch, "vel": round(vel, 3)}
    if expr:
        n["expr"] = {k: float(v) for k, v in expr.items()}
    T.setdefault(tr, []).append(n)


def drum(piece, s16, vel):
    tr = {"k": "kick", "s": "snare", "h": "hat", "c": "cym", "x": "cym"}.get(piece, "toms")
    T.setdefault(tr, []).append({"at": round(s16 / 4, 4), "len": 2.0 if piece in ("c", "x") else 0.5 if piece == "h" else 0.25,
                                 "pitch": piece, "vel": round(vel, 3)})


def say(riff, t, gtrs, low=False, root=0, chord=False, stop=None, bass=True):
    """One statement of a riff from sixteenth t (cut at `stop`), on the guitars `gtrs`; with the kick, and the bass
    unless `bass` is off, if `low`."""
    for i, k in enumerate(riff):
        if k in "r-" or (stop is not None and t + i >= stop):
            continue
        n = 1
        while i + n < len(riff) and riff[i + n] == "-":
            n += 1
        at = t + i
        if k == "c":
            for tr in gtrs:
                add(tr, at, 1, F1 + root, 0.88, pm=1)
            if low:
                if bass:
                    add("bass", at, 1, F1 + root, 0.88)
                drum("k", at, 0.88)
        else:
            semi = 0 if k == "o" else int(k)
            pitch = ",".join(nm(F1 + root + j) for j in (0, 7, 12)) if chord and k == "o" else F1 + root + semi
            for tr in gtrs:
                add(tr, at, n, pitch, 1.0 if k == "o" else 0.95)
            if low:
                if bass:
                    add("bass", at, n, F1 + root + semi, 0.95)
                drum("k", at, 0.95)


def beat(s0, s1, cym="h", step=2, vel=0.5, snare=(4, 12)):
    for q in range(s0, s1, step):
        drum(cym, q, vel + (0.05 if (q - s0) % 16 == 0 else 0))
    for q in range(s0, s1, 16):
        for b in snare:
            if q + b < s1:
                drum("s", q + b, 0.95)


def fill(s):
    """The last half bar before sixteenth s."""
    for i, pc in enumerate(["t1", "t1", "t2", "t2", "ft", "ft", "s", "s"]):
        drum(pc, s - 8 + i, 0.6 + 0.045 * i)


ALL = ("gl", "gr", "dl", "dr", "wl", "wr")
def bell(side, s16, root=0, vel=None):
    if BELLS:
        add("bell-" + side, s16, 1, F1 + root + (55 if side == "l" else 60), float(BELLS.split(";")[1]) if vel is None else vel)


MARKS = [("the two given", 0)]            # (name, first sixteenth)
ROOTS = [(0, 0)]


def compose():
    # the two given: B alone on the right, twice bare (a hat in quarters) and twice with the band
    for i in range(4):
        say(B, i * 32, ("gr", "dr") if i >= 2 else ("gr",), low=i >= 2)
        bell("r", i * 32)
    beat(0, 64, cym="h", step=4, vel=0.45, snare=())
    beat(64, INTRO)
    t = INTRO
    for (left, right), reps in zip(PAIRS, REPS):
        a, b = len(left), len(right)
        cyc = lcm(a, b)
        n = cyc * reps
        MARKS.append((f"{a} against {b}", t))
        k = PAIRS.index((left, right))
        last = k == len(PAIRS) - 1
        # WHAT IS LEFT OVER IS HEARD ALONE: for the last |a - b| sixteenths of a pair the longer riff plays its tail by
        # itself (that tail is the next section's riff). The last pair leaves nothing over: two beats of silence instead
        stop = t + n - (8 if last else abs(a - b))
        # THE ARGUMENT NARROWS: the last two pairs are one guitar a side, and the last has no bass; the measure gets everything
        gl, gr = (("gl", "dl"), ("gr", "dr")) if k < 3 else (("gl",), ("gr",))
        kick_from = t + n // 2 if last else t          # the last pair: the guitars alone for its first half, then the kick

        def grow(q, t=t, stop=stop):                   # in the last pair the bells grow with the snare (0.5 to 0.9)
            return 0.5 + 0.4 * (q - t) / (stop - t)
        for i in range(n // a):
            say(left, t + i * a, gl, low=a < b and t + i * a >= kick_from, stop=stop if last or a < b else None, bass=not last)
            if not (last or a < b) or t + i * a < stop:
                bell("l", t + i * a, vel=grow(t + i * a) if last else None)
        for i in range(n // b):
            say(right, t + i * b, gr, low=b < a and t + i * b >= kick_from, stop=stop if last or b < a else None, bass=not last)
            if not (last or b < a) or t + i * b < stop:
                bell("r", t + i * b, vel=grow(t + i * b) if last else None)
        if k == 0:
            fill(t)
        drum("c", t, 0.9)
        for i in range(1, reps):                       # a crash wherever the two riffs meet again
            if cyc >= 24:
                drum("c", t + i * cyc, 0.75 if cyc >= 60 else 0.65)
        # the kit keeps common time, and its feel changes with each cut
        if k == 0:
            beat(t, stop)                                              # a hat in eighths, the snare on two and four
        elif k == 1:
            beat(t, stop, cym="x", step=4)                             # the china in quarters
        elif k == 2:
            beat(t, stop, cym="x", step=4, snare=(8,))                 # half time: the snare on three
        elif k == 3:
            beat(t, stop)                                              # the hat again, the backbeat back
        else:
            beat(t, stop, snare=())                                    # the snare on every beat, growing
            beats = list(range(t, stop, 4))
            for j, q in enumerate(beats):
                drum("s", q, 0.45 + 0.55 * j / (len(beats) - 1))
        t += n
    # the measure: every guitar on the four sixteenths both riffs end with; the cell climbs the hook notes as chords
    MARKS.append(("the measure", t))
    drum("c", t, 0.95)
    for j, root in enumerate(HOOK):
        ROOTS.append((t + j * 32, root))
        for i in range(8):
            say(G, t + j * 32 + i * 4, ALL, low=True, root=root, chord=True)
            for side in "lr":
                bell(side, t + j * 32 + i * 4, root, float(BELLS.split(";")[2]) if BELLS else 0)
        if j:
            drum("c", t + j * 32, 0.7)
    beat(t, t + 256, cym="x", step=4, vel=0.5)
    t += 256
    # measured: the two riffs said together, in unison, the beat under them
    MARKS.append(("measured", t))
    fill(t)
    drum("c", t, 0.95)
    s = t
    for riff in (A, A, A, A, B, B, B, B):
        say(riff, s, ALL, low=True)
        bell("l", s)
        bell("r", s)
        if s > t:
            drum("c", s, 0.7)
        s += len(riff)
    beat(t, s, cym="x", step=4, vel=0.5)
    fill(s)
    MARKS.append(("one chord", s))
    for tr in ALL:
        add(tr, s, 32, ",".join(nm(F1 + j) for j in (0, 7, 12, 19)), 0.95)
    add("bass", s, 32, F1, 0.95)
    drum("k", s, 0.95)
    drum("c", s, 0.95)
    bell("l", s)
    bell("r", s)
    ROOTS.append((t, 0))
    return s + 32


def song():
    total = compose()
    assert total % 16 == 0 and all(m[1] % 16 == 0 for m in MARKS)
    kit = "ct-kit-here"
    air = [{"type": "eq", "bands": ["highshelf cutoff=9000 gain=-2dB"]}]
    main = "ct-twin fx.1.model=gojira fx.2.mic=0.5 fx.2.cone={}"
    dbl = "ct-twin fx.1.model=modern fx.2.mic=0.35 fx.2.cone={}"            # each riff is two takes: a second through another amp, microphone and cone
    mids = {"fx": [{"type": "eq", "bands": ["peak cutoff=700 q=0.9 gain=2.5dB"]}]}
    wall = {"fx": [{"type": "eq", "bands": ["peak cutoff=380 q=1 gain=-3dB"]}]}
    tracks = [
        {"name": "gl", "patch": main.format(60), "gain": os.environ.get("C10T8_MAIN", "0.7dB"), "pan": -1, "out": "gtrs", **mids},
        {"name": "gr", "patch": main.format(61), "gain": os.environ.get("C10T8_MAIN", "0.7dB"), "pan": 1, "out": "gtrs", **mids},
        {"name": "dl", "patch": dbl.format(62), "gain": os.environ.get("C10T8_DBL", "-2.5dB"), "pan": -0.75, "out": "gtrs", **mids},
        {"name": "dr", "patch": dbl.format(63), "gain": os.environ.get("C10T8_DBL", "-2.5dB"), "pan": 0.75, "out": "gtrs", **mids},
        {"name": "wl", "patch": "ct-wall-stop-l", "gain": "-3.5dB", "pan": -0.75, "out": "gtrs", **wall},
        {"name": "wr", "patch": "ct-wall-stop-r", "gain": "-3.5dB", "pan": 0.75, "out": "gtrs", **wall},
        *([{"name": "bell-" + side, "patch": "cm-bell", "gain": f"{float(BELLS.split(';')[0]) + (float(BELLS.split(';')[3]) if side == 'l' else 0):g}dB", "pan": pan}
           for side, pan in (("l", -0.6), ("r", 0.6))] if BELLS else []),
        {"name": "bass", "patch": "ct-bass", "gain": "0.5dB", "pan": 0, "out": "low"},
        {"name": "kick", "patch": kit, "gain": "2dB", "out": "drums", "fx": [{"type": "eq", "bands": ["peak cutoff=4500 q=0.8 gain=10dB"]}]},
        {"name": "snare", "patch": kit, "gain": "3.5dB", "out": "drums", "sends": {"oh": "-1.5dB", "snr": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=7000 gain=-3dB"]}]},
        {"name": "toms", "patch": kit, "gain": "4dB", "out": "drums", "sends": {"oh": "-1.5dB"}},
        {"name": "cym", "patch": kit, "gain": "-4.5dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
        {"name": "hat", "patch": kit, "gain": "14dB", "out": "drums", "sends": {"oh": "4.5dB"}, "fx": air},
    ]
    for t in tracks:
        t["notes"] = sorted(T.get(t["name"], []), key=lambda n: n["at"])

    def key_f(hz):
        return {"value": hz, "mod": [{"src": "auto.key", "amount": round(1 / 12, 5)}]}

    pts, prev = [["0b", 0]], 0
    for p, r in ROOTS[1:]:
        if r != prev:
            pts += [[f"{p / 4 - 0.02:g}b", prev], [f"{p / 4:g}b", r]]
            prev = r
    return {
        "about": ("chirpers X (Common Time), track 8 by chirper-zero: Common Measure. Two riffs of different lengths, 52 sixteenths on the "
                  "left guitar and 32 on the right, and Euclid's way of finding what measures both: take the less from the greater. "
                  "Each section the longer riff is cut down to what was left over, its own tail: 52 against 32, 20 against 32, 20 "
                  "against 12, 8 against 12, 8 against 4. Four goes into eight: the measure is one beat, the four sixteenths both "
                  "riffs end with, and then the two riffs are played whole, together. The fast song: 160. v1 is the skeleton."),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -10, "seed": 1, "tail": "5s", "length": f"{total // 4}b", "event_stable": True,
        "patches": {"ct-kit-here": {"extends": "ct-kit", "kit": {"x": {"pan": 0.35}, "rde": {"pan": 0.4}, "rb": {"pan": 0.35}, "h": {"pan": -0.45}}},
                    **({"cm-bell": {
                        "about": ("Common Measure's bell (chirper-zero, 17 Nov): the library's agogo bell (afro-perc's `ah`: three partials at 1, "
                                  "2.4 and 3.9 and a 4 ms click) as a patch that takes a pitch, so the two bells can sit on the song's fifth "
                                  "and root and follow the chords."),
                        "synth": {"amp": {"a": "0.2ms", "curve": 3, "d": "240ms", "r": "30ms", "s": 0},
                                  "env": {"h": {"a": "0.2ms", "d": "4ms", "s": 0}},
                                  "layers": [{"type": "additive", "damp": 0.3, "partials": [[1, 1], [2.4, 0.4], [3.9, 0.15]]},
                                             {"type": "noise", "level": {"value": "-60dB", "mod": [{"src": "env.h", "amount": 40}]}}]}}} if BELLS else {})},
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
        "master": {"fx": [{"type": "eq", "bands": ["hp cutoff=24"]}, {"type": "gain", "gain": os.environ.get("C10T8_MASTER", "2.7dB")}]},
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
    if os.environ.get("C10T8_SHOW"):
        end = compose()
        sec = 15 / BPM
        for (name, s0), (_, s1) in zip(MARKS, MARKS[1:] + [("", end)]):
            print(f"{name:16s} bars {s0 // 16 + 1:3d}-{s1 // 16 + 1:3d}  {int(s0 * sec) // 60}:{s0 * sec % 60:04.1f}-{int(s1 * sec) // 60}:{s1 * sec % 60:04.1f}")
    else:
        open(OUT, "w").write(dump(song()))
