#!/usr/bin/env python3
"""chirpers1-t5 "The breath" (Chirpers I, track 5) - generator for songs/chirpers1-t5.yaml (chirper-zero).

Identity: 64 bpm, 4/4 pulse, F lydian. The air after track 4's onslaught: a clean five-sixteenth figure that
ripples against the slow bar (realigning every five bars), pads, a long falling lead line; one crushing half-time
passage on the same five-cell, in F against Gb; the figure comes back reharmonised, the lead in augmentation; the
ending counts the figure in thirteens, a clock that hands over to track 6 ("the machine").

Motifs (also in compose/chirpers1/motifs.md):
  BREATH CELL  five sixteenths. Clean: an arpeggio rising root-5-7-#11 and stepping back to the 9th
               (F3 C4 E4 B4 G4) on every sixteenth, so its downbeat drifts against the bar (5 against 16).
               Heavy: the same cell as palm-muted chugs on steps 1, 2 and 4 (x x . x .).
  COLD CHORD   the lydian tritone: root, fifth, major seventh, sharp eleventh, no third (F C E B).
  EXHALE       the lead: E5 B4 C5 | G4 A4 | E5 D5 B4 | F4 (falls a fifth, steps up, falls, lands a tritone below
               where it started), stated, then displaced by an eighth, then howled on the heavy lead, then in
               augmentation.
Run: python3 compose/chirpers1/src/chirpers1-t5.py  (writes songs/chirpers1-t5.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.path.join(ROOT, "songs", "chirpers1-t5.yaml")
BPM = 64
BAR = 4.0  # beats
MG = float(os.environ.get("T5_MG", "20"))  # master make-up gain (dB) before the ceiling

# ---------------------------------------------------------------- motifs
# The breath cell's clean arpeggio per harmony (five notes each, F lydian throughout until the exhale's Db).
CELLS = {
    "F": ["F3", "C4", "E4", "B4", "G4"],      # cold chord: F C E B (+G)
    "Dm": ["D3", "A3", "E4", "C5", "F4"],     # vi with the ninth
    "Am": ["A2", "E3", "G3", "C4", "B3"],     # iii, low
    "Bo": ["B2", "F3", "A3", "D4", "E4"],     # the #4 itself: half-diminished with the eleventh
    "Db": ["Db3", "Ab3", "C4", "G4", "Eb4"],  # the exhale's reharmonisation: Dbmaj7#11 (a third below F)
    "Bb": ["Bb2", "F3", "A3", "E4", "C4"],    # Bbmaj7#11 (lydian colour moved to the fourth)
}
PAD = {  # pad voicings (cold chord shapes)
    "F": "F2,C3,E3,B3,G4", "Dm": "D2,A2,F3,C4,E4", "Am": "A1,E2,C3,G3,B3", "Bo": "B1,F2,A2,D3,E4",
    "Db": "Db2,Ab2,C3,G3,Eb4", "Bb": "Bb1,F2,A2,E3,C4", "Gb": "Gb1,Db2,F2,C3",
}
BASS = {"F": "F1", "Dm": "D2", "Am": "A1", "Bo": "B1", "Db": "Db2", "Bb": "Bb1", "Gb": "Gb1"}
EXHALE = [("E5", 2), ("B4", 1), ("C5", 1), ("G4", 3), ("A4", 1), ("E5", 1.5), ("D5", 0.5), ("B4", 2), ("F4", 4)]


def tok(n, d, v=None, art=""):
    s = f"{n}/{d:g}b"
    if v is not None:
        s += f"@{int(v)}"
    return s + art


def rest(d):
    return f"R/{d:g}b" if d > 0 else ""


def breath_clean(harms, start_step=0, vel=(84, 58), cycle=5, accent_every=None):
    """The breath cell on every sixteenth over the bars of `harms` (one harmony per bar); the cell keeps running
    across bar lines (start_step carries the phase). cycle 5 = the cell, 13 = the machine count (5+4+4)."""
    out, step = [], start_step
    for h in harms:
        notes = CELLS[h]
        for i in range(16):
            ph = step % cycle
            if cycle == 13:  # 5 + 4 + 4: the cell, then the cell without its last note, twice
                k = ph if ph < 5 else (ph - 5) % 4
            else:
                k = ph % 5
            v = vel[0] if ph == 0 else vel[1] + (6 if (cycle == 13 and ph in (5, 9)) else 0) + (i % 4 == 0) * 4
            out.append(tok(notes[k], 0.25, v))
            step += 1
    return " ".join(out), step


def breath_heavy(nbars, roots, displace=0, stab_every=4, end_stop=False):
    """The breath cell as palm-muted chugs: hits on cell steps 0, 1, 3 (x x . x .); every `stab_every`-th cell
    opens into a ringing tritone stab. Returns (guitar, bass, kick) scores."""
    g, b, k = [], [], []
    step = -displace
    ncell = 0
    total = nbars * 16
    i = 0
    while i < total:
        bar = i // 16
        root = roots[bar]
        ph = step % 5
        if ph == 0:
            ncell += 1
        last = end_stop and bar == nbars - 1 and (i % 16) >= 1
        if last:
            g.append(rest(0.25)); b.append(rest(0.25)); k.append(rest(0.25))
        elif ph in (0, 1, 3):
            stab = (ncell % stab_every == 0) and ph == 0 and i + 2 <= total and not (end_stop and bar == nbars - 1)
            if stab:
                tri = {"F1": "F1,B1,F2", "Gb1": "Gb1,C2,Gb2"}[root]
                g.append(tok(tri, 0.5, 112)); b.append(tok(root, 0.5, 112)); k.append("c,k/0.5b@118")
                i += 2; step += 2
                continue
            g.append(tok(root, 0.25, 108 if ph == 0 else 92, "^pm")); b.append(tok(root, 0.25, 100 if ph == 0 else 86))
            k.append(f"k/0.25b@{112 if ph == 0 else 96}")
        else:
            g.append(rest(0.25)); b.append(rest(0.25)); k.append(rest(0.25))
        i += 1; step += 1
    return " ".join(g), " ".join(b), " ".join(k)


def exhale(scale=1.0, octave=0, vel=88, displace=0.0):
    out = [rest(displace)] if displace else []
    shift = {0: lambda n: n, 1: lambda n: n[:-1] + str(int(n[-1]) + 1), -1: lambda n: n[:-1] + str(int(n[-1]) - 1)}[octave]
    for i, (n, d) in enumerate(EXHALE):
        out.append(tok(shift(n), d * scale, vel - (6 if i % 3 else 0)))
    s = " ".join(x for x in out if x)
    return s, sum(d for _, d in EXHALE) * scale + displace


# ---------------------------------------------------------------- form (bars of 4/4 at 64 bpm = 3.75 s)
# A inhale 6 | B drift 6 | C float 10 | D held 4 | E weight 8 | E2 weight, displaced, stop 4 | F exhale 10 | G clock 6
FORM = [("A", 6), ("B", 6), ("C", 10), ("D", 4), ("E", 8), ("E2", 4), ("F", 10), ("G", 6)]
HARM = {
    "A": ["F"] * 6,
    "B": ["F", "F", "Dm", "Dm", "F", "F"],
    "C": ["F", "F", "Dm", "Dm", "Am", "Am", "Bo", "Bo", "F", "F"],
    "D": ["F", "F", "Bo", "Bo"],
    "F": ["Db", "Db", "Bb", "Bb", "Db", "Db", "Bb", "Bb", "F", "F"],
    "G": ["F"] * 6,
}


def build():
    T = {n: [] for n in ("pad", "glass", "cln", "cln2", "mel", "howl", "bass", "gtr-l", "gtr-r", "drums", "tick")}

    def add(name, s, beats):
        T[name].append((s, beats))

    def pad_bars(name, harms, vel=70):
        add(name, " ".join(tok(PAD[h], BAR, vel) for h in harms), BAR * len(harms))

    def silent(name, beats):
        add(name, rest(beats), beats)

    phase = 0
    for sec, n in FORM:
        beats = n * BAR
        used = set()
        if sec == "A":
            # the moment after the onslaught: one ringing low chord + crash, decaying into the pad swell
            add("gtr-l", tok("F1,C2,F2,B2", BAR * 2, 112) + " " + rest(beats - BAR * 2), beats)
            add("gtr-r", tok("F1,C2,F2,B2", BAR * 2, 110) + " " + rest(beats - BAR * 2), beats)
            add("drums", "c,k/2b@120 " + rest(beats - 2), beats)
            add("bass", tok("F1", BAR * 2, 108) + " " + rest(beats - BAR * 2), beats)
            pad_bars("pad", HARM[sec], vel=60)
            s, phase2 = breath_clean(HARM[sec][2:], phase, vel=(70, 48))
            add("cln", rest(BAR * 2) + " " + s, beats); phase = phase2
            used |= {"gtr-l", "gtr-r", "drums", "bass", "pad", "cln"}
        elif sec in ("B", "C"):
            pad_bars("pad", HARM[sec], vel=64 if sec == "B" else 70)
            s, phase = breath_clean(HARM[sec], phase, vel=(84, 58) if sec == "C" else (78, 54))
            add("cln", s, beats)
            add("bass", " ".join(tok(BASS[h], BAR, 74) for h in HARM[sec]), beats)
            if sec == "B":
                m, mb = exhale(vel=86)
                add("mel", rest(BAR * 2) + " " + m + " " + rest(beats - BAR * 2 - mb), beats)
                # kit: a breath of ride on beat 1, kick on 1
                add("drums", " ".join(["k,rc/1b@70 h1/1b@44 h1/1b@50 h1/1b@44"] * n), beats)
            else:
                m1, mb1 = exhale(vel=90)
                m2, mb2 = exhale(vel=92, displace=0.5, octave=0)
                add("mel", m1 + " " + rest(BAR) + " " + m2 + " " + rest(beats - mb1 - BAR - mb2), beats)
                # second clean: the cell's downbeats only, an octave up, on the other side
                c2 = []
                for b in range(n):
                    c2.append(f"{CELLS[HARM[sec][b]][3]}/1.25b@62 {CELLS[HARM[sec][b]][2]}/1.25b@56 {CELLS[HARM[sec][b]][4]}/1.5b@58")
                add("cln2", " ".join(c2), beats)
                # kit: soft hat eighths, kick on the cell's 5-step downbeats (polymeter), rim on 3
                d = []
                for b in range(n):
                    bar = []
                    for i in range(16):
                        absstep = b * 16 + i
                        hits = []
                        if i % 2 == 0:
                            hits.append("h1")
                        if absstep % 5 == 0:
                            hits.append("k")
                        if i == 8:
                            hits.append("so")
                        bar.append((",".join(hits) + f"/0.25b@{64 if 'k' in hits else 46}") if hits else "R/0.25b")
                    d.append(" ".join(bar))
                add("drums", " ".join(d), beats)
                add("glass", rest(BAR * 6) + " " + " ".join(tok(PAD[h], BAR, 54) for h in HARM[sec][6:]), beats)
            used |= {"pad", "cln", "bass", "mel", "drums"} | ({"cln2", "glass"} if sec == "C" else set())
        elif sec == "D":
            # breath held: the cell in augmentation (quarters), thinning; a swell into the weight
            notes = []
            for b, h in enumerate(HARM[sec]):
                c = CELLS[h]
                notes.append(" ".join(tok(c[(b * 4 + j) % 5], 1, 66 - b * 4) for j in range(4)))
            add("cln", " ".join(notes), beats)
            pad_bars("pad", HARM[sec], vel=72)
            add("glass", rest(BAR * 2) + " " + tok("B3,E4,B4", BAR * 2, 70), beats)
            add("drums", rest(BAR * 3) + " " + " ".join(f"s/0.25b@{40 + 5 * i}" for i in range(16)), beats)
            add("bass", rest(BAR * 3) + " " + tok("F1", BAR, 60), beats)
            used |= {"cln", "pad", "glass", "drums", "bass"}
        elif sec in ("E", "E2"):
            roots = (["F1"] * 4 + ["Gb1"] * 2 + ["F1"] * 2) if sec == "E" else (["F1", "Gb1", "F1", "F1"])
            g, bs, k = breath_heavy(n, roots, displace=0 if sec == "E" else 1, stab_every=4 if sec == "E" else 3,
                                    end_stop=(sec == "E2"))
            add("gtr-l", g, beats); add("gtr-r", g, beats); add("bass", bs, beats)
            # kit: kick with the chugs, half-time snare on 3, china/ride quarters
            ks = k.split()
            # merge: snare on beat 3 of each bar (half time), ride quarters; positions in sixteenths
            out = []
            pos = 0
            for t in ks:
                dur16 = int(round(float(t.split("/")[1].split("b")[0]) * 4))
                barpos = pos % 16
                extra = []
                if barpos == 8:
                    extra.append("s")
                if barpos % 4 == 0:
                    extra.append("rc")
                if sec == "E2" and pos // 16 == n - 1 and barpos >= 1:
                    out.append(t if t.startswith("R/") else "R/" + t.split("/")[1].split("@")[0]); pos += dur16; continue
                if t.startswith("R/"):
                    out.append((",".join(extra) + f"/{dur16 / 4:g}b@96") if extra else t)
                else:
                    pre, rest_ = t.split("/", 1)
                    out.append(",".join([pre] + extra) + "/" + rest_)
                pos += dur16
            add("drums", " ".join(out), beats)
            pad_bars("pad", ["F"] * 4 + ["Gb"] * 2 + ["F"] * 2 if sec == "E" else ["F", "Gb", "F", "F"], vel=58)
            if sec == "E":
                m, mb = exhale(vel=96, octave=0)
                add("howl", m + " " + rest(beats - mb), beats)
            used |= {"gtr-l", "gtr-r", "bass", "drums", "pad"} | ({"howl"} if sec == "E" else set())
        elif sec == "F":
            pad_bars("pad", HARM[sec], vel=66)
            s, phase = breath_clean(HARM[sec], phase, vel=(80, 54))
            add("cln", s, beats)
            add("bass", " ".join(tok(BASS[h], BAR, 70) for h in HARM[sec]), beats)
            m, mb = exhale(scale=2.0, vel=84)
            add("mel", rest(BAR * 1) + " " + m + " " + rest(beats - BAR - mb), beats)
            add("glass", " ".join(tok(PAD[h], BAR, 50) for h in HARM[sec]), beats)
            add("drums", " ".join(["rbs,k/1b@58 h1/1b@42 h1/1b@48 h1/1b@42"] * n), beats)
            used |= {"pad", "cln", "bass", "mel", "glass", "drums"}
        elif sec == "G":
            pad_bars("pad", HARM[sec], vel=64)
            s, _ = breath_clean(HARM[sec], 0, vel=(86, 56), cycle=13)
            add("cln", s, beats)
            add("bass", " ".join(tok("F1", BAR, 66) for _ in range(n)), beats)
            # the clock: hats on every sixteenth, accent on the 13-count
            tk = []
            for b in range(n):
                for i in range(16):
                    st = b * 16 + i
                    tk.append(f"h1/0.25b@{70 if st % 13 == 0 else 40 + (st % 2) * 6}")
            add("tick", " ".join(tk), beats)
            add("drums", " ".join(["k/1b@64 R/3b"] * n), beats)
            used |= {"pad", "cln", "bass", "tick", "drums"}
        for name in T:
            if name not in used:
                silent(name, beats)
    return T


def song():
    T = build()
    total_beats = sum(n for _, n in FORM) * BAR
    def sc(name):
        s = " | ".join(x for x, _ in T[name] if x)
        assert abs(sum(b for _, b in T[name]) - total_beats) < 1e-6, name
        return s
    tracks = [
        {"name": "pad", "patch": "juno-pad", "gain": "-14dB", "pan": 0, "sends": {"hall": "-8dB"}, "score": sc("pad")},
        {"name": "glass", "patch": "pad-glass", "gain": "-16dB", "pan": 0.2, "score": sc("glass")},
        {"name": "cln", "patch": "m8-clean", "gain": "-9dB", "pan": -0.45, "sends": {"dly": "-12dB", "hall": "-12dB"}, "score": sc("cln")},
        {"name": "cln2", "patch": "m8-twang-chorus", "gain": "-15dB", "pan": 0.55, "sends": {"hall": "-10dB"}, "score": sc("cln2")},
        {"name": "mel", "patch": "m8-clean", "gain": "-7dB", "pan": 0.1, "sends": {"dly": "-6dB", "hall": "-8dB"}, "score": sc("mel")},
        {"name": "howl", "patch": "m8-lead", "gain": "-6dB", "pan": 0, "score": sc("howl")},
        {"name": "bass", "patch": "bass-fat", "gain": "-6dB", "pan": 0, "score": sc("bass")},
        {"name": "gtr-l", "patch": "m8-emg-l", "gain": "-1dB", "pan": -1, "score": sc("gtr-l")},
        {"name": "gtr-r", "patch": "m8-emg-r", "gain": "-1dB", "pan": 1, "score": sc("gtr-r")},
        {"name": "drums", "patch": "metal-kit", "gain": "-4dB", "score": sc("drums")},
        {"name": "tick", "patch": "metal-kit", "gain": "-12dB", "pan": 0.3, "score": sc("tick")},
    ]
    doc = {
        "about": ("Chirpers - Chirpers I, track 5 'The breath' (original composition, chirper-zero; generator "
                  "compose/chirpers1/src/chirpers1-t5.py). 64 bpm, F lydian: a clean five-sixteenth 'breath cell' "
                  "rippling against the bar, pads and a falling lead ('exhale'); one crushing half-time passage of "
                  "the same cell in F against Gb; the figure returns over Db/Bb, the lead in augmentation; the ending "
                  "counts the cell in thirteens for track 6."),
        "tempo": BPM,
        "ceiling": "-0.1dB",
        "tail": "3s",
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=3.2s mix=1 predelay=24ms"]},
            "dly": {"fx": ["delay time=3/16 feedback=.38 mix=1 ping_pong=true", "reverb kind=hall decay=2.4s mix=0.4"]},
        },
        "master": {"fx": [
            {"type": "eq", "bands": ["peak cutoff=350 q=0.8 gain=-5dB", "highshelf cutoff=4k gain=5dB"]},
            {"type": "compressor", "threshold": "-28dB", "ratio": 2, "attack": "15ms", "release": "250ms", "makeup": "0dB"},
            {"type": "gain", "gain": f"+{MG:g}dB"},
        ]},
        "tracks": tracks,
    }
    return doc


def dump(doc):
    lines = []
    for k in ("about", "tempo", "ceiling", "tail", "master"):
        lines.append(f"{k}: {json.dumps(doc[k])}")
    lines.append("buses:")
    for b, v in doc["buses"].items():
        lines.append(f"  {b}: {json.dumps(v)}")
    lines.append("tracks:")
    for t in doc["tracks"]:
        lines.append("  - " + json.dumps(t))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = dump(song())
    open(OUT, "w").write(text)
    print("wrote", OUT)
