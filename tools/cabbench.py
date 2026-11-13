#!/usr/bin/env python3
"""cabbench: a song's heavy guitar rigs with ANOTHER CABINET STAGE and no eq after the amp, each rendered alone on its
own riff, for reading against a record's guitar alone (cabspec.py, ripple.py, gspec.py). (chirper-zero, Common Time
v33 and the engine's `4x12-modern`, bd-af781d; the rigs and the binary made arguments by chirp-eco.)

  cabbench.py W NAME[=SPEC] ... [--rigs RIG=TRACK,TRACK:FROM-TO ...] [--pin CHIRP]

W is a work folder holding base.yaml: the song as its generator writes it (one track a line, `  - {...}`, and a
`patches: {...}` line), with the track and bus eqs off. Each rig's patch must be the djent family's shape: effect 2
the amp, effect 3 the cabinet (`ir` or `cab`), effect 4 the patch's eq. For every NAME the rigs' tracks get a
song-local copy of their patch with effect 3 replaced by SPEC and effect 4 removed (`fx.4.*` overrides on the track
go with it; the others, such as `fx.0.mix` and `fx.2.tight`, still point at the right effects).
SPEC (NAME alone = a SPEC of that name):
  amp                             nothing: the amp's output as the cabinet receives it (the dry file for ripple --over)
  files                           the rig as it is (its ir files, or its cab), eq off
  cab:MODEL[:MIC[:DIST[:CONES]]]  the engine's cab model on every rig; CONES "0,1" = the cone of the left tracks and
                                  of the right ones (a track is a right one when its name, less a trailing 2, ends in r)
  eq:BANDS                        an eq standing in for a cabinet, BANDS as a song takes them, separated by '|'
                                  (e.g. "hp cutoff=70 q=0.9|peak cutoff=110 q=1.3 gain=4.5dB|lp cutoff=5600 q=0.7")
  json:FILE                       effect 3 replaced by the effects (a JSON list) in FILE
Writes W/NAME.yaml and W/NAME-RIG.wav (raw: loudness off, seed 0), two renders at a time, and prints "done NAME".
--rigs: which tracks make a rig and the bars it plays alone (as `chirp render --from/--to` take them). Default,
Common Time's three: chug=gl,gr:42-48 bite=sl,sr:80-86 wall=wl,wr:113-119.
--pin: the chirp binary (else $CZ_CHIRP, else the groove's pin). Tests: tools/tests/test_cabbench.py.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RIGS = {"chug": (("gl", "gr"), 42, 48), "bite": (("sl", "sr"), 80, 86), "wall": (("wl", "wr"), 113, 119)}


def clean_env():
    return {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}


def resolved(pin, name):
    out = subprocess.run([pin, "patch", "show", name, "--resolved", "--json"], capture_output=True, text=True, env=clean_env()).stdout
    return json.loads(out)["data"]["patch"]


def stage(spec, right=False):
    if spec == "amp":
        return [{"type": "gain", "gain": "0dB"}]
    if spec == "files":
        return None
    k, _, rest = spec.partition(":")
    if k == "cab":
        a = rest.split(":")
        fx = {"type": "cab", "model": a[0]}
        if len(a) > 1:
            fx["mic"] = float(a[1])
        if len(a) > 2:
            fx["distance"] = float(a[2])
        if len(a) > 3:
            c = int(a[3].split(",")[1 if right else 0])
            if c:
                fx["cone"] = c
        return [fx]
    if k == "eq":
        return [{"type": "eq", "bands": [b for b in rest.split("|") if b]}]
    if k == "json":
        with open(rest) as f:
            return json.load(f)
    raise SystemExit("unknown spec " + spec)


def build(W, name, spec, rigs, pin):
    with open(W + "/base.yaml") as f:
        lines = f.read().split("\n")
    local = {}
    for i, ln in enumerate(lines):
        if ln.startswith("  - {"):
            t = json.loads(ln[4:])
            if any(t["name"] in trs for trs, _, _ in rigs.values()):
                base, _, suffix = t["patch"].partition(" ")
                st = stage(spec, t["name"].rstrip("2").endswith("r"))
                p = resolved(pin, base)
                fx = p["fx"]
                if not (len(fx) > 4 and fx[2]["type"] == "amp" and fx[3]["type"] in ("ir", "cab") and fx[4]["type"] == "eq"):
                    raise SystemExit(f"cabbench: {base} is not amp, cabinet, eq at effects 2, 3, 4: {[e['type'] for e in fx]}")
                keep = " ".join(s for s in suffix.split() if not s.startswith("fx.4."))        # the eq's overrides go with the eq
                cabs = [fx[3]] if st is None else st
                # the amp stays fx.2 and the old overrides (fx.0.mix, fx.2.tight) still point at the right effects
                p["fx"] = fx[:3] + cabs + fx[5:]
                p["about"] = "cabbench " + name
                nm = "cb-" + base
                local[nm] = p
                t["patch"] = nm + (" " + keep if keep else "")
                t.pop("fx", None)
                lines[i] = "  - " + json.dumps(t)
    for i, ln in enumerate(lines):
        if ln.startswith("patches:"):
            d = json.loads(ln[len("patches:"):])
            d.update(local)
            lines[i] = "patches: " + json.dumps(d)
    y = f"{W}/{name}.yaml"
    with open(y, "w") as f:
        f.write("\n".join(lines))
    return y


def parse_rigs(tokens):
    rigs = {}
    for tok in tokens:
        try:
            name, rest = tok.split("=", 1)
            trs, span = rest.rsplit(":", 1)
            b0, b1 = span.split("-")
            rigs[name] = (tuple(trs.split(",")), b0, b1)
        except ValueError:
            raise SystemExit("cabbench: --rigs RIG=TRACK,TRACK:FROM-TO, as in --rigs chug=gl,gr:42-48") from None
    return rigs


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) < 2 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    pin = os.environ.get("CZ_CHIRP")
    if "--pin" in a:
        i = a.index("--pin")
        pin = a[i + 1]
        del a[i:i + 2]
    rigs = RIGS
    if "--rigs" in a:
        i = a.index("--rigs")
        j = i + 1
        while j < len(a) and "=" in a[j] and ":" in a[j] and not a[j].partition("=")[2].startswith(("cab:", "eq:", "json:")):
            j += 1
        rigs = parse_rigs(a[i + 1:j])
        del a[i:j]
    if not pin:
        with open(ROOT + "/tools/groove-pin") as f:
            pin = f.readline().strip()
    W = a[0]
    env = clean_env()
    for arg in a[1:]:
        name, _, spec = arg.partition("=")
        spec = spec or name
        y = build(W, name, spec, rigs, pin)
        procs = []
        for rig, (trs, b0, b1) in rigs.items():
            cmd = ["nice", "-n", "7", pin, "render", "--threads", "2", "-f", y, "--seed", "0", "--from", str(b0), "--to", str(b1),
                   "--set", "loudness=null", "-o", f"{W}/{name}-{rig}.wav"]
            for t in trs:
                cmd += ["--solo", t]
            procs.append((rig, subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, env=env)))
            if len(procs) == 2:
                for r, p in procs:
                    e = p.communicate()[1]
                    if p.returncode:
                        print(name, r, "FAILED", e.strip()[-300:])
                procs = []
        for r, p in procs:
            e = p.communicate()[1]
            if p.returncode:
                print(name, r, "FAILED", e.strip()[-300:])
        print("done", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
