#!/usr/bin/env python3
"""pitchbench: the pitch a note really sounds at through a track's own rig, one held note at a time.
(chirper-zero's bench, Common Time v40, made a tool by chirp-eco, 14 Nov.)

  pitchbench.py SONG TRACK NOTE [NOTE ...] [--hold 1.6] [--gap 1] [--at POS] [--top 6] [--pin CHIRP] [--keep DIR] [--json]

Why a bench: a note's pitch cannot be read off a riff through a saturated rig by picking partials out of the song's
own render. The neighbours' partials land on the new notes (3 x F1 is C3, 6 x F1 is C4; a note an octave up shares
every partial with the old one), so every reading is confounded. One held note at a time through the same rig is not.

SONG is an id (songs/ID.yaml) or a file; TRACK the track whose rig is wanted; each NOTE a pitch as the song writes it
(Gb3, F#2, C4; a MIDI number; a chord "F1,C2" prints its partials and no pitch). The bench is the song itself with
every track's notes taken out and TRACK's replaced by the NOTEs in turn, each held --hold seconds (default 1.6) with
--gap seconds between (default 1; a rig with a long reverb or a delay needs more, and the tool says when the note
before still rings): the rig, its bus and the master are the song's own, loudness off, seed 0. TRACK's `warp`, `risset`,
`repeat`, `stretch` and start offset are dropped; its `transpose`, patch, effects and lanes stay. Lanes are read
where the notes are put: the top of the song, or --at POS (as `chirp render` takes positions) to bench the rig as a
section lane leaves it.
For each note it prints the written pitch, what it SOUNDS AS (from how often the wave repeats, so a rig that takes
the fundamental out is still read; and how many cents that is from the written pitch), and the --top strongest
partials (default 6, from 30 Hz to 5 kHz): hertz, dB under the strongest, and the multiple of the written pitch. A
note that sounds more than 50 cents from where it is written is marked NOT AS WRITTEN. Through a saturated amp a
stiff string's partials stand in clusters a few hertz wide (the amp makes sums and differences of partials that are
not whole multiples), so one partial can read 2-3 Hz off its place while the note is in tune. A sound with a layer
an octave under the note (or an FM bell's half multiples) repeats at the lower octave and is read there: the
partials' multiples (x0.50) show it.
Pitches are read 12-tone equal, A4 440 Hz: a song with its own `tuning` is read against that.
--keep DIR keeps the bench song and its render there. --pin: the chirp binary (else $CHIRP, else the groove's pin).
Read-only. Tests: tools/tests/test_pitchbench.py.
"""
import json
import math
import os
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
import songfmt  # noqa: E402
import wincut  # noqa: E402

NAMES = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
SOURCES = ("score", "gen", "song")                           # what else gives a track notes
OWN_CLOCK = ("warp", "risset", "repeat", "stretch", "at")     # what would move the bench's notes


def midi(text):
    """The MIDI number of "Gb3", "F#2", "C4" or "54" (C4 = 60). ValueError for anything else."""
    s = str(text).strip()
    try:
        return float(s)
    except ValueError:
        pass
    if not s or s[0].upper() not in STEP:
        raise ValueError(f"{text!r} is not a pitch (Gb3, F#2, C4 or a MIDI number)")
    i, n = 1, STEP[s[0].upper()]
    while i < len(s) and s[i] in "#b":
        n += 1 if s[i] == "#" else -1
        i += 1
    try:
        return float(n + 12 * (int(s[i:]) + 1))
    except ValueError:
        raise ValueError(f"{text!r} is not a pitch (Gb3, F#2, C4 or a MIDI number)") from None


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def name(f):
    """("Gb3", cents from it) for a frequency."""
    m = 69 + 12 * math.log2(f / 440.0)
    n = int(round(m))
    return f"{NAMES[n % 12]}{n // 12 - 1}", 100 * (m - n)


def bench(doc, track, notes, hold_beats, gap_beats, at_beats=0.0):
    """The song `doc` as a bench: every track's notes out, `track`'s replaced by `notes` (pitch strings) held in turn
    from at_beats. Returns (the new song, each note's start in beats). KeyError when there is no such track."""
    out = json.loads(json.dumps(doc))
    found = []

    def walk(ts):
        for t in ts or []:
            if not isinstance(t, dict):
                continue
            for k in SOURCES + ("risset",):                       # a risset with no notes does not plan
                t.pop(k, None)
            if "notes" in t or t.get("name") == track:
                t["notes"] = []
            if t.get("name") == track:
                found.append(t)
            walk(t.get("tracks"))
    walk(out.get("tracks"))
    if not found:
        raise KeyError(track)
    t = found[0]
    for k in OWN_CLOCK:
        t.pop(k, None)
    t.pop("mute", None)
    starts = [at_beats + i * (hold_beats + gap_beats) for i in range(len(notes))]
    t["notes"] = [{"at": round(s, 4), "len": round(hold_beats, 4), "pitch": p, "vel": 0.85} for s, p in zip(starts, notes)]
    return out, starts


