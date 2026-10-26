#!/usr/bin/env python3
"""tools/livestems.py --gpu: picks the ROCm GPU with the most compute units (pocket4: the 7900 XTX over the 890M) and
only then sets the HIP environment.

  python3 tools/tests/test_livestems_gpu.py      (from ~/.config/chirp; instant)
"""
import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import livestems as S  # noqa: E402

ROCMINFO = """*******
Agent 1
*******
  Name:                    AMD Ryzen AI 9 HX 370 w/ Radeon 890M
  Device Type:             CPU
  Compute Unit:            24
*******
Agent 2
*******
  Name:                    gfx1150
  Marketing Name:          AMD Radeon 890M Graphics
  Device Type:             GPU
  Compute Unit:            16
*******
Agent 3
*******
  Name:                    gfx1100
  Marketing Name:          AMD Radeon RX 7900 XTX
  Device Type:             GPU
  Compute Unit:            96
"""


class Gpu(unittest.TestCase):
    def test_agents_in_hip_order_cpu_skipped(self):
        self.assertEqual(S.gpu_agents(ROCMINFO), [(0, "gfx1150", 16), (1, "gfx1100", 96)])

    def test_explicit_ordinal(self):
        self.assertEqual(S.pick_gpu("0"), "0")

    def test_env_only_with_gpu(self):
        old = S.GPU[0]
        try:
            S.GPU[0] = None
            self.assertNotIn("HIP_VISIBLE_DEVICES", S.env(4))
            S.GPU[0] = "1"
            e = S.env(4)
            self.assertEqual((e["HIP_VISIBLE_DEVICES"], e["HSA_OVERRIDE_GFX_VERSION"]), ("1", "11.0.0"))
        finally:
            S.GPU[0] = old


if __name__ == "__main__":
    unittest.main()
