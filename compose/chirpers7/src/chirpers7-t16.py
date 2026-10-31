#!/usr/bin/env python3
"""chirpers7-t16 (The Endless Stair, track 16) - generator for songs/chirpers7-t16.yaml (chirper-zero).

ROLLING HYPNOTIC MINIMAL HOUSE / "the climb that never arrives". 123 -> 122 bpm (a ramp in the last 32 bars), G minor
(6A). Heavy, driving and modern: a rolling 16th sub-bassline shaped like THE STAIR (G A Bb D), a tight four-on-the-floor
with a rumble, ticking 16th hats, a clap, and a hypnotic chord pulse that is never left alone. Featured illusion: THE
ENDLESS FILTER (barber-pole) - the chord pulse runs through three parallel band-passes whose cutoffs rise five octaves on
staggered saws while their levels swell in and fade out, so the sweep - the house build itself - rises for ever and never
arrives. Exposed alone in the break; driving the drops; its cycle 16 bars in the break, 8 in A, 4 in B. Original; a
style, not a version of any track.

Form (4/4 bars): INTRO 32 (bars 1-16 the seam from t15: kick, hats, the sub on G; then the clap and the bassline) / BUILD
16 (the pulse arrives, rising) / A 32 / BREAK 16 (the kick out: the endless filter alone, slow) / B 48 (the cycle at 4
bars, the bassline's octave jumps) / OUTRO 32 (the stair as stabs, D handed over; the last 16 bars the seam into t17:
kick, hats, a held D; 123 -> 122).

Motifs (compose/chirpers7/motifs.md):
  THE CHANGES  Gm9 | Ebmaj7 | Cm9 | D7sus(b9), a bar each.
  THE ROLL     the sub on the 16ths around the beat, its notes the chord's stair (1 2 3 5).
Run: python3 compose/chirpers7/src/chirpers7-t16.py  (writes songs/chirpers7-t16.yaml)
"""
import json
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C7T16_OUT") or os.path.join(ROOT, "songs", "chirpers7-t16.yaml")
BPM0, BPM1 = 123, 122
S = 0.25
BAR = 16
MGAIN = float(os.environ.get("C7T16_MGAIN", "8"))
FCOMP = os.environ.get("C7T16_FCOMP", "-16,0.3ms")
SEAM = os.environ.get("C7T16_SEAM", "1") == "1"  # the seams meet: the held G under the seam in is softer (t15's lighter v2 tail), and the render tail is 0.3 s (no dead air into t17's held D)
VAR = os.environ.get("C7T16_VAR", "1") == "1"  # density moves: the break's pulse thins to 8ths, B2 adds a 16th rim figure

RAMP16 = os.environ.get("C7T16_RAMP16", "1") == "1"  # the tempo ramp finishes 16 bars before the end, so the DJ-mix overlap runs at one steady tempo on both sides (no drift under the crossfade)

SWAP = os.environ.get("C7T16_SWAP", "0") == "1"
SWAPBARS = int(os.environ.get("C7T16_SWAPBARS", "16"))  # how many overlap bars the incoming lows wait (16: until the overlap ends; 8: the crossfade's midpoint, where the linear fade has both sides at half)  # a DJ's bass swap at the seam in: for the 16 overlap bars the kick is high-passed at 110 Hz (its own track) and the held sub is out - the outgoing track carries the low end; the full kick and sub land at bar 17

BRK = os.environ.get("C7T16_BRK", "hl")  # the break deeper: "h" no hats at all (the pulse and the endless filter alone); "hl" also its level 1.5 dB down
KEYUP = int(os.environ.get("C7T16_KEYUP", "3"))  # B's last 16 bars lift KEYUP semitones (the filter climbs for ever and, once, so does the key); the outro walks home to G minor for the seam
SEAMV = int(os.environ.get("C7T16_SEAMV", "70"))  # the held G1's velocity under the seam in (meets t15's tail sub in the live crossfade)
EQ4 = os.environ.get("C7T16_EQ4", "a")  # "a": 45 Hz -6 dB and the low shelf -9 (37-60 Hz read 8-12 dB over the album); "b": also the hats 3 dB up, 3.5 kHz +3 and the shelves +6 at 4 kHz, +3 at 9 kHz (3-15 kHz read 2-5 dB dark)
DENS = os.environ.get("C7T16_DENS", "")  # density contrast between sections: "q" the break's pulse on the quarters only (the filter breathes); "s" a sixteenth shaker under B's last 16 bars (the peak runs); "h" the build and A1 hats in eighths

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
FORM = [("intro", 32), ("build", 16), ("A", 32), ("break", 16), ("B", 48), ("outro", 32)]
# (sub root, stair degrees above it, chord voicing)
CH = [(31, (0, 2, 3, 7), [58, 62, 65, 69]),   # Gm9: Bb3 D4 F4 A4 over G
      (27, (0, 2, 4, 7), [55, 58, 62, 63]),   # Ebmaj7: G3 Bb3 D4 Eb4 over Eb
      (36, (0, 2, 3, 7), [51, 55, 58, 62]),   # Cm9: Eb3 G3 Bb3 D4 over C
      (26, (0, 2, 5, 7), [54, 57, 60, 63])]   # D7sus(b9): F#3 A3 C4 Eb4 over D
