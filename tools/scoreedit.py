#!/usr/bin/env python3
"""scoreedit: same-count note substitutions INSIDE a time window of a song's tracks, in place (chirper-two).

  scoreedit.py SONG.yaml OUT.yaml TRACK[,TRACK...] T0 T1 '[["C3","C4"],["C#3","C#4"]]'

Edits the published song file directly (no map regeneration, no replacement tracks), so a candidate compares
against the CURRENT version itself. Token start times come from the song's own tempo (a number or the list of
{at: "Nb", bpm} points; seconds assumed constant between points). A token whose START lies in [T0, T1) has its note
names substituted element-wise in chords (C3 -> C4 inside "C3,F3"); its duration/velocity/marks are kept. A
repeat group `[...]xN` that holds an edited token is expanded in place first (same notes, same order). Note count
and order do not change, so the track's later random draws stay where they were; only the edited voices change
pitch (and rekey their own DSP seed). Check with ab.ir_diff before rendering. Ties `_` and rests `R` are skipped.
"""
import json
import re
import sys

NOTE = re.compile(r"^([A-G](?:#|b)?-?\d)$")



def is_track_line(line, track):
    """A song file's flow-mapping line for TRACK, whatever its key order (rngsafe and drumtrans write
    {patch: ..., name: ...}); the original matched only lines starting '- {name: ...'."""
    return line.lstrip().startswith("- {") and re.search(r'(?:\{|, )name: "' + re.escape(track) + '"', line) is not None

def tempo_points(song_text):
    m = re.search(r"^tempo:\s*(.+)$", song_text, re.M)
    v = m.group(1).strip()
    if v.startswith("["):
        pts = json.loads(v)
        return [(float(str(p["at"]).rstrip("b")), float(p["bpm"])) for p in pts]
    return [(0.0, float(v))]


def beat_to_sec(beat, pts):
    s, prev_b, prev_bpm = 0.0, 0.0, pts[0][1]
    for b, bpm in pts:
        if b > beat:
            break
        s += (b - prev_b) * 60 / prev_bpm
        prev_b, prev_bpm = b, bpm
    return s + (beat - prev_b) * 60 / prev_bpm


def tokens(score):
    """Split into a flat list of items: ('bar',) separators, ('grp', [items], n) groups, ('tok', text)."""
    out, i = [], 0
    while i < len(score):
        c = score[i]
        if c.isspace():
            i += 1
        elif c == "|":
            out.append(("bar", "|"))
            i += 1
        elif c == "[":
            depth, j = 1, i + 1
            while depth:
                depth += {"[": 1, "]": -1}.get(score[j], 0)
                j += 1
            m = re.match(r"x(\d+)", score[j:])
            n = int(m.group(1)) if m else 1
            out.append(("grp", tokens(score[i + 1:j - 1]), n))
            i = j + (len(m.group(0)) if m else 0)
        else:
            j = i
            while j < len(score) and not score[j].isspace() and score[j] not in "|[":
                j += 1
            out.append(("tok", score[i:j]))
            i = j
    return out


def dur_beats(tok):
    m = re.search(r"/([0-9.]+)b", tok)
    return float(m.group(1)) if m else 0.0


def render(items):
    parts = []
    for it in items:
        if it[0] == "bar":
            parts.append("|")
        elif it[0] == "tok":
            parts.append(it[1])
        else:
            parts.append("[" + render(it[1]) + f"]x{it[2]}")
    return " ".join(parts)


def edit(items, pos, pts, t0, t1, sub, count):
    out = []
    for it in items:
        if it[0] == "bar":
            out.append(it)
        elif it[0] == "tok":
            tok = it[1]
            start = beat_to_sec(pos[0], pts)
            head, _, rest = tok.partition("/")
            if t0 <= start < t1 and head not in ("R", "_") and not head.startswith("R") and "=" not in head:
                els = head.split(",")
                new = [sub.get(e, e) for e in els]
                if new != els:
                    count[0] += sum(1 for a, b in zip(els, new) if a != b)
                    tok = ",".join(new) + ("/" + rest if rest or "/" in tok else "")
            out.append(("tok", tok))
            pos[0] += dur_beats(it[1]) if "=" not in it[1].split("/")[0] else 0.0
        else:
            body, n = it[1], it[2]
            # trial pass: does any copy hold an edited token?
            trial_pos, trial_cnt, copies = [pos[0]], [0], []
            for _ in range(n):
                copies.append(edit(body, trial_pos, pts, t0, t1, sub, trial_cnt))
            if trial_cnt[0] == 0:
                out.append(it)
                pos[0] = trial_pos[0]
            else:
                for c in copies:
                    out.extend(c)
                count[0] += trial_cnt[0]
                pos[0] = trial_pos[0]
    return out


def main():
    song, outp, tracks, t0, t1, subj = sys.argv[1:7]
    t0, t1, sub = float(t0), float(t1), dict(json.loads(subj))
    text = open(song).read()
    pts = tempo_points(text)
    lines = text.split("\n")
    for tr in tracks.split(","):
        idx = [i for i, ln in enumerate(lines) if is_track_line(ln, tr)]
        assert len(idx) == 1, (tr, idx)
        ln = lines[idx[0]]
        a = ln.index('score: "') + len('score: "')
        b = ln.index('"', a)
        items = tokens(ln[a:b])
        cnt = [0]
        new = edit(items, [0.0], pts, t0, t1, sub, cnt)
        lines[idx[0]] = ln[:a] + render(new) + ln[b:]
        print(f"{tr}: {cnt[0]} note(s) substituted in {t0}-{t1} s", file=sys.stderr)
    open(outp, "w").write("\n".join(lines))


if __name__ == "__main__":
    main()
