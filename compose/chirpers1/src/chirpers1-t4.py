#!/usr/bin/env python3
"""chirpers1-t4 "Splinterwork" (Chirpers, Ferrous Bloom, track 4: the onslaught). Composed by chirper-two.

Identity: 204 BPM, dead straight, the album's fastest and most violent track. Its harmony is the MINOR-THIRD AXIS:
roots F -> Ab -> B -> D (the diminished axis; Moult's wheel turned by major thirds, this one by minor thirds), and
its stabs are LATTICE's colour (t1) stacked into one cluster on each root: root, b9, #11, maj7 (F1 Gb2 B2 E3).
Its riff is SPLINTER, an 11-sixteenth cell of three stabs and a tremolo burst (3+3+5) that realigns with the bar
every 11 bars. The form is built from abrupt stops: silences cut the riffs, and in the end the riff sheds itself
slot by slot (Collapse) until a dead stop hands over to t5's ringing chord.

Joins: it opens on the downbeat Moult's closing roll lands on (Moult's NINEFOLD, frenzied: Ignition); it ends on a
choked cluster and silence, into t5 "Five Breaths" (which opens on a ringing F1-C2-F2-B2 chord and a crash).

Emits songs/chirpers1-t4.yaml. Edit the music here, not the YAML.
"""
import json
import os

OUT = os.environ.get("SPLINTER_OUT") or os.path.expanduser("~/.config/chirp/songs/chirpers1-t4.yaml")
# Round 2 (kept as v2): J, Moult's tom roll keeps rolling as Ignition's backbeat for two bars under the ride (the
# join from Moult 9.9 -> 8.0 dB; with Moult v3's swell 6.5). K (a warmer master tilt toward the album mean) was
# tested and not taken: cohesion 60 -> 95 but structure and variety fell, total -0.14/-0.13, and it is convergence.
# SPLINTER_R2=none for v1.
R2 = set(filter(None, os.environ.get("SPLINTER_R2", "J").split(","))) - {"none"}
# Round 3 (kept as v3): M, Maw without cymbals (kick, snare and the crush only); L, SHARDS on the lead over Splinter's
# third cycle; E, the choked last hit is t5's opening chord. Tested, not kept (off): S, dead stops in Stop-start
# (choked crashes, shorter hits): the gaps go silent, but compscore's rhythm term falls 100 -> 45 because its
# off-grid peaks came from those ringing crashes, not from SPLINTER (at 204 BPM the 0.04*lag tolerance swallows
# odd-sixteenth lags past ~0.9 s); H, a china/kick accent on every cell's first stab: no change (-0.14/-0.17).
# SPLINTER_R3=none for v2.
R3 = set(filter(None, os.environ.get("SPLINTER_R3", "M,L,E").split(","))) - {"none"}
# Round 4 (sound playground, kept as v4 on judgment): A = the AXIS TOMS, stick-hard physical membrane toms (chirp
# `type: drum`, bd-7d117e) whose air-spring split is a minor third, so each tom sounds two neighbouring axis notes;
# T = their parts: they mark the Swarm's pairs (and run down to the next pair), double the Stop-start hits and two
# of the final hits. Tried and not kept (off): K = a stick-hard physical kick and snare too (seeds 0/11 89.8 -> 91.3
# over five voicings vs 92.96, and the kick carries the 11/9 cells: their polymeter salience fell 90 -> 17-31 however
# tight the kick); S = a tom on every cell's third stab (polymeter 27: it masks the 11-cycle).
R4 = set(filter(None, os.environ.get("SPLINTER_R4", "A,T").split(","))) - {"none"}
AXIS_TOM = {29: "ft", 32: "t3", 35: "t2", 38: "t1"}
# Round 5 (sound trade): H = Ingot's SHARD rig (chirper-three: the m8 chain bit-crushed and centred, HINGE's hocket
# partner) borrowed and turned: in Splinter II every other stab jumps from the wide pair to a harsher shard
# (5 bits, 4 kHz), a minor third UP, so the hocket also turns the axis. SPLINTER_R5=H to try it.
R5 = set(filter(None, os.environ.get("SPLINTER_R5", "H").split(","))) - {"none"}  # kept as v5  # root -> its tom (batter F2/Ab2/B2/D3)


