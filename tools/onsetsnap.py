#!/usr/bin/env python3
"""onsetsnap: snap a tab drum part's hits to the record's drum-stem onsets (chirper-one's Dollars and Cents r6).

  onsetsnap.py SONG -o OUT [--stem DRUMS.wav] [--tracks NAME,…] [--window 160]
               [--bands low=40-150,mid=150-2000,hi=5000-12000] [--map PIECE=BAND,…] [--min-rise 2] [--dry-run]

Each hit of the drum tracks (default: the tracks on a kit patch, or named/patched drum, kick, snare, hat, perc or kit)
moves to the strongest onset of its band in the stem within +-WINDOW ms: kick -> low; snare, rim, clap and toms ->
mid; hats, cymbals and ride -> hi (a chord of pieces takes its lowest band; --map adds PIECE=BAND). Onsets are flux
peaks of the band-passed RMS (at least --min-rise dB, 40 ms apart). A hit with no onset in reach keeps its time. Times
and lengths are written in seconds.
Live drummer + tab drums, Dollars and Cents: W 80/160/320 ms gave +1.0/+1.7/+2.8 (rhythm 35 -> 47) where griddrums
and dtwgrid failed. Scan W on the ledger; snapping a bass to its stem lost (its notes were already right): drums only.
--dry-run prints how many hits would move and the median/p90 shift per band, and writes nothing.
Default stem: ref/stems/htdemucs_6s/<song id>/drums.wav. OUT keeps the source's own structure (songfmt.load; chirp
plan's canonical song only for formats songfmt cannot read) and is written by its extension: .json as JSON, anything
else as songfmt's song YAML in the source's key order. (OUT.yaml used to get JSON, and masterstack/songride then appended a second
YAML document: 'more than one document' at render, chirper-zero's Knives Out r3.) Notes tracks only.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import likeness as L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
HOP = 96
LOW = {"k", "kick", "bd", "kd", "b"}
MID = {"s", "sn", "snare", "g", "ghost", "rs", "ss", "rim", "cp", "clap", "t", "tom", "t1", "t2", "t3", "lt", "mt", "ht",
       "ft", "ft2", "st"}   # rock-kit's snares, sidestick and toms; hats, rides, crashes and china fall to hi
DRUMWORDS = ("drum", "kick", "snare", "hat", "perc", "kit", "cymbal", "tom")


def band_of(pitch, extra):
    pieces = [p.strip().lower() for p in str(pitch).split(",") if p.strip()]
    bands = [extra.get(p) or ("low" if p in LOW else "mid" if p in MID else "hi") for p in pieces]
    for b in ("low", "mid", "hi"):
        if b in bands:
            return b
    return "hi"


def onsets(y, lo, hi, min_rise):
    sos = signal.butter(4, [lo, hi], "bandpass", fs=SR, output="sos")
    z = signal.sosfilt(sos, y)
    e = np.sqrt(np.convolve(z ** 2, np.ones(240) / 240, "same"))[::HOP]
    db = 20 * np.log10(e + 1e-9)
    fl = np.maximum(np.diff(db), 0)
    pk, pr = signal.find_peaks(fl, height=min_rise, distance=int(0.04 * SR / HOP))
    return (pk + 1) * HOP / SR, pr["peak_heights"]


class Clock:
    """Beats -> seconds through a constant tempo or a map of {at: 'Nb', bpm, ramp} segments."""
    def __init__(self, tempo):
        if isinstance(tempo, (int, float)):
            self.seg = [(0.0, float(tempo), False)]
        else:
            self.seg = [(float(str(x["at"]).rstrip("b")), float(x["bpm"]), bool(x.get("ramp"))) for x in tempo]

    def __call__(self, b):
        t = 0.0
        for i, (a, bpm, ramp) in enumerate(self.seg):
            nxt = self.seg[i + 1][0] if i + 1 < len(self.seg) else float("inf")
            end = min(b, nxt)
            if ramp and nxt != float("inf"):
                b1 = self.seg[i + 1][1]
                xs = np.linspace(a, end, 65)
                bp = bpm + (b1 - bpm) * (xs - a) / (nxt - a)
                t += float(np.trapezoid(60.0 / bp, xs)) if end > a else 0.0
            else:
                t += max(0.0, end - a) * 60.0 / bpm
            if b <= nxt:
                return t
        return t


def seconds(v, clock):
    s = str(v)
    return float(s.rstrip("s")) if s.endswith("s") else clock(float(s.rstrip("b")))


def load_song(path):
    """(song dict to edit and write: the source's own structure, canonical song for tempo and drum tracks)."""
    import songfmt
    r = subprocess.run([chirpbin.resolve("chirp"), "plan", "-f", path, "--json"], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL)
    try:
        canon = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"onsetsnap: chirp plan failed for {path}: {r.stderr.strip()[-300:]}")
    try:
        return songfmt.load(path), canon
    except Exception as e:   # songfmt.Unsupported or a parse error: fall back to the canonical song
        print(f"onsetsnap: songfmt cannot read {path} ({e}); editing chirp plan's canonical song", file=sys.stderr)
        return canon, canon


