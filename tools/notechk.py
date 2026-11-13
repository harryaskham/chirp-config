#!/usr/bin/env python3
"""notechk: how one track's notes are struck, note by note, in a render of our OWN song (chirper-zero, Common Time v25,
where it showed that the string pick makes a muted low F pulse, not attack faster; made general and promoted by chirp-eco).

The same per-note measures as tools/riffpunch.py takes on a record, here on a guitars-alone (or one-track) render:
  rise    10-90% of the attack's peak, 150 Hz-8 kHz, in ms
  punch   the attack's peak against 30-60 ms later, in dB
  tight   100-250 Hz in the first 20 ms against 40-80 ms, in dB (how fast the low end dies)
  grain   spectral flatness at 1-4 kHz over 20-120 ms (the noise between the harmonics)
Medians over the track's clean onsets: those with no other note of the track 40 ms before or 60 ms after.

  notechk.py SONG TRACK [--from POS] [--which muted|open|all] [--channel left|right|mid] [--pin BIN] WAV [WAV ...]

SONG is a climb ID (songs/ID.yaml) or a song file. The notes and the tempo come from `chirp plan` (a fixed tempo only;
the plan leaves out a tempo of 120). --from is where the render starts, as `chirp render --from` takes it: a bar (41,
1-indexed, in 4/4), beats (160b) or seconds (76.2s); default the top. --which: muted (notes with `expr.pm`, the
default), open (those without) or all. --channel: left by default (a track panned hard left in a pair). Several WAVs
are several candidates over the same notes: render each the same way and read the rows against each other.
Read-only; nothing is rendered.
"""
import argparse
import json
import os
import subprocess
import sys
import wave

import numpy as np
from scipy import signal as sg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wincut  # noqa: E402


def track_notes(canon, name):
    """The notes of the track called name, at any depth; None when there is no such track."""
    def walk(ts):
        for t in ts or []:
            if isinstance(t, dict):
                if t.get("name") == name:
                    return [n for n in t.get("notes") or [] if isinstance(n, dict)]
                found = walk(t.get("tracks"))
                if found is not None:
                    return found
        return None
    return walk(canon.get("tracks"))


def start_beats(pos, tempo):
    """Where a render that began at `chirp render --from POS` starts, in beats."""
    s = wincut.position(pos, tempo)
    return None if s is None else s * tempo / 60.0


def onsets(notes, start, tempo, which="muted"):
    """(the chosen notes' times, every note's time), seconds into the render."""
    def at(n):
        return round((float(n.get("at") or 0) - start) * 60 / tempo, 4)
    muted = lambda n: bool((n.get("expr") or {}).get("pm"))  # noqa: E731
    pick = {"muted": muted, "open": lambda n: not muted(n), "all": lambda n: True}[which]
    return sorted(set(at(n) for n in notes if pick(n))), sorted(set(at(n) for n in notes))


def load(path, channel="left"):
    with wave.open(path) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float).reshape(-1, w.getnchannels()) / 32768
    if channel == "mid":
        return x.mean(axis=1), sr
    return x[:, 0 if channel == "left" else x.shape[1] - 1], sr