def axis_kit():
    """obzen-kit-dry's cymbals and hats; kick, snare and toms on the physical drum layer, hit hard with sticks.
    Matched tom heads at cavity 0.2 raise the in-phase pair by sqrt(1.4) = 1.183, a minor third: the toms sound
    F2+Ab2, Ab2+B2, B2+D3, D3+F3 (the MINOR-THIRD AXIS in pairs). The kick: a short plastic contact with a
    heavy slap (the click), batter F1 over a slightly higher resonant head; the snare: hard stick, tight bright
    wires, a ringing shell."""

    def piece(pitch, layer, filters, amp, drive, vs, gain="0dB"):
        return {"pitch": pitch, "gain": gain, "patch": {"synth": {"layers": [dict(type="drum", **layer)],
                "filters": filters, "amp": amp, "drive": drive}, "play": {"vel_sens": vs}}}
    tom = dict(beater="stick", contact=0.6, decay="0.4s", sharp=70, reso=1.0, cavity=0.2, reso_level=0.55, air=0.5,
               strike=0.35, shell=0.35, damp=0.35, slap=float(os.environ.get("AXIS_TOM_SLAP", "0.8")))
    tamp = {"a": "0.1ms", "d": "0.6s", "s": 0, "r": "40ms", "curve": 4}
    return {"axis-kit": {
        "about": "Splinterwork's axis kit (chirper-two): obzen-kit-dry with stick-hard physical membrane toms whose "
                 "cavity split is a minor third, so they sound the MINOR-THIRD AXIS in pairs (F2+Ab2, Ab2+B2, "
                 "B2+D3, D3+F3).",
        "extends": "obzen-kit-dry",
        "kit": dict(({
            "k": piece("A1", dict(beater="plastic", contact=0.7, decay="0.12s", sharp=70, reso=1.1, cavity=0.15,
                                  reso_level=0.5, air=0.5, strike=0.35, damp=1.0, shell=0.35, shell_hz=260,
                                  shell_decay="0.06s", slap=0.8),
                       ["hp cutoff=32", "peak cutoff=4k q=1 gain=2dB"],
                       {"a": "0.1ms", "d": "200ms", "s": 0, "r": "15ms", "curve": 5}, 0.3, 0.4, gain="7dB"),
            "s": piece("F#3", dict(beater="stick", contact=0.6, decay="0.28s", sharp=35, reso=1.5, cavity=0.3,
                                   reso_level=0.5, wires=0.55, gap=0.15, wire_tone="5.5k", shell=0.5, shell_hz=560,
                                   damp=0.35, strike=0.25, slap=0.8),
                       ["hp cutoff=140", "peak cutoff=5k q=0.8 gain=2dB"],
                       {"a": "0.1ms", "d": "320ms", "s": 0, "r": "25ms"}, 0.25, 0.6, gain="-6.5dB"),
        } if "K" in R4 else {}), **{
            "ft": piece("F2", tom, ["hp cutoff=45"], tamp, 0.15, 0.5, gain="1.5dB"),
            "t3": piece("G#2", tom, ["hp cutoff=50"], tamp, 0.15, 0.5, gain="1.5dB"),
            "t2": piece("B2", tom, ["hp cutoff=55"], tamp, 0.15, 0.5, gain="1.5dB"),
            "t1": piece("D3", tom, ["hp cutoff=60"], tamp, 0.15, 0.5, gain="1.5dB")})}}
BPM = 204
STEP = 0.25
BAR = 16
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
F1, AB1, B1, D2 = 29, 32, 35, 38  # the minor-third axis on the 8-string (low F1 open)
AXIS = (F1, AB1, B1, D2)


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


