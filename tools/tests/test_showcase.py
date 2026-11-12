#!/usr/bin/env python3
"""tools/showcase.py: which of the engine's features a song uses (Harry, 12 Nov: "make it a showcase of all features").

Hermetic: a stand-in engine that prints a small schema and a canned plan, so what is offered and what is used are known.
One more test reads the real groove pin's schema when there is one: the tool reads the schema's SHAPE (effects told
apart by a `type` constant, layer options named by the kind their description starts with), and a change of shape would
otherwise turn the checklist empty without a word.

  python3 tools/tests/test_showcase.py      (from ~/.config/chirp; a second or two)
"""
import contextlib
import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import showcase as S  # noqa: E402

SCHEMA = {
    "$defs": {
        "AmpModel": {"oneOf": [{"const": "mark", "description": "Mark-style."}, {"const": "nolly", "description": "Tightest input."}]},
        "LayerKind": {"oneOf": [{"enum": ["noise"], "type": "string"}, {"const": "pluck", "description": "Plucked string."},
                                {"const": "voice"}]},
        "ReverbKind": {"type": "string", "enum": ["room", "hall"]},
        "Effect": {"oneOf": [
            {"type": "object", "description": "A guitar amp.", "properties": {
                "type": {"const": "amp"}, "model": {"$ref": "#/$defs/AmpModel"},
                "gain": {"type": "number", "description": "Drive."}, "bloom": {"type": "number", "description": "Power-tube bloom."}}},
            {"type": "object", "properties": {"type": {"const": "reverb"}, "kind": {"$ref": "#/$defs/ReverbKind"},
                                              "mix": {"type": "number"}}},
            {"type": "object", "description": "A wah pedal.", "properties": {"type": {"const": "wah"}, "pos": {"type": "number"}}}]},
        "Param": {"anyOf": [{"type": "number"}, {"type": "string"},
                            {"type": "object", "properties": {"value": {}, "mod": {"type": "array"}}}]},
        "Layer": {"type": "object", "properties": {
            "type": {"$ref": "#/$defs/LayerKind"},
            "level": {"anyOf": [{"$ref": "#/$defs/Param"}, {"type": "null"}], "description": "The layer's level."},
            "pick": {"type": "number", "description": "pluck: pick position."},
            "mute": {"type": "number", "description": "pluck: a palm on the strings."},
            "nasal": {"type": "number", "description": "voice: nasality."}}},
        "Synth": {"type": "object", "properties": {"layers": {"type": "array", "items": {"$ref": "#/$defs/Layer"}}}},
        "Play": {"type": "object", "properties": {"gate": {"type": "number"}, "phrase_arc": {"type": "number"}}},
        "Patch": {"type": "object", "properties": {
            "synth": {"$ref": "#/$defs/Synth"}, "play": {"anyOf": [{"$ref": "#/$defs/Play"}, {"type": "null"}]},
            "fx": {"type": "array", "items": {"$ref": "#/$defs/Effect"}},
            "kit": {"type": ["object", "null"], "additionalProperties": {"type": "object"}}}},
        "Track": {"type": "object", "properties": {
            "name": {"type": "string"}, "patch": {"anyOf": [{"type": "string"}, {"$ref": "#/$defs/Patch"}]},
            "fx": {"type": "array", "items": {"$ref": "#/$defs/Effect"}}, "notes": {"type": "array"}}},
        "Bus": {"type": "object", "properties": {"fx": {"type": "array", "items": {"$ref": "#/$defs/Effect"}}}},
    },
    "type": "object",
    "properties": {
        "tempo": {"type": "number", "description": "Quarter-note BPM."},
        "patches": {"type": "object", "additionalProperties": {"$ref": "#/$defs/Patch"}},
        "tracks": {"type": "array", "items": {"$ref": "#/$defs/Track"}},
        "buses": {"type": "object", "additionalProperties": {"$ref": "#/$defs/Bus"}},
        "songs": {"type": "object", "additionalProperties": {"$ref": "#"}},
    },
}
PLAN = {"data": {"canonical": {
    "tempo": 120,
    "patches": {
        "rig": {"synth": {"layers": [{"type": "pluck", "pick": 0.2, "level": {"value": 1, "mod": []}}, {"type": "noise"}]},
                "play": {"gate": 0.9},
                "fx": [{"type": "amp", "model": "mark", "gain": 0.8}, "reverb kind=hall mix=0.2"]},
        "kit": {"kit": {"k": {}}},
        "kit.k": {"synth": {"layers": [{"type": "noise"}]}},
    },
    "tracks": [{"name": "gl", "patch": "rig", "notes": []}, {"name": "gr", "patch": "rig", "notes": []},
               {"name": "kick", "patch": "kit", "notes": []}],
    "buses": {"hall": {"fx": [{"type": "reverb", "kind": "room"}]}},
}}}
ENGINE = '''#!/usr/bin/env python3
import json, sys
a = sys.argv[1:]
if a[:2] == ["schema", "song"]:
    print(json.dumps(%r))
elif "plan" in a:
    if "BAD" in open(a[a.index("-f") + 1]).read():
        print(json.dumps({"status": "error", "error": "no patch named nosuch"}))
        sys.exit(2)
    print(json.dumps(%r))
else:
    sys.exit(64)
''' % (SCHEMA, PLAN)


