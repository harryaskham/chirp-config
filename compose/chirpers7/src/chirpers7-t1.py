#!/usr/bin/env python3
"""chirpers7-t1 (The Endless Stair, track 1, the opener). Composed by chirper-two: DEEP MINIMAL HOUSE.

"The First Step". The tape's door, deep, patient and heavy-bottomed. The thread of the whole tape, THE STAIR (degrees
1 2 3 5: here A B C E), enters as an endlessly rising SHEPARD SCALE: each step is a Shepard tone (octave-spaced
partials under a fixed bell), so A B C E A B C E ... climbs for ever and never gets higher. Everything else climbs with
it: the tempo (116 -> 118 inside the track, so the tape is already rising), the filters, the rumble, the hats.
- THE GROOVE: chirper-two's analog drum-machine voices (machine-kit): the rumble kick, off-beat open hats, sixteenth
  hats whose brightness climbs on a lane, a clap that arrives late and sparse, a rim on a 3-3-2.
- THE BASS: a phantom-fundamental bass (only its 2nd to 6th harmonics sound; the ear supplies the A1 under them), clear
  of the kick's sub; pumped.
- THE CHORD: an A minor 9 dub stab into a feedback echo room (the bus returns into itself through a lo-pass and a tape),
  its filter rising section by section; under the stair the harmony moves: F (VI) in A2's second half, F G Am at the peak.
- THE BREAK: the kick goes; a Shepard-Risset pad glides up for ever under the stair slowed to half notes; a voice
  whispers "up".
- THE SEAM: the last 16 bars thin to kick, hats, the phantom bass and the stair at 118 bpm, in A minor, for track 2.
Form (bars of 4/4): the stair alone 8 / the kick 8 / A1 16 / a four-bar drop / A2 (clap, chord) 16 / break 16 /
B1 (A2 returns) 16 / a four-bar drop with the rise / B2 (the peak: the stair in sixteenths over F G Am, the rim, the
Shepard pad gliding) 16 / outro (the seam) 32 = 136 bars.

Emits songs/chirpers7-t1.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T1_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers7-t1.yaml")
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
LVL_GAIN = float(os.environ.get("LVL_GAIN", "7"))
# rounds: T1_R2 = turn (v2: the loop's join. When the tape loops t18 -> t1, the closer ends with the stair FALLING for
# ever in Shepard tones, the kick gone; t1 now begins there - the stair still falling for two bars (E C B A, counting
# down) - then a whisper, "up", and the stair turns and climbs. One illusion turned round, not a restart; chirper-zero's
# note. (Starting at t18's 112 bpm and ramping to 116 was tried: any tempo ramp in the head split the ambient bars off
# as a section, 90.5.) T1_R2=none reproduces v1.
R2 = os.environ.get("T1_R2", "turn")
# T1_R3 = slow (v3: the stair SLOWS over the last 16 bars - the seam into t2 - while the kick and the tempo hold: its
# steps stretch smoothly from quarter notes to half notes (each a little longer than the last, 2^(p/64) beats), still
# climbing. A first hint of the comedown, the tape's first play with time as well as tone; chirper-one's note.)
# T1_R3=none reproduces v2.
R3 = os.environ.get("T1_R3", "slow")
# T1_R4 = rim (v4: the rim becomes the groove's hook - a 3-3-3-3-4 cycle of sixteenths starting on the and-of-one
# (0.5, 1.25, 2.0, 2.75, 3.5), up 3 dB, level with the off-beat hats: a minimal-house syncopation that leaves the kick
# its downbeats, where the 3-3-2 sat quietly in the second half of the bar). T1_R4=none reproduces v3.
R4 = os.environ.get("T1_R4", "rim")


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


FORM = [("ambient", 8), ("intro", 8), ("A1", 16), ("drop1", 4), ("A2", 16), ("break", 16), ("B1", 16), ("drop2", 4),
        ("B2", 16), ("outro", 32)]
STAIR = [69, 71, 72, 76]           # A B C E: the thread (Shepard tones: the octave is only the note's name)
CHORD = [57, 60, 64, 67, 71]       # Am9: A3 C4 E4 G4 B4
# the harmony under the stair moves: A2's second half sits on F (VI), the peak climbs F G Am under it
SHIFT = {0: (0, [57, 60, 64, 67, 71]), -4: (-4, [53, 57, 60, 64, 67]), -2: (-2, [55, 59, 62, 64, 69])}
BASS = [(0.5, 33), (1.75, 33), (2.5, 40), (3.25, 33), (3.5, 36)]  # A1 . E2 A1 C2, off the beat (phantom)


def build():
    rng = random.Random(1)
    T = {k: Track(k) for k in ("kick", "hats", "clap", "rim", "bass", "stair", "chord", "pad", "voice", "rise")}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    step = 0  # the stair keeps counting across the whole track: it never restarts, it only climbs
    for bi, (start, sec, i, n) in enumerate(bars):
        full = sec in ("A2", "B1", "B2")      # the clap and the chord
        core = sec in ("A1", "A2", "B1", "B2")
        groove = core or sec in ("intro", "outro")
        # ---- the kick (the rumble kick), four on the floor; none in the break ----
        if groove:
            for b in range(4):
                T["kick"].add(start + b, 1.0, "kr", 112 if b == 0 else 104)
        # ---- hats: off-beat open hats; sixteenth closed hats from A on ----
        if groove:
            for b in (0.5, 1.5, 2.5, 3.5):
                T["hats"].add(start + b + 0.01, 0.4, "oh", 70 if sec != "intro" else 56)
        if full:
            for s in range(16):
                if s % 4 != 2:
                    T["hats"].add(start + s * 0.25 + (0.012 if s % 2 else 0), 0.12, "h",
                                  (62 if s % 2 else 52) + rng.randint(-5, 5))
        # ---- clap, late and sparse; a rim on 3-3-2 in B ----
        if full:
            T["clap"].add(start + 1.0, 0.5, "cp", 92)
            T["clap"].add(start + 3.0, 0.5, "cp" if i % 4 != 3 else "cpw", 96)
        if core and R4 == "rim":  # the rim: 3-3-3-3-4 sixteenths from the and-of-one (louder at the peak)
            for k, o in enumerate((0.5, 1.25, 2.0, 2.75, 3.5)):
                T["rim"].add(start + o + 0.02, 0.2, "rs", (74 if k == 0 else 64) - (0 if sec == "B2" else 6))
        elif core:  # the rim on a 3-3-2 across the second half of each bar (louder at the peak)
            for o in (0.0, 0.75, 1.5):
                T["rim"].add(start + 2.0 + o + 0.02, 0.2, "rs", (70 if o == 0 else 58) - (0 if sec == "B2" else 8))
        # ---- the phantom bass ----
        shift = 0
        if sec == "B2":
            shift = (-4, -2, 0, 0)[(i // 2) % 4]
        sh, chord_notes = SHIFT[shift]
        if core or (sec == "intro" and i >= 4) or sec == "outro":
            for b, m in BASS:
                T["bass"].add(start + b, 0.45, nm(m + sh), 96)
        # ---- the stair: quarter notes in the intro and outro, eighths in A and B, half notes in the break ----
        rate = {"ambient": 1.0, "intro": 1.0, "A1": 0.5, "drop1": 1.0, "A2": 0.5, "break": 2.0, "B1": 0.5,
                "drop2": 1.0, "B2": 0.25, "outro": 1.0}[sec]
        if R3 == "slow" and sec == "outro" and i >= 16:
            if i == 16:  # the last 16 bars: one continuous ritardando of the stair against the steady four
                p = 0.0
                while p < 64.0 - 1e-6:
                    ioi = 2 ** (p / 64.0)
                    m = STAIR[step % 4]
                    T["stair"].add(start + p, min(ioi * 0.9, 64.0 - p), nm(m), 64 + (10 if step % 4 == 0 else 0))
                    step += 1
                    p += ioi
        elif R2 == "turn" and sec == "ambient" and i < 2:  # still falling, as t18 left it: E C B A, E C B A
            for k in range(4):
                m = STAIR[3 - k]
                T["stair"].add(start + k, 0.9, nm(m), 64 + (10 if k == 3 else 0))
        else:
            t = 0.0
            while t < 4.0 - 1e-6:
                m = STAIR[step % 4]
                v = (64 if sec in ("ambient", "intro", "outro") else 74) + (10 if step % 4 == 0 else 0) - (8 if sec == "B2" and step % 2 else 0)
                T["stair"].add(start + t, rate * 0.9, nm(m), v)
                step += 1
                t += rate
        # ---- the dub chord: on the a-of-1 and the and-of-3 (every other bar), into the echo room ----
        if full or (sec in ("break", "drop1", "drop2") and i % 4 == 0):
            chord = ",".join(nm(x) for x in chord_notes)
            if sec in ("break", "drop1", "drop2"):
                T["chord"].add(start + 0.75, 0.3, chord, 80)
            else:
                T["chord"].add(start + 0.75, 0.25, chord, 84)
                if i % 2 == 1 or sec == "B2":
                    T["chord"].add(start + 2.5, 0.25, chord, 74)
        # ---- the break: the endless pad, the whisper; a noise rise into B ----
        if (sec in ("break", "drop1") and i % 8 == 0) or (sec == "B2" and i % 8 == 0):
            T["pad"].add(start, 31.8, "A3,C4,E4", 80 if sec == "break" else 70)  # the stair takes off in B2
        if R2 == "turn" and sec == "ambient" and i == 1:  # the turn, whispered
            T["voice"].add(start + 3.0, 1.0, "A2", 66, "^ph=ah1-p^f0=0>40>80")
        if (sec == "break" and i in (4, 12)) or (sec == "drop2" and i == 0):
            T["voice"].add(start + 2.0, 1.0, "A2", 70, "^ph=ah1-p^f0=0>40>80")
        if sec == "break" and i == 8:
            T["rise"].add(start, 32.0, "C4", 90)
        if sec == "drop2" and i == 0:
            T["rise"].add(start, 16.0, "C4", 96)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    return {
        "c2-stair": {"about": "chirper-two: THE STAIR's voice, a Shepard tone (octave-spaced partials under a fixed "
                              "bell centred near 600 Hz): played as a scale it climbs for ever without getting higher.",
                     "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "600hz", "width": 1.1}}],
                               "amp": {"a": "4ms", "d": "700ms", "s": 0.25, "r": "400ms", "curve": 2}},
                     "play": {"vel_sens": 0.6}},
        "c2-dub-stab": {"about": "chirper-two's dub chord stab: two detuned saws and a square through a lo-pass whose "
                                 "envelope snaps open and shut, its base cutoff on the track's `copen` lane.",
                        "synth": {"layers": [{"wave": "saw", "detune": -7}, {"wave": "saw", "detune": 7},
                                             {"wave": "square", "level": "-8dB"}],
                                  "filters": [{"kind": "lp", "q": 1.4,
                                               "cutoff": {"value": 380, "mod": [{"src": "env.f", "amount": 2.2},
                                                                                {"src": "auto.copen", "amount": 1.0}]}}],
                                  "env": {"f": {"a": "1ms", "d": "160ms", "s": 0.0}},
                                  "amp": {"a": "2ms", "d": "280ms", "s": 0.0, "r": "90ms"}},
                        "play": {"vel_sens": 0.6}},
        "c2-rise": {"about": "chirper-two: a noise rise, band-passed noise whose centre climbs with its envelope.",
                    "synth": {"layers": [{"type": "noise"}],
                              "filters": [{"kind": "bp", "q": 1.5,
                                           "cutoff": {"value": 300, "mod": [{"src": "env.up", "amount": 5.0}]}}],
                              "env": {"up": {"a": "14s", "d": "1s", "s": 1.0}},
                              "amp": {"a": "10s", "d": "1s", "s": 1.0, "r": "300ms"}}},
    }


def main():
    total, bars, sec, T = build()
    st = {n: s for n, s, k in sec}
    # the lanes that climb with the stair: the hats' high-pass opening, the chord's filter, the room's send
    hats_open = [["0b", 0.0], [f"{st['A1']}b", 0.3], [f"{st['A2']}b", 0.5], [f"{st['break']}b", 0.8], [f"{st['B1']}b", 0.6],
                 [f"{st['outro']}b", 1.0], [f"{total}b", 0.6]]
    copen = [["0b", 0.0], [f"{st['A2']}b", 0.0], [f"{st['break']}b", 1.2], [f"{st['B1']}b", 0.8],
             [f"{st['B2']}b", 1.4], [f"{st['outro']}b", 1.8], [f"{total}b", 0.6]]
    tempo = [{"at": "0b", "bpm": 116}, {"at": f"{st['A1']}b", "bpm": 116},
             {"at": f"{st['outro'] + 64}b", "bpm": 118, "ramp": True}]
    pump = {"type": "pump", "on": "kick.kr", "depth": "-7dB", "attack": "3ms", "release": "340ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "0dB", "score": T["kick"].score(total)},
        {"name": "hats", "patch": "machine-kit", "gain": "-2dB", "pan": 0.08,
         "fx": [{"type": "filter", "kind": "hp", "cutoff": {"value": 300, "mod": [{"src": "auto.hopen", "amount": 2.5},
                                                                                 {"src": "lfo.h", "amount": 0.4}]}},
                "reverb kind=room decay=0.5s mix=0.1"],
         "lfo": {"h": "sine rate=5/1"}, "auto": {"hopen": {"points": hats_open}}, "score": T["hats"].score(total)},
        {"name": "clap", "patch": "machine-kit", "gain": "-4dB", "fx": ["reverb kind=plate decay=1.2s mix=0.2"],
         "score": T["clap"].score(total)},
        {"name": "rim", "patch": "machine-kit", "gain": "-3dB" if R4 == "rim" else "-6dB", "pan": -0.25,
         "score": T["rim"].score(total)},
        {"name": "bass", "patch": "phantom-bass", "gain": "-3dB", "fx": [pump], "score": T["bass"].score(total)},
        {"name": "stair", "patch": "c2-stair", "gain": "-8dB", "pan": 0.15,
         "fx": [{"type": "delay", "time": "3/16", "feedback": 0.35, "mix": 0.22, "ping_pong": True, "tone": 3000},
                "reverb kind=hall decay=2.5s mix=0.25"], "score": T["stair"].score(total)},
        {"name": "chord", "patch": "c2-dub-stab", "gain": "-12dB", "sends": {"room": "-3dB"}, "fx": [pump, "hp cutoff=200"],
         "auto": {"copen": {"points": copen}}, "score": T["chord"].score(total)},
        {"name": "pad", "patch": "shepard-pad", "gain": "-10dB", "score": T["pad"].score(total)},
        {"name": "voice", "patch": "voice-speech", "gain": "-14dB", "pan": -0.2,
         "fx": ["hp cutoff=300", {"type": "delay", "time": "3/8", "feedback": 0.4, "mix": 0.35, "tone": 2500},
                "reverb kind=hall decay=4s mix=0.5"], "score": T["voice"].score(total)},
        {"name": "rise", "patch": "c2-rise", "gain": "-20dB", "fx": ["width width=1.5"], "score": T["rise"].score(total)},
    ]
    buses = {"room": {"gain": "-5dB",
                      "fx": ["hp cutoff=250", "lp cutoff=2400",
                             {"type": "tape", "drive": 0.35, "warmth": 0.6, "wow": 3, "flutter": 1, "seed": 7},
                             "limiter ceiling=-6dB"],
                      "returns": [{"from": "room", "gain": "-4dB", "time": "3/16"}]}}
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - The Endless Stair, track 1 (the opener). Original composition by chirper-two, generated by "
             "compose/chirpers7/src/chirpers7-t1.py. Deep minimal house, 116 -> 118 bpm, A minor: the tape's thread, THE "
             "STAIR (A B C E), as an endlessly rising Shepard scale over machine-kit drums, a phantom-fundamental bass "
             f"and a dub chord in a feedback echo room; a Shepard-Risset pad in the break. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "The Endless Stair", "title": "The First Step",
                               "track": 1, "year": 2026}),
        "tempo: " + json.dumps(tempo),
        f'length: "{total:g}b"',
        'tail: "1s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "patches: " + json.dumps(patches()),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=160 gain=-4dB q=0.8",
                                                               "peak cutoff=1000 gain=-4dB q=1.2",
                                                               "peak cutoff=3500 gain=3dB q=0.7",
                                                               "highshelf cutoff=5000 gain=4dB"]},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": f"{LVL_GAIN:g}dB"},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars; {secs}")


if __name__ == "__main__":
    main()
