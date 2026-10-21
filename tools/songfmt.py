#!/usr/bin/env python3
"""songfmt: move a song between the flow YAML the tools write and its JSON source, exactly (chirper-zero's request).

  songfmt.py json SONG.yaml -o SOURCE.json [--like SOURCE.json] [--no-check]
  songfmt.py yaml SOURCE.json -o SONG.yaml [--like SONG.yaml] [--no-check]
  songfmt.py same A B                      # do two files resolve to the same song? (exit 0 yes, 1 no)
  songfmt.py notes SONG TRACK -o OUT [--no-check]   # a score-string track as a native notes list

Songs built from a JSON source (tools/ID-source.json) are rendered from their flow-YAML form (songs/ID.yaml: one
`key: <JSON>` line per top-level field, one `- {key: <JSON>, …}` line per track — what tab2song writes). songride,
widthfit, stemhats and sectionlevel edit that YAML (songride re-appends `master:` after the tracks), so after a
master or part step the source must be regenerated from the YAML. `json` does that: the output keeps --like's
top-level key order (new keys at the end) and its exact formatting (indent, ASCII escaping, trailing newline, found by
reproducing --like byte for byte). `yaml` goes the other way in tab2song's layout (or, when --like is a native JSON song saved as .yaml,
in its JSON formatting).

`notes` rewrites one track's generated score string (PITCH/Nb@V^marks, chords, kit pieces, R rests, _ holds, |)
as a `notes` list — at and len in beats (tempo maps still apply), pitch as MIDI (Hz as fractional MIDI) or the kit
piece, velocity (a token without @V takes the velocity chirp actually plays), ^NAME[=v] as expr, ^NAME=a>b as
expr + expr_end, ^gate as the note's gate — so the notes-list tools (stemfix, splitpart, griddrums --replace) work on
it. Ratchets, flams, drags and other syntax are refused. Proven before writing: with humanization off the converted
song's voices equal the original's (catches a latched octave or anything else the rewrite would change).

It parses only that flow form (no PyYAML here): top-level `key: value` lines whose value is JSON or a bare scalar,
and a `tracks:` block of single-line flow mappings with bare keys. Anything else is refused, never guessed. Before
writing, `chirp plan` resolves the input and the output (the groove pin unless $CHIRP is set) and the conversion
is refused unless both give the same plan hash (--no-check skips this; not recommended). Writes are atomic.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chirpbin  # noqa: E402

KEY = re.compile(r"^([A-Za-z_][\w.-]*):(?:\s+(.*?))?\s*$")
ITEM = re.compile(r"^\s+-\s+(.*?)\s*$")
DEC = json.JSONDecoder()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class Unsupported(ValueError):
    pass


def scalar(text):
    """A YAML flow scalar: JSON when it parses, else YAML's plain forms (numbers, booleans, null), else a string."""
    try:
        return json.loads(text)
    except ValueError:
        pass
    low = text.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"[-+]?\d+", text):
        return int(text)
    if re.fullmatch(r"[-+]?(\d+\.\d*|\.\d+|\d+)([eE][-+]?\d+)?", text):
        return float(text)
    if text[:1] in "'\"[{&*!|>%@`" or ": " in text or " #" in text:
        raise Unsupported(f"not a plain YAML scalar: {text[:60]!r}")
    return text


def flow_value(s, i, where):
    """One YAML flow value at s[i:] → (value, end): JSON strings and numbers, nested {…}/[…] with bare or quoted keys,
    and plain scalars up to the next , } or ]."""
    n = len(s)
    while i < n and s[i] in " \t":
        i += 1
    if i >= n:
        raise Unsupported(f"{where}: a value is missing")
    c = s[i]
    if c == '"':
        return DEC.raw_decode(s, i)
    if c in "{[":
        close, out = ("}", {}) if c == "{" else ("]", [])
        i += 1
        while True:
            while i < n and s[i] in " \t":
                i += 1
            if i < n and s[i] == close:
                return out, i + 1
            if c == "{":
                if i < n and s[i] == '"':
                    k, i = DEC.raw_decode(s, i)
                else:
                    m = re.match(r"[A-Za-z_][\w.-]*", s[i:])
                    if not m:
                        raise Unsupported(f"{where}: cannot read a key at {s[i:i + 30]!r}")
                    k, i = m.group(0), i + m.end()
                while i < n and s[i] in " \t":
                    i += 1
                if i >= n or s[i] != ":":
                    raise Unsupported(f"{where}: expected ':' after key {k!r}")
                v, i = flow_value(s, i + 1, where)
                if k in out:
                    raise Unsupported(f"{where}: duplicate key {k!r}")
                out[k] = v
            else:
                v, i = flow_value(s, i, where)
                out.append(v)
            while i < n and s[i] in " \t":
                i += 1
            if i < n and s[i] == ",":
                i += 1
            elif not (i < n and s[i] == close):
                raise Unsupported(f"{where}: expected ',' or {close!r} at {s[i:i + 30]!r}")
    m = re.match(r"[^,}\]]*", s[i:])
    return scalar(m.group(0).strip()), i + m.end()


