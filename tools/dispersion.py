#!/usr/bin/env python3
"""dispersion: does a reverb's tail CHIRP? When each band of its impulse response arrives, and whether the highs
come after the lows, as on a spring. (chirp-eco, for chirper-zero's question on Common Time v35: "whether the
spring sounds like a spring".)

  dispersion.py fx "reverb kind=spring decay=1.6s mix=1" "reverb kind=plate mix=1" ... [--pin CHIRP]
  dispersion.py ir NAME=FILE.wav[:START] ...

`fx`: an impulse is rendered through each effect alone, on the groove's pin (or --pin), and read. Give the effect
as a song takes it, wet only (mix=1). `ir`: impulse responses on file (16-bit WAV; START seconds = where the
impulse is, default 0).
For each, in half-octave bands from 250 Hz to 5.7 kHz, two rows:
  first arrival   when the band's envelope first peaks (ms after the impulse); then how much LATER the 2.8 kHz and
                  4 kHz bands are than the 500 Hz band, and how far apart the bands from 500 Hz to 2 kHz are.
  echo lag        how far each band's train of echoes sits behind the 500 Hz band's (the lag that best lines their
                  envelopes up, within 60 ms), with the same summary: the question asked of the whole tail, for a
                  model whose first sound is not delayed at all.
HOW TO READ IT. On a spring the sound runs the length of the spring before it is heard, and the highs run slower,
steeply so towards a transition frequency of a few kHz: the first echo is a chirp (the "drip"). That reads as the
bands up to 2 kHz close together and 2.8 kHz and 4 kHz later by several ms, 4 kHz the more. The standard model of
it (a chain of a hundred allpasses stretched to a 4.8 kHz transition, coefficient 0.62) reads +3 ms at 2.8 kHz and
+6 at 4 kHz here (by its formula +4 and +18: a band that straddles the steep part reads its early edge), and each
further echo adds as much again. Everything 0: every band arrives together (a delay line, a comb). The bands up to
2 kHz tens of ms apart: a dense room, hall or plate; the reading says nothing about a chirp there.
The engine's `reverb kind=spring` (14 Nov, pin 9d179572): first arrival 11.6 ms in every band, echo lag 0 in every
band: a comb. Its loops carry twelve first-order allpasses, whose delay differs by 0.004 ms between 500 Hz and
4 kHz a round trip: there is no chirp to hear. Read-only (it renders into a temporary folder).
Tests: tools/tests/test_dispersion.py.
"""
import json
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FCS = [250, 354, 500, 707, 1000, 1414, 2000, 2828, 4000, 5657]
CLICK = 0.01                                          # where the impulse sits in the file the engine is fed, seconds


def read(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float).reshape(-1, w.getnchannels()) / 32768
    return x[:, 0], sr


def envelopes(h, sr):
    """The energy envelope of h in each half-octave band of FCS (a Gaussian in log frequency; the analytic signal)."""
    n = len(h)
    H = np.fft.rfft(h)
    f = np.fft.rfftfreq(n, 1 / sr)
    out = []
    for fc in FCS:
        g = np.exp(-0.5 * (np.log2(np.maximum(f, 1.0) / fc) / 0.25) ** 2)
        A = np.zeros(n, complex)
        A[:len(H)] = 2 * H * g
        out.append(np.abs(np.fft.ifft(A)) ** 2)
    return out


def first_arrivals(env, sr, t0, win=0.25):
    """When each band's envelope first peaks, ms after sample t0: the first time it reaches half its largest value in
    the window, followed up to the top of that rise."""
    out = []
    for e in env:
        seg = e[t0:t0 + int(win * sr)]
        if not len(seg) or seg.max() <= 0:
            out.append(float("nan"))
            continue
        j = int(np.argmax(seg >= 0.5 * seg.max()))
        while j + 1 < len(seg) and seg[j + 1] >= seg[j]:
            j += 1
        out.append(j / sr * 1000)
    return np.array(out)


def echo_lags(env, sr, t0, win=0.4, reach=60):
    """How far each band's envelope sits behind the 500 Hz band's, ms: the lag (within `reach` ms) that best lines the
    two up over the first `win` seconds, read in millisecond steps."""
    step = max(1, sr // 1000)
    rows = []
    for e in env:
        seg = e[t0:t0 + int(win * sr)]
        seg = seg[:len(seg) // step * step].reshape(-1, step).mean(1)
        rows.append(seg - seg.mean() if len(seg) else seg)
    ref = rows[FCS.index(500)]
    out = []
    for r in rows:
        best, top = 0, -np.inf
        for lag in range(-reach, reach + 1):
            a, b = (r[lag:], ref[:len(ref) - lag]) if lag >= 0 else (r[:lag], ref[-lag:])
            c = float(np.dot(a, b)) if len(a) else -np.inf
            if c > top:
                best, top = lag, c
        out.append(float(best))
    return np.array(out)


def late(values):
    """(how much later the 2.8 kHz band is than the 500 Hz band, the same for 4 kHz, how far apart the bands from
    500 Hz to 2 kHz are), ms."""
    low = [values[i] for i, f in enumerate(FCS) if 500 <= f <= 2000]
    ref = values[FCS.index(500)]
    return float(values[FCS.index(2828)] - ref), float(values[FCS.index(4000)] - ref), float(max(low) - min(low))


def impulse_through(spec, pin, folder, seconds=3.0, sr=48000):
    """The effect's impulse response on the pin: (samples, rate, the sample the impulse is at)."""
    click = os.path.join(folder, "click.wav")
    x = np.zeros(int(seconds * sr), "<i2")
    x[int(CLICK * sr)] = 16000
    with wave.open(click, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(x.tobytes())
    song = os.path.join(folder, "probe.json")
    with open(song, "w") as f:
        json.dump({"tempo": 120, "length": "%gb" % (seconds * 2), "tracks": [{"name": "t", "input": "click", "fx": [spec]}]}, f)
    out = os.path.join(folder, "out.wav")
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    r = subprocess.run([pin, "render", "-f", song, "--input", "click=" + click, "--set", "loudness=null", "-o", out],
                       capture_output=True, text=True, env=env)
    if r.returncode or not os.path.exists(out):
        raise SystemExit(f"dispersion: the engine would not render {spec!r}: {(r.stderr or r.stdout).strip()[-300:]}")
    h, rate = read(out)
    return h, rate, int(CLICK * rate)


def report(name, h, sr, t0):
    env = envelopes(h, sr)
    for label, values in (("first arrival", first_arrivals(env, sr, t0)), ("echo lag", echo_lags(env, sr, t0))):
        print("%-30s %-14s" % (name[:30], label) + "".join("%7.1f" % v for v in values)
              + "   2.8k %+.1f, 4k %+.1f; 500-2k within %.1f" % late(values))


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) < 2 or a[0] not in ("fx", "ir") or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    pin = None
    if "--pin" in a:
        i = a.index("--pin")
        pin = a[i + 1]
        del a[i:i + 2]
    print("%-30s %-14s" % ("ms, by band (Hz)", "") + "".join("%7d" % f for f in FCS) + "   later than 500 Hz; spread")
    if a[0] == "ir":
        for arg in a[1:]:
            name, rest = arg.split("=", 1)
            path, _, start = rest.partition(":")
            h, sr = read(path)
            report(name, h, sr, int(float(start or 0) * sr))
        return 0
    if not pin:
        with open(os.path.join(ROOT, "tools", "groove-pin")) as f:
            pin = f.readline().strip()
    with tempfile.TemporaryDirectory(prefix="dispersion-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None) as folder:
        for spec in a[1:]:
            report(spec, *impulse_through(spec, pin, folder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
