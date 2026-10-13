#!/usr/bin/env python3
"""Compose fresh tempo-inheriting parts (16 beats = 4 bars) for a song: key, mode and a
four-chord progression, then a style-idiomatic main riff, a hook built from a motif
(statement, repeat, sequence, cadence), chords, an arpeggio and a held layer.
Deterministic from `seed`, so any form slot can regenerate the same material."""
import json, random, re

SONGS = "/home/harry/.config/chirp/songs"
MODES = {
    "minor": [0, 2, 3, 5, 7, 8, 10], "dorian": [0, 2, 3, 5, 7, 9, 10], "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "harmonic": [0, 2, 3, 5, 7, 8, 11], "lydian": [0, 2, 4, 6, 7, 9, 11], "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "major": [0, 2, 4, 5, 7, 9, 11],
    "locrian": [0, 1, 3, 5, 6, 8, 10], "diminished": [0, 1, 3, 4, 6, 7, 9, 10],
    # Evil: double harmonic (Byzantine), Hungarian minor, Neapolitan minor, phrygian dominant.
    "double-harmonic": [0, 1, 4, 5, 7, 8, 11], "hungarian": [0, 2, 3, 6, 7, 8, 11],
    "neapolitan": [0, 1, 3, 5, 7, 8, 11], "phrygian-dominant": [0, 1, 4, 5, 7, 8, 10],
}
PROGS = {  # 0-based scale-degree roots, one chord per bar
    "minor": [[0, 5, 2, 6], [0, 3, 6, 2], [0, 5, 3, 4], [0, 6, 5, 6], [0, 2, 6, 3], [0, 5, 6, 4], [0, 3, 0, 4]],
    "dorian": [[0, 3, 0, 3], [0, 6, 3, 0], [0, 1, 6, 3], [0, 3, 6, 4]],
    "phrygian": [[0, 1, 0, 6], [0, 1, 5, 1], [0, 5, 1, 0], [0, 6, 1, 0]],
    "harmonic": [[0, 5, 1, 4], [0, 3, 4, 0], [0, 5, 3, 4], [0, 2, 3, 4]],
    "lydian": [[0, 1, 0, 1], [0, 1, 4, 3], [0, 4, 1, 5]],
    "mixolydian": [[0, 6, 3, 0], [0, 3, 6, 4], [0, 6, 5, 3]],
    "major": [[0, 4, 5, 3], [0, 3, 4, 0], [0, 5, 3, 4], [0, 3, 1, 4]],
    "locrian": [[0, 1, 0, 1], [0, 1, 4, 1], [0, 6, 1, 0]],
    "diminished": [[0, 1, 0, 1], [0, 2, 1, 0], [0, 1, 4, 1]],
    "double-harmonic": [[0, 1, 0, 1], [0, 1, 3, 1], [0, 5, 1, 0]],
    "hungarian": [[0, 3, 0, 1], [0, 5, 3, 4], [0, 3, 5, 4]],
    "neapolitan": [[0, 1, 0, 4], [0, 1, 5, 4], [0, 5, 1, 0]],
    "phrygian-dominant": [[0, 1, 0, 6], [0, 1, 5, 1], [0, 6, 5, 1]],
}
STYLE_MODES = {
    "djent": ["phrygian", "minor", "harmonic", "phrygian-dominant", "neapolitan", "hungarian"],
    "djent-breakdown": ["phrygian", "harmonic", "double-harmonic", "locrian"],
    "doom-ambient": ["minor", "phrygian", "harmonic"], "hardcore": ["phrygian", "minor"], "acid": ["phrygian", "minor", "dorian"],
    "idm": ["dorian", "lydian", "minor", "harmonic"], "prog-clean": ["dorian", "lydian", "minor", "mixolydian"],
    "poly": ["dorian", "mixolydian", "minor", "major"], "house": ["minor", "dorian", "major"], "garage": ["minor", "dorian"],
    "lofi": ["dorian", "major", "minor", "mixolydian"], "classical": ["harmonic", "major", "minor"],
    "meshuggah": ["phrygian", "locrian", "diminished", "double-harmonic", "hungarian", "neapolitan", "phrygian-dominant"],
    "tech-death": ["harmonic", "diminished", "phrygian-dominant", "hungarian", "locrian", "double-harmonic"],
    "thrash": ["phrygian", "minor", "locrian", "phrygian-dominant"],
    "brostep": ["minor", "phrygian", "harmonic"],
    "blackgaze": ["major", "lydian", "dorian", "mixolydian"],
    "numetal": ["phrygian", "locrian", "minor"], "industrial": ["phrygian", "minor", "harmonic"], "dnb": ["minor", "phrygian", "dorian"],
    "darksynth": ["minor", "phrygian", "harmonic", "dorian"],
    "hardcore-kl": ["phrygian", "locrian", "minor", "diminished"],
    "tool": ["phrygian", "dorian", "locrian", "double-harmonic", "minor"],
}
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


_HAVE = {}

def have(patch):
    """Is `patch` available to the running chirp (built-ins differ by build)?"""
    if patch not in _HAVE:
        import os, subprocess
        c = os.environ.get("CHIRP_BIN") or "chirp"
        _HAVE[patch] = any(subprocess.run([c, "plan", "-p", patch, note], capture_output=True).returncode == 0 for note in ("C2/4", "k/4"))
    return _HAVE[patch]


def pick_patch(*names):
    """First available patch in order of preference."""
    return next((n for n in names if have(n)), names[-1])


# Rigs: the instrument choices every generator uses, with fallbacks for builds that lack a
# patch. Import this module from other composition scripts and reuse the same sound:
#     sys.path.insert(0, os.path.expanduser("~/.config/chirp/tools")); import compose
#     tracks = compose.rhythm_tracks("expr.pm=1 F1/16@110 …") + [compose.track("bass", compose.rig("bass"), "F1/16@110 …")]
RIGS = {
    "rhythm": (("m8-rhythm-l", "m8-rhythm-r"), ("m8-tight", "m8-tight layers.0.pick=0.14 humanize.time=5ms")),
    "bass": ("bass-fat", "bass-di", "m8-bass"),
    "sub": ("sub-sine", "sub"),
    "twang": ("m8-twang", "m8"),
    "lead": ("lead-monster", "synth-lead"),
    "drums": ("metal-kit", "prog-kit"),
    "clean": ("clean-chorus",),
    "atmos": ("ebow", "ambient-swell"),
}


# Per-song rig sets (pedalboards): a song picks one; roles fall back to RIGS.
RIG_SETS = {
    "modern": {},
    "chug": {"rhythm": (("m8-chug-l", "m8-chug-r"),), "lead": ("lead-tape", "lead-monster"), "twang": ("m8-twang-chorus", "m8-twang")},
    "fuzz": {"rhythm": (("m8-fuzz", "m8-fuzz layers.0.pick=0.1 humanize.time=9ms"),), "bass": ("bass-fuzz", "bass-fat"), "lead": ("lead-wah", "lead-monster")},
    "phase": {"rhythm": (("m8-rhythm-l", "m8-phase"),), "lead": ("lead-slap", "lead-monster"), "twang": ("m8-twang-chorus", "m8-twang")},
    "tech": {"rhythm": (("m8-chug-l", "m8-chug-r"),), "lead": ("lead-slap", "lead-monster")},
    "thrash": {"rhythm": (("m8-chug-l", "m8-chug-r"),), "bass": ("pick-bass", "bass-fat"), "lead": ("lead-wah", "lead-monster")},
    "tool-fuzz": {"bass": ("bass-fuzz", "bass-fat"), "lead": ("ebow", "lead-tape"), "clean": ("baritone", "clean-chorus")},
    "tool-pick": {"bass": ("pick-bass", "bass-fat"), "lead": ("lead-tape", "lead-monster"), "clean": ("twelve-string", "clean-chorus")},
}
_RIGSET = {}


def rig(role):
    """The first available patch for a rig role (rhythm returns a (left, right) pair), honouring
    the current song's rig set."""
    opts = tuple(_RIGSET.get(role, ())) + tuple(RIGS[role])
    if role == "rhythm":
        return next((pair for pair in opts if all(have(p.split()[0]) for p in pair)), opts[-1])
    return pick_patch(*opts)


def rhythm_tracks(score, *, pair=None, pan=90, seeds=(7, 13), fx=None):
    """A real double-tracked rhythm guitar: the same part on two rigs played by two "players"
    (own seeds, the right looser), hard-panned. `pair` overrides the (left, right) rigs; `fx`
    adds per-part inserts after the rigs (a phaser, chorus or stutter gate for this section)."""
    left, right = pair or rig("rhythm")
    extra = {"fx": fx} if fx else {}
    return [track("gtr-l", left, score, pan=f"L{pan}", seed=seeds[0], **extra), track("gtr-r", right, score, pan=f"R{pan}", seed=seeds[1], **extra)]


# Section inserts for variety (post-rig): picked per part.
SECTION_FX = {
    "space": [None, None, ["rack:phaser-slow"], ["rack:chorus-wide"], ["rack:shimmer-hall"]],
    "break": [None, None, None, ["rack:stutter-16"], ["rack:dub-throw"]],
}


def section_fx(r, kind):
    choice = r.choice(SECTION_FX.get(kind, [None]))
    return expand(choice) if choice else None


