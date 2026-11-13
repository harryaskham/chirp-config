#!/usr/bin/env python3
"""wincut: where a `chirp render --from/--to` window falls in a whole render, so a tool that measures many windows can
render the song ONCE and cut them out (chirp-eco, 13 Nov, for stembal.py and presence.py).

A window render starts from the top anyway (without --preroll), so N windows cost N part-renders; nine of stembal's
took 28 minutes on Common Time, and a presence audit of every section about two hours. The cut is the same samples:
a window render is frames round(start * rate) to round(end * rate) of the whole render, checked against the engine
bit for bit on bars, beats and seconds.

  position(tok, tempo)            a position in seconds: a bar (49, 1-indexed, in 4/4), beats (12b) or seconds (30s)
  window_seconds(canon, windows)  [(start, end)] for FROM-TO[:label] windows, or None when it cannot be worked out here
  frames(s0, s1, rate)            the frame range of a window
  cut(src, dst, s0, s1)           that range of a WAV, written as a WAV

Only songs it can place: a fixed tempo, 4/4, no embedded songs. For the rest window_seconds returns None and the caller
renders window by window, as before. Tests: tools/tests/test_stembal.py, tools/tests/test_presence.py.
"""
import re
import wave


def position(tok, tempo):
    """A `chirp render --from/--to` position in seconds: a bar (49, 1-indexed, in 4/4), beats (12b) or seconds (30s)."""
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([bs]?)", tok.strip())
    if not m:
        return None
    v = float(m.group(1))
    if m.group(2) == "s":
        return v
    beats = v if m.group(2) == "b" else (v - 1) * 4
    return beats * 60.0 / tempo if beats >= 0 else None


def window_seconds(canon, windows):
    """[(start, end)] in seconds for --windows, or None when they cannot be worked out here (a tempo that changes, a
    meter other than 4/4, embedded songs, a position in another form): then each window is rendered by itself."""
    tempo = canon.get("tempo")
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0:
        return None
    if str(canon.get("meter") or "4/4").replace(" ", "") != "4/4" or canon.get("songs"):
        return None
    out = []
    for win in windows:
        b0, _, b1 = win.partition(":")[0].partition("-")
        s0, s1 = position(b0, tempo), position(b1, tempo)
        if s0 is None or s1 is None or s1 <= s0:
            return None
        out.append((s0, s1))
    return out


def frames(s0, s1, rate):
    """The frames of a whole render that a window render of s0..s1 seconds gives."""
    return int(round(s0 * rate)), int(round(s1 * rate))


def cut(src, dst, s0, s1):
    """Seconds s0..s1 of a render, as a window render gives them, written to dst."""
    with wave.open(src, "rb") as w:
        f0, f1 = frames(s0, s1, w.getframerate())
        w.setpos(min(f0, w.getnframes()))
        data = w.readframes(max(0, f1 - f0))
        params = w.getparams()
    with wave.open(dst, "wb") as o:
        o.setparams(params)
        o.writeframes(data)
    return dst
