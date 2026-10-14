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
    "blues": [0, 3, 5, 6, 7, 10], "pentatonic-minor": [0, 3, 5, 7, 10],
    "hirajoshi": [0, 2, 3, 7, 8], "pelog": [0, 1, 3, 7, 8],
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
    "blues": [[0, 0, 2, 0], [0, 2, 3, 0], [0, 4, 3, 2]], "pentatonic-minor": [[0, 0, 3, 2], [0, 3, 2, 0], [0, 2, 0, 4]],
    "hirajoshi": [[0, 0, 4, 3], [0, 3, 4, 0], [0, 1, 0, 4]], "pelog": [[0, 0, 3, 1], [0, 3, 0, 4], [0, 1, 3, 0]],
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
    "numetal": ["phrygian", "locrian", "minor"], "deathcore": ["phrygian", "harmonic", "locrian", "diminished"],
    "postrock": ["major", "lydian", "mixolydian", "dorian"], "postmetal": ["minor", "phrygian", "dorian", "harmonic"], "slam": ["phrygian", "locrian", "minor", "diminished"], "metalcore": ["minor", "harmonic", "dorian", "phrygian"], "symphonic": ["harmonic", "minor", "phrygian-dominant", "minor"], "cynic": ["lydian", "dorian", "minor", "diminished"], "tigran": ["phrygian-dominant", "harmonic", "phrygian", "minor"], "mahavishnu": ["dorian", "mixolydian", "phrygian", "minor"], "groovemetal": ["blues", "pentatonic-minor", "phrygian", "minor"],
    "power": ["major", "harmonic", "minor", "major"], "sludge": ["blues", "pentatonic-minor", "phrygian"],
    "breakcore": ["harmonic", "minor", "diminished", "phrygian-dominant"],
    "mathcore": ["locrian", "diminished", "phrygian", "double-harmonic"],
    "gojira": ["phrygian", "minor", "locrian", "pentatonic-minor"],
    "raga": ["phrygian-dominant", "double-harmonic", "harmonic", "phrygian"], "gamelan": ["pelog", "phrygian", "locrian"],
    "lofihop": ["dorian", "minor", "major", "mixolydian"], "gogo": ["minor", "dorian", "harmonic"], "ukjazz": ["dorian", "minor", "mixolydian"],
    "ambient": ["lydian", "major", "dorian", "pentatonic-minor"], "downtempo": ["dorian", "minor", "mixolydian"],
    "smile": ["dorian", "minor", "mixolydian", "phrygian"], "house-melodic": ["dorian", "minor", "major"],
    "chamber": ["major", "minor", "harmonic", "dorian"],
    "triphop": ["minor", "phrygian", "harmonic"], "neoclassical": ["major", "minor", "lydian", "dorian"], "ballad": ["major", "dorian", "minor"],
    "bossa": ["major", "dorian", "minor", "lydian"], "dub": ["minor", "dorian", "mixolydian"],
    "manouche": ["harmonic", "minor", "harmonic", "major"], "celtic": ["dorian", "mixolydian", "minor", "major"],
    "doomjazz": ["minor", "phrygian", "dorian", "harmonic"], "mali": ["dorian", "minor", "mixolydian"], "guofeng": ["major", "minor", "dorian"], "vaporwave": ["major", "lydian", "dorian", "minor"], "slowcore": ["major", "mixolydian", "minor", "dorian"],
    "backrooms": ["major", "lydian", "mixolydian"], "neosoul": ["dorian", "minor", "major", "mixolydian"], "minimal": ["major", "lydian", "dorian", "mixolydian"], "fusion": ["minor", "dorian", "major", "mixolydian"], "berlin": ["minor", "dorian", "phrygian", "aeolian" if "aeolian" in MODES else "minor"], "satie": ["major", "lydian", "mixolydian", "dorian"], "kankyo": ["major", "lydian", "dorian", "mixolydian"], "dawnraga": ["double-harmonic", "phrygian-dominant", "phrygian", "mixolydian"], "handpan": ["minor", "dorian", "phrygian-dominant", "hirajoshi"], "citypop": ["major", "lydian", "dorian", "major"], "lid": ["major", "lydian", "minor", "dorian"], "tiersen": ["minor", "major", "harmonic", "dorian"], "balearic": ["phrygian-dominant", "minor", "dorian", "major"], "chillwave": ["major", "lydian", "dorian", "mixolydian"], "souljazz": ["mixolydian", "dorian", "blues", "mixolydian"], "ethiojazz": ["minor", "hirajoshi", "major", "phrygian"], "hauntology": ["major", "dorian", "lydian", "minor"], "dawnchorus": ["major", "lydian", "mixolydian"], "beattape": ["minor", "dorian", "major"], "lofihouse": ["minor", "dorian", "major"], "amapiano": ["minor", "dorian", "minor"], "liquid": ["minor", "dorian", "major", "lydian"], "nujazz": ["dorian", "minor", "mixolydian"], "highlife": ["major", "mixolydian", "major"], "samba": ["major", "dorian", "minor", "mixolydian"], "rumba": ["phrygian-dominant", "harmonic", "minor"], "secondline": ["mixolydian", "major", "blues"], "exotica": ["major", "lydian", "minor", "dorian"], "slowed": ["major"], "cyberscape": ["minor", "dorian", "lydian", "phrygian"],
    "koto": ["hirajoshi", "hirajoshi", "phrygian"],
    "djazz": ["dorian", "lydian", "harmonic", "minor", "mixolydian"], "industrial": ["phrygian", "minor", "harmonic"], "dnb": ["minor", "phrygian", "dorian"],
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
        _HAVE[patch] = any(subprocess.run([c, "plan", "-p", patch, note], capture_output=True).returncode == 0 for note in ("R/4", "R/4 C2/4", "k/4", "na/4"))
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
    "gojira": {"rhythm": (("m8-gojira", "m8-gojira layers.0.pick=0.095 humanize.time=9ms"),), "lead": ("lead-monster", "lead-tape")},
    "emg": {"rhythm": (("m8-emg-l", "m8-emg-r"),)},
    "bkp": {"rhythm": (("m8-bkp-l", "m8-bkp-r"),), "lead": ("lead-tape", "lead-monster")},
    "fluence": {"rhythm": (("m8-fluence-l", "m8-fluence-r"),), "lead": ("lead-slap", "lead-monster")},
    "chill": {"drums": ("tight-kit", "prog-kit"), "clean": ("tele", "strat-neck", "clean-chorus"), "bass": ("finger-bass", "bass-di")},
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
    if LITE:  # little render headroom: one centred rig instead of the double (halves the amp-sim cost)
        return [track("gtr-l", left, score, pan=0, seed=seeds[0], **extra)]
    return [track("gtr-l", left, score, pan=f"L{pan}", seed=seeds[0], **extra), track("gtr-r", right, score, pan=f"R{pan}", seed=seeds[1], **extra)]


# Section inserts for variety (post-rig): picked per part.
SECTION_FX = {
    "space": [None, None, ["rack:phaser-slow"], ["rack:chorus-wide"], ["rack:shimmer-hall"], ["rack:glitch-reverse"]],
    "break": [None, None, None, ["rack:stutter-16"], ["rack:dub-throw"], ["rack:octave-down"], ["rack:glitch-stutter"]],
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
        pts = [["0b", 0], [f"{beats - 3:g}b", 0], [f"{beats - 2.9:g}b", 1], [f"{beats - 0.1:g}b", 1], [f"{beats:g}b", 0]]
        tracks = [_add(t, fx=[{"type": "freeze", "size": "180ms", "mix": 0.7, "hold": {"value": 0, "mod": [{"src": "auto.frz", "amount": 1}]}}],
                       auto={"frz": {"points": pts}}) if t["name"] == "twang" else t for t in tracks]
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

def gen_djent_clean(r, k, prog):
    """Djent's ambient side (TesseracT / Periphery): clean arpeggios on add9 / maj7 chords through a
    ping-pong delay and hall, over a Juno or glass pad."""
    arp = []
    for root in prog:
        tones = [k.deg(root + d, 55) for d in r.choice([(0, 4, 8, 9), (0, 2, 4, 6), (0, 4, 6, 8)])]
        arp += [f"{mname(tones[i])}/8@{74 if j % 4 == 0 else 62}" for j, i in enumerate(r.choice([[0, 1, 2, 3, 2, 1, 2, 3], [0, 2, 1, 3, 0, 2, 3, 1]]))]
    delay = [{"type": "delay", "time": "3/16", "feedback": 0.45, "ping_pong": True, "tone": 3500, "mix": 0.32}, {"type": "reverb", "kind": "hall", "decay": "3.5s", "mix": 0.35}]
    return [track("clean", pick_patch("clean-chorus", "tele"), " ".join(arp), pan=-0.2, fx=delay)] + \
        [dict(t, name="pad", gain="-10dB") for t in gen_pad(r, k, prog, 52, pick_patch(r.choice(["juno-pad", "pad-glass"]), "pad"), vel=58)]


def gen_tapping(r, k, prog, patch):
    """Animals as Leaders-style tapping: sextuplet arpeggios across the chord tones in a high register."""
    out = []
    for root in prog:
        tones = [k.deg(root + d, 67) for d in r.choice([(0, 2, 4, 7, 9, 11), (0, 4, 7, 9, 11, 14), (0, 2, 4, 6, 7, 9)])]
        shape = r.choice([[0, 1, 2, 3, 4, 5], [0, 2, 4, 5, 3, 1], [5, 3, 1, 0, 2, 4]])
        out += [f"{mname(tones[i])}/24@{80 if j % 6 == 0 else 66}" for _ in range(4) for j, i in enumerate(shape)]
    return [track("tap", patch, " ".join(out), pan=0.25, gain="-4dB",
                  fx=[{"type": "delay", "time": "1/8", "feedback": 0.2, "mix": 0.15}, {"type": "reverb", "kind": "plate", "decay": "1.6s", "mix": 0.2}])]


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
    """A 16-beat melody in one of three phrase forms — classic (motif, repeat with an altered ending,
    sequence, cadence), call-and-response (motif, short answer, sequenced motif, long tone + rest) or
    sparse (motif, a bar of silence, inverted motif, short cadence). Non-heavy instruments breathe
    (long final notes clipped with a rest) and get a phrase-arc dynamic instead of fixed hard hits."""
    cells = [[0.5, 0.5, 1, 2], [1, 0.5, 0.5, 1, 1], [0.75, 0.75, 0.5, 2], [0.5, 0.25, 0.25, 1, 2], [1.5, 0.5, 2], [0.5, 0.5, 0.5, 0.5, 2]]
    rhythm = r.choice(cells)
    steps = [0] + [r.choice([-2, -1, 1, 1, 2, 3, -3]) for _ in rhythm[1:]]
    heavy = str(patch).startswith(("lead-", "m8"))
    form = "classic" if heavy else r.choice(["classic", "classic", "qa", "sparse"])

    def fmt(ln):
        return {0.25: "16", 0.5: "8", 0.75: "8.", 1: "4", 1.5: "4.", 2: "2", 3: "2.", 4: "1"}[ln]

    def vel(i, count, strong):
        if heavy:
            return 108 if strong else 96
        import math as _m
        arc = _m.sin(_m.pi * (i + 0.5) / max(1, count))
        return max(40, min(118, int(74 + 18 * arc + (6 if strong else 0) + r.randint(-5, 5))))

    def phrase(root, alt_end=False, inv=False, rhy=None):
        rhy = rhy or rhythm
        st_ = steps if len(steps) == len(rhy) else [0] + [r.choice([-2, -1, 1, 2]) for _ in rhy[1:]]
        d = root + r.choice([0, 2, 4])
        out = []
        for i, (ln, st) in enumerate(zip(rhy, st_)):
            d += -st if inv else st
            if i == len(rhy) - 1:
                d = root + (r.choice([2, 4]) if alt_end else r.choice([0, 4]))
            tok = f"{mname(k.deg(d, base))}/{fmt(ln)}@{vel(i, len(rhy), i == 0 or ln >= 1)}"
            if i == len(rhy) - 1 and ln >= 2 and not heavy and r.random() < 0.5:  # breathe
                tok = f"{mname(k.deg(d, base))}/{fmt(ln - 1)}@{vel(i, len(rhy), True)} R/4"
            out.append(tok)
        return out

    def cadence(root, short=False):
        last = mname(k.deg(0 if r.random() < 0.6 else 4, base))
        a, b = mname(k.deg(root + 4, base)), mname(k.deg(root + 2, base))
        if short:
            return [f"{a}/4@{vel(0, 3, True)}", f"{last}/4@{vel(1, 3, True)}", "R/2"]
        return [f"{a}/4@{vel(0, 3, True)}", f"{b}/4@{vel(1, 3, False)}", f"{last}/2@{vel(2, 3, True)}^gate=1.2"]

    if form == "qa":
        ans = r.choice([[1, 1, 2], [2, 2], [1.5, 0.5, 2]])
        d = prog[1] + r.choice([2, 4])
        answer = []
        for i, ln in enumerate(ans):
            answer.append(f"{mname(k.deg(d, base))}/{fmt(ln)}@{vel(i, len(ans), i == 0)}")
            d += r.choice([-1, -2, 1])
        tail = [f"{mname(k.deg(prog[3] + r.choice([0, 2, 4]), base))}/2@{vel(0, 2, True)}", "R/2"]
        body = phrase(prog[0]) + answer + phrase(prog[2], inv=r.random() < 0.4) + tail
    elif form == "sparse":
        body = phrase(prog[0]) + ["R/1"] + phrase(prog[2], inv=True) + cadence(prog[3], short=True)
    else:
        body = phrase(prog[0]) + phrase(prog[1], alt_end=True) + phrase(prog[2], inv=r.random() < 0.4) + cadence(prog[3])
        if r.random() < 0.5:  # lead-in: rest an eighth and shorten the cadence to keep 16 beats
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


def gen_thordendal(r, k, low, patch, beats=16):
    """A Fredrik Thordendal-style solo (Holdsworth-like fusion): fluid legato runs in 16ths or sextuplets
    over diminished / whole-tone fragments with wide leaps, long notes bent up and released, breaths."""
    t = k.deg(0, low) + 36
    scale = r.choice([[0, 1, 3, 4, 6, 7, 9, 10], [0, 2, 4, 6, 8, 10], [0, 2, 3, 5, 6, 8, 9, 11]])
    note = lambda idx: t + scale[idx % len(scale)] + 12 * (idx // len(scale))
    toks, used, idx = [], 0, r.randrange(len(scale))
    while used < beats:
        left = beats - used
        g = r.random()
        if g < 0.55 and left >= 1:  # legato run
            n_beats = min(left, r.choice([1, 1, 2]))
            per = r.choice([6, 4, 6])
            for j in range(n_beats * per):
                idx = max(0, min(2 * len(scale), idx + r.choice([1, 1, 2, -1, -2, 4, -4] if r.random() < 0.9 else [5, -5])))
                toks.append(f"{mname(note(idx))}/{24 if per == 6 else 16}@{100 if j % per == 0 else 88}")
            used += n_beats
        elif g < 0.8 and left >= 2:  # a long note bent up a whole tone and released
            toks.append(f"bend= {mname(note(idx))}/4@108 bend=2 _ bend=")
            used += 2
        else:
            toks.append("bend= R/4"); used += 1
    return [track("solo", patch, " ".join(toks), pan=0.15)]


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
    yoi = {"lfo": {"v": {"wave": "sine", "rate": "1/8"}},
           "fx": [{"type": "formant", "q": 9, "mix": 0.55, "vowel": {"value": 2, "mod": [{"src": "lfo.v", "amount": 2}]}}]}
    out = [dict(track("bassA", a_p, jn(A), gain="-6dB"), **yoi), track("bassB", b_p, jn(B), gain="-6dB"), track("sub", rig("sub"), jn(sub), seed=7, gain="-2dB")]
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
        trem = kind in ("blast", "drive")
        for i in range(16 if trem else 8):
            v = (104 if i % 2 == 0 else 92) if trem else (112 if i % 4 == 0 else 96)
            gtr.append(f"{chordhead(ch)}/{16 if trem else 8}@{v}" + ("" if trem else "^gate=1.2"))
    guitars = rhythm_tracks("expr.pm=0 " + " ".join(gtr), fx=expand(["rack:chorus-wide"]))  # space comes from the wet energy hall
    if kind == "drive":  # post-rock climax: tremolo chords over a driving 8th-note beat
        return guitars + [track("bass", rig("bass"), " ".join(f"{mname(k.deg(root, 40))}/8@108" for root in prog for _ in range(8)), seed=7)] + _drums_of(gen_thrash(r, k, prog, 40, "skank"))
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


# ---------- harmony leads / power metal -------------------------------------------------------

def note_midi(name):
    """`C#4` / `Eb3` → MIDI."""
    m = re.match(r"([A-G][b#]?)(-?\d+)$", name)
    if not m:
        return None
    pcs = {n: i for i, n in enumerate(NAMES)}
    pcs.update({"Db": 1, "D#": 3, "Gb": 6, "G#": 8, "A#": 10, "Cb": 11, "E#": 5, "Fb": 4, "B#": 0})
    return pcs[m.group(1)] + 12 * (int(m.group(2)) + 1)


def harmonize(score, k, steps=2, base=48):
    """Shift every note of a lead score `steps` scale degrees (2 = a diatonic third above)."""
    scale = sorted({k.deg(d, base) for d in range(-14, 40)})
    def shift(mt):
        n = note_midi(mt.group(0))
        if n is None or n not in scale:
            return mt.group(0)
        return mname(scale[min(len(scale) - 1, scale.index(n) + steps)])
    return re.sub(r"\b[A-G][b#]?-?\d+\b", shift, score)


def gen_twin_hook(r, k, prog, base, patch):
    """A lead hook doubled a diatonic third above (twin guitars), panned apart."""
    lead = gen_hook(r, k, prog, base, patch)[0]
    return [dict(lead, name="hook", pan=-0.25), dict(lead, name="hook3", pan=0.25, score=harmonize(lead["score"], k, 2), gain="-2dB")]


def gen_power(r, k, prog, low=40, kind="verse"):
    """Power metal: verse (16th double kick under palm-muted gallops), chorus (open power chords in
    8ths, crash-ride, half the snares), with a strings pad added at song level."""
    t = k.deg(0, low)
    gtr, kick, snare, cym = [], [], [], []
    for i in range(64):
        x = i % 16
        root = k.deg(prog[i // 16], low)
        if root - t > 7:
            root -= 12
        if kind == "verse":
            gtr.append(f"expr.pm=1 {mname(root)}/16@{116 if x % 4 == 0 else 100}" if x % 4 in (0, 2, 3) else "R/16")
            cym.append(f"{'c' if x == 0 else 'rd'}/16@{110 if x == 0 else 86}" if x % 4 == 0 else "R/16")
        else:
            gtr.append(f"expr.pm=0 {chordhead([root, root + 7, root + 12])}/16@{120 if x % 4 == 0 else 108}^gate=1" if x % 2 == 0 else "R/16")
            cym.append(f"{'c' if x % 8 == 0 else 'rde'}/16@{114 if x % 8 == 0 else 96}" if x % 4 == 0 else "R/16")
        kick.append(f"k/16@{110 if x % 2 == 0 else 98}")
        snare.append("s/16@118" if x in (4, 12) else (f"g/16@34" if r.random() < 0.06 else "R/16"))
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr)), seed=7), track("sub", rig("sub"), jn(mirror_bass(gtr)), seed=7),
            track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- sludge / stoner doom -------------------------------------------------------------

def gen_sludge(r, k, prog, low=28, kind="riff"):
    """Sludge: slow blues-scale riffs on an 8th grid with bends and dips over heavy half-time drums
    (riff), ringing feedback chords over tom rolls and ride wash (drone), a mid gallop (gallop)."""
    t = k.deg(0, low)
    blues = [0, 3, 5, 6, 7, 10, 12]
    gtr, kick, snare, cym = [], [], [], []
    dip = False
    for i in range(32):
        x = i % 8
        if kind == "riff":
            if dip:
                gtr.append("bend=-1 _ bend="); dip = False
            elif x == 0 or r.random() < 0.6:
                iv = 0 if x == 0 else r.choice(blues)
                if iv in (3, 10) and x < 7 and r.random() < 0.4:
                    gtr.append(f"expr.pm=0 {mname(t + iv)}/8@{114}"); dip = True
                else:
                    ch = [t + iv, t + iv + 7] if iv in (0, 5, 7) else [t + iv]
                    gtr.append(f"expr.pm={1 if iv == 0 and x else 0} {chordhead(ch)}/8@{120 if x == 0 else 108}^gate=1.3")
            else:
                gtr.append("R/8")
            kick.append("k/8@118" if x in (0, 3) else "R/8")
            snare.append("s/8@120" if x == 4 else "R/8")
            cym.append(f"{'c' if x == 0 and i % 16 == 0 else 'rde'}/8@{110 if x == 0 else 82}" if x % 2 == 0 else "R/8")
        elif kind == "drone":
            gtr.append(f"expr.pm=0 {chordhead([t, t + 7, t + 12])}/8@122^gate=4" if x == 0 else "R/8")  # a ringing chord every bar
            kick.append("k,ft/8@116" if x == 0 else "R/8")
            snare.append(f"{['t1', 't2', 't3', 'ft'][x % 4]}/8@{96 + x * 3}" if x >= 4 and i % 16 >= 8 else "R/8")
            cym.append("rde/8@90" if x % 2 == 0 else "R/8")
        else:
            gtr.append(f"expr.pm=1 {mname(t)}/8@{112 if x % 2 == 0 else 98}" if x != 6 else f"expr.pm=0 {chordhead([t + 3, t + 10])}/8@118")
            kick.append("k/8@116" if x % 2 == 0 else "R/8")
            snare.append("s/8@118" if x in (2, 6) else "R/8")
            cym.append(f"rds/8@88" if x % 2 == 0 else "R/8")
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr, "/8")), seed=7), track("sub", rig("sub"), jn(mirror_bass(gtr, "/8")), seed=7),
            track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- post-metal (Isis / Cult of Luna / Russian Circles / Neurosis) ----------------------

def gen_postmetal(r, k, prog, low=28, kind="crush"):
    """Post-metal. kind=clean: delay-soaked clean arpeggios, soft toms and ride bell. kind=toms: the
    tribal build — kick + floor-tom 8ths with rack-tom accents and ride under a repeating crunchy
    motif. kind=crush: slow, crushing half-time chords in drop tuning (ringing, palm-muted re-strikes),
    kick doubling, snare on 3, crash/china. kind=wall: the crush under a crash wash + strings."""
    t = k.deg(0, low)
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    kick, snare, cym, gtr = [], [], [], []
    if kind == "clean":
        arp = []
        for root in prog:
            tones = [k.deg(root + d, 52) for d in (0, 4, 7, 9)]
            arp += [f"{mname(tones[c])}/8@{78 if j % 4 == 0 else 64}" for j, c in enumerate(r.choice([[0, 1, 2, 3, 2, 1, 2, 1], [0, 2, 1, 3, 0, 2, 3, 1]]))]
        toms = jn((f"{r.choice(['t2', 't3', 'ft'])}/8@{60 if x % 4 == 0 else 44}" if x % 2 == 0 and r.random() < 0.5 else "R/8") for x in range(32))
        return [track("clean", pick_patch("clean-chorus", "tele"), jn(arp), pan=-0.2, fx=[{"type": "delay", "time": "3/8", "feedback": 0.4, "mix": 0.3, "ping_pong": True}, {"type": "reverb", "kind": "hall", "decay": "3s", "mix": 0.3}]),
                track("toms", kit, toms, gain="-4dB"), track("cym", kit, jn("rb/4@56" if x % 2 == 0 else "R/4" for x in range(16)), gain="-6dB"),
                track("bass", rig("bass"), jn(f"{mname(k.deg(root, low + 12))}/1@{70}" for root in prog), seed=7, gain="-4dB")]
    motif = r.choice([[0, None, 0, 3, None, 0, 5, None], [0, 0, None, 7, None, 5, 3, None], [0, None, 3, 0, None, 5, None, 7]])
    for i in range(32):
        x = i % 8
        root = prog[(i // 8) % len(prog)]
        rt = k.deg(root, low)
        if kind == "toms":
            d = motif[x]
            gtr.append(f"expr.pm=1 {mname(rt + d)}/8@{100 if x == 0 else 88}" if d is not None else "R/8")
            kick.append("k/8@104" if x in (0, 3, 6) else "R/8")
            snare.append(f"{'ft' if x % 2 == 0 else r.choice(['t1', 't2', 't3'])}/8@{98 if x % 2 == 0 else 84}" if x not in (0, 3) or i % 16 > 8 else "R/8")
            cym.append(f"rd/8@{80 if x % 2 == 0 else 62}")
        else:  # crush / wall
            if x == 0:
                gtr.append(f"expr.pm=0 {chordhead([rt, rt + 7, rt + 12])}/8@124^gate=3.5")
            elif x == 4 and r.random() < 0.6:
                gtr.append(f"expr.pm=0 {chordhead([rt + 3, rt + 10])}/8@116^gate=3.5")
            elif x == 7 and r.random() < 0.5:
                gtr.append(f"expr.pm=1 {mname(rt)}/8@108")
            else:
                gtr.append("R/8")
            kick.append("k/8@122" if x in (0, 1) or (x == 7 and r.random() < 0.4) else "R/8")
            snare.append("s/8@124" if x == 4 else "R/8")
            if kind == "wall":
                cym.append(f"{'c' if x % 2 == 0 else 'c'}/8@{112 if x == 0 else 96}")
            else:
                cym.append("c/8@114" if x == 0 else ("cch/8@104" if x == 4 and i % 16 == 4 else ("rde/8@86" if x % 2 == 0 else "R/8")))
    out = rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr, "/8")), seed=7), track("sub", rig("sub"), jn(mirror_bass(gtr, "/8")), seed=7),
                                    track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]
    if kind == "wall":
        out += [dict(tr, name="strings") for tr in gen_pad(r, k, prog, 52, "strings", gain="-8dB", vel=72)]
    return out


def gen_tremolo_lead(r, k, prog, base, patch):
    """Tremolo-picked high melody: each melody note repeated in 16ths, a slow line over the chords."""
    out = []
    for root in prog:
        for d in r.choice([[0, 2], [4, 2], [7, 4], [2, 0], [4, 7]]):
            n = mname(k.deg(root + d, base))
            out += [f"{n}/16@{96 if j % 4 == 0 else 84}" for j in range(8)]
    return [track("trem", patch, " ".join(out), pan=0.35, gain="-3dB")]


# ---------- brutal slam death metal (Devourment / Abominable Putridity / Ingested) -------------

def gen_slam(r, k, prog, low=28, kind="slam"):
    """Slam death. slam: a palm-muted chromatic chug cell on the low tonic and its minor-second
    neighbours with pinch-harmonic squeals bending up, half-time drums (kick doubling the chugs, snare
    on 3, china on the beats). blast: hyper-blasts under a tremolo-picked chromatic riff. gravity: a
    32nd snare roll under the tremolo riff. brk: sparser slower chugs with china/crash downbeats."""
    t = k.deg(0, low)
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    gtr, kick, snare, cym = [], [], [], []
    if kind in ("slam", "brk"):
        dens = 0.55 if kind == "slam" else 0.3
        cell = [i == 0 or r.random() < dens for i in range(16)]
        offs = [r.choice([0, 0, 0, 1, 2, -1]) for _ in range(16)]
        for i in range(64):
            x = i % 16
            if cell[x]:
                if x in (7, 15) and r.random() < 0.35:  # pinch squeal, bending up
                    gtr.append(f"expr.pm=0 {mname(t + 31 + r.choice([0, 1, 3]))}/16@124 bend=2")
                else:
                    gtr.append(f"expr.pm=1 bend= {mname(t + offs[x])}/16@{118 if x % 4 == 0 else 108}")
                kick.append(f"k/16@{120 if x % 4 == 0 else 110}")
            else:
                gtr.append("bend= R/16"); kick.append("R/16")
            snare.append("s/16@124" if x == 8 else "R/16")
            cym.append(("cch/16@112" if kind == "slam" else ("c/16@116" if x == 0 else "cch/16@108")) if x % 4 == 0 else "R/16")
    else:
        riff = [t + r.choice([0, 1, 2, 3, 6]) for _ in range(8)]
        for i in range(64):
            gtr.append(f"expr.pm=0 {mname(riff[(i // 2) % 8] + 12)}/16@{112 if i % 4 == 0 else 100}")
            if kind == "blast":
                kick.append("k/16@114" if i % 2 == 0 else "R/16"); snare.append("s/16@110" if i % 2 == 1 else "R/16")
                cym.append(f"{'c' if i % 16 == 0 else 'rd'}/16@{108 if i % 16 == 0 else 90}" if i % 2 == 0 else "R/16")
            else:  # gravity: one-handed snare roll at full speed
                kick.append("k/16@112" if i % 4 == 0 else "R/16")
                snare.append(" ".join(f"s/32@{r.choice([92, 98, 104])}" for _ in range(2)))
                cym.append("c/16@112" if i % 16 == 0 else "R/16")
    return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass([g.replace("bend= ", "").replace(" bend=2", "") for g in gtr], "/16")), seed=7),
                                     track("sub", rig("sub"), jn(mirror_bass([g.replace("bend= ", "").replace(" bend=2", "") for g in gtr], "/16")), seed=7),
                                     track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- metalcore (Killswitch Engage / Architects / Parkway Drive) --------------------------

def gen_metalcore(r, k, prog, low=28, kind="verse"):
    """Metalcore. verse: palm-muted 16th gallops (x-xx) on the low tonic with chord-root accents over
    double kick; chorus: open ringing melodic chords (root-fifth-octave + third on top) over driving
    8th kicks, crash on the 1s; harmony: twin guitars in diatonic thirds playing a melodic line;
    breakdown: half-time chugs on the low tonic with china and syncopated kicks."""
    t = k.deg(0, low)
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    gtr, kick, snare, cym = [], [], [], []
    if kind == "harmony":
        line = []
        d = r.choice([0, 2, 4])
        for i in range(32):
            d = max(-2, min(9, d + r.choice([-2, -1, 1, 1, 2])))
            line.append(d)
        lo = jn(f"expr.pm=0 {mname(k.deg(prog[(i // 8) % 4] * 0 + d, 52))}/8@{104 if i % 2 == 0 else 96}" for i, d in enumerate(line))
        hi = jn(f"expr.pm=0 {mname(k.deg(d + 2, 52))}/8@{104 if i % 2 == 0 else 96}" for i, d in enumerate(line))
        out = [track("gtr-l", rig("rhythm")[0], lo, pan="L80", seed=7), track("gtr-r", rig("rhythm")[1], hi, pan="R80", seed=13)]
        kick = ["k/8@104" if x % 2 == 0 else "R/8" for _ in range(4) for x in range(8)]
        snare = ["s/8@112" if x in (2, 6) else "R/8" for _ in range(4) for x in range(8)]
        cym = [f"{'c' if x == 0 else 'rd'}/8@{110 if x == 0 else 88}" for _ in range(4) for x in range(8)]
        return out + [track("bass", rig("bass"), jn(f"{mname(k.deg(root, 28))}/2@96 {mname(k.deg(root, 28))}/2@90" for root in prog), seed=7),
                      track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]
    for i in range(64):
        x = i % 16
        root = prog[(i // 16) % len(prog)]
        rt = k.deg(root, low)
        if kind == "verse":
            hit = x % 4 in (0, 2, 3)
            gtr.append((f"expr.pm=0 {chordhead([rt, rt + 7])}/16@118" if x == 0 else f"expr.pm=1 {mname(t)}/16@{110 if x % 4 == 0 else 100}") if hit else "R/16")
            kick.append(f"k/16@{112 if hit else 100}" if hit or x % 2 == 0 else "R/16")
            snare.append("s/16@118" if x in (4, 12) else "R/16")
            cym.append(f"{'c' if x == 0 and i % 32 == 0 else 'h'}/16@{108 if x == 0 else 82}" if x % 2 == 0 else "R/16")
        elif kind == "chorus":
            third = k.deg(root + 2, low + 12)
            gtr.append(f"expr.pm=0 {chordhead([rt, rt + 7, rt + 12, third + 12])}/16@116" if x == 0 else ("_" if x < 8 else (f"expr.pm=0 {chordhead([rt, rt + 7, rt + 12])}/16@108" if x == 8 else "_")))
            kick.append("k/16@110" if x % 2 == 0 else "R/16")
            snare.append("s/16@118" if x in (4, 12) else "R/16")
            cym.append(f"{'c' if x == 0 else 'rd'}/16@{112 if x == 0 else 90}" if x % 4 == 0 else "R/16")
        else:  # breakdown
            cell = "x..x.x....x..x.." if (i // 16) % 2 == 0 else "x..x.x..x.x.x..."
            hit = cell[x] == "x"
            gtr.append(f"expr.pm=1 {mname(t)}/16@{122 if x == 0 else 114}" if hit else "R/16")
            kick.append(f"k/16@{122 if x == 0 else 112}" if hit else "R/16")
            snare.append("s/16@124" if x == 8 else "R/16")
            cym.append("cch/16@114" if x % 4 == 0 else "R/16")
    return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr, "/16")), seed=7), track("sub", rig("sub"), jn(mirror_bass(gtr, "/16")), seed=7),
                                     track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- symphonic metal (Nightwish / Epica / Fleshgod Apocalypse) ---------------------------

