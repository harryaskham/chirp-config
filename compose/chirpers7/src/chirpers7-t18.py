#!/usr/bin/env python3
"""chirpers7-t18 (The Endless Stair, track 18, the closer) - generator for songs/chirpers7-t18.yaml (chirper-zero).

THE STAIR COMES DOWN - THE ODYSSEY (v12, Harry 31 Oct 14:50: 'the final track should bring in every element and work out
simultaneously running like all illusions at once in interplay, and make it all actually work; a long trippy odyssey to
close the album out'). Deep minimal house, 120 bpm with a decelerando to 112 at the very end, D minor walking home to A
minor (t1's key). Every illusion on the tape returns, one by one, then stacked and interlocking, then all at once, and the
stair comes down for ever to close.

Form (4/4 bars, ~13.5 min):
  DESCENT 32   bars 1-16 the seam from The Room Turns (kick, hats, a held D2, soft rims); then the falling stair.
  GALLERY 240  fifteen 16-bar panels, each one illusion in front over a groove that keeps changing (two chord worlds
               alternate: Dm9 Bbmaj9#11 Gm9 A7b9, and a Phrygian D pedal with Ebmaj7 planing over it):
               t1 Shepard stair UP / t2+t16 barber-pole filter / t3 speech-to-song ('the stair comes down') / t4+t11 tritone
               pairs / t5 streaming (one acid line splitting in two) / t6 missing fundamental (the bass nobody plays, then
               the reveal) / t7 octave illusion / t8 continuity (a line singing on through static) / t9 beat flip /
               t10 Zwicker (notched noise, a bar of silence, the note that wasn't there) / t12 Huggins (a note between
               the ears in hiss) / t13 Risset accelerando / t14 scale illusion / t17 the turning room / t15 Risset
               decelerando.
  INTERLOCK 64 four 16-bar groups that share a register: LOW (missing fundamental, streaming, decelerando), MID (barber
               pole, tritone pairs, the sung phrase), HIGH (Shepard up, octave, scale), TIME (Risset up AND down, beat
               flip, the turning room).
  ALL 32       everything at once, each in its own band and place, the falling stair on top; ends in a Zwicker silence.
  CODA 32      the kick gone, the falling Shepard chords in A minor, the stair coming down, 120 -> 112; it ends on the
               stair's 2, unresolved, so the loop into The First Step finishes the phrase.
Recipes: chirper-two (c2-stair, c2-tritone, static burst, Risset both ways), chirper-three (streaming, missing
fundamental, beat flip, Zwicker), chirper-one (Huggins), chirper-zero (endless filter, Haas turning room, scale illusion,
Risset beds, falling stair). See compose/chirpers7/sounds.md.
Run: python3 compose/chirpers7/src/chirpers7-t18.py  (writes songs/chirpers7-t18.yaml)
"""
import json
import math
import os

ROOT = os.path.expanduser("~/.config/chirp")
OUT = os.environ.get("C7T18_OUT") or os.path.join(ROOT, "songs", "chirpers7-t18.yaml")
BPM0, BPM1 = 120, 112
S = 0.25
BAR = 16
MGAIN = float(os.environ.get("C7T18_MGAIN", "8"))
FCOMP = os.environ.get("C7T18_FCOMP", "-16,0.3ms")
REF = os.environ.get("C7T18_REF", "sfphv")  # the owners' notes on their panels (chirper-three, chirper-one): "s" streaming steps 2/7/12 then the rate cue (eighths fuse it back); "f" beat flip with the ghost one, a counting voice (a hemiola) and 'ONE' on the true downbeat; "p" the bass taken apart (partials 2-6 staggered and panned, then together) before the reveal; "h" the Huggins wash with the pads out of the ghost's way; "v" speech blending into song syllable by syllable
REF2 = os.environ.get("C7T18_REF2", "tr")  # "t" chirper-one's tritone timing (the answer a dotted quarter after its stair note); "r" chirper-two's 'radio dies': the whole mix tape-stops over the two beats before the last silence, the coda starts from nothing
ILV = float(os.environ.get("C7T18_ILV", "0"))  # every illusion track's level offset (dB)

NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
GALLERY = ["shepard", "pole", "speech", "tritone", "stream", "phantom", "octave", "continuity", "flip", "zwicker",
           "huggins", "accel", "scale", "turn", "decel"]
INTER = [("phantom", "stream", "decel"), ("pole", "tritone", "speech"), ("shepard", "octave", "scale"),
         ("accel", "decel", "flip", "turn")]
ALL = ("shepard", "pole", "speech", "tritone", "stream", "phantom", "octave", "continuity", "huggins", "accel", "scale",
       "turn", "decel")