def peaks(x, sr, top=6, lo=30.0, hi=5000.0, sep=15.0, floor_db=40.0):
    """[(hertz, dB under the strongest)] of the `top` strongest partials of a held note, low to high."""
    if len(x) < sr // 4:
        return []
    n = 1 << max(18, int(np.ceil(np.log2(len(x)))) + 2)
    mag = np.abs(np.fft.rfft(x * np.hanning(len(x)), n))
    fr = np.fft.rfftfreq(n, 1 / sr)
    mag[(fr < lo) | (fr > hi)] = 0.0
    if mag.max() <= 0:
        return []
    ref = mag.max()
    width = int(sep / (sr / n))
    got = []
    work = mag.copy()
    while len(got) < top:
        i = int(np.argmax(work))
        if work[i] <= ref * 10 ** (-floor_db / 20):
            break
        f = fr[i]
        if 0 < i < len(mag) - 1:                                  # the peak between the bins
            a, b, c = np.log(mag[i - 1] + 1e-30), np.log(mag[i] + 1e-30), np.log(mag[i + 1] + 1e-30)
            d = a - 2 * b + c
            if d < 0:
                f += 0.5 * (a - c) / d * (sr / n)
        got.append((float(f), float(20 * np.log10(mag[i] / ref))))
        work[max(0, i - width):i + width + 1] = 0.0
    return sorted(got)


def sounds_as(x, sr, lo=25.0, hi=2000.0, dip=0.2):
    """The pitch of a held note in hertz, from how often the WAVE repeats (the YIN difference function: the shortest
    lag at which all but `dip` of the wave matches itself; failing that, the lag where it matches best), not from
    its partials: a rig that takes the fundamental out, or whose cabinet lifts partial sixteen over partial one,
    still repeats at the note's own rate. None when nothing repeats. A sound with a layer an octave under the note,
    or partials at half multiples (an FM bell), repeats at the lower octave and is read there; a wave four-fifths of
    which repeats at a higher rate (a fundamental 20 dB under its even partials and nothing else odd) is read up
    there."""
    n = int(min(len(x), 0.6 * sr))
    if n < sr // 5:
        return None
    y = x[:n] - x[:n].mean()
    if not np.any(y):
        return None
    top = int(sr / lo)
    size = 1 << int(np.ceil(np.log2(2 * n)))
    spec = np.fft.rfft(y, size)
    acf = np.fft.irfft(spec * np.conj(spec))[:top + 2]
    sq = np.concatenate(([0.0], np.cumsum(y * y)))
    lags = np.arange(top + 2)
    energy = (sq[n - lags] - sq[0]) + (sq[n] - sq[lags])            # the two overlapping stretches' energy at each lag
    diff = np.maximum(energy - 2 * acf, 0.0)
    norm = np.ones(top + 2)
    cum = np.cumsum(diff[1:])
    norm[1:] = diff[1:] * lags[1:] / np.maximum(cum, 1e-30)
    first = max(2, int(sr / hi))
    under = np.nonzero(norm[first:top] < dip)[0]
    if len(under):
        t = first + int(under[0])
        while t + 1 < top and norm[t + 1] < norm[t]:                # down to the bottom of that dip
            t += 1
    else:
        t = first + int(np.argmin(norm[first:top]))
        if norm[t] > 0.5:
            return None
    a, b, c = norm[t - 1], norm[t], norm[t + 1]
    d = a - 2 * b + c
    return float(sr / (t + (0.5 * (a - c) / d if d > 0 else 0.0)))


def read(path):
    with wave.open(path) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[sw]).reshape(-1, ch).astype(float)
    return x.sum(1) / float(1 << (8 * sw - 1)), sr


def level(x):
    return 10 * math.log10(float(np.mean(x * x)) + 1e-20) if len(x) else -200.0


def measure(x, sr, starts_s, hold_s, notes, top=6):
    """One row a note: {"note", "written_hz" (None for a chord), "sounds_hz", "sounds", "cents", "partials", "rings_db"
    (how far under this note the one before still rings as this one starts, when that is less than 30 dB)}."""
    rows = []
    for s, p in zip(starts_s, notes):
        seg = x[int((s + 0.15) * sr):int((s + hold_s - 0.05) * sr)]
        before = level(x[int(max(0.0, s - 0.2) * sr):int(max(0.0, s - 0.02) * sr)]) - level(seg) if s > 0.3 else -200.0
        chord = "," in p
        written = None if chord else hz(midi(p))
        pk = peaks(seg, sr, top, sep=15.0 if chord or written is None else max(15.0, 0.4 * written))
        row = {"note": p, "written_hz": written, "sounds_hz": None, "sounds": None, "cents": None,
               "rings_db": round(before, 1) if before > -30 else None,
               "partials": [{"hz": round(f, 1), "db": round(db, 1), "multiple": None if chord else round(f / written, 2)} for f, db in pk]}
        if not chord:
            f0 = sounds_as(seg, sr)
            if f0:
                nm, _ = name(f0)
                row.update(sounds_hz=round(f0, 1), sounds=nm, cents=round(1200 * math.log2(f0 / written), 1))
        rows.append(row)
    return rows


