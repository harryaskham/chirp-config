#!/usr/bin/env python3
"""chirpers1-t2 (chirper-three): the statement. Track 2 of Ferrous Bloom.

Identity: 144 BPM straight 4/4, full force. TRIAD, the album's main riff: LATTICE's 7-cell in its three rotations
(3+2+2, 2+3+2, 2+2+3) chained into a 21-sixteenth phrase whose first chugs pivot through the LATTICE colour
F -> Gb -> B (with an E2 stab). The phrase restarts every 4 bars (64 = 21+21+22, the last one stretched by a chug),
so the riff turns over against the steady kit and snaps back on every fourth downbeat.
Form: Ignition (t1's cluster still ringing) - Statement - Statement II (lead) - Hinge (3+3+3+3+4 tritone riff) -
Release (clean LATTICE in eighth-note augmentation) - Return (TRIAD harmonised) - Bloom (guitars on TRIAD's 21,
kick on Hinge's grouping: polymeter) - Exhale (half-time TRIAD into a held F-B cluster for t3).

Emits songs/chirpers1-t2.yaml. Edit the music here, not the YAML.
"""
import json, os

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers1-t2.yaml")
TEMPO = 144
S = 16
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"
F1 = 29
LATTICE = [0, 1, 6, 11]                       # F Gb B E

SEC = {"ignite": (1, 4), "stmt": (5, 20), "stmt2": (21, 36), "hinge": (37, 52), "release": (53, 68),
       "ret": (69, 84), "bloom": (85, 104), "exhale": (105, 120)}
BARS = 120
TOTAL = BARS * S
def bar0(b):
    return (b - 1) * S
def span(k):
    a, z = SEC[k]
    return bar0(a), bar0(z + 1)

# ---------- TRIAD: the 21-sixteenth phrase from the three rotations of the 7-cell ----------
ROT = [[0, 3, 5], [0, 2, 5], [0, 2, 4]]       # 3+2+2, 2+3+2, 2+2+3
PIVOT = [0, 1, 6]                             # F, Gb, B: each rotation's first chug
def triad(a, z, half=False):
    """(time, length, kind, pivot) for TRIAD between a and z, restarting every 4 bars (21+21+22)."""
    out = []
    for blk in range(a, z, 64):
        t = blk
        for ph in range(3):
            for r in range(3):
                for i, o in enumerate(ROT[r]):
                    st = t + 7 * r + o
                    if st >= min(blk + 64, z):
                        continue
                    if half and i != 0:
                        continue
                    nxt = (ROT[r] + [7])[i + 1] - o
                    out.append((st, nxt, "pivot" if i == 0 else "chug", PIVOT[r]))
            if ph == 2:                       # the stretched last phrase: one extra chug
                if t + 21 < min(blk + 64, z) and not half:
                    out.append((t + 21, 1, "chug", 0))
            t += 21
    return out

def hinge(a, z):
    """3+3+3+3+4 per bar: chugs on the groups, a tritone stab on the 4, alternate bars pivot on Gb."""
    out = []
    for b0 in range(a, z, S):
        n = (b0 - a) // S
        for g in (0, 3, 6, 9):
            out.append((b0 + g, 3, "chug", 1 if (n % 2 and g == 0) else 0))
        out.append((b0 + 12, 2, "stab", 6))
        out.append((b0 + 14, 1, "chug", 0))
        out.append((b0 + 15, 1, "chug", 0))
    return out

# ---------- serialisation ----------
DUR = {1: "/16", 2: "/8", 3: "/8.", 4: "/4", 6: "/4.", 8: "/2", 12: "/2.", 16: "/1"}
def dur(n):
    if n in DUR:
        return DUR[n]
    parts, rest = [], n
    for k in (16, 8, 4, 2, 1):
        while rest >= k:
            parts.append(k); rest -= k
    return "/" + "+".join(DUR[p][1:] for p in parts)

