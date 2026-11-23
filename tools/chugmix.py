#!/usr/bin/env python3
"""chugmix: THE CHUG IN THE MIX: what the low end does under a guitar stroke, on the record itself. (chirper-zero,
Common Time, 23 Nov 2026.)

  chugmix.py wavs --song SONG.yaml --tracks gl,gr --from SECONDS LABEL=FILE.wav ...
  chugmix.py records [--scan] [ID ...]

THE MEASURE is riffpunch's `tight_db`, the low end's fall: 100-250 Hz in a stroke's first 20 ms over its 40-80 ms,
the median over the clean onsets. POSITIVE = the low end has died by 40-80 ms. riffpunch reads it on a guitar
alone, against six records' separated guitar stems. Two things that needed saying about that yardstick:

  1. IT HANGS ON WHERE THE STROKE IS SAID TO BEGIN. On a stem it moves 0.03 to 0.44 dB for every millisecond the
     onset is early or late (`records --scan`). riffpunch-records.json was read at our transcriptions' onsets with
     no lag: -1.10 (-2.2 .. +0.3). Read where the record itself says the strokes begin (the lag in +-16 ms at
     which the record's own 150 Hz-8 kHz jumps most at those onsets) the same stems give -0.07 (-0.46 .. +0.60).
     So: THE RECORDS' GUITAR HOLDS ITS LOW END LEVEL THROUGH THE STROKE, within half a dB. A song's guitar is
     read at its written note, where the string starts, so it needs no lag.
  2. A GUITAR ALONE IS NOT WHAT IS HEARD. On the record itself (no separator) the low end at a guitar stroke
     FALLS, because the bass drum strikes with it:

         the record itself   +2.89   (+2.38 .. +4.46)     <- the yardstick for a song's MIX
         its guitar stem     -0.07   (-0.46 .. +0.60)
         its bass stem       -0.25   (-2.17 .. +0.43)
         guitar + bass       -0.14   (-1.00 .. +0.56)
         its drums stem     +10.36   (+7.52 .. +13.33)

     (six records, 30-90 s of each, 184 to 582 strokes; bleed, combustion, electric-red, obzen, pravus,
     the-faultless.) A mix that falls further than +4.5 at its chugs has more bass drum on the stroke's front
     than held low end after it: look at the bass drum's 120-250 Hz alone (kickref: the records -13.4 against the
     drum's low band), the guitars' `thump`, and whether the bass's own low band holds (the records' does).

`wavs` reads files you have rendered, all beginning at --from seconds of the song: solos and the mix, e.g.
  chirp render -f SONG.yaml --seed 1 --set loudness=null --from 17.8s --to 35.6s --preroll 5 [--solo T ...] -o X.wav
at the written strokes of --tracks (doubles merged, clean onsets, as riffpunch's). Each file's fall, and its low
band's level at 40-80 ms against the last file's (or the one labelled `mix`): who holds the low end once the stroke
has landed. `records` re-reads the table above from ref/ and the stems (no render); `--scan` shows the fall at
onsets shifted -16 .. +16 ms on each record's guitar stem and on the record itself.

First readings (raw mixes): Common Time riff C at the wall rig's strokes +8.39 (the wall alone +3.17, the bass
+2.25, the bass drum +12.86); Odd Sympathy in step +7.76 at v42, +6.67 at v43, 'against' +5.17 -> +4.83.
"""
import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import drumpunch as D  # noqa: E402
import likeness as L  # noqa: E402
import riffpunch as R  # noqa: E402

SR = L.SR
# the six records, read on 23 Nov 2026 (`chugmix.py records`): lag ms, guitar, bass, drums, guitar + bass, the record
RECORDS = {"bleed": (2, -0.46, -1.37, 12.58, -1.00, 2.86), "combustion": (-8, -0.11, -0.46, 12.52, -0.09, 4.46),
           "electric-red": (-14, 0.09, 0.43, 7.59, 0.23, 2.38), "obzen": (-8, 0.60, -0.04, 13.33, -0.20, 3.28),
           "pravus": (-4, -0.18, 0.00, 8.19, 0.56, 2.91), "the-faultless": (-14, -0.04, -2.17, 7.52, -0.95, 2.59)}


def stroke(y, t):
    """(the low band's rms in the stroke's first 20 ms, in its 40-80 ms), as riffpunch.measure_note; None at an edge."""
    s0 = int(t * SR)
    seg = y[max(0, s0 - int(0.005 * SR)):s0 + int(0.09 * SR)]
    if s0 < int(0.005 * SR) or len(seg) <= int(0.09 * SR):
        return None
    lo = D.bandpass(seg, 100, 250)
    e = lambda a, b: float(np.sqrt(np.mean(lo[int(a * SR):int(b * SR)] ** 2)) + 1e-12)  # noqa: E731
    return e(0.005, 0.025), e(0.045, 0.085)


def fall(y, ts):
    """(the median fall in dB, the median level at 40-80 ms in dB, strokes read)."""
    r = [p for p in (stroke(y, t) for t in ts) if p]
    if not r:
        return float("nan"), float("nan"), 0
    return (float(np.median([20 * np.log10(a / b) for a, b in r])), float(np.median([20 * np.log10(b) for a, b in r])), len(r))


