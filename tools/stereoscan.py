#!/usr/bin/env python3
"""stereoscan: which bands of our render are narrower than the record's, and has the master width stage given up on
them? (chirper-zero, Fitter Happier v2 +2.8 from stereo alone.)

  stereoscan.py [ID …] [--all] [-j 3] [--under 10] [--mono -40] [--win 10] [--min-pinned 10] [--keep DIR]
                [--renders DIR] [--json] [--mute crowd-l,crowd-r]
  stereoscan.py --wav OURS.wav --ref REF.wav [--song songs/ID.yaml]               # analysis only

Default IDs: the focus's climbs (climbs.json `focus`), else every enabled climb; each is rendered with the adopted
groove pin (nice 15), or read from --renders DIR/ID.wav when there. Per band (likeness' seven: 20-60-150-400-1.2k-
3.5k-8k-16k), side/mid in dB of the record and of our render (likeness.stereo_bands), over the whole song and per
--win s window. A band is NARROW where ours is more than --under dB under the record's (record side above -35 dB);
it is MONO where ours is also under --mono dB: its sources carry no side, and a width stage cannot widen nothing.
The song's master width lanes (wb0..wb6, tools/widthfit.py) are read too: seconds each lane sits PINNED at the
stage's maximum (6: the fit wanted more side than the stage can make, the source is mono there) or at or under
--lane-floor (0.5 default: the stage squeezing a band our sources make too wide), for --min-pinned s or more (10:
a short quiet intro whose lanes all sit at 6 is not a band the stage failed on).

Fitter Happier v1: 20-60/60-150 Hz at -53/-45 dB and 8k+ at -40 (record -21/-22/-8): a mono noise bed and a mono
fricative track, the width lanes maxed at 6 trying to widen them, every section's stereo 5-20. Fix: faint independent
L/R copies of the tracks feeding those bands (pan +-1, +7/+19 ms, -18/-10 dB) give the stage side to scale, then
`masterstack width:0.1,8` twice: 54.24 -> 57.04, +2.7..+2.8 on every seed. Read-only.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import driftscan  # noqa: E402  (focus_ids)
import likeness as L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANDS = [f"{a}-{b}" if b < 1000 else f"{a if a < 1000 else f'{a / 1000:g}k'}-{b / 1000:g}k"
         for _, a, b in L.BANDS7]
LANE_MAX = 6.0
REC_SIDE = -35.0      # a record band with less side than this is mono itself: nothing to match


def db(x):
    return 20 * np.log10(np.maximum(np.asarray(x, float), 1e-6))


def stereo(path):
    x = L.load(path)
    return x if x.ndim > 1 and x.shape[1] >= 2 else np.stack([x, x], 1)


def image(ours, ref, win=10.0, under=10.0, mono=-40.0):
    """Per band: record and render side/mid (dB) over the whole song, the share of --win s windows where ours is
    NARROW, and whether ours is MONO there."""
    n = min(len(ours), len(ref))
    ours, ref = ours[:n], ref[:n]
    whole_o, whole_r = db(L.stereo_bands(ours)), db(L.stereo_bands(ref))
    w = int(win * L.SR)
    narrow = np.zeros(7)
    count = 0
    for i in range(0, n - w // 2, w):
        o, r = db(L.stereo_bands(ours[i:i + w])), db(L.stereo_bands(ref[i:i + w]))
        narrow += (r > REC_SIDE) & (r - o > under)
        count += 1
    share = narrow / max(1, count)
    out = []
    for b in range(7):
        deficit = float(whole_r[b] - whole_o[b])
        out.append({"band": BANDS[b], "record_db": round(float(whole_r[b]), 1), "ours_db": round(float(whole_o[b]), 1),
                    "deficit_db": round(deficit, 1), "narrow_share": round(float(share[b]), 2),
                    "narrow": bool(whole_r[b] > REC_SIDE and (deficit > under or (share[b] >= 0.25 and deficit > 0))),
                    "mono": bool(whole_r[b] > REC_SIDE and whole_o[b] < mono and deficit > under)})
    return out


def _secs(t):
    t = str(t).strip()
    return float(t[:-1]) if t.endswith("s") else float(t)


def width_lanes(text):
    """{k: [(seconds, value), …]} for every master lane wbK in a song's text (JSON flow, as widthfit writes)."""
    dec = json.JSONDecoder()
    lanes = {}
    for m in re.finditer(r'"wb([0-6])"\s*:\s*', text):
        try:
            obj, _ = dec.raw_decode(text, m.end())
        except ValueError:
            continue
        pts = obj.get("points") if isinstance(obj, dict) else None
        if not pts:
            continue
        try:
            lanes[int(m.group(1))] = [(_secs(t), float(v)) for t, v in pts]
        except (TypeError, ValueError):
            continue
    return lanes


