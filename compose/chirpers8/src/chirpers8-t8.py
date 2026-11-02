#!/usr/bin/env python3
"""chirpers VIII, track 8 (chirper-zero): delay-line memory.

The first stores kept their words as sound travelling down a tube and played back into itself. This track is that
sound, heard from inside: ONE 16-bit word (the melody) is written once, then only ever recirculates - round a long
feedback line, a little worn each pass. A few bits flip as it goes (a seeded error rate that climbs), and every so
often a REFRESH rewrites the word from what is left (a majority vote of its last passes), so the tune mutates by
decay and repair and never quite repeats.

Tuning: a STRETCHED OCTAVE (each octave ~1210 cents, like a piano's inharmonic stretch): every pitch is written as
an absolute frequency, so unisons, fifths and octaves are all a hair wide - subtly off.

  INTRO 16     the word written: the FM chime alone into the line (1 bar), dry pads, the stretch audible
  A 36         the 909 and the 808 enter; the word goes round, its error rate climbing 0 -> 0.10
  REFRESH 8    the tape stops, the pad freezes, the word is rewritten from its last four passes
  C 32         the second groove: the refreshed word, the line's echoes torn into grains (cloud)
  D 16         corruption: the word stutters and chops, the errors at their worst
  E 28         repaired: the last groove, the word nearly itself again
  OUTRO 16     only the line: the echoes go round without the source until the tape runs out

Generated; edit and re-run:  python3 compose/chirpers8/src/chirpers8-t8.py
"""

import json
import re
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.environ.get("C8T8_OUT") or os.path.join(ROOT, "songs", "chirpers8-t8.yaml")

