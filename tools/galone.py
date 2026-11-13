#!/usr/bin/env python3
"""galone: where a guitar plays ALONE on a reference record, so its tone can be read from the record itself and
not from a separated stem. (chirper-zero, Common Time v30: it showed that the separator, not the record, was the
"fizz" our rigs were being held against.)

  galone.py ID... [--clear 18] [--min 1.5] [--model bs_roformer_sw]

The separated stems (ref/stems/MODEL/ID/*.wav) are used only to FIND the passages: the guitar stem within 12 dB of
its loud level (its 90th percentile, in quarter-second steps) and every other stem at least --clear dB under it, for
at least --min seconds. Prints, a record, the guitar's loud level and up to eight passages: start, length, how far
under the others are, and the guitar's level against its loud level. Then read the record there:
  gspec.py rec=ref/obzen.wav:183.2:8.8 ours=RIG-ALONE.wav --diff
Found on the Meshuggah records at the defaults: obzen 183.2 s for 8.8 s, combustion 44.5 s for 2.8 s, bleed 387.0 s
for 1.5 s, this-spiteful-snake 287.0 s for 4.2 s. Read-only. Tests: tools/tests/test_galone.py.
"""
import glob
import os
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
while not os.path.isdir(os.path.join(ROOT, "ref")) and ROOT != "/":
    ROOT = os.path.dirname(ROOT)


def env(p, hop=0.25):
    """The file's level in dBFS, one value a hop (all channels together)."""
    with wave.open(p) as w:
        sr = w.getframerate()
        n = int(hop * sr)
        out = []
        while True:
            b = w.readframes(n)
            if len(b) < n * w.getnchannels() * w.getsampwidth():
                break
            x = np.frombuffer(b, "<i2").astype(np.float32) / 32768
            out.append(10 * np.log10(np.mean(x * x) + 1e-12))
    return np.array(out)


def passages(stems, clear=18.0, mins=1.5):
    """(the guitar's loud level, [(start s, length s, mean dB the others are under, the guitar's level re loud)])."""
    g = stems["guitar"]
    n = min(len(v) for v in stems.values())
    g = g[:n]
    others = np.max(np.stack([v[:n] for k, v in stems.items() if k != "guitar"]), 0)
    loud = np.percentile(g, 90)
    ok = (g > loud - 12) & (g - others > clear)
    runs = []
    i = 0
    while i < n:
        if ok[i]:
            j = i
            while j < n and ok[j]:
                j += 1
            if (j - i) * 0.25 >= mins:
                runs.append((i * 0.25, (j - i) * 0.25, float(np.mean(g[i:j] - others[i:j])), float(np.mean(g[i:j]) - loud)))
            i = j
        else:
            i += 1
    return loud, runs


def main(argv=None):
    clear, mins, model, args = 18.0, 1.5, "bs_roformer_sw", []
    it = iter(sys.argv[1:] if argv is None else argv)
    for a in it:
        if a in ("-h", "--help"):
            print(__doc__)
            return 0
        if a == "--clear":
            clear = float(next(it))
        elif a == "--min":
            mins = float(next(it))
        elif a == "--model":
            model = next(it)
        else:
            args.append(a)
    if not args:
        print(__doc__)
        return 2
    R = os.path.join(ROOT, "ref", "stems", model, "")
    for sid in args:
        stems = {os.path.basename(p)[:-4]: env(p) for p in sorted(glob.glob(R + sid + "/*.wav"))}
        if "guitar" not in stems:
            print(sid, "no guitar stem")
            continue
        if len(stems) < 2:
            print(sid, "no other stem to be alone from")
            continue
        loud, runs = passages(stems, clear, mins)
        print("%-34s guitar's loud level %.1f dBFS; %d passage(s): " % (sid, loud, len(runs))
              + "; ".join("%.1f s for %.1f s (others %.0f dB under; guitar %+.0f re loud)" % r for r in runs[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
