#!/usr/bin/env python3
"""splitpart: move one time range of a track onto a second patch (a per-section instrument; chirper-zero's request).

  splitpart.py SONG TRACK --from A --to B --patch NEWPATCH [--name NEWNAME] -o OUT [--no-check]
      A, B: seconds (60, 60s) or beats (120b) on the song's clock; NEWNAME defaults to TRACK-alt.

The notes of TRACK that START in [A, B) move to a new track NEWNAME (a copy of TRACK's settings with patch
NEWPATCH, inserted right after it); TRACK keeps everything else, with rests where the moved notes were. Works on
JSON songs and sources (tools/ID-source.json) and on the flow YAML tab2song writes, with tracks given either as
`notes` lists (`at` in seconds or beats) or as generated `score` strings (`PITCH/Nb@V^marks`, `R/Nb`, `_/Nb` holds,
`|`). A hold follows the note it extends. Anything else in a score is refused.

The split is proven before anything is written: chirp plans the original and the split song with NEWNAME still on
TRACK's patch and humanization off on both tracks (`play.humanize=null`), and the voices (start, end, key, velocity,
release, expression) must be identical as multisets — so a score token that leans on a latched octave or velocity,
or anything else the split might change, is caught. Then the real output (with NEWPATCH) is planned once and
written atomically in the input's format. Humanization is randomness drawn in sequence per track, so a humanized
patch's timing and velocity draws re-roll on the two split tracks (`play.humanize.stable: true` keys them to events).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402
import songfmt  # noqa: E402

TOK = re.compile(r"^(?P<head>[^/\s]+)/(?P<dur>\d+(?:\.\d+)?|\.\d+)b(?P<tail>(@[\d.]+)?(\^\S*)?)$")
RESTS = {"R", "r", ".", "-"}
EPS = 1e-9


class Refused(ValueError):
    pass


def tempo_segments(tempo):
    """[(start_beat, bpm)] from a number or a tempo map of {at: 'Nb', bpm} entries (piecewise constant)."""
    if isinstance(tempo, (int, float)):
        return [(0.0, float(tempo))]
    if isinstance(tempo, list) and tempo:
        segs = []
        for e in tempo:
            at = str(e.get("at", ""))
            if not at.endswith("b") or set(e) - {"at", "bpm", "meter"}:
                raise Refused(f"tempo map entry {e} (only {{at: 'Nb', bpm, meter}} is supported)")
            segs.append((float(at[:-1]), float(e["bpm"])))
        return sorted(segs)
    raise Refused(f"tempo {tempo!r}")


def to_beats(pos, segs):
    """A position '60s' / 60 (seconds) or '120b' (beats) → beats."""
    s = str(pos).strip()
    if s.endswith("b"):
        return float(s[:-1])
    sec = float(s.rstrip("s"))
    beat, t = 0.0, 0.0
    for i, (b0, bpm) in enumerate(segs):
        b1 = segs[i + 1][0] if i + 1 < len(segs) else float("inf")
        span = (b1 - b0) * 60 / bpm
        if sec <= t + span:
            return b0 + (sec - t) * bpm / 60
        t += span
        beat = b1
    return beat


def split_score(score, a, b):
    """(kept score, moved score): note tokens starting in [a, b) beats move; each side gets rests for the other's."""
    keep, move, pos, last, moved = [], [], 0.0, None, 0
    for tok in score.split():
        if tok == "|":
            keep.append(tok), move.append(tok)
            continue
        m = TOK.match(tok)
        if not m:
            raise Refused(f"score token {tok!r} (only PITCH/Nb@V^marks, R/Nb, _/Nb and | are supported)")
        head, dur = m.group("head"), m.group("dur")
        rest = f"R/{dur}b"
        if head in RESTS:
            keep.append(tok), move.append(tok)
            last = None
        elif head == "_":
            if last == "move":
                move.append(tok), keep.append(rest)
            elif last == "keep":
                keep.append(tok), move.append(rest)
            else:
                keep.append(tok), move.append(tok)
        elif a - EPS <= pos < b - EPS:
            move.append(tok), keep.append(rest)
            last, moved = "move", moved + 1
        else:
            keep.append(tok), move.append(rest)
            last = "keep"
        pos += float(dur)
    return " ".join(keep), " ".join(move), moved


def split_notes(notes, a, b, segs):
    keep, move = [], []
    for n in notes:
        at = to_beats(n["at"], segs) if isinstance(n.get("at"), (str, int, float)) else None
        if at is None:
            raise Refused(f"note without an `at`: {n}")
        (move if a - EPS <= at < b - EPS else keep).append(n)
    return keep, move


