#!/usr/bin/env python3
"""partrhythm: per-bar onset match of OUR rendered parts against the record's separated stem: the rhythm term's
counterpart of partchroma (pitch content), for finding bars whose drum pattern or riff onsets differ from the record.

  partrhythm.py ID --render TRACKS [--set PATH=V …] [--song-file F] --stem FAMILY|a+b|PATH [--bars A-B] [--top 20]
                [--json]
  partrhythm.py ID --ours SOLO.wav --stem …

The onset envelope is likeness's own (spectral flux over 40 log bands at likeness.FPS, smoothed +-50 ms), so a bar
that reads badly here is one the rhythm term (weight .18) sees badly. Per bar of the map's performed clock
(tools/maps/ID.json): the correlation of ours with the stem (best of -1/0/+1 frame, as likeness allows) and the onset
energy ratio ours/stem in dB. A low correlation with a similar energy means a different pattern there (the tab's drum
or riff pattern differs from the record). The flux is level-invariant (it is taken on dB bands), so the level column
is the bar's RMS ratio ours/stem relative to the song's median ratio: far below 0 means a part missing or thin there,
far above, an extra part. Prints the mean correlation, the energy-ratio spread and the TOP worst bars. obZen, 27 Oct: rhythm
averaged 61.9 across the album (pravus 43, this-spiteful-snake 46, dancers 52), about 6.7 points of headroom.
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import microscore as MS  # noqa: E402  (render, snapshot, stem helpers)
import partchroma as PC  # noqa: E402  (the map's bar clock)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def onset_env(stereo):
    """likeness's onset envelope (spectral flux) smoothed +-50 ms, at likeness.FPS."""
    L = MS.L
    st = stereo if stereo.ndim == 2 else np.stack([stereo, stereo], 1)
    o = L.Feat(st.astype(np.float32)).onset
    return np.convolve(o, np.ones(5) / 5, "same")


def corr(a, b):
    """Pearson correlation, best of a -1/0/+1 frame shift of B; None when either side is flat."""
    best = None
    for s in (-1, 0, 1):
        x, y = (a[1:], b[:-1]) if s == 1 else (a[:-1], b[1:]) if s == -1 else (a, b)
        if len(x) < 3 or x.std() == 0 or y.std() == 0:
            continue
        c = float(np.corrcoef(x, y)[0, 1])
        best = c if best is None else max(best, c)
    return best


def bar_db(stereo, s, e, sr):
    x = stereo[int(s * sr):int(e * sr)]
    return 10 * np.log10(float((x.astype(float) ** 2).mean()) + 1e-12) if len(x) else None


def audit(ref_env, ours_env, bars, fps, b0=1, b1=10 ** 6, ref_audio=None, ours_audio=None, sr=48000):
    """Per bar: the onset correlation, and (with the audio) the RMS ratio ours/stem relative to the song's median."""
    rows = []
    for m, s, e in bars:
        if not b0 <= m <= b1:
            continue
        i0, i1 = int(s * fps), int(e * fps)
        a, b = ref_env[i0:i1], ours_env[i0:i1]
        if len(a) < 3 or len(b) < 3:
            continue
        c = corr(a, b)
        if c is None:
            continue
        row = {"bar": m, "corr": round(c, 3)}
        if ref_audio is not None and ours_audio is not None:
            lr, lo = bar_db(ref_audio, s, e, sr), bar_db(ours_audio, s, e, sr)
            if lr is not None and lo is not None and lr > -80:
                row["level_db"] = lo - lr
        rows.append(row)
    lv = [r["level_db"] for r in rows if "level_db" in r]
    med = float(np.median(lv)) if lv else 0.0
    for r in rows:
        if "level_db" in r:
            r["level_db"] = round(r["level_db"] - med, 1)
    return rows


def summary(rows, top=20):
    if not rows:
        return {"bars": 0}
    out = {"bars": len(rows), "mean_corr": round(float(np.mean([r["corr"] for r in rows])), 3),
           "worst": sorted(rows, key=lambda r: r["corr"])[:top]}
    thin = [r for r in rows if r.get("level_db", 0) <= -10]
    out["thin"] = [r["bar"] for r in thin]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("--ours")
    ap.add_argument("--render", metavar="TRACKS")
    ap.add_argument("--set", action="append", default=[], metavar="PATH=V")
    ap.add_argument("--song-file")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--stem", required=True)
    ap.add_argument("--bars")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if bool(a.ours) == bool(a.render):
        ap.error("give --ours WAV or --render TRACKS")
    MS.exit_on_term()
    bars = PC.bars_of(a.id)
    b0, b1 = (int(v) for v in a.bars.split("-")) if a.bars else (1, 10 ** 6)
    ref = MS.stem_audio(a.id, a.stem)
    if a.ours:
        ours = MS.L.load(a.ours)
    else:
        song = a.song_file or os.path.join(ROOT, "songs", f"{a.id}.yaml")
        extra = MS.solo_args(a.render) + [x for v in a.set for x in ("--set", v)]
        with MS.snapshot(song) as snap:
            ours = MS.render_window(snap, None, None, a.seed, extra)
    fps = MS.L.FPS
    s = summary(audit(onset_env(ref), onset_env(ours), bars, fps, b0, b1, ref, ours, MS.SR), a.top)
    if a.json:
        print(json.dumps(s, indent=1))
        return
    if not s["bars"]:
        print("no bars")
        return
    print(f"bars {s['bars']}  mean corr {s['mean_corr']:.2f}  bars >=10 dB thinner than usual: {len(s['thin'])}"
          + (f" ({', '.join(map(str, s['thin'][:20]))})" if s["thin"] else ""))
    print("worst: " + " ".join(f"{r['bar']}:{r['corr']:.2f}" + (f"({r['level_db']:+.0f}dB)" if "level_db" in r else "")
                               for r in s["worst"]))


if __name__ == "__main__":
    main()
