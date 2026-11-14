#!/usr/bin/env python3
"""presence: how audible each of a song's tracks is inside its own mix (chirp-eco, 5 Nov; chirper-three found layers
30-50 dB under the mix in two Accretion songs by soloing them one at a time: parts nobody can hear).

  presence.py ID [--from POS --to POS] [--seed 0] [-j 3] [--buried -25] [--rms] [--json]
  presence.py ID --windows 3-10:wait 41-56:riffA 309-311 ...    (several windows in ONE run: a table for each)
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

--windows FROM-TO[:label] ... is for auditing a song section by section. A window render starts from the top, so a
window by itself costs a part-render of every track; with --windows the mix and every track are rendered ONCE, to the
end of the last window, and each window is cut from that (the same samples: tools/wincut.py), so twenty sections cost
what one costs. A song wincut cannot place (a tempo that changes, a meter other than 4/4) is rendered window by window.

A yardstick for a VOICE (14 Nov, for chirper-zero's question on Odd Sympathy v5, "what does `near` predict for an
ear"): the same measure taken on eleven Meshuggah records, the vocals stem against the record, reads vs mix -9.1 dB
(-6.8 to -9.9) and near 69% (52% to 82%). Those are voices a listener follows through a full band. A voice at -11 to
-12 dB and near 14-37% sits under every one of them; a recogniser read 5 of its 24 words in the mix and 14 alone
(tools/wordread.py: for a clean voice the mix is a fair test, for a harsh one it is not).

What it cannot see (chirper-zero, Common Time v22): a pure tone has all its energy in one band. A sine-like part read
-12 to -14 dB here ("buried", 5 dB under the lead) while it put its section's 250-500 Hz 3.8 dB further over the
reference records (tools/stembal.py). Both readings were right. A level under the mix is not a share of a band: for a
part with a narrow spectrum run stembal on the section as well.
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
import wincut  # noqa: E402

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


def plan_canonical(pin, song):
    """The song as chirp plan --json resolves it."""
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True)
    d = json.loads(r.stdout)
    d = d.get("data") or d
    return d.get("canonical") or {}


def plan_tracks(pin, song, canon=None):
    """[(name, muted)] of the song's top-level tracks, from chirp plan --json."""
    out = []
    for t in (plan_canonical(pin, song) if canon is None else canon).get("tracks") or []:
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


def one_window(pin, song, live, win, a, work):
    """{track: presence} for one window: the mix and every live track rendered over it."""
    jobs = [("__mix__", None)] + [(n, n) for n in live]
    with ThreadPoolExecutor(max(1, a.j)) as ex:
        wavs = dict(zip([j[0] for j in jobs], ex.map(
            lambda j: render(pin, song, os.path.join(work, f"{len(j[0])}-{abs(hash(j[0]))}.wav"), a.seed, win, j[1]),
            jobs)))
    kw = not a.rms
    mix = frames_db(L.load(wavs["__mix__"]), L.SR, kweight=kw)
    rows = {n: presence(mix, frames_db(L.load(wavs[n]), L.SR, kweight=kw), a.buried) for n in live}
    for f in wavs.values():
        os.remove(f)
    return rows


def many_windows(pin, song, live, windows, secs, a, work):
    """[{track: presence}] a window: the mix and every live track rendered ONCE, to the end of the last window, and
    each window cut from that (tools/wincut.py: the same samples a window render gives)."""
    last = max(range(len(secs)), key=lambda i: secs[i][1])
    to = windows[last].partition(":")[0].partition("-")[2]
    kw = not a.rms

    def one(job):
        name, solo = job
        wav = render(pin, song, os.path.join(work, f"{len(name)}-{abs(hash(name))}.wav"), a.seed, (None, to), solo)
        x = L.load(wav)
        os.remove(wav)
        out = []
        for s0, s1 in secs:
            f0, f1 = wincut.frames(s0, s1, L.SR)
            out.append(frames_db(x[f0:f1], L.SR, kweight=kw))
        return out

    jobs = [("__mix__", None)] + [(n, n) for n in live]
    with ThreadPoolExecutor(max(1, a.j)) as ex:
        db = dict(zip([j[0] for j in jobs], ex.map(one, jobs)))
    return [{n: presence(db["__mix__"][i], db[n][i], a.buried) for n in live} for i in range(len(secs))]


def report(song, span, a, tracks, live, rows):
    order = sorted(rows, key=lambda n: (rows[n]["vs_mix_db"] is None, -(rows[n]["vs_mix_db"] or -999)))
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--song")
    ap.add_argument("--from", dest="frm")
    ap.add_argument("--to")
    ap.add_argument("--windows", nargs="+", help="FROM-TO[:label] ...: several windows in one run, every track rendered once")
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
    if a.windows and (a.frm or a.to):
        raise SystemExit("presence: --windows or --from/--to, not both")
    for w in a.windows or []:
        if "-" not in w.partition(":")[0]:
            raise SystemExit(f"presence: --windows takes FROM-TO[:label], not {w!r}")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    canon = plan_canonical(pin, song)
    tracks = plan_tracks(pin, song, canon)
    live = [n for n, muted in tracks if not muted]
    win = (a.frm, a.to)
    work = tempfile.mkdtemp(prefix="presence-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    try:
        if a.windows:
            spans = [tuple(w.partition(":")[0].split("-", 1)) for w in a.windows]
            secs = wincut.window_seconds(canon, a.windows)
            many = many_windows(pin, song, live, a.windows, secs, a, work) if secs \
                else [one_window(pin, song, live, sp, a, work) for sp in spans]
        else:
            rows = one_window(pin, song, live, win, a, work)
    finally:
        for f in os.listdir(work):
            os.remove(os.path.join(work, f))
        os.rmdir(work)
    if a.windows:
        labels = [w.partition(":")[2] for w in a.windows]
        if a.json:
            print(json.dumps({"song": song, "muted": [n for n, m in tracks if m], "windows": [
                {"window": list(sp), "label": lb, "tracks": r} for sp, lb, r in zip(spans, labels, many)]}))
            return
        for sp, lb, r in zip(spans, labels, many):
            report(song, (f"{lb}: " if lb else "") + f"{sp[0]} -> {sp[1]}", a, tracks, live, r)
        return
    if a.json:
        print(json.dumps({"song": song, "window": win, "muted": [n for n, m in tracks if m], "tracks": rows}))
        return
    report(song, f"{a.frm or 'start'} -> {a.to or 'end'}", a, tracks, live, rows)


if __name__ == "__main__":
    main()