def score(events, total=TOTAL):
    ev = sorted(events, key=lambda e: e[0])
    out, t = [], 0
    for i, (st, ln, tok, vel, pre) in enumerate(ev):
        if st < t:
            continue
        if st > t:
            out.append("R" + dur(st - t))
        nxt = ev[i + 1][0] if i + 1 < len(ev) else total
        ln = max(1, min(ln, nxt - st, total - st))
        out.append((pre + " " if pre else "") + f"{tok}{dur(ln)}@{int(vel)}")
        t = st + ln
    if t < total:
        out.append("R" + dur(total - t))
    return " ".join(out)

def ramp(t, a, z, v0, v1):
    return v0 + (v1 - v0) * max(0.0, min(1.0, (t - a) / max(1, z - a)))

# ---------- parts ----------
PM, OP = "expr.pm=1", "expr.pm=0"
def chord(*ms):
    return ",".join(nm(m) for m in ms)

def riff_events(octave_up_pivots=False):
    """The rhythm guitars' material for every section."""
    ev = []
    clus = chord(F1, F1 + 6, F1 + 11)
    ev.append((bar0(1), 2 * S, clus, 112, OP))                                   # Ignition: t1's cluster rings on
    for st, ln, kind, p in triad(bar0(3), bar0(5)):                             # then TRIAD's rhythm gathers under it
        ev.append((st, ln, nm(F1 + p) if kind == "pivot" else nm(F1), ramp(st, bar0(3), bar0(5), 70, 100),
                   OP if kind == "pivot" else PM))
    for k, v0, v1 in (("stmt", 104, 112), ("stmt2", 106, 114), ("ret", 108, 116), ("bloom", 110, 120)):
        a, z = span(k)
        for st, ln, kind, p in triad(a, z):
            if kind == "pivot":
                base = F1 + p
                tok = chord(base, base + 12) if (octave_up_pivots and k in ("ret", "bloom")) else (
                    chord(F1, F1 + 11) if p == 6 and (st - a) % 64 >= 42 else nm(base))   # the E stab on the 3rd phrase
                ev.append((st, ln, tok, ramp(st, a, z, v0 + 6, v1 + 6), OP))
            else:
                ev.append((st, ln, nm(F1), ramp(st, a, z, v0 - 14, v1 - 10), PM))
    a, z = span("hinge")
    for st, ln, kind, p in hinge(a, z):
        if kind == "stab":
            ev.append((st, ln, chord(F1, F1 + 6), 118, OP))
        else:
            ev.append((st, ln, nm(F1 + p), 98 if p else 94, PM))
    a, z = span("exhale")
    for st, ln, kind, p in triad(a, bar0(117), half=True):
        ev.append((st, 6, nm(F1 + p), ramp(st, a, bar0(117), 112, 92), OP))
    ev.append((bar0(117), S, chord(F1, F1 + 6, F1 + 12), 108, OP))              # the F-B cluster, one bar, then the guitars stop
    return ev

def guitar(right=False):
    return score(riff_events(octave_up_pivots=right))

def bass():
    ev = []
    for st, ln, tok, v, pre in riff_events():
        if "," in tok:                         # chords: the bass takes the root
            tok = tok.split(",")[0]
        ev.append((st, ln, tok, min(124, v), ""))
    a, z = span("release")                     # the release: long roots under the clean motif
    ev = [e for e in ev if not (a <= e[0] < z)]
    for b in range(53, 69, 4):
        ev.append((bar0(b), 4 * S, nm(F1 + (0 if (b - 53) % 8 == 0 else 1)), 74, ""))
    ev.append((bar0(118), 3 * S, nm(F1), 72, ""))                # the F rings on under the hand-off to Moult
    return score(ev)

HANDOFF = bar0(118)   # the last 3 bars: Moult's pulse (96 BPM quarter = 144 BPM dotted quarter) arrives early

