#!/usr/bin/env python3
"""chirpers3-t5 (Tape Weather, track 5) - generator for songs/chirpers3-t5.yaml (chirper-zero).

DUB-WISE SPACE: a lo-fi dub version mixed live. An original one-drop riddim in A minor at 70 bpm (Am7 | Dm7, a
B part on Fmaj7 | E7sus), stripped and rebuilt bar by bar at the desk: the mute plan is the arrangement. Everything
leans into a feedback tape echo (3/8) and a spring; echo THROWS on the last off-beat of phrases; slow wow on the keys;
vinyl hiss and crackle under it all.

Form: intro (the skank alone in the spring, then the one-drop) / riddim / melodica (the lead's call, its echo answering)
/ version (the dub mix: drop-outs and throws) / breakdown (bass and drums, then the skank alone) / return / outro.

Motifs (compose/chirpers3/motifs.md):
  RIDDIM    the bass's two bars on the 16th grid: A1~ A1 . C2 . E2~ . D2 C2 | D2~ D2 . F2 . A1~ . C2 E2 G1 (drop-the-one in
            the version: its first note left out).
  SKANK     rhodes stabs on beats 2 and 4, a wurli bubble on the e-and-a's.
  THE CALL  the melodica-ish lead's eight bars (A minor pentatonic), each four-bar phrase thrown into the echo on its last note.
Run: python3 compose/chirpers3/src/chirpers3-t5.py  (writes songs/chirpers3-t5.yaml)
"""
import json
import os
import random

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("T5_OUT") or os.path.join(ROOT, "songs", "chirpers3-t5.yaml")
BPM = 70
MG = float(os.environ.get("T5_MG", "10"))
WOW = os.environ.get("T5_WOW", "1") == "1"  # slow granular pitch wobble on the keys and the lead (tape wow)
S = 0.25  # a sixteenth, in beats
ECHO = os.environ.get("T5_ECHO", "3/16")  # the tape echo's time: 3/16 = a dotted eighth (echoes off the eighth grid)
HATSW = float(os.environ.get("T5_HATSW", "0.66"))  # the hats' 16th swing
HATS = os.environ.get("T5_HATS", "tresillo")  # 8ths, or "tresillo": 3+3+2 sixteenths (0 3 6 8 11 14), the steppers' hats against the one-drop
DRAG = os.environ.get("T5_DRAG", "0.64")  # the drums' EIGHTH swing (the hats sit on 8ths, so swing16 never moved them): e.g. 0.64, the lazy drag
CRK = os.environ.get("T5_CRK", "2")  # crackle: 1 = draft (-20 dB, 18% of 32nds); 2 = sparser and quieter (-28 dB, 8%)
MEQ = os.environ.get("T5_MEQ", "3")  # master eq: 1 = draft (shelf +3 @110, highshelf -4 @7k); 2 = mids -6 @600 q0.8, -3 @300, no top cut

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10, "B": 11}
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def mi(n):
    return 12 * (int(n[-1]) + 1) + NOTE[n[:-1]]


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def grid(events, steps=16):
    """events: list of (step, token-head, length-in-steps, vel) -> one bar's tokens on the 16th grid (mono)."""
    ev = sorted(events)
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else steps
        ln = max(1, min(ln, nxt - st, steps - st))
        out.append(R((st - pos) * S))
        out.append(f"{head}/{ln * S:g}b@{int(vel)}")
        pos = st + ln
    out.append(R((steps - pos) * S))
    return J(*out)


