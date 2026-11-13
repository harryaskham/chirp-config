#!/usr/bin/env python3
"""vocsplit: the reference records' whole-mix band shares in their loud passages WITH the voice and WITHOUT it, so an
instrumental section is judged against instrumental passages and a sung one against sung ones. (chirper-zero, Common
Time v30, where it showed that most of the piece had been read against the wrong passages; made a module, with a
cache for stembal, by chirp-eco.)

  vocsplit.py ID... [--frame 4] [--with 12] [--without 25] [--model bs_roformer_sw]

The bands are stembal's nine (20-60-120-250-500-1k-2k-4k-8k-16k Hz), each as its share of the mix in dB. A record is
the sum of its separated stems (ref/stems/MODEL/ID/*.wav), cut into frames of --frame seconds. A frame is loud when
it is within 3 dB of the record's 90th-percentile level; it is WITH the voice when the vocals stem is within --with dB
of the mix and WITHOUT when it is more than --without dB under. The separator is used only to SORT the frames: the
spectra are the mixes' own. A tune on a lead guitar is counted as a voice. Prints each record's rows, the medians,
and without minus with, without minus all and with minus all.

Eleven Meshuggah records: their passages without a voice hold, beside all their loud passages together,
+0.4 +0.4 -0.3 +0.5 -2.3 -0.6 +0.4 +0.4 -1.4 dB; those with one -0.5 -0.3 -0.3 0.0 +1.3 +0.3 0.0 -0.2 +0.5. The voice
is 3.6 dB of 500 Hz-1 kHz and 1.9 dB of 8-16 kHz. `stembal.py song ... --voice` reads every window both ways.
Read-only (it writes its medians to ref/stembal/ for stembal). Tests: tools/tests/test_vocsplit.py.
"""
import glob
import hashlib
import json
import os
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
while not os.path.isdir(os.path.join(ROOT, "ref")) and ROOT != "/":
    ROOT = os.path.dirname(ROOT)
E = [20, 60, 120, 250, 500, 1000, 2000, 4000, 8000, 16000]
CLASSES = ("with", "without", "all")


def load(p):
    with wave.open(p) as w:
        sr = w.getframerate()
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32).reshape(-1, w.getnchannels()).mean(1) / 32768, sr


def split(ids, frame=4.0, w_with=12.0, w_without=25.0, model="bs_roformer_sw", say=None, gaps=None):
    """{class: [nine band shares in dB, one row a record that has two such frames]}; `say` gets each record's lines;
    `gaps` (a list) gets, a record, how far under the mix its voice is in its loud frames WITH the voice (median dB)."""
    R = os.path.join(ROOT, "ref", "stems", model, "")
    rows = {c: [] for c in CLASSES}
    for sid in ids:
        stems = {os.path.basename(p)[:-4]: load(p) for p in sorted(glob.glob(R + sid + "/*.wav"))}
        if "vocals" not in stems:
            raise SystemExit(f"vocsplit: no vocals stem (WAV) for {sid} under {R}")
        sr = next(iter(stems.values()))[1]
        n = min(len(v[0]) for v in stems.values())
        mix = sum(v[0][:n] for v in stems.values())
        vox = stems["vocals"][0][:n]
        L = int(frame * sr)
        fr = [(i, 10 * np.log10(np.mean(mix[i:i + L] ** 2) + 1e-12), 10 * np.log10(np.mean(vox[i:i + L] ** 2) + 1e-12))
              for i in range(0, n - L, L)]
        if not fr:
            raise SystemExit(f"vocsplit: {sid} is shorter than two frames of {frame:g} s")
        loud = np.percentile([x[1] for x in fr], 90)
        f = np.fft.rfftfreq(L, 1 / sr)
        if gaps is not None:
            sung = [lm - lv for _, lm, lv in fr if lm >= loud - 3 and lm - lv < w_with]
            if len(sung) >= 2:
                gaps.append(float(np.median(sung)))
        out = {}
        for cls in CLASSES:
            P = 0
            k = 0
            for i, lm, lv in fr:
                if lm < loud - 3:
                    continue
                d = lm - lv
                if (cls == "with" and d < w_with) or (cls == "without" and d > w_without) or cls == "all":
                    P = P + np.abs(np.fft.rfft(mix[i:i + L])) ** 2
                    k += 1
            if k >= 2:
                tot = P[(f >= 20) & (f < 16000)].sum()
                out[cls] = (k, np.array([10 * np.log10(P[(f >= lo) & (f < hi)].sum() / tot + 1e-12) for lo, hi in zip(E, E[1:])]))
                rows[cls].append(out[cls][1])
        if say:
            for cls in CLASSES:
                if cls in out:
                    say("%-32s %-8s %3d frames  " % (sid, cls, out[cls][0]) + " ".join("%6.1f" % v for v in out[cls][1]))
                else:
                    say("%-32s %-8s too few frames" % (sid, cls))
    return rows


