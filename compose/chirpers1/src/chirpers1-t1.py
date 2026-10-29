#!/usr/bin/env python3
"""chirpers1-t1 "Seed Crystal" (chirper-three): the album's opening.

Identity: 80 BPM, 4/4 pulse; the album's core motif LATTICE = a 7-sixteenth cell (3+2+2) carrying the colour
F-Gb-B-E (root, minor 2nd, tritone, major 7th). The cell cycles over the 16-sixteenth bar and realigns with the
downbeat every 7 bars (bars 1, 8, 15, 22, 29): each realignment opens a section; the build (Threshold) runs one full
cycle of the 5-cell (5 bars), then the Breach: a stop, the seed's return, unison hits and the held cluster. Quiet and clean, it grows into
the full rig and ends on a sustained F-B-E cluster that rings straight into track 2.

Emits songs/chirpers1-t1.yaml. Edit the music here, not the YAML.
"""
import json, os

ROOT = "/home/harry/.config/chirp"
OUT = os.path.join(ROOT, "songs", "chirpers1-t1.yaml")
TEMPO = 80
BARS = 42
STOP, SEED, HITS, HOLD = 34, (35, 36, 37, 38, 39), (40, 41), 42   # the Breach: stop, the seed returns, unison hits, held cluster
S = 16                      # sixteenths per bar
TOTAL = BARS * S

NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
def nm(m):                  # MIDI -> name ("F1" = 29)
    return f"{NAMES[m % 12]}{m // 12 - 1}"
F1 = 29
LATTICE = [0, 1, 6, 11]     # F, Gb, B, E above F
CELL7 = [0, 3, 5]           # 3+2+2 sixteenths: the album's rhythmic cell
CELL5 = [0, 3]              # its diminution (3+2), used in the build

def bar0(b):                # first sixteenth of 1-based bar b
    return (b - 1) * S

SECTIONS = {"A": (1, 7), "B": (8, 14), "C": (15, 21), "D": (22, 28), "E": (29, 33), "F": (34, 42)}
def span(sec):
    a, z = SECTIONS[sec]
    return bar0(a), bar0(z + 1)

def cell_onsets(start, end, cell=CELL7, length=7, phase=0):
    """Onsets of a repeating cell from START (sixteenths), (onset, index in cell, cell number)."""
    out, n, t = [], 0, start - phase
    while t < end:
        for i, o in enumerate(cell):
            if start <= t + o < end:
                out.append((t + o, i, n))
        t += length
        n += 1
    return out

# ---------- serialisation ----------
DUR = {1: "/16", 2: "/8", 3: "/8.", 4: "/4", 6: "/4.", 8: "/2", 12: "/2.", 16: "/1"}
def dur(n):
    if n in DUR:
        return DUR[n]
    parts, rest = [], n
    for k in (16, 8, 4, 2, 1):
        while rest >= k:
            parts.append(k); rest -= k
    return "/" + "+".join(DUR[p][1:] for p in parts)

def score(events, total=TOTAL):
    """events: (start, length, token, vel, prefix). Monophonic: later events cut earlier ones."""
    ev = sorted(events, key=lambda e: e[0])
    out, t = [], 0
    for i, (st, ln, tok, vel, pre) in enumerate(ev):
        if st < t:
            continue
        if st > t:
            out.append("R" + dur(st - t))
        nxt = ev[i + 1][0] if i + 1 < len(ev) else total
        ln = max(1, min(ln, nxt - st, total - st))
        out.append((pre + " " if pre else "") + f"{tok}{dur(ln)}@{int(vel)}")
        t = st + ln
    if t < total:
        out.append("R" + dur(total - t))
    return " ".join(out)

def ramp(t, a, z, v0, v1):  # velocity ramp across [a, z)
    return v0 + (v1 - v0) * max(0.0, min(1.0, (t - a) / max(1, z - a)))

