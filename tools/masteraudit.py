#!/usr/bin/env python3
"""Master audit: what is each song's master chain correcting, and do songs agree?

A master EQ that boosts or cuts the same band in every section is often compensating for an
instrument (Saturnine's master boosted 45 Hz by 4.5–9 dB for rounds because the upright bass had
a weak fundamental). That fix helps one song; the library fix helps them all. For every enabled
climb this renders a window with and without its master effects and compares the spectral shape
(1/3-octave, each normalised to its total): the difference is the master's net correction per band,
whatever it is made of (EQ, section lanes, multiband).

  masteraudit.py                      # every enabled climb, 30–150 s
  masteraudit.py --songs saturnine --from 60s --to 120s --threshold 2

Reports, per song, bands corrected by at least --threshold dB; then bands that at least --agree
songs correct the same way — candidates for a library or engine fix (file a bead).
"""
import argparse
import json
import os
import subprocess
import wave
from concurrent.futures import ThreadPoolExecutor

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/tmp/masteraudit"
EDGES = 25.0 * 2 ** (np.arange(0, 31) / 3)  # 1/3-octave edges, 25 Hz … 25 kHz


def load(p):
    w = wave.open(p)
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64).reshape(-1, w.getnchannels())
    return x.mean(1), w.getframerate()


def shape(x, sr):
    n = 8192
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[:: n // 2] * np.hanning(n)
    P = (np.abs(np.fft.rfft(fr, axis=1)) ** 2).mean(0)
    f = np.fft.rfftfreq(n, 1 / sr)
    out = []
    for lo, hi in zip(EDGES[:-1], EDGES[1:]):
        if hi > min(sr / 2, 16000):
            break
        out.append(P[(f >= lo) & (f < hi)].sum())
    out = np.array(out)
    return 10 * np.log10(out / out.sum() + 1e-20)


def audit(c, a):
    song = os.path.join(ROOT, c["song"])
    env = dict(os.environ, RAYON_NUM_THREADS="1")
    res = {}
    for tag, extra in (("with", []), ("without", ["--set", "master.fx=[]"])):
        wav = f"{OUT}/{c['id']}-{tag}.wav"
        p = subprocess.run([a.bin, "render", "-f", song, "--from", a.frm, "--to", a.to, *extra, "-o", wav, "--json"],
                           capture_output=True, text=True, env=env, cwd=ROOT)
        try:
            ok = json.loads(p.stdout[p.stdout.find("{"):]).get("status") == "success"
        except ValueError:
            ok = False
        if not ok:
            return c["id"], None
        res[tag] = shape(*load(wav))
        os.remove(wav)
    return c["id"], res["with"] - res["without"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bin", default="chirp")
    ap.add_argument("--songs", help="comma-separated climb ids (default: every enabled climb)")
    ap.add_argument("--from", dest="frm", default="30s")
    ap.add_argument("--to", default="150s")
    ap.add_argument("--threshold", type=float, default=3.0, help="report a band corrected by at least this (dB)")
    ap.add_argument("--agree", type=int, default=4, help="songs correcting a band the same way to flag it")
    ap.add_argument("-j", type=int, default=3)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    climbs = [c for c in json.load(open(os.path.join(ROOT, "climbs.json")))["climbs"]
              if c.get("enabled") and c.get("song") and os.path.exists(os.path.join(ROOT, c["song"]))]
    if a.songs:
        want = set(a.songs.split(","))
        climbs = [c for c in climbs if c["id"] in want]
    centres = np.sqrt(EDGES[:-1] * EDGES[1:])
    rows = {}
    with ThreadPoolExecutor(max_workers=max(1, a.j)) as ex:
        for cid, d in ex.map(lambda c: audit(c, a), climbs):
            if d is None:
                print(f"{cid:28s} render failed")
                continue
            rows[cid] = d
            hits = [f"{centres[i]:.0f} Hz {d[i]:+.1f}" for i in range(len(d)) if abs(d[i]) >= a.threshold]
            print(f"{cid:28s} " + (", ".join(hits) if hits else f"no band beyond ±{a.threshold:g} dB"), flush=True)
    if len(rows) >= 2:
        m = np.array(list(rows.values()))
        n = min(len(r) for r in rows.values())
        m = np.array([r[:n] for r in rows.values()])
        print(f"\nBands {len(rows)} masters correct the same way (≥ {a.threshold / 2:g} dB in ≥ {a.agree} songs):")
        any_flag = False
        for i in range(n):
            up = [k for k, r in rows.items() if r[i] >= a.threshold / 2]
            dn = [k for k, r in rows.items() if r[i] <= -a.threshold / 2]
            for lab, ks in (("boost", up), ("cut", dn)):
                if len(ks) >= a.agree:
                    any_flag = True
                    print(f"  {centres[i]:6.0f} Hz {lab} in {len(ks)}: median {np.median([rows[k][i] for k in ks]):+.1f} dB — {', '.join(ks)}")
        if not any_flag:
            print("  none")


if __name__ == "__main__":
    main()
