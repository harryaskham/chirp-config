#!/usr/bin/env python3
"""floorfit: give a song the record's own noise floor (tape hiss, rumble), calibrated in the full mix (chirper-zero's
request: its solo-rendered probes read 8-9 dB off the level the same noise reached inside the mix).

  floorfit.py measure WAV [--bands hiss=3000-16000,rumble=20-100] [--pct 10] [--from A --to B]
      each band's floor: the --pct percentile of 100 ms frame band power (dBFS per channel; the quiet moments the
      floor shows through), and its left/right correlation (≈0 for tape hiss, ≈1 for mono hum)
  floorfit.py fit SONG REF.wav --from A --to B -o OUT [--bands …] [--pct 10] [--prefix floor] [--loud-ok] [--no-follow]
      adds, per band, a song-local patch (two noise layers panned hard left and right, so the channels are
      independent; brown noise below 300 Hz, else pink; high-pass and low-pass at the band edges) and a track playing
      it over the whole song, then calibrates each track's gain IN THE MIX: renders the song over [A, B] without the
      floor tracks (our floor M) and with them at a probe gain (F), and sets the gain whose added noise power lifts our
      floor to the record's T (gain = probe + 10 log10((T - M) / (F - M))); a final render reports what it reached.
      A band where our mix is already at or above the record's floor is left out (said so). The window must be
      one where the record goes quiet (an intro, a gap, the fade — measure helps find it): in busy music the
      quietest frames are music, not noise, so a band "floor" louder than -50 dBFS is skipped unless --loud-ok.
      The master chain (width stages, EQ) acts on the floor tracks too: the reported L/R r shows what it made of
      the independent channels.
      Each track follows the record's own floor over time (unless --no-follow): a gain lane (auto.follow) from the
      band's floor every 0.5 s over 2 s windows, only where it falls more than 3 dB under the calibrated level —
      fade-ins, fade-outs, a silent ending — never above it. Hedphelym v2's constant floor tracks ran 10-23 dB over
      the record's fade in its last 3 s and its join into Delphium fell 19.1 -> 4.7.

Only noise the record shows: measure first, and keep the result only if it scores (the album rule: tape, hiss and
wobble only from evidence). The tracks have no fades: the master's fade (if any) shapes them with the music.
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import songfmt  # noqa: E402
from likeness import SR, load  # noqa: E402

DEFAULT_BANDS = "hiss=3000-16000,rumble=20-100"
FRAME, HOPF = 4800, 2400                 # 100 ms frames, 50 ms hop


def parse_bands(spec):
    out = {}
    for item in spec.split(","):
        name, rng = item.split("=")
        lo, hi = (float(v) for v in rng.split("-"))
        out[name.strip()] = (lo, hi)
    return out


def floors(st, bands, pct=10.0):
    """{band: (floor dBFS per channel, L/R correlation)} of a stereo array."""
    n = (len(st) - FRAME) // HOPF + 1
    if n < 4:
        raise SystemExit("floorfit: the audio is shorter than a few frames")
    win = np.hanning(FRAME)
    norm = (win ** 2).sum() * FRAME / 2
    f = np.fft.rfftfreq(FRAME, 1 / SR)
    view = np.lib.stride_tricks.sliding_window_view(st, FRAME, axis=0)[::HOPF]   # frames x 2 x FRAME
    out = {}
    pw = {name: [] for name in bands}
    cross = {name: [0.0, 0.0, 0.0] for name in bands}
    for i in range(0, len(view), 512):
        X = np.fft.rfft(view[i:i + 512] * win, axis=-1)                                # frames x 2 x bins
        for name, (lo, hi) in bands.items():
            sel = (f >= lo) & (f < hi)
            P = (np.abs(X[:, :, sel]) ** 2).sum(-1) / norm                              # frames x 2
            pw[name].append(P.mean(1))
            c = X[:, 0, sel] * np.conj(X[:, 1, sel])
            cross[name][0] += float(c.real.sum())
            cross[name][1] += float((np.abs(X[:, 0, sel]) ** 2).sum())
            cross[name][2] += float((np.abs(X[:, 1, sel]) ** 2).sum())
    for name in bands:
        p = np.concatenate(pw[name])
        xc, a, b = cross[name]
        out[name] = (float(10 * np.log10(np.percentile(p, pct) + 1e-30)), float(xc / np.sqrt(a * b + 1e-30)))
    return out


def window(st, t0, t1):
    a = int((t0 or 0) * SR)
    b = int(t1 * SR) if t1 else len(st)
    return st[a:b]


def patch(lo, hi, about):
    color = "brown" if hi <= 300 else "pink"
    return {"about": about, "gain": "0dB", "play": {"gate": 1, "event_stable": True, "humanize": {"time": "0ms", "vel": 0}},
            "synth": {"amp": {"a": "5ms", "d": "0s", "s": 1, "r": "300ms"},
                      "layers": [{"name": "l", "type": "noise", "color": color, "pan": -1, "level": "-3dB"},
                                 {"name": "r", "type": "noise", "color": color, "pan": 1, "level": "-3dB"}],
                      "filters": [{"kind": "hp", "cutoff": lo, "q": 0.7}, {"kind": "lp", "cutoff": hi, "q": 0.7}]}}


def follow_lane(st, lo, hi, target_db, pct=10.0, step=0.5, span=2.0, dead=3.0, floor_db=-80.0):
    """[["Ts", dB], …] following the record's band floor where it drops more than `dead` dB under target_db (≤ 0),
    or None when it never does."""
    n = len(st) / SR
    times = np.arange(0.0, n, step)
    vals = []
    for t in times:
        seg = st[int(max(0.0, t - span / 2) * SR):int(min(n, t + span / 2) * SR)]
        vals.append(floors(seg, {"b": (lo, hi)}, pct)["b"][0] if len(seg) >= FRAME + 4 * HOPF else target_db)
    v = np.array(vals)
    v = np.array([np.median(v[max(0, i - 1):i + 2]) for i in range(len(v))])         # a 3-point median: no flicker
    rel = np.where(v < target_db - dead, np.maximum(v - target_db, floor_db), 0.0)
    if not (rel < 0).any():
        return None
    rel = np.round(rel * 2) / 2                                                       # 0.5 dB steps
    pts = [[f"{times[0]:.2f}s", float(rel[0])]]
    for i in range(1, len(rel)):
        if rel[i] != rel[i - 1]:
            if pts[-1][0] != f"{times[i - 1]:.2f}s":
                pts.append([f"{times[i - 1]:.2f}s", float(rel[i - 1])])
            pts.append([f"{times[i]:.2f}s", float(rel[i])])
    pts.append([f"{times[-1]:.2f}s", float(rel[-1])])
    return pts


def with_floor(doc, bands, gains, prefix, song_id, seconds, lanes=None):
    out = json.loads(json.dumps(doc))
    pats = out.setdefault("patches", {})
    for name, (lo, hi) in bands.items():
        if name not in gains:
            continue
        pid = f"{song_id}-{prefix}-{name}"
        pats[pid] = patch(lo, hi, f"This record's measured {name} floor ({lo:g}-{hi:g} Hz), song-local (floorfit.py).")
        tr = {"name": f"{prefix}-{name}", "patch": pid, "gain": f"{gains[name]:.2f}dB",
              "notes": [{"at": "0s", "len": f"{seconds:.3f}s", "pitch": 60, "vel": 0.8}]}
        if lanes and lanes.get(name):
            tr["gain"] = {"value": f"{gains[name]:.2f}dB", "mod": [{"src": "auto.follow", "amount": 1}]}
            tr["auto"] = {"follow": {"points": lanes[name]}}
        out["tracks"].append(tr)
    return out


def render_floors(doc, text, song, d, bands, pct, t0, t1, tag):
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(song)[1], prefix=f".floorfit-{tag}-", dir=d)
    wav = tmp + ".wav"
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(doc, indent=2) if text.lstrip().startswith("{") else songfmt.dump_yaml(doc))
        cmd = [chirpbin.resolve("chirp"), "render", "-f", tmp, "-o", wav]
        if t0 is not None:
            cmd += ["--from", f"{t0}s"]
        if t1 is not None:
            cmd += ["--to", f"{t1}s"]
        r = subprocess.run(["nice", "-n", "12", *cmd], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode or not os.path.exists(wav):
            raise SystemExit(f"floorfit: render failed: {r.stderr.strip()[-300:]}")
        return floors(load(wav), bands, pct)
    finally:
        for p in (tmp, wav):
            if os.path.exists(p):
                os.remove(p)


def main(argv):
    a = list(argv)

    def opt(k, d=None):
        if k in a:
            i = a.index(k)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return d

    if not a or a[0] not in ("measure", "fit"):
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    cmd = a.pop(0)
    bands = parse_bands(opt("--bands", DEFAULT_BANDS))
    pct = float(opt("--pct", 10))
    t0, t1 = opt("--from"), opt("--to")
    t0, t1 = (float(t0) if t0 else None), (float(t1) if t1 else None)
    if cmd == "measure":
        for name, (db, r) in floors(window(load(a[0]), t0, t1), bands, pct).items():
            print(f"{name:10s} {bands[name][0]:g}-{bands[name][1]:g} Hz  floor {db:7.1f} dBFS  L/R r {r:+.2f}")
        return
    out, prefix = opt("-o"), opt("--prefix", "floor")
    loud_ok, follow = "--loud-ok" in a, "--no-follow" not in a
    a = [x for x in a if x not in ("--loud-ok", "--no-follow")]
    if t0 is None or t1 is None:
        raise SystemExit("floorfit fit: give --from A --to B, a window where the record goes quiet (floorfit measure helps)")
    if len(a) != 2 or not out:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    song, ref = a
    text, doc = songfmt.read(song), songfmt.load(song)
    if any(t.get("name", "").startswith(prefix + "-") for t in doc.get("tracks", []) if isinstance(t, dict)):
        raise SystemExit(f"floorfit: the song already has {prefix}-* tracks (remove them or pass --prefix)")
    rs = load(ref)
    target = floors(window(rs, t0, t1), bands, pct)
    for b in list(bands):
        if target[b][0] > -50 and not loud_ok:
            print(f"{b}: the record's floor here is {target[b][0]:.1f} dBFS, louder than tape hiss or rumble sits — "
                  f"music, not noise (choose a quieter window, or --loud-ok): left out")
            bands = {k: v for k, v in bands.items() if k != b}
    if not bands:
        raise SystemExit("floorfit: no band has a noise floor in this window; nothing written")
    d = os.path.dirname(os.path.abspath(out)) or "."
    song_id = os.path.basename(song).split(".")[0].replace("-source", "")
    seconds = float(str(doc.get("length", "")).rstrip("s")) if doc.get("length") else len(rs) / SR
    probe = -20.0
    M = render_floors(doc, text, song, d, bands, pct, t0, t1, "base")
    F = render_floors(with_floor(doc, bands, {b: probe for b in bands}, prefix, song_id, seconds), text, song, d, bands,
                      pct, t0, t1, "probe")
    gains = {}
    for b in bands:
        T, m, fp = (10 ** (v[0] / 10) for v in (target[b], M[b], F[b]))
        if T <= m * 1.12:
            print(f"{b}: our mix floor {M[b][0]:.1f} dBFS is already at the record's {target[b][0]:.1f}: left out")
            continue
        if fp <= m:
            print(f"{b}: the probe did not raise our floor (check the band): left out")
            continue
        gains[b] = probe + 10 * np.log10((T - m) / (fp - m))
    if not gains:
        raise SystemExit("floorfit: no band needs a floor; nothing written")
    lanes = {}
    if follow:
        for b in gains:
            lanes[b] = follow_lane(rs, *bands[b], target[b][0], pct)
            if lanes[b]:
                low = min(v for _, v in lanes[b])
                spans, start = [], None
                for (t, v), (t2, _) in zip(lanes[b], lanes[b][1:] + [lanes[b][-1]]):
                    if v < 0 and start is None:
                        start = t
                    if v == 0 and start is not None:
                        spans.append(f"{start}-{t}")
                        start = None
                if start is not None:
                    spans.append(f"{start}-{lanes[b][-1][0]}")
                print(f"{b}: follows the record's floor down in {', '.join(spans)} (lowest {low:+.1f} dB)")
    final = with_floor(doc, bands, gains, prefix, song_id, seconds, lanes)
    got = render_floors(final, text, song, d, bands, pct, t0, t1, "check")
    for b in gains:
        print(f"{b}: record {target[b][0]:.1f} dBFS (L/R r {target[b][1]:+.2f}), ours {M[b][0]:.1f} -> {got[b][0]:.1f} "
              f"(L/R r {got[b][1]:+.2f}); track gain {gains[b]:.2f} dB")
    body = (json.dumps(final, **songfmt.json_style(song)[0]) + songfmt.json_style(song)[1]
            if text.lstrip().startswith("{") else songfmt.dump_yaml(final))
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(song)[1], prefix=".floorfit-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body)
        os.replace(tmp, out)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
