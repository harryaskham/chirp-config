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


# ── a ledger mark is found again after the song is reshaped (14 Nov: Plain Hunt v5, 96 bpm / 483 beats -> 120 / 648) ──
def _grid(total, w=64):
    """Today's map as rows: windows of W beats up to TOTAL, with what print_map reads."""
    edges = list(range(0, int(total), w)) + [total]
    if len(edges) > 2 and edges[-1] - edges[-2] < w / 2:
        edges.pop(-2)
    return [{"n": i + 1, "beats": [float(a), float(b)], "time": [a / 2.0, b / 2.0], "level": -13.0, "bright_hz": 600, "density": 6.0,
             "motion": 0.04} for i, (a, b) in enumerate(zip(edges[:-1], edges[1:]))]


def test_the_window_width_is_the_one_the_map_uses():
    for tempo, dur in ((120, 120.0), (96, 301.0), (126, 783.0), (108, 299.0)):
        song = _song({"tempo": tempo})
        w = SM.window_beats(song, tempo)
        assert all(b - a == w for a, b, _, _ in SM.windows(song, dur)[:-1])
    assert SM.window_beats(_song({"tempo": 96}), 96) == 48 and SM.window_beats(_song({"tempo": 120}), 120) == 64


def test_a_mark_carries_the_shape_it_was_made_on():
    song = _song({"tempo": 120, "length": "648b"})
    assert SM.declared_beats(song) == 648.0
    assert SM.shape(song) == {"tempo": 120.0, "of": 648.0}
    assert SM.shape(song, 9) == {"tempo": 120.0, "of": 648.0, "beats": [512.0, 576.0]}
    assert SM.shape(song, 11)["beats"] == [640.0, 648.0]                     # the last window stops where the song does
    assert SM.shape(_song({"tempo": 96}), 2) == {"tempo": 96.0, "beats": [48.0, 96.0]}   # no declared length
    d = tempfile.mkdtemp()
    with open(os.path.join(d, "s.yaml"), "w") as f:
        f.write('about: "x"\ntempo: 108\nlength: "532b"\ntracks: []\n')
    assert SM.shape(os.path.join(d, "s.yaml"), 1) == {"tempo": 108.0, "of": 532.0, "beats": [0.0, 64.0]}
    assert SM.shape(_song({"tempo": [{"at": 0, "bpm": 120}, {"at": 64, "bpm": 90}]}), 3) == {}   # a tempo map: by number
    assert SM.shape(_song({}), 3) == {}


def test_a_mark_is_placed_on_todays_window():
    now = {"tempo": 120.0, "of": 648.0}
    rows = _grid(653)                                                        # ten windows of 64 beats, the last to 653
    assert len(rows) == 10
    assert SM.place({"window": 9}, rows, now) == (9, False)                  # marked before 14 Nov: by its number
    same = {"window": 9, "beats": [512.0, 576.0], "tempo": 120.0, "of": 648.0}
    assert SM.place(same, rows, now) == (9, False)
    assert SM.place(same, _grid(653, 32), now) == (17, False)                # the same song mapped on shorter windows
    # Plain Hunt: marked on v4 (96 bpm, 480 beats, windows of 48) as w9 = beats 384-432, the climb; v5 is 120 bpm and 648
    v4 = {"window": 9, "version": "v4", "beats": [384.0, 432.0], "tempo": 96.0, "of": 480.0}
    assert SM.place(v4, rows, now) == (9, True)                              # 518-583 of today's beats: still w9, a guess
    early = {"window": 2, "beats": [48.0, 96.0], "tempo": 96.0, "of": 480.0}
    assert SM.place(early, _grid(960), {"tempo": 96.0, "of": 960.0}) == (3, True)   # the song doubled: it is w3's music now
    assert SM.place(dict(v4, of=None), rows, now) == (9, True)               # no length to scale by: its number, as a guess
    assert SM.place(v4, [{"n": 1, "beats": [None, None]}], now) == (9, False)   # a map without beats: by number


