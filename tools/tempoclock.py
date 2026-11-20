#!/usr/bin/env python3
"""tempoclock: one clock for a song's tempo, a number OR a tempo map, so a tool need not assume one tempo.

    import tempoclock
    c = tempoclock.of(doc.get("tempo"))        # a number, a numeric string, a map [{at, bpm[, ramp]}, ...] or None
    c.secs(beat)      seconds at a beat (a number or a list of numbers)
    c.beats(secs)     the beat at a time in seconds (a number or a list)
    c.bpm_at(beat)    the tempo in force at a beat
    c.at(position)    the beat of a written position: 12, "96b", "8bar", "1.5s", "200ms"
    c.bpm             the tempo at beat 0 (for a tool that prints one figure)
    c.mapped          True when the tempo changes
    tempoclock.of_song(path)                   # the same, from a song file's top-level tempo (compscore.raw_tempo)

A map follows the engine (chirp-core tempo.rs) as tools/compscore.py does: points sorted by beat, a point at beat 0
added when the first is later, a point with no bpm holding the previous one's (a meter change), and a segment RAMPS
toward the next point when THAT point says `ramp` (the tempo changes linearly in beats). Positions must be in beats
(`"64b"` or a number): a map placed in bars or seconds raises ValueError, which says so; a tool should let that be
seen and not fall back to one tempo. tools/tests/test_tempoclock.py holds this to compscore's and drumpunch's
clocks. Why (bd-10e881, 20 Nov 2026): twelve tools read `tempo` as one number, so a song that changed gear wrote
the change into its note positions instead of a tempo map (Slow Enough to Count v18; chirper-three's list).
"""
import math
import re

DEFAULT = 120.0


def points(tempo):
    """[(beat, bpm, ramp)] for a tempo MAP value, sorted, with a point at beat 0; None for a single tempo (a number,
    a numeric string, None, an empty list, or a map whose tempo never changes). ValueError for a map this cannot place."""
    if not isinstance(tempo, list) or not tempo:
        return None
    pts, prev = [], None
    for p in tempo:
        if not isinstance(p, dict):
            raise ValueError(f"tempoclock: a tempo map's point must be a mapping, not {p!r}")
        at = p.get("at", 0)
        m = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*b?\s*", at) if isinstance(at, str) else None
        if isinstance(at, (int, float)) and not isinstance(at, bool):
            beat = float(at)
        elif m:
            beat = float(m.group(1))
        else:
            raise ValueError(f"tempoclock: a tempo map's `at` must be in beats ('64b' or a number), not {at!r}")
        bpm = float(p["bpm"]) if p.get("bpm") is not None else prev
        if bpm is None or not 1.0 <= bpm <= 1000.0:
            raise ValueError(f"tempoclock: a tempo map's bpm must be between 1 and 1000, not {p.get('bpm')!r}")
        pts.append((beat, bpm, bool(p.get("ramp")) and p.get("bpm") is not None))
        prev = bpm
    pts.sort(key=lambda q: q[0])
    if pts[0][0] > 0:
        pts.insert(0, (0.0, pts[0][1], False))
    if len({b for _, b, _ in pts}) < 2:
        return None
    return pts


def _seg_secs(bpm0, k, db):
    if abs(k) < 1e-12:
        return db * 60.0 / bpm0
    return 60.0 / k * math.log(max((bpm0 + k * db) / bpm0, 1e-9))


class Clock:
    """Beats <-> seconds on one tempo or on a tempo map (see the module's docstring)."""

    def __init__(self, tempo, default=DEFAULT):
        pts = points(tempo)
        if pts is None:
            if isinstance(tempo, list) and tempo:                # a map that never changes: its one tempo
                one = next((p.get("bpm") for p in tempo if isinstance(p, dict) and p.get("bpm") is not None), None)
            else:
                one = tempo
            try:
                bpm = float(one) if one else float(default)
            except (TypeError, ValueError):
                raise ValueError(f"tempoclock: a tempo must be a number or a tempo map, not {tempo!r}")
            pts = [(0.0, bpm, False)]
        self.mapped = len(pts) > 1
        self.b0, self.t0, self.v0, self.k = [], [], [], []
        for i, (b, bpm, _) in enumerate(pts):
            nxt = pts[i + 1] if i + 1 < len(pts) else None
            kk = (nxt[1] - bpm) / (nxt[0] - b) if nxt and nxt[2] and nxt[0] > b else 0.0
            t = 0.0 if not self.b0 else self.t0[-1] + _seg_secs(self.v0[-1], self.k[-1], b - self.b0[-1])
            self.b0.append(b)
            self.t0.append(t)
            self.v0.append(bpm)
            self.k.append(kk)
        self.bpm = self.v0[0]

    def _seg(self, xs, x):
        i = 0
        for j, v in enumerate(xs):
            if x >= v:
                i = j
        return i

    def _secs(self, beat):
        i = self._seg(self.b0, beat)
        return self.t0[i] + _seg_secs(self.v0[i], self.k[i], float(beat) - self.b0[i])

    def _beats(self, secs):
        i = self._seg(self.t0, secs)
        dt = float(secs) - self.t0[i]
        if abs(self.k[i]) < 1e-12:
            return self.b0[i] + dt * self.v0[i] / 60.0
        return self.b0[i] + self.v0[i] * (math.exp(self.k[i] * dt / 60.0) - 1.0) / self.k[i]

    def secs(self, beat):
        """Seconds at BEAT (a number, or a list or tuple of numbers: then a list)."""
        return [self._secs(b) for b in beat] if isinstance(beat, (list, tuple)) else self._secs(beat)

    def beats(self, secs):
        """The beat at SECS seconds (a number, or a list or tuple: then a list)."""
        return [self._beats(s) for s in secs] if isinstance(secs, (list, tuple)) else self._beats(secs)

    def at(self, value):
        """The beat of a POSITION written as an automation point or a mark is: a number (beats), "96b", "8bar" or
        "8bars" (4/4, counted from 0), "1.5s", "200ms" (seconds from the song's start, through the map)."""
        if isinstance(value, bool):
            raise ValueError(f"not a position: {value!r}")
        if isinstance(value, (int, float)):
            return float(value)
        s = str(value).strip()
        for suffix in ("bars", "bar", "ms", "s", "b"):
            if s.endswith(suffix):
                v = float(s[:-len(suffix)])
                return v * 4.0 if suffix in ("bars", "bar") else self._beats(v / 1000.0 if suffix == "ms" else v) if suffix != "b" else v
        return float(s)

    def bpm_at(self, beat):
        """The tempo in force at BEAT (inside a ramp, the tempo reached there)."""
        i = self._seg(self.b0, beat)
        return self.v0[i] + self.k[i] * (float(beat) - self.b0[i])


def of(tempo, default=DEFAULT):
    """A Clock for a tempo value: a number, a numeric string, a tempo map, or None (then DEFAULT bpm)."""
    return Clock(tempo, default)


def of_song(path, default=DEFAULT):
    """A Clock for a song file's top-level tempo, read as compscore reads it (a generator-written YAML song too)."""
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import compscore
    return Clock(compscore.raw_tempo(path), default)
