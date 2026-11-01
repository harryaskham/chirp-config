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