FORM = [("descent", 32)] + [(f"g{i}", 16) for i in range(len(GALLERY))] + [(f"i{i}", 16) for i in range(len(INTER))] + \
       [("all", 32), ("coda", 32)]

# chord worlds (sub root, voicing): darker than a loop of plain minor triads
PROG_A = [(38, [53, 57, 60, 64]),   # Dm9: F3 A3 C4 E4
          (34, [50, 57, 60, 64]),   # Bbmaj9#11: D3 A3 C4 E4 over Bb
          (31, [53, 57, 58, 62]),   # Gm9: F3 A3 Bb3 D4
          (33, [49, 55, 58, 64])]   # A7b9: C#3 G3 Bb3 E4
PROG_P = [(38, [53, 57, 60, 64]),   # Dm9
          (38, [51, 55, 58, 62]),   # Ebmaj7 over the D pedal (Phrygian b2)
          (38, [53, 57, 60, 64]),   # Dm9
          (38, [52, 55, 60, 62])]   # C/D (a sus colour on the pedal)
PROG_HOME = [(33, [48, 52, 55, 59]),   # Am9 (coda)
             (29, [48, 52, 57, 60]),   # Fmaj7/C
             (26, [48, 53, 57, 60]),   # Dm9/C
             (28, [47, 52, 55, 59])]   # Em7/B
STAIR_D = [69, 65, 64, 62]   # A F E D: 5 3 2 1 of D minor, falling
STAIR_A = [64, 60, 59, 57]   # E C B A
UP = [62, 64, 65, 69]        # D E F A rising
SCALE = [62, 64, 65, 67, 69, 70, 72, 74]   # D natural minor, D4-D5
RISSET_DOWN = "rs/0.75b@96 rs/0.75b@84 rs/0.5b@90 rs/0.75b@96 cb/0.75b@80 rs/0.5b@88"
RISSET_UP = "cb/0.75b@86 ht/0.75b@74 R/0.5b ht/0.75b@80 cb/0.75b@68 mt/0.5b@70"


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def R(d):
    return f"R/{d:g}b" if d > 1e-9 else ""


def J(*xs):
    return " ".join(x for x in xs if x)


def sec_start(name):
    t = 0
    for sec, nb in FORM:
        if sec == name:
            return t
        t += nb * BAR
    raise KeyError(name)


def total_steps():
    return sum(nb for _, nb in FORM) * BAR


def active(sec):
    if sec.startswith("g"):
        return {GALLERY[int(sec[1:])]}
    if sec.startswith("i"):
        return set(INTER[int(sec[1:])])
    if sec == "all":
        return set(ALL)
    return set()


def stream(events, total):
    by = {}
    for st, head, ln, vel in events:
        if st in by:
            h0, l0, v0 = by[st]
            n0, _, a0 = h0.partition("^")
            by[st] = (f"{n0},{head.partition('^')[0]}" + (f"^{a0}" if a0 else ""), min(l0, ln), max(v0, vel))
        else:
            by[st] = (head, ln, vel)
    ev = sorted((st, h, l, v) for st, (h, l, v) in by.items())
    out, pos = [], 0
    for i, (st, head, ln, vel) in enumerate(ev):
        if st < pos:
            continue
        nxt = ev[i + 1][0] if i + 1 < len(ev) else total
        hold = max(1, min(ln, max(nxt, st + 1) - st, total - st))
        out.append(R((st - pos) * S))
        note, _, art = head.partition("^")
        out.append(f"{note}/{hold * S:g}b@{max(1, min(127, int(vel)))}" + (f"^{art}" if art else ""))
        pos = st + hold
    out.append(R((total - pos) * S))
    return J(*out)


TRACKS = ("kick", "hats", "clap", "sub", "pads", "stab", "rims", "stair", "fall", "up", "pole", "speech", "tri",
          "acidA", "acidB", "phantom", "octL", "octR", "cont", "burst", "zw", "bell", "wash", "earL", "earR", "loop",
          "hs2", "hs3", "hs4", "hs5", "hs6", "hc2", "hc3", "hc4", "hc5", "hc6")


