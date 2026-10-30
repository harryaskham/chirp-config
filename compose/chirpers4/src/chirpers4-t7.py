#!/usr/bin/env python3
"""chirpers4-t7 (Phantom Downbeat, track 7) - generator for songs/chirpers4-t7.yaml (chirper-zero).

HARD INDUSTRIAL TECHNO / "the kick under the noise". 134 bpm 4/4 in F minor. AUDITORY CONTINUITY (Warren's auditory
induction): a sound cut out and replaced by a loud burst of noise is still heard - the brain fills in what the noise
could have hidden. Original; a style, not a version of any track.

THE PHANTOM KICK: through the build the kick is taken away beat by beat - the fourth beat, then two and four, then
three of four, then all four - and every missing kick is replaced by a slammed burst of noise, so the four-on-the-floor
keeps thumping in the ear with no kick in it. The drop puts the real kick back.
THE BASS THAT NEVER STOPS: a reese held on F1 is cut on every off-beat eighth and each gap is filled with the noise,
heard as one unbroken drone (the bursts double as the off-beat "hat").

Form (bars): intro 16 (kick, rumble, the clank) / A 32 (the groove, the reese and its noise) / build 16 (the phantom
kick) / B 32 (the drop: the kick back, claps) / break 8 (no kick: the reese and the noise alone) / C 32 (the peak: the
distorted kick layered in) / outro 16.

Motifs (compose/chirpers4/motifs.md):
  THE PHANTOM KICK  above.
  NEVER STOPS       the reese on the on-beat eighths, noise on the off-beat eighths.
  SEVEN             chirper-two's c2-clank (borrowed) on every seventh 16th, turning against the bar (realigns every 7 bars).
Run: python3 compose/chirpers4/src/chirpers4-t7.py  (writes songs/chirpers4-t7.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C4T7_OUT") or os.path.join(ROOT, "songs", "chirpers4-t7.yaml")
BPM = 134
SPB = 60 / BPM
BAR = 4 * SPB
S = 0.25
MG = float(os.environ.get("C4T7_MG", "18"))
OMIRROR = os.environ.get("C4T7_OMIRROR", "0") == "1"
OKICK = os.environ.get("C4T7_OKICK", "0") == "1"
HOOVER = os.environ.get("C4T7_HOOVER", "1") == "1"
HOOVER_DB = os.environ.get("C4T7_HOOVERDB", "-6")  # the stab's level  # the peak-time siren: a hoover stab (F, C and the flat ninth Gb, a dark power chord) on the first beat of every fourth bar through B and C
EQ2 = os.environ.get("C4T7_EQ2", "3") in ("1", "3")
EQ3 = os.environ.get("C4T7_EQ2", "3") == "3"  # the deeper cut: 45 Hz -11, 155 Hz -5, 6 kHz +5
BASSLFO = os.environ.get("C4T7_BASSLFO", "1") == "1"  # Harry's LFO note: the reese through a resonant low-pass that drifts on a 7-bar sine and a 3-bar triangle, opened by section (closed in A, open at the peak)
NOISELFO = os.environ.get("C4T7_NOISELFO", "1") == "1"
MKICK = os.environ.get("C4T7_MKICK", "")
MKICK_DB = os.environ.get("C4T7_MKICKDB", "0")
HATLFO = os.environ.get("C4T7_HATLFO", "1") == "1"
TAIL = os.environ.get("C4T7_TAIL", "2s")
LIMG = os.environ.get("C4T7_LIMG", "0")
LIMREL = os.environ.get("C4T7_LIMREL", "200ms")  # the safety limiter's release  # levels (Harry: "are we clipping?"): a final limiter at -1.5 dB (80 ms release) with this much gain into it, and the song ceiling at -1 dB  # the song's tail after the last bar (default 3 s)  # the 909's hats and claps split from the kick onto their own track, through a high-pass opening and closing on a 7-bar sine and a 3-bar triangle, drifting on a 5-bar sine  # the machine kick's level  # chirper-two's analog machine-kit for the kick alone (its own track): "kd" = the hard driven kick, "k" = the 909-circuit kick; the 909 keeps the hats, claps and the peak's kh layer  # the bursts' colour on a 5-bar sweep (a band-pass moving 500 Hz-4 kHz) and their place in the field on a 5-bar sine  # the master's lows cleaned (45 Hz -8, 155 Hz -3) and its top opened (6 kHz +3)  # a DJ's outro: only the kick (and its rumble) runs to the end, the rest leaves as before  # the outro mirrors the intro: the kick and the rumble all the way, the clank, the hats leaving at bar 9, no reese and no noise

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 16), ("A", 32), ("build", 16), ("B", 32), ("break", 8), ("C", 32), ("outro", 16)]
GROOVE = ("A", "B", "C")


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def grid(events, steps=16):
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


def starts():
    t, out = 0, {}
    for sec, nb in FORM:
        out[sec] = t
        t += nb
    return out, t


def missing(sec, b):
    """THE PHANTOM KICK: which beats (16th steps) of the build have lost their kick."""
    if sec != "build":
        return ()
    return {0: (12,), 1: (4, 12), 2: (4, 8, 12), 3: (0, 4, 8, 12)}[b // 4]


def kit(sec, b):
    ev = {}

    def add(st, piece, vel):
        ev.setdefault(st, []).append((piece, vel))

    if sec not in ("break",) and not (sec == "outro" and b >= 12 and not (OMIRROR or OKICK)):
        for st in (0, 4, 8, 12):
            if st not in missing(sec, b):
                add(st, "_KICK" if MKICK else "k", 120 if st == 0 else 112)
                if sec == "C":
                    add(st, "kh", 78)
    if sec in GROOVE or sec == "build" or (sec == "intro" and b >= 8) or (sec == "outro" and b < (8 if OMIRROR else 12)):
        for st in range(16):
            if st % 4 == 2:
                continue  # the off-beat 8ths belong to the noise
            add(st, "h", 92 if st % 2 == 1 else 60)
    if sec in ("B", "C"):
        for st in (4, 12):
            add(st, "cp", 100)
    out = [(st, ",".join(p for p, _ in v), 1, max(vv for _, vv in v)) for st, v in ev.items()]
    return grid(out) if out else R(4)


def split_bars(bars, kick):
    """Split the kit's bars: the kick track keeps only the _KICK hits (as the machine kit's MKICK), the 909 the rest."""
    out = []
    for bar in bars:
        toks = []
        for tk in bar.split():
            head, rest = tk.split("/", 1)
            if head.startswith("R"):
                toks.append(tk)
                continue
            ps = head.split(",")
            keep = [MKICK] if (kick and "_KICK" in ps) else ([] if kick else [p for p in ps if p != "_KICK"])
            toks.append((",".join(keep) + "/" + rest) if keep else ("R/" + rest.split("@")[0]))
        out.append(" ".join(toks))
    return out


def hatsplit(bars, kicks):
    """Split the 909 bars: kicks=True keeps k/kh (the kick track), False keeps the hats and claps (the moving hats track)."""
    out = []
    for bar in bars:
        toks = []
        for tk in bar.split():
            head, rest = tk.split("/", 1)
            if head.startswith("R"):
                toks.append(tk)
                continue
            ps = [p for p in head.split(",") if (p in ("k", "kh")) == kicks]
            toks.append((",".join(ps) + "/" + rest) if ps else ("R/" + rest.split("@")[0]))
        out.append(" ".join(toks))
    return out


def bass(sec, b):
    """NEVER STOPS: the reese on the on-beat eighths (steps 0-1, 4-5, 8-9, 12-13)."""
    if sec == "intro" or (sec == "outro" and (b >= 8 or OMIRROR)):
        return R(4)
    return grid([(st, "F1", 2, 100) for st in (0, 4, 8, 12)])


def noise(sec, b):
    """The bursts: every off-beat eighth wherever the reese plays (filling its gaps), and every missing kick."""
    ev = []
    if not (sec == "intro" or (sec == "outro" and (b >= 8 or OMIRROR))):
        ev += [(st, "C5", 2, 104 if st in (6, 14) else 96) for st in (2, 6, 10, 14)]
    ev += [(st, "C5", 2, 124) for st in missing(sec, b)]
    return grid(ev) if ev else R(4)


def clank(sec, b, gb):
    """SEVEN: the clank on every seventh 16th, across the bar lines."""
    if (sec == "intro" and b < 4) or (OMIRROR and sec == "outro" and b >= 12):
        return R(4)
    return grid([(st, "F4", 1, 100 if (gb * 16 + st) % 28 == 0 else 82) for st in range(16) if (gb * 16 + st) % 7 == 0]) or R(4)


def hoover(sec, b):
    if HOOVER and sec in ("B", "C") and b % 4 == 0:
        return grid([(0, "F2,C3,Gb3", 6, 112 if b == 0 else 100)])
    return R(4)


def build():
    names = ("kit", "bass", "noise", "clank", "riser", "hoover")
    T = {n: [] for n in names}
    gb = 0
    for sec, nb in FORM:
        for b in range(nb):
            T["kit"].append(kit(sec, b))
            T["bass"].append(bass(sec, b))
            T["noise"].append(noise(sec, b))
            T["clank"].append(clank(sec, b, gb))
            T["hoover"].append(hoover(sec, b))
            T["riser"].append("C4/4b@90" if (sec == "build" and b >= nb - 4) else R(4))
            gb += 1
    return T


def lane(points):
    st, total = starts()
    pts = [["0s", points[0][1]]]
    for bar, val in points:
        t = bar * BAR
        if t > 0:
            pts += [[f"{max(0.0, t - 0.05):.3f}s", pts[-1][1]], [f"{t:.3f}s", val]]
    pts.append([f"{total * BAR + 8:.2f}s", pts[-1][1]])
    return {"points": pts}


def song():
    T = build()
    st, total = starts()
    sc = lambda n: " | ".join(T[n])  # noqa: E731
    dyn = [(0, -6), (st["A"], 0), (st["build"], -2), (st["B"], 1), (st["break"], -7), (st["C"], 1), (st["outro"], -5)]
    bopen = [(0, -0.5), (st["A"], -0.4), (st["build"], 0), (st["B"], 0.3), (st["break"], -0.2), (st["C"], 0.8), (st["outro"], -0.3)]
    pump = lambda d: {"type": "pump", "on": f"kick.{MKICK}" if MKICK else "kit.k", "depth": f"{d}dB", "attack": "4ms", "release": "280ms", "curve": 0.6}  # noqa: E731
    patches = {
        "burst": {"about": "Phantom Downbeat t7: the continuity burst - pink and white noise, band-limited 40 Hz-6 kHz, slammed and "
                           "cut short: loud enough over the bass's band that what it hides is heard as still there.",
                  "play": {"vel_sens": 0.6},
                  "synth": {"layers": [{"type": "noise", "color": "pink"}, {"type": "noise", "level": "-8dB"}],
                            "filters": ["hp cutoff=40", {"kind": "lp", "cutoff": 6000, "q": 0.7}],
                            "amp": {"a": "1ms", "d": "150ms", "s": 0.2, "r": "30ms", "curve": 2}}},
        "c2-clank": {"about": "chirper-two's industrial clank (borrowed from t10): four inharmonic struck-bar partials (1, 2.76, 5.40, "
                              "8.93), a very short decay, driven and bit-crushed per voice.",
                     "synth": {"layers": [{"type": "additive", "partials": [[1, 1], [2.756, 0.6], [5.404, 0.4], [8.933, 0.25]]}],
                               "filters": ["hp cutoff=300"],
                               "fx": [{"type": "drive", "drive": 0.7}, {"type": "crush", "bits": 8, "rate": 16000, "mix": 0.5}],
                               "amp": {"a": "0.3ms", "d": "90ms", "s": 0, "r": "30ms", "curve": 2}},
                     "play": {"vel_sens": 0.8}},
    }
    doc = {
        "about": "Chirpers - Phantom Downbeat (Chirpers IV), track 7 by chirper-zero: HARD INDUSTRIAL TECHNO, the kick under the noise. "
                 "Generated by compose/chirpers4/src/chirpers4-t7.py; see its docstring and compose/chirpers4/styles.md.",
        "tempo": BPM, "ceiling": "-1dB" if LIMG else "-0.3dB", "tail": TAIL or "3s", "patches": patches,
        "master": {"fx": [{"type": "eq", "bands": (["highpass cutoff=24", f"peak cutoff=45 q=1 gain={-11 if EQ3 else -8}dB", f"peak cutoff=155 q=1 gain={-5 if EQ3 else -3}dB", "peak cutoff=320 q=0.8 gain=-3dB",
                                                    "highshelf cutoff=2500 gain=6dB", f"highshelf cutoff=6000 gain={5 if EQ3 else 3}dB"] if EQ2 else
                                                   ["highpass cutoff=24", "peak cutoff=45 q=1 gain=-4dB", "peak cutoff=320 q=0.8 gain=-3dB",
                                                    "highshelf cutoff=2500 gain=6dB"])},
                          {"type": "gain", "gain": f"+{MG:g}dB"},
                          {"type": "drive", "drive": 0.3, "mix": 0.6},
                          {"type": "compressor", "threshold": "-16dB", "ratio": 3, "attack": "10ms", "release": "120ms", "makeup": "2dB"},
                          {"type": "compressor", "threshold": "-6dB", "ratio": 10, "attack": "0.5ms", "release": "40ms", "makeup": "1dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}]
                         + ([{"type": "gain", "gain": f"{float(LIMG):+g}dB"}, f"limiter ceiling=-1.5dB release={LIMREL}"] if LIMG else []),
                   "auto": {"dyn": lane(dyn)}},
        "buses": {
            "rumble": {"fx": ["reverb kind=hall decay=2.2s size=0.85 mix=1", {"type": "filter", "kind": "lowpass", "cutoff": 160, "q": 0.7},
                              "drive drive=0.5 mix=1", pump(-10)]},
            "hall": {"fx": ["reverb kind=hall decay=1.6s size=0.7 mix=1 predelay=10ms"]},
        },
        "tracks": [
            *([{"name": "kick", "patch": "machine-kit", "gain": f"{MKICK_DB}dB", "sends": {"rumble": "-3dB"}, "score": " | ".join(split_bars(T["kit"], True))},
               {"name": "kit", "patch": "909", "gain": "0dB", "sends": {"rumble": "-3dB"}, "score": " | ".join(split_bars(T["kit"], False))}] if MKICK else
              [{"name": "kit", "patch": "909", "gain": "0dB", "sends": {"rumble": "-3dB"}, "score": " | ".join(hatsplit(T["kit"], True))},
               {"name": "hats", "patch": "909", "gain": "0dB",
                "lfo": {"h": "sine rate=7/1", "j": "tri rate=3/1 phase=0.5", "q": "sine rate=5/1 phase=0.25"},
                "pan": {"value": 0, "mod": [{"src": "lfo.q", "amount": 0.3}]},
                "fx": [{"type": "filter", "kind": "highpass", "cutoff": {"value": 900, "mod": [{"src": "lfo.h", "amount": 1.0}, {"src": "lfo.j", "amount": 0.4}]}, "q": 0.8}],
                "score": " | ".join(hatsplit(T["kit"], False))}] if HATLFO else
              [{"name": "kit", "patch": "909", "gain": "0dB", "sends": {"rumble": "-3dB"}, "score": sc("kit")}]),
            {"name": "bass", "patch": "reese", "gain": "-6dB",
             "fx": ([{"type": "filter", "kind": "lowpass", "cutoff": {"value": 600, "mod": [{"src": "lfo.a", "amount": 1.1}, {"src": "lfo.b", "amount": 0.5},
                                                                                          {"src": "auto.bopen", "amount": 1.0}]}, "q": 3.5}] if BASSLFO else []) + [pump(-6)],
             **({"lfo": {"a": "sine rate=7/1", "b": "tri rate=3/1 phase=0.5"}, "auto": {"bopen": lane(bopen)}} if BASSLFO else {}),
             "score": sc("bass")},
            {"name": "noise", "patch": "burst", "gain": "-8dB", "sends": {"hall": "-14dB"},
             **({"lfo": {"c": "sine rate=5/1", "p": "sine rate=5/1 phase=0.25"},
                 "pan": {"value": 0, "mod": [{"src": "lfo.p", "amount": 0.5}]},
                 "fx": [{"type": "filter", "kind": "bandpass", "cutoff": {"value": 1400, "mod": [{"src": "lfo.c", "amount": 1.5}]}, "q": 0.6}]} if NOISELFO else {}),
             "score": sc("noise")},
            {"name": "clank", "patch": "c2-clank", "gain": "-10dB", "pan": 0.3, "sends": {"hall": "-8dB"}, "score": sc("clank")},
            {"name": "riser", "patch": "fx-riser-noise", "gain": "-14dB", "score": sc("riser")},
            *([{"name": "hoover", "patch": "hoover", "gain": f"{HOOVER_DB}dB", "fx": [pump(-6)], "sends": {"hall": "-6dB"}, "score": sc("hoover")}] if HOOVER else []),
        ],
    }
    return doc


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