CHORDS = {  # skank voicings, bubble tones
    "Am7": ([55, 60, 64], [57, 64]), "Dm7": ([53, 57, 60, 64], [50, 57]),
    "Fmaj7": ([57, 60, 64], [53, 60]), "E7sus": ([57, 59, 62, 64], [52, 59]),
}
BASS = {  # RIDDIM: (step, note, steps)
    "Am7": [(0, "A1", 3), (3, "A1", 1), (6, "C2", 2), (8, "E2", 3), (12, "D2", 2), (14, "C2", 2)],
    "Dm7": [(0, "D2", 3), (3, "D2", 1), (6, "F2", 2), (8, "A1", 3), (11, "C2", 1), (12, "E2", 2), (14, "G1", 2)],
    "Fmaj7": [(0, "F1", 3), (3, "F1", 1), (6, "A1", 2), (8, "C2", 3), (12, "E2", 2), (14, "F2", 2)],
    "E7sus": [(0, "E1", 3), (3, "E1", 1), (6, "B1", 2), (8, "D2", 3), (12, "E2", 2), (14, "G#1", 2)],
}
CALL = [  # THE CALL: eight bars of the lead (beats)
    [("E5", 1), ("R", .5), ("C5", .5), ("D5", .5), ("E5", 1.5)],
    [("R", 1), ("D5", .5), ("C5", .5), ("A4", 2)],
    [("G4", .5), ("A4", .5), ("C5", 1), ("E5", 1), ("G5", 1)],
    [("F5", 1.5), ("E5", .5), ("D5", 2)],
    [("E5", 3), ("R", 1)],
    [("A5", 1), ("G5", .5), ("F5", .5), ("E5", 1), ("D5", 1)],
    [("C5", 1), ("A4", 1), ("G4", 1), ("E4", 1)],
    [("A4", 4)],
]

# (name, bars, chords)
FORM = [("intro", 4, ["Am7", "Dm7"]), ("riddim", 16, ["Am7", "Dm7"]), ("melodica", 16, ["Am7", "Dm7"]),
        ("version", 16, ["Am7", "Dm7", "Am7", "Dm7", "Fmaj7", "E7sus", "Fmaj7", "E7sus"]),
        ("breakdown", 8, ["Am7", "Dm7"]), ("return", 8, ["Am7", "Dm7"]), ("outro", 6, ["Am7", "Dm7"])]
ALL = {"drums", "bass", "skank", "bubble", "lead"}
VERSION_MIX = [  # the dub mix, bar by bar: who is up on the desk
    {"drums", "bass"}, {"drums", "bass", "skank"}, {"bass", "skank"}, {"drums", "bass", "skank", "bubble"},
    {"drums"}, {"drums", "bass"}, {"drums", "bass", "bubble"}, {"skank"},
    {"drums", "bass", "skank", "bubble"}, {"bass"}, {"drums", "bass", "skank"}, {"drums", "skank", "bubble"},
    {"drums", "bass"}, {"drums", "bass", "skank", "bubble"}, {"bass", "skank"}, {"drums", "bass", "skank", "bubble"},
]


def drums(sec, b, rng, full=True):
    """The one-drop: kick and rim together on 3, hats on the 8ths (swung), ghost rims, a rim roll at phrase ends."""
    ev = [(8, "k,so", 1, 108)]
    for st in ((0, 3, 6, 11, 14) if HATS == "tresillo" else range(0, 16, 2)):
        if st != 8:
            ev.append((st, "h", 1, 70 if st % 4 else 80))
    if rng.random() < 0.5:
        ev.append((rng.choice([3, 11, 13]), "so", 1, 52))
    if b % 4 == 3 and full:
        ev += [(12, "so", 1, 70), (13, "so", 1, 76), (14, "oh", 1, 84), (15, "so", 1, 88)]
    if sec == "intro" and b < 2:
        return grid([(e[0], "h", 1, 40) for e in ev if e[1] == "h"])
    return grid(ev)


def bass(c, drop_one=False):
    ev = [(st, n, ln, 100 if st in (0, 8) else 88) for st, n, ln in BASS[c]]
    if drop_one:
        ev = ev[1:]
    return grid(ev)


def skank(c):
    v, _ = CHORDS[c]
    ch = ",".join(nm(n) for n in v)
    return grid([(4, ch, 1, 86), (12, ch, 1, 90)])


