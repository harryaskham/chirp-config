#!/usr/bin/env python3
"""width: how wide is the top end? (chirp-eco, 10 Nov, after chirper-three's finding)

chirper-three, 10 Nov: "our top end is mono; the album's genre anchors are widest there" - side/mid above 2 kHz read
-8 to -13 dB on every Accretion track against -3 to +3 dB on the anchors, with the band LEVELS on-genre. This is the
album-wide number for that, as flatness.py is for stillness: one line a track, numeric, absolute.

  width.py FILE ...                 any audio ffmpeg reads (stereo; a mono file reads "mono");
                                    FILE@START+SECONDS measures a section, e.g. a crest: t6.wav@150+32
  width.py --snap SNAPSHOT_DIR      every track of a review-app snapshot (listen.py), then the album's genre anchors
                                    (compose/ALBUM/album.json genre_refs -> ref/ID.wav) for comparison
  [--json]

Side/mid in dB for mid = (L+R)/2 and side = (L-R)/2 (chirper-three's look.py definition): 0 dB is as much side as mid
(two unrelated channels), -inf is mono. Bands: low 20-200 Hz, mid 200 Hz-2 kHz, high 2-6 kHz, air 6-16 kHz, and the
headline TOP = 2-16 kHz. Whole-file power ratios, so a wide section in a narrow song moves the number only by its
share of the energy. A flashlight, not a target: width that is one source smeared (a chorus on a mono hat) reads wide
and sounds phasey; chirper-three's recipe is independent sources left and right. Low end stays narrow on purpose.

HIGHS' SPREAD (chirper-one, 10 Nov: "highs are events over silence ... the refs' hats are noise bursts with a tail over
a floor; ours are thin ticks over black"): the mono mix above 5 kHz in 10 ms frames, frames more than 45 dB under the
99th percentile dropped, P90 - P10 in dB - his figure, taken here in 8 s windows with the median reported, so a quiet
intro against a loud crest does not count as texture. High = ticks over black; low = a floor under the events.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
SR = 44100
BANDS = (("low", 20, 200), ("mid", 200, 2000), ("high", 2000, 6000), ("air", 6000, 16000), ("top", 2000, 16000))
MONO = -99.0                      # reported for a band with no side signal at all (+99: no mid at all)


def section(arg):
    """(path, start s or None, seconds or None) of FILE or FILE@START+SECONDS (chirper-one's form)."""
    path, _, rng = arg.rpartition("@") if "@" in arg and not os.path.exists(arg) else (arg, "", "")
    if not rng:
        return arg, None, None
    t0, _, dur = rng.partition("+")
    return path, float(t0), float(dur) if dur else None


def load(arg):
    """Stereo samples (n, 2) at SR, or (n, 1) for a mono file; FILE@START+SECONDS reads that section."""
    path, t0, dur = section(arg)
    ch = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels", "-of",
                         "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    n = 1 if ch == "1" else 2
    cut = (["-ss", str(t0)] if t0 is not None else []) + (["-t", str(dur)] if dur is not None else [])
    b = subprocess.run(["ffmpeg", "-v", "error", *cut, "-i", path, "-ac", str(n), "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True).stdout
    return np.frombuffer(b, dtype=np.float32).reshape(-1, n)


def band_power(x, nfft=4096):
    """Power in each of BANDS for a mono signal (Hann STFT, half overlap), as {name: power}."""
    win = np.hanning(nfft)
    freqs = np.fft.rfftfreq(nfft, 1 / SR)
    acc = np.zeros(len(freqs))
    for i in range(0, max(1, len(x) - nfft), nfft // 2):
        seg = x[i:i + nfft]
        if len(seg) < nfft:
            break
        acc += np.abs(np.fft.rfft(seg * win)) ** 2
    return {name: float(acc[(freqs >= lo) & (freqs < hi)].sum()) for name, lo, hi in BANDS}


def measure(x):
    """{band: side/mid dB} for stereo samples (n, 2); every band MONO for a one-channel file."""
    if x.shape[1] < 2:
        return {**{name: MONO for name, _, _ in BANDS}, "spread": highs_spread(x)}
    mid, side = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2
    pm, ps = band_power(mid), band_power(side)
    out = {"spread": highs_spread(x)}
    for name, _, _ in BANDS:
        if ps[name] <= 0:
            out[name] = MONO                                   # no side at all (or silence)
        elif pm[name] <= 0:
            out[name] = -MONO                                  # no mid at all: the channels are opposite
        else:
            out[name] = float(np.clip(round(10 * float(np.log10(ps[name] / pm[name])), 1), MONO, -MONO))
    return out


def highs_spread(x, lo=5000.0, win_s=8.0, hop_s=0.01):
    """chirper-one's highs figure (see the module text): the median over WIN_S windows of P90 - P10 (dB) of the 10 ms
    frame levels above LO Hz, frames 45 dB under the file's 99th percentile dropped. None when the highs are silent."""
    m = x.mean(axis=1).astype(np.float64)
    X = np.fft.rfft(m)
    X[np.fft.rfftfreq(len(m), 1 / SR) < lo] = 0
    y = np.fft.irfft(X, len(m))
    w = int(hop_s * SR)
    k = len(y) // w
    if k < 100:
        return None
    e = 10 * np.log10((y[:k * w].reshape(k, w) ** 2).mean(1) + 1e-14)
    if np.percentile(e, 99) < -120:                            # no highs at all
        return None
    gate = np.percentile(e, 99) - 45
    n = int(win_s / hop_s)
    out = []
    for i in range(0, k - n // 2, n):
        ev = e[i:i + n]
        ev = ev[ev > gate]
        if len(ev) >= n // 20:                                 # a window with a twentieth of its frames sounding
            out.append(float(np.percentile(ev, 90) - np.percentile(ev, 10)))
    return round(float(np.median(out)), 1) if out else None


def fmt(v):
    return "mono" if v <= MONO else f"{v:+.1f}"


def line(label, w):
    sp = w.get("spread")
    return (f"{label}: top (2-16 kHz) {fmt(w['top'])} dB  [high 2-6k {fmt(w['high'])}, air 6-16k {fmt(w['air'])}; "
            f"mid 200-2k {fmt(w['mid'])}, low {fmt(w['low'])}]" + (f"  highs' spread {sp:.1f} dB" if sp is not None else ""))


def anchors(album_id):
    """[(id, widths)] of the album's genre anchors that are on disk."""
    try:
        with open(os.path.join(ROOT, "compose", album_id, "album.json")) as f:
            refs = json.load(f).get("genre_refs") or []
    except (OSError, ValueError):
        return []
    out = []
    for r in refs:
        p = os.path.join(ROOT, "ref", r + ".wav")
        if os.path.exists(p):
            out.append((r, measure(load(p))))
    return out


def snapshot(snap_dir):
    """{album, tracks: [{n, title, width}], anchors: [{id, width}], anchor_top: [lo, median, hi]} for a snapshot."""
    with open(os.path.join(snap_dir, "snapshot.json")) as f:
        meta = json.load(f)
    tracks = [{"n": t["n"], "title": t.get("title", ""), "width": measure(load(os.path.join(snap_dir, f"t{t['n']:02d}.mp3")))}
              for t in meta["tracks"] if os.path.exists(os.path.join(snap_dir, f"t{t['n']:02d}.mp3"))]
    anc = [{"id": i, "width": w} for i, w in anchors(meta["album"])]
    tops = sorted(a["width"]["top"] for a in anc if a["width"]["top"] > MONO)
    sps = sorted(a["width"]["spread"] for a in anc if a["width"].get("spread") is not None)
    return {"album": meta["album"], "snapshot": meta.get("id"), "tracks": tracks, "anchors": anc,
            "anchor_top": [tops[0], float(np.median(tops)), tops[-1]] if tops else None,
            "anchor_spread": [sps[0], float(np.median(sps)), sps[-1]] if sps else None}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--snap", metavar="SNAPSHOT_DIR")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.snap:
        r = snapshot(a.snap)
        if a.json:
            print(json.dumps(r, indent=1))
            return 0
        at = r["anchor_top"]
        print(f"width as heard, {r['album']} {r['snapshot'] or ''}: side/mid in dB (0 = as much side as mid)"
              + (f"; genre anchors' top {at[0]:+.1f} to {at[2]:+.1f}, median {at[1]:+.1f}" if at else "")
              + (f"; their highs' spread {r['anchor_spread'][0]:.1f} to {r['anchor_spread'][2]:.1f}, median "
                 f"{r['anchor_spread'][1]:.1f}" if r.get("anchor_spread") else ""))
        for t in r["tracks"]:
            print("  " + line(f"t{t['n']} {t['title']}", t["width"]))
        for x in r["anchors"]:
            print("  " + line(f"anchor {x['id']}", x["width"]))
        return 0
    if not a.files:
        ap.error("give FILEs or --snap SNAPSHOT_DIR")
    res = [{"file": f, "width": measure(load(f))} for f in a.files]
    print(json.dumps(res, indent=1) if a.json else "\n".join(line(r["file"], r["width"]) for r in res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
