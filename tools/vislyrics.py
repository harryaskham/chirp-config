#!/usr/bin/env python3
"""Lyrics for a song's video captions, found in the song itself.

Chirpers songs sing phrases made with `chirp tts` (JSON files whose `about` holds the words and
whose notes carry phonemes). This finds where each phrase is sung in a song, by its phoneme
sequence, and prints `captions` lines ([at, seconds, text]) for a vis programme.

  vislyrics.py songs/chirpers8-t6.yaml compose/chirpers8/src/t6 [--tracks voice,singb] [--hold 1.5]
"""
import argparse
import glob
import json
import os
import re
import subprocess


def song_tracks(path, chirp):
    """Tracks with phonemes, from `chirp plan` (any song format); else JSON-per-line songs."""
    try:
        out = subprocess.run([chirp, "--json", "plan", "-f", path], capture_output=True, text=True, timeout=300)
        doc = json.loads(out.stdout)["data"]["canonical"]
        tempo = doc.get("tempo")
        bpm = float(tempo[0]["bpm"] if isinstance(tempo, list) else tempo or 120)
        tracks = {}

        def walk(ts):
            for t in ts or []:
                notes = [(float(n["at"]), float(n.get("len", 0)), n.get("ph", ""))
                         for n in t.get("notes") or [] if isinstance(n, dict) and "at" in n]
                if any(n[2] for n in notes):
                    tracks[t["name"]] = sorted(notes)
                walk(t.get("tracks"))

        walk(doc.get("tracks"))
        return tracks, bpm
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        pass
    tracks, bpm = {}, 120.0
    for line in open(path):
        if line.startswith("tempo:"):
            v = json.loads(line.split(":", 1)[1])
            bpm = float(v[0]["bpm"] if isinstance(v, list) else v)
        if line.startswith("  - {") and '"notes"' in line:
            t = json.loads(line[4:])
            notes = [(float(n["at"]), float(n.get("len", 0)), n.get("ph", ""))
                     for n in t.get("notes", []) if isinstance(n, dict) and "at" in n]
            if any(n[2] for n in notes):
                tracks[t["name"]] = sorted(notes)
    return tracks, bpm


def phrases(dirs):
    out = []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, "*.json"))):
            try:
                doc = json.load(open(f))
                notes = doc["tracks"][0]["notes"]
            except (KeyError, IndexError, ValueError, TypeError):
                continue
            m = re.search(r"\):\s*(.+)$", doc.get("about", ""))
            ph = [n.get("ph", "") for n in notes]
            if m and len(ph) >= 2 and all(ph):
                out.append((m.group(1).strip(), ph))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song")
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--tracks", default="")
    ap.add_argument("--hold", type=float, default=1.5, help="seconds a line stays after it is sung")
    ap.add_argument("--key", type=int, default=4, help="phonemes that must match when a phrase is cut short")
    ap.add_argument("--chirp", default=os.environ.get("CHIRP", "chirp"), help="chirp binary for `plan`")
    ap.add_argument("--longest", type=float, default=9.0, help="seconds a line may stay at most")
    a = ap.parse_args()
    tracks, bpm = song_tracks(a.song, a.chirp)
    want = [t for t in a.tracks.split(",") if t] or list(tracks)
    found = []
    for text, ph in phrases(a.dirs):
        # The whole phrase where it is sung whole, and its opening where it is cut short.
        for k in sorted({len(ph), min(a.key, len(ph))}, reverse=True):
            for name in want:
                notes = tracks.get(name, [])
                seq = [n[2] for n in notes]
                for i in range(len(seq) - k + 1):
                    if seq[i:i + k] == ph[:k]:
                        j = i + k - 1
                        found.append((notes[i][0], notes[j][0] + notes[j][1], text, name, k))
    # At one start, the longest phrase that matched ("nothing is kept. it only goes around."
    # over "nothing is kept.").
    found.sort(key=lambda h: (round(h[0], 1), -h[4], -len(h[2])))
    lines = []
    for at, end, text, name, k in found:
        if lines and abs(at - lines[-1][0]) < 0.1:
            continue
        # The same line on several tracks (a voice and its vocoder): keep the first.
        if lines and lines[-1][2] == text and at - lines[-1][0] < 4:
            continue
        lines.append((at, end, text, name))
    for i, (at, end, text, name) in enumerate(lines):
        secs = (end - at) * 60.0 / bpm + a.hold
        if i + 1 < len(lines):
            secs = min(secs, (lines[i + 1][0] - at) * 60.0 / bpm - 0.2)
        secs = min(secs, a.longest)
        print(f'        - [{at:g}b, {max(secs, 1.0):.1f}, {json.dumps(text.lower())}]  # {name}')


if __name__ == "__main__":
    main()