# ---------- parts ----------
def pad():
    chords = {}
    for b in range(1, STOP):
        if b <= 7:   ch = [F1 + 12, F1 + 19]                         # F2 C3: bare fifth
        elif b <= 14: ch = [F1 + 12, F1 + 19, F1 + 23]               # + E3: the maj7 colour
        elif b <= 21: ch = [F1 + 13, F1 + 20, F1 + 24] if (b - 15) % 4 in (2, 3) else [F1 + 12, F1 + 19, F1 + 23]
        elif b <= 28: ch = [F1 + 12, F1 + 18, F1 + 23]               # F B E: the lattice colour
        elif b <= 35: ch = [F1 + 12, F1 + 18, F1 + 23, F1 + 25]      # + Gb3: full cluster, rising tension
        else:         ch = [F1 + 12, F1 + 18, F1 + 23, F1 + 25]
        chords[b] = ch
    ev, b = [], 1
    while b < STOP:
        e = b
        while e + 1 < STOP and chords[e + 1] == chords[b] and e + 1 not in (8, 15, 22, 29):
            e += 1
        v = 52 if b < 15 else 62 if b < 29 else 74
        ev.append((bar0(b), (e - b + 1) * S, ",".join(nm(m) for m in chords[b]), v, ""))
        b = e + 1
    # the Breach: silent for the stop; the opening's bare fifth returns under the seed; the cluster for the hold
    ev.append((bar0(SEED[0]), len(SEED) * S, ",".join(nm(m) for m in (F1 + 12, F1 + 19)), 56, ""))
    # the held cluster voiced from B2 up (F an octave higher, F3): the tail's 87 Hz F2 read +21 dB over Ingot's head,
    # and the sub swell carries the F root below
    ev.append((bar0(HOLD), S, ",".join(nm(m) for m in (F1 + 18, F1 + 23, F1 + 24, F1 + 25)), 76, ""))
    return score(ev)

def clean_a():               # the motif, stated: cell onsets walk through LATTICE (4 notes over 3 onsets)
    ev = []
    a, z = bar0(1), bar0(STOP)
    k = 0
    for t, i, n in cell_onsets(a, z):
        nxt = (CELL7 + [7])[i + 1] - CELL7[i]
        note = F1 + 24 + LATTICE[k % 4]                       # F3 Gb3 B3 E4
        bar = t // S + 1
        if 22 <= bar <= 28 and n % 2:                          # Pressure: thin to every other cell
            k += 1; continue
        v = ramp(t, 0, bar0(15), 54, 70) if bar < 22 else 60 if bar < 29 else ramp(t, bar0(29), bar0(STOP), 64, 84)
        ev.append((t, nxt, nm(note), v, ""))
        k += 1
    # the seed returns after the stop: the opening statement, alone, from the top of the line
    a, z = bar0(SEED[0]), bar0(SEED[-1] + 1)
    for k, (t, i, n) in enumerate(cell_onsets(a, z)):
        nxt = (CELL7 + [7])[i + 1] - CELL7[i]
        ev.append((t, nxt, nm(F1 + 24 + LATTICE[k % 4]), 60, ""))
    return score(ev)

def clean_b():               # the motif inverted (E5 B4 Gb4 F4) and augmented: one note per cell, a sixteenth late
    ev = []
    inv = [F1 + 47, F1 + 42, F1 + 37, F1 + 36]
    for sec, v in (("B", 58), ("C", 64)):
        a, z = span(sec)
        for t, i, n in cell_onsets(a, z):
            if i == 0:
                ev.append((t + 1, 6, nm(inv[n % 4]), v, ""))
    a, z = span("E")                                          # Threshold: returns in diminution on the 5-cell
    for t, i, n in cell_onsets(a, z, CELL5, 5):
        if i == 0:
            ev.append((t + 1, 3, nm(inv[n % 4] + 12 if n % 8 >= 4 else inv[n % 4]), ramp(t, a, z, 62, 86), ""))
    a, z = bar0(SEED[0]), bar0(SEED[-1] + 1)                  # and its inversion now sounds against the seed
    for t, i, n in cell_onsets(a, z):
        if i == 0:
            ev.append((t + 1, 6, nm(inv[n % 4]), 54, ""))
    return score(ev)

def lead():                  # the motif in long notes over the Lattice; tension held through the build
    ev = []
    for (b, nb, m) in ((15, 2, F1 + 36), (17, 2, F1 + 37), (19, 2, F1 + 42), (21, 1, F1 + 47)):
        ev.append((bar0(b), nb * S, nm(m), 66, ""))
    ev.append((bar0(29), 3 * S, nm(F1 + 47), 72, ""))          # E5 held
    ev.append((bar0(32), 2 * S, nm(F1 + 48), 80, ""))          # F5: the semitone pull upward
    ev.append((bar0(HOLD), S, nm(F1 + 49), 88, ""))            # Gb5 on the final cluster
    return score(ev)

