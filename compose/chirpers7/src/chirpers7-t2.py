#!/usr/bin/env python3
"""chirpers7-t2 (The Endless Stair, track 2). Composed by chirper-two: MODERN DEEP HOUSE.

"The Filter Never Opens". Sleek, warm and driving: a tech-leaning deep groove whose chord stab lives inside a
BARBER-POLE FILTER. Four copies of the stab run through band-passes an octave apart (200, 400, 800, 1600 Hz); one
song-time sawtooth carries every band up an octave every eight bars while the lowest copy fades in and the highest fades
out, so when the saw wraps each copy lands exactly where its neighbour was: the filter keeps opening and never gets
brighter. (The Shepard idea, applied to a filter sweep.)
- THE STAIR (A B C E) answers t1's Shepard stair as the stab's top note, chopped on the off-beats.
- THE GROOVE: machine-kit rumble kick, crisp hats, claps on 2 and 4, a rim on 3-3-2; a rolling bass (a short saw and
  a sine, pumped) on A.
- THE DROPS: the kick leaves and a noise rise climbs alongside the pole; THE BREAK holds the stab as long chords, so
  the pole's endless rise is heard on its own under the stair.
- THE SEAMS: in, t1's outro (kick, hats, phantom bass, the Shepard stair at 118) plays over t2's first 16 bars of kick
  and hats, the pole entering low at bar 9; out, t2's last 16 bars at 118.5 keep the kick, the hats and the pole turning
  on an open A-E fifth (a colour that sits over t3's E minor), the bass gone.
Tempo 118 -> 118.5 (a ramp inside the track). A minor (8A).
Form (bars of 4/4): in 16 / A1 16 / drop 4 / A2 16 / break 16 / B1 16 / drop 4 / B2 16 / out 16 = 120 bars.

Emits songs/chirpers7-t2.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T2_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t2.yaml")
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
POLE = [200, 400, 800, 1600]  # the four bands, an octave apart


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if e[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - e[0]) < 1e-3:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


FORM = [("in", 16), ("A1", 16), ("drop1", 4), ("A2", 16), ("break", 16), ("B1", 16), ("drop2", 4), ("B2", 16),
        ("out", 16)]
STAIR = [69, 71, 72, 76]                    # A B C E
CHORD = [57, 60, 64, 67]                    # Am7 under the stair's note
# the grooves move under the pole, four bars a chord: Am9 | Fmaj9 | G6 | Em7 (bass root, chord)
PROG = [(33, [57, 60, 64, 67]), (29, [57, 60, 64, 65]), (31, [55, 59, 62, 64]), (28, [55, 59, 62, 64])]
FIFTH = [57, 64, 69]                        # A3 E4 A4: the open fifth for the out seam
BASS = [(0.0, 33, 0.4), (0.75, 33, 0.2), (1.5, 45, 0.25), (2.5, 33, 0.4), (3.25, 40, 0.25), (3.75, 43, 0.2)]


def build():
    rng = random.Random(2)
    T = {k: Track(k) for k in ("kick", "hats", "clap", "rim", "bass", "stab", "stair", "rise")}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    step = 0
    for bi, (start, sec, i, n) in enumerate(bars):
        core = sec in ("A1", "A2", "B1", "B2")
        full = sec in ("A2", "B1", "B2")
        if core or sec in ("in", "out"):
            for b in range(4):
                T["kick"].add(start + b, 1.0, "kr", 112 if b == 0 else 104)
            for b in (0.5, 1.5, 2.5, 3.5):
                T["hats"].add(start + b + 0.01, 0.35, "oh", 66)
        if core:
            for s in range(16):
                if s % 4 != 2:
                    T["hats"].add(start + s * 0.25 + (0.015 if s % 2 else 0), 0.1, "h", (60 if s % 2 else 50) + rng.randint(-5, 5))
        if full:
            T["clap"].add(start + 1.0, 0.5, "cp", 96)
            T["clap"].add(start + 3.0, 0.5, "cp", 96)
        if core:
            for o in (0.0, 0.75, 1.5):
                T["rim"].add(start + 2.0 + o + 0.02, 0.2, "rs", 64 if o == 0 else 52)
        root, chord = 33, CHORD  # (a moving progression under the pole was tried: it split the grooves into shards)
        if core or sec in ("drop1", "drop2"):
            for b, m, ln in BASS:
                T["bass"].add(start + b, ln, nm(m - 33 + root), 100 if b == 0 else 86)
        # ---- the stab inside the barber pole: the chord with the stair's note on top, chopped off the beat ----
        if sec == "out":
            if i % 2 == 0:
                T["stab"].add(start, 7.8, ",".join(nm(x) for x in FIFTH), 70)
        elif sec in ("break",):
            if i % 2 == 0:
                T["stab"].add(start, 7.8, ",".join(nm(x) for x in CHORD + [STAIR[(i // 2) % 4]]), 70)
        elif not (sec == "in" and i < 8):
            for o in ((0.5, 1.75, 2.5, 3.25) if core else (0.5, 2.5)):
                top = STAIR[step % 4]
                step += 1
                T["stab"].add(start + o, 0.3, ",".join(nm(x) for x in chord + [top]), 84 if o == 0.5 else 74)
        # ---- the stair itself, quoted plainly once a phrase (as t1 handed it over) ----
        if sec in ("A2", "B2") and i % 8 == 7:
            for k, m in enumerate(STAIR):
                T["stair"].add(start + k, 0.9, nm(m), 70)
        if sec in ("drop1", "drop2") and i == 0:
            T["rise"].add(start, 16.0, "C4", 92)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    return {
        "c2-stab": {"about": "chirper-two: a bright house chord stab, two detuned saws and a pulse, quick.",
                    "synth": {"layers": [{"wave": "saw", "detune": -8}, {"wave": "saw", "detune": 8},
                                         {"wave": "pulse", "level": "-6dB"}],
                              "amp": {"a": "2ms", "d": "260ms", "s": 0.15, "r": "120ms"}},
                    "play": {"vel_sens": 0.6}},
        "c2-rollbass": {"about": "chirper-two: a rolling deep-house bass, a short saw and a sine through a low-pass.",
                        "synth": {"layers": [{"wave": "sine"}, {"wave": "saw", "level": "-10dB"}],
                                  "filters": [{"kind": "lp", "q": 1.0,
                                               "cutoff": {"value": 260, "mod": [{"src": "env.f", "amount": 1.6}]}}],
                                  "env": {"f": {"a": "1ms", "d": "120ms", "s": 0.0}},
                                  "amp": {"a": "2ms", "d": "220ms", "s": 0.4, "r": "60ms"}},
                        "play": {"vel_sens": 0.6, "mono": True}},
        "c2-stair": {"about": "chirper-two: THE STAIR's voice, a Shepard tone (see t1).",
                     "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "600hz", "width": 1.1}}],
                               "amp": {"a": "4ms", "d": "700ms", "s": 0.25, "r": "400ms", "curve": 2}},
                     "play": {"vel_sens": 0.6}},
        "c2-rise": {"about": "chirper-two: a noise rise, band-passed noise whose centre climbs with its envelope.",
                    "synth": {"layers": [{"type": "noise"}],
                              "filters": [{"kind": "bp", "q": 1.5,
                                           "cutoff": {"value": 300, "mod": [{"src": "env.up", "amount": 5.0}]}}],
                              "env": {"up": {"a": "8s", "d": "1s", "s": 1.0}},
                              "amp": {"a": "6s", "d": "1s", "s": 1.0, "r": "300ms"}}},
    }


def pole_tracks(score, total, st):
    """The barber pole: four copies of the stab, band-passed an octave apart, all carried up an octave per cycle by one
    song-time sawtooth (lfo.s, 0..1, eight bars a cycle); the lowest fades in and the highest fades out across it."""
    out = []
    n = len(POLE)
    for k, base in enumerate(POLE):
        if k == 0:
            g = {"value": "-30dB", "mod": [{"src": "lfo.s", "amount": 30}]}       # fades in as it rises
        elif k == n - 1:
            g = {"value": "0dB", "mod": [{"src": "lfo.s", "amount": -30}]}       # fades out as it rises
        else:
            g = "0dB"
        out.append({"name": f"pole{k}", "patch": "c2-stab", "gain": "-14dB", "pan": [-0.3, -0.1, 0.1, 0.3][k],
                    "lfo": {"s": "saw rate=8/1 unipolar=true"},
                    "sends": {"room": "-6dB"},
                    "fx": [{"type": "filter", "kind": "bp", "q": 2.2,
                            "cutoff": {"value": base, "mod": [{"src": "lfo.s", "amount": 1.0}]}},
                           {"type": "gain", "gain": g}],
                    "score": score})
    return out


def main():
    total, bars, sec, T = build()
    st = {n: s for n, s, k in sec}
    tempo = [{"at": "0b", "bpm": 118}, {"at": f"{st['A1']}b", "bpm": 118},
             {"at": f"{st['out']}b", "bpm": 118.5, "ramp": True}]
    dyn = [["0b", 0.0], [f"{st['drop1']}b", -3.0], [f"{st['A2'] - 0.01}b", -3.0], [f"{st['A2']}b", 0.0],
           [f"{st['break']}b", -5.0], [f"{st['B1'] - 0.01}b", -5.0], [f"{st['B1']}b", 0.0], [f"{st['drop2']}b", -3.0],
           [f"{st['B2'] - 0.01}b", -3.0], [f"{st['B2']}b", 0.0], [f"{total}b", 0.0]]
    pump = {"type": "pump", "on": "kick.kr", "depth": "-7dB", "attack": "3ms", "release": "340ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "0dB", "score": T["kick"].score(total)},
        {"name": "hats", "patch": "machine-kit", "gain": "-2dB", "pan": 0.08,
         "fx": ["hp cutoff=500", "reverb kind=room decay=0.5s mix=0.1"], "score": T["hats"].score(total)},
        {"name": "clap", "patch": "machine-kit", "gain": "-4dB", "fx": ["reverb kind=plate decay=1.1s mix=0.2"],
         "score": T["clap"].score(total)},
        {"name": "rim", "patch": "machine-kit", "gain": "-8dB", "pan": -0.25, "score": T["rim"].score(total)},
        {"name": "bass", "patch": "c2-rollbass", "gain": "-4dB", "fx": [pump], "score": T["bass"].score(total)},
        *pole_tracks(T["stab"].score(total), total, st),
        {"name": "stair", "patch": "c2-stair", "gain": "-10dB", "pan": 0.2,
         "fx": [{"type": "delay", "time": "3/16", "feedback": 0.35, "mix": 0.25, "ping_pong": True, "tone": 3000},
                "reverb kind=hall decay=2.5s mix=0.25"], "score": T["stair"].score(total)},
        {"name": "rise", "patch": "c2-rise", "gain": "-20dB", "fx": ["width width=1.5"], "score": T["rise"].score(total)},
    ]
    for tr in tracks:
        if tr["name"].startswith("pole"):
            tr["fx"] = [pump] + tr["fx"]
    buses = {"room": {"gain": "-6dB",
                      "fx": ["hp cutoff=300", "lp cutoff=3000",
                             {"type": "tape", "drive": 0.3, "warmth": 0.6, "wow": 2, "flutter": 1, "seed": 2},
                             "limiter ceiling=-6dB"],
                      "returns": [{"from": "room", "gain": "-5dB", "time": "3/16"}]}}
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - The Endless Stair, track 2. Original composition by chirper-two, generated by "
             "compose/chirpers7/src/chirpers7-t2.py. Modern deep house, 118 -> 118.5 bpm, A minor: a chord stab inside "
             "a BARBER-POLE FILTER (four band-passed copies an octave apart, carried up by one sawtooth while the lowest "
             f"fades in and the highest fades out: it keeps opening, never brighter). Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "The Endless Stair", "title": "The Filter Never Opens",
                               "track": 2, "year": 2026}),
        "tempo: " + json.dumps(tempo),
        f'length: "{total:g}b"',
        'tail: "1s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "patches: " + json.dumps(patches()),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=160 gain=-3dB q=0.8",
                                                               "peak cutoff=3500 gain=2dB q=0.7",
                                                               "highshelf cutoff=6000 gain=3dB"]},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars; {secs}")


if __name__ == "__main__":
    main()
