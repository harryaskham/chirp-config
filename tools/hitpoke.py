#!/usr/bin/env python3
"""hitpoke: does a part's hit get through the WHOLE MIX? (chirper-zero, Common Time v36, the kick's click; the notes,
the tempo and the windows taken from the engine by chirp-eco.)

  hitpoke.py SONG TRACK LO-HI FROM-TO[:label] ... -- WAV [WAV ...] [--pin CHIRP]

SONG is a climb ID (songs/ID.yaml) or a song file; TRACK the part whose hits are looked for (its notes and the tempo
come from `chirp plan`); LO-HI the band in hertz where the hit should show (3000-6000 for a kick's click); each
window is what `chirp render --from/--to` take (bars 1-indexed: 41-57; beats: 160b-224b; seconds: 76s-107s). The
WAVs are whole-song renders of the mix (from the top), 16- or 32-bit.
For every note of TRACK in a window that has no other note of TRACK in the 60 ms before it: the mix's envelope in
the band (2 ms RMS) over the 12 ms from the hit, less the same over the 12 ms ending 6 ms before it. Prints the
median rise in dB for each window and file, and how many hits. 0 dB: the hit is not there in that band; 3 dB: it
doubles the band's power for those 12 ms. Compare two versions of a song by giving both renders.
It reads fixed-tempo songs in 4/4 only; a TRACK with a `warp` is read where its notes sound (tools/warp.py).
Read-only; needs scipy. Tests: tools/tests/test_hitpoke.py.
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import notechk  # noqa: E402
import wincut  # noqa: E402


def load(p):
    with wave.open(p) as w:
        sr = w.getframerate()
        sw = w.getsampwidth()
        return np.frombuffer(w.readframes(w.getnframes()), "<i%d" % sw).astype(np.float32).reshape(-1, w.getnchannels()).mean(1) \
            / 2 ** (8 * sw - 1), sr


def envelope(x, sr, lo, hi):
    """The band's 2 ms RMS envelope."""
    from scipy.signal import butter, sosfilt
    y = sosfilt(butter(4, [lo, hi], btype="band", fs=sr, output="sos"), x)
    n = int(0.002 * sr)
    m = len(y) // n
    return np.sqrt(np.mean(y[:m * n].reshape(m, n) ** 2, 1) + 1e-12)


def rises(e, sec, s0, s1):
    """The rise in dB at each hit of `sec` (seconds, sorted) inside [s0, s1) that has no other hit in the 60 ms before."""
    out = []
    for k, t in enumerate(sec):
        if not (s0 <= t < s1):
            continue
        if k and t - sec[k - 1] < 0.06:
            continue
        f = int(t / 0.002)
        if f < 12 or f + 6 >= len(e):
            continue
        out.append(20 * np.log10(np.mean(e[f:f + 6]) / np.mean(e[f - 9:f - 3])))
    return out


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if "-h" in a or "--help" in a or "--" not in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    pin = None
    if "--pin" in a:
        i = a.index("--pin")
        pin = a[i + 1]
        del a[i:i + 2]
    i = a.index("--")
    if i < 4 or i + 1 >= len(a):
        print(__doc__)
        return 2
    song, track, band = a[0], a[1], a[2]
    wins, wavs = a[3:i], a[i + 1:]
    try:
        lo, hi = [float(x) for x in band.split("-")]
    except ValueError:
        raise SystemExit(f"hitpoke: the band {band!r} is not LO-HI in hertz, as in 3000-6000") from None
    path = song if os.path.exists(song) else os.path.join(ROOT, "songs", f"{song}.yaml")
    if not os.path.exists(path):
        raise SystemExit(f"hitpoke: no song {song!r} (a climb ID or a file)")
    if not pin:
        with open(os.path.join(HERE, "groove-pin")) as f:
            pin = f.read().strip()
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    r = subprocess.run([pin, "plan", "-f", path, "--json"], capture_output=True, text=True, env=env)
    try:
        d = json.loads(r.stdout)
        canon = (d.get("data") or d).get("canonical") or {}
    except ValueError:
        raise SystemExit(f"hitpoke: chirp plan failed: {r.stderr.strip()[-300:]}") from None
    spans = wincut.window_seconds(canon, wins)
    if spans is None:
        raise SystemExit("hitpoke: a window is not FROM-TO as chirp render takes them, or the song's tempo changes or it is not in 4/4")
    notes = notechk.track_notes(canon, track)
    if not notes:
        raise SystemExit("no notes for " + track)
    tempo = canon.get("tempo", 120.0)
    sec = np.array(sorted(float(n.get("at") or 0) for n in notes)) * 60.0 / tempo
    print("%-22s" % ("%s in %g-%g Hz" % (track, lo, hi)) + "".join("%16s" % (w.split(":")[1] if ":" in w else w) for w in wins))
    for p in wavs:
        x, sr = load(p)
        e = envelope(x, sr, lo, hi)
        row = []
        for s0, s1 in spans:
            got = rises(e, sec, s0, s1)
            row.append("%9.1f (%3d)" % (np.median(got), len(got)) if got else "       -      ")
        print("%-22s" % p.split("/")[-1][:22] + "".join("%16s" % v for v in row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
