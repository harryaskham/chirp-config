#!/usr/bin/env python3
"""Guitar-tone micro hill-climb against a separated reference stem, corrected for the separation's own bias.

The reference is only available as a Demucs stem, and separation itself fills spectral valleys and reshapes
the envelope. So the target is: reference-stem profile − (our separated stem − our soloed render), measured
on the same events. Candidates are then plain soloed renders (no separation per candidate).

  guitarclimb.py bias REF_STEM REF_T0 OUR_SEP OUR_SEP_T0 OUR_SOLO OUR_SOLO_T0 --events E,.. > target.json
  guitarclimb.py score target.json CANDIDATE_SOLO.wav T0 --events E,..      (lower dist = closer)

dist = mean |envelope error| over 1/6-octave bands 80 Hz-12 kHz (dB)
     + 0.5 x mean |contrast error| 100 Hz-3.2 kHz (dB) + |decay error| / 4 (dB/s) + 2 x |irregularity error| (dB)"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import tonecmp as T

OCT = (100, 200, 400, 800, 1600)


def prof(path, t0, evs):
    return T.profile(path, t0, evs, 0.04, 0.66, 30.87)


def bias(a):
    evs = [float(v) for v in a[a.index("--events") + 1].split(",")]
    R, S, O = prof(a[0], float(a[1]), evs), prof(a[2], float(a[3]), evs), prof(a[4], float(a[5]), evs)
    tgt = {"centres": R["centres"],
           "env": (np.array(R["env"]) - (np.array(S["env"]) - np.array(O["env"]))).tolist(),
           "contrast": {lo: R["contrast"][lo] - (S["contrast"][lo] - O["contrast"][lo]) for lo in R["contrast"]},
           "decay_db_s": R["decay_db_s"], "irreg": R["irreg"] - (S["irreg"] - O["irreg"]), "corr": R["corr"]}
    print(json.dumps(tgt))


def score(tgt, cand):
    c = np.array(tgt["centres"]); sel = (c >= 80) & (c <= 12000)
    e = np.array(cand["env"]) - np.array(tgt["env"])
    con = [cand["contrast"][lo] - tgt["contrast"][str(lo)] if str(lo) in tgt["contrast"] else cand["contrast"][lo] - tgt["contrast"][lo] for lo in OCT]
    d = float(np.mean(np.abs(e[sel])) + 0.5 * np.mean(np.abs(con)) + abs(cand["decay_db_s"] - tgt["decay_db_s"]) / 4
              + 2 * abs(cand["irreg"] - tgt["irreg"]))
    return d, e, con


def main():
    a = sys.argv[1:]
    if a[0] == "bias":
        return bias(a[1:])
    tgt = json.load(open(a[1])); evs = [float(v) for v in a[a.index("--events") + 1].split(",")]
    cand = prof(a[2], float(a[3]), evs)
    d, e, con = score(tgt, cand)
    c = np.array(tgt["centres"])
    groups = [("80-160", 80, 160), ("160-320", 160, 320), ("320-640", 320, 640), ("640-1.3k", 640, 1280), ("1.3-2.6k", 1280, 2560),
              ("2.6-5k", 2560, 5120), ("5-10k", 5120, 10240), ("10-16k", 10240, 16000)]
    env = "  ".join(f"{n} {np.mean(e[(c >= lo) & (c < hi)]):+5.1f}" for n, lo, hi in groups)
    out = {"dist": round(d, 2), "env_err": env, "contrast_err": [round(v, 1) for v in con],
           "decay": [round(cand["decay_db_s"], 1), round(tgt["decay_db_s"], 1)], "irreg": [round(cand["irreg"], 2), round(tgt["irreg"], 2)],
           "corr": [round(cand["corr"], 2), round(tgt["corr"], 2)]}
    print(json.dumps(out) if "--json" in a else
          f"dist {out['dist']:6.2f} | env {env}\n            contrast err {out['contrast_err']} | decay {out['decay']} (ours, target) | irreg {out['irreg']} | corr {out['corr']}")


if __name__ == "__main__":
    main()