def pinned(lanes, end=None, floor=0.5):
    """Per lane: seconds at the stage maximum and at or under `floor`, and those spans ([(from, to)])."""
    out = {}
    for k, pts in sorted(lanes.items()):
        stop = max(end or 0.0, pts[-1][0])
        spans_hi, spans_lo, hi, lo = [], [], 0.0, 0.0
        for (t0, a0), (t1, a1) in zip(pts, pts[1:] + [(stop, pts[-1][1])]):
            if t1 <= t0:
                continue
            v0 = (a0 + a1) / 2          # lanes ramp linearly between knots (widthfit: 50 ms ramps at the cuts)
            for flag, spans in ((v0 >= LANE_MAX - 0.05, spans_hi), (v0 <= floor, spans_lo)):
                if not flag:
                    continue
                if spans and abs(spans[-1][1] - t0) < 0.2:
                    spans[-1] = (spans[-1][0], t1)
                else:
                    spans.append((t0, t1))
            hi += (t1 - t0) if v0 >= LANE_MAX - 0.05 else 0.0
            lo += (t1 - t0) if v0 <= floor else 0.0
        if hi > 0 or lo > 0:
            out[k] = {"band": BANDS[k], "at_max_s": round(hi, 1), "at_floor_s": round(lo, 1),
                      "max_spans": [(round(a, 1), round(b, 1)) for a, b in spans_hi],
                      "floor_spans": [(round(a, 1), round(b, 1)) for a, b in spans_lo]}
    return out


def measure(ours_path, ref_path, a, song=None):
    ours, ref = stereo(ours_path), stereo(ref_path)
    m = {"bands": image(ours, ref, a.win, a.under, a.mono), "seconds": round(len(ref) / L.SR, 1)}
    if song and os.path.exists(song):
        with open(song) as f:
            m["lanes"] = {str(k): v for k, v in pinned(width_lanes(f.read()), m["seconds"], a.lane_floor).items()}
    return m


def mute_args(names, mute):
    """chirp render --mute flags for the comma list MUTE, keeping only tracks in NAMES (chirp refuses unknown ones)."""
    return [x for t in (mute or "").split(",") if t in names for x in ("--mute", t)]


def scan(cid, work, a):
    song = os.path.join(ROOT, "songs", f"{cid}.yaml")
    ref = os.path.join(ROOT, "ref", f"{cid}.wav")
    if not (os.path.exists(song) and os.path.exists(ref)):
        return cid, {"error": "no song or reference"}
    have = os.path.join(a.renders, f"{cid}.wav") if a.renders else None
    if have and os.path.exists(have):
        out = have
    else:
        out = os.path.join(work, f"{cid}.wav")
        mute = mute_args(driftscan.track_names(song), a.mute) if a.mute else []
        r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song, *mute, "-o", out],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode:
            return cid, {"error": f"render failed: {r.stderr.strip()[-200:]}"}
    return cid, measure(out, ref, a, song)


