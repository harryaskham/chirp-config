#!/usr/bin/env python3
"""Vocal diagnostics: serial/settings plumbing, temporary-audio lifetime, and external-input safety."""
import contextlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import vocaltest as V

SHARES = {s: (100.0 if s == 'vocals' else 0.0) for s in V.STEMS}


class LifetimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='vocaltest-unit-')
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.work = self.root / 'work'

    def render(self, cmd, **kwargs):
        path = pathlib.Path(cmd[cmd.index('-o') + 1])
        path.write_bytes(b'rendered-audio-placeholder')
        return subprocess.CompletedProcess(cmd, 0, '', '')

    def run_tool(self, args, failure=None, render=None):
        out = io.StringIO()
        with mock.patch.object(V.tempfile, 'mkdtemp', return_value=str(self.work)) as temp, \
                mock.patch.object(V.subprocess, 'run', side_effect=render or self.render) as renderer, \
                mock.patch.object(V, 'shares', side_effect=failure, return_value=SHARES) as shares, \
                contextlib.redirect_stdout(out):
            V.main(args)
        return out.getvalue(), temp, renderer, shares

    def test_default_cleans_render_and_uses_one_job(self):
        text, _, render, shares = self.run_tool(['song.yaml', 'vox', '--json'])
        self.assertEqual(json.loads(text), SHARES)
        self.assertFalse(self.work.exists())
        self.assertEqual(shares.call_args.kwargs, {'jobs': 1, 'shifts': None})
        self.assertIn('song.yaml', render.call_args.args[0])
        self.assertNotIn('--seed', render.call_args.args[0])

    def test_settings_values_are_not_positionals(self):
        _, _, render, shares = self.run_tool(['--jobs', '2', '--shifts', '0', '--seed', '11', 'song.yaml', 'vox', '--json'])
        cmd = render.call_args.args[0]
        self.assertEqual(cmd[cmd.index('-f') + 1], 'song.yaml')
        self.assertEqual(cmd[cmd.index('--solo') + 1], 'vox')
        self.assertEqual(cmd[cmd.index('--seed') + 1], '11')
        self.assertEqual(shares.call_args.kwargs, {'jobs': 2, 'shifts': 0})
        self.assertFalse(self.work.exists())

    def test_classifier_failure_still_cleans(self):
        with self.assertRaisesRegex(SystemExit, 'classifier failed'):
            self.run_tool(['song.yaml', 'vox'], failure=SystemExit('classifier failed'))
        self.assertFalse(self.work.exists())

    def test_render_failure_still_cleans(self):
        def failed(cmd, **kwargs):
            self.render(cmd, **kwargs)
            return subprocess.CompletedProcess(cmd, 1, '', 'render failure')
        with self.assertRaisesRegex(SystemExit, 'render failed'):
            self.run_tool(['song.yaml', 'vox'], render=failed)
        self.assertFalse(self.work.exists())

    def test_explicit_keep_retains_audio(self):
        keep = self.root / 'evidence'
        self.run_tool(['song.yaml', 'vox', '--keep', str(keep), '--json'])
        self.assertTrue(keep.exists())
        self.assertEqual(len(list(keep.glob('vox-*.wav'))), 1)

    def test_external_wav_is_not_deleted(self):
        original = self.root / 'source.wav'
        original.write_bytes(b'original')
        _, _, render, _ = self.run_tool(['--wav', str(original), '--json'])
        render.assert_not_called()
        self.assertEqual(original.read_bytes(), b'original')
        self.assertFalse(self.work.exists())

    def test_invalid_settings_create_no_work_directory(self):
        for args in (['--jobs', '0'], ['--shifts', '-1'], ['--jobs', 'no'], ['--jobs'],
                     ['--seed', '-1'], ['--seed', str(2**64)]):
            with self.subTest(args=args), mock.patch.object(V.tempfile, 'mkdtemp') as temp:
                with self.assertRaises(SystemExit):
                    V.main(['song.yaml', 'vox', *args])
                temp.assert_not_called()


class SeparationSettingsTests(unittest.TestCase):
    def test_explicit_jobs_and_shift_override_template_without_mutating_it(self):
        template = ['demucs', '-j', '2', '--shifts', '1']
        with mock.patch.object(V, 'DEMUCS', template), \
                mock.patch.object(V.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run, \
                mock.patch.object(V.L, 'load', return_value=np.ones((10, 2))):
            result = V.shares('voice.wav', '/tmp/not-created-vocaltest-test', jobs=1, shifts=0)
        cmd = run.call_args.args[0]
        self.assertEqual(cmd[cmd.index('-j') + 1], '1')
        self.assertEqual(cmd[cmd.index('--shifts') + 1], '0')
        self.assertEqual(template, ['demucs', '-j', '2', '--shifts', '1'])
        self.assertEqual(set(result), set(V.STEMS))
        self.assertTrue(all(v == 16.7 for v in result.values()))

    def test_default_keeps_model_default_shift_behavior(self):
        with mock.patch.object(V, 'DEMUCS', ['demucs', '-j', '2']), \
                mock.patch.object(V.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run, \
                mock.patch.object(V.L, 'load', return_value=np.ones((10, 2))):
            V.shares('voice.wav', '/tmp/not-created-vocaltest-test')
        cmd = run.call_args.args[0]
        self.assertNotIn('--shifts', cmd)
        self.assertEqual(cmd[cmd.index('-j') + 1], '1')

    def test_separation_cannot_overwrite_an_input_stem(self):
        with tempfile.TemporaryDirectory(prefix='vocaltest-collision-') as tmp:
            path = pathlib.Path(tmp) / 'htdemucs_6s' / 'vocals' / 'vocals.wav'
            path.parent.mkdir(parents=True)
            path.write_bytes(b'original')
            with mock.patch.object(V.subprocess, 'run') as run, self.assertRaisesRegex(SystemExit, 'overwrite'):
                V.shares(str(path), tmp)
            run.assert_not_called()
            self.assertEqual(path.read_bytes(), b'original')


if __name__ == '__main__':
    unittest.main()
