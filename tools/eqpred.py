#!/usr/bin/env python3
"""eqpred: what a filter or an eq WILL do to a part, band by band, before anything is rendered.
(chirp-eco, 14 Nov; chirper-zero, Common Time v39: "Two full renders went on what ten lines would have told me",
after a low-pass fitted by trial. eqfit.py goes the other way: it finds peaks that reach a wanted tone.)

  eqpred.py FILE[:START:DUR] FILTER [FILTER ...] [--band LO-HI ...] [--thirds]

FILE is the part (or the mix) as it is now, a WAV; START and DUR in seconds cut a passage. Each FILTER is one band of
the engine's `eq` or one filter effect, written as the song writes it or short:
    "lp cutoff=14250 q=0.8"      "highshelf cutoff=9000 gain=-2dB"      "peak cutoff=400 q=1 gain=-12dB slope=24"
    lp:14250:0.8                 highshelf:9000:0.707:-2                peak:400:1:-12
(kinds lp hp bp notch peak lowshelf highshelf allpass; q 0.707 when not given; gain in dB; slope 12 or 24, 24 being
the same filter twice). Several FILTERs are applied one after another, as an eq's bands are.
Prints, for each band, how many dB the file's level in that band would change: the filters' exact response (the
engine's own filter: a trapezoidal state-variable filter, crates/chirp-core/src/dsp/mod.rs `SvfCoef`) weighted by
the file's own spectrum, so a band the file fills unevenly is read as it will sound. Bands: --band LO-HI (hertz,
repeatable, as tools/gspec.py takes them), or --thirds for third-octaves from 50 Hz to 16 kHz; default the nine
octaves from 63 Hz to 16 kHz. The last column is the whole file.
Checked against renders on pin e8830ba0 (pink noise through each kind and an eq of three bands, 24 third-octaves):
within 0.01 dB.
What it cannot know: anything after the filter that is not linear (a bus clip, a compressor) will hand part of a
change back. Read-only. Tests: tools/tests/test_eqpred.py.
"""
import sys
import wave

import numpy as np

KINDS = ("lp", "hp", "bp", "notch", "peak", "lowshelf", "highshelf", "allpass")
ALIASES = {"lowpass": "lp", "highpass": "hp", "bandpass": "bp"}
OCTAVES = [(44, 88), (88, 177), (177, 354), (354, 707), (707, 1414), (1414, 2828), (2828, 5657), (5657, 11314), (11314, 20000)]
THIRDS = (50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300,
          8000, 10000, 12500, 16000)


def decibels(text):
    """A gain as the song writes it, in dB: "-2dB", or a bare number, which the engine reads as a linear factor."""
    s = str(text).strip()
    if s.lower().endswith("db"):
        return float(s[:-2])
    v = float(s)
    if v <= 0:
        raise ValueError(f"a gain of {s} is not a level: write it in dB, as in -2dB")
    return 20 * np.log10(v)


def hertz(text):
    s = str(text).strip().lower()
    return float(s[:-1]) * 1000 if s.endswith("k") else float(s[:-2]) if s.endswith("hz") else float(s)


def parse(text):
    """{"kind", "cutoff", "q", "gain" (dB), "stages"} from "lp cutoff=14250 q=0.8" or lp:14250:0.8[:GAIN_DB]."""
    s = text.strip()
    f = {"q": 0.707, "gain": 0.0, "stages": 1}
    if "=" in s:
        parts = s.split()
        f["kind"] = parts[0]
        for kv in parts[1:]:
            k, _, v = kv.partition("=")
            if k == "cutoff":
                f["cutoff"] = hertz(v)
            elif k == "q":
                f["q"] = float(v)
            elif k == "gain":
                f["gain"] = decibels(v)
            elif k == "slope":
                f["stages"] = 2 if int(float(v)) >= 24 else 1
            elif k not in ("type", "kind"):
                raise ValueError(f"{text!r}: {k} is not cutoff, q, gain or slope")
    else:
        parts = s.split(":")
        f["kind"] = parts[0]
        if len(parts) > 1:
            f["cutoff"] = hertz(parts[1])
        if len(parts) > 2 and parts[2]:
            f["q"] = float(parts[2])
        if len(parts) > 3 and parts[3]:
            f["gain"] = float(parts[3].lower().removesuffix("db"))         # the short form's gain is always dB
    f["kind"] = ALIASES.get(f["kind"], f["kind"])
    if f["kind"] not in KINDS:
        raise ValueError(f"{text!r}: the kind is one of {', '.join(KINDS)}")
    if "cutoff" not in f:
        raise ValueError(f"{text!r}: no cutoff")
    return f


