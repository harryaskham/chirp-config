#!/usr/bin/env python3
"""The chirp engine a tool renders with when $CHIRP is unset: the groove's adopted pin (tools/groove-pin, the binary
every climb measures on), never the PATH `chirp` (the old Nix 0.1.0) or a shared build path that goes stale (the
/tmp/lt/chirp-main build sat five days and eight adoptions behind the groove; jobs queued without CHIRP failed or,
worse, measured on it). $CHIRP still wins; a host without a usable groove pin keeps the tool's old default, with a
warning on stderr.

  import chirpbin; C = chirpbin.resolve("/old/default")
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def resolve(fallback="chirp"):
    v = os.environ.get("CHIRP")
    if v:
        return v
    try:
        with open(os.path.join(HERE, "groove-pin")) as f:
            pin = f.read().strip()
    except OSError:
        pin = ""
    if pin and os.path.isfile(pin) and os.access(pin, os.X_OK):
        return pin
    print(f"chirpbin: tools/groove-pin is {'unusable: ' + pin if pin else 'missing'}; using {fallback} (set CHIRP to "
          "the adopted pin)", file=sys.stderr)
    return fallback


if __name__ == "__main__":
    print(resolve())