STOPS = []  # (start, end) steps of silence: every part is cut there (the abrupt stops)


def silent(s):
    return any(a <= s < b for a, b in STOPS)


class Part:
    def __init__(self, name):
        self.name, self.ev = name, []

    def add(self, step, length, head, vel, mark=""):
        self.ev.append((step, length, head, vel, mark))

    def score(self, total):
        merged = {}
        for e in sorted(self.ev, key=lambda e: (e[0], -e[3])):
            if not silent(e[0]):
                merged.setdefault(e[0], e)
        ev = sorted(merged.values())
        toks, pos = [], 0
        for i, (s, ln, head, vel, mark) in enumerate(ev):
            nxt = ev[i + 1][0] if i + 1 < len(ev) else total
            cut = min([a for a, b in STOPS if a > s] + [total])
            ln = max(1, min(ln, nxt - s, cut - s))
            if s > pos:
                toks.append(f"R/{(s - pos) * STEP:g}b")
            toks.append(f"{head}/{ln * STEP:g}b@{min(127, vel)}" + (f"^{mark}" if mark else ""))
            pos = s + ln
        if total > pos:
            toks.append(f"R/{(total - pos) * STEP:g}b")
        return " ".join(toks)


def cluster(r):
    """LATTICE's colour as one stab: root, b9, #11 (tritone + octave), maj7 (two octaves - 1)."""
    return [r, r + 13, r + 18, r + 23]


def ch(notes):
    return ",".join(nm(n) for n in notes)


# SPLINTER: C cluster stab, T palm-muted tremolo sixteenth, . rest. 11 sixteenths: 3 + 3 + 5.
SPLINTER = {
    "plain": "C..C..CTTT.",
    "fill": "C..C..CTTTT",
    "dense": "C.TC.TCTTT.",
    "stab": "C..C..C.C.C",
}
# NINEFOLD from t3 "Moult" (X chug, x ghost, S stab), here at 204 with the stab as the cluster.
NINEFOLD = "X.XX.x.S."


