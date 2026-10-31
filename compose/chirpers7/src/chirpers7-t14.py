#!/usr/bin/env python3
"""chirpers7-t14 (The Endless Stair, track 14) - generator for songs/chirpers7-t14.yaml (chirper-zero).

RESTRAINED JACKIN' HOUSE, PEAK PLATEAU / "both ears". 124 bpm throughout (the plateau: t13 -> t14 -> t15 all meet at
124), F minor (4A). The top of the night, held: a shuffled, bouncing groove with a swung hat, claps and rim rolls, short
organ stabs, a pumping bassline. Featured illusion: THE SCALE ILLUSION (Deutsch) - a rising and a falling scale play at
once, their notes swapping ears on every step, so neither ear plays a melody; the brain sorts the tones by pitch and
hears a smooth high V in one ear and a low inverted V in the other. Original; a style, not a version of any track.

Form (4/4 bars): INTRO 32 (bars 1-16 the seam from t13: kick, hats, a held F; organ stabs from 17, the bass and the clap
from 25) / A 32 (the groove; A2 the scales enter, quiet) / BREAK 16 (no kick: the scales alone over a glass pad) / B 48
(B1 the scales over the full groove; B2 the scales in 16ths, twice as fast, the organ answering) / OUTRO 32 (the scales
fade; the last 16 bars the seam into t15: kick, hats, a held C2).
Run: python3 compose/chirpers7/src/chirpers7-t14.py  (writes songs/chirpers7-t14.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C7T14_OUT") or os.path.join(ROOT, "songs", "chirpers7-t14.yaml")
BPM = 124
S = 0.25
BAR = 16
MGAIN = float(os.environ.get("C7T14_MGAIN", "8"))
FCOMP = os.environ.get("C7T14_FCOMP", "-16,0.3ms")
SEAMLV = os.environ.get("C7T14_SEAMLV", "-0.5,1")  # the seam bars' levels (first 16, last 16, dB): set to meet t13's tail and t15's head as the live crossfade plays them
SOLO = os.environ.get("C7T14_SOLO", "1") == "1"  # chirper-one's note: B bars 23-24 the scales alone, unaccompanied, so the room hears the two lines it imagines before the groove folds them back in (and B2 lands with them in 16ths)
PRES = os.environ.get("C7T14_PRES", "1") == "1"  # presence: the clap 3 dB up and 3.5 kHz +3 dB (2.6-4.2 kHz read 7-9 dB under the album)
DOT = os.environ.get("C7T14_DOT", "")  # a dotted-eighth rim and shaker cycle (every third 16th across the bar lines) in the named sections: "B" or "A,B"
KEYUP = int(os.environ.get("C7T14_KEYUP", "3"))  # B2 lands in another key: after the scales alone (still F minor), the groove and both scales come back KEYUP semitones up (3: A-flat minor - the top of the stair goes one step higher), and the outro walks home to F minor for the seam
ANTIC = os.environ.get("C7T14_ANTIC", "1") == "1"  # the organ stabs anticipate: on the a-of-1 and the a-of-3 (16ths 3 and 11), jackin' pushes

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 32), ("A", 32), ("break", 16), ("B", 48), ("outro", 32)]
CH = [(29, [56, 60, 63, 67]),   # Fm9: Ab3 C4 Eb4 G4 over F
      (32, [55, 60, 63, 67]),   # Abmaj7: G3 C4 Eb4 G4 over Ab
      (27, [55, 58, 60, 63]),   # Eb6: G3 Bb3 C4 Eb4 over Eb
      (25, [53, 56, 60, 63])]   # Dbmaj7(9): F3 Ab3 C4 Eb4 over Db
ASC = [65, 67, 68, 70, 72, 73, 75, 77]          # F4 G4 Ab4 Bb4 C5 Db5 Eb5 F5 (F natural minor, THE STAIR F G Ab C inside)
DESC = list(reversed(ASC))
TRACKS = ("kick", "hats", "clap", "sub", "bass", "organ", "earL", "earR", "pad", "dot")


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

    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            r, v = CH[b % 4]
            ku = KEYUP if (sec == "B" and b >= 24) else 0
            r, v = r + ku, [n + ku for n in v]
            seam_in = sec == "intro" and b < 16
            seam_out = sec == "outro" and b >= 16
            solo = SOLO and sec == "B" and b in (22, 23)
            if solo:
                for k, q in enumerate(range(0, 16, 2)):
                    i = k % 8
                    lo, hi = ASC[i], DESC[i]
                    left, right = (lo, hi) if i % 2 == 0 else (hi, lo)
                    add("earL", at + q, nm(left), 2, 90)
                    add("earR", at + q, nm(right), 2, 90)
                continue
            if sec != "break":
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, 118 if q == 0 else 110)
            # the shuffled hats: 16ths with accents, open on the off-beats in the grooves
            if not (sec == "break" and b < 12):
                for q in range(16):
                    if q % 4 == 2:
                        add("hats", at + q, "oh" if sec in ("A", "B") else "h", 1, 78)
                    elif not seam_in and not seam_out:
                        add("hats", at + q, "h", 1, 60 if q % 2 else 44)
                    elif q % 2 == 0:
                        add("hats", at + q, "h", 1, 48)
            # claps on 2 and 4; a rim roll at every eighth bar's end
            if sec in ("A", "B") or (sec == "outro" and b < 16):
                add("clap", at + 4, "cp", 1, 96)
                add("clap", at + 12, "cp", 1, 100)
                if b % 8 == 7:
                    for q in (13, 14, 15):
                        add("clap", at + q, "rs", 1, 70 + 8 * (q - 13))
            if DOT and sec in DOT.split(","):
                for q in range(16):
                    k = at + q - a0
                    if k % 3 == 0:
                        add("dot", at + q, "rs" if (k // 3) % 2 == 0 else "sh", 1, 80 if (k // 3) % 4 == 0 else 66)
            # the sub: a held F under the seam in, the roots in the grooves, a held C2 under the seam out
            if seam_in:
                if b % 4 == 0:
                    add("sub", at, "F1", 4 * BAR, 86)
            elif seam_out:
                if b % 4 == 0:
                    add("sub", at, "C2", 4 * BAR, 86)
            elif sec != "break":
                add("sub", at, nm(r), 7, 92)
                add("sub", at + 10, nm(r), 5, 84)
            # the pumping bassline: off-beat octaves (jackin')
            if sec in ("A", "B") or (sec == "outro" and b < 16):
                for q in (2, 6, 10, 14):
                    add("bass", at + q, nm(r + 24 if q in (6, 14) else r + 12), 2, 96 if q in (2, 10) else 86)
            # the organ: short stabs on the and-of-1 and the a-of-2 (B2 answers on the 3 and the a-of-4)
            if (sec == "A" and b < 16) or sec == "B" or (sec == "intro" and b >= 16):
                ch = ",".join(nm(n + 12) for n in v)
                hits = ((3, 11) if ANTIC else (2, 7)) if not (sec == "B" and b >= 24) else ((3, 8, 11, 15) if ANTIC else (2, 7, 8, 15))
                for q in hits:
                    add("organ", at + q, ch, 1, 86 if q in (2, 3) else 74)
            # THE SCALE ILLUSION: the rising and the falling scale at once, swapping ears on every step
            on = (sec == "A" and b >= 16) or sec in ("break", "B")
            if on:
                step16 = 1 if (sec == "B" and b >= 24) else 2
                vel = 70 if (sec == "A") else (84 if sec in ("break", "B") else 64 - 2 * b)
                for k, q in enumerate(range(0, 16, step16)):
                    i = k % 8
                    lo, hi = ASC[i] + ku, DESC[i] + ku
                    left, right = (lo, hi) if i % 2 == 0 else (hi, lo)
                    add("earL", at + q, nm(left), step16, vel)
                    add("earR", at + q, nm(right), step16, vel)
            if sec == "break" and b % 4 == 0:
                add("pad", at, ",".join(nm(n) for n in v), 4 * BAR, 70)
    return {k: stream(ev[k], total_steps()) for k in TRACKS}


def lane(points, step=True):
    spb = 60 / BPM
    pts = [["0s", points[0][1]]]
    prev = points[0][1]
    for t16, val in points[1:]:
        t = t16 * S * spb
        if step:
            pts.append([f"{max(0.0, t - 0.01):.3f}s", prev])
        pts.append([f"{t:.3f}s", val])
        prev = val
    pts.append([f"{total_steps() * S * spb + 10:.2f}s", pts[-1][1]])
    return {"points": pts}


def song():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    pump = {"type": "pump", "on": "kick.k", "depth": "-6dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    sin, sout = ((int(float(x)) if float(x) == int(float(x)) else float(x)) for x in SEAMLV.split(","))
    dyn = lane([(0, sin), (st["intro"] + 16 * BAR, -1), (st["A"], 0), (st["A"] + 16 * BAR, 0.5), (st["break"], -6), (st["B"], 0.5),
                (st["B"] + 24 * BAR, 1), (st["outro"], -1), (st["outro"] + 16 * BAR, sout)])
    doc = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 14 by chirper-zero: RESTRAINED JACKIN' HOUSE, both ears. The scale "
                 "illusion: a rising and a falling scale swapping ears on every step - two melodies nobody plays. Generated by "
                 "compose/chirpers7/src/chirpers7-t14.py; see its docstring and compose/chirpers7/styles.md.",
        "tempo": BPM, "ceiling": "-1dB", "loudness": -11, "tail": "0.3s",
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=50 q=1 gain=-5dB", "lowshelf cutoff=70 gain=-9dB", "peak cutoff=320 q=0.8 gain=-3dB",
                                                   "peak cutoff=3000 q=0.8 gain=4dB", *(["peak cutoff=3500 q=1 gain=3dB"] if PRES else []), "highshelf cutoff=4000 gain=7dB", "highshelf cutoff=9000 gain=4dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "compressor", "threshold": f"{FCOMP.split(',')[0]}dB", "ratio": 8, "attack": FCOMP.split(',')[1], "release": "60ms", "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": dyn}},
        "buses": {
            "room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=8ms", "hp cutoff=250"]},
            "hall": {"fx": ["reverb kind=hall decay=3s mix=1 predelay=25ms", "lp cutoff=7000"]},
        },
        "tracks": [
            {"name": "kick", "patch": "machine-kit", "gain": "-3dB", "score": T["kick"]},
            {"name": "hats", "patch": "machine-kit", "gain": "-3dB", "pan": 0.1, "lfo": {"hh": "sine rate=5/1"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": {"value": 3500, "mod": [{"src": "lfo.hh", "amount": 0.5}]}, "q": 0.7}],
             "score": "swing16=0.6 " + T["hats"]},
            {"name": "clap", "patch": "machine-kit", "gain": "-5dB" if PRES else "-8dB", "sends": {"room": "-6dB"}, "score": "swing16=0.6 " + T["clap"]},
            *([{"name": "dot", "patch": "machine-kit", "gain": "-10dB", "pan": -0.3, "sends": {"room": "-10dB"}, "score": T["dot"]}] if DOT else []),
            {"name": "sub", "patch": "sub", "gain": "-16dB", "fx": [pump, {"type": "phantom", "cutoff": 100, "harmonics": "-6dB"}], "score": T["sub"]},
            {"name": "bass", "patch": "bass", "gain": "-14dB", "fx": [pump, {"type": "filter", "kind": "lp", "cutoff": 900, "q": 1.2}], "score": T["bass"]},
            {"name": "organ", "patch": "organ", "gain": "-12dB", "pan": -0.15, "fx": [pump], "sends": {"room": "-8dB"}, "score": "swing16=0.6 " + T["organ"]},
            {"name": "earL", "patch": "blip", "gain": "-12dB", "pan": -1, "sends": {"hall": "-14dB"}, "score": T["earL"]},
            {"name": "earR", "patch": "blip", "gain": "-12dB", "pan": 1, "sends": {"hall": "-14dB"}, "score": T["earR"]},
            {"name": "pad", "patch": "pad-glass", "gain": "-14dB", "sends": {"hall": "-6dB"}, "score": T["pad"]},
        ],
    }
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "loudness", "tail", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