def flow_whole(text, where):
    v, i = flow_value(text, 0, where)
    if text[i:].strip():
        raise Unsupported(f"{where}: unexpected text after the value: {text[i:i + 30]!r}")
    return v


def flow_map(s, where):
    """A track: `{key: value, …}` on one line → dict."""
    s = s.strip()
    if not s.startswith("{"):
        raise Unsupported(f"{where}: a track must be one flow mapping {{…}} on one line")
    return flow_whole(s, where)


def parse_yaml(text, name="song"):
    doc, block = {}, None
    for no, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        where = f"{name}:{no}"
        m = ITEM.match(line)
        if m and block is not None:
            body = m.group(1)
            doc[block].append(json.loads(body) if body.startswith('{"') else flow_map(body, where))
            continue
        if line[:1] in " \t-":
            raise Unsupported(f"{where}: only top-level `key: value` lines and a list of one-line flow mappings")
        m = KEY.match(line)
        if not m:
            raise Unsupported(f"{where}: cannot read {line[:60]!r}")
        k, rest = m.group(1), m.group(2)
        if k in doc:
            raise Unsupported(f"{where}: duplicate top-level key {k!r}")
        if rest is None or rest == "":
            doc[k], block = [], k
        else:
            doc[k], block = (flow_whole(rest, where) if rest[:1] in '{["' else scalar(rest)), None
    return doc


def load(path):
    text = read(path)
    if text.lstrip().startswith("{"):
        return json.loads(text)
    return parse_yaml(text, os.path.basename(path))


def ordered(doc, like):
    """doc's top-level keys in like's order, then doc's new keys in their own order (removed keys stay removed)."""
    keys = [k for k in like if k in doc] + [k for k in doc if k not in like]
    return {k: doc[k] for k in keys}


def json_style(path):
    """json.dumps kwargs (and trailing newline) that reproduce the file at path byte for byte, else indent 2."""
    text = read(path)
    doc = json.loads(text)
    for indent in (2, 4, 1, None, "\t"):
        for ascii_ in (False, True):
            for seps in ((",", ": "), (", ", ": "), (",", ":")):
                if indent is not None and seps == (", ", ": "):
                    continue
                body = json.dumps(doc, indent=indent, ensure_ascii=ascii_, separators=seps)
                for nl in ("\n", ""):
                    if body + nl == text:
                        return {"indent": indent, "ensure_ascii": ascii_, "separators": seps}, nl
    print(f"songfmt: {path}'s formatting is not a plain json.dumps; writing indent 2", file=sys.stderr)
    return {"indent": 2, "ensure_ascii": False}, "\n"


def dump_yaml(doc):
    """tab2song's layout: one `key: JSON` line per field, `tracks:` then one flow mapping per track (in doc order)."""
    out = []
    for k, v in doc.items():
        if k == "tracks" and isinstance(v, list) and all(isinstance(t, dict) for t in v):
            out.append("tracks:")
            for t in v:
                out.append("  - {" + ", ".join(f"{tk}: {json.dumps(tv, ensure_ascii=False)}" for tk, tv in t.items()) + "}")
        else:
            out.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(out) + "\n"


def plan_hash(path):
    r = subprocess.run([chirpbin.resolve("chirp"), "--json", "plan", "-f", os.path.abspath(path)], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL, cwd=os.path.dirname(os.path.abspath(path)))
    try:
        d = json.loads(r.stdout)
        return d["data"]["plan_hash"]
    except (ValueError, KeyError, TypeError):
        raise SystemExit(f"songfmt: chirp plan failed on {path}: {(r.stderr or r.stdout).strip()[-300:]}")