def build():
    P = {k: Part(k) for k in ("gl", "gr", "bass", "drums", "lead", "pad", "shard")}
    gl, gr, bass, lead = P["gl"], P["gr"], P["bass"], P["lead"]
    kit = {}

    def hit(step, piece, vel):
        kit.setdefault(step, {})[piece] = max(vel, kit.get(step, {}).get(piece, 0))

    def both(step, ln, head, vel, mark=""):
        gl.add(step, ln, head, vel, mark)
        gr.add(step, ln, head, vel, mark)

    def splinter(start, bars, root_at, kind_at, kick=True, shift=0, keep=None, acc=112):
        """SPLINTER from `start` (+shift sixteenths) for `bars` bars; keep(k) -> slots of cell k that sound."""
        end, k, s = start + bars * BAR, 0, start + shift
        while s < end:
            pat, r = SPLINTER[kind_at(k)], root_at(s)
            n = keep(k) if keep else len(pat)
            for i, c in enumerate(pat[:n]):
                t = s + i
                if t >= end or c == ".":
                    continue
                if c == "C":
                    head = "H" in R3 and i == 0  # H: each cell's first stab is its accent (china, kick, harder)
                    both(t, 2, ch(cluster(r)), acc + (8 if head else 0))
                    bass.add(t, 2, nm(r), acc)
                    if kick or head:
                        hit(t, "k", 127 if head else 120)
                    if head:
                        hit(t, "x", 116)
                elif c == "T":
                    both(t, 1, nm(r), acc - 18 + 6 * (i % 2), "pm")
                    bass.add(t, 1, nm(r), 98)
                    if kick:
                        hit(t, "k", 100)
            k, s = k + 1, s + len(pat)
        return k

    # drum grammars, one bar each
    def blast(s0, cym="rd"):
        for i in range(BAR):
            hit(s0 + i, "k" if i % 2 == 0 else "s", 104 if i % 2 == 0 else 100)
        for i in range(0, BAR, 4):
            hit(s0 + i, cym, 92)

    def hammer(s0, cym="x"):
        for i in range(0, BAR, 2):
            hit(s0 + i, "k", 110)
            hit(s0 + i, "s", 108)
            hit(s0 + i, cym, 74 if i % 4 else 92)

    def backbeat(s0, cym="x", dkick=False):
        for i in range(0, BAR, 4):
            hit(s0 + i, cym, 90)
        hit(s0 + 4, "s", 116)
        hit(s0 + 12, "s", 116)
        if dkick:
            for i in range(BAR):
                hit(s0 + i, "k", 96)

    def halftime(s0, cym="x"):
        for i in range(0, BAR, 4 if cym else BAR):
            if cym:
                hit(s0 + i, cym, 88)
        hit(s0 + 8, "s", 120)

    def fill(s0, n=8, pieces=("s", "t1", "t2", "t3", "ft")):
        for i in range(n):
            hit(s0 + BAR - n + i, pieces[min(len(pieces) - 1, i * len(pieces) // n)], 96 + 3 * i)

    sec, t = {}, 0

    # 1. IGNITION (12 bars): Moult's roll lands here. NINEFOLD at 204, the stab now LATTICE's cluster, kick in
    # unison, china on the quarter; blasts for the last 4 bars; the last beat is cut dead.
    # The landing: Moult's roll arrives on one ringing bar (the cluster, the octave, a crash) under Moult's own
    # final pad (F3 A3 C#4 F4), which carries across for three bars before the frenzy has it.
    sec["ignition"] = (t, 12)
    both(t, BAR - 1, ch(cluster(F1) + [F1 + 12]), 122)
    bass.add(t, BAR - 1, nm(F1), 122)
    hit(t, "k", 126)
    P["pad"].add(t, 3 * BAR, ch((53, 57, 61, 65)), 84)
    s = t + BAR
    while s < t + 12 * BAR:
        for i, c in enumerate(NINEFOLD):
            st = s + i
            if st >= t + 12 * BAR or c == ".":
                continue
            if c == "X":
                both(st, 1, nm(F1), 116, "pm")
                bass.add(st, 1, nm(F1), 110)
                hit(st, "k", 118)
            elif c == "x":
                both(st, 1, nm(F1), 70, "pm")
            else:
                both(st, 2, ch(cluster(F1)), 112)
                bass.add(st, 2, nm(F1), 110)
        s += 9
    for b in range(1, 12):
        if "J" in R2 and b < 3:  # round 2: Moult's tom roll keeps rolling as the backbeat for two bars, under the ride
            for i in range(0, BAR, 4):
                hit(t + b * BAR + i, "rd", 90)
            for o, p_ in ((4, "t3"), (10, "t3"), (12, "ft"), (14, "ft")):
                hit(t + b * BAR + o, p_, 112)
            continue
        (backbeat if b < 8 else blast)(t + b * BAR, "x")
    hit(t, "c", 124)
    hit(t + 8 * BAR, "c", 120)
    STOPS.append((t + 12 * BAR - 4, t + 12 * BAR))
    t += 12 * BAR

    # 2. SPLINTER (33 bars = three realignments): F plain over a backbeat with the kick in unison; Ab with the
    # tremolo filled in, over blasts; B dense, over the hammer. A crash at every realignment.
    sec["splinter"] = (t, 33)
    for c, (root, kind, drum) in enumerate(((F1, "plain", "back"), (AB1, "fill", "blast"), (B1, "dense", "hammer"))):
        s0 = t + c * 11 * BAR
        splinter(s0, 11, lambda st, r=root: r, lambda k, kd=kind: kd, kick=(drum == "back"))
        if "L" in R3 and c == 2:  # round 3, L: SHARDS on the lead over the third cycle: the cluster's b9, #11 and
            # maj7 rise one per stab, then fall to the root during the tremolo burst (C5 F5 A#5 | B4 on B)
            for k in range(0, 11 * BAR // 11):
                cs = s0 + k * 11
                if cs >= s0 + 11 * BAR:
                    break
                for o, n, ln in ((0, 13, 2), (3, 18, 2), (6, 23, 1), (7, 0, 3)):
                    lead.add(cs + o, ln, nm(root + 24 + n + (12 if n == 0 else 0)), 104 if n else 96)
        for b in range(11):
            {"back": backbeat, "blast": blast, "hammer": hammer}[drum](s0 + b * BAR)
        hit(s0, "c", 124)
        if "S" in R4:  # every cell's third stab lands on the root's axis tom (tried: it masks the 11-cycle)
            for cs in range(s0, s0 + 11 * BAR, 11):
                if cs + 6 < s0 + 11 * BAR:
                    hit(cs + 6, AXIS_TOM[root], 112)
    STOPS.append((t + 33 * BAR - 8, t + 33 * BAR))
    t += 33 * BAR

    # 3. SWARM (22 bars): the two guitars tremolo a minor 2nd apart, hard left and right (the cluster split in
    # stereo), walking the octatonic pairs F/Gb Ab/A B/C D/Eb every two bars; double kick and backbeat, then blasts.
    # The lead stabs b9 shrieks in the second half.
    sec["swarm"] = (t, 22)
    for b in range(22):
        r = AXIS[(b // 2) % 4] + 12
        s0 = t + b * BAR
        for i in range(BAR):
            gl.add(s0 + i, 1, nm(r), 96 + 10 * (i % 4 == 0))
            gr.add(s0 + i, 1, nm(r + 1), 96 + 10 * (i % 4 == 0))
        for i in range(0, BAR, 2):
            bass.add(s0 + i, 2, nm(r - 12), 104)
        (lambda x: backbeat(x, "x", dkick=True))(s0) if b < 11 else blast(s0, "x")
        if b >= 11 and b % 2 == 0:
            for o, n in ((0, 0), (3, 13), (6, 18)):
                lead.add(s0 + o + (b % 4) * 2, 2, nm(r + 36 + n), 104)
        if b % 4 == 0:
            hit(s0, "c", 118)
        if "T" in R4:  # each octatonic pair opens on its axis tom; its second bar runs down to the next pair's
            tom_now, tom_next = AXIS_TOM[AXIS[(b // 2) % 4]], AXIS_TOM[AXIS[(b // 2 + 1) % 4]]
            if b % 2 == 0:
                hit(s0, tom_now, 116)
            else:
                for i, tt in enumerate((tom_now, tom_now, tom_next, tom_next)):
                    hit(s0 + 12 + i, tt, 100 + 4 * i)
    STOPS.append((t + 22 * BAR - 4, t + 22 * BAR))
    t += 22 * BAR

    # 4. STOP-START (20 bars): single cluster hits with silence between them, roots around the axis per four bars;
    # two hits in the third bar, a tremolo burst with a snare roll in the fourth; the last group accelerates
    # (quarters, eighths, a full tremolo bar) into two beats of nothing.
    sec["stopstart"] = (t, 20)
    for g in range(5):
        r = (F1, AB1, B1, D2, F1)[g]
        g0 = t + g * 4 * BAR
        if g < 4:
            for b, onsets in ((0, (0,)), (1, (0,)), (2, (0, 6))):
                for o in onsets:
                    hl = 2 if "S" in R3 else 3  # S: shorter hits, so the gaps go dead
                    both(g0 + b * BAR + o, hl, ch(cluster(r)), 118)
                    bass.add(g0 + b * BAR + o, hl, nm(r), 118)
                    hit(g0 + b * BAR + o, "k", 124)
                    if "T" in R4:  # the hit's root on its axis tom
                        hit(g0 + b * BAR + o, AXIS_TOM[r], 118)
                    hit(g0 + b * BAR + o, "cch" if "S" in R3 else ("c" if o == 0 else "x"), 118)
            s3 = g0 + 3 * BAR
            for i in range(8, BAR):
                both(s3 + i, 1, nm(r), 92 + 3 * (i - 8), "pm")
                bass.add(s3 + i, 1, nm(r), 100)
                hit(s3 + i, "s", 70 + 6 * (i - 8))
        else:
            for b, step in ((0, 4), (1, 2), (2, 1)):
                for o in range(0, BAR, step):
                    st = g0 + b * BAR + o
                    if step == 1:
                        both(st, 1, nm(r), 104, "pm")
                    else:
                        both(st, step, ch(cluster(r)), 116)
                    bass.add(st, step, nm(r), 108)
                    hit(st, "k", 116)
                    if o % 4 == 0:
                        hit(st, "x", 110)
                hit(g0 + b * BAR + 4, "s", 116)
                hit(g0 + b * BAR + 12, "s", 116)
            fill(g0 + 3 * BAR, 8)
            STOPS.append((g0 + 3 * BAR, g0 + 3 * BAR + 8))
    t += 20 * BAR

    # 5. MAW (16 bars): the one half-time crush. A ringing cluster, three chugs and a stab per bar, space between;
    # roots F then E (LATTICE's major 7th under the root); the lead wails LATTICE in retrograde, E5 B4 Gb4 F4.
    sec["maw"] = (t, 16)
    for b in range(16):
        r = F1 if b < 8 else F1 - 1 + 12  # E2: the 8-string's open F1 cannot go lower, so the E sits an octave up
        s0 = t + b * BAR
        both(s0, 6, ch(cluster(r)), 116)
        bass.add(s0, 6, nm(r if r < 36 else r - 12), 116)
        hit(s0, "k", 120)
        for o in (8, 9, 11):
            both(s0 + o, 1, nm(r), 104, "pm")
            bass.add(s0 + o, 1, nm(r if r < 36 else r - 12), 104)
            hit(s0 + o, "k", 108)
        both(s0 + 12, 4, ch(cluster(r)[:3]), 110)
        halftime(s0, None if "M" in R3 else ("x" if b % 2 else "c"))  # M: Maw without cymbals
    for i, n in enumerate((76, 71, 66, 65)):  # E5 B4 Gb4 F4, four bars each
        lead.add(t + i * 4 * BAR, 4 * BAR - 2, nm(n), 100)
    fill(t + 15 * BAR, 12)
    t += 16 * BAR

    # 6. SPLINTER II (22 bars): SPLINTER returns a sixteenth late (displaced) and as pure stabs, on D then F (the
    # axis's far side, then home), over the hammer; the lead doubles every stab's b9 two octaves up.
    sec["splinter2"] = (t, 22)
    s0 = t
    splinter(t, 22, lambda st: D2 if st < s0 + 11 * BAR else F1, lambda k: "stab" if k % 3 != 2 else "dense",
             kick=False, shift=1, acc=118)
    for e in [e for e in gl.ev if s0 <= e[0] < s0 + 22 * BAR and len(e[2].split(",")) == 4]:
        root = D2 if e[0] < s0 + 11 * BAR else F1
        lead.add(e[0], 2, nm(root + 13 + 36), 96)
    if "H" in R5:  # the SHARD hocket: alternate stabs leave the pair for the centred shard, a minor third up
        stabs = sorted(e for e in gl.ev if s0 <= e[0] < s0 + 22 * BAR and len(e[2].split(",")) == 4)
        moved = {e[0] for k, e in enumerate(stabs) if k % 2 == 1}
        for st, ln, head, vel, mark in stabs:
            if st in moved:
                root = D2 if st < s0 + 11 * BAR else F1
                P["shard"].add(st, ln, ch(cluster(root + 3)), vel, mark)
        for g in (gl, gr):
            g.ev = [e for e in g.ev if not (e[0] in moved and len(e[2].split(",")) == 4)]
    for b in range(22):
        hammer(t + b * BAR, "x" if b % 2 else "rd")
        if b % 11 == 0:
            hit(t + b * BAR, "c", 124)
    STOPS.append((t + 22 * BAR - 4, t + 22 * BAR))
    t += 22 * BAR

    # 7. FRACTURE (22 bars): the album's cycles collide: guitars in SPLINTER's 11, bass and kick in Moult's 9,
    # china and backbeat in 4/4. Roots climb the axis every four bars (F Ab B D, then F for the last six).
    sec["fracture"] = (t, 22)
    s0 = t
    fr = lambda st: (F1, AB1, B1, D2, F1, F1)[min((st - s0) // (4 * BAR), 5)]  # noqa: E731
    splinter(t, 22, fr, lambda k: ("plain", "fill", "dense")[k % 3], kick=False, acc=116)
    s = t
    while s < t + 22 * BAR:
        for i, c in enumerate(NINEFOLD):
            st = s + i
            if st < t + 22 * BAR and c in "XS":
                bass.add(st, 2 if c == "S" else 1, nm(fr(st)), 116 if i == 0 else 104)
                hit(st, "k", 124 if i == 0 else 104)
        s += 9
    for b in range(22):
        backbeat(t + b * BAR, "x" if b < 16 else "c")
        lead.add(t + b * BAR, BAR - 1, nm(fr(t + b * BAR) + 48 + (0, 1, 6, 11)[b % 4]), 88)
    t += 22 * BAR

    # 8. COLLAPSE (14 bars): four bars of full SPLINTER over blasts, then the cell sheds a slot every repeat
    # (11 sounding slots, 10, 9 ... 1) with silence in the gaps, the blast going with it; then three tutti
    # cluster hits and a dead, choked stop into t5's ringing chord.
    sec["collapse"] = (t, 13)
    s0 = t
    ncells = splinter(t, 4, lambda st: F1, lambda k: "fill", kick=False)
    for b in range(4):
        blast(t + b * BAR, "x")
    s = t + ncells * 11
    for k, n in enumerate(range(11, 0, -1)):
        pat = SPLINTER["fill"][:n]
        for i, c in enumerate(pat):
            st = s + i
            if c == "C":
                both(st, 2, ch(cluster(F1)), 116)
                bass.add(st, 2, nm(F1), 116)
                hit(st, "k", 120)
                hit(st, "x", 112)
            elif c == "T":
                both(st, 1, nm(F1), 100, "pm")
                bass.add(st, 1, nm(F1), 100)
                hit(st, "k", 100)
                hit(st, "s", 92)
        s += 11
    end_hits = t + 14 * BAR - 2 * BAR
    s = max(s, end_hits - 4)
    for j, o in enumerate((0, 4, 8)):
        st = end_hits + o
        last = ch((F1, F1 + 7, F1 + 12, F1 + 18)) if ("E" in R3 and j == 2) else ch(cluster(F1) + [F1 + 12])
        both(st, 3 if j < 2 else 6, last, 124)  # E: the choked last hit IS t5's opening chord (F1 C2 F2 B2),
        # cut dead here and let ring there
        bass.add(st, 3 if j < 2 else 6, nm(F1), 124)
        hit(st, "k", 127)
        hit(st, "s", 124)
        if "T" in R4 and j < 2:
            hit(st, "ft", 120)
        hit(st, "cch" if j == 2 else "c", 124)
    STOPS.append((end_hits + 14, end_hits + 20))
    t = end_hits + 20  # 6 sixteenths (0.44 s) of dead air after the choke, then t5

    for s in sorted(kit):
        pieces = kit[s]
        P["drums"].add(s, 1, ",".join(sorted(pieces)), max(pieces.values()))
    return t, sec, P


def main():
    total, sec, P = build()
    # Mix: in v-a the kit owned >90% of everything above 3 kHz and 70% below 250 Hz, the guitars 9% of 80-250 Hz:
    # the kit down and darker, the guitars keep their low mids (no box cut here) with a little more body.
    geq = {"type": "eq", "bands": ["lowshelf cutoff=180 gain=3dB", "peak cutoff=420 q=0.8 gain=-1dB", "highshelf cutoff=3000 gain=2dB"]}
    beq = {"type": "eq", "bands": ["lowshelf cutoff=55 gain=-6dB", "peak cutoff=110 q=0.8 gain=6dB"]}
    tracks = [
        {"name": "gtr-l", "patch": "m8-emg-l", "pan": -1, "gain": "0dB", "fx": [geq], "score": P["gl"].score(total)},
        {"name": "gtr-r", "patch": "m8-emg-r", "pan": 1, "gain": "0dB", "fx": [geq], "score": P["gr"].score(total)},
        {"name": "bass", "patch": "m8-bass", "gain": "0dB", "fx": [beq], "score": P["bass"].score(total)},
        {"name": "drums", "patch": "axis-kit" if "A" in R4 else "obzen-kit-dry", "out": "kit", "gain": "-8dB",
         "score": P["drums"].score(total)},
        {"name": "lead", "patch": "m8-lead", "gain": "-6dB", "pan": 0.1,
         "fx": [{"type": "delay", "time": f"{60000 / BPM * 0.75:.1f}ms", "feedback": 0.25, "mix": 0.18},
                "reverb kind=plate decay=1.4s mix=0.15"], "score": P["lead"].score(total)},
        {"name": "pad", "patch": "juno-pad", "gain": "-14dB", "score": P["pad"].score(total)},
    ] + ([{"name": "shard", "patch": "m8-emg-r", "pan": 0, "gain": "-6dB", "seed": 19,
           "fx": [{"type": "crush", "bits": 5, "rate": 4000, "mix": 0.6}], "score": P["shard"].score(total)}]
         if "H" in R5 else [])
    secs = "; ".join(f"{k} {v[0] // BAR + 1}-{v[0] // BAR + v[1]}" for k, v in sec.items())
    about = ("Chirpers - Splinterwork (Ferrous Bloom, track 4: the onslaught). Original composition by chirper-two, "
             "generated by compose/chirpers1/src/chirpers1-t4.py. 204 BPM straight; SPLINTER, an 11-sixteenth cell "
             "of LATTICE-cluster stabs (root b9 #11 maj7) and tremolo; the MINOR-THIRD AXIS F-Ab-B-D; abrupt stops; "
             f"opens on Moult's NINEFOLD at speed, collapses into a dead stop. Bars: {secs}.")
    lines = [
        f"about: {json.dumps(about)}",
        "meta: " + json.dumps({"artist": "Chirpers", "album": "Ferrous Bloom", "title": "Splinterwork", "track": 4, "year": 2026}),
        f"tempo: {BPM}",
        f'length: "{total * STEP:g}b"',
        'ceiling: "-0.1dB"',
        'volume: "2dB"',
        "buses: " + json.dumps({"kit": {"fx": ["rack:drum-bus-punch", {"type": "eq", "bands": ["highshelf cutoff=6000 gain=-6dB"]}]}}),
    ] + (["patches: " + json.dumps(axis_kit())] if "A" in R4 else []) + [
        "master: " + json.dumps({"fx": [
            {"type": "eq", "bands": ["lowshelf cutoff=40 gain=-3dB", "peak cutoff=100 q=1 gain=2dB"] +
             (["peak cutoff=350 q=0.7 gain=2dB", "highshelf cutoff=3000 gain=-2dB"] if "K" in R2 else
              ["peak cutoff=500 q=0.7 gain=-1dB"]) + ["highshelf cutoff=10000 gain=-4dB"]},
            "glue threshold=-20dB ratio=2.5 attack=10ms release=120ms makeup=2dB",
            "clip drive=5dB ceiling=-0.5dB"]}),
        "tracks:",
    ]
    lines += ["  - " + json.dumps(t) for t in tracks]
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {total // BAR} bars, {total * STEP / BPM * 60:.1f} s; {secs}")


if __name__ == "__main__":
    main()