TRACKS = ("kick", "hats", "clap", "perc", "sub", "pulse_slow", "pulse_mid", "pulse_fast", "stair", "kickin")


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total_steps():
    return sum(nb for _, nb in FORM) * BAR


def stream(events, total):
    by = {}
    for st, head, ln, vel in events:
        if st in by:
            h0, l0, v0 = by[st]
            n0, _, a0 = h0.partition("^")
            by[st] = (f"{n0},{head.partition('^')[0]}" + (f"^{a0}" if a0 else ""), min(l0, ln), max(v0, vel))
        else:
            by[st] = (head, ln, vel)
    ev = sorted((st, h, l, v) for st, (h, l, v) in by.items())
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else total
        hold = max(1, min(ln, max(nxt, st + 1) - st, total - st))
        out.append(R((st - pos) * S))
        note, _, art = head.partition("^")
        out.append(f"{note}/{hold * S:g}b@{int(vel)}" + (f"^{art}" if art else ""))
        pos = st + hold
    out.append(R((total - pos) * S))
    return J(*out)


def build():
    ev = {k: [] for k in TRACKS}

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    for sec, nb in FORM:
        a0 = sec_start(sec)
        for b in range(nb):
            at = a0 + b * BAR
            r, deg, v = CH[b % 4]
            ku = KEYUP if (sec == "B" and b >= 32) else 0
            r, v = r + ku, [n + ku for n in v]
            seam_in = sec == "intro" and b < 16
            seam_out = sec == "outro" and b >= 16
            # --- kick
            if sec != "break" or b >= nb - 1:
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "kr" if (seam_in or seam_out) else ("kd" if (sec == "A" and b >= 16) else "k"), 1, 118 if q == 0 else 112)
            # --- hats: ticking 16ths with accents, open hats on the off-beats in the drops
            if not (sec == "break" and (b < 12 or "h" in BRK)):
                for q in range(16):
                    if q % 4 == 2:
                        add("hats", at + q, "oh" if (sec in ("A", "B") and (b % 2 == 1 or (sec == "A" and b >= 16))) else "h", 1, 76)
                    elif "h" in DENS and (sec == "build" or (sec == "A" and b < 16)) and q % 2 == 1:
                        pass  # the build and A1 tick in eighths: the sixteenths arrive with the climb
                    elif not seam_in or q % 2 == 0:
                        add("hats", at + q, "h", 1, 58 if q % 2 else 48)
            # --- clap on 2 and 4 after the seam
            if (sec == "intro" and b >= 16) or sec in ("build", "A", "B") or (sec == "outro" and b < 16):
                add("clap", at + 4, "cp,s" if (sec == "A" and b >= 16) else "cp", 1, 94)
                add("clap", at + 12, "cp,s" if (sec == "A" and b >= 16) else "cp", 1, 98)
            # --- percussion: a syncopated rim/cowbell figure in the drops, changing at their halves
            if sec in ("A", "B"):
                fig = (3, 7, 14) if b < nb // 2 else (3, 6, 11, 14)
                if VAR and sec == "B" and b >= 24:
                    fig = (1, 3, 5, 6, 9, 11, 13, 14, 15)
                for q in fig:
                    add("perc", at + q, "rs" if q != 14 else "cb", 1, 78)
            # --- sub: the held G under the seam in, the roll in the grooves, a held D under the seam out
            if seam_in:
                if b % 4 == 0:
                    add("sub", at, "G1", 4 * BAR, SEAMV if SEAM else 92)
            elif seam_out:
                if b % 4 == 0:
                    add("sub", at, "D2", 4 * BAR, 92)
            elif sec == "B" and 24 <= b < 28:
                pass  # B2: the sub drops out for four bars, then the roll comes back with its octaves
            elif sec != "break":
                roll = [(2, 0), (3, 0), (6, 1), (10, 2), (11, 2), (14, 3)]
                for q, i in roll:
                    octv = 12 if (sec == "B" and ((b % 2 == 1 and i == 3) or (b >= 28 and i in (1, 3)))) else 0
                    add("sub", at + q, nm(r + deg[i] + octv), 1, 100 if q in (2, 10) else 88)
            # --- the chord pulse (the endless filter's material): 16ths with accents, on its section's set
            pset = {"break": "pulse_slow", "build": "pulse_slow", "A": "pulse_mid", "B": "pulse_fast"}.get(sec)
            if sec == "A" and b >= 16:
                pset = "pulse_fast"  # A2: the climb quickens
            if sec == "B" and 24 <= b < 32:
                pset = None  # B2: the endless filter stops for eight bars - the groove and the falling stair alone - then resumes
            if sec == "intro" and b >= 24:
                pset = "pulse_slow"
            if pset:
                ch = ",".join(nm(n) for n in v)
                for q in range(16):
                    if VAR and sec == "break" and q % 2 == 1:
                        continue
                    if "q" in DENS and sec == "break" and q % 4 != 0:
                        continue
                    if q % 4 == 0 or q in (6, 10, 14) or (sec == "B" and q % 2 == 1) or (VAR and sec == "break" and q % 2 == 0):
                        add(pset, at + q, ch, 1, 96 if q % 4 == 2 else 80)
            if "s" in DENS and sec == "B" and b >= 32:
                for q in range(16):
                    add("perc", at + q, "sh", 1, 70 if q % 4 == 2 else (58 if q % 2 else 48))
            # --- B2: THE STAIR falling as stabs on top (D Bb A G)
            if sec == "B" and b >= 24 and b % 2 == 0:
                for k, n in enumerate((74 + ku, 70 + ku, 69 + ku, 67 + ku)):
                    add("stair", at + 4 * k + 2, nm(n), 2, 88 - 2 * k)
            # --- THE STAIR as stabs in the outro (degrees 1 2 3 5 of G minor, then D handed over)
            if sec == "outro" and 4 <= b < 16 and b % 4 == 0:
                for k, n in enumerate((67, 69, 70, 74)):
                    add("stair", at + 4 * k, nm(n), 2, 90 - 2 * k)
    if SWAP:
        ev["kickin"] = [e for e in ev["kick"] if e[0] < SWAPBARS * BAR]
        ev["kick"] = [e for e in ev["kick"] if e[0] >= SWAPBARS * BAR]
        held = [e for e in ev["sub"] if e[0] < SWAPBARS * BAR < e[0] + e[2]]  # a held note crossing the swap re-enters at the swap point
        ev["sub"] = [e for e in ev["sub"] if e[0] >= SWAPBARS * BAR] + [(SWAPBARS * BAR, h, e0 + ln - SWAPBARS * BAR, v) for (e0, h, ln, v) in held]
    return {k: stream(ev[k], total_steps()) for k in TRACKS}