def mname(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


class Key:
    def __init__(self, pc, mode):
        self.pc, self.mode = pc, mode
        self.iv = MODES[mode]

    def deg(self, d, base):
        """Scale degree d (0-based, any integer) above tonic in the octave starting at MIDI `base`."""
        t = base + (self.pc - base) % 12
        n = len(self.iv)
        return t + 12 * (d // n) + self.iv[d % n]

    def chord(self, root, base, n=3):
        return [self.deg(root + 2 * i, base) for i in range(n)]

    def nearest_scale(self, m):
        """Snap MIDI m to the nearest scale tone."""
        for off in [0, -1, 1, -2, 2]:
            if (m + off - self.pc) % 12 in self.iv:
                return m + off
        return m


def track(name, patch, score, **kw):
    t = {"name": name, "patch": patch, "score": score}
    t.update(kw)
    return t


LENGTHS = {}  # part name → length in beats (parts default to 16)

# ---------- racks: named, composable effect chains (~/.config/chirp/racks/NAME.yaml) ------
import os as _os
RACKS_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "racks")


def rack(name, _depth=0):
    """The effect list of rack NAME with nested `rack:OTHER` entries expanded."""
    if _depth > 8:
        raise ValueError(f"rack nesting too deep at {name}")
    data = json.load(open(_os.path.join(RACKS_DIR, f"{name}.yaml")))
    return expand(data["fx"], _depth + 1)


def expand(fx, _depth=0):
    """Expand `rack:NAME` references in an effect list (effects and strings pass through)."""
    out = []
    for e in fx or []:
        if isinstance(e, str) and e.startswith("rack:"):
            out += rack(e[5:].strip(), _depth)
        else:
            out.append(e)
    return out


def racks():
    return sorted(f[:-5] for f in _os.listdir(RACKS_DIR) if f.endswith(".yaml"))


# ---------- time-varying effects (modulation, automation, sidechain) ----------------------

def _add(t, fx=(), auto=None, lfo=None, **kw):
    t = dict(t)
    if fx:
        t["fx"] = list(t.get("fx", [])) + list(fx)
    if auto:
        t["auto"] = dict(t.get("auto", {}), **auto)
    if lfo:
        t["lfo"] = dict(t.get("lfo", {}), **lfo)
    t.update(kw)
    return t


def duck_low(tracks):
    """Sidechain: the sub, reese and bass duck under the part's kick (tighter, punchier lows)."""
    if not any(t["name"] == "kick" for t in tracks):
        return tracks
    depth = {"sub": "-8dB", "reese": "-6dB", "bass": "-3dB", "bassA": "-5dB", "bassB": "-5dB"}
    return [_add(t, fx=[{"type": "duck", "by": "kick", "depth": depth[t["name"]], "attack": "2ms", "release": "90ms"}])
            if t["name"] in depth else t for t in tracks]


def sweep_build(tracks, beats=16):
    """A build: the guitars' low-pass opens across the part and their level swells."""
    pts = [["0b", 0.12], [f"{beats * 0.75:g}b", 0.7], [f"{beats:g}b", 1.0]]
    out = []
    for t in tracks:
        if t["name"] in ("gtr-l", "gtr-r", "gtr", "twang"):
            t = _add(t, fx=[{"type": "filter", "kind": "lp", "cutoff": {"value": 350, "mod": [{"src": "auto.open", "amount": 5.6}]}}],
                     auto={"open": {"points": pts}, "swell": {"points": pts}},
                     gain={"value": "-6dB", "mod": [{"src": "auto.swell", "amount": 6}]})
        out.append(t)
    return out


def delay_throw(tracks, names, beats=16):
    """Dub-style throw: a feedback delay's mix spikes over the last beat and a half, so the final
    hits echo into the next section."""
    pts = [["0b", 0], [f"{beats - 2:g}b", 0], [f"{beats - 1:g}b", 1], [f"{beats:g}b", 0.3]]
    return [_add(t, fx=[{"type": "delay", "time": "3/16", "feedback": 0.5, "ping_pong": True, "tone": 3000,
                         "mix": {"value": 0, "mod": [{"src": "auto.throw", "amount": 0.45}]}}],
                 auto={"throw": {"points": pts}}) if t["name"] in names else t for t in tracks]


def auto_pan(tracks, names, rate="1/1", depth=0.6):
    return [_add(t, lfo={"pan": {"wave": "sine", "rate": rate}}, pan={"value": 0, "mod": [{"src": "lfo.pan", "amount": depth}]})
            if t["name"] in names else t for t in tracks]


def enhance(role, tracks, beats):
    """Per-role time-varying effects applied to every generated part."""
    tracks = duck_low(tracks)
    if role in ("riffSoft", "riffUp"):
        tracks = sweep_build(tracks, beats)
    if role == "riffX":
        tracks = auto_pan(delay_throw(tracks, ("twang",), beats), ("twang",))
    if role == "riffBrk":
        tracks = delay_throw(tracks, ("gtr-l", "gtr-r"), beats)
    return tracks


DRUM_BUS = ["rack:drum-bus-punch", {"type": "eq", "bands": ["highshelf cutoff=8000 gain=2dB"]}]  # QA: keep cymbal air
FLAVOR_DRUMS = {"vintage": ["rack:spring-surf"], "industrial": [{"type": "drive", "shape": "crush", "bits": 10, "downsample": 2, "drive": 0.35, "mix": 0.25}]}
_FLAVOR = {"name": "modern"}


def drum_bus(tracks):
    """Route metal-kit tracks through one shared drums bus (glued, and processed once per part):
    the tracks switch to metal-kit-dry and `out: drums`; returns (tracks, buses)."""
    if not have("metal-kit-dry") or not any(t.get("patch") == "metal-kit" for t in tracks):
        return tracks, {}
    out = [dict(t, patch="metal-kit-dry", out="drums") if t.get("patch") == "metal-kit" else t for t in tracks]
    return out, {"drums": {"fx": expand(DRUM_BUS + FLAVOR_DRUMS.get(_FLAVOR["name"], []))}}


def write(name, about, tracks, beats=16):
    LENGTHS[name] = beats
    tracks = enhance(name.rsplit("-", 1)[-1], tracks, beats)
    tracks, buses = drum_bus(tracks)
    b = f"{beats:g}b"
    lines = [f"about: {json.dumps(f'Generated part (tempo: inherit, {beats:g} beats) — ' + about)}", "tempo: inherit", f"length: {b}"]
    if buses:
        lines.append("buses: " + json.dumps(buses))
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(f"{SONGS}/{name}.yaml", "w").write("\n".join(lines) + "\n")


def chordhead(ms):
    return ",".join(mname(m) for m in ms)


# ---------- generators -----------------------------------------------------------------

def gen_djent(r, k, prog, low, breakdown=False):
    """16th chugs on the low tonic in a per-song rhythm cell; power-chord accents on chord roots."""
    cell = [r.random() < (0.35 if breakdown else 0.62) for _ in range(16)]
    cell[0] = True
    acc = {i for i in range(16) if cell[i] and r.random() < 0.28}
    acc.add(r.choice([i for i in range(16) if cell[i]]))
    gtr, bass = [], []
    t0 = k.deg(0, low)
    for bar, root in enumerate(prog):
        rt = k.deg(root, low)
        if rt - t0 > 7:
            rt -= 12
        for i in range(16):
            last = bar == 3 and i >= 14
            if breakdown and i % 2 == 1 and i not in acc:
                gtr.append("R/16"); bass.append("R/16"); continue
            if not cell[i]:
                if r.random() < 0.3:
                    gtr.append(f"expr.pm=1 {mname(t0)}/16@64^dead"); bass.append("R/16")
                else:
                    gtr.append("R/16"); bass.append("R/16")
                continue
            if i in acc or last:
                pc = [rt, rt + 7, rt + 12]
                stab = k.deg(1, low) if r.random() < 0.2 else None
                if stab and i not in (0,):
                    pc = [stab, stab + 7]
                v = 120 + r.randint(0, 6)
                art = "^ph^gate=1.6" if last and i == 15 else "^gate=0.95"
                choice = f"({chordhead(pc)}|{chordhead([rt, rt + 7])})" if r.random() < 0.3 else chordhead(pc)
                gtr.append(f"expr.pm=0 {choice}/16@{v}{art}"); bass.append(f"{mname(pc[0])}/16@{v}")
            else:
                v = r.choice([96, 104, 110, 116])
                note = mname(t0 if r.random() < 0.85 else rt)
                gtr.append(f"expr.pm=1 {note}/16@{v}"); bass.append(f"{note}/16@{v}")
    g = " ".join(gtr)
    b = " ".join(bass)
    # Drums locked to the riff: kick under every chug/accent, backbeat (2 & 4, or 3 for
    # breakdowns) from rimshot/centre/off-centre with ghosts, ride tip/shank quarters, crash or
    # china on bar 1, china/stack/choked crash on accents.
    kick, snare, cym = [], [], []
    for i, tok in enumerate(gtr):
        hit = not tok.startswith("R") and "^dead" not in tok
        accent = "expr.pm=0" in tok
        beat, sub = divmod(i % 16, 4)
        kick.append(f"k/16@{118 if accent else 104}" if hit else "R/16")
        back = (beat == 2) if breakdown else (beat in (1, 3))
        if sub == 0 and back:
            snare.append(f"{r.choice(['s', 's', 'sc', 'so'])}/16@118" + ("^flam" if r.random() < 0.15 else ""))
        else:
            snare.append(f"g/16@{r.choice([30, 38])}" if r.random() < 0.12 else "R/16")
        if i % 16 == 0:
            cym.append(f"{r.choice(['c', 'x', 'cbl'])}/16@114")
        elif accent and r.random() < 0.5:
            cym.append(f"{r.choice(['x', 'st', 'cch'])}/16@108")
        elif sub == 0:
            cym.append(f"{'rds' if beat % 2 else 'rd'}/16@{88 if beat % 2 else 80}")
        else:
            cym.append("R/16")
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    return rhythm_tracks(g) + [track("bass", rig("bass"), b, seed=7), track("sub", rig("sub"), b, seed=7),
            track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


def gen_taps(r, k, prog, base):
    shape = r.choice(["up", "updown", "skip"])
    out = []
    for root in prog:
        tones = [k.deg(root + 2 * i, base) for i in range(6)]  # two-octave arpeggio of thirds
        seq = {"up": tones[:4] + tones[1:5] + tones[2:6] + tones[1:5], "updown": tones[:5] + tones[4:0:-1] + tones[:5] + tones[4:1:-1],
               "skip": [tones[i] for i in [0, 2, 1, 3, 2, 4, 3, 5, 4, 2, 3, 1, 2, 0, 1, 3]]}[shape][:16]
        for i, m in enumerate(seq):
            ham = "^h" if i % 4 else ""
            v = 100 if i % 4 == 0 else r.choice([80, 84, 90])
            out.append(f"({mname(m)}|{mname(m + 12) if i % 8 == 7 else mname(m)})/16@{v}{ham}" if i % 8 == 7 else f"{mname(m)}/16@{v}{ham}")
    return [track("taps", "clean-chorus", " ".join(out), pan=0.15)]


def gen_acid(r, k, prog, base):
    out = []
    for root in prog:
        rt = k.deg(root, base)
        for i in range(16):
            x = r.random()
            if x < 0.15:
                m = rt + 12
            elif x < 0.3:
                m = k.nearest_scale(rt + r.choice([3, 5, 7, 10, 1]))
            else:
                m = rt
            v = 118 if (i % 4 == 0 or r.random() < 0.25) else 72
            out.append(f"{mname(m)}/16@{v}" if r.random() > 0.08 else "R/16")
    return [track("acid", "acid", " ".join(out))]


def gen_bassline(r, k, prog, base, patch="bass"):
    pat = r.choice([["R", "x", "R", "x"], ["x", "R", "x", "x"], ["R", "x", "x", "R"]])
    out = []
    for root in prog:
        rt = k.deg(root, base)
        for beat in range(4):
            for j, p in enumerate(pat):
                if p == "R":
                    out.append("R/16")
                else:
                    m = rt + (12 if (beat == 3 and j == 3) else 0)
                    if r.random() < 0.15:
                        m = k.nearest_scale(rt + 7)
                    out.append(f"{mname(m)}/16@{r.choice([96, 100, 106])}")
    return [track("bass", patch, " ".join(out), gain="-4dB")]


def gen_808(r, k, prog, base, patch="808"):
    out = []
    for root in prog:
        rt = k.deg(root, base)
        out.append(f"{mname(rt)}/4.@110 {mname(rt)}/8@100 R/4 ({mname(k.deg(root + 2, base))}|{mname(rt + 12)})/8@104 {mname(rt)}/8@100")
    return [track("sub808", patch, " ".join(out))]


def gen_stabs(r, k, prog, base, patch):
    rhythm = r.choice(["R/8 X/8 R/4 R/8 X/8 R/4", "X/8. X/16 R/4 R/8 X/8 R/4", "R/8 X/8 R/8 X/8 R/4 X/4"])
    out = []
    for root in prog:
        ch = chordhead(k.chord(root, base, 4))
        out.append(rhythm.replace("X", ch).replace(f"{ch}/8", f"{ch}/8@{r.choice([92, 100])}"))
    return [track("stabs", patch, " ".join(out), pan=0.15)]


def gen_chops(r, k, prog, base):
    out = []
    for root in prog:
        ch = chordhead(k.chord(root, base, 4))
        out.append(f"{ch}/16@96 {ch}@58^dead R {ch}@92 R {ch}@60^dead {ch}@90 R {ch}@96 {ch}@58^dead R {ch}@92 R {ch}@60^dead {ch}@94 ({ch}@88|R)")
    return [track("chops", "strat-quack", " ".join(out), pan=-0.35)]


def gen_comp(r, k, prog, base, patch="rhodes", swing=0.62):
    out = []
    for root in prog:
        ch = chordhead(k.chord(root, base, 4))
        top = mname(k.deg(root + 8, base))
        out.append(f"{ch}/4.@80 ({top}|R)/8@70 R/4 {ch}/4@72")
    return [track("keys", patch, f"swing={swing} " + " ".join(out))]


def gen_alberti(r, k, prog, base):
    out = []
    for root in prog:
        c = k.chord(root, base, 3)
        out.append(" ".join(f"{mname(m)}/8@{v}" for m, v in zip([c[0], c[2], c[1], c[2]] * 2, [70, 60, 64, 60] * 2)))
    return [track("lh", "piano", " ".join(out), pan=-0.15)]


def gen_hook(r, k, prog, base, patch):
    """Motif statement, repeat with altered ending, sequence onto chord 3, cadence."""
    cells = [[0.5, 0.5, 1, 2], [1, 0.5, 0.5, 1, 1], [0.75, 0.75, 0.5, 2], [0.5, 0.25, 0.25, 1, 2], [1.5, 0.5, 2], [0.5, 0.5, 0.5, 0.5, 2]]
    rhythm = r.choice(cells)
    lead_in = r.random() < 0.5
    steps = [0] + [r.choice([-2, -1, 1, 1, 2, 3, -3]) for _ in rhythm[1:]]

    def phrase(root, alt_end=False, inv=False):
        d = root + r.choice([0, 2, 4])
        out = []
        for i, (ln, st) in enumerate(zip(rhythm, steps)):
            d += -st if inv else st
            if i == len(rhythm) - 1:
                d = root + (r.choice([2, 4]) if alt_end else r.choice([0, 4]))
            m = k.deg(d, base)
            v = 108 if i == 0 or ln >= 1 else 96
            out.append(f"{mname(m)}/{fmt(ln)}@{v}")
        return out

    def fmt(ln):
        return {0.25: "16", 0.5: "8", 0.75: "8.", 1: "4", 1.5: "4.", 2: "2", 3: "2.", 4: "1"}[ln]

    bars = [phrase(prog[0]), phrase(prog[1], alt_end=True), phrase(prog[2], inv=r.random() < 0.4)]
    cad_root = prog[3]
    cad = [f"{mname(k.deg(cad_root + 4, base))}/4@100", f"{mname(k.deg(cad_root + 2, base))}/4@96", f"{mname(k.deg(0 if r.random() < 0.6 else 4, base))}/2@110^gate=1.2"]
    body = bars[0] + bars[1] + bars[2] + cad
    if lead_in:  # rest an eighth and shorten the cadence to keep 16 beats
        body = ["R/8"] + body[:-1] + [body[-1].replace("/2@", "/4.@")]
    return [track("hook", patch, " ".join(body), pan=0.1)]


def gen_pad(r, k, prog, base, patch, gain="-4dB", vel=80):
    out = [f"{chordhead(k.chord(root, base, 4))}/1@{vel}" for root in prog]
    return [track("pad", patch, " ".join(out), gain=gain)]


def gen_arp(r, k, prog, base, patch):
    shape = r.choice([[0, 2, 4, 7], [0, 4, 2, 4], [0, 2, 4, 2], [0, 4, 7, 9]])
    out = []
    for root in prog:
        for rep in range(4):
            out += [f"{mname(k.deg(root + s, base))}/16@{v}" for s, v in zip(shape, [100, 88, 94, 86])]
    return [track("arp", patch, " ".join(out), pan=0.3)]


def gen_hold(r, k, prog, low, gp):
    out, bass = [], []
    for root in prog:
        rt = k.deg(root, low)
        if rt - k.deg(0, low) > 7:
            rt -= 12
        out.append(f"{chordhead([rt, rt + 7, rt + 12])}/1@{r.choice([120, 124])}^gate=1")
        bass.append(f"{mname(rt)}/1@120")
    return rhythm_tracks("expr.pm=0 " + " ".join(out)) + [track("bass", rig("bass"), " ".join(bass)), track("sub", rig("sub"), " ".join(bass))]


def gen_meshuggah(r, k, low, gp, cycle, grid="16", mode="riff"):
    """Polymetric riff: a cycle of `cycle` steps repeated over a steady 4/4 pulse (reset at the
    phrase). Chugs on the low tonic (sometimes ♭2), b2-cluster / tritone / ♭5 / ♭9 accents, dead
    notes and gaps. Drums lock to it: kick on every hit, half-time snare on 3, ride/hats on
    quarters, china on each cycle restart, a tom fill to end the phrase."""
    steps = {"16": 64, "12": 48, "8": 32}[grid]
    per_beat = {"16": 4, "12": 3, "8": 2}[grid]
    t = k.deg(0, low)
    evil = [[t, t + 1], [t, t + 1, t + 12], [t, t + 6], [t + 6, t + 12], [t + 6, t + 13], [t, t + 13], [t + 12, t + 13, t + 18],
            [t, t + 11], [t + 12, t + 15, t + 18]]  # clusters, tritones, maj7, diminished
    power = [[t, t + 7, t + 12], [t + 1, t + 8, t + 13], [t + 6, t + 13, t + 18], [t + 3, t + 10, t + 15], [t, t + 7]]
    pick_acc = lambda: r.choice(power) if r.random() < 0.6 else r.choice(evil)
    # Build one cycle from cells: chug runs, gaps, accents, dead notes.
    cyc = [("acc", pick_acc())]
    while len(cyc) < cycle:
        x = r.random()
        if x < 0.42:
            for _ in range(r.choice([1, 2, 2, 3])):
                cyc.append(("chug", t if r.random() < 0.85 else t + 1))
        elif x < 0.58:
            cyc.append(("rest", None))
        elif x < 0.8:
            if r.random() < 0.3:  # choked stab into a full-band stop
                cyc.append(("stab", pick_acc()))
                cyc += [("stop", None)] * r.choice([1, 2])
            else:
                cyc.append(("acc", pick_acc()))
        elif x < 0.9:
            cyc.append(("mute", r.choice(power)))  # muted chord scratch
        else:
            cyc.append(("dead", t))
    cyc = cyc[:cycle]
    gtr, bass, kick, snare, cym = [], [], [], [], []
    ring = mode == "break"
    run = 0
    for i in range(steps):
        kind, pc = cyc[i % cycle]
        restart = i % cycle == 0
        dur = f"/{grid}"
        bar_off = [-6, -2, 0, 4][min(3, i * 4 // steps)]  # each phrase builds
        run = run + 1 if kind == "chug" else 0
        if kind == "stab":
            v = min(127, 122 + bar_off)
            gtr.append(f"expr.pm=0 {chordhead(pc)}{dur}@{v}^gate=0.35"); bass.append(f"{mname(pc[0])}{dur}@{v}^gate=0.35")
            kick.append(f"k{dur}@{v}")
        elif kind == "stop":
            gtr.append(f"R{dur}"); bass.append(f"R{dur}"); kick.append(f"R{dur}")
        elif kind == "mute":
            gtr.append(f"expr.pm=0 {chordhead(pc)}{dur}@{r.choice([64, 72, 80])}^dead"); bass.append(f"R{dur}"); kick.append(f"R{dur}")
        elif kind == "acc":
            v = min(127, (126 if restart else r.choice([110, 116, 120])) + bar_off)
            art = "^gate=1.6" if ring else "^gate=0.9"
            x = r.random()
            if x < 0.12:
                art = "^ph^gate=1.4"          # pinch squeal
            elif x < 0.2 and not ring:
                art = "^r=4^gate=1"           # tremolo-picked stab
            gtr.append(f"expr.pm=0 {chordhead(pc)}{dur}@{v}{art}"); bass.append(f"{mname(pc[0])}{dur}@{v}")
            kick.append(f"k,ft{dur}@{v}" if mode == "toms" else f"k{dur}@{v}")
        elif kind == "chug":
            v = max(70, min(124, [112, 98, 106, 92][min(run - 1, 3)] + r.randint(-6, 6) + bar_off))  # runs swell and decay
            mg = "^r=2" if r.random() < 0.08 else ""  # machine-gun double chug
            gtr.append(f"expr.pm=1 {mname(pc)}{dur}@{v}{mg}"); bass.append(f"{mname(pc)}{dur}@{v}")
            # Tom grooves: chug runs walk down the toms (high → floor) instead of the kick.
            kick.append(f"{['t1', 't2', 't3', 'ft'][min(run - 1, 3)]}{dur}@{v}" if mode == "toms" else f"k{dur}@{v - 6}")
        elif kind == "dead":
            gtr.append(f"expr.pm=1 {mname(pc)}{dur}@62^dead"); bass.append(f"R{dur}"); kick.append(f"R{dur}")
        else:
            gtr.append(f"R{dur}"); bass.append(f"R{dur}"); kick.append(f"R{dur}")
        beat_pos, beat = i % per_beat, i // per_beat
        backbeat = r.choice(["s", "s", "s", "sc", "so"]) if beat_pos == 0 and beat % 4 == 2 else None
        snare.append((f"{backbeat}{dur}@118" + ("^flam" if r.random() < 0.2 else "")) if backbeat else
                     (f"g{dur}@{r.choice([30, 36, 42])}" if r.random() < 0.16 else (f"rc{dur}@70" if r.random() < 0.03 else f"R{dur}")))
        if kind == "stop":
            cym.append(f"R{dur}")
        elif beat_pos == 0:
            if restart:
                piece = r.choice(["x", "x", "rbs", "cbl"])
            elif mode == "toms":
                piece = "rb"                                  # Meshuggah bell on the quarters
            elif mode == "shuffle":
                piece = r.choice(["h1", "hs", "h", "h2"])     # hats at varying openings
            else:
                piece = "rds" if beat % 2 == 1 else "rd"      # ride tip / shank
            cym.append(f"{piece}{dur}@{(118 if restart else r.choice([84, 90, 96])) + bar_off}")
        else:
            cym.append(f"x{dur}@104" if restart else f"R{dur}")
    # Tom fill over the last beat.
    fill = ["t1", "t2", "t3", "ft"][:per_beat] if per_beat <= 4 else ["t1", "t2", "t3", "ft"]
    for j, piece in enumerate(fill):
        snare[steps - per_beat + j] = f"{piece}/{grid}@{110 + 2 * j}"
    if mode == "break":  # Garstka-style drums on a finer grid around the ringing hits
        scale = 64 // steps
        hit_steps = [i * scale for i in range(steps) if cyc[i % cycle][0] in ("acc", "stab")]
        restarts = [i * scale for i in range(0, steps, cycle)]
        k16, s16, c16 = garstka(r, hit_steps, 64, restarts)
        kit = rig("drums")
        return rhythm_tracks(" ".join(gtr), fx=section_fx(r, "break")) + [track("bass", rig("bass"), " ".join(bass), seed=7), track("sub", rig("sub"), " ".join(bass), seed=7),
                track("kick", kit, k16), track("snare", kit, s16), track("cym", kit, c16)] + (
                [track("reese", "reese", " ".join(f"{mname(pc[0] + 12)}/{grid}@100^gate=2" if kind == "acc" else f"R/{grid}" for kind, pc in (cyc[i % cycle] for i in range(steps))), gain="-8dB")]
                if have("reese") else [])
    j = lambda xs: " ".join(xs)
    kit = rig("drums")
    return rhythm_tracks(j(gtr)) + [track("bass", rig("bass"), j(bass), seed=7), track("sub", rig("sub"), j(bass), seed=7),
            track("kick", kit, j(kick)), track("snare", kit, j(snare)), track("cym", kit, j(cym))] + (
            [track("reese", "reese", j(f"{mname(pc[0] + 12)}{dur}@{100}^gate=2" if kind == "acc" else f"R{dur}" for kind, pc in (cyc[i % cycle] for i in range(steps))), gain="-8dB")]
            if mode == "break" and have("reese") else [])


def gen_space(r, k, low, gp, cycle):
    """Space for the twangs: big open hits (low tonic, b2, tritone) ring out on m8-twang with
    gaps after them for the amp, delay and hall to play out; short tight chug bursts between.
    Slow eighth grid; kick + crash/china on hits, half-time snare on 3, soft hats in the gaps."""
    steps, dur = 32, "/8"
    t = k.deg(0, low)
    hits = [[t], [t, t + 7], [t, t + 1], [t, t + 6], [t + 1, t + 7], [t, t + 11]]
    cyc = []
    while len(cyc) < cycle:
        cyc.append(("ring", r.choice(hits), r.choice([3, 3.5, 4])))
        cyc += [("rest",)] * r.choice([2, 3, 4])
        if r.random() < 0.5:
            cyc += [("chug",)] * r.choice([1, 2, 3])
    cyc = cyc[:cycle]
    gtr, twang, bass, kick, snare, cym = [], [], [], [], [], []
    dives = []
    for i in range(steps):
        ev = cyc[i % cycle]
        beat = i // 2
        if ev[0] == "ring":
            v = 120 + r.randint(0, 6)
            x = r.random()
            if x < 0.25 and i + 3 < steps and all(cyc[(i + d) % cycle][0] == "rest" for d in (1, 2, 3)):
                dives.append(i)               # whammy dive: hold and bend down over the gap
                twang.append(f"{mname(ev[1][0])}{dur}@{v}")
            elif x < 0.42:
                twang.append(f"{mname(ev[1][0] + 12)}{dur}@{v}^nh={r.choice([2, 3])}^gate={ev[2]}")  # natural harmonic
            elif x < 0.55:
                twang.append(f"{chordhead(ev[1])}{dur}@{v}^ph^gate={ev[2]}")  # pinch squeal
            else:
                twang.append(f"{chordhead(ev[1])}{dur}@{v}^gate={ev[2]}")
            gtr.append(f"R{dur}")
            bass.append(f"{mname(ev[1][0])}{dur}@{v}^gate={ev[2]}"); kick.append(f"k{dur}@{v}")
            cym.append(f"{r.choice(['c', 'x', 'cbl', 'rde'])}{dur}@{v - 6}")
        else:
            twang.append(f"R{dur}")
            if ev[0] == "chug":
                v = r.choice([100, 108, 114])
                gtr.append(f"expr.pm=1 {mname(t)}{dur}@{v}"); bass.append(f"{mname(t)}{dur}@{v - 8}"); kick.append(f"k{dur}@{v - 8}")
            else:
                gtr.append(f"R{dur}"); bass.append(f"R{dur}"); kick.append(f"R{dur}")
            cym.append(f"{r.choice(['hf', 'h1', 'hf'])}{dur}@{r.choice([60, 70])}" if i % 2 == 0 else f"R{dur}")
        snare.append(f"s{dur}@116" if i % 8 == 4 else (f"g{dur}@{r.choice([30, 38])}" if r.random() < 0.14 else f"R{dur}"))
    for i in dives:  # turn the rests after a dive note into held, bending steps
        for d, b in zip((1, 2, 3), (-1, -4, -9)):
            twang[i + d] = f"bend={b} _"
        if i + 4 < steps:
            twang[i + 4] = "bend= " + twang[i + 4]
        else:
            twang[i + 3] += " bend="
    j = lambda xs: " ".join(xs)
    kit = rig("drums")
    return rhythm_tracks(j(gtr), fx=section_fx(r, "space")) + [track("twang", rig("twang"), j(twang)), track("bass", rig("bass"), j(bass), seed=7),
            track("sub", rig("sub"), j(bass), seed=7), track("kick", kit, j(kick)), track("snare", kit, j(snare)), track("cym", kit, j(cym))]


def gen_drone(k, base, patch):
    return [track("drone", patch, f"{mname(k.deg(0, base))},{mname(k.deg(0, base) + 7)}/1@84 _ _ _", gain="-6dB")]


def soften(tracks, scale=0.78):
    """The same part played softer: every explicit velocity scaled (timbre follows velocity)."""
    f = lambda m: "@" + str(max(30, int(int(m.group(1)) * scale)))
    return [dict(t, score=re.sub(r"@(\d+)", f, t["score"])) for t in tracks]


def garstka(r, hits, steps=64, restarts=()):
    """Breakdown drums on a 16th grid around ringing hits (step indices): kick + china/crash on
    every hit; each gap filled with a double-kick roll (with 32nd bursts), a linear tom run, or
    stack/splash accents on the off-16ths against the kick; snare on 3 (flams) with ghosts."""
    kick, snare, cym = ["R"] * steps, ["R"] * steps, ["R"] * steps
    hs = sorted(set(h for h in hits if 0 <= h < steps)) or [0]
    for h in hs:
        kick[h] = f"k@{r.choice([120, 124])}"
        cym[h] = f"{'x' if h in restarts else r.choice(['x', 'c', 'cbl', 'st', 'cch'])}@{r.choice([112, 118])}"
    bounds = hs + [steps]
    for a, b in zip(bounds, bounds[1:]):
        gap = list(range(a + 1, b))
        if len(gap) < 2:
            continue
        idea = r.choice(["roll", "roll", "toms", "accents"])
        if idea == "roll":
            start = r.choice([0, len(gap) // 3, len(gap) // 2])
            for n, i in enumerate(gap[start:]):
                v = min(124, 88 + 4 * n)
                kick[i] = f"k@{v}" + ("^r=2" if r.random() < 0.25 else "")
        elif idea == "toms":
            seq = r.choice([["t1", "t1", "t2", "t2", "t3", "t3", "ft", "ft"], ["t1", "t2", "t3", "ft"], ["ft", "t3", "t2", "t1", "t2", "t3"]])
            for n, i in enumerate(gap[-min(len(gap), len(seq)):]):
                snare[i] = f"{seq[n % len(seq)]}@{100 + 3 * n}"
                if n % 2 == 1:
                    kick[i] = "k@96"
        else:
            for i in gap:
                if i % 4 in (1, 3) and r.random() < 0.55:
                    cym[i] = f"{r.choice(['st', 'sp', 'st', 'x', 'cch', 'rbs'])}@{r.choice([96, 104, 110])}"
                if i % 4 == 0:
                    kick[i] = "k@104"
    for i in range(steps):
        if i % 16 == 8 and snare[i] == "R":
            snare[i] = "s@118" + ("^flam" if r.random() < 0.3 else "")
        elif snare[i] == "R" and kick[i] == "R" and r.random() < 0.18:
            snare[i] = f"g@{r.choice([30, 36, 42])}"
        if cym[i] == "R" and i % 4 == 0 and r.random() < 0.5:
            cym[i] = f"{r.choice(['rb', 'rb', 'rbs'])}@70"
        elif cym[i] == "R" and i % 4 == 2 and r.random() < 0.15:
            cym[i] = "h2@64"
    f = lambda xs: " ".join(x.replace("@", "/16@", 1) if x != "R" else "R/16" for x in xs)
    return f(kick), f(snare), f(cym)


def gen_blast(r, k, prog, low, kind="trad"):
    """Tech-death: tremolo-picked 16th runs sequenced through the progression with power-chord
    stabs at bar starts, over blast beats (trad: kick/snare alternate 16ths; hammer: unison 8ths;
    bomb: kick 16ths + snare 8ths; dbeat: palm-muted chugs over a d-beat), tom fill at the end."""
    steps = 64
    cells = [[0, 1, 0, 2], [0, -1, 1, 0], [0, 2, 3, 1], [0, 1, 2, 1], [3, 2, 1, 0]]
    cell = r.choice(cells)
    seqs = r.choice([[0, 1, 2, 1], [0, 0, 1, 1], [0, 2, 1, 3], [0, -1, 0, 1]])
    gtr, bass = [], []
    for bar, root in enumerate(prog):
        rt = k.deg(root, low + 12)
        for beat in range(4):
            for j in range(4):
                i = bar * 16 + beat * 4 + j
                if beat == 0 and j == 0:
                    pc = [rt - 12, rt - 5, rt]
                    gtr.append(f"expr.pm=0 {chordhead(pc)}/16@124^gate=0.9"); bass.append(f"{mname(rt - 12)}/16@120")
                    continue
                if kind == "dbeat":
                    v = 112 if j % 2 == 0 else 96
                    gtr.append(f"expr.pm=1 {mname(rt - 12)}/16@{v}" if r.random() < 0.85 else f"expr.pm=0 {chordhead([rt - 12, rt - 5])}/16@118")
                else:
                    m = k.deg(root + cell[j] + seqs[beat], low + 12)
                    art = "^ph" if (beat == 3 and j == 3 and r.random() < 0.4) else ("^h" if j % 2 == 1 and r.random() < 0.15 else "")
                    gtr.append(f"expr.pm=0 {mname(m)}/16@{108 if j % 2 == 0 else 94}{art}")
                bass.append(f"{mname(rt - 12)}/16@{100 if j % 2 == 0 else 88}")
    kick, snare, cym = [], [], []
    for i in range(steps):
        beat, sub = i // 4, i % 4
        if kind == "trad":
            kick.append("k/16@110" if i % 2 == 0 else "R/16"); snare.append("s/16@100" if i % 2 else "R/16")
        elif kind == "hammer":
            kick.append("k/16@112" if i % 2 == 0 else "R/16"); snare.append("s/16@108" if i % 2 == 0 else "R/16")
        elif kind == "bomb":
            kick.append(f"k/16@{108 if i % 2 == 0 else 98}"); snare.append("s/16@104" if i % 2 == 0 else "R/16")
        else:  # d-beat: k . s . k k s .
            pat = {0: "k", 4: "s", 8: "k", 10: "k", 12: "s"}
            x = pat.get(i % 16)
            kick.append("k/16@114" if x == "k" else "R/16"); snare.append("s/16@110" if x == "s" else "R/16")
        cym.append(("x/16@112" if i % 16 == 0 else f"{'rb' if sub == 0 else 'rd'}/16@{90 if sub == 0 else 80}") if i % 2 == 0 else "R/16")
    for n, i in enumerate(range(steps - 8, steps)):  # tom fill
        snare[i] = f"{['t1', 't1', 't2', 't2', 't3', 't3', 'ft', 'ft'][n]}/16@{104 + 2 * n}"
        kick[i] = "k/16@100" if n % 2 == 0 else "R/16"
        cym[i] = "R/16"
    kit = rig("drums")
    j = lambda xs: " ".join(xs)
    return rhythm_tracks(j(gtr)) + [track("bass", rig("bass"), j(bass), seed=7), track("sub", rig("sub"), j(bass), seed=7),
            track("kick", kit, j(kick)), track("snare", kit, j(snare)), track("cym", kit, j(cym))]


def gen_shred(r, k, prog, base, patch):
    """Fast lead: 16th scale runs (up/down sequences of four) through the progression, landing
    on chord tones; a long bend-held note to end."""
    out = []
    for bar, root in enumerate(prog):
        d = root + r.choice([0, 2, 4])
        for beat in range(4):
            if bar == 3 and beat >= 2:
                break
            run = r.choice([[0, 1, 2, 3], [3, 2, 1, 0], [0, 2, 1, 3], [0, 1, 0, -1]])
            for x in run:
                out.append(f"{mname(k.deg(d + x, base))}/16@{100 if x == run[0] else 90}^h")
            d += r.choice([1, 2, -1, 3])
    out.append(f"{mname(k.deg(prog[3] + 7, base))}/2@112^gate=1.2")
    return [track("hook", patch, " ".join(out), pan=0.1)]


# ---------- thrash -----------------------------------------------------------------------

def gen_thrash(r, k, prog, low=40, kind="gallop"):
    """Thrash: gallops (8th + two 16ths) with chromatic power-chord moves, 16th palm-muted pedal
    with chromatic stabs over a d-beat, skank-beat chugs, half-time ringing chords; snare roll
    into the next section."""
    t = k.deg(0, low)
    pc5 = lambda m: [m, m + 7, m + 12]
    gtr, bass, kick, snare, cym = [], [], [], [], []
    chroma = r.choice([[0, 1, 3, 1], [0, 3, 5, 6], [0, -1, -2, 1], [0, 6, 5, 1], [0, 1, 0, 6]])
    for bar in range(4):
        root = k.deg(prog[bar], low)
        if root - t > 7:
            root -= 12
        for beat in range(4):
            for j in range(4):
                i = bar * 16 + beat * 4 + j
                stab = t + chroma[beat] if kind in ("chromatic", "gallop") else root
                if kind == "gallop":
                    if beat == 3 and j == 0:
                        g = f"expr.pm=0 {chordhead(pc5(stab))}/16@122^gate=1.6"
                    elif j in (0, 2, 3):
                        g = f"expr.pm=1 {mname(t)}/16@{116 if j == 0 else 100}"
                    else:
                        g = "R/16"
                elif kind == "chromatic":
                    if j == 0 and beat % 2 == 1:
                        g = f"expr.pm=0 {chordhead(pc5(stab))}/16@120^gate=1.8"
                    else:
                        g = f"expr.pm=1 {mname(t)}/16@{110 if j % 2 == 0 else 96}"
                elif kind == "skank":
                    if j % 2 == 1:
                        g = "R/16"
                    elif beat in (0, 2) and j == 0:
                        g = f"expr.pm=0 {chordhead(pc5(root))}/16@120^gate=1.6"
                    else:
                        g = f"expr.pm=1 {mname(t)}/16@{108 if j == 0 else 98}"
                else:  # half: ringing chords
                    g = f"expr.pm=0 {chordhead(pc5(root))}/16@122^gate=4" if (beat % 2 == 0 and j == 0) else "R/16"
                gtr.append(g)
                bass.append(re.sub(r"expr\.pm=\d ", "", g).split(",")[0].split("/")[0] + "/16@" + (g.split("@")[1].split("^")[0] if "@" in g else "0") if g != "R/16" else "R/16")
                # drums
                if kind == "gallop":
                    kick.append("k/16@114" if j in (0, 2, 3) else "R/16")
                    snare.append("s/16@118" if (beat % 2 == 1 and j == 0) else ("g/16@36" if r.random() < 0.08 else "R/16"))
                elif kind == "chromatic":
                    x = {0: "k", 4: "s", 8: "k", 10: "k", 12: "s"}.get((beat * 4 + j) % 16)
                    kick.append("k/16@114" if x == "k" else "R/16"); snare.append("s/16@116" if x == "s" else "R/16")
                elif kind == "skank":
                    kick.append("k/16@112" if j == 0 else "R/16"); snare.append("s/16@114" if j == 2 else "R/16")
                else:
                    kick.append("k/16@118" if (beat == 0 and j == 0) or (beat == 2 and j == 2) else "R/16")
                    snare.append("s/16@120" if (beat == 2 and j == 0) else "R/16")
                if j == 0 and beat == 0:
                    cym.append(f"{r.choice(['c', 'c', 'cbl'])}/16@110")
                elif j == 0:
                    cym.append({"skank": "h2/16@92", "chromatic": "oh/16@96", "gallop": f"{'rds' if beat % 2 else 'rd'}/16@92"}.get(kind, "rd/16@92")
                               if not (kind == "gallop" and r.random() < 0.12) else "cow/16@96")
                elif kind == "skank" and j == 2:
                    cym.append("h/16@78")
                else:
                    cym.append("R/16")
    for n, i in enumerate(range(56, 64)):  # snare roll into the next section
        snare[i] = f"s/16@{96 + 3 * n}^r=2"
        cym[i] = "R/16"
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(bass), seed=7), track("sub", rig("sub"), jn(bass), seed=7),
            track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- Tool-style odd meters --------------------------------------------------------

METERS = {  # eighths per bar → groupings (all sum to the meter)
    5: [[3, 2], [2, 3]], 7: [[2, 2, 3], [3, 2, 2], [2, 3, 2]], 9: [[2, 2, 2, 3], [3, 3, 3], [2, 3, 2, 2]],
    11: [[3, 3, 3, 2], [2, 2, 3, 2, 2], [4, 4, 3]], 13: [[3, 3, 3, 4], [2, 2, 2, 3, 2, 2], [4, 3, 3, 3]],
    15: [[3, 3, 3, 3, 3], [4, 4, 4, 3]], 23: [[4, 4, 4, 4, 4, 3], [3, 3, 3, 3, 3, 3, 3, 2]],
    31: [[8, 8, 8, 7], [3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 4], [7, 7, 7, 5, 5], [4, 4, 4, 4, 4, 4, 4, 3]],
}


def reps_for(meter):
    return max(1, round(32 / meter))


def gen_tool(r, k, low, meter, groups, mode="heavy", reps=None, lead=None):
    """Odd-meter riff (Tool-style): the band plays the meter. Guitar accents each group start
    (tonic / b2 / b5 / 9 dyads moving through the groups), palm-muted pedal between; melodic bass
    doubles with fifths and octaves; drums (Carey-ish): kick and toms rotate across group starts,
    snare on chosen groups, ride 8ths accented on group starts, a ride-bell polyrhythm in 3s or 5s
    across the meter, crash at each cycle, tom cascade at the end. Modes: heavy, clean (delayed
    arpeggios, side-stick + toms), tribal (bass + toms only), poly, build (crescendo)."""
    reps = reps or reps_for(meter)
    n = meter * reps
    t = k.deg(0, low)
    moves = r.choice([[0, 1, 0, 6], [0, 6, 1, 0], [0, 2, 1, 0, 6], [0, 13, 1, 6], [0, 1, 6, 7]])
    starts = []
    pos = 0
    for g in groups:
        starts.append(pos)
        pos += g
    poly = r.choice([3, 5, 3, 4])
    snare_groups = set(r.sample(range(len(groups)), max(1, len(groups) // 3)))
    toms = r.choice([["t1", "t2", "t3", "ft"], ["ft", "t3", "t1", "t2"], ["t2", "ft", "t1", "t3"]])
    gtr, bass, kick, snare, cym = [], [], [], [], []
    for i in range(n):
        rep_i, x = divmod(i, meter)
        cres = int((i / n) * 24) - 12 if mode == "build" else 0
        gi = max(j for j, s0 in enumerate(starts) if s0 <= x)
        at_start = x == starts[gi]
        mv = moves[gi % len(moves)]
        root = t + mv
        if mode == "clean":
            chord = [k.deg(d, 52) for d in (0, 2, 4, 7, 9)]
            gtr.append(f"{mname(chord[(i + gi) % len(chord)])}/8@{(92 if at_start else 74) + cres}")
            bass.append(f"{mname(root + 12)}/8@{86}^gate=2" if at_start and gi % 2 == 0 else "R/8")
        elif mode == "tribal":
            gtr.append("R/8")
            bass.append(f"{mname(root + 12)}/8@{104 if at_start else 88}" if (at_start or r.random() < 0.4) else "R/8")
        else:
            if at_start:
                dy = [root, root + 7] if r.random() < 0.6 else [root, root + r.choice([1, 6, 13])]
                gtr.append(f"expr.pm=0 {chordhead(dy)}/8@{min(127, 118 + cres)}^gate={1.6 if mode != 'poly' else 1}")
                bass.append(f"{mname(root)}/8@{min(127, 116 + cres)}")
            else:
                v = min(127, (100 if x % 2 == 0 else 92) + cres)
                gtr.append(f"expr.pm=1 {mname(t)}/8@{v}" if r.random() < 0.8 else "R/8")
                bass.append(f"{mname(t + (7 if r.random() < 0.2 else 0))}/8@{v}")
        # drums
        if mode == "clean":
            kick.append(f"k/8@84" if x == 0 else "R/8")
            snare.append(f"ss/8@80" if at_start and gi % 2 == 1 else (f"{toms[gi % 4]}/8@70" if at_start and r.random() < 0.4 else (f"rc/8@60" if r.random() < 0.08 else "R/8")))
            cym.append(f"{'rd' if at_start else 'shk'}/8@{70 if at_start else 62}")
        else:
            if at_start:
                kick.append(f"k/8@{min(127, 116 + cres)}" if gi % 2 == 0 or mode == "tribal" else "R/8")
                snare.append((f"s/8@{min(127, 118 + cres)}" if gi in snare_groups and mode != "tribal" else f"{toms[gi % 4]}/8@{min(127, 108 + cres)}"))
            else:
                kick.append(f"k/8@{96 + cres}" if mode in ("heavy", "build") and r.random() < 0.25 else "R/8")
                snare.append(f"g/8@{r.choice([30, 38])}" if r.random() < 0.2 else (f"{toms[(gi + x) % 4]}/8@{88 + cres}" if mode == "tribal" and r.random() < 0.5 else "R/8"))
            if x == 0:
                cym.append(f"{r.choice(['c', 'cbl', 'rde'])}/8@{min(127, 116 + cres)}")
            elif i % poly == 0:
                perc = r.choice(["wb", "wbl", "cowm", "clv"]) if mode == "tribal" else r.choice(["rb", "rbs"])
                cym.append(f"{perc}/8@{min(127, 96 + cres)}")
            else:
                cym.append(f"{('rds' if at_start else 'rd') if mode != 'tribal' else ('hf' if at_start else 'h1')}/8@{(90 if at_start else 72) + cres}")
    # tom cascade over the last group
    last = groups[-1]
    for j2, i in enumerate(range(n - last, n)):
        snare[i] = f"{['t1', 't2', 't3', 'ft', 'ft'][min(j2, 4)]}/8@{104 + 3 * j2}"
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    if mode == "clean":
        out = [track("gtr", rig("clean"), jn(gtr), pan=0.2), track("bass", rig("bass"), jn(bass), seed=7)]
    elif mode == "tribal":
        out = [track("bass", rig("bass"), jn(bass), seed=7), track("sub", rig("sub"), jn(bass), seed=7)]
    else:
        out = rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(bass), seed=7), track("sub", rig("sub"), jn(bass), seed=7)]
    return out + [track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


def gen_tool_lead(r, k, prog, meter, base, patch, reps=None):
    """A long-note melodic lead (vocal-like) across the odd meter: phrases land on group starts."""
    reps = reps or reps_for(meter)
    n = meter * reps
    out, i = [], 0
    d = r.choice([0, 2, 4])
    while i < n:
        ln = min(n - i, r.choice([2, 3, 4, 6]))
        out.append(f"{mname(k.deg(d, base))}/8@{r.choice([92, 100, 108])}" + (" _" * (ln - 1)))
        d += r.choice([-2, -1, 1, 2, 0])
        i += ln
    return [track("hook", patch, " ".join(out), pan=0.1)]


def gen_atmos(r, k, prog, base, patch):
    """A slow soaring line (e-bow / swell): one or two long overlapping notes per bar on chord
    tones, legato into each other."""
    out = []
    for root in prog:
        if r.random() < 0.5:
            out.append(f"{mname(k.deg(root + r.choice([2, 4, 7]), base))}/1@{r.choice([84, 92, 100])}^gate=1.1")
        else:
            out += [f"{mname(k.deg(root + r.choice([0, 2, 4]), base))}/2@{r.choice([84, 92])}^gate=1.1",
                    f"{mname(k.deg(root + r.choice([4, 6, 7]), base))}/2@{r.choice([92, 100])}^gate=1.1"]
    return [track("hook", patch, " ".join(out), pan=-0.1)]


# ---------- brostep ------------------------------------------------------------------------

def _bro_drums(r, steps=64, kind="drop"):
    kick, snare, clap, hats, cym = [], [], [], [], []
    for i in range(steps):
        bar_i, x = divmod(i, 16)
        if kind == "build":
            # Snare roll accelerates: 8ths, 8ths, 16ths, then 32nds with 64ths on the last beat.
            div = [2, 2, 1, 1][bar_i]
            kick.append("k/16@116" if x % 4 == 0 else "R/16")
            if x % div == 0:
                rat = ("^r=4" if x >= 12 else "^r=2") if bar_i == 3 else ""
                snare.append(f"s/16@{min(124, 84 + bar_i * 10 + x)}{rat}")
            else:
                snare.append("R/16")
            clap.append("R/16"); hats.append("R/16")
            cym.append("c/16@110" if i == 0 else "R/16")
            continue
        if kind == "intro":
            kick.append("k/16@100" if x == 0 else "R/16")
            snare.append("s/16@100" if x == 8 else "R/16"); clap.append("R/16")
            hats.append(f"h/16@{60 if x % 4 == 2 else 0}" if x % 4 == 2 else "R/16")
            cym.append("R/16"); continue
        kick.append("k/16@124" if x == 0 or (x in (10, 11) and r.random() < 0.4) or (x == 6 and r.random() < 0.3) else "R/16")
        snare.append("s/16@124" if x == 8 else ("g/16@40" if r.random() < 0.06 else "R/16"))
        clap.append("cp/16@118" if x == 8 else "R/16")
        roll = "^r=2" if r.random() < 0.15 else ("^r=3" if r.random() < 0.05 else "")
        hats.append(f"h/16@{78 if x % 2 == 0 else 58}{roll}" if x % 2 == 0 or r.random() < 0.5 else ("oh/16@70" if r.random() < 0.05 else "R/16"))
        cym.append(f"{r.choice(['c', 'x'])}/16@116" if i == 0 else "R/16")
    jn = lambda xs: " ".join(xs)
    kit, perc = rig("drums"), pick_patch("trap-kit", "metal-kit")
    out = [track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]
    if any(c != "R/16" for c in clap):
        out.append(track("clap", perc, jn(clap), fx=expand(["rack:plate-short"])))
    if any(h != "R/16" for h in hats):
        out.append(track("hats", perc, jn(hats), pan=0.15))
    return out


def gen_bro_drop(r, k, prog, low=33, metal=False):
    """Brostep drop: two bass voices (growl ↔ wobble / reese ↔ 808-dist) answering in 1–3-step
    segments — tonic, octave, b2, tritone, fifth — with stutters and an end-of-phrase dive; sub on
    the roots; gap for the snare on 3; half-time drums with a clap-layered snare and rolling hats.
    metal=True doubles the rhythm with palm-muted guitars and power chords."""
    a_p = pick_patch(*r.choice([("growl", "wobble", "reese"), ("reese", "growl", "wobble")]))
    b_p = pick_patch(*r.choice([("wobble", "808-dist", "reese"), ("808-dist", "wobble", "growl")]))
    t = k.deg(0, low)
    A, B, sub, gtr = [], [], [], []
    for bar in range(4):
        root = k.deg(prog[bar], low)
        if root - t > 6:
            root -= 12
        x = 0
        voice = 0
        while x < 16:
            if x == 8:  # the snare hit gets air
                for L in (A, B, gtr):
                    L.append("R/16")
                sub.append("R/16"); x += 1; continue
            ln = min(r.choice([1, 1, 2, 2, 3]), 16 - x, (8 - x) if x < 8 else 16 - x)
            m = r.choice([root, root, root + 12, t + 1, t + 6, root + 7])
            stut = "^r=2" if ln == 1 and r.random() < 0.3 else ("^r=3" if ln == 1 and r.random() < 0.1 else "")
            dive = bar == 3 and x + ln >= 16 and ln >= 2
            tok = [f"{mname(m)}/16@{118 if x == 0 else 108}{stut}"] + (["bend=-5 _", "bend=-12 _"][:ln - 1] if dive else ["_"] * (ln - 1))
            if dive:
                tok[-1] += " bend="
            mine, other = (A, B) if voice == 0 else (B, A)
            mine.extend(tok); other.extend(["R/16"] * ln)
            sub.extend([f"{mname(root)}/16@110"] + ["_"] * (ln - 1))
            if metal:
                gtr.extend([f"expr.pm=0 {chordhead([t, t + 7, t + 12])}/16@122^gate=0.9" if ln >= 2 else f"expr.pm=1 {mname(t)}/16@112"] + ["R/16"] * (ln - 1))
            voice = 1 - voice if r.random() < 0.7 else voice
            x += ln
    jn = lambda xs: " ".join(xs)
    out = [track("bassA", a_p, jn(A), gain="-6dB"), track("bassB", b_p, jn(B), gain="-6dB"), track("sub", rig("sub"), jn(sub), seed=7, gain="-2dB")]
    if metal:
        out += rhythm_tracks(jn(gtr))
    return out + _bro_drums(r)


def gen_bro_build(r, k, prog, low=33):
    """Brostep build: four-on-the-floor kick, snare roll accelerating to 32nds/64ths, crash on 1."""
    return _bro_drums(r, kind="build")


def gen_bro_intro(r, k, prog):
    return _bro_drums(r, kind="intro") + gen_arp(r, k, prog, 60, pick_patch("pluck-lead", "arp-pluck"))


# ---------- Knocked Loose-style hardcore -----------------------------------------------------

def gen_hc(r, k, prog, low=28, kind="twostep"):
    """Metallic hardcore: two-step (8th chugs, offbeat power chords, b2 slides), d-beat (16th
    palm-muted runs, chromatic stabs), beatdown (dissonant open chords in slow 8ths: kick+floor tom
    and china/crash on hits, choked crash after, gaps; a diving pinch squeal to end), slowdown
    (beatdown on quarters), stop (hits into full-band silence)."""
    t = k.deg(0, low)
    pc5 = lambda m: [m, m + 7, m + 12]
    diss = [[t, t + 1, t + 7], [t, t + 6, t + 12], [t + 1, t + 8, t + 13], [t, t + 7, t + 13], pc5(t)]
    grid = {"twostep": 16, "dbeat": 16, "beatdown": 8, "slowdown": 4, "stop": 8}[kind]
    steps = {16: 64, 8: 32, 4: 16}[grid]
    d = f"/{grid}"
    gtr, bass, kick, snare, cym = [], [], [], [], []
    hits = set()
    if kind in ("beatdown", "slowdown", "stop"):
        pos = 0
        while pos < steps:
            hits.add(pos)
            pos += r.choice([2, 3, 3, 4, 5]) if kind != "slowdown" else r.choice([2, 3, 4])
    for i in range(steps):
        beat = i * 4 // grid  # quarter-note index
        if kind == "twostep":
            j = i % 4
            if j == 2 and r.random() < 0.6:
                g = f"expr.pm=0 {chordhead(r.choice([pc5(t), pc5(t + 1), pc5(t + 3)]))}{d}@120^gate=0.8"
            elif j in (0, 2):
                g = f"expr.pm=1 {mname(t)}{d}@{112 if j == 0 else 100}"
            else:
                g = "R/16" if r.random() < 0.6 else f"expr.pm=1 {mname(t)}{d}@92"
            gtr.append(g)
            kick.append(f"k{d}@116" if i % 8 in (0, 6) else "R" + d)
            snare.append(f"{r.choice(['s', 's', 'sc'])}{d}@118" if i % 8 == 4 else (f"g{d}@36" if r.random() < 0.1 else "R" + d))
            cym.append((f"{r.choice(['c', 'x'])}{d}@114" if i % 16 == 0 else f"{r.choice(['h2', 'rds'])}{d}@88") if i % 2 == 0 else "R" + d)
        elif kind == "dbeat":
            if i % 8 == 4 and r.random() < 0.5:
                g = f"expr.pm=0 {chordhead(pc5(t + r.choice([1, 3, 6])))}{d}@120^gate=1"
            else:
                g = f"expr.pm=1 {mname(t)}{d}@{110 if i % 2 == 0 else 96}"
            gtr.append(g)
            x = {0: "k", 4: "s", 8: "k", 10: "k", 12: "s"}.get(i % 16)
            kick.append(f"k{d}@116" if x == "k" else "R" + d); snare.append(f"s{d}@116" if x == "s" else "R" + d)
            cym.append((f"{'c' if i % 16 == 0 else 'h3'}{d}@{112 if i % 16 == 0 else 92}") if i % 4 == 0 else "R" + d)
        else:
            if i in hits:
                ch = r.choice(diss)
                last = i == max(hits)
                art = "^ph^gate=2" if last else ("^gate=0.6" if kind == "stop" else "^gate=1.8")
                gtr.append(f"expr.pm=0 {chordhead(ch)}{d}@124{art}")
                kick.append(f"k,ft{d}@124")
                cym.append(f"{r.choice(['x', 'c', 'x', 'cbl'])}{d}@120")
            else:
                choke = (i - 1) in hits and kind != "slowdown" and r.random() < 0.6
                gtr.append("R" + d)
                kick.append("R" + d)
                cym.append(f"cch{d}@100" if choke else ("R" + d if kind == "stop" else (f"rb{d}@64" if i % 2 == 0 and kind == "beatdown" else "R" + d)))
            snare.append(f"s{d}@120" if (i * 4 // grid) % 4 == 2 and i % (grid // 4 or 1) == 0 and i not in hits and kind != "stop" else "R" + d)
        bass.append(re.sub(r"expr\.pm=\d ", "", gtr[-1]).split(",")[0].split("/")[0] + d + "@" + gtr[-1].split("@")[1].split("^")[0] if not gtr[-1].startswith("R") else "R" + d)
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(bass), seed=7), track("sub", rig("sub"), jn(bass), seed=7),
            track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- blackgaze ------------------------------------------------------------------------

def _drums_of(tracks):
    return [t for t in tracks if t["name"] in ("kick", "snare", "cym", "clap", "hats")]


def gen_gaze(r, k, prog, kind="blast"):
    """Blackgaze: tremolo-picked open chords (triad + 9th, mid register) through a shimmer hall
    over blasts (kind=blast), or ringing 8th-note chords over half-time drums with toms and ride
    wash (kind=half); clean arpeggios (kind=clean)."""
    base = 52
    chords = [[k.deg(root + d, base) for d in (0, 2, 4, 8)] for root in prog]
    if kind == "clean":
        out = []
        for ch in chords:
            for rep_ in range(2):
                out += [f"{mname(ch[i])}/8@{88 if i == 0 else 74}" for i in (0, 2, 1, 3)]
        return [track("gtr", rig("clean"), " ".join(out), pan=0.2, fx=expand(["rack:shimmer-hall"]))] + _drums_of(gen_tool(r, k, 28, 8, [3, 3, 2], "clean", reps=4))
    gtr = []
    for ch in chords:
        for i in range(16 if kind == "blast" else 8):
            v = (104 if i % 2 == 0 else 92) if kind == "blast" else (112 if i % 4 == 0 else 96)
            gtr.append(f"{chordhead(ch)}/{16 if kind == 'blast' else 8}@{v}" + ("" if kind == "blast" else "^gate=1.2"))
    guitars = rhythm_tracks("expr.pm=0 " + " ".join(gtr), fx=expand(["rack:chorus-wide"]))  # space comes from the wet energy hall
    bass = [track("bass", rig("bass"), " ".join(f"{mname(k.deg(root, 28 + 12))}/2@104" for root in prog for _ in range(2)), seed=7)]
    drums = _drums_of(gen_blast(r, k, prog, 28, "trad")) if kind == "blast" else _drums_of(gen_tool(r, k, 28, 8, [3, 3, 2], "build", reps=4))
    return guitars + bass + drums


# ---------- darksynth -------------------------------------------------------------------------

def gen_darksynth(r, k, prog, kind="verse"):
    """Darksynth (Carpenter Brut / Perturbator): 16th distorted-bass octaves, supersaw arps,
    electro drums with a big gated snare (four-on-the-floor in verses, half-time in drops);
    kind=drop adds doubled metal chugs on the bass rhythm."""
    t = k.deg(0, 33)
    kit = pick_patch("electro-kit", "909")
    bass, kick, snare, hats = [], [], [], []
    for bar, root in enumerate(prog):
        rt = k.deg(root, 33)
        for x in range(16):
            bass.append(f"{mname(rt + (12 if x % 2 else 0))}/16@{110 if x % 4 == 0 else 96}")
            if kind == "drop":
                kick.append("k/16@120" if x in (0, 10) else "R/16"); snare.append("s/16@122" if x == 8 else "R/16")
            else:
                kick.append("k/16@118" if x % 4 == 0 else "R/16"); snare.append("s/16@118" if x in (4, 12) else "R/16")
            hats.append(f"h/16@{80 if x % 2 == 0 else 60}" if x % 2 == 0 or kind == "drop" else "R/16")
    gated = [{"type": "reverb", "kind": "plate", "decay": "1.2s", "mix": 0.3}, {"type": "gate", "threshold": "-30dB", "hold": "60ms", "release": "20ms"}]
    jn = lambda xs: " ".join(xs)
    out = [track("bassA", pick_patch("808-dist", "reese", "acid"), jn(bass), gain="-4dB"),
           track("kick", kit, jn(kick)), track("snare", kit, jn(snare), fx=gated), track("hats", kit, jn(hats), pan=0.1, gain="1.5dB")]
    out += gen_arp(r, k, prog, 60, pick_patch("supersaw", "arp-pluck"))
    if kind == "drop":
        chug = [f"expr.pm=1 {mname(t)}/16@{112 if x % 4 == 0 else 100}" if x % 2 == 0 else "R/16" for x in range(64)]
        out += rhythm_tracks(jn(chug))
    return out


def mirror_bass(tokens, d="/16"):
    """A bass line from a guitar token list: same rhythm and velocity, the lowest note of each
    chord; rests stay rests, bend/hold steps hold."""
    out = []
    for g in tokens:
        if g.startswith("R"):
            out.append("R" + d)
        elif g.startswith("bend") or g.startswith("_"):
            out.append("_")
        else:
            head = re.sub(r"expr\.pm=\d ", "", g).split("/")[0].split(",")[0]
            vel = g.split("@")[1].split("^")[0] if "@" in g else "100"
            out.append(f"{head}{d}@{vel}")
    return out


# ---------- nu-metal ---------------------------------------------------------------------------

def gen_numetal(r, k, prog, low=23, kind="bounce"):
    """Korn-style: bounce (syncopated low chugs with pitch dips and b9 pinch squeals over a hip-hop
    groove: syncopated kick, ghosts, open hats on the ands), verse (creepy muted notes and harmonics
    over a sparse beat), chorus (big ringing power chords, crash/ride)."""
    t = k.deg(0, low)
    pat = r.choice(["x..x..x.x.x..x..", "x.x..x..x..x.x..", "x..x.x..x..x..x."])
    gtr, bass, kick, snare, cym = [], [], [], [], []
    dip = False
    for i in range(64):
        x = i % 16
        if kind == "bounce":
            if dip:  # the step after a dip note: hold it and bend down a semitone
                gtr.append("bend=-1 _ bend="); dip = False
            elif pat[x] == "x":
                if r.random() < 0.12:
                    gtr.append(f"expr.pm=0 {mname(t + 13)}/16@118^ph^gate=1.5")
                elif r.random() < 0.15 and x < 15:
                    gtr.append(f"expr.pm=1 {mname(t)}/16@116"); dip = True
                else:
                    gtr.append(f"expr.pm=1 {mname(t)}/16@{116 if x == 0 else 108}")
            else:
                gtr.append("R/16")
            kick.append("k/16@118" if pat[x] == "x" and x not in (4, 12) else "R/16")
            snare.append("s/16@118" if x in (4, 12) else (f"g/16@{r.choice([32, 40])}" if r.random() < 0.15 else "R/16"))
            cym.append("oh/16@84" if x in (2, 6, 10, 14) and r.random() < 0.5 else (f"h/16@{76 if x % 2 == 0 else 54}" if x % 2 == 0 else "R/16"))
        elif kind == "verse":
            if x % 4 == 0 and r.random() < 0.7:
                gtr.append(f"expr.pm=1 {mname(t + r.choice([12, 13, 18]))}/16@{84}" if r.random() < 0.6 else f"{mname(t + 12)}/16@90^nh=2^gate=2")
            else:
                gtr.append("R/16")
            kick.append("k/16@104" if x in (0, 7, 10) else "R/16")
            snare.append("rc/16@80" if x in (4, 12) else "R/16")
            cym.append("hs/16@64" if x % 2 == 0 else "R/16")
        else:
            root = k.deg(prog[i // 16], low)
            gtr.append(f"expr.pm=0 {chordhead([root, root + 7, root + 12])}/16@122^gate=1.8" if x in (0, 6, 8) else "R/16")
            kick.append("k/16@118" if x in (0, 6, 8, 11) else "R/16")
            snare.append("s/16@120" if x in (4, 12) else "R/16")
            cym.append(f"{'c' if x == 0 else 'rds'}/16@{110 if x == 0 else 88}" if x % 2 == 0 else "R/16")
    bass = mirror_bass(gtr)
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    return rhythm_tracks(jn(gtr)) + [track("bass", pick_patch("slap-bass", "pick-bass", "bass-fat"), jn(bass), seed=7),
            track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- industrial -------------------------------------------------------------------------

def gen_industrial(r, k, prog, low=28, kind="march"):
    """Rammstein/Ministry: march (straight 8th palm-muted chugs on the root with power-chord stomps,
    four-on-the-floor metal kick + electro clap, 16th sequencer arp), stomp (stop-start hits),
    verse (synth bass + drum machine)."""
    t = k.deg(0, low)
    gtr, kick, snare, clap = [], [], [], []
    for i in range(64):
        x = i % 16
        root = k.deg(prog[i // 16], low)
        if root - t > 6:
            root -= 12
        if kind == "march":
            gtr.append(f"expr.pm=0 {chordhead([root, root + 7, root + 12])}/16@124^gate=0.9" if x == 0 else (f"expr.pm=1 {mname(t)}/16@{108 if x % 4 == 0 else 98}" if x % 2 == 0 else "R/16"))
        elif kind == "stomp":
            hit = x in (0, 3, 6) or (x == 12 and r.random() < 0.6)
            gtr.append(f"expr.pm=0 {chordhead([root, root + 7, root + 12])}/16@124^gate=0.6" if hit else "R/16")
        else:
            gtr.append("R/16")
        kick.append("k/16@120" if x % 4 == 0 and kind != "stomp" else ("k/16@122" if kind == "stomp" and x in (0, 3, 6, 12) else "R/16"))
        snare.append("s/16@118" if x in (4, 12) and kind != "stomp" else "R/16")
        clap.append("cp/16@110" if x in (4, 12) else "R/16")
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    out = [track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("clap", pick_patch("electro-kit", "909"), jn(clap))]
    if kind != "verse":
        out += rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr)), seed=7)]
    else:
        out += gen_bassline(r, k, prog, 33, pick_patch("808-dist", "acid"))
    return out + [dict(t, gain="-6dB") for t in gen_arp(r, k, prog, 60, pick_patch("supersaw", "arp-pluck"))]


# ---------- drum & bass / neuro --------------------------------------------------------------

def gen_dnb(r, k, prog, kind="drop"):
    """Pendulum-style D&B at ~174: two-step amen-ish break edits (break-kit) under a sliding reese
    with growl stabs; kind=metal layers palm-muted chugs on the bass rhythm; kind=intro is drums
    and pads only."""
    kit = pick_patch("break-kit", "metal-kit")
    kick, snare = [], []
    for i in range(64):
        x = i % 16
        kick.append("k/16@118" if x in (0, 10) or (x == 11 and r.random() < 0.3) else "R/16")
        snare.append("s/16@120" if x in (4, 12) else (f"{r.choice(['g', 's2'])}/16@{r.choice([44, 60, 70])}" + ("^r=2" if r.random() < 0.15 else "") if r.random() < 0.25 else "R/16"))
    hats = [f"h/16@{76 if x % 2 == 0 else 56}" if x % 2 == 0 or r.random() < 0.3 else "R/16" for x in range(64)]
    jn = lambda xs: " ".join(xs)
    out = [track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("hats", kit, jn(hats), pan=0.12)]
    if kind == "intro":
        return out
    t = k.deg(0, 33)
    bass, stabs, gtr = [], [], []
    for i in range(64):
        x = i % 16
        root = k.deg(prog[i // 16], 33)
        if x % 4 == 0:
            bass.append(f"{mname(root + (12 if x == 8 else 0))}/16@110^gate=3.8")
        else:
            bass.append("_")
        stabs.append(f"{mname(root + 12)}/16@108" if x in (6, 14) and r.random() < 0.6 else "R/16")
        gtr.append((f"expr.pm=0 {chordhead([t, t + 7, t + 12])}/16@122^gate=0.9" if x in (0, 10) else (f"expr.pm=1 {mname(t)}/16@106" if x % 2 == 0 else "R/16")) if kind == "metal" else "R/16")
    out += [track("reese", pick_patch("reese", "saw-pad"), jn(bass), gain="-4dB"), track("bassB", pick_patch("growl", "wobble", "acid"), jn(stabs), gain="-6dB"),
            track("sub", rig("sub"), jn(bass), seed=7, gain="-2dB")]
    if kind == "metal":
        out += rhythm_tracks(jn(gtr))
    return out


def gen_clusters(r, k, prog, base, patch, gain="-6dB", vel=74):
    """Dissonant pad: minor-2nd and tritone clusters over the progression roots."""
    out = []
    for root in prog:
        rt = k.deg(root, base)
        out.append(f"{chordhead(r.choice([[rt, rt + 1, rt + 6], [rt, rt + 6, rt + 13], [rt + 1, rt + 6, rt + 12], [rt, rt + 7, rt + 13]]))}/1@{vel}")
    return [track("pad", patch, " ".join(out), gain=gain)]


def _write_parts(slot, style, parts, desc, beats=None):
    names = {}
    for role, tr in parts.items():
        n = f"gen-{slot}-{role}"
        write(n, f"{role} for {style} in {desc}", tr, (beats or {}).get(role, 16))
        names[role] = n
    return names, desc


# ---------- per-style composition -------------------------------------------------------

def params(style, rng=random):
    mode = rng.choice(STYLE_MODES.get(style, ["minor"]))
    heavy = style in ("meshuggah", "djent", "djent-breakdown", "doom-ambient", "tech-death", "thrash", "tool", "hardcore-kl", "brostep", "blackgaze", "darksynth", "numetal", "industrial", "dnb")
    rigset = ("tech" if style == "tech-death" and rng.random() < 0.6 else
              "thrash" if style == "thrash" else
              "chug" if style in ("hardcore-kl", "brostep") else
              rng.choice(["tool-fuzz", "tool-pick", "tool-fuzz", "phase"]) if style == "tool" else
              rng.choice(["modern", "chug", "chug", "fuzz", "phase"])) if heavy else "modern"
    flavor = rng.choice(["modern", "modern", "vintage", "industrial", "space", "wide"]) if style != "industrial" else "industrial"
    return {"pc": rng.randrange(12), "mode": mode, "prog": rng.choice(PROGS[mode]), "seed": rng.randrange(1 << 30), "rigset": rigset, "flavor": flavor}


def compose(style, slot, p):
    """Write gen-<slot>-{riff,hook,pad,soft,arp,hold}; return role → part name."""
    global _RIGSET
    _RIGSET = RIG_SETS.get(p.get("rigset", "modern"), {})
    _FLAVOR["name"] = p.get("flavor", "modern")
    r = random.Random(p["seed"])
    k = Key(p["pc"], p["mode"])
    prog = p["prog"]
    low = 28  # E1: 8-string range for riffs
    gp = r.choice(["m8-tight", "m8-tight", "m8-nolly"]) if style in ("djent", "djent-breakdown", "meshuggah", "doom-ambient") else r.choice(["m8-tight", "m8-gojira", "m8-nolly"])
    if style == "brostep":
        pad_p = pick_patch("supersaw", "saw-pad")
        parts = {
            "riffIntro": gen_bro_intro(r, k, prog),
            "riffUp": gen_bro_build(r, k, prog),
            "riff": gen_bro_drop(r, k, prog),
            "riffB": gen_bro_drop(r, k, prog),
            "riffM": gen_bro_drop(r, k, prog, metal=True),
            "riffM2": gen_bro_drop(r, k, prog, metal=True),
            "pad": gen_pad(r, k, prog, 48, pad_p, gain="-8dB"),
            "soft": gen_clusters(r, k, prog, 48, "ambient-swell", vel=68),
            "arp": gen_arp(r, k, prog, 60, pick_patch("pluck-lead", "arp-pluck")),
            "hookE": gen_atmos(r, k, prog, 62, rig("atmos")),
        }
        return _write_parts(slot, "brostep", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "numetal":
        parts = {"riff": gen_numetal(r, k, prog, 23, "bounce"), "riffB": gen_numetal(r, k, prog, 23, "bounce"),
                 "riffV": gen_numetal(r, k, prog, 23, "verse"), "riffH": gen_numetal(r, k, prog, 23, "chorus"),
                 "riffBrk": gen_hc(r, k, prog, 23, "beatdown"), "hook": gen_hook(r, k, prog, 62, rig("lead")), "pad": gen_clusters(r, k, prog, 48, "saw-pad")}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "numetal", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "industrial":
        parts = {"riff": gen_industrial(r, k, prog, low, "march"), "riffS": gen_industrial(r, k, prog, low, "stomp"),
                 "riffV": gen_industrial(r, k, prog, low, "verse"), "hook": gen_hook(r, k, prog, 64, pick_patch("synth-lead", "lead-monster")),
                 "pad": gen_pad(r, k, prog, 48, pick_patch("supersaw", "saw-pad"), gain="-8dB")}
        parts["riffSoft"] = soften(parts["riff"])
        parts["riffUp"] = parts["riffV"]
        return _write_parts(slot, "industrial", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "dnb":
        parts = {"riffIntro": gen_dnb(r, k, prog, "intro") + gen_pad(r, k, prog, 48, pick_patch("supersaw", "saw-pad"), gain="-8dB"),
                 "riffUp": gen_bro_build(r, k, prog), "riff": gen_dnb(r, k, prog, "drop"), "riffB": gen_dnb(r, k, prog, "drop"),
                 "riffM": gen_dnb(r, k, prog, "metal"), "riffM2": gen_dnb(r, k, prog, "metal"),
                 "pad": gen_pad(r, k, prog, 48, pick_patch("supersaw", "saw-pad"), gain="-8dB"), "soft": gen_clusters(r, k, prog, 48, "ambient-swell", vel=68),
                 "arp": gen_arp(r, k, prog, 60, pick_patch("pluck-lead", "arp-pluck")), "hookE": gen_atmos(r, k, prog, 62, rig("atmos"))}
        return _write_parts(slot, "dnb", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "blackgaze":
        parts = {"riffClean": gen_gaze(r, k, prog, "clean"), "riff": gen_gaze(r, k, prog, "blast"), "riffB": gen_gaze(r, k, prog, "blast"),
                 "riffH": gen_gaze(r, k, prog, "half"), "hook": gen_hook(r, k, prog, 64, rig("lead")), "hookE": gen_atmos(r, k, prog, 62, rig("atmos"))}
        parts["riffUp"] = parts["riffH"]
        return _write_parts(slot, "blackgaze", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "darksynth":
        parts = {"riffIntro": gen_arp(r, k, prog, 60, pick_patch("supersaw", "arp-pluck")) + gen_pad(r, k, prog, 48, pick_patch("supersaw", "saw-pad"), gain="-8dB"),
                 "riff": gen_darksynth(r, k, prog, "verse"), "riffD": gen_darksynth(r, k, prog, "drop"), "riffD2": gen_darksynth(r, k, prog, "drop"),
                 "riffUp": gen_darksynth(r, k, prog, "verse"), "hook": gen_hook(r, k, prog, 64, pick_patch("synth-lead", "chip-lead")),
                 "pad": gen_pad(r, k, prog, 48, pick_patch("supersaw", "saw-pad"), gain="-8dB")}
        return _write_parts(slot, "darksynth", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "hardcore-kl":
        parts = {
            "riff": gen_hc(r, k, prog, low, "twostep"),
            "riffD": gen_hc(r, k, prog, low, "dbeat"),
            "riffBd": gen_hc(r, k, prog, low, "beatdown"),
            "riffBd2": gen_hc(r, k, prog, low, "beatdown"),
            "riffSlow": gen_hc(r, k, prog, low, "slowdown"),
            "riffStop": gen_hc(r, k, prog, low, "stop"),
            "riffSq": gen_space(r, k, low, gp, r.choice([11, 13, 9])),
        }
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "hardcore-kl", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "thrash":
        parts = {
            "riff": gen_thrash(r, k, prog, 40, "skank"),
            "riffG": gen_thrash(r, k, prog, 40, "gallop"),
            "riffC": gen_thrash(r, k, prog, 40, "chromatic"),
            "riffH": gen_thrash(r, k, prog, 40, "half"),
            "riffBrk": gen_meshuggah(r, k, 40, gp, r.choice([7, 11, 5]), grid="8", mode="break"),
            "hook": gen_hook(r, k, prog, 64, rig("lead")),
            "solo": gen_shred(r, k, prog, 64, pick_patch("lead-wah", "lead-monster")),
            "pad": gen_clusters(r, k, prog, 48, "saw-pad"),
        }
        parts["riffSoft"] = soften(parts["riffG"])
        return _write_parts(slot, "thrash", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "tool":
        m1 = r.choice([7, 7, 5, 9, 11, 13]); g1 = r.choice(METERS[m1])
        m2 = r.choice([31, 31, 23, 15]); g2 = r.choice(METERS[m2])
        m3 = r.choice([9, 11, 13]); g3 = r.choice(METERS[m3])
        tl = rig("lead")
        parts = {
            "riffClean": gen_tool(r, k, low, m1, g1, "clean"),
            "riffCleanB": gen_tool(r, k, low, m1, g1, "clean"),
            "riff": gen_tool(r, k, low, m1, g1, "heavy"),
            "riffB": gen_tool(r, k, low, m2, g2, "heavy"),
            "riffT": gen_tool(r, k, low, m3, g3, "tribal"),
            "riffP": gen_tool(r, k, low, m2, g2, "poly"),
            "riffUp": gen_tool(r, k, low, m1, g1, "build"),
            "hookA": gen_tool_lead(r, k, prog, m1, 62, tl),
            "hookB": gen_tool_lead(r, k, prog, m2, 62, tl),
        }
        parts["riffSoft"] = soften(parts["riff"])
        lens = {"riffClean": m1, "riffCleanB": m1, "riff": m1, "riffSoft": m1, "riffUp": m1, "hookA": m1,
                "riffB": m2, "riffP": m2, "hookB": m2, "riffT": m3}
        desc = f"{NAMES[p['pc']]} {p['mode']}, meters {m1}/8 ({'+'.join(map(str, g1))}), {m2}/8 ({'+'.join(map(str, g2))}), {m3}/8, rigs {p.get('rigset', 'modern')}"
        return _write_parts(slot, "tool", parts, desc, {role: m * reps_for(m) / 2 for role, m in lens.items()})
    if style == "tech-death":
        kinds = r.sample(["trad", "hammer", "bomb"], 2)
        parts = {
            "riff": gen_blast(r, k, prog, low, kinds[0]),
            "riffB": gen_blast(r, k, prog, low, kinds[1]),
            "riffD": gen_blast(r, k, prog, low, "dbeat"),
            "riffG": gen_meshuggah(r, k, low, gp, r.choice([14, 22, 20])),
            "riffBrk": gen_meshuggah(r, k, low, gp, r.choice([7, 11, 5]), grid="8", mode="break"),
            "riffT": gen_meshuggah(r, k, low, gp, r.choice([22, 14, 20, 18]), mode="toms"),
            "hook": gen_shred(r, k, prog, 62, rig("lead")),
            "pad": gen_clusters(r, k, prog, 48, "saw-pad"),
            "soft": gen_clusters(r, k, prog, 48, "ambient-swell", vel=68),
            "drone": gen_drone(k, 36, "drone"),
        }
        parts["riffSoft"] = soften(parts["riffG"])
        desc = f"{NAMES[p['pc']]} {p['mode']}, blasts {'/'.join(kinds)}, rigs {p.get('rigset', 'modern')}"
        names = {}
        for role, tr in parts.items():
            n = f"gen-{slot}-{role}"
            write(n, f"{role} for tech-death in {desc}", tr)
            names[role] = n
        return names, desc
    if style == "meshuggah":
        cycles = r.sample([22, 14, 20, 18, 26, 23, 13], 3)  # 11/8, 7/8, 10/8, 9/8, 13/8, 23/16, 13/16
        parts = {
            "riff": (main := gen_meshuggah(r, k, low, gp, cycles[0])),
            "riffSoft": soften(main),
            "riffB": gen_meshuggah(r, k, low, gp, cycles[1]),
            "riffC": gen_meshuggah(r, k, low, gp, cycles[2]),
            "riffX": gen_space(r, k, low, gp, r.choice([11, 13, 9, 14])),
            "hookE": gen_atmos(r, k, prog, 62, rig("atmos")),
            "riffT": gen_meshuggah(r, k, low, gp, r.choice([22, 14, 20, 18]), mode="toms"),
            "riffBl": gen_blast(r, k, prog, low, r.choice(["trad", "hammer", "bomb"])),
            "riffS": gen_meshuggah(r, k, low, gp, r.choice([11, 7, 10, 5]), grid="12", mode="shuffle"),
            "riffBrk": gen_meshuggah(r, k, low, gp, r.choice([7, 11, 5]), grid="8", mode="break"),
            "hook": gen_hook(r, k, prog, 62, rig("lead")),
            "pad": gen_clusters(r, k, prog, 48, "saw-pad"),
            "soft": gen_clusters(r, k, prog, 48, "ambient-swell", vel=68),
            "arp": gen_arp(r, k, prog, 55, "arp-pluck"),
            "hold": gen_hold(r, k, prog, low, gp),
            "drone": gen_drone(k, 36, "drone"),
        }
        desc = f"{NAMES[p['pc']]} {p['mode']}, cycles {'/'.join(f'{c}/16' for c in cycles)}, rigs {p.get('rigset', 'modern')}"
        names = {}
        for role, tr in parts.items():
            n = f"gen-{slot}-{role}"
            write(n, f"{role} for meshuggah in {desc}", tr)
            names[role] = n
        return names, desc
    heavy = style in ("djent", "djent-breakdown", "doom-ambient")
    if style in ("djent", "djent-breakdown"):
        riff = gen_djent(r, k, prog, low, style == "djent-breakdown")
    elif style == "doom-ambient":
        riff = gen_hold(r, k, prog, low, gp)
    elif style == "prog-clean":
        riff = gen_taps(r, k, prog, 50)
    elif style == "poly":
        riff = gen_chops(r, k, prog, 52) + gen_808(r, k, prog, 26, pick_patch("808-slide", "808"))
    elif style in ("house",):
        riff = gen_bassline(r, k, prog, 33)
    elif style == "garage":
        riff = gen_808(r, k, prog, 26, pick_patch("808-short", "808")) + gen_stabs(r, k, prog, 50, "rhodes")
    elif style == "idm" and r.random() < 0.6 and have("reese"):
        riff = gen_bassline(r, k, prog, 33, r.choice([p for p in ["reese", "growl"] if have(p)]))
    elif style in ("acid", "hardcore", "idm"):
        riff = gen_acid(r, k, prog, 33)
    elif style == "lofi":
        riff = gen_comp(r, k, prog, 50)
    else:  # classical
        riff = gen_alberti(r, k, prog, 41)
    hook_patch = {"djent": r.choice(["lead-monster", "synth-lead"] + (["supersaw"] if have("supersaw") else [])),
                  "hardcore": pick_patch("hoover", "synth-lead"), "djent-breakdown": "lead-monster", "doom-ambient": "lead-monster",
                  "prog-clean": r.choice(["synth-lead", "strat-neck"]), "poly": "nylon", "house": "house-chord", "garage": "rhodes",
                  "lofi": "nylon", "classical": "piano"}.get(style, "synth-lead")
    if style in ("house",) and not (have("pluck-lead") and r.random() < 0.5):
        hook = gen_stabs(r, k, prog, 53, "house-chord")
    elif style == "house":
        hook = gen_hook(r, k, prog, 64, "pluck-lead")
    else:
        hook = gen_hook(r, k, prog, 64 if style not in ("lofi", "poly", "classical") else 60, hook_patch)
    pad_patch = "strings" if style in ("classical", "doom-ambient") else ("rhodes" if style == "lofi" else "saw-pad")
    pad = gen_pad(r, k, prog, 48, pad_patch, gain="-6dB" if pad_patch == "rhodes" else "-4dB")
    soft = gen_pad(r, k, prog, 48, "strings" if not heavy else "ambient-swell", gain="-6dB", vel=70)
    arp = gen_arp(r, k, prog, 55, {"classical": "piano", "lofi": "rhodes", "prog-clean": "clean-chorus"}.get(style, "arp-pluck"))
    hold = gen_hold(r, k, prog, low, gp) if heavy or style in ("prog-clean", "poly") else gen_pad(r, k, prog, 48, "strings", vel=76)
    desc = f"{NAMES[p['pc']]} {p['mode']}, prog {'-'.join(str(d + 1) for d in prog)}"
    names = {}
    for role, tr in [("riff", riff), ("riffSoft", soften(riff)), ("hook", hook), ("pad", pad), ("soft", soft), ("arp", arp), ("hold", hold)]:
        n = f"gen-{slot}-{role}"
        write(n, f"{role} for {style} in {desc}", tr)
        names[role] = n
    return names, desc


if __name__ == "__main__":
    import sys
    style = sys.argv[1] if len(sys.argv) > 1 else "djent"
    p = params(style)
    print(compose(style, "test", p), p)
