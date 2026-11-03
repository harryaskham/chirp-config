"""compscore's spectrum term names the worst band's frequency and signed level, so a deficit reads as one."""
import os
import sys
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import compscore as C  # noqa: E402


def _ctx(ours_logb, env):
    return {"envelope": env, "album": {}, "F": SimpleNamespace(logb=ours_logb[:, None])}


def test_a_short_band_reads_negative_with_its_frequency():
    env = np.zeros(40)
    ours = np.zeros(40)
    live = np.flatnonzero(C.LIVE)
    k = int(live[6])
    ours[k] = -12.0          # this song is 12 dB short at band k
    s, d = C.m_spectrum(_ctx(ours, env))
    assert d["worst_band"] == k
    assert d["worst_band_hz"] == int(round(C.BAND_HZ[k]))
    assert d["worst_band_db"] < -10      # a deficit (the level normalisation shifts it slightly)
    assert d["mean_excess_db"] > 0 and s < 100


def test_a_loud_band_reads_positive():
    env = np.zeros(40)
    ours = np.zeros(40)
    k = int(np.flatnonzero(C.LIVE)[20])
    ours[k] = 9.0
    _, d = C.m_spectrum(_ctx(ours, env))
    assert d["worst_band"] == k and d["worst_band_db"] > 7
