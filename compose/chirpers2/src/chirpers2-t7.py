#!/usr/bin/env python3
"""chirpers2-t7 (Odd Hours, track 7): "Cross Purposes". Composed by chirper-three.

GENTLE GIANT / ZAPPA COUNTERPOINT: a through-composed chamber-prog piece where the lines argue.

- THE SUBJECT: nine notes over a 7/8 + 5/8 pair, D F A G# E | G Eb F# D (semitones 0 3 7 6 2 | 5 1 4 0), angular
  and chromatic; its INVERSION is the countersubject.
- FORM (every bar changes something; the meters say how long each bar is, in eighths):
    1 STATEMENT  the subject HOCKETED note by note across marimba / flute / muted trumpet / guitar (the rotation turns
                 one place each time), then in unison, then inverted low under hocketed fragments;
    2 FUGUE      four entries (sax at D, trumpet at A, guitar inverted, bass), each continuing with the countersubject,
                 so each bar's texture differs; wurli stabs a new chord every bar;
    3 BLACK PAGE a rhythmic unison for the whole band in sixteenth meters (11 13 9 15 11 13 7 17 sixteenths), the
                 subject's pitches in diminution, toms on every hit;
    4 CROSS      CROSS PURPOSES: horns + wurli in 7/8 cycles against flute + marimba + guitar in 4/4, the subject
                 augmented in the bass, a ride bell on the 7 (12 bars of 4/4);
    5 TRADES     sax and trumpet trade single bars, then pairs, over a meter wheel 7 5 6 9 (24 bars), walking bass;
    6 STRETTO    subject entries every two eighths in every voice, the climax;
    7 CODA       the subject in augmentation (bass + flute), then the final chord built one hocketed note at a time.
- KIT: prog-kit, groupings follow each meter (7 = 2+2+3 or 3+2+2 alternating bar by bar, 5 = 3+2 / 2+3, 9 = 2+2+2+3,
  6 = 3+3, 8 = 3+3+2): kick on group starts, snare on the last group, hats on the eighths.

Emits songs/chirpers2-t7.yaml. Edit the music here.
"""
import json
import os
import random

OUT = os.environ.get("T7_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers2-t7.yaml")
BPM = 100
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
D4 = 62

SUBJ = [(0, 1), (3, 1), (7, 1), (6, 2), (2, 2), (5, 1), (1, 1), (4, 1), (0, 2)]   # (semitones from tonic, eighths)
INV = [(-p, d) for p, d in SUBJ]
SUBJ_LEN = 12                                                                         # 7 + 5 eighths

# One chord per bar, cycling: (root pitch class, intervals). Modal / quartal / altered.
PROG = [(2, [0, 3, 7, 10, 14]), (10, [0, 4, 7, 11, 18]), (4, [0, 3, 6, 10]), (9, [0, 4, 10, 13, 15]),
        (5, [0, 4, 7, 11, 18]), (7, [0, 4, 10, 14, 21]), (1, [0, 3, 6, 9]), (2, [0, 5, 10, 15])]

