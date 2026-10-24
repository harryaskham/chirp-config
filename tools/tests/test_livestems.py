#!/usr/bin/env python3
"""tools/livestems.py: output-name matching for audio-separator's stems and the argument rules (no separation run).

  python3 tools/tests/test_livestems.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import livestems as S  # noqa: E402


class LiveStems(unittest.TestCase):
    def test_pick_matches_audio_separator_names(self):
        files = ["/x/song_(Crowd)_UVR-MDX-NET_Crowd_HQ_1.wav", "/x/song_(No Crowd)_UVR-MDX-NET_Crowd_HQ_1.wav"]
        self.assertTrue(S.pick(files, "crowd").endswith("(Crowd)_UVR-MDX-NET_Crowd_HQ_1.wav"))
        self.assertTrue(S.pick(files, "no crowd").endswith("(No Crowd)_UVR-MDX-NET_Crowd_HQ_1.wav"))
        rof = ["/x/s_(crowd)_mel_band.wav", "/x/s_(other)_mel_band.wav"]
        self.assertTrue(S.pick(rof, "other").endswith("(other)_mel_band.wav"))
        self.assertIsNone(S.pick(rof, "no crowd"))
        sw = [f"/x/s_({n})_BS-Roformer-SW.wav" for n in S.STEMS6]
        self.assertEqual([os.path.basename(S.pick(sw, n)) for n in S.STEMS6], [os.path.basename(f) for f in sw])

    def test_arguments(self):
        with self.assertRaises(SystemExit):
            S.main([])                                  # neither ID nor --wav
        with self.assertRaises(SystemExit):
            S.main(["--wav", "/nonexistent.wav"])       # --wav needs --out
        with self.assertRaises(SystemExit):
            S.main(["no-such-climb-id"])                # no ref/ID.wav

    def test_env_caps_threads_and_drops_ld_library_path(self):
        os.environ["LD_LIBRARY_PATH"] = "/bad"
        e = S.env(3)
        self.assertNotIn("LD_LIBRARY_PATH", e)
        self.assertEqual((e["OMP_NUM_THREADS"], e["OPENBLAS_NUM_THREADS"]), ("3", "1"))


class Confine(unittest.TestCase):
    def test_every_step_is_cpu_bounded(self):
        S.CPUS[0], S.QUOTA[0] = "2-5", 300
        os.environ["XDG_RUNTIME_DIR"] = os.environ.get("XDG_RUNTIME_DIR") or "/run/user/1000"
        cmd = S.confine(["nice", "x"])
        if cmd[0] == "systemd-run":                       # a cgroup quota the runtime can't lift
            self.assertIn("CPUQuota=300%", cmd)
            self.assertEqual(cmd[-2:], ["nice", "x"])
        else:
            self.assertEqual(cmd[:3], ["taskset", "-c", "2-5"])
        S.CPUS[0], S.QUOTA[0] = "0-3", 400

if __name__ == "__main__":
    unittest.main()
