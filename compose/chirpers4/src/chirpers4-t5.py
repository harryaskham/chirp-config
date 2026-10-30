#!/usr/bin/env python3
"""chirpers4-t5 (Phantom Downbeat, track 5). Composed by chirper-two: HYPNOTIC DRIVING TECHNO.

"The Room Turns". No Floor's drive in another style (no acid): few parts, and the motion is the hypnosis.
- THE ORBITS (a space illusion): the rim, the clap, the ride and the cowbell circle the listener. Each pans on a
  slow song-time LFO while a second LFO a quarter-cycle behind it darkens, quiets and wets the voice as it passes
  "behind" you, so it is heard going round, not side to side. The rim orbits every 3 bars, the clap every 5, the
  ride every 7, the cowbell every 5 on the far side of the clap.
- THE MACHINE: chirper-two's analog drum-machine voices (machine-kit): the rumble kick on every beat, the hard
  kick layered on the ones at the peaks, multi-burst claps, metallic hats.
- THE BOOM BASS: the machine's 808 boom played as a bass line (tuned per note, short, driven), galloping on every
  off-beat (the and, then the a), pumped by the kick.
- THE STAB: a short D minor (add 9) stab whose band-pass breathes on a 5-bar LFO, thrown into a dotted echo.
- THE TURN: in the break the kick thins and the orbits speed up to a bar a turn; THE STOP: for eight bars the kick
  and the hats drop out and every orbiting voice is dry and dead centre, right at your ear, over the bass: the room
  standing still. Then it TURNS BACK, the other way round, for the peak.
Form (bars of 4/4, 134 bpm): intro 16 / A 32 / turn 16 / B 32 / stop 8 / C 32 / outro 16 = 152 bars, ~272 s.

Emits songs/chirpers4-t5.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T5_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers4-t5.yaml")
BPM = 134
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel)))))

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
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            toks.append(f"{head}/{ln:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


FORM = [("intro", 16), ("A", 32), ("turn", 16), ("B", 32), ("stop", 8), ("C", 32), ("outro", 16)]
S16 = 0.25
STAB = [50, 53, 57, 64]          # D3 F3 A3 E4: D minor add 9
BASS = [38, 38, 38, 41, 38, 38, 45, 43]  # D2 ... F2 ... A2 G2: the boom bass, one note per beat, two bars
# Round 2 (v2), polish (Harry: patient entries, better LFO motion, don't overcook): W = THE ENTRIES WAIT: the stab
# approaches from far off through A's first sixteen bars (from a whisper to its full strength) instead of arriving
# at once, the hard kick waits for the second half of B, and the cowbell comes only in B's second half and then
# every fourth bar; B = THE BASS BREATHES: a low-pass on the boom bass opens and closes on a 9-bar LFO (its own odd
# cycle against the orbits' 3, 5 and 7), so its driven harmonics swell and recede. (Tried: holding the stab back
# entirely, and leaning the hats' off-sixteenths late; both cost the groove its syncopation.)
R2 = set(filter(None, os.environ.get("T5_R2", "W,B").split(","))) - {"none"}
# Round 3 (v3), polish: Z = THE ROOM HOLDS ITS ECHO: at THE STOP the hall the orbiting voices were turning in
# freezes (wM's reverb freeze on the room bus): the last turn's echo hangs in the air as a still chord of metal while
# the voices stand dry and dead centre at your ear; it lets go when the room turns back. (Tried: four or eight bars of
# the room before the kick at the start; it made the opening a twin of the break: recurrence share 0.8, 51.)
R3 = set(filter(None, os.environ.get("T5_R3", "Z").split(","))) - {"none"}
# the orbiting voices: (kit piece, orbit period in bars, phase)
ORBITS = {"rim": ("rs", 3, 0.0), "clap": ("cp", 5, 0.0), "ride": ("rd", 7, 0.25), "bell": ("cb", 5, 0.5)}


def mode_of(sec):
    """How the room moves in a section: cw (clockwise), fast, still or ccw."""
    return {"turn": "fast", "stop": "still", "C": "ccw", "outro": "ccw"}.get(sec, "cw")


def build():
    rng = random.Random(5)
    names = ["kick", "kickhard", "hats", "bass", "stab", "air"] + \
        [f"{o}-{m}" for o in ORBITS for m in ("cw", "fast", "still", "ccw")]
    T = {k: Track(k) for k in names}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    for bi, (start, sec, i, n) in enumerate(bars):
        mode = mode_of(sec)
        full = sec in ("A", "B", "C") or (sec == "intro" and i >= 8) or (sec == "outro" and i < 8)
        # ---- the kick: every beat, but for the turn (a heartbeat) ----
        if sec == "turn":
            if i % 2 == 0 and i < 12:
                T["kick"].add(start, 1.0, "kr", 104)
        elif not (sec == "outro" and i >= 12) and sec != "stop":
            for b in range(4):
                T["kick"].add(start + b, 1.0, "kr", 116 if b == 0 else 108)
        if sec == "C" or (sec == "B" and not ("W" in R2 and i < 16)):
            for b in (range(4) if sec == "C" and i >= 16 else (0,)):
                T["kickhard"].add(start + b, 0.5, "kd", 100 if b == 0 else 88)
        # ---- hats: sixteenths, the off-eighth leaning; an open hat on the off-beat ----
        if (sec != "turn" or i >= 8) and sec != "stop":
            for s in range(16):
                if sec == "intro" and i < 4 and s % 2 == 0:
                    continue
                v = (78 if s % 4 == 2 else 52 if s % 2 else 62) + rng.randint(-4, 4)
                T["hats"].add(start + s * S16 + (0.008 if s % 2 else 0.0), 0.12, "h", v - (14 if sec == "turn" else 0))
            if full:
                for b in (0.5, 1.5, 2.5, 3.5):
                    T["hats"].add(start + b + 0.01, 0.4, "oh", 74)
        # ---- the orbiting voices ----
        o = f"-{mode}"
        T["rim" + o].add(start + 0.75, 0.2, "rs", 92)
        T["rim" + o].add(start + 1.5, 0.2, "rs", 78)
        T["rim" + o].add(start + 2.75, 0.2, "rs", 86)
        if i % 2 == 1:
            T["rim" + o].add(start + 3.5, 0.2, "rs", 74)
        if sec in ("A", "B", "stop", "C") or (sec == "outro" and i < 8) or (sec == "turn" and i >= 8):
            for b in (1.0, 3.0):
                T["clap" + o].add(start + b + 0.004, 0.5, "cp", 104)
            if sec == "C" and i % 4 == 3:
                T["clap" + o].add(start + 3.75, 0.5, "cpw", 84)
        if sec in ("B", "stop", "C"):
            for b in (0.5, 1.5, 2.5, 3.5):
                T["ride" + o].add(start + b + 0.015, 0.5, "rd", 76)
            bell = (i % 2 == 1) if "W" not in R2 else (i % 4 == 3 and not (sec == "B" and i < 16))
            if bell:
                T["bell" + o].add(start + 1.75, 0.3, "cb", 88)
                T["bell" + o].add(start + 2.5, 0.3, "cb", 76)
        # ---- the boom bass: a gallop on each off-beat (the and, then the a), pumped ----
        if full or sec in ("stop",):
            for k, b in enumerate((0.5, 1.5, 2.5, 3.5)):
                note = BASS[(bi % 2) * 4 + k]
                T["bass"].add(start + b, 0.22, nm(note), 108 if k % 2 == 0 else 98)
                if not (i % 4 == 3 and k == 3):
                    T["bass"].add(start + b + 0.25, 0.2, nm(note), 84)
            if i % 4 == 3:
                T["bass"].add(start + 3.75, 0.2, nm(50), 92)  # a pickup an octave up
        # ---- the stab: on the a-of-1 and the and-of-3, breathing ----
        if sec in ("A", "B", "C", "turn") or (sec == "outro" and i < 8):
            chord = ",".join(nm(x) for x in STAB)
            far = 1.0 if not ("W" in R2 and sec == "A" and i < 16) else 0.35 + 0.65 * i / 16  # it approaches
            T["stab"].add(start + 0.75, 0.2, chord, int(96 * far))
            T["stab"].add(start + 2.5, 0.2, chord, int(84 * far))
            if i % 2 == 1:
                T["stab"].add(start + 3.25, 0.2, chord, int(78 * far))
        # ---- air: a noise wash in the intro, the turn and the outro ----
        if sec in ("intro", "turn", "outro") and i % 8 == 0:
            T["air"].add(start, 32.0, "C4", 80)
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    return {
        "c2-boom-bass": {"about": "chirper-two: the machine layer's 808 boom played as a bass line (tuned per note), "
                                  "short and driven.",
                         "synth": {"layers": [{"type": "machine", "machine": {"part": "boom", "decay": "420ms",
                                                                               "punch": 3, "drive": 0.35,
                                                                               "click": 0.1}}],
                                   "amp": {"a": "0.1ms", "d": "0s", "s": 1, "r": "120ms"}},
                         "play": {"mono": True, "vel_sens": 0.5}},
        "c2-hypno-stab": {"about": "chirper-two: a short two-oscillator stab through a band-pass whose centre "
                                   "follows a per-note envelope, the track's 5-bar LFO `s` and its `hopen` lane.",
                          "synth": {"layers": [{"wave": "square", "detune": -6},
                                               {"wave": "saw", "detune": 6, "level": "-4dB"}],
                                    "filters": [{"kind": "bp", "q": 2.5,
                                                 "cutoff": {"value": 800, "mod": [{"src": "env.f", "amount": 1.5},
                                                                                  {"src": "lfo.s", "amount": 1.2},
                                                                                  {"src": "auto.hopen", "amount": 1.0}]}}],
                                    "env": {"f": {"a": "1ms", "d": "120ms", "s": 0.0}},
                                    "amp": {"a": "1ms", "d": "240ms", "s": 0.0, "r": "80ms"}},
                          "play": {"vel_sens": 0.6}},
        "c2-air": {"about": "chirper-two: an airy noise wash through a band-pass breathing on the track's LFO `w`.",
                   "synth": {"layers": [{"type": "noise"}],
                             "filters": [{"kind": "bp", "q": 1.2,
                                          "cutoff": {"value": 2500, "mod": [{"src": "lfo.w", "amount": 1.5}]}}],
                             "amp": {"a": "4s", "d": "1s", "s": 0.9, "r": "4s"}}},
    }


def orbit_track(voice, mode, piece_gain, score, period, phase):
    """An orbiting voice: pan on lfo.x; lfo.y (a quarter-cycle behind) is "in front" at +1 and "behind" at -1:
    behind is darker, quieter and wetter. ccw turns the other way (the pan's phase flipped); fast is a bar a turn;
    still is dead centre and dry."""
    name = f"{voice}-{mode}"
    if mode == "still":
        return {"name": name, "patch": "machine-kit", "gain": piece_gain, "score": score,
                "fx": ["hp cutoff=120"]}
    per = 1 if mode == "fast" else period
    px = phase + (0.5 if mode == "ccw" else 0.0)
    return {"name": name, "patch": "machine-kit", "gain": piece_gain, "score": score,
            "lfo": {"x": f"sine rate={per}/1 phase={px % 1:g}", "y": f"sine rate={per}/1 phase={(phase + 0.25) % 1:g}"},
            "sends": {"room": "-8dB"},
            "fx": [{"type": "filter", "kind": "lp", "cutoff": {"value": 5000, "mod": [{"src": "lfo.y", "amount": 1.2}]}},
                   {"type": "gain", "gain": {"value": "-2dB", "mod": [{"src": "lfo.y", "amount": 2.5}]}},
                   {"type": "pan", "pan": {"value": 0, "mod": [{"src": "lfo.x", "amount": 0.9}]}}]}


def main():
    total, bars, sec, T = build()
    st = {n: s for n, s, k in sec}
    hopen = [["0b", 0.0], [f"{st['A']}b", 0.0], [f"{st['turn']}b", 0.6], [f"{st['B']}b", 0.4],
             [f"{st['stop']}b", 0.9], [f"{st['C']}b", 0.6], [f"{st['outro']}b", 0.8], [f"{total}b", 0.0]]
    fade = [["0b", 0.0], [f"{total - 16}b", 0.0], [f"{total}b", -30.0]]
    pump = {"type": "pump", "on": "kick.kr", "depth": "-8dB", "attack": "3ms", "release": "300ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "0dB", "score": T["kick"].score(total)},
        {"name": "kickhard", "patch": "machine-kit", "gain": "-7dB", "fx": ["hp cutoff=60"],
         "score": T["kickhard"].score(total)},
        {"name": "hats", "patch": "machine-kit", "gain": "1dB", "pan": 0.08,
         "fx": [{"type": "filter", "kind": "hp", "cutoff": {"value": 500, "mod": [{"src": "lfo.h", "amount": 0.8}]}},
                "reverb kind=room decay=0.5s mix=0.1"],
         "lfo": {"h": "sine rate=6/1"}, "score": T["hats"].score(total)},
        {"name": "bass", "patch": "c2-boom-bass", "gain": "-4dB",
         "fx": [pump, "hp cutoff=30"] + ([{"type": "filter", "kind": "lp", "q": 0.9,
                                            "cutoff": {"value": 700, "mod": [{"src": "lfo.b", "amount": 1.3}]}}]
                                          if "B" in R2 else []),
         **({"lfo": {"b": "sine rate=9/1 phase=0.75"}} if "B" in R2 else {}),
         "score": T["bass"].score(total)},
        {"name": "stab", "patch": "c2-hypno-stab", "gain": "-14dB", "pan": -0.1,
         "lfo": {"s": "sine rate=5/1 phase=0.75"},
         "fx": [pump, {"type": "delay", "time": "3/16", "feedback": 0.42, "mix": 0.3, "ping_pong": True,
                       "tone": 2600},
                "reverb kind=plate decay=1.6s mix=0.18"],
         "auto": {"hopen": {"points": hopen}}, "score": T["stab"].score(total)},
        {"name": "air", "patch": "c2-air", "gain": "-30dB", "fx": ["width width=1.6"],
         "lfo": {"w": "sine rate=7/1"}, "score": T["air"].score(total)},
    ]
    gains = {"rim": "-1dB", "clap": "0dB", "ride": "-3dB", "bell": "-6dB"}
    for voice, (piece, period, phase) in ORBITS.items():
        for mode in ("cw", "fast", "still", "ccw"):
            tr = T[f"{voice}-{mode}"]
            if tr.ev:
                tracks.append(orbit_track(voice, mode, gains[voice], tr.score(total), period, phase))
    buses = {"room": {"gain": "-2dB", "fx": [{"type": "reverb", "kind": "hall", "decay": "2.2s", "mix": 1.0,
                                              **({"freeze": {"value": 0, "mod": [{"src": "auto.frz", "amount": 1}]}}
                                                 if "Z" in R3 else {})},
                                             "lp cutoff=4000"]
                             + ([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.frz", "amount": 18}]}}]
                                if "Z" in R3 else []),
                      **({"auto": {"frz": {"points": [["0b", 0.0], [f"{st['stop']}b", 0.0], [f"{st['stop'] + 0.25}b", 1.0],
                                                      [f"{st['C'] - 0.25}b", 1.0], [f"{st['C']}b", 0.0]]}}}
                         if "Z" in R3 else {})}}
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Phantom Downbeat, track 5. Original composition by chirper-two, generated by "
             "compose/chirpers4/src/chirpers4-t5.py. Hypnotic driving techno at 134 bpm in D minor on chirper-two's "
             "analog drum-machine voices: a rumble kick, a hard kick at the peaks, a boom bass, a breathing minor stab, "
             "and percussion ORBITING the listener (pan on one slow LFO, darker, quieter and wetter behind on another a "
             f"quarter-cycle on), every 3, 5 and 7 bars; the room speeds up, stops dead, and turns back. Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Phantom Downbeat", "title": "The Room Turns",
                               "track": 5, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "2s"',
        'ceiling: "-0.3dB"',
        'volume: "6dB"',
        "patches: " + json.dumps(patches()),
        "buses: " + json.dumps(buses),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=42 gain=-6dB q=1.0",
                                                               "peak cutoff=650 gain=-2dB q=0.7",
                                                               "highshelf cutoff=6000 gain=2dB"]},
                                        "glue threshold=-18dB ratio=2 attack=10ms release=150ms makeup=2dB",
                                        "tape drive=0.25 warmth=0.4",
                                        {"type": "gain", "gain": {"value": "0dB",
                                                                  "mod": [{"src": "auto.fade", "amount": 1}]}}],
                                 "auto": {"fade": {"points": fade}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
