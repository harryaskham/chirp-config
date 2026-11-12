#!/usr/bin/env python3
"""showcase: which of the engine's features a song uses, and which it does not.

Harry, 12 Nov, on Common Time: "make it a showcase of all features". This is the checklist for that. It asks the engine
itself what exists (`chirp schema song`: every effect, sound source, amp, cabinet, tone stack, reverb, option ...) and
what the song really is after every patch and `extends` is resolved (`chirp plan`), and sets one against the other.
Nothing is hard-coded, so a feature that lands in the engine tomorrow appears here as "not used" the day the groove
adopts it.

  showcase.py SONG.yaml                 the rigs, then every kind the engine offers (used, with where; not used), then
                                        the options of what is used (set somewhere / never set)
  showcase.py SONG.yaml --only amp      only the lines whose name matches (a regular expression, any case)
  showcase.py SONG.yaml --all           also the options of sound sources and effects the song does not use
  showcase.py SONG.yaml --why nolly bloom pickup_nl
                                        what the engine says each of these is (its own description), and where it lives
  showcase.py SONG.yaml --diff ct-chug-l ct-bite-l
                                        how two of the song's patches really differ, setting by setting, once resolved
                                        (two rigs that differ only in the amp are one guitar through two amps).
                                        It counts settings; it cannot know which are heard: through a saturated amp
                                        (gain 0.3 and up on these models) a different string moved the spectrum by
                                        about 2 dB at most (chirper-zero, Common Time v14); measure before trusting it
  showcase.py SONG.yaml --json          the same as data
  --pin BIN                             another engine (default: $CHIRP, else the groove's pin, tools/groove-pin)

Read it as a map, not a score. A KIND is used when the song or a patch it plays names it, or gets it by default from
something it does use (a reverb with no `kind` is a hall, an amp with no `model` is `modern`: listed as "by default").
An OPTION is "set" when it is given a value other than the engine's default somewhere; the plan drops values equal to
the default, so "default" means nowhere moved, written or not. A feature left out because it does not serve the piece
is a choice; a feature nobody knew was there is what this is for.
(chirp-eco, 12 Nov; tests: tools/tests/test_showcase.py.)"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chirpbin  # noqa: E402

NAMES = {"Effect": "effects", "LayerKind": "sound sources (layer kinds)", "AmpModel": "amp models", "CabModel": "cabinets",
         "ToneStack": "tone stacks", "ReverbKind": "reverbs", "FilterKind": "filter kinds", "Shape": "drive shapes",
         "Wave": "oscillator waves", "PickMode": "pick modes", "Voicing": "voicings", "Exciter": "wind exciters",
         "Beater": "drum beaters", "SystemKind": "generative systems", "Color": "noise colours", "ChipKind": "chip channels"}
FIRST = ["Effect", "LayerKind", "AmpModel", "CabModel", "ToneStack", "ReverbKind", "FilterKind", "Shape", "PickMode", "Voicing"]


def die(msg):
    sys.exit("showcase: " + msg)


def engine(pin, *args):
    env = dict(os.environ)
    env.pop("LD_LIBRARY_PATH", None)
    try:
        return subprocess.run([pin, *args], capture_output=True, text=True, env=env, timeout=600)
    except OSError as e:
        die(f"cannot run {pin}: {e}")


def load_schema(pin):
    r = engine(pin, "schema", "song")
    try:
        return json.loads(r.stdout)
    except ValueError:
        die(f"`{os.path.basename(pin)} schema song` gave no schema: {(r.stderr or r.stdout)[-300:]}")


def load_plan(pin, song):
    r = engine(pin, "--json", "plan", "-f", song)
    try:
        d = json.loads(r.stdout)
        return d["data"]["canonical"]
    except (ValueError, KeyError, TypeError):
        try:
            why = json.loads(r.stdout).get("error") or r.stdout
        except ValueError:
            why = r.stderr or r.stdout
        die(f"{song} does not plan on {os.path.basename(pin)}: {str(why)[-400:]}")


def first_line(text):
    return " ".join((text or "").split())


class Catalogue:
    """What the engine offers, read from its JSON Schema: `kinds[label][value]` (enumerations) and `opts[label][option]`
    (an object's properties), each with the engine's description. Labels are the schema's definition names; an effect's
    options are under "fx TYPE", a layer's under "Layer KIND" (from the "KIND: ..." its description starts with)."""

    def __init__(self, schema):
        self.defs = dict(schema.get("$defs") or schema.get("definitions") or {})
        self.root = schema
        self.defs.setdefault("Song", {k: v for k, v in schema.items() if k not in ("$defs", "definitions")})
        self.kinds, self.opts = {}, {}
        self.layer_group = {}
        self._layer_kinds = set()
        self.default_kind = (((self.defs.get("Layer") or {}).get("properties") or {}).get("type") or {}).get("default") or "osc"
        lk = self.defs.get("LayerKind") or {}
        for node in [lk] + (lk.get("oneOf") or []) + (lk.get("anyOf") or []):
            self._layer_kinds |= {v for v, _ in self._values(node)}
        seen = {"Song"}
        self._build(self.defs["Song"], "Song", seen)

    def ref(self, sch):
        """The definition a $ref names; "#" (a song inside a song) is the root, kept under the name "Song"."""
        r = sch["$ref"]
        return "Song" if r == "#" else r.rsplit("/", 1)[-1]

    @staticmethod
    def _values(sch):
        """[(value, description)] when the node is a string enumeration (enum, const, or a oneOf of them)."""
        out = []
        if isinstance(sch, dict):
            desc = first_line(sch.get("description"))
            out += [(v, desc) for v in sch.get("enum") or [] if isinstance(v, str)]
            if isinstance(sch.get("const"), str):
                out.append((sch["const"], desc))
        return out

    def group(self, label, key, sch=None):
        """The label an option is listed under: a Layer's options are split by the kind their description names."""
        if label != "Layer":
            return label
        if key not in self.layer_group:
            desc = (sch or {}).get("description") or ""
            m = re.match(r"([a-z][a-z0-9]*)[a-z0-9 ,/]*:\s", desc)
            self.layer_group[key] = f"Layer {m.group(1)}" if m and m.group(1) in self._layer_kinds else "Layer"
        return self.layer_group[key]

    def _build(self, sch, label, seen):
        if not isinstance(sch, dict):
            return
        if "$ref" in sch:
            name = self.ref(sch)
            if name not in seen and name in self.defs:
                seen.add(name)
                self._build(self.defs[name], name, seen)
            return
        for s in sch.get("allOf") or []:
            self._build(s, label, seen)
        for v, desc in self._values(sch):
            self.kinds.setdefault(label, {})[v] = desc
        for a in (sch.get("oneOf") or []) + (sch.get("anyOf") or []):
            self._build(a, label, seen)
        props = sch.get("properties")
        if props:
            lab = label
            t = props.get("type") if label == "Effect" else None
            if isinstance(t, dict) and isinstance(t.get("const"), str):
                lab = "fx " + t["const"]
                self.kinds.setdefault("Effect", {})[t["const"]] = first_line(sch.get("description"))
                self.opts.setdefault(lab, {})
            for k, v in props.items():
                if lab.startswith("fx ") and k == "type":
                    continue
                self.opts.setdefault(self.group(lab, k, v), {})[k] = first_line(v.get("description") if isinstance(v, dict) else "")
                self._build(v, f"{lab}.{k}", seen)
        if isinstance(sch.get("additionalProperties"), dict):
            self._build(sch["additionalProperties"], label + ".*", seen)
        if isinstance(sch.get("items"), dict):
            self._build(sch["items"], label, seen)
        for s in sch.get("prefixItems") or []:
            self._build(s, label, seen)


class Usage:
    """Walk the planned song beside the schema and note what is set, and where (a patch, a track, a bus, the master)."""

    def __init__(self, cat):
        self.cat = cat
        self.kinds, self.opts = {}, {}

    def _mark(self, table, label, value, ctx):
        where = table.setdefault(label, {}).setdefault(value, [])
        if ctx not in where:
            where.append(ctx)

    def _resolved(self, sch):
        while isinstance(sch, dict) and "$ref" in sch and self.cat.ref(sch) in self.cat.defs:
            sch = self.cat.defs[self.cat.ref(sch)]
        return sch

    def _fits(self, inst, sch):
        s = self._resolved(sch)
        if not isinstance(s, dict):
            return 1
        alts = (s.get("oneOf") or []) + (s.get("anyOf") or [])
        if alts and not s.get("properties"):
            return max((self._fits(inst, a) for a in alts), default=0)
        types = s.get("type")
        types = set(types if isinstance(types, list) else [types] if types else [])
        if isinstance(inst, str):
            if "const" in s or "enum" in s:
                return 3 if inst == s.get("const") or inst in (s.get("enum") or []) else 0
            return 1 if not types or "string" in types else 0
        if isinstance(inst, dict):
            props = s.get("properties")
            if props is None and "object" not in types:
                return 0
            t = (props or {}).get("type")
            if isinstance(t, dict) and "const" in t:
                return 3 if inst.get("type") == t["const"] else 0
            return 1 + (sum(k in props for k in inst) / (len(inst) + 1) if props else 0)
        if isinstance(inst, list):
            return 1 if "array" in types or "items" in s or "prefixItems" in s else 0
        if isinstance(inst, bool):
            return 1 if not types or "boolean" in types else 0
        if inst is None:
            return 1 if not types or "null" in types else 0
        return 1 if not types or types & {"number", "integer"} else 0

    def walk(self, inst, sch, label, ctx):
        if not isinstance(sch, dict) or inst is None:
            return
        if "$ref" in sch:
            name = self.cat.ref(sch)
            if name in self.cat.defs:
                self.walk(inst, self.cat.defs[name], name, ctx)
            return
        for s in sch.get("allOf") or []:
            self.walk(inst, s, label, ctx)
        if label == "Effect" and isinstance(inst, str):
            inst = parse_fx(inst)
        alts = (sch.get("oneOf") or []) + (sch.get("anyOf") or [])
        if alts:
            scored = [(self._fits(inst, a), a) for a in alts]
            best = max((s for s, _ in scored), default=0)
            for s, a in scored:
                if s and s == best:
                    self.walk(inst, a, label, ctx)
        if isinstance(inst, str):
            if inst in self.cat.kinds.get(label, {}) and (inst == sch.get("const") or inst in (sch.get("enum") or [])):
                self._mark(self.kinds, label, inst, ctx)
            return
        if isinstance(inst, dict):
            props = sch.get("properties") or {}
            lab = label
            if label == "Effect" and props:
                lab = "fx " + str(inst.get("type"))
                if inst.get("type") in self.cat.kinds.get("Effect", {}):
                    self._mark(self.kinds, "Effect", inst["type"], ctx)
            ap = sch.get("additionalProperties")
            for k, v in inst.items():
                if k in props:
                    if not (lab.startswith("fx ") and k == "type"):
                        self._mark(self.opts, self.cat.group(lab, k, props[k]), k, ctx)
                    self.walk(v, props[k], f"{lab}.{k}", ctx)
                elif isinstance(ap, dict):
                    self.walk(v, ap, label + ".*", ctx)
            self._defaults(inst, props, lab, ctx)
        elif isinstance(inst, list):
            items = sch.get("items")
            pre = sch.get("prefixItems") or []
            for i, x in enumerate(inst):
                self.walk(x, pre[i] if i < len(pre) else items, label, ctx)

    def _defaults(self, inst, props, lab, ctx):
        """The kinds this object gets by default: the plan leaves out what equals the engine's default, so a reverb with
        no `kind` is still a hall. A layer only takes the defaults of its own kind's options."""
        mine = None
        if lab == "Layer":
            t = props.get("type") if isinstance(props.get("type"), dict) else {}
            mine = f"Layer {inst.get('type', t.get('default'))}"
        for k, ps in props.items():
            if k in inst or not isinstance(ps, dict) or not isinstance(ps.get("default"), str):
                continue
            if mine and self.cat.group(lab, k, ps) not in ("Layer", mine):
                continue
            refs = [x for x in [ps] + (ps.get("anyOf") or []) + (ps.get("oneOf") or []) if isinstance(x, dict) and "$ref" in x]
            for target in [self.cat.ref(x) for x in refs] + [f"{lab}.{k}"]:
                if ps["default"] in self.cat.kinds.get(target, {}):
                    self._mark(self.kinds, target, ps["default"], ctx + " by default")
                    break

    def song(self, canon):
        props = self.cat.root.get("properties") or {}
        for k, v in canon.items():
            if k not in props or v is None:
                continue
            self._mark(self.opts, "Song", k, "song")
            sub = self._resolved(props[k])
            if k == "patches" and isinstance(v, dict):
                for name, p in v.items():
                    self.walk(p, sub.get("additionalProperties"), "Song.patches.*", base(name))
            elif k == "tracks" and isinstance(v, list):
                for t in v:
                    self.walk(t, sub.get("items"), "Song.tracks", f"track {t.get('name', '?')}" if isinstance(t, dict) else "track")
            elif k == "buses" and isinstance(v, dict):
                for name, b in v.items():
                    self.walk(b, sub.get("additionalProperties"), "Song.buses.*", f"bus {name}")
            else:
                self.walk(v, props[k], f"Song.{k}", "master" if k == "master" else "song")
        return self


def base(name):
    """The patch a name belongs to: "ct-kit.k" (a kit's piece) and "haake-hat amp.r=80ms" (overrides) are their base."""
    return name.split()[0].split(".")[0] if name.split() else name


def check_shape(cat, pin):
    """Refuse a schema this tool cannot read rather than report an empty checklist (it reads the schema's shape: effects
    told apart by a `type` constant, a layer's options named by the kind their description starts with)."""
    if len(cat.kinds.get("Effect", {})) < 2 or not cat.opts.get("Song"):
        die(f"{os.path.basename(pin)}'s schema is not the shape this tool reads (it found {len(cat.kinds.get('Effect', {}))} "
            f"effects): the engine's schema changed; fix tools/showcase.py (tools/tests/test_showcase.py says what it expects)")


def parse_fx(text):
    """An effect written as a string ("reverb kind=hall mix=0.2") as the object the schema describes."""
    try:
        words = shlex.split(text)
    except ValueError:
        words = text.split()
    if not words:
        return text
    out = {"type": words[0]}
    for w in words[1:]:
        k, eq, v = w.partition("=")
        out[k] = v if eq else True
    return out


def rigs(canon, default_kind="osc"):
    """One line a patch the song plays: its sound sources, then its effects in order (an amp with its model, a cabinet
    or reverb with its kind). Kit pieces are counted, not listed."""
    patches = canon.get("patches") or {}
    played = []
    for t in canon.get("tracks") or []:
        p = t.get("patch") if isinstance(t, dict) else None
        if isinstance(p, str) and p.split() and p.split()[0] not in played:
            played.append(p.split()[0])
    out = []
    for name in played:
        p = patches.get(name)
        if not isinstance(p, dict):
            continue
        pieces = sum(1 for n in patches if n.startswith(name + "."))
        layers = [str(ly.get("type") or default_kind) for ly in ((p.get("synth") or {}).get("layers") or [])
                  if isinstance(ly, dict)]
        src = " + ".join(f"{k}×{layers.count(k)}" if layers.count(k) > 1 else k for k in dict.fromkeys(layers))
        chain = []
        for f in (p.get("fx") or []) + ((p.get("synth") or {}).get("fx") or []):
            f = parse_fx(f) if isinstance(f, str) else f
            if isinstance(f, dict):
                tags = [str(f[k]) + (" stack" if k == "stack" else "") for k in ("model", "stack", "kind", "file", "shape")
                        if isinstance(f.get(k), str)]
                chain.append(f"{f.get('type')}({', '.join(tags)})" if tags else str(f.get("type")))
        tracks = [t.get("name") for t in canon.get("tracks") or [] if isinstance(t, dict) and isinstance(t.get("patch"), str)
                  and t["patch"].split() and t["patch"].split()[0] == name]
        out.append({"patch": name, "tracks": tracks, "sources": src or (f"kit of {pieces} pieces" if pieces else "-"),
                    "pieces": pieces, "fx": chain})
    return out


def kind_order(labels):
    return [k for k in FIRST if k in labels] + sorted((k for k in labels if k not in FIRST), key=lambda s: NAMES.get(s, s).lower())


def nice(label):
    if label in NAMES:
        return NAMES[label]
    if label.startswith("fx "):
        return label[3:] + " (effect)"
    if label.startswith("Layer "):
        return label[6:] + " (source)"
    return {"Layer": "any source (layer)", "Play": "play", "Synth": "synth", "Track": "track", "Bus": "bus", "Note": "note",
            "Song": "song", "Patch": "patch"}.get(label, label)


def where(ctxs, n=3):
    return ", ".join(ctxs[:n]) + (f", +{len(ctxs) - n}" if len(ctxs) > n else "")


def wrap(prefix, words, width=132):
    lines, cur = [], prefix
    for i, w in enumerate(words):
        piece = w + ("," if i < len(words) - 1 else "")
        if len(cur) + 1 + len(piece) > width and cur.strip() != prefix.strip():
            lines.append(cur)
            cur = " " * len(prefix)
        cur += (" " if cur.strip() and not cur.endswith(" ") else "") + piece
    return lines + [cur]


def report(cat, use, canon, a):
    pat = re.compile(a.only, re.I) if a.only else None
    keep = lambda label: not pat or pat.search(label) or pat.search(nice(label))   # noqa: E731
    out = []
    if not pat:
        out.append("RIGS (each patch the song plays: its sources -> its effects, in order)")
        for r in rigs(canon, cat.default_kind):
            tr = f" [{where(r['tracks'], 4)}]" if r["tracks"] else ""
            out += wrap(f"  {r['patch']}{tr}: {r['sources']}{' ->' if r['fx'] else ''}", r["fx"])
        out.append("")
    out.append("KINDS (what the engine offers / what this song uses, and where)")
    for label in kind_order(cat.kinds):
        vals = cat.kinds[label]
        if len(vals) < 2 or not keep(label):
            continue
        used = use.kinds.get(label, {})
        if not used and label not in FIRST and not pat:
            out += wrap(f"  {nice(label)}: 0 of {len(vals)}: ", list(vals))
            continue
        out.append(f"  {nice(label)}: {len(used)} of {len(vals)}")
        if used:
            out += wrap("      used:     ", [f"{v} ({where(used[v])})" for v in vals if v in used])
        if len(used) < len(vals):
            out += wrap("      not used: ", [v for v in vals if v not in used])
    out.append("")
    out.append("OPTIONS of what is used (set: moved from the engine's default somewhere; default: nowhere)"
               + ("" if not (a.all or pat) else ", and of what is not used"))
    used_fx = set(use.kinds.get("Effect", {}))
    used_layers = set(use.kinds.get("LayerKind", {}))
    full = []
    for label in sorted(cat.opts, key=lambda s: (not s.startswith("fx "), not s.startswith("Layer"), s)):
        opts = cat.opts[label]
        if not opts or not keep(label) or "." in label:
            continue
        live = (label[3:] in used_fx if label.startswith("fx ") else label[6:] in used_layers if label.startswith("Layer ")
                else bool(use.opts.get(label)))
        if not live and not (a.all or pat):
            continue
        got = use.opts.get(label, {})
        if len(got) == len(opts) and not (a.all or pat):
            full.append(nice(label))                     # nothing left to find there
            continue
        out.append(f"  {nice(label)}: {len(got)} of {len(opts)}")
        if got:
            out += wrap("      set:     ", [k for k in opts if k in got])
        if len(got) < len(opts):
            out += wrap("      default: ", [k for k in opts if k not in got])
    if full:
        out += wrap("  every option set of: ", full)
    return out


def flatten(x, path="", out=None):
    """A resolved patch as {path: value}. Effects (and layers, when each names its type) are numbered with their type,
    "fx.3:amp.model", so the same effect in the same place lines up and a different one shows as only on one side."""
    out = {} if out is None else out
    if isinstance(x, dict):
        for k, v in x.items():
            if k != "about":
                flatten(v, f"{path}.{k}" if path else k, out)
    elif isinstance(x, list):
        if path.rsplit(".", 1)[-1] == "fx":
            x = [parse_fx(v) if isinstance(v, str) else v for v in x]
        typed = bool(x) and all(isinstance(v, dict) and isinstance(v.get("type"), str) for v in x)
        for i, v in enumerate(x, 1):
            if typed:
                out[f"{path}.{i}:{v['type']}"] = "(on)"
                flatten({k: w for k, w in v.items() if k != "type"}, f"{path}.{i}:{v['type']}", out)
            else:
                flatten(v, f"{path}.{i}", out)
    else:
        out[path] = x
    return out


def diff(canon, a, b):
    patches = canon.get("patches") or {}
    for n in (a, b):
        if not isinstance(patches.get(n), dict):
            die(f"the song plays no patch named {n}. It has: {', '.join(sorted(k for k in patches if '.' not in k))}")
    fa, fb = flatten(patches[a]), flatten(patches[b])
    keys = list(dict.fromkeys(list(fa) + list(fb)))
    group = lambda k: ".".join(k.split(".")[:2]) if k.startswith(("fx.", "synth.")) else k.split(".")[0]   # noqa: E731
    differ = [k for k in keys if fa.get(k) != fb.get(k)]
    out = [f"{a} against {b}: {len(differ)} of {len(keys)} settings differ"]
    same = {}
    for k in keys:
        same.setdefault(group(k), [0, 0])[k in differ] += 1
    whole = [f"{g} ({n[0]})" for g, n in same.items() if not n[1]]
    if whole:
        out += wrap("  the same in both: ", whole)
    if differ:
        wk = min(44, max(len(k) for k in differ))
        wa = min(34, max(len(str(fa.get(k, "-"))) for k in differ))
        out.append(f"  {'setting':{wk}s}  {a[:wa]:{wa}s} | {b}")
        for k in differ:
            out.append(f"  {k[:wk]:{wk}s}  {str(fa.get(k, '-'))[:wa]:{wa}s} | {fb.get(k, '-')}")
    return out


def why(cat, use, names):
    out = []
    for n in names:
        hits = []
        for label, vals in cat.kinds.items():
            if n in vals:
                hits.append((label, "a kind of " + nice(label), vals[n], use.kinds.get(label, {}).get(n)))
        for label, opts in cat.opts.items():
            if n in opts and "." not in label:
                hits.append((label, "an option of " + nice(label), opts[n], use.opts.get(label, {}).get(n)))
        if not hits:
            out.append(f"{n}: the engine's schema has nothing of that name")
        for _, what, desc, ctxs in hits:
            out.append(f"{n}: {what}; {'used in ' + where(ctxs, 6) if ctxs else 'NOT used in this song'}"
                       if what.startswith("a kind") else
                       f"{n}: {what}; {'set in ' + where(ctxs, 6) if ctxs else 'at its default everywhere in this song'}")
            out += textwrap.wrap(desc or "(the engine gives no description)", 118, initial_indent="    ", subsequent_indent="    ")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("song")
    ap.add_argument("--pin")
    ap.add_argument("--only")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--why", nargs="+")
    ap.add_argument("--diff", nargs=2, metavar=("PATCH_A", "PATCH_B"))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.song):
        die(f"no song at {a.song}")
    pin = a.pin or chirpbin.resolve("chirp")
    cat = Catalogue(load_schema(pin))
    check_shape(cat, pin)
    canon = load_plan(pin, a.song)
    if a.diff:
        print("\n".join(diff(canon, *a.diff)))
        return
    use = Usage(cat).song(canon)
    if a.json:
        print(json.dumps({"song": a.song, "engine": os.path.basename(pin), "rigs": rigs(canon, cat.default_kind),
                          "kinds": {k: {"offered": list(v), "used": use.kinds.get(k, {})} for k, v in cat.kinds.items()},
                          "options": {k: {"offered": list(v), "used": use.opts.get(k, {})} for k, v in cat.opts.items()
                                      if "." not in k}}, ensure_ascii=False))
        return
    if a.why:
        print("\n".join(why(cat, use, a.why)))
        return
    n_tracks = len(canon.get("tracks") or [])
    n_patch = len([n for n in (canon.get("patches") or {}) if "." not in n])
    print(f"showcase: {a.song} on {os.path.basename(pin)}: {n_tracks} tracks, {n_patch} patches, {len(canon.get('buses') or {})} buses")
    print("\n".join(report(cat, use, canon, a)))


if __name__ == "__main__":
    main()