def split(doc, track, a, b, patch, name):
    """A new song dict with TRACK split; raises Refused. Returns (song, moved count)."""
    tracks = doc.get("tracks")
    if not isinstance(tracks, list):
        raise Refused("the song has no tracks list")
    idx = [i for i, t in enumerate(tracks) if isinstance(t, dict) and t.get("name") == track]
    if len(idx) != 1:
        raise Refused(f"track {track!r} {'not found' if not idx else 'is not unique'} "
                      f"(tracks: {', '.join(str(t.get('name')) for t in tracks if isinstance(t, dict))})")
    if any(isinstance(t, dict) and t.get("name") == name for t in tracks):
        raise Refused(f"a track named {name!r} already exists (--name)")
    segs = tempo_segments(doc.get("tempo", 120))
    ab, bb = to_beats(a, segs), to_beats(b, segs)
    if not bb > ab:
        raise Refused(f"empty range {a}..{b}")
    t = tracks[idx[0]]
    new = json.loads(json.dumps(t))
    new["name"], new["patch"] = name, patch
    if isinstance(t.get("score"), str):
        k, m, moved = split_score(t["score"], ab, bb)
        t2 = dict(t, score=k)
        new["score"] = m
    elif isinstance(t.get("notes"), list):
        k, m = split_notes(t["notes"], ab, bb, segs)
        moved = len(m)
        t2 = dict(t, notes=k)
        new["notes"] = m
    else:
        raise Refused(f"track {track!r} has neither a score string nor a notes list")
    if not moved:
        raise Refused(f"no notes of {track!r} start in {a}..{b}")
    out = dict(doc)
    out["tracks"] = tracks[:idx[0]] + [t2, new] + tracks[idx[0] + 1:]
    return out, moved


def voices(path):
    r = subprocess.run([chirpbin.resolve("chirp"), "--json", "plan", "-f", os.path.abspath(path), "--ir"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    try:
        vs = json.loads(r.stdout)["data"]["ir"]["voices"]
    except (ValueError, KeyError, TypeError):
        raise Refused(f"chirp plan failed on {path}: {(r.stderr or r.stdout).strip()[-300:]}")
    return Counter((v["start"], v["end"], v["key"], round(v["vel"], 6), v["release"], json.dumps(v.get("expr"), sort_keys=True))
                   for v in vs)


def dehumanize(doc, names):
    """A copy of doc with humanization off on the named tracks (their patch strings get play.humanize=null)."""
    out = json.loads(json.dumps(doc))
    for t in out["tracks"]:
        if isinstance(t, dict) and t.get("name") in names:
            if isinstance(t.get("patch"), str):
                t["patch"] = t["patch"] + " play.humanize=null"
            elif isinstance(t.get("patch"), dict):
                t["patch"].setdefault("play", {})["humanize"] = None
    return out


def planned_voices(doc, like_text, like_path, d):
    fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(like_path)[1], prefix=".splitpart-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(render_text(doc, like_text, like_path))
        return voices(tmp)
    finally:
        os.remove(tmp)


def render_text(doc, like_text, like_path):
    if like_text.lstrip().startswith("{"):
        style, nl = songfmt.json_style(like_path)
        return json.dumps(doc, **style) + nl
    return songfmt.dump_yaml(doc)


def main(argv):
    a = list(argv)

    def opt(flag, default=None):
        if flag in a:
            i = a.index(flag)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return default

    check = "--no-check" not in a
    a = [x for x in a if x != "--no-check"]
    t0, t1, patch, out, name = opt("--from"), opt("--to"), opt("--patch"), opt("-o"), opt("--name")
    if len(a) != 2 or None in (t0, t1, patch, out):
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    song, track = a
    name = name or f"{track}-alt"
    text = songfmt.read(song)
    try:
        doc = songfmt.load(song)
        result, moved = split(doc, track, t0, t1, patch, name)
        d = os.path.dirname(os.path.abspath(out)) or "."
        if check:
            orig_patch = next(t for t in doc["tracks"] if t.get("name") == track).get("patch")
            same, _ = split(doc, track, t0, t1, orig_patch, name)
            if (planned_voices(dehumanize(doc, {track}), text, song, d)
                    != planned_voices(dehumanize(same, {track, name}), text, song, d)):
                raise Refused("the split changes the voices (a score token leans on a latched octave or velocity, "
                              "or the range cuts something the split cannot move); nothing written")
        fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(song)[1], prefix=".splitpart-", dir=d)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(render_text(result, text, song))
            if check:
                voices(tmp)   # the real output (NEWPATCH) must plan
            os.replace(tmp, out)
            tmp = None
        finally:
            if tmp and os.path.exists(tmp):
                os.remove(tmp)
    except (Refused, songfmt.Unsupported) as e:
        raise SystemExit(f"splitpart: {e}")
    print(f"moved {moved} note(s) of {track} in {t0}..{t1} to {name} ({patch}) -> {out}"
          + (" (voices proven identical with the original patch)" if check else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