def gen_symphonic(r, k, prog, low=28, kind="verse"):
    """Symphonic metal. orch: the orchestra alone (string chords, choir, horn swells, a timpani roll
    into each bar's last beat). verse: palm-muted gallops with power-chord accents over double kick,
    string stabs on 1 and the and-of-2, a choir pad. chorus: open power chords under double kick and
    crash-ride, a soaring violin line, choir chords and timpani downbeats."""
    t = k.deg(0, low)
    jn = lambda xs: " ".join(xs)
    strings_ch = lambda root, base=55: chordhead([k.deg(root + d, base) for d in (0, 2, 4, 7)])
    if kind == "orch":
        out = [track("strings", pick_patch("strings", "pad"), jn(f"{strings_ch(root)}/1@{80}" for root in prog), gain="-4dB"),
               track("choir", pick_patch("choir", "pad"), jn(f"{chordhead([k.deg(root + d, 57) for d in (0, 2, 4)])}/1@{72}" for root in prog), gain="-6dB"),
               track("horns", pick_patch("horn", "brass"), jn(f"{chordhead([k.deg(root, 45), k.deg(root + 4, 45)])}/2@{60} {chordhead([k.deg(root, 45), k.deg(root + 4, 45)])}/2@{84}" for root in prog), gain="-4dB"),
               track("timp", pick_patch("timpani", "tight-kit"), jn(f"R/2 R/4 " + " ".join(f"{mname(k.deg(root, 36))}/32@{70 + 6 * j}" for j in range(8)) for root in prog), gain="-4dB")]
        return out
    kit = rig("drums")
    gtr, kick, snare, cym, stab = [], [], [], [], []
    for i in range(64):
        x = i % 16
        root = prog[(i // 16) % len(prog)]
        rt = k.deg(root, low)
        if kind == "verse":
            hit = x % 4 in (0, 2, 3)
            gtr.append((f"expr.pm=0 {chordhead([rt, rt + 7])}/16@118" if x == 0 else f"expr.pm=1 {mname(t)}/16@{110 if x % 4 == 0 else 100}") if hit else "R/16")
            cym.append(f"{'c' if x == 0 else 'h'}/16@{110 if x == 0 else 80}" if x % 2 == 0 else "R/16")
            stab.append(f"{strings_ch(root)}/16@{96}" if x in (0, 6) else "R/16")
        else:
            gtr.append(f"expr.pm=0 {chordhead([rt, rt + 7, rt + 12])}/16@116" if x == 0 else "_")
            cym.append(f"{'c' if x == 0 else 'rd'}/16@{112 if x == 0 else 88}" if x % 4 == 0 else "R/16")
        kick.append(f"k/16@{110 if x % 4 == 0 else 102}")
        snare.append("s/16@118" if x in (4, 12) else "R/16")
    out = rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr, "/16")), seed=7), track("sub", rig("sub"), jn(mirror_bass(gtr, "/16")), seed=7),
                                    track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym)),
                                    track("choir", pick_patch("choir", "pad"), jn(f"{chordhead([k.deg(root + d, 57) for d in (0, 2, 4)])}/1@{64 if kind == 'verse' else 80}" for root in prog), gain="-8dB")]
    if kind == "verse":
        out.append(track("stabs", pick_patch("strings", "brass-stab"), jn(stab), gain="-6dB"))
    else:
        line = []
        for root in prog:
            d = root + r.choice([4, 7])
            for j in range(8):
                d += r.choice([-1, 1, 1, 2, -2]) if j else 0
                line.append(f"{mname(k.deg(d, 67))}/8@{90 if j % 2 == 0 else 80}")
        out += [track("violins", pick_patch("violins", "strings"), jn(line), gain="-5dB"),
                track("timp", pick_patch("timpani", "tight-kit"), jn(f"{mname(k.deg(root, 36))}/4@{100} R/4 R/2" for root in prog), gain="-5dB")]
    return out


# ---------- breakcore metal (Igorrr / Venetian Snares) ----------------------------------------

def gen_breakcore(r, k, prog, low=28, wild=1.0):
    """Beat-by-beat genre cuts: amen break edits with ratchets, metal chug bursts with double kick
    and china, baroque piano arpeggios over silence, glitch stutters."""
    t = k.deg(0, low)
    bk, mk = pick_patch("break-kit", "metal-kit"), rig("drums")
    tr = {n: [] for n in ("bk", "bs", "bh", "mk", "mc", "gtr", "piano")}
    for beat in range(16):
        mode = r.choices(["break", "chug", "baroque", "stutter"], [3, 2.5 * wild, 1.5, 1.2 * wild])[0]
        root = k.deg(prog[beat // 4], 52)
        for j in range(4):
            def put(**kv):
                for n in tr:
                    tr[n].append(kv.get(n, "R/16"))
            if mode == "break":
                pat = r.choice(["k.s.", ".ks.", "k.sk", "s.ks"])
                c = pat[j]
                put(bk="k/16@118" if c == "k" else "R/16", bs=(f"s/16@{116 if c == 's' else 0}" + ("^r=2" if r.random() < 0.2 else "")) if c == "s" else "R/16",
                    bh=f"h/16@{70 if j % 2 == 0 else 52}")
            elif mode == "chug":
                put(mk=f"k/16@{116 if j % 2 == 0 else 104}", mc="x/16@110" if j == 0 else "R/16",
                    gtr=f"expr.pm={0 if j == 0 else 1} {chordhead([t, t + 7, t + 12]) if j == 0 else mname(t)}/16@{120 if j == 0 else 108}")
            elif mode == "baroque":
                put(piano=f"{mname(k.deg(prog[beat // 4] + [0, 2, 4, 7][j], 60))}/16@{96 if j == 0 else 80}")
            else:
                put(bs=f"s2/16@{100 + j * 5}^r={r.choice([3, 4, 6])}" if j % 2 == 0 else "R/16", bk="k/16@110^r=2" if j == 3 else "R/16")
    jn = lambda xs: " ".join(xs)
    stut = [{"type": "stutter", "slice": "1/32", "repeats": 6, "chance": 0.3, "decay": 0.1, "seed": r.randrange(1000)}]
    out = [track("brk-k", bk, jn(tr["bk"])), track("brk-s", bk, jn(tr["bs"]), fx=stut), track("brk-h", bk, jn(tr["bh"]), pan=0.12),
           track("kick", mk, jn(tr["mk"])), track("cym", mk, jn(tr["mc"])), track("piano", pick_patch("piano", "rhodes"), jn(tr["piano"]), pan=0.2)]
    if any(g != "R/16" for g in tr["gtr"]):
        out += rhythm_tracks(jn(tr["gtr"]), fx=expand(["rack:glitch-stutter"])) + [track("bass", rig("bass"), jn(mirror_bass(tr["gtr"])), seed=7)]
    return out


# ---------- mathcore (Dillinger Escape Plan) ----------------------------------------------------

def gen_swingmetal(r, k, prog, low=28):
    """Swing metal (Intervals / Plini / Thank You Scientist): a jazz rhythm section and heavy guitars at
    once — swung spang-a-lang ride, hat foot on 2 and 4, comping ghost snares, a walking finger bass —
    under distorted double-tracked extended-chord stabs (add9 / maj7 / m9 in an open mid voicing) on the
    Charleston (1 and the and-of-2) with an occasional push on 4."""
    sw = "swing=0.66 "
    kit = rig("drums")
    gtr, bass, kick = [], [], []
    for bi, root in enumerate(prog):
        rt = k.deg(root, low + 12)
        voic = chordhead([rt, k.deg(root + 4, low + 12), k.deg(root + 6, low + 24), k.deg(root + 8, low + 24)])
        push = r.random() < 0.4
        cells = [f"expr.pm=0 {voic}/8@118^gate=0.6", "R/8", "R/8", f"expr.pm=0 {voic}/8@110^gate=0.5", "R/8", "R/8",
                 (f"expr.pm=0 {voic}/8@112^gate=0.4" if push else "R/8"), "R/8"]
        gtr += cells
        kick += ["k/8@112", "R/8", "R/8", "k/8@104", "R/8", "R/8", ("k/8@106" if push else "R/8"), "R/8"]
        nxt = prog[(bi + 1) % len(prog)]
        walk = [root, root + r.choice([1, 2]), root + r.choice([2, 4]), None]
        bass += [f"{mname(k.deg(d, 33))}/4@{84 if j == 0 else 74}" for j, d in enumerate(walk[:3])] + [f"{mname(k.deg(nxt, 33) + r.choice([-1, 1]))}/4@72"]
    ride = " ".join(("rd/8@96" if x % 2 == 0 else ("rd/8@70" if x in (3, 7) else "R/8")) for _ in range(4) for x in range(8))
    hat = " ".join(("hf/4@70" if x % 2 == 1 else "R/4") for _ in range(4) for x in range(4))
    snare = " ".join((f"g/8@{r.choice([26, 32, 40])}" if r.random() < 0.18 else ("s/8@84" if r.random() < 0.05 else "R/8")) for _ in range(32))
    return rhythm_tracks(sw + " ".join(gtr)) + [track("bass", pick_patch("finger-bass", "upright-bass"), " ".join(bass), seed=7),
                                               track("kick", kit, sw + " ".join(kick)), track("ride", kit, sw + ride, gain="-3dB"),
                                               track("hats", kit, hat, gain="-6dB"), track("snare", kit, sw + snare, gain="-3dB")]


def gen_cynic(r, k, prog, low=28, kind="riff"):
    """Tech-death fusion (Cynic / Atheist / Pestilence). riff: tremolo-picked chromatic / diminished
    figures grouped in 7s or 5s over double kick with blast fragments. fusion: the metal drums keep
    going while a fretless bass plays melodic counterpoint and clean jazz voicings (maj7#11 / m9) ring
    over it. clean: chorused clean arpeggios over a soft ride and pad with a singing fretless line."""
    t = k.deg(0, low)
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    if kind == "riff":
        grp = r.choice([7, 5])
        shape = [t + d for d in r.choice([[0, 1, 3, 4, 6, 4, 1], [0, 3, 6, 9, 6, 3, 1], [0, 1, 0, 6, 7, 6, 1]])][:grp]
        gtr, kick, snare, cym = [], [], [], []
        for i in range(64):
            x = i % grp
            blast = (i // 16) == 2
            gtr.append(f"expr.pm={0 if x == 0 else 1} {mname(shape[x] + 12)}/16@{116 if x == 0 else 102}")
            kick.append("k/16@112" if blast and i % 2 == 0 or (not blast) else "R/16")
            snare.append("s/16@116" if (blast and i % 2 == 1) or (not blast and i % 8 == 4) else "R/16")
            cym.append(f"{'c' if x == 0 else ('rd' if i % 2 == 0 else 'R')}/16@{108 if x == 0 else 86}".replace("R/16@86", "R/16"))
        return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr, "/16")), seed=7),
                                         track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn([c_ if not c_.startswith("R") else "R/16" for c_ in cym]))]
    voic = lambda root: chordhead([k.deg(root + d, 55) for d in r.choice([[0, 4, 6, 10], [0, 2, 6, 8], [2, 4, 6, 8]])])
    fret = []
    for root in prog:
        d = root + r.choice([0, 2, 4])
        for ln in r.choice([[2, 1, 1], [1, 1, 2], [3, 1]]):
            fret.append(f"{mname(k.deg(d, 40))}/{ {1: '4', 2: '2', 3: '2.'}[ln] }@{84}")
            d += r.choice([-2, -1, 1, 2])
    fretless = track("fretless", pick_patch("fretless", "finger-bass"), " ".join(fret), seed=7)
    clean = track("clean", pick_patch("clean-chorus", "tele"), " ".join(f"{voic(root)}/2@{74} {voic(root)}/2@{66}" for root in prog), pan=-0.25,
                  fx=[{"type": "delay", "time": "3/16", "feedback": 0.35, "ping_pong": True, "mix": 0.25}, {"type": "reverb", "kind": "hall", "decay": "2.5s", "mix": 0.3}])
    if kind == "fusion":
        kick = jn(("k/16@108" if x in (0, 3, 6, 10) else "R/16") for _ in range(4) for x in range(16))
        snare = jn(("s/16@112" if x in (4, 12) else (f"g/16@{r.choice([28, 34])}" if r.random() < 0.12 else "R/16")) for _ in range(4) for x in range(16))
        cym = jn((f"{'c' if x == 0 else 'rd'}/16@{106 if x == 0 else 80}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16))
        return [clean, fretless, track("kick", kit, kick), track("snare", kit, snare), track("cym", kit, cym)]
    soft = jn(("rd/8@60" if x % 2 == 0 else "rd/8@44") for x in range(32))
    return [clean, fretless, track("ride", kit, "swing=0.62 " + soft, gain="-6dB")] + [dict(t_, name="pad", gain="-12dB") for t_ in gen_pad(r, k, prog, 52, pick_patch("pad-glass", "pad"), vel=56)]


def gen_tigran(r, k, prog, kind="groove"):
    """Tigran Hamasyan (Mockroot): a jazz piano trio as heavy as metal, no guitars. groove: piano
    left-hand octaves and right-hand chords on the accents of a 5/7/9-step polymetric cycle against
    the 4/4, a synth bass doubling the accents, drums locked to them (kick on accents, half-time snare
    on 3); folk: an ornamented phrygian-dominant piano melody over a drone, rim and toms; heavy: the
    groove plus a distorted synth bass and crash on every cycle restart."""
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    t = k.deg(0, 36)
    if kind == "folk":
        mel, d = [], r.choice([0, 2, 4])
        for root in prog:
            for ln in r.choice([[2, 1, 1], [1, 1, 2], [1, 2, 1]]):
                if r.random() < 0.4:
                    mel.append(f"{mname(k.deg(d + 1, 67))}/16@{70}^h")
                    mel.append(f"{mname(k.deg(d, 67))}/{ {1: '8.', 2: '4..'}.get(ln, '8.') }@{84}" if ln in (1, 2) else f"{mname(k.deg(d, 67))}/4@84")
                else:
                    mel.append(f"{mname(k.deg(d, 67))}/{ {1: '4', 2: '2'}[ln] }@{84}")
                d += r.choice([-2, -1, 1, 2])
        return [track("piano", "piano", jn(mel), pan=0.1), track("drone", "piano", jn(f"{chordhead([t, t + 7])}/1@{60}" for _ in prog), pan=-0.2, gain="-6dB"),
                track("rim", kit, jn(("rs/16@70" if x in (4, 12) else (r.choice(["t2", "t3", "ft"]) + "/16@60" if x in (14, 15) and r.random() < 0.5 else "R/16")) for _ in range(4) for x in range(16)), gain="-6dB")]
    cyc = r.choice([5, 7, 9])
    acc = sorted(set([0] + r.sample(range(1, cyc), r.choice([1, 2]))))
    lh, rh, bass, kick, snare, cym = [], [], [], [], [], []
    for i in range(64):
        x = i % cyc
        root = prog[(i // 16) % len(prog)]
        rt = k.deg(root, 36)
        hit = x in acc
        lh.append(f"{chordhead([rt, rt + 12])}/16@{96 if x == 0 else 86}" if hit else "R/16")
        rh.append(f"{chordhead([k.deg(root + d, 60) for d in (2, 4, 6)])}/16@{90}" if hit and x == 0 else "R/16")
        bass.append(f"{mname(rt - 12)}/16@{104}" if hit else "R/16")
        kick.append("k/16@112" if hit else "R/16")
        snare.append("s/16@116" if i % 16 == 8 else ("g/16@30" if r.random() < 0.1 else "R/16"))
        cym.append(("c/16@108" if x == 0 and kind == "heavy" else "h/16@70") if i % 4 == 0 else "R/16")
    sb = pick_patch("bass-fuzz", "growl") if kind == "heavy" else pick_patch("moog-seq", "sub-sine")
    return [track("piano-lh", "piano", jn(lh), pan=-0.15), track("piano-rh", "piano", jn(rh), pan=0.15),
            track("synthbass", sb, jn(bass), seed=7, gain="-5dB" if kind == "heavy" else "-7dB"),
            track("kick", kit, jn(kick), gain="-3dB"), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


def gen_mahavishnu(r, k, prog, meter=7, low=28, kind="riff"):
    """Mahavishnu Orchestra: a unison riff in 7/8, 9/8 or 11/8 (8ths) on distorted guitar and electric
    violin an octave apart, a Hammond comping on the group starts, busy Cobham drums in the meter (kick and
    snare on the groupings, toms filling the last group, crash each cycle), bass doubling the riff.
    kind=solo drops the violin from the riff (it solos) and thins the Hammond."""
    groups = {7: [2, 2, 3], 9: [2, 2, 2, 3], 11: [3, 3, 3, 2]}[meter]
    starts, pos = [], 0
    for g in groups:
        starts.append(pos); pos += g
    t = k.deg(0, low + 12)
    cell = [t + d for d in r.choice([[0, 1, 3, 5, 6, 3, 1, 0, 7, 6, 5], [0, 3, 5, 6, 5, 3, 0, 10, 12, 10, 7], [0, 2, 3, 5, 7, 8, 7, 5, 3, 2, 0]])][:meter]
    reps = 4
    gtr, vln, bass, organ, kick, snare, cym = [], [], [], [], [], [], []
    for rep_ in range(reps):
        root = prog[rep_ % len(prog)]
        shift = k.deg(root, low + 12) - k.deg(0, low + 12)
        for x in range(meter):
            n = cell[x] + shift
            acc = x in starts
            gtr.append(f"expr.pm=0 {mname(n)}/8@{106 if acc else 98}")
            vln.append(f"{mname(n + 24)}/8@{100 if acc else 86}")
            bass.append(f"{mname(n - 12)}/8@{100 if acc else 88}")
            organ.append(f"{chordhead([k.deg(root + d, 55) for d in (0, 2, 4, 6)])}/8@{78}^gate=0.6" if acc and (kind != "solo" or x == 0) else "R/8")
            last = x >= starts[-1]
            kick.append("k/8@108" if acc else ("k/8@90" if r.random() < 0.25 else "R/8"))
            snare.append((r.choice(["t1", "t2", "t3", "ft"]) + "/8@100") if last and rep_ == reps - 1 else ("s/8@108" if x == starts[1] else ("g/8@34" if r.random() < 0.2 else "R/8")))
            cym.append("c/8@110" if x == 0 else ("rd/8@88" if not last else "R/8"))
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    out = rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(bass), seed=7, gain="-3dB"), track("organ", pick_patch("hammond-b3", "organ"), jn(organ), pan=-0.2, gain="-8dB"),
                                    track("kick", kit, jn(kick), gain="-2dB"), track("snare", kit, jn(snare)), track("cym", kit, jn(cym), gain="-5dB")]
    if kind != "solo":
        out.append(track("violin", pick_patch("violins", "strings"), jn(vln), pan=0.25, gain="-13dB", fx=[{"type": "drive", "drive": 0.25}]))
    return out


def gen_drumsolo(r, beats=8):
    """A fusion drum break on the metal kit: four-beat phrases, each a linear kick / snare / tom figure,
    a descending tom run, a snare roll in 32nd pairs or double-kick bursts under snare accents; a crash
    to open, landing on the last beat."""
    toks = ["c/16@112"]
    used = 1
    while used < beats * 4:
        left = beats * 4 - used
        idea = r.choice(["linear", "toms", "roll", "dkick"])
        n = min(left, 16 - (used % 16) if used % 16 else 16)
        for j in range(n):
            if idea == "linear":
                toks.append(f"{['k', 's', 't1', 'k', 't2', 's', 'ft', 'k'][j % 8]}/16@{r.choice([92, 100, 108])}")
            elif idea == "toms":
                toks.append(f"{['t1', 't1', 't2', 't2', 't3', 't3', 'ft', 'ft'][(j // 2) % 8 if j < 16 else 7]}/16@{100 + (j % 2) * 6}")
            elif idea == "roll":
                toks.append(f"s/32@{60 + j * 3 if j < 16 else 100} s/32@{64 + j * 3 if j < 16 else 104}")
            else:
                toks.append(f"{'s' if j % 4 == 2 else 'k'}/16@{110 if j % 4 == 2 else 96}")
        used += n
    toks[-1] = "c/16@116"
    return [track("drumsolo", rig("drums"), " ".join(toks))]


def gen_coltrane(r, k, prog, low=28):
    """Coltrane changes (Giant Steps) as a fusion guest: the tonic moving by major thirds, each new key
    approached from its dominant seventh (I · V7/III · III · V7/bVI · bVI · V7 · I …), eight chords in
    16 beats; Rhodes comping, a walking bass with chromatic approaches, a swung ride with hat foot and a
    tenor sax playing 1-2-3-5 patterns through the changes. Absolute pitches from the song's tonic."""
    t = k.deg(0, 48) % 12 + 48
    # (root offset, quality): maj7 tonics a major third apart, each preceded by its V7
    seq = [(0, "maj7"), (11, "7"), (4, "maj7"), (3, "7"), (8, "maj7"), (7, "7"), (0, "maj7"), (11, "7")]  # B7→E, Eb7→Ab, G7→C
    shapes = {"maj7": (0, 4, 7, 11), "7": (0, 4, 7, 10)}
    sw = "swing=0.66 "
    keys, bass, sax = [], [], []
    for j, (ro, q) in enumerate(seq):
        root = t + ro
        keys.append(f"{chordhead([root + i for i in shapes[q]])}/4@{70} {chordhead([root + i for i in shapes[q]])}/8@{60}^gate=0.5 R/8")
        nxt = t + seq[(j + 1) % len(seq)][0]
        bass.append(f"{mname(root - 24)}/4@{82} {mname(nxt - 24 + r.choice([-1, 1]))}/4@{72}")
        sax.append(" ".join(f"{mname(root + 12 + i)}/8@{88 if n == 0 else 80}" for n, i in enumerate((0, 2, 4, 7))))  # the 1-2-3-5 pattern
    kit = rig("drums")
    ride = " ".join(("rd/8@90" if x % 2 == 0 else ("rd/8@66" if x in (3, 7) else "R/8")) for _ in range(4) for x in range(8))
    hat = " ".join(("hf/4@64" if x % 2 == 1 else "R/4") for _ in range(4) for x in range(4))
    return [track("rhodes", pick_patch("rhodes", "piano"), sw + " ".join(keys), pan=-0.2),
            track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(bass), seed=7),
            track("ride", kit, sw + ride, gain="-4dB"), track("hats", kit, hat, gain="-6dB"),
            track("sax", pick_patch("tenor-sax", "synth-lead"), sw + " ".join(sax), pan=0.2)]


def gen_mathcore(r, k, prog, low=28, kind="chaos"):
    """chaos: the 16-beat part cut into odd-length chunks (3–13 sixteenths, summing to 64); each a
    cluster stab into a hard stop, a dissonant tremolo run, chugs over a blast fragment or silence;
    crash/china + kick on every chunk start, blasts inside blast chunks, toms in short chunks.
    jazz: lounge breaks — jazz-box maj7#11 / m9 / 7#9 voicings in odd placements over brushes."""
    t = k.deg(0, low)
    if kind == "jazz":
        kit = pick_patch("brush-kit", "metal-kit")
        gtr, ride, snare = [], [], []
        for bar, root in enumerate(prog):
            rt = k.deg(root, 50)
            voicing = r.choice([[0, 4, 11, 18], [0, 3, 10, 14], [0, 4, 10, 15], [0, 7, 11, 14]])
            hits = sorted(r.sample(range(16), r.choice([2, 3])))
            for x in range(16):
                gtr.append(f"{chordhead([rt + v for v in voicing])}/16@{r.choice([70, 78, 86])}^gate=2" if x in hits else "R/16")
                ride.append(f"rd/16@{70 if x % 4 == 0 else 56}" if x % 4 in (0, 3) else "R/16")
                snare.append(f"s/16@{r.choice([28, 34])}" if r.random() < 0.15 else "R/16")  # brushed ghosts (brush-kit has no g)
        jn = lambda xs: " ".join(xs)
        return [track("gtr", pick_patch("jazz-box", "clean-chorus"), jn(gtr), pan=0.15), track("ride", kit, jn(ride)), track("snare", kit, jn(snare)),
                track("bass", pick_patch("upright-bass", "finger-bass", "bass-di"), " ".join(f"{mname(k.deg(root + d, 33))}/4@{84}" for root in prog for d in (0, 2, 4, 6)), seed=7)]
    sizes, total = [], 0
    while total < 64:
        sz = min(r.choice([3, 5, 7, 7, 9, 9, 11, 13]), 64 - total)
        sizes.append(sz); total += sz
    clusters = [[t, t + 1, t + 6], [t + 1, t + 7, t + 13], [t, t + 6, t + 11], [t + 12, t + 13, t + 18]]
    gtr, kick, snare, cym = [], [], [], []
    for sz in sizes:
        cell = r.choice(["stab", "trem", "blast", "stab", "stop"])
        for j in range(sz):
            first = j == 0
            if cell == "stab":
                gtr.append(f"expr.pm=0 {chordhead(r.choice(clusters))}/16@124^gate=0.7" if first else "R/16")
            elif cell == "trem":
                gtr.append(f"expr.pm=0 {mname(t + 12 + r.choice([0, 1, 3, 6, 7, 11]))}/16@{106 if j % 2 == 0 else 94}")
            elif cell == "blast":
                gtr.append(f"expr.pm={0 if first else 1} {chordhead([t, t + 7]) if first else mname(t)}/16@{120 if first else 106}")
            else:
                gtr.append(f"expr.pm=0 {chordhead(r.choice(clusters))}/16@122^gate=0.4" if first else "R/16")
            kick.append("k/16@120" if first else ("k/16@108" if cell == "blast" and j % 2 == 0 else "R/16"))
            snare.append("R/16" if first else ("s/16@108" if cell == "blast" and j % 2 == 1 else
                         (f"{['t1', 't2', 't3', 'ft'][j % 4]}/16@{100 + j}" if sz <= 5 and cell != "stop" else "R/16")))
            cym.append(f"{r.choice(['x', 'c', 'st', 'cch'])}/16@118" if first else ("rd/16@84" if cell in ("blast", "trem") and j % 2 == 0 else "R/16"))
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    return rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr)), seed=7), track("sub", rig("sub"), jn(mirror_bass(gtr)), seed=7),
            track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- Gojira ------------------------------------------------------------------------------

def gen_gojira(r, k, prog, low=28, kind="groove"):
    """groove: 4/4 chugs with gaps, power/tritone accents, kick on the riff, china accents;
    whammy: the riff through a pitch shifter whose interval is automated (unison / octave / fifth
    jumps every two beats, a la DigiTech Whammy); tribal: toms carry the beat (Duplantier) under
    sparse chugs; harmonic: ringing natural harmonics diving via bends over sparse drums."""
    t = k.deg(0, low)
    cell = [r.random() < 0.6 for _ in range(16)]
    cell[0] = True
    gtr, kick, snare, cym = [], [], [], []
    dive = 0
    for i in range(64):
        x = i % 16
        if kind in ("groove", "whammy"):
            if cell[x]:
                acc = x in (0, 6, 10) or r.random() < 0.15
                ch = r.choice([[t, t + 7, t + 12], [t, t + 6], [t + 1, t + 8]]) if acc else [t]
                gtr.append(f"expr.pm={0 if acc else 1} {chordhead(ch)}/16@{120 if acc else 104}" + ("^gate=0.9" if acc else ""))
            else:
                gtr.append("R/16")
            kick.append("k/16@114" if cell[x] else "R/16")
            snare.append("s/16@118" if x in (4, 12) else (f"g/16@{r.choice([30, 38])}" if r.random() < 0.12 else "R/16"))
            cym.append("x/16@114" if x == 0 else (f"{'rds' if x % 8 == 4 else 'rd'}/16@86" if x % 4 == 0 else "R/16"))
        elif kind == "tribal":
            toms = r.choice(["t1", "t2", "t3", "ft"])
            gtr.append(f"expr.pm=0 {chordhead([t, t + 7, t + 12])}/16@120^gate=1.2" if x in (0, 10) else ("R/16"))
            kick.append("k/16@116" if x % 4 == 0 or x in (6, 14) else "R/16")
            snare.append(f"{toms}/16@{100 + (x % 4) * 4}" if x % 2 == 1 or x in (2, 6) else ("s/16@118" if x == 12 else "R/16"))
            cym.append("x/16@112" if x == 0 else ("rb/16@80" if x % 4 == 0 else "R/16"))
        else:  # harmonic
            if dive:
                gtr.append(["bend=-2 _", "bend=-5 _", "bend=-12 _ bend="][3 - dive]); dive -= 1
            elif x % 8 == 0:
                if r.random() < 0.4 and x + 3 < 16:
                    gtr.append(f"{mname(t + 12)}/16@116^nh={r.choice([2, 3, 4])}"); dive = 3
                else:
                    gtr.append(f"{mname(t + 12)}/16@112^nh={r.choice([2, 3, 4])}^gate=4")
            else:
                gtr.append("R/16")
            kick.append("k,ft/16@110" if x == 0 else "R/16")
            snare.append("s/16@112" if x == 8 else "R/16")
            cym.append("rde/16@80" if x % 4 == 0 else "R/16")
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    fx = None
    if kind == "whammy":
        pts, ivs = [], [0, 12, 0, 7, 0, 12, 7, 0]
        for b in range(8):
            v = ivs[b] / 12
            pts += [[f"{b * 2:g}b", v], [f"{b * 2 + 1.95:g}b", v]]
        fx = [{"type": "pitch", "grain": "35ms", "mix": 1.0, "semitones": {"value": 0, "mod": [{"src": "auto.wh", "amount": 12}]}}]
    gt = rhythm_tracks(jn(gtr), fx=fx)
    if kind == "whammy":
        gt = [dict(t2, auto={"wh": {"points": pts}}) for t2 in gt]
    return gt + [track("bass", rig("bass"), jn(mirror_bass(gtr)), seed=7), track("sub", rig("sub"), jn(mirror_bass(gtr)), seed=7),
                 track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("cym", kit, jn(cym))]


# ---------- world x metal: raga, gamelan, koto ---------------------------------------------------

def gen_tabla(r, kind="teental"):
    """Tabla bols on a 16th grid over 16 beats: teental (8th bols), tirakita runs, or a sparse groove."""
    kit = pick_patch("tabla-kit", "metal-kit")
    teental = "dha dhin dhin dha dha dhin dhin dha dha tin tin na na dhin dhin dha".split()
    out = []
    for beat in range(16):
        if kind == "teental":
            b = teental[(beat * 2) % 16], teental[(beat * 2 + 1) % 16]
            out += [f"{b[0]}/16@100", "R/16", f"{b[1]}/16@{88}", "R/16"]
        elif kind == "tirakita":
            out += [f"{x}/16@{v}" for x, v in zip(r.choice([["te", "re", "ke", "te"], ["dha", "te", "re", "ke"], ["na", "tin", "na", "ge"]]), [96, 80, 86, 82])]
        else:
            out += [f"{r.choice(['ge', 'na', 'dha', 'tin'])}/16@{94}" if j == 0 or r.random() < 0.3 else "R/16" for j in range(4)]
    return [track("tabla", kit, " ".join(out), pan=-0.2)]


def gen_raga(r, k, prog, kind="alap"):
    """alap: tanpura cycle (Pa Sa Sa Sa) and a slow sitar line with meend bends; groove: tabla + tanpura."""
    sa = k.deg(0, 48)
    tanpura = [track("tanpura", pick_patch("tanpura", "drone"), " ".join([f"{mname(sa + 7)}/4@70 {mname(sa + 12)}/4@66 {mname(sa + 12)}/4@66 {mname(sa)}/4@72"] * 4), gain="-4dB")]
    if kind == "groove":
        return tanpura + gen_tabla(r, r.choice(["teental", "tirakita"]))
    line, t = [], 0
    while t < 16:
        ln = min(16 - t, r.choice([2, 3, 4]))
        m = k.deg(r.choice([0, 1, 2, 4, 5, 7]), 60)
        line.append(f"{mname(m)}/4@{r.choice([86, 94])}" + ("".join(" _" for _ in range(ln - 1)) if ln > 1 else ""))
        if ln >= 3 and r.random() < 0.5:
            line[-1] = f"{mname(m)}/4@90 _ bend=1 _ bend=" + "".join(" _" for _ in range(ln - 3))
        t += ln
    return tanpura + [track("sitar", pick_patch("sitar", "nylon"), " ".join(line), pan=0.15)]


def gen_dawnraga(r, k, prog, kind="alap"):
    """A morning raga in the classical arc. alap: tanpura + a free sitar line with meend glides over a
    soft harmonium drone; jor: a pulsing sitar (Sa on the beat, melodic figures between); gat:
    soft teental tabla, harmonium chords and the sitar melody (the hook)."""
    sa = k.deg(0, 48)
    harm = track("harmonium", pick_patch("harmonium", "organ"), " ".join(f"{chordhead([sa, sa + 7, sa + 12])}/1@{56}" for _ in range(4)), gain="-6dB", pan=-0.2)
    if kind == "alap":
        return gen_raga(r, k, prog, "alap") + [harm]
    tanpura = [t for t in gen_raga(r, k, prog, "alap") if t["name"] == "tanpura"]
    if kind == "jor":
        line = []
        for j in range(32):
            if j % 2 == 0:
                line.append(f"{mname(sa + 12)}/8@{r.choice([72, 78])}")
            else:
                line.append(f"{mname(k.deg(r.choice([1, 2, 4, 5, 7]), 60))}/8@{r.choice([82, 88])}" if r.random() < 0.6 else f"{mname(sa + 12)}/8@{64}")
        return tanpura + [track("sitar", pick_patch("sitar", "nylon"), " ".join(line), pan=0.15)]
    tabla = [dict(t, gain="-5dB") for t in gen_tabla(r, "teental")]
    return tanpura + tabla + [track("harmonium", pick_patch("harmonium", "organ"),
                                    " ".join(f"{chordhead([k.deg(root, 48), k.deg(root + 2, 48), k.deg(root + 4, 48)])}/2@{58} R/2" for root in prog), gain="-8dB", pan=-0.2)]


