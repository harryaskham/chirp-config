#!/usr/bin/env python3
"""tools/dispersion.py: when each band of a reverb's impulse response arrives (does the tail chirp, as a spring's does).

Hermetic: a comb (echoes that arrive together in every band) and a made spring: the same echoes through a chain of
stretched allpasses, whose delay at each frequency is known in closed form. The `fx` mode runs on a stand-in engine.

  python3 tools/tests/test_dispersion.py      (from ~/.config/chirp; a few seconds; needs scipy for the made spring)
"""
import contextlib
import io
import os
import shutil
import stat
import sys
import tempfile
import unittest
import wave

import numpy as np
from scipy.signal import lfilter

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import dispersion as D  # noqa: E402

SR = 48000
A, K, M = 0.62, 5, 100                    # allpass coefficient, stretch (transition at SR / 2K = 4.8 kHz), sections a trip


def chirped(x, trips=1):
    """x through `trips` runs of the spring: M stretched allpasses (a + z^-K) / (1 + a z^-K) a run."""
    b = np.zeros(K + 1)
    b[0], b[K] = A, 1.0
    a = np.zeros(K + 1)
    a[0], a[K] = 1.0, A
    for _ in range(M * trips):
        x = lfilter(b, a, x)
    return x


def delay_ms(hz, trips=1):
    """The chain's group delay at a frequency, ms."""
    w = 2 * np.pi * hz / SR * K
    return trips * M * K * (1 - A * A) / (1 + 2 * A * np.cos(w) + A * A) / SR * 1000


def comb(echoes=((40, 1.0), (80, 0.6), (120, 0.36)), seconds=1.0):
    h = np.zeros(int(seconds * SR))
    for ms, g in echoes:
        h[int(ms / 1000 * SR)] = g
    return h


def save(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 30000).astype("<i2").tobytes())


ENGINE = r'''#!/usr/bin/env python3
import sys, wave
a = sys.argv[1:]
if "refuse" in open(a[a.index("-f") + 1]).read():
    sys.stderr.write("chirp: unknown effect\n")
    sys.exit(2)
src = dict(x.split("=", 1) for x in a if x.startswith("click="))["click"]
with wave.open(src) as w:
    sr, n = w.getframerate(), w.getnframes()
    data = w.readframes(n)
shift = int(0.020 * sr) * 2
with wave.open(a[a.index("-o") + 1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b"\0" * shift + data[:len(data) - shift])
'''


class Dispersion(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="dispersion-test-")
        self.addCleanup(shutil.rmtree, self.root, True)

    def run_tool(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = D.main(list(argv))
        return code, out.getvalue()

    @staticmethod
    def row(text, name, label):
        line = next(ln for ln in text.splitlines() if ln.startswith(name) and label in ln)
        return [float(line[45 + 7 * i:52 + 7 * i]) for i in range(len(D.FCS))], line[45 + 7 * len(D.FCS):]

    def test_echoes_that_arrive_together_have_no_trend(self):
        env = D.envelopes(comb(), SR)
        first = D.first_arrivals(env, SR, 0)
        for v in first:
            self.assertAlmostEqual(v, 40.0, delta=0.5)
        for v in D.late(first):
            self.assertAlmostEqual(v, 0.0, delta=0.1)
        self.assertEqual(list(D.echo_lags(env, SR, 0)), [0.0] * len(D.FCS))

    def test_a_springs_first_echo_is_a_chirp_the_highs_after_the_lows(self):
        h = chirped(comb(echoes=((30, 1.0),)))                             # one run of the spring, heard 30 ms on
        first = D.first_arrivals(D.envelopes(h, SR), SR, 0)
        for hz, tol in ((500, 1.5), (1000, 1.5), (2000, 2.0), (2828, 4.0)):
            self.assertAlmostEqual(first[D.FCS.index(hz)], 30.0 + delay_ms(hz), delta=tol)
        l28, l40, low = D.late(first)
        self.assertAlmostEqual(l28, 3.1, delta=0.8)                        # +3.7 by the formula
        self.assertGreater(l40, 5.0)                                       # +18 by the formula: the band reads its early edge
        self.assertGreater(l40, l28)
        self.assertLess(low, 2.0)                                          # up to 2 kHz the bands are close together

    def test_the_echo_train_of_a_spring_lags_more_the_higher_the_band(self):
        """Three echoes, each one more run of the spring: the 2 kHz band's train sits behind the 500 Hz band's."""
        h = sum(g * chirped(comb(echoes=((40.0 * n, 1.0),)), trips=n) for n, g in ((1, 1.0), (2, 0.7), (3, 0.5)))
        lags = D.echo_lags(D.envelopes(h, SR), SR, 0)
        self.assertEqual(lags[D.FCS.index(500)], 0.0)
        self.assertGreaterEqual(lags[D.FCS.index(2000)], 1.0)
        self.assertGreater(lags[D.FCS.index(2828)], lags[D.FCS.index(1000)])
        self.assertGreater(D.late(lags)[0], 1.0)

    def test_impulse_responses_on_file_and_where_the_impulse_is(self):
        save(os.path.join(self.root, "comb.wav"), np.concatenate([np.zeros(SR // 2), comb()]))
        code, text = self.run_tool("ir", "comb=" + os.path.join(self.root, "comb.wav") + ":0.5")
        self.assertEqual(code, 0)
        self.assertTrue(text.splitlines()[0].startswith("%-30s %-14s" % ("ms, by band (Hz)", "") + "    250    354"))
        values, rest = self.row(text, "comb", "first arrival")
        for v in values:
            self.assertAlmostEqual(v, 40.0, delta=0.5)
        self.assertRegex(rest, r"^ +2\.8k [+-]0\.0, 4k [+-]0\.0; 500-2k within 0\.0$")
        self.assertEqual(self.row(text, "comb", "echo lag")[0], [0.0] * len(D.FCS))

    def test_fx_renders_an_impulse_through_the_effect_on_the_pin(self):
        engine = os.path.join(self.root, "fake-chirp")
        with open(engine, "w") as f:
            f.write(ENGINE)
        os.chmod(engine, os.stat(engine).st_mode | stat.S_IXUSR)
        code, text = self.run_tool("fx", "delay time=20ms mix=1", "--pin", engine)
        self.assertEqual(code, 0)
        for v in self.row(text, "delay time=20ms mix=1", "first arrival")[0]:
            self.assertAlmostEqual(v, 20.0, delta=0.5)                     # after the impulse, not after the file's start
        with self.assertRaises(SystemExit) as e:
            self.run_tool("fx", "refuse", "--pin", engine)
        self.assertIn("would not render 'refuse': chirp: unknown effect", str(e.exception))

    def test_no_arguments_is_the_help(self):
        code, text = self.run_tool()
        self.assertEqual(code, 2)
        self.assertIn('dispersion.py fx "reverb kind=spring', text)


if __name__ == "__main__":
    unittest.main()