def test_the_placed_ledger_feeds_the_focus_order_and_the_map_says_so(capsys):
    song = _song({"tempo": 96, "length": "960b"})
    rows = _grid(960)
    ledger = SM.placed_ledger([{"window": 2, "version": "v4", "at": "2026-11-14T19:31:39Z", "who": "zero", "beats": [48.0, 96.0],
                                "tempo": 96.0, "of": 480.0},
                               {"window": 5, "at": "2026-11-14T20:00:00Z", "who": "zero"}], rows, song)
    assert [(e["window"], e.get("marked_as"), e.get("reshaped")) for e in ledger] == [(3, 2, True), (5, None, None)]
    order = SM.focus_order(rows, ledger)
    assert 3 not in order and 5 not in order and 2 in order                  # w3 rests (it holds the marked music), w2 does not
    SM.print_map("x", song, rows, 480.0, ledger)
    out = capsys.readouterr().out
    line3 = next(ln for ln in out.splitlines() if ln.startswith("  3 "))
    assert "focused 2026-11-14T19:31 by zero (about here: marked on v4 as w2, and the song's tempo or length has changed since)" in line3
    line5 = next(ln for ln in out.splitlines() if ln.startswith("  5 "))
    assert line5.rstrip().endswith("focused 2026-11-14T20:00 by zero")


# ── what enters in a static window (14 Nov, Common Time v48: "static" was "the arrival is masked") ──
def test_entries_are_notes_after_two_bars_of_silence_one_a_track_a_window():
    rows = _grid(256)                                                        # four windows of 64 beats
    canon = {"tracks": [
        {"name": "five", "notes": [{"at": 4.0 * i, "len": 3.9} for i in range(64)]},                 # never rests: enters once, at 0
        {"name": "eleven", "notes": [{"at": 100.0, "len": 2}, {"at": 104.0, "len": 2}, {"at": 200.0, "len": 2}]},
        {"name": "kit", "tracks": [{"name": "china", "notes": [{"at": 100.0, "len": 1}, {"at": 107.0, "len": 1},
                                                               {"at": 118.0, "len": 1}]}]},
        {"name": "silent", "notes": []}]}
    got = SM.entries(canon, rows)
    assert got[1] == [("five", 0.0)]
    assert got[2] == [("eleven", 100.0), ("china", 100.0)]                   # 107 is 6 beats after 101: not an entry; 118 is, but
    assert got[4] == [("eleven", 200.0)]                                     # the window already has the china's first
    assert 3 not in got
    assert SM.entries(None, rows) == {} and SM.entries(canon, [{"n": 1, "beats": [None, None]}]) == {}


def test_a_static_window_says_what_enters_and_how_to_weigh_it():
    rows = _grid(256)
    rows[1]["flags"], rows[2]["flags"], rows[3]["flags"] = ["static"], ["static", "little new vs w2"], ["little new vs w3"]
    enters = {2: [("eleven", 100.0), ("china", 100.0), ("lead", 120.0)], 4: [("eleven", 200.0)]}
    lines = SM.entry_lines("x", rows, enters, lambda b: [b / 2.0])
    assert lines == [
        "  w2 static, and these ENTER in it: eleven, china at 0:50; lead at 1:00. How loud against what was already playing: "
        "presence.py x --windows 100b-116b --preroll 8",
        "  w3 static: nothing enters in it (the same parts throughout, or parts that never rested two bars)"]


# ── rhythm inside a window (15 Nov, Plain Hunt v9: a snare moved in time changed no tone, harmony or level) ──
def _attacks(strokes, bars=8, hop=0.005, tempo=120.0, bpb=4):
    """An onset envelope at 5 ms for `bars` bars of `bpb` beats: strokes(bar) gives the beats struck in that bar."""
    spb = 60.0 / tempo
    times = np.arange(0, bars * bpb * spb, hop)
    env = np.zeros(len(times))
    for bar in range(bars):
        for beat in strokes(bar):
            env[int(round((bar * bpb + beat) * spb / hop))] += 1.0
    return env, times, (lambda b: np.atleast_1d(np.asarray(b, float)) * spb)


