#!/usr/bin/env python3
"""Absolute edge diagnostics are opt-in and never change the edge metric."""
import contextlib
import copy
import io
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import albumedges as A


class AbsoluteEdgeTests(unittest.TestCase):
    def setUp(self):
        self.ref = {side: dict.fromkeys(A.NAMES, -40.0) for side in ('head', 'tail')}
        self.ours = copy.deepcopy(self.ref)
        self.ours['tail']['120-400'] = -73.0
        self.ref['tail']['120-400'] = -92.0
        self.ours['head']['8k+'] = -45.0
        self.ref['head']['8k+'] = -57.0

    def check(self, absolute=False):
        out = io.StringIO()
        args = ['test', '/example.wav'] + (['--absolute'] if absolute else [])
        with mock.patch.object(A, 'render_edges', return_value=(self.ours, self.ref, 10.0)), \
                mock.patch.object(A, 'neighbours', return_value=(None, None, None)), contextlib.redirect_stdout(out):
            A.cmd_check(args)
        return out.getvalue()

    def test_default_output_stays_compact(self):
        text = self.check()
        self.assertEqual(len(text.splitlines()), 3)
        self.assertNotIn('RMS dBFS', text)
        self.assertNotIn('quiet-band', text)

    def test_absolute_shows_ours_and_reference(self):
        text = self.check(True)
        self.assertEqual(text.count('ours RMS dBFS'), 2)
        self.assertEqual(text.count('record RMS dBFS'), 2)
        self.assertIn('-73.0', text)
        self.assertIn('-92.0', text)
        self.assertIn('tail quiet-band deltas', text)
        self.assertIn('120-400', text.split('tail quiet-band deltas')[1])
        self.assertNotIn('head quiet-band deltas', text)

    def test_deltas_and_metric_are_unchanged(self):
        before = A.err(A.vec(self.ours['tail']), A.vec(self.ref['tail']))
        plain = self.check().splitlines()
        absolute = self.check(True).splitlines()
        for line in plain:
            self.assertIn(line, absolute)
        self.assertEqual(before, A.err(A.vec(self.ours['tail']), A.vec(self.ref['tail'])))
        self.assertAlmostEqual(before[0], 19 / len(A.NAMES))

    def test_one_loud_side_is_not_flagged_as_quiet(self):
        self.ours['tail']['120-400'] = -60.0
        self.assertNotIn('quiet-band deltas', self.check(True))

    def test_threshold_only_affects_diagnostics(self):
        self.ours['tail']['120-400'] = -92.1
        self.assertNotIn('quiet-band deltas', self.check(True))
        self.ours['tail']['120-400'] = -70.0
        self.assertNotIn('quiet-band deltas', self.check(True))


class DroppedNeighbour(unittest.TestCase):
    def test_a_dropped_duplicate_is_no_neighbour(self):
        reg = {"climbs": [
            {"id": "electric-red", "status": "active", "meta": {"album": "obZen", "track": 2}},
            {"id": "bleed", "status": "active", "meta": {"album": "obZen", "track": 3}},
            {"id": "obzen-bleed", "status": "dropped", "meta": {"album": "obZen", "track": 3}},
            {"id": "lethargica", "status": "requested", "meta": {"album": "obZen", "track": 4}},
        ]}
        with mock.patch.object(A, 'registry', return_value=reg):
            me, prev, nxt = A.neighbours('bleed')
        self.assertEqual((prev['id'], nxt['id']), ('electric-red', 'lethargica'))


if __name__ == '__main__':
    unittest.main()