def clean():                                    # the release: LATTICE's 7-cell in eighth-note augmentation
    ev = []
    a, z = span("release")
    k = 0
    t = a
    while t < z:
        for i, o in enumerate([0, 6, 10]):      # 3+2+2 eighths = 6+4+4 sixteenths
            st = t + o
            if st < z:
                nxt = ([0, 6, 10] + [14])[i + 1] - o
                ev.append((st, nxt, nm(F1 + 36 + LATTICE[k % 4]), ramp(st, a, z, 62, 80), ""))
                k += 1
        t += 14
    for i, st in enumerate(range(HANDOFF, TOTAL, 6)):  # muted plucks on the dotted quarter: F-C, then A-C# (Moult's colour)
        ev.append((st, 3, chord(F1 + 24, F1 + 31) if i < 4 else chord(F1 + 28, F1 + 32), 70 + 2 * i, PM))
    return score(ev)

def pad():
    ev = [(bar0(1), 4 * S, chord(F1 + 12, F1 + 18, F1 + 23), 70, "")]
    a, z = span("release")
    for b in range(53, 69, 4):
        top = F1 + 25 if (b - 53) % 8 == 4 else F1 + 23
        ev.append((bar0(b), 4 * S, chord(F1 + 12, F1 + 18, top), 66, ""))
    ev.append((bar0(117), 2 * S, chord(F1 + 12, F1 + 18, F1 + 24), 70, ""))
    ev.append((bar0(119), 2 * S, chord(F1 + 12, F1 + 16, F1 + 20), 62, ""))  # F-A-C#: the colour leans into Moult
    return score(ev)

def lead():
    ev = []
    for i, m in enumerate(LATTICE):             # Statement II: the line in long notes, 4 bars each, an octave up
        ev.append((bar0(21 + 4 * i), 4 * S, nm(F1 + 36 + m), 84, ""))
    for i, m in enumerate([11, 12, 11, 13]):    # Bloom: E5 -> F5 -> E5 -> Gb5, the semitone pull from t1
        ev.append((bar0(85 + 5 * i), 5 * S, nm(F1 + 36 + m), 90, ""))
    return score(ev)

def kick():
    ev = [(bar0(1), 1, "k", 118, "")]
    for st, ln, tok, v, pre in riff_events():
        if bar0(3) <= st < bar0(85) and not (bar0(53) <= st < bar0(69)):
            ev.append((st, 1, "k", min(124, v + 2), ""))
    a, z = span("bloom")                        # polymeter: the kick plays Hinge's grouping under TRIAD
    for st, ln, kind, p in hinge(a, z):
        ev.append((st, 1, "k", 118 if kind == "stab" else 108, ""))
    for b in range(53, 69):                     # release: kick on 1 only
        ev.append((bar0(b), 1, "k", 84, ""))
    a, z = span("exhale")
    for st, ln, kind, p in triad(a, bar0(117), half=True):
        ev.append((st, 1, "k", 110, ""))
    ev.append((bar0(117), 1, "k", 120, ""))
    return score(ev)

def snare():
    ev = []
    for e8 in range(8):                         # Ignition's build: eighths, then a sixteenth roll into the Statement
        ev.append((bar0(3) + 2 * e8, 1, "s", 64 + 3 * e8, ""))
    for k in range(16):
        ev.append((bar0(4) + k, 1, "s", 86 + 2 * k, ""))
    for b in range(5, 117):
        if 53 <= b < 69:                       # release: a soft backbeat on 3
            ev.append((bar0(b) + 8, 1, "s", 70, ""))
        elif 37 <= b < 53 or b >= 105:         # Hinge and Exhale: half-time
            ev.append((bar0(b) + 8, 1, "s", 116, ""))
        else:
            for q in (4, 12):
                ev.append((bar0(b) + q, 1, "s", 114, ""))
    for k in range(16):                         # fills into Hinge, Return, Bloom
        for b in (36, 68, 84):
            ev.append((bar0(b) + k, 1, "s", 80 + 2 * k, ""))
    ev.append((bar0(117), 1, "s", 122, ""))
    return score(ev)