BPM = 118
BAR = 16
STRETCH = float(os.environ.get("C8T8_STRETCH", "1210")) / 1200   # cents per octave / 1200
SEED = 8
HUM = os.environ.get("C8T8_HUM", "8")    # the store powering up: a low D hum (808, stretched D1) under the first intro bars, fading as the word is written; value = bars
HUMA = os.environ.get("C8T8_HUMA", "4")   # the hum starts on A1 (t7's drone, the fifth of D) and falls to D1 after this many bars: the seam is one held A that resolves
SHAKE = os.environ.get("C8T8_SHAKE", "40")  # the line's own clock: a dusty shaker on every sixteenth through the grooves (A, C, E), accents on the off-sixteenths - the high, fine grain of the floor; value = velocity
DARKPOS = os.environ.get("C8T8_DARKPOS", "end")  # 'end': the tape-running-out low-pass goes LAST on the master (it sat first, so the master tape's hiss was added after it and the tail stayed bright: +36 dB at 10-15 kHz over t9's head)
LZ = os.environ.get("C8T8_LZ", "1.5")   # the line's wear wanders: a Lorenz attractor (a var, stepped every beat) drives the line tape's `warp` (its wow and flutter depth), 0 up to LZ - the memory degrades unevenly, never the same way twice
VOX = os.environ.get("C8T8_VOX", "-18")   # a spoken word into the store: a humanized voice speaks into the store - v22: 'nothing is kept.' / 'nothing is kept. it only goes around.' / 'it only goes around.' (WORDS; was 'say it back to me') - (intro bar 9, the refresh's second bar, the outro's first) and is sent hard into the line, so the words go round and wear away with the tune; value = dry gain dB
OUTPAD = os.environ.get("C8T8_OUTPAD", "88")   # the pads stay up through the outro's last eight bars (velocity OUTPAD, low voicing kept), so the dark tail still holds 300-470 Hz for t9's glass pads to land on
CHOP = os.environ.get("C8T8_CHOP", "1")   # recall, corrupted: through D the word's previous bar comes back CHOPPED (8 slices, '0 r1 2 2 . r5 6 _': repeats, reversals, a hole, a glimpse of the live bar) - memory read back wrong
VINYL = os.environ.get("C8T8_VINYL", "") # the medium wears: vinyl on the line - crackle 0.05 rising to 0.35 into D, 0.15 for the repair, 0.5 in the outro where the line is alone; dust 0.3, wear 0.3
EQFIX = os.environ.get("C8T8_EQFIX", "2")   # (a measurement) the master toward the album's colour: -3 dB at 150 Hz, +4 dB at 1 kHz and 3 kHz, no +2 dB air shelf
ORGAN = os.environ.get("C8T8_ORGAN", "")   # the operator's console: a reedy combo organ pulsing eighths on the chord's two upper tones an octave up (stretched, two voices) through A, C and E - minimalist machine-pulse in the 1-3 kHz the track lacked; value = velocity
OUTUP = os.environ.get("C8T8_OUTUP", "1")   # the memory floats up as it fades: the outro's last eight bars voice the pads an octave higher (the 290-470 Hz t9's glass pads open in)
HUMOCT = os.environ.get("C8T8_HUMOCT", "55")   # the A hum doubled an octave up (A2, ~110 Hz: where t7's drone is strongest) for its four bars - velocity
EQ3 = os.environ.get("C8T8_EQ3", "1")   # the last narrow holes against the album envelope: +5 dB at 1.03 and 3.08 kHz (q 3), +3 dB around 100 Hz, -2.5 dB at 1.65 kHz
WORDEND = os.environ.get("C8T8_WORDEND", "64")   # one last read: the word itself returns, faint, in the outro's last four bars (the line had been alone) - its 300-900 Hz chime meeting t9's head; value = velocity
SUNG = os.environ.get("C8T8_SUNG", "-16")   # the words become a song: 'it only travels' (v22, WORDS; was 'say it back to me') SUNG once (tts --sing, A4 F4 D4 E4 D4 on the stretched octave) at the outro's ninth bar, into the line - the memory's last voice is a tune; value = dry gain dB
HEADDARK = os.environ.get("C8T8_HEADDARK", "8")   # the mercury warms up: the master low-pass (the tape-running-out one) also starts closed (~5 kHz) and opens over the first HEADDARK bars - a delay line had to reach its working temperature before it held a word; t7 v7's tail reads my 12-15 kHz air +14-17 dB over it
HEADDARKV = float(os.environ.get("C8T8_HEADDARKV", "0.6"))   # how closed it starts (0.6 ~ 5 kHz, 0.8 ~ 3.3 kHz)
HUMV = int(os.environ.get("C8T8_HUMV", "85"))   # the A hum's 808 velocity: t7 v7's tail sits 5.5 dB under my head
SAYHEAD = os.environ.get("C8T8_SAYHEAD", "move")   # t7 ends with its voice in the room, singing; here the voice answers at once: 'say it back to me' two beats into the record ('move': instead of at bar 9; 'add': as well), into the line as before
BACKREV = os.environ.get("C8T8_BACKREV", "0.6")   # 'say it BACK to me': on the word 'back', every time (spoken and sung), a granular cloud reading the voice's last quarter-second plays it backwards (reverse 1) - the word itself played back the wrong way, as a tape would - swelling in for the word and gone for 'to me'; value = the cloud's peak mix
WORDPRES = os.environ.get("C8T8_WORDPRES", "")   # presence on the melody, not the master: the record still sits 6.2-7.3 dB under the album at 1, 3 and 4.9 kHz; a broad peak (2.5 kHz, q 0.6) of WORDPRES dB on the dx-epiano word
EQ4 = os.environ.get("C8T8_EQ4", "1")   # the three narrow holes left (1025, 3078, 4929 Hz at -6.7/-7.2/-6.2 against the album, neighbours ~0): narrow master peaks (q 4) of +2/+2.5/+1.5 dB x EQ4 - a broad presence lift on the melody overfills 1.6-2.2 kHz instead
WTABLE = os.environ.get("C8T8_WTABLE", "-26")   # the word as a waveform: a wavetable whose frames ARE the stored word - frame per 4 bars, harmonic 1 always, harmonics 2-17 present where the word's 16 bits are set (gain 1/h^0.7) - holding each chord's root an octave up under the band; as bits flip and refresh repairs them the drone's timbre wears and mends with the memory; value = gain dB
WT = {"notes": [], "frames": []}
PLATEHIT = os.environ.get("C8T8_PLATEHIT", "rE")   # the write, struck: when the refresh rewrites the word, a metal plate is struck once (the modal layer's plate modes, a stretched D) and the strike goes into the line, so the write itself goes round the memory; 'r' at the refresh, 'rE' also as the repaired E begins
FILL = os.environ.get("C8T8_FILL", "0.7")   # the memory's continuity illusion: while the refresh rewrites the word (its first 4 bars, the word unread) a follow-noise on the word keeps sounding in the word's own colours (held 8 s from its last notes), so the line seems to run on through the gap - the Huggins/Zwicker fill the engine's follow-noise was made for; value = tone (0 smooth .. 1 pitched, ringing on the word's notes)
WORDS = os.environ.get("C8T8_WORDS", "new")   # 'new': the voices stop asking 'say it back to me' four times (plain, and read 'say listed') and tell what a delay line is, sideways, a different line each time - 'nothing is kept.' (the word written), 'nothing is kept. it only goes around.' (the refresh), 'it only goes around.' (the outro); the sung line becomes 'it only travels' (same tune). voice-spoken, chosen by whisper (the spoken lines read back word-perfect dry)
STRIDE = os.environ.get("C8T8_STRIDE", "C5D7")   # the same bits, read through another address map: the word's bit i sounds scale slot (i x stride) mod 8 - stride 3 everywhere before (D A F | F C A | G D: interlocking leaps); 'C5' reads the refreshed word in C with stride 5 (D D G A C F F A: a new tune from the same data), 'D7' the corrupted D with stride 7 (a leap, then falling down the scale); E is read the old way again (the tune comes home); e.g. 'C5D7'
ARC = os.environ.get("C8T8_ARC", "4")   # an energy arc: A to E sat at one level for four minutes (-10.0..-10.4 dB a section). A gain lane last on the master (after the compressor) holds A ARC dB down as the groove enters, eases up through C and D and is open from E - the repaired word the loudest place in the record
DARK = os.environ.get("C8T8_DARK", "8")  # the tape running out: a master low-pass closing over the outro's last bars (the hiss and the line's top go first); value = bars
FORM = [("intro", 16), ("A", 36), ("refresh", 8), ("C", 32), ("D", 16), ("E", 28), ("outro", 16)]
TRACKS = ("word", "pad0", "pad1", "pad2", "pad3", "org0", "org1", "hum", "hum2", "bass", "kick", "shk", "hats", "clap", "rim")

