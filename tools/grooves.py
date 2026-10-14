#!/usr/bin/env python3
"""Build the groove library: drum-only, tempo-inheriting parts (songs/groove-*.yaml) from the
composer's drum generators with fixed seeds, so good grooves persist and anyone can drop them in:
`@groove-mesh-11-8-a`, `@groove-tool-31-8-33233233234-tribal`, `@groove-blast-bomb`."""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as c

DRUMS = ("kick", "snare", "cym", "hats", "rim", "shaker", "ride", "clap", "frame", "blocks")


def drums_only(tracks):
    return [t for t in tracks if t["name"] in DRUMS]


def save(name, about, tracks, beats=16):
    c.write(name, about, drums_only(tracks), beats)
    return name


def main():
    k = c.Key(5, "phrygian")  # pitch content is irrelevant for kits
    prog, low = [0, 1, 0, 6], 28
    made = []
    for i, seed in enumerate([11, 23, 37, 51]):
        r = random.Random(seed)
        made.append(save(f"groove-djent-{'abcd'[i]}", f"djent 4/4: kick locked to a 16th riff cell (seed {seed}), backbeat zones with ghosts, ride tip/shank, china/stack accents", c.gen_djent(r, k, prog, low)))
    for i, seed in enumerate([5, 9]):
        r = random.Random(seed)
        made.append(save(f"groove-djent-break-{'ab'[i]}", "djent half-time breakdown: kick locked to a sparse cell, snare on 3", c.gen_djent(r, k, prog, low, breakdown=True)))
    for cyc, label in [(14, "7-8"), (22, "11-8"), (26, "13-8"), (18, "9-8"), (23, "23-16"), (13, "13-16")]:
        r = random.Random(cyc)
        made.append(save(f"groove-mesh-{label}", f"Meshuggah: a {cyc}/16 cycle over a 4/4 pulse — kick follows the riff, ride tip/shank, half-time snare, china on each restart", c.gen_meshuggah(r, k, low, None, cyc)))
    for cyc, label in [(22, "11-8"), (14, "7-8")]:
        r = random.Random(100 + cyc)
        made.append(save(f"groove-mesh-toms-{label}", f"Meshuggah tom groove: {cyc}/16 cycle, chug runs walk the toms, kick+floor on accents, bell quarters", c.gen_meshuggah(r, k, low, None, cyc, mode="toms")))
    r = random.Random(77)
    made.append(save("groove-mesh-shuffle", "Meshuggah shuffle: triplet grid, 11-step cycle, hats at varying openings", c.gen_meshuggah(r, k, low, None, 11, grid="12", mode="shuffle")))
    for i, cyc in enumerate([7, 11, 5]):
        r = random.Random(200 + cyc)
        made.append(save(f"groove-garstka-{'abc'[i]}", f"Garstka-style breakdown around a {cyc}-eighth cycle: double-kick rolls (32nd bursts), linear toms, stack/splash/china accents, flams, ghosts", c.gen_meshuggah(r, k, low, None, cyc, grid="8", mode="break")))
    for kind in ["trad", "hammer", "bomb", "dbeat"]:
        r = random.Random(len(kind))
        made.append(save(f"groove-blast-{kind}", f"tech-death {kind} blast: ride tip/bell, china on bar starts, tom fill", c.gen_blast(r, k, prog, low, kind)))
    for kind in ["gallop", "chromatic", "skank", "half"]:
        r = random.Random(len(kind) * 3)
        made.append(save(f"groove-thrash-{kind}", f"thrash {kind}: crash/crash-bell downbeats, ride/hats by feel, snare-roll fill", c.gen_thrash(r, k, prog, 40, kind)))
    for meter, groups in [(5, [3, 2]), (7, [2, 2, 3]), (7, [3, 2, 2]), (9, [2, 2, 2, 3]), (11, [3, 3, 3, 2]), (13, [3, 3, 3, 4]), (15, [4, 4, 4, 3]), (31, [8, 8, 8, 7]), (31, [3, 3, 2, 3, 3, 2, 3, 3, 2, 3, 4]), (31, [7, 7, 7, 5, 5])]:
        for mode in ["heavy", "tribal"] + (["clean"] if meter in (5, 7, 9) else []):
            r = random.Random(meter * 10 + len(groups))
            g = "".join(map(str, groups))
            beats = meter * c.reps_for(meter) / 2
            made.append(save(f"groove-tool-{meter}-8-{g}-{mode}", f"Tool-style {meter}/8 ({'+'.join(map(str, groups))}) {mode}: kick/toms rotate across groups, snare on chosen groups, ride/bell or woodblock/cowbell polyrhythm, crash per cycle, tom cascade", c.gen_tool(r, k, low, meter, groups, mode), beats))
    # chill grooves (tight / lofi / brush kits)
    c._RIGSET = c.RIG_SETS["chill"]
    for i, seed in enumerate([3, 8]):
        made.append(save(f"groove-lofi-{'ab'[i]}", "lofi hip hop boom-bap: swung kick/snare, lazy hats", c.gen_lofi_drums(random.Random(seed), busy=i == 1)))
    made.append(save("groove-bossa", "bossa nova: rim clicks on a 3-2 clave, soft shaker, kick on 1 and 3", c.gen_bossa(random.Random(4), k, prog)))
    for meter, label in [(7, "7-8"), (10, "5-4")]:
        beats = meter * 2 * (4 if meter in (7, 9) else 3) / 4
        made.append(save(f"groove-broken-{label}", f"UK jazz broken beat in {label.replace('-', '/')}: shuffled 16ths, odd kick placements, ghosts", c.gen_broken(random.Random(meter), k, prog, meter, "drums"), beats))
    made.append(save("groove-ballad-brush", "jazz ballad brushes: swung ride, soft snare", c.gen_ballad(random.Random(5), k, prog)))
    made.append(save("groove-triphop", "trip-hop: dusty half-time breakbeat, low-passed", c.gen_triphop(random.Random(6), k, prog)))
    made.append(save("groove-trio", "GoGo Penguin trio drums: busy tight hats, offbeat kicks", c.gen_trio_drums(random.Random(7))))
    made.append(save("groove-dub", "dub one-drop: kick + rim on 3 with delay throws, swung hats", c.gen_dub(random.Random(9), k, prog)))
    made.append(save("groove-citypop", "city pop disco: LinnDrum-ish kick on the beats, snare 2 and 4, 16th hats with open offbeats", c.gen_citypop(random.Random(3), k, prog)))
    made.append(save("groove-dilla", "neo-soul / Dilla: drunk unquantized kick, late snare, drifting hats (sub-step offsets)", c.gen_neosoul(random.Random(4), k, prog)))
    made.append(save("groove-gated", "80s gated-reverb snare and clap on 2 and 4 with swung electro hats (vaporwave)", c.gen_vaporwave(random.Random(5), k, prog)))
    made.append(save("groove-future-garage", "future garage: skippy rim and kick with shuffled hats (cyberscape)", c.gen_cyberscape(random.Random(6), k, prog, "full")))
    made.append(save("groove-berlin-pulse", "Berlin school: a soft electro kick on every beat", c.gen_berlin(random.Random(7), k, prog, "drive")))
    made.append(save("groove-handpan-frame", "handpan meditation: frame drum boom-taps and a soft shaker", c.gen_handpan(random.Random(8), k, prog, "full")))
    made.append(save("groove-temple", "guofeng temple woodblocks over a soft kick", c.gen_guofeng(random.Random(9), k, prog)))
    print(len(made), "grooves")
    return made


if __name__ == "__main__":
    main()
