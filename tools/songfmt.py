#!/usr/bin/env python3
"""songfmt: move a song between the flow YAML the tools write and its JSON source, exactly (chirper-zero's request).

  songfmt.py json SONG.yaml -o SOURCE.json [--like SOURCE.json] [--no-check]
  songfmt.py yaml SOURCE.json -o SONG.yaml [--like SONG.yaml] [--no-check]
  songfmt.py same A B                      # do two files resolve to the same song? (exit 0 yes, 1 no)

Songs built from a JSON source (tools/ID-source.json) are rendered from their flow-YAML form (songs/ID.yaml: one
`key: <JSON>` line per top-level field, one `- {key: <JSON>, …}` line per track — what tab2song writes). songride,
widthfit, stemhats and sectionlevel edit that YAML (songride re-appends `master:` after the tracks), so after a
master or part step the source must be regenerated from the YAML. `json` does that: the output keeps --like's
top-level key order (new keys at the end) and its exact formatting (indent, ASCII escaping, trailing newline, found by
reproducing --like byte for byte). `yaml` goes the other way in tab2song's layout (or, when --like is a native JSON song saved as .yaml,
in its JSON formatting).

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
    if len(a) < 2 or a[0] not in ("json", "yaml", "same"):
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
