#!/usr/bin/env python3
"""QA the styles as the groove plays them: compose a chapter per style, render it through the song's
own master chain, and report loudness, peak, limiter time, render speed and spectral balance.
`qa.py [STYLE …]` (default: the heavy rotation)."""
import importlib.util, json, os, random, subprocess, sys, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ev", os.path.join(HERE, "evolve.py"))
ev = importlib.util.module_from_spec(spec); spec.loader.exec_module(ev)
BANDS = [(30, 100), (100, 300), (300, 1000), (1000, 3000), (3000, 8000), (8000, 16000)]


def measure(wav):
    b = open(wav, "rb").read(); i = b.index(b"data") + 8; n = (len(b) - i) // 2
    x = np.frombuffer(b[i:i + n * 2], dtype="<i2").astype(float) / 32768
    a = (x[0::2] + x[1::2]) / 2
    N = 8192; acc = np.zeros(N // 2 + 1)
    for s in range(0, len(a) - N, N):
        acc += np.abs(np.fft.rfft(a[s:s + N] * np.hanning(N))) ** 2
    f = np.fft.rfftfreq(N, 1 / 48000); tot = acc[(f >= 30) & (f < 16000)].sum()
    bands = [10 * np.log10(acc[(f >= lo) & (f < hi)].sum() / tot + 1e-12) for lo, hi in BANDS]
    w = 48000 * 3
    win = [20 * np.log10(np.sqrt((a[j:j + w] ** 2).mean()) + 1e-9) for j in range(0, len(a) - w, w)]
    return 20 * np.log10(np.sqrt((x ** 2).mean())), bands, max(win) - min(win) if win else 0


def main(styles):
    print(f"{'style':13s} {'bpm':>4s} {'rms':>6s} {'peak':>5s} {'lim':>6s} {'xRT':>4s} {'dyn':>4s} | sub   low  lmid  mid  hmid  air")
    for st in styles:
        random.seed(zlib.crc32(st.encode()))  # stable per style across runs
        ident = ev.identity(st)
        name = f"form-qa-{st}"
        ev.write_form(name, dict(ident, chapter=0))
        doc = {"tempo": ident["tempo"], "vars": {"stop": {"value": 0, "smooth": "5ms", "min": 0, "max": 1}},
               "master": {"fx": json.loads(ev.master_for(ident))}, "tracks": [{"name": "a", "score": f"@{name}"}]}
        json.dump(doc, open("/tmp/chirp-qa.json", "w"))
        r = subprocess.run([ev.C, "render", "--json", "-f", "/tmp/chirp-qa.json", "-o", "/tmp/chirp-qa.wav"], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)["data"]
        except Exception:
            print(st, "RENDER FAILED", r.stderr[-200:]); continue
        rms, bands, dyn = measure("/tmp/chirp-qa.wav")
        print(f"{st:13s} {ident['tempo']:4d} {rms:6.1f} {d['peak_dbfs']:5.1f} {round(d['limited_ms']):6d} {d['duration'] * 1000 / d['timings']['render_ms']:4.1f} {dyn:4.1f} | " + " ".join(f"{v:5.1f}" for v in bands))
        for f in [f"{ev.SONGS}/{name}.yaml"] + [os.path.join(ev.SONGS, g) for g in os.listdir(ev.SONGS) if g.startswith(f"gen-{name}-")]:
            os.remove(f)


if __name__ == "__main__":
    main(sys.argv[1:] or ["meshuggah", "hardcore-kl", "tech-death", "thrash", "tool", "djent", "brostep", "blackgaze", "darksynth"])
