#!/usr/bin/env python3
"""masterstack: --slots caps concurrent renders and --max-load waits for the load average (chirper-zero's request);
the default still renders every seed at once. A fake chirp logs start/end times (no audio is made).

  python3 tools/tests/test_masterstack.py      (from ~/.config/chirp; a few seconds)
"""
import os
import stat
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import masterstack as M  # noqa: E402

FAKE = """#!/bin/sh
out=""
while [ $# -gt 0 ]; do [ "$1" = "-o" ] && out="$2"; shift; done
echo "start $(date +%s.%N)" >> "$LOG"
sleep 0.4
: > "$out"
echo "end $(date +%s.%N)" >> "$LOG"
"""


class Slots(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="masterstack-test-")
        self.chirp = os.path.join(self.dir, "chirp")
        with open(self.chirp, "w") as f:
            f.write(FAKE)
        os.chmod(self.chirp, os.stat(self.chirp).st_mode | stat.S_IEXEC)
        self.sections = os.path.join(self.dir, "sections.txt")
        with open(self.sections, "w") as f:
            f.write("0,10\n")
        self.song = os.path.join(self.dir, "song.yaml")
        with open(self.song, "w") as f:
            f.write("tempo: 120\n")
        self.log = os.path.join(self.dir, "log")
        os.environ["LOG"] = self.log

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dir, ignore_errors=True)

    def overlap(self):
        """The most renders that were running at once."""
        ev = sorted((float(t), 1 if k == "start" else -1) for k, t in (l.split() for l in open(self.log)))
        run = peak = 0
        for _, d in ev:
            run += d
            peak = max(peak, run)
        return peak

    def stack(self, **kw):
        return M.Stack(self.song, "ref.wav", self.sections, self.dir, [0, 11, 7], self.chirp, **kw)

    def test_default_renders_every_seed_at_once(self):
        wavs = self.stack().render(self.song, [0, 11, 7])
        self.assertTrue(all(os.path.exists(w) for w in wavs.values()))
        self.assertEqual(self.overlap(), 3)

    def test_one_slot_renders_one_at_a_time(self):
        wavs = self.stack(slots=1).render(self.song, [0, 11, 7])
        self.assertEqual(sorted(wavs), [0, 7, 11])
        self.assertTrue(all(os.path.exists(w) for w in wavs.values()))
        self.assertEqual(self.overlap(), 1)

    def test_max_load_waits_before_starting(self):
        loads = iter([(50.0, 0, 0), (50.0, 0, 0), (2.0, 0, 0)] + [(2.0, 0, 0)] * 10)
        with mock.patch.object(M.os, "getloadavg", lambda: next(loads)), \
                mock.patch.object(M.time, "sleep") as slept:
            self.stack(slots=1, max_load=10).render(self.song, [0, 11])
        self.assertEqual(slept.call_count, 2, "waited twice while the load was 50")
        self.assertEqual(self.overlap(), 1)

    def test_heldout_passes_the_slot_cap_to_seedscore(self):
        seen = {}

        def fake_run(cmd, **kw):
            seen.update(kw.get("env", {}))
            return mock.Mock(stdout='{"mean": 1, "per_seed": [1]}', stderr="", returncode=0)

        with mock.patch.object(M, "run", fake_run):
            M.heldout(self.chirp, self.song, "ref.wav", self.sections, "7,13", 1)
        self.assertEqual(seen.get("SEEDSCORE_JOBS"), "1")
        seen.clear()
        with mock.patch.object(M, "run", fake_run):
            M.heldout(self.chirp, self.song, "ref.wav", self.sections, "7,13")
        self.assertNotIn("SEEDSCORE_JOBS", seen)


if __name__ == "__main__":
    unittest.main()
