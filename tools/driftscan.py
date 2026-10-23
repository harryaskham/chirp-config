#!/usr/bin/env python3
"""driftscan: does a song drift against its record? The windowed onset lag (tools/onsetlag.py) fitted against time.

  driftscan.py [ID …] [--all] [--mix] [-j 3] [--flag 60] [--win 4] [--step 8] [--max 250] [--keep DIR] [--json]
  driftscan.py --wav OURS.wav --ref REF.wav [--flag 60]                          # analysis only
  driftscan.py --offset [ID …] [--per-track] [--max-ms 130] [--flag-ms 15]       # whole-song offset (below)

Default IDs: the focus's climbs (climbs.json `focus`), else every enabled climb. By default it compares DRUMS WITH
DRUMS, the skill's recipe: the song's drum tracks rendered solo (a kit patch, or a track/patch named drum/kick/snare/
hat/perc/kit) against the record's htdemucs_6s drums stem. A record whose drums stem is under 10% of the stems'
energy has no percussive reference and is not measured. Full mixes mislead: parts placed on the record's own onsets
(re-strikes, onset chords) read as offsets or drift that shifting the notes only loses (chirper-zero: You and Whose
Army 'steady +110 ms' and Hunting Bears '-100 ms' both false; Pulk/Pull's drums lag 0 ms in every window).
--mix keeps the old whole-mix comparison, as leads only. Windows correlating above 0.1 give (time, lag) points;
their Theil-Sen slope (the median of pairwise slopes, robust to the +-half-beat aliases single windows show) times
the record's length is the drift. A tempo a fraction off shows as a steady slope: Pulk/Pull's tab said 97.000 BPM
against the record's 97.089, 0.17 s over the song, and fixing its tempo map was +11.4 on every seed (chirper-zero,
23 Oct). A constant offset shows as a median lag with no slope (onsetlag.py --shift, or the map's `offset`).
Flags |drift| >= --flag ms. Negative = ours early. Read-only: it never edits a song.
--offset: one whole-song lag on likeness's own onset envelope (40-band spectral flux, smoothed +-50 ms, the rhythm
term's), cross-correlated over +-MAX ms with sub-frame refinement; flags |lag| >= --flag-ms with a correlation gain
over lag 0. Parts placed on the record's onset-flux peaks (re-strikes, onset chords) sound EARLY: chirper-zero found
Like Spinning Plates -21 ms and Morning Bell/Amnesiac -43 ms, and shifting just those tracks later (+30 / +55 ms)
gained +1.9 / +4.4 on every seed. --per-track renders each track solo against the record's mix, to say which tracks to
shift (drum tracks are better judged by the default drums-vs-stem mode).
A record with little percussion (its htdemucs_6s drums stem under 10% of the stems' energy) has soft, smeared onsets
and its lags drift with them, not with our timeline: those flags print as `drift?`. Like Spinning Plates (0.6%
drums) read +170 ms, and after warping our notes by that slope it still read +142 ms (chirper-one's r4).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
import onsetlag  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def theil_sen(ts, ys):
    """Median of pairwise slopes (closed form; no least squares)."""
    s = [(ys[j] - ys[i]) / (ts[j] - ts[i]) for i in range(len(ts)) for j in range(i + 1, len(ts)) if ts[j] > ts[i]]
    return float(np.median(s)) if s else 0.0


def measure(ours, ref, win=4.0, step=8.0, mx=250):
    pts = [(t + win / 2, lag) for t, lag, corr in onsetlag.windowed_lags(ours, ref, win, step, mx) if corr > 0.1]
    if len(pts) < 4:
        return None
    ts = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    length = ts[-1] - ts[0]
    q = max(1, len(ys) // 4)
    slope = theil_sen(ts, ys)
    return {"windows": len(pts), "median_ms": float(np.median(ys)), "drift_ms": slope * length,
            "first_q_ms": float(np.median(ys[:q])), "last_q_ms": float(np.median(ys[-q:])),
            "span_s": length}


def drum_share(cid):
    """The drums stem's share (%) of the separated stems' energy, or None without stems."""
    import likeness as L
    d = os.path.join(ROOT, "ref", "stems", "htdemucs_6s", cid)
    e = {}
    for st in ("drums", "bass", "other", "vocals", "guitar", "piano"):
        f = os.path.join(d, f"{st}.wav")
        if os.path.exists(f):
            e[st] = float((L.load(f).astype(float) ** 2).mean())
    tot = sum(e.values())
    return 100.0 * e.get("drums", 0.0) / tot if tot > 0 and "drums" in e else None


PERC = 10.0   # % drums: below it, onset lags follow the record's smeared onsets, not our timeline
DRUMWORDS = ("drum", "kick", "snare", "hat", "perc", "kit", "cymbal", "tom")


_DRUM_PATCHES = None


def drum_patch_names():
    """The library's drums family (chirp presets): built-in kits like electro-kit are not inlined by chirp plan."""
    global _DRUM_PATCHES
    if _DRUM_PATCHES is None:
        r = subprocess.run([chirpbin.resolve("chirp"), "--json", "presets"], capture_output=True, text=True,
                           stdin=subprocess.DEVNULL)
        try:
            fam = json.loads(r.stdout)["data"]["patches"].get("drums") or []
            _DRUM_PATCHES = {x["name"] if isinstance(x, dict) else str(x) for x in fam}
        except (ValueError, KeyError, TypeError, AttributeError):
            _DRUM_PATCHES = set()
    return _DRUM_PATCHES


