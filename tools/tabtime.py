#!/usr/bin/env python3
"""Tab timing: a Songsterr tab's measure timeline (seconds, from its tempo automations and time signatures),
per-track onset times, and their alignment against a recording or stem.

  tabtime.py timeline DIR                       measure starts / beats / bpm / meter (JSON)
  tabtime.py onsets DIR TRACK                   onset times of one track (JSON)
  tabtime.py align DIR TRACK AUDIO [WIN]        offset (audio = tab + d) globally and per WIN-second window

DIR is a songsterr.py cache (ref/songsterr-ID/). The tab is a transcription aid; the alignment shows where a
transcription drifts from the recording (offsets that move between windows) and where it is trustworthy."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import songsterr as S  # noqa: E402


def timeline(cache):
    meta = json.load(open(f"{cache}/songsterr-meta.json"))
    tempo = {}
    for i in range(len(meta.get("tracks", []))):
        auto = S.load(cache, i).get("automations", {}).get("tempo", [])
        if auto:
            tempo = {p["measure"]: p["bpm"] for p in auto}
            break
    tr = S.load(cache, 0)
    out, sec, sig, bpm = [], 0.0, [4, 4], tempo.get(0, 120)
    for i, m in enumerate(tr["measures"]):
        sig = m.get("signature", sig)
        bpm = tempo.get(i, bpm)
        beats = 4 * sig[0] / sig[1]
        out.append({"m": i + 1, "start": round(sec, 4), "beats": beats, "bpm": bpm, "sig": f"{sig[0]}/{sig[1]}"})
        sec += beats * 60 / bpm
    return out


def onsets(cache, track, tl=None):
    tl = tl or timeline(cache)
    tr = S.load(cache, track)
    out = []
    for i, m in enumerate(tr["measures"]):
        pos, bpm = 0.0, tl[i]["bpm"]
        for b in m["voices"][0]["beats"]:
            notes = [n for n in b.get("notes", []) if not n.get("rest")]
            if notes and not b.get("rest") and not all(n.get("tie") for n in notes):
                out.append(round(tl[i]["start"] + pos * 60 / bpm, 4))
            pos += S.beats_of(b)
    return out


def flux_env(audio, fps=None):
    import likeness as L
    F = L.Feat(L.load(audio))
    f = np.maximum(np.diff(F.logb, axis=1), 0).sum(0)
    return (f - f.mean()) / (f.std() + 1e-9), L.FPS


def align(cache, track, audio, win=30.0, rng=2.0):
    on = onsets(cache, track)
    flux, fps = flux_env(audio)
    n = len(flux)
    train = np.zeros(n)
    for t in on:
        k = int(round(t * fps))
        if 0 <= k < n:
            train[k] = 1
    train = np.convolve(train, np.hanning(5), "same")

    def best(lo, hi, r):
        a, b, R = int(lo * fps), int(hi * fps), int(r * fps)
        sc = []
        for k in range(-R, R + 1):
            if a + k < 0 or b + k > n:
                sc.append(-1e9); continue
            x, y = flux[a + k:b + k], train[a:b]
            sc.append(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-9))
        k = int(np.argmax(sc))
        return round((k - R) / fps, 3), round(float(sc[k]), 3)

    end = min(on[-1] if on else 0, n / fps - rng)
    g = best(rng, end, rng)
    wins = [(w, *best(w, min(w + win, end), rng)) for w in np.arange(rng, end - win / 2, win)]
    return {"global": {"offset": g[0], "corr": g[1]}, "windows": [{"start": round(float(w), 1), "offset": d, "corr": c} for w, d, c in wins]}


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "timeline":
        print(json.dumps(timeline(a[1])))
    elif a[0] == "onsets":
        print(json.dumps(onsets(a[1], int(a[2]))))
    elif a[0] == "align":
        print(json.dumps(align(a[1], int(a[2]), a[3], float(a[4]) if len(a) > 4 else 30.0), indent=1))
