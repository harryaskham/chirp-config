#!/usr/bin/env python3
"""amap: an arrangement map - which of a song's tracks can be HEARD, window by window (chirper-two, 10 Nov).

  amap.py ID [--song FILE] [--win 32] [--seed 0] [-j 3] [--cache DIR] [--by entry] [--json]

After a hundred rounds of accretion a song has a hundred tracks, 30-45 of them sounding at once. presence.py answers
"how loud is each track in THIS window" by rendering every track solo for the window; amap renders every track solo
ONCE for the whole song (unmastered, loudness=null, as presence does), keeps each track's frame levels and band
powers, and prints the whole arrangement as a matrix: tracks down, windows of --win beats across.

Each cell is a digit 0-9: the share of the track's SOUNDING frames in that window in which it can be heard, tenths.
"Heard" is a masking estimate, not a level: in a 0.4 s frame the track holds at least a quarter of the mix's power
(within 6 dB) in at least one of nine octave-wide bands (20 Hz - 11 kHz), and that band is within 40 dB of the frame's
loudest band. So a quiet hat over a loud bass counts (it owns its band), and a pad 15 dB under three other pads in the
same octave does not. A `!` after the digit: the track is also under -25 dB against the whole mix there (presence's
BURIED). `.`: silent in that window.
Below the matrix: tracks sounding per window, tracks masked (< 0.15) per window, and the list of tracks masked in
every window they play or in most of them - the candidates to raise, re-voice, move in register, or cut.

What it is for: finding the parts nobody can hear (a signature arp at -28 dB, a lyric fragment under the bass, an
element's carrier masked through a whole section) and seeing a re-balance land. What it is not: a score, or an ear.
A part masked 90% of the time can still be the right ghost; a part "heard" in a band can still be lost in a busy
texture. Octave bands are wider than critical bands, so the estimate leans strict for narrow sounds.

The cache (--cache DIR, default /tmp/lt/amap/<song sha1>-<pin>-s<seed>) holds one small .npz per track; a second run
is instant. Rendering 100 solos of a 5-minute song takes 10-20 minutes at -j 3: run it in a guarded unit.
Read-only on the song.
"""
import argparse
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as L  # noqa: E402
import presence as P  # noqa: E402

ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
EDGES = [20, 45, 90, 180, 355, 710, 1400, 2800, 5600, 11025]
SHARE = 0.25          # a track is heard in a band when it holds this share of the mix's power there
FLOOR = 1e-4          # ... and the band is within 40 dB of the frame's loudest band
MASKED = 0.15         # a cell under this is "masked"


def stem(pin, song, cache, name, seed):
    """Render NAME solo (or the mix) for the whole song, keep frame levels (K-weighted dB) and band powers."""
    npz = os.path.join(cache, name + ".npz")
    if os.path.exists(npz):
        return name
    wav = os.path.join(cache, name + ".wav")
    P.render(pin, song, wav, seed, (None, None), None if name == "__mix__" else name)
    x = L.load(wav)
    db = P.frames_db(x, L.SR, kweight=True)
    m = x.mean(axis=1) if x.ndim > 1 else x
    n = max(1, int(P.FRAME * L.SR))
    k = len(m) // n
    fr = m[:k * n].astype(np.float64).reshape(k, n) * np.hanning(n)
    spec = np.abs(np.fft.rfft(fr, axis=1)) ** 2
    f = np.fft.rfftfreq(n, 1 / L.SR)
    bp = np.stack([spec[:, (f >= a) & (f < b)].sum(1) for a, b in zip(EDGES[:-1], EDGES[1:])], 1)
    np.savez_compressed(npz, db=db, bp=bp)
    os.remove(wav)
    return name


