import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import compscore as C  # noqa: E402


def test_novelty_thresholds_opt_in():
    assert C.novelty_thresholds({}) is None
    assert C.novelty_thresholds({"params": {"rhythm": {}}}) is None
    assert C.novelty_thresholds({"params": {"sections": {"novelty": 0.15}}}) == [0.15]
    assert C.novelty_thresholds({"params": {"sections": {"novelty": [0.18, 0.12, 0.15]}}}) == [0.12, 0.15, 0.18]


def _nov():
    n = np.zeros(400)
    for at, h in ((60, 0.30), (140, 0.14), (220, 0.16), (300, 0.25)):
        n[at] = h
    return n


def test_section_bounds_cut_and_precomputed_novelty():
    nov = _nov()
    dur = 200.0                                   # 2 frames per second
    cnt = lambda t: len(C.section_bounds(None, dur, thr=t, nov=nov))  # noqa: E731
    assert cnt(0.15) == 4                          # 0.30, 0.16, 0.25 pass: 3 cuts, 4 sections
    assert cnt(0.13) == 5 and cnt(0.20) == 3
    assert cnt(None) == cnt(C.NOVELTY)             # the default cut is NOVELTY


def test_section_frames_are_their_own_length_not_half_a_second():
    # chirper-one, 28 Nov: a frame is int(FPS / 2) onset frames (0.4907 s at FPS 46.875); reading frame p as second
    # p / 2 put every section's audio 1.9% late.
    assert C.FRAME_S == C.FRAME_HOP / C.L.FPS and abs(C.FRAME_S - 0.5) > 0.005
    nov = _nov()
    cuts = [a for a, _ in C.section_bounds(None, 200.0, thr=0.15, nov=nov)][1:]
    assert cuts == [C.frame_s(p) for p in (60, 220, 300)]
    assert all(C.frame_at(C.frame_s(p)) == p for p in range(0, 2000))


def test_ensemble_averages_form_terms_and_reports_cuts():
    sets = [[1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
    ctx = {"section_sets": sets, "novelty_thresholds": [0.14, 0.15, 0.16], "sections": sets[1]}

    def fn(c):
        return 10.0 * len(c["sections"]), {"sections": len(c["sections"])}
    s, d = C.ensemble(fn, ctx)
    assert s == 40.0 and d["sections"] == 4
    assert d["ensemble"] == {"novelty": [0.14, 0.15, 0.16], "sections": [3, 4, 5], "scores": [30.0, 40.0, 50.0]}
    s, d = C.ensemble(lambda c: (None, {"n": len(c["sections"])}), ctx)
    assert s is None and d == {"n": 4}             # a term that does not apply stays the middle cut's


def test_score_uses_the_ensemble_only_for_form_terms(monkeypatch):
    sets = [[1] * 3, [1] * 4, [1] * 5]
    monkeypatch.setattr(C, "BUILTIN", {"structure": lambda c: (10.0 * len(c["sections"]), {}),
                                       "length": lambda c: (10.0 * len(c["sections"]), {})})
    ctx = {"album": {"weights": {"structure": 1.0, "length": 1.0}}, "sections": sets[1], "section_sets": sets}
    r = C.score(ctx)
    assert r["terms"] == {"structure": 40.0, "length": 40.0}
    ctx = {**ctx, "section_sets": [sets[0], sets[2], sets[2]]}  # middle cut 5, mean (3+5+5)/3
    r = C.score({**ctx, "sections": sets[2]})
    assert r["terms"]["structure"] == round(10.0 * 13 / 3, 2) and r["terms"]["length"] == 50.0
    r = C.score({**ctx, "section_sets": None, "sections": sets[0]})   # default: no ensemble anywhere
    assert r["terms"] == {"structure": 30.0, "length": 30.0} and "ensemble" not in r["detail"]["structure"]


def _sec(a, b, level=-14.0, density=6.0, tilt=0.0):
    return {"a": a, "b": b, "level": level, "density": density, "profile": np.full(9, tilt)}


def test_a_short_section_that_carries_a_form_term_is_named():
    """Six long sections alike, and the last chord cut off as four seconds of its own with no attacks in it: variety's
    density cv is all that section. The note names its seconds and both readings; nothing else changes."""
    body = [_sec(i * 45.0, (i + 1) * 45.0, density=6.0 + 0.1 * (i % 2)) for i in range(6)]
    chord = _sec(270.0, 274.0, density=0.0)
    ctx = {"dur": 276.0, "sections": body + [chord], "section_sets": None}
    terms = {"structure": C.m_structure(ctx)[0], "variety": C.m_variety(ctx)[0]}
    note = C.short_section_note(ctx, terms)
    assert note.startswith("A SHORT SECTION CARRIES A FORM TERM: 270-274 s (under 3% of the render): ")
    without = C.m_variety({**ctx, "sections": body})[0]
    assert f"variety {terms['variety']:.1f} ({without:.1f} without)" in note and terms["variety"] - without > 20
    assert C.short_section_note({**ctx, "sections": body}, terms) == ""                    # no short section: nothing
    edges = [0.0, 20.0, 80.0, 110.0, 180.0, 220.0, 270.0]                                  # uneven, as a song's are
    even = [_sec(a, b, density=3.0 + 3.0 * (i % 2), level=-14.0 - 6.0 * (i % 2)) for i, (a, b) in enumerate(zip(edges, edges[1:]))]
    busy = {"dur": 276.0, "sections": even + [_sec(270.0, 274.0, density=4.0, level=-16.0)], "section_sets": None}
    got = {"structure": C.m_structure(busy)[0], "variety": C.m_variety(busy)[0]}
    assert C.short_section_note(busy, got) == ""                                           # short, but it carries nothing
    sets = [body, body + [chord], body + [chord]]                                           # the album's cuts: their mean
    ens = {"dur": 276.0, "sections": sets[1], "section_sets": sets, "novelty_thresholds": [0.1, 0.2, 0.3]}
    mean = float(np.mean([C.m_variety({**ens, "sections": s})[0] for s in sets]))
    assert f"variety {mean:.1f} ({without:.1f} without)" in C.short_section_note(ens, {"variety": mean})
    assert "structure" not in C.short_section_note(ens, {"variety": mean})                 # a term not scored is not read


def test_a_saved_file_is_whole_or_not_there(tmp_path, monkeypatch):
    """--save and the album's files are read by other runs while they are written: a temporary file, then a rename."""
    import json
    path = str(tmp_path / "features.json")
    C.write_json(path, {"a": [1.5, 2, None], "long": "x" * 4000})
    C.write_json(path, {"a": 1})                                   # a shorter file over a longer one: nothing left of it
    with open(path) as f:
        assert json.load(f) == {"a": 1}
    assert os.listdir(tmp_path) == ["features.json"]               # no temporary file stays

    def boom(*_a, **_k):
        raise RuntimeError("the disk is full")
    monkeypatch.setattr(C.os, "replace", boom)
    try:
        C.write_json(path, {"a": 2})
    except RuntimeError:
        pass
    with open(path) as f:
        assert json.load(f) == {"a": 1}                            # a write that fails leaves the old file as it was
    assert os.listdir(tmp_path) == ["features.json"]
    monkeypatch.undo()
    import threading                                               # eight writers at once: one of their files, whole
    docs = [{"n": i, "pad": "y" * (500 * (i + 1))} for i in range(8)]
    ts = [threading.Thread(target=lambda d=d: [C.write_json(path, d) for _ in range(40)]) for d in docs]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    with open(path) as f:
        assert json.load(f) in docs
