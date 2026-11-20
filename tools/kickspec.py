#!/usr/bin/env python3
"""kickspec: a bass drum alone beside the bass drums of six records, by thirds of an octave (40 Hz-8 kHz), as a
shape; with knock against thump and click against thump. chirper-one's bench of 20 Nov (Where It Was v27), moved
into tools/ at his offer; a twin of tools/snarespec.py (and of bassspec.py and cymspec.py).

  kickspec.py NAME=SOLO.wav:SONG.yaml:START_S[:TRACK] ... [--each]

SOLO.wav is a raw solo render of the kick's track (`chirp render --solo TRACK --set loudness=null --from START_S…`),
SONG.yaml the song it came from, START_S the second of the song the file begins at, TRACK the track's name (default
`kick`). The strokes are the track's own notes, placed by the song's tempo (through `chirp plan`, so a tempo map is
followed). Rows are SHAPES, each level on its own mean over 40 Hz-5 kHz: the records' median, half their range, then
each NAME less the median, its mean distance, KNOCK against thump (400 Hz-1.6 kHz less 40-125 Hz) and CLICK against
thump (2-6 kHz less 40-125 Hz), medians over the strokes. --each also prints every record less the median.

THE RECORDS' SIDE: each record's separated drum stem (ref/stems/bs_roformer_sw/ID/drums.wav), 30-90 s, at the kicks
of OUR transcription of that record (songs/ID.yaml) that no snare or tom falls within 30 ms of; the stem is lined up
with the transcription by its onsets. A stroke is read over 120 ms from 5 ms before it. CYMBALS MAY FALL WITH THOSE
KICKS: over 1.6 kHz the records' row is kick plus metal, so for the CLICK trust chirper-alpha's kickref.py, and a
stem's level is not the record's (tools/cymspec.py says how much of the top a stem loses). The cache is
ref/kickspec/records-kick.json (local).

WHAT IT SHOWED ON THE DAY IT WAS WRITTEN (the album kit's kick, Where It Was): its middle is NOT over the records'
(knock against thump -25.0; the records' stems -25.9), so a kit's "+6 dB at 500 Hz-1 kHz by part" there was a share,
not the kick's box. What the kick lacks is its chest: nothing at 90-120 Hz (chirper-alpha's finding, Take Up the
Slack): the drum is one sine at 58 Hz and the odd harmonics its drive makes. A read, not a score.
"""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snarespec as S  # noqa: E402

ROOT = S.ROOT
REFS = S.REFS
C = [40 * 2 ** (i / 3) for i in range(24)]                    # 40 Hz ... 8 kHz
LAB = "40 50 63 80 100 125 160 200 250 315 400 500 630 800 1k 1.25k 1.6k 2k 2.5k 3.15k 4k 5k 6.3k 8k".split()
NORM = [i for i, c in enumerate(C) if 39 <= c <= 5100]
SR = S.SR


def read(y, peaks):
    """(shape, knock against thump, click against thump, strokes read) over the strokes at `peaks` (s)."""
    acc = np.zeros(len(C))
    n = 1 << 15
    f = np.fft.rfftfreq(n, 1 / SR)
    knock, click = [], []
    for t in peaks:
        a = int((t - 0.005) * SR)
        seg = y[a:a + int(0.12 * SR)]
        if a < 0 or len(seg) < int(0.12 * SR):
            continue
        P = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n)) ** 2
        acc += np.array([P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum() for c in C])
        band = lambda lo, hi: 10 * np.log10(P[(f >= lo) & (f < hi)].sum() + 1e-20)  # noqa: E731
        knock.append(band(400, 1600) - band(40, 125))
        click.append(band(2000, 6000) - band(40, 125))
    if not knock:
        raise SystemExit("kickspec: no stroke found (a stroke needs 120 ms of the file after it)")
    s = 10 * np.log10(acc + 1e-20)
    return s - s[NORM].mean(), float(np.median(knock)), float(np.median(click)), len(knock)