def is_kit_track(t, local):
    """A kit patch (the library's drums family, or a song-local patch defining `kit`)."""
    p = t.get("patch")
    pname = p.split()[0] if isinstance(p, str) and p.split() else ""
    pdef = local.get(pname) if pname else (p if isinstance(p, dict) else None)
    return (isinstance(pdef, dict) and "kit" in pdef) or pname in drum_patch_names()


def drum_tracks(song):
    """Names of the song's drum tracks, from `chirp plan --json`'s canonical song."""
    r = subprocess.run([chirpbin.resolve("chirp"), "plan", "-f", song, "--json"], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL)
    try:
        c = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        return []
    local = c.get("patches") or {}
    tracks = [t for t in c.get("tracks") or [] if isinstance(t, dict) and t.get("name")]
    kits = [t["name"] for t in tracks if is_kit_track(t, local)]
    # names only when the song has no kit track, and track names only (kharm plays pp-kickharm, a sine patch)
    return kits or [t["name"] for t in tracks if any(w in t["name"].lower() for w in DRUMWORDS)]


def flux_env(path):
    """likeness's onset envelope (40-band spectral flux) smoothed as its rhythm term does (5 frames, +-50 ms)."""
    import likeness as L
    return np.convolve(L.Feat(L.load(path)).onset, np.ones(5) / 5, "same")


def offset(ours, ref, max_ms=130.0, r_env=None):
    """The whole-song lag (ms; negative = ours early) maximising the flux envelopes' correlation, and the gain over 0."""
    import likeness as L
    r = flux_env(ref) if r_env is None else r_env
    o = flux_env(ours)
    n = min(len(r), len(o))
    r, o = r[:n], o[:n]
    M = max(1, int(round(max_ms / 1000 * L.FPS)))

    def corr(g):
        a, b = (r[:n - g], o[g:]) if g >= 0 else (r[-g:], o[:n + g])
        a, b = a - a.mean(), b - b.mean()
        return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
    cs = {g: corr(g) for g in range(-M, M + 1)}
    g = max(cs, key=cs.get)
    off = 0.0
    if -M < g < M:
        y0, y1, y2 = cs[g - 1], cs[g], cs[g + 1]
        den = y0 - 2 * y1 + y2
        off = float(np.clip(0.5 * (y0 - y2) / den, -0.5, 0.5)) if den else 0.0
    return {"lag_ms": (g + off) * 1000 / L.FPS, "corr": cs[g], "corr0": cs[0], "gain": cs[g] - cs[0]}


