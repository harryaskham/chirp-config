#!/usr/bin/env python3
"""chirpers5-t6 (Soft Concrete, track 6). Composed by chirper-two: SOULFUL LIQUID ROLLER.

"Overpass Rain". The album's heart: rolling liquid drum & bass where euphoria and melancholy sit together.
- THE CHORDS: Rhodes ninths (epiano-tine with its damper) sinking through Fm9 | Dbmaj9 | Bbm9 | C7sus(b9), two bars
  each, comped in a 2-step rhythm; a high Juno pad holds them from the first drop on.
- THE ROLLER: wM's amen-chops re-sequenced into a liquid roller (the downbeat kick, ghosts, the snare on 2, the
  double kick on the and-of-3, the snare on 4), its ghost slices re-pitched; a clean break-kit kick and snare under it.
- THE HOOK: the voice engine hums a falling five-note hook (a shadow song, never played whole), and a sampler chops
  it into one-beat slices that answer the Rhodes, each slice somewhere new in the stereo field.
- THE LOW END: a sub on the roots in the same 2-step; the reese only in the second drop, warm and low-passed.
- THE WEATHER: the rain we are sheltering from (chirper-two's rain droplets from Tape Weather), thick in the intro, the
  break and the outro.
- THE SEAMS: a stutter roll (wM: repeats shortening 1/8 -> 1/64, rising) only on the last bar into each drop.
Form (bars of 4/4, 174 bpm): intro 16 / drop A 32 / break 16 / build 8 / drop B 32 / outro 16 = 120 bars, ~166 s.

Emits songs/chirpers5-t6.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers5-t6.yaml")
BPM = 174
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


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


LVL_GAIN = 7  # dB into the master's peak compressor and limiter (levels.py: TP under -1 dBTP, no flat runs)
DRUM_CLIP = -11  # the drum bus's soft clip: shaves the break's spikes
PEAK_T = -5  # the master's fast peak compressor (smooth, so nothing is pinned)
FORM = [("intro", 16), ("A", 32), ("break", 16), ("build", 8), ("B", 32), ("outro", 16)]
# (bass root, Rhodes voicing), two bars each
CHORDS = [(41, [56, 60, 63, 67]),   # Fm9: F2 | Ab3 C4 Eb4 G4
          (37, [53, 56, 60, 63]),   # Dbmaj9: Db2 | F3 Ab3 C4 Eb4
          (34, [56, 60, 61, 65]),   # Bbm9: Bb1 | Ab3 C4 Db4 F4
          (36, [58, 61, 65, 67])]   # C7sus(b9): C2 | Bb3 Db4 F4 G4
COMP = [(0.0, 1.4, 0), (1.75, 0.6, -14), (3.5, 1.0, -6), (5.0, 0.45, -16), (6.5, 1.4, -8)]  # a 2-bar 2-step comp
# the roller, one bar of eighth-note amen slices: (beat, slice, velocity offset, tune)
ROLL_A = [(0.0, 0, 0, 0), (0.5, 3, -18, 0), (1.0, 2, 0, 0), (1.5, 7, -16, 0),
          (2.0, 4, -20, 0), (2.5, 5, -4, 0), (3.0, 2, -2, 0), (3.5, 6, -16, 0)]
ROLL_B = [(0.0, 0, 0, 0), (0.5, 3, -18, 0), (1.0, 2, 0, 0), (1.5, 7, -16, 0),
          (2.0, 4, -20, 2), (2.5, 5, -4, 0), (3.0, 2, -2, 0), (3.5, 15, -10, 0), (3.75, 6, -18, 5)]
HOOK = "C5/1b@84^u Ab4/1b@78^u G4/1.5b@80^o Eb4/0.5b@70^o F4/4b@86"  # the hummed sigh, 8 beats (oo, oo, oh, oh, ah)
VOX_ANSWER = [(0.5, 0, -2), (1.25, 1, -10), (2.0, 2, -4), (3.0, 4, -8)]  # (beat, slice, vel offset)


def build():
    rng = random.Random(6)
    wrng = random.Random(66)  # the weather's own dice
    T = {k: Track(k) for k in ("rhodes", "pad", "amen", "kick", "snare", "sub", "body", "reese", "vox", "voxlong",
                               "rain")}
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    for bi, (start, sec, i, n) in enumerate(bars):
        root, voic = CHORDS[(i // 2) % 4]
        drop = sec in ("A", "B")
        # ---- Rhodes: the 2-step comp, from the intro's fifth bar ----
        if i % 2 == 0 and not (sec == "intro" and i < 4) and not (sec == "outro" and i >= 12):
            for o, ln, dv in COMP:
                v = (72 if sec in ("intro", "break", "outro") else 80) + dv
                T["rhodes"].add(start + o + 0.02, ln, ",".join(nm(x) for x in voic), v)
        # ---- the pad: held, high, from the first drop ----
        if i % 2 == 0 and sec in ("A", "break", "build", "B"):
            T["pad"].add(start, 7.9, ",".join(nm(x + 12) for x in voic[1:]), 60)
        # ---- the roller ----
        if drop or (sec == "intro" and i >= 8) or sec == "build" or (sec == "outro" and i < 8):
            pat = ROLL_B if i % 4 == 3 else ROLL_A
            soft = sec == "intro" or sec == "outro"
            for b, sl, dv, tune in pat:
                if sec == "build" and i < 4 and b not in (0.0, 1.0, 2.5, 3.0):
                    continue  # the build starts bare
                T["amen"].add(start + b, 0.5, nm(36 + sl), 100 + dv - (12 if soft else 0),
                              f"^tune={tune}" if tune else "")
            if drop or sec == "build":
                for b in (0.0, 2.5):
                    T["kick"].add(start + b, 0.5, "k", 104 if b == 0 else 96)
                for b in (1.0, 3.0):
                    T["snare"].add(start + b, 0.5, "s", 98)
        # ---- the low end ----
        if drop or sec == "build":
            r = root - 12 if root >= 36 else root  # the sub: F1 Db1 Bb1 C1
            T["sub"].add(start, 1.6, nm(r), 104)
            T["sub"].add(start + 2.5, 1.3, nm(r), 96)
            if i % 2 == 1:
                T["sub"].add(start + 3.75, 0.25, nm(r + 12), 84)
            if sec == "B" and i % 2 == 0:
                T["reese"].add(start, 7.8, nm(r + 12), 90)
        # ---- the hook: whole in the intro and the break, chopped in the drops ----
        if (sec == "intro" and i in (8, 12)) or (sec == "break" and i % 4 == 0) or (sec == "outro" and i in (4, 8)):
            T["voxlong"].add(start, 8.0, "C4", 92)
        if drop and i % 4 in (1, 3):
            for b, sl, dv in VOX_ANSWER:
                T["vox"].add(start + b + 0.02, 0.95, nm(60 + sl), 96 + dv)
        # ---- the rain ----
        heavy = sec in ("intro", "break", "outro")
        for _ in range(wrng.randint(14, 20) if heavy else wrng.randint(3, 6)):
            T["rain"].add(start + wrng.uniform(0, 3.97), 0.05, "C5", wrng.randint(20, 66 if heavy else 40))
    sec = []
    for name, n in FORM:
        first = next(bb for bb in bars if bb[1] == name)
        sec.append((name, first[0], n))
    return total, bars, sec, T


def patches():
    return {
        "c2-rain": {"about": "chirper-two's rain: a droplet of band-passed noise (8 ms), scattered at random.",
                    "synth": {"layers": [{"name": "drop", "type": "noise"}],
                              "filters": ["hp cutoff=900", "lp cutoff=5500"],
                              "amp": {"a": "0.3ms", "d": "9ms", "s": 0, "r": "6ms", "curve": 2}},
                    "play": {"vel_sens": 1.0}},
        "c2-hook-chop": {"about": "chirper-two: the shadow song `hook` (the voice engine humming t6's hook) in eight "
                                  "one-beat slices (C4 slice 1 ... G4 slice 8), each slice panned by its own random value.",
                         "synth": {"layers": [{"type": "sample", "song": "hook", "root": "C4", "slices": 8}],
                                   "fx": [{"type": "pan", "pan": {"value": 0, "mod": [{"src": "rand", "amount": 0.7}]}}],
                                   "amp": {"a": "4ms", "d": "0s", "s": 1, "r": "60ms"}}},
        "c2-hook": {"about": "chirper-two: the shadow song `hook`, whole.",
                    "synth": {"layers": [{"type": "sample", "song": "hook", "root": "C4"}],
                              "amp": {"a": "10ms", "d": "0s", "s": 1, "r": "300ms"}}},
    }


def hook_song():
    """A shadow source: the voice engine humming the hook (rendered inside this song, never played)."""
    return {"tempo": BPM, "length": "8b", "tail": "0.3s",
            "tracks": [{"name": "hum", "patch": "voice", "gain": "-2dB",
                        "fx": [{"type": "chorus", "rate": 0.4, "depth": 0.35, "voices": 1, "mix": 0.6},
                               "lp cutoff=5000"], "score": HOOK}]}


def main():
    total, bars, sec, T = build()
    st = {n: s for n, s, k in sec}
    roll = [["0b", 0.0], [f"{st['break'] - 4}b", 0.0], [f"{st['break'] - 4 + 0.01}b", 1.0], [f"{st['break']}b", 1.0],
            [f"{st['break'] + 0.01}b", 0.0], [f"{st['B'] - 4}b", 0.0], [f"{st['B'] - 4 + 0.01}b", 1.0],
            [f"{st['B']}b", 1.0], [f"{st['B'] + 0.01}b", 0.0]]
    rhodes = "epiano-tine synth.tine.sense=0.4 play.release.patch=epiano-damper play.release.decay=2s"
    tracks = [
        {"name": "rhodes", "patch": rhodes, "gain": "-4dB", "pan": -0.1,
         "fx": [{"type": "chorus", "rate": 0.6, "depth": 0.35, "voices": 2, "mix": 0.45},
                "tape drive=0.25 warmth=0.6", "peak cutoff=300 gain=-3dB q=0.8", "hp cutoff=120",
                "reverb kind=hall decay=2.4s mix=0.25"],
         "score": T["rhodes"].score(total)},
        {"name": "pad", "patch": "juno-pad", "gain": "-16dB", "fx": ["hp cutoff=300"], "score": T["pad"].score(total)},
        {"name": "amen", "patch": "amen-chops", "gain": "-5dB",
         "fx": ["hp cutoff=60",
                {"type": "stutter", "slice": "1/8", "repeats": 8, "roll": 0.5, "pitch": 1,
                 "chance": {"value": 0, "mod": [{"src": "auto.roll", "amount": 1}]}},
                "reverb kind=room decay=0.5s mix=0.1"],
         "auto": {"roll": {"points": roll}}, "score": T["amen"].score(total)},
        {"name": "kick", "patch": "break-kit", "gain": "-6dB", "fx": ["lp cutoff=3000"], "score": T["kick"].score(total)},
        {"name": "snare", "patch": "break-kit", "gain": "-9dB", "score": T["snare"].score(total)},
        {"name": "sub", "patch": "sub-sine", "gain": "-4dB",
         "fx": [{"type": "pump", "on": "kick.k", "depth": "-6dB", "attack": "2ms", "release": "150ms", "curve": 0.8}],
         "score": T["sub"].score(total)},
        {"name": "reese", "patch": "reese", "gain": "-16dB", "fx": ["lp cutoff=700", "hp cutoff=80"],
         "score": T["reese"].score(total)},
        {"name": "hook", "patch": "c2-hook", "gain": "-6dB", "pan": 0.1,
         "fx": ["hp cutoff=200", "reverb kind=hall decay=3.5s mix=0.4"], "score": T["voxlong"].score(total)},
        {"name": "hook-chops", "patch": "c2-hook-chop", "gain": "-5dB",
         "fx": ["hp cutoff=200", {"type": "delay", "time": "3/16", "feedback": 0.3, "mix": 0.2, "ping_pong": True,
                                   "tone": 3000}, "reverb kind=plate decay=1.6s mix=0.22"],
         "score": T["vox"].score(total)},
        {"name": "rain", "patch": "c2-rain", "pan": -0.15, "gain": "-20dB",
         "fx": ["reverb kind=room decay=0.6s mix=0.25", "width width=1.6"], "score": T["rain"].score(total)},
    ]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "3ms", "release": "230ms", "curve": 0.8}
    for tr in tracks:  # the break, the kick and the snare go through one drum bus (a fast compressor: punch, not peaks)
        if tr["name"] in ("amen", "kick", "snare"):
            tr["out"] = "drums"
    for tr in tracks:  # the Rhodes, the pad and the reese breathe with the kick (release ~2/3 beat)
        if tr["name"] in ("rhodes", "pad", "reese"):
            tr["fx"] = [pump] + tr["fx"]
    secs = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in sec)
    about = ("Chirpers - Soft Concrete, track 6. Original composition by chirper-two, generated by "
             "compose/chirpers5/src/chirpers5-t6.py. A soulful liquid drum & bass roller at 174 bpm in F minor: "
             "Rhodes ninths through Fm9 Dbmaj9 Bbm9 C7sus(b9), a re-sequenced amen over a clean 2-step kick and snare, "
             "a sub on the roots and a reese in the second drop, a hummed hook chopped to answer the chords, rain. "
             f"Sections: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Soft Concrete", "title": "Overpass Rain",
                               "track": 6, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "2s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "patches: " + json.dumps(patches()),
        "songs: " + json.dumps({"hook": hook_song()}),
        "buses: " + json.dumps({"drums": {"gain": "0dB", "fx": [
            {"type": "compressor", "threshold": "-16dB", "ratio": 4, "attack": "1ms", "release": "70ms",
             "makeup": "2dB"},
            f"clip ceiling={DRUM_CLIP:g}dB knee=0.7 link=true"]}}),
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25"]},
                                        "glue threshold=-22dB ratio=2.5 attack=10ms release=150ms makeup=1dB",
                                        "tape drive=0.2 warmth=0.4",
                                        {"type": "gain", "gain": f"{LVL_GAIN:g}dB"},
                                        {"type": "compressor", "threshold": f"{PEAK_T:g}dB", "ratio": 10,
                                         "attack": "0.3ms", "release": "60ms", "makeup": "0dB"},
                                        "limiter ceiling=-1.5dB release=80ms"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(bars)} bars, {total / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