def report(cid, m, a):
    if "error" in m:
        return f"{cid:40s} {m['error']}"
    narrow = [b for b in m["bands"] if b["narrow"]]
    lanes = {k: v for k, v in (m.get("lanes") or {}).items()
             if max(v["at_max_s"], v["at_floor_s"]) >= a.min_pinned}
    maxed = {k: v for k, v in lanes.items() if v["at_max_s"] >= a.min_pinned}
    head = (f"{cid:40s} " + ("image matches (no band more than "
                             f"{a.under:g} dB narrower)" if not narrow else
                             f"{len(narrow)} narrow band{'s' if len(narrow) > 1 else ''}") +
            (f"; width lanes maxed: {', '.join(v['band'] for v in maxed.values())}" if maxed else ""))
    lines = [head]
    for b in narrow:
        lines.append(f"    {b['band']:>9s} Hz  ours {b['ours_db']:6.1f} dB  record {b['record_db']:6.1f}  "
                     f"({b['deficit_db']:+.1f} under; narrow in {b['narrow_share'] * 100:.0f}% of {a.win:g} s windows)"
                     + ("  MONO: its sources carry no side" if b["mono"] else ""))
    for k, v in lanes.items():
        parts = []
        if v["at_max_s"] >= a.min_pinned:
            parts.append(f"at max 6 for {v['at_max_s']:.0f} s " +
                         " ".join(f"{x:.0f}-{y:.0f}" for x, y in v["max_spans"][:4]))
        if v["at_floor_s"] >= a.min_pinned:
            parts.append(f"at/under {a.lane_floor:g} for {v['at_floor_s']:.0f} s")
        lines.append(f"    lane wb{k} ({v['band']} Hz): " + "; ".join(parts))
    if any(b["mono"] for b in narrow) or maxed:
        lines.append("    fix (Fitter Happier v2 +2.8): faint independent L/R copies of the mono tracks feeding those bands "
                     "(pan +-1, +7/+19 ms, -18/-10 dB), then masterstack width:0.1,8 twice")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--under", type=float, default=10.0, help="narrower than the record by more than this (dB)")
    ap.add_argument("--mono", type=float, default=-40.0, help="our side/mid under this (dB) is a mono source")
    ap.add_argument("--win", type=float, default=10.0)
    ap.add_argument("--lane-floor", type=float, default=0.5)
    ap.add_argument("--min-pinned", type=float, default=10.0, help="report a lane pinned at least this long (s)")
    ap.add_argument("--keep")
    ap.add_argument("--renders", help="use DIR/ID.wav renders when present (e.g. a floorscan --keep dir)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--mute", help="render with these tracks muted (comma list; absent ones skipped), e.g. crowd-l,crowd-r: "
                                   "what the MUSIC alone gives the image when a noise bed supplies the side (wM, S&M)")
    ap.add_argument("--wav")
    ap.add_argument("--ref")
    ap.add_argument("--song")
    a = ap.parse_args(argv)
    if a.wav:
        if not a.ref:
            ap.error("--wav needs --ref")
        m = measure(a.wav, a.ref, a, a.song)
        print(json.dumps(m, indent=1) if a.json else report(os.path.basename(a.wav), m, a))
        return
    with open(os.path.join(ROOT, "climbs.json")) as f:
        reg = json.load(f)
    ids = a.ids or ([c["id"] for c in reg["climbs"] if c.get("enabled") and c.get("song")] if a.all
                    else driftscan.focus_ids(reg))
    work = a.keep or tempfile.mkdtemp(prefix="stereoscan-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    os.makedirs(work, exist_ok=True)
    try:
        with ThreadPoolExecutor(max_workers=max(1, a.j)) as ex:
            res = dict(ex.map(lambda c: scan(c, work, a), ids))
    finally:
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)
    if a.json:
        print(json.dumps(res, indent=1))
        return
    for cid in ids:
        print(report(cid, res[cid], a))


if __name__ == "__main__":
    main()