def bass():
    ev = []
    a, z = span("B")
    for b in range(8, 15, 2):
        ev.append((bar0(b), 2 * S, nm(F1), 50, ""))           # sub swells under Growth
    a, z = span("C")
    for t, i, n in cell_onsets(a, z):
        if i == 0:
            ev.append((t, 3, nm(F1), 66, ""))
    a, z = span("D")
    for t, i, n in cell_onsets(a, z):
        ev.append((t, 2, nm(F1 + 6 if (i == 0 and n % 4 == 3) else F1), ramp(t, a, z, 74, 94), ""))
    a, z = span("E")
    for t, i, n in cell_onsets(a, z, CELL5, 5):
        ev.append((t, 2, nm(F1), ramp(t, a, z, 92, 112), ""))
    ev += breach_hits(lambda: nm(F1), 110)
    ev.append((bar0(HOLD), S, nm(F1), 112, ""))
    return score(ev)

def breach_hits(tok, v):
    """STOP: one hit then silence (the seed returns); HITS: the cell in unison, then denser; HOLD is the caller's."""
    ev = [(bar0(STOP), 4, tok(), v + 6, "")]
    for b in HITS:
        a, z = bar0(b), bar0(b + 1)
        cell, ln = (CELL7, 7) if b < HITS[-1] else (CELL5, 5)
        for t, i, n in cell_onsets(a, z, cell, ln):
            ev.append((t, 2, tok(), v if i == 0 else v - 14, ""))
    return ev

def guitar():
    ev = []
    pm, op = "expr.pm=1", "expr.pm=0"
    trit = ",".join(nm(m) for m in (F1, F1 + 6))               # F1 B1
    clus = ",".join(nm(m) for m in (F1, F1 + 6, F1 + 11))      # F1 B1 E2
    a, z = span("D")
    for t, i, n in cell_onsets(a, z):
        if i == 0 and n % 4 == 3:
            ev.append((t, 3, trit, ramp(t, a, z, 84, 100), op))
        else:
            ev.append((t, 2, nm(F1), ramp(t, a, z, 64, 92), pm))
    a, z = span("E")
    for t, i, n in cell_onsets(a, z, CELL5, 5):
        if i == 0 and n % 3 == 2:
            ev.append((t, 3, trit, ramp(t, a, z, 98, 118), op))
        else:
            ev.append((t, 2, nm(F1), ramp(t, a, z, 92, 114), pm))
    ev.append((bar0(STOP), 8, clus, 122, op))
    for st, ln, tok, v, pre in breach_hits(lambda: nm(F1), 112)[1:]:
        ev.append((st, ln, tok, v, pm))
    ev.append((bar0(HOLD), S, clus, 124, op))
    return score(ev)

def kick():
    ev = []
    a, z = span("C")
    for t, i, n in cell_onsets(a, z):
        if i == 0:
            ev.append((t, 1, "k", 62, ""))
    a, z = span("D")
    for t, i, n in cell_onsets(a, z):
        ev.append((t, 1, "k", ramp(t, a, z, 78, 100), ""))
    a, z = span("E")
    for t, i, n in cell_onsets(a, z, CELL5, 5):
        ev.append((t, 1, "k", ramp(t, a, z, 96, 118), ""))
    ev += [(st, 1, "k", v, "") for st, ln, tok, v, pre in breach_hits(lambda: "k", 112)]
    ev.append((bar0(HOLD), 1, "k", 124, ""))
    return score(ev)

def snare():
    ev = []
    for b in range(22, 29):
        ev.append((bar0(b) + 8, 1, "s", ramp(bar0(b), bar0(22), bar0(29), 66, 96), ""))   # half-time: beat 3
    for b in range(29, STOP):
        for q in (4, 12):
            ev.append((bar0(b) + q, 1, "s", 104 if b < STOP - 1 else 110, ""))
    a = bar0(STOP - 1) + 8                                      # roll into the stop
    for k in range(8):
        ev.append((a + k, 1, "s", 70 + 6 * k, ""))
    ev.append((bar0(HITS[0]) + 8, 1, "s", 112, ""))
    a = bar0(HITS[-1])
    for k in range(16):                                         # the last bar before the hold: a full roll
        ev.append((a + k, 1, "s", 72 + 3 * k, ""))
    ev.append((bar0(HOLD), 1, "s", 124, ""))
    return score(ev)

