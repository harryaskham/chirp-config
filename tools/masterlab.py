#!/usr/bin/env python3
"""masterlab: try master chains on a song in 40 s a try instead of a full render each (chirper-three, 10 Nov).

  masterlab.py RAW.wav --try VARIANTS.json [--song songs/ID.yaml] [--score ID] [--sections name:sec,…]
               [--volume DB] [--loudness -11] [--keep DIR]

RAW is the song rendered with `--set loudness=null` (what limwork.py calls RAW: the mix as the song's master chain
leaves it). masterlab plays that file back through the engine as two `input` tracks (left and right, hard-panned)
with ONLY the stages under test on the master, once without loudness and once with it, and reports for each try:

  - limwork.py's table (how much the final limiter is doing, by section),
  - short-term loudness by section against the song as it is (the pass-through, run first),
  - the tone against the pass-through, in bands, for the first, the loudest and the last section,
  - compscore's total, both seams and the section counts when --score ID --song FILE are given.

VARIANTS.json is a list of tries: [{"name": "tape + glue", "fx": [{"type": "tape", "drive": 0.33, "warmth": 0},
{"type": "glue", "threshold": "-27dB"}], "auto": {…lanes for those fx…}, "loudness_clip": "2.5dB"}, …]. The fx are
the stages you would APPEND to the song's master (everything already in it is baked into RAW). Lanes are in the
harness's own time: its tempo is 60, so one beat is one second ("257.7b" is 4:17.7).

Why it is exact: a master chain only sees the stereo mix, so a recording of the mix is as good as the mix. The
harness's finished file correlates 0.9999 with the real render's (it sits 72 samples later: the input path), and its
limiter table matched the real render's line for line on t4 (crest -0.6 dB / 22% / 2% in both).

The one trap (it cost a round): the config's master volume, -3 dB by default, sits AFTER the master effects. A song
without `volume: 0dB` therefore shows a RAW file 3 dB under what its master effects see, and a harness that ignores
this drives a tape or a glue 3 dB harder or softer than the song will. masterlab reads the song's `volume` (--song,
or --volume DB) and feeds the stages at the level the song does. Thresholds read off a RAW file with a meter are
3 dB low for such a song.

Not a score and not an ear. Read-only on the song; its scratch songs live in songs/ as .masterlab-*.yaml for the
length of a render and are removed.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EDGES = [30, 60, 120, 250, 500, 1000, 2000, 4000, 6000, 8000, 11000, 14000, 18000]


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def duration(path):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(r.stdout.strip())


def song_volume(song):
    """The song's master volume in dB: its `volume:` when it has one, else the config default (-3 dB)."""
    try:
        m = re.search(r'^\s*"?volume"?\s*:\s*"?(-?[\d.]+)\s*dB', open(song).read(), re.M)
    except OSError:
        m = None
    return float(m.group(1)) if m else -3.0


def load(path, t0, dur, ch=1, sr=48000):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t0), "-t", str(dur), "-i", path, "-ac", str(ch),
                          "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, ch).astype(np.float64)


def bands(path, t0, dur):
    x = load(path, t0, dur)[:, 0]
    n = 8192
    k = len(x) // n
    if k < 1:
        return np.zeros(len(EDGES) - 1)
    s = (np.abs(np.fft.rfft(x[:k * n].reshape(k, n) * np.hanning(n), axis=1)) ** 2).mean(0)
    f = np.fft.rfftfreq(n, 1 / 48000)
    return np.array([10 * np.log10(s[(f >= a) & (f < b)].sum() + 1e-20) for a, b in zip(EDGES[:-1], EDGES[1:])])


