#!/usr/bin/env python3
"""songmap: what a song gives its picture to work with (chirp-video, 10 Nov).

A programme (vis/<id>.yaml) is co-built with its song: scenes on bars, bodies on tracks and
notes, the story on automation lanes. This prints the song's side of that, from the engine's
own plan (`chirp plan --json`) and note list (`chirp render -o x.mid`):

  - length, tempo map, metre, and where the bars fall (bar -> m:ss);
  - every track: notes, when it plays (spans, in bars and m:ss), pitch range, its cycle
    (the commonest gap between onsets, in beats), pan;
  - every automation lane: where it moves (bar, m:ss, value);
  - sung tracks: their syllables.

    python3 tools/songmap.py chirpers9-t1                 # the whole map
    python3 tools/songmap.py chirpers9-t1 --tracks seed   # only tracks whose name contains "seed"
    python3 tools/songmap.py chirpers9-t1 --lanes         # only the lanes
    python3 tools/songmap.py chirpers9-t1 --json          # everything, for scripts

Names here are what a programme reads: `track.NAME.hit|level|key|gate`, `lane.NAME`. Bars are
counted as a programme writes them (`at: 32bar` and keys `[[16bar, 0], [24bar, 1]]` are after
that many bars, so the song starts at 0bar).
"""
import argparse, collections, glob, json, os, struct, subprocess, sys, tempfile

CFG = os.path.expanduser("~/.config/chirp")


def chirp_bin():
    pins = sorted(glob.glob("/tmp/lt/pins/chirp-*"), key=os.path.getmtime)
    return pins[-1] if pins else "chirp"


def read_midi(path):
    """-> (ppq, tempo [(tick, us per beat)], metre [(tick, num, den)], {track name: [(on, off, key, vel)]})"""
    d = open(path, "rb").read()
    assert d[:4] == b"MThd"
    _, _, ntr, ppq = struct.unpack(">IHHH", d[4:14])
    pos, tempo, metre, tracks = 14, [], [], collections.OrderedDict()
    for _ in range(ntr):
        assert d[pos:pos + 4] == b"MTrk"
        n = struct.unpack(">I", d[pos + 4:pos + 8])[0]
        p, end, tick, run, name, held, notes = pos + 8, pos + 8 + n, 0, 0, None, {}, []
        while p < end:
            dt = 0
            while True:
                b = d[p]; p += 1
                dt = (dt << 7) | (b & 0x7F)
                if b < 0x80:
                    break
            tick += dt
            st = d[p]
            if st == 0xFF:
                kind = d[p + 1]; p += 2
                ln = 0
                while True:
                    b = d[p]; p += 1
                    ln = (ln << 7) | (b & 0x7F)
                    if b < 0x80:
                        break
                body = d[p:p + ln]; p += ln
                if kind == 0x03:
                    name = body.decode("utf8", "replace")
                elif kind == 0x51:
                    tempo.append((tick, int.from_bytes(body, "big")))
                elif kind == 0x58:
                    metre.append((tick, body[0], 2 ** body[1]))
                continue
            if st in (0xF0, 0xF7):
                p += 1
                ln = 0
                while True:
                    b = d[p]; p += 1
                    ln = (ln << 7) | (b & 0x7F)
                    if b < 0x80:
                        break
                p += ln
                continue
            if st & 0x80:
                run = st; p += 1
            hi = run & 0xF0
            if hi in (0xC0, 0xD0):
                p += 1
                continue
            a, b2 = d[p], d[p + 1]; p += 2
            if hi == 0x90 and b2 > 0:
                held.setdefault(a, []).append((tick, b2))
            elif hi == 0x80 or (hi == 0x90 and b2 == 0):
                if held.get(a):
                    on, vel = held[a].pop(0)
                    notes.append((on, tick, a, vel))
        if notes:
            tracks.setdefault(name or f"track{len(tracks)}", []).extend(sorted(notes))
        pos = end
    return ppq, sorted(tempo) or [(0, 500000)], sorted(metre) or [(0, 4, 4)], tracks


