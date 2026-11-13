#!/usr/bin/env python3
"""lowwide: who carries the low end, the guitars (wide) or the bass and kick (centre)? It needs no stems: the record
itself says. (chirper-zero, Common Time v32, where it showed our bass carrying weight that the records' guitars carry.)

  lowwide.py NAME=FILE[:START:DUR] ...

For each stereo file (16- or 32-bit WAV), or START seconds for DUR seconds of it: the side-minus-mid level in dB and
the left/right correlation in 70-110, 110-180, 180-300 and 300-600 Hz, over its loud 4 s frames (within 3 dB of the
90th percentile). A double-tracked guitar is as much side as mid (0 dB, correlation 0); a bass or a kick is all mid
(very negative, correlation 1). Rows whose NAME starts with "ours" are left out of the last line, the MEDIAN of the
others (printed when there are two or more).
Eleven Meshuggah records: 70-110 Hz, around the low string's second harmonic, is 9.3 dB more centre than sides
(median; 13.8 to 6.4). Common Time's heavy sections read 12.2 before an 87 Hz peak after each heavy rig's amp (like a
cabinet's resonance), 9.5 after. Read-only; needs scipy. Tests: tools/tests/test_lowwide.py.
"""
import sys
import wave

import numpy as np

B = ((70, 110), (110, 180), (180, 300), (300, 600))


def load(p, t0=None, dur=None):
    with wave.open(p) as w:
        sr = w.getframerate()
        sw = w.getsampwidth()
        if t0 is not None:
            w.setpos(int(t0 * sr))
        n = int(dur * sr) if dur else w.getnframes() - (int(t0 * sr) if t0 else 0)
        return np.frombuffer(w.readframes(n), "<i%d" % sw).astype(np.float32).reshape(-1, w.getnchannels()) / 2 ** (8 * sw - 1), sr


def measure(x, sr):
    """[(side minus mid in dB, left/right correlation)] for each band of B, over the loud 4 s frames of x."""
    from scipy.signal import butter, sosfilt
    L = int(4 * sr)
    fr = [(i, 10 * np.log10(np.mean(x[i:i + L] ** 2) + 1e-12)) for i in range(0, max(1, len(x) - L + 1), L)]
    loud = np.percentile([f[1] for f in fr], 90)
    keep = [i for i, lv in fr if lv > loud - 3]
    y = np.concatenate([x[i:i + L] for i in keep]) if keep else x
    out = []
    for lo, hi in B:
        s = butter(4, [lo, hi], btype="band", fs=sr, output="sos")
        left = sosfilt(s, y[:, 0])
        right = sosfilt(s, y[:, 1])
        m = (left + right) / 2
        sd = (left - right) / 2
        out.append((10 * np.log10(np.mean(sd ** 2) / (np.mean(m ** 2) + 1e-20) + 1e-12), np.corrcoef(left, right)[0, 1]))
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0 if argv else 2
    rows = []
    print("%-34s" % "side - mid dB (corr)" + "".join("%16s" % ("%d-%d Hz" % b) for b in B))
    for a in argv:
        name, rest = a.split("=", 1)
        parts = rest.split(":")
        x, sr = load(parts[0], float(parts[1]) if len(parts) > 1 else None, float(parts[2]) if len(parts) > 2 else None)
        if x.shape[1] < 2:
            raise SystemExit(f"lowwide: {parts[0]} is not stereo; there are no sides to read")
        out = measure(x, sr)
        rows.append((name, out))
        print("%-34s" % name + "".join("%9.1f (%4.2f)" % o for o in out))
    recs = [o for n, o in rows if not n.upper().startswith("OURS")]
    if len(recs) > 1:
        print("%-34s" % "MEDIAN of the others" + "".join("%9.1f       " % np.median([r[i][0] for r in recs]) for i in range(len(B))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
