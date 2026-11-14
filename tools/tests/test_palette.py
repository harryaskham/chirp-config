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


# ── what a track does in the song, from the plan (14 Nov) ──
def _song():
    drone = [{"len": 16, "pitch": "F1"}, {"at": 32, "len": 8, "pitch": "F1"}]            # bars 1-4 and 9-10
    return {"tempo": 96, "patches": {"kit-here": KIT, "bow": {"synth": {}}, "voice": {"synth": {}}, "gtr": {"synth": {}}},
            "tracks": [
                {"name": "drone", "patch": "bow", "notes": drone},
                {"name": "chant", "patch": "voice", "notes": [{"len": 16, "pitch": "F2"}, {"len": 16, "pitch": "C3"}]},   # bars 1-4
                {"name": "gl", "patch": "gtr", "notes": [{"at": 16 + k, "len": 0.5, "pitch": p}
                                                         for k, p in enumerate(["F1", "Eb2", "C2", "B1"] * 6)]},      # bars 5-10
                {"name": "bell", "patch": "voice", "notes": [{"at": 40, "len": 4, "pitch": "Eb5"}]},                  # bar 11, alone
                {"name": "kick", "patch": "kit-here", "notes": [{"at": 16 + 2 * k, "pitch": "k"} for k in range(12)]},
                {"name": "empty", "patch": "bow", "notes": []}]}


def test_roles_read_register_bars_and_the_floor():
    r = P.roles(_song())
    assert set(r) == {"drone", "chant", "gl", "bell", "kick"}
    assert (r["drone"]["lo"], r["drone"]["hi"], r["drone"]["lo_hz"]) == ("F1", "F1", 43.7)
    assert (r["drone"]["bars"], r["drone"]["of"], r["drone"]["lowest"]) == (6, 11, 6)
    assert r["drone"]["floor"] == [0, 1, 2, 3]            # an octave under the chant; level with the guitar in bars 9-10
    assert (r["chant"]["lo"], r["chant"]["hi"], r["chant"]["lowest"], r["chant"]["floor"]) == ("F2", "C3", 0, [])
    assert (r["gl"]["lo"], r["gl"]["hi"], r["gl"]["bars"], r["gl"]["lowest"]) == ("F1", "Eb2", 6, 6)
    assert r["gl"]["floor"] == [4, 5, 6, 7]               # bars 5-8: nothing else pitched under it
    assert r["bell"]["floor"] == [10]                     # the only pitched part there is
    assert r["kick"] == {"kit": True, "hits": 12, "bars": 6, "of": 11}


def test_role_lines_and_bar_ranges():
    r = P.roles(_song())
    assert P.role_line("drone", r["drone"]) == ("drone: F1 (43.7 Hz) as written; sounds in 6 of 11 bars; the lowest written part in 6; "
                                                "THE FLOOR (an octave or more under every other pitched part) in 4: bars 1-4")
    assert P.role_line("chant", r["chant"]) == ("chant: F2-C3 (87.3-130.8 Hz) as written; sounds in 4 of 11 bars; "
                                                "the lowest written part in 0")
    assert P.role_line("kick", r["kick"]) == "kick: a kit's part, 12 hits in 6 of 11 bars"
    assert P.spans([0, 1, 2, 7, 9, 10]) == "1-3, 8, 10-11"
    assert P.note_name(29) == "F1" and P.note_name(63) == "Eb4"


def test_roles_without_bars_when_the_song_is_not_in_one_tempo_and_four_four():
    for change in ({"tempo": [[0, 120], [8, 90]]}, {"meter": "7/8"}):
        r = P.roles(dict(_song(), **change))
        assert r["drone"]["of"] is None and "floor" not in r["drone"]
        assert P.role_line("drone", r["drone"]) == "drone: F1 (43.7 Hz) as written"
        assert P.role_line("kick", r["kick"]) == "kick: a kit's part, 12 hits"


if __name__ == "__main__":
    import traceback
    failed = 0
    for _name, _fn in sorted(globals().items()):
        if _name.startswith("test_") and callable(_fn):
            try:
                _fn()
                print("ok  ", _name)
            except Exception:
                failed += 1
                print("FAIL", _name)
                traceback.print_exc()
    print(f"{'FAILED' if failed else 'OK'} ({failed} failed)")
    sys.exit(1 if failed else 0)