def render(doc, pin, out, where, start_b, end_b):
    song = os.path.join(where, "bench.json")
    with open(song, "w") as f:
        json.dump(doc, f)
    cmd = ["nice", "-n", "12", pin, "render", "-f", song, "--seed", "0", "--set", "loudness=null", "--threads", "2",
           "--to", f"{end_b:g}b", "-o", out]
    if start_b > 0:
        cmd += ["--from", f"{start_b:g}b"]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    if r.returncode:
        raise SystemExit("pitchbench: the bench did not render: " + (r.stderr or r.stdout).strip()[-400:])


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--hold": "1.6", "--gap": "1", "--at": None, "--top": "6", "--pin": None, "--keep": None}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    as_json = "--json" in a
    if as_json:
        a.remove("--json")
    if len(a) < 3 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    song, track, notes = a[0], a[1], a[2:]
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
    if not os.path.exists(path):
        raise SystemExit(f"pitchbench: no song {song}")
    doc = songfmt.load(path)
    tempo = doc.get("tempo", 120)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("pitchbench: the song's tempo changes: only fixed-tempo songs are benched")
    try:
        for p in notes:
            for q in p.split(","):
                midi(q)
    except ValueError as e:
        raise SystemExit(f"pitchbench: {e}") from None
    hold_s, gap_s = float(opt["--hold"]), float(opt["--gap"])
    beat = 60.0 / tempo
    at_b = 0.0
    if opt["--at"]:
        s = wincut.position(opt["--at"], tempo)
        if s is None:
            raise SystemExit(f"pitchbench: --at {opt['--at']}: a bar (41), beats (160b) or seconds (30s)")
        at_b = float(math.ceil(s / beat))
    try:
        made, starts = bench(doc, track, notes, hold_s / beat, gap_s / beat, at_b)
    except KeyError:
        raise SystemExit(f"pitchbench: {os.path.basename(path)} has no track {track}") from None
    end_b = math.ceil(starts[-1] + (hold_s + gap_s) / beat)
    made["length"] = f"{end_b}b"
    made.pop("tail", None)
    pin = opt["--pin"] or chirpbin.resolve()
    where = opt["--keep"] or tempfile.mkdtemp(prefix="pitchbench-")
    os.makedirs(where, exist_ok=True)
    try:
        wav = os.path.join(where, "bench.wav")
        render(made, pin, wav, where, at_b, end_b)
        x, sr = read(wav)
        rows = measure(x, sr, [(s - at_b) * beat for s in starts], hold_s, notes, int(opt["--top"]))
    finally:
        if not opt["--keep"]:
            shutil.rmtree(where, True)
    if as_json:
        print(json.dumps({"song": os.path.basename(path), "track": track, "rows": rows}))
        return 0
    where_said = f", at {opt['--at']}" if opt["--at"] else ""
    print(f"{os.path.basename(path)} track {track}: each note held {hold_s:g} s alone through the track's own rig{where_said}")
    print(f"  {'note':12s} {'written':>9s}  {'sounds as':22s} the strongest partials: Hz (dB under the strongest, x the written pitch)")
    for r in rows:
        parts = "  ".join(f"{p['hz']:.0f} ({p['db']:+.0f}" + (f", x{p['multiple']:.2f})" if p["multiple"] is not None else ")")
                          for p in r["partials"])
        if r["written_hz"] is None:
            print(f"  {r['note']:12s} {'':>9s}  {'(a chord: no one pitch)':22s} {parts}")
            continue
        if r["sounds"] is None:
            print(f"  {r['note']:12s} {r['written_hz']:7.1f}Hz  {'silent':22s}")
            continue
        heard = f"{r['sounds']} {r['cents']:+.0f} cents" if abs(r["cents"]) <= 50 else f"{r['sounds']}  NOT AS WRITTEN"
        print(f"  {r['note']:12s} {r['written_hz']:7.1f}Hz  {heard:22s} {parts}")
    for r in rows:
        if r["rings_db"] is not None:
            print(f"  ! as {r['note']} starts, the note before still rings {-r['rings_db']:.0f} dB under it (a reverb, a delay"
                  " or a long release in the rig): its partials are in this reading; give --gap more seconds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