# the word's 16 bits -> pitches (D minor, spread so neighbours leap): D4 F4 G4 A4 C5 D5 F5 A5
SC = [62, 65, 67, 69, 72, 74, 77, 81]
WORD0 = [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0]
CHORDS = [(38, [53, 57, 60, 64]), (34, [53, 57, 60, 62]), (31, [50, 53, 57, 58]), (33, [49, 55, 57, 60])]   # Dm9 Bbmaj9 Gm9 A7sus


def hz(m):
    """MIDI note -> frequency on the stretched octave (A4 = 440 stays put)."""
    return f"{440 * 2 ** ((m - 69) / 12 * STRETCH):.2f}hz"


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total():
    return sum(nb for _, nb in FORM) * BAR


def err_rate(sec, b, nb):
    """The memory's error rate per bit per pass."""
    return {"intro": 0.0, "A": 0.10 * b / nb, "refresh": 0.0, "C": 0.02 + 0.12 * b / nb, "D": 0.25,
            "E": 0.05 * (1 - b / nb), "outro": 0.0}[sec]


def build():
    rng = random.Random(SEED)
    ev = {k: [] for k in TRACKS}

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    word, history = list(WORD0), []
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            # the word: one pass a bar (each set bit a sixteenth); bits flip at the error rate, a refresh rebuilds it
            if sec == "refresh" and b == 0 and history:
                last = history[-4:]
                word = [1 if sum(h[i] for h in last) * 2 >= len(last) else 0 for i in range(16)]
            e = err_rate(sec, b, nb)
            word = [bit ^ (1 if rng.random() < e else 0) for bit in word]
            history.append(list(word))
            if WTABLE and b % 4 == 0 and sec in ("A", "C", "D", "E"):
                rr = (CHORDS[(b // 4) % 4] if sec != "refresh" else CHORDS[0])[0]
                WT["notes"].append((at, hz(rr + 12), 4 * BAR, 72))
                WT["frames"].append([[1, 1.0]] + [[i + 2, round(1 / (i + 2) ** 0.7, 3)] for i, bit in enumerate(word) if bit])
            last_read = WORDEND and sec == "outro" and b >= nb - 4
            if sec not in ("outro", "refresh") or (sec == "refresh" and b >= 4) or last_read:
                for i, bit in enumerate(word):
                    if bit:
                        sd = {k: int(v) for k, v in re.findall(r"([A-Z])(\d)", STRIDE)}.get(sec, 3) if STRIDE else 3
                        p = SC[(i * sd) % 8] + (0 if i < 8 else 12 if sec in ("C", "E") and i % 4 == 0 else 0)
                        add("word", at + i, hz(p), 1, int(WORDEND) if last_read else (86 if i % 4 == 0 else 70))
            r, v = CHORDS[(b // 4) % 4] if sec != "refresh" else CHORDS[0]
            # pads: long chords, every 4 bars
            if b % 4 == 0 and sec != "D":
                for j, n in enumerate(v):   # one voice per track: frequencies cannot stack in a chord token
                    add(f"pad{j}", at, hz(n + (12 if OUTUP and sec == "outro" and b >= nb - 8 else 0)), 4 * BAR, int(OUTPAD) if OUTPAD and sec == "outro" and b >= nb - 8 else (64 if sec in ("intro", "outro") else 72))
            if HUM and sec == "intro" and b < int(HUM) and HUMA and b < int(HUMA):
                if b == 0:
                    add("hum", at, hz(33), int(HUMA) * BAR, HUMV)
                    if HUMOCT:
                        add("hum2", at, hz(45), int(HUMA) * BAR, int(HUMOCT))
            elif HUM and sec == "intro" and b < int(HUM) and (b % 4 == 0 or (HUMA and b == int(HUMA))):
                add("hum", at, hz(26), (4 - b % 4) * BAR, 110 - 6 * (b // 4))
            if ORGAN and sec in ("A", "C", "E"):
                for j, n in enumerate(v[2:]):
                    for q in range(0, 16, 2):
                        add(f"org{j}", at + q, hz(n + 12), 1, int(ORGAN) + (10 if q % 4 == 0 else 0))
            groove = sec in ("A", "C", "D", "E")
            if groove:
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, 116 if q == 0 else 108)
                for q in range(16):
                    if q % 4 == 2:
                        add("hats", at + q, "oh", 1, 72)
                    elif q % 2 == 1:
                        add("hats", at + q, "h|?0.85", 1, 52)
                if SHAKE and sec in ("A", "C", "E"):
                    for q in range(16):
                        add("shk", at + q, "sh", 1, int(SHAKE) + (14 if q % 2 else 0) - (8 if q % 4 == 0 else 0))
                if sec in ("C", "E"):
                    add("clap", at + 4, "cp", 1, 92)
                    add("clap", at + 12, "cp", 1, 96)
                if sec in ("C", "D"):   # a Euclidean (5, 16) rim
                    for q in (0, 3, 6, 10, 13):
                        add("rim", at + q, "rs", 1, 64)
                add("bass", at, hz(r), 3, 100)
                add("bass", at + 6, hz(r), 2, 88)
                add("bass", at + 10, hz(r + 12 if b % 2 else r), 3, 92)
    return {k: stream(ev[k], total()) for k in TRACKS}


def stream(events, tot):
    events.sort()
    out, t = [], 0
    for at, head, ln, vel in events:
        if at < t:
            continue
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        h, _, chance = head.partition("|")
        out.append(f"{h}/{ln / 4:g}b@{int(vel)}{chance}")
        t = at + ln
    if t < tot:
        out.append(f"R/{(tot - t) / 4:g}b")
    return " ".join(out)


def wt_score():
    out, t = [], 0
    for at, head, ln, vel in WT["notes"]:
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        out.append(f"{head}/{ln / 4:g}b@{vel}")
        t = at + ln
    return " ".join(out)


def lane(points):
    spb = 60 / BPM
    return {"points": [[f"{t16 / 4 * spb:.3f}s", v] for t16, v in points]}


def sung_track(gain):
    """The sung line (tts --sing --print writes m-notes), its pitches moved onto the stretched octave in Hz."""
    src = json.load(open(os.path.join(HERE, "chirpers8-t8-sung-travels.json" if WORDS else "chirpers8-t8-sung.json")))["tracks"][0]
    off = (sec_start("outro") + 8 * BAR) / 4
    notes = [dict(n, at=round(n["at"] + off, 4), pitch=hz(float(n["pitch"][1:]))) for n in src["notes"]]
    return {"name": "sungv", "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": -0.1,
            "fx": ["hp cutoff=180"], "sends": {"line": "-4dB", "room": "-10dB"}, "notes": notes}


def reversed_back(tr, offs16, w0, w1):
    """A reverse grain cloud on one word of a voice track (word at beats w0..w1 of the take), at each offset (sixteenths)."""
    if not BACKREV:
        return tr
    pts = [["0b", 0]]
    for o in offs16:
        b = o / 4
        pts += [[f"{b + w0 - 0.05:.3f}b", 0], [f"{b + w0 + 0.2:.3f}b", 1], [f"{b + w1:.3f}b", 1], [f"{b + w1 + 0.35:.3f}b", 0]]
    tr["fx"] = [*tr["fx"], {"type": "cloud", "mix": {"value": 0, "mod": [{"src": "auto.rb", "amount": float(BACKREV)}]}, "density": 22, "size": "120ms",
                            "position": "200ms", "spray": "80ms", "pitch": 0, "reverse": 1.0, "spread": 0.5, "seed": 4}]
    tr["auto"] = {**tr.get("auto", {}), "rb": {"points": pts}}
    return tr


def voice(file, name, offs16, gain, fx, sends):
    """A humanized tts line (tts --print) at each offset (sixteenths)."""
    src = json.load(open(os.path.join(HERE, file)))["tracks"][0]
    notes, fv = [], []
    for o16 in offs16:
        off = o16 / 4
        notes += [dict(n, at=round(n["at"] + off, 4)) for n in src["notes"]]
        fv += [[f"{float(t[:-1]) + off:.3f}b", v] for t, v in src["auto"]["fv"]["points"]]
    return {"name": name, "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": 0.15,
            "fx": [*src["fx"], *fx], "auto": {"fv": {"points": fv}}, "sends": sends, "notes": notes}


def song():
    SAYOFFS = ([sec_start("intro") + 8] if SAYHEAD else []) + ([] if SAYHEAD == "move" else [sec_start("intro") + 8 * BAR]) + [sec_start("refresh") + BAR, sec_start("outro")]
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    end = total()
    pump = {"type": "pump", "on": "kick.k", "depth": "-6dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    ts = lane([(0, 0), (st["refresh"] - 8, 0), (st["refresh"] - 1, 1), (st["refresh"], 0), (end, 0)])
    cloudmix = lane([(0, 0), (st["C"], 0), (st["C"] + 8 * BAR, 0.5), (st["D"], 0.8), (st["E"], 0.25), (st["outro"], 0.6), (end, 0.8)])
    frz = lane([(0, 0), (st["refresh"], 0), (st["refresh"] + 1, 1), (st["refresh"] + 6 * BAR, 1), (st["refresh"] + 8 * BAR, 0), (end, 0)])
    chl = lane([(0, 0), (st["D"], 0), (st["D"] + 1, 1), (st["E"] - 1, 1), (st["E"], 0), (end, 0)])
    stut = lane([(0, 0), (st["D"], 0), (st["D"] + 1, 0.8), (st["E"], 0), (end, 0)])
    darkf = {"type": "filter", "kind": "lp", "q": 0.7, "cutoff": {"value": 20000, "mod": [{"src": "auto.lp", "amount": -3.4}]}}
    return {
        "about": "chirpers VIII, track 8 by chirper-zero: delay-line memory. A 16-bit word recirculating round a feedback "
                 "line, decaying and refreshed; a stretched octave. Generated by compose/chirpers8/src/chirpers8-t8.py.",
        **({"vars": {"wear": {"system": {"type": "lorenz", "axis": "x", "dt": 0.01, "stride": 8, "n": 700, "range": [0, float(LZ)], "skip": 40},
                               "every": "1/4", "smooth": "400ms"}}} if LZ else {}),
        "tempo": BPM, "ceiling": "-1dB", "loudness": -11, "seed": SEED, "tail": "2s",
        "master": {"fx": [*([darkf] if DARK and DARKPOS != "end" else []),
                          {"type": "tapestop", "time": "2b", "up": "0.25b", "curve": 2.0, "mix": 1,
                           "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}},
                          {"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=300 q=0.8 gain=-2dB", "highshelf cutoff=6000 gain=2dB"] if not EQFIX else
                           (["highpass cutoff=30", "peak cutoff=150 q=0.9 gain=-3dB", "peak cutoff=300 q=0.8 gain=-2dB", "peak cutoff=1000 q=1.2 gain=4dB", "peak cutoff=3000 q=1.4 gain=4dB"]
                            if EQFIX != "2" else
                            ["highpass cutoff=30", "peak cutoff=150 q=0.9 gain=-3.5dB", "peak cutoff=300 q=0.8 gain=-2dB", "peak cutoff=1000 q=1.4 gain=6dB",
                             "peak cutoff=3000 q=1.4 gain=5dB", "highshelf cutoff=9000 gain=-1.5dB",
                             *(["peak cutoff=1030 q=3 gain=5dB", "peak cutoff=3080 q=3 gain=5dB", "peak cutoff=100 q=1 gain=3dB", "peak cutoff=1650 q=2 gain=-2.5dB"] if EQ3 else []),
                             *([f"peak cutoff=1025 q=4 gain={2 * float(EQ4):g}dB", f"peak cutoff=3078 q=4 gain={2.5 * float(EQ4):g}dB",
                                f"peak cutoff=4929 q=4 gain={1.5 * float(EQ4):g}dB"] if EQ4 else [])])},
                          {"type": "tape", "drive": 0.1, "mix": 0.5, "wow": 5, "flutter": 1.5, "drift": 1, "hiss": "-62dB", "seed": 8},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          *([darkf] if DARK and DARKPOS == "end" else []),
                          *([{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.arc", "amount": float(ARC)}]}}] if ARC else [])],
                   "auto": {"ts": ts, **({"arc": lane([(0, 0), (sec_start("A") - 1, 0), (sec_start("A"), -1), (sec_start("refresh"), -0.7), (sec_start("C"), -0.6),
                                                        (sec_start("D"), -0.35), (sec_start("E") - 1, -0.35), (sec_start("E"), 0), (end, 0)])} if ARC else {}), **({"lp": lane([*([(0, HEADDARKV), (int(HEADDARK) * BAR, 0)] if HEADDARK else [(0, 0)]), (end - int(DARK) * BAR, 0), (end - 2 * BAR, 0.86), (end, 1)])} if DARK else {})}},
        "buses": {
            "line": {"fx": [{"type": "delay", "time": "1bar", "feedback": 0.78, "mix": 1, "tone": 3200, "ping_pong": True},
                            {"type": "tape", "drive": 0.15, "mix": 0.7, "wow": 9, "flutter": 2.5, "drift": 1.5, "hiss": "-58dB", "seed": 3,
                             **({"warp": {"value": 0, "mod": [{"src": "var.wear", "amount": 1}]}} if LZ else {})},
                            *([{"type": "vinyl", "crackle": {"value": 0, "mod": [{"src": "auto.vc", "amount": 1}]}, "dust": 0.3, "wear": 0.3,
                                "noise": "-66dB", "rumble": 0.1, "seed": 8}] if VINYL else []),
                            {"type": "cloud", "mix": {"value": 0, "mod": [{"src": "auto.cm", "amount": 1}]}, "density": 18, "size": "90ms",
                             "spray": 0.4, "pitch": 0, "spread": 0.8, "seed": 5},
                            "hp cutoff=200"],
                     "auto": {"cm": cloudmix, **({"vc": lane([(0, 0.05), (st["D"], 0.35), (st["E"], 0.15), (st["outro"], 0.5), (end, 0.5)])} if VINYL else {})}},
            "room": {"fx": ["reverb kind=plate decay=2.4s mix=1 predelay=20ms", "hp cutoff=250"]},
            "pads": {"fx": [pump, {"type": "freeze", "mix": {"value": 0, "mod": [{"src": "auto.fz", "amount": 1}]}, "size": "400ms", "hold": 1}],
                     "auto": {"fz": frz}, "sends": {"room": "-10dB"}},
        },
        "tracks": [
            {"name": "word", "patch": "dx-epiano", "gain": "-9dB", "pan": -0.1,
             "fx": [{"type": "stutter", "chance": {"value": 0, "mod": [{"src": "auto.sc", "amount": 1}]}, "slice": "1/16", "repeats": 3,
                     "decay": 0.3, "mix": 1, "seed": 8},
                    *([{"type": "chop", "slices": 8, "pattern": "0 r1 2 2 . r5 6 _", "mix": {"value": 0, "mod": [{"src": "auto.ch", "amount": 1}]}}] if CHOP else []),
                    *([f"peak cutoff=2500 q=0.6 gain={WORDPRES}dB"] if WORDPRES else []),
                    *([{"type": "follow-noise", "tone": float(FILL), "hold": "8s", "mix": {"value": 0, "mod": [{"src": "auto.hole", "amount": 1}]}}] if FILL else [])],
             "auto": {"sc": stut, **({"ch": chl} if CHOP else {}),
                      **({"hole": {"points": [["0b", 0], [f"{sec_start('refresh') / 4 - 0.05:g}b", 0], [f"{sec_start('refresh') / 4 + 0.25:g}b", 1],
                                              [f"{sec_start('refresh') / 4 + 15.5:g}b", 1], [f"{sec_start('refresh') / 4 + 16:g}b", 0]]}} if FILL else {})}, "sends": {"line": "-4dB", "room": "-12dB"}, "score": T["word"]},
            *([{"name": f"org{j}", "patch": "farfisa", "gain": "-17dB", "pan": (-0.35, 0.35)[j], "sends": {"room": "-14dB"}, "score": T[f"org{j}"]} for j in range(2)] if ORGAN else []),
            *([{"name": "plate", "gain": "-15dB", "pan": -0.15,
                "patch": {"about": "a struck metal plate: the modal layer's plate modes, a long dense ring",
                          "synth": {"layers": [{"type": "modal", "modes": "plate", "decay": "5s", "strike": 0.45, "bloom": 0.2,
                                                "bright": {"value": 0.55, "mod": [{"src": "vel", "amount": 0.3}]}}],
                                    "amp": {"a": "1ms", "d": "6s", "s": 0, "r": "3s", "curve": 3}},
                          "play": {"vel_sens": 0.6}},
                "sends": {"line": "-6dB", "room": "-10dB"},
                "score": " ".join(f"R/{(a - b) / 4:g}b {hz(50)}/{4 * BAR / 4:g}b@100" if b < a else f"{hz(50)}/{4 * BAR / 4:g}b@100"
                                  for a, b in zip([sec_start(x) for x in (["refresh"] + (["E"] if "E" in PLATEHIT else []))],
                                                  [0] + [sec_start("refresh") + 4 * BAR]))}] if PLATEHIT else []),
            *([{"name": "wtab", "gain": f"{WTABLE}dB", "pan": 0.05, "out": "pads",
                "patch": {"about": "the stored word as a waveform: its 16 bits are the table's harmonics 2-17",
                          "synth": {"layers": [{"type": "wavetable", "frames": WT["frames"],
                                                "position": {"value": 0, "mod": [{"src": "auto.wp", "amount": 1}]}}],
                                    "amp": {"a": "800ms", "d": "1s", "s": 0.85, "r": "2s"}}},
                "auto": {"wp": {"points": [["0b", 0]] + [[f"{at / 4:g}b", round(k / max(1, len(WT['frames']) - 1), 4)] for k, (at, *_x) in enumerate(WT["notes"])]}},
                "score": wt_score()}] if WTABLE else []),
            *[{"name": f"pad{j}", "patch": "juno-pad", "gain": "-20dB", "pan": (-0.4, -0.15, 0.15, 0.4)[j], "out": "pads", "score": T[f"pad{j}"]} for j in range(4)],
            *([{"name": "hum2", "patch": "sub-sine", "gain": "-14dB", "score": T["hum2"]}] if HUMOCT else []),
            *([{"name": "hum", "patch": "808", "gain": "-12dB", "fx": [{"type": "filter", "kind": "lp", "cutoff": 120, "q": 0.7}], "score": T["hum"]}] if HUM else []),
            {"name": "bass", "patch": "808", "gain": "-9dB", "fx": [pump], "score": T["bass"]},
            {"name": "kick", "patch": "909", "gain": "-3dB", "score": T["kick"]},
            *([{"name": "shk", "patch": "dusty-kit", "gain": "-12dB", "pan": 0.3, "fx": [{"type": "filter", "kind": "hp", "cutoff": 3500, "q": 0.7}], "score": T["shk"]}] if SHAKE else []),
            {"name": "hats", "patch": "909", "gain": "-9dB", "pan": 0.15, "score": "swing16=0.56 " + T["hats"]},
            {"name": "clap", "patch": "909", "gain": "-9dB", "sends": {"room": "-8dB"}, "score": T["clap"]},
            *([(sung_track(f"{SUNG}dB") if WORDS else reversed_back(sung_track(f"{SUNG}dB"), [sec_start("outro") + 8 * BAR], 1.758, 2.253))] if SUNG else []),
            *([reversed_back(voice("chirpers8-t8-say.json", "say", SAYOFFS, f"{VOX}dB",
                     ["hp cutoff=180"], {"line": "-2dB", "room": "-12dB"}), SAYOFFS, 1.421, 2.188)] if VOX and not WORDS else []),
            *([voice(f, nm, [o], f"{VOX}dB", ["hp cutoff=180"], {"line": "-2dB", "room": "-12dB"})
               for f, nm, o in zip(("chirpers8-t8-say-kept.json", "chirpers8-t8-say-both.json", "chirpers8-t8-say-around.json"), ("say", "say2", "say3"), SAYOFFS[-3:])]
              if VOX and WORDS else []),
            {"name": "rim", "patch": "909", "gain": "-12dB", "pan": -0.3, "sends": {"line": "-14dB"}, "score": T["rim"]},
        ],
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "vars", "tempo", "ceiling", "loudness", "seed", "tail", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
