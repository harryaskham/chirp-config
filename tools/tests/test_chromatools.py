#!/usr/bin/env python3
"""chirper-two's obZen chroma tools, promoted 28 Oct (tools/chromadiag.py, bandsrc.py, drumshare.py, drumtune.py, ab.py,
scoreedit.py): chromadiag's section chroma equals likeness's chroma term, scoreedit's token round trip is a no-op and
a window edit touches exactly the notes in the window, and both editors find a track line in either key order.

  python3 tools/tests/test_chromatools.py      (from ~/.config/chirp; a few seconds)
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ab as AB  # noqa: E402
import chromadiag as CD  # noqa: E402
import likeness as L  # noqa: E402
import scoreedit as SE  # noqa: E402


def chord(freqs, sec=8.0):
    t = np.arange(int(sec * L.SR)) / L.SR
    x = sum(0.2 * np.sin(2 * np.pi * f * t) * (1 + 0.1 * np.sin(2 * np.pi * 0.5 * t)) for f in freqs)
    return np.stack([x, x], 1).astype(np.float32)


class Chromadiag(unittest.TestCase):
    def test_section_chroma_is_likeness_exact(self):
        ref, ours = chord([110, 138.6, 164.8, 220]), chord([110, 130.8, 164.8, 261.6])     # A major vs A minor-ish
        R, C = L.Feat(ref), L.Feat(ours)
        n = min(R.n, C.n)
        w2 = int(L.FPS / 2)
        cs = [L._cos(R.chroma[:, i:i + w2].mean(1) - 1 / 12, C.chroma[:, i:i + w2].mean(1) - 1 / 12) for i in range(0, n - w2, w2)]
        expected = 100 * max(0, float(np.mean(cs)))
        got = CD.score(CD.total(CD.raw_pc(CD.mono(ref))), CD.total(CD.raw_pc(CD.mono(ours))), n)[0]
        self.assertAlmostEqual(got, expected, delta=0.05)
        self.assertLess(got, 99.0)                                   # the chords differ, so not a trivial match

    def test_registers_tile_the_band(self):
        x = CD.mono(chord([150, 600, 2500], 2.0))
        parts = CD.raw_pc(x)
        whole = CD.raw_pc(x, [(100, 4000)])[(100, 4000)]
        self.assertTrue(np.allclose(CD.total(parts), whole, rtol=1e-6))


class Scoreedit(unittest.TestCase):
    def test_round_trip_and_window_edit(self):
        s = "R/0.5b | F1/0.5b@100 [F1/0.25b G1/0.25b]x2 | C2/1b"
        items = SE.tokens(s)
        self.assertEqual(SE.render(items), s)                        # no-op pass is identical
        pts = SE.tempo_points("tempo: 120\n")                         # a beat is 0.5 s
        count = [0]
        # 0.5-1.0 s = beats 1-2: both copies of the group's F1 (beats 1.0 and 1.5), not the F1 at beat 0.5 (0.25 s);
        # the group is expanded only because an edited token sits in it
        out = SE.edit(items, [0.0], pts, 0.5, 1.0, {"F1": "F2"}, count)
        self.assertEqual(count[0], 2)
        self.assertEqual(SE.render(out), "R/0.5b | F1/0.5b@100 F2/0.25b G1/0.25b F2/0.25b G1/0.25b | C2/1b")
        untouched = SE.edit(SE.tokens(s), [0.0], pts, 2.0, 3.0, {"F1": "F2"}, [0])
        self.assertEqual(SE.render(untouched), s)                    # nothing in the window: the group stays folded


class TrackLine(unittest.TestCase):
    def test_either_key_order(self):
        for mod in (AB, SE):
            self.assertTrue(mod.is_track_line('  - {name: "drums", patch: "metal-kit-dry", score: "k/1b"}', "drums"))
            self.assertTrue(mod.is_track_line('  - {patch: "metal-kit-dry", name: "drumsr", notes: []}', "drumsr"))
            self.assertFalse(mod.is_track_line('  - {name: "drumsr", patch: "x"}', "drums"))
            self.assertFalse(mod.is_track_line('tempo: 120', "drums"))


if __name__ == "__main__":
    unittest.main()
