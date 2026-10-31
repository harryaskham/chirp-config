#!/usr/bin/env python3
"""chirpers7-t18 (The Endless Stair, track 18: the closer) - generator for songs/chirpers7-t18.yaml (chirper-zero).

THE CLOSER: AMBIENT DEEP HOUSE / "the stair comes down". 120 bpm, then a decelerando to 112 over the last 32 bars (the
tape's end). D minor (7A) for the first half, rising a fifth to A minor (8A) - home, where t1 began - for the last third.
Featured illusion: THE STAIR COMES DOWN - the tape's thread, which t1 taught as an endlessly rising Shepard scale, falls
for ever: its four notes (5 3 2 1) on Shepard tones, each step smaller than a tritone (A F E D A ... : -4 -1 -2 -5), so
every step is heard going down, the stair descends through the whole track and never gets lower. Under the break,
falling Shepard chords: a pad gliding down an octave every eight seconds, for ever. Original; a style, not a version of
any track.

Form (4/4 bars): INTRO 32 (bars 1-16 the seam from t17: kick, hats, a held D; then the pads and the first steps) / A 32
(the groove; the stair a beat a step; A2 the clap and the stair doubled) / BREAK 16 (no kick: the falling chords, the stair
at half speed) / B 32 / HOME 32 (A minor: the stair in A, the brightest pads, the open hats) / OUTRO 32 (the decelerando
120 -> 112; the kick leaves at bar 17; the stair falls alone into a held A minor).
Run: python3 compose/chirpers7/src/chirpers7-t18.py  (writes songs/chirpers7-t18.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C7T18_OUT") or os.path.join(ROOT, "songs", "chirpers7-t18.yaml")
BPM0, BPM1 = 120, 112
S = 0.25
BAR = 16
MGAIN = float(os.environ.get("C7T18_MGAIN", "8"))
FCOMP = os.environ.get("C7T18_FCOMP", "-16,0.3ms")
OUTRO = os.environ.get("C7T18_OUTRO", "0") == "1"  # the outro is its own room: the hats and the clap stop as it starts, only the kick, the sub and the falling stair walk on
EQ2 = os.environ.get("C7T18_EQ2", "0") == "1"  # 50 Hz down 10 dB (was 7), the air shelf at 9 kHz +8 dB (was 5)
RIM3 = os.environ.get("C7T18_RIM3", "1") == "1"
FORM2 = os.environ.get("C7T18_FORM2", "1") == "1"  # B splits (B2: the stair doubled an octave up, the hats open, no clap) and the outro is the falling floor: the kick leaves at its first bar, the falling Shepard chords return in A minor under the decelerando  # a soft rim on every third 16th in the grooves (a dotted-eighth cycle across the bar lines): the stair's echo in the kit

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 32), ("A", 32), ("break", 16), ("B", 32), ("home", 32), ("outro", 32)]
CHD = [(38, [53, 57, 60, 64]),   # Dm9: F3 A3 C4 E4 over D
       (34, [53, 57, 62, 65]),   # Bbmaj7(9): F3 A3 D4 F4 over Bb
       (31, [50, 53, 57, 58]),   # Gm9: D3 F3 A3 Bb3 over G
       (33, [52, 55, 59, 62])]   # A7sus: E3 G3 B3 D4 over A
CHA = [(33, [48, 52, 55, 59]),   # Am9: C3 E3 G3 B3 over A
       (29, [52, 55, 57, 60]),   # Fmaj7(9): E3 G3 A3 C4 over F
       (38, [53, 57, 60, 64]),   # Dm9 over D
       (40, [50, 55, 57, 62])]   # E7sus: D3 G3 A3 D4 over E (the sus resolving home)
STAIR_D = ["A4", "F4", "E4", "D4"]   # 5 3 2 1 of D minor, falling (-4 -1 -2, then -5 to the next A)
STAIR_A = ["E4", "C4", "B3", "A3"]   # 5 3 2 1 of A minor
TRACKS = ("kick", "hats", "clap", "sub", "pads", "stair", "fall", "stair2")


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total_steps():
    return sum(nb for _, nb in FORM) * BAR


def stream(events, total):
    by = {}
    for st, head, ln, vel in events:
        if st in by:
            h0, l0, v0 = by[st]
            n0, _, a0 = h0.partition("^")
            by[st] = (f"{n0},{head.partition('^')[0]}" + (f"^{a0}" if a0 else ""), min(l0, ln), max(v0, vel))
        else:
            by[st] = (head, ln, vel)
    ev = sorted((st, h, l, v) for st, (h, l, v) in by.items())
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else total
        hold = max(1, min(ln, max(nxt, st + 1) - st, total - st))
        out.append(R((st - pos) * S))
        note, _, art = head.partition("^")
        out.append(f"{note}/{hold * S:g}b@{int(vel)}" + (f"^{art}" if art else ""))
        pos = st + hold
    out.append(R((total - pos) * S))
    return J(*out)


def build():
    ev = {k: [] for k in TRACKS}

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    total = total_steps()
    step_i = 0  # the stair counts on, never restarting
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            home = sec in ("home", "outro")
            r, v = (CHA if home else CHD)[b % 4]
            stair = STAIR_A if home else STAIR_D
            seam_in = sec == "intro" and b < 16
            last = sec == "outro" and b >= 16
            # kick: everywhere but the break and the outro's second half
            if sec != "break" and not last and not (FORM2 and sec == "outro"):
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, (104 if q == 0 else 96) - (10 if sec == "outro" else 0))
            # hats: off-beats (open in home), a soft shaker on the 16ths in the grooves
            if not (sec == "break" and b < 12) and not (last and b >= 24) and not (OUTRO and sec == "outro"):
                for q in (2, 6, 10, 14):
                    add("hats", at + q, "oh" if ((sec == "home" and q in (6, 14)) or (FORM2 and sec == "B" and b >= 16)) else "h", 1, 66)
                if sec in ("A", "B", "home"):
                    for q in (1, 3, 5, 7, 9, 11, 13, 15):
                        add("hats", at + q, "h", 1, 38)
            if RIM3 and sec in ("A", "B", "home"):
                for q in range(16):
                    k = (at + q) - sec_start("A")
                    if k % 3 == 0:
                        add("clap", at + q, "rs", 1, 70 if (k // 3) % 4 == 0 else 58)
            if (sec == "A" and b >= 16) or (sec == "B" and not (FORM2 and b >= 16)) or sec == "home":
                add("clap", at + 4, "cp", 1, 84)
                add("clap", at + 12, "cp", 1, 88)
            # sub: the held D under the seam, the roots elsewhere (none in the break), a held A at the very end
            if seam_in:
                if b % 4 == 0:
                    add("sub", at, "D2", 4 * BAR, 88)
            elif last:
                if b == 16:
                    add("sub", at, "A1", 16 * BAR, 80)
            elif sec != "break":
                add("sub", at, nm(r), 7, 94)
                add("sub", at + 10, nm(r), 5, 84)
            # pads: glassy chords from bar 17 on, held two bars
            if not seam_in and b % 2 == 0 and sec != "break":
                add("pads", at, ",".join(nm(n + 12) for n in v), 2 * BAR, 70 if sec != "home" else 80)
            if last and b == 28:
                add("pads", at, ",".join(nm(n + 12) for n in CHA[0][1]), 4 * BAR, 72)
            # THE STAIR COMES DOWN: a step a beat in the grooves, a step a half-bar in the break and the outro's end
            if not seam_in and not (sec == "intro" and b < 24):
                per = 8 if (sec == "break" or last) else 4
                for q in range(0, 16, per):
                    n = stair[step_i % 4]
                    vel = 88 if step_i % 4 == 0 else 76
                    if sec == "A" and b >= 16:
                        add("stair", at + q, n, per, vel + 4)
                    else:
                        add("stair", at + q, n, per, vel)
                    step_i += 1
            if FORM2 and sec == "B" and b >= 16:  # B2: the stair shimmers an octave up with it
                for q in range(0, 16, 4):
                    add("stair2", at + q, stair[(step_i - 4 + q // 4) % 4], 4, 70)
            # the falling chords under the break (Shepard pad gliding down), and (FORM2) under the outro's decelerando
            if FORM2 and sec == "outro" and b % 8 == 0:
                add("fall", at, ",".join(nm(n) for n in CHA[0][1]), 8 * BAR, 72)
            if sec == "break" and b % 8 == 0:
                add("fall", at, ",".join(nm(n) for n in v), 8 * BAR, 76)
    return {k: stream(ev[k], total) for k in TRACKS}


def lane(points, step=True):
    spb = 60 / BPM0
    pts = [["0s", points[0][1]]]
    prev = points[0][1]
    for t16, val in points[1:]:
        t = t16 * S * spb
        if step:
            pts.append([f"{max(0.0, t - 0.01):.3f}s", prev])
        pts.append([f"{t:.3f}s", val])
        prev = val
    pts.append([f"{total_steps() * S * spb + 20:.2f}s", pts[-1][1]])
    return {"points": pts}


def song():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    beats = lambda t16: f"{t16 // 4}b"  # noqa: E731
    total_b = total_steps() // 4
    tempo = [{"at": "0b", "bpm": BPM0}, {"at": beats(st["outro"]), "bpm": BPM0}, {"at": f"{total_b}b", "bpm": BPM1, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "2ms", "release": "220ms", "curve": 0.7}
    dyn = lane([(0, -4), (st["intro"] + 16 * BAR, -3), (st["A"], -1), (st["A"] + 16 * BAR, 0), (st["break"], -7), (st["B"], 0),
                (st["home"], 1), (st["outro"], -2), (st["outro"] + 16 * BAR, -5)])
    doc = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 18 by chirper-zero: THE CLOSER, ambient deep house, the stair "
                 "comes down. THE STAIR falling for ever on Shepard tones while the key steps up home. Generated by "
                 "compose/chirpers7/src/chirpers7-t18.py; see its docstring and compose/chirpers7/styles.md.",
        "tempo": tempo, "ceiling": "-1dB", "loudness": -11, "tail": "3s",
        "patches": {
            "stair-down": {"about": "the stair comes down: Shepard tones (chirper-two's c2-stair recipe), a softer decay",
                           "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "1200hz", "width": 1.2}}],
                                     "amp": {"a": "6ms", "d": "900ms", "s": 0.3, "r": "600ms"}}},
            "fall-pad": {"about": "the stair comes down: falling Shepard chords - each note glides down an octave every 8 s, for ever",
                         "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "300hz", "width": 1.2, "cycle": "8s", "down": True}}],
                                   "amp": {"a": "2s", "s": 1, "r": "4s"}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", f"peak cutoff=50 q=1 gain={-10 if EQ2 else -7}dB", "peak cutoff=110 q=1 gain=3dB", "peak cutoff=320 q=0.8 gain=-3dB",
                                                   "peak cutoff=1000 q=0.7 gain=-3dB", "peak cutoff=1400 q=1.2 gain=-4dB", "highshelf cutoff=4500 gain=9dB",
                                                   f"highshelf cutoff=9000 gain={8 if EQ2 else 5}dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "compressor", "threshold": f"{FCOMP.split(',')[0]}dB", "ratio": 8, "attack": FCOMP.split(',')[1], "release": "60ms", "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": dyn}},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4s mix=1 predelay=30ms", "lp cutoff=7000"]},
            "echo": {"fx": ["delay time=3/16 feedback=0.4 mix=1 tone=2600", "hp cutoff=300", "reverb kind=hall decay=2.5s mix=0.3"]},
        },
        "tracks": [
            {"name": "kick", "patch": "machine-kit", "gain": "-3dB", "score": T["kick"]},
            {"name": "hats", "patch": "machine-kit", "gain": "-4dB", "pan": 0.1, "lfo": {"hh": "sine rate=7/1"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": {"value": 3500, "mod": [{"src": "lfo.hh", "amount": 0.5}]}, "q": 0.7}], "score": T["hats"]},
            {"name": "clap", "patch": "machine-kit", "gain": "-10dB", "sends": {"hall": "-10dB"}, "score": T["clap"]},
            {"name": "sub", "patch": "sub", "gain": "-14dB", "fx": [pump, {"type": "phantom", "cutoff": 100, "harmonics": "-6dB"}], "score": T["sub"]},
            {"name": "pads", "patch": "pad-glass", "gain": "-15dB", "fx": [pump], "sends": {"hall": "-6dB"}, "score": T["pads"]},
            {"name": "stair", "patch": "stair-down", "gain": "-12dB", "sends": {"echo": "-8dB", "hall": "-8dB"}, "score": T["stair"]},
            *([{"name": "stair2", "patch": "stair-down", "gain": "-16dB", "transpose": 12, "pan": 0.3, "sends": {"echo": "-6dB"}, "score": T["stair2"]}] if FORM2 else []),
            {"name": "fall", "patch": "fall-pad", "gain": "-12dB", "sends": {"hall": "-4dB"}, "score": T["fall"]},
        ],
    }
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "loudness", "tail", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
