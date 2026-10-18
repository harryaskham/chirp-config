#!/usr/bin/env python3
"""drumtrans exports every family it can classify (bd-dfa7eb): the 909/electro kits' clap `cp` has a family
("claps"), so a cp-only or cp+snare stem keeps its claps instead of dropping them at export; a supplied piece in no
family is reported on stderr (it still absorbs energy in the decomposition) rather than silently lost; and a kit
without cp transcribes exactly as before.

  python3 tools/tests/test_drumtrans.py          (from ~/.config/chirp; a few seconds; DRUMTRANS_OLD=previous
                                                  drumtrans.py also compares a kick/snare run with it)
"""
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
import unittest
import wave
from contextlib import redirect_stderr

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = load(os.path.join(TOOLS, "drumtrans.py"), "drumtrans_test")
rng = np.random.default_rng(3)


def bandnoise(n, lo, hi):
    spec = np.fft.rfft(rng.normal(0, 1, n))
    f = np.fft.rfftfreq(n, 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(spec, n)
    return x / (np.abs(x).max() + 1e-12)


def piece(name):
    t = np.arange(int(0.25 * SR)) / SR
    if name == "k":
        return np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.12)
    if name == "s":
        return (0.7 * bandnoise(len(t), 1500, 9000) + 0.5 * np.sin(2 * np.pi * 200 * t)) * np.exp(-t / 0.09)
    if name == "zz":   # a piece in no family (a stand-in for anything outside FAMILIES)
        return bandnoise(len(t), 9000, 15000) * np.exp(-t / 0.05)
    out = np.zeros(len(t))   # cp: three quick bursts of mid noise
    for k in range(3):
        i = int(k * 0.011 * SR)
        seg = bandnoise(len(t) - i, 700, 2500) * np.exp(-t[:len(t) - i] / (0.012 if k < 2 else 0.07))
        out[i:] += seg
    return out / np.abs(out).max()


def write(path, x):
    y = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.repeat(y[:, None], 2, axis=1).tobytes())


def place(total, hits):
    x = np.zeros(int(total * SR))
    for t, name, v in hits:
        p = piece(name) * (v / 127) * 0.5
        i = int(t * SR)
        x[i:i + len(p)] += p[:len(x) - i]
    return x


def counts(res):
    return {fam: v["hits"] for fam, v in res.items()}


