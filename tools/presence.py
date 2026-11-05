#!/usr/bin/env python3
"""presence: how audible each of a song's tracks is inside its own mix (chirp-eco, 5 Nov; chirper-three found layers
30-50 dB under the mix in two Accretion songs by soloing them one at a time: parts nobody can hear).

  presence.py ID [--from POS --to POS] [--seed 0] [-j 3] [--buried -25] [--rms] [--json]
  presence.py --song FILE ...                       (any song file; default songs/ID.yaml)

Renders the mix and every top-level track solo over the window (whole song by default; POS as chirp render takes it:
bars 49, beats 12b, seconds 30s), all unmastered (loudness=null) with the groove pin at nice 12, and prints per track:
  vs mix   its level against the mix while it SOUNDS (0.4 s frames where the solo is within 50 dB of its own peak
           frame), so a part that plays briefly is judged on when it plays, not diluted by its silence
  near     the share of those frames where it is within 10 dB of the mix (how often it can be followed)
  active   the share of the window it sounds at all
and flags BURIED (vs mix below --buried, default -25 dB) and LOUDEST. Levels are K-weighted (BS.1770, as LUFS:
the sub does not swamp the measure and hats are judged as heard); --rms for plain RMS. Tracks silent in the window
are listed as such, not as buried. Muted tracks are skipped. Read-only.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import levels  # noqa: E402
import likeness as L  # noqa: E402

ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
FRAME = 0.4          # seconds
SOUNDS_DB = 50.0     # a frame "sounds" within this many dB of the track's loudest frame
NEAR_DB = 10.0


def frames_db(x, sr, frame=FRAME, kweight=False):
    """Per-frame level in dB (mono sum): RMS, or K-weighted (BS.1770's filter, LUFS-like) with KWEIGHT."""
    m = x.mean(axis=1) if x.ndim > 1 else x
    if kweight:
        m = levels.k_weight(m.astype(np.float64), sr)
    n = max(1, int(frame * sr))
    k = len(m) // n
    if k == 0:
        return np.array([-120.0])
    r = np.sqrt((m[:k * n].astype(np.float64).reshape(k, n) ** 2).mean(1))
    return 20 * np.log10(r + 1e-9)


def presence(mix_db, solo_db, buried=-25.0):
    """{vs_mix_db, near, active, buried} for one track's frame levels against the mix's (same frame grid)."""
    k = min(len(mix_db), len(solo_db))
    mix_db, solo_db = mix_db[:k], solo_db[:k]
    peak = float(solo_db.max()) if k else -120.0
    on = solo_db > max(peak - SOUNDS_DB, -100.0)
    if peak < -100.0 or not on.any():
        return {"vs_mix_db": None, "near": 0.0, "active": 0.0, "buried": True, "silent": True}
    # power means over the sounding frames
    p = lambda v: 10 * np.log10(np.mean(10 ** (v / 10)) + 1e-12)  # noqa: E731
    vs = p(solo_db[on]) - p(mix_db[on])
    near = float(np.mean(solo_db[on] >= mix_db[on] - NEAR_DB))
    return {"vs_mix_db": round(float(vs), 1), "near": round(near, 2), "active": round(float(on.mean()), 2),
            "buried": bool(vs < buried), "silent": False}


def plan_tracks(pin, song):
    """[(name, muted)] of the song's top-level tracks, from chirp plan --json."""
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True)
    d = json.loads(r.stdout)
    d = d.get("data") or d
    out = []
    for t in (d.get("canonical") or {}).get("tracks") or []:
        if t.get("name"):
            out.append((t["name"], bool(t.get("mute"))))
    return out


def render(pin, song, out, seed, win, solo=None):
    cmd = ["nice", "-n", "12", pin, "render", "-f", song, "--seed", str(seed), "--set", "loudness=null", "-o", out]
    if win[0]:
        cmd += ["--from", win[0]]
    if win[1]:
        cmd += ["--to", win[1]]
    if solo:
        cmd += ["--solo", solo]
    env = dict(os.environ, RAYON_NUM_THREADS="2")
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode:
        raise RuntimeError(f"render failed ({solo or 'mix'}): {r.stderr.strip()[-300:]}")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--song")
    ap.add_argument("--from", dest="frm")
    ap.add_argument("--to")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--buried", type=float, default=-25.0)
    ap.add_argument("--pin")
    ap.add_argument("--rms", action="store_true", help="plain RMS instead of K-weighted levels")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song = a.song or (os.path.join(ROOT, "songs", f"{a.id}.yaml") if a.id else None)
    if not song or not os.path.exists(song):
        raise SystemExit("presence: give a climb ID (songs/ID.yaml) or --song FILE")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    tracks = plan_tracks(pin, song)
    live = [n for n, muted in tracks if not muted]
    win = (a.frm, a.to)
    work = tempfile.mkdtemp(prefix="presence-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    try:
        jobs = [("__mix__", None)] + [(n, n) for n in live]
        with ThreadPoolExecutor(max(1, a.j)) as ex:
            wavs = dict(zip([j[0] for j in jobs], ex.map(
                lambda j: render(pin, song, os.path.join(work, f"{len(j[0])}-{abs(hash(j[0]))}.wav"), a.seed, win, j[1]),
                jobs)))
        kw = not a.rms
        mix = frames_db(L.load(wavs["__mix__"]), L.SR, kweight=kw)
        rows = {n: presence(mix, frames_db(L.load(wavs[n]), L.SR, kweight=kw), a.buried) for n in live}
    finally:
        for f in os.listdir(work):
            os.remove(os.path.join(work, f))
        os.rmdir(work)
    order = sorted(rows, key=lambda n: (rows[n]["vs_mix_db"] is None, -(rows[n]["vs_mix_db"] or -999)))
    if a.json:
        print(json.dumps({"song": song, "window": win, "muted": [n for n, m in tracks if m], "tracks": rows}))
        return
    span = f"{a.frm or 'start'} -> {a.to or 'end'}"
    print(f"{os.path.basename(song)} ({span}; seed {a.seed}; unmastered, {'RMS' if a.rms else 'K-weighted'}): {len(live)} tracks"
          + (f", {len(tracks) - len(live)} muted skipped" if len(tracks) > len(live) else ""))
    print(f"  {'track':16s} {'vs mix':>8s} {'near':>6s} {'active':>7s}")
    loud = order[0] if order else None
    for n in order:
        r = rows[n]
        if r["silent"]:
            print(f"  {n:16s} {'silent':>8s}  (not in this window)")
            continue
        flag = "BURIED" if r["buried"] else ("LOUDEST" if n == loud else "")
        print(f"  {n:16s} {r['vs_mix_db']:+7.1f}  {r['near']:6.2f} {r['active']:7.2f}  {flag}")
    nb = sum(1 for r in rows.values() if r["buried"] and not r["silent"])
    if nb:
        print(f"  {nb} track(s) under {a.buried:g} dB while they sound: inaudible in the mix (raise, cut, or let them go)")


if __name__ == "__main__":
    main()
