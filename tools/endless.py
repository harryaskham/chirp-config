#!/usr/bin/env python3
"""tools/endless.py: DOES THE ENDLESS THING HOLD?  (chirper-zero's ask after False Summit v1, 15 Nov)

  python3 tools/endless.py SONG TRACK[,TRACK...] FROM-TO --cycle 1bar [--steps 16] [--seed 0] [--pin CHIRP] [--keep DIR] [--json]
  python3 tools/endless.py --wav FILE.wav --cycle 2.4s [--steps 16] [--json]

An illusion of endless motion (a Shepard scale, a Risset rhythm, a barber-pole sweep, a riser that never arrives)
is, measured, a thing that moves and is THE SAME ONE CYCLE LATER, with nothing starting again where the cycle wraps.
`tools/chirpers.py illusion` says whether the part LEADS its mix; this says whether the illusion HOLDS.

SONG is an id (songs/ID.yaml) or a file; the TRACKs are the illusion's parts, rendered alone (--solo) through their
own effects, bus and master with the groove's engine, from the top, so lanes, faders and tails are the song's.
FROM-TO are positions as `chirp render --from/--to` take them (bars from 1: 9-33 is bars 9 to 32). --cycle is the
illusion's period: 1bar, 4bars, 16b (beats) or 2.4s. With --wav: a render you already have, cut to the passage.
A cycle SHORTER THAN A BAR is asked in beats, with a slice a stroke: a fill falling a semitone a sixteenth comes round
every twelve, so `falls 71-73 --cycle 3b --steps 12` (False Summit v5: two cycles of 35 notes, the same; it holds).
--seed N renders the parts on another seed (0 is the groove's). A band's SPREAD that MOVES WITH THE SEED is the
players' own variation, not the song: four guitars on one patch, the same notes and the same fader lanes in every
cycle, still read 2.1 to 3.4 dB apart at 120-250 Hz, and a different cycle is the loud one on each seed (False
Summit v8, the stair's left side). A spread that stays on the same cycle on every seed is written in the song.

It prints
  ONE CYCLE LATER: each cycle's level, nine bands and centroid against the other cycles: the spread, and the
    centroid's drift in octaves a cycle (a part that really climbed an octave a cycle would read +1.00); whether
    the levels repeat over some LONGER cycle (four guitars taking turns make one of four); and, from the song,
    whether every cycle has the same notes at the same places (the parts together: which guitar plays which
    octave, or which copy of a rhythm, is not asked).
  INSIDE THE CYCLE, AND AT THE WRAP: the cycle in --steps slices, the mean over the cycles: each slice's level
    and centroid against the cycle's own, how far each RUNS through the cycle (a straight line through the
    slices) and what it does AT THE WRAP (the last slice to the next cycle's first). A SAW-TOOTH is a run undone
    at the wrap: a riser that starts again, which is what the illusion is there to hide.
The marks (SPREAD, DRIFT, A LONGER CYCLE, ANOTHER PATTERN, SAW-TOOTH) are questions for an ear before they are
faults: a part may change on purpose. What it cannot say: whether a listener hears it climb for ever (the bell's
width, the register and the ear decide that); whether the part is heard in the mix (chirpers.py illusion,
presence.py); and, for a RHYTHM, how fast it sounds: through a saturated rig the attacks cannot be counted from
the audio (tried: an onset measure followed the level, not the rate), so a Risset rhythm is read by its notes
(the same in every cycle), its level and its brightness, and each copy's fade is read by soloing that copy.
The song's notes are read where they SOUND: a `risset` track's copies (tools/risset.py), a warped track's notes
moved (tools/warp.py), a track that starts late from its own start.
"""
import collections
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import keyshape  # noqa: E402
import risset  # noqa: E402
import songfmt  # noqa: E402
import warp  # noqa: E402
import wincut  # noqa: E402
from keybench import EDGES, LABELS  # noqa: E402

