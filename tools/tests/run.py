#!/usr/bin/env python3
"""run: the whole tools/tests suite, EACH FILE IN ITS OWN PROCESS (chirp-eco, 14 Nov).

  python3 tools/tests/run.py [WORD ...] [-j 6] [--dir DIR] [--list]

Every test file here is written to be run by itself (`python3 tools/tests/test_X.py`), and some depend on it: a few
set CLIMB_ROOT to a scratch folder as they are imported, and the tools read CLIMB_ROOT once, at import. So
`pytest tools/tests` in ONE process binds whatever is imported later to a folder that is then removed, and reports
failures that are not there (14 Nov: 29 failed and 6 errors across seven files, every one of which passes alone).
This runs each `test_*.py` in a process of its own (through pytest, which runs both the unittest classes and the
plain test functions), a few at a time at low priority, and prints what failed with its own lines.

WORD ...   only the files whose name holds one of the words (run.py stembal presence)
-j N       how many at once (default 6)
--dir DIR  another folder of test files (default: this one)
--list     name the files and stop
Exit status 1 when any file fails. About two and a half minutes for everything; run it after touching a module
other tools import (compscore, presence, stembal, wincut, notechk, keybench, listen).
"""
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))


def files(where, words):
    """The test files of a folder, by name; only those holding one of `words` when any are given."""
    names = sorted(f for f in os.listdir(where) if f.startswith("test_") and f.endswith(".py"))
    return [f for f in names if not words or any(w in f for w in words)]


def counts(text):
    """{"passed": n, "failed": n, "skipped": n, "error": n} from pytest's last summary line ({} when there is none)."""
    out = {}
    for line in reversed(text.splitlines()):
        found = re.findall(r"(\d+) (passed|failed|skipped|errors?|subtests passed)", line)
        if found:
            for n, what in found:
                key = "error" if what.startswith("error") else what
                if key != "subtests passed":
                    out[key] = out.get(key, 0) + int(n)
            break
    return out


def one(where, name):
    """(name, exit status, counts, the lines that say what failed, seconds) for one file in its own process."""
    env = {k: v for k, v in os.environ.items() if k not in ("LD_LIBRARY_PATH", "CLIMB_ROOT")}
    env["OPENBLAS_NUM_THREADS"] = "1"
    t0 = time.time()
    cwd = os.path.dirname(os.path.dirname(HERE)) if where == HERE else where       # the tests here are run from the config root
    r = subprocess.run(["nice", "-n", "14", sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        os.path.join(where, name)], capture_output=True, text=True, env=env, cwd=cwd)
    text = r.stdout + r.stderr
    said = [ln for ln in text.splitlines() if ln.startswith(("FAILED", "ERROR")) or "no tests ran" in ln]
    said += [ln for ln in text.splitlines() if ln.startswith("E  ")][:6]           # and why: pytest's own error lines
    if r.returncode and not said:
        said = text.strip().splitlines()[-3:]
    return name, r.returncode, counts(text), said, time.time() - t0


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if "-h" in a or "--help" in a:
        print(__doc__)
        return 0
    jobs, where = 6, HERE
    for flag in ("-j", "--dir"):
        if flag in a and a.index(flag) + 1 < len(a):
            i = a.index(flag)
            if flag == "-j":
                jobs = max(1, int(a[i + 1]))
            else:
                where = os.path.abspath(a[i + 1])
            del a[i:i + 2]
    listing = "--list" in a
    names = files(where, [w for w in a if not w.startswith("-")])
    if listing:
        print("\n".join(names))
        return 0
    if not names:
        print("run: no test files" + (f" matching {' '.join(a)}" if a else ""))
        return 1
    t0 = time.time()
    with ThreadPoolExecutor(jobs) as ex:
        results = list(ex.map(lambda n: one(where, n), names))
    total = {}
    bad = [r for r in results if r[1]]
    for _, _, c, _, _ in results:
        for k, v in c.items():
            total[k] = total.get(k, 0) + v
    for name, code, _, said, _ in bad:
        print(f"FAILED {name} (exit {code})")
        for ln in said[:12]:
            print("    " + ln[:200])
    slow = sorted(results, key=lambda r: -r[4])[:3]
    print(f"{len(names)} file(s), each in its own process: {len(names) - len(bad)} passed, {len(bad)} failed; tests "
          + ", ".join(f"{total.get(k, 0)} {k}" for k in ("passed", "failed", "error", "skipped") if total.get(k) or k == "passed")
          + f"; {time.time() - t0:.0f} s (slowest: " + ", ".join(f"{n[5:-3]} {s:.0f} s" for n, _, _, _, s in slow) + ")")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