def write_song(song, out):
    """By extension: .json -> JSON; anything else -> songfmt's song YAML in the source's key order (a load/dump round
    trip of a tab2song-layout song is byte-identical, so the diff shows only the moved hits). Never JSON in a .yaml."""
    import songfmt
    with open(out, "w") as f:
        if out.lower().endswith(".json"):
            json.dump(song, f, indent=1)
            f.write("\n")
        else:
            f.write(songfmt.dump_yaml(song))


def drum_tracks(canon):
    local = canon.get("patches") or {}
    out = []
    for t in canon.get("tracks") or []:
        p = t.get("patch")
        pname = p if isinstance(p, str) else ""
        pdef = local.get(pname.split()[0]) if pname else (p if isinstance(p, dict) else None)
        if (isinstance(pdef, dict) and "kit" in pdef) or any(w in f"{t.get('name', '')} {pname}".lower() for w in DRUMWORDS):
            out.append(t["name"])
    return out


def snap(song, canon, y, names, window, bands, extra, min_rise):
    clock = Clock(canon.get("tempo") or 120)   # canonical omits the default 120
    found = {b: onsets(y, lo, hi, min_rise) for b, (lo, hi) in bands.items()}
    report = {b: [] for b in bands}
    total = moved = 0
    for name in names:
        tr = next((t for t in song.get("tracks", []) if t.get("name") == name), None)
        if tr is None:
            raise SystemExit(f"onsetsnap: no track {name}")
        if not isinstance(tr.get("notes"), list):
            raise SystemExit(f"onsetsnap: track {name} has no notes list (notes tracks only)")
        new = []
        for n in tr["notes"]:
            s = seconds(n["at"], clock)
            b = band_of(n.get("pitch", ""), extra)
            ts, hs = found[b]
            i = int(np.searchsorted(ts, s))
            best = None
            for j in range(max(0, i - 3), min(len(ts), i + 4)):
                if abs(ts[j] - s) <= window and (best is None or hs[j] > hs[best]):
                    best = j
            x = dict(n)
            to = float(ts[best]) if best is not None else s
            if "len" in n and not str(n["len"]).endswith("s"):
                start_b = float(str(n["at"]).rstrip("b")) if not str(n["at"]).endswith("s") else None
                length = (clock(start_b + float(str(n["len"]).rstrip("b"))) - clock(start_b) if start_b is not None
                          else float(str(n["len"]).rstrip("b")) * 60.0 / clock.seg[0][1])
                x["len"] = f"{length:.4f}s"
            x["at"] = f"{to:.4f}s"
            if best is not None:
                moved += 1
                report[b].append(abs(to - s) * 1000)
            total += 1
            new.append(x)
        tr["notes"] = new
    return total, moved, report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song")
    ap.add_argument("-o", dest="out")
    ap.add_argument("--stem")
    ap.add_argument("--tracks")
    ap.add_argument("--window", type=float, default=160.0, help="ms (Dollars and Cents: 80/160/320 -> +1.0/+1.7/+2.8)")
    ap.add_argument("--bands", default="low=40-150,mid=150-2000,hi=5000-12000")
    ap.add_argument("--map", default="", help="extra PIECE=BAND pairs, e.g. cb=mid,tamb=hi")
    ap.add_argument("--min-rise", type=float, default=2.0)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if not a.dry_run and not a.out:
        ap.error("-o OUT (or --dry-run)")
    bands = {}
    for kv in a.bands.split(","):
        k, _, v = kv.partition("=")
        lo, _, hi = v.partition("-")
        bands[k] = (float(lo), float(hi))
    if set(bands) != {"low", "mid", "hi"}:
        ap.error("--bands needs low, mid and hi")
    extra = dict(kv.split("=", 1) for kv in a.map.split(",") if "=" in kv)
    song, canon = load_song(a.song)
    sid = os.path.splitext(os.path.basename(a.song))[0]
    stem = a.stem or os.path.join(ROOT, "ref", "stems", "htdemucs_6s", sid, "drums.wav")
    if not os.path.exists(stem):
        raise SystemExit(f"onsetsnap: no drum stem at {stem} (give --stem)")
    names = a.tracks.split(",") if a.tracks else drum_tracks(canon)
    if not names:
        raise SystemExit("onsetsnap: no drum tracks found (give --tracks)")
    y = L.load(stem)
    y = y.mean(1) if y.ndim > 1 else y
    total, moved, report = snap(song, canon, y, names, a.window / 1000, bands, extra, a.min_rise)
    print(f"onsetsnap {sid}: {moved} of {total} hits on {', '.join(names)} moved (window {a.window:g} ms)")
    for b, xs in report.items():
        if xs:
            print(f"  {b:4s} {len(xs):5d} hits  median {np.median(xs):5.1f} ms  p90 {np.percentile(xs, 90):5.1f} ms")
    if a.dry_run:
        return
    write_song(song, a.out)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
