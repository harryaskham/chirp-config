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


def test_gain_matching_and_the_residual_floor():
    # a whole-song gain change is matched away; one reworked window cannot pull the gain (the least-touched window)
    sr = 1000
    rng = np.random.default_rng(1)
    old = rng.standard_normal(10 * sr)
    new = old * 0.96
    new[3 * sr:4 * sr] = rng.standard_normal(sr)              # window 4 rewritten
    spans = [(i, i + 1) for i in range(10)]
    g = SM.match_gain(new, old, spans, sr)
    assert abs(g - 0.96) < 1e-9
    cmp_ = [{"residual_db": SM.residual_db(new, old * g, a, b, sr)} for a, b in spans]
    floor, cut = SM.residual_floor(cmp_)
    assert floor == -99.0 and cut == -40.0                      # untouched windows read as untouched
    assert [i for i, c in enumerate(cmp_) if c["residual_db"] > cut] == [3]
    # a song whose every window moved (the mastering gain through the master compressors): read against its floor
    moved = [{"residual_db": r} for r in (-29.4, -28.4, -28.5, -3.1, -25.0, -29.1)]
    floor, cut = SM.residual_floor(moved)
    assert floor == -28.4 and cut == -18.4
    assert [i for i, c in enumerate(moved) if c["residual_db"] > cut] == [3]


def test_gain_matching_survives_edits_in_most_windows():
    # chirper-zero's t5 overshoot (6 Nov): a pitch edit decorrelated 6 of 8 windows, each window's least-squares gain
    # shrank, and the median put the untouched w1 at -13.5 dB. The least-touched window carries the true gain.
    sr = 1000
    rng = np.random.default_rng(2)
    old = rng.standard_normal(8 * sr)
    new = old * 0.99988                                        # the loudness normalisation's reaction
    for w in range(2, 8):                                       # windows 3-8 edited: half-decorrelated
        a, b = w * sr, (w + 1) * sr
        new[a:b] = 0.5 * new[a:b] + 0.5 * rng.standard_normal(sr)
    spans = [(i, i + 1) for i in range(8)]
    g = SM.match_gain(new, old, spans, sr)
    assert abs(g - 0.99988) < 1e-9
    assert SM.residual_db(new, old * g, 0, 1, sr) < -60       # w1 reads as untouched again
    # nothing close enough to anchor on: no gain match at all
    assert SM.match_gain(rng.standard_normal(8 * sr), old, spans, sr) == 1.0
    # the 'changed' line stays at -40 while an audible window is untouched; silent windows (-99) never anchor
    cmp_ = [{"residual_db": r} for r in (-76.0, -75.5, -15.0, -12.0, -9.0, -14.0, -11.0, -13.0)]
    assert SM.residual_floor(cmp_, [-20.0] * 8) == (-13.5, -40.0)
    assert SM.residual_floor(cmp_) == (-13.5, -3.5)                    # without levels: the old whole-song reading
    moved = [{"residual_db": r} for r in (-99.0, -29.4, -28.4, -28.5, -3.1, -25.0, -29.1)]
    assert SM.residual_floor(moved, [-90.0] + [-20.0] * 6) == (-28.5, -18.5)   # silent w1 is no anchor


def _clicks(times, sr=48000, dur=None):
    x = np.zeros(int(sr * (dur or (times[-1] + 1.0))), np.float32)
    burst = (np.random.default_rng(0).standard_normal(240) * np.hanning(240)).astype(np.float32)
    for t in times:
        i = int(t * sr)
        x[i:i + 240] += burst[:len(x) - i]
    return np.stack([x, x], 1)


def test_groove_hears_a_shuffle_that_texture_misses():
    # 120 bpm, 16 bars: straight 8ths, then a triplet shuffle (off-beats at 2/3 of the beat); same clicks, same density
    song = _song({"tempo": 120, "tracks": []})
    clock, _ = SM.beat_clock(song)
    straight = [b * 0.5 for b in range(64)] + [(b + 0.5) * 0.5 for b in range(64)]
    shuffle = [32 + b * 0.5 for b in range(64)] + [32 + (b + 2 / 3) * 0.5 for b in range(64)]
    x = _clicks(sorted(straight + shuffle), dur=65.0)
    env, t = SM.onset_env(x, 48000)
    h1 = SM.groove_hist(env, t, clock, 0, 32)
    h2 = SM.groove_hist(env, t, clock, 32, 64)
    h3 = SM.groove_hist(env, t, clock, 64, 96)
    h4 = SM.groove_hist(env, t, clock, 96, 128)
    assert 1 - SM._cos(h1, h2) < 0.02                       # straight vs straight
    assert 1 - SM._cos(h3, h4) < 0.02                       # shuffle vs shuffle
    assert 1 - SM._cos(h2, h3) >= SM.GROOVE_NEW             # straight -> shuffle
    # the off-beat mass sits at half a beat, then at two thirds of one
    assert int(np.argmax(h2[6:18])) + 6 == SM.GROOVE_BINS // 2
    assert int(np.argmax(h3[6:18])) + 6 == 2 * SM.GROOVE_BINS // 3


def test_a_new_groove_is_never_little_new():
    rows = _rows()
    rows[3]["groove"] = SM.GROOVE_NEW + 0.05
    SM.flag(rows)
    assert not any(f.startswith("little new") for f in rows[3]["flags"])
    assert "static" in rows[3]["flags"]                     # the window's own motion still reads as it did
