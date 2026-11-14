#!/usr/bin/env python3
"""arrivals: each section's level beside the one after it, and an ARRIVAL that is quieter than its approach.
(chirp-eco, 14 Nov, for chirper-zero's finding on Plain Hunt v4: "read a passage against the NEXT one, not only
against its old self". A lead at a sensible level made a climb 0.7 dB louder than the landing it leads to; the climb
read against the last version would have passed a song whose arrival is the quieter of the two.)

  arrivals.py SONG MARK [MARK ...] [--edge 4] [--flag 0.5] [--to POS] [--wav FILE] [--mastered] [--pin CHIRP] [--json]

SONG is an id (songs/ID.yaml) or a file. Each MARK is where a section starts, as `chirp render --from` takes
positions, with a label if wanted: 94:climb, 372b:climb, 232s. A `!` after the position says the section is an
ARRIVAL, a place the music is meant to land: 109!:landing. The sections run from each mark to the next; the last
to the end of the render (or --to POS).
It renders the mix ONCE, RAW (loudness off, seed 0: what the groove plays, where one passage's level against the
next is heard as written), and prints for each section:
  level      its loudness (K-weighted, gated, as LUFS)
  opens      its first --edge bars (default 4)
  closes     its last --edge bars
  step in    its opening against the close of the section before        (how it ARRIVES)
  vs before  its level against the section before's                     (how it SITS after it)
and at every `!` mark flags QUIETER THAN ITS APPROACH when the step in, or the section against the one before, is
down by --flag dB or more (default 0.5). Marks without a `!` are never flagged: a break is meant to fall.
--mastered renders with the song's own loudness and limiter instead (what the released file will do: a limiter
flattens steps the raw mix has). --wav FILE reads a render already made in place of rendering (raw or mastered is
then what that file is; the positions still come from the song's tempo).
What it cannot say: whether an arrival FEELS like one. Level is one of the things an arrival is made of (weight in
the low end, a new part, a stop before it are others); tools/stembal.py reads the bands, the ear the rest.
Only songs in one tempo and 4/4. Read-only. Tests: tools/tests/test_arrivals.py.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402
import levels  # noqa: E402
import likeness as L  # noqa: E402
import wincut  # noqa: E402


def mark(text, tempo):
    """"109!:landing" -> {"pos": "109", "at": seconds, "arrival": True, "label": "landing"}; None when it is not one."""
    pos, _, label = text.partition(":")
    arrival = pos.endswith("!")
    pos = pos.rstrip("!")
    at = wincut.position(pos, tempo)
    return None if at is None else {"pos": pos, "at": at, "arrival": arrival, "label": label}


def lufs(x, sr):
    return round(levels.loudness(x, sr)[0], 1) if len(x) else None


def sections(x, sr, marks, end, edge_s):
    """[{label, pos, at, to, arrival, level, opens, closes, step, vs_before}] for the stretches between the marks
    (seconds; the last runs to `end`). The edges are edge_s seconds, or the whole section when it is shorter."""
    rows = []
    for m, nxt in zip(marks, marks[1:] + [{"at": end}]):
        s0, s1 = m["at"], min(nxt["at"], end)
        if s1 <= s0:
            continue
        f0, f1 = wincut.frames(s0, s1, sr)
        seg = x[f0:f1]
        e = min(len(seg), int(round(edge_s * sr)))
        rows.append({"label": m["label"], "pos": m["pos"], "at": round(s0, 2), "to": round(s1, 2), "arrival": m["arrival"],
                     "level": lufs(seg, sr), "opens": lufs(seg[:e], sr), "closes": lufs(seg[len(seg) - e:], sr),
                     "step": None, "vs_before": None})
    for before, r in zip(rows, rows[1:]):
        r["step"] = round(r["opens"] - before["closes"], 1)
        r["vs_before"] = round(r["level"] - before["level"], 1)
    return rows


def flagged(r, flag):
    """Why an arrival is quieter than its approach ("" when it is not, or when the section is no arrival)."""
    if not r["arrival"] or r["step"] is None:
        return ""
    why = []
    if r["step"] <= -flag:
        why.append(f"it opens {-r['step']:.1f} dB under the close before it")
    if r["vs_before"] <= -flag:
        why.append(f"it sits {-r['vs_before']:.1f} dB under the section before it")
    return "QUIETER THAN ITS APPROACH: " + " and ".join(why) if why else ""


def render(pin, song, out, mastered, to=None):
    cmd = ["nice", "-n", "12", pin, "render", "-f", song, "--seed", "0", "--threads", "4", "-o", out]
    cmd += [] if mastered else ["--set", "loudness=null"]
    cmd += ["--to", to] if to else []
    env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env=env)
    if r.returncode:
        raise SystemExit("arrivals: the song did not render: " + (r.stderr or r.stdout).strip()[-400:])
    return out


def clock(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {"--pin": None, "--wav": None, "--edge": "4", "--flag": "0.5", "--to": None}
    for k in list(opt):
        if k in a and a.index(k) + 1 < len(a):
            i = a.index(k)
            opt[k] = a[i + 1]
            del a[i:i + 2]
    flags = {k: k in a for k in ("--json", "--mastered")}
    a = [x for x in a if x not in flags]
    if len(a) < 2 or "-h" in a or "--help" in a:
        print(__doc__)
        return 0 if ("-h" in a or "--help" in a) else 2
    song = a[0] if os.path.exists(a[0]) else os.path.join(ROOT, "songs", a[0] + ".yaml")
    if not os.path.exists(song):
        raise SystemExit(f"arrivals: no song {a[0]}")
    pin = opt["--pin"] or chirpbin.resolve()
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True, cwd=ROOT,
                       env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
    try:
        canon = json.loads(r.stdout)["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"arrivals: {os.path.basename(song)} does not plan") from None
    tempo = canon.get("tempo", 120.0)
    if (not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0
            or str(canon.get("meter") or "4/4").replace(" ", "") != "4/4"):
        raise SystemExit("arrivals: only songs in one tempo and 4/4 are read")
    try:
        edge, flag = float(opt["--edge"]), float(opt["--flag"])
    except ValueError:
        raise SystemExit("arrivals: --edge takes bars and --flag dB, as in --edge 4 --flag 0.5") from None
    marks = [mark(t, tempo) for t in a[1:]]
    if None in marks:
        raise SystemExit(f"arrivals: {a[1:][marks.index(None)]}: a MARK is POS[!][:label], POS as chirp render takes one "
                         "(94, 372b, 232s)")
    marks.sort(key=lambda m: m["at"])
    to = wincut.position(opt["--to"], tempo) if opt["--to"] else None
    if opt["--to"] and to is None:
        raise SystemExit(f"arrivals: --to {opt['--to']}: a position as chirp render takes one")
    work = None
    try:
        wav = opt["--wav"]
        if not wav:
            work = tempfile.mkdtemp(prefix="arrivals-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
            wav = render(pin, song, os.path.join(work, "mix.wav"), flags["--mastered"], opt["--to"])
        x = L.load(wav)
    finally:
        if work:
            for f in os.listdir(work):
                os.remove(os.path.join(work, f))
            os.rmdir(work)
    end = min(len(x) / L.SR, to) if to else len(x) / L.SR
    rows = sections(x, L.SR, marks, end, edge * 240.0 / tempo)
    for r in rows:
        r["flag"] = flagged(r, flag)
    what = "a render given" if opt["--wav"] else ("mastered" if flags["--mastered"] else "raw")
    if flags["--json"]:
        print(json.dumps({"song": os.path.basename(song), "what": what, "edge_bars": edge, "flag_db": flag, "sections": rows}))
        return 0
    print(f"{os.path.basename(song)} ({what}; seed 0; edges of {edge:g} bars): each section beside the one before it")
    width = max(12, max(len(r["label"] or r["pos"]) for r in rows) + 2) if rows else 12
    print(f"  {'section':{width}s} {'at':>6s} {'level':>7s} {'opens':>7s} {'closes':>7s} {'step in':>8s} {'vs before':>10s}")
    for r in rows:
        name = (r["label"] or r["pos"]) + ("!" if r["arrival"] else "")
        step = f"{r['step']:+8.1f}" if r["step"] is not None else f"{'':8s}"
        vs = f"{r['vs_before']:+10.1f}" if r["vs_before"] is not None else f"{'':10s}"
        print(f"  {name:{width}s} {clock(r['at']):>6s} {r['level']:7.1f} {r['opens']:7.1f} {r['closes']:7.1f} {step} {vs}"
              + (f"   {r['flag']}" if r["flag"] else ""))
    n = sum(1 for r in rows if r["flag"])
    arrivals = sum(1 for r in rows if r["arrival"])
    if not arrivals:
        print("  (no mark has a `!`: nothing is called an arrival, so nothing is flagged)")
    elif n:
        print(f"  {n} of {arrivals} arrival(s) quieter than the approach (by {flag:g} dB or more): the ear's to judge; level is "
              "one of the things an arrival is made of")
    else:
        print(f"  {arrivals} arrival(s), none quieter than its approach")
    return 0


if __name__ == "__main__":
    sys.exit(main())
