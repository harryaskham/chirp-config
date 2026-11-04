import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import palette as P  # noqa: E402

LIB = {"machine-kit": "", "brush-kit": "", "lead": ""}
KIT = {"kit": {"k": {}, "s": {}, "h": {}, "oh": {}}}


def test_kit_voices_counts_only_voices_played():
    cn = {"patches": {"machine-kit": KIT, "lead": {"synth": {}}},
          "tracks": [{"name": "kick", "patch": "machine-kit", "notes": [{"pitch": "k"}, {"at": 1, "pitch": "k"}]},
                     {"name": "lead", "patch": "lead", "notes": [{"pitch": "C4"}]}]}
    assert P.kit_voices(cn, LIB) == {("machine-kit", "k")}


def test_kit_voices_follows_variant_keys_and_nested_tracks():
    key = "brush-kit play.humanize.drunk=4ms"
    cn = {"patches": {key: KIT},
          "tracks": [{"name": "group", "tracks": [{"name": "hats", "patch": key, "notes": [{"pitch": "h"}, {"pitch": "oh"}]}]}]}
    assert P.kit_voices(cn, LIB) == {("brush-kit", "h"), ("brush-kit", "oh")}


def test_kit_voices_ignores_song_own_kits_and_non_voice_pitches():
    cn = {"patches": {"mykit": KIT, "machine-kit": KIT},
          "tracks": [{"name": "a", "patch": "mykit", "notes": [{"pitch": "k"}]},
                     {"name": "b", "patch": "machine-kit", "notes": [{"pitch": "C4"}, {"pitch": "zz"}]}]}
    assert P.kit_voices(cn, LIB) == set()
    assert P.kit_voices(None, LIB) == set()
