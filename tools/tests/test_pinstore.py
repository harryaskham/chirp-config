#!/usr/bin/env python3
"""tools/pinstore.py: the groove's pin and the release pins outlive /tmp (the system deletes what nobody used for
ten days there, and restart-groove.sh refuses to start without its pin).

  python3 tools/tests/test_pinstore.py      (from ~/.config/chirp; under a second)
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import pinstore as P  # noqa: E402


class PinStore(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="pinstore-")
        self.addCleanup(self.cleanup)
        self.store = os.path.join(self.d, "store")
        self.pins = os.path.join(self.d, "tmp", "pins")
        os.makedirs(self.pins)
        self.pin = os.path.join(self.pins, "chirp-0a1b2c3d")
        with open(self.pin, "wb") as f:
            f.write(b"#!/bin/sh\necho engine\n" + bytes(range(256)) * 40)
        os.chmod(self.pin, 0o555)

    def cleanup(self):
        for root, dirs, files in os.walk(self.d):
            for n in dirs + files:
                os.chmod(os.path.join(root, n), 0o755)
        shutil.rmtree(self.d, True)

    def test_keep_then_restore_gives_the_same_binary_back(self):
        want = P.sha(self.pin)
        ok, msg = P.keep(self.pin, self.store)
        self.assertTrue(ok, msg)
        self.assertIn("stored", msg)
        os.chmod(self.pin, 0o755)
        os.remove(self.pin)
        shutil.rmtree(os.path.dirname(self.pin))             # the whole pins directory aged away
        ok, msg = P.restore(self.pin, self.store)
        self.assertTrue(ok, msg)
        self.assertIn("restored", msg)
        self.assertEqual(P.sha(self.pin), want)
        self.assertTrue(os.access(self.pin, os.X_OK))
        self.assertEqual(os.stat(self.pin).st_mode & 0o222, 0)   # pins are read-only, as adoption leaves them
        self.assertEqual([n for n in os.listdir(self.pins) if ".part-" in n], [])

    def test_restore_leaves_a_present_pin_alone(self):
        before = os.stat(self.pin).st_mtime_ns
        ok, msg = P.restore(self.pin, self.store)                # nothing stored, nothing needed
        self.assertTrue(ok, msg)
        self.assertIn("present", msg)
        self.assertEqual(os.stat(self.pin).st_mtime_ns, before)

    def test_restore_without_a_stored_copy_fails(self):
        gone = os.path.join(self.pins, "chirp-ffffffff")
        ok, msg = P.restore(gone, self.store)
        self.assertFalse(ok)
        self.assertIn("no stored copy", msg)
        self.assertFalse(os.path.exists(gone))

    def test_a_damaged_stored_copy_is_not_restored(self):
        P.keep(self.pin, self.store)
        stored = os.path.join(self.store, os.path.basename(self.pin))
        os.chmod(stored, 0o755)
        with open(stored, "ab") as f:
            f.write(b"x")
        os.chmod(self.pin, 0o755)
        os.remove(self.pin)
        ok, msg = P.restore(self.pin, self.store)
        self.assertFalse(ok)
        self.assertIn("no longer matches", msg)
        self.assertFalse(os.path.exists(self.pin))
        self.assertTrue(any("DOES NOT MATCH" in line for line in P.listing(self.store)))

    def test_keep_is_once_and_a_pin_never_changes(self):
        P.keep(self.pin, self.store)
        stored = os.path.join(self.store, os.path.basename(self.pin))
        first = P.sha(stored)
        ok, msg = P.keep(self.pin, self.store)
        self.assertTrue(ok)
        self.assertIn("already", msg)
        os.chmod(self.pin, 0o755)
        with open(self.pin, "ab") as f:
            f.write(b"another build")
        ok, msg = P.keep(self.pin, self.store)                   # a different binary under a stored name
        self.assertFalse(ok)
        self.assertIn("differs", msg)
        self.assertEqual(P.sha(stored), first)

    def test_seal_records_hashes_for_pins_stored_before_this_tool(self):
        os.makedirs(self.store)
        old = os.path.join(self.store, "chirp-01d0ld00")
        shutil.copyfile(self.pin, old)
        self.assertEqual(P.listing(self.store), [f"chirp-01d0ld00  {os.path.getsize(old) / 1e6:.1f} MB  no sha256"])
        self.assertEqual(len(P.seal(self.store)), 1)
        self.assertEqual(P.seal(self.store), [])
        self.assertTrue(P.listing(self.store)[0].endswith("ok"))

    def test_command_line_and_exit_codes(self):
        env = {**os.environ, "CHIRP_PIN_STORE": self.store}
        run = lambda *a: subprocess.run([sys.executable, os.path.join(TOOLS, "pinstore.py"), *a],  # noqa: E731
                                        capture_output=True, text=True, env=env)
        r = run("keep", self.pin)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        os.chmod(self.pin, 0o755)
        os.remove(self.pin)
        r = run("restore", self.pin)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.access(self.pin, os.X_OK))
        self.assertEqual(run("restore", os.path.join(self.pins, "chirp-ffffffff")).returncode, 1)
        self.assertEqual(run("list").returncode, 0)
        self.assertEqual(run("keep", os.path.join(self.pins, "chirp-ffffffff")).returncode, 1)

    def test_restart_groove_asks_the_store_before_it_refuses(self):
        with open(os.path.join(TOOLS, "restart-groove.sh")) as f:
            text = f.read()
        ask = text.find('pinstore.py" restore "$pin"')
        refuse = text.find("refusing to restart")
        self.assertGreater(ask, 0, "restart-groove.sh no longer restores a missing pin")
        self.assertLess(ask, refuse)


if __name__ == "__main__":
    unittest.main()
