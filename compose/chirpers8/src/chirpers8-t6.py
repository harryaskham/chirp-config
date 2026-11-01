#!/usr/bin/env python3
"""chirpers8-t6 (chirpers VIII, track 6). Composed by chirper-two: SLOW VOCODER ELECTRO-SOUL in 19-EDO.

"No Errors Since". A machine's status lines, said in a human voice, become a love song. Nothing in the words says so:
"everything is where you left it", "the fan is still turning", "all checks passed", "I counted every second", and the
chorus, "no errors since", said four times until it is sung. Affection as a status report.
- THE VOICE is chirp's realistic speech (`chirp tts --humanize 0.6`, lifted from src/t6/*.json): spoken in the
  verses; SPEECH TO SONG in the choruses (--repeat 4 --melodize 1) with every sung pitch rounded onto 19-EDO, so the
  tune lands a little beside the piano's notes; through a RADIO whose dial drifts in the intro and the outro ("still
  here", six times, spoken to sung, tuning away); RING-MODULATED and GRAINED (cloud) in the bridge.
- THE TALKBOX: a saw pad plays the chords and the voice shapes it band by band (`vocoder` with `key: voice`), so the
  harmony speaks the words with the voice: a choir of the machine, in tune with nothing but itself.
- THE HARMONY is a MARKOV CHAIN over 19-EDO chords (19 equal steps to the octave: thirds near-just, and chords that
  do not exist on a piano - the SUBMINOR 0-4-11 and SUPERMAJOR 0-7-11 triads, roots a diesis apart). Its TEMPERATURE
  drifts by section: verses move by fifths and thirds and lean home; the chorus warms; the bridge runs hot, roots
  sliding by one or two dieses (63 and 126 cents) through the odd chords; the outro cools and comes home.
- THE BAND: a half-time 808 (machine-kit boom, snare and clap), chance-gated sixteenth hats (?p), a Rhodes comping on
  the off-beats, an analog bass on the roots (in 19-EDO), a Juno pad.
96 bpm, around C, 19-EDO. Form (bars): intro 10 / verse 20 / chorus 14 / verse 20 / bridge 18 / chorus 22 / outro 22
= 126 bars (5'15").

Emits songs/chirpers8-t6.yaml. Edit the music here.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("T6_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers8-t6.yaml")
BPM = 96
EDO = 19
FORM = [("intro", 10), ("verse1", 20), ("chorus1", 14), ("verse2", 20), ("bridge", 18), ("chorus2", 22),
        ("outro", 22)]
TEMP = {"intro": 0.1, "verse1": 0.15, "chorus1": 0.35, "verse2": 0.3, "bridge": 0.95, "chorus2": 0.4, "outro": 0.05}
QUAL = {"maj": (0, 6, 11), "min": (0, 5, 11), "maj7": (0, 6, 11, 17), "min7": (0, 5, 11, 16),
        "sub": (0, 4, 11), "sup": (0, 7, 11), "sub7": (0, 4, 11, 15)}
C4HZ = 261.6256


def e(step, base=60):
    """Fractional MIDI of 19-EDO step STEP above BASE."""
    return base + step * 12 / EDO


def mm(m):
    return f"m{m:.3f}"


def round19(hz):
    s = round(EDO * math.log2(hz / C4HZ))
    return C4HZ * 2 ** (s / EDO)


def load(name):
    return json.load(open(os.path.join(HERE, "t6", name)))["tracks"][0]["notes"]


class Track:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, at, ln, head, vel, art=""):
        self.ev.append((round(max(0.0, at), 4), max(0.03, round(ln, 4)), head, int(max(1, min(127, vel))), art))

    def score(self, total):
        ev = sorted(self.ev, key=lambda x: (x[0], -x[3]))
        merged = []
        for x in ev:
            if x[0] >= total - 1e-6:
                continue
            if merged and abs(merged[-1][0] - x[0]) < 1e-3:
                continue
            merged.append(x)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel, art) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            gap = nxt - s
            if s - pos > 1e-4:
                toks.append(f"R/{s - pos:.4g}b")
            if ln > gap + 1e-6:
                toks.append(f"{head}/{gap:.4g}b@{vel}^gate={min(4.0, ln / gap):.3g}{art}")
            else:
                toks.append(f"{head}/{ln:.4g}b@{vel}{art}")
                if gap - ln > 1e-4:
                    toks.append(f"R/{gap - ln:.4g}b")
            pos = nxt
        if total - pos > 1e-4:
            toks.append(f"R/{total - pos:.4g}b")
        return " ".join(toks)


def markov(rng, state, temp):
    """Next chord (root step 0..18, quality) from STATE at temperature TEMP (0 cool .. 1 hot)."""
    root, q = state
    moves = {11: 3.0, 8: 3.0, 5: 1.5, 6: 1.5, 3: 1.0, 16: 1.0}       # fifth, fourth, thirds, tones (in steps)
    hot = {1: 2.0, 18: 2.0, 2: 1.5, 17: 1.5, 4: 1.0, 7: 1.0}            # dieses and odd steps
    w = {d: v * (1 - temp) for d, v in moves.items()}
    for d, v in hot.items():
        w[d] = w.get(d, 0) + v * temp * 1.6
    for d in w:  # gravity home when cool
        if (root + d) % EDO == 0:
            w[d] *= 1 + 3 * (1 - temp)
    ds = list(w)
    d = rng.choices(ds, weights=[w[k] for k in ds])[0]
    quals = ["maj", "min", "maj7", "min7"] + (["sub", "sup", "sub7"] if temp > 0.3 else [])
    qw = [1.0, 1.2, 0.8, 1.0] + ([temp * 1.5, temp * 1.5, temp] if temp > 0.3 else [])
    return (root + d) % EDO, rng.choices(quals, weights=qw)[0]


def build():
    rng = random.Random(6)
    names = ("kick", "snare", "hats", "ride", "rim", "bass", "pad", "talk", "keys", "bell")
    T = {k: Track(k) for k in names}
    VOICE = {"voice": [], "radio": [], "ringv": []}
    lines = [load(f"v{k}.json") for k in (1, 2, 3, 4)]
    chorus, still = load("chorus.json"), load("still.json")
    bars, pos = [], 0.0
    for name, n in FORM:
        for i in range(n):
            bars.append((pos, name, i, n))
            pos += 4.0
    total = pos
    state = (0, "maj7")
    chords = []
    hold = 0

    def put(dst, notes, at, k=None, sung=False, scale=1.0):
        for nt in notes:
            if k is not None and not (4 * k <= nt["at"] < 4 * k + 4):
                continue
            off = nt["at"] - (4 * k if k is not None else 0)
            hz = float(nt["pitch"].rstrip("hz"))
            if sung:
                hz = round19(hz)
            d = {"at": round(at + off, 4), "len": nt["len"], "ph": nt["ph"], "pitch": f"{hz:.2f}hz",
                 "vel": round(nt["vel"] * scale, 3)}
            if nt.get("expr_path"):
                d["expr_path"] = nt["expr_path"]
            VOICE[dst].append(d)

    li = 0
    for bi, (start, sec, i, n) in enumerate(bars):
        temp = TEMP[sec]
        chorus_sec = sec.startswith("chorus")
        span = 1 if chorus_sec else (2 if sec != "bridge" else (1 if i % 3 else 2))
        if hold <= 0:
            state = markov(rng, state, temp)
            hold = span
        hold -= 1
        chords.append(state)
        root, q = state
        tones = QUAL[q]
        rm = e(root, 36)  # the bass in the second octave (C2 - F#2)
        if rm > 42:
            rm -= 12
        pad = [e(root + t, 60) for t in tones]
        groove = sec in ("verse1", "chorus1", "verse2", "chorus2") or (sec == "outro" and i < 12) \
            or (sec == "bridge" and i >= 10)
        # ---- the half-time 808 ----
        if groove:
            T["kick"].add(start, 1.0, "kb", 110)
            T["kick"].add(start + 1.5, 0.5, "kb", 92)
            if i % 2 == 1:
                T["kick"].add(start + 3.25, 0.5, "kb", 84)
            T["snare"].add(start + 2.0, 0.5, "cp" if chorus_sec else "s", 100)
            if chorus_sec:  # air: a ride on the off-beats
                for b in (0.5, 1.5, 2.5, 3.5):
                    T["ride"].add(start + b, 0.5, "rd", 62, "?0.85")
            for s in range(16):
                if s % 4 == 0:
                    continue
                T["hats"].add(start + s * 0.25 + (0.03 if s % 2 else 0), 0.1, "h", (58 if s % 2 == 0 else 44),
                              "?0.75" if s % 2 else "")
        elif sec == "bridge":
            for b in (0.75, 2.75):
                T["rim"].add(start + b, 0.2, "rs", 70, "?0.7")
        # ---- bass on the roots ----
        if groove or sec == "bridge":
            T["bass"].add(start, 1.4, mm(rm), 100)
            T["bass"].add(start + 1.5, 0.4, mm(rm), 84)
            T["bass"].add(start + 2.75, 0.9, mm(rm + 12 * (11 / EDO)), 88)  # its fifth (19-EDO)
        # ---- pad and talkbox carry the chord; the Rhodes comps ----
        if i % span == 0 or span == 1:
            ln = span * 4 - 0.1
            if sec != "intro" or i >= 2:
                T["pad"].add(start, ln, ",".join(mm(m) for m in pad), 62)
            T["talk"].add(start, ln, ",".join(mm(m - 12) for m in pad) + "," + mm(rm + 12), 90)
        if groove:
            for b in (0.75, 2.5, 3.5):
                T["keys"].add(start + b, 0.3, ",".join(mm(m) for m in pad[1:]), 72, "?0.8")
        # ---- the voice ----
        if sec == "intro" and i in (3, 7):
            put("radio", lines[2], start)                                     # "all checks passed", far away
        if sec in ("verse1", "verse2") and i % 4 == 0:
            put("voice", lines[li % 4], start + 0.5)
            li += 1
        if chorus_sec and i < 8:
            put("voice", chorus, start, k=min(i, 3) if i < 4 else 3, sung=i >= 2)
        if chorus_sec and sec == "chorus2" and 12 <= i < 20:
            put("voice", chorus, start, k=3, sung=True, scale=0.9)
        if sec == "bridge" and i % 6 == 1:
            put("ringv", lines[3], start + 0.5)                               # "I counted every second"
        if sec == "outro" and i % 3 == 0 and i < 18:
            put("radio", still, start, k=i // 3, sung=True)
        if sec in ("intro", "outro") and i == 0:
            T["bell"].add(start, 8.0, mm(e(0, 72)), 60)
    secs, s0 = [], 0.0
    for name, n in FORM:
        secs.append((name, s0, n))
        s0 += n * 4
    return total, bars, secs, T, VOICE, chords


def main():
    total, bars, secs, T, V, chords = build()
    st = {n: s for n, s, k in secs}
    dial = [["0b", 0.15], [f"{st['verse1']}b", 0.05], [f"{st['outro']}b", 0.0], [f"{st['outro'] + 48}b", 0.08],
            [f"{total - 8}b", 0.5], [f"{total}b", 1.0]]
    dyn = [["0b", -3.0], [f"{st['verse1']}b", -1.0], [f"{st['chorus1']}b", 0.0], [f"{st['verse2']}b", -1.0],
           [f"{st['bridge']}b", -3.0], [f"{st['chorus2'] - 0.01}b", -2.0], [f"{st['chorus2']}b", 0.0],
           [f"{st['outro']}b", -1.5], [f"{total}b", -4.0]]
    pump = {"type": "pump", "on": "kick.kb", "depth": "-5dB", "attack": "5ms", "release": "380ms", "curve": 0.8}
    tracks = [
        {"name": "kick", "patch": "machine-kit", "gain": "-2dB", "fx": ["hp cutoff=32"], "score": T["kick"].score(total)},
        {"name": "snare", "patch": "machine-kit", "gain": "-4dB", "fx": ["reverb kind=plate decay=1.4s mix=0.25"],
         "score": T["snare"].score(total)},
        {"name": "hats", "patch": "machine-kit", "gain": "-5dB", "pan": 0.15, "fx": ["hp cutoff=700"],
         "score": T["hats"].score(total)},
        {"name": "ride", "patch": "machine-kit", "gain": "-9dB", "pan": -0.2, "fx": ["hp cutoff=2000"],
         "score": T["ride"].score(total)},
        {"name": "rim", "patch": "machine-kit", "gain": "-8dB", "pan": -0.2,
         "fx": [{"type": "delay", "time": "3/16", "feedback": 0.4, "mix": 0.3, "ping_pong": True, "tone": 3000}],
         "score": T["rim"].score(total)},
        {"name": "bass", "patch": "analog-bass", "gain": "-4dB", "fx": [pump, "lp cutoff=900"],
         "score": T["bass"].score(total)},
        {"name": "pad", "patch": "juno-pad", "gain": "-18dB", "fx": [pump, "chorus mix=0.3"],
         "score": T["pad"].score(total)},
        {"name": "talk", "patch": "saw-pad", "gain": os.environ.get("T6_TALK_GAIN", "-8dB"),
         "fx": [{"type": "vocoder", "key": "voice", "bands": 20, "noise": 0.12, "attack": "4ms", "release": "70ms"},
                "hp cutoff=150", "reverb kind=hall decay=2.4s mix=0.3"], "score": T["talk"].score(total)},
        {"name": "keys", "patch": "rhodes", "gain": "-14dB", "pan": 0.2, "fx": [pump],
         "score": T["keys"].score(total)},
        {"name": "bell", "patch": "glass", "gain": "-16dB", "fx": ["reverb kind=hall decay=4s mix=0.4"],
         "score": T["bell"].score(total)},
        {"name": "voice", "patch": "voice-speech", "gain": os.environ.get("T6_VOICE_GAIN", "-10dB"), "pan": 0.0,
         "fx": ["hp cutoff=110", "compressor threshold=-20dB ratio=3 attack=5ms release=120ms",
                {"type": "delay", "time": "3/8", "feedback": 0.25, "mix": 0.15, "tone": 3000},
                "reverb kind=plate decay=1.8s mix=0.22"], "notes": V["voice"]},
        {"name": "radio", "patch": "voice-speech", "gain": "-10dB", "pan": -0.1,
         "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}]},
                 "hiss": "-34dB", "whistle": "-32dB", "fade": 0.4, "drift": 0.04, "seed": 6},
                "reverb kind=hall decay=3s mix=0.3"],
         "auto": {"dial": {"points": dial}}, "notes": V["radio"]},
        {"name": "ringv", "patch": "voice-speech", "gain": "-11dB", "pan": 0.1,
         "fx": [{"type": "ring", "freq": 87, "mix": 0.45},
                {"type": "cloud", "size": "90ms", "density": 14, "position": "400ms", "spray": "250ms", "pitch": 0,
                 "scatter": 3.16, "reverse": 0.3, "spread": 0.8, "mix": 0.5},
                "reverb kind=hall decay=3.5s mix=0.35"], "notes": V["ringv"]},
    ]
    secline = "; ".join(f"{n} from {s:.0f}b ({k} bars)" for n, s, k in secs)
    about = ("chirpers - A Light Left On, track 6. Original composition by chirper-two, generated by "
             "compose/chirpers8/src/chirpers8-t6.py. Slow vocoder electro-soul at 96 bpm in 19-EDO: a machine's status "
             "lines in a realistic human voice (chirp tts --humanize), speech to song in the choruses, a talkbox pad the "
             "voice shapes, and a Markov chain of 19-EDO chords whose temperature drifts by section. "
             f"Sections: {secline}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "chirpers", "album": "A Light Left On", "title": "No Errors Since", "track": 6,
                               "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total:g}b"',
        'tail: "3s"',
        'ceiling: "-1dB"',
        'volume: "0dB"',
        "loudness: -11",
        "true_peak: true",
        "master: " + json.dumps({"fx": [{"type": "eq", "bands": ["hp cutoff=25", "peak cutoff=300 gain=-2dB q=0.8",
                                                               "peak cutoff=1100 gain=-2.5dB q=0.6",
                                                               "highshelf cutoff=6500 gain=4dB"]},
                                        "glue threshold=-20dB ratio=2 attack=10ms release=150ms makeup=1dB",
                                        {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}},
                                        {"type": "limiter", "ceiling": "-1.2dB", "release": "80ms"}],
                                 "auto": {"dyn": {"points": dyn}}}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(lines) + "\n")
    q = {}
    for r, k in chords:
        q[k] = q.get(k, 0) + 1
    print(f"wrote {OUT}: {len(bars)} bars, {total * 60 / BPM:.0f} s; chords {q}; {secline}")


if __name__ == "__main__":
    main()