class Claps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix="drumtrans-")
        cls.song = os.path.join(cls.dir, "song.yaml")
        with open(cls.song, "w") as f:
            f.write("tempo: 120\ntracks: []\n")
        cls.tpl = {}
        for pieces in (["k", "s", "cp"], ["k", "s"], ["k", "s", "zz"]):
            path = os.path.join(cls.dir, "tpl-" + "".join(pieces) + ".wav")
            write(path, place(6.0 * len(pieces) + 2, [((3 * i + j) * 2.0, p, v) for i, p in enumerate(pieces)
                                                         for j, v in enumerate((40, 80, 120))]))
            cls.tpl[tuple(pieces)] = path
        # 16 bars at 120 bpm: kick on 1 and 3, snare on 2 and 4, a clap on every "and" of 4 (8 alone) and with
        # every snare on 4 in the second half (8 together)
        hits = []
        for bar in range(16):
            b0 = bar * 2.0
            hits += [(b0, "k", 110), (b0 + 1.0, "k", 110), (b0 + 0.5, "s", 110), (b0 + 1.5, "s", 110)]
            if bar < 8:
                hits.append((b0 + 1.75, "cp", 110))
            else:
                hits.append((b0 + 1.5, "cp", 110))
        cls.stem = os.path.join(cls.dir, "stem.wav")
        write(cls.stem, place(34.0, hits))
        cls.ks = os.path.join(cls.dir, "ks.wav")
        write(cls.ks, place(34.0, [h for h in hits if h[1] != "cp"]))
        cls.kx = os.path.join(cls.dir, "kx.wav")
        write(cls.kx, place(34.0, [h if h[1] != "cp" else (h[0], "zz", h[2]) for h in hits]))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, True)

    def run_(self, mod, stem, pieces):
        err = io.StringIO()
        with redirect_stderr(err):
            res, _ = mod.transcribe(stem, self.song, self.tpl[tuple(pieces)], pieces)
        return res, err.getvalue()

    def test_claps_are_exported(self):
        res, err = self.run_(D, self.stem, ["k", "s", "cp"])
        self.assertGreater(counts(res).get("claps", 0), 0, counts(res))
        self.assertTrue(all(tok.startswith(("cp/", "R/")) for tok in res["claps"]["score"].split()))
        self.assertNotIn("not exported", err)
        # the export alone changed: without the claps family the same transcription is the old one minus claps
        saved = D.FAMILIES.pop("claps")
        try:
            before, err0 = self.run_(D, self.stem, ["k", "s", "cp"])
        finally:
            D.FAMILIES["claps"] = saved
        self.assertEqual({k: v for k, v in res.items() if k != "claps"}, before)
        self.assertRegex(err0, r"not exported .*cp \d+ hits", "without a family the loss is reported, not silent")

    def test_a_piece_in_no_family_is_reported(self):
        _, err = self.run_(D, self.kx, ["k", "s", "zz"])
        self.assertIn("not exported", err)
        self.assertRegex(err, r"zz \d+ hits")

    def test_a_kit_without_cp_is_unchanged(self):
        res, err = self.run_(D, self.ks, ["k", "s"])
        self.assertNotIn("claps", res)
        self.assertNotIn("not exported", err)

    @unittest.skipUnless(os.environ.get("DRUMTRANS_OLD"), "set DRUMTRANS_OLD to the previous drumtrans.py")
    def test_kick_snare_output_is_identical_to_before(self):
        old = load(os.environ["DRUMTRANS_OLD"], "drumtrans_old")
        self.assertEqual(self.run_(D, self.ks, ["k", "s"])[0], self.run_(old, self.ks, ["k", "s"])[0])
        self.assertEqual(self.run_(D, self.stem, ["k", "s"])[0], self.run_(old, self.stem, ["k", "s"])[0])
        new, _ = self.run_(D, self.stem, ["k", "s", "cp"])
        before = self.run_(old, self.stem, ["k", "s", "cp"])[0]
        if "claps" in old.FAMILIES:
            self.assertEqual(new, before)
        else:   # a widthfit older than bd-dfa7eb: the old output is the new one without its claps
            self.assertEqual({k: v for k, v in new.items() if k != "claps"}, before)


def kit_pieces():
    """{piece: {kit, …}} for every `kit:` in the config's patches and, if found, the installed library's."""
    import glob
    dirs = [os.path.join(os.path.dirname(TOOLS), "patches"),
            os.environ.get("CHIRP_LIBRARY_PATCHES",
                           os.path.expanduser("~/.pi/agent/git/github.com/harryaskham/tools/cli/chirp/crates/chirp-cli/library/patches"))]
    out = {}
    for path in [p for d in dirs if os.path.isdir(d) for p in glob.glob(os.path.join(d, "*.yaml"))]:
        lines = open(path).read().splitlines()
        for i, ln in enumerate(lines):
            if not re.match(r"^(\s*)kit:\s*$", ln):
                continue
            ind = len(ln) - len(ln.lstrip())
            body = [x for x in lines[i + 1:] if x.strip() and not x.lstrip().startswith("#")]
            kind = len(body[0]) - len(body[0].lstrip()) if body else 0
            for nl in body:
                nind = len(nl) - len(nl.lstrip())
                if nind <= ind:
                    break
                m = re.match(r"^\s*([A-Za-z0-9_]+):", nl)
                if m and nind == kind:
                    out.setdefault(m.group(1), set()).add(os.path.basename(path)[:-5])
    return out