class Clock:
    """Beats <-> seconds on the song's tempo map; bars on its metre."""

    def __init__(self, ppq, tempo, metre):
        self.pts, t, last_tick, us = [], 0.0, 0, tempo[0][1]
        for tick, u in tempo:
            t += (tick - last_tick) / ppq * us / 1e6
            self.pts.append((tick / ppq, t, u / 1e6))
            last_tick, us = tick, u
        self.bar_beats = metre[0][1] * 4.0 / metre[0][2]

    def sec(self, beat):
        b0, t0, spb = self.pts[0]
        for p in self.pts:
            if p[0] <= beat:
                b0, t0, spb = p
            else:
                break
        return t0 + (beat - b0) * spb

    def bar(self, beat):
        # As a programme writes positions: `8bar` is after eight bars, so the song starts at 0.
        return beat / self.bar_beats


def mmss(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def load(song):
    path = song if os.path.exists(song) else os.path.join(CFG, "songs", song + ".yaml")
    b = chirp_bin()
    cwd = os.path.dirname(os.path.abspath(path))
    r = subprocess.run([b, "plan", "-f", path, "--json"], capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        sys.exit(f"songmap: chirp plan failed: {r.stderr.strip()[-400:]}")
    data = json.loads(r.stdout)["data"]
    with tempfile.TemporaryDirectory() as td:
        mid = os.path.join(td, "s.mid")
        r = subprocess.run([b, "render", "-f", path, "-o", mid], capture_output=True, text=True, cwd=cwd)
        if r.returncode != 0:
            sys.exit(f"songmap: chirp render -o x.mid failed: {r.stderr.strip()[-400:]}")
        ppq, tempo, metre, notes = read_midi(mid)
    return data, ppq, tempo, metre, notes


def beats_of(x):
    """'12.5b' or 12.5 -> beats"""
    if isinstance(x, (int, float)):
        return float(x)
    x = str(x).strip()
    return float(x[:-1]) if x.endswith("b") else float(x)


def build(song):
    data, ppq, tempo, metre, notes = load(song)
    canon = data["canonical"]
    clk = Clock(ppq, tempo, metre)
    out = {"song": song, "seconds": data["seconds"], "bar_beats": clk.bar_beats,
           "tempo": [{"beat": round(b, 2), "at": round(t, 2), "bpm": round(60 / spb, 1)} for b, t, spb in clk.pts],
           "tracks": [], "lanes": []}
    # Collapse the many small steps of a ramp: keep points where the tempo has moved 1 bpm.
    kept, last = [], None
    for p in out["tempo"]:
        if last is None or abs(p["bpm"] - last) >= 1:
            kept.append(p); last = p["bpm"]
    out["tempo"] = kept
    ctracks = canon.get("tracks") or []
    by_name = {t.get("name"): t for t in ctracks if isinstance(t, dict)}
    for name, ns in notes.items():
        on = [n[0] / ppq for n in ns]
        gaps = collections.Counter(round(b - a, 2) for a, b in zip(on, on[1:]) if b - a > 0.01)
        spans, start, prev = [], on[0], ns[0][1] / ppq
        for n in ns[1:]:
            b = n[0] / ppq
            if b - prev > 2 * clk.bar_beats:  # silent for two bars: a new span
                spans.append((start, prev)); start = b
            prev = max(prev, n[1] / ppq)
        spans.append((start, prev))
        t = by_name.get(name, {})
        pan = t.get("pan")
        out["tracks"].append({
            "name": name, "notes": len(ns), "keys": [min(n[2] for n in ns), max(n[2] for n in ns)],
            "cycle_beats": gaps.most_common(1)[0][0] if gaps else None,
            "pan": pan if isinstance(pan, (int, float)) else (pan.get("value") if isinstance(pan, dict) else None),
            "spans": [{"bars": [round(clk.bar(a), 1), round(clk.bar(b), 1)], "at": [round(clk.sec(a), 1), round(clk.sec(b), 1)]} for a, b in spans],
            "sung": [n.get("ph") for n in (t.get("notes") or []) if isinstance(n, dict) and n.get("ph")] or None,
        })
    seen = set()

    def lanes_of(owner, obj):
        for lname, lane in ((obj or {}).get("auto") or {}).items():
            pts = [(beats_of(p[0]), float(p[1])) for p in (lane.get("points") or [])]
            key = (lname, tuple(pts))
            if not pts or key in seen:
                continue
            first = lname not in {k[0] for k in seen}
            seen.add(key)
            # Every corner of the lane: a point is dropped only inside a run of equal values
            # (the run's first and last are kept, so a hold and the ramp after it both show).
            moves = []
            for i, (b, v) in enumerate(pts):
                inside = 0 < i < len(pts) - 1 and abs(pts[i - 1][1] - v) < 1e-6 and abs(pts[i + 1][1] - v) < 1e-6
                if not inside:
                    moves.append({"bar": round(clk.bar(b), 1), "at": round(clk.sec(b), 1), "value": round(v, 3)})
            out["lanes"].append({"name": lname, "on": owner, "read": first, "lo": min(v for _, v in pts),
                                 "hi": max(v for _, v in pts), "moves": moves})

    for t in ctracks:
        if isinstance(t, dict):
            lanes_of(t.get("name"), t)
    lanes_of("master", canon.get("master") if isinstance(canon.get("master"), dict) else {})
    for bname, bus in (canon.get("buses") or {}).items():
        if isinstance(bus, dict):
            lanes_of("bus " + bname, bus)
    return out, clk


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song")
    ap.add_argument("--tracks", help="only tracks whose name contains this")
    ap.add_argument("--lanes", action="store_true", help="only the lanes")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m, clk = build(a.song)
    if a.json:
        print(json.dumps(m))
        return
    print(f"{m['song']}: {mmss(m['seconds'])}, {m['bar_beats']:g} beats a bar")
    print("tempo: " + ", ".join(f"{p['bpm']:g} from {mmss(p['at'])}" for p in m["tempo"]))
    last_bar = int(max(max(s["bars"][1] for s in t["spans"]) for t in m["tracks"]))
    print("bars (as a programme writes them: `8bar` is after eight bars):")
    print("  " + "  ".join(f"{b}bar={mmss(clk.sec(b * m['bar_beats']))}" for b in range(0, last_bar + 1, 8)))
    if not a.lanes:
        print(f"\ntracks ({len(m['tracks'])}): name, notes, keys, cycle (beats), pan, then when it plays (bars, m:ss)")
        for t in m["tracks"]:
            if a.tracks and a.tracks not in t["name"]:
                continue
            spans = "; ".join(f"{s['bars'][0]:g}-{s['bars'][1]:g} ({mmss(s['at'][0])}-{mmss(s['at'][1])})" for s in t["spans"][:8])
            more = f"; +{len(t['spans']) - 8} more" if len(t["spans"]) > 8 else ""
            pan = "" if t["pan"] is None else f" pan {t['pan']:+g}"
            cyc = "" if t["cycle_beats"] is None else f" cycle {t['cycle_beats']:g}"
            print(f"  {t['name']:<14} {t['notes']:>4} notes  keys {t['keys'][0]}-{t['keys'][1]}{cyc}{pan}\n      {spans}{more}")
            if t["sung"]:
                print("      sung: " + " | ".join(t["sung"][:14]) + (" ..." if len(t["sung"]) > 14 else ""))
    if not a.tracks:
        print(f"\nlanes ({len(m['lanes'])}): lane.NAME reads the first of a name; its corners (bar m:ss value), straight lines between")
        for l in m["lanes"]:
            mv = l["moves"]
            shown = mv if len(mv) <= 10 else mv[:5] + [None] + mv[-4:]
            txt = "  ".join("..." if x is None else f"{x['bar']:g} {mmss(x['at'])} {x['value']:g}" for x in shown)
            tag = "" if l["read"] else "  (shadowed: another lane of this name comes first)"
            print(f"  {l['name']:<12} on {l['on']:<12} {l['lo']:g}..{l['hi']:g}, {len(mv)} corners{tag}\n      {txt}")


if __name__ == "__main__":
    main()