def gen_kotekan(r, k, prog):
    """Gamelan kotekan: polos and sangsih interlock on alternate 16ths from a repeating degree cell,
    a gong (low tubular bell) on every bar."""
    cell = [r.choice([0, 1, 2, 3, 4]) for _ in range(8)]
    polos, sang, gong = [], [], []
    for i in range(64):
        d = cell[i % 8] + prog[i // 16]
        if i % 2 == 0:
            polos.append(f"{mname(k.deg(d, 72))}/16@{96 if i % 4 == 0 else 84}"); sang.append("R/16")
        else:
            sang.append(f"{mname(k.deg(d + 2, 72))}/16@{88}"); polos.append("R/16")
    gong = [f"{mname(k.deg(root, 36))}/1@96" for root in prog]  # one gong stroke per bar, ringing the bar
    g = pick_patch("gamelan", "vibes")
    return [track("polos", g, " ".join(polos), pan=-0.3), track("sangsih", g, " ".join(sang), pan=0.3),
            track("gong", pick_patch("tubular-bells", "gamelan"), " ".join(gong), gain="-6dB")]


def gen_koto(r, k, prog, kind="arp"):
    """Koto: hirajoshi arpeggios (with sararin tremolo on long notes); taiko thunder on floor toms
    and kick (kind=taiko)."""
    if kind == "taiko":
        kit = rig("drums")
        pat = r.choice(["x..x..x.x.x.xxx.", "x...x.x.x..xx.x.", "x.x..x.xx..x.x.."])
        toms = " ".join((f"{r.choice(['ft', 'ft2', 't3'])}/16@{116 if x % 4 == 0 else 104}" if pat[x] == "x" else "R/16") for _ in range(4) for x in range(16))
        kick = " ".join(("k/16@118" if x in (0, 8) else "R/16") for _ in range(4) for x in range(16))
        return [track("taiko", kit, toms), track("taiko-k", kit, kick)]
    out = []
    for root in prog:
        if r.random() < 0.3:
            out.append(f"{mname(k.deg(root + 4, 60))}/2@{90}^r=8 {mname(k.deg(root + 2, 60))}/2@86^r=8")
        else:
            out += [f"{mname(k.deg(root + d, 60))}/16@{96 if j % 4 == 0 else 80}" for j, d in enumerate([0, 1, 2, 4, 2, 1, 0, 2] * 2)]
    return [track("koto", pick_patch("koto", "nylon"), " ".join(out), pan=0.2)]


# ---------- groove metal --------------------------------------------------------------------

def gen_groovemetal(r, k, prog, low=28, kind="groove"):
    """Pantera / Lamb of God: swung 16ths (swing16) — blues-scale riffs with b5 passing notes,
    hammer-ons, pinch squeals and stops, the kick following the riff and a double-kick fill at the
    phrase end (kind=groove); gallop choruses (gallop); half-time breakdown (half)."""
    t = k.deg(0, low)
    blues = [0, 3, 5, 6, 7, 10, 12]
    cell = [r.choice(blues + [0, 0, 0]) if r.random() < 0.75 else None for _ in range(16)]
    cell[0] = 0
    gtr, kick, snare, cym = [], [], [], []
    for i in range(64):
        x = i % 16
        bar = i // 16
        if kind == "gallop":
            if x % 4 in (0, 2, 3):
                g = f"expr.pm={0 if x == 0 else 1} {chordhead([t, t + 7]) if x == 0 else mname(t)}/16@{120 if x == 0 else 104}"
            else:
                g = "R/16"
            kick.append("k/16@114" if x % 4 in (0, 2, 3) else "R/16")
        elif kind == "half":
            g = f"expr.pm=0 {chordhead([t, t + 7, t + 12])}/16@124^gate=2" if x in (0, 7, 10) else "R/16"
            kick.append("k/16@120" if x in (0, 7, 10) else "R/16")
        else:
            iv = cell[x]
            if iv is None:
                g = "R/16"
            else:
                m = t + iv + (12 if bar == 3 and x > 11 and iv < 7 else 0)
                art = "^ph" if (iv in (6, 10, 12) and r.random() < 0.35) else ("^h" if x % 2 == 1 and r.random() < 0.3 else "")
                pm = 1 if iv == 0 else 0
                g = f"expr.pm={pm} {mname(m)}/16@{118 if x == 0 else 106}{art}"
            kick.append(("k/16@112" if iv is not None and (iv == 0 or x % 4 == 0) else "R/16") if not (bar == 3 and x >= 12) else "k/16@116^r=2")
        gtr.append(g)
        back = x in (8,) if kind == "half" else x in (4, 12)
        snare.append(f"{r.choice(['s', 's', 'sc'])}/16@118" if back else (f"g/16@{r.choice([30, 38])}" if r.random() < 0.12 else "R/16"))
        cym.append((f"{r.choice(['x', 'c'])}/16@112" if x == 0 and bar % 2 == 0 else f"{r.choice(['rd', 'rds', 'h2'])}/16@{88 if x % 4 == 0 else 74}") if x % 2 == 0 else "R/16")
    kit = rig("drums")
    jn = lambda xs: " ".join(xs)
    sw = "swing16=0.58 " if kind == "groove" else ""
    gt = rhythm_tracks(sw + jn(gtr))
    return gt + [track("bass", rig("bass"), sw + jn(mirror_bass(gtr)), seed=7), track("sub", rig("sub"), sw + jn(mirror_bass(gtr)), seed=7),
                 track("kick", kit, sw + jn(kick)), track("snare", kit, sw + jn(snare)), track("cym", kit, sw + jn(cym))]


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
    return rhythm_tracks(jn(gtr)) + [track("bass", pick_patch("slap-bass", "pick-bass", "bass-fat"), jn(bass), seed=7, gain="-4dB"),
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
    out = [track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("clap", pick_patch("electro-kit", "909"), jn(clap), gain="-3dB")]
    if kind != "verse":
        out += rhythm_tracks(jn(gtr)) + [track("bass", rig("bass"), jn(mirror_bass(gtr)), seed=7)]
    else:
        out += [dict(t, gain="-8dB") for t in gen_bassline(r, k, prog, 33, pick_patch("808-dist", "acid"))]
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


SCAPES = {"wind": ("wind", "C5", "-6dB"), "shortwave": ("shortwave", "A4", "-8dB"), "hum": ("shortwave", "E4", "-10dB"),
          "rain": ("rain", "C5", "-4dB"), "waterphone": ("waterphone", "E5", "-14dB")}
SCAPE_STYLES = {"backrooms": ["shortwave", "hum", "wind", "waterphone"], "cyberscape": ["shortwave", "wind", "waterphone"], "ambient": ["wind", "rain", "waterphone"],
                "celtic": ["wind", "rain"], "slowcore": ["wind", "rain"], "doomjazz": ["wind", "shortwave", "waterphone", "rain"], "guofeng": ["wind", "rain"], "mali": ["wind"],
                "satie": ["rain", "rain", "wind"], "balearic": ["wind"], "hauntology": ["shortwave", "wind", "rain"], "kankyo": ["rain", "wind", "rain"], "handpan": ["wind", "rain"], "lofihop": ["rain"], "neoclassical": ["rain", "wind"], "triphop": ["rain", "shortwave"]}


def scape(style, role, beats, seed):
    """A held scape layer (wind / shortwave) for some chill riff parts, or None."""
    import zlib
    r = random.Random(zlib.crc32(f"{seed}{role}".encode()))
    pool = SCAPE_STYLES.get(style, ["wind", "shortwave"])
    if r.random() > (0.6 if style in SCAPE_STYLES else 0.25) or abs(beats - round(beats)) > 1e-9:
        return None
    patch, note, gain = SCAPES[r.choice(pool)]
    if not have(patch):
        return None
    return track("scape", patch, f"{note}/4" + " _" * (int(round(beats)) - 1), gain=gain, pan=round(r.uniform(-0.5, 0.5), 2))


FEEL_LATE = {"s", "rs", "rc", "cp", "ss", "sc", "so", "se", "g", "sl"}
FEEL_DRIFT = {"h", "hs", "h1", "h2", "h3", "oh", "hf", "hp", "hh", "rd", "rds", "rde", "rb", "shk", "sh", "tamb", "t"}


def feel_track(t, profile, r):
    """Re-time a 16th-grid kit track per feel profile (kick on the grid, backbeats late, hats
    drifting) using drunk(); tracks not purely on the 16th grid are returned unchanged."""
    p = t.get("patch", "")
    if profile == "tight" or not ("kit" in p or p in ("djembe", "bodhran")):
        return t
    toks = t["score"].split()
    pre = []
    while toks and "=" in toks[0] and "/" not in toks[0]:
        pre.append(toks.pop(0))
    slots = []
    for tok in toks:
        m = re.match(r"^([A-Za-z][A-Za-z0-9]*)/16(@\d+)?$", tok)
        if tok == "R/16":
            slots.append((None, 0))
        elif m and m.group(1) != "R":
            piece = m.group(1)
            late = {"laid": [1, 1, 2], "drunk": [1, 2, 2, 3]}[profile]
            drift = {"laid": [0, 0, 1], "drunk": [0, 1, 1, 2]}[profile]
            slots.append((tok, r.choice(late) if piece in FEEL_LATE else r.choice(drift) if piece in FEEL_DRIFT else 0))
        else:
            return t
    return dict(t, score=" ".join(pre + [drunk(slots)]))


_KEY = (0, "minor")
_CHAPTER = 0
_TEMPO = 100
FUSION = False  # set by the evolver in the fusion-metal journey
LITE = False  # set by the evolver when the groove's render load is high: skip optional layers
VOX_CHOPS = {"house-melodic": 0.6, "cyberscape": 0.5, "fusion": 0.3, "dnb": 0.5, "brostep": 0.4, "garage": 0.6, "house": 0.5, "darksynth": 0.3}
ORCH_HITS = {"darksynth": 0.5, "industrial": 0.4, "power": 0.5, "deathcore": 0.4, "numetal": 0.3, "brostep": 0.3}
MINORISH = {"minor", "dorian", "phrygian", "harmonic", "locrian", "melodic", "blues", "pentatonic-minor", "neapolitan", "hungarian", "phrygian-dominant"}


def _tr_to_minor():
    """Semitones that move a C-minor library part to the current song's minor colour (relative minor
    for major-ish modes), folded into −6…+5."""
    pc, mode = _KEY
    t = (pc + (0 if mode in MINORISH else 9)) % 12
    return t - 12 if t > 5 else t


def stock_layers(style, parts, beats, seed):
    """Layer the engine's @vox-chops / @orch-hit into one non-intro riff part (deterministic per song)."""
    import zlib
    r = random.Random(zlib.crc32(f"stock{seed}".encode()))
    roles = [ro for ro in ("riffB", "riffD", "riffDrop", "riffF", "riff") if ro in parts and abs((beats or {}).get(ro, 16) - 16) < 1e-9]
    if not roles:
        return
    tr = _tr_to_minor()
    if r.random() < VOX_CHOPS.get(style, 0):
        parts[roles[0]] = parts[roles[0]] + [{"name": "chops", "score": f"tr={tr} @vox-chops @vox-chops", "gain": "-3dB"}]
    if r.random() < ORCH_HITS.get(style, 0):
        parts[roles[0]] = parts[roles[0]] + [{"name": "orch", "score": f"tr={tr} @orch-hit R/1 @orch-hit R/1", "gain": "-4dB"}]


FAMILIES = [
    ["rhodes", "wurli", "rhodes-rotary", "dx-epiano", "tape-piano", "hammond-b3"],
    ["vibes", "marimba", "celesta", "music-box", "glock", "kalimba", "toy-piano"],
    ["flute", "dizi", "low-whistle", "shakuhachi", "mellotron-flute", "clarinet"],
    ["tenor-sax", "trumpet-mute", "melodica", "horn-section", "trombone"],
    ["pad-glass", "juno-pad", "mellotron-strings", "mellotron-choir"],
    ["piano", "tape-piano"],
    ["nylon", "acoustic"],
    ["finger-bass", "fretless", "upright-bass"],
    ["tuba", "upright-bass"],
]


def swap_plan(desc):
    """Per song: each instrument family swaps to a sibling with p=0.35 (deterministic from the song)."""
    import zlib
    plan = {}
    for i, fam in enumerate(FAMILIES):
        r = random.Random(zlib.crc32(f"swap{i}{desc}".encode()))
        if r.random() < 0.35:
            for src in fam:
                opts = [d for d in fam if d != src and have(d)]
                if opts:
                    plan.setdefault(src, r.choice(opts))
    return plan


def drum_enrich(t, r):
    """Heavy kits: soft ghost snares in isolated 16th rests (12%), hat strokes varied across
    h/h1/h2/h3 (~30%), ride hits moved to the shank (~25%). Plain 16th tokens only."""
    p = t.get("patch", "")
    name = t.get("name", "")
    if p not in ("metal-kit", "metal-kit-dry", "prog-kit") or not any(w in name for w in ("snare", "cym", "hat")):
        return t
    toks = t["score"].split()
    pre = []
    while toks and "=" in toks[0] and "/" not in toks[0]:
        pre.append(toks.pop(0))
    out = []
    ghost_p = 0.2 if FUSION else 0.12
    cycle = r.choice([3, 5]) if FUSION and ("cym" in name or "hat" in name) else None
    step = 0
    for i, tok in enumerate(toks):
        if cycle:  # polyrhythmic accents across a 16th hat / ride stream (3s or 5s against the 4/4)
            m16 = re.match(r"^(h|h1|h2|h3|rd|rds)/16@(\d+)$", tok)
            if m16:
                v = int(m16.group(2))
                tok = f"{m16.group(1)}/16@{min(127, v + 22) if step % cycle == 0 else max(30, v - 12)}"
            if re.match(r"^[A-Za-z]+[0-9]?/16", tok) or tok == "R/16":
                step += 1
        if "snare" in name and tok == "R/16" and 0 < i < len(toks) - 1 and toks[i - 1] == "R/16" and toks[i + 1] == "R/16" and r.random() < ghost_p:
            out.append(f"g/16@{r.choice([24, 28, 32, 38])}")
            continue
        m = re.match(r"^(h|rd)/(8|16)(@\d+)?$", tok)
        if m and m.group(1) == "h" and r.random() < 0.3:
            out.append(r.choice(["h1", "h2", "h3"]) + tok[1:]); continue
        if m and m.group(1) == "rd" and r.random() < 0.25:
            out.append("rds" + tok[2:]); continue
        out.append(tok)
    return dict(t, score=" ".join(pre + out))


def poly_lead(r, k, patch, cycle, base=64, steps=64):
    """A polymetric lead: a 5- or 7-step motif (16ths) from the mode, repeated against the 4/4 so it
    realigns with the bar only every `cycle` bars; accents on each cycle start, rests inside."""
    motif = []
    d = r.choice([0, 2, 4])
    for j in range(cycle):
        if j and r.random() < 0.2:
            motif.append(None)
        else:
            motif.append(d)
            d += r.choice([-2, -1, 1, 2, 3])
    toks = [(f"{mname(k.deg(motif[i % cycle], base))}/16@{104 if i % cycle == 0 else 88}" if motif[i % cycle] is not None else "R/16") for i in range(steps)]
    return [track("hook", patch, " ".join(toks), pan=0.1)]


def fusion_layers(style, parts, beats, desc):
    """Fusion journey, heavy songs: a polyrhythmic overlay (a 3/5/7-step motif of extended chord tones
    on vibes / DX bell / pluck / marimba cycling against the 4/4) on a main riff section, and jazz
    chord stabs (m11 / maj7#11 on Rhodes / vibes / Wurlitzer) on the downbeats under breakdowns."""
    import zlib
    r = random.Random(zlib.crc32(f"fusion{desc}".encode()))
    k = Key(*_KEY)
    if "hook" in parts and abs((beats or {}).get("hook", 16) - 16) < 1e-9 and r.random() < 0.5:
        lead_patch = next((t.get("patch") for t in parts["hook"] if t.get("patch")), rig("lead"))
        parts["hook"] = poly_lead(r, k, lead_patch, r.choice([5, 7]))
    is16 = lambda ro: abs((beats or {}).get(ro, 16) - 16) < 1e-9
    host = next((ro for ro in ("riffB", "riffC", "riffV", "riff") if ro in parts and is16(ro)), None)
    if host:
        cyc = r.choice([3, 5, 7])
        motif = [k.deg(r.choice([1, 3, 5, 6, 8, 10, 12]), 72) if r.random() < 0.8 else None for _ in range(cyc)]
        line = " ".join((f"{mname(motif[i % cyc])}/16@{r.choice([70, 78, 86])}" if motif[i % cyc] is not None else "R/16") for i in range(64))
        parts[host] = parts[host] + [track("polyline", pick_patch(r.choice(["vibes", "dx-epiano", "pluck-lead", "marimba"]), "vibes"), line, pan=0.3, gain="-8dB")]
    for ro in [ro for ro in parts if "Brk" in ro and is16(ro)]:
        voic = r.choice([[0, 2, 4, 6, 10], [0, 4, 6, 8, 11], [2, 4, 6, 8, 12]])
        stabs = " ".join(f"{chordhead([k.deg(d, 55) for d in voic])}/4@{r.choice([70, 78])} R/4 R/2" for _ in range(4))
        parts[ro] = parts[ro] + [track("jazzkeys", pick_patch(r.choice(["rhodes", "vibes", "wurli"]), "rhodes"), stabs, pan=-0.25, gain="-6dB")]


def _write_parts(slot, style, parts, desc, beats=None):
    names = {}
    parts = dict(parts)
    if not LITE:
        stock_layers(style, parts, beats, desc)
    if style in CHILL_STYLES and _CHAPTER >= 1 and not LITE:
        # Development across chapters: the melody gains an octave double (a mallet above in chapter 2,
        # cellos/horn below or a flute above later), quiet, so it thickens rather than competes.
        import zlib
        dr = random.Random(zlib.crc32(f"dbl{desc}{_CHAPTER}".encode()))
        for role in [ro for ro in parts if ro.startswith("hook")]:
            if _CHAPTER == 1:
                dbl, tr_ = pick_patch(dr.choice(["vibes", "celesta", "glock", "music-box"]), "vibes"), 12
            else:
                dbl, tr_ = dr.choice([(pick_patch("cellos", "strings"), -12), (pick_patch("horn", "strings"), -12), (pick_patch("flute", "vibes"), 12)])
            parts[role] = parts[role] + [dict(t, name=t["name"] + "-dbl", patch=dbl, score=f"tr={tr_} " + t["score"], gain="-8dB", pan=-float(t.get("pan", 0) or 0))
                                         for t in parts[role] if isinstance(t.get("patch"), str) and "kit" not in t["patch"]]
    if style in HEAVY_STYLES and FUSION and not LITE:
        fusion_layers(style, parts, beats, desc)
    if style in HEAVY_STYLES:
        import zlib
        er = random.Random(zlib.crc32(f"enrich{desc}".encode()))
        parts = {role: (tr if any(b in role for b in ("Bl", "Blast", "Grav")) else [drum_enrich(t, er) for t in tr]) for role, tr in parts.items()}
    if style in CHILL_STYLES:
        sw = swap_plan(f"{style}{desc}")
        if sw:
            parts = {role: [dict(t, patch=sw.get(t.get("patch"), t.get("patch"))) if isinstance(t.get("patch"), str) and " " not in t.get("patch", "") else t for t in tr]
                     for role, tr in parts.items()}
    feel = None
    if style in CHILL_STYLES and style != "neosoul":
        import zlib
        fr = random.Random(zlib.crc32(f"{style}{desc}".encode()))
        feel = fr.choices(["tight", "laid", "drunk"], [0.3, 0.45, 0.25])[0]
    for role, tr in parts.items():
        if feel:
            tr = [feel_track(t, feel, fr) for t in tr]
        if style in CHILL_STYLES and role.startswith("riff") and not LITE:
            sc = scape(style, role, (beats or {}).get(role, 16), desc + slot)
            if sc:
                tr = tr + [sc]
        n = f"gen-{slot}-{role}"
        write(n, f"{role} for {style} in {desc}", tr, (beats or {}).get(role, 16))
        names[role] = n
    return names, desc


# ---------- per-style composition -------------------------------------------------------

# Wider harmonic vocabulary (idiomatic loops per mode); appended to PROGS, deduplicated.
_MORE_PROGS = {
    "major": [[0, 3, 5, 4], [5, 3, 0, 4], [1, 4, 0, 5], [0, 1, 2, 3], [3, 4, 2, 5], [0, 4, 1, 3], [2, 5, 1, 4], [0, 3, 0, 4], [0, 2, 3, 4], [3, 0, 4, 5]],
    "minor": [[5, 6, 0, 0], [0, 4, 5, 3], [0, 2, 6, 3], [3, 0, 6, 5], [0, 5, 3, 4], [0, 6, 3, 5], [0, 3, 4, 0], [5, 2, 6, 0]],
    "dorian": [[0, 1, 2, 1], [0, 4, 3, 0], [0, 2, 3, 6], [3, 0, 6, 0], [0, 1, 3, 0], [0, 6, 4, 3]],
    "lydian": [[0, 1, 6, 0], [0, 5, 1, 0], [0, 4, 1, 0], [5, 1, 0, 4], [0, 1, 2, 1]],
    "mixolydian": [[0, 4, 6, 3], [0, 3, 4, 0], [6, 3, 0, 0], [0, 1, 3, 0], [5, 6, 0, 0], [0, 6, 0, 3]],
    "phrygian": [[0, 6, 5, 1], [0, 3, 1, 0], [0, 2, 1, 0], [0, 1, 2, 1], [0, 5, 6, 1]],
    "harmonic": [[0, 5, 4, 4], [0, 2, 5, 4], [3, 4, 0, 0], [0, 3, 5, 4], [0, 6, 0, 4]],
    "blues": [[0, 3, 0, 4], [0, 3, 4, 3], [0, 0, 3, 3]],
    "pentatonic-minor": [[0, 3, 0, 2], [0, 4, 3, 0], [0, 1, 3, 4]],
    "double-harmonic": [[0, 1, 4, 0], [0, 3, 1, 0], [0, 4, 3, 1]],
    "hirajoshi": [[0, 2, 1, 0], [0, 4, 1, 0], [0, 3, 2, 1]],
    "hungarian": [[0, 4, 3, 0], [0, 1, 0, 4], [0, 5, 4, 0]],
    "neapolitan": [[0, 3, 1, 4], [0, 1, 3, 0]],
    "pelog": [[0, 2, 1, 0], [0, 4, 3, 1]],
    "diminished": [[0, 2, 0, 2], [0, 3, 1, 2]],
    "locrian": [[0, 3, 1, 0], [0, 1, 5, 6]],
    "phrygian-dominant": [[0, 3, 1, 0], [0, 5, 1, 0], [0, 1, 3, 1]],
}
for _m, _ps in _MORE_PROGS.items():
    if _m in PROGS:
        for _p in _ps:
            if _p not in PROGS[_m]:
                PROGS[_m].append(_p)


def params(style, rng=random):
    mode = rng.choice(STYLE_MODES.get(style, ["minor"]))
    heavy = style in ("meshuggah", "djent", "djent-breakdown", "doom-ambient", "tech-death", "thrash", "tool", "hardcore-kl", "brostep", "blackgaze", "darksynth", "numetal", "industrial", "dnb", "deathcore", "postrock", "postmetal", "slam", "metalcore", "symphonic", "cynic", "tigran", "mahavishnu", "groovemetal", "power", "sludge", "breakcore", "mathcore", "gojira", "djazz", "raga", "gamelan", "koto", "postmetal", "slam", "metalcore", "symphonic", "cynic", "tigran", "mahavishnu")
    if style in CHILL_STYLES:
        rigset = "chill"
    else:
        rigset = None
    rigset = rigset or ("tech" if style == "tech-death" and rng.random() < 0.6 else
              "thrash" if style == "thrash" else
              "fuzz" if style == "sludge" else
              rng.choice(["fuzz", "tool-fuzz", "bkp", "fluence", "chug"]) if style == "postmetal" else
              rng.choice(["chug", "fluence", "bkp", "emg"]) if style == "slam" else
              rng.choice(["modern", "emg", "bkp", "fluence"]) if style in ("metalcore", "symphonic") else
              "gojira" if style == "gojira" else
              "chug" if style in ("hardcore-kl", "brostep") else
              rng.choice(["tool-fuzz", "tool-pick", "tool-fuzz", "phase"]) if style == "tool" else
              rng.choice(["modern", "chug", "chug", "fuzz", "phase", "emg", "bkp", "fluence", "fluence"])) if heavy else "modern"
    flavor = (rng.choice(["modern", "vintage", "vintage", "space", "wide"]) if style in CHILL_STYLES else
              rng.choice(["modern", "modern", "vintage", "industrial", "space", "wide"]) if style != "industrial" else "industrial")
    return {"pc": rng.randrange(12), "mode": mode, "prog": rng.choice(PROGS[mode]), "seed": rng.randrange(1 << 30), "rigset": rigset, "flavor": flavor}


def gen_fill(r, k, low=28, kind=None):
    """A 4-beat drum fill leading into a big section: descending tom 16ths, a crescendo snare roll
    into 32nds, a linear kick/snare/tom figure, a triplet tom fill, or a stop (silence, then a
    flammed pickup). Some open with a ringing power chord (or just a bass note)."""
    kind = kind or r.choice(["toms", "roll", "linear", "triplets", "stop"])
    t = k.deg(0, low)
    kit = rig("drums")
    if kind == "triplets":
        seq = [r.choice(["t1", "t2"]), "t2", "t3", "t3", "ft", "ft", "s", "t1", "t2", "t3", "ft", "s"]
        drums = " ".join(f"{p_}/12@{100 + 2 * i}" for i, p_ in enumerate(seq))
        kick = " ".join("k/12@104" if i % 3 == 0 else "R/12" for i in range(12))
    elif kind == "stop":
        drums = "R/4 R/4 R/4 R/8 s/8@118^flam"
        kick = "R/4 R/4 R/4 R/8 k/8@118"
    else:
        steps = []
        for i in range(16):
            if kind == "toms":
                steps.append(f"{['t1', 't1', 't2', 't2', 't3', 't3', 'ft', 'ft'][i % 8]}/16@{100 + i}")
            elif kind == "roll":
                steps.append(f"s/16@{70 + 3 * i}" + ("^r=2" if i >= 12 else ""))
            else:
                steps.append(f"{['s', 't1', 't2', 's', 't3', 'ft', 's', 'ft'][i % 8]}/16@{102 + i}")
        drums = " ".join(steps)
        kick = " ".join(("k/16@108" if (kind == "linear" and i % 4 == 2) or (kind != "linear" and i % 4 == 0) else "R/16") for i in range(16))
    out = [track("fill", kit, drums), track("fill-k", kit, kick)]
    if r.random() < 0.5 and kind != "stop":
        out += rhythm_tracks(f"expr.pm=0 {chordhead([t, t + 7, t + 12])}/4@118^gate=3 R/4 R/4 R/4")
    elif kind != "stop":
        out.append(track("bass", rig("bass"), f"{mname(t)}/4@110^gate=2 R/4 R/4 R/4", seed=7))
    return out


def gen_ending(r, k, prog, low=28, kind=None):
    """Song endings (16 beats): `rock` — the final chord rings over a building drum roll into a
    last crash; `cut` — three hard hits on the root, then dead silence."""
    kind = kind or r.choice(["rock", "cut"])
    t = k.deg(0, low)
    kit = rig("drums")
    pc = [t, t + 7, t + 12]
    if kind == "cut":
        g = f"expr.pm=0 {chordhead(pc)}/8@124^gate=0.5 R/8 R/4 {chordhead(pc)}/8@124^gate=0.5 R/8 R/4 R/2 {chordhead(pc)}/4@127^gate=0.6 R/4 R/1 R/1"
        drums = "x/8@120 R/8 R/4 x/8@120 R/8 R/4 R/2 c/4@124 R/4 R/1 R/1"
        kick = "k/8@122 R/8 R/4 k/8@122 R/8 R/4 R/2 k/4@124 R/4 R/1 R/1"
        bass = f"{mname(t)}/8@124 R/8 R/4 {mname(t)}/8@124 R/8 R/4 R/2 {mname(t)}/4@127 R/4 R/1 R/1"
    else:
        g = f"expr.pm=0 {chordhead(pc)}/1@124^gate=4 _ _ R/1"
        roll = " ".join(f"{p_}/16@{min(127, 80 + i)}" for i, p_ in enumerate((["t1", "t1", "t2", "t2", "t3", "t3", "ft", "ft"] * 4)))
        drums = f"c/4@120 R/4 R/2 {roll} c/4@127 R/4 R/2"
        kick = "k/4@120 R/4 R/2 " + " ".join("k/16@96" if i % 2 == 0 else "R/16" for i in range(32)) + " k/4@124 R/4 R/2"
        bass = f"{mname(t)}/1@120^gate=4 _ _ R/1"
    return rhythm_tracks(g) + [track("bass", rig("bass"), bass, seed=7), track("end-d", kit, drums), track("end-k", kit, kick)]


# ---------- chill: lofi hip hop, GoGo Penguin, UK jazz, ambient, downtempo -----------------------

def gen_lofi_drums(r, kit=None, busy=False):
    """Swung boom-bap: kick on 1 and the 'and' of 2 / 3, snare (or rim) on 2 & 4, lazy swung hats."""
    kit = kit or pick_patch("lofi-kit", "prog-kit")
    pat = r.choice(["x.....x.x.......", "x......x..x.....", "x.....x...x..x.."])
    kick = " ".join(("k/16@96" if pat[x] == "x" else "R/16") for _ in range(4) for x in range(16))
    sn = r.choice(["s", "s", "rs"])
    snare = " ".join((f"{sn}/16@92" if x in (4, 12) else (f"{sn}/16@{r.choice([28, 34])}" if busy and r.random() < 0.1 else "R/16")) for _ in range(4) for x in range(16))
    hats = " ".join((f"h/16@{r.choice([62, 70]) if x % 4 == 0 else r.choice([40, 50])}" if x % 2 == 0 or (busy and r.random() < 0.3) else "R/16") for _ in range(4) for x in range(16))
    sw = "swing16=0.62 "
    return [track("kick", kit, sw + kick), track("snare", kit, sw + snare), track("hats", kit, sw + hats, pan=0.15, gain="-3dB")]


def voice_lead(k, prog, degs=(0, 2, 4, 6, 8), base=52, lo=48, hi=74):
    """Voice-led chords: each chord takes the inversion (octave placement of each tone) closest to the
    previous voicing, so the inner voices glide."""
    out, prev = [], None
    for root in prog:
        tones = sorted(k.deg(root + d, base) for d in degs)
        if prev:
            placed = []
            for t in tones:
                cands = [t + o for o in (-12, 0, 12) if lo <= t + o <= hi]
                placed.append(min(cands or [t], key=lambda c: min(abs(c - p_) for p_ in prev)))
            tones = sorted(set(placed))
        out.append(tones)
        prev = tones
    return out


def gen_lofi(r, k, prog, kind="main"):
    """Lofi hip hop: swung boom-bap; voice-led Rhodes / Wurlitzer / tape-piano 9th chords in varied comp
    rhythms through tape wow and a soft low-pass (a 'sampled' feel; the intro opens from muffled); a
    melodic finger bass with approach notes; a vinyl bed; kind=busy adds jazz-guitar licks at bar ends."""
    out = []
    if kind != "intro":
        out += gen_lofi_drums(r, busy=kind == "busy")
    voicings = voice_lead(k, prog, r.choice([(0, 2, 4, 6, 8), (2, 4, 6, 8, 11), (0, 4, 6, 8, 9)]))
    cells = [lambda c: f"{c}/4.@80 R/8 R/4 {c}/4@72", lambda c: f"R/8 {c}/4.@78 R/4 {c}/8@66 R/8", lambda c: f"{c}/2@80 R/8 {c}/8@64 R/4",
             lambda c: f"{c}/8@76 R/8 R/8 {c}/8@68 R/4 {c}/4@72", lambda c: f"{c}/1@78"]
    keys = " ".join(r.choice(cells)(chordhead(v)) for v in voicings)
    sampled = [{"type": "chorus", "rate": round(r.uniform(0.4, 0.7), 2), "depth": 0.25, "voices": 1, "mix": 1.0},
               {"type": "filter", "kind": "lp", "cutoff": {"value": 5000, "mod": [{"src": "auto.open", "amount": -2.5}]} if kind == "intro" else 5000},
               {"type": "crush", "bits": 12, "rate": 18000, "mix": 0.2}]
    kt = track("keys", pick_patch(r.choice(["rhodes", "wurli", "tape-piano"]), "rhodes"), "swing=0.62 " + keys, fx=sampled)
    if kind == "intro":
        kt["auto"] = {"open": {"points": [["0b", 1.0], ["12b", 0.0], ["16b", 0.0]]}}
    out.append(kt)
    if kind != "intro":
        bass = []
        for bi, root in enumerate(prog):
            nxt = prog[(bi + 1) % len(prog)]
            b1, b5 = mname(k.deg(root, 33)), mname(k.deg(root + 4, 33))
            appr = mname(k.deg(nxt, 33) - 1)
            bass.append(r.choice([f"{b1}/4.@90 {b5}/8@76 R/4 {b1}/8@82 {appr}/8@70",
                                  f"{b1}/4@90 R/8 {b1}/8@72 {b5}/4@80 R/8 {appr}/8@68",
                                  f"{b1}/2@88 R/8 {b5}/8@74 {b1}/8@80 {appr}/8@70"]))
        out.append(track("bass", pick_patch("finger-bass", "bass-di"), "swing16=0.62 " + " ".join(bass), seed=7))
    if kind == "busy":
        pt = penta(k)
        licks = []
        for bi, root in enumerate(prog):
            if bi % 2 == 1:
                lick = [mname(k.deg(root + pt[i % 5] + 7 * (i // 5), 60)) for i in r.sample(range(7), 4)]
                licks.append("R/2 R/4 " + " ".join(f"{n_}/16@{r.choice([64, 72])}" for n_ in lick))
            else:
                licks.append("R/1")
        out.append(track("licks", pick_patch("jazz-box", "clean-chorus"), "swing16=0.62 " + " ".join(licks), pan=0.3, gain="-4dB"))
    out.append(track("vinyl", "vinyl", "C4/1 _ _ _", gain="-4dB"))
    return out

def gen_ostinato(r, k, prog, base=60, patch="piano", group=None):
    """GoGo Penguin piano: a repeating 16th cell over chord tones with odd accent groupings over 4/4."""
    group = group or r.choice([[3, 3, 2], [3, 3, 3, 3, 4], [5, 5, 6], [3, 5]])
    accents, pos = set(), 0
    while pos < 16:
        accents.add(pos); pos += group[len(accents) % len(group)]
    cell = r.choice([[0, 2, 4, 7], [0, 4, 7, 9], [0, 2, 4, 2, 7, 4], [4, 2, 0, 2]])
    rh, lh = [], []
    for bar, root in enumerate(prog):
        for x in range(16):
            rh.append(f"{mname(k.deg(root + cell[x % len(cell)], base))}/16@{96 if x in accents else 72}")
        lh.append(f"{mname(k.deg(root, base - 24))},{mname(k.deg(root, base - 12))}/2@80 {mname(k.deg(root + 4, base - 24))}/2@74")
    room = {"fx": expand(["rack:piano-room"])} if patch == "piano" else {}
    return [track("rh", pick_patch(patch, "piano"), " ".join(rh), pan=0.15, **room), track("lh", pick_patch(patch, "piano"), " ".join(lh), pan=-0.15, **room)]


def gen_trio_drums(r, kind="groove"):
    """Tight, electronic-feeling acoustic drums: busy closed hats, offbeat kicks, cross-stick backbeat."""
    kit = rig("drums")
    if kind == "breaks":  # GoGo Penguin's drum-and-bass-inspired breaks: two-step kick, rolling ghosts, ride + hats
        kp = r.choice(["x.........x.....", "x.........x..x..", "x......x..x....."])
        return [track("hats", kit, " ".join((f"{'rd' if x % 4 == 0 else 'h'}/16@{66 if x % 4 == 0 else 48}") for _ in range(4) for x in range(16)), pan=0.12, gain="-4dB"),
                track("kick", kit, " ".join(("k/16@100" if kp[x] == "x" else "R/16") for _ in range(4) for x in range(16))),
                track("snare", kit, " ".join(("s/16@98" if x in (4, 12) else (f"g/16@{r.choice([26, 32, 38])}" if x in (6, 9, 14, 15) and r.random() < 0.6 else "R/16")) for _ in range(4) for x in range(16)))]
    hats, kick, snare = [], [], []
    for i in range(64):
        x = i % 16
        hats.append(f"h/16@{70 if x % 4 == 0 else 52}" if kind != "sparse" else ("hp/16@50" if x % 4 == 2 else "R/16"))
        kick.append("k/16@100" if x in (0, 7, 10) or (kind == "build" and x % 4 == 0) else "R/16")
        snare.append(("ss/16@84" if kind == "sparse" else "s/16@96") if x in (4, 12) else (f"g/16@30" if kind != "sparse" and r.random() < 0.12 else "R/16"))
    return [track("hats", kit, " ".join(hats), pan=0.12, gain="-3dB"), track("kick", kit, " ".join(kick)), track("snare", kit, " ".join(snare))]


def gen_broken(r, k, prog, meter=7, kind="main", bass_patch=None):
    """UK jazz broken beat in an odd meter (7/8 or 5/4 as 10/8): shuffled 16ths, kick on odd
    placements, snare/rim backbeats with ghosts; Rhodes chords and an upright (or tuba) line in the
    meter; kind=horns adds a horn-section riff in the meter (octave dyads) and shekere."""
    kit = rig("drums")
    reps = 4 if meter in (7, 9) else 3
    n = meter * 2 * reps  # 16ths
    kick, snare, hats, keys, bass = [], [], [], [], []
    keys_patch = pick_patch(r.choice(["rhodes", "wurli"]), "rhodes")
    for i in range(n):
        x = i % (meter * 2)
        bar = i // (meter * 2)
        root = prog[bar % len(prog)]
        kick.append("k/16@96" if x in (0, 5, 9) or (x == meter * 2 - 3 and r.random() < 0.5) else "R/16")
        snare.append("s/16@92" if x in (4, meter * 2 - 4) else (f"g/16@{r.choice([26, 32])}" if r.random() < 0.18 else "R/16"))
        hats.append(f"h/16@{66 if x % 2 == 0 else 46}" if r.random() < 0.85 else "R/16")
        keys.append(f"{chordhead([k.deg(root + d, 50) for d in (0, 2, 4, 6, 8)])}/16@{78}^gate=4" if x in (0, 7) and kind != "sparse" else "R/16")
        bass.append(f"{mname(k.deg(root + r.choice([0, 0, 4, 2]), 33))}/16@{88}^gate=2" if x % 4 == 0 or x == meter * 2 - 2 else "R/16")
    sw = "swing16=0.6 "
    jn = lambda xs: sw + " ".join(xs)
    out = [track("kick", kit, jn(kick)), track("snare", kit, jn(snare)), track("hats", kit, jn(hats), pan=0.12, gain="-3dB"),
           track("bass", bass_patch or pick_patch("upright-bass", "finger-bass"), jn(bass), seed=7)]
    if kind != "drums":
        out.append(track("keys", keys_patch, jn(keys), pan=-0.15))
    if kind == "horns":
        pt = penta(k)
        cell = [pt[i] for i in r.choice([[0, 2, 3, 2], [4, 3, 2, 0], [0, 0, 2, 4]])]
        hpos = sorted(r.sample([x for x in range(meter * 2) if x % 2 == 0], 4))
        riff, sk = [], []
        for i in range(n):
            x = i % (meter * 2)
            root = prog[(i // (meter * 2)) % len(prog)]
            if x in hpos:
                note = k.deg(root + cell[hpos.index(x)], 57)
                riff.append(f"{chordhead([note, note + 12])}/16@{96 if x == hpos[0] else 86}^gate=1.5")
            else:
                riff.append("R/16")
            sk.append(f"sk/16@{56 if x % 4 == 0 else 44}" if x % 2 == 0 else "R/16")
        out += [track("horns", pick_patch("horn-section", "brass"), jn(riff), pan=0.15, gain="-4dB"),
                track("shekere", pick_patch("afro-perc", "tight-kit"), jn(sk), pan=-0.25, gain="-6dB")]
    return out


def gen_ambient(r, k, prog, kind="A"):
    """Ethereal ambient: a swelling pad (strings / Juno / Mellotron choir / glass, chosen per song) and a
    drone; twinkles through a shimmer hall and a spectral freeze that catches them into a sustained cloud
    at a random point of the section (Eno); singing-bowl or handpan strokes; kind=B adds a short Rhodes /
    piano phrase looping and disintegrating (Basinski: crush and darkening grow over the section) and a
    sustained e-bow / theremin line. No drums."""
    pad_patch = pick_patch(r.choice(["strings", "juno-pad", "mellotron-choir", "pad-glass"]), "strings")
    peak = r.choice([6, 10, 14])
    swell = {"sw": {"points": [["0b", 0.2], [f"{peak}b", 1.0], ["16b", 0.35]]}}
    out = [dict(t, auto=swell, gain={"value": "-14dB", "mod": [{"src": "auto.sw", "amount": 6}]})
           for t in gen_pad(r, k, prog, 48, pad_patch, vel=60)]
    out += gen_drone(k, 36, pick_patch("drone", "pad"))
    if have("choir") and r.random() < 0.4:
        out += [dict(t, name="choir", gain="-12dB") for t in gen_pad(r, k, prog, 48, "choir", vel=56)]
    tw = pick_patch(r.choice(["music-box", "kalimba", "glock", "celesta", "harp"]), "bell")
    notes = []
    for x in range(64):
        notes.append(f"{mname(k.deg(r.choice([0, 2, 4, 7, 9, 11]), 72))}/16@{r.choice([50, 60, 70])}" if r.random() < (0.12 if kind == "A" else 0.2) else "R/16")
    at = r.choice([4, 6, 8, 10])
    freeze_lane = {"fz": {"points": [["0b", 0], [f"{at}b", 0], [f"{at + 0.1:g}b", 1], [f"{at + r.choice([3, 4, 5])}b", 1], [f"{at + 6}b", 0], ["16b", 0]]}}
    freeze = {"type": "freeze", "hold": {"value": 0, "mod": [{"src": "auto.fz", "amount": 1}]}, "size": f"{r.choice([150, 220, 300])}ms", "mix": 0.55}
    out.append(track("twinkle", tw, " ".join(notes), pan=r.choice([-0.4, 0.4]), fx=[freeze] + expand(["rack:shimmer-hall"]), auto=freeze_lane, gain="-4dB"))
    bowl = pick_patch(r.choice(["singing-bowl", "handpan"]), "bell")
    out.append(track("bowl", bowl, " ".join(f"{mname(k.deg(root, 48))}/1@{60}" if i % 2 == 0 else "R/1" for i, root in enumerate(prog)), gain="-6dB"))
    if kind == "B":
        cell = " ".join(f"{mname(k.deg(prog[0] + d, 60))}/8@{r.choice([60, 66, 72])}" if d is not None else "R/8" for d in r.choice([[0, 2, 4, None, 7, 4, None, 2], [4, None, 2, 0, None, 2, 4, None], [7, 4, 2, None, 0, None, 2, None]]))
        wear = {"wear": {"points": [["0b", 0.0], ["16b", 1.0]]}}
        loop_fx = [{"type": "crush", "bits": 10, "rate": 12000, "mix": {"value": 0, "mod": [{"src": "auto.wear", "amount": 0.7}]}},
                   {"type": "filter", "kind": "lp", "cutoff": {"value": 6000, "mod": [{"src": "auto.wear", "amount": -2.0}]}},
                   {"type": "chorus", "rate": 0.3, "depth": 0.4, "voices": 1, "mix": 1.0}, {"type": "reverb", "kind": "hall", "decay": "4s", "mix": 0.35}]
        out.append(track("loop", pick_patch(r.choice(["rhodes", "piano", "tape-piano"]), "piano"), " ".join([cell] * 4), fx=loop_fx, auto=wear, pan=0.2, gain="-6dB"))
        out += [dict(t, gain="-6dB") for t in gen_atmos(r, k, prog, 62, pick_patch(r.choice(["ebow", "theremin"]), "ambient-swell"))]
    return out

def gen_cycles(r, k, prog, kind="main"):
    """Four Tet / Bonobo melodic house: sparkly motifs in different cycle lengths (5, 7, 3 steps)
    over four-on-the-floor, shuffled hats and claps, warm offbeat bass, pads."""
    out = []
    for cyc, patch, base, pan in [(5, pick_patch("pluck-lead", "arp-pluck"), 64, -0.3), (7, pick_patch("kalimba", "marimba"), 72, 0.3), (3, pick_patch("glock", "music-box"), 84, 0.1)]:
        if kind == "intro" and cyc == 5:
            continue
        motif = [r.choice([0, 2, 4, 7, 9]) if r.random() < 0.75 else None for _ in range(cyc)]
        notes = []
        for i in range(64):
            d = motif[i % cyc]
            notes.append(f"{mname(k.deg(prog[i // 16] + d, base))}/16@{r.choice([70, 80, 88])}" if d is not None else "R/16")
        out.append(track(f"cyc{cyc}", patch, " ".join(notes), pan=pan, gain="-6dB" if cyc == 3 else "-3dB"))
    if kind != "intro":
        kit = pick_patch("909", "electro-kit")
        sw = "swing16=0.57 "
        out += [track("kick", kit, sw + " ".join(("k/16@112" if x % 4 == 0 else "R/16") for _ in range(4) for x in range(16))),
                track("clap", kit, sw + " ".join(("cp/16@96" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), gain="-2dB"),
                track("hats", kit, sw + " ".join((f"{'oh' if x % 4 == 2 else 'h'}/16@{76 if x % 4 == 2 else 52}" if x % 2 == 0 or r.random() < 0.4 else "R/16") for _ in range(4) for x in range(16)), pan=0.12, gain="-3dB"),
                track("bass", pick_patch("finger-bass", "sub-sine"), sw + " ".join(f"R/8 {mname(k.deg(root, 33))}/8@96 R/8 {mname(k.deg(root, 33))}/8@88 R/8 {mname(k.deg(root + 4, 33))}/8@92 R/8 {mname(k.deg(root, 45))}/8@84" for root in prog), seed=7)]
    return out + gen_pad(r, k, prog, 48, pick_patch("supersaw", "saw-pad"), gain="-12dB", vel=64)


def gen_classical(r, k, prog, kind="nocturne"):
    """Pure classical: nocturne (left-hand broken chords + lyrical right-hand melody, roomy piano),
    quartet (four voice-led parts: cello, viola, violins; first violin carries the melody),
    minimal (Reich/Glass phasing patterns on piano and marimba)."""
    room = expand(["rack:piano-room"])
    if kind == "nocturne":
        lh = []
        for root in prog:
            c = [k.deg(root, 36), k.deg(root + 4, 48), k.deg(root + 7, 48), k.deg(root + 9, 48), k.deg(root + 11, 48), k.deg(root + 9, 48)]
            lh += [f"{mname(m)}/12@{70 if j == 0 else 58}" for j, m in enumerate(c * 2)]
        mel = gen_hook(r, k, prog, 72, "piano")[0]
        lhp = pick_patch("harp", "piano") if r.random() < 0.5 else "piano"
        return [track("lh", lhp, " ".join(lh), pan=-0.2, fx=room), dict(mel, name="rh", pan=0.2, fx=room)]
    if kind == "quartet":
        voices = {"cello": [], "viola": [], "vln2": []}
        for root in prog:
            ch = sorted([k.deg(root, 36), k.deg(root + 4, 48), k.deg(root + 2, 60)])
            for (name, m) in zip(voices, ch):
                voices[name].append(f"{mname(m)}/2@{72} {mname(m + r.choice([0, 0, 2, -1]))}/2@68")
        sect = {"cello": pick_patch("cellos", "strings"), "viola": "strings", "vln2": pick_patch("violins", "strings")}
        out = [track(n, sect[n], " ".join(v), pan=p_, gain="-4dB") for (n, v), p_ in zip(voices.items(), [-0.4, -0.15, 0.15])]
        mel = gen_hook(r, k, prog, 72, pick_patch("violins", "strings"))[0]
        return out + [dict(mel, name="vln1", pan=0.4)]
    cell = r.choice([[0, 2, 4, 2, 7, 4], [0, 4, 7, 4, 2, 4, 7, 9], [0, 2, 7, 4, 9]])
    a = " ".join(f"{mname(k.deg(prog[i // 16] + cell[i % len(cell)], 60))}/16@{80 if i % len(cell) == 0 else 66}" for i in range(64))
    b = " ".join(f"{mname(k.deg(prog[i // 16] + cell[(i + 1) % len(cell)] + 2, 72))}/16@{70}" for i in range(64))
    return [track("piano", "piano", a, pan=-0.25, fx=room), track("marimba", pick_patch("marimba", "vibes"), b, pan=0.25, gain="-4dB")]


def gen_smile(r, k, prog, kind="arp"):
    """The Smile / Radiohead: interlocking clean-guitar arpeggios with odd accent groupings, a
    melodic bass counterline, roomy piano chords, tight busy drums with rim clicks; kind=quiet drops
    the drums, kind=full adds string swells and horn swells; kind=kida is the electronic side (Kid A):
    a glitchy stuttering drum machine, pulsing Rhodes/Wurlitzer chords, a sub bass and a drifting
    falsetto-like dream-vox pad."""
    if kind == "kida":
        kit = pick_patch("electro-kit", "tight-kit")
        stut = [{"type": "stutter", "slice": r.choice(["1/32", "1/16"]), "repeats": r.choice([2, 3, 4]), "chance": 0.3, "seed": r.randrange(1000)},
                {"type": "crush", "bits": 10, "rate": 14000, "mix": 0.35}]
        kp = r.choice(["x.....x...x.....", "x..x......x..x..", "x.......x.x....."])
        drift = {"dr": {"wave": "sine", "rate": "0.11hz"}}
        out = [track("kick", kit, " ".join(("k/16@90" if kp[x] == "x" else "R/16") for _ in range(4) for x in range(16)), fx=stut, gain="-5dB"),
               track("snare", kit, " ".join(("rs/16@80" if x in (4, 12) else ("rs/16@40" if r.random() < 0.12 else "R/16")) for _ in range(4) for x in range(16)), fx=stut, gain="-5dB"),
               track("hats", kit, " ".join((f"h/16@{r.choice([40, 50])}" if r.random() < 0.6 else "R/16") for _ in range(64)), fx=stut, pan=0.2, gain="-8dB"),
               track("keys", pick_patch(r.choice(["rhodes", "wurli"]), "rhodes"), " ".join(" ".join(f"{chordhead(v)}/8@{r.choice([66, 74])}" for _ in range(8)) for v in voice_lead(k, prog, (0, 2, 4, 6))), pan=-0.15, gain="-3dB"),
               track("sub", pick_patch("sub-sine", "finger-bass"), " ".join(f"{mname(k.deg(root, 33))}/2@80 R/2" for root in prog), seed=7),
               track("falsetto", pick_patch("dream-vox", "choir"), " ".join(f"{mname(k.deg(root + r.choice([2, 4, 7]), 67))}/1@{60}" for root in prog), lfo=drift, gain="-6dB",
                     fx=[{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "lfo.dr", "amount": 0.2}]}, "grain": "70ms", "mix": 1.0}])]
        return out
    g1 = gen_ostinato(r, k, prog, 52, rig("clean"), r.choice([[3, 3, 2], [3, 5], [5, 5, 6]]))[0]
    g2 = gen_ostinato(r, k, prog, 64, rig("clean"), r.choice([[3, 3, 3, 3, 4], [3, 3, 2]]))[0]
    tape = expand(["rack:tape-echo"])
    out = [dict(g1, name="gtr1", pan=-0.35, fx=tape), dict(g2, name="gtr2", pan=0.35, gain="-3dB")]
    out.append(track("bass", rig("bass"), " ".join(f"{mname(k.deg(root, 33))}/8@{88} {mname(k.deg(root + 4, 33))}/8@78 R/8 {mname(k.deg(root + 2, 33))}/8@80 {mname(k.deg(root + 6, 33))}/4@82 {mname(k.deg(root + 4, 33))}/4@76" for root in prog), seed=7))
    out += [dict(t, fx=expand(["rack:piano-room"]), gain="-4dB") for t in gen_pad(r, k, prog, 52, "piano", gain="-6dB", vel=70)]
    if kind != "quiet":
        out += gen_trio_drums(r, "groove")
    if kind == "full":
        out += [dict(t, name="strings") for t in gen_pad(r, k, prog, 48, pick_patch(r.choice(["strings", "mellotron-strings"]), "strings"), gain="-10dB", vel=64)]
        if r.random() < 0.6:  # The Smile's brass: slow horn swells under the guitars
            out.append(track("horns", pick_patch("horn", "brass"), " ".join(f"{chordhead([k.deg(root, 50), k.deg(root + 4, 50)])}/2@{58} {chordhead([k.deg(root + 2, 50), k.deg(root + 4, 50)])}/2@{74}" for root in prog), gain="-6dB", pan=0.1))
    return out


def gen_triphop(r, k, prog, kind="main"):
    """Trip-hop: a slow, dusty half-time breakbeat (low-passed) with vinyl, deep finger bass, minor
    Rhodes chords, strings in kind=full; kind=intro is keys + vinyl only."""
    kit = pick_patch("break-kit", "lofi-kit")
    lp = [{"type": "filter", "kind": "lp", "cutoff": 2800}, {"type": "crush", "bits": 12, "rate": 18000, "mix": 0.3}]
    out = [track("vinyl", "vinyl", "C4/1 _ _ _", gain="-2dB")]
    out += gen_comp(r, k, prog, 48, pick_patch("rhodes", "piano"), swing=0.6)
    if kind == "intro":
        return out
    pat = r.choice(["x......x..x.....", "x.......x.x....."])
    out += [track("kick", kit, " ".join(("k/16@100" if pat[x] == "x" else "R/16") for _ in range(4) for x in range(16)), fx=lp, gain="-3dB"),
            track("snare", kit, " ".join(("s/16@104" if x == 8 else (f"g/16@32" if r.random() < 0.08 else "R/16")) for _ in range(4) for x in range(16)), fx=lp, gain="-3dB"),
            track("hats", kit, " ".join((f"h/16@{56 if x % 4 == 0 else 40}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16)), fx=lp, gain="-5dB"),
            track("bass", pick_patch("finger-bass", "sub-sine"), " ".join(f"{mname(k.deg(root, 28))}/2@96 R/4 {mname(k.deg(root + 4, 28))}/4@80" for root in prog), seed=7)]
    if kind == "full":
        out += [dict(t, name="strings") for t in gen_pad(r, k, prog, 48, "strings", gain="-12dB", vel=60)]
    return out


def gen_neoclassical(r, k, prog, kind="main"):
    """Neo-classical (Arnalds / Frahm): a gentle roomy piano ostinato, cellos and strings swelling
    beneath (kind main/full), celesta glints (full)."""
    out = [dict(t, gain="-2dB") for t in gen_ostinato(r, k, prog, 60, "piano", r.choice([[3, 3, 2], [4, 4], [3, 5]]))]
    out = [dict(t, score=re.sub(r"@(\d+)", lambda m_: "@" + str(int(int(m_.group(1)) * 0.8)), t["score"])) for t in out]  # softer touch
    if kind == "full" and r.random() < 0.5:
        out += [dict(t, name="glass", gain="-10dB") for t in gen_pad(r, k, prog, 60, pick_patch("pad-glass", "pad"), vel=56)]
    if kind in ("main", "full"):
        out.append(track("cellos", pick_patch("cellos", "strings"), " ".join(f"{mname(k.deg(root, 36))}/1@{66}" for root in prog), gain="-6dB"))
    if kind == "full":
        out += [dict(t, name="strings") for t in gen_pad(r, k, prog, 52, "strings", gain="-10dB", vel=60)]
        out.append(track("celesta", pick_patch(r.choice(["celesta", "music-box"]), "glock"), " ".join(f"{mname(k.deg(r.choice([0, 2, 4, 7]), 72))}/8@{60}" if r.random() < 0.15 else "R/8" for _ in range(32)), pan=0.3, gain="-6dB"))
    return out


def gen_ballad(r, k, prog, kind="trio"):
    """Late-night jazz ballad: brushes (swung ride, soft snare sweeps), rootless piano voicings twice
    a bar, a walking upright line in quarters; kind=melody adds nothing here (the hook carries it)."""
    kit = pick_patch("brush-kit", "tight-kit")
    ride = " ".join("rd/8@64 rd/8@46" for _ in range(32))
    snare = " ".join(("s/8@38" if x % 4 == 2 else "R/8") for x in range(32))
    piano, bass = [], []
    for root in prog:
        v = r.choice([[2, 6, 8], [6, 8, 9], [2, 4, 6]])
        ch = chordhead([k.deg(root + d, 52) for d in v])
        piano.append(f"{ch}/2@{r.choice([62, 68])} {ch}/4@56 R/4")
        bass.append(" ".join(f"{mname(k.deg(root + d, 33))}/4@{78}" for d in r.choice([[0, 2, 4, 5], [0, 4, 2, 1], [0, 1, 2, 4]])))
    sw = "swing=0.66 "
    room = expand(["rack:piano-room"])
    return [track("ride", kit, sw + ride), track("snare", kit, sw + snare), track("piano", "piano", " ".join(piano), pan=-0.15, fx=room),
            track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(bass), seed=7)]


def gen_bossa(r, k, prog, kind="main"):
    """Bossa nova: nylon comping in the syncopated Gilberto pattern (thumb basses on 1 and 3, rootless
    maj7/m7/9 voicings between), rim clicks on a 3-2 clave, soft shaker, upright root–fifth; kind=guitar
    is the guitar alone."""
    stabs = r.choice([[3, 6, 10, 13], [2, 6, 9, 13], [3, 7, 10, 14]])
    gtr, bass = [], []
    for root in prog:
        v = chordhead([k.deg(root + d, 52) for d in r.choice([[2, 4, 6, 8], [4, 6, 8, 9], [2, 6, 8, 11]])])
        for x in range(16):
            if x in (0, 8):
                gtr.append(f"{mname(k.deg(root + (0 if x == 0 else 4), 40))}/16@{72}^gate=3")
            elif x in stabs:
                gtr.append(f"{v}/16@{r.choice([62, 68])}^gate=2")
            else:
                gtr.append("R/16")
        bass.append(f"{mname(k.deg(root, 33))}/4.@80 {mname(k.deg(root + 4, 33))}/8@70 {mname(k.deg(root, 33))}/4.@78 {mname(k.deg(root + 4, 33))}/8@68")
    out = [track("gtr", pick_patch("nylon", "acoustic"), " ".join(gtr), pan=-0.15)]
    if kind == "guitar":
        return out
    kit = rig("drums")
    clave = {0, 6, 12, 20, 24}
    rim = " ".join(("rc/16@70" if (i % 32) in clave else "R/16") for i in range(64))
    shaker = " ".join(f"shk/16@{48 if i % 4 == 0 else 34}" for i in range(64))
    kick = " ".join(("k/16@58" if i % 8 == 0 else "R/16") for i in range(64))
    return out + [track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(bass), seed=7),
                  track("rim", kit, rim), track("shaker", kit, shaker, pan=0.2, gain="-4dB"), track("kick", kit, kick)]


def gen_dub(r, k, prog, kind="main"):
    """Dub reggae: one-drop drums (kick + rim together on 3), swung hats, offbeat guitar skanks on 2
    and 4, a 16th organ bubble, a deep melodic bass with space; kind=dub drops instruments in and out
    under big delay throws and spring; kind=intro is bass + bubble."""
    kit = rig("drums")
    sw = "swing16=0.6 "
    kick = " ".join(("k/16@100" if x == 8 else "R/16") for _ in range(4) for x in range(16))
    rim = " ".join(("rs/16@96" if x == 8 else (f"rc/16@60" if x == 14 and r.random() < 0.3 else "R/16")) for _ in range(4) for x in range(16))
    hats = " ".join((f"h/16@{60 if x % 4 == 0 else 42}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16))
    skank, bubble, bass = [], [], []
    for root in prog:
        ch = chordhead([k.deg(root + d, 52) for d in (0, 2, 4)])
        skank.append(f"R/4 {ch}/8@84^gate=0.4 R/8 R/4 {ch}/8@82^gate=0.4 R/8")
        bubble.append(" ".join(f"{mname(k.deg(root + (0 if j % 2 == 0 else 4), 48))}/16@{70 if j % 4 == 1 else 54}" if j % 2 == 1 else "R/16" for j in range(16)))
        b = r.choice([[0, None, 0, 4, None, 2, 0, None], [0, 0, None, 4, 5, None, 4, 2], [0, None, 4, None, 0, 6, 5, None]])
        bass.append(" ".join(f"{mname(k.deg(root + d, 28))}/8@{96}" if d is not None else "R/8" for d in b))
    throw = {"type": "delay", "time": "3/16", "feedback": 0.55, "ping_pong": True, "tone": 2200, "mix": {"value": 0.1, "mod": [{"src": "auto.dub", "amount": 0.4}]}}
    dub_pts = {"dub": {"points": [["0b", 0], ["7b", 0], ["7.5b", 1], ["8b", 0.2], ["15b", 0.2], ["15.5b", 1], ["16b", 0.2]]}}
    spring = expand(["rack:spring-surf"])
    out = [track("bass", pick_patch("finger-bass", "sub-sine"), sw + " ".join(bass), seed=7, gain="2dB"),
           track("bubble", pick_patch("organ", "rhodes"), sw + " ".join(bubble), pan=0.25, gain="-6dB")]
    if kind == "intro":
        return out
    out += [track("kick", kit, sw + kick), track("rim", kit, sw + rim, fx=[throw] + spring, auto=dub_pts),
            track("hats", kit, sw + hats, pan=0.15, gain="-4dB"),
            track("skank", pick_patch("tele", "clean-chorus"), sw + " ".join(skank), pan=-0.25, fx=[dict(throw)] + spring, auto=dub_pts)]
    if kind == "dub":  # stripped: drop the bubble and hats in and out
        out = [t for t in out if t["name"] != "hats" or r.random() < 0.5]
    return out


def gen_manouche(r, k, prog, kind="main"):
    """Gypsy jazz (Django): la pompe on a steel-string acoustic — a bass strum on 1 and 3, short
    percussive chunks on 2 and 4 — in minor-6 / diminished colours; upright bass two-feel; no drums.
    kind=guitar is the rhythm guitar alone."""
    gtr, bass = [], []
    for root in prog:
        ch = chordhead([k.deg(root, 48)] + [k.deg(root + d, 52) for d in r.choice([[2, 4, 5], [2, 4, 6], [2, 3, 5]])])
        gtr.append(f"{ch}/4@{88}^gate=0.6 {ch}/4@{70}^gate=0.15 {ch}/4@{84}^gate=0.6 {ch}/4@{70}^gate=0.15")
        bass.append(f"{mname(k.deg(root, 33))}/2@{84} {mname(k.deg(root + 4, 33))}/2@{78}")
    sw = "swing=0.64 "
    out = [track("pompe", pick_patch("acoustic", "nylon"), sw + " ".join(gtr), pan=-0.2)]
    if kind == "guitar":
        return out
    return out + [track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(bass), seed=7)]


def gen_swing_run(r, k, prog, base, patch):
    """Fast swung 8th runs for gypsy-jazz solos: arpeggios and scale runs through the chords."""
    out = []
    for root in prog:
        cell = r.choice([[0, 2, 4, 6, 7, 6, 4, 2], [4, 3, 2, 1, 0, 2, 4, 7], [0, 4, 7, 9, 8, 7, 4, 2]])
        out += [f"{mname(k.deg(root + d, base))}/8@{96 if j % 2 == 0 else 82}" for j, d in enumerate(cell)]
    return [track("hook", patch, "swing=0.64 " + " ".join(out), pan=0.15)]


def gen_celtic(r, k, prog, kind="harp"):
    """Celtic folk-ambient on a triplet (6/8) grid: harp arpeggios on triplet 8ths; kind=drums adds
    the bodhrán (boom-tap jig pattern with rim accents); kind=intro is drone + harp."""
    harp = []
    for root in prog:
        tones = [k.deg(root + d, 48) for d in (0, 2, 4, 7, 9, 11)]
        seq = r.choice([tones + tones[::-1], tones[:3] * 2 + tones[3:] * 2, [tones[i] for i in (0, 2, 4, 1, 3, 5, 0, 4, 2, 5, 3, 1)]])
        harp += [f"{mname(m)}/12@{80 if j % 3 == 0 else 64}" for j, m in enumerate(seq[:12])]
    out = [track("harp", pick_patch("harp", "nylon"), " ".join(harp), pan=-0.2)]
    out += [dict(t, gain="-8dB") for t in gen_drone(k, 36, pick_patch("drone", "tanpura"))]
    if kind == "drums":
        pat = r.choice(["b..t.tb.tt.r", "b.tt.tb..t.r", "b..b.tt.tb.r"])
        hits = " ".join({"b": "b/12@96", "t": "t/12@72", "r": "r/12@64", ".": "R/12"}[c] for _ in range(4) for c in pat)
        out.append(track("bodhran", pick_patch("bodhran", "tight-kit"), hits, pan=0.15))
    return out


def gen_air(r, k, prog, base, patch):
    """A slow Celtic air: dotted rhythms on the triplet grid, grace-note flicks (^h) into long notes."""
    out = []
    for root in prog:
        d = root + r.choice([0, 2, 4])
        for ln in r.choice([[6, 3, 3], [3, 3, 6], [9, 3], [6, 6]]):
            if r.random() < 0.4:
                out.append(f"{mname(k.deg(d + 1, base))}/12@{70}^h")
                ln -= 1
            out.append(f"{mname(k.deg(d, base))}/12@{88}" + " _" * (ln - 1))
            d += r.choice([-2, -1, 1, 2])
    return [track("hook", patch, " ".join(out), pan=0.15)]


def gen_doomjazz(r, k, prog, kind="main"):
    """Doom jazz (Bohren & der Club of Gore): ultra-slow brushes (soft ride quarters, swishes on 2 and
    4), upright whole notes, dark Rhodes minor-9 / maj7#11 chords held for the bar, vibes ringing in
    kind=full, all in a vast hall. kind=intro: Rhodes alone."""
    hall = [{"type": "reverb", "kind": "hall", "decay": "7s", "predelay": "40ms", "low_cut": 150, "mix": 0.35}]
    keys = []
    for root in prog:
        keys.append(f"{chordhead([k.deg(root + d, 48) for d in r.choice([[0, 2, 4, 6, 8], [0, 4, 6, 8, 10], [0, 2, 6, 8, 11]])])}/1@{62}")
    out = [track("rhodes", pick_patch("rhodes", "piano"), " ".join(keys), pan=-0.15, fx=hall)]
    if kind == "intro":
        return out
    kit = pick_patch("brush-kit", "tight-kit")
    out += [track("ride", kit, " ".join("rd/4@54" for _ in range(16)), fx=hall, gain="-4dB"),
            track("snare", kit, " ".join(("s/4@40" if x % 2 == 1 else "R/4") for x in range(16)), fx=hall),
            track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(f"{mname(k.deg(root, 28))}/1@{80}" for root in prog), seed=7)]
    if kind == "full":
        out.append(track("vibes", pick_patch("vibes", "celesta"), " ".join(f"{chordhead([k.deg(root + d, 60) for d in (2, 4, 6)])}/2@56 R/2" for root in prog), pan=0.25, fx=hall, gain="-4dB"))
    return out


def penta(k):
    """Scale-degree indices of the pentatonic inside the key's mode (minor-ish modes → minor pentatonic)."""
    return [0, 2, 3, 4, 6] if k.mode in ("minor", "dorian", "phrygian", "harmonic", "locrian") else [0, 1, 2, 4, 5]


def gen_mali(r, k, prog, kind="main"):
    """Mali / desert blues: an interlocking kora ostinato (thumb bass on the beats, pentatonic upper
    notes between), a pentatonic bass ostinato, djembe bass/tone/slap with calabash and shaker;
    kind=riff adds a hypnotic lightly-driven Tele riff; kind=intro is the kora alone."""
    pt = penta(k)
    kora = []
    for root in prog:
        hi = [k.deg(root + pt[i % 5] + 7 * (i // 5), 60) for i in r.sample(range(8), 6)]
        for j in range(16):
            kora.append(f"{mname(k.deg(root, 48))}/16@{84}" if j % 4 == 0 else f"{mname(hi[j % 6])}/16@{70 if j % 2 else 76}")
    out = [track("kora", pick_patch("kora", "harp"), " ".join(kora), pan=-0.2)]
    if kind == "intro":
        return out
    bass_cell = r.choice([[0, None, 4, 0, None, 3, 4, None], [0, 0, None, 4, None, 6, 4, 2], [0, None, 0, 4, 3, None, 2, None]])
    bass = " ".join(f"{mname(k.deg(root + (pt[d % 5] if d is not None else 0), 33))}/8@{90}" if d is not None else "R/8" for root in prog for d in bass_cell)
    dj = r.choice(["b.s.t.s.b.tts.t.", "b..st.s.b.s.tt.s", "b.ts.tb.s.tts.t."])
    cal = "c.....c.c.......".replace(".", ".")
    hits = " ".join({"b": "b/16@100", "t": "t/16@74", "s": "s/16@90", ".": "R/16"}[c] for _ in range(4) for c in dj)
    gourd = " ".join(("c/16@88" if c == "c" else ("sh/16@52" if x % 2 == 0 else "R/16")) for _ in range(4) for x, c in enumerate(cal))
    out += [track("bass", pick_patch("finger-bass", "bass-di"), bass, seed=7),
            track("djembe", pick_patch("djembe", "tight-kit"), hits, pan=0.2), track("calabash", pick_patch("djembe", "tight-kit"), gourd, pan=-0.1)]
    if kind == "riff":
        cell = [pt[i] for i in r.choice([[0, 2, 3, 2, 0, 4, 3, 2], [0, 0, 2, 3, 4, 3, 2, 0], [4, 3, 2, 0, 2, 0, 3, 2]])]
        riff = " ".join(f"{mname(k.deg(root + d, 52))}/8@{86 if j % 2 == 0 else 72}" for root in prog for j, d in enumerate(cell))
        out.append(track("gtr", pick_patch("tele", "clean-chorus"), riff, pan=0.3, fx=[{"type": "drive", "drive": 0.25}, {"type": "reverb", "kind": "room", "decay": "1s", "mix": 0.15}], gain="-3dB"))
    return out


def gen_guofeng(r, k, prog, kind="main"):
    """Guofeng (Chinese-style ambient): cascading pentatonic koto/guzheng arpeggios over a soft string
    drone; temple woodblocks, soft kick and a frame-drum pulse in kind=full; kind=intro is koto + drone."""
    pt = penta(k)
    koto = []
    for root in prog:
        run = [k.deg(root + pt[i % 5] + 7 * (i // 5), 55) for i in range(8)]
        seq = r.choice([run + run[::-1], run[::2] + run[1::2] + run[::-2] + run[-2::-2], run[:4] * 2 + run[4:] * 2])
        koto += [f"{mname(m)}/16@{78 if j % 4 == 0 else 62}" for j, m in enumerate(seq[:16])]
    out = [track("koto", pick_patch("koto", "harp"), " ".join(koto), pan=-0.2),
           track("drone", pick_patch("strings", "pad"), " ".join(f"{chordhead([k.deg(root, 43), k.deg(root + 4, 43)])}/1@{54}" for root in prog), gain="-10dB")]
    if kind == "intro":
        return out
    kit = pick_patch("tight-kit", "metal-kit")
    blocks = r.choice(["x...x.x.....x...", "x.....x.x...x...", "x...x...x.x.x..."])
    out += [track("blocks", kit, " ".join((f"{'wb' if x % 8 == 0 else 'wbl'}/16@{64 if x % 8 == 0 else 54}" if c == "x" else "R/16") for _ in range(4) for x, c in enumerate(blocks)), pan=0.25, gain="-4dB"),
            track("kick", kit, " ".join(("k/16@60" if x in (0, 10) else "R/16") for _ in range(4) for x in range(16)))]
    if kind == "full":
        out.append(track("frame", pick_patch("bodhran", "tight-kit"), " ".join(("b/16@80" if x == 0 else ("t/16@60" if x in (6, 12) else "R/16")) for _ in range(4) for x in range(16)), pan=-0.1))
    return out


def gen_penta_air(r, k, prog, base, patch):
    """A slow pentatonic melody with long sliding notes (legato portamento does the slides)."""
    pt = penta(k)
    out = []
    for root in prog:
        for ln in r.choice([[2, 1, 1], [1, 1, 2], [3, 1], [4]]):
            out.append(f"{mname(k.deg(root + pt[r.randrange(5)], base))}/{4 // ln if ln in (1, 2, 4) else 4}@{84}" if ln != 3 else f"{mname(k.deg(root + pt[r.randrange(5)], base))}/2.@{84}")
    return [track("hook", patch, " ".join(out), pan=0.15)]


TAPE_WOW = [{"type": "chorus", "rate": 0.35, "depth": 0.3, "voices": 1, "mix": 1.0}, {"type": "filter", "kind": "lp", "cutoff": 6500}]


def gen_vaporwave(r, k, prog, kind="main"):
    """Vaporwave / city-pop chill: electro kick and hats, a gated-reverb snare and clap on 2 and 4,
    DX7 E.Piano maj9/m9 chords, a sliding fretless bass, everything through slow tape wow and a soft
    low-pass; kind=intro is the keys alone, kind=full adds a string bed."""
    gated = [{"type": "reverb", "kind": "room", "decay": "1.4s", "mix": 0.55}, {"type": "gate", "threshold": "-26dB", "hold": "110ms", "release": "35ms"}]
    keys, bass = [], []
    for root in prog:
        ch = chordhead([k.deg(root + d, 52) for d in r.choice([[0, 2, 4, 6, 8], [2, 4, 6, 8], [0, 4, 6, 8, 11]])])
        keys.append(r.choice([f"{ch}/2.@{78} {ch}/4@{66}", f"{ch}/4.@{76} {ch}/8@{64}^gate=0.5 R/4 {ch}/4@{68}", f"{ch}/1@{76}"]))
        cell = r.choice([[(0, 4), (4, 8), (7, 8), (5, 4), (4, 4)], [(0, 2), (2, 8), (4, 8), (5, 4)], [(0, 4), (0, 8), (4, 8), (6, 4), (7, 4)]])
        bass.append(" ".join(f"{mname(k.deg(root + d, 33))}/{ln}@{86}" for d, ln in cell))
    out = [track("keys", pick_patch("dx-epiano", "rhodes"), " ".join(keys), pan=-0.1, fx=TAPE_WOW)]
    if kind == "intro":
        return out
    kit = pick_patch("electro-kit", "tight-kit")
    sw = "swing16=0.56 "
    out += [track("bass", pick_patch("fretless", "finger-bass"), " ".join(bass), seed=7, fx=TAPE_WOW),
            track("kick", kit, sw + " ".join(("k/16@96" if x in (0, 10) or (x == 7 and r.random() < 0.3) else "R/16") for _ in range(4) for x in range(16))),
            track("snare", kit, sw + " ".join(("s/16@92" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), fx=gated),
            track("clap", kit, sw + " ".join(("cp/16@70" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), fx=gated, gain="-6dB"),
            track("hats", kit, sw + " ".join((f"h/16@{60 if x % 4 == 2 else 44}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16)), pan=0.2, gain="-6dB")]
    if kind == "full":
        out += [dict(t, name="strings", fx=TAPE_WOW) for t in gen_pad(r, k, prog, 55, "strings", gain="-12dB", vel=56)]
    return out


def gen_slowcore(r, k, prog, kind="main"):
    """Slowcore / Americana (Low, Red House Painters, Hammock): clean electric arpeggios through slow
    tremolo and spring, soft brushes on a slow backbeat, a root–fifth bass; kind=full adds Wurlitzer
    chords; kind=intro is the guitar alone."""
    trem = [{"type": "tremolo", "rate": 3.2, "depth": 0.35}] + expand(["rack:spring-surf"])
    gtr = []
    for root in prog:
        tones = [k.deg(root + d, 52) for d in (0, 4, 7, 9, 11)]
        cell = r.choice([[0, 1, 2, 3, 2, 1, 2, 4], [0, 2, 1, 3, 0, 2, 4, 2], [0, 1, 2, 1, 3, 2, 1, 2]])
        gtr += [f"{mname(tones[c])}/8@{80 if j % 4 == 0 else 66}" for j, c in enumerate(cell)]
    out = [track("gtr", pick_patch("tele", "clean-chorus"), " ".join(gtr), pan=-0.25, fx=trem, gain="-2dB")]
    if kind == "intro":
        return out
    kit = pick_patch("brush-kit", "tight-kit")
    out += [track("ride", kit, " ".join(f"rd/8@{52 if x % 2 == 0 else 40}" for x in range(32)), gain="-4dB"),
            track("snare", kit, " ".join(("s/4@58" if x % 2 == 1 else "k/4@62") for x in range(16))),
            track("bass", pick_patch("finger-bass", "bass-di"), " ".join(f"{mname(k.deg(root, 33))}/2@{82} {mname(k.deg(root + 4, 33))}/2@{74}" for root in prog), seed=7)]
    if kind == "full":
        out.append(track("wurli", pick_patch("wurli", "rhodes"), " ".join(f"{chordhead([k.deg(root + d, 55) for d in (0, 2, 4)])}/1@{58}" for root in prog), pan=0.25, gain="-6dB"))
    return out


def warped(r, amount=1.0):
    """Liminal tape: heavy wow, a slight detune, a muffled band-limit, light crush, tape-skip stutter, a big hall."""
    return [{"type": "chorus", "rate": round(r.uniform(0.15, 0.35), 2), "depth": round(0.6 + 0.3 * amount, 2), "voices": 1, "mix": 1.0},
            {"type": "pitch", "semitones": r.choice([-0.3, -0.5, -1.0]) * amount, "grain": "80ms", "mix": 1.0},
            {"type": "filter", "kind": "hp", "cutoff": 180}, {"type": "filter", "kind": "lp", "cutoff": int(2200 - 700 * amount)},
            {"type": "crush", "bits": 12, "rate": 14000, "mix": 0.35},
            {"type": "stutter", "slice": "1/8", "repeats": 2, "chance": round(0.08 + 0.25 * (amount - 1 if amount > 1 else 0) + 0.05 * amount, 2), "reverse": r.random() < 0.5, "seed": r.randrange(1000)},
            {"type": "reverb", "kind": "hall", "decay": "4.5s", "predelay": "30ms", "mix": 0.45}]


def gen_backrooms(r, k, prog, kind="main"):
    """Backrooms / liminal tape ambient: a distant ballroom-lounge band (stride piano or Wurlitzer,
    maj6/maj7, a waltzing bass) through heavy tape wow, detune, muffling, tape skips and a big hall,
    over fluorescent hum and tape hiss. kind=far adds warped strings; kind=decay warps harder."""
    amount = {"intro": 0.8, "main": 1.0, "far": 1.1, "decay": 1.6}.get(kind, 1.0)
    keys = []
    for root in prog:
        ch = chordhead([k.deg(root + d, 55) for d in r.choice([[0, 2, 4, 5], [0, 2, 4, 6], [2, 4, 5, 7]])])
        b1, b5 = mname(k.deg(root, 40)), mname(k.deg(root + 4, 40))
        keys.append(r.choice([f"{b1}/4@70 {ch}/4@58 {b5}/4@66 {ch}/4@56", f"{b1}/4@70 {ch}/4@58 {ch}/4@54 {b5}/4@64"]))
    out = [track("band", pick_patch(r.choice(["piano", "wurli", "tape-piano"]), "piano"), " ".join(keys), fx=warped(r, amount)),
           track("hum", pick_patch("sub-sine", "pad"), "B1,B2,F#3/1 _ _ _", gain="-26dB"),
           track("hiss", pick_patch("vinyl", "pad"), "C4/1 _ _ _", gain="-4dB")]
    if kind in ("far", "decay"):
        out += [dict(t, name="strings", fx=warped(r, amount)) for t in gen_pad(r, k, prog, 52, pick_patch("mellotron-strings", "strings"), gain="-8dB", vel=60)]
    if kind == "far" and have("music-box") and r.random() < 0.6:  # a warped music-box tune drifting through
        out += [dict(t, name="musicbox", fx=warped(r, amount * 1.2), gain="-4dB") for t in gen_hook(r, k, prog, 72, "music-box")]
    return out


def gen_cyberscape(r, k, prog, kind="main"):
    """Cyberscape / future ambient: glassy FM pads, DX-bell arps through ping-pong delays, digital rain
    (random high plinks, stuttered and shimmered), a sub heartbeat, a filter-swept supersaw; kind=full
    adds a skippy future-garage beat; kind=intro is pads + rain."""
    pp = {"type": "delay", "time": r.choice(["3/16", "1/8", "3/8"]), "feedback": 0.45, "ping_pong": True, "tone": 4000, "mix": 0.3}
    shimmer = [{"type": "pitch", "semitones": 12, "mix": 0.3}, {"type": "reverb", "kind": "hall", "decay": "6s", "mix": 0.5}]
    out = [dict(t, name="glass", gain="-6dB") for t in gen_pad(r, k, prog, 55, pick_patch("pad-glass", "pad"), vel=60)]
    rain = " ".join((f"{mname(k.deg(r.choice([0, 2, 4, 6, 7, 9]), 79))}/16@{r.choice([50, 60, 70])}" if r.random() < 0.14 else "R/16") for _ in range(64))
    out.append(track("rain", pick_patch("dx-epiano", "celesta"), rain, pan=round(r.uniform(-0.4, 0.4), 2),
                     fx=[{"type": "stutter", "slice": "1/32", "repeats": 3, "chance": 0.3, "seed": r.randrange(1000)}] + shimmer, gain="-8dB"))
    if kind == "intro":
        return out
    arp = []
    for root in prog:
        tones = [k.deg(root + d, 67) for d in (0, 2, 4, 6, 7)]
        arp += [f"{mname(tones[j % len(tones)] if r.random() > 0.1 else tones[0] + 12)}/16@{70 if j % 3 == 0 else 56}" for j in range(16)]
    sweep = {"cut": {"points": [["0b", 0.1], ["8b", 0.8], ["16b", 0.2]]}}
    out += [track("arp", pick_patch("dx-epiano", "pluck-lead"), " ".join(arp), pan=0.2, fx=[pp], gain="-4dB"),
            track("pulse", pick_patch("sub-sine", "808-sub"), " ".join(f"{mname(k.deg(root, 28))}/4@{90} R/4 {mname(k.deg(root, 28))}/8@{70} R/8 R/4" for root in prog), gain="-6dB"),
            track("saw", pick_patch("supersaw", "pad"), " ".join(f"{chordhead([k.deg(root + d, 52) for d in (0, 2, 4)])}/1@{56}" for root in prog), gain="-14dB",
                  fx=[{"type": "filter", "kind": "lp", "cutoff": {"value": 600, "mod": [{"src": "auto.cut", "amount": 2.5}]}, "q": 0.8}], auto=sweep)]
    if kind == "full":
        kit = rig("drums")
        out += [track("rim", kit, "swing16=0.6 " + " ".join(("rc/16@72" if x in (4, 12) else ("rc/16@40" if x == 14 and r.random() < 0.4 else "R/16")) for _ in range(4) for x in range(16)), gain="-6dB"),
                track("kick", kit, "swing16=0.6 " + " ".join(("k/16@84" if x in (0, 7, 10) and (x == 0 or r.random() < 0.5) else "R/16") for _ in range(4) for x in range(16)), gain="-6dB"),
                track("hats", kit, "swing16=0.6 " + " ".join((f"h/16@{48 if x % 4 == 2 else 34}" if r.random() < 0.7 else "R/16") for _ in range(4) for x in range(16)), pan=0.2, gain="-6dB")]
    return out


def drunk(slots):
    """Unquantized 16ths: slots = [(token or None, offset 0..3 in 1/128-note sub-steps)], each hit
    delayed by its offset (≈20 ms per step at ~88 BPM) and held so every slot is exactly a 16th."""
    out = []
    for tok, off in slots:
        if tok is None:
            out.append("R/16")
            continue
        off = max(0, min(3, off))
        out.append(" ".join(["R/128"] * off + [tok.replace("/16", "/128")] + ["_"] * (7 - off)))
    return " ".join(out)


def gen_neosoul(r, k, prog, kind="main"):
    """Neo-soul / Dilla jazz-hop: drunk unquantized drums (kick on the grid, snare late, hats drifting
    with uneven velocities, lazy ghosts), rotary Rhodes 9/11/13 voicings, syncopated finger bass a
    touch behind; kind=full adds a Wurlitzer; kind=intro is keys alone."""
    keys = []
    for root in prog:
        ch = chordhead([k.deg(root + d, 50) for d in r.choice([[0, 2, 4, 6, 8], [2, 4, 6, 8, 10], [0, 4, 6, 8, 12], [2, 6, 8, 11]])])
        keys.append(r.choice([f"{ch}/4.@72 {ch}/8@60^gate=0.6 R/4 {ch}/4@66", f"R/8 {ch}/4.@70 R/4 {ch}/4@64", f"{ch}/2@72 R/8 {ch}/4.@62"]))
    out = [track("keys", pick_patch("rhodes-rotary", "rhodes"), "swing16=0.58 " + " ".join(keys), pan=-0.15)]
    if kind == "intro":
        return out
    kit = rig("drums")
    kpat = r.choice(["x.......x.x.....", "x......x..x.....", "x.......x..x..x."])
    kick, snare, hats, bass = [], [], [], []
    for bar in range(4):
        root = prog[bar % len(prog)]
        for x in range(16):
            kick.append((f"k/16@{r.choice([92, 98, 104])}", 0) if kpat[x] == "x" else (None, 0))
            if x in (4, 12):
                snare.append((f"s/16@{r.choice([96, 102])}", r.choice([1, 2, 2, 3])))
            elif r.random() < 0.12:
                snare.append((f"g/16@{r.choice([24, 30, 36])}", r.choice([1, 2, 3])))
            else:
                snare.append((None, 0))
            hats.append((f"h/16@{r.choice([40, 48, 56, 64]) if x % 2 == 0 else r.choice([28, 34, 40])}", r.choice([0, 1, 1, 2])) if r.random() < 0.85 else (None, 0))
            bnote = {0: 0, 3: 0, 6: 4, 10: r.choice([2, 4, 6]), 14: r.choice([5, 6])}.get(x)
            bass.append((f"{mname(k.deg(root + bnote, 33))}/16@{r.choice([84, 90, 96])}", 1) if bnote is not None and (x in (0, 6) or r.random() < 0.7) else (None, 0))
    out += [track("kick", kit, drunk(kick), gain="-4dB"), track("snare", kit, drunk(snare), gain="-3dB"), track("hats", kit, drunk(hats), pan=0.15, gain="-5dB"),
            track("bass", pick_patch("finger-bass", "fretless"), drunk(bass), seed=7)]
    if kind == "full":
        out.append(track("wurli", pick_patch("wurli", "rhodes"), " ".join(f"R/4 {chordhead([k.deg(root + d, 62) for d in (2, 4, 6)])}/8@56^gate=0.5 R/8 R/2" for root in prog), pan=0.3, gain="-6dB"))
    return out


def gen_minimal(r, k, prog, kind="pulse"):
    """Minimalism (Reich / Glass). kind=phase: a 12-note marimba figure left, the same figure with an
    extra rest (13 steps) right — they drift apart and back (Piano Phase). kind=additive: an organ
    figure that grows a note per cycle (Glass). kind=pulse: pulsing 8th chords on marimba + piano
    swelling each bar, a pulsing bass and long string swells (Music for 18 Musicians). kind=full:
    pulse + phase."""
    root0 = prog[0]
    fig = [k.deg(root0 + d, 64) for d in r.choice([[0, 1, 4, 5, 6, 1, 0, 5, 4, 1, 6, 5], [0, 2, 4, 2, 7, 4, 2, 4, 0, 2, 7, 4], [4, 0, 2, 0, 5, 2, 4, 2, 6, 4, 2, 0]])]
    def stream(cells, n=64, vel=74):
        return " ".join((f"{mname(cells[i % len(cells)])}/16@{vel if i % 4 == 0 else vel - 10}" if cells[i % len(cells)] is not None else "R/16") for i in range(n))
    out = []
    if kind in ("phase", "full"):
        out += [track("phaseL", pick_patch("marimba", "vibes"), stream(fig), pan=-0.5),
                track("phaseR", pick_patch("marimba" if kind == "phase" else "vibes", "vibes"), stream(fig + [None], vel=68), pan=0.5)]
    if kind == "additive":
        tones = [k.deg(root0 + d, 60) for d in r.choice([[0, 2, 4, 7, 9, 7, 4, 2], [0, 4, 2, 4, 7, 4, 9, 7], [0, 2, 0, 4, 0, 5, 0, 7]])]
        seq, n = [], 2
        while len(seq) < 64:
            seq += tones[:n]
            n = n + 1 if n < len(tones) else 2
        out.append(track("organ", pick_patch("farfisa", "organ"), " ".join(f"{mname(m)}/16@{72 if j % 2 == 0 else 62}" for j, m in enumerate(seq[:64])), pan=-0.1))
        out.append(track("bass", pick_patch("finger-bass", "upright-bass"), " ".join(f"{mname(k.deg(root, 33))}/4@{70}" for root in prog for _ in range(4)), seed=7, gain="-4dB"))
    if kind in ("pulse", "full"):
        swell = [56, 62, 70, 78, 84, 78, 70, 62]
        mar, pno, bass = [], [], []
        for root in prog:
            ch = chordhead([k.deg(root + d, 60) for d in (0, 2, 4, 7)])
            low = chordhead([k.deg(root + d, 48) for d in (0, 4, 7)])
            mar += [f"{ch}/8@{v}" for v in swell]
            pno += [f"{low}/8@{v - 8}" if j % 2 else "R/8" for j, v in enumerate(swell)]
            bass += [f"{mname(k.deg(root, 33))}/8@{v - 6}" for v in swell]
        out += [track("marimba", pick_patch("marimba", "vibes"), " ".join(mar), pan=-0.2, gain="-3dB"),
                track("piano", "piano", " ".join(pno), pan=0.2, gain="-4dB"),
                track("pulsebass", pick_patch("finger-bass", "upright-bass"), " ".join(bass), seed=7, gain="-4dB")]
        out += [dict(t, name="swell") for t in gen_pad(r, k, prog, 55, pick_patch("strings", "pad"), gain="-10dB", vel=60)]
    return out


def gen_berlin(r, k, prog, kind="main"):
    """Berlin school (Tangerine Dream / Schulze): a hypnotic 16th sequencer ostinato transposed per
    bar under a slow filter sweep (automation), Mellotron choir chords; kind=full adds a 12-step
    counter-sequence an octave up phasing against it; kind=drive adds a soft electro kick."""
    cell = r.choice([[0, 0, 7, 0, 12, 0, 7, 10], [0, 7, 12, 7, 0, 7, 10, 7], [0, 12, 0, 7, 0, 12, 3, 7], [0, 0, 12, 0, 7, 0, 10, 12]])
    seq = []
    for root in prog:
        base = k.deg(root, 33)
        seq += [f"{mname(base + cell[j % 8])}/16@{90 if j % 8 == 0 else (82 if j % 4 == 0 else 70)}" for j in range(16)]
    shape = r.choice([[0.1, 0.9, 0.2], [0.2, 0.5, 1.0], [0.8, 0.2, 0.7]])
    sweep = {"sw": {"points": [["0b", shape[0]], ["8b", shape[1]], ["16b", shape[2]]]}}
    out = [track("seq", pick_patch("moog-seq", "acid"), " ".join(seq), auto=sweep, gain="-2dB",
                 fx=[{"type": "filter", "kind": "lp", "cutoff": {"value": 500, "mod": [{"src": "auto.sw", "amount": 3.0}]}, "q": 0.7}])]
    out += [dict(t, name="choir") for t in gen_pad(r, k, prog, 52, pick_patch("mellotron-choir", "choir"), gain="-4dB", vel=62)]
    if kind == "full":
        c2 = r.choice([[0, 7, 12, 7, 3, 7, 12, 15, 12, 7, 3, 7], [12, 7, 0, 7, 10, 7, 12, 7, 3, 7, 0, 7]])
        root0 = k.deg(prog[0], 45)
        out.append(track("seq2", pick_patch("moog-seq", "acid"), " ".join(f"{mname(root0 + c2[j % 12])}/16@{80 if j % 12 == 0 else 62}" for j in range(64)), pan=0.4, gain="-6dB"))
    if kind == "drive":
        kit = pick_patch("electro-kit", "tight-kit")
        out.append(track("kick", kit, " ".join("k/4@64" for _ in range(16)), gain="-6dB"))
    return out


def gen_satie(r, k, prog, kind="main"):
    """Satie / Gymnopédie in 3/4 (24 beats = 8 bars, 2 per chord): the left hand's bass on 1 and a
    soft maj7/9 chord on 2 held through 3; a slow falling right-hand melody in dotted halves and
    quarter–half figures (kind main/full); strings under it in kind=full; kind=piano is the left hand."""
    lh, rh = [], []
    m = k.deg(prog[0] + r.choice([4, 6, 7]), 67)
    for bar in range(8):
        root = prog[(bar // 2) % len(prog)]
        ch = chordhead([k.deg(root + d, 55) for d in r.choice([[2, 4, 6], [4, 6, 8], [2, 6, 8]])])
        lh.append(f"{mname(k.deg(root, 40))}/4@{58} {ch}/2@{50}")
        tones = [k.deg(root + d, 64) for d in (0, 2, 4, 6, 7, 9)]
        near = min(tones, key=lambda t: abs(t - m))
        step = r.choice([-1, -1, -2, 0, 1])
        m = max(62, min(79, near + (0 if step == 0 else (2 if step > 0 else -1) * abs(step))))
        rh.append(r.choice([f"{mname(m)}/2.@{60}", f"{mname(m + 2)}/4@{56} {mname(m)}/2@{62}", f"R/4 {mname(m)}/2@{60}"]))
    room = expand(["rack:piano-room"])
    out = [track("lh", "piano", " ".join(lh), pan=-0.15, fx=room)]
    if kind == "piano":
        return out
    out.append(track("rh", "piano", " ".join(rh), pan=0.15, fx=room))
    if kind == "full":
        out.append(track("strings", pick_patch("strings", "pad"), " ".join(f"{chordhead([k.deg(prog[(b // 2) % len(prog)] + d, 48) for d in (0, 4)])}/2.@{52}" for b in range(8)), gain="-12dB"))
    return out


def gen_kankyo(r, k, prog, kind="main"):
    """Kankyō ongaku (Yoshimura / Ashikawa): a small pentatonic motif on DX piano, celesta or marimba
    repeating gently with long rests and small variations through a ping-pong delay, soft glass pads,
    a quiet sine bass; kind=water adds music-box / kalimba droplets; kind=intro is pads alone."""
    pt = penta(k)
    hall = {"type": "reverb", "kind": "hall", "decay": "4s", "predelay": "30ms", "mix": 0.3}
    pp = {"type": "delay", "time": "3/16", "feedback": 0.4, "ping_pong": True, "tone": 3500, "mix": 0.28}
    pads = [dict(t, name="glass", gain="-7dB") for t in gen_pad(r, k, prog, 57, pick_patch("pad-glass", "pad"), vel=56)]
    if kind == "intro":
        return pads
    cell = [(r.choice(pt) if r.random() > 0.25 else None, r.choice(["/4", "/8", "/8"])) for _ in range(r.choice([5, 6, 7]))]
    motif = []
    for root in prog:
        beats, toks = 0.0, []
        for d, ln in cell:
            dur = 1.0 if ln == "/4" else 0.5
            if beats + dur > 4:
                break
            if d is not None and r.random() < 0.3:  # small variation: a neighbour pentatonic step
                d = pt[(pt.index(d) + r.choice([-1, 1])) % 5]
            toks.append(f"{mname(k.deg(root + d, 67))}{ln}@{r.choice([58, 64, 70])}" if d is not None else f"R{ln}")
            beats += dur
        rest = 4 - beats
        while rest > 0:
            ln, dur = ("/2", 2.0) if rest >= 2 else (("/4", 1.0) if rest >= 1 else ("/8", 0.5))
            toks.append(f"R{ln}"); rest -= dur
        motif.append(" ".join(toks))
    voice = pick_patch(r.choice(["dx-epiano", "celesta", "marimba"]), "rhodes")
    out = pads + [track("motif", voice, " ".join(motif), pan=round(r.uniform(-0.3, 0.3), 2), fx=[pp, hall]),
                  track("sine", pick_patch("sub-sine", "pad"), " ".join(f"{mname(k.deg(root, 36))}/1@{60}" if j % 2 == 0 else "R/1" for j, root in enumerate(prog)), gain="-10dB")]
    if kind == "water":
        drops = " ".join((f"{mname(k.deg(r.choice(pt), 79))}/16@{r.choice([44, 52, 60])}" if r.random() < 0.08 else "R/16") for _ in range(64))
        out.append(track("drops", pick_patch(r.choice(["music-box", "kalimba"]), "celesta"), drops, pan=round(r.uniform(-0.5, 0.5), 2), fx=[hall], gain="-4dB"))
    return out


def gen_handpan(r, k, prog, kind="main"):
    """Handpan meditation: the ding (low centre note) on 1 and sometimes 3, an eight-note tone field
    played hand-to-hand on a 16th cell with accents and a slow melodic contour, a soft drone; kind=full
    adds a frame drum and shaker; kalimba sparkles; kind=intro is ding + drone."""
    ding = k.deg(0, 50)
    field = [k.deg(d, 57) for d in range(8)]
    cell = r.choice(["x.x.xx.x..x.x.x.", "x..x.x.xx.x..x.x", "x.xx.x..x.xx.x.."])
    drone = [dict(t, gain="-12dB") for t in gen_drone(k, 38, pick_patch("drone", "tanpura"))]
    hp = pick_patch("handpan", "kalimba")
    pan_t, dg = [], []
    pos = r.randrange(8)
    for bar, root in enumerate(prog):
        dg.append(f"{mname(ding)}/2@{88}" + (f" {mname(ding)}/2@{76}" if r.random() < 0.4 else " R/2"))
        for x, c in enumerate(cell):
            if c == "x" and x not in (0,):
                pos = max(0, min(7, pos + r.choice([-2, -1, 1, 1, 2])))
                pan_t.append(f"{mname(field[pos])}/16@{80 if x % 4 == 0 else r.choice([58, 64, 70])}")
            else:
                pan_t.append("R/16")
    out = drone + [track("ding", hp, " ".join(dg), pan=0.0)]
    if kind == "intro":
        return out
    out.append(track("tones", hp, " ".join(pan_t), pan=round(r.uniform(-0.25, 0.25), 2)))
    out.append(track("kalimba", pick_patch("kalimba", "celesta"), " ".join((f"{mname(field[r.randrange(8)] + 12)}/16@{50}" if r.random() < 0.05 else "R/16") for _ in range(64)), pan=0.4, gain="-6dB"))
    if kind == "full":
        out += [track("frame", pick_patch("bodhran", "tight-kit"), " ".join(("b/16@74" if x in (0, 10) else ("t/16@54" if x in (4, 12, 14) else "R/16")) for _ in range(4) for x in range(16)), pan=-0.15, gain="-4dB"),
                track("shaker", pick_patch("djembe", "tight-kit"), " ".join(("sh/16@" + str(50 if x % 4 == 2 else 38)) if x % 2 == 0 else "R/16" for _ in range(4) for x in range(16)), pan=0.3, gain="-4dB")]
    return out


def gen_citypop(r, k, prog, kind="main"):
    """City pop (Yamashita / Takeuchi): light disco drums (kick on the beats, snare 2 and 4, 16th hats,
    open hats on the offbeats), slap-bass octave pops, 16th cutting-guitar chops, DX maj7/9 chords;
    kind=full adds brass stabs on the bar-end anticipations; kind=intro is keys + guitar."""
    chop = r.choice(["..x...x...x.x.x.", ".x..x...x.x..x..", "..x.x...x...x.xx"])
    keys, gtr, bass, brass = [], [], [], []
    for root in prog:
        ch = chordhead([k.deg(root + d, 55) for d in r.choice([[0, 2, 4, 6], [2, 4, 6, 8], [0, 4, 6, 8]])])
        g = chordhead([k.deg(root + d, 52) for d in (2, 4, 6)])
        keys.append(r.choice([f"{ch}/4.@70 {ch}/8@62^gate=0.5 R/4 {ch}/4@66", f"R/8 {ch}/4.@70 R/8 {ch}/4.@64"]))
        gtr += [f"{g}/16@{r.choice([78, 86])}^gate=0.25" if c == "x" else "R/16" for c in chop]
        lo, hi = mname(k.deg(root, 28)), mname(k.deg(root, 40))
        bass += [f"{lo}/16@92", "R/16", f"{hi}/16@84", f"{lo}/16@76", "R/16", f"{hi}/16@88", "R/16", f"{lo}/16@80",
                 f"{lo}/16@90", "R/16", f"{mname(k.deg(root + 4, 28))}/16@84", "R/16", f"{hi}/16@86", "R/16", f"{lo}/16@78", f"{hi}/16@82"]
        brass.append(f"R/2 R/4 R/8 R/16 {chordhead([k.deg(root + d, 60) for d in (0, 2, 4)])}/16@104")
    out = [track("keys", pick_patch("dx-epiano", "rhodes"), " ".join(keys), pan=-0.2),
           track("gtr", pick_patch("cutting-guitar", "tele"), " ".join(gtr), pan=0.3, gain="2dB")]
    if kind == "intro":
        return out
    kit = pick_patch("electro-kit", "tight-kit")  # LinnDrum-ish, softer crack than the metal-derived kit
    out += [track("bass", pick_patch("slap-bass", "finger-bass"), " ".join(bass), seed=7, gain="-4dB"),
            track("kick", kit, " ".join(("k/16@96" if x % 4 == 0 or (x == 10 and r.random() < 0.3) else "R/16") for _ in range(4) for x in range(16)), gain="-6dB"),
            track("snare", kit, " ".join(("s/16@96" if x in (4, 12) else ("rs/16@34" if r.random() < 0.08 else "R/16")) for _ in range(4) for x in range(16)), gain="-6dB"),
            track("hats", kit, " ".join(("oh/16@70" if x % 4 == 2 else f"h/16@{54 if x % 2 == 0 else 40}") for _ in range(4) for x in range(16)), pan=0.15, gain="-6dB")]
    if kind == "full":
        out.append(track("brass", pick_patch("brass-stab", "brass"), " ".join(brass), pan=-0.1, gain="-7dB"))
    return out


def gen_lid(r, k, prog, kind="A"):
    """Orchestral drone (Stars of the Lid / Eluvium): huge sustained chords on several layers, each
    entering offset so harmony changes crossfade, each swelling up and down by automation over the
    section; a rare soft piano note. kind: intro (glass), A (strings + horn), B (cellos + glass +
    horn), low (cellos + glass)."""
    layers = {"intro": ["pad-glass"], "A": ["strings", "horn"], "B": ["cellos", "pad-glass", "horn"], "low": ["cellos", "pad-glass"]}[kind]
    hall = {"type": "reverb", "kind": "hall", "decay": "6s", "predelay": "40ms", "low_cut": 120, "mix": 0.42}
    out = []
    for li, patch in enumerate(layers):
        off = [0, 2, 4, 6][li % 4] + r.choice([0, 1])
        base = {"pad-glass": 60, "strings": 55, "horn": 50, "cellos": 43}.get(patch, 52)
        q = ["R/4"] * off
        seg = 0
        while len(q) < 16:
            root = prog[(seg * 2 + li) % len(prog)]
            ch = chordhead([k.deg(root + d, base) for d in r.choice([[0, 4], [0, 2, 4], [0, 4, 9], [2, 4, 7]])])
            q += [f"{ch}/4@{r.choice([58, 64])}"] + ["_"] * 7
            seg += 1
        q = q[:16]
        if q[-1] == "_" and q[-2] == "_" and all(x == "_" for x in q[-1:]):
            pass
        peak = r.choice([4, 8, 12])
        sw = {f"sw{li}": {"points": [["0b", 0.15], [f"{peak}b", 1.0], ["16b", 0.25]]}}
        out.append(track(f"drone{li}", pick_patch(patch, "strings"), " ".join(q), auto=sw, fx=[hall], pan=round([-0.35, 0.35, 0.0][li % 3], 2),
                         gain={"value": "-12dB", "mod": [{"src": f"auto.sw{li}", "amount": 8}]}))
    if kind != "intro" and r.random() < 0.5:
        pos = r.randrange(4, 14)
        q = ["R/4"] * 16
        q[pos] = f"{mname(k.deg(r.choice([0, 2, 4]), 72))}/4@{40}"
        out.append(track("piano", "piano", " ".join(q), fx=[hall], gain="-6dB", pan=0.2))
    return out


def gen_tiersen(r, k, prog, kind="main", lead=None):
    """Amélie / Yann Tiersen waltz in 3/4 (24 beats = 8 bars, 2 per chord): an oom-pah-pah left hand
    (piano bass on 1, chords on 2 and 3 — or accordion on 2 and 3), a melody on toy piano / glock /
    accordion / tremolo mandolin; kind=full adds running piano 8th arpeggios; kind=intro: left hand."""
    acc = r.random() < 0.5
    lh, arp, mel = [], [], []
    m = k.deg(prog[0] + r.choice([2, 4]), 67)
    lead = lead or pick_patch(r.choice(["toy-piano", "glock", "accordion", "mandolin"]), "celesta")
    for bar in range(8):
        root = prog[(bar // 2) % len(prog)]
        ch = chordhead([k.deg(root + d, 55) for d in (0, 2, 4)])
        lh.append(f"{mname(k.deg(root, 40))}/4@{70} {ch}/4@{56} {ch}/4@{54}")
        tones = [k.deg(root + d, 60) for d in (0, 2, 4, 7, 9, 11)]
        arp += [f"{mname(t)}/8@{58 if j % 2 == 0 else 50}" for j, t in enumerate([tones[i % 6] for i in r.choice([[0, 1, 2, 3, 2, 1], [0, 2, 1, 3, 4, 2], [3, 2, 1, 0, 1, 2]])])]
        figs = r.choice([[1, 1, 1], [2, 1], [3], [1, 2]])
        bar_t = []
        for ln in figs:
            m = max(64, min(81, m + r.choice([-2, -1, 1, 1, 2])))
            n = mname(k.deg(prog[(bar // 2) % len(prog)] + r.choice([0, 2, 4]), 67)) if r.random() < 0.4 else mname(m)
            if "mandolin" in lead and ln >= 2:  # tremolo: repeated 32nds
                bar_t.append(f"[ {n}/32@{r.choice([70, 76])} ]x{ln * 8}")
            else:
                bar_t.append(f"{n}/{ {1: '4', 2: '2', 3: '2.'}[ln] }@{r.choice([72, 80, 86])}")
        mel.append(" ".join(bar_t))
    if acc:
        left = [track("bass", "piano", " ".join(f"{mname(k.deg(prog[(b // 2) % len(prog)], 40))}/4@70 R/2" for b in range(8)), pan=-0.1),
                track("accordion", pick_patch("accordion", "organ"), " ".join(f"R/4 {chordhead([k.deg(prog[(b // 2) % len(prog)] + d, 55) for d in (0, 2, 4)])}/4@60 {chordhead([k.deg(prog[(b // 2) % len(prog)] + d, 55) for d in (0, 2, 4)])}/4@56" for b in range(8)), pan=-0.25, gain="-3dB")]
    else:
        left = [track("lh", "piano", " ".join(lh), pan=-0.15)]
    if kind == "intro":
        return left
    out = left + [track("melody", lead, " ".join(mel), pan=0.15)]
    if kind == "full":
        out.append(track("arp", "piano", " ".join(arp), pan=0.25, gain="-6dB"))
    return out


def gen_balearic(r, k, prog, kind="main"):
    """Balearic chill-out (Café del Mar): nylon arpeggios with a flamenco rasgueado flourish now and
    then, a soft slow-house kick + shaker, a congas/bongos tumbao, finger-bass root–fifth pulse and Rhodes
    on 1 and the and-of-2; kind=full adds a warm pad; kind=intro is the guitar alone."""
    gtr, bass, keys = [], [], []
    for bar, root in enumerate(prog):
        tones = [k.deg(root + d, 52) for d in (0, 4, 7, 9, 11)]
        if r.random() < 0.25:  # rasgueado: a quick strummed flourish into the bar's last beat
            ch = chordhead([k.deg(root + d, 52) for d in (0, 2, 4, 7)])
            gtr += [f"{mname(tones[i])}/8@{70 if i % 2 else 78}" for i in (0, 1, 2, 3, 2, 1)] + [f"{ch}/32@{60 + 8 * j}" for j in range(4)] + [f"{ch}/8@96"]
        else:
            seq = r.choice([[0, 1, 2, 3, 2, 1, 2, 4], [0, 2, 1, 3, 2, 4, 3, 1], [0, 1, 2, 1, 3, 2, 4, 2]])
            gtr += [f"{mname(tones[i])}/8@{78 if j % 4 == 0 else 64}" for j, i in enumerate(seq)]
        bass.append(f"{mname(k.deg(root, 33))}/4@84 R/8 {mname(k.deg(root + 4, 33))}/8@72 {mname(k.deg(root, 33))}/4@80 R/4")
        keys.append(f"{chordhead([k.deg(root + d, 57) for d in (2, 4, 6)])}/4@58 R/8 {chordhead([k.deg(root + d, 57) for d in (2, 4, 6)])}/8@52^gate=0.6 R/2")
    out = [track("nylon", pick_patch("nylon", "acoustic"), " ".join(gtr), pan=-0.2)]
    if kind == "intro":
        return out
    kit = pick_patch("electro-kit", "tight-kit")
    tumbao = r.choice(["o.mu.sl.o.lo.mu.", "mu.sl.o.o.lo.sl.", "o.sl.mu.bh.bl.lo."])
    toks = []
    for _ in range(4):
        i = 0
        while i < len(tumbao) and len(toks) % 16 < 16:
            ch_ = tumbao[i]
            if ch_ == ".":
                toks.append("R/16"); i += 1
            else:
                piece = tumbao[i:i + 2] if tumbao[i:i + 2] in ("mu", "sl", "lo", "bh", "bl") else tumbao[i]
                toks.append(f"{piece}/16@{r.choice([70, 78, 86])}"); i += len(piece)
        while len(toks) % 16:
            toks.append("R/16")
    out += [track("kick", kit, " ".join(("k/16@84" if x % 4 == 0 else "R/16") for _ in range(4) for x in range(16)), gain="-6dB"),
            track("shaker", pick_patch("djembe", "tight-kit"), " ".join(f"sh/16@{48 if x % 4 == 2 else 36}" for _ in range(4) for x in range(16)), pan=0.3, gain="-5dB"),
            track("congas", pick_patch("congas", "djembe"), " ".join(toks[:64]), pan=0.2, gain="-3dB"),
            track("bass", pick_patch("finger-bass", "upright-bass"), " ".join(bass), seed=7),
            track("rhodes", pick_patch("rhodes", "piano"), " ".join(keys), pan=0.15, gain="-4dB")]
    if kind == "full":
        out += [dict(t, name="pad") for t in gen_pad(r, k, prog, 55, pick_patch("pad-glass", "strings"), gain="-10dB", vel=56)]
    return out


def gen_chillwave(r, k, prog, kind="main"):
    """Chillwave / dream pop (Washed Out / Beach House / Toro y Moi): a hazy Juno pad bed pumping to the
    beat (gain automation), chorused bass, reverb-drenched clean guitar arpeggios, an electro kick /
    snare+clap / soft hats; kind=full adds wordless dream 'ooh's; kind=intro is the pads."""
    pump = {"pump": {"points": sum(([[f"{b}b", 0.0], [f"{b + 0.25:g}b", 0.35], [f"{b + 0.9:g}b", 1.0]] for b in range(16)), []) + [["16b", 1.0]]}}
    pump_gain = lambda base: {"value": base, "mod": [{"src": "auto.pump", "amount": 4}]}
    pads = " ".join(f"{chordhead([k.deg(root + d, 52) for d in r.choice([[0, 2, 4, 6], [0, 2, 4, 8], [0, 4, 6, 9]])])}/1@{62}" for root in prog)
    out = [track("juno", pick_patch("juno-pad", "pad"), pads, auto=pump, gain=pump_gain("-6dB"))]
    if kind == "intro":
        return out
    gtr = []
    for root in prog:
        tones = [k.deg(root + d, 60) for d in (0, 2, 4, 7, 9)]
        gtr += [f"{mname(tones[i])}/8@{70 if j % 4 == 0 else 58}" for j, i in enumerate(r.choice([[0, 2, 4, 2, 3, 2, 1, 2], [4, 2, 0, 2, 3, 1, 2, 0]]))]
    bass = " ".join(f"{mname(k.deg(root, 33))}/4.@84 {mname(k.deg(root, 45))}/8@70 R/8 {mname(k.deg(root + 4, 33))}/8@76 {mname(k.deg(root, 33))}/4@80" for root in prog)
    kit = pick_patch("electro-kit", "tight-kit")
    out += [track("gtr", pick_patch("clean-chorus", "tele"), " ".join(gtr), pan=0.3, gain="-3dB",
                  fx=[{"type": "delay", "time": "3/16", "feedback": 0.4, "ping_pong": True, "tone": 3000, "mix": 0.3}, {"type": "reverb", "kind": "hall", "decay": "3s", "mix": 0.35}]),
            track("bass", pick_patch("finger-bass", "fretless"), bass, seed=7, fx=[{"type": "chorus", "rate": 0.6, "depth": 0.3, "mix": 0.35}]),
            track("kick", kit, " ".join(("k/16@90" if x in (0, 6, 10) and (x != 10 or r.random() < 0.5) else "R/16") for _ in range(4) for x in range(16)), gain="-6dB"),
            track("snare", kit, " ".join(("s/16@84" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), gain="-7dB",
                  fx=[{"type": "reverb", "kind": "plate", "decay": "1.8s", "mix": 0.35}]),
            track("clap", kit, " ".join(("cp/16@64" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), gain="-9dB"),
            track("hats", kit, " ".join((f"h/16@{50 if x % 4 == 2 else 34}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16)), pan=0.2, gain="-8dB")]
    if kind == "full":
        out.append(track("oohs", pick_patch("dream-vox", "choir"), " ".join(f"{chordhead([k.deg(root + d, 60) for d in (0, 2, 4)])}/1@{60}" for root in prog), auto=pump, gain=pump_gain("-6dB")))
    return out


def gen_souljazz(r, k, prog, kind="main"):
    """Soul-jazz organ trio (Jimmy Smith / Lonnie Smith): Hammond comping with dominant 9/13 stabs on
    the swung offbeats, a walking bass, spang-a-lang ride with hat on 2 and 4, comping snare and a
    feathered kick; kind=full adds jazz-guitar stabs on 2 and 4; kind=intro is the organ."""
    sw = "swing=0.66 "
    organ, bass, gtr = [], [], []
    for bi, root in enumerate(prog):
        ch = chordhead([k.deg(root + d, 53) for d in r.choice([[2, 4, 6, 8], [4, 6, 8, 12], [2, 6, 8, 11]])])
        cell = r.choice([[None, 1, None, 1, None, None, 1, None], [None, 1, None, None, 1, None, None, 1], [1, None, None, 1, None, 1, None, None]])
        organ += [f"{ch}/8@{r.choice([78, 86])}^gate=0.5" if c else "R/8" for c in cell]
        nxt = prog[(bi + 1) % len(prog)]
        walk = [root, root + r.choice([1, 2]), root + r.choice([2, 4]), nxt + r.choice([-1, 1])]
        bass += [f"{mname(k.deg(d, 33))}/4@{84 if j == 0 else 74}" for j, d in enumerate(walk)]
        g = chordhead([k.deg(root + d, 55) for d in (2, 4, 6)])
        gtr.append(f"R/4 {g}/8@64^gate=0.4 R/8 R/4 {g}/8@60^gate=0.4 R/8")
    out = [track("organ", pick_patch("hammond-b3", "organ"), sw + " ".join(organ), pan=-0.1)]
    if kind == "intro":
        return out
    kit = rig("drums")
    ride = " ".join(("rd/8@70" if x % 2 == 0 else ("rd/8@54" if x in (3, 7) else "R/8")) for _ in range(4) for x in range(8))
    hat = " ".join(("hp/4@60" if x % 2 == 1 else "R/4") for _ in range(4) for x in range(4))
    snare = " ".join((f"g/8@{r.choice([28, 34, 40])}" if r.random() < 0.15 else "R/8") for _ in range(32))
    kick = " ".join("k/4@40" for _ in range(16))
    out += [track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(bass), seed=7),
            track("ride", kit, sw + ride, gain="-5dB"), track("hats", kit, hat, gain="-8dB"),
            track("snare", kit, sw + snare, gain="-6dB"), track("kick", kit, kick, gain="-8dB")]
    if kind == "full":
        out.append(track("gtr", pick_patch("jazz-box", "clean-chorus"), sw + " ".join(gtr), pan=0.3, gain="-4dB"))
    return out


def gen_ethiojazz(r, k, prog, kind="main"):
    """Ethio-jazz (Mulatu Astatke): a two-bar pentatonic bass ostinato (the heartbeat), a laid groove
    with tom accents, organ stabs; kind=full adds a horn-section riff (low, then answered an octave
    up); kind=intro is bass + organ."""
    pt = penta(k)
    root0 = prog[0]
    cell = r.choice([[0, None, 2, 0, None, 3, 4, None, 0, None, 2, 4, 3, None, 2, None],
                     [0, 0, None, 3, None, 2, None, 0, 4, None, 3, None, 2, 0, None, None],
                     [0, None, 4, 3, 2, None, 0, None, 0, None, 4, 3, None, 2, 3, None]])
    bass = " ".join((f"{mname(k.deg(root0 + pt[d], 33))}/8@{90 if j % 4 == 0 else 78}" if d is not None else "R/8") for _ in range(2) for j, d in enumerate(cell))
    organ = " ".join(f"R/4 {chordhead([k.deg(root + pt[d], 55) for d in (0, 2, 3)])}/8@{70}^gate=0.5 R/8 R/2" for root in prog)
    out = [track("bass", pick_patch("finger-bass", "upright-bass"), bass, seed=7),
           track("organ", pick_patch(r.choice(["farfisa", "hammond-b3"]), "organ"), organ, pan=-0.25, gain="-4dB")]
    if kind == "intro":
        return out
    kit = rig("drums")
    out += [track("kick", kit, " ".join(("k/16@88" if x in (0, 6, 10) else "R/16") for _ in range(4) for x in range(16)), gain="-5dB"),
            track("snare", kit, " ".join(("s/16@86" if x == 8 else ("g/16@32" if r.random() < 0.1 else "R/16")) for _ in range(4) for x in range(16)), gain="-5dB"),
            track("hats", kit, " ".join((f"h/16@{52 if x % 4 == 0 else 38}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16)), pan=0.2, gain="-7dB"),
            track("toms", kit, " ".join(((r.choice(["t2", "t3", "ft"]) + f"/16@{70}") if x in (12, 14) and r.random() < 0.6 else "R/16") for _ in range(4) for x in range(16)), gain="-9dB")]
    if kind == "full":
        riff = [pt[i] for i in r.choice([[0, 2, 3, 4, 3, 2], [4, 3, 2, 0, 2, 3], [0, 0, 2, 3, 4, 4]])]
        hs = []
        for bar in range(4):
            base = 57 if bar % 2 == 0 else 69
            hs.append(" ".join(f"{mname(k.deg(root0 + d, base))}/8@{96 if j == 0 else 86}" for j, d in enumerate(riff)) + " R/4")
        out.append(track("horns", pick_patch("horn-section", "brass"), " ".join(hs), pan=0.15, gain="-4dB"))
    return out


def gen_hauntology(r, k, prog, kind="main"):
    """Hauntology / Boards of Canada: drifting detuned Juno pads (a slow pitch wobble + tape grit),
    dusty low-passed boom-bap, a warm sine-saw bass; kind=full adds a warped music-box / celesta
    tune; kind=intro is the pads."""
    wob = [{"type": "pitch", "semitones": {"value": 0, "mod": [{"src": "lfo.wob", "amount": round(r.uniform(0.12, 0.22), 2)}]}, "grain": "70ms", "mix": 1.0},
           {"type": "crush", "bits": 12, "rate": 16000, "mix": 0.25}, {"type": "filter", "kind": "lp", "cutoff": 3500}]
    wl = {"wob": {"wave": "sine", "rate": f"{r.uniform(0.08, 0.16):.2f}hz"}}
    pads = " ".join(f"{chordhead([k.deg(root + d, 52) for d in r.choice([[0, 2, 4, 6], [0, 4, 6, 9], [0, 2, 4, 9]])])}/1@{60}" for root in prog)
    out = [track("pads", pick_patch("juno-pad", "pad"), pads, fx=wob, lfo=wl, gain="-2dB")]
    if kind == "intro":
        return out
    kit = pick_patch("lofi-kit", "tight-kit")
    dusty = [{"type": "filter", "kind": "lp", "cutoff": 3200}, {"type": "crush", "bits": 12, "rate": 14000, "mix": 0.3}]
    kp = r.choice(["x.......x.x.....", "x......x..x.....", "x.......x...x..."])
    out += [track("kick", kit, "swing16=0.58 " + " ".join(("k/16@92" if kp[x] == "x" else "R/16") for _ in range(4) for x in range(16)), fx=dusty, gain="-6dB"),
            track("snare", kit, "swing16=0.58 " + " ".join(("s/16@90" if x in (4, 12) else ("rs/16@30" if r.random() < 0.08 else "R/16")) for _ in range(4) for x in range(16)), fx=dusty, gain="-6dB"),
            track("hats", kit, "swing16=0.58 " + " ".join((f"h/16@{50 if x % 4 == 2 else 36}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16)), fx=dusty, pan=0.2, gain="-8dB"),
            track("bass", pick_patch("sub-sine", "finger-bass"), " ".join(f"{mname(k.deg(root, 33))}/4.@84 {mname(k.deg(root + 4, 33))}/8@70 {mname(k.deg(root, 33))}/2@78" for root in prog), seed=7, gain="2dB")]
    if kind == "full":
        tune = gen_hook(r, k, prog, 76, pick_patch(r.choice(["music-box", "celesta"]), "celesta"))
        out += [dict(t, name="tune", fx=wob, lfo=wl, gain="-6dB") for t in tune]
    return out


def gen_dawnchorus(r, k, prog, kind="main"):
    """Dawn chorus: synthesized birdsong (two species: quick high 32nd chirp clusters and a lower,
    slower caller) over a babbling stream; kind main adds soft glass pads, kind full sparse kalimba /
    handpan drops; kind=intro is water and birds."""
    pt = penta(k)
    def birds(base, p_, sub):
        toks = []
        for _ in range(16):
            if r.random() < p_:
                n = r.randint(2, 5) if sub == 32 else r.randint(1, 2)
                per = 8 if sub == 32 else 4
                toks += [f"{mname(k.deg(r.choice(pt) + 7 * r.choice([0, 1]), base))}/{sub}@{r.choice([60, 70, 80])}" for _ in range(n)] + [f"R/{sub}"] * (per - n)
            else:
                toks.append("R/4")
        return " ".join(toks)
    out = [track("birds", pick_patch("birds", "celesta"), birds(84, 0.25, 32), pan=round(r.uniform(-0.6, 0.6), 2)),
           track("birds2", pick_patch("birds", "celesta"), birds(76, 0.15, 16), pan=round(r.uniform(-0.6, 0.6), 2), gain="-4dB"),
           track("stream", pick_patch("stream", "wind"), "C5/4" + " _" * 15, pan=-0.2)]
    if kind == "intro":
        return out
    out += [dict(t, name="glass", gain="-9dB") for t in gen_pad(r, k, prog, 57, pick_patch("pad-glass", "pad"), vel=54)]
    if kind == "full":
        drops = " ".join((f"{mname(k.deg(r.choice(pt), 67))}/8@{r.choice([50, 58])}" if r.random() < 0.12 else "R/8") for _ in range(32))
        out.append(track("drops", pick_patch(r.choice(["kalimba", "handpan"]), "celesta"), drops, pan=0.3, gain="-3dB"))
    return out


CHOP_SOURCES = ["satie", "souljazz", "ballad", "neoclassical", "bossa", "kankyo", "lofihop", "ukjazz", "citypop", "tiersen", "dawnraga", "ethiojazz",
                "berlin", "guofeng", "mali", "handpan", "chillwave", "vaporwave", "celtic", "smile"]


def chop_patch(src):
    """A chop-SRC patch time-stretched so each slice lasts one beat of the song (library parts render
    at 120 BPM, so speed = tempo / 120; pitch is unchanged)."""
    base = pick_patch(f"chop-{src}", "chopper")
    return f"{base} layers.0.speed={_TEMPO / 120:.3f}" if base.startswith("chop-") else base


def chop_phrase(r, bars=4):
    """An MPC phrase: 8 eighth steps per bar, mostly runs of adjacent slices (they belong together),
    some rests; each bar flips a couple of steps."""
    a = r.randrange(0, 12)
    base = []
    for j in range(8):
        base.append(None if r.random() < 0.2 else (a + (j if r.random() < 0.7 else r.randrange(-2, 4))) % 16)
    out = []
    for b in range(bars):
        bar = list(base)
        for _ in range(2 if b % 2 else 1):
            bar[r.randrange(8)] = r.choice([None, r.randrange(16)])
        out += [f"{mname(60 + i)}/8@{r.choice([92, 100, 108])}" if i is not None else "R/8" for i in bar]
    return " ".join(out)


def gen_beattape(r, k, prog, kind="main", src=None, src2=None):
    """Beat tape (J Dilla / Nujabes / Madlib): a resampled library part chopped into 16 slices and
    re-sequenced into new phrases (flipped each bar) over dusty boom-bap, a soft tonic bass and vinyl;
    kind=full adds a second source as a counter-chop; kind=intro is the chops and vinyl."""
    src = src or r.choice(CHOP_SOURCES)
    out = [track("chops", chop_patch(src), chop_phrase(r)), track("vinyl", pick_patch("vinyl", "pad"), "C4/1 _ _ _", gain="-2dB")]
    if kind == "intro":
        return out
    kit = pick_patch("lofi-kit", "tight-kit")
    kp = r.choice(["x.....x...x.....", "x......x..x.x...", "x.......x.x....."])
    out += [track("kick", kit, "swing16=0.6 " + " ".join(("k/16@96" if kp[x] == "x" else "R/16") for _ in range(4) for x in range(16)), gain="-4dB"),
            track("snare", kit, "swing16=0.6 " + " ".join(("s/16@94" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), gain="-4dB"),
            track("hats", kit, "swing16=0.6 " + " ".join((f"h/16@{52 if x % 4 == 2 else 38}" if x % 2 == 0 else "R/16") for _ in range(4) for x in range(16)), pan=0.2, gain="-7dB"),
            track("bass", pick_patch("sub-sine", "finger-bass"), " ".join("C2/4@86 R/4 R/8 C2/8@70 R/4" for _ in range(4)), seed=7, gain="-7dB")]
    if kind == "full" and not LITE:
        s2 = src2 or r.choice([c for c in CHOP_SOURCES if c != src])
        out.append(track("chops2", chop_patch(s2), chop_phrase(r), pan=0.3, gain="-6dB"))
    return out


def gen_lofihouse(r, k, prog, kind="main", src=None, src2=None):
    """Lo-fi house (Ross from Friends / DJ Seinfeld): swung chops of a resampled library part pumping
    against a dusty four-on-the-floor (kick every beat, clap 2 and 4, open hats on the offbeats,
    shuffled closed hats, all crunchy), offbeat sub pulses, a soft C–G fifth pad; kind=full adds a
    counter-chop; kind=intro is chops and vinyl."""
    src = src or r.choice(CHOP_SOURCES)
    pump = {"pump": {"points": sum(([[f"{b}b", 0.0], [f"{b + 0.2:g}b", 0.4], [f"{b + 0.85:g}b", 1.0]] for b in range(16)), []) + [["16b", 1.0]]}}
    chops = "swing16=0.58 " + " ".join(tok.replace("/8@", "/16@") + " R/16" if tok != "R/8" else "R/8" for tok in chop_phrase(r).split())
    out = [track("chops", chop_patch(src), chops, auto=pump, gain={"value": "-4dB", "mod": [{"src": "auto.pump", "amount": 4}]}),
           track("vinyl", pick_patch("vinyl", "pad"), "C4/1 _ _ _", gain="-4dB")]
    if kind == "intro":
        return out
    kit = pick_patch("lofi-kit", "tight-kit")
    crunch = [{"type": "crush", "bits": 10, "rate": 14000, "mix": 0.35}, {"type": "filter", "kind": "lp", "cutoff": 6000}]
    out += [track("kick", kit, " ".join(("k/16@100" if x % 4 == 0 else "R/16") for _ in range(4) for x in range(16)), fx=crunch, gain="-4dB"),
            track("clap", kit, " ".join(("cp/16@86" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), fx=crunch, gain="-6dB"),
            track("hats", kit, "swing16=0.58 " + " ".join(("oh/16@64" if x % 4 == 2 else (f"h/16@{44}" if r.random() < 0.6 else "R/16")) for _ in range(4) for x in range(16)), fx=crunch, pan=0.2, gain="-8dB"),
            track("bass", pick_patch("sub-sine", "finger-bass"), " ".join("R/8 C2/8@84 R/8 C2/8@80 R/8 C2/8@84 R/8 G1/8@78" for _ in range(4)), seed=7, gain="-5dB"),
            track("pad", pick_patch("juno-pad", "pad"), "C3,G3/1@56 _ _ _", gain="-10dB", auto=pump)]
    if kind == "full" and not LITE:
        s2 = src2 or r.choice([c for c in CHOP_SOURCES if c != src])
        out.append(track("chops2", chop_patch(s2), chop_phrase(r), pan=0.35, gain="-8dB"))
    return out


def gen_amapiano(r, k, prog, kind="main"):
    """Amapiano (Kabza De Small / DJ Maphorisa): a syncopated log-drum bass line with glides, deep-house
    piano chords on the offbeats, a soft kick, rimshot syncopations, shaker 16ths, light congas and an
    open hat; kind=full adds a jazzy pad; kind=intro is piano and shaker."""
    piano = []
    logd = []
    for root in prog:
        ch = chordhead([k.deg(root + d, 55) for d in r.choice([[0, 2, 4, 6, 8], [2, 4, 6, 8], [0, 4, 6, 9]])])
        piano.append(" ".join(f"{ch}/8@{r.choice([66, 72])}^gate=0.6" if j % 2 == 1 and r.random() < 0.8 else "R/8" for j in range(8)))
        pos = sorted(set([0, r.choice([3, 6]), 10] + r.sample([7, 11, 13, 14], 2)))
        for x in range(16):
            if x in pos:
                d = r.choice([0, 0, 4, 7, 6])
                logd.append(f"{mname(k.deg(root + d, 33))}/16@{r.choice([92, 100, 108])}")
            else:
                logd.append("R/16")
    shaker = track("shaker", pick_patch("djembe", "tight-kit"), " ".join(f"sh/16@{50 if x % 4 == 2 else 36}" for _ in range(4) for x in range(16)), pan=0.3, gain="-5dB")
    out = [track("piano", "piano", " ".join(piano), pan=-0.15, fx=expand(["rack:piano-room"]), gain="-2dB"), shaker]
    if kind == "intro":
        return out
    kit = rig("drums")
    out += [track("logdrum", pick_patch("log-drum", "sub-sine"), " ".join(logd), seed=7, gain="-4dB"),
            track("kick", kit, " ".join(("k/16@80" if x % 4 == 0 else "R/16") for _ in range(4) for x in range(16)), gain="-7dB"),
            track("rim", kit, " ".join(("rc/16@70" if x in (3, 6, 11, 14) and r.random() < 0.7 else "R/16") for _ in range(4) for x in range(16)), gain="-6dB"),
            track("hats", kit, " ".join(("oh/16@58" if x % 4 == 2 else "R/16") for _ in range(4) for x in range(16)), pan=0.15, gain="-8dB"),
            track("congas", pick_patch("congas", "djembe"), " ".join((f"{r.choice(['o', 'mu', 'sl'])}/16@{r.choice([60, 70])}" if x in (2, 7, 9, 13) and r.random() < 0.6 else "R/16") for _ in range(4) for x in range(16)), pan=-0.25, gain="-6dB")]
    if kind == "full":
        out += [dict(t, name="pad") for t in gen_pad(r, k, prog, 57, pick_patch(r.choice(["pad-glass", "juno-pad"]), "pad"), gain="-10dB", vel=56)]
    return out


def gen_liquid(r, k, prog, kind="main"):
    """Liquid drum & bass (LTJ Bukem / Calibre): a two-step breakbeat (kick 1 and the and-of-3,
    snare 2 and 4) with rolling ghost snares and ride/shaker 16ths, a warm rolling sub line, Rhodes
    chords and atmospheric pads; kind=full adds dream oohs; kind=intro is pads + Rhodes."""
    rh = " ".join(f"{chordhead([k.deg(root + d, 55) for d in r.choice([[0, 2, 4, 6], [2, 4, 6, 8], [0, 4, 6, 9]])])}/2@{64} R/4 {chordhead([k.deg(root + d, 55) for d in (2, 4, 6)])}/4@{56}" for root in prog)
    out = [track("rhodes", pick_patch("rhodes", "piano"), rh, pan=-0.15, gain="-2dB")]
    out += [dict(t, name="atmos", gain="-10dB") for t in gen_pad(r, k, prog, 57, pick_patch("pad-glass", "pad"), vel=54)]
    if kind == "intro":
        return out
    kit = rig("drums")
    kick = " ".join(("k/16@96" if x in (0, 10) or (x == 14 and r.random() < 0.3) else "R/16") for _ in range(4) for x in range(16))
    snare = " ".join(("s/16@96" if x in (4, 12) else (f"g/16@{r.choice([26, 32, 38])}" if x in (7, 9, 15) and r.random() < 0.5 else "R/16")) for _ in range(4) for x in range(16))
    ride = " ".join((f"{r.choice(['rd', 'h'])}/16@{52 if x % 2 == 0 else 36}") for _ in range(4) for x in range(16))
    bass = []
    for root in prog:
        bass.append(f"{mname(k.deg(root, 28))}/4.@86 {mname(k.deg(root, 28))}/8@70 R/8 {mname(k.deg(root + r.choice([2, 4]), 28))}/8@76 {mname(k.deg(root, 28))}/4@80")
    out += [track("kick", kit, kick, gain="-5dB"), track("snare", kit, snare, gain="-5dB"), track("ride", kit, ride, pan=0.2, gain="-9dB"),
            track("sub", pick_patch("sub-sine", "finger-bass"), " ".join(bass), seed=7, gain="-1dB")]
    if kind == "full":
        out.append(track("oohs", pick_patch("dream-vox", "choir"), " ".join(f"{chordhead([k.deg(root + d, 60) for d in (0, 2, 4)])}/1@{58}" for root in prog), gain="-6dB"))
    return out


def gen_nujazz(r, k, prog, kind="main"):
    """Nu-jazz / jazz house (St Germain / Jazzanova): a shuffled house groove (four-on-the-floor kick,
    offbeat open hats, shaker, congas), a Rhodes vamp on m9/13 voicings, an upright line in 8ths;
    kind=full adds muted-trumpet stabs; kind=intro is the Rhodes and congas."""
    sw = "swing16=0.6 "
    rh, bass, stabs = [], [], []
    for root in prog:
        ch = chordhead([k.deg(root + d, 53) for d in r.choice([[0, 2, 4, 6, 8], [2, 4, 6, 8, 12], [0, 4, 6, 8, 11]])])
        rh.append(r.choice([f"R/8 {ch}/8@{70}^gate=0.5 R/4 R/8 {ch}/8@{64}^gate=0.5 R/4", f"{ch}/8@{72}^gate=0.5 R/8 R/8 {ch}/8@{62}^gate=0.5 R/4 {ch}/8@{66}^gate=0.5 R/8"]))
        walk = [root, root + 4, root + r.choice([5, 6]), root + r.choice([4, 2])]
        bass.append(" ".join(f"{mname(k.deg(d, 33))}/8@{84 if j % 2 == 0 else 72} {mname(k.deg(d, 33))}/8@{60}" if j % 2 == 0 else f"{mname(k.deg(d, 33))}/4@{76}" for j, d in enumerate(walk)))
        stabs.append(f"R/2 R/8 {chordhead([k.deg(root + d, 60) for d in (2, 4, 6)])}/8@{92}^gate=0.4 R/4")
    congas = " ".join((f"{r.choice(['o', 'mu', 'sl', 'bh'])}/16@{r.choice([60, 70])}" if x in (2, 5, 7, 10, 13, 15) and r.random() < 0.6 else "R/16") for _ in range(4) for x in range(16))
    out = [track("rhodes", pick_patch("rhodes", "piano"), sw + " ".join(rh), pan=-0.15), track("congas", pick_patch("congas", "djembe"), sw + congas, pan=0.25, gain="-6dB")]
    if kind == "intro":
        return out
    kit = rig("drums")
    out += [track("kick", kit, " ".join(("k/16@88" if x % 4 == 0 else "R/16") for _ in range(4) for x in range(16)), gain="-6dB"),
            track("hats", kit, sw + " ".join(("oh/16@60" if x % 4 == 2 else ("h/16@38" if x % 2 == 1 and r.random() < 0.6 else "R/16")) for _ in range(4) for x in range(16)), pan=0.15, gain="-8dB"),
            track("snare", kit, sw + " ".join(("rc/16@64" if x in (4, 12) else "R/16") for _ in range(4) for x in range(16)), gain="-6dB"),
            track("shaker", pick_patch("djembe", "tight-kit"), sw + " ".join(f"sh/16@{48 if x % 4 == 2 else 34}" for _ in range(4) for x in range(16)), pan=0.3, gain="-6dB"),
            track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(bass), seed=7)]
    if kind == "full":
        out.append(track("stabs", pick_patch("trumpet-mute", "horn-section"), " ".join(stabs), pan=0.2, gain="-4dB"))
    return out


def gen_highlife(r, k, prog, kind="main"):
    """Highlife (E.T. Mensah / Ebo Taylor / palm-wine) on a 12/8 triplet grid: two interlocking guitar
    arpeggios (even / odd steps, an octave apart), the standard bell pattern on agogô, shekere on the
    dotted quarters, a melodic bass, a soft kick and congas; kind=full adds horn stabs; kind=intro is
    the guitars and bell."""
    bell = "x.x.xx.x.x.x"
    g1, g2, bass, horns = [], [], [], []
    for root in prog:
        tones = [k.deg(root + d, 55) for d in (0, 2, 4, 7, 9, 4)]
        for j in range(12):
            t_ = tones[(j // 2) % 6]
            if j % 2 == 0:
                g1.append(f"{mname(t_)}/12@{80 if j % 6 == 0 else 66}"); g2.append("R/12")
            else:
                g2.append(f"{mname(t_ + 12)}/12@{70}"); g1.append("R/12")
        walk = [root, root + 2, root + 4, root + r.choice([2, 5, 6])]
        bass.append(" ".join(f"{mname(k.deg(d, 33))}/12@{84 if i == 0 else 74} _ _" for i, d in enumerate(walk)))
        horns.append("R/12 " * 9 + f"{chordhead([k.deg(root + d, 60) for d in (0, 2, 4)])}/12@{94} _ R/12")
    perc = pick_patch("afro-perc", "metal-kit")
    out = [track("gtr1", pick_patch("acoustic", "nylon"), " ".join(g1), pan=-0.3), track("gtr2", pick_patch("clean-chorus", "tele"), " ".join(g2), pan=0.3, gain="-3dB"),
           track("bell", perc, " ".join((f"ah/12@{84 if j == 0 else 72}" if bell[j] == "x" else ("al/12@60" if j == 3 else "R/12")) for _ in range(4) for j in range(12)), pan=0.15, gain="-4dB")]
    if kind == "intro":
        return out
    kit = rig("drums")
    out += [track("shekere", perc, " ".join(("sk/12@64" if j % 3 == 0 else "R/12") for _ in range(4) for j in range(12)), pan=-0.2, gain="-4dB"),
            track("kick", kit, " ".join(("k/12@80" if j in (0, 6) else "R/12") for _ in range(4) for j in range(12)), gain="-6dB"),
            track("congas", pick_patch("congas", "djembe"), " ".join((f"{r.choice(['o', 'mu', 'sl'])}/12@{r.choice([60, 70])}" if j in (2, 5, 8, 11) and r.random() < 0.6 else "R/12") for _ in range(4) for j in range(12)), pan=0.25, gain="-6dB"),
            track("bass", pick_patch("finger-bass", "upright-bass"), " ".join(bass), seed=7)]
    if kind == "full":
        out.append(track("horns", pick_patch("horn-section", "brass"), " ".join(horns), pan=0.1, gain="-5dB"))
    return out


def gen_samba(r, k, prog, kind="main"):
    """Samba-jazz (Tamba Trio / Jorge Ben / Sérgio Mendes): batucada core — surdo (muted 1, open 2),
    tamborim telecoteco, pandeiro jingles + thumb, ganzá — a cavaquinho strumming 16ths, a bass on the
    surdo; kind=full adds piano comping; kind=intro is cavaquinho + pandeiro."""
    kit = pick_patch("samba-kit", "tight-kit")
    tam = r.choice(["x..x..x...x..x..", "x.x..x.x..x.x..x", "x..x.x...x..x.x."])
    strum = r.choice(["x.xx.x.xx.xx.x.x", "x.x.xx.xx.x.xx.x", "xx.x.xx.x.xx.x.x"])
    cav, bass, pno = [], [], []
    for root in prog:
        ch = chordhead([k.deg(root + d, 60) for d in r.choice([[0, 2, 4, 6], [2, 4, 6, 8], [0, 4, 6, 8]])])
        cav += [f"{ch}/16@{82 if x % 4 == 0 else 66}^gate=0.5" if strum[x] == "x" else "R/16" for x in range(16)]
        b1, b5 = mname(k.deg(root, 33)), mname(k.deg(root + 4, 33))
        bass.append(f"{b1}/8.@84 {b5}/16@70 {b1}/4@80 {b1}/8.@82 {b5}/16@68 {b5}/4@76")
        pc_ = chordhead([k.deg(root + d, 53) for d in (2, 4, 6)])
        pno.append(f"R/8 {pc_}/8@{64}^gate=0.5 R/4 R/8 {pc_}/8@{60}^gate=0.5 R/8 {pc_}/8@{58}^gate=0.5")
    pandeiro = " ".join((f"pt/16@{72}" if x % 4 == 0 else f"pd/16@{58 if x % 4 == 3 else 44}") for _ in range(4) for x in range(16))
    out = [track("cavaquinho", pick_patch("cavaquinho", "nylon"), " ".join(cav), pan=-0.25), track("pandeiro", kit, pandeiro, pan=0.2)]
    if kind == "intro":
        return out
    out += [track("surdo", kit, " ".join(({0: "sm/16@74", 4: "sd/16@98", 8: "sm/16@72", 12: "sd/16@100"}.get(x, "R/16")) for _ in range(4) for x in range(16))),
            track("tamborim", kit, " ".join((f"tm/16@{84 if x % 4 == 0 else 74}" if tam[x] == "x" else "R/16") for _ in range(4) for x in range(16)), pan=-0.1),
            track("ganza", kit, " ".join(f"gz/16@{52 if x % 2 == 1 else 40}" for _ in range(4) for x in range(16)), pan=0.3),
            track("bass", pick_patch("finger-bass", "upright-bass"), " ".join(bass), seed=7)]
    if kind == "full":
        out.append(track("piano", "piano", " ".join(pno), pan=0.15, gain="-4dB"))
    return out


def gen_rumba(r, k, prog, kind="main"):
    """Rumba flamenca (Gipsy Kings / Paco de Lucía's rumbas): nylon rhythm guitar strumming the rumba
    pattern (open chords on the accents, muted slaps and up-strokes between), a syncopated bass, cajón
    (bass on 1/3, slaps on 2/4, ghosts) and palmas on the offbeats; kind=intro is the rhythm guitar."""
    strum = r.choice(["A.ms.uAm.us.Am.u", "A.mAu.m.A.mu.Am.", "Am.uA.mu.Am.uA.u"])
    gtr, bass = [], []
    for root in prog:
        ch = chordhead([k.deg(root + d, 52) for d in (0, 2, 4, 7)])
        for x, c_ in enumerate(strum):
            gtr.append({"A": f"{ch}/16@{86}^gate=1", "m": f"{ch}/16@{56}^gate=0.15", "s": f"{ch}/16@{70}^gate=0.2", "u": f"{ch}/16@{64}^gate=0.6", ".": "R/16"}[c_])
        b1, b5 = mname(k.deg(root, 33)), mname(k.deg(root + 4, 33))
        bass.append(f"{b1}/8.@86 {b1}/16@70 R/8 {b5}/8@78 {b1}/8.@84 {b5}/16@72 R/8 {b1}/8@76")
    out = [track("rhythm", pick_patch("nylon", "acoustic"), " ".join(gtr), pan=-0.25, gain="-2dB")]
    if kind == "intro":
        return out
    caj = pick_patch("cajon", "tight-kit")
    out += [track("cajon", caj, " ".join(({0: "cb/16@96", 8: "cb/16@90", 4: "cs/16@98", 12: "cs/16@100"}.get(x, "cg/16@40" if r.random() < 0.4 else "R/16")) for _ in range(4) for x in range(16))),
            track("palmas", caj, " ".join(("pa/16@72" if x % 4 == 2 else ("pa/16@50" if x % 4 == 3 and r.random() < 0.3 else "R/16")) for _ in range(4) for x in range(16)), pan=0.2),
            track("bass", pick_patch("finger-bass", "upright-bass"), " ".join(bass), seed=7)]
    return out


def gen_picado(r, k, prog, base, patch):
    """Flamenco picado: fast 16th scale runs (4–8 notes, up or down) landing on held chord tones, with
    breaths between — the nylon lead."""
    out = []
    for root in prog:
        toks, used = [], 0
        while used < 16:
            n = min(r.choice([4, 6, 8]), 16 - used)
            d = root + r.choice([0, 4, 7])
            step = r.choice([1, -1])
            for j in range(n - 1):
                toks.append(f"{mname(k.deg(d + step * j, base))}/16@{86 if j == 0 else 74}")
            land = mname(k.deg(root + r.choice([0, 2, 4]), base))
            toks.append(f"{land}/16@{92}")
            used += n
            if used < 16:
                hold = min(r.choice([2, 4]), 16 - used)
                toks += ["_"] * hold
                used += hold
        out.append(" ".join(toks))
    return [track("hook", patch, " ".join(out), pan=0.2)]


def gen_secondline(r, k, prog, kind="main"):
    """New Orleans second line (Rebirth / Dirty Dozen): the second-line snare (accented syncopated 16ths
    with buzz pairs), a marching bass drum with a cymbal on top, a syncopated tuba line, horn-section
    calls answered by trombone; kind=intro is the drums and tuba."""
    kit = rig("drums")
    sw = "swing16=0.62 "
    cell = r.choice(["x.xxx.x.x.xx.x.x", "x.x.xx.xx.x.xx.x", "xx.x.x.xx.x.x.xx"])
    snare = []
    for _ in range(4):
        for x, c_ in enumerate(cell):
            if c_ == "x":
                snare.append(f"s/32@{r.choice([60, 66])} s/32@{r.choice([70, 76])}" if r.random() < 0.15 else f"s/16@{92 if x % 4 == 0 else r.choice([58, 70, 80])}")
            else:
                snare.append("R/16")
    bd = " ".join(("k/16@96" if x in (0, 6, 12) else "R/16") for _ in range(4) for x in range(16))
    cymb = " ".join(("c/16@70" if x in (0, 6, 12) else "R/16") for _ in range(4) for x in range(16))
    tuba = []
    for bi, root in enumerate(prog):
        nxt = prog[(bi + 1) % len(prog)]
        b1, b5, b8, ap = (mname(k.deg(root, 28)), mname(k.deg(root + 4, 28)), mname(k.deg(root, 40)), mname(k.deg(nxt, 28) - 1))
        tuba.append(r.choice([f"{b1}/8.@90 {b5}/16@74 R/8 {b8}/8@80 {b5}/8@78 R/8 {b1}/8@82 {ap}/8@72",
                              f"{b1}/8@90 R/16 {b1}/16@72 {b5}/8@80 R/8 {b8}/8.@84 {b5}/16@70 {ap}/4@76"]))
    out = [track("snare", kit, sw + " ".join(snare)), track("bassdrum", kit, sw + bd), track("cymbal", kit, sw + cymb, gain="-8dB"),
           track("tuba", pick_patch("tuba", "finger-bass"), sw + " ".join(tuba), seed=7)]
    if kind == "intro":
        return out
    pt = penta(k)
    riff = [pt[i] for i in r.choice([[0, 2, 3, 4], [4, 3, 2, 0], [0, 0, 2, 3]])]
    calls, answers = [], []
    for bi, root in enumerate(prog):
        if bi % 2 == 0:
            calls.append(" ".join(f"{chordhead([k.deg(root + d, 57), k.deg(root + d, 69)])}/8@{96 if j == 0 else 86}" for j, d in enumerate(riff)) + " R/2")
            answers.append("R/1")
        else:
            calls.append("R/1")
            answers.append("R/2 " + " ".join(f"{mname(k.deg(root + d, 48))}/8@{84}" for d in reversed(riff)))
    out += [track("horns", pick_patch("horn-section", "brass"), sw + " ".join(calls), pan=0.15, gain="-4dB"),
            track("bone", pick_patch("trombone", "brass"), sw + " ".join(answers), pan=-0.2, gain="-3dB")]
    return out


def gen_exotica(r, k, prog, kind="main"):
    """Exotica (Martin Denny / Arthur Lyman): a gentle bolero/mambo on congas and bongos, rippling piano
    arpeggios, ukulele on the offbeats, string swells, jungle birdcalls; kind=full adds lap-steel glides;
    kind=intro is birds, piano and strings."""
    piano = []
    for root in prog:
        tones = [k.deg(root + d, 60) for d in (0, 2, 4, 6, 7, 9)]
        piano += [f"{mname(tones[i])}/16@{62 if j % 4 == 0 else 50}" for j, i in enumerate(r.choice([[0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3], [0, 2, 4, 5, 3, 1, 0, 2, 4, 5, 3, 1, 0, 2, 4, 5]]))]
    birds = " ".join((" ".join(f"{mname(k.deg(r.choice(penta(k)) + 7 * r.choice([1, 2]), 72))}/32@{r.choice([56, 66])}" for _ in range(3)) + " R/32 " * 5).strip() if r.random() < 0.15 else "R/4" for _ in range(16))
    out = [track("piano", "piano", " ".join(piano), pan=-0.2, gain="-6dB", fx=expand(["rack:piano-room"])),
           track("birds", pick_patch("birds", "celesta"), birds, pan=round(r.uniform(-0.6, 0.6), 2), gain="-4dB")]
    out += [dict(t, name="strings", gain="-12dB") for t in gen_pad(r, k, prog, 55, "strings", vel=60)]
    if kind == "intro":
        return out
    cg = pick_patch("congas", "djembe")
    bolero = r.choice(["o.mumu..bhbl.lo.", "o..bhbl.mu.o.lo.", "bh.bl.o.mumu.lo."])
    pat, i = [], 0
    while i < len(bolero):  # tokenize: '.', a two-letter piece (mu bh bl lo) or a one-letter piece (o)
        two = bolero[i:i + 2]
        tok = two if two in ("mu", "bh", "bl", "lo") else bolero[i]
        pat.append(tok); i += len(tok)
    toks = [("R/16" if pat[j % len(pat)] == "." else f"{pat[j % len(pat)]}/16@{r.choice([60, 68, 76])}") for j in range(16)]
    uke = " ".join(f"R/8 {chordhead([k.deg(root + d, 60) for d in (0, 2, 4, 7)])}/8@{70}" for root in prog for _ in range(4))
    out += [track("congas", cg, " ".join(toks * 4), pan=0.25, gain="-4dB"), track("ukulele", pick_patch("ukulele", "nylon"), uke, pan=0.3, gain="-3dB"),
            track("bass", pick_patch("upright-bass", "finger-bass"), " ".join(f"{mname(k.deg(root, 33))}/4@80 R/4 {mname(k.deg(root + 4, 33))}/4@72 R/4" for root in prog), seed=7)]
    if kind == "full":
        out.append(track("steel", pick_patch("pedal-steel", "ebow"), " ".join(f"{mname(k.deg(root + r.choice([2, 4, 7]), 67))}/1@{70}" for root in prog), gain="-6dB"))
    return out


SLOW_SOURCES = ["citypop", "neosoul", "chillwave", "lofihop", "bossa", "vaporwave", "souljazz", "balearic"]


def gen_slowed(r, k, prog, kind="main", src="lofihop", drop=3):
    """Slowed + reverb: a whole library part played as one sample, lowered `drop` semitones and
    time-stretched to exactly one 16-beat section at the song's tempo, through chorus, a soft low-pass
    and a long hall; a root–fifth pad in the lowered key and vinyl; kind=B adds a soft kick on 1 and 3;
    kind=intro is the sample, more muffled."""
    note = mname(60 - drop)
    patch = f"{pick_patch(f'slow-{src}', 'pad')} layers.0.speed={_TEMPO / 120:.3f}"
    t = {"name": "slowed", "patch": patch, "score": f"{note}/1 _ _ _"}
    if kind == "intro":
        t["fx"] = [{"type": "filter", "kind": "lp", "cutoff": 2500}]
    out = [t, track("vinyl", pick_patch("vinyl", "pad"), "C4/1 _ _ _", gain="-4dB"),
           track("pad", pick_patch("pad-glass", "pad"), f"{chordhead([48 - drop, 55 - drop])}/1 _ _ _", gain="-12dB")]
    if kind == "B":
        out.append(track("kick", pick_patch("lofi-kit", "tight-kit"), " ".join(("k/16@70" if x in (0, 8) else "R/16") for _ in range(4) for x in range(16)), gain="-8dB"))
    return out


def gen_downtempo(r, k, prog, kind="main"):
    """Downtempo (Bonobo / Emancipator / Tycho): a breakbeat (one of three patterns) whose low-pass opens
    over the section, an ostinato on marimba / kalimba / harp / nylon / celesta, a melodic syncopated bass
    (finger or fretless), a swelling string pad; kind=B adds an open hat, light congas, a second
    interlocking ostinato and sometimes pizzicato strings; kind=intro is ostinato, bass and pad."""
    kit = pick_patch("break-kit", "lofi-kit")
    opening = {"open": {"points": [["0b", 0.0], ["12b", 1.0], ["16b", 1.0]]}}
    lp = [{"type": "filter", "kind": "lp", "cutoff": {"value": 2200, "mod": [{"src": "auto.open", "amount": 1.6}]}}]
    kp, sp = r.choice([("x.........x.....", (4, 12)), ("x......x..x.....", (4, 12)), ("x.....x...x..x..", (4, 12))])
    busy = kind == "B"
    kick = " ".join(("k/16@96" if kp[x] == "x" else "R/16") for _ in range(4) for x in range(16))
    snare = " ".join(("s/16@90" if x in sp else (f"g/16@{r.choice([26, 32])}" if r.random() < (0.2 if busy else 0.1) else "R/16")) for _ in range(4) for x in range(16))
    hats = " ".join(("oh/16@54" if busy and x % 8 == 6 else (f"h/16@{60 if x % 4 == 0 else 44}" if x % 2 == 0 or (busy and r.random() < 0.3) else "R/16")) for _ in range(4) for x in range(16))
    out = [] if kind == "intro" else [track("kick", kit, kick, fx=lp, auto=opening), track("snare", kit, snare, fx=lp, auto=opening),
                                      track("hats", kit, hats, fx=lp, auto=opening, gain="-4dB", pan=0.1)]
    osts = r.sample(["marimba", "kalimba", "harp", "nylon", "celesta"], 2)
    out += [dict(t, name="ostinato") for t in gen_ostinato(r, k, prog, 60, pick_patch(osts[0], "marimba"), r.choice([[3, 3, 2], [3, 5]]))[:1]]
    if busy:
        out += [dict(t, name="ostinato2", pan=0.35, gain="-6dB") for t in gen_ostinato(r, k, prog, 72, pick_patch(osts[1], "kalimba"), r.choice([[3, 3, 3, 3, 4], [5, 5, 6]]))[:1]]
    bass = []
    for bi, root in enumerate(prog):
        nxt = prog[(bi + 1) % len(prog)]
        b1, b5, appr = mname(k.deg(root, 33)), mname(k.deg(root + 4, 33)), mname(k.deg(nxt, 33) + r.choice([-1, 1]))
        bass.append(r.choice([f"{b1}/4.@86 {b1}/8@72 R/4 {b5}/8@76 {appr}/8@68", f"{b1}/8@86 R/8 {b1}/8@70 {b5}/8@78 R/4 {b1}/8@80 {appr}/8@66",
                              f"{b1}/2@86 R/8 {b5}/8@74 R/8 {appr}/8@68"]))
    out.append(track("bass", pick_patch(r.choice(["finger-bass", "fretless"]), "bass-di"), " ".join(bass), seed=7))
    if kind != "intro" or r.random() < 0.5:
        peak = r.choice([6, 10, 14])
        sw = {"sw": {"points": [["0b", 0.2], [f"{peak}b", 1.0], ["16b", 0.4]]}}
        out += [dict(t, auto=sw, gain={"value": "-14dB", "mod": [{"src": "auto.sw", "amount": 5}]}) for t in gen_pad(r, k, prog, 48, "strings", vel=64)]
    if busy and r.random() < 0.5:
        pizz = " ".join(f"{mname(k.deg(root + d, 55))}/8@{r.choice([60, 68])}^gate=0.25" if j % 2 == 0 else "R/8" for root in prog for j, d in enumerate([0, 2, 4, 2, 4, 7, 4, 2]))
        out.append(track("pizz", pick_patch("strings", "harp"), pizz, pan=-0.3, gain="-8dB"))
    return out


# Guest sections: other styles' generators composed in the song's key, slotted into its form.
GUESTS = {
    "brokenjazz": (None, {"ukjazz"}),
    "swingmetal": (lambda r, k, prog, low, gp: gen_swingmetal(r, k, prog, low), {"djazz"}),
    "coltrane": (lambda r, k, prog, low, gp: gen_coltrane(r, k, prog, low), set()),
    "jazz": (lambda r, k, prog, low, gp: gen_mathcore(r, k, prog, low, "jazz"), {"djazz", "mathcore"}),
    "breakcore": (lambda r, k, prog, low, gp: gen_breakcore(r, k, prog, low), {"breakcore"}),
    "blast": (lambda r, k, prog, low, gp: gen_blast(r, k, prog, low, r.choice(["trad", "hammer", "bomb"])), {"tech-death", "deathcore"}),
    "tribal": (lambda r, k, prog, low, gp: gen_gojira(r, k, prog, low, "tribal"), {"gojira"}),
    "whammy": (lambda r, k, prog, low, gp: gen_gojira(r, k, prog, low, "whammy"), {"gojira"}),
    "taiko": (lambda r, k, prog, low, gp: gen_koto(r, k, prog, "arp") + gen_koto(r, k, prog, "taiko"), {"koto"}),
    "kotekan": (lambda r, k, prog, low, gp: gen_meshuggah(r, k, low, gp, r.choice([14, 22])) + gen_kotekan(r, k, prog), {"gamelan"}),
    "tabla": (lambda r, k, prog, low, gp: gen_raga(r, k, prog, "groove"), {"raga"}),
    "space": (lambda r, k, prog, low, gp: gen_space(r, k, low, gp, r.choice([11, 13, 9])), {"meshuggah"}),
    "beatdown": (lambda r, k, prog, low, gp: gen_hc(r, k, prog, low, "beatdown"), {"hardcore-kl"}),
    "dnb": (lambda r, k, prog, low, gp: gen_dnb(r, k, prog, "metal"), {"dnb"}),
    "brostep": (lambda r, k, prog, low, gp: gen_bro_drop(r, k, prog, metal=True), {"brostep"}),
    "gallop": (lambda r, k, prog, low, gp: gen_power(r, k, prog, 40, "verse"), {"power", "thrash"}),
    "chaos": (lambda r, k, prog, low, gp: gen_mathcore(r, k, prog, low), {"mathcore"}),
}


CHILL_GUESTS = {
    "ballad": (lambda r, k, prog: gen_ballad(r, k, prog), {"ballad"}),
    "bossa": (lambda r, k, prog: gen_bossa(r, k, prog), {"bossa"}),
    "doomjazz": (lambda r, k, prog: gen_doomjazz(r, k, prog, "full") + gen_atmos(r, k, prog, 55, pick_patch("tenor-sax", "clarinet")), {"doomjazz"}),
    "mali": (lambda r, k, prog: gen_mali(r, k, prog), {"mali"}),
    "vaporwave": (lambda r, k, prog: gen_vaporwave(r, k, prog), {"vaporwave"}),
    "backrooms": (lambda r, k, prog: gen_backrooms(r, k, prog, "far"), {"backrooms"}),
    "neosoul": (lambda r, k, prog: gen_neosoul(r, k, prog), {"neosoul"}),
    "minimal": (lambda r, k, prog: gen_minimal(r, k, prog, "phase"), {"minimal"}),
    "cyberscape": (lambda r, k, prog: gen_cyberscape(r, k, prog), {"cyberscape"}),
    "slowcore": (lambda r, k, prog: gen_slowcore(r, k, prog) + gen_atmos(r, k, prog, 64, pick_patch("pedal-steel", "ebow")), {"slowcore"}),
    "guofeng": (lambda r, k, prog: gen_guofeng(r, k, prog) + gen_penta_air(r, k, prog, 67, pick_patch("dizi", "flute")), {"guofeng"}),
    "celtic": (lambda r, k, prog: gen_celtic(r, k, prog, "drums") + gen_air(r, k, prog, 72, pick_patch("low-whistle", "flute")), {"celtic"}),
    "manouche": (lambda r, k, prog: gen_manouche(r, k, prog) + gen_swing_run(r, k, prog, 64, pick_patch("accordion", "clarinet")), {"manouche"}),
    "neo": (lambda r, k, prog: gen_neoclassical(r, k, prog), {"neoclassical", "chamber"}),
    "ambient": (lambda r, k, prog: gen_ambient(r, k, prog, "A"), {"ambient"}),
    "lofi": (lambda r, k, prog: gen_lofi(r, k, prog), {"lofihop"}),
    "cycles": (lambda r, k, prog: gen_cycles(r, k, prog), {"house-melodic"}),
    "triphop": (lambda r, k, prog: gen_triphop(r, k, prog), {"triphop"}),
}


CHILL_GUESTS["dub"] = (lambda r, k, prog: gen_dub(r, k, prog), {"dub"})
CHILL_GUESTS["berlin"] = (lambda r, k, prog: gen_berlin(r, k, prog, "full"), {"berlin"})
CHILL_GUESTS["kankyo"] = (lambda r, k, prog: gen_kankyo(r, k, prog, "water"), {"kankyo"})
CHILL_GUESTS["handpan"] = (lambda r, k, prog: gen_handpan(r, k, prog), {"handpan"})
CHILL_GUESTS["lid"] = (lambda r, k, prog: gen_lid(r, k, prog, "B"), {"lid"})
RHYTHM_SRC = {
    "dub": lambda r, k, prog: gen_dub(r, k, prog), "triphop": lambda r, k, prog: gen_triphop(r, k, prog),
    "lofi": lambda r, k, prog: gen_lofi(r, k, prog), "bossa": lambda r, k, prog: gen_bossa(r, k, prog),
    "neosoul": lambda r, k, prog: gen_neosoul(r, k, prog), "mali": lambda r, k, prog: gen_mali(r, k, prog),
    "citypop": lambda r, k, prog: gen_citypop(r, k, prog), "balearic": lambda r, k, prog: gen_balearic(r, k, prog),
    "chillwave": lambda r, k, prog: gen_chillwave(r, k, prog), "souljazz": lambda r, k, prog: gen_souljazz(r, k, prog),
    "ethiojazz": lambda r, k, prog: gen_ethiojazz(r, k, prog), "hauntology": lambda r, k, prog: gen_hauntology(r, k, prog),
    "amapiano": lambda r, k, prog: gen_amapiano(r, k, prog), "liquid": lambda r, k, prog: gen_liquid(r, k, prog),
    "nujazz": lambda r, k, prog: gen_nujazz(r, k, prog), "highlife": lambda r, k, prog: gen_highlife(r, k, prog),
    "samba": lambda r, k, prog: gen_samba(r, k, prog), "rumba": lambda r, k, prog: gen_rumba(r, k, prog),
    "exotica": lambda r, k, prog: gen_exotica(r, k, prog),
    "celtic": lambda r, k, prog: gen_celtic(r, k, prog, "drums"), "cycles": lambda r, k, prog: gen_cycles(r, k, prog),
    "ballad": lambda r, k, prog: gen_ballad(r, k, prog), "slowcore": lambda r, k, prog: gen_slowcore(r, k, prog),
    "vaporwave": lambda r, k, prog: gen_vaporwave(r, k, prog), "cyberscape": lambda r, k, prog: gen_cyberscape(r, k, prog, "full"),
    "doomjazz": lambda r, k, prog: gen_doomjazz(r, k, prog),
}


def is_rhythm(t):
    p, n = t.get("patch", ""), t.get("name", "")
    return "kit" in p or p in ("djembe", "bodhran") or n in ("bass", "pulsebass", "sub", "pulse") or n.startswith("bass")


def fusion_pair(seed):
    r = random.Random(seed * 3 + 11)
    src = r.choice(sorted(CHILL_GUESTS))
    beat = r.choice([b for b in sorted(RHYTHM_SRC) if b != src and not (src == "lofi" and b == "lofi")])
    return src, beat


def gen_fusion(r, k, prog, src, beat, with_beat=True):
    tonal = [t for t in CHILL_GUESTS[src][0](r, k, prog) if not is_rhythm(t)]
    out = list(tonal)
    if with_beat:
        names = {t["name"] for t in out}
        for t in RHYTHM_SRC[beat](r, k, prog):
            if is_rhythm(t):
                t = dict(t, gain=f"{float(str(t.get('gain', '0dB')).replace('dB', '')) - 3:g}dB")
                out.append(dict(t, name=t["name"] + "-x") if t["name"] in names else t)
    return out


# Odd-meter guest sections from the engine's built-in parts (in F minor; length in beats, repeats).
ODD_PARTS = {"54": (10, 2, "beat-54", "beat-54-ghost"), "68": (6, 3, "beat-68", "beat-68-trap"), "74": (14, 1, "beat-74", "beat-74"),
             "78": (7, 2, "beat-78", "beat-78"), "118": (11, 2, "beat-118", "beat-118-ghost")}
ODD_HOSTS_HEAVY = {"tigran", "cynic", "mathcore", "djazz", "tool", "djent", "meshuggah", "metalcore", "postmetal", "gojira", "tech-death", "postrock", "blackgaze", "groovemetal"}
ODD_HOSTS_CHILL = {"ukjazz", "gogo", "neosoul", "fusion", "souljazz", "ethiojazz", "citypop", "nujazz"}


def odd_section(style, slot, p):
    """Write gen-SLOT-riffOdd: an engine odd-meter riff (+ its beat) transposed into the song's key."""
    import zlib
    r = random.Random(zlib.crc32(f"odd{p['seed']}".encode()))
    meter = r.choice(sorted(ODD_PARTS))
    beats, reps, beat_h, beat_c = ODD_PARTS[meter]
    clean = style in ODD_HOSTS_CHILL
    riff = f"riff-{meter}" + ("-clean" if clean else "")
    beat = beat_c if clean else beat_h
    t = (p["pc"] - 5) % 12
    t = t - 12 if t > 6 else t
    n = f"gen-{slot}-riffOdd"
    total = beats * reps
    LENGTHS[n] = total
    tracks = [{"name": "odd", "score": f"tr={t} " + " ".join(f"@{riff}" for _ in range(reps))},
              {"name": "oddbeat", "score": " ".join(f"@{beat}" for _ in range(reps))}]
    lines = [f"about: {json.dumps(f'Generated part (tempo: inherit, {total:g} beats) — odd-meter guest ({meter[0]}/{meter[1:]} {riff} + {beat}) for {style}')}",
             "tempo: inherit", f"length: {total:g}b", "tracks:"] + ["  - " + json.dumps(tr_) for tr_ in tracks]
    open(f"{SONGS}/{n}.yaml", "w").write("\n".join(lines) + "\n")
    return n, f"{meter[0]}/{meter[1:]}"


def compose(style, slot, p):
    """Compose the style's parts, plus two guest sections from other styles (riffGuest1/2, same key)."""
    global _KEY, _CHAPTER, _TEMPO
    _TEMPO = p.get("tempo", 100)
    if style in ("beattape", "lofihouse"):  # the chopped samples are in C: these styles live in their key
        p = dict(p, pc=0)
    _KEY = (p["pc"], p["mode"])
    _CHAPTER = p.get("chapter", 0)
    names, desc = _compose_style(style, slot, p)
    if style in ODD_HOSTS_HEAVY | ODD_HOSTS_CHILL:
        n, meter = odd_section(style, slot, p)
        names["riffOdd"] = n
        desc += f", odd {meter}"
    if style in CHILL_STYLES:
        r = random.Random(p["seed"] + 1)
        k = Key(p["pc"], p["mode"])
        pool = [g for g, (_, homes) in CHILL_GUESTS.items() if style not in homes]
        if style in ("chamber", "neoclassical", "ambient"):  # drumless pieces borrow only drumless guests
            pool = [g for g in pool if g in ("neo", "ambient")] or ["neo"]
        picks = r.sample(pool, min(2, len(pool))) + (["neo"] if len(pool) < 2 else [])
        for i, g in enumerate(picks, 1):
            n = f"gen-{slot}-riffGuest{i}"
            write(n, f"chill guest section ({g}) for {style}", CHILL_GUESTS[g][0](r, k, p["prog"]))
            names[f"riffGuest{i}"] = n
        desc += f", guests {'/'.join(picks)}"
    if style in HEAVY_STYLES:
        r = random.Random(p["seed"] + 1)  # separate stream: the style's own parts stay as they were
        k = Key(p["pc"], p["mode"])
        gp = rig("rhythm")[0]
        pool = [g for g, (_, homes) in GUESTS.items() if style not in homes]
        picks = r.sample(pool, 2)
        if FUSION:  # fusion-metal journey: one guest from the jazz / polymetric set
            pref = [g for g in ("jazz", "space", "tribal", "tabla", "kotekan", "brokenjazz", "brokenjazz", "swingmetal", "swingmetal", "coltrane", "coltrane") if g in pool]
            if pref:
                first = r.choice(pref)
                picks = [first, r.choice([g for g in pool if g != first])]
        for i, g in enumerate(picks, 1):
            n = f"gen-{slot}-riffGuest{i}"
            if g == "brokenjazz":  # odd-meter section: its own length
                meter = r.choice([7, 7, 10])
                beats = meter * 2 * (4 if meter in (7, 9) else 3) / 4
                bp = pick_patch("tuba", "upright-bass") if r.random() < 0.5 else pick_patch("upright-bass", "finger-bass")
                write(n, f"guest section (broken jazz in {meter}/8) for {style}", gen_broken(r, k, p["prog"], meter, "horns", bp), beats)
            else:
                write(n, f"guest section ({g}) for {style}", GUESTS[g][0](r, k, p["prog"], 28, gp))
            names[f"riffGuest{i}"] = n
        desc += f", guests {'/'.join(picks)}"
        if FUSION and "riff" in names and abs(LENGTHS.get(names["riff"], 16) - 16) < 1e-9:
            # Fusion solo trading over the song's own main riff: guitar two bars, synth two bars.
            gl = rig("lead")
            sl = pick_patch(r.choice(["moog-seq", "synth-lead", "lead-monster"]), "synth-lead")
            g1 = gen_thordendal(r, k, 28, gl, 8)[0]
            g2 = gen_thordendal(r, k, 28, sl, 8)[0]
            trade = [{"name": "band", "score": f"@{names['riff']}"},
                     dict(g1, name="solo-gtr", score=g1["score"] + " R/1 R/1"),
                     dict(g2, name="solo-syn", score="R/1 R/1 " + g2["score"], pan=-0.15)]
            nt = f"gen-{slot}-riffTrade"
            write(nt, f"fusion trading solos over the main riff for {style}", trade)
            names["riffTrade"] = nt
            # Trading fours with the drums: the band two bars (the main riff cut at 8 beats), the drummer two.
            ds = gen_drumsolo(r, 8)[0]
            fours = [{"name": "band", "score": f"@{names['riff']}^cut=8"}, dict(ds, score="R/1 R/1 " + ds["score"])]
            nf = f"gen-{slot}-riffFours"
            write(nf, f"trading fours: band and drum breaks for {style}", fours)
            names["riffFours"] = nf
        n = f"gen-{slot}-riffEnd"
        write(n, f"ending for {style}", gen_ending(r, k, p["prog"]))
        names["riffEnd"] = n
        for tag in ("A", "B"):  # two 4-beat fills leading into big sections
            n = f"gen-{slot}-fill{tag}"
            write(n, f"4-beat fill for {style}", gen_fill(r, k), 4)
            names[f"fill{tag}"] = n
    return names, desc


CHILL_STYLES = {"lofihop", "gogo", "ukjazz", "ambient", "downtempo", "smile", "house-melodic", "chamber", "triphop", "neoclassical", "ballad", "bossa", "dub", "manouche", "celtic", "doomjazz", "mali", "guofeng", "vaporwave", "slowcore", "backrooms", "cyberscape", "neosoul", "minimal", "fusion", "berlin", "satie", "kankyo", "dawnraga", "handpan", "citypop", "lid", "tiersen", "balearic", "chillwave", "souljazz", "ethiojazz", "hauntology", "dawnchorus", "beattape", "lofihouse", "amapiano", "liquid", "nujazz", "highlife", "samba", "rumba", "secondline", "exotica", "slowed"}
HEAVY_STYLES = {"meshuggah", "djent", "djent-breakdown", "doom-ambient", "tech-death", "thrash", "tool", "hardcore-kl", "brostep",
                "blackgaze", "darksynth", "numetal", "industrial", "dnb", "deathcore", "postrock", "groovemetal", "power", "sludge",
                "breakcore", "mathcore", "gojira", "djazz", "raga", "gamelan", "koto"}


def _compose_style(style, slot, p):
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
    if style == "slowed":
        src = r.choice(SLOW_SOURCES)
        drop = r.choice([2, 3, 4, 5])
        parts = {"riffI": gen_slowed(r, k, prog, "intro", src, drop), "riff": gen_slowed(r, k, prog, "main", src, drop), "riffB": gen_slowed(r, k, prog, "B", src, drop)}
        return _write_parts(slot, "slowed", parts, f"{src} slowed {drop} semitones")
    if style == "exotica":
        parts = {"riffI": gen_exotica(r, k, prog, "intro"), "riff": gen_exotica(r, k, prog), "riffB": gen_exotica(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 67, pick_patch("vibes", "marimba"))}
        return _write_parts(slot, "exotica", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "secondline":
        lead = pick_patch(r.choice(["trombone", "tenor-sax", "horn-section"]), "brass")
        parts = {"riffI": gen_secondline(r, k, prog, "intro"), "riff": gen_secondline(r, k, prog), "riffB": gen_secondline(r, k, prog),
                 "hook": [dict(t, score="swing16=0.62 " + t["score"]) for t in gen_hook(r, k, prog, 60 if lead == "trombone" else 64, lead)]}
        return _write_parts(slot, "secondline", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "rumba":
        parts = {"riffI": gen_rumba(r, k, prog, "intro"), "riff": gen_rumba(r, k, prog), "riffB": gen_rumba(r, k, prog),
                 "hook": gen_picado(r, k, prog, 64, pick_patch("nylon", "acoustic"))}
        return _write_parts(slot, "rumba", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "samba":
        lead = pick_patch(r.choice(["flute", "trumpet-mute", "tenor-sax"]), "flute")
        parts = {"riffI": gen_samba(r, k, prog, "intro"), "riff": gen_samba(r, k, prog), "riffB": gen_samba(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 72 if lead == "flute" else 64, lead)}
        return _write_parts(slot, "samba", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "highlife":
        lead = pick_patch(r.choice(["flute", "horn-section", "tenor-sax"]), "flute")
        parts = {"riffI": gen_highlife(r, k, prog, "intro"), "riff": gen_highlife(r, k, prog), "riffB": gen_highlife(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 67 if lead != "flute" else 72, lead)}
        return _write_parts(slot, "highlife", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "nujazz":
        lead = pick_patch(r.choice(["trumpet-mute", "trumpet-mute", "tenor-sax", "flute"]), "flute")
        parts = {"riffI": gen_nujazz(r, k, prog, "intro"), "riff": gen_nujazz(r, k, prog), "riffB": gen_nujazz(r, k, prog, "full"),
                 "hook": [dict(t, score="swing16=0.6 " + t["score"]) for t in gen_hook(r, k, prog, 64 if lead != "flute" else 72, lead)]}
        return _write_parts(slot, "nujazz", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "liquid":
        lead = pick_patch(r.choice(["flute", "dream-vox", "dx-epiano"]), "flute")
        parts = {"riffI": gen_liquid(r, k, prog, "intro"), "riff": gen_liquid(r, k, prog), "riffB": gen_liquid(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 72 if lead != "dream-vox" else 67, lead)}
        return _write_parts(slot, "liquid", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "amapiano":
        lead = pick_patch(r.choice(["flute", "tenor-sax", "low-whistle"]), "flute")
        parts = {"riffI": gen_amapiano(r, k, prog, "intro"), "riff": gen_amapiano(r, k, prog), "riffB": gen_amapiano(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 67 if lead == "tenor-sax" else 72, lead)}
        return _write_parts(slot, "amapiano", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "lofihouse":
        src, src2 = r.sample(CHOP_SOURCES, 2)
        parts = {"riffI": gen_lofihouse(r, k, prog, "intro", src), "riff": gen_lofihouse(r, k, prog, "main", src), "riffB": gen_lofihouse(r, k, prog, "full", src, src2)}
        return _write_parts(slot, "lofihouse", parts, f"C (sample key), chops of {src} + {src2}")
    if style == "beattape":
        src, src2 = r.sample(CHOP_SOURCES, 2)
        parts = {"riffI": gen_beattape(r, k, prog, "intro", src), "riff": gen_beattape(r, k, prog, "main", src), "riffB": gen_beattape(r, k, prog, "full", src, src2)}
        return _write_parts(slot, "beattape", parts, f"C (sample key), chops of {src} + {src2}")
    if style == "dawnchorus":
        parts = {"riffI": gen_dawnchorus(r, k, prog, "intro"), "riff": gen_dawnchorus(r, k, prog), "riffB": gen_dawnchorus(r, k, prog, "full"),
                 "hook": gen_penta_air(r, k, prog, 67, pick_patch(r.choice(["low-whistle", "flute", "shakuhachi"]), "flute"))}
        return _write_parts(slot, "dawnchorus", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "hauntology":
        lead = pick_patch(r.choice(["boc-lead", "boc-lead", "music-box", "mellotron-flute"]), "synth-lead")
        parts = {"riffI": gen_hauntology(r, k, prog, "intro"), "riff": gen_hauntology(r, k, prog), "riffB": gen_hauntology(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 67 if lead == "boc-lead" else 74, lead)}
        return _write_parts(slot, "hauntology", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "ethiojazz":
        lead = pick_patch(r.choice(["vibes", "vibes", "tenor-sax"]), "vibes")
        parts = {"riffI": gen_ethiojazz(r, k, prog, "intro"), "riff": gen_ethiojazz(r, k, prog), "riffB": gen_ethiojazz(r, k, prog, "full"),
                 "hook": gen_penta_air(r, k, prog, 67, lead) if r.random() < 0.4 else gen_hook(r, k, prog, 67, lead)}
        return _write_parts(slot, "ethiojazz", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "souljazz":
        lead = pick_patch(r.choice(["hammond-b3", "jazz-box"]), "organ")
        parts = {"riffI": gen_souljazz(r, k, prog, "intro"), "riff": gen_souljazz(r, k, prog), "riffB": gen_souljazz(r, k, prog, "full"),
                 "hook": [dict(t, score="swing=0.66 " + t["score"]) for t in gen_hook(r, k, prog, 67, lead)]}
        return _write_parts(slot, "souljazz", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "chillwave":
        lead = pick_patch(r.choice(["dream-vox", "synth-lead", "dx-epiano"]), "rhodes")
        parts = {"riffI": gen_chillwave(r, k, prog, "intro"), "riff": gen_chillwave(r, k, prog), "riffB": gen_chillwave(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 69 if lead != "dx-epiano" else 74, lead)}
        return _write_parts(slot, "chillwave", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "balearic":
        lead = pick_patch(r.choice(["flute", "tenor-sax", "nylon"]), "flute")
        parts = {"riffI": gen_balearic(r, k, prog, "intro"), "riff": gen_balearic(r, k, prog), "riffB": gen_balearic(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 64 if lead != "flute" else 72, lead)}
        return _write_parts(slot, "balearic", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "tiersen":
        lead = pick_patch(r.choice(["toy-piano", "glock", "accordion", "mandolin"]), "celesta")
        parts = {"riffI": gen_tiersen(r, k, prog, "intro", lead), "riff": gen_tiersen(r, k, prog, "main", lead), "riffB": gen_tiersen(r, k, prog, "full", lead)}
        return _write_parts(slot, "tiersen", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}", {"riffI": 24, "riff": 24, "riffB": 24})
    if style == "lid":
        parts = {"riffI": gen_lid(r, k, prog, "intro"), "riff": gen_lid(r, k, prog, "A"), "riffB": gen_lid(r, k, prog, "B"), "riffL": gen_lid(r, k, prog, "low")}
        return _write_parts(slot, "lid", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "citypop":
        lead = pick_patch(r.choice(["tenor-sax", "synth-lead", "dx-epiano"]), "rhodes")
        parts = {"riffI": gen_citypop(r, k, prog, "intro"), "riff": gen_citypop(r, k, prog), "riffB": gen_citypop(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 67 if "sax" in lead else 72, lead)}
        return _write_parts(slot, "citypop", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "handpan":
        parts = {"riffI": gen_handpan(r, k, prog, "intro"), "riff": gen_handpan(r, k, prog), "riffB": gen_handpan(r, k, prog, "full"),
                 "hook": gen_penta_air(r, k, prog, 67, pick_patch(r.choice(["low-whistle", "shakuhachi"]), "flute"))}
        return _write_parts(slot, "handpan", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "dawnraga":
        parts = {"riffA": gen_dawnraga(r, k, prog, "alap"), "riffJ": gen_dawnraga(r, k, prog, "jor"), "riffG": gen_dawnraga(r, k, prog, "gat"),
                 "hook": gen_hook(r, k, prog, 62, pick_patch("sitar", "nylon")), "hookE": gen_atmos(r, k, prog, 60, pick_patch(r.choice(["shakuhachi", "flute", "harmonium"]), "flute"))}
        return _write_parts(slot, "dawnraga", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "kankyo":
        parts = {"riffI": gen_kankyo(r, k, prog, "intro"), "riff": gen_kankyo(r, k, prog), "riffW": gen_kankyo(r, k, prog, "water"),
                 "hook": gen_penta_air(r, k, prog, 67, pick_patch("shakuhachi", "flute"))}
        return _write_parts(slot, "kankyo", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "satie":
        parts = {"riffP": gen_satie(r, k, prog, "piano"), "riff": gen_satie(r, k, prog), "riffB": gen_satie(r, k, prog, "full")}
        return _write_parts(slot, "satie", parts, f"{NAMES[p['pc']]} {p['mode']}", {"riffP": 24, "riff": 24, "riffB": 24})
    if style == "berlin":
        parts = {"riffI": [t for t in gen_berlin(r, k, prog) if t["name"] == "choir"], "riff": gen_berlin(r, k, prog), "riffB": gen_berlin(r, k, prog, "full"),
                 "riffD": gen_berlin(r, k, prog, "drive"),
                 "hook": gen_atmos(r, k, prog, 67, pick_patch(r.choice(["theremin", "synth-lead", "mellotron-flute"]), "synth-lead"))}
        return _write_parts(slot, "berlin", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "fusion":
        src, beat = fusion_pair(p["seed"])
        lead = pick_patch(r.choice(["tenor-sax", "flute", "erhu", "kora", "music-box", "theremin", "trumpet-mute", "vibes"]), "rhodes")
        parts = {"riffI": gen_fusion(r, k, prog, src, beat, with_beat=False), "riff": gen_fusion(r, k, prog, src, beat),
                 "riffB": gen_fusion(r, k, prog, src, beat) + [dict(t, name="pad-f") for t in gen_pad(r, k, prog, 55, pick_patch("pad-glass", "strings"), gain="-10dB", vel=58)],
                 "hook": gen_hook(r, k, prog, 64 if lead in ("tenor-sax", "trumpet-mute") else 69, lead)}
        return _write_parts(slot, "fusion", parts, f"{NAMES[p['pc']]} {p['mode']}, {src} over {beat}, lead {lead}")
    if style == "minimal":
        parts = {"riffP": gen_minimal(r, k, prog, "phase"), "riffA": gen_minimal(r, k, prog, "additive"), "riff": gen_minimal(r, k, prog, "pulse"),
                 "riffF": gen_minimal(r, k, prog, "full"), "hook": gen_atmos(r, k, prog, 60, pick_patch(r.choice(["clarinet", "cellos", "flute"]), "strings"))}
        return _write_parts(slot, "minimal", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "neosoul":
        lead = pick_patch(r.choice(["tenor-sax", "trumpet-mute", "synth-lead"]), "rhodes")
        parts = {"riffI": gen_neosoul(r, k, prog, "intro"), "riff": gen_neosoul(r, k, prog), "riffB": gen_neosoul(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 64 if "synth" not in lead else 69, lead)}
        return _write_parts(slot, "neosoul", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "backrooms":
        parts = {"riffI": gen_backrooms(r, k, prog, "intro"), "riff": gen_backrooms(r, k, prog), "riffF": gen_backrooms(r, k, prog, "far"),
                 "riffD": gen_backrooms(r, k, prog, "decay")}
        return _write_parts(slot, "backrooms", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "cyberscape":
        parts = {"riffI": gen_cyberscape(r, k, prog, "intro"), "riff": gen_cyberscape(r, k, prog), "riffB": gen_cyberscape(r, k, prog, "full"),
                 "hook": [dict(t, fx=[{"type": "delay", "time": "3/8", "feedback": 0.4, "ping_pong": True, "mix": 0.3}]) for t in gen_atmos(r, k, prog, 67, pick_patch(r.choice(["theremin", "pad-glass", "ebow"]), "synth-lead"))]}
        return _write_parts(slot, "cyberscape", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "slowcore":
        steel = pick_patch("pedal-steel", "ebow")
        parts = {"riffI": gen_slowcore(r, k, prog, "intro"), "riff": gen_slowcore(r, k, prog), "riffB": gen_slowcore(r, k, prog, "full"),
                 "hookE": gen_atmos(r, k, prog, 64, steel), "hook": gen_atmos(r, k, prog, 69, steel)}
        return _write_parts(slot, "slowcore", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "vaporwave":
        lead = pick_patch(r.choice(["tenor-sax", "dx-epiano"]), "rhodes")
        parts = {"riffI": gen_vaporwave(r, k, prog, "intro"), "riff": gen_vaporwave(r, k, prog), "riffB": gen_vaporwave(r, k, prog, "full"),
                 "hook": [dict(t, fx=TAPE_WOW) for t in gen_hook(r, k, prog, 67 if "sax" in lead else 74, lead)]}
        return _write_parts(slot, "vaporwave", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "guofeng":
        lead = pick_patch(r.choice(["erhu", "dizi"]), "flute")
        parts = {"riffI": gen_guofeng(r, k, prog, "intro"), "riff": gen_guofeng(r, k, prog), "riffB": gen_guofeng(r, k, prog, "full"),
                 "hook": gen_penta_air(r, k, prog, 67, lead), "hookE": gen_penta_air(r, k, prog, 62, pick_patch("erhu", "strings"))}
        return _write_parts(slot, "guofeng", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "mali":
        parts = {"riffI": gen_mali(r, k, prog, "intro"), "riff": gen_mali(r, k, prog), "riffB": gen_mali(r, k, prog, "riff"),
                 "hook": gen_hook(r, k, prog, 67, pick_patch("kora", "harp"))}
        return _write_parts(slot, "mali", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "doomjazz":
        sax = pick_patch("tenor-sax", "clarinet")
        parts = {"riffI": gen_doomjazz(r, k, prog, "intro"), "riff": gen_doomjazz(r, k, prog), "riffB": gen_doomjazz(r, k, prog, "full"),
                 "hookE": gen_atmos(r, k, prog, 55, sax), "hook": gen_atmos(r, k, prog, 60, pick_patch(r.choice(["tenor-sax", "trumpet-mute"]), "clarinet"))}
        return _write_parts(slot, "doomjazz", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "celtic":
        lead = pick_patch("low-whistle", "flute")
        parts = {"riffI": gen_celtic(r, k, prog, "intro"), "riff": gen_celtic(r, k, prog), "riffB": gen_celtic(r, k, prog, "drums"),
                 "hook": gen_air(r, k, prog, 72, lead), "hookB": gen_air(r, k, prog, 72, lead)}
        return _write_parts(slot, "celtic", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "manouche":
        lead = pick_patch(r.choice(["violins", "clarinet", "accordion"]), "violins")
        parts = {"riffG": gen_manouche(r, k, prog, "guitar"), "riff": gen_manouche(r, k, prog), "riffB": gen_manouche(r, k, prog),
                 "hook": [dict(t, score="swing=0.64 " + t["score"]) for t in gen_hook(r, k, prog, 64, lead)],
                 "solo": gen_swing_run(r, k, prog, 64, lead)}
        return _write_parts(slot, "manouche", parts, f"{NAMES[p['pc']]} {p['mode']}, lead {lead}")
    if style == "dub":
        parts = {"riffI": gen_dub(r, k, prog, "intro"), "riff": gen_dub(r, k, prog), "riffD": gen_dub(r, k, prog, "dub"),
                 "hook": gen_hook(r, k, prog, 64, pick_patch("melodica", "flute"))}
        return _write_parts(slot, "dub", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "bossa":
        parts = {"riffG": gen_bossa(r, k, prog, "guitar"), "riff": gen_bossa(r, k, prog), "riffB": gen_bossa(r, k, prog),
                 "hook": gen_hook(r, k, prog, 64, pick_patch(r.choice(["flute", "trumpet-mute", "trumpet-mute"]), "flute")),
                 "pad": gen_pad(r, k, prog, 52, "strings", gain="-12dB", vel=58)}
        return _write_parts(slot, "bossa", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "triphop":
        parts = {"riffI": gen_triphop(r, k, prog, "intro"), "riff": gen_triphop(r, k, prog), "riffB": gen_triphop(r, k, prog, "full"),
                 "hook": gen_hook(r, k, prog, 62, pick_patch(r.choice(["ebow", "flute", "rhodes"]), "rhodes"))}
        return _write_parts(slot, "triphop", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "neoclassical":
        parts = {"riffP": gen_neoclassical(r, k, prog, "piano"), "riff": gen_neoclassical(r, k, prog), "riffB": gen_neoclassical(r, k, prog, "full"),
                 "hookE": [dict(t, gain="-4dB") for t in gen_atmos(r, k, prog, 67 if r.random() < 0.5 else 60, pick_patch(r.choice(["violins", "horn"]), "strings"))]}
        return _write_parts(slot, "neoclassical", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "ballad":
        parts = {"riff": gen_ballad(r, k, prog), "riffB": gen_ballad(r, k, prog),
                 "hook": gen_hook(r, k, prog, 60, pick_patch(r.choice(["clarinet", "flute", "vibes", "piano", "trumpet-mute", "tenor-sax", "tenor-sax"]), "vibes"))}
        return _write_parts(slot, "ballad", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "smile":
        parts = {"riffQ": gen_smile(r, k, prog, "quiet"), "riff": gen_smile(r, k, prog), "riffF": gen_smile(r, k, prog, "full"), "riffK": gen_smile(r, k, prog, "kida"),
                 "riff5": gen_tool(r, k, 40, 10, r.choice([[3, 3, 2, 2], [3, 3, 4]]), "clean", reps=3) + gen_trio_drums(r, "sparse")[:0],
                 "hookE": [dict(t, gain="-6dB") for t in gen_atmos(r, k, prog, 64, pick_patch(r.choice(["ebow", "theremin"]), "synth-lead"))]}
        lens = {"riff5": 10 * 3 / 2}
        return _write_parts(slot, "smile", parts, f"{NAMES[p['pc']]} {p['mode']}", lens)
    if style == "house-melodic":
        parts = {"riffI": gen_cycles(r, k, prog, "intro"), "riff": gen_cycles(r, k, prog), "riffB": gen_cycles(r, k, prog),
                 "hook": gen_hook(r, k, prog, 64, pick_patch("pluck-lead", "rhodes"))}
        return _write_parts(slot, "house-melodic", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "chamber":
        parts = {"riffN": gen_classical(r, k, prog, "nocturne"), "riffQ": gen_classical(r, k, prog, "quartet"),
                 "riffM": gen_classical(r, k, prog, "minimal"), "riffN2": gen_classical(r, k, prog, "nocturne")}
        return _write_parts(slot, "chamber", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "lofihop":
        parts = {"riffI": gen_lofi(r, k, prog, "intro"), "riff": gen_lofi(r, k, prog), "riffB": gen_lofi(r, k, prog, "busy"),
                 "hook": gen_hook(r, k, prog, 64, pick_patch(r.choice(["vibes", "nylon", "rhodes", "flute", "mellotron-flute", "tape-piano", "music-box"]), "rhodes")),
                 "arp": [dict(t, gain="-6dB") for t in gen_arp(r, k, prog, 72, pick_patch("kalimba", "music-box"))]}
        return _write_parts(slot, "lofihop", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "gogo":
        grp = r.choice([[3, 3, 2], [3, 3, 3, 3, 4], [5, 5, 6]])
        piano = gen_ostinato(r, k, prog, 60, "piano", grp)
        ub = pick_patch("upright-bass", "finger-bass")
        bass = [track("bass", ub, " ".join(f"{mname(k.deg(root, 33))}/8@90 R/8 {mname(k.deg(root, 33))}/8@80 {mname(k.deg(root + 4, 33))}/8@84 R/4 {mname(k.deg(root + 2, 33))}/4@82" for root in prog), seed=7)]
        bassB = [track("bass", ub, " ".join(f"{mname(k.deg(root, 33))}/16@92 R/16 {mname(k.deg(root, 45))}/16@80 R/16 R/8 {mname(k.deg(root, 33))}/8@86 {mname(k.deg(root + 4, 33))}/8@80 R/8 {mname(k.deg(root, 45))}/8@84 R/8" for root in prog), seed=7)]
        sw = {"sw": {"points": [["0b", 0.1], ["8b", 1.0], ["16b", 0.3]]}}
        arco = [track("arco", pick_patch("cellos", "strings"), " ".join(f"{mname(k.deg(root, 36))}/1@{70}" for root in prog), auto=sw, gain={"value": "-12dB", "mod": [{"src": "auto.sw", "amount": 6}]})]
        lh = [track("lhoct", "piano", " ".join(f"{chordhead([k.deg(root, 36), k.deg(root, 48)])}/8@{78 if j % 2 == 0 else 66}" for root in prog for j in range(8)), pan=-0.15, gain="-5dB")]
        cresc = {"cr": {"points": [["0b", 0.0], ["16b", 1.0]]}}
        build_piano = [dict(t, auto=cresc, gain={"value": "-6dB", "mod": [{"src": "auto.cr", "amount": 6}]}) for t in piano]
        pianoB = gen_ostinato(r, k, prog, 60, "piano", r.choice([[3, 5], [3, 3, 2]]))
        parts = {"riffP": piano + arco, "riff": piano + bass + gen_trio_drums(r, "groove"), "riffB": pianoB + lh + bassB + gen_trio_drums(r, "breaks"),
                 "riffUp": build_piano + bass + gen_trio_drums(r, "build"), "riffS": piano + bass + gen_trio_drums(r, "sparse")}
        return _write_parts(slot, "gogo", parts, f"{NAMES[p['pc']]} {p['mode']}, piano grouping {'+'.join(map(str, grp))}")
    if style == "ukjazz":
        meter = r.choice([7, 7, 5, 9])
        m = meter * 2 if meter == 5 else meter  # 5/4 as 10/8
        beats = (m * 2 * (4 if m in (7, 9) else 3)) / 4
        bp = pick_patch("tuba", "upright-bass") if r.random() < 0.4 else pick_patch("upright-bass", "finger-bass")
        parts = {"riffK": gen_broken(r, k, prog, m, "sparse", bp), "riff": gen_broken(r, k, prog, m, "main", bp), "riffB": gen_broken(r, k, prog, m, "horns", bp),
                 "hook": gen_tool_lead(r, k, prog, m, 60, pick_patch(r.choice(["clarinet", "flute", "vibes", "tenor-sax", "trumpet-mute"]), "vibes"), reps=int(beats * 2 / m)),
                 "solo": gen_tool_lead(r, k, prog, m, 67, pick_patch("vibes", "rhodes"), reps=int(beats * 2 / m))}
        lens = {role: beats for role in parts}
        return _write_parts(slot, "ukjazz", parts, f"{NAMES[p['pc']]} {p['mode']}, {meter}/{4 if meter == 5 else 8}, bass {bp}", lens)
    if style == "ambient":
        parts = {"riffA": gen_ambient(r, k, prog, "A"), "riffB": gen_ambient(r, k, prog, "B"), "hookE": gen_atmos(r, k, prog, 62, pick_patch("ebow", "ambient-swell"))}
        return _write_parts(slot, "ambient", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "downtempo":
        parts = {"riffI": gen_downtempo(r, k, prog, "intro"), "riff": gen_downtempo(r, k, prog), "riffB": gen_downtempo(r, k, prog, "B"),
                 "hook": gen_hook(r, k, prog, 64, pick_patch(r.choice(["vibes", "flute", "clarinet", "pluck-lead"]), "rhodes"))}
        return _write_parts(slot, "downtempo", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "raga":
        parts = {"riffA": gen_raga(r, k, prog, "alap"), "riffG": gen_raga(r, k, prog, "groove"),
                 "riff": gen_meshuggah(r, k, low, gp, r.choice([14, 22, 20])) + gen_tabla(r, "tirakita"),
                 "riffB": gen_djent(r, k, prog, low) + gen_tabla(r, "sparse"), "riffBrk": gen_meshuggah(r, k, low, gp, 7, grid="8", mode="break"),
                 "hook": gen_hook(r, k, prog, 60, pick_patch("sitar", "lead-monster"))}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "raga", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "gamelan":
        parts = {"riffK": gen_kotekan(r, k, prog), "riff": gen_meshuggah(r, k, low, gp, r.choice([14, 22, 20, 18])) + gen_kotekan(r, k, prog),
                 "riffB": gen_meshuggah(r, k, low, gp, r.choice([13, 23, 26]), mode="toms"), "riffT": gen_tool(r, k, low, 7, [2, 2, 3], "tribal", reps=5),
                 "hook": gen_hook(r, k, prog, 62, rig("lead")), "drone": gen_drone(k, 36, "drone")}
        parts["riffSoft"] = soften(parts["riff"])
        lens = {"riffT": 7 * 5 / 2}
        return _write_parts(slot, "gamelan", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}", lens)
    if style == "koto":
        parts = {"riffK": gen_koto(r, k, prog, "arp") + gen_koto(r, k, prog, "taiko"),
                 "riff": gen_djent(r, k, prog, low) + gen_koto(r, k, prog, "arp"), "riffC": gen_power(r, k, prog, 40, "chorus"),
                 "riffT": gen_koto(r, k, prog, "taiko") + gen_hc(r, k, prog, low, "beatdown"),
                 "hook": gen_hook(r, k, prog, 60, pick_patch("koto", "lead-monster")), "pad": gen_pad(r, k, prog, 48, "strings", gain="-8dB")}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "koto", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "djazz":
        jz = gen_mathcore(r, k, prog, low, "jazz")
        if have("vibes") and r.random() < 0.5:  # mallet break: vibes or marimba take the comping
            jz = [dict(t, patch=r.choice(["vibes", "marimba"])) if t["name"] == "gtr" else t for t in jz]
        parts = {"riffJ": jz, "riffJ2": gen_mathcore(r, k, prog, low, "jazz"),
                 "riff": gen_djent(r, k, prog, low), "riffB": gen_meshuggah(r, k, low, gp, r.choice([14, 22, 20])),
                 "riffC": gen_mathcore(r, k, prog, low), "hook": gen_hook(r, k, prog, 64, pick_patch("lead-tape", "lead-monster")),
                 "pad": gen_clusters(r, k, prog, 48, "saw-pad"), "riffSW": gen_swingmetal(r, k, prog, low)}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "djazz", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "gojira":
        parts = {"riff": gen_gojira(r, k, prog, low, "groove"), "riffB": gen_gojira(r, k, prog, low, "groove"),
                 "riffW": gen_gojira(r, k, prog, low, "whammy"), "riffT": gen_gojira(r, k, prog, low, "tribal"),
                 "riffN": gen_gojira(r, k, prog, low, "harmonic"), "hook": gen_hook(r, k, prog, 64, rig("lead")), "drone": gen_drone(k, 36, "drone")}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "gojira", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "mathcore":
        parts = {"riff": gen_mathcore(r, k, prog, low), "riffB": gen_mathcore(r, k, prog, low), "riffC": gen_mathcore(r, k, prog, low),
                 "riffJ": gen_mathcore(r, k, prog, low, "jazz"), "riffSlam": gen_hc(r, k, prog, low, "slowdown")}
        return _write_parts(slot, "mathcore", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "sludge":
        parts = {"riff": gen_sludge(r, k, prog, 28, "riff"), "riffB": gen_sludge(r, k, prog, 28, "riff"),
                 "riffD": gen_sludge(r, k, prog, 28, "drone"), "riffG": gen_sludge(r, k, prog, 28, "gallop"),
                 "hook": gen_hook(r, k, prog, 62, rig("lead")), "solo": gen_hook(r, k, prog, 64, rig("lead"))}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "sludge", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "breakcore":
        parts = {"riff": gen_breakcore(r, k, prog), "riffB": gen_breakcore(r, k, prog), "riffM": gen_breakcore(r, k, prog, wild=1.6),
                 "riffP": [track("piano", pick_patch("piano", "rhodes"), " ".join(f"{mname(k.deg(root + d, 60))}/16@{90 if d == 0 else 76}" for root in prog for _ in range(4) for d in (0, 2, 4, 7)), pan=0.2)],
                 "riffUp": gen_bro_build(r, k, prog), "pad": gen_pad(r, k, prog, 48, "strings", gain="-8dB")}
        return _write_parts(slot, "breakcore", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "power":
        parts = {"riff": gen_power(r, k, prog, 40, "verse"), "riffC": gen_power(r, k, prog, 40, "chorus"),
                 "hook": gen_twin_hook(r, k, prog, 64, pick_patch("lead-slap", "lead-monster")),
                 "solo": gen_shred(r, k, prog, 64, pick_patch("lead-slap", "lead-monster")),
                 "pad": gen_pad(r, k, prog, 48, "strings", gain="-6dB"), "riffBrk": gen_meshuggah(r, k, 40, gp, 7, grid="8", mode="break")}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "power", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "groovemetal":
        parts = {"riff": gen_groovemetal(r, k, prog, 28, "groove"), "riffB": gen_groovemetal(r, k, prog, 28, "groove"),
                 "riffG": gen_groovemetal(r, k, prog, 28, "gallop"), "riffH": gen_groovemetal(r, k, prog, 28, "half"),
                 "solo": gen_shred(r, k, prog, 64, pick_patch("lead-wah", "lead-monster")), "hook": gen_hook(r, k, prog, 64, rig("lead"))}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "groovemetal", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "deathcore":
        dl = 26  # tuned lower
        parts = {"riff": gen_blast(r, k, prog, dl, "bomb"), "riffB": gen_blast(r, k, prog, dl, "trad"),
                 "riffG": gen_meshuggah(r, k, dl, gp, r.choice([14, 22, 20])), "riffBd": gen_hc(r, k, prog, dl, "beatdown"),
                 "riffSlam": gen_hc(r, k, prog, dl, "slowdown"), "pad": gen_pad(r, k, prog, 48, "strings", gain="-6dB"),
                 "soft": gen_pad(r, k, prog, 48, "strings", gain="-8dB", vel=70), "drone": gen_drone(k, 36, "drone")}
        return _write_parts(slot, "deathcore", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "mahavishnu":
        meter = r.choice([7, 9, 11])
        beats = meter * 4 / 2
        vl = pick_patch("violins", "strings")
        parts = {"riff": gen_mahavishnu(r, k, prog, meter), "riffB": gen_mahavishnu(r, k, prog, meter), "riffS": gen_mahavishnu(r, k, prog, meter, kind="solo"),
                 "solo": gen_thordendal(r, k, 28, vl, int(beats))}
        return _write_parts(slot, "mahavishnu", parts, f"{NAMES[p['pc']]} {p['mode']}, {meter}/8", {role: beats for role in parts})
    if style == "tigran":
        parts = {"riffF": gen_tigran(r, k, prog, "folk"), "riff": gen_tigran(r, k, prog), "riffB": gen_tigran(r, k, prog), "riffH": gen_tigran(r, k, prog, "heavy"),
                 "hook": gen_hook(r, k, prog, 67, "piano")}
        return _write_parts(slot, "tigran", parts, f"{NAMES[p['pc']]} {p['mode']}")
    if style == "cynic":
        parts = {"riffClean": gen_cynic(r, k, prog, kind="clean"), "riff": gen_cynic(r, k, prog), "riffB": gen_cynic(r, k, prog),
                 "riffF": gen_cynic(r, k, prog, kind="fusion"), "hook": gen_hook(r, k, prog, 52, pick_patch("fretless", "finger-bass")),
                 "solo": gen_thordendal(r, k, 28, rig("lead"))}
        return _write_parts(slot, "cynic", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "symphonic":
        parts = {"riffO": gen_symphonic(r, k, prog, kind="orch"), "riffV": gen_symphonic(r, k, prog, kind="verse"),
                 "riffC": gen_symphonic(r, k, prog, kind="chorus"), "hook": gen_hook(r, k, prog, 69, pick_patch(r.choice(["violins", "lead-tape"]), "strings"))}
        return _write_parts(slot, "symphonic", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "metalcore":
        parts = {"riffV": gen_metalcore(r, k, prog, kind="verse"), "riffC": gen_metalcore(r, k, prog, kind="chorus"),
                 "riffH": gen_metalcore(r, k, prog, kind="harmony"), "riffBrk": gen_metalcore(r, k, prog, kind="breakdown"),
                 "hook": gen_hook(r, k, prog, 64, pick_patch("lead-tape", "lead-monster"))}
        return _write_parts(slot, "metalcore", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "slam":
        parts = {"riffSlam": gen_slam(r, k, prog, kind="slam"), "riffSlam2": gen_slam(r, k, prog, kind="slam"), "riffBlast": gen_slam(r, k, prog, kind="blast"),
                 "riffGrav": gen_slam(r, k, prog, kind="gravity"), "riffBrk": gen_slam(r, k, prog, kind="brk")}
        return _write_parts(slot, "slam", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "postmetal":
        lead = rig("lead") if "lead" in RIGS else pick_patch("lead-tape", "lead-monster")
        parts = {"riffClean": gen_postmetal(r, k, prog, kind="clean"), "riffToms": gen_postmetal(r, k, prog, kind="toms"),
                 "riffCrush": gen_postmetal(r, k, prog, kind="crush"), "riffWall": gen_postmetal(r, k, prog, kind="wall"),
                 "hookT": gen_tremolo_lead(r, k, prog, 64, lead), "hookE": gen_atmos(r, k, prog, 62, rig("atmos"))}
        return _write_parts(slot, "postmetal", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "postrock":
        parts = {"riffClean": gen_gaze(r, k, prog, "clean"), "riffH": gen_gaze(r, k, prog, "half"), "riff": gen_gaze(r, k, prog, "drive"),
                 "hook": gen_hook(r, k, prog, 64, pick_patch("lead-tape", "lead-monster")), "hookE": gen_atmos(r, k, prog, 62, rig("atmos"))}
        parts["riffSoft"] = soften(parts["riffH"], 0.7)
        parts["riffUp"] = gen_gaze(r, k, prog, "half")
        return _write_parts(slot, "postrock", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "numetal":
        parts = {"riff": gen_numetal(r, k, prog, 23, "bounce"), "riffB": gen_numetal(r, k, prog, 23, "bounce"),
                 "riffV": gen_numetal(r, k, prog, 23, "verse"), "riffH": gen_numetal(r, k, prog, 23, "chorus"),
                 "riffBrk": gen_hc(r, k, prog, 23, "beatdown"), "hook": gen_hook(r, k, prog, 62, rig("lead")), "pad": gen_clusters(r, k, prog, 48, "saw-pad")}
        parts["riffSoft"] = soften(parts["riff"])
        return _write_parts(slot, "numetal", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
    if style == "industrial":
        parts = {"riff": gen_industrial(r, k, prog, low, "march"), "riffS": gen_industrial(r, k, prog, low, "stomp"),
                 "riffV": gen_industrial(r, k, prog, low, "verse"), "hook": gen_hook(r, k, prog, 64, pick_patch("synth-lead", "lead-monster")),
                 "pad": gen_pad(r, k, prog, 48, pick_patch("supersaw", "saw-pad"), gain="-12dB")}
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
            "riffT": gen_tool(r, k, low, m3, g3, "tribal") + ([track("tabla", pick_patch("tabla-kit"), " ".join(
                (f"{r.choice(['na', 'tin', 'te', 'ge', 'dha'])}/8@{90}" if r.random() < 0.6 else "R/8") for _ in range(m3 * reps_for(m3))), pan=-0.2)] if have("tabla-kit") else []),
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
            "riffBrk2": gen_meshuggah(r, k, low, gp, r.choice([5, 9, 11]), grid="8", mode="break"),
            "riffSlam": gen_hc(r, k, prog, low, "slowdown"),
            "riffS": gen_meshuggah(r, k, low, gp, r.choice([11, 7, 10, 5]), grid="12", mode="shuffle"),
            "riffBrk": gen_meshuggah(r, k, low, gp, r.choice([7, 11, 5]), grid="8", mode="break"),
            "hook": gen_hook(r, k, prog, 62, rig("lead")),
            "solo": gen_thordendal(r, k, low, rig("lead")),
            "pad": gen_clusters(r, k, prog, 48, "saw-pad"),
            "soft": gen_clusters(r, k, prog, 48, "ambient-swell", vel=68),
            "arp": gen_arp(r, k, prog, 55, "arp-pluck"),
            "hold": gen_hold(r, k, prog, low, gp),
            "drone": gen_drone(k, 36, "drone"),
        }
        desc = f"{NAMES[p['pc']]} {p['mode']}, cycles {'/'.join(f'{c}/16' for c in cycles)}, rigs {p.get('rigset', 'modern')}"
        names = {}
        import zlib
        if FUSION and not LITE:
            fusion_layers("meshuggah", parts, None, desc)
        er = random.Random(zlib.crc32(f"enrich{desc}".encode()))
        for role, tr in parts.items():
            n = f"gen-{slot}-{role}"
            if "Bl" not in role:
                tr = [drum_enrich(t, er) for t in tr]
            write(n, f"{role} for meshuggah in {desc}", tr)
            names[role] = n
        return names, desc
    if style == "djent":  # the modern form: ambient cleans, polyrhythmic verses, a glitch edit, open choruses, tapping, breakdowns
        verse = gen_djent(r, k, prog, low)
        glitch_fx = [{"type": "stutter", "slice": r.choice(["1/32", "1/16"]), "repeats": r.choice([2, 3, 4]), "chance": 0.35, "seed": r.randrange(1000)},
                     {"type": "crush", "bits": 10, "rate": 16000, "mix": 0.3}]
        glitch = [dict(t, fx=list(t.get("fx", [])) + glitch_fx) if t.get("name", "").startswith("gtr") else t for t in gen_djent(r, k, prog, low)]
        lead = r.choice(["lead-monster", "synth-lead"] + (["supersaw"] if have("supersaw") else []))
        parts = {"riffClean": gen_djent_clean(r, k, prog), "riff": verse, "riffG": glitch, "riffC": gen_metalcore(r, k, prog, low, kind="chorus"),
                 "riffBrk": gen_djent(r, k, prog, low, True), "hook": gen_hook(r, k, prog, 64, lead),
                 "tap": gen_tapping(r, k, prog, pick_patch(r.choice(["clean-chorus", "pluck-lead"]), "clean-chorus")),
                 "pad": gen_clusters(r, k, prog, 48, pick_patch("saw-pad", "pad"))}
        return _write_parts(slot, "djent", parts, f"{NAMES[p['pc']]} {p['mode']}, rigs {p.get('rigset', 'modern')}")
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
