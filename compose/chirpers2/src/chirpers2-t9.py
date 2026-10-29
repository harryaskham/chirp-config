#!/usr/bin/env python3
"""chirpers2-t9 "Slow Shutter" (Odd Hours, track 9) - generator for songs/chirpers2-t9.yaml (chirper-zero).

ECM SPACE: the album's breath before the closer. An 11/8 ostinato (3+3+3+2 eighths, quarter = 132) framed by
free-sounding passages written in long values over 5/4, 6/4 and 4/4 bars. The harmony moves EVERY bar through
major-seventh #11 colours (E lydian, C# aeolian, A lydian, F# dorian, D lydian, B sus, G lydian).

Form: dawn (free, piano alone and cymbal washes) -> ostinato (piano arpeggio + singing fretless, mallet toms) ->
song (the tenor high and slow over the ostinato, the guitar's delayed swells) -> open (free again: the guitar sings
over held chords) -> return (the tutti 11/8: tenor and guitar in octaves, full kit) -> dusk (free, the fretless and
piano alone, dissolving).

Motifs (compose/chirpers2/motifs.md):
  SHUTTER   the 11/8 ostinato: the fretless on each group's first eighth (root, fifth, ninth, octave: 3+3+3+2), the
            piano's arpeggio rotating its order every bar.
  EXPOSURE  the tenor's song: one long colour tone per bar (the 9th, #11 or 13th of each chord), approached by a leap.
Run: python3 compose/chirpers2/src/chirpers2-t9.py  (writes songs/chirpers2-t9.yaml)
"""
import json
import os
import random

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("T9_OUT") or os.path.join(ROOT, "songs", "chirpers2-t9.yaml")
MG = float(os.environ.get("T9_MG", "13"))
BPM = 132
DLY = os.environ.get("T9_DLY", "3/16")  # the guitar/tenor delay: 3/16 = a dotted eighth (echoes off the eighth grid)
EQ = os.environ.get("T9_EQ", "2")  # 1 = draft; 2 = mids -5 dB @500 q0.5, highshelf +4 @4k, lowshelf +5 @150
LOWROOT = os.environ.get("T9_LOWROOT", "1") == "1"  # the fretless's first group note an octave down (the low E)
KIT = os.environ.get("T9_KIT", "1")
STEADY = os.environ.get("T9_STEADY", "0") == "1"  # the ostinato as a figure: a fixed arpeggio contour and tom pattern (harmony still moves every bar)
DOTTED = os.environ.get("T9_DOTTED", "1") == "1"
RIDE3 = os.environ.get("T9_RIDE3", "1") == "1"
RECAP = os.environ.get("T9_RECAP", "1") == "1"
BASSOLO = os.environ.get("T9_BASSOLO", "0") == "1"
SEGUE = os.environ.get("T9_SEGUE", "1") == "1"
ARCH = os.environ.get("T9_ARCH", "1") == "1"
MOTIF = os.environ.get("T9_MOTIF", "1") == "1"
VIBES = os.environ.get("T9_VIBES", "1") == "1"
KLANG = os.environ.get("T9_KLANG", "1") == "1"
LIFT = int(os.environ.get("T9_LIFT", "0"))
CANON = os.environ.get("T9_CANON", "1") == "1"
HORNOPEN = os.environ.get("T9_HORNOPEN", "0") == "1"
HORNANS = os.environ.get("T9_HORNANS", "1") == "1"
FAREWELL = os.environ.get("T9_FAREWELL", "1") == "1"
LOWE = os.environ.get("T9_LOWE", "0") == "1"
VIB_DLY = os.environ.get("T9_VIBDLY", "-6")  # the dawn vibes' send to the dotted-eighth delay (dB): t8's coda echo, echoed back  # the dawn's first two bars: the fretless catches t8's last low E (E1), held and fading under the piano  # the dusk: the tenor's last EXPOSURE, in augmentation (a slow fourth up into each chord's 9th, held through the bar), over the arch  # the open section's horn ANSWERS inside each bar: the guitar's fourth, then late in the bar t4's sixth on the horn  # the open section as a dialogue: the french horn's EXPOSURE as t4 transformed it (a sixth up into a colour tone) on even bars, the guitar's fourth on odd  # in the return the strings answer the tenor in canon: last bar's EXPOSURE an octave down  # the return's last eight bars lifted (semitones; 3 = a minor third up): the climax rises  # EXPOSURE passes bar by bar tenor -> guitar -> piano in the song (chirper-one's note), whole again on the tenor in the return
VIB_BARS = int(os.environ.get("T9_VIBBARS", "4"))  # how many dawn bars the vibes answer in
VIB_DB = os.environ.get("T9_VIBDB", "-14")
VIB_DUSK = os.environ.get("T9_VIBDUSK", "0") == "1"  # the arch carries the vibes into the dusk too  # the vibes' track gain (dB)  # chirper-two's vibes (t8's c2-vibes, borrowed) answer t8's coda in the dawn, and come back in the dusk  # EXPOSURE as a sequence: every bar the leap of a fourth up into the chord's 9th (one shape carried down the changes)  # the dusk replays the dawn (its piano figures and washes, bar for bar) with the fretless singing over it: the day ends as it began  # under the last chord, Cierre's bembe bell arrives at Cierre's own tempo (eighths of 192 ms): the segue into the closer  # the open section becomes the fretless's solo (high, singing, sliding), the guitar swelling behind  # the return replays the song's EXPOSURE melody (a recapitulation) with the full band  # the ride on dotted eighths across the 11/8 (with the guitar): the cymbal's own cycle  # the guitar's dotted-eighth ostinato (0.75 beats: seven per 11/8 bar) in the ostinato and return  # 1 = kit -12 dB + highshelf -5 @4k; 2 = kit -10 dB, no shelf

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10, "B": 11}
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def NOTE_IDX(t):
    head = t.split("/", 1)[0]
    return 12 * (int(head[-1]) + 1) + NOTE[head[:-1]]