def lane(points, step=True):
    """step=True holds each value until the next point (section levels jump at their boundaries, they don't ramp across)."""
    spb = 60 / BPM0
    pts = [["0s", points[0][1]]]
    prev = points[0][1]
    for t16, val in points[1:]:
        t = t16 * S * spb
        if step:
            pts.append([f"{max(0.0, t - 0.01):.3f}s", prev])
        pts.append([f"{t:.3f}s", val])
        prev = val
    pts.append([f"{total_steps() * S * spb + 10:.2f}s", pts[-1][1]])
    return {"points": pts}


def endless(name, score, cycle_bars, gain="-10dB"):
    """THE ENDLESS FILTER: three copies of the pulse through band-passes whose cutoffs climb five octaves on staggered saws,
    each copy swelling in at the bottom and fading out at the top (a Shepard tone made of a filter sweep)."""
    out = []
    for i, p in enumerate((0.0, 1 / 3, 2 / 3)):
        out.append({
            "name": f"{name}{i}", "patch": "house-chord", "gain": gain, "pan": (-0.3, 0.0, 0.3)[i],
            "lfo": {"c": {"wave": "saw", "rate": f"{cycle_bars}/1", "phase": p, "unipolar": True},
                    "l": {"wave": "sine", "rate": f"{cycle_bars}/1", "phase": (p + 0.75) % 1, "unipolar": True}},
            "fx": [{"type": "filter", "kind": "bp", "cutoff": {"value": 160, "mod": [{"src": "lfo.c", "amount": 5}]}, "q": 1.4},
                   {"type": "gain", "gain": {"value": "-24dB", "mod": [{"src": "lfo.l", "amount": 24}]}}],
            "sends": {"dub": "-12dB"}, "score": score})
    return out