def jump(yb, ts):
    """How far a 150 Hz-8 kHz signal jumps at the onsets: its 15 ms after over the 25..5 ms before, dB, the median."""
    v = []
    for t in ts:
        a, b = int(t * SR), int((t - 0.025) * SR)
        if b >= 0 and a + 720 <= len(yb):
            v.append(10 * np.log10((np.mean(yb[a:a + 720] ** 2) + 1e-14) / (np.mean(yb[b:b + 960] ** 2) + 1e-14)))
    return float(np.median(v)) if v else -99.0


def records(ids, scan):
    tab = R.records_table()
    rows = []
    print(f"{'record':16s} {'n':>4s} {'lag ms':>6s} | {'guitar':>7s} {'bass':>7s} {'drums':>7s} {'g+b':>7s} {'RECORD':>7s} | "
          "at 40-80 ms, dB under the record's own low band: guitar bass drums")
    for i in ids or list(RECORDS):
        ts, _ = R.guitar_events(os.path.join(ROOT, "songs", f"{i}.yaml"))
        cts = [t for t in R.clean(ts) if 30 <= t < 90]
        n = int(96 * SR)
        st = {p: D.mono(R.ref_audio(i, p))[:n] for p in ("guitar", "bass", "drums")}
        mix = D.mono(L.load(os.path.join(ROOT, "ref", f"{i}.wav")))[:n]
        mb = D.bandpass(mix, 150, 8000)
        sh = max((x / 1000 for x in range(-16, 17, 2)), key=lambda s: jump(mb, [t + s for t in cts]))
        t2 = [t + sh for t in cts]
        m = min(len(mix), *(len(x) for x in st.values()))
        g, b, d = (st[p][:m] for p in ("guitar", "bass", "drums"))
        f = {k: fall(y, t2) for k, y in (("g", g), ("b", b), ("d", d), ("gb", g + b), ("m", mix[:m]))}
        rows.append([f[k][0] for k in ("g", "b", "d", "gb", "m")])
        print(f"{i:16s} {f['m'][2]:4d} {sh * 1000:+6.0f} | {f['g'][0]:+7.2f} {f['b'][0]:+7.2f} {f['d'][0]:+7.2f} {f['gb'][0]:+7.2f} "
              f"{f['m'][0]:+7.2f} | {f['g'][1] - f['m'][1]:+6.1f} {f['b'][1] - f['m'][1]:+6.1f} {f['d'][1] - f['m'][1]:+6.1f}", flush=True)
        if scan:
            for lab, y in (("guitar stem", g), ("the record", mix[:m])):
                v = [fall(y, [t + s / 1000 for t in cts])[0] for s in range(-16, 17, 4)]
                was = f" ; riffpunch-records.json has {tab[i]['tight_db']:+.2f}" if i in tab and lab == "guitar stem" else ""
                print(f"    {lab:12s} by onset -16 .. +16 ms: " + " ".join(f"{x:+.1f}" for x in v) + f"   ({(v[5] - v[3]) / 8:+.2f} dB a ms round 0{was})", flush=True)
    r = np.array(rows)
    if len(r) > 1:
        md, lo, hi = np.median(r, 0), r.min(0), r.max(0)
        print(f"{'MEDIAN':16s} {'':4s} {'':6s} | " + " ".join(f"{x:+7.2f}" for x in md))
        print(f"{'lowest':16s} {'':4s} {'':6s} | " + " ".join(f"{x:+7.2f}" for x in lo))
        print(f"{'highest':16s} {'':4s} {'':6s} | " + " ".join(f"{x:+7.2f}" for x in hi))


def wavs(song, tracks, t0, files):
    ts, found = R.guitar_events(song, tracks, by_chain=True)
    if not found:
        raise SystemExit(f"chugmix: none of {','.join(tracks)} in {song}")
    res = {}
    for a in files:
        lab, p = a.split("=", 1)
        y = D.mono(L.load(p))
        dur = len(y) / SR
        res[lab] = fall(y, [t - t0 for t in R.clean(ts) if 0.03 < t - t0 < dur - 0.2])
    ref = res.get("mix") or list(res.values())[-1]
    md = np.median(np.array(list(RECORDS.values())), 0)
    print(f"chugmix {os.path.basename(song)} from {t0:g} s, at the strokes of {','.join(found)}")
    for lab, (f, lv, n) in res.items():
        print(f"  {lab:28s} {n:4d} strokes ; fall {f:+6.2f} ; its low band at 40-80 ms {lv - ref[1]:+6.1f} dB against the reference's")
    print(f"  the records: the record itself {md[5]:+.1f} ({min(v[5] for v in RECORDS.values()):+.1f} .. {max(v[5] for v in RECORDS.values()):+.1f}) ; "
          f"guitar {md[1]:+.1f} ; bass {md[2]:+.1f} ; guitar + bass {md[4]:+.1f} ; drums {md[3]:+.1f}  (positive = the low end has died by 40-80 ms)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("wavs")
    w.add_argument("--song", required=True)
    w.add_argument("--tracks", required=True)
    w.add_argument("--from", dest="t0", type=float, required=True)
    w.add_argument("files", nargs="+", metavar="LABEL=FILE.wav")
    r = sub.add_parser("records")
    r.add_argument("--scan", action="store_true")
    r.add_argument("ids", nargs="*")
    a = ap.parse_args(argv)
    if a.cmd == "records":
        records(a.ids, a.scan)
    else:
        wavs(a.song, a.tracks.split(","), a.t0, a.files)


if __name__ == "__main__":
    main()
