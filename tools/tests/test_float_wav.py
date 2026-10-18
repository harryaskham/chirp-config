#!/usr/bin/env python3
"""IEEE float-WAV support, preserving the pre-existing integer PCM decode exactly."""
import pathlib
import sys
import tempfile
import unittest
import wave

import numpy as np
from scipy import signal
from scipy.io import wavfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import likeness as L


def legacy_load(path):
    with wave.open(path, 'rb') as stream:
        rate, channels, width, frames = stream.getframerate(), stream.getnchannels(), stream.getsampwidth(), stream.getnframes()
        data = stream.readframes(frames)
    samples = np.frombuffer(data, dtype='<i2' if width == 2 else '<i4').astype(np.float32) / (32768 if width == 2 else 2147483648)
    samples = samples.reshape(-1, channels)
    stereo = samples if channels == 2 else np.repeat(samples, 2, axis=1)
    if rate != L.SR:
        divisor = np.gcd(rate, L.SR)
        stereo = signal.resample_poly(stereo, L.SR // divisor, rate // divisor, axis=0).astype(np.float32)
    return stereo


class FloatWav(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='float-wav-test-')
        self.addCleanup(self.temporary.cleanup)
        self.path = str(pathlib.Path(self.temporary.name) / 'test.wav')

    def test_integer_pcm_is_bit_identical(self):
        rng = np.random.default_rng(7)
        for rate in (24000, 44100, 48000):
            for channels in (1, 2):
                for width in (2, 4):
                    with self.subTest(rate=rate, channels=channels, width=width):
                        data = rng.integers(-(2 ** (width * 8 - 2)), 2 ** (width * 8 - 2), size=(480, channels)).astype('<i2' if width == 2 else '<i4')
                        with wave.open(self.path, 'wb') as stream:
                            stream.setnchannels(channels)
                            stream.setsampwidth(width)
                            stream.setframerate(rate)
                            stream.writeframes(data.tobytes())
                        self.assertTrue(np.array_equal(L.load(self.path), legacy_load(self.path)))

    def test_float32_preserves_absolute_unclipped_amplitude(self):
        data = np.tile(np.array([-1.25, -.25, 0, .5, 1.5], dtype=np.float32), 100)
        for channels in (1, 2):
            source = data if channels == 1 else np.stack([data, data * -.5], axis=1)
            wavfile.write(self.path, 48000, source)
            expected = np.repeat(data[:, None], 2, axis=1) if channels == 1 else source
            decoded = L.load(self.path)
            self.assertEqual(decoded.dtype, np.float32)
            self.assertTrue(np.array_equal(decoded, expected))
            self.assertGreater(float(abs(decoded).max()), 1)

    def test_float64_resampling_matches_float32_contract(self):
        data = np.linspace(-1.2, 1.4, 1000, dtype=np.float64)
        wavfile.write(self.path, 44100, data)
        expected = signal.resample_poly(np.repeat(data.astype(np.float32)[:, None], 2, axis=1), 160, 147, axis=0).astype(np.float32)
        self.assertTrue(np.array_equal(L.load(self.path), expected))

    def test_invalid_float_data_is_rejected(self):
        for data in (np.array([0, np.nan], dtype=np.float32), np.array([0, np.inf], dtype=np.float32),
                     np.array([0, 1e300], dtype=np.float64), np.zeros((10, 3), dtype=np.float32)):
            wavfile.write(self.path, 48000, data)
            with self.assertRaisesRegex(ValueError, 'finite mono or stereo'):
                L.load(self.path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
