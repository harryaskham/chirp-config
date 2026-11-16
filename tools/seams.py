#!/usr/bin/env python3
"""seams: DOES THE SONG STEP WHERE IT SHOULD? Its loudness stretch by stretch, and the step at each seam.
(chirp-eco, 16 Nov, from chirper-zero's Running Total v10: "a form fault the band readings cannot see: sections that
should step and do not". A piece about waiting for a riff to be whole read -9.3, -9.1, -9.3 LUFS through the count's
end, the first whole statement and the total: no step when it arrived. Found at v9 by hand, with ebur128 over bar
ranges; "a one-line LUFS by section, and the step at each seam, would have shown this at v1".)

  seams.py ID [--wav FINISHED.wav] [--least 2] [--quiet 4] [--json] [--pin CHIRP]
  seams.py ID [--wav FINISHED.wav] --windows 21-33:count 33-41:whole 41-49:total ...

ID is a climb (songs/ID.yaml) or a song file. --wav is the FINISHED file (mastered: the render the score reads, a
round's n-0.wav); without it the song is rendered at seed 0 with the groove's pin, idle.

Without --windows THE SEAMS ARE THE PLAN'S: every place a part ENTERS (a note after --quiet bars or more of its own
silence, or its first) or LEAVES (its last note before that much silence), read from the notes where they sound. A part
counts when it then plays for --least bars or more (a single stroke is not an entry); seams within --least bars of
each other are one seam. Each stretch between seams is printed with its bars, its time, its loudness (LUFS: BS.1770,
gated, of the finished file), the STEP into it from the stretch before, and who entered and who left at the seam.
With --windows the stretches are yours (bars from 1, as `chirp render --from/--to`; a stretch that starts where the
one before ends has a step), and the plan's entries and exits within a bar of each start are named beside it.

Under the table: where it steps up 1 dB or more, and its loudest stretch: read whether the arrivals you wrote are in
that list. Marked: ENTERS, NO STEP: parts enter, none leave, and the level moves between -1 and +0.5 dB (a seam where
parts change hands is not marked: read its step in the table). A question for an ear before
it is a fault: an arrival can be a change of tone at one level, and a master that holds the level is doing its job.
But a song that adds players four times and never gets louder has nowhere to arrive.
What it cannot see: an arrival made without a new part (the same players, fuller): give those as --windows. Steps
between stretches under about 3 s are rough (the meter gates on 400 ms blocks). Fixed-tempo songs in 4/4 only.
Read-only. Tests: tools/tests/test_seams.py.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLIMB_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import levels  # noqa: E402
import likeness as L  # noqa: E402
import notechk  # noqa: E402
import wincut  # noqa: E402

BEATS = 4.0
STEP_DB = 0.5          # parts enter and the level rises less than this ...
DROP_DB = -1.0         # ... and does not fall further than this (then the others thinned out: another matter): ENTERS, NO STEP
UP_DB = 1.0            # a step up of this much is listed under the table


def flat(s):
    """Whether a stretch is one that parts ENTER (and none leave) with no step."""
    return bool(s["enter"]) and not s["leave"] and s["step"] is not None and DROP_DB <= s["step"] < STEP_DB


def names(canon):
    """Every named track with notes, at any depth, in the song's order."""
    out, stack = [], list(canon.get("tracks") or [])
    while stack:
        t = stack.pop(0)
        if isinstance(t, dict):
            stack = list(t.get("tracks") or []) + stack
            if t.get("name") and t.get("notes") and not t.get("mute"):
                out.append(t["name"])
    return out


def runs(canon, quiet_beats, least_beats):
    """{track: [(first beat, last beat)]}: the stretches a part plays through, a gap of quiet_beats or more ending one;
    stretches shorter than least_beats (a stroke, a fill) are left out."""
    out = {}
    for name in names(canon):
        try:
            notes = notechk.track_notes(canon, name) or []
        except SystemExit:
            continue
        spans = sorted((float(n.get("at") or 0), float(n.get("at") or 0) + float(n.get("len") or 0)) for n in notes)
        got, cur = [], None
        for a, b in spans:
            if cur is None or a - cur[1] >= quiet_beats:
                if cur and cur[1] - cur[0] >= least_beats:
                    got.append(tuple(cur))
                cur = [a, b]
            else:
                cur[1] = max(cur[1], b)
        if cur and cur[1] - cur[0] >= least_beats:
            got.append(tuple(cur))
        if got:
            out[name] = got
    return out


