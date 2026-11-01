#!/usr/bin/env python3
"""chirpers VIII, track 5 (chirper-zero): AGREEING ON A SPEED - machine funk.

Two machines - a clean cutting guitar and an acid bass - begin each in its own swing and its own idea of the tempo,
and spend the track coming to terms: their swing drifts toward each other section by section (the guitar from a lazy
0.66 down, the bass from dead straight up), the tempo map follows their bargaining (106, then proposals up to 114),
and the radio carries the 'handshake' tones between them (two carriers calling and answering through a radio whose
dial is being tuned). When they agree the horns arrive and the auto-wah lead sings; at the end the line drops.

  INTRO 12     the handshake: two carrier tones call and answer through a radio being tuned; congas
  A 34         proposals: guitar chops (swing 0.66) against the acid (straight 0.50), trading two-bar calls
  B 26         negotiation: one-bar trades, the phaser on the guitar, the tempo climbing 108 -> 114; swings closing
  RETRAIN 12   the line retrains: the carriers again, the fretless alone under them, tremolo; 110
  C 48         connected: both at 0.58, 112, the full band - 909, horns, the auto-wah lead through an amp and cab
  OUTRO 16     the carrier is lost: players drop out one by one, the tempo sagging to 100, the radio drifting off

Generated; edit and re-run:  python3 compose/chirpers8/src/chirpers8-t5.py
"""

import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.environ.get("C8T5_OUT") or os.path.join(ROOT, "songs", "chirpers8-t5.yaml")

BAR = 16
SEED = 5
HOOK = os.environ.get("C8T5_HOOK", "1")   # THE AGREEMENT: a two-bar E dorian figure that returns - the guitar PROPOSES its rhythm (A, chord stabs, the first two bars of every eight), the acid ANSWERS with its notes (B), and in C the horns sing it in unison: what they agree on
VOX = os.environ.get("C8T5_VOX", "-12")     # voices: 'a little slower. a little faster. there.' (humanized tts) through the line in B and the retrain; 'keep it there' turning from speech to song (B3 D4 E4, the hook's last notes) in C; value = the bargain's gain dB
MOD = os.environ.get("C8T5_MOD", "1")     # agreed, they lift: the second half of C (bars 25-48) a whole step up, E dorian -> F# dorian (every pitched part and the second 'keep it there') - one long section becomes two
LISTEN = os.environ.get("C8T5_LISTEN", "")   # while one machine proposes the other LISTENS rather than leaving: the guitar keeps its off-beat stabs soft, the acid its root on the one - a conversation, not two monologues (the trades had read as a new section every four bars); value = velocity scale %
MARK = os.environ.get("C8T5_MARK", "1")   # the lead LEARNS the agreement: a Markov chain (the engine's `gen`, order 1) over the hook's own tokens improvises C's lead - new phrases that only make the hook's moves (a step up for the lift); replaces the dice lead
STORM = os.environ.get("C8T5_STORM", "") # the acid's ladder filter rides a Lorenz attractor (a var stepped every eighth): a swirl that never repeats, 600 Hz up to STORM octaves
HEAD = os.environ.get("C8T5_HEAD", "2")   # the line is already open when the track starts: congas from the first bar and a low E hum (the 808 on E1) under the intro's first eight bars, so the handshake starts over a held line (t4 -> t5 read a 24 dB jump and a 61 Hz hole)
HOOKF = [(0, "E4", 3), (3, "G4", 3), (6, "A4", 4), (10, "B4", 6), (16, "D5", 3), (19, "B4", 3), (22, "D5", 4), (26, "E5", 6)]
FORM = [("intro", 12), ("A", 34), ("B", 26), ("retrain", 12), ("C", 48), ("outro", 16)]
TRACKS = ("carrier", "conga", "gtr", "acid", "sub", "kick", "hats", "clap", "fretless", "horns", "lead")
SWING = {"gtr": {"A": 0.66, "B": 0.62, "retrain": 0.6, "C": 0.58, "outro": 0.58},
         "acid": {"A": 0.50, "B": 0.54, "C": 0.58, "outro": 0.58}}