def medians(rows):
    return {c: np.median(np.array(rows[c]), 0) for c in rows if rows[c]}


def cache_file(ids, frame, w_with, w_without, model):
    key = hashlib.sha1(json.dumps(["voice", list(ids), model, frame, w_with, w_without]).encode()).hexdigest()[:12]
    return os.path.join(ROOT, "ref", "stembal", f"voice-{key}.json")


def cached(ids, frame=4.0, w_with=12.0, w_without=25.0, model="bs_roformer_sw"):
    """{"with": nine bands, "without": ..., "all": ..., "n": {class: records}, "gap": how far under the mix the
    records' voice is in their frames with it (median of the records' medians, dB)}, from ref/stembal/ when it is there."""
    path = cache_file(ids, frame, w_with, w_without, model)
    if os.path.exists(path):
        with open(path) as f:
            got = json.load(f)
        if "gap" in got:                              # a file from before the gap was kept is made again
            return got
    gaps = []
    return store(path, split(ids, frame, w_with, w_without, model, gaps=gaps), gaps)


def store(path, rows, gaps=None):
    out = {c: v.tolist() for c, v in medians(rows).items()}
    out["n"] = {c: len(rows[c]) for c in rows}
    out["gap"] = float(np.median(gaps)) if gaps else None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f)
    return out


def report(ids, frame=4.0, w_with=12.0, w_without=25.0, model="bs_roformer_sw"):
    gaps = []
    rows = split(ids, frame, w_with, w_without, model, say=print, gaps=gaps)
    print("%-56s" % "bands: <60 -120 -250 -500 -1k -2k -4k -8k -16k")
    m = medians(rows)
    for c in m:
        print("%-32s %-8s %3d records " % ("MEDIAN", c, len(rows[c])) + " ".join("%6.1f" % v for v in m[c]))
    if "with" in m and "without" in m:
        print("%-32s %-21s" % ("WITHOUT minus WITH", "") + " ".join("%+6.1f" % v for v in m["without"] - m["with"]))
        print("%-32s %-21s" % ("WITHOUT minus ALL", "") + " ".join("%+6.1f" % v for v in m["without"] - m["all"]))
        print("%-32s %-21s" % ("WITH minus ALL", "") + " ".join("%+6.1f" % v for v in m["with"] - m["all"]))
    store(cache_file(ids, frame, w_with, w_without, model), rows, gaps)


def main(argv=None):
    frame, w_with, w_without, model, ids = 4.0, 12.0, 25.0, "bs_roformer_sw", []
    it = iter(sys.argv[1:] if argv is None else argv)
    for a in it:
        if a in ("-h", "--help"):
            print(__doc__)
            return 0
        if a == "--frame":
            frame = float(next(it))
        elif a == "--with":
            w_with = float(next(it))
        elif a == "--without":
            w_without = float(next(it))
        elif a == "--model":
            model = next(it)
        else:
            ids.append(a)
    if not ids:
        print(__doc__)
        return 2
    report(ids, frame, w_with, w_without, model)
    return 0


if __name__ == "__main__":
    sys.exit(main())
