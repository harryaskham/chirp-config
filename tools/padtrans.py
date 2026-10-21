#!/usr/bin/env python3
"""padtrans: transcribe a sustained chord pad from a stem (chirper-zero's Ptolemy r16 prototype, made a tool).

  padtrans.py STEM.wav --from A --to B [--win 0.5] [--floor -45] [--voices 3] [--range 120-1500] [--within 12]
              [--a4 440] [--json]                                  print the notes
  padtrans.py STEM.wav --from A --to B … --into SONG --track NAME [--patch P] -o OUT
              write them into SONG: TRACK's notes starting in [A, B) are replaced (a notes track; songfmt notes
              converts a score track), or a new track on --patch; written in SONG's format, planned by chirp

Per --win window: a window quieter than --floor dBFS is silence; otherwise the power of a long FFT in --range Hz
is summed per semitone (MIDI, at --a4) and the strongest notes with distinct pitch classes, up to --voices, within
--within dB of the strongest form the chord. Consecutive windows with the same chord merge into one run (one note per
chord tone), its velocity from the run's level. On Ptolemy's vocals-stem pad chirper-zero measured 82-88 pitch
accuracy (noteacc); a long FFT's partials can still add a fifth or octave that is not played, so audition the result
(audition.py) and keep it only if it scores.
"""
import json
import os
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from likeness import SR, load  # noqa: E402

NF = 1 << 17


def chords(x, t0, t1, win=0.5, floor=-45.0, voices=3, lo=120.0, hi=1500.0, within=12.0, a4=440.0):
    """[(start s, chord tuple of MIDI notes or None, level dB)] per window."""
    f = np.fft.rfftfreq(NF, 1 / SR)
    band = (f >= lo) & (f <= hi)
    midi = np.round(12 * np.log2(f[band] / a4) + 69).astype(int)
    out = []
    t = t0
    while t < t1 - 1e-9:
        z = x[int(t * SR):int(min(t + win, t1) * SR)]
        lv = float(10 * np.log10(np.mean(z ** 2) + 1e-20)) if len(z) else -200.0
        if lv < floor or len(z) < 64:
            out.append((t, None, lv))
            t += win
            continue
        p = (np.abs(np.fft.rfft(z * np.hanning(len(z)), NF)) ** 2)[band]
        e = np.bincount(midi - midi.min(), weights=p)
        order = np.argsort(e)[::-1]
        mx, sel, pcs = e[order[0]], [], set()
        for i in order:
            if e[i] < mx * 10 ** (-within / 10):
                break
            m = int(i + midi.min())
            if m % 12 in pcs:
                continue
            sel.append(m)
            pcs.add(m % 12)
            if len(sel) == voices:
                break
        out.append((t, tuple(sorted(sel)) if sel else None, lv))
        t += win
    return out


def runs(wins, t1, win):
    """Merge consecutive equal chords → notes [{at, len, pitch, vel}] (seconds)."""
    notes, cur = [], None
    for t, c, lv in wins + [(t1, None, -200.0)]:
        if cur and c == cur[1]:
            cur[2] = min(t + win, t1)
            cur[3].append(lv)
            continue
        if cur:
            vel = round(float(np.clip(0.5 + (np.mean(cur[3]) + 25) / 30, 0.2, 1.0)), 3)
            for m in cur[1]:
                notes.append({"at": f"{cur[0]:.3f}s", "len": f"{cur[2] - cur[0]:.3f}s", "pitch": m, "vel": vel})
        cur = [t, c, min(t + win, t1), [lv]] if c else None
    return notes


def main(argv):
    a = list(argv)

    def opt(k, d=None):
        if k in a:
            i = a.index(k)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return d

    t0, t1 = opt("--from"), opt("--to")
    if t0 is None or t1 is None:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    t0, t1 = float(t0.rstrip("s")), float(t1.rstrip("s"))
    lo, hi = (float(v) for v in opt("--range", "120-1500").split("-"))
    kw = dict(win=float(opt("--win", 0.5)), floor=float(opt("--floor", -45)), voices=int(opt("--voices", 3)), lo=lo, hi=hi,
              within=float(opt("--within", 12)), a4=float(opt("--a4", 440)))
    into, track, patch, out = opt("--into"), opt("--track"), opt("--patch"), opt("-o")
    as_json = "--json" in a
    a = [v for v in a if v != "--json"]
    if len(a) != 1:
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    x = load(a[0]).mean(1).astype(np.float64)
    notes = runs(chords(x, t0, t1, **kw), t1, kw["win"])
    if not into:
        print(json.dumps(notes) if as_json else "\n".join(f"{n['at']:>10} {n['len']:>9}  {n['pitch']:3d}  vel {n['vel']}" for n in notes))
        return
    import songfmt
    if not track or not out:
        raise SystemExit("padtrans: --into SONG needs --track NAME and -o OUT")
    text, doc = songfmt.read(into), songfmt.load(into)
    tr = next((t for t in doc.get("tracks", []) if isinstance(t, dict) and t.get("name") == track), None)
    if tr is not None:
        if not isinstance(tr.get("notes"), list):
            raise SystemExit(f"padtrans: {track!r} is not a notes track (songfmt.py notes converts a score track)")
        def sec(n):
            v = str(n["at"])
            if v.endswith("b"):
                raise SystemExit(f"padtrans: {track!r} has notes in beats; replace by hand or convert")
            return float(v.rstrip("s"))
        keep = [n for n in tr["notes"] if not (t0 <= sec(n) < t1)]
        tr["notes"] = sorted(keep + notes, key=sec)
    else:
        if not patch:
            raise SystemExit(f"padtrans: no track {track!r}: pass --patch P to add one")
        doc["tracks"].append({"name": track, "patch": patch, "notes": notes})
    body = (json.dumps(doc, **songfmt.json_style(into)[0]) + songfmt.json_style(into)[1] if text.lstrip().startswith("{")
            else songfmt.dump_yaml(doc))
    d = os.path.dirname(os.path.abspath(out)) or "."
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(into)[1], prefix=".padtrans-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body)
        songfmt.plan_hash(tmp)
        os.replace(tmp, out)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    print(f"wrote {out}: {len(notes)} pad notes in {t0:g}-{t1:g} s on {track}")


if __name__ == "__main__":
    main(sys.argv[1:])