GROUPS = {5: [[3, 2], [2, 3]], 6: [[3, 3], [2, 2, 2]], 7: [[2, 2, 3], [3, 2, 2]], 8: [[3, 3, 2], [2, 3, 3]],
          9: [[2, 2, 2, 3], [3, 3, 3]], 12: [[3, 3, 3, 3], [2, 2, 2, 3, 3]]}


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Part:
    def __init__(self):
        self.ev = []                         # (start eighths, length eighths, head, vel)

    def add(self, st, ln, head, vel):
        self.ev.append((st, ln, head, int(max(1, min(127, vel)))))

    def score(self, total):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        merged = []
        for e in ev:
            if merged and abs(merged[-1][0] - e[0]) < 1e-6:
                continue
            merged.append(e)
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(merged):
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-4:
                toks.append(f"R/{(s - pos) / 2:.4g}b")
            toks.append(f"{head}/{ln / 2:.4g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-4:
            toks.append(f"R/{(total - pos) / 2:.4g}b")
        return " ".join(toks)


P = {k: Part() for k in ("mar", "flute", "tpt", "sax", "gtr", "keys", "bass", "kick", "snare", "hat", "toms", "ride")}
BARS = []          # (start eighths, length eighths, section, index in section)
rng = random.Random(7)


def line(part, st, notes, base, vel, scale=1.0, art=1.0):
    """Place a (semitone, eighths) line from st; returns the end time."""
    t = st
    for p, d in notes:
        part.add(t, d * scale * art, nm(base + p), vel)
        t += d * scale
    return t


def chord_at(i):
    return PROG[i % len(PROG)]


def kit_bar(st, ln, k, vel=96, fill=False):
    """Kick on group starts, snare on the last group, hats on the eighths; the grouping alternates bar by bar."""
    opts = GROUPS.get(ln) or [[2] * (ln // 2) + ([ln % 2] if ln % 2 else [])]
    grp = opts[k % len(opts)]
    t = st
    for gi, g in enumerate(grp):
        if gi == len(grp) - 1 and len(grp) > 1:
            P["snare"].add(t, 1, "s", vel + 4)
        else:
            P["kick"].add(t, 1, "k", vel + (8 if gi == 0 else 0))
        t += g
    for e in range(int(ln)):
        accent = e == 0 or e in [sum(grp[:j]) for j in range(len(grp))]
        P["hat"].add(st + e, 1, "h", (vel - 14) if accent else (vel - 30))
    if rng.random() < 0.5 and ln >= 6:                                        # a ghost before the snare
        P["snare"].add(st + ln - grp[-1] - 0.5, 0.5, "g", vel - 40)
    if fill:
        for j, tom in enumerate(("t1", "t2", "t3", "ft")):
            P["toms"].add(st + ln - 2 + j * 0.5, 0.5, tom, vel + 2)


def bar(st, ln, sec, i):
    BARS.append((st, ln, sec, i))


def harmony_bar(st, ln, ci, vel=80, bass=True, stabs=True, walk=False):
    root, iv = chord_at(ci)
    if stabs:
        voic = [60 + ((root + x) % 12) for x in iv[1:]]
        head = ",".join(nm(m) for m in sorted(set(voic)))
        P["keys"].add(st, 0.8, head, vel)
        P["keys"].add(st + ln - 2, 0.8, head, vel - 12)
    if bass:
        b = 38 + ((root - 2) % 12)                                            # around D2
        if walk:
            nxt_root = chord_at(ci + 1)[0]
            tones = [b, b + iv[1], b + iv[2], b + 12 - 2]
            for e in range(int(ln)):
                if e == ln - 1:
                    tgt = 38 + ((nxt_root - 2) % 12)
                    P["bass"].add(st + e, 1, nm(tgt + (1 if rng.random() < 0.5 else -1)), vel + 4)
                else:
                    P["bass"].add(st + e, 1, nm(tones[e % len(tones)] + (12 if e % 4 == 3 else 0)), vel + (8 if e == 0 else 0))
        else:
            P["bass"].add(st, ln - 1, nm(b), vel + 10)
            P["bass"].add(st + ln - 1, 1, nm(b + 7), vel)


# ---------- 1 STATEMENT ----------
def statement(t):
    rot = ["mar", "flute", "tpt", "gtr"]
    for rep in range(2):                                       # the subject hocketed, rotation turning
        x = t
        for j, (p, d) in enumerate(SUBJ):
            who = rot[(j + rep) % 4]
            base = D4 - 12 if who == "gtr" else D4
            P[who].add(x, d * 0.9, nm(base + p), 78 + 6 * rep)
            x += d
        bar(t, 7, "statement", 2 * rep); bar(t + 7, 5, "statement", 2 * rep + 1)
        for k in range(2):
            P["hat"].add(t + 7 * k, 1, "h", 50)
        if rep == 1:
            harmony_bar(t, 7, 0, 70, stabs=False); harmony_bar(t + 7, 5, 1, 70, stabs=False)
        t += SUBJ_LEN
    for who, base, v in (("mar", D4, 96), ("flute", D4 + 12, 88), ("tpt", D4, 92), ("sax", D4 - 12, 90),
                         ("gtr", D4 - 12, 86)):                  # in unison, the band arrives
        line(P[who], t, SUBJ, base, v, art=0.9)
    bar(t, 7, "statement", 4); bar(t + 7, 5, "statement", 5)
    kit_bar(t, 7, 0, 92); kit_bar(t + 7, 5, 1, 92)
    harmony_bar(t, 7, 2, 84); harmony_bar(t + 7, 5, 3, 84)
    t += SUBJ_LEN
    line(P["sax"], t, INV, D4 - 12, 92); line(P["bass"], t, INV, D4 - 24, 96)          # inverted, low
    frag = [(0, "mar", 3), (3, "flute", 7), (6, "mar", 6), (8, "tpt", 2), (10, "flute", 5)]
    for o, who, p in frag:                                       # hocketed fragments answer above
        P[who].add(t + o, 1, nm(D4 + 12 + p), 80)
    bar(t, 7, "statement", 6); bar(t + 7, 5, "statement", 7)
    kit_bar(t, 7, 1, 94); kit_bar(t + 7, 5, 0, 94, fill=True)
    P["keys"].add(t, 0.8, "D4,F4,A4,C5,E5", 86)
    return t + SUBJ_LEN


# ---------- 2 FUGUE ----------
def fugue(t):
    a = t
    voices = [("sax", D4 - 12, SUBJ, 0), ("tpt", D4 + 7, SUBJ, 1), ("gtr", D4 - 12, INV, 2), ("bass", D4 - 24, SUBJ, 3)]
    for who, base, subj, k in voices:
        st = a + k * SUBJ_LEN
        e = line(P[who], st, subj, base, 92)
        cs = INV if subj is SUBJ else SUBJ
        e = line(P[who], e, cs, base + (5 if k % 2 else -2), 86)          # the countersubject, displaced
        if k < 2:
            line(P[who], e, SUBJ[:5], base + 3, 84)                       # a free tail on the subject's head
    for i in range(16):                                         # 8 subject units of 7 + 5
        ln = 7 if i % 2 == 0 else 5
        bar(t, ln, "fugue", i)
        harmony_bar(t, ln, i, 76 + 2 * (i // 4), bass=(i < 6))
        kit_bar(t, ln, i // 2, 88 + i, fill=(i % 4 == 3))
        if i >= 8 and i % 2 == 0:                                 # the marimba doubles the inner voice's head
            line(P["mar"], t, SUBJ[:3], D4 + 12 + (i % 5), 74)
        t += ln
    return t


# ---------- 3 BLACK PAGE ----------
def black_page(t):
    meters16 = [11, 13, 9, 15, 11, 13, 7, 17]
    tom_of = {0: "ft", 1: "t3", 2: "t2", 3: "t1"}
    k = 0
    for i, m in enumerate(meters16):
        ln = m / 2                                               # eighths
        bar(t, ln, "black", i)
        x, j = 0.0, 0
        groups = []
        rest = m
        while rest > 0:                                          # 2s and 3s, alternating starts bar by bar
            g = 3 if ((j + i) % 2 == 0 and rest != 4) or rest == 3 else 2
            g = min(g, rest)
            groups.append(g)
            rest -= g
            j += 1
        for g in groups:
            p, _ = SUBJ[k % len(SUBJ)]
            st = t + x / 2
            v = 104 if x == 0 else 92
            for who, base in (("mar", D4), ("flute", D4 + 12), ("tpt", D4), ("sax", D4 - 12), ("gtr", D4 - 12),
                              ("bass", D4 - 24)):
                P[who].add(st, g / 2 * 0.7, nm(base + p), v)
            P["toms"].add(st, 0.5, tom_of[(p // 2) % 4], v)
            P["kick" if g == 3 else "snare"].add(st, 0.5, "k" if g == 3 else "s", v - 6)
            x += g
            k += 1
        P["keys"].add(t, 0.5, "D4,Ab4,Db5,G5", 90)
        t += ln
    return t


# ---------- 4 CROSS PURPOSES ----------
def cross(t):
    a, z = t, t + 12 * 8
    x = a                                                         # horns + wurli: the subject's 7/8 bar, cycling
    n = 0
    while x < z:
        for p, d in SUBJ[:5]:
            if x < z:
                P["tpt" if n % 2 == 0 else "sax"].add(x, d * 0.85, nm(D4 + p + (12 if n % 2 == 0 else 0)), 88)
            x += d
        P["keys"].add(x - 7, 0.6, "D4,G4,C5" if n % 2 else "E4,A4,D5", 74)
        P["ride"].add(x - 7, 1, "D5", 100)                         # the ride bell marks the 7
        n += 1
    x, n = a, 0                                                   # flute + marimba + guitar: 4/4, the inversion's tail
    fig = [(0, 1.5), (-5, 0.5), (-1, 1), (-4, 1), (0, 2), (2, 2)]
    while x < z:
        for p, d in fig:
            who = ("flute", "mar", "gtr")[n % 3]
            base = D4 + 12 if who != "gtr" else D4
            P[who].add(x, d * 0.9, nm(base + p + (3 if n % 4 == 3 else 0)), 82)
            x += d
        n += 1
    line(P["bass"], a, SUBJ * 4, D4 - 24, 100, scale=2.0)          # the subject augmented, four times
    for i in range(12):
        bar(t, 8, "cross", i)
        kit_bar(t, 8, i, 94 + (i // 3) * 2, fill=(i == 11))
        t += 8
    return t


# ---------- 5 TRADES ----------
def improv_bar(who, st, ln, ci, prev, vel):
    root, iv = chord_at(ci)
    pool = sorted({(root + x) % 12 for x in iv} | {(root + 2) % 12, (root + 5) % 12})
    lo, hi = (55, 79) if who == "tpt" else (46, 70)
    p = prev
    x = 0.0
    while x < ln - 1:
        d = rng.choice([0.5, 0.5, 1, 1, 1, 1.5, 2]) if x < ln - 2 else 1
        step = rng.choice([-2, -1, 1, 2, 3, -3, 5, -4])
        p = max(lo, min(hi, p + step))
        while p % 12 not in pool and rng.random() < 0.75:
            p += 1 if step > 0 else -1
        P[who].add(st + x, d * 0.92, nm(p), vel + int(8 * rng.random()) + (6 if x == 0 else 0))
        x += d
    return p


def trades(t):
    wheel = [7, 5, 6, 9]
    pt, ps = 69, 58
    for i in range(24):
        ln = wheel[i % 4]
        who = ("tpt", "sax")[(i if i < 16 else i // 2) % 2]       # single bars, then pairs
        if who == "tpt":
            pt = improv_bar("tpt", t, ln, i, pt, 84 + i // 3)
        else:
            ps = improv_bar("sax", t, ln, i, ps, 84 + i // 3)
        bar(t, ln, "trades", i)
        harmony_bar(t, ln, i, 70 + i // 2, walk=True)
        kit_bar(t, ln, i, 84 + i // 2, fill=(i % 8 == 7))
        if i % 4 == 3:                                            # the marimba answers each wheel turn
            line(P["mar"], t + ln - 3, [(7, 1), (6, 1), (2, 1)], D4 + 12, 76)
        t += ln
    return t


# ---------- 6 STRETTO ----------
def stretto(t):
    a = t
    entries = [("bass", D4 - 24), ("gtr", D4 - 12), ("sax", D4 - 12), ("keys", D4), ("tpt", D4 + 7), ("mar", D4 + 12),
               ("flute", D4 + 12)]
    for j, (who, base) in enumerate(entries):
        e = line(P[who], a + 2 * j, SUBJ, base, 96 + j)
        line(P[who], e, INV, base, 92 + j)
    for i in range(8):
        ln = 7 if i % 2 == 0 else 5
        bar(t, ln, "stretto", i)
        kit_bar(t, ln, i, 104 + i, fill=(i == 7))
        t += ln
    return t


# ---------- 7 CODA ----------
def coda(t):
    line(P["bass"], t, SUBJ, D4 - 24, 92, scale=2.0)
    line(P["flute"], t, SUBJ, D4 + 12, 80, scale=2.0)
    for i in range(2):
        bar(t + 12 * i, 12, "coda", i)
        kit_bar(t + 12 * i, 12, i, 80)
        harmony_bar(t + 12 * i, 12, 7 * i, 70, bass=False)
    t += 24
    stack = [("bass", D4 - 24), ("gtr", D4 - 12 + 3), ("sax", D4 - 12 + 7), ("keys", D4 + 6), ("tpt", D4 + 2),
             ("mar", D4 + 12 + 5), ("flute", D4 + 12 + 1)]               # the subject's pitch set, one note an eighth
    for j, (who, m) in enumerate(stack):
        P[who].add(t + j, 14 - j, nm(m), 84 + 3 * j)
    bar(t, 8, "coda", 2); bar(t + 8, 8, "coda", 3)
    P["kick"].add(t + 14, 1, "k", 118); P["snare"].add(t + 14, 1, "s", 116)
    P["toms"].add(t + 14, 1, "ft", 112)
    return t + 16


def main():
    t = 0.0
    for sec in (statement, fugue, black_page, cross, trades, stretto, coda):
        t = sec(t)
    total = t
    MAR = {"about": "Cross Purposes' marimba (chirper-three): additive wooden-bar partials 1 / 3.93 / 9.2 with a mallet click.",
           "synth": {"layers": [{"name": "bar", "type": "additive", "partials": [[1, 1], [3.93, 0.32], [9.2, 0.07]]},
                                {"name": "click", "type": "noise", "level": {"value": "-70dB", "mod": [{"src": "env.ck", "amount": 40}]}}],
                     "env": {"ck": {"a": "0.2ms", "d": "5ms", "s": 0}},
                     "filters": ["hp cutoff=120"],
                     "amp": {"a": "1ms", "d": "650ms", "s": 0, "r": "80ms", "curve": 3}},
           "play": {"vel_sens": 0.6}}
    tr = lambda name, patch, **kw: dict({"name": name, "patch": patch, "score": P[name].score(total)}, **kw)
    tracks = [
        tr("mar", "c3-marimba", pan="L40", gain="-4dB", sends={"room": "-10dB"}),
        tr("flute", "mellotron-flute", pan="R40", gain="-6dB", sends={"room": "-10dB"}),
        tr("tpt", "trumpet-mute", pan="L20", gain="-5dB", sends={"room": "-12dB"}),
        tr("sax", "tenor-sax-synth", pan="R20", gain="-5dB", sends={"room": "-12dB"}),
        tr("gtr", "starcaster-clean", pan="L60", gain="-6dB", sends={"room": "-12dB"}),
        tr("keys", "wurli", pan="R60", gain="-7dB", sends={"room": "-12dB"}),
        tr("bass", "bass-di", gain="-3dB"),
        tr("kick", "prog-kit", out="drums"),
        tr("snare", "prog-kit", out="drums"),
        tr("hat", "prog-kit", out="drums", gain="-4dB"),
        tr("toms", "prog-kit", out="drums"),
        tr("ride", "modal-ride", out="drums", gain="-8dB"),
    ]
    head = [
        'about: "Chirpers - Odd Hours, track 7: Cross Purposes (chirper-three). Gentle Giant / Zappa counterpoint: a nine-note subject over 7/8 + 5/8, hocketed, fugued, black-paged, set at cross purposes (7 against 4), traded and stretto\'d. Generated by compose/chirpers2/src/chirpers2-t7.py."',
        f"tempo: {BPM}",
        'tail: "2s"',
        'ceiling: "-0.3dB"',
        "patches: " + json.dumps({"c3-marimba": MAR}),
        "buses:",
        '  room: {fx: ["reverb kind=room decay=1.1s mix=1 predelay=12ms mono_below=150hz"]}',
        '  drums: {fx: [{"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "12ms", "release": "100ms", "makeup": "2dB"}, "reverb kind=room decay=0.8s mix=0.12 predelay=8ms mono_below=200hz"]}',
        'master: ' + json.dumps({"fx": ["glue threshold=-20dB ratio=2 attack=15ms release=200ms makeup=2dB", {"type": "gain", "gain": "6dB"}]}),
        "tracks:",
    ]
    with open(OUT, "w") as f:
        f.write("\n".join(head) + "\n")
        for d in tracks:
            f.write("  - " + json.dumps(d) + "\n")
    secs = total / 2 * 60 / BPM
    print(f"wrote {OUT}: {len(BARS)} bars, {total:.1f} eighths, {secs:.0f} s")


if __name__ == "__main__":
    main()