def cells(live, cache, times, edges):
    """{track: [None | (heard share, level vs mix dB, active share)] per window}."""
    mix = np.load(os.path.join(cache, "__mix__.npz"))
    stems = {n: np.load(os.path.join(cache, n + ".npz")) for n in live}
    k = min([len(mix["db"])] + [len(stems[n]["db"]) for n in live])
    mdb, mbp = mix["db"][:k], mix["bp"][:k]
    sig = mbp > mbp.max(axis=1, keepdims=True) * FLOOR
    pw = lambda v: 10 * np.log10(np.mean(10 ** (v / 10)) + 1e-12)  # noqa: E731
    rows = {}
    for n in live:
        d, bp = stems[n]["db"][:k], stems[n]["bp"][:k]
        peak = float(d.max()) if k else -120.0
        on = d > max(peak - P.SOUNDS_DB, -100.0)
        heard = ((bp >= SHARE * mbp) & sig).any(axis=1)
        row = []
        for a, b in zip(edges[:-1], edges[1:]):
            i0, i1 = int(times[a] / P.FRAME), int(times[b] / P.FRAME)
            o = on[i0:i1]
            if peak < -100.0 or not o.any():
                row.append(None)
                continue
            row.append((round(float(heard[i0:i1][o].mean()), 2), round(float(pw(d[i0:i1][o]) - pw(mdb[i0:i1][o])), 1),
                        round(float(o.mean()), 2)))
        rows[n] = row
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--song")
    ap.add_argument("--win", type=int, default=32, help="window in beats (default 32)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-j", type=int, default=3)
    ap.add_argument("--cache")
    ap.add_argument("--pin")
    ap.add_argument("--by", choices=["heard", "entry"], default="heard", help="row order (default: most heard first)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song = a.song or (os.path.join(ROOT, "songs", f"{a.id}.yaml") if a.id else None)
    if not song or not os.path.exists(song):
        raise SystemExit("amap: give a climb ID (songs/ID.yaml) or --song FILE")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    sha = hashlib.sha1(open(song, "rb").read()).hexdigest()[:12]
    cache = a.cache or os.path.join("/tmp/lt/amap" if os.path.isdir("/tmp/lt") else "/tmp/amap",
                                    f"{sha}-{os.path.basename(pin)[-8:]}-s{a.seed}")
    os.makedirs(cache, exist_ok=True)
    live = [n for n, muted in P.plan_tracks(pin, song) if not muted]
    todo = [n for n in ["__mix__"] + live if not os.path.exists(os.path.join(cache, n + ".npz"))]
    if todo:
        print(f"amap: rendering {len(todo)} solo(s) into {cache} ...", file=sys.stderr, flush=True)
        with ThreadPoolExecutor(max(1, a.j)) as ex:
            list(ex.map(lambda n: stem(pin, song, cache, n, a.seed), todo))
    import chirpers as CH
    times = CH.song_timeline(pin, song)["times"]
    nb = len(times) - 1
    edges = list(range(0, nb, a.win)) + [nb]
    rows = cells(live, cache, times, edges)
    nw = len(edges) - 1
    if a.json:
        print(json.dumps({"song": song, "cache": cache, "win": a.win, "edges": edges,
                          "times": [round(times[e], 2) for e in edges], "tracks": rows}))
        return
    first = lambda n: next((i for i, c in enumerate(rows[n]) if c), nw)  # noqa: E731
    if a.by == "entry":
        order = sorted(live, key=lambda n: (first(n), -sum(c[0] * c[2] for c in rows[n] if c)))
    else:
        order = sorted(live, key=lambda n: -sum(c[0] * c[2] for c in rows[n] if c))
    w = max(8, max(len(n) for n in live))
    print(f"{os.path.basename(song)}: {len(live)} tracks, windows of {a.win} beats; digit = share of the track's sounding "
          f"frames it is HEARD in (tenths), ! = also under -25 dB, . = silent")
    print(f"{'beat':{w}s} " + " ".join(f"{e:>4d}" for e in edges[:-1]))
    print(f"{'m:ss':{w}s} " + " ".join(f"{int(times[e] // 60)}:{int(times[e] % 60):02d}" for e in edges[:-1]))
    for n in order:
        print(f"{n:{w}s} " + " ".join("   ." if c is None else f"{min(9, int(c[0] * 10)):>3d}{'!' if c[1] < -25 else ' '}"
                                      for c in rows[n]))
    print(f"{'sounding':{w}s} " + " ".join(f"{sum(1 for n in live if rows[n][i]):>4d}" for i in range(nw)))
    print(f"{'masked':{w}s} " + " ".join(f"{sum(1 for n in live if rows[n][i] and rows[n][i][0] < MASKED):>4d}"
                                         for i in range(nw)))
    always, mostly = [], []
    for n in live:
        cs = [c for c in rows[n] if c]
        if not cs:
            continue
        m = sum(1 for c in cs if c[0] < MASKED)
        if m == len(cs):
            always.append(n)
        elif m * 2 >= len(cs) and len(cs) >= 2:
            mostly.append(f"{n} ({m}/{len(cs)})")
    if always:
        print("masked wherever they play: " + ", ".join(always))
    if mostly:
        print("masked in most of their windows: " + ", ".join(mostly))


if __name__ == "__main__":
    main()
