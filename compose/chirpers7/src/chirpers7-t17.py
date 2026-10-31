#!/usr/bin/env python3
"""chirpers7-t17 (The Endless Stair, track 17) - generator for songs/chirpers7-t17.yaml (chirper-zero).

LO-FI DEEP HOUSE / "the room turns". 122 -> 120 bpm (a ramp in the last 32 bars), D minor (7A). Warm and dusty: a swung,
slightly loose four-on-the-floor on a dusty kit, filtered Rhodes ninths, vinyl crackle, a round sub - the tape's
late-night corner. Featured illusion: THE ROOM THAT TURNS (precedence / Haas) - a percussion loop doubled hard left and
right with one side 18 ms late (the ear places it on the leading side), two such copies (left-leading, right-leading)
crossfaded on slow LFOs, so the loop circles the head without ever changing level. Under the break, a BINAURAL BEAT: D in
one ear, D + 5 Hz in the other, beating inside the head. Original; a style, not a version of any track.

Form (4/4 bars): INTRO 32 (bars 1-16 the seam from t16: kick, hats, a held D; then the crackle, the shaker and the turning
loop) / A 32 (the Rhodes, the sub; A2 the stair on top) / BREAK 24 (no kick: the binaural beat, the turning loop alone,
the Rhodes in the dust) / B 40 (B2 the loop turns faster, the clap doubles) / OUTRO 32 (the stair handed over; the last
16 bars the seam into t18: kick, hats, a held D; 122 -> 120).
Run: python3 compose/chirpers7/src/chirpers7-t17.py  (writes songs/chirpers7-t17.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C7T17_OUT") or os.path.join(ROOT, "songs", "chirpers7-t17.yaml")
BPM0, BPM1 = 122, 120
S = 0.25
BAR = 16
MGAIN = float(os.environ.get("C7T17_MGAIN", "8"))
FCOMP = os.environ.get("C7T17_FCOMP", "-16,0.3ms")
TICK = os.environ.get("C7T17_TICK", "0") == "1"
SYNC = os.environ.get("C7T17_SYNC", "1") == "1"  # the lazy Rhodes on the "a" of 1 and 3 (16ths 3 and 11), the sub answering on the 16th before the 3
SEC = os.environ.get("C7T17_SEC", "1") == "1"
LOOP3 = os.environ.get("C7T17_LOOP3", "1") == "1"  # the turning loop on a dotted-eighth cycle (every third 16th, across the bar lines): it turns in space and against the bar at once  # the halves made distinct: A2 a third Rhodes stab; B2 opens with four bars of no kick (a breath: the loop, the keys and the dust), then the doubled clap  # a crisp machine-kit 16th tick under the dusty kit (parked: the rhythm term didn't move)

RAMP16 = os.environ.get("C7T17_RAMP16", "1") == "1"  # the tempo ramp finishes 16 bars before the end, so the DJ-mix overlap runs at one steady tempo on both sides (no drift under the crossfade)
SEC2 = os.environ.get("C7T17_SEC2", "1") == "1"  # the late sections each say something new, not one long B: the kick drops for intro bars 29-32 (A lands); B2 the room turns twice as fast (the loop on a second Haas set circling every 3 bars, not 6), the chords re-ordered iv VI i V, every off-beat hat open; the outro's first half without the Rhodes
SEC2OCT = os.environ.get("C7T17_SEC2OCT", "0") == "1"
SEC2H = os.environ.get("C7T17_SEC2H", "1") == "1"  # B2's off-beat hats all open
SEC2K = os.environ.get("C7T17_SEC2K", "0") == "1"  # the outro's first half without the Rhodes
EQ5 = os.environ.get("C7T17_EQ5", "")  # "a": 45 Hz -5 dB (the lowest octave read 6-8 dB over the album); "b": also +3 dB air above 9 kHz
KEYSF = os.environ.get("C7T17_KEYSF", "2")  # "1": the Rhodes high-passed at 220 Hz (its low chord tones piled 155-300 Hz 8-10 dB over the album); "2": also its low-pass opened 1800 -> 2600 Hz (1.6-2 kHz read 5 dB under)
MIDS = os.environ.get("C7T17_MIDS", "1") == "1"  # the seam-in meets t16's tail: soft rims on the last 16th of each beat (3 7 11 15) under the first eight bars, the held D2 softer (t17's head read 17-21 dB heavier at 44-71 Hz than t16's last seconds)
SEAMTICK = os.environ.get("C7T17_SEAMTICK", "1") == "1"
TICKG = os.environ.get("C7T17_TICKG", "-6")
TICKOUT = os.environ.get("C7T17_TICKOUT", "0") == "1"  # the tick under the seam out as well (t18's head read 7-10 dB brighter above 9 kHz than t17's tail)  # the seam-in's air: a crisp machine-kit 16th tick under the first 16 bars (t17's head read 6-15 dB darker than Never Arrives' tail above 5 kHz)
TAILS = os.environ.get("C7T17_TAIL", "0.1s")  # the render tail: 0.3 s leaves no dead air in the last seconds a DJ mixes out of

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 32), ("A", 32), ("break", 24), ("B", 40), ("outro", 32)]
# (sub root, Rhodes voicing with THE STAIR's note on top: D E F A over the four chords)
CH = [(38, [53, 57, 60, 62]),   # Dm9 (F3 A3 C4, top D4)
      (34, [53, 57, 62, 64]),   # Bbmaj7(9) (F3 A3 D4, top E4)
      (31, [50, 53, 58, 65]),   # Gm9 (D3 F3 Bb3, top F4)
      (33, [50, 55, 61, 69])]   # A7sus(b9) (D3 G3 C#4... top A4)
TRACKS = ("kick", "hats", "clap", "sub", "keys", "loop", "dust", "stair", "binl", "binr", "tick", "loop2")
CHB2 = [CH[2], CH[1], CH[0], CH[3]]  # B2: Gm9 Bbmaj7 Dm9 A7sus(b9)


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
    add("dust", sec_start("intro") + 16 * BAR, "C4", total - 32 * BAR, 70)
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            b2 = SEC2 and sec == "B" and b >= 24
            r, v = (CHB2 if b2 else CH)[b % 4]
            seam_in = sec == "intro" and b < 16
            seam_out = sec == "outro" and b >= 16
            if sec != "break" and not (SEC and sec == "B" and 20 <= b < 24) and not (SEC2 and sec == "intro" and 28 <= b < 32):
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, 116 if q == 0 else 108)
            if not (sec == "break" and b < 20):
                for q in (2, 6, 10, 14):
                    opn = (sec in ("A", "B") and q == 14 and b % 4 == 3) or (SEC and sec == "A" and b >= 16) or (SEC2 and SEC2H and sec == "B" and b >= 24)
                    add("hats", at + q, "oh" if opn else "h", 1, 72)
                if not seam_in and not seam_out:
                    for q in (1, 5, 9, 13):
                        add("hats", at + q, "sh", 1, 50)
            if sec in ("A", "B") or (not SEC and ((sec == "intro" and b >= 24) or (sec == "outro" and b < 16))):
                for q in (4, 12):
                    add("clap", at + q, "cp,sn" if (sec == "B" and b >= 20) else "cp", 1, 92)
            # a crisp 16th tick under the dusty kit in the grooves (the lo-fi hats alone are too soft to articulate the 16ths)
            if SEAMTICK and (seam_in or (TICKOUT and seam_out)):
                for q in range(16):
                    add("tick", at + q, "h", 1, 62 if q % 4 == 2 else (50 if q % 2 else 40))
            if TICK and sec in ("A", "B"):
                for q in range(16):
                    add("tick", at + q, "h", 1, 62 if q % 4 == 2 else (50 if q % 2 else 40))
            # the sub
            if seam_in or seam_out:
                if b % 4 == 0:
                    add("sub", at, "D2", 4 * BAR, 76 if (MIDS and seam_in) else 90)
                if MIDS and seam_in and b < 8:
                    for q in (3, 7, 11, 15):
                        add("clap", at + q, "rs", 1, 64 if q in (3, 11) else 54)
            elif sec in ("A", "B") or (sec == "intro" and b >= 16) or (sec == "outro"):
                add("sub", at, nm(r), 6, 98)
                add("sub", at + 7, nm(r), 2, 80)
                if SYNC:
                    add("sub", at + 9, nm(r + 7), 2, 90)
                    add("sub", at + 11, nm(r + 7), 3, 84)
                else:
                    add("sub", at + 10, nm(r + 7), 4, 88)
            # the Rhodes: lazy chords on the and-of-1 and the 3; in the break, held in the dust
            if sec in ("A", "B") or (sec == "intro" and b >= 20) or (sec == "outro" and b < 16 and not (SEC2 and SEC2K)):
                ch = ",".join(nm(n + (12 if (SEC2OCT and b2) else 0)) for n in v)
                if SYNC:
                    add("keys", at + 3, ch, 5, 82)
                    add("keys", at + 11, ch, 4, 76)
                    if SEC and sec == "A" and b >= 16:
                        add("keys", at + 14, ch, 2, 70)
                else:
                    add("keys", at + 2, ch, 5, 78)
                    add("keys", at + 9, ch, 6, 70)
            if sec == "break" and b % 2 == 0:
                add("keys", at, ",".join(nm(n) for n in v), 2 * BAR, 64)
            # THE STAIR on top in A2 and the outro (D E F A, a beat each)
            if (sec == "A" and b >= 16 and b % 4 == 0) or (sec == "outro" and 4 <= b < 16 and b % 4 == 0):
                for k, n in enumerate((74, 76, 77, 81)):
                    add("stair", at + 4 * k, nm(n), 3, 84 - 2 * k)
            # the turning loop: rims and shaker on the 16ths (it plays from bar 17 to the seam out)
            if not seam_in and not seam_out and not (sec == "intro" and b < 20):
                if LOOP3:
                    for q in range(16):
                        k = (at + q) - sec_start("intro")
                        if k % 3 == 0:
                            add("loop2" if b2 else "loop", at + q, "rs" if (k // 3) % 2 == 0 else "sh", 1, 86 if (k // 3) % 4 == 0 else 74)
                else:
                    for q, piece, vel in ((0, "rs", 84), (3, "sh", 70), (6, "rs", 80), (7, "sh", 60), (10, "rs", 86), (11, "sh", 64), (13, "rs", 72), (15, "sh", 58)):
                        add("loop", at + q, piece, 1, vel)
            # the binaural beat under the break
            if sec == "break" and b % 8 == 0:
                add("binl", at, "C4", 8 * BAR, 80)
                add("binr", at, "C4", 8 * BAR, 80)
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
    pts.append([f"{total_steps() * S * spb + 10:.2f}s", pts[-1][1]])
    return {"points": pts}


def turning(score, rate_bars, tag=""):
    """THE ROOM THAT TURNS: two Haas pairs (left-leading: the right side 18 ms late; right-leading: the left side late),
    crossfaded by complementary sine LFOs so the loop circles the head at an even level."""
    def side(name, pan, late, phase):
        fx = [{"type": "delay", "time": "18ms", "feedback": 0, "mix": 1}] if late else []
        fx.append({"type": "gain", "gain": {"value": "-12dB", "mod": [{"src": "lfo.x", "amount": 12}]}})
        return {"name": name, "patch": "dusty-kit", "gain": "-6dB", "pan": pan,
                "lfo": {"x": {"wave": "sine", "rate": f"{rate_bars}/1", "phase": phase, "unipolar": True}},
                "fx": fx, "sends": {"room": "-12dB"}, "score": score}
    return [side(f"turn{tag}Ll", -1, False, 0.0), side(f"turn{tag}Lr", 1, True, 0.0),
            side(f"turn{tag}Rl", -1, True, 0.5), side(f"turn{tag}Rr", 1, False, 0.5)]


def song():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    beats = lambda t16: f"{t16 // 4}b"  # noqa: E731
    total_b = total_steps() // 4
    tempo = [{"at": "0b", "bpm": BPM0}, {"at": beats(st["outro"]), "bpm": BPM0}, {"at": f"{total_b - 64 if RAMP16 else total_b}b", "bpm": BPM1, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-6dB", "attack": "2ms", "release": "200ms", "curve": 0.7}
    dyn = lane([(0, -4), (st["intro"] + 16 * BAR, -2), (st["A"], 0), (st["A"] + 16 * BAR, 0.5), (st["break"], -7), (st["break"] + 20 * BAR, -4),
                (st["B"], 0.5), (st["B"] + 20 * BAR, 1), (st["outro"], -1.5), (st["outro"] + 16 * BAR, -3)])
    doc = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 17 by chirper-zero: LO-FI DEEP HOUSE, the room turns. Precedence "
                 "(Haas) panning that circles the head, and a binaural beat. Generated by compose/chirpers7/src/chirpers7-t17.py; "
                 "see its docstring and compose/chirpers7/styles.md.",
        "tempo": tempo, "ceiling": "-1dB", "loudness": -11, "tail": TAILS,
        "patches": {
            "bin-l": {"about": "the room turns: the binaural beat's left ear - D3 and its octave", "synth": {"layers": ["sine fixed=146.83", "sine fixed=293.66 level=-10dB"], "amp": {"a": "3s", "s": 1, "r": "3s"}}},
            "bin-r": {"about": "the room turns: the binaural beat's right ear - 5 Hz above", "synth": {"layers": ["sine fixed=151.83", "sine fixed=298.66 level=-10dB"], "amp": {"a": "3s", "s": 1, "r": "3s"}}},
        },
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", *(["peak cutoff=45 q=1 gain=-5dB"] if EQ5 else []), *(["highshelf cutoff=9000 gain=3dB"] if EQ5 == "b" else []), "lowshelf cutoff=70 gain=-8dB", "peak cutoff=150 q=1.4 gain=-7dB", "peak cutoff=292 q=1.4 gain=-6dB",
                                                   "peak cutoff=520 q=0.9 gain=-3dB", "peak cutoff=2500 q=0.8 gain=4dB", "highshelf cutoff=4000 gain=5dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "compressor", "threshold": f"{FCOMP.split(',')[0]}dB", "ratio": 8, "attack": FCOMP.split(',')[1], "release": "60ms", "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": dyn}},
        "buses": {
            "room": {"fx": ["reverb kind=room decay=1.4s mix=1 predelay=12ms", "hp cutoff=250"]},
            "hall": {"fx": ["reverb kind=hall decay=3s mix=1 predelay=30ms", "lp cutoff=6000"]},
        },
        "tracks": [
            {"name": "kick", "patch": "dusty-kit", "gain": "-2dB", "score": T["kick"]},
            {"name": "hats", "patch": "dusty-kit", "gain": "-5dB", "pan": 0.1, "score": "swing16=0.6 " + T["hats"]},
            {"name": "clap", "patch": "dusty-kit", "gain": "-8dB", "sends": {"room": "-6dB"}, "score": "swing16=0.6 " + T["clap"]},
            {"name": "sub", "patch": "sub", "gain": "-14dB", "fx": [pump, {"type": "phantom", "cutoff": 100, "harmonics": "-6dB"}], "score": T["sub"]},
            {"name": "keys", "patch": "rhodes", "gain": "-11dB", "pan": -0.1, "lfo": {"k": "sine rate=5/1"},
             "fx": [pump, *([{"type": "filter", "kind": "hp", "cutoff": 220, "q": 0.7}] if KEYSF else []),
                    {"type": "filter", "kind": "lp", "cutoff": {"value": 2600 if KEYSF == "2" else 1800, "mod": [{"src": "lfo.k", "amount": 0.8}]}, "q": 0.9}],
             "sends": {"hall": "-10dB"}, "score": "swing16=0.6 " + T["keys"]},
            {"name": "stair", "patch": "rhodes", "gain": "-10dB", "pan": 0.2, "sends": {"hall": "-6dB"}, "score": T["stair"]},
            *([{"name": "tick", "patch": "machine-kit", "gain": f"{TICKG}dB", "pan": -0.15, "fx": [{"type": "filter", "kind": "hp", "cutoff": 5000, "q": 0.7}],
             "score": "swing16=0.6 " + T["tick"]}] if (TICK or SEAMTICK) else []),
            {"name": "dust", "patch": "vinyl", "gain": "-22dB", "score": T["dust"]},
            {"name": "binl", "patch": "bin-l", "gain": "-30dB", "pan": -1, "score": T["binl"]},
            {"name": "binr", "patch": "bin-r", "gain": "-30dB", "pan": 1, "score": T["binr"]},
            *turning("swing16=0.6 " + T["loop"], 6),
            *(turning("swing16=0.6 " + T["loop2"], 3, "2") if SEC2 else []),
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