def write_checked(src, text, out, check, suffix):
    d = os.path.dirname(os.path.abspath(out)) or "."
    fd, tmp = tempfile.mkstemp(suffix=suffix, prefix=".songfmt-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        if check:
            a, b = plan_hash(src), plan_hash(tmp)
            if a != b:
                raise SystemExit(f"songfmt: refused — {src} and the converted song plan differently ({a} vs {b}); "
                                 "nothing written")
        os.replace(tmp, out)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)


STRUCTURAL = {"r", "flam", "drag", "ramp"}


def score_to_notes(doc, name, song_path):
    """(new song, note count): TRACK's score string as a notes list, velocities filled from chirp's plan."""
    import splitpart as SP
    import stemfix as SF
    track = next((t for t in doc.get("tracks", []) if isinstance(t, dict) and t.get("name") == name), None)
    if track is None or not isinstance(track.get("score"), str):
        raise Unsupported(f"track {name!r} not found or has no score string")
    segs = SP.tempo_segments(doc.get("tempo", 120))
    a4 = float(doc.get("a4", 440))
    notes, last, pos = [], [], 0.0
    for tok in track["score"].split():
        if tok == "|":
            continue
        m = SP.TOK.match(tok)
        if not m:
            raise Unsupported(f"score token {tok!r} (only PITCH/Nb@V^marks, R, _ and | convert)")
        head, dur, tail = m.group("head"), float(m.group("dur")), m.group("tail")
        if head in SP.RESTS:
            last = []
        elif head == "_":
            for i in last:
                notes[i]["_beats"] += dur
        else:
            if ":" in head:
                raise Unsupported(f"chord symbol {head!r} (voiced by the patch) does not convert")
            vel = None
            mv = re.match(r"@([\d.]+)", tail)
            if mv:
                vel = float(mv.group(1)) / 127
            expr, expr_end, gate = {}, {}, None
            for mark in [x for x in re.sub(r"^@[\d.]+", "", tail).split("^") if x]:
                k, _, v = mark.partition("=")
                if k in STRUCTURAL:
                    raise Unsupported(f"^{k} in {tok!r} makes extra hits; it does not convert to one note")
                if k == "gate":
                    gate = float(v)
                elif ">" in v:
                    a, b = v.split(">")
                    expr[k], expr_end[k] = float(a), float(b)
                else:
                    expr[k] = float(v) if v else 1.0
            last = []
            members = head.split(",")
            # a chord stays one event with the score's spelling ("A2,E3,A3"): the patch strums chords, not
            # separate notes that happen to start together
            for x in (members if len(members) == 1 else [head]):
                p = SF.parse_pitch(x, a4) if len(members) == 1 else None
                n = {"_at": pos, "_beats": dur, "pitch": (int(p) if p == int(p) else p) if p is not None else x,
                     "vel": vel, "_keys": [SF.parse_pitch(y, a4) for y in members]}
                if expr:
                    n["expr"] = dict(expr)
                if expr_end:
                    n["expr_end"] = dict(expr_end)
                if gate is not None:
                    n["gate"] = gate
                last.append(len(notes))
                notes.append(n)
        pos += dur
    if any(n["vel"] is None for n in notes):
        # tokens without @V: the velocity chirp plays them at (dehumanized plan of this track alone)
        voices = _track_voices(doc, name, song_path)
        for n in notes:
            if n["vel"] is None:
                start = round(SF.beats_to_s(n["_at"], segs) * 48000)
                keys = [k for k in n["_keys"] if k is not None]
                # a member's pitch at the beat, or up to 100 ms after it (a strummed chord's later members), nearest first
                hit = sorted((v for v in voices if -2 <= v["start"] - start <= 4800
                              and (not keys or any(abs(v["key"] - k) < 1e-3 for k in keys))),
                             key=lambda v: abs(v["start"] - start))
                if not hit:
                    raise Unsupported(f"no planned voice for the note at beat {n['_at']:g} ({n['pitch']}) to take a velocity from")
                n["vel"] = hit[0]["vel"]
    out_notes = []
    for n in notes:
        o = {"at": f"{round(n['_at'], 9)!r}b", "len": f"{round(n['_beats'], 9)!r}b", "pitch": n["pitch"], "vel": n["vel"]}
        for k in ("gate", "expr", "expr_end"):
            if k in n:
                o[k] = n[k]
        out_notes.append(o)
    out = json.loads(json.dumps(doc))
    t = next(t for t in out["tracks"] if isinstance(t, dict) and t.get("name") == name)
    keys = list(t)
    t["notes"] = out_notes
    del t["score"]
    out["tracks"][out["tracks"].index(t)] = {k: t[k] for k in [*(k for k in keys if k != "score"), "notes"]}
    return out, len(out_notes)