def build():
    ev = {k: [] for k in TRACKS}
    risset_spans = {"accel": [], "decel": []}
    silent = set()   # Zwicker bars: every part out (the master lane drops to -60 too)

    def add(tr, at, head, ln, vel):
        ev[tr].append((at, head, ln, vel))

    total = total_steps()
    step_dn = 0   # the falling stair counts on, never restarting
    step_up = 0
    for sec, nb in FORM:
        a0 = sec_start(sec)
        act = active(sec)
        gi = int(sec[1:]) if sec[0] in "gi" and sec[1:].isdigit() else 0
        prog = PROG_HOME if sec == "coda" else (PROG_P if (sec.startswith("g") and gi % 2 == 1) else PROG_A)
        lv = 0.8 if sec == "all" else (0.9 if sec.startswith("i") else 1.0)
        if "accel" in act:
            risset_spans["accel"].append((a0, nb))
        if "decel" in act:
            risset_spans["decel"].append((a0, nb))
        for b in range(nb):
            at = a0 + b * BAR
            r, v = prog[b % 4]
            seam_in = sec == "descent" and b < 16
            zw = "zwicker" in act and sec.startswith("g")
            if zw and b % 4 == 3:
                silent.add(b + a0 // BAR)
                continue
            if sec == "all" and b == nb - 1:
                silent.add(b + a0 // BAR)   # the odyssey's last breath before the coda: a Zwicker silence
                continue
            # --- kick (the beat flip moves it; the coda has none)
            kick_qs = (0, 4, 8, 12)
            if "flip" in act:
                ph = b % 16
                kick_qs = () if ph < 4 or 8 <= ph < 10 else ((2, 6, 10, 14) if ph < 8 else (0, 4, 8, 12))
            ghost = "f" in REF and "flip" in act and b % 16 >= 10 and b % 4 == 3   # the ghost one: beat one emptied
            if ghost:
                kick_qs = tuple(q for q in kick_qs if q != 0)
            if sec != "coda":
                for q in kick_qs:
                    add("kick", at + q, "k", 1, 104 if q in (0, 2) else 96)
            if "f" in REF and "flip" in act:
                ph = b % 16
                if ph < 4 or 8 <= ph < 10:   # the counting voice over the kickless bars: one two three every three eighths
                    for q in range(16):
                        k = at + q - a0
                        if k % 6 == 0:
                            ph_, glide = (("w-ah1-n", "+40>-20"), ("t-uw1", "+30>-30"), ("th-r-iy1", "+20>-40"))[(k // 6) % 3]
                            add("speech", at + q, f"D3^ph={ph_}^f0={glide}", 3, 84)
                if ph == 10:
                    add("speech", at, "D3^ph=w-ah1-n^f0=0>-60", 4, 112)   # ONE, as the true downbeat comes home
            # --- hats: off-beats (open in the interlock and all), 16ths speaking in the grooves
            if sec != "coda" or b < 16:
                for q in (2, 6, 10, 14):
                    if "flip" in act and 4 <= b % 16 < 8:
                        continue
                    add("hats", at + q, "oh" if sec in ("all",) or sec.startswith("i") and q in (6, 14) else "h", 1, 66)
                if not seam_in and sec not in ("coda",):
                    for q in (1, 3, 5, 7, 9, 11, 13, 15):
                        add("hats", at + q, "h", 1, 70 if (sec.startswith("i") or sec == "all") else 52)
            if seam_in and b < 8:
                for q in (3, 7, 11, 15):
                    add("rims", at + q, "rs", 1, 64 if q in (3, 11) else 54)
            # --- clap: interlock and all, and the second half of every other panel
            if (sec.startswith("i") or sec == "all" or (sec.startswith("g") and gi % 2 == 0 and b >= 8)) and "flip" not in act:
                add("clap", at + 4, "cp", 1, 84)
                add("clap", at + 12, "cp", 1, 88)
            # --- sub: the held D under the seam, roots elsewhere; the missing fundamental takes it away until the reveal
            if seam_in:
                if b % 4 == 0:
                    add("sub", at, "D2", 4 * BAR, 76)
            elif sec != "coda" and not ("phantom" in act and b < nb - 4 and sec.startswith("g")):
                if not ghost:
                    add("sub", at, nm(r), 7, 94)
                add("sub", at + 10, nm(r), 5, 84)
            # --- pads (two-bar chords) and the off-beat stabs (the beat flip's anchor)
            hug_clear = "h" in REF and "huggins" in act and sec.startswith("g") and b % 4 == 2
            if not seam_in and b % 2 == 0 and sec != "coda" and not hug_clear:
                add("pads", at, ",".join(nm(n + 12) for n in v), 2 * BAR, 66)
            if "flip" in act:
                for q in (2, 6, 10, 14):
                    add("stab", at + q, ",".join(nm(n + 12) for n in v), 1, 86)
            # --- the falling stair: the descent, all, the coda
            if (sec == "descent" and b >= 16) or sec == "all" or sec == "coda":
                stair = STAIR_A if sec == "coda" else STAIR_D
                per = 8 if sec == "coda" else 4
                for q in range(0, 16, per):
                    add("stair", at + q, nm(stair[step_dn % 4]), per, (84 if step_dn % 4 == 0 else 74) * lv)
                    step_dn += 1
            if sec == "coda" and b % 8 == 0:
                add("fall", at, ",".join(nm(n) for n in v), 8 * BAR, 72)
            # ===== the illusions =====
            if "shepard" in act:   # t1: the stair climbing for ever
                for q in range(0, 16, 4):
                    add("up", at + q, nm(UP[step_up % 4]), 4, (86 if step_up % 4 == 0 else 76) * lv)
                    step_up += 1
            if "pole" in act:      # t2/t16: the filter that rises for ever
                ch = ",".join(nm(n + 12) for n in v)
                for q in range(16):
                    if q % 4 == 0 or q in (6, 10, 14):
                        add("pole", at + q, ch, 1, (96 if q % 4 == 2 else 80) * lv)
            if "speech" in act and b % 2 == 0:   # t3: speech that turns into song
                sung = (b >= nb // 2) or not sec.startswith("g")
                syl = [("dh-ah0", 0, 2, 69, "+60>-40"), ("s-t-eh1-r", 2, 2, 65, "+120>-60"),
                       ("k-ah1-m-z", 4, 3, 64, "+40>-120"), ("d-aw1-n", 7, 5, 62, "-40>-300")]
                w = min(1.0, b / max(1, nb - 4)) if (sec.startswith("g") and "v" in REF) else None
                for ph, q, ln, pitch, glide in syl:
                    if w is not None:   # the contour slides onto the stair note and the glides flatten, syllable by syllable
                        pc = round(50 + w * (pitch - 12 - 50))
                        a, z = (int(x) for x in glide.split(">"))
                        gl = f"{round(a * (1 - w)):+d}>{round(z * (1 - w)):+d}"
                        head = f"{nm(pc)}^ph={ph}" + (f"^f0={gl}" if w < 0.95 else "")
                    else:
                        head = f"{nm(pitch - 12)}^ph={ph}" if sung else f"D3^ph={ph}^f0={glide}"
                    add("speech", at + q, head, ln, 92 * lv)
            if "tritone" in act:   # t4/t11: pairs a tritone apart, no up or down
                if "t" in REF2:
                    for k, q in enumerate((0, 8)):
                        n = UP[(b * 2 + k) % 4]
                        first, second = (n, n + 6) if (b + k) % 2 == 0 else (n + 6, n)
                        add("tri", at + q, nm(first), 5, 86 * lv)
                        add("tri", at + q + 6, nm(second), 2, 86 * lv)
                else:
                    for k, q in enumerate((0, 4, 8, 12)):
                        n = UP[(b * 4 + k) % 4]
                        first, second = (n, n + 6) if (b + k) % 2 == 0 else (n + 6, n)
                        add("tri", at + q, nm(first), 2, 84 * lv)
                        add("tri", at + q + 2, nm(second), 2, 84 * lv)
            if "stream" in act:    # t5: one acid line that splits in two
                rate_cue = False
                if sec.startswith("g") and "s" in REF:
                    interval = (2, 7, 12, 12)[min(3, b // 4)]   # one line, wavering, two players ...
                    rate_cue = b >= 12                           # ... then the same gallop in eighths fuses back
                elif sec.startswith("g"):
                    interval = 2 + round(10 * b / max(1, nb - 1))
                else:
                    interval = 12
                if rate_cue:
                    for q in (0, 8):
                        add("acidA", at + q, nm(r + 12), 2, 92 * lv)
                        add("acidB", at + q + 2, nm(r + 12 + interval), 2, 88 * lv)
                        add("acidA", at + q + 4, nm(r + 12), 2, 84 * lv)
                else:
                    for q in range(0, 16, 4):
                        add("acidA", at + q, nm(r + 12), 1, 92 * lv)
                        add("acidB", at + q + 1, nm(r + 12 + interval), 1, 88 * lv)
                        add("acidA", at + q + 2, nm(r + 12), 1, 84 * lv)
            if "phantom" in act:   # t6: the bass nobody plays (harmonics 2-6), the real sub arrives at the end (the reveal)
                for q in (0, 3, 6, 10, 12):
                    add("phantom", at + q, nm(r + 12), 2, 96 * lv)
                if "p" in REF and sec.startswith("g") and b == 8:   # the bass taken apart: partials 2-6 of D2, staggered and panned
                    for h in range(2, 7):
                        add(f"hs{h}", at + (h - 2) * 4, "D2", 2 * BAR - (h - 2) * 4, 84)
                if "p" in REF and sec.startswith("g") and b in (10, 11):   # ... then centred, pulsing together: they fuse into the low D
                    for h in range(2, 7):
                        for q in range(0, 16, 2):
                            add(f"hc{h}", at + q, "D2", 1, 90 if q % 4 == 0 else 78)
            if "octave" in act:    # t7: one tone hopping ear and octave (two tones swapping ears every eighth)
                n = UP[(b // 4) % 4] + 12
                for k, q in enumerate(range(0, 16, 2)):
                    hi_left = k % 2 == 0
                    add("octL", at + q, nm(n + (12 if hi_left else 0)), 2, 80 * lv)
                    add("octR", at + q, nm(n + (0 if hi_left else 12)), 2, 80 * lv)
            if "continuity" in act:   # t8: a line sung on through bursts of static
                n = STAIR_D[(b // 2) % 4] + 12
                for q0, q1 in ((0, 6), (8, 14)):
                    add("cont", at + q0, nm(n), q1 - q0, 82 * lv)
                    add("burst", at + q1, "C4", 2, 104 * lv)
            if "huggins" in act and b % 4 == 2:   # t12: a note heard between the ears in identical hiss
                add("wash", at, "C4", 2 * BAR, 96 * lv)
            if "zwicker" in act and sec.startswith("g"):   # t10: notched noise swelling, then a silent bar; the bell plays the note
                ph = b % 4
                add("zw", at, "C4", BAR, (72, 92, 112)[ph] * lv)
                if ph == 0 and b > 0:
                    add("bell", at, "A5", 4, 88)
            if "scale" in act:     # t14: a rising and a falling scale swapping ears every eighth
                for k, q in enumerate(range(0, 16, 2)):
                    i = k % 8
                    lo, hi = SCALE[i], SCALE[7 - i]
                    left, right = (lo, hi) if i % 2 == 0 else (hi, lo)
                    add("earL", at + q, nm(left), 2, 78 * lv)
                    add("earR", at + q, nm(right), 2, 78 * lv)
            if "turn" in act:      # t17: the room turning (a dotted-eighth loop on Haas pairs)
                for q in range(16):
                    k = (at + q) - a0
                    if k % 3 == 0:
                        add("loop", at + q, "rs" if (k // 3) % 2 == 0 else "sh", 1, (86 if (k // 3) % 4 == 0 else 74) * lv)
    # the stair ends on its 2 (B3), held: the loop into The First Step finishes the phrase
    if ev["stair"] and ev["stair"][-1][1] == nm(STAIR_A[3]):
        a_at, _, a_ln, _ = ev["stair"].pop()
        p_at, p_h, p_ln, p_v = ev["stair"].pop()
        ev["stair"].append((p_at, p_h, p_ln + a_ln, p_v))
    return {k: stream(ev[k], total) for k in TRACKS}, risset_spans, silent


def lane(points, step=True):
    """Section lane in seconds along the tempo map (constant BPM0 until the coda)."""
    spb = 60 / BPM0
    pts = [["0s", points[0][1]]]
    prev = points[0][1]
    for t16, val in points[1:]:
        t = t16 * S * spb
        if step:
            pts.append([f"{max(0.0, t - 0.01):.3f}s", prev])
        pts.append([f"{t:.3f}s", val])
        prev = val
    pts.append([f"{total_steps() * S * spb + 30:.2f}s", pts[-1][1]])
    return {"points": pts}


def song():
    T, rspans, silent = build()
    st = {sec: sec_start(sec) for sec, _ in FORM}
    total_b = total_steps() // 4
    coda_b = st["coda"] // 4
    tempo = [{"at": "0b", "bpm": BPM0}, {"at": f"{coda_b}b", "bpm": BPM0}, {"at": f"{total_b}b", "bpm": BPM1, "ramp": True}]
    pump = {"type": "pump", "on": "kick.k", "depth": "-5dB", "attack": "2ms", "release": "220ms", "curve": 0.7}
    # the section lane: the seam at its neighbour's level, panels level, the interlock and all up, the coda down; the
    # Zwicker bars drop to digital silence
    pts = [(0, 1.5), (16 * BAR, -1), (st["g0"], 0)]
    for sec, nb in FORM:
        if sec.startswith("i") or sec == "all":
            pts.append((st[sec], 0.5 if sec.startswith("i") else 1))
        if sec == "coda":
            pts += [(st["coda"], -2), (st["coda"] + 16 * BAR, -4)]
    for bar in sorted(silent):
        a = bar * BAR
        nxt = next((v for t, v in reversed(sorted(pts)) if t <= a), 0)
        pts += [(a, -60), (a + BAR, nxt)]
    pts = sorted(dict(pts).items())
    dyn = lane(pts)
    last_silent = max(silent) * BAR
    ts_lane = lane([(0, 0), (last_silent - 8, 1), (st["coda"], 0)])   # the tape winds down over the two beats before the last silence
    ilv = lambda g: f"{g + ILV:g}dB"  # noqa: E731

    def risset(kind, at, nbars):
        up = kind == "accel"
        return {"name": f"{kind}{at}", "patch": "machine-kit", "gain": ilv(0 if up else -3), "pan": -0.35 if up else 0.35,
                "at": f"{at // 4}b", "risset": {"cycle": "4bar", "down": not up, "layers": 3, "length": f"{nbars}bar"},
                "fx": [{"type": "filter", "kind": "hp", "cutoff": 400 if up else 90, "q": 0.7}] + ([] if up else [{"type": "filter", "kind": "lp", "cutoff": 3500, "q": 0.7}]),
                "sends": {"room": "-10dB"}, "score": RISSET_UP if up else RISSET_DOWN}

    def endless(name, score, cycle_bars, gain):
        out = []
        for i, p in enumerate((0.0, 1 / 3, 2 / 3)):
            out.append({"name": f"{name}{i}", "patch": "house-chord", "gain": gain, "pan": (-0.3, 0.0, 0.3)[i],
                        "lfo": {"c": {"wave": "saw", "rate": f"{cycle_bars}/1", "phase": p, "unipolar": True},
                                "l": {"wave": "sine", "rate": f"{cycle_bars}/1", "phase": (p + 0.75) % 1, "unipolar": True}},
                        "fx": [{"type": "filter", "kind": "bp", "cutoff": {"value": 160, "mod": [{"src": "lfo.c", "amount": 5}]}, "q": 1.4},
                               {"type": "gain", "gain": {"value": "-24dB", "mod": [{"src": "lfo.l", "amount": 24}]}}],
                        "sends": {"echo": "-12dB"}, "score": score})
        return out

    def turning(score):
        def side(name, pan, late, phase):
            fx = [{"type": "delay", "time": "18ms", "feedback": 0, "mix": 1}] if late else []
            fx.append({"type": "gain", "gain": {"value": "-12dB", "mod": [{"src": "lfo.x", "amount": 12}]}})
            return {"name": name, "patch": "dusty-kit", "gain": ilv(-4), "pan": pan,
                    "lfo": {"x": {"wave": "sine", "rate": "6/1", "phase": phase, "unipolar": True}},
                    "fx": fx, "sends": {"room": "-12dB"}, "score": score}
        return [side("turnLl", -1, False, 0.0), side("turnLr", 1, True, 0.0), side("turnRl", -1, True, 0.5), side("turnRr", 1, False, 0.5)]

    # the Huggins ghost walks the stair (A F E D around A5) along the wash phrases
    gm, hug_hz = [], 880.0
    for k in range(0, total_steps() // BAR, 4):
        gm.append([f"{k * BAR * S * 60 / BPM0:.3f}s", round(math.log2([880, 698.46, 659.26, 587.33][(k // 4) % 4] / hug_hz), 4)])
    zw_f = 880 * 1.08
    doc = {
        "about": "Chirpers - The Endless Stair (Chirpers VII), track 18 by chirper-zero: THE STAIR COMES DOWN, the closing odyssey. "
                 "Every illusion on the tape returns one by one, interlocks, runs all at once, and the stair comes down for ever. "
                 "Generated by compose/chirpers7/src/chirpers7-t18.py; recipes from all four chirpers (compose/chirpers7/sounds.md).",
        "tempo": tempo, "ceiling": "-1dB", "loudness": -11, "tail": "1.5s",
        "patches": {
            "stair-down": {"about": "the stair comes down: Shepard tones (chirper-two's c2-stair recipe), a softer decay",
                           "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "1200hz", "width": 1.2}}],
                                     "amp": {"a": "6ms", "d": "900ms", "s": 0.3, "r": "600ms"}}},
            "fall-pad": {"about": "falling Shepard chords - each note glides down an octave every 8 s, for ever",
                         "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "300hz", "width": 1.2, "cycle": "8s", "down": True}}],
                                   "amp": {"a": "2s", "s": 1, "r": "4s"}}},
            "stair-up": {"about": "chirper-two's c2-stair: the Shepard tone that climbs for ever",
                         "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 8, "center": "600hz", "width": 1.1}}],
                                   "amp": {"a": "4ms", "d": "700ms", "s": 0.25, "r": "400ms", "curve": 2}}},
            "tritone": {"about": "chirper-two's c2-tritone: a wide Shepard tone; a pair a tritone apart has no up or down",
                        "synth": {"layers": [{"type": "shepard", "shepard": {"octaves": 9, "center": "500hz", "width": 1.4}}],
                                  "amp": {"a": "4ms", "d": "400ms", "s": 0.2, "r": "200ms"}}},
            "pure": {"about": "a pure tone for the octave illusion", "synth": {"layers": ["sine"], "amp": {"a": "4ms", "s": 1, "r": "20ms"}}},
            "static": {"about": "chirper-two's static burst: broadband noise 300 Hz-7 kHz, flat while held",
                       "synth": {"layers": [{"type": "noise"}], "filters": ["hp cutoff=300", "lp cutoff=7000"], "amp": {"a": "6ms", "s": 1, "r": "10ms"}}},
            "zwick": {"about": "chirper-three's Zwicker noise: broadband with a notch around the after-tone",
                      "synth": {"layers": [{"type": "noise"}], "amp": {"a": "1.5s", "s": 1, "r": "4ms"}}},
            "hiss": {"about": "chirper-one's Huggins wash: pink hiss, identical to both ears but for an allpass band",
                     "synth": {"layers": [{"type": "noise", "color": "pink"}], "amp": {"a": "2.5s", "d": "1s", "s": 1, "r": "4ms"}}},
        },
        "master": {"fx": [*([{"type": "tapestop", "time": "2b", "up": "0.25b", "curve": 2.0, "mix": 1,
                               "stop": {"value": 0, "mod": [{"src": "auto.ts", "amount": 1}]}}] if "r" in REF2 else []),
                          {"type": "eq", "bands": ["highpass cutoff=30", "peak cutoff=50 q=1 gain=-7dB", "peak cutoff=110 q=1 gain=3dB",
                                                   "peak cutoff=320 q=0.8 gain=-3dB", "peak cutoff=1000 q=0.7 gain=-3dB",
                                                   "peak cutoff=3100 q=1.5 gain=4dB", "highshelf cutoff=4500 gain=7dB", "highshelf cutoff=9000 gain=5dB"]},
                          {"type": "compressor", "threshold": "-20dB", "ratio": 2.5, "attack": "15ms", "release": "150ms", "makeup": "0dB"},
                          {"type": "gain", "gain": f"+{MGAIN:g}dB"},
                          {"type": "compressor", "threshold": f"{FCOMP.split(',')[0]}dB", "ratio": 8, "attack": FCOMP.split(',')[1], "release": "60ms", "makeup": "0dB"},
                          {"type": "gain", "gain": {"value": "0dB", "mod": [{"src": "auto.dyn", "amount": 1}]}}],
                   "auto": {"dyn": dyn, **({"ts": ts_lane} if "r" in REF2 else {})}},
        "buses": {
            "hall": {"fx": ["reverb kind=hall decay=4s mix=1 predelay=30ms", "lp cutoff=7000"]},
            "echo": {"fx": ["delay time=3/16 feedback=0.4 mix=1 tone=2600", "hp cutoff=300", "reverb kind=hall decay=2.5s mix=0.3"]},
            "room": {"fx": ["reverb kind=room decay=1.0s mix=1 predelay=8ms", "hp cutoff=250"]},
            "hugL": {"fx": [{"type": "pan", "pan": -1}], "returns": []},
            "hugR": {"fx": [{"type": "filter", "kind": "allpass", "q": 6, "cutoff": {"value": hug_hz, "mod": [{"src": "auto.gm", "amount": 1}]}},
                            {"type": "pan", "pan": 1}], "returns": [], "auto": {"gm": {"points": gm}}},
        },
        "tracks": [
            {"name": "kick", "patch": "machine-kit", "gain": "-3dB", "score": T["kick"]},
            {"name": "hats", "patch": "machine-kit", "gain": "-1dB", "pan": 0.1, "score": "swing16=0.56 " + T["hats"]},
            {"name": "clap", "patch": "machine-kit", "gain": "-10dB", "sends": {"hall": "-10dB"}, "score": "swing16=0.56 " + T["clap"]},
            {"name": "rims", "patch": "machine-kit", "gain": "-10dB", "sends": {"hall": "-10dB"}, "score": T["rims"]},
            {"name": "sub", "patch": "sub", "gain": "-14dB", "fx": [pump, {"type": "phantom", "cutoff": 100, "harmonics": "-6dB"}], "score": T["sub"]},
            {"name": "pads", "patch": "pad-glass", "gain": "-16dB", "fx": [pump], "sends": {"hall": "-6dB"}, "score": T["pads"]},
            {"name": "stab", "patch": "house-chord", "gain": "-12dB", "fx": [pump], "sends": {"echo": "-8dB"}, "score": T["stab"]},
            {"name": "stair", "patch": "stair-down", "gain": "-12dB", "sends": {"echo": "-8dB", "hall": "-8dB"}, "score": T["stair"]},
            {"name": "fall", "patch": "fall-pad", "gain": "-12dB", "sends": {"hall": "-4dB"}, "score": T["fall"]},
            {"name": "up", "patch": "stair-up", "gain": ilv(-10), "pan": -0.2, "sends": {"echo": "-8dB", "hall": "-10dB"}, "score": T["up"]},
            *endless("pole", T["pole"], 4, ilv(-9)),
            {"name": "speech", "patch": "voice-speech", "gain": ilv(-6), "sends": {"echo": "-10dB", "hall": "-12dB"}, "score": T["speech"]},
            {"name": "tri", "patch": "tritone", "gain": ilv(-10), "pan": 0.2, "sends": {"hall": "-10dB"}, "score": T["tri"]},
            {"name": "acidA", "patch": "acid", "gain": ilv(-12), "pan": -0.1, "score": T["acidA"]},
            {"name": "acidB", "patch": "acid", "gain": ilv(-12), "pan": -0.1, "score": T["acidB"]},
            {"name": "phantom", "patch": "phantom-bass", "gain": ilv(-8), "fx": [pump], "score": T["phantom"]},
            {"name": "octL", "patch": "pure", "gain": ilv(-18), "pan": -1, "score": T["octL"]},
            {"name": "octR", "patch": "pure", "gain": ilv(-18), "pan": 1, "score": T["octR"]},
            {"name": "cont", "patch": "pad-glass", "gain": ilv(-6), "pan": 0.15, "sends": {"hall": "-10dB"}, "score": T["cont"]},
            {"name": "burst", "patch": "static", "gain": ilv(-14), "score": T["burst"]},
            {"name": "zw", "patch": "zwick", "gain": ilv(-12), "fx": [
                {"type": "filter", "kind": "notch", "cutoff": round(zw_f * 0.9, 1), "q": 1.5}, {"type": "filter", "kind": "notch", "cutoff": round(zw_f, 1), "q": 1.5},
                {"type": "filter", "kind": "notch", "cutoff": round(zw_f * 1.1, 1), "q": 1.5}, "hp cutoff=120", "lp cutoff=9000"], "score": T["zw"]},
            {"name": "bell", "patch": "bell", "gain": ilv(-10), "sends": {"hall": "-8dB"}, "score": T["bell"]},
            {"name": "wash", "patch": "hiss", "gain": ilv(-12), "fx": ["hp cutoff=200", "lp cutoff=9000"], "out": "hugL", "sends": {"hugR": "0dB"}, "score": T["wash"]},
            {"name": "earL", "patch": "blip", "gain": ilv(-12), "pan": -1, "sends": {"hall": "-14dB"}, "score": T["earL"]},
            {"name": "earR", "patch": "blip", "gain": ilv(-12), "pan": 1, "sends": {"hall": "-14dB"}, "score": T["earR"]},
            *[{"name": f"hs{h}", "patch": {"extends": "partial", "synth": {"layers": [f"sine ratio={h}"]}}, "gain": ilv(-12),
               "pan": (-0.8, -0.4, 0.0, 0.4, 0.8)[h - 2], "score": T[f"hs{h}"]} for h in range(2, 7) if "p" in REF],
            *[{"name": f"hc{h}", "patch": {"extends": "partial", "synth": {"layers": [f"sine ratio={h}"]}}, "gain": ilv(-12),
               "fx": [pump], "score": T[f"hc{h}"]} for h in range(2, 7) if "p" in REF],
            *turning("swing16=0.56 " + T["loop"]),
            *[risset("accel", a, nb) for a, nb in rspans["accel"]],
            *[risset("decel", a, nb) for a, nb in rspans["decel"]],
        ],
    }
    return doc


def dump(doc):
    lines = [f"{k}: {json.dumps(doc[k])}" for k in ("about", "tempo", "ceiling", "loudness", "tail", "patches", "master") if k in doc]
    lines.append("buses:")
    lines += [f"  {b}: {json.dumps(v)}" for b, v in doc["buses"].items()]
    lines.append("tracks:")
    lines += ["  - " + json.dumps(t) for t in doc["tracks"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    open(OUT, "w").write(dump(song()))
    print("wrote", OUT)
