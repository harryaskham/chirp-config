#!/usr/bin/env python3
"""chirpers2-t10 (Odd Hours, the closer) - generator for songs/chirpers2-t10.yaml (chirper-zero).

AFRO-CUBAN / LATIN-JAZZ CLOSER: a suite in clave, D minor, that grows from an intimate 12/8 bembe into a son
montuno, a horn mambo, a 7/4 interlude, an afro 12/8 descarga and a final cierre. Metric modulation keeps one pulse:
the bembe's dotted quarter (104) becomes the son's half note (208 bpm 4/4); the 7/4 keeps the quarter; the descarga
pushes the dotted quarter to 116.

Motifs (compose/chirpers2/motifs.md):
  MONTUNO      the piano's 2-bar figure in eighths (x.x.xx.x | .xx.x.xx), dyads walking the chord's top voice; it
               displaces by an eighth every fourth bar and passes to the horns in the mambo.
  CLAVE STRETCH the son clave's 3-side (1, 2&, 4) stretched over 7 quarters as 3+2+2 in the 7/4 interlude.
  CORO         the descarga's call: D5 C5 A4 | G4 A4 (dotted), answered by the trumpet, a step higher each time round.
Bar by bar: the clave flips 3-2 / 2-3 at section seams, the bembe bell alternates 6/8 and 3/4 groupings, chords
re-voice every bar, the tumbao anticipates the next chord, melody passes piano -> trumpet -> horns -> rhodes -> tenor.
Run: python3 compose/chirpers2/src/chirpers2-t10.py  (writes songs/chirpers2-t10.yaml)
"""
import json
import os
import random

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("T10_OUT") or os.path.join(ROOT, "songs", "chirpers2-t10.yaml")
MG = float(os.environ.get("T10_MG", "10"))
DYN = os.environ.get("T10_DYN", "1") == "1"
EQ = os.environ.get("T10_EQ", "2")  # master eq: 1 = v1 (shelf +3 @100, 800 -2); 2 = shelf +6 @120, 700 q0.6 -3
LOWB = os.environ.get("T10_LOWB", "0") == "1"  # the tumbao's anticipated root an octave lower (the baby bass's floor)
KICK = os.environ.get("T10_KICK", "0") == "1"  # more bombo: the ponche on 4 in the mambo/cierre, dotted quarters in the descarga
SEAM = os.environ.get("T10_SEAM", "1") == "1"  # every section's last bar breaks at its middle into a timbale fill (the seams read)
MAMBO_KEY = int(os.environ.get("T10_MAMBOKEY", "0"))  # the mambo transposed (semitones): +5 = up a fourth, to G minor
QUOTE = os.environ.get("T10_QUOTE", "1") == "1"  # the 7/4 interlude quotes the album's opener: SEVEN DOORS (t1 Doors at Seven), up a step into D
MONA = os.environ.get("T10_MONA", "cierre") in ("1", "cierre")  # the mona: a second horn riff interlocking with the mambo's
MONA_WHERE = os.environ.get("T10_MONA", "cierre")  # "1": the mambo's second half and the shout; "cierre": the shout only
CONGAS = os.environ.get("T10_CONGAS", "1") == "1"  # real congas on the physical drum layer (quinto, conga, slap) for the kit's toms
CONGA_DB = float(os.environ.get("T10_CONGADB", "0"))  # the congas' level offset (dB)
CONGA_EQ = os.environ.get("T10_CONGAEQ", "0") == "1"  # a 250 Hz -3 dB cut on the congas (the box)
KEEP_FT = os.environ.get("T10_KEEPFT", "1") == "1"  # keep the room-kit floor tom under the congas (its low end) instead of the tumba
SUNG = os.environ.get("T10_SUNG", "1") == "1"  # the descarga's CORO sung: a baritone (maynard) an octave under, wordless dream voices at pitch
QUINTO = os.environ.get("T10_QUINTO", "1") == "1"  # the quinto improvises in the descarga's solo bars: open tones and slaps drawn per bar
PSOLO = os.environ.get("T10_PSOLO", "1") == "1"  # a 16-bar piano solo over the montuno groove between the son and the mambo (octave lines, horns out)