def seams(played, least_beats):
    """[(beat, [who enters], [who leaves])] in order: entries at the bar a part's stretch starts in (a pickup of under a
    beat belongs to the next bar), exits at the bar line after its last note; seams within least_beats are one."""
    at = {}
    for name, spans in played.items():
        for a, b in spans:
            start = (a // BEATS + (1 if a % BEATS > BEATS - 1 else 0)) * BEATS
            end = -(-b // BEATS) * BEATS
            at.setdefault(start, ([], []))[0].append(name)
            at.setdefault(end, ([], []))[1].append(name)
    out = []
    for beat in sorted(at):
        ins, outs = at[beat]
        if out and beat - out[-1][0] < least_beats:
            out[-1][1].extend(ins)
            out[-1][2].extend(outs)
        else:
            out.append((beat, list(ins), list(outs)))
    return out


def lufs(x, sr, s0, s1):
    """The loudness of s0..s1 seconds of a render (integrated, gated), or None when there is under 0.4 s of it."""
    seg = x[int(round(s0 * sr)):int(round(s1 * sr))]
    if len(seg) < 0.4 * sr:
        return None
    return round(levels.loudness(seg, sr)[0], 1)


def table(stretches):
    """The lines for [{bars, time, lufs, step, enter, leave, label}], and the ENTERS, NO STEP marks."""
    def t(s):
        return f"{int(s // 60)}:{int(s % 60):02d}"
    out = [f"  {'bars':>11s}  {'time':>11s}  {'LUFS':>6s}  {'step':>5s}   at the seam"]
    for s in stretches:
        who = "; ".join(x for x in (("ENTER " + ", ".join(s["enter"][:8]) + (f" +{len(s['enter']) - 8}" if len(s["enter"]) > 8 else ""))
                                    if s["enter"] else "",
                                    ("LEAVE " + ", ".join(s["leave"][:8]) + (f" +{len(s['leave']) - 8}" if len(s["leave"]) > 8 else ""))
                                    if s["leave"] else "") if x)
        out.append(f"  {s['bars'][0]:>5.5g}-{s['bars'][1]:<5.5g}  {t(s['time'][0]):>5s}-{t(s['time'][1]):<5s}  "
                   f"{'-' if s['lufs'] is None else format(s['lufs'], '.1f'):>6s}  "
                   f"{'' if s['step'] is None else format(s['step'], '+.1f'):>5s}   "
                   + (f"{s['label']}: " if s.get("label") else "") + who + ("   ENTERS, NO STEP" if flat(s) else ""))
    ups = [s for s in stretches if s["step"] is not None and s["step"] >= UP_DB]
    heard = [s for s in stretches if s["lufs"] is not None]
    if heard:
        top = max(heard, key=lambda s: s["lufs"])
        out.append("  it steps up 1 dB or more " + ("at bar " + ", ".join(f"{s['bars'][0]:g} ({s['step']:+.1f})" for s in ups) if ups
                                                    else "nowhere")
                   + f"; its loudest stretch is {top['bars'][0]:g}-{top['bars'][1]:g} ({top['lufs']:.1f} LUFS)")
    flats = [s for s in stretches if flat(s)]
    if flats:
        out.append(f"  ENTERS, NO STEP at bar {', '.join(format(s['bars'][0], 'g') for s in flats)}: parts come in and the finished "
                   f"file rises less than {STEP_DB:g} dB. A question for an ear: an arrival can be tone at one level; a song that "
                   "adds players and never gets louder has nowhere to arrive")
    return out


def read(canon, x, sr, windows=None, least=2.0, quiet=4.0):
    """The stretches of a song: the plan's own (windows None) or the given ones."""
    tempo = canon.get("tempo", 120.0)
    if not isinstance(tempo, (int, float)) or isinstance(tempo, bool) or tempo <= 0 or \
            str(canon.get("meter") or "4/4").replace(" ", "") != "4/4":
        raise SystemExit("seams: only fixed-tempo songs in 4/4 are read")
    beat = 60.0 / tempo
    dur = len(x) / sr
    played = runs(canon, quiet * BEATS, least * BEATS)
    found = seams(played, least * BEATS)
    out = []
    if windows:
        secs = wincut.window_seconds(canon, windows)
        if secs is None:
            raise SystemExit("seams: --windows takes FROM-TO[:label] in bars (1-9), beats (0b-32b) or seconds (0s-19.2s)")
        for (s0, s1), win in zip(secs, windows):
            b0, b1 = s0 / beat, s1 / beat
            near = [f for f in found if abs(f[0] - b0) <= BEATS]
            out.append({"bars": [round(b0 / BEATS + 1, 2), round(b1 / BEATS + 1, 2)], "time": [s0, min(s1, dur)],
                        "lufs": lufs(x, sr, s0, s1), "label": win.partition(":")[2],
                        "enter": [n for f in near for n in f[1]], "leave": [n for f in near for n in f[2]],
                        "adjacent": bool(out) and abs(out[-1]["time"][1] - s0) < 1e-6})
    else:
        cuts = [f for f in found if 0 < f[0] * beat < dur - 0.4]
        edges = [0.0] + [f[0] for f in cuts] + [dur / beat]
        first = next((f for f in found if f[0] == 0), (0.0, [], []))
        for i, (b0, b1) in enumerate(zip(edges, edges[1:])):
            f = first if i == 0 else cuts[i - 1]
            out.append({"bars": [round(b0 / BEATS + 1, 2), round(b1 / BEATS + 1, 2)], "time": [b0 * beat, b1 * beat],
                        "lufs": lufs(x, sr, b0 * beat, b1 * beat), "label": "", "enter": list(f[1]), "leave": list(f[2]),
                        "adjacent": i > 0})
    for i, s in enumerate(out):
        adjacent = s.pop("adjacent")
        prev = out[i - 1] if i and adjacent else None
        s["step"] = round(s["lufs"] - prev["lufs"], 1) if prev and None not in (s["lufs"], prev["lufs"]) else None
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("id")
    ap.add_argument("--wav", help="the finished (mastered) render; else the song is rendered at seed 0")
    ap.add_argument("--windows", nargs="+", help="FROM-TO[:label] ...: your own stretches instead of the plan's seams")
    ap.add_argument("--least", type=float, default=2.0, help="bars a part must play for to count, and between two seams")
    ap.add_argument("--quiet", type=float, default=4.0, help="bars of its own silence after which a part has LEFT")
    ap.add_argument("--pin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    song = a.id if os.path.exists(a.id) else os.path.join(ROOT, "songs", f"{a.id}.yaml")
    if not os.path.exists(song):
        raise SystemExit(f"seams: no song {a.id}")
    pin = a.pin or open(os.path.join(HERE, "groove-pin")).read().strip()
    r = subprocess.run([pin, "plan", "-f", song, "--json"], capture_output=True, text=True)
    try:
        canon = json.loads(r.stdout)
        canon = (canon.get("data") or canon)["canonical"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"seams: {os.path.basename(song)} did not plan: {(r.stderr or r.stdout).strip()[-300:]}") from None
    tmp, wav = None, a.wav
    try:
        if not wav:
            tmp = tempfile.mkdtemp(prefix="seams-", dir="/tmp/lt" if os.path.isdir("/tmp/lt") else None)
            wav = os.path.join(tmp, "seams.wav")
            rr = subprocess.run(["nice", "-n", "15", pin, "render", "-f", song, "--seed", "0", "-o", wav], capture_output=True,
                                text=True, env={k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"})
            if rr.returncode:
                raise SystemExit(f"seams: the song did not render: {rr.stderr.strip()[-300:]}")
        x = L.load(wav)
        got = read(canon, x, L.SR, a.windows, a.least, a.quiet)
    finally:
        if tmp:
            import shutil
            shutil.rmtree(tmp, True)
    if a.json:
        print(json.dumps({"song": song, "wav": a.wav, "stretches": got}))
        return 0
    print(f"{os.path.basename(song)}, {os.path.basename(a.wav) if a.wav else 'rendered at seed 0'}: {len(got)} stretches "
          + ("(yours)" if a.windows else f"between the plan's seams (a part enters or leaves; --least {a.least:g} bars, "
             f"--quiet {a.quiet:g})") + "; LUFS of the finished file, and the step into each")
    print("\n".join(table(got)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
