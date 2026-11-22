#!/usr/bin/env python3
"""wtry: draw idioms of wild.py over a stretch of a song, one strip of frames each.

    wtry.py N A B OUT.jpg [idiom …] [key=value …]

Song N, bars A..B. Each idiom is drawn at 480x270 and six frames of it are laid in a row.
Environment: P (the chirp to draw with), SIZE, FPS, JOBS, FRAMES.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wild as W  # noqa: E402
import wildgen as G  # noqa: E402

P = os.environ.get("P") or G.C.CHIRP
SIZE = os.environ.get("SIZE", "480x270")
FPS = os.environ.get("FPS", "12")
JOBS = int(os.environ.get("JOBS", "5"))
FRAMES = int(os.environ.get("FRAMES", "6"))
TMP = "/tmp/cv/ct/w"


def main():
    n, a, b, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    names = [x for x in sys.argv[5:] if "=" not in x] or sorted(W.REG)
    kw = dict(x.split("=", 1) for x in sys.argv[5:] if "=" in x)
    if "arrive" in kw:      # arrive=1: the treatment comes on half way through
        W.Cx.arrive = f"smooth({(a + b) * 2 - 0.12:g}, {(a + b) * 2 + 0.12:g}, time.beat)"
    song = f"chirpers10-t{n}"
    S = G.Song(n)
    bar_s = S.bar_s
    os.makedirs(TMP, exist_ok=True)

    def one(name):
        c = S.cx(int(a * 16), int(b * 16), k=int(kw.get("k", 0)), variant=int(kw.get("v", 0)), paper=bool(int(kw.get("paper", 0))))
        # NAME, NAME/TREATMENT, or A+B/COMBINATION.
        spec = name
        base, _, how = name.partition("/")
        name = name.replace("/", "_").replace("+", "-")
        try:
            if "+" in base:
                x, y_ = base.split("+")
                look = W.COMBOS[how or "double"](c, W.bolder(x, W.REG[x]["f"](c)), W.bolder(y_, W.REG[y_]["f"](c.sub(1 if len(c.riffs) > 1 else 0, 2))))
            else:
                look = W.bolder(base, W.REG[base]["f"](c))
                if how:
                    for h in how.split(","):
                        look = W.TREAT[h][0](c, look) if h in W.TREAT else W.rostrum(c, look, h)
        except Exception as e:  # noqa: BLE001
            return spec, None, f"{type(e).__name__}: {e}"
        prog = {"scenes": [{"at": 0, "look": {"layers": []}}, {"at": f"{a:g}bar", "look": look, "lead": "1bar"}]}
        y = f"{TMP}/{name}.yaml"
        json.dump(prog, open(y, "w"), indent=1)
        r = subprocess.run([P, "--json", "vis", "check", y, "-f", f"{song}.yaml"], capture_output=True, text=True, cwd=G.C.CFG + "/songs")
        if '"ok":true' not in r.stdout:
            return name, None, (r.stdout + r.stderr)[:600]
        mp4 = f"{TMP}/{name}.mp4"
        cmd = ["systemd-run", "--user", "--collect", "-q", "--wait", "--pipe", f"--unit=guarded-soft-cv-w-{name}-{os.getpid()}", "-p", "CPUSchedulingPolicy=idle", "-p", "Nice=15",
               "-p", "AllowedCPUs=4-23", f"--setenv=PATH={os.environ['PATH']}", f"--setenv=HOME={os.environ['HOME']}", "--setenv=RAYON_NUM_THREADS=4", f"--working-directory={G.C.CFG}/songs",
               P, "--json", "video", "--vis", y, "-f", f"{song}.yaml", "--audio", f"/tmp/cv/ct/wav/t{n}.wav", "--from", f"{a * bar_s:.3f}s", "--to", f"{b * bar_s:.3f}s",
               "--size", SIZE, "--fps", FPS, "--preset", "ultrafast", "--warmup", f"{bar_s:.2f}", "--no-safety", "-o", mp4]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if not os.path.exists(mp4) or r.returncode:
            return name, None, (r.stdout + r.stderr)[-600:]
        ms = ""
        try:
            ms = f"{json.loads(r.stdout)['data'].get('draw_ms', 0):.0f} ms"
        except Exception:  # noqa: BLE001
            pass
        dur = (b - a) * bar_s
        row = f"{TMP}/{name}.jpg"
        w = int(SIZE.split("x")[0])
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-vf",
                        f"fps={FRAMES / dur:.5f},scale={w}:-1,tile={FRAMES}x1:padding=2:color=0x303030,drawtext=text='{name} {ms}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6",
                        "-frames:v", "1", "-update", "1", "-q:v", "3", row], capture_output=True)
        return name, row, ms

    with ThreadPoolExecutor(JOBS) as ex:
        res = list(ex.map(one, names))
    rows = [r for _, r, _ in res if r and os.path.exists(r)]
    for name, r, msg in res:
        print(f"{name:16s} {'ok ' + msg if r else 'FAILED ' + msg}")
    if rows:
        ins = sum((["-i", r] for r in rows), [])
        if len(rows) == 1:
            subprocess.run(["cp", rows[0], out])
        else:
            subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", f"vstack=inputs={len(rows)}", "-frames:v", "1", "-update", "1", "-q:v", "4", out])
        print(out)


if __name__ == "__main__":
    main()