def section_loudness(path, marks):
    r = sh(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"]).stderr
    st = [(float(m.group(1)), float(m.group(2))) for m in re.finditer(r"t:\s*([\d.]+)\s+TARGET.*?S:\s*(-?[\d.]+)", r)]
    out = {}
    for (name, t0), (_, t1) in zip(marks, marks[1:] + [("end", 1e9)]):
        v = [s for t, s in st if t0 + 3 <= t < t1 and s > -60]
        out[name] = sum(v) / len(v) if v else float("nan")
    return out


class Lab:
    def __init__(self, raw, pin, volume, loudness, keep):
        self.pin, self.volume, self.loudness = pin, volume, loudness
        self.dir = keep or tempfile.mkdtemp(prefix="masterlab-")
        os.makedirs(self.dir, exist_ok=True)
        self.dur = duration(raw)
        self.l, self.r = os.path.join(self.dir, "raw-l.wav"), os.path.join(self.dir, "raw-r.wav")
        r = sh(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-filter_complex",
                "[0:a]channelsplit=channel_layout=stereo[l][r]", "-map", "[l]", "-c:a", "pcm_f32le", self.l,
                "-map", "[r]", "-c:a", "pcm_f32le", self.r])
        if r.returncode:
            sys.exit(f"masterlab: cannot split {raw}: {r.stderr[-300:]}")

    def run(self, tag, fx, auto=None, clip=None):
        out = {}
        gain = f"{-self.volume:g}dB"
        for kind in ("raw", "final"):
            master = {"fx": fx}
            if auto:
                master["auto"] = auto
            song = {"tempo": 60, "tail": "0s", "volume": f"{self.volume:g}dB",
                    "tracks": [{"name": "l", "input": "rawl", "pan": -1, "gain": gain},
                               {"name": "r", "input": "rawr", "pan": 1, "gain": gain},
                               {"name": "len", "patch": "sub-sine", "score": f"R/{self.dur:.3f}b"}],
                    "master": master}
            if kind == "final":
                song["loudness"] = self.loudness
                if clip:
                    song["loudness_clip"] = clip
            name = f".masterlab-{os.getpid()}-{tag}-{kind}.yaml"
            path = os.path.join(ROOT, "songs", name)
            wav = os.path.join(self.dir, f"{tag}-{kind}.wav")
            with open(path, "w") as f:
                json.dump(song, f)
            try:
                r = sh([self.pin, "render", "-f", name, "-o", wav, "--input", f"rawl={self.l}", "--input",
                        f"rawr={self.r}", "--threads", "3"], cwd=os.path.join(ROOT, "songs"), timeout=1800)
            finally:
                os.remove(path)
            if r.returncode:
                sys.exit(f"masterlab: {tag}: {r.stderr.strip()[-400:]}")
            out[kind] = wav
        return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("raw")
    ap.add_argument("--try", dest="tries", required=True, help="JSON file: a list of {name, fx, auto?, loudness_clip?}")
    ap.add_argument("--song", help="the song the RAW render came from (for its volume and for --score)")
    ap.add_argument("--score", metavar="ID", help="also run compscore as this album track (needs --song)")
    ap.add_argument("--sections", default="", help="name:seconds,… in order (limwork's form)")
    ap.add_argument("--volume", type=float, help="the song's master volume in dB (default: read from --song, else -3)")
    ap.add_argument("--loudness", type=float, default=-11.0)
    ap.add_argument("--keep", metavar="DIR", help="keep the rendered files here")
    a = ap.parse_args()
    if a.score and not a.song:
        sys.exit("masterlab: --score needs --song")
    pin = open(os.path.join(HERE, "groove-pin")).read().strip()
    volume = a.volume if a.volume is not None else (song_volume(a.song) if a.song else -3.0)
    tries = json.load(open(a.tries))
    lab = Lab(a.raw, pin, volume, a.loudness, a.keep)
    marks = [(n, float(t)) for n, t in (x.split(":") for x in a.sections.split(",") if x)] or [("whole", 0.0)]
    print(f"masterlab: {os.path.basename(a.raw)} ({lab.dur:.0f} s), master volume {volume:g} dB, files in {lab.dir}")

    def report(name, out, base):
        lw = sh([sys.executable, os.path.join(HERE, "limwork.py"), out["raw"], out["final"]] +
                ([a.sections] if a.sections else [])).stdout.strip().split("\n")
        lv = section_loudness(out["final"], marks)
        print(f"\n== {name}\n   {lw[0] if lw else ''}")
        for line in lw[1:]:
            n = line.split()[0] if line.split() else ""
            extra = ""
            if n in lv:
                extra = f"   S {lv[n]:6.1f} LUFS" + (f" ({lv[n] - base['lv'][n]:+.1f})" if base else "")
            print("  " + line.rstrip()[:70] + extra)
        if base:
            for n, t0, dur in base["spans"]:
                d = bands(out["final"], t0, dur) - base["tone"][n]
                print(f"   tone, {n:<8} {EDGES[0]}..{EDGES[-1]} Hz: " + " ".join(f"{v:+.1f}" for v in d))
        if a.score:
            r = sh([sys.executable, os.path.join(HERE, "compscore.py"), a.score, out["final"], "--song", a.song],
                   cwd=ROOT, timeout=1200).stdout.strip().split("\n")[-1]
            try:
                d = json.loads(r)
                fl = d["detail"].get("flow", {})
                seams = "  ".join(f"{s} {fl[s]['spectral_db']} / {fl[s].get('level_jump_db')}" for s in ("in", "out")
                                  if s in fl)
                print(f"   compscore {d['total']}   seams (tone / level): {seams}   sections "
                      f"{d['detail']['recurrence']['ensemble']['sections']}")
            except (ValueError, KeyError):
                print(f"   compscore: {r[:200]}")
        return lv

    out = lab.run("pass", [])
    lv = report("pass-through (the song as it is)", out, None)
    order = [n for n, _ in marks]
    ends = dict(zip(order, [t for _, t in marks[1:]] + [lab.dur]))
    starts = dict(marks)
    pick = [order[0], max(order, key=lambda n: lv[n] if lv[n] == lv[n] else -99), order[-1]]
    spans = []
    for n in dict.fromkeys(pick):
        t0 = starts[n] + 3
        spans.append((n, t0, max(4.0, min(30.0, ends[n] - t0 - 1))))
    base = {"lv": lv, "spans": spans, "tone": {n: bands(out["final"], t0, dur) for n, t0, dur in spans}}
    for i, t in enumerate(tries):
        out = lab.run(f"try{i}", t["fx"], t.get("auto"), t.get("loudness_clip"))
        report(t.get("name", f"try {i}"), out, base)


if __name__ == "__main__":
    main()
