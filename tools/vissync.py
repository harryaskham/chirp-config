#!/usr/bin/env python3
"""Measure picture-to-sound sync of an album video against its release files.

For each chapter, the picture's per-frame change (mean |frame - previous|) is
cross-correlated with the release audio's onset envelope (the positive change in log
energy per video frame). Both are taken on the album's absolute timeline: the audio is
decoded by ffmpeg from release.json's files in order, back to back, which is what ytpub's
kit does. The lag that best lines them up is reported for the first and the last 40 s of
every chapter. A lag of 0 means in sync; a positive lag means the picture is late.

  synccheck.py VIDEO RELEASE.json [--fps 30] [--window 40] [--max-lag 12]
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

SR = 48000


def decode_audio(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def video_motion(path, fps, w=96, h=54):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = w * h
    out = []
    prev = None
    while True:
        chunk = p.stdout.read(size * 600)
        if not chunk:
            break
        frames = np.frombuffer(chunk[: len(chunk) // size * size], dtype=np.uint8).reshape(-1, size).astype(np.float32)
        if prev is not None:
            frames_all = np.vstack([prev[None, :], frames])
        else:
            frames_all = np.vstack([frames[:1], frames])
        d = np.abs(np.diff(frames_all, axis=0)).mean(axis=1)
        out.append(d)
        prev = frames[-1]
    p.wait()
    return np.concatenate(out) if out else np.zeros(0)


def onset_env(audio, fps):
    """Per video frame n: the rise in log energy over the frame period ENDING at frame n's
    time (n / fps), i.e. the sound the picture at frame n could already have heard."""
    hop = int(round(SR / fps))
    n = len(audio) // hop
    e = (audio[: n * hop].reshape(n, hop) ** 2).mean(axis=1)
    le = np.log10(e + 1e-9)
    rise = np.maximum(np.diff(le, prepend=le[:1]), 0.0)
    # Bin k covers [k, k+1) frame periods; frame n's past period is bin n-1.
    return np.concatenate([[0.0], rise[:-1]])


def best_lag(v, a, max_lag):
    def z(x):
        s = x.std()
        return (x - x.mean()) / s if s > 1e-9 else x * 0
    v, a = z(v), z(a)
    best = (0, -9.0)
    scores = {}
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x, y = v[lag:], a[: len(a) - lag]
        else:
            x, y = v[: len(v) + lag], a[-lag:]
        m = min(len(x), len(y))
        if m < 30:
            continue
        c = float((x[:m] * y[:m]).mean())
        scores[lag] = c
        if c > best[1]:
            best = (lag, c)
    return best


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("release")
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--window", type=float, default=40.0)
    ap.add_argument("--max-lag", type=int, default=12)
    a = ap.parse_args()
    rel = json.load(open(a.release))
    files = [t["file"] if os.path.isabs(t["file"]) else os.path.join(os.path.dirname(a.release), t["file"])
             for t in sorted(rel["tracks"], key=lambda t: t.get("n", 0))]
    titles = [t.get("title", f"track {i + 1}") for i, t in enumerate(sorted(rel["tracks"], key=lambda t: t.get("n", 0)))]
    print(f"decoding {len(files)} release files ...", file=sys.stderr)
    tracks = [decode_audio(f) for f in files]
    lens = [len(t) / SR for t in tracks]
    env = onset_env(np.concatenate(tracks), a.fps)
    print("reading the picture ...", file=sys.stderr)
    mot = video_motion(a.video, a.fps)
    n = min(len(env), len(mot))
    print(f"frames: picture {len(mot)}, audio {len(env)} (album {sum(lens):.3f} s)")
    worst = 0
    at = 0.0
    rows = []
    for k, (title, L) in enumerate(zip(titles, lens)):
        res = []
        # Clear of the cut itself (the dip and the title), where both sides change at once.
        for which, (s, e) in (("start", (at + 3, at + 3 + a.window)), ("end", (at + L - 3 - a.window, at + L - 3))):
            i0, i1 = int(round(s * a.fps)), min(int(round(e * a.fps)), n)
            lag, c = best_lag(mot[i0:i1], env[i0:i1], a.max_lag)
            res.append((which, lag, c))
            if c > 0.12:
                worst = max(worst, abs(lag))
        rows.append((k + 1, title, res))
        at += L
    for k, title, res in rows:
        cells = "   ".join(f"{w}: {lag:+d} fr ({lag * 1000 / a.fps:+.0f} ms, r {c:.2f})" + ("" if c > 0.12 else " unclear") for w, lag, c in res)
        print(f"{k:2} {title[:28]:28}  {cells}")
    print(f"worst |lag| where the picture clearly follows the sound (r > 0.12): {worst} frame(s)")


if __name__ == "__main__":
    main()
