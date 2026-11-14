#!/usr/bin/env python3
"""velramp: crescendos written in VELOCITY, and whether they sound (chirper-zero's finding and the check he asked for,
Common Time v42).

  velramp.py SONG [--min 30] [--bars 3] [--track T,T,...] [--measure] [--pin CHIRP] [--json]

A velocity ramp on a high-gain or compressed part is a crescendo that is not there: the amp is already saturated and
the compressor levels what is left. Common Time's five-bar approach was written so from v4 to v41 (velocity 0.45 to
0.9 on the tight rig and the bass, +6 dB as written): the guitars alone read -24.5 dB at its first bar and -24.6 at
its last, and the mix jumped 5.5 dB five bars early instead. Nothing measured it for 38 versions because every
balance tool read the section as fine.
From the plan (`chirp plan`), for each track of SONG (an id, or a file): every run of bars over which the velocity
of each bar's loudest note rises or falls by --min percent or more (default 30) across --bars bars or more (default 3; two bars
is a step between sections, not a ramp, and a kit has many), with the velocity at its two ends and what that is in
dB as written (20 log of the ratio). Bars are numbered as `chirp render --from` takes them. A warped track is read
where it sounds. --track keeps it to some tracks.
--measure renders each such track alone ONCE (through its own rig, bus and master, loudness off, seed 0) and reads
the level of the ramp's first bar and its last: "written +6.0 dB, sounds +0.1". A ramp that sounds less than a
quarter of what is written is marked NOT THERE; write that one as a gain lane (`auto`) on the track or its bus.
On drums and clean parts a velocity ramp is real, and the same table shows it.
What it cannot see: a ramp shorter than a bar, or one under a steady accent (it reads each bar's loudest note). The
level read is the bar's, so it also moves with how many notes the bar holds, and with any lane that rides the part
(the two add in the reading). Songs whose tempo changes or whose meter is not 4/4 are refused. Read-only.
Tests: tools/tests/test_velramp.py.
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
import notechk  # noqa: E402

TOL = 0.03          # a bar may step this far against the ramp (an accent pattern that does not fit the bar)


def bar_tops(notes, default=0.8, beats=4.0):
    """[(bar, the velocity of its loudest note)] for the bars that have notes, in order (bars 0-indexed). The
    loudest, not the mean: ghost strokes added to a bar bring its mean down while the bar gets louder."""
    by = {}
    for n in notes:
        v = n.get("vel")
        by.setdefault(int(math.floor(float(n.get("at") or 0) / beats + 1e-9)), []).append(default if v is None else float(v))
    return [(b, float(max(vs))) for b, vs in sorted(by.items())]


def _rising(means, least, bars):
    """[(index of the first bar, of the last)] of each run of consecutive bars whose value climbs by `least` or more
    over `bars` bars or more: a run goes on while no bar falls more than TOL under the highest so far, and is then
    cut down to where it moves (from the last bar still at the bottom to the first bar at the top)."""
    out, i, n = [], 0, len(means)
    while i < n - 1:
        j, top = i, means[i][1]
        while j + 1 < n and means[j + 1][0] == means[j][0] + 1 and means[j + 1][1] >= top * (1 - TOL):
            j += 1
            top = max(top, means[j][1])
        if j > i:
            vs = [v for _, v in means[i:j + 1]]
            ih = vs.index(max(vs))
            lo = min(vs[:ih + 1])
            a = max(k for k in range(ih + 1) if vs[k] <= lo * (1 + TOL))
            b = min(k for k in range(a, ih + 1) if vs[k] >= vs[ih] * (1 - TOL))
            if b - a + 1 >= bars and vs[a] > 0 and vs[b] / vs[a] >= 1 + least:
                out.append((i + a, i + b))
        i = max(j, i + 1)
    return out


def ramps(means, least=0.30, bars=3):
    """[(first bar, last bar, velocity at the first, at the last)] for every run of consecutive bars whose top
    velocity rises, or falls, by `least` or more (as a ratio: 0.30 is 0.45 to 0.585, or back) over `bars` bars or
    more. The level bars before and after a ramp are not part of it; a bar with no notes ends one."""
    up = _rising(means, least, bars)
    down = _rising([(b, 1.0 / v if v > 0 else float("inf")) for b, v in means], least, bars)
    return sorted((means[a][0], means[b][0], round(means[a][1], 3), round(means[b][1], 3)) for a, b in up + down)


def tracks_of(canon):
    names = []

    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") and (t.get("notes") or []):
                    names.append((t["name"], t.get("vel")))
                walk(t.get("tracks"))
    walk(canon.get("tracks"))
    return names


def find(canon, least=0.30, bars=3, only=None):
    """[{track, from, to (bars, 1-indexed), vel_from, vel_to, written_db}] over the whole song."""
    rows = []
    for name, vel in tracks_of(canon):
        if only and name not in only:
            continue
        notes = notechk.track_notes(canon, name) or []
        for a, b, v0, v1 in ramps(bar_tops(notes, 0.8 if vel is None else float(vel)), least, bars):
            rows.append({"track": name, "from": a + 1, "to": b + 1, "vel_from": v0, "vel_to": v1,
                         "written_db": round(20 * math.log10(v1 / v0), 1) if v0 > 0 and v1 > 0 else None})
    return rows


def plan(pin, song):
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, cwd=ROOT,
                       env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    try:
        d = json.loads(r.stdout)
    except ValueError:
        raise SystemExit(f"velramp: {os.path.basename(song)} does not plan: {(r.stderr or r.stdout).strip()[-300:]}") from None
    return (d.get("data") or d).get("canonical") or {}


def bar_level(x, sr, bar, tempo):
    """The level in dB of one bar (1-indexed) of a render that starts at the top of the song; None when silent."""
    spb = 4 * 60.0 / tempo
    seg = x[int((bar - 1) * spb * sr):int(bar * spb * sr)]
    p = float(np.mean(seg * seg)) if len(seg) else 0.0
    return 10 * math.log10(p) if p > 1e-12 else None


def measure(song, rows, tempo, pin, where, say=None):
    """Adds sounds_db (the last bar's level minus the first's, the track alone) and there (False: NOT THERE)."""
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    for name in dict.fromkeys(r["track"] for r in rows):
        mine = [r for r in rows if r["track"] == name]
        out = os.path.join(where, "solo.wav")
        end = max(r["to"] for r in mine) * 4
        if say:
            say(f"  rendering {name} alone to bar {end // 4} ...")
        r = subprocess.run(["nice", "-n", "12", pin, "render", "-f", song, "--seed", "0", "--set", "loudness=null", "--threads", "2",
                            "--solo", name, "--to", f"{end}b", "-o", out], capture_output=True, text=True, cwd=ROOT, env=env)
        if r.returncode:
            raise SystemExit("velramp: the track did not render: " + (r.stderr or r.stdout).strip()[-300:])
        with wave.open(out) as w:
            sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[sw]).reshape(-1, ch).astype(float)
        x = x.mean(1) / float(1 << (8 * sw - 1))
        for row in mine:
            a, b = bar_level(x, sr, row["from"], tempo), bar_level(x, sr, row["to"], tempo)
            row["sounds_db"] = None if a is None or b is None else round(b - a, 1)
            w_db = row["written_db"]
            row["there"] = None if row["sounds_db"] is None or w_db is None else not (
                abs(w_db) >= 2 and (row["sounds_db"] * w_db <= 0 or abs(row["sounds_db"]) < 0.25 * abs(w_db)))
    return rows


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--min": "30", "--bars": "3", "--track": None, "--pin": None}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    flags = {k: k in a for k in ("--measure", "--json")}
    a = [x for x in a if x not in flags]
    if len(a) != 1 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    song = a[0]
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", song + ".yaml")
    if not os.path.exists(path):
        raise SystemExit(f"velramp: no song {song}")
    pin = opt["--pin"] or chirpbin.resolve()
    canon = plan(pin, path)
    tempo = canon.get("tempo", 120.0)                # the plan leaves out a tempo of 120
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        raise SystemExit("velramp: the song's tempo changes: only fixed-tempo songs are read")
    if str(canon.get("meter") or "4/4").replace(" ", "") != "4/4":
        raise SystemExit("velramp: the song is not in 4/4: bars are not read")
    only = set(opt["--track"].split(",")) if opt["--track"] else None
    rows = find(canon, float(opt["--min"]) / 100.0, int(opt["--bars"]), only)
    if flags["--measure"] and rows:
        where = tempfile.mkdtemp(prefix="velramp-")
        try:
            measure(path, rows, tempo, pin, where, None if flags["--json"] else lambda m: print(m, file=sys.stderr))
        finally:
            shutil.rmtree(where, True)
    if flags["--json"]:
        print(json.dumps({"song": os.path.basename(path), "ramps": rows}))
        return 0
    if not rows:
        print(f"{os.path.basename(path)}: no velocity ramp of {float(opt['--min']):g}% or more over {opt['--bars']} bars or more")
        return 0
    gone = sum(1 for r in rows if r.get("there") is False)
    tail = f", {gone} that do{'es' if gone == 1 else ''} not sound" if flags["--measure"] else " (as written; --measure says which sound)"
    print(f"{os.path.basename(path)}: {len(rows)} velocity ramp{'s' if len(rows) != 1 else ''}{tail}")
    print(f"  {'track':12s} {'bars':>9s}  {'velocity':14s} {'written':>9s}" + ("   sounds (the track alone)" if flags["--measure"] else ""))
    for r in rows:
        w_db = "       -" if r["written_db"] is None else f"{r['written_db']:+6.1f} dB"
        line = f"  {r['track']:12s} {str(r['from']) + '-' + str(r['to']):>9s}  {r['vel_from']:.2f} to {r['vel_to']:.2f}   {w_db}"
        if "sounds_db" in r:
            line += ("   silent at an end" if r["sounds_db"] is None
                     else f"   {r['sounds_db']:+6.1f} dB" + ("   NOT THERE" if r["there"] is False else ""))
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