def records(root=None, cache=None):
    """{record id: {shape, knock, click, n, lag_ms}}, cached in ref/kickspec/records-kick.json."""
    root = root or S.ROOT
    cache = cache or os.path.join(root, "ref", "kickspec", "records-kick.json")
    if os.path.exists(cache):
        with open(cache) as fh:
            return json.load(fh)
    import drumpunch as Dp
    out = {}
    for r in REFS:
        song, stem = os.path.join(root, "songs", r + ".yaml"), os.path.join(root, "ref", "stems", "bs_roformer_sw", r, "drums.wav")
        if not (os.path.exists(song) and os.path.exists(stem)):
            continue
        evs, _ = Dp.events(song)
        y = S.load(stem, 29.8, 90.2)
        e, h = S.env(S.bp(y, 150, 12000))
        train = np.zeros(len(e))
        for t, _, _ in evs:
            if 30 <= t < 90:
                train[min(len(e) - 1, int((t - 29.8) * SR / h))] = 1
        d = np.diff(e, prepend=e[0]).clip(0)
        L = int(0.1 * SR / h)
        lag = max(range(-L, L + 1), key=lambda s: float((np.roll(train, s) * d).sum())) * h / SR
        el, hl = S.env(S.bp(y, 35, 6000))
        peaks = []
        for t in Dp.clean(evs, "kick"):
            if 30.3 <= t < 89.7:
                k, w = int((t - 29.8 + lag) * SR / hl), int(0.02 * SR / hl)
                dd = np.diff(el[k - w:k + w + 2]).clip(0)
                peaks.append((k - w + int(np.argmax(dd))) * hl / SR)
        s, knock, click, n = read(y, peaks)
        out[r] = {"shape": [float(v) for v in s], "knock": knock, "click": click, "n": n, "lag_ms": 1000 * lag}
    if not out:
        raise SystemExit("kickspec: no record to read (songs/ID.yaml and ref/stems/bs_roformer_sw/ID/drums.wav)")
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache + ".new", "w") as fh:
        json.dump(out, fh)
    os.replace(cache + ".new", cache)
    return out


def track_times(song_file, track):
    """The seconds at which `track`'s notes fall in the song, by the song's own tempo (chirp plan)."""
    import chirpbin
    import drumpunch as Dp
    r = subprocess.run([chirpbin.resolve("chirp"), "plan", "-f", os.path.abspath(song_file), "--json"], capture_output=True,
                       text=True, cwd=os.path.dirname(os.path.abspath(song_file)))
    try:
        can = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"kickspec: chirp plan failed for {song_file}: {r.stderr.strip()[-200:]}")
    to_s = Dp.beats_to_seconds(can.get("tempo"))
    for t in can.get("tracks", []):
        if t.get("name") == track:
            return sorted(to_s(float(n["at"])) for n in t.get("notes") or [] if n.get("at") is not None)
    raise SystemExit(f"kickspec: no track named {track} in {song_file} (give NAME=SOLO.wav:SONG.yaml:START_S:TRACK)")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return
    R = records()
    A = np.array([v["shape"] for v in R.values()])
    med = np.median(A, 0)
    half = (A.max(0) - A.min(0)) / 2
    print(f"{'':22s}" + " ".join(f"{x:>5s}" for x in LAB) + "   dist  knock  click  strokes")
    print(f"{'the records, median':22s}" + " ".join(f"{v:5.1f}" for v in med)
          + f"         {np.median([v['knock'] for v in R.values()]):6.1f} {np.median([v['click'] for v in R.values()]):6.1f}"
          + f"  {sum(v['n'] for v in R.values())} ({len(R)} records)")
    print(f"{'half their range':22s}" + " ".join(f"{v:5.1f}" for v in half))
    if "--each" in argv:
        for r, v in R.items():
            print(f"{r[:22]:22s}" + " ".join(f"{x:+5.1f}" for x in np.array(v["shape"]) - med)
                  + f"         {v['knock']:6.1f} {v['click']:6.1f}  {v['n']}")
    for arg in argv:
        if arg.startswith("--"):
            continue
        parts = arg.split("=", 1)[1].split(":") if "=" in arg else []
        if len(parts) < 3:
            raise SystemExit("kickspec: NAME=SOLO.wav:SONG.yaml:START_S[:TRACK]")
        name, wav, song, start = arg.split("=", 1)[0], parts[0], parts[1], float(parts[2])
        y = S.load(wav)
        peaks = [t - start for t in track_times(song, parts[3] if len(parts) > 3 else "kick") if 0.01 <= t - start < len(y) / SR - 0.13]
        s, knock, click, n = read(y, peaks)
        print(f"{name[:22]:22s}" + " ".join(f"{v:+5.1f}" for v in s - med)
              + f"  {np.abs((s - med)[NORM]).mean():5.2f} {knock:6.1f} {click:6.1f}  {n}")
    print("(shapes, not levels. Over 1.6 kHz the records' row is kick plus cymbals: trust chirper-alpha's kickref.py for the "
          "click; a stem's level is not the record's.)")


if __name__ == "__main__":
    main()
