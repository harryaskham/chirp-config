#!/usr/bin/env python3
"""lagchk: how far the RIGHT channel's part leads the LEFT's, in sixteenths (chirper-zero, Odd Sympathy v1: is the
right guitar where the form says? The check that a track's `warp` did what was written. Positions as chirp render
takes them and a module by chirp-eco.)

  lagchk.py WAV BPM POS [POS ...] [--bars 4] [--reach 9]
  lagchk.py WAV BPM --step FROM-TO [--bars 1] [--reach 9]     (one line a bar: to SEE a warp move)

WAV is a render of the two parts ALONE, one hard left and one hard right (`chirp render --solo L --solo R`); on a full
mix the cymbals win. BPM is the song's tempo. Each POS is where to look, as `chirp render --from` takes it: a bar
(41, 1-indexed, in 4/4), beats (160b) or seconds (76.2s). From there, over --bars bars (default 4), the two channels'
level envelopes (2 ms peaks, in dB, floored 30 dB under the file's peak, zero-mean) are cross-correlated within
--reach sixteenths either way (default 9). Prints the best two leads: plus = the right channel is EARLY. A part that
repeats every bar reads +8 and -8 alike (half a bar either way is the same place), which is why two are printed.
tools/warp.py prints what the lead should be (a shift of -1 beat is a lead of +4 sixteenths).
--step FROM-TO (bars, as `chirp render --from/--to` takes them: TO is where it stops) reads every bar from FROM on,
one line each, over --bars bars (default 1 here): a warp that slides out and back draws itself down the page
(chirper-zero, Odd Sympathy v18: 8.01, 7.99, 8.64, 9.88, 8.56, 8.11, 7.98). A lead is only known to within a bar,
so each line is printed as the reading a whole bar on or back that lies nearest the line before, and says so when
that is not the one found ("found as -6.12").
The corr it prints says how alike the two envelopes are at that lead, not whether the lead is right: on a part that
rings (a music box through a spring) it falls to 3-8 where two dry guitars read 90 and over, and the leads are still
the warp's (chirper-zero, Odd Sympathy v15). Judge a lead against tools/warp.py, not by a threshold on corr.
Read-only. Tests: tools/tests/test_lagchk.py.
"""
import sys
import wave

import numpy as np

HOP = 96                                                      # samples an envelope frame (2 ms at 48 kHz)


def load(path):
    with wave.open(path) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[sw]).reshape(-1, ch).astype(float)
    return x, sr


def envelope(x, c):
    """Channel c's level in dB against its own peak, a frame of HOP samples, floored at -30."""
    e = np.abs(x[:, c])
    e = e[: len(e) // HOP * HOP].reshape(-1, HOP).max(1)
    return np.maximum(20 * np.log10(np.maximum(e, 1) / e.max()), -30)


def leads(left, right, a0, a1, reach, step):
    """The best two (correlation, lead in frames) of the right envelope over the left in frames a0..a1, within `reach`
    frames either way, the second at least half of `step` (a sixteenth, in frames) from the first."""
    lft, rgt = left[a0:a1] - left[a0:a1].mean(), right[a0:a1] - right[a0:a1].mean()
    res = []
    for lag in range(-reach, reach + 1):                      # r(t) ~ l(t + lag): positive = right is EARLY by lag
        if lag >= 0:
            c = float(np.dot(lft[lag:], rgt[: len(rgt) - lag])) / (len(rgt) - lag)
        else:
            c = float(np.dot(lft[: len(lft) + lag], rgt[-lag:])) / (len(rgt) + lag)
        res.append((c, lag))
    res.sort(reverse=True)
    top = [res[0]]
    for c, lag in res[1:]:
        if all(abs(lag - t[1]) > 0.5 * step for t in top):
            top.append((c, lag))
        if len(top) == 2:
            break
    return top


def beside(found, prev):
    """A lead as found, or a whole bar (16 sixteenths) on or back, whichever lies nearest the reading before
    (as found when there is none): a lead is only known to within a bar."""
    return found if prev is None else min((found - 16, found, found + 16), key=lambda v: abs(v - prev))


def bar_of(tok, bpm):
    """A `chirp render --from` position as a 0-indexed bar (a float), in 4/4."""
    s = tok.strip()
    if s.endswith("s"):
        return float(s[:-1]) * bpm / 240.0
    if s.endswith("b"):
        return float(s[:-1]) / 4.0
    return float(s) - 1.0


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if "-h" in a or "--help" in a or len(a) < 3:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    span, reach16 = 4.0, 9.0
    bars_given = "--bars" in a
    if "--bars" in a:
        i = a.index("--bars")
        span = float(a[i + 1])
        del a[i:i + 2]
    if "--reach" in a:
        i = a.index("--reach")
        reach16 = float(a[i + 1])
        del a[i:i + 2]
    step = None
    if "--step" in a:
        i = a.index("--step")
        try:
            lo, hi = (int(v) for v in a[i + 1].split("-"))
        except (IndexError, ValueError):
            raise SystemExit("lagchk: --step takes FROM-TO in bars, as in --step 104-111") from None
        if hi <= lo:
            raise SystemExit("lagchk: --step FROM-TO: TO is where it stops, after FROM")
        step = [str(b) for b in range(lo, hi)]
        if not bars_given:
            span = 1.0
        del a[i:i + 2]
    if len(a) < 2 or (len(a) < 3 and not step):
        print(__doc__)
        return 2
    x, sr = load(a[0])
    if x.shape[1] < 2:
        raise SystemExit("lagchk: the file has one channel; it reads a part hard left against a part hard right")
    bpm = float(a[1])
    bar = 240.0 / bpm
    s16 = bar / 16
    fr = sr / HOP
    left, right = envelope(x, 0), envelope(x, 1)
    prev = None
    for tok in a[2:] + (step or []):
        b = bar_of(tok, bpm)
        a0, a1 = int(b * bar * fr), int((b + span) * bar * fr)
        if a0 < 0 or a1 > len(left):
            print(f"{tok:>10s}: outside the file")
            continue
        top = leads(left, right, a0, a1, int(reach16 * s16 * fr), s16 * fr)
        if step and tok in step:                      # one line a bar, each reading kept next to the one before
            c, found = top[0][0], top[0][1] / fr / s16
            lead = prev = beside(found, prev)
            print(f"{tok:>10s}: right leads by {lead:+.2f} sixteenths (corr {c:.0f}"
                  + (f"; found as {found:+.2f}, a bar {'back' if found < lead else 'on'}" if lead != found else "") + ")")
            continue
        print(f"{tok:>10s}: right leads by " + ", then ".join(f"{lag / fr / s16:+.2f} sixteenths (corr {c:.0f})" for c, lag in top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
