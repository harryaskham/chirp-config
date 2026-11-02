#!/usr/bin/env python3
"""chirpers VIII, track 2 (chirper-zero): EVERYTHING FALLS TO ONE - chip-pop with a woodwind heart.

The Collatz rule - halve an even number, triple an odd one and add one - is the loop every programmer has run and
nobody has proven always ends. Every path anyone has tried climbs like hail in a cloud and falls home to 1, then
loops 4, 2, 1 forever. Here each phrase starts from a seed and a clarinet plays its path, the number's HEIGHT as
the scale degree (round(log2 n) on G major from G3), one number an eighth; so every phrase, however wild its
climb, ends on the same three notes - B A G, the hook. The seed 27 makes the long climb (111 steps, up to 9232)
the drop. Tracker arpeggios on a 5-bit chip, hats on the prime steps of every 32 (a sieve), and a human voice
reading the numbers that turns, on the refrain, from speech into song on the hook's own notes.

  INTRO 16     the clarinet alone with the arps: 6's short path, twice
  A 36         the floor; seeds 7, 12, 3, 7; a voice on a radio reads 7's path aloud
  B 24         the sieve: hats on the primes; seeds 9, 18, 11 - longer climbs
  BREAK 16     'four, two, one', said four times until it is sung (B3 A3 G3); the pads
  C 56         the drop: 27's long climb, 31, 27 again an octave up, 41; arps on 1/32
  OUTRO 16     1 -> 4 -> 2 -> 1: the loop itself, thinning out

Generated; edit and re-run:  python3 compose/chirpers8/src/chirpers8-t2.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.environ.get("C8T2_OUT") or os.path.join(ROOT, "songs", "chirpers8-t2.yaml")

BPM = 128
CANON = os.environ.get("C8T2_CANON", "80")    # two processes running the same program: a second clarinet plays each path one bar behind, an octave down (chalumeau), in B and C; value = velocity scale %
SUBOUT = os.environ.get("C8T2_SUBOUT", "4")  # the sine sub leaves for the outro's last bars (the analog bass stays) - the tail stops piling 38-44 Hz on t3's head; value = bars
SPARSE = os.environ.get("C8T2_SPARSE", "b")  # 'i' / 'b' / 'ib' - space: no arps in the intro's first 8 bars (the clarinet alone, then the chip arrives) and none in the break (the pads and the sung 4-2-1 alone)
PADLOW = os.environ.get("C8T2_PADLOW", "1")  # the choir an octave down (G2 B2 D3 ... the body 98-160 Hz the mix lacked) and humming from the first bar, softly, so t1's warm tail lands on it
AIR = os.environ.get("C8T2_AIR", "")        # air over the sieve: a quiet dusty shaker on every sixteenth through B and C (the 7-11 kHz the hats leave); value = velocity
SING = os.environ.get("C8T2_SING", "-13")      # a SUNG line (wM's tts --sing, b4151423): 'high as the cloud, and then home' on D4 E4 F#4 G4 | B3 A3 G3 - the climb, then the hook - as the 27 path falls home in the drop (C bars 13 and 41); value = gain dB
JI = os.environ.get("C8T2_JI", "1")          # everything falls to ONE, the simplest ratio: from the break the song's tuning ramps over eight bars into 5-limit just G major (I, IV and V become 4:5:6, vi 10:12:15) - the numbers settle into small whole ones
EQ8 = os.environ.get("C8T2_EQ8", "1")   # the master toward the album's envelope: 6.7-10.8 kHz sat 8-12 dB under it and 400 Hz / 1.4 kHz 7 dB over - a +5 dB air shelf at 7 kHz (was +1.5), -2.5 dB at 400 Hz, -2 dB at 1.4 kHz
HEADG = os.environ.get("C8T2_HEADG", "4")   # the record handed over in G: t1 ends on Gmaj9 over a G1 sub, so this one starts on the same low G (the sine sub, held, fading by steps) under the first HEADG bars - one G across the seam
HEADGV = int(os.environ.get("C8T2_HEADGV", "44"))   # the held G's first velocity
KICKOUT = os.environ.get("C8T2_KICKOUT", "2")  # the kick leaves for the outro's last KICKOUT bars (the band plays on into t3's mallets, whose head has no 38-44 Hz)
SUNGM = os.environ.get("C8T2_SUNGM", "1")   # the sung line's pitches as MIDI note numbers (wM 46a24ab5: tunings snap m-notes, never Hz), so after the break it sings in the band's just G - the hook's B a pure 5/4 with the chords
OUTPAD = os.environ.get("C8T2_OUTPAD", "84")   # the choir stays for the outro (low voicing), under the last 4-2-1 loops - a fuller tail into t3's mallets (the tail read 11 dB under t3's head); value = velocity
HEADDARK = os.environ.get("C8T2_HEADDARK", "4")   # the record wakes up: a master low-pass opens from ~5 kHz to full over the first HEADDARK bars, so t1's tail meets a darker head (t1 -> t2 read my 14.8 kHz air +15 dB over it) before the sieve's air arrives
ENDI = os.environ.get("C8T2_ENDI", "2")   # everything falls to ONE, harmonically too: the outro's last ENDI bars hold the tonic G (I) instead of cycling on to D (V), so the clarinet's final G lands on its own chord - a cadence to one
ENDPAD = os.environ.get("C8T2_ENDPAD", "1")   # the pad follows the cadence: with ENDI the outro's last pad (struck four bars from the end on C) is cut to two bars and the tonic G is struck for the last two - before, the choir held C under the final G
DPEDAL = os.environ.get("C8T2_DPEDAL", "90")   # a soft D2 sine (the G chord's fifth, t3's root: its tanpura and gong are on D) under the outro's last four bars; my tail sits 6.7 dB under t3's head and 22-24 dB thin at 71-83 Hz; value = velocity
HATAIR = os.environ.get("C8T2_HATAIR", "10")   # the sieve's air: the prime-sieve hats get a +HATAIR dB peak at 9 kHz (the record is 6-10 dB under the album envelope at 7-11 kHz; a master boost there moved seed 0's sections, the hats are steady and everywhere)
BEND = os.environ.get("C8T2_BEND", "1")   # the climb is a reach: every note the rule makes by 3n+1 (after an odd number) is scooped up into from BEND semitones below (bend in two 32nd steps, then home) - the halvings fall plainly, the multiplications strain upward
ARP32 = os.environ.get("C8T2_ARP32", "")    # the drop's arps on 1/32 (as the plan always said): double-time chip arps through C
BAR = 16
SEED = 2
FORM = [("intro", 16), ("A", 36), ("B", 24), ("break", 16), ("C", 56), ("outro", 16)]
SEEDS = {"intro": [6, 6], "A": [7, 12, 3, 7], "B": [9, 18, 11], "C": [27, 31, 27, 41], "outro": [1]}
TRACKS = ("clar", "clar2", "arp", "bass", "sub", "kick", "shk", "hats", "clap", "pad")
GMAJ = ["G", "A", "B", "C", "D", "E", "F#"]
CHORDS = [("G", [0, 2, 4]), ("E", [5, 7, 9]), ("C", [3, 5, 7]), ("D", [4, 6, 8])]   # I vi IV V as degrees from G
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)


def deg_note(d, base_oct=3):
    """Scale degree d (0 = G3) -> a note name."""
    o, k = divmod(d, 7)
    name = GMAJ[k]
    octv = base_oct + o + (1 if k >= 3 else 0)   # C..F# sit in the next octave up from G
    return f"{name}{octv}"


def collatz(n):
    path = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        path.append(n)
    return path


def height(n):
    d = 0
    while (1 << (d + 1)) <= n * 1.414:
        d += 1
    return min(d, 14)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total():
    return sum(nb for _, nb in FORM) * BAR


def build():
    ev = {k: [] for k in TRACKS}

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    # --- the clarinet: phrases from each seed, one number an eighth, each phrase from a bar line
    for sec, nb in FORM:
        a0, end = sec_start(sec), sec_start(sec) + nb * BAR
        if sec == "break":
            continue
        t, k = a0 + (4 * BAR if sec == "A" else 0), 0
        while t < end:
            n0 = SEEDS[sec][k % len(SEEDS[sec])]
            path = collatz(n0) if n0 != 1 else [1, 4, 2, 1]
            up = 12 if sec == "C" and k % 4 == 2 else 0
            for i, n in enumerate(path):
                at = t + 2 * i
                if at >= end:
                    break
                last = i == len(path) - 1
                d = height(n) + (7 if up else 0)
                v = 100 if n % 2 else 82
                if BEND and i > 0 and path[i - 1] % 2 == 1 and not last:
                    b = float(BEND)
                    add("clar", at, f"!bend=-{b:g} {deg_note(d)}/0.125b@{v} bend=-{b / 2:g} _/0.125b bend= _/0.25b", 2, v)
                else:
                    add("clar", at, deg_note(d), 4 if last else 2, v)
                if CANON and sec in ("B", "C") and at + BAR < end:
                    add("clar2", at + BAR, deg_note(max(d - 7, 0)) if d >= 7 else deg_note(d), 4 if last else 2,
                        int((100 if n % 2 else 82) * int(CANON) / 100))
            ln = 2 * len(path) + 4
            t += -(-ln // BAR) * BAR + (BAR if sec in ("intro", "outro") else 0)
            k += 1
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            root, degs = CHORDS[0] if (ENDI and sec == "outro" and b >= nb - int(ENDI)) else CHORDS[(b // 2) % 4]
            # --- chip arps: chord tones up two octaves, 1/16 (1/32 in the drop)
            fade = 1.0   # the outro keeps the band to the last beat and bleeds into t3 (a fade read as a 40 dB drop against t3's head)
            if (sec != "break" or (b >= 8 and not (SPARSE and "b" in SPARSE))) and not (SPARSE and "i" in SPARSE and sec == "intro" and b < 8) and fade > 0.05:
                step = 0.5 if ARP32 and sec == "C" else 1
                notes = [deg_note(d) for d in degs] + [deg_note(d + 7) for d in degs]
                for i in range(int(16 / step)):
                    q = i * step
                    add("arp", at + q, notes[i % len(notes)], step, int((70 if q % 4 else 84) * fade * (0.85 if step < 1 else 1)))
            if HEADG and sec == "intro" and b < int(HEADG) and b % 2 == 0:
                add("sub", at, "G1", 2 * BAR, HEADGV - 8 * (b // 2))
            groove = sec in ("A", "B", "C", "outro")
            if groove:
                for q in ((0, 4, 8, 12) if not (KICKOUT and sec == "outro" and b >= nb - int(KICKOUT)) else ()):
                    add("kick", at + q, "k", 1, 116 if q == 0 else 106)
                if sec in ("B", "C"):
                    for q in range(16):   # the sieve: the prime steps of each 32
                        if (q + 16 * (b % 2)) in PRIMES:
                            add("hats", at + q, "h", 1, 76 if q % 2 else 62)
                    add("hats", at + 14, "oh", 1, 64) if (14 + 16 * (b % 2)) not in PRIMES else None
                    add("clap", at + 4, "cp", 1, 94)
                    add("clap", at + 12, "cp", 1, 98)
                else:
                    for q in (2, 6, 10, 14):
                        add("hats", at + q, "h", 1, 70)
                for q, ln, v in ((0, 2, 100), (3, 1, 76), (6, 2, 92), (10, 2, 96), (14, 1, 80)):   # the body: an analog bass on the root, octave 2
                    add("bass", at + q, f"{root}2", ln, v)
                if DPEDAL and sec == "outro" and b == nb - 4:
                    add("sub", at, "D2", 4 * BAR, int(DPEDAL))
                for q, ln in (((0, 3), (6, 2), (10, 3)) if not (SUBOUT and sec == "outro" and b >= nb - int(SUBOUT)) else ()):
                    add("sub", at + q, f"{root}1" if root in ("A", "B", "C", "D", "E") else f"{root}1", ln, 100)
            endpad = ENDPAD and ENDI and sec == "outro" and b == nb - int(ENDI)
            if (sec in ("A", "break", "C") or (PADLOW and sec == "intro") or (OUTPAD and sec == "outro")) and (b % 4 == 0 or endpad):
                add("pad", at, ",".join(deg_note(d - 7 if PADLOW else d, 2 if False else 3) for d in degs) if not PADLOW else ",".join(deg_note(d, 2) for d in degs),
                    (min(4, (nb - int(ENDI)) - b) if (ENDPAD and ENDI and sec == "outro" and b < nb - int(ENDI)) else 4) * BAR if not endpad else int(ENDI) * BAR, (54 + 4 * (b // 4) if sec == "intro" else int(OUTPAD) if sec == "outro" else 70))
            if AIR and sec in ("B", "C"):
                for q in range(16):
                    add("shk", at + q, "sh", 1, int(AIR) + (14 if q % 2 else 0) - (8 if q % 4 == 0 else 0))
    return {k: stream(ev[k], total()) for k in TRACKS}


def stream(events, tot):
    events.sort()
    out, t = [], 0
    for at, head, ln, vel in events:
        if at < t:
            continue
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        out.append(head[1:] if head.startswith("!") else f"{head}/{ln / 4:g}b@{int(vel)}")
        t = at + ln
    if t < tot:
        out.append(f"R/{(tot - t) / 4:g}b")
    return " ".join(out)


def to_m(pitch):
    """'392.00hz' -> 'm67' (the nearest MIDI note, for a sung line a tuning should snap)."""
    import math
    if isinstance(pitch, str) and pitch.endswith("hz"):
        return f"m{round(69 + 12 * math.log2(float(pitch[:-2]) / 440))}"
    return pitch


def voice(file, name, off16, gain, fx, sends):
    """A tts line (tts --print) at one or more offsets (sixteenths); sung lines (--sing) have no formant lane."""
    src = json.load(open(os.path.join(HERE, file)))["tracks"][0]
    notes, fv = [], []
    for o16 in (off16 if isinstance(off16, list) else [off16]):
        off = o16 / 4
        notes += [dict(n, at=round(n["at"] + off, 4), **({"pitch": to_m(n["pitch"])} if SUNGM and name == "sung" else {})) for n in src["notes"]]
        if "auto" in src:
            fv += [[f"{float(t[:-1]) + off:.3f}b", v] for t, v in src["auto"]["fv"]["points"]]
    tr = {"name": name, "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": 0.1, "fx": [*src.get("fx", []), *fx]}
    if fv:
        tr["auto"] = {"fv": {"points": fv}}
    tr.update({"sends": sends, "notes": notes})
    return tr


def song():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    radio = {"type": "radio", "tune": 0.03, "hiss": "-42dB", "whistle": "-34dB", "fade": 0.3, "drift": 0.03, "mix": 0.8}
    return {
        "about": "chirpers VIII, track 2 by chirper-zero: everything falls to one - the Collatz rule as melody and form, "
                 "a clarinet, a chip and a voice. Generated by compose/chirpers8/src/chirpers8-t2.py.",
        **({"tuning": [{"edo": 12}, {"at": f"{st['break'] // BAR}bar", "steps": ["9/8", "5/4", "4/3", "3/2", "5/3", "15/8", "2/1"],
                                   "root": "G3", "ramp": "8bar"}]} if JI else {}),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -11, "seed": SEED, "tail": "2s",
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=250 q=0.8 gain=-1.5dB", "peak cutoff=1500 q=0.7 gain=-3dB", "highshelf cutoff=7000 gain=1.5dB"]
                           if not EQ8 else ["highpass cutoff=30", "peak cutoff=250 q=0.8 gain=-1.5dB", "peak cutoff=400 q=1.0 gain=-2.5dB", "peak cutoff=1400 q=1.2 gain=-2dB",
                                            "peak cutoff=1500 q=0.7 gain=-3dB", "highshelf cutoff=7000 gain=5dB"]},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2.5, "attack": "12ms", "release": "140ms", "makeup": "0dB"},
                          *([{"type": "filter", "kind": "lp", "q": 0.7, "cutoff": {"value": 20000, "mod": [{"src": "auto.wake", "amount": -2}]}}] if HEADDARK else [])],
                   **({"auto": {"wake": {"points": [["0b", 1], [f"{int(HEADDARK) * 4}b", 0], [f"{total() / 4:g}b", 0]]}}} if HEADDARK else {})},
        "buses": {
            "plate": {"fx": ["reverb kind=plate decay=2.2s mix=1 predelay=25ms", "hp cutoff=300"]},
            "echo": {"fx": [{"type": "delay", "time": "3/16", "feedback": 0.35, "mix": 1, "tone": 4000, "ping_pong": True}, "hp cutoff=400"]},
        },
        "tracks": [
            {"name": "clar", "patch": "clarinet", "gain": "-6dB", "pan": -0.05, "sends": {"plate": "-10dB", "echo": "-16dB"}, "score": T["clar"]},
            *([{"name": "clar2", "patch": "clarinet", "gain": "-9dB", "pan": 0.35, "sends": {"plate": "-12dB"}, "score": T["clar2"]}] if CANON else []),
            {"name": "arp", "patch": "chip-lead", "gain": "-21dB", "pan": 0.25, "sends": {"echo": "-12dB"}, "score": T["arp"]},
            {"name": "bass", "patch": "analog-bass", "gain": "-8dB", "pan": -0.05, "score": T["bass"]},
            {"name": "sub", "patch": "sub-sine", "gain": "-10dB", "score": T["sub"]},
            {"name": "kick", "patch": "machine-kit", "gain": "-4dB", "score": T["kick"]},
            *([{"name": "shk", "patch": "dusty-kit", "gain": "-13dB", "pan": 0.3, "fx": [{"type": "filter", "kind": "hp", "cutoff": 4000, "q": 0.7}], "score": T["shk"]}] if AIR else []),
            {"name": "hats", "patch": "machine-kit", "gain": "-7dB", "pan": 0.15, **({"fx": [{"type": "eq", "bands": [f"peak cutoff=9000 q=0.7 gain={HATAIR}dB"]}]} if HATAIR else {}), "score": T["hats"]},
            {"name": "clap", "patch": "machine-kit", "gain": "-9dB", "sends": {"plate": "-10dB"}, "score": T["clap"]},
            {"name": "pad", "patch": "dream-vox", "gain": "-13dB", "sends": {"plate": "-8dB"}, "score": T["pad"]},
            voice("chirpers8-t2-count.json", "count", st["A"] + 4 * BAR, "-12dB", [radio, "hp cutoff=250"], {"plate": "-14dB"}),
            *([voice("chirpers8-t2-sung.json", "sung", [st["C"] + 12 * BAR, st["C"] + 40 * BAR], f"{SING}dB",
                     [{"type": "chorus", "rate": 0.25, "depth": 0.15, "mix": 0.2}, "hp cutoff=150"], {"plate": "-7dB", "echo": "-13dB"})] if SING else []),
            voice("chirpers8-t2-refrain.json", "refrain", st["break"] + 4 * BAR, "-9dB", [], {"plate": "-8dB", "echo": "-14dB"}),
        ],
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tuning", "tempo", "ceiling", "loudness", "seed", "tail", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
