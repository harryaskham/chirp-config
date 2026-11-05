#!/usr/bin/env python3
"""chirpers - Accretion (chirpers IX), track 8 (chirper-three): JET AND HORIZON. The release.

t7's storm falls in at 150 bpm. E4's lights catch it. Then THE STRETTO: every element enters in turn on its own
cycle - E1 (5 beats), E2 (seven sixteenths), E3 (2+2+3), E5 (3 beats) - each started at the phase that lands it on
ONE downbeat, bar 97 (beat 384). Before it they rub: E2's F, E3's Eb and E5's G# against the D pedal, out of phase,
in a minor haze. AT THE JET every cycle lands together, the material turns major (F -> F#, Eb -> E), the band locks
into 4/4, and the voice - a CHOIR this time, a bright lead with a fifth above and an octave below - sings full
lines, the first of them carrying E8 at last: E1 augmented, then E F# D, landed once, on 'light'. Then THE HORIZON:
the tempo slows (150 -> 90) while a held D, sung and on a pad, sinks in pitch and closes - the light redshifting away.

E6 (provisional) and E7 (not yet posted) join the stretto when their owners post them in motifs.md.
Writes songs/chirpers9-t8.yaml (or T8_OUT). Original music.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.environ.get("T8_OUT", os.path.join(ROOT, "songs", "chirpers9-t8.yaml"))
TAKES = json.load(open(os.path.join(HERE, "chirpers9-t8-takes.json")))["takes"]

BARS, BPB = 176, 4
TOTAL = BARS * BPB
SEAM_IN = 150                 # mixplan: t7>t8 150, flat across the 16-bar overlap
SECTIONS = [("lens", 1, 16), ("stretto", 17, 96), ("jet", 97, 140), ("horizon", 141, 176)]
JET = 97
JB = (JET - 1) * BPB          # beat 384: every cycle lands here
HORIZON = 141
BREAK = (121, 128)            # the breakdown inside the jet: the lens returns (lights and choir), then the jet again


def in_break(bar):
    return BREAK[0] <= bar <= BREAK[1]


def b0(bar):
    return (bar - 1) * BPB


def sec_of(bar):
    for name, a, z in SECTIONS:
        if a <= bar <= z:
            return name
    return SECTIONS[-1][0]


NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(name):
    n, rest = name[0], name[1:]
    acc = 0
    while rest and rest[0] in "#b":
        acc += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + NOTE[n] + acc


def name_of(m):
    return f"m{m}"


MAJOR = {5: 6, 3: 4}          # after the jet: F -> F#, Eb -> E (pitch classes)


def brighten(m):
    pc = m % 12
    return m + (MAJOR[pc] - pc) if pc in MAJOR else m


class Part:
    def __init__(self):
        self.ev = []

    def add(self, at, ln, head, vel):
        self.ev.append((round(at, 4), ln, head, int(max(1, min(127, vel)))))

    def score(self, total=TOTAL):
        ev = sorted(self.ev, key=lambda e: (e[0], -e[3]))
        toks, pos = [], 0.0
        for i, (s, ln, head, vel) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            ln = min(ln, nxt - s)
            if ln <= 1e-6:
                continue
            if s - pos > 1e-5:
                toks.append(f"R/{s - pos:.5g}b")
            toks.append(f"{head}/{ln:.5g}b@{vel}")
            pos = s + ln
        if total - pos > 1e-5:
            toks.append(f"R/{total - pos:.5g}b")
        return " ".join(toks) if toks else f"R/{total:g}b"


P = {}


def part(n):
    return P.setdefault(n, Part())


# ---------------------------------------------------------------- the elements (motifs.md)
E1 = [("D4", 0.0, 0.5), ("A4", 0.5, 0.75), ("C5", 1.25, 0.25), ("G4", 1.5, 1.0), ("E4", 2.5, 1.0)]     # 5 beats
E2 = [("D4", 0, 112), ("A4", 2, 84), ("F4", 3, 98), ("C4", 5, 76)]                                       # 7 sixteenths
E3 = [(("D3", "A3", "E4", "F4"), 2.0), (("Eb3", "Bb3", "D4", "G4", "A4"), 2.0), (("C3", "Bb3", "D4", "F4"), 3.0)]
E4 = [("D2", "A2", "F#3", "C4", "E4"), ("Bb1", "F2", "D3", "A3", "C4", "E4"), ("A1", "E2", "C3", "G3", "B3", "D4"),
      ("D2", "A2", "C3", "G3", "B3", "E4")]
E5 = [("A4", 0), ("G#4", 1), ("A4", 2), ("E5", 4), ("A4", 6), ("G#4", 7), ("A4", 8), ("D5", 10)]          # 3 beats
CYCLE = {"E1": 5.0, "E2": 1.75, "E3": 7.0, "E4": 20.0, "E5": 3.0}
ENTRY = {"E4": 1, "E1": 17, "E2": 29, "E3": 41, "E5": 53}          # the stretto's entries (bars)


def phase_start(el, entry_bar):
    """The first cycle start at or after the entry bar that lands a cycle exactly on the jet's downbeat."""
    c = CYCLE[el]
    k = int((JB - b0(entry_bar)) // c)
    return JB - k * c


def chord(notes, bright=False):
    ms = [midi(n) for n in notes]
    if bright:
        ms = [brighten(m) for m in ms]
    return ",".join(name_of(m) for m in ms)


# ---------------------------------------------------------------- the stretto (before the jet)
def write_stretto():
    # E4: the lights catch the fall, phased from beat 4 so a turn lands on the jet
    beat = phase_start("E4", 1)
    k = 0
    while beat < JB - 0.01:
        bar = int(beat // BPB) + 1
        v = 48 + min(30, bar // 3)
        part("lights").add(beat, 5.0, chord(E4[k % 4]), v)
        beat += 5.0; k += 1
    # E1 on the chip pulse
    beat = phase_start("E1", ENTRY["E1"])
    while beat < JB - 0.01:
        bar = int(beat // BPB) + 1
        for n, on, ln in E1:
            part("e1").add(beat + on, ln, n, 66 + min(24, (bar - 17) // 3))
        beat += 5.0
    # E2: the seven-sixteenth cell, pitched, on a pluck
    beat = phase_start("E2", ENTRY["E2"])
    while beat < JB - 0.01:
        for n, step, v in E2:
            part("e2").add(beat + step * 0.25, 0.25, n, v - 20)
        beat += 1.75
    # E3: t3's progression on 2+2+3, a dark pad
    beat = phase_start("E3", ENTRY["E3"])
    while beat < JB - 0.01:
        on = 0.0
        for notes, ln in E3:
            part("e3").add(beat + on, ln, chord(notes), 54)
            on += ln
        beat += 7.0
    # E5: the inner orbit, marimba
    beat = phase_start("E5", ENTRY["E5"])
    while beat < JB - 0.01:
        for n, s in E5:
            part("e5").add(beat + s * 0.25, 0.25, n, 70 if s == 0 else 56)
        beat += 3.0
    # the D pedal everything shares (the triangle bass), in E2's rhythm, from 33
    beat = phase_start("E2", 33)
    while beat < JB - 0.01:
        for n, step, v in E2[:2]:
            part("bass").add(beat + step * 0.25, 0.25, "D2", v - 10)
        beat += 1.75
    # the drums gather: noise snare and hat on E5's 3 against the bar, from 65
    for bar in range(65, JET):
        part("kick").add(b0(bar), 0.5, "k", 90)
        for i in range(0, 16):
            if i % 3 == 0:
                part("hat").add(b0(bar) + i * 0.25, 0.25, "C7", 50 + (bar - 65))
    part("riser").add(b0(JET - 4), 16.0, "C4", 100)


# ---------------------------------------------------------------- the jet (locked 4/4, major)
def write_jet():
    part("impact").add(JB, 4.0, "C3", 120)
    for bar in range(JET, HORIZON):
        t = b0(bar)
        k = (bar - JET) % 4
        part("lights").add(t, 4.0, chord(E4[k], bright=True), 64 if in_break(bar) else 90)
        part("sub").add(t, 3.75, name_of(midi(E4[k][0]) - 12 if midi(E4[k][0]) >= 33 else midi(E4[k][0])), 70 if in_break(bar) else 92)
        if in_break(bar):
            continue                                       # the breakdown: lights, sub and the choir only
        part("bass").add(t, 1.5, name_of(midi(E4[k][0]) + 12), 104)
        part("bass").add(t + 2.5, 1.0, name_of(midi(E4[k][1]) + 12), 88)
        # E1 re-barred into the bar (x 0.8), bright, on the pulse lead - except where the choir sings
        for n, on, ln in E1:
            part("e1").add(t + on * 0.8, ln * 0.8, name_of(brighten(midi(n)) + 12), 62)
        # the groove: half time at 150 (75 felt)
        part("kick").add(t, 0.5, "k", 112)
        part("kick").add(t + 2.5, 0.5, "k", 92)
        part("snare").add(t + 2, 0.5, "s", 104)
        for e in range(8):
            part("hat").add(t + e * 0.5, 0.25, "C7" if e % 2 else "F6", 64 if e % 2 else 52)
        if bar % 8 == JET % 8:
            part("crash").add(t, 4.0, "cy", 96)
    # E5 continues across the lock in its own 3 (polymeter kept, now consonant)
    beat = JB
    while beat < b0(HORIZON) - 0.01:
        quiet = in_break(int(beat // BPB) + 1)
        for n, s in E5:
            part("e5").add(beat + s * 0.25, 0.25, name_of(brighten(midi(n)) + 12), (34 if quiet else 58) if s else (44 if quiet else 70))
        beat += 3.0
    # E2, brightened, on the pluck, the seven against everything
    beat = JB
    while beat < b0(HORIZON) - 0.01:
        if not in_break(int(beat // BPB) + 1):
            for n, step, v in E2:
                part("e2").add(beat + step * 0.25, 0.25, name_of(brighten(midi(n)) + 12), v - 24)
        beat += 1.75


def sung(at, take, transpose=0, vel_scale=1.0):
    out = []
    for n in take["notes"]:
        d = {"at": round(at + n["at"], 4), "len": n["len"], "ph": n["ph"],
             "pitch": f"m{int(float(n['pitch'][1:])) + transpose}", "vel": round(n["vel"] * vel_scale, 3)}
        if n.get("expr_path"):
            d["expr_path"] = n["expr_path"]
        out.append(d)
    return out


def choir():
    """Lines from the jet: (bar, take). E8 rides on take 0 - sung ONCE."""
    plan = [(JET, 0), (JET + 4, 1), (JET + 8, 2), (JET + 12, 3), (BREAK[0], 2), (BREAK[0] + 4, 3),
            (BREAK[1] + 1, 1), (BREAK[1] + 5, 2), (BREAK[1] + 9, 3)]
    lead, fifth, low = [], [], []
    for bar, k in plan:
        lead += sung(b0(bar), TAKES[k])
        fifth += sung(b0(bar), TAKES[k], transpose=7, vel_scale=0.7)
        low += sung(b0(bar), TAKES[k], transpose=-12, vel_scale=0.8)
    return lead, fifth, low


# ---------------------------------------------------------------- the horizon
def write_horizon():
    a, z = HORIZON, BARS
    part("hold").add(b0(a), b0(z + 1) - b0(a) - 2, "D3,A3,D4,F#4", 80)
    part("hsub").add(b0(a), b0(z + 1) - b0(a) - 2, "D1", 84)
    part("lights").add(b0(a), 16.0, chord(E4[0], bright=True), 70)


def horizon_lane(drop):
    """Redshift: 0 until the horizon, then sinking to `drop` semitones by the end."""
    return [["0b", 0.0], [f"{b0(HORIZON):g}b", 0.0], [f"{b0(BARS + 1):g}b", drop]]


VOICE8 = {"about": "t8's choir lead: bright and open - a smaller tract, more air, quick vibrato",
          "play": {"mono": True, "glide": "30ms"},
          "synth": {"layers": [{"type": "voice", "tract": 0.92, "breath": 0.18, "ph_soft": 0.2, "pulse_rate": 5}],
                    "pitch": {"value": 0, "mod": [{"src": "expr.f0", "amount": 0.01}, {"src": "auto.rs", "amount": 1}]},
                    "amp": {"a": "30ms", "d": "0s", "s": 1, "r": "300ms"}}}
SUB8 = {"about": "t8's sub: a sine under the lights' roots", "synth": {"layers": [{"wave": "sine"}],
        "amp": {"a": "15ms", "d": "0s", "s": 1, "r": "250ms"}}, "fx": ["drive drive=0.1"]}
HSUB = {"about": "t8's horizon sub: the held D's floor, sinking with it",
        "synth": {"layers": [{"wave": "sine"}], "pitch": {"value": 0, "mod": [{"src": "auto.rs", "amount": 1}]},
                  "amp": {"a": "3s", "d": "0s", "s": 1, "r": "6s"}}}
HOLD = {"about": "t8's horizon: a held light, its pitch sinking on a lane",
        "synth": {"layers": [{"wave": "saw", "level": "-6dB"}, {"wave": "saw", "cents": 7, "level": "-6dB"},
                             {"wave": "sine", "ratio": 0.5, "level": "-8dB"}],
                  "pitch": {"value": 0, "mod": [{"src": "auto.rs", "amount": 1}]},
                  "filters": [{"kind": "lp", "cutoff": {"value": 3000, "mod": [{"src": "auto.cl", "amount": -2600}]}}],
                  "amp": {"a": "3s", "d": "0s", "s": 1, "r": "6s"}}}


def main():
    write_stretto()
    write_jet()
    write_horizon()
    lead, fifth, low = choir()
    lead += [{"at": b0(HORIZON), "len": b0(BARS + 1) - b0(HORIZON) - 4, "pitch": "D4", "vel": 0.6}]   # the held 'ah'
    tempo = [{"at": "0b", "bpm": SEAM_IN}, {"at": f"{b0(HORIZON):g}b", "bpm": SEAM_IN},
             {"at": f"{b0(BARS + 1):g}b", "bpm": 90, "ramp": True}]
    cl = [["0b", 0.0], [f"{b0(HORIZON):g}b", 0.0], [f"{b0(BARS + 1):g}b", 1.0]]
    tr = lambda n, patch, **kw: dict({"name": n, "patch": patch, "score": part(n).score()}, **kw)
    song = {
        "about": "chirpers - Accretion (chirpers IX), track 8 by chirper-three: jet and horizon. Every element enters "
                 "in stretto on its own cycle and they all land on one downbeat; the choir sings the arrival (E F# D) "
                 "once; then a held light redshifts away.",
        "tempo": tempo,
        "loudness": -11,
        "volume": "0dB",
        "tail": "6s",
        "event_stable": True,
        "tracks": [
            tr("lights", "strings", gain="-12dB", sends={"hall": "-8dB"},
               fx=[{"type": "filter", "kind": "peak", "cutoff": 230, "q": 0.9, "gain": "-5dB"}]),
            tr("e1", "nes-pulse-lead", gain="-16dB", pan=-0.25, sends={"dly": "-12dB"}),
            tr("e2", "arp-pluck", gain="-17dB", pan=0.35, sends={"dly": "-14dB"}),
            tr("e3", "strings-synth", gain="-18dB", pan=-0.1, sends={"hall": "-8dB"}, fx=["lp cutoff=1800"]),
            tr("e5", "marimba", gain="-14dB", pan=0.2, sends={"room": "-10dB"}),
            tr("bass", "nes-triangle-bass", gain="-8dB"),
            tr("sub", SUB8, gain="-12dB"),
            tr("hsub", HSUB, gain="-13dB", auto={"rs": {"points": horizon_lane(-5.0)}}),
            tr("kick", "machine-kit", gain="-8dB"),
            tr("snare", "machine-kit", gain="-10dB", sends={"room": "-10dB"}),
            tr("hat", "nes-noise-hat", gain="-17dB", pan=0.25),
            tr("crash", "machine-kit", gain="-14dB", pan=-0.2),
            tr("riser", "fx-revcym", gain="-12dB"),
            tr("impact", "fx-impact", gain="-10dB"),
            {"name": "choir", "patch": VOICE8, "gain": "-7dB", "sends": {"hall": "-7dB", "dly": "-16dB"},
             "notes": lead, "auto": {"rs": {"points": horizon_lane(-5.0)}}},
            {"name": "choir5", "patch": VOICE8, "gain": "-15dB", "pan": 0.3, "sends": {"hall": "-6dB"}, "notes": fifth,
             "auto": {"rs": {"points": horizon_lane(-5.0)}}},
            {"name": "choir8", "patch": VOICE8, "gain": "-14dB", "pan": -0.3, "sends": {"hall": "-6dB"}, "notes": low,
             "auto": {"rs": {"points": horizon_lane(-5.0)}}},
            tr("hold", HOLD, gain="-14dB", sends={"hall": "-4dB"},
               auto={"rs": {"points": horizon_lane(-5.0)}, "cl": {"points": cl}}),
        ],
        "buses": {"room": {"fx": ["reverb kind=room decay=0.8s mix=1 predelay=6ms", "hp cutoff=200"]},
                  "hall": {"fx": ["reverb kind=hall decay=4s mix=1 predelay=24ms", "hp cutoff=180"]},
                  "dly": {"fx": ["delay time=3/8 mix=1 feedback=0.32", "hp cutoff=400", "lp cutoff=6000"]}},
        "master": {"fx": [{"type": "eq", "bands": ["highpass cutoff=28", "peak cutoff=240 q=0.8 gain=-2dB",
                                                   "highshelf cutoff=6000 gain=4dB"]},
                          {"type": "compressor", "threshold": "-14dB", "ratio": 3, "attack": "8ms",
                           "release": "120ms", "makeup": "0dB"}]},
    }
    with open(OUT, "w") as f:
        json.dump(song, f, indent=1)
    print(f"wrote {OUT} bars {BARS} jet {JET} (beat {JB}) choir notes {len(lead)}")


if __name__ == "__main__":
    main()