def bubble(c):
    _, (lo, hi) = CHORDS[c]
    ev = []
    for beat in range(4):
        ev += [(beat * 4 + 2, nm(lo), 1, 64), (beat * 4 + 3, nm(hi), 1, 70)]
    return grid(ev)


def lead(k, vel=90):
    return J(*[R(d) if n == "R" else f"{n}/{d:g}b@{vel}" for n, d in CALL[k % 8]])


def crackle(rng):
    """Vinyl crackle: sparse random clicks on the 32nd grid, soft."""
    out = []
    for i in range(32):
        out.append(f"C5/0.125b@{rng.randint(18, 60)}" if rng.random() < (0.18 if CRK == "1" else 0.08) else "R/0.125b")
    return J(*out)


def build():
    names = ("drums", "bass", "skank", "bubble", "lead", "crackle", "hiss")
    T = {n: [] for n in names}
    rng = random.Random(5)
    t, times, throws = 0.0, {}, []
    for sec, nb, chs in FORM:
        times[sec] = t
        for b in range(nb):
            c = chs[b % len(chs)]
            up = set(ALL)
            if sec == "intro":
                up = {"skank"} if b < 2 else {"skank", "drums"}
            elif sec == "riddim":
                up = {"drums", "bass", "skank"} | ({"bubble"} if b >= 4 else set())
            elif sec in ("melodica", "return"):
                up = ALL
            elif sec == "version":
                up = VERSION_MIX[b]
            elif sec == "breakdown":
                up = {"drums", "bass"} if b < 4 else {"skank"}
            elif sec == "outro":
                up = [ALL, ALL - {"lead"}, {"drums", "bass", "skank"}, {"drums", "skank"}, {"skank"}, set()][b]
            bar = {n: R(4) for n in names}
            if "drums" in up:
                bar["drums"] = drums(sec, b, rng)
            else:
                rng.random()  # keep the drums' RNG stream steady across mutes
            if "bass" in up:
                bar["bass"] = bass(c, drop_one=(sec == "version" and b % 2 == 1))
            if "skank" in up:
                bar["skank"] = skank(c)
            if "bubble" in up:
                bar["bubble"] = bubble(c)
            if "lead" in up and sec in ("melodica", "return"):
                bar["lead"] = lead(b, vel=88 if sec == "melodica" else 94)
            bar["crackle"] = crackle(rng)
            bar["hiss"] = "C4/4b@60"
            bt = t + 4 * 60 / BPM
            if b % 4 == 3 and sec != "intro":  # the echo THROW on the phrase's last off-beat
                throws.append(bt - 60 / BPM * 1.0)
            for n in names:
                T[n].append(bar[n])
            t = bt
    return T, times, t, throws


def throw_lane(throws, total):
    pts = [["0s", 0]]
    for a in throws:
        pts += [[f"{a - 0.05:.2f}s", 0], [f"{a:.2f}s", 14], [f"{a + 0.55:.2f}s", 14], [f"{a + 0.75:.2f}s", 0]]
    pts.append([f"{total + 8:.2f}s", 0])
    return pts