def cym():
    ev = [(bar0(1), 1, "c", 120, "")]
    for b in range(5, 117):
        if 53 <= b < 69:
            for q in range(4):
                ev.append((bar0(b) + 4 * q, 1, "rb", 64, ""))
            continue
        if b in (5, 21, 37, 69, 85, 105):
            ev.append((bar0(b), 1, "c", 124, ""))
            start = 2
        else:
            start = 0
        tok = "rd" if (21 <= b < 37 or 85 <= b < 105) else "h"
        for e8 in range(start // 2, 8):
            ev.append((bar0(b) + 2 * e8, 1, tok, 92 if e8 % 2 == 0 else 74, ""))
    a, z = span("stmt2")                        # china on TRIAD's Gb pivots in Statement II
    for st, ln, kind, p in triad(a, z):
        if kind == "pivot" and p == 1:
            ev.append((st, 1, "x", 108, ""))
    ev.append((bar0(117), 1, "c", 124, ""))
    for st in range(HANDOFF, TOTAL, 6):         # closed hats on Moult's pulse, a ghost between
        ev.append((st, 1, "h", 70, ""))
        ev.append((st + 3, 1, "h", 42, ""))
    return score(ev)

def ride():
    sec = 4 * 60 / TEMPO
    t = lambda b: f"{(b - 1) * sec:.2f}s"
    pts = [(1, 0.0), (52.8, 0.0), (53.2, -5.0), (66, -5.0), (69, 0.0), (118, 0.0), (121, -4.0)]
    return [[t(b), v] for b, v in pts]

def tr(name, patch, sc, **kw):
    d = {"name": name, "patch": patch, "score": sc}
    d.update(kw)
    return d

def main():
    tracks = [
        tr("gtr-l", "m8-emg-l", guitar(), pan="L90", gain="-4dB", seed=7),
        tr("gtr-r", "m8-emg-r", guitar(right=True), pan="R90", gain="-4dB", seed=13),
        tr("bass", "bass-fat", bass(), gain="-2dB", fx=[{"type": "duck", "by": "kick", "depth": "-3dB", "attack": "2ms", "release": "90ms"}]),
        tr("lead", "m8-lead", lead(), gain="-7dB", sends={"hall": "-8dB"}, fx=["delay time=3/8 feedback=0.3 mix=0.18"]),
        tr("clean", "m8-clean", clean(), pan="L30", gain="-3dB", sends={"hall": "-8dB"}, fx=["delay time=3/16 feedback=0.35 mix=0.25"]),
        tr("pad", "pad-glass", pad(), gain="-8dB", sends={"hall": "-6dB"}),
        tr("kick", "metal-kit-dry", kick(), out="drums"),
        tr("snare", "metal-kit-dry", snare(), out="drums"),
        tr("cym", "metal-kit-dry", cym(), out="drums"),
    ]
    head = [
        'about: "Chirpers - Ferrous Bloom, track 2: the statement (chirper-three). Generated by compose/chirpers1/src/chirpers1-t2.py; TRIAD, a 21-sixteenth riff from LATTICE\'s three 7-cell rotations, restarting every 4 bars."',
        f"tempo: {TEMPO}",
        'tail: "0.5s"',                # the held F-B cluster is still ringing when t3 begins (the songs bleed)
        'ceiling: "-0.1dB"',
        "buses:",
        '  hall: {fx: ["reverb kind=hall decay=2.6s mix=1 predelay=20ms mono_below=150hz"]}',
        '  drums: {fx: [{"type": "compressor", "threshold": "-18dB", "ratio": 3, "attack": "10ms", "release": "90ms", "makeup": "2dB"}, "reverb kind=room decay=0.6s mix=0.07 predelay=6ms mono_below=200hz"]}',
        'master: ' + json.dumps({"fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}},
                                       "glue threshold=-18dB ratio=2.5 attack=10ms release=150ms makeup=2dB",
                                       {"type": "gain", "gain": "10dB"}],
                                "auto": {"ride": {"points": ride()}}}),
        "tracks:",
    ]
    with open(OUT, "w") as f:
        f.write("\n".join(head + ["  - " + json.dumps(t) for t in tracks]) + "\n")
    print(OUT, f"{BARS} bars at {TEMPO} BPM = {BARS * 4 * 60 / TEMPO:.1f} s")

if __name__ == "__main__":
    main()