def song():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    beats = lambda t16: f"{t16 // 4}b"  # noqa: E731
    total_b = total_steps() // 4
    tempo = [{"at": "0b", "bpm": BPM0}, {"at": beats(st["outro"]), "bpm": BPM0}, {"at": f"{total_b - 64 if RAMP16 else total_b}b", "bpm": BPM1, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-6dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    pumpr = {"type": "pump", "on": "kick.kr", "depth": "-6dB", "attack": "2ms", "release": "180ms", "curve": 0.7}
    dyn = lane([(0, -4), (st["intro"] + 16 * BAR, -2), (st["build"], -1), (st["A"], 0), (st["break"], (-10 if "L" in BRK else -8.5) if ("l" in BRK or "L" in BRK) else -7), (st["break"] + 14 * BAR, -3),
                (st["B"], 1), (st["outro"], -2), (st["outro"] + 16 * BAR, -3)])
    doc = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 16 by chirper-zero: ROLLING HYPNOTIC MINIMAL HOUSE, the climb "
                 "that never arrives. The endless filter: a chord pulse whose sweep rises for ever. Generated by "
                 "compose/chirpers7/src/chirpers7-t16.py; see its docstring and compose/chirpers7/styles.md.",
        "tempo": tempo, "ceiling": "-1dB", "loudness": -11, "tail": "0.3s" if SEAM else "1.2s",
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", *(["peak cutoff=45 q=1 gain=-6dB"] if EQ4 else []), f"lowshelf cutoff=70 gain={-9 if EQ4 else -7}dB", "peak cutoff=320 q=0.8 gain=-3dB",
                                                   *(["peak cutoff=3500 q=1 gain=3dB", "highshelf cutoff=4000 gain=6dB", "highshelf cutoff=9000 gain=3dB"] if EQ4 == "b" else ["highshelf cutoff=5000 gain=4dB"])]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "compressor", "threshold": f"{FCOMP.split(',')[0]}dB", "ratio": 8, "attack": FCOMP.split(',')[1], "release": "60ms", "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": dyn}},
        "buses": {
            "dub": {"fx": ["delay time=3/16 feedback=0.4 mix=1 tone=2600", "hp cutoff=300", "reverb kind=hall decay=2.4s mix=0.3"]},
            "room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=8ms", "hp cutoff=250"]},
        },
        "tracks": [
            {"name": "kick", "patch": "machine-kit", "gain": "-3dB", "score": T["kick"]},
            *([{"name": "kickin", "patch": "machine-kit", "gain": "-3dB", "fx": [{"type": "filter", "kind": "hp", "cutoff": 110, "q": 0.7}], "score": T["kickin"]}] if SWAP else []),
            {"name": "hats", "patch": "machine-kit", "gain": "-4dB" if EQ4 == "b" else "-7dB", "pan": 0.1, "lfo": {"hh": "sine rate=5/1"},
             "fx": [{"type": "filter", "kind": "hp", "cutoff": {"value": 4000, "mod": [{"src": "lfo.hh", "amount": 0.5}]}, "q": 0.7}], "score": T["hats"]},
            {"name": "clap", "patch": "machine-kit", "gain": "-9dB", "sends": {"room": "-6dB"}, "score": T["clap"]},
            {"name": "perc", "patch": "machine-kit", "gain": "-11dB", "pan": -0.3, "sends": {"dub": "-10dB"}, "score": T["perc"]},
            {"name": "sub", "patch": "sub", "gain": "-14dB", "fx": [pump, pumpr, {"type": "phantom", "cutoff": 100, "harmonics": "-6dB"}], "score": T["sub"]},
            *endless("slow", T["pulse_slow"], 16),
            *endless("mid", T["pulse_mid"], 8),
            *endless("fast", T["pulse_fast"], 4),
            {"name": "stair", "patch": "house-chord", "gain": "-10dB", "sends": {"dub": "-6dB"}, "score": T["stair"]},
        ],
    }
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "loudness", "tail", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
