#!/usr/bin/env python3
"""tools/proc.sh: safe_pgrep never hangs its caller (a stuck process blocked plain pgrep, freezing the watchdog), and
launch starts a detached command as its own systemd user unit (a groove started inside an agent's pi-daemon.service died
with every switch that restarted it).

  python3 tools/tests/test_proc_sh.py      (from ~/.config/chirp; ~15 s)
"""
import os
import shutil
import subprocess
import tempfile
import time
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(TOOLS, "proc.sh")


def bash(script, env=None):
    return subprocess.run(["bash", "-c", f". {PROC}\n{script}"], capture_output=True, text=True, timeout=60,
                          env={**os.environ, **(env or {})})


class SafePgrep(unittest.TestCase):
    def fake(self, body):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        with open(os.path.join(d, "pgrep"), "w") as f:
            f.write("#!/bin/sh\n" + body + "\n")
        os.chmod(os.path.join(d, "pgrep"), 0o755)
        return {"PATH": f"{d}:{os.environ['PATH']}"}

    def test_found_and_not_found(self):
        # (a fake pgrep: the real one hangs on a host with a process stuck in the kernel, which is the point)
        r = bash('safe_pgrep -f x; echo "rc=$?"', env=self.fake('echo 4242; exit 0'))
        self.assertEqual(r.stdout.split(), ["4242", "rc=0"])
        r = bash('safe_pgrep -f x; echo "rc=$?"', env=self.fake('exit 1'))
        self.assertEqual(r.stdout.split(), ["rc=1"])

    def test_a_hung_pgrep_reports_unknown_quickly(self):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        with open(os.path.join(d, "pgrep"), "w") as f:
            f.write("#!/bin/sh\nexec sleep 600\n")
        os.chmod(os.path.join(d, "pgrep"), 0o755)
        t = time.monotonic()
        r = bash('safe_pgrep -f anything >/dev/null; echo "rc=$?"', env={"PATH": f"{d}:{os.environ['PATH']}"})
        self.assertIn("rc=2", r.stdout)
        self.assertLess(time.monotonic() - t, 20)


@unittest.skipUnless(shutil.which("systemd-run") and subprocess.run(["systemctl", "--user", "show-environment"],
                                                                     capture_output=True).returncode == 0,
                     "needs a systemd user manager")
class Launch(unittest.TestCase):
    def test_launch_runs_its_own_unit_that_outlives_the_caller(self):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        flag = os.path.join(d, "ran")
        r = bash(f'launch proc-sh-test "sleep 2; touch {flag}"; echo started')
        self.assertIn("started", r.stdout)
        units = subprocess.run(["systemctl", "--user", "list-units", "proc-sh-test-*", "--no-legend"],
                               capture_output=True, text=True).stdout
        self.assertIn("proc-sh-test-", units)
        for _ in range(40):
            if os.path.exists(flag):
                break
            time.sleep(0.25)
        self.assertTrue(os.path.exists(flag), "the command ran after the caller returned")

    def test_without_systemd_run_it_falls_back_to_setsid(self):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        flag = os.path.join(d, "ran")
        with open(os.path.join(d, "systemctl"), "w") as f:       # no user manager: launch must fall back
            f.write("#!/bin/sh\nexit 1\n")
        os.chmod(os.path.join(d, "systemctl"), 0o755)
        bash(f'launch proc-sh-test "touch {flag}"', env={"PATH": f"{d}:{os.environ['PATH']}"})
        for _ in range(40):
            if os.path.exists(flag):
                break
            time.sleep(0.25)
        self.assertTrue(os.path.exists(flag))


if __name__ == "__main__":
    unittest.main()
