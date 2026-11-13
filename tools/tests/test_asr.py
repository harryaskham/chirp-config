#!/usr/bin/env python3
"""tools/asr.py: every Whisper call is confined (taskset, nice, thread caps, no fallback), windows tile the range and
their times land on the audio's timeline, finished windows are reused. A fake `whisper` records its argv/env.

  python3 tools/tests/test_asr.py      (from ~/.config/chirp; a few seconds)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAKE = r'''#!/usr/bin/env python3
import json, os, sys
a = sys.argv[1:]
log = os.environ["ASR_TEST_LOG"]
with open(log, "a") as f:
    f.write(json.dumps({"argv": a, "omp": os.environ.get("OMP_NUM_THREADS"),
                        "openblas": os.environ.get("OPENBLAS_NUM_THREADS")}) + "\n")
wav = a[0]
import wave, struct
with wave.open(wav, "rb") as w:
    raw = w.readframes(w.getnframes())
peak = max((abs(v[0]) for v in struct.iter_unpack("<h", raw)), default=0)
with open(log, "a") as f:
    f.write(json.dumps({"peak": peak, "affinity": sorted(os.sched_getaffinity(0))}) + "\n")
out = a[a.index("--output_dir") + 1]
words = "--word_timestamps" in a
seg = {"start": 1.0, "end": 2.5, "text": " hello world"}
if words:
    seg["words"] = [{"word": " hello", "start": 1.0, "end": 1.6}, {"word": " world", "start": 1.7, "end": 2.5}]
with open(os.path.join(out, os.path.splitext(os.path.basename(wav))[0] + ".json"), "w") as f:
    json.dump({"text": " hello world", "segments": [seg]}, f)
'''


class Asr(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="asr-test-")
        self.addCleanup(shutil.rmtree, self.d, True)
        bin_ = os.path.join(self.d, "bin")
        os.makedirs(bin_)
        with open(os.path.join(bin_, "whisper"), "w") as f:
            f.write(FAKE)
        os.chmod(os.path.join(bin_, "whisper"), 0o755)
        self.log = os.path.join(self.d, "calls.jsonl")
        self.env = {**os.environ, "PATH": f"{bin_}:{os.environ['PATH']}", "ASR_TEST_LOG": self.log}
        self.audio = os.path.join(self.d, "a.wav")
        with wave.open(self.audio, "wb") as f:                       # 70 s of silence
            f.setnchannels(1), f.setsampwidth(2), f.setframerate(16000)
            f.writeframes(b"\0\0" * 16000 * 70)

    def run_asr(self, *args):
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "asr.py"), self.audio, *args], capture_output=True,
                           text=True, env=self.env, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def calls(self, key="argv"):
        with open(self.log) as f:
            return [x for x in (json.loads(ln) for ln in f) if key in x]

    def test_windows_tile_the_range_and_shift_times(self):
        out = self.run_asr("--from", "10", "--to", "70", "--window", "25")
        self.assertEqual([s["start"] for s in out["segments"]], [11.0, 36.0, 61.0])   # windows at 10, 35, 60
        self.assertEqual(out["text"], "hello world hello world hello world")
        self.assertEqual(len(self.calls()), 3)

    def test_every_call_is_confined(self):
        self.run_asr("--to", "20")
        c = self.calls()[0]
        a = c["argv"]
        for flag, val in (("--threads", "4"), ("--condition_on_previous_text", "False"),
                          ("--temperature_increment_on_fallback", "None")):
            self.assertEqual(a[a.index(flag) + 1], val)
        self.assertNotIn("--word_timestamps", a)
        self.assertEqual((c["omp"], c["openblas"]), ("4", "1"))

    def test_taskset_and_nice_wrap_whisper(self):
        sys.path.insert(0, TOOLS)
        import asr
        cmd = asr.whisper_cmd("x.wav", "/tmp", "base.en", True, "2-5")
        self.assertEqual(cmd[:6], ["taskset", "-c", "2-5", "nice", "-n", "15"])
        self.assertIn("--word_timestamps", cmd)

    def test_the_default_cores_are_the_last_four_not_the_grooves(self):
        sys.path.insert(0, TOOLS)
        import asr
        real = os.cpu_count
        self.addCleanup(lambda: setattr(os, "cpu_count", real))
        for n, want in ((24, "20-23"), (8, "4-7"), (4, "0-3"), (2, "0-1")):
            os.cpu_count = lambda n=n: n
            self.assertEqual(asr.default_cores(), want)
        os.cpu_count = real
        n = os.cpu_count()
        self.run_asr("--to", "20")
        self.assertEqual(self.calls("affinity")[0]["affinity"], list(range(max(0, n - 4), n)))   # whisper really ran there
        self.run_asr("--to", "20", "--cores", "0")
        self.assertEqual(self.calls("affinity")[1]["affinity"], [0])
        self.env["ASR_CORES"] = "1"
        self.run_asr("--to", "20")
        self.assertEqual(self.calls("affinity")[2]["affinity"], [1])

    def test_norm_brings_a_quiet_voice_up_and_is_off_by_default(self):
        import math
        import struct
        with wave.open(self.audio, "wb") as f:                       # a quiet tone: peak 300 of 32768
            f.setnchannels(1), f.setsampwidth(2), f.setframerate(16000)
            f.writeframes(b"".join(struct.pack("<h", int(300 * math.sin(2 * math.pi * 220 * i / 16000))) for i in range(16000 * 20)))
        work = os.path.join(self.d, "work")
        self.run_asr("--to", "20", "--work", work)
        self.run_asr("--to", "20", "--norm", "--work", work)         # not the plain run's cached window
        plain, norm = [c["peak"] for c in self.calls("peak")]
        self.assertLess(plain, 320)
        self.assertGreater(norm, 10 * plain)
        self.assertLess(norm, 32767)                                 # brought up, not clipped

    def test_words_are_shifted_too(self):
        out = self.run_asr("--from", "30", "--to", "40", "--words")
        self.assertEqual([w["start"] for w in out["segments"][0]["words"]], [31.0, 31.7])

    def test_finished_windows_are_reused(self):
        work = os.path.join(self.d, "work")
        self.run_asr("--to", "40", "--window", "20", "--work", work)
        self.run_asr("--to", "40", "--window", "20", "--work", work)
        self.assertEqual(len(self.calls()), 2, "the second run reused both windows")


if __name__ == "__main__":
    unittest.main()