SPREAD_DB = 1.5        # the cycles' levels apart by this much: SPREAD
BAND_DB = 3.0          # a band the part has, apart by this much between cycles: SPREAD
HOLDS_DB = -25         # a band counts when it is within this of the part's total
DRIFT_OCT = 0.05       # the centroid moving this much a cycle ...
DRIFT_ALL = 0.25       # ... or this much over the passage: DRIFT
CYCLE_NOISE_OCT = 0.045  # how far a cycle's centroid sits from the line through them where a passage HOLDS: False
#                          Summit's stair (eight guitars, seven cycles of two bars) runs +0.009 octaves a cycle while
#                          neighbouring cycles differ by up to 0.11. So few cycles cannot show a small drift: see drift_floor
LONGER = 0.6           # the cycles' levels this alike some cycles on (and 1 dB apart): A LONGER CYCLE under this one
SAW_DB, SAW_OCT = 1.5, 0.15                    # a run through the cycle of this much, undone at the wrap: SAW-TOOTH


def load(path):
    """A render as mono floats and its rate."""
    with wave.open(path) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if sw == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        x = ((b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)) << 8 >> 8).astype(float) / (1 << 23)
    else:
        x = np.frombuffer(raw, dtype={1: np.uint8, 2: np.int16, 4: np.int32}[sw]).astype(float)
        x = (x - 128) / 128 if sw == 1 else x / float(1 << (8 * sw - 1))
    return x.reshape(-1, ch).mean(axis=1), sr


def cycle_seconds(tok, tempo=None):
    """--cycle in seconds: 1bar / 4bars (4/4), 16b (beats), 2.4s. None when it cannot be read (or needs a tempo)."""
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*(bars?|b|s)", tok.strip())
    if not m or float(m.group(1)) <= 0:
        return None
    n, unit = float(m.group(1)), m.group(2)
    if unit == "s":
        return n
    return None if not tempo else n * (4 if unit.startswith("bar") else 1) * 60.0 / tempo