# sections: (name, meter, bpm (quarter), bars)
FORM = [("bembe", "12/8", 156, 12), ("son", "4/4", 208, 40), ("mambo", "4/4", 208, 24), ("siete", "7/4", 208, 12),
        ("descarga", "12/8", 174, 28), ("cierre", "4/4", 208, 10)]
if PSOLO:
    FORM.insert(2, ("psolo", "4/4", 208, 16))
BEATS = {"12/8": 6, "4/4": 4, "7/4": 7}

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10, "B": 11}
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def mi(n):
    p, o = n[:-1], int(n[-1])
    return 12 * (o + 1) + NOTE[p]


def tok(n, d, v=None, art=""):
    return f"{n}/{d:g}b" + (f"@{int(v)}" if v is not None else "") + art


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def transpose(piece, n):
    """Shift every pitched token (notes and comma chords) by n semitones; rests and kit pieces untouched."""
    if not n:
        return piece
    out = []
    for t in piece.split():
        head, rest = t.split("/", 1) if "/" in t else (t, None)
        parts = head.split(",")
        if all(p[:-1] in NOTE and p[-1].isdigit() for p in parts):
            head = ",".join(nm(mi(p) + n) for p in parts)
        out.append(head + ("/" + rest if rest is not None else ""))
    return " ".join(out)


def cut(piece, beats):
    """The first `beats` of a bar's tokens (notes clipped at the cut)."""
    out, pos = [], 0.0
    for t in piece.split():
        if pos >= beats - 1e-9:
            break
        head, rest = t.split("/", 1)
        dur = rest.split("b", 1)[0]
        tail = rest[len(dur) + 1:]
        d = float(dur)
        d2 = min(d, beats - pos)
        out.append(f"{head}/{d2:g}b{tail}")
        pos += d
    if pos < beats - 1e-9:
        out.append(R(beats - pos))
    return " ".join(out)


def chord(names):
    return ",".join(names)


# harmony (voicings as midi lists; root for the bass)
CH = {
    "Dm9": (38, [53, 57, 60, 64]),        # F A C E over D
    "Gm9/D": (38, [53, 58, 62, 69]),      # F Bb D A (pedal D)
    "G13": (43, [53, 59, 64, 69]),        # F B E A
    "Cmaj7#11": (36, [52, 54, 59, 64]),   # E F# B E
    "A7b13": (45, [55, 61, 65, 70]),      # G C# F Bb
    "Bbmaj7#11": (46, [57, 62, 64, 69]),  # A D E A
    "A7sus": (45, [55, 62, 64, 71]),      # G D E B
    "Dm11": (38, [53, 55, 60, 64]),       # F G C E
    "Em11": (40, [55, 57, 62, 66]),       # G A D F#
    "Dmaj9#11": (38, [54, 57, 61, 64, 68]),  # F# A C# E G#
    "Ebmaj7#11": (39, [55, 57, 62, 65]),  # G A D F (Eb lydian)
}
SON_PROG = ["Dm9", "G13", "Cmaj7#11", "A7b13"]


SEVEN_DOORS = [  # t1 Doors at Seven's head (chirper-zero), quoted in the 7/4 interlude a whole step up (C -> D dorian)
    [("C5", 1.5), ("Bb4", 0.5), ("G4", 1), ("F4", 1), ("Eb4", 1), ("F4", 2)],
    [("G4", 0.5), ("Bb4", 0.5), ("C5", 0.5), ("D5", 0.5), ("Eb5", 3), ("R", 2)],
    [("F5", 1), ("Eb5", 0.5), ("C5", 0.5), ("Ab4", 2), ("G4", 1), ("Ab4", 2)],
    [("Bb4", 0.5), ("C5", 0.5), ("Db5", 1), ("Eb5", 1), ("F5", 1), ("G5", 3)],
    [("Eb5", 1.5), ("D5", 0.5), ("C5", 1), ("Bb4", 1), ("G4", 3)],
    [("F4", 0.5), ("G4", 0.5), ("Bb4", 1), ("C5", 0.5), ("D5", 0.5), ("F5", 4)],
    [("Eb5", 1), ("Db5", 1), ("B4", 1), ("Ab4", 1), ("F4", 1), ("Eb4", 2)],
    [("D4", 1), ("F4", 0.5), ("Ab4", 0.5), ("B4", 1), ("D5", 1), ("C5", 3)],
]
QUOTE_CH = ["Dm11", "Dm11", "Ebmaj7#11", "Ebmaj7#11", "Dm11", "Dm11", "A7b13", "A7b13"]
MONA_RIFF = [  # the mona: low horns in the mambo riff's gaps
    [("D4", 1), ("R", 0.5), ("F4", 0.5), ("E4", 1), ("R", 1)],
    [("R", 0.5), ("C4", 0.5), ("D4", 1), ("R", 0.5), ("A3", 1.5)],
]