class Families(unittest.TestCase):
    """bd-dbdf72: every kit piece has a family, so no selected hit is dropped at export."""

    def test_every_kit_piece_has_a_family(self):
        homed = [p for ms in D.FAMILIES.values() for p in ms]
        self.assertEqual(len(homed), len(set(homed)), "a piece belongs to one family")
        pieces = kit_pieces()
        self.assertGreater(len(pieces), 50)
        missing = {p: sorted(k) for p, k in pieces.items() if p not in homed}
        self.assertEqual(missing, {}, "kit pieces without a drumtrans family")

    def test_maracas_export_as_perc(self):
        from unittest.mock import patch
        T = np.eye(80, 2)
        frames = np.array([8, 208])
        feats = {8: T[:, 0] * 2.0, 208: T[:, 1] * 2.0}
        with tempfile.TemporaryDirectory() as d:
            song = os.path.join(d, "t.yaml")
            with open(song, "w") as f:
                f.write("tempo: 60\n")
            err = io.StringIO()
            with patch.object(D.L, "load", return_value=np.zeros((48000, 2), np.float32)), \
                    patch.object(D, "bands", return_value=np.ones((40, 80))), patch.object(D, "pick", return_value=frames), \
                    patch.object(D, "templates", return_value=(T, np.ones(2), np.ones(2))), \
                    patch.object(D, "feat", side_effect=lambda _B, fr: feats[int(fr)]), redirect_stderr(err):
                res, _ = D.transcribe("x.wav", song, "t.wav", ["k", "ma"])
        self.assertIn("perc", res)
        self.assertTrue(res["perc"]["score"].count("ma/"), res["perc"]["score"])
        self.assertNotIn("not exported", err.getvalue())


class KitLevels(unittest.TestCase):
    """bd-6f5e5a: --kit-levels reads each hit in its own piece's velocity-120 units. Detection and classification are
    mocked exactly (one orthogonal template per piece), so only the velocity inversion is under test."""

    def run_mock(self, levels, gammas, hits, **kw):
        from unittest.mock import patch
        T = np.eye(80, len(levels))
        frames = np.arange(len(hits)) * 200 + 8   # ~1.07 s apart: one hit per grid slot
        gain = kw.pop("stem_gain", 1.0)
        feats = {int(f): T[:, i] * levels[i] * (v / 120) ** gammas[i] * gain for f, (i, v) in zip(frames, hits)}
        pieces = ["k", "s", "h"][:len(levels)]
        with tempfile.TemporaryDirectory() as d:
            song = os.path.join(d, "t.yaml")
            with open(song, "w") as f:
                f.write("tempo: 60\n")
            err = io.StringIO()
            with patch.object(D.L, "load", return_value=np.zeros((48000, 2), np.float32)), \
                    patch.object(D, "bands", return_value=np.ones((40, 80))), patch.object(D, "pick", return_value=frames), \
                    patch.object(D, "templates", return_value=(T, np.array(gammas, float), np.array(levels, float))), \
                    patch.object(D, "feat", side_effect=lambda _B, fr: feats[int(fr)]), redirect_stderr(err):
                res, _ = D.transcribe("x.wav", song, "t.wav", pieces, **kw)
        fams = {"k": "kick", "s": "snare", "h": "hats"}
        out = {}
        for p in pieces:
            out[p] = [int(v) for v in re.findall(r"@(\d+)", res.get(fams[p], {}).get("score", ""))]
        return out, err.getvalue()

    def test_unequal_piece_levels_read_as_equal_playing(self):
        for levels in ([1.0, 10.0], [10.0, 1.0]):
            got, _ = self.run_mock(levels, [1.0, 1.0], [(0, 120), (1, 120)], kit_levels=True)
            self.assertEqual(got, {"k": [120], "s": [120]}, levels)
            legacy, _ = self.run_mock(levels, [1.0, 1.0], [(0, 120), (1, 120)])
            self.assertNotEqual(legacy, {"k": [120], "s": [120]}, "the default keeps its single calibration")

    def test_round_trip_with_unequal_levels_and_gammas(self):
        levels, gammas = [1.0, 10.0, 0.3], [0.6, 1.0, 1.7]
        hits = [(i, v) for i in range(3) for v in (40, 80, 100, 120)]
        want = {"k": [40, 80, 100, 120], "s": [40, 80, 100, 120], "h": [40, 80, 100, 120]}
        got, err = self.run_mock(levels, gammas, hits, kit_levels=True, source_gain_db=0.0)
        self.assertEqual(got, want)
        self.assertIn("source gain +0.00 dB (given)", err)
        hot, _ = self.run_mock(levels, gammas, hits, kit_levels=True, source_gain_db=20 * np.log10(2), stem_gain=2.0)
        self.assertEqual(hot, want, "a stem 6 dB hot, with its gain given")
        auto, err = self.run_mock(levels, gammas, hits, kit_levels=True)
        self.assertIn("95th-percentile", err)
        for p in "ksh":
            self.assertEqual(auto[p], sorted(auto[p]), "order kept")
        for j in range(4):   # equal playing reads as equal velocity, whatever the piece's level and curve
            col = [auto[p][j] for p in "ksh"]
            self.assertLessEqual(max(col) - min(col), 3, auto)
        self.assertTrue(118 <= max(auto["k"]) <= 127, "the anchors' 95th-percentile hit is velocity 120")