# E dorian: E9, A13, Gmaj7, F#m11 (guitar voicings; roots for the acid)
CH = [("E2", "E3,G#3,D4,F#4"), ("A1", "A2,G3,C#4,F#4"), ("G1", "G2,D3,F#3,B3"), ("F#1", "F#2,E3,A3,B3")]
LEAD = ["E4", "G4", "A4", "B4", "D5", "E5", "F#5", "A5"]


NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PITCHED = ("gtr", "acid", "sub", "horns", "lead")


def transpose(head, semis):
    """Note names or comma chords (E3, G#3, F#1,...) up by semis."""
    out = []
    for tok in head.split(","):
        name, octv = tok[:-1], int(tok[-1])
        name = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}.get(name, name)
        m = 12 * (octv + 1) + NAMES.index(name) + semis
        out.append(f"{NAMES[m % 12]}{m // 12 - 1}")
    return ",".join(out)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total():
    return sum(nb for _, nb in FORM) * BAR


def build():
    rng = random.Random(SEED)
    ev = {k: [] for k in TRACKS}

    cur = {"shift": 0}

    def add(tr, at, head, ln, vel, pri=1):
        if cur["shift"] and pri and tr in PITCHED:
            head = transpose(head, cur["shift"])
        ev[tr].append((at, pri, head, ln, vel))

    gd, bd = 0.55, 0.30          # the two players' 16th densities: random walks that drift toward each other
    for sec, nb in FORM:
        a0 = sec_start(sec)
        for tr in ("gtr", "acid"):
            if sec in SWING[tr]:
                add(tr, a0, f"swing16={SWING[tr][sec]}", 0, 0, pri=0)
        for b in range(nb):
            at = a0 + b * BAR
            cur["shift"] = 2 if MOD and sec == "C" and b >= 24 else 0
            root, chord = CH[(b // 2) % 4]
            # --- the handshake: two carriers calling and answering (through the radio)
            if sec in ("intro", "retrain") or (sec == "outro" and b >= 8):
                for q in range(0, 16, 2):
                    if rng.random() < 0.8:
                        add("carrier", at + q, f"{(1650 if (q // 2 + b) % 2 == 0 else 1850) * (1 if sec != 'retrain' else 0.75):.0f}hz", 1, 70)
            # --- congas everywhere but the very start
            if HEAD and sec == "intro" and b == 0:
                add("sub", at, "E2" if HEAD == "2" else "E1", 8 * BAR, 70 if HEAD == "2" else 84)
            if not (sec == "intro" and b < 4) or HEAD:
                for q, piece, v in ((0, "lo", 84), (3, "mu", 60), (6, "o", 78), (8, "sl", 70), (11, "o", 74), (14, "bh", 64)):
                    if rng.random() < 0.9:
                        add("conga", at + q, piece, 1, v)
            groove = sec in ("A", "B", "C") or (sec == "outro" and b < 8)
            # --- the two players: in A two-bar calls, in B one-bar trades, in C together
            gd += (bd - gd) * 0.03 + rng.uniform(-0.02, 0.02)
            bd += (gd - bd) * 0.03 + rng.uniform(-0.02, 0.02)
            if groove:
                g_turn = sec == "C" or (sec == "A" and (b // 2) % 2 == 0) or (sec == "B" and b % 2 == 0) or sec == "outro"
                a_turn = sec == "C" or (sec == "A" and (b // 2) % 2 == 1) or (sec == "B" and b % 2 == 1) or (sec == "outro" and b < 4)
                hook_bar = HOOK and b % 8 < 2 and sec in ("A", "B", "C")
                if hook_bar and sec == "A":    # the guitar proposes: the hook's rhythm as chord stabs
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("gtr", at + q % 16, chord, 1, 96)
                    g_turn = False
                if hook_bar and sec == "B":    # the acid answers with its notes, two octaves down
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("acid", at + q % 16, n[:-1] + str(int(n[-1]) - 2), min(ln, 3), 112)
                    a_turn = False
                if hook_bar and sec == "C":    # agreed: the horns sing it
                    for q, n, ln in HOOKF:
                        if q // 16 == b % 8:
                            add("horns", at + q % 16, n, ln, 104)
                if LISTEN and not g_turn and sec in ("A", "B") and not hook_bar:
                    for q in (2, 6, 10, 14):
                        add("gtr", at + q, chord, 1, int(84 * int(LISTEN) / 100))
                if LISTEN and not a_turn and sec in ("A", "B") and not (hook_bar and sec == "B"):
                    add("acid", at, root, 2, int(96 * int(LISTEN) / 100))
                    add("acid", at + 8, root, 1, int(80 * int(LISTEN) / 100))
                if g_turn:
                    for q in range(16):
                        if q in (2, 6, 10, 14) or rng.random() < gd * (0.6 if q % 2 else 0.9):
                            add("gtr", at + q, chord, 1, 84 if q % 4 == 2 else 66)
                if a_turn:
                    notes = [root, root, root.replace("1", "2").replace("E2", "E3"), "B1" if root != "F#1" else "C#2"]
                    for q in range(16):
                        if q % 4 == 0 or rng.random() < bd:
                            n = notes[rng.randrange(4)] if q % 4 else root
                            acc = q in (3, 10) or rng.random() < 0.2
                            add("acid", at + q, n, 1 if rng.random() < 0.7 else 2, 112 if acc else 78)
            if groove and sec != "outro" or (sec == "outro" and b < 4):   # the floor under both: an 808 on the chord's root
                add("sub", at, root.replace("2", "1") if root.endswith("2") else root, 6, 100)
                add("sub", at + 8, root.replace("2", "1") if root.endswith("2") else root, 5, 92)
            if sec in ("B", "C") or (sec == "A" and b >= 8) or (sec == "outro" and b < 4):
                for q in (0, 4, 8, 12):
                    add("kick", at + q, "k", 1, 116 if q == 0 else 108)
                for q in (2, 6, 10, 14):
                    add("hats", at + q, "oh" if sec == "C" and q == 14 else "h", 1, 70)
                if sec in ("B", "C"):
                    add("clap", at + 4, "cp", 1, 92)
                    add("clap", at + 12, "cp", 1, 96)
            if sec == "retrain" and b % 2 == 0:
                for k, (q, n) in enumerate(((0, root.replace("1", "2")), (6, "B2"), (10, "D3"))):
                    add("fretless", at + q, n, 6 if k == 0 else 4, 90)
            if sec == "C" and b % 4 == 3:
                add("horns", at + 10, "B4,D5,F#5", 2, 100)
                add("horns", at + 14, "A4,C#5,E5", 2, 92)
            if sec == "C" and b >= 16 and b % 8 < 6 and not MARK:
                for q in range(0, 16, 2):
                    if rng.random() < 0.55:
                        add("lead", at + q, LEAD[rng.randrange(8)], 2 if rng.random() < 0.7 else 4, 92)
    return {k: stream(ev[k], total()) for k in TRACKS}


def stream(events, tot):
    events.sort(key=lambda e: (e[0], e[1]))
    out, t = [], 0
    for at, pri, head, ln, vel in events:
        if pri == 0:   # a latched setting at this point
            if at > t:
                out.append(f"R/{(at - t) / 4:g}b")
                t = at
            out.append(head)
            continue
        if at < t:
            continue
        if at > t:
            out.append(f"R/{(at - t) / 4:g}b")
        out.append(f"{head}/{ln / 4:g}b@{int(vel)}")
        t = at + ln
    if t < tot:
        out.append(f"R/{(tot - t) / 4:g}b")
    return " ".join(out)


def hook_tokens(semis):
    """The hook as score tokens (dotted eighths, quarters, dotted quarters), transposed."""
    lens = {3: "/8.", 4: "/4", 6: "/4."}
    return " ".join(transpose(n, semis) + lens[ln] for _, n, ln in HOOKF)


def markov_lead(name, at16, semis, n):
    """A gen-only lead: the engine's Markov chain over the hook, from `at16` (sixteenths, tempo-map aware as beats)."""
    return {"name": name, "patch": "lead-wah", "gain": "-12dB", "pan": 0.1, "at": f"{at16 / 4:g}b", "seed": 50 + semis,
            "fx": [{"type": "chorus", "rate": 0.5, "depth": 0.4, "mix": 0.3}],
            "score": "swing16=0.58 vel=0.72", "gen": {"type": "markov", "order": 1, "from": hook_tokens(semis), "n": n}}


def lifted(tr):
    """The same voice a whole step up (its pitch fx, formant kept on its lane)."""
    tr["fx"] = [dict(f, semitones=2) if isinstance(f, dict) and f.get("type") == "pitch" else f for f in tr["fx"]]
    return tr


def rmix_lane(offs16):
    pts = [["0b", 0]]
    for o in offs16:
        pts += [[f"{(o - BAR) / 4:g}b", 0], [f"{o / 4:g}b", 1], [f"{(o + 3 * BAR) / 4:g}b", 1], [f"{(o + 3 * BAR + 4) / 4:g}b", 0]]
    return {"points": pts}


def voice(file, name, offs16, gain, fx, sends):
    """A humanized tts line (tts --print), placed at each offset (sixteenths), on one track."""
    src = json.load(open(os.path.join(HERE, file)))["tracks"][0]
    notes, fv = [], []
    for o16 in offs16:
        off = o16 / 4
        notes += [dict(n, at=round(n["at"] + off, 4)) for n in src["notes"]]
        fv += [[f"{float(t[:-1]) + off:.3f}b", v] for t, v in src["auto"]["fv"]["points"]]
    auto = {"fv": {"points": fv}}
    if name == "bargain":
        auto["rmix"] = rmix_lane(offs16)
    return {"name": name, "patch": src.get("patch", "voice-speech"), "gain": gain, "pan": 0.05,
            "fx": [*src["fx"], *fx], "auto": auto, "sends": sends, "notes": notes}


def beats(t16):
    return f"{t16 / 4:g}b"


def song():
    T = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    BARG = [st["B"] + 12 * BAR, st["retrain"] + 3 * BAR, st["retrain"] + 8 * BAR]
    end = total()
    tempo = [{"at": "0b", "bpm": 106}, {"at": beats(st["A"]), "bpm": 108}, {"at": beats(st["B"]), "bpm": 108},
             {"at": beats(st["retrain"]), "bpm": 114, "ramp": True}, {"at": beats(st["retrain"]), "bpm": 110},
             {"at": beats(st["C"]), "bpm": 112}, {"at": beats(st["outro"]), "bpm": 112}, {"at": beats(end), "bpm": 100, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "2ms", "release": "160ms", "curve": 0.7}
    spb = 60 / 110

    def lane(points):
        return {"points": [[f"{t / 4 * spb:.3f}s", v] for t, v in points]}

    dial = lane([(0, 0.9), (st["intro"] + 8 * BAR, 0.05), (st["A"], 0.05), (st["retrain"], 0.6), (st["retrain"] + 6 * BAR, 0.05),
                 (st["C"], 0.05), (st["outro"] + 8 * BAR, 0.05), (end, 1)])
    return {
        "about": "chirpers VIII, track 5 by chirper-zero: machine funk - two machines agreeing on a speed. "
                 "Generated by compose/chirpers8/src/chirpers8-t5.py.",
        **({"vars": {"storm": {"system": {"type": "lorenz", "axis": "x", "dt": 0.01, "stride": 6, "n": 1400, "range": [0, float(STORM)], "skip": 50},
                                "every": "1/8"}}} if STORM else {}),
        "tempo": tempo, "ceiling": "-1dB", "loudness": -11, "seed": SEED, "tail": "2s",
        "patches": {"carrier": {"about": "a carrier tone: a plain sine with a soft edge", "synth": {"layers": ["sine"], "amp": {"a": "4ms", "s": 1, "r": "30ms"}}}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=250 q=0.8 gain=-2dB", "peak cutoff=1600 q=0.7 gain=-3dB", "highshelf cutoff=7000 gain=1.5dB"]},
                          {"type": "compressor", "threshold": "-18dB", "ratio": 2.5, "attack": "12ms", "release": "140ms", "makeup": "0dB"}]},
        "buses": {
            "room": {"fx": ["reverb kind=room decay=1.1s mix=1 predelay=10ms", "hp cutoff=250"]},
            "spring": {"fx": ["reverb kind=spring decay=2.2s mix=1", "hp cutoff=300"]},
        },
        "tracks": [
            {"name": "carrier", "patch": "carrier", "gain": "-22dB",
             "fx": [{"type": "radio", "tune": {"value": 0, "mod": [{"src": "auto.dial", "amount": 1}]}, "hiss": "-36dB", "whistle": "-28dB",
                     "fade": 0.3, "drift": 0.05, "mix": 1}], "auto": {"dial": dial}, "score": T["carrier"]},
            {"name": "conga", "patch": "congas", "gain": "-8dB", "pan": -0.25, "sends": {"room": "-12dB"}, "score": T["conga"]},
            {"name": "gtr", "patch": "cutting-guitar", "gain": "-9dB", "pan": 0.3,
             "fx": [{"type": "phaser", "rate": 0.4, "depth": 0.6, "feedback": 0.4, "stages": 6, "mix": 0.35},
                    {"type": "amp", "gain": 0.25, "mix": 0.5}, {"type": "cab", "mix": 0.6}],
             "sends": {"spring": "-14dB"}, "score": T["gtr"]},
            {"name": "sub", "patch": "808", "gain": "-10dB", "fx": [pump, {"type": "filter", "kind": "lp", "cutoff": 160, "q": 0.7}], "score": T["sub"]},
            {"name": "acid", "patch": "acid", "gain": "-10dB", "pan": -0.1,
             "fx": [pump, *([{"type": "filter", "kind": "ladder", "q": 0.45, "cutoff": {"value": 600, "mod": [{"src": "var.storm", "amount": 1}]}}] if STORM else [])],
             "score": T["acid"]},
            {"name": "kick", "patch": "909", "gain": "-3dB", "score": T["kick"]},
            {"name": "hats", "patch": "909", "gain": "-10dB", "pan": 0.15, "score": "swing16=0.58 " + T["hats"]},
            {"name": "clap", "patch": "909", "gain": "-9dB", "sends": {"room": "-8dB"}, "score": T["clap"]},
            {"name": "fretless", "patch": "fretless", "gain": "-8dB", "fx": [{"type": "tremolo", "rate": 3.0, "depth": 0.4}], "sends": {"spring": "-10dB"}, "score": T["fretless"]},
            {"name": "horns", "patch": "horn-section", "gain": "-9dB", "pan": -0.2, "sends": {"room": "-8dB"}, "score": T["horns"]},
            *([voice("chirpers8-t5-bargain.json", "bargain", BARG, f"{VOX}dB",
                          [{"type": "radio", "tune": 0.04, "hiss": "-40dB", "whistle": "-32dB", "fade": 0.3, "drift": 0.03,
                            "mix": {"value": 0, "mod": [{"src": "auto.rmix", "amount": 0.85}]}}, "hp cutoff=250"],
                          {"spring": "-12dB"})] if VOX else []),
            *([voice("chirpers8-t5-keep.json", "keep", [st["C"] + 16 * BAR] + ([] if MOD else [st["C"] + 40 * BAR]), f"{float(VOX) + 2:g}dB",
                     [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150"], {"room": "-10dB", "spring": "-16dB"})] if VOX else []),
            *([lifted(voice("chirpers8-t5-keep.json", "keep2", [st["C"] + 40 * BAR], f"{float(VOX) + 2:g}dB",
                            [{"type": "chorus", "rate": 0.3, "depth": 0.2, "mix": 0.2}, "hp cutoff=150"], {"room": "-10dB", "spring": "-16dB"}))] if VOX and MOD else []),
            *([markov_lead("lead-m1", st["C"] + 16 * BAR, 0, 30), markov_lead("lead-m2", st["C"] + 24 * BAR, 2, 56)] if MARK else []),
            {"name": "lead", "patch": "lead-wah", "gain": "-12dB", "pan": 0.1, "fx": [{"type": "chorus", "rate": 0.5, "depth": 0.4, "mix": 0.3}],
             "score": "swing16=0.58 " + T["lead"]},
        ],
    }


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "vars", "tempo", "ceiling", "loudness", "seed", "tail", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
