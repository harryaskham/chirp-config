#!/usr/bin/env python3
"""partchroma: per-bar pitch-class match of OUR rendered part against the record's separated stem (chirper-one's
Immutable audit, promoted). tools/barchroma.py checks a TAB's notes against a stem; this checks the SOUND we render.

  partchroma.py ID --render TRACKS [--set PATH=V …] [--song-file F] --stem FAMILY|a+b|PATH [--lo 60 --hi 600]
                [--bars A-B] [--json] [--detail]
  partchroma.py ID --ours SOLO.wav --stem … (a render you made: chirp render --solo TRACK)

Per bar of the map's performed clock (tools/maps/ID.json, tab2song.performed_timeline): 12-bin pitch-class profiles
(long-FFT power summed per semitone over LO-HI Hz) of ours and of the stem, their cosine at shift 0, and the rotation
of ours that matches best. Prints mean cos0, a histogram of best shifts in bars where the best beats shift 0 by more
than 0.15, and those bars. A +5 cluster means our part reads a fourth low: a low note's 3rd harmonic dominating its
root (F1 reads C; Immutable's 8-string through m8-emg's 140 Hz tight). A constant +-2 from a bar on is a tab
bend/transposition artefact, BUT check --detail before transposing: a run of +-1 also appears when our part
over-weights the neighbour notes of the record's pedal (pravus bars 3-40: record F 0.4-0.5 with E/F# secondary, ours
E and D# on top with F third, so a +1 rotation fits while transposing the notes lost ~1.4 both ways; chirper-one).
--detail prints each flagged bar's top pitch classes for the record and for ours.
--render solos TRACKS in a private snapshot of the song (microscore's), so a climber's commit can't land
mid-comparison; --stem takes a family, a sum (guitar+bass) or a WAV (e.g. the bs_roformer_sw stems).
Resolution: 8192-point FFTs at 48 kHz give 5.9 Hz bins, which smear neighbouring semitones below ~90 Hz (F1 at
43.7 Hz spreads into E and F#); keep --lo at 60 for guitars, and read --lo 25 bass audits as coarse.
"""
import argparse
import collections
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import microscore as MS  # noqa: E402  (render, snapshot, stem helpers)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = MS.SR


def pc(x, lo=60.0, hi=600.0, n=8192):
    """The 12-bin pitch-class profile of mono X (sums to 1; zeros when silent). Bin 0 = A (MIDI % 12 == 9 is A;
    bins follow MIDI note number % 12, so C = 0)."""
    if len(x) < n:
        x = np.pad(x, (0, n - len(x)))
    X = np.abs(np.fft.rfft(x[:len(x) // n * n].reshape(-1, n) * np.hanning(n), axis=1)).mean(0)
    f = np.fft.rfftfreq(n, 1 / SR)
    msk = (f > lo) & (f < hi)
    p = np.round(12 * np.log2(f[msk] / 440) + 69).astype(int) % 12
    c = np.zeros(12)
    np.add.at(c, p, X[msk] ** 2)
    return c / max(c.sum(), 1e-12) if c.sum() > 0 else c


def match(ref, ours):
    """(cos at shift 0, best shift in -6..+5, best cos): the rotation of OURS (up by k semitones) closest to REF."""
    if ours.sum() == 0 or ref.sum() == 0:
        return None
    cs = [float(np.dot(ref, np.roll(ours, k)) / np.linalg.norm(ref) / np.linalg.norm(ours)) for k in range(12)]
    return cs[0], (int(np.argmax(cs)) + 6) % 12 - 6, max(cs)


def bars_of(cid):
    import tab2song as T
    path = os.path.join(ROOT, "tools", "maps", f"{cid}.json")
    if not os.path.exists(path):
        raise SystemExit(f"partchroma: no map {path} (the bar clock comes from the song's tab map)")
    m = json.load(open(path))
    return [(x["m"], x["start"], x["start"] + 60 * x["beats"] / x["bpm"]) for x in T.performed_timeline(m["cache"], m)]


NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")


def top(profile, k=3):
    """The K strongest pitch classes of a profile as (name, share), strongest first."""
    return [(NAMES[i], round(float(profile[i]), 2)) for i in np.argsort(profile)[::-1][:k]]


def fmt_top(t):
    return " ".join(f"{n} {v:.2f}" for n, v in t)


def audit(ref, ours, bars, lo, hi, b0=1, b1=10 ** 6):
    rows = []
    for m, s, e in bars:
        if not b0 <= m <= b1:
            continue
        pr, po = pc(ref[int(s * SR):int(e * SR)], lo, hi), pc(ours[int(s * SR):int(e * SR)], lo, hi)
        r = match(pr, po)
        if r:
            rows.append({"bar": m, "cos0": r[0], "shift": r[1], "best": r[2], "record": top(pr), "ours": top(po)})
    return rows


def summary(rows):
    bad = [r for r in rows if r["best"] - r["cos0"] > 0.15]
    return {"bars": len(rows), "mean_cos0": float(np.mean([r["cos0"] for r in rows])) if rows else None,
            "shifts": collections.Counter(r["shift"] for r in bad).most_common(6), "bad": bad}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("--ours")
    ap.add_argument("--render", metavar="TRACKS")
    ap.add_argument("--set", action="append", default=[], metavar="PATH=V")
    ap.add_argument("--song-file")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--stem", required=True)
    ap.add_argument("--lo", type=float, default=60.0)
    ap.add_argument("--hi", type=float, default=600.0)
    ap.add_argument("--bars")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--detail", action="store_true", help="per flagged bar, the top pitch classes of the record and of ours")
    a = ap.parse_args(argv)
    MS.exit_on_term()
    if bool(a.ours) == bool(a.render):
        ap.error("give --ours WAV or --render TRACKS")
    bars = bars_of(a.id)
    b0, b1 = (int(v) for v in a.bars.split("-")) if a.bars else (1, 10 ** 6)
    ref = MS.stem_audio(a.id, a.stem).mean(1)
    if a.ours:
        ours = MS.L.load(a.ours).mean(1)
    else:
        song = a.song_file or os.path.join(ROOT, "songs", f"{a.id}.yaml")
        extra = MS.solo_args(a.render) + [x for v in a.set for x in ("--set", v)]
        with MS.snapshot(song) as snap:
            ours = MS.render_window(snap, None, None, a.seed, extra).mean(1)
    s = summary(audit(ref, ours, bars, a.lo, a.hi, b0, b1))
    if not a.detail:
        s["bad"] = [{k: v for k, v in r.items() if k not in ("record", "ours")} for r in s["bad"]]
    if a.json:
        print(json.dumps(s, indent=1))
        return
    print(f"bars {s['bars']}  mean cos0 {s['mean_cos0']:.2f}  shifts {s['shifts']}" if s["bars"] else "no bars")
    if s["bad"]:
        print("bad: " + " ".join(f"{r['bar']}:{r['shift']:+d}({r['cos0']:.2f})" for r in s["bad"]))
    if a.detail:
        for r in s["bad"]:
            print(f"  bar {r['bar']:4d} {r['shift']:+d} | record {fmt_top(r['record'])} | ours {fmt_top(r['ours'])}")


if __name__ == "__main__":
    main()