def _plan_voices(doc, song_path):
    d = os.path.dirname(os.path.abspath(song_path)) or "."
    fd, tmp = tempfile.mkstemp(suffix=".json", prefix=".songfmt-", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(doc, f)
        r = subprocess.run([chirpbin.resolve("chirp"), "--json", "plan", "-f", tmp, "--ir"], capture_output=True, text=True,
                           stdin=subprocess.DEVNULL)
        try:
            return json.loads(r.stdout)["data"]["ir"]["voices"]
        except (ValueError, KeyError, TypeError):
            raise SystemExit(f"songfmt: chirp plan failed: {(r.stderr or r.stdout).strip()[-300:]}")
    finally:
        os.remove(tmp)


def _track_voices(doc, name, song_path):
    """The voices TRACK plays with humanization off: the dehumanized plan minus the plan without the track."""
    import splitpart as SP
    from collections import Counter
    flat = SP.dehumanize(doc, {name})
    key = lambda v: (v["start"], round(v["key"], 6), round(v["vel"], 6))  # noqa: E731
    allv = _plan_voices(flat, song_path)
    without = dict(flat, tracks=[t for t in flat["tracks"] if not (isinstance(t, dict) and t.get("name") == name)])
    rest = Counter(key(v) for v in _plan_voices(without, song_path))
    mine = []
    for v in allv:
        k = key(v)
        if rest[k]:
            rest[k] -= 1
        else:
            mine.append(v)
    return mine


def main(argv):
    a = list(argv)

    def opt(flag):
        if flag in a:
            i = a.index(flag)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return None

    check = "--no-check" not in a
    a = [x for x in a if x != "--no-check"]
    out, like = opt("-o"), opt("--like")
    if len(a) < 2 or a[0] not in ("json", "yaml", "same", "notes"):
        raise SystemExit(__doc__.strip().split("\n\n")[1])
    cmd = a[0]
    try:
        if cmd == "same":
            x, y = load(a[1]), load(a[2])
            if x == y or (check and plan_hash(a[1]) == plan_hash(a[2])):
                print("same" + ("" if x == y else " plan (the documents differ in form)"))
                return 0
            diff = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
            print(f"different: {', '.join(diff) or 'key order'}")
            return 1
        doc = load(a[1])
        if not out:
            raise SystemExit("songfmt: -o OUT is required")
        if cmd == "notes":
            import splitpart as SP
            from collections import Counter
            new, n = score_to_notes(doc, a[2], a[1])
            if check:
                sig = lambda vs: Counter((v["start"], v["end"], round(v["key"], 6), round(v["vel"], 6), v["release"],  # noqa: E731
                                          json.dumps(v.get("expr"))) for v in vs)
                if sig(_plan_voices(SP.dehumanize(doc, {a[2]}), a[1])) != sig(_plan_voices(SP.dehumanize(new, {a[2]}), a[1])):
                    raise SystemExit("songfmt: refused — the notes play differently from the score (a latched octave or "
                                     "velocity, or syntax this does not model); nothing written")
            text = read(a[1])
            body = (json.dumps(new, **json_style(a[1])[0]) + json_style(a[1])[1]) if text.lstrip().startswith("{") \
                else dump_yaml(new)
            write_checked(a[1], body, out, False, os.path.splitext(a[1])[1])
            print(f"wrote {out}: {a[2]} as {n} notes" + (" (proven: the same voices as the score)" if check else ""))
            return 0
        if cmd == "json":
            style, nl = json_style(like) if like else ({"indent": 2, "ensure_ascii": False}, "\n")
            doc = ordered(doc, load(like)) if like else doc
            write_checked(a[1], json.dumps(doc, **style) + nl, out, check, ".json")
        else:
            doc = ordered(doc, load(like)) if like else doc
            if like and read(like).lstrip().startswith("{"):   # a native JSON song under .yaml
                style, nl = json_style(like)
                write_checked(a[1], json.dumps(doc, **style) + nl, out, check, ".yaml")
            else:
                write_checked(a[1], dump_yaml(doc), out, check, ".yaml")
        print(f"wrote {out}" + (" (same plan as the input)" if check else ""))
        return 0
    except Unsupported as e:
        raise SystemExit(f"songfmt: {e}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