def harm(sec, b):
    if sec == "bembe":
        return ["Dm9", "Gm9/D"][b % 2]
    if sec in ("son", "mambo", "cierre", "psolo"):
        return SON_PROG[b % 4]
    if sec == "siete":
        if QUOTE and b < 8:
            return QUOTE_CH[b]
        return ["Bbmaj7#11", "A7sus"][(b // 2) % 2]
    if sec == "descarga":
        return "Dm11" if b < 16 else "Em11"
    return "Dm9"


def voicing(c, b):
    """Re-voice every bar: rotate the top voice up an octave on odd bars (inversions walk)."""
    root, v = CH[c]
    v = list(v)
    if b % 2:
        v = v[1:] + [v[0] + 12]
    return root, v


# ---------------------------------------------------------------- parts per bar
def montuno(c, b, disp=0, vel=86):
    """Piano MONTUNO in eighths: 2-bar figure; dyads of the top voice and the voice an octave below; displaced by
    `disp` eighths (the displacement shifts every 4th bar)."""
    root, v = voicing(c, b)
    top = sorted(v)[-2:]
    pat = "x.x.xx.x" if b % 2 == 0 else ".xx.x.xx"
    pat = (pat[-disp:] + pat[:-disp]) if disp else pat
    out = []
    for i, ch in enumerate(pat):
        if ch == "x":
            n = top[i % 2]
            out.append(tok(chord([nm(n - 12), nm(n)]), 0.5, vel - (10 if i % 2 else 0)))
        else:
            out.append(R(0.5))
    return J(*out)


def comp(c, b, beats, vel=70, style="block"):
    """A held or stabbed chord for keys/pads."""
    root, v = voicing(c, b)
    names = chord([nm(n) for n in v])
    if style == "block":
        return tok(names, beats, vel)
    if style == "stab":  # two stabs: on 1 and the and of 2 (4/4) / on 1 and 4 (12/8)
        if beats == 4:
            return J(tok(names, 1, vel), R(0.5), tok(names, 1, vel - 8), R(1.5))
        return J(tok(names, 1.5, vel), tok(names, 1.5, vel - 8), R(3))
    return tok(names, beats, vel)


def tumbao(c, nxt, b, beats):
    """Bass: in 4/4 the son tumbao - the next chord's root anticipated on 2&, its fifth on 4 (tied feel); in 12/8 the
    bembe bass on dotted quarters; in 7/4 a 3+2+2 ostinato."""
    r = CH[c][0]
    rn = CH[nxt][0]
    lo = -12 if LOWB else 0
    if beats == 4:
        return J(R(1.5), tok(nm(rn + lo), 1.5, 96), tok(nm(rn + 7), 1, 88))
    if beats == 6:
        return J(tok(nm(r + lo), 1.5, 92), R(1.5), tok(nm(r + 7), 1, 84), tok(nm(r + 12), 0.5, 80), tok(nm(r), 1.5, 90))
    if beats == 7:
        return J(tok(nm(r), 3, 94), tok(nm(r + 7), 2, 86), tok(nm(r + 10), 2, 84))
    return tok(nm(r), beats, 90)


def clave(beats, side):
    """Son clave in 4/4 (3-side: 1, 2&, 4 ; 2-side: 2, 3); the CLAVE STRETCH in 7/4 (3+2+2: 1, 4, 6, and a ghost on 7&)."""
    if beats == 4:
        return J(tok("clv", 1.5, 100), tok("clv", 1.5, 96), tok("clv", 1, 100)) if side == 3 else J(R(1), tok("clv", 1, 98), tok("clv", 2, 98))
    if beats == 7:
        return J(tok("clv", 3, 102), tok("clv", 2, 96), tok("clv", 1.5, 96), tok("clv", 0.5, 70))
    return R(beats)


def bell(beats, b, hemiola=False):
    """The bembe bell over a 12/8 bar (eighths): x.x.xx.x.x.x; on hemiola bars the 3/4 grouping (every quarter)."""
    pat = "x.x.x.x.x.x." if hemiola else "x.x.xx.x.x.x"
    return J(*[tok("cow", 0.5, 100 if i == 0 else 84) if c == "x" else R(0.5) for i, c in enumerate(pat)])


def drums(sec, b, beats, dens=1):
    """The kit + congas (t1 = quinto, t2 = conga, ft = tumba) and shaker, one token per eighth (12/8, 4/4, 7/4)."""
    n8 = int(beats * 2)
    out = []
    for i in range(n8):
        h = []
        if sec in ("bembe", "descarga"):
            if i % 1 == 0:
                h.append("shk")
            if i in (3, 4, 9, 10):
                h.append("t2")
            if i in (0, 6) and (sec == "descarga" or b >= 4):
                h.append("k")
            if KICK and sec == "descarga" and i in (3, 9):
                h.append("k")
            if sec == "descarga" and i in (5, 11):
                h.append("t1")
            if sec == "descarga" and dens > 1 and i in (3, 9):
                h.append("s")
        elif sec in ("son", "mambo", "cierre", "psolo"):
            # cascara-ish ride bell on quarters, conga tumbao (open tones on 4 and 4&), bombo on 2& of the 3-side bar
            if i % 2 == 0:
                h.append("rbs" if sec != "son" or b >= 8 else "cowm")
            if i in (6, 7):
                h.append("t2")
            if i == 5:
                h.append("ft")
            if i == 3 and b % 2 == 0:
                h.append("k")
            if KICK and sec != "son" and i == 6:
                h.append("k")
            if sec != "son" and i in (2, 6):
                h.append("so")
            if dens > 1 and i in (2, 6):
                h.append("s")
        elif sec == "siete":
            if i % 2 == 0:
                h.append("rc")
            if i in (0, 6, 10):
                h.append("k")
            if i in (4, 8, 12):
                h.append("so")
        if CONGAS and QUINTO and sec == "descarga" and b % 4 in (2, 3):
            if i == 0:
                qr = random.Random(1000 + b)
                qpat = {j: qr.choice(["qo", "qo", "cs", "qo,co", "co"]) for j in range(n8) if qr.random() < 0.45}
            if i in qpat:
                h = [x for x in h if x != "t1"] + qpat[i].split(",")
        if CONGAS:
            h = [{"t1": "qo", "t2": "co", "ft": ("ft" if KEEP_FT else "to")}.get(x, x) for x in h]
            if sec in ("son", "mambo", "cierre", "psolo") and i == 2:
                h.append("cs")  # the tumbao's slap on 2
            if sec in ("bembe", "descarga") and i in (2, 8):
                h.append("cs")
        v = 92 if (i == 0) else 74
        out.append((",".join(h) + f"/0.5b@{v}") if h else R(0.5))
    return J(*out)


THEME = [  # trumpet's son theme, 4 bars of 4/4 over the progression
    [("A4", 1.5), ("G4", 0.5), ("F4", 1), ("E4", 1)],
    [("D4", 1), ("F4", 0.5), ("A4", 1), ("C5", 1.5)],
    [("E5", 1), ("D5", 0.5), ("B4", 0.5), ("F#4", 2)],
    [("G4", 0.5), ("Bb4", 0.5), ("C#5", 1), ("E5", 2)],
]
SIETE = [[("A4", 2), ("E5", 1), ("D5", 2), ("A4", 2)], [("G4", 3), ("B4", 2), ("E5", 2)]]  # rhodes, 7/4
CORO = [("D5", 1.5), ("C5", 1.5), ("A4", 3)], [("G4", 1.5), ("A4", 4.5)]  # 12/8, two bars
MAMBO = [  # horn-section mambo riff (4/4), answering the montuno: short, punchy, syncopated
    [("R", 0.5), ("A4", 0.5), ("C5", 0.5), ("D5", 0.5), ("R", 0.5), ("F5", 1), ("R", 0.5)],
    [("E5", 0.5), ("R", 0.5), ("D5", 0.5), ("C5", 1), ("A4", 0.5), ("R", 1)],
]


SCALES = {"Dm9": [0, 2, 3, 5, 7, 9, 10], "G13": [0, 2, 4, 5, 7, 9, 10], "Cmaj7#11": [0, 2, 4, 6, 7, 9, 11],
          "A7b13": [0, 1, 3, 4, 6, 8, 10]}
PSOLO_RHY = ["x.xx.x.x", ".x.xx.xx", "xx.x.xx.", "x..x.x.x"]  # the solo's eighth-note cells; bar 4 of each 4 repeats bar 1's


def piano_solo(c, b, rng, vel=90):
    """The piano's solo over the montuno: a right hand in octaves (dyads an octave apart), lines drawn from the
    chord's scale in syncopated eighth cells, the top climbing over the 16 bars."""
    root = CH[c][0] % 12
    pcs = {(root + x) % 12 for x in SCALES[c]}
    lo, hi = 67 + b // 2, 84 + b // 2
    pool = [m for m in range(lo, hi + 1) if m % 12 in pcs]
    cell = PSOLO_RHY[(b % 4) if b % 4 != 3 else 0]
    i = rng.randrange(len(pool) // 3, 2 * len(pool) // 3)
    up = rng.random() < 0.5
    out = []
    for k, ch in enumerate(cell):
        if ch == "x":
            m = pool[i]
            out.append(tok(f"{nm(m - 12)},{nm(m)}", 0.5, vel + (6 if k == 0 else 0) - (8 if k % 2 else 0)))
            i += (1 if up else -1) * rng.choice([1, 1, 2])
            if i <= 0 or i >= len(pool) - 1:
                up = not up
                i = max(0, min(len(pool) - 1, i))
        else:
            out.append(R(0.5))
    return J(*out)


def line(notes, vel=92, shift=0):
    out = []
    for n, d in notes:
        out.append(R(d) if n == "R" else tok(nm(mi(n) + shift), d, vel))
    return J(*out)


def solo_bar(b, beats, scale_root=62, seed=0, vel=88):
    """A composed 'improvised' line: a dorian run in eighths with a held note at the end, contour by bar."""
    dor = [0, 2, 3, 5, 7, 9, 10]
    n8 = int(beats * 2)
    out, step = [], (b * 3 + seed) % 7
    up = (b + seed) % 2 == 0
    for i in range(n8 - 2):
        deg = dor[step % 7] + 12 * (step // 7)
        out.append(tok(nm(scale_root + deg), 0.5, vel - (0 if i % 2 == 0 else 8)))
        step += (1 if up else -1) * (1 if i % 3 else 2)
        step = max(-3, min(10, step))
    out.append(tok(nm(scale_root + dor[step % 7] + 12 * (step // 7)), 1, vel + 4))
    return J(*out)


# ---------------------------------------------------------------- arrangement
def build():
    names = ("piano", "bass", "kit", "clave", "bell", "trumpet", "tenor", "horns", "rhodes", "pad") + (("mona",) if MONA else ()) + (("coro", "coro2") if SUNG else ())
    T = {n: [] for n in names}
    tempo = []
    beat0 = 0.0
    prng = random.Random(16)
    for si, (sec, meter, bpm, nb) in enumerate(FORM):
        beats = BEATS[meter]
        tempo.append({"at": f"{beat0:g}b", "bpm": bpm, "meter": meter})
        flip = si % 2  # the clave flips 3-2 / 2-3 at every section seam
        for b in range(nb):
            c = harm(sec, b)
            nxt = harm(sec, b + 1) if b + 1 < nb else c
            bar = {n: R(beats) for n in names}
            if sec == "bembe":
                bar["bell"] = bell(beats, b, hemiola=(b % 4 == 3))
                bar["kit"] = drums(sec, b, beats)
                if b >= 4:
                    bar["piano"] = comp(c, b, beats, vel=62 + b, style="stab")
                if b >= 8:
                    bar["bass"] = tumbao(c, nxt, b, beats)
                bar["pad"] = comp(c, b, beats, vel=50)
            elif sec in ("son", "mambo", "cierre"):
                side = 3 if (b + flip) % 2 == 0 else 2
                bar["clave"] = clave(beats, side)
                dens = 2 if sec != "son" else 1
                bar["kit"] = drums(sec, b, beats, dens)
                bar["bass"] = tumbao(c, nxt, b, beats)
                disp = (b // 4) % 2
                if sec == "psolo":  # the piano's turn: octave lines over clave, congas and tumbao; the horns lay out
                    bar["piano"] = piano_solo(c, b, prng)
                    bar["pad"] = comp(c, b, beats, vel=40)
                elif sec == "son":
                    bar["piano"] = montuno(c, b, disp, vel=82 + (b // 8) * 2)
                    if b >= 16:
                        bar["trumpet"] = line(THEME[b % 4], vel=94, shift=(12 if b >= 32 else 0) if b % 8 < 4 else 0)
                    if b >= 24 and b % 4 in (2, 3):
                        bar["horns"] = line(MAMBO[b % 2], vel=96)
                elif sec == "mambo":
                    bar["horns"] = line(MAMBO[b % 2], vel=100, shift=(0 if b < 12 else 2))
                    if MONA and MONA_WHERE == "1" and b >= 12:
                        bar["mona"] = line(MONA_RIFF[b % 2], vel=92, shift=2)
                    bar["piano"] = montuno(c, b, disp, vel=78)
                    # trading fours: trumpet then tenor, a composed solo line each
                    if (b // 4) % 2 == 0:
                        bar["trumpet"] = solo_bar(b, beats, 62, seed=1, vel=92)
                    else:
                        bar["tenor"] = solo_bar(b, beats, 50, seed=3, vel=90)
                else:  # cierre: the shout, then the break on the clave's rhythm and the last chord
                    if b < 6:
                        bar["horns"] = line(MAMBO[b % 2], vel=108, shift=2)
                        if MONA:
                            bar["mona"] = line(MONA_RIFF[b % 2], vel=100, shift=2)
                        bar["trumpet"] = line(THEME[b % 4], vel=100, shift=12)
                        bar["piano"] = montuno(c, b, 0, vel=90)
                    elif b < 8:  # the cierre: everyone on the clave's 3-side hits
                        hit = chord([nm(n) for n in CH["A7b13"][1]])
                        hits = J(tok(hit, 1.5, 116), tok(hit, 1.5, 112), tok(hit, 1, 118))
                        for k in ("piano", "horns"):
                            bar[k] = hits
                        bar["bass"] = J(tok("A1", 1.5, 116), tok("A1", 1.5, 112), tok("A1", 1, 118))
                        bar["kit"] = J(tok("c,k", 1.5, 120), tok("s,k", 1.5, 116), tok("c,k", 1, 124))
                        bar["clave"] = clave(beats, 3)
                    else:  # the last chord, held two bars: Dmaj9#11 (the album ends in the light)
                        last = chord([nm(n) for n in CH["Dmaj9#11"][1]])
                        if b == 8:
                            for k in ("piano", "horns", "pad"):
                                bar[k] = tok(last, beats * 2, 104)
                            bar["bass"] = tok("D2", beats * 2, 104)
                            bar["kit"] = J(tok("c,k", 1, 118), R(beats * 2 - 1))
                            bar["trumpet"] = tok("F#5", beats * 2, 96)
                            bar["rhodes"] = tok(last, beats * 2, 80)
                        else:
                            for k in names:
                                bar[k] = ""  # covered by the held notes of bar 8
            elif sec == "siete":
                bar["clave"] = clave(beats, 3)
                bar["kit"] = drums(sec, b, beats)
                bar["bass"] = tumbao(c, nxt, b, beats)
                bar["rhodes"] = line(SIETE[b % 2], vel=82, shift=(0 if b < 8 else 12))
                if QUOTE and b < 8:
                    bar["rhodes"] = line(SEVEN_DOORS[b], vel=84, shift=2)
                bar["pad"] = comp(c, b, beats, vel=56)
            elif sec == "descarga":
                bar["bell"] = bell(beats, b, hemiola=(b % 8 == 7))
                bar["kit"] = drums(sec, b, beats, dens=(2 if b >= 12 else 1))
                bar["bass"] = tumbao(c, nxt, b, beats)
                bar["piano"] = comp(c, b, beats, vel=78, style="stab")
                up = 2 if b >= 16 else 0
                if b % 4 in (0, 1):
                    bar["horns"] = line(CORO[b % 2], vel=102, shift=up + (b // 8) * 0)
                    if SUNG:  # the coro: vowels a / e / o by note, the baritone an octave under the horns
                        vows = [0.5, 0.75, 0.25]
                        bar["coro"] = J(*[R(d) if n == "R" else f"{nm(mi(n) + up - 12)}/{d:g}b@{92}^vow={vows[k % 3]}"
                                          for k, (n, d) in enumerate(CORO[b % 2])])
                        bar["coro2"] = line(CORO[b % 2], vel=80, shift=up)
                else:
                    who = "trumpet" if (b // 4) % 2 == 0 else "tenor"
                    bar[who] = solo_bar(b, beats, 62 + up if who == "trumpet" else 50 + up, seed=b, vel=94)
            if MAMBO_KEY and sec == "mambo":
                for n in names:
                    if n not in ("kit", "clave", "bell"):
                        bar[n] = transpose(bar[n], MAMBO_KEY)
            if SEAM and b == nb - 1 and sec != "cierre":  # the break: the band stops at the bar's middle; timbales fill
                half = beats / 2
                for n in names:
                    if n in ("kit", "clave", "bell"):
                        continue
                    bar[n] = J(cut(bar[n], half), R(beats - half))
                n16 = int((beats - half) * 4)
                fill = [("t1" if i % 4 < 2 else "t2") + f"/0.25b@{80 + 3 * i}" for i in range(n16 - 2)]
                fill += [tok("c,k", 0.5, 118)]
                bar["kit"] = J(cut(bar["kit"], half), *fill)
                bar["clave"] = J(cut(bar["clave"], half), R(beats - half))
                bar["bell"] = J(cut(bar["bell"], half), R(beats - half))
            for n in names:
                T[n].append((bar[n], beats))
            beat0 += beats
    return T, tempo, beat0


def num(name, default):
    v = float(os.environ.get(name, default))
    return int(v) if v == int(v) else v


def section_times():
    t, out = 0.0, {}
    for sec, meter, bpm, nb in FORM:
        d = BEATS[meter] * nb * 60 / bpm
        out[sec] = (t, t + d)
        t += d
    return out


def master():
    bands = (["lowshelf cutoff=100 gain=3dB", "peak cutoff=800 q=0.8 gain=-2dB"] if EQ == "1" else
             [f"lowshelf cutoff=120 gain={os.environ.get('T10_LS', '12')}dB", "peak cutoff=700 q=0.6 gain=-3dB"])
    fx = [{"type": "eq", "bands": bands},
          {"type": "compressor", "threshold": "-22dB", "ratio": 2, "attack": "15ms", "release": "200ms", "makeup": "0dB"},
          {"type": "gain", "gain": f"+{MG:g}dB"}]
    m = {"fx": fx}
    if DYN:  # the suite's arc: an intimate bembe, the son and mambo up, the 7/4 interlude down, the descarga building, the cierre on top
        st = section_times()
        lv = {"bembe": -6, "son": -2, "psolo": -3, "mambo": 0, "siete": -6, "descarga": -3, "cierre": num("T10_CIERRE", "5")}
        pts = [["0s", lv["bembe"]]]
        for sec in [n for n, *_ in FORM][1:]:
            a = st[sec][0]
            prev = pts[-1][1]
            pts += [[f"{a - 0.6:.2f}s", prev], [f"{a:.2f}s", lv[sec]]]
            if sec == "descarga":  # the descarga builds -3 -> +1 over its length
                pts += [[f"{st[sec][1] - 0.8:.2f}s", num("T10_DESEND", "1")]]
        pts += [[f"{st['cierre'][1] + 10:.2f}s", lv["cierre"]]]
        fx.append({"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}})
        m["auto"] = {"dyn": {"points": pts}}
    return m


def conga_kit():
    """Cierre's congas (chirper-zero) on chirper-two's physical drum layer (bd-7d117e): open-bottomed hand drums, so no
    resonant head and little air; a short felt contact for the open tones (the palm-and-fingers stroke), a hard plastic
    contact with full slap for the slap; tuned and sounding at pitch."""
    def conga(pitch, slap=False, gain="0dB"):
        layer = {"type": "drum", "beater": "plastic" if slap else "felt", "contact": 0.5 if slap else 0.8,
                 "decay": "0.18s" if slap else "0.55s", "sharp": 60 if slap else 30, "reso": 1.0, "cavity": 0.15,
                 "reso_level": 0.0, "air": 0.15, "strike": 0.35 if slap else 0.25, "shell": 0.35, "slap": 1.0 if slap else 0.3,
                 "tune_sounding": True, "stereo": 0.3}
        amp = {"a": "0.3ms", "d": "250ms" if slap else "700ms", "s": 0, "r": "60ms", "curve": 3}
        g = float(gain.replace("dB", "")) + CONGA_DB
        filt = ["hp cutoff=120"] + (["peak cutoff=250 q=1 gain=-3dB"] if CONGA_EQ else [])
        return {"pitch": pitch, "gain": f"{g:g}dB", "patch": {"synth": {"layers": [layer], "filters": filt, "amp": amp},
                                                         "play": {"vel_sens": 0.6}}}
    return {"cierre-kit": {"about": "Cierre's kit: room-kit plus congas on the physical drum layer (qo quinto E4, co conga B3, "
                                    "to tumba G3, cs slap).", "extends": "room-kit",
                           "kit": {"qo": conga("E4"), "co": conga("B3"), "to": conga("G3", gain="2dB"), "cs": conga("B3", slap=True, gain="-2dB")}}}


def song():
    T, tempo, total = build()

    def sc(name):
        bars = []
        skip_hold = 0.0
        for s, b in T[name]:
            if s == "":
                continue
            bars.append(s)
        return " | ".join(bars)

    tracks = [
        {"name": "piano", "patch": "piano", "gain": "-6dB", "pan": -0.25, "sends": {"room": "-12dB"}, "score": sc("piano")},
        {"name": "bass", "patch": "fretless", "gain": "-1dB", "score": sc("bass")},
        {"name": "kit", "patch": "cierre-kit" if CONGAS else "room-kit", "gain": "-6dB", "score": sc("kit")},
        {"name": "clave", "patch": "room-kit", "gain": "-8dB", "pan": 0.3, "score": sc("clave")},
        {"name": "bell", "patch": "room-kit", "gain": "-9dB", "pan": -0.35, "score": sc("bell")},
        {"name": "trumpet", "patch": "trumpet-mute", "gain": "-6dB", "pan": 0.2, "sends": {"room": "-10dB"}, "score": sc("trumpet")},
        {"name": "tenor", "patch": "tenor-sax-synth", "gain": "-7dB", "pan": -0.2, "sends": {"room": "-10dB"}, "score": sc("tenor")},
        {"name": "horns", "patch": "horn-section", "gain": "-6dB", "pan": 0.1, "sends": {"room": "-9dB"}, "score": sc("horns")},
        {"name": "rhodes", "patch": "rhodes-rotary", "gain": "-7dB", "pan": 0.3, "sends": {"room": "-10dB"}, "score": sc("rhodes")},
        {"name": "pad", "patch": "juno-pad", "gain": "-18dB", "sends": {"room": "-8dB"}, "score": sc("pad")},
    ]
    if SUNG:
        tracks.append({"name": "coro", "patch": "maynard", "gain": "-4dB", "pan": -0.1, "sends": {"room": "-7dB"}, "score": sc("coro")})
        tracks.append({"name": "coro2", "patch": "dream-vox", "gain": "-10dB", "pan": 0.25, "sends": {"room": "-6dB"}, "score": sc("coro2")})
    if MONA:
        tracks.append({"name": "mona", "patch": "horn", "gain": "-7dB", "pan": -0.3, "sends": {"room": "-9dB"}, "score": sc("mona")})
    return {
        "about": ("Chirpers - Odd Hours, track 10 (the closer; original composition, chirper-zero; generator "
                  "compose/chirpers2/src/chirpers2-t10.py). An Afro-Cuban / Latin-jazz suite in clave, D minor: 12/8 "
                  "bembe -> 4/4 son montuno (3-2) -> horn mambo with trumpet and tenor trading fours (clave flipped) -> a "
                  "7/4 interlude on a stretched 3+2+2 clave (rhodes) -> an afro 12/8 descarga with a coro, rising D to E "
                  "-> cierre and a last Dmaj9#11. One pulse throughout by metric modulation (dotted quarter 104 = half note 104)."),
        "tempo": tempo, "ceiling": "-0.1dB", "tail": "3s",
        **({"patches": conga_kit()} if CONGAS else {}),
        "buses": {"room": {"fx": ["reverb kind=room decay=1.4s size=0.7 mix=1 predelay=14ms"]}},
        "master": master(),
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
    text = dump(song())
    open(OUT, "w").write(text)
    print("wrote", OUT)