class Showcase(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="showcase-test-")
        self.addCleanup(shutil.rmtree, self.root, True)
        self.engine = os.path.join(self.root, "fake-chirp")
        with open(self.engine, "w") as f:
            f.write(ENGINE)
        os.chmod(self.engine, os.stat(self.engine).st_mode | stat.S_IXUSR)
        self.song = os.path.join(self.root, "song.yaml")
        with open(self.song, "w") as f:
            f.write("tempo: 120\n")

    def run_tool(self, *argv, song=None):
        out, old = io.StringIO(), sys.argv
        sys.argv = ["showcase.py", song or self.song, "--pin", self.engine, *argv]
        try:
            with contextlib.redirect_stdout(out):
                S.main()
        finally:
            sys.argv = old
        return out.getvalue()

    def both(self):
        cat = S.Catalogue(SCHEMA)
        return cat, S.Usage(cat).song(PLAN["data"]["canonical"])

    def test_the_catalogue_is_read_from_the_schema(self):
        cat, _ = self.both()
        self.assertEqual(list(cat.kinds["Effect"]), ["amp", "reverb", "wah"])
        self.assertEqual(cat.kinds["AmpModel"], {"mark": "Mark-style.", "nolly": "Tightest input."})
        self.assertEqual(list(cat.kinds["LayerKind"]), ["noise", "pluck", "voice"])
        self.assertEqual(list(cat.kinds["ReverbKind"]), ["room", "hall"])
        self.assertEqual(list(cat.opts["fx amp"]), ["model", "gain", "bloom"])          # not its `type`
        self.assertEqual(list(cat.opts["Layer pluck"]), ["pick", "mute"])              # by the description's "pluck:"
        self.assertEqual(list(cat.opts["Layer voice"]), ["nasal"])
        self.assertEqual(list(cat.opts["Layer"]), ["type", "level"])
        self.assertIn("songs", cat.opts["Song"])                                       # "$ref": "#" does not loop

    def test_what_the_song_sets_and_where(self):
        _, use = self.both()
        self.assertEqual(use.kinds["Effect"], {"amp": ["rig"], "reverb": ["rig", "bus hall"]})
        self.assertEqual(use.kinds["AmpModel"], {"mark": ["rig"]})
        self.assertEqual(use.kinds["ReverbKind"], {"hall": ["rig"], "room": ["bus hall"]})   # hall from the string form
        self.assertEqual(use.kinds["LayerKind"], {"pluck": ["rig"], "noise": ["rig", "kit"]})  # a kit's piece is its kit
        self.assertEqual(sorted(use.opts["fx amp"]), ["gain", "model"])
        self.assertEqual(sorted(use.opts["Layer pluck"]), ["pick"])
        self.assertEqual(sorted(use.opts["Play"]), ["gate"])
        self.assertNotIn("Layer voice", use.opts)

    def test_the_report_names_what_is_not_used(self):
        text = self.run_tool()
        self.assertIn("3 tracks, 2 patches, 1 buses", text)
        self.assertIn("rig [gl, gr]: pluck + noise -> amp(mark), reverb(hall)", text)
        self.assertIn("kit [kick]: kit of 1 pieces", text)
        lines = text.splitlines()
        i = lines.index("  amp models: 1 of 2")
        self.assertEqual(lines[i + 1:i + 3], ["      used:     mark (rig)", "      not used: nolly"])
        i = lines.index("  effects: 2 of 3")
        self.assertIn("not used: wah", lines[i + 2])
        i = lines.index("  amp (effect): 2 of 3")
        self.assertEqual(lines[i + 1:i + 3], ["      set:   model, gain", "      never: bloom"])
        i = lines.index("  pluck (source): 1 of 2")
        self.assertEqual(lines[i + 2], "      never: mute")
        self.assertNotIn("voice (source)", text)             # a source the song does not use: its options are not listed
        self.assertNotIn("wah (effect)", text)

    def test_all_and_only_also_list_what_is_not_used(self):
        self.assertIn("voice (source): 0 of 1", self.run_tool("--all"))
        text = self.run_tool("--only", "voice|wah")
        self.assertIn("voice (source): 0 of 1", text)
        self.assertIn("wah (effect): 0 of 1", text)
        self.assertNotIn("amp models", text)
        self.assertNotIn("RIGS", text)

    def test_why_gives_the_engines_own_words(self):
        text = self.run_tool("--why", "nolly", "bloom", "pick", "nosuch")
        self.assertIn("nolly: a kind of amp models; NOT used in this song\n    Tightest input.", text)
        self.assertIn("bloom: an option of amp (effect); NOT used in this song\n    Power-tube bloom.", text)
        self.assertIn("pick: an option of pluck (source); used in rig", text)
        self.assertIn("nosuch: the engine's schema has nothing of that name", text)

    def test_json(self):
        d = json.loads(self.run_tool("--json"))
        self.assertEqual(d["kinds"]["Effect"], {"offered": ["amp", "reverb", "wah"],
                                                "used": {"amp": ["rig"], "reverb": ["rig", "bus hall"]}})
        self.assertEqual(d["options"]["fx amp"]["offered"], ["model", "gain", "bloom"])
        self.assertEqual(d["rigs"][0]["fx"], ["amp(mark)", "reverb(hall)"])

    def test_a_song_that_does_not_plan_stops_with_the_engines_words(self):
        bad = os.path.join(self.root, "bad.yaml")
        with open(bad, "w") as f:
            f.write("BAD\n")
        with self.assertRaises(SystemExit) as e:
            self.run_tool(song=bad)
        self.assertIn("does not plan", str(e.exception))
        self.assertIn("no patch named nosuch", str(e.exception))
        with self.assertRaises(SystemExit) as e:
            self.run_tool(song=os.path.join(self.root, "absent.yaml"))
        self.assertIn("no song at", str(e.exception))

    def test_a_schema_without_effects_is_refused_not_reported_as_empty(self):
        with self.assertRaises(SystemExit) as e:
            S.check_shape(S.Catalogue({"type": "object", "properties": {"tempo": {"type": "number"}}}), "x")
        self.assertIn("shape", str(e.exception))


@unittest.skipUnless(os.access(S.chirpbin.resolve("") or "", os.X_OK), "no groove pin on this host")
class RealSchema(unittest.TestCase):
    def test_the_real_schema_still_has_the_shape_the_tool_reads(self):
        pin = S.chirpbin.resolve("")
        cat = S.Catalogue(S.load_schema(pin))
        S.check_shape(cat, pin)
        self.assertGreaterEqual(len(cat.kinds["Effect"]), 40)
        for fx in ("amp", "cab", "reverb", "filter"):
            self.assertIn(fx, cat.kinds["Effect"])
            self.assertTrue(cat.opts.get("fx " + fx), fx)
        self.assertIn("mark", cat.kinds["AmpModel"])
        self.assertIn("pluck", cat.kinds["LayerKind"])
        self.assertIn("pick", cat.opts["Layer pluck"])
        self.assertIn("diction", cat.opts["Layer voice"])
        self.assertIn("phrase_arc", cat.opts["Play"])
        self.assertLess(len(cat.opts["Layer"]), 40)           # the options are sorted under their kinds, not left in one heap


if __name__ == "__main__":
    unittest.main()