def test_rhythm_is_nothing_for_a_bar_that_repeats_and_plain_for_a_stroke_that_slides():
    kick = [0.0, 1.0, 2.0, 3.0]
    env, t, clock = _attacks(lambda bar: kick + [1.0, 3.0])                       # a backbeat, every bar alike
    assert SM.rhythm_motion(env, t, clock, 0.0, 32.0) < 0.01
    env, t, clock = _attacks(lambda bar: kick + [1.0 + 0.25 * (bar % 4), 3.0 + 0.25 * (bar % 4)])   # a sixteenth later each bar
    assert SM.rhythm_motion(env, t, clock, 0.0, 32.0) > SM.RHYTHM_MOVES
    env, t, clock = _attacks(lambda bar: [] if bar in (3, 4) else kick + [1.0, 3.0])                # two bars of rest
    assert SM.rhythm_motion(env, t, clock, 0.0, 32.0) < 0.01                      # a rest is not a change of rhythm
    assert SM.rhythm_motion(env, t, clock, 0.0, 4.0) is None                      # one bar: nothing to compare
    env, t, clock = _attacks(lambda bar: [0.0, 1.5, 2.0], bpb=3)                  # bars of three beats, read in their own meter
    assert SM.rhythm_motion(env, t, clock, 0.0, 24.0, bpb=3.0) < 0.01
    assert SM.rhythm_motion(env, t, clock, 0.0, 24.0) > 0.3                       # and read as fours, nothing lines up
    early = np.roll(env, -1)                                                      # every attack 5 ms early: still each bar's own
    assert SM.rhythm_motion(early, t, clock, 3.0, 24.0, bpb=3.0) < 0.01           # (from the second bar: the roll wraps the first)


def test_a_static_window_whose_rhythm_moves_is_static_in_tone():
    rows = _rows()
    for r, v in zip(rows, (0.08, 0.10, 0.09, 0.23, 0.12)):
        r["rhythm"] = v
    SM.flag(rows)
    assert "static in tone" in rows[3]["flags"] and "static" not in rows[3]["flags"]
    assert SM.is_static(rows[3]) and not SM.is_static(rows[1])
    low, mid, moves = SM.rhythm_line(rows)
    assert (round(low, 3), round(mid, 3), round(moves, 3)) == (0.09, 0.10, 0.15)   # the top quarter is 0.12: the floor holds
    rows = _rows()
    for r, v in zip(rows, (0.02, 0.03, 0.02, 0.05, 0.03)):                        # a steady song: its "most moving" window
        r["rhythm"] = v                                                           # still repeats bar for bar
    SM.flag(rows)
    assert "static" in rows[3]["flags"]
    assert SM.rhythm_line(_rows()) == (None, None, None)                          # no rhythm figures: as before


def test_the_static_lines_say_which_way_the_rhythm_reads():
    rows = _grid(320)                                                             # five windows
    for r, v, f in zip(rows, (0.07, 0.23, 0.12, 0.10, 0.12), (["static"], ["static in tone"], ["static"], [], ["little new vs w4"])):
        r["rhythm"], r["flags"] = v, f
    lines = SM.entry_lines("x", rows, {3: [("lead", 130.0)]}, lambda b: [b / 2.0])
    assert lines == [
        "  w1 static (and its rhythm repeats: 0.070 bar to bar, this song's median 0.120): nothing enters in it (the same parts "
        "throughout, or parts that never rested two bars)",
        "  w2 static in tone (its rhythm MOVES: 0.230 bar to bar, this song's median 0.120): nothing enters in it (the same parts "
        "throughout, or parts that never rested two bars)",
        "  w3 static (rhythm 0.120 bar to bar, this song's median 0.120), and these ENTER in it: lead at 1:05. How loud against what "
        "was already playing: presence.py x --windows 130b-146b --preroll 8"]


def test_an_ab_carries_the_rhythm_was_and_now():
    def row(n, rhythm):
        v = np.ones(8)
        return {"n": n, "level": -12.0, "bright_hz": 600, "density": 6.0, "motion": 0.03, "vec": v, "chroma": v, "seq": None,
                "rhythm": rhythm}
    cmp_ = SM.compare([row(1, 0.228), row(2, None)], [row(1, 0.068), row(2, 0.1)])
    assert cmp_[0]["rhythm"] == [0.068, 0.228] and "rhythm" not in cmp_[1]


