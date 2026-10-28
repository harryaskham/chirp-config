#!/usr/bin/env python3
"""chirpers1-t6 "The machine" (Ferrous Bloom, track 6) - generator for songs/chirpers1-t6.yaml (chirper-zero).

Identity: 128 bpm, a dead-straight 4/4 pulse, F. A machine assembling itself out of t5's ending clock: GEARTRAIN, a
13-sixteenth chug riff, realigns with the bar every 13 bars, so every section is 13 bars and every boundary is a
realignment; gears are added one at a time (a second guitar, LATTICE's 7-cell as a high ping, the GOVERNOR lead in
13 eighths), the machine stalls, then overdrives on a 23-sixteenth cycle (GEARTRAIN + two of t5's breath cells)
and seizes on LATTICE's cluster, held into t7.

Motifs (compose/chirpers1/motifs.md):
  GEARTRAIN  13 sixteenths: X . x x . O . x x . S . .  (X accent chug, x palm-muted chug, O open octave tooth,
             S tritone stab F1 B1 F2), kick in unison. Roots by cycle in the governor: F F Gb G Gb.
  GOVERNOR   13 eighths (26 sixteenths: realigns every 13 bars too): F4 B4 E5 F5 Gb5 F5 E5 B4 F4 Gb4 B4 C5 E5 -
             LATTICE's colour (F Gb B E) with t5's C, as a mechanical arpeggio.
  OVERDRIVE  23 sixteenths = GEARTRAIN + t5's BREATH CELL twice (x x . x . | x x . x .) on Gb1.
Borrowed: t5's 13-count clock (5+4+4) opens the track at t5's speed (its sixteenths = our eighths); LATTICE's
3+2+2 7-cell and F-Gb-B-E line as the ping gear; LATTICE's final cluster F1 B1 E2 + Gb5 to close.
Run: python3 compose/chirpers1/src/chirpers1-t6.py  (writes songs/chirpers1-t6.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.path.join(ROOT, "songs", "chirpers1-t6.yaml")
BPM = 128
BAR = 4.0
S16 = 0.25
MG = float(os.environ.get("T6_MG", "15"))
FORM = [("spin", 13), ("engage", 13), ("mesh", 13), ("governor", 13), ("stall", 13), ("overdrive", 23), ("seize", 13)]


def tok(n, d, v=None, art=""):
    return f"{n}/{d:g}b" + (f"@{int(v)}" if v is not None else "") + art


def rest(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def join(*xs):
    return " ".join(x for x in xs if x)


# ---------------------------------------------------------------- motifs
GEAR = "X.xx.O.xx.S.."  # 13


def up(n, k=1):
    """Semitone transposition of a note name with sharps (F1 -> F#1)."""
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    flat = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
    p, o = n[:-1], int(n[-1])
    p = flat.get(p, p)
    i = names.index(p) + k
    return names[i % 12] + str(o + i // 12)


def gear_steps(pattern, root, vel_scale=1.0):
    """One cycle of a chug pattern -> list of (guitar token, bass token, kick token) per sixteenth (stabs: 2 steps)."""
    g, b, k = [], [], []
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == "X":
            g.append(tok(root, S16, 112 * vel_scale, "^pm")); b.append(tok(root, S16, 104)); k.append("k/0.25b@116")
        elif c == "o":  # open root + octave, lighter
            g.append(tok(f"{root},{up(root, 12)}", S16, 96)); b.append(tok(root, S16, 88)); k.append("k/0.25b@96")
        elif c == "x":
            g.append(tok(root, S16, 94 * vel_scale, "^pm")); b.append(tok(root, S16, 90)); k.append("k/0.25b@100")
        elif c == "O":
            g.append(tok(f"{root},{up(root, 12)}", S16, 106)); b.append(tok(root, S16, 96)); k.append("k/0.25b@104")
        elif c == "S" and i + 1 < len(pattern) and pattern[i + 1] == ".":
            g.append(tok(f"{root},{up(root, 6)},{up(root, 12)}", 2 * S16, 116)); b.append(tok(root, 2 * S16, 108))
            k.append("c,k/0.5b@120"); i += 2; continue
        else:
            g.append(rest(S16)); b.append(rest(S16)); k.append(rest(S16))
        i += 1
    return g, b, k


def riff(nbars, pattern, roots=None, vel=1.0, mute_every=0, kick="unison"):
    """Run `pattern` (sixteenth slots) across nbars of 4/4, cycle after cycle (roots per cycle). mute_every=2 drops
    every other cycle (the stall). Returns (guitar, bass, kick) score strings and the cycle-start positions (16ths)."""
    total = nbars * 16
    G, B, K, starts = [], [], [], []
    pos, cyc = 0, 0
    while pos < total:
        root = (roots or ["F1"])[cyc % len(roots or ["F1"])]
        n = min(len(pattern), total - pos)
        pat = pattern[:n]
        if pat.endswith("S"):
            pat = pat[:-1] + "x"
        starts.append(pos)
        if mute_every and cyc % mute_every == 1:
            G.append(rest(n * S16)); B.append(rest(n * S16)); K.append(rest(n * S16))
        else:
            g, b, k = gear_steps(pat, root, vel)
            if kick == "accents":  # kick only on X, O and stabs
                k = [t if (t.startswith("c,") or "@116" in t or "@104" in t or t.startswith("R/")) else "R/" + t.split("/")[1].split("@")[0] for t in k]
            elif kick == "double":  # a machine-gun double kick under everything
                k = [("c,k/0.5b@120" if t.startswith("c,") else (f"k/{t.split('/')[1].split('@')[0]}@{96 if t.startswith('R/') else 112}")) for t in k]
            G += g; B += b; K += k
        pos += n; cyc += 1
    return join(*G), join(*B), join(*K), starts


def kit_layer(nbars, kick_tokens, snare="3", hats="8", ride=False, crash_at=(), accent13=False):
    """Merge a kick line (sixteenth tokens, some 0.5b) with a steady pulse: snare on beat 3 (half time) or on 2 and
    4, hats on 8ths or 16ths (accent every 13 when accent13), crashes at the given 16th positions."""
    toks = kick_tokens.split() if kick_tokens else [rest(S16)] * (nbars * 16)
    out, pos = [], 0
    for t in toks:
        d16 = int(round(float(t.split("/")[1].split("b")[0]) * 4))
        bp = pos % 16
        extra = []
        if (snare == "3" and bp == 8) or (snare == "24" and bp in (4, 12)):
            extra.append("s")
        if hats == "8" and bp % 2 == 0:
            extra.append("rc" if ride else "h1")
        if hats == "16":
            extra.append("h1")
        if hats == "4" and bp % 4 == 0:
            extra.append("h1")
        if pos in crash_at:
            extra.append("c")
        if t.startswith("R/"):
            out.append(",".join(extra) + f"/{d16 / 4:g}b@{(84 if 's' in extra else 70) if not accent13 or pos % 13 else 96}" if extra else t)
        else:
            pre, rest_ = t.split("/", 1)
            names = [p for p in pre.split(",") if p not in extra] + extra
            out.append(",".join(names) + "/" + rest_)
        pos += d16
    return join(*out)


GOVERNOR = ["F4", "B4", "E5", "F5", "F#5", "F5", "E5", "B4", "F4", "F#4", "B4", "C5", "E5"]


def governor(nbars, octave=0, vel=92, long=False):
    out, i = [], 0
    if long:  # one note per beat
        for j in range(nbars * 4):
            n = GOVERNOR[j % 13]
            out.append(tok(n if not octave else up(n, 12 * octave), 1, vel))
        return join(*out)
    for j in range(nbars * 8):
        n = GOVERNOR[j % 13]
        out.append(tok(n if not octave else up(n, 12 * octave), 0.5, vel if j % 13 == 0 else vel - 10))
    return join(*out)


def ping7(nbars, vel=70):
    """LATTICE's 3+2+2 seven-cell walking F Gb B E (one note per onset), high, on the twang chorus."""
    line = ["F5", "F#5", "B5", "E6"]
    out, pos, k = [], 0, 0
    total = nbars * 16
    while pos < total:
        for seg in (3, 2, 2):
            if pos >= total:
                break
            d = min(seg, total - pos)
            out.append(tok(line[k % 4], d * S16, vel)); k += 1; pos += d
    return join(*out)


def clock13(nbars, unit=0.5, vel=(92, 54)):
    """t5's ending figure (F3 C4 E4 B4 G4 counted 5+4+4) on the clean, at `unit` beats per note."""
    cell = ["F3", "C4", "E4", "B4", "G4"]
    per_bar = int(BAR / unit)
    out = []
    for st in range(nbars * per_bar):
        ph = st % 13
        kk = ph if ph < 5 else (ph - 5) % 4
        out.append(tok(cell[kk], unit, vel[0] if ph == 0 else vel[1] + (8 if ph in (5, 9) else 0)))
    return join(*out)


def ticks(nbars, unit, vel=(78, 42)):
    per_bar = int(BAR / unit)
    return join(*[f"h1/{unit:g}b@{vel[0] if st % 13 == 0 else vel[1] + (st % 2) * 6}" for st in range(nbars * per_bar)])


# ---------------------------------------------------------------- arrangement
def build():
    names = ("pad", "cln", "tick", "gtr-l", "gtr-r", "bass", "drums", "ping", "gov", "sub")
    T = {n: [] for n in names}

    def put(name, s, beats):
        T[name].append((s, beats))

    t_beats = 0
    for sec, n in FORM:
        beats = n * BAR
        used = set()
        if sec == "spin":
            put("pad", join(tok("F2,C3,E3,B3,G4", BAR * 4, 70), tok("F2,C3,E3,B3,G4", BAR * 4, 56), rest(beats - BAR * 8)), beats)
            put("cln", join(clock13(8, 0.5), clock13(4, 0.25, (96, 60)), rest(BAR)), beats)
            put("tick", join(ticks(8, 0.5), ticks(5, 0.25, (84, 46))), beats)
            put("drums", join(rest(BAR * 10), " ".join(["k/1b@96"] * 8), " ".join(f"s/0.25b@{50 + 4 * i}" for i in range(16))), beats)
            put("bass", join(rest(BAR * 12), tok("F1", BAR, 90)), beats)
            put("sub", join(rest(BAR * 12), tok("F1", BAR, 100)), beats)
            used |= {"pad", "cln", "tick", "drums", "bass", "sub"}
        elif sec in ("engage", "mesh", "governor", "seize"):
            roots = ["F1", "F1", "F#1", "G1", "F#1"] if sec == "governor" else ["F1"]
            pat = "O.oo.O.oo.S.." if sec == "governor" else GEAR  # the governor opens the gears: ringing octaves
            g, b, k, starts = riff(n if sec != "seize" else n - 2, pat, roots, vel=0.9 if sec == "engage" else 1.0,
                                   kick="accents" if sec == "engage" else "unison")
            if sec == "seize":  # two final bars: LATTICE's cluster, held into t7
                g = join(g, tok("F1,B1,E2", BAR * 2, 118)); b = join(b, tok("F1", BAR * 2, 110))
                k = join(k, "c,k/2b@124", rest(BAR * 2 - 2))
            put("gtr-l", g, beats); put("bass", b, beats)
            if sec != "engage":
                put("gtr-r", g, beats); used.add("gtr-r")
            put("drums", kit_layer(n, k, snare="3" if sec in ("engage", "mesh", "governor", "seize") else "24",
                                   hats={"engage": "4", "governor": "16"}.get(sec, "8"), ride=(sec == "governor"), crash_at={0}), beats)
            if sec in ("mesh", "seize"):
                put("ping", ping7(n if sec == "mesh" else n - 2) + (" " + rest(BAR * 2) if sec == "seize" else ""), beats); used.add("ping")
            if sec == "governor":
                put("gov", governor(n), beats); used.add("gov")
            if sec == "seize":
                put("gov", join(governor(n - 2, long=True, vel=98), tok("F#5", BAR * 2, 96)), beats); used.add("gov")
                put("pad", join(rest(BAR * (n - 2)), tok("F2,B2,E3,F#4", BAR * 2, 70)), beats); used.add("pad")
                put("tick", ticks(n - 2, 0.25, (80, 40)) + " " + rest(BAR * 2), beats); used.add("tick")
            used |= {"gtr-l", "bass", "drums"}
        elif sec == "stall":
            # the machine stalls: only the first three slots of every other cycle survive (X . x), quieter
            frag = "X.x" + "." * 10
            g, b, k, starts = riff(n, frag, ["F1"], vel=0.8, mute_every=2)
            put("gtr-l", g, beats); put("gtr-r", g, beats); put("bass", b, beats)
            put("drums", kit_layer(n, k, snare="none", hats="none"), beats)
            put("pad", join(*[tok("F2,C3,E3,B3,G4" if i % 2 == 0 else "F2,F#2,B2,E3", BAR, 60) for i in range(n)]), beats)
            put("cln", clock13(n, 0.25, (80, 50)), beats)
            used |= {"gtr-l", "gtr-r", "bass", "drums", "pad", "cln"}
        elif sec == "overdrive":
            pat = GEAR + "xx.x." + "xx.x."  # 23
            g, b, k, starts = riff(n, pat, ["F1", "F1", "F#1"], vel=1.05, kick="double")
            put("gtr-l", g, beats); put("gtr-r", g, beats); put("bass", b, beats)
            put("drums", kit_layer(n, k, snare="24", hats="16", crash_at=set(starts[::2]), accent13=False), beats)
            put("gov", governor(n, vel=94), beats)
            put("ping", ping7(n, vel=64), beats)
            put("sub", join(*[tok("F1", BAR * 1, 70) if i % 4 == 0 else rest(BAR) for i in range(n)]), beats)
            used |= {"gtr-l", "gtr-r", "bass", "drums", "gov", "ping", "sub"}
        for nm in names:
            if nm not in used:
                put(nm, rest(beats), beats)
        t_beats += beats
    return T, t_beats


def song():
    T, total = build()

    def sc(name):
        for s, b in T[name]:
            got = sum(float(x.split("/")[1].split("b")[0]) for x in s.split() if "/" in x and x != "|")
            assert abs(got - b) < 1e-6, (name, got, b)
        return " | ".join(s for s, _ in T[name])

    tracks = [
        {"name": "pad", "patch": "juno-pad", "gain": "-10dB", "sends": {"hall": "-8dB"}, "score": sc("pad")},
        {"name": "cln", "patch": "m8-clean", "gain": "-5dB", "pan": -0.35, "sends": {"dly": "-14dB"}, "score": sc("cln")},
        {"name": "tick", "patch": "metal-kit", "gain": "-9dB", "pan": 0.35, "score": sc("tick")},
        {"name": "gtr-l", "patch": "m8-emg-l", "gain": "-4dB", "pan": -1, "score": sc("gtr-l")},
        {"name": "gtr-r", "patch": "m8-emg-r", "gain": "-4dB", "pan": 1, "score": sc("gtr-r")},
        {"name": "bass", "patch": "bass-fat", "gain": "-5dB", "score": sc("bass")},
        {"name": "sub", "patch": "bass-fat", "gain": "-8dB", "score": sc("sub")},
        {"name": "drums", "patch": "metal-kit", "gain": "-3dB", "score": sc("drums")},
        {"name": "ping", "patch": "m8-twang-chorus", "gain": "-16dB", "pan": 0.6, "sends": {"dly": "-10dB"}, "score": sc("ping")},
        {"name": "gov", "patch": "m8-lead", "gain": "-9dB", "pan": 0.05, "score": sc("gov")},
    ]
    return {
        "about": ("Chirpers - Ferrous Bloom, track 6 'The machine' (original composition, chirper-zero; generator "
                  "compose/chirpers1/src/chirpers1-t6.py). 128 bpm 4/4 in F. GEARTRAIN, a 13-sixteenth chug riff, "
                  "realigns every 13 bars, so each section is a 13-bar realignment; the machine assembles out of t5's "
                  "13-count clock (gears: a second guitar, LATTICE's 7-cell as a high ping, the GOVERNOR lead in 13 "
                  "eighths), stalls, overdrives on 23 sixteenths (GEARTRAIN + two of t5's breath cells) and seizes on "
                  "LATTICE's cluster F1 B1 E2, held into t7."),
        "tempo": BPM, "ceiling": "-0.1dB", "tail": "2s",
        "buses": {"hall": {"fx": ["reverb kind=hall decay=2.6s mix=1 predelay=20ms"]},
                  "dly": {"fx": ["delay time=3/16 feedback=.32 mix=1 ping_pong=true", "reverb kind=room decay=1.2s mix=0.3"]}},
        "master": {"fx": [{"type": "eq", "bands": ["peak cutoff=350 q=0.8 gain=-3dB", "highshelf cutoff=5k gain=2dB"]},
                          {"type": "compressor", "threshold": "-24dB", "ratio": 2, "attack": "10ms", "release": "200ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MG:g}dB"}]},
        "tracks": tracks,
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "tail", "master")]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = dump(song())
    open(OUT, "w").write(text)
    print("wrote", OUT)
