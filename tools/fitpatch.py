#!/usr/bin/env python3
"""Fit an instrument patch to a reference spectral fingerprint: render the patch on one note, measure
its harmonic series (h1..hN, dB relative to the strongest) and the noise floor between harmonics, and
score the mean absolute dB difference against a target fingerprint (taken from a reference passage with
harmonic/percussive separation). Candidates are patch kv overrides; best first.

  fitpatch.py target REF.wav START END F0 [N]          print a target fingerprint (JSON) from a passage
  fitpatch.py fit TARGET.json PATCH NOTE SECONDS 'label=kv kv …' …   render + score candidates
"""
import json, os, shlex, subprocess, sys
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import chirpbin  # noqa: E402  (the adopted groove pin when CHIRP is unset)
import numpy as np
from scipy import ndimage, signal
sys.path.insert(0, os.path.dirname(__file__))
import likeness as L

C = chirpbin.resolve("/tmp/lt/chirp-main/cli/chirp/target/release/chirp")


def fingerprint(x, f0, n=40, hpss=True):
    f, t, Z = signal.stft(x, 48000, nperseg=16384, noverlap=16384 - 2048)
    M = np.abs(Z)
    if hpss:
        H = ndimage.median_filter(M, size=(1, 17)); P = ndimage.median_filter(M, size=(17, 1))
        M = M * (H ** 2 / (H ** 2 + P ** 2 + 1e-12))
    spec = (M ** 2).mean(1)
    harm, noise = [], []
    for h in range(1, n + 1):
        b = np.argmin(np.abs(f - f0 * h)); harm.append(10 * np.log10(spec[max(0, b - 2):b + 3].max() + 1e-20))
        m = np.argmin(np.abs(f - f0 * (h + 0.5))); noise.append(10 * np.log10(spec[max(0, m - 2):m + 3].mean() + 1e-20))
    top = max(harm)
    return {"f0": f0, "harm": [round(float(v - top), 1) for v in harm], "noise": [round(float(v - top), 1) for v in noise]}


def score(fp, tgt):
    h = np.array(fp["harm"]); th = np.array(tgt["harm"]); nz = np.array(fp["noise"]); tn = np.array(tgt["noise"])
    k = min(len(h), len(th))
    return float(np.abs(h[:k] - th[:k]).mean()), float(np.abs(nz[:k] - tn[:k]).mean())


if __name__ == "__main__":
    if sys.argv[1] == "target":
        x = L.load(sys.argv[2]).mean(1)[int(float(sys.argv[3]) * 48000):int(float(sys.argv[4]) * 48000)]
        print(json.dumps(fingerprint(x, float(sys.argv[5]), int(sys.argv[6]) if len(sys.argv) > 6 else 40)))
    elif sys.argv[1] == "fit":
        tgt = json.load(open(sys.argv[2])); patch, note, secs = sys.argv[3], sys.argv[4], float(sys.argv[5])
        res = []
        for cand in sys.argv[6:]:
            label, kv = cand.split("=", 1)
            song = {"tempo": 60, "tracks": [{"patch": f"{patch} {kv}".strip(), "score": f"{note}/{secs}s@100"}]}
            open("/tmp/lt/fit.yaml", "w").write(json.dumps(song))
            r = subprocess.run(["nice", "-n", "10", C, "render", "-f", "/tmp/lt/fit.yaml", "-o", f"/tmp/lt/fit-{label}.wav"], capture_output=True, text=True)
            if r.returncode:
                print(label, "ERROR", r.stderr[-200:]); continue
            x = L.load(f"/tmp/lt/fit-{label}.wav").mean(1)[int(0.3 * 48000):int(secs * 48000)]
            fp = fingerprint(x, tgt["f0"], len(tgt["harm"]), hpss=False)
            eh, en = score(fp, tgt)
            res.append((eh + 0.5 * en, eh, en, label, fp))
        res.sort()
        for tot, eh, en, label, fp in res:
            print(f"{label:22s} err {tot:5.2f}  harmonics {eh:5.2f} dB  noise {en:5.2f} dB  h1-8 {fp['harm'][:8]}")
