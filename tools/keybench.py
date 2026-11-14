#!/usr/bin/env python3
"""keybench: the same bars of a part moved to other grounds, alone through its own rig: what a key does to the tone.
(chirp-eco, 14 Nov, for chirper-zero's question on Odd Sympathy v8: "is there a cheap way to read the same rig on F
and on C without a render each?" Not without a render: the amp is not linear and its tight filter sits ahead of it.
But the render needed is the part alone for a few bars, a second or two a ground.)

  keybench.py SONG TRACK[,TRACK...] FROM-TO SHIFT [SHIFT ...] [--pin CHIRP] [--keep DIR] [--json]

SONG is an id (songs/ID.yaml) or a file; the TRACKs are the part (both guitars of a rig: gl,gr); FROM-TO the bars it
plays, as `chirp render --from/--to` take positions (29-33, 112b-128b); each SHIFT a number of semitones (-7, 5).
The bench is the song with every other track's notes out, so the rig, its bus and the master are the song's own
(loudness off, seed 0), and the part's notes in the window as written, then moved by each SHIFT.
Prints the nine bands tools/stembal.py reads (under 60 Hz to 8-16 kHz) and the whole: the first row is the passage
as written, each band against its own total; every other row is that ground MINUS as written, in dB, same rig and
same gain. So a row says what the move does to the part's tone and level, and tools/eqpred.py says what filter
would take it back.
What it cannot say: what the rest of the band does on that ground (the bass moves too), and what a bus compressor
keyed by other tracks would do. Kit pieces and pitches that are not note names are left where they are.
--keep DIR keeps each bench song and render. --pin: the chirp binary (else $CHIRP, else the groove's pin).
Read-only. Tests: tools/tests/test_keybench.py.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import pitchbench  # noqa: E402
import songfmt  # noqa: E402
import wincut  # noqa: E402

EDGES = [20, 60, 120, 250, 500, 1000, 2000, 4000, 8000, 16000]             # tools/stembal.py's bands
LABELS = ["<60", "60-120", "120-250", "250-500", "500-1k", "1-2k", "2-4k", "4-8k", "8-16k"]


def moved(pitch, semis):
    """A note's `pitch` (a name, a chord "F1,C2", a MIDI number) moved by semis; anything else (a kit piece) as it is."""
    def one(q):
        try:
            m = pitchbench.midi(q)
        except ValueError:
            return q
        if isinstance(q, (int, float)) or str(q).strip().lstrip("-").replace(".", "", 1).isdigit():
            return m + semis if isinstance(q, (int, float)) else f"{m + semis:g}"
        m = int(round(m)) + semis
        return f"{pitchbench.NAMES[m % 12]}{m // 12 - 1}"
    if isinstance(pitch, (int, float)):
        return one(pitch)
    return ",".join(one(q) for q in str(pitch).split(","))


def bench(doc, tracks, b0, b1, semis):
    """The song with every note out but those of `tracks` that start in [b0, b1) beats, moved by semis.
    KeyError (the name) when a track is missing or plays nothing there."""
    out = json.loads(json.dumps(doc))
    src, got = {}, {}

    def walk(ts, into):
        for t in ts or []:
            if isinstance(t, dict):
                into[t.get("name")] = t
                walk(t.get("tracks"), into)
    walk(doc.get("tracks"), src)
    walk(out.get("tracks"), got)
    for name, t in got.items():
        for k in pitchbench.SOURCES + ("risset",):
            t.pop(k, None)
        if "notes" in t:
            t["notes"] = []
    for name in tracks:
        if name not in got:
            raise KeyError(name)
        notes = [n for n in src[name].get("notes") or [] if isinstance(n, dict) and b0 <= float(n.get("at") or 0) < b1]
        if not notes:
            raise KeyError(name + " (no notes there)")
        got[name]["notes"] = [dict(n, pitch=moved(n["pitch"], semis)) if "pitch" in n else dict(n) for n in notes]
        got[name].pop("mute", None)
    return out


