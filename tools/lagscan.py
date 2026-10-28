"""lagscan: per-bar onset LAG of our rendered parts against the record's stem (chirper-one, obZen Pravus v12).
partrhythm.py gives each bar's onset correlation at lag 0; this scans +-200 ms and reports the best lag, so a riff
whose phase is off by a 16th (polymetric cycle started at the wrong step, or a tab that drifts) shows as a run of
bars with corr0 ~0 or negative and the same best lag. Fix candidates: tools/rngsafe.py replacement of those bars with
the replacement tracks' lead rest shifted (+0.25b = one 16th later when the best lag is about -(16th) ms).

  lagscan.py ID TRACKS STEM A-B      e.g. lagscan.py pravus gtr-l,gtr-r,bass guitar+bass 1-60
Negative best lag = ours EARLY (ours at t-lag matches the record at t)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import partrhythm as PR

MS, PC = PR.MS, PR.PC


def scan(ref_env, ours_env, s, e, fps, span=0.2):
    i0, i1 = int(s * fps), int(e * fps)
    a = ref_env[i0:i1]
    out = []
    for lag in range(-int(span * fps), int(span * fps) + 1):
        if i0 + lag < 0:
            continue
        c = ours_env[i0 + lag:i1 + lag]
        if len(c) != len(a) or len(a) < 4 or np.std(a) == 0 or np.std(c) == 0:
            continue
        out.append((float(np.corrcoef(a, c)[0, 1]), lag / fps))
    return out


def main():
    cid, tracks, stem, rng = sys.argv[1:5]
    b0, b1 = (int(x) for x in rng.split("-"))
    MS.exit_on_term()
    bars = PC.bars_of(cid)
    ref = MS.stem_audio(cid, stem)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with MS.snapshot(os.path.join(root, "songs", f"{cid}.yaml")) as snap:
        ours = MS.render_window(snap, None, None, 0, MS.solo_args(tracks))
    fps = MS.L.FPS
    re_, oe = PR.onset_env(ref), PR.onset_env(ours)
    for m, s, e in bars:
        if not b0 <= m <= b1:
            continue
        r = scan(re_, oe, s, e, fps)
        if not r:
            continue
        z = min(r, key=lambda x: abs(x[1]))
        b = max(r)
        print(f"{m:4d} corr0 {z[0]:+.2f} best {b[0]:+.2f} at {b[1] * 1000:+.0f} ms")


if __name__ == "__main__":
    main()