def song():
    T, times, total, throws = build()

    def sc(n, swing=None, swing8=None):
        s = " | ".join(T[n])
        s = (f"swing16={swing:g} " + s) if swing else s
        return (f"swing={swing8} " + s) if swing8 else s

    wow = ([{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "lfo.wow", "amount": 0.12}]}, "mix": 1}] if WOW else [])
    lfo = {"wow": "sine rate=0.37hz"} if WOW else {}
    lane = {"thr": {"points": throw_lane(throws, total)}}
    thr_send = lambda base: {"value": f"{base}dB", "mod": [{"src": "auto.thr", "amount": 1}]}  # noqa: E731
    tracks = [
        {"name": "drums", "patch": "room-kit", "gain": "-6dB", "sends": {"spring": "-16dB", "echo": thr_send(-22)},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=6000 gain=-6dB"]}], "auto": lane, "score": sc("drums", HATSW, DRAG or None)},
        {"name": "bass", "patch": "analog-bass", "gain": "0dB", "fx": [{"type": "filter", "kind": "lowpass", "cutoff": 420}],
         "score": sc("bass")},
        {"name": "skank", "patch": "rhodes", "gain": "-6dB", "pan": -0.2, "fx": wow, "lfo": lfo,
         "sends": {"spring": "-6dB", "echo": thr_send(-14)}, "auto": lane, "score": sc("skank", 0.58)},
        {"name": "bubble", "patch": "wurli", "gain": "-12dB", "pan": 0.3, "fx": wow, "lfo": lfo,
         "sends": {"spring": "-12dB"}, "score": sc("bubble", 0.58)},
        {"name": "lead", "patch": "boc-lead", "gain": "-7dB", "pan": 0.1, "fx": wow, "lfo": lfo,
         "sends": {"spring": "-10dB", "echo": thr_send(-9)}, "auto": lane, "score": sc("lead")},
        {"name": "crackle", "patch": "vinyl-crackle", "gain": "-20dB" if CRK == "1" else "-28dB", "score": sc("crackle")},
        {"name": "hiss", "patch": "vinyl-hiss", "gain": "-34dB", "score": sc("hiss")},
    ]
    patches = {
        "vinyl-hiss": {"about": "Tape Weather t5: vinyl/tape hiss - pink noise, band-passed, steady.",
                       "synth": {"layers": [{"type": "noise", "color": "pink"}], "filters": ["bp cutoff=3k q=0.5"],
                                 "amp": {"a": "40ms", "s": 1, "r": "120ms"}}},
        "vinyl-crackle": {"about": "Tape Weather t5: vinyl crackle - 2 ms white-noise ticks, high-passed.",
                          "synth": {"layers": [{"type": "noise"}], "filters": ["hp cutoff=2k"],
                                    "amp": {"a": "0.1ms", "d": "2ms", "s": 0, "r": "2ms"}}},
    }
    bands = (["lowshelf cutoff=110 gain=3dB", "highshelf cutoff=7000 gain=-4dB"] if MEQ == "1" else
             ["lowshelf cutoff=110 gain=3dB", "peak cutoff=600 q=0.8 gain=-6dB", "peak cutoff=300 q=1 gain=-3dB"] if MEQ == "2" else
             ["peak cutoff=640 q=0.8 gain=-9dB", "peak cutoff=300 q=1 gain=-3dB", "highshelf cutoff=6000 gain=4dB"])
    master = {"fx": [{"type": "eq", "bands": bands},
                     {"type": "tape", "drive": 0.35, "warmth": 0.5, "mix": 1},
                     {"type": "compressor", "threshold": "-20dB", "ratio": 2, "attack": "20ms", "release": "220ms", "makeup": "0dB"},
                     {"type": "gain", "gain": f"+{MG:g}dB"}]}
    return {
        "about": ("Chirpers - Tape Weather, track 5 (original composition, chirper-zero; generator "
                  "compose/chirpers3/src/chirpers3-t5.py). Dub-wise space: an original one-drop riddim in A minor at 70 bpm "
                  "mixed live - the mute plan is the arrangement - into a feedback tape echo and a spring, with echo throws, "
                  "tape wow on the keys, vinyl hiss and crackle."),
        "tempo": BPM, "ceiling": "-0.3dB", "tail": "6s", "patches": patches,
        "buses": {"echo": {"fx": [f"delay time={ECHO} feedback=0.62 mix=1 tone=1600"]},
                  "spring": {"fx": ["reverb kind=spring decay=2.4s mix=1 predelay=6ms"]}},
        "master": master, "tracks": tracks,
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "tail", "patches", "master")]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