def transpose(piece, n):
    """Shift every pitched token (notes, comma chords) by n semitones; rests and kit pieces untouched."""
    if not n:
        return piece
    out = []
    for t in piece.split():
        if "/" not in t:
            out.append(t)
            continue
        head, rest = t.split("/", 1)
        parts = head.split(",")
        if all(p[:-1] in NOTE and p[-1].isdigit() for p in parts):
            head = ",".join(nm(12 * (int(p[-1]) + 1) + NOTE[p[:-1]] + n) for p in parts)
        out.append(head + "/" + rest)
    return " ".join(out)


def tok(n, d, v=None):
    return f"{n}/{d:g}b" + (f"@{int(max(1, min(127, v)))}" if v is not None else "")


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


# chirper-two's vibraphone from t8 Mallet Chamber in Phase (song-local c2-vibes, copied 29 Oct 05:1x; credited in sounds.md)
C2_VIBES = {"about": "chirper-two's vibraphone for Odd Hours t8: aluminium-bar partials 1 / 4 / 10 (tuned bars), a soft yarn-mallet tick, a long ring, and the MOTOR: a 5.2 Hz tremolo on the bar.", "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [4.0, 0.16], [10.0, 0.025]], "level": {"value": "0dB", "mod": [{"src": "lfo.motor", "amount": 3}]}}, {"name": "tick", "type": "noise", "level": {"value": "-72dB", "mod": [{"src": "env.tk", "amount": 36}]}}], "env": {"tk": {"a": "0.3ms", "d": "4ms", "s": 0}}, "lfo": {"motor": {"wave": "sine", "rate": "5.2hz"}}, "filters": ["hp cutoff=150", "lp cutoff=7k"], "amp": {"a": "2ms", "d": "3.2s", "s": 0, "r": "500ms", "curve": 2}}, "play": {"vel_sens": 0.55}}


# chords: bass root midi, voicing (piano), colour tones (pcs relative to root) for the melody
CH = {
    "Emaj9": (40, [54, 56, 59, 63], [2, 6, 11]),
    "C#m11": (37, [52, 56, 59, 66], [2, 5, 10]),
    "Amaj9#11": (45, [61, 63, 68, 71], [2, 6, 11]),
    "F#m9": (42, [57, 61, 64, 68], [2, 5, 10]),
    "Dmaj7#11": (38, [54, 56, 61, 64], [2, 6, 9]),
    "Bsus13": (35, [57, 61, 64, 68], [2, 5, 9]),
    "Gmaj9#11": (43, [54, 57, 61, 62], [2, 6, 9]),
    "B7sus": (35, [57, 61, 64, 66], [2, 5, 10]),
    "E/G#": (44, [52, 56, 59, 66], [2, 7, 10]),
    "Cmaj7#11": (36, [52, 54, 59, 62], [2, 6, 11]),
}
CYCLE = ["Emaj9", "C#m11", "Amaj9#11", "F#m9", "Dmaj7#11", "Bsus13", "Gmaj9#11", "B7sus"]
CYCLE2 = ["Emaj9", "E/G#", "Amaj9#11", "F#m9", "Dmaj7#11", "Cmaj7#11", "Gmaj9#11", "B7sus"]
FREE_BARS = [5, 6, 4, 5, 6, 4, 6, 5]  # the free passages' bar lengths (beats)

# (name, bars, beats per bar (None = FREE_BARS), chords)
FORM = [("dawn", 8, None, CYCLE), ("ostinato", 16, 5.5, CYCLE + CYCLE2), ("song", 16, 5.5, CYCLE + CYCLE2),
        ("open", 8, None, CYCLE2), ("return", 16, 5.5, CYCLE + CYCLE2), ("dusk", 6, None, CYCLE[:6])]
GROUPS = [0, 1.5, 3, 4.5]  # the 3+3+3+2 group starts in an 11/8 bar (beats)


def bar_beats(sec, b):
    beats = dict((n, bb) for n, _, bb, _ in FORM)[sec]
    return beats if beats else FREE_BARS[b % len(FREE_BARS)]


# ------------------------------------------------------------------ parts
def arpeggio(c, b, beats, vel=64):
    """Piano SHUTTER arpeggio in eighths over the 11/8 (or free bar): chord tones, order rotated every bar, an
    accent on each group's first eighth."""
    _, v, _ = CH[c]
    tones = v + [v[1] + 12, v[2] + 12]
    k = 0 if STEADY else b % len(tones)
    order = tones[k:] + tones[:k]
    if b % 2 and not STEADY:
        order = order[::-1]
    if STEADY:  # the SHUTTER contour: up the voicing, down from the top, per group
        order = [tones[i] for i in (0, 2, 4, 5, 3, 1)]
    out = []
    for i in range(int(beats * 2)):
        acc = (i * 0.5) in GROUPS
        out.append(tok(nm(order[i % len(order)]), 0.5, vel + (12 if acc else 0)))
    return J(*out)


def fretless(c, beats, b, sing=False):
    """The fretless on each group's first eighth: root, fifth, ninth, octave (3+3+3+2); in free bars one long root
    then a sung ninth."""
    r, _, _ = CH[c]
    if beats != 5.5:
        return J(tok(nm(r), beats - 1.5, 84), tok(nm(r + 14), 1.5, 74 if sing else 66))
    lo = r - 12 if LOWROOT else r
    notes = [lo, r + 7, r + 14, r + 12] if b % 2 == 0 else [lo, r + 12, r + 7, r + 14]
    durs = [1.5, 1.5, 1.5, 1]
    return J(*[tok(nm(n), d, 88 - 6 * i) for i, (n, d) in enumerate(zip(notes, durs))])


def bass_solo(c, beats, rng, vel=88):
    """The fretless sings: a high line (D3-A4) over the free bar - a long colour tone, a turn of three eighths, a
    held landing - with the mwah opening on each long note."""
    r, _, col = CH[c]
    cands = [m for m in range(50, 70) if (m - r) % 12 in col + [0, 7]]
    a = rng.choice(cands)
    b2 = min(cands, key=lambda m: abs(m - (a + rng.choice([-5, -3, 3, 5, 7]))))
    turn = [a + rng.choice([2, -1]), a + rng.choice([4, 1]), b2 + rng.choice([2, -2])]
    long1 = max(1.0, beats - 1.5 - 2.0)
    return J(tok(nm(a), long1, vel + 4), *[tok(nm(n), 0.5, vel - 8) for n in turn], tok(nm(b2), beats - long1 - 1.5, vel))


def held(c, beats, vel=56):
    _, v, _ = CH[c]
    return tok(",".join(nm(n) for n in v), beats, vel)


def exposure(c, beats, rng, lo=62, hi=81, vel=86, prev=None):
    """The EXPOSURE melody, one bar: a short pickup (a leap from below or above) into one long colour tone."""
    r, _, col = CH[c]
    cands = [m for m in range(lo, hi + 1) if (m - r) % 12 in col]
    tgt = rng.choice(cands) if prev is None else min(cands, key=lambda m: abs(m - prev) + rng.random() * 6)
    leap = tgt + rng.choice([-7, -5, -9, 5])
    if MOTIF:
        nines = [m for m in range(lo, hi + 1) if (m - r) % 12 == 2]
        tgt = nines[len(nines) // 2] if prev is None else min(nines, key=lambda m: abs(m - prev))
        leap = tgt - 5
    if beats >= 5:
        pick = [tok(nm(leap), 0.5, vel - 10), tok(nm(tgt), beats - 1.5, vel + 4), R(1)]
    else:
        pick = [tok(nm(tgt), beats - 0.5, vel), R(0.5)]
    return J(*pick), tgt


def guitar_swell(c, beats, rng, vel=60):
    """Delayed clean guitar: two colour tones high, placed late in the bar (swells into the delay)."""
    r, _, col = CH[c]
    cands = [m for m in range(64, 84) if (m - r) % 12 in col]
    a, b2 = sorted(rng.sample(cands, 2))
    off = rng.choice([1.5, 3, 0.5])
    return J(R(off), tok(f"{nm(a)},{nm(b2)}", beats - off, vel))


def dotted(c, beats, vel=64):
    """The guitar's dotted-eighth ostinato: colour tones cycling every 0.75 beat (seven per 11/8 bar, a sixteenth rest)."""
    r, v, col = CH[c]
    tones = sorted({m for m in range(64, 80) if (m - r) % 12 in col + [0, 7]})[:4]
    n = int(beats / 0.75)
    out = [tok(nm(tones[i % len(tones)]), 0.75, vel + (8 if i == 0 else 0)) for i in range(n)]
    return J(*out, R(beats - 0.75 * n))


def mallets(beats, b, rng, full=False, vel=70):
    """Drums: mallet toms on the group starts (t2 t1 t2 ft), ride washes; `full`: kick on 1 and 3+, snare on the
    third group, ride in eighths, a crash at the phrase starts."""
    n8 = int(beats * 2)
    hits = {i: [] for i in range(n8)}
    toms = ["t2", "t1", "t2", "ft"] if (b % 2 == 0 or STEADY) else ["ft", "t2", "t1", "t2"]
    for g, t in zip(GROUPS, toms):
        i = int(g * 2)
        if i < n8:
            hits[i].append(t if not full or g in (1.5,) else ("k" if g == 0 else ("s" if g == 3 else t)))
    for i in range(0, n8, 1 if full else 3):
        hits[i].append("rd")
    if full and b % 4 == 0:
        hits[0].append("c")
    if rng.random() < 0.4:
        r2 = rng.randrange(n8)
        if not STEADY:
            hits[r2].append("so")
    if RIDE3 and beats == 5.5:  # on a sixteenth grid: the toms/kick/snare where they were, the ride every three sixteenths
        n16 = int(beats * 4)
        h16 = {i: [p for p in hits.get(i // 2, []) if p != "rd"] if i % 2 == 0 else [] for i in range(n16)}
        for i in range(0, n16, 3):
            h16[i].append("rd")
        out = []
        for i in range(n16):
            if h16[i]:
                out.append(",".join(dict.fromkeys(h16[i])) + f"/0.25b@{vel + (8 if i == 0 else 0) - (0 if i % 2 == 0 else 6)}")
            else:
                out.append(R(0.25))
        for i in range(n8):
            if hits[i]:
                rng.randint(-6, 4)  # keep the RNG stream
        return J(*out)
    out = []
    for i in range(n8):
        if hits[i]:
            out.append(",".join(dict.fromkeys(hits[i])) + f"/0.5b@{vel + (8 if i == 0 else 0) + rng.randint(-6, 4)}")
        else:
            out.append(R(0.5))
    return J(*out)


def wash(beats, vel=46):
    """A soft ride roll swelling across a free bar (sixteenths, crescendo into the next bar)."""
    n = int(beats * 4)
    return J(R(beats / 2), *[tok("rd", 0.25, vel + int(30 * i / max(1, n // 2))) for i in range(n // 2)])


def cut(piece, beats):
    out, pos = [], 0.0
    for t in piece.split():
        if pos >= beats - 1e-9:
            break
        head, rest = t.split("/", 1)
        dur = rest.split("b", 1)[0]
        tail = rest[len(dur) + 1:]
        d = float(dur)
        out.append(f"{head}/{min(d, beats - pos):g}b{tail}")
        pos += d
    if pos < beats - 1e-9:
        out.append(R(beats - pos))
    return " ".join(out)


# ------------------------------------------------------------------ arrangement
def build():
    names = ("piano", "bass", "tenor", "gtr", "strings", "kit") + (("vibes",) if VIBES else ()) + (("pmel",) if KLANG else ()) + (("horn",) if (HORNOPEN or HORNANS) else ())
    T = {n: [] for n in names}
    seg_at = [0.0]
    beat_pos = 0.0
    rng = random.Random(9)
    times, t = {}, 0.0
    prev = None
    song_lines = []
    dawn_bars = []
    for si, (sec, nb, _, chs) in enumerate(FORM):
        start = t
        for b in range(nb):
            beats = bar_beats(sec, b)
            c = chs[b % len(chs)]
            bar = {n: R(beats) for n in names}
            if sec == "dawn":
                bar["piano"] = J(held(c, beats - 0.5, 50 + 2 * b), R(0.5)) if b % 2 == 0 else arpeggio(c, b, beats, 48)
                if LOWE and b < int(os.environ.get("T9_LOWEBARS", "2")):  # t8 ends on a low E (its bass marimba); the fretless holds it into the dawn
                    bar["bass"] = tok("E1", beats, int(os.environ.get("T9_LOWEVEL", "70")) - 12 * b)
                if VIBES and b < VIB_BARS:  # t8's vibes answer: one colour tone per bar, struck with the piano and left to ring under the motor
                    r, _, col = CH[c]
                    tone = [m for m in range(72, 89) if (m - r) % 12 in col][b % 3]
                    bar["vibes"] = J(tok(nm(tone), beats - 0.5, 70 + b), R(0.5))
                bar["kit"] = wash(beats) if b % 2 == 1 else R(beats)
                if b >= 4:
                    bar["strings"] = held(c, beats, 40)
                dawn_bars.append(dict(bar))
            elif sec == "ostinato":
                bar["piano"] = arpeggio(c, b, beats, 60 + b // 2)
                bar["bass"] = fretless(c, beats, b) if b >= 2 else R(beats)
                bar["kit"] = mallets(beats, b, rng, vel=62) if b >= 4 else R(beats)
                if b >= 8:
                    bar["strings"] = held(c, beats, 44)
                    if DOTTED:
                        bar["gtr"] = dotted(c, beats, 58)
            elif sec == "song":
                bar["piano"] = arpeggio(c, b, beats, 58)
                bar["bass"] = fretless(c, beats, b)
                bar["kit"] = mallets(beats, b, rng, vel=66)
                bar["tenor"], prev = exposure(c, beats, rng, vel=84 + b // 2, prev=prev)
                song_lines.append(bar["tenor"])
                if b % 2 == 1:
                    bar["gtr"] = guitar_swell(c, beats, rng)
                if KLANG and b % 3 == 1:  # the guitar takes the bar's gesture (its swell steps aside)
                    bar["gtr"], bar["tenor"] = bar["tenor"], R(beats)
                elif KLANG and b % 3 == 2:  # the piano's right hand takes it, an octave up, over its own arpeggio
                    bar["pmel"] = " ".join(t if t.startswith("R/") else nm(NOTE_IDX(t) + 12) + "/" + t.split("/", 1)[1] for t in bar["tenor"].split())
                    bar["tenor"] = R(beats)
            elif sec == "open":
                bar["strings"] = held(c, beats, 48)
                bar["bass"] = fretless(c, beats, b, sing=True)
                bar["gtr"], prev = exposure(c, beats, rng, lo=64, hi=86, vel=82, prev=prev)
                if HORNANS:  # call and response in every bar: the guitar's gesture, then the horn's sixth answering it late
                    r, _, col = CH[c]
                    tgts = [m for m in range(60, 77) if (m - r) % 12 in col]
                    tgt = min(tgts, key=lambda m: abs(m - ((prev or 82) - 12)))
                    bar["horn"] = J(R(beats - 2.5), tok(nm(tgt - 9), 0.5, 72), tok(nm(tgt), 2, 82))
                if HORNOPEN and b % 2 == 0:  # chirper-two's answer in t4's coda, answered: the horn leaps a sixth
                    r, _, col = CH[c]
                    tgts = [m for m in range(60, 77) if (m - r) % 12 in col]
                    tgt = min(tgts, key=lambda m: abs(m - (prev or 70)))
                    bar["horn"] = J(tok(nm(tgt - 9), 1, 74), tok(nm(tgt), beats - 2, 84), R(1))
                    bar["gtr"] = R(beats)
                if BASSOLO:
                    bar["bass"] = bass_solo(c, beats, rng)
                    bar["gtr"] = guitar_swell(c, beats, rng, vel=54)
                    bar["piano"] = J(tok(nm(CH[c][0] - 12 + 24), beats, 52))  # the piano holds the root low, the bass is free
                bar["kit"] = wash(beats, 40) if b % 2 == 0 else R(beats)
                if b % 2 == 1:
                    bar["piano"] = J(R(1), held(c, beats - 1, 46))
            elif sec == "return":
                bar["piano"] = arpeggio(c, b, beats, 70)
                bar["bass"] = fretless(c, beats, b)
                bar["kit"] = mallets(beats, b, rng, full=True, vel=82)
                line, prev = exposure(c, beats, rng, lo=64, hi=84, vel=96, prev=prev)
                if RECAP and b < len(song_lines):
                    line = " ".join(t if t.startswith("R/") else t.rsplit("@", 1)[0] + f"@{min(127, int(t.rsplit('@', 1)[1]) + 10)}"
                                    for t in song_lines[b].split())
                bar["tenor"] = line
                bar["gtr"] = dotted(c, beats, 66) if DOTTED else " ".join(x if x.startswith("R/") else x.replace("/", "/", 1) for x in line.split())
                bar["strings"] = held(c, beats, 56)
            elif sec == "dusk":
                bar["bass"] = fretless(c, beats, b, sing=True)
                bar["piano"] = arpeggio(c, b, beats, 44 - 2 * b) if b % 2 == 0 else J(held(c, beats - 1, 40), R(1))
                if FAREWELL and b < nb - 1:  # the melody's farewell: the gesture slowed, a long pickup into the 9th
                    r = CH[c][0]
                    nines = [m for m in range(62, 80) if (m - r) % 12 == 2]
                    tgt = min(nines, key=lambda m: abs(m - 71))
                    bar["tenor"] = J(tok(nm(tgt - 5), 1.5, 66 - 2 * b), tok(nm(tgt), beats - 2, 72 - 2 * b), R(0.5))
                if ARCH and b < nb - 1 and b < len(dawn_bars) and bar_beats("dawn", b) == beats:
                    for k in ("piano", "kit", "strings") + (("vibes",) if VIBES and VIB_DUSK else ()):
                        bar[k] = dawn_bars[b][k]
                if b == nb - 1:
                    seg_at[0] = beat_pos
                    bar["piano"] = held("Emaj9", beats * 2, 46)
                    bar["bass"] = tok("E2", beats * 2, 70)
                    bar["strings"] = held("Emaj9", beats * 2, 38)
            if CANON and sec == "return" and b > 0:
                prev_line = T["tenor"][-1]
                if prev_line and not prev_line.startswith("R/"):
                    bar["strings"] = " ".join(t if t.startswith("R/") else t.rsplit("@", 1)[0] + "@64" for t in transpose(prev_line, -12).split())
            if LIFT and sec == "return" and b >= nb - 8:
                for k in ("piano", "bass", "tenor", "gtr", "strings"):
                    bar[k] = transpose(bar[k], LIFT)
            if b == nb - 1 and sec != "dusk":  # the break: the band stops at the bar's middle, the toms fill
                half = int(beats) // 2 + 0.5 * (beats % 1 == 0.5) if beats != 5.5 else 3
                for n in names:
                    if n != "kit":
                        bar[n] = J(cut(bar[n], half), R(beats - half))
                n16 = int((beats - half) * 4)
                fill = [("t1" if i % 3 == 0 else "t2" if i % 3 == 1 else "ft") + f"/0.25b@{60 + 3 * i}" for i in range(n16 - 2)]
                bar["kit"] = J(cut(bar["kit"], half), *fill, tok("c,k", 0.5, 100))
            for n in names:
                T[n].append(bar[n])
            t += beats * 60 / BPM
            beat_pos += beats
        times[sec] = (start, t)
    if SEGUE:  # Cierre's bembe bell (x.x.xx.x.x.x), two cycles at dotted quarter = 104, rising from silence
        pat = "x.x.xx.x.x.x" * 2
        toks = [f"cow/192ms@{int(34 + 50 * i / len(pat))}" if ch == "x" else "R/192ms" for i, ch in enumerate(pat)]
        T["bell"] = [f"R/{seg_at[0]:g}b " + " ".join(toks)]
    return T, times


def master(times):
    bands = (["lowshelf cutoff=150 gain=5dB", "peak cutoff=700 q=0.7 gain=-2dB", "highshelf cutoff=6000 gain=-3dB"] if EQ == "1" else
             ["lowshelf cutoff=150 gain=5dB", "peak cutoff=500 q=0.5 gain=-5dB", "highshelf cutoff=4000 gain=4dB"])
    fx = [{"type": "eq", "bands": bands},
          {"type": "compressor", "threshold": "-22dB", "ratio": 2, "attack": "20ms", "release": "250ms", "makeup": "0dB"},
          {"type": "gain", "gain": f"+{MG:g}dB"}]
    lv = {"dawn": -8, "ostinato": -4, "song": -1, "open": -5, "return": 2, "dusk": -7}
    pts = [["0s", lv["dawn"]]]
    for sec, *_ in FORM[1:]:
        a = times[sec][0]
        pts += [[f"{a - 0.6:.2f}s", pts[-1][1]], [f"{a:.2f}s", lv[sec]]]
    pts += [[f"{times['dusk'][1] + 12:.2f}s", lv["dusk"]]]
    fx.append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}})
    return {"fx": fx, "auto": {"dyn": {"points": pts}}}


def song():
    T, times = build()

    def sc(name):
        return " | ".join(x for x in T[name] if x)

    tracks = [
        {"name": "piano", "patch": "piano", "gain": "-7dB", "pan": -0.15, "sends": {"hall": "-8dB"}, "score": sc("piano")},
        {"name": "bass", "patch": "fretless", "gain": "-2dB", "sends": {"hall": "-14dB"}, "score": sc("bass")},
        {"name": "tenor", "patch": "tenor-sax", "gain": "-6dB", "pan": 0.15, "sends": {"hall": "-6dB", "dly": "-12dB"}, "score": sc("tenor")},
        {"name": "gtr", "patch": "starcaster-clean", "gain": "-9dB", "pan": 0.35, "sends": {"hall": "-5dB", "dly": "-6dB"}, "score": sc("gtr")},
        {"name": "strings", "patch": "mellotron-strings", "gain": "-14dB", "pan": -0.3, "sends": {"hall": "-6dB"}, "score": sc("strings")},
        {"name": "kit", "patch": "room-kit", "gain": "-12dB", "sends": {"hall": "-10dB"},
         "fx": [{"type": "eq", "bands": ["highshelf cutoff=4000 gain=-5dB"]}], "score": sc("kit")},
    ]
    if HORNOPEN or HORNANS:
        tracks.append({"name": "horn", "patch": "horn", "gain": "-7dB", "pan": -0.25, "sends": {"hall": "-6dB"}, "score": sc("horn")})
    if KLANG:
        tracks.append({"name": "pmel", "patch": "piano", "gain": "-5dB", "pan": -0.1, "sends": {"hall": "-7dB"}, "score": sc("pmel")})
    if VIBES:
        tracks.append({"name": "vibes", "patch": "c2-vibes", "gain": f"{VIB_DB}dB", "pan": 0.25, "sends": {"hall": "-8dB", "dly": f"{VIB_DLY}dB"}, "score": sc("vibes")})
    if SEGUE:
        tracks.append({"name": "bell", "patch": "room-kit", "gain": "-12dB", "pan": -0.35, "sends": {"hall": "-10dB"}, "score": sc("bell")})
    if KIT == "2":
        tracks[-1]["gain"] = "-10dB"
        del tracks[-1]["fx"]
    return {
        "about": ("Chirpers - Odd Hours, track 9: Slow Shutter (original composition, chirper-zero; generator "
                  "compose/chirpers2/src/chirpers2-t9.py). ECM space: an 11/8 ostinato (3+3+3+2, quarter = 132) framed "
                  "by free-sounding passages in long values; the harmony moves every bar through lydian colours. dawn -> "
                  "ostinato -> song (high tenor) -> open (the guitar sings) -> return (tutti 11/8) -> dusk on Emaj9."),
        "tempo": BPM, "ceiling": "-0.1dB", "tail": "4s",
        **({"patches": {"c2-vibes": C2_VIBES}} if VIBES else {}),
        "buses": {"hall": {"fx": ["reverb kind=hall decay=4.5s size=0.95 mix=1 predelay=40ms"]},
                  "dly": {"fx": [f"delay time={DLY} feedback=0.45 mix=1 tone=2500"]}},
        "master": master(times),
        "tracks": tracks,
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "tail") + (("patches",) if "patches" in doc else ()) + ("master",)]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
