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

Only songs it can place: one tempo or a tempo map placed in beats (tools/tempoclock.py), 4/4 throughout, no embedded
songs. For the rest window_seconds returns None and the caller renders window by window, as before.
Tests: tools/tests/test_stembal.py, tools/tests/test_presence.py.
"""
import re
import wave


def clock_of(tempo):
    """The tempoclock for a tempo as a plan gives it: a number, a tempo MAP placed in beats with no change of meter, or
    a clock already; None for anything this cannot place (a map with a meter change: its bars are not fours; a map
    placed in bars or seconds; no tempo at all)."""
    import tempoclock
    if isinstance(tempo, tempoclock.Clock):
        return tempo
    if isinstance(tempo, bool):
        return None
    if isinstance(tempo, (int, float)):
        return tempoclock.of(tempo) if tempo > 0 else None
    if isinstance(tempo, list) and tempo:
        if any(not isinstance(p, dict) or p.get("meter") is not None for p in tempo):
            return None
        try:
            return tempoclock.of(tempo)
        except ValueError:
            return None
    return None


def position(tok, tempo):
    """A `chirp render --from/--to` position in seconds: a bar (49, 1-indexed, in 4/4), beats (12b) or seconds (30s).
    `tempo` is a number, a tempo map as the plan gives it, or a tempoclock (bd-10e881: a map is followed)."""
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([bs]?)", tok.strip())
    if not m:
        return None
    v = float(m.group(1))
    if m.group(2) == "s":
        return v
    beats = v if m.group(2) == "b" else (v - 1) * 4
    clock = clock_of(tempo)
    return clock.secs(beats) if clock is not None and beats >= 0 else None


def songs_only_as_layers(canon):
    """True when the plan embeds no songs, or every embedded song is used, and used only, as a synth layer's `song`
    (a sampler source, which does not move the song's clock). An embedded song placed as a note, named in a score
    string (`@NAME`) or not referenced at all is False: those are rendered window by window."""
    names = set(canon.get("songs") or {})
    if not names:
        return True
    used, other = set(), []

    def walk(x, path, key):
        if isinstance(x, dict):
            for k, v in x.items():
                if not (path == "" and k == "songs"):
                    walk(v, path + "." + k, k)
        elif isinstance(x, list):
            for v in x:
                walk(v, path + "[]", key)
        elif isinstance(x, str):
            if key == "song" and x in names and ".synth.layers[]" in path:
                used.add(x)
            elif (key == "song" and x in names) or any("@" + n in x for n in names):
                other.append(path)
    walk(canon, "", None)
    return not other and used == names


def window_seconds(canon, windows):
    """[(start, end)] in seconds for --windows, or None when they cannot be worked out here (a tempo map with a change
    of meter or placed in bars or seconds, a meter other than 4/4, embedded songs placed other than as a sampler
    layer's source, a position in another form): then each window is rendered by itself. A tempo map placed in beats
    is followed (checked against the engine bit for bit across a change of tempo, 20 Nov). Embedded songs that are
    only a synth layer's `song` (tape samples: Common Time, Still Owing, The Other Hand) leave the song's clock alone
    and are cut like any other (one whole render cut into windows is bit for bit the window rendered by itself:
    chirper-zero on Common Time v72, bars 56-71; chirp-eco on The Other Hand v34, bars 30-40 and 100-106, 24 Nov)."""
    if "tracks" not in canon:                  # not a plan (it could not be read): do not guess
        return None
    clock = clock_of(canon.get("tempo", 120.0))    # the plan leaves out a tempo of 120, the engine's default
    if clock is None:
        return None
    if str(canon.get("meter") or "4/4").replace(" ", "") != "4/4" or not songs_only_as_layers(canon):
        return None
    out = []
    for win in windows:
        b0, _, b1 = win.partition(":")[0].partition("-")
        s0, s1 = position(b0, clock), position(b1, clock)
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