@unittest.skipUnless(os.access(os.environ.get("CHIRP", ""), os.X_OK), "set CHIRP to an engine build to render the 909")
class KitLevelsRendered(unittest.TestCase):
    """The same on real renders: the 909's pieces sit 22 dB apart at velocity 120; every piece plays 50/80/110."""

    def test_the_909(self):
        import subprocess as sp
        d = tempfile.mkdtemp(prefix="kitlevels-")
        self.addCleanup(shutil.rmtree, d, True)
        pieces, vels = ["k", "s", "h", "cp"], [50, 80, 110]
        tpl = D.template_song("909", pieces)
        tracks = [{"name": p, "patch": "909", "score": " ".join(
            " ".join(["R/1b"] * i + [f"{p}/1b@{vels[bar % 3]}"] + ["R/1b"] * (3 - i)) for bar in range(24))}
            for i, p in enumerate(pieces)]
        for name, song in (("tpl", tpl), ("stem", {"tempo": 120, "tail": "2s", "tracks": tracks})):
            with open(os.path.join(d, f"{name}.json"), "w") as f:
                f.write(__import__("json").dumps(song))
            sp.run([os.environ["CHIRP"], "render", "-f", os.path.join(d, f"{name}.json"), "-o", os.path.join(d, f"{name}.wav")],
                   check=True, capture_output=True, stdin=sp.DEVNULL)
        song = os.path.join(d, "song.yaml")
        with open(song, "w") as f:
            f.write("tempo: 120\ntracks: []\n")
        fams = {"k": "kick", "s": "snare", "h": "hats", "cp": "claps"}

        def medians(kit_levels):
            with redirect_stderr(io.StringIO()):
                res, _ = D.transcribe(os.path.join(d, "stem.wav"), song, os.path.join(d, "tpl.wav"), pieces,
                                      vel_gamma=1.5, kit_levels=kit_levels)
            out = {}
            for i, p in enumerate(pieces):
                pos, hits = 0.0, {}
                for tok in res[fams[p]]["score"].split():
                    m = re.match(r"([^/]+)/([0-9.]+)b(?:@(\d+))?", tok)
                    if m.group(1) != "R" and m.group(3):
                        hits[round(pos, 2)] = int(m.group(3))
                    pos += float(m.group(2))
                got = {v: [] for v in vels}
                for bar in range(24):
                    near = [hits[x] for x in hits if abs(x - (bar * 4 + i)) <= 0.1]
                    if near:
                        got[vels[bar % 3]].append(near[0])
                out[p] = [float(np.median(got[v])) for v in vels]
            return out

        kl, legacy = medians(True), medians(False)
        for p in ("s", "h", "cp"):
            for want, have in zip(vels, kl[p]):
                self.assertLessEqual(abs(have - want), 12, f"{p}: {kl[p]}")
        self.assertEqual(kl["k"], sorted(kl["k"]), "the kick keeps its order")
        self.assertLess(legacy["h"][2], 40, "the default reads the quiet hats as soft playing (the bug)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