def cymbals():
    ev = []
    for b in range(8, 15):                                      # Growth: a quiet bell keeps the 4/4 pulse
        for q in range(4):
            ev.append((bar0(b) + 4 * q, 1, "rb", 44 + (6 if q == 0 else 0), ""))
    for b in range(15, 22):
        for q in range(4):
            ev.append((bar0(b) + 4 * q, 1, "rd", 52 + (8 if q == 0 else 0), ""))
    for b in range(22, 29):
        for e8 in range(8):
            ev.append((bar0(b) + 2 * e8, 1, "h", 58 + (10 if e8 % 2 == 0 else 0), ""))
    for b in range(29, STOP):
        for e8 in range(8):
            tok = "c" if (b in (29, 32) and e8 == 0) else "rd"
            ev.append((bar0(b) + 2 * e8, 1, tok, 112 if tok == "c" else 80 + (10 if e8 % 2 == 0 else 0), ""))
    ev.append((bar0(STOP), 1, "x", 120, ""))
    for b in SEED:                                              # the seed's quiet bell, as in Growth
        for q in range(4):
            ev.append((bar0(b) + 4 * q, 1, "rb", 42, ""))
    ev.append((bar0(HITS[0]), 1, "c", 112, ""))
    ev.append((bar0(HOLD), 1, "c", 124, ""))
    return score(ev)

def toms():                  # the distant percussion of the opening
    ev = []
    for sec, v in (("A", 0), ("B", 42), ("C", 50)):
        if not v:
            continue
        a, z = span(sec)
        for t, i, n in cell_onsets(a, z):
            if i == 0:
                ev.append((t, 1, "ft", v + (6 if n % 4 == 0 else 0), ""))
            elif sec == "C" and i == 2 and n % 2:
                ev.append((t, 1, "t3", v - 8, ""))
    a, z = bar0(SEED[0]), bar0(SEED[-1] + 1)                  # the distant floor tom returns with the seed
    for t, i, n in cell_onsets(a, z):
        if i == 0:
            ev.append((t, 1, "ft", 44, ""))
    return score(ev)

def ride():
    """The master's dynamics (dB before the glue): the intro starts quietly and grows; the seed's return drops back."""
    sec = 4 * 60 / TEMPO                                        # seconds per bar
    t = lambda b: f"{(b - 1) * sec:.2f}s"
    pts = [(1, -6.0), (8, -6.0), (15, -3.0), (22, -1.0), (22.05, 0.0), (STOP + 0.25, 0.0), (STOP + 0.9, -6.0),
           (SEED[-1] + 0.85, -6.0), (HITS[0], 0.0), (HOLD + 2, 0.0)]
    return [[t(b), v] for b, v in pts]

def felt_tom(decay_s, sharp):
    """A physical tom (chirper-two's drum layer, bd-7d117e) struck with a felt mallet: soft attack, open resonant head."""
    return {"synth": {"layers": [{"type": "drum", "beater": "felt", "decay": f"{decay_s}s", "sharp": sharp, "reso": 1.0,
                                  # full head/cavity coupling (richer partials); tune_sounding (pin 73554f44) keeps the tom
                                  # at its written pitch, where the coupled heads alone read 1.33x high
                                  "cavity": 0.4, "reso_level": 0.5, "tune_sounding": True, "air": 0.5, "strike": 0.3, "shell": 0.3, "damp": 0.2}],
                      "filters": ["hp cutoff=40", "peak cutoff=2k q=1 gain=1dB"],
                      "amp": {"a": "0.5ms", "d": f"{int(decay_s * 900)}ms", "s": 0, "r": "120ms", "curve": 3}, "drive": 0.05},
            "play": {"vel_sens": 0.55}}

# The distant toms speak LATTICE's poles: the floor tom is F, the high tom B (the tritone).
SEED_TOMS = {"about": "Seed Crystal's toms: physical felt-mallet drums tuned to LATTICE's F and B (chirper-three).",
             "extends": "metal-kit-dry",
             "kit": {"ft": {"pitch": "F2", "gain": "12dB", "patch": felt_tom(1.2, 25)},      # felt is soft: +12 dB meets
                     "t3": {"pitch": "B2", "gain": "12dB", "patch": felt_tom(0.9, 30)}}}     # the old toms' level

# The SUB SWELL: a pure F1 sine that fades in across the held cluster and peaks as Ingot's first kick and F1 bass land,
# so the intro's last bar blooms into the floor t2 stands on (the join read 24 dB short at 38 Hz, 23 dB over at 83-97).
SEED_SUB = {"about": "Seed Crystal's sub swell into Ingot (chirper-three): a sine with a 2.6 s attack.",
            "synth": {"layers": [{"name": "sub", "wave": "sine"}, {"name": "oct", "wave": "sine", "ratio": 2, "level": "-14dB"}],
                      "amp": {"a": "2600ms", "d": "0ms", "s": 1, "r": "600ms"}}}

def sub_swell():
    return score([(bar0(HOLD), S, nm(F1), 100, "")])

