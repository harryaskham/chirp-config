#!/usr/bin/env python3
"""chirpers5-t7 (Soft Concrete, track 7). Composed by chirper-two: REESE-LED LIQUID.

"Concrete Hum". A deep rolling liquid tune whose lead is a living reese: not a neuro snarl but a warm, moving, singing
bass the whole tune leans on.
- THE REESE: the library reese (detuned saw pairs drifting against each other) sings a gliding two-bar riff. On top of
  its own churn, its low-pass breathes on two song-time LFOs, 3 and 5 bars long, and a notch sweeps through it on a
  7-bar one (No Floor's throb, brought to liquid), so no two bars of it sound the same; it ducks under the kick.
- THE FRAME: the chords only frame it: a high pad and sparse Rhodes stabs, Gm9 | Ebmaj7 | Cm9 | D7(b9), four bars
  each. A sub under the reese's roots.
- THE ROLLER: a straight amen-chops roller (a different re-sequence from Overpass Rain) over a clean kick and snare.
- THE HALF-TIME BREAK: in the middle the drums drop to half time (kick on 1, snare on 3) and the reese is drawn out
  long, one note a bar, the LFOs slowly opening it.
- THE SECOND DROP: an octave-up counter-reese answers the riff.
Form (bars of 4/4, 174 bpm): intro 16 / drop A 32 / half-time 16 / build 8 / drop B 40 / outro 16 = 128 bars, ~177 s.

Emits songs/chirpers5-t7.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T7_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers5-t7.yaml")
BPM = 174
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
LVL_GAIN = 5  # dB into the true-peak master limiter (levels.py: -12.2 LUFS, TP -1.19 dBTP, no flat runs)


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
            ln = min(ln, nxt - s)  # the score is sequential; a ^gate above 1 makes the notes overlap (glide)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


# Round 2 (v2), polish for the running order: J = THE END HUMS: the outro no longer runs out into four bars of
# silence; the pad and the held reese hum (the intro's mirror) carry it to the last bar, a short tail (0.5 s), so
# Concrete Hum hands Wet Brick a room, not a gap.
# (G, a ghost on the a-of-4 leaning into each bar, was tried: it did not move the groove; off by default.)
R2 = set(filter(None, os.environ.get("T7_R2", "J").split(","))) - {"none"}
# Round 3 (v3), the FINAL round, on Harry's Soft Concrete notes. (No swing here either: the rolls sit on the straight
# grid.) B = A BASS THAT READS: the mono sub comes up 2 dB and gains wM's phantom harmonics; the reese, its mid layer,
# drives its tape a little harder; both pumped by the kick; T = THE TOOLBOX IN THE TRANSITIONS: the first drop ends on
# a VINYL SPIN-BACK into the half-time break, and through the build a second copy of the amen rings through a COMB
# filter whose pitch climbs two octaves into the second drop; D = A SHADE DARKER: the top down 1.5 dB above 6 kHz.
R3 = set(filter(None, os.environ.get("T7_R3", "B,T,D").split(","))) - {"none"}
FORM = [("intro", 16), ("A", 32), ("half", 16), ("build", 8), ("B", 40), ("outro", 16)]
CHORDS = [(43, [58, 62, 65, 69]),   # Gm9: G2 | Bb3 D4 F4 A4
          (39, [55, 58, 62, 67]),   # Ebmaj7(9): Eb2 | G3 Bb3 D4 G4
          (36, [58, 62, 63, 67]),   # Cm9: C2 | Bb3 D4 Eb4 G4
          (38, [60, 63, 66, 69])]   # D7(b9): D2 | C4 Eb4 F#4 A4
# the reese riff, two bars over each chord's root (offsets in semitones from the root): (beat, length, offset)
# in 3+3+2 sixteenths (the dotted D&B bass rhythm): each half bar lands on 0, the a-of-1 and the and-of-2
RIFF = [(0.0, 0.75, 0), (0.75, 0.75, 0), (1.5, 0.5, 3), (2.0, 0.75, 0), (2.75, 0.75, -2), (3.5, 0.5, 0),
        (4.0, 0.75, 0), (4.75, 1.25, 7), (6.0, 0.75, 5), (6.75, 0.75, 3), (7.5, 0.5, 2)]
COUNTER = [(0.5, 0.5, 12), (1.0, 1.0, 10), (2.5, 1.5, 7), (5.0, 1.0, 15), (6.5, 1.5, 12)]  # the octave-up answer
# the roller: (beat, amen slice, velocity offset, tune)
ROLL = [(0.0, 0, 0, 0), (0.5, 1, -10, 0), (1.0, 2, 0, 0), (1.5, 3, -18, 0),
        (2.0, 9, -14, 0), (2.75, 13, -6, 0), (3.0, 2, -2, 0), (3.5, 7, -16, 0)]
ROLL_FILL = [(0.0, 0, 0, 0), (0.5, 1, -10, 0), (1.0, 2, 0, 0), (1.5, 3, -18, 0),
             (2.0, 9, -14, 0), (2.75, 13, -6, 0), (3.0, 2, -2, 0), (3.25, 6, -12, 3), (3.5, 7, -10, 5), (3.75, 6, -8, 7)]


def build():
    rng = random.Random(7)
    T = {k: Track(k) for k in ("reese", "counter", "sub", "pad", "rhodes", "amen", "kick", "snare", "hats", "comb")}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    for bi, (start, sec, i, n) in enumerate(bars):
        root, voic = CHORDS[(i // 4) % 4]
        drop = sec in ("A", "B")
        r = root - 12  # the reese and the sub sit an octave below the chord root: G1 Eb1 C1 D1
        # ---- the reese ----
        if (drop or sec == "build" or (sec == "outro" and i < 8)) and i % 2 == 0:
            for b, ln, off in RIFF:
                T["reese"].add(start + b, ln, nm(r + 12 + off), 104 if b in (0.0, 4.0) else 92, "^gate=1.15")
        elif (sec == "intro" and i >= 8 and i % 4 == 0) or ("J" in R2 and sec == "outro" and i in (8, 12)):
            T["reese"].add(start, 16.0, nm(r + 12), 76)  # the hum, held, filtered: the reese waiting
        elif sec == "half":
            T["reese"].add(start, 4.0, nm(r + 12), 90, "^gate=1.05")  # drawn out, a note a bar
        if sec == "B" and i % 2 == 0 and i >= 8:
            for b, ln, off in COUNTER:
                T["counter"].add(start + b, ln, nm(r + 12 + off), 86, "^gate=1.1")
        # ---- the sub on the roots ----
        if drop or sec in ("build", "half"):
            T["sub"].add(start, 1.8, nm(r), 100)
            T["sub"].add(start + 2.5, 1.3, nm(r), 92)
        # ---- the frame: a pad (four bars a chord) and Rhodes stabs ----
        if i % 4 == 0 and sec != "outro" or (sec == "outro" and i % 4 == 0 and (i < 12 or "J" in R2)):
            T["pad"].add(start, 15.9, ",".join(nm(x + 12) for x in voic[1:]), 58)
        if drop and i % 2 == 1:
            for b in (0.75, 2.75):
                T["rhodes"].add(start + b + 0.02, 0.35, ",".join(nm(x) for x in voic), 78 if b == 0.75 else 70)
        # ---- the drums ----
        half = sec == "half"
        rolling = drop or sec == "build" or (sec == "intro" and i >= 12) or (sec == "outro" and i < 8)
        if rolling:
            pat = ROLL_FILL if (i % 8 == 7 or (sec == "build" and i == n - 1)) else (ROLL + [(3.75, 6, -20, 2)] if "G" in R2 else ROLL)
            soft = sec in ("intro", "outro")
            for b, sl, dv, tune in pat:
                if sec == "build" and i < 4 and b not in (0.0, 1.0, 2.5, 3.0):
                    continue
                T["amen"].add(start + b, 0.5, nm(36 + sl), 100 + dv - (12 if soft else 0), f"^tune={tune}" if tune else "")
                if "T" in R3 and sec == "build":  # the build's ringing copy
                    T["comb"].add(start + b, 0.5, nm(36 + sl), 100 + dv, f"^tune={tune}" if tune else "")
        if drop or sec == "build":
            for b in (0.0, 2.75):  # the second kick on the a-of-3: the roller leans
                T["kick"].add(start + b, 0.5, "k", 104 if b == 0 else 94)
            for b in (1.0, 3.0):
                T["snare"].add(start + b, 0.5, "s", 98)
        if half:  # half time: kick on 1, snare on 3, the amen's ride slices between
            T["kick"].add(start, 0.5, "k", 100)
            T["snare"].add(start + 2.0, 0.5, "s", 100)
            for b, sl in ((1.0, 4), (3.0, 7)):
                T["amen"].add(start + b, 0.5, nm(36 + sl), 70)
        # ---- shaker sixteenths over the drops ----
        if drop:
            for s in range(16):
                if s % 2 == 1:
                    T["hats"].add(start + s * 0.25, 0.1, "h", 50 + (14 if s % 4 == 3 else 0) + rng.randint(-4, 4))
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def main():
    total, bars, sec, T = build()
    st = {n: s for n, s, k in sec}
    roll = [["0b", 0.0], [f"{st['build'] + 28}b", 0.0], [f"{st['build'] + 28.01}b", 1.0], [f"{st['B']}b", 1.0],
            [f"{st['B'] + 0.01}b", 0.0]]
    ropen = [["0b", -1.5], [f"{st['A']}b", 0.0], [f"{st['half']}b", -0.5], [f"{st['build']}b", 0.3],
             [f"{st['B']}b", 0.2], [f"{st['outro']}b", 0.0], [f"{total}b", -1.5]]
    pump = {"type": "pump", "on": "kick.k", "depth": "-7dB", "attack": "3ms", "release": "230ms", "curve": 0.8}
    rhodes = "epiano-tine synth.tine.sense=0.4 play.release.patch=epiano-damper play.release.decay=1.5s"
    cpitch = [["0b", 0.0], [f"{st['build']}b", 0.0], [f"{st['B']}b", 2.0], [f"{total}b", 2.0]]
    spin = [["0b", 0.0], [f"{st['half'] - 1}b", 0.0], [f"{st['half'] - 0.99}b", 1.0], [f"{st['half']}b", 1.0],
            [f"{st['half'] + 0.01}b", 0.0], [f"{total}b", 0.0]]
    tracks = [
        {"name": "reese", "patch": "reese", "gain": "-7dB",
         "lfo": {"a": "sine rate=3/1", "b": "tri rate=5/1 phase=0.25", "n": "sine rate=7/1 phase=0.5"},
         "fx": [pump,
                {"type": "filter", "kind": "lp", "q": 1.2,
                 "cutoff": {"value": 900, "mod": [{"src": "lfo.a", "amount": 0.7}, {"src": "lfo.b", "amount": 0.5},
                                                  {"src": "auto.ropen", "amount": 1.0}]}},
                {"type": "filter", "kind": "notch", "q": 2.0,
                 "cutoff": {"value": 600, "mod": [{"src": "lfo.n", "amount": 1.2}]}},
                "hp cutoff=45", "tape drive=%g warmth=0.5" % (0.55 if "B" in R3 else 0.35)],
         "auto": {"ropen": {"points": ropen}}, "score": T["reese"].score(total)},
        {"name": "counter", "patch": "reese", "gain": "-15dB", "pan": 0.25,
         "lfo": {"c": "sine rate=5/1 phase=0.6"},
         "fx": [pump, {"type": "filter", "kind": "lp", "q": 1.0,
                       "cutoff": {"value": 1600, "mod": [{"src": "lfo.c", "amount": 0.6}]}},
                "hp cutoff=150", {"type": "delay", "time": "3/16", "feedback": 0.25, "mix": 0.18, "tone": 2500}],
         "score": T["counter"].score(total)},
        {"name": "sub", "patch": "sub-sine", "gain": "-4dB" if "B" in R3 else "-6dB",
         "fx": [{"type": "pump", "on": "kick.k", "depth": "-6dB", "attack": "2ms", "release": "150ms", "curve": 0.8}]
                + ([{"type": "phantom", "cutoff": "120hz", "harmonics": "-6dB", "odd": 0.4}] if "B" in R3 else []),
         "score": T["sub"].score(total)},
        {"name": "pad", "patch": "juno-pad", "gain": "-18dB", "fx": [pump, "hp cutoff=350"], "score": T["pad"].score(total)},
        {"name": "rhodes", "patch": rhodes, "gain": "-9dB", "pan": -0.2,
         "fx": [{"type": "chorus", "rate": 0.6, "depth": 0.3, "voices": 2, "mix": 0.4}, "hp cutoff=150",
                {"type": "delay", "time": "3/8", "feedback": 0.3, "mix": 0.22, "ping_pong": True, "tone": 2800},
                "reverb kind=hall decay=2.2s mix=0.25"], "score": T["rhodes"].score(total)},
        {"name": "amen", "patch": "amen-chops", "gain": "-5dB", "out": "drums",
         "fx": ["hp cutoff=60",
                {"type": "stutter", "slice": "1/8", "repeats": 8, "roll": 0.5, "pitch": 1,
                 "chance": {"value": 0, "mod": [{"src": "auto.roll", "amount": 1}]}},
                "reverb kind=room decay=0.5s mix=0.1"],
         "auto": {"roll": {"points": roll}}, "score": T["amen"].score(total)},
        *([{"name": "amen-comb", "patch": "amen-chops", "gain": "-14dB", "pan": 0.2,
            "fx": [{"type": "filter", "kind": "comb", "q": 12,
                    "cutoff": {"value": 196, "mod": [{"src": "auto.cp", "amount": 1.0}]}},
                   "hp cutoff=200", "reverb kind=plate decay=1.2s mix=0.2"],
            "auto": {"cp": {"points": cpitch}}, "score": T["comb"].score(total)}] if "T" in R3 else []),
        {"name": "kick", "patch": "break-kit", "gain": "-6dB", "out": "drums", "fx": ["lp cutoff=3000"],
         "score": T["kick"].score(total)},
        {"name": "snare", "patch": "break-kit", "gain": "-9dB", "out": "drums", "score": T["snare"].score(total)},
        {"name": "hats", "patch": "break-kit", "gain": "-12dB", "pan": 0.15, "fx": ["hp cutoff=5000"],
         "score": T["hats"].score(total)},
    ]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Soft Concrete, track 7. Original composition by chirper-two, generated by "
             "compose/chirpers5/src/chirpers5-t7.py. Reese-led liquid drum & bass at 174 bpm in G minor: a living reese "
             "sings a gliding riff, its filter breathing on 3- and 5-bar song-time LFOs and a notch sweeping it every 7 "
             "bars; pads and sparse Rhodes stabs frame it (Gm9 Ebmaj7 Cm9 D7(b9)); an amen roller over a clean kick and "
             f"snare, a half-time break, an octave-up counter-reese in the second drop. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Soft Concrete", "title": "Concrete Hum",
                               "track": 7, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "%s"' % ("0.5s" if "J" in R2 else "2s"),
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "true_peak: true",
        "buses: " + json.dumps({"drums": {"gain": "0dB", "fx": [
            {"type": "compressor", "threshold": "-16dB", "ratio": 4, "attack": "1ms", "release": "70ms",
             "makeup": "2dB"}]}}),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25"]
                                          + (["highshelf cutoff=6000 gain=-1.5dB"] if "D" in R3 else [])},
                                        "glue threshold=-22dB ratio=2.5 attack=10ms release=150ms makeup=1dB",
                                        "tape drive=0.2 warmth=0.4",
                                        {"type": "gain", "gain": f"{LVL_GAIN:g}dB"},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}]
                                 + ([{"type": "tapestop", "stop": {"value": 0, "mod": [{"src": "auto.spin", "amount": 1}]},
                                      "time": "1b", "spin": 3}] if "T" in R3 else []),
                                 **({"auto": {"spin": {"points": spin}}} if "T" in R3 else {})}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
