import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import compscore as C  # noqa: E402

CHROMA_A = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
CHROMA_B = [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]


def _f(tempo, chroma, density=2.0, bpm=None):
    s = sum(chroma)
    f = {"tempo": tempo, "chroma": [c / s for c in chroma], "density": density}
    if bpm is not None:
        f["bpm"] = bpm
    return f


def test_a_flipped_onset_estimate_no_longer_reads_as_a_copy():
    # chirper-three, 8 Nov: t8's estimate flipped onto t4's exact 87.9; the declared tempos (150 vs 108.9) differ
    root = tempfile.mkdtemp()
    old = C.ROOT
    C.ROOT = root
    try:
        before, _ = C.m_distinct({"id": "t8", "me": _f(87.9, CHROMA_A), "bpm": None, "others": {"t4": _f(87.9, CHROMA_A)}})
        after, d = C.m_distinct({"id": "t8", "me": _f(87.9, CHROMA_A), "bpm": 150.0,
                                 "others": {"t4": _f(87.9, CHROMA_A, bpm=108.9)}})
    finally:
        C.ROOT = old
    assert before < 1e-3                 # the old measure: same estimate, same notes -> a copy
    assert after == 100.0
    assert d["similarity"] < 0.7


def test_others_declared_tempo_is_read_from_the_song_file():
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, "songs"))
    with open(os.path.join(root, "songs", "other.json"), "w") as f:
        json.dump({"tempo": 90}, f)
    old = C.ROOT
    C.ROOT = root
    try:
        assert C.distinct_tempo("other", {"tempo": 187.5}) == 90.0       # a stale cache without bpm
        assert C.distinct_tempo("nosong", {"tempo": 187.5}) == 187.5     # no song file: the estimate
        assert C.distinct_tempo("other", {"tempo": 187.5, "bpm": 95}) == 95.0
        assert C.distinct_tempo("other", {"tempo": 187.5}, bpm=100) == 100.0
    finally:
        C.ROOT = old


def test_no_declared_tempo_anywhere_is_the_old_measure():
    me, other = _f(120.0, CHROMA_A), {"x": _f(118.0, CHROMA_B)}
    root = tempfile.mkdtemp()
    old = C.ROOT
    C.ROOT = root
    try:
        new, _ = C.m_distinct({"id": "me", "me": me, "bpm": None, "others": other})
    finally:
        C.ROOT = old
    import numpy as np
    import likeness as L
    c = max(0.0, L._cos(np.array(me["chroma"]) - 1 / 12, np.array(other["x"]["chroma"]) - 1 / 12))
    t = float(np.exp(-abs(np.log2(120.0 / 118.0)) * 12))
    s = (c + t + 1.0) / 3
    assert abs(new - float(100 * np.clip((1 - s) / 0.15, 0, 1))) < 1e-9