# The CRYSTAL: the seed's return grows LATTICE's cluster note by note. Each voice strikes with an inharmonic chime ping
# and then sustains (a near-harmonic additive body), so F, Gb, B and E pile up into the chord the Breach hits and holds.
SEED_CRYSTAL = {"about": "Seed Crystal's growing cluster (chirper-three): a chime strike over a sustained glassy body.",
                "synth": {"layers": [
                    {"name": "body", "type": "additive", "partials": [[1, 1], [2.0, 0.22], [3.0, 0.1], [5.04, 0.05]]},
                    {"name": "strike", "type": "additive", "partials": [[1, 0.7], [2.76, 0.35], [5.4, 0.18]],
                     "level": {"value": "-60dB", "mod": [{"src": "env.st", "amount": 60}]}}],
                          "env": {"st": {"a": "0.5ms", "d": "600ms", "s": 0, "curve": 3}},
                          "amp": {"a": "60ms", "d": "0ms", "s": 1, "r": "900ms"}},
                "play": {"vel_sens": 0.4}}

def crystal(k):
    """Voice k of the growing cluster: LATTICE[k] enters on the seed's cell 2k and holds until the hits."""
    a, z = bar0(SEED[0]), bar0(HITS[0])
    for t, i, n in cell_onsets(a, z):
        if i == 0 and n == 2 * k:
            return score([(t, z - t, nm(F1 + 36 + LATTICE[k]), 70, "")])
    return score([])

def tr(name, patch, sc, **kw):
    d = {"name": name, "patch": patch, "score": sc}
    d.update(kw)
    return d

def main():
    tracks = [
        tr("pad", "pad-glass", pad(), gain="-9dB", sends={"hall": "-6dB"}),
        tr("clean-a", "m8-clean", clean_a(), pan="L35", gain="-4dB",
           fx=["delay time=3/16 feedback=0.35 mix=0.28"], sends={"hall": "-10dB"}),
        tr("clean-b", "m8-twang-chorus", clean_b(), pan="R40", gain="-7dB", sends={"hall": "-8dB"}),
        tr("lead", "m8-lead", lead(), gain="-10dB", sends={"hall": "-4dB"},
           fx=["delay time=3/8 feedback=0.3 mix=0.2"]),
        tr("bass", "bass-fat", bass(), gain="-3dB"),
        tr("sub", "seed-sub", sub_swell(), gain="0dB"),
        *[tr(f"xtal{k}", "seed-crystal", crystal(k), gain="-27dB", pan=pn, sends={"hall": "-8dB"})   # the CRYSTAL
          for k, pn in enumerate(("L30", "R30", "L60", "R60"))],
        tr("gtr-l", "m8-emg-l", guitar(), pan="L90", gain="-5dB", seed=7),
        tr("gtr-r", "m8-emg-r", guitar(), pan="R90", gain="-5dB", seed=13),
        tr("kick", "metal-kit-phys", kick(), out="drums"),        # chirper-two's physical kick and snare (v11)
        tr("snare", "metal-kit-phys", snare(), out="drums"),
        tr("cym", "metal-kit-dry", cymbals(), out="drums"),
        tr("toms", "seed-toms", toms(), out="drums", sends={"hall": "-9dB"}),
    ]
    head = [
        'about: "Chirpers I, track 1 (chirper-three): the album\'s opening. Generated by compose/chirpers1/src/chirpers1-t1.py; edit the generator."',
        f"tempo: {TEMPO}",
        'tail: "0.5s"',                # the held F-B-E cluster is still ringing when t2 begins (the songs bleed)
        'ceiling: "-0.1dB"',
        'patches: ' + json.dumps({"seed-toms": SEED_TOMS, "seed-sub": SEED_SUB, "seed-crystal": SEED_CRYSTAL}),
        "buses:",
        '  hall: {fx: ["reverb kind=hall decay=3.4s mix=1 predelay=25ms mono_below=150hz"]}',
        '  drums: {fx: [{"type": "compressor", "threshold": "-18dB", "ratio": 3, "attack": "10ms", "release": "90ms", "makeup": "2dB"}, "reverb kind=room decay=0.6s mix=0.08 predelay=6ms mono_below=200hz"]}',
        'master: ' + json.dumps({"fx": [{"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.ride", "amount": 1}]}},
                                   "glue threshold=-20dB ratio=2.5 attack=10ms release=150ms makeup=3dB",
                                   {"type": "gain", "gain": "11.5dB"}],
                            "auto": {"ride": {"points": ride()}}}),
        "tracks:",
    ]
    lines = head + ["  - " + json.dumps(t) for t in tracks]
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(OUT, f"{BARS} bars at {TEMPO} BPM = {BARS * 4 * 60 / TEMPO:.1f} s")

if __name__ == "__main__":
    main()
