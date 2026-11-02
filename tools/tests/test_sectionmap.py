import json
import os
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import palette as P  # noqa: E402
import sectionmap as SM  # noqa: E402


def _song(obj):
    d = tempfile.mkdtemp()
    path = os.path.join(d, "s.json")
    with open(path, "w") as f:
        json.dump(obj, f)
    return path


def test_windows_are_whole_phrases_on_a_constant_tempo():
    w = SM.windows(_song({"tempo": 120}), 120.0, 30.0)
    # 30 s at 120 bpm is 60 beats: whole 4-bar phrases make it 64 (32 s); 240 beats in all, the last 48 kept
    assert [(a, b) for a, b, _, _ in w] == [(0, 64), (64, 128), (128, 192), (192, 240)]
    assert [round(ta, 3) for _, _, ta, _ in w] == [0, 32, 64, 96]


def test_a_short_last_window_joins_the_one_before():
    w = SM.windows(_song({"tempo": 120}), 105.0, 30.0)      # 210 beats: 0-64-128-210 (a 18-beat tail joins)
    assert [(a, round(b)) for a, b, _, _ in w] == [(0, 64), (64, 128), (128, 210)]


def test_windows_follow_a_tempo_map():
    song = _song({"tempo": [{"at": "0b", "bpm": 100}, {"at": "96b", "bpm": 140, "ramp": True}]})
    w = SM.windows(song, 60.0, 15.0)
    ts = [ta for _, _, ta, _ in w] + [w[-1][3]]
    assert all(b > a for a, b in zip(ts, ts[1:]))
    assert abs(w[-1][3] - 60.0) < 1e-6
    beats = [a for a, _, _, _ in w]
    assert all(b % 16 == 0 for b in beats)                   # whole 4-bar phrases in beats, not seconds


def _rows():
    rows = []
    for i, (motion, change, like, dl) in enumerate([(0.10, None, None, 0), (0.12, 0.5, 0.80, 0), (0.11, 0.6, 0.85, 0),
                                                    (0.02, 0.05, 0.995, 0.3), (0.09, 0.4, 0.82, 0)]):
        r = {"n": i + 1, "motion": motion, "level": -10.0}
        if change is not None:
            r["change"] = change
        if like is not None:
            r["like"] = {"n": 2, "sim": like, "dlevel": dl, "notes": 0.2 if like > 0.99 else 2.5, "avg": like}
        rows.append(r)
    return rows


def test_flags_mark_a_near_repeat_that_barely_moves():
    rows = _rows()
    SM.flag(rows)
    assert "near-repeat of w2" in rows[3]["flags"] and "static" in rows[3]["flags"]
    assert any(f.startswith("little new") for f in rows[3]["flags"])
    assert not any(f.startswith("near-repeat") for f in rows[1]["flags"])


def test_focus_order_puts_flagged_first_and_rests_a_recent_window():
    rows = _rows()
    SM.flag(rows)
    assert SM.focus_order(rows, [])[0] == 4
    assert 4 not in SM.focus_order(rows, [{"window": 4}])     # focused in the last round: it waits
    assert 4 in SM.focus_order(rows, [{"window": 4}, {"window": 1}, {"window": 2}, {"window": 3}])


def test_compare_reads_identical_windows_as_unchanged():
    rows = [{"n": 1, "level": -10.0, "bright_hz": 900, "density": 3.0, "motion": 0.1, "vec": np.ones(8),
             "chroma": np.arange(12.0), "seq": np.ones((16, 60)), "time": [0.0, 1.0]}]
    x = np.random.default_rng(0).standard_normal((48000, 2)).astype(np.float32)
    c = SM.compare(rows, [dict(rows[0])], x, x.copy(), 48000)[0]
    assert c["change"] == 0.0 and c["dlevel"] == 0.0 and c["melody"] == 0.0 and c["residual_db"] == -99.0


def test_the_note_sequence_hears_a_melody_the_averages_miss():
    # the same pitch classes and the same average energy, one octave apart: the window averages can't tell, the
    # note sequence can (chirper-zero, t8 v26's octave leaps)
    a = np.zeros((16, 60))
    b = np.zeros((16, 60))
    for t in range(16):
        a[t, 24 + (t % 4)] = 3.0
        b[t, 24 + (t % 4) + (12 if t % 2 else 0)] = 3.0
    assert SM.seq_dist(a, a) == 0.0 and SM.seq_sim(a, a) == 1.0
    assert SM.seq_dist(a, b) > 1.0
    sr = 48000
    t = np.arange(sr) / sr
    x = np.sin(2 * np.pi * 440 * t)
    y = x + 0.1 * np.sin(2 * np.pi * 880 * t)
    assert SM.residual_db(x, x, 0, 1, sr) == -99.0
    assert -25 < SM.residual_db(y, x, 0, 1, sr) < -15                       # a tenth's amplitude: about -20 dB


def test_palette_reads_library_bases_and_patch_makeup():
    lib = {"machine-kit": "", "blip": "", "juno-pad": ""}
    assert P.base("machine-kit.cb", lib) == "machine-kit"
    assert P.base("blip amp.d=30ms layers.0.fixed=1700", lib) == "blip"
    assert P.base("babble.patch", lib) is None
    s = P.summary({"synth": {"layers": [{"type": "wind", "exciter": "lips"}, {"type": "modal"}, {"type": "osc"}]},
                   "fx": [{"type": "reverb"}, {"type": "reverb"}, {"type": "tape"}]})
    assert s == "wind:lips+modal:membrane+osc:sine | fx reverb,tape"