def _plan_for_notes():
    """Twelve bars of 4/4. riff: a two-bar figure. octaves: one figure, an octave higher every bar. harm: one figure for
    six bars, then the same places a third higher. short: six notes a bar, four of them in bar 4. late: rests eight bars,
    then loops. The kit: a kick that loops and a tom whose place moves every bar."""
    def bar(k, places_pitches):
        return [{"at": k * 4 + pl, "len": 0.5, "pitch": p} for pl, p in places_pitches]
    a, b = [(0, "F2"), (1, "Ab2"), (2.5, "C3")], [(0, "F2"), (1.5, "Eb2"), (3, "C3")]
    six = [(i * 0.5, p) for i, p in enumerate(["F2", "G2", "Ab2", "Bb2", "C3", "Db3"])]
    return {"tempo": 120, "tracks": [
        {"name": "riff", "notes": [n for k in range(12) for n in bar(k, a if k % 2 == 0 else b)]},
        {"name": "octaves", "notes": [n for k in range(12) for n in bar(k, [(0, f"F{1 + k % 4}"), (2, f"C{2 + k % 4}")])]},
        {"name": "harm", "notes": [n for k in range(12) for n in bar(k, a if k < 6 else [(0, "A2"), (1, "C3"), (2.5, "E3")])]},
        {"name": "short", "notes": [n for k in range(12) for n in bar(k, six[:4] if k == 3 else six)]},
        {"name": "late", "notes": [n for k in range(8, 12) for n in bar(k, a)]},
        {"name": "kit", "tracks": [{"name": "drums", "notes": [n for k in range(12)
                                                               for n in bar(k, [(0, "k"), (2, "k"), ((k * 0.75) % 4, "t1")])]}]},
    ]}


def test_the_plans_notes_part_by_part_loop_change_or_never_settle():
    rows = [{"n": 1, "beats": [0.0, 48.0], "flags": ["static"]}, {"n": 2, "beats": [48.0, 96.0], "flags": []}]
    got = SM.note_motion(_plan_for_notes(), rows)
    assert set(got) == {1}                                                   # nothing plays in the second window
    assert got[1]["loops"] == ["riff", "octaves", "short", "late", "drums:k"]   # an octave up is the same notes; a figure cut
    assert got[1]["changes"] == [("harm", 24.0)]                             # short is the figure; an entry is not a change
    assert got[1]["moves"] == ["drums:t1"] and got[1]["mixed"] == []         # one piece of a kit is a part of its own
    assert SM.note_motion(None, rows) == {} and SM.note_motion(_plan_for_notes(), [{"n": 1, "beats": [None, None]}]) == {}
    half = SM.note_motion(_plan_for_notes(), [{"n": 1, "beats": [0.0, 24.0]}])   # the harmony is not in the first six bars
    assert half[1]["changes"] == [] and "harm" in half[1]["loops"] and "late" not in half[1]["loops"]


def test_a_static_window_says_what_its_notes_do():
    rows = [{"n": 1, "beats": [0.0, 48.0], "flags": ["static"]}]
    clock = lambda b: np.atleast_1d(np.asarray(b, float)) * 0.5  # noqa: E731
    motion = SM.note_motion(_plan_for_notes(), rows)
    lines = SM.note_lines(rows, motion, clock)
    head = "  w1 by the plan's notes (part by part; a note is its place in the bar and its pitch class): "
    assert len(lines) == 1 and lines[0].startswith(head + "5 parts loop; ")
    assert "these CHANGE in it (a loop, then other notes): harm at 0:12 (bar 7)" in lines[0]
    assert "these NEVER SETTLE (most of their bars repeat nothing near them): drums:t1" in lines[0]
    assert lines[0].endswith("Static in its SOUND, not in its notes: the flag cannot hear which notes; listen before rewriting it")
    assert SM.note_lines([{**rows[0], "flags": ["little new vs w0"]}], motion, clock) == []     # only under a static window
    loop = {"tempo": 120, "tracks": [_plan_for_notes()["tracks"][0]]}
    only = SM.note_lines(rows, SM.note_motion(loop, rows), clock)
    assert only == [head + "1 part loops"]
