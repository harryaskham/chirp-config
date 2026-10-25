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
        r = bash('safe_pgrep -f x; echo "rc=$?"', env={**self.fake('echo 4242; exit 0'), "TMPDIR": tempfile.mkdtemp()})
        self.assertEqual(r.stdout.split(), ["4242", "rc=0"])
        r = bash('safe_pgrep -f x; echo "rc=$?"', env={**self.fake('exit 1'), "TMPDIR": tempfile.mkdtemp()})
        self.assertEqual(r.stdout.split(), ["rc=1"])

    def test_after_a_hang_it_answers_unknown_without_spawning(self):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        calls = os.path.join(d, "calls")
        env = self.fake(f'echo x >> {calls}; exec sleep 600')
        env["TMPDIR"] = d
        bash('safe_pgrep -f a >/dev/null; echo "rc=$?"', env=env)            # hangs once: marker
        self.assertTrue(os.path.exists(os.path.join(d, "chirp-pgrep-hung")))
        t = time.monotonic()
        r = bash('safe_pgrep -f b >/dev/null; echo "rc=$?"', env=env)
        self.assertIn("rc=2", r.stdout)
        self.assertLess(time.monotonic() - t, 3, "answered at once")
        self.assertEqual(open(calls).read().count("x"), 1, "no second pgrep was spawned")

    def test_a_hung_pgrep_never_holds_the_callers_lock(self):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        lock = os.path.join(d, "restart.lock")
        env = {**self.fake("exec sleep 30"), "TMPDIR": d}
        # the caller holds its flock on fd 9 (as restart-groove.sh does), asks, and exits; the hung pgrep lives on
        bash(f'exec 9>"{lock}"; flock 9; safe_pgrep -f x >/dev/null; echo "rc=$?"', env=env)
        r = subprocess.run(["flock", "-n", lock, "true"], capture_output=True)
        self.assertEqual(r.returncode, 0, "the lock is free once the caller has gone")

    def test_a_hung_pgrep_reports_unknown_quickly(self):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        with open(os.path.join(d, "pgrep"), "w") as f:
            f.write("#!/bin/sh\nexec sleep 600\n")
        os.chmod(os.path.join(d, "pgrep"), 0o755)
        t = time.monotonic()
        r = bash('safe_pgrep -f anything >/dev/null; echo "rc=$?"', env={"PATH": f"{d}:{os.environ['PATH']}", "TMPDIR": d})
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

    def test_unit_active_sees_a_running_unit(self):
        r = bash('launch proc-sh-active "sleep 5"; sleep 1; unit_active "proc-sh-active-*" && echo yes; '
                 'unit_active "proc-sh-none-*" || echo no')
        self.assertEqual(r.stdout.split(), ["yes", "no"])

    def test_the_groove_unit_gets_a_high_cpu_weight(self):
        d = tempfile.mkdtemp(prefix="proc-sh-")
        self.addCleanup(shutil.rmtree, d, True)
        log = os.path.join(d, "args")
        with open(os.path.join(d, "systemd-run"), "w") as f:     # a fake systemd-run that records its arguments
            f.write(f"#!/bin/sh\necho \"$@\" >> {log}\n")
        os.chmod(os.path.join(d, "systemd-run"), 0o755)
        env = {"PATH": f"{d}:{os.environ['PATH']}"}
        bash('launch chirp-groove "true"; launch chirp-playlist "true"', env=env)
        lines = open(log).read().splitlines()
        self.assertIn("-p CPUWeight=10000", lines[0])
        self.assertNotIn("CPUWeight", lines[1])

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
