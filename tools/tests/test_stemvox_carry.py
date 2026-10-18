#!/usr/bin/env python3
"""Cross-bar vocal continuations: preserve performed time, phone gestures, and valid note origins."""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import stemvox as V


class CarryTests(unittest.TestCase):
    def test_note_crosses_bar_without_retriggering_phones(self):
        rows = [(1, '1', 0.0, 4, 120), (2, '2', 2.0, 4, 120)]
        bars = {'1': [[3, 2, 100, 'A4', '^on=3^off=4', 2.5]], '2': []}
        lines = V.carried_lines(rows, bars, .125)
        self.assertEqual(lines, ['bar   1  R/3b A4/1b@100^on=3^off=4', 'bar   2  _/1b R/3b'])
        self.assertEqual(' '.join(lines).count('^on='), 1)
        self.assertEqual(' '.join(lines).count('^off='), 1)

    def test_continuation_uses_next_bars_tempo(self):
        rows = [(1, '1', 0.0, 4, 120), (2, '2', 2.0, 4, 60)]
        bars = {'1': [[3, 3, 100, 'A4', '', 3.0]], '2': []}
        self.assertEqual(V.carried_lines(rows, bars, .125)[1], 'bar   2  _/1b R/3b')

    def test_repeat_wrap_uses_performed_not_measure_order(self):
        rows = [(3, '3.2', 2.0, 4, 120), (4, '4.1', 0.0, 4, 120)]
        bars = {'4.1': [[3, 2, 90, 'E4', '', 2.5]], '3.2': []}
        lines = V.carried_lines(rows, bars, .125)
        self.assertEqual(lines[0], 'bar 4.1  R/3b E4/1b@90')
        self.assertEqual(lines[1], 'bar 3.2  _/1b R/3b')

    def test_excluded_bar_gap_stops_continuation(self):
        rows = [(1, '1', 0.0, 4, 120), (3, '3', 4.0, 4, 120)]
        bars = {'1': [[3, 8, 100, 'A4', '', 5.5]], '3': []}
        self.assertEqual(V.carried_lines(rows, bars, .125)[1], 'bar   3  R/4b')

    def test_rejected_origin_does_not_create_an_orphan_hold(self):
        rows = [(1, '1', 0.0, 4, 120), (2, '2', 2.0, 4, 120)]
        bars = {'1': [[0, 3, 100, 'C4', '', 1.5], [2, 3, 90, 'D4', '', 2.5]], '2': []}
        lines = V.carried_lines(rows, bars, .125)
        self.assertEqual(lines[0], 'bar   1  C4/3b@100 R/1b')
        self.assertEqual(lines[1], 'bar   2  R/4b')

    def test_note_ending_at_barline_has_no_hold(self):
        rows = [(1, '1', 0.0, 4, 120), (2, '2', 2.0, 4, 120)]
        bars = {'1': [[3, 1, 100, 'A4', '', 2.0]], '2': []}
        self.assertEqual(V.carried_lines(rows, bars, .125)[1], 'bar   2  R/4b')

    def test_quantized_onset_past_barline_does_not_create_hold(self):
        rows = [(1, '1', 0.0, 4, 120), (2, '2', 2.0, 4, 120)]
        bars = {'1': [[4, 1, 100, 'A4', '', 2.5]], '2': []}
        self.assertEqual(V.carried_lines(rows, bars, .125), ['bar   1  R/4b', 'bar   2  R/4b'])

    def test_syllable_can_span_three_bars(self):
        rows = [(i + 1, str(i + 1), i * 2.0, 4, 120) for i in range(3)]
        bars = {'1': [[3, 8, 100, 'A4', '', 5.5]], '2': [], '3': []}
        self.assertEqual(V.carried_lines(rows, bars, .125),
                         ['bar   1  R/3b A4/1b@100', 'bar   2  _/4b', 'bar   3  _/3b R/1b'])

    def test_skipped_source_bar_remains_empty(self):
        rows = [(1, '1', 0.0, 4, 120), (2, '2', 0.0, 0, 120)]
        bars = {'1': [], '2': []}
        self.assertEqual(V.carried_lines(rows, bars, .125), ['bar   1  R/4b', 'bar   2  '])

    @unittest.skipUnless(os.environ.get('CHIRP'), 'set CHIRP for the native plan check')
    def test_native_hold_is_one_voice_with_final_coda(self):
        rows = [(1, '1', 0.0, 4, 120), (2, '2', 2.0, 4, 120)]
        bars = {'1': [[3, 2, 100, 'A4', '^on=3^off=4', 2.5]], '2': []}
        score = ' | '.join(line.split(None, 2)[2] for line in V.carried_lines(rows, bars, .125))
        song = {'tempo': 120, 'patches': {'p': {'synth': {'layers': ['sine']}}},
                'tracks': [{'name': 'probe', 'patch': 'p', 'score': score}]}
        with tempfile.TemporaryDirectory(prefix='stemvox-carry-test-') as tmp:
            path = pathlib.Path(tmp) / 'song.json'
            path.write_text(json.dumps(song))
            run = subprocess.run([os.environ['CHIRP'], 'plan', '-f', str(path), '--json'],
                                 capture_output=True, text=True, check=True)
        data = json.loads(run.stdout)['data']
        notes = [n for n in data['canonical']['tracks'][0]['notes'] if 'pitch' in n]
        self.assertEqual(data['voices'], 1)
        self.assertEqual(len(notes), 1)
        self.assertEqual((notes[0]['at'], notes[0]['len']), (3, 2))
        self.assertEqual(notes[0]['expr'], {'on': 3.0, 'off': 4.0})


if __name__ == '__main__':
    unittest.main()