def power(seg, sr):
    """Frequencies and power of a stretch: overlapping Hann frames (hop a quarter), or one unfaded frame when short."""
    n = 4096
    while n > len(seg):
        n //= 2
    if n < 256 or len(seg) < 2 * n:
        return np.fft.rfftfreq(len(seg), 1 / sr), np.abs(np.fft.rfft(seg)) ** 2
    win, acc = np.hanning(n), 0
    for i in range(0, len(seg) - n + 1, n // 4):
        acc = acc + np.abs(np.fft.rfft(seg[i:i + n] * win)) ** 2
    return np.fft.rfftfreq(n, 1 / sr), acc


def shape(seg, sr):
    """(level dB, [nine bands dB], centroid Hz) of a stretch."""
    f, p = power(seg, sr)
    rows = [10 * np.log10(p[(f >= lo) & (f < hi)].sum() + 1e-30) for lo, hi in zip(EDGES, EDGES[1:])]
    m = (f >= 40) & (f < 8000)
    cen = float((f[m] * p[m]).sum() / (p[m].sum() + 1e-30))
    return 10 * np.log10(np.mean(seg ** 2) + 1e-20), rows, max(cen, 1.0)


def run_of(values):
    """How far a profile runs through the cycle: a straight line through its slices, end to end."""
    k = len(values)
    if k < 2:
        return 0.0
    pos = (np.arange(k) + 0.5) / k
    return float(np.polyfit(pos, np.asarray(values, float), 1)[0])


def saw(run, wrap, least):
    """A run through the cycle undone at the wrap."""
    return abs(run) >= least and run * wrap < 0 and abs(wrap) >= abs(run) / 2


def measure(x, sr, cycle_s, steps=16):
    """Everything read from the audio: the cycles against each other, and the cycle's inside."""
    lc = cycle_s * sr
    n = int(len(x) / lc + 1e-6)
    if n < 2:
        raise SystemExit(f"endless: the passage holds {len(x) / lc:.2f} cycles of {cycle_s:g} s: two or more are needed")
    edge = [int(round(i * lc)) for i in range(n + 1)]
    cyc = [shape(x[a:b], sr) for a, b in zip(edge, edge[1:])]
    lev = [c[0] for c in cyc]
    bands = np.array([c[1] for c in cyc])
    total = 10 * np.log10((10 ** (bands / 10)).sum(axis=1))
    held = [i for i in range(len(LABELS)) if (bands[:, i] - total).mean() >= HOLDS_DB]
    spread = {LABELS[i]: float(np.ptp(bands[:, i] - total)) for i in held}
    worst = max(spread, key=spread.get) if spread else None
    cen = np.log2([c[2] for c in cyc])
    drift = float(np.polyfit(np.arange(n), cen, 1)[0])
    dev, longer = np.asarray(lev) - np.mean(lev), None
    if np.ptp(lev) >= 1.0:                           # a longer cycle: the levels alike `lag` cycles on, seen three times
        best = max(((float(np.corrcoef(dev[:-lag], dev[lag:])[0, 1]), lag) for lag in range(2, min(8, n // 3) + 1)
                    if dev[:-lag].std() > 0 and dev[lag:].std() > 0), default=(0.0, 0))
        if best[0] >= LONGER:
            longer = {"every": best[1], "alike": best[0],
                      "places": [float(dev[i::best[1]].mean()) for i in range(best[1])]}
    lv, ce = np.zeros((n, steps)), np.zeros((n, steps))
    for c in range(n):
        for k in range(steps):
            a = int(round((c + k / steps) * lc))
            b = int(round((c + (k + 1) / steps) * lc))
            lv[c, k], _, cz = shape(x[a:b], sr)
            ce[c, k] = np.log2(cz)
    quiet = lv < lv.max() - 50                      # a silent slice has no centroid to speak of
    ce = np.where(quiet, np.nan, ce)
    lvp = (lv - lv.mean(axis=1, keepdims=True)).mean(axis=0)

    def mean_of(rows):                               # a mean that leaves the silent slices out (0 where all are)
        ok = ~np.isnan(rows)
        return np.where(ok.any(axis=0), np.where(ok, rows, 0).sum(axis=0) / np.maximum(1, ok.sum(axis=0)), 0.0)
    own = np.array([np.nanmean(r) if (~np.isnan(r)).any() else 0.0 for r in ce])
    cep = mean_of(ce - own[:, None])
    wraps = {"level": float(np.mean(lv[1:, 0] - lv[:-1, -1])), "centroid": float(mean_of((ce[1:, 0] - ce[:-1, -1])[:, None])[0])}
    runs = {"level": run_of(lvp), "centroid": run_of(cep)}
    steps_in = {"level": float(np.abs(np.diff(lvp)).max()), "centroid": float(np.abs(np.diff(cep)).max())}
    return {
        "cycles": n, "cycle_s": cycle_s, "steps": steps,
        "level": float(np.mean(lev)), "level_spread": float(np.ptp(lev)), "levels": [float(v) for v in lev],
        "band_spread": spread, "worst_band": worst, "longer": longer,
        "worst_by_cycle": [] if worst is None else [float(v) for v in (lambda r: r - r.mean())(
            bands[:, LABELS.index(worst)] - total)],
        "centroid_hz": float(2 ** cen.mean()), "centroid_drift": drift, "centroid_all": float(cen[-1] - cen[0]),
        "inside": {"level": [float(v) for v in lvp], "centroid": [float(v) for v in cep]},
        "runs": runs, "wraps": wraps, "steps_inside": steps_in,
    }


def find(doc, name):
    """The track of that name, at any depth; None when there is none."""
    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") == name:
                    return t
                got = walk(t.get("tracks"))
                if got is not None:
                    return got
        return None
    return walk(doc.get("tracks"))


def notes_sounding(doc, name, tempo=None):
    """A track's notes where they SOUND, in the song's beats: a `risset` track's copies, a warped track's notes moved,
    a late track's notes from its own start; as written when no tempo is given. [] when there is no such track."""
    t = find(doc, name)
    if t is None:
        return []
    notes = [n for n in t.get("notes") or [] if isinstance(n, dict)]
    if not tempo:
        return notes
    try:
        if t.get("risset"):
            return risset.sounding(t, tempo)
        origin = warp.beats(t.get("at", 0), tempo)
        if t.get("warp"):
            notes = warp.moved(notes, t["warp"], tempo)
    except (ValueError, TypeError, KeyError):
        return notes
    return [dict(n, at=origin + float(n.get("at") or 0)) for n in notes] if origin else notes


def plan_cycles(doc, tracks, b0, b1, cycle_beats, tempo=None):
    """From the song: each whole cycle's notes of the parts together, as {(place in the cycle, pitch): count}; then
    (how many cycles, notes in the usual cycle, [(cycle from 1, notes that differ)])."""
    n = int((b1 - b0) / cycle_beats + 1e-6)
    cyc = [collections.Counter() for _ in range(n)]
    for t in tracks:
        for note in notes_sounding(doc, t, tempo):
            at = float(note.get("at") or 0)
            i = int((at - b0) / cycle_beats + 1e-6) if at >= b0 - 1e-9 else -1
            if 0 <= i < n and at < b1 - 1e-9:
                cyc[i][(round(at - b0 - i * cycle_beats, 4), str(note.get("pitch", note.get("key", ""))))] += 1
    if not cyc:
        return 0, 0, []
    usual = collections.Counter(frozenset(c.items()) for c in cyc).most_common(1)[0][0]
    ref = collections.Counter(dict(usual))
    odd = [(i + 1, sum(((c - ref) + (ref - c)).values())) for i, c in enumerate(cyc) if c != ref]
    return n, sum(ref.values()), odd


def drift_floor(n):
    """The least drift (octaves a cycle) that n cycles can show: DRIFT_OCT, or with few cycles twice what their own
    scatter (CYCLE_NOISE_OCT) gives a line through n of them: two cycles 0.13, three 0.064, four or more 0.05.
    (chirper-zero, False Summit v6: -0.06 and +0.10 on two cycles of a lead with an echo were marked DRIFT; they
    are inside what one cycle differs from the next where a passage holds.)"""
    i = np.arange(max(2, int(n)))
    return max(DRIFT_OCT, 2 * CYCLE_NOISE_OCT / float(np.sqrt(((i - i.mean()) ** 2).sum())))


def marks(got, plan=None):
    """The lines an ear should look at: [(mark, what)]."""
    out = []
    if got["level_spread"] > SPREAD_DB:
        out.append(("SPREAD", f"the cycles' levels are {got['level_spread']:.1f} dB apart"))
    if got["worst_band"] and got["band_spread"][got["worst_band"]] > BAND_DB:
        out.append(("SPREAD", f"{got['worst_band']} Hz moves {got['band_spread'][got['worst_band']]:.1f} dB between cycles"))
    if abs(got["centroid_drift"]) >= drift_floor(got["cycles"]) or abs(got["centroid_all"]) >= DRIFT_ALL:
        out.append(("DRIFT", f"the centroid moves {got['centroid_drift']:+.2f} octaves a cycle, {got['centroid_all']:+.2f} over "
                             "the passage: it is going somewhere (a real octave a cycle would read 1.00)"))
    if got.get("longer"):
        lg = got["longer"]
        out.append(("A LONGER CYCLE", f"the cycles' levels repeat every {lg['every']} cycles ("
                    + " ".join(f"{v:+.1f}" for v in lg["places"]) + " dB by place): the ear may hear that period"))
    for name, least, unit in (("level", SAW_DB, "dB"), ("centroid", SAW_OCT, "octaves")):
        r, w = got["runs"][name], got["wraps"][name]
        if saw(r, w, least):
            what = {"level": "the level", "centroid": "the brightness"}[name]
            out.append(("SAW-TOOTH", f"{what} runs {r:+.2f} {unit} through the cycle and goes {w:+.2f} at the wrap: it starts again"))
    if plan and plan[2]:
        out.append(("ANOTHER PATTERN", "the song writes other notes in cycle " + ", ".join(f"{i} ({d} notes)" for i, d in plan[2][:8])
                    + ("..." if len(plan[2]) > 8 else "")))
    return out


def render_solo(path, tracks, pin, f, t, where, seed=0):
    wav = os.path.join(where, "endless.wav")
    cmd = ["nice", "-n", "12", pin, "render", "-f", path, "--seed", str(seed), "--set", "loudness=null", "--threads", "2",
           "--from", f, "--to", t, "-o", wav]
    for name in tracks:
        cmd += ["--solo", name]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    if r.returncode:
        raise SystemExit("endless: the parts did not render: " + (r.stderr or r.stdout).strip()[-400:])
    return wav


def report(head, got, plan, warped):
    print(head)
    print("  ONE CYCLE LATER (each cycle against the others):")
    print(f"    level       {got['level']:6.1f} dB; the cycles within {got['level_spread']:.1f} dB of each other")
    if got["cycles"] <= 48:
        print("                by cycle, against their mean: " + " ".join(f"{v - got['level']:+.1f}" for v in got["levels"]))
    if got["worst_band"]:
        worst = got["worst_band"]
        print(f"    spectrum    the band that moves most between cycles: {worst} Hz, {got['band_spread'][worst]:.1f} dB"
              f"   ({', '.join(f'{k} {v:.1f}' for k, v in got['band_spread'].items())})")
        if got["cycles"] <= 48 and got.get("worst_by_cycle"):
            print("                that band by cycle, against their mean: " + " ".join(f"{v:+.1f}" for v in got["worst_by_cycle"]))
    print(f"    brightness  centroid {got['centroid_hz']:.0f} Hz; it moves {got['centroid_drift']:+.2f} octaves a cycle, "
          f"{got['centroid_all']:+.2f} over the passage (a part that climbed an octave a cycle: +1.00)")
    if plan:
        n, notes, odd = plan
        print(f"    the song    {n} cycles of {notes} notes" + (", the same notes at the same places in every one" if not odd else
              ": NOT the same in cycle " + ", ".join(f"{i} ({d} notes differ)" for i, d in odd[:8]) + ("..." if len(odd) > 8 else "")))
        if warped:
            print(f"                ({', '.join(warped)}: a risset AND a warp on one track: its notes are read as the risset alone)")
    k = got["steps"]
    print(f"  INSIDE THE CYCLE, AND AT THE WRAP ({k} slices, the mean over the {got['cycles']} cycles, against the cycle's own):")
    for a in range(0, k, 16):
        b = min(k, a + 16)
        print("    slice          " + "".join(f"{i + 1:6d}" for i in range(a, b)))
        print("    level dB       " + "".join(f"{v:+6.1f}" for v in got["inside"]["level"][a:b]))
        print("    centroid oct   " + "".join(f"{v:+6.2f}" for v in got["inside"]["centroid"][a:b]))
    r, w = got["runs"], got["wraps"]
    si = got["steps_inside"]
    print(f"    level       runs {r['level']:+.1f} dB through the cycle; at the wrap {w['level']:+.1f} dB "
          f"(slice to slice inside it: up to {si['level']:.1f})")
    print(f"    brightness  runs {r['centroid']:+.2f} octaves through the cycle; at the wrap {w['centroid']:+.2f} "
          f"(slice to slice inside it: up to {si['centroid']:.2f})")
    ms = marks(got, plan)
    if not ms:
        print("  IT HOLDS: one cycle later it is the same, and nothing starts again at the wrap.")
    for mark, what in ms:
        print(f"  {mark}: {what}")
    if any(m == "SPREAD" for m, _ in ms) and got.get("seed") is not None:
        print(f"  (a SPREAD is read on one seed, {got['seed']}: read it on another, --seed {got['seed'] + 1}. One that moves to "
              "another cycle with the seed is the players' own variation; one that stays put is written in the song)")
    floor = drift_floor(got["cycles"])
    if DRIFT_OCT <= abs(got["centroid_drift"]) < floor and not any(m == "DRIFT" for m, _ in ms):
        print(f"  (the centroid's {got['centroid_drift']:+.2f} octaves a cycle is not marked: from {got['cycles']} cycles a drift "
              f"under {floor:.2f} is inside what one cycle differs from the next where a passage holds; more cycles would say)")
    print("  (whether an ear hears it climb for ever is not measured here; marks are questions for an ear before they are faults)")


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--keep": None, "--cycle": None, "--steps": "16", "--wav": None, "--tempo": None, "--seed": "0"}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    as_json = "--json" in a
    if as_json:
        a.remove("--json")
    want = 0 if opt["--wav"] else 3
    if "-h" in a or "--help" in a or len(a) != want or not opt["--cycle"]:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    try:
        steps = int(opt["--steps"])
    except ValueError:
        steps = 0
    try:
        seed = int(opt["--seed"])
    except ValueError:
        raise SystemExit("endless: --seed takes a whole number") from None
    if not 2 <= steps <= 96:
        raise SystemExit("endless: --steps takes a whole number of slices, 2 to 96")
    plan, warped = None, []
    if opt["--wav"]:
        cyc = cycle_seconds(opt["--cycle"], float(opt["--tempo"]) if opt["--tempo"] else None)
        if not cyc:
            raise SystemExit("endless: --cycle takes 1bar, 4bars, 16b (with --tempo BPM) or 2.4s")
        x, sr = load(opt["--wav"])
        got = measure(x, sr, cyc, steps)
        head = f"{os.path.basename(opt['--wav'])}: {got['cycles']} cycles of {opt['--cycle']} ({cyc:.3f} s)"
    else:
        song, tracks, span = a[0], a[1].split(","), a[2]
        path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
        if not os.path.exists(path):
            raise SystemExit(f"endless: no song {song}")
        doc = songfmt.load(path)
        tempo = doc.get("tempo", 120)
        if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
            raise SystemExit("endless: the song's tempo changes: only fixed-tempo songs are read")
        ends = span.split("-")
        pos = [wincut.position(t, tempo) for t in ends] if len(ends) == 2 else [None]
        if None in pos or pos[1] <= pos[0]:
            raise SystemExit("endless: FROM-TO takes two positions as chirp render does (9-33, 32b-128b, 19.2s-76.8s)")
        cyc = cycle_seconds(opt["--cycle"], tempo)
        if not cyc:
            raise SystemExit("endless: --cycle takes 1bar, 4bars, 16b or 2.4s")
        for t in tracks:
            if keyshape.track_notes(doc, t) is None:
                raise SystemExit(f"endless: {os.path.basename(path)} has no track {t}")
        where = opt["--keep"] or tempfile.mkdtemp(prefix="endless-")
        os.makedirs(where, exist_ok=True)
        try:
            x, sr = load(render_solo(path, tracks, opt["--pin"] or chirpbin.resolve(), ends[0], ends[1], where, seed))
        finally:
            if not opt["--keep"]:
                shutil.rmtree(where, True)
        got = {**measure(x, sr, cyc, steps), "seed": seed}
        plan = plan_cycles(doc, tracks, pos[0] * tempo / 60.0, pos[1] * tempo / 60.0, cyc * tempo / 60.0, tempo)
        warped = [t for t in tracks if (find(doc, t) or {}).get("risset") and (find(doc, t) or {}).get("warp")]
        head = (f"{os.path.basename(path)} {', '.join(tracks)}: {span}, {got['cycles']} cycles of {opt['--cycle']} ({cyc:.3f} s), "
                "alone through their own effects, bus and master")
    if as_json:
        print(json.dumps({**got, "drift_floor": drift_floor(got["cycles"]), "marks": marks(got, plan), "plan": None if not plan else
                          {"cycles": plan[0], "notes": plan[1], "differ": plan[2]}, "written_only": warped}))
        return 0
    report(head, got, plan, warped)
    return 0


if __name__ == "__main__":
    sys.exit(main())
