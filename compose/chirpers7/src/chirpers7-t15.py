#!/usr/bin/env python3
"""chirpers7-t15 (The Endless Stair, track 15) - generator for songs/chirpers7-t15.yaml (chirper-zero).

DUB HOUSE / "slower forever". 124 -> 123 bpm (the ramp in the last 32 bars: the comedown's first -1), C minor (5A).
The comedown felt before it happens: a percussion pattern played as a RISSET DECELERANDO - three tempo octaves of the same
rims, clave and shaker, each halving its tempo over eight bars while the slowest fades out and the fastest fades in - so
the groove seems to sink for minutes while the kick never changes; when the bpm really drops at the end, it feels like
arriving. Minor-ninth stabs are thrown into a dub delay whose feedback rises and falls; a round sub; THE STAIR falls
(G Eb D C) as the stabs' top line and rises again (C D Eb G) only in the outro, handing t16 its G. Original; a style,
not a version of any track.

Form (4/4 bars): INTRO 32 (bars 1-16 the seam from t14: kick, hats, a held C; then rims and the first stabs) / A 32
(the groove: stabs, sub line, clap) / BREAK 32 (the kick out: the Risset alone under a glass pad, the dub's feedback
climbing) / B 48 (the full groove with the Risset sinking under it) / R2 16 (a second, faster-cycling Risset, the stabs
filtered down) / OUTRO 32 (the stair rises; the last 16 bars the seam into t16: kick, hats, the sub on G; 124 -> 123).

Motifs (compose/chirpers7/motifs.md):
  THE CHANGES  Cm9 | Abmaj7 | Gsus(b9) | Fm9, one a bar; the stabs' tops fall G Eb D C (THE STAIR, falling).
  THE SINKING  the Risset decelerando: rims 0 3 6 | 8 11 14, a clave on 10, shakers on the off-16ths.
Run: python3 compose/chirpers7/src/chirpers7-t15.py  (writes songs/chirpers7-t15.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C7T15_OUT") or os.path.join(ROOT, "songs", "chirpers7-t15.yaml")
BPM0, BPM1 = 124, 123
S = 0.25
BAR = 16
MGAIN = float(os.environ.get("C7T15_MGAIN", "8"))
CLIP = os.environ.get("C7T15_CLIP", "")
KCLIP = os.environ.get("C7T15_KCLIP", "")  # the kick's own soft clip (dB): its click transient shaved so the master's limiter has nothing to hold
KGAIN = os.environ.get("C7T15_KGAIN", "-3")
LOUD = float(os.environ.get("C7T15_LOUD", "-11"))
FCOMP = os.environ.get("C7T15_FCOMP", "-15,0.3ms")
STEP = os.environ.get("C7T15_STEP", "1") == "1"  # section lanes step at their boundaries (v1's ramped across sections: A faded down into the break, B swelled)
LOWS = os.environ.get("C7T15_LOWS", "-8,-12")
TAILS = os.environ.get("C7T15_TAIL", "0.3s")  # the render tail: 0.3 s leaves no dead air before t16 picks up the held G  # "shelf,sub": the master's 70 Hz shelf and the sub's gain (dB)  # the fast master compressor's threshold (dB) and attack, 8:1: it catches the kick's peaks before the loudness stage's limiter  # a soft clip ends the master (dB): the kick's peaks rounded before the loudness stage's true-peak limiter, which then has almost nothing to hold

RAMP16 = os.environ.get("C7T15_RAMP16", "1") == "1"  # the tempo ramp finishes 16 bars before the end, so the DJ-mix overlap runs at one steady tempo on both sides (no drift under the crossfade)

SWAP = os.environ.get("C7T15_SWAP", "0") == "1"
SWAPBARS = int(os.environ.get("C7T15_SWAPBARS", "16"))  # how many overlap bars the incoming lows wait (16: until the overlap ends; 8: the crossfade's midpoint, where the linear fade has both sides at half)  # a DJ's bass swap at the seam in: for the 16 overlap bars the kick is high-passed at 110 Hz (its own track) and the held sub is out - the outgoing track carries the low end; the full kick and sub land at bar 17

EQ6 = os.environ.get("C7T15_EQ6", "b")  # "a": 45 Hz -5 dB (37-60 Hz read 6-9 dB over the album); "b": also 3.8 kHz +4 dB (3-5 kHz read 6-8 dB under)
BED = os.environ.get("C7T15_BED", "2")  # Harry 14:50, 'most tracks have no illusion': the Risset decelerando leads. "1": the bed also under intro bars 17-32, all of A and the outro's first 16 (never more than one break without it); "2": as 1, and under B's last 16 bars an ACCELERATING bed (panned the other way) runs against the slowing one - poly accel/decel over a kick that never changes
BEDG = os.environ.get("C7T15_BEDG", "-9")  # the beds' level (was -9 dB: compscore's illusion survey read them 11 LU under the mix)
BEDLV = os.environ.get("C7T15_BEDLV", "-8,-6,2,-3,-3,-1,-6")  # per-bed levels (dB): intro,A,break,B,rise,r2,outro - the bed swells and recedes with the form
KEYUP = int(os.environ.get("C7T15_KEYUP", "3"))  # B's last 16 bars lift KEYUP semitones (the dub's last high before the comedown); r2 and the outro walk home to C minor
ALONE = os.environ.get("C7T15_ALONE", "1") == "1"  # chirper-one's note: break bar 30, the deepest point, the decelerating bed alone (no hats, the pad cut, the kick still out) - then the kick comes back

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 32), ("A", 32), ("break", 32), ("B", 48), ("r2", 16), ("outro", 32)]
# (sub root, stab voicing with its top note last): the tops fall G Eb D C
CH = [(36, [58, 62, 63, 67]),   # Cm9: Bb3 D4 Eb4 G4
      (32, [55, 56, 60, 63]),   # Abmaj7: G3 Ab3 C4 Eb4
      (31, [53, 56, 60, 62]),   # Gsus(b9): F3 Ab3 C4 D4
      (29, [51, 55, 56, 60])]   # Fm9: Eb3 G3 Ab3 C4
TRACKS = ("kick", "hats", "clap", "sub", "stab", "pad", "rims", "stair", "kickin")


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
            ku = KEYUP if (sec == "B" and b >= 32) else 0
            r, v = r + ku, [n + ku for n in v]
            seam_in = sec == "intro" and b < 16
            seam_out = sec == "outro" and b >= 16
            # --- kick: four on the floor, everywhere but the break
            if sec != "break" or b >= nb - 2:
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "kr" if sec in ("intro", "outro") else ("kd" if (sec == "B" and b >= 24) else "k"), 1, 118 if q == 0 else 112)
            # --- hats: off-beats; open hats in the grooves
            if not (sec == "break" and b < 24) and not (ALONE and sec == "break" and b == 29):
                for q in (2, 6, 10, 14):
                    add("hats", at + q, "oh" if (sec in ("A", "B") and q == 14 and b % 2 == 1) else "h", 1, 70 if q % 4 == 2 else 60)
            if sec in ("A", "B", "r2"):
                for q in (1, 3, 5, 7, 9, 11, 13, 15):
                    add("hats", at + q, "h", 1, 44 + (8 if q in (3, 11) else 0))
            # --- clap on 2 and 4 in the grooves
            if sec in ("A", "B") or (sec == "r2" and b % 2 == 1):
                add("clap", at + 4, "cp", 1, 96)
                add("clap", at + 12, "cp", 1, 100)
            # --- sub: a held C under the seam in, the bassline in the grooves, G under the seam out
            if seam_in:
                if b % 4 == 0:
                    add("sub", at, "C2", 4 * BAR, 92)
            elif seam_out:
                if b % 4 == 0:
                    add("sub", at, "G1", 4 * BAR, 92)
            elif sec in ("A", "B", "r2") or (sec == "intro" and b >= 16) or (sec == "outro" and b < 16):
                add("sub", at, nm(r), 6, 100)
                add("sub", at + 7, nm(r), 3, 84)
                add("sub", at + 10, nm(r + 12 if b % 2 else r), 4, 90)
            # --- the dub stabs: off-beat minor ninths; every fourth bar only one; the break leaves them to the delay
            if (sec in ("A", "B", "r2")) or (sec == "intro" and b >= 24) or (sec == "outro" and b < 16) or (sec == "break" and b % 4 == 0):
                ch = ",".join(nm(n) for n in v)
                if b % 4 == 3 or sec == "break" or sec == "intro":
                    hits = (2,)
                elif sec == "A" and b >= 16:  # A2: the stabs answer themselves
                    hits = (2, 7, 10, 15)
                elif sec == "B":
                    hits = (2, 7, 10)
                else:
                    hits = (2, 10)
                for q in hits:
                    add("stab", at + q, ch, 1, 100 if q == 2 else 88)
            # --- A2: rims on the off-16ths; B2: THE STAIR falling on the glass (G Eb D C), a beat a note
            if sec == "A" and b >= 16:
                for q in (3, 11):
                    add("hats", at + q, "rs", 1, 74)
            if sec == "B" and b >= 24 and b % 2 == 0:
                for k, n in enumerate((67, 63, 62, 60)):
                    add("stair", at + 4 * k, nm(n + 12 + ku), 3, 84 - 2 * k)
            # --- THE STAIR rising in the outro (C D Eb G), handing t16 its G
            if sec == "outro" and 8 <= b < 16 and b % 2 == 0:
                for k, n in enumerate((60, 62, 63, 67)):
                    add("stair", at + 4 * k, nm(n + 12), 3, 86 - 2 * k)
            # --- the glass pad under the break
            if sec == "break" and b % 4 == 0:
                add("pad", at, ",".join(nm(n) for n in v), (BAR if (ALONE and b == 28) else 4 * BAR), 80)
    if SWAP:
        ev["kickin"] = [e for e in ev["kick"] if e[0] < SWAPBARS * BAR]
        ev["kick"] = [e for e in ev["kick"] if e[0] >= SWAPBARS * BAR]
        held = [e for e in ev["sub"] if e[0] < SWAPBARS * BAR < e[0] + e[2]]  # a held note crossing the swap re-enters at the swap point
        ev["sub"] = [e for e in ev["sub"] if e[0] >= SWAPBARS * BAR] + [(SWAPBARS * BAR, h, e0 + ln - SWAPBARS * BAR, v) for (e0, h, ln, v) in held]
    return {k: stream(ev[k], total_steps()) for k in TRACKS}


RISSET_PAT = "rs/0.75b@96 rs/0.75b@84 rs/0.5b@90 rs/0.75b@96 cb/0.75b@80 rs/0.5b@88"  # one bar: rims 0 3 6 | 8 11 14 with a clave on 11


def lane(points, step=None):
    step = STEP if step is None else step
    spb = 60 / BPM0
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
    beats = lambda t16: f"{t16 // 4}b"  # noqa: E731
    total_b = total_steps() // 4
    tempo = [{"at": "0b", "bpm": BPM0}, {"at": beats(st["outro"]), "bpm": BPM0}, {"at": f"{total_b - 64 if RAMP16 else total_b}b", "bpm": BPM1, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "2ms", "release": "200ms", "curve": 0.7}
    pumpr = {"type": "pump", "on": "kick.kr", "depth": "-5dB", "attack": "2ms", "release": "200ms", "curve": 0.7}
    # the dub's feedback: settled in the grooves, climbing through the break, falling into B
    fb = lane([(0, 0), (st["break"], 0), (st["break"] + 28 * BAR, 0.3), (st["B"], 0.05), (st["r2"], 0.15), (st["outro"], 0)], step=False)
    blv = dict(zip(("intro", "A", "break", "B", "rise", "r2", "outro"), BEDLV.split(","))) if BEDLV else {}
    def bedg(at, nm):
        if not blv:
            return BEDG
        if nm == "rise":
            return blv["rise"]
        for sec in ("outro", "r2", "B", "break", "A", "intro"):
            if at >= st[sec]:
                return blv[sec]
        return BEDG
    risset = lambda at, nbars, cycle, down=True, pan=0.25, nm="sink": {  # noqa: E731
        "name": f"{nm}{at}", "patch": "machine-kit", "gain": f"{bedg(at, nm)}dB", "pan": pan, "at": beats(at),
        "risset": {"cycle": f"{cycle}bar", "down": down, "layers": 3, "length": f"{nbars}bar"},
        "sends": {"dub": "-14dB", "room": "-8dB"}, "score": RISSET_PAT}
    extra = []
    if BED:
        extra += [risset(st["intro"] + 16 * BAR, 16, 8), risset(st["A"], 32, 8), risset(st["outro"], 16, 8)]
    if BED == "2":
        extra += [risset(st["B"] + 32 * BAR, 16, 8, down=False, pan=-0.3, nm="rise")]
    doc = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 15 by chirper-zero: DUB HOUSE, slower forever. The Risset "
                 "decelerando: a percussion pattern slowing forever over a kick that never changes. Generated by "
                 "compose/chirpers7/src/chirpers7-t15.py; see its docstring and compose/chirpers7/styles.md.",
        "tempo": tempo, "ceiling": "-1dB", "loudness": LOUD, "tail": TAILS,
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", *(["peak cutoff=45 q=1 gain=-5dB"] if EQ6 else []), *(["peak cutoff=3800 q=1 gain=4dB"] if EQ6 == "b" else []), f"lowshelf cutoff=70 gain={LOWS.split(',')[0] if LOWS else -5}dB", "peak cutoff=320 q=0.8 gain=-4dB",
                                                   "highshelf cutoff=5000 gain=5dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "compressor", "threshold": f"{FCOMP.split(',')[0]}dB", "ratio": 8, "attack": FCOMP.split(',')[1], "release": "60ms", "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                          *([{"type": "clip", "ceiling": f"{CLIP}dB", "knee": 0.8, "link": True}] if CLIP else [])],
                   "auto": {"dyn": lane([(0, -4), (st["A"], 0), (st["break"], -8), (st["break"] + 30 * BAR, -4), (st["B"], 1),
                                         (st["r2"], -2), (st["outro"], -3)])}},
        "buses": {
            "dub": {"fx": [{"type": "delay", "time": "3/16", "feedback": {"value": 0.5, "mod": [{"src": "auto.fb", "amount": 1}]}, "mix": 1, "tone": 2400},
                           "hp cutoff=300", "reverb kind=hall decay=2.8s mix=0.35"],
                    "auto": {"fb": fb}},
            "room": {"fx": ["reverb kind=room decay=1.1s mix=1 predelay=10ms", "hp cutoff=250"]},
            "hall": {"fx": ["reverb kind=hall decay=5s size=1 mix=1 predelay=40ms", "lp cutoff=7000"]},
        },
        "tracks": [
            {"name": "kick", "patch": "machine-kit", "gain": f"{KGAIN}dB", **({"fx": [{"type": "clip", "ceiling": f"{KCLIP}dB", "knee": 0.7, "link": True}]} if KCLIP else {}),
             "score": T["kick"]},
            *([{"name": "kickin", "patch": "machine-kit", "gain": "-3dB", "fx": [{"type": "filter", "kind": "hp", "cutoff": 110, "q": 0.7}], "score": T["kickin"]}] if SWAP else []),
            {"name": "hats", "patch": "machine-kit", "gain": "-6dB", "pan": -0.1, "lfo": {"hh": "sine rate=7/1"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": {"value": 3000, "mod": [{"src": "lfo.hh", "amount": 0.6}]}, "q": 0.7}], "score": T["hats"]},
            {"name": "clap", "patch": "machine-kit", "gain": "-9dB", "sends": {"room": "-6dB"}, "score": T["clap"]},
            {"name": "sub", "patch": "sub", "gain": f"{LOWS.split(',')[1] if LOWS else -10}dB", "fx": [pump, pumpr, {"type": "phantom", "cutoff": 100, "harmonics": "-6dB"}], "score": T["sub"]},
            {"name": "stab", "patch": "house-chord", "gain": "-11dB", "lfo": {"st": "sine rate=7/1"},
             "fx": [pump, {"type": "filter", "kind": "lp", "cutoff": {"value": 2400, "mod": [{"src": "lfo.st", "amount": 1.0}]}, "q": 1.2}],
             "sends": {"dub": "-4dB"}, "score": T["stab"]},
            {"name": "stair", "patch": "pad-glass", "gain": "-12dB", "sends": {"dub": "-6dB", "hall": "-8dB"}, "score": T["stair"]},
            {"name": "pad", "patch": "pad-glass", "gain": "-14dB", "sends": {"hall": "-4dB"}, "score": T["pad"]},
            risset(st["break"], 32, 8),
            risset(st["B"], 48, 8),
            risset(st["r2"], 16, 4),
            *extra,
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