def band_levels(path):
    """The nine bands' and the whole's power in dB, both channels summed."""
    power, freqs, _ = spectrum(path)
    rows = [10 * np.log10(power[(freqs >= lo) & (freqs < hi)].sum() + 1e-30) for lo, hi in zip(EDGES, EDGES[1:])]
    return rows + [10 * np.log10(power[(freqs >= EDGES[0]) & (freqs < EDGES[-1])].sum() + 1e-30)]


def spectrum(path):
    import eqpred
    return eqpred.spectrum(path)


def render(doc, pin, where, tag, b0, b1):
    song = os.path.join(where, f"bench{tag}.json")
    wav = os.path.join(where, f"bench{tag}.wav")
    with open(song, "w") as f:
        json.dump(doc, f)
    cmd = ["nice", "-n", "12", pin, "render", "-f", song, "--seed", "0", "--set", "loudness=null", "--threads", "2",
           "--from", f"{b0:g}b", "--to", f"{b1:g}b", "-o", wav]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    if r.returncode:
        raise SystemExit("keybench: the bench did not render: " + (r.stderr or r.stdout).strip()[-400:])
    return wav


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--keep": None}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    as_json = "--json" in a
    if as_json:
        a.remove("--json")
    if len(a) < 4 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    song, tracks, window = a[0], a[1].split(","), a[2]
    try:
        shifts = [int(s) for s in a[3:]]
    except ValueError:
        raise SystemExit("keybench: each SHIFT is a whole number of semitones, as in -7 5") from None
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
    if not os.path.exists(path):
        raise SystemExit(f"keybench: no song {song}")
    doc = songfmt.load(path)
    tempo = doc.get("tempo", 120)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("keybench: the song's tempo changes: only fixed-tempo songs are benched")
    lo, _, hi = window.partition("-")
    ends = [wincut.position(lo, tempo), wincut.position(hi, tempo) if hi else None]
    if ends[0] is None or ends[1] is None or ends[1] <= ends[0]:
        raise SystemExit(f"keybench: {window}: FROM-TO as chirp render takes positions, as in 29-33 or 112b-128b")
    b0, b1 = (round(s * tempo / 60.0, 4) for s in ends)
    pin = opt["--pin"] or chirpbin.resolve()
    where = opt["--keep"] or tempfile.mkdtemp(prefix="keybench-")
    os.makedirs(where, exist_ok=True)
    rows = []
    try:
        for k in [0] + [s for s in shifts if s != 0]:
            try:
                made = bench(doc, tracks, b0, b1, k)
            except KeyError as e:
                raise SystemExit(f"keybench: {os.path.basename(path)} has no track {e.args[0]}") from None
            rows.append((k, band_levels(render(made, pin, where, f"{k:+d}" if k else "", b0, b1))))
    finally:
        if not opt["--keep"]:
            shutil.rmtree(where, True)
    base = rows[0][1]
    table = [{"shift": 0, "bands": [round(v - base[-1], 1) for v in base[:-1]], "all": 0.0}]
    table += [{"shift": k, "bands": [round(v - b, 1) for v, b in zip(got[:-1], base[:-1])], "all": round(got[-1] - base[-1], 1)}
              for k, got in rows[1:]]
    if as_json:
        print(json.dumps({"song": os.path.basename(path), "tracks": tracks, "window": window, "bands": LABELS, "rows": table}))
        return 0
    print(f"{os.path.basename(path)} {', '.join(tracks)} at {window}: the same notes moved, alone through their own rig, bus and master")
    print(f"  {'semitones':14s}" + "".join(s.rjust(8) for s in LABELS) + "     all")
    for r in table:
        label = "as written" if r["shift"] == 0 else f"{r['shift']:+d}"
        print(f"  {label:14s}" + "".join(f"{v:+8.1f}" for v in r["bands"]) + (f"{r['all']:+8.1f}" if r["shift"] else "        "))
    print("  (as written: each band against the passage's own total; the rest: dB against as written, same rig, same gain)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