def track_names(song):
    r = subprocess.run([chirpbin.resolve("chirp"), "plan", "-f", song, "--json"], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL)
    try:
        return [t["name"] for t in json.loads(r.stdout)["data"]["canonical"]["tracks"] if t.get("name")]
    except (ValueError, KeyError, TypeError):
        return []


def scan_offset(cid, work, a):
    song = os.path.join(ROOT, "songs", f"{cid}.yaml")
    ref = os.path.join(ROOT, "ref", f"{cid}.wav")
    if not (os.path.exists(song) and os.path.exists(ref)):
        return cid, {"error": "no song or reference"}
    renders = [("", [])] + ([(n, ["--solo", n]) for n in track_names(song)] if a.per_track else [])
    r_env = flux_env(ref)
    res = {}
    for name, extra in renders:
        out = os.path.join(work, f"{cid}{'-' + name if name else ''}.wav")
        r = subprocess.run(["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song, *extra, "-o", out],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode:
            res[name or "_mix"] = {"error": f"render failed: {r.stderr.strip()[-160:]}"}
            continue
        res[name or "_mix"] = offset(out, ref, a.max_ms, r_env)
    return cid, res


def offset_row(cid, res, flag_ms):
    m = res.get("_mix", {})
    if "error" in m:
        return f"{cid:40s} {m['error']}"
    early = "  EARLY" if m["lag_ms"] <= -flag_ms and m["gain"] > 0.002 else (
        "  LATE" if m["lag_ms"] >= flag_ms and m["gain"] > 0.002 else "")
    line = f"{cid:40s} offset {m['lag_ms']:+5.0f} ms  (corr {m['corr']:.3f} vs {m['corr0']:.3f} at 0){early}"
    tr = [(k, v) for k, v in res.items() if k != "_mix" and "lag_ms" in v]
    if tr:
        line += "\n    per track: " + ", ".join(f"{k} {v['lag_ms']:+.0f}" + ("*" if abs(v["lag_ms"]) >= flag_ms
                                                                                  and v["gain"] > 0.002 else "")
                                             for k, v in tr)
    return line


def focus_ids(reg):
    f = reg.get("focus")
    enabled = [c for c in reg["climbs"] if c.get("enabled") and c.get("song")]
    if isinstance(f, str) and f.startswith("climbs:"):
        want = [x.strip() for x in f.split(":", 1)[1].split(",")]
        return [c["id"] for c in enabled if c["id"] in want]
    if isinstance(f, str) and f:
        alb = [c for c in enabled if (c.get("meta") or {}).get("album", "").lower() == f.lower()]
        return [c["id"] for c in sorted(alb, key=lambda c: (c.get("meta") or {}).get("track") or 99)]
    return [c["id"] for c in enabled]


def scan(cid, work, a):
    song = os.path.join(ROOT, "songs", f"{cid}.yaml")
    ref = os.path.join(ROOT, "ref", f"{cid}.wav")
    if not (os.path.exists(song) and os.path.exists(ref)):
        return cid, {"error": "no song or reference"}
    pct = drum_share(cid)
    cmd = ["nice", "-n", "15", chirpbin.resolve("chirp"), "render", "-f", song]
    if not a.mix:
        if pct is None:
            return cid, {"error": "no htdemucs_6s stems to compare drums with (--mix for the whole mix, leads only)"}
        if pct < PERC:
            return cid, {"error": f"no percussive reference ({pct:.1f}% drums): not measured"}
        drums = drum_tracks(song)
        if not drums:
            return cid, {"error": f"the record has drums ({pct:.0f}%) but the song has no drum track"}
        for n in drums:
            cmd += ["--solo", n]
        ref = os.path.join(ROOT, "ref", "stems", "htdemucs_6s", cid, "drums.wav")
    out = os.path.join(work, f"{cid}.wav")
    r = subprocess.run(cmd + ["-o", out], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode:
        return cid, {"error": f"render failed: {r.stderr.strip()[-200:]}"}
    m = measure(out, ref, a.win, a.step, a.max)
    if m:
        m["drums_pct"] = pct
        m["method"] = "mix" if a.mix else "drums"
    return cid, m or {"error": "too few correlated windows"}


def row(cid, m, flag):
    if "error" in m:
        return f"{cid:40s} {m['error']}"
    weak = m.get("method") == "mix" or (m.get("drums_pct") is not None and m["drums_pct"] < PERC)
    mark = ""
    if abs(m["drift_ms"]) >= flag:
        why = (f"little percussion: {m['drums_pct']:.1f}% drums" if m.get("drums_pct") is not None
               and m["drums_pct"] < PERC else "whole mix")
        mark = f"  drift? ({why}; a lead only)" if weak else "  DRIFT"
    return (f"{cid:40s} {m['windows']:4d}  median {m['median_ms']:+5.0f} ms  drift {m['drift_ms']:+6.0f} ms over "
            f"{m['span_s']:.0f} s  (first quarter {m['first_q_ms']:+.0f}, last {m['last_q_ms']:+.0f}){mark}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true", help="every enabled climb, not just the focus")
    ap.add_argument("--mix", action="store_true", help="compare whole mixes (leads only) instead of drums with drums")
    ap.add_argument("--offset", action="store_true", help="one whole-song lag on likeness's flux envelope")
    ap.add_argument("--per-track", action="store_true", help="--offset: also each track solo")
    ap.add_argument("--max-ms", type=float, default=130.0)
    ap.add_argument("--flag-ms", type=float, default=15.0)
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--flag", type=float, default=60.0)
    ap.add_argument("--win", type=float, default=4.0)
    ap.add_argument("--step", type=float, default=8.0)
    ap.add_argument("--max", type=int, default=250)
    ap.add_argument("--keep")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--wav")
    ap.add_argument("--ref")
    a = ap.parse_args(argv)
    if a.wav:
        if not a.ref:
            ap.error("--wav needs --ref")
        m = measure(a.wav, a.ref, a.win, a.step, a.max) or {"error": "too few correlated windows"}
        print(json.dumps(m) if a.json else row(os.path.basename(a.wav), m, a.flag))
        return
    with open(os.path.join(ROOT, "climbs.json")) as f:
        reg = json.load(f)
    ids = a.ids or ([c["id"] for c in reg["climbs"] if c.get("enabled") and c.get("song")] if a.all else focus_ids(reg))
    work = a.keep or tempfile.mkdtemp(prefix="driftscan-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
    os.makedirs(work, exist_ok=True)
    try:
        if a.offset:
            with ThreadPoolExecutor(max_workers=max(1, a.j)) as ex:
                res = dict(ex.map(lambda c: scan_offset(c, work, a), ids))
            if a.json:
                print(json.dumps(res, indent=1))
                return
            for cid in ids:
                print(offset_row(cid, res[cid], a.flag_ms))
            return
        with ThreadPoolExecutor(max_workers=max(1, a.j)) as ex:
            res = dict(ex.map(lambda c: scan(c, work, a), ids))
    finally:
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)
    if a.json:
        print(json.dumps(res, indent=1))
        return
    for cid in ids:
        print(row(cid, res[cid], a.flag))
    big = [c for c in ids if "drift_ms" in res[c] and abs(res[c]["drift_ms"]) >= a.flag]
    weak = [c for c in big if res[c].get("method") == "mix"
            or (res[c].get("drums_pct") is not None and res[c]["drums_pct"] < PERC)]
    sure = [c for c in big if c not in weak]
    print(f"\n{len(sure)} of {len(ids)} drift by {a.flag:g} ms or more" + (f": {', '.join(sure)}" if sure else ""))
    if weak:
        print(f"{len(weak)} more read as drift with little percussion (leads only): {', '.join(weak)}")


if __name__ == "__main__":
    main()