def measure(x, sr, on, allon):
    """{n, rise, punch, tight, grain}: medians over the clean onsets (n of them); None values when there is none."""
    dur = len(x) / sr
    bp = sg.sosfilt(sg.butter(4, [150, 8000], "bandpass", fs=sr, output="sos"), x)
    env = sg.sosfiltfilt(sg.butter(2, 200, fs=sr, output="sos"), np.abs(bp))
    lo = sg.sosfilt(sg.butter(4, [100, 250], "bandpass", fs=sr, output="sos"), x)
    rise, tight, grain, punch = [], [], [], []
    for t in on:
        if t < 0.05 or t > dur - 0.2:
            continue
        if any(0 < t - u < 0.04 or 0 < u - t < 0.06 for u in allon):
            continue
        a, b = int((t - 0.01) * sr), int((t + 0.04) * sr)
        seg = env[a:b]
        k = int(np.argmax(seg))
        pk = seg[k]
        if pk <= 0:
            continue
        base = env[max(0, a - int(0.004 * sr)):a + 1].min()
        r = seg[:k + 1]
        span = pk - base
        i10 = np.argmax(r >= base + 0.1 * span)
        i90 = np.argmax(r >= base + 0.9 * span)
        rise.append((i90 - i10) / sr * 1000)
        t0 = a + k
        later = env[t0 + int(0.03 * sr):t0 + int(0.06 * sr)].mean()
        punch.append(20 * np.log10(pk / max(later, 1e-9)))
        e = lambda s, u, v: np.sqrt((s[int((t + u) * sr):int((t + v) * sr)] ** 2).mean() + 1e-18)  # noqa: E731
        tight.append(20 * np.log10(e(lo, 0, 0.02) / e(lo, 0.04, 0.08)))
        w = x[int((t + 0.02) * sr):int((t + 0.12) * sr)]
        if len(w) > 256:
            X = np.abs(np.fft.rfft(w * np.hanning(len(w)))) ** 2
            f = np.fft.rfftfreq(len(w), 1 / sr)
            m = (f >= 1000) & (f < 4000)
            grain.append(np.exp(np.mean(np.log(X[m] + 1e-20))) / (X[m].mean() + 1e-20))
    md = lambda v: float(np.median(v)) if len(v) else None  # noqa: E731
    return {"n": len(rise), "rise": md(rise), "punch": md(punch), "tight": md(tight), "grain": md(grain)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song", help="a climb ID (songs/ID.yaml) or a song file")
    ap.add_argument("track")
    ap.add_argument("wav", nargs="+")
    ap.add_argument("--from", dest="frm", default="1", help="where the render starts: a bar (1-indexed), beats (160b) or seconds (76.2s)")
    ap.add_argument("--which", choices=["muted", "open", "all"], default="muted")
    ap.add_argument("--channel", choices=["left", "right", "mid"], default="left")
    ap.add_argument("--pin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song = a.song if os.path.exists(a.song) else os.path.join(ROOT, "songs", f"{a.song}.yaml")
    if not os.path.exists(song):
        raise SystemExit(f"notechk: no song {a.song!r} (a climb ID or a file)")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, env=env)
    try:
        d = json.loads(r.stdout)
        canon = (d.get("data") or d).get("canonical") or {}
    except ValueError:
        raise SystemExit(f"notechk: chirp plan failed: {r.stderr.strip()[-300:]}")
    tempo = canon.get("tempo", 120.0)          # the plan leaves out a tempo of 120, the engine's default
    if not isinstance(tempo, (int, float)) or tempo <= 0:
        raise SystemExit("notechk: this song's tempo changes; notechk reads fixed-tempo songs only")
    notes = track_notes(canon, a.track)
    if notes is None:
        raise SystemExit(f"notechk: no track {a.track!r} in {os.path.basename(song)}")
    start = start_beats(a.frm, tempo)
    if start is None:
        raise SystemExit(f"notechk: --from {a.frm!r} is not a bar (41), beats (160b) or seconds (76.2s)")
    on, allon = onsets(notes, start, tempo, a.which)
    rows = []
    for p in a.wav:
        x, sr = load(p, a.channel)
        rows.append(dict(measure(x, sr, on, allon), file=p))
    if a.json:
        print(json.dumps({"song": song, "track": a.track, "which": a.which, "channel": a.channel, "rows": rows}))
        return
    for m in rows:
        name = m["file"].split("/")[-1]
        if not m["n"]:
            print("%-34s n %3d | no clean %s onsets of %s in this render" % (name, 0, a.which, a.track))
            continue
        print("%-34s n %3d | rise %5.1f ms  punch %4.1f dB  tight %4.1f dB  grain %.2f"
              % (name, m["n"], m["rise"], m["punch"], m["tight"], m["grain"]))


if __name__ == "__main__":
    sys.exit(main())
