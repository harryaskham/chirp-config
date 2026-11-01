import json
import os
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import compscore as C  # noqa: E402
import likeness as L  # noqa: E402


def _song(tempo, d):
    path = os.path.join(d, "s.json")
    with open(path, "w") as f:
        json.dump({"tempo": tempo}, f)
    return path


def test_tempo_points_parse_like_the_engine():
    d = tempfile.mkdtemp()
    ramp = [{"at": "0b", "bpm": 112}, {"at": "136b", "bpm": 118, "ramp": True},
            {"at": "356b", "meter": "7/8"}, {"at": 400, "bpm": 124, "ramp": True}]
    assert C.tempo_points(_song(ramp, d)) == [(0.0, 112.0, False), (136.0, 118.0, True), (356.0, 118.0, False),
                                              (400.0, 124.0, True)]
    assert C.tempo_points(_song([{"at": "8b", "bpm": 100}, {"at": "16b", "bpm": 90}], d))[0] == (0.0, 100.0, False)
    assert C.tempo_points(_song(120, d)) is None                                         # a single tempo
    assert C.tempo_points(_song([{"at": "0b", "bpm": 120}, {"at": "64b", "bpm": 120, "meter": "7/8"}], d)) is None
    assert C.tempo_points(_song([{"at": "0b", "bpm": 120}, {"at": "4bar", "bpm": 130}], d)) is None   # bars: no warp
    assert C.tempo_points(os.path.join(d, "missing.json")) is None
    assert C.declared_tempo(_song(ramp, d)) == 118.0                                     # unchanged: median of points


def test_map_secs_matches_the_engine_ramp():
    segs = C.tempo_segments([(0.0, 60.0, False), (4.0, 120.0, True)])
    # tempo.rs: a ramp's time is 60/k ln(bpm1/bpm0); 60 -> 120 over 4 beats is 4 ln 2 s (its own unit test)
    assert abs(float(C.map_secs(segs, np.array([4.0]))[0]) - 4 * np.log(2)) < 1e-9
    assert abs(C.map_beats(segs, 4 * np.log(2)) - 4.0) < 1e-9
    assert abs(float(C.map_secs(segs, np.array([6.0]))[0]) - (4 * np.log(2) + 1.0)) < 1e-9   # 120 after the ramp


def _accelerando(pts, beats, sr=L.SR):
    """Eighth-note noise clicks (accented on the beat) placed on the tempo map PTS for BEATS beats."""
    segs = C.tempo_segments(pts)
    at = C.map_secs(segs, np.arange(0, beats, 0.5))
    n = int((at[-1] + 1.0) * sr)
    x = np.zeros(n, dtype=np.float32)
    rng = np.random.default_rng(0)
    for i, t in enumerate(at):
        s = int(t * sr)
        amp, ln = (1.0, 2000) if i % 2 == 0 else (0.4, 600)
        x[s:s + ln] += amp * rng.standard_normal(ln).astype(np.float32) * np.exp(-np.arange(ln) / (ln / 4))
    return np.stack([x, x], axis=1)


def test_the_map_puts_an_accelerando_on_one_grid():
    pts = [(0.0, 100.0, False), (96.0, 140.0, True)]
    x = _accelerando(pts, 96)
    base = {"x": x, "F": L.Feat(x), "bpm": 120.0, "density": 8.0, "tempo_map": pts}
    off = C.m_rhythm({**base, "album": {"params": {}}})
    on = C.m_rhythm({**base, "album": {"params": {"rhythm": {"map": True}}}})
    assert "tempo_map" not in off[1] and on[1]["tempo_map"] is True
    assert on[1]["offgrid_share"] < 0.05                   # every eighth on the grid in beat time
    assert off[1]["offgrid_share"] >= on[1]["offgrid_share"] + 0.08   # one 120 grid smears a 100 -> 140 ramp (0.12)


def test_the_map_is_opt_in_and_needs_a_map():
    pts = [(0.0, 100.0, False), (96.0, 140.0, True)]
    x = _accelerando(pts, 96)
    base = {"x": x, "F": L.Feat(x), "bpm": 120.0, "density": 8.0}
    plain = C.m_rhythm({**base, "album": {"params": {}}})
    assert C.m_rhythm({**base, "tempo_map": None, "album": {"params": {"rhythm": {"map": True}}}}) == plain
    assert C.m_rhythm({**base, "tempo_map": pts, "album": {"params": {}}}) == plain