def response(f, freqs, rate):
    """|H| at freqs (hertz) of one filter as the engine runs it at `rate`."""
    fc = min(max(f["cutoff"], 10.0), rate * 0.49)
    q = min(max(f["q"], 0.05), 40.0)
    g = np.tan(np.pi * fc / rate)
    a = np.sqrt(max(10 ** (f["gain"] / 20), 1e-6))                       # the engine's `a`: the square root of the linear gain
    k = 1.0 / q
    kind = f["kind"]
    if kind == "lp":
        m = (0.0, 0.0, 1.0)
    elif kind == "hp":
        m = (1.0, -k, -1.0)
    elif kind == "bp":
        m = (0.0, 1.0, 0.0)
    elif kind == "notch":
        m = (1.0, -k, 0.0)
    elif kind == "allpass":
        m = (1.0, -2.0 * k, 0.0)
    elif kind == "peak":
        k = 1.0 / (q * a)
        m = (1.0, k * (a * a - 1.0), 0.0)
    elif kind == "lowshelf":
        g /= np.sqrt(a)
        m = (1.0, k * (a - 1.0), a * a - 1.0)
    else:                                                                 # highshelf
        g *= np.sqrt(a)
        m = (a * a, k * (1.0 - a) * a, 1.0 - a * a)
    s = 1j * np.tan(np.pi * np.minimum(np.asarray(freqs, float), rate * 0.4999) / rate) / g   # the trapezoidal SVF is the
    den = s * s + k * s + 1.0                                                                # analog one, frequency-warped
    h = m[0] + m[1] * s / den + m[2] / den
    return np.abs(h) ** f["stages"]


def spectrum(spec):
    """(power spectrum, its frequencies, rate) of FILE[:START:DUR], channels averaged in power."""
    p = spec.split(":")
    with wave.open(p[0]) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        if len(p) > 1 and p[1]:
            w.setpos(int(float(p[1]) * sr))
        n = int(float(p[2]) * sr) if len(p) > 2 else w.getnframes() - w.tell()
        x = np.frombuffer(w.readframes(n), dtype={2: np.int16, 4: np.int32}[sw]).reshape(-1, ch).astype(float)
    size, hop = 16384, 4096
    if len(x) < size:
        raise SystemExit(f"eqpred: {p[0]}: the passage is shorter than {size} samples")
    # Frames a quarter of a frame apart, so every sample counts alike (Hann squares that far apart add to a constant).
    # Until 14 Nov the frames did not overlap: a hit at a frame's edge hardly counted, and at 108 bpm (a beat is 1.5
    # of these frames) the hits on the beat stayed at one place in the frame through a short passage.
    win = np.hanning(size)[:, None]
    power, k = np.zeros(size // 2 + 1), 0
    for i in range(0, len(x) - size + 1, hop):
        power += (np.abs(np.fft.rfft(x[i:i + size] * win, axis=0)) ** 2).mean(axis=1)
        k += 1
    return power / k, np.fft.rfftfreq(size, 1 / sr), sr


def changes(power, freqs, gain2, bands):
    """The level change in dB of each (lo, hi) band and of the whole, for a power response gain2 on this spectrum."""
    out = []
    for lo, hi in list(bands) + [(0.0, freqs[-1] + 1)]:
        sel = (freqs >= lo) & (freqs < hi)
        before = power[sel].sum()
        out.append(float(10 * np.log10((power[sel] * gain2[sel]).sum() / before)) if before > 0 else float("nan"))
    return out


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) < 2 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    bands, thirds = [], False
    while "--band" in a:
        i = a.index("--band")
        lo, _, hi = a[i + 1].partition("-")
        bands.append((float(lo), float(hi)))
        del a[i:i + 2]
    if "--thirds" in a:
        a.remove("--thirds")
        thirds = True
    try:
        filters = [parse(t) for t in a[1:]]
    except ValueError as e:
        raise SystemExit(f"eqpred: {e}") from None
    power, freqs, sr = spectrum(a[0])
    if not bands:
        bands = [(c / 2 ** (1 / 6), c * 2 ** (1 / 6)) for c in THIRDS] if thirds else OCTAVES
    gain2 = np.ones(len(freqs))
    for f in filters:
        gain2 *= response(f, freqs, sr) ** 2
    got = changes(power, freqs, gain2, bands)

    def name(lo, hi):
        mid = (lo * hi) ** 0.5
        return f"{mid / 1000:.3g}k" if mid >= 1000 else f"{mid:.0f}"
    labels = [f"{lo:g}-{hi:g}" for lo, hi in bands] if len(bands) <= 8 and not thirds and bands != OCTAVES else [name(*b) for b in bands]
    width = max(7, max(len(s) for s in labels) + 1)
    print("change, dB".ljust(14) + "".join(s.rjust(width) for s in labels) + "all".rjust(width))
    print("predicted".ljust(14) + "".join(("%+.1f" % v if v == v else "-").rjust(width) for v in got))
    return 0


if __name__ == "__main__":
    sys.exit(main())
